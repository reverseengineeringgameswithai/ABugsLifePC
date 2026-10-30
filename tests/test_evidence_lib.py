from __future__ import annotations

import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import time

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import evidence_lib as ev  # noqa: E402


# --------------------------------------------------------------------------
# hex / run-dir helpers
# --------------------------------------------------------------------------


def test_parse_hex_u64_accepts_prefixed_and_bare() -> None:
    assert ev.parse_hex_u64("0x10") == 16
    assert ev.parse_hex_u64("1a") == 26


@pytest.mark.parametrize("bad", ["", "zz", "0xg", "-1"])
def test_parse_hex_u64_rejects(bad: str) -> None:
    with pytest.raises(ValueError):
        ev.parse_hex_u64(bad)


def test_parse_hex_u64_rejects_over_64_bits() -> None:
    with pytest.raises(ValueError):
        ev.parse_hex_u64("1" + "0" * 16)  # 2**64


def test_new_run_dir_refuses_collision(tmp_path: Path) -> None:
    moment = ev.now()
    first = ev.new_run_dir("TEST", root=tmp_path, moment=moment)
    assert first.exists()
    assert first.parent == tmp_path / "dynamic" / "wine"
    with pytest.raises(FileExistsError):
        ev.new_run_dir("TEST", root=tmp_path, moment=moment)


def test_repo_root_honors_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ABLPC_ROOT", str(tmp_path))
    assert ev.repo_root() == tmp_path.resolve()


# --------------------------------------------------------------------------
# ownership proof (against real spawned python children — no ptrace)
# --------------------------------------------------------------------------


def _make_game(cwd: Path, content: bytes = b"game-bytes") -> str:
    exe = cwd / "bugs.exe"
    exe.write_bytes(content)
    return ev.sha256_file(exe)


def _await_cmdline(pid: int, basename: str, timeout: float = 5.0) -> None:
    # Wait for the child's execve to complete so /proc/<pid>/cmdline reflects
    # the intended argv (avoids a fork/exec race under load).
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            toks = ev._read_proc_cmdline(pid)
        except OSError:
            toks = ()
        if any(ev._win_unix_basename(t).lower() == basename.lower() for t in toks):
            return
        time.sleep(0.02)


def _spawn_game(cwd: Path, argv0: str = "bugs.exe") -> subprocess.Popen:
    # Run the real python interpreter but with argv[0] == the game basename, so
    # /proc/<pid>/cmdline carries it while /proc/<pid>/exe resolves to python
    # (loader check overridden in tests).
    proc = subprocess.Popen(
        [argv0, "-c", "import time; time.sleep(30)"],
        executable=sys.executable,
        cwd=str(cwd),
    )
    _await_cmdline(proc.pid, "bugs.exe")
    return proc


def test_ownership_pass(tmp_path: Path) -> None:
    copies = tmp_path / "work" / "copies" / "run"
    copies.mkdir(parents=True)
    sha = _make_game(copies)
    child = _spawn_game(copies)
    try:
        proof = ev.ownership_proof(
            child.pid,
            expected_sha256=sha,
            exe_basename="bugs.exe",
            loader_re=".*",
            cwd_prefix=str(copies) + os.sep,
        )
        assert proof.verified is True
        assert proof.exe_sha256 == sha
        assert proof.pid == child.pid
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_win_unix_basename() -> None:
    # Regression: the Wine game's cmdline carries a Windows path.
    assert ev._win_unix_basename("R:\\PC\\BUGS\\bugs.exe") == "bugs.exe"
    assert ev._win_unix_basename("/unix/path/bugs.exe") == "bugs.exe"
    assert ev._win_unix_basename("bugs.exe") == "bugs.exe"


