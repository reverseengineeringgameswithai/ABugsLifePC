"""Original Anthill leaf structure and its separate shell, EXP-20260915-008.

Scene109 is one317-vertex mesh, including the leaf, stems and yellow base.
Source89 is its expanded collision shell. Original bytes are caller supplied.
The24-byte unscaled object is represented by a32-byte unit-scale object:
native004498F0 produces identical transform and0045A7F0 inputs (nine contexts).
"""
from dataclasses import replace
import math
import struct

from .terrain_all import TerrainAll
from .terrain_scenery import (MAX_BYTES, MAX_SOURCES, digest, immutable, integer,
                              read_mesh, scene_pointer_fields, translated, vector)

# EXP-20260916-017: original yellow base's twelve upper rim vertices fit
# Y = -145.408769 - .0856621438 X - .126638309 Z (max residual .555).
# Undo that intrinsic 8.6926-degree tilt before applying authored upright yaw.
BASE_SLOPES = (-.0856621438, -.126638309)


def level_point(point):
    """Rigid rotation taking the measured base normal onto positive PC Y."""
    a, b = BASE_SLOPES
    length = math.sqrt(1+a*a+b*b)
    nx, ny, nz = -a/length, 1/length, -b/length
    sine = math.hypot(nx, nz)
    axis = (-nz/sine, 0, nx/sine)
    x, y, z = point
    cross = (-axis[2]*y, axis[2]*x-axis[0]*z, axis[0]*y)
    dot = sum(axis[k]*point[k] for k in range(3))
    return tuple(round(ny*point[k]+sine*cross[k]+(1-ny)*axis[k]*dot) for k in range(3))


def level_visual(source, anchor):
    """Level this instance by changing only XYZ, preserving original artwork."""
    from .terrain_foliage import decode_mesh
    source.validate(); anchor = vector(anchor)
    vertices, _ = decode_mesh(source.geometry)
    origin = struct.unpack_from('<3i', source.object)
    geometry = bytearray(source.geometry)
    for i, vertex in enumerate(vertices):
        local = struct.unpack_from('<3h', vertex)
        point = level_point(tuple(origin[k]+local[k]-anchor[k] for k in range(3)))
        for word in point: integer(word, -32768, 32767, 'leveled leaf vertex')
        struct.pack_into('<3h', geometry, 4+12*i, *point)
    scene, obj = bytearray(source.scene), bytearray(source.object)
    center = struct.unpack_from('<3i', scene)
    offset = level_point(tuple(center[k]-anchor[k] for k in range(3)))
    struct.pack_into('<3i', scene, 0, *vector(tuple(anchor[k]+offset[k] for k in range(3))))
    struct.pack_into('<3i', obj, 0, *anchor)
    result = replace(source, scene=bytes(scene), object=bytes(obj), geometry=bytes(geometry))
    result.validate()
    return result


def leveled_preview(original):
    from .terrain_foliage import decode_mesh
    source = level_visual(visual(original), (4392, -3862, -3563))
    vertices, groups = decode_mesh(source.geometry)
    return dict(id='statue.leaf', kind='decoration',
        vertices=[dict(position=list(struct.unpack_from('<3h', v)), rgb=list(v[8:11]),
                       opaque=[v[6], v[7], v[11]]) for v in vertices],
        faces=[dict(tag=tag, indices=list(ids), uv=list(uv)) for tag, fs in groups for ids, uv in fs])


def visual(original):
    from .terrain_anthill_props import ORIGINAL_DAT, PropVisual
    immutable(original)
    if digest(original) != ORIGINAL_DAT:
        raise ValueError('Leaf statue requires the original Anthill DAT')
    parsed, _ = scene_pointer_fields(original)
    row = parsed.primary_records[109]
    if (row.offset, row.flags, row.payload_offset_candidate) != (7560, 0x41, 20632):
        raise ValueError('Leaf statue scene locator changed')
    obj = original[20632:20656]
    if (struct.unpack_from('<3h', obj, 12) != (0, 0, 0) or obj[19] & 31
            or struct.unpack_from('<I', obj, 20)[0] != 264144):
        raise ValueError('Leaf statue object differs')
    scene = bytearray(original[7560:7580])
    struct.pack_into('<H', scene, 14, 0x49)
    # Preserve both native control bytes. The scaled layout adds scales and
    # two padding bytes; geometry/material/UV/vertex bytes are untouched.
    scaled = obj[:18]+struct.pack('<3h', 4096, 4096, 4096)+obj[18:20]+b'\0\0'+obj[20:24]
    result = PropVisual(bytes(scene), scaled, read_mesh(original, 264144))
    result.validate()
    return result


def yaw(point, heading):
    """PC upright Euler Y: X'=cos*X+sin*Z, Z'=cos*Z-sin*X.

    Native00463C80 comparisons in test_leaf_statue bound fixed-point error.
    """
    angle = heading*math.tau/4096
    c, s = math.cos(angle), math.sin(angle)
    x, y, z = point
    return (round(c*x+s*z), y, round(c*z-s*x))


