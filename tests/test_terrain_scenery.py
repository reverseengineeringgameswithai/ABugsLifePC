"""Synthetic net-new scenery/descriptor growth and private native relocation."""
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import struct

import pytest

from ablpc.level_dat import LevelDat
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_scenery import (SceneryTemplate, append_instances, mushroom_template,
                                    read_mesh, scene_pointer_fields)
from test_terrain_additive import dat, terrain, group, mesh


def donor():
    scene = struct.pack('<3ihHI', 10, 20, 30, 1800, 0x19, 0)
    obj = struct.pack('<3i6hBBHI', 7, 8, 9, 123, 456, 789, 4096, 5000, 3000, 4, 0xc0, 0x1234, 0)
    t = TerrainAll.parse(terrain((group()+b'\xff\xff\x12\x34',)))
    return SceneryTemplate(scene, obj, mesh(), t.records[0].raw, t.collision_payload(0).raw)


def fixture():
    return dat(mesh()), terrain((group()+b'\xff\xff\x33\x44',))


@pytest.mark.parametrize('count', [1, 2, 8, 64])
def test_new_slots_and_full_preservation(count):
    d, t = fixture(); template = donor()
    positions = [(100+i*2000, -3000, 8000) for i in range(count)]
    out, col, meta = append_instances(d, t, template, positions)
    old, new = LevelDat.parse(d), LevelDat.parse(out)
    before, after = TerrainAll.parse(t), TerrainAll.parse(col)
    assert len(new.primary_records) == len(old.primary_records)+count
    assert len(after.records) == len(before.records)+count
    assert new.secondary_records == old.secondary_records == ()
    growth = count*20
    allowed = {f+j for f in scene_pointer_fields(d)[1] for j in range(4)}
    insertion = old.primary_sentinel_offset
    for i, value in enumerate(d[:-4]):
        if i not in allowed:
            assert out[i+(growth if i >= insertion else 0)] == value
    for f in scene_pointer_fields(d)[1]:
        assert struct.unpack_from('<I', out, f+(growth if f >= insertion else 0))[0] == struct.unpack_from('<I', d, f)[0]+growth
    assert len(out)-new.final_dword == len(d)-old.final_dword+growth
    assert col[4:before.directory_offset] == t[4:before.directory_offset]
    assert after.records[0].raw == before.records[0].raw
    assert after.collision_payload(0).raw == before.collision_payload(0).raw
    assert after.suffix == before.suffix
    for i, position in enumerate(positions):
        r = new.primary_records[1+i]; o = r.payload_offset_candidate
        assert struct.unpack_from('<3i', out, o) == position
        assert out[o+12:o+28] == template.object[12:28]
        assert out[r.offset+12:r.offset+16] == template.scene[12:16]
        assert read_mesh(out, struct.unpack_from('<I', out, o+28)[0]) == template.mesh
        assert after.collision_payload(1+i).raw == template.collision_payload
        assert after.records[1+i].raw[:4] == template.collision_record[:4]
        assert after.records[1+i].raw[16:] == template.collision_record[16:]
        assert (after.records[1+i].component_x, after.records[1+i].component_y, after.records[1+i].component_z) == tuple(position[k]-[7, 8, 9][k] for k in range(3))
    assert meta['scene_indices'] == list(range(1, count+1))


def test_add_more_later_keeps_previous_new_instances():
    d, t = fixture(); template = donor()
    first, c1, _ = append_instances(d, t, template, [(100, -3000, 8000)])
    second, c2, _ = append_instances(first, c1, template, [(3000, -3000, 8000)])
    p = LevelDat.parse(second)
    assert len(p.primary_records) == 3
    for i, x in [(1, 100), (2, 3000)]:
        assert struct.unpack_from('<3i', second, p.primary_records[i].payload_offset_candidate) == (x, -3000, 8000)
    assert TerrainAll.parse(c2).collision_payload(1).raw == TerrainAll.parse(c1).collision_payload(1).raw


def test_shared_mesh_saves_bytes_without_changing_collision_or_object_transforms():
    d,t=fixture();template=donor();positions=[(100,-3000,8000),(3000,-3000,8000)]
    shared,col,report=append_instances(d,t,template,positions,reuse_mesh=True)
    duplicate,expected,_=append_instances(d,t,template,positions)
    assert col==expected and report['mesh_reused']
    assert len(duplicate)-len(shared)==len(template.mesh)+(-len(template.mesh))%4
    records=LevelDat.parse(shared).primary_records
    pointers=[struct.unpack_from('<I',shared,r.payload_offset_candidate+(28 if r.flags&8 else 20))[0] for r in records]
    assert len(set(pointers))==1 and read_mesh(shared,pointers[0])==template.mesh
    for r,pos in zip(records[-2:],positions):
        assert struct.unpack_from('<3i',shared,r.payload_offset_candidate)==pos
        assert shared[r.payload_offset_candidate+12:r.payload_offset_candidate+28]==template.object[12:28]


