"""Synthetic bound/writer regressions plus the private EXP-009 control."""

import hashlib
import struct
from pathlib import Path
from types import SimpleNamespace

import pytest

from ablpc import terrain_visibility as visibility


@pytest.mark.parametrize("radius,previous,expected", [(0, 0, 8), (1, 0, 10), (100, 0, 150), (100, 200, 200), (6047, 0, 8560)])
def test_plane_scaled_radius(radius, previous, expected):
    assert visibility.scene_visibility_radius(radius, previous) == expected


@pytest.mark.parametrize("kwargs", [
    {"geometric_radius": -1}, {"geometric_radius": True}, {"geometric_radius": 1.5},
    {"geometric_radius": 65536}, {"geometric_radius": 32767},
    {"geometric_radius": 10, "previous_bound": -1},
    {"geometric_radius": 10, "previous_bound": 32768},
    {"geometric_radius": 10, "width": 0},
    {"geometric_radius": 10, "height": False},
    {"geometric_radius": 10, "focal": 0},
])
def test_invalid_or_overflowing_bounds_rejected(kwargs):
    with pytest.raises(ValueError):
        visibility.scene_visibility_radius(**kwargs)


def test_wider_profile_requires_a_larger_bound():
    assert visibility.scene_visibility_radius(100, width=1280) > visibility.scene_visibility_radius(100)


@pytest.fixture
def synthetic(monkeypatch):
    # Byte-level writer fixture; parser validity is covered independently by
    # LevelDat regressions and the private integration arm below.
    scene = struct.pack("<3ihHI", 0, 0, 0, 10, 0x41, 20)
    obj = struct.pack("<3i3hBBI", 0, 0, 0, 0, 0, 0, 0, 0xc0, 44)
    suffix = bytes.fromhex("112233445566")
    data = scene + obj + struct.pack("<i", 2) + struct.pack("<3h", 100, 0, 0) + suffix + struct.pack("<3h", 0, 200, 0) + suffix
    ref = SimpleNamespace(record_offset=0, object_offset=20,
                          payload=SimpleNamespace(vertex_count=2, vertices_offset=48))
    monkeypatch.setattr(visibility.LevelDat, "parse", lambda raw: SimpleNamespace(static_mesh_reference=lambda *args: ref))
    return data, ref


def test_writer_preserves_every_other_byte(synthetic):
    data, _ = synthetic
    result, report = visibility.patch_scene_visibility(data, expected_bound=10)
    assert report["bound_after"] == 291
    assert report["geometric_radius"] == 200
    assert result[:12] == data[:12] and result[14:] == data[14:]
    assert len(result) == len(data)
    repeated, again = visibility.patch_scene_visibility(result, expected_bound=291)
    assert repeated == result and again["bound_after"] == 291


@pytest.mark.parametrize("size", [0, 19, 43, 47, 71])
def test_writer_rejects_truncation(synthetic, size):
    data, _ = synthetic
    with pytest.raises(ValueError):
        visibility.patch_scene_visibility(data[:size])


@pytest.mark.parametrize("field,value", [("record_offset", -1), ("object_offset", 999)])
def test_writer_rejects_impossible_offsets(synthetic, field, value):
    data, ref = synthetic
    setattr(ref, field, value)
    with pytest.raises(ValueError):
        visibility.patch_scene_visibility(data)


@pytest.mark.parametrize("count", [0, -1, True, 65536])
def test_writer_rejects_bad_counts(synthetic, count):
    data, ref = synthetic
    ref.payload.vertex_count = count
    with pytest.raises(ValueError):
        visibility.patch_scene_visibility(data)


def test_writer_requires_immutable_input_and_expected_bound(synthetic):
    data, _ = synthetic
    with pytest.raises(ValueError):
        visibility.patch_scene_visibility(bytearray(data))
    with pytest.raises(ValueError):
        visibility.patch_scene_visibility(data, expected_bound=11)


@pytest.mark.parametrize("offset,value", [(32, 1), (34, 1), (36, 1), (39, 0xc1)])
def test_writer_rejects_unestablished_transforms(synthetic, offset, value):
    data, _ = synthetic
    changed = data[:offset] + bytes([value]) + data[offset + 1:]
    with pytest.raises(ValueError):
        visibility.patch_scene_visibility(changed)


def test_private_exp009_only_changes_the_bound():
    path = Path(__file__).resolve().parents[1] / "work/copies/EXP-20260905-009/fixture/LEVEL.DAT"
    if not path.exists():
        pytest.skip("private EXP-009 fixture is absent")
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == "24b8c345d82bb3489ab765d3ad24f917fcacf1da4d5a910e715b4daf84b071e8"
    result, report = visibility.patch_scene_visibility(data, expected_bound=6047)
    assert report["bound_offset"] == 8592 and report["bound_after"] == 8560
    assert report["vertex_count"] == 439
    assert result[:8592] == data[:8592] and result[8594:] == data[8594:]
