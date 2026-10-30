from __future__ import annotations

import hashlib
import json
from pathlib import Path
import struct

import pytest

from reimplementation.ablpc.level_dat import DatFormatError, LevelDat
from reimplementation.ablpc.cli import main as cli_main
from reimplementation.ablpc.manifest import (
    ManifestError,
    apply_manifest,
    load_manifest,
    stage_manifest,
)


def _scene_record(
    component_00: int,
    component_04: int,
    component_08: int,
    field_0c: int,
    flags: int,
    payload: int,
) -> bytes:
    return struct.pack(
        "<iiihHi",
        component_00,
        component_04,
        component_08,
        field_0c,
        flags,
        payload,
    )


def _sentinel() -> bytes:
    return struct.pack("<IIIII", *(0x80008000,) * 5)


def synthetic_dat(*, negative_top_type: bool = False) -> bytes:
    pieces = [struct.pack("<i", 2)]
    pieces.append(struct.pack("<hh", 2, 0x3F) + bytes(range(32)))
    if negative_top_type:
        pieces.append(struct.pack("<hh", 1, -2) + bytes(20))
    else:
        pieces.append(struct.pack("<hh", 1, 11) + bytes(12))
    pieces.append(struct.pack("<i", 1) + bytes(128))
    pieces.extend(
        (
            _scene_record(10, 20, 30, 0x123, 0x41, 0x200),
            _scene_record(-40, -50, -60, 0x456, 0x59, 0x220),
            _sentinel(),
            struct.pack("<iii", 1, 0, 0x240),
            _scene_record(70, 80, 90, 0x789, 1, 0x260),
            _sentinel(),
            bytes(96),
            struct.pack("<i", -1),
        )
    )
    return b"".join(pieces)


def synthetic_dat_with_positive_payload_target() -> bytes:
    source = bytearray(synthetic_dat())
    source.extend(bytes(0x200 - len(source)))
    payload = bytearray(0x18)
    struct.pack_into("<I", payload, 0x14, 0x240)
    source.extend(payload)
    source.extend(bytes(0x220 - len(source)))
    payload = bytearray(0x20)
    struct.pack_into("<I", payload, 0x1C, 0x240)
    source.extend(payload)
    entries = bytes(24)
    command_header = struct.pack("<Hh", 0x60, 1)
    command_item = struct.pack("<HHHH8s", 0, 12, 0, 12, bytes(8))
    target = (
        struct.pack("<i", 2)
        + entries
        + command_header
        + command_item
        + struct.pack("<HH", 0xFFFF, 0)
    )
    source.extend(target)
    source.extend(target)
    return bytes(source)


def _static_mesh_bytes(*, triangle: bool = False) -> bytes:
    vertices = b"".join(
        (
            struct.pack("<hhhhBBBB", 10, -20, 30, 0, 4, 8, 12, 0),
            struct.pack("<hhhhBBBB", 40, 50, -60, 7, 16, 20, 24, 1),
            struct.pack("<hhhhBBBB", -70, 80, 90, -2, 28, 32, 36, 2),
            struct.pack("<hhhhBBBB", 100, -110, 120, 3, 40, 44, 48, 3),
        )
    )
    if triangle:
        return (
            struct.pack("<i", 4)
            + vertices
            + struct.pack("<HH", 0x0161, 1)
            + struct.pack("<HHHHHH", 0, 12, 36, 0x1111, 0x2222, 0x3333)
        )
    return (
        struct.pack("<i", 4)
        + vertices
        + struct.pack("<HH", 0x0060, 1)
        + struct.pack(
            "<HHHHHHHH", 0, 12, 24, 36, 0x1111, 0x2222, 0x3333, 0x4444
        )
    )


def synthetic_dat_with_static_mesh(*, triangle: bool = False) -> bytes:
    source = bytearray(synthetic_dat())
    source.extend(bytes(0x200 - len(source)))
    source.extend(struct.pack("<iiihhhBBI", 100, 200, 300, 0, 0, 0, 8, 0, 0x218))
    source.extend(_static_mesh_bytes(triangle=triangle))
    return bytes(source)


