"""Bounded ramp composition, byte preservation and original-PC route checks."""
from collections import Counter
import importlib.util
from pathlib import Path
import struct
import pytest
from ablpc import terrain_play_area as area
from ablpc.level_dat import LevelDat
from ablpc.terrain_all import TerrainAll

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('play_area',ROOT/'scripts/terrain-play-area.py')
probe=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(probe)


@pytest.fixture(scope='module')
def banked():
    if not (ROOT/'work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/TERRAIN.ALL').exists():
        pytest.skip('private Level01 fixture unavailable')
    return probe.reference('terrain-deck-grid-probe.py','area_test_grid').build(4,4,flip_top=True)


@pytest.fixture(scope='module')
def built(banked):
    return area.build(*banked[:2])


@pytest.fixture(scope='module')
def measured(banked):
    return probe.report()


@pytest.mark.parametrize('triangle', [[(0,0,0)]*3,[(0,0,0),(0,0,1)],
    [(0,0,0),(0,0,True),(1,0,0)],[(0,0,0),(0,0,32768),(1,0,0)],
    [(0,0,0),(0,8192,1),(1,0,0)]])
def test_invalid_or_overflowing_triangle_rejected(triangle):
    with pytest.raises(ValueError):area.encode_group(triangle,(0,0,0))


def test_synthetic_cell_fields_and_windows():
    raw=area.encode_group([(0,0,0),(0,0,64),(64,0,0)],(0,0,0))
    assert len(raw)==44
    assert struct.unpack_from('<6h',raw)==(1,1,0,64,0,64)
    assert struct.unpack_from('<3h',raw,12)==(0,-16384,0)
    assert struct.unpack_from('<4b',raw,40)==(0,1,0,1)


@pytest.mark.parametrize('offset,capacity,prefix', [(-1,2,b'x'),(2,4,b'x'),(0,1,b'xx'),(True,1,b'x')])
def test_prefix_bounds_reject(offset,capacity,prefix):
    with pytest.raises(ValueError):area.replace_prefix(b'abcd',offset,capacity,prefix)


def test_prefix_preserves_surrounding_unknown_bytes():
    assert area.replace_prefix(b'opaque:1234:tail',7,4,b'xy')==b'opaque:xy34:tail'


def test_requires_exact_banked_pair(banked):
    with pytest.raises(ValueError,match='banked'):area.build(banked[0]+b'x',banked[1])
    with pytest.raises(ValueError,match='banked'):area.build(banked[0],banked[1][:-1])


def test_only_allocated_prefixes_change(banked,built):
    t,d,m=built
    for old,new,start,size in ((banked[0],t,m['source99_payload_offset'],m['source99_replaced_prefix_bytes']),
                               (banked[1],d,m['mesh160_geometry_offset'],m['mesh160_replaced_prefix_bytes'])):
        assert len(old)==len(new)
        assert old[:start]==new[:start] and old[start+size:]==new[start+size:]
    assert m['mesh160_replaced_prefix_bytes']<=m['known_mesh_capacity']==2234
    assert m['depth_offset']==0


def test_top_and_opaque_vertex_fields_preserved(banked,built):
    old=LevelDat.parse(banked[1]).static_mesh_reference('primary',160)
    new=LevelDat.parse(built[1]).static_mesh_reference('primary',160)
    for a,b in zip(old.payload.faces[:17],new.payload.faces[:17],strict=True):
        assert a.vertex_byte_offsets==b.vertex_byte_offsets and a.field_words==b.field_words
        assert [old.payload.vertices[i//12].to_bytes() for i in a.vertex_byte_offsets]==[new.payload.vertices[i//12].to_bytes() for i in b.vertex_byte_offsets]
    assert {v.to_bytes()[6:] for v in new.payload.vertices}=={v.to_bytes()[6:] for v in old.payload.vertices}


def test_mesh_rim_and_midrow_edges_conform(built):
    ref=LevelDat.parse(built[1]).static_mesh_reference('primary',160)
    floor=area.DECK[4]-built[2]['mesh_origin'][1]
    edges=Counter()
    for face in ref.payload.faces:
        points=[struct.unpack_from('<3h',ref.payload.vertices[i//12].to_bytes()) for i in face.vertex_byte_offsets]
        for a,b in zip(points,points[1:]+points[:1]):edges[a,b]+=1
    for (a,b),count in edges.items():
        if a[1]!=floor or b[1]!=floor:assert count==edges[b,a]==1
    assert ref.payload.face_count==49


def test_collision_bounds_and_surface_normals(built):
    terrain=TerrainAll.parse(built[0]);r=terrain.records[99]
    groups=terrain.collision_payload(99).groups
    assert len(groups)==14
    for g,row in zip(groups,built[2]['cells'],strict=True):
        c=g.cells[0];assert c.offset==row['file_offset']
        assert c.words[:3]==tuple(row['normal'])
        yb,ys,zb,zs=struct.unpack_from('<4b',c.raw,28)
        for x,y,z in row['vertices']:
            x-=r.component_x;y-=r.component_y;z-=r.component_z
            assert g.minimum_x_units<=x<=g.minimum_x_units+g.span_x_units
            assert g.minimum_z_units<=z<=g.minimum_z_units+g.span_z_units
            assert c.words[4]+64*yb<=y<=c.words[4]+64*(yb+ys)
            assert c.words[5]+64*zb<=z<=c.words[5]+64*(zb+zs)
        if row['surface'] in ('deck','top','ramp'):assert c.words[1]<0
        if row['surface']=='north_wall':assert c.words[:3]==(0,0,-16384)
        if row['surface']=='south_wall':assert c.words[:3]==(0,0,16384)


def test_all_original_instruction_routes_and_controls(measured):
    assert measured['accepted']
    assert len(measured['routes'])==6
    for row in measured['routes']:
        for leg in ('uphill','downhill'):
            assert row[leg]['accepted'] and row[leg]['final']['flags']==[1,1]
    assert not measured['banked_closed_wall_control']['accepted']


def test_original_landings_and_step_off(measured):
    for row in measured['landings']:
        assert row['landing']['after']['flags']==[1,1]
        assert row['settle'][-1]['after']['flags']==[1,1]
    assert measured['step_off']['route']['accepted']


def test_writer_rejects_nonwork_and_existing(tmp_path):
    with pytest.raises(ValueError,match='work/copies'):probe.write_fixture(tmp_path/'bad')
    if not (ROOT / 'work/copies').is_dir():
        pytest.skip('retail work copies unavailable')
    with pytest.raises(FileExistsError):probe.write_fixture(ROOT/'work/copies')
