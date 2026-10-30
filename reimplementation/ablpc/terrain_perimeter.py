"""Bounded orthogonal PC barrier loops, EXP-20260906-006.

Uses the banked full-block bounds and short-block sentinel grammar. This is not a general mesh
writer or a claim that the barrier supplies visible foliage.
"""

import struct

from .terrain_all import TerrainAll, TerrainFormatError
from .terrain_barriers import BarrierPayload, MAGIC, SENTINEL


def closed_outline(points):
    points = tuple(tuple(p) for p in points)
    if not 4 <= len(points) <= 37 or any(len(p) != 2 for p in points):
        raise TerrainFormatError("need 3..36 segments and X/Z pairs")
    if points[0] != points[-1] or len(set(points[:-1])) != len(points) - 1:
        raise TerrainFormatError("need one explicitly closed, nonrepeating loop")
    for point in points:
        if any(type(v) is not int or not -0x80000000 <= v * 32 <= 0x7FFFFFFF for v in point):
            raise TerrainFormatError("stored coordinate overflows PC world dword")
    segments = tuple(zip(points, points[1:]))
    for a, b in segments:
        if (a[0] == b[0]) == (a[1] == b[1]):
            raise TerrainFormatError("require nonzero orthogonal segments")
    for i, (a, b) in enumerate(segments):
        for j, (c, d) in enumerate(segments):
            if j <= i or j == i + 1 or (i == 0 and j == len(segments) - 1):
                continue
            if (max(min(a[0], b[0]), min(c[0], d[0])) <= min(max(a[0], b[0]), max(c[0], d[0]))
                    and max(min(a[1], b[1]), min(c[1], d[1])) <= min(max(a[1], b[1]), max(c[1], d[1]))):
                raise TerrainFormatError("nonadjacent perimeter segments intersect")
    area2 = sum(a[0] * b[1] - b[0] * a[1] for a, b in segments)
    if area2 == 0:
        raise TerrainFormatError("zero-area perimeter")
    return points


def reshape_short_loop(template: bytes, points) -> bytes:
    """Preserve allocation, unknown header/middle/trailing bytes of a donor."""
    strip = BarrierPayload.parse(template)
    points = closed_outline(points)
    if len(points) > 16:
        raise TerrainFormatError("short loop requires at most 15 segments")
    if len(points) > len(strip.points):
        raise TerrainFormatError("perimeter exceeds donor point allocation")
    if not all(strip.bounds_cover_points(block) for block in strip.blocks):
        raise TerrainFormatError("donor block bounds exclude points")
    result = bytearray(strip.raw)
    struct.pack_into("<H", result, 4, len(points) - 1)
    for index, (x, z) in enumerate(points):
        struct.pack_into("<i", result, 8 + 12 * index, x)
        struct.pack_into("<i", result, 16 + 12 * index, z)
    # Only this first middle word is consumed as short-block metadata.
    struct.pack_into("<i", result, 12, SENTINEL)
    BarrierPayload.parse(result)
    return bytes(result)


def reshape_loop(template: bytes, points, *, allocation_template=None) -> bytes:
    """Author at most the original donor's point allocation (EXP-018).

    Earlier short-loop builds retain unused original point slots as a trailer.
    Reclaim those only when an explicit original allocation proves the suffix
    is still exact. Unknown header, unused middle words and tail bytes survive.
    """
    strip = BarrierPayload.parse(template)
    points = closed_outline(points)
    if not all(strip.bounds_cover_points(b) for b in strip.blocks):
        raise TerrainFormatError('donor block bounds exclude points')
    capacity = len(strip.points)
    if allocation_template is not None:
        original = BarrierPayload.parse(allocation_template)
        end = 8+12*capacity
        if (len(original.raw) != len(strip.raw) or original.unknown_06 != strip.unknown_06
                or capacity > len(original.points) or strip.raw[end:] != original.raw[end:]
                or not all(original.bounds_cover_points(b) for b in original.blocks)):
            raise TerrainFormatError('unused donor point allocation is not the exact original suffix')
        capacity = len(original.points)
    if len(points) > capacity:
        raise TerrainFormatError('perimeter exceeds donor point allocation')
    result = bytearray(strip.raw)
    struct.pack_into('<H', result, 4, len(points)-1)
    for i, (x,z) in enumerate(points):
        struct.pack_into('<i', result, 8+12*i, x)
        struct.pack_into('<i', result, 16+12*i, z)
    for first in range(0, len(points)-1, 16):
        if len(points)-1-first < 16:
            struct.pack_into('<i', result, 12+12*first, SENTINEL)
        else:
            block = points[first:first+17]
            xs,zs = zip(*block)
            bounds = (min(xs), max(xs)-min(xs), min(zs), max(zs)-min(zs))
            for j,value in enumerate(bounds):
                struct.pack_into('<i', result, 12+12*(first+j), value)
    checked = BarrierPayload.parse(result)
    if not all(checked.bounds_cover_points(b) for b in checked.blocks):
        raise TerrainFormatError('authored bounds exclude perimeter points')
    return bytes(result)


def install_perimeter(data: bytes, template: bytes, source_index: int, points):
    if not isinstance(data, bytes):
        raise TerrainFormatError("terrain input must be immutable bytes")
    terrain = TerrainAll.parse(data)
    if type(source_index) is not int or not 0 <= source_index < len(terrain.records):
        raise TerrainFormatError("invalid perimeter source")
    record = terrain.records[source_index]
    if record.field_10 != 0x101:
        raise TerrainFormatError("perimeter needs the established 0x101 source kind")
    offset, size = record.payload_offset, record.payload_size
    current = data[offset:offset + size]
    if len(template) != size or current[:4] != b"\0" * 4 or current[4:] != template[4:]:
        raise TerrainFormatError("target is not the exact unlinked donor control")
    replacement = reshape_short_loop(template, points)
    if struct.unpack_from("<I", replacement)[0] != MAGIC:
        raise TerrainFormatError("donor lost registration magic")
    return data[:offset] + replacement + data[offset + size:]