def fixture_builder():
    path = Path(__file__).resolve().parents[1]/'scripts/terrain-scenery-fixture.py'
    spec = importlib.util.spec_from_file_location('scenery_fixture', path)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    return builder


@pytest.mark.parametrize('kept', [[], [0], [0, 2, 3, 4, 5], list(range(6)), list(range(7))])
def test_manifest_rebuild_adds_or_removes_visual_and_collision_together(monkeypatch, kept):
    builder = fixture_builder()
    monkeypatch.setattr(builder, 'mushroom_template', lambda *a, **kw: donor())
    d, t = fixture()
    control = {'LEVEL.DAT': d, 'TERRAIN.ALL': t, 'PLANTTER.ALL': t}
    placements = [{'variant': 'tall', 'origin': [100+i*2000, -3000, 8000]} for i in range(7)]
    source = {'LEVEL.DAT': d, 'TERRAIN.ALL': t}
    full, _ = builder.build(control, source, placements[:6])
    out, receipt = builder.build(control, source, [placements[i] for i in kept])
    parsed, collision = LevelDat.parse(out['LEVEL.DAT']), TerrainAll.parse(out['TERRAIN.ALL'])
    assert len(parsed.primary_records) == len(collision.records) == 1+len(kept)
    assert out['PLANTTER.ALL'] == control['PLANTTER.ALL']
    assert receipt['placements'] == [placements[i] for i in kept]
    for slot, i in enumerate(kept, 1):
        obj = parsed.primary_records[slot].payload_offset_candidate
        assert struct.unpack_from('<3i', out['LEVEL.DAT'], obj) == tuple(placements[i]['origin'])
        assert collision.records[slot].component_x == placements[i]['origin'][0]-7
        assert collision.collision_payload(slot).raw == donor().collision_payload
    if not kept:
        assert out == control
    if kept == list(range(6)):
        assert out == full
    assert control == {'LEVEL.DAT': d, 'TERRAIN.ALL': t, 'PLANTTER.ALL': t}


@pytest.mark.parametrize('name', ['LEVEL.DAT', 'TERRAIN.ALL', 'PLANTTER.ALL'])
def test_empty_manifest_still_rejects_truncated_inputs(name):
    d, t = fixture()
    control = {'LEVEL.DAT': d, 'TERRAIN.ALL': t, 'PLANTTER.ALL': t}
    control[name] = b'\x00'
    with pytest.raises(ValueError):
        fixture_builder().build(control, {}, [])


def test_private_approved_manifest_rebuilds_exact_six_mushroom_fixture():
    root = Path(__file__).resolve().parents[1]
    base = root/'work/copies/EXP-20260906-012/fixture'
    original = root/'work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01'
    if not base.exists() or not original.exists() or not (root/'config/terrain/test-area-mushrooms.json').exists():
        pytest.skip('private PC files unavailable')
    control = {n: (base/n).read_bytes() for n in ('LEVEL.DAT', 'TERRAIN.ALL', 'PLANTTER.ALL')}
    source = {n: (original/n).read_bytes() for n in ('LEVEL.DAT', 'TERRAIN.ALL')}
    placements = json.loads((root/'config/terrain/test-area-mushrooms.json').read_text())
    assert len(placements) == 6
    out, receipt = fixture_builder().build(control, source, placements)
    assert receipt['hashes'] == {
        'LEVEL.DAT': '409820b25e7422d3d3bd9a4d58b0eef10a1ed8b7aa581639f3c69ae10c778a37',
        'TERRAIN.ALL': 'b48b9d830f3182c8cacb4d330cd111ad451a6724c401a1946ac8de63cbda450a',
        'PLANTTER.ALL': 'c8251790b317e0458525d898237a54a88d473aac0758d01f36effcebeb38a762',
    }
    assert len(LevelDat.parse(out['LEVEL.DAT']).primary_records) == 490
    assert len(TerrainAll.parse(out['TERRAIN.ALL']).records) == 195


@pytest.mark.parametrize('positions', [[], [()], [(True, 0, 0)], [(1.5, 0, 0)], [(0, 0, 2**31)], [(0, 0, 0)]*65, None])
def test_invalid_placements(positions):
    with pytest.raises(ValueError):
        append_instances(*fixture(), donor(), positions)


