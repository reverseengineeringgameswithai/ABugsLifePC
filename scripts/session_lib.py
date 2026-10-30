#!/usr/bin/env python3
"""Shared foundation for ABLPC live game-session control.

Stdlib only.  This module holds the session-control primitives that were
previously either unexposed Python inside the Tk companion
(``play-pristine-with-inputs.py``) or prose in
``Vault/10-Environment/PC autonomous game control.md``: owned-process
enumeration, nested-display resolution, exact game-window discovery, the
fail-closed renderer log gate, ``process_vm_readv``/``process_vm_writev``
access, and the durable session manifest that records exactly which process
identities and audio sinks a run owns.

Nothing here launches, signals, or writes to a process.  ``game-session.py``,
``game-memory.py``, ``send-keys.py``, and ``wait-for.py`` are the callers that
add those effects, each behind its own explicit refusal gates.

Two invariants are load-bearing and deliberately encoded here rather than in a
note:

* A session is identified by ``(pid, process-group, PID start ticks)``.  Start
  ticks make a recycled PID detectable, so cleanup can refuse to signal a
  process that merely reuses a recorded number.
* Renderer acceptance comes from the game log only.  ``evaluate_renderer_log``
  requires every positive marker and rejects on any software marker; no
  screenshot, key-press receipt, or selection summary can substitute.
"""

from __future__ import annotations

import ctypes
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
import subprocess
import time
from typing import Callable, Iterable, Sequence

import evidence_lib as ev


SESSION_LIB_VERSION = "1.0.0"
SESSION_SCHEMA_VERSION = 1

# Run-directory prefix for session manifests.  Kept distinct from the capture
# tools' prefixes (GDB/WINE/INP/CORE/FRZ) so a session is never confused with
# an evidence capture.
SESSION_RUN_PREFIX = "SESSION"

KNOWN_RETAIL_SHA256 = (
    "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
)
# scripts/play-pristine.sh --auto-hardware cache hash (EXP-20260816-150/151).
KNOWN_AUTO_HARDWARE_SHA256 = (
    "1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f"
)
ACCEPTED_EXECUTABLE_SHA256S = frozenset(
    {KNOWN_RETAIL_SHA256, KNOWN_AUTO_HARDWARE_SHA256}
)

GAME_WINDOW_CLASS = "bugs.exe"
GAME_WINDOW_SIZE = (640, 480)
GAME_LOG_BASENAME = "bugs.log"

DISPLAY_RE = re.compile(r"^:[0-9]+$")
KEYSYM_RE = re.compile(r"^[A-Za-z0-9_+]{1,32}$")

# The six positive markers required by Vault/00-System/START HERE.md.  Every
# one must be present in the same log for a renderer-facing arm to be
# accepted.  Verbatim from that note; do not paraphrase them.
HARDWARE_MARKERS: tuple[str, ...] = (
    "Native software render mode is FALSE",
    "RenderMode set to Direct3d render mode",
    "Screen mode 640x480x16 selected",
    "OnlySystemMemory status VIDEO MEMORY ONLY",
    "D3DAPPCREATE : Mode set to 640x480",
    "INIT : Starting Direct3D renderer",
)

# START HERE rejects an arm that "instead records SYSTEM MEMORY ONLY, 320x200,
# or INITSOFTRENDER".  The first and third are verbatim tokens.  The 320x200
# condition is expressed here as a selected-mode line, because
# Vault/10-Environment/PC autonomous game control.md records that the
# enumeration lines "DDMODE ... 320x200x*" list available modes and are not a
# reject condition on their own.  DDMODE lines are therefore skipped before
# testing.  Status: the INITSOFTRENDER and SYSTEM MEMORY ONLY tokens are
# confirmed; the exact selected-320x200 wording is derived from the positive
# 640x480 marker forms and is Inferred until a software arm is captured with
# this gate in place.
SOFTWARE_REJECT_MARKERS: tuple[str, ...] = (
    "INITSOFTRENDER",
    "SYSTEM MEMORY ONLY",
    "Native software render mode is TRUE",
)
SOFTWARE_REJECT_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"Screen mode 320x200"),
    re.compile(r"Mode set to 320x200"),
)
LOG_ENUMERATION_PREFIX = "DDMODE"

# Flik's Journey carousel position -> internal engine index at 0x00861C84.
# Statically derived from the level-select table at 0x004C6A30 and recorded in
# Vault/20-Research/PC level roster and numbering.md.  Position 0 is the
# carousel's starting "training" slot.
LEVEL_TABLE: tuple[tuple[int, str, int], ...] = (
    (0, "Training", 17),
    (1, "Anthill", 1),
    (2, "Tunnels", 3),
    (3, "Council Chamber", 2),
    (4, "Cliffside", 6),
    (5, "Riverbed Canyon", 10),
    (6, "Bird Nest", 11),
    (7, "City Entrance", 4),
    (8, "City Square", 5),
    (9, "Bug Bar", 14),
    (10, "Clover Forest", 7),
    (11, "The Tree", 12),
    (12, "Battle Arena", 13),
    (13, "Anthill Pt 2", 9),
    (14, "Riverbed Flight", 8),
    (15, "Canyon Showdown", 15),
)
LEVEL_ADDRESS = 0x00861C84
# Carousel position counter read by the level-select code at 0x0041475F before
# it indexes the table at 0x004C6A30 (PC level roster and numbering.md, static
# derivation).  Reading it makes a dropped carousel press detectable
# immediately, rather than after the wrong level has loaded.  Static-derived;
# its live width and behaviour are unvalidated until a runtime arm confirms
# them, so callers must report the raw value alongside any conclusion.
CAROUSEL_POSITION_ADDRESS = 0x00599AF8
CAROUSEL_POSITION_SIZE = 2
CAROUSEL_POSITION_COUNT = 16

