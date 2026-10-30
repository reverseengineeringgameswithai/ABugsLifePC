"""EXP-20260906-003: checked wall collision and visible-ground skirt trimming.

Uses established PC cell fields and mesh storage, not a new solver or a
general scene-ground classifier. The selected original render records must
be explicitly supplied and unrotated. Other scene objects are not inferred.
"""
from __future__ import annotations

from fractions import Fraction as F
import math
import struct

from .level_dat import LevelDat
from .terrain_floor_patch import mesh_groups
from .terrain_play_area import encode_group, normal
from .terrain_ramp_sides import _integer, _vector
from .terrain_texture_tiling import MAX_FACES, MAX_VERTICES, cross, decode_mesh


def render_profile(data, *, records, x, z_start, z_end, max_bridge=F(1)):
    """Exact intersections with selected upward original render triangles.

    At most one stored unit of inter-mesh seam can be bridged, explicitly
    reported. This is an authored trim contour, not welding original data.
    Inconsistent overlap, unsupported transforms or larger gaps reject.
    """
    if type(data) is not bytes:
        raise ValueError("DAT must be immutable bytes")
    if not isinstance(records, (tuple, list)) or not records or len(set(records)) != len(records):
        raise ValueError("unique explicit render records required")
    for value in records:
        _integer(value, 0, 65535, "record")
    for value in (x, z_start, z_end):
        _integer(value, -2147483648, 2147483647, "boundary coordinate")
    if z_start >= z_end or not isinstance(max_bridge, (int, F)) or isinstance(max_bridge, bool) or not 0 <= max_bridge <= 1:
        raise ValueError("invalid boundary or bridge limit")
    dat = LevelDat.parse(data)
    spans = []
    for index in records:
        ref = dat.static_mesh_reference("primary", index)
        if ref.object_offset < 0 or ref.object_offset + 24 > len(data):
            raise ValueError("object exceeds file")
        if struct.unpack_from("<3h", data, ref.object_offset + 12) != (0, 0, 0) or data[ref.object_offset + 19] & 31:
            raise ValueError("ground profile requires an established unrotated transform")
        origin = struct.unpack_from("<3i", data, ref.object_offset)
        points = []
        for v in ref.payload.vertices:
            if v.offset < 0 or v.offset + 12 > len(data):
                raise ValueError("vertex exceeds file")
            points.append(tuple(a+b for a,b in zip(struct.unpack_from("<3h", data, v.offset), origin)))
        for group in mesh_groups(data, ref)[0]:
            for face in group["faces"]:
                ids = face["vertex_indices"]
                for order in (((0,1,2),) if len(ids) == 3 else ((0,1,2),(0,2,3))):
                    tri = [points[ids[i]] for i in order]
                    n = cross(*tri)
                    if n[1] >= 0:
                        continue
                    intersections = []
                    for a,b in zip(tri, tri[1:]+tri[:1]):
                        if a[0] == b[0]:
                            if x == a[0]:
                                intersections.extend((F(a[2]), F(b[2])))
                        elif min(a[0],b[0]) <= x <= max(a[0],b[0]):
                            intersections.append(a[2]+F(x-a[0],b[0]-a[0])*(b[2]-a[2]))
                    if not intersections:
                        continue
                    lo,hi = max(F(z_start),min(intersections)), min(F(z_end),max(intersections))
                    if lo >= hi:
                        continue
                    a = tri[0]
                    heights = [F(a[1])-F(n[0]*(x-a[0])+n[2]*(z-a[2]), n[1]) for z in (lo,hi)]
                    spans.append(dict(lo=lo, hi=hi, y_lo=heights[0], y_hi=heights[1],
                                      record=index, face_offset=face["offset"], triangle=order))
    result = []
    cursor = F(z_start)
    for span in sorted(spans, key=lambda s:(s["lo"],s["hi"])):
        if span["lo"] < cursor:
            raise ValueError("overlapping render profile requires separate discrimination")
        if span["lo"] > cursor:
            if not result or span["lo"]-cursor > max_bridge:
                raise ValueError("uncovered original render boundary")
            result.append(dict(lo=cursor, hi=span["lo"], y_lo=result[-1]["y_hi"],
                               y_hi=span["y_lo"], bridge=True))
        result.append(span)
        cursor = span["hi"]
    if cursor != z_end:
        raise ValueError("render boundary is incomplete")
    return result


def profile_y(profile, z):
    for span in profile:
        if span["lo"] <= z <= span["hi"]:
            return span["y_lo"]+(span["y_hi"]-span["y_lo"])*(z-span["lo"])/(span["hi"]-span["lo"])
    raise ValueError("coordinate outside render profile")


def _clip(points, distance):
    if not points:
        return []
    result = []
    a = points[-1]
    da = distance(a)
    for b in points:
        db = distance(b)
        if (da >= 0) != (db >= 0):
            t = da/(da-db)
            result.append(tuple(u+t*(v-u) for u,v in zip(a,b)))
        if db >= 0:
            result.append(b)
        a,da = b,db
    return result


