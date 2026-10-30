"""Mapped Anthill scenery, EXP-20260908-019 and EXP-20260909-001.

The berry is two scene records: a leaf mesh and 21 camera-facing sprite groups.
004498F0 dispatch 0x0A calls 00454B70, whose source is a count of int32 XYZ
centers followed by a count and 44-byte quads for each center. Original bytes
are retained, including UV/color/material words. This is a bounded importer,
not a replacement sprite renderer.

The berry blocks through Level01 barrier180 points24..48, not a top surface.
Those native contour segments are retained; a straight closing segment replaces
the original connection to the outer level boundary for freestanding placement.
"""
from dataclasses import dataclass, replace
import math
import struct

from .terrain_all import TerrainAll
from .terrain_barriers import BarrierPayload, MAGIC, SENTINEL
from .terrain_floor_patch import segments_touch
from .terrain_foliage import decode_mesh
from .terrain_scenery import (MAX_BYTES, MAX_SCENES, MAX_SOURCES, digest,
                              immutable, integer, vector, read_mesh,
                              scene_pointer_fields, translated)

ORIGINAL_DAT = '786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53'
ORIGINAL_TERRAIN = '62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868'
ASSETS = ('berry.red', 'flower.tall', 'flower.short', 'marker.end-of-stage', 'statue.leaf')
# Exact primary-scene indices and geometry offsets in ORIGINAL_DAT.
MESH_DONORS = {'flower.tall': (90, 207900), 'flower.short': (91, 207900),
               'marker.end-of-stage': (82, 211780)}
BERRY_ANCHOR = (-6392, -2639, 8563)


@dataclass(frozen=True)
class SpriteGroup:
    center: tuple[int, int, int]
    quads: tuple[bytes, ...]