# Menu input timing.  Vault/10-Environment/PC autonomous game control.md:
# menus poll GetAsyncKeyState, an ~12 ms xdotool tap falls between polls and is
# silently dropped, and every press in both EXP-20260816-156 arms landed with a
# ~180 ms hold.
DEFAULT_KEY_HOLD_MS = 180
DEFAULT_KEY_GAP_MS = 1000
MAX_KEY_HOLD_MS = 5000
MAX_KEY_PRESSES = 64

MAX_MEMORY_RANGES = 32
MAX_MEMORY_RANGE_BYTES = 65536
MAX_WRITE_BYTES = 256

# Region checkpointing (snapshot/restore) moves whole PE sections rather than a
# guarded field, so it uses its own bounds: one region up to this size, read
# and written in <=64 KiB syscalls.  The 256-byte poke cap above is deliberately
# left untouched, so the guarded single-field write path stays small.
MAX_REGION_BYTES = 16 << 20
CHUNK_BYTES = MAX_MEMORY_RANGE_BYTES

# bugs.exe PE image base and section layout (rabin2 sections; image base
# 0x00400000).  The mutable game state the project has identified — Flik
# position 0x0059D910, internal level 0x00861C84, NextLife 0x0059A5B0, the
# collision table 0x007F45A0, the type-1 pointer 0x005C5864 — all live inside
# the single writable .data section.  Capturing .data therefore captures every
# named global in one contiguous region that is neither code nor stack.
IMAGE_BASE = 0x00400000
DATA_SECTION_START = 0x004C1000
DATA_SECTION_END = 0x00864000  # exclusive; .idata begins here
DATA_SECTION_SIZE = DATA_SECTION_END - DATA_SECTION_START

# Process names that belong to a game session and must be accounted for at
# launch and closure (Agent Operating Manual#Runtime instance lifecycle).
RUNTIME_PROCESS_NAMES = (
    "bugs.exe",
    "gamescope",
    "gamescopereaper",
    "wineserver",
    "winedevice.exe",
    "Xwayland",
    "wine-preloader",
    "wine64-preloader",
)


class SessionError(RuntimeError):
    """Raised when a session precondition cannot be satisfied."""

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(detail or reason)
        self.reason = reason
        self.detail = detail


def refusal(tool: str, reason: str, detail: str = "") -> dict:
    """Return the shared refusal payload used by every ABLPC tool."""

    return {"refused": True, "tool": tool, "reason": reason, "detail": detail}


# --------------------------------------------------------------------------
# Process table
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ProcessRecord:
    pid: int
    process_group: int
    start_ticks: int
    command: tuple[str, ...]

    @property
    def executable(self) -> str:
        return Path(self.command[0]).name if self.command else ""

    def to_dict(self) -> dict:
        return {
            "pid": self.pid,
            "process_group": self.process_group,
            "start_ticks": self.start_ticks,
            "command": list(self.command),
        }


def parse_proc_stat(text: str) -> tuple[int, int]:
    """Return ``(process_group, start_ticks)`` from ``/proc/<pid>/stat`` text.

    The comm field may contain spaces and parentheses, so parsing resumes
    after the final ``)``.  Fields then run from ``state`` (field 3), making
    ``pgrp`` index 2 and ``starttime`` index 19.
    """

    close = text.rfind(")")
    if close < 0:
        raise ValueError("malformed /proc stat: no comm terminator")
    tail = text[close + 1:].split()
    if len(tail) < 20:
        raise ValueError(f"malformed /proc stat: {len(tail)} fields after comm")
    return int(tail[2], 10), int(tail[19], 10)


def process_records(proc_root: Path = Path("/proc")) -> tuple[ProcessRecord, ...]:
    """Snapshot every readable process as a :class:`ProcessRecord`.

    Processes that exit mid-scan are skipped rather than raising: the table is
    inherently racy and callers re-verify the identities they care about.
    """

    records: list[ProcessRecord] = []
    try:
        entries = tuple(proc_root.iterdir())
    except OSError as exc:
        raise SessionError("proc_unreadable", f"cannot enumerate {proc_root}: {exc}") from exc
    for entry in entries:
        if not entry.name.isdigit():
            continue
        try:
            pid = int(entry.name, 10)
            group, ticks = parse_proc_stat(
                (entry / "stat").read_text(encoding="utf-8", errors="replace")
            )
            command = tuple(
                part.decode("utf-8", "replace")
                for part in (entry / "cmdline").read_bytes().split(b"\0")
                if part
            )
        except (OSError, ValueError):
            continue
        records.append(ProcessRecord(pid, group, ticks, command))
    return tuple(records)