@pytest.mark.parametrize("negative_top_type", [False, True])
def test_parser_is_lossless_for_multiple_synthetic_layouts(
    negative_top_type: bool,
) -> None:
    source = synthetic_dat(negative_top_type=negative_top_type)
    parsed = LevelDat.parse(source)

    assert parsed.data == source
    assert [record.type_id for record in parsed.top_records] == [0x3F, -2 if negative_top_type else 11]
    assert parsed.fixed_record_count == 1
    assert len(parsed.primary_records) == 2
    assert parsed.index_table_values == (0, 0x240)
    assert len(parsed.secondary_records) == 1
    assert parsed.final_dword == -1


def test_position_edit_changes_only_selected_coordinates() -> None:
    source = synthetic_dat()
    parsed = LevelDat.parse(source)
    offset = parsed.primary_records[1].offset

    changed = parsed.set_record_position("primary", 1, (1000, -2000, 3000))

    changed_offsets = [
        index for index, (before, after) in enumerate(zip(source, changed)) if before != after
    ]
    assert changed_offsets
    assert all(offset <= index < offset + 12 for index in changed_offsets)
    reparsed = LevelDat.parse(changed)
    record = reparsed.primary_records[1]
    assert (
        record.center_component_00,
        record.center_component_04,
        record.center_component_08,
    ) == (1000, -2000, 3000)
    assert record.field_0c_signed == parsed.primary_records[1].field_0c_signed
    assert record.flags == parsed.primary_records[1].flags


def test_field_0c_edit_is_guarded_and_changes_only_selected_word() -> None:
    source = synthetic_dat()
    parsed = LevelDat.parse(source)
    field_offset = parsed.primary_records[1].offset + 0x0C

    changed = parsed.set_record_field_0c(
        "primary", 1, expected_value=0x456, value=0
    )

    changed_offsets = [
        index for index, (before, after) in enumerate(zip(source, changed)) if before != after
    ]
    assert changed_offsets
    assert all(field_offset <= index < field_offset + 2 for index in changed_offsets)
    assert struct.unpack_from("<h", changed, field_offset)[0] == 0
    negative = parsed.set_record_field_0c(
        "primary", 1, expected_value=0x456, value=-7
    )
    assert LevelDat.parse(negative).primary_records[1].field_0c_signed == -7
    with pytest.raises(DatFormatError, match=r"field \+0x0c mismatch"):
        parsed.set_record_field_0c(
            "primary", 1, expected_value=0, value=0x456
        )
    with pytest.raises(ValueError, match="signed 16-bit range"):
        parsed.set_record_field_0c(
            "primary", 1, expected_value=0x456, value=2**15
        )


def test_parser_rejects_impossible_counts_and_truncation() -> None:
    with pytest.raises(DatFormatError, match="top-record count"):
        LevelDat.parse(struct.pack("<i", 100))

    source = synthetic_dat()
    parsed = LevelDat.parse(source)
    corrupt = bytearray(source)
    struct.pack_into("<i", corrupt, parsed.fixed_records_offset, 2**30)
    with pytest.raises(DatFormatError, match="fixed-record section"):
        LevelDat.parse(bytes(corrupt))

    with pytest.raises(DatFormatError, match="scene record or sentinel"):
        LevelDat.parse(source[: parsed.primary_sentinel_offset])


@pytest.mark.parametrize("triangle", [False, True])
def test_static_mesh_parser_round_trips_unknown_fields_and_face_arities(
    triangle: bool,
) -> None:
    source = synthetic_dat_with_static_mesh(triangle=triangle)
    parsed = LevelDat.parse(source)
    reference = parsed.static_mesh_reference("primary", 0)
    mesh = reference.payload

    assert reference.record_offset == parsed.primary_records[0].offset
    assert reference.object_offset == 0x200
    assert reference.geometry_offset == 0x218
    assert mesh.vertex_count == 4
    assert mesh.is_triangle is triangle
    assert mesh.tag_low_5 == (1 if triangle else 0)
    assert mesh.tag_bits_5_6 == 0x60
    assert mesh.tag_upper_index == (1 if triangle else 0)
    assert mesh.vertices[0].component_02 == -20
    assert mesh.vertices[1].field_06 == 7
    assert mesh.vertices[3].field_0b == 3
    assert mesh.faces[0].vertex_byte_offsets == (
        (0, 12, 36) if triangle else (0, 12, 24, 36)
    )
    assert mesh.faces[0].field_words == (
        (0x1111, 0x2222, 0x3333)
        if triangle
        else (0x1111, 0x2222, 0x3333, 0x4444)
    )
    assert mesh.to_bytes() == source[mesh.offset : mesh.end_offset]
    assert parsed.static_mesh_references("primary") == (reference,)


