#!/usr/bin/env python3
"""Offline instruction experiments for EXP-20260904-001.

Execute hash-checked retail x86 instructions in Unicorn with synthetic data.
This does not start the executable, Wine, a game, or a live debugger. No
decompiler code is reimplemented here. The movement probe executes its full
callee path; the descriptor probe explicitly excludes rendering after cb5d.
Output contains measurements and hashes, never executable bytes or RAM dumps.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path
import struct

import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BINARY = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe"
BINARY_SHA256 = "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
DESCRIPTORS = 0x007F4590
DESCRIPTOR_SIZE = 0x30
DESCRIPTOR_COUNT = 700
BOUNDARY = 0x007F3D30
OBJECTS = 0x0059D9C0
STACK = 0x01000000
FIXTURE = 0x02000000
STOP = 0x03000000


class ProbeError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProbeError(message)


def load_text(path: Path) -> tuple[int, bytes]:
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == BINARY_SHA256, "retail executable SHA-256 mismatch")
    pe = pefile.PE(data=raw, fast_load=True)
    require(pe.FILE_HEADER.Machine == 0x14C, "expected i386 executable")
    require(pe.OPTIONAL_HEADER.ImageBase == 0x400000, "unexpected image base")
    section = next(section for section in pe.sections if section.Name.rstrip(b"\0") == b".text")
    code = raw[section.PointerToRawData:section.PointerToRawData + section.Misc_VirtualSize]
    require(len(code) == section.Misc_VirtualSize, "truncated text section")
    return pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress, code


def machine(text: tuple[int, bytes]) -> Uc:
    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    cpu.mem_map(0x00400000, 0x00470000)
    cpu.mem_write(text[0], text[1])
    cpu.mem_map(STACK, 0x10000)
    cpu.mem_map(FIXTURE, 0x10000)
    cpu.mem_map(STOP, 0x1000)
    cpu.reg_write(UC_X86_REG_ESP, STACK + 0x8000)
    return cpu


def put(cpu: Uc, address: int, fmt: str, *values: int) -> None:
    cpu.mem_write(address, struct.pack("<" + fmt, *values))


def get(cpu: Uc, address: int, fmt: str) -> tuple[int, ...]:
    return struct.unpack("<" + fmt, cpu.mem_read(address, struct.calcsize("<" + fmt)))


def invoke(cpu: Uc, entry: int, args: tuple[int, ...]) -> dict:
    """Run an ordinary cdecl function to a sentinel return, without stubs."""
    stack_pointer = cpu.reg_read(UC_X86_REG_ESP)
    put(cpu, stack_pointer, "I" * (len(args) + 1), STOP, *args)
    visits: Counter = Counter()

    def trace(uc, address, size, _):
        require(0x401000 <= address < 0x4BF765, f"execution escaped text at {address:#x}")
        visits[address] += 1

    cpu.hook_add(UC_HOOK_CODE, trace)
    cpu.emu_start(entry, STOP, timeout=1_000_000, count=20_000)
    require(cpu.reg_read(UC_X86_REG_EIP) == STOP, "instruction/time bound reached before return")
    return {
        "return_eax": cpu.reg_read(UC_X86_REG_EAX),
        "instruction_count": sum(visits.values()),
        "entered": [f"0x{address:08x}" for address in (0x4AA4D0, 0x4A9860, 0x4A9420, 0x4A95E0) if visits[address]],
        "instruction_visit_counts_sha256": hashlib.sha256(json.dumps(sorted(visits.items())).encode()).hexdigest(),
    }


def movement_case(text: tuple[int, bytes], *, normal_axis: str, candidate: bool,
                  start: int, delta: int, tangent: int = 512,
                  reverse_winding: bool = False, special_contact: bool = False) -> dict:
    """A plane through origin with edges of 100 encoded = 3200 position units.

    +X uses edges +Z then +Y; +Z uses +Y then +X, matching the executable's
    directed edge tests (not an assumed cross-product convention). Candidate collection is
    supplied as a synthetic precondition; the original response and triangle
    tests execute unmodified. Coordinates/deltas are in the routine's units.
    """
    require(normal_axis in ("x", "z"), "unsupported fixture plane")
    cpu = machine(text)
    position, velocity, residual, cell = (FIXTURE + value for value in (0, 0x20, 0x40, 0x100))
    pos = [start, tangent, 512] if normal_axis == "x" else [512, tangent, start]
    move = [delta, 0, 0] if normal_axis == "x" else [0, 0, delta]
    put(cpu, position, "4i", *pos, 0)
    put(cpu, velocity, "4i", *move, 0)
    put(cpu, residual, "4h", *move, 0)
    words = [0] * 16
    words[0 if normal_axis == "x" else 2] = 0x4000
    if normal_axis == "x":
        words[8], words[10] = 100, 100
    else:
        words[7], words[9] = 100, 100
    if reverse_winding:
        words[6:9], words[9:12] = words[9:12], words[6:9]
    put(cpu, cell, "16h", *words)
    put(cpu, 0x007FC8D4, "i", int(candidate))
    put(cpu, 0x007F3F50, "I", cell)
    put(cpu, 0x007F2680, "h", 0)
    put(cpu, 0x007FC8E8, "i", 0)  # separate line-segment list deliberately empty
    contact = 0x007F3EA8 if special_contact else 0x007F3D68
    stats = invoke(cpu, 0x004AA4D0, (residual, position, velocity, contact))
    return {
        "axis": normal_axis, "candidate_count": int(candidate), "start": pos,
        "reverse_winding": reverse_winding,
        "contact_pointer": f"0x{contact:08x}",
        "requested_delta": move, "unconstrained_endpoint": [p + d for p, d in zip(pos, move)],
        "position_after": list(get(cpu, position, "3i")),
        "velocity_after": list(get(cpu, velocity, "3i")),
        "residual_after": list(get(cpu, residual, "3h")), **stats,
    }


DESCRIPTOR_CASES = ("create", "same_tag", "flag_clear", "missing_template", "empty_tag", "type_zero", "unloaded", "contact_other", "contact_zero")


def descriptor_case(text: tuple[int, bytes], boundary: int, case: str) -> dict:
    require(type(boundary) is int and 1 <= boundary <= DESCRIPTOR_COUNT - 32, "fixture boundary outside 1..668")
    require(case in DESCRIPTOR_CASES, "unknown descriptor fixture")
    cpu = machine(text)
    # Deterministic synthetic bytes make unintended stores visible, even when
    # they write zero. Template 0 is outside the reserved range in these cases.
    initial = bytes((i * 37 + 11) % 256 for i in range(DESCRIPTOR_COUNT * DESCRIPTOR_SIZE))
    cpu.mem_write(DESCRIPTORS, initial)
    put(cpu, BOUNDARY, "i", boundary)
    template_base = (100, 200, 300)
    put(cpu, DESCRIPTORS, "3i", *template_base)
    put(cpu, DESCRIPTORS + 0x10, "I", FIXTURE + 0x800)
    put(cpu, DESCRIPTORS + 0x14, "i", 132)
    put(cpu, DESCRIPTORS + 0x1C, "i", 364)
    put(cpu, DESCRIPTORS + 0x24, "2i", 640, 960)
    put(cpu, 0x005B1A80, "I", FIXTURE + 0x400)  # type-1 object table
    put(cpu, FIXTURE + 0x400, "h", 0 if case == "unloaded" else 1)
    put(cpu, 0x007F29EA, "h", -1 if case == "missing_template" else 0)
    put(cpu, 0x0059D992, "h", 0 if case == "contact_zero" else 1)
    put(cpu, 0x007F3D68, "i", boundary + (31 if case == "contact_other" else 0))
    for slot in range(20):
        item = OBJECTS + slot * 0x30
        put(cpu, item, "h", 0 if case == "type_zero" else 1)
        put(cpu, item + 8, "3i", 1000 + slot, -2000 - slot, 3000 + slot)
        put(cpu, item + 0x2E, "H", 0 if case in ("flag_clear", "empty_tag") else 2)
        tag = 104 if case == "same_tag" else (0 if case == "empty_tag" else 7)
        put(cpu, DESCRIPTORS + (boundary + slot) * 0x30 + 0x2C, "H", tag)
    before = bytes(cpu.mem_read(DESCRIPTORS, len(initial)))
    writes: list[tuple[int, int, int]] = []
    visited_slots: list[int] = []

    def write_trace(uc, access, address, size, value, _):
        if address < DESCRIPTORS + len(initial) and address + size > DESCRIPTORS:
            writes.append((uc.reg_read(UC_X86_REG_EIP), address, size))

    def control(uc, address, size, _):
        if address == 0x44CA24:
            visited_slots.append(get(uc, uc.reg_read(UC_X86_REG_ESP) + 0x2C, "i")[0])
        elif address == 0x44CB5D:
            # Explicit slice boundary: exclude rendering, use the ORIGINAL
            # loop epilogue to advance the slot and position pointer.
            uc.reg_write(UC_X86_REG_EIP, 0x44D1F3)
        require(0x44CA19 <= address <= 0x44CB5D or 0x44D1F3 <= address <= 0x44D20B,
                f"descriptor slice escaped at {address:#x}")

    cpu.hook_add(UC_HOOK_MEM_WRITE, write_trace)
    cpu.hook_add(UC_HOOK_CODE, control)
    cpu.emu_start(0x44CA19, 0x44D20B, timeout=1_000_000, count=5000)
    require(cpu.reg_read(UC_X86_REG_EIP) == 0x44D20B, "descriptor slice did not finish")
    require(visited_slots == list(range(20)), "original loop did not visit exactly slots 0..19")
    after = bytes(cpu.mem_read(DESCRIPTORS, len(initial)))
    expected = bytearray(before)
    creates = case in ("create", "contact_other", "contact_zero")
    clears = case in ("flag_clear", "missing_template")
    for slot in range(20):
        offset = (boundary + slot) * 0x30
        if creates:
            struct.pack_into("<3i", expected, offset, 1000 + slot, -2000 - slot, 3000 + slot)
            struct.pack_into("<I", expected, offset + 0x10, FIXTURE + 0x800)
            struct.pack_into("<i", expected, offset + 0x14, 1032 + slot)
            struct.pack_into("<i", expected, offset + 0x1C, 3064 + slot)
            struct.pack_into("<2i", expected, offset + 0x24, 640, 960)
            struct.pack_into("<H", expected, offset + 0x2C, 104)
        elif clears:
            struct.pack_into("<H", expected, offset + 0x2C, 0)
    require(after == expected, f"descriptor fixture {case} produced unexpected bytes")
    expected_count = 180 if creates else (20 if clears else 0)
    require(len(writes) == expected_count, "unexpected descriptor store count")
    require(all(DESCRIPTORS + boundary * 0x30 <= address and
                address + size <= DESCRIPTORS + (boundary + 20) * 0x30
                for _, address, size in writes), "store outside reserved object slots")
    return {
        "boundary_N": boundary, "case": case, "visited_slots": visited_slots,
        "descriptor_store_count": len(writes),
        "written_indices": sorted({(address - DESCRIPTORS) // 0x30 for _, address, _ in writes}),
        "store_pcs": sorted({f"0x{pc:08x}" for pc, _, _ in writes}),
        "prefix_below_N_unchanged": after[:boundary * 0x30] == before[:boundary * 0x30],
        "remaining_reserved_slots_unchanged": after[(boundary + 20) * 0x30:] == before[(boundary + 20) * 0x30:],
        "contact_flag_after": get(cpu, 0x0059D992, "h")[0],
        "table_after_sha256": hashlib.sha256(after).hexdigest(),
    }


def probe(path: Path) -> dict:
    text = load_text(path)
    movement = []
    for axis in ("x", "z"):
        for label, candidate, start, delta, tangent in (
            ("crossing", True, 1024, -2048, 512),
            ("no_candidate", False, 1024, -2048, 512),
            ("moving_away", True, 1024, 2048, 512),
            ("outside_triangle", True, 1024, -2048, 6400),
        ):
            movement.append({"case": label, **movement_case(text, normal_axis=axis,
                            candidate=candidate, start=start, delta=delta, tangent=tangent)})
        movement.append({"case": "reversed_winding", **movement_case(text, normal_axis=axis,
                        candidate=True, start=1024, delta=-2048, reverse_winding=True)})
        movement.append({"case": "special_contact", **movement_case(text, normal_axis=axis,
                        candidate=True, start=1024, delta=-2048, special_contact=True)})
    return {
        "experiment": "EXP-20260904-001", "binary_sha256": BINARY_SHA256,
        "probe_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "binary_path": str(path.resolve().relative_to(ROOT)),
        "text_sha256": hashlib.sha256(text[1]).hexdigest(),
        "unicorn_version": importlib.metadata.version("unicorn"),
        "scope": "original-x86-instructions-with-synthetic-inputs-no-game-runtime",
        "memory_initialization": "retail .text only; all other mapped bytes zero-filled before synthetic fixture seeding",
        "descriptor_excluded_code": "initial transform call before 0x44ca19; rendering [0x44cb5d,0x44d1f3); function prologue/return",
        "movement_excluded_code": "caller 0x4ab1a0 and candidate collection; zero synthetic line-segment count",
        "descriptor_cases": [descriptor_case(text, boundary, case) for boundary in (1, 64, 668) for case in DESCRIPTOR_CASES],
        "movement_cases": movement,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, default=DEFAULT_BINARY)
    parser.add_argument("--output", type=Path, help="optional fresh JSON file under work/copies")
    args = parser.parse_args()
    try:
        result = probe(args.binary)
        output = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            target = args.output.resolve()
            require(target.is_relative_to((ROOT / "work/copies").resolve()), "output must be under work/copies")
            with target.open("x") as stream:
                stream.write(output)
            print(json.dumps({"path": str(target.relative_to(ROOT)), "sha256": hashlib.sha256(output.encode()).hexdigest(),
                              "byte_count": len(output.encode()), "descriptor_cases": len(result["descriptor_cases"]),
                              "movement_cases": len(result["movement_cases"])}))
        else:
            print(output, end="")
    except (OSError, ValueError) as exc:
        parser.exit(2, f"terrain collision probe rejected: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
