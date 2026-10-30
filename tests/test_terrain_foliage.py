import struct
from pathlib import Path

import pytest

from ablpc.terrain_foliage import (append_blades, append_scene_mesh, blade_templates,
                                  decode_mesh, encode_mesh, mesh_bytes, quarter_turn)


def synthetic():
    points = ((-50,-400,0),(50,-400,0),(50,0,10),(-50,0,10),(0,-800,-20))
    vertices = tuple(struct.pack("<3h",*p)+bytes((1,2,30+i,40+i,50+i,6))
                     for i,p in enumerate(points))
    quad = ((0,1,2,3),(0x3f00,0x3f1f,0x201f,0x2000))
    tri = ((1,0,4),(0x2000,0x201f,0x3f10))
    return encode_mesh(vertices, ((0x162,(quad,quad,quad)),(0x8163,(tri,))))


def test_roundtrip_and_unknown_bytes():
    raw=synthetic()
    assert encode_mesh(*decode_mesh(raw)) == raw
    templates=blade_templates(raw)
    assert len(templates)==3
    assert templates[0]['pivot']==(0,0,10)


@pytest.mark.parametrize('turn',range(4))
def test_reuse_preserves_fields_and_existing_mesh(turn):
    raw=synthetic();oldv,oldg=decode_mesh(raw)
    changed=append_blades(raw,raw,((100,200,300,turn),),(0,0,0))
    vertices,groups=decode_mesh(changed)
    assert vertices[:len(oldv)]==oldv and groups[:len(oldg)]==oldg
    assert tuple(v[6:] for v in vertices[-5:])==tuple(v[6:] for v in oldv)
    assert [g[0] for g in groups[-2:]]==[0x162,0x8163]
    assert groups[-2][1][0][1]==oldg[0][1][0][1]
    for old,new in zip(oldv,vertices[-5:]):
        x,y,z=struct.unpack_from('<3h',old)
        dx,dz=quarter_turn(x,z-10,turn)
        assert struct.unpack_from('<3h',new)==(100+dx,200+y,300+dz)


@pytest.mark.parametrize('raw',[b'',b'\0'*9,struct.pack('<i',-1)+b'\0'*30,
    struct.pack('<i',5463)+b'\0'*65562,synthetic()[:-1],synthetic()+b'x'])
def test_bad_mesh(raw):
    with pytest.raises(ValueError):decode_mesh(raw)


@pytest.mark.parametrize('offset,value',[(4+5*12+2,-1),(4+5*12+4,13),(4+5*12+4,65520)])
def test_bad_count_or_index(offset,value):
    raw=bytearray(synthetic());struct.pack_into('<H',raw,offset,value&65535)
    with pytest.raises(ValueError):decode_mesh(bytes(raw))


@pytest.mark.parametrize('placement',[(40000,0,0,0),(0,0,0,4),(0,0,0,-1),
                                     (2**31,0,0,0),(0.5,0,0,0),(0,0,0)])
def test_bad_placement(placement):
    with pytest.raises(ValueError):append_blades(synthetic(),synthetic(),(placement,),(0,0,0))


def test_ambiguous_tip_rejected():
    vertices,groups=decode_mesh(synthetic())
    raw=encode_mesh(vertices,groups+((0x8163,groups[-1][1]),))
    with pytest.raises(ValueError,match='unambiguous'):blade_templates(raw)


def test_vertex_capacity():
    vertices,groups=decode_mesh(synthetic())
    with pytest.raises(ValueError):encode_mesh(vertices*1100,groups)


@pytest.mark.parametrize('name',('LEVEL01','LEVEL03'))
def test_original_mesh_streams(name):
    from ablpc.level_dat import LevelDat
    path=Path('work/copies/BUGS_PC-full-disc/PC/BUGS/CD')/name/'LEVEL.DAT'
    if not path.exists():pytest.skip('private original copy unavailable')
    raw=path.read_bytes();level=LevelDat.parse(raw)
    refs=level.static_mesh_references('primary')[:12]
    assert refs
    for ref in refs:
        mesh,_=mesh_bytes(raw,ref.record_index)
        assert encode_mesh(*decode_mesh(mesh))==mesh


def test_private_growth_preserves_old_offsets():
    path=Path('work/copies/EXP-20260906-005/fixture/LEVEL.DAT')
    if not path.exists():pytest.skip('private control unavailable')
    raw=path.read_bytes();mesh,ref=mesh_bytes(raw,160)
    out,report=append_scene_mesh(raw,160,mesh)
    allowed=set(range(ref.object_offset+20,ref.object_offset+24))|set(range(ref.record_offset+12,ref.record_offset+14))
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(raw[:-4],out)))
    assert len(raw)-struct.unpack_from('<i',raw,len(raw)-4)[0]==len(out)-struct.unpack_from('<i',out,len(out)-4)[0]
    assert out[report['geometry_offset']:report['geometry_offset']+len(mesh)]==mesh
