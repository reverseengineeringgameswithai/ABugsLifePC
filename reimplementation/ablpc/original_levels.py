"""All original PC gameplay levels as Blender reference maps, EXP-20260927-001.

Read-only composition of the bounded DAT/RAW/terrain readers. It extends the
Training importer (EXP-20260909-012) to every masked scene dispatch drawn by
004498F0, every type3F pickup, every RAW type35 creature slot and its 0x102
model packet. Nothing here writes game files.

Engine index -> files is the static 004671D0 rule: 1..10 use LEVELnn/LEVEL.*
and TERRAIN.ALL; 11..17 add 0x140 to 005C5E88 and use LEVEL(n-10)/LEVEL1.*
and TERR1.ALL. Runtime logs independently confirm engines 1, 3, 6 and 17.
"""
from collections import Counter, defaultdict
import hashlib
import struct
import zlib

from .level_dat import LevelDat
from .level_raw import packets
from .original_level import RETAIL_EXE, trunc4096, unpack
from .terrain_all import TerrainAll
from .terrain_anthill_props import read_sprites
from .terrain_barriers import BarrierPayload
from .terrain_floor_patch import floor_cells
from .terrain_foliage import decode_mesh
from .terrain_scenery import read_mesh

# Progression is the 004C6A30 carousel position; names are researcher-provided
# (PC level roster and numbering). Engine16 has no carousel position.
LEVELS = {
    1: ('Anthill', 1), 2: ('Council Chamber', 3), 3: ('Tunnels', 2),
    4: ('City Entrance', 7), 5: ('City Square', 8), 6: ('Cliffside', 4),
    7: ('Clover Forest', 10), 8: ('Riverbed Flight', 14), 9: ('Anthill Pt 2', 13),
    10: ('Riverbed Canyon', 5), 11: ('Bird Nest', 6), 12: ('The Tree', 11),
    13: ('Battle Arena', 12), 14: ('Bug Bar', 9), 15: ('Canyon Showdown', 15),
    16: ('Special stage (engine 16)', None), 17: ('Training', 0),
}
SOURCE_SHA256 = {
    1: ('786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53',
        'c07452bafcf3799b55574d1622a37189358f5debcbd1127e167fd0fe0181700e',
        '62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868'),
    2: ('0bb00fa7387c2125ae20c55400bf5cea6a64641a7328cedc5cbd543bbd437ee7',
        '6f0c0e44daf0014de890046679f82ade7623e6b5472df3634bc056cd09b13269',
        '7f6b446fa9fac0951a6a6e3b1e70f2f9bd456ea4dc69160918aaa36c95de83fd'),
    3: ('bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b',
        '869700f6f8cd51d3d78ca14f55f350b343d6f77692f33fb11a8aef2b5f6a3ca4',
        'b878c378c924fbdb45e450f4314808fdd3506f8685da2c3f255b7e316f4a2d9c'),
    4: ('a6bbb538257e8652645df847623fa3623d889fdb7211891c2b145a2a18ffc905',
        '526fe962ffd5743769123229469f0129e0e754dc3387057701410281ba4108fe',
        '9cf8fb6990a955a808f2e4f2c22ffce3fe5d62136f4a9271bdc444a6dd7fc103'),
    5: ('438372b363692af46351be01f0e74d3cd0547980147766e4a00b2445b75c8d90',
        'ebfa2a5acc65a4d6ddbde57d97b9547962609c3b1a81aaba3f76bd11055e48eb',
        '57bce45056f8ecdeebc14d9851badab5f930c3c4736059075baacd390bb701ff'),
    6: ('7b23281eda241e215ea35f767f3dcf9bc948ec8b14b11ae7b572a997be1ee688',
        '5bbd05b081e79d7d0fe95156b3d49e541a86686a558d3e7cb2ac4c46dc06c9e3',
        'a478f03958a4ff2ed557e2ebc1b88ccd5d4966f3608c1fabfc8707646d536f44'),
    7: ('3b130e5a596b716f841e45b7fc0f8b0fea7c6e1d7fc2add795760ededca63d42',
        'e7f75265d4591a5534a76ee193a63108b9837bc318a9433d97404ef2fad6c020',
        '7b168efa7934cd6db15d94ae927151ed3df4e78064f1619877d5dcee463cf1c8'),
    8: ('596a13e3b80765ee81b0331ac74dd66916075683bcd3066ba51729c07e42d7ab',
        '79f7592d8de319660c1c4d36a96ebc7e9d5e7d5f01ca68593d588e364a4e2343',
        'adde03ec0126e4e831930fd79ba5a09e2ef40469a5becf783a2d52b56122db3a'),
    9: ('92559f64f0cad9e05d31972757f7f639d86aea713b9fe7698fa455a46ddcddab',
        'c9a5456e53db16bb63461c5a2ac4228ac4cd6fb1afd4aed5dfb7daa338f6a57b',
        '9132b16f120a8e4202d97a75decdf1fc785d2150feccdf4a0051c4832eb2d5af'),
    10: ('bba726988e64192d9bff73d5be8c0582f1d6a885b152050ec4e8883983a47319',
         '50a1ec79a0d9b55118692dd184778959088487aa397b54c0ff0c33ff56b2fb8c',
         '7a8471bb3fa14769de03edd58c1bae79428476b0c8f90e4bdc6d2e1d20e8206a'),
    11: ('20a8fd66de234e5ce30131cb3997f33dd75527c1fb18c5ffed5f33681cf6da15',
         'de7d7cf814fbaef5f86c847d55e76a3f8709e41469e6d1c6146f94a0ee5069a5',
         '602e71eefeaaf3b05cf6f441a5198d59d41d917bbd590cc623e4e1ec5edaa627'),
    12: ('5e850a16ee98bd9d7feb747b53390babeef372e98a82378f602104cd7ba76471',
         'ecfffece1a7196da4d556f9767a3b3c2d18e63e7ae1c8e8cfbd8bff2871f5493',
         '672412e9dc1373c9c6258a8ff0c7f780cf35c69bbf22f6df077ce08c3165c08e'),
    13: ('c0a1d40cb912162ee5ace15efed11022b4852a55238f238a1b650030f1dfb48d',
         '67c9b8e4bd2b7fc7339eb564bf4de419f0780c07f28f3ca2977854213c495b1f',
         '266678bbfa0475ebb14a07295f5122fc9d5be2614a53c20c6ce4d762181c0f3c'),
    14: ('a81f2397d32983014b5f3354e1dece7604168f84a998572ef1d9a8bada1d4dd2',
         '71ceb765fc4c08ea5e80d7584eaab2afafbee48b8d2ccb19b5651a824f3b87bf',
         'fb1efb453c41e2b8180a840819f1ee384ef7f979e770d59a7026ccaec5d705a1'),
    15: ('46e24f7566aa7592d8b118369088f5ca34ec05df028dd72383fed382cf4cc30b',
         '3bd5e71140f1d25b60c8be54f712de6f84c4e98d9bfa507003e8574305d9716c',
         '123969b6540c66e80fa35c73276d227d4c23492347dfaabf7bdab3098e7b0307'),
    16: ('7aab378d952f807ef283e93e90fc1c6f0f060e774a9c315f75b37c1cf54c2f13',
         'dba053d0ba9ef686a6f30d77fb3801f9c8298924f3659311cf0d05a6259f1e4d',
         'b024e1c0cbfb3e7070e13a0e62d76030433b416289aff0123fdb3207ba7dafc2'),
    17: ('494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22',
         'c5f81eed3c9d1a01cc188ead50fc10a5ae0f213b0ca165764fa7b311a02a0926',
         '97141bdc9953e963329fe968f4263478dffd74af041d6a4676a984239c4dfd8c'),
}
# 004498F0 masked dispatch -> drawing routine. Bit 0x10 selects the pass only.
MESH, MESH4, CAMERA, YAW = 'mesh', 'mesh-4', 'camera-facing sprites', 'yaw-facing sprites'
DISPATCH = {1: MESH, 0x41: MESH, 9: MESH, 0x49: MESH, 4: MESH4, 0x44: MESH4,
            0xc: MESH4, 0x4c: MESH4, 2: CAMERA, 0x42: CAMERA, 10: CAMERA, 0x4a: CAMERA,
            3: YAW, 0x43: YAW}
