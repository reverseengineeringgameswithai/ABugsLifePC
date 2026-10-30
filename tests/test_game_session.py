"""End-to-end regressions for the session-control tool.

Exercises the whole launch recipe against the synthetic fixture: detached
launch, owned-display and owned-window discovery, the chooser sequence, the
fail-closed renderer gate, carousel navigation confirmed from memory, the
ownership ledger, and closure by recorded identity only.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import time

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import evidence_lib as ev  # noqa: E402
import session_lib as sl  # noqa: E402
import game_fixture as gf  # noqa: E402

TOOL = SCRIPTS / "game-session.py"

requires_fixed_map = pytest.mark.skipif(
    not gf.have_fixed_mapping(),
    reason="the fixture's fixed address window is not mappable on this host",
)

# A name the runtime audit will never match, so the preflight gate can be
# exercised in both directions without depending on what the host happens to
# be running.
NO_SUCH_PROCESS = "ablpc-no-such-runtime-process"


def run(root: Path, *args: str, config: Path | None = None,
        timeout: float = 180) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["ABLPC_ROOT"] = str(root)
    if config is not None:
        env["ABLPC_FIXTURE_CONFIG"] = str(config)
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True, text=True, env=env, timeout=timeout,
    )


def payload(result: subprocess.CompletedProcess) -> dict:
    return json.loads(result.stdout)


def launch_args(session: gf.FakeSession, stub: Path, **overrides) -> list[str]:
    args = {
        "--launcher": str(session.launcher_path),
        "--game-dir": str(session.game_dir),
        "--xdotool": str(stub),
        "--pactl": "/bin/false",
        "--accept-sha": session.exe_sha256,
        "--loader-re": ".*",
        "--audit-name": NO_SUCH_PROCESS,
        "--window-timeout": "30",
        "--gate-timeout": "30",
        "--level-timeout": "20",
        "--chooser-delay-ms": "150",
        "--hold-ms": "10",
        "--gap-ms": "60",
        "--poll-ms": "50",
        "--grace-s": "3",
    }
    args.update(overrides)
    flat: list[str] = ["launch"]
    for key, value in args.items():
        # An empty value marks a store_true flag, which takes no argument.
        flat.extend([key] if value == "" else [key, str(value)])
    return flat


def do_launch(root: Path, session: gf.FakeSession, stub: Path,
              **overrides) -> subprocess.CompletedProcess:
    """Launch through the tool, then read the launcher's own status file."""

    result = run(root, *launch_args(session, stub, **overrides),
                 config=session.config_path)
    try:
        session.await_status(timeout=5)
    except RuntimeError:
        pass
    return result


def sessions(root: Path) -> list[Path]:
    return sorted((root / ev.RUN_ROOT).glob("RUN-SESSION-*"))


def alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


# --------------------------------------------------------------------------
# Contract
# --------------------------------------------------------------------------


def test_capabilities_records_the_gate_and_ownership_rules(tmp_path: Path) -> None:
    caps = payload(run(tmp_path, "--capabilities"))
    assert caps["verbs"] == [
        "preflight", "launch", "status", "level", "close", "audit", "list"
    ]
    assert len(caps["renderer_gate"]["required_markers"]) == 6
    assert "screenshots" in caps["renderer_gate"]["authority"]
    assert caps["ownership"]["identity"] == "pid + process group + PID start ticks"
    assert "recycled PIDs are skipped" in caps["ownership"]["cleanup"]


def test_no_subcommand_is_a_usage_error(tmp_path: Path) -> None:
    assert run(tmp_path).returncode == ev.EXIT_USAGE


def test_dry_run_prints_the_plan_without_launching(tmp_path: Path) -> None:
    result = run(tmp_path, "launch", "--dry-run", "--game-dir", str(tmp_path / "g"))
    assert result.returncode == 0, result.stderr
    data = payload(result)
    assert data["dry_run"] is True
    assert "--research" in data["launcher_command"]
    assert "six" in data["renderer_plan"]
    assert not sessions(tmp_path)


def test_dry_run_reports_the_auto_hardware_plan(tmp_path: Path) -> None:
    result = run(tmp_path, "launch", "--dry-run", "--auto-hardware",
                 "--game-dir", str(tmp_path / "g"))
    data = payload(result)
    assert "--auto-hardware" in data["launcher_command"]
    assert "no chooser input" in data["renderer_plan"]


