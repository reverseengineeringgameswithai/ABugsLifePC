#!/usr/bin/env python3
"""Read-only live coordinate display for the exact PC game process.

The tool verifies one ``bugs.exe`` process under ``work/copies/`` whose
executable is exactly retail or the accepted EXP-20260815-136 grain-gates
profile, and samples known PC runtime fields with ``process_vm_readv``.  It
never attaches, pauses, sets breakpoints, or writes target memory.  The
default UI is a draggable, translucent, always-on-top overlay; ``--mode
window`` provides an ordinary decorated-window fallback.  ``--gates`` adds
the nearest grain-gate mechanism readout from the EXP-20260815-139 static
trigger geometry for the Tunnels/City mapping pass.
"""

from __future__ import annotations

import argparse
import ctypes
from dataclasses import dataclass
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import struct
import subprocess
import sys
import time
from typing import Iterable, Protocol

import evidence_lib as ev


TOOL = "coordinate-overlay"
TOOL_VERSION = "1.3.0"
KNOWN_RETAIL_SHA256 = (
    "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
)
# Accepted EXP-20260815-136 grain-gates profile build; its edits do not
# overlap any address this tool reads except the City requirement lookup,
# which is read only on this exact build.
KNOWN_GRAIN_GATES_PROFILE_SHA256 = (
    "69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b"
)
ALLOWED_EXECUTABLE_SHA256S = frozenset(
    {KNOWN_RETAIL_SHA256, KNOWN_GRAIN_GATES_PROFILE_SHA256}
)

# EXP-20260815-128 runtime-discriminates this triple from the auxiliary
# ground/reset coordinates at 0x0059D960: its Y field follows the complete
# Shift-jump arc while X/Z follow ordinary directional movement.
XYZ_ADDRESS = 0x0059D910
FLAGS_ADDRESS = 0x0059D9A0
NEXT_LIFE_ADDRESS = 0x0059A5B0
STATE_COUNTER_ADDRESS = 0x0059D9A4
LEVEL_ADDRESS = 0x00861C84
COLLISION_INDEX_ADDRESS = 0x007F3D68
COLLISION_TABLE_ADDRESS = 0x007F45A0
COLLISION_STRIDE = 48
COLLISION_MATERIAL_OFFSET = 0x1E
MAX_COLLISION_INDEX = 4096
POSITION_RE = re.compile(r"^[+-][0-9]+[+-][0-9]+$")
DISPLAY_RE = re.compile(r"^:[0-9]+$")

# EXP-20260815-139 static grain-gate trigger geometry. Visible Tunnels is
# internal level 3 and City Entrance internal level 4 (EXP-20260815-136).
TUNNELS_INTERNAL_LEVEL = 3
CITY_INTERNAL_LEVEL = 4
TUNNELS_GATE_TABLE_ADDRESS = 0x004DA9C8
TUNNELS_GATE_ROW_COUNT = 9
TUNNELS_GATE_ROW_STRIDE = 20
TUNNELS_OPEN_DISTANCE_SQ = 0x2710
TUNNELS_MESSAGE_DISTANCE_SQ = 0x640
CITY_GATE_STATE_ADDRESS = 0x0059F020
CITY_REQUIREMENT_TABLE_ADDRESS = 0x004338B0
CITY_RETAIL_REQUIREMENTS = (10, 20, 30)
# (x, z, radius parameter) immediates from the three 0x00433900 call sites.
CITY_GATES = (
    (-71129, -184314, 80),
    (354031, 35256, 90),
    (582271, 310212, 100),
)
GATE_DISTANCE_SHIFT = 8


def engine_gate_distance_sq(flik_x: int, flik_z: int, gate_x: int, gate_z: int) -> int:
    """Planar squared distance exactly as PC helper ``0x00416580`` computes it.

    Python ``>>`` on negative integers is an arithmetic shift, matching the
    ``sar`` instructions in the helper and in the Tunnels inline copy.
    """

    dx = (flik_x - gate_x) >> GATE_DISTANCE_SHIFT
    dz = (flik_z - gate_z) >> GATE_DISTANCE_SHIFT
    return dx * dx + dz * dz


def _world_distance(flik_x: int, flik_z: int, gate_x: int, gate_z: int) -> int:
    return math.isqrt(
        (flik_x - gate_x) ** 2 + (flik_z - gate_z) ** 2
    )


class OverlayError(RuntimeError):
    pass


