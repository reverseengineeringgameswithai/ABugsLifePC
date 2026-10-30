#!/usr/bin/env python3
"""In-game save-state hotkeys for the PC game under Wine/Gamescope.

The game is not an emulator with a built-in savestate menu -- it is the native
``bugs.exe`` running under Wine, presented by Gamescope on a nested X display.
This daemon gives the emulator-style experience anyway: it grabs a few hotkeys
**on the game's nested display only** (never the host desktop ``:0``), so
pressing e.g. F5 while playing saves and F9 loads, with a filename popup on
save and a picker on load.

It is a thin front end over the validated ``game-memory.py snapshot`` and
``restore`` verbs ([[EXP-20260817-188 ...]]): the save/load, the same-process
and level guards, the SIGSTOP-atomic capture, and the receipts all come from
there. A load is a memory write; here the human pressing the load key is the
authorization, and every load still writes a receipt recording that it was
hotkey-initiated.

Scope and honesty: the ``game-memory`` path this drives is live-validated, but
the X key-grab and Tk popups running under Gamescope's nested Xwayland are new
and validated only at the logic level here -- the first real "press F5 in the
game" run is the acceptance test. Same-process only: these are checkpoints
within one running game, not a savegame that survives a relaunch (that is
CRIU, blocked here by ntsync; see CAP-011).
"""

from __future__ import annotations

import argparse
import ctypes
from ctypes.util import find_library
from dataclasses import dataclass
import json
import os
from pathlib import Path
import select
import shutil
import subprocess
import sys
import time
from typing import Callable

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import evidence_lib as ev  # noqa: E402
import session_lib as sl  # noqa: E402


TOOL = "savestate-hotkeys"
TOOL_VERSION = "1.0.0"
GAME_MEMORY = SCRIPTS / "game-memory.py"

QUICKSAVE_NAME = "quicksave"
LOAD_AUTHORIZE = "savestate-hotkey (interactive user)"

# X constants.
GRAB_MODE_ASYNC = 1
ANY_MODIFIER = 1 << 15
KEY_PRESS = 2
DESTROY_NOTIFY = 17
UNMAP_NOTIFY = 18


class SaveStateError(RuntimeError):
    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(detail or reason)
        self.reason = reason
        self.detail = detail


def _fail(reason: str, detail: str = "") -> int:
    print(json.dumps(sl.refusal(TOOL, reason, detail)))
    return ev.EXIT_REFUSAL


# --------------------------------------------------------------------------
# Save-state controller (drives game-memory.py)
# --------------------------------------------------------------------------


@dataclass
class Snapshot:
    name: str
    directory: Path
    level: int | None
    captured_at: str
    total_bytes: int


