"""Decorative, downward-only ramp skirts using established PC mesh fields.

EXP-20260906-002: no collision or new material semantics. Texture U runs
down each 512-unit band; V retains the ramp's existing longitudinal tiling.
The bands follow the top edge, so tiling adds no new top-edge vertices.
"""

from __future__ import annotations

from fractions import Fraction
import math
import struct

from .terrain_all import TerrainAll
from .terrain_height import CellWords
from .terrain_texture_tiling import MAX_FACES, MAX_VERTICES, cross


def _integer(value, low, high, name):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in [{low}, {high}]")
    return value


def _vector(value, low, high, name):
    if not isinstance(value, (tuple, list)) or len(value) != 3:
        raise ValueError(f"{name} must contain three integers")
    return tuple(_integer(v, low, high, name) for v in value)


def ground_boundary_spans(data, *, source_index, x, z_start, z_end):
    """Intersect original source triangles with one finite stored-X side line.

    Heights are rational geometric planes from the established cell normal
    and origin fields, not a replacement for the fixed-point PC resolver.
    Used only to choose a buried decorative base. Unknown cell fields remain
    untouched. Coverage must be complete; unsupported source variants reject.
    """
    if type(data) is not bytes:
        raise ValueError("terrain must be immutable bytes")
    _integer(source_index, 0, 65535, "source index")
    for name, value in (("x", x), ("z_start", z_start), ("z_end", z_end)):
        _integer(value, -2147483648, 2147483647, name)
    if z_start >= z_end:
        raise ValueError("empty boundary")
    parsed = TerrainAll.parse(data)
    if source_index >= len(parsed.records):
        raise ValueError("source index outside directory")
    record = parsed.records[source_index]
    if record.field_10 != 6 or record.field_44 != -1 or record.field_46 != 0:
        raise ValueError("only a unique active local height source is supported")
    bx, by, bz = record.component_x, record.component_y, record.component_z
    spans = []
    for group in parsed.collision_payload(source_index).groups:
        for cell in group.cells:
            fields = CellWords.parse(cell.raw)
            nx, ny, nz = fields.slope_x, fields.divisor, fields.slope_z
            x0, y0, z0 = fields.x0, fields.h0, fields.z0
            dx1, dz1, dx2, dz2 = fields.dx1, fields.dz1, fields.dx2, fields.dz2
            if not ny:
                continue
            points = ((bx + x0, bz + z0), (bx + x0 + dx1, bz + z0 + dz1),
                      (bx + x0 + dx2, bz + z0 + dz2))
            if dx1 * dz2 == dx2 * dz1:
                continue
            intersections = []
            for a, b in zip(points, points[1:] + points[:1]):
                if a[0] == b[0]:
                    if a[0] == x:
                        intersections.extend((Fraction(a[1]), Fraction(b[1])))
                elif min(a[0], b[0]) <= x <= max(a[0], b[0]):
                    intersections.append(a[1] + Fraction(x - a[0], b[0] - a[0]) * (b[1] - a[1]))
            if not intersections:
                continue
            lo, hi = max(Fraction(z_start), min(intersections)), min(Fraction(z_end), max(intersections))
            if lo >= hi:
                continue
            heights = tuple(Fraction(by + y0) - Fraction(nx * (x - bx - x0), ny)
                            - Fraction(nz, ny) * (z - bz - z0) for z in (lo, hi))
            spans.append({"cell_offset": cell.offset, "z_start": lo, "z_end": hi,
                          "height_start": heights[0], "height_end": heights[1]})
    end = Fraction(z_start)
    for span in sorted(spans, key=lambda item: item["z_start"]):
        if span["z_start"] > end:
            raise ValueError("original triangle footprint has an uncovered interval")
        end = max(end, span["z_end"])
    if end < z_end:
        raise ValueError("original triangle footprint does not cover the boundary")
    return spans


def buried_base(spans, *, burial=256):
    """Choose a flat base below every supplied plane endpoint, Y down."""
    _integer(burial, 1, 4096, "burial")
    if not spans:
        raise ValueError("ground spans are required")
    return math.ceil(max(span[key] for span in spans for key in ("height_start", "height_end"))) + burial


