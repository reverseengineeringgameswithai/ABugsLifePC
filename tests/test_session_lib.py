"""Synthetic regressions for the shared session-control foundation."""

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


requires_fixed_map = pytest.mark.skipif(
    not gf.have_fixed_mapping(),
    reason="the fixture's fixed address window is not mappable on this host",
)


# --------------------------------------------------------------------------
# /proc parsing
# --------------------------------------------------------------------------


def test_parse_proc_stat_extracts_group_and_start_ticks() -> None:
    fields = " ".join(str(index) for index in range(3, 53))
    group, ticks = sl.parse_proc_stat(f"42 (python3) {fields}")
    assert (group, ticks) == (5, 22)


def test_parse_proc_stat_tolerates_parentheses_in_comm() -> None:
    fields = " ".join(str(index) for index in range(3, 53))
    group, ticks = sl.parse_proc_stat(f"42 (weird (name) here) {fields}")
    assert (group, ticks) == (5, 22)


@pytest.mark.parametrize("text", ["no terminator", "42 (short) S 1 2"])
def test_parse_proc_stat_rejects_malformed(text: str) -> None:
    with pytest.raises(ValueError):
        sl.parse_proc_stat(text)


def test_process_records_includes_this_process() -> None:
    records = {record.pid: record for record in sl.process_records()}
    assert os.getpid() in records
    assert records[os.getpid()].process_group == os.getpgid(0)


def test_pid_matches_identity_detects_a_different_process() -> None:
    assert sl.pid_matches_identity(os.getpid(), sl.pid_identity(os.getpid())[1])
    assert not sl.pid_matches_identity(os.getpid(), 999_999_999)


# --------------------------------------------------------------------------
# Nested display resolution
# --------------------------------------------------------------------------


def _record(pid: int, group: int, command: tuple[str, ...]) -> sl.ProcessRecord:
    return sl.ProcessRecord(pid=pid, process_group=group, start_ticks=1, command=command)


def test_nested_display_binds_to_the_owned_group_only() -> None:
    records = (
        _record(10, 10, ("/usr/bin/Xwayland", ":2", "-rootless")),
        _record(20, 20, ("/usr/bin/Xwayland", ":3", "-rootless")),
    )
    assert sl.nested_display(records, 20) == ":3"
    assert sl.nested_display(records, 30) is None


def test_nested_display_refuses_two_displays_in_one_group() -> None:
    records = (
        _record(10, 10, ("Xwayland", ":2")),
        _record(11, 10, ("Xwayland", ":3")),
    )
    with pytest.raises(sl.SessionError) as excinfo:
        sl.nested_display(records, 10)
    assert excinfo.value.reason == "ambiguous_display"


# --------------------------------------------------------------------------
# Renderer log gate
# --------------------------------------------------------------------------


def _hardware_log(extra: tuple[str, ...] = ()) -> str:
    return "\n".join(("start",) + gf.HARDWARE_MARKERS + extra)


def test_renderer_gate_accepts_all_six_markers() -> None:
    gate = sl.evaluate_renderer_log(_hardware_log())
    assert gate.accepted
    assert set(gate.markers_found) == set(sl.HARDWARE_MARKERS)
    assert gate.markers_missing == ()


@pytest.mark.parametrize("dropped", range(len(sl.HARDWARE_MARKERS)))
def test_renderer_gate_requires_every_marker(dropped: int) -> None:
    kept = tuple(m for i, m in enumerate(sl.HARDWARE_MARKERS) if i != dropped)
    gate = sl.evaluate_renderer_log("\n".join(kept))
    assert not gate.accepted
    assert gate.markers_missing == (sl.HARDWARE_MARKERS[dropped],)


@pytest.mark.parametrize("marker", [
    "INITSOFTRENDER",
    "OnlySystemMemory status SYSTEM MEMORY ONLY",
    "Native software render mode is TRUE",
    "Screen mode 320x200x8 selected",
])
def test_renderer_gate_rejects_software_markers(marker: str) -> None:
    gate = sl.evaluate_renderer_log(_hardware_log((marker,)))
    assert not gate.accepted
    assert gate.rejects_found