def test_ownership_pass_windows_path_cmdline(tmp_path: Path) -> None:
    # Regression for the live-found bug: argv[0] is a Windows path with
    # backslashes, so os.path.basename would not have split it on Linux.
    copies = tmp_path / "work" / "copies" / "run"
    copies.mkdir(parents=True)
    sha = _make_game(copies)
    child = _spawn_game(copies, argv0="R:\\PC\\BUGS\\bugs.exe")
    try:
        proof = ev.ownership_proof(
            child.pid,
            expected_sha256=sha,
            exe_basename="bugs.exe",
            loader_re=".*",
            cwd_prefix=str(copies) + os.sep,
        )
        assert proof.verified is True
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_ownership_refuses_wrong_sha(tmp_path: Path) -> None:
    copies = tmp_path / "work" / "copies" / "run"
    copies.mkdir(parents=True)
    _make_game(copies)
    child = _spawn_game(copies)
    try:
        with pytest.raises(ev.OwnershipError) as exc:
            ev.ownership_proof(
                child.pid,
                expected_sha256="0" * 64,
                exe_basename="bugs.exe",
                loader_re=".*",
                cwd_prefix=str(copies) + os.sep,
            )
        assert exc.value.reason == "sha_mismatch"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_ownership_refuses_cwd_outside_copies(tmp_path: Path) -> None:
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    _make_game(outside)
    child = _spawn_game(outside)
    try:
        with pytest.raises(ev.OwnershipError) as exc:
            ev.ownership_proof(
                child.pid,
                exe_basename="bugs.exe",
                loader_re=".*",
                cwd_prefix=str(tmp_path / "work" / "copies") + os.sep,
            )
        assert exc.value.reason == "cwd_outside_copies"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_ownership_refuses_loader_mismatch(tmp_path: Path) -> None:
    copies = tmp_path / "work" / "copies" / "run"
    copies.mkdir(parents=True)
    _make_game(copies)
    child = _spawn_game(copies)
    try:
        with pytest.raises(ev.OwnershipError) as exc:
            ev.ownership_proof(
                child.pid,
                exe_basename="bugs.exe",
                loader_re=r"^/nonexistent/wine$",
                cwd_prefix=str(copies) + os.sep,
            )
        assert exc.value.reason == "loader_mismatch"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_ownership_cli_refusal_exit_code(tmp_path: Path) -> None:
    rc = ev.main([
        "ownership",
        "--pid", "1",
        "--loader-re", r"^/nonexistent/wine$",
    ])
    assert rc == ev.EXIT_REFUSAL


# --------------------------------------------------------------------------
# watch spec validation
# --------------------------------------------------------------------------


def _base_spec() -> dict:
    return {
        "schema_version": 1,
        "experiment_id": "EXP-20260812-999",
        "target": {"mode": "pid", "pid": 123},
        "watchpoints": [{"id": "w0", "address": "0x00400010", "kind": "read", "size": 4}],
        "breakpoints": [],
        "window": {"max_stops": 5, "timeout_seconds": 30, "end_milestones": ["NextLife"], "log_path": None},
        "on_stop": {"registers": ["rip"], "memory_reads": [], "backtrace_limit": 8},
    }


def test_valid_spec_normalizes() -> None:
    spec = ev.validate_watch_spec(_base_spec())
    assert spec.watchpoints[0].address == 0x00400010
    assert spec.watchpoints[0].kind == "read"
    assert spec.window["max_stops"] == 5
    assert spec.schema_version == 1
    assert spec.survival == {}


def test_v2_survival_spec_normalizes() -> None:
    raw = _base_spec()
    raw["schema_version"] = 2
    raw["survival"] = {"required": True, "settle_ms": 500}
    spec = ev.validate_watch_spec(raw)
    assert spec.schema_version == 2
    assert spec.survival == {
        "required": True,
        "settle_ms": 500,
        "sample_count": 3,
        "sample_interval_ms": 100,
        "require_untraced": True,
        "require_resumed": True,
    }


def test_v1_rejects_survival_block() -> None:
    raw = _base_spec()
    raw["survival"] = {"required": True}
    with pytest.raises(ev.SpecError, match="unknown keys"):
        ev.validate_watch_spec(raw)


def _submission_capture_block() -> dict:
    return {
        "interval_mode": "paired",
        "pre_trigger_id": "pre",
        "post_trigger_id": "post",
        "pre_stop_pc": "0x00400101",
        "post_stop_pc": "0x00400201",
        "entry_register": "rdi",
        "entry_root": "0x00600000",
        "entry_stride": 16,
        "entry_count": 4,
        "candidate_indices": [0, 1, 3],
        "counter_address": "0x00610000",
        "capacity_address": "0x00610004",
        "base_pointer_address": "0x00610008",
        "pointer_size": 8,
        "output_stride": 16,
        "max_records_per_entry": 4,
        "warmup_rollovers": 1,
        "capture_cycles": 1,
    }


