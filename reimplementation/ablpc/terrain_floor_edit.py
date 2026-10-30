"""Rigid Y translation of one non-template PC kind-6 collision group.

EXP-20260904-005 tests six Level01 floor cells. This bounded operation preserves
normals and relative bounds; it does not deform triangles or stitch group edges.
"""
from __future__ import annotations

import struct

from .terrain_all import TerrainAll, TerrainFormatError


def translate_floor_group(raw: bytes, index: int, group_index: int, dy: int) -> bytes:
    """Move each cell origin by ``dy`` stored units (32 world units).

Reject clones/templates so the caller cannot inadvertently move other instances.
Only the signed h0 at cell+8 changes. X/Z admission bounds, relative Y bounds,
edge vectors, normals, directory entries and opaque bytes remain unchanged.
"""
    if not isinstance(raw, (bytes, bytearray, memoryview)):
        raise TerrainFormatError("terrain source must be bytes")
    if any(type(v) is not int for v in (index, group_index, dy)):
        raise TerrainFormatError("floor indices and translation must be integers")
    terrain = TerrainAll.parse(bytes(raw))
    if not 0 <= index < len(terrain.records):
        raise TerrainFormatError("floor source index out of range")
    record = terrain.records[index]
    if record.field_10 != 6:
        raise TerrainFormatError("floor translation requires kind 6")
    if record.field_44 != -1 or record.field_46 != 0:
        raise TerrainFormatError("floor translation requires a non-template, non-clone source")
    groups = terrain.collision_payload(index).groups
    if not 0 <= group_index < len(groups) or not groups[group_index].cells:
        raise TerrainFormatError("floor group index is absent or empty")
    output = bytearray(terrain.data)
    for cell in groups[group_index].cells:
        if cell.words[1] >= 0:
            raise TerrainFormatError("group contains a cell without an upward floor normal")
        height = cell.words[4] + dy
        if not -32768 <= height <= 32767:
            raise TerrainFormatError("translated floor origin overflows int16")
        # Edge endpoints and the relative admission window participate in signed
        # 32-bit world arithmetic in the original consumer; do not permit wrap.
        y_min, y_span = struct.unpack_from("<bB", cell.raw, 0x1c)
        for value in (height, height + cell.words[7], height + cell.words[10],
                      height + y_min * 64, height + (y_min + y_span) * 64):
            if not -0x80000000 <= (record.component_y + value) * 32 <= 0x7fffffff:
                raise TerrainFormatError("translated floor world Y overflows int32")
        struct.pack_into("<h", output, cell.offset + 8, height)
    return bytes(output)
