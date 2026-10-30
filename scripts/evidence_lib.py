"""Shared foundation for ABLPC runtime-evidence capture tooling.

Stdlib only. This module is imported by the Python capture tools and invoked as
a CLI helper by the bash wrappers (`evidence_lib.py <subcommand> --json`) so a
single implementation of run-directory stamping, process ownership proof, watch
specification validation, and ELF core iteration is shared across every tool.

Nothing here signals, ptraces, or writes to a traced process. The ownership
helpers are pure ``/proc`` reads used to refuse acting on an unexpected process
before any privileged tool (gdb, gcore) is launched by a caller.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import sys
from typing import Iterator

import exact_0a6c_admission as exact_admission


DEFAULT_LOADER_RE = r"^/usr/(bin|lib64)/.*wine.*$"
DEFAULT_EXE_BASENAME = "bugs.exe"
RUN_ROOT = "dynamic/wine"

# Exit codes shared by every capture tool.
EXIT_OK = 0
EXIT_TOOL_NEGATIVE = 1
EXIT_USAGE = 2
EXIT_REFUSAL = 3


class OwnershipError(Exception):
    """Raised when a target process fails its expected-identity proof."""

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(detail or reason)
        self.reason = reason
        self.detail = detail


class SpecError(ValueError):
    """Raised when a watch specification violates the bounded schema."""


class ElfCoreError(ValueError):
    """Raised when bytes cannot satisfy the bounded ELF core layout."""


def repo_root() -> Path:
    """Return the repository root, honoring the ``ABLPC_ROOT`` override.

    The override lets bash wrappers and tests sandbox generated run
    directories into a temporary tree instead of the real ``dynamic/wine``.
    """

    override = os.environ.get("ABLPC_ROOT")
    if override:
        return Path(override).resolve()
    return Path(__file__).resolve().parents[1]


def now() -> datetime:
    return datetime.now().astimezone()


def run_stamp(moment: datetime | None = None) -> str:
    return (moment or now()).strftime("%Y%m%d-%H%M%S")


def new_run_dir(prefix: str, *, root: Path | None = None,
                moment: datetime | None = None) -> Path:
    """Create and return ``dynamic/wine/RUN-<PREFIX>-<stamp>``.

    Refuses to reuse an existing directory, matching ``wine-capture.sh``.
    """

    base = (root or repo_root()) / RUN_ROOT
    run_id = f"RUN-{prefix}-{run_stamp(moment)}"
    run_dir = base / run_id
    if run_dir.exists():
        raise FileExistsError(f"Run already exists: {run_dir}")
    run_dir.mkdir(parents=True)
    return run_dir


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_hex_u64(text: str) -> int:
    """Parse a hex string (``0x``-prefixed or bare) into an unsigned 64-bit int."""

    value = text.strip()
    if not value:
        raise ValueError("empty hex value")
    try:
        parsed = int(value, 16)
    except ValueError as exc:
        raise ValueError(f"not a hex value: {text!r}") from exc
    if parsed < 0 or parsed >= 2 ** 64:
        raise ValueError(f"hex value out of unsigned 64-bit range: {text!r}")
    return parsed


# --------------------------------------------------------------------------
# Ownership proof
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class OwnershipProof:
    pid: int
    loader_exe: str
    cmdline: tuple[str, ...]
    cwd: str
    exe_path: str
    exe_sha256: str
    verified: bool
    checked_at: str

    def to_dict(self) -> dict:
        return {
            "pid": self.pid,
            "loader_exe": self.loader_exe,
            "cmdline": list(self.cmdline),
            "cwd": self.cwd,
            "exe_path": self.exe_path,
            "exe_sha256": self.exe_sha256,
            "verified": self.verified,
            "checked_at": self.checked_at,
        }


def _read_proc_cmdline(pid: int) -> tuple[str, ...]:
    raw = Path(f"/proc/{pid}/cmdline").read_bytes()
    parts = [part for part in raw.split(b"\x00") if part]
    return tuple(part.decode("utf-8", "replace") for part in parts)


def _win_unix_basename(token: str) -> str:
    """Basename of a token that may use Windows (\\) or Unix (/) separators.

    The Wine game's command line carries a Windows path such as
    ``R:\\PC\\BUGS\\bugs.exe``, which ``os.path.basename`` does not split on a
    Linux host, so both separators are normalized here.
    """

    return token.replace("\\", "/").rsplit("/", 1)[-1]


def ownership_proof(
    pid: int,
    *,
    expected_sha256: str | None = None,
    exe_basename: str = DEFAULT_EXE_BASENAME,
    loader_re: str = DEFAULT_LOADER_RE,
    cwd_prefix: str | None = None,
    root: Path | None = None,
) -> OwnershipProof:
    """Prove ``pid`` is the expected Wine-hosted game before acting on it.

    Verifies, using only ``/proc`` reads, that: the loader behind ``exe`` looks
    like a Wine loader; the command line references ``exe_basename``; the
    working directory sits under ``work/copies/`` (the derived-tree root); and
    the on-disk game executable there matches ``expected_sha256``. Raises
    :class:`OwnershipError` on the first failing check. Never signals the
    process.
    """

    proc = Path(f"/proc/{pid}")
    if not proc.exists():
        raise OwnershipError("no_such_pid", f"/proc/{pid} does not exist")

    try:
        loader_exe = os.readlink(proc / "exe")
    except OSError as exc:
        raise OwnershipError("exe_unreadable", str(exc)) from exc
    if not re.search(loader_re, loader_exe):
        raise OwnershipError(
            "loader_mismatch",
            f"{loader_exe!r} does not match {loader_re!r}",
        )

    try:
        cmdline = _read_proc_cmdline(pid)
    except OSError as exc:
        raise OwnershipError("cmdline_unreadable", str(exc)) from exc
    want = exe_basename.lower()
    if not any(_win_unix_basename(token).lower() == want for token in cmdline):
        raise OwnershipError(
            "cmdline_missing_exe",
            f"no cmdline token basename == {exe_basename!r}",
        )

    try:
        cwd = os.readlink(proc / "cwd")
    except OSError as exc:
        raise OwnershipError("cwd_unreadable", str(exc)) from exc
    prefix = cwd_prefix or str((root or repo_root()) / "work" / "copies") + os.sep
    if not cwd.rstrip(os.sep).startswith(prefix.rstrip(os.sep)):
        raise OwnershipError(
            "cwd_outside_copies",
            f"{cwd!r} is not under {prefix!r}",
        )

    exe_path = os.path.join(cwd, exe_basename)
    if not os.path.isfile(exe_path):
        raise OwnershipError("exe_not_found", f"{exe_path!r} is not a file")
    exe_sha = sha256_file(exe_path)
    if expected_sha256 is not None and exe_sha.lower() != expected_sha256.lower():
        raise OwnershipError(
            "sha_mismatch",
            f"{exe_path} sha256 {exe_sha} != expected {expected_sha256}",
        )

    return OwnershipProof(
        pid=pid,
        loader_exe=loader_exe,
        cmdline=cmdline,
        cwd=cwd,
        exe_path=exe_path,
        exe_sha256=exe_sha,
        verified=True,
        checked_at=now().isoformat(),
    )


def find_pid_by_name(exe_basename: str = DEFAULT_EXE_BASENAME) -> int:
    """Return the single PID whose cmdline references ``exe_basename``.

    Zero or more than one match is an error: the caller must disambiguate.
    """

    want = exe_basename.lower()
    matches: list[int] = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            cmdline = _read_proc_cmdline(int(entry.name))
        except OSError:
            continue
        if any(_win_unix_basename(token).lower() == want for token in cmdline):
            matches.append(int(entry.name))
    if not matches:
        raise OwnershipError("pid_not_found", f"no process references {exe_basename!r}")
    if len(matches) > 1:
        raise OwnershipError(
            "pid_ambiguous",
            f"multiple processes reference {exe_basename!r}: {sorted(matches)}",
        )
    return matches[0]


# --------------------------------------------------------------------------
# Watch specification validation
# --------------------------------------------------------------------------


HW_SLOTS = 4
WATCH_SIZES = (1, 2, 4)
WATCH_KINDS = ("read", "write", "access")
MAX_STOPS = 1000
MAX_TIMEOUT_SECONDS = 3600
MAX_MEMORY_READ_BYTES = 256
MAX_MEMORY_READS = 16
MAX_BACKTRACE = 32
MAX_SUBMISSION_DIGEST_BYTES = 1 << 20
MAX_SUBMISSION_CAPACITY_RECORDS = 1 << 20
MAX_BATCH_DIGEST_BYTES = 1 << 24
MAX_BATCH_PAGES = 64
SPEC_SCHEMA_VERSION = 6
SUPPORTED_SPEC_SCHEMA_VERSIONS = (1, 2, 3, 4, 5, 6)
MAX_SURVIVAL_WINDOW_MS = 30_000


@dataclass(frozen=True)
class Watchpoint:
    id: str
    address: int
    kind: str
    size: int


@dataclass(frozen=True)
class Breakpoint:
    id: str
    address: int


@dataclass(frozen=True)
class MemoryRead:
    id: str
    address: int
    size: int


@dataclass(frozen=True)
class SubmissionCapture:
    interval_mode: str
    pre_trigger_id: str
    post_trigger_id: str
    pre_stop_pc: int | None
    post_stop_pc: int | None
    entry_register: str
    entry_root: int
    entry_stride: int
    entry_count: int
    candidate_indices: tuple[int, ...]
    counter_address: int
    capacity_address: int
    base_pointer_address: int
    pointer_size: int
    output_stride: int
    max_records_per_entry: int
    warmup_rollovers: int
    capture_cycles: int


@dataclass(frozen=True)
class Direct3DBatchFamily:
    id: str
    flush_stop_pc: int
    root_pointer_address: int
    allowed_roots: tuple[int, ...]
    vertex_pointer_table_offset: int
    vertex_count_offset: int
    index_base_offset: int
    index_count_offset: int
    index_page_stride: int
    vertex_stride: int
    max_vertex_count: int
    max_index_count: int


@dataclass(frozen=True)
class Direct3DRecordForm:
    form: int
    stop_pc: int
    append_vertex_count: int
    append_index_count: int


@dataclass(frozen=True)
class Direct3DRecordPlanItem:
    entry_index: int
    file_offset: int
    form: int


@dataclass(frozen=True)
class Direct3DBatchCapture:
    pre_trigger_id: str
    flush_trigger_id: str
    post_trigger_id: str
    pre_stop_pcs: tuple[int, ...]
    post_stop_pc: int
    call_return_address: int
    stack_pointer_register: str
    entry_return_stack_offset: int
    entry_pointer_stack_offset: int
    entry_index_stack_offset: int
    post_entry_register: str
    page_register: str
    entry_root: int
    entry_stride: int
    entry_count: int
    candidate_indices: tuple[int, ...]
    pointer_size: int
    page_count: int
    families: tuple[Direct3DBatchFamily, ...]
    max_digest_bytes_per_entry: int
    warmup_rollovers: int
    capture_cycles: int
    capture_mode: str = "entry_digest"
    record_pointer_register: str | None = None
    record_forms: tuple[Direct3DRecordForm, ...] = ()
    record_plan: tuple[Direct3DRecordPlanItem, ...] = ()
    candidate_record_offsets: tuple[int, ...] = ()
    allowed_outcome_family_id: str | None = None
    allowed_outcome_page: int | None = None


@dataclass(frozen=True)
class WatchSpec:
    schema_version: int
    experiment_id: str
    target: dict
    watchpoints: tuple[Watchpoint, ...]
    breakpoints: tuple[Breakpoint, ...]
    window: dict
    on_stop: dict
    survival: dict
    registers: tuple[str, ...] = field(default_factory=tuple)
    memory_reads: tuple[MemoryRead, ...] = field(default_factory=tuple)
    backtrace_limit: int = 8
    submission_capture: SubmissionCapture | None = None
    direct3d_batch_capture: Direct3DBatchCapture | None = None


def _require_keys(obj: dict, allowed: set[str], where: str) -> None:
    if not isinstance(obj, dict):
        raise SpecError(f"{where} must be an object")
    unknown = set(obj) - allowed
    if unknown:
        raise SpecError(f"{where} has unknown keys: {sorted(unknown)}")


def _addr(value, where: str) -> int:
    if isinstance(value, int):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = parse_hex_u64(value)
        except ValueError as exc:
            raise SpecError(f"{where}: {exc}") from exc
    else:
        raise SpecError(f"{where} must be an int or hex string")
    if parsed < 0 or parsed >= 2 ** 63:
        raise SpecError(f"{where} out of range: {value!r}")
    return parsed


def _validate_exact_0a6c_capture(
    capture: Direct3DBatchCapture,
    *,
    raw_target: dict,
    watchpoints: tuple[Watchpoint, ...],
    breakpoints: tuple[Breakpoint, ...],
    registers: tuple[str, ...],
    memory_reads: tuple[MemoryRead, ...],
    backtrace_limit: int,
    window: dict,
    survival: dict,
) -> None:
    """Fail closed unless schema 6 is an audited exact-0A6C envelope."""

    if not isinstance(raw_target, dict) or (
        raw_target.get("expected_exe_sha256")
        != exact_admission.EXACT_EXE_SHA256
    ):
        raise SpecError(
            "exact_0a6c_admission requires the hash-locked executable"
        )
    cwd_prefix = raw_target.get("expected_cwd_prefix")
    copies_prefix = str((repo_root() / "work/copies").resolve()) + os.sep
    if (
        raw_target.get("mode") != "pid"
        or not isinstance(raw_target.get("pid"), int)
        or isinstance(raw_target.get("pid"), bool)
        or raw_target["pid"] <= 0
        or raw_target.get("exe_basename") != "bugs.exe"
        or raw_target.get("expected_loader_re") != ".*wine-preloader$"
        or not isinstance(cwd_prefix, str)
        or not cwd_prefix.startswith(copies_prefix)
        or not cwd_prefix.rstrip("/").endswith("/PC/BUGS")
    ):
        raise SpecError(
            "exact_0a6c_admission requires the audited paused-target identity"
        )
    if breakpoints or len(watchpoints) != 3:
        raise SpecError(
            "exact_0a6c_admission requires exactly the three existing data watches"
        )
    watch_by_id = {item.id: item for item in watchpoints}
    exact_watches = (
        (capture.pre_trigger_id, 0x0059F7F0, 2),
        (capture.flush_trigger_id, 0x004C4118, 2),
        (capture.post_trigger_id, 0x005B18E0, 4),
    )
    if any(
        watch_by_id.get(trigger_id) != Watchpoint(
            trigger_id, address, "access", size
        )
        for trigger_id, address, size in exact_watches
    ):
        raise SpecError(
            "exact_0a6c_admission data watches differ from the audited boundaries"
        )
    if registers or memory_reads or backtrace_limit > 2:
        raise SpecError(
            "exact_0a6c_admission forbids raw register/memory output and deep backtraces"
        )
    expected_survival = {
        "required": True,
        "settle_ms": 500,
        "sample_count": 5,
        "sample_interval_ms": 200,
        "require_untraced": True,
        "require_resumed": True,
    }
    if survival != expected_survival:
        raise SpecError(
            "exact_0a6c_admission requires the accepted survival gate"
        )
    if (
        window.get("max_stops") != 1000
        or window.get("timeout_seconds") != 90
        or window.get("end_milestones") != []
        or not isinstance(window.get("log_path"), str)
        or os.path.basename(window["log_path"]).lower() != "bugs.log"
    ):
        raise SpecError(
            "exact_0a6c_admission requires the accepted bounded window"
        )

    exact_scalars = {
        "pre_stop_pcs": (0x0044F951, 0x0045026C),
        "post_stop_pc": 0x0044C8AB,
        "call_return_address": 0x0044C89E,
        "stack_pointer_register": "esp",
        "entry_return_stack_offset": 88,
        "entry_pointer_stack_offset": 4,
        "entry_index_stack_offset": 8,
        "post_entry_register": "esi",
        "page_register": "esi",
        "entry_root": 0x005A9660,
        "entry_stride": 80,
        "entry_count": 24,
        "candidate_indices": (exact_admission.EXACT_ENTRY_INDEX,),
        "pointer_size": 4,
        "page_count": 32,
        "max_digest_bytes_per_entry": 1,
        "warmup_rollovers": 1,
        "record_pointer_register": "esi",
        "candidate_record_offsets": (exact_admission.EXACT_FILE_OFFSET,),
        "allowed_outcome_page": exact_admission.EXACT_PAGE,
    }
    for name, expected in exact_scalars.items():
        if getattr(capture, name) != expected:
            raise SpecError(
                f"exact_0a6c_admission has non-audited {name}"
            )
    if capture.capture_cycles not in exact_admission.EXACT_ALLOWED_CAPTURE_CYCLES:
        raise SpecError(
            "exact_0a6c_admission capture_cycles must be the audited legacy "
            "single cycle or fixed three-cycle stability bound"
        )

    expected_forms = (
        Direct3DRecordForm(0x3C, 0x0044F951, 4, 6),
        Direct3DRecordForm(0x34, 0x0045026C, 3, 3),
    )
    if capture.record_forms != expected_forms:
        raise SpecError("exact_0a6c_admission has non-audited record forms")

    expected_families = (
        Direct3DBatchFamily(
            id="root_004c4108",
            flush_stop_pc=0x00405838,
            root_pointer_address=0x004C4108,
            allowed_roots=(0x004F1730,),
            vertex_pointer_table_offset=0,
            vertex_count_offset=260,
            index_base_offset=390,
            index_count_offset=130390,
            index_page_stride=2000,
            vertex_stride=32,
            max_vertex_count=500,
            max_index_count=1000,
        ),
        Direct3DBatchFamily(
            id="root_004c410c",
            flush_stop_pc=0x004059AB,
            root_pointer_address=0x004C410C,
            allowed_roots=(0x00511510,),
            vertex_pointer_table_offset=0,
            vertex_count_offset=260,
            index_base_offset=390,
            index_count_offset=307590,
            index_page_stride=9600,
            vertex_stride=32,
            max_vertex_count=500,
            max_index_count=4800,
        ),
    )
    if capture.families != expected_families:
        raise SpecError("exact_0a6c_admission has non-audited batch families")
    if capture.allowed_outcome_family_id != "root_004c4108":
        raise SpecError(
            "exact_0a6c_admission has non-audited outcome family"
        )

    canonical_plan = [
        [item.entry_index, item.file_offset, item.form]
        for item in capture.record_plan
    ]
    plan_bytes = json.dumps(
        canonical_plan, separators=(",", ":")
    ).encode("ascii")
    plan_sha256 = hashlib.sha256(plan_bytes).hexdigest()
    if (
        len(capture.record_plan) != exact_admission.EXACT_RECORD_PLAN_COUNT
        or plan_sha256 != exact_admission.EXACT_RECORD_PLAN_SHA256
    ):
        raise SpecError(
            "exact_0a6c_admission record plan differs from the audited 168-call plan"
        )


def validate_watch_spec(raw: dict) -> WatchSpec:
    """Validate and normalize a watch spec, raising :class:`SpecError`."""

    schema_version = raw.get("schema_version")
    if schema_version not in SUPPORTED_SPEC_SCHEMA_VERSIONS:
        raise SpecError(
            f"unsupported schema_version: {schema_version!r} "
            f"(supported {SUPPORTED_SPEC_SCHEMA_VERSIONS})"
        )
    allowed_spec_keys = {
        "schema_version", "experiment_id", "target", "watchpoints",
        "breakpoints", "window", "on_stop",
    }
    if schema_version >= 2:
        allowed_spec_keys.add("survival")
    if schema_version >= 3:
        allowed_spec_keys.add("submission_capture")
    if schema_version >= 4:
        allowed_spec_keys.add("direct3d_batch_capture")
    _require_keys(raw, allowed_spec_keys, "spec")
    experiment_id = raw.get("experiment_id")
    if not isinstance(experiment_id, str) or not experiment_id:
        raise SpecError("experiment_id must be a non-empty string")

    watch_raw = raw.get("watchpoints") or []
    brk_raw = raw.get("breakpoints") or []
    if not isinstance(watch_raw, list) or not isinstance(brk_raw, list):
        raise SpecError("watchpoints and breakpoints must be lists")
    total = len(watch_raw) + len(brk_raw)
    if not 1 <= total <= HW_SLOTS:
        raise SpecError(
            f"watchpoints + breakpoints must be 1..{HW_SLOTS}, got {total}"
        )

    seen_ids: set[str] = set()

    def _claim_id(value, where: str) -> str:
        if not isinstance(value, str) or not value:
            raise SpecError(f"{where} id must be a non-empty string")
        if value in seen_ids:
            raise SpecError(f"duplicate id: {value!r}")
        seen_ids.add(value)
        return value

    watchpoints: list[Watchpoint] = []
    for i, item in enumerate(watch_raw):
        _require_keys(item, {"id", "address", "kind", "size"}, f"watchpoint[{i}]")
        kind = item.get("kind")
        if kind not in WATCH_KINDS:
            raise SpecError(f"watchpoint[{i}] kind must be one of {WATCH_KINDS}")
        size = item.get("size")
        if size not in WATCH_SIZES:
            raise SpecError(f"watchpoint[{i}] size must be one of {WATCH_SIZES}")
        address = _addr(item.get("address"), f"watchpoint[{i}] address")
        if address % size != 0:
            raise SpecError(
                f"watchpoint[{i}] address 0x{address:x} not aligned to size {size}"
            )
        watchpoints.append(
            Watchpoint(_claim_id(item.get("id"), f"watchpoint[{i}]"), address, kind, size)
        )

    breakpoints: list[Breakpoint] = []
    for i, item in enumerate(brk_raw):
        _require_keys(item, {"id", "address"}, f"breakpoint[{i}]")
        address = _addr(item.get("address"), f"breakpoint[{i}] address")
        breakpoints.append(
            Breakpoint(_claim_id(item.get("id"), f"breakpoint[{i}]"), address)
        )

    window = raw.get("window") or {}
    _require_keys(
        window,
        {"max_stops", "timeout_seconds", "end_milestones", "log_path"},
        "window",
    )
    max_stops = window.get("max_stops", MAX_STOPS)
    if not isinstance(max_stops, int) or not 1 <= max_stops <= MAX_STOPS:
        raise SpecError(f"window.max_stops must be 1..{MAX_STOPS}")
    timeout_seconds = window.get("timeout_seconds", MAX_TIMEOUT_SECONDS)
    if not isinstance(timeout_seconds, int) or not 1 <= timeout_seconds <= MAX_TIMEOUT_SECONDS:
        raise SpecError(f"window.timeout_seconds must be 1..{MAX_TIMEOUT_SECONDS}")
    milestones = window.get("end_milestones") or []
    if not isinstance(milestones, list) or not all(isinstance(m, str) for m in milestones):
        raise SpecError("window.end_milestones must be a list of strings")

    on_stop = raw.get("on_stop") or {}
    _require_keys(on_stop, {"registers", "memory_reads", "backtrace_limit"}, "on_stop")
    registers = on_stop.get("registers") or []
    if not isinstance(registers, list) or not all(isinstance(r, str) for r in registers):
        raise SpecError("on_stop.registers must be a list of strings")
    reads_raw = on_stop.get("memory_reads") or []
    if not isinstance(reads_raw, list):
        raise SpecError("on_stop.memory_reads must be a list")
    if len(reads_raw) > MAX_MEMORY_READS:
        raise SpecError(f"on_stop.memory_reads exceeds {MAX_MEMORY_READS}")
    memory_reads: list[MemoryRead] = []
    for i, item in enumerate(reads_raw):
        _require_keys(item, {"id", "address", "size"}, f"memory_read[{i}]")
        size = item.get("size")
        if not isinstance(size, int) or not 1 <= size <= MAX_MEMORY_READ_BYTES:
            raise SpecError(f"memory_read[{i}] size must be 1..{MAX_MEMORY_READ_BYTES}")
        rid = item.get("id")
        if not isinstance(rid, str) or not rid:
            raise SpecError(f"memory_read[{i}] id must be a non-empty string")
        address = _addr(item.get("address"), f"memory_read[{i}] address")
        memory_reads.append(MemoryRead(rid, address, size))
    backtrace_limit = on_stop.get("backtrace_limit", 8)
    if not isinstance(backtrace_limit, int) or not 0 <= backtrace_limit <= MAX_BACKTRACE:
        raise SpecError(f"on_stop.backtrace_limit must be 0..{MAX_BACKTRACE}")

    survival: dict = {}
    if schema_version >= 2 and "survival" in raw:
        survival_raw = raw.get("survival")
        _require_keys(
            survival_raw,
            {"required", "settle_ms", "sample_count", "sample_interval_ms",
             "require_untraced", "require_resumed"},
            "survival",
        )
        required = survival_raw.get("required", True)
        require_untraced = survival_raw.get("require_untraced", True)
        require_resumed = survival_raw.get("require_resumed", True)
        for key, value in (
            ("required", required),
            ("require_untraced", require_untraced),
            ("require_resumed", require_resumed),
        ):
            if not isinstance(value, bool):
                raise SpecError(f"survival.{key} must be a boolean")
        settle_ms = survival_raw.get("settle_ms", 250)
        sample_count = survival_raw.get("sample_count", 3)
        sample_interval_ms = survival_raw.get("sample_interval_ms", 100)
        if not isinstance(settle_ms, int) or not 0 <= settle_ms <= MAX_SURVIVAL_WINDOW_MS:
            raise SpecError(
                f"survival.settle_ms must be 0..{MAX_SURVIVAL_WINDOW_MS}"
            )
        if not isinstance(sample_count, int) or not 1 <= sample_count <= 20:
            raise SpecError("survival.sample_count must be 1..20")
        if not isinstance(sample_interval_ms, int) or not 0 <= sample_interval_ms <= 5000:
            raise SpecError("survival.sample_interval_ms must be 0..5000")
        total_ms = settle_ms + (sample_count - 1) * sample_interval_ms
        if total_ms > MAX_SURVIVAL_WINDOW_MS:
            raise SpecError(
                f"survival sampling window must be <= {MAX_SURVIVAL_WINDOW_MS} ms"
            )
        survival = {
            "required": required,
            "settle_ms": settle_ms,
            "sample_count": sample_count,
            "sample_interval_ms": sample_interval_ms,
            "require_untraced": require_untraced,
            "require_resumed": require_resumed,
        }

    submission_capture = None
    if schema_version >= 3 and "submission_capture" in raw:
        capture_raw = raw.get("submission_capture")
        _require_keys(
            capture_raw,
            {
                "pre_trigger_id", "post_trigger_id", "entry_register",
                "pre_stop_pc", "post_stop_pc",
                "interval_mode",
                "entry_root", "entry_stride", "entry_count",
                "candidate_indices", "counter_address", "capacity_address",
                "base_pointer_address", "pointer_size", "output_stride",
                "max_records_per_entry", "warmup_rollovers", "capture_cycles",
            },
            "submission_capture",
        )

        pre_trigger_id = capture_raw.get("pre_trigger_id")
        post_trigger_id = capture_raw.get("post_trigger_id")
        interval_mode = capture_raw.get("interval_mode", "paired")
        if interval_mode not in ("paired", "zero_post"):
            raise SpecError(
                "submission_capture.interval_mode must be paired or zero_post"
            )
        trigger_ids = {item.id for item in (*watchpoints, *breakpoints)}
        for key, value in (
            ("pre_trigger_id", pre_trigger_id),
            ("post_trigger_id", post_trigger_id),
        ):
            if not isinstance(value, str) or value not in trigger_ids:
                raise SpecError(
                    f"submission_capture.{key} must name a configured hardware point"
                )
        if interval_mode == "paired" and pre_trigger_id == post_trigger_id:
            raise SpecError("paired submission_capture trigger ids must be distinct")
        if interval_mode == "zero_post" and pre_trigger_id != post_trigger_id:
            raise SpecError("zero_post submission_capture must use one trigger id")

        entry_register = capture_raw.get("entry_register")
        if not isinstance(entry_register, str) or not re.fullmatch(
            r"[A-Za-z][A-Za-z0-9]*", entry_register
        ):
            raise SpecError(
                "submission_capture.entry_register must be a register name"
            )

        def positive_int(key: str, maximum: int) -> int:
            value = capture_raw.get(key)
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or not 1 <= value <= maximum
            ):
                raise SpecError(
                    f"submission_capture.{key} must be 1..{maximum}"
                )
            return value

        entry_stride = positive_int("entry_stride", 0x10000)
        entry_count = positive_int("entry_count", 0x10000)
        output_stride = positive_int("output_stride", 0x10000)
        max_records = positive_int("max_records_per_entry", 0x10000)
        if output_stride * max_records > MAX_SUBMISSION_DIGEST_BYTES:
            raise SpecError(
                "submission_capture maximum digest span exceeds "
                f"{MAX_SUBMISSION_DIGEST_BYTES} bytes"
            )
        pointer_size = capture_raw.get("pointer_size")
        if pointer_size not in (4, 8):
            raise SpecError("submission_capture.pointer_size must be 4 or 8")

        candidate_raw = capture_raw.get("candidate_indices")
        if not isinstance(candidate_raw, list) or not candidate_raw:
            raise SpecError(
                "submission_capture.candidate_indices must be a non-empty list"
            )
        if not all(
            isinstance(value, int)
            and not isinstance(value, bool)
            and 0 <= value < entry_count
            for value in candidate_raw
        ):
            raise SpecError(
                "submission_capture candidate index outside entry_count"
            )
        if len(set(candidate_raw)) != len(candidate_raw):
            raise SpecError("submission_capture candidate indices must be unique")

        submission_capture = SubmissionCapture(
            interval_mode=interval_mode,
            pre_trigger_id=pre_trigger_id,
            post_trigger_id=post_trigger_id,
            pre_stop_pc=(
                _addr(capture_raw.get("pre_stop_pc"),
                      "submission_capture pre_stop_pc")
                if "pre_stop_pc" in capture_raw else None
            ),
            post_stop_pc=(
                _addr(capture_raw.get("post_stop_pc"),
                      "submission_capture post_stop_pc")
                if "post_stop_pc" in capture_raw else None
            ),
            entry_register=entry_register.lower(),
            entry_root=_addr(
                capture_raw.get("entry_root"), "submission_capture entry_root"
            ),
            entry_stride=entry_stride,
            entry_count=entry_count,
            candidate_indices=tuple(sorted(candidate_raw)),
            counter_address=_addr(
                capture_raw.get("counter_address"),
                "submission_capture counter_address",
            ),
            capacity_address=_addr(
                capture_raw.get("capacity_address"),
                "submission_capture capacity_address",
            ),
            base_pointer_address=_addr(
                capture_raw.get("base_pointer_address"),
                "submission_capture base_pointer_address",
            ),
            pointer_size=pointer_size,
            output_stride=output_stride,
            max_records_per_entry=max_records,
            warmup_rollovers=positive_int("warmup_rollovers", 8),
            capture_cycles=positive_int("capture_cycles", 8),
        )

    direct3d_batch_capture = None
    if schema_version >= 4 and "direct3d_batch_capture" in raw:
        batch_raw = raw.get("direct3d_batch_capture")
        allowed_batch_keys = {
            "pre_trigger_id", "flush_trigger_id", "post_trigger_id",
            "pre_stop_pcs", "post_stop_pc", "call_return_address",
            "stack_pointer_register", "entry_return_stack_offset",
            "entry_pointer_stack_offset", "entry_index_stack_offset",
            "post_entry_register", "page_register", "entry_root",
            "entry_stride", "entry_count", "candidate_indices",
            "pointer_size", "page_count", "families",
            "max_digest_bytes_per_entry", "warmup_rollovers",
            "capture_cycles",
        }
        if schema_version >= 5:
            allowed_batch_keys.update({
                "capture_mode", "record_pointer_register", "record_forms",
                "record_plan", "candidate_record_offsets",
                "allowed_outcome_family_id", "allowed_outcome_page",
            })
        _require_keys(
            batch_raw,
            allowed_batch_keys,
            "direct3d_batch_capture",
        )
        if submission_capture is not None:
            raise SpecError(
                "submission_capture and direct3d_batch_capture are mutually exclusive"
            )

        trigger_ids = {item.id for item in watchpoints}
        trigger_values = []
        for key in ("pre_trigger_id", "flush_trigger_id", "post_trigger_id"):
            value = batch_raw.get(key)
            if not isinstance(value, str) or value not in trigger_ids:
                raise SpecError(
                    f"direct3d_batch_capture.{key} must name a configured "
                    "hardware point backed by a data watchpoint"
                )
            trigger_values.append(value)
        if len(set(trigger_values)) != 3:
            raise SpecError("direct3d_batch_capture trigger ids must be distinct")
        if memory_reads:
            raise SpecError(
                "direct3d_batch_capture forbids on_stop.memory_reads; "
                "the capture retains metadata and digests only"
            )

        capture_mode = batch_raw.get("capture_mode", "entry_digest")
        if capture_mode not in (
            "entry_digest", "record_outcome", "exact_0a6c_admission",
        ):
            raise SpecError(
                "direct3d_batch_capture.capture_mode must be "
                "entry_digest, record_outcome, or exact_0a6c_admission"
            )
        if capture_mode == "record_outcome" and schema_version < 5:
            raise SpecError(
                "direct3d_batch_capture record_outcome mode requires schema 5"
            )
        if capture_mode == "exact_0a6c_admission" and schema_version < 6:
            raise SpecError(
                "direct3d_batch_capture exact_0a6c_admission mode requires schema 6"
            )

        def batch_positive_int(key: str, maximum: int) -> int:
            value = batch_raw.get(key)
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or not 1 <= value <= maximum
            ):
                raise SpecError(
                    f"direct3d_batch_capture.{key} must be 1..{maximum}"
                )
            return value

        def batch_offset(key: str, where: str, obj: dict = batch_raw) -> int:
            value = obj.get(key)
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or not 0 <= value <= 0x1000000
            ):
                raise SpecError(f"{where}.{key} must be 0..0x1000000")
            return value

        def batch_register(key: str) -> str:
            value = batch_raw.get(key)
            if not isinstance(value, str) or not re.fullmatch(
                r"[A-Za-z][A-Za-z0-9]*", value
            ):
                raise SpecError(
                    f"direct3d_batch_capture.{key} must be a register name"
                )
            return value.lower()

        pre_pcs_raw = batch_raw.get("pre_stop_pcs")
        if not isinstance(pre_pcs_raw, list) or not pre_pcs_raw:
            raise SpecError(
                "direct3d_batch_capture.pre_stop_pcs must be a non-empty list"
            )
        pre_stop_pcs = tuple(
            _addr(value, "direct3d_batch_capture pre_stop_pc")
            for value in pre_pcs_raw
        )
        if len(set(pre_stop_pcs)) != len(pre_stop_pcs):
            raise SpecError("direct3d_batch_capture pre_stop_pcs must be unique")

        entry_stride = batch_positive_int("entry_stride", 0x10000)
        entry_count = batch_positive_int("entry_count", 0x10000)
        pointer_size = batch_raw.get("pointer_size")
        if pointer_size not in (4, 8):
            raise SpecError("direct3d_batch_capture.pointer_size must be 4 or 8")
        page_count = batch_positive_int("page_count", MAX_BATCH_PAGES)
        max_digest_bytes = batch_positive_int(
            "max_digest_bytes_per_entry", MAX_BATCH_DIGEST_BYTES
        )

        candidate_raw = batch_raw.get("candidate_indices")
        if not isinstance(candidate_raw, list) or not candidate_raw:
            raise SpecError(
                "direct3d_batch_capture.candidate_indices must be a non-empty list"
            )
        if not all(
            isinstance(value, int)
            and not isinstance(value, bool)
            and 0 <= value < entry_count
            for value in candidate_raw
        ):
            raise SpecError(
                "direct3d_batch_capture candidate index outside entry_count"
            )
        if len(set(candidate_raw)) != len(candidate_raw):
            raise SpecError(
                "direct3d_batch_capture candidate indices must be unique"
            )

        families_raw = batch_raw.get("families")
        if not isinstance(families_raw, list) or not families_raw:
            raise SpecError(
                "direct3d_batch_capture.families must be a non-empty list"
            )
        families = []
        family_ids = set()
        flush_pcs = set()
        for index, family_raw in enumerate(families_raw):
            where = f"direct3d_batch_capture.families[{index}]"
            _require_keys(
                family_raw,
                {
                    "id", "flush_stop_pc", "root_pointer_address",
                    "allowed_roots", "vertex_pointer_table_offset",
                    "vertex_count_offset", "index_base_offset",
                    "index_count_offset", "index_page_stride",
                    "vertex_stride", "max_vertex_count", "max_index_count",
                },
                where,
            )
            family_id = family_raw.get("id")
            if not isinstance(family_id, str) or not family_id:
                raise SpecError(f"{where}.id must be a non-empty string")
            if family_id in family_ids:
                raise SpecError("direct3d_batch_capture family ids must be unique")
            family_ids.add(family_id)
            flush_stop_pc = _addr(
                family_raw.get("flush_stop_pc"), f"{where} flush_stop_pc"
            )
            if flush_stop_pc in flush_pcs:
                raise SpecError(
                    "direct3d_batch_capture family flush_stop_pc values must be unique"
                )
            flush_pcs.add(flush_stop_pc)
            roots_raw = family_raw.get("allowed_roots")
            if not isinstance(roots_raw, list) or not roots_raw:
                raise SpecError(f"{where}.allowed_roots must be a non-empty list")
            roots = tuple(_addr(value, f"{where} allowed_root") for value in roots_raw)
            if len(set(roots)) != len(roots):
                raise SpecError(f"{where}.allowed_roots must be unique")

            def family_positive_int(key: str, maximum: int) -> int:
                value = family_raw.get(key)
                if (
                    not isinstance(value, int)
                    or isinstance(value, bool)
                    or not 1 <= value <= maximum
                ):
                    raise SpecError(f"{where}.{key} must be 1..{maximum}")
                return value

            family = Direct3DBatchFamily(
                id=family_id,
                flush_stop_pc=flush_stop_pc,
                root_pointer_address=_addr(
                    family_raw.get("root_pointer_address"),
                    f"{where} root_pointer_address",
                ),
                allowed_roots=roots,
                vertex_pointer_table_offset=batch_offset(
                    "vertex_pointer_table_offset", where, family_raw
                ),
                vertex_count_offset=batch_offset(
                    "vertex_count_offset", where, family_raw
                ),
                index_base_offset=batch_offset(
                    "index_base_offset", where, family_raw
                ),
                index_count_offset=batch_offset(
                    "index_count_offset", where, family_raw
                ),
                index_page_stride=family_positive_int(
                    "index_page_stride", 0x1000000
                ),
                vertex_stride=family_positive_int("vertex_stride", 0x10000),
                max_vertex_count=family_positive_int(
                    "max_vertex_count", 0x100000
                ),
                max_index_count=family_positive_int(
                    "max_index_count", 0x100000
                ),
            )
            if family.max_index_count * 2 > family.index_page_stride:
                raise SpecError(f"{where} index bound exceeds page stride")
            families.append(family)

        record_pointer_register = None
        record_forms: tuple[Direct3DRecordForm, ...] = ()
        record_plan: tuple[Direct3DRecordPlanItem, ...] = ()
        candidate_record_offsets: tuple[int, ...] = ()
        allowed_outcome_family_id = None
        allowed_outcome_page = None
        if capture_mode in ("record_outcome", "exact_0a6c_admission"):
            record_pointer_register = batch_register("record_pointer_register")

            forms_raw = batch_raw.get("record_forms")
            if not isinstance(forms_raw, list) or not forms_raw:
                raise SpecError(
                    "direct3d_batch_capture.record_forms must be a non-empty list"
                )
            parsed_forms = []
            seen_forms = set()
            seen_form_pcs = set()
            for index, form_raw in enumerate(forms_raw):
                where = f"direct3d_batch_capture.record_forms[{index}]"
                _require_keys(
                    form_raw,
                    {"form", "stop_pc", "append_vertex_count",
                     "append_index_count"},
                    where,
                )
                form = form_raw.get("form")
                if (
                    not isinstance(form, int) or isinstance(form, bool)
                    or not 1 <= form <= 0x10000
                ):
                    raise SpecError(f"{where}.form must be 1..0x10000")
                if form in seen_forms:
                    raise SpecError(
                        "direct3d_batch_capture record form values must be unique"
                    )
                stop_pc = _addr(form_raw.get("stop_pc"), f"{where} stop_pc")
                if stop_pc in seen_form_pcs:
                    raise SpecError(
                        "direct3d_batch_capture record form stop PCs must be unique"
                    )
                append_vertex_count = form_raw.get("append_vertex_count")
                append_index_count = form_raw.get("append_index_count")
                if not all(
                    isinstance(value, int) and not isinstance(value, bool)
                    and 1 <= value <= 0x10000
                    for value in (append_vertex_count, append_index_count)
                ):
                    raise SpecError(
                        f"{where} append counts must be 1..0x10000"
                    )
                seen_forms.add(form)
                seen_form_pcs.add(stop_pc)
                parsed_forms.append(Direct3DRecordForm(
                    form=form,
                    stop_pc=stop_pc,
                    append_vertex_count=append_vertex_count,
                    append_index_count=append_index_count,
                ))
            if seen_form_pcs != set(pre_stop_pcs):
                raise SpecError(
                    "direct3d_batch_capture record form stop PCs must exactly "
                    "match pre_stop_pcs"
                )
            record_forms = tuple(parsed_forms)

            plan_raw = batch_raw.get("record_plan")
            if not isinstance(plan_raw, list) or not plan_raw:
                raise SpecError(
                    "direct3d_batch_capture.record_plan must be a non-empty list"
                )
            parsed_plan = []
            prior_entry = -1
            prior_offset = -1
            for index, item_raw in enumerate(plan_raw):
                where = f"direct3d_batch_capture.record_plan[{index}]"
                _require_keys(
                    item_raw, {"entry_index", "file_offset", "form"}, where
                )
                plan_entry = item_raw.get("entry_index")
                plan_offset = item_raw.get("file_offset")
                plan_form = item_raw.get("form")
                if (
                    not isinstance(plan_entry, int)
                    or isinstance(plan_entry, bool)
                    or not 0 <= plan_entry < entry_count
                ):
                    raise SpecError(f"{where}.entry_index outside entry_count")
                if (
                    not isinstance(plan_offset, int)
                    or isinstance(plan_offset, bool)
                    or not 0 <= plan_offset <= 0x1000000
                ):
                    raise SpecError(f"{where}.file_offset must be 0..0x1000000")
                if plan_form not in seen_forms:
                    raise SpecError(f"{where}.form is not configured")
                if plan_entry < prior_entry or plan_offset <= prior_offset:
                    raise SpecError(
                        "direct3d_batch_capture record plan must have "
                        "nondecreasing entries and strictly increasing offsets"
                    )
                parsed_plan.append(Direct3DRecordPlanItem(
                    entry_index=plan_entry,
                    file_offset=plan_offset,
                    form=plan_form,
                ))
                prior_entry = plan_entry
                prior_offset = plan_offset
            record_plan = tuple(parsed_plan)

            offsets_raw = batch_raw.get("candidate_record_offsets")
            if not isinstance(offsets_raw, list) or not offsets_raw:
                raise SpecError(
                    "direct3d_batch_capture.candidate_record_offsets must be "
                    "a non-empty list"
                )
            if not all(
                isinstance(value, int) and not isinstance(value, bool)
                and 0 <= value <= 0x1000000
                for value in offsets_raw
            ):
                raise SpecError(
                    "direct3d_batch_capture candidate record offset out of range"
                )
            if len(set(offsets_raw)) != len(offsets_raw):
                raise SpecError(
                    "direct3d_batch_capture candidate record offsets must be unique"
                )
            plan_offsets = {item.file_offset for item in record_plan}
            if not set(offsets_raw) <= plan_offsets:
                raise SpecError(
                    "direct3d_batch_capture candidate record offsets must be "
                    "a subset of record_plan"
                )
            candidate_record_offsets = tuple(sorted(offsets_raw))
            candidate_entries = {
                item.entry_index for item in record_plan
                if item.file_offset in candidate_record_offsets
            }
            if candidate_entries != set(candidate_raw):
                raise SpecError(
                    "direct3d_batch_capture candidate_indices must exactly match "
                    "candidate record entries"
                )

            allowed_outcome_family_id = batch_raw.get(
                "allowed_outcome_family_id"
            )
            if allowed_outcome_family_id not in family_ids:
                raise SpecError(
                    "direct3d_batch_capture.allowed_outcome_family_id must name "
                    "a configured family"
                )
            allowed_outcome_page = batch_raw.get("allowed_outcome_page")
            if (
                not isinstance(allowed_outcome_page, int)
                or isinstance(allowed_outcome_page, bool)
                or not 0 <= allowed_outcome_page < page_count
            ):
                raise SpecError(
                    "direct3d_batch_capture.allowed_outcome_page outside page_count"
                )
        else:
            record_only_keys = {
                "record_pointer_register", "record_forms", "record_plan",
                "candidate_record_offsets", "allowed_outcome_family_id",
                "allowed_outcome_page",
            }
            present = record_only_keys & set(batch_raw)
            if present:
                raise SpecError(
                    "direct3d_batch_capture entry_digest mode has record-only "
                    f"keys: {sorted(present)}"
                )

        direct3d_batch_capture = Direct3DBatchCapture(
            pre_trigger_id=trigger_values[0],
            flush_trigger_id=trigger_values[1],
            post_trigger_id=trigger_values[2],
            pre_stop_pcs=pre_stop_pcs,
            post_stop_pc=_addr(
                batch_raw.get("post_stop_pc"),
                "direct3d_batch_capture post_stop_pc",
            ),
            call_return_address=_addr(
                batch_raw.get("call_return_address"),
                "direct3d_batch_capture call_return_address",
            ),
            stack_pointer_register=batch_register("stack_pointer_register"),
            entry_return_stack_offset=batch_offset(
                "entry_return_stack_offset", "direct3d_batch_capture"
            ),
            entry_pointer_stack_offset=batch_offset(
                "entry_pointer_stack_offset", "direct3d_batch_capture"
            ),
            entry_index_stack_offset=batch_offset(
                "entry_index_stack_offset", "direct3d_batch_capture"
            ),
            post_entry_register=batch_register("post_entry_register"),
            page_register=batch_register("page_register"),
            entry_root=_addr(
                batch_raw.get("entry_root"), "direct3d_batch_capture entry_root"
            ),
            entry_stride=entry_stride,
            entry_count=entry_count,
            candidate_indices=tuple(sorted(candidate_raw)),
            pointer_size=pointer_size,
            page_count=page_count,
            families=tuple(families),
            max_digest_bytes_per_entry=max_digest_bytes,
            warmup_rollovers=batch_positive_int("warmup_rollovers", 8),
            capture_cycles=batch_positive_int("capture_cycles", 8),
            capture_mode=capture_mode,
            record_pointer_register=record_pointer_register,
            record_forms=record_forms,
            record_plan=record_plan,
            candidate_record_offsets=candidate_record_offsets,
            allowed_outcome_family_id=allowed_outcome_family_id,
            allowed_outcome_page=allowed_outcome_page,
        )

        if capture_mode == "exact_0a6c_admission":
            _validate_exact_0a6c_capture(
                direct3d_batch_capture,
                raw_target=raw.get("target") or {},
                watchpoints=tuple(watchpoints),
                breakpoints=tuple(breakpoints),
                registers=tuple(registers),
                memory_reads=tuple(memory_reads),
                backtrace_limit=backtrace_limit,
                window=window,
                survival=survival,
            )

    return WatchSpec(
        schema_version=schema_version,
        experiment_id=experiment_id,
        target=raw.get("target") or {},
        watchpoints=tuple(watchpoints),
        breakpoints=tuple(breakpoints),
        window=window,
        on_stop=on_stop,
        survival=survival,
        registers=tuple(registers),
        memory_reads=tuple(memory_reads),
        backtrace_limit=backtrace_limit,
        submission_capture=submission_capture,
        direct3d_batch_capture=direct3d_batch_capture,
    )


# --------------------------------------------------------------------------
# ELF core iteration (shared with core-grep.py)
# --------------------------------------------------------------------------


ELF_MAGIC = b"\x7fELF"
ELFCLASS32 = 1
ELFCLASS64 = 2
ELFDATA2LSB = 1
ET_CORE = 4
PT_LOAD = 1
PN_XNUM = 0xFFFF


@dataclass(frozen=True)
class LoadSegment:
    index: int
    vaddr: int
    file_offset: int
    file_size: int
    mem_size: int
    flags: int
    truncated: bool

    @property
    def flags_str(self) -> str:
        r = "r" if self.flags & 0x4 else "-"
        w = "w" if self.flags & 0x2 else "-"
        x = "x" if self.flags & 0x1 else "-"
        return r + w + x


def iter_core_load_segments(data: bytes) -> Iterator[LoadSegment]:
    """Yield PT_LOAD segments from an ELF core, bounds-checking every field."""

    if len(data) < 20 or data[:4] != ELF_MAGIC:
        raise ElfCoreError("not an ELF file (bad magic)")
    ei_class = data[4]
    ei_data = data[5]
    if ei_class not in (ELFCLASS32, ELFCLASS64):
        raise ElfCoreError(f"unsupported ELF class: {ei_class}")
    if ei_data != ELFDATA2LSB:
        raise ElfCoreError("only little-endian ELF cores are supported")

    is64 = ei_class == ELFCLASS64
    if is64:
        if len(data) < 64:
            raise ElfCoreError("truncated ELF64 header")
        e_type = struct.unpack_from("<H", data, 16)[0]
        e_phoff = struct.unpack_from("<Q", data, 32)[0]
        e_phentsize = struct.unpack_from("<H", data, 54)[0]
        e_phnum = struct.unpack_from("<H", data, 56)[0]
        want_phentsize = 56
    else:
        if len(data) < 52:
            raise ElfCoreError("truncated ELF32 header")
        e_type = struct.unpack_from("<H", data, 16)[0]
        e_phoff = struct.unpack_from("<I", data, 28)[0]
        e_phentsize = struct.unpack_from("<H", data, 42)[0]
        e_phnum = struct.unpack_from("<H", data, 44)[0]
        want_phentsize = 32

    if e_type != ET_CORE:
        raise ElfCoreError(f"not an ET_CORE file (e_type={e_type})")
    if e_phnum == PN_XNUM:
        raise ElfCoreError("PN_XNUM program-header count is unsupported")
    if e_phentsize != want_phentsize:
        raise ElfCoreError(
            f"unexpected e_phentsize {e_phentsize} (want {want_phentsize})"
        )
    if e_phnum == 0:
        raise ElfCoreError("no program headers")
    table_end = e_phoff + e_phnum * e_phentsize
    if e_phoff < want_phentsize or table_end > len(data):
        raise ElfCoreError("program-header table out of bounds")

    for i in range(e_phnum):
        base = e_phoff + i * e_phentsize
        if is64:
            p_type, p_flags = struct.unpack_from("<II", data, base)
            p_offset, p_vaddr = struct.unpack_from("<QQ", data, base + 8)
            p_filesz = struct.unpack_from("<Q", data, base + 32)[0]
            p_memsz = struct.unpack_from("<Q", data, base + 40)[0]
        else:
            p_type = struct.unpack_from("<I", data, base)[0]
            p_offset, p_vaddr = struct.unpack_from("<II", data, base + 4)
            p_filesz, p_memsz = struct.unpack_from("<II", data, base + 16)
            p_flags = struct.unpack_from("<I", data, base + 24)[0]
        if p_type != PT_LOAD or p_filesz == 0:
            continue
        truncated = p_offset + p_filesz > len(data)
        yield LoadSegment(
            index=i,
            vaddr=p_vaddr,
            file_offset=p_offset,
            file_size=p_filesz,
            mem_size=p_memsz,
            flags=p_flags,
            truncated=truncated,
        )


# --------------------------------------------------------------------------
# CLI (used by the bash wrappers)
# --------------------------------------------------------------------------


def _cmd_ownership(args: argparse.Namespace) -> int:
    try:
        proof = ownership_proof(
            args.pid,
            expected_sha256=args.expected_sha,
            exe_basename=args.exe_basename,
            loader_re=args.loader_re,
            cwd_prefix=args.cwd_prefix,
        )
    except OwnershipError as exc:
        payload = {
            "refused": True,
            "tool": "evidence_lib",
            "reason": exc.reason,
            "detail": exc.detail,
        }
        print(json.dumps(payload))
        return EXIT_REFUSAL
    print(json.dumps(proof.to_dict()))
    return EXIT_OK


def _cmd_sha256(args: argparse.Namespace) -> int:
    print(sha256_file(args.path))
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ABLPC evidence helper")
    sub = parser.add_subparsers(dest="command", required=True)

    own = sub.add_parser("ownership", help="prove a PID is the expected game")
    own.add_argument("--pid", type=int, required=True)
    own.add_argument("--expected-sha", default=None)
    own.add_argument("--exe-basename", default=DEFAULT_EXE_BASENAME)
    own.add_argument("--loader-re", default=DEFAULT_LOADER_RE)
    own.add_argument("--cwd-prefix", default=None)
    own.add_argument("--json", action="store_true", help="accepted for symmetry")
    own.set_defaults(func=_cmd_ownership)

    sha = sub.add_parser("sha256", help="hash a file")
    sha.add_argument("path")
    sha.set_defaults(func=_cmd_sha256)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
