from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import evidence_lib as ev  # noqa: E402


def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "gdb_harness", SCRIPTS / "gdb-harness.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


harness = _load_harness()


FIXTURE_C = r"""
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
volatile unsigned int sentinel = 0x1111;
int main(int argc, char** argv) {
    printf("ADDR %p\n", (void*)&sentinel);
    fflush(stdout);
    FILE* logf = NULL;
    if (argc > 1 && argv[1][0]) { logf = fopen(argv[1], "a"); }
    int touch = (argc > 2) ? atoi(argv[2]) : 1;
    int sig = (argc > 3) ? atoi(argv[3]) : 0;
    const char* fatal_trigger = (argc > 4) ? argv[4] : "";
    int fatal_sent = 0;
    if (sig) signal(SIGUSR1, SIG_IGN);  /* like Wine: SIGUSR1 is normal */
    for (long i = 0; ; i++) {
        if (touch) sentinel = sentinel + 1;
        if (sig) raise(SIGUSR1);
        if (!fatal_sent && fatal_trigger[0] && access(fatal_trigger, F_OK) == 0) {
            fatal_sent = 1;
            raise(SIGSEGV);
        }
        if (logf && i == 15) { fputs("MILESTONE\n", logf); fflush(logf); }
        usleep(20000);
    }
    return 0;
}
"""


SUBMISSION_FIXTURE_C = r"""
#include <stdio.h>
#include <string.h>
#include <unistd.h>
unsigned int submission_counter = 0;
unsigned int submission_capacity = 16;
unsigned char submission_arena[16 * 16];
unsigned char* submission_base = submission_arena;
unsigned char entries[4 * 16];
__attribute__((noinline)) void capture_pre(void* entry) {
    __asm__ volatile("" : : "r"(entry) : "memory");
}
__attribute__((noinline)) void capture_post(void* entry) {
    __asm__ volatile("" : : "r"(entry) : "memory");
}
int main(int argc, char** argv) {
    printf("READY\n");
    fflush(stdout);
    int inactive = argc > 1;
    if (inactive) {
        submission_capacity = 0;
        submission_base = NULL;
    }
    for (;;) {
        submission_counter = 0;
        for (unsigned int i = 0; i < 4; i++) {
            capture_pre(&entries[i * 16]);
            if (!inactive) {
                memset(&submission_arena[submission_counter * 16], (int)(0x20 + i), 16);
                submission_counter++;
            }
            capture_post(&entries[i * 16]);
        }
        usleep(20000);
    }
}
"""


def _compile_fixture(tmp_path: Path) -> Path:
    cc = shutil.which("cc") or shutil.which("gcc")
    if cc is None:
        pytest.skip("no C compiler available")
    src = tmp_path / "sentinel.c"
    src.write_text(FIXTURE_C)
    exe = tmp_path / "sentinel"
    result = subprocess.run(
        [cc, "-O0", "-o", str(exe), str(src)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"fixture compile failed: {result.stderr}")
    return exe


def _compile_submission_fixture(tmp_path: Path) -> Path:
    cc = shutil.which("cc") or shutil.which("gcc")
    if cc is None:
        pytest.skip("no C compiler available")
    src = tmp_path / "submission.c"
    src.write_text(SUBMISSION_FIXTURE_C)
    exe = tmp_path / "submission"
    result = subprocess.run(
        [cc, "-O0", "-no-pie", "-o", str(exe), str(src)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"submission fixture compile failed: {result.stderr}")
    return exe


def _symbols(exe: Path, *names: str) -> dict[str, int]:
    nm = shutil.which("nm")
    if nm is None:
        pytest.skip("nm not available")
    result = subprocess.run(
        [nm, "-n", str(exe)], capture_output=True, text=True, check=True,
    )
    wanted = set(names)
    found = {}
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) >= 3 and fields[2] in wanted:
            found[fields[2]] = int(fields[0], 16)
    assert set(found) == wanted
    return found


def _spawn_fixture(exe: Path, cwd: Path, extra=()):
    proc = subprocess.Popen(
        [str(exe), *[str(e) for e in extra]],
        cwd=str(cwd),
        stdout=subprocess.PIPE, text=True,
    )
    line = proc.stdout.readline()
    match = re.search(r"ADDR (0x[0-9a-fA-F]+)", line)
    if not match:
        proc.terminate()
        pytest.skip("fixture did not print address")
    return proc, int(match.group(1), 16)


def _run_harness(spec_path: Path, root: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["ABLPC_ROOT"] = str(root)
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "gdb-harness.py"), "--spec", str(spec_path)],
        capture_output=True, text=True, env=env, timeout=120,
    )


def _latest_run(root: Path) -> Path:
    runs = sorted((root / "dynamic" / "wine").glob("RUN-GDB-*"))
    assert runs, "no RUN-GDB dir created"
    return runs[-1]


# --------------------------------------------------------------------------
# Pure / CLI unit tests (no gdb needed)
# --------------------------------------------------------------------------


def test_capabilities_write_verbs_empty() -> None:
    caps = harness.capabilities()
    assert caps["write_verbs"] == []
    assert caps["mode"] == "read-only"
    assert caps["limits"]["hw_slots"] == 4
    assert caps["supported_spec_schema_versions"] == [1, 2, 3, 4, 5, 6]
    assert "target_signal" in caps["stop_reasons"]
    assert "capture_complete" in caps["stop_reasons"]
    assert caps["submission_capture"]["retains_payload_bytes"] is False
    assert caps["direct3d_batch_capture"]["retains_payload_bytes"] is False
    assert caps["direct3d_batch_capture"][
        "supports_exact_0a6c_first_reject"
    ] is True
    assert caps["direct3d_batch_capture"][
        "supports_exact_0a6c_consecutive_cycles"
    ] is True
    assert caps["direct3d_batch_capture"][
        "exact_0a6c_consecutive_capture_cycles"
    ] == 3
    assert caps["direct3d_batch_capture"][
        "exact_0a6c_requires_existing_pid"
    ] is True
    assert caps["direct3d_batch_capture"][
        "exact_0a6c_retains_raw_stop_values"
    ] is False


def test_capabilities_cli(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "gdb-harness.py"), "--capabilities"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    caps = json.loads(result.stdout)
    assert caps["tool"] == "gdb-harness"
    assert caps["write_verbs"] == []