def pid_identity(pid: int, proc_root: Path = Path("/proc")) -> tuple[int, int]:
    """Return ``(process_group, start_ticks)`` for one live PID."""

    try:
        text = (proc_root / str(pid) / "stat").read_text(
            encoding="utf-8", errors="replace"
        )
    except OSError as exc:
        raise SessionError("no_such_pid", f"/proc/{pid}/stat unreadable: {exc}") from exc
    return parse_proc_stat(text)


def pid_matches_identity(
    pid: int, start_ticks: int, proc_root: Path = Path("/proc")
) -> bool:
    """True when ``pid`` is still the process that recorded ``start_ticks``.

    A recycled PID reports different start ticks, so this is what makes
    "terminate only the identities recorded at launch" enforceable rather than
    aspirational.
    """

    try:
        _, ticks = pid_identity(pid, proc_root=proc_root)
    except SessionError:
        return False
    return ticks == start_ticks


def group_members(
    records: Iterable[ProcessRecord], process_group: int
) -> tuple[ProcessRecord, ...]:
    return tuple(r for r in records if r.process_group == process_group)


def nested_display(
    records: Iterable[ProcessRecord], process_group: int
) -> str | None:
    """Resolve the nested Xwayland display owned by ``process_group``.

    Binding by process group rather than by ``pgrep Xwayland | head -1`` is
    what prevents attaching to a parallel session's game
    (``PC autonomous game control.md``, "Parallel-session caution").
    """

    matches: set[str] = set()
    for record in records:
        if record.process_group != process_group or not record.command:
            continue
        if record.executable.lower() != "xwayland":
            continue
        for token in record.command[1:]:
            if DISPLAY_RE.fullmatch(token):
                matches.add(token)
                break
    if len(matches) > 1:
        raise SessionError(
            "ambiguous_display",
            f"multiple nested X displays in owned process group: {sorted(matches)}",
        )
    return next(iter(matches), None)


# --------------------------------------------------------------------------
# xdotool / XTEST
# --------------------------------------------------------------------------


class XDo:
    """Bounded ``xdotool`` wrapper on one nested display.

    Key delivery uses XTEST against the focused window and never
    ``xdotool key --window``.  The chooser and menus read input with
    ``GetAsyncKeyState`` (chooser at ``0x004A7600``), which under Wine reflects
    real keyboard state, so synthetic ``XSendEvent`` input is ignored entirely
    (``PC autonomous game control.md``).  ``send_key`` therefore focuses first
    and holds the key across several frames.
    """

    def __init__(
        self,
        display: str,
        executable: str = "xdotool",
        *,
        timeout: float = 5.0,
        runner: Callable[[list[str], dict], subprocess.CompletedProcess] | None = None,
    ) -> None:
        if not DISPLAY_RE.fullmatch(display):
            raise SessionError("invalid_display", f"not an X display: {display!r}")
        self.display = display
        self.executable = executable
        self.timeout = timeout
        self._runner = runner

    def run(self, *args: str, allow_negative: bool = False) -> str:
        env = dict(os.environ)
        env["DISPLAY"] = self.display
        argv = [self.executable, *args]
        try:
            if self._runner is not None:
                result = self._runner(argv, env)
            else:
                result = subprocess.run(
                    argv,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    check=False,
                    env=env,
                )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise SessionError("xdotool_failed", f"{' '.join(argv)}: {exc}") from exc
        if result.returncode != 0:
            if allow_negative:
                return ""
            detail = (result.stderr or result.stdout or "").strip()
            raise SessionError(
                "xdotool_failed", f"{' '.join(args)} exited {result.returncode}: {detail}"
            )
        return (result.stdout or "").rstrip("\n")

    def search_game_windows(self) -> tuple[int, ...]:
        raw = self.run("search", "--class", GAME_WINDOW_CLASS, allow_negative=True)
        windows: list[int] = []
        for line in raw.splitlines():
            try:
                value = int(line.strip(), 0)
            except ValueError:
                continue
            if value > 0:
                windows.append(value)
        return tuple(dict.fromkeys(windows))

    def window_pid(self, window_id: int) -> int:
        raw = self.run("getwindowpid", str(window_id)).strip()
        try:
            value = int(raw, 10)
        except ValueError as exc:
            raise SessionError("window_pid_unparseable", repr(raw)) from exc
        if value <= 0:
            raise SessionError("window_pid_invalid", str(value))
        return value

    def window_class(self, window_id: int) -> str:
        return self.run("getwindowclassname", str(window_id))

    def geometry(self, window_id: int) -> tuple[int, int]:
        raw = self.run("getwindowgeometry", "--shell", str(window_id))
        values: dict[str, int] = {}
        for line in raw.splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key in {"WIDTH", "HEIGHT"}:
                try:
                    values[key] = int(value, 10)
                except ValueError as exc:
                    raise SessionError("geometry_unparseable", line) from exc
        if set(values) != {"WIDTH", "HEIGHT"}:
            raise SessionError("geometry_incomplete", "no WIDTH/HEIGHT rows")
        return values["WIDTH"], values["HEIGHT"]

    def focused_window(self) -> int:
        raw = self.run("getwindowfocus", allow_negative=True).strip()
        try:
            return int(raw, 10)
        except ValueError:
            return 0

    def focus(self, window_id: int) -> None:
        """Activate and focus one window, both synchronously.

        Both calls are issued because the game advances its logic loop only
        while its window holds input focus (EXP-20260816-148), and a lapse
        silently drops menu presses.
        """

        self.run("windowactivate", "--sync", str(window_id))
        self.run("windowfocus", "--sync", str(window_id))

    def send_key(
        self,
        window_id: int,
        keysym: str,
        *,
        hold_ms: int = DEFAULT_KEY_HOLD_MS,
        sleep: Callable[[float], None] = time.sleep,
        verify_focus: bool = True,
    ) -> dict:
        """Focus the window, hold ``keysym`` for ``hold_ms``, release it.

        Returns a per-press receipt.  Raises when focus cannot be established
        or is lost, because an unfocused press is silently dropped rather than
        failing loudly.
        """

        if not KEYSYM_RE.fullmatch(keysym):
            raise SessionError("invalid_keysym", repr(keysym))
        if hold_ms <= 0 or hold_ms > MAX_KEY_HOLD_MS:
            raise SessionError(
                "invalid_hold", f"hold_ms must be 1..{MAX_KEY_HOLD_MS}, got {hold_ms}"
            )
        self.focus(window_id)
        if verify_focus:
            focused = self.focused_window()
            if focused and focused != window_id:
                raise SessionError(
                    "focus_lost",
                    f"focused window {focused} is not the target {window_id}",
                )
        started = time.monotonic_ns()
        self.run("keydown", keysym)
        try:
            sleep(hold_ms / 1000.0)
        finally:
            self.run("keyup", keysym)
        ended = time.monotonic_ns()
        return {
            "keysym": keysym,
            "window_id": window_id,
            "hold_ms": hold_ms,
            "observed_hold_ms": round((ended - started) / 1e6, 3),
            "focus_verified": verify_focus,
            "method": "xtest",
        }


