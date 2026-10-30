"""Bounded EXP-004 ramp/box composition, not a general level mesh writer."""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import math
import struct

from .level_dat import LevelDat
from .terrain_all import TerrainAll

BANKED_TERRAIN_SHA = "26f3e0235533419a80b2a0eff18f423fadc20617a6c2ed2be445abeae87b35d5"
BANKED_DAT_SHA = "572d244f1cc053ef29d2c343e4311a6ff20237c2259c5e84867bade53d57c247"
DECK = (4000, 8300, 13000, 18100, -3200)
BOX = (5100, 5750, 15550, 16250, -3392)
RAMP_FOOT_X = 7150
# EXP-003 checked every original command group through this mesh's terminator.
# Unlike the older first-group-only bound (1336), this is the complete known span.
MESH_START, MESH_CAPACITY = 113136, 2234


def digest(data):
    return hashlib.sha256(data).hexdigest()


def integer(value, low, high, name):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} outside established integer bounds")
    return value


def vector(value):
    if len(value) != 3:
        raise ValueError("three coordinates required")
    return tuple(integer(v, -(2**31), 2**31-1, "coordinate") for v in value)


def normal(triangle):
    if len(triangle) != 3:
        raise ValueError("three vertices required")
    a, b, c = [vector(v) for v in triangle]
    u, v = [b[i]-a[i] for i in range(3)], [c[i]-a[i] for i in range(3)]
    cross = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
    length = math.sqrt(sum(x*x for x in cross))
    if not length:
        raise ValueError("degenerate triangle")
    # Same directed 16384-scale construction as the banked deck writer.
    return tuple(round(-x*16384/length) for x in cross)