class SaveStateController:
    """Save/load/list checkpoints for one live game via game-memory.py."""

    def __init__(
        self,
        pid: int,
        *,
        accept_sha: str,
        snapshot_dir: Path,
        loader_re: str = ev.DEFAULT_LOADER_RE,
        regions: tuple[str, ...] = (),
        python: str = sys.executable,
        runner: Callable[[list[str]], subprocess.CompletedProcess] | None = None,
    ) -> None:
        self.pid = pid
        self.accept_sha = accept_sha
        self.snapshot_dir = snapshot_dir
        self.loader_re = loader_re
        # Non-empty only for fixture tests, where the synthetic game does not
        # map the full .data section; production always captures default .data.
        self.regions = regions
        self.python = python
        self._runner = runner

    def _run(self, *args: str) -> tuple[int, dict]:
        argv = [self.python, str(GAME_MEMORY), *args,
                "--pid", str(self.pid), "--loader-re", self.loader_re,
                "--accept-sha", self.accept_sha]
        if self._runner is not None:
            result = self._runner(argv)
        else:
            result = subprocess.run(argv, capture_output=True, text=True, timeout=120)
        try:
            payload = json.loads(result.stdout) if result.stdout.strip() else {}
        except json.JSONDecodeError:
            payload = {"_stdout": result.stdout, "_stderr": result.stderr}
        return result.returncode, payload

    def save(self, name: str, *, overwrite: bool = False, freeze: bool = True) -> dict:
        target = self.snapshot_dir / name
        if target.exists():
            if not overwrite:
                raise SaveStateError("save_exists", f"a save named {name!r} already exists")
            shutil.rmtree(target)
        args = ["snapshot", "--name", name, "--snapshot-dir", str(self.snapshot_dir)]
        if self.regions:
            args.append("--no-data")
            for region in self.regions:
                args.extend(["--region", region])
        if not freeze:
            args.append("--no-freeze")
        rc, payload = self._run(*args)
        if rc != ev.EXIT_OK:
            raise SaveStateError(payload.get("reason", "save_failed"),
                                 payload.get("detail", json.dumps(payload)))
        return payload

    def load(self, name: str) -> dict:
        directory = self.snapshot_dir / name
        if not (directory / "snapshot.json").is_file():
            raise SaveStateError("save_not_found", f"no save named {name!r}")
        rc, payload = self._run("restore", "--snapshot", str(directory),
                                "--authorize", LOAD_AUTHORIZE,
                                "--purpose", "interactive hotkey load")
        if rc != ev.EXIT_OK and payload.get("refused"):
            raise SaveStateError(payload.get("reason", "load_refused"),
                                 payload.get("detail", ""))
        payload["load_verified"] = bool(payload.get("verified"))
        return payload

    def list_saves(self) -> list[Snapshot]:
        if not self.snapshot_dir.is_dir():
            return []
        saves: list[Snapshot] = []
        for entry in self.snapshot_dir.iterdir():
            header = entry / "snapshot.json"
            if not header.is_file():
                continue
            try:
                data = json.loads(header.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            saves.append(Snapshot(
                name=entry.name,
                directory=entry,
                level=data.get("internal_level"),
                captured_at=data.get("captured_at", ""),
                total_bytes=sum(r.get("size", 0) for r in data.get("regions", [])),
            ))
        saves.sort(key=lambda s: s.captured_at, reverse=True)
        return saves

    def latest(self) -> Snapshot | None:
        saves = self.list_saves()
        return saves[0] if saves else None


# --------------------------------------------------------------------------
# X11 hotkey grabber (nested display only)
# --------------------------------------------------------------------------


class _XAnyEvent(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int), ("serial", ctypes.c_ulong),
        ("send_event", ctypes.c_int), ("display", ctypes.c_void_p),
        ("window", ctypes.c_ulong),
    ]


class _XKeyEvent(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int), ("serial", ctypes.c_ulong),
        ("send_event", ctypes.c_int), ("display", ctypes.c_void_p),
        ("window", ctypes.c_ulong), ("root", ctypes.c_ulong),
        ("subwindow", ctypes.c_ulong), ("time", ctypes.c_ulong),
        ("x", ctypes.c_int), ("y", ctypes.c_int),
        ("x_root", ctypes.c_int), ("y_root", ctypes.c_int),
        ("state", ctypes.c_uint), ("keycode", ctypes.c_uint),
        ("same_screen", ctypes.c_int),
    ]


class _XEvent(ctypes.Union):
    _fields_ = [
        ("type", ctypes.c_int), ("xany", _XAnyEvent), ("xkey", _XKeyEvent),
        ("pad", ctypes.c_long * 24),
    ]


