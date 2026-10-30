"""Synthetic format/tiling regressions plus pinned private PC file controls."""
from fractions import Fraction
from pathlib import Path
import runpy
import struct

import pytest

from ablpc.level_dat import LevelDat
from ablpc.terrain_texture_tiling import (
    SOURCE_OFFSET, SOURCE_SIZE, append_mesh, build_tiled_pair, cross, decode_mesh, tile_mesh,
)

ROOT = Path(__file__).resolve().parents[1]


def mesh(points=None, *, wall=False, unknown=b"\x23\x01", tail=177):
    points = points or [(0, 0, 0), (1024, 0, 0), (1024, 0, 1024), (0, 0, 1024)]
    vertices = [struct.pack("<3h", *p) + unknown + bytes((90, 80, 70, tail)) for p in points]
    u = 64 if wall else 0
    words = (u | 192 << 8, u+63 | 192 << 8, u+63 | 255 << 8, u | 255 << 8)
    return struct.pack("<i", 4) + b"".join(vertices) + struct.pack("<2H8H", 0x60, 1, 0, 12, 24, 36, *words) + b"\xff\xff"


def synthetic_dat(source, *, trailer=True):
    prefix = bytearray(96)
    struct.pack_into("<H", prefix, 8+14, 0x41)
    struct.pack_into("<I", prefix, 8+16, 72)
    struct.pack_into("<H", prefix, 28+14, 0xffff)
    struct.pack_into("<i", prefix, 48, -1)
    struct.pack_into("<H", prefix, 52+14, 0xffff)
    struct.pack_into("<I", prefix, 72+20, 96)
    out = bytes(prefix) + source + bytes((-len(source)) % 4)
    return out + (bytes(range(256)) + bytes(64) + struct.pack("<i", 324) if trailer else struct.pack("<i", -1))


