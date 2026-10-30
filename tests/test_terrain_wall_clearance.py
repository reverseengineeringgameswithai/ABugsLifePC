"""Synthetic storage/writer regressions; no game assets required."""
import struct

import pytest

from ablpc.terrain_all import TerrainAll
from ablpc.terrain_wall_clearance import offset_x_wall_groups


def fixture(*, x=100, sign=-1, prefix=False):
    edges = (0, -64, 64, 0, -64, 0) if sign < 0 else (0, -64, 0, 0, -64, 64)
    group = struct.pack("<6h14h4b", 1, 1, x, 0, 0, 64,
                        sign * 16384, 0, 0, x, 0, 0, *edges, x, 0, -1, 1, 0, 1)
    wall = group + b"\xff\xff\xc1\x9e"
    payloads = ([b"\xaa\xbb\xcc\xdd"] if prefix else []) + [wall, wall]
    source = int(prefix)
    directory = 4 + sum(map(len, payloads))
    records = []
    for index, payload in enumerate(payloads):
        rec = bytearray(76)
        struct.pack_into("<I3iI", rec, 0, len(payload) // 2, -37, 20, 81,
                         257 if prefix and index == 0 else 6)
        rec[20:40] = bytes(range(20))
        rec[42:68] = bytes(range(26))
        struct.pack_into("<h", rec, 68, -1)
        rec[72:76] = b"tail"
        records.append(bytes(rec))
    raw = (struct.pack("<I", directory // 2) + b"".join(payloads)
           + struct.pack("<I", len(records)) + b"".join(records) + b"unknown-suffix")
    return raw, source, 4 + (4 if prefix else 0)


@pytest.mark.parametrize("prefix", [False, True])
@pytest.mark.parametrize("sign", [-1, 1])
@pytest.mark.parametrize("clearance", [0, 5, 48])
def test_preserves_every_other_byte_and_relative_field(prefix, sign, clearance):
    raw, source, group = fixture(prefix=prefix, sign=sign)
    result, report = offset_x_wall_groups(raw, source_index=source,
        group_offsets=[group], outward_stored=clearance)
    expected = bytearray(raw)
    for offset in (group + 4, group + 18, group + 36):
        struct.pack_into("<h", expected, offset, 100 + sign * clearance)
    assert result == bytes(expected)
    assert len(result) == len(raw)
    parsed = TerrainAll.parse(result)
    assert parsed.directory_offset == TerrainAll.parse(raw).directory_offset
    assert parsed.collision_payload(source).groups[0].cells[0].words[3] == 100 + sign * clearance
    assert report["outward_world"] == clearance * 32
    assert report["groups"][0]["plane_x_world_after"] == (-37 + 100 + sign * clearance) * 32


@pytest.mark.parametrize("clearance", [-1, True, 1.5, "48", 32768])
def test_rejects_bad_clearance(clearance):
    raw, source, group = fixture()
    with pytest.raises(ValueError):
        offset_x_wall_groups(raw, source_index=source, group_offsets=[group], outward_stored=clearance)


@pytest.mark.parametrize("source", [-1, True, 2, 999])
def test_rejects_bad_source(source):
    raw, _, group = fixture()
    with pytest.raises(ValueError):
        offset_x_wall_groups(raw, source_index=source, group_offsets=[group], outward_stored=48)


@pytest.mark.parametrize("offsets", [[], [True], [-1], [6], [16], [4, 4], [52]])
def test_requires_exact_unique_group_in_selected_source(offsets):
    raw, source, _ = fixture()
    with pytest.raises(ValueError):
        offset_x_wall_groups(raw, source_index=source, group_offsets=offsets, outward_stored=48)


@pytest.mark.parametrize("cut", [0, 3, 5, 15, 40, 100])
def test_rejects_truncated_files(cut):
    raw, source, group = fixture()
    with pytest.raises(ValueError):
        offset_x_wall_groups(raw[:cut], source_index=source, group_offsets=[group], outward_stored=48)


@pytest.mark.parametrize("relative,value", [
    (0, 0), (2, 2), (6, -1), (10, -1),
    (12, 8192), (14, 1), (16, 1), (24, 1), (30, 1), (38, -1),
])
def test_rejects_unsupported_geometry_and_windows(relative, value):
    raw, source, group = fixture()
    malformed = bytearray(raw)
    struct.pack_into("<h", malformed, group + relative, value)
    with pytest.raises(ValueError):
        offset_x_wall_groups(bytes(malformed), source_index=source,
                             group_offsets=[group], outward_stored=48)


@pytest.mark.parametrize("sign,x", [(-1, -32760), (1, 32760)])
def test_checks_translated_signed_bounds_before_writing(sign, x):
    raw, source, group = fixture(x=x, sign=sign)
    with pytest.raises(ValueError):
        offset_x_wall_groups(raw, source_index=source, group_offsets=[group], outward_stored=48)


def test_rejects_clone_and_opaque_source():
    raw, source, group = fixture(prefix=True)
    with pytest.raises(ValueError):
        offset_x_wall_groups(raw, source_index=0, group_offsets=[group], outward_stored=48)
    modified = bytearray(raw)
    directory = TerrainAll.parse(raw).directory_offset
    struct.pack_into("<h", modified, directory + 4 + 76 * source + 70, 1)
    with pytest.raises(ValueError):
        offset_x_wall_groups(bytes(modified), source_index=source,
                             group_offsets=[group], outward_stored=48)