class MemoryReader(Protocol):
    def read_many(self, requests: Iterable[tuple[int, int]]) -> tuple[bytes, ...]:
        ...


class IOVec(ctypes.Structure):
    _fields_ = [("iov_base", ctypes.c_void_p), ("iov_len", ctypes.c_size_t)]


class ProcessMemory:
    """Small read-only ``process_vm_readv`` wrapper."""

    def __init__(self, pid: int, *, libc=None) -> None:
        if pid <= 0:
            raise OverlayError("PID must be positive")
        self.pid = pid
        self.libc = libc if libc is not None else ctypes.CDLL(None, use_errno=True)
        self._readv = self.libc.process_vm_readv
        self._readv.argtypes = (
            ctypes.c_int,
            ctypes.POINTER(IOVec),
            ctypes.c_ulong,
            ctypes.POINTER(IOVec),
            ctypes.c_ulong,
            ctypes.c_ulong,
        )
        self._readv.restype = ctypes.c_ssize_t

    def read_many(self, requests: Iterable[tuple[int, int]]) -> tuple[bytes, ...]:
        plan = tuple(requests)
        if not plan or len(plan) > 32:
            raise OverlayError("memory read plan must contain 1..32 ranges")
        for address, size in plan:
            if address <= 0 or size <= 0 or size > 65536:
                raise OverlayError("invalid memory read address or size")

        buffers = tuple(ctypes.create_string_buffer(size) for _, size in plan)
        local = (IOVec * len(plan))(
            *(IOVec(ctypes.cast(buffer, ctypes.c_void_p), size)
              for buffer, (_, size) in zip(buffers, plan, strict=True))
        )
        remote = (IOVec * len(plan))(
            *(IOVec(ctypes.c_void_p(address), size) for address, size in plan)
        )
        expected = sum(size for _, size in plan)
        ctypes.set_errno(0)
        received = self._readv(
            self.pid, local, len(plan), remote, len(plan), 0
        )
        if received != expected:
            error = ctypes.get_errno()
            detail = os.strerror(error) if error else f"short read {received}/{expected}"
            raise OverlayError(f"process_vm_readv failed: {detail}")
        return tuple(
            buffer.raw[:size]
            for buffer, (_, size) in zip(buffers, plan, strict=True)
        )


@dataclass(frozen=True)
class CoordinateSample:
    x: int
    y: int
    z: int
    level: int
    flags: int
    next_life: int
    state_counter: int
    collision_index: int
    collision_material: int | None
    sampled_ns: int

    def coordinate_text(self) -> str:
        return (
            f"X {self.x:>9d}\n"
            f"Y {self.y:>9d}\n"
            f"Z {self.z:>9d}"
        )

    def detail_text(self) -> str:
        material = "—" if self.collision_material is None else str(self.collision_material)
        return (
            f"{self.coordinate_text()}\n"
            f"LEVEL {self.level:>3d}   FLAGS 0x{self.flags:04X}\n"
            f"NEXT {self.next_life:>3d}   STATE {self.state_counter:>4d}\n"
            f"COLLISION {self.collision_index:>4d}   VALUE {material}"
        )

    def display_text(self) -> str:
        """Compatibility alias for the opt-in diagnostic readout."""

        return self.detail_text()


def read_coordinate_sample(
    memory: MemoryReader, *, monotonic_ns=time.monotonic_ns
) -> CoordinateSample:
    xyz, flags, next_life, counter, level, collision = memory.read_many(
        (
            (XYZ_ADDRESS, 12),
            (FLAGS_ADDRESS, 2),
            (NEXT_LIFE_ADDRESS, 2),
            (STATE_COUNTER_ADDRESS, 2),
            (LEVEL_ADDRESS, 4),
            (COLLISION_INDEX_ADDRESS, 4),
        )
    )
    x, y, z = struct.unpack("<iii", xyz)
    flags_value = struct.unpack("<H", flags)[0]
    next_value = struct.unpack("<H", next_life)[0]
    counter_value = struct.unpack("<h", counter)[0]
    level_value = struct.unpack("<i", level)[0]
    collision_index = struct.unpack("<i", collision)[0]
    collision_material: int | None = None
    if 0 <= collision_index < MAX_COLLISION_INDEX:
        address = (
            COLLISION_TABLE_ADDRESS
            + collision_index * COLLISION_STRIDE
            + COLLISION_MATERIAL_OFFSET
        )
        collision_material = struct.unpack(
            "<h", memory.read_many(((address, 2),))[0]
        )[0]
    return CoordinateSample(
        x=x,
        y=y,
        z=z,
        level=level_value,
        flags=flags_value,
        next_life=next_value,
        state_counter=counter_value,
        collision_index=collision_index,
        collision_material=collision_material,
        sampled_ns=monotonic_ns(),
    )


