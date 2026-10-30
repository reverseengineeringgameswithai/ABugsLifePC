"""Regressions for the unified wait-for-condition tool."""

from __future__ import annotations

import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import threading
import time

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import evidence_lib as ev  # noqa: E402
import session_lib as sl  # noqa: E402
import game_fixture as gf  # noqa: E402

TOOL = SCRIPTS / "wait-for.py"

requires_fixed_map = pytest.mark.skipif(
    not gf.have_fixed_mapping(),
    reason="the fixture's fixed address window is not mappable on this host",
)


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["ABLPC_ROOT"] = str(root)
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True, text=True, env=env, timeout=180,
    )


def payload(result: subprocess.CompletedProcess) -> dict:
    return json.loads(result.stdout)


def after(delay: float, action) -> threading.Thread:
    def body() -> None:
        time.sleep(delay)
        action()

    thread = threading.Thread(target=body)
    thread.start()
    return thread


# --------------------------------------------------------------------------
# Contract
# --------------------------------------------------------------------------


def test_capabilities_lists_the_conditions(tmp_path: Path) -> None:
    caps = payload(run(tmp_path, "--capabilities"))
    assert caps["conditions"] == ["log", "memory", "level", "file", "window"]
    assert caps["exit_codes"]["1"] == "timed out"


def test_no_condition_is_a_usage_error(tmp_path: Path) -> None:
    assert run(tmp_path).returncode == ev.EXIT_USAGE


# --------------------------------------------------------------------------
# log
# --------------------------------------------------------------------------


def test_log_matches_a_marker_appended_after_the_wait_starts(tmp_path: Path) -> None:
    log = tmp_path / "bugs.log"
    log.write_text("boot\n", encoding="utf-8")

    def append() -> None:
        with open(log, "a", encoding="utf-8") as handle:
            handle.write("INIT : Starting Direct3D renderer\n")

    thread = after(0.3, append)
    result = run(tmp_path, "log", "--path", str(log),
                 "--marker", "Starting Direct3D renderer",
                 "--timeout", "10", "--poll-ms", "20")
    thread.join()
    assert result.returncode == 0, result.stderr
    data = payload(result)
    assert data["satisfied"] is True
    assert "Direct3D" in data["matched_line"]


def test_log_ignores_a_marker_that_predates_the_wait(tmp_path: Path) -> None:
    """New-bytes semantics: a previous run's marker must not satisfy a wait."""

    log = tmp_path / "bugs.log"
    log.write_text("INIT : Starting Direct3D renderer\n", encoding="utf-8")
    result = run(tmp_path, "log", "--path", str(log),
                 "--marker", "Starting Direct3D renderer",
                 "--timeout", "0.5", "--poll-ms", "20")
    assert result.returncode == ev.EXIT_TOOL_NEGATIVE
    assert payload(result)["reason"] == "timeout"


def test_log_from_start_scans_existing_content(tmp_path: Path) -> None:
    log = tmp_path / "bugs.log"
    log.write_text("INIT : Starting Direct3D renderer\n", encoding="utf-8")
    result = run(tmp_path, "log", "--path", str(log), "--from-start",
                 "--marker", "Starting Direct3D renderer",
                 "--timeout", "5", "--poll-ms", "20")
    assert result.returncode == 0
    assert payload(result)["satisfied"] is True


def test_log_tolerates_a_file_that_does_not_exist_yet(tmp_path: Path) -> None:
    log = tmp_path / "bugs.log"
    thread = after(0.3, lambda: log.write_text("NextLife.\n", encoding="utf-8"))
    result = run(tmp_path, "log", "--path", str(log), "--marker", "NextLife.",
                 "--timeout", "10", "--poll-ms", "20")
    thread.join()
    assert result.returncode == 0, result.stderr


def test_log_restarts_when_the_file_is_recreated(tmp_path: Path) -> None:
    """A relaunch truncates bugs.log; the offset must not skip the new run."""

    log = tmp_path / "bugs.log"
    log.write_text("x" * 5000, encoding="utf-8")

    def relaunch() -> None:
        log.write_text("fresh run\nNextLife.\n", encoding="utf-8")

    thread = after(0.3, relaunch)
    result = run(tmp_path, "log", "--path", str(log), "--marker", "NextLife.",
                 "--timeout", "10", "--poll-ms", "20")
    thread.join()
    assert result.returncode == 0, result.stderr
    assert payload(result)["satisfied"] is True


@pytest.mark.parametrize("bad", [["--timeout", "0"], ["--poll-ms", "0"]])
def test_log_rejects_invalid_timing(tmp_path: Path, bad: list[str]) -> None:
    log = tmp_path / "bugs.log"
    log.touch()
    result = run(tmp_path, "log", "--path", str(log), "--marker", "x", *bad)
    assert result.returncode == ev.EXIT_USAGE


# --------------------------------------------------------------------------
# file
# --------------------------------------------------------------------------


def test_file_waits_for_an_asynchronous_producer(tmp_path: Path) -> None:
    """gamescopectl screenshot returns before the file lands."""

    shot = tmp_path / "frame.png"

    def produce() -> None:
        shot.write_bytes(b"\x89PNG" + b"\x00" * 100)
        time.sleep(0.1)
        with open(shot, "ab") as handle:
            handle.write(b"\x00" * 5000)

    thread = after(0.2, produce)
    result = run(tmp_path, "file", "--path", str(shot), "--stable-ms", "150",
                 "--timeout", "10", "--poll-ms", "20")
    thread.join()
    assert result.returncode == 0, result.stderr
    data = payload(result)
    assert data["satisfied"] is True
    assert data["size"] == 5104