def read_sprites(data, offset=0):
    """Bounds-checked 00454B70 source; return groups and the exact extent.

    The 256-center/1024-total-quad limits bound this authoring path. They are
    not engine limits. Unknown quad bytes remain opaque and immutable.
    """
    immutable(data)
    integer(offset, 0, len(data)-4, 'sprite offset')
    count = struct.unpack_from('<i', data, offset)[0]
    integer(count, 1, min(256, (len(data)-offset-4)//12), 'sprite center count')
    cursor = offset+4+12*count
    result = []; total = 0
    for i in range(count):
        if cursor > len(data)-4:
            raise ValueError('Truncated sprite group count')
        n = struct.unpack_from('<i', data, cursor)[0]; cursor += 4
        integer(n, 1, min(256, (len(data)-cursor)//44), 'sprite quad count')
        total += n
        if total > 1024:
            raise ValueError('Sprite quad budget exceeded')
        center = struct.unpack_from('<3i', data, offset+4+12*i)
        # Reject impossible authoring extents without assigning unknown fields.
        if any(abs(v) > 32767 for v in center):
            raise ValueError('Sprite center exceeds local authoring range')
        result.append(SpriteGroup(center, tuple(data[p:p+44] for p in range(cursor, cursor+44*n, 44))))
        cursor += 44*n
    return tuple(result), cursor


@dataclass(frozen=True)
class PropVisual:
    scene: bytes
    object: bytes
    geometry: bytes

    @property
    def sprite(self):
        return struct.unpack_from('<H', self.scene, 14)[0] == 0x1a

    def validate(self):
        immutable(self.scene, 20); immutable(self.object, 32); immutable(self.geometry)
        flag = struct.unpack_from('<H', self.scene, 14)[0]
        if flag not in (0x19, 0x1a, 0x49) or struct.unpack_from('<h', self.scene, 12)[0] <= 0:
            raise ValueError('Unsupported Anthill prop scene')
        if any(s <= 0 for s in struct.unpack_from('<3h', self.object, 18)):
            raise ValueError('Prop requires positive native scale')
        if self.object[25] & 31 not in ((0,) if self.sprite else (0, 14)):
            raise ValueError('Unsupported prop animation selector')
        if self.sprite:
            _, end = read_sprites(self.geometry)
            if end != len(self.geometry):
                raise ValueError('Sprite template has trailing bytes')
        else:
            if read_mesh(self.geometry, 0) != self.geometry:
                raise ValueError('Mesh template has trailing bytes')
            _, groups = decode_mesh(self.geometry)
            if not any(f for _, f in groups) or any(tag not in
                    (0x60, 0x62, 0x8064, 0x8066, 0x360, 0x8362, 0x8364, 0x8366,
                     0x160, 0x8161, 0x8162, 0x8163, 0x8164, 0x8166,
                     # Original Training flora 120/150/180 (EXP-20260911-004).
                     0x8061, 0x8062, 0x262, 0x8263, 0x8266,
                     # Training gate: City grain mapped to page21 (EXP009).
                     0x1561,
                     # Cliffside meadow: page21 opaque ground / keyed grass.
                     0x1560, 0x9564,
                     # Cliffside ripple atlas on reserved page22.
                     0x1661,
                     # Training garden polish (EXP-20261002-001): page 4, as Training's
                     # own secondary meshes use it (opaque 0x460, keyed quads 0x8466).
                     0x460, 0x8466)
                    for tag, _ in groups):
                raise ValueError('Unsupported Anthill prop material')


def prop_visuals(dat, asset):
    immutable(dat)
    if digest(dat) != ORIGINAL_DAT or not isinstance(asset, str) or asset not in ASSETS:
        raise ValueError('Expected mapped original Anthill prop')
    if asset == 'statue.leaf':
        from .leaf_statue import visual
        return (visual(dat),)
    d, _ = scene_pointer_fields(dat)
    donors = ((65, 188988), (66, 277584)) if asset == 'berry.red' else (MESH_DONORS[asset],)
    visuals = []
    for i, geometry in donors:
        r = d.primary_records[i]; o = r.payload_offset_candidate
        if struct.unpack_from('<I', dat, o+28)[0] != geometry:
            raise ValueError('Prop geometry locator changed')
        if i == 66:
            _, end = read_sprites(dat, geometry); raw = dat[geometry:end]
        else:
            raw = read_mesh(dat, geometry)
        v = PropVisual(dat[r.offset:r.offset+20], dat[o:o+32], raw)
        v.validate(); visuals.append(v)
    return tuple(visuals)


def prop_anchor(dat, asset):
    visuals = prop_visuals(dat, asset)
    if asset == 'statue.leaf':
        # Lowest foot below the central yellow base. A curling side stem
        # extends farther down; using that as the pivot would suspend the base.
        return (4392, -3862, -3563)
    return BERRY_ANCHOR if asset == 'berry.red' else struct.unpack_from('<3i', visuals[0].object)


def append_visual(dat, visual, delta):
    """One native object, sharing only an exact same-dispatch geometry extent."""
    if not isinstance(visual, PropVisual):
        raise ValueError('Expected mapped prop visual')
    visual.validate(); delta = vector(delta)
    d, fields = scene_pointer_fields(dat)
    integer(len(d.primary_records)+len(d.secondary_records)+1, 1, MAX_SCENES, 'scene count')
    shared = None
    for record in (*d.primary_records, *d.secondary_records):
        if record.flags != struct.unpack_from('<H', visual.scene, 14)[0]:
            continue
        ptr = struct.unpack_from('<I', dat, record.payload_offset_candidate+28)[0]
        if dat[ptr:ptr+len(visual.geometry)] != visual.geometry:
            continue
        end = read_sprites(dat, ptr)[1] if visual.sprite else ptr+len(read_mesh(dat, ptr))
        if end-ptr == len(visual.geometry):
            shared = ptr; break
    insertion = d.primary_sentinel_offset; growth = 20
    end = len(dat)-4+growth; pad = (-end) % 4; obj = end+pad
    addition = visual.geometry if shared is None else b''
    geometry = obj+32 if shared is None else shared+growth
    padding = (-len(addition)) % 4; tail = pad+32+len(addition)+padding
    integer(len(dat)+growth+tail, 4, MAX_BYTES, 'expanded prop DAT')
    scene = bytearray(visual.scene); object_data = bytearray(visual.object)
    struct.pack_into('<3i', scene, 0, *translated(scene, 0, delta))
    struct.pack_into('<I', scene, 16, obj)
    struct.pack_into('<3i', object_data, 0, *translated(object_data, 0, delta))
    struct.pack_into('<I', object_data, 28, geometry)
    footer = -1 if d.final_dword == -1 else d.final_dword+tail
    out = bytearray(dat[:insertion]+scene+dat[insertion:-4]+bytes(pad)+object_data+
                    addition+bytes(padding)+struct.pack('<i', footer))
    for f in fields:
        struct.pack_into('<I', out, f+(growth if f >= insertion else 0),
                         struct.unpack_from('<I', dat, f)[0]+growth)
    result = bytes(out); scene_pointer_fields(result)
    return result, dict(scene_index=len(d.primary_records), object_offset=obj,
        geometry_offset=geometry, geometry_bytes=len(visual.geometry), geometry_sha256=digest(visual.geometry),
        geometry_reused=shared is not None, sprite=visual.sprite,
        animation_selector=visual.object[25] & 31, translation_stored=delta,
        dat_sha256=digest(result))


def berry_outline(original):
    immutable(original)
    if digest(original) != ORIGINAL_TERRAIN:
        raise ValueError('Expected original Anthill terrain')
    strip = BarrierPayload.from_terrain(TerrainAll.parse(original), 180)
    points = tuple((p.x, p.z) for p in strip.points[24:49])
    return points+(points[0],)


def obstacle_payload(points):
    """A closed, clockwise native barrier; no top or Y plane is generated."""
    if not isinstance(points, (tuple, list)) or not 4 <= len(points) <= 37:
        raise ValueError('Expected bounded closed obstacle')
    checked = []
    for p in points:
        if not isinstance(p, (tuple, list)) or len(p) != 2:
            raise ValueError('Obstacle points need X/Z')
        checked.append(tuple(integer(v, -0x4000000, 0x3ffffff, 'obstacle coordinate') for v in p))
    points = tuple(checked)
    if points[0] != points[-1] or len(set(points[:-1])) != len(points)-1:
        raise ValueError('Obstacle must be closed and nonrepeating')
    segments = tuple(zip(points, points[1:]))
    if sum(a[0]*b[1]-b[0]*a[1] for a, b in segments) >= 0:
        raise ValueError('Obstacle must keep clockwise native winding')
    for i, (a, b) in enumerate(segments):
        if max(abs(a[k]-b[k]) for k in range(2)) > 8000:
            raise ValueError('Obstacle segment too long')
        for j, (c, d) in enumerate(segments):
            if j <= i+1 or (i == 0 and j == len(segments)-1): continue
            if segments_touch(a, b, c, d):
                raise ValueError('Obstacle intersects itself')
    out = bytearray(struct.pack('<IHH', MAGIC, len(segments), 0)+
                    b''.join(struct.pack('<3i', x, 0, z) for x, z in points))
    for first in range(0, len(segments), 16):
        if len(segments)-first < 16:
            struct.pack_into('<i', out, 12+12*first, SENTINEL)
        else:
            xs, zs = zip(*points[first:first+17])
            for j, value in enumerate((min(xs), max(xs)-min(xs), min(zs), max(zs)-min(zs))):
                struct.pack_into('<i', out, 12+12*(first+j), value)
    parsed = BarrierPayload.parse(bytes(out))
    if not all(parsed.bounds_cover_points(b) for b in parsed.blocks):
        raise ValueError('Obstacle bounds do not contain its points')
    return bytes(out)


def append_berry_barrier(terrain, original, delta):
    immutable(terrain); delta = vector(delta); t = TerrainAll.parse(terrain)
    if len(t.records) >= MAX_SOURCES:
        raise ValueError('Collision source budget exceeded')
    source = TerrainAll.parse(original)
    outline = berry_outline(original)
    points = tuple((x+delta[0], z+delta[2]) for x, z in outline)
    payload = obstacle_payload(points)
    record = bytearray(source.records[180].raw)
    struct.pack_into('<I', record, 0, len(payload)//2)
    directory = t.directory_offset+len(payload)
    records_end = t.directory_offset+4+76*len(t.records)
    out = (struct.pack('<I', directory//2)+terrain[4:t.directory_offset]+payload+
           struct.pack('<I', len(t.records)+1)+terrain[t.directory_offset+4:records_end]+record+t.suffix)
    if len(out) > MAX_BYTES:
        raise ValueError('Expanded terrain budget exceeded')
    checked = TerrainAll.parse(out); strip = BarrierPayload.from_terrain(checked, len(t.records))
    return out, dict(source_index=len(t.records), points_stored=points,
        payload_bytes=len(payload), payload_sha256=digest(payload), segment_count=strip.segment_count,
        native_source=180, retained_segments=[24, 47], authored_closing_segment=True,
        collision='X/Z blocking only; no top surface or height limit')


def turn_end_marker(visual, heading):
    """Relative upright yaw; retain mesh, scale and opaque object fields.

    PC object+14 is the Y Euler word consumed by 00463C80 (EXP-20260910-012).
    Rotate the off-center culling sphere around the same stem origin.
    """
    visual.validate(); integer(heading, 0, 4095, 'marker heading')
    angles = struct.unpack_from('<3h', visual.object, 12)
    if visual.sprite or angles[0] or angles[2] or visual.object[25] & 31:
        raise ValueError('Heading requires an upright static mesh')
    if not heading: return visual
    obj = bytearray(visual.object); scene = bytearray(visual.scene)
    struct.pack_into('<h', obj, 14, (angles[1]+heading) % 4096)
    origin = struct.unpack_from('<3i', obj)
    center = struct.unpack_from('<3i', scene)
    x, z = center[0]-origin[0], center[2]-origin[2]
    angle = heading*math.tau/4096; c, s = math.cos(angle), math.sin(angle)
    struct.pack_into('<3i', scene, 0, *vector((origin[0]+round(c*x+s*z),
        center[1], origin[2]+round(c*z-s*x))))
    return replace(visual, object=bytes(obj), scene=bytes(scene))


def append_prop(dat, terrain, original_dat, original_terrain, asset, position, *, heading=0, level_base=False):
    integer(heading, 0, 4095, 'prop heading')
    if type(level_base) is not bool or (level_base and asset != 'statue.leaf'):
        raise ValueError('Only the leaf statue supports boolean base leveling')
    if heading and asset not in ('marker.end-of-stage', 'statue.leaf'):
        raise ValueError('Only the leaf statue and the end-of-stage marker support an authored heading')
    position = vector(position); visuals = prop_visuals(original_dat, asset)
    anchor = prop_anchor(original_dat, asset)
    delta = tuple(position[k]-anchor[k] for k in range(3)); rows = []
    for visual in visuals:
        if level_base:
            from .leaf_statue import level_visual
            visual = level_visual(visual, anchor)
        if heading:
            if asset == 'statue.leaf':
                from .leaf_statue import turn_visual
                visual = turn_visual(visual, heading, anchor)
            else:
                visual = turn_end_marker(visual, heading)
        dat, row = append_visual(dat, visual, delta); rows.append(row)
    collision = None
    if asset == 'berry.red':
        terrain, collision = append_berry_barrier(terrain, original_terrain, delta)
    shell = None
    if asset == 'statue.leaf':
        from .leaf_statue import append_shell
        terrain, shell = append_shell(terrain, original_terrain, delta, heading=heading, anchor=anchor, level_base=level_base)
    return dat, terrain, dict(asset=asset, position_stored=position, anchor_stored=anchor,
        heading=heading, level_base=level_base,
        translation_stored=delta, visuals=rows, barrier=collision, shell=shell,
        collision=('original finite triangle shell' if shell else 'blocking without top' if collision else
                   'none authored; native static scenery' if asset == 'marker.end-of-stage' else
                   'none; native animated scenery'))