def test_preflight_is_clean_when_no_runtime_process_matches(tmp_path: Path) -> None:
    result = run(tmp_path, "preflight", "--audit-name", NO_SUCH_PROCESS)
    assert result.returncode == 0, result.stderr
    data = payload(result)
    assert data["clean"] is True
    assert data["audit_names"] == [NO_SUCH_PROCESS]


def test_list_is_empty_before_any_launch(tmp_path: Path) -> None:
    data = payload(run(tmp_path, "list"))
    assert data["count"] == 0


def test_close_without_a_session_is_refused(tmp_path: Path) -> None:
    result = run(tmp_path, "close")
    assert result.returncode == ev.EXIT_REFUSAL
    assert payload(result)["reason"] == "no_live_session"


# --------------------------------------------------------------------------
# Launch
# --------------------------------------------------------------------------


@requires_fixed_map
def test_launch_drives_the_chooser_and_accepts_the_six_markers(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=90) as session:
        stub, _, calls, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
        )
        result = do_launch(tmp_path, session, stub)
        assert result.returncode == 0, result.stdout + result.stderr
        data = payload(result)
        assert data["accepted"] is True

        manifest = data["session"]
        assert manifest["display"] == ":9"
        assert manifest["window_id"] == 777
        assert manifest["game_pid"] == session.status["game_pid"]
        assert manifest["exe_sha256"] == session.exe_sha256
        assert manifest["game_start_ticks"] is not None

        gate = manifest["renderer_gate"]
        assert gate["accepted"] is True
        assert len(gate["markers_found"]) == 6
        assert gate["rejects_found"] == []
        assert [press["keysym"] for press in gate["presses"]] == ["Down", "Return"]

        # The chooser was driven with held XTEST presses, never with
        # window-targeted synthetic events.
        for line in calls.read_text().splitlines():
            if line.startswith(("keydown", "keyup")):
                assert "--window" not in line

        # The ownership ledger exists on disk and records the group members.
        directory = sessions(tmp_path)[0]
        stored = json.loads((directory / "session.json").read_text())
        assert stored["state"] == "open"
        assert stored["schema_version"] == sl.SESSION_SCHEMA_VERSION
        assert any(p["pid"] == session.status["game_pid"]
                   for p in stored["owned_processes"])
        assert (directory / "preflight.json").exists()
        assert (directory / "launcher-stdout.txt").exists()

        run(tmp_path, "close", "--session", stored["session_id"],
            "--pactl", "/bin/false", "--audit-name", NO_SUCH_PROCESS)


@requires_fixed_map
def test_launch_rejects_a_software_renderer_arm_and_closes_it(tmp_path: Path) -> None:
    """A software arm is not a hardware control; the arm is rejected."""

    with gf.FakeSession(tmp_path, lifetime_s=90,
                        confirm_markers=gf.SOFTWARE_MARKERS) as session:
        stub, _, _, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
        )
        result = do_launch(tmp_path, session, stub)
        assert result.returncode == ev.EXIT_TOOL_NEGATIVE
        data = payload(result)
        assert data["accepted"] is False
        assert data["reason"] == "renderer_gate_failed"
        assert data["session"]["renderer_gate"]["rejects_found"]

        # The rejected arm was closed rather than left running.
        assert data["closure"]["reason"] == "renderer_gate_failed"
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline and alive(session.status["game_pid"]):
            time.sleep(0.1)
        assert not alive(session.status["game_pid"])
        stored = json.loads((sessions(tmp_path)[0] / "session.json").read_text())
        assert stored["state"] == "closed"


@requires_fixed_map
def test_launch_can_keep_a_rejected_arm_for_inspection(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=90,
                        confirm_markers=gf.SOFTWARE_MARKERS) as session:
        stub, _, _, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
        )
        result = do_launch(tmp_path, session, stub, **{"--keep-on-reject": ""})
        assert result.returncode == ev.EXIT_TOOL_NEGATIVE
        assert alive(session.status["game_pid"])
        stored = json.loads((sessions(tmp_path)[0] / "session.json").read_text())
        assert stored["state"] == "open"
        run(tmp_path, "close", "--session", stored["session_id"],
            "--pactl", "/bin/false", "--audit-name", NO_SUCH_PROCESS)