@pytest.mark.parametrize("size", [128, 256, 512, 1024, 2048])
def test_repeated_tiles_cover_floor_without_atlas_wrap(size):
    output, report = tile_mesh(mesh(), (0, 0, 0), tile_size=size, anchor=(0, 0, 0))
    vertices, faces = decode_mesh(output)
    area = 0
    uv_origins = 0
    for tag, refs, fields in faces:
        xyz = [struct.unpack_from("<3h", vertices[i]) for i in refs]
        assert tag == 0x61
        area += abs(cross(*xyz)[1])
        assert all(0 <= (w & 255) <= 63 and 192 <= w >> 8 <= 255 for w in fields)
        uv_origins += 0xc000 in fields
    assert area == 2*1024*1024
    assert uv_origins >= max(1, (1024//size)**2)
    assert report["tile_size_world"] == size*32
    assert all(v[6:8] == b"\x23\x01" and v[8:] == bytes((90,80,70,177)) for v in vertices)


def test_wall_region_vertical_orientation_and_colour_interpolation():
    source = bytearray(mesh([(0, 0, 0), (0, -1024, 0), (0, -1024, 1024), (0, 0, 1024)], wall=True))
    for index in (1, 2):
        source[4+index*12+8:4+index*12+11] = bytes((110,100,90))
    output, report = tile_mesh(bytes(source), (0,0,0), anchor=(0,0,0))
    vertices, faces = decode_mesh(output)
    assert report["surface_triangles"]["ground"] == 0
    assert all(64 <= (w & 255) <= 127 and 192 <= w >> 8 <= 255 for _,_,fields in faces for w in fields)
    assert any(struct.unpack_from("<3h", v)[1] == -512 and v[8:11] == bytes((100,90,80)) for v in vertices)


def test_negative_tile_coordinates_and_original_diagonal_containment():
    source = mesh([(-750,0,-750), (250,0,-750), (250,0,250), (-750,0,250)])
    output, report = tile_mesh(source, (0,0,0), anchor=(0,0,0))
    vertices, faces = decode_mesh(output)
    assert any(min(row["tile"]) < 0 for row in report["faces"])
    for (_, refs, _), provenance in zip(faces, report["faces"]):
        positions = [struct.unpack_from("<3h", vertices[i]) for i in refs]
        signs = [x-z for x,_,z in positions]
        assert min(signs) >= 0 if provenance["source_triangle"] == 0 else max(signs) <= 0


def test_slope_rounding_is_explicit_and_bounded():
    output, report = tile_mesh(mesh([(0,0,0),(1400,-192,0),(1400,-192,700),(0,0,700)]), (0,0,0), anchor=(0,0,0))
    vertices, _ = decode_mesh(output)
    assert Fraction(report["max_coordinate_rounding_error_stored"]) <= Fraction(1,2)
    assert all(abs(Fraction(v[0]*192,1400) + v[1]) <= Fraction(1,2) for v in (struct.unpack_from("<3h", r) for r in vertices))


@pytest.mark.parametrize("size", [0, 127, 2049, True, 512.0])
def test_invalid_tile_size(size):
    with pytest.raises(ValueError):
        tile_mesh(mesh(), (0,0,0), tile_size=size)


@pytest.mark.parametrize("mutation", ["short", "negative_vertices", "huge_vertices", "reference", "negative_faces", "tag", "terminator", "extra"])
def test_bounds_checked_parser(mutation):
    data = bytearray(mesh())
    if mutation == "short": data = data[:3]
    elif mutation == "negative_vertices": struct.pack_into("<i", data, 0, -1)
    elif mutation == "huge_vertices": struct.pack_into("<i", data, 0, 2**30)
    elif mutation == "reference": struct.pack_into("<H", data, 56, 49)
    elif mutation == "negative_faces": struct.pack_into("<h", data, 54, -1)
    elif mutation == "tag": struct.pack_into("<H", data, 52, 0x62)
    elif mutation == "terminator": data = data[:-1]
    elif mutation == "extra": data += b"\x00"
    with pytest.raises(ValueError): decode_mesh(bytes(data))


def test_unknown_fields_and_unexpected_atlas_are_rejected():
    source = bytearray(mesh())
    source[4+12+6] ^= 1
    with pytest.raises(ValueError, match="unidentified"):
        tile_mesh(bytes(source), (0,0,0))
    source = bytearray(mesh())
    source[56+8] = 128
    with pytest.raises(ValueError, match="atlas"):
        tile_mesh(bytes(source), (0,0,0))


@pytest.mark.parametrize("trailer", [True, False])
def test_growth_changes_only_pointer_and_known_footer(trailer):
    source = synthetic_dat(mesh(), trailer=trailer)
    tiled, _ = tile_mesh(mesh(), (0,0,0), anchor=(0,0,0))
    output, report = append_mesh(source, tiled, record_index=0, expected_geometry=96)
    assert output[:92] == source[:92]
    assert output[96:len(source)-4] == source[96:-4]
    ref = LevelDat.parse(output).static_mesh_reference("primary", 0)
    assert ref.geometry_offset == len(source)-4
    assert output[ref.geometry_offset:ref.geometry_offset+len(tiled)] == tiled
    assert len(output) % 4 == 0
    if trailer:
        assert len(source)-324 == len(output)-struct.unpack_from("<i", output, len(output)-4)[0]
    else:
        assert output[-4:] == b"\xff"*4
    assert report["growth_bytes"] == len(output)-len(source)


@pytest.mark.parametrize("value", [0, 4, 279, 2**30, -2])
def test_invalid_trailer_span(value):
    source = synthetic_dat(mesh())[:-4] + struct.pack("<i", value)
    with pytest.raises(ValueError, match="trailing-data"):
        append_mesh(source, mesh(), record_index=0, expected_geometry=96)


def test_wrong_geometry_and_misaligned_file():
    source = synthetic_dat(mesh())
    with pytest.raises(ValueError): append_mesh(source, mesh(), record_index=0, expected_geometry=100)
    with pytest.raises(ValueError): append_mesh(source+b"x", mesh(), record_index=0, expected_geometry=96)


@pytest.fixture(scope="module")
def private_pair():
    root = ROOT / "work/copies/EXP-20260905-005/material-fixture"
    if not (root / "LEVEL.DAT").is_file():
        pytest.skip("Private PC fixture unavailable")
    return (root / "TERRAIN.ALL").read_bytes(), (root / "LEVEL.DAT").read_bytes()


@pytest.mark.parametrize("size", [512, 1024])
def test_private_pair_preserves_collision_and_old_payloads(private_pair, size):
    terrain, dat = private_pair
    same, output, report = build_tiled_pair(terrain, dat, tile_size=size)
    assert same is terrain
    pointer = 18692
    assert dat[:pointer] == output[:pointer]
    assert dat[pointer+4:-4] == output[pointer+4:len(dat)-4]
    assert output[SOURCE_OFFSET:SOURCE_OFFSET+SOURCE_SIZE] == dat[SOURCE_OFFSET:SOURCE_OFFSET+SOURCE_SIZE]
    assert report["tiling"]["stream_bytes"] > 2234
    assert Fraction(report["tiling"]["max_coordinate_rounding_error_stored"]) <= Fraction(1,2)
    parsed = LevelDat.parse(output).static_mesh_reference("primary", 160)
    assert parsed.geometry_offset == len(dat)-4


def test_private_input_hash_guards(private_pair):
    terrain, dat = private_pair
    with pytest.raises(ValueError): build_tiled_pair(terrain+b"x", dat)
    with pytest.raises(ValueError): build_tiled_pair(terrain, dat+b"x")


def test_original_pc_relocator_preserves_trailing_data(private_pair):
    pytest.importorskip("unicorn")
    pytest.importorskip("pefile")
    image = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe"
    if not image.is_file(): pytest.skip("Private original PC executable unavailable")
    terrain, dat = private_pair
    _, candidate, report = build_tiled_pair(terrain, dat)
    compare = runpy.run_path(str(ROOT / "scripts/terrain-texture-tiling-probe.py"))["compare"]
    result = compare(image.read_bytes(), dat, candidate, report["allocation"]["geometry_offset"], report["tiling"]["stream_bytes"])
    assert result["passed"], result
