"""Size-preserving translation of canonical PC kind-0x101 barrier strips.

EXP-20260904-004 validates one four-segment translation in the live game.
Full-block metadata translation is covered by synthetic/corpus regressions;
this is not an arbitrary mesh encoder or a guarantee of gameplay at any site.
"""
from __future__ import annotations

import struct

from .terrain_all import TerrainAll, TerrainFormatError
from .terrain_barriers import BarrierPayload


def translate_payload(raw: bytes, dx: int, dz: int) -> bytes:
    """Translate in stored units (32 world units), retaining every other byte."""
    if type(dx) is not int or type(dz) is not int:
        raise TerrainFormatError("barrier translation requires integer stored units")
    strip = BarrierPayload.parse(raw)
    if not all(strip.bounds_cover_points(block) for block in strip.blocks):
        raise TerrainFormatError("source barrier bounds do not cover their points")
    output = bytearray(strip.raw)

    def put(offset: int, value: int, *, coordinate: bool = False) -> None:
        if not -0x80000000 <= value <= 0x7fffffff:
            raise TerrainFormatError("translated barrier value overflows int32")
        if coordinate and not -0x80000000 <= value * 32 <= 0x7fffffff:
            raise TerrainFormatError("translated barrier world coordinate overflows int32")
        struct.pack_into("<i", output, offset, value)

    for point in strip.points:
        put(point.offset, point.x + dx, coordinate=True)
        put(point.offset + 8, point.z + dz, coordinate=True)
    for block in strip.blocks:
        if block.bounds is not None:
            # Minima move; spans, loose padding and sentinel tails do not.
            put(block.metadata_offset, block.bounds[0] + dx)
            put(block.metadata_offset + 24, block.bounds[2] + dz)
    result = bytes(output)
    parsed = BarrierPayload.parse(result)
    if not all(parsed.bounds_cover_points(block) for block in parsed.blocks):
        raise TerrainFormatError("translated bounds do not cover their points")
    return result


def translate_terrain_barrier(raw: bytes, index: int, dx: int, dz: int) -> bytes:
    """Replace only one payload in an otherwise byte-identical terrain file."""
    if not isinstance(raw, (bytes, bytearray, memoryview)):
        raise TerrainFormatError("terrain source must be bytes")
    terrain = TerrainAll.parse(bytes(raw))
    strip = BarrierPayload.from_terrain(terrain, index)
    moved = translate_payload(strip.raw, dx, dz)
    return terrain.data[:strip.offset] + moved + terrain.data[strip.offset + len(strip.raw):]