# 00417720 selector cases. Berries set weapon byte 0059D9A7; tokens bump
# 0059D9A8..0059D9AC; 0x30/0x31 are not removed on contact.
PICKUPS = {0x10: ('FLIK letters', 'Letter F'), 0x11: ('FLIK letters', 'Letter L'),
           0x12: ('FLIK letters', 'Letter I'), 0x13: ('FLIK letters', 'Letter K'),
           0x14: ('Grain', 'Grain'), 0x20: ('Berries', 'Berry reset (weapon 0)'),
           0x21: ('Berries', 'Green berry'), 0x22: ('Berries', 'Gold berry'),
           0x23: ('Berries', 'Blue berry'), 0x24: ('Berries', 'Purple berry'),
           0x29: ('Seed tokens', 'Yellow seed token'), 0x2a: ('Seed tokens', 'Blue seed token'),
           0x2b: ('Seed tokens', 'Green seed token'),
           0x2c: ('Seed tokens', 'Fourth seed token (0059D9AB)'),
           0x2d: ('Seed tokens', 'Fifth seed token (0059D9AC)'),
           0x30: ('Telescopes', 'Telescope'),
           0x31: ('Other pickups', 'Persistent selector 0x31 (unidentified)')}
PREVIEW_KINDS = {0x14: 'grain', 0x21: 'berry-green', 0x22: 'berry-gold', 0x23: 'berry-blue',
                 0x24: 'berry-purple', 0x29: 'token-yellow', 0x2a: 'token-blue', 0x2b: 'token-green'}