def test_v3_submission_capture_normalizes() -> None:
    raw = _base_spec()
    raw["schema_version"] = 3
    raw["watchpoints"] = []
    raw["breakpoints"] = [
        {"id": "pre", "address": "0x00400100"},
        {"id": "post", "address": "0x00400200"},
    ]
    raw["submission_capture"] = _submission_capture_block()
    spec = ev.validate_watch_spec(raw)
    capture = spec.submission_capture
    assert capture is not None
    assert capture.interval_mode == "paired"
    assert capture.candidate_indices == (0, 1, 3)
    assert capture.entry_register == "rdi"
    assert capture.output_stride == 16
    assert capture.pre_stop_pc == 0x00400101


@pytest.mark.parametrize(
    ("key", "value", "match"),
    [
        ("pre_trigger_id", "missing", "configured hardware point"),
        ("pointer_size", 3, "pointer_size"),
        ("candidate_indices", [0, 4], "outside entry_count"),
        ("candidate_indices", [0, 0], "unique"),
        ("max_records_per_entry", 65537, "max_records_per_entry"),
        ("entry_count", True, "entry_count"),
    ],
)
def test_v3_rejects_invalid_submission_capture(
    key: str, value, match: str,
) -> None:
    raw = _base_spec()
    raw["schema_version"] = 3
    raw["watchpoints"] = []
    raw["breakpoints"] = [
        {"id": "pre", "address": "0x00400100"},
        {"id": "post", "address": "0x00400200"},
    ]
    raw["submission_capture"] = _submission_capture_block()
    raw["submission_capture"][key] = value
    with pytest.raises(ev.SpecError, match=match):
        ev.validate_watch_spec(raw)


def test_v3_rejects_oversized_submission_digest_span() -> None:
    raw = _base_spec()
    raw["schema_version"] = 3
    raw["watchpoints"] = []
    raw["breakpoints"] = [
        {"id": "pre", "address": "0x00400100"},
        {"id": "post", "address": "0x00400200"},
    ]
    raw["submission_capture"] = _submission_capture_block()
    raw["submission_capture"]["output_stride"] = 65536
    raw["submission_capture"]["max_records_per_entry"] = 17
    with pytest.raises(ev.SpecError, match="maximum digest span"):
        ev.validate_watch_spec(raw)


def test_v3_zero_post_allows_one_data_trigger() -> None:
    raw = _base_spec()
    raw["schema_version"] = 3
    raw["watchpoints"] = [
        {"id": "post", "address": "0x00610000", "kind": "access", "size": 4}
    ]
    raw["breakpoints"] = []
    raw["submission_capture"] = _submission_capture_block()
    raw["submission_capture"].update({
        "interval_mode": "zero_post",
        "pre_trigger_id": "post",
        "post_trigger_id": "post",
    })
    spec = ev.validate_watch_spec(raw)
    assert spec.submission_capture.interval_mode == "zero_post"
    assert spec.submission_capture.pre_trigger_id == "post"


def test_v3_zero_post_rejects_distinct_trigger_ids() -> None:
    raw = _base_spec()
    raw["schema_version"] = 3
    raw["watchpoints"] = []
    raw["breakpoints"] = [
        {"id": "pre", "address": "0x00400100"},
        {"id": "post", "address": "0x00400200"},
    ]
    raw["submission_capture"] = _submission_capture_block()
    raw["submission_capture"]["interval_mode"] = "zero_post"
    with pytest.raises(ev.SpecError, match="must use one trigger id"):
        ev.validate_watch_spec(raw)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("required", 1),
        ("settle_ms", -1),
        ("sample_count", 0),
        ("sample_interval_ms", 5001),
        ("require_untraced", "yes"),
        ("require_resumed", None),
    ],
)
def test_v2_rejects_invalid_survival_values(key: str, value) -> None:
    raw = _base_spec()
    raw["schema_version"] = 2
    raw["survival"] = {key: value}
    with pytest.raises(ev.SpecError, match=f"survival.{key}"):
        ev.validate_watch_spec(raw)


def test_spec_rejects_too_many_slots() -> None:
    raw = _base_spec()
    raw["watchpoints"] = [
        {"id": f"w{i}", "address": f"0x{0x400000 + i * 4:x}", "kind": "read", "size": 4}
        for i in range(5)
    ]
    with pytest.raises(ev.SpecError, match="1..4"):
        ev.validate_watch_spec(raw)


