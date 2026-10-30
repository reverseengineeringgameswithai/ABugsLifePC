from __future__ import annotations

import copy
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import struct
import subprocess
import sys

import pytest

from reimplementation.ablpc import manifest as manifest_module
from reimplementation.ablpc.cli import main as cli_main
from reimplementation.ablpc.level_dat import LevelDat
from reimplementation.ablpc.manifest import (
    ManifestCompositionConflict,
    ManifestError,
    _MountEntry,
    _mount_alias_points,
    apply_manifest,
    compose_manifests,
    dry_run_manifest,
    load_manifest,
    remove_manifest,
    remove_receipt,
    replay_receipt,
    restore_manifest,
    stage_manifest,
)


DESTINATION_PATH = "CD/CHARS/FLICK.ALL"
SOURCE_PATH = "CD/CHARS3/FLICKD.ALL"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _replacement_manifest(
    destination: bytes,
    replacement: bytes,
    *,
    destination_path: str = DESTINATION_PATH,
    source_path: str = SOURCE_PATH,
) -> dict[str, object]:
    return {
        "schema_version": 2,
        "name": "synthetic-whole-file-replacement",
        "files": [
            {
                "path": destination_path,
                "sha256": _sha256(destination),
                "format": "opaque-file-v0",
                "edits": [
                    {
                        "operation": "replace-whole-file",
                        "source_path": source_path,
                        "source_sha256": _sha256(replacement),
                    }
                ],
            }
        ],
    }


def _write_json(path: Path, value: object) -> Path:
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def _write_work_copy(root: Path, destination: bytes, replacement: bytes) -> None:
    destination_path = root / DESTINATION_PATH
    replacement_path = root / SOURCE_PATH
    destination_path.parent.mkdir(parents=True)
    replacement_path.parent.mkdir(parents=True)
    destination_path.write_bytes(destination)
    replacement_path.write_bytes(replacement)


def _write_source_file(root: Path, relative: str, data: bytes) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _append_replacement(
    manifest: dict[str, object],
    destination: bytes,
    replacement: bytes,
    *,
    destination_path: str,
    source_path: str,
) -> None:
    manifest["files"].append(
        {
            "path": destination_path,
            "sha256": _sha256(destination),
            "format": "opaque-file-v0",
            "edits": [
                {
                    "operation": "replace-whole-file",
                    "source_path": source_path,
                    "source_sha256": _sha256(replacement),
                }
            ],
        }
    )


def _synthetic_dat() -> bytes:
    def record(values: tuple[int, int, int, int, int, int]) -> bytes:
        return struct.pack("<iiihHi", *values)

    sentinel = struct.pack("<IIIII", *(0x80008000,) * 5)
    return b"".join(
        (
            struct.pack("<i", 1),
            struct.pack("<hh", 1, 11),
            bytes(12),
            struct.pack("<i", 1),
            bytes(128),
            record((10, 20, 30, 0x123, 0x41, 0x200)),
            sentinel,
            struct.pack("<iii", 1, 0, 0x240),
            record((70, 80, 90, 0x789, 1, 0x260)),
            sentinel,
            bytes(96),
            struct.pack("<i", -1),
        )
    )


def _synthetic_dat_with_payload_target() -> bytes:
    def record(values: tuple[int, int, int, int, int, int]) -> bytes:
        return struct.pack("<iiihHi", *values)

    sentinel = struct.pack("<IIIII", *(0x80008000,) * 5)
    source = bytearray(
        b"".join(
            (
                struct.pack("<i", 1),
                struct.pack("<hh", 1, 11),
                bytes(12),
                struct.pack("<i", 1),
                bytes(128),
                record((10, 20, 30, 0x123, 0x49, 0x200)),
                sentinel,
                struct.pack("<iii", 1, 0, 0x240),
                record((70, 80, 90, 0x789, 1, 0x260)),
                sentinel,
                bytes(96),
                struct.pack("<i", -1),
            )
        )
    )
    source.extend(bytes(0x200 - len(source)))
    payload = bytearray(0x20)
    struct.pack_into("<I", payload, 0x1C, 0x240)
    source.extend(payload)
    source.extend(bytes(0x240 - len(source)))
    source.extend(struct.pack("<iHH", 0, 0xFFFF, 0))
    source.extend(struct.pack("<iHH", 0, 0xFFFF, 0))
    return bytes(source)


def _synthetic_dat_with_order_sensitive_payload_target() -> bytes:
    def record(values: tuple[int, int, int, int, int, int]) -> bytes:
        return struct.pack("<iiihHi", *values)

    sentinel = struct.pack("<IIIII", *(0x80008000,) * 5)
    source = bytearray(
        b"".join(
            (
                struct.pack("<i", 1),
                struct.pack("<hh", 1, 11),
                bytes(12),
                struct.pack("<i", 1),
                bytes(128),
                record((0, 0xFFFF, 0, 0x123, 0x49, 0x200)),
                sentinel,
                struct.pack("<iii", 1, 0, 0x240),
                record((70, 80, 90, 0x789, 1, 0x260)),
                sentinel,
                bytes(96),
                struct.pack("<i", -1),
            )
        )
    )
    source.extend(bytes(0x200 - len(source)))
    payload = bytearray(0x20)
    struct.pack_into("<I", payload, 0x1C, 0x98)
    source.extend(payload)
    source.extend(bytes(0x240 - len(source)))
    source.extend(struct.pack("<iHH", 0, 0xFFFF, 0))
    return bytes(source)


def _level_manifest(
    source: bytes,
    name: str,
    edits: list[dict[str, object]],
    *,
    path: str = "CD/LEVEL07/LEVEL1.DAT",
    schema_version: int = 1,
) -> dict[str, object]:
    return {
        "schema_version": schema_version,
        "name": name,
        "files": [
            {
                "path": path,
                "sha256": _sha256(source),
                "format": "pc-level-dat-prefix-v0",
                "edits": edits,
            }
        ],
    }


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def _tree_paths(root: Path) -> set[str]:
    return {str(path.relative_to(root)) for path in root.rglob("*")}


def _tree_snapshot(root: Path) -> tuple[tuple[str, str, object], ...]:
    if not root.exists() and not root.is_symlink():
        return ()
    snapshot: list[tuple[str, str, object]] = []

    def visit(path: Path, relative: str) -> None:
        metadata = path.lstat()
        if stat.S_ISDIR(metadata.st_mode):
            kind = "directory"
            payload: object = None
        elif stat.S_ISREG(metadata.st_mode):
            kind = "regular"
            payload = (path.read_bytes(), metadata.st_nlink)
        elif stat.S_ISLNK(metadata.st_mode):
            kind = "symlink"
            payload = os.readlink(path)
        else:
            kind = "non-regular"
            payload = metadata.st_mode
        snapshot.append((relative, kind, payload))
        if kind == "directory":
            for child in sorted(path.iterdir(), key=lambda item: item.name):
                child_relative = f"{relative}/{child.name}" if relative else child.name
                visit(child, child_relative)

    visit(root, "")
    return tuple(snapshot)


def _open_descriptor_count() -> int:
    return len(tuple(Path("/proc/self/fd").iterdir()))


@pytest.mark.parametrize("schema_version", [1, 2])
def test_dry_run_reports_all_level_edit_ranges_in_authored_order_without_writes(
    tmp_path: Path, schema_version: int
) -> None:
    source = _synthetic_dat_with_payload_target()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    edits = [
        {
            "operation": "set-scene-record-payload-target-offset",
            "section": "primary",
            "index": 0,
            "expected_target_offset": 0x240,
            "target_offset": 0x248,
        },
        {
            "operation": "set-scene-record-position",
            "section": "primary",
            "index": 0,
            "position": [111, 222, 333],
        },
        {
            "operation": "set-scene-record-field-0c",
            "section": "primary",
            "index": 0,
            "expected_value": 0x123,
            "value": 0,
        },
    ]
    manifest = _level_manifest(
        source,
        f"dry-run-level-schema-{schema_version}",
        edits,
        schema_version=schema_version,
    )
    before = _tree_snapshot(source_root)

    report = dry_run_manifest(manifest, source_root)

    expected_output = LevelDat.parse(source).set_record_payload_target_offset(
        "primary", 0, 0x240, 0x248
    )
    expected_output = LevelDat.parse(expected_output).set_record_position(
        "primary", 0, (111, 222, 333)
    )
    expected_output = LevelDat.parse(expected_output).set_record_field_0c(
        "primary", 0, 0x123, 0
    )
    record_offset = LevelDat.parse(source).primary_records[0].offset
    assert report == {
        "report_schema_version": 1,
        "manifest": {
            "schema_version": schema_version,
            "name": f"dry-run-level-schema-{schema_version}",
            "sha256": _sha256(_canonical_json_bytes(manifest)),
        },
        "files": [
            {
                "path": relative,
                "format": "pc-level-dat-prefix-v0",
                "input_sha256": _sha256(source),
                "input_size": len(source),
                "output_sha256": _sha256(expected_output),
                "output_size": len(expected_output),
                "edits": [
                    {
                        "edit_index": 0,
                        "operation": "set-scene-record-payload-target-offset",
                        "section": "primary",
                        "record_index": 0,
                        "record_offset": record_offset,
                        "destination_range": {"start": 0x21C, "end": 0x220},
                    },
                    {
                        "edit_index": 1,
                        "operation": "set-scene-record-position",
                        "section": "primary",
                        "record_index": 0,
                        "record_offset": record_offset,
                        "destination_range": {
                            "start": record_offset,
                            "end": record_offset + 12,
                        },
                    },
                    {
                        "edit_index": 2,
                        "operation": "set-scene-record-field-0c",
                        "section": "primary",
                        "record_index": 0,
                        "record_offset": record_offset,
                        "destination_range": {
                            "start": record_offset + 0x0C,
                            "end": record_offset + 0x0E,
                        },
                    },
                ],
            }
        ],
    }
    assert _tree_snapshot(source_root) == before


def test_dry_run_reports_distinct_whole_file_input_and_output_extents(
    tmp_path: Path,
) -> None:
    destination = b"destination"
    replacement = b"longer replacement bytes"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = _replacement_manifest(destination, replacement)
    before = _tree_snapshot(source_root)

    report = dry_run_manifest(manifest, source_root)

    assert report["files"] == [
        {
            "path": DESTINATION_PATH,
            "format": "opaque-file-v0",
            "input_sha256": _sha256(destination),
            "input_size": len(destination),
            "output_sha256": _sha256(replacement),
            "output_size": len(replacement),
            "edits": [
                {
                    "edit_index": 0,
                    "operation": "replace-whole-file",
                    "source_path": SOURCE_PATH,
                    "input_range": {"start": 0, "end": len(destination)},
                    "output_range": {"start": 0, "end": len(replacement)},
                }
            ],
        }
    ]
    assert _tree_snapshot(source_root) == before


def test_dry_run_preserves_authored_file_order(tmp_path: Path) -> None:
    source_root = tmp_path / "work-copy"
    first_destination = b"first destination"
    first_replacement = b"first replacement"
    second_destination = b"second destination"
    second_replacement = b"second replacement"
    _write_source_file(source_root, "CD/FIRST.OUT", first_destination)
    _write_source_file(source_root, "CD/FIRST.IN", first_replacement)
    _write_source_file(source_root, "CD/SECOND.OUT", second_destination)
    _write_source_file(source_root, "CD/SECOND.IN", second_replacement)
    manifest = _replacement_manifest(
        first_destination,
        first_replacement,
        destination_path="CD/FIRST.OUT",
        source_path="CD/FIRST.IN",
    )
    _append_replacement(
        manifest,
        second_destination,
        second_replacement,
        destination_path="CD/SECOND.OUT",
        source_path="CD/SECOND.IN",
    )

    report = dry_run_manifest(manifest, source_root)

    assert [entry["path"] for entry in report["files"]] == [
        "CD/FIRST.OUT",
        "CD/SECOND.OUT",
    ]