def test_direct3d_watch_conditions_are_exact_and_read_only() -> None:
    family = ev.Direct3DBatchFamily(
        id="family_a", flush_stop_pc=0x401,
        root_pointer_address=0x6100, allowed_roots=(0x6200,),
        vertex_pointer_table_offset=0, vertex_count_offset=8,
        index_base_offset=16, index_count_offset=32,
        index_page_stride=8, vertex_stride=4,
        max_vertex_count=2, max_index_count=4,
    )
    capture = ev.Direct3DBatchCapture(
        pre_trigger_id="pre", flush_trigger_id="flush",
        post_trigger_id="post", pre_stop_pcs=(0x101, 0x111),
        post_stop_pc=0x201, call_return_address=0x300,
        stack_pointer_register="esp", entry_return_stack_offset=16,
        entry_pointer_stack_offset=4, entry_index_stack_offset=8,
        post_entry_register="esi", page_register="edi",
        entry_root=0x6000, entry_stride=16, entry_count=4,
        candidate_indices=(0,), pointer_size=4, page_count=1,
        families=(family,), max_digest_bytes_per_entry=4096,
        warmup_rollovers=1, capture_cycles=1,
    )
    pre = harness._direct3d_watch_condition(capture, "pre")
    assert "$pc == 0x101" in pre and "$pc == 0x111" in pre
    assert "*(unsigned int *)($esp + 16) == 0x300" in pre
    assert harness._direct3d_watch_condition(capture, "flush") == "$pc == 0x401"
    assert harness._direct3d_watch_condition(capture, "post") == "$pc == 0x201"
    assert harness._direct3d_watch_condition(capture, "other") is None


def test_exact_admission_stop_record_redacts_raw_values() -> None:
    class Frame:
        @staticmethod
        def pc():
            return 0x0044F951

        @staticmethod
        def read_register(_name):
            return 0xDEADBEEF

    class Inferior:
        @staticmethod
        def read_memory(_address, size):
            return b"\xA5" * size

    class FakeGdb:
        error = RuntimeError

        @staticmethod
        def newest_frame():
            return Frame()

        @staticmethod
        def selected_inferior():
            return Inferior()

    record = harness._build_stop_record(
        FakeGdb(), 1, 0,
        ("watchpoint", "batch_pre", 0x0059F7F0, 2),
        ["esi"], [ev.MemoryRead("raw", 0x1000, 4)], 0,
        redact_values=True,
    )
    assert record["registers"] == {}
    assert record["watched_value_hex"] is None
    assert record["memory_reads"] == []
    serialized = json.dumps(record)
    assert "deadbeef" not in serialized.lower()
    assert "a5a5a5a5" not in serialized.lower()


def test_exact_admission_failure_detail_redacts_raw_values() -> None:
    class Capture:
        capture_mode = "exact_0a6c_admission"

    state = {"failure": None}
    assert harness._capture_fail_for_mode(
        Capture(), state, RuntimeError("unexpected root 0xDEADBEEF")
    ) == "error"
    assert state["failure"] == (
        "exact_0a6c_admission:capture_structure_mismatch"
    )
    assert "deadbeef" not in json.dumps(state).lower()


@pytest.mark.parametrize("command", [
    "set var x=1",
    "call foo()",
    "break *0x1",
    "print x=1",
    "run",
    "jump *0x1",
])
def test_readonly_allowlist_rejects(command: str) -> None:
    with pytest.raises(harness.ReadOnlyViolation):
        harness.check_gdb_command(command)


@pytest.mark.parametrize("command", [
    "attach 123",
    "continue",
    "detach",
    "set can-use-hw-watchpoints 1",
    "info watchpoints",
    "handle SIGUSR1 nostop noprint pass",
])
def test_readonly_allowlist_accepts(command: str) -> None:
    assert harness.check_gdb_command(command) == command


# --------------------------------------------------------------------------
# End-to-end tests against a compiled C fixture (exercise the gdb controller)
# --------------------------------------------------------------------------


def _base_spec(exe: Path, cwd: Path, pid: int, address: int, **window) -> dict:
    win = {"max_stops": 3, "timeout_seconds": 20, "end_milestones": [], "log_path": None}
    win.update(window)
    return {
        "schema_version": 1,
        "experiment_id": "EXP-20260812-999",
        "target": {
            "mode": "pid",
            "pid": pid,
            "exe_basename": exe.name,
            "expected_exe_sha256": ev.sha256_file(exe),
            "expected_loader_re": ".*",
            "expected_cwd_prefix": str(cwd) + os.sep,
        },
        "watchpoints": [{"id": "w0", "address": f"0x{address:x}", "kind": "access", "size": 4}],
        "breakpoints": [],
        "window": win,
        "on_stop": {"registers": ["rip"], "memory_reads": [], "backtrace_limit": 4},
    }