def test_spec_rejects_zero_slots() -> None:
    raw = _base_spec()
    raw["watchpoints"] = []
    with pytest.raises(ev.SpecError, match="1..4"):
        ev.validate_watch_spec(raw)


def test_spec_rejects_bad_size() -> None:
    raw = _base_spec()
    raw["watchpoints"][0]["size"] = 3
    with pytest.raises(ev.SpecError, match="size"):
        ev.validate_watch_spec(raw)


def test_spec_rejects_misaligned_address() -> None:
    raw = _base_spec()
    raw["watchpoints"][0]["address"] = "0x00400011"
    with pytest.raises(ev.SpecError, match="aligned"):
        ev.validate_watch_spec(raw)


def test_spec_rejects_unknown_key() -> None:
    raw = _base_spec()
    raw["surprise"] = 1
    with pytest.raises(ev.SpecError, match="unknown keys"):
        ev.validate_watch_spec(raw)


def test_spec_rejects_oversized_memory_read() -> None:
    raw = _base_spec()
    raw["on_stop"]["memory_reads"] = [{"id": "m0", "address": "0x00400000", "size": 300}]
    with pytest.raises(ev.SpecError, match="256"):
        ev.validate_watch_spec(raw)


def test_spec_rejects_duplicate_id() -> None:
    raw = _base_spec()
    raw["breakpoints"] = [{"id": "w0", "address": "0x00400020"}]
    with pytest.raises(ev.SpecError, match="duplicate id"):
        ev.validate_watch_spec(raw)


def test_spec_rejects_wrong_schema_version() -> None:
    raw = _base_spec()
    raw["schema_version"] = 7
    with pytest.raises(ev.SpecError, match="schema_version"):
        ev.validate_watch_spec(raw)


def _direct3d_batch_capture_block() -> dict:
    return {
        "pre_trigger_id": "pre",
        "flush_trigger_id": "flush",
        "post_trigger_id": "post",
        "pre_stop_pcs": ["0x00400101", "0x00400111"],
        "post_stop_pc": "0x00400201",
        "call_return_address": "0x00400300",
        "stack_pointer_register": "esp",
        "entry_return_stack_offset": 16,
        "entry_pointer_stack_offset": 20,
        "entry_index_stack_offset": 4,
        "post_entry_register": "esi",
        "page_register": "edi",
        "entry_root": "0x00600000",
        "entry_stride": 16,
        "entry_count": 4,
        "candidate_indices": [0, 1, 3],
        "pointer_size": 4,
        "page_count": 2,
        "max_digest_bytes_per_entry": 4096,
        "warmup_rollovers": 1,
        "capture_cycles": 1,
        "families": [{
            "id": "family_a",
            "flush_stop_pc": "0x00400401",
            "root_pointer_address": "0x00610000",
            "allowed_roots": ["0x00620000"],
            "vertex_pointer_table_offset": 0,
            "vertex_count_offset": 8,
            "index_base_offset": 16,
            "index_count_offset": 32,
            "index_page_stride": 8,
            "vertex_stride": 4,
            "max_vertex_count": 2,
            "max_index_count": 4,
        }],
    }


def _direct3d_record_capture_block() -> dict:
    block = _direct3d_batch_capture_block()
    block.update({
        "capture_mode": "record_outcome",
        "record_pointer_register": "esi",
        "record_forms": [
            {
                "form": 0x3C,
                "stop_pc": "0x00400101",
                "append_vertex_count": 4,
                "append_index_count": 6,
            },
            {
                "form": 0x34,
                "stop_pc": "0x00400111",
                "append_vertex_count": 3,
                "append_index_count": 3,
            },
        ],
        "record_plan": [
            {"entry_index": 0, "file_offset": 4, "form": 0x3C},
            {"entry_index": 1, "file_offset": 0x34, "form": 0x34},
            {"entry_index": 3, "file_offset": 0x58, "form": 0x34},
        ],
        "candidate_record_offsets": [4, 0x34, 0x58],
        "allowed_outcome_family_id": "family_a",
        "allowed_outcome_page": 1,
    })
    return block