# --------------------------------------------------------------------------
# Game window discovery
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class GameTarget:
    display: str
    window_id: int
    pid: int
    process_group: int
    start_ticks: int
    window_class: str
    width: int
    height: int
    cwd: str
    exe_sha256: str

    def to_dict(self) -> dict:
        return {
            "display": self.display,
            "window_id": self.window_id,
            "pid": self.pid,
            "process_group": self.process_group,
            "start_ticks": self.start_ticks,
            "window_class": self.window_class,
            "width": self.width,
            "height": self.height,
            "cwd": self.cwd,
            "exe_sha256": self.exe_sha256,
        }


def discover_game_target(
    process_group: int,
    game_dir: Path,
    *,
    accepted_sha256: Iterable[str] = ACCEPTED_EXECUTABLE_SHA256S,
    process_reader: Callable[[], tuple[ProcessRecord, ...]] = process_records,
    xdo_factory: Callable[[str], XDo] = XDo,
    loader_re: str = ev.DEFAULT_LOADER_RE,
) -> GameTarget | None:
    """Find the one owned 640x480 ``bugs.exe`` window, or ``None``.

    Every candidate must satisfy all of: nested display owned by
    ``process_group``; window class ``bugs.exe``; geometry exactly 640x480;
    window PID inside ``process_group``; process CWD equal to ``game_dir``;
    and an ``evidence_lib`` ownership proof whose executable hash is accepted.
    More than one surviving candidate is an error, never a silent pick.
    """

    records = process_reader()
    display = nested_display(records, process_group)
    if display is None:
        return None
    probe = xdo_factory(display)
    accepted = {value.lower() for value in accepted_sha256}
    by_pid = {record.pid: record for record in records}
    candidates: list[GameTarget] = []
    for window_id in probe.search_game_windows():
        try:
            pid = probe.window_pid(window_id)
            record = by_pid.get(pid)
            if record is None or record.process_group != process_group:
                continue
            window_class = probe.window_class(window_id)
            if window_class.lower() != GAME_WINDOW_CLASS:
                continue
            size = probe.geometry(window_id)
            if size != GAME_WINDOW_SIZE:
                continue
            cwd = Path(os.readlink(f"/proc/{pid}/cwd")).resolve()
            if cwd != game_dir.resolve():
                continue
            proof = ev.ownership_proof(
                pid,
                cwd_prefix=str(cwd) + os.sep,
                loader_re=loader_re,
            )
            if proof.exe_sha256.lower() not in accepted:
                continue
        except (SessionError, OSError, ev.OwnershipError):
            continue
        candidates.append(
            GameTarget(
                display=display,
                window_id=window_id,
                pid=pid,
                process_group=process_group,
                start_ticks=record.start_ticks,
                window_class=window_class,
                width=size[0],
                height=size[1],
                cwd=str(cwd),
                exe_sha256=proof.exe_sha256,
            )
        )
    if len(candidates) > 1:
        raise SessionError(
            "ambiguous_window",
            f"{len(candidates)} exact 640x480 bugs.exe windows in the owned session",
        )
    return candidates[0] if candidates else None


# --------------------------------------------------------------------------
# Renderer log gate
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class RendererGate:
    accepted: bool
    markers_found: dict[str, int]
    markers_missing: tuple[str, ...]
    rejects_found: tuple[dict, ...]
    lines_scanned: int

    def to_dict(self) -> dict:
        return {
            "accepted": self.accepted,
            "markers_found": self.markers_found,
            "markers_missing": list(self.markers_missing),
            "rejects_found": [dict(item) for item in self.rejects_found],
            "lines_scanned": self.lines_scanned,
            "required_marker_count": len(HARDWARE_MARKERS),
        }