def turn_visual(visual, heading, anchor):
    """Rotate the intact mesh and its culling center about the central foot."""
    from .terrain_anthill_props import turn_end_marker
    anchor = vector(anchor)
    turned = turn_end_marker(visual, heading)
    if not heading: return visual
    scene, obj = bytearray(turned.scene), bytearray(turned.object)
    for source, target in ((visual.scene, scene), (visual.object, obj)):
        point = struct.unpack_from('<3i', source)
        offset = yaw(tuple(point[k]-anchor[k] for k in range(3)), heading)
        struct.pack_into('<3i', target, 0, *vector(tuple(anchor[k]+offset[k] for k in range(3))))
    return replace(turned, scene=bytes(scene), object=bytes(obj))


def turn_shell(payload, base, anchor, heading, *, level_base=False):
    """Turn the original226 shell triangles; retain grouping and opaque tail.

    Recompute corners, edges, normals and admission windows. Upright yaw
    retains Y; optional base leveling turns Y too. Group markers/counts,
    source controls, terminator and trailer survive.
    No render triangles are used to construct collision.
    """
    output = bytearray(payload.raw)
    def rotate(point):
        return yaw(level_point(point) if level_base else point, heading)
    for group in payload.groups:
        corners = []
        for cell in group.cells:
            w = cell.words
            triangle = [rotate(tuple(base[k]+w[3+k]+edge[k]-anchor[k] for k in range(3)))
                        for edge in ((0, 0, 0), w[6:9], w[9:12])]
            corners.extend(triangle)
            a, b, c = triangle
            normal = rotate(w[:3])
            lo = [min(p[k] for p in triangle) for k in range(3)]
            hi = [max(p[k] for p in triangle) for k in range(3)]
            words = (*normal, *a, *(b[k]-a[k] for k in range(3)),
                     *(c[k]-a[k] for k in range(3)), lo[0], hi[0]-lo[0])
            windows = []
            for axis in (1, 2):
                low = (lo[axis]-a[axis])//64
                span = max(1, -(-(hi[axis]-a[axis]-64*low)//64))
                windows.extend((low, span))
            for word in words: integer(word, -32768, 32767, 'rotated shell word')
            for window in windows: integer(window, -128, 127, 'rotated shell window')
            struct.pack_into('<14h4b', output, cell.offset-payload.offset, *words, *windows)
        bounds = tuple(v for axis in (0, 2)
                       for v in (min(p[axis] for p in corners),
                                 max(p[axis] for p in corners)-min(p[axis] for p in corners)))
        for bound in bounds: integer(bound, -32768, 32767, 'rotated shell group bound')
        struct.pack_into('<4h', output, group.offset-payload.offset+4, *bounds)
    return bytes(output)


def append_shell(terrain, original, delta, *, heading=0, anchor=(4392, -3862, -3563), level_base=False):
    from .terrain_anthill_props import ORIGINAL_TERRAIN
    immutable(terrain); immutable(original); delta = vector(delta)
    integer(heading, 0, 4095, 'leaf statue heading'); anchor = vector(anchor)
    if type(level_base) is not bool: raise ValueError('Leaf base leveling must be boolean')
    if digest(original) != ORIGINAL_TERRAIN:
        raise ValueError('Leaf statue requires the original Anthill collision')
    source = TerrainAll.parse(original)
    donor = source.records[89]; payload = source.collision_payload(89)
    if ((donor.offset, donor.payload_offset, donor.field_10, donor.field_44, donor.field_46)
            != (229340, 7652, 6, -1, 0)
            or sum(g.cell_count for g in payload.groups) != 226):
        raise ValueError('Leaf statue collision locator changed')
    target = TerrainAll.parse(terrain)
    integer(len(target.records)+1, 1, MAX_SOURCES, 'leaf statue collision sources')
    record = bytearray(donor.raw)
    shell = payload.raw
    if heading or level_base:
        base = (donor.component_x, donor.component_y, donor.component_z)
        shell = turn_shell(payload, base, anchor, heading, level_base=level_base)
        struct.pack_into('<3i', record, 4, *vector(tuple(anchor[k]+delta[k] for k in range(3))))
    else:
        struct.pack_into('<3i', record, 4, *translated(record, 4, delta))
    directory = target.directory_offset+len(shell)
    out = (struct.pack('<I', directory//2)+terrain[4:target.directory_offset]+shell+
           struct.pack('<I', len(target.records)+1)+b''.join(r.raw for r in target.records)+
           bytes(record)+target.suffix)
    integer(len(out), 4, MAX_BYTES, 'leaf statue terrain size')
    TerrainAll.parse(out).collision_payload(len(target.records))
    return out, dict(source_index=len(target.records), donor_source=89,
        donor_record_offset=donor.offset, donor_payload_offset=donor.payload_offset,
        origin_stored=struct.unpack_from('<3i', record, 4), triangles=226,
        payload_sha256=digest(shell), payload_bytes=len(shell),
        translation_stored=delta, original_payload_exact=not (heading or level_base), heading=heading,
        level_base=level_base,
        original_triangles_retained=True)
