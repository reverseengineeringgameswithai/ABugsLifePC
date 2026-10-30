"""Synthetic skirts, source-boundary coverage and additive preservation."""

from fractions import Fraction
from pathlib import Path
import struct

import pytest

from ablpc.level_dat import LevelDat
from ablpc.terrain_additive import append_render_geometry
from ablpc.terrain_ramp_sides import buried_base, ground_boundary_spans, side_face_mesh
from ablpc.terrain_texture_tiling import cross, decode_mesh
from test_terrain_additive import appended_stream, dat, group, mesh, terrain


ROOT = Path(__file__).resolve().parents[1]
LEFT = ((0, 0, 0), (0, -64, 512), (0, -128, 1024))
RIGHT = ((256, -20, 0), (256, -70, 512), (256, -128, 1024))
SUFFIX = b"\x23\x01\x60\x60\x64\xb1"


def skirts(**overrides):
    options = dict(left=LEFT, right=RIGHT, origin=(0, 0, 0), bottom_y=700,
                   vertex_suffix=SUFFIX, anchor_z=0)
    options.update(overrides)
    return side_face_mesh(**options)


@pytest.mark.parametrize("bottom", [1, 512, 700, 1024])
def test_two_outward_sides_keep_exact_top_and_opaque_fields(bottom):
    stream, report = skirts(bottom_y=bottom)
    vertices, faces = decode_mesh(stream)
    points = [struct.unpack_from("<3h", raw) for raw in vertices]
    assert set(LEFT + RIGHT).issubset(points)
    assert report["triangle_count"] == len(faces)
    assert all(v[6:8] == SUFFIX[:2] and v[11] == SUFFIX[5] for v in vertices)
    for tag, indices, words in faces:
        corners = [points[i] for i in indices]
        assert tag == 0x61
        assert len({p[0] for p in corners}) == 1
        normal = cross(*corners)
        assert normal[1:] == (0, 0)
        assert normal[0] < 0 if corners[0][0] == 0 else normal[0] > 0
        assert all(64 <= word & 255 <= 127 and 192 <= word >> 8 <= 255 for word in words)
    for point in LEFT + RIGHT:
        raw = vertices[points.index(point)]
        assert raw[8:11] == bytes((114, 82, 60))
    assert all(raw[8:11] == bytes((98, 70, 50)) for raw, p in zip(vertices, points) if p[1] == bottom)


def test_no_new_top_vertices_or_triangle_above_the_existing_top_polyline():
    stream, _ = skirts()
    vertices, _ = decode_mesh(stream)
    points = [struct.unpack_from("<3h", raw) for raw in vertices]
    for edge in (LEFT, RIGHT):
        for point in (p for p in points if p[0] == edge[0][0]):
            column = next(p for p in edge if p[2] == point[2])
            assert point[1] >= column[1]


@pytest.mark.parametrize("options", [
    {"bottom_y": 0}, {"bottom_y": True}, {"bottom_y": 40000},
    {"vertex_suffix": b"short"}, {"vertex_suffix": bytearray(SUFFIX)},
    {"origin": (0, 0)}, {"origin": (True, 0, 0)}, {"origin": (40000, 0, 0)},
    {"top_channels": (256, 0, 0)}, {"bottom_channels": (1.0, 0, 0)},
    {"tile_size": 0}, {"tile_size": True}, {"anchor_z": 1.5},
    {"left": ()}, {"left": LEFT[::-1]}, {"left": ((0, 0, 0), (0, -128, 1024))},
    {"left": ((1, 0, 0),) + LEFT[1:]}, {"right": LEFT},
    {"right": RIGHT[:-1]},
])
def test_invalid_geometry_and_fields_reject(options):
    with pytest.raises(ValueError):
        skirts(**options)


def test_vertex_capacity_is_checked_before_uint16_encoding():
    left = tuple((0, -100, z) for z in range(0, 32769, 128))
    right = tuple((128, -100, z) for z in range(0, 32769, 128))
    with pytest.raises(ValueError, match="capacity"):
        skirts(left=left, right=right, origin=(0, 0, 1), bottom_y=30000, tile_size=128)