def test_static_mesh_parser_rejects_invalid_counts_and_vertex_offsets() -> None:
    source = bytearray(synthetic_dat_with_static_mesh())
    struct.pack_into("<i", source, 0x218, 2**30)
    with pytest.raises(DatFormatError, match="vertices and face header"):
        LevelDat.parse(bytes(source)).static_mesh_reference("primary", 0)

    source = bytearray(synthetic_dat_with_static_mesh())
    face_offset = 0x218 + 4 + 4 * 12 + 4
    struct.pack_into("<H", source, face_offset, 1)
    with pytest.raises(DatFormatError, match="does not select one of 4"):
        LevelDat.parse(bytes(source)).static_mesh_reference("primary", 0)

    parsed = LevelDat.parse(synthetic_dat_with_static_mesh())
    with pytest.raises(DatFormatError, match="dispatch 0x41"):
        parsed.static_mesh_reference("secondary", 0)


def test_static_mesh_vertex_edit_is_guarded_and_byte_local() -> None:
    source = synthetic_dat_with_static_mesh()
    parsed = LevelDat.parse(source)
    changed = parsed.set_static_mesh_vertex_component(
        "primary",
        0,
        0,
        2,
        expected_value=-20,
        value=1234,
    )
    field_offset = 0x218 + 4 + 2
    changed_offsets = [
        index for index, (before, after) in enumerate(zip(source, changed)) if before != after
    ]
    assert changed_offsets
    assert all(field_offset <= index < field_offset + 2 for index in changed_offsets)
    assert LevelDat.parse(changed).static_mesh_reference(
        "primary", 0
    ).payload.vertices[0].component_02 == 1234

    with pytest.raises(DatFormatError, match="mismatch"):
        parsed.set_static_mesh_vertex_component(
            "primary", 0, 0, 2, expected_value=0, value=1234
        )
    with pytest.raises(ValueError, match="must be 0, 2, or 4"):
        parsed.set_static_mesh_vertex_component(
            "primary", 0, 0, 1, expected_value=-20, value=1234  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("triangle", "expected_offsets", "replacement_offsets"),
    [
        (False, (0, 12, 24, 36), (0, 0, 0, 0)),
        (True, (0, 12, 36), (12, 12, 12)),
    ],
)
def test_static_mesh_face_edit_is_guarded_reparsed_and_byte_local(
    triangle: bool,
    expected_offsets: tuple[int, ...],
    replacement_offsets: tuple[int, ...],
) -> None:
    source = synthetic_dat_with_static_mesh(triangle=triangle)
    parsed = LevelDat.parse(source)
    before = parsed.static_mesh_reference("primary", 0)
    changed = parsed.set_static_mesh_face_vertex_byte_offsets(
        "primary",
        0,
        0,
        expected_object_offset=0x200,
        expected_geometry_offset=0x218,
        expected_offsets=expected_offsets,
        offsets=replacement_offsets,
    )

    face = before.payload.faces[0]
    changed_offsets = [
        index for index, (old, new) in enumerate(zip(source, changed)) if old != new
    ]
    assert changed_offsets
    assert all(face.offset <= index < face.offset + len(expected_offsets) * 2 for index in changed_offsets)
    after = LevelDat.parse(changed).static_mesh_reference("primary", 0)
    assert after.object_offset == before.object_offset
    assert after.geometry_offset == before.geometry_offset
    assert after.payload.faces[0].vertex_byte_offsets == replacement_offsets
    assert after.payload.faces[0].field_words == before.payload.faces[0].field_words