@dataclass(frozen=True)
class GateSample:
    """Nearest grain-gate mechanism for the mapping pass (EXP-20260815-139)."""

    kind: str  # "T" Tunnels row, "C" City Entrance gate
    index: int
    requirement: int | None
    status: int  # Tunnels: live row type dword; City: live state dword
    distance_sq: int  # engine sar-8 space
    threshold_sq: int  # engine sar-8 space
    world_distance: int

    @property
    def inside(self) -> bool:
        return self.distance_sq < self.threshold_sq

    @property
    def world_radius(self) -> int:
        return math.isqrt(self.threshold_sq) << GATE_DISTANCE_SHIFT

    def gate_text(self) -> str:
        requirement = "?" if self.requirement is None else str(self.requirement)
        status = (
            f"TYPE 0x{self.status & 0xFFFFFFFF:04X}"
            if self.kind == "T"
            else f"STATE {self.status}"
        )
        verdict = "IN" if self.inside else "out"
        return (
            f"GATE {self.kind}{self.index}   REQ {requirement}   {status}\n"
            f"DIST {self.world_distance}/{self.world_radius} {verdict}"
        )


def resolve_city_requirements(
    memory: MemoryReader, exe_sha256: str
) -> tuple[int | None, int | None, int | None]:
    """Return the three City Entrance requirements for a verified build.

    Retail derives ``10 * (index + 1)`` at ``0x004337D1``; the accepted
    grain-gates profile replaces that with the three-dword lookup at
    ``0x004338B0``, which is read once from the live image. Any other hash
    has no accepted requirement source and yields unknowns.
    """

    normalized = exe_sha256.lower()
    if normalized == KNOWN_RETAIL_SHA256:
        return CITY_RETAIL_REQUIREMENTS
    if normalized == KNOWN_GRAIN_GATES_PROFILE_SHA256:
        raw = memory.read_many(((CITY_REQUIREMENT_TABLE_ADDRESS, 12),))[0]
        return struct.unpack("<iii", raw)
    return (None, None, None)


def read_nearest_gate(
    memory: MemoryReader,
    sample: CoordinateSample,
    city_requirements: tuple[int | None, int | None, int | None],
) -> GateSample | None:
    """Read-only nearest-mechanism sample for internal levels 3 and 4."""

    if sample.level == TUNNELS_INTERNAL_LEVEL:
        raw = memory.read_many(
            (
                (
                    TUNNELS_GATE_TABLE_ADDRESS,
                    TUNNELS_GATE_ROW_COUNT * TUNNELS_GATE_ROW_STRIDE,
                ),
            )
        )[0]
        values = struct.unpack(f"<{TUNNELS_GATE_ROW_COUNT * 5}i", raw)
        best: GateSample | None = None
        for row in range(TUNNELS_GATE_ROW_COUNT):
            row_type, _, requirement, gate_x, gate_z = values[row * 5 : row * 5 + 5]
            candidate = GateSample(
                kind="T",
                index=row,
                requirement=requirement,
                status=row_type,
                distance_sq=engine_gate_distance_sq(
                    sample.x, sample.z, gate_x, gate_z
                ),
                threshold_sq=TUNNELS_OPEN_DISTANCE_SQ,
                world_distance=_world_distance(sample.x, sample.z, gate_x, gate_z),
            )
            if best is None or candidate.distance_sq < best.distance_sq:
                best = candidate
        return best
    if sample.level == CITY_INTERNAL_LEVEL:
        raw = memory.read_many(((CITY_GATE_STATE_ADDRESS, 12),))[0]
        states = struct.unpack("<iii", raw)
        best = None
        for index, (gate_x, gate_z, radius) in enumerate(CITY_GATES):
            candidate = GateSample(
                kind="C",
                index=index,
                requirement=city_requirements[index],
                status=states[index],
                distance_sq=engine_gate_distance_sq(
                    sample.x, sample.z, gate_x, gate_z
                ),
                threshold_sq=radius * radius,
                world_distance=_world_distance(sample.x, sample.z, gate_x, gate_z),
            )
            if best is None or candidate.distance_sq < best.distance_sq:
                best = candidate
        return best
    return None