@requires_fixed_map
def test_launch_accepts_the_auto_hardware_path_without_pressing_keys(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=90, confirm_markers=(),
                        pre_log_lines=gf.HARDWARE_MARKERS) as session:
        stub, _, _, keys = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
        )
        result = do_launch(tmp_path, session, stub, **{"--auto-hardware": ""})
        assert result.returncode == 0, result.stdout + result.stderr
        data = payload(result)
        assert data["accepted"] is True
        assert data["session"]["auto_hardware"] is True
        assert data["session"]["renderer_gate"]["presses"] == []
        assert keys.read_text().strip() == ""
        run(tmp_path, "close", "--session", data["session_id"],
            "--pactl", "/bin/false", "--audit-name", NO_SUCH_PROCESS)


@requires_fixed_map
def test_launch_refuses_when_unattributed_runtime_processes_exist(tmp_path: Path) -> None:
    """The lifecycle policy requires accounting for pre-existing instances."""

    with gf.FakeSession(tmp_path, lifetime_s=30) as session:
        session.start()
        stub, _, _, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
        )
        # Audit for the fixture's own bugs.exe, which is already running.
        result = run(tmp_path, *launch_args(session, stub,
                                            **{"--audit-name": "bugs.exe"}),
                     config=session.config_path)
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "unattributed_runtime_processes"
        assert not sessions(tmp_path)


# --------------------------------------------------------------------------
# Level navigation
# --------------------------------------------------------------------------


@requires_fixed_map
def test_launch_navigates_to_a_level_and_confirms_it_from_memory(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=90) as session:
        stub, _, _, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
        )
        result = do_launch(tmp_path, session, stub, **{"--level": "Tunnels"})
        assert result.returncode == 0, result.stdout + result.stderr
        navigation = payload(result)["level"]
        assert navigation["level_name"] == "Tunnels"
        assert navigation["carousel_target"] == 2
        assert navigation["carousel_observed"] == 2
        assert navigation["internal_expected"] == 3
        assert navigation["internal_observed"] == 3
        assert navigation["matched"] is True
        assert len(navigation["steps"]) == 2
        assert all(step["advanced"] for step in navigation["steps"])
        run(tmp_path, "close", "--session", payload(result)["session_id"],
            "--pactl", "/bin/false", "--audit-name", NO_SUCH_PROCESS)


@requires_fixed_map
def test_navigation_retries_a_dropped_carousel_press(tmp_path: Path) -> None:
    """A press that falls between GetAsyncKeyState polls is detected from the
    carousel counter and retried, instead of silently selecting the wrong
    level as it did in EXP-20260816-156."""

    with gf.FakeSession(tmp_path, lifetime_s=90) as session:
        stub, _, _, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
            # The chooser Return lands; then the first Right press is dropped.
            drop_keys=("Right",),
        )
        result = do_launch(tmp_path, session, stub, **{"--level": "Tunnels"})
        assert result.returncode == 0, result.stdout + result.stderr
        navigation = payload(result)["level"]
        assert navigation["matched"] is True
        assert navigation["internal_observed"] == 3
        attempts = [step for step in navigation["steps"] if step["press"] == 0]
        assert len(attempts) == 2
        assert attempts[0]["advanced"] is False
        assert attempts[1]["advanced"] is True
        run(tmp_path, "close", "--session", payload(result)["session_id"],
            "--pactl", "/bin/false", "--audit-name", NO_SUCH_PROCESS)


@requires_fixed_map
def test_navigation_gives_up_after_repeated_dropped_presses(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=90) as session:
        stub, _, _, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
            drop_keys=("Right", "Right", "Right", "Right"),
        )
        result = do_launch(
            tmp_path, session, stub,
            **{"--level": "Tunnels", "--max-press-retries": "2"})
        assert result.returncode == ev.EXIT_TOOL_NEGATIVE
        data = payload(result)
        assert data["reason"] == "level_navigation_failed"
        assert data["level"]["reason"] == "carousel_press_not_registered"
        assert data["level"]["matched"] is False
        run(tmp_path, "close", "--session", data["session_id"],
            "--pactl", "/bin/false", "--audit-name", NO_SUCH_PROCESS)


@requires_fixed_map
def test_level_refuses_an_unknown_level(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=60) as session:
        stub, _, _, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
        )
        launch = do_launch(tmp_path, session, stub)
        assert launch.returncode == 0, launch.stdout + launch.stderr
        session_id = payload(launch)["session_id"]
        result = run(tmp_path, "level", "--session", session_id, "--level", "Atlantis",
                     "--xdotool", str(stub), "--pactl", "/bin/false")
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "unknown_level"
        run(tmp_path, "close", "--session", session_id,
            "--pactl", "/bin/false", "--audit-name", NO_SUCH_PROCESS)


