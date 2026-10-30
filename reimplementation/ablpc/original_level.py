"""PC original-level mapping scenes, EXP-20260909-012.

Read-only composition of existing DAT/RAW/terrain readers. Coordinates and
opaque records remain available; this is not a game-file compiler. Native
Euler matrices use the hashed PC executable's 00463C80 in offline Unicorn.
"""
from collections import Counter, defaultdict
import hashlib
import struct
import zlib

from .level_dat import LevelDat
from .level_raw import packets
from .terrain_all import TerrainAll
from .terrain_barriers import BarrierPayload
from .terrain_floor_patch import floor_cells
from .terrain_foliage import decode_mesh
from .terrain_scenery import read_mesh

RETAIL_EXE = '97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878'
TRAINING = {
    'dat': ('LEVEL07/LEVEL1.DAT', '494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22'),
    'raw': ('LEVEL07/LEVEL1.RAW', 'c5f81eed3c9d1a01cc188ead50fc10a5ae0f213b0ca165764fa7b311a02a0926'),
    'terrain': ('LEVEL07/TERR1.ALL', '97141bdc9953e963329fe968f4263478dffd74af041d6a4676a984239c4dfd8c'),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unpack(data, offset, fmt):
    size = struct.calcsize(fmt)
    if type(offset) is not int or offset < 0 or offset + size > len(data):
        raise ValueError(f'Original-level read outside file at {offset!r}, size {size}')
    return struct.unpack_from(fmt, data, offset)


def trunc4096(n):
    return (abs(n) // 4096) * (-1 if n < 0 else 1)


class NativeMatrices:
    def __init__(self, image):
        if digest(image) != RETAIL_EXE:
            raise ValueError('Original-level matrices require the exact retail PC executable')
        import pefile
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
        from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EIP
        self.esp, self.eip = UC_X86_REG_ESP, UC_X86_REG_EIP
        pe = pefile.PE(data=image)
        self.cpu = Uc(UC_ARCH_X86, UC_MODE_32)
        self.cpu.mem_map(0x400000, (pe.OPTIONAL_HEADER.SizeOfImage + 4095) & ~4095)
        self.cpu.mem_write(0x400000, pe.get_memory_mapped_image())
        self.cpu.mem_map(0x10000000, 0x10000)
        self.cache = {}

    def __call__(self, angles):
        if angles not in self.cache:
            self.cpu.mem_write(0x10001000, struct.pack('<3h', *angles))
            self.cpu.mem_write(0x1000f000, struct.pack('<3I', 0x1000fff0, 0x10001000, 0x10002000))
            self.cpu.reg_write(self.esp, 0x1000f000)
            self.cpu.emu_start(0x463c80, 0x1000fff0, count=20000)
            if self.cpu.reg_read(self.eip) != 0x1000fff0:
                raise ValueError('Native original-level matrix instruction budget exceeded')
            self.cache[angles] = struct.unpack('<9h', self.cpu.mem_read(0x10002000, 18))
        return self.cache[angles]


def scene_objects(data, matrix_for):
    """Import both scene lists, refusing unsupported dispatches or pointer variants."""
    parsed = LevelDat.parse(data)
    if parsed.fixed_record_count or parsed.index_table_max != -1:
        raise ValueError('Original mapping does not support fixed/indexed DAT variants')
    if len(parsed.primary_records) + len(parsed.secondary_records) > 4096:
        raise ValueError('Original mapping scene budget exceeded')
    objects = []
    for section in ('primary', 'secondary'):
        for row in parsed.records(section):
            dispatch = row.flags & 0xbfef
            if dispatch not in (1, 9, 0x41, 0x49) or row.flags & 0x20:
                raise ValueError(f'Unsupported {section} scene {row.index}: flags {row.flags:#x}')
            offset = row.payload_offset_candidate
            size = 32 if row.flags & 8 else 24
            if offset < parsed.parsed_prefix_end:
                raise ValueError('Object overlaps DAT prefix')
            unpack(data, offset, f'<{size}s')
            origin = unpack(data, offset, '<3i')
            angles = unpack(data, offset + 12, '<3h')
            scale = unpack(data, offset + 18, '<3h') if row.flags & 8 else (4096,) * 3
            geometry, = unpack(data, offset + size - 4, '<I')
            if geometry < parsed.parsed_prefix_end:
                raise ValueError('Geometry overlaps DAT prefix')
            vs, groups = decode_mesh(read_mesh(data, geometry))
            matrix = matrix_for(angles)
            scaled = [trunc4096(matrix[k] * scale[k % 3]) for k in range(9)]
            vertices = []
            for v in vs:
                local = unpack(v, 0, '<3h')
                vertices.append({
                    'position': [trunc4096(sum(scaled[k*3+j]*local[j] for j in range(3))) for k in range(3)],
                    'source_xyz': list(local), 'rgb': list(v[8:11]), 'opaque': v[6:8].hex() + v[11:12].hex(),
                })
            objects.append({
                'id': f'{section}.{row.index:03d}', 'section': section,
                'record_offset': row.offset, 'object_offset': offset, 'geometry_offset': geometry,
                'flags': row.flags, 'origin': list(origin), 'angles': list(angles), 'scale': list(scale),
                'matrix': list(matrix), 'scaled_matrix': scaled,
                'animation_selector': data[offset + (25 if row.flags & 8 else 19)] & 31,
                'record_hex': data[row.offset:row.offset+20].hex(), 'object_hex': data[offset:offset+size].hex(),
                'vertices': vertices,
                'faces': [{'tag': tag, 'indices': list(ids), 'uv': list(uv)} for tag, fs in groups for ids, uv in fs],
            })
    return parsed, objects


def texture_page(payload):
    """256-square 4-bit banks or 8-bit PC page; RGB green is the colour key.

    00462C30 expands low nibble first, bank = x//64 + 4*(y//64)
    (4-bit branch 004630D2..00463126; EXP-20261018-009).
    The 8-bit index result can be compared directly with EXP-20260905-005.
    """
    tag, width, height, palette_size, mode = unpack(payload, 0, '<I4H')
    if width != 256 or height != 256 or palette_size != 768 or mode not in (0, 1):
        raise ValueError('Unsupported original mapping texture layout')
    expected = 780 + (32768 if mode == 0 else 65536)
    if len(payload) != expected:
        raise ValueError('Original mapping texture size mismatch')
    palette = payload[12:780]
    if mode == 0:
        indices = bytes(((payload[780+i//2] >> (4*(i & 1))) & 15)
                        + 16*((i % 256)//64 + 4*((i//256)//64)) for i in range(65536))
    else:
        indices = payload[780:]
    rgba = bytearray()
    for index in indices:
        r, g, b = palette[index*3:index*3+3]
        rgba.extend((r, g, b, 0 if r == b == 0 and g > 249 else 255))
    return tag, indices, palette, bytes(rgba)


def png_rgba(rgba):
    if len(rgba) != 256*256*4:
        raise ValueError('Expected 256-square RGBA pixels')
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind+data) & 0xffffffff)
    rows = b''.join(b'\0' + rgba[y*1024:(y+1)*1024] for y in range(256))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 256, 256, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))


def extract(dat, raw, terrain, matrix_for):
    parsed, objects = scene_objects(dat, matrix_for)
    wanted = {(f['tag'] >> 8) & 31 for o in objects for f in o['faces']}
    textures, pages = {}, []
    chunks, suffix = packets(raw)
    for offset, packet, payload in chunks:
        tag, = unpack(payload, 0, '<I')
        if tag not in wanted:
            continue
        if tag in textures:
            raise ValueError(f'Duplicate requested texture page {tag}')
        _, indices, palette, rgba = texture_page(payload)
        textures[tag] = png_rgba(rgba)
        pages.append({'page': tag, 'packet_offset': offset, 'packet_sha256': digest(packet),
                      'indices_sha256': digest(indices), 'palette_sha256': digest(palette),
                      'png_sha256': digest(textures[tag])})
    if set(textures) != wanted:
        raise ValueError(f'Missing original texture pages: {wanted - set(textures)}')
    ground = TerrainAll.parse(terrain)
    by_source = defaultdict(list)
    for cell in floor_cells(ground):
        by_source[cell.source].append(cell.report())
    collision = [{'source': source, 'cells': cells} for source, cells in sorted(by_source.items())]
    barriers = []
    for source in ground.records:
        if source.field_10 == 0x101:
            strip = BarrierPayload.from_terrain(ground, source.index)
            barriers.append({'source': source.index, 'record_offset': source.offset,
                             'payload_offset': strip.offset, 'segments': strip.segment_count,
                             'points_xz': [[p.x, p.z] for p in strip.points],
                             'display_y': 0, 'note': 'XZ-only barrier; display elevation is arbitrary, not collision height'})
    placements = []
    labels = {0x14: 'Grain', 0x10: 'Letter F', 0x11: 'Letter L', 0x12: 'Letter I', 0x13: 'Letter K'}
    for top in parsed.top_records:
        if top.type_id < 0:
            continue  # Opaque data remains in the original retained DAT.
        stride = 16 if top.type_id == 0x3f else 12
        for i in range(top.count):
            offset = top.offset + 4 + i*stride
            position = unpack(dat, offset, '<3i')
            selector = dat[offset+12] if top.type_id == 0x3f else None
            label = labels.get(selector, f'Unknown selector 0x{selector:02X}') if selector is not None else f'Type 0x{top.type_id:02X} position'
            placements.append({'id': f'type{top.type_id:02x}.{i:03d}', 'label': label,
                               'position': list(position), 'offset': offset, 'selector': selector,
                               'raw_hex': dat[offset:offset+stride].hex(),
                               'note': 'Stored placement; native initialization may replace Y'})
    counts = {'primary_objects': len(parsed.primary_records), 'secondary_objects': len(parsed.secondary_records),
              'vertices': sum(len(o['vertices']) for o in objects), 'faces': sum(len(o['faces']) for o in objects),
              'texture_pages': len(pages), 'collision_sources': len(collision),
              'collision_triangles': sum(len(c['cells']) for c in collision),
              'barrier_segments': sum(b['segments'] for b in barriers), 'placement_markers': len(placements),
              'animated_objects_in_stored_pose': sum(o['animation_selector'] != 0 for o in objects)}
    scene = {'format': 'ablpc.original-map', 'version': 1, 'name': 'LEVEL00 - Training',
             'coordinate_system': {'blender_xyz': '[stored X, stored Z, -stored Y] / 256',
                                   'origin_stored': [0, 0, 0], 'runtime_units_per_stored_unit': 32},
             'objects': objects, 'collision': collision, 'barriers': barriers, 'placements': placements,
             'textures': pages, 'counts': counts,
             'limits': ['Stored scenery pose, no animation playback or camera-dependent deformation.',
                        'Secondary scene hidden initially; scene-list membership is preserved.',
                        'No Flik, Mr Soil, dynamic actors, particles, scripts or generated plant geometry.',
                        'Placement markers retain file Y; native initialized height may differ.',
                        'Texture/vertex-colour preview is not a reproduction of the native renderer.',
                        'Mapping and annotation only; no original-level game-file export.']}
    report = {'format': scene['format'], 'version': 1, 'experiment': 'EXP-20260909-012',
              'name': scene['name'], 'hashes': {'dat': digest(dat), 'raw': digest(raw), 'terrain': digest(terrain)},
              'counts': counts, 'textures': pages, 'limits': scene['limits'],
              'scene_flags': dict(Counter(f'{o["flags"]:#06x}' for o in objects)),
              'raw_packet_count': len(chunks), 'raw_suffix_hex': suffix.hex()}
    return scene, textures, report