def evaluate_renderer_log(text: str) -> RendererGate:
    """Apply the fail-closed six-marker hardware gate to game-log text.

    Acceptance requires every marker in :data:`HARDWARE_MARKERS` and no
    software reject.  ``DDMODE`` enumeration lines are excluded from the
    320x200 test because they list available modes rather than the selected
    one (``PC autonomous game control.md``).
    """

    found: dict[str, int] = {}
    rejects: list[dict] = []
    lines = text.splitlines()
    for number, line in enumerate(lines, start=1):
        for marker in HARDWARE_MARKERS:
            if marker not in found and marker in line:
                found[marker] = number
        stripped = line.lstrip()
        if stripped.startswith(LOG_ENUMERATION_PREFIX):
            continue
        for marker in SOFTWARE_REJECT_MARKERS:
            if marker in line:
                rejects.append({"marker": marker, "line": number, "text": line.strip()})
        for pattern in SOFTWARE_REJECT_PATTERNS:
            if pattern.search(line):
                rejects.append(
                    {"marker": pattern.pattern, "line": number, "text": line.strip()}
                )
    missing = tuple(m for m in HARDWARE_MARKERS if m not in found)
    return RendererGate(
        accepted=not missing and not rejects,
        markers_found=found,
        markers_missing=missing,
        rejects_found=tuple(rejects),
        lines_scanned=len(lines),
    )


def read_log_text(path: Path, *, from_offset: int = 0, max_bytes: int = 1 << 22) -> tuple[str, int]:
    """Read game-log bytes from ``from_offset``, returning text and end offset.

    The game recreates ``bugs.log`` on each ``log``-argument launch, so a
    caller carrying an offset from a previous run must detect truncation:
    when the file is shorter than ``from_offset`` the read restarts at zero
    and the returned end offset reflects the new file.
    """

    try:
        size = path.stat().st_size
    except OSError as exc:
        raise SessionError("log_unreadable", f"{path}: {exc}") from exc
    start = 0 if size < from_offset else from_offset
    with open(path, "rb") as handle:
        handle.seek(start)
        raw = handle.read(max_bytes)
    return raw.decode("utf-8", "replace"), start + len(raw)


# --------------------------------------------------------------------------
# Process memory
# --------------------------------------------------------------------------


class IOVec(ctypes.Structure):
    _fields_ = [("iov_base", ctypes.c_void_p), ("iov_len", ctypes.c_size_t)]