@pytest.mark.parametrize('field,offset,fmt,value', [
    ('scene', 14, 'H', 0x41), ('scene', 12, 'h', -1), ('object', 25, 'B', 1),
    ('object', 18, 'h', 0), ('collision_record', 16, 'i', 7),
    ('collision_record', 68, 'h', 0), ('collision_record', 70, 'h', 1),
    ('collision_record', 0, 'I', 999999)])
def test_unsupported_template(field, offset, fmt, value):
    template = donor(); b = bytearray(getattr(template, field))
    struct.pack_into('<'+fmt, b, offset, value)
    with pytest.raises(ValueError):
        append_instances(*fixture(), replace(template, **{field: bytes(b)}), [(0, 0, 0)])


@pytest.mark.parametrize('field', ['scene', 'object', 'mesh', 'collision_record', 'collision_payload'])
def test_template_truncation_and_mutability(field):
    template = donor()
    for value in (getattr(template, field)[:1], bytearray(getattr(template, field))):
        with pytest.raises(ValueError):
            append_instances(*fixture(), replace(template, **{field: value}), [(0, 0, 0)])


@pytest.mark.parametrize('offset,fmt,value', [(22, 'H', 0x61), (24, 'I', 8), (92, 'I', 72), (92, 'I', 999999)])
def test_invalid_existing_pointer_layout(offset, fmt, value):
    d, t = fixture(); raw = bytearray(d); struct.pack_into('<'+fmt, raw, offset, value)
    with pytest.raises(ValueError):
        append_instances(bytes(raw), t, donor(), [(0, 0, 0)])


def test_overflowed_translated_center_or_collision_origin_rejected():
    with pytest.raises(ValueError):
        append_instances(*fixture(), donor(), [(2**31-1, 0, 0)])


@pytest.mark.parametrize('trailer', [False, True])
def test_footer_and_unaligned_input(trailer):
    source = dat(mesh(), trailer=trailer)
    # Original DAT/older appender can have word-aligned, not dword-aligned EOF.
    source = source[:-4]+b'\x12\x34'+struct.pack('<i', 326 if trailer else -1)
    out, _, _ = append_instances(source, fixture()[1], donor(), [(0, 0, 0)])
    a, b = LevelDat.parse(source), LevelDat.parse(out)
    assert b.primary_records[1].payload_offset_candidate % 4 == 0
    assert b.final_dword == -1 if not trailer else len(out)-b.final_dword == len(source)-a.final_dword+20


def test_private_original_and_mod_native_relocation_preserve_old_runtime_data():
    root = Path(__file__).resolve().parents[1]
    original = root/'work/copies/BUGS_PC-full-disc/PC/BUGS'
    mod = root/'work/copies/EXP-20260906-012/game/PC/BUGS/CD/LEVEL01'
    if not (original/'bugs.exe').exists() or not mod.exists():
        pytest.skip('private PC files unavailable')
    spec = importlib.util.spec_from_file_location('scenery_native_relocation', root/'scripts/terrain-texture-tiling-probe.py')
    native = importlib.util.module_from_spec(spec); spec.loader.exec_module(native)
    template = mushroom_template((original/'CD/LEVEL01/LEVEL.DAT').read_bytes(), (original/'CD/LEVEL01/TERRAIN.ALL').read_bytes())
    image = (original/'bugs.exe').read_bytes()
    for source in (original/'CD/LEVEL01', mod):
        d, t = ((source/n).read_bytes() for n in ('LEVEL.DAT', 'TERRAIN.ALL'))
        out, _, meta = append_instances(d, t, template, [(6000, -3200, 17000), (8000, -3200, 17000)])
        before, bg = native.relocate(image, d); after, ag = native.relocate(image, out)
        parsed, fields = scene_pointer_fields(d)
        normalized = bytearray(after[:parsed.primary_sentinel_offset]+after[parsed.primary_sentinel_offset+40:len(d)-4+40])
        for f in fields:
            v = struct.unpack_from('<I', normalized, f)[0]
            struct.pack_into('<I', normalized, f, v-40)
        assert bytes(normalized) == before[:-4]
        assert ag['trailing_data_pointer'] == bg['trailing_data_pointer']+40
        assert ag['trailing_plus_118_pointer'] == bg['trailing_plus_118_pointer']+40
        assert ag['trailer_table_sha256'] == bg['trailer_table_sha256']
        for r in LevelDat.parse(out).primary_records[-2:]:
            o = r.payload_offset_candidate
            assert struct.unpack_from('<I', after, r.offset+16)[0] == native.BASE+o
            assert struct.unpack_from('<I', after, o+28)[0] == native.BASE+meta['geometry_offset']
        assert after[meta['geometry_offset']:meta['geometry_offset']+len(template.mesh)] == template.mesh