def _proc_stat_identity(raw: str) -> tuple[int, int]:
    """Return process group (field 5) and start time (field 22)."""

    close = raw.rfind(")")
    if close < 0:
        raise OverlayError("malformed /proc stat: missing command terminator")
    tail = raw[close + 1 :].split()
    if len(tail) < 20:
        raise OverlayError("malformed /proc stat: too few fields")
    try:
        return int(tail[2], 10), int(tail[19], 10)
    except ValueError as exc:
        raise OverlayError("malformed /proc stat: non-integer identity") from exc


@dataclass(frozen=True)
class TargetIdentity:
    pid: int
    process_group: int
    start_time: int
    cwd: str
    exe_sha256: str

    @classmethod
    def verify_initial(
        cls, pid: int, process_group: int, cwd_prefix: str
    ) -> "TargetIdentity":
        try:
            proof = ev.ownership_proof(
                pid,
                expected_sha256=None,
                cwd_prefix=cwd_prefix,
            )
            raw = Path(f"/proc/{pid}/stat").read_text(
                encoding="utf-8", errors="replace"
            )
            observed_group, start_time = _proc_stat_identity(raw)
        except (OSError, ev.OwnershipError) as exc:
            raise OverlayError(f"target ownership refused: {exc}") from exc
        if proof.exe_sha256.lower() not in ALLOWED_EXECUTABLE_SHA256S:
            raise OverlayError(
                "target executable sha256 "
                f"{proof.exe_sha256} is neither exact retail nor the accepted "
                "EXP-20260815-136 grain-gates profile"
            )
        if observed_group != process_group:
            raise OverlayError(
                f"target process group {observed_group} != expected {process_group}"
            )
        return cls(
            pid=pid,
            process_group=process_group,
            start_time=start_time,
            cwd=proof.cwd,
            exe_sha256=proof.exe_sha256,
        )

    def reverify_runtime(self) -> None:
        try:
            raw = Path(f"/proc/{self.pid}/stat").read_text(
                encoding="utf-8", errors="replace"
            )
            process_group, start_time = _proc_stat_identity(raw)
        except OSError as exc:
            raise OverlayError("game process exited") from exc
        if (process_group, start_time) != (self.process_group, self.start_time):
            raise OverlayError("game PID identity changed")


