"""Bounded atlas tiling and copy-on-write growth for the EXP-005 PC mesh.

The PC relocator adds the DAT base to object +0x14 (0044bd13..0044bd22).
0044bec4..0044bf25 locates trailing data as base + file_size - final_word.
Keep all old offsets, including that trailing-data base, when adding a mesh.
This is not a general LEVEL.DAT repacker or a collision writer.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import struct

from .level_dat import LevelDat


SOURCE_SHA256 = "b9da33f9fa8a8227e78ed72fe6870f187e8065a04039b6de4ebcd72f719d6241"
TERRAIN_SHA256 = "1ff3af9f0b5b2c2957bde8e877e1d988054455f3e1be18f8ea0e6cb57875d16b"
SOURCE_OFFSET, SOURCE_SIZE = 113136, 1730
MAX_VERTICES = 5462  # Largest index*12 representable in a uint16 face reference.
MAX_FACES = 32767  # Native group counts are signed int16.


def digest(data):
    return hashlib.sha256(data).hexdigest()


def decode_mesh(data):
    """Read complete positive-count 0x60/0x61 streams, including the terminator."""
    if not isinstance(data, bytes) or len(data) < 10:
        raise ValueError("Expected immutable complete mesh bytes")
    count = struct.unpack_from("<i", data)[0]
    if not 1 <= count <= min(MAX_VERTICES, (len(data) - 6) // 12):
        raise ValueError("Impossible vertex count")
    vertices = tuple(data[4 + i*12:16 + i*12] for i in range(count))
    cursor, faces = 4 + count*12, []
    while True:
        if cursor > len(data) - 2:
            raise ValueError("Missing bounded mesh terminator")
        tag = struct.unpack_from("<H", data, cursor)[0]
        if tag == 0xffff:
            if cursor + 2 != len(data) or not faces:
                raise ValueError("Empty mesh or bytes after terminator")
            return vertices, tuple(faces)
        if tag not in (0x60, 0x61) or cursor > len(data) - 4:
            raise ValueError("Unsupported or truncated mesh group")
        count_faces = struct.unpack_from("<h", data, cursor + 2)[0]
        arity = 3 if tag & 1 else 4
        cursor += 4
        if count_faces <= 0 or count_faces > (len(data) - cursor) // (arity*4):
            raise ValueError("Impossible signed face count")
        if len(faces) + count_faces > MAX_FACES:
            raise ValueError("Face budget exceeded")
        for _ in range(count_faces):
            words = struct.unpack_from("<" + "H"*(arity*2), data, cursor)
            if any(ref % 12 or ref >= count*12 for ref in words[:arity]):
                raise ValueError("Invalid vertex byte offset")
            faces.append((tag, tuple(ref//12 for ref in words[:arity]), words[arity:]))
            cursor += arity*4


def cross(a, b, c):
    u, v = [b[i]-a[i] for i in range(3)], [c[i]-a[i] for i in range(3)]
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])


def clip(poly, axis, bound, greater):
    """Clip exact (projected_u, projected_v, barycentric_weights) vertices."""
    output = []
    for start, end in zip(poly, poly[1:] + poly[:1]):
        ds, de = start[axis]-bound, end[axis]-bound
        inside_s, inside_e = (ds >= 0, de >= 0) if greater else (ds <= 0, de <= 0)
        if inside_s != inside_e:
            t = Fraction(ds, ds-de)
            output.append(tuple(start[i] + t*(end[i]-start[i]) for i in range(5)))
        if inside_e:
            output.append(end)
    compact = []
    for p in output:
        if not compact or p[:2] != compact[-1][:2]:
            compact.append(p)
    if len(compact) > 1 and compact[0][:2] == compact[-1][:2]:
        compact.pop()
    return compact


def tile_mesh(data, origin, *, tile_size=512, anchor=(4000, -3200, 13000)):
    """Tile each original triangle without crossing its existing diagonal.

    Ground uses projected world X/Z. Walls retain U-height, V-horizontal.
    XYZ is rounded only when encoding int16; the exact rounding error is
    reported. Unknown vertex +6/+7/+11 must agree within each source triangle.
    """
    if type(tile_size) is not int or not 128 <= tile_size <= 2048:
        raise ValueError("Tile size must be an integer in 128..2048 stored units")
    for vector in (origin, anchor):
        if not isinstance(vector, (tuple, list)) or len(vector) != 3 or any(type(v) is not int or not -2**31 <= v < 2**31 for v in vector):
            raise ValueError("Expected three signed int32 coordinates")
    vertices, faces = decode_mesh(data)
    output_vertices, lookup, output_faces, provenance = [], {}, [], []
    max_error, degenerates = Fraction(0), 0
    surface_counts = {"ground": 0, "wall": 0}
    for face_index, (tag, refs, fields) in enumerate(faces):
        raw = [vertices[i] for i in refs]
        xyz = [tuple(v + origin[i] for i, v in enumerate(struct.unpack_from("<3h", r))) for r in raw]
        wall_axis = next((axis for axis in (0, 2) if len({p[axis] for p in xyz}) == 1), None)
        wall = wall_axis is not None and len({p[1] for p in xyz}) > 1
        region_u = 64 if wall else 0
        if any(not (region_u <= (w & 255) <= region_u + 63 and 192 <= (w >> 8) <= 255) for w in fields):
            raise ValueError("Source face does not use its expected atlas region")
        projected = [((anchor[1]-p[1], p[2]-anchor[2]) if wall_axis == 0 else (anchor[1]-p[1], p[0]-anchor[0]))
                     if wall else (p[0]-anchor[0], p[2]-anchor[2]) for p in xyz]
        triangles = ((0, 1, 2),) if tag & 1 else ((0, 1, 2), (0, 2, 3))
        for triangle_index, corners in enumerate(triangles):
            points = [xyz[i] for i in corners]
            source_normal = cross(*points)
            if not any(source_normal):
                degenerates += 1
                continue
            attrs = [raw[i] for i in corners]
            if len({r[6:8] + r[11:12] for r in attrs}) != 1:
                raise ValueError("Cannot interpolate unidentified vertex fields")
            q = [projected[i] for i in corners]
            if (q[1][0]-q[0][0])*(q[2][1]-q[0][1]) == (q[2][0]-q[0][0])*(q[1][1]-q[0][1]):
                raise ValueError("Unsupported degenerate texture projection")
            initial = [tuple(map(Fraction, (*p, *(int(i == j) for j in range(3))))) for i, p in enumerate(q)]
            ranges = [range(min(p[a] for p in q)//tile_size, -(-max(p[a] for p in q)//tile_size)) for a in (0, 1)]
            if len(ranges[0])*len(ranges[1]) > MAX_FACES:
                raise ValueError("Texture subdivision budget exceeded")
            for tu in ranges[0]:
                for tv in ranges[1]:
                    poly = initial
                    for axis, tile in ((0, tu), (1, tv)):
                        poly = clip(poly, axis, tile*tile_size, True)
                        poly = clip(poly, axis, (tile+1)*tile_size, False)
                    if len(poly) < 3:
                        continue
                    encoded = []
                    for p in poly:
                        exact = [sum(p[2+j]*points[j][axis] for j in range(3)) - origin[axis] for axis in range(3)]
                        local = tuple(round(v) for v in exact)
                        if any(not -32768 <= v <= 32767 for v in local):
                            raise ValueError("Tiled vertex exceeds int16")
                        max_error = max(max_error, *(abs(exact[i]-local[i]) for i in range(3)))
                        channels = bytes(round(sum(p[2+j]*attrs[j][axis] for j in range(3))) for axis in (8, 9, 10))
                        vertex = struct.pack("<3h", *local) + attrs[0][6:8] + channels + attrs[0][11:12]
                        u = region_u + round((p[0]-tu*tile_size)*63/tile_size)
                        v = 192 + round((p[1]-tv*tile_size)*63/tile_size)
                        if not region_u <= u <= region_u + 63 or not 192 <= v <= 255:
                            raise ValueError("Tiled UV escapes selected atlas region")
                        encoded.append((vertex, u | v << 8, local))
                    for i in range(1, len(encoded)-1):
                        tri = [encoded[k] for k in (0, i, i+1)]
                        n = cross(*(p[2] for p in tri))
                        if not any(n):
                            degenerates += 1
                            continue
                        if sum(n[a]*source_normal[a] for a in range(3)) <= 0:
                            raise ValueError("Coordinate rounding reverses triangle winding")
                        indices = []
                        for vertex, _, _ in tri:
                            if vertex not in lookup:
                                if len(output_vertices) >= MAX_VERTICES:
                                    raise ValueError("Tiled mesh exceeds uint16 vertex-reference capacity")
                                lookup[vertex] = len(output_vertices)
                                output_vertices.append(vertex)
                            indices.append(lookup[vertex]*12)
                        if len(output_faces) >= MAX_FACES:
                            raise ValueError("Tiled mesh exceeds signed face-count capacity")
                        output_faces.append(struct.pack("<6H", *indices, *(p[1] for p in tri)))
                        provenance.append({"source_face": face_index, "source_triangle": triangle_index,
                                           "tile": [tu, tv], "surface": "wall" if wall else "ground"})
                        surface_counts["wall" if wall else "ground"] += 1
    if not output_faces:
        raise ValueError("Tiling produced no nondegenerate faces")
    result = (struct.pack("<i", len(output_vertices)) + b"".join(output_vertices)
              + struct.pack("<Hh", 0x61, len(output_faces)) + b"".join(output_faces) + b"\xff\xff")
    return result, {
        "tile_size_stored": tile_size, "tile_size_world": tile_size*32, "anchor_stored": list(anchor),
        "source_vertices": len(vertices), "source_faces": len(faces), "vertex_count": len(output_vertices),
        "face_count": len(output_faces), "stream_bytes": len(result), "stream_sha256": digest(result),
        "tag": 0x61, "surface_triangles": surface_counts, "degenerate_triangles_omitted": degenerates,
        "max_coordinate_rounding_error_stored": str(max_error),
        "projection": "Ground X/Z; vertical-wall U is height and V is X or Z. 512 is an authoring choice, not a native universal tile scale.",
        "preservation": "Original triangle boundaries before int16 quantization; original corner colours; interpolated known colour bytes; unchanged unknown vertex fields. Collision is not an input to tiling.",
        "faces": provenance,
    }


def append_mesh(dat, mesh, *, record_index=160, expected_geometry=SOURCE_OFFSET):
    """Rebind one unique static object to fresh bytes before a relocated footer."""
    if not isinstance(dat, bytes) or len(dat) < 4 or len(dat) % 4:
        raise ValueError("Expected a four-byte-aligned immutable DAT")
    if type(record_index) is not int or type(expected_geometry) is not int:
        raise ValueError("Record and expected geometry must be integers")
    decode_mesh(mesh)
    parsed = LevelDat.parse(dat)
    ref = parsed.static_mesh_reference("primary", record_index)
    footer_offset = len(dat)-4
    pointer_offset = ref.object_offset + 20
    if (ref.geometry_offset != expected_geometry or ref.object_offset < parsed.parsed_prefix_end
            or pointer_offset+4 > footer_offset or ref.geometry_offset < parsed.parsed_prefix_end
            or ref.payload.end_offset > footer_offset):
        raise ValueError("Static mesh identity or allocation bounds changed")
    aliases = [r for section in ("primary", "secondary") for r in parsed.records(section)
               if r.payload_offset_candidate == ref.object_offset]
    if len(aliases) != 1:
        raise ValueError("Cannot rebind an aliased object")
    final_word = struct.unpack_from("<i", dat, footer_offset)[0]
    if final_word != -1 and not 0x118+4 <= final_word <= len(dat)-parsed.parsed_prefix_end:
        raise ValueError("Invalid end-relative trailing-data span")
    padding = (-len(mesh)) % 4
    growth = len(mesh) + padding
    if len(dat)+growth >= 2**31 or final_word != -1 and final_word+growth >= 2**31:
        raise ValueError("Expanded DAT exceeds signed offset range")
    new_word = -1 if final_word == -1 else final_word + growth
    result = bytearray(dat[:-4] + mesh + bytes(padding) + struct.pack("<i", new_word))
    struct.pack_into("<I", result, pointer_offset, footer_offset)
    return bytes(result), {
        "geometry_offset": footer_offset, "object_offset": ref.object_offset,
        "scene_record_offset": ref.record_offset, "pointer_field_offset": pointer_offset,
        "previous_geometry_offset": ref.geometry_offset, "source_bytes": len(dat), "candidate_bytes": len(result),
        "growth_bytes": growth, "alignment_padding_bytes": padding,
        "footer_offset_before": footer_offset, "footer_offset_after": len(result)-4,
        "end_relative_word_before": final_word, "end_relative_word_after": new_word,
        "trailing_data_offset": None if final_word == -1 else len(dat)-final_word,
        "preservation": "All original bytes except object+0x14 and the displaced final word; no existing payload or unknown field moved or overwritten.",
        "native_evidence": ["0044bd13..0044bd22", "0044bec4..0044bf25"],
    }


def build_tiled_pair(terrain, dat, *, tile_size=512):
    if not isinstance(terrain, bytes) or digest(terrain) != TERRAIN_SHA256:
        raise ValueError("Expected unchanged EXP-004/005 collision")
    if not isinstance(dat, bytes) or digest(dat) != SOURCE_SHA256:
        raise ValueError("Expected exact combined EXP-005 material DAT")
    ref = LevelDat.parse(dat).static_mesh_reference("primary", 160)
    if (ref.object_offset, ref.geometry_offset) != (18672, SOURCE_OFFSET):
        raise ValueError("Pinned mesh identity changed")
    origin = struct.unpack_from("<3i", dat, ref.object_offset)
    mesh, tiling = tile_mesh(dat[SOURCE_OFFSET:SOURCE_OFFSET+SOURCE_SIZE], origin, tile_size=tile_size)
    result, allocation = append_mesh(dat, mesh)
    return terrain, result, {
        "experiment": "EXP-20260905-006", "arm": "tiled-material",
        "source_dat_sha256": SOURCE_SHA256, "candidate_dat_sha256": digest(result),
        "terrain_sha256": TERRAIN_SHA256, "collision_byte_identical": True,
        "mesh_origin": list(origin), "tiling": tiling, "allocation": allocation,
        "runtime_acceptance": "Pending; this is an offline authored candidate, not a live appearance or general repacking result.",
    }
