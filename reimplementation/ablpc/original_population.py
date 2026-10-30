"""Bounded Training mapping additions, EXP-20260909-013.

Actor records: PC 0041C420/0041BD10. Stored ALL primitives: 0044F8E0.
These are reference poses and editor markers, never game-file output.
"""
import struct

from .original_level import unpack
from .terrain_all import TerrainAll

TOKEN_KINDS = {0x29: 'token-yellow', 0x2a: 'token-blue', 0x2b: 'token-green'}
BERRY_PICKUPS = {0x23: 'berry-blue', 0x2c: 'berry-seed-token'}
MAPPED_PICKUPS = {0x14, 0x10, 0x11, 0x12, 0x13, *TOKEN_KINDS, *BERRY_PICKUPS}


def initialized_placements(placements, table_offset, initialized, selectors=MAPPED_PICKUPS):
    """Join checked source locators to native-initialized rows; keep file bytes.

Tokens are DAT pickups, not RAW seed actors. Unidentified selectors stay omitted.
    """
    count, kind = unpack(initialized, 0, '<hh')
    if kind != 0x3f or count < 0 or len(initialized) != 4+count*16:
        raise ValueError('Invalid initialized type3F table')
    rows, seen = [], set()
    for row in placements:
        if row['selector'] not in selectors:
            continue
        offset = row['offset']-table_offset
        if offset < 4 or (offset-4)%16 or offset+16 > len(initialized) or offset in seen:
            raise ValueError('Invalid or duplicate pickup locator')
        seen.add(offset)
        raw = bytes.fromhex(row['raw_hex'])
        if len(raw)!=16 or raw[12]!=row['selector'] or initialized[offset+12]!=row['selector']:
            raise ValueError('Source/initialized pickup selector mismatch')
        position = list(unpack(initialized, offset, '<3i'))
        if position[::2] != list(unpack(raw,0,'<3i'))[::2]:
            raise ValueError('Native initializer unexpectedly moved pickup XZ')
        result = dict(row,position=position,stored_position=row['position'],
                      initialized_hex=initialized[offset:offset+16].hex())
        if row['selector'] in TOKEN_KINDS:
            result['preview_kind'] = TOKEN_KINDS[row['selector']]
            result['label'] = result['preview_kind'].split('-')[1].title()+' seed token'
        if row['selector'] in BERRY_PICKUPS:
            result['preview_kind'] = BERRY_PICKUPS[row['selector']]
            result['label'] = 'Blueberry' if row['selector']==0x23 else 'Berry seed token'
            result['availability'] = 'Stored placement' if row['selector']==0x23 else 'Revealed by tutorial lesson13 after lesson12 berry-weapon gate'
        rows.append(result)
    return rows


def actors(payload):
    if len(payload) != 4 + 64*28 or unpack(payload, 0, '<I') != (0x23,):
        raise ValueError('Expected one complete PC 64-slot actor packet')
    rows = []
    kinds = {9: 'spider', 11: 'seed', 38: 'Mr. Soil'}
    for slot in range(64):
        offset = 4 + slot*28
        raw = payload[offset:offset+28]
        kind = raw[12]
        if not kind:
            continue
        if kind not in kinds:
            raise ValueError(f'Unsupported Training actor type {kind}')
        rows.append(dict(slot=slot, offset=offset, type=kind, kind=kinds[kind],
                         script=raw[13], position=list(unpack(raw, 0, '<3i')), raw_hex=raw.hex()))
    return rows


def stored_model(data):
    """Read the demonstrated 36/48-byte textured ALL primitive subset.

Source descriptor translation is retained; animation matrices are NOT applied.
Only exact four-byte terminators are accepted. Other kinds stay in source bytes.
    """
    parsed = TerrainAll.parse(data)
    vertices, faces, sources = [], [], []
    for record in parsed.records:
        if record.field_10 != 1:
            continue
        cur = record.payload_offset
        end = cur + record.payload_size
        origin = (record.component_x, record.component_y, record.component_z)
        while True:
            if cur+4 > end:
                raise ValueError('Missing ALL primitive terminator')
            command = data[cur+3]
            if command == 0:
                if cur+4 != end:
                    raise ValueError('Unsupported ALL data after terminator')
                break
            count = {0x34: 3, 0x3c: 4}.get(command & 0x7c)
            if count is None:
                raise ValueError(f'Unsupported ALL primitive {command:#x}')
            size = 36 if count == 3 else 48
            if cur+size > end:
                raise ValueError('ALL primitive overruns its payload')
            base = len(vertices)
            colors = [cur] + [cur+4+count*8+4*i for i in range(count-1)]
            for i in range(count):
                position = unpack(data, cur+4+i*8, '<3h')
                vertices.append(dict(position=[position[k]+origin[k] for k in range(3)],
                                     rgb=list(data[colors[i]:colors[i]+3]),
                                     source_xyz=list(position), source_offset=cur+4+i*8))
            # The original renderer submits 0,1,3 and 0,3,2 for strip quads.
            order = [0, 1, 2] if count == 3 else [0, 1, 3, 2]
            faces.append(dict(indices=[base+i for i in order],
                              uv=[unpack(data, cur+10+8*i, '<H')[0] for i in order],
                              tag=unpack(data, cur+size-2, '<H')[0],
                              source_offset=cur, raw_hex=data[cur:cur+size].hex()))
            cur += size
        sources.append(dict(index=record.index, offset=record.offset,
                            origin=list(origin), raw_hex=record.raw.hex()))
    if not faces:
        raise ValueError('No supported ALL visual primitives')
    return dict(vertices=vertices, faces=faces, sources=sources,
                pose='Stored descriptor translations; no native animation matrices')


def letter_pixels(payload, palette):
    if (len(payload) != 4620 or unpack(payload, 0, '<IIHH') not in
            [(34, tile, 24, 24) for tile in range(16, 20)] or len(palette) != 768):
        raise ValueError('Expected native 24-square, 16-frame FLIK strip and palette')
    # EXP-011: pickup letter strips use palette bank 7. Frame zero only.
    pixels = []
    for i in range(576):
        index = (payload[12+i//2] >> (4*(i & 1))) & 15
        if index:
            pixels.append(dict(x=i % 24, y=i//24, rgb=list(palette[(112+index)*3:(113+index)*3])))
    return pixels