# Names established by EXP-20260926-001 (Anthill) and EXP-20260909-013
# (Training). Every other type keeps its numeric name; models show appearance.
CREATURES = {9: 'spider', 10: 'mosquito', 11: 'seed', 13: 'bee', 14: 'Dot',
             35: 'harvester', 38: 'Mr. Soil', 39: 'pill bug', 40: 'caterpillar'}
# Appearance only, from stored-pose model galleries rendered in EXP-20260927-001.
# These are viewing hints for the map, not creature identities or roles.
APPEARANCE = {1: 'winged moth', 2: 'mantis', 5: 'stick insect', 17: 'long-legged spider', 21: 'ant',
              25: 'winged moth', 28: 'ant', 29: 'grasshopper', 30: 'bird', 31: 'flytrap plant', 32: 'ant',
              34: 'dragonfly', 37: 'dandelion seed', 41: 'centipede'}
SPAWN_VA = 0x4dc7e8  # + engine*12: runtime X, Z, heading (clover_forest.py, EXP-20260913-003).
MAX_SCENE_RECORDS = 4096
MAX_MODEL_VERTICES = 20000
OFFSET_PART = 2048  # stored units from the model origin


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sources(engine):
    """Return (folder, DAT, RAW, terrain) CD-relative paths for engine 1..17."""
    if type(engine) is not int or engine not in LEVELS:
        raise ValueError('Engine index must be 1..17')
    folder = f'LEVEL{engine if engine <= 10 else engine-10:02d}'
    stem, terrain = ('LEVEL', 'TERRAIN.ALL') if engine <= 10 else ('LEVEL1', 'TERR1.ALL')
    return folder, f'{folder}/{stem}.DAT', f'{folder}/{stem}.RAW', f'{folder}/{terrain}'


def read_inputs(cd, engine):
    """Read and hash-check one level from a private CD copy."""
    _, *paths = sources(engine)
    data = [(cd/p).read_bytes() for p in paths]
    for path, content, expected in zip(paths, data, SOURCE_SHA256[engine], strict=True):
        if digest(content) != expected:
            raise ValueError(f'Expected exact original PC source: {path}')
    return dict(zip(('dat', 'raw', 'terrain'), data))