def test_renderer_gate_ignores_ddmode_enumeration_lines() -> None:
    """DDMODE lines list available modes; they are not the selected mode."""

    gate = sl.evaluate_renderer_log(_hardware_log((
        "DDMODE : 320x200x8",
        "DDMODE : 320x200x16",
        "DDMODE : 640x480x16",
    )))
    assert gate.accepted
    assert gate.rejects_found == ()


def test_renderer_gate_on_empty_log_is_not_accepted() -> None:
    gate = sl.evaluate_renderer_log("")
    assert not gate.accepted
    assert len(gate.markers_missing) == len(sl.HARDWARE_MARKERS)


# --------------------------------------------------------------------------
# Log reading
# --------------------------------------------------------------------------


def test_read_log_text_returns_only_new_bytes(tmp_path: Path) -> None:
    log = tmp_path / "bugs.log"
    log.write_text("first\n", encoding="utf-8")
    text, offset = sl.read_log_text(log)
    assert text == "first\n" and offset == 6
    log.write_text("first\nsecond\n", encoding="utf-8")
    text, offset = sl.read_log_text(log, from_offset=offset)
    assert text == "second\n" and offset == 13


def test_read_log_text_restarts_after_truncation(tmp_path: Path) -> None:
    """The game recreates bugs.log on each log-argument launch."""

    log = tmp_path / "bugs.log"
    log.write_text("a" * 100, encoding="utf-8")
    log.write_text("new run\n", encoding="utf-8")
    text, offset = sl.read_log_text(log, from_offset=100)
    assert text == "new run\n"
    assert offset == 8


def test_read_log_text_refuses_missing_file(tmp_path: Path) -> None:
    with pytest.raises(sl.SessionError) as excinfo:
        sl.read_log_text(tmp_path / "absent.log")
    assert excinfo.value.reason == "log_unreadable"


# --------------------------------------------------------------------------
# Process memory
# --------------------------------------------------------------------------


@requires_fixed_map
def test_memory_reads_known_globals(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=30) as game:
        memory = sl.ProcessMemory(game.pid)
        assert sl.read_internal_level(memory) == 0
        assert sl.read_carousel_position(memory) == 0
        current = memory.read(gf.CURRENT_XYZ, 12)
        assert struct.unpack("<iii", current) == (501696, 30092, 494016)


@requires_fixed_map
def test_memory_write_is_visible_to_the_target_itself(tmp_path: Path) -> None:
    """The target mirrors src->dst each loop, so a changed dst proves the
    write landed in the target's own view rather than only in our readback."""

    with gf.FakeGame(tmp_path, lifetime_s=30) as game:
        memory = sl.ProcessMemory(game.pid)
        memory.write_many(((gf.MIRROR_SRC_ADDRESS, bytes.fromhex("0a0b0c0d")),))
        deadline = time.monotonic() + 5
        mirrored = b""
        while time.monotonic() < deadline:
            mirrored = memory.read(gf.MIRROR_DST_ADDRESS, 4)
            if mirrored == bytes.fromhex("0a0b0c0d"):
                break
            time.sleep(0.05)
        assert mirrored == bytes.fromhex("0a0b0c0d")


@requires_fixed_map
def test_memory_read_many_batches_ranges(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=30) as game:
        memory = sl.ProcessMemory(game.pid)
        payloads = memory.read_many((
            (gf.LEVEL_ADDRESS, 4), (gf.SCRATCH_ADDRESS, 4), (gf.CURRENT_XYZ, 12)
        ))
        assert len(payloads) == 3
        assert payloads[1].hex() == "deadbeef"


def test_memory_rejects_invalid_plans() -> None:
    memory = sl.ProcessMemory.__new__(sl.ProcessMemory)
    with pytest.raises(sl.SessionError):
        sl.ProcessMemory._check_plan(())
    with pytest.raises(sl.SessionError):
        sl.ProcessMemory._check_plan(tuple((0x1000, 1) for _ in range(33)))
    with pytest.raises(sl.SessionError):
        sl.ProcessMemory._check_plan(((0, 4),))
    with pytest.raises(sl.SessionError):
        sl.ProcessMemory._check_plan(((0x1000, sl.MAX_MEMORY_RANGE_BYTES + 1),))
    assert memory is not None