class HotkeyGrabber:
    """Grab named keysyms on one nested X display's root window."""

    def __init__(self, display_name: str) -> None:
        if not sl.DISPLAY_RE.fullmatch(display_name):
            raise SaveStateError("invalid_display", display_name)
        lib_name = find_library("X11")
        if not lib_name:
            raise SaveStateError("libx11_missing", "libX11 could not be located")
        self.display_name = display_name
        self.lib = ctypes.CDLL(lib_name)
        self._bind()
        self.display = self.lib.XOpenDisplay(display_name.encode("utf-8"))
        if not self.display:
            raise SaveStateError("x11_display_open_failed", display_name)
        self.root = self.lib.XDefaultRootWindow(self.display)
        self.connection_fd = self.lib.XConnectionNumber(self.display)
        self._grabbed: dict[int, str] = {}  # keycode -> keysym name

    def _bind(self) -> None:
        L = self.lib
        L.XOpenDisplay.argtypes = [ctypes.c_char_p]; L.XOpenDisplay.restype = ctypes.c_void_p
        L.XCloseDisplay.argtypes = [ctypes.c_void_p]; L.XCloseDisplay.restype = ctypes.c_int
        L.XDefaultRootWindow.argtypes = [ctypes.c_void_p]; L.XDefaultRootWindow.restype = ctypes.c_ulong
        L.XConnectionNumber.argtypes = [ctypes.c_void_p]; L.XConnectionNumber.restype = ctypes.c_int
        L.XStringToKeysym.argtypes = [ctypes.c_char_p]; L.XStringToKeysym.restype = ctypes.c_ulong
        L.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]; L.XKeysymToKeycode.restype = ctypes.c_ubyte
        L.XGrabKey.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint,
                               ctypes.c_ulong, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        L.XGrabKey.restype = ctypes.c_int
        L.XUngrabKey.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint, ctypes.c_ulong]
        L.XUngrabKey.restype = ctypes.c_int
        L.XSync.argtypes = [ctypes.c_void_p, ctypes.c_int]; L.XSync.restype = ctypes.c_int
        L.XPending.argtypes = [ctypes.c_void_p]; L.XPending.restype = ctypes.c_int
        L.XNextEvent.argtypes = [ctypes.c_void_p, ctypes.POINTER(_XEvent)]; L.XNextEvent.restype = ctypes.c_int

    def keycode_for(self, keysym_name: str) -> int:
        keysym = self.lib.XStringToKeysym(keysym_name.encode("ascii"))
        if keysym == 0:
            raise SaveStateError("unknown_keysym", keysym_name)
        keycode = self.lib.XKeysymToKeycode(self.display, keysym)
        if keycode == 0:
            raise SaveStateError("unmapped_keysym", keysym_name)
        return int(keycode)

    def grab(self, keysym_name: str) -> None:
        keycode = self.keycode_for(keysym_name)
        self.lib.XGrabKey(self.display, keycode, ANY_MODIFIER, self.root, 0,
                          GRAB_MODE_ASYNC, GRAB_MODE_ASYNC)
        self.lib.XSync(self.display, 0)
        self._grabbed[keycode] = keysym_name

    def poll(self, timeout_seconds: float) -> str | None:
        """Return the keysym name of a grabbed KeyPress, or None on timeout."""

        if self.lib.XPending(self.display) == 0:
            try:
                readable, _, _ = select.select(
                    [self.connection_fd], [], [], max(0.0, timeout_seconds))
            except (OSError, ValueError):
                return None
            if not readable or self.lib.XPending(self.display) == 0:
                return None
        raw = _XEvent()
        self.lib.XNextEvent(self.display, ctypes.byref(raw))
        if raw.type == KEY_PRESS:
            return self._grabbed.get(int(raw.xkey.keycode))
        if raw.type in {DESTROY_NOTIFY, UNMAP_NOTIFY}:
            return "__window_gone__"
        return None

    def close(self) -> None:
        if self.display:
            for keycode in list(self._grabbed):
                self.lib.XUngrabKey(self.display, keycode, ANY_MODIFIER, self.root)
            self.lib.XCloseDisplay(self.display)
            self.display = None

    def __enter__(self) -> "HotkeyGrabber":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


# --------------------------------------------------------------------------
# Tk popups (optional; on the nested display)
# --------------------------------------------------------------------------


