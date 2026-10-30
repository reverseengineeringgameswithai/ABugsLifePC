"""Bounded static floor stitching and projected-footprint inspection.

PC consumers: 004AA5C3..004AA646 (14-bit signed plane normal),
004AA650..004AA666 (Y edges), 004AB527..004AB547 (signed Y window).
Mesh stream: 0045A8B0 (terminator), 0045C787 / 0046024E (12/16 strides).
Unknown bytes are retained. This is not a movement solver or a mesh importer.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import math
import struct

from .level_dat import LevelDat, DatFormatError
from .terrain_all import TerrainAll, TerrainFormatError
from .terrain_height import TerrainHeightModel


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def on_segment(p, a, b):
    return orient(a, b, p) == 0 and all(min(a[i], b[i]) <= p[i] <= max(a[i], b[i]) for i in (0, 1))


def segments_touch(a, b, c, d):
    q = (orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b))
    return (q[0]*q[1] < 0 and q[2]*q[3] < 0) or any(
        on_segment(p, u, v) for p, u, v in ((a, c, d), (b, c, d), (c, a, b), (d, a, b)))


def contains(tri, point):
    if orient(*tri) == 0:
        return any(on_segment(point, tri[i], tri[(i+1) % 3]) for i in range(3))
    signs = [orient(tri[i], tri[(i+1) % 3], point) for i in range(3)]
    return min(signs) >= 0 or max(signs) <= 0


def polygons_touch(a, b):
    """Inclusive intersection, including projected vertical/degenerate faces."""
    if not a or not b:
        return False
    if any(max(p[i] for p in a) < min(p[i] for p in b) or
           max(p[i] for p in b) < min(p[i] for p in a) for i in (0, 1)):
        return False
    if any(segments_touch(a[i], a[(i+1) % len(a)], b[j], b[(j+1) % len(b)])
           for i in range(len(a)) for j in range(len(b))):
        return True
    return (any(contains((a[0], a[i], a[i+1]), p) for i in range(1, len(a)-1) for p in b)
            or any(contains((b[0], b[i], b[i+1]), p) for i in range(1, len(b)-1) for p in a))


@dataclass(frozen=True)
class FloorCell:
    source: int
    payload_source: int
    group: int
    offset: int
    vertices: tuple
    raw: bytes
    editable: bool

    @property
    def footprint(self):
        return tuple((v[0], v[2]) for v in self.vertices)

    def report(self):
        return {"source_record": self.source, "payload_source": self.payload_source,
                "group_offset": self.group, "file_offset": self.offset,
                "vertices_stored": self.vertices, "normal": struct.unpack_from("<3h", self.raw),
                "x_window": struct.unpack_from("<2h", self.raw, 24),
                "y_z_windows_signed": struct.unpack_from("<4b", self.raw, 28),
                "cell_sha256": digest(self.raw), "editable": self.editable}


def floor_cells(terrain):
    """Resolve static and cloned terrain instances; omit inactive templates."""
    result = []
    for d in TerrainHeightModel(terrain).descriptors:
        r = terrain.records[d.source_index]
        if not d.height_eligible or d.payload_source_index is None:
            continue
        if r.field_44 >= 0 and r.field_46 == 0:
            continue  # Original initializer clears template tags; EXP-002.
        base = (r.component_x, r.component_y, r.component_z)
        for g in terrain.collision_payload(d.payload_source_index).groups:
            for c in g.cells:
                w = c.words
                vertices = tuple(tuple(base[i]+w[3+i]+delta[i] for i in range(3))
                                 for delta in ((0, 0, 0), w[6:9], w[9:12]))
                result.append(FloorCell(r.index, d.payload_source_index, g.offset, c.offset,
                                        vertices, c.raw, (r.field_10, r.field_44, r.field_46) == (6, -1, 0)))
    return tuple(result)


def boundary_census(cells, source=99, group=47640):
    target = [c for c in cells if c.source == source and c.group == group]
    if not target:
        raise TerrainFormatError("target group is absent")
    edges = defaultdict(list)
    for c in target:
        for i in range(3):
            edges[tuple(sorted((c.footprint[i], c.footprint[(i+1) % 3])))].append(c)
    if any(len(v) > 2 for v in edges.values()):
        raise TerrainFormatError("nonmanifold target footprint")
    boundaries = []
    touching = set()
    for edge, owners in sorted(edges.items()):
        if len(owners) != 1:
            continue
        owner = owners[0]
        neighbors = []
        for i, c in enumerate(cells):
            if polygons_touch(edge, c.footprint):
                touching.add(i)
            if c != owner and all(v in c.footprint for v in edge):
                neighbors.append(c.report())
        boundaries.append({"edge_xz_stored": edge, "owner": owner.report(), "full_edge_neighbors": neighbors})
    return {"target_cells": [c.report() for c in target], "boundaries": boundaries,
            "touching_cells": [cells[i].report() for i in sorted(touching)],
            "scope": "all resolved tag-6/7/8 static/clone instances; inactive templates excluded"}


def normal(vertices):
    a, b, c = vertices
    u = [b[i]-a[i] for i in range(3)]
    v = [c[i]-a[i] for i in range(3)]
    cross = (u[2]*v[1]-u[1]*v[2], u[0]*v[2]-u[2]*v[0], u[1]*v[0]-u[0]*v[1])
    length2 = sum(x*x for x in cross)
    if not length2 or cross[1] >= 0:
        raise TerrainFormatError("requires a nondegenerate upward floor")
    # Exact truncation toward zero at length 16384, without floating rounding.
    return tuple((-1 if v < 0 else 1)*math.isqrt((v*16384)**2//length2) for v in cross)


def stitch_floor_vertex(raw, vertex, dy):
    """Move every incident editable cell at an exact stored-world XYZ corner.

    Change only normal, h0, two Y edges and the enclosing relative Y window.
    No X/Z field, directory, group, material, opaque field or length changes.
    The source must be a complete terrain file, not an arbitrarily chosen group.
    """
    if not isinstance(raw, (bytes, bytearray, memoryview)):
        raise TerrainFormatError("terrain source must be bytes")
    if not isinstance(vertex, (tuple, list)) or len(vertex) != 3 or any(type(v) is not int for v in vertex) or type(dy) is not int:
        raise TerrainFormatError("corner and displacement must be integers")
    vertex = tuple(vertex)
    t = TerrainAll.parse(bytes(raw))
    incident = [c for c in floor_cells(t) if vertex in c.vertices]
    if not incident or any(not c.editable for c in incident):
        raise TerrainFormatError("corner is absent or touches an unsupported instance")
    if dy == 0:
        return t.data, []
    output = bytearray(t.data)
    changes = []
    for cell in incident:
        if struct.unpack_from("<h", cell.raw, 2)[0] >= 0:
            raise TerrainFormatError("incident cell is not an upward floor")
        r = t.records[cell.source]
        vertices = tuple((p[0], p[1]+dy, p[2]) if p == vertex else p for p in cell.vertices)
        if any(not -0x80000000 <= x*32 <= 0x7fffffff for p in vertices for x in p):
            raise TerrainFormatError("world coordinate overflows int32")
        a, b, c = vertices
        n = normal(vertices)
        values = (a[1]-r.component_y, b[1]-a[1], c[1]-a[1])
        if any(not -32768 <= v <= 32767 for v in values):
            raise TerrainFormatError("cell Y field overflows int16")
        lower = (min(p[1] for p in vertices)-a[1])//64
        span = max(1, (max(p[1] for p in vertices)-a[1]-lower*64+63)//64)
        if not -128 <= lower <= 127 or not 0 <= span <= 127:
            raise TerrainFormatError("Y admission window overflows signed byte")
        struct.pack_into("<3h", output, cell.offset, *n)
        for offset, value in zip((8, 14, 20), values, strict=True):
            struct.pack_into("<h", output, cell.offset+offset, value)
        struct.pack_into("<2b", output, cell.offset+28, lower, span)
        changes.append({**cell.report(), "new_vertices_stored": vertices, "new_normal": n,
                        "new_y_window": [lower, span]})
    return bytes(output), changes


def mesh_groups(raw, reference):
    """Read every group through 0xffff with signed counts and bounded indices.

    The original triangle/quad tails advance 12/16 bytes regardless of the
    tag's material branch. Other tag fields and every face word stay opaque.
    """
    payload = reference.payload
    cursor = payload.vertices_offset+payload.vertex_count*12
    groups = []
    while True:
        if cursor < 0 or cursor > len(raw)-2:
            raise DatFormatError("mesh stream lacks a bounded terminator")
        tag = struct.unpack_from("<H", raw, cursor)[0]
        if tag == 0xffff:
            return tuple(groups), cursor
        if cursor > len(raw)-4:
            raise DatFormatError("truncated mesh group header")
        count = struct.unpack_from("<h", raw, cursor+2)[0]
        if count < 0:
            raise DatFormatError("negative mesh face count is outside this reader's scope")
        arity = 3 if tag & 1 else 4
        end = cursor+4+count*arity*4
        if end > len(raw):
            raise DatFormatError("mesh faces exceed file bounds")
        faces = []
        for i in range(count):
            offset = cursor+4+i*arity*4
            words = struct.unpack_from("<"+"H"*(arity*2), raw, offset)
            indices = words[:arity]
            if any(v % 12 or v >= payload.vertex_count*12 for v in indices):
                raise DatFormatError("mesh face selects an invalid vertex byte offset")
            faces.append({"index": i, "offset": offset, "vertex_indices": tuple(v//12 for v in indices),
                          "field_words": words[arity:]})
        groups.append({"offset": cursor, "tag": tag, "faces": faces})
        cursor = end


def point_segment_distance2(p, a, b):
    length2 = sum((b[i]-a[i])**2 for i in (0, 1))
    dot = sum((p[i]-a[i])*(b[i]-a[i]) for i in (0, 1))
    if not length2 or dot <= 0:
        return sum((p[i]-a[i])**2 for i in (0, 1))
    if dot >= length2:
        return sum((p[i]-b[i])**2 for i in (0, 1))
    return Fraction(orient(a, b, p)**2, length2)


def polygons_near(a, b, margin=32):
    if any(max(p[i] for p in a)+margin < min(p[i] for p in b) or
           max(p[i] for p in b)+margin < min(p[i] for p in a) for i in (0, 1)):
        return False
    if polygons_touch(a, b):
        return True
    return any(point_segment_distance2(p, poly[i], poly[(i+1) % len(poly)]) <= margin*margin
               for points, poly in ((a, b), (b, a)) for p in points for i in range(len(poly)))


def render_census(dat, footprint, *, transformed=None, excluded=()):
    meshes, vertices, unresolved = [], [], []
    transformed = transformed or {}
    for section in ("primary", "secondary"):
        for ref in dat.static_mesh_references(section):
            key = (section, ref.record_index)
            if key in excluded:
                continue
            groups, end = mesh_groups(dat.data, ref)
            rotation = struct.unpack_from("<3h", dat.data, ref.object_offset+12)
            if (rotation != (0, 0, 0) or dat.data[ref.object_offset+19] & 31) and key not in transformed:
                unresolved.append({"section": section, "record": ref.record_index, "rotation": rotation})
                continue
            origin = struct.unpack_from("<3i", dat.data, ref.object_offset)
            xyz = transformed.get(key) or [tuple(origin[i]+(v.component_00, v.component_02, v.component_04)[i] for i in range(3)) for v in ref.payload.vertices]
            faces = []
            used = set()
            for group in groups:
                for face in group["faces"]:
                    poly = [(xyz[i][0], xyz[i][2]) for i in face["vertex_indices"]]
                    if any(polygons_near(poly, tri) for tri in footprint):
                        faces.append({**face, "group_offset": group["offset"], "tag": group["tag"],
                                      "exact_footprint_overlap": any(polygons_touch(poly, tri) for tri in footprint)})
                        used.update(face["vertex_indices"])
            if not faces:
                continue
            meshes.append({"section": section, "record": ref.record_index, "record_offset": ref.record_offset,
                           "object_offset": ref.object_offset, "geometry_offset": ref.geometry_offset,
                           "terminator_offset": end, "total_groups": len(groups), "touching_faces": faces})
            for i in sorted(used):
                v = ref.payload.vertices[i]
                vertices.append({"section": section, "record": ref.record_index, "vertex": i,
                                 "offset": v.offset, "xyz_stored": xyz[i],
                                 "inside_footprint": any(contains(tri, (xyz[i][0], xyz[i][2])) for tri in footprint)})
    duplicates = defaultdict(list)
    for row in vertices:
        duplicates[tuple(row["xyz_stored"])].append({k: row[k] for k in ("section", "record", "vertex", "offset")})
    return {"meshes": meshes, "vertices": vertices,
            "duplicate_vertices": [{"xyz_stored": xyz, "references": refs} for xyz, refs in sorted(duplicates.items()) if len(refs) > 1],
            "unresolved_rotated_references": unresolved,
            "scope": "complete type-0x41 static streams; exact overlap marked separately from 32-stored-unit correspondence margin; other dispatches are not inferred to be ground"}


def displacement_at(point, incident, vertex, dy):
    values = []
    for cell in incident:
        tri = cell.footprint
        if contains(tri, point):
            i = cell.vertices.index(vertex)
            weight = Fraction(orient(tri[(i+1) % 3], tri[(i+2) % 3], point),
                              orient(tri[(i+1) % 3], tri[(i+2) % 3], tri[i]))
            values.append(weight*dy)
    if values and max(values)-min(values) != 0:
        raise TerrainFormatError("incident triangles disagree on displacement")
    return round(values[0]) if values else 0


def paired_visual(raw, incident, vertex, dy, records=(160, 213, 280)):
    """Fixed zero-rotation ground pairing; preserve XYZ duplicates and attrs.

    A continuous piecewise-linear displacement is sampled at existing vertices.
    Different render triangulation and native skin offsets remain explicit.
    """
    dat = LevelDat.parse(raw)
    output = bytearray(raw)
    edits = []
    for ref in dat.static_mesh_references("primary"):
        if ref.record_index not in records:
            continue
        if struct.unpack_from("<3h", raw, ref.object_offset+12) != (0, 0, 0):
            raise DatFormatError("visual pairing requires zero object rotation")
        origin = struct.unpack_from("<3i", raw, ref.object_offset)
        mesh_groups(raw, ref)
        for v in ref.payload.vertices:
            xyz = (origin[0]+v.component_00, origin[1]+v.component_02, origin[2]+v.component_04)
            delta = displacement_at((xyz[0], xyz[2]), incident, vertex, dy)
            if not delta:
                continue
            new = v.component_02+delta
            if not -32768 <= new <= 32767:
                raise DatFormatError("visual Y overflows int16")
            struct.pack_into("<h", output, v.offset+2, new)
            edits.append({"section": "primary", "record": ref.record_index, "vertex": v.index,
                          "field_offset": v.offset+2, "old": v.component_02, "new": new,
                          "xyz_stored": xyz, "displacement_stored": delta})
    return bytes(output), edits
