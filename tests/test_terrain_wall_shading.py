import struct
from pathlib import Path

import pytest

from ablpc.terrain_wall_shading import (
    GEOMETRY_OFFSET, SOURCE_SIZE, decode, shade_level_dat, shade_quad_stream,
)


def fixture():
    points = [(0, 0, 0), (8, 0, 0), (0, 0, 8), (8, 0, 8), (0, 8, 0), (8, 8, 0)]
    vertices = b"".join(struct.pack("<3hh4B", *point, 0x1234, 96, 96, 100, 0xab) for point in points)
    faces = b"".join(struct.pack("<8H", *(i * 12 for i in refs), 1, 2, 3, 4)
                     for refs in [(0, 1, 2, 3), (0, 1, 4, 5)])
    return struct.pack("<i", 6) + vertices + struct.pack("<2H", 0x60, 2) + faces + b"\xff\xff"


def test_wall_darkens_without_bleeding_onto_top():
    source = fixture()
    shaded, report = shade_quad_stream(source)
    before, old_faces = decode(source)
    after, faces = decode(shaded)
    assert report["vertices_after"] == 8
    assert report["duplicated_boundary_vertices"] == [0, 1]
    for face_index, ((old_refs, old_fields), (refs, fields)) in enumerate(zip(old_faces, faces)):
        assert old_fields == fields
        for old_index, index in zip(old_refs, refs):
            assert before[old_index][:8] == after[index][:8]
            assert before[old_index][11:] == after[index][11:]
            assert after[index][8:11] == (bytes((57, 57, 60)) if face_index else before[old_index][8:11])


@pytest.mark.parametrize("data", [b"", b"\x00" * 10, struct.pack("<i", -1) + b"\x00" * 20,
                                  fixture()[:-1], fixture() + b"\x00", fixture()[:12]])
def test_rejects_bad_counts_truncation_and_trailing_data(data):
    with pytest.raises(ValueError):
        decode(data)


@pytest.mark.parametrize("reference", [1, 72, 65535])
def test_rejects_bad_references(reference):
    data = bytearray(fixture())
    struct.pack_into("<H", data, 4 + 6 * 12 + 4, reference)
    with pytest.raises(ValueError):
        decode(bytes(data))


@pytest.mark.parametrize("numerator,denominator", [(True, 5), (3, False), (-1, 5), (6, 5), (3, 0), (0.5, 1)])
def test_rejects_invalid_ratio(numerator, denominator):
    with pytest.raises(ValueError):
        shade_quad_stream(fixture(), numerator, denominator)


def test_rejects_unknown_tag():
    data = bytearray(fixture())
    struct.pack_into("<H", data, 4 + 6 * 12, 0x61)
    with pytest.raises(ValueError):
        decode(bytes(data))


def test_rejects_unpinned_dat():
    with pytest.raises(ValueError):
        shade_level_dat(b"\x00" * 120000)


def test_real_fixture_changes_only_wall_appearance():
    path = Path(__file__).resolve().parents[1] / "work/copies/EXP-20260905-004/fixture/LEVEL.DAT"
    if not path.exists():
        pytest.skip("Private EXP-004 asset is not distributed")
    source = path.read_bytes()
    shaded, report = shade_level_dat(source)
    size = report["stream_bytes_after"]
    assert len(source) == len(shaded)
    assert shaded[:GEOMETRY_OFFSET] == source[:GEOMETRY_OFFSET]
    assert shaded[GEOMETRY_OFFSET + size:] == source[GEOMETRY_OFFSET + size:]
    assert (report["vertices_after"], report["wall_faces"], size) == (78, 24, 1730)
    before, old_faces = decode(source[GEOMETRY_OFFSET:GEOMETRY_OFFSET + SOURCE_SIZE])
    after, faces = decode(shaded[GEOMETRY_OFFSET:GEOMETRY_OFFSET + size])
    assert len(old_faces) == len(faces) == 49
    for (old_refs, old_fields), (refs, fields) in zip(old_faces, faces):
        assert fields == old_fields
        for old_index, index in zip(old_refs, refs):
            assert before[old_index][:8] == after[index][:8]
            assert before[old_index][11:] == after[index][11:]
        points = [struct.unpack_from("<3h", before[index]) for index in old_refs]
        wall = len({p[1] for p in points}) > 1 and (len({p[0] for p in points}) == 1 or len({p[2] for p in points}) == 1)
        assert all(after[index][8:11] == (bytes((57, 57, 60)) if wall else bytes((96, 96, 100))) for index in refs)
