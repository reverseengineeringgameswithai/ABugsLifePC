"""Bounded depth experiments preserve physics and the covered box surfaces."""
from pathlib import Path
import importlib.util
import struct
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('deck_visual', ROOT/'scripts/terrain-deck-visual-probe.py')
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


@pytest.mark.parametrize('options', [dict(divisions=0), dict(divisions=8),
                                   dict(depth_offset=1), dict(depth_offset=True)])
def test_unsupported_variants_rejected(options):
    with pytest.raises(ValueError):
        probe.build(**options)


def test_synthetic_bilinear_quad_preserves_corners_and_center():
    corners = [(0,2,0), (8,2,0), (8,2,12), (0,2,12)]
    assert probe.interpolate(corners, 0, 0) == corners[0]
    assert probe.interpolate(corners, 1, 1) == corners[2]
    assert probe.interpolate(corners, .5, .5) == (4,2,6)


@pytest.fixture(scope='module')
def variants():
    base = probe.reference()
    if not (base.SOURCE/'LEVEL.DAT').is_file():
        pytest.skip('retail work copies unavailable')
    return {key: probe.build(stationary=True, depth_offset=bias, divisions=div)
            for key, bias, div in [('control',8,1),('zero',0,1),('split',0,4)]}


def test_offset_pair_diff_is_one_byte_and_physics_identical(variants):
    a,b = variants['control'], variants['zero']
    assert a[0] == b[0] == variants['split'][0]
    assert len(a[1]) == len(b[1])
    assert [i for i,(x,y) in enumerate(zip(a[1],b[1])) if x != y] == [18690]
    assert (a[1][18690],b[1][18690]) == (8,0)


def test_subdivision_only_changes_known_mesh_span(variants):
    _,a,am = variants['zero']; _,b,bm = variants['split']
    start=bm['mesh160_geometry_offset'];end=start+bm['mesh160_replaced_prefix_bytes']
    assert len(a)==len(b) and a[:start]==b[:start] and a[end:]==b[end:]
    assert (bm['vertex_count'],bm['face_count'])==(45,33)
    base=probe.reference();ref=base.LevelDat.parse(b).static_mesh_reference('primary',160)
    assert b[ref.payload.end_offset:ref.payload.end_offset+2]==b'\xff\xff'


def test_subdivided_faces_cover_same_planes_with_same_winding(variants):
    base=probe.reference(); _,raw,_=variants['split']
    ref=base.LevelDat.parse(raw).static_mesh_reference('primary',160)
    origin=struct.unpack_from('<3i',raw,ref.object_offset)
    vertices=[tuple(v+origin[i] for i,v in enumerate(struct.unpack_from('<3h',row.to_bytes())))
              for row in ref.payload.vertices]
    areas={};normals={}
    # Exact integer cross products: sum area per axis plane, preserving sign.
    for face in ref.payload.faces:
        q=[vertices[i//12] for i in face.vertex_byte_offsets]
        u=[q[1][i]-q[0][i] for i in range(3)];v=[q[3][i]-q[0][i] for i in range(3)]
        cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
        axes=[i for i,x in enumerate(cross) if x];assert len(axes)==1
        axis=axes[0];assert len({p[axis] for p in q})==1
        key=(axis,q[0][axis]);areas[key]=areas.get(key,0)+abs(cross[axis])
        normals.setdefault(key,set()).add(1 if cross[axis]>0 else -1)
    x0,x1,z0,z1,top=probe.STATIONARY_BOX;floor=base.DECK[4]
    assert areas == {(1,floor):4300*5100,(1,top):650*700,
                     (0,x0):192*700,(0,x1):192*700,
                     (2,z0):192*650,(2,z1):192*650}
    assert normals == {(1,floor):{-1},(1,top):{-1},(0,x0):{-1},(0,x1):{1},
                       (2,z0):{-1},(2,z1):{1}}


def test_asset_output_rejects_outside_workspace(tmp_path):
    with pytest.raises(ValueError, match='work/copies'):
        probe.write_fixture(tmp_path/'fixture')