def negative_mesh_view(data, offset):
    """Positive view of a negative-count mesh; the extra span stays opaque.

    Static 0045A82E..0045A8B4: commands start at geometry+8+18N-2(N&1) for
    N=-count, after N ordinary 12-byte vertices and an auxiliary span.
    """
    count = -unpack(data, offset, '<i')[0]
    if not 1 <= count <= 5462:
        raise ValueError('Expected bounded negative vertex count')
    vertices_end = offset+4+12*count
    commands = offset+8+18*count-2*(count & 1)
    if commands > len(data)-2:
        raise ValueError('Truncated negative mesh auxiliary span')
    view = read_mesh(struct.pack('<i', count)+data[offset+4:vertices_end]+data[commands:], 0)
    extra = dict(offset=vertices_end, bytes=commands-vertices_end, sha256=digest(data[vertices_end:commands]))
    return view, extra


def mesh_geometry(data, geometry):
    """Return (decodable view, metadata); geometry_sha256 always covers the source span."""
    if unpack(data, geometry, '<i')[0] < 0:
        view, extra = negative_mesh_view(data, geometry)
        count = (extra['offset']-geometry-4)//12
        # Source = header + vertices + opaque span + the same command stream as the view.
        end = extra['offset']+extra['bytes']+len(view)-4-12*count
        return view, dict(mesh_format='negative-count mesh', auxiliary=extra,
                          geometry_sha256=digest(data[geometry:end]), geometry_bytes=end-geometry)
    mesh = read_mesh(data, geometry)
    return mesh, dict(mesh_format='positive mesh', auxiliary=None, geometry_sha256=digest(mesh),
                      geometry_bytes=len(mesh))


def sprite_quads(data, geometry, matrix, size):
    """00454B70/00453FF0 groups: centers use the object matrix, quads stay screen-aligned.

    `size` is the sprite-space scale: 0x1000 for dispatches 2/3, object +0x12/+0x14
    for dispatch 10. Quad +16 is a depth bias (param_4), not a size.
    """
    groups, end = read_sprites(data, geometry)
    rows = []
    for group in groups:
        center = [trunc4096(sum(matrix[k*3+j]*group.center[j] for j in range(3))) for k in range(3)]
        for quad in group.quads:
            xy = struct.unpack_from('<8h', quad)
            rows.append(dict(center=center, corners=[[trunc4096(xy[2*i]*size[0]), trunc4096(xy[2*i+1]*size[1])]
                                                     for i in range(4)],
                             page=struct.unpack_from('<H', quad, 18)[0] & 31, tag=struct.unpack_from('<H', quad, 18)[0],
                             uv=list(struct.unpack_from('<4H', quad, 20)),
                             rgb=[list(quad[28+4*i:31+4*i]) for i in range(4)], quad_hex=quad.hex()))
    return rows, end