@requires_fixed_map
def test_memory_write_refuses_oversized_payload(tmp_path: Path) -> None:
    with gf.FakeGame(tmp_path, lifetime_s=30) as game:
        memory = sl.ProcessMemory(game.pid)
        with pytest.raises(sl.SessionError) as excinfo:
            memory.write_many(((gf.SCRATCH_ADDRESS, b"\x00" * (sl.MAX_WRITE_BYTES + 1)),))
        assert excinfo.value.reason == "write_too_large"


def test_memory_rejects_nonpositive_pid() -> None:
    with pytest.raises(sl.SessionError):
        sl.ProcessMemory(0)


# --------------------------------------------------------------------------
# Level roster
# --------------------------------------------------------------------------


def test_level_by_name_uses_the_static_table() -> None:
    assert sl.level_by_name("Tunnels") == (2, "Tunnels", 3)
    assert sl.level_by_name("city entrance") == (7, "City Entrance", 4)


def test_level_by_name_refuses_unknown_level() -> None:
    with pytest.raises(sl.SessionError) as excinfo:
        sl.level_by_name("Nonexistent Level")
    assert excinfo.value.reason == "unknown_level"


def test_level_table_matches_the_recorded_static_derivation() -> None:
    expected = (17, 1, 3, 2, 6, 10, 11, 4, 5, 14, 7, 12, 13, 9, 8, 15)
    assert tuple(internal for _, _, internal in sl.LEVEL_TABLE) == expected


# --------------------------------------------------------------------------
# xdotool wrapper
# --------------------------------------------------------------------------


class _Runner:
    def __init__(self, responses: dict[str, str] | None = None, focus: str = "") -> None:
        self.calls: list[list[str]] = []
        self.responses = responses or {}
        self.focus = focus

    def __call__(self, argv, env):
        self.calls.append(argv)
        verb = argv[1] if len(argv) > 1 else ""
        stdout = self.responses.get(verb, self.focus if verb == "getwindowfocus" else "")
        return subprocess.CompletedProcess(argv, 0, stdout, "")


def test_send_key_holds_and_never_uses_window_targeted_delivery() -> None:
    runner = _Runner(focus="777")
    xdo = sl.XDo(":9", runner=runner)
    slept: list[float] = []
    receipt = xdo.send_key(777, "Down", hold_ms=180, sleep=slept.append)

    assert receipt["method"] == "xtest"
    assert slept == [0.18]
    verbs = [call[1] for call in runner.calls]
    assert verbs == ["windowactivate", "windowfocus", "getwindowfocus", "keydown", "keyup"]
    assert not any("--window" in call for call in runner.calls if call[1] in {"keydown", "keyup"})


def test_send_key_refuses_when_focus_is_elsewhere() -> None:
    xdo = sl.XDo(":9", runner=_Runner(focus="999"))
    with pytest.raises(sl.SessionError) as excinfo:
        xdo.send_key(777, "Down", sleep=lambda _: None)
    assert excinfo.value.reason == "focus_lost"


def test_send_key_releases_the_key_even_when_the_wait_fails() -> None:
    runner = _Runner(focus="777")
    xdo = sl.XDo(":9", runner=runner)

    def boom(_seconds: float) -> None:
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        xdo.send_key(777, "Down", sleep=boom)
    assert [call[1] for call in runner.calls][-1] == "keyup"


@pytest.mark.parametrize("keysym", ["", "a b", "Down;rm -rf /", "x" * 40])
def test_send_key_rejects_invalid_keysyms(keysym: str) -> None:
    xdo = sl.XDo(":9", runner=_Runner())
    with pytest.raises(sl.SessionError) as excinfo:
        xdo.send_key(1, keysym, sleep=lambda _: None)
    assert excinfo.value.reason == "invalid_keysym"


@pytest.mark.parametrize("hold", [0, -5, sl.MAX_KEY_HOLD_MS + 1])
def test_send_key_rejects_out_of_range_holds(hold: int) -> None:
    xdo = sl.XDo(":9", runner=_Runner())
    with pytest.raises(sl.SessionError) as excinfo:
        xdo.send_key(1, "Down", hold_ms=hold, sleep=lambda _: None)
    assert excinfo.value.reason == "invalid_hold"


def test_xdo_rejects_a_malformed_display() -> None:
    with pytest.raises(sl.SessionError):
        sl.XDo("not-a-display")


