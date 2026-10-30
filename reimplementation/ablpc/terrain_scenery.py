"""Add independent PC scenery instances, preserving the demonstrated file grammar.

EXP-20260906-014: primary scene insertion and two object-pointer layouts follow
PC relocation stores 0044BD12/21/47/57 and 0044BE70/79/94/9D. The no-op
0044BB50 does not relocate mesh internals. This deliberately rejects indexed,
fixed-record and bit-0x20 variants rather than claiming a general DAT repacker.
Collision copies retain the complete authored shell, not a render-mesh rebuild.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import struct

from .level_dat import LevelDat
from .terrain_all import TerrainAll
from .terrain_foliage import decode_mesh

# EXP-20260928-001: 26-door hub DAT (was 0x120000 for 17 doors). The 8 MiB
# asset arena stress fixture loaded 3094194 DAT/TERRAIN/PLANTTER bytes.
MAX_BYTES = 0x160000
MAX_SCENES = 1536  # EXP-20260914-002 authoring budget; not an engine limit.
MAX_SOURCES = 512


def digest(data):
    return hashlib.sha256(data).hexdigest()


def integer(value, low, high, label):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"invalid {label}")
    return value


def immutable(data, size=None):
    if not isinstance(data, bytes) or size is not None and len(data) != size:
        raise ValueError("expected immutable bytes of the required size")


def vector(value):
    if not isinstance(value, (tuple, list)) or len(value) != 3:
        raise ValueError("expected three stored-unit coordinates")
    return tuple(integer(v, -2**31, 2**31-1, "coordinate") for v in value)


def translated(raw, offset, delta):
    old = struct.unpack_from('<3i', raw, offset)
    return vector(tuple(a+b for a, b in zip(old, delta)))


@dataclass(frozen=True)
class SceneryTemplate:
    """Paired, already-scaled scenery donor. No assets are embedded in source."""
    scene: bytes
    object: bytes
    mesh: bytes
    collision_record: bytes
    collision_payload: bytes

    def validate(self):
        immutable(self.scene, 20)
        immutable(self.object, 32)
        immutable(self.mesh)
        immutable(self.collision_record, 76)
        immutable(self.collision_payload)
        # Only the observed scaled scenery path, no dynamic selected matrices.
        if struct.unpack_from('<H', self.scene, 14)[0] != 0x19:
            raise ValueError("template must use the observed scene 0x19 path")
        if struct.unpack_from('<h', self.scene, 12)[0] <= 0 or self.object[25] & 31:
            raise ValueError("unsupported template bound or runtime matrix")
        if any(v <= 0 for v in struct.unpack_from('<3h', self.object, 18)):
            raise ValueError("template requires positive retained scales")
        _, groups = decode_mesh(self.mesh)
        if not any(faces for _, faces in groups):
            raise ValueError("empty template mesh")
        if any(tag not in (0x60, 0x8064) for tag, _ in groups):
            raise ValueError("unsupported mushroom material command")
        if not 2 <= len(self.collision_payload) <= MAX_BYTES or len(self.collision_payload) % 2:
            raise ValueError("invalid collision payload size")
        r = self.collision_record
        if (struct.unpack_from('<I', r)[0]*2 != len(self.collision_payload)
                or struct.unpack_from('<i', r, 16)[0] != 6
                or struct.unpack_from('<2h', r, 68) != (-1, 0)):
            raise ValueError("template requires an explicit active tag-6 source")
        probe = (struct.pack('<I', (4+len(self.collision_payload))//2)
                 + self.collision_payload + struct.pack('<I', 1) + r)
        payload = TerrainAll.parse(probe).collision_payload(0)
        if not payload.groups or any(g.cell_count <= 0 or g.span_x_units < 0 or g.span_z_units < 0
                                     for g in payload.groups):
            raise ValueError("empty or impossible template collision")


def read_mesh(data, offset):
    """Extract one complete bounded positive mesh, preserving every face word."""
    integer(offset, 0, len(data)-4, "mesh offset")
    count = struct.unpack_from('<i', data, offset)[0]
    integer(count, 1, min(5462, (len(data)-offset-6)//12), "vertex count")
    cursor = offset+4+count*12
    while cursor <= len(data)-2:
        tag = struct.unpack_from('<H', data, cursor)[0]
        if tag == 65535:
            mesh = data[offset:cursor+2]
            decode_mesh(mesh)
            return mesh
        if cursor > len(data)-4:
            break
        count = struct.unpack_from('<h', data, cursor+2)[0]
        stride = 12 if tag & 1 else 16
        integer(count, 0, (len(data)-cursor-4)//stride, "face count")
        cursor += 4+count*stride
    raise ValueError("missing complete mesh terminator")


def mushroom_template(dat, terrain, *, scene_index=344, source_index=147):
    """Extract only mapped OG Level01 donors; callers supply their own files.

    Visual localization is original-PC projection at the saved live camera;
    shell pairing is geometric/contextual and checked by native movement.
    """
    immutable(dat)
    immutable(terrain)
    if digest(dat) != '786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53':
        raise ValueError("expected original Level01 DAT")
    if digest(terrain) != '62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868':
        raise ValueError("expected original Level01 terrain")
    if type(scene_index) is not int or type(source_index) is not int or (scene_index, source_index) not in ((344, 147), (342, 142), (396, 146), (400, 148)):
        raise ValueError("unmapped mushroom pair")
    d, t = LevelDat.parse(dat), TerrainAll.parse(terrain)
    r = d.primary_records[scene_index]
    o = r.payload_offset_candidate
    geometry = struct.unpack_from('<I', dat, o+28)[0]
    if geometry != 179576:
        raise ValueError("mushroom geometry locator changed")
    result = SceneryTemplate(dat[r.offset:r.offset+20], dat[o:o+32],
                             read_mesh(dat, geometry), t.records[source_index].raw,
                             t.collision_payload(source_index).raw)
    result.validate()
    return result


def scene_pointer_fields(data):
    """Known offset fields in the bounded unindexed, unique-object layout."""
    immutable(data)
    if not 4 <= len(data) <= MAX_BYTES:
        raise ValueError("DAT exceeds bounded size")
    d = LevelDat.parse(data)
    if d.fixed_record_count or d.index_table_max != -1:
        raise ValueError("fixed/indexed DAT layouts are unsupported")
    records = (*d.primary_records, *d.secondary_records)
    if len(records) > MAX_SCENES:
        raise ValueError("scene budget exceeded")
    fields, objects = [], []
    for r in records:
        if r.flags & 0x20:
            raise ValueError("extra-pointer scene variant unsupported")
        o = r.payload_offset_candidate
        size = 32 if r.flags & 8 else 24
        if not d.parsed_prefix_end <= o <= len(data)-4-size:
            raise ValueError("object outside payload storage")
        objects.append((o, o+size))
        pointer = o+size-4
        geometry = struct.unpack_from('<I', data, pointer)[0]
        if not d.parsed_prefix_end <= geometry <= len(data)-8:
            raise ValueError("geometry outside payload storage")
        fields.extend((r.offset+16, pointer))
    objects.sort()
    if any(a[1] > b[0] for a, b in zip(objects, objects[1:])):
        raise ValueError("aliased or overlapping objects unsupported")
    if any(a <= struct.unpack_from('<I', data, f)[0] < b
           for f in fields[1::2] for a, b in objects):
        raise ValueError("geometry overlaps object storage")
    if d.final_dword != -1 and not 0x11c <= d.final_dword <= len(data)-d.parsed_prefix_end:
        raise ValueError("invalid end-relative footer")
    return d, tuple(fields)


def matching_mesh_offset(dat, fields, mesh):
    """Reuse only a complete, byte-identical mesh already named by an object.

    Native PC objects already share immutable positive mesh streams. Do not
    scan arbitrary file bytes or reuse a partial/prefix match (EXP-017).
    """
    decode_mesh(mesh)
    for offset in sorted({struct.unpack_from('<I', dat, f)[0] for f in fields[1::2]}):
        if offset <= len(dat)-4-len(mesh) and dat[offset:offset+len(mesh)] == mesh:
            if read_mesh(dat, offset) == mesh:
                return offset
    return None


def append_instances(dat, terrain, template, positions, *, reuse_mesh=False):
    """Append paired scene objects and collision sources at absolute object origins.

    Every old instance remains. New objects share one immutable mesh copy per
    call; reuse_mesh also allows an exact existing stream instead of appending
    another copy. Each object receives its own collision payload/descriptor. Calling
    again on the result adds more instances; no reserved original slot is used.
    Rotation, scale, materials, depth/pass flags and collision clearance stay
    as in the donor. Arbitrary rotation/rescaling and cross-level atlases are
    intentionally not supported. Returned bytes do not alter any live session.
    """
    if not isinstance(template, SceneryTemplate):
        raise ValueError("expected a validated scenery template")
    template.validate()
    if not isinstance(positions, (list, tuple)) or not 1 <= len(positions) <= 64:
        raise ValueError("expected one to 64 placements")
    positions = tuple(vector(p) for p in positions)
    origin = struct.unpack_from('<3i', template.object)
    deltas = tuple(tuple(p[k]-origin[k] for k in range(3)) for p in positions)
    d, fields = scene_pointer_fields(dat)
    immutable(terrain)
    if not 4 <= len(terrain) <= MAX_BYTES:
        raise ValueError("terrain exceeds bounded size")
    t = TerrainAll.parse(terrain)
    n = len(positions)
    if len(d.primary_records)+len(d.secondary_records)+n > MAX_SCENES or len(t.records)+n > MAX_SOURCES:
        raise ValueError("instance budget exceeded")
    insertion, prefix_growth = d.primary_sentinel_offset, 20*n
    # Align appended objects without assuming older appenders made EOF aligned.
    end = len(dat)-4+prefix_growth
    pad = (-end) % 4
    shared = matching_mesh_offset(dat, fields, template.mesh) if reuse_mesh else None
    addition_mesh = template.mesh if shared is None else b''
    object_base = end+pad
    geometry = object_base+32*n if shared is None else shared+prefix_growth
    mesh_pad = (-len(addition_mesh)) % 4
    tail_growth = pad+32*n+len(addition_mesh)+mesh_pad
    if len(dat)+prefix_growth+tail_growth > MAX_BYTES:
        raise ValueError("expanded DAT exceeds bounded size")
    scene_bytes, object_bytes, descriptors = [], [], []
    for i, delta in enumerate(deltas):
        scene, obj, record = bytearray(template.scene), bytearray(template.object), bytearray(template.collision_record)
        struct.pack_into('<3i', scene, 0, *translated(scene, 0, delta))
        struct.pack_into('<I', scene, 16, object_base+32*i)
        struct.pack_into('<3i', obj, 0, *positions[i])
        struct.pack_into('<I', obj, 28, geometry)
        struct.pack_into('<3i', record, 4, *translated(record, 4, delta))
        scene_bytes.append(bytes(scene)); object_bytes.append(bytes(obj)); descriptors.append(bytes(record))
    output = bytearray(dat[:insertion]+b''.join(scene_bytes)+dat[insertion:-4]
                       +bytes(pad)+b''.join(object_bytes)+addition_mesh+bytes(mesh_pad)
                       +struct.pack('<i', -1 if d.final_dword == -1 else d.final_dword+tail_growth))
    for f in fields:
        value = struct.unpack_from('<I', dat, f)[0]
        # Existing targets are all payloads after the insertion boundary.
        struct.pack_into('<I', output, f+(prefix_growth if f >= insertion else 0), value+prefix_growth)
    addition = template.collision_payload*n
    new_directory = t.directory_offset+len(addition)
    records_end = t.directory_offset+4+76*len(t.records)
    collision = (struct.pack('<I', new_directory//2)+terrain[4:t.directory_offset]
                 +addition+struct.pack('<I', len(t.records)+n)
                 +terrain[t.directory_offset+4:records_end]+b''.join(descriptors)+t.suffix)
    if len(collision) > MAX_BYTES:
        raise ValueError("expanded terrain exceeds bounded size")
    result = bytes(output)
    scene_pointer_fields(result)
    TerrainAll.parse(collision)
    return result, collision, {
        'old_primary_count': len(d.primary_records), 'new_primary_count': len(d.primary_records)+n,
        'old_source_count': len(t.records), 'new_source_count': len(t.records)+n,
        'scene_indices': list(range(len(d.primary_records), len(d.primary_records)+n)),
        'source_indices': list(range(len(t.records), len(t.records)+n)),
        'positions_stored': positions, 'translations_stored': deltas,
        'scene_insertion': insertion, 'prefix_growth': prefix_growth,
        'object_offset': object_base, 'geometry_offset': geometry,
        'mesh_sha256': digest(template.mesh), 'mesh_bytes': len(template.mesh),
        'mesh_reused': shared is not None,
        'collision_payload_sha256': digest(template.collision_payload),
        'pointer_fields_rebased': len(fields), 'tail_growth': tail_growth,
        'dat_sha256': digest(result), 'terrain_sha256': digest(collision),
        'scope': 'net-new independent scene objects and collision sources; retained donor transforms/materials/shell; original Level01 texture resources required',
    }