def side_face_mesh(left, right, *, origin, bottom_y, vertex_suffix,
                   top_channels=(114, 82, 60), bottom_channels=(98, 70, 50),
                   tile_size=512, anchor_z=13000):
    """Return a checked triangle stream and metadata for two outward skirts.

    Edge points are copied from the existing render mesh, in increasing Z.
    They must already include every longitudinal tile boundary. Keeping each
    top segment intact avoids new quantized vertices or colour edits on the
    playable surface. No faces extend above that surface, and no barrier is
    implied by this render-only geometry.
    """
    origin = _vector(origin, -2147483648, 2147483647, "origin")
    top_channels = _vector(top_channels, 0, 255, "top channels")
    bottom_channels = _vector(bottom_channels, 0, 255, "bottom channels")
    _integer(bottom_y, -2147483648, 2147483647, "bottom y")
    _integer(tile_size, 128, 2048, "tile size")
    _integer(anchor_z, -2147483648, 2147483647, "anchor z")
    if type(vertex_suffix) is not bytes or len(vertex_suffix) != 6:
        raise ValueError("a complete immutable six-byte vertex suffix is required")
    edges = []
    for side in (left, right):
        if not isinstance(side, (tuple, list)) or not 2 <= len(side) <= MAX_VERTICES:
            raise ValueError("each side needs a bounded vertex sequence")
        points = tuple(_vector(p, -2147483648, 2147483647, "edge point") for p in side)
        if len({p[0] for p in points}) != 1:
            raise ValueError("side edges must have constant X")
        if any(p[1] >= bottom_y for p in points):
            raise ValueError("the base must be strictly below both top edges")
        for a, b in zip(points, points[1:]):
            boundary = anchor_z + ((a[2] - anchor_z) // tile_size + 1) * tile_size
            if not a[2] < b[2] <= boundary:
                raise ValueError("edge order or existing longitudinal tile boundary is invalid")
        for point in points + ((points[0][0], bottom_y, points[0][2]),):
            for value, offset in zip(point, origin):
                _integer(value - offset, -32768, 32767, "local coordinate")
        edges.append(points)
    if edges[0][0][0] >= edges[1][0][0]:
        raise ValueError("left must be west of right")
    if (edges[0][0][2], edges[0][-1][2]) != (edges[1][0][2], edges[1][-1][2]):
        raise ValueError("side extents must agree")

    vertices, lookup, faces = [], {}, []

    def vertex(top, depth):
        y = min(top[1] + depth, bottom_y)
        fraction = Fraction(y - top[1], bottom_y - top[1])
        channels = bytes(round(a + fraction * (b - a)) for a, b in zip(top_channels, bottom_channels))
        local = (top[0] - origin[0], y - origin[1], top[2] - origin[2])
        raw = struct.pack("<3h", *local) + vertex_suffix[:2] + channels + vertex_suffix[5:]
        if raw not in lookup:
            if len(vertices) >= MAX_VERTICES:
                raise ValueError("wall vertices exceed uint16 byte-offset capacity")
            lookup[raw] = len(vertices)
            vertices.append(raw)
        return lookup[raw], (top[0], y, top[2])

    side_counts = []
    for side_index, edge in enumerate(edges):
        before = len(faces)
        for a, b in zip(edge, edge[1:]):
            phase = anchor_z + ((a[2] - anchor_z) // tile_size) * tile_size
            bands = (max(bottom_y - a[1], bottom_y - b[1]) + tile_size - 1) // tile_size
            for band in range(bands):
                corners, words = [], []
                for top, depth in ((a, band * tile_size), (b, band * tile_size),
                                   (b, (band + 1) * tile_size), (a, (band + 1) * tile_size)):
                    index, point = vertex(top, depth)
                    within = max(0, min(tile_size, point[1] - top[1] - band * tile_size))
                    u = 127 - round(Fraction(63 * within, tile_size))
                    v = 192 + round(Fraction(63 * (point[2] - phase), tile_size))
                    corners.append((index, point))
                    words.append(u | (v << 8))
                for triangle in ((0, 1, 2), (0, 2, 3)):
                    normal = cross(*(corners[k][1] for k in triangle))
                    if normal == (0, 0, 0):
                        continue
                    order = triangle if (normal[0] < 0) == (side_index == 0) else tuple(reversed(triangle))
                    faces.append((tuple(corners[k][0] for k in order), tuple(words[k] for k in order)))
                    if len(faces) > MAX_FACES:
                        raise ValueError("wall face count exceeds the bounded mesh grammar")
        side_counts.append(len(faces) - before)
    stream = struct.pack("<i", len(vertices)) + b"".join(vertices)
    stream += struct.pack("<Hh", 0x61, len(faces))
    stream += b"".join(struct.pack("<6H", *(index * 12 for index in indices), *words) for indices, words in faces)
    stream += b"\xff\xff"
    return stream, {"vertex_count": len(vertices), "triangle_count": len(faces),
                    "triangles_by_side": side_counts, "top_edges": edges,
                    "bottom_y": bottom_y, "tile_size": tile_size, "anchor_z": anchor_z,
                    "uv_region": {"u": [64, 127], "v": [192, 255]},
                    "top_channels": top_channels, "bottom_channels": bottom_channels,
                    "unknown_vertex_fields": "copied +6/+7/+11; existing vertices unchanged",
                    "tiling": "height bands follow the exact top polyline; no inserted top vertices",
                    "collision": "not authored; decorative below-floor faces only"}
