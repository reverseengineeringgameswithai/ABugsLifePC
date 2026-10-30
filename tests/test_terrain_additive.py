"""Bounds and preservation regressions for additive PC terrain allocation."""

from __future__ import annotations

import struct
from pathlib import Path

import pytest

from ablpc.level_dat import LevelDat
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_additive import (
    append_collision_groups,
    append_render_geometry,
    build_additive_pair,
)
from ablpc.terrain_play_area import encode_group
from ablpc.terrain_texture_tiling import decode_mesh


ROOT = Path(__file__).resolve().parents[1]


def group(x: int = 0) -> bytes:
    return encode_group(((x, 0, 0), (x + 256, 0, 256), (x + 256, 0, 0)), (0, 0, 0))


def terrain(payloads: tuple[bytes, ...]) -> bytes:
    directory = 4 + sum(map(len, payloads))
    records = []
    for index, payload in enumerate(payloads):
        record = bytearray(76)
        struct.pack_into("<I", record, 0, len(payload) // 2)
        struct.pack_into("<i", record, 16, 6)
        struct.pack_into("<h", record, 40, index + 23)
        struct.pack_into("<h", record, 68, -1)
        record[72:76] = b"keep"
        records.append(bytes(record))
    return struct.pack("<I", directory // 2) + b"".join(payloads) + struct.pack("<I", len(records)) + b"".join(records) + b"tail"


def mesh(*, suffix: bytes = b"\x23\x01\x5a\x50\x46\xb1", mixed: bool = False) -> bytes:
    points = ((0, 0, 0), (1024, 0, 0), (1024, 0, 1024), (0, 0, 1024))
    vertices = b"".join(struct.pack("<3h", *point) + suffix for point in points)
    commands = struct.pack("<2H8H", 0x60, 1, 0, 12, 24, 36, 0xC000, 0xC03F, 0xFF3F, 0xFF00)
    if mixed:
        commands += struct.pack("<2H6H", 0x61, 1, 0, 24, 36, 0xC000, 0xFF3F, 0xFF00)
    return struct.pack("<i", 4) + vertices + commands + b"\xff\xff"


def dat(source: bytes, *, trailer: bool = True) -> bytes:
    prefix = bytearray(96)
    struct.pack_into("<h", prefix, 20, 64)
    struct.pack_into("<H", prefix, 22, 0x41)
    struct.pack_into("<I", prefix, 24, 72)
    struct.pack_into("<H", prefix, 42, 0xFFFF)
    struct.pack_into("<i", prefix, 48, -1)
    struct.pack_into("<H", prefix, 66, 0xFFFF)
    prefix[90] = 8
    struct.pack_into("<I", prefix, 92, 96)
    result = bytes(prefix) + source
    result += bytes((-len(result)) % 4)
    return result + (bytes(range(256)) + bytes(64) + struct.pack("<i", 324) if trailer else struct.pack("<i", -1))


def appended_stream(result: bytes) -> bytes:
    reference = LevelDat.parse(result).static_mesh_reference("primary", 0)
    end = len(result) - 4
    # All these synthetic streams have a two-byte terminator, then at most
    # two bytes of alignment padding. Do not trim vertex or command bytes.
    if result[end - 2:end] == b"\x00\x00":
        end -= 2
    return result[reference.geometry_offset:end]


@pytest.mark.parametrize("slot", [0, 1, 2])
def test_collision_append_preserves_every_original_byte_and_payload(slot):
    source = terrain(tuple(group(index * 300) + b"\xff\xff\x12\x34" for index in range(3)))
    old = TerrainAll.parse(source)
    addition = group(1000) + group(1400) + b"\xff\xff"
    result, _ = append_collision_groups(source, addition, source_index=slot)
    new = TerrainAll.parse(result)
    insertion = old.collision_payload(slot).terminator_offset
    growth = len(addition) - 2
    expected = bytearray(source[:insertion] + addition[:-2] + source[insertion:])
    struct.pack_into("<I", expected, 0, new.directory_offset // 2)
    struct.pack_into("<I", expected, new.records[slot].offset, old.records[slot].payload_word_count + growth // 2)
    assert result == bytes(expected)
    assert new.suffix == old.suffix == b"tail"
    assert new.collision_payload(slot).trailer == b"\x12\x34"
    assert len(new.collision_payload(slot).groups) == 3
    for index in range(3):
        if index != slot:
            assert new.collision_payload(index).raw == old.collision_payload(index).raw
            assert new.records[index].raw == old.records[index].raw
    assert new.records[slot].raw[4:] == old.records[slot].raw[4:]


@pytest.mark.parametrize("addition", [b"", b"\xff", b"\xff\xff", group(), group() + b"\xff\xffxx", b"\x01\x00\xff\x7f" + bytes(10) + b"\xff\xff"])
def test_collision_rejects_malformed_or_empty_additions(addition):
    with pytest.raises((ValueError, IndexError)):
        append_collision_groups(terrain((group() + b"\xff\xff",)), addition, source_index=0)


@pytest.mark.parametrize("slot", [-1, 1, True, 0.5])
def test_collision_rejects_invalid_source_index(slot):
    with pytest.raises((ValueError, TypeError, IndexError)):
        append_collision_groups(terrain((group() + b"\xff\xff",)), group(500) + b"\xff\xff", source_index=slot)


@pytest.mark.parametrize("field,value", [(16, 5), (68, 0), (70, 1)])
def test_collision_rejects_unsupported_descriptor_variants(field, value):
    source = bytearray(terrain((group() + b"\xff\xff",)))
    record = TerrainAll.parse(bytes(source)).records[0]
    struct.pack_into("<i" if field == 16 else "<h", source, record.offset + field, value)
    with pytest.raises(ValueError):
        append_collision_groups(bytes(source), group(500) + b"\xff\xff", source_index=0)


def test_collision_rejects_mutable_and_truncated_inputs():
    source = terrain((group() + b"\xff\xff",))
    addition = group(500) + b"\xff\xff"
    with pytest.raises(ValueError):
        append_collision_groups(bytearray(source), addition, source_index=0)
    with pytest.raises(ValueError):
        append_collision_groups(source, bytearray(addition), source_index=0)
    for end in (0, 2, 4, len(source) - 20):
        with pytest.raises(ValueError):
            append_collision_groups(source[:end], addition, source_index=0)


@pytest.mark.parametrize("trailer", [False, True])
@pytest.mark.parametrize("mixed", [False, True])
def test_render_preserves_original_geometry_commands_material_and_footer(trailer, mixed):
    original_mesh = mesh(mixed=mixed)
    source = dat(original_mesh, trailer=trailer)
    extra = mesh(suffix=b"\x42\x10\x44\x33\x22\xa9")
    result, _ = append_render_geometry(source, ((extra, (100, -50, 200)),), record_index=0)
    reference = LevelDat.parse(result).static_mesh_reference("primary", 0)
    combined = appended_stream(result)
    vertices, faces = decode_mesh(combined)
    old_vertices, old_faces = decode_mesh(original_mesh)
    assert vertices[:4] == old_vertices
    assert faces[:len(old_faces)] == old_faces
    assert combined[4 + 8 * 12:4 + 8 * 12 + len(original_mesh) - 54] == original_mesh[52:-2]
    assert struct.unpack_from("<3h", vertices[4]) == (100, -50, 200)
    assert vertices[4][6:] == b"\x42\x10\x44\x33\x22\xa9"
    assert faces[-1][1] == (4, 5, 6, 7)
    assert faces[-1][2] == decode_mesh(extra)[1][0][2]
    assert reference.geometry_offset == len(source) - 4
    assert result[90] == source[90] == 8
    assert result[96:len(source) - 4] == source[96:-4]
    assert result[22:24] == source[22:24]
    assert struct.unpack_from("<h", result, 20)[0] >= 1632
    old_footer, new_footer = struct.unpack_from("<i", source, len(source) - 4)[0], struct.unpack_from("<i", result, len(result) - 4)[0]
    assert new_footer == (-1 if not trailer else old_footer + len(result) - len(source))
    if trailer:
        assert len(result) - new_footer == len(source) - old_footer


def test_render_depth_neutralization_is_explicit_and_local():
    source = dat(mesh())
    retained, _ = append_render_geometry(source, ((mesh(), (0, 0, 0)),), record_index=0)
    neutral, _ = append_render_geometry(source, ((mesh(), (0, 0, 0)),), record_index=0, neutral_depth=True)
    assert retained[90] == 8 and neutral[90] == 0
    assert retained[:90] == neutral[:90] and retained[91:] == neutral[91:]


@pytest.mark.parametrize("offset,value", [(84, 1), (91, 1)])
def test_render_rejects_nontrivial_transform(offset, value):
    source = bytearray(dat(mesh()))
    source[offset] = value
    with pytest.raises(ValueError):
        append_render_geometry(bytes(source), ((mesh(), (0, 0, 0)),), record_index=0)


@pytest.mark.parametrize("origin", [(40000, 0, 0), (0, -40000, 0), (32760, 32760, 32760)])
def test_render_rejects_coordinate_or_visibility_bound_overflow(origin):
    with pytest.raises(ValueError):
        append_render_geometry(dat(mesh()), ((mesh(), origin),), record_index=0)


@pytest.mark.parametrize("value", [0, 4, 280, 0x7FFFFFFF, -2])
def test_render_rejects_unsupported_footer(value):
    source = bytearray(dat(mesh()))
    struct.pack_into("<i", source, len(source) - 4, value)
    with pytest.raises(ValueError):
        append_render_geometry(bytes(source), ((mesh(), (0, 0, 0)),), record_index=0)


def test_render_rejects_bad_references_and_mutable_input():
    bad = bytearray(mesh())
    struct.pack_into("<H", bad, 56, 48)
    with pytest.raises(ValueError):
        append_render_geometry(dat(mesh()), ((bytes(bad), (0, 0, 0)),), record_index=0)
    with pytest.raises(ValueError):
        append_render_geometry(bytearray(dat(mesh())), ((mesh(), (0, 0, 0)),), record_index=0)
    with pytest.raises(ValueError):
        append_render_geometry(dat(mesh())[:-1], ((mesh(), (0, 0, 0)),), record_index=0)
    with pytest.raises(ValueError):
        append_render_geometry(dat(mesh()), (), record_index=0)


@pytest.fixture(scope="module")
def private_pair():
    original = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01"
    donor = ROOT / "work/copies/EXP-20260905-006/fixture"
    paths = (original / "TERRAIN.ALL", original / "LEVEL.DAT", donor / "TERRAIN.ALL", donor / "LEVEL.DAT")
    if not all(path.is_file() for path in paths):
        pytest.skip("private PC and banked EXP-006 fixtures unavailable")
    inputs = tuple(path.read_bytes() for path in paths)
    return inputs, build_additive_pair(*inputs)


def test_private_pair_retains_all_original_payloads_and_adds_sixteen_cells(private_pair):
    inputs, (changed, _, _) = private_pair
    old, new = TerrainAll.parse(inputs[0]), TerrainAll.parse(changed)
    assert len(new.records) == len(old.records) == 189
    assert len(changed) - len(inputs[0]) == 704
    for index in range(189):
        a, b = old.records[index], new.records[index]
        if index != 99:
            assert a.raw == b.raw
            assert old.data[a.payload_offset:a.payload_offset + a.payload_size] == new.data[b.payload_offset:b.payload_offset + b.payload_size]
        else:
            old_payload, new_payload = old.collision_payload(index), new.collision_payload(index)
            assert new_payload.groups[:len(old_payload.groups)] == old_payload.groups
            assert sum(group.cell_count for group in old_payload.groups) == 134
            assert sum(group.cell_count for group in new_payload.groups) == 150
            assert new_payload.terminator_offset == 49084
            assert old_payload.trailer == new_payload.trailer


def test_private_pair_retains_original_mesh_and_all_other_static_references(private_pair):
    inputs, (_, changed, _) = private_pair
    old, new = LevelDat.parse(inputs[1]), LevelDat.parse(changed)
    original = old.static_mesh_reference("primary", 160)
    combined = new.static_mesh_reference("primary", 160)
    assert original.geometry_offset == 113136
    assert struct.unpack_from("<i", inputs[1], original.geometry_offset)[0] == 92
    assert changed[combined.geometry_offset + 4:combined.geometry_offset + 4 + 92 * 12] == inputs[1][113140:114244]
    count = struct.unpack_from("<i", changed, combined.geometry_offset)[0]
    new_command = combined.geometry_offset + 4 + count * 12
    assert changed[new_command:new_command + 115368 - 114244] == inputs[1][114244:115368]
    for section in ("primary", "secondary"):
        for reference in old.static_mesh_references(section):
            if section == "primary" and reference.record_index == 160:
                continue
            assert new.static_mesh_reference(section, reference.record_index) == reference
    allowed = set(range(18692, 18696)) | {18690, 8592, 8593}
    assert all(a == b or index in allowed for index, (a, b) in enumerate(zip(inputs[1][:-4], changed)))


@pytest.mark.parametrize("slot", range(4))
def test_private_builder_rejects_any_wrong_provenance(private_pair, slot):
    inputs, _ = private_pair
    changed = list(inputs)
    changed[slot] = bytes([changed[slot][0] ^ 1]) + changed[slot][1:]
    with pytest.raises(ValueError):
        build_additive_pair(*changed)