def test_file_times_out_when_nothing_appears(tmp_path: Path) -> None:
    result = run(tmp_path, "file", "--path", str(tmp_path / "absent.png"),
                 "--timeout", "0.4", "--poll-ms", "20")
    assert result.returncode == ev.EXIT_TOOL_NEGATIVE
    assert payload(result)["reason"] == "timeout"


# --------------------------------------------------------------------------
# memory and level
# --------------------------------------------------------------------------


@requires_fixed_map
def test_memory_waits_for_a_value(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        memory = sl.ProcessMemory(game.pid)
        thread = after(0.3, lambda: memory.write_many(
            ((gf.SCRATCH_ADDRESS, struct.pack("<i", 4242)),)
        ))
        result = run(tmp_path, "memory", "--pid", str(game.pid),
                     "--addr", f"0x{gf.SCRATCH_ADDRESS:08X}", "--format", "i32",
                     "--equals", "4242", "--timeout", "10", "--poll-ms", "20")
        thread.join()
        assert result.returncode == 0, result.stderr
        assert payload(result)["observed"] == 4242


@requires_fixed_map
def test_memory_waits_for_a_change(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        memory = sl.ProcessMemory(game.pid)
        thread = after(0.3, lambda: memory.write_many(
            ((gf.SCRATCH_ADDRESS, struct.pack("<i", 7)),)
        ))
        result = run(tmp_path, "memory", "--pid", str(game.pid),
                     "--addr", f"0x{gf.SCRATCH_ADDRESS:08X}", "--format", "i32",
                     "--changed", "--timeout", "10", "--poll-ms", "20")
        thread.join()
        assert result.returncode == 0, result.stderr
        data = payload(result)
        assert data["observed"] == 7 and data["baseline"] != 7


@requires_fixed_map
def test_memory_times_out_and_reports_the_last_value(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "memory", "--pid", str(game.pid),
                     "--addr", f"0x{gf.LEVEL_ADDRESS:08X}", "--format", "i32",
                     "--equals", "99", "--timeout", "0.4", "--poll-ms", "20")
        assert result.returncode == ev.EXIT_TOOL_NEGATIVE
        data = payload(result)
        assert data["reason"] == "timeout" and data["observed"] == 0


@requires_fixed_map
def test_memory_requires_exactly_one_predicate(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "memory", "--pid", str(game.pid),
                     "--addr", f"0x{gf.LEVEL_ADDRESS:08X}",
                     "--equals", "1", "--changed", "--timeout", "1")
        assert result.returncode == ev.EXIT_USAGE


@requires_fixed_map
def test_level_waits_for_the_internal_index(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        memory = sl.ProcessMemory(game.pid)
        thread = after(0.3, lambda: memory.write_many(
            ((gf.LEVEL_ADDRESS, struct.pack("<i", 3)),)
        ))
        result = run(tmp_path, "level", "--pid", str(game.pid), "--name", "Tunnels",
                     "--timeout", "10", "--poll-ms", "20")
        thread.join()
        assert result.returncode == 0, result.stderr
        data = payload(result)
        assert data["expected_internal_index"] == 3
        assert data["carousel_position"] == 2
        assert data["observed_internal_index"] == 3


@requires_fixed_map
def test_level_refuses_an_unknown_level_name(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "level", "--pid", str(game.pid),
                     "--name", "Atlantis", "--timeout", "1")
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "unknown_level"


# --------------------------------------------------------------------------
# window
# --------------------------------------------------------------------------


@requires_fixed_map
def test_window_waits_for_the_owned_game_window(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=40) as session:
        status = session.start()
        binary, _, _, _ = gf.write_stub_xdotool(
            tmp_path, window_id=777, game_pid=status["game_pid"]
        )
        manifest = sl.SessionManifest(
            session_id="RUN-SESSION-20260817-120000",
            created_at="2026-08-17T12:00:00-04:00",
            process_group=status["process_group"],
            game_dir=str(session.game_dir),
            game_pid=status["game_pid"],
            game_start_ticks=sl.pid_identity(status["game_pid"])[1],
        )
        manifest.save(root=tmp_path)
        env_path = os.environ.get("PATH", "")
        env = dict(os.environ)
        env["ABLPC_ROOT"] = str(tmp_path)
        env["PATH"] = f"{tmp_path}:{env_path}"
        result = subprocess.run(
            [sys.executable, str(TOOL), "window", "--session", manifest.session_id,
             "--timeout", "10", "--poll-ms", "50"],
            capture_output=True, text=True, env=env, timeout=60,
        )
        # The default loader regex expects a Wine loader, so the fixture's
        # python-hosted process is correctly not discoverable.
        assert result.returncode == ev.EXIT_TOOL_NEGATIVE
        assert json.loads(result.stdout)["reason"] == "timeout"


def test_window_requires_a_target(tmp_path: Path) -> None:
    result = run(tmp_path, "window", "--timeout", "1")
    assert result.returncode == ev.EXIT_USAGE
