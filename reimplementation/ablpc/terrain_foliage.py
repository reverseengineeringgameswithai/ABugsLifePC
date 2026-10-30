"""Checked reuse of original PC grass primitives, EXP-20260906-006.

Positive-count mesh grammar: 0045A7F0; 12/16-byte face strides; texture page
and unknown tag bits are retained. Only XYZ, indices and allocation pointers
are authored. Texture pixels remain a dependency of the original level.
"""

import math
import struct
from collections import defaultdict

from .level_dat import LevelDat
from .terrain_floor_patch import contains, mesh_groups
from .terrain_visibility import scene_visibility_radius

MAX_VERTICES = 5462


def decode_mesh(raw):
    if not isinstance(raw, bytes) or len(raw) < 10:
        raise ValueError("expected immutable complete positive mesh")
    count = struct.unpack_from("<i", raw)[0]
    if not 1 <= count <= min(MAX_VERTICES, (len(raw) - 6) // 12):
        raise ValueError("invalid vertex count")
    vertices = tuple(raw[4 + i * 12:16 + i * 12] for i in range(count))
    cursor, groups = 4 + count * 12, []
    while cursor <= len(raw) - 2:
        tag = struct.unpack_from("<H", raw, cursor)[0]
        if tag == 0xFFFF:
            if cursor + 2 != len(raw) or not groups:
                raise ValueError("empty stream or trailing bytes")
            return vertices, tuple(groups)
        if cursor > len(raw) - 4:
            raise ValueError("truncated group header")
        count = struct.unpack_from("<h", raw, cursor + 2)[0]
        arity = 3 if tag & 1 else 4
        if count < 0 or count > (len(raw) - cursor - 4) // (arity * 4):
            raise ValueError("invalid signed face count")
        cursor += 4
        faces = []
        for _ in range(count):
            words = struct.unpack_from("<" + "H" * (arity * 2), raw, cursor)
            if any(i % 12 or i >= len(vertices) * 12 for i in words[:arity]):
                raise ValueError("invalid vertex byte reference")
            faces.append((tuple(i // 12 for i in words[:arity]), words[arity:]))
            cursor += arity * 4
        groups.append((tag, tuple(faces)))
    raise ValueError("missing mesh terminator")


def encode_mesh(vertices, groups):
    if not 1 <= len(vertices) <= MAX_VERTICES or any(len(v) != 12 for v in vertices):
        raise ValueError("invalid vertex allocation")
    out = bytearray(struct.pack("<i", len(vertices)) + b"".join(vertices))
    for tag, faces in groups:
        if type(tag) is not int or not 0 <= tag < 0xFFFF or len(faces) > 32767:
            raise ValueError("invalid group header")
        arity = 3 if tag & 1 else 4
        out.extend(struct.pack("<Hh", tag, len(faces)))
        for indices, fields in faces:
            if len(indices) != arity or len(fields) != arity:
                raise ValueError("face arity mismatch")
            if any(type(i) is not int or not 0 <= i < len(vertices) for i in indices):
                raise ValueError("invalid face index")
            if any(type(v) is not int or not 0 <= v <= 65535 for v in fields):
                raise ValueError("invalid preserved face word")
            out.extend(struct.pack("<" + "H" * (arity * 2),
                                   *(i * 12 for i in indices), *fields))
    out.extend(b"\xff\xff")
    return bytes(out)


def blade_templates(raw, *, count=3):
    """Select connected original stem quads and their unique tip triangles."""
    vertices, groups = decode_mesh(raw)
    quads = [(tag, f) for tag, faces in groups if tag == 0x162 for f in faces]
    triangles = [(tag, f) for tag, faces in groups if tag == 0x8163 for f in faces]
    if type(count) is not int or not 1 <= count <= len(quads):
        raise ValueError("unavailable blade count")
    result = []
    for tag, quad in quads[:count]:
        shared = [(t, f) for t, f in triangles if len(set(f[0]) & set(quad[0])) == 2]
        if len(shared) != 1:
            raise ValueError("blade tip must have one unambiguous shared edge")
        tri_tag, tri = shared[0]
        ids = tuple(dict.fromkeys((*quad[0], *tri[0])))
        if len(ids) != 5:
            raise ValueError("expected five-vertex blade")
        coords = [struct.unpack_from("<3h", vertices[i]) for i in ids]
        bases = set(quad[0]) - set(tri[0])
        if len(bases) != 2:
            raise ValueError("expected two base vertices")
        base_points = [struct.unpack_from("<3h", vertices[i]) for i in sorted(bases)]
        pivot = tuple(round(sum(p[k] for p in base_points) / 2) for k in range(3))
        if not min(p[1] for p in coords) < min(p[1] for p in base_points):
            raise ValueError("tip must extend upward from base")
        mapping = {old: new for new, old in enumerate(ids)}
        result.append({"vertices": tuple(vertices[i] for i in ids), "pivot": pivot,
                       "source_indices": ids,
                       "faces": ((tag, (tuple(mapping[i] for i in quad[0]), quad[1])),
                                 (tri_tag, (tuple(mapping[i] for i in tri[0]), tri[1])))})
    return tuple(result)


def quarter_turn(x, z, turns):
    if type(turns) is not int or not 0 <= turns < 4:
        raise ValueError("expected quarter turn 0..3")
    return ((x, z), (z, -x), (-x, -z), (-z, x))[turns]


def append_blades(control, donor, placements, origin):
    vertices, groups = decode_mesh(control)
    templates = blade_templates(donor)
    vertices, groups = list(vertices), list(groups)
    if len(origin) != 3 or any(type(v) is not int or not -2**31 <= v < 2**31 for v in origin):
        raise ValueError("invalid mesh origin")
    extra = defaultdict(list)
    for index, placement in enumerate(placements):
        if len(placement) != 4 or any(type(v) is not int for v in placement):
            raise ValueError("placement needs integer world XYZ and quarter turn")
        x, y, z, turns = placement
        if any(not -2**31 <= v * 32 < 2**31 for v in (x, y, z)):
            raise ValueError("placement overflows world coordinates")
        template = templates[index % len(templates)]
        offset = len(vertices)
        for source in template["vertices"]:
            point = struct.unpack_from("<3h", source)
            dx, dz = quarter_turn(point[0] - template["pivot"][0],
                                  point[2] - template["pivot"][2], turns)
            local = (x + dx - origin[0], y + point[1] - template["pivot"][1] - origin[1],
                     z + dz - origin[2])
            if any(not -32768 <= v <= 32767 for v in local):
                raise ValueError("placed vertex overflows local int16")
            vertices.append(struct.pack("<3h", *local) + source[6:])
        for tag, (indices, fields) in template["faces"]:
            extra[tag].append((tuple(offset + i for i in indices), fields))
    groups.extend((tag, tuple(faces)) for tag, faces in extra.items())
    return encode_mesh(vertices, groups)


def visible_floor_height(control, origin, x, z):
    """Interpolate authored visible triangles, not unidentified collision fields."""
    vertices, groups = decode_mesh(control)
    xyz = [tuple(v + origin[i] for i, v in enumerate(struct.unpack_from("<3h", p)))
           for p in vertices]
    heights = []
    for tag, faces in groups:
        for indices, _ in faces:
            points = [xyz[i] for i in indices]
            for ids in (((0, 1, 2),) if tag & 1 else ((0, 1, 2), (0, 2, 3))):
                a, b, c = [points[i] for i in ids]
                den = (b[0]-a[0])*(c[2]-a[2]) - (b[2]-a[2])*(c[0]-a[0])
                if not den or not contains(tuple((p[0], p[2]) for p in (a, b, c)), (x, z)):
                    continue
                u = ((x-a[0])*(c[2]-a[2]) - (z-a[2])*(c[0]-a[0])) / den
                v = ((b[0]-a[0])*(z-a[2]) - (b[2]-a[2])*(x-a[0])) / den
                heights.append(a[1]+u*(b[1]-a[1])+v*(c[1]-a[1]))
    if not heights:
        raise ValueError("placement has no authored visible floor")
    return round(min(heights))


def append_scene_mesh(raw, scene_index, mesh):
    """Copy-on-write growth with PC-aware bounds for 640x480/focal320.

    EXP-20260906-011: a geometric sphere alone can cull the entire expanded
    ground/foliage while collision remains active. Use the shared side-plane
    bound, retain larger existing bounds, and reject unsupported transforms.
    """
    vertices, groups = decode_mesh(mesh)
    dat = LevelDat.parse(raw)
    ref = dat.static_mesh_reference("primary", scene_index)
    if (struct.unpack_from("<3h", raw, ref.object_offset + 12) != (0, 0, 0)
            or raw[ref.object_offset + 19] & 0x1f):
        raise ValueError("growth requires an unrotated, unscaled target")
    old_tail_distance = struct.unpack_from("<i", raw, len(raw)-4)[0]
    if not 4 <= old_tail_distance <= len(raw):
        raise ValueError("invalid trailing data distance")
    pad = (-(len(raw)-4)) % 4
    geometry = len(raw)-4+pad
    growth = pad + len(mesh)
    if old_tail_distance+growth >= 2**31 or geometry+len(mesh)+4 >= 2**31:
        raise ValueError("DAT growth exceeds signed PC offset")
    origin = struct.unpack_from("<3i", raw, ref.object_offset)
    scene = dat.primary_records[scene_index]
    center = (scene.center_component_00, scene.center_component_04, scene.center_component_08)
    if not any(faces for _, faces in groups):
        raise ValueError("growth requires at least one face")
    distance2 = max(sum((struct.unpack_from("<3h", vertex)[k]+origin[k]-center[k])**2
                        for k in range(3)) for vertex in vertices)
    geometric_radius = math.isqrt(distance2)
    geometric_radius += geometric_radius * geometric_radius != distance2
    radius = scene_visibility_radius(geometric_radius, scene.field_0c_signed)
    out = bytearray(raw[:-4] + b"\0"*pad + mesh + struct.pack("<i", old_tail_distance+growth))
    struct.pack_into("<I", out, ref.object_offset+20, geometry)
    struct.pack_into("<h", out, ref.record_offset+12, radius)
    return bytes(out), {"geometry_offset": geometry, "mesh_bytes": len(mesh),
                        "growth_bytes": growth, "radius": radius,
                        "pointer_offset": ref.object_offset+20,
                        "radius_offset": ref.record_offset+12,
                        "old_trailing_base": len(raw)-old_tail_distance}


def mesh_bytes(raw, scene_index):
    dat = LevelDat.parse(raw)
    ref = dat.static_mesh_reference("primary", scene_index)
    _, end = mesh_groups(raw, ref)
    return raw[ref.geometry_offset:end+2], ref
