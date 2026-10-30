"""Complete original-level mapping, EXP-20260927-001: synthetic bounds plus private corpus."""
from pathlib import Path
import runpy
import struct

import pytest

from ablpc import original_levels as ol

ROOT = Path(__file__).resolve().parents[1]
CD = ROOT/'work/copies/BUGS_PC-full-disc/PC/BUGS/CD'
IDENTITY = (4096, 0, 0, 0, 4096, 0, 0, 0, 4096)
SENTINEL = struct.pack('<5I', *(0x80008000,)*5)


def quad(tag=0x62, xy=(-10, -20, 10, -20, 10, 0, -10, 0)):
    return (struct.pack('<8hhH4H', *xy, 1, tag, 0x0000, 0x00ff, 0xffff, 0xff00)
            + bytes((10, 20, 30, 0, 40, 50, 60, 0, 70, 80, 90, 0, 1, 2, 3, 0)))


def sprites(center=(100, -200, 300)):
    return struct.pack('<i3ii', 1, *center, 1)+quad()


def negative_mesh():
    # N=3: vertices end at +40, commands at +8+54-2=+60, so a 20-byte opaque span.
    vertices = b''.join(struct.pack('<3h6B', *p, 0, 0, 9, 8, 7, 0) for p in [(1, 2, 3), (4, 5, 6), (7, 8, 9)])
    return struct.pack('<i', -3)+vertices+b'\xAA'*20+struct.pack('<2H6H', 0x61, 1, 0, 12, 24, 0, 1, 2)+b'\xff\xff'


def synthetic_dat(rows, index=(), secondary=()):
    """rows: (flags, object_bytes_without_pointer, geometry). Pointer is appended."""
    records = [(f, o, g, 'p') for f, o, g in rows]+[(f, o, g, 's') for f, o, g in secondary]
    size = 4+4+20*len(rows)+20+4+4*len(index)+20*len(secondary)+20
    payload, record_bytes = b'', {'p': b'', 's': b''}
    for flags, obj, geometry, section in records:
        object_offset = size+len(payload)
        geometry_offset = object_offset+len(obj)+4
        payload += obj+struct.pack('<I', geometry_offset)+geometry
        payload += b'\0'*(-len(payload) % 4)
        record_bytes[section] += struct.pack('<3ihHI', 1, 2, 3, 100, flags, object_offset)
    prefix = (struct.pack('<2i', 0, 0)+record_bytes['p']+SENTINEL+struct.pack('<i', len(index)-1)
              + b''.join(struct.pack('<i', v) for v in index)+record_bytes['s']+SENTINEL)
    assert len(prefix) == size
    return prefix+payload+struct.pack('<i', -1)


def unscaled(origin=(1000, 2000, 3000), angles=(0, 0, 0), selector=0):
    return struct.pack('<3i3h', *origin, *angles)+bytes((0, selector))


def scaled(origin=(1000, 2000, 3000), scale=(2048, 4096, 8192), selector=0):
    return struct.pack('<3i3h3h', *origin, 0, 0, 0, *scale)+bytes((0, selector, 0, 0))


def test_engine_file_rule_matches_004671d0():
    assert ol.sources(1) == ('LEVEL01', 'LEVEL01/LEVEL.DAT', 'LEVEL01/LEVEL.RAW', 'LEVEL01/TERRAIN.ALL')
    assert ol.sources(10)[1] == 'LEVEL10/LEVEL.DAT'
    assert ol.sources(11)[1:] == ('LEVEL01/LEVEL1.DAT', 'LEVEL01/LEVEL1.RAW', 'LEVEL01/TERR1.ALL')
    assert ol.sources(17)[1] == 'LEVEL07/LEVEL1.DAT'  # Training, EXP-20260812-010.
    assert ol.sources(6)[1] == 'LEVEL06/LEVEL.DAT'  # Cliffside, EXP-20260914-010.
    for bad in (0, 18, '3', True):
        with pytest.raises(ValueError):
            ol.sources(bad)
    assert sorted(p for _, p in ol.LEVELS.values() if p is not None) == list(range(16))


