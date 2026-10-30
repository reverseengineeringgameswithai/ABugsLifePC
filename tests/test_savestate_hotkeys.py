"""Regressions for the save-state hotkey daemon's testable core.

The X key-grab and Tk popups need a live Gamescope display and are validated by
a real run, not here. What is covered: the SaveStateController that drives
game-memory.py snapshot/restore against the synthetic game, hotkey-map
construction, listing/ordering, and refusals.
"""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import types

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import evidence_lib as ev  # noqa: E402
import session_lib as sl  # noqa: E402
import game_fixture as gf  # noqa: E402


def load_module():
    spec = importlib.util.spec_from_file_location(
        "savestate_hotkeys", SCRIPTS / "savestate-hotkeys.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ssh = load_module()

requires_fixed_map = pytest.mark.skipif(
    not gf.have_fixed_mapping(),
    reason="the fixture's fixed address window is not mappable on this host")

FIXTURE_REGION = f"0x{gf.MIRROR_SRC_ADDRESS:08X}:16"


def git_sandbox(root: Path) -> None:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / ".gitignore").write_text("/work/snapshots/\n", encoding="utf-8")


def controller_for(game: gf.FakeGame, root: Path) -> "ssh.SaveStateController":
    # game-memory.py resolves ABLPC_ROOT from the environment for its run dirs;
    # the controller shells out, so set it for the subprocess.
    os.environ["ABLPC_ROOT"] = str(root)
    return ssh.SaveStateController(
        game.pid, accept_sha=game.exe_sha256,
        snapshot_dir=root / "work" / "snapshots",
        loader_re=".*", regions=(FIXTURE_REGION,))


# --------------------------------------------------------------------------
# Contract
# --------------------------------------------------------------------------


def test_capabilities_is_honest_about_validation(tmp_path: Path) -> None:
    r = subprocess.run([sys.executable, str(SCRIPTS / "savestate-hotkeys.py"),
                        "--capabilities"], capture_output=True, text=True)
    caps = json.loads(r.stdout)
    assert caps["verbs"] == ["run", "list"]
    assert "nested" in caps["hotkeys"]["scope"]
    assert "logic-tested only" in caps["validation"]
    assert "relaunch" in caps["not_a_savestate"]


def test_build_keymap_rejects_duplicate_hotkeys() -> None:
    args = types.SimpleNamespace(save_key="F5", load_key="F5", quicksave_key="F6",
                                 quickload_key="F7", quit_key="F12")
    with pytest.raises(ssh.SaveStateError) as exc:
        ssh.build_keymap(args)
    assert exc.value.reason == "duplicate_hotkey"


def test_build_keymap_maps_all_five_actions() -> None:
    args = types.SimpleNamespace(save_key="F1", load_key="F3", quicksave_key="F6",
                                 quickload_key="F7", quit_key="F12")
    keymap = ssh.build_keymap(args)
    assert keymap == {"F1": "save", "F3": "load", "F6": "quicksave",
                      "F7": "quickload", "F12": "quit"}


def test_resolve_game_requires_a_target(tmp_path: Path) -> None:
    args = types.SimpleNamespace(session=None, pid=None, display=None,
                                 window_id=None, loader_re=".*", xdotool="xdotool")
    with pytest.raises(ssh.SaveStateError) as exc:
        ssh.resolve_game(args)
    assert exc.value.reason == "no_target"


# --------------------------------------------------------------------------
# SaveStateController against the synthetic game
# --------------------------------------------------------------------------


@requires_fixed_map
def test_save_then_list_shows_the_checkpoint(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        c = controller_for(game, tmp_path)
        c.save("before-jump")
        names = [s.name for s in c.list_saves()]
        assert names == ["before-jump"]
        latest = c.latest()
        assert latest.name == "before-jump" and latest.level == 0


@requires_fixed_map
def test_save_refuses_a_duplicate_unless_overwrite(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        c = controller_for(game, tmp_path)
        c.save("slot1")
        with pytest.raises(ssh.SaveStateError) as exc:
            c.save("slot1")
        assert exc.value.reason == "save_exists"
        # Overwrite replaces it (a quicksave semantics).
        c.save("slot1", overwrite=True)
        assert [s.name for s in c.list_saves()] == ["slot1"]


@requires_fixed_map
def test_save_change_load_reverts(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        c = controller_for(game, tmp_path)
        memory = sl.ProcessMemory(game.pid)
        original = memory.read(gf.MIRROR_SRC_ADDRESS, 4)
        c.save("checkpoint")
        memory.write_many(((gf.MIRROR_SRC_ADDRESS, bytes.fromhex("11223344")),))
        assert memory.read(gf.MIRROR_SRC_ADDRESS, 4).hex() == "11223344"
        result = c.load("checkpoint")
        assert result["load_verified"] is True
        assert memory.read(gf.MIRROR_SRC_ADDRESS, 4) == original


@requires_fixed_map
def test_load_missing_save_raises(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        c = controller_for(game, tmp_path)
        with pytest.raises(ssh.SaveStateError) as exc:
            c.load("nope")
        assert exc.value.reason == "save_not_found"


@requires_fixed_map
def test_list_orders_newest_first(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        c = controller_for(game, tmp_path)
        c.save("first")
        time.sleep(1.05)  # captured_at is whole-second resolution
        c.save("second")
        assert [s.name for s in c.list_saves()] == ["second", "first"]
        assert c.latest().name == "second"


@requires_fixed_map
def test_load_authorizes_and_writes_a_receipt(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        c = controller_for(game, tmp_path)
        c.save("cp")
        c.load("cp")
        receipts = sorted((tmp_path / ev.RUN_ROOT).glob("RUN-RESTORE-*/receipt.json"))
        assert receipts
        receipt = json.loads(receipts[-1].read_text())
        assert receipt["authorization"] == ssh.LOAD_AUTHORIZE
        assert "hotkey" in receipt["purpose"]
