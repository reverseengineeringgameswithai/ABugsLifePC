"""Regressions for the bounded live memory tool.

Every case runs against the synthetic fake game from ``game_fixture``, which
maps the real PC global addresses, so reads and writes exercise
``process_vm_readv``/``process_vm_writev`` for real without Wine or the game.
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

TOOL = SCRIPTS / "game-memory.py"

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


def target_flags(game: gf.FakeGame) -> list[str]:
    return ["--pid", str(game.pid), "--loader-re", ".*",
            "--accept-sha", game.exe_sha256]


def receipts(root: Path) -> list[Path]:
    return sorted((root / ev.RUN_ROOT).glob("RUN-POKE-*/receipt.json"))


def restore_receipts(root: Path) -> list[Path]:
    return sorted((root / ev.RUN_ROOT).glob("RUN-RESTORE-*/receipt.json"))


def git_sandbox(root: Path) -> None:
    """Init a git repo so snapshot's git-ignored-path check works."""

    subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / ".gitignore").write_text("/work/snapshots/\n", encoding="utf-8")


# A region inside the fixture's mapped window (0x00599000-0x00862FFF).
FIXTURE_REGION = f"0x{gf.MIRROR_SRC_ADDRESS:08X}:4096"


# --------------------------------------------------------------------------
# Contract
# --------------------------------------------------------------------------


def test_capabilities_declares_the_write_gates(tmp_path: Path) -> None:
    result = run(tmp_path, "--capabilities")
    assert result.returncode == 0
    caps = payload(result)
    assert caps["tool"] == "game-memory"
    assert caps["read_verbs"] == ["peek", "state", "watch", "snapshot"]
    assert caps["write_verbs"] == ["poke", "teleport", "restore"]
    assert any("authorize" in rule for rule in caps["write_requirements"])
    assert "engine-frame synchronization" in caps["claims_not_made"]


def test_no_subcommand_is_a_usage_error(tmp_path: Path) -> None:
    assert run(tmp_path).returncode == ev.EXIT_USAGE


def test_peek_without_a_target_is_a_usage_error(tmp_path: Path) -> None:
    result = run(tmp_path, "peek", "--read", "0x1000:4")
    assert result.returncode == ev.EXIT_USAGE


# --------------------------------------------------------------------------
# Reads
# --------------------------------------------------------------------------


@requires_fixed_map
def test_peek_reads_a_known_global(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "peek", *target_flags(game),
                     "--read", f"0x{gf.SCRATCH_ADDRESS:08X}:4")
        assert result.returncode == 0, result.stderr
        data = payload(result)
        assert data["reads"][0]["hex"] == "deadbeef"
        assert data["target"]["pid"] == game.pid
        assert data["target"]["ownership"]["verified"] is True


@requires_fixed_map
def test_peek_decodes_multiple_ranges_and_formats(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "peek", *target_flags(game),
                     "--read", f"0x{gf.CURRENT_XYZ:08X}:12",
                     "--read", f"0x{gf.LEVEL_ADDRESS:08X}:4",
                     "--format", "i32")
        assert result.returncode == 0, result.stderr
        reads = payload(result)["reads"]
        assert reads[0]["value"] == [501696, 30092, 494016]
        assert reads[1]["value"] == 0


@requires_fixed_map
def test_state_reports_the_known_live_block(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "state", *target_flags(game), "--triples")
        assert result.returncode == 0, result.stderr
        state = payload(result)["state"]
        assert (state["x"], state["y"], state["z"]) == (501696, 30092, 494016)
        assert state["next_life"] == 0
        assert state["collision_index"] == 572
        assert state["collision_material"] == 1
        assert state["triples"]["auxiliary"] == [500000, 30000, 493000]


@requires_fixed_map
def test_watch_writes_jsonl_samples(tmp_path: Path) -> None:
    out = tmp_path / "samples.jsonl"
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "watch", *target_flags(game),
                     "--read", f"0x{gf.SCRATCH_ADDRESS:08X}:4",
                     "--interval-ms", "10", "--duration-s", "0.3",
                     "--out", str(out))
        assert result.returncode == 0, result.stderr
        summary = payload(result)
        assert summary["samples"] >= 2
        rows = [json.loads(line) for line in out.read_text().splitlines()]
        assert rows and rows[0]["reads"][0]["hex"] == "deadbeef"


