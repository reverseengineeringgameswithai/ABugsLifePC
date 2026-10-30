"""A bounded, appearance-only candidate for the EXP-004 authored walls.

Keep offset-named fields: FUN_0045a7f0 consumes vertex +8..+10 as three
colour channels, but the final live appearance is a separate acceptance gate.
"""

import hashlib
import struct

SOURCE_SHA256 = "54d1ae4d96a4d926b806584cc669e791c3f6565688ec4aa491a987b0c2f56aab"
GEOMETRY_OFFSET = 113136
SOURCE_SIZE = 1526
CAPACITY = 2234


def decode(data):
    """Read exactly one bounded tag-0x60 quad group and its terminator."""
    if not isinstance(data, bytes) or len(data) < 10:
        raise ValueError("Expected a complete immutable mesh stream")
    count = struct.unpack_from("<i", data)[0]
    if count <= 0 or count > (len(data) - 10) // 12:
        raise ValueError("Impossible vertex count")
    group = 4 + count * 12
    tag, faces = struct.unpack_from("<2H", data, group)
    if tag != 0x60 or faces <= 0:
        raise ValueError("Only the banked nonempty tag-0x60 quad group is supported")
    end = group + 4 + faces * 16
    if end + 2 != len(data) or data[end:] != b"\xff\xff":
        raise ValueError("Truncated, extra, or unterminated primitive data")
    vertices = [data[4 + i * 12:4 + (i + 1) * 12] for i in range(count)]
    records = []
    for index in range(faces):
        start = group + 4 + index * 16
        refs = struct.unpack_from("<4H", data, start)
        if any(ref % 12 or ref >= count * 12 for ref in refs):
            raise ValueError("Misaligned or out-of-range vertex reference")
        records.append((tuple(ref // 12 for ref in refs), data[start + 8:start + 16]))
    return vertices, records


def shade_quad_stream(data, numerator=3, denominator=5):
    """Darken axis-aligned vertical faces without changing other faces."""
    if (type(numerator) is not int or type(denominator) is not int
            or denominator <= 0 or not 0 <= numerator <= denominator):
        raise ValueError("Expected an integer darkening ratio between zero and one")
    vertices, records = decode(data)
    original_count = len(vertices)
    walls = []
    wall_users, other_users = set(), set()
    for refs, _ in records:
        points = [struct.unpack_from("<3h", vertices[index]) for index in refs]
        wall = (len({point[1] for point in points}) > 1
                and (len({point[0] for point in points}) == 1
                     or len({point[2] for point in points}) == 1))
        walls.append(wall)
        (wall_users if wall else other_users).update(refs)
    if not wall_users:
        raise ValueError("No axis-aligned vertical walls in the bounded stream")
    mapping = {}
    for index in sorted(wall_users):
        vertex = vertices[index]
        channels = bytes(value * numerator // denominator for value in vertex[8:11])
        shaded = vertex[:8] + channels + vertex[11:]
        if index in other_users:
            mapping[index] = len(vertices)
            vertices.append(shaded)
        else:
            mapping[index] = index
            vertices[index] = shaded
    if (len(vertices) - 1) * 12 > 65535:
        raise ValueError("Expanded vertex offsets exceed uint16")
    output = bytearray(struct.pack("<i", len(vertices)) + b"".join(vertices))
    output.extend(struct.pack("<2H", 0x60, len(records)))
    for wall, (refs, fields) in zip(walls, records):
        new_refs = tuple(mapping[index] if wall else index for index in refs)
        output.extend(struct.pack("<4H", *(index * 12 for index in new_refs)))
        output.extend(fields)
    output.extend(b"\xff\xff")
    return bytes(output), {
        "vertices_before": original_count,
        "vertices_after": len(vertices),
        "wall_faces": sum(walls),
        "unchanged_appearance_faces": len(walls) - sum(walls),
        "wall_vertex_sources": sorted(wall_users),
        "duplicated_boundary_vertices": sorted(wall_users & other_users),
        "wall_vertex_remapping": mapping,
        "field_08_09_0a_scale": [numerator, denominator],
        "preserved_vertex_fields": ["component_00", "component_02", "component_04", "field_06", "field_0b"],
    }


def shade_level_dat(data):
    """Apply only to the exact EXP-004 DAT, inside its known mesh allocation."""
    if not isinstance(data, bytes) or hashlib.sha256(data).hexdigest() != SOURCE_SHA256:
        raise ValueError("Expected the exact banked EXP-004 LEVEL.DAT")
    if GEOMETRY_OFFSET + CAPACITY > len(data):
        raise ValueError("Known geometry allocation exceeds file bounds")
    stream, report = shade_quad_stream(data[GEOMETRY_OFFSET:GEOMETRY_OFFSET + SOURCE_SIZE])
    if len(stream) > CAPACITY:
        raise ValueError("Shaded stream exceeds the known allocation")
    result = data[:GEOMETRY_OFFSET] + stream + data[GEOMETRY_OFFSET + len(stream):]
    report.update({
        "geometry_offset": GEOMETRY_OFFSET,
        "stream_bytes_before": SOURCE_SIZE,
        "stream_bytes_after": len(stream),
        "allocation_bytes": CAPACITY,
        "source_sha256": SOURCE_SHA256,
        "candidate_sha256": hashlib.sha256(result).hexdigest(),
        "collision": "Not modified",
        "live_appearance": "Pending user comparison; the 3/5 input scale is not a measured pixel ratio",
    })
    return result, report