class ProcessMemory:
    """``process_vm_readv``/``process_vm_writev`` access to one live process.

    Reads are ordinary evidence gathering.  Writes are a separate, explicitly
    authorized action: this class exposes :meth:`write_many`, but every caller
    in the repository gates it behind an authorization reference and a
    compare-before-write guard (see ``game-memory.py poke``).
    """

    def __init__(self, pid: int, *, libc=None) -> None:
        if pid <= 0:
            raise SessionError("invalid_pid", f"pid must be positive, got {pid}")
        self.pid = pid
        self.libc = libc if libc is not None else ctypes.CDLL(None, use_errno=True)
        self._readv = self.libc.process_vm_readv
        self._writev = self.libc.process_vm_writev
        for handle in (self._readv, self._writev):
            handle.argtypes = (
                ctypes.c_int,
                ctypes.POINTER(IOVec),
                ctypes.c_ulong,
                ctypes.POINTER(IOVec),
                ctypes.c_ulong,
                ctypes.c_ulong,
            )
            handle.restype = ctypes.c_ssize_t

    @staticmethod
    def _check_plan(plan: Sequence[tuple[int, int]]) -> None:
        if not plan or len(plan) > MAX_MEMORY_RANGES:
            raise SessionError(
                "invalid_plan", f"1..{MAX_MEMORY_RANGES} ranges required, got {len(plan)}"
            )
        for address, size in plan:
            if address <= 0:
                raise SessionError("invalid_address", f"0x{address:X}")
            if size <= 0 or size > MAX_MEMORY_RANGE_BYTES:
                raise SessionError(
                    "invalid_size", f"1..{MAX_MEMORY_RANGE_BYTES} bytes required, got {size}"
                )

    def read_many(self, requests: Iterable[tuple[int, int]]) -> tuple[bytes, ...]:
        plan = tuple(requests)
        self._check_plan(plan)
        buffers = tuple(ctypes.create_string_buffer(size) for _, size in plan)
        local = (IOVec * len(plan))(
            *(
                IOVec(ctypes.cast(buffer, ctypes.c_void_p), size)
                for buffer, (_, size) in zip(buffers, plan, strict=True)
            )
        )
        remote = (IOVec * len(plan))(
            *(IOVec(ctypes.c_void_p(address), size) for address, size in plan)
        )
        expected = sum(size for _, size in plan)
        ctypes.set_errno(0)
        received = self._readv(self.pid, local, len(plan), remote, len(plan), 0)
        if received != expected:
            error = ctypes.get_errno()
            detail = os.strerror(error) if error else f"short read {received}/{expected}"
            raise SessionError("read_failed", f"process_vm_readv: {detail}")
        return tuple(
            buffer.raw[:size] for buffer, (_, size) in zip(buffers, plan, strict=True)
        )

    def read(self, address: int, size: int) -> bytes:
        return self.read_many(((address, size),))[0]

    def read_region(self, address: int, size: int) -> bytes:
        """Read a large contiguous region in <=64 KiB syscalls.

        Used by snapshot/restore to move whole sections; a short read is an
        error, so a torn or partially-unmapped region fails rather than
        returning silent garbage.
        """

        if address <= 0:
            raise SessionError("invalid_address", f"0x{address:X}")
        if size <= 0 or size > MAX_REGION_BYTES:
            raise SessionError(
                "invalid_region", f"1..{MAX_REGION_BYTES} bytes required, got {size}"
            )
        parts: list[bytes] = []
        offset = 0
        while offset < size:
            span = min(CHUNK_BYTES, size - offset)
            parts.append(self.read(address + offset, span))
            offset += span
        return b"".join(parts)

    def write_region(self, address: int, payload: bytes) -> int:
        """Write a large contiguous region in <=64 KiB syscalls.

        Deliberately separate from :meth:`write_many`, whose 256-byte cap
        guards the single-field poke path.  This path is only reached by
        restore, which is itself authorization-gated by its caller.
        """

        if address <= 0:
            raise SessionError("invalid_address", f"0x{address:X}")
        size = len(payload)
        if size <= 0 or size > MAX_REGION_BYTES:
            raise SessionError(
                "invalid_region", f"1..{MAX_REGION_BYTES} bytes required, got {size}"
            )
        offset = 0
        while offset < size:
            span = min(CHUNK_BYTES, size - offset)
            chunk = payload[offset:offset + span]
            buffer = ctypes.create_string_buffer(chunk, span)
            local = (IOVec * 1)(IOVec(ctypes.cast(buffer, ctypes.c_void_p), span))
            remote = (IOVec * 1)(IOVec(ctypes.c_void_p(address + offset), span))
            ctypes.set_errno(0)
            written = self._writev(self.pid, local, 1, remote, 1, 0)
            if written != span:
                error = ctypes.get_errno()
                detail = os.strerror(error) if error else f"short write {written}/{span}"
                raise SessionError(
                    "write_failed",
                    f"process_vm_writev at 0x{address + offset:08X}: {detail}",
                )
            offset += span
        return size

    def write_many(self, writes: Iterable[tuple[int, bytes]]) -> int:
        """Write payloads to the target, returning the byte count written.

        A short write is an error, not a partial success: the caller cannot
        reason about a half-applied multi-field write, so the tools treat any
        mismatch as a failed arm.
        """

        plan = tuple(writes)
        self._check_plan(tuple((address, len(payload)) for address, payload in plan))
        total = sum(len(payload) for _, payload in plan)
        if total > MAX_WRITE_BYTES:
            raise SessionError(
                "write_too_large", f"at most {MAX_WRITE_BYTES} bytes per call, got {total}"
            )
        buffers = tuple(ctypes.create_string_buffer(payload, len(payload)) for _, payload in plan)
        local = (IOVec * len(plan))(
            *(
                IOVec(ctypes.cast(buffer, ctypes.c_void_p), len(payload))
                for buffer, (_, payload) in zip(buffers, plan, strict=True)
            )
        )
        remote = (IOVec * len(plan))(
            *(IOVec(ctypes.c_void_p(address), len(payload)) for address, payload in plan)
        )
        ctypes.set_errno(0)
        written = self._writev(self.pid, local, len(plan), remote, len(plan), 0)
        if written != total:
            error = ctypes.get_errno()
            detail = os.strerror(error) if error else f"short write {written}/{total}"
            raise SessionError("write_failed", f"process_vm_writev: {detail}")
        return written


def read_internal_level(memory: ProcessMemory) -> int:
    """Read the internal engine level index at ``0x00861C84``.

    Carousel position is not the internal level number, so navigation must be
    confirmed from this global rather than from a screenshot
    (``PC level roster and numbering.md``).
    """

    return int.from_bytes(memory.read(LEVEL_ADDRESS, 4), "little", signed=True)


# --------------------------------------------------------------------------
# Memory maps and freeze
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class MemoryMapping:
    start: int
    end: int
    perms: str
    offset: int
    path: str

    @property
    def size(self) -> int:
        return self.end - self.start

    @property
    def writable(self) -> bool:
        return "w" in self.perms

    @property
    def private(self) -> bool:
        return "p" in self.perms

    def to_dict(self) -> dict:
        return {
            "start": f"0x{self.start:08X}",
            "end": f"0x{self.end:08X}",
            "size": self.size,
            "perms": self.perms,
            "offset": self.offset,
            "path": self.path,
        }


def read_maps(pid: int, proc_root: Path = Path("/proc")) -> tuple[MemoryMapping, ...]:
    """Parse ``/proc/<pid>/maps`` into mappings."""

    try:
        text = (proc_root / str(pid) / "maps").read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise SessionError("maps_unreadable", f"/proc/{pid}/maps: {exc}") from exc
    mappings: list[MemoryMapping] = []
    for line in text.splitlines():
        parts = line.split(maxsplit=5)
        if len(parts) < 5:
            continue
        span, perms, offset = parts[0], parts[1], parts[2]
        path = parts[5] if len(parts) > 5 else ""
        if "-" not in span:
            continue
        start_hex, end_hex = span.split("-", 1)
        try:
            start = int(start_hex, 16)
            end = int(end_hex, 16)
            file_offset = int(offset, 16)
        except ValueError:
            continue
        mappings.append(MemoryMapping(start, end, perms, file_offset, path))
    return tuple(mappings)