def test_v4_direct3d_batch_capture_normalizes() -> None:
    raw = _base_spec()
    raw["schema_version"] = 4
    raw["watchpoints"] = [
        {"id": "pre", "address": "0x00630000", "kind": "access", "size": 2},
        {"id": "flush", "address": "0x00630002", "kind": "access", "size": 2},
        {"id": "post", "address": "0x00630004", "kind": "access", "size": 4},
    ]
    raw["direct3d_batch_capture"] = _direct3d_batch_capture_block()
    spec = ev.validate_watch_spec(raw)
    capture = spec.direct3d_batch_capture
    assert capture is not None
    assert capture.pre_stop_pcs == (0x00400101, 0x00400111)
    assert capture.candidate_indices == (0, 1, 3)
    assert capture.families[0].allowed_roots == (0x00620000,)
    assert capture.families[0].index_page_stride == 8


def test_v5_direct3d_record_capture_normalizes() -> None:
    raw = _base_spec()
    raw["schema_version"] = 5
    raw["watchpoints"] = [
        {"id": "pre", "address": "0x00630000", "kind": "access", "size": 2},
        {"id": "flush", "address": "0x00630002", "kind": "access", "size": 2},
        {"id": "post", "address": "0x00630004", "kind": "access", "size": 4},
    ]
    raw["direct3d_batch_capture"] = _direct3d_record_capture_block()
    spec = ev.validate_watch_spec(raw)
    capture = spec.direct3d_batch_capture
    assert capture is not None
    assert capture.capture_mode == "record_outcome"
    assert capture.record_pointer_register == "esi"
    assert [item.file_offset for item in capture.record_plan] == [4, 0x34, 0x58]
    assert capture.candidate_record_offsets == (4, 0x34, 0x58)
    assert capture.allowed_outcome_family_id == "family_a"
    assert capture.allowed_outcome_page == 1


def _exact_0a6c_spec(run_id: str = "RUN-GDB-20260813-124153") -> dict:
    path = (
        Path(__file__).resolve().parents[1]
        / f"dynamic/wine/{run_id}/spec.resolved.json"
    )
    raw = json.loads(path.read_text(encoding="utf-8"))
    copies = str((Path(__file__).resolve().parents[1] / "work/copies").resolve())
    if not raw["target"]["expected_cwd_prefix"].startswith(copies + "/"):
        pytest.skip("receipt records the original checkout path; re-audit runs only from that path")
    raw["schema_version"] = 6
    raw["experiment_id"] = "EXP-20260813-045"
    raw["on_stop"] = {
        "registers": [], "memory_reads": [], "backtrace_limit": 2,
    }
    capture = raw["direct3d_batch_capture"]
    capture["capture_mode"] = "exact_0a6c_admission"
    capture["candidate_indices"] = [7]
    capture["candidate_record_offsets"] = [0x0A6C]
    return raw


@pytest.mark.parametrize("run_id", [
    "RUN-GDB-20260813-124153",
    "RUN-GDB-20260813-124414",
    "RUN-GDB-20260813-124610",
])
def test_v6_exact_0a6c_capture_reaudits_the_complete_plan(
    run_id: str,
) -> None:
    spec = ev.validate_watch_spec(_exact_0a6c_spec(run_id))
    capture = spec.direct3d_batch_capture
    assert capture is not None
    assert capture.capture_mode == "exact_0a6c_admission"
    assert len(capture.record_plan) == 168
    assert capture.candidate_indices == (7,)
    assert capture.candidate_record_offsets == (0x0A6C,)


def test_v6_exact_0a6c_capture_accepts_only_fixed_cycle_bounds() -> None:
    for capture_cycles in (1, 3):
        raw = _exact_0a6c_spec()
        raw["direct3d_batch_capture"]["capture_cycles"] = capture_cycles
        capture = ev.validate_watch_spec(raw).direct3d_batch_capture
        assert capture is not None
        assert capture.capture_cycles == capture_cycles

    for capture_cycles in (2, 4, 8):
        raw = _exact_0a6c_spec()
        raw["direct3d_batch_capture"]["capture_cycles"] = capture_cycles
        with pytest.raises(ev.SpecError, match="fixed three-cycle"):
            ev.validate_watch_spec(raw)