def trim_side_mesh(mesh, *, origin, profiles):
    """Clip only the new skirts; retain UV/colour interpolation and opaque bytes.

    Ground clipping uses exact fractions. Integer output is rounded and the
    lower contour is clamped upward to the selected ground at rounded Z.
    Original ramp vertices and command groups are never rewritten here.
    """
    origin = _vector(origin, -2147483648, 2147483647, "origin")
    vertices,faces = decode_mesh(mesh)
    if not profiles or any(type(x) is not int for x in profiles):
        raise ValueError("explicit side profiles required")
    for profile in profiles.values():
        if not profile:
            raise ValueError("empty profile")
        for i,s in enumerate(profile):
            if s["lo"] >= s["hi"] or (i and profile[i-1]["hi"] != s["lo"]):
                raise ValueError("profile intervals must be positive and contiguous")
    output,lookup,commands = [],{},[]
    max_rounding = F(0)
    for tag,ids,words in faces:
        if tag != 0x61:
            raise ValueError("skirt input must be established textured triangles")
        raw = [vertices[i] for i in ids]
        opaque = [v[6:8]+v[11:] for v in raw]
        if len(set(opaque)) != 1:
            raise ValueError("cannot interpolate unknown fields")
        points = [tuple(F(a+b) for a,b in zip(struct.unpack_from("<3h",v),origin))
                  +tuple(F(c) for c in v[8:11])+(F(w&255),F(w>>8)) for v,w in zip(raw,words)]
        if len({p[0] for p in points}) != 1 or int(points[0][0]) not in profiles:
            raise ValueError("face is not on a selected vertical side")
        profile = profiles[int(points[0][0])]
        original_normal = cross(*(p[:3] for p in points))
        for span in profile:
            if max(p[2] for p in points) <= span["lo"] or min(p[2] for p in points) >= span["hi"]:
                continue
            polygon = _clip(points, lambda p:p[2]-span["lo"])
            polygon = _clip(polygon, lambda p:span["hi"]-p[2])
            polygon = _clip(polygon, lambda p:span["y_lo"]+(span["y_hi"]-span["y_lo"])*(p[2]-span["lo"])/(span["hi"]-span["lo"])-p[1])
            if len(polygon) < 3:
                continue
            corners = []
            for p in polygon:
                xyz = [round(c) for c in p[:3]]
                xyz[1] = min(xyz[1],math.floor(profile_y(profile,xyz[2])))
                max_rounding = max(max_rounding, *(abs(F(c)-v) for c,v in zip(xyz,p[:3])))
                local = [c-o for c,o in zip(xyz,origin)]
                for c in local:
                    _integer(c,-32768,32767,"trimmed local coordinate")
                colour = bytes(_integer(round(c),0,255,"colour") for c in p[3:6])
                u,v = round(p[6]),round(p[7])
                _integer(u,64,127,"wall U"); _integer(v,192,255,"wall V")
                value = struct.pack("<3h",*local)+opaque[0][:2]+colour+opaque[0][2:]
                if value not in lookup:
                    if len(output) >= MAX_VERTICES:
                        raise ValueError("trimmed vertex capacity exceeded")
                    lookup[value] = len(output); output.append(value)
                corners.append((lookup[value],u|(v<<8),tuple(xyz)))
            for i in range(1,len(corners)-1):
                triangle = (corners[0],corners[i],corners[i+1])
                n = cross(*(v[2] for v in triangle))
                if n == (0,0,0):
                    continue
                if sum(a*b for a,b in zip(n,original_normal)) <= 0:
                    raise ValueError("trimmed face winding changed")
                if len(commands) >= MAX_FACES:
                    raise ValueError("trimmed face capacity exceeded")
                commands.append(struct.pack("<6H",*(v[0]*12 for v in triangle),*(v[1] for v in triangle)))
    if not commands:
        raise ValueError("ground trim removed every face")
    stream = struct.pack("<i",len(output))+b"".join(output)+struct.pack("<Hh",0x61,len(commands))+b"".join(commands)+b"\xff\xff"
    return stream,dict(original_vertices=len(vertices),original_faces=len(faces),vertices=len(output),faces=len(commands),
                       max_coordinate_change_from_exact=float(max_rounding),unknown_fields="+6/+7/+11 retained",
                       scope="only new side mesh; original top/storage unchanged; lower contour is not buried")


def side_collision(left, right, *, origin, bottom_y, skin=96):
    """Outward-facing vertical cells using the banked box's 96-unit pairing.

    Upper collision edge is render top minus skin; lower edge is the buried
    control base plus skin. These are not guardrails or global X/Z barriers.
    """
    origin = _vector(origin,-2147483648,2147483647,"collision origin")
    _integer(bottom_y,-32768,32767,"base"); _integer(skin,0,256,"skin")
    edges = []
    for edge in (left,right):
        if not isinstance(edge,(list,tuple)) or not 2 <= len(edge) <= 256:
            raise ValueError("bounded side edge required")
        edge = tuple(_vector(v,-32768,32767,"edge") for v in edge)
        if len({v[0] for v in edge}) != 1 or any(a[2] >= b[2] for a,b in zip(edge,edge[1:])):
            raise ValueError("constant-X, increasing-Z edge required")
        if any(v[1]-skin >= bottom_y+skin for v in edge):
            raise ValueError("wall base must be below the collision top")
        edges.append(edge)
    if edges[0][0][0] >= edges[1][0][0] or (edges[0][0][2],edges[0][-1][2]) != (edges[1][0][2],edges[1][-1][2]):
        raise ValueError("side orientation or extents disagree")
    data,rows = bytearray(),[]
    for side,edge in enumerate(edges):
        for a,b in zip(edge,edge[1:]):
            q = ((a[0],a[1]-skin,a[2]),(b[0],b[1]-skin,b[2]),
                 (b[0],bottom_y+skin,b[2]),(a[0],bottom_y+skin,a[2]))
            for ids in ((0,1,2),(0,2,3)):
                # PC normal is negative cross, opposite the render convention.
                tri = tuple(q[i] for i in (tuple(reversed(ids)) if side == 0 else ids))
                n = normal(tri)
                if n != ((-16384,0,0) if side == 0 else (16384,0,0)):
                    raise ValueError("wall normal does not face outward")
                rows.append(dict(side="west" if side == 0 else "east",cell_relative_offset=len(data)+12,vertices=tri,normal=n))
                data.extend(encode_group(tri,origin))
    return bytes(data)+b"\xff\xff",rows