def test_every_masked_dispatch_and_undispatched_row_is_kept():
    dat = synthetic_dat([(0x13, unscaled(), sprites()),                     # yaw sprites
                         (0x1a, scaled(scale=(8192, 2048, 99)), sprites()),  # camera sprites, scaled
                         (0x14, unscaled(), negative_mesh()),                # dispatch 4
                         (0x93, unscaled(), sprites())],                     # 0x83: no 004498F0 case
                        index=(7, 8), secondary=[(0x12, unscaled(), sprites())])
    parsed, objects, undispatched = ol.scene_objects(dat, lambda _: IDENTITY)
    assert parsed.index_table_values == (7, 8)
    assert [o['kind'] for o in objects] == [ol.YAW, ol.CAMERA, ol.MESH4, ol.CAMERA]
    assert [o['section'] for o in objects] == ['primary']*3+['secondary']
    yaw, camera, mesh4, _ = objects
    assert yaw['sprites'][0]['center'] == [100, -200, 300] and yaw['sprite_scale'] == [4096, 4096]
    assert yaw['sprites'][0]['corners'][0] == [-10, -20]
    # Dispatch 10 scales quad X/Y by object +0x12/+0x14; +0x16 is only a depth bias.
    assert camera['sprite_scale'] == [8192, 2048] and camera['sprites'][0]['corners'][0] == [-20, -10]
    assert yaw['sprites'][0]['page'] == 2 and yaw['sprites'][0]['rgb'][1] == [40, 50, 60]
    assert mesh4['mesh_format'] == 'negative-count mesh' and mesh4['auxiliary']['bytes'] == 20
    assert mesh4['geometry_bytes'] == len(negative_mesh())
    assert mesh4['geometry_sha256'] == ol.digest(negative_mesh())
    assert [v['position'] for v in mesh4['vertices']] == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert mesh4['animation_selector'] == 0
    assert len(undispatched) == 1 and undispatched[0]['dispatch'] == 0x83
    assert undispatched[0]['origin'] == [1000, 2000, 3000]


def test_scaled_mesh_keeps_selector_and_truncates_toward_zero():
    mesh = struct.pack('<i', 1)+struct.pack('<3h6B', -3, 4, 5, 0, 0, 1, 2, 3, 0)+struct.pack('<2H6H', 0x61, 1, 0, 0, 0, 0, 0, 0)+b'\xff\xff'
    dat = synthetic_dat([(0x59, scaled(selector=0x2e), mesh)])
    _, (obj,), _ = ol.scene_objects(dat, lambda _: IDENTITY)
    assert obj['kind'] == ol.MESH and obj['animation_selector'] == 14
    assert obj['vertices'][0]['position'] == [-1, 4, 10] and obj['vertices'][0]['rgb'] == [1, 2, 3]


@pytest.mark.parametrize('mutation', ['pointer', 'negative', 'sprite'])
def test_bad_scene_geometry_rejects(mutation):
    geometry = {'pointer': negative_mesh(), 'negative': negative_mesh(), 'sprite': sprites()}[mutation]
    dat = bytearray(synthetic_dat([(0x14 if mutation != 'sprite' else 0x13, unscaled(), geometry)]))
    object_offset = struct.unpack_from('<I', dat, 8+16)[0]
    if mutation == 'pointer':
        struct.pack_into('<I', dat, object_offset+20, 4)  # into the prefix
    elif mutation == 'negative':
        struct.pack_into('<i', dat, object_offset+24, -6000)
    else:
        struct.pack_into('<i', dat, object_offset+24, 0)  # zero sprite centers
    with pytest.raises(ValueError):
        ol.scene_objects(bytes(dat), lambda _: IDENTITY)


def test_unimplemented_0x20_dispatch_family_refuses():
    with pytest.raises(ValueError, match='0x20'):
        ol.scene_objects(synthetic_dat([(0x21, unscaled(), sprites())]), lambda _: IDENTITY)


def test_fixed_record_variant_refuses():
    dat = bytearray(synthetic_dat([(0x13, unscaled(), sprites())]))
    struct.pack_into('<i', dat, 4, 1)
    with pytest.raises(ValueError):
        ol.scene_objects(bytes(dat), lambda _: IDENTITY)


def normals(count, corners, length=4096):
    return (struct.pack('<HBB', count, 0, 16)+b''.join(struct.pack('<4h', length, 0, 0, 0x110) for _ in range(count))
            + struct.pack(f'<{corners}H', *[0]*corners))


def test_normal_table_requires_unit_vectors_and_one_index_per_corner():
    good = normals(3, 8)
    assert ol.normal_table(good, 0, len(good), 8)['normals'] == 3
    assert ol.normal_table(good, 0, len(good), 7) is None
    assert ol.normal_table(normals(3, 8, 3000), 0, len(good), 8) is None
    assert ol.normal_table(b'\1\0', 0, 2, 0) is None