@pytest.mark.parametrize(
    ("mutation", "match"),
    [
        ("record_plan", "168-call plan"),
        ("watchpoint", "audited boundaries"),
        ("register_output", "raw register/memory output"),
        ("candidate", "candidate_indices must exactly match"),
        ("executable", "hash-locked executable"),
        ("target_mode", "paused-target identity"),
        ("survival", "accepted survival gate"),
        ("window", "accepted bounded window"),
    ],
)
def test_v6_exact_0a6c_capture_rejects_envelope_drift(
    mutation: str, match: str,
) -> None:
    raw = _exact_0a6c_spec()
    if mutation == "record_plan":
        raw["direct3d_batch_capture"]["record_plan"][-1]["form"] = 0x34
    elif mutation == "watchpoint":
        raw["watchpoints"][0]["address"] = "0x0059F7F2"
    elif mutation == "register_output":
        raw["on_stop"]["registers"] = ["esi"]
    elif mutation == "candidate":
        raw["direct3d_batch_capture"]["candidate_indices"] = [6, 7]
    elif mutation == "executable":
        raw["target"]["expected_exe_sha256"] = "0" * 64
    elif mutation == "target_mode":
        raw["target"]["mode"] = "spawn"
    elif mutation == "survival":
        raw["survival"]["sample_count"] = 6
    elif mutation == "window":
        raw["window"]["timeout_seconds"] = 91
    with pytest.raises(ev.SpecError, match=match):
        ev.validate_watch_spec(raw)


@pytest.mark.parametrize(
    ("key", "value", "match"),
    [
        ("record_forms", [], "non-empty list"),
        ("candidate_record_offsets", [0x999], "subset"),
        ("allowed_outcome_family_id", "missing", "configured family"),
        ("allowed_outcome_page", 2, "outside page_count"),
    ],
)
def test_v5_rejects_invalid_direct3d_record_capture(
    key: str, value, match: str,
) -> None:
    raw = _base_spec()
    raw["schema_version"] = 5
    raw["watchpoints"] = [
        {"id": "pre", "address": "0x00630000", "kind": "access", "size": 2},
        {"id": "flush", "address": "0x00630002", "kind": "access", "size": 2},
        {"id": "post", "address": "0x00630004", "kind": "access", "size": 4},
    ]
    raw["direct3d_batch_capture"] = _direct3d_record_capture_block()
    raw["direct3d_batch_capture"][key] = value
    with pytest.raises(ev.SpecError, match=match):
        ev.validate_watch_spec(raw)


@pytest.mark.parametrize(
    ("path", "value", "match"),
    [
        (("pre_trigger_id",), "missing", "configured hardware point"),
        (("pre_stop_pcs",), [], "non-empty list"),
        (("candidate_indices",), [4], "outside entry_count"),
        (("pointer_size",), 3, "pointer_size"),
        (("families", 0, "allowed_roots"), [], "allowed_roots"),
        (("families", 0, "max_index_count"), 5, "index bound"),
    ],
)
def test_v4_rejects_invalid_direct3d_batch_capture(
    path: tuple, value, match: str,
) -> None:
    raw = _base_spec()
    raw["schema_version"] = 4
    raw["watchpoints"] = [
        {"id": "pre", "address": "0x00630000", "kind": "access", "size": 2},
        {"id": "flush", "address": "0x00630002", "kind": "access", "size": 2},
        {"id": "post", "address": "0x00630004", "kind": "access", "size": 4},
    ]
    raw["direct3d_batch_capture"] = _direct3d_batch_capture_block()
    target = raw["direct3d_batch_capture"]
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ev.SpecError, match=match):
        ev.validate_watch_spec(raw)


def test_v4_capture_modes_are_mutually_exclusive() -> None:
    raw = _base_spec()
    raw["schema_version"] = 4
    raw["watchpoints"] = []
    raw["breakpoints"] = [
        {"id": "pre", "address": "0x00400100"},
        {"id": "flush", "address": "0x00400110"},
        {"id": "post", "address": "0x00400200"},
    ]
    raw["submission_capture"] = _submission_capture_block()
    raw["direct3d_batch_capture"] = _direct3d_batch_capture_block()
    with pytest.raises(ev.SpecError, match="mutually exclusive"):
        ev.validate_watch_spec(raw)


def test_v4_direct3d_capture_requires_data_watchpoint_triggers() -> None:
    raw = _base_spec()
    raw["schema_version"] = 4
    raw["watchpoints"] = [
        {"id": "flush", "address": "0x00630002", "kind": "access", "size": 2},
        {"id": "post", "address": "0x00630004", "kind": "access", "size": 4},
    ]
    raw["breakpoints"] = [{"id": "pre", "address": "0x00400100"}]
    raw["direct3d_batch_capture"] = _direct3d_batch_capture_block()
    with pytest.raises(ev.SpecError, match="backed by a data watchpoint"):
        ev.validate_watch_spec(raw)