def test_cli_dry_run_is_byte_deterministic_and_write_free(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = _synthetic_dat()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    manifest_path = _write_json(
        tmp_path / "dry-run.json",
        _level_manifest(
            source,
            "dry-run-cli",
            [
                {
                    "operation": "set-scene-record-position",
                    "section": "primary",
                    "index": 0,
                    "position": [111, 222, 333],
                }
            ],
        ),
    )
    before = _tree_snapshot(tmp_path)
    outputs: list[str] = []

    for _ in range(2):
        assert (
            cli_main(
                [
                    "dry-run",
                    str(manifest_path),
                    "--source-root",
                    str(source_root),
                ]
            )
            == 0
        )
        captured = capsys.readouterr()
        assert captured.err == ""
        outputs.append(captured.out)

    assert outputs[0] == outputs[1]
    assert json.loads(outputs[0])["files"][0]["path"] == relative
    assert _tree_snapshot(tmp_path) == before


def test_cli_dry_run_later_file_failure_emits_no_report_or_write(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = _synthetic_dat()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    _write_work_copy(source_root, destination, replacement)
    manifest = _level_manifest(
        source,
        "dry-run-late-failure",
        [
            {
                "operation": "set-scene-record-position",
                "section": "primary",
                "index": 0,
                "position": [111, 222, 333],
            }
        ],
        schema_version=2,
    )
    _append_replacement(
        manifest,
        destination,
        replacement,
        destination_path=DESTINATION_PATH,
        source_path=SOURCE_PATH,
    )
    manifest["files"][1]["edits"][0]["source_sha256"] = "0" * 64
    manifest_path = _write_json(tmp_path / "late-failure.json", manifest)
    before = _tree_snapshot(tmp_path)

    result = cli_main(
        [
            "dry-run",
            str(manifest_path),
            "--source-root",
            str(source_root),
        ]
    )

    captured = capsys.readouterr()
    assert result == 2
    assert captured.out == ""
    assert "replacement SHA-256 mismatch" in captured.err
    assert _tree_snapshot(tmp_path) == before


def test_cli_dry_run_rejects_input_hash_without_report_or_write(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = _replacement_manifest(destination, replacement)
    manifest["files"][0]["sha256"] = "0" * 64
    manifest_path = _write_json(tmp_path / "bad-input-hash.json", manifest)
    before = _tree_snapshot(tmp_path)

    result = cli_main(
        [
            "dry-run",
            str(manifest_path),
            "--source-root",
            str(source_root),
        ]
    )

    captured = capsys.readouterr()
    assert result == 2
    assert captured.out == ""
    assert "SHA-256 mismatch" in captured.err
    assert _tree_snapshot(tmp_path) == before


def test_cli_dry_run_rejects_record_guard_without_report_or_write(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = _synthetic_dat()
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, "CD/LEVEL07/LEVEL1.DAT", source)
    manifest_path = _write_json(
        tmp_path / "bad-guard.json",
        _level_manifest(
            source,
            "dry-run-bad-guard",
            [
                {
                    "operation": "set-scene-record-field-0c",
                    "section": "primary",
                    "index": 0,
                    "expected_value": 999,
                    "value": 0,
                }
            ],
        ),
    )
    before = _tree_snapshot(tmp_path)

    result = cli_main(
        [
            "dry-run",
            str(manifest_path),
            "--source-root",
            str(source_root),
        ]
    )

    captured = capsys.readouterr()
    assert result == 2
    assert captured.out == ""
    assert "field +0x0c mismatch" in captured.err.lower()
    assert _tree_snapshot(tmp_path) == before


def test_cli_dry_run_rejects_protected_source_without_report_or_write(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "originals" / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest_path = _write_json(
        tmp_path / "protected.json",
        _replacement_manifest(destination, replacement),
    )
    before = _tree_snapshot(tmp_path)

    result = cli_main(
        [
            "dry-run",
            str(manifest_path),
            "--source-root",
            str(source_root),
        ]
    )

    captured = capsys.readouterr()
    assert result == 2
    assert captured.out == ""
    assert "protected content" in captured.err
    assert _tree_snapshot(tmp_path) == before


def test_compose_disjoint_same_file_is_order_independent_and_applies_and_stages(
    tmp_path: Path,
) -> None:
    source = _synthetic_dat()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    left = _level_manifest(
        source,
        "left-position",
        [
            {
                "operation": "set-scene-record-position",
                "section": "primary",
                "index": 0,
                "position": [111, 222, 333],
            }
        ],
    )
    right = _level_manifest(
        source,
        "right-field-0c",
        [
            {
                "operation": "set-scene-record-field-0c",
                "section": "primary",
                "index": 0,
                "expected_value": 0x123,
                "value": 0,
            }
        ],
    )

    composed = compose_manifests(left, right, source_root)
    reversed_composed = compose_manifests(right, left, source_root)

    assert _canonical_json_bytes(composed) == _canonical_json_bytes(reversed_composed)
    assert composed["schema_version"] == 1
    assert len(composed["files"]) == 1
    assert {edit["operation"] for edit in composed["files"][0]["edits"]} == {
        "set-scene-record-position",
        "set-scene-record-field-0c",
    }

    expected = LevelDat.parse(source).set_record_position(
        "primary", 0, (111, 222, 333)
    )
    expected = LevelDat.parse(expected).set_record_field_0c("primary", 0, 0x123, 0)
    overlay = tmp_path / "overlay"
    staged = tmp_path / "staged"
    overlay_receipt = apply_manifest(composed, source_root, overlay)
    staged_receipt = stage_manifest(composed, source_root, staged)

    assert (overlay / relative).read_bytes() == expected
    assert (staged / relative).read_bytes() == expected
    assert overlay_receipt == staged_receipt
    assert (source_root / relative).read_bytes() == source


def test_compose_preserves_order_sensitive_input_sequence_and_saved_application(
    tmp_path: Path,
) -> None:
    source = _synthetic_dat_with_order_sensitive_payload_target()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    payload_edit = {
        "operation": "set-scene-record-payload-target-offset",
        "section": "primary",
        "index": 0,
        "expected_target_offset": 0x98,
        "target_offset": 0x240,
    }
    position_edit = {
        "operation": "set-scene-record-position",
        "section": "primary",
        "index": 0,
        "position": [1, 2, 3],
    }
    field_edit = {
        "operation": "set-scene-record-field-0c",
        "section": "primary",
        "index": 0,
        "expected_value": 0x123,
        "value": 0,
    }
    left = _level_manifest(
        source, "left-valid-ordered", [payload_edit, position_edit]
    )
    right = _level_manifest(source, "right-disjoint", [field_edit])

    parsed = LevelDat.parse(source)
    record_offset = parsed.primary_records[0].offset
    reference = parsed.payload_target_reference("primary", 0)
    target_field = reference.payload_offset + reference.target_field_offset
    assert (record_offset, record_offset + 12) == (0x98, 0xA4)
    assert (record_offset + 12, record_offset + 14) == (0xA4, 0xA6)
    assert (target_field, target_field + 4) == (0x21C, 0x220)
    assert all(
        max(left_start, 0xA4) >= min(left_end, 0xA6)
        for left_start, left_end in ((0x21C, 0x220), (0x98, 0xA4))
    )

    left_overlay = tmp_path / "left-overlay"
    right_overlay = tmp_path / "right-overlay"
    apply_manifest(left, source_root, left_overlay)
    apply_manifest(right, source_root, right_overlay)
    assert (left_overlay / relative).is_file()
    assert (right_overlay / relative).is_file()

    composed = compose_manifests(left, right, source_root)
    reversed_composed = compose_manifests(right, left, source_root)
    assert _canonical_json_bytes(composed) == _canonical_json_bytes(reversed_composed)
    composed_edits = composed["files"][0]["edits"]
    assert composed_edits.index(payload_edit) < composed_edits.index(position_edit)

    expected = parsed.set_record_payload_target_offset("primary", 0, 0x98, 0x240)
    expected = LevelDat.parse(expected).set_record_position("primary", 0, (1, 2, 3))
    expected = LevelDat.parse(expected).set_record_field_0c("primary", 0, 0x123, 0)
    saved = load_manifest(_write_json(tmp_path / "composed.json", composed))
    overlay = tmp_path / "overlay"
    staged = tmp_path / "staged"
    overlay_receipt = apply_manifest(saved, source_root, overlay)
    staged_receipt = stage_manifest(saved, source_root, staged)

    assert (overlay / relative).read_bytes() == expected
    assert (staged / relative).read_bytes() == expected
    assert overlay_receipt == staged_receipt
    assert (source_root / relative).read_bytes() == source


def test_compose_preserves_descending_offsets_within_one_input(tmp_path: Path) -> None:
    source = _synthetic_dat_with_payload_target()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    field_edit = {
        "operation": "set-scene-record-field-0c",
        "section": "primary",
        "index": 0,
        "expected_value": 0x123,
        "value": 0,
    }
    position_edit = {
        "operation": "set-scene-record-position",
        "section": "primary",
        "index": 0,
        "position": [1, 2, 3],
    }
    target_edit = {
        "operation": "set-scene-record-payload-target-offset",
        "section": "primary",
        "index": 0,
        "expected_target_offset": 0x240,
        "target_offset": 0x248,
    }
    descending = _level_manifest(
        source, "descending-offsets", [field_edit, position_edit]
    )
    disjoint = _level_manifest(source, "disjoint-target", [target_edit])

    composed = compose_manifests(descending, disjoint, source_root)
    reversed_composed = compose_manifests(disjoint, descending, source_root)
    assert _canonical_json_bytes(composed) == _canonical_json_bytes(reversed_composed)
    edits = composed["files"][0]["edits"]
    assert edits.index(field_edit) < edits.index(position_edit)


def test_compose_preserves_same_span_sequential_guards(tmp_path: Path) -> None:
    source = _synthetic_dat()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    first_field = {
        "operation": "set-scene-record-field-0c",
        "section": "primary",
        "index": 0,
        "expected_value": 0x123,
        "value": 0x124,
    }
    second_field = {
        "operation": "set-scene-record-field-0c",
        "section": "primary",
        "index": 0,
        "expected_value": 0x124,
        "value": 0,
    }
    position = {
        "operation": "set-scene-record-position",
        "section": "primary",
        "index": 0,
        "position": [1, 2, 3],
    }
    sequential = _level_manifest(
        source, "sequential-guards", [first_field, second_field]
    )
    disjoint = _level_manifest(source, "disjoint-position", [position])

    composed = compose_manifests(sequential, disjoint, source_root)
    reversed_composed = compose_manifests(disjoint, sequential, source_root)
    assert _canonical_json_bytes(composed) == _canonical_json_bytes(reversed_composed)
    edits = composed["files"][0]["edits"]
    assert edits.index(first_field) < edits.index(second_field)
    expected = LevelDat.parse(source).set_record_field_0c(
        "primary", 0, 0x123, 0x124
    )
    expected = LevelDat.parse(expected).set_record_field_0c(
        "primary", 0, 0x124, 0
    )
    expected = LevelDat.parse(expected).set_record_position("primary", 0, (1, 2, 3))
    overlay = tmp_path / "overlay"
    apply_manifest(composed, source_root, overlay)
    assert (overlay / relative).read_bytes() == expected


def test_compose_different_files_selects_schema_two_and_normalizes_hashes(
    tmp_path: Path,
) -> None:
    level_source = _synthetic_dat()
    level_relative = "CD/LEVEL07/LEVEL1.DAT"
    destination = b"opaque destination"
    replacement = b"opaque replacement"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, level_relative, level_source)
    _write_work_copy(source_root, destination, replacement)
    level = _level_manifest(
        level_source,
        "level-edit",
        [
            {
                "operation": "set-scene-record-field-0c",
                "section": "primary",
                "index": 0,
                "expected_value": 0x123,
                "value": 0,
            }
        ],
    )
    opaque = _replacement_manifest(destination, replacement)
    opaque["files"][0]["sha256"] = opaque["files"][0]["sha256"].upper()
    opaque["files"][0]["edits"][0]["source_sha256"] = opaque["files"][0][
        "edits"
    ][0]["source_sha256"].upper()

    composed = compose_manifests(level, opaque, source_root)
    reversed_composed = compose_manifests(opaque, level, source_root)

    assert _canonical_json_bytes(composed) == _canonical_json_bytes(reversed_composed)
    assert composed["schema_version"] == 2
    assert [entry["path"] for entry in composed["files"]] == [
        DESTINATION_PATH,
        level_relative,
    ]
    opaque_entry = composed["files"][0]
    assert opaque_entry["sha256"] == opaque_entry["sha256"].lower()
    assert opaque_entry["edits"][0]["source_sha256"] == opaque_entry["edits"][
        0
    ]["source_sha256"].lower()

    expected_level = LevelDat.parse(level_source).set_record_field_0c(
        "primary", 0, 0x123, 0
    )
    overlay = tmp_path / "overlay"
    staged = tmp_path / "staged"
    apply_manifest(composed, source_root, overlay)
    stage_manifest(composed, source_root, staged)
    for root in (overlay, staged):
        assert (root / level_relative).read_bytes() == expected_level
        assert (root / DESTINATION_PATH).read_bytes() == replacement
    assert (source_root / level_relative).read_bytes() == level_source
    assert (source_root / DESTINATION_PATH).read_bytes() == destination


def test_cli_compose_success_stdout_is_byte_identical_when_inputs_are_reversed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = _synthetic_dat()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    left = _write_json(
        tmp_path / "left.json",
        _level_manifest(
            source,
            "left-position",
            [
                {
                    "operation": "set-scene-record-position",
                    "section": "primary",
                    "index": 0,
                    "position": [111, 222, 333],
                }
            ],
        ),
    )
    right = _write_json(
        tmp_path / "right.json",
        _level_manifest(
            source,
            "right-field",
            [
                {
                    "operation": "set-scene-record-field-0c",
                    "section": "primary",
                    "index": 0,
                    "expected_value": 0x123,
                    "value": 0,
                }
            ],
        ),
    )

    outputs = []
    for first, second in ((left, right), (right, left)):
        assert (
            cli_main(
                [
                    "compose",
                    str(first),
                    str(second),
                    "--source-root",
                    str(source_root),
                ]
            )
            == 0
        )
        outputs.append(capsys.readouterr())

    assert outputs[0].err == outputs[1].err == ""
    assert outputs[0].out == outputs[1].out
    emitted = json.loads(outputs[0].out)
    assert emitted["name"].startswith("composed-")
    assert emitted["schema_version"] == 1


def test_compose_field_0c_overlap_reports_exact_two_byte_span(tmp_path: Path) -> None:
    source = _synthetic_dat()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    manifests = [
        _level_manifest(
            source,
            name,
            [
                {
                    "operation": "set-scene-record-field-0c",
                    "section": "primary",
                    "index": 0,
                    "expected_value": 0x123,
                    "value": value,
                }
            ],
        )
        for name, value in (("field-left", 1), ("field-right", 2))
    ]

    with pytest.raises(ManifestCompositionConflict) as caught:
        compose_manifests(manifests[0], manifests[1], source_root)

    record_offset = LevelDat.parse(source).primary_records[0].offset
    assert caught.value.report["kind"] == "overlapping-byte-claims"
    assert caught.value.report["overlap"] == [record_offset + 12, record_offset + 14]


def test_compose_payload_target_overlap_reports_exact_four_byte_span(
    tmp_path: Path,
) -> None:
    source = _synthetic_dat_with_payload_target()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    left = _level_manifest(
        source,
        "target-left",
        [
            {
                "operation": "set-scene-record-payload-target-offset",
                "section": "primary",
                "index": 0,
                "expected_target_offset": 0x240,
                "target_offset": 0x248,
            }
        ],
    )
    right = _level_manifest(
        source,
        "target-right",
        [
            {
                "operation": "set-scene-record-payload-target-offset",
                "section": "primary",
                "index": 0,
                "expected_target_offset": 0x240,
                "target_offset": 0x240,
            }
        ],
    )

    with pytest.raises(ManifestCompositionConflict) as caught:
        compose_manifests(left, right, source_root)

    assert caught.value.report["kind"] == "overlapping-byte-claims"
    assert caught.value.report["destination"] == relative.casefold()
    assert caught.value.report["overlap"] == [0x21C, 0x220]


def test_cli_compose_overlap_report_is_order_independent_and_writes_nothing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = _synthetic_dat()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    manifests = []
    for name, position in (("left", [1, 2, 3]), ("right", [4, 5, 6])):
        manifests.append(
            _write_json(
                tmp_path / f"{name}.json",
                _level_manifest(
                    source,
                    name,
                    [
                        {
                            "operation": "set-scene-record-position",
                            "section": "primary",
                            "index": 0,
                            "position": position,
                        }
                    ],
                ),
            )
        )
    before_paths = _tree_paths(tmp_path)
    source_hash = _sha256((source_root / relative).read_bytes())

    first_result = cli_main(
        [
            "compose",
            str(manifests[0]),
            str(manifests[1]),
            "--source-root",
            str(source_root),
        ]
    )
    first = capsys.readouterr()
    second_result = cli_main(
        [
            "compose",
            str(manifests[1]),
            str(manifests[0]),
            "--source-root",
            str(source_root),
        ]
    )
    second = capsys.readouterr()

    record_offset = LevelDat.parse(source).primary_records[0].offset
    assert first_result == second_result == 2
    assert first.out == second.out == ""
    assert first.err == second.err
    report = json.loads(first.err)
    assert report["kind"] == "overlapping-byte-claims"
    assert report["overlap"] == [record_offset, record_offset + 12]
    assert [item["name"] for item in report["inputs"]] in (
        ["left", "right"],
        ["right", "left"],
    )
    assert _tree_paths(tmp_path) == before_paths
    assert _sha256((source_root / relative).read_bytes()) == source_hash


def test_cli_compose_opaque_collision_is_order_independent_and_asset_free(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    destination = b"GAME-BYTE-SENTINEL-A"
    replacement_a = b"GAME-BYTE-SENTINEL-B"
    replacement_b = b"GAME-BYTE-SENTINEL-C"
    source_root = tmp_path / "work-copy"
    for relative, data in (
        ("CD/A.bin", destination),
        ("CD/source-a.bin", replacement_a),
        ("CD/source-b.bin", replacement_b),
    ):
        _write_source_file(source_root, relative, data)
    left = _replacement_manifest(
        destination,
        replacement_a,
        destination_path="CD/A.bin",
        source_path="CD/source-a.bin",
    )
    left["name"] = "opaque-left"
    right = _replacement_manifest(
        destination,
        replacement_b,
        destination_path="CD/A.bin",
        source_path="CD/source-b.bin",
    )
    right["name"] = "opaque-right"
    paths = [
        _write_json(tmp_path / "opaque-left.json", left),
        _write_json(tmp_path / "opaque-right.json", right),
    ]
    before_paths = _tree_paths(tmp_path)

    outputs = []
    for first, second in (paths, paths[::-1]):
        assert (
            cli_main(
                [
                    "compose",
                    str(first),
                    str(second),
                    "--source-root",
                    str(source_root),
                ]
            )
            == 2
        )
        outputs.append(capsys.readouterr())

    assert outputs[0].out == outputs[1].out == ""
    assert outputs[0].err == outputs[1].err
    report = json.loads(outputs[0].err)
    assert report == {
        "destination": "cd/a.bin",
        "error": "manifest-composition-conflict",
        "inputs": report["inputs"],
        "kind": "opaque-whole-file-collision",
        "overlap": [0, len(destination)],
    }
    assert set(report) == {"destination", "error", "inputs", "kind", "overlap"}
    assert destination.decode() not in outputs[0].err
    assert replacement_a.decode() not in outputs[0].err
    assert replacement_b.decode() not in outputs[0].err
    assert _tree_paths(tmp_path) == before_paths


def test_compose_empty_opaque_collision_and_unequal_distinct_replacements(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "work-copy"
    values = {
        "CD/empty.bin": b"",
        "CD/empty-source-a.bin": b"a",
        "CD/empty-source-b.bin": b"bb",
        "CD/short.bin": b"short",
        "CD/short-source.bin": b"x",
        "CD/long.bin": b"long",
        "CD/long-source.bin": b"unequal replacement",
    }
    for relative, data in values.items():
        _write_source_file(source_root, relative, data)

    empty_left = _replacement_manifest(
        values["CD/empty.bin"],
        values["CD/empty-source-a.bin"],
        destination_path="CD/empty.bin",
        source_path="CD/empty-source-a.bin",
    )
    empty_right = _replacement_manifest(
        values["CD/empty.bin"],
        values["CD/empty-source-b.bin"],
        destination_path="CD/empty.bin",
        source_path="CD/empty-source-b.bin",
    )
    with pytest.raises(ManifestCompositionConflict) as forward:
        compose_manifests(empty_left, empty_right, source_root)
    with pytest.raises(ManifestCompositionConflict) as reverse:
        compose_manifests(empty_right, empty_left, source_root)
    assert forward.value.report == reverse.value.report
    assert forward.value.report["overlap"] == [0, 0]

    short = _replacement_manifest(
        values["CD/short.bin"],
        values["CD/short-source.bin"],
        destination_path="CD/short.bin",
        source_path="CD/short-source.bin",
    )
    long = _replacement_manifest(
        values["CD/long.bin"],
        values["CD/long-source.bin"],
        destination_path="CD/long.bin",
        source_path="CD/long-source.bin",
    )
    composed = compose_manifests(short, long, source_root)
    reversed_composed = compose_manifests(long, short, source_root)
    assert _canonical_json_bytes(composed) == _canonical_json_bytes(reversed_composed)
    overlay = tmp_path / "overlay"
    apply_manifest(composed, source_root, overlay)
    assert (overlay / "CD/short.bin").read_bytes() == b"x"
    assert (overlay / "CD/long.bin").read_bytes() == b"unequal replacement"


def test_compose_selects_first_overlap_deterministically_when_multiple_exist(
    tmp_path: Path,
) -> None:
    source = _synthetic_dat()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    manifests = []
    for name, position, field in (
        ("multiple-left", [1, 2, 3], 1),
        ("multiple-right", [4, 5, 6], 2),
    ):
        manifests.append(
            _level_manifest(
                source,
                name,
                [
                    {
                        "operation": "set-scene-record-field-0c",
                        "section": "primary",
                        "index": 0,
                        "expected_value": 0x123,
                        "value": field,
                    },
                    {
                        "operation": "set-scene-record-position",
                        "section": "primary",
                        "index": 0,
                        "position": position,
                    },
                ],
            )
        )

    with pytest.raises(ManifestCompositionConflict) as forward:
        compose_manifests(manifests[0], manifests[1], source_root)
    with pytest.raises(ManifestCompositionConflict) as reverse:
        compose_manifests(manifests[1], manifests[0], source_root)
    record_offset = LevelDat.parse(source).primary_records[0].offset
    assert forward.value.report == reverse.value.report
    assert forward.value.report["overlap"] == [record_offset, record_offset + 12]


def test_compose_rejects_case_insensitive_destination_spelling_collision(
    tmp_path: Path,
) -> None:
    source = _synthetic_dat()
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, "CD/A.DAT", source)
    _write_source_file(source_root, "cd/a.dat", source)
    left = _level_manifest(
        source,
        "upper-path",
        [
            {
                "operation": "set-scene-record-position",
                "section": "primary",
                "index": 0,
                "position": [1, 2, 3],
            }
        ],
        path="CD/A.DAT",
    )
    right = _level_manifest(
        source,
        "lower-path",
        [
            {
                "operation": "set-scene-record-field-0c",
                "section": "primary",
                "index": 0,
                "expected_value": 0x123,
                "value": 0,
            }
        ],
        path="cd/a.dat",
    )

    with pytest.raises(ManifestCompositionConflict) as caught:
        compose_manifests(left, right, source_root)

    assert caught.value.report["kind"] == "case-insensitive-path-collision"
    assert caught.value.report["destination"] == "cd/a.dat"
    assert caught.value.report["overlap"] is None


def test_compose_rejects_cross_manifest_replacement_source_destination_collision(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "work-copy"
    values = {"CD/A.bin": b"a", "CD/B.bin": b"b", "CD/C.bin": b"c"}
    for relative, data in values.items():
        _write_source_file(source_root, relative, data)
    left = _replacement_manifest(
        values["CD/A.bin"],
        values["CD/B.bin"],
        destination_path="CD/A.bin",
        source_path="CD/B.bin",
    )
    left["name"] = "a-from-b"
    right = _replacement_manifest(
        values["CD/B.bin"],
        values["CD/C.bin"],
        destination_path="CD/B.bin",
        source_path="CD/C.bin",
    )
    right["name"] = "b-from-c"

    with pytest.raises(ManifestCompositionConflict) as caught:
        compose_manifests(left, right, source_root)

    assert caught.value.report["kind"] == "replacement-source-destination-collision"
    assert caught.value.report["destination"] == "cd/b.bin"
    assert caught.value.report["overlap"] is None


def test_compose_rejects_same_destination_format_mismatch(tmp_path: Path) -> None:
    source = _synthetic_dat()
    replacement = b"replacement"
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    _write_source_file(source_root, "CD/source.bin", replacement)
    level = _level_manifest(
        source,
        "level-format",
        [
            {
                "operation": "set-scene-record-position",
                "section": "primary",
                "index": 0,
                "position": [1, 2, 3],
            }
        ],
    )
    opaque = _replacement_manifest(
        source,
        replacement,
        destination_path=relative,
        source_path="CD/source.bin",
    )
    opaque["name"] = "opaque-format"

    with pytest.raises(ManifestCompositionConflict) as caught:
        compose_manifests(level, opaque, source_root)

    assert caught.value.report["kind"] == "format-mismatch"
    assert caught.value.report["destination"] == relative.casefold()
    assert caught.value.report["overlap"] is None


def test_compose_reports_same_destination_source_hash_mismatch_before_emission(
    tmp_path: Path,
) -> None:
    source = _synthetic_dat()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    left = _level_manifest(
        source,
        "correct-hash",
        [
            {
                "operation": "set-scene-record-position",
                "section": "primary",
                "index": 0,
                "position": [1, 2, 3],
            }
        ],
    )
    right = _level_manifest(
        source,
        "different-hash",
        [
            {
                "operation": "set-scene-record-field-0c",
                "section": "primary",
                "index": 0,
                "expected_value": 0x123,
                "value": 0,
            }
        ],
    )
    right["files"][0]["sha256"] = "0" * 64

    with pytest.raises(ManifestCompositionConflict) as caught:
        compose_manifests(left, right, source_root)

    assert caught.value.report["kind"] == "source-hash-mismatch"
    assert caught.value.report["destination"] == relative.casefold()
    assert caught.value.report["overlap"] is None


def test_whole_file_replacement_builds_byte_exact_sparse_overlay_and_receipt(
    tmp_path: Path,
) -> None:
    destination = b"original destination bytes"
    replacement = b"replacement bytes from the same work copy"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )

    first_output = tmp_path / "overlay-a"
    first_receipt = apply_manifest(manifest, source_root, first_output)
    second_output = tmp_path / "overlay-b"
    second_receipt = apply_manifest(manifest, source_root, second_output)

    assert (first_output / DESTINATION_PATH).read_bytes() == replacement
    assert not (first_output / SOURCE_PATH).exists()
    assert (source_root / DESTINATION_PATH).read_bytes() == destination
    assert (source_root / SOURCE_PATH).read_bytes() == replacement
    assert first_receipt == second_receipt
    assert (
        first_output / ".ablpc/receipt.json"
    ).read_bytes() == (second_output / ".ablpc/receipt.json").read_bytes()
    assert first_receipt == {
        "schema_version": 2,
        "manifest_name": "synthetic-whole-file-replacement",
        "files": [
            {
                "path": DESTINATION_PATH,
                "input_sha256": _sha256(destination),
                "output_sha256": _sha256(replacement),
                "edits": [
                    {
                        "edit_index": 0,
                        "operation": "replace-whole-file",
                        "source_path": SOURCE_PATH,
                        "replacement_sha256": _sha256(replacement),
                    }
                ],
            }
        ],
    }


def test_remove_single_file_sparse_overlay_recomputes_receipt_and_preserves_source(
    tmp_path: Path,
) -> None:
    destination = b"original destination bytes"
    replacement = b"replacement bytes"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    source_before = _tree_snapshot(source_root)
    overlay = tmp_path / "overlay"
    applied_receipt = apply_manifest(manifest, source_root, overlay)

    removed_receipt = remove_manifest(manifest, source_root, overlay)

    assert removed_receipt == applied_receipt
    assert not overlay.exists()
    assert _tree_snapshot(source_root) == source_before


def test_remove_accepts_an_empty_recorded_output(tmp_path: Path) -> None:
    destination = b"destination"
    replacement = b""
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    source_before = _tree_snapshot(source_root)
    overlay = tmp_path / "overlay"
    receipt = apply_manifest(manifest, source_root, overlay)
    assert (overlay / DESTINATION_PATH).read_bytes() == b""

    assert remove_manifest(manifest, source_root, overlay) == receipt
    assert not overlay.exists()
    assert _tree_snapshot(source_root) == source_before


def test_remove_multi_file_sparse_overlay_prunes_only_authenticated_tree(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "work-copy"
    pairs = (
        ("A/one.bin", b"destination one", "SOURCE/one.bin", b"replacement one"),
        ("B/deep/two.bin", b"destination two", "SOURCE/two.bin", b"replacement two"),
    )
    for destination_path, destination, source_path, replacement in pairs:
        _write_source_file(source_root, destination_path, destination)
        _write_source_file(source_root, source_path, replacement)
    manifest_value = _replacement_manifest(
        pairs[0][1],
        pairs[0][3],
        destination_path=pairs[0][0],
        source_path=pairs[0][2],
    )
    _append_replacement(
        manifest_value,
        pairs[1][1],
        pairs[1][3],
        destination_path=pairs[1][0],
        source_path=pairs[1][2],
    )
    manifest = load_manifest(_write_json(tmp_path / "multi.json", manifest_value))
    source_before = _tree_snapshot(source_root)
    overlay = tmp_path / "overlay"
    receipt = apply_manifest(manifest, source_root, overlay)

    assert remove_manifest(manifest, source_root, overlay) == receipt
    assert not overlay.exists()
    assert _tree_snapshot(source_root) == source_before


def test_remove_composed_manifest_sparse_overlay_preserves_source(tmp_path: Path) -> None:
    source = _synthetic_dat()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    left = _level_manifest(
        source,
        "left-position",
        [
            {
                "operation": "set-scene-record-position",
                "section": "primary",
                "index": 0,
                "position": [111, 222, 333],
            }
        ],
    )
    right = _level_manifest(
        source,
        "right-field",
        [
            {
                "operation": "set-scene-record-field-0c",
                "section": "primary",
                "index": 0,
                "expected_value": 0x123,
                "value": 0,
            }
        ],
    )
    composed = compose_manifests(left, right, source_root)
    source_before = _tree_snapshot(source_root)
    overlay = tmp_path / "overlay"
    receipt = apply_manifest(composed, source_root, overlay)

    assert remove_manifest(composed, source_root, overlay) == receipt
    assert not overlay.exists()
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize("schema_version", [1, 2])
@pytest.mark.parametrize(
    "edit",
    [
        {
            "operation": "set-scene-record-position",
            "section": "primary",
            "index": 0,
            "position": [111, 222, 333],
        },
        {
            "operation": "set-scene-record-field-0c",
            "section": "primary",
            "index": 0,
            "expected_value": 0x123,
            "value": 0,
        },
        {
            "operation": "set-scene-record-payload-target-offset",
            "section": "primary",
            "index": 0,
            "expected_target_offset": 0x240,
            "target_offset": 0x248,
        },
    ],
    ids=("position", "field-0c", "payload-target"),
)
def test_receipt_replays_and_removes_every_level_operation_without_manifest(
    tmp_path: Path, schema_version: int, edit: dict[str, object]
) -> None:
    source = _synthetic_dat_with_payload_target()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    manifest = _level_manifest(
        source,
        f"receipt-level-{schema_version}-{edit['operation']}",
        [copy.deepcopy(edit)],
        schema_version=schema_version,
    )
    source_before = _tree_snapshot(source_root)
    ordinary = tmp_path / "ordinary-overlay"
    ordinary_receipt = apply_manifest(manifest, source_root, ordinary)
    receipt_path = tmp_path / "external-receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())

    replayed = tmp_path / "replayed-overlay"
    replayed_receipt = replay_receipt(receipt_path, source_root, replayed)

    assert replayed_receipt == ordinary_receipt
    assert _tree_snapshot(replayed) == _tree_snapshot(ordinary)
    assert _tree_snapshot(source_root) == source_before
    assert remove_receipt(receipt_path, source_root, replayed) == ordinary_receipt
    assert not replayed.exists()
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize(
    "replacement", [b"", b"short", b"a replacement longer than the destination"]
)
def test_receipt_replays_and_removes_opaque_replacement_without_manifest(
    tmp_path: Path, replacement: bytes
) -> None:
    destination = b"longer original destination"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = _replacement_manifest(destination, replacement)
    source_before = _tree_snapshot(source_root)
    ordinary = tmp_path / "ordinary-overlay"
    receipt = apply_manifest(manifest, source_root, ordinary)
    receipt_path = tmp_path / "external-receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())

    replayed = tmp_path / "replayed-overlay"
    assert replay_receipt(receipt_path, source_root, replayed) == receipt
    assert _tree_snapshot(replayed) == _tree_snapshot(ordinary)
    assert remove_receipt(receipt_path, source_root, replayed) == receipt
    assert not replayed.exists()
    assert _tree_snapshot(source_root) == source_before


def test_receipt_replays_and_removes_a_no_op_level_edit(tmp_path: Path) -> None:
    source = _synthetic_dat()
    relative = "CD/LEVEL07/LEVEL1.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, relative, source)
    manifest = _level_manifest(
        source,
        "receipt-no-op",
        [
            {
                "operation": "set-scene-record-position",
                "section": "primary",
                "index": 0,
                "position": [10, 20, 30],
            }
        ],
        schema_version=2,
    )
    ordinary = tmp_path / "ordinary-overlay"
    receipt = apply_manifest(manifest, source_root, ordinary)
    receipt_path = tmp_path / "external-receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())

    replayed = tmp_path / "replayed-overlay"
    assert replay_receipt(receipt_path, source_root, replayed) == receipt
    assert (replayed / relative).read_bytes() == source
    assert receipt["files"][0]["input_sha256"] == receipt["files"][0][
        "output_sha256"
    ]
    assert remove_receipt(receipt_path, source_root, replayed) == receipt
    assert not replayed.exists()


def test_receipt_replays_and_removes_composed_multi_file_manifest(
    tmp_path: Path,
) -> None:
    source = _synthetic_dat()
    first_path = "Z/LATE.DAT"
    second_path = "A/EARLY.DAT"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, first_path, source)
    _write_source_file(source_root, second_path, source)
    left = _level_manifest(
        source,
        "left",
        [
            {
                "operation": "set-scene-record-position",
                "section": "primary",
                "index": 0,
                "position": [111, 222, 333],
            }
        ],
        path=first_path,
        schema_version=2,
    )
    right = _level_manifest(
        source,
        "right",
        [
            {
                "operation": "set-scene-record-field-0c",
                "section": "primary",
                "index": 0,
                "expected_value": 0x123,
                "value": 0,
            }
        ],
        path=second_path,
        schema_version=2,
    )
    composed = compose_manifests(left, right, source_root)
    ordinary = tmp_path / "ordinary-overlay"
    receipt = apply_manifest(composed, source_root, ordinary)
    receipt_path = tmp_path / "external-receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    source_before = _tree_snapshot(source_root)

    replayed = tmp_path / "replayed-overlay"
    assert replay_receipt(receipt_path, source_root, replayed) == receipt
    assert _tree_snapshot(replayed) == _tree_snapshot(ordinary)
    assert remove_receipt(receipt_path, source_root, replayed) == receipt
    assert not replayed.exists()
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize(
    "mutation",
    [
        "root-extra",
        "schema",
        "name",
        "file-extra",
        "unsafe-path",
        "uppercase-input",
        "uppercase-output",
        "uppercase-replacement",
        "edit-index",
        "missing-edit-field",
        "unknown-operation",
        "duplicate-path",
        "input-hash",
        "output-hash",
        "replacement-hash",
    ],
)
def test_receipt_replay_rejects_structural_ambiguous_and_forged_input_before_write(
    tmp_path: Path, mutation: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    receipt = apply_manifest(
        _replacement_manifest(destination, replacement), source_root, ordinary
    )
    forged = copy.deepcopy(receipt)
    if mutation == "root-extra":
        forged["unexpected"] = True
    elif mutation == "schema":
        forged["schema_version"] = 1
    elif mutation == "name":
        forged["manifest_name"] = ""
    elif mutation == "file-extra":
        forged["files"][0]["unexpected"] = True
    elif mutation == "unsafe-path":
        forged["files"][0]["path"] = "../escape.bin"
    elif mutation == "uppercase-input":
        forged["files"][0]["input_sha256"] = forged["files"][0][
            "input_sha256"
        ].upper()
    elif mutation == "uppercase-output":
        forged["files"][0]["output_sha256"] = forged["files"][0][
            "output_sha256"
        ].upper()
    elif mutation == "uppercase-replacement":
        forged["files"][0]["edits"][0]["replacement_sha256"] = forged[
            "files"
        ][0]["edits"][0]["replacement_sha256"].upper()
    elif mutation == "edit-index":
        forged["files"][0]["edits"][0]["edit_index"] = 1
    elif mutation == "missing-edit-field":
        del forged["files"][0]["edits"][0]["source_path"]
    elif mutation == "unknown-operation":
        forged["files"][0]["edits"][0]["operation"] = "unknown"
    elif mutation == "duplicate-path":
        forged["files"].append(copy.deepcopy(forged["files"][0]))
    elif mutation == "input-hash":
        forged["files"][0]["input_sha256"] = "0" * 64
    elif mutation == "output-hash":
        forged["files"][0]["output_sha256"] = "0" * 64
    else:
        forged["files"][0]["edits"][0]["replacement_sha256"] = "0" * 64
    receipt_path = tmp_path / "forged-receipt.json"
    receipt_path.write_text(json.dumps(forged, indent=2) + "\n", encoding="utf-8")
    source_before = _tree_snapshot(source_root)
    output = tmp_path / "output"

    with pytest.raises(ManifestError):
        replay_receipt(receipt_path, source_root, output)

    assert not output.exists()
    assert _tree_snapshot(source_root) == source_before


def test_receipt_replay_prepares_every_file_before_writing(tmp_path: Path) -> None:
    source_root = tmp_path / "work-copy"
    first = ("A/one.bin", b"first destination", "SOURCE/one.bin", b"first output")
    second = ("B/two.bin", b"second destination", "SOURCE/two.bin", b"second output")
    for destination_path, destination, source_path, replacement in (first, second):
        _write_source_file(source_root, destination_path, destination)
        _write_source_file(source_root, source_path, replacement)
    manifest = _replacement_manifest(
        first[1], first[3], destination_path=first[0], source_path=first[2]
    )
    _append_replacement(
        manifest,
        second[1],
        second[3],
        destination_path=second[0],
        source_path=second[2],
    )
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(manifest, source_root, ordinary)
    receipt_path = tmp_path / "external-receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    (source_root / second[2]).unlink()
    source_before = _tree_snapshot(source_root)
    output = tmp_path / "replayed-overlay"

    with pytest.raises(ManifestError, match="does not exist"):
        replay_receipt(receipt_path, source_root, output)

    assert not output.exists()
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize("existing_content", [False, True])
def test_receipt_replay_requires_a_new_dedicated_output_root(
    tmp_path: Path, existing_content: bool
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    receipt_path = tmp_path / "external-receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    output = tmp_path / "existing-output"
    output.mkdir()
    if existing_content:
        (output / "unrelated.txt").write_text("preserve", encoding="utf-8")
    output_before = _tree_snapshot(output)
    source_before = _tree_snapshot(source_root)

    with pytest.raises(ManifestError, match="already exists"):
        replay_receipt(receipt_path, source_root, output)

    assert _tree_snapshot(output) == output_before
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize(
    "encoding",
    ["malformed", "duplicate", "compact", "crlf", "bom", "root-order", "deep"],
)
def test_receipt_replay_rejects_nonordinary_encoding_before_write(
    tmp_path: Path, encoding: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    receipt = apply_manifest(
        _replacement_manifest(destination, replacement), source_root, ordinary
    )
    ordinary_bytes = (ordinary / ".ablpc/receipt.json").read_bytes()
    if encoding == "malformed":
        data = b"{"
    elif encoding == "duplicate":
        data = ordinary_bytes.replace(
            b'  "schema_version": 2,',
            b'  "schema_version": 2,\n  "schema_version": 2,',
            1,
        )
    elif encoding == "compact":
        data = json.dumps(receipt).encode("utf-8")
    elif encoding == "crlf":
        data = ordinary_bytes.replace(b"\n", b"\r\n")
    elif encoding == "bom":
        data = b"\xef\xbb\xbf" + ordinary_bytes
    elif encoding == "root-order":
        reordered = {
            "files": receipt["files"],
            "manifest_name": receipt["manifest_name"],
            "schema_version": receipt["schema_version"],
        }
        data = (json.dumps(reordered, indent=2) + "\n").encode("utf-8")
    else:
        data = b"[" * 2000 + b"0" + b"]" * 2000
    receipt_path = tmp_path / "encoded-receipt.json"
    receipt_path.write_bytes(data)
    source_before = _tree_snapshot(source_root)
    output = tmp_path / "output"

    with pytest.raises(ManifestError):
        replay_receipt(receipt_path, source_root, output)

    assert not output.exists()
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize("kind", ["symlink", "hardlink", "directory", "fifo"])
def test_receipt_replay_rejects_nonregular_or_aliased_receipt_input(
    tmp_path: Path, kind: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    ordinary_receipt = ordinary / ".ablpc/receipt.json"
    receipt_path = tmp_path / "receipt-input"
    if kind == "symlink":
        receipt_path.symlink_to(ordinary_receipt)
    elif kind == "hardlink":
        os.link(ordinary_receipt, receipt_path)
    elif kind == "directory":
        receipt_path.mkdir()
    else:
        os.mkfifo(receipt_path)
    source_before = _tree_snapshot(source_root)
    output = tmp_path / "output"

    with pytest.raises(ManifestError):
        replay_receipt(receipt_path, source_root, output)

    assert not output.exists()
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize("replacement_kind", ["regular", "fifo"])
def test_receipt_replay_rejects_receipt_type_or_inode_swap_at_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    replacement_kind: str,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    receipt_path = tmp_path / "external-receipt.json"
    receipt_data = (ordinary / ".ablpc/receipt.json").read_bytes()
    receipt_path.write_bytes(receipt_data)
    real_open = manifest_module.os.open
    swapped = False

    def swap_then_open(
        path: object, flags: int, *args: object, **kwargs: object
    ) -> int:
        nonlocal swapped
        if (
            not swapped
            and Path(path) == Path(receipt_path.name)
            and kwargs.get("dir_fd") is not None
        ):
            swapped = True
            receipt_path.unlink()
            if replacement_kind == "regular":
                receipt_path.write_bytes(receipt_data)
            else:
                os.mkfifo(receipt_path)
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(manifest_module.os, "open", swap_then_open)
    source_before = _tree_snapshot(source_root)
    output = tmp_path / "output"

    with pytest.raises(ManifestError, match="changed before it could be read safely"):
        replay_receipt(receipt_path, source_root, output)

    assert not output.exists()
    assert _tree_snapshot(source_root) == source_before


def test_receipt_replay_rejects_receipt_change_during_descriptor_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    receipt_path = tmp_path / "external-receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    real_fstat = manifest_module.os.fstat
    regular_calls = 0

    def changed_second_fstat(descriptor: int) -> os.stat_result:
        nonlocal regular_calls
        result = real_fstat(descriptor)
        if not stat.S_ISREG(result.st_mode):
            return result
        regular_calls += 1
        if regular_calls != 2:
            return result
        fields = list(result)
        fields[6] += 1
        return os.stat_result(fields)

    monkeypatch.setattr(manifest_module.os, "fstat", changed_second_fstat)
    output = tmp_path / "output"

    with pytest.raises(ManifestError, match="changed while it was being read"):
        replay_receipt(receipt_path, source_root, output)

    assert not output.exists()


@pytest.mark.parametrize("workflow", ["replay", "remove-receipt"])
def test_receipt_parent_rename_and_link_substitution_rejects_before_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    workflow: str,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = _replacement_manifest(destination, replacement)
    overlay = tmp_path / "overlay"
    apply_manifest(manifest, source_root, overlay)
    external_parent = tmp_path / "external"
    external_parent.mkdir()
    receipt_path = external_parent / "receipt.json"
    receipt_path.write_bytes((overlay / ".ablpc/receipt.json").read_bytes())
    protected_parent = tmp_path / "originals"
    protected_parent.mkdir()
    moved_parent = protected_parent / "external"
    source_before = _tree_snapshot(source_root)
    overlay_before = _tree_snapshot(overlay)
    output = tmp_path / "replayed"
    real_open = manifest_module.os.open
    changed = False

    def change_parent_then_open(
        path: object, flags: int, *args: object, **kwargs: object
    ) -> int:
        nonlocal changed
        if (
            not changed
            and Path(path) == Path(receipt_path.name)
            and kwargs.get("dir_fd") is not None
        ):
            changed = True
            external_parent.rename(moved_parent)
            external_parent.symlink_to(moved_parent, target_is_directory=True)
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(manifest_module.os, "open", change_parent_then_open)

    with pytest.raises(ManifestError, match="protected content"):
        if workflow == "replay":
            replay_receipt(receipt_path, source_root, output)
        else:
            remove_receipt(receipt_path, source_root, overlay)

    assert changed
    assert external_parent.is_symlink()
    assert receipt_path.resolve() == moved_parent / "receipt.json"
    assert not output.exists()
    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(overlay) == overlay_before


def test_receipt_parent_inode_replacement_rejects_before_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    external_parent = tmp_path / "external"
    external_parent.mkdir()
    receipt_path = external_parent / "receipt.json"
    receipt_data = (ordinary / ".ablpc/receipt.json").read_bytes()
    receipt_path.write_bytes(receipt_data)
    moved_parent = tmp_path / "moved-external"
    source_before = _tree_snapshot(source_root)
    output = tmp_path / "replayed"
    real_open = manifest_module.os.open
    changed = False

    def replace_parent_then_open(
        path: object, flags: int, *args: object, **kwargs: object
    ) -> int:
        nonlocal changed
        if (
            not changed
            and Path(path) == Path(receipt_path.name)
            and kwargs.get("dir_fd") is not None
        ):
            changed = True
            external_parent.rename(moved_parent)
            external_parent.mkdir()
            receipt_path.write_bytes(receipt_data)
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(manifest_module.os, "open", replace_parent_then_open)

    with pytest.raises(ManifestError, match="path changed"):
        replay_receipt(receipt_path, source_root, output)

    assert changed
    assert not output.exists()
    assert _tree_snapshot(source_root) == source_before


def test_receipt_parent_inode_swap_during_component_open_rejects_before_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    external_parent = tmp_path / "external"
    external_parent.mkdir()
    receipt_path = external_parent / "receipt.json"
    receipt_data = (ordinary / ".ablpc/receipt.json").read_bytes()
    receipt_path.write_bytes(receipt_data)
    moved_parent = tmp_path / "moved-external"
    source_before = _tree_snapshot(source_root)
    output = tmp_path / "replayed"
    real_open = manifest_module.os.open
    changed = False

    def replace_component_then_open(
        path: object, flags: int, *args: object, **kwargs: object
    ) -> int:
        nonlocal changed
        if (
            not changed
            and Path(path) == Path(external_parent.name)
            and kwargs.get("dir_fd") is not None
        ):
            changed = True
            external_parent.rename(moved_parent)
            external_parent.mkdir()
            receipt_path.write_bytes(receipt_data)
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(manifest_module.os, "open", replace_component_then_open)

    with pytest.raises(ManifestError, match="ancestor changed"):
        replay_receipt(receipt_path, source_root, output)

    assert changed
    assert not output.exists()
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize("change", ["hardlink", "metadata"])
def test_receipt_final_link_or_metadata_change_at_open_rejects_before_replay(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    change: str,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    receipt_path = tmp_path / "external-receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    source_before = _tree_snapshot(source_root)
    output = tmp_path / "replayed"
    real_open = manifest_module.os.open
    changed = False

    def change_final_then_open(
        path: object, flags: int, *args: object, **kwargs: object
    ) -> int:
        nonlocal changed
        if (
            not changed
            and Path(path) == Path(receipt_path.name)
            and kwargs.get("dir_fd") is not None
        ):
            changed = True
            if change == "hardlink":
                os.link(receipt_path, tmp_path / "receipt-hardlink.json")
            else:
                metadata = receipt_path.stat()
                os.utime(
                    receipt_path,
                    ns=(metadata.st_atime_ns, metadata.st_mtime_ns + 1_000_000_000),
                )
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(manifest_module.os, "open", change_final_then_open)

    with pytest.raises(ManifestError, match="changed before it could be read safely"):
        replay_receipt(receipt_path, source_root, output)

    assert changed
    assert not output.exists()
    assert _tree_snapshot(source_root) == source_before


def test_cli_parent_link_substitution_has_empty_stdout_and_no_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    external_parent = tmp_path / "external"
    external_parent.mkdir()
    receipt_path = external_parent / "receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    protected_parent = tmp_path / "media"
    protected_parent.mkdir()
    moved_parent = protected_parent / "external"
    output = tmp_path / "replayed"
    source_before = _tree_snapshot(source_root)
    real_open = manifest_module.os.open
    changed = False

    def change_parent_then_open(
        path: object, flags: int, *args: object, **kwargs: object
    ) -> int:
        nonlocal changed
        if (
            not changed
            and Path(path) == Path(receipt_path.name)
            and kwargs.get("dir_fd") is not None
        ):
            changed = True
            external_parent.rename(moved_parent)
            external_parent.symlink_to(moved_parent, target_is_directory=True)
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(manifest_module.os, "open", change_parent_then_open)

    result = cli_main(
        [
            "replay",
            str(receipt_path),
            "--source-root",
            str(source_root),
            "--output-root",
            str(output),
        ]
    )
    captured = capsys.readouterr()

    assert result == 2
    assert captured.out == ""
    assert captured.err.startswith("ablpc-mod:")
    assert changed
    assert not output.exists()
    assert _tree_snapshot(source_root) == source_before


def test_receipt_replay_accepts_execute_only_parent_directory(tmp_path: Path) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    external_parent = tmp_path / "execute-only"
    external_parent.mkdir()
    receipt_path = external_parent / "receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    output = tmp_path / "replayed"

    external_parent.chmod(0o111)
    try:
        replay_receipt(receipt_path, source_root, output)
    finally:
        external_parent.chmod(0o700)

    assert (output / DESTINATION_PATH).read_bytes() == replacement


@pytest.mark.parametrize(
    ("chain_name", "chain_offset"),
    [
        ("reacquired-first", 0),
        ("reacquired-second", 1),
        ("acquired-first", 0),
        ("acquired-last", -1),
    ],
)
def test_receipt_cleanup_error_attempts_every_descriptor_before_parsing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    chain_name: str,
    chain_offset: int,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    external_parent = tmp_path / "deep/receipt/parent"
    external_parent.mkdir(parents=True)
    receipt_path = external_parent / "receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    output = tmp_path / "replayed"
    source_before = _tree_snapshot(source_root)
    ordinary_before = _tree_snapshot(ordinary)
    descriptor_count = len(receipt_path.absolute().parts)
    chain_start = 0 if chain_name.startswith("reacquired") else descriptor_count
    fail_index = chain_start + (
        descriptor_count if chain_offset == -1 else chain_offset + 1
    )
    real_close = manifest_module.os.close
    close_attempts: list[int] = []

    def close_then_fail(descriptor: int) -> None:
        close_attempts.append(descriptor)
        real_close(descriptor)
        if len(close_attempts) == fail_index:
            raise OSError(errno.EIO, f"injected {chain_name} close failure")

    def parsing_must_not_begin(*args: object, **kwargs: object) -> object:
        raise AssertionError("receipt parsing began after cleanup failure")

    before_descriptors = _open_descriptor_count()
    monkeypatch.setattr(manifest_module.os, "close", close_then_fail)
    monkeypatch.setattr(manifest_module, "_parse_receipt", parsing_must_not_begin)

    with pytest.raises(ManifestError, match="cannot close receipt input"):
        replay_receipt(receipt_path, source_root, output)

    assert len(close_attempts) == descriptor_count * 2
    assert len(set(close_attempts)) == descriptor_count * 2
    assert _open_descriptor_count() == before_descriptors
    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(ordinary) == ordinary_before
    assert not output.exists()


def test_receipt_partial_acquisition_cleanup_preserves_primary_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    external_parent = tmp_path / "deep/receipt/parent"
    external_parent.mkdir(parents=True)
    receipt_path = external_parent / "receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    output = tmp_path / "replayed"
    source_before = _tree_snapshot(source_root)
    ordinary_before = _tree_snapshot(ordinary)
    descriptor_count = len(receipt_path.absolute().parts)
    real_fstat = manifest_module.os.fstat
    real_close = manifest_module.os.close
    close_attempts: list[int] = []
    primary_raised = False

    def fail_final_file_fstat(descriptor: int) -> os.stat_result:
        nonlocal primary_raised
        result = real_fstat(descriptor)
        if not primary_raised and stat.S_ISREG(result.st_mode):
            primary_raised = True
            raise OSError(errno.EIO, "primary final fstat failure")
        return result

    def first_close_fails(descriptor: int) -> None:
        close_attempts.append(descriptor)
        real_close(descriptor)
        if len(close_attempts) == 1:
            raise OSError(errno.EIO, "secondary cleanup failure")

    before_descriptors = _open_descriptor_count()
    monkeypatch.setattr(manifest_module.os, "fstat", fail_final_file_fstat)
    monkeypatch.setattr(manifest_module.os, "close", first_close_fails)

    with pytest.raises(OSError, match="primary final fstat failure") as captured:
        replay_receipt(receipt_path, source_root, output)

    assert primary_raised
    assert len(close_attempts) == descriptor_count
    assert len(set(close_attempts)) == descriptor_count
    assert any(
        "secondary cleanup failure" in note
        for note in getattr(captured.value, "__notes__", ())
    )
    assert _open_descriptor_count() == before_descriptors
    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(ordinary) == ordinary_before
    assert not output.exists()


def test_receipt_both_chain_cleanup_errors_preserve_body_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    external_parent = tmp_path / "deep/receipt/parent"
    external_parent.mkdir(parents=True)
    receipt_path = external_parent / "receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    output = tmp_path / "replayed"
    source_before = _tree_snapshot(source_root)
    ordinary_before = _tree_snapshot(ordinary)
    descriptor_count = len(receipt_path.absolute().parts)
    real_close = manifest_module.os.close
    close_attempts: list[int] = []

    def fail_first_close_in_each_chain(descriptor: int) -> None:
        close_attempts.append(descriptor)
        real_close(descriptor)
        if len(close_attempts) in (1, descriptor_count + 1):
            raise OSError(errno.EIO, "secondary chain cleanup failure")

    def primary_comparison_failure(*args: object, **kwargs: object) -> bool:
        raise ManifestError("primary receipt comparison failure")

    before_descriptors = _open_descriptor_count()
    monkeypatch.setattr(manifest_module.os, "close", fail_first_close_in_each_chain)
    monkeypatch.setattr(
        manifest_module, "_same_receipt_handle_chain", primary_comparison_failure
    )

    with pytest.raises(ManifestError, match="primary receipt comparison failure") as captured:
        replay_receipt(receipt_path, source_root, output)

    assert len(close_attempts) == descriptor_count * 2
    assert len(set(close_attempts)) == descriptor_count * 2
    assert sum(
        "secondary chain cleanup failure" in note
        for note in getattr(captured.value, "__notes__", ())
    ) == 2
    assert _open_descriptor_count() == before_descriptors
    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(ordinary) == ordinary_before
    assert not output.exists()


def test_cli_receipt_cleanup_error_is_silent_and_closes_every_descriptor(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    apply_manifest(_replacement_manifest(destination, replacement), source_root, ordinary)
    external_parent = tmp_path / "deep/receipt/parent"
    external_parent.mkdir(parents=True)
    receipt_path = external_parent / "receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    output = tmp_path / "replayed"
    source_before = _tree_snapshot(source_root)
    descriptor_count = len(receipt_path.absolute().parts)
    real_close = manifest_module.os.close
    close_attempts: list[int] = []

    def first_close_fails(descriptor: int) -> None:
        close_attempts.append(descriptor)
        real_close(descriptor)
        if len(close_attempts) == 1:
            raise OSError(errno.EIO, "injected CLI cleanup failure")

    before_descriptors = _open_descriptor_count()
    monkeypatch.setattr(manifest_module.os, "close", first_close_fails)
    result = cli_main(
        [
            "replay",
            str(receipt_path),
            "--source-root",
            str(source_root),
            "--output-root",
            str(output),
        ]
    )
    captured = capsys.readouterr()

    assert result == 2
    assert captured.out == ""
    assert "cannot close receipt input" in captured.err
    assert len(close_attempts) == descriptor_count * 2
    assert len(set(close_attempts)) == descriptor_count * 2
    assert _open_descriptor_count() == before_descriptors
    assert _tree_snapshot(source_root) == source_before
    assert not output.exists()


def test_receipt_input_must_be_external_to_source_and_overlay(tmp_path: Path) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = _replacement_manifest(destination, replacement)
    overlay = tmp_path / "overlay"
    receipt = apply_manifest(manifest, source_root, overlay)
    source_receipt = source_root / "receipt.json"
    source_receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    source_before = _tree_snapshot(source_root)
    overlay_before = _tree_snapshot(overlay)

    with pytest.raises(ManifestError, match="outside the source root"):
        replay_receipt(source_receipt, source_root, tmp_path / "output")
    with pytest.raises(ManifestError, match="outside the output root"):
        remove_receipt(overlay / ".ablpc/receipt.json", source_root, overlay)

    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(overlay) == overlay_before


def test_receipt_removal_rejects_external_or_overlay_drift_without_mutation(
    tmp_path: Path,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = _replacement_manifest(destination, replacement)
    overlay = tmp_path / "overlay"
    receipt = apply_manifest(manifest, source_root, overlay)
    valid_receipt_path = tmp_path / "valid-receipt.json"
    valid_receipt_path.write_bytes((overlay / ".ablpc/receipt.json").read_bytes())
    forged = copy.deepcopy(receipt)
    forged["files"][0]["output_sha256"] = "0" * 64
    forged_receipt_path = tmp_path / "forged-receipt.json"
    forged_receipt_path.write_text(
        json.dumps(forged, indent=2) + "\n", encoding="utf-8"
    )
    source_before = _tree_snapshot(source_root)
    overlay_before = _tree_snapshot(overlay)

    with pytest.raises(ManifestError, match="does not match"):
        remove_receipt(forged_receipt_path, source_root, overlay)
    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(overlay) == overlay_before

    (overlay / DESTINATION_PATH).write_bytes(b"changed")
    changed_overlay = _tree_snapshot(overlay)
    with pytest.raises(ManifestError, match="output SHA-256 mismatch"):
        remove_receipt(valid_receipt_path, source_root, overlay)
    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(overlay) == changed_overlay


def test_cli_replays_and_removes_an_exact_receipt_without_manifest(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    ordinary = tmp_path / "ordinary-overlay"
    receipt = apply_manifest(
        _replacement_manifest(destination, replacement), source_root, ordinary
    )
    receipt_path = tmp_path / "external-receipt.json"
    receipt_path.write_bytes((ordinary / ".ablpc/receipt.json").read_bytes())
    replayed = tmp_path / "replayed-overlay"
    source_before = _tree_snapshot(source_root)

    replay_result = cli_main(
        [
            "replay",
            str(receipt_path),
            "--source-root",
            str(source_root),
            "--output-root",
            str(replayed),
        ]
    )
    replay_output = capsys.readouterr()
    assert replay_result == 0
    assert json.loads(replay_output.out) == receipt
    assert replay_output.err == ""

    remove_result = cli_main(
        [
            "remove-receipt",
            str(receipt_path),
            "--source-root",
            str(source_root),
            "--overlay-root",
            str(replayed),
        ]
    )
    remove_output = capsys.readouterr()
    assert remove_result == 0
    assert json.loads(remove_output.out) == receipt
    assert remove_output.err == ""
    assert not replayed.exists()
    assert _tree_snapshot(source_root) == source_before


def test_cli_receipt_failures_have_empty_stdout_and_preserve_trees(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    overlay = tmp_path / "overlay"
    receipt = apply_manifest(
        _replacement_manifest(destination, replacement), source_root, overlay
    )
    forged = copy.deepcopy(receipt)
    forged["files"][0]["output_sha256"] = "0" * 64
    receipt_path = tmp_path / "forged-receipt.json"
    receipt_path.write_text(json.dumps(forged, indent=2) + "\n", encoding="utf-8")
    source_before = _tree_snapshot(source_root)
    overlay_before = _tree_snapshot(overlay)
    replayed = tmp_path / "replayed"

    replay_result = cli_main(
        [
            "replay",
            str(receipt_path),
            "--source-root",
            str(source_root),
            "--output-root",
            str(replayed),
        ]
    )
    replay_output = capsys.readouterr()
    assert replay_result == 2
    assert replay_output.out == ""
    assert replay_output.err.startswith("ablpc-mod:")
    assert not replayed.exists()

    remove_result = cli_main(
        [
            "remove-receipt",
            str(receipt_path),
            "--source-root",
            str(source_root),
            "--overlay-root",
            str(overlay),
        ]
    )
    remove_output = capsys.readouterr()
    assert remove_result == 2
    assert remove_output.out == ""
    assert remove_output.err.startswith("ablpc-mod:")
    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(overlay) == overlay_before


def test_mount_alias_classification_preserves_ordinary_filesystem_mounts() -> None:
    entries = (
        _MountEntry(1, 0, 0, 36, Path("/root"), Path("/"), 1),
        _MountEntry(2, 1, 0, 36, Path("/home"), Path("/home"), 2),
        _MountEntry(3, 1, 0, 53, Path("/"), Path("/tmp"), 3),
        _MountEntry(
            4,
            3,
            0,
            53,
            Path("/pytest/independent parent"),
            Path("/tmp/pytest/alias parent"),
            4,
        ),
        _MountEntry(5, 1, 0, 53, Path("/"), Path("/home/tmp alias"), 5),
        _MountEntry(
            6,
            2,
            0,
            36,
            Path("/home/project"),
            Path("/home/project"),
            6,
        ),
        _MountEntry(
            12,
            8,
            0,
            74,
            Path("/"),
            Path("/tmp/stacked parent"),
            12,
        ),
        _MountEntry(
            7,
            3,
            0,
            53,
            Path("/hidden-independent"),
            Path("/tmp/stacked parent"),
            7,
        ),
        _MountEntry(
            8,
            7,
            0,
            73,
            Path("/middle-covered"),
            Path("/tmp/stacked parent"),
            8,
        ),
        _MountEntry(9, 1, 0, 70, Path("/"), Path("/hidden source"), 9),
        _MountEntry(10, 9, 0, 71, Path("/"), Path("/hidden source"), 10),
        _MountEntry(
            11,
            1,
            0,
            70,
            Path("/ordinary-root"),
            Path("/ordinary"),
            11,
        ),
    )

    assert _mount_alias_points(entries) == frozenset(
        {Path("/tmp/pytest/alias parent"), Path("/home/tmp alias")}
    )


@pytest.mark.parametrize("reverse_entries", [False, True])
def test_mount_alias_classification_uses_explicit_order_after_id_reuse(
    reverse_entries: bool,
) -> None:
    entries = (
        _MountEntry(1, 0, 0, 36, Path("/root"), Path("/"), 1),
        _MountEntry(
            1082,
            1,
            0,
            75,
            Path("/"),
            Path("/independent source"),
            2,
        ),
        _MountEntry(
            1081,
            1,
            0,
            75,
            Path("/"),
            Path("/later alias with reused id"),
            3,
        ),
    )
    if reverse_entries:
        entries = tuple(reversed(entries))

    assert _mount_alias_points(entries) == frozenset(
        {Path("/later alias with reused id")}
    )


@pytest.mark.parametrize(
    "mounted_path",
    ["ancestor", "root", "intermediate", "output", "receipt", "reuse"],
)
def test_remove_rejects_mounted_deletion_plan_paths_without_mutation(
    tmp_path: Path, mounted_path: str
) -> None:
    unshare = shutil.which("unshare")
    mount = shutil.which("mount")
    if unshare is None or mount is None:
        pytest.skip("host does not provide unshare and mount")
    helper = Path(__file__).with_name("mount_overlay_case.py")
    case_root = tmp_path / mounted_path
    result = subprocess.run(
        [
            unshare,
            "--user",
            "--map-root-user",
            "--mount",
            "--fork",
            sys.executable,
            os.fspath(helper),
            mounted_path,
            os.fspath(case_root),
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode == 77:
        pytest.skip(result.stdout.strip() or result.stderr.strip())
    if result.returncode != 0 and result.stderr.startswith("unshare:"):
        pytest.skip(
            "host cannot create a private mount namespace: "
            f"{result.stderr.strip()}"
        )
    assert result.returncode == 0, (
        f"isolated {mounted_path} mount case failed\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_remove_allows_visible_mount_covering_lower_parent_alias(
    tmp_path: Path,
) -> None:
    unshare = shutil.which("unshare")
    mount = shutil.which("mount")
    if unshare is None or mount is None:
        pytest.skip("host does not provide unshare and mount")
    helper = Path(__file__).with_name("mount_overlay_case.py")
    case_root = tmp_path / "stacked"
    result = subprocess.run(
        [
            unshare,
            "--user",
            "--map-root-user",
            "--mount",
            "--fork",
            sys.executable,
            os.fspath(helper),
            "stacked",
            os.fspath(case_root),
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode == 77:
        pytest.skip(result.stdout.strip() or result.stderr.strip())
    if result.returncode != 0 and result.stderr.startswith("unshare:"):
        pytest.skip(
            "host cannot create a private mount namespace: "
            f"{result.stderr.strip()}"
        )
    assert result.returncode == 0, (
        "isolated stacked mount case failed\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


@pytest.mark.parametrize("change", ["changed", "missing"])
def test_remove_rejects_changed_or_missing_output_without_deleting_anything(
    tmp_path: Path, change: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    overlay = tmp_path / "overlay"
    apply_manifest(manifest, source_root, overlay)
    output = overlay / DESTINATION_PATH
    if change == "changed":
        output.write_bytes(b"changed output")
        match = "output SHA-256 mismatch"
    else:
        output.unlink()
        match = "file is missing"
    overlay_before = _tree_snapshot(overlay)
    source_before = _tree_snapshot(source_root)

    with pytest.raises(ManifestError, match=match):
        remove_manifest(manifest, source_root, overlay)

    assert _tree_snapshot(overlay) == overlay_before
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize("kind", ["symlink", "fifo"])
def test_remove_rejects_non_regular_recorded_output_without_deletion(
    tmp_path: Path, kind: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    overlay = tmp_path / "overlay"
    apply_manifest(manifest, source_root, overlay)
    output = overlay / DESTINATION_PATH
    output.unlink()
    if kind == "symlink":
        outside = tmp_path / "outside.bin"
        outside.write_bytes(replacement)
        output.symlink_to(outside)
        match = "destination is a symlink"
    else:
        os.mkfifo(output)
        match = "destination is not a regular file"
    overlay_before = _tree_snapshot(overlay)
    source_before = _tree_snapshot(source_root)

    with pytest.raises(ManifestError, match=match):
        remove_manifest(manifest, source_root, overlay)

    assert _tree_snapshot(overlay) == overlay_before
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize("change", ["missing", "symlink", "fifo"])
def test_remove_rejects_missing_or_non_regular_receipt_without_deletion(
    tmp_path: Path, change: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    overlay = tmp_path / "overlay"
    apply_manifest(manifest, source_root, overlay)
    receipt_path = overlay / ".ablpc/receipt.json"
    receipt_path.unlink()
    if change == "missing":
        match = "file is missing"
    elif change == "symlink":
        outside = tmp_path / "outside-receipt.json"
        outside.write_bytes(b"{}")
        receipt_path.symlink_to(outside)
        match = "destination is a symlink"
    else:
        os.mkfifo(receipt_path)
        match = "destination is not a regular file"
    overlay_before = _tree_snapshot(overlay)
    source_before = _tree_snapshot(source_root)

    with pytest.raises(ManifestError, match=match):
        remove_manifest(manifest, source_root, overlay)

    assert _tree_snapshot(overlay) == overlay_before
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize("target", ["output", "receipt"])
def test_remove_rejects_hard_linked_recorded_files_without_deletion(
    tmp_path: Path, target: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    overlay = tmp_path / "overlay"
    apply_manifest(manifest, source_root, overlay)
    linked = (
        overlay / DESTINATION_PATH
        if target == "output"
        else overlay / ".ablpc/receipt.json"
    )
    outside = tmp_path / f"outside-{target}"
    os.link(linked, outside)
    overlay_before = _tree_snapshot(overlay)
    source_before = _tree_snapshot(source_root)
    outside_before = _tree_snapshot(outside)

    with pytest.raises(ManifestError, match="file has multiple hard links"):
        remove_manifest(manifest, source_root, overlay)

    assert _tree_snapshot(overlay) == overlay_before
    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(outside) == outside_before


@pytest.mark.parametrize("source_change", ["destination", "replacement"])
def test_remove_rejects_source_drift_before_deleting_the_overlay(
    tmp_path: Path, source_change: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    overlay = tmp_path / "overlay"
    apply_manifest(manifest, source_root, overlay)
    changed_path = source_root / (
        DESTINATION_PATH if source_change == "destination" else SOURCE_PATH
    )
    changed_path.write_bytes(b"changed source")
    overlay_before = _tree_snapshot(overlay)
    source_before = _tree_snapshot(source_root)

    with pytest.raises(ManifestError, match="SHA-256 mismatch"):
        remove_manifest(manifest, source_root, overlay)

    assert _tree_snapshot(overlay) == overlay_before
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize("kind", ["file", "directory", "symlink", "fifo"])
def test_remove_rejects_every_extra_overlay_entry_without_deletion(
    tmp_path: Path, kind: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    overlay = tmp_path / "overlay"
    apply_manifest(manifest, source_root, overlay)
    extra = overlay / "EXTRA"
    if kind == "file":
        extra.write_bytes(b"extra")
    elif kind == "directory":
        extra.mkdir()
    elif kind == "symlink":
        outside = tmp_path / "outside"
        outside.write_bytes(b"outside")
        extra.symlink_to(outside)
    else:
        os.mkfifo(extra)
    overlay_before = _tree_snapshot(overlay)
    source_before = _tree_snapshot(source_root)

    with pytest.raises(ManifestError, match="contains extra content"):
        remove_manifest(manifest, source_root, overlay)

    assert _tree_snapshot(overlay) == overlay_before
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize(
    "mismatch",
    ["schema", "name", "path", "edit", "input-hash", "output-hash", "extra"],
)
def test_remove_rejects_every_receipt_metadata_mismatch_without_deletion(
    tmp_path: Path, mismatch: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    overlay = tmp_path / "overlay"
    apply_manifest(manifest, source_root, overlay)
    receipt_path = overlay / ".ablpc/receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if mismatch == "schema":
        receipt["schema_version"] = 1
    elif mismatch == "name":
        receipt["manifest_name"] = "forged-name"
    elif mismatch == "path":
        receipt["files"][0]["path"] = "CD/FORGED.BIN"
    elif mismatch == "edit":
        receipt["files"][0]["edits"][0]["source_path"] = "CD/FORGED.BIN"
    elif mismatch == "input-hash":
        receipt["files"][0]["input_sha256"] = "0" * 64
    elif mismatch == "output-hash":
        receipt["files"][0]["output_sha256"] = "0" * 64
    else:
        receipt["unexpected"] = True
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    overlay_before = _tree_snapshot(overlay)
    source_before = _tree_snapshot(source_root)

    with pytest.raises(ManifestError, match="receipt does not match"):
        remove_manifest(manifest, source_root, overlay)

    assert _tree_snapshot(overlay) == overlay_before
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize("receipt_change", ["malformed", "duplicate", "reformatted"])
def test_remove_strictly_parses_the_ordinary_receipt_without_deletion(
    tmp_path: Path, receipt_change: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    overlay = tmp_path / "overlay"
    receipt = apply_manifest(manifest, source_root, overlay)
    receipt_path = overlay / ".ablpc/receipt.json"
    if receipt_change == "malformed":
        receipt_path.write_bytes(b"{")
        match = "cannot parse overlay receipt"
    elif receipt_change == "duplicate":
        receipt_path.write_text(
            json.dumps(
                {
                    "schema_version": receipt["schema_version"],
                    "manifest_name": receipt["manifest_name"],
                    "files": receipt["files"],
                }
            ).replace(
                '{"schema_version": 2,',
                '{"schema_version": 2, "schema_version": 2,',
                1,
            ),
            encoding="utf-8",
        )
        match = "duplicate key"
    else:
        receipt_path.write_text(json.dumps(receipt, sort_keys=True), encoding="utf-8")
        match = "receipt encoding does not match"
    overlay_before = _tree_snapshot(overlay)
    source_before = _tree_snapshot(source_root)

    with pytest.raises(ManifestError, match=match):
        remove_manifest(manifest, source_root, overlay)

    assert _tree_snapshot(overlay) == overlay_before
    assert _tree_snapshot(source_root) == source_before


def test_remove_refuses_a_staged_tree_as_extra_content_without_deletion(
    tmp_path: Path,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    _write_source_file(source_root, "unchanged.txt", b"unchanged")
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    staged = tmp_path / "staged"
    stage_manifest(manifest, source_root, staged)
    staged_before = _tree_snapshot(staged)
    source_before = _tree_snapshot(source_root)

    with pytest.raises(ManifestError, match="contains extra content"):
        remove_manifest(manifest, source_root, staged)

    assert _tree_snapshot(staged) == staged_before
    assert _tree_snapshot(source_root) == source_before


def test_restore_exact_staged_tree_to_clean_source_content(tmp_path: Path) -> None:
    destination = b"destination"
    replacement = b"replacement with a different size"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    _write_source_file(source_root, "bugs.exe", b"synthetic executable")
    _write_source_file(source_root, "UNRELATED/keep.bin", b"keep")
    manifest = _replacement_manifest(destination, replacement)
    source_before = _tree_snapshot(source_root)
    staged = tmp_path / "staged"
    receipt = stage_manifest(manifest, source_root, staged)

    assert (staged / DESTINATION_PATH).read_bytes() == replacement
    assert restore_manifest(manifest, source_root, staged) == receipt

    assert _tree_snapshot(staged) == source_before
    assert _tree_snapshot(source_root) == source_before
    assert not (staged / ".ablpc").exists()


@pytest.mark.parametrize("schema_version", [1, 2])
@pytest.mark.parametrize(
    "edit",
    [
        {
            "operation": "set-scene-record-position",
            "section": "primary",
            "index": 0,
            "position": [111, 222, 333],
        },
        {
            "operation": "set-scene-record-field-0c",
            "section": "primary",
            "index": 0,
            "expected_value": 0x123,
            "value": 0,
        },
        {
            "operation": "set-scene-record-payload-target-offset",
            "section": "primary",
            "index": 0,
            "expected_target_offset": 0x240,
            "target_offset": 0x248,
        },
    ],
)
def test_restore_accepts_every_level_operation_under_schemas_one_and_two(
    tmp_path: Path, schema_version: int, edit: dict[str, object]
) -> None:
    source = _synthetic_dat_with_payload_target()
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, "CD/LEVEL07/LEVEL1.DAT", source)
    _write_source_file(source_root, "bugs.exe", b"synthetic executable")
    manifest = _level_manifest(
        source,
        f"restore-schema-{schema_version}-{edit['operation']}",
        [edit],
        schema_version=schema_version,
    )
    source_before = _tree_snapshot(source_root)
    staged = tmp_path / "staged"
    receipt = stage_manifest(manifest, source_root, staged)

    assert restore_manifest(manifest, source_root, staged) == receipt
    assert _tree_snapshot(staged) == source_before
    assert _tree_snapshot(source_root) == source_before


def test_restore_accepts_multi_file_and_composed_staged_trees(tmp_path: Path) -> None:
    destination_one = b"destination one"
    replacement_one = b"replacement one"
    destination_two = b"destination two"
    replacement_two = b"replacement two"
    source_root = tmp_path / "work-copy"
    _write_source_file(source_root, "A/one.bin", destination_one)
    _write_source_file(source_root, "SOURCE/one.bin", replacement_one)
    _write_source_file(source_root, "B/deep/two.bin", destination_two)
    _write_source_file(source_root, "SOURCE/two.bin", replacement_two)
    _write_source_file(source_root, "bugs.exe", b"synthetic executable")
    multi = _replacement_manifest(
        destination_one,
        replacement_one,
        destination_path="A/one.bin",
        source_path="SOURCE/one.bin",
    )
    _append_replacement(
        multi,
        destination_two,
        replacement_two,
        destination_path="B/deep/two.bin",
        source_path="SOURCE/two.bin",
    )
    source_before = _tree_snapshot(source_root)
    staged = tmp_path / "multi-staged"
    receipt = stage_manifest(multi, source_root, staged)
    assert restore_manifest(multi, source_root, staged) == receipt
    assert _tree_snapshot(staged) == source_before

    level = _synthetic_dat()
    level_root = tmp_path / "level-work-copy"
    _write_source_file(level_root, "CD/LEVEL07/LEVEL1.DAT", level)
    _write_source_file(level_root, "bugs.exe", b"synthetic executable")
    left = _level_manifest(
        level,
        "restore-left",
        [{
            "operation": "set-scene-record-position",
            "section": "primary",
            "index": 0,
            "position": [111, 222, 333],
        }],
    )
    right = _level_manifest(
        level,
        "restore-right",
        [{
            "operation": "set-scene-record-field-0c",
            "section": "primary",
            "index": 0,
            "expected_value": 0x123,
            "value": 0,
        }],
    )
    composed = compose_manifests(left, right, level_root)
    level_before = _tree_snapshot(level_root)
    composed_staged = tmp_path / "composed-staged"
    composed_receipt = stage_manifest(composed, level_root, composed_staged)
    assert (
        restore_manifest(composed, level_root, composed_staged)
        == composed_receipt
    )
    assert _tree_snapshot(composed_staged) == level_before


@pytest.mark.parametrize(
    "change", ["extra", "missing", "changed", "symlink", "fifo", "hardlink"]
)
def test_restore_rejects_unrelated_tree_drift_before_mutation(
    tmp_path: Path, change: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    _write_source_file(source_root, "UNRELATED/keep.bin", b"keep")
    manifest = _replacement_manifest(destination, replacement)
    staged = tmp_path / "staged"
    stage_manifest(manifest, source_root, staged)
    target = staged / "UNRELATED/keep.bin"
    if change == "extra":
        _write_source_file(staged, "UNRELATED/extra.bin", b"extra")
    elif change == "missing":
        target.unlink()
    elif change == "changed":
        target.write_bytes(b"changed")
    elif change == "symlink":
        target.unlink()
        target.symlink_to(staged / DESTINATION_PATH)
    elif change == "fifo":
        target.unlink()
        os.mkfifo(target)
    else:
        target.unlink()
        os.link(staged / SOURCE_PATH, target)
    source_before = _tree_snapshot(source_root)
    staged_before = _tree_snapshot(staged)

    with pytest.raises(ManifestError):
        restore_manifest(manifest, source_root, staged)

    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(staged) == staged_before


@pytest.mark.parametrize("authority", ["source", "manifest", "output", "receipt"])
def test_restore_rejects_authority_drift_before_mutation(
    tmp_path: Path, authority: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    _write_source_file(source_root, "UNRELATED/keep.bin", b"keep")
    manifest = _replacement_manifest(destination, replacement)
    staged = tmp_path / "staged"
    stage_manifest(manifest, source_root, staged)
    supplied = copy.deepcopy(manifest)
    if authority == "source":
        (source_root / DESTINATION_PATH).write_bytes(b"changed source")
    elif authority == "manifest":
        supplied["name"] = "different-manifest-name"
    elif authority == "output":
        (staged / DESTINATION_PATH).write_bytes(b"changed output")
    else:
        receipt_path = staged / ".ablpc/receipt.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["manifest_name"] = "changed-receipt"
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    source_before = _tree_snapshot(source_root)
    staged_before = _tree_snapshot(staged)

    with pytest.raises(ManifestError):
        restore_manifest(supplied, source_root, staged)

    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(staged) == staged_before


def test_restore_rejects_reserved_source_metadata_before_mutation(
    tmp_path: Path,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = _replacement_manifest(destination, replacement)
    staged = tmp_path / "staged"
    stage_manifest(manifest, source_root, staged)
    _write_source_file(source_root, ".ABLPC/prior.txt", b"reserved")
    source_before = _tree_snapshot(source_root)
    staged_before = _tree_snapshot(staged)

    with pytest.raises(ManifestError, match="reserved .ablpc"):
        restore_manifest(manifest, source_root, staged)

    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(staged) == staged_before


@pytest.mark.parametrize(
    ("collision_kind", "first_path", "second_path"),
    [
        ("file-file", "UNRELATED/Case.bin", "UNRELATED/case.bin"),
        (
            "directory-directory",
            "UNRELATED/Dir/one.bin",
            "UNRELATED/dir/two.bin",
        ),
        ("file-directory", "UNRELATED/Node", "UNRELATED/node/inside.bin"),
        (
            "nested-ancestor",
            "UNRELATED/Parent/Leaf.bin",
            "UNRELATED/parent/leaf.bin",
        ),
    ],
)
def test_restore_rejects_case_insensitive_source_tree_collisions_before_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    collision_kind: str,
    first_path: str,
    second_path: str,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    _write_source_file(source_root, first_path, b"first")
    _write_source_file(source_root, second_path, b"second")
    manifest = _replacement_manifest(destination, replacement)
    staged = tmp_path / f"staged-{collision_kind}"
    stage_manifest(manifest, source_root, staged)
    source_before = _tree_snapshot(source_root)
    staged_before = _tree_snapshot(staged)

    def unexpected(*args: object, **kwargs: object) -> None:
        pytest.fail(f"restoration advanced past source collision preflight: {args!r}")

    monkeypatch.setattr(
        manifest_module, "_validate_unmounted_restoration_plan", unexpected
    )
    monkeypatch.setattr(manifest_module, "_prepare_manifest", unexpected)
    monkeypatch.setattr(manifest_module, "_read_stable_tree_file", unexpected)
    monkeypatch.setattr(manifest_module, "_atomic_write", unexpected)
    monkeypatch.setattr(Path, "unlink", unexpected)

    with pytest.raises(ManifestError, match="case-insensitive duplicate paths"):
        restore_manifest(manifest, source_root, staged)

    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(staged) == staged_before


@pytest.mark.parametrize(
    ("collision_kind", "first_path", "second_path"),
    [
        ("file-file", "UNRELATED/Case.bin", "UNRELATED/case.bin"),
        (
            "directory-directory",
            "UNRELATED/Dir/one.bin",
            "UNRELATED/dir/two.bin",
        ),
        ("file-directory", "UNRELATED/Node", "UNRELATED/node/inside.bin"),
        (
            "nested-ancestor",
            "UNRELATED/Parent/Leaf.bin",
            "UNRELATED/parent/leaf.bin",
        ),
    ],
)
def test_restore_rejects_case_insensitive_staged_tree_collisions_before_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    collision_kind: str,
    first_path: str,
    second_path: str,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    _write_source_file(source_root, first_path, b"first")
    manifest = _replacement_manifest(destination, replacement)
    staged = tmp_path / f"staged-{collision_kind}"
    stage_manifest(manifest, source_root, staged)
    _write_source_file(staged, second_path, b"second")
    source_before = _tree_snapshot(source_root)
    staged_before = _tree_snapshot(staged)

    def unexpected(*args: object, **kwargs: object) -> None:
        pytest.fail(f"restoration mutated or read content after collision: {args!r}")

    monkeypatch.setattr(manifest_module, "_read_stable_tree_file", unexpected)
    monkeypatch.setattr(manifest_module, "_atomic_write", unexpected)
    monkeypatch.setattr(Path, "unlink", unexpected)

    with pytest.raises(ManifestError, match="case-insensitive duplicate paths"):
        restore_manifest(manifest, source_root, staged)

    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(staged) == staged_before


@pytest.mark.parametrize("tree", ["source", "staged"])
def test_restore_rejects_case_colliding_directories_before_descending(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    tree: str,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    _write_source_file(source_root, "UNRELATED/lower/one.bin", b"one")
    manifest = _replacement_manifest(destination, replacement)
    staged = tmp_path / f"staged-{tree}"
    stage_manifest(manifest, source_root, staged)
    collision_root = source_root if tree == "source" else staged
    _write_source_file(collision_root, "UNRELATED/LOWER/two.bin", b"two")
    source_before = _tree_snapshot(source_root)
    staged_before = _tree_snapshot(staged)
    original_scandir = os.scandir
    visited: list[Path] = []

    def recording_scandir(path: os.PathLike[str] | str):
        visited.append(Path(path))
        return original_scandir(path)

    monkeypatch.setattr(manifest_module.os, "scandir", recording_scandir)

    with pytest.raises(ManifestError, match="case-insensitive duplicate paths"):
        restore_manifest(manifest, source_root, staged)

    assert collision_root / "UNRELATED/LOWER" not in visited
    assert collision_root / "UNRELATED/lower" not in visited
    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(staged) == staged_before


@pytest.mark.parametrize("kind", ["symlink", "fifo", "hardlink"])
def test_restore_rejects_nonordinary_source_tree_before_mutation(
    tmp_path: Path, kind: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    _write_source_file(source_root, "UNRELATED/keep.bin", b"keep")
    manifest = _replacement_manifest(destination, replacement)
    staged = tmp_path / "staged"
    stage_manifest(manifest, source_root, staged)
    target = source_root / "UNRELATED/keep.bin"
    target.unlink()
    if kind == "symlink":
        target.symlink_to(source_root / SOURCE_PATH)
    elif kind == "fifo":
        os.mkfifo(target)
    else:
        os.link(source_root / SOURCE_PATH, target)
    source_before = _tree_snapshot(source_root)
    staged_before = _tree_snapshot(staged)

    with pytest.raises(ManifestError):
        restore_manifest(manifest, source_root, staged)

    assert _tree_snapshot(source_root) == source_before
    assert _tree_snapshot(staged) == staged_before


def test_restore_cli_success_and_failure_silence(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    _write_source_file(source_root, "bugs.exe", b"synthetic executable")
    manifest_path = _write_json(
        tmp_path / "replacement.json",
        _replacement_manifest(destination, replacement),
    )
    manifest = load_manifest(manifest_path)
    source_before = _tree_snapshot(source_root)
    staged = tmp_path / "staged"
    receipt = stage_manifest(manifest, source_root, staged)

    assert cli_main([
        "restore",
        str(manifest_path),
        "--source-root",
        str(source_root),
        "--game-root",
        str(staged),
    ]) == 0
    assert json.loads(capsys.readouterr().out) == receipt
    assert _tree_snapshot(staged) == source_before

    rejected = tmp_path / "rejected"
    stage_manifest(manifest, source_root, rejected)
    _write_source_file(rejected, "extra.bin", b"extra")
    rejected_before = _tree_snapshot(rejected)
    assert cli_main([
        "restore",
        str(manifest_path),
        "--source-root",
        str(source_root),
        "--game-root",
        str(rejected),
    ]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("ablpc-mod:")
    assert _tree_snapshot(rejected) == rejected_before
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize(
    "mounted_path",
    ["restore-root", "restore-output", "restore-receipt", "restore-unrelated"],
)
def test_restore_rejects_mounted_complete_tree_paths_without_mutation(
    tmp_path: Path, mounted_path: str
) -> None:
    unshare = shutil.which("unshare")
    mount = shutil.which("mount")
    if unshare is None or mount is None:
        pytest.skip("host does not provide unshare and mount")
    helper = Path(__file__).with_name("mount_overlay_case.py")
    case_root = tmp_path / mounted_path
    result = subprocess.run(
        [
            unshare,
            "--user",
            "--map-root-user",
            "--mount",
            "--fork",
            sys.executable,
            os.fspath(helper),
            mounted_path,
            os.fspath(case_root),
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode == 77:
        pytest.skip(result.stdout.strip() or result.stderr.strip())
    if result.returncode != 0 and result.stderr.startswith("unshare:"):
        pytest.skip(
            "host cannot create a private mount namespace: "
            f"{result.stderr.strip()}"
        )
    assert result.returncode == 0, (
        f"isolated {mounted_path} restoration case failed\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def test_remove_rejects_symlinked_or_protected_overlay_roots_without_deletion(
    tmp_path: Path,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    overlay = tmp_path / "overlay"
    apply_manifest(manifest, source_root, overlay)
    overlay_before = _tree_snapshot(overlay)
    alias = tmp_path / "overlay-alias"
    alias.symlink_to(overlay, target_is_directory=True)

    with pytest.raises(ManifestError, match="output root path contains a symlink"):
        remove_manifest(manifest, source_root, alias)
    assert _tree_snapshot(overlay) == overlay_before

    protected = tmp_path / "originals" / "overlay"
    protected.parent.mkdir()
    overlay.rename(protected)
    protected_before = _tree_snapshot(protected)
    with pytest.raises(ManifestError, match="protected content"):
        remove_manifest(manifest, source_root, protected)
    assert _tree_snapshot(protected) == protected_before


def test_cli_removes_an_exact_sparse_overlay(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest_path = _write_json(
        tmp_path / "replacement.json",
        _replacement_manifest(destination, replacement),
    )
    manifest = load_manifest(manifest_path)
    overlay = tmp_path / "overlay"
    receipt = apply_manifest(manifest, source_root, overlay)
    source_before = _tree_snapshot(source_root)

    result = cli_main(
        [
            "remove",
            str(manifest_path),
            "--source-root",
            str(source_root),
            "--overlay-root",
            str(overlay),
        ]
    )

    assert result == 0
    assert json.loads(capsys.readouterr().out) == receipt
    assert not overlay.exists()
    assert _tree_snapshot(source_root) == source_before


@pytest.mark.parametrize("bad_hash", ["destination", "replacement"])
def test_whole_file_replacement_hash_mismatch_fails_before_output(
    tmp_path: Path, bad_hash: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    value = _replacement_manifest(destination, replacement)
    file_entry = value["files"][0]
    if bad_hash == "destination":
        file_entry["sha256"] = "0" * 64
    else:
        file_entry["edits"][0]["source_sha256"] = "0" * 64
    manifest = load_manifest(_write_json(tmp_path / "bad.json", value))
    output = tmp_path / "overlay"

    with pytest.raises(ManifestError, match="SHA-256 mismatch"):
        apply_manifest(manifest, source_root, output)

    assert not output.exists()
    assert (source_root / DESTINATION_PATH).read_bytes() == destination
    assert (source_root / SOURCE_PATH).read_bytes() == replacement


@pytest.mark.parametrize(
    "unsafe_path",
    [
        "../escape.ALL",
        "CD/../escape.ALL",
        "CD\\escape.ALL",
        "C:/escape.ALL",
        "CD//escape.ALL",
        ".ablpc/receipt.json",
        "CD/bad?.ALL",
        "CD/trailing./file.ALL",
    ],
)
def test_whole_file_replacement_rejects_unsafe_target_and_source_paths(
    tmp_path: Path, unsafe_path: str
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    target_value = _replacement_manifest(
        destination, replacement, destination_path=unsafe_path
    )
    with pytest.raises(ManifestError, match="unsafe manifest path"):
        load_manifest(_write_json(tmp_path / "unsafe-target.json", target_value))

    source_value = _replacement_manifest(
        destination, replacement, source_path=unsafe_path
    )
    with pytest.raises(ManifestError, match="unsafe manifest path"):
        load_manifest(_write_json(tmp_path / "unsafe-source.json", source_value))


def test_whole_file_replacement_rejects_symlink_escape(tmp_path: Path) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    destination_file = source_root / DESTINATION_PATH
    destination_file.parent.mkdir(parents=True)
    destination_file.write_bytes(destination)
    outside = tmp_path / "outside.ALL"
    outside.write_bytes(replacement)
    replacement_file = source_root / SOURCE_PATH
    replacement_file.parent.mkdir(parents=True)
    replacement_file.symlink_to(outside)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )

    with pytest.raises(ManifestError, match="escapes source root"):
        apply_manifest(manifest, source_root, tmp_path / "overlay")


def test_manifest_rejects_lexical_protected_root_through_symlink(tmp_path: Path) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    protected_alias = tmp_path / "originals" / "alias"
    protected_alias.parent.mkdir()
    protected_alias.symlink_to(source_root)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )

    with pytest.raises(ManifestError, match="protected content"):
        apply_manifest(manifest, protected_alias, tmp_path / "overlay")


def test_whole_file_replacement_rejects_same_windows_path(tmp_path: Path) -> None:
    value = _replacement_manifest(
        b"destination", b"replacement", source_path="cd/chars/flick.all"
    )
    with pytest.raises(ManifestError, match="same path"):
        load_manifest(_write_json(tmp_path / "same-path.json", value))


def test_whole_file_replacement_rejects_source_destination_collision(
    tmp_path: Path,
) -> None:
    value = _replacement_manifest(
        b"a", b"b", destination_path="CD/A.ALL", source_path="CD/B.ALL"
    )
    value["files"].append(
        {
            "path": "cd/b.all",
            "sha256": _sha256(b"b"),
            "format": "opaque-file-v0",
            "edits": [
                {
                    "operation": "replace-whole-file",
                    "source_path": "CD/C.ALL",
                    "source_sha256": _sha256(b"c"),
                }
            ],
        }
    )

    with pytest.raises(ManifestError, match="collides with a manifest destination"):
        load_manifest(_write_json(tmp_path / "collision.json", value))


def test_manifest_preflights_all_hashes_before_writing_any_file(tmp_path: Path) -> None:
    destination_a = b"destination a"
    replacement_a = b"replacement a"
    destination_b = b"destination b"
    replacement_b = b"replacement b"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination_a, replacement_a)
    (source_root / "CD/SECOND/DEST.ALL").parent.mkdir(parents=True)
    (source_root / "CD/SECOND/DEST.ALL").write_bytes(destination_b)
    (source_root / "CD/SECOND/SOURCE.ALL").write_bytes(replacement_b)
    value = _replacement_manifest(destination_a, replacement_a)
    value["files"].append(
        {
            "path": "CD/SECOND/DEST.ALL",
            "sha256": _sha256(destination_b),
            "format": "opaque-file-v0",
            "edits": [
                {
                    "operation": "replace-whole-file",
                    "source_path": "CD/SECOND/SOURCE.ALL",
                    "source_sha256": "0" * 64,
                }
            ],
        }
    )
    manifest = load_manifest(_write_json(tmp_path / "late-mismatch.json", value))
    output = tmp_path / "overlay"

    with pytest.raises(ManifestError, match="replacement SHA-256 mismatch"):
        apply_manifest(manifest, source_root, output)

    assert not output.exists()


def test_apply_preflights_receipt_symlink_before_any_output(tmp_path: Path) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    output = tmp_path / "overlay"
    outside = tmp_path / "outside"
    output.mkdir()
    outside.mkdir()
    (output / ".ablpc").symlink_to(outside, target_is_directory=True)

    with pytest.raises(ManifestError, match="output ancestor is a symlink"):
        apply_manifest(manifest, source_root, output)

    assert not (output / DESTINATION_PATH).exists()
    assert not (outside / "receipt.json").exists()


def test_apply_rejects_symlinked_output_root_before_any_output(tmp_path: Path) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    real_output = tmp_path / "real-output"
    real_output.mkdir()
    output_alias = tmp_path / "output-alias"
    output_alias.symlink_to(real_output, target_is_directory=True)
    output_through_dotdot = tmp_path / "missing-component" / ".." / "output-alias"

    with pytest.raises(ManifestError, match="output root path contains a symlink"):
        apply_manifest(manifest, source_root, output_through_dotdot)

    assert not (real_output / DESTINATION_PATH).exists()
    assert not (real_output / ".ablpc/receipt.json").exists()


def test_apply_preflights_later_parent_blocker_before_any_output(
    tmp_path: Path,
) -> None:
    destination_a = b"destination a"
    replacement_a = b"replacement a"
    destination_b = b"destination b"
    replacement_b = b"replacement b"
    source_root = tmp_path / "work-copy"
    for relative, data in (
        ("A/one.bin", destination_a),
        ("SOURCE/one.bin", replacement_a),
        ("B/two.bin", destination_b),
        ("SOURCE/two.bin", replacement_b),
    ):
        _write_source_file(source_root, relative, data)
    value = _replacement_manifest(
        destination_a,
        replacement_a,
        destination_path="A/one.bin",
        source_path="SOURCE/one.bin",
    )
    _append_replacement(
        value,
        destination_b,
        replacement_b,
        destination_path="B/two.bin",
        source_path="SOURCE/two.bin",
    )
    manifest = load_manifest(_write_json(tmp_path / "two-files.json", value))
    output = tmp_path / "overlay"
    output.mkdir()
    (output / "B").write_bytes(b"parent blocker")

    with pytest.raises(ManifestError, match="ancestor is not a directory"):
        apply_manifest(manifest, source_root, output)

    assert not (output / "A/one.bin").exists()
    assert (output / "B").read_bytes() == b"parent blocker"
    assert not (output / ".ablpc/receipt.json").exists()


def test_apply_force_rejects_later_directory_before_any_output(
    tmp_path: Path,
) -> None:
    destination_a = b"destination a"
    replacement_a = b"replacement a"
    destination_b = b"destination b"
    replacement_b = b"replacement b"
    source_root = tmp_path / "work-copy"
    for relative, data in (
        ("A/one.bin", destination_a),
        ("SOURCE/one.bin", replacement_a),
        ("B/two.bin", destination_b),
        ("SOURCE/two.bin", replacement_b),
    ):
        _write_source_file(source_root, relative, data)
    value = _replacement_manifest(
        destination_a,
        replacement_a,
        destination_path="A/one.bin",
        source_path="SOURCE/one.bin",
    )
    _append_replacement(
        value,
        destination_b,
        replacement_b,
        destination_path="B/two.bin",
        source_path="SOURCE/two.bin",
    )
    manifest = load_manifest(_write_json(tmp_path / "two-files.json", value))
    output = tmp_path / "overlay"
    (output / "B/two.bin").mkdir(parents=True)

    with pytest.raises(ManifestError, match="destination is not a regular file"):
        apply_manifest(manifest, source_root, output, force=True)

    assert not (output / "A/one.bin").exists()
    assert (output / "B/two.bin").is_dir()
    assert not (output / ".ablpc/receipt.json").exists()


def test_apply_force_rejects_symlink_destination_before_output(tmp_path: Path) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    output = tmp_path / "overlay"
    outside = tmp_path / "outside.ALL"
    outside.write_bytes(b"outside")
    destination_link = output / DESTINATION_PATH
    destination_link.parent.mkdir(parents=True)
    destination_link.symlink_to(outside)

    with pytest.raises(ManifestError, match="destination is a symlink"):
        apply_manifest(manifest, source_root, output, force=True)

    assert outside.read_bytes() == b"outside"
    assert not (output / ".ablpc/receipt.json").exists()


def test_apply_force_replaces_existing_regular_file(tmp_path: Path) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    output = tmp_path / "overlay"
    existing = output / DESTINATION_PATH
    existing.parent.mkdir(parents=True)
    existing.write_bytes(b"prior output")

    apply_manifest(manifest, source_root, output, force=True)

    assert existing.read_bytes() == replacement
    assert (output / ".ablpc/receipt.json").is_file()


def test_stage_preflights_receipt_parent_blocker_before_copy(tmp_path: Path) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    (source_root / ".ablpc").write_bytes(b"receipt parent blocker")
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    staged = tmp_path / "staged"

    with pytest.raises(ManifestError, match="ancestor is not a directory"):
        stage_manifest(manifest, source_root, staged)

    assert not staged.exists()
    assert (source_root / DESTINATION_PATH).read_bytes() == destination
    assert (source_root / ".ablpc").read_bytes() == b"receipt parent blocker"


def test_whole_file_replacement_stages_full_tree_and_preserves_source(
    tmp_path: Path,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    (source_root / "unchanged.txt").write_text("unchanged", encoding="utf-8")
    manifest = load_manifest(
        _write_json(
            tmp_path / "replacement.json",
            _replacement_manifest(destination, replacement),
        )
    )
    staged = tmp_path / "staged"

    receipt = stage_manifest(manifest, source_root, staged)

    assert (staged / DESTINATION_PATH).read_bytes() == replacement
    assert (staged / SOURCE_PATH).read_bytes() == replacement
    assert (staged / "unchanged.txt").read_text(encoding="utf-8") == "unchanged"
    assert (source_root / DESTINATION_PATH).read_bytes() == destination
    assert receipt["files"][0]["input_sha256"] == _sha256(destination)
    assert receipt["files"][0]["edits"][0]["replacement_sha256"] == _sha256(
        replacement
    )


def test_schema_two_can_mix_existing_level_edit_and_whole_file_replacement(
    tmp_path: Path,
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    level_bytes = _synthetic_dat()
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    level_path = source_root / "CD/LEVEL07/LEVEL1.DAT"
    level_path.parent.mkdir(parents=True)
    level_path.write_bytes(level_bytes)
    value = _replacement_manifest(destination, replacement)
    value["files"].append(
        {
            "path": "CD/LEVEL07/LEVEL1.DAT",
            "sha256": _sha256(level_bytes),
            "format": "pc-level-dat-prefix-v0",
            "edits": [
                {
                    "operation": "set-scene-record-position",
                    "section": "primary",
                    "index": 0,
                    "position": [111, 222, 333],
                }
            ],
        }
    )
    manifest = load_manifest(_write_json(tmp_path / "mixed.json", value))

    receipt = apply_manifest(manifest, source_root, tmp_path / "overlay")

    assert [entry["path"] for entry in receipt["files"]] == [
        DESTINATION_PATH,
        "CD/LEVEL07/LEVEL1.DAT",
    ]
    assert receipt["files"][1]["edits"][0]["operation"] == "set-scene-record-position"


def test_schema_one_rejects_whole_file_replacement(tmp_path: Path) -> None:
    value = _replacement_manifest(b"destination", b"replacement")
    value["schema_version"] = 1
    with pytest.raises(ManifestError, match="format is unsupported"):
        load_manifest(_write_json(tmp_path / "v1.json", value))


@pytest.mark.parametrize("schema_version", [True, 0, 3, "2"])
def test_manifest_rejects_non_exact_schema_versions(
    tmp_path: Path, schema_version: object
) -> None:
    value = _replacement_manifest(b"destination", b"replacement")
    value["schema_version"] = schema_version
    with pytest.raises(ManifestError, match="schema_version"):
        load_manifest(_write_json(tmp_path / "schema.json", value))


def test_manifest_rejects_non_string_format_without_type_error(tmp_path: Path) -> None:
    value = _replacement_manifest(b"destination", b"replacement")
    value["files"][0]["format"] = []
    with pytest.raises(ManifestError, match="format is unsupported"):
        load_manifest(_write_json(tmp_path / "format.json", value))


def test_cli_applies_whole_file_replacement(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    destination = b"destination"
    replacement = b"replacement"
    source_root = tmp_path / "work-copy"
    _write_work_copy(source_root, destination, replacement)
    manifest_path = _write_json(
        tmp_path / "replacement.json",
        _replacement_manifest(destination, replacement),
    )
    output = tmp_path / "overlay"

    result = cli_main(
        [
            "apply",
            str(manifest_path),
            "--source-root",
            str(source_root),
            "--output-root",
            str(output),
        ]
    )

    assert result == 0
    assert json.loads(capsys.readouterr().out)["schema_version"] == 2
    assert (output / DESTINATION_PATH).read_bytes() == replacement
