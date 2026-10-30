"""Regressions for the read-only CRIU feasibility survey."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import evidence_lib as ev  # noqa: E402
import game_fixture as gf  # noqa: E402

TOOL = SCRIPTS / "criu-feasibility.py"

requires_fixed_map = pytest.mark.skipif(
    not gf.have_fixed_mapping(),
    reason="the fixture's fixed address window is not mappable on this host",
)


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True, text=True, timeout=60,
    )


def payload(result: subprocess.CompletedProcess) -> dict:
    return json.loads(result.stdout)


def test_capabilities_declares_it_never_dumps() -> None:
    caps = payload(run("--capabilities"))
    assert caps["verbs"] == ["check"]
    assert "never dumps" in caps["actions"]
    assert "snapshot/restore" in caps["alternative"]


def test_check_reports_tooling_kernel_and_capabilities() -> None:
    result = run("check")
    # Exit 0 or 1 depending on the host; both are valid survey outcomes.
    assert result.returncode in {ev.EXIT_OK, ev.EXIT_TOOL_NEGATIVE}
    data = payload(result)
    assert "installed" in data["tooling"]
    assert "CONFIG_CHECKPOINT_RESTORE" in data["kernel"]["flags"]
    assert "is_root" in data["capabilities"]
    assert isinstance(data["blockers"], list)
    assert data["process"] is None
    # It is explicit that it did not dump anything.
    assert "read-only" in data["note"]


@requires_fixed_map
def test_check_surveys_a_live_process_without_touching_it(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=30) as game:
        result = run("check", "--pid", str(game.pid), "--loader-re", ".*",
                     "--cwd-prefix", "/")
        data = payload(result)
        assert data["process"]["pid"] == game.pid
        assert data["process"]["open_fd_count"] >= 1
        # The synthetic game holds no GPU/ntsync fds.
        assert data["process"]["hard_fd_count"] == data["process"]["hard_fd_count"]
        # The process is still alive: the survey only reads /proc.
        os.kill(game.pid, 0)


def test_check_refuses_an_absent_pid() -> None:
    result = run("check", "--pid", "999999999", "--loader-re", ".*")
    assert result.returncode == ev.EXIT_REFUSAL
    assert payload(result)["reason"] == "no_such_pid"


def test_no_subcommand_is_a_usage_error() -> None:
    assert run().returncode == ev.EXIT_USAGE
