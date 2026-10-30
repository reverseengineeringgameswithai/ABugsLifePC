"""Synthetic game-session fixture for the session-control tool tests.

Builds a process tree structurally identical to a real launch -- a launcher
that owns its own process group, a nested ``Xwayland`` on its own display, and
a ``bugs.exe`` process under a ``work/copies/`` tree -- without Wine,
Gamescope, or any game asset.

The fake game maps anonymous memory over the exact address window holding the
PC globals the tools read (``0x00599000``..``0x00862FFF``), so the internal
level global ``0x00861C84``, the carousel counter ``0x00599AF8``, and the
position triples at ``0x0059D910`` are readable and writable at their real
addresses.  ``game-memory.py``, ``wait-for.py``, and ``game-session.py`` are
therefore exercised against a real ``process_vm_readv``/``process_vm_writev``
target rather than a mock.

The fake game consumes the key log written by the stub ``xdotool``: a carousel
press advances the counter, ``Return`` confirms the chooser (appending the
renderer markers) and later selects a level through the statically derived
table.  Dropped presses can be injected and are detected exactly as they would
be live.  The game also mirrors one address to another every loop, giving the
write tests an independent confirmation that the target's own view of memory
changed rather than only the writer's readback.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import time

# Address window covering every global the tools touch.
MAP_BASE = 0x00599000
MAP_SIZE = 0x2CA000  # through 0x00862FFF

LEVEL_ADDRESS = 0x00861C84
CAROUSEL_ADDRESS = 0x00599AF8
CURRENT_XYZ = 0x0059D910
PRECEDING_XYZ = 0x0059D920
AUXILIARY_XYZ = 0x0059D960
FLAGS_ADDRESS = 0x0059D9A0
NEXT_LIFE_ADDRESS = 0x0059A5B0
STATE_COUNTER_ADDRESS = 0x0059D9A4
COLLISION_INDEX_ADDRESS = 0x007F3D68
COLLISION_TABLE_ADDRESS = 0x007F45A0
SCRATCH_ADDRESS = 0x005A0000
MIRROR_SRC_ADDRESS = 0x005A1000
MIRROR_DST_ADDRESS = 0x005A2000

# Carousel position -> internal level index (PC level roster and numbering).
LEVEL_TABLE = (17, 1, 3, 2, 6, 10, 11, 4, 5, 14, 7, 12, 13, 9, 8, 15)

HARDWARE_MARKERS = (
    "Native software render mode is FALSE",
    "RenderMode set to Direct3d render mode",
    "Screen mode 640x480x16 selected",
    "OnlySystemMemory status VIDEO MEMORY ONLY",
    "D3DAPPCREATE : Mode set to 640x480",
    "INIT : Starting Direct3D renderer",
)
SOFTWARE_MARKERS = (
    "Native software render mode is TRUE",
    "INITSOFTRENDER",
    "OnlySystemMemory status SYSTEM MEMORY ONLY",
)

FAKE_GAME_SOURCE = r'''
import ctypes, json, os, struct, sys, time

config = json.loads(sys.argv[1])
BASE = config["map_base"]
SIZE = config["map_size"]

libc = ctypes.CDLL(None, use_errno=True)
libc.mmap.restype = ctypes.c_void_p
libc.mmap.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int,
                      ctypes.c_int, ctypes.c_int, ctypes.c_long)
PROT_READ_WRITE = 0x1 | 0x2
FLAGS = 0x02 | 0x20 | 0x100000  # PRIVATE | ANONYMOUS | FIXED_NOREPLACE
got = libc.mmap(ctypes.c_void_p(BASE), SIZE, PROT_READ_WRITE, FLAGS, -1, 0)
ready_path = config.get("ready_path")
if got != BASE:
    message = "MAPFAIL %s" % os.strerror(ctypes.get_errno())
    if ready_path:
        open(ready_path, "w").write(message)
    print(message, flush=True)
    sys.exit(3)


def poke(address, payload):
    ctypes.memmove(ctypes.c_void_p(address), payload, len(payload))


def peek(address, size):
    return ctypes.string_at(address, size)


for address, payload in config["initial"].items():
    poke(int(address), bytes.fromhex(payload))

carousel = config.get("carousel_start", 0)
poke(config["carousel_address"], struct.pack("<H", carousel))

log_path = config.get("log_path")
keys_path = config.get("keys_path")
markers = list(config.get("confirm_markers") or [])
mirror_src = config.get("mirror_src")
mirror_dst = config.get("mirror_dst")

if ready_path:
    open(ready_path, "w").write("READY %d" % os.getpid())
print("READY %d" % os.getpid(), flush=True)

seen_keys = 0
deadline = time.monotonic() + config.get("lifetime_s", 120)
while time.monotonic() < deadline:
    if keys_path and os.path.exists(keys_path):
        try:
            with open(keys_path, "r", encoding="utf-8") as handle:
                lines = handle.read().splitlines()
        except OSError:
            lines = []
        while seen_keys < len(lines):
            key = lines[seen_keys].strip()
            seen_keys += 1
            if key == "Right":
                carousel = (carousel + 1) % 16
                poke(config["carousel_address"], struct.pack("<H", carousel))
            elif key == "Left":
                carousel = (carousel - 1) % 16
                poke(config["carousel_address"], struct.pack("<H", carousel))
            elif key == "Return":
                if markers and log_path:
                    with open(log_path, "a", encoding="utf-8") as handle:
                        for marker in markers:
                            handle.write(marker + "\n")
                    markers = []
                else:
                    table = config["level_table"]
                    poke(config["level_address"],
                         struct.pack("<i", table[carousel]))
    if mirror_src is not None and mirror_dst is not None:
        poke(mirror_dst, peek(mirror_src, 4))
    time.sleep(0.02)
'''

LAUNCHER_SOURCE = r'''#!/usr/bin/env python3
"""Stand-in for scripts/play-pristine.sh in the session-control tests.