def test_end_to_end_max_stops(tmp_path: Path) -> None:
    if shutil.which("gdb") is None:
        pytest.skip("gdb not available")
    exe = _compile_fixture(tmp_path)
    proc, address = _spawn_fixture(exe, tmp_path)
    try:
        spec = _base_spec(exe, tmp_path, proc.pid, address)
        spec_path = tmp_path / "spec.json"
        spec_path.write_text(json.dumps(spec))
        result = _run_harness(spec_path, tmp_path)
        assert result.returncode == 0, result.stderr + result.stdout

        run_dir = _latest_run(tmp_path)
        metadata = json.loads((run_dir / "metadata.json").read_text())
        completion = metadata["completion"]
        assert completion["stop_reason"] == "max_stops"
        assert completion["stops_observed"] >= 3
        assert completion["watchpoints_installed"] == 1
        assert completion["watchpoints_deleted"] == 1
        assert completion["cleanup_verified"] is True
        assert completion["detached"] is True

        lines = (run_dir / "stops.jsonl").read_text().strip().splitlines()
        assert len(lines) >= 3
        for line in lines:
            record = json.loads(line)
            for key in ("seq", "kind", "trigger_id", "pc", "registers",
                        "watched_value_hex", "backtrace_pcs"):
                assert key in record
            assert record["kind"] == "watchpoint"
            assert record["trigger_id"] == "w0"

        # The fixture must still be running: detach resumed it.
        assert proc.poll() is None
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_submission_capture_is_paired_bounded_and_digest_only(
    tmp_path: Path,
) -> None:
    if shutil.which("gdb") is None:
        pytest.skip("gdb not available")
    exe = _compile_submission_fixture(tmp_path)
    symbols = _symbols(
        exe, "capture_pre", "capture_post", "entries", "submission_counter",
        "submission_capacity", "submission_base",
    )
    proc = subprocess.Popen(
        [str(exe)], cwd=str(tmp_path), stdout=subprocess.PIPE, text=True,
    )
    assert proc.stdout.readline().strip() == "READY"
    try:
        spec = {
            "schema_version": 3,
            "experiment_id": "EXP-20260813-999",
            "target": {
                "mode": "pid",
                "pid": proc.pid,
                "exe_basename": exe.name,
                "expected_exe_sha256": ev.sha256_file(exe),
                "expected_loader_re": ".*",
                "expected_cwd_prefix": str(tmp_path) + os.sep,
            },
            "watchpoints": [],
            "breakpoints": [
                {"id": "pre", "address": f"0x{symbols['capture_pre']:x}"},
                {"id": "post", "address": f"0x{symbols['capture_post']:x}"},
            ],
            "window": {
                "max_stops": 40,
                "timeout_seconds": 20,
                "end_milestones": [],
                "log_path": None,
            },
            "on_stop": {
                "registers": ["rip", "rdi"],
                "memory_reads": [],
                "backtrace_limit": 2,
            },
            "survival": {
                "required": True,
                "settle_ms": 50,
                "sample_count": 2,
                "sample_interval_ms": 50,
                "require_untraced": True,
                "require_resumed": True,
            },
            "submission_capture": {
                "interval_mode": "paired",
                "pre_trigger_id": "pre",
                "post_trigger_id": "post",
                "entry_register": "rdi",
                "entry_root": f"0x{symbols['entries']:x}",
                "entry_stride": 16,
                "entry_count": 4,
                "candidate_indices": [0, 1, 3],
                "counter_address": f"0x{symbols['submission_counter']:x}",
                "capacity_address": f"0x{symbols['submission_capacity']:x}",
                "base_pointer_address": f"0x{symbols['submission_base']:x}",
                "pointer_size": 8,
                "output_stride": 16,
                "max_records_per_entry": 4,
                "warmup_rollovers": 1,
                "capture_cycles": 1,
            },
        }
        spec_path = tmp_path / "submission-spec.json"
        spec_path.write_text(json.dumps(spec))
        run = _run_harness(spec_path, tmp_path)
        assert run.returncode == 0, run.stderr + run.stdout

        result = json.loads((_latest_run(tmp_path) / "result.json").read_text())
        assert result["completion"]["stop_reason"] == "capture_complete"
        assert result["completion"]["accepted"] is True
        assert result["completion"]["survival_verified"] is True
        capture = result["submission_capture"]
        assert capture["completed"] is True
        assert capture["payload_bytes_retained"] is False
        assert capture["failure"] is None
        assert len(capture["cycles"]) == 1
        entries = capture["cycles"][0]["entries"]
        assert [entry["entry_index"] for entry in entries] == [0, 1, 3]
        assert all(entry["record_count"] == 1 for entry in entries)
        assert all(entry["byte_count"] == 16 for entry in entries)
        assert all(re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])
                   for entry in entries)
        capture_text = json.dumps(capture)
        assert "payload" not in capture_text.replace("payload_bytes_retained", "")
        assert "hex" not in capture_text
        assert proc.poll() is None
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_zero_post_capture_accepts_only_coherent_inactive_arena(
    tmp_path: Path,
) -> None:
    if shutil.which("gdb") is None:
        pytest.skip("gdb not available")
    exe = _compile_submission_fixture(tmp_path)
    symbols = _symbols(
        exe, "capture_post", "entries", "submission_counter",
        "submission_capacity", "submission_base",
    )
    proc = subprocess.Popen(
        [str(exe), "inactive"], cwd=str(tmp_path), stdout=subprocess.PIPE,
        text=True,
    )
    assert proc.stdout.readline().strip() == "READY"
    try:
        spec = {
            "schema_version": 3,
            "experiment_id": "EXP-20260813-999",
            "target": {
                "mode": "pid",
                "pid": proc.pid,
                "exe_basename": exe.name,
                "expected_exe_sha256": ev.sha256_file(exe),
                "expected_loader_re": ".*",
                "expected_cwd_prefix": str(tmp_path) + os.sep,
            },
            "watchpoints": [],
            "breakpoints": [
                {"id": "post", "address": f"0x{symbols['capture_post']:x}"},
            ],
            "window": {
                "max_stops": 20,
                "timeout_seconds": 20,
                "end_milestones": [],
                "log_path": None,
            },
            "on_stop": {
                "registers": ["rip", "rdi"],
                "memory_reads": [],
                "backtrace_limit": 2,
            },
            "survival": {
                "required": True,
                "settle_ms": 50,
                "sample_count": 2,
                "sample_interval_ms": 50,
                "require_untraced": True,
                "require_resumed": True,
            },
            "submission_capture": {
                "interval_mode": "zero_post",
                "pre_trigger_id": "post",
                "post_trigger_id": "post",
                "entry_register": "rdi",
                "entry_root": f"0x{symbols['entries']:x}",
                "entry_stride": 16,
                "entry_count": 4,
                "candidate_indices": [0, 1, 3],
                "counter_address": f"0x{symbols['submission_counter']:x}",
                "capacity_address": f"0x{symbols['submission_capacity']:x}",
                "base_pointer_address": f"0x{symbols['submission_base']:x}",
                "pointer_size": 8,
                "output_stride": 16,
                "max_records_per_entry": 4,
                "warmup_rollovers": 1,
                "capture_cycles": 1,
            },
        }
        spec_path = tmp_path / "zero-post-spec.json"
        spec_path.write_text(json.dumps(spec))
        run = _run_harness(spec_path, tmp_path)
        assert run.returncode == 0, run.stderr + run.stdout
        result = json.loads((_latest_run(tmp_path) / "result.json").read_text())
        assert result["completion"]["stop_reason"] == "capture_complete"
        assert result["completion"]["accepted"] is True
        capture = result["submission_capture"]
        assert capture["interval_mode"] == "zero_post"
        entries = capture["cycles"][0]["entries"]
        assert [entry["entry_index"] for entry in entries] == [0, 1, 3]
        assert all(entry["pre_counter"] == entry["post_counter"] == 0
                   for entry in entries)
        assert all(entry["byte_count"] == 0 for entry in entries)
        assert all(entry["sha256"] == hashlib.sha256(b"").hexdigest()
                   for entry in entries)
        assert proc.poll() is None
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_survives_target_signals(tmp_path: Path) -> None:
    # Regression for the live-found bug: the target raises SIGUSR1 every loop
    # (as Wine does). The harness must pass it through and still reach its
    # window end rather than treating the signal stop as the end of the run.
    if shutil.which("gdb") is None:
        pytest.skip("gdb not available")
    exe = _compile_fixture(tmp_path)
    proc, address = _spawn_fixture(exe, tmp_path, extra=("", "1", "1"))
    try:
        spec = _base_spec(exe, tmp_path, proc.pid, address, max_stops=3)
        spec_path = tmp_path / "spec.json"
        spec_path.write_text(json.dumps(spec))
        result = _run_harness(spec_path, tmp_path)
        assert result.returncode == 0, result.stderr + result.stdout
        completion = json.loads((_latest_run(tmp_path) / "metadata.json").read_text())["completion"]
        assert completion["stop_reason"] == "max_stops"
        assert completion["stops_observed"] >= 3
        assert completion["cleanup_verified"] is True
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_fatal_signal_is_structured_terminal_and_detach_is_safe(
    tmp_path: Path,
) -> None:
    if shutil.which("gdb") is None:
        pytest.skip("gdb not available")
    exe = _compile_fixture(tmp_path)
    trigger = tmp_path / "raise-segv"
    proc, address = _spawn_fixture(
        exe, tmp_path, extra=("", "0", "0", str(trigger))
    )
    harness_proc = None
    try:
        spec = _base_spec(exe, tmp_path, proc.pid, address,
                          timeout_seconds=20, max_stops=5)
        spec["schema_version"] = 2
        spec["survival"] = {
            "required": True,
            "settle_ms": 100,
            "sample_count": 3,
            "sample_interval_ms": 50,
            "require_untraced": True,
            "require_resumed": True,
        }
        spec_path = tmp_path / "spec.json"
        spec_path.write_text(json.dumps(spec))
        env = dict(os.environ)
        env["ABLPC_ROOT"] = str(tmp_path)
        harness_proc = subprocess.Popen(
            [sys.executable, str(SCRIPTS / "gdb-harness.py"),
             "--spec", str(spec_path)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
        )

        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            status = Path(f"/proc/{proc.pid}/status").read_text()
            match = re.search(r"^TracerPid:\s+(\d+)$", status, re.MULTILINE)
            if match and int(match.group(1)):
                break
            if harness_proc.poll() is not None:
                break
            time.sleep(0.02)
        else:
            pytest.fail("gdb did not attach to the fatal-signal fixture")
        assert harness_proc.poll() is None

        trigger.write_text("raise SIGSEGV\n")
        stdout, stderr = harness_proc.communicate(timeout=30)
        assert harness_proc.returncode == ev.EXIT_TOOL_NEGATIVE, stderr + stdout

        run_dir = _latest_run(tmp_path)
        result = json.loads((run_dir / "result.json").read_text())
        completion = result["completion"]
        assert completion["stop_reason"] == "target_signal"
        assert completion["completed"] is False
        assert completion["accepted"] is False
        assert completion["target_signal"]["name"] == "SIGSEGV"
        assert completion["target_signal"]["classification"] == "fatal"
        assert completion["target_signal"]["pc"].startswith("0x")
        assert completion["target_signal"]["delivery_policy"] == "stop-print-nopass"
        assert completion["cleanup_verified"] is True
        assert completion["detached"] is True
        assert completion["survival_verified"] is True
        receipt = completion["survival_receipt"]
        assert receipt["passed"] is True
        assert receipt["identity_verified"] is True
        assert len(receipt["samples"]) == 3
        assert all(sample["tracer_pid"] == 0 for sample in receipt["samples"])
        assert all(sample["passed"] for sample in receipt["samples"])
        assert proc.poll() is None
    finally:
        if harness_proc is not None and harness_proc.poll() is None:
            harness_proc.terminate()
            harness_proc.wait(timeout=5)
        proc.terminate()
        proc.wait(timeout=5)


def test_required_failed_survival_cannot_be_accepted() -> None:
    result = {
        "completion": {
            "completed": True,
            "accepted": True,
            "stop_reason": "target_reached",
        }
    }
    receipt = {"passed": False, "failure_reasons": ["sample[0]:state:T"]}
    updated = harness._apply_survival_receipt(result, receipt, required=True)
    completion = updated["completion"]
    assert completion["primary_stop_reason"] == "target_reached"
    assert completion["stop_reason"] == "survival_failed"
    assert completion["completed"] is False
    assert completion["accepted"] is False
    assert completion["survival_verified"] is False


def test_all_zero_submission_arena_is_a_bounded_inactive_state() -> None:
    class Inferior:
        def read_memory(self, _address, size):
            return b"\0" * size

    class FakeGdb:
        @staticmethod
        def selected_inferior():
            return Inferior()

    capture = ev.SubmissionCapture(
        interval_mode="paired",
        pre_trigger_id="pre",
        post_trigger_id="post",
        pre_stop_pc=None,
        post_stop_pc=None,
        entry_register="rdi",
        entry_root=0x600000,
        entry_stride=16,
        entry_count=4,
        candidate_indices=(0, 1, 3),
        counter_address=0x610000,
        capacity_address=0x610004,
        base_pointer_address=0x610008,
        pointer_size=8,
        output_stride=16,
        max_records_per_entry=4,
        warmup_rollovers=1,
        capture_cycles=1,
    )
    assert harness._read_submission_bounds(FakeGdb(), capture) == (0, 0, 0)


def test_partially_initialized_submission_arena_fails_closed() -> None:
    values = {
        0x610000: (0).to_bytes(4, "little"),
        0x610004: (0).to_bytes(4, "little"),
        0x610008: (0x620000).to_bytes(8, "little"),
    }

    class Inferior:
        def read_memory(self, address, size):
            return values[address][:size]

    class FakeGdb:
        @staticmethod
        def selected_inferior():
            return Inferior()

    capture = ev.SubmissionCapture(
        interval_mode="zero_post",
        pre_trigger_id="post",
        post_trigger_id="post",
        pre_stop_pc=None,
        post_stop_pc=None,
        entry_register="rdi",
        entry_root=0x600000,
        entry_stride=16,
        entry_count=4,
        candidate_indices=(0, 1, 3),
        counter_address=0x610000,
        capacity_address=0x610004,
        base_pointer_address=0x610008,
        pointer_size=8,
        output_stride=16,
        max_records_per_entry=4,
        warmup_rollovers=1,
        capture_cycles=1,
    )
    with pytest.raises(RuntimeError, match="inactive submission arena"):
        harness._read_submission_bounds(FakeGdb(), capture)


def test_direct3d_batch_capture_preserves_pre_reset_flush_segments() -> None:
    class Memory:
        def __init__(self):
            self.values = {}

        def write(self, address, data):
            for offset, value in enumerate(data):
                self.values[address + offset] = value

        def read_memory(self, address, size):
            return bytes(self.values[address + offset] for offset in range(size))

    class Frame:
        pc_value = 0
        registers = {"esp": 0x7000, "esi": 0x6000, "edi": 0}

        @classmethod
        def pc(cls):
            return cls.pc_value

        @classmethod
        def read_register(cls, name):
            return cls.registers[name]

    memory = Memory()

    class FakeGdb:
        @staticmethod
        def selected_inferior():
            return memory

        @staticmethod
        def newest_frame():
            return Frame

    family = ev.Direct3DBatchFamily(
        id="family_a",
        flush_stop_pc=0x401,
        root_pointer_address=0x6100,
        allowed_roots=(0x6200,),
        vertex_pointer_table_offset=0,
        vertex_count_offset=8,
        index_base_offset=16,
        index_count_offset=32,
        index_page_stride=8,
        vertex_stride=4,
        max_vertex_count=2,
        max_index_count=4,
    )
    capture = ev.Direct3DBatchCapture(
        pre_trigger_id="pre",
        flush_trigger_id="flush",
        post_trigger_id="post",
        pre_stop_pcs=(0x101,),
        post_stop_pc=0x201,
        call_return_address=0x300,
        stack_pointer_register="esp",
        entry_return_stack_offset=16,
        entry_pointer_stack_offset=4,
        entry_index_stack_offset=8,
        post_entry_register="esi",
        page_register="edi",
        entry_root=0x6000,
        entry_stride=16,
        entry_count=4,
        candidate_indices=(0,),
        pointer_size=4,
        page_count=1,
        families=(family,),
        max_digest_bytes_per_entry=4096,
        warmup_rollovers=1,
        capture_cycles=1,
    )
    memory.write(0x7010, (0x300).to_bytes(4, "little"))
    memory.write(0x7004, (0x6000).to_bytes(4, "little"))
    memory.write(0x7008, (0).to_bytes(4, "little"))
    memory.write(0x6100, (0x6200).to_bytes(4, "little"))
    memory.write(0x6200, (0x6300).to_bytes(4, "little"))
    memory.write(0x6208, (1).to_bytes(2, "little"))
    memory.write(0x6220, (1).to_bytes(2, "little"))
    memory.write(0x6300, b"old0")
    memory.write(0x6210, b"\x00\x00")

    state = harness._new_direct3d_batch_capture_state(capture)
    state["active"] = True
    Frame.pc_value = 0x101
    assert harness._process_direct3d_batch_stop(
        FakeGdb(), ("watchpoint", "pre", 0, 2), capture, state
    ) is None

    memory.write(0x6208, (2).to_bytes(2, "little"))
    memory.write(0x6220, (2).to_bytes(2, "little"))
    memory.write(0x6304, b"new1")
    memory.write(0x6212, b"\x01\x00")
    Frame.pc_value = 0x401
    assert harness._process_direct3d_batch_stop(
        FakeGdb(), ("watchpoint", "flush", 0, 2), capture, state
    ) is None

    memory.write(0x6208, (1).to_bytes(2, "little"))
    memory.write(0x6220, (1).to_bytes(2, "little"))
    memory.write(0x6300, b"new2")
    memory.write(0x6210, b"\x02\x00")
    Frame.pc_value = 0x201
    assert harness._process_direct3d_batch_stop(
        FakeGdb(), ("watchpoint", "post", 0, 4), capture, state
    ) is None

    entry = state["current_entries"][0]
    result_family = entry["families"][0]
    assert entry["vertex_count"] == 2
    assert entry["index_count"] == 2
    assert result_family["flush_count"] == 1
    assert [segment["flushed"] for segment in result_family["segments"]] == [
        True, False,
    ]
    serialized = json.dumps(entry)
    assert "new1" not in serialized
    assert "new2" not in serialized


def test_direct3d_record_capture_discriminates_append_and_flushed_no_append() -> None:
    class Memory:
        def __init__(self):
            self.values = {}

        def write(self, address, data):
            for offset, value in enumerate(data):
                self.values[address + offset] = value

        def read_memory(self, address, size):
            return bytes(self.values[address + offset] for offset in range(size))

    class Frame:
        pc_value = 0
        registers = {
            "esp": 0x7000,
            "esi": 0x8004,
            "edi": 0x6000,
            "ebp": 0,
        }

        @classmethod
        def pc(cls):
            return cls.pc_value

        @classmethod
        def read_register(cls, name):
            return cls.registers[name]

    memory = Memory()

    class FakeGdb:
        @staticmethod
        def selected_inferior():
            return memory

        @staticmethod
        def newest_frame():
            return Frame

    family = ev.Direct3DBatchFamily(
        id="family_a",
        flush_stop_pc=0x401,
        root_pointer_address=0x6100,
        allowed_roots=(0x6200,),
        vertex_pointer_table_offset=0,
        vertex_count_offset=8,
        index_base_offset=16,
        index_count_offset=32,
        index_page_stride=64,
        vertex_stride=4,
        max_vertex_count=16,
        max_index_count=32,
    )
    forms = (
        ev.Direct3DRecordForm(0x34, 0x101, 3, 3),
        ev.Direct3DRecordForm(0x3C, 0x111, 4, 6),
    )
    plan = (
        ev.Direct3DRecordPlanItem(0, 4, 0x34),
        ev.Direct3DRecordPlanItem(1, 0x28, 0x3C),
    )
    capture = ev.Direct3DBatchCapture(
        pre_trigger_id="pre",
        flush_trigger_id="flush",
        post_trigger_id="post",
        pre_stop_pcs=(0x101, 0x111),
        post_stop_pc=0x201,
        call_return_address=0x300,
        stack_pointer_register="esp",
        entry_return_stack_offset=16,
        entry_pointer_stack_offset=4,
        entry_index_stack_offset=8,
        post_entry_register="edi",
        page_register="ebp",
        entry_root=0x6000,
        entry_stride=16,
        entry_count=2,
        candidate_indices=(0, 1),
        pointer_size=4,
        page_count=1,
        families=(family,),
        max_digest_bytes_per_entry=1,
        warmup_rollovers=1,
        capture_cycles=1,
        capture_mode="record_outcome",
        record_pointer_register="esi",
        record_forms=forms,
        record_plan=plan,
        candidate_record_offsets=(4, 0x28),
        allowed_outcome_family_id="family_a",
        allowed_outcome_page=0,
    )
    memory.write(0x7010, (0x300).to_bytes(4, "little"))
    memory.write(0x7004, (0x6000).to_bytes(4, "little"))
    memory.write(0x7008, (0).to_bytes(4, "little"))
    memory.write(0x6100, (0x6200).to_bytes(4, "little"))
    memory.write(0x6200, (0x6300).to_bytes(4, "little"))
    memory.write(0x6208, (0).to_bytes(2, "little"))
    memory.write(0x6220, (0).to_bytes(2, "little"))

    state = harness._new_direct3d_batch_capture_state(capture)
    state["active"] = True
    Frame.pc_value = 0x101
    assert harness._process_direct3d_batch_stop(
        FakeGdb(), ("watchpoint", "pre", 0, 2), capture, state
    ) is None

    memory.write(0x6208, (3).to_bytes(2, "little"))
    memory.write(0x6220, (3).to_bytes(2, "little"))
    Frame.pc_value = 0x201
    assert harness._process_direct3d_batch_stop(
        FakeGdb(), ("watchpoint", "post", 0, 4), capture, state
    ) is None

    memory.write(0x7004, (0x6010).to_bytes(4, "little"))
    memory.write(0x7008, (1).to_bytes(4, "little"))
    Frame.registers.update({"esi": 0x8028, "edi": 0x6010})
    Frame.pc_value = 0x111
    assert harness._process_direct3d_batch_stop(
        FakeGdb(), ("watchpoint", "pre", 0, 2), capture, state
    ) is None

    Frame.pc_value = 0x401
    assert harness._process_direct3d_batch_stop(
        FakeGdb(), ("watchpoint", "flush", 0, 2), capture, state
    ) is None
    memory.write(0x6208, (0).to_bytes(2, "little"))
    memory.write(0x6220, (0).to_bytes(2, "little"))
    Frame.pc_value = 0x201
    assert harness._process_direct3d_batch_stop(
        FakeGdb(), ("watchpoint", "post", 0, 4), capture, state
    ) == "capture_complete"

    records = state["cycles"][0]["records"]
    assert records[0]["appended"] is True
    assert (records[0]["vertex_count"], records[0]["index_count"]) == (3, 3)
    assert records[1]["appended"] is False
    assert records[1]["flush_count"] == 1
    serialized = json.dumps(records)
    assert "payload" not in serialized
    assert "sha256" not in serialized


def test_exact_admission_count_mismatch_fails_closed() -> None:
    class Memory:
        def __init__(self):
            self.values = {}

        def write(self, address, data):
            for offset, value in enumerate(data):
                self.values[address + offset] = value

        def read_memory(self, address, size):
            return bytes(self.values[address + offset] for offset in range(size))

    memory = Memory()

    class FakeGdb:
        @staticmethod
        def selected_inferior():
            return memory

    family = ev.Direct3DBatchFamily(
        id="family_a", flush_stop_pc=0x401,
        root_pointer_address=0x6100, allowed_roots=(0x6200,),
        vertex_pointer_table_offset=0, vertex_count_offset=8,
        index_base_offset=16, index_count_offset=32,
        index_page_stride=64, vertex_stride=4,
        max_vertex_count=16, max_index_count=32,
    )
    capture = ev.Direct3DBatchCapture(
        pre_trigger_id="pre", flush_trigger_id="flush", post_trigger_id="post",
        pre_stop_pcs=(0x111,), post_stop_pc=0x201,
        call_return_address=0x300, stack_pointer_register="esp",
        entry_return_stack_offset=16, entry_pointer_stack_offset=4,
        entry_index_stack_offset=8, post_entry_register="edi",
        page_register="ebp", entry_root=0x6000, entry_stride=16,
        entry_count=8, candidate_indices=(7,), pointer_size=4, page_count=1,
        families=(family,), max_digest_bytes_per_entry=1,
        warmup_rollovers=1, capture_cycles=1,
        capture_mode="exact_0a6c_admission", record_pointer_register="esi",
        record_forms=(ev.Direct3DRecordForm(0x3C, 0x111, 4, 6),),
        record_plan=(ev.Direct3DRecordPlanItem(7, 0x0A6C, 0x3C),),
        candidate_record_offsets=(0x0A6C,),
        allowed_outcome_family_id="family_a", allowed_outcome_page=0,
    )
    memory.write(0x6100, (0x6200).to_bytes(4, "little"))
    memory.write(0x6200, (0x6300).to_bytes(4, "little"))
    memory.write(0x6208, (0).to_bytes(2, "little"))
    memory.write(0x6220, (0).to_bytes(2, "little"))
    memory.write(0x9000, (0x12345678).to_bytes(4, "little"))
    digest = harness.exact_admission.digest_active_state(
        lambda address: int.from_bytes(memory.read_memory(address, 4), "little"),
        (0x9000,),
    )
    evaluation = harness.exact_admission.AdmissionEvaluation(
        active_state_sha256=digest,
        evaluated_predicate_count=12,
        first_reject_pc=None,
        predicted_append=True,
        active_addresses=(0x9000,),
    )
    state = harness._new_direct3d_batch_capture_state(capture)
    state["pending"] = {
        "entry_index": 7,
        "file_offset": 0x0A6C,
        "form": 0x3C,
        "candidate": True,
        "capture": True,
        "families": {
            "family_a": {
                "root": 0x6200,
                "pages": [{
                    "vertex_pointer": 0x6300,
                    "vertex_count": 0,
                    "index_count": 0,
                }],
            },
        },
        "starts": {
            "family_a": [{
                "vertex_pointer": 0x6300,
                "vertex_count": 0,
                "index_count": 0,
            }],
        },
        "segments": [],
        "admission_evaluation": evaluation,
    }
    with pytest.raises(RuntimeError, match="prediction/count outcome mismatch"):
        harness._finalize_direct3d_record(FakeGdb(), capture, state)


def test_exact_admission_record_path_emits_only_the_receipt() -> None:
    class Memory:
        def __init__(self):
            self.values = {}

        def write(self, address, data):
            for offset, value in enumerate(data):
                self.values[address + offset] = value

        def read_memory(self, address, size):
            return bytes(self.values[address + offset] for offset in range(size))

    class Frame:
        pc_value = 0x111
        registers = {
            "esp": 0x7000, "esi": 0x8000,
            "edi": 0x6070, "ebp": 0,
        }

        @classmethod
        def pc(cls):
            return cls.pc_value

        @classmethod
        def read_register(cls, name):
            return cls.registers[name]

    memory = Memory()

    class FakeGdb:
        @staticmethod
        def selected_inferior():
            return memory

        @staticmethod
        def newest_frame():
            return Frame

    family = ev.Direct3DBatchFamily(
        id="family_a", flush_stop_pc=0x401,
        root_pointer_address=0x6100, allowed_roots=(0x6200,),
        vertex_pointer_table_offset=0, vertex_count_offset=8,
        index_base_offset=16, index_count_offset=32,
        index_page_stride=64, vertex_stride=4,
        max_vertex_count=16, max_index_count=32,
    )
    capture = ev.Direct3DBatchCapture(
        pre_trigger_id="pre", flush_trigger_id="flush", post_trigger_id="post",
        pre_stop_pcs=(0x111,), post_stop_pc=0x201,
        call_return_address=0x300, stack_pointer_register="esp",
        entry_return_stack_offset=16, entry_pointer_stack_offset=4,
        entry_index_stack_offset=8, post_entry_register="edi",
        page_register="ebp", entry_root=0x6000, entry_stride=16,
        entry_count=8, candidate_indices=(7,), pointer_size=4, page_count=1,
        families=(family,), max_digest_bytes_per_entry=1,
        warmup_rollovers=1, capture_cycles=1,
        capture_mode="exact_0a6c_admission", record_pointer_register="esi",
        record_forms=(ev.Direct3DRecordForm(0x3C, 0x111, 4, 6),),
        record_plan=(ev.Direct3DRecordPlanItem(7, 0x0A6C, 0x3C),),
        candidate_record_offsets=(0x0A6C,),
        allowed_outcome_family_id="family_a", allowed_outcome_page=0,
    )
    memory.write(0x7010, (0x300).to_bytes(4, "little"))
    memory.write(0x7004, (0x6070).to_bytes(4, "little"))
    memory.write(0x7008, (7).to_bytes(4, "little"))
    memory.write(0x6100, (0x6200).to_bytes(4, "little"))
    memory.write(0x6200, (0x6300).to_bytes(4, "little"))
    memory.write(0x6208, (0).to_bytes(2, "little"))
    memory.write(0x6220, (0).to_bytes(2, "little"))
    memory.write(0x8000, b"\x00" * 0x30)
    memory.write(0x802E, (0x1001).to_bytes(2, "little"))
    page_class_address = (
        harness.exact_admission.PAGE_CLASS_BASE
        + harness.exact_admission.EXACT_PAGE * 4
    )
    memory.write(page_class_address, (2).to_bytes(4, "little"))

    state = harness._new_direct3d_batch_capture_state(capture)
    state.update({
        "active": True,
        "last_post_index": 6,
        "cycle_base": 0x8000 - 0x0A6C,
    })
    assert harness._process_direct3d_batch_stop(
        FakeGdb(), ("watchpoint", "pre", 0, 2), capture, state
    ) is None
    Frame.pc_value = 0x201
    assert harness._process_direct3d_batch_stop(
        FakeGdb(), ("watchpoint", "post", 0, 4), capture, state
    ) == "capture_complete"
    receipt = state["cycles"][0]["records"][0]
    assert receipt["first_reject_pc"] == "0x00405FFF"
    assert receipt["predicted_append"] is False
    assert receipt["observed_append"] is False
    serialized = json.dumps(receipt)
    assert "source" not in serialized
    assert "vertex_count" not in serialized
    assert "index_count" not in serialized


def _three_cycle_exact_capture() -> ev.Direct3DBatchCapture:
    return ev.Direct3DBatchCapture(
        pre_trigger_id="pre", flush_trigger_id="flush", post_trigger_id="post",
        pre_stop_pcs=(0x111,), post_stop_pc=0x201,
        call_return_address=0x300, stack_pointer_register="esp",
        entry_return_stack_offset=16, entry_pointer_stack_offset=4,
        entry_index_stack_offset=8, post_entry_register="edi",
        page_register="ebp", entry_root=0x6000, entry_stride=16,
        entry_count=8, candidate_indices=(7,), pointer_size=4, page_count=1,
        families=(), max_digest_bytes_per_entry=1,
        warmup_rollovers=1, capture_cycles=3,
        capture_mode="exact_0a6c_admission", record_pointer_register="esi",
        record_forms=(ev.Direct3DRecordForm(0x3C, 0x111, 4, 6),),
        record_plan=(ev.Direct3DRecordPlanItem(7, 0x0A6C, 0x3C),),
        candidate_record_offsets=(0x0A6C,),
        allowed_outcome_family_id="family_a", allowed_outcome_page=0,
    )


def _exact_cycle_receipt(appended: bool, digest_byte: str = "a") -> dict:
    return {
        "schema_version": 1,
        "entry_index": 7,
        "file_offset": 0x0A6C,
        "form": 0x3C,
        "page_16_validated": True,
        "caller_mode_2_validated": True,
        "active_state_sha256": digest_byte * 64,
        "evaluated_predicate_count": 12 if appended else 7,
        "first_reject_pc": None if appended else "0x004065B0",
        "predicted_append": appended,
        "observed_append": appended,
        "prediction_matches_observation": True,
        "raw_inputs_retained": False,
        "payload_bytes_retained": 0,
    }


@pytest.mark.parametrize(
    "outcomes",
    [
        pytest.param((False, False, False), id="stable-reject"),
        pytest.param((True, True, True), id="stable-pass"),
        pytest.param((False, True, False), id="alternating"),
    ],
)
def test_exact_admission_fixed_three_cycle_outcome_sequences(
    outcomes: tuple[bool, bool, bool],
) -> None:
    capture = _three_cycle_exact_capture()
    state = harness._new_direct3d_batch_capture_state(capture)
    state.update({"active": True, "rollovers_seen": 1})

    for cycle_index, appended in enumerate(outcomes):
        state["plan_cursor"] = len(capture.record_plan)
        state["current_records"] = [
            _exact_cycle_receipt(appended, chr(ord("a") + cycle_index))
        ]
        reason = harness._finish_direct3d_record_cycle(capture, state)
        assert reason == (
            "capture_complete" if cycle_index == len(outcomes) - 1 else None
        )

    result = harness._direct3d_batch_capture_result(capture, state, True)
    assert result["completed"] is True
    assert result["capture_cycles_requested"] == 3
    assert result["rollovers_observed"] == 4
    assert [cycle["cycle_index"] for cycle in result["cycles"]] == [0, 1, 2]
    assert [
        cycle["records"][0]["observed_append"]
        for cycle in result["cycles"]
    ] == list(outcomes)
    serialized = json.dumps(result)
    for excluded in (
        "source_words", "classification_word", "projected_p", "projected_q",
        "projected_r", "vertex_count", "index_count", "watched_value_hex",
        "registers", "memory_reads", "raw_payload",
    ):
        assert excluded not in serialized


def test_exact_admission_incomplete_final_cycle_is_not_emitted() -> None:
    capture = _three_cycle_exact_capture()
    state = harness._new_direct3d_batch_capture_state(capture)
    state.update({"active": True, "rollovers_seen": 1})
    for appended in (False, True):
        state["plan_cursor"] = len(capture.record_plan)
        state["current_records"] = [_exact_cycle_receipt(appended)]
        assert harness._finish_direct3d_record_cycle(
            capture, state
        ) is None

    partial_marker = "f" * 64
    state["plan_cursor"] = len(capture.record_plan)
    state["current_records"] = [
        _exact_cycle_receipt(False, partial_marker[0])
    ]
    result = harness._direct3d_batch_capture_result(capture, state, False)
    assert result["completed"] is False
    assert len(result["cycles"]) == 2
    assert partial_marker not in json.dumps(result)


def test_exact_admission_rejects_an_unclosed_cycle() -> None:
    capture = _three_cycle_exact_capture()
    state = harness._new_direct3d_batch_capture_state(capture)
    state.update({"active": True, "plan_cursor": 0})
    with pytest.raises(RuntimeError, match="before the exact record plan"):
        harness._finish_direct3d_record_cycle(capture, state)


def test_exited_process_survival_probe_fails_closed(tmp_path: Path) -> None:
    exe = _compile_fixture(tmp_path)
    proc, _ = _spawn_fixture(exe, tmp_path)
    proc.terminate()
    proc.wait(timeout=5)
    target = {
        "exe_basename": exe.name,
        "expected_exe_sha256": ev.sha256_file(exe),
        "expected_loader_re": ".*",
        "expected_cwd_prefix": str(tmp_path) + os.sep,
    }
    config = {
        "required": True,
        "settle_ms": 0,
        "sample_count": 1,
        "sample_interval_ms": 0,
        "require_untraced": True,
        "require_resumed": True,
    }
    receipt = harness._collect_survival_receipt(proc.pid, target, config)
    assert receipt["passed"] is False
    assert receipt["identity_verified"] is False
    assert receipt["samples"][0]["passed"] is False

    result = {"completion": {"completed": True, "stop_reason": "timeout"}}
    completion = harness._apply_survival_receipt(
        result, receipt, required=True
    )["completion"]
    assert completion["stop_reason"] == "survival_failed"
    assert completion["completed"] is False
    assert completion["accepted"] is False


def test_timeout_path(tmp_path: Path) -> None:
    if shutil.which("gdb") is None:
        pytest.skip("gdb not available")
    exe = _compile_fixture(tmp_path)
    # touch=0 → the global is never modified, so an access watch never fires.
    proc, address = _spawn_fixture(exe, tmp_path, extra=("", "0"))
    try:
        spec = _base_spec(exe, tmp_path, proc.pid, address,
                          timeout_seconds=2, max_stops=5)
        spec_path = tmp_path / "spec.json"
        spec_path.write_text(json.dumps(spec))
        result = _run_harness(spec_path, tmp_path)
        assert result.returncode == 0, result.stderr + result.stdout

        run_dir = _latest_run(tmp_path)
        completion = json.loads((run_dir / "metadata.json").read_text())["completion"]
        assert completion["stop_reason"] == "timeout"
        assert completion["stops_observed"] == 0
        assert completion["cleanup_verified"] is True
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_milestone_target_reached(tmp_path: Path) -> None:
    if shutil.which("gdb") is None:
        pytest.skip("gdb not available")
    exe = _compile_fixture(tmp_path)
    logf = tmp_path / "game.log"
    # Pre-existing milestone line must NOT end the window.
    logf.write_text("MILESTONE\n")
    proc, address = _spawn_fixture(exe, tmp_path, extra=(str(logf), "0"))
    try:
        spec = _base_spec(exe, tmp_path, proc.pid, address,
                          timeout_seconds=20, max_stops=5,
                          end_milestones=["MILESTONE"], log_path=str(logf))
        spec_path = tmp_path / "spec.json"
        spec_path.write_text(json.dumps(spec))
        result = _run_harness(spec_path, tmp_path)
        assert result.returncode == 0, result.stderr + result.stdout

        run_dir = _latest_run(tmp_path)
        completion = json.loads((run_dir / "metadata.json").read_text())["completion"]
        assert completion["stop_reason"] == "target_reached"
    finally:
        proc.terminate()
        proc.wait(timeout=5)


def test_ownership_refusal_no_run_dir(tmp_path: Path) -> None:
    # A PID that exists but fails the loader check (this python process),
    # with an impossible loader regex.
    spec = {
        "schema_version": 1,
        "experiment_id": "EXP-20260812-999",
        "target": {
            "mode": "pid",
            "pid": os.getpid(),
            "exe_basename": "bugs.exe",
            "expected_loader_re": r"^/nonexistent/wine$",
            "expected_cwd_prefix": str(tmp_path) + os.sep,
        },
        "watchpoints": [{"id": "w0", "address": "0x400000", "kind": "access", "size": 4}],
        "breakpoints": [],
        "window": {"max_stops": 1, "timeout_seconds": 5, "end_milestones": [], "log_path": None},
        "on_stop": {"registers": [], "memory_reads": [], "backtrace_limit": 0},
    }
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec))
    result = _run_harness(spec_path, tmp_path)
    assert result.returncode == ev.EXIT_REFUSAL
    payload = json.loads(result.stdout)
    assert payload["refused"] is True
    assert payload["reason"] == "ownership"
    assert not list((tmp_path / "dynamic" / "wine").glob("RUN-GDB-*"))