# --------------------------------------------------------------------------
# Status, audit, and closure
# --------------------------------------------------------------------------


@requires_fixed_map
def test_status_reverifies_identity_and_reads_the_level(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=90) as session:
        stub, _, _, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
        )
        launch = do_launch(tmp_path, session, stub)
        session_id = payload(launch)["session_id"]

        result = run(tmp_path, "status", "--session", session_id,
                     "--pactl", "/bin/false")
        assert result.returncode == 0, result.stderr
        data = payload(result)
        assert data["live"] is True
        assert data["internal_level"] == 0
        assert any(member["pid"] == session.status["game_pid"]
                   for member in data["group_members"])
        run(tmp_path, "close", "--session", session_id,
            "--pactl", "/bin/false", "--audit-name", NO_SUCH_PROCESS)


@requires_fixed_map
def test_close_terminates_only_recorded_identities(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=90) as session:
        stub, _, _, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
        )
        launch = do_launch(tmp_path, session, stub)
        session_id = payload(launch)["session_id"]
        game_pid = session.status["game_pid"]
        launcher_pid = session.status["launcher_pid"]

        result = run(tmp_path, "close", "--session", session_id, "--grace-s", "3",
                     "--pactl", "/bin/false", "--audit-name", NO_SUCH_PROCESS)
        assert result.returncode == 0, result.stdout
        closure = payload(result)["closure"]
        assert closure["clean"] is True
        assert closure["survivors"] == []
        signalled = {row["pid"] for row in closure["process_actions"]
                     if row["action"] in {"sigterm", "sigkill"}}
        assert game_pid in signalled and launcher_pid in signalled
        # Nothing outside the recorded group was touched.
        assert os.getpid() not in signalled
        assert not alive(game_pid)

        stored = json.loads((sessions(tmp_path)[0] / "session.json").read_text())
        assert stored["state"] == "closed"
        assert stored["closure"]["clean"] is True


@requires_fixed_map
def test_close_skips_a_recycled_pid(tmp_path: Path) -> None:
    """Start ticks make a reused PID number detectable, so cleanup declines it."""

    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        group, ticks = sl.pid_identity(game.pid)
        manifest = sl.SessionManifest(
            session_id="RUN-SESSION-20260817-120000",
            created_at="2026-08-17T12:00:00-04:00",
            process_group=group,
            game_pid=game.pid,
            game_start_ticks=ticks,
            owned_processes=[{"pid": game.pid, "start_ticks": ticks + 7,
                              "process_group": group, "command": ["bugs.exe"]}],
        )
        manifest.save(root=tmp_path)
        result = run(tmp_path, "close", "--session", manifest.session_id,
                     "--grace-s", "1", "--pactl", "/bin/false",
                     "--audit-name", NO_SUCH_PROCESS)
        actions = {row["pid"]: row for row in payload(result)["closure"]["process_actions"]}
        assert actions[game.pid]["action"] == "skipped_recycled"
        assert alive(game.pid)


@requires_fixed_map
def test_audit_attributes_an_open_session(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=90) as session:
        stub, _, _, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
        )
        launch = do_launch(tmp_path, session, stub)
        session_id = payload(launch)["session_id"]

        result = run(tmp_path, "audit", "--pactl", "/bin/false",
                     "--audit-name", "bugs.exe")
        data = payload(result)
        owned = [row for row in data["processes"]["processes"] if row["owned"]]
        assert any(row["pid"] == session.status["game_pid"] for row in owned)
        assert session_id in data["open_sessions"]
        run(tmp_path, "close", "--session", session_id,
            "--pactl", "/bin/false", "--audit-name", NO_SUCH_PROCESS)


@requires_fixed_map
def test_list_reports_state_after_launch_and_close(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=90) as session:
        stub, _, _, _ = gf.write_stub_xdotool(
            tmp_path / "fixture", window_id=777, game_pid=0,
            status_path=session.status_path,
        )
        launch = do_launch(tmp_path, session, stub)
        session_id = payload(launch)["session_id"]
        listing = payload(run(tmp_path, "list"))
        row = listing["sessions"][0]
        assert row["session_id"] == session_id
        assert row["state"] == "open" and row["live"] is True
        assert row["renderer_accepted"] is True

        run(tmp_path, "close", "--session", session_id,
            "--pactl", "/bin/false", "--audit-name", NO_SUCH_PROCESS)
        after = payload(run(tmp_path, "list"))["sessions"][0]
        assert after["state"] == "closed" and after["live"] is False
