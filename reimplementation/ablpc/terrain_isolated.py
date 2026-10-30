"""Bounded PC-only landscape isolation, EXP-20260906-005.

Deactivate active traversal, not archaeological bytes: directory identities,
templates, unused mesh vertices, unknown fields and file sizes are preserved.
Evidence: collision loader 004A8410, initializer 004A8950; scene dispatch
004498F0/00448D70; initial placement 0043E6B0 and table 004DC7E8.
"""

from __future__ import annotations

import hashlib
import struct
from collections.abc import Mapping, Sequence

from .level_dat import LevelDat
from .terrain_all import TerrainAll
from .terrain_floor_patch import mesh_groups


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def checked(data: bytes, offset: int, size: int) -> bytes:
    if not isinstance(data, bytes):
        raise ValueError("input must be immutable bytes")
    if type(offset) is not int or type(size) is not int or offset < 0 or size < 0:
        raise ValueError("invalid span")
    if offset > len(data) or size > len(data) - offset:
        raise ValueError("span outside input")
    return data[offset:offset + size]


def replace_spans(data: bytes, changes: Sequence[tuple[int, bytes, bytes]]) -> bytes:
    """Validate all compare-before-write guards and overlaps before mutation."""
    checked(data, 0, 0)
    end = 0
    for offset, expected, replacement in sorted(changes):
        if not isinstance(expected, bytes) or not isinstance(replacement, bytes):
            raise ValueError("replacement spans must be bytes")
        if not expected or len(expected) != len(replacement):
            raise ValueError("replacement must be nonempty and size preserving")
        if checked(data, offset, len(expected)) != expected:
            raise ValueError("compare-before-write mismatch")
        if offset < end:
            raise ValueError("overlapping edits")
        end = offset + len(expected)
    out = bytearray(data)
    for offset, expected, replacement in changes:
        out[offset:offset + len(expected)] = replacement
    return bytes(out)


def isolate_collision(
    data: bytes, keep: Mapping[int, Sequence[int]]
) -> tuple[bytes, dict]:
    """Keep exact selected groups; empty other templates; unlink high streams.

    Do not zero descriptor kinds: their counted slots reserve runtime template
    identities. Clones continue to refer to the now-empty original templates.
    """
    checked(data, 0, 4)
    terrain = TerrainAll.parse(data)
    if any(type(i) is not int or i < 0 or i >= len(terrain.records) for i in keep):
        raise ValueError("invalid source index")
    changes = []
    records = []
    for record in terrain.records:
        start, size = record.payload_offset, record.payload_size
        checked(data, start, size)
        selected = tuple(keep.get(record.index, ()))
        if record.field_46 == 1:
            if selected:
                raise ValueError("cannot retain groups through a clone")
            records.append({"source": record.index, "action": "preserve clone identity"})
            continue
        if record.field_10 in (6, 7, 8):
            groups = {g.offset: g for g in terrain.collision_payload(record.index).groups}
            if any(type(i) is not int or i not in groups for i in selected):
                raise ValueError("selected offset is not an active group")
            if len(set(selected)) != len(selected) or tuple(sorted(selected)) != selected:
                raise ValueError("selected groups must be ordered and unique")
            chunks = []
            mapping = []
            cursor = start
            for offset in selected:
                group = groups[offset]
                length = 12 + 32 * len(group.cells)
                if offset + length > start + size:
                    raise ValueError("group exceeds its payload")
                chunks.append(checked(data, offset, length))
                mapping.append({"old_group": offset, "new_group": cursor,
                                "cells": len(group.cells), "bytes": length})
                cursor += length
            replacement = b"".join(chunks) + b"\xff\xff"
            if len(replacement) > size:
                raise ValueError("retained groups exceed payload allocation")
            changes.append((start, checked(data, start, len(replacement)), replacement))
            records.append({"source": record.index, "action": "retain" if selected else "empty",
                            "payload_offset": start, "groups": mapping,
                            "terminator": cursor})
        elif record.field_10 in (0x101, 0x104):
            if selected or size < 4 or checked(data, start, 4) != b"\x78\x56\x34\x12":
                raise ValueError("unexpected linked-stream header")
            changes.append((start, data[start:start + 4], b"\0" * 4))
            records.append({"source": record.index, "action": "unlink",
                            "kind": record.field_10, "marker_offset": start})
        else:
            raise ValueError("unestablished collision kind")
    result = replace_spans(data, changes)
    return result, {"before_sha256": digest(data), "after_sha256": digest(result),
                    "bytes": len(data), "directory_offset": terrain.directory_offset,
                    "records": records}


