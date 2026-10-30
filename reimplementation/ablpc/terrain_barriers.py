"""Lossless reader for PC terrain kind-0x101 X/Z barrier strips.

EXP-20260904-003: the original collector at 004ab60f..004ab73a consumes
segments between adjacent points, with bounds in the middle dwords of the
first four points of each full 16-segment block. A short final block uses an
INT32_MIN sentinel. This is a reader for the observed canonical layout, not
a collision solver or writer. Unknown header, middle and trailing bytes stay
available. Source bytes (before the loader replaces the magic with a link)
are required.
"""
from __future__ import annotations

from dataclasses import dataclass
import struct

from .terrain_all import TerrainAll, TerrainFormatError

MAGIC = 0x12345678
SENTINEL = -0x80000000
POINT_SIZE = 12
BLOCK_SEGMENTS = 16


@dataclass(frozen=True)
class BarrierPoint:
    offset: int
    x: int
    middle_dword: int
    z: int
    raw: bytes


@dataclass(frozen=True)
class BarrierBlock:
    first_segment: int
    segment_count: int
    metadata_offset: int
    # (minimum X, X span, minimum Z, Z span), in stored coordinate units.
    bounds: tuple[int, int, int, int] | None


@dataclass(frozen=True)
class BarrierPayload:
    offset: int
    segment_count: int
    unknown_06: int
    points: tuple[BarrierPoint, ...]
    blocks: tuple[BarrierBlock, ...]
    trailer: bytes
    raw: bytes

    @classmethod
    def from_terrain(cls, terrain: TerrainAll, index: int) -> "BarrierPayload":
        if type(index) is not int or not 0 <= index < len(terrain.records):
            raise TerrainFormatError("barrier source-record index outside directory")
        record = terrain.records[index]
        if record.field_10 != 0x101:
            raise TerrainFormatError("barrier reader requires source kind 0x101")
        start = record.payload_offset
        return cls.parse(terrain.data[start:start + record.payload_size], offset=start)

    @classmethod
    def parse(cls, raw: bytes, *, offset: int = 0) -> "BarrierPayload":
        if not isinstance(raw, (bytes, bytearray, memoryview)):
            raise TerrainFormatError("barrier payload must be bytes")
        raw = bytes(raw)
        if type(offset) is not int or offset < 0:
            raise TerrainFormatError("invalid barrier file offset")
        if len(raw) < 8:
            raise TerrainFormatError("truncated barrier header")
        magic, count, unknown = struct.unpack_from("<IHH", raw)
        if magic != MAGIC:
            raise TerrainFormatError("barrier source magic mismatch (runtime links are not source bytes)")
        end = 8 + (count + 1) * POINT_SIZE
        if end > len(raw):
            raise TerrainFormatError("barrier point count overruns payload")
        points = tuple(
            BarrierPoint(offset + pos, *struct.unpack_from("<3i", raw, pos), raw[pos:pos + POINT_SIZE])
            for pos in range(8, end, POINT_SIZE)
        )
        blocks = []
        for first in range(0, count, BLOCK_SEGMENTS):
            size = min(BLOCK_SEGMENTS, count - first)
            metadata_offset = points[first].offset + 4
            if size < BLOCK_SEGMENTS:
                if points[first].middle_dword != SENTINEL:
                    raise TerrainFormatError("short final barrier block lacks sentinel; original would scan 16 segments")
                bounds = None
            else:
                # Early sentinels cause the original to scan all remaining
                # segments, then visit later blocks again. Reject that variant;
                # every full block in the examined retail corpus uses bounds.
                if points[first].middle_dword == SENTINEL:
                    raise TerrainFormatError("sentinel in full barrier block is outside observed canonical layout")
                bounds = tuple(points[first + j].middle_dword for j in range(4))
                if bounds[1] < 0 or bounds[3] < 0:
                    raise TerrainFormatError("negative barrier block span outside supported layout")
            blocks.append(BarrierBlock(first, size, metadata_offset, bounds))
        return cls(offset, count, unknown, points, tuple(blocks), raw[end:], raw)

    def bounds_cover_points(self, block: BarrierBlock) -> bool:
        """Report containment, not tightness; retail bounds can be loose."""
        if block not in self.blocks:
            raise TerrainFormatError("block does not belong to this barrier payload")
        if block.bounds is None:
            return True
        x, width, z, depth = block.bounds
        return all(x <= point.x <= x + width and z <= point.z <= z + depth
                   for point in self.points[block.first_segment:block.first_segment + block.segment_count + 1])