def test_static_mesh_face_edit_rejects_identity_guard_and_invalid_offsets() -> None:
    parsed = LevelDat.parse(synthetic_dat_with_static_mesh())
    arguments = {
        "section": "primary",
        "record_index": 0,
        "face_index": 0,
        "expected_object_offset": 0x200,
        "expected_geometry_offset": 0x218,
        "expected_offsets": (0, 12, 24, 36),
        "offsets": (0, 0, 0, 0),
    }

    with pytest.raises(DatFormatError, match="object offset mismatch"):
        parsed.set_static_mesh_face_vertex_byte_offsets(
            **(arguments | {"expected_object_offset": 0x204})
        )
    with pytest.raises(DatFormatError, match="geometry offset mismatch"):
        parsed.set_static_mesh_face_vertex_byte_offsets(
            **(arguments | {"expected_geometry_offset": 0x21C})
        )
    with pytest.raises(DatFormatError, match="face 0 offsets mismatch"):
        parsed.set_static_mesh_face_vertex_byte_offsets(
            **(arguments | {"expected_offsets": (0, 12, 36, 24)})
        )
    with pytest.raises(ValueError, match="arity must be 4"):
        parsed.set_static_mesh_face_vertex_byte_offsets(
            **(arguments | {"offsets": (0, 0, 0)})
        )
    with pytest.raises(ValueError, match="12-byte aligned"):
        parsed.set_static_mesh_face_vertex_byte_offsets(
            **(arguments | {"offsets": (0, 0, 0, 1)})
        )
    with pytest.raises(ValueError, match="outside"):
        parsed.set_static_mesh_face_vertex_byte_offsets(
            **(arguments | {"offsets": (0, 0, 0, 48)})
        )
    with pytest.raises(IndexError, match="face index 1"):
        parsed.set_static_mesh_face_vertex_byte_offsets(
            **(arguments | {"face_index": 1})
        )


def test_positive_payload_target_reference_and_block_layout() -> None:
    parsed = LevelDat.parse(synthetic_dat_with_positive_payload_target())

    reference = parsed.payload_target_reference("primary", 0)
    assert reference.record_offset == parsed.primary_records[0].offset
    assert reference.payload_offset == 0x200
    assert reference.target_field_offset == 0x14
    assert reference.target_offset == 0x240

    block = parsed.positive_payload_target_block(reference.target_offset)
    assert block.entry_count == 2
    assert block.entries_offset == 0x244
    assert block.command_stream_offset == 0x25C
    assert len(block.command_groups) == 1
    assert block.command_groups[0].mode == 0x60
    assert block.command_groups[0].item_count == 1
    assert block.command_groups[0].item_size == 16
    assert block.terminator_offset == 0x270
    assert block.end_offset == 0x274