def prompt_save_name(display: str, default: str) -> str | None:
    """Filename entry popup on the nested display; None if cancelled."""

    try:
        import tkinter as tk
    except Exception:
        return default
    root = tk.Tk(screenName=display)
    root.title("Save state")
    root.attributes("-topmost", True)
    result: dict[str, str | None] = {"value": None}
    tk.Label(root, text="Save name:").pack(padx=12, pady=(12, 4))
    entry = tk.Entry(root, width=32)
    entry.insert(0, default)
    entry.select_range(0, tk.END)
    entry.pack(padx=12, pady=4)
    entry.focus_set()

    def accept(_evt=None) -> None:
        result["value"] = entry.get().strip() or default
        root.destroy()

    def cancel(_evt=None) -> None:
        root.destroy()

    tk.Button(root, text="Save", command=accept).pack(side="left", padx=12, pady=12)
    tk.Button(root, text="Cancel", command=cancel).pack(side="right", padx=12, pady=12)
    root.bind("<Return>", accept)
    root.bind("<Escape>", cancel)
    root.mainloop()
    return result["value"]


def pick_save(display: str, saves: list[Snapshot]) -> str | None:
    """Picker popup listing saves newest-first; None if cancelled."""

    try:
        import tkinter as tk
    except Exception:
        return saves[0].name if saves else None
    root = tk.Tk(screenName=display)
    root.title("Load state")
    root.attributes("-topmost", True)
    result: dict[str, str | None] = {"value": None}
    tk.Label(root, text="Choose a save:").pack(padx=12, pady=(12, 4))
    listbox = tk.Listbox(root, width=48, height=min(12, max(3, len(saves))))
    for save in saves:
        listbox.insert(tk.END, f"{save.name}   (level {save.level}, {save.captured_at[:19]})")
    if saves:
        listbox.select_set(0)
    listbox.pack(padx=12, pady=4)
    listbox.focus_set()

    def accept(_evt=None) -> None:
        sel = listbox.curselection()
        if sel:
            result["value"] = saves[sel[0]].name
        root.destroy()

    def cancel(_evt=None) -> None:
        root.destroy()

    tk.Button(root, text="Load", command=accept).pack(side="left", padx=12, pady=12)
    tk.Button(root, text="Cancel", command=cancel).pack(side="right", padx=12, pady=12)
    root.bind("<Return>", accept)
    root.bind("<Double-Button-1>", accept)
    root.bind("<Escape>", cancel)
    root.mainloop()
    return result["value"]


def toast(display: str, message: str, *, ms: int = 1200) -> None:
    """Brief self-closing confirmation label on the nested display."""

    try:
        import tkinter as tk
    except Exception:
        print(message, file=sys.stderr)
        return
    root = tk.Tk(screenName=display)
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    tk.Label(root, text=message, padx=16, pady=8,
             bg="#101010", fg="#e0e0e0").pack()
    root.after(ms, root.destroy)
    root.mainloop()


# --------------------------------------------------------------------------
# Target resolution and daemon
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class GameHandle:
    pid: int
    process_group: int
    start_ticks: int
    display: str
    window_id: int
    exe_sha256: str
    game_dir: str


def resolve_game(args: argparse.Namespace) -> GameHandle:
    if args.session:
        m = sl.resolve_session(args.session)
        if m.game_pid is None or not m.display or m.window_id is None:
            raise SaveStateError("session_incomplete", f"{m.session_id} is not addressable")
        proof = ev.ownership_proof(m.game_pid, loader_re=args.loader_re)
        return GameHandle(m.game_pid, m.process_group or os.getpgid(m.game_pid),
                          m.game_start_ticks or sl.pid_identity(m.game_pid)[1],
                          m.display, m.window_id, proof.exe_sha256, m.game_dir)
    if args.pid is None:
        raise SaveStateError("no_target", "pass --session or --pid")
    pid = args.pid
    group, ticks = sl.pid_identity(pid)
    cwd = os.readlink(f"/proc/{pid}/cwd")
    proof = ev.ownership_proof(pid, loader_re=args.loader_re)
    if args.display and args.window_id is not None:
        display, window_id = args.display, args.window_id
    else:
        target = sl.discover_game_target(
            group, Path(cwd),
            accepted_sha256={proof.exe_sha256},
            loader_re=args.loader_re,
            xdo_factory=lambda d: sl.XDo(d, executable=args.xdotool))
        if target is None:
            raise SaveStateError(
                "window_not_found",
                "could not find the owned game window; pass --display and --window-id")
        display, window_id = target.display, target.window_id
    return GameHandle(pid, group, ticks, display, window_id, proof.exe_sha256, cwd)


