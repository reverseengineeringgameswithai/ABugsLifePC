"""Regressions for the menu/chooser key delivery tool.

The behaviours under test are the ones this project learned the hard way: the
game ignores synthetic ``XSendEvent`` input, a tapped key falls between
``GetAsyncKeyState`` polls, and focus must be re-established before every
press.  The stub ``xdotool`` records a press as delivered only when it arrives
the way the game actually accepts it.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import struct
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import evidence_lib as ev  # noqa: E402
import session_lib as sl  # noqa: E402
import game_fixture as gf  # noqa: E402

TOOL = SCRIPTS / "send-keys.py"

requires_fixed_map = pytest.mark.skipif(
    not gf.have_fixed_mapping(),
    reason="the fixture's fixed address window is not mappable on this host",
)


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["ABLPC_ROOT"] = str(root)
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True, text=True, env=env, timeout=120,
    )


def payload(result: subprocess.CompletedProcess) -> dict:
    return json.loads(result.stdout)


def test_capabilities_declares_the_delivery_contract(tmp_path: Path) -> None:
    caps = payload(run(tmp_path, "--capabilities"))
    assert caps["delivery"]["method"] == "xtest"
    assert caps["delivery"]["refuses_synthetic_xsendevent"] is True
    assert caps["delivery"]["focus_before_every_press"] is True
    assert caps["delivery"]["default_hold_ms"] == 180


def test_levels_reports_the_static_roster(tmp_path: Path) -> None:
    data = payload(run(tmp_path, "levels"))
    rows = {row["name"]: row for row in data["levels"]}
    assert rows["Tunnels"]["carousel_position"] == 2
    assert rows["Tunnels"]["internal_index"] == 3
    assert rows["City Entrance"]["carousel_position"] == 7
    assert rows["City Entrance"]["internal_index"] == 4


def test_send_holds_each_key_and_refocuses_first(tmp_path: Path) -> None:
    binary, _, calls, keys = gf.write_stub_xdotool(
        tmp_path, window_id=777, game_pid=os.getpid()
    )
    result = run(tmp_path, "send", "--display", ":9", "--window-id", "777",
                 "--keys", "Down,Return", "--hold-ms", "20", "--gap-ms", "10",
                 "--xdotool", str(binary))
    assert result.returncode == 0, result.stderr
    data = payload(result)
    assert data["press_count"] == 2
    assert data["method"] == "xtest"
    assert data["synthetic_xsendevent_used"] is False
    assert [press["keysym"] for press in data["presses"]] == ["Down", "Return"]
    assert all(press["observed_hold_ms"] >= 20 for press in data["presses"])

    # Both presses actually landed, and each was preceded by a focus pair.
    assert keys.read_text().split() == ["Down", "Return"]
    verbs = [line.split()[0] for line in calls.read_text().splitlines() if line.strip()]
    assert verbs.count("keydown") == 2 and verbs.count("keyup") == 2
    for index, verb in enumerate(verbs):
        if verb == "keydown":
            assert "windowactivate" in verbs[:index]
            assert "windowfocus" in verbs[:index]


def test_send_never_uses_window_targeted_delivery(tmp_path: Path) -> None:
    binary, _, calls, _ = gf.write_stub_xdotool(
        tmp_path, window_id=777, game_pid=os.getpid()
    )
    run(tmp_path, "send", "--display", ":9", "--window-id", "777",
        "--key", "Down", "--hold-ms", "5", "--xdotool", str(binary))
    for line in calls.read_text().splitlines():
        if line.startswith(("keydown", "keyup", "key ")):
            assert "--window" not in line


def test_send_refuses_a_window_that_is_not_the_game(tmp_path: Path) -> None:
    binary, _, _, _ = gf.write_stub_xdotool(
        tmp_path, window_id=777, game_pid=os.getpid(), window_class="firefox"
    )
    result = run(tmp_path, "send", "--display", ":9", "--window-id", "777",
                 "--key", "Down", "--xdotool", str(binary))
    assert result.returncode == ev.EXIT_REFUSAL
    assert payload(result)["reason"] == "window_class_mismatch"


def test_send_refuses_a_window_of_the_wrong_size(tmp_path: Path) -> None:
    binary, _, _, _ = gf.write_stub_xdotool(
        tmp_path, window_id=777, game_pid=os.getpid(), width=1280, height=960
    )
    result = run(tmp_path, "send", "--display", ":9", "--window-id", "777",
                 "--key", "Down", "--xdotool", str(binary))
    assert result.returncode == ev.EXIT_REFUSAL
    assert payload(result)["reason"] == "window_size_mismatch"


def test_send_refuses_when_focus_is_elsewhere(tmp_path: Path) -> None:
    binary, _, _, _ = gf.write_stub_xdotool(
        tmp_path, window_id=777, game_pid=os.getpid(), focused_window=42
    )
    result = run(tmp_path, "send", "--display", ":9", "--window-id", "777",
                 "--key", "Down", "--xdotool", str(binary))
    assert result.returncode == ev.EXIT_REFUSAL
    assert payload(result)["reason"] == "focus_lost"


def test_send_caps_the_press_count(tmp_path: Path) -> None:
    binary, _, _, _ = gf.write_stub_xdotool(
        tmp_path, window_id=777, game_pid=os.getpid()
    )
    result = run(tmp_path, "send", "--display", ":9", "--window-id", "777",
                 "--key", "Right", "--repeat", str(sl.MAX_KEY_PRESSES + 1),
                 "--xdotool", str(binary))
    assert result.returncode == ev.EXIT_USAGE
    assert "cap" in result.stderr


@pytest.mark.parametrize("keysym", ["Down;reboot", "two words", ""])
def test_send_rejects_invalid_keysyms(tmp_path: Path, keysym: str) -> None:
    binary, _, _, _ = gf.write_stub_xdotool(
        tmp_path, window_id=777, game_pid=os.getpid()
    )
    result = run(tmp_path, "send", "--display", ":9", "--window-id", "777",
                 "--key", keysym, "--xdotool", str(binary))
    assert result.returncode == ev.EXIT_USAGE


def test_send_requires_a_target(tmp_path: Path) -> None:
    result = run(tmp_path, "send", "--key", "Down")
    assert result.returncode == ev.EXIT_USAGE


@requires_fixed_map
def test_verify_level_confirms_from_memory(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        binary, _, _, _ = gf.write_stub_xdotool(
            tmp_path, window_id=777, game_pid=game.pid
        )
        result = run(tmp_path, "send", "--display", ":9", "--window-id", "777",
                     "--pid", str(game.pid), "--key", "Down", "--hold-ms", "5",
                     "--verify-level", "0", "--xdotool", str(binary))
        assert result.returncode == 0, result.stderr
        verification = payload(result)["level_verification"]
        assert verification["matched"] is True
        assert verification["observed_internal_index"] == 0


@requires_fixed_map
def test_verify_level_reports_a_mismatch_as_tool_negative(tmp_path: Path) -> None:
    """Dispatching input is not the same as reaching the level."""

    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        binary, _, _, _ = gf.write_stub_xdotool(
            tmp_path, window_id=777, game_pid=game.pid
        )
        result = run(tmp_path, "send", "--display", ":9", "--window-id", "777",
                     "--pid", str(game.pid), "--key", "Return", "--hold-ms", "5",
                     "--verify-level", "Tunnels", "--xdotool", str(binary))
        assert result.returncode == ev.EXIT_TOOL_NEGATIVE
        verification = payload(result)["level_verification"]
        assert verification["expected_internal_index"] == 3
        assert verification["observed_internal_index"] == 0
        assert verification["matched"] is False


@requires_fixed_map
def test_send_resolves_a_recorded_session(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        binary, _, _, keys = gf.write_stub_xdotool(
            tmp_path, window_id=777, game_pid=game.pid
        )
        manifest = sl.SessionManifest(
            session_id="RUN-SESSION-20260817-120000",
            created_at="2026-08-17T12:00:00-04:00",
            display=":9", window_id=777, game_pid=game.pid,
            game_start_ticks=sl.pid_identity(game.pid)[1],
            process_group=os.getpgid(game.pid),
        )
        manifest.save(root=tmp_path)
        result = run(tmp_path, "send", "--session", "current",
                     "--key", "Left", "--hold-ms", "5", "--xdotool", str(binary))
        assert result.returncode == 0, result.stderr
        assert payload(result)["session_id"] == manifest.session_id
        assert keys.read_text().strip() == "Left"