def test_inspect_payload_targets_filters_to_supported_dispatch(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = bytearray(synthetic_dat_with_positive_payload_target())
    struct.pack_into("<I", source, 0x200 + 0x14, 0x274)
    struct.pack_into("<i", source, 0x274, -2)
    path = tmp_path / "LEVEL.DAT"
    path.write_bytes(source)

    result = cli_main(
        ["inspect", str(path), "--payload-targets", "primary", "--json"]
    )

    assert result == 0
    output = json.loads(capsys.readouterr().out)
    references = output["primary_payload_target_references"]
    assert [reference["record_index"] for reference in references] == [1]
    assert [reference["target_offset"] for reference in references] == [0x240]
    blocks = output["primary_positive_payload_target_blocks"]
    assert [block["offset"] for block in blocks] == [0x240]


def test_positive_payload_target_rejects_unsupported_or_invalid_layouts() -> None:
    source = bytearray(synthetic_dat_with_positive_payload_target())
    struct.pack_into("<i", source, 0x240, -2)
    parsed = LevelDat.parse(bytes(source))
    with pytest.raises(DatFormatError, match="unsupported layout"):
        parsed.positive_payload_target_block(0x240)

    source = bytearray(synthetic_dat_with_positive_payload_target())
    struct.pack_into("<H", source, 0x260, 1)
    parsed = LevelDat.parse(bytes(source))
    with pytest.raises(DatFormatError, match="outside the 24-byte entry table"):
        parsed.positive_payload_target_block(0x240)


def test_payload_target_rebind_changes_only_the_guarded_pointer() -> None:
    source = synthetic_dat_with_positive_payload_target()
    parsed = LevelDat.parse(source)

    changed = parsed.set_record_payload_target_offset(
        "primary", 1, expected_target_offset=0x240, target_offset=0x274
    )

    pointer_offset = 0x220 + 0x1C
    changed_offsets = [
        index for index, (before, after) in enumerate(zip(source, changed)) if before != after
    ]
    assert changed_offsets
    assert all(pointer_offset <= index < pointer_offset + 4 for index in changed_offsets)
    rebound = LevelDat.parse(changed).payload_target_reference("primary", 1)
    assert rebound.target_offset == 0x274

    with pytest.raises(DatFormatError, match="target mismatch"):
        parsed.set_record_payload_target_offset(
            "primary", 1, expected_target_offset=0x274, target_offset=0x240
        )
    with pytest.raises(DatFormatError, match="do not select"):
        parsed.set_record_payload_target_offset(
            "primary", 0, expected_target_offset=0x240, target_offset=0x274
        )
    with pytest.raises(IndexError, match="index -1 is outside"):
        parsed.set_record_payload_target_offset(
            "primary", -1, expected_target_offset=0x240, target_offset=0x274
        )


def _write_manifest(path: Path, source_bytes: bytes) -> Path:
    manifest = {
        "schema_version": 1,
        "name": "synthetic-position-test",
        "files": [
            {
                "path": "CD/LEVEL07/LEVEL1.DAT",
                "sha256": hashlib.sha256(source_bytes).hexdigest(),
                "format": "pc-level-dat-prefix-v0",
                "edits": [
                    {
                        "operation": "set-scene-record-position",
                        "section": "secondary",
                        "index": 0,
                        "position": [111, 222, 333],
                    }
                ],
            }
        ],
    }
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def _write_target_manifest(path: Path, source_bytes: bytes) -> Path:
    manifest = {
        "schema_version": 1,
        "name": "synthetic-target-rebind-test",
        "files": [
            {
                "path": "CD/LEVEL07/LEVEL1.DAT",
                "sha256": hashlib.sha256(source_bytes).hexdigest(),
                "format": "pc-level-dat-prefix-v0",
                "edits": [
                    {
                        "operation": "set-scene-record-payload-target-offset",
                        "section": "primary",
                        "index": 1,
                        "expected_target_offset": 0x240,
                        "target_offset": 0x274,
                    }
                ],
            }
        ],
    }
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def _write_field_0c_manifest(path: Path, source_bytes: bytes) -> Path:
    manifest = {
        "schema_version": 1,
        "name": "synthetic-field-0c-test",
        "files": [
            {
                "path": "CD/LEVEL07/LEVEL1.DAT",
                "sha256": hashlib.sha256(source_bytes).hexdigest(),
                "format": "pc-level-dat-prefix-v0",
                "edits": [
                    {
                        "operation": "set-scene-record-field-0c",
                        "section": "primary",
                        "index": 1,
                        "expected_value": 0x456,
                        "value": 0,
                    }
                ],
            }
        ],
    }
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def test_manifest_builds_sparse_overlay_and_receipt(tmp_path: Path) -> None:
    source_bytes = synthetic_dat()
    source_root = tmp_path / "source"
    source_file = source_root / "CD/LEVEL07/LEVEL1.DAT"
    source_file.parent.mkdir(parents=True)
    source_file.write_bytes(source_bytes)
    manifest = load_manifest(_write_manifest(tmp_path / "mod.json", source_bytes))
    output_root = tmp_path / "overlay"

    receipt = apply_manifest(manifest, source_root, output_root)

    assert source_file.read_bytes() == source_bytes
    output_file = output_root / "CD/LEVEL07/LEVEL1.DAT"
    changed = LevelDat.from_path(output_file)
    assert (
        changed.secondary_records[0].center_component_00,
        changed.secondary_records[0].center_component_04,
        changed.secondary_records[0].center_component_08,
    ) == (111, 222, 333)
    assert receipt["files"][0]["input_sha256"] != receipt["files"][0]["output_sha256"]
    assert json.loads((output_root / ".ablpc/receipt.json").read_text()) == receipt


def test_manifest_rebinds_a_guarded_positive_payload_target(tmp_path: Path) -> None:
    source_bytes = synthetic_dat_with_positive_payload_target()
    source_root = tmp_path / "source"
    source_file = source_root / "CD/LEVEL07/LEVEL1.DAT"
    source_file.parent.mkdir(parents=True)
    source_file.write_bytes(source_bytes)
    manifest = load_manifest(_write_target_manifest(tmp_path / "mod.json", source_bytes))
    output_root = tmp_path / "overlay"

    receipt = apply_manifest(manifest, source_root, output_root)

    output = LevelDat.from_path(output_root / "CD/LEVEL07/LEVEL1.DAT")
    assert output.payload_target_reference("primary", 1).target_offset == 0x274
    assert source_file.read_bytes() == source_bytes
    assert receipt["files"][0]["edits"][0] == {
        "edit_index": 0,
        "operation": "set-scene-record-payload-target-offset",
        "section": "primary",
        "index": 1,
        "expected_target_offset": 0x240,
        "target_offset": 0x274,
    }


def test_manifest_edits_guarded_field_0c(tmp_path: Path) -> None:
    source_bytes = synthetic_dat()
    source_root = tmp_path / "source"
    source_file = source_root / "CD/LEVEL07/LEVEL1.DAT"
    source_file.parent.mkdir(parents=True)
    source_file.write_bytes(source_bytes)
    manifest = load_manifest(
        _write_field_0c_manifest(tmp_path / "mod.json", source_bytes)
    )
    output_root = tmp_path / "overlay"

    receipt = apply_manifest(manifest, source_root, output_root)

    output_bytes = (output_root / "CD/LEVEL07/LEVEL1.DAT").read_bytes()
    field_offset = LevelDat.parse(source_bytes).primary_records[1].offset + 0x0C
    assert struct.unpack_from("<h", output_bytes, field_offset)[0] == 0
    assert receipt["files"][0]["edits"][0] == {
        "edit_index": 0,
        "operation": "set-scene-record-field-0c",
        "section": "primary",
        "index": 1,
        "expected_value": 0x456,
        "value": 0,
    }


def test_manifest_stage_copies_base_before_editing(tmp_path: Path) -> None:
    source_bytes = synthetic_dat()
    source_root = tmp_path / "base"
    source_file = source_root / "CD/LEVEL07/LEVEL1.DAT"
    source_file.parent.mkdir(parents=True)
    source_file.write_bytes(source_bytes)
    (source_root / "unchanged.txt").write_text("base", encoding="utf-8")
    manifest = load_manifest(_write_manifest(tmp_path / "mod.json", source_bytes))
    game_root = tmp_path / "staged"

    stage_manifest(manifest, source_root, game_root)

    assert (game_root / "unchanged.txt").read_text(encoding="utf-8") == "base"
    assert (game_root / "CD/LEVEL07/LEVEL1.DAT").read_bytes() != source_bytes
    assert source_file.read_bytes() == source_bytes


def test_manifest_rejects_traversal_hash_mismatch_and_protected_roots(
    tmp_path: Path,
) -> None:
    source_bytes = synthetic_dat()
    source_root = tmp_path / "source"
    source_file = source_root / "CD/LEVEL07/LEVEL1.DAT"
    source_file.parent.mkdir(parents=True)
    source_file.write_bytes(source_bytes)
    manifest_path = _write_manifest(tmp_path / "mod.json", source_bytes)
    manifest_value = json.loads(manifest_path.read_text())
    manifest_value["files"][0]["path"] = "../escape.dat"
    manifest_path.write_text(json.dumps(manifest_value), encoding="utf-8")
    with pytest.raises(ManifestError, match="unsafe manifest path"):
        load_manifest(manifest_path)

    manifest_path = _write_manifest(tmp_path / "mod.json", source_bytes)
    manifest = load_manifest(manifest_path)
    manifest["files"][0]["sha256"] = "0" * 64
    with pytest.raises(ManifestError, match="SHA-256 mismatch"):
        apply_manifest(manifest, source_root, tmp_path / "overlay")

    protected = tmp_path / "originals" / "game"
    protected.mkdir(parents=True)
    with pytest.raises(ManifestError, match="protected content"):
        apply_manifest(load_manifest(manifest_path), protected, tmp_path / "safe")


def test_manifest_rejects_unknown_root_fields_and_duplicate_paths(
    tmp_path: Path,
) -> None:
    source_bytes = synthetic_dat()
    manifest_path = _write_manifest(tmp_path / "mod.json", source_bytes)
    manifest_value = json.loads(manifest_path.read_text())
    manifest_value["unsupported"] = True
    manifest_path.write_text(json.dumps(manifest_value), encoding="utf-8")
    with pytest.raises(ManifestError, match="manifest root must contain exactly"):
        load_manifest(manifest_path)

    manifest_path = _write_manifest(tmp_path / "mod.json", source_bytes)
    manifest_value = json.loads(manifest_path.read_text())
    duplicate = json.loads(json.dumps(manifest_value["files"][0]))
    duplicate["path"] = duplicate["path"].lower()
    manifest_value["files"].append(duplicate)
    manifest_path.write_text(json.dumps(manifest_value), encoding="utf-8")
    with pytest.raises(ManifestError, match="duplicates another manifest input"):
        load_manifest(manifest_path)