def build_keymap(args: argparse.Namespace) -> dict[str, str]:
    keymap = {
        args.save_key: "save",
        args.load_key: "load",
        args.quicksave_key: "quicksave",
        args.quickload_key: "quickload",
        args.quit_key: "quit",
    }
    if len(keymap) != 5:
        raise SaveStateError("duplicate_hotkey",
                             "save/load/quicksave/quickload/quit keys must be distinct")
    return keymap


def run_daemon(handle: GameHandle, args: argparse.Namespace) -> int:
    snapshot_dir = Path(args.snapshot_dir) if args.snapshot_dir else \
        ev.repo_root() / "work" / "snapshots"
    if not _git_ignored(snapshot_dir / "probe"):
        return _fail("snapshot_dir_not_ignored",
                     f"{snapshot_dir} is not git-ignored; saves hold game bytes")
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    controller = SaveStateController(
        handle.pid, accept_sha=handle.exe_sha256, snapshot_dir=snapshot_dir,
        loader_re=args.loader_re)
    keymap = build_keymap(args)
    action_for = {v: k for k, v in keymap.items()}
    refocus = sl.XDo(handle.display, executable=args.xdotool)

    print(json.dumps({
        "tool": TOOL, "tool_version": TOOL_VERSION, "verb": "daemon-started",
        "pid": handle.pid, "display": handle.display, "window_id": handle.window_id,
        "snapshot_dir": str(snapshot_dir),
        "hotkeys": {v: k for k, v in keymap.items()},
        "note": "hotkeys are grabbed on the game's nested display only",
    }, indent=2), flush=True)

    def do_save(popup: bool) -> None:
        default = time.strftime("save-%H%M%S") if not args.no_clock else "save"
        name = QUICKSAVE_NAME
        overwrite = True
        if popup and not args.no_popup:
            chosen = prompt_save_name(handle.display, default)
            if chosen is None:
                return
            name, overwrite = chosen, chosen in {s.name for s in controller.list_saves()}
        try:
            controller.save(name, overwrite=overwrite)
            toast(handle.display, f"Saved: {name}")
        except SaveStateError as exc:
            toast(handle.display, f"Save failed: {exc.reason}")
        _refocus(refocus, handle.window_id)

    def do_load(popup: bool) -> None:
        saves = controller.list_saves()
        if not saves:
            toast(handle.display, "No saves yet")
            return
        name = saves[0].name
        if popup and not args.no_popup:
            chosen = pick_save(handle.display, saves)
            if chosen is None:
                _refocus(refocus, handle.window_id)
                return
            name = chosen
        else:
            name = QUICKSAVE_NAME if any(s.name == QUICKSAVE_NAME for s in saves) else saves[0].name
        try:
            result = controller.load(name)
            ok = result.get("load_verified")
            toast(handle.display, f"Loaded: {name}" if ok else f"Load unverified: {name}")
        except SaveStateError as exc:
            toast(handle.display, f"Load failed: {exc.reason}")
        _refocus(refocus, handle.window_id)

    with HotkeyGrabber(handle.display) as grabber:
        for keysym in keymap:
            grabber.grab(keysym)
        while True:
            if not sl.pid_matches_identity(handle.pid, handle.start_ticks):
                print(json.dumps({"tool": TOOL, "verb": "game-exited"}), flush=True)
                return ev.EXIT_OK
            pressed = grabber.poll(timeout_seconds=0.5)
            if pressed is None:
                continue
            if pressed == "__window_gone__":
                return ev.EXIT_OK
            action = keymap.get(pressed)
            if action == "quit":
                print(json.dumps({"tool": TOOL, "verb": "quit"}), flush=True)
                return ev.EXIT_OK
            if action == "save":
                do_save(popup=True)
            elif action == "quicksave":
                do_save(popup=False)
            elif action == "load":
                do_load(popup=True)
            elif action == "quickload":
                do_load(popup=False)


