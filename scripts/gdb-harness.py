#!/usr/bin/env python3
"""Read-only GDB hardware-watchpoint harness for the Wine-hosted PC game.

This is one dual-mode file.

* **CLI mode** (run under the repo venv, e.g.
  ``.venv/bin/python scripts/gdb-harness.py --spec spec.json``): validates a
  watch specification, proves the target process identity from ``/proc`` before
  any ptrace, creates a ``dynamic/wine/RUN-GDB-<stamp>`` evidence directory, and
  launches gdb as a subprocess with this same file as ``-x`` script.
* **Controller mode** (running *inside* gdb because ``import gdb`` succeeds and
  ``ABLPC_GDB_RUNDIR`` is set): attaches, installs up to four hardware
  watch/breakpoints, runs a bounded window, writes one JSONL record per stop,
  then deletes every breakpoint and detaches on every exit path.

The harness is strictly read-only. It never writes target memory, registers,
code, or execution state; the only privileged actions are installing and
deleting its own hardware watch/breakpoints at a natural pause, which is the
method approved in DEC-20260812-006. Interpretation of the collected reads is
deliberately left to a linked experiment note.
"""

from __future__ import annotations

import os
import sys

# Make evidence_lib importable in both modes (gdb's embedded python does not
# put scripts/ on sys.path).
_SCRIPTS_DIR = os.environ.get("ABLPC_SCRIPTS_DIR") or os.path.dirname(
    os.path.abspath(__file__)
)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import evidence_lib as ev  # noqa: E402
import exact_0a6c_admission as exact_admission  # noqa: E402


TOOL = "gdb-harness"
TOOL_VERSION = "1.6.0"
SCHEMA_VERSION = 6

STOP_REASONS = (
    "capture_complete",
    "target_reached",
    "max_stops",
    "timeout",
    "detached",
    "target_exited",
    "target_signal",
    "survival_failed",
    "error",
)

DEFAULT_REGISTERS = (
    "rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp", "rip", "eflags",
)

# --------------------------------------------------------------------------
# Read-only command allowlist (pure; unit-testable without gdb)
# --------------------------------------------------------------------------

_ALLOWED_HEADS = frozenset({"attach", "continue", "detach", "info", "handle"})
_ALLOWED_SET_COMMANDS = frozenset({"set can-use-hw-watchpoints 1"})

# Signals the Wine-hosted target uses normally; gdb must pass them through
# without stopping. `pass` keeps delivering them to the game, so this changes
# only debugger interception, never the program.
WINE_PASS_SIGNALS = ("SIGUSR1", "SIGUSR2")
TARGET_TERMINAL_SIGNALS = (
    "SIGSEGV", "SIGILL", "SIGBUS", "SIGFPE", "SIGABRT", "SIGSYS",
)
SAFE_RESUMED_STATES = frozenset({"R", "S", "D", "I"})


class ReadOnlyViolation(Exception):
    """Raised when a gdb command outside the read-only allowlist is attempted."""


def check_gdb_command(command: str) -> str:
    """Return the command if it is on the read-only allowlist, else raise."""

    stripped = command.strip()
    if not stripped:
        raise ReadOnlyViolation("empty gdb command")
    head = stripped.split()[0]
    if head == "set":
        if stripped not in _ALLOWED_SET_COMMANDS:
            raise ReadOnlyViolation(f"disallowed set command: {command!r}")
        return command
    if head not in _ALLOWED_HEADS:
        raise ReadOnlyViolation(f"disallowed gdb command: {command!r}")
    return command


def capabilities() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "mode": "read-only",
        "verbs": [
            "attach", "install-hw-watchpoint", "install-hw-breakpoint",
            "read-memory", "read-registers", "backtrace", "detach",
        ],
        "write_verbs": [],
        "limits": {
            "hw_slots": ev.HW_SLOTS,
            "watch_sizes": list(ev.WATCH_SIZES),
            "watch_kinds": list(ev.WATCH_KINDS),
            "max_memory_read_bytes": ev.MAX_MEMORY_READ_BYTES,
            "max_memory_reads_per_stop": ev.MAX_MEMORY_READS,
            "max_stops": ev.MAX_STOPS,
            "max_timeout_seconds": ev.MAX_TIMEOUT_SECONDS,
            "max_backtrace": ev.MAX_BACKTRACE,
            "max_submission_digest_bytes": ev.MAX_SUBMISSION_DIGEST_BYTES,
            "max_submission_capacity_records":
                ev.MAX_SUBMISSION_CAPACITY_RECORDS,
            "max_batch_digest_bytes": ev.MAX_BATCH_DIGEST_BYTES,
            "max_batch_pages": ev.MAX_BATCH_PAGES,
        },
        "stop_reasons": list(STOP_REASONS),
        "spec_schema_version": ev.SPEC_SCHEMA_VERSION,
        "supported_spec_schema_versions": list(ev.SUPPORTED_SPEC_SCHEMA_VERSIONS),
        "target_terminal_signals": list(TARGET_TERMINAL_SIGNALS),
        "survival_receipt": {
            "schema_version": 1,
            "probe": "proc-identity-state-tracer",
            "max_window_ms": ev.MAX_SURVIVAL_WINDOW_MS,
        },
        "submission_capture": {
            "schema_version": 1,
            "algorithm": "sha256",
            "retains_payload_bytes": False,
            "interval_modes": ["paired", "zero_post"],
            "requires_ordered_triggers": True,
            "supports_exact_stop_pc_filters": True,
        },
        "direct3d_batch_capture": {
            "schema_version": 3,
            "algorithms": [
                "sha256", "count-delta", "native-first-reject",
            ],
            "capture_modes": [
                "entry_digest", "record_outcome", "exact_0a6c_admission",
            ],
            "retains_payload_bytes": False,
            "requires_ordered_pre_flush_post_triggers": True,
            "supports_exact_stop_pc_filters": True,
            "supports_pre_reset_flush_segments": True,
            "supports_exact_record_plans": True,
            "supports_exact_0a6c_first_reject": True,
            "supports_exact_0a6c_consecutive_cycles": True,
            "exact_0a6c_consecutive_capture_cycles": (
                exact_admission.EXACT_CONSECUTIVE_CAPTURE_CYCLES
            ),
            "exact_0a6c_requires_existing_pid": True,
            "exact_0a6c_retains_raw_stop_values": False,
        },
    }


def _direct3d_watch_condition(capture, trigger_id):
    if capture is None:
        return None
    if trigger_id == capture.pre_trigger_id:
        pc_terms = " || ".join(
            f"$pc == 0x{pc:x}" for pc in capture.pre_stop_pcs
        )
        uint_type = "unsigned int" if capture.pointer_size == 4 else (
            "unsigned long long"
        )
        return (
            f"({pc_terms}) && *({uint_type} *)"
            f"(${capture.stack_pointer_register} + "
            f"{capture.entry_return_stack_offset}) == "
            f"0x{capture.call_return_address:x}"
        )
    if trigger_id == capture.flush_trigger_id:
        return " || ".join(
            f"$pc == 0x{family.flush_stop_pc:x}"
            for family in capture.families
        )
    if trigger_id == capture.post_trigger_id:
        return f"$pc == 0x{capture.post_stop_pc:x}"
    return None


# ==========================================================================
# Controller mode (runs inside gdb)
# ==========================================================================


