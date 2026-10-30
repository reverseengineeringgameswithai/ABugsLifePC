"""Fixed flat-deck geometry, original collision controls and byte preservation."""
from pathlib import Path
import importlib.util
import struct
import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('deck_probe',ROOT/'scripts/terrain-deck-probe.py')
probe=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(probe)

@pytest.fixture(scope='module')
def built():
    if not (probe.SOURCE/'TERRAIN.ALL').exists():
        pytest.skip('retail work copies unavailable')
    return probe.build()

@pytest.fixture(scope='module')
def measured():
    if not (probe.SOURCE/'TERRAIN.ALL').exists():
        pytest.skip('retail work copies unavailable')
    return probe.report()

@pytest.mark.parametrize('tri,normal',[
    ([(0,0,0),(0,0,10),(10,0,0)],(0,-16384,0)),
    ([(0,0,0),(0,0,10),(0,10,0)],(16384,0,0)),
    ([(0,0,0),(0,10,0),(10,0,0)],(0,0,16384)),
])
def test_directed_collision_normal_matches_demonstrated_axes(tri,normal):
    assert probe.normal(tri)==normal
    assert probe.normal([tri[0],tri[2],tri[1]])==tuple(-x for x in normal)


def test_degenerate_triangle_rejected():
    with pytest.raises(AssertionError):
        probe.normal([(0,0,0)]*3)


def test_only_explicit_source_prefix_and_scene_center_change(built):
    terrain,dat,meta=built
    oldterrain=(probe.SOURCE/'TERRAIN.ALL').read_bytes();olddat=(probe.SOURCE/'LEVEL.DAT').read_bytes()
    start=meta['source99_payload_offset'];end=start+meta['source99_replaced_prefix_bytes']
    assert len(terrain)==len(oldterrain)
    assert terrain[:start]==oldterrain[:start] and terrain[end:]==oldterrain[end:]
    start=meta['mesh160_geometry_offset'];end=start+meta['mesh160_replaced_prefix_bytes'];scene=meta['scene_record_offset']
    assert len(dat)==len(olddat)
    assert all(a==b or start<=i<end or scene<=i<scene+12 for i,(a,b) in enumerate(zip(dat,olddat,strict=True)))
    assert dat[scene+12:scene+20]==olddat[scene+12:scene+20]


def test_generated_normals_edges_and_bounds_enclose_every_triangle(built):
    terrain,_,meta=built;t=probe.TerrainAll.parse(terrain);r=t.records[99];groups=t.collision_payload(99).groups
    assert len(groups)==12
    for g,row in zip(groups,meta['cells'],strict=True):
        assert len(g.cells)==1;cell=g.cells[0];w=cell.words
        assert cell.offset==row['file_offset'] and tuple(row['normal'])==w[:3]
        ybase,yspan,zbase,zspan=struct.unpack_from('<4b',cell.raw,28)
        for xyz in row['vertices']:
            x,y,z=(xyz[i]-(r.component_x,r.component_y,r.component_z)[i] for i in range(3))
            assert g.minimum_x_units<=x<=g.minimum_x_units+g.span_x_units
            assert g.minimum_z_units<=z<=g.minimum_z_units+g.span_z_units
            assert w[12]<=x<=w[12]+w[13]
            assert w[4]+64*ybase<=y<=w[4]+64*(ybase+yspan)
            assert w[5]+64*zbase<=z<=w[5]+64*(zbase+zspan)
            assert sum(w[i]*(v-w[i+3]) for i,v in enumerate((x,y,z)))==0


def test_render_prefix_has_exactly_six_quads_and_a_terminator(built):
    _,dat,meta=built;ref=probe.LevelDat.parse(dat).static_mesh_reference('primary',160)
    assert ref.payload.vertex_count==24 and ref.payload.face_count==6
    assert ref.payload.tag==0x60
    assert dat[ref.payload.end_offset:ref.payload.end_offset+2]==b'\xff\xff'
    assert ref.payload.end_offset+2==ref.geometry_offset+meta['mesh160_replaced_prefix_bytes']


def test_original_roundtrip_stays_on_flat_deck(measured):
    c=measured['cases']['deck_roundtrip']
    assert c['landing']['after']['flags']==[1,1]
    assert c['steps'][-1]['after']['position']==c['landing']['after']['position']
    assert all(s['after']['position'][1]==-102403 for s in c['steps'])


def test_side_control_blocks_return_and_removal_permits_entry(measured):
    cases=measured['cases'];full=cases['approach_reverse']['steps'][:25];removed=cases['without_sides']['steps']
    assert min(s['after']['position'][0] for s in full)>=5750*32
    end=removed[-1]['after']['position'];assert 5100*32<end[0]<5750*32 and 15550*32<end[2]<16250*32
    assert -102404<=end[1]<=-102400
    returned=cases['top_leave_return']['steps'][-1]['after']['position']
    assert returned[0]>=5750*32 and -102404<=returned[1]<=-102400


def test_top_control_lands_on_block_then_deck_and_removal_changes_landing(measured):
    cases=measured['cases'];full=cases['top_leave_return']
    assert full['landing']['after']['position'][1]==-108547 and full['landing']['after']['flags']==[1,1]
    assert -102404<=full['steps'][24]['after']['position'][1]<=-102400
    absent=cases['without_top'];assert absent['landing']['after']['flags']==[0,0]
    assert absent['steps'][-1]['after']['position'][1]==-102403


def test_asset_output_refuses_nonwork_path_and_existing_directory(tmp_path):
    with pytest.raises(ValueError,match='work/copies'):
        probe.write_fixture(tmp_path/'deck')
    if not (ROOT / 'work/copies').is_dir():
        pytest.skip('retail work copies unavailable')
    with pytest.raises(FileExistsError):
        probe.write_fixture(ROOT/'work/copies')
