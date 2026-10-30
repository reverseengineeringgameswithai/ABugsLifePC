#!/usr/bin/env python3
"""Record and replay keyboard input for one verified ABLPC game window.

The production recorder selects KeyPress/KeyRelease events on one explicit
X11 window.  It does not use an evdev device, an XRecord display-wide hook, or
the host desktop.  Replay uses one persistent X11/XTEST connection while the
same explicit window is focused and accepts only events echoed by an observer
on that exact window.

Movie formats v1/v2 are intentionally keyboard-only and wall-clock scheduled.
A new bugs.log milestone and/or an independently captured frame hash can
anchor the schedule.  Version 2 also binds a log-anchored recording's bounded
runtime-log checkpoint.  This tool does not claim access to the game's
internal frame counter.
"""

from __future__ import annotations

import argparse
import ctypes
from ctypes.util import find_library
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import select
import signal
import subprocess
import sys
import time
from typing import Iterator

import evidence_lib as ev


TOOL = "input-movie"
TOOL_VERSION = "1.3.0"
MOVIE_TOOL = "ablpc-input-movie"
SCHEMA_VERSION = 2
SUPPORTED_SCHEMA_VERSIONS = {1, 2}
KNOWN_RETAIL_SHA256 = (
    "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
)
MAX_DURATION_SECONDS = 3600.0
MAX_EVENTS = 100_000
MAX_LOG_CHECKPOINT_BYTES = 64 * 1024 * 1024
MAX_ROUTINE_CHECKPOINTS = 100_000
MAX_ROUTINE_TEXT_LENGTH = 1024
KEYBOARD_MODIFIER_MASK = 0xFF
KEYSYM_RE = re.compile(r"^[A-Za-z0-9_]+$")


class Refusal(RuntimeError):
    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(detail or reason)
        self.reason = reason
        self.detail = detail


class MovieError(ValueError):
    pass


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _status_descriptor(text: str) -> int:
    try:
        value = int(text, 10)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("status fd must be an integer") from exc
    if value < 3:
        raise argparse.ArgumentTypeError("status fd must be at least 3")
    return value


def _emit_status(args: argparse.Namespace, event: str, **fields: object) -> None:
    """Emit one optional inherited-pipe status event for a supervising UI."""

    descriptor = getattr(args, "status_fd", None)
    if descriptor is None:
        return
    payload = _canonical_bytes({"event": event, **fields}) + b"\n"
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError("zero-byte status write")
            view = view[written:]
    except OSError as exc:
        raise Refusal("status_channel_failed", str(exc)) from exc


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_schedule(events: list[dict]) -> str:
    schedule = [
        {
            "sequence": event["sequence"],
            "offset_ns": event["offset_ns"],
            "action": event["action"],
            "keysym": event["keysym"],
        }
        for event in events
    ]
    return _sha256_bytes(_canonical_bytes(schedule))


def _write_new_file(path: Path, data: bytes) -> None:
    """Write a new regular file without following or replacing a final link."""

    if not path.parent.is_dir():
        raise Refusal("movie_parent_missing", f"parent is not a directory: {path.parent}")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags, 0o644)
    except FileExistsError as exc:
        raise Refusal("movie_exists", str(path)) from exc
    except OSError as exc:
        raise Refusal("movie_create_failed", f"{path}: {exc}") from exc
    try:
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)