def test_geometry_parses_shell_output() -> None:
    runner = _Runner({"getwindowgeometry": "WINDOW=1\nX=0\nY=0\nWIDTH=640\nHEIGHT=480"})
    assert sl.XDo(":9", runner=runner).geometry(1) == (640, 480)


def test_geometry_refuses_incomplete_output() -> None:
    runner = _Runner({"getwindowgeometry": "WINDOW=1\nX=0"})
    with pytest.raises(sl.SessionError) as excinfo:
        sl.XDo(":9", runner=runner).geometry(1)
    assert excinfo.value.reason == "geometry_incomplete"


# --------------------------------------------------------------------------
# Runtime audit
# --------------------------------------------------------------------------


def test_audit_runtime_separates_owned_from_unattributed() -> None:
    records = (
        _record(1, 100, ("/usr/bin/gamescope", "--backend", "wayland")),
        _record(2, 100, ("/usr/bin/wine", "bugs.exe")),
        _record(3, 200, ("/usr/lib64/wine/winedevice.exe",)),
        _record(4, 300, ("/usr/bin/bash",)),
    )
    audit = sl.audit_runtime(records, owned_groups=(100,))
    assert audit["owned_count"] == 1
    assert audit["unattributed_count"] == 1
    names = {row["name"] for row in audit["processes"]}
    assert "gamescope" in names and "winedevice.exe" in names
    assert "bash" not in names


def test_audit_runtime_matches_windows_style_command_names() -> None:
    records = (_record(9, 1, (r"C:\\windows\\system32\\winedevice.exe",)),)
    audit = sl.audit_runtime(records)
    assert audit["unattributed_count"] == 1


# --------------------------------------------------------------------------
# Session manifest
# --------------------------------------------------------------------------


def _manifest(session_id: str = "RUN-SESSION-20260817-120000", **kwargs) -> sl.SessionManifest:
    defaults = dict(
        created_at="2026-08-17T12:00:00-04:00",
        process_group=4242,
        game_pid=4243,
        game_start_ticks=99,
        display=":9",
        window_id=777,
        game_dir="/tmp/game",
    )
    defaults.update(kwargs)
    return sl.SessionManifest(session_id=session_id, **defaults)


def test_manifest_round_trips(tmp_path: Path) -> None:
    manifest = _manifest()
    manifest.save(root=tmp_path)
    loaded = sl.load_session(manifest.session_id, root=tmp_path)
    assert loaded.to_dict() == manifest.to_dict()