@requires_fixed_map
def test_watch_can_stop_on_the_first_change(tmp_path: Path) -> None:
    out = tmp_path / "samples.jsonl"
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        memory = sl.ProcessMemory(game.pid)

        def mutate() -> None:
            time.sleep(0.15)
            memory.write_many(((gf.SCRATCH_ADDRESS, bytes.fromhex("01010101")),))

        import threading
        thread = threading.Thread(target=mutate)
        thread.start()
        result = run(tmp_path, "watch", *target_flags(game),
                     "--read", f"0x{gf.SCRATCH_ADDRESS:08X}:4",
                     "--interval-ms", "10", "--duration-s", "5",
                     "--until-change", "--out", str(out))
        thread.join()
        assert result.returncode == 0, result.stderr
        summary = payload(result)
        assert summary["changes"] == 1
        assert summary["duration_s"] < 4


# --------------------------------------------------------------------------
# Identity refusals
# --------------------------------------------------------------------------


@requires_fixed_map
def test_unexpected_executable_hash_is_refused(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "peek", "--pid", str(game.pid), "--loader-re", ".*",
                     "--read", f"0x{gf.SCRATCH_ADDRESS:08X}:4")
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "unexpected_executable"


@requires_fixed_map
def test_expected_sha_mismatch_is_refused(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "peek", "--pid", str(game.pid), "--loader-re", ".*",
                     "--expected-sha", "0" * 64,
                     "--read", f"0x{gf.SCRATCH_ADDRESS:08X}:4")
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "sha_mismatch"


def test_absent_pid_is_refused(tmp_path: Path) -> None:
    result = run(tmp_path, "peek", "--pid", "999999999", "--loader-re", ".*",
                 "--read", "0x1000:4")
    assert result.returncode == ev.EXIT_REFUSAL
    assert payload(result)["reason"] in {"no_such_pid", "no_such_pid"}