def test_v4_direct3d_capture_forbids_retained_memory_reads() -> None:
    raw = _base_spec()
    raw["schema_version"] = 4
    raw["watchpoints"] = [
        {"id": "pre", "address": "0x00630000", "kind": "access", "size": 2},
        {"id": "flush", "address": "0x00630002", "kind": "access", "size": 2},
        {"id": "post", "address": "0x00630004", "kind": "access", "size": 4},
    ]
    raw["on_stop"]["memory_reads"] = [
        {"id": "forbidden", "address": "0x00640000", "size": 4}
    ]
    raw["direct3d_batch_capture"] = _direct3d_batch_capture_block()
    with pytest.raises(ev.SpecError, match="forbids on_stop.memory_reads"):
        ev.validate_watch_spec(raw)


# --------------------------------------------------------------------------
# ELF core iteration
# --------------------------------------------------------------------------


def build_core(
    *,
    segments: tuple[tuple[int, bytes, int], ...] = ((0x00400000, b"\x11\x22\x33\x44payload", 0x5),),
    truncate: int = 0,
    e_type: int = ev.ET_CORE,
    phnum_override: int | None = None,
) -> bytes:
    # Minimal ELF64 little-endian core: Ehdr + N Phdr + segment payloads.
    ehsize = 64
    phentsize = 56
    phnum = len(segments)
    phoff = ehsize
    header_end = phoff + phnum * phentsize

    payloads = b"".join(payload for _, payload, _ in segments)
    ehdr = bytearray(ehsize)
    ehdr[0:4] = ev.ELF_MAGIC
    ehdr[4] = ev.ELFCLASS64
    ehdr[5] = ev.ELFDATA2LSB
    ehdr[6] = 1
    struct.pack_into("<H", ehdr, 16, e_type)
    struct.pack_into("<H", ehdr, 18, 0x3E)  # EM_X86_64
    struct.pack_into("<I", ehdr, 20, 1)
    struct.pack_into("<Q", ehdr, 32, phoff)
    struct.pack_into("<H", ehdr, 52, ehsize)
    struct.pack_into("<H", ehdr, 54, phentsize)
    struct.pack_into("<H", ehdr, 56, phnum if phnum_override is None else phnum_override)

    phdrs = bytearray()
    offset = header_end
    for vaddr, payload, flags in segments:
        phdr = bytearray(phentsize)
        struct.pack_into("<I", phdr, 0, ev.PT_LOAD)
        struct.pack_into("<I", phdr, 4, flags)
        struct.pack_into("<Q", phdr, 8, offset)
        struct.pack_into("<Q", phdr, 16, vaddr)
        struct.pack_into("<Q", phdr, 32, len(payload))
        struct.pack_into("<Q", phdr, 40, len(payload))
        phdrs += phdr
        offset += len(payload)

    core = bytes(ehdr) + bytes(phdrs) + payloads
    if truncate:
        core = core[:-truncate]
    return core


def test_core_iterates_segments() -> None:
    core = build_core(
        segments=(
            (0x00400000, b"AAAA", 0x5),
            (0x005AA000, b"BBBBBBBB", 0x6),
        )
    )
    segs = list(ev.iter_core_load_segments(core))
    assert [s.vaddr for s in segs] == [0x00400000, 0x005AA000]
    assert segs[0].flags_str == "r-x"
    assert segs[1].flags_str == "rw-"


def test_core_rejects_bad_magic() -> None:
    with pytest.raises(ev.ElfCoreError, match="magic"):
        list(ev.iter_core_load_segments(b"\x00" * 128))


def test_core_rejects_non_core_type() -> None:
    core = build_core(e_type=2)  # ET_EXEC
    with pytest.raises(ev.ElfCoreError, match="ET_CORE"):
        list(ev.iter_core_load_segments(core))


def test_core_rejects_pn_xnum() -> None:
    core = build_core(phnum_override=ev.PN_XNUM)
    with pytest.raises(ev.ElfCoreError, match="PN_XNUM"):
        list(ev.iter_core_load_segments(core))


def test_core_reports_truncated_segment() -> None:
    core = build_core(segments=((0x00400000, b"ABCDEFGH", 0x5),), truncate=3)
    segs = list(ev.iter_core_load_segments(core))
    assert segs[0].truncated is True