def scene_objects(data, matrix_for):
    """Every primary/secondary record, including sprites and undispatched rows."""
    parsed = LevelDat.parse(data)
    if parsed.fixed_record_count:
        raise ValueError('Fixed-record DAT variants are not observed in retail levels')
    if len(parsed.primary_records)+len(parsed.secondary_records) > MAX_SCENE_RECORDS:
        raise ValueError('Original mapping scene budget exceeded')
    objects, undispatched = [], []
    for section in ('primary', 'secondary'):
        for row in parsed.records(section):
            masked = row.flags & 0xbfef
            offset = row.payload_offset_candidate
            size = 32 if row.flags & 8 else 24
            if offset < parsed.parsed_prefix_end:
                raise ValueError('Object overlaps DAT prefix')
            unpack(data, offset, f'<{size}s')
            geometry, = unpack(data, offset+size-4, '<I')
            if geometry < parsed.parsed_prefix_end:
                raise ValueError('Geometry overlaps DAT prefix')
            common = dict(id=f'{section}.{row.index:03d}', section=section, record_offset=row.offset,
                          object_offset=offset, geometry_offset=geometry, flags=row.flags, dispatch=masked,
                          record_center=list(unpack(data, row.offset, '<3i')),
                          record_hex=data[row.offset:row.offset+20].hex(), object_hex=data[offset:offset+size].hex())
            if masked & 0x20:
                # 004498F0 has 0x21/0x24/0x29/0x2C cases; none occur in retail levels.
                raise ValueError(f'Unsupported dispatch 0x20 family: {section} {row.index} flags {row.flags:#x}')
            kind = DISPATCH.get(masked)
            if kind is None:
                # No 004498F0 case: keep the record, never guess a drawing path.
                undispatched.append(dict(common, origin=list(unpack(data, offset, '<3i')),
                                         note='Masked dispatch has no 004498F0 case; not drawn by that dispatcher'))
                continue
            origin = unpack(data, offset, '<3i')
            angles = unpack(data, offset+12, '<3h')
            scale = unpack(data, offset+18, '<3h') if row.flags & 8 else (4096,)*3
            matrix = matrix_for(angles)
            item = dict(common, kind=kind, origin=list(origin), angles=list(angles), scale=list(scale),
                        matrix=list(matrix), animation_selector=data[offset+(25 if row.flags & 8 else 19)] & 31
                        if kind == MESH else 0)
            if kind in (MESH, MESH4):
                mesh, meta = mesh_geometry(data, geometry)
                vs, groups = decode_mesh(mesh)
                scaled = [trunc4096(matrix[k]*scale[k % 3]) for k in range(9)]
                item.update(meta, vertices=[dict(position=[trunc4096(sum(scaled[k*3+j]*local[j] for j in range(3)))
                                                           for k in range(3)], rgb=list(v[8:11]))
                                            for v in vs for local in [unpack(v, 0, '<3h')]],
                            faces=[dict(tag=tag, indices=list(ids), uv=list(uv)) for tag, fs in groups for ids, uv in fs])
            else:
                size2 = (scale[0], scale[1]) if kind == CAMERA and row.flags & 8 else (4096, 4096)
                quads, end = sprite_quads(data, geometry, matrix, size2)
                item.update(sprites=quads, sprite_scale=list(size2), geometry_sha256=digest(data[geometry:end]),
                            preview='Screen-aligned quads shown as crossed planes; native faces the camera')
            objects.append(item)
    return parsed, objects, undispatched