@pytest.mark.parametrize("trailer", [False, True])
@pytest.mark.parametrize("mixed", [False, True])
def test_addition_retains_all_original_vertices_faces_suffixes_and_storage(trailer, mixed):
    source_mesh = mesh(mixed=mixed)
    source = dat(source_mesh, trailer=trailer)
    extra, _ = skirts()
    candidate, _ = append_render_geometry(source, ((extra, (0, 0, 0)),), record_index=0)
    vertices, faces = decode_mesh(appended_stream(candidate))
    old_vertices, old_faces = decode_mesh(source_mesh)
    assert vertices[:len(old_vertices)] == old_vertices
    assert faces[:len(old_faces)] == old_faces
    allowed = set(range(20, 22)) | set(range(92, 96))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(source[:-4], candidate)))
    old_footer, new_footer = struct.unpack_from("<i", source, len(source)-4)[0], struct.unpack_from("<i", candidate, len(candidate)-4)[0]
    assert new_footer == (-1 if old_footer == -1 else old_footer + len(candidate) - len(source))


def test_original_triangle_intersection_has_exact_offsets_and_heights():
    source = terrain((group() + b"\xff\xff",))
    spans = ground_boundary_spans(source, source_index=0, x=128, z_start=0, z_end=128)
    assert len(spans) == 1
    assert spans[0]["cell_offset"] == 16
    assert spans[0]["z_start"] == 0 and spans[0]["z_end"] == 128
    assert spans[0]["height_start"] == spans[0]["height_end"] == 0
    assert buried_base(spans) == 256


@pytest.mark.parametrize("options", [{"x": 300}, {"z_end": 200}, {"source_index": 1},
    {"source_index": True}, {"z_start": 128}, {"x": True}])
def test_ground_boundary_rejects_gaps_and_bad_input(options):
    arguments = dict(source_index=0, x=128, z_start=0, z_end=128)
    arguments.update(options)
    with pytest.raises(ValueError):
        ground_boundary_spans(terrain((group() + b"\xff\xff",)), **arguments)


@pytest.mark.parametrize("source", [b"", b"\0\0", b"\xff" * 8, bytearray(terrain((group() + b"\xff\xff",)))])
def test_ground_parser_rejects_truncated_or_mutable_sources(source):
    with pytest.raises((ValueError, IndexError)):
        ground_boundary_spans(source, source_index=0, x=128, z_start=0, z_end=128)


def test_buried_base_rounds_downward_in_y_and_rejects_empty_evidence():
    assert buried_base([{"height_start": Fraction(-5, 2), "height_end": Fraction(-7, 3)}], burial=1) == -1
    with pytest.raises(ValueError):
        buried_base([])
    with pytest.raises(ValueError):
        buried_base([{"height_start": 0, "height_end": 1}], burial=True)


def test_private_original_boundary_planes_bound_the_buried_candidate():
    path = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/TERRAIN.ALL"
    if not path.is_file():
        pytest.skip("private original terrain unavailable")
    source = path.read_bytes()
    spans = [s for x in (5750, 6250) for s in ground_boundary_spans(source, source_index=99, x=x, z_start=10900, z_end=13000)]
    base = buried_base(spans)
    assert base > -1400
    assert all(base - s[key] >= 256 for s in spans for key in ("height_start", "height_end"))


def test_private_candidate_preserves_the_working_control():
    base = ROOT / "work/copies/EXP-20260906-001/fixture"
    candidate = ROOT / "work/copies/EXP-20260906-002/fixture"
    if not (candidate / "LEVEL.DAT").is_file():
        pytest.skip("isolated side-face candidate not built")
    before, after = (base / "LEVEL.DAT").read_bytes(), (candidate / "LEVEL.DAT").read_bytes()
    assert (base / "TERRAIN.ALL").read_bytes() == (candidate / "TERRAIN.ALL").read_bytes()
    old_ref = LevelDat.parse(before).static_mesh_reference("primary", 160)
    new_ref = LevelDat.parse(after).static_mesh_reference("primary", 160)
    old_count = struct.unpack_from("<i", before, old_ref.geometry_offset)[0]
    new_count = struct.unpack_from("<i", after, new_ref.geometry_offset)[0]
    assert old_count == 439 and new_count > old_count
    assert after[new_ref.geometry_offset+4:new_ref.geometry_offset+4+old_count*12] == before[old_ref.geometry_offset+4:old_ref.geometry_offset+4+old_count*12]
    old_commands = before[old_ref.geometry_offset+4+old_count*12:345872]
    start = new_ref.geometry_offset+4+new_count*12
    assert after[start:start+len(old_commands)] == old_commands
    allowed = set(range(18692,18696)) | {8592,8593}
    assert all(a == b or i in allowed for i,(a,b) in enumerate(zip(before[:-4],after)))
    assert struct.unpack_from("<h",after,8592)[0] >= 8560