def test_manifest_refuses_a_foreign_schema(tmp_path: Path) -> None:
    manifest = _manifest()
    path = manifest.path(root=tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = manifest.to_dict() | {"schema_version": 99}
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(sl.SessionError) as excinfo:
        sl.load_session(manifest.session_id, root=tmp_path)
    assert excinfo.value.reason == "manifest_schema"


def test_manifest_refuses_malformed_json(tmp_path: Path) -> None:
    directory = tmp_path / ev.RUN_ROOT / "RUN-SESSION-20260817-120000"
    directory.mkdir(parents=True)
    (directory / "session.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(sl.SessionError) as excinfo:
        sl.load_session("RUN-SESSION-20260817-120000", root=tmp_path)
    assert excinfo.value.reason == "manifest_malformed"


@pytest.mark.parametrize("bad", ["", "RUN-GDB-20260817-120000", "../escape", "RUN-SESSION-x"])
def test_session_dir_refuses_malformed_ids(bad: str) -> None:
    with pytest.raises(sl.SessionError) as excinfo:
        sl.session_dir(bad)
    assert excinfo.value.reason == "invalid_session_id"


def test_missing_session_is_a_refusal(tmp_path: Path) -> None:
    with pytest.raises(sl.SessionError) as excinfo:
        sl.load_session("RUN-SESSION-20260817-120000", root=tmp_path)
    assert excinfo.value.reason == "session_not_found"


def test_iter_sessions_skips_unreadable_entries(tmp_path: Path) -> None:
    good = _manifest("RUN-SESSION-20260817-120000")
    good.save(root=tmp_path)
    bad = tmp_path / ev.RUN_ROOT / "RUN-SESSION-20260817-130000"
    bad.mkdir(parents=True)
    (bad / "session.json").write_text("{", encoding="utf-8")
    (tmp_path / ev.RUN_ROOT / "RUN-SESSION-20260817-140000").mkdir()
    found = sl.iter_sessions(root=tmp_path)
    assert [m.session_id for m in found] == ["RUN-SESSION-20260817-120000"]


def test_session_is_live_uses_start_ticks(tmp_path: Path) -> None:
    group, ticks = sl.pid_identity(os.getpid())
    live = _manifest(game_pid=os.getpid(), game_start_ticks=ticks)
    stale = _manifest("RUN-SESSION-20260817-130000",
                      game_pid=os.getpid(), game_start_ticks=ticks + 1)
    assert sl.session_is_live(live)
    assert not sl.session_is_live(stale)


def test_resolve_session_refuses_when_nothing_is_live(tmp_path: Path) -> None:
    with pytest.raises(sl.SessionError) as excinfo:
        sl.resolve_session(None, root=tmp_path)
    assert excinfo.value.reason == "no_live_session"


def test_resolve_session_refuses_ambiguity(tmp_path: Path) -> None:
    _, ticks = sl.pid_identity(os.getpid())
    for stamp in ("20260817-120000", "20260817-130000"):
        _manifest(f"RUN-SESSION-{stamp}", game_pid=os.getpid(),
                  game_start_ticks=ticks).save(root=tmp_path)
    with pytest.raises(sl.SessionError) as excinfo:
        sl.resolve_session(None, root=tmp_path)
    assert excinfo.value.reason == "ambiguous_session"


def test_resolve_session_returns_the_single_live_session(tmp_path: Path) -> None:
    _, ticks = sl.pid_identity(os.getpid())
    _manifest(game_pid=os.getpid(), game_start_ticks=ticks).save(root=tmp_path)
    _manifest("RUN-SESSION-20260817-130000", state="closed",
              game_pid=os.getpid(), game_start_ticks=ticks).save(root=tmp_path)
    resolved = sl.resolve_session(None, root=tmp_path)
    assert resolved.session_id == "RUN-SESSION-20260817-120000"


# --------------------------------------------------------------------------
# Window discovery
# --------------------------------------------------------------------------


@requires_fixed_map
def test_discover_game_target_finds_the_owned_window(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=30) as session:
        status = session.start()
        binary, _, _, _ = gf.write_stub_xdotool(
            tmp_path, window_id=777, game_pid=status["game_pid"]
        )
        target = sl.discover_game_target(
            status["process_group"], session.game_dir,
            accepted_sha256={session.exe_sha256},
            xdo_factory=lambda display: sl.XDo(display, executable=str(binary)),
            loader_re=".*",
        )
        assert target is not None
        assert target.display == ":9"
        assert target.pid == status["game_pid"]
        assert (target.width, target.height) == (640, 480)
        assert target.exe_sha256 == session.exe_sha256


@requires_fixed_map
@pytest.mark.parametrize("override", [
    {"window_class": "not-the-game"},
    {"width": 1280, "height": 960},
])
def test_discover_game_target_rejects_wrong_surfaces(tmp_path: Path, override: dict) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=30) as session:
        status = session.start()
        binary, state, _, _ = gf.write_stub_xdotool(
            tmp_path, window_id=777, game_pid=status["game_pid"]
        )
        gf.write_stub_state(state, window_id=777, game_pid=status["game_pid"], **override)
        target = sl.discover_game_target(
            status["process_group"], session.game_dir,
            accepted_sha256={session.exe_sha256},
            xdo_factory=lambda display: sl.XDo(display, executable=str(binary)),
            loader_re=".*",
        )
        assert target is None


@requires_fixed_map
def test_discover_game_target_rejects_an_unaccepted_executable(tmp_path: Path) -> None:
    with gf.FakeSession(tmp_path, lifetime_s=30) as session:
        status = session.start()
        binary, _, _, _ = gf.write_stub_xdotool(
            tmp_path, window_id=777, game_pid=status["game_pid"]
        )
        target = sl.discover_game_target(
            status["process_group"], session.game_dir,
            accepted_sha256={"0" * 64},
            xdo_factory=lambda display: sl.XDo(display, executable=str(binary)),
            loader_re=".*",
        )
        assert target is None


def test_discover_game_target_without_a_display_returns_none(tmp_path: Path) -> None:
    assert sl.discover_game_target(
        os.getpgid(0) + 999_999, tmp_path,
        process_reader=lambda: (), loader_re=".*",
    ) is None