def run_controller() -> None:
    import json
    import threading
    import time

    import gdb  # available only inside gdb

    rundir = os.environ["ABLPC_GDB_RUNDIR"]
    pid = int(os.environ["ABLPC_GDB_TARGET_PID"])
    with open(os.environ["ABLPC_GDB_SPEC"], encoding="utf-8") as handle:
        raw_spec = json.load(handle)
    spec = ev.validate_watch_spec(raw_spec)

    ctype = {1: "unsigned char", 2: "unsigned short", 4: "unsigned int"}
    wp_class = {
        "read": gdb.WP_READ,
        "write": gdb.WP_WRITE,
        "access": gdb.WP_ACCESS,
    }

    stops_path = os.path.join(rundir, "stops.jsonl")
    result_path = os.path.join(rundir, "result.json")
    evidence_path = os.path.join(rundir, "debugger-evidence.txt")

    window = spec.window
    max_stops = window.get("max_stops", ev.MAX_STOPS)
    timeout_seconds = window.get("timeout_seconds", ev.MAX_TIMEOUT_SECONDS)
    milestones = list(window.get("end_milestones") or [])
    log_path = window.get("log_path")
    log_start_offset = 0
    if log_path and os.path.isfile(log_path):
        log_start_offset = os.path.getsize(log_path)

    exact_admission_capture = (
        spec.direct3d_batch_capture is not None
        and spec.direct3d_batch_capture.capture_mode
        == "exact_0a6c_admission"
    )
    registers = (
        list(spec.registers)
        if exact_admission_capture
        else list(spec.registers) or list(DEFAULT_REGISTERS)
    )

    state = {
        "end_reason": None,     # set by monitor thread
        "done": threading.Event(),
        "exited": False,
        "exit_code": None,
        "last_event": None,
        "target_signal": None,
    }

    def on_stop(event: "gdb.StopEvent") -> None:  # noqa: F821
        state["last_event"] = event

    def on_exited(event) -> None:
        state["exited"] = True
        state["exit_code"] = getattr(event, "exit_code", None)

    gdb.events.stop.connect(on_stop)
    gdb.events.exited.connect(on_exited)

    started = ev.now().isoformat()
    t0 = time.monotonic()
    deadline = t0 + timeout_seconds

    def monitor() -> None:
        while not state["done"].wait(0.1):
            if state["end_reason"] is not None:
                return
            if time.monotonic() >= deadline:
                state["end_reason"] = "timeout"
                _safe_interrupt(gdb)
                return
            if milestones and log_path and os.path.isfile(log_path):
                try:
                    with open(log_path, "rb") as handle:
                        handle.seek(log_start_offset)
                        appended = handle.read().decode("utf-8", "replace")
                except OSError:
                    appended = ""
                if any(m in appended for m in milestones):
                    state["end_reason"] = "target_reached"
                    _safe_interrupt(gdb)
                    return

    installed_watch: list = []
    installed_break: list = []
    bp_to_spec: dict = {}
    stop_records: list = []
    capture_state = _new_submission_capture_state(spec.submission_capture)
    batch_state = _new_direct3d_batch_capture_state(
        spec.direct3d_batch_capture
    )
    error_detail = None
    attached = False
    cleanup_verified = False
    detached = False

    stops_file = open(stops_path, "w", encoding="utf-8")
    monitor_thread = threading.Thread(target=monitor, daemon=True)

    try:
        gdb.execute(check_gdb_command("set can-use-hw-watchpoints 1"), to_string=True)
        gdb.execute(check_gdb_command(f"attach {pid}"), to_string=True)
        attached = True

        # Pass Wine's normal thread signals through without stopping. Each is
        # issued separately so an unrecognized name cannot abort the batch.
        for sig in WINE_PASS_SIGNALS:
            try:
                gdb.execute(check_gdb_command(f"handle {sig} nostop noprint pass"),
                            to_string=True)
            except gdb.error:
                pass
        # Unexpected fatal signals are evidence endpoints, not signals to pass
        # through. `nopass` is intentional: fixture validation demonstrates
        # that cleanup/detach does not deliver an injected pending signal.
        for sig in TARGET_TERMINAL_SIGNALS:
            try:
                gdb.execute(check_gdb_command(f"handle {sig} stop print nopass"),
                            to_string=True)
            except gdb.error:
                pass

        for wp in spec.watchpoints:
            expr = f"*({ctype[wp.size]} *)0x{wp.address:x}"
            bp = gdb.Breakpoint(expr, type=gdb.BP_WATCHPOINT, wp_class=wp_class[wp.kind])
            condition = _direct3d_watch_condition(
                spec.direct3d_batch_capture, wp.id
            )
            if condition is not None:
                bp.condition = condition
            installed_watch.append(bp)
            bp_to_spec[id(bp)] = ("watchpoint", wp.id, wp.address, wp.size)
        for brk in spec.breakpoints:
            bp = gdb.Breakpoint(f"*0x{brk.address:x}", type=gdb.BP_HARDWARE_BREAKPOINT)
            installed_break.append(bp)
            bp_to_spec[id(bp)] = ("breakpoint", brk.id, brk.address, None)

        monitor_thread.start()

        seq = 0
        while True:
            if state["end_reason"] is not None:
                break
            if len(stop_records) >= max_stops:
                state["end_reason"] = "max_stops"
                break
            state["last_event"] = None
            try:
                gdb.execute(check_gdb_command("continue"), to_string=True)
            except gdb.error as exc:
                if state["exited"] or "not being run" in str(exc):
                    state["end_reason"] = "target_exited"
                    break
                error_detail = str(exc)
                state["end_reason"] = "error"
                break
            if state["exited"]:
                state["end_reason"] = "target_exited"
                break
            event = state["last_event"]
            hit = _match_breakpoint(event, bp_to_spec)
            if hit is None:
                stop_signal = getattr(event, "stop_signal", None)
                # Inspect a real target signal before honoring a concurrently
                # observed log milestone. This prevents a milestone from
                # hiding the fatal stop that actually ended target survival.
                if stop_signal and stop_signal != "SIGINT":
                    if stop_signal in WINE_PASS_SIGNALS:
                        continue
                    state["target_signal"] = _build_signal_record(
                        gdb, stop_signal,
                        "fatal" if stop_signal in TARGET_TERMINAL_SIGNALS
                        else "unexpected",
                        "stop-print-nopass"
                        if stop_signal in TARGET_TERMINAL_SIGNALS
                        else "gdb-default-no-continue",
                    )
                    state["end_reason"] = "target_signal"
                    break
                # Not one of our breakpoints. If the monitor set an end reason
                # (timeout/milestone) its interrupt lands here, so end.
                if state["end_reason"] is not None:
                    break
                # A bare SIGINT with no monitor reason, or an unclassified stop.
                state["end_reason"] = "detached"
                break
            seq += 1
            record = _build_stop_record(
                gdb, seq, t0, hit, registers, spec.memory_reads,
                spec.backtrace_limit, redact_values=exact_admission_capture,
            )
            stop_records.append(record)
            stops_file.write(json.dumps(record) + "\n")
            stops_file.flush()
            if spec.submission_capture is not None:
                capture_end = _process_submission_stop(
                    gdb, hit, spec.submission_capture, capture_state
                )
                if capture_end is not None:
                    state["end_reason"] = capture_end
                    if capture_end == "error":
                        error_detail = capture_state["failure"]
            elif spec.direct3d_batch_capture is not None:
                capture_end = _process_direct3d_batch_stop(
                    gdb, hit, spec.direct3d_batch_capture, batch_state
                )
                if capture_end is not None:
                    state["end_reason"] = capture_end
                    if capture_end == "error":
                        error_detail = batch_state["failure"]
    except Exception as exc:  # pragma: no cover - defensive
        error_detail = (
            "exact_0a6c_admission:controller_failed_closed"
            if exact_admission_capture
            else f"{type(exc).__name__}: {exc}"
        )
        if state["end_reason"] is None:
            state["end_reason"] = "error"
    finally:
        state["done"].set()
        if monitor_thread.is_alive():
            monitor_thread.join(timeout=2)
        stops_file.close()

        deleted_watch = _delete_all(installed_watch)
        deleted_break = _delete_all(installed_break)
        try:
            remaining = [b for b in (gdb.breakpoints() or [])
                         if id(b) in bp_to_spec]
            cleanup_verified = not remaining
        except Exception:  # pragma: no cover
            cleanup_verified = False
        if attached:
            try:
                gdb.execute(check_gdb_command("detach"), to_string=True)
                detached = True
            except Exception:  # pragma: no cover
                detached = False

        end_reason = state["end_reason"] or "error"
        if (
            spec.submission_capture is not None
            or spec.direct3d_batch_capture is not None
        ):
            completed = end_reason == "capture_complete"
        else:
            completed = end_reason in (
                "target_reached", "max_stops", "timeout", "target_exited",
                "detached",
            )
        completion = {
            "completed": completed,
            "accepted": completed,
            "stop_reason": end_reason,
            "stops_observed": len(stop_records),
            "watchpoints_installed": len(installed_watch),
            "watchpoints_deleted": deleted_watch,
            "breakpoints_installed": len(installed_break),
            "breakpoints_deleted": deleted_break,
            "cleanup_verified": cleanup_verified,
            "detached": detached,
            "target_signal": state["target_signal"],
            "error": error_detail,
        }
        result = {
            "tool": TOOL,
            "tool_version": TOOL_VERSION,
            "schema_version": SCHEMA_VERSION,
            "spec_schema_version": spec.schema_version,
            "time_window_start": started,
            "time_window_end": ev.now().isoformat(),
            "log_start_offset": log_start_offset,
            "completion": completion,
        }
        if capture_state is not None:
            result["submission_capture"] = _submission_capture_result(
                spec.submission_capture, capture_state, completed
            )
        if batch_state is not None:
            result["direct3d_batch_capture"] = _direct3d_batch_capture_result(
                spec.direct3d_batch_capture, batch_state, completed
            )
        with open(result_path, "w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2)
        _write_evidence_draft(evidence_path, spec, result, stop_records)


def _safe_interrupt(gdb) -> None:
    try:
        gdb.interrupt()
    except Exception:  # pragma: no cover - defensive
        pass


def _match_breakpoint(event, bp_to_spec):
    breakpoints = getattr(event, "breakpoints", None) if event else None
    if not breakpoints:
        return None
    for bp in breakpoints:
        info = bp_to_spec.get(id(bp))
        if info is not None:
            return info
    return None


def _delete_all(breakpoints) -> int:
    deleted = 0
    for bp in breakpoints:
        try:
            bp.delete()
            deleted += 1
        except Exception:  # pragma: no cover - defensive
            pass
    return deleted


def _build_stop_record(
    gdb, seq, t0, hit, registers, memory_reads, backtrace_limit,
    redact_values=False,
):
    import time

    kind, trigger_id, address, size = hit
    inferior = gdb.selected_inferior()
    frame = None
    try:
        frame = gdb.newest_frame()
    except gdb.error:  # pragma: no cover - defensive
        frame = None

    reg_values = {}
    if frame is not None and not redact_values:
        for name in registers:
            try:
                value = int(frame.read_register(name)) & 0xFFFFFFFFFFFFFFFF
                reg_values[name] = f"0x{value:x}"
            except Exception:
                reg_values[name] = None

    pc = None
    if frame is not None:
        try:
            pc = f"0x{frame.pc() & 0xFFFFFFFFFFFFFFFF:x}"
        except Exception:  # pragma: no cover
            pc = None

    watched_value = None
    if kind == "watchpoint" and not redact_values:
        watched_value = _read_hex(inferior, address, size)

    reads = []
    if not redact_values:
        for read in memory_reads:
            hexval = _read_hex(inferior, read.address, read.size)
            reads.append({
                "id": read.id,
                "address": f"0x{read.address:x}",
                "size": read.size,
                "ok": hexval is not None,
                "hex": hexval,
            })

    backtrace = []
    truncated = False
    if frame is not None and backtrace_limit:
        f = frame
        while f is not None and len(backtrace) < backtrace_limit:
            try:
                backtrace.append(f"0x{f.pc() & 0xFFFFFFFFFFFFFFFF:x}")
                f = f.older()
            except Exception:  # pragma: no cover
                break
        if f is not None:
            truncated = True

    return {
        "schema_version": SCHEMA_VERSION,
        "seq": seq,
        "t_mono_ns": int((time.monotonic() - t0) * 1e9),
        "t_wall": ev.now().isoformat(),
        "kind": kind,
        "trigger_id": trigger_id,
        "pc": pc,
        "registers": reg_values,
        "watched_value_hex": watched_value,
        "memory_reads": reads,
        "backtrace_pcs": backtrace,
        "backtrace_truncated": truncated,
    }


def _build_signal_record(gdb, signal_name, classification, delivery_policy):
    pc = None
    try:
        frame = gdb.newest_frame()
        if frame is not None:
            pc = f"0x{frame.pc() & 0xFFFFFFFFFFFFFFFF:x}"
    except Exception:  # pragma: no cover - defensive
        pass
    return {
        "schema_version": 1,
        "name": signal_name,
        "classification": classification,
        "pc": pc,
        "t_wall": ev.now().isoformat(),
        "delivery_policy": delivery_policy,
    }


def _read_hex(inferior, address, size):
    try:
        buf = inferior.read_memory(address, size)
        return bytes(buf).hex()
    except Exception:
        return None


def _new_submission_capture_state(capture):
    if capture is None:
        return None
    return {
        "active": False,
        "last_pre_index": None,
        "pending": None,
        "rollovers_seen": 0,
        "current_entries": [],
        "cycles": [],
        "failure": None,
    }


def _capture_fail(state, detail):
    state["failure"] = detail
    return "error"


def _capture_fail_for_mode(capture, state, exc):
    if capture.capture_mode != "exact_0a6c_admission":
        return _capture_fail(state, str(exc))
    detail = str(exc)
    categories = (
        ("classification validation failed", "source_classification_mismatch"),
        ("native signed division failed closed", "native_division_failure"),
        ("active-state read failed closed", "active_state_read_failure"),
        ("evaluation metadata validation failed", "evaluation_metadata_invalid"),
        ("active-state digest changed", "active_state_digest_changed"),
        ("prediction/count outcome mismatch", "prediction_count_mismatch"),
        ("target call flushed", "target_call_flushed"),
        ("evaluation is missing", "evaluation_missing"),
    )
    code = next(
        (code for phrase, code in categories if phrase in detail),
        "capture_structure_mismatch",
    )
    return _capture_fail(state, f"exact_0a6c_admission:{code}")


def _read_uint(inferior, address, size, label):
    try:
        raw = bytes(inferior.read_memory(address, size))
    except Exception as exc:
        raise RuntimeError(f"cannot read {label}: {type(exc).__name__}") from exc
    if len(raw) != size:
        raise RuntimeError(f"short read for {label}")
    return int.from_bytes(raw, "little", signed=False)


def _submission_index(gdb, capture):
    try:
        frame = gdb.newest_frame()
        pointer = int(frame.read_register(capture.entry_register))
    except Exception as exc:
        raise RuntimeError(
            f"cannot read entry register {capture.entry_register}"
        ) from exc
    maximum = (1 << (capture.pointer_size * 8)) - 1
    pointer &= maximum
    delta = pointer - capture.entry_root
    if delta < 0 or delta % capture.entry_stride:
        raise RuntimeError("entry pointer is outside the exact entry lattice")
    index = delta // capture.entry_stride
    if index >= capture.entry_count:
        raise RuntimeError("entry pointer index is outside entry_count")
    return index


def _read_submission_bounds(gdb, capture):
    inferior = gdb.selected_inferior()
    counter = _read_uint(inferior, capture.counter_address, 4, "counter")
    capacity = _read_uint(inferior, capture.capacity_address, 4, "capacity")
    base = _read_uint(
        inferior, capture.base_pointer_address, capture.pointer_size,
        "base pointer",
    )
    if capacity > ev.MAX_SUBMISSION_CAPACITY_RECORDS:
        raise RuntimeError("submission capacity is outside the hard bound")
    # The exact native initializer sets capacity and base together. Before it
    # runs, the all-zero triple is a coherent inactive arena and can safely
    # describe only a zero-length interval; no target bytes will be read.
    if capacity == 0:
        if counter != 0 or base != 0:
            raise RuntimeError("inactive submission arena has nonzero state")
        return counter, capacity, base
    if counter > capacity:
        raise RuntimeError("submission counter exceeds capacity")
    if base == 0:
        raise RuntimeError("submission base pointer is null")
    maximum = (1 << (capture.pointer_size * 8)) - 1
    arena_bytes = capacity * capture.output_stride
    if base > maximum or arena_bytes > maximum - base:
        raise RuntimeError("submission arena address range overflows")
    return counter, capacity, base


def _finalize_submission_cycle(capture, state):
    entries = state["current_entries"]
    expected = list(capture.candidate_indices)
    observed = [entry["entry_index"] for entry in entries]
    if observed != expected:
        raise RuntimeError(
            f"candidate sequence mismatch: expected {expected}, observed {observed}"
        )
    state["cycles"].append({
        "cycle_index": len(state["cycles"]),
        "entries": entries,
    })
    state["current_entries"] = []


def _process_submission_stop(gdb, hit, capture, state):
    import hashlib

    _kind, trigger_id, _address, _size = hit
    if capture.interval_mode == "zero_post":
        if trigger_id != capture.post_trigger_id:
            return _capture_fail(
                state, f"unexpected zero-post trigger {trigger_id!r}"
            )
        try:
            if capture.post_stop_pc is not None:
                observed_pc = int(gdb.newest_frame().pc())
                if observed_pc != capture.post_stop_pc:
                    return None
            index = _submission_index(gdb, capture)
            counter, capacity, base = _read_submission_bounds(gdb, capture)
            if (counter, capacity, base) != (0, 0, 0):
                raise RuntimeError(
                    "zero-post capture observed an active submission arena"
                )

            last_index = state["last_pre_index"]
            if last_index is not None and index <= last_index:
                if last_index != capture.entry_count - 1 or index != 0:
                    raise RuntimeError(
                        f"non-canonical entry rollover {last_index}->{index}"
                    )
                state["rollovers_seen"] += 1
                if state["active"]:
                    _finalize_submission_cycle(capture, state)
                    if len(state["cycles"]) >= capture.capture_cycles:
                        return "capture_complete"
                elif state["rollovers_seen"] >= capture.warmup_rollovers:
                    state["active"] = True
                    state["current_entries"] = []

            if state["active"]:
                expected_index = 0 if last_index is None else last_index + 1
                if index == 0:
                    expected_index = 0
                if index != expected_index:
                    raise RuntimeError(
                        f"non-contiguous entry order: expected {expected_index}, "
                        f"observed {index}"
                    )
                if index in capture.candidate_indices:
                    state["current_entries"].append({
                        "entry_index": index,
                        "pre_counter": 0,
                        "post_counter": 0,
                        "record_count": 0,
                        "byte_count": 0,
                        "sha256": hashlib.sha256(b"").hexdigest(),
                    })
            state["last_pre_index"] = index
            return None
        except Exception as exc:
            return _capture_fail(state, str(exc))

    if trigger_id not in (capture.pre_trigger_id, capture.post_trigger_id):
        return _capture_fail(state, f"unexpected capture trigger {trigger_id!r}")
    try:
        expected_pc = (
            capture.pre_stop_pc
            if trigger_id == capture.pre_trigger_id
            else capture.post_stop_pc
        )
        if expected_pc is not None:
            try:
                observed_pc = int(gdb.newest_frame().pc())
            except Exception as exc:
                raise RuntimeError("cannot read capture stop PC") from exc
            # Data watchpoints report the PC after the access instruction and
            # can share their watched address with unrelated accesses. Those
            # non-matching stops remain in stops.jsonl for audit but do not
            # enter the ordered capture state machine.
            if observed_pc != expected_pc:
                return None
        index = _submission_index(gdb, capture)
        if trigger_id == capture.pre_trigger_id:
            if state["pending"] is not None:
                raise RuntimeError("pre trigger arrived before paired post trigger")

            last_index = state["last_pre_index"]
            if last_index is not None and index <= last_index:
                if last_index != capture.entry_count - 1 or index != 0:
                    raise RuntimeError(
                        f"non-canonical entry rollover {last_index}->{index}"
                    )
                state["rollovers_seen"] += 1
                if state["active"]:
                    _finalize_submission_cycle(capture, state)
                    if len(state["cycles"]) >= capture.capture_cycles:
                        return "capture_complete"
                elif state["rollovers_seen"] >= capture.warmup_rollovers:
                    state["active"] = True
                    state["current_entries"] = []

            if state["active"]:
                expected_index = (
                    0 if not state["current_entries"]
                    else state["current_entries"][-1]["entry_index"] + 1
                )
                # Entry 8 is deliberately not retained in the candidate list,
                # so validate the complete native order from last_pre_index.
                if index == 0:
                    expected_index = 0
                elif last_index is not None:
                    expected_index = last_index + 1
                if index != expected_index:
                    raise RuntimeError(
                        f"non-contiguous entry order: expected {expected_index}, "
                        f"observed {index}"
                    )

            pre_counter, capacity, base = _read_submission_bounds(gdb, capture)
            state["pending"] = {
                "entry_index": index,
                "capture": state["active"],
                "pre_counter": pre_counter,
                "capacity": capacity,
                "base": base,
            }
            state["last_pre_index"] = index
            return None

        pending = state["pending"]
        if pending is None:
            raise RuntimeError("post trigger arrived without paired pre trigger")
        if pending["entry_index"] != index:
            raise RuntimeError(
                f"pre/post entry mismatch {pending['entry_index']}->{index}"
            )
        post_counter, capacity, base = _read_submission_bounds(gdb, capture)
        if capacity != pending["capacity"] or base != pending["base"]:
            raise RuntimeError("submission arena bounds changed within interval")
        if post_counter < pending["pre_counter"]:
            raise RuntimeError("submission counter decreased within interval")
        record_count = post_counter - pending["pre_counter"]
        if record_count > capture.max_records_per_entry:
            raise RuntimeError("per-entry record count exceeds configured bound")
        byte_count = record_count * capture.output_stride
        start = base + pending["pre_counter"] * capture.output_stride
        end = start + byte_count
        arena_end = base + capacity * capture.output_stride
        if start < base or end < start or end > arena_end:
            raise RuntimeError("new-record interval is outside submission arena")

        if pending["capture"] and index in capture.candidate_indices:
            inferior = gdb.selected_inferior()
            if byte_count:
                try:
                    payload = bytes(inferior.read_memory(start, byte_count))
                except Exception as exc:
                    raise RuntimeError(
                        "cannot read bounded new-record interval: "
                        f"{type(exc).__name__}"
                    ) from exc
            else:
                payload = b""
            if len(payload) != byte_count:
                raise RuntimeError("short read for bounded new-record interval")
            state["current_entries"].append({
                "entry_index": index,
                "pre_counter": pending["pre_counter"],
                "post_counter": post_counter,
                "record_count": record_count,
                "byte_count": byte_count,
                "sha256": hashlib.sha256(payload).hexdigest(),
            })
        state["pending"] = None
        return None
    except Exception as exc:
        state["pending"] = None
        return _capture_fail(state, str(exc))


def _submission_capture_result(capture, state, completed):
    return {
        "schema_version": 1,
        "completed": completed,
        "algorithm": "sha256",
        "interval_mode": capture.interval_mode,
        "payload_bytes_retained": False,
        "candidate_indices": list(capture.candidate_indices),
        "warmup_rollovers_required": capture.warmup_rollovers,
        "rollovers_observed": state["rollovers_seen"],
        "capture_cycles_requested": capture.capture_cycles,
        "cycles": state["cycles"],
        "failure": state["failure"],
    }


def _new_direct3d_batch_capture_state(capture):
    if capture is None:
        return None
    state = {
        "active": False,
        "last_pre_index": None,
        "last_post_index": None,
        "rollover_started": False,
        "pending": None,
        "rollovers_seen": 0,
        "current_entries": [],
        "cycles": [],
        "failure": None,
        "segment_sequence": 0,
        "ignored_unmatched_flushes": 0,
    }
    if capture.capture_mode in (
        "record_outcome", "exact_0a6c_admission",
    ):
        state.update({
            "plan_cursor": 0,
            "cycle_base": None,
            "current_records": [],
        })
    return state


def _batch_register(gdb, name, pointer_size):
    try:
        value = int(gdb.newest_frame().read_register(name))
    except Exception as exc:
        raise RuntimeError(f"cannot read register {name}") from exc
    return value & ((1 << (pointer_size * 8)) - 1)


def _batch_lattice_index(pointer, capture):
    delta = pointer - capture.entry_root
    if delta < 0 or delta % capture.entry_stride:
        raise RuntimeError(
            f"entry pointer 0x{pointer:x} is outside the exact entry lattice"
        )
    index = delta // capture.entry_stride
    if index >= capture.entry_count:
        raise RuntimeError("entry pointer index is outside entry_count")
    return index


def _batch_pre_index(gdb, capture):
    inferior = gdb.selected_inferior()
    stack = _batch_register(
        gdb, capture.stack_pointer_register, capture.pointer_size
    )
    return_address = _read_uint(
        inferior, stack + capture.entry_return_stack_offset,
        capture.pointer_size, "batch caller return address",
    )
    if return_address != capture.call_return_address:
        return None
    pointer = _read_uint(
        inferior, stack + capture.entry_pointer_stack_offset,
        capture.pointer_size, "batch entry pointer",
    )
    index = _batch_lattice_index(pointer, capture)
    saved_index = _read_uint(
        inferior, stack + capture.entry_index_stack_offset,
        4, "batch saved entry index",
    )
    if saved_index != index:
        raise RuntimeError(
            f"batch saved entry index mismatch {saved_index}->{index}"
        )
    return index


def _batch_post_index(gdb, capture):
    pointer = _batch_register(gdb, capture.post_entry_register,
                              capture.pointer_size)
    return _batch_lattice_index(pointer, capture)


def _read_batch_root(inferior, capture, family):
    root = _read_uint(
        inferior, family.root_pointer_address, capture.pointer_size,
        f"{family.id} root pointer",
    )
    if root not in family.allowed_roots:
        raise RuntimeError(
            f"{family.id} root pointer 0x{root:x} is outside its allowlist"
        )
    return root


def _read_batch_family_snapshot(inferior, capture, family):
    root = _read_batch_root(inferior, capture, family)
    pointer_bytes = bytes(inferior.read_memory(
        root + family.vertex_pointer_table_offset,
        capture.page_count * capture.pointer_size,
    ))
    vertex_count_bytes = bytes(inferior.read_memory(
        root + family.vertex_count_offset, capture.page_count * 2,
    ))
    index_count_bytes = bytes(inferior.read_memory(
        root + family.index_count_offset, capture.page_count * 2,
    ))
    if len(pointer_bytes) != capture.page_count * capture.pointer_size:
        raise RuntimeError(f"short read for {family.id} vertex pointer table")
    if len(vertex_count_bytes) != capture.page_count * 2:
        raise RuntimeError(f"short read for {family.id} vertex count table")
    if len(index_count_bytes) != capture.page_count * 2:
        raise RuntimeError(f"short read for {family.id} index count table")
    pages = []
    maximum = (1 << (capture.pointer_size * 8)) - 1
    for page in range(capture.page_count):
        pointer_start = page * capture.pointer_size
        vertex_pointer = int.from_bytes(
            pointer_bytes[pointer_start:pointer_start + capture.pointer_size],
            "little", signed=False,
        )
        vertex_count = int.from_bytes(
            vertex_count_bytes[page * 2:page * 2 + 2],
            "little", signed=False,
        )
        index_count = int.from_bytes(
            index_count_bytes[page * 2:page * 2 + 2],
            "little", signed=False,
        )
        if vertex_pointer == 0 and (vertex_count or index_count):
            raise RuntimeError(
                f"{family.id} page {page} has counts with a null vertex pointer"
            )
        if vertex_count > family.max_vertex_count:
            raise RuntimeError(f"{family.id} page {page} vertex count exceeds bound")
        if index_count > family.max_index_count:
            raise RuntimeError(f"{family.id} page {page} index count exceeds bound")
        maximum_vertex_bytes = family.max_vertex_count * family.vertex_stride
        if vertex_pointer and vertex_pointer > maximum - maximum_vertex_bytes:
            raise RuntimeError(
                f"{family.id} page {page} vertex address range overflows"
            )
        index_address = (
            root + family.index_base_offset + page * family.index_page_stride
        )
        if index_address > maximum - family.index_page_stride:
            raise RuntimeError(
                f"{family.id} page {page} index address range overflows"
            )
        pages.append({
            "vertex_pointer": vertex_pointer,
            "vertex_count": vertex_count,
            "index_count": index_count,
        })
    return {"root": root, "pages": pages}


def _read_batch_page(inferior, capture, family, page):
    root = _read_batch_root(inferior, capture, family)
    vertex_pointer = _read_uint(
        inferior,
        root + family.vertex_pointer_table_offset
        + page * capture.pointer_size,
        capture.pointer_size, f"{family.id} page {page} vertex pointer",
    )
    vertex_count = _read_uint(
        inferior, root + family.vertex_count_offset + page * 2,
        2, f"{family.id} page {page} vertex count",
    )
    index_count = _read_uint(
        inferior, root + family.index_count_offset + page * 2,
        2, f"{family.id} page {page} index count",
    )
    if vertex_pointer == 0:
        raise RuntimeError(f"{family.id} page {page} vertex pointer is null")
    if vertex_count > family.max_vertex_count:
        raise RuntimeError(f"{family.id} page {page} vertex count exceeds bound")
    if index_count > family.max_index_count:
        raise RuntimeError(f"{family.id} page {page} index count exceeds bound")
    return root, {
        "vertex_pointer": vertex_pointer,
        "vertex_count": vertex_count,
        "index_count": index_count,
    }


def _read_exact_0a6c_evaluation(gdb, capture):
    inferior = gdb.selected_inferior()
    source_pointer = _batch_register(
        gdb, capture.record_pointer_register, capture.pointer_size
    )
    source_offsets = (
        (0x04, 0x06, 0x08),
        (0x0C, 0x0E, 0x10),
        (0x1C, 0x1E, 0x20),
        (0x14, 0x16, 0x18),
    )
    source_words = tuple(
        tuple(
            _read_uint(
                inferior, source_pointer + offset, 2,
                "exact admission source word",
            )
            for offset in offsets
        )
        for offsets in source_offsets
    )
    classification_word = _read_uint(
        inferior, source_pointer + 0x2E, 2,
        "exact admission classification word",
    )

    def read_u32(address):
        return _read_uint(inferior, address, 4, "exact admission active state")

    return exact_admission.evaluate_exact_0a6c(
        source_words, classification_word, read_u32
    )


def _batch_segment(gdb, capture, state, pending, family, page,
                   observed, flushed):
    import hashlib

    start = pending["starts"][family.id][page]
    start_vertex = start["vertex_count"]
    start_index = start["index_count"]
    end_vertex = observed["vertex_count"]
    end_index = observed["index_count"]
    if end_vertex < start_vertex or end_index < start_index:
        raise RuntimeError(
            f"{family.id} page {page} counter decreased without captured flush"
        )
    if observed["vertex_pointer"] != start["vertex_pointer"]:
        raise RuntimeError(f"{family.id} page {page} vertex pointer changed")
    vertex_count = end_vertex - start_vertex
    index_count = end_index - start_index
    vertex_byte_count = vertex_count * family.vertex_stride
    index_byte_count = index_count * 2
    if pending["capture"]:
        new_total = (
            pending["digest_bytes"] + vertex_byte_count + index_byte_count
        )
        if new_total > capture.max_digest_bytes_per_entry:
            raise RuntimeError(
                "batch digest bytes exceed configured per-entry bound"
            )
        pending["digest_bytes"] = new_total

    vertex_digest = hashlib.sha256(b"").hexdigest()
    index_digest = hashlib.sha256(b"").hexdigest()
    if pending["capture"]:
        inferior = gdb.selected_inferior()
        vertex_address = (
            observed["vertex_pointer"] + start_vertex * family.vertex_stride
        )
        index_address = (
            pending["families"][family.id]["root"]
            + family.index_base_offset
            + page * family.index_page_stride
            + start_index * 2
        )
        try:
            vertex_bytes = bytes(
                inferior.read_memory(vertex_address, vertex_byte_count)
            ) if vertex_byte_count else b""
            index_bytes = bytes(
                inferior.read_memory(index_address, index_byte_count)
            ) if index_byte_count else b""
        except Exception as exc:
            raise RuntimeError(
                f"cannot read bounded {family.id} page {page} batch interval: "
                f"{type(exc).__name__}"
            ) from exc
        if len(vertex_bytes) != vertex_byte_count:
            raise RuntimeError("short read for bounded batch vertex interval")
        if len(index_bytes) != index_byte_count:
            raise RuntimeError("short read for bounded batch index interval")
        vertex_digest = hashlib.sha256(vertex_bytes).hexdigest()
        index_digest = hashlib.sha256(index_bytes).hexdigest()

    segment = {
        "event_index": state["segment_sequence"],
        "page_index": page,
        "flushed": flushed,
        "pre_vertex_count": start_vertex,
        "post_vertex_count": end_vertex,
        "vertex_count": vertex_count,
        "vertex_byte_count": vertex_byte_count,
        "vertex_sha256": vertex_digest,
        "pre_index_count": start_index,
        "post_index_count": end_index,
        "index_count": index_count,
        "index_byte_count": index_byte_count,
        "index_sha256": index_digest,
    }
    state["segment_sequence"] += 1
    if pending["capture"] and (flushed or vertex_count or index_count):
        pending["segments"][family.id].append(segment)
    return segment


def _finalize_direct3d_batch_entry(capture, pending):
    import hashlib
    import json

    family_results = []
    for family in capture.families:
        segments = pending["segments"][family.id]
        vertex_count = sum(segment["vertex_count"] for segment in segments)
        index_count = sum(segment["index_count"] for segment in segments)
        vertex_byte_count = sum(
            segment["vertex_byte_count"] for segment in segments
        )
        index_byte_count = sum(
            segment["index_byte_count"] for segment in segments
        )
        digest_input = json.dumps(
            segments, sort_keys=True, separators=(",", ":")
        ).encode("ascii")
        family_results.append({
            "family_id": family.id,
            "vertex_count": vertex_count,
            "index_count": index_count,
            "vertex_byte_count": vertex_byte_count,
            "index_byte_count": index_byte_count,
            "flush_count": sum(segment["flushed"] for segment in segments),
            "sha256": hashlib.sha256(digest_input).hexdigest(),
            "segments": segments,
        })
    digest_input = json.dumps(
        family_results, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return {
        "entry_index": pending["entry_index"],
        "vertex_count": sum(item["vertex_count"] for item in family_results),
        "index_count": sum(item["index_count"] for item in family_results),
        "byte_count": sum(
            item["vertex_byte_count"] + item["index_byte_count"]
            for item in family_results
        ),
        "sha256": hashlib.sha256(digest_input).hexdigest(),
        "families": family_results,
    }


def _finalize_direct3d_batch_cycle(capture, state):
    entries = state["current_entries"]
    expected = list(capture.candidate_indices)
    observed = [entry["entry_index"] for entry in entries]
    if observed != expected:
        raise RuntimeError(
            f"candidate sequence mismatch: expected {expected}, observed {observed}"
        )
    state["cycles"].append({
        "cycle_index": len(state["cycles"]),
        "entries": entries,
    })
    state["current_entries"] = []


def _start_direct3d_batch_rollover(capture, state):
    state["rollovers_seen"] += 1
    state["rollover_started"] = True
    if state["active"]:
        _finalize_direct3d_batch_cycle(capture, state)
        if len(state["cycles"]) >= capture.capture_cycles:
            return "capture_complete"
    elif state["rollovers_seen"] >= capture.warmup_rollovers:
        state["active"] = True
        state["current_entries"] = []
    return None


def _direct3d_record_form_for_pc(capture, observed_pc):
    return next(
        (item for item in capture.record_forms if item.stop_pc == observed_pc),
        None,
    )


def _direct3d_record_segment(pending, family, page, observed, flushed):
    start = pending["starts"][family.id][page]
    if observed["vertex_pointer"] != start["vertex_pointer"]:
        raise RuntimeError(
            f"{family.id} page {page} vertex pointer changed within record"
        )
    start_vertex = start["vertex_count"]
    start_index = start["index_count"]
    end_vertex = observed["vertex_count"]
    end_index = observed["index_count"]
    if end_vertex < start_vertex or end_index < start_index:
        raise RuntimeError(
            f"{family.id} page {page} counter decreased without captured flush"
        )
    segment = {
        "family_id": family.id,
        "page_index": page,
        "flushed": flushed,
        "vertex_count": end_vertex - start_vertex,
        "index_count": end_index - start_index,
    }
    if flushed or segment["vertex_count"] or segment["index_count"]:
        pending["segments"].append(segment)
    return segment


def _finalize_direct3d_record(gdb, capture, state):
    pending = state["pending"]
    if pending is None:
        return
    inferior = gdb.selected_inferior()
    for family in capture.families:
        observed_family = _read_batch_family_snapshot(inferior, capture, family)
        expected_family = pending["families"][family.id]
        if observed_family["root"] != expected_family["root"]:
            raise RuntimeError(f"{family.id} root changed within record")
        for page, observed in enumerate(observed_family["pages"]):
            _direct3d_record_segment(
                pending, family, page, observed, False
            )

    additions = {}
    flush_count = 0
    for segment in pending["segments"]:
        flush_count += int(segment["flushed"])
        key = (segment["family_id"], segment["page_index"])
        counts = additions.setdefault(key, [0, 0])
        counts[0] += segment["vertex_count"]
        counts[1] += segment["index_count"]
    positive = [
        (key, counts) for key, counts in additions.items()
        if counts[0] or counts[1]
    ]
    form = next(
        item for item in capture.record_forms
        if item.form == pending["form"]
    )
    appended = bool(positive)
    family_id = None
    page_index = None
    vertex_count = 0
    index_count = 0
    if appended:
        if len(positive) != 1:
            raise RuntimeError(
                "record changed batch counters in more than one family/page"
            )
        (family_id, page_index), counts = positive[0]
        vertex_count, index_count = counts
        if (
            vertex_count != form.append_vertex_count
            or index_count != form.append_index_count
        ):
            raise RuntimeError(
                f"record form 0x{form.form:x} produced unexpected count delta "
                f"({vertex_count},{index_count})"
            )
        if pending["candidate"] and (
            family_id != capture.allowed_outcome_family_id
            or page_index != capture.allowed_outcome_page
        ):
            raise RuntimeError(
                "candidate record append left the allowed family/page"
            )

    if pending["capture"]:
        if capture.capture_mode == "exact_0a6c_admission":
            if flush_count:
                raise RuntimeError("exact admission target call flushed")
            evaluation = pending.get("admission_evaluation")
            if evaluation is None:
                raise RuntimeError("exact admission evaluation is missing")
            inferior = gdb.selected_inferior()

            def post_read_u32(address):
                return _read_uint(
                    inferior, address, 4,
                    "exact admission post-call active state",
                )

            receipt = exact_admission.reconcile_receipt(
                evaluation, appended, post_read_u32
            )
            if not receipt["prediction_matches_observation"]:
                raise RuntimeError(
                    "exact admission prediction/count outcome mismatch"
                )
            state["current_records"].append(receipt)
        else:
            state["current_records"].append({
                "entry_index": pending["entry_index"],
                "file_offset": pending["file_offset"],
                "form": pending["form"],
                "appended": appended,
                "family_id": family_id,
                "page_index": page_index,
                "vertex_count": vertex_count,
                "index_count": index_count,
                "flush_count": flush_count,
            })
    state["pending"] = None


def _finish_direct3d_record_cycle(capture, state):
    if state["plan_cursor"] != len(capture.record_plan):
        raise RuntimeError(
            "record cycle ended before the exact record plan was consumed"
        )
    state["rollovers_seen"] += 1
    if state["active"]:
        observed_offsets = [
            item["file_offset"] for item in state["current_records"]
        ]
        expected_offsets = list(capture.candidate_record_offsets)
        if observed_offsets != expected_offsets:
            raise RuntimeError(
                "candidate record sequence mismatch: expected "
                f"{expected_offsets}, observed {observed_offsets}"
            )
        state["cycles"].append({
            "cycle_index": len(state["cycles"]),
            "records": state["current_records"],
        })
        if len(state["cycles"]) >= capture.capture_cycles:
            return "capture_complete"
    elif state["rollovers_seen"] >= capture.warmup_rollovers:
        state["active"] = True
    state["plan_cursor"] = 0
    state["cycle_base"] = None
    state["current_records"] = []
    state["last_post_index"] = None
    return None


def _process_direct3d_record_stop(gdb, hit, capture, state, observed_pc):
    _kind, trigger_id, _address, _size = hit
    try:
        if trigger_id == capture.pre_trigger_id:
            form = _direct3d_record_form_for_pc(capture, observed_pc)
            if form is None:
                return None
            index = _batch_pre_index(gdb, capture)
            if index is None:
                return None
            _finalize_direct3d_record(gdb, capture, state)

            expected_entry = (
                0 if state["last_post_index"] is None
                else state["last_post_index"] + 1
            )
            if index != expected_entry:
                raise RuntimeError(
                    f"record pre/post order mismatch: expected entry "
                    f"{expected_entry}, observed {index}"
                )
            cursor = state["plan_cursor"]
            if cursor >= len(capture.record_plan):
                raise RuntimeError("record pre exceeded the exact record plan")
            planned = capture.record_plan[cursor]
            if planned.entry_index != index or planned.form != form.form:
                raise RuntimeError(
                    "record plan mismatch at cursor "
                    f"{cursor}: expected entry/form "
                    f"{planned.entry_index}/0x{planned.form:x}, observed "
                    f"{index}/0x{form.form:x}"
                )
            pointer = _batch_register(
                gdb, capture.record_pointer_register, capture.pointer_size
            )
            if state["cycle_base"] is None:
                state["cycle_base"] = pointer - planned.file_offset
                if state["cycle_base"] < 0:
                    raise RuntimeError("record stream base underflow")
            observed_offset = pointer - state["cycle_base"]
            if observed_offset != planned.file_offset:
                raise RuntimeError(
                    f"record pointer mismatch: expected file offset "
                    f"0x{planned.file_offset:x}, observed 0x{observed_offset:x}"
                )

            inferior = gdb.selected_inferior()
            family_snapshots = {
                family.id: _read_batch_family_snapshot(
                    inferior, capture, family
                )
                for family in capture.families
            }
            candidate = planned.file_offset in capture.candidate_record_offsets
            admission_evaluation = None
            if (
                capture.capture_mode == "exact_0a6c_admission"
                and state["active"] and candidate
            ):
                admission_evaluation = _read_exact_0a6c_evaluation(
                    gdb, capture
                )
            state["pending"] = {
                "entry_index": index,
                "file_offset": planned.file_offset,
                "form": planned.form,
                "candidate": candidate,
                "capture": state["active"] and candidate,
                "families": family_snapshots,
                "starts": {
                    family.id: [
                        dict(page)
                        for page in family_snapshots[family.id]["pages"]
                    ]
                    for family in capture.families
                },
                "segments": [],
                "admission_evaluation": admission_evaluation,
            }
            state["plan_cursor"] += 1
            return None

        if trigger_id == capture.flush_trigger_id:
            family = next(
                (item for item in capture.families
                 if item.flush_stop_pc == observed_pc),
                None,
            )
            if family is None:
                return None
            pending = state["pending"]
            if pending is None:
                state["ignored_unmatched_flushes"] += 1
                return None
            page = _batch_register(
                gdb, capture.page_register, capture.pointer_size
            )
            if page >= capture.page_count:
                raise RuntimeError("record flush page is outside page_count")
            root, observed = _read_batch_page(
                gdb.selected_inferior(), capture, family, page
            )
            if root != pending["families"][family.id]["root"]:
                raise RuntimeError(f"{family.id} root changed within record")
            _direct3d_record_segment(
                pending, family, page, observed, True
            )
            pending["starts"][family.id][page] = {
                "vertex_pointer": observed["vertex_pointer"],
                "vertex_count": 0,
                "index_count": 0,
            }
            return None

        if trigger_id != capture.post_trigger_id:
            raise RuntimeError(
                f"unexpected record capture trigger {trigger_id!r}"
            )
        if observed_pc != capture.post_stop_pc:
            return None
        index = _batch_post_index(gdb, capture)
        expected_index = (
            0 if state["last_post_index"] is None
            else state["last_post_index"] + 1
        )
        if index != expected_index:
            raise RuntimeError(
                f"non-contiguous record post order: expected "
                f"{expected_index}, observed {index}"
            )
        if state["pending"] is not None:
            if state["pending"]["entry_index"] != index:
                raise RuntimeError(
                    "record pre/post entry mismatch "
                    f"{state['pending']['entry_index']}->{index}"
                )
            _finalize_direct3d_record(gdb, capture, state)
        cursor = state["plan_cursor"]
        if (
            cursor < len(capture.record_plan)
            and capture.record_plan[cursor].entry_index <= index
        ):
            raise RuntimeError(
                f"entry {index} post arrived before its record plan was consumed"
            )
        state["last_post_index"] = index
        if index == capture.entry_count - 1:
            return _finish_direct3d_record_cycle(capture, state)
        return None
    except Exception as exc:
        state["pending"] = None
        return _capture_fail_for_mode(capture, state, exc)


def _process_direct3d_batch_stop(gdb, hit, capture, state):
    _kind, trigger_id, _address, _size = hit
    try:
        observed_pc = int(gdb.newest_frame().pc())
    except Exception as exc:
        return _capture_fail(state, "cannot read batch capture stop PC")

    if capture.capture_mode in (
        "record_outcome", "exact_0a6c_admission",
    ):
        return _process_direct3d_record_stop(
            gdb, hit, capture, state, observed_pc
        )

    try:
        if trigger_id == capture.pre_trigger_id:
            if observed_pc not in capture.pre_stop_pcs:
                return None
            index = _batch_pre_index(gdb, capture)
            if index is None:
                return None
            if state["pending"] is not None:
                if state["pending"]["entry_index"] == index:
                    return None
                raise RuntimeError("batch pre trigger arrived before paired post")

            last_post_index = state["last_post_index"]
            if last_post_index is not None:
                expected_index = (last_post_index + 1) % capture.entry_count
                if index != expected_index:
                    raise RuntimeError(
                        f"batch pre/post order mismatch: expected "
                        f"{expected_index}, observed {index}"
                    )
            if (
                last_post_index == capture.entry_count - 1
                and index == 0
            ):
                rollover_end = _start_direct3d_batch_rollover(capture, state)
                if rollover_end is not None:
                    return rollover_end

            inferior = gdb.selected_inferior()
            family_snapshots = {
                family.id: _read_batch_family_snapshot(
                    inferior, capture, family
                )
                for family in capture.families
            }
            state["pending"] = {
                "entry_index": index,
                "capture": (
                    state["active"] and index in capture.candidate_indices
                ),
                "families": family_snapshots,
                "starts": {
                    family.id: [dict(page) for page in family_snapshots[family.id]["pages"]]
                    for family in capture.families
                },
                "segments": {family.id: [] for family in capture.families},
                "digest_bytes": 0,
            }
            state["last_pre_index"] = index
            return None

        if trigger_id == capture.flush_trigger_id:
            family = next(
                (item for item in capture.families
                 if item.flush_stop_pc == observed_pc),
                None,
            )
            if family is None:
                return None
            pending = state["pending"]
            if pending is None:
                state["ignored_unmatched_flushes"] += 1
                return None
            page = _batch_register(gdb, capture.page_register,
                                   capture.pointer_size)
            if page >= capture.page_count:
                raise RuntimeError("batch flush page is outside page_count")
            inferior = gdb.selected_inferior()
            root, observed = _read_batch_page(
                inferior, capture, family, page
            )
            expected_family = pending["families"][family.id]
            if root != expected_family["root"]:
                raise RuntimeError(f"{family.id} root changed within entry")
            _batch_segment(
                gdb, capture, state, pending, family, page, observed, True
            )
            pending["starts"][family.id][page] = {
                "vertex_pointer": observed["vertex_pointer"],
                "vertex_count": 0,
                "index_count": 0,
            }
            return None

        if trigger_id != capture.post_trigger_id:
            raise RuntimeError(f"unexpected batch capture trigger {trigger_id!r}")
        if observed_pc != capture.post_stop_pc:
            return None
        index = _batch_post_index(gdb, capture)
        last_post_index = state["last_post_index"]
        if last_post_index is not None:
            expected_index = (last_post_index + 1) % capture.entry_count
            if index != expected_index:
                raise RuntimeError(
                    f"non-contiguous post order: expected {expected_index}, "
                    f"observed {index}"
                )
        if last_post_index == capture.entry_count - 1 and index == 0:
            if state["rollover_started"]:
                state["rollover_started"] = False
            else:
                rollover_end = _start_direct3d_batch_rollover(capture, state)
                state["rollover_started"] = False
                if rollover_end is not None:
                    return rollover_end

        pending = state["pending"]
        if pending is None:
            if state["active"] and index in capture.candidate_indices:
                empty_pending = {
                    "entry_index": index,
                    "segments": {
                        family.id: [] for family in capture.families
                    },
                }
                state["current_entries"].append(
                    _finalize_direct3d_batch_entry(capture, empty_pending)
                )
            state["last_post_index"] = index
            return None
        if pending["entry_index"] != index:
            raise RuntimeError(
                f"batch pre/post entry mismatch {pending['entry_index']}->{index}"
            )

        pending["capture"] = (
            state["active"] and index in capture.candidate_indices
        )
        inferior = gdb.selected_inferior()
        for family in capture.families:
            observed_family = _read_batch_family_snapshot(
                inferior, capture, family
            )
            expected_family = pending["families"][family.id]
            if observed_family["root"] != expected_family["root"]:
                raise RuntimeError(f"{family.id} root changed within entry")
            for page, observed in enumerate(observed_family["pages"]):
                _batch_segment(
                    gdb, capture, state, pending, family, page,
                    observed, False,
                )
        if pending["capture"]:
            state["current_entries"].append(
                _finalize_direct3d_batch_entry(capture, pending)
            )
        state["pending"] = None
        state["last_post_index"] = index
        return None
    except Exception as exc:
        state["pending"] = None
        return _capture_fail(state, str(exc))


def _direct3d_batch_capture_result(capture, state, completed):
    if capture.capture_mode == "exact_0a6c_admission":
        return {
            "schema_version": 3,
            "completed": completed,
            "capture_mode": capture.capture_mode,
            "algorithm": "native-first-reject/count-delta/sha256",
            "raw_inputs_retained": False,
            "payload_bytes_retained": 0,
            "candidate_indices": list(capture.candidate_indices),
            "candidate_record_offsets": list(
                capture.candidate_record_offsets
            ),
            "record_plan_count": len(capture.record_plan),
            "record_plan_sha256": exact_admission.EXACT_RECORD_PLAN_SHA256,
            "family_ids": [family.id for family in capture.families],
            "allowed_outcome_family_id": (
                capture.allowed_outcome_family_id
            ),
            "allowed_outcome_page": capture.allowed_outcome_page,
            "warmup_rollovers_required": capture.warmup_rollovers,
            "rollovers_observed": state["rollovers_seen"],
            "capture_cycles_requested": capture.capture_cycles,
            "ignored_unmatched_flushes": state["ignored_unmatched_flushes"],
            "cycles": state["cycles"],
            "failure": state["failure"],
        }
    if capture.capture_mode == "record_outcome":
        return {
            "schema_version": 2,
            "completed": completed,
            "capture_mode": capture.capture_mode,
            "algorithm": "count-delta",
            "payload_bytes_retained": False,
            "candidate_indices": list(capture.candidate_indices),
            "candidate_record_offsets": list(
                capture.candidate_record_offsets
            ),
            "record_plan_count": len(capture.record_plan),
            "family_ids": [family.id for family in capture.families],
            "allowed_outcome_family_id": (
                capture.allowed_outcome_family_id
            ),
            "allowed_outcome_page": capture.allowed_outcome_page,
            "warmup_rollovers_required": capture.warmup_rollovers,
            "rollovers_observed": state["rollovers_seen"],
            "capture_cycles_requested": capture.capture_cycles,
            "ignored_unmatched_flushes": state["ignored_unmatched_flushes"],
            "cycles": state["cycles"],
            "failure": state["failure"],
        }
    return {
        "schema_version": 1,
        "completed": completed,
        "capture_mode": capture.capture_mode,
        "algorithm": "sha256",
        "payload_bytes_retained": False,
        "candidate_indices": list(capture.candidate_indices),
        "family_ids": [family.id for family in capture.families],
        "warmup_rollovers_required": capture.warmup_rollovers,
        "rollovers_observed": state["rollovers_seen"],
        "capture_cycles_requested": capture.capture_cycles,
        "ignored_unmatched_flushes": state["ignored_unmatched_flushes"],
        "cycles": state["cycles"],
        "failure": state["failure"],
    }


def _write_evidence_draft(path, spec, result, stop_records) -> None:
    completion = result["completion"]
    lines = [
        f"# {os.path.basename(os.path.dirname(path))}",
        "",
        f"Experiment: {spec.experiment_id}",
        f"Tool: {TOOL} {TOOL_VERSION} (read-only hardware watch/breakpoints)",
        f"Window start: {result['time_window_start']}",
        f"Window end:   {result['time_window_end']}",
        "",
        "This is an auto-generated draft of read-only debugger stops. No game "
        "memory, register, executable byte, or game file was changed. Read "
        "watchpoints are read-class hardware traps on x86 and may report during "
        "writes; treat them as access evidence, not proof of a read.",
        "",
        f"Completion: {completion['stop_reason']} "
        f"(completed={completion['completed']}, "
        f"accepted={completion.get('accepted', completion['completed'])}, "
        f"stops={completion['stops_observed']}, "
        f"cleanup_verified={completion['cleanup_verified']}, "
        f"detached={completion['detached']})",
        "",
        "Stops",
        "-----",
    ]
    if not stop_records:
        lines.append("(no stops observed in the bounded window)")
    for record in stop_records:
        lines.append(
            f"seq {record['seq']}: {record['kind']} {record['trigger_id']} "
            f"at PC {record['pc']} watched={record['watched_value_hex']}"
        )
    target_signal = completion.get("target_signal")
    if target_signal:
        lines += [
            "",
            "Target signal",
            "-------------",
            f"{target_signal.get('name')} at PC {target_signal.get('pc')} "
            f"({target_signal.get('classification')}, "
            f"{target_signal.get('delivery_policy')})",
        ]
    capture = result.get("submission_capture")
    if capture:
        lines += [
            "",
            "Submission capture",
            "------------------",
            f"completed={capture.get('completed')} "
            f"cycles={len(capture.get('cycles') or [])} "
            f"algorithm={capture.get('algorithm')} "
            f"payload_bytes_retained={capture.get('payload_bytes_retained')} "
            f"failure={capture.get('failure')}",
        ]
    batch_capture = result.get("direct3d_batch_capture")
    if batch_capture:
        lines += [
            "",
            "Direct3D batch capture",
            "----------------------",
            f"completed={batch_capture.get('completed')} "
            f"cycles={len(batch_capture.get('cycles') or [])} "
            f"algorithm={batch_capture.get('algorithm')} "
            f"payload_bytes_retained="
            f"{batch_capture.get('payload_bytes_retained')} "
            f"failure={batch_capture.get('failure')}",
        ]
    survival = completion.get("survival_receipt")
    if survival:
        lines += [
            "",
            "Post-detach survival",
            "--------------------",
            f"passed={survival.get('passed')} "
            f"identity_verified={survival.get('identity_verified')} "
            f"samples={len(survival.get('samples') or [])} "
            f"failure_reasons={survival.get('failure_reasons') or []}",
        ]
    lines += [
        "",
        "Interpretation is intentionally left for a linked experiment note.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


# ==========================================================================
# CLI mode (runs under the repo venv)
# ==========================================================================


def _environment_string() -> str:
    parts = []
    try:
        with open("/etc/os-release", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("PRETTY_NAME="):
                    parts.append(line.split("=", 1)[1].strip().strip('"'))
                    break
    except OSError:
        pass
    try:
        parts.append(f"kernel {os.uname().release}")
    except Exception:  # pragma: no cover
        pass
    wine = _first_line(["wine", "--version"])
    if wine:
        parts.append(wine)
    return ", ".join(parts) if parts else "unknown"


def _first_line(argv):
    import subprocess
    try:
        out = subprocess.run(argv, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    text = (out.stdout or out.stderr or "").strip().splitlines()
    return text[0] if text else None


def _read_proc_survival_state(pid: int) -> dict:
    state = None
    tracer_pid = None
    with open(f"/proc/{pid}/status", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("State:"):
                fields = line.split()
                state = fields[1] if len(fields) > 1 else None
            elif line.startswith("TracerPid:"):
                fields = line.split()
                tracer_pid = int(fields[1]) if len(fields) > 1 else None
    if state is None or tracer_pid is None:
        raise OSError("State or TracerPid missing from /proc status")
    return {"state": state, "tracer_pid": tracer_pid}


def _collect_survival_receipt(pid: int, target: dict, config: dict) -> dict:
    import time

    started = ev.now().isoformat()
    if config["settle_ms"]:
        time.sleep(config["settle_ms"] / 1000.0)

    failure_reasons = []
    identity_verified = False
    identity = None
    try:
        proof = ev.ownership_proof(
            pid,
            expected_sha256=target.get("expected_exe_sha256"),
            exe_basename=target.get("exe_basename", ev.DEFAULT_EXE_BASENAME),
            loader_re=target.get("expected_loader_re", ev.DEFAULT_LOADER_RE),
            cwd_prefix=target.get("expected_cwd_prefix"),
        )
        identity_verified = True
        identity = proof.to_dict()
    except ev.OwnershipError as exc:
        failure_reasons.append(f"identity:{exc.reason}")

    samples = []
    for index in range(config["sample_count"]):
        if index and config["sample_interval_ms"]:
            time.sleep(config["sample_interval_ms"] / 1000.0)
        sample = {
            "index": index,
            "t_wall": ev.now().isoformat(),
            "state": None,
            "tracer_pid": None,
            "passed": False,
        }
        sample_reasons = []
        try:
            proc_state = _read_proc_survival_state(pid)
            sample.update(proc_state)
            if (
                config["require_resumed"]
                and proc_state["state"] not in SAFE_RESUMED_STATES
            ):
                sample_reasons.append(f"state:{proc_state['state']}")
            if config["require_untraced"] and proc_state["tracer_pid"] != 0:
                sample_reasons.append(f"tracer_pid:{proc_state['tracer_pid']}")
        except (OSError, ValueError) as exc:
            sample_reasons.append(f"proc_status:{type(exc).__name__}")
        sample["failure_reasons"] = sample_reasons
        sample["passed"] = not sample_reasons
        samples.append(sample)
        failure_reasons.extend(
            f"sample[{index}]:{reason}" for reason in sample_reasons
        )

    passed = identity_verified and all(sample["passed"] for sample in samples)
    return {
        "schema_version": 1,
        "probe": "proc-identity-state-tracer",
        "pid": pid,
        "time_start": started,
        "time_end": ev.now().isoformat(),
        "configuration": dict(config),
        "identity_verified": identity_verified,
        "identity": identity,
        "samples": samples,
        "passed": passed,
        "failure_reasons": failure_reasons,
    }


def _apply_survival_receipt(result: dict, receipt: dict, required: bool) -> dict:
    completion = result.setdefault("completion", {})
    primary_reason = completion.get("stop_reason", "error")
    primary_completed = bool(completion.get("completed"))
    completion["survival_required"] = required
    completion["survival_verified"] = bool(receipt.get("passed"))
    completion["survival_receipt"] = receipt
    completion["accepted"] = primary_completed and (
        not required or bool(receipt.get("passed"))
    )
    if required and primary_completed and not receipt.get("passed"):
        completion["primary_stop_reason"] = primary_reason
        completion["stop_reason"] = "survival_failed"
        completion["completed"] = False
    return result


def _read_jsonl(path: str) -> list[dict]:
    import json

    records = []
    try:
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    records.append(json.loads(line))
    except (OSError, ValueError):
        return []
    return records


def _refuse(reason: str, detail: str = "", **extra) -> int:
    import json
    payload = {"refused": True, "tool": TOOL, "reason": reason}
    if detail:
        payload["detail"] = detail
    payload.update(extra)
    print(json.dumps(payload))
    return ev.EXIT_REFUSAL


def run_cli(argv=None) -> int:
    import argparse
    import json
    import subprocess

    parser = argparse.ArgumentParser(description="Read-only GDB watch harness")
    parser.add_argument("--capabilities", action="store_true",
                        help="print machine-readable capabilities and exit")
    parser.add_argument("--spec", help="path to a watch-spec JSON file")
    parser.add_argument("--gdb-bin", default=os.environ.get("GDB_BIN", "gdb"))
    parser.add_argument("--spawn-settle-ms", type=int, default=200)
    args = parser.parse_args(argv)

    if args.capabilities:
        print(json.dumps(capabilities(), indent=2))
        return ev.EXIT_OK
    if not args.spec:
        parser.error("--spec is required unless --capabilities is given")

    with open(args.spec, encoding="utf-8") as handle:
        raw_spec = json.load(handle)
    try:
        spec = ev.validate_watch_spec(raw_spec)
    except ev.SpecError as exc:
        print(json.dumps({"error": "spec", "detail": str(exc)}))
        return ev.EXIT_USAGE

    target = spec.target or {}
    mode = target.get("mode", "pid")
    spawned = None
    try:
        if mode == "pid":
            pid = int(target["pid"])
        elif mode == "name":
            pid = ev.find_pid_by_name(target.get("exe_basename", ev.DEFAULT_EXE_BASENAME))
        elif mode == "spawn":
            spawn_argv = target.get("spawn_argv")
            if not spawn_argv:
                return _refuse("spawn_argv_missing")
            spawn_cwd = target.get("spawn_cwd") or os.path.dirname(spawn_argv[0])
            spawned = subprocess.Popen(spawn_argv, cwd=spawn_cwd or None)
            pid = spawned.pid
            import time
            time.sleep(max(0, args.spawn_settle_ms) / 1000.0)
        else:
            return _refuse("bad_target_mode", f"unknown mode {mode!r}")
    except (KeyError, ValueError, ev.OwnershipError) as exc:
        return _refuse("target_resolution", str(exc))

    try:
        proof = ev.ownership_proof(
            pid,
            expected_sha256=target.get("expected_exe_sha256"),
            exe_basename=target.get("exe_basename", ev.DEFAULT_EXE_BASENAME),
            loader_re=target.get("expected_loader_re", ev.DEFAULT_LOADER_RE),
            cwd_prefix=target.get("expected_cwd_prefix"),
        )
    except ev.OwnershipError as exc:
        if spawned is not None:
            spawned.terminate()
        return _refuse("ownership", exc.detail, ownership_reason=exc.reason)

    run_dir = ev.new_run_dir("GDB")
    resolved_spec_path = os.path.join(run_dir, "spec.resolved.json")
    with open(resolved_spec_path, "w", encoding="utf-8") as handle:
        json.dump(raw_spec, handle, indent=2)

    metadata = {
        "run_id": os.path.basename(run_dir),
        "experiment_id": spec.experiment_id,
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "schema_version": SCHEMA_VERSION,
        "executable_sha256": proof.exe_sha256,
        "environment": _environment_string(),
        "debugger": _first_line([args.gdb_bin, "--version"]) or "unknown",
        "working_directory": proof.cwd,
        "target_pid": pid,
        "ownership": proof.to_dict(),
        "status": "running",
        "spec": raw_spec,
    }
    metadata_path = os.path.join(run_dir, "metadata.json")
    _write_json(metadata_path, metadata)

    log_path = spec.window.get("log_path")
    if log_path and os.path.isfile(log_path):
        metadata["log_start_offset"] = os.path.getsize(log_path)

    gdb_stderr_path = os.path.join(run_dir, "gdb-stderr.txt")
    gdb_stdout_path = os.path.join(run_dir, "gdb-stdout.txt")
    env = dict(os.environ)
    env.update({
        "ABLPC_GDB_RUNDIR": run_dir,
        "ABLPC_GDB_TARGET_PID": str(pid),
        "ABLPC_GDB_SPEC": resolved_spec_path,
        "ABLPC_SCRIPTS_DIR": _SCRIPTS_DIR,
    })
    gdb_cmd = [
        args.gdb_bin, "-nx", "-q", "-batch",
        "-iex", "set auto-load off",
        "-ex", "set confirm off",
        "-ex", "set pagination off",
        "-ex", "set height 0",
        "-ex", "set width 0",
        "-x", os.path.abspath(__file__),
    ]
    backstop = spec.window.get("timeout_seconds", ev.MAX_TIMEOUT_SECONDS) + 30

    status = "complete"
    with open(gdb_stdout_path, "w") as out, open(gdb_stderr_path, "w") as err:
        proc = subprocess.Popen(gdb_cmd, env=env, stdout=out, stderr=err)
        try:
            proc.wait(timeout=backstop)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
            status = "aborted-hard-timeout"

    result_path = os.path.join(run_dir, "result.json")
    result = _read_json(result_path)
    if result is not None:
        completion = result.get("completion") or {}
        if spec.survival:
            receipt = _collect_survival_receipt(pid, target, spec.survival)
            result = _apply_survival_receipt(
                result, receipt, bool(spec.survival["required"])
            )
        else:
            completion.setdefault("accepted", bool(completion.get("completed")))
            completion.setdefault("survival_required", False)
        _write_json(result_path, result)
        _write_evidence_draft(
            os.path.join(run_dir, "debugger-evidence.txt"),
            spec,
            result,
            _read_jsonl(os.path.join(run_dir, "stops.jsonl")),
        )

    metadata["gdb_arch_warning"] = _grep_arch_warning(gdb_stderr_path)
    metadata["artifacts"] = _existing_artifacts(run_dir)
    if result is not None:
        metadata["time_window_start"] = result.get("time_window_start")
        metadata["time_window_end"] = result.get("time_window_end")
        metadata["log_start_offset"] = result.get("log_start_offset",
                                                   metadata.get("log_start_offset"))
        metadata["completion"] = result.get("completion")
        completion = result.get("completion") or {}
        if status != "aborted-hard-timeout":
            status = completion.get("stop_reason", "error")
    else:
        metadata["completion"] = {
            "completed": False,
            "accepted": False,
            "stop_reason": "error",
            "error": "controller wrote no result.json",
        }
        if status != "aborted-hard-timeout":
            status = "error"

    if spawned is not None:
        spawned.terminate()
        try:
            spawned.wait(timeout=5)
        except subprocess.TimeoutExpired:  # pragma: no cover
            spawned.kill()

    metadata["status"] = status
    _write_json(metadata_path, metadata)

    completion = metadata.get("completion") or {}
    print(f"{metadata['run_id']}: {status} "
          f"(stops={completion.get('stops_observed', 0)}, "
          f"cleanup_verified={completion.get('cleanup_verified')})")
    if status == "aborted-hard-timeout" or not completion.get(
        "accepted", completion.get("completed")
    ):
        return ev.EXIT_TOOL_NEGATIVE
    return ev.EXIT_OK


def _write_json(path, obj) -> None:
    import json
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(obj, handle, indent=2)


def _read_json(path):
    import json
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def _existing_artifacts(run_dir):
    names = ["metadata.json", "spec.resolved.json", "stops.jsonl",
             "result.json", "debugger-evidence.txt", "gdb-stderr.txt"]
    return [n for n in names if os.path.isfile(os.path.join(run_dir, n))]


def _grep_arch_warning(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                low = line.lower()
                if "architecture" in low or "i386:x" in low:
                    return line.strip()
    except OSError:
        return None
    return None


# ==========================================================================
# Entry point dispatch
# ==========================================================================

try:
    import gdb as _gdb_module  # noqa: F401
    _HAVE_GDB = True
except ImportError:
    _HAVE_GDB = False


if _HAVE_GDB and os.environ.get("ABLPC_GDB_RUNDIR"):
    run_controller()
elif __name__ == "__main__":
    sys.exit(run_cli())