def _refocus(xdo: sl.XDo, window_id: int) -> None:
    try:
        xdo.focus(window_id)
    except sl.SessionError:
        pass


def _git_ignored(path: Path) -> bool:
    try:
        result = subprocess.run(["git", "check-ignore", "-q", str(path)],
                                cwd=str(ev.repo_root()), capture_output=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def capabilities() -> dict:
    return {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "session_lib_version": sl.SESSION_LIB_VERSION,
        "verbs": ["run", "list"],
        "hotkeys": {
            "scope": "grabbed on the game's nested X display only, never host :0",
            "defaults": {"save": "F5 (filename popup)", "load": "F9 (picker)",
                         "quicksave": "F6", "quickload": "F7", "quit": "F12"},
            "configurable": "any --*-key, e.g. --save-key F1",
        },
        "backend": "game-memory.py snapshot/restore (live-validated, EXP-20260817-188)",
        "authorization": "the human keypress authorizes a load; every load writes a receipt",
        "not_a_savestate": "same-process memory checkpoints; do not survive a relaunch (CAP-011)",
        "validation": "game-memory backend is live-validated; the X key-grab and "
                      "Tk popups under Gamescope are logic-tested only and need a live run",
    }


def cmd_list(args: argparse.Namespace) -> int:
    handle = resolve_game(args)
    snapshot_dir = Path(args.snapshot_dir) if args.snapshot_dir else \
        ev.repo_root() / "work" / "snapshots"
    controller = SaveStateController(handle.pid, accept_sha=handle.exe_sha256,
                                     snapshot_dir=snapshot_dir, loader_re=args.loader_re)
    print(json.dumps({
        "tool": TOOL, "verb": "list",
        "saves": [{"name": s.name, "level": s.level, "captured_at": s.captured_at,
                   "bytes": s.total_bytes} for s in controller.list_saves()],
    }, indent=2))
    return ev.EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="savestate-hotkeys.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--capabilities", action="store_true")
    sub = parser.add_subparsers(dest="command")

    def add_target(p: argparse.ArgumentParser) -> None:
        p.add_argument("--session", default=None, help="session id, or 'current'")
        p.add_argument("--pid", type=int, default=None)
        p.add_argument("--display", default=None)
        p.add_argument("--window-id", type=int, default=None)
        p.add_argument("--loader-re", default=ev.DEFAULT_LOADER_RE)
        p.add_argument("--xdotool", default="xdotool")
        p.add_argument("--snapshot-dir", default=None)

    run = sub.add_parser("run", help="grab hotkeys and serve save/load")
    add_target(run)
    run.add_argument("--save-key", default="F5")
    run.add_argument("--load-key", default="F9")
    run.add_argument("--quicksave-key", default="F6")
    run.add_argument("--quickload-key", default="F7")
    run.add_argument("--quit-key", default="F12")
    run.add_argument("--no-popup", action="store_true",
                     help="skip the filename/picker dialogs (quick slots only)")
    run.add_argument("--no-clock", action="store_true",
                     help="default save name is 'save' rather than a timestamp")
    run.set_defaults(func=run_daemon_cmd)

    listing = sub.add_parser("list", help="list existing saves")
    add_target(listing)
    listing.set_defaults(func=cmd_list)
    return parser


def run_daemon_cmd(args: argparse.Namespace) -> int:
    handle = resolve_game(args)
    return run_daemon(handle, args)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.capabilities:
        print(json.dumps(capabilities(), indent=2))
        return ev.EXIT_OK
    if not getattr(args, "command", None):
        parser.print_usage(sys.stderr)
        return ev.EXIT_USAGE
    try:
        return args.func(args)
    except SaveStateError as exc:
        return _fail(exc.reason, exc.detail)
    except sl.SessionError as exc:
        return _fail(exc.reason, exc.detail)
    except ev.OwnershipError as exc:
        return _fail(exc.reason, exc.detail)


if __name__ == "__main__":
    sys.exit(main())
