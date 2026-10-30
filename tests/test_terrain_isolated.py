"""Synthetic preservation/bounds tests for EXP-20260906-005."""

import struct
from pathlib import Path

import pytest

from ablpc.terrain_all import TerrainAll
from ablpc.terrain_isolated import (
    checked, isolate_collision, isolate_render, muted_scene_flags,
    pe_file_offset, platform_spawn, replace_spans,
)


def terrain_fixture(extra=False):
    group = struct.pack("<6h14h4b", 1, 1, 0, 100, 0, 100,
                        0, -16384, 0, 0, 0, 0, 100, 0, 0, 0, 0, 100, 0, 100,
                        -1, 2, -1, 3)
    payloads = [group * 2 + b"\xff\xffXY", group + b"\xff\xffXY"]
    if extra:
        payloads.append(b"\x78\x56\x34\x12" + b"unknown!" * 2)
    directory = 4 + sum(map(len, payloads))
    records = []
    for i, payload in enumerate(payloads):
        record = bytearray(76)
        struct.pack_into("<I", record, 0, len(payload) // 2)
        struct.pack_into("<i", record, 16, 0x101 if i == 2 else 6)
        record[24:28] = b"KEEP"
        struct.pack_into("<h", record, 68, -1)
        records.append(bytes(record))
    return struct.pack("<I", directory // 2) + b"".join(payloads) + struct.pack("<I", len(records)) + b"".join(records) + b"suffix!!"


@pytest.mark.parametrize("extra", [False, True])
def test_collision_retains_exact_group_unknown_fields_and_all_other_bytes(extra):
    data = terrain_fixture(extra)
    out, receipt = isolate_collision(data, {0: [48]})
    parsed = TerrainAll.parse(out)
    assert len(parsed.collision_payload(0).groups) == 1
    assert not parsed.collision_payload(1).groups
    assert out[4:48] == data[48:92]
    assert out[48:50] == b"\xff\xff"
    allowed = set(range(4, 50)) | {96, 97}
    if extra:
        allowed |= set(range(144, 148))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(data, out)))
    assert out[parsed.directory_offset:] == data[parsed.directory_offset:]
    assert receipt["records"][0]["groups"][0]["old_group"] == 48


@pytest.mark.parametrize("keep", [{2: [4]}, {False: [4]}, {0: [5]}, {0: [4, 4]}, {0: [48, 4]}, {0: [True]}])
def test_collision_rejects_bad_selection(keep):
    with pytest.raises(ValueError):
        isolate_collision(terrain_fixture(), keep)


@pytest.mark.parametrize("cut", [0, 3, 12, 95, 150, 290])
def test_collision_truncation(cut):
    with pytest.raises(ValueError):
        isolate_collision(terrain_fixture()[:cut], {})


@pytest.mark.parametrize("flags", [25, 65, 16409, 17, 19, 16401, 16473, 89, 26, 73, 20, 1, 16393, 9])
def test_scene_muting_keeps_relocation_layout_bits(flags):
    muted = muted_scene_flags(flags)
    assert muted & 0x38 == flags & 0x38
    assert muted & 7 == 0
    assert muted & 0xBFEF in (0, 8, 0x40, 0x48)
    assert muted & 0xBF6F in (0, 8, 0x40, 0x48)


@pytest.mark.parametrize("flags", [-1, 0x8000, True, 5, 0x21])
def test_scene_muting_refuses_unknown_cases(flags):
    with pytest.raises(ValueError):
        muted_scene_flags(flags)


def pe_fixture():
    data = bytearray(0x1200)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 0x3C, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HH", data, 0x84, 0x14C, 1)
    struct.pack_into("<H", data, 0x94, 0xE0)
    struct.pack_into("<H", data, 0x98, 0x10B)
    struct.pack_into("<I", data, 0xB4, 0x400000)
    struct.pack_into("<IIII", data, 0x180, 0x1000, 0xDC000, 0x1000, 0x200)
    struct.pack_into("<iii", data, 0x9F4, 197108, 492895, 3505)
    return bytes(data)


def test_spawn_changes_only_x_z_and_keeps_heading():
    data = pe_fixture()
    out, receipt = platform_spawn(data, x=192000, z=448000)
    assert pe_file_offset(data, 0x4DC7F4, 12) == 0x9F4
    assert out[:0x9F4] == data[:0x9F4]
    assert out[0x9FC:] == data[0x9FC:]
    assert struct.unpack_from("<iii", out, 0x9F4) == (192000, 448000, 3505)
    assert receipt["file_offset"] == 0x9F4


@pytest.mark.parametrize("cut", [0, 2, 60, 130, 170, 390, 0x9FA])
def test_pe_bounds(cut):
    with pytest.raises(ValueError):
        platform_spawn(pe_fixture()[:cut], x=0, z=0)


@pytest.mark.parametrize("x", [True, 1.5, -0x80000001, 0x80000000])
def test_spawn_refuses_bad_coordinates(x):
    with pytest.raises(ValueError):
        platform_spawn(pe_fixture(), x=x, z=0)


def test_spawn_compare_guard():
    data = bytearray(pe_fixture())
    data[0x9F4] ^= 1
    with pytest.raises(ValueError):
        platform_spawn(bytes(data), x=0, z=0)


@pytest.mark.parametrize("offset,size", [(-1, 1), (0, -1), (3, 2), (True, 1), (5, 0)])
def test_checked_bounds(offset, size):
    with pytest.raises(ValueError):
        checked(b"abcd", offset, size)


def test_span_guards_and_no_mutation():
    data = b"abcdef"
    assert replace_spans(data, [(1, b"bc", b"XY")]) == b"aXYdef"
    for changes in ([(1, b"bd", b"XY")], [(1, b"bc", b"X")], [(1, b"bc", b"XY"), (2, b"cd", b"ZZ")]):
        with pytest.raises(ValueError):
            replace_spans(data, changes)
    assert data == b"abcdef"


def test_private_render_pair_preservation():
    control = Path(__file__).resolve().parents[1] / "work/copies/EXP-20260906-004/fixture/LEVEL.DAT"
    if not control.exists():
        pytest.skip("private terrain control unavailable")
    data = control.read_bytes()
    out, receipt = isolate_render(data, record_index=160, first_group=5)
    assert receipt["authored_faces"] == 807
    assert receipt["original_faces_removed"] == 69
    assert len(receipt["muted_scenes"]) == 623
    allowed = set(range(receipt["command_start"], receipt["new_terminator"] + 2))
    for scene in receipt["muted_scenes"]:
        allowed.update((scene["offset"], scene["offset"] + 1))
    assert len(out) == len(data)
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(data, out)))