def mapping_covering(
    mappings: Iterable[MemoryMapping], start: int, end: int
) -> MemoryMapping | None:
    """Return the mapping that fully contains ``[start, end)``, or ``None``."""

    for mapping in mappings:
        if mapping.start <= start and end <= mapping.end:
            return mapping
    return None


def freeze(pid: int, *, kill=os.kill) -> None:
    """Stop every thread of ``pid`` with ``SIGSTOP`` for an atomic memory op.

    Mirrors ``scripts/frozen-capture.sh``: gamescope and wineserver keep
    running to serve the held frame, and only the game process is frozen.  On
    this setup the game already advances its logic loop only while focused
    (EXP-20260816-148), but the freeze makes a multi-megabyte read or write
    atomic against every game thread regardless of focus.
    """

    import signal as _signal

    kill(pid, _signal.SIGSTOP)


def unfreeze(pid: int, *, kill=os.kill) -> None:
    """Resume ``pid`` with ``SIGCONT``."""

    import signal as _signal

    kill(pid, _signal.SIGCONT)


def read_carousel_position(
    memory: ProcessMemory, address: int = CAROUSEL_POSITION_ADDRESS
) -> int:
    """Read the level-select carousel position counter."""

    return int.from_bytes(
        memory.read(address, CAROUSEL_POSITION_SIZE), "little", signed=False
    )


def level_by_name(name: str) -> tuple[int, str, int]:
    """Resolve a level name to ``(carousel_position, name, internal_index)``."""

    want = name.strip().lower()
    for position, label, internal in LEVEL_TABLE:
        if label.lower() == want:
            return position, label, internal
    raise SessionError(
        "unknown_level",
        f"{name!r} is not in the level roster: "
        + ", ".join(label for _, label, _ in LEVEL_TABLE),
    )


# --------------------------------------------------------------------------
# Audio sinks
# --------------------------------------------------------------------------


def list_null_sinks(
    *, pactl: str = "pactl",
    runner: Callable[[list[str]], subprocess.CompletedProcess] | None = None,
) -> tuple[dict, ...]:
    """List loaded ``module-null-sink`` modules, or ``()`` when pactl is absent."""

    argv = [pactl, "list", "short", "modules"]
    try:
        if runner is not None:
            result = runner(argv)
        else:
            result = subprocess.run(
                argv, capture_output=True, text=True, timeout=5, check=False
            )
    except (OSError, subprocess.TimeoutExpired):
        return ()
    if result.returncode != 0:
        return ()
    sinks: list[dict] = []
    for line in (result.stdout or "").splitlines():
        parts = line.split("\t")
        if len(parts) < 2 or parts[1].strip() != "module-null-sink":
            continue
        arguments = parts[2].strip() if len(parts) > 2 else ""
        name = ""
        match = re.search(r"sink_name=([^\s]+)", arguments)
        if match:
            name = match.group(1)
        try:
            module_id = int(parts[0].strip(), 10)
        except ValueError:
            continue
        sinks.append({"module_id": module_id, "sink_name": name, "arguments": arguments})
    return tuple(sinks)


# --------------------------------------------------------------------------
# Runtime audit
# --------------------------------------------------------------------------


def _is_host_display(record: ProcessRecord) -> bool:
    """True when an Xwayland record serves the host desktop display ``:0``."""

    for token in record.command[1:]:
        if DISPLAY_RE.fullmatch(token):
            return token == ":0"
    return False


def audit_runtime(
    records: Iterable[ProcessRecord],
    *,
    owned_groups: Iterable[int] = (),
    names: Iterable[str] = RUNTIME_PROCESS_NAMES,
) -> dict:
    """Classify runtime-related processes as owned or unattributed.

    The unattributed list is the durable answer to the EXP-163 closure audit,
    which found 32 ``winedevice.exe`` processes with no ownership ledger and
    could therefore neither attribute nor terminate them.
    """

    wanted = {name.lower() for name in names}
    owned = set(owned_groups)
    matched: list[dict] = []
    for record in records:
        executable = record.executable.lower()
        command_name = ""
        if record.command:
            command_name = Path(record.command[0].replace("\\", "/")).name.lower()
        if executable not in wanted and command_name not in wanted:
            continue
        if executable == "xwayland" and _is_host_display(record):
            # The desktop's own Xwayland on :0 is not session residue; only
            # the nested displays a gamescope session creates are.
            continue
        row = record.to_dict()
        row["name"] = executable or command_name
        row["owned"] = record.process_group in owned
        matched.append(row)
    return {
        "processes": matched,
        "owned_count": sum(1 for row in matched if row["owned"]),
        "unattributed_count": sum(1 for row in matched if not row["owned"]),
        "owned_groups": sorted(owned),
    }


# --------------------------------------------------------------------------
# Session manifest
# --------------------------------------------------------------------------


