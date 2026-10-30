from pathlib import Path
import struct

import pytest

from ablpc.terrain_wall_material import build_material_pair, match_wall_stream, native_wall_profile
from ablpc.terrain_wall_shading import GEOMETRY_OFFSET, SOURCE_SIZE, decode


def fixture():
    points = [(0, 0, 0), (8, 0, 0), (0, 0, 8), (8, 0, 8), (0, 8, 0), (8, 8, 0)]
    vertices = b"".join(struct.pack("<3hh4B", *p, 0x1234, 96, 96, 100, 0xab) for p in points)
    top = struct.pack("<8H", 0, 12, 24, 36, 0xc03f, 0xc000, 0xff00, 0xff3f)
    wall = struct.pack("<8H", 0, 12, 48, 60, 0xc03f, 0xff3f, 0xc000, 0xff00)
    return struct.pack("<i", 6) + vertices + struct.pack("<2H", 0x60, 2) + top + wall + b"\xff\xff"


@pytest.mark.parametrize("texture,tint", [(False, False), (True, False), (False, True), (True, True)])
def test_independent_material_arms_preserve_geometry_and_other_faces(texture, tint):
    source = fixture()
    output, report = match_wall_stream(source, (114, 82, 60), (98, 70, 50), texture=texture, tint=tint)
    before, old_faces = decode(source)
    after, faces = decode(output)
    assert report["vertices_after"] == 8
    for face_index, ((old_refs, old_fields), (refs, fields)) in enumerate(zip(old_faces, faces)):
        for corner, (old_index, index) in enumerate(zip(old_refs, refs)):
            assert before[old_index][:8] == after[index][:8]
            assert before[old_index][11:] == after[index][11:]
            u, v = old_fields[corner * 2:corner * 2 + 2]
            assert fields[corner * 2:corner * 2 + 2] == bytes((u + 64 if face_index and texture else u, v))
            expected = bytes((114, 82, 60) if u == 63 else (98, 70, 50)) if face_index and tint else before[old_index][8:11]
            assert after[index][8:11] == expected


@pytest.mark.parametrize("channels", [(256, 0, 0), (-1, 0, 0), (True, 1, 2), (1.5, 1, 2), (1, 2)])
def test_invalid_colour_profile_rejected(channels):
    with pytest.raises(ValueError):
        match_wall_stream(fixture(), channels, (98, 70, 50))


def test_unknown_wall_uv_region_rejected():
    source = bytearray(fixture())
    source[4 + 6 * 12 + 4 + 16 + 8] = 64
    with pytest.raises(ValueError):
        match_wall_stream(bytes(source), (114, 82, 60), (98, 70, 50))


def test_source_guards():
    with pytest.raises(ValueError):
        native_wall_profile(b"not the original")
    with pytest.raises(ValueError):
        build_material_pair(b"wrong collision", b"wrong mesh", b"wrong original")


@pytest.mark.parametrize("texture,tint", [(True, False), (False, True), (True, True)])
def test_private_pair_preserves_collision_geometry_and_top(texture, tint):
    root = Path(__file__).resolve().parents[1]
    base = root / "work/copies/EXP-20260905-004/fixture"
    original_path = root / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/LEVEL.DAT"
    if not (base / "LEVEL.DAT").exists() or not original_path.exists():
        pytest.skip("Private PC assets are not distributed")
    terrain = (base / "TERRAIN.ALL").read_bytes()
    source = (base / "LEVEL.DAT").read_bytes()
    collision, output, report = build_material_pair(terrain, source, original_path.read_bytes(), texture=texture, tint=tint)
    assert collision is terrain
    assert report["donor"]["top_channels"] == (114, 82, 60)
    assert report["donor"]["bottom_channels"] == (98, 70, 50)
    size = report["mesh160_replaced_prefix_bytes"]
    assert (size, report["vertices_after"], report["wall_faces"]) == (1730, 78, 24)
    assert len(output) == len(source)
    assert output[:GEOMETRY_OFFSET] == source[:GEOMETRY_OFFSET]
    assert output[GEOMETRY_OFFSET + size:] == source[GEOMETRY_OFFSET + size:]
    before, old_faces = decode(source[GEOMETRY_OFFSET:GEOMETRY_OFFSET + SOURCE_SIZE])
    after, faces = decode(output[GEOMETRY_OFFSET:GEOMETRY_OFFSET + size])
    changed = {edit["face"] for edit in report["wall_face_edits"]}
    assert len(changed) == 24 and len(faces) == len(old_faces) == 49
    for face_index, ((old_refs, old_fields), (refs, fields)) in enumerate(zip(old_faces, faces)):
        for old_index, index in zip(old_refs, refs):
            assert before[old_index][:8] == after[index][:8]
            assert before[old_index][11:] == after[index][11:]
            if face_index not in changed:
                assert before[old_index] == after[index]
        if face_index not in changed or not texture:
            assert fields == old_fields
        else:
            assert fields[1::2] == old_fields[1::2]
            assert fields[::2] == bytes(u + 64 for u in old_fields[::2])
