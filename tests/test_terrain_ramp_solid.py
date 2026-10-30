"""Ground clipping and box-style wall cell bounds/preservation regressions."""
from fractions import Fraction as F
from pathlib import Path
import struct

import pytest

from ablpc.level_dat import LevelDat
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_floor_patch import mesh_groups
from ablpc.terrain_height import CellWords
from ablpc.terrain_ramp_solid import render_profile,profile_y,trim_side_mesh,side_collision
from ablpc.terrain_texture_tiling import decode_mesh,cross
from test_terrain_additive import dat,mesh,terrain
from test_terrain_ramp_sides import LEFT,RIGHT,SUFFIX,skirts

ROOT=Path(__file__).resolve().parents[1]


def profile():
    return [dict(lo=F(0),hi=F(512),y_lo=F(100),y_hi=F(300)),dict(lo=F(512),hi=F(1024),y_lo=F(300),y_hi=F(100))]


def test_box_style_normals_edges_and_height_windows():
    stream,rows=side_collision(LEFT,RIGHT,origin=(0,0,0),bottom_y=700)
    parsed=TerrainAll.parse(terrain((stream,)))
    cells=[c for g in parsed.collision_payload(0).groups for c in g.cells]
    assert len(cells)==len(rows)==8
    for cell,row in zip(cells,rows):
        fields=CellWords.parse(cell.raw)
        assert fields.divisor==0 and fields.slope_z==0
        assert fields.slope_x==(-16384 if row['side']=='west' else 16384)
        a,b,c=row['vertices']
        assert (fields.x0,fields.h0,fields.z0)==a
        assert (fields.dx1,fields.dz1)==(b[0]-a[0],b[2]-a[2])
        assert (fields.dx2,fields.dz2)==(c[0]-a[0],c[2]-a[2])
        lower,span=struct.unpack_from('<2b',cell.raw,28)
        assert all(a[1]+lower*64<=p[1]<=a[1]+(lower+span)*64 for p in row['vertices'])


@pytest.mark.parametrize('kwargs',[{'skin':True},{'skin':257},{'bottom_y':-1000},{'left':LEFT[::-1]},{'right':LEFT},{'origin':(40000,0,0)},{'left':[]}])
def test_wall_rejects_invalid_geometry(kwargs):
    args=dict(left=LEFT,right=RIGHT,origin=(0,0,0),bottom_y=700);args.update(kwargs)
    with pytest.raises(ValueError):side_collision(**args)


def test_clipped_walls_stay_above_ground_with_material_and_opaque_fields():
    source,_=skirts();profiles={0:profile(),256:profile()}
    result,report=trim_side_mesh(source,origin=(0,0,0),profiles=profiles)
    vertices,faces=decode_mesh(result)
    points=[struct.unpack_from('<3h',v) for v in vertices]
    assert report['original_faces']>0 and report['faces']==len(faces)
    assert set(LEFT+RIGHT)<=set(points)
    for v,p in zip(vertices,points):
        assert p[1]<=profile_y(profiles[p[0]],p[2])
        assert v[6:8]==SUFFIX[:2] and v[11]==SUFFIX[5]
    for tag,ids,words in faces:
        p=[points[i] for i in ids];n=cross(*p)
        assert tag==0x61 and n[1:]==(0,0)
        assert n[0]<0 if p[0][0]==0 else n[0]>0
        assert all(64<=w&255<=127 and 192<=w>>8<=255 for w in words)


@pytest.mark.parametrize('end',[0,2,8,30])
def test_truncated_skirt_is_rejected(end):
    source,_=skirts()
    with pytest.raises(ValueError):trim_side_mesh(source[:end],origin=(0,0,0),profiles={0:profile(),256:profile()})


@pytest.mark.parametrize('profiles',[{}, {0:[]}, {0:[dict(lo=0,hi=0,y_lo=0,y_hi=1)]}, {0:profile()}])
def test_invalid_profile_or_missing_side_rejects(profiles):
    with pytest.raises(ValueError):trim_side_mesh(skirts()[0],origin=(0,0,0),profiles=profiles)


def test_ground_profile_reads_both_synthetic_footer_variants():
    # The existing fixture is already wound as an upward render face.
    raw=mesh()
    for trailer in (False,True):
        rows=render_profile(dat(bytes(raw),trailer=trailer),records=(0,),x=512,z_start=0,z_end=1024)
        assert profile_y(rows,128)==profile_y(rows,900)==0


@pytest.mark.parametrize('source',[b'',b'\0\0',bytearray(dat(mesh()))])
def test_bad_dat_input_rejects(source):
    with pytest.raises((ValueError,IndexError)):
        render_profile(source,records=(0,),x=512,z_start=0,z_end=1024)


def test_private_pair_preserves_existing_cells_top_and_other_meshes():
    base=ROOT/'work/copies/EXP-20260906-001/fixture';out=ROOT/'work/copies/EXP-20260906-003/fixture'
    if not (out/'LEVEL.DAT').is_file():pytest.skip('private candidate not built')
    old=TerrainAll.from_path(base/'TERRAIN.ALL');new=TerrainAll.from_path(out/'TERRAIN.ALL')
    for i in range(len(old.records)):
        a,b=old.records[i],new.records[i]
        if i==99:
            pa,pb=old.collision_payload(i),new.collision_payload(i)
            assert pb.groups[:len(pa.groups)]==pa.groups
            assert sum(g.cell_count for g in pb.groups)-sum(g.cell_count for g in pa.groups)==20
        else:
            assert a.raw==b.raw
            assert old.data[a.payload_offset:a.payload_offset+a.payload_size]==new.data[b.payload_offset:b.payload_offset+b.payload_size]
    a,b=LevelDat.from_path(base/'LEVEL.DAT'),LevelDat.from_path(out/'LEVEL.DAT')
    ra,rb=a.static_mesh_reference('primary',160),b.static_mesh_reference('primary',160)
    assert b.data[rb.geometry_offset+4:rb.geometry_offset+4+439*12]==a.data[ra.geometry_offset+4:ra.geometry_offset+4+439*12]
    ga,ea=mesh_groups(a.data,ra);gb,eb=mesh_groups(b.data,rb)
    ca=ra.payload.vertices_offset+439*12;cb=rb.payload.vertices_offset+rb.payload.vertex_count*12
    assert b.data[cb:cb+ea-ca]==a.data[ca:ea]
    for i in (124,128,213,280):assert a.static_mesh_reference('primary',i)==b.static_mesh_reference('primary',i)
    allowed=set(range(18692,18696))|{8592,8593}
    assert all(x==y or i in allowed for i,(x,y) in enumerate(zip(a.data[:-4],b.data)))
    assert struct.unpack_from('<h',b.data,8592)[0]>=8560