def texture_image(payload):
    """256/128-square 4-bit (256 only) or 8-bit pages; RGB green is the colour key.

    4-bit pixels take palette row x//64 + 4*(y//64), as 00462C30's 4-bit
    branch does (004630D2..00463126, EXP-20261018-009).
    """
    tag, width, height, palette_size, mode = unpack(payload, 0, '<I4H')
    if palette_size != 768 or width != height or width not in (128, 256) or mode not in (0, 1) \
            or (mode == 0 and width != 256):
        raise ValueError('Unsupported original mapping texture layout')
    pixels = width*height
    if len(payload) != 780+(pixels//2 if mode == 0 else pixels):
        raise ValueError('Original mapping texture size mismatch')
    palette = payload[12:780]
    if mode == 0:
        indices = bytes(((payload[780+i//2] >> (4*(i & 1))) & 15)
                        + 16*((i % 256)//64 + 4*((i//256)//64)) for i in range(pixels))
    else:
        indices = payload[780:]
    rgba = bytearray()
    for index in indices:
        r, g, b = palette[index*3:index*3+3]
        rgba.extend((r, g, b, 0 if r == b == 0 and g > 249 else 255))
    return tag, width, indices, palette, bytes(rgba)


def png(rgba, width):
    if len(rgba) != width*width*4:
        raise ValueError('Expected square RGBA pixels')
    def chunk(kind, data):
        return struct.pack('>I', len(data))+kind+data+struct.pack('>I', zlib.crc32(kind+data) & 0xffffffff)
    rows = b''.join(b'\0'+rgba[y*width*4:(y+1)*width*4] for y in range(width))
    return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('>IIBBBBB', width, width, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(rows))+chunk(b'IEND', b''))


def normal_table(data, cur, end, corners):
    """Bytes after a model primitive terminator: u16 count, two bytes, count*8, then u16 per corner.

    Structural reading (EXP-20260927-001): every vector has length ~4096 and the
    index count equals the preceding primitives' corners (3 per triangle, 4 per
    quad), i.e. per-corner normals. 0044F8E0 stops at the terminator; the
    consumer is not localized. Nothing here is drawn. Other layouts stay opaque.
    """
    if end-cur < 4:
        return None
    count, byte2, byte3 = unpack(data, cur, '<HBB')
    indices = cur+4+count*8
    if not 1 <= count <= 1024 or indices > end or end-indices != 2*corners:
        return None
    lengths = [sum(c*c for c in unpack(data, cur+4+8*i, '<3h'))**.5 for i in range(count)]
    if any(abs(length-4096) > 64 for length in lengths):
        return None
    return dict(offset=cur, normals=count, header=[byte2, byte3], corner_indices=corners,
                bytes=end-cur, sha256=digest(data[cur:end]), role='per-corner normals (structural inference)')


def creature_model(data):
    """Textured 36/48-byte ALL primitives in stored pose; trailing normal tables are metadata."""
    parsed = TerrainAll.parse(data)
    vertices, faces, parts, opaque = [], [], [], []
    for record in parsed.records:
        if record.field_10 != 1:
            opaque.append(dict(index=record.index, kind=record.field_10, offset=record.offset,
                               payload_offset=record.payload_offset, payload_size=record.payload_size))
            continue
        cur, end = record.payload_offset, record.payload_offset+record.payload_size
        origin = (record.component_x, record.component_y, record.component_z)
        tail, corners = None, 0
        while True:
            if cur+4 > end:
                raise ValueError('Missing ALL primitive terminator')
            command = data[cur+3]
            if command == 0:
                if cur+4 != end:
                    tail = normal_table(data, cur+4, end, corners)
                    if tail is None:
                        opaque.append(dict(index=record.index, kind='unparsed tail', offset=cur+4,
                                           bytes=end-cur-4, sha256=digest(data[cur+4:end])))
                break
            count = {0x34: 3, 0x3c: 4}.get(command & 0x7c)
            if count is None:
                raise ValueError(f'Unsupported ALL primitive {command:#x}')
            size = 36 if count == 3 else 48
            if cur+size > end:
                raise ValueError('ALL primitive overruns its payload')
            base = len(vertices); corners += count
            colors = [cur]+[cur+4+count*8+4*i for i in range(count-1)]
            for i in range(count):
                position = unpack(data, cur+4+i*8, '<3h')
                vertices.append(dict(position=[position[k]+origin[k] for k in range(3)],
                                     rgb=list(data[colors[i]:colors[i]+3])))
            # 0044F8E0 submits strip quads as 0,1,3 and 0,3,2.
            order = [0, 1, 2] if count == 3 else [0, 1, 3, 2]
            faces.append(dict(indices=[base+i for i in order],
                              uv=[unpack(data, cur+10+8*i, '<H')[0] for i in order],
                              tag=unpack(data, cur+size-2, '<H')[0], part=record.index))
            cur += size
        # Structural split only: some models store extra parts far from the
        # model origin (e.g. seed parts at X-5000); their role is not claimed.
        parts.append(dict(index=record.index, origin=list(origin), normal_table=tail,
                          offset_part=max(abs(c) for c in origin) > OFFSET_PART))
        if len(vertices) > MAX_MODEL_VERTICES:
            raise ValueError('Creature model vertex budget exceeded')
    if not faces:
        raise ValueError('No supported ALL visual primitives')
    return dict(vertices=vertices, faces=faces, parts=parts, opaque=opaque,
                pose='Stored descriptor translations; no native animation matrices')


def creature_rows(payload):
    if len(payload) != 4+64*28 or unpack(payload, 0, '<I') != (0x23,):
        raise ValueError('Expected one complete PC 64-slot creature packet')
    rows = []
    for slot in range(64):
        raw = payload[4+slot*28:4+slot*28+28]
        if raw[12]:
            rows.append(dict(slot=slot, offset=4+slot*28, type=raw[12], script=raw[13], flags=raw[14],
                             position=list(unpack(raw, 0, '<3i')), raw_hex=raw.hex(),
                             name=CREATURES.get(raw[12]), appearance=APPEARANCE.get(raw[12])))
    return rows


def spawn(exe, pe, engine):
    """Runtime X/Z/heading from the executable's per-engine table (12 bytes)."""
    offset = pe.get_offset_from_rva(SPAWN_VA+12*engine-pe.OPTIONAL_HEADER.ImageBase)
    x, z, heading = unpack(exe, offset, '<3i')
    return dict(runtime_xz=[x, z], stored_xz=[x/32, z/32], heading=heading,
                va=f'0x{SPAWN_VA+12*engine:08X}', file_offset=offset)


def extract(engine, inputs, matrix_for):
    """Scenery, terrain and raw populations; native initialization is added by the caller."""
    dat, raw, terrain = inputs['dat'], inputs['raw'], inputs['terrain']
    parsed, objects, undispatched = scene_objects(dat, matrix_for)
    chunks, suffix = packets(raw)
    by_tag = defaultdict(list)
    for offset, packet, payload in chunks:
        by_tag[unpack(payload, 0, '<I')[0]].append((offset, payload))
    creature_packets = by_tag.get(0x23, [])
    if len(creature_packets) != 1:
        raise ValueError('Expected one type35 creature packet')
    creatures = creature_rows(creature_packets[0][1])
    models = {}
    for kind in sorted({r['type'] for r in creatures}):
        found = [(o, p) for o, p in by_tag.get(0x102, []) if len(p) >= 8 and unpack(p, 4, '<I')[0] == kind]
        if len(found) != 1:
            raise ValueError(f'Expected one model packet for creature type {kind}')
        offset, payload = found[0]
        models[kind] = dict(creature_model(payload[8:]), packet_offset=offset, payload_sha256=digest(payload))
    wanted = {(f['tag'] >> 8) & 31 for o in objects for f in o.get('faces', ())}
    wanted |= {q['page'] for o in objects for q in o.get('sprites', ())}
    wanted |= {(f['tag'] >> 8) & 31 for m in models.values() for f in m['faces'] if f['tag'] is not None}
    textures, pages, unavailable = {}, [], {}
    for page in sorted(wanted):
        found = by_tag.get(page, [])
        if len(found) != 1:
            unavailable[page] = f'{len(found)} RAW packets'
            continue
        try:
            _, width, indices, palette, rgba = texture_image(found[0][1])
        except ValueError as error:
            unavailable[page] = str(error)
            continue
        textures[page] = png(rgba, width)
        pages.append(dict(page=page, width=width, packet_offset=found[0][0], packet_sha256=digest(found[0][1]),
                          indices_sha256=digest(indices), palette_sha256=digest(palette),
                          png_sha256=digest(textures[page])))
    ground = TerrainAll.parse(terrain)
    by_source = defaultdict(list)
    for cell in floor_cells(ground):
        by_source[cell.source].append(cell.report())
    collision = [dict(source=s, result_word=ground.records[s].result_word, kind=ground.records[s].field_10,
                      cells=cells) for s, cells in sorted(by_source.items())]
    barriers = []
    for source in ground.records:
        if source.field_10 == 0x101:
            strip = BarrierPayload.from_terrain(ground, source.index)
            barriers.append(dict(source=source.index, record_offset=source.offset, payload_offset=strip.offset,
                                 segments=strip.segment_count, points_xz=[[p.x, p.z] for p in strip.points],
                                 display_y=0, note='XZ-only barrier; display elevation is arbitrary'))
    terrain_other = [dict(source=r.index, kind=r.field_10, result_word=r.result_word, offset=r.offset,
                          payload_offset=r.payload_offset, payload_size=r.payload_size)
                     for r in ground.records if r.field_10 not in (6, 7, 8, 0x101)]
    pickups, rows = [], []
    for top in parsed.top_records:
        if top.type_id < 0:
            continue
        stride = 16 if top.type_id == 0x3f else 12
        for i in range(top.count):
            offset = top.offset+4+i*stride
            position = list(unpack(dat, offset, '<3i'))
            if top.type_id == 0x3f:
                selector = dat[offset+12]
                layer, label = PICKUPS.get(selector, ('Other pickups', f'Unidentified selector 0x{selector:02X}'))
                pickups.append(dict(id=f'type3f.{i:03d}', index=i, selector=selector, layer=layer, label=label,
                                    stored_position=position, offset=offset, raw_hex=dat[offset:offset+16].hex()))
            else:
                rows.append(dict(id=f'type{top.type_id:02x}.{i:03d}', type=top.type_id, position=position,
                                 offset=offset, raw_hex=dat[offset:offset+12].hex()))
    opaque_tops = [dict(index=t.index, type=t.type_id, offset=t.offset, count=t.count, size=t.size)
                   for t in parsed.top_records if t.type_id < 0]
    name, progression = LEVELS[engine]
    counts = dict(scene_records=len(parsed.primary_records)+len(parsed.secondary_records),
                  drawn_objects=len(objects), undispatched_records=len(undispatched),
                  mesh_objects=sum(o['kind'] in (MESH, MESH4) for o in objects),
                  sprite_objects=sum(o['kind'] in (CAMERA, YAW) for o in objects),
                  sprite_quads=sum(len(o.get('sprites', ())) for o in objects),
                  vertices=sum(len(o.get('vertices', ())) for o in objects),
                  faces=sum(len(o.get('faces', ())) for o in objects),
                  pickups=len(pickups), creatures=len(creatures), creature_types=len(models),
                  other_rows=len(rows), collision_sources=len(collision),
                  collision_triangles=sum(len(c['cells']) for c in collision),
                  barrier_segments=sum(b['segments'] for b in barriers), texture_pages=len(pages))
    return dict(format='ablpc.original-map', version=2, engine=engine, name=name, progression=progression,
                coordinate_system={'blender_xyz': '[stored X, stored Z, -stored Y] / 256',
                                   'origin_stored': [0, 0, 0], 'runtime_units_per_stored_unit': 32},
                objects=objects, undispatched=undispatched, pickups=pickups, other_rows=rows,
                creatures=creatures, creature_models={str(k): v for k, v in models.items()},
                collision=collision, barriers=barriers, terrain_other=terrain_other, textures=pages,
                unavailable_pages={str(k): v for k, v in unavailable.items()},
                dat_structure=dict(index_table_offset=parsed.index_table_offset,
                                   index_table_values=list(parsed.index_table_values), opaque_top_records=opaque_tops,
                                   final_dword=parsed.final_dword),
                raw_structure=dict(packets=len(chunks), suffix_hex=suffix.hex(),
                                   tags=dict(sorted(Counter(unpack(p, 0, '<I')[0] for _, _, p in chunks).items()))),
                counts=counts, dispatches=dict(Counter(f'{o["dispatch"]:#04x}' for o in objects+undispatched))), textures


def initialized_pickups(pickups, table_offset, initialized):
    """Join stored rows to the native 00456A90 table; XZ must be unchanged."""
    count, kind = unpack(initialized, 0, '<hh')
    if kind != 0x3f or count != len(pickups) or len(initialized) != 4+count*16:
        raise ValueError('Invalid initialized type3F table')
    for row in pickups:
        offset = row['offset']-table_offset
        if offset != 4+16*row['index'] or initialized[offset+12] != row['selector']:
            raise ValueError('Source/initialized pickup mismatch')
        position = list(unpack(initialized, offset, '<3i'))
        if position[::2] != row['stored_position'][::2]:
            raise ValueError('Native initializer unexpectedly moved pickup XZ')
        row.update(position=position, initialized_hex=initialized[offset:offset+16].hex())
    return pickups
