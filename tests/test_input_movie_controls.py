from __future__ import annotations

from datetime import datetime
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "play-pristine-with-inputs.py"
PYTHON = ROOT / ".venv" / "bin" / "python"


def _load_module():
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location("ablpc_input_controls", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


controls = _load_module()


def _config(tmp_path: Path):
    root = tmp_path / "repo"
    game = root / "work" / "copies" / "game" / "PC" / "BUGS"
    prefix = root / "work" / "wine" / "baseline"
    movies = root / "work" / "copies" / "input-movies"
    game.mkdir(parents=True)
    prefix.mkdir(parents=True)
    movies.mkdir(parents=True)
    return controls.SessionConfig(
        root=root,
        game_dir=game,
        prefix=prefix,
        movie_dir=movies,
        output=None,
        filter_name=None,
        research=True,
        mute=True,
        arm_delay=3.0,
        anchor_timeout=120.0,
        max_duration=900.0,
    )


def test_capabilities_declare_companion_scope_without_host_capture() -> None:
    result = subprocess.run(
        [str(PYTHON), str(SCRIPT), "--capabilities"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["launcher"] == "unchanged scripts/play-pristine.sh"
    assert payload["always_windowed"] is True
    assert payload["automatic_target_discovery"] is True
    assert payload["default_record_anchor"] == {
        "type": "log-milestone",
        "marker": controls.NEXT_LIFE_MARKER,
    }
    assert payload["record_anchor_choices"] == {
        "gameplay": controls.NEXT_LIFE_MARKER,
        "menu_only": controls.LEVEL_SELECT_MARKER,
        "fallback": "manual-delay",
    }
    assert payload["manual_delay_available"] is True
    assert payload["supervisor_status_events"] == [
        "armed",
        "recording-started",
        "replay-started",
    ]
    assert payload["coordinate_display"] == {
        "worker": "scripts/coordinate-overlay.py",
        "backend": "read-only process_vm_readv",
        "default_mode": "live Flik X/Y/Z overlay inside the owned Gamescope display",
        "ordinary_window_fallback": True,
        "automatic_cli_flag": "--coordinates",
    }
    assert payload["host_input_capture"] is False
    assert payload["display_wide_capture"] is False
    assert payload["internal_game_frame_synchronization"] is False


def test_proc_stat_parser_handles_spaces_and_parentheses_in_command() -> None:
    raw = "123 (odd name) here) S 1 456 456 0 -1 0 0 0 0"
    assert controls._proc_stat_process_group(raw) == 456
    with pytest.raises(ValueError, match="malformed"):
        controls._proc_stat_process_group("123 malformed")


def test_nested_display_is_scoped_to_one_owned_process_group() -> None:
    records = (
        controls.ProcessRecord(10, 500, ("/usr/bin/Xwayland", ":0", "-rootless")),
        controls.ProcessRecord(11, 700, ("Xwayland", ":2", "-terminate")),
        controls.ProcessRecord(12, 700, ("gamescope", "--backend", "wayland")),
    )
    assert controls._nested_display(records, 700) == ":2"
    assert controls._nested_display(records, 800) is None

    ambiguous = records + (
        controls.ProcessRecord(13, 700, ("Xwayland", ":3", "-terminate")),
    )
    with pytest.raises(controls.ControlError, match="multiple nested X displays"):
        controls._nested_display(ambiguous, 700)


def test_launcher_command_keeps_pinned_launcher_and_forces_windowed(tmp_path: Path) -> None:
    config = _config(tmp_path)
    command = controls.launcher_command(config)
    assert command[0] == str(config.root / "scripts" / "play-pristine.sh")
    assert command.count("--windowed") == 1
    assert command[-2:] == ["--research", "--mute"]
    assert "--game-dir" in command and str(config.game_dir) in command
    assert "--prefix" in command and str(config.prefix) in command


def test_record_and_replay_commands_use_explicit_movie_anchor(tmp_path: Path) -> None:
    config = _config(tmp_path)
    movie = config.movie_dir / "route.json"
    target = controls.GameTarget(":2", 99, 1234, 900, "bugs.exe", 640, 480)
    command = controls.record_command(config, target, movie, status_fd=8)
    assert command[:3] == [
        sys.executable,
        str(config.root / "scripts" / "input-movie.py"),
        "record",
    ]
    assert command[command.index("--pid") + 1] == "1234"
    assert command[command.index("--window-id") + 1] == "99"
    assert command[command.index("--display") + 1] == ":2"
    assert command[command.index("--movie") + 1] == str(movie)
    assert command[command.index("--start-milestone") + 1] == controls.NEXT_LIFE_MARKER
    assert command[command.index("--log") + 1] == str(config.game_dir / "bugs.log")
    assert command[command.index("--anchor-timeout") + 1] == "120.0"
    assert command[command.index("--status-fd") + 1] == "8"
    assert "--start-now" not in command

    menu = controls.record_command(
        config, target, movie, anchor_mode="level-select"
    )
    assert menu[menu.index("--start-milestone") + 1] == controls.LEVEL_SELECT_MARKER
    assert "--start-now" not in menu

    manual = controls.record_command(
        config, target, movie, anchor_mode="manual"
    )
    assert manual[manual.index("--arm-delay") + 1] == "3.0"
    assert "--start-now" in manual
    assert "--start-milestone" not in manual

    replay = controls.replay_command(
        config, target, movie, "log-milestone", status_fd=9
    )
    assert replay[2] == "replay"
    assert replay[replay.index("--log") + 1] == str(config.game_dir / "bugs.log")
    assert replay[replay.index("--status-fd") + 1] == "9"
    assert "--arm-delay" not in replay

    replay_manual = controls.replay_command(
        config, target, movie, "manual-delay"
    )
    assert replay_manual[replay_manual.index("--arm-delay") + 1] == "3.0"
    assert "--log" not in replay_manual

    overlay = controls.coordinate_overlay_command(config, target)
    assert overlay[:2] == [
        sys.executable,
        str(config.root / "scripts" / "coordinate-overlay.py"),
    ]
    assert overlay[overlay.index("--pid") + 1] == "1234"
    assert overlay[overlay.index("--process-group") + 1] == "900"
    assert overlay[overlay.index("--cwd-prefix") + 1] == str(config.game_dir)
    assert overlay[overlay.index("--mode") + 1] == "overlay"
    assert overlay[overlay.index("--opacity") + 1] == "0.78"
    assert overlay[overlay.index("--interval-ms") + 1] == "100"
    assert overlay[overlay.index("--display") + 1] == ":2"

    with pytest.raises(controls.ControlError, match="unsupported"):
        controls.coordinate_overlay_command(config, target, mode="unknown")


def test_movie_path_is_create_only_and_confined_to_work_copies(tmp_path: Path) -> None:
    config = _config(tmp_path)
    wanted = config.movie_dir / "route.json"
    assert controls.validate_movie_path(
        wanted, config.root / "work" / "copies"
    ) == wanted

    wanted.write_text("existing", encoding="utf-8")
    with pytest.raises(controls.ControlError, match="already exists"):
        controls.validate_movie_path(wanted, config.root / "work" / "copies")

    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(controls.ControlError, match="inside work/copies"):
        controls.validate_movie_path(
            outside / "route.json", config.root / "work" / "copies"
        )

    linked = config.movie_dir / "linked.json"
    linked.symlink_to(wanted)
    with pytest.raises(controls.ControlError, match="already exists"):
        controls.validate_movie_path(linked, config.root / "work" / "copies")


def test_next_movie_path_never_overwrites_same_second(tmp_path: Path) -> None:
    movie_dir = tmp_path / "movies"
    movie_dir.mkdir()
    now = datetime(2026, 8, 15, 13, 45, 6)
    first = controls.next_movie_path(movie_dir, now)
    assert first.name == "input-20260815-134506.input-movie.json"
    first.write_text("one", encoding="utf-8")
    second = controls.next_movie_path(movie_dir, now)
    assert second.name == "input-20260815-134506-2.input-movie.json"


class _Probe:
    def __init__(self, display: str, *, two_exact: bool = False) -> None:
        self.display = display
        self.two_exact = two_exact

    def search_game_windows(self) -> tuple[int, ...]:
        return (10, 20, 30) if self.two_exact else (10, 20)

    def window_pid(self, window_id: int) -> int:
        return 5000 + window_id

    def window_class(self, window_id: int) -> str:
        return "bugs.exe"

    def geometry(self, window_id: int) -> tuple[int, int]:
        return (1, 1) if window_id == 10 else (640, 480)


def test_discovery_ignores_ime_surface_and_selects_one_exact_game(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = _config(tmp_path)
    group = 800
    records = (
        controls.ProcessRecord(77, group, ("Xwayland", ":4", "-terminate")),
    )
    monkeypatch.setattr(controls.os, "getpgid", lambda _pid: group)
    monkeypatch.setattr(controls.os, "readlink", lambda _path: str(config.game_dir))
    monkeypatch.setattr(controls.ev, "ownership_proof", lambda *_a, **_kw: object())

    target = controls.discover_game_target(
        group,
        config.game_dir,
        process_reader=lambda: records,
        probe_factory=lambda display: _Probe(display),
    )
    assert target == controls.GameTarget(":4", 20, 5020, group, "bugs.exe", 640, 480)

    stopped: list[tuple[str, int]] = []

    class _StopProbe:
        def __init__(self, display: str) -> None:
            self.display = display

        def stop_recording(self, window_id: int) -> None:
            stopped.append((self.display, window_id))

    controls.stop_recording_exact(
        target,
        config.game_dir,
        discoverer=lambda _group, _game_dir: target,
        probe_factory=_StopProbe,
    )
    assert stopped == [(":4", 20)]

    with pytest.raises(controls.ControlError, match="identity changed"):
        controls.stop_recording_exact(
            target,
            config.game_dir,
            discoverer=lambda _group, _game_dir: None,
            probe_factory=_StopProbe,
        )
    assert stopped == [(":4", 20)]

    with pytest.raises(controls.ControlError, match="multiple exact"):
        controls.discover_game_target(
            group,
            config.game_dir,
            process_reader=lambda: records,
            probe_factory=lambda display: _Probe(display, two_exact=True),
        )


def test_dry_run_preserves_familiar_pristine_options() -> None:
    result = subprocess.run(
        [
            str(PYTHON),
            str(SCRIPT),
            "--research",
            "--windowed",
            "--mute",
            "--coordinates",
            "--dry-run",
        ],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    command = payload["launcher_command"]
    assert command[0].endswith("/scripts/play-pristine.sh")
    assert command.count("--windowed") == 1
    assert command[-2:] == ["--research", "--mute"]
    assert payload["always_windowed"] is True
    assert payload["auto_coordinates"] is True


def test_recorder_cleanup_targets_only_its_isolated_process_group() -> None:
    child = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        start_new_session=True,
    )
    try:
        controls.interrupt_recorder(child)
        assert child.poll() is not None
    finally:
        if child.poll() is None:
            child.terminate()
            child.wait(timeout=5)


def test_recorder_cleanup_refuses_nonisolated_child() -> None:
    child = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"],
    )
    try:
        with pytest.raises(controls.ControlError, match="non-isolated"):
            controls.interrupt_recorder(child)
        assert child.poll() is None
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_session_cleanup_retains_group_after_launcher_leader_exits() -> None:
    leader = subprocess.Popen(
        [
            sys.executable,
            "-c",
            (
                "import os,time\n"
                "child=os.fork()\n"
                "if child:\n print(child,flush=True); raise SystemExit(0)\n"
                "time.sleep(30)\n"
            ),
        ],
        start_new_session=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    assert leader.stdout is not None
    child_pid = int(leader.stdout.readline().strip())
    leader.wait(timeout=5)
    try:
        assert any(
            item.pid == child_pid
            for item in controls._process_group_members(leader.pid)
        )
        controls.terminate_session(leader, timeout=2)
        assert controls._process_group_members(leader.pid) == ()
    finally:
        if controls._process_group_members(leader.pid):
            os.killpg(leader.pid, signal.SIGKILL)