def encode_group(triangle, origin):
    """One established marker-1 group and its 32-byte cell, with checked fields."""
    n = normal(triangle)
    origin = vector(origin)
    local = [tuple(v[i]-origin[i] for i in range(3)) for v in triangle]
    a, b, c = local
    lo = [min(v[i] for v in local) for i in range(3)]
    hi = [max(v[i] for v in local) for i in range(3)]
    windows = []
    for axis in (1, 2):
        base = (lo[axis]-a[axis])//64
        span = max(1, -(-(hi[axis]-a[axis]-64*base)//64))
        windows.extend((base, span))
    words = (*n, *a, *(b[i]-a[i] for i in range(3)),
             *(c[i]-a[i] for i in range(3)), lo[0], hi[0]-lo[0])
    header = (1, 1, lo[0], hi[0]-lo[0], lo[2], hi[2]-lo[2])
    for v in (*header, *words):
        integer(v, -32768, 32767, "cell/header word")
    for v in windows:
        integer(v, -128, 127, "relative admission window")
    return struct.pack("<6h14h4b", *header, *words, *windows)


def quad(x0, x1, z0, z1, y):
    return [(x0,y,z0), (x1,y,z0), (x1,y,z1), (x0,y,z1)]


def collision_surfaces():
    deck = quad(*DECK[:4], DECK[4]-96)
    top = quad(*BOX[:4], BOX[4]-96)
    bottom = quad(*BOX[:4], DECK[4]+96)
    ramp = [top[1], (RAMP_FOOT_X,DECK[4]-96,BOX[2]),
            (RAMP_FOOT_X,DECK[4]-96,BOX[3]), top[2]]
    north = [top[0], top[1], ramp[1],
             (RAMP_FOOT_X,DECK[4]+96,BOX[2]), bottom[0]]
    south = list(reversed([top[3], top[2], ramp[2],
                          (RAMP_FOOT_X,DECK[4]+96,BOX[3]), bottom[3]]))
    west = [top[3], bottom[3], bottom[0], top[0]]
    rows = []
    for label, points in (("deck",deck), ("top",top), ("ramp",ramp), ("west_wall",west)):
        for ids in ((0,2,1), (0,3,2)):
            rows.append((label, [points[i] for i in ids]))
    for label, points in (("north_wall",north), ("south_wall",south)):
        for i in range(1, len(points)-1):
            rows.append((label, [points[0], points[i], points[i+1]]))
    return rows


def interpolate(corners, u, v):
    weights = ((1-u)*(1-v), u*(1-v), u*v, (1-u)*v)
    return tuple(round(sum(w*p[k] for w,p in zip(weights,corners)))
                 for k in range(len(corners[0])))


def replace_prefix(data, offset, capacity, prefix):
    integer(offset, 0, len(data), "offset")
    integer(capacity, 0, len(data)-offset, "capacity")
    if len(prefix) > capacity:
        raise ValueError("authored prefix exceeds known allocation")
    return data[:offset]+prefix+data[offset+len(prefix):]


def build(terrain, dat):
    """Compose only the exact banked alternate-4x4 deck/box fixture."""
    if digest(terrain) != BANKED_TERRAIN_SHA or digest(dat) != BANKED_DAT_SHA:
        raise ValueError("expected exact banked alternate-4x4 fixture")
    parsed = TerrainAll.parse(terrain)
    record = parsed.records[99]
    origin = (record.component_x,record.component_y,record.component_z)
    payload, cells = bytearray(), []
    for label, triangle in collision_surfaces():
        group = encode_group(triangle, origin)
        cells.append({"file_offset":record.payload_offset+len(payload)+12,
                      "surface":label, "vertices":triangle, "normal":normal(triangle)})
        payload.extend(group)
    payload.extend(b"\xff\xff")
    terrain_out = replace_prefix(terrain,record.payload_offset,record.payload_size,bytes(payload))

    ref = LevelDat.parse(dat).static_mesh_reference("primary",160)
    if ref.geometry_offset != MESH_START or dat[MESH_START+MESH_CAPACITY-2:MESH_START+MESH_CAPACITY] != b"\xff\xff":
        raise ValueError("complete known mesh allocation changed")
    mesh_origin = struct.unpack_from("<3i",dat,ref.object_offset)
    vertices = []
    for vertex in ref.payload.vertices:
        raw = vertex.to_bytes()
        xyz = tuple(a+b for a,b in zip(struct.unpack_from("<3h",raw),mesh_origin))
        x,y,z = xyz
        if y == DECK[4] and BOX[0] <= x <= BOX[1] and BOX[2] <= z <= BOX[3]:
            x = BOX[0]+round(Fraction((x-BOX[0])*(RAMP_FOOT_X-BOX[0]),BOX[1]-BOX[0]))
        local = (x-mesh_origin[0],y-mesh_origin[1],z-mesh_origin[2])
        vertices.append(struct.pack("<3h",*local)+raw[6:])
    lookup = {v:i for i,v in enumerate(vertices)}
    faces, provenance = [], []
    for index, face in enumerate(ref.payload.faces):
        if index <= 16:  # deck and all sixteen banked alternate top quads
            faces.append(struct.pack("<8H",*face.vertex_byte_offsets,*face.field_words))
            provenance.append({"banked_face":index,"half":None})
            continue
        raw = [vertices[i//12] for i in face.vertex_byte_offsets]
        xyz = [struct.unpack_from("<3h",v) for v in raw]
        if len({v[6:] for v in raw}) != 1:
            raise ValueError("unsupported mixed vertex suffixes")
        uv = [(w&255,w>>8) for w in face.field_words]
        for half in range(2):
            u0,u1 = Fraction(half,2),Fraction(half+1,2)
            offsets,fields = [],[]
            for u,v in ((u0,0),(u1,0),(u1,1),(u0,1)):
                pos = interpolate(xyz,u,v)
                for n in pos:
                    integer(n,-32768,32767,"mesh coordinate")
                value = struct.pack("<3h",*pos)+raw[0][6:]
                if value not in lookup:
                    lookup[value]=len(vertices);vertices.append(value)
                offsets.append(lookup[value]*12)
                tx,ty = interpolate(uv,u,v)
                integer(tx,0,255,"U");integer(ty,0,255,"V")
                fields.append(tx | ty<<8)
            faces.append(struct.pack("<8H",*offsets,*fields))
            provenance.append({"banked_face":index,"half":half})
    mesh = (struct.pack("<i",len(vertices))+b"".join(vertices)
            +struct.pack("<HH",ref.payload.tag,len(faces))+b"".join(faces)+b"\xff\xff")
    dat_out = replace_prefix(dat,MESH_START,MESH_CAPACITY,mesh)
    meta = {"experiment":"EXP-20260905-004","deck":DECK,"box":BOX,
            "ramp_foot_x":RAMP_FOOT_X,"ramp_run_stored":RAMP_FOOT_X-BOX[1],
            "ramp_rise_stored":DECK[4]-BOX[4],"source99_payload_offset":record.payload_offset,
            "source99_replaced_prefix_bytes":len(payload),"mesh160_geometry_offset":MESH_START,
            "mesh160_replaced_prefix_bytes":len(mesh),"known_mesh_capacity":MESH_CAPACITY,
            "capacity_evidence":"EXP-20260905-003 complete original mesh stream",
            "scene_record_offset":ref.record_offset,"object_offset":ref.object_offset,
            "mesh_origin":mesh_origin,"depth_offset":dat[ref.object_offset+18],
            "vertex_count":len(vertices),"face_count":len(faces),"source_faces":provenance,
            "cells":cells,"terrain_sha256":digest(terrain_out),"level_dat_sha256":digest(dat_out),
            "banked_terrain_sha256":digest(terrain),"banked_level_dat_sha256":digest(dat),
            "scope":"Finite composition on the banked elevated deck; not connected to the distant retail landscape."}
    return terrain_out,dat_out,meta