def muted_scene_flags(flags: int) -> int:
    """Retain loader layout bits, select no draw case in both PC dispatchers."""
    if type(flags) is not int or not 0 <= flags < 0x8000:
        raise ValueError("not a live scene flag word")
    if flags & 0xBFEF not in (1, 2, 3, 4, 9, 10, 12, 0x41, 0x42, 0x43, 0x44, 0x49, 0x4A, 0x4C):
        raise ValueError("unestablished scene dispatch kind")
    return flags & ~7


def isolate_render(data: bytes, *, record_index: int, first_group: int) -> tuple[bytes, dict]:
    checked(data, 0, 4)
    dat = LevelDat.parse(data)
    if type(record_index) is not int or record_index < 0:
        raise ValueError("invalid scene index")
    ref = dat.static_mesh_reference("primary", record_index)
    groups, end = mesh_groups(data, ref)
    if type(first_group) is not int or not 0 < first_group < len(groups):
        raise ValueError("need a proper authored command suffix")
    start = groups[0]["offset"]
    authored = checked(data, groups[first_group]["offset"], end + 2 - groups[first_group]["offset"])
    if authored[-2:] != b"\xff\xff":
        raise ValueError("missing command terminator")
    changes = [(start, checked(data, start, len(authored)), authored)]
    muted = []
    for section, records in (("primary", dat.primary_records), ("secondary", dat.secondary_records)):
        for record in records:
            if section == "primary" and record.index == record_index:
                continue
            flags = muted_scene_flags(record.flags)
            changes.append((record.offset + 14, struct.pack("<H", record.flags), struct.pack("<H", flags)))
            muted.append({"section": section, "index": record.index, "offset": record.offset + 14,
                          "before": record.flags, "after": flags})
    result = replace_spans(data, changes)
    return result, {"before_sha256": digest(data), "after_sha256": digest(result), "bytes": len(data),
                    "retained_scene": record_index, "geometry_offset": ref.geometry_offset,
                    "retained_vertices_including_unreferenced": ref.payload.vertex_count,
                    "original_faces_removed": sum(len(g["faces"]) for g in groups[:first_group]),
                    "authored_faces": sum(len(g["faces"]) for g in groups[first_group:]),
                    "command_start": start, "new_terminator": start + len(authored) - 2,
                    "authored_commands_sha256": digest(authored), "muted_scenes": muted}


def pe_file_offset(data: bytes, address: int, size: int) -> int:
    """Translate a bounded PE32 VA through one file-backed section."""
    if checked(data, 0, 2) != b"MZ":
        raise ValueError("not a DOS image")
    pe = struct.unpack("<I", checked(data, 0x3C, 4))[0]
    if checked(data, pe, 4) != b"PE\0\0":
        raise ValueError("not a PE image")
    coff = checked(data, pe + 4, 20)
    machine, count = struct.unpack_from("<HH", coff)
    opt_size = struct.unpack_from("<H", coff, 16)[0]
    opt = checked(data, pe + 24, opt_size)
    if machine != 0x14C or count == 0 or len(opt) < 32 or struct.unpack_from("<H", opt)[0] != 0x10B:
        raise ValueError("not a bounded x86 PE32 image")
    base = struct.unpack_from("<I", opt, 28)[0]
    if type(address) is not int or type(size) is not int or address < base or size <= 0:
        raise ValueError("invalid virtual span")
    rva = address - base
    matches = []
    for i in range(count):
        section = checked(data, pe + 24 + opt_size + i * 40, 40)
        va, raw_size, raw = struct.unpack_from("<III", section, 12)
        if va <= rva and rva - va + size <= raw_size:
            offset = raw + rva - va
            checked(data, offset, size)
            matches.append(offset)
    if len(matches) != 1:
        raise ValueError("VA must have one file-backed section")
    return matches[0]


def platform_spawn(data: bytes, *, x: int, z: int) -> tuple[bytes, dict]:
    if any(type(v) is not int or not -0x80000000 <= v <= 0x7FFFFFFF for v in (x, z)):
        raise ValueError("spawn coordinates must be signed world dwords")
    address = 0x004DC7E8 + 12  # Level 1, XYZ-like table actually stores X/Z/heading.
    offset = pe_file_offset(data, address, 12)
    expected = struct.pack("<iii", 197108, 492895, 3505)
    if checked(data, offset, 12) != expected:
        raise ValueError("not the established Level 1 start row")
    out = replace_spans(data, [(offset, expected[:8], struct.pack("<ii", x, z))])
    return out, {"before_sha256": digest(data), "after_sha256": digest(out),
                 "address": hex(address), "file_offset": offset, "changed_span": [offset, offset + 8],
                 "original_x_z_heading": [197108, 492895, 3505], "x_z_heading": [x, z, 3505],
                 "height": "original 004AC460 query through 0043E6B0; not patched"}
