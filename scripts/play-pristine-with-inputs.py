#!/usr/bin/env python3
"""Launch the pinned pristine PC game with an exact-window input control panel.

The existing ``play-pristine.sh`` remains the launcher authority.  This
companion starts it in an isolated process session, discovers only the nested
Gamescope X11 ``bugs.exe`` window owned by that session, and drives
``input-movie.py`` with verified PID/display/window arguments.

The GUI never captures host or display-wide input.  Recording and replay are
both delegated to ``input-movie.py`` for the one discovered game window.
Gameplay recording defaults to a new ``NextLife`` log milestone after level
initialization; a separate Level Select anchor remains available for menu-only
movies.  Stop Recording sends only F12 to that exact window after re-proving
its identity.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import json
import os
from pathlib import Path
import re
import signal
import shutil
import subprocess
import sys
import time
from typing import Callable, Iterable

import evidence_lib as ev


TOOL = "play-pristine-with-inputs"
TOOL_VERSION = "1.5.0"
KNOWN_RETAIL_SHA256 = (
    "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
)
DISPLAY_RE = re.compile(r"^:[0-9]+$")
OUTPUT_RE = re.compile(r"^[1-9][0-9]*x[1-9][0-9]*$")
LEVEL_SELECT_MARKER = "--- Start LevelSelect ---"
NEXT_LIFE_MARKER = "NextLife."


class ControlError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProcessRecord:
    pid: int
    process_group: int
    command: tuple[str, ...]


@dataclass(frozen=True)
class GameTarget:
    display: str
    window_id: int
    pid: int
    process_group: int
    window_class: str
    width: int
    height: int

    def description(self) -> str:
        return (
            f"PID {self.pid} · window 0x{self.window_id:x} · "
            f"{self.display} · {self.width}×{self.height}"
        )


@dataclass(frozen=True)
class SessionConfig:
    root: Path
    game_dir: Path
    prefix: Path
    movie_dir: Path
    output: str | None
    filter_name: str | None
    research: bool
    mute: bool
    arm_delay: float
    anchor_timeout: float
    max_duration: float
    auto_coordinates: bool = False


def _proc_stat_process_group(raw: str) -> int:
    """Parse field 5 (process group) from one Linux /proc/PID/stat row."""

    close = raw.rfind(")")
    if close < 0:
        raise ValueError("malformed proc stat: missing command terminator")
    tail = raw[close + 1 :].split()
    if len(tail) < 3:
        raise ValueError("malformed proc stat: too few fields")
    return int(tail[2], 10)


def _process_records(proc_root: Path = Path("/proc")) -> tuple[ProcessRecord, ...]:
    records: list[ProcessRecord] = []
    try:
        entries = tuple(proc_root.iterdir())
    except OSError as exc:
        raise ControlError(f"cannot enumerate {proc_root}: {exc}") from exc
    for entry in entries:
        if not entry.name.isdigit():
            continue
        try:
            pid = int(entry.name, 10)
            group = _proc_stat_process_group(
                (entry / "stat").read_text(encoding="utf-8", errors="replace")
            )
            command = tuple(
                part.decode("utf-8", "replace")
                for part in (entry / "cmdline").read_bytes().split(b"\0")
                if part
            )
        except (OSError, ValueError):
            continue
        records.append(ProcessRecord(pid, group, command))
    return tuple(records)


def _nested_display(
    records: Iterable[ProcessRecord], process_group: int
) -> str | None:
    matches: set[str] = set()
    for record in records:
        if record.process_group != process_group or not record.command:
            continue
        executable = Path(record.command[0]).name.lower()
        if executable != "xwayland":
            continue
        for token in record.command[1:]:
            if DISPLAY_RE.fullmatch(token):
                matches.add(token)
                break
    if len(matches) > 1:
        raise ControlError(
            f"multiple nested X displays in owned process group: {sorted(matches)}"
        )
    return next(iter(matches), None)


class XDoProbe:
    def __init__(self, display: str, executable: str = "xdotool") -> None:
        self.display = display
        self.executable = executable

    def run(self, *args: str, allow_negative: bool = False) -> str:
        env = dict(os.environ)
        env["DISPLAY"] = self.display
        try:
            result = subprocess.run(
                [self.executable, *args],
                capture_output=True,
                text=True,
                timeout=3,
                check=False,
                env=env,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ControlError(f"xdotool failed: {exc}") from exc
        if result.returncode != 0:
            if allow_negative:
                return ""
            detail = (result.stderr or result.stdout).strip()
            raise ControlError(f"xdotool {' '.join(args)} failed: {detail}")
        return result.stdout.rstrip("\n")

    def search_game_windows(self) -> tuple[int, ...]:
        raw = self.run("search", "--class", "bugs.exe", allow_negative=True)
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
            raise ControlError(f"unparseable window PID: {raw!r}") from exc
        if value <= 0:
            raise ControlError(f"invalid window PID: {value}")
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
                    raise ControlError(f"unparseable geometry row: {line}") from exc
        if set(values) != {"WIDTH", "HEIGHT"}:
            raise ControlError("window geometry lacks WIDTH/HEIGHT")
        return values["WIDTH"], values["HEIGHT"]

    def stop_recording(self, window_id: int) -> None:
        # Separate down/up commands make the stop press visible even if the
        # recorder exits immediately after observing the key-down.
        self.run("keydown", "--window", str(window_id), "F12")
        self.run("keyup", "--window", str(window_id), "F12")


def discover_game_target(
    process_group: int,
    game_dir: Path,
    *,
    process_reader: Callable[[], tuple[ProcessRecord, ...]] = _process_records,
    probe_factory: Callable[[str], XDoProbe] = XDoProbe,
) -> GameTarget | None:
    records = process_reader()
    display = _nested_display(records, process_group)
    if display is None:
        return None
    probe = probe_factory(display)
    candidates: list[GameTarget] = []
    for window_id in probe.search_game_windows():
        try:
            pid = probe.window_pid(window_id)
            if os.getpgid(pid) != process_group:
                continue
            window_class = probe.window_class(window_id)
            if window_class.lower() != "bugs.exe":
                continue
            width, height = probe.geometry(window_id)
            if (width, height) != (640, 480):
                continue
            if Path(os.readlink(f"/proc/{pid}/cwd")).resolve() != game_dir:
                continue
            ev.ownership_proof(
                pid,
                expected_sha256=KNOWN_RETAIL_SHA256,
                cwd_prefix=str(game_dir) + os.sep,
            )
        except (ControlError, OSError, ev.OwnershipError):
            continue
        candidates.append(
            GameTarget(
                display=display,
                window_id=window_id,
                pid=pid,
                process_group=process_group,
                window_class=window_class,
                width=width,
                height=height,
            )
        )
    if len(candidates) > 1:
        raise ControlError(
            "multiple exact 640x480 bugs.exe windows in the owned session"
        )
    return candidates[0] if candidates else None


def stop_recording_exact(
    target: GameTarget,
    game_dir: Path,
    *,
    discoverer: Callable[[int, Path], GameTarget | None] = discover_game_target,
    probe_factory: Callable[[str], XDoProbe] = XDoProbe,
) -> None:
    """Send F12 only after re-proving the stored target identity."""

    current = discoverer(target.process_group, game_dir)
    if current != target:
        raise ControlError("game identity changed; refusing to send F12")
    probe_factory(target.display).stop_recording(target.window_id)


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def validate_movie_path(path: Path, copies_root: Path) -> Path:
    if not path.name or path.name in {".", ".."}:
        raise ControlError("movie filename is empty")
    try:
        resolved_parent = path.parent.resolve(strict=True)
        resolved_copies = copies_root.resolve(strict=True)
    except OSError as exc:
        raise ControlError(f"movie parent is unavailable: {exc}") from exc
    if not resolved_parent.is_dir() or not _inside(resolved_parent, resolved_copies):
        raise ControlError("movie must be inside work/copies/")
    normalized = resolved_parent / path.name
    if normalized.exists() or normalized.is_symlink():
        raise ControlError("movie already exists; choose a new filename")
    return normalized


def next_movie_path(movie_dir: Path, now: datetime | None = None) -> Path:
    stamp = (now or datetime.now().astimezone()).strftime("%Y%m%d-%H%M%S")
    base = movie_dir / f"input-{stamp}.input-movie.json"
    if not base.exists() and not base.is_symlink():
        return base
    for index in range(2, 1000):
        candidate = movie_dir / f"input-{stamp}-{index}.input-movie.json"
        if not candidate.exists() and not candidate.is_symlink():
            return candidate
    raise ControlError("could not allocate a unique movie filename")


def launcher_command(config: SessionConfig) -> list[str]:
    command = [
        str(config.root / "scripts" / "play-pristine.sh"),
        "--windowed",
        "--game-dir",
        str(config.game_dir),
        "--prefix",
        str(config.prefix),
    ]
    if config.output is not None:
        command.extend(["--output", config.output])
    if config.filter_name is not None:
        command.extend(["--filter", config.filter_name])
    if config.research:
        command.append("--research")
    if config.mute:
        command.append("--mute")
    return command


def record_command(
    config: SessionConfig,
    target: GameTarget,
    movie_path: Path,
    *,
    anchor_mode: str = "gameplay",
    status_fd: int | None = None,
) -> list[str]:
    command = [
        sys.executable,
        str(config.root / "scripts" / "input-movie.py"),
        "record",
        "--pid",
        str(target.pid),
        "--window-id",
        str(target.window_id),
        "--display",
        target.display,
        "--cwd-prefix",
        str(config.root / "work" / "copies") + os.sep,
        "--movie",
        str(movie_path),
        "--max-duration",
        str(config.max_duration),
    ]
    if anchor_mode in {"gameplay", "level-select"}:
        marker = (
            NEXT_LIFE_MARKER if anchor_mode == "gameplay" else LEVEL_SELECT_MARKER
        )
        command.extend(
            [
                "--start-milestone",
                marker,
                "--log",
                str(config.game_dir / "bugs.log"),
                "--anchor-timeout",
                str(config.anchor_timeout),
            ]
        )
    elif anchor_mode == "manual":
        command.extend(["--start-now", "--arm-delay", str(config.arm_delay)])
    else:
        raise ControlError(f"unsupported recording anchor: {anchor_mode}")
    if status_fd is not None:
        command.extend(["--status-fd", str(status_fd)])
    return command


def replay_command(
    config: SessionConfig,
    target: GameTarget,
    movie_path: Path,
    anchor_type: str,
    *,
    status_fd: int | None = None,
) -> list[str]:
    command = [
        sys.executable,
        str(config.root / "scripts" / "input-movie.py"),
        "replay",
        "--pid",
        str(target.pid),
        "--window-id",
        str(target.window_id),
        "--display",
        target.display,
        "--cwd-prefix",
        str(config.root / "work" / "copies") + os.sep,
        "--movie",
        str(movie_path),
        "--anchor-timeout",
        str(config.anchor_timeout),
    ]
    if anchor_type == "log-milestone":
        command.extend(["--log", str(config.game_dir / "bugs.log")])
    elif anchor_type == "manual-delay":
        command.extend(["--arm-delay", str(config.arm_delay)])
    else:
        raise ControlError(f"unsupported movie anchor: {anchor_type}")
    if status_fd is not None:
        command.extend(["--status-fd", str(status_fd)])
    return command


def coordinate_overlay_command(
    config: SessionConfig,
    target: GameTarget,
    *,
    mode: str = "overlay",
    opacity: float = 0.78,
    interval_ms: int = 100,
) -> list[str]:
    if mode not in {"overlay", "window"}:
        raise ControlError(f"unsupported coordinate display mode: {mode}")
    if not 0.2 <= opacity <= 1.0:
        raise ControlError("coordinate opacity must be between 0.2 and 1.0")
    if not 16 <= interval_ms <= 2000:
        raise ControlError("coordinate interval must be 16..2000 ms")
    return [
        sys.executable,
        str(config.root / "scripts" / "coordinate-overlay.py"),
        "--pid",
        str(target.pid),
        "--process-group",
        str(target.process_group),
        "--cwd-prefix",
        str(config.game_dir),
        "--mode",
        mode,
        "--opacity",
        str(opacity),
        "--interval-ms",
        str(interval_ms),
        "--display",
        target.display,
    ]


def validate_replay_movie(config: SessionConfig, movie_path: Path) -> dict:
    if not movie_path.is_file() or movie_path.is_symlink():
        raise ControlError("replay movie must be one regular non-link file")
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(config.root / "scripts" / "input-movie.py"),
                "validate",
                "--movie",
                str(movie_path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ControlError(f"movie validation failed: {exc}") from exc
    if result.returncode != 0:
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            payload = {}
        detail = payload.get("detail") or payload.get("reason") or result.stderr.strip()
        raise ControlError(f"movie validation refused: {detail or 'unknown error'}")
    try:
        raw = json.loads(movie_path.read_text(encoding="utf-8"))
        anchor = raw["anchor"]
        anchor_type = anchor["type"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ControlError(f"validated movie anchor is unreadable: {exc}") from exc
    return {
        "anchor_type": anchor_type,
        "marker": anchor.get("marker"),
        "validation": json.loads(result.stdout),
    }


def _process_group_members(process_group: int) -> tuple[ProcessRecord, ...]:
    return tuple(
        item for item in _process_records() if item.process_group == process_group
    )


def _wait_for_group_exit(
    process: subprocess.Popen, process_group: int, timeout: float
) -> bool:
    deadline = time.monotonic() + timeout
    while True:
        process.poll()
        if not _process_group_members(process_group):
            return True
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.05)


def _prove_isolated_group(process: subprocess.Popen) -> int:
    process_group = process.pid
    if process.poll() is None:
        try:
            observed = os.getpgid(process.pid)
        except OSError as exc:
            raise ControlError(f"cannot prove live process group: {exc}") from exc
        if observed != process_group:
            raise ControlError(
                f"refusing non-isolated process group {observed}; expected {process_group}"
            )
    return process_group


def terminate_session(process: subprocess.Popen, timeout: float = 5.0) -> None:
    process_group = _prove_isolated_group(process)
    if not _process_group_members(process_group):
        return
    try:
        os.killpg(process_group, signal.SIGTERM)
    except ProcessLookupError:
        return
    if _wait_for_group_exit(process, process_group, timeout):
        return
    try:
        os.killpg(process_group, signal.SIGKILL)
    except ProcessLookupError:
        return
    if not _wait_for_group_exit(process, process_group, timeout):
        members = [item.pid for item in _process_group_members(process_group)]
        raise ControlError(f"isolated launcher group did not terminate: {members}")


def interrupt_recorder(process: subprocess.Popen) -> None:
    process_group = _prove_isolated_group(process)
    if not _process_group_members(process_group):
        return
    for stop_signal, timeout in (
        (signal.SIGINT, 3.0),
        (signal.SIGTERM, 2.0),
        (signal.SIGKILL, 2.0),
    ):
        try:
            os.killpg(process_group, stop_signal)
        except ProcessLookupError:
            return
        if _wait_for_group_exit(process, process_group, timeout):
            return
    raise ControlError("isolated recorder did not terminate")


class RecorderWindow:
    def __init__(self, root, launcher: subprocess.Popen, config: SessionConfig) -> None:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk

        self.tk = tk
        self.ttk = ttk
        self.filedialog = filedialog
        self.messagebox = messagebox
        self.root = root
        self.launcher = launcher
        self.config = config
        self.target: GameTarget | None = None
        self.worker_target: GameTarget | None = None
        self.worker_process: subprocess.Popen | None = None
        self.worker_mode: str | None = None
        self.worker_movie: Path | None = None
        self.worker_status_fd: int | None = None
        self.worker_status_buffer = b""
        self.worker_started = False
        self.worker_cancel_requested = False
        self.coordinate_process: subprocess.Popen | None = None
        self.closing = False
        self.signal_requested = False
        self.session_process_group = launcher.pid

        root.title("ABLPC Input Recorder")
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", self.request_close)

        style = ttk.Style(root)
        style.configure("Recording.TLabel", foreground="#c62828", font=("Sans", 11, "bold"))
        style.configure("Replay.TLabel", foreground="#1565c0", font=("Sans", 11, "bold"))

        self.status_text = tk.StringVar(value="Waiting for the PC game window…")
        self.target_text = tk.StringVar(value="Game target: discovering")
        self.movie_text = tk.StringVar(value=str(next_movie_path(config.movie_dir)))
        self.last_saved_text = tk.StringVar(value="Last saved: none this session")
        self.anchor_mode = tk.StringVar(value="gameplay")

        menu = tk.Menu(root)
        recording_menu = tk.Menu(menu, tearoff=False)
        recording_menu.add_command(
            label="Start Recording", command=self.start_recording, accelerator="Ctrl+R"
        )
        recording_menu.add_command(
            label="Stop Current Operation", command=self.stop_active, accelerator="F12"
        )
        recording_menu.add_separator()
        recording_menu.add_command(label="Choose Next Output…", command=self.choose_movie)
        menu.add_cascade(label="Recording", menu=recording_menu)
        replay_menu = tk.Menu(menu, tearoff=False)
        replay_menu.add_command(
            label="Replay Movie…", command=self.replay_movie, accelerator="Ctrl+P"
        )
        replay_menu.add_command(label="Stop Replay", command=self.stop_active)
        menu.add_cascade(label="Replay", menu=replay_menu)
        view_menu = tk.Menu(menu, tearoff=False)
        view_menu.add_command(
            label="Show Coordinate Overlay", command=self.toggle_coordinate_overlay
        )
        menu.add_cascade(label="View", menu=view_menu)
        session_menu = tk.Menu(menu, tearoff=False)
        session_menu.add_command(label="Close Game and Controls", command=self.request_close)
        menu.add_cascade(label="Session", menu=session_menu)
        root.configure(menu=menu)

        frame = ttk.Frame(root, padding=14)
        frame.grid(row=0, column=0, sticky="nsew")
        ttk.Label(frame, text="PC input movie", font=("Sans", 14, "bold")).grid(
            row=0, column=0, columnspan=4, sticky="w"
        )
        ttk.Label(frame, textvariable=self.target_text).grid(
            row=1, column=0, columnspan=4, sticky="w", pady=(7, 2)
        )
        self.status_label = ttk.Label(
            frame, textvariable=self.status_text, wraplength=650
        )
        self.status_label.grid(
            row=2, column=0, columnspan=4, sticky="w", pady=(0, 10)
        )

        ttk.Label(frame, text="Recording anchor:").grid(row=3, column=0, sticky="w")
        self.gameplay_anchor_button = ttk.Radiobutton(
            frame,
            text="Gameplay / NextLife (recommended)",
            variable=self.anchor_mode,
            value="gameplay",
        )
        self.gameplay_anchor_button.grid(row=3, column=1, sticky="w")
        self.level_anchor_button = ttk.Radiobutton(
            frame,
            text="Level Select (menu only)",
            variable=self.anchor_mode,
            value="level-select",
        )
        self.level_anchor_button.grid(row=3, column=2, sticky="w")
        self.manual_anchor_button = ttk.Radiobutton(
            frame,
            text=f"Manual delay ({config.arm_delay:g} s; weaker)",
            variable=self.anchor_mode,
            value="manual",
        )
        self.manual_anchor_button.grid(row=3, column=3, sticky="w")

        ttk.Label(frame, text="Next recording output:").grid(
            row=4, column=0, columnspan=4, sticky="w", pady=(9, 0)
        )
        self.movie_entry = ttk.Entry(frame, textvariable=self.movie_text, width=74)
        self.movie_entry.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(2, 5))
        self.choose_button = ttk.Button(
            frame, text="Choose…", command=self.choose_movie
        )
        self.choose_button.grid(row=5, column=3, padx=(8, 0), pady=(2, 5))
        ttk.Label(frame, textvariable=self.last_saved_text, wraplength=650).grid(
            row=6, column=0, columnspan=4, sticky="w", pady=(0, 10)
        )

        self.start_button = ttk.Button(
            frame, text="Start Recording", command=self.start_recording, state="disabled"
        )
        self.start_button.grid(row=7, column=0, sticky="ew")
        self.stop_button = ttk.Button(
            frame, text="Stop", command=self.stop_active, state="disabled"
        )
        self.stop_button.grid(row=7, column=1, sticky="ew", padx=(8, 0))
        self.replay_button = ttk.Button(
            frame, text="Replay Movie…", command=self.replay_movie, state="disabled"
        )
        self.replay_button.grid(row=7, column=2, sticky="ew", padx=(8, 0))
        ttk.Button(frame, text="Close Session", command=self.request_close).grid(
            row=7, column=3, sticky="ew", padx=(8, 0)
        )
        self.coordinate_button = ttk.Button(
            frame,
            text="Show Coordinate Overlay",
            command=self.toggle_coordinate_overlay,
            state="disabled",
        )
        self.coordinate_button.grid(
            row=8, column=0, columnspan=2, sticky="ew", pady=(9, 0)
        )
        ttk.Label(
            frame,
            text=(
                "Recommended: click Start before selecting Hardware. Setup keys are ignored; "
                "select Training, then begin the route only when RECORDING NOW appears. "
                "F12 stops recording. Coordinates are read-only and may remain visible "
                "during recording or manual play."
            ),
            wraplength=650,
        ).grid(row=9, column=0, columnspan=4, sticky="w", pady=(12, 0))

        root.bind("<Control-r>", lambda _event: self.start_recording())
        root.bind("<Control-p>", lambda _event: self.replay_movie())
        root.bind("<F12>", lambda _event: self.stop_active())
        self.poll()

    def _set_status(self, text: str, active: str | None = None) -> None:
        self.status_text.set(text)
        style = "TLabel"
        if active == "record":
            style = "Recording.TLabel"
        elif active == "replay":
            style = "Replay.TLabel"
        self.status_label.configure(style=style)

    def _set_controls(self, active: bool) -> None:
        idle_state = "disabled" if active or self.target is None else "normal"
        self.start_button.configure(state=idle_state)
        self.replay_button.configure(state=idle_state)
        self.choose_button.configure(state="disabled" if active else "normal")
        self.movie_entry.configure(state="disabled" if active else "normal")
        self.gameplay_anchor_button.configure(state="disabled" if active else "normal")
        self.level_anchor_button.configure(state="disabled" if active else "normal")
        self.manual_anchor_button.configure(state="disabled" if active else "normal")
        self.stop_button.configure(state="normal" if active else "disabled")
        self._refresh_coordinate_button()

    def _refresh_coordinate_button(self) -> None:
        active = (
            self.coordinate_process is not None
            and self.coordinate_process.poll() is None
        )
        self.coordinate_button.configure(
            text="Hide Coordinate Overlay" if active else "Show Coordinate Overlay",
            state="normal" if active or self.target is not None else "disabled",
        )

    def _stop_coordinate_overlay(self) -> bool:
        process = self.coordinate_process
        if process is None:
            return True
        if process.poll() is None:
            try:
                interrupt_recorder(process)
            except ControlError as exc:
                self._set_status(str(exc))
                return False
        self.coordinate_process = None
        self._refresh_coordinate_button()
        return True

    def toggle_coordinate_overlay(self) -> None:
        if self.coordinate_process is not None:
            if self.coordinate_process.poll() is None:
                self._stop_coordinate_overlay()
                return
            self.coordinate_process = None
        try:
            target = self._verified_target()
            command = coordinate_overlay_command(self.config, target)
            self.coordinate_process = subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                start_new_session=True,
            )
        except (ControlError, OSError) as exc:
            self.coordinate_process = None
            self._set_status(f"Coordinate overlay was not started: {exc}")
            self.messagebox.showerror("Coordinate overlay", str(exc))
            self._refresh_coordinate_button()
            return
        self._set_status(
            "Coordinate overlay active. Drag with the left button; double-click toggles "
            "window chrome; right-click or Escape closes only the overlay."
        )
        self._refresh_coordinate_button()

    def _verified_target(self) -> GameTarget:
        if self.target is None:
            raise ControlError("the exact 640x480 PC game window is not ready")
        target = discover_game_target(self.session_process_group, self.config.game_dir)
        if target is None or target != self.target:
            raise ControlError("game identity changed; wait for rediscovery")
        return target

    def _marker_already_seen(self, marker: str) -> bool:
        log_path = self.config.game_dir / "bugs.log"
        try:
            return marker.encode("utf-8") in log_path.read_bytes()
        except OSError as exc:
            raise ControlError(f"fresh bugs.log is unavailable: {exc}") from exc

    def choose_movie(self) -> None:
        if self.worker_process is not None:
            return
        selected = self.filedialog.asksaveasfilename(
            title="Save PC input movie",
            initialdir=str(self.config.movie_dir),
            initialfile=Path(self.movie_text.get()).name,
            defaultextension=".json",
            filetypes=(("Input movie JSON", "*.json"), ("All files", "*")),
        )
        if selected:
            self.movie_text.set(selected)

    def _start_worker(
        self,
        command_builder: Callable[[int], list[str]],
        *,
        mode: str,
        target: GameTarget,
        movie_path: Path,
    ) -> None:
        read_fd, write_fd = os.pipe()
        try:
            os.set_blocking(read_fd, False)
            command = command_builder(write_fd)
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
                pass_fds=(write_fd,),
            )
        except (OSError, ControlError):
            os.close(read_fd)
            raise
        finally:
            os.close(write_fd)
        self.worker_target = target
        self.worker_process = process
        self.worker_mode = mode
        self.worker_movie = movie_path
        self.worker_status_fd = read_fd
        self.worker_status_buffer = b""
        self.worker_started = False
        self.worker_cancel_requested = False
        self._set_controls(True)
        self._set_status(f"Starting {mode} worker; wait for ARMED…")

    def start_recording(self) -> None:
        if self.worker_process is not None:
            return
        try:
            movie_path = validate_movie_path(
                Path(self.movie_text.get()), self.config.root / "work" / "copies"
            )
            target = self._verified_target()
            anchor_mode = self.anchor_mode.get()
            if anchor_mode in {"gameplay", "level-select"}:
                if not self.config.research:
                    raise ControlError("log-milestone anchoring requires --research")
                marker = (
                    NEXT_LIFE_MARKER
                    if anchor_mode == "gameplay"
                    else LEVEL_SELECT_MARKER
                )
                if self._marker_already_seen(marker):
                    raise ControlError(
                        f"{marker} already occurred; restart this companion session "
                        "and click Start before reaching that milestone"
                    )
            self._start_worker(
                lambda status_fd: record_command(
                    self.config,
                    target,
                    movie_path,
                    anchor_mode=anchor_mode,
                    status_fd=status_fd,
                ),
                mode="record",
                target=target,
                movie_path=movie_path,
            )
        except (ControlError, OSError) as exc:
            self.messagebox.showerror("Recording refused", str(exc))

    def replay_movie(self) -> None:
        if self.worker_process is not None:
            return
        selected = self.filedialog.askopenfilename(
            title="Replay PC input movie",
            initialdir=str(self.config.movie_dir),
            filetypes=(("Input movie JSON", "*.json"), ("All files", "*")),
        )
        if not selected:
            return
        movie_path = Path(selected).absolute()
        try:
            target = self._verified_target()
            info = validate_replay_movie(self.config, movie_path)
            anchor_type = info["anchor_type"]
            if anchor_type == "log-milestone":
                marker = info["marker"]
                if not self.config.research:
                    raise ControlError("log-anchored replay requires --research")
                if not isinstance(marker, str) or not marker:
                    raise ControlError("validated movie has no usable log marker")
                if self._marker_already_seen(marker):
                    raise ControlError(
                        "the movie's anchor already occurred; restart this companion "
                        "session and choose Replay before selecting Hardware"
                    )
            elif not self.messagebox.askyesno(
                "Manual-delay replay",
                "This movie has no game-state marker. Replay can dispatch every input "
                "but may reach different menus or gameplay. Replay anyway?",
            ):
                return
            self._start_worker(
                lambda status_fd: replay_command(
                    self.config,
                    target,
                    movie_path,
                    anchor_type,
                    status_fd=status_fd,
                ),
                mode="replay",
                target=target,
                movie_path=movie_path,
            )
        except (ControlError, OSError) as exc:
            self.messagebox.showerror("Replay refused", str(exc))

    def _interrupt_worker_signal(self) -> None:
        if self.worker_process is None:
            return
        process_group = _prove_isolated_group(self.worker_process)
        if not _process_group_members(process_group):
            return
        try:
            os.killpg(process_group, signal.SIGINT)
        except ProcessLookupError:
            return

    def stop_active(self) -> None:
        if self.worker_process is None or self.worker_target is None:
            return
        if self.worker_mode == "record" and self.worker_started:
            try:
                stop_recording_exact(self.worker_target, self.config.game_dir)
                self._set_status("Stopping after exact-window F12…")
                return
            except ControlError as exc:
                self._set_status(f"F12 stop failed; interrupting safely: {exc}")
        try:
            self._interrupt_worker_signal()
            self.worker_cancel_requested = True
            self._set_status(f"Stopping {self.worker_mode} safely…")
        except ControlError as exc:
            self._set_status(f"Could not stop the isolated worker: {exc}")

    def _handle_worker_status(self, payload: dict) -> None:
        event = payload.get("event")
        mode = payload.get("mode")
        anchor_type = payload.get("anchor_type")
        if event == "armed" and mode == "record":
            if anchor_type == "log-milestone":
                if payload.get("marker") == NEXT_LIFE_MARKER:
                    self._set_status(
                        "ARMED — click the game, select Hardware, then Training. "
                        "Wait for RECORDING NOW before moving Flik."
                    )
                else:
                    self._set_status(
                        "ARMED — click the game and select Hardware. Wait for "
                        "RECORDING NOW before navigating Level Select."
                    )
            else:
                delay = payload.get("arm_delay_ms", 0) / 1000
                self._set_status(
                    f"ARMED — click the game. Do not play until RECORDING NOW "
                    f"(at least {delay:g} seconds and focused)."
                )
        elif event == "recording-started":
            self.worker_started = True
            self._set_status("● RECORDING NOW — play. F12 stops and saves.", "record")
        elif event == "armed" and mode == "replay":
            if anchor_type == "log-milestone":
                if payload.get("marker") == NEXT_LIFE_MARKER:
                    self._set_status(
                        "REPLAY ARMED — click the game, select Hardware, then Training. "
                        "Recorded gameplay begins automatically at NextLife."
                    )
                else:
                    self._set_status(
                        "REPLAY ARMED — click the game and select Hardware. Recorded "
                        "inputs begin automatically at the movie's log marker."
                    )
            else:
                delay = payload.get("arm_delay_ms", 0) / 1000
                self._set_status(
                    f"REPLAY ARMED — keep the game focused; inputs begin after "
                    f"{delay:g} seconds."
                )
        elif event == "replay-started":
            self.worker_started = True
            self._set_status("▶ REPLAYING NOW — do not press game keys.", "replay")

    def _drain_worker_status(self) -> None:
        descriptor = self.worker_status_fd
        if descriptor is None:
            return
        while True:
            try:
                chunk = os.read(descriptor, 4096)
            except BlockingIOError:
                break
            except OSError:
                chunk = b""
            if not chunk:
                os.close(descriptor)
                self.worker_status_fd = None
                break
            self.worker_status_buffer += chunk
            while b"\n" in self.worker_status_buffer:
                line, self.worker_status_buffer = self.worker_status_buffer.split(b"\n", 1)
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(payload, dict):
                    self._handle_worker_status(payload)

    def _worker_finished(self) -> None:
        assert self.worker_process is not None
        process = self.worker_process
        mode = self.worker_mode
        cancel_requested = self.worker_cancel_requested
        self._drain_worker_status()
        stdout, stderr = process.communicate()
        returncode = process.returncode
        if self.worker_status_fd is not None:
            os.close(self.worker_status_fd)
        self.worker_status_fd = None
        self.worker_status_buffer = b""
        self.worker_process = None
        self.worker_target = None
        self.worker_mode = None
        self.worker_started = False
        self.worker_cancel_requested = False
        self._set_controls(False)
        try:
            payload = json.loads(stdout.strip().splitlines()[-1]) if stdout.strip() else {}
        except (json.JSONDecodeError, IndexError):
            payload = {}
        if cancel_requested:
            if mode == "record":
                self._set_status("Recording canceled before save; no movie was created.")
            else:
                self._set_status("Replay stopped.")
        elif returncode == 0 and payload.get("accepted") is True and mode == "record":
            saved = payload.get("movie", str(self.worker_movie or ""))
            count = payload.get("event_count", "?")
            self.last_saved_text.set(f"Last saved: {saved}")
            self.movie_text.set(str(next_movie_path(self.config.movie_dir)))
            self._set_status(f"Saved {count} events. Last saved path is shown below.")
        elif returncode == 0 and payload.get("accepted") is True and mode == "replay":
            count = payload.get("events_dispatched", "?")
            run_id = payload.get("run_id", "unknown run")
            self._set_status(
                f"Replay dispatched {count} events ({run_id}). Verify the gameplay outcome."
            )
        else:
            reason = payload.get("reason") or payload.get("failure") or stderr.strip()
            if isinstance(reason, dict):
                reason = reason.get("reason") or json.dumps(reason, sort_keys=True)
            self._set_status(
                f"{(mode or 'worker').capitalize()} was not accepted: "
                f"{reason or 'unknown error'}"
            )
            self.messagebox.showerror(
                f"{(mode or 'Worker').capitalize()} not accepted",
                str(reason or "Worker exited without an acceptance receipt"),
            )
        self.worker_movie = None

    def _interrupt_worker(self) -> bool:
        if self.worker_process is None:
            return True
        try:
            interrupt_recorder(self.worker_process)
            return True
        except ControlError as exc:
            self._set_status(str(exc))
            return False

    def _close_session(self, *, confirm: bool) -> None:
        if self.closing:
            return
        if confirm and not self.messagebox.askyesno(
            "Close session",
            "Close the pristine game, stop any recording/replay, and close controls?",
        ):
            return
        self.closing = True
        if not self._interrupt_worker():
            self.closing = False
            if confirm:
                self.messagebox.showerror(
                    "Session cleanup refused", "The isolated input worker is still active."
                )
            return
        if not self._stop_coordinate_overlay():
            self.closing = False
            if confirm:
                self.messagebox.showerror(
                    "Session cleanup refused",
                    "The isolated coordinate overlay is still active.",
                )
            return
        try:
            terminate_session(self.launcher)
        except ControlError as exc:
            self.closing = False
            if confirm:
                self.messagebox.showerror("Session cleanup refused", str(exc))
            return
        self.root.destroy()

    def request_close(self) -> None:
        self._close_session(confirm=True)

    def poll(self) -> None:
        if self.closing:
            return
        if self.signal_requested:
            self._close_session(confirm=False)
            return
        if self.launcher.poll() is not None:
            self._interrupt_worker()
            self._stop_coordinate_overlay()
            try:
                terminate_session(self.launcher)
            except ControlError as exc:
                self._set_status(str(exc))
                self.root.after(500, self.poll)
                return
            self.root.destroy()
            return
        if (
            self.coordinate_process is not None
            and self.coordinate_process.poll() is not None
        ):
            self.coordinate_process = None
            self._refresh_coordinate_button()
        if self.worker_process is not None:
            self._drain_worker_status()
            if self.worker_process.poll() is not None:
                self._worker_finished()
            else:
                self.root.after(100, self.poll)
                return
        previous = self.target
        try:
            target = discover_game_target(
                self.session_process_group, self.config.game_dir
            )
            self.target = target
            if target is None:
                self.target_text.set("Game target: waiting for the 640×480 window")
                if previous is not None:
                    self._set_status("Waiting for the PC game window…")
                self._set_controls(False)
            else:
                self.target_text.set(f"Game target: {target.description()}")
                if previous != target:
                    self._set_status(
                        "Ready. Start or choose Replay before selecting Hardware."
                    )
                self._set_controls(False)
                if (
                    previous != target
                    and self.config.auto_coordinates
                    and self.coordinate_process is None
                ):
                    self.toggle_coordinate_overlay()
        except ControlError as exc:
            self.target = None
            self.target_text.set("Game target: discovery refused")
            self._set_status(str(exc))
            self._set_controls(False)
        self.root.after(500, self.poll)


def _positive_float(text: str) -> float:
    try:
        value = float(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a number") from exc
    if not (0 < value <= 3600):
        raise argparse.ArgumentTypeError("value must be greater than 0 and at most 3600")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Launch the pinned pristine PC game window with a companion input "
            "recording and replay menu."
        )
    )
    parser.add_argument("--game-dir", help="derived PC/BUGS work copy")
    parser.add_argument("--prefix", help="Wine prefix (default: work/wine/baseline)")
    parser.add_argument(
        "--movie-dir",
        help="new movie destination directory (default: work/copies/input-movies)",
    )
    parser.add_argument(
        "--output", type=str, help="window size WIDTHxHEIGHT (default: 1280x960)"
    )
    parser.add_argument(
        "--filter", choices=("nearest", "linear"), help="Gamescope scaling filter"
    )
    parser.add_argument("--research", action="store_true", help="enable log/cheat args")
    parser.add_argument("--mute", action="store_true", help="use a private null sink")
    parser.add_argument(
        "--windowed",
        action="store_true",
        help="accepted for command compatibility; this wrapper is always windowed",
    )
    parser.add_argument(
        "--arm-delay",
        type=_positive_float,
        default=3.0,
        help="delay for the explicit manual-anchor fallback (default: 3 seconds)",
    )
    parser.add_argument(
        "--anchor-timeout",
        type=_positive_float,
        default=120.0,
        help="Level Select marker wait ceiling in seconds (default: 120)",
    )
    parser.add_argument(
        "--max-duration",
        type=_positive_float,
        default=900.0,
        help="recording ceiling in seconds (default: 900)",
    )
    parser.add_argument("--dry-run", action="store_true", help="print launch plan only")
    parser.add_argument(
        "--capabilities", action="store_true", help="print machine-readable scope"
    )
    parser.add_argument(
        "--coordinates",
        action="store_true",
        help="open the read-only translucent coordinate overlay when the game appears",
    )
    return parser


def _config(args: argparse.Namespace) -> SessionConfig:
    root = ev.repo_root().resolve()
    copies = (root / "work" / "copies").resolve()
    game_dir = Path(args.game_dir or copies / "BUGS_PC-full-disc" / "PC" / "BUGS")
    prefix = Path(args.prefix or root / "work" / "wine" / "baseline")
    movie_dir = Path(args.movie_dir or copies / "input-movies")
    game_dir = game_dir.resolve()
    prefix = prefix.resolve()
    movie_dir = movie_dir.resolve(strict=False)
    if not _inside(game_dir, copies):
        raise ControlError("game directory must be inside work/copies/")
    if not _inside(movie_dir, copies):
        raise ControlError("movie directory must be inside work/copies/")
    if args.output is not None and not OUTPUT_RE.fullmatch(args.output):
        raise ControlError("output must be WIDTHxHEIGHT with positive integers")
    return SessionConfig(
        root=root,
        game_dir=game_dir,
        prefix=prefix,
        movie_dir=movie_dir,
        output=args.output,
        filter_name=args.filter,
        research=args.research,
        mute=args.mute,
        arm_delay=args.arm_delay,
        anchor_timeout=args.anchor_timeout,
        max_duration=args.max_duration,
        auto_coordinates=args.coordinates,
    )


def capabilities() -> dict:
    return {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "interface": "Tk companion window with Recording, Replay, and Session menus",
        "launcher": "unchanged scripts/play-pristine.sh",
        "always_windowed": True,
        "automatic_target_discovery": True,
        "record_backend": "scripts/input-movie.py exact-window XSelectInput",
        "replay_backend": (
            "scripts/input-movie.py persistent X11/XTEST with exact-window echo"
        ),
        "coordinate_display": {
            "worker": "scripts/coordinate-overlay.py",
            "backend": "read-only process_vm_readv",
            "default_mode": "live Flik X/Y/Z overlay inside the owned Gamescope display",
            "ordinary_window_fallback": True,
            "automatic_cli_flag": "--coordinates",
        },
        "target_echo_required": True,
        "default_record_anchor": {
            "type": "log-milestone",
            "marker": NEXT_LIFE_MARKER,
        },
        "record_anchor_choices": {
            "gameplay": NEXT_LIFE_MARKER,
            "menu_only": LEVEL_SELECT_MARKER,
            "fallback": "manual-delay",
        },
        "manual_delay_available": True,
        "supervisor_status_events": [
            "armed",
            "recording-started",
            "replay-started",
        ],
        "stop_action": {
            "active_recording": "F12 to discovered exact game window only",
            "armed_recording_or_replay": "SIGINT to isolated worker process group",
        },
        "host_input_capture": False,
        "display_wide_capture": False,
        "internal_game_frame_synchronization": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.capabilities:
        print(json.dumps(capabilities(), indent=2, sort_keys=True))
        return 0
    try:
        config = _config(args)
    except ControlError as exc:
        print(json.dumps({"refused": True, "tool": TOOL, "reason": str(exc)}))
        return 3
    command = launcher_command(config)
    if args.dry_run:
        print(
            json.dumps(
                {
                    "tool": TOOL,
                    "launcher_command": command,
                    "movie_dir": str(config.movie_dir),
                    "always_windowed": True,
                    "auto_coordinates": config.auto_coordinates,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if not config.game_dir.is_dir():
        print(f"Game directory is missing: {config.game_dir}", file=sys.stderr)
        return 3
    if not config.prefix.is_dir():
        print(f"Wine prefix is missing: {config.prefix}", file=sys.stderr)
        return 3
    try:
        config.movie_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"Cannot create movie directory: {exc}", file=sys.stderr)
        return 3
    if not _inside(config.movie_dir, (config.root / "work" / "copies").resolve()):
        print("Movie directory escaped work/copies/", file=sys.stderr)
        return 3
    for executable in ("gamescope", "wine", "xdotool"):
        if not shutil.which(executable):
            print(f"Required executable is missing: {executable}", file=sys.stderr)
            return 3
    try:
        launcher = subprocess.Popen(command, start_new_session=True)
    except OSError as exc:
        print(f"Could not launch pristine session: {exc}", file=sys.stderr)
        return 3
    app: RecorderWindow | None = None
    received_signal: list[int] = []
    previous_handlers: dict[int, object] = {}
    try:
        import tkinter as tk

        root = tk.Tk()
        app = RecorderWindow(root, launcher, config)

        def request_shutdown(signum: int, _frame: object) -> None:
            received_signal.append(signum)
            app.signal_requested = True

        for signum in (signal.SIGINT, signal.SIGTERM):
            previous_handlers[signum] = signal.getsignal(signum)
            signal.signal(signum, request_shutdown)
        root.mainloop()
    except KeyboardInterrupt:
        if app is not None:
            try:
                app._close_session(confirm=False)
            except (ControlError, OSError):
                pass
        try:
            terminate_session(launcher)
        except (ControlError, OSError):
            pass
        return 130
    except Exception as exc:
        if app is not None:
            try:
                app._interrupt_worker()
            except (ControlError, OSError):
                pass
            try:
                app._stop_coordinate_overlay()
            except (ControlError, OSError):
                pass
        try:
            terminate_session(launcher)
        except (ControlError, OSError):
            pass
        print(f"Input controls failed: {exc}", file=sys.stderr)
        return 3
    finally:
        for signum, previous in previous_handlers.items():
            signal.signal(signum, previous)
    assert app is not None
    if received_signal:
        return 128 + received_signal[-1]
    if app.closing:
        return 0
    return launcher.returncode if launcher.returncode is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