class CoordinateWindow:
    def __init__(
        self,
        root,
        identity: TargetIdentity,
        memory: MemoryReader,
        *,
        mode: str,
        opacity: float,
        interval_ms: int,
        position: str,
        details: bool,
        gamescope_overlay: bool,
        gates: bool = False,
        city_requirements: tuple[int | None, int | None, int | None] = (
            None,
            None,
            None,
        ),
    ) -> None:
        import tkinter as tk

        self.tk = tk
        self.root = root
        self.identity = identity
        self.memory = memory
        self.mode = mode
        self.opacity = opacity
        self.interval_ms = interval_ms
        self.details = details
        self.gates = gates
        self.city_requirements = city_requirements
        self.gamescope_overlay = gamescope_overlay
        self.failure_count = 0
        self.drag_origin: tuple[int, int, int, int] | None = None
        self.closing = False

        root.title("ABLPC Coordinates")
        root.configure(background="#101418")
        # Ask the nested X window manager for ABOVE before making the overlay
        # override-redirect; some compositors ignore a later state request.
        root.attributes("-topmost", True)
        if mode == "overlay":
            root.overrideredirect(True)
            try:
                root.attributes("-alpha", opacity)
            except tk.TclError:
                pass
        else:
            root.resizable(False, False)
        root.geometry(position)
        root.protocol("WM_DELETE_WINDOW", self.close)

        self.text = tk.StringVar(value="Waiting for game state…")
        label = tk.Label(
            root,
            textvariable=self.text,
            justify="left",
            anchor="nw",
            padx=12,
            pady=10,
            background="#101418",
            foreground="#E8F5E9",
            font=("DejaVu Sans Mono", 15 if not details else 12, "bold"),
        )
        label.pack(fill="both", expand=True)
        for widget in (root, label):
            widget.bind("<ButtonPress-1>", self.begin_drag)
            widget.bind("<B1-Motion>", self.drag)
            widget.bind("<Double-Button-1>", self.toggle_chrome)
            widget.bind("<Button-3>", lambda _event: self.close())
        root.bind("<Escape>", lambda _event: self.close())
        root.bind("<Control-q>", lambda _event: self.close())
        root.update_idletasks()
        self.keep_above()
        root.after_idle(self.maintain_above)
        self.apply_window_properties()
        root.after(100, self.apply_window_properties)
        self.poll()

    def keep_above(self) -> None:
        self.root.lift()
        self.root.attributes("-topmost", True)

    def maintain_above(self) -> None:
        """Restack after game mode/window transitions inside Gamescope."""

        if self.closing:
            return
        self.keep_above()
        self.root.after(500, self.maintain_above)

    def set_x11_cardinal(self, property_name: str, value: int) -> None:
        display = os.environ.get("DISPLAY", "")
        xprop = shutil.which("xprop")
        if not DISPLAY_RE.fullmatch(display) or xprop is None:
            return
        window_ids = {str(self.root.winfo_id())}
        xdotool = shutil.which("xdotool")
        if xdotool is not None:
            try:
                discovered = subprocess.run(
                    [
                        xdotool,
                        "search",
                        "--pid",
                        str(os.getpid()),
                        "--name",
                        "^ABLPC Coordinates$",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=1,
                    check=False,
                )
                window_ids.update(
                    line.strip()
                    for line in discovered.stdout.splitlines()
                    if line.strip().isdigit()
                )
            except (OSError, subprocess.TimeoutExpired):
                pass
        try:
            for window_id in sorted(window_ids):
                subprocess.run(
                    [
                        xprop,
                        "-id",
                        window_id,
                        "-f",
                        property_name,
                        "32c",
                        "-set",
                        property_name,
                        str(value),
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=1,
                    check=False,
                )
        except (OSError, subprocess.TimeoutExpired):
            pass

    def apply_window_properties(self) -> None:
        """Apply compositor properties after Tk maps its top-level X window."""

        self.apply_gamescope_layer()
        self.apply_opacity()

    def apply_gamescope_layer(self) -> None:
        if self.gamescope_overlay:
            self.set_x11_cardinal(
                "GAMESCOPE_EXTERNAL_OVERLAY", 1 if self.mode == "overlay" else 0
            )

    def apply_opacity(self) -> None:
        """Set both Tk and EWMH opacity, where the X11 compositor supports it."""

        wanted = self.opacity if self.mode == "overlay" else 1.0
        try:
            self.root.attributes("-alpha", wanted)
        except self.tk.TclError:
            pass
        cardinal = round(wanted * 0xFFFFFFFF)
        self.set_x11_cardinal("_NET_WM_WINDOW_OPACITY", cardinal)

    def begin_drag(self, event) -> None:
        self.drag_origin = (
            event.x_root,
            event.y_root,
            self.root.winfo_x(),
            self.root.winfo_y(),
        )

    def drag(self, event) -> None:
        if self.drag_origin is None:
            return
        start_x, start_y, window_x, window_y = self.drag_origin
        self.root.geometry(
            f"+{window_x + event.x_root - start_x}+{window_y + event.y_root - start_y}"
        )

    def toggle_chrome(self, _event=None) -> None:
        self.mode = "window" if self.mode == "overlay" else "overlay"
        self.root.overrideredirect(self.mode == "overlay")
        self.root.after_idle(self.keep_above)
        self.root.after_idle(self.apply_window_properties)

    def close(self) -> None:
        if self.closing:
            return
        self.closing = True
        self.root.destroy()

    def poll(self) -> None:
        if self.closing:
            return
        try:
            self.identity.reverify_runtime()
            sample = read_coordinate_sample(self.memory)
            gate = (
                read_nearest_gate(self.memory, sample, self.city_requirements)
                if self.gates
                else None
            )
        except OverlayError as exc:
            self.failure_count += 1
            self.text.set(f"Coordinate read unavailable\n{exc}")
            if self.failure_count >= 5:
                self.root.after(1200, self.close)
                return
        else:
            self.failure_count = 0
            text = sample.detail_text() if self.details else sample.coordinate_text()
            if self.gates:
                text += "\n" + (gate.gate_text() if gate is not None else "GATE —")
            self.text.set(text)
        self.root.after(self.interval_ms, self.poll)


def _opacity(text: str) -> float:
    try:
        value = float(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("opacity must be a number") from exc
    if not 0.2 <= value <= 1.0:
        raise argparse.ArgumentTypeError("opacity must be between 0.2 and 1.0")
    return value


def _interval(text: str) -> int:
    try:
        value = int(text, 10)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("interval must be an integer") from exc
    if not 16 <= value <= 2000:
        raise argparse.ArgumentTypeError("interval must be 16..2000 ms")
    return value


def capabilities() -> dict[str, object]:
    return {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "target": (
            "exact retail or accepted EXP-20260815-136 grain-gates profile "
            "PC bugs.exe under work/copies/"
        ),
        "allowed_executable_sha256s": sorted(ALLOWED_EXECUTABLE_SHA256S),
        "read_backend": "process_vm_readv",
        "writes_target_memory": False,
        "attaches_debugger": False,
        "pauses_target": False,
        "sets_breakpoints": False,
        "fields": [
            "actor_xyz",
            "internal_level",
            "actor_flags",
            "next_life",
            "state_counter",
            "collision_index",
            "collision_material_value",
            "nearest_grain_gate",
        ],
        "coordinate_address": "0x0059D910",
        "coordinate_evidence": "EXP-20260815-128",
        "gate_geometry_evidence": "EXP-20260815-139",
        "modes": ["overlay", "window"],
        "default_readout": ["actor_x", "actor_y", "actor_z"],
        "diagnostic_readout_opt_in": True,
        "nearest_gate_readout_opt_in": True,
        "overlay": {
            "translucent": True,
            "always_on_top": True,
            "target_display_aware": True,
            "gamescope_external_overlay_atom": True,
            "draggable": True,
            "click_through": False,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Show read-only PC game coordinates in a live Tk overlay."
    )
    parser.add_argument("--pid", type=int, help="verified bugs.exe PID")
    parser.add_argument("--process-group", type=int, help="expected owned process group")
    parser.add_argument(
        "--cwd-prefix",
        help="expected work-copy directory prefix (default: repository work/copies/)",
    )
    parser.add_argument("--mode", choices=("overlay", "window"), default="overlay")
    parser.add_argument("--opacity", type=_opacity, default=0.78)
    parser.add_argument("--interval-ms", type=_interval, default=100)
    parser.add_argument("--position", default="+12+12")
    parser.add_argument(
        "--display",
        help="owned Gamescope X display (for example :2); defaults to current DISPLAY",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="also show level, flags, state, and collision diagnostics",
    )
    parser.add_argument(
        "--gates",
        action="store_true",
        help=(
            "also show the nearest Tunnels/City grain-gate mechanism, its "
            "requirement, live state, and engine-exact trigger distance"
        ),
    )
    parser.add_argument("--capabilities", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.capabilities:
        print(json.dumps(capabilities(), indent=2, sort_keys=True))
        return 0
    if args.pid is None or args.process_group is None:
        parser.error("--pid and --process-group are required")
    if not POSITION_RE.fullmatch(args.position):
        parser.error("--position must look like +24+24 or -10+20")
    if args.display is not None:
        if not DISPLAY_RE.fullmatch(args.display):
            parser.error("--display must look like :2")
        os.environ["DISPLAY"] = args.display
    root_dir = ev.repo_root().resolve()
    cwd_prefix = args.cwd_prefix or str(root_dir / "work" / "copies") + os.sep
    try:
        identity = TargetIdentity.verify_initial(
            args.pid, args.process_group, cwd_prefix
        )
        memory = ProcessMemory(args.pid)
        city_requirements = (
            resolve_city_requirements(memory, identity.exe_sha256)
            if args.gates
            else (None, None, None)
        )
    except OverlayError as exc:
        print(json.dumps({"refused": True, "tool": TOOL, "reason": str(exc)}))
        return 3

    received_signal: list[int] = []
    previous_handlers: dict[int, object] = {}
    app: CoordinateWindow | None = None
    try:
        import tkinter as tk

        root = tk.Tk()
        app = CoordinateWindow(
            root,
            identity,
            memory,
            mode=args.mode,
            opacity=args.opacity,
            interval_ms=args.interval_ms,
            position=args.position,
            details=args.details,
            gamescope_overlay=args.display is not None,
            gates=args.gates,
            city_requirements=city_requirements,
        )

        def request_shutdown(signum: int, _frame: object) -> None:
            received_signal.append(signum)
            if app is not None:
                root.after(0, app.close)

        for signum in (signal.SIGINT, signal.SIGTERM):
            previous_handlers[signum] = signal.getsignal(signum)
            signal.signal(signum, request_shutdown)
        root.mainloop()
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"Coordinate overlay failed: {exc}", file=sys.stderr)
        return 3
    finally:
        for signum, previous in previous_handlers.items():
            signal.signal(signum, previous)
    if received_signal:
        return 128 + received_signal[-1]
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