def test_creature_rows_and_names():
    payload = bytearray(struct.pack('<I', 0x23)+bytes(64*28))
    struct.pack_into('<3iBBB', payload, 4+2*28, -5, 6, 7, 9, 3, 0x20)
    struct.pack_into('<3iB', payload, 4+5*28, 1, 2, 3, 77)
    rows = ol.creature_rows(bytes(payload))
    assert [(r['slot'], r['type'], r['name']) for r in rows] == [(2, 9, 'spider'), (5, 77, None)]
    assert rows[1]['appearance'] is None and ol.APPEARANCE[30] == 'bird'
    assert rows[0]['position'] == [-5, 6, 7] and rows[0]['script'] == 3 and rows[0]['flags'] == 0x20
    with pytest.raises(ValueError):
        ol.creature_rows(bytes(payload[:-1]))
    with pytest.raises(ValueError):
        ol.creature_rows(struct.pack('<I', 0x24)+bytes(64*28))


def test_128_square_8bit_page_and_4bit_128_rejects():
    palette = bytes(v for i in range(256) for v in (i, 255-i, i))
    page = struct.pack('<I4H', 14, 128, 128, 768, 1)+palette+bytes(range(128))*128
    tag, width, indices, _, rgba = ol.texture_image(page)
    assert (tag, width, len(indices), len(rgba)) == (14, 128, 16384, 65536)
    assert ol.png(rgba, 128)[:8] == b'\x89PNG\r\n\x1a\n'
    with pytest.raises(ValueError):
        ol.texture_image(struct.pack('<I4H', 14, 128, 128, 768, 0)+palette+bytes(8192))
    with pytest.raises(ValueError):
        ol.texture_image(page[:-1])


def test_initialized_pickups_refuse_moved_xz_and_selector_changes():
    rows = [dict(index=0, offset=104, selector=0x14, stored_position=[1, 2, 3])]
    table = struct.pack('<hh', 1, 0x3f)+struct.pack('<3iI', 1, 9, 3, 0x14)
    assert ol.initialized_pickups([dict(r) for r in rows], 100, table)[0]['position'] == [1, 9, 3]
    for bad in (struct.pack('<hh', 1, 0x3f)+struct.pack('<3iI', 2, 9, 3, 0x14),
                struct.pack('<hh', 1, 0x3f)+struct.pack('<3iI', 1, 9, 3, 0x15),
                struct.pack('<hh', 2, 0x3f)+struct.pack('<3iI', 1, 9, 3, 0x14)):
        with pytest.raises(ValueError):
            ol.initialized_pickups([dict(r) for r in rows], 100, bad)


def test_read_inputs_rejects_changed_source(tmp_path):
    for relative in ol.sources(14)[1:]:
        (tmp_path/relative).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path/relative).write_bytes(b'not original')
    with pytest.raises(ValueError, match='exact original'):
        ol.read_inputs(tmp_path, 14)


def test_cli_refuses_outputs_outside_level_projects(tmp_path, monkeypatch):
    cli = runpy.run_path(str(ROOT/'scripts/map-original-levels.py'))
    monkeypatch.setattr('sys.argv', ['map-original-levels', '--out', str(tmp_path)])
    with pytest.raises(ValueError):
        cli['main']()


def retail():
    if not (CD/'LEVEL07/LEVEL1.DAT').exists():
        pytest.skip('Private retail fixture absent')
    from ablpc.original_level import NativeMatrices
    return NativeMatrices((ROOT/'work/copies/BUGS_PC-disc/bugs.exe').read_bytes())


def test_retail_training_and_cliffside_reproduce_earlier_imports():
    matrices = retail()
    training, _ = ol.extract(17, ol.read_inputs(CD, 17), matrices)
    cliffside, _ = ol.extract(6, ol.read_inputs(CD, 6), matrices)
    # EXP-20260909-012 and EXP-20260914-010 counts with the bounded importer.
    assert (training['counts']['vertices'], training['counts']['faces']) == (12414, 7953)
    assert training['counts']['collision_triangles'] == 1360 and training['counts']['barrier_segments'] == 80
    assert (cliffside['counts']['vertices'], cliffside['counts']['faces']) == (29308, 17093)
    assert {c['type'] for c in training['creatures']} == {9, 11, 38}


def test_retail_corpus_every_level_every_record():
    matrices = retail()
    totals = dict(records=0, undispatched=0, creatures=0)
    for engine in range(1, 18):
        scene, textures = ol.extract(engine, ol.read_inputs(CD, engine), matrices)
        counts = scene['counts']
        assert counts['drawn_objects']+counts['undispatched_records'] == counts['scene_records']
        assert set(textures) == {p['page'] for p in scene['textures']}
        assert {str(c['type']) for c in scene['creatures']} == set(scene['creature_models'])
        totals['records'] += counts['scene_records']; totals['undispatched'] += counts['undispatched_records']
        totals['creatures'] += counts['creatures']
    assert totals == dict(records=9951, undispatched=1, creatures=534)