@requires_fixed_map
def test_recycled_pid_in_a_session_is_refused(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        manifest = sl.SessionManifest(
            session_id="RUN-SESSION-20260817-120000",
            created_at="2026-08-17T12:00:00-04:00",
            game_pid=game.pid,
            game_start_ticks=sl.pid_identity(game.pid)[1] + 5,
            process_group=os.getpgid(game.pid),
        )
        manifest.save(root=tmp_path)
        result = run(tmp_path, "peek", "--session", manifest.session_id,
                     "--loader-re", ".*", "--accept-sha", game.exe_sha256,
                     "--read", f"0x{gf.SCRATCH_ADDRESS:08X}:4")
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "pid_recycled"


# --------------------------------------------------------------------------
# poke
# --------------------------------------------------------------------------


@requires_fixed_map
def test_poke_requires_a_guard(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "poke", *target_flags(game),
                     "--addr", f"0x{gf.SCRATCH_ADDRESS:08X}",
                     "--bytes", "01020304", "--authorize", "test")
        assert result.returncode == ev.EXIT_USAGE
        assert "--expect-current" in result.stderr


@requires_fixed_map
def test_poke_refuses_when_the_guard_does_not_match(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "poke", *target_flags(game),
                     "--addr", f"0x{gf.SCRATCH_ADDRESS:08X}",
                     "--bytes", "01020304", "--expect-current", "aabbccdd",
                     "--authorize", "test")
        assert result.returncode == ev.EXIT_REFUSAL
        data = payload(result)
        assert data["reason"] == "guard_mismatch"
        assert data["written"] is False
        # The refusal itself is retained as evidence.
        assert receipts(tmp_path)
        # And the target is untouched.
        memory = sl.ProcessMemory(game.pid)
        assert memory.read(gf.SCRATCH_ADDRESS, 4).hex() == "deadbeef"


@requires_fixed_map
def test_poke_dry_run_writes_nothing(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "poke", *target_flags(game),
                     "--addr", f"0x{gf.SCRATCH_ADDRESS:08X}",
                     "--bytes", "01020304", "--expect-current", "deadbeef",
                     "--authorize", "test", "--dry-run")
        assert result.returncode == 0, result.stderr
        assert payload(result)["written"] is False
        memory = sl.ProcessMemory(game.pid)
        assert memory.read(gf.SCRATCH_ADDRESS, 4).hex() == "deadbeef"


@requires_fixed_map
def test_poke_writes_verifies_and_receipts(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "poke", *target_flags(game),
                     "--addr", f"0x{gf.MIRROR_SRC_ADDRESS:08X}",
                     "--bytes", "0a0b0c0d", "--expect-current", "00000000",
                     "--authorize", "EXP-TEST user approval", "--purpose", "regression")
        assert result.returncode == 0, result.stderr
        data = payload(result)
        assert data["written"] is True and data["verified"] is True
        assert data["authorization"] == "EXP-TEST user approval"

        written = receipts(tmp_path)
        assert len(written) == 1
        receipt = json.loads(written[0].read_text())
        assert receipt["before_hex"] == "00000000"
        assert receipt["after_hex"] == "0a0b0c0d"
        assert receipt["target"]["ownership"]["exe_sha256"] == game.exe_sha256

        # The target's own loop mirrors src->dst, proving the write landed in
        # the target rather than only in our readback.
        memory = sl.ProcessMemory(game.pid)
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if memory.read(gf.MIRROR_DST_ADDRESS, 4).hex() == "0a0b0c0d":
                break
            time.sleep(0.05)
        assert memory.read(gf.MIRROR_DST_ADDRESS, 4).hex() == "0a0b0c0d"


@requires_fixed_map
def test_poke_rejects_a_guard_of_the_wrong_length(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "poke", *target_flags(game),
                     "--addr", f"0x{gf.SCRATCH_ADDRESS:08X}",
                     "--bytes", "01020304", "--expect-current", "dead",
                     "--authorize", "test")
        assert result.returncode == ev.EXIT_USAGE


@requires_fixed_map
def test_poke_rejects_an_empty_authorization(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "poke", *target_flags(game),
                     "--addr", f"0x{gf.SCRATCH_ADDRESS:08X}",
                     "--bytes", "01020304", "--expect-current", "deadbeef",
                     "--authorize", "   ")
        assert result.returncode == ev.EXIT_USAGE


@requires_fixed_map
def test_poke_rejects_an_oversized_payload(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        oversized = "00" * (sl.MAX_WRITE_BYTES + 1)
        result = run(tmp_path, "poke", *target_flags(game),
                     "--addr", f"0x{gf.SCRATCH_ADDRESS:08X}",
                     "--bytes", oversized, "--no-expect", "--authorize", "test")
        assert result.returncode == ev.EXIT_USAGE


# --------------------------------------------------------------------------
# teleport
# --------------------------------------------------------------------------


def _teleport_args(game: gf.FakeGame, *extra: str) -> list[str]:
    return [
        "teleport", *target_flags(game),
        "--x", "501696", "--y", "30092", "--z", "494016",
        "--authorize", "user approved 2026-08-17",
        "--destination-evidence", "EXP-20260815-130 accepted walkable point",
        "--settle-samples", "2", "--settle-interval-ms", "20", *extra,
    ]


@requires_fixed_map
def test_teleport_requires_destination_evidence(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        args = [
            "teleport", *target_flags(game),
            "--x", "1", "--y", "2", "--z", "3",
            "--authorize", "user approved",
            "--destination-evidence", "  ",
        ]
        result = run(tmp_path, *args)
        assert result.returncode == ev.EXIT_USAGE
        assert "walkable" in result.stderr


@requires_fixed_map
def test_teleport_dry_run_writes_nothing(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, *_teleport_args(game, "--dry-run"))
        assert result.returncode == 0, result.stderr
        data = payload(result)
        assert data["dry_run"] is True
        assert "readback" not in data
        memory = sl.ProcessMemory(game.pid)
        assert struct.unpack("<iii", memory.read(gf.PRECEDING_XYZ, 12)) == (
            501000, 30092, 494000
        )


@requires_fixed_map
def test_teleport_writes_current_and_preceding_only(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, *_teleport_args(game))
        assert result.returncode == 0, result.stderr
        data = payload(result)
        assert data["write_bytes"] == 24
        assert data["write_vectors"] == 2
        # The dword between the two triples is not part of either and must
        # survive the relocation untouched.
        assert data["unknown_dword_preserved"] is True
        assert data["auxiliary_written"] is False
        assert data["accepted"] is True
        assert data["readback"]["current"] == [501696, 30092, 494016]
        assert data["readback"]["preceding"] == [501696, 30092, 494016]
        # Auxiliary is deliberately not part of the routine relocation.
        assert data["readback"]["auxiliary"] == [500000, 30000, 493000]
        assert data["write_assisted"] is True

        receipt = json.loads(receipts(tmp_path)[0].read_text())
        assert receipt["written_addresses"] == ["0x0059D910", "0x0059D920"]
        assert receipt["destination_evidence"].startswith("EXP-20260815-130")
        assert len(receipt["settle"]) == 2


@requires_fixed_map
def test_teleport_reports_a_reset_loop_as_tool_negative(tmp_path: Path) -> None:
    """A nonzero NextLife after settling is the EXP-20260815-130 signature."""

    initial = gf.default_initial_state()
    initial[str(gf.NEXT_LIFE_ADDRESS)] = struct.pack("<H", 2).hex()
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        memory = sl.ProcessMemory(game.pid)
        memory.write_many(((gf.NEXT_LIFE_ADDRESS, struct.pack("<H", 2)),))
        result = run(tmp_path, *_teleport_args(game))
        assert result.returncode == ev.EXIT_TOOL_NEGATIVE
        data = payload(result)
        assert data["accepted"] is False
        assert data["next_life_after_settle"] == 2
        assert "reset" in data["caution"]


# --------------------------------------------------------------------------
# snapshot / restore (region state checkpoints)
# --------------------------------------------------------------------------


def test_capabilities_declares_the_checkpoint_contract(tmp_path: Path) -> None:
    caps = payload(run(tmp_path, "--capabilities"))
    assert "snapshot" in caps["read_verbs"]
    assert "restore" in caps["write_verbs"]
    assert caps["checkpoint"]["kind"] == "region-state-checkpoint"
    assert "same-process" in caps["checkpoint"]["not_a_savestate"].lower()
    assert "CRIU" in caps["checkpoint"]["durable_savestate_path"]


@requires_fixed_map
def test_snapshot_captures_a_region_and_writes_a_header(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "snapshot", "--name", "save1", "--no-data",
                     "--region", FIXTURE_REGION, *target_flags(game))
        assert result.returncode == 0, result.stdout + result.stderr
        data = payload(result)
        assert data["internal_level"] == 0
        assert data["regions"][0]["size"] == 4096
        snapdir = tmp_path / "work" / "snapshots" / "save1"
        header = json.loads((snapdir / "snapshot.json").read_text())
        assert header["schema_version"] == 1
        assert header["exe_sha256"] == game.exe_sha256
        assert header["pid"] == game.pid
        assert header["froze_process"] is True
        assert (snapdir / header["regions"][0]["file"]).stat().st_size == 4096


@requires_fixed_map
def test_snapshot_restore_round_trip_is_visible_to_the_game(tmp_path: Path) -> None:
    """The game mirrors src->dst each loop, so a restored value that the game
    re-propagates proves the restore landed in the game's own memory."""

    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        memory = sl.ProcessMemory(game.pid)
        run(tmp_path, "snapshot", "--name", "save1", "--no-data",
            "--region", FIXTURE_REGION, *target_flags(game))

        # Mutate the captured region; the game mirrors it forward.
        memory.write_many(((gf.MIRROR_SRC_ADDRESS, bytes.fromhex("ffffffff")),))
        time.sleep(0.2)
        assert memory.read(gf.MIRROR_DST_ADDRESS, 4).hex() == "ffffffff"

        snapdir = tmp_path / "work" / "snapshots" / "save1"
        result = run(tmp_path, "restore", "--snapshot", str(snapdir),
                     "--authorize", "test approval", *target_flags(game))
        assert result.returncode == 0, result.stdout + result.stderr
        data = payload(result)
        assert data["verified"] is True
        assert data["same_process"] is True
        assert data["level_changed"] is False

        assert memory.read(gf.MIRROR_SRC_ADDRESS, 4).hex() == "00000000"
        time.sleep(0.2)
        # The running game re-mirrored the restored value.
        assert memory.read(gf.MIRROR_DST_ADDRESS, 4).hex() == "00000000"
        assert restore_receipts(tmp_path)


@requires_fixed_map
def test_snapshot_can_be_taken_without_freezing(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "snapshot", "--name", "nf", "--no-data",
                     "--no-freeze", "--region", FIXTURE_REGION, *target_flags(game))
        assert result.returncode == 0, result.stderr
        header = json.loads(
            (tmp_path / "work" / "snapshots" / "nf" / "snapshot.json").read_text()
        )
        assert header["froze_process"] is False


@requires_fixed_map
def test_default_data_region_refuses_when_unmapped(tmp_path: Path) -> None:
    """The fixture does not map the low part of .data, proving the region
    mapping guard refuses rather than reading garbage."""

    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "snapshot", "--name", "d", *target_flags(game))
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "region_unmapped"


@requires_fixed_map
def test_snapshot_refuses_a_non_ignored_directory(tmp_path: Path) -> None:
    """Snapshots contain game bytes and must not be committable."""

    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text("# nothing ignored\n", encoding="utf-8")
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        result = run(tmp_path, "snapshot", "--name", "s", "--no-data",
                     "--region", FIXTURE_REGION, *target_flags(game))
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "snapshot_dir_not_ignored"


@requires_fixed_map
def test_snapshot_refuses_a_duplicate_name(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        args = ["snapshot", "--name", "dup", "--no-data",
                "--region", FIXTURE_REGION, *target_flags(game)]
        assert run(tmp_path, *args).returncode == 0
        result = run(tmp_path, *args)
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "snapshot_exists"


@requires_fixed_map
def test_restore_requires_authorization(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        run(tmp_path, "snapshot", "--name", "s", "--no-data",
            "--region", FIXTURE_REGION, *target_flags(game))
        snapdir = tmp_path / "work" / "snapshots" / "s"
        result = run(tmp_path, "restore", "--snapshot", str(snapdir),
                     "--authorize", "   ", *target_flags(game))
        assert result.returncode == ev.EXIT_USAGE


@requires_fixed_map
def test_restore_dry_run_writes_nothing(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        memory = sl.ProcessMemory(game.pid)
        run(tmp_path, "snapshot", "--name", "s", "--no-data",
            "--region", FIXTURE_REGION, *target_flags(game))
        memory.write_many(((gf.MIRROR_SRC_ADDRESS, bytes.fromhex("abababab")),))
        snapdir = tmp_path / "work" / "snapshots" / "s"
        result = run(tmp_path, "restore", "--snapshot", str(snapdir),
                     "--authorize", "test", "--dry-run", *target_flags(game))
        assert result.returncode == 0, result.stderr
        assert payload(result)["dry_run"] is True
        assert memory.read(gf.MIRROR_SRC_ADDRESS, 4).hex() == "abababab"


@requires_fixed_map
def test_restore_refuses_a_corrupt_snapshot(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        run(tmp_path, "snapshot", "--name", "s", "--no-data",
            "--region", FIXTURE_REGION, *target_flags(game))
        snapdir = tmp_path / "work" / "snapshots" / "s"
        header = json.loads((snapdir / "snapshot.json").read_text())
        # Tamper with a non-zero fill so the hash cannot coincide with the
        # (mostly zero-filled) captured region.
        (snapdir / header["regions"][0]["file"]).write_bytes(b"\x5a" * 4096)
        result = run(tmp_path, "restore", "--snapshot", str(snapdir),
                     "--authorize", "test", *target_flags(game))
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "snapshot_corrupt"


@requires_fixed_map
def test_restore_refuses_an_executable_mismatch(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        run(tmp_path, "snapshot", "--name", "s", "--no-data",
            "--region", FIXTURE_REGION, *target_flags(game))
        snapdir = tmp_path / "work" / "snapshots" / "s"
        header = json.loads((snapdir / "snapshot.json").read_text())
        header["exe_sha256"] = "0" * 64
        (snapdir / "snapshot.json").write_text(json.dumps(header))
        result = run(tmp_path, "restore", "--snapshot", str(snapdir),
                     "--authorize", "test", *target_flags(game))
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "executable_mismatch"


@requires_fixed_map
def test_restore_refuses_a_level_change(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, lifetime_s=60) as game:
        memory = sl.ProcessMemory(game.pid)
        run(tmp_path, "snapshot", "--name", "s", "--no-data",
            "--region", FIXTURE_REGION, *target_flags(game))
        # Simulate a level change since capture.
        memory.write_many(((sl.LEVEL_ADDRESS, struct.pack("<i", 7)),))
        snapdir = tmp_path / "work" / "snapshots" / "s"
        result = run(tmp_path, "restore", "--snapshot", str(snapdir),
                     "--authorize", "test", *target_flags(game))
        assert result.returncode == ev.EXIT_REFUSAL
        assert payload(result)["reason"] == "level_changed"
        # And it proceeds when the override is disclosed.
        ok = run(tmp_path, "restore", "--snapshot", str(snapdir),
                 "--authorize", "test", "--allow-level-change", *target_flags(game))
        assert ok.returncode == 0, ok.stderr
        assert payload(ok)["level_changed"] is True


@requires_fixed_map
def test_restore_refuses_a_different_process(tmp_path: Path) -> None:
    git_sandbox(tmp_path)
    with gf.FakeGame(tmp_path, name="a", lifetime_s=60) as game_a:
        run(tmp_path, "snapshot", "--name", "s", "--no-data",
            "--region", FIXTURE_REGION, *target_flags(game_a))
        snapdir = tmp_path / "work" / "snapshots" / "s"
        with gf.FakeGame(tmp_path, name="b", lifetime_s=60) as game_b:
            result = run(tmp_path, "restore", "--snapshot", str(snapdir),
                         "--authorize", "test", *target_flags(game_b))
            assert result.returncode == ev.EXIT_REFUSAL
            assert payload(result)["reason"] == "different_process"
            # Disclosed override is accepted (both fixtures map the same window).
            ok = run(tmp_path, "restore", "--snapshot", str(snapdir),
                     "--authorize", "test", "--allow-different-process",
                     *target_flags(game_b))
            assert ok.returncode == 0, ok.stderr
            assert payload(ok)["same_process"] is False
