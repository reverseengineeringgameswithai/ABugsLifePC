#!/usr/bin/env python3
"""EXP-20260904-002: offline retail terrain loading and movement experiments.

The full original loader and movement coordinator run without stubs. A named
initializer slice builds bounds/buckets and clears templates; filename setup
and collectible initialization are excluded. Inputs are hash-pinned work copies.
Only Unicorn memory changes. No game, OS, debugger or renderer is launched.
Reports contain locators, counts and measurements, never source assets/dumps.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import struct
import sys

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESI, UC_X86_REG_ESP

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))
from ablpc.terrain_all import TerrainAll

_spec = importlib.util.spec_from_file_location("collision_instructions", ROOT / "scripts/terrain-collision-probe.py")
p = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p)

SOURCE_ROOT = p.DEFAULT_BINARY.parent
SOURCES = {
    "level01": ("CD/LEVEL01/TERRAIN.ALL", "62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868"),
    "level03": ("CD/LEVEL03/TERRAIN.ALL", "b878c378c924fbdb45e450f4314808fdd3506f8685da2c3f255b7e316f4a2d9c"),
    "plantter": ("CD/BITS/PLANTTER.ALL", "0a0cf7fa9e110eef8e2112760dcbefaa433b391ca613a3d673ee0327767eb468"),
}
SOURCE_BASES = (0x04000000, 0x05000000)
IMAGE = (0x00400000, 0x00470000)
POSITION, VELOCITY, FLAGS = p.FIXTURE + 0x100, p.FIXTURE + 0x120, p.FIXTURE + 0x140
CASES = ("retail", "without_record87", "without_triangles", "without_segments", "moving_away")


def load_source(key: str, root: Path = SOURCE_ROOT) -> TerrainAll:
    relative, expected = SOURCES[key]
    raw = (root / relative).read_bytes()
    p.require(hashlib.sha256(raw).hexdigest() == expected, f"{key} SHA-256 mismatch")
    return TerrainAll.parse(raw)


def census(terrain: TerrainAll) -> dict:
    """Count stored low-kind cells; keep other payload kinds opaque."""
    cells = [cell for record in terrain.records
             if record.field_10 in (6, 7, 8) and record.payload_size and record.field_46 != 1
             for group in terrain.collision_payload(record.index).groups for cell in group.cells]
    return {
        "size": len(terrain.data), "sha256": hashlib.sha256(terrain.data).hexdigest(),
        "directory_offset": terrain.directory_offset, "source_records": len(terrain.records),
        "kind_counts": dict(sorted(Counter(r.field_10 for r in terrain.records).items())),
        "clone_records": sum(r.field_46 == 1 for r in terrain.records),
        "stored_cells": len(cells),
        "vertical_normal_cells": sum(c.words[1] == 0 and bool(c.words[0] or c.words[2]) for c in cells),
        "lateral_dominant_normal_cells": sum(max(abs(c.words[0]), abs(c.words[2])) > abs(c.words[1]) for c in cells),
        "minimum_absolute_normal_y": min((abs(c.words[1]) for c in cells), default=None),
        "opaque_high_kinds": [
            {"source_record": r.index, "kind": r.field_10, "payload_offset": r.payload_offset,
             "payload_size": r.payload_size}
            for r in terrain.records if r.field_10 >= 0x100
        ],
    }


class RetailProbe:
    def __init__(self, level: str, text: tuple[int, bytes]):
        p.require(level in ("level01", "level03"), "unsupported retail level")
        self.level = level
        self.sources = (load_source(level), load_source("plantter"))
        self.cpu = p.machine(text)
        self.cpu.mem_map(p.STACK + 0x10000, 0x20000)
        for base, source in zip(SOURCE_BASES, self.sources, strict=True):
            p.require(len(source.data) < 0x100000, "source exceeds mapped capacity")
            self.cpu.mem_map(base, 0x100000)
            self.cpu.mem_write(base, source.data)
        # Original preloaded-buffer branches avoid the disk loader naturally.
        p.put(self.cpu, 0x007F3D60, "I", SOURCE_BASES[0])
        p.put(self.cpu, 0x007F2D2C, "I", SOURCE_BASES[1])
        # Reproduce 004a895e..004a8989's zero count/buckets and -1 template map.
        # All other image globals start zero, not from a live game snapshot.
        self.cpu.mem_write(0x007F29A8, b"\xff" * 128)
        p.put(self.cpu, p.FIXTURE, "I", p.FIXTURE + 0x1000)
        self.loader = self.call(0x004A8410, (0, 0, p.FIXTURE))
        self.loaded_count = self.loader["eax_at_stop"]
        p.require(0 < self.loaded_count <= 668, "loaded descriptors exceed reserved capacity")
        self.loaded_tags = self.tags()
        self.template_map = self.templates()
        # Start just after the loader call, including its original add esp,12.
        # Allocate the original local-frame space explicitly; no guessed args.
        self.cpu.reg_write(UC_X86_REG_ESP, p.STACK + 0x10000 - 12)
        self.initializer = self.run(0x004A89F8, 0x004A908F)
        self.initialized_tags = self.tags()
        self.boundary = p.get(self.cpu, p.BOUNDARY, "i")[0]
        self.total = p.get(self.cpu, 0x007F2D28, "i")[0]
        p.require(self.total <= 700 and self.total == self.boundary + 32, "invalid descriptor reservation")
        self.buckets = self.bucket_members()
        # Internal reset image only; never written to disk or included in reports.
        self.baseline = bytes(self.cpu.mem_read(*IMAGE))
        self.baseline_context = self.cpu.context_save()
        self.scratch_baseline = {
            p.STACK: bytes(self.cpu.mem_read(p.STACK, 0x30000)),
            p.FIXTURE: bytes(self.cpu.mem_read(p.FIXTURE, 0x10000)),
        }
        self.loaded_source_hashes = self.source_hashes()

    def source_hashes(self) -> list[str]:
        return [hashlib.sha256(self.cpu.mem_read(base, len(source.data))).hexdigest()
                for base, source in zip(SOURCE_BASES, self.sources, strict=True)]

    def locate(self, pointer: int) -> dict:
        for base, source, key in zip(SOURCE_BASES, self.sources, (self.level, "plantter"), strict=True):
            offset = pointer - base
            if 0 <= offset < len(source.data):
                for record in source.records:
                    if record.payload_offset <= offset < record.payload_offset + record.payload_size:
                        return {"source": key, "source_record": record.index, "file_offset": offset}
        raise p.ProbeError(f"pointer is not inside a source payload: {pointer:#x}")

    def run(self, entry: int, stop: int, observe=None, *, instruction_limit=3_000_000) -> dict:
        visits = Counter()
        ordered = hashlib.sha256()

        def trace(cpu, address, size, _):
            p.require(0x00401000 <= address < 0x004BF765, f"execution escaped .text: {address:#x}")
            visits[address] += 1
            ordered.update(struct.pack("<I", address))
            if observe is not None:
                observe(cpu, address)

        hook = self.cpu.hook_add(UC_HOOK_CODE, trace)
        try:
            self.cpu.emu_start(entry, stop, timeout=10_000_000, count=instruction_limit)
            p.require(self.cpu.reg_read(UC_X86_REG_EIP) == stop, "instruction/time bound reached")
        finally:
            self.cpu.hook_del(hook)
        entries = (0x004A8410, 0x004B0240, 0x004AB1A0, 0x004AA4D0,
                   0x004A9860, 0x004A9420, 0x004A95E0, 0x00464CA0,
                   0x004AAE30, 0x004A9BA0)
        return {
            "entry": f"0x{entry:08x}", "stop": f"0x{stop:08x}",
            "eax_at_stop": self.cpu.reg_read(UC_X86_REG_EAX),
            "instruction_count": sum(visits.values()), "ordered_pc_sha256": ordered.hexdigest(),
            "entry_visits": {f"0x{addr:08x}": visits[addr] for addr in entries if visits[addr]},
        }

    def call(self, entry: int, args: tuple[int, ...], observe=None) -> dict:
        stack = p.STACK + 0x20000
        self.cpu.reg_write(UC_X86_REG_ESP, stack)
        p.put(self.cpu, stack, "I" * (1 + len(args)), p.STOP, *args)
        return self.run(entry, p.STOP, observe)

    def tags(self) -> list[int]:
        return [p.get(self.cpu, p.DESCRIPTORS + i * 48 + 44, "H")[0] for i in range(700)]

    def templates(self) -> list[dict]:
        result = []
        for object_type in range(1, 32):
            index = p.get(self.cpu, 0x007F29E8 + object_type * 2, "h")[0]
            if index >= 0:
                p.require(index < self.loaded_count, "template index outside loaded records")
                pointer = p.get(self.cpu, p.DESCRIPTORS + index * 48 + 16, "I")[0]
                result.append({"object_type": object_type, "descriptor_index": index, **self.locate(pointer)})
        return result

    def bucket_members(self) -> list[int]:
        count = p.get(self.cpu, 0x007F3D58, "i")[0]
        p.require(0 <= count <= 256, "bucket count exceeds table capacity")
        members = []
        for i in range(count):
            offset, size = p.get(self.cpu, 0x007F1280 + i * 20, "2h")
            p.require(0 <= offset <= 2048 and 0 <= size <= 700 and offset + size <= 2048,
                      "bucket member span outside table")
            indices = p.get(self.cpu, 0x007FC8F0 + offset * 2, "h" * size)
            p.require(all(0 <= j < 700 for j in indices), "invalid bucket descriptor index")
            members.extend(indices)
        return members

    def initialization_report(self) -> dict:
        return {
            "level": self.level, "loaded_descriptor_count": self.loaded_count,
            "loader": self.loader, "initializer_slice": self.initializer,
            "loaded_tag_counts": dict(sorted(Counter(self.loaded_tags).items())),
            "initialized_tag_counts": dict(sorted(Counter(self.initialized_tags).items())),
            "template_map": self.template_map, "boundary_N": self.boundary,
            "reserved_end_exclusive": self.total,
            "cleared_loaded_indices": [i for i in range(self.loaded_count)
                                       if self.loaded_tags[i] and not self.initialized_tags[i]],
            "bucket_count": p.get(self.cpu, 0x007F3D58, "i")[0],
            "bucket_members": len(self.buckets), "unique_bucket_members": len(set(self.buckets)),
            "bucket_members_cover_loaded_records": sorted(self.buckets) == list(range(self.loaded_count)),
        }

    def movement(self, family: str, case: str, *, y: int = 0, axis: int = 0) -> dict:
        p.require(self.level == "level01", "movement fixtures are Level01 only")
        p.require(family in ("triangle", "segment") and case in CASES, "unknown movement fixture")
        p.require(type(axis) is int and axis in (0, 2), "unsupported movement axis")
        p.require(type(y) is int and y in (-200000, 0, 200000), "unsupported segment height")
        p.require(not (family == "segment" and case == "without_record87"), "irrelevant segment control")
        self.cpu.mem_write(IMAGE[0], self.baseline)
        for base, data in self.scratch_baseline.items():
            self.cpu.mem_write(base, data)
        self.cpu.context_restore(self.baseline_context)
        if case == "without_record87":
            p.put(self.cpu, p.DESCRIPTORS + 87 * 48 + 44, "H", 0)
        elif case == "without_triangles":
            for i in range(self.loaded_count):
                p.put(self.cpu, p.DESCRIPTORS + i * 48 + 44, "H", 0)
        elif case == "without_segments":
            p.put(self.cpu, 0x007F3D3C, "I", 0)

        if family == "triangle":
            # Integer centroid of source87/group988/cell1000, offset outward.
            cell = self.sources[0].collision_payload(87).groups[0].cells[0]
            p.require(cell.offset == 1000, "fixture cell locator changed")
            w = cell.words
            base = self.sources[0].records[87].world_base
            start = [(w[3+i]*3 + w[6+i] + w[9+i])*32//3 + base[i] for i in range(3)]
            start[1] += 0xC80  # coordinator subtracts this actor-height offset
            sign = 1 if w[axis] > 0 else -1
            start[axis] += sign * 1024
            delta = [0, 0, 0]
            delta[axis] = -sign * 2048
        else:
            # Midpoint of source179's first XZ segment, 1024 units on +Z side.
            record = self.sources[0].records[179]
            first = struct.unpack_from("<3i", self.sources[0].data, record.payload_offset + 8)
            second = struct.unpack_from("<3i", self.sources[0].data, record.payload_offset + 20)
            start = [(first[0]+second[0])*16, y, (first[2]+second[2])*16 + 1024]
            delta = [0, 0, -2048]
        if case == "moving_away":
            delta = [-d for d in delta]
        p.put(self.cpu, POSITION, "4i", *start, 0)
        p.put(self.cpu, VELOCITY, "4i", *delta, 0)
        p.put(self.cpu, FLAGS, "I", 0)  # nongrounded entry, contact slot0
        best_triangles, best_segments = [], []

        def observe(cpu, address):
            if address == 0x004AA715:
                best_triangles.append(self.locate(cpu.reg_read(UC_X86_REG_ESI)))
            elif address == 0x004A9787:
                pointer = cpu.reg_read(UC_X86_REG_ESI) - 8
                p.require(0x007F2A28 <= pointer < 0x007F2BA8, "segment outside candidate array")
                best_segments.append((pointer - 0x007F2A28) // 24)

        stats = self.call(0x004AB1A0, (POSITION, VELOCITY, FLAGS, 0), observe)
        triangle_count = p.get(self.cpu, 0x007FC8D4, "i")[0]
        segment_vertices = p.get(self.cpu, 0x007FC8E8, "i")[0]
        p.require(0 <= triangle_count <= 400, "triangle candidate capacity exceeded")
        p.require(0 <= segment_vertices <= 32 and segment_vertices % 2 == 0, "invalid segment count")
        candidates = [
            {"descriptor_index": p.get(self.cpu, 0x007F2680 + i * 2, "h")[0],
             **self.locate(p.get(self.cpu, 0x007F3F50 + i * 4, "I")[0])}
            for i in range(triangle_count)
        ]
        # Bind copied XZ pairs to source locators; the middle dwords are opaque
        # metadata in this record family, not asserted world Y coordinates.
        segment_locators = []
        for i in range(segment_vertices // 2):
            v = p.get(self.cpu, 0x007F2A28 + i * 24, "6i")
            matches = []
            for base, source in zip(SOURCE_BASES, self.sources, strict=True):
                for record in source.records:
                    if record.field_10 != 0x101:
                        continue
                    for off in range(record.payload_offset + 8, record.payload_offset + record.payload_size - 23, 12):
                        pair = struct.unpack_from("<6i", source.data, off)
                        if pair == v:
                            matches.append(self.locate(base + off))
            p.require(bool(matches), "segment candidate lacks source provenance")
            segment_locators.append(matches)
        endpoint = [a+b for a, b in zip(start, delta)]
        after = list(p.get(self.cpu, POSITION, "3i"))
        p.require(self.source_hashes() == self.loaded_source_hashes, "movement modified emulated source payloads")
        return {
            "family": family, "case": case, "axis": axis if family == "triangle" else 2,
            "start": start, "requested_delta": delta, "unconstrained_endpoint": endpoint,
            "position_after": after, "velocity_after": list(p.get(self.cpu, VELOCITY, "3i")),
            "flags_after": list(p.get(self.cpu, FLAGS, "2B")), "changed_endpoint": after != endpoint,
            "triangle_candidates": candidates, "segment_candidate_pairs": segment_vertices // 2,
            "segment_source_matches": segment_locators,
            "best_triangle_updates": best_triangles, "best_segment_updates": best_segments,
            "execution": stats,
        }


def report() -> dict:
    text = p.load_text(p.DEFAULT_BINARY)
    probes = [RetailProbe(level, text) for level in ("level01", "level03")]
    level01 = probes[0]
    result = {
        "experiment": "EXP-20260904-002", "evidence_kind": "offline-original-instructions",
        "binary_sha256": p.BINARY_SHA256, "text_sha256": hashlib.sha256(text[1]).hexdigest(),
        "unicorn_version": importlib.metadata.version("unicorn"),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "helper_sha256": hashlib.sha256(Path(p.__file__).read_bytes()).hexdigest(),
        "terrain_parser_sha256": hashlib.sha256((ROOT / "reimplementation/ablpc/terrain_all.py").read_bytes()).hexdigest(),
        "scope": {
            "loader": "full 004a8410 with original preloaded-buffer branches; no stubs",
            "initializer": "004a89f8..004a908f exclusive; excludes filename setup and collectible init",
            "movement": "full 004ab1a0 and callees; slot0, nongrounded entry, synthetic position/velocity",
            "globals": "zero-filled image except original .text and explicit fixture state",
            "controls": "only private emulated memory; source files unchanged",
            "live_gameplay_claim": False,
        },
        "sources": {key: {"path": str((SOURCE_ROOT / SOURCES[key][0]).relative_to(ROOT)), **census(load_source(key))}
                    for key in SOURCES},
        "initialization": [probe.initialization_report() for probe in probes],
        "movement": [level01.movement("triangle", case, axis=axis) for axis in (0, 2) for case in CASES]
        + [level01.movement("segment", case, y=y) for y in (-200000, 0, 200000)
           for case in CASES if case != "without_record87"],
    }
    return result


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(report(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