def _parse_window_id(text: str) -> int:
    try:
        value = int(text, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("window id must be decimal or 0x-prefixed") from exc
    if value <= 0 or value >= 2**64:
        raise argparse.ArgumentTypeError("window id is outside the X11 range")
    return value


def _positive_float(text: str) -> float:
    try:
        value = float(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a number") from exc
    if not (0 < value <= MAX_DURATION_SECONDS):
        raise argparse.ArgumentTypeError(
            f"value must be greater than zero and at most {MAX_DURATION_SECONDS:g}"
        )
    return value


def _nonnegative_float(text: str) -> float:
    try:
        value = float(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a number") from exc
    if not (0 <= value <= MAX_DURATION_SECONDS):
        raise argparse.ArgumentTypeError(
            f"value must be between zero and {MAX_DURATION_SECONDS:g}"
        )
    return value


def _validate_sha256(text: str) -> str:
    lowered = text.lower()
    if not re.fullmatch(r"[0-9a-f]{64}", lowered):
        raise argparse.ArgumentTypeError("expected a 64-character SHA-256")
    return lowered


def _safe_keysym(value: object, where: str) -> str:
    if not isinstance(value, str) or not KEYSYM_RE.fullmatch(value):
        raise MovieError(f"{where} is not a bounded X keysym name")
    return value


def _refusal_payload(reason: str, detail: str = "") -> dict:
    return {"refused": True, "tool": TOOL, "reason": reason, "detail": detail}


def _print_refusal(reason: str, detail: str = "") -> None:
    print(json.dumps(_refusal_payload(reason, detail), sort_keys=True))


@dataclass(frozen=True)
class WindowSnapshot:
    window_id: int
    pid: int
    name: str
    window_class: str
    x: int
    y: int
    width: int
    height: int
    screen: int
    owner_exe: str
    owner_cmdline: tuple[str, ...]
    owner_pgid: int
    game_pgid: int
    same_process_group: bool
    display: str
    focused_window_id: int
    checked_at: str

    def signature(self) -> dict:
        return {
            "class": self.window_class,
            "width": self.width,
            "height": self.height,
            "screen": self.screen,
            "owner_exe_basename": os.path.basename(self.owner_exe),
        }

    def to_dict(self) -> dict:
        return {
            "window_id": self.window_id,
            "window_id_hex": f"0x{self.window_id:x}",
            "pid": self.pid,
            "name": self.name,
            "class": self.window_class,
            "geometry": {
                "x": self.x,
                "y": self.y,
                "width": self.width,
                "height": self.height,
                "screen": self.screen,
            },
            "owner_exe": self.owner_exe,
            "owner_cmdline": list(self.owner_cmdline),
            "owner_pgid": self.owner_pgid,
            "game_pgid": self.game_pgid,
            "same_process_group": self.same_process_group,
            "display": self.display,
            "focused_window_id": self.focused_window_id,
            "focused": self.focused_window_id == self.window_id,
            "checked_at": self.checked_at,
            "signature": self.signature(),
        }


class XDoTool:
    def __init__(self, executable: str, display: str) -> None:
        self.executable = executable
        self.display = display

    def _run(self, *args: str) -> str:
        env = dict(os.environ)
        env["DISPLAY"] = self.display
        try:
            result = subprocess.run(
                [self.executable, *args],
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
                env=env,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise Refusal("xdotool_failed", str(exc)) from exc
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            raise Refusal("xdotool_failed", f"{' '.join(args)}: {detail}")
        return result.stdout.rstrip("\n")

    def focus(self) -> int:
        text = self._run("getwindowfocus").strip()
        try:
            return int(text, 0)
        except ValueError as exc:
            raise Refusal("window_focus_unparseable", repr(text)) from exc

    def snapshot(
        self,
        window_id: int,
        game_pid: int,
        *,
        owner_exe_re: str,
        name_re: str,
        class_re: str,
    ) -> WindowSnapshot:
        wid = str(window_id)
        pid_text = self._run("getwindowpid", wid).strip()
        try:
            pid = int(pid_text, 10)
        except ValueError as exc:
            raise Refusal("window_pid_unparseable", repr(pid_text)) from exc
        if pid <= 0 or not Path(f"/proc/{pid}").exists():
            raise Refusal("window_owner_missing", f"window pid {pid}")

        name = self._run("getwindowname", wid)
        window_class = self._run("getwindowclassname", wid)
        if not re.search(name_re, name):
            raise Refusal("window_name_mismatch", f"{name!r} does not match {name_re!r}")
        if not re.search(class_re, window_class):
            raise Refusal(
                "window_class_mismatch",
                f"{window_class!r} does not match {class_re!r}",
            )

        geometry_raw = self._run("getwindowgeometry", "--shell", wid)
        geometry: dict[str, int] = {}
        for line in geometry_raw.splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key in {"X", "Y", "WIDTH", "HEIGHT", "SCREEN"}:
                try:
                    geometry[key] = int(value, 10)
                except ValueError as exc:
                    raise Refusal("window_geometry_unparseable", line) from exc
        if set(geometry) != {"X", "Y", "WIDTH", "HEIGHT", "SCREEN"}:
            raise Refusal("window_geometry_incomplete", geometry_raw)
        if geometry["WIDTH"] <= 0 or geometry["HEIGHT"] <= 0:
            raise Refusal("window_geometry_invalid", geometry_raw)

        try:
            owner_exe = os.readlink(f"/proc/{pid}/exe")
            raw_cmdline = Path(f"/proc/{pid}/cmdline").read_bytes()
            owner_cmdline = tuple(
                item.decode("utf-8", "replace")
                for item in raw_cmdline.split(b"\0")
                if item
            )
            owner_pgid = os.getpgid(pid)
            game_pgid = os.getpgid(game_pid)
        except OSError as exc:
            raise Refusal("window_owner_unreadable", str(exc)) from exc
        if not re.search(owner_exe_re, owner_exe):
            raise Refusal(
                "window_owner_mismatch",
                f"{owner_exe!r} does not match {owner_exe_re!r}",
            )
        same_group = owner_pgid == game_pgid
        if not same_group:
            raise Refusal(
                "window_process_group_mismatch",
                f"window PGID {owner_pgid} != game PGID {game_pgid}",
            )

        return WindowSnapshot(
            window_id=window_id,
            pid=pid,
            name=name,
            window_class=window_class,
            x=geometry["X"],
            y=geometry["Y"],
            width=geometry["WIDTH"],
            height=geometry["HEIGHT"],
            screen=geometry["SCREEN"],
            owner_exe=owner_exe,
            owner_cmdline=owner_cmdline,
            owner_pgid=owner_pgid,
            game_pgid=game_pgid,
            same_process_group=same_group,
            display=self.display,
            focused_window_id=self.focus(),
            checked_at=ev.now().isoformat(),
        )

    def send(self, window_id: int, action: str, keysym: str) -> None:
        command = "keydown" if action == "down" else "keyup"
        self._run(command, "--window", str(window_id), keysym)


class _XAnyEvent(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("serial", ctypes.c_ulong),
        ("send_event", ctypes.c_int),
        ("display", ctypes.c_void_p),
        ("window", ctypes.c_ulong),
    ]


class _XKeyEvent(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("serial", ctypes.c_ulong),
        ("send_event", ctypes.c_int),
        ("display", ctypes.c_void_p),
        ("window", ctypes.c_ulong),
        ("root", ctypes.c_ulong),
        ("subwindow", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
        ("x_root", ctypes.c_int),
        ("y_root", ctypes.c_int),
        ("state", ctypes.c_uint),
        ("keycode", ctypes.c_uint),
        ("same_screen", ctypes.c_int),
    ]


class _XFocusChangeEvent(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("serial", ctypes.c_ulong),
        ("send_event", ctypes.c_int),
        ("display", ctypes.c_void_p),
        ("window", ctypes.c_ulong),
        ("mode", ctypes.c_int),
        ("detail", ctypes.c_int),
    ]


class _XKeyboardState(ctypes.Structure):
    _fields_ = [
        ("key_click_percent", ctypes.c_int),
        ("bell_percent", ctypes.c_int),
        ("bell_pitch", ctypes.c_uint),
        ("bell_duration", ctypes.c_uint),
        ("led_mask", ctypes.c_ulong),
        ("global_auto_repeat", ctypes.c_int),
        ("auto_repeats", ctypes.c_char * 32),
    ]


class _XEvent(ctypes.Union):
    _fields_ = [
        ("type", ctypes.c_int),
        ("xany", _XAnyEvent),
        ("xkey", _XKeyEvent),
        ("xfocus", _XFocusChangeEvent),
        ("pad", ctypes.c_long * 24),
    ]


@dataclass(frozen=True)
class ObservedEvent:
    kind: str
    observed_ns: int
    keycode: int | None = None
    keysym: str | None = None
    state: int | None = None
    send_event: bool | None = None


class X11WindowObserver:
    KEY_PRESS = 2
    KEY_RELEASE = 3
    FOCUS_OUT = 10
    DESTROY_NOTIFY = 17
    UNMAP_NOTIFY = 18
    KEY_PRESS_MASK = 1 << 0
    KEY_RELEASE_MASK = 1 << 1
    FOCUS_CHANGE_MASK = 1 << 21
    STRUCTURE_NOTIFY_MASK = 1 << 17

    def __init__(self, display_name: str, window_id: int) -> None:
        lib_name = find_library("X11")
        if not lib_name:
            raise Refusal("libx11_missing", "libX11 could not be located")
        self.lib = ctypes.CDLL(lib_name)
        self.lib.XOpenDisplay.argtypes = [ctypes.c_char_p]
        self.lib.XOpenDisplay.restype = ctypes.c_void_p
        self.lib.XCloseDisplay.argtypes = [ctypes.c_void_p]
        self.lib.XCloseDisplay.restype = ctypes.c_int
        self.lib.XSelectInput.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_long]
        self.lib.XSelectInput.restype = ctypes.c_int
        self.lib.XSync.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self.lib.XSync.restype = ctypes.c_int
        self.lib.XPending.argtypes = [ctypes.c_void_p]
        self.lib.XPending.restype = ctypes.c_int
        self.lib.XConnectionNumber.argtypes = [ctypes.c_void_p]
        self.lib.XConnectionNumber.restype = ctypes.c_int
        self.lib.XNextEvent.argtypes = [ctypes.c_void_p, ctypes.POINTER(_XEvent)]
        self.lib.XNextEvent.restype = ctypes.c_int
        self.lib.XLookupKeysym.argtypes = [ctypes.POINTER(_XKeyEvent), ctypes.c_int]
        self.lib.XLookupKeysym.restype = ctypes.c_ulong
        self.lib.XKeysymToString.argtypes = [ctypes.c_ulong]
        self.lib.XKeysymToString.restype = ctypes.c_char_p

        self.window_id = window_id
        self.display_name = display_name
        self.display = self.lib.XOpenDisplay(display_name.encode("utf-8"))
        if not self.display:
            raise Refusal("x11_display_open_failed", display_name)
        mask = (
            self.KEY_PRESS_MASK
            | self.KEY_RELEASE_MASK
            | self.FOCUS_CHANGE_MASK
            | self.STRUCTURE_NOTIFY_MASK
        )
        self.lib.XSelectInput(self.display, window_id, mask)
        self.lib.XSync(self.display, 0)
        self.connection_fd = self.lib.XConnectionNumber(self.display)
        if self.connection_fd < 0:
            self.close()
            raise Refusal("x11_connection_invalid", display_name)

    def close(self) -> None:
        if self.display:
            self.lib.XCloseDisplay(self.display)
            self.display = None

    def __enter__(self) -> "X11WindowObserver":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def poll(self, timeout_seconds: float) -> ObservedEvent | None:
        if self.lib.XPending(self.display) == 0:
            try:
                readable, _, _ = select.select(
                    [self.connection_fd], [], [], max(0.0, timeout_seconds)
                )
            except (OSError, ValueError) as exc:
                raise Refusal("x11_observer_poll_failed", str(exc)) from exc
            if not readable or self.lib.XPending(self.display) == 0:
                return None
        raw = _XEvent()
        self.lib.XNextEvent(self.display, ctypes.byref(raw))
        observed_ns = time.monotonic_ns()
        if raw.type in {self.KEY_PRESS, self.KEY_RELEASE}:
            keysym_value = self.lib.XLookupKeysym(ctypes.byref(raw.xkey), 0)
            keysym_pointer = self.lib.XKeysymToString(keysym_value)
            keysym = keysym_pointer.decode("ascii") if keysym_pointer else ""
            return ObservedEvent(
                kind="down" if raw.type == self.KEY_PRESS else "up",
                observed_ns=observed_ns,
                keycode=int(raw.xkey.keycode),
                keysym=keysym,
                state=int(raw.xkey.state),
                send_event=bool(raw.xkey.send_event),
            )
        if raw.type == self.FOCUS_OUT:
            return ObservedEvent(kind="focus-out", observed_ns=observed_ns)
        if raw.type in {self.DESTROY_NOTIFY, self.UNMAP_NOTIFY}:
            return ObservedEvent(kind="window-gone", observed_ns=observed_ns)
        return ObservedEvent(kind="other", observed_ns=observed_ns)

    def discard_pending(self) -> int:
        discarded = 0
        while self.lib.XPending(self.display) > 0:
            raw = _XEvent()
            self.lib.XNextEvent(self.display, ctypes.byref(raw))
            discarded += 1
        return discarded


class SyntheticObserver:
    """Fixture-only event source selected by ABLPC_INPUT_EVENT_STREAM."""

    def __init__(self, path: Path) -> None:
        try:
            raw_items = [
                json.loads(line)
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        except (OSError, json.JSONDecodeError) as exc:
            raise Refusal("synthetic_event_stream_invalid", str(exc)) from exc
        self.items = iter(raw_items)
        self.pending: dict | None = None
        self.due_ns: int | None = None

    def __enter__(self) -> "SyntheticObserver":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def poll(self, timeout_seconds: float) -> ObservedEvent | None:
        if self.pending is None:
            try:
                self.pending = next(self.items)
            except StopIteration:
                time.sleep(min(timeout_seconds, 0.005))
                return None
            delay_ms = self.pending.get("delay_ms", 0)
            if not isinstance(delay_ms, (int, float)) or not (0 <= delay_ms <= 60_000):
                raise Refusal("synthetic_event_stream_invalid", "bad delay_ms")
            self.due_ns = time.monotonic_ns() + int(delay_ms * 1_000_000)
        assert self.due_ns is not None
        remaining_ns = self.due_ns - time.monotonic_ns()
        if remaining_ns > 0:
            time.sleep(min(timeout_seconds, remaining_ns / 1_000_000_000))
            return None
        item = self.pending
        self.pending = None
        kind = item.get("kind")
        if kind not in {"down", "up", "focus-out", "window-gone"}:
            raise Refusal("synthetic_event_stream_invalid", f"bad kind: {kind!r}")
        if kind in {"down", "up"}:
            keysym = item.get("keysym")
            keycode = item.get("keycode", 1)
            state = item.get("state", 0)
            if not isinstance(keysym, str) or not KEYSYM_RE.fullmatch(keysym):
                raise Refusal("synthetic_event_stream_invalid", "bad keysym")
            if not isinstance(keycode, int) or not (1 <= keycode <= 255):
                raise Refusal("synthetic_event_stream_invalid", "bad keycode")
            if not isinstance(state, int) or not (0 <= state <= 0xFFFFFFFF):
                raise Refusal("synthetic_event_stream_invalid", "bad state")
            return ObservedEvent(
                kind=kind,
                observed_ns=time.monotonic_ns(),
                keycode=keycode,
                keysym=keysym,
                state=state,
                send_event=bool(item.get("send_event", True)),
            )
        return ObservedEvent(kind=kind, observed_ns=time.monotonic_ns())


class X11ReplayBackend:
    """Persistent XTEST sender plus exact-window X11 delivery observer."""

    backend_name = "x11-xtest-persistent-v1"
    echo_backend = "x11-window-select-v1"

    def __init__(self, display_name: str, window_id: int) -> None:
        self.display_name = display_name
        self.window_id = window_id
        self.display: int | None = None
        self.started = False
        self.auto_repeat_before: int | None = None
        self.auto_repeat_disabled = False
        self.auto_repeat_restored = False
        self.discarded_pre_anchor_events = 0
        self.observer = X11WindowObserver(display_name, window_id)

        x11_name = find_library("X11")
        xtst_name = find_library("Xtst")
        if not x11_name:
            self.observer.close()
            raise Refusal("libx11_missing", "libX11 could not be located")
        if not xtst_name:
            self.observer.close()
            raise Refusal("libxtst_missing", "libXtst could not be located")
        self.x11 = ctypes.CDLL(x11_name)
        self.xtst = ctypes.CDLL(xtst_name)
        self.x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
        self.x11.XOpenDisplay.restype = ctypes.c_void_p
        self.x11.XCloseDisplay.argtypes = [ctypes.c_void_p]
        self.x11.XCloseDisplay.restype = ctypes.c_int
        self.x11.XGetInputFocus.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_ulong),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.x11.XGetInputFocus.restype = ctypes.c_int
        self.x11.XStringToKeysym.argtypes = [ctypes.c_char_p]
        self.x11.XStringToKeysym.restype = ctypes.c_ulong
        self.x11.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        self.x11.XKeysymToKeycode.restype = ctypes.c_ubyte
        self.x11.XGetKeyboardControl.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(_XKeyboardState),
        ]
        self.x11.XGetKeyboardControl.restype = ctypes.c_int
        self.x11.XAutoRepeatOff.argtypes = [ctypes.c_void_p]
        self.x11.XAutoRepeatOff.restype = ctypes.c_int
        self.x11.XAutoRepeatOn.argtypes = [ctypes.c_void_p]
        self.x11.XAutoRepeatOn.restype = ctypes.c_int
        self.x11.XFlush.argtypes = [ctypes.c_void_p]
        self.x11.XFlush.restype = ctypes.c_int
        self.x11.XSync.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self.x11.XSync.restype = ctypes.c_int
        self.xtst.XTestQueryExtension.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.xtst.XTestQueryExtension.restype = ctypes.c_int
        self.xtst.XTestFakeKeyEvent.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint,
            ctypes.c_int,
            ctypes.c_ulong,
        ]
        self.xtst.XTestFakeKeyEvent.restype = ctypes.c_int

        self.display = self.x11.XOpenDisplay(display_name.encode("utf-8"))
        if not self.display:
            self.observer.close()
            raise Refusal("x11_replay_display_open_failed", display_name)
        event_base = ctypes.c_int()
        error_base = ctypes.c_int()
        major = ctypes.c_int()
        minor = ctypes.c_int()
        supported = self.xtst.XTestQueryExtension(
            self.display,
            ctypes.byref(event_base),
            ctypes.byref(error_base),
            ctypes.byref(major),
            ctypes.byref(minor),
        )
        if not supported:
            self.close()
            raise Refusal("xtest_extension_missing", display_name)
        self.xtest_version = f"{major.value}.{minor.value}"

    def __enter__(self) -> "X11ReplayBackend":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def begin(self) -> None:
        if self.started:
            return
        self.discarded_pre_anchor_events = self.observer.discard_pending()
        state = _XKeyboardState()
        if not self.x11.XGetKeyboardControl(self.display, ctypes.byref(state)):
            raise Refusal("x11_keyboard_state_failed", self.display_name)
        self.auto_repeat_before = int(state.global_auto_repeat)
        if self.auto_repeat_before:
            self.x11.XAutoRepeatOff(self.display)
            self.x11.XSync(self.display, 0)
            self.auto_repeat_disabled = True
        self.started = True

    def close(self) -> None:
        if self.display:
            if self.started and self.auto_repeat_before:
                self.x11.XAutoRepeatOn(self.display)
                self.x11.XSync(self.display, 0)
                self.auto_repeat_restored = True
            self.x11.XCloseDisplay(self.display)
            self.display = None
        self.observer.close()

    def focus(self) -> int:
        focused = ctypes.c_ulong()
        revert_to = ctypes.c_int()
        if not self.x11.XGetInputFocus(
            self.display, ctypes.byref(focused), ctypes.byref(revert_to)
        ):
            raise Refusal("x11_focus_query_failed", self.display_name)
        return int(focused.value)

    def _keycode(self, keysym: str, recorded_keycode: int = 0) -> int:
        value = self.x11.XStringToKeysym(keysym.encode("ascii"))
        if value == 0:
            raise Refusal("keysym_unmapped", keysym)
        mapped = int(self.x11.XKeysymToKeycode(self.display, value))
        if not (1 <= mapped <= 255):
            raise Refusal("keysym_unmapped", keysym)
        if recorded_keycode and recorded_keycode != mapped:
            raise Refusal(
                "keycode_mapping_mismatch",
                f"{keysym}: recorded {recorded_keycode}, current {mapped}",
            )
        return recorded_keycode or mapped

    def send(self, event: dict) -> dict:
        keycode = self._keycode(event["keysym"], event["keycode"])
        requested_ns = time.monotonic_ns()
        accepted = self.xtst.XTestFakeKeyEvent(
            self.display, keycode, int(event["action"] == "down"), 0
        )
        if not accepted:
            raise Refusal(
                "xtest_send_failed", f"{event['action']} {event['keysym']}"
            )
        self.x11.XFlush(self.display)
        return {
            "requested_ns": requested_ns,
            "flushed_ns": time.monotonic_ns(),
            "keycode": keycode,
        }

    def release(self, keysym: str, keycode: int) -> bool:
        try:
            resolved = self._keycode(keysym, keycode)
            accepted = self.xtst.XTestFakeKeyEvent(self.display, resolved, 0, 0)
            self.x11.XSync(self.display, 0)
            return bool(accepted)
        except Refusal:
            return False

    def poll(self, timeout_seconds: float) -> ObservedEvent | None:
        return self.observer.poll(timeout_seconds)

    def receipt(self) -> dict:
        return {
            "backend": self.backend_name,
            "echo_backend": self.echo_backend,
            "xtest_version": getattr(self, "xtest_version", None),
            "auto_repeat_before": self.auto_repeat_before,
            "auto_repeat_disabled": self.auto_repeat_disabled,
            "auto_repeat_restored": self.auto_repeat_restored,
            "discarded_pre_anchor_events": self.discarded_pre_anchor_events,
        }


class SyntheticReplayBackend:
    """Fixture-only exact reflection or scripted target echo."""

    backend_name = "synthetic-persistent-replay-v1"
    echo_backend = "synthetic-replay-echo-v1"

    def __init__(self, xdo: XDoTool, scripted_path: Path | None) -> None:
        self.xdo = xdo
        self.scripted = SyntheticObserver(scripted_path) if scripted_path else None
        self.reflected: list[ObservedEvent] = []
        self.started = False
        self.sent_count = 0

    def __enter__(self) -> "SyntheticReplayBackend":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def begin(self) -> None:
        self.started = True

    def close(self) -> None:
        return None

    def focus(self) -> int:
        return self.xdo.focus()

    def send(self, event: dict) -> dict:
        requested_ns = time.monotonic_ns()
        self.sent_count += 1
        if self.scripted is None:
            self.reflected.append(
                ObservedEvent(
                    kind=event["action"],
                    observed_ns=time.monotonic_ns(),
                    keycode=event["keycode"] or 1,
                    keysym=event["keysym"],
                    state=event["state"],
                    send_event=event["send_event"],
                )
            )
        return {
            "requested_ns": requested_ns,
            "flushed_ns": time.monotonic_ns(),
            "keycode": event["keycode"] or 1,
        }

    def release(self, keysym: str, keycode: int) -> bool:
        return True

    def poll(self, timeout_seconds: float) -> ObservedEvent | None:
        if self.reflected:
            return self.reflected.pop(0)
        if self.scripted is not None and self.sent_count:
            return self.scripted.poll(timeout_seconds)
        if timeout_seconds > 0:
            time.sleep(timeout_seconds)
        return None

    def receipt(self) -> dict:
        return {
            "backend": self.backend_name,
            "echo_backend": self.echo_backend,
            "xtest_version": None,
            "auto_repeat_before": None,
            "auto_repeat_disabled": False,
            "auto_repeat_restored": False,
            "discarded_pre_anchor_events": 0,
        }


class LogMilestone:
    def __init__(self, path: Path, marker: str) -> None:
        if not path.is_file():
            raise Refusal("log_missing", str(path))
        self.path = path
        self.marker = marker.encode("utf-8")
        self.start_offset = path.stat().st_size
        self.read_offset = self.start_offset
        self.tail = b""
        self.matched_offset: int | None = None

    def poll(self) -> bool:
        try:
            size = self.path.stat().st_size
            if size < self.read_offset:
                raise Refusal("log_truncated", str(self.path))
            if size == self.read_offset:
                return False
            with self.path.open("rb") as handle:
                handle.seek(self.read_offset)
                new = handle.read(size - self.read_offset)
        except OSError as exc:
            raise Refusal("log_unreadable", str(exc)) from exc
        combined = self.tail + new
        index = combined.find(self.marker)
        if index >= 0:
            self.matched_offset = self.read_offset - len(self.tail) + index
            self.read_offset = size
            return True
        retain = max(0, len(self.marker) - 1)
        self.tail = combined[-retain:] if retain else b""
        self.read_offset = size
        return False

    def receipt(self) -> dict:
        return {
            "type": "log-milestone",
            "log_basename": self.path.name,
            "marker": self.marker.decode("utf-8"),
            "start_offset": self.start_offset,
            "matched_offset": self.matched_offset,
        }


def _ownership(args: argparse.Namespace, expected_sha: str) -> ev.OwnershipProof:
    try:
        return ev.ownership_proof(
            args.pid,
            expected_sha256=expected_sha,
            exe_basename=args.exe_basename,
            loader_re=args.loader_re,
            cwd_prefix=args.cwd_prefix,
        )
    except ev.OwnershipError as exc:
        raise Refusal(exc.reason, exc.detail) from exc


def _window_snapshot(
    args: argparse.Namespace, xdo: XDoTool
) -> WindowSnapshot:
    return xdo.snapshot(
        args.window_id,
        args.pid,
        owner_exe_re=args.window_owner_re,
        name_re=args.window_name_re,
        class_re=args.window_class_re,
    )


def _frame_anchor(path_text: str | None) -> dict | None:
    if not path_text:
        return None
    path = Path(path_text)
    if not path.is_file() or path.is_symlink():
        raise Refusal("anchor_frame_invalid", str(path))
    return {"sha256": ev.sha256_file(path), "size": path.stat().st_size}


def _runtime_log_checkpoint(
    path_text: str,
    observed_anchor: dict,
) -> tuple[dict, bytes]:
    """Capture the bounded post-anchor PC log segment and stable routine trace."""

    path = Path(path_text)
    start_offset = observed_anchor.get("matched_offset")
    if not isinstance(start_offset, int) or start_offset < 0:
        raise Refusal("log_checkpoint_anchor_invalid", str(start_offset))
    try:
        end_offset = path.stat().st_size
        if end_offset < start_offset:
            raise Refusal(
                "log_checkpoint_truncated", f"{end_offset} < {start_offset}"
            )
        size = end_offset - start_offset
        if size > MAX_LOG_CHECKPOINT_BYTES:
            raise Refusal("log_checkpoint_too_large", str(size))
        with path.open("rb") as handle:
            handle.seek(start_offset)
            segment = handle.read(size)
    except OSError as exc:
        raise Refusal("log_checkpoint_unreadable", str(exc)) from exc
    if len(segment) != size:
        raise Refusal(
            "log_checkpoint_short_read", f"expected {size}, read {len(segment)}"
        )

    routine_trace: list[str] = []
    for line in segment.splitlines():
        if line.startswith(b"ROUTINE : "):
            routine = line[len(b"ROUTINE : ") :].decode("utf-8", "replace")
            if len(routine) > MAX_ROUTINE_TEXT_LENGTH:
                raise Refusal("log_checkpoint_routine_too_long", str(len(routine)))
            routine_trace.append(routine)
            if len(routine_trace) > MAX_ROUTINE_CHECKPOINTS:
                raise Refusal(
                    "log_checkpoint_routine_limit", str(MAX_ROUTINE_CHECKPOINTS)
                )
    trace_bytes = _canonical_bytes(routine_trace)
    return ({
        "log_basename": path.name,
        "start_offset": start_offset,
        "end_offset": end_offset,
        "size": size,
        "segment_sha256": _sha256_bytes(segment),
        "routine_count": len(routine_trace),
        "routine_trace": routine_trace,
        "routine_trace_sha256": _sha256_bytes(trace_bytes),
        "captured_at": ev.now().isoformat(),
        "artifact_basename": "runtime-log-segment.bin",
    }, segment)


def _checkpoint_contract(checkpoint: dict) -> dict:
    return {
        "size": checkpoint["size"],
        "segment_sha256": checkpoint["segment_sha256"],
        "routine_count": checkpoint["routine_count"],
        "routine_trace": checkpoint["routine_trace"],
        "routine_trace_sha256": checkpoint["routine_trace_sha256"],
    }


def _checkpoint_digests_match(expected: dict, observed: dict) -> bool:
    return all(
        expected[key] == observed[key]
        for key in {"segment_sha256", "routine_trace_sha256"}
    )


def _make_observer(args: argparse.Namespace):
    synthetic = os.environ.get("ABLPC_INPUT_EVENT_STREAM")
    if synthetic:
        return SyntheticObserver(Path(synthetic)), "synthetic-jsonl-v1"
    return X11WindowObserver(args.display, args.window_id), "x11-window-select-v1"


def _make_replay_backend(args: argparse.Namespace, movie: dict, xdo: XDoTool):
    if movie["recording_backend"] == "synthetic-jsonl-v1":
        scripted = os.environ.get("ABLPC_INPUT_REPLAY_ECHO_STREAM")
        return SyntheticReplayBackend(xdo, Path(scripted) if scripted else None)
    return X11ReplayBackend(args.display, args.window_id)


def _wait_until(deadline_ns: int) -> None:
    while True:
        remaining = deadline_ns - time.monotonic_ns()
        if remaining <= 0:
            return
        if remaining > 2_000_000:
            time.sleep((remaining - 1_000_000) / 1_000_000_000)
        else:
            time.sleep(remaining / 1_000_000_000)


def _new_run_metadata(
    mode: str,
    ownership: ev.OwnershipProof,
    window: WindowSnapshot,
) -> tuple[Path, dict]:
    try:
        run_dir = ev.new_run_dir("INP-REC" if mode == "record" else "INP-REP")
    except FileExistsError as exc:
        raise Refusal("run_collision", str(exc)) from exc
    metadata = {
        "run_id": run_dir.name,
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "implementation_sha256": ev.sha256_file(Path(__file__).resolve()),
        "schema_version": SCHEMA_VERSION,
        "mode": mode,
        "started": ev.now().isoformat(),
        "status": "running",
        "ownership": ownership.to_dict(),
        "window_before": window.to_dict(),
    }
    (run_dir / "metadata.json").write_bytes(_json_bytes(metadata))
    return run_dir, metadata


def _save_metadata(run_dir: Path, metadata: dict) -> None:
    (run_dir / "metadata.json").write_bytes(_json_bytes(metadata))


def _anchor_for_record(
    args: argparse.Namespace,
    observer,
    xdo: XDoTool,
) -> tuple[int, dict, set[str]]:
    preheld: set[str] = set()
    milestone = LogMilestone(Path(args.log), args.start_milestone) if args.start_milestone else None
    _emit_status(
        args,
        "armed",
        mode="record",
        anchor_type="log-milestone" if milestone else "manual-delay",
        marker=args.start_milestone,
        arm_delay_ms=int(args.arm_delay * 1000),
    )
    began_ns = time.monotonic_ns()
    deadline_ns = began_ns + int(args.anchor_timeout * 1_000_000_000)
    delay_deadline_ns = began_ns + int(args.arm_delay * 1_000_000_000)
    marker_seen_ns: int | None = None

    while True:
        event = observer.poll(0.01)
        if event is not None:
            if event.kind in {"focus-out", "window-gone"}:
                if event.kind == "window-gone":
                    raise Refusal("window_disappeared_before_anchor", "")
            elif event.kind in {"down", "up"} and event.keysym:
                if event.kind == "down":
                    preheld.add(event.keysym)
                else:
                    preheld.discard(event.keysym)

        now_ns = time.monotonic_ns()
        if milestone is not None:
            if marker_seen_ns is None and milestone.poll():
                marker_seen_ns = now_ns
            ready = marker_seen_ns is not None
        else:
            ready = now_ns >= delay_deadline_ns

        if ready and not preheld:
            focused = xdo.focus()
            if focused != args.window_id:
                if milestone is not None:
                    raise Refusal(
                        "anchor_focus_mismatch",
                        f"focused 0x{focused:x}, expected 0x{args.window_id:x}",
                    )
            else:
                anchor = milestone.receipt() if milestone else {
                    "type": "manual-delay",
                    "arm_delay_ms": int(args.arm_delay * 1000),
                }
                anchor["anchored_at"] = ev.now().isoformat()
                anchor["frame"] = _frame_anchor(args.anchor_frame)
                if marker_seen_ns is not None:
                    anchor["neutral_wait_ns"] = now_ns - marker_seen_ns
                return now_ns, anchor, preheld

        if now_ns >= deadline_ns:
            reason = "anchor_timeout" if milestone else "focus_timeout"
            raise Refusal(reason, "recording anchor was not reached with neutral input")


def _normal_event(event: ObservedEvent, anchor_ns: int, sequence: int) -> dict:
    assert event.keysym is not None and event.keycode is not None
    keysym = _safe_keysym(event.keysym, f"event[{sequence}].keysym")
    if not (1 <= event.keycode <= 255):
        raise Refusal("keycode_out_of_range", str(event.keycode))
    return {
        "sequence": sequence,
        "offset_ns": max(0, event.observed_ns - anchor_ns),
        "action": event.kind,
        "keysym": keysym,
        "keycode": event.keycode,
        "state": int(event.state or 0),
        "send_event": bool(event.send_event),
        "source": "window-event",
    }


class ReplayEchoVerifier:
    def __init__(
        self,
        backend,
        *,
        anchor_ns: int,
        max_delivery_drift_ns: int,
        echo_timeout_ns: int,
    ) -> None:
        self.backend = backend
        self.anchor_ns = anchor_ns
        self.max_delivery_drift_ns = max_delivery_drift_ns
        self.echo_timeout_ns = echo_timeout_ns
        self.held: set[str] = set()
        self.events: list[dict] = []
        self.ignored_unmatched_releases: list[dict] = []

    def _normalized(self, timeout_seconds: float) -> dict | None:
        event = self.backend.poll(timeout_seconds)
        if event is None:
            return None
        if event.kind == "focus-out":
            raise Refusal("focus_lost_during_replay", "target echo saw FocusOut")
        if event.kind == "window-gone":
            raise Refusal("window_disappeared_during_replay", "")
        if event.kind == "other":
            return {}
        item = _normal_event(event, self.anchor_ns, len(self.events))
        if item["action"] == "up" and item["keysym"] not in self.held:
            self.ignored_unmatched_releases.append(item)
            return {}
        if item["action"] == "down":
            self.held.add(item["keysym"])
        else:
            self.held.remove(item["keysym"])
        return item

    def assert_quiet(self) -> None:
        while True:
            item = self._normalized(0.0)
            if item is None:
                return
            if not item:
                continue
            raise Refusal(
                "unexpected_target_event",
                json.dumps(
                    {
                        "action": item["action"],
                        "keysym": item["keysym"],
                        "keycode": item["keycode"],
                        "observed_offset_ns": item["offset_ns"],
                    },
                    sort_keys=True,
                ),
            )

    def expect(self, expected: dict) -> dict:
        deadline_ns = time.monotonic_ns() + self.echo_timeout_ns
        while True:
            remaining_ns = deadline_ns - time.monotonic_ns()
            if remaining_ns <= 0:
                raise Refusal(
                    "target_echo_timeout",
                    f"event {expected['sequence']} {expected['action']} "
                    f"{expected['keysym']}",
                )
            item = self._normalized(remaining_ns / 1_000_000_000)
            if item is None:
                continue
            if not item:
                continue
            expected_keycode = expected["keycode"]
            same = (
                item["action"] == expected["action"]
                and item["keysym"] == expected["keysym"]
                and (expected_keycode == 0 or item["keycode"] == expected_keycode)
                and (
                    item["state"] & KEYBOARD_MODIFIER_MASK
                    == expected["state"] & KEYBOARD_MODIFIER_MASK
                )
                and item["send_event"] == expected["send_event"]
            )
            if not same:
                raise Refusal(
                    "target_echo_mismatch",
                    json.dumps(
                        {
                            "sequence": expected["sequence"],
                            "expected": {
                                "action": expected["action"],
                                "keysym": expected["keysym"],
                                "keycode": expected_keycode,
                                "keyboard_state": (
                                    expected["state"] & KEYBOARD_MODIFIER_MASK
                                ),
                                "send_event": expected["send_event"],
                            },
                            "observed": {
                                "action": item["action"],
                                "keysym": item["keysym"],
                                "keycode": item["keycode"],
                                "keyboard_state": (
                                    item["state"] & KEYBOARD_MODIFIER_MASK
                                ),
                                "send_event": item["send_event"],
                            },
                        },
                        sort_keys=True,
                    ),
                )
            delivery_drift_ns = item["offset_ns"] - expected["offset_ns"]
            if abs(delivery_drift_ns) > self.max_delivery_drift_ns:
                raise Refusal(
                    "target_delivery_timing_drift",
                    f"event {expected['sequence']} drifted {delivery_drift_ns} ns",
                )
            item["sequence"] = expected["sequence"]
            self.events.append(item)
            return {
                "sequence": expected["sequence"],
                "action": item["action"],
                "keysym": item["keysym"],
                "keycode": item["keycode"],
                "state": item["state"],
                "send_event": item["send_event"],
                "scheduled_offset_ns": expected["offset_ns"],
                "observed_offset_ns": item["offset_ns"],
                "delivery_drift_ns": delivery_drift_ns,
            }


def _release_held(
    xdo: XDoTool,
    window_id: int,
    held: set[str],
    *,
    anchor_ns: int | None = None,
    events: list[dict] | None = None,
) -> list[dict]:
    releases: list[dict] = []
    for keysym in sorted(held):
        try:
            xdo.send(window_id, "up", keysym)
            ok = True
        except Refusal:
            ok = False
        item = {"keysym": keysym, "released": ok, "released_at": ev.now().isoformat()}
        releases.append(item)
        if ok and anchor_ns is not None and events is not None:
            events.append(
                {
                    "sequence": len(events),
                    "offset_ns": max(0, time.monotonic_ns() - anchor_ns),
                    "action": "up",
                    "keysym": keysym,
                    "keycode": 0,
                    "state": 0,
                    "send_event": True,
                    "source": "emergency-release",
                }
            )
    held.clear()
    return releases


def _release_replay_held(
    backend,
    held: dict[str, int],
    echo_held: set[str],
) -> list[dict]:
    releases: list[dict] = []
    for keysym in sorted(set(held) | echo_held):
        keycode = held.get(keysym, 0)
        ok = backend.release(keysym, keycode)
        releases.append(
            {
                "keysym": keysym,
                "keycode": keycode,
                "released": ok,
                "released_at": ev.now().isoformat(),
            }
        )
    held.clear()
    echo_held.clear()
    return releases


def record(args: argparse.Namespace) -> int:
    movie_path = Path(args.movie).absolute()
    root = ev.repo_root()
    originals = (root / "originals").resolve()
    try:
        if movie_path.resolve(strict=False).is_relative_to(originals):
            raise Refusal("movie_under_originals", str(movie_path))
    except OSError as exc:
        raise Refusal("movie_path_invalid", str(exc)) from exc
    if movie_path.exists() or movie_path.is_symlink():
        raise Refusal("movie_exists", str(movie_path))

    ownership = _ownership(args, args.expected_sha)
    xdo = XDoTool(args.xdotool, args.display)
    window_before = _window_snapshot(args, xdo)
    observer, backend = _make_observer(args)
    run_dir: Path | None = None
    metadata: dict | None = None
    held: set[str] = set()
    events: list[dict] = []
    ignored_unmatched_releases: list[dict] = []
    termination = ""
    releases: list[dict] = []
    runtime_log_checkpoint: dict | None = None

    try:
        with observer:
            anchor_ns, anchor, _ = _anchor_for_record(args, observer, xdo)
            _emit_status(args, "recording-started", mode="record", anchor=anchor)
            run_dir, metadata = _new_run_metadata("record", ownership, window_before)
            metadata.update({"recording_backend": backend, "anchor": anchor})
            _save_metadata(run_dir, metadata)
            deadline_ns = anchor_ns + int(args.max_duration * 1_000_000_000)

            while True:
                if time.monotonic_ns() >= deadline_ns:
                    termination = "max-duration"
                    break
                event = observer.poll(0.01)
                if event is None or event.kind == "other":
                    continue
                if event.kind == "focus-out":
                    raise Refusal("focus_lost_during_recording", "")
                if event.kind == "window-gone":
                    raise Refusal("window_disappeared_during_recording", "")
                assert event.keysym is not None
                if event.keysym == args.stop_keysym:
                    if event.kind == "down":
                        termination = "stop-keysym"
                        try:
                            xdo.send(args.window_id, "up", args.stop_keysym)
                        except Refusal:
                            pass
                        break
                    continue
                item = _normal_event(event, anchor_ns, len(events))
                if item["action"] == "down":
                    held.add(item["keysym"])
                else:
                    if item["keysym"] not in held:
                        # xdotool/XTEST may emit a preparatory release before a
                        # synthetic key press.  It cannot make a key more held,
                        # so retain it only as normalization metadata.  The
                        # corresponding replay keydown performs the same XTEST
                        # neutralization on the fresh target.
                        ignored_unmatched_releases.append(item)
                        continue
                    held.remove(item["keysym"])
                events.append(item)
                if len(events) > MAX_EVENTS:
                    raise Refusal("event_limit", str(MAX_EVENTS))

        releases = _release_held(
            xdo, args.window_id, held, anchor_ns=anchor_ns, events=events
        )
        duration_ns = max(
            time.monotonic_ns() - anchor_ns,
            events[-1]["offset_ns"] if events else 0,
        )
        if anchor["type"] == "log-milestone":
            runtime_log_checkpoint, log_segment = _runtime_log_checkpoint(
                args.log, anchor
            )
            assert run_dir is not None
            _write_new_file(run_dir / "runtime-log-segment.bin", log_segment)
        movie = {
            "schema_version": SCHEMA_VERSION,
            "tool": MOVIE_TOOL,
            "recording_backend": backend,
            "recorded_at": ev.now().isoformat(),
            "clock": "monotonic-offset-ns",
            "target": {
                "exe_basename": args.exe_basename,
                "executable_sha256": ownership.exe_sha256,
                "window_signature": window_before.signature(),
            },
            "anchor": anchor,
            "runtime_log_checkpoint": (
                _checkpoint_contract(runtime_log_checkpoint)
                if runtime_log_checkpoint is not None
                else None
            ),
            "events": events,
            "duration_ns": duration_ns,
            "schedule_sha256": _sha256_schedule(events),
            "termination": termination,
            "complete": True,
        }
        try:
            validate_movie(movie)
        except MovieError as exc:
            raise Refusal("recorded_movie_invalid", str(exc)) from exc
        window_after = _window_snapshot(args, xdo)
        movie_bytes = _json_bytes(movie)
        _write_new_file(movie_path, movie_bytes)
        metadata.update(
            {
                "ended": ev.now().isoformat(),
                "status": "complete",
                "accepted": backend == "x11-window-select-v1",
                "movie_path": str(movie_path),
                "movie_sha256": _sha256_bytes(movie_bytes),
                "schedule_sha256": movie["schedule_sha256"],
                "event_count": len(events),
                "ignored_unmatched_release_count": len(ignored_unmatched_releases),
                "ignored_unmatched_releases": ignored_unmatched_releases,
                "duration_ns": duration_ns,
                "termination": termination,
                "runtime_log_checkpoint": runtime_log_checkpoint,
                "emergency_releases": releases,
                "all_keys_released": not held and all(
                    item["released"] for item in releases
                ),
                "window_after": window_after.to_dict(),
            }
        )
        _save_metadata(run_dir, metadata)
        print(json.dumps({
            "run_id": run_dir.name,
            "movie": str(movie_path),
            "movie_sha256": metadata["movie_sha256"],
            "event_count": len(events),
            "accepted": metadata["accepted"],
        }, sort_keys=True))
        return ev.EXIT_OK
    except KeyboardInterrupt:
        termination = "interrupt"
        releases = _release_held(xdo, args.window_id, held)
        if run_dir is not None and metadata is not None:
            metadata.update({
                "ended": ev.now().isoformat(),
                "status": "interrupted",
                "accepted": False,
                "termination": termination,
                "emergency_releases": releases,
                "all_keys_released": all(item["released"] for item in releases),
            })
            _save_metadata(run_dir, metadata)
        return ev.EXIT_TOOL_NEGATIVE
    except Refusal as exc:
        releases = _release_held(xdo, args.window_id, held)
        if run_dir is not None and metadata is not None:
            metadata.update({
                "ended": ev.now().isoformat(),
                "status": "recording-failed",
                "accepted": False,
                "emergency_releases": releases,
                "all_keys_released": all(item["released"] for item in releases),
                "failure": {"reason": exc.reason, "detail": exc.detail},
            })
            _save_metadata(run_dir, metadata)
        raise


def _strict_keys(obj: dict, expected: set[str], where: str) -> None:
    if set(obj) != expected:
        missing = sorted(expected - set(obj))
        extra = sorted(set(obj) - expected)
        raise MovieError(f"{where} keys differ; missing={missing}, extra={extra}")


def _validate_checkpoint_contract(value: object, where: str) -> None:
    if not isinstance(value, dict):
        raise MovieError(f"{where} must be an object")
    _strict_keys(value, {
        "size", "segment_sha256", "routine_count", "routine_trace",
        "routine_trace_sha256",
    }, where)
    if not isinstance(value["size"], int) or not (
        0 <= value["size"] <= MAX_LOG_CHECKPOINT_BYTES
    ):
        raise MovieError(f"{where}.size is invalid")
    for key in {"segment_sha256", "routine_trace_sha256"}:
        if not isinstance(value[key], str) or not re.fullmatch(
            r"[0-9a-f]{64}", value[key]
        ):
            raise MovieError(f"{where}.{key} is invalid")
    trace = value["routine_trace"]
    if not isinstance(trace, list) or len(trace) > MAX_ROUTINE_CHECKPOINTS:
        raise MovieError(f"{where}.routine_trace is invalid")
    for index, item in enumerate(trace):
        if (
            not isinstance(item, str)
            or len(item) > MAX_ROUTINE_TEXT_LENGTH
            or "\n" in item
            or "\r" in item
        ):
            raise MovieError(f"{where}.routine_trace[{index}] is invalid")
    if value["routine_count"] != len(trace):
        raise MovieError(f"{where}.routine_count is invalid")
    if value["routine_trace_sha256"] != _sha256_bytes(_canonical_bytes(trace)):
        raise MovieError(f"{where}.routine_trace_sha256 mismatch")


def validate_movie(raw: object) -> dict:
    if not isinstance(raw, dict):
        raise MovieError("movie root must be an object")
    schema_version = raw.get("schema_version")
    if (
        not isinstance(schema_version, int)
        or isinstance(schema_version, bool)
        or schema_version not in SUPPORTED_SCHEMA_VERSIONS
        or raw.get("tool") != MOVIE_TOOL
    ):
        raise MovieError("unsupported movie schema/tool")
    movie_keys = {
        "schema_version", "tool", "recording_backend", "recorded_at", "clock",
        "target", "anchor", "events", "duration_ns", "schedule_sha256",
        "termination", "complete",
    }
    if schema_version == 2:
        movie_keys.add("runtime_log_checkpoint")
    _strict_keys(raw, movie_keys, "movie")
    if raw["recording_backend"] not in {
        "x11-window-select-v1", "synthetic-jsonl-v1"
    }:
        raise MovieError("unsupported recording_backend")
    if raw["clock"] != "monotonic-offset-ns" or raw["complete"] is not True:
        raise MovieError("movie is incomplete or uses an unsupported clock")
    if not isinstance(raw["recorded_at"], str) or not raw["recorded_at"]:
        raise MovieError("recorded_at must be a string")
    if raw["termination"] not in {"stop-keysym", "max-duration"}:
        raise MovieError("unsupported termination")

    target = raw["target"]
    if not isinstance(target, dict):
        raise MovieError("target must be an object")
    _strict_keys(target, {"exe_basename", "executable_sha256", "window_signature"}, "target")
    if not isinstance(target["exe_basename"], str) or not target["exe_basename"]:
        raise MovieError("target.exe_basename is invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", target["executable_sha256"]):
        raise MovieError("target executable SHA-256 is invalid")
    signature = target["window_signature"]
    if not isinstance(signature, dict):
        raise MovieError("window_signature must be an object")
    _strict_keys(signature, {
        "class", "width", "height", "screen",
        "owner_exe_basename",
    }, "window_signature")
    for key in {"class", "owner_exe_basename"}:
        if not isinstance(signature[key], str) or not signature[key]:
            raise MovieError(f"window_signature.{key} is invalid")
    for key in {"width", "height"}:
        if not isinstance(signature[key], int) or signature[key] <= 0:
            raise MovieError(f"window_signature.{key} is invalid")
    if not isinstance(signature["screen"], int) or signature["screen"] < 0:
        raise MovieError("window_signature.screen is invalid")

    anchor = raw["anchor"]
    if not isinstance(anchor, dict):
        raise MovieError("anchor must be an object")
    anchor_type = anchor.get("type")
    if anchor_type == "log-milestone":
        required = {
            "type", "log_basename", "marker", "start_offset", "matched_offset",
            "anchored_at", "frame", "neutral_wait_ns",
        }
        _strict_keys(anchor, required, "anchor")
        if not isinstance(anchor["marker"], str) or not anchor["marker"]:
            raise MovieError("anchor marker is invalid")
        for key in {"start_offset", "matched_offset", "neutral_wait_ns"}:
            if not isinstance(anchor[key], int) or anchor[key] < 0:
                raise MovieError(f"anchor.{key} is invalid")
    elif anchor_type == "manual-delay":
        _strict_keys(anchor, {"type", "arm_delay_ms", "anchored_at", "frame"}, "anchor")
        if not isinstance(anchor["arm_delay_ms"], int) or anchor["arm_delay_ms"] < 0:
            raise MovieError("anchor.arm_delay_ms is invalid")
    else:
        raise MovieError("unsupported anchor type")
    if not isinstance(anchor["anchored_at"], str) or not anchor["anchored_at"]:
        raise MovieError("anchor.anchored_at is invalid")
    frame = anchor["frame"]
    if frame is not None:
        if not isinstance(frame, dict):
            raise MovieError("anchor.frame must be null or an object")
        _strict_keys(frame, {"sha256", "size"}, "anchor.frame")
        if not re.fullmatch(r"[0-9a-f]{64}", frame["sha256"]):
            raise MovieError("anchor.frame.sha256 is invalid")
        if not isinstance(frame["size"], int) or frame["size"] <= 0:
            raise MovieError("anchor.frame.size is invalid")

    if schema_version == 2:
        checkpoint = raw["runtime_log_checkpoint"]
        if anchor_type == "log-milestone":
            _validate_checkpoint_contract(checkpoint, "runtime_log_checkpoint")
        elif checkpoint is not None:
            raise MovieError(
                "manual-delay movie runtime_log_checkpoint must be null"
            )

    events = raw["events"]
    if not isinstance(events, list) or not events or len(events) > MAX_EVENTS:
        raise MovieError("events must be a non-empty bounded list")
    held: set[str] = set()
    previous_offset = -1
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise MovieError(f"event[{index}] must be an object")
        _strict_keys(event, {
            "sequence", "offset_ns", "action", "keysym", "keycode", "state",
            "send_event", "source",
        }, f"event[{index}]")
        if event["sequence"] != index:
            raise MovieError(f"event[{index}] sequence mismatch")
        offset = event["offset_ns"]
        if not isinstance(offset, int) or offset < previous_offset or offset < 0:
            raise MovieError(f"event[{index}] offset is not monotonic")
        previous_offset = offset
        if event["action"] not in {"down", "up"}:
            raise MovieError(f"event[{index}] action is invalid")
        keysym = _safe_keysym(event["keysym"], f"event[{index}].keysym")
        if not isinstance(event["keycode"], int) or not (0 <= event["keycode"] <= 255):
            raise MovieError(f"event[{index}] keycode is invalid")
        if event["source"] == "window-event" and event["keycode"] == 0:
            raise MovieError(f"event[{index}] window keycode cannot be zero")
        if event["source"] not in {"window-event", "emergency-release"}:
            raise MovieError(f"event[{index}] source is invalid")
        if not isinstance(event["state"], int) or not (0 <= event["state"] <= 0xFFFFFFFF):
            raise MovieError(f"event[{index}] state is invalid")
        if not isinstance(event["send_event"], bool):
            raise MovieError(f"event[{index}] send_event is invalid")
        if event["action"] == "down":
            held.add(keysym)
        else:
            if keysym not in held:
                raise MovieError(f"event[{index}] releases an unheld key")
            held.remove(keysym)
    if held:
        raise MovieError(f"movie ends with held keys: {sorted(held)}")
    if not isinstance(raw["duration_ns"], int) or raw["duration_ns"] < 0:
        raise MovieError("duration_ns is invalid")
    if events and raw["duration_ns"] < events[-1]["offset_ns"]:
        raise MovieError("duration_ns precedes the final event")
    expected_schedule = _sha256_schedule(events)
    if raw["schedule_sha256"] != expected_schedule:
        raise MovieError("schedule_sha256 mismatch")
    return raw


def load_movie(path: Path) -> tuple[dict, bytes]:
    if not path.is_file() or path.is_symlink():
        raise Refusal("movie_invalid", str(path))
    try:
        data = path.read_bytes()
        raw = json.loads(data)
    except (OSError, json.JSONDecodeError) as exc:
        raise Refusal("movie_invalid", str(exc)) from exc
    try:
        return validate_movie(raw), data
    except MovieError as exc:
        raise Refusal("movie_invalid", str(exc)) from exc


def _compare_window_signature(expected: dict, observed: dict) -> None:
    if expected != observed:
        raise Refusal(
            "window_signature_mismatch",
            json.dumps({"expected": expected, "observed": observed}, sort_keys=True),
        )


def _anchor_for_replay(args: argparse.Namespace, movie: dict, xdo: XDoTool) -> tuple[int, dict]:
    anchor = movie["anchor"]
    frame = anchor["frame"]
    observed_frame = _frame_anchor(args.anchor_frame)
    if frame is not None and observed_frame != frame:
        raise Refusal(
            "anchor_frame_mismatch",
            json.dumps({"expected": frame, "observed": observed_frame}, sort_keys=True),
        )
    if frame is None and observed_frame is not None:
        raise Refusal("unexpected_anchor_frame", "movie has no frame anchor")

    if anchor["type"] == "log-milestone":
        if not args.log:
            raise Refusal("log_required", anchor["marker"])
        log = LogMilestone(Path(args.log), anchor["marker"])
        _emit_status(
            args,
            "armed",
            mode="replay",
            anchor_type="log-milestone",
            marker=anchor["marker"],
            arm_delay_ms=0,
        )
        deadline = time.monotonic() + args.anchor_timeout
        while not log.poll():
            if time.monotonic() >= deadline:
                raise Refusal("anchor_timeout", anchor["marker"])
            time.sleep(0.01)
        marker_seen_ns = time.monotonic_ns()
        observed_anchor = log.receipt()
        # Recording begins only after the marker, focus, and any held setup
        # key have all settled.  Preserve that recorded post-marker interval
        # so replay's zero point has the same definition.
        neutral_wait_ns = anchor["neutral_wait_ns"]
        _wait_until(marker_seen_ns + neutral_wait_ns)
        observed_anchor["neutral_wait_ns"] = neutral_wait_ns
    else:
        _emit_status(
            args,
            "armed",
            mode="replay",
            anchor_type="manual-delay",
            marker=None,
            arm_delay_ms=int(args.arm_delay * 1000),
        )
        _wait_until(time.monotonic_ns() + int(args.arm_delay * 1_000_000_000))
        observed_anchor = {
            "type": "manual-delay",
            "arm_delay_ms": int(args.arm_delay * 1000),
        }
    focused = xdo.focus()
    if focused != args.window_id:
        raise Refusal(
            "anchor_focus_mismatch",
            f"focused 0x{focused:x}, expected 0x{args.window_id:x}",
        )
    observed_anchor["anchored_at"] = ev.now().isoformat()
    observed_anchor["frame"] = observed_frame
    return time.monotonic_ns(), observed_anchor


def replay(args: argparse.Namespace) -> int:
    movie_path = Path(args.movie).absolute()
    movie, movie_bytes = load_movie(movie_path)
    if movie["recording_backend"] != "x11-window-select-v1" and not args.allow_synthetic:
        raise Refusal("synthetic_movie_refused", movie["recording_backend"])
    movie_sha = _sha256_bytes(movie_bytes)
    expected_sha = movie["target"]["executable_sha256"]
    if args.expected_sha is not None and args.expected_sha != expected_sha:
        raise Refusal(
            "expected_sha_disagrees_with_movie",
            f"{args.expected_sha} != {expected_sha}",
        )
    ownership = _ownership(args, expected_sha)
    xdo = XDoTool(args.xdotool, args.display)
    window_before = _window_snapshot(args, xdo)
    _compare_window_signature(
        movie["target"]["window_signature"], window_before.signature()
    )
    backend = _make_replay_backend(args, movie, xdo)
    run_dir: Path | None = None
    metadata: dict | None = None
    held: dict[str, int] = {}
    dispatches: list[dict] = []
    deliveries: list[dict] = []
    releases: list[dict] = []
    failure: Refusal | None = None
    verifier: ReplayEchoVerifier | None = None
    backend_receipt: dict = {}
    echo_balanced_before_cleanup = False
    runtime_log_checkpoint: dict | None = None

    try:
        anchor_ns, observed_anchor = _anchor_for_replay(args, movie, backend)
        backend.begin()
        _emit_status(args, "replay-started", mode="replay", anchor=observed_anchor)
        run_dir, metadata = _new_run_metadata("replay", ownership, window_before)
        metadata.update({
            "movie_path": str(movie_path),
            "movie_sha256": movie_sha,
            "schedule_sha256": movie["schedule_sha256"],
            "recorded_anchor": movie["anchor"],
            "replay_anchor": observed_anchor,
            "max_request_drift_ns": int(args.max_drift_ms * 1_000_000),
            "max_delivery_drift_ns": int(
                args.max_delivery_drift_ms * 1_000_000
            ),
            "echo_timeout_ns": int(args.echo_timeout_ms * 1_000_000),
            "replay_backend": backend.receipt(),
        })
        _save_metadata(run_dir, metadata)
        verifier = ReplayEchoVerifier(
            backend,
            anchor_ns=anchor_ns,
            max_delivery_drift_ns=int(args.max_delivery_drift_ms * 1_000_000),
            echo_timeout_ns=int(args.echo_timeout_ms * 1_000_000),
        )
        for event in movie["events"]:
            scheduled_ns = anchor_ns + event["offset_ns"]
            _wait_until(scheduled_ns)
            verifier.assert_quiet()
            focused = backend.focus()
            if focused != args.window_id:
                raise Refusal(
                    "focus_lost_during_replay",
                    f"focused 0x{focused:x}, expected 0x{args.window_id:x}",
                )
            ready_ns = time.monotonic_ns()
            if abs(ready_ns - scheduled_ns) > int(args.max_drift_ms * 1_000_000):
                raise Refusal(
                    "replay_timing_drift",
                    f"event {event['sequence']} drifted {ready_ns - scheduled_ns} ns",
                )
            request = backend.send(event)
            request_drift_ns = request["requested_ns"] - scheduled_ns
            if abs(request_drift_ns) > int(args.max_drift_ms * 1_000_000):
                raise Refusal(
                    "replay_timing_drift",
                    f"event {event['sequence']} drifted {request_drift_ns} ns",
                )
            if event["action"] == "down":
                held[event["keysym"]] = request["keycode"]
            else:
                held.pop(event["keysym"], None)
            dispatches.append({
                "sequence": event["sequence"],
                "action": event["action"],
                "keysym": event["keysym"],
                "keycode": request["keycode"],
                "scheduled_offset_ns": event["offset_ns"],
                "requested_offset_ns": request["requested_ns"] - anchor_ns,
                "flushed_offset_ns": request["flushed_ns"] - anchor_ns,
                "request_drift_ns": request_drift_ns,
            })
            deliveries.append(verifier.expect(event))
        _wait_until(anchor_ns + movie["duration_ns"])
        verifier.assert_quiet()
        if movie["anchor"]["type"] == "log-milestone":
            runtime_log_checkpoint, log_segment = _runtime_log_checkpoint(
                args.log, observed_anchor
            )
            assert run_dir is not None
            _write_new_file(run_dir / "runtime-log-segment.bin", log_segment)
            expected_checkpoint = movie.get("runtime_log_checkpoint")
            if expected_checkpoint is not None and not _checkpoint_digests_match(
                expected_checkpoint, runtime_log_checkpoint
            ):
                raise Refusal(
                    "runtime_log_checkpoint_mismatch",
                    json.dumps(
                        {
                            "expected_segment_sha256": expected_checkpoint[
                                "segment_sha256"
                            ],
                            "observed_segment_sha256": runtime_log_checkpoint[
                                "segment_sha256"
                            ],
                            "expected_routine_trace_sha256": expected_checkpoint[
                                "routine_trace_sha256"
                            ],
                            "observed_routine_trace_sha256": runtime_log_checkpoint[
                                "routine_trace_sha256"
                            ],
                        },
                        sort_keys=True,
                    ),
                )
    except (Refusal, KeyboardInterrupt) as exc:
        failure = exc if isinstance(exc, Refusal) else Refusal("interrupted", "")
    finally:
        echo_held = verifier.held if verifier is not None else set()
        echo_balanced_before_cleanup = not echo_held
        releases = _release_replay_held(backend, held, echo_held)
        backend.close()
        backend_receipt = backend.receipt()

    if run_dir is None or metadata is None:
        assert failure is not None
        raise failure
    event_count = len(movie["events"])
    echo_verified = (
        failure is None
        and len(deliveries) == event_count
        and verifier is not None
        and echo_balanced_before_cleanup
    )
    accepted = (
        echo_verified
        and len(dispatches) == event_count
        and all(item["released"] for item in releases)
        and (
            movie["anchor"]["type"] != "log-milestone"
            or runtime_log_checkpoint is not None
        )
    )
    try:
        window_after = _window_snapshot(args, xdo)
        _compare_window_signature(
            movie["target"]["window_signature"], window_after.signature()
        )
    except Refusal as exc:
        window_after = None
        if failure is None:
            failure = exc
        accepted = False
    request_drifts = [abs(item["request_drift_ns"]) for item in dispatches]
    delivery_drifts = [abs(item["delivery_drift_ns"]) for item in deliveries]
    metadata.update({
        "ended": ev.now().isoformat(),
        "status": "complete" if accepted else "replay-failed",
        "accepted": accepted,
        "event_count": event_count,
        "events_dispatched": len(dispatches),
        "events_delivered": len(deliveries),
        "dispatches": dispatches,
        "deliveries": deliveries,
        "target_echo_verified": echo_verified,
        "target_echo_backend": backend_receipt["echo_backend"],
        "ignored_unmatched_release_count": (
            len(verifier.ignored_unmatched_releases) if verifier is not None else 0
        ),
        "ignored_unmatched_releases": (
            verifier.ignored_unmatched_releases if verifier is not None else []
        ),
        "maximum_absolute_drift_ns": max(delivery_drifts, default=0),
        "maximum_absolute_request_drift_ns": max(request_drifts, default=0),
        "maximum_absolute_delivery_drift_ns": max(delivery_drifts, default=0),
        "replay_backend": backend_receipt,
        "runtime_log_checkpoint": runtime_log_checkpoint,
        "emergency_releases": releases,
        "all_keys_released": not held and all(item["released"] for item in releases),
        "window_after": window_after.to_dict() if window_after else None,
        "failure": (
            {"reason": failure.reason, "detail": failure.detail}
            if failure is not None else None
        ),
    })
    _save_metadata(run_dir, metadata)
    print(json.dumps({
        "run_id": run_dir.name,
        "movie_sha256": movie_sha,
        "schedule_sha256": movie["schedule_sha256"],
        "events_dispatched": len(dispatches),
        "events_delivered": len(deliveries),
        "target_echo_verified": echo_verified,
        "runtime_log_checkpoint_captured": runtime_log_checkpoint is not None,
        "accepted": accepted,
        "failure": metadata["failure"],
    }, sort_keys=True))
    return ev.EXIT_OK if accepted else ev.EXIT_TOOL_NEGATIVE


def validate_command(args: argparse.Namespace) -> int:
    movie, data = load_movie(Path(args.movie))
    print(json.dumps({
        "valid": True,
        "schema_version": movie["schema_version"],
        "movie_sha256": _sha256_bytes(data),
        "schedule_sha256": movie["schedule_sha256"],
        "recording_backend": movie["recording_backend"],
        "anchor_type": movie["anchor"]["type"],
        "event_count": len(movie["events"]),
        "duration_ns": movie["duration_ns"],
    }, sort_keys=True))
    return ev.EXIT_OK


def compare_command(args: argparse.Namespace) -> int:
    if len(args.receipts) < 2:
        raise Refusal("receipt_count", "compare requires at least two receipts")
    receipts: list[dict] = []
    for path_text in args.receipts:
        path = Path(path_text)
        try:
            receipt = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise Refusal("receipt_invalid", f"{path}: {exc}") from exc
        if not isinstance(receipt, dict) or receipt.get("tool") != TOOL:
            raise Refusal("receipt_invalid", str(path))
        receipts.append(receipt)
    first = receipts[0]
    reasons: list[str] = []
    for index, receipt in enumerate(receipts):
        if receipt.get("mode") != "replay" or receipt.get("accepted") is not True:
            reasons.append(f"receipt[{index}] is not an accepted replay")
        for key in {
            "movie_sha256",
            "schedule_sha256",
            "event_count",
            "implementation_sha256",
            "tool_version",
            "max_request_drift_ns",
            "max_delivery_drift_ns",
            "echo_timeout_ns",
        }:
            if receipt.get(key) != first.get(key):
                reasons.append(f"receipt[{index}] differs at {key}")
        if receipt.get("events_dispatched") != receipt.get("event_count"):
            reasons.append(f"receipt[{index}] did not dispatch every event")
        if receipt.get("events_delivered") != receipt.get("event_count"):
            reasons.append(f"receipt[{index}] did not deliver every event")
        if receipt.get("target_echo_verified") is not True:
            reasons.append(f"receipt[{index}] has no accepted target echo")
        if receipt.get("all_keys_released") is not True:
            reasons.append(f"receipt[{index}] did not release every key")
        before = receipt.get("window_before") or {}
        if before.get("signature") != (first.get("window_before") or {}).get("signature"):
            reasons.append(f"receipt[{index}] window signature differs")
        replay_anchor = receipt.get("replay_anchor") or {}
        if replay_anchor.get("type") != (first.get("replay_anchor") or {}).get("type"):
            reasons.append(f"receipt[{index}] anchor type differs")
        if replay_anchor.get("type") == "log-milestone":
            if replay_anchor.get("marker") != (first.get("replay_anchor") or {}).get("marker"):
                reasons.append(f"receipt[{index}] log marker differs")
            checkpoint = receipt.get("runtime_log_checkpoint")
            first_checkpoint = first.get("runtime_log_checkpoint")
            if not isinstance(checkpoint, dict):
                reasons.append(f"receipt[{index}] has no runtime log checkpoint")
            elif not isinstance(first_checkpoint, dict):
                reasons.append("receipt[0] has no runtime log checkpoint")
            else:
                for digest_key, label in {
                    "segment_sha256": "runtime log segment",
                    "routine_trace_sha256": "runtime ROUTINE trace",
                }.items():
                    digest = checkpoint.get(digest_key)
                    first_digest = first_checkpoint.get(digest_key)
                    if not isinstance(digest, str) or not re.fullmatch(
                        r"[0-9a-f]{64}", digest
                    ):
                        reasons.append(
                            f"receipt[{index}] has invalid {label} digest"
                        )
                    elif not isinstance(first_digest, str) or not re.fullmatch(
                        r"[0-9a-f]{64}", first_digest
                    ):
                        reasons.append(f"receipt[0] has invalid {label} digest")
                    elif digest != first_digest:
                        reasons.append(f"receipt[{index}] {label} differs")
    result = {
        "agreement": not reasons,
        "receipt_count": len(receipts),
        "movie_sha256": first.get("movie_sha256"),
        "schedule_sha256": first.get("schedule_sha256"),
        "reasons": reasons,
    }
    print(json.dumps(result, sort_keys=True))
    return ev.EXIT_OK if not reasons else ev.EXIT_TOOL_NEGATIVE


def capabilities_command(_: argparse.Namespace) -> int:
    print(json.dumps({
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "schema_version": SCHEMA_VERSION,
        "supported_schema_versions": sorted(SUPPORTED_SCHEMA_VERSIONS),
        "modes": ["record", "replay", "validate", "compare"],
        "input_scope": "one-explicit-X11-window-keyboard-events",
        "recording_backend": "XSelectInput KeyPress/KeyRelease on target window",
        "display_wide_capture": False,
        "host_input_device_capture": False,
        "replay_backend": "persistent X11/XTEST with exact-window echo",
        "target_echo_required": True,
        "target_echo_sequence": "action/keysym/keycode/keyboard-modifiers/send-event",
        "log_anchored_runtime_checkpoint": (
            "bounded post-anchor log segment and ROUTINE trace"
        ),
        "nested_x11_auto_repeat_during_replay": False,
        "anchors": ["new-log-milestone", "manual-delay", "optional-frame-hash"],
        "supervisor_status_events": ["armed", "recording-started", "replay-started"],
        "clock": "monotonic-offset-ns",
        "max_duration_seconds": MAX_DURATION_SECONDS,
        "max_events": MAX_EVENTS,
        "internal_game_frame_synchronization": False,
        "write_verbs": ["target-window-keydown", "target-window-keyup"],
    }, indent=2, sort_keys=True))
    return ev.EXIT_OK


def _add_target_args(parser: argparse.ArgumentParser, *, expected_default: str | None) -> None:
    parser.add_argument("--pid", required=True, type=int, help="verified bugs.exe host PID")
    parser.add_argument("--window-id", required=True, type=_parse_window_id)
    parser.add_argument("--expected-sha", type=_validate_sha256, default=expected_default)
    parser.add_argument("--exe-basename", default="bugs.exe")
    parser.add_argument("--loader-re", default=ev.DEFAULT_LOADER_RE)
    parser.add_argument("--cwd-prefix")
    parser.add_argument("--display", default=os.environ.get("DISPLAY", ""))
    parser.add_argument("--xdotool", default=os.environ.get("ABLPC_XDOTOOL", "xdotool"))
    parser.add_argument("--window-owner-re", default=ev.DEFAULT_LOADER_RE)
    parser.add_argument("--window-name-re", default=r".+")
    parser.add_argument("--window-class-re", default=r"(?i)^bugs\.exe$")
    parser.add_argument("--anchor-frame", help="optional frame file whose hash anchors start")
    parser.add_argument("--anchor-timeout", type=_positive_float, default=120.0)
    parser.add_argument("--status-fd", type=_status_descriptor, help=argparse.SUPPRESS)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Record/replay keyboard input on one verified ABLPC Gamescope window."
    )
    parser.add_argument("--capabilities", action="store_true")
    sub = parser.add_subparsers(dest="command")

    rec = sub.add_parser("record", help="record target-window key press/release events")
    _add_target_args(rec, expected_default=KNOWN_RETAIL_SHA256)
    rec.add_argument("--movie", required=True)
    anchors = rec.add_mutually_exclusive_group(required=True)
    anchors.add_argument("--start-milestone", help="new bugs.log marker that starts movie time")
    anchors.add_argument("--start-now", action="store_true", help="start after --arm-delay")
    rec.add_argument("--log", help="bugs.log for --start-milestone")
    rec.add_argument("--arm-delay", type=_nonnegative_float, default=3.0)
    rec.add_argument("--max-duration", type=_positive_float, default=900.0)
    rec.add_argument("--stop-keysym", default="F12")
    rec.set_defaults(func=record)

    rep = sub.add_parser("replay", help="replay a movie to a verified target window")
    _add_target_args(rep, expected_default=None)
    rep.add_argument("--movie", required=True)
    rep.add_argument("--log", help="fresh bugs.log required by a log-anchored movie")
    rep.add_argument("--arm-delay", type=_nonnegative_float, default=3.0)
    rep.add_argument(
        "--max-drift-ms",
        type=_positive_float,
        default=50.0,
        help="maximum pre-send request drift",
    )
    rep.add_argument(
        "--max-delivery-drift-ms",
        type=_positive_float,
        default=5.0,
        help="maximum target-observed event drift (default: 5 ms)",
    )
    rep.add_argument(
        "--echo-timeout-ms",
        type=_positive_float,
        default=100.0,
        help="maximum wait for each target-window echo (default: 100 ms)",
    )
    rep.add_argument("--allow-synthetic", action="store_true", help=argparse.SUPPRESS)
    rep.set_defaults(func=replay)

    val = sub.add_parser("validate", help="strictly validate a movie without replaying it")
    val.add_argument("--movie", required=True)
    val.set_defaults(func=validate_command)

    comp = sub.add_parser("compare", help="compare two or more accepted replay receipts")
    comp.add_argument("receipts", nargs="+")
    comp.set_defaults(func=compare_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.capabilities:
        if args.command is not None:
            parser.error("--capabilities cannot be combined with a command")
        return capabilities_command(args)
    if args.command is None:
        parser.error("a command is required")
    if hasattr(args, "display") and not args.display:
        _print_refusal("display_missing", "DISPLAY is empty")
        return ev.EXIT_REFUSAL
    if getattr(args, "start_milestone", None) and not getattr(args, "log", None):
        parser.error("--start-milestone requires --log")
    try:
        return args.func(args)
    except Refusal as exc:
        _print_refusal(exc.reason, exc.detail)
        return ev.EXIT_REFUSAL
    except MovieError as exc:
        _print_refusal("movie_invalid", str(exc))
        return ev.EXIT_REFUSAL


if __name__ == "__main__":
    raise SystemExit(main())