Owns its process group, starts a nested Xwayland stand-in and the fake game as
children, records their PIDs, and waits -- the same topology the real launcher
produces under gamescope.
"""
import json, os, subprocess, sys, time

config_path = os.environ.get("ABLPC_FIXTURE_CONFIG") or sys.argv[1]
config = json.loads(open(config_path, encoding="utf-8").read())
extra = sys.argv[1:]

if config.get("pre_log_lines"):
    with open(config["log_path"], "a", encoding="utf-8") as handle:
        for line in config["pre_log_lines"]:
            handle.write(line + "\n")

children = []
xwayland = subprocess.Popen(
    ["Xwayland", "-c", "import time;time.sleep(%f)" % config["lifetime_s"],
     config["display"], "-rootless"],
    executable=sys.executable,
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
children.append(xwayland)

game = subprocess.Popen(
    ["bugs.exe", "-c", config["game_source"], json.dumps(config["game_config"])],
    executable=sys.executable,
    cwd=config["game_dir"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
children.append(game)

with open(config["status_path"], "w", encoding="utf-8") as handle:
    json.dump({
        "launcher_pid": os.getpid(),
        "process_group": os.getpgid(0),
        "xwayland_pid": xwayland.pid,
        "game_pid": game.pid,
        "argv": extra,
    }, handle)

deadline = time.monotonic() + config["lifetime_s"]
try:
    while time.monotonic() < deadline:
        time.sleep(0.05)
finally:
    for child in children:
        try:
            child.terminate()
        except OSError:
            pass
'''

STUB_XDOTOOL = r'''#!/usr/bin/env bash
# Stub xdotool for the session-control tests.  Records every invocation and
# answers window queries from a JSON state file.  A key press is recorded only
# when delivered the way the game actually accepts it: XTEST to the focused
# window, never "key --window" (synthetic XSendEvent, which the game ignores).
set -u
STATE="__STATE__"
LOG="__LOG__"
KEYS="__KEYS__"
printf '%s\n' "$*" >> "$LOG"

value() { "__PYTHON__" -c "import json,sys;print(json.load(open('$STATE'))[sys.argv[1]])" "$1"; }

case "${1:-}" in
  search) value window_id ;;
  getwindowpid)
    "__PYTHON__" -c "
import json,sys
state=json.load(open('$STATE'))
path=state.get('status_path')
if path:
    print(json.load(open(path))['game_pid'])
else:
    print(state['game_pid'])
"
    ;;
  getwindowclassname) value window_class ;;
  getwindowgeometry)
    echo "WINDOW=$(value window_id)"
    echo "X=0"
    echo "Y=0"
    echo "WIDTH=$(value width)"
    echo "HEIGHT=$(value height)"
    ;;
  getwindowfocus) value focused_window ;;
  windowactivate|windowfocus) exit 0 ;;
  key)
    # A whole-key press: too short to survive GetAsyncKeyState polling, and
    # with --window it is synthetic.  Never recorded as delivered input.
    exit 0
    ;;
  keydown)
    shift
    if [ "${1:-}" = "--window" ]; then exit 0; fi
    if [ -f "$STATE.drop" ] && grep -qx -- "$1" "$STATE.drop"; then
      sed -i "0,/^$1\$/{/^$1\$/d}" "$STATE.drop"
      exit 0
    fi
    printf '%s\n' "$1" >> "$KEYS"
    exit 0
    ;;
  keyup) exit 0 ;;
  *) exit 0 ;;
esac
'''


def pack_xyz(x: int, y: int, z: int) -> str:
    return struct.pack("<iii", x, y, z).hex()


def default_initial_state() -> dict[str, str]:
    """Known values at the real global addresses, as hex payloads."""

    return {
        str(CURRENT_XYZ): pack_xyz(501696, 30092, 494016),
        str(PRECEDING_XYZ): pack_xyz(501000, 30092, 494000),
        str(AUXILIARY_XYZ): pack_xyz(500000, 30000, 493000),
        str(FLAGS_ADDRESS): struct.pack("<H", 0x0014).hex(),
        str(NEXT_LIFE_ADDRESS): struct.pack("<H", 0).hex(),
        str(STATE_COUNTER_ADDRESS): struct.pack("<h", 3).hex(),
        str(LEVEL_ADDRESS): struct.pack("<i", 0).hex(),
        str(COLLISION_INDEX_ADDRESS): struct.pack("<i", 572).hex(),
        str(COLLISION_TABLE_ADDRESS + 572 * 48 + 0x1E): struct.pack("<h", 1).hex(),
        str(SCRATCH_ADDRESS): "deadbeef",
        str(MIRROR_SRC_ADDRESS): "00000000",
        str(MIRROR_DST_ADDRESS): "00000000",
    }


def game_config(
    *,
    ready_path: Path | None = None,
    keys_path: Path | None = None,
    log_path: Path | None = None,
    confirm_markers: tuple[str, ...] = (),
    carousel_start: int = 0,
    lifetime_s: float = 120.0,
    initial: dict[str, str] | None = None,
) -> dict:
    return {
        "map_base": MAP_BASE,
        "map_size": MAP_SIZE,
        "initial": default_initial_state() if initial is None else initial,
        "level_address": LEVEL_ADDRESS,
        "carousel_address": CAROUSEL_ADDRESS,
        "level_table": list(LEVEL_TABLE),
        "carousel_start": carousel_start,
        "lifetime_s": lifetime_s,
        "ready_path": str(ready_path) if ready_path else None,
        "keys_path": str(keys_path) if keys_path else None,
        "log_path": str(log_path) if log_path else None,
        "confirm_markers": list(confirm_markers),
        "mirror_src": MIRROR_SRC_ADDRESS,
        "mirror_dst": MIRROR_DST_ADDRESS,
    }


def make_game_dir(root: Path, name: str = "game") -> tuple[Path, str]:
    """Create ``work/copies/<name>/bugs.exe`` and return its path and hash."""

    game_dir = root / "work" / "copies" / name
    game_dir.mkdir(parents=True, exist_ok=True)
    exe = game_dir / "bugs.exe"
    exe.write_bytes(b"MZ-fake-game-fixture")
    return game_dir, hashlib.sha256(exe.read_bytes()).hexdigest()


def write_stub_xdotool(
    directory: Path,
    *,
    window_id: int,
    game_pid: int,
    window_class: str = "bugs.exe",
    width: int = 640,
    height: int = 480,
    focused_window: int | None = None,
    drop_keys: tuple[str, ...] = (),
    status_path: Path | None = None,
) -> tuple[Path, Path, Path, Path]:
    """Write the stub; return ``(binary, state, call_log, key_log)``."""

    state = directory / "xdotool-state.json"
    call_log = directory / "xdotool-calls.log"
    key_log = directory / "xdotool-keys.log"
    write_stub_state(
        state, window_id=window_id, game_pid=game_pid, window_class=window_class,
        width=width, height=height, focused_window=focused_window,
        status_path=status_path,
    )
    if drop_keys:
        Path(str(state) + ".drop").write_text(
            "\n".join(drop_keys) + "\n", encoding="utf-8"
        )
    call_log.touch()
    key_log.touch()
    binary = directory / "xdotool"
    binary.write_text(
        STUB_XDOTOOL
        .replace("__STATE__", str(state))
        .replace("__LOG__", str(call_log))
        .replace("__KEYS__", str(key_log))
        .replace("__PYTHON__", sys.executable),
        encoding="utf-8",
    )
    binary.chmod(0o755)
    return binary, state, call_log, key_log


def write_stub_state(
    state: Path,
    *,
    window_id: int,
    game_pid: int,
    window_class: str = "bugs.exe",
    width: int = 640,
    height: int = 480,
    focused_window: int | None = None,
    status_path: Path | None = None,
) -> None:
    payload = {
        "window_id": window_id,
        "game_pid": game_pid,
        "window_class": window_class,
        "width": width,
        "height": height,
        "focused_window": window_id if focused_window is None else focused_window,
    }
    if status_path is not None:
        # Resolve the game PID from the launcher's status file at call time,
        # because the tool starts the launcher itself and the PID is not known
        # when the stub is written.
        payload["status_path"] = str(status_path)
    state.write_text(json.dumps(payload), encoding="utf-8")


class FakeGame:
    """A standalone ``bugs.exe``-shaped process with the PC globals mapped."""

    def __init__(
        self,
        root: Path,
        *,
        name: str = "game",
        lifetime_s: float = 120.0,
        keys_path: Path | None = None,
        log_path: Path | None = None,
        confirm_markers: tuple[str, ...] = (),
        carousel_start: int = 0,
    ) -> None:
        self.root = root
        self.name = name
        self.lifetime_s = lifetime_s
        self.keys_path = keys_path
        self.log_path = log_path
        self.confirm_markers = confirm_markers
        self.carousel_start = carousel_start
        self.game_dir: Path | None = None
        self.exe_sha256 = ""
        self.process: subprocess.Popen | None = None

    def __enter__(self) -> "FakeGame":
        self.game_dir, self.exe_sha256 = make_game_dir(self.root, self.name)
        config = game_config(
            keys_path=self.keys_path, log_path=self.log_path,
            confirm_markers=self.confirm_markers,
            carousel_start=self.carousel_start, lifetime_s=self.lifetime_s,
        )
        self.process = subprocess.Popen(
            ["bugs.exe", "-c", FAKE_GAME_SOURCE, json.dumps(config)],
            executable=sys.executable,
            cwd=str(self.game_dir),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            start_new_session=True,
        )
        line = (self.process.stdout.readline() or "").strip()
        if not line.startswith("READY"):
            detail = line + (self.process.stderr.read() if self.process.stderr else "")
            self.close()
            raise RuntimeError(f"fake game failed to start: {detail}")
        return self

    @property
    def pid(self) -> int:
        assert self.process is not None
        return self.process.pid

    def close(self) -> None:
        if self.process is None:
            return
        try:
            self.process.terminate()
            self.process.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            try:
                self.process.kill()
            except OSError:
                pass

    def __exit__(self, *exc: object) -> None:
        self.close()


class FakeSession:
    """A launcher-owned process group with a nested display and a fake game."""

    def __init__(
        self,
        root: Path,
        *,
        display: str = ":9",
        lifetime_s: float = 120.0,
        confirm_markers: tuple[str, ...] = HARDWARE_MARKERS,
        pre_log_lines: tuple[str, ...] = (),
        carousel_start: int = 0,
        name: str = "game",
    ) -> None:
        self.root = root
        self.display = display
        self.lifetime_s = lifetime_s
        self.confirm_markers = confirm_markers
        self.pre_log_lines = pre_log_lines
        self.carousel_start = carousel_start
        self.name = name
        self.game_dir: Path | None = None
        self.exe_sha256 = ""
        self.launcher_path: Path | None = None
        self.config_path: Path | None = None
        self.status_path: Path | None = None
        self.keys_path: Path | None = None
        self.log_path: Path | None = None
        self.process: subprocess.Popen | None = None
        self.status: dict = {}

    def prepare(self) -> Path:
        """Write the launcher and its config; return the launcher path."""

        self.game_dir, self.exe_sha256 = make_game_dir(self.root, self.name)
        support = self.root / "fixture"
        support.mkdir(parents=True, exist_ok=True)
        self.status_path = support / "session-status.json"
        self.keys_path = support / "xdotool-keys.log"
        self.log_path = self.game_dir / "bugs.log"
        self.launcher_path = support / "play-stub.py"
        self.launcher_path.write_text(LAUNCHER_SOURCE, encoding="utf-8")
        self.launcher_path.chmod(0o755)
        config = {
            "display": self.display,
            "lifetime_s": self.lifetime_s,
            "game_dir": str(self.game_dir),
            "game_source": FAKE_GAME_SOURCE,
            "status_path": str(self.status_path),
            "log_path": str(self.log_path),
            "pre_log_lines": list(self.pre_log_lines),
            "game_config": game_config(
                keys_path=self.keys_path, log_path=self.log_path,
                confirm_markers=self.confirm_markers,
                carousel_start=self.carousel_start, lifetime_s=self.lifetime_s,
            ),
        }
        self.config_path = support / "launcher-config.json"
        self.config_path.write_text(json.dumps(config), encoding="utf-8")
        return self.launcher_path

    def launcher_argv(self) -> list[str]:
        assert self.launcher_path is not None and self.config_path is not None
        return [sys.executable, str(self.launcher_path), str(self.config_path)]

    def start(self, timeout: float = 20.0) -> dict:
        """Start the launcher directly (for tests that do not use the tool)."""

        argv = self.launcher_argv()
        self.process = subprocess.Popen(
            argv, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            start_new_session=True, text=True,
        )
        return self.await_status(timeout=timeout)

    def await_status(self, timeout: float = 20.0) -> dict:
        assert self.status_path is not None
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.status_path.exists():
                try:
                    self.status = json.loads(self.status_path.read_text(encoding="utf-8"))
                    return self.status
                except json.JSONDecodeError:
                    pass
            time.sleep(0.05)
        raise RuntimeError("fake session never reported its status")

    def close(self) -> None:
        pids = [
            self.status.get("game_pid"),
            self.status.get("xwayland_pid"),
            self.status.get("launcher_pid"),
        ]
        for pid in pids:
            if not pid:
                continue
            try:
                os.kill(pid, 15)
            except OSError:
                pass
        if self.process is not None:
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    self.process.kill()
                except OSError:
                    pass

    def __enter__(self) -> "FakeSession":
        self.prepare()
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def have_fixed_mapping() -> bool:
    """True when the fixture's fixed address window can actually be mapped."""

    config = game_config(lifetime_s=0.05, initial={})
    probe = subprocess.run(
        [sys.executable, "-c", FAKE_GAME_SOURCE, json.dumps(config)],
        capture_output=True, text=True, timeout=30,
    )
    return "MAPFAIL" not in (probe.stdout or "")
