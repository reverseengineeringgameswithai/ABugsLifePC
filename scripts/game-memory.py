#!/usr/bin/env python3
"""Bounded live memory access for the exact PC game process.

Replaces the per-experiment throwaway C and Python helpers (``gate_probe.c``,
``grain_gate_probe.c``, ``teleport_flik_keep_anchor.c``, ``state_watch.c``, ...)
that each re-derived identity proof, ``process_vm_readv`` framing, and guarded
writes.  Every subcommand proves target identity from ``/proc`` before touching
the process and emits JSON.

Read verbs (``peek``, ``state``, ``watch``) are ordinary evidence gathering.

Write verbs are not.  ``poke`` and ``teleport`` require an explicit
authorization reference, refuse without a compare-before-write guard, read the
target back, and write a receipt under ``dynamic/wine/RUN-POKE-<stamp>/``.
``teleport`` additionally enforces the mandatory preflight and accepted write
boundary from ``Vault/40-Implementation/PC Flik teleport procedure.md``:
current+preceding only, in one 24-byte call, to a destination whose walkable
evidence the caller must cite, with a settle check afterwards.  A write is
still write-assisted: it never makes a later observation natural gameplay.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import time
from typing import Any, Callable, Iterable

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import evidence_lib as ev  # noqa: E402
import session_lib as sl  # noqa: E402


TOOL = "game-memory"
TOOL_VERSION = "1.1.0"
RECEIPT_SCHEMA_VERSION = 1
POKE_RUN_PREFIX = "POKE"
RESTORE_RUN_PREFIX = "RESTORE"
SNAPSHOT_SCHEMA_VERSION = 1
DEFAULT_SNAPSHOT_DIR = "work/snapshots"
SNAPSHOT_NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,80}$")

MAX_WATCH_SAMPLES = 100_000
MAX_WATCH_DURATION_S = 3600.0
MIN_WATCH_INTERVAL_MS = 1

# Position globals confirmed by EXP-20260815-128 and recorded in
# Vault/40-Implementation/PC Flik teleport procedure.md.  All components are
# signed little-endian 32-bit integers.
CURRENT_XYZ_ADDRESS = 0x0059D910
PRECEDING_XYZ_ADDRESS = 0x0059D920
AUXILIARY_XYZ_ADDRESS = 0x0059D960
FLAGS_ADDRESS = 0x0059D9A0
NEXT_LIFE_ADDRESS = 0x0059A5B0
TELEPORT_WRITE_BYTES = 24

FORMATS = (
    "hex", "u8", "i8", "u16", "i16", "u32", "i32", "u64", "i64", "f32", "f64",
    "utf8", "bytes",
)
_STRUCT = {
    "u8": "<B", "i8": "<b", "u16": "<H", "i16": "<h",
    "u32": "<I", "i32": "<i", "u64": "<Q", "i64": "<q",
    "f32": "<f", "f64": "<d",
}


class UsageError(ValueError):
    """Raised for a malformed command line."""


def _fail(reason: str, detail: str = "") -> int:
    print(json.dumps(sl.refusal(TOOL, reason, detail)))
    return ev.EXIT_REFUSAL


def parse_address(text: str) -> int:
    value = text.strip()
    if not value:
        raise UsageError("empty address")
    try:
        parsed = int(value, 16) if value.lower().startswith("0x") else int(value, 16)
    except ValueError as exc:
        raise UsageError(f"not a hex address: {text!r}") from exc
    if parsed <= 0 or parsed >= 2 ** 64:
        raise UsageError(f"address out of range: {text!r}")
    return parsed


def parse_signed_int(text: str) -> int:
    value = text.strip()
    try:
        parsed = int(value, 0)
    except ValueError as exc:
        raise UsageError(f"not an integer: {text!r}") from exc
    if not -(2 ** 31) <= parsed < 2 ** 31:
        raise UsageError(f"value out of signed 32-bit range: {text!r}")
    return parsed


def parse_hex_bytes(text: str) -> bytes:
    cleaned = text.strip().replace(" ", "").replace("_", "").replace(":", "")
    if cleaned.lower().startswith("0x"):
        cleaned = cleaned[2:]
    if not cleaned or len(cleaned) % 2:
        raise UsageError(f"hex payload must have an even digit count: {text!r}")
    try:
        return bytes.fromhex(cleaned)
    except ValueError as exc:
        raise UsageError(f"not hex bytes: {text!r}") from exc


def parse_read_spec(text: str) -> tuple[int, int]:
    """Parse ``ADDR:SIZE`` into ``(address, size)``."""

    if ":" not in text:
        raise UsageError(f"read spec must be ADDR:SIZE, got {text!r}")
    address_text, size_text = text.rsplit(":", 1)
    address = parse_address(address_text)
    try:
        size = int(size_text, 0)
    except ValueError as exc:
        raise UsageError(f"not a size: {size_text!r}") from exc
    if size <= 0 or size > sl.MAX_MEMORY_RANGE_BYTES:
        raise UsageError(
            f"size must be 1..{sl.MAX_MEMORY_RANGE_BYTES}, got {size}"
        )
    return address, size


def decode(payload: bytes, fmt: str) -> Any:
    """Decode raw bytes for reporting.  ``hex``/``bytes`` never fail."""

    if fmt in {"hex", "bytes"}:
        return payload.hex()
    if fmt == "utf8":
        return payload.split(b"\x00", 1)[0].decode("utf-8", "replace")
    layout = _STRUCT[fmt]
    width = struct.calcsize(layout)
    if len(payload) % width:
        raise UsageError(
            f"{len(payload)} bytes is not a multiple of {width} for format {fmt}"
        )
    values = [struct.unpack_from(layout, payload, off)[0]
              for off in range(0, len(payload), width)]
    return values[0] if len(values) == 1 else values


# --------------------------------------------------------------------------
# Target resolution
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Target:
    pid: int
    process_group: int
    start_ticks: int
    proof: ev.OwnershipProof
    session_id: str | None

    def to_dict(self) -> dict:
        return {
            "pid": self.pid,
            "process_group": self.process_group,
            "start_ticks": self.start_ticks,
            "session_id": self.session_id,
            "ownership": self.proof.to_dict(),
        }


def resolve_target(args: argparse.Namespace) -> Target:
    """Prove the target identity before any memory access.

    Accepts either an explicit ``--pid`` or a ``--session`` handle; a session
    additionally binds the recorded start ticks so a recycled PID is refused.
    """

    session_id: str | None = None
    expected_ticks: int | None = None
    pid = getattr(args, "pid", None)
    if getattr(args, "session", None):
        manifest = sl.resolve_session(args.session)
        session_id = manifest.session_id
        if manifest.game_pid is None:
            raise sl.SessionError("session_incomplete", f"{session_id} has no game PID")
        if pid is not None and pid != manifest.game_pid:
            raise sl.SessionError(
                "pid_session_conflict",
                f"--pid {pid} does not match session game PID {manifest.game_pid}",
            )
        pid = manifest.game_pid
        expected_ticks = manifest.game_start_ticks
    if pid is None:
        raise UsageError("one of --pid or --session is required")

    group, ticks = sl.pid_identity(pid)
    if expected_ticks is not None and ticks != expected_ticks:
        raise sl.SessionError(
            "pid_recycled",
            f"pid {pid} start ticks {ticks} != recorded {expected_ticks}",
        )
    proof = ev.ownership_proof(
        pid,
        expected_sha256=getattr(args, "expected_sha", None),
        exe_basename=getattr(args, "exe_basename", ev.DEFAULT_EXE_BASENAME),
        loader_re=getattr(args, "loader_re", ev.DEFAULT_LOADER_RE),
        cwd_prefix=getattr(args, "cwd_prefix", None),
    )
    accepted = getattr(args, "accept_sha", None) or []
    allowed = {value.lower() for value in accepted} or set(sl.ACCEPTED_EXECUTABLE_SHA256S)
    if not getattr(args, "any_exe_sha", False):
        if proof.exe_sha256.lower() not in allowed:
            raise sl.SessionError(
                "unexpected_executable",
                f"{proof.exe_sha256} is not an accepted build "
                "(pass --accept-sha or --any-exe-sha to widen, and disclose it)",
            )
    return Target(
        pid=pid,
        process_group=group,
        start_ticks=ticks,
        proof=proof,
        session_id=session_id,
    )


def _memory(target: Target) -> sl.ProcessMemory:
    return sl.ProcessMemory(target.pid)


# --------------------------------------------------------------------------
# Read verbs
# --------------------------------------------------------------------------


def cmd_peek(args: argparse.Namespace) -> int:
    target = resolve_target(args)
    plan = [parse_read_spec(spec) for spec in args.read]
    memory = _memory(target)
    payloads = memory.read_many(plan)
    reads = []
    for (address, size), payload in zip(plan, payloads, strict=True):
        row: dict[str, Any] = {
            "address": f"0x{address:08X}",
            "size": size,
            "hex": payload.hex(),
        }
        if args.format not in {"hex", "bytes"}:
            row["value"] = decode(payload, args.format)
            row["format"] = args.format
        reads.append(row)
    print(json.dumps({
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "verb": "peek",
        "target": target.to_dict(),
        "sampled_ns": time.monotonic_ns(),
        "reads": reads,
    }, indent=2 if args.pretty else None))
    return ev.EXIT_OK


def _coordinate_overlay():
    """Import the audited coordinate reader for its field layout.

    The address constants and sample decoding live in
    ``scripts/coordinate-overlay.py`` (EXP-20260815-127/128).  Importing them
    keeps one source of truth rather than a second copy that can drift.
    """

    cached = sys.modules.get("coordinate_overlay")
    if cached is not None:
        return cached
    spec = importlib.util.spec_from_file_location(
        "coordinate_overlay", SCRIPTS / "coordinate-overlay.py"
    )
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise sl.SessionError("overlay_unavailable", "cannot load coordinate-overlay.py")
    module = importlib.util.module_from_spec(spec)
    # Registered before execution because the module defines dataclasses, and
    # dataclass field resolution looks the defining module up in sys.modules.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _state_sample(memory: sl.ProcessMemory) -> dict:
    overlay = _coordinate_overlay()
    sample = overlay.read_coordinate_sample(memory)
    return {
        "x": sample.x,
        "y": sample.y,
        "z": sample.z,
        "level": sample.level,
        "flags": sample.flags,
        "flags_hex": f"0x{sample.flags:04X}",
        "next_life": sample.next_life,
        "state_counter": sample.state_counter,
        "collision_index": sample.collision_index,
        "collision_material": sample.collision_material,
        "sampled_ns": sample.sampled_ns,
    }


def cmd_state(args: argparse.Namespace) -> int:
    target = resolve_target(args)
    memory = _memory(target)
    state = _state_sample(memory)
    if args.triples:
        current, preceding, auxiliary = memory.read_many(
            (
                (CURRENT_XYZ_ADDRESS, 12),
                (PRECEDING_XYZ_ADDRESS, 12),
                (AUXILIARY_XYZ_ADDRESS, 12),
            )
        )
        state["triples"] = {
            "current": list(struct.unpack("<iii", current)),
            "preceding": list(struct.unpack("<iii", preceding)),
            "auxiliary": list(struct.unpack("<iii", auxiliary)),
        }
    print(json.dumps({
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "verb": "state",
        "target": target.to_dict(),
        "state": state,
    }, indent=2 if args.pretty else None))
    return ev.EXIT_OK


def cmd_watch(args: argparse.Namespace) -> int:
    """Sample ranges (or the state block) on an interval, emitting JSONL.

    This is the read-only observer the teleport procedure requires to be
    running before a write, and the sampler previous packets rebuilt by hand.
    """

    target = resolve_target(args)
    if args.interval_ms < MIN_WATCH_INTERVAL_MS:
        raise UsageError(f"--interval-ms must be >= {MIN_WATCH_INTERVAL_MS}")
    if args.duration_s <= 0 or args.duration_s > MAX_WATCH_DURATION_S:
        raise UsageError(f"--duration-s must be 0 < d <= {MAX_WATCH_DURATION_S}")
    plan = [parse_read_spec(spec) for spec in args.read] if args.read else []
    memory = _memory(target)

    handle = open(args.out, "w", encoding="utf-8") if args.out else None
    samples = 0
    changes = 0
    previous: tuple[bytes, ...] | None = None
    started = time.monotonic()
    deadline = started + args.duration_s
    failures = 0
    try:
        while time.monotonic() < deadline and samples < MAX_WATCH_SAMPLES:
            row: dict[str, Any] = {
                "sample": samples,
                "monotonic_ns": time.monotonic_ns(),
                "elapsed_s": round(time.monotonic() - started, 6),
            }
            try:
                if plan:
                    payloads = memory.read_many(plan)
                    row["reads"] = [
                        {
                            "address": f"0x{address:08X}",
                            "size": size,
                            "hex": payload.hex(),
                            **(
                                {"value": decode(payload, args.format)}
                                if args.format not in {"hex", "bytes"}
                                else {}
                            ),
                        }
                        for (address, size), payload in zip(plan, payloads, strict=True)
                    ]
                    if previous is not None and payloads != previous:
                        row["changed"] = True
                        changes += 1
                    previous = payloads
                if args.state:
                    row["state"] = _state_sample(memory)
            except sl.SessionError as exc:
                failures += 1
                row["error"] = {"reason": exc.reason, "detail": exc.detail}
                if failures > args.max_read_failures:
                    row["aborted"] = True
                    _emit_sample(row, handle)
                    samples += 1
                    break
            _emit_sample(row, handle)
            samples += 1
            if args.until_change and row.get("changed"):
                break
            time.sleep(args.interval_ms / 1000.0)
    finally:
        if handle is not None:
            handle.close()

    summary = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "verb": "watch",
        "target": target.to_dict(),
        "samples": samples,
        "changes": changes,
        "read_failures": failures,
        "duration_s": round(time.monotonic() - started, 6),
        "out": str(args.out) if args.out else None,
        "interval_ms": args.interval_ms,
    }
    print(json.dumps(summary, indent=2 if args.pretty else None))
    return ev.EXIT_OK if failures <= args.max_read_failures else ev.EXIT_TOOL_NEGATIVE


def _emit_sample(row: dict, handle) -> None:
    line = json.dumps(row)
    if handle is not None:
        handle.write(line + "\n")
        handle.flush()
    else:
        print(line, file=sys.stderr)


# --------------------------------------------------------------------------
# Write verbs
# --------------------------------------------------------------------------


def _receipt_dir(root: Path | None = None) -> Path:
    return ev.new_run_dir(POKE_RUN_PREFIX, root=root)


def _write_receipt(payload: dict, *, root: Path | None = None) -> Path:
    directory = _receipt_dir(root=root)
    path = directory / "receipt.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def cmd_poke(args: argparse.Namespace) -> int:
    """Guarded single-range write.

    Fail-closed by construction: an authorization reference is mandatory, the
    current bytes must match ``--expect-current`` unless the caller explicitly
    and disclosably opts out, and the write is read back and verified.
    """

    target = resolve_target(args)
    payload = parse_hex_bytes(args.bytes)
    address = parse_address(args.addr)
    if not args.authorize.strip():
        raise UsageError("--authorize must carry a non-empty authorization reference")
    if len(payload) > sl.MAX_WRITE_BYTES:
        raise UsageError(
            f"payload of {len(payload)} bytes exceeds the {sl.MAX_WRITE_BYTES}-byte cap"
        )
    if args.expect_current is None and not args.no_expect:
        raise UsageError(
            "--expect-current is required; pass --no-expect only when the "
            "unguarded write is deliberate and disclosed"
        )

    memory = _memory(target)
    before = memory.read(address, len(payload))
    guard: dict[str, Any] = {"guarded": not args.no_expect}
    if args.expect_current is not None:
        expected = parse_hex_bytes(args.expect_current)
        guard["expected_hex"] = expected.hex()
        if len(expected) != len(payload):
            raise UsageError(
                f"--expect-current is {len(expected)} bytes but the payload is "
                f"{len(payload)} bytes"
            )
        if expected != before:
            return _refuse_write(
                target, address, payload, before, args,
                reason="guard_mismatch",
                detail=f"current bytes {before.hex()} != expected {expected.hex()}",
            )

    receipt: dict[str, Any] = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "verb": "poke",
        "authorization": args.authorize,
        "purpose": args.purpose,
        "target": target.to_dict(),
        "address": f"0x{address:08X}",
        "size": len(payload),
        "before_hex": before.hex(),
        "payload_hex": payload.hex(),
        "guard": guard,
        "dry_run": bool(args.dry_run),
        "written": False,
        "verified": False,
        "started_at": ev.now().isoformat(),
    }
    if args.dry_run:
        receipt["note"] = "dry run: no write was issued"
        path = _write_receipt(receipt)
        receipt["receipt_path"] = str(path)
        print(json.dumps(receipt, indent=2))
        return ev.EXIT_OK

    written = memory.write_many(((address, payload),))
    after = memory.read(address, len(payload))
    receipt["written"] = True
    receipt["bytes_written"] = written
    receipt["after_hex"] = after.hex()
    receipt["verified"] = after == payload
    receipt["finished_at"] = ev.now().isoformat()
    path = _write_receipt(receipt)
    receipt["receipt_path"] = str(path)
    print(json.dumps(receipt, indent=2))
    return ev.EXIT_OK if receipt["verified"] else ev.EXIT_TOOL_NEGATIVE


def _refuse_write(
    target: Target, address: int, payload: bytes, before: bytes,
    args: argparse.Namespace, *, reason: str, detail: str,
) -> int:
    receipt = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "verb": "poke",
        "refused": True,
        "reason": reason,
        "detail": detail,
        "authorization": args.authorize,
        "target": target.to_dict(),
        "address": f"0x{address:08X}",
        "before_hex": before.hex(),
        "payload_hex": payload.hex(),
        "written": False,
        "refused_at": ev.now().isoformat(),
    }
    path = _write_receipt(receipt)
    receipt["receipt_path"] = str(path)
    print(json.dumps(receipt, indent=2))
    return ev.EXIT_REFUSAL


def cmd_teleport(args: argparse.Namespace) -> int:
    """The accepted write-assisted relocation from the teleport procedure.

    Writes current and preceding XYZ together in one 24-byte call, never
    auxiliary, to a destination the caller must justify with
    ``--destination-evidence``.  Reads all three triples before and after, then
    settles and reports ``NextLife``.  A nonzero ``NextLife`` after settling is
    reported as tool-negative because it is the observable signature of the
    EXP-20260815-130 reset loop.
    """

    target = resolve_target(args)
    if not args.authorize.strip():
        raise UsageError("--authorize must carry a non-empty authorization reference")
    if not args.destination_evidence.strip():
        raise UsageError(
            "--destination-evidence must cite the evidence that this destination "
            "is already proven walkable (PC Flik teleport procedure)"
        )
    destination = (
        parse_signed_int(args.x), parse_signed_int(args.y), parse_signed_int(args.z)
    )
    memory = _memory(target)

    def triples() -> dict:
        current, preceding, auxiliary = memory.read_many(
            (
                (CURRENT_XYZ_ADDRESS, 12),
                (PRECEDING_XYZ_ADDRESS, 12),
                (AUXILIARY_XYZ_ADDRESS, 12),
            )
        )
        return {
            "current": list(struct.unpack("<iii", current)),
            "preceding": list(struct.unpack("<iii", preceding)),
            "auxiliary": list(struct.unpack("<iii", auxiliary)),
        }

    before_state = _state_sample(memory)
    before_triples = triples()
    # The current and preceding triples are NOT contiguous: current occupies
    # 0x0059D910/14/18 and preceding starts at 0x0059D920, leaving an
    # unidentified dword at 0x0059D91C between them.  The accepted boundary is
    # one 24-byte process_vm_writev, which is expressed as a single call
    # carrying two 12-byte vectors -- not a 24-byte contiguous range, which
    # would overwrite that unknown dword and misalign the second triple.
    triple = struct.pack("<iii", *destination)
    writes = ((CURRENT_XYZ_ADDRESS, triple), (PRECEDING_XYZ_ADDRESS, triple))
    assert sum(len(chunk) for _, chunk in writes) == TELEPORT_WRITE_BYTES

    receipt: dict[str, Any] = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "verb": "teleport",
        "procedure": "Vault/40-Implementation/PC Flik teleport procedure.md",
        "write_assisted": True,
        "authorization": args.authorize,
        "purpose": args.purpose,
        "destination_evidence": args.destination_evidence,
        "target": target.to_dict(),
        "destination": list(destination),
        "written_addresses": [
            f"0x{CURRENT_XYZ_ADDRESS:08X}", f"0x{PRECEDING_XYZ_ADDRESS:08X}"
        ],
        "write_bytes": TELEPORT_WRITE_BYTES,
        "write_vectors": 2,
        "preserved_unknown_dword": f"0x{CURRENT_XYZ_ADDRESS + 12:08X}",
        "auxiliary_written": False,
        "before": {"state": before_state, "triples": before_triples},
        "dry_run": bool(args.dry_run),
        "started_at": ev.now().isoformat(),
    }

    if args.dry_run:
        receipt["note"] = "dry run: no write was issued"
        path = _write_receipt(receipt)
        receipt["receipt_path"] = str(path)
        print(json.dumps(receipt, indent=2))
        return ev.EXIT_OK

    gap_before = memory.read(CURRENT_XYZ_ADDRESS + 12, 4)
    written = memory.write_many(writes)
    readback = triples()
    receipt["unknown_dword_preserved"] = (
        memory.read(CURRENT_XYZ_ADDRESS + 12, 4) == gap_before
    )
    receipt["bytes_written"] = written
    receipt["readback"] = readback

    settle_samples = []
    for index in range(args.settle_samples):
        time.sleep(args.settle_interval_ms / 1000.0)
        settle_samples.append({
            "sample": index,
            "state": _state_sample(memory),
            "triples": triples(),
        })
    receipt["settle"] = settle_samples
    receipt["finished_at"] = ev.now().isoformat()

    final = settle_samples[-1] if settle_samples else {"state": before_state}
    next_life = final["state"]["next_life"]
    positions = [tuple(sample["triples"]["current"]) for sample in settle_samples]
    stable = len(set(positions)) <= 1 if positions else False
    receipt["accepted"] = bool(readback["current"] == list(destination)
                               and next_life == 0)
    receipt["current_stable_across_settle"] = stable
    receipt["next_life_after_settle"] = next_life
    if next_life != 0:
        receipt["caution"] = (
            "nonzero NextLife after settling matches the EXP-20260815-130 reset "
            "loop signature; terminate the owned process group rather than "
            "attempting speculative in-flight repairs"
        )
    path = _write_receipt(receipt)
    receipt["receipt_path"] = str(path)
    print(json.dumps(receipt, indent=2))
    return ev.EXIT_OK if receipt["accepted"] else ev.EXIT_TOOL_NEGATIVE


# --------------------------------------------------------------------------
# Region checkpoints (snapshot / restore)
# --------------------------------------------------------------------------
#
# A snapshot captures curated game-data regions from a *running* process and a
# restore writes them back into the *same* process.  This is a state
# checkpoint, not a true savestate: it moves memory only, so it does not carry
# renderer/GPU state, sound buffers, file positions, thread execution points,
# or anything the kernel and Wine own.  It is deliberately limited to
# regions — by default the single writable .data section, which holds every
# global the project has identified and is neither code nor stack — because
# restoring a running thread's stack or a freed heap pointer would crash the
# game.  Restore refuses a different process by default, because a fresh launch
# has a different heap base and the captured .data pointers would dangle.  The
# durable savestate that survives a relaunch is CRIU, recorded as CAP-011.


def _git_ignored(path: Path) -> bool:
    """True when ``path`` is inside a git-ignored tree (game bytes go there)."""

    try:
        result = subprocess.run(
            ["git", "check-ignore", "-q", str(path)],
            cwd=str(ev.repo_root()), capture_output=True, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


def _snapshot_root(args: argparse.Namespace) -> Path:
    root = ev.repo_root()
    base = Path(args.snapshot_dir) if args.snapshot_dir else root / DEFAULT_SNAPSHOT_DIR
    return base if base.is_absolute() else root / base


def _parse_regions(args: argparse.Namespace) -> list[tuple[str, int, int]]:
    """Return labelled ``(label, start, size)`` regions to checkpoint."""

    regions: list[tuple[str, int, int]] = []
    if not args.no_data:
        regions.append((".data", sl.DATA_SECTION_START, sl.DATA_SECTION_SIZE))
    for spec in args.region or []:
        address, size = parse_read_spec(spec)
        if size > sl.MAX_REGION_BYTES:
            raise UsageError(
                f"region size {size} exceeds the {sl.MAX_REGION_BYTES}-byte cap"
            )
        regions.append((f"0x{address:08X}", address, size))
    if not regions:
        raise UsageError("no regions selected: pass --region or drop --no-data")
    return regions


def _validate_region_mappings(
    memory_pid: int, regions: list[tuple[str, int, int]]
) -> list[dict]:
    """Refuse any region not fully inside one writable private mapping.

    This is the safety gate: a region that straddles a gap, a read-only
    section, a file/device mapping, or a thread stack is refused rather than
    checkpointed.  Stacks are writable+private too, so callers must not select
    them; the default .data region and explicit data ranges are the supported
    inputs.
    """

    maps = sl.read_maps(memory_pid)
    resolved: list[dict] = []
    for label, start, size in regions:
        end = start + size
        covering = sl.mapping_covering(maps, start, end)
        if covering is None:
            raise sl.SessionError(
                "region_unmapped",
                f"{label} [0x{start:08X},0x{end:08X}) is not inside one mapping",
            )
        if not covering.writable:
            raise sl.SessionError(
                "region_not_writable",
                f"{label} lies in a non-writable mapping {covering.perms}",
            )
        if covering.path.endswith((".so", "/dev/dri/card0", "/dev/dri/renderD128")):
            raise sl.SessionError(
                "region_device_backed",
                f"{label} lies in {covering.path!r}, which is not game data",
            )
        resolved.append({
            "label": label,
            "address": f"0x{start:08X}",
            "size": size,
            "mapping": covering.to_dict(),
        })
    return resolved


def _freeze_guard(pid: int, enabled: bool):
    """Context manager that SIGSTOPs the game around an atomic memory op."""

    class _Guard:
        def __enter__(self):
            if enabled:
                sl.freeze(pid)
            return self

        def __exit__(self, *exc):
            if enabled:
                sl.unfreeze(pid)
            return False

    return _Guard()


def cmd_snapshot(args: argparse.Namespace) -> int:
    target = resolve_target(args)
    if not SNAPSHOT_NAME_RE.fullmatch(args.name):
        raise UsageError(f"--name must match {SNAPSHOT_NAME_RE.pattern}")
    regions = _parse_regions(args)
    resolved = _validate_region_mappings(target.pid, regions)

    root = _snapshot_root(args)
    if not _git_ignored(root / "probe"):
        return _fail(
            "snapshot_dir_not_ignored",
            f"{root} is not git-ignored; snapshots contain game bytes and must "
            "not be committable (add it to .gitignore)",
        )
    directory = root / args.name
    if directory.exists():
        return _fail("snapshot_exists", f"{directory} already exists")
    directory.mkdir(parents=True)

    memory = _memory(target)
    level = sl.read_internal_level(memory)
    captured: list[dict] = []
    with _freeze_guard(target.pid, not args.no_freeze):
        for index, (label, start, size) in enumerate(regions):
            payload = memory.read_region(start, size)
            filename = f"region-{index}.bin"
            (directory / filename).write_bytes(payload)
            captured.append({
                "index": index,
                "label": label,
                "address": f"0x{start:08X}",
                "size": size,
                "sha256": hashlib.sha256(payload).hexdigest(),
                "file": filename,
            })

    header = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "kind": "region-state-checkpoint",
        "name": args.name,
        "captured_at": ev.now().isoformat(),
        "exe_sha256": target.proof.exe_sha256,
        "pid": target.pid,
        "process_group": target.process_group,
        "start_ticks": target.start_ticks,
        "session_id": target.session_id,
        "internal_level": level,
        "froze_process": not args.no_freeze,
        "regions": captured,
        "region_mappings": resolved,
        "not_a_savestate": (
            "memory-only; carries no renderer/GPU/sound/thread/kernel state. "
            "Restore is same-process only by default (CAP-011)."
        ),
    }
    (directory / "snapshot.json").write_text(
        json.dumps(header, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "verb": "snapshot",
        "snapshot_dir": str(directory),
        "internal_level": level,
        "regions": captured,
        "total_bytes": sum(item["size"] for item in captured),
        "target": target.to_dict(),
    }, indent=2))
    return ev.EXIT_OK


def _load_snapshot(path: Path) -> tuple[dict, Path]:
    directory = path if path.is_dir() else path.parent
    header_path = directory / "snapshot.json"
    try:
        header = json.loads(header_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise sl.SessionError("snapshot_not_found", str(header_path)) from exc
    except json.JSONDecodeError as exc:
        raise sl.SessionError("snapshot_malformed", f"{header_path}: {exc}") from exc
    if header.get("schema_version") != SNAPSHOT_SCHEMA_VERSION:
        raise sl.SessionError(
            "snapshot_schema",
            f"expected schema {SNAPSHOT_SCHEMA_VERSION}, found {header.get('schema_version')!r}",
        )
    return header, directory


def cmd_restore(args: argparse.Namespace) -> int:
    if not args.authorize.strip():
        raise UsageError("--authorize must carry a non-empty authorization reference")
    header, directory = _load_snapshot(Path(args.snapshot))

    # Verify snapshot integrity before touching the target.
    regions: list[tuple[dict, bytes]] = []
    for item in header.get("regions", []):
        payload = (directory / item["file"]).read_bytes()
        if hashlib.sha256(payload).hexdigest() != item["sha256"]:
            return _fail("snapshot_corrupt", f"region {item['label']} hash mismatch")
        if len(payload) != item["size"]:
            return _fail("snapshot_corrupt", f"region {item['label']} size mismatch")
        regions.append((item, payload))
    if not regions:
        raise UsageError("snapshot has no regions")

    target = resolve_target(args)

    if target.proof.exe_sha256.lower() != str(header.get("exe_sha256", "")).lower():
        return _fail(
            "executable_mismatch",
            f"target exe {target.proof.exe_sha256} != snapshot "
            f"{header.get('exe_sha256')}",
        )

    same_process = (
        target.pid == header.get("pid")
        and target.start_ticks == header.get("start_ticks")
    )
    if not same_process and not args.allow_different_process:
        return _fail(
            "different_process",
            "restore is same-process only by default: the target is not the "
            "process this snapshot was captured from, so its heap base differs "
            "and the captured .data pointers may dangle. Pass "
            "--allow-different-process only when the risk is understood and "
            "disclosed (CAP-011 covers cross-launch savestates separately).",
        )

    memory = _memory(target)
    current_level = sl.read_internal_level(memory)
    level_changed = current_level != header.get("internal_level")
    if level_changed and not args.allow_level_change:
        return _fail(
            "level_changed",
            f"target is on internal level {current_level} but the snapshot was "
            f"captured on {header.get('internal_level')}; restoring .data across "
            "a level change is unsafe. Pass --allow-level-change to override.",
        )

    receipt: dict[str, Any] = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "verb": "restore",
        "authorization": args.authorize,
        "purpose": args.purpose,
        "snapshot_dir": str(directory),
        "snapshot_name": header.get("name"),
        "same_process": same_process,
        "level_changed": level_changed,
        "target": target.to_dict(),
        "internal_level_before": current_level,
        "regions": [item["label"] for item, _ in regions],
        "write_assisted": True,
        "dry_run": bool(args.dry_run),
        "started_at": ev.now().isoformat(),
    }

    if args.dry_run:
        receipt["note"] = "dry run: no write was issued"
        path = _write_restore_receipt(receipt)
        receipt["receipt_path"] = str(path)
        print(json.dumps(receipt, indent=2))
        return ev.EXIT_OK

    # Re-validate the mappings just before writing, so a region that has moved
    # or been unmapped since capture is refused rather than written blindly.
    _validate_region_mappings(
        target.pid, [(item["label"], int(item["address"], 16), item["size"])
                     for item, _ in regions]
    )

    verified: list[dict] = []
    with _freeze_guard(target.pid, not args.no_freeze):
        for item, payload in regions:
            address = int(item["address"], 16)
            memory.write_region(address, payload)
            readback = memory.read_region(address, len(payload))
            verified.append({
                "label": item["label"],
                "address": item["address"],
                "size": item["size"],
                "verified": readback == payload,
            })

    receipt["region_results"] = verified
    receipt["verified"] = all(item["verified"] for item in verified)
    receipt["internal_level_after"] = sl.read_internal_level(memory)
    receipt["finished_at"] = ev.now().isoformat()
    path = _write_restore_receipt(receipt)
    receipt["receipt_path"] = str(path)
    print(json.dumps(receipt, indent=2))
    return ev.EXIT_OK if receipt["verified"] else ev.EXIT_TOOL_NEGATIVE


def _write_restore_receipt(payload: dict, *, root: Path | None = None) -> Path:
    directory = ev.new_run_dir(RESTORE_RUN_PREFIX, root=root)
    path = directory / "receipt.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def capabilities() -> dict:
    return {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "session_lib_version": sl.SESSION_LIB_VERSION,
        "read_verbs": ["peek", "state", "watch", "snapshot"],
        "write_verbs": ["poke", "teleport", "restore"],
        "write_requirements": [
            "explicit --authorize reference recorded in the receipt",
            "--expect-current compare-before-write guard (or a disclosed --no-expect)",
            "post-write readback verification",
            "receipt under dynamic/wine/RUN-POKE-<stamp>/",
            "teleport also requires --destination-evidence and writes "
            "current+preceding only, never auxiliary",
            "restore is same-process only by default, refuses a different "
            "executable hash, refuses a level change, and reads every region "
            "back to verify",
        ],
        "checkpoint": {
            "kind": "region-state-checkpoint",
            "default_region": ".data (0x004C1000-0x00864000)",
            "froze_with_sigstop": True,
            "not_a_savestate": (
                "captures memory only: no renderer/GPU, sound, file position, "
                "thread execution point, or kernel/Wine state. Same-process "
                "restore only; a relaunch has a different heap base."
            ),
            "durable_savestate_path": "CRIU (CAP-011), needs root and is unproven here",
        },
        "limits": {
            "max_ranges_per_call": sl.MAX_MEMORY_RANGES,
            "max_range_bytes": sl.MAX_MEMORY_RANGE_BYTES,
            "max_write_bytes": sl.MAX_WRITE_BYTES,
            "max_region_bytes": sl.MAX_REGION_BYTES,
            "max_watch_samples": MAX_WATCH_SAMPLES,
            "max_watch_duration_s": MAX_WATCH_DURATION_S,
        },
        "formats": list(FORMATS),
        "accepted_executable_sha256": sorted(sl.ACCEPTED_EXECUTABLE_SHA256S),
        "claims_not_made": [
            "engine-frame synchronization",
            "atomicity relative to the game's threads",
            "that a region checkpoint is a full savestate",
            "that any post-write observation is natural gameplay",
        ],
    }


def _add_target_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--pid", type=int, default=None)
    parser.add_argument("--session", default=None,
                        help="session id from game-session.py, or 'current'")
    parser.add_argument("--expected-sha", default=None)
    parser.add_argument("--accept-sha", action="append", default=None,
                        help="widen the accepted executable hash set (disclose it)")
    parser.add_argument("--any-exe-sha", action="store_true",
                        help="accept any executable hash (disclose it)")
    parser.add_argument("--exe-basename", default=ev.DEFAULT_EXE_BASENAME)
    parser.add_argument("--loader-re", default=ev.DEFAULT_LOADER_RE)
    parser.add_argument("--cwd-prefix", default=None)
    parser.add_argument("--pretty", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="game-memory.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--capabilities", action="store_true",
                        help="print the tool contract as JSON and exit")
    sub = parser.add_subparsers(dest="command")

    peek = sub.add_parser("peek", help="read one or more ranges")
    _add_target_flags(peek)
    peek.add_argument("--read", action="append", required=True, metavar="ADDR:SIZE")
    peek.add_argument("--format", choices=FORMATS, default="hex")
    peek.set_defaults(func=cmd_peek)

    state = sub.add_parser("state", help="read the known live state block")
    _add_target_flags(state)
    state.add_argument("--triples", action="store_true",
                       help="also read current/preceding/auxiliary XYZ")
    state.set_defaults(func=cmd_state)

    watch = sub.add_parser("watch", help="sample ranges or state on an interval")
    _add_target_flags(watch)
    watch.add_argument("--read", action="append", default=None, metavar="ADDR:SIZE")
    watch.add_argument("--state", action="store_true")
    watch.add_argument("--format", choices=FORMATS, default="hex")
    watch.add_argument("--interval-ms", type=int, default=50)
    watch.add_argument("--duration-s", type=float, default=10.0)
    watch.add_argument("--until-change", action="store_true")
    watch.add_argument("--max-read-failures", type=int, default=0)
    watch.add_argument("--out", type=Path, default=None,
                       help="JSONL destination (default: stderr)")
    watch.set_defaults(func=cmd_watch)

    poke = sub.add_parser("poke", help="guarded authorized write")
    _add_target_flags(poke)
    poke.add_argument("--addr", required=True)
    poke.add_argument("--bytes", required=True, help="hex payload")
    poke.add_argument("--expect-current", default=None,
                      help="hex bytes that must currently be present")
    poke.add_argument("--no-expect", action="store_true",
                      help="disclosed unguarded write")
    poke.add_argument("--authorize", required=True,
                      help="authorization reference recorded in the receipt")
    poke.add_argument("--purpose", default="")
    poke.add_argument("--dry-run", action="store_true")
    poke.set_defaults(func=cmd_poke)

    tele = sub.add_parser("teleport", help="accepted current+preceding relocation")
    _add_target_flags(tele)
    tele.add_argument("--x", required=True)
    tele.add_argument("--y", required=True)
    tele.add_argument("--z", required=True)
    tele.add_argument("--authorize", required=True)
    tele.add_argument("--destination-evidence", required=True,
                      help="evidence that the destination is already proven walkable")
    tele.add_argument("--purpose", default="")
    tele.add_argument("--settle-samples", type=int, default=5)
    tele.add_argument("--settle-interval-ms", type=int, default=50)
    tele.add_argument("--dry-run", action="store_true")
    tele.set_defaults(func=cmd_teleport)

    snap = sub.add_parser(
        "snapshot", help="capture game-data regions to a same-process checkpoint"
    )
    _add_target_flags(snap)
    snap.add_argument("--name", required=True, help="checkpoint name")
    snap.add_argument("--region", action="append", default=None, metavar="ADDR:SIZE",
                      help="additional region to capture (repeatable)")
    snap.add_argument("--no-data", action="store_true",
                      help="do not capture the default .data section")
    snap.add_argument("--snapshot-dir", default=None,
                      help=f"checkpoint root (default {DEFAULT_SNAPSHOT_DIR}, must be git-ignored)")
    snap.add_argument("--no-freeze", action="store_true",
                      help="do not SIGSTOP the game during capture (may tear)")
    snap.set_defaults(func=cmd_snapshot)

    restore = sub.add_parser(
        "restore", help="write a checkpoint back into the same process"
    )
    _add_target_flags(restore)
    restore.add_argument("--snapshot", required=True,
                         help="checkpoint directory or its snapshot.json")
    restore.add_argument("--authorize", required=True,
                         help="authorization reference recorded in the receipt")
    restore.add_argument("--purpose", default="")
    restore.add_argument("--allow-different-process", action="store_true",
                         help="disclosed: restore into a process other than the "
                              "one captured (heap base differs; pointers may dangle)")
    restore.add_argument("--allow-level-change", action="store_true",
                         help="disclosed: restore across a level change")
    restore.add_argument("--no-freeze", action="store_true",
                         help="do not SIGSTOP the game during the write (may tear)")
    restore.add_argument("--dry-run", action="store_true")
    restore.set_defaults(func=cmd_restore)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.capabilities:
        print(json.dumps(capabilities(), indent=2))
        return ev.EXIT_OK
    if not getattr(args, "command", None):
        parser.print_usage(sys.stderr)
        return ev.EXIT_USAGE
    try:
        return args.func(args)
    except UsageError as exc:
        print(f"{TOOL}: {exc}", file=sys.stderr)
        return ev.EXIT_USAGE
    except ev.OwnershipError as exc:
        return _fail(exc.reason, exc.detail)
    except sl.SessionError as exc:
        return _fail(exc.reason, exc.detail)
    except FileExistsError as exc:
        return _fail("receipt_collision", str(exc))


if __name__ == "__main__":
    sys.exit(main())