@dataclass
class SessionManifest:
    """Durable record of exactly what one launched session owns.

    Persisted to ``dynamic/wine/RUN-SESSION-<stamp>/session.json``.  Liveness
    is never trusted from the file: ``game-session.py status`` re-derives it
    from ``/proc`` and compares start ticks.
    """

    session_id: str
    schema_version: int = SESSION_SCHEMA_VERSION
    state: str = "open"
    created_at: str = ""
    closed_at: str | None = None
    launcher_command: list[str] = field(default_factory=list)
    launcher_pid: int | None = None
    process_group: int | None = None
    game_dir: str = ""
    prefix: str = ""
    log_path: str = ""
    display: str | None = None
    window_id: int | None = None
    game_pid: int | None = None
    game_start_ticks: int | None = None
    exe_sha256: str | None = None
    auto_hardware: bool = False
    renderer_gate: dict | None = None
    owned_processes: list[dict] = field(default_factory=list)
    owned_sinks: list[dict] = field(default_factory=list)
    level: dict | None = None
    notes: list[str] = field(default_factory=list)
    closure: dict | None = None

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "schema_version": self.schema_version,
            "state": self.state,
            "created_at": self.created_at,
            "closed_at": self.closed_at,
            "launcher_command": list(self.launcher_command),
            "launcher_pid": self.launcher_pid,
            "process_group": self.process_group,
            "game_dir": self.game_dir,
            "prefix": self.prefix,
            "log_path": self.log_path,
            "display": self.display,
            "window_id": self.window_id,
            "game_pid": self.game_pid,
            "game_start_ticks": self.game_start_ticks,
            "exe_sha256": self.exe_sha256,
            "auto_hardware": self.auto_hardware,
            "renderer_gate": self.renderer_gate,
            "owned_processes": [dict(item) for item in self.owned_processes],
            "owned_sinks": [dict(item) for item in self.owned_sinks],
            "level": self.level,
            "notes": list(self.notes),
            "closure": self.closure,
        }

    @classmethod
    def from_dict(cls, raw: dict) -> "SessionManifest":
        if not isinstance(raw, dict):
            raise SessionError("manifest_malformed", "session manifest is not an object")
        session_id = raw.get("session_id")
        if not isinstance(session_id, str) or not session_id:
            raise SessionError("manifest_malformed", "session_id missing")
        version = raw.get("schema_version")
        if version != SESSION_SCHEMA_VERSION:
            raise SessionError(
                "manifest_schema",
                f"expected schema {SESSION_SCHEMA_VERSION}, found {version!r}",
            )
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{key: value for key, value in raw.items() if key in known})

    def path(self, root: Path | None = None) -> Path:
        return session_dir(self.session_id, root=root) / "session.json"

    def save(self, root: Path | None = None) -> Path:
        target = self.path(root=root)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(self.to_dict(), indent=2) + "\n", encoding="utf-8")
        tmp.replace(target)
        return target


def sessions_root(root: Path | None = None) -> Path:
    return (root or ev.repo_root()) / ev.RUN_ROOT


def session_dir(session_id: str, root: Path | None = None) -> Path:
    if not re.fullmatch(r"RUN-SESSION-[0-9]{8}-[0-9]{6}", session_id):
        raise SessionError("invalid_session_id", repr(session_id))
    return sessions_root(root) / session_id


def load_session(session_id: str, root: Path | None = None) -> SessionManifest:
    path = session_dir(session_id, root=root) / "session.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SessionError("session_not_found", str(path)) from exc
    except json.JSONDecodeError as exc:
        raise SessionError("manifest_malformed", f"{path}: {exc}") from exc
    return SessionManifest.from_dict(raw)


def iter_sessions(root: Path | None = None) -> tuple[SessionManifest, ...]:
    base = sessions_root(root)
    if not base.is_dir():
        return ()
    found: list[SessionManifest] = []
    for entry in sorted(base.glob("RUN-SESSION-*")):
        manifest = entry / "session.json"
        if not manifest.is_file():
            continue
        try:
            found.append(SessionManifest.from_dict(json.loads(manifest.read_text(encoding="utf-8"))))
        except (SessionError, json.JSONDecodeError, OSError):
            continue
    return tuple(found)


def session_is_live(manifest: SessionManifest, proc_root: Path = Path("/proc")) -> bool:
    """True when the recorded game PID is still the same process."""

    if manifest.game_pid is None or manifest.game_start_ticks is None:
        return False
    return pid_matches_identity(
        manifest.game_pid, manifest.game_start_ticks, proc_root=proc_root
    )


def resolve_session(
    session_id: str | None, root: Path | None = None, proc_root: Path = Path("/proc")
) -> SessionManifest:
    """Resolve an explicit session id, or the single live open session.

    Ambiguity is a refusal rather than a guess: picking "the first" session is
    exactly the parallel-session hazard this module exists to remove.
    """

    if session_id and session_id != "current":
        return load_session(session_id, root=root)
    live = [
        manifest
        for manifest in iter_sessions(root=root)
        if manifest.state == "open" and session_is_live(manifest, proc_root=proc_root)
    ]
    if not live:
        raise SessionError("no_live_session", "no open session with a live game process")
    if len(live) > 1:
        raise SessionError(
            "ambiguous_session",
            "multiple live sessions: " + ", ".join(m.session_id for m in live),
        )
    return live[0]


def new_session_id(moment=None) -> str:
    return f"RUN-{SESSION_RUN_PREFIX}-{ev.run_stamp(moment)}"
