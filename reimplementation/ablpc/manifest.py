"""Validated manifest application for sparse or staged game-data overlays."""

from __future__ import annotations

import copy
import ctypes
from contextlib import contextmanager
from dataclasses import dataclass, replace
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import struct
import tempfile
from typing import Any, Iterator

from .level_dat import LevelDat


class ManifestError(ValueError):
    """Raised for an invalid manifest or unsafe application request."""


class ManifestCompositionConflict(ManifestError):
    """Raised when two valid manifests make incompatible combined claims."""

    def __init__(self, report: dict[str, Any]):
        self.report = report
        super().__init__(_canonical_json(report).decode("utf-8"))


@dataclass(frozen=True)
class _PreparedFile:
    relative: PurePosixPath
    input_size: int
    output_bytes: bytes
    receipt: dict[str, Any]
    report_edits: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class _EditClaim:
    edit: dict[str, Any]
    edit_index: int
    start: int
    end: int


@dataclass(frozen=True)
class _CompositionInput:
    manifest: dict[str, Any]
    canonical_bytes: bytes
    digest: str


@dataclass(frozen=True)
class _MountEntry:
    mount_id: int
    parent_id: int
    major: int
    minor: int
    root: Path
    mount_point: Path
    mount_order: int


@dataclass(frozen=True)
class _ReceiptHandleChain:
    directory_descriptors: tuple[int, ...]
    directory_metadata: tuple[os.stat_result, ...]
    file_descriptor: int
    file_metadata: os.stat_result


class _MountIdRequest(ctypes.Structure):
    _fields_ = (
        ("size", ctypes.c_uint32),
        ("mount_namespace_fd", ctypes.c_uint32),
        ("mount_id", ctypes.c_uint64),
        ("parameter", ctypes.c_uint64),
    )


_RECEIPT_RELATIVE = PurePosixPath(".ablpc", "receipt.json")
_LISTMOUNT_REVERSE = 1
_LSMT_ROOT = 0xFFFFFFFFFFFFFFFF
_STATMOUNT_SB_BASIC = 1
_STATMOUNT_MNT_BASIC = 2
_STATMOUNT_ORDER_FIELDS = _STATMOUNT_SB_BASIC | _STATMOUNT_MNT_BASIC
_SYS_STATMOUNT = 457
_SYS_LISTMOUNT = 458
_MOUNT_ID_BATCH_SIZE = 256
_STATMOUNT_BUFFER_SIZE = 512


def load_manifest(path: Path | str) -> dict[str, Any]:
    manifest_path = Path(path)
    try:
        value = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ManifestError(f"cannot read manifest {manifest_path}: {error}") from error
    _validate_manifest(value)
    return value


def replay_receipt(
    receipt_path: Path | str,
    source_root: Path | str,
    output_root: Path | str,
) -> dict[str, Any]:
    """Reproduce one sparse overlay from an exact ordinary receipt."""

    source = _resolved_root(source_root, "source")
    output = _resolved_root(output_root, "output")
    _validate_roots(source, output)
    if not source.is_dir():
        raise ManifestError(f"source root is not a directory: {source}")
    _validate_new_output_root(output, label="replay output root")

    receipt = _load_external_receipt(receipt_path, source, output)
    manifest, prepared, _ = _prepare_receipt_authority(receipt, source)
    _validate_output_plan(prepared, output, force=False)
    output.mkdir(parents=True, exist_ok=True)
    return _write_prepared(manifest, prepared, output)


def remove_receipt(
    receipt_path: Path | str,
    source_root: Path | str,
    overlay_root: Path | str,
) -> dict[str, Any]:
    """Remove one exact sparse overlay using its external ordinary receipt."""

    source = _resolved_root(source_root, "source")
    overlay = _resolved_root(overlay_root, "output")
    _validate_roots(source, overlay)
    if not source.is_dir():
        raise ManifestError(f"source root is not a directory: {source}")
    _validate_output_root_topology(overlay)
    overlay_metadata = _lstat(overlay)
    if overlay_metadata is None or not stat.S_ISDIR(overlay_metadata.st_mode):
        raise ManifestError(f"overlay root is not a directory: {overlay}")

    receipt = _load_external_receipt(receipt_path, source, overlay)
    _, prepared, expected_receipt = _prepare_receipt_authority(receipt, source)
    return _remove_prepared_overlay(prepared, expected_receipt, overlay)


def compose_manifests(
    left: dict[str, Any],
    right: dict[str, Any],
    source_root: Path | str,
) -> dict[str, Any]:
    """Compose exactly two independently valid manifests.

    Composition is limited to the existing schema-1/schema-2 operations. Each
    input is first applied in memory against the same source root. Entries for
    one destination merge only when their exact byte claims are disjoint.
    """

    source = _resolved_root(source_root, "source")
    if not source.is_dir():
        raise ManifestError(f"source root is not a directory: {source}")

    inputs: list[_CompositionInput] = []
    for value in (left, right):
        _validate_manifest(value)
        normalized = _canonicalized_manifest(value)
        canonical_bytes = _canonical_json(normalized)
        inputs.append(
            _CompositionInput(
                manifest=normalized,
                canonical_bytes=canonical_bytes,
                digest=hashlib.sha256(canonical_bytes).hexdigest(),
            )
        )

    ordered = sorted(inputs, key=lambda item: (item.digest, item.canonical_bytes))
    identities = [
        {"name": item.manifest["name"], "sha256": item.digest} for item in ordered
    ]
    input_rank = {id(item): rank for rank, item in enumerate(ordered)}

    destinations: dict[
        str, list[tuple[_CompositionInput, dict[str, Any]]]
    ] = {}
    for item in ordered:
        for entry in item.manifest["files"]:
            normalized_path = _normalized_windows_path(entry["path"])
            destinations.setdefault(normalized_path, []).append((item, entry))

    # Resolve semantic Windows-path ambiguity and incompatible source
    # declarations before reading either path. This makes structural conflict
    # output independent of host filesystem case behavior.
    for normalized_path in sorted(destinations):
        members = destinations[normalized_path]
        if len(members) == 1:
            continue
        _, first_entry = members[0]
        _, second_entry = members[1]
        if first_entry["path"] != second_entry["path"]:
            _raise_composition_conflict(
                identities, "case-insensitive-path-collision", normalized_path, None
            )
        if first_entry["format"] != second_entry["format"]:
            _raise_composition_conflict(
                identities, "format-mismatch", normalized_path, None
            )
        if first_entry["sha256"] != second_entry["sha256"]:
            _raise_composition_conflict(
                identities, "source-hash-mismatch", normalized_path, None
            )

    claims_by_input: dict[int, dict[str, tuple[_EditClaim, ...]]] = {}
    for item in ordered:
        # Independently execute every guard and transformation in memory before
        # deriving or combining byte claims.
        _prepare_manifest(item.manifest, source)
        claims_by_input[id(item)] = _manifest_claims(item.manifest, source)

    combined_files: list[dict[str, Any]] = []
    for normalized_path in sorted(destinations):
        members = destinations[normalized_path]
        if len(members) == 1:
            item, entry = members[0]
            combined_files.append(
                _composed_file_entry(
                    entry,
                    claims_by_input[id(item)][normalized_path],
                    input_rank[id(item)],
                )
            )
            continue

        first_item, first_entry = members[0]
        second_item, second_entry = members[1]
        first_claims = claims_by_input[id(first_item)][normalized_path]
        second_claims = claims_by_input[id(second_item)][normalized_path]
        if first_entry["format"] == "opaque-file-v0":
            overlap_end = min(first_claims[0].end, second_claims[0].end)
            _raise_composition_conflict(
                identities,
                "opaque-whole-file-collision",
                normalized_path,
                (0, overlap_end),
            )

        overlaps = sorted(
            (
                max(first.start, second.start),
                min(first.end, second.end),
            )
            for first in first_claims
            for second in second_claims
            if max(first.start, second.start) < min(first.end, second.end)
        )
        if overlaps:
            _raise_composition_conflict(
                identities,
                "overlapping-byte-claims",
                normalized_path,
                overlaps[0],
            )

        ranked_claims = [
            (claim, input_rank[id(first_item)]) for claim in first_claims
        ] + [(claim, input_rank[id(second_item)]) for claim in second_claims]
        combined_files.append(
            _composed_file_entry_from_ranked_claims(first_entry, ranked_claims)
        )

    # A whole-file replacement source must not become a destination merely by
    # combining two manifests that were each safe on their own.
    cross_collisions: list[str] = []
    for item in ordered:
        for entry in item.manifest["files"]:
            if entry["format"] != "opaque-file-v0":
                continue
            source_path = _normalized_windows_path(entry["edits"][0]["source_path"])
            for destination_item, _ in destinations.get(source_path, []):
                if destination_item is not item:
                    cross_collisions.append(source_path)
    if cross_collisions:
        _raise_composition_conflict(
            identities,
            "replacement-source-destination-collision",
            sorted(cross_collisions)[0],
            None,
        )

    combined_files.sort(
        key=lambda entry: (_normalized_windows_path(entry["path"]), entry["path"])
    )
    combined_digest = hashlib.sha256(
        _canonical_json([item.digest for item in ordered])
    ).hexdigest()
    combined = {
        "schema_version": max(item.manifest["schema_version"] for item in ordered),
        "name": f"composed-{combined_digest}",
        "files": combined_files,
    }
    _validate_manifest(combined)
    # Prove that the canonical input interleaving retains every independently
    # validated guard and produces one ordinary existing-schema manifest.
    _prepare_manifest(combined, source)
    return combined


def apply_manifest(
    manifest: dict[str, Any],
    source_root: Path | str,
    output_root: Path | str,
    *,
    force: bool = False,
) -> dict[str, Any]:
    source = _resolved_root(source_root, "source")
    output = _resolved_root(output_root, "output")
    _validate_roots(source, output)
    if not source.is_dir():
        raise ManifestError(f"source root is not a directory: {source}")
    if output.exists() and not output.is_dir():
        raise ManifestError(f"output root is not a directory: {output}")

    # Validate and compute every result before creating or changing the output.
    # A bad hash in a later entry must not leave an earlier entry applied.
    prepared = _prepare_manifest(manifest, source)
    _validate_output_plan(prepared, output, force=force)
    output.mkdir(parents=True, exist_ok=True)
    return _write_prepared(manifest, prepared, output)


def dry_run_manifest(
    manifest: dict[str, Any],
    source_root: Path | str,
) -> dict[str, Any]:
    """Validate and report one manifest without writing an output or receipt."""

    source = _resolved_root(source_root, "source")
    if not source.is_dir():
        raise ManifestError(f"source root is not a directory: {source}")

    prepared = _prepare_manifest(manifest, source)
    normalized = _canonicalized_manifest(manifest)
    return {
        "report_schema_version": 1,
        "manifest": {
            "schema_version": normalized["schema_version"],
            "name": normalized["name"],
            "sha256": hashlib.sha256(_canonical_json(normalized)).hexdigest(),
        },
        "files": [
            {
                "path": entry["path"],
                "format": entry["format"],
                "input_sha256": item.receipt["input_sha256"],
                "input_size": item.input_size,
                "output_sha256": item.receipt["output_sha256"],
                "output_size": len(item.output_bytes),
                "edits": [copy.deepcopy(edit) for edit in item.report_edits],
            }
            for entry, item in zip(manifest["files"], prepared, strict=True)
        ],
    }


def stage_manifest(
    manifest: dict[str, Any],
    source_root: Path | str,
    game_root: Path | str,
) -> dict[str, Any]:
    source = _resolved_root(source_root, "source")
    game = _resolved_root(game_root, "output")
    _validate_roots(source, game)
    if not source.is_dir():
        raise ManifestError(f"source root is not a directory: {source}")
    if game.exists():
        raise ManifestError(f"staged game root already exists: {game}")

    # Preflight before copying so a wrong destination or replacement hash does
    # not leave a staged tree that appears to contain an applied manifest.
    prepared = _prepare_manifest(manifest, source)
    _validate_new_output_root(game)
    _validate_staged_output_plan(prepared, source)
    shutil.copytree(source, game, copy_function=shutil.copy2)
    return _write_prepared(manifest, prepared, game)


def restore_manifest(
    manifest: dict[str, Any],
    source_root: Path | str,
    game_root: Path | str,
) -> dict[str, Any]:
    """Restore one exact complete staged tree from its clean source tree."""

    source = _resolved_root(source_root, "source")
    game = _resolved_root(game_root, "output")
    _validate_roots(source, game)
    if not source.is_dir():
        raise ManifestError(f"source root is not a directory: {source}")
    _validate_output_root_topology(game)
    game_metadata = _lstat(game)
    if game_metadata is None or not stat.S_ISDIR(game_metadata.st_mode):
        raise ManifestError(f"staged game root is not a directory: {game}")

    source_entries = _regular_tree_inventory(source, "source tree")
    _validate_restoration_source_entries(source_entries)
    prepared = _prepare_manifest(manifest, source)
    expected_receipt = _receipt_for(manifest, prepared)
    source_bytes = _validate_complete_staged_tree(
        source, game, source_entries, prepared, expected_receipt
    )

    # The complete source/game/receipt/output and mutation topology is
    # authenticated above. Restoration is deliberately limited to recorded
    # destinations and the fixed receipt metadata directory.
    for item in prepared:
        _atomic_write(
            _safe_output_file(game, item.relative), source_bytes[item.relative]
        )
    _safe_output_file(game, _RECEIPT_RELATIVE).unlink()
    (game / _RECEIPT_RELATIVE.parent).rmdir()
    return expected_receipt


def remove_manifest(
    manifest: dict[str, Any],
    source_root: Path | str,
    overlay_root: Path | str,
) -> dict[str, Any]:
    """Remove one exact sparse overlay previously produced by ``apply``.

    The ordinary receipt is recomputed from the supplied manifest and source
    tree. Every expected path, output hash, and byte of the receipt must still
    match, and the overlay may contain no other entries. All checks complete
    before any recorded file is removed.
    """

    source = _resolved_root(source_root, "source")
    overlay = _resolved_root(overlay_root, "output")
    _validate_roots(source, overlay)
    if not source.is_dir():
        raise ManifestError(f"source root is not a directory: {source}")
    _validate_output_root_topology(overlay)
    overlay_metadata = _lstat(overlay)
    if overlay_metadata is None or not stat.S_ISDIR(overlay_metadata.st_mode):
        raise ManifestError(f"overlay root is not a directory: {overlay}")

    prepared = _prepare_manifest(manifest, source)
    expected_receipt = _receipt_for(manifest, prepared)
    return _remove_prepared_overlay(prepared, expected_receipt, overlay)


def _remove_prepared_overlay(
    prepared: list[_PreparedFile],
    expected_receipt: dict[str, Any],
    overlay: Path,
) -> dict[str, Any]:
    expected_files = [item.relative for item in prepared] + [_RECEIPT_RELATIVE]
    expected_directories = _expected_overlay_directories(expected_files)

    # lstat/scandir cannot distinguish an ordinary path from a same-filesystem
    # bind mount. Authenticate the deletion topology from the kernel's mount
    # table before traversing, reading, or removing anything below the overlay.
    _validate_unmounted_deletion_plan(
        overlay, expected_files, expected_directories
    )

    for relative in expected_files:
        _validate_existing_regular_file(overlay, relative, "overlay")
    _validate_exact_overlay_tree(
        overlay, expected_files, expected_directories
    )

    receipt_path = _safe_output_file(overlay, _RECEIPT_RELATIVE)
    receipt_bytes = _read_overlay_bytes(receipt_path, "overlay receipt")
    receipt = _parse_receipt(receipt_bytes, receipt_path)
    if _canonical_json(receipt) != _canonical_json(expected_receipt):
        raise ManifestError(
            "overlay receipt does not match the recomputed manifest/source result"
        )
    if receipt_bytes != _receipt_bytes(expected_receipt):
        raise ManifestError(
            "overlay receipt encoding does not match ordinary apply output"
        )

    for item in prepared:
        destination = _safe_output_file(overlay, item.relative)
        actual_sha = hashlib.sha256(
            _read_overlay_bytes(destination, f"overlay output {item.relative}")
        ).hexdigest()
        expected_sha = item.receipt["output_sha256"]
        if actual_sha != expected_sha:
            raise ManifestError(
                f"overlay output SHA-256 mismatch for {item.relative}: "
                f"expected {expected_sha}, got {actual_sha}"
            )

    # The complete deletion plan is authenticated above. Removal is deliberately
    # limited to the recorded sparse files, fixed receipt, and now-empty parents.
    for relative in [item.relative for item in prepared]:
        _safe_output_file(overlay, relative).unlink()
    receipt_path.unlink()
    for relative in sorted(
        expected_directories, key=lambda value: (-len(value.parts), value.as_posix())
    ):
        overlay.joinpath(*relative.parts).rmdir()
    overlay.rmdir()
    return expected_receipt


def _prepare_manifest(
    manifest: dict[str, Any], source_root: Path
) -> list[_PreparedFile]:
    _validate_manifest(manifest)
    prepared: list[_PreparedFile] = []
    for entry in manifest["files"]:
        relative = _safe_relative_path(entry["path"])
        source_file = _existing_source_file(source_root, relative, "manifest input")
        source_bytes = source_file.read_bytes()
        source_sha = hashlib.sha256(source_bytes).hexdigest()
        if source_sha.lower() != entry["sha256"].lower():
            raise ManifestError(
                f"SHA-256 mismatch for {entry['path']}: "
                f"expected {entry['sha256']}, got {source_sha}"
            )

        if entry["format"] == "pc-level-dat-prefix-v0":
            output_bytes, applied, report_edits = _apply_level_dat_edits(
                source_bytes, entry["edits"]
            )
        else:
            output_bytes, applied = _apply_whole_file_replacement(
                source_root, entry["edits"][0]
            )
            report_edits = [
                {
                    "edit_index": 0,
                    "operation": "replace-whole-file",
                    "source_path": entry["edits"][0]["source_path"],
                    "input_range": {"start": 0, "end": len(source_bytes)},
                    "output_range": {"start": 0, "end": len(output_bytes)},
                }
            ]

        prepared.append(
            _PreparedFile(
                relative=relative,
                input_size=len(source_bytes),
                output_bytes=output_bytes,
                receipt={
                    "path": entry["path"],
                    "input_sha256": source_sha,
                    "output_sha256": hashlib.sha256(output_bytes).hexdigest(),
                    "edits": applied,
                },
                report_edits=tuple(report_edits),
            )
        )
    return prepared


def _apply_level_dat_edits(
    source_bytes: bytes, edits: list[dict[str, Any]]
) -> tuple[bytes, list[dict[str, Any]], list[dict[str, Any]]]:
    output_bytes = source_bytes
    applied: list[dict[str, Any]] = []
    report_edits: list[dict[str, Any]] = []
    for edit_index, edit in enumerate(edits):
        parsed = LevelDat.parse(output_bytes)
        if edit["operation"] == "set-scene-record-position":
            position = tuple(edit["position"])
            output_bytes = parsed.set_record_position(
                edit["section"], edit["index"], position
            )
            applied.append(
                {
                    "edit_index": edit_index,
                    "operation": edit["operation"],
                    "section": edit["section"],
                    "index": edit["index"],
                    "position": list(position),
                }
            )
            record = parsed.records(edit["section"])[edit["index"]]
            start, end = record.offset, record.offset + 12
        elif edit["operation"] == "set-scene-record-payload-target-offset":
            output_bytes = parsed.set_record_payload_target_offset(
                edit["section"],
                edit["index"],
                edit["expected_target_offset"],
                edit["target_offset"],
            )
            applied.append(
                {
                    "edit_index": edit_index,
                    "operation": edit["operation"],
                    "section": edit["section"],
                    "index": edit["index"],
                    "expected_target_offset": edit["expected_target_offset"],
                    "target_offset": edit["target_offset"],
                }
            )
            record = parsed.records(edit["section"])[edit["index"]]
            reference = parsed.payload_target_reference(
                edit["section"], edit["index"]
            )
            start = reference.payload_offset + reference.target_field_offset
            end = start + 4
        else:
            output_bytes = parsed.set_record_field_0c(
                edit["section"],
                edit["index"],
                edit["expected_value"],
                edit["value"],
            )
            applied.append(
                {
                    "edit_index": edit_index,
                    "operation": edit["operation"],
                    "section": edit["section"],
                    "index": edit["index"],
                    "expected_value": edit["expected_value"],
                    "value": edit["value"],
                }
            )
            record = parsed.records(edit["section"])[edit["index"]]
            start, end = record.offset + 0x0C, record.offset + 0x0E
        report_edits.append(
            {
                "edit_index": edit_index,
                "operation": edit["operation"],
                "section": edit["section"],
                "record_index": edit["index"],
                "record_offset": record.offset,
                "destination_range": {"start": start, "end": end},
            }
        )
    return output_bytes, applied, report_edits


def _apply_whole_file_replacement(
    source_root: Path, edit: dict[str, Any]
) -> tuple[bytes, list[dict[str, Any]]]:
    replacement_relative = _safe_relative_path(edit["source_path"])
    replacement_file = _existing_source_file(
        source_root, replacement_relative, "replacement source"
    )
    replacement_bytes = replacement_file.read_bytes()
    replacement_sha = hashlib.sha256(replacement_bytes).hexdigest()
    if replacement_sha.lower() != edit["source_sha256"].lower():
        raise ManifestError(
            f"replacement SHA-256 mismatch for {edit['source_path']}: "
            f"expected {edit['source_sha256']}, got {replacement_sha}"
        )
    return replacement_bytes, [
        {
            "edit_index": 0,
            "operation": "replace-whole-file",
            "source_path": edit["source_path"],
            "replacement_sha256": replacement_sha,
        }
    ]


def _canonicalized_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(manifest)
    for entry in normalized["files"]:
        entry["sha256"] = entry["sha256"].lower()
        if entry["format"] == "opaque-file-v0":
            entry["edits"][0]["source_sha256"] = entry["edits"][0][
                "source_sha256"
            ].lower()
    return normalized


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def _manifest_claims(
    manifest: dict[str, Any], source_root: Path
) -> dict[str, tuple[_EditClaim, ...]]:
    claims: dict[str, tuple[_EditClaim, ...]] = {}
    for entry in manifest["files"]:
        normalized_path = _normalized_windows_path(entry["path"])
        relative = _safe_relative_path(entry["path"])
        source_file = _existing_source_file(source_root, relative, "manifest input")
        source_bytes = source_file.read_bytes()
        if entry["format"] == "opaque-file-v0":
            claims[normalized_path] = (
                _EditClaim(
                    edit=copy.deepcopy(entry["edits"][0]),
                    edit_index=0,
                    start=0,
                    end=len(source_bytes),
                ),
            )
            continue

        parsed = LevelDat.parse(source_bytes)
        entry_claims: list[_EditClaim] = []
        for edit_index, edit in enumerate(entry["edits"]):
            record = parsed.records(edit["section"])[edit["index"]]
            if edit["operation"] == "set-scene-record-position":
                start, end = record.offset, record.offset + 12
            elif edit["operation"] == "set-scene-record-field-0c":
                start, end = record.offset + 0x0C, record.offset + 0x0E
            else:
                reference = parsed.payload_target_reference(
                    edit["section"], edit["index"]
                )
                start = reference.payload_offset + reference.target_field_offset
                end = start + 4
            entry_claims.append(
                _EditClaim(
                    edit=copy.deepcopy(edit),
                    edit_index=edit_index,
                    start=start,
                    end=end,
                )
            )
        claims[normalized_path] = tuple(entry_claims)
    return claims


def _composed_file_entry(
    entry: dict[str, Any], claims: tuple[_EditClaim, ...], rank: int
) -> dict[str, Any]:
    return _composed_file_entry_from_ranked_claims(
        entry, [(claim, rank) for claim in claims]
    )


def _composed_file_entry_from_ranked_claims(
    entry: dict[str, Any], ranked_claims: list[tuple[_EditClaim, int]]
) -> dict[str, Any]:
    ordered_claims = sorted(
        ranked_claims,
        key=lambda item: (
            item[1],
            item[0].edit_index,
            _canonical_json(item[0].edit),
        ),
    )
    return {
        "path": entry["path"],
        "sha256": entry["sha256"].lower(),
        "format": entry["format"],
        "edits": [copy.deepcopy(claim.edit) for claim, _ in ordered_claims],
    }


def _raise_composition_conflict(
    identities: list[dict[str, str]],
    kind: str,
    destination: str,
    overlap: tuple[int, int] | None,
) -> None:
    raise ManifestCompositionConflict(
        {
            "destination": destination,
            "error": "manifest-composition-conflict",
            "inputs": identities,
            "kind": kind,
            "overlap": list(overlap) if overlap is not None else None,
        }
    )


def _write_prepared(
    manifest: dict[str, Any], prepared: list[_PreparedFile], output_root: Path
) -> dict[str, Any]:
    for item in prepared:
        destination = _safe_output_file(output_root, item.relative)
        _atomic_write(destination, item.output_bytes)

    receipt = _receipt_for(manifest, prepared)
    receipt_path = _safe_output_file(output_root, _RECEIPT_RELATIVE)
    _atomic_write(receipt_path, _receipt_bytes(receipt))
    return receipt


def _receipt_for(
    manifest: dict[str, Any], prepared: list[_PreparedFile]
) -> dict[str, Any]:
    return {
        "schema_version": manifest["schema_version"],
        "manifest_name": manifest["name"],
        "files": [item.receipt for item in prepared],
    }


def _receipt_bytes(receipt: dict[str, Any]) -> bytes:
    return (json.dumps(receipt, indent=2) + "\n").encode()


def _load_external_receipt(
    receipt_path: Path | str,
    source_root: Path,
    output_root: Path,
) -> dict[str, Any]:
    requested = Path(receipt_path)
    if not requested.is_absolute():
        requested = Path.cwd() / requested
    _reject_protected_root(requested, "receipt")
    lexical = Path(os.path.abspath(requested))
    _reject_protected_root(lexical, "receipt")
    _validate_external_receipt_placement(lexical, source_root, output_root)

    acquired = _open_external_receipt_chain(lexical)
    with _managed_receipt_handle_chain(acquired, lexical):
        try:
            with os.fdopen(acquired.file_descriptor, "rb", closefd=False) as stream:
                data = stream.read()
            opened_after = os.fstat(acquired.file_descriptor)
            if not _same_receipt_file_metadata(
                acquired.file_metadata, opened_after
            ):
                raise ManifestError(
                    f"receipt input changed while it was being read: {lexical}"
                )
        except OSError as error:
            raise ManifestError(
                f"cannot read receipt input {lexical}: {error}"
            ) from error

        # Re-resolve placement and independently reacquire the complete lexical
        # chain while the original descriptors remain open. A renamed parent,
        # replacement directory, or newly installed link must therefore either
        # fail no-link acquisition or disagree with the retained device/inode
        # chain before receipt parsing can begin.
        _validate_external_receipt_placement(lexical, source_root, output_root)
        reacquired = _open_external_receipt_chain(lexical)
        with _managed_receipt_handle_chain(reacquired, lexical):
            if not _same_receipt_handle_chain(acquired, reacquired):
                raise ManifestError(
                    f"receipt input path changed before it could be read safely: {lexical}"
                )

    receipt = _parse_receipt(data, lexical)
    _manifest_from_receipt(receipt)
    if data != _receipt_bytes(receipt):
        raise ManifestError("receipt input encoding is not ordinary apply output")
    return receipt


def _validate_external_receipt_placement(
    lexical: Path, source_root: Path, output_root: Path
) -> None:
    try:
        resolved = lexical.resolve(strict=True)
    except OSError as error:
        raise ManifestError(
            f"cannot resolve receipt input {lexical}: {error}"
        ) from error
    _reject_protected_root(resolved, "receipt")
    for root, label in ((source_root, "source"), (output_root, "output")):
        if resolved == root or root in resolved.parents:
            raise ManifestError(f"receipt input must be outside the {label} root")


def _open_external_receipt_chain(lexical: Path) -> _ReceiptHandleChain:
    if not lexical.is_absolute() or len(lexical.parts) < 2:
        raise ManifestError(f"receipt input is not a regular file: {lexical}")

    directory_flags = (
        getattr(os, "O_PATH", os.O_RDONLY)
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    file_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    directory_descriptors: list[int] = []
    directory_metadata: list[os.stat_result] = []
    file_descriptor: int | None = None

    try:
        root_descriptor = os.open(lexical.anchor, directory_flags)
        directory_descriptors.append(root_descriptor)
        root_metadata = os.fstat(root_descriptor)
        if not stat.S_ISDIR(root_metadata.st_mode):
            raise ManifestError(
                f"receipt input ancestor is not a directory: {lexical.anchor}"
            )
        directory_metadata.append(root_metadata)

        current = Path(lexical.anchor)
        for component in lexical.parts[1:-1]:
            current /= component
            parent_descriptor = directory_descriptors[-1]
            try:
                before = os.stat(
                    component,
                    dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
            except FileNotFoundError as error:
                raise ManifestError(
                    f"receipt input does not exist: {lexical}"
                ) from error
            except OSError as error:
                raise ManifestError(
                    f"cannot inspect receipt input ancestor {current}: {error}"
                ) from error
            if stat.S_ISLNK(before.st_mode):
                raise ManifestError(
                    f"receipt input path contains a symlink: {current}"
                )
            if not stat.S_ISDIR(before.st_mode):
                raise ManifestError(
                    f"receipt input ancestor is not a directory: {current}"
                )
            try:
                descriptor = os.open(
                    component, directory_flags, dir_fd=parent_descriptor
                )
            except OSError as error:
                raise ManifestError(
                    f"cannot open receipt input ancestor {current}: {error}"
                ) from error
            directory_descriptors.append(descriptor)
            opened = os.fstat(descriptor)
            if not _same_path_component(before, opened, directory=True):
                raise ManifestError(
                    f"receipt input ancestor changed before it could be acquired: {current}"
                )
            directory_metadata.append(opened)

        filename = lexical.parts[-1]
        parent_descriptor = directory_descriptors[-1]
        try:
            before_file = os.stat(
                filename,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError as error:
            raise ManifestError(f"receipt input does not exist: {lexical}") from error
        except OSError as error:
            raise ManifestError(
                f"cannot inspect receipt input {lexical}: {error}"
            ) from error
        if not stat.S_ISREG(before_file.st_mode):
            raise ManifestError(f"receipt input is not a regular file: {lexical}")
        if before_file.st_nlink != 1:
            raise ManifestError(f"receipt input has multiple hard links: {lexical}")

        try:
            file_descriptor = os.open(
                filename, file_flags, dir_fd=parent_descriptor
            )
        except OSError as error:
            raise ManifestError(
                f"cannot read receipt input {lexical}: {error}"
            ) from error
        opened_file = os.fstat(file_descriptor)
        if not _same_receipt_file_metadata(before_file, opened_file):
            raise ManifestError(
                f"receipt input changed before it could be read safely: {lexical}"
            )

        return _ReceiptHandleChain(
            directory_descriptors=tuple(directory_descriptors),
            directory_metadata=tuple(directory_metadata),
            file_descriptor=file_descriptor,
            file_metadata=opened_file,
        )
    except BaseException as error:
        close_error = _close_receipt_descriptors(
            file_descriptor, directory_descriptors
        )
        if close_error is not None:
            error.add_note(f"receipt handle cleanup also failed: {close_error}")
        raise


def _same_path_component(
    before: os.stat_result, after: os.stat_result, *, directory: bool
) -> bool:
    expected_type = stat.S_ISDIR if directory else stat.S_ISREG
    return (
        expected_type(before.st_mode)
        and expected_type(after.st_mode)
        and (before.st_dev, before.st_ino) == (after.st_dev, after.st_ino)
    )


def _same_receipt_file_metadata(
    before: os.stat_result, after: os.stat_result
) -> bool:
    stable_fields = (
        "st_mode",
        "st_nlink",
        "st_dev",
        "st_ino",
        "st_size",
        "st_mtime_ns",
        "st_ctime_ns",
    )
    return (
        _same_path_component(before, after, directory=False)
        and before.st_nlink == 1
        and after.st_nlink == 1
        and all(getattr(before, field) == getattr(after, field) for field in stable_fields)
    )


def _same_receipt_handle_chain(
    first: _ReceiptHandleChain, second: _ReceiptHandleChain
) -> bool:
    return (
        len(first.directory_metadata) == len(second.directory_metadata)
        and all(
            _same_path_component(before, after, directory=True)
            for before, after in zip(
                first.directory_metadata, second.directory_metadata, strict=True
            )
        )
        and _same_receipt_file_metadata(first.file_metadata, second.file_metadata)
    )


def _close_receipt_descriptors(
    file_descriptor: int | None,
    directory_descriptors: tuple[int, ...] | list[int],
) -> OSError | None:
    descriptors = [] if file_descriptor is None else [file_descriptor]
    descriptors.extend(reversed(directory_descriptors))
    first_error: OSError | None = None
    for descriptor in descriptors:
        try:
            os.close(descriptor)
        except OSError as error:
            if first_error is None:
                first_error = error
    return first_error


def _close_receipt_handle_chain(chain: _ReceiptHandleChain) -> OSError | None:
    return _close_receipt_descriptors(
        chain.file_descriptor, chain.directory_descriptors
    )


@contextmanager
def _managed_receipt_handle_chain(
    chain: _ReceiptHandleChain, lexical: Path
) -> Iterator[_ReceiptHandleChain]:
    try:
        yield chain
    except BaseException as error:
        close_error = _close_receipt_handle_chain(chain)
        if close_error is not None:
            error.add_note(f"receipt handle cleanup also failed: {close_error}")
        raise
    else:
        close_error = _close_receipt_handle_chain(chain)
        if close_error is not None:
            raise ManifestError(
                f"cannot close receipt input {lexical}: {close_error}"
            ) from close_error


def _prepare_receipt_authority(
    receipt: dict[str, Any], source_root: Path
) -> tuple[dict[str, Any], list[_PreparedFile], dict[str, Any]]:
    manifest = _manifest_from_receipt(receipt)
    prepared = _prepare_manifest(manifest, source_root)
    expected_receipt = _receipt_for(manifest, prepared)
    if _receipt_bytes(receipt) != _receipt_bytes(expected_receipt):
        raise ManifestError(
            "receipt input does not match the recomputed source and edits"
        )
    return manifest, prepared, expected_receipt


def _manifest_from_receipt(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ManifestError("receipt input root must be a JSON object")
    if set(value) != {"schema_version", "manifest_name", "files"}:
        raise ManifestError(
            "receipt input root must contain exactly schema_version, "
            "manifest_name, and files"
        )
    schema_version = value.get("schema_version")
    if (
        not isinstance(schema_version, int)
        or isinstance(schema_version, bool)
        or schema_version not in (1, 2)
    ):
        raise ManifestError("receipt input schema_version must be 1 or 2")
    manifest_name = value.get("manifest_name")
    if not isinstance(manifest_name, str) or not manifest_name.strip():
        raise ManifestError("receipt input manifest_name must be a non-empty string")
    files = value.get("files")
    if not isinstance(files, list) or not files:
        raise ManifestError("receipt input files must be a non-empty array")

    manifest_files: list[dict[str, Any]] = []
    for file_index, receipt_file in enumerate(files):
        label = f"receipt input files[{file_index}]"
        if not isinstance(receipt_file, dict):
            raise ManifestError(f"{label} must be an object")
        if set(receipt_file) != {
            "path",
            "input_sha256",
            "output_sha256",
            "edits",
        }:
            raise ManifestError(
                f"{label} must contain exactly path, input_sha256, "
                "output_sha256, and edits"
            )
        _safe_relative_path(receipt_file["path"])
        for key in ("input_sha256", "output_sha256"):
            digest = receipt_file[key]
            _validate_sha256(digest, f"{label}.{key}")
            if digest != digest.lower():
                raise ManifestError(f"{label}.{key} must be lowercase")
        receipt_edits = receipt_file["edits"]
        if not isinstance(receipt_edits, list) or not receipt_edits:
            raise ManifestError(f"{label}.edits must be a non-empty array")

        manifest_edits: list[dict[str, Any]] = []
        operation_family: str | None = None
        for edit_index, receipt_edit in enumerate(receipt_edits):
            edit_label = f"{label}.edits[{edit_index}]"
            if not isinstance(receipt_edit, dict):
                raise ManifestError(f"{edit_label} must be an object")
            operation = receipt_edit.get("operation")
            if operation == "set-scene-record-position":
                expected_keys = {
                    "edit_index",
                    "operation",
                    "section",
                    "index",
                    "position",
                }
                family = "level"
            elif operation == "set-scene-record-payload-target-offset":
                expected_keys = {
                    "edit_index",
                    "operation",
                    "section",
                    "index",
                    "expected_target_offset",
                    "target_offset",
                }
                family = "level"
            elif operation == "set-scene-record-field-0c":
                expected_keys = {
                    "edit_index",
                    "operation",
                    "section",
                    "index",
                    "expected_value",
                    "value",
                }
                family = "level"
            elif operation == "replace-whole-file":
                expected_keys = {
                    "edit_index",
                    "operation",
                    "source_path",
                    "replacement_sha256",
                }
                family = "opaque"
            else:
                raise ManifestError(f"{edit_label}.operation is unsupported")
            if set(receipt_edit) != expected_keys:
                raise ManifestError(
                    f"{edit_label} fields do not match operation {operation!r}"
                )
            if (
                not isinstance(receipt_edit["edit_index"], int)
                or isinstance(receipt_edit["edit_index"], bool)
                or receipt_edit["edit_index"] != edit_index
            ):
                raise ManifestError(
                    f"{edit_label}.edit_index must equal authored index {edit_index}"
                )
            if operation == "set-scene-record-position":
                manifest_edit = {
                    key: copy.deepcopy(receipt_edit[key])
                    for key in ("operation", "section", "index", "position")
                }
            elif operation == "set-scene-record-payload-target-offset":
                manifest_edit = {
                    key: copy.deepcopy(receipt_edit[key])
                    for key in (
                        "operation",
                        "section",
                        "index",
                        "expected_target_offset",
                        "target_offset",
                    )
                }
            elif operation == "set-scene-record-field-0c":
                manifest_edit = {
                    key: copy.deepcopy(receipt_edit[key])
                    for key in (
                        "operation",
                        "section",
                        "index",
                        "expected_value",
                        "value",
                    )
                }
            else:
                replacement_sha256 = receipt_edit["replacement_sha256"]
                _validate_sha256(
                    replacement_sha256, f"{edit_label}.replacement_sha256"
                )
                if replacement_sha256 != replacement_sha256.lower():
                    raise ManifestError(
                        f"{edit_label}.replacement_sha256 must be lowercase"
                    )
                manifest_edit = {
                    "operation": operation,
                    "source_path": receipt_edit["source_path"],
                    "source_sha256": replacement_sha256,
                }
            if operation_family is not None and operation_family != family:
                raise ManifestError(
                    f"{label}.edits mixes incompatible operation families"
                )
            operation_family = family
            manifest_edits.append(manifest_edit)

        format_name = (
            "opaque-file-v0"
            if operation_family == "opaque"
            else "pc-level-dat-prefix-v0"
        )
        manifest_files.append(
            {
                "path": receipt_file["path"],
                "sha256": receipt_file["input_sha256"],
                "format": format_name,
                "edits": manifest_edits,
            }
        )

    manifest = {
        "schema_version": schema_version,
        "name": manifest_name,
        "files": manifest_files,
    }
    _validate_manifest(manifest)
    return manifest


def _validate_manifest(value: Any) -> None:
    if not isinstance(value, dict):
        raise ManifestError("manifest root must be a JSON object")
    if set(value) != {"schema_version", "name", "files"}:
        raise ManifestError(
            "manifest root must contain exactly schema_version, name, and files"
        )
    schema_version = value.get("schema_version")
    if (
        not isinstance(schema_version, int)
        or isinstance(schema_version, bool)
        or schema_version not in (1, 2)
    ):
        raise ManifestError("manifest schema_version must be 1 or 2")
    if not isinstance(value.get("name"), str) or not value["name"].strip():
        raise ManifestError("manifest name must be a non-empty string")
    files = value.get("files")
    if not isinstance(files, list) or not files:
        raise ManifestError("manifest files must be a non-empty array")

    seen_paths: set[str] = set()
    destination_paths: set[str] = set()
    replacement_sources: list[tuple[int, str, str]] = []
    for file_index, entry in enumerate(files):
        _validate_file_entry(entry, file_index, schema_version)
        normalized_path = _normalized_windows_path(entry["path"])
        if normalized_path in seen_paths:
            raise ManifestError(
                f"files[{file_index}].path duplicates another manifest input"
            )
        seen_paths.add(normalized_path)
        destination_paths.add(normalized_path)
        if entry["format"] == "opaque-file-v0":
            source_path = entry["edits"][0]["source_path"]
            normalized_source = _normalized_windows_path(source_path)
            if normalized_source == normalized_path:
                raise ManifestError(
                    f"files[{file_index}] replacement source and destination are the same path"
                )
            replacement_sources.append((file_index, source_path, normalized_source))

    for file_index, source_path, normalized_source in replacement_sources:
        if normalized_source in destination_paths:
            raise ManifestError(
                f"files[{file_index}] replacement source path {source_path!r} "
                "collides with a manifest destination"
            )


def _validate_file_entry(entry: Any, file_index: int, schema_version: int) -> None:
    if not isinstance(entry, dict):
        raise ManifestError(f"files[{file_index}] must be an object")
    if set(entry) != {"path", "sha256", "format", "edits"}:
        raise ManifestError(
            f"files[{file_index}] must contain exactly path, sha256, format, and edits"
        )
    _safe_relative_path(entry["path"])
    _validate_sha256(entry["sha256"], f"files[{file_index}].sha256")
    format_name = entry["format"]
    supported_formats = {"pc-level-dat-prefix-v0"}
    if schema_version == 2:
        supported_formats.add("opaque-file-v0")
    if not isinstance(format_name, str) or format_name not in supported_formats:
        raise ManifestError(f"files[{file_index}].format is unsupported")
    edits = entry["edits"]
    if not isinstance(edits, list) or not edits:
        raise ManifestError(f"files[{file_index}].edits must be a non-empty array")
    if format_name == "opaque-file-v0":
        if len(edits) != 1:
            raise ManifestError(
                f"files[{file_index}].edits must contain exactly one whole-file replacement"
            )
        _validate_whole_file_edit(edits[0], file_index)
        return
    for edit_index, edit in enumerate(edits):
        _validate_level_dat_edit(edit, file_index, edit_index)


def _validate_level_dat_edit(edit: Any, file_index: int, edit_index: int) -> None:
    label = f"files[{file_index}].edits[{edit_index}]"
    if not isinstance(edit, dict):
        raise ManifestError(f"{label} must be an object")
    operation = edit.get("operation")
    if operation == "set-scene-record-position":
        expected_keys = {"operation", "section", "index", "position"}
    elif operation == "set-scene-record-payload-target-offset":
        expected_keys = {
            "operation",
            "section",
            "index",
            "expected_target_offset",
            "target_offset",
        }
    elif operation == "set-scene-record-field-0c":
        expected_keys = {
            "operation",
            "section",
            "index",
            "expected_value",
            "value",
        }
    else:
        raise ManifestError(f"{label}.operation is unsupported")
    if set(edit) != expected_keys:
        raise ManifestError(f"{label} fields do not match operation {operation!r}")
    if edit["section"] not in ("primary", "secondary"):
        raise ManifestError(f"{label}.section must be primary or secondary")
    if not isinstance(edit["index"], int) or isinstance(edit["index"], bool):
        raise ManifestError(f"{label}.index must be an integer")
    if edit["index"] < 0:
        raise ManifestError(f"{label}.index cannot be negative")
    if operation == "set-scene-record-payload-target-offset":
        for key in ("expected_target_offset", "target_offset"):
            number = edit[key]
            if not isinstance(number, int) or isinstance(number, bool):
                raise ManifestError(f"{label}.{key} must be an integer")
            if number < 0 or number > 2**32 - 1:
                raise ManifestError(f"{label}.{key} is outside unsigned 32-bit range")
        return
    if operation == "set-scene-record-field-0c":
        for key in ("expected_value", "value"):
            number = edit[key]
            if not isinstance(number, int) or isinstance(number, bool):
                raise ManifestError(f"{label}.{key} must be an integer")
            if number < -(2**15) or number > 2**15 - 1:
                raise ManifestError(f"{label}.{key} is outside signed 16-bit range")
        return
    position = edit["position"]
    if not isinstance(position, list) or len(position) != 3:
        raise ManifestError(f"{label}.position must contain three integers")
    for number in position:
        if not isinstance(number, int) or isinstance(number, bool):
            raise ManifestError(f"{label}.position values must be integers")
        if number < -(2**31) or number > 2**31 - 1:
            raise ManifestError(f"{label}.position value is outside signed 32-bit range")


def _validate_whole_file_edit(edit: Any, file_index: int) -> None:
    label = f"files[{file_index}].edits[0]"
    if not isinstance(edit, dict):
        raise ManifestError(f"{label} must be an object")
    if set(edit) != {"operation", "source_path", "source_sha256"}:
        raise ManifestError(
            f"{label} fields do not match operation {edit.get('operation')!r}"
        )
    if edit["operation"] != "replace-whole-file":
        raise ManifestError(f"{label}.operation is unsupported")
    _safe_relative_path(edit["source_path"])
    _validate_sha256(edit["source_sha256"], f"{label}.source_sha256")


def _validate_sha256(value: Any, label: str) -> None:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdefABCDEF" for character in value)
    ):
        raise ManifestError(f"{label} is not a SHA-256 hex digest")


def _safe_relative_path(value: Any) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise ManifestError("manifest path must be a non-empty POSIX path string")
    components = value.split("/")
    windows_invalid = '<>"|?*'
    if (
        value.startswith("/")
        or any(component in ("", ".", "..") for component in components)
        or components[0].casefold() == ".ablpc"
        or "\\" in value
        or ":" in value
        or "\x00" in value
        or any(
            character in windows_invalid or ord(character) < 32
            for character in value
        )
        or any(component.endswith((".", " ")) for component in components)
    ):
        raise ManifestError(f"unsafe manifest path: {value!r}")
    return PurePosixPath(*components)


def _normalized_windows_path(value: str) -> str:
    return str(_safe_relative_path(value)).casefold()


def _existing_source_file(root: Path, relative: PurePosixPath, label: str) -> Path:
    candidate = root.joinpath(*relative.parts)
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as error:
        raise ManifestError(f"{label} does not exist: {candidate}") from error
    if root != resolved and root not in resolved.parents:
        raise ManifestError(f"{label} escapes source root: {candidate}")
    if not resolved.is_file():
        raise ManifestError(f"{label} is not a file: {candidate}")
    return resolved


def _safe_output_file(root: Path, relative: PurePosixPath) -> Path:
    candidate = root.joinpath(*relative.parts)
    resolved_parent = candidate.parent.resolve(strict=False)
    if root != resolved_parent and root not in resolved_parent.parents:
        raise ManifestError(f"output path escapes output root: {candidate}")
    if candidate.is_symlink():
        raise ManifestError(f"refusing symlink output path: {candidate}")
    return candidate


def _validate_output_plan(
    prepared: list[_PreparedFile], output_root: Path, *, force: bool
) -> None:
    _validate_output_root_topology(output_root)
    for item in prepared:
        _validate_planned_file(
            output_root,
            item.relative,
            allow_existing=force,
            label="output",
        )
    _validate_planned_file(
        output_root,
        _RECEIPT_RELATIVE,
        allow_existing=force,
        label="output",
    )


def _validate_staged_output_plan(
    prepared: list[_PreparedFile], source_root: Path
) -> None:
    # copytree reproduces this topology at the new game root. Validate every
    # path that will later be replaced before the copy can create partial output.
    for item in prepared:
        _validate_planned_file(
            source_root,
            item.relative,
            allow_existing=True,
            label="staged output source",
        )
    _validate_planned_file(
        source_root,
        _RECEIPT_RELATIVE,
        allow_existing=True,
        label="staged output source",
    )


def _validate_new_output_root(
    output_root: Path, *, label: str = "staged game root"
) -> None:
    _validate_output_root_topology(output_root)
    if _lstat(output_root) is not None:
        raise ManifestError(f"{label} already exists: {output_root}")


def _validate_output_root_topology(output_root: Path) -> None:
    current = Path(output_root.anchor)
    for component in output_root.parts[1:-1]:
        current /= component
        metadata = _lstat(current)
        if metadata is None:
            break
        if stat.S_ISLNK(metadata.st_mode):
            raise ManifestError(f"output root ancestor is a symlink: {current}")
        if not stat.S_ISDIR(metadata.st_mode):
            raise ManifestError(f"output root ancestor is not a directory: {current}")

    metadata = _lstat(output_root)
    if metadata is None:
        return
    if stat.S_ISLNK(metadata.st_mode):
        raise ManifestError(f"output root is a symlink: {output_root}")
    if not stat.S_ISDIR(metadata.st_mode):
        raise ManifestError(f"output root is not a directory: {output_root}")


def _validate_planned_file(
    root: Path,
    relative: PurePosixPath,
    *,
    allow_existing: bool,
    label: str,
) -> None:
    candidate = root.joinpath(*relative.parts)
    current = root
    for component in relative.parts[:-1]:
        current /= component
        metadata = _lstat(current)
        if metadata is None:
            break
        if stat.S_ISLNK(metadata.st_mode):
            raise ManifestError(f"{label} ancestor is a symlink: {current}")
        if not stat.S_ISDIR(metadata.st_mode):
            raise ManifestError(f"{label} ancestor is not a directory: {current}")

    metadata = _lstat(candidate)
    if metadata is None:
        return
    if stat.S_ISLNK(metadata.st_mode):
        raise ManifestError(f"{label} destination is a symlink: {candidate}")
    if not stat.S_ISREG(metadata.st_mode):
        raise ManifestError(f"{label} destination is not a regular file: {candidate}")
    if not allow_existing:
        raise ManifestError(f"output already exists (use --force): {candidate}")


def _validate_existing_regular_file(
    root: Path, relative: PurePosixPath, label: str
) -> None:
    _validate_planned_file(root, relative, allow_existing=True, label=label)
    candidate = root.joinpath(*relative.parts)
    metadata = _lstat(candidate)
    if metadata is None:
        raise ManifestError(f"{label} file is missing: {candidate}")
    if metadata.st_nlink != 1:
        raise ManifestError(f"{label} file has multiple hard links: {candidate}")


def _expected_overlay_directories(
    expected_files: list[PurePosixPath],
) -> set[PurePosixPath]:
    expected_directories: set[PurePosixPath] = set()
    for relative in expected_files:
        parent = relative.parent
        while parent != PurePosixPath("."):
            expected_directories.add(parent)
            parent = parent.parent
    return expected_directories


def _validate_exact_overlay_tree(
    overlay_root: Path,
    expected_files: list[PurePosixPath],
    expected_directories: set[PurePosixPath],
) -> None:
    expected: dict[PurePosixPath, str] = {
        relative: "regular file" for relative in expected_files
    }
    expected.update(
        {relative: "directory" for relative in expected_directories}
    )
    actual: dict[PurePosixPath, str] = {}

    def visit(directory: Path, relative_directory: PurePosixPath) -> None:
        try:
            with os.scandir(directory) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name)
        except OSError as error:
            raise ManifestError(
                f"cannot inspect overlay tree {directory}: {error}"
            ) from error
        for entry in entries:
            relative = (
                PurePosixPath(entry.name)
                if relative_directory == PurePosixPath(".")
                else relative_directory / entry.name
            )
            try:
                metadata = entry.stat(follow_symlinks=False)
            except OSError as error:
                raise ManifestError(
                    f"cannot inspect overlay entry {entry.path}: {error}"
                ) from error
            if stat.S_ISDIR(metadata.st_mode):
                kind = "directory"
            elif stat.S_ISREG(metadata.st_mode):
                kind = "regular file"
            elif stat.S_ISLNK(metadata.st_mode):
                kind = "symlink"
            else:
                kind = "non-regular file"
            actual[relative] = kind
            if kind == "directory":
                visit(Path(entry.path), relative)

    visit(overlay_root, PurePosixPath("."))

    unexpected = sorted(set(actual) - set(expected), key=lambda path: path.as_posix())
    if unexpected:
        relative = unexpected[0]
        raise ManifestError(
            f"overlay contains extra content: {relative} ({actual[relative]})"
        )
    missing = sorted(set(expected) - set(actual), key=lambda path: path.as_posix())
    if missing:
        relative = missing[0]
        raise ManifestError(
            f"overlay content is missing: {relative} ({expected[relative]})"
        )
    mismatched = sorted(
        (
            relative
            for relative in expected
            if actual[relative] != expected[relative]
        ),
        key=lambda path: path.as_posix(),
    )
    if mismatched:
        relative = mismatched[0]
        raise ManifestError(
            f"overlay entry type mismatch for {relative}: "
            f"expected {expected[relative]}, got {actual[relative]}"
        )


def _regular_tree_inventory(
    root: Path, label: str
) -> dict[PurePosixPath, tuple[str, os.stat_result]]:
    entries: dict[PurePosixPath, tuple[str, os.stat_result]] = {}
    paths_by_casefold: dict[str, PurePosixPath] = {}

    def visit(directory: Path, relative_directory: PurePosixPath) -> None:
        try:
            with os.scandir(directory) as iterator:
                children = sorted(iterator, key=lambda entry: entry.name)
        except OSError as error:
            raise ManifestError(
                f"cannot inspect {label} {directory}: {error}"
            ) from error
        child_directories: list[tuple[Path, PurePosixPath]] = []
        for child in children:
            relative = (
                PurePosixPath(child.name)
                if relative_directory == PurePosixPath(".")
                else relative_directory / child.name
            )
            try:
                metadata = child.stat(follow_symlinks=False)
            except OSError as error:
                raise ManifestError(
                    f"cannot inspect {label} entry {child.path}: {error}"
                ) from error
            if stat.S_ISDIR(metadata.st_mode):
                kind = "directory"
            elif stat.S_ISREG(metadata.st_mode):
                kind = "regular file"
                if metadata.st_nlink != 1:
                    raise ManifestError(
                        f"{label} file has multiple hard links: {child.path}"
                    )
            elif stat.S_ISLNK(metadata.st_mode):
                raise ManifestError(f"{label} contains a symlink: {relative}")
            else:
                raise ManifestError(
                    f"{label} contains a non-regular entry: {relative}"
                )
            folded = relative.as_posix().casefold()
            prior = paths_by_casefold.get(folded)
            if prior is not None:
                raise ManifestError(
                    f"{label} contains case-insensitive duplicate paths: "
                    f"{prior} and {relative}"
                )
            paths_by_casefold[folded] = relative
            entries[relative] = (kind, metadata)
            if kind == "directory":
                child_directories.append((Path(child.path), relative))

        # Validate every sibling spelling before descending into any branch.
        # A case-colliding directory may itself be a mounted or otherwise
        # independent tree, so ambiguity must stop traversal at its parent.
        for child_path, relative in child_directories:
            visit(child_path, relative)

    visit(root, PurePosixPath("."))
    return entries


def _read_stable_tree_file(
    root: Path,
    relative: PurePosixPath,
    metadata: os.stat_result,
    label: str,
) -> bytes:
    path = root.joinpath(*relative.parts)
    try:
        data = path.read_bytes()
    except OSError as error:
        raise ManifestError(f"cannot read {label} {path}: {error}") from error
    after = _lstat(path)
    if after is None or (
        stat.S_IFMT(after.st_mode),
        after.st_dev,
        after.st_ino,
        after.st_nlink,
        after.st_size,
        after.st_mtime_ns,
        after.st_ctime_ns,
    ) != (
        stat.S_IFMT(metadata.st_mode),
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_nlink,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    ):
        raise ManifestError(f"{label} changed during restoration preflight: {path}")
    return data


def _validate_restoration_source_entries(
    source_entries: dict[PurePosixPath, tuple[str, os.stat_result]],
) -> None:
    reserved = sorted(
        (
            relative
            for relative in source_entries
            if relative.parts and relative.parts[0].casefold() == ".ablpc"
        ),
        key=lambda path: path.as_posix(),
    )
    if reserved:
        raise ManifestError(
            f"source tree contains reserved .ablpc content: {reserved[0]}"
        )


def _validate_complete_staged_tree(
    source_root: Path,
    game_root: Path,
    source_entries: dict[PurePosixPath, tuple[str, os.stat_result]],
    prepared: list[_PreparedFile],
    expected_receipt: dict[str, Any],
) -> dict[PurePosixPath, bytes]:
    source_files = {
        relative
        for relative, (kind, _) in source_entries.items()
        if kind == "regular file"
    }
    source_directories = {
        relative
        for relative, (kind, _) in source_entries.items()
        if kind == "directory"
    }
    destinations = {item.relative for item in prepared}
    missing_destinations = sorted(
        destinations - source_files, key=lambda path: path.as_posix()
    )
    if missing_destinations:
        raise ManifestError(
            "source tree is missing a manifest destination: "
            f"{missing_destinations[0]}"
        )

    expected_files = sorted(
        source_files | {_RECEIPT_RELATIVE}, key=lambda path: path.as_posix()
    )
    expected_directories = source_directories | {_RECEIPT_RELATIVE.parent}
    _validate_unmounted_restoration_plan(
        game_root, expected_files, expected_directories
    )

    game_entries = _regular_tree_inventory(game_root, "staged game tree")
    expected_kinds = {
        relative: kind for relative, (kind, _) in source_entries.items()
    }
    expected_kinds[_RECEIPT_RELATIVE.parent] = "directory"
    expected_kinds[_RECEIPT_RELATIVE] = "regular file"

    unexpected = sorted(
        set(game_entries) - set(expected_kinds), key=lambda path: path.as_posix()
    )
    if unexpected:
        raise ManifestError(
            f"staged game tree contains extra content: {unexpected[0]}"
        )
    missing = sorted(
        set(expected_kinds) - set(game_entries), key=lambda path: path.as_posix()
    )
    if missing:
        raise ManifestError(f"staged game tree content is missing: {missing[0]}")
    mismatched = sorted(
        (
            relative
            for relative, expected_kind in expected_kinds.items()
            if game_entries[relative][0] != expected_kind
        ),
        key=lambda path: path.as_posix(),
    )
    if mismatched:
        relative = mismatched[0]
        raise ManifestError(
            f"staged game tree entry type mismatch for {relative}: "
            f"expected {expected_kinds[relative]}, got {game_entries[relative][0]}"
        )

    receipt_path = _safe_output_file(game_root, _RECEIPT_RELATIVE)
    receipt_bytes = _read_stable_tree_file(
        game_root,
        _RECEIPT_RELATIVE,
        game_entries[_RECEIPT_RELATIVE][1],
        "staged game receipt",
    )
    receipt = _parse_receipt(receipt_bytes, receipt_path)
    if _canonical_json(receipt) != _canonical_json(expected_receipt):
        raise ManifestError(
            "staged game receipt does not match the recomputed manifest/source result"
        )
    if receipt_bytes != _receipt_bytes(expected_receipt):
        raise ManifestError(
            "staged game receipt encoding does not match ordinary stage output"
        )

    prepared_by_path = {item.relative: item for item in prepared}
    restoration_bytes: dict[PurePosixPath, bytes] = {}
    for relative in sorted(source_files, key=lambda path: path.as_posix()):
        source_bytes = _read_stable_tree_file(
            source_root,
            relative,
            source_entries[relative][1],
            "source tree file",
        )
        game_bytes = _read_stable_tree_file(
            game_root,
            relative,
            game_entries[relative][1],
            "staged game file",
        )
        item = prepared_by_path.get(relative)
        if item is None:
            if game_bytes != source_bytes:
                raise ManifestError(
                    f"staged game unrelated content differs from source: {relative}"
                )
            continue
        if hashlib.sha256(source_bytes).hexdigest() != item.receipt["input_sha256"]:
            raise ManifestError(
                f"source tree input SHA-256 changed during restoration preflight: {relative}"
            )
        if hashlib.sha256(game_bytes).hexdigest() != item.receipt["output_sha256"]:
            raise ManifestError(
                f"staged game output SHA-256 mismatch for {relative}"
            )
        restoration_bytes[relative] = source_bytes

    return restoration_bytes


def _validate_unmounted_deletion_plan(
    overlay_root: Path,
    expected_files: list[PurePosixPath],
    expected_directories: set[PurePosixPath],
) -> None:
    _validate_unmounted_plan(
        overlay_root,
        expected_files,
        expected_directories,
        plan_label="overlay deletion plan",
        ancestry_label="overlay root ancestry",
    )


def _validate_unmounted_restoration_plan(
    game_root: Path,
    expected_files: list[PurePosixPath],
    expected_directories: set[PurePosixPath],
) -> None:
    _validate_unmounted_plan(
        game_root,
        expected_files,
        expected_directories,
        plan_label="game restoration plan",
        ancestry_label="game root ancestry",
    )


def _validate_unmounted_plan(
    root: Path,
    expected_files: list[PurePosixPath],
    expected_directories: set[PurePosixPath],
    *,
    plan_label: str,
    ancestry_label: str,
) -> None:
    mount_entries = _linux_mount_entries()
    mounted_paths = frozenset(entry.mount_point for entry in mount_entries)
    planned_paths = [root]
    planned_paths.extend(
        root.joinpath(*relative.parts)
        for relative in expected_directories
    )
    planned_paths.extend(
        root.joinpath(*relative.parts) for relative in expected_files
    )
    for path in sorted(planned_paths, key=os.fspath):
        normalized = Path(os.path.normpath(os.fspath(path)))
        if normalized in mounted_paths:
            raise ManifestError(
                f"{plan_label} contains a mounted path: {path}"
            )

    # Reaching the exact requested root also traverses its proper ancestry. An
    # ordinary filesystem mount such as /home or /tmp is a valid ownership
    # boundary, but a newer mount that exposes an already reachable filesystem
    # root at a different path is an alias to independent content. Refuse only
    # such alias records on the requested ancestry before traversing the tree.
    alias_points = _mount_alias_points(mount_entries)
    for parent in root.parents:
        if parent in alias_points:
            raise ManifestError(
                f"{ancestry_label} contains a mount alias: {parent}"
            )


def _linux_mount_points() -> frozenset[Path]:
    return frozenset(entry.mount_point for entry in _linux_mount_entries())


def _linux_mount_entries() -> tuple[_MountEntry, ...]:
    mountinfo_path = Path("/proc/self/mountinfo")
    try:
        mountinfo = mountinfo_path.read_bytes()
    except OSError as error:
        raise ManifestError(
            f"cannot inspect overlay mount topology {mountinfo_path}: {error}"
        ) from error

    mount_entries: list[_MountEntry] = []
    mount_ids: set[int] = set()
    for line_number, line in enumerate(mountinfo.splitlines(), start=1):
        fields = line.split()
        separators = [index for index, field in enumerate(fields) if field == b"-"]
        if (
            len(separators) != 1
            or separators[0] < 6
            or len(fields) != separators[0] + 4
        ):
            raise ManifestError(
                f"cannot parse overlay mount topology {mountinfo_path} "
                f"line {line_number}"
            )
        try:
            major_text, minor_text = fields[2].split(b":", 1)
            if not all(
                value.isdigit()
                for value in (fields[0], fields[1], major_text, minor_text)
            ):
                raise ValueError("non-decimal mountinfo identifier")
            mount_id = int(fields[0])
            parent_id = int(fields[1])
            major = int(major_text)
            minor = int(minor_text)
        except (ValueError, TypeError) as error:
            raise ManifestError(
                f"cannot parse overlay mount topology {mountinfo_path} "
                f"line {line_number}"
            ) from error
        if (
            mount_id <= 0
            or parent_id < 0
            or major < 0
            or minor < 0
            or mount_id in mount_ids
        ):
            raise ManifestError(
                f"cannot parse overlay mount topology {mountinfo_path} "
                f"line {line_number}"
            )
        mount_ids.add(mount_id)
        root = Path(
            os.path.normpath(
                os.fsdecode(
                    _decode_mountinfo_path(
                        fields[3], mountinfo_path, line_number
                    )
                )
            )
        )
        decoded = _decode_mountinfo_path(
            fields[4], mountinfo_path, line_number
        )
        mount_point = Path(os.path.normpath(os.fsdecode(decoded)))
        if not root.is_absolute() or not mount_point.is_absolute():
            raise ManifestError(
                f"cannot parse overlay mount topology {mountinfo_path} "
                f"line {line_number}"
            )
        mount_entries.append(
            _MountEntry(
                mount_id=mount_id,
                parent_id=parent_id,
                major=major,
                minor=minor,
                root=root,
                mount_point=mount_point,
                mount_order=0,
            )
        )
    mount_points = {entry.mount_point for entry in mount_entries}
    if Path("/") not in mount_points:
        raise ManifestError(
            f"cannot inspect overlay mount topology {mountinfo_path}: "
            "root mount is missing"
        )
    order_by_id = _linux_mount_order_by_old_id()
    try:
        current_mountinfo = mountinfo_path.read_bytes()
    except OSError as error:
        raise ManifestError(
            f"cannot inspect overlay mount topology {mountinfo_path}: {error}"
        ) from error
    if current_mountinfo != mountinfo:
        raise ManifestError(
            "cannot inspect overlay mount ordering: mount table changed "
            "during preflight"
        )
    if set(order_by_id) != mount_ids:
        raise ManifestError(
            "cannot inspect overlay mount ordering: mount table changed "
            "during preflight"
        )

    ordered_entries: list[_MountEntry] = []
    for entry in mount_entries:
        mount_order, parent_id, major, minor = order_by_id[entry.mount_id]
        if (
            parent_id != entry.parent_id
            or major != entry.major
            or minor != entry.minor
        ):
            raise ManifestError(
                "cannot inspect overlay mount ordering: mount table changed "
                "during preflight"
            )
        ordered_entries.append(replace(entry, mount_order=mount_order))
    return tuple(ordered_entries)


def _linux_mount_order_by_old_id() -> dict[int, tuple[int, int, int, int]]:
    """Map reusable mountinfo IDs to explicit kernel later-mount order."""

    unique_ids = _linux_unique_mount_ids_later_first()
    result: dict[int, tuple[int, int, int, int]] = {}
    total = len(unique_ids)
    for later_index, unique_id in enumerate(unique_ids):
        old_id, parent_old_id, major, minor = _linux_statmount_basic(unique_id)
        if old_id in result:
            raise ManifestError(
                "cannot inspect overlay mount ordering: duplicate mountinfo ID"
            )
        # LISTMOUNT_REVERSE returns later mounts first. Convert that explicit
        # sequence to an ordinal that increases from older to later mounts;
        # unlike /proc/self/mountinfo IDs, this does not infer age from a
        # reusable numeric identifier.
        result[old_id] = (total - later_index, parent_old_id, major, minor)
    if not result:
        raise ManifestError("cannot inspect overlay mount ordering: no mounts")
    return result


def _linux_unique_mount_ids_later_first() -> tuple[int, ...]:
    libc = ctypes.CDLL(None, use_errno=True)
    syscall = libc.syscall
    syscall.restype = ctypes.c_long
    unique_ids: list[int] = []
    last_mount_id = 0
    seen: set[int] = set()

    while True:
        request = _MountIdRequest(
            size=ctypes.sizeof(_MountIdRequest),
            mount_namespace_fd=0,
            mount_id=_LSMT_ROOT,
            parameter=last_mount_id,
        )
        batch = (ctypes.c_uint64 * _MOUNT_ID_BATCH_SIZE)()
        ctypes.set_errno(0)
        count = syscall(
            _SYS_LISTMOUNT,
            ctypes.byref(request),
            batch,
            _MOUNT_ID_BATCH_SIZE,
            _LISTMOUNT_REVERSE,
        )
        if count < 0:
            error_number = ctypes.get_errno()
            raise ManifestError(
                "cannot inspect overlay mount ordering with listmount: "
                f"{os.strerror(error_number)}"
            )
        if count > _MOUNT_ID_BATCH_SIZE:
            raise ManifestError(
                "cannot inspect overlay mount ordering: invalid listmount count"
            )
        if count == 0:
            break
        current = [int(batch[index]) for index in range(count)]
        if (
            any(value <= 0 or value in seen for value in current)
            or any(left <= right for left, right in zip(current, current[1:]))
            or (unique_ids and unique_ids[-1] <= current[0])
        ):
            raise ManifestError(
                "cannot inspect overlay mount ordering: invalid listmount sequence"
            )
        unique_ids.extend(current)
        seen.update(current)
        if count < _MOUNT_ID_BATCH_SIZE:
            break
        if current[-1] == last_mount_id:
            raise ManifestError(
                "cannot inspect overlay mount ordering: listmount made no progress"
            )
        last_mount_id = current[-1]
    return tuple(unique_ids)


def _linux_statmount_basic(unique_id: int) -> tuple[int, int, int, int]:
    libc = ctypes.CDLL(None, use_errno=True)
    syscall = libc.syscall
    syscall.restype = ctypes.c_long
    request = _MountIdRequest(
        size=ctypes.sizeof(_MountIdRequest),
        mount_namespace_fd=0,
        mount_id=unique_id,
        parameter=_STATMOUNT_ORDER_FIELDS,
    )
    buffer = ctypes.create_string_buffer(_STATMOUNT_BUFFER_SIZE)
    ctypes.set_errno(0)
    result = syscall(
        _SYS_STATMOUNT,
        ctypes.byref(request),
        buffer,
        _STATMOUNT_BUFFER_SIZE,
        0,
    )
    if result < 0:
        error_number = ctypes.get_errno()
        raise ManifestError(
            "cannot inspect overlay mount ordering with statmount: "
            f"{os.strerror(error_number)}"
        )

    data = buffer.raw
    size = struct.unpack_from("=I", data, 0)[0]
    mask = struct.unpack_from("=Q", data, 8)[0]
    major, minor = struct.unpack_from("=II", data, 16)
    returned_unique_id = struct.unpack_from("=Q", data, 40)[0]
    old_id, parent_old_id = struct.unpack_from("=II", data, 56)
    if (
        size < 64
        or size > len(data)
        or mask & _STATMOUNT_ORDER_FIELDS != _STATMOUNT_ORDER_FIELDS
        or returned_unique_id != unique_id
        or old_id <= 0
        or parent_old_id < 0
    ):
        raise ManifestError(
            "cannot inspect overlay mount ordering: invalid statmount result"
        )
    return old_id, parent_old_id, major, minor


def _mount_alias_points(entries: tuple[_MountEntry, ...]) -> frozenset[Path]:
    """Return visible mountpoints that alias an earlier visible filesystem path."""

    mount_orders = {entry.mount_order for entry in entries}
    if (
        any(entry.mount_order <= 0 for entry in entries)
        or len(mount_orders) != len(entries)
    ):
        raise ManifestError("cannot inspect overlay mount ordering: invalid order")
    entries_by_id = {entry.mount_id: entry for entry in entries}
    covered_mount_ids: set[int] = set()
    for covering in entries:
        covered = entries_by_id.get(covering.parent_id)
        if covered is None:
            continue
        # A stacked mount at the same pathname names the covered lower mount
        # as its parent. Only the topmost record describes the path reached by
        # subsequent overlay traversal.
        if covered.mount_point == covering.mount_point:
            covered_mount_ids.add(covered.mount_id)

    visible_entries = tuple(
        entry for entry in entries if entry.mount_id not in covered_mount_ids
    )

    aliases: set[Path] = set()
    for candidate in visible_entries:
        for source in visible_entries:
            if source.mount_order >= candidate.mount_order:
                continue
            if (source.major, source.minor) != (candidate.major, candidate.minor):
                continue
            try:
                relative_root = candidate.root.relative_to(source.root)
            except ValueError:
                continue
            source_path = Path(
                os.path.normpath(
                    os.fspath(source.mount_point.joinpath(*relative_root.parts))
                )
            )
            if source_path != candidate.mount_point:
                aliases.add(candidate.mount_point)
                break
    return frozenset(aliases)


def _decode_mountinfo_path(
    value: bytes, mountinfo_path: Path, line_number: int
) -> bytes:
    decoded = bytearray()
    index = 0
    while index < len(value):
        if value[index] != ord("\\"):
            decoded.append(value[index])
            index += 1
            continue
        escape = value[index + 1 : index + 4]
        if escape not in {b"011", b"012", b"040", b"134"}:
            raise ManifestError(
                f"cannot parse overlay mount topology {mountinfo_path} "
                f"line {line_number}"
            )
        decoded.append(int(escape, 8))
        index += 4
    return bytes(decoded)


def _read_overlay_bytes(path: Path, label: str) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise ManifestError(f"cannot read {label} {path}: {error}") from error


def _parse_receipt(data: bytes, path: Path) -> dict[str, Any]:
    def object_from_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ManifestError(f"overlay receipt contains duplicate key {key!r}")
            value[key] = item
        return value

    def reject_constant(value: str) -> None:
        raise ManifestError(f"overlay receipt contains invalid JSON number {value}")

    try:
        value = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=object_from_pairs,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
        raise ManifestError(f"cannot parse overlay receipt {path}: {error}") from error
    if not isinstance(value, dict):
        raise ManifestError("overlay receipt root must be a JSON object")
    return value


def _lstat(path: Path) -> os.stat_result | None:
    try:
        return path.lstat()
    except FileNotFoundError:
        return None
    except OSError as error:
        raise ManifestError(f"cannot inspect output topology {path}: {error}") from error


def _validate_roots(source: Path, output: Path) -> None:
    for root, label in ((source, "source"), (output, "output")):
        if any(part.lower() in {"originals", "media"} for part in root.parts):
            raise ManifestError(f"refusing {label} root under protected content: {root}")
    if source == output:
        raise ManifestError("source and output roots must differ")
    if source in output.parents or output in source.parents:
        raise ManifestError("source and output roots must not contain one another")


def _resolved_root(value: Path | str, label: str) -> Path:
    requested = Path(value)
    if not requested.is_absolute():
        requested = Path.cwd() / requested
    _reject_protected_root(requested, label)
    lexical = Path(os.path.abspath(requested))
    if label == "output":
        _reject_output_symlink_components(lexical)
    resolved = lexical.resolve()
    _reject_protected_root(resolved, label)
    return resolved


def _reject_protected_root(root: Path, label: str) -> None:
    if any(part.lower() in {"originals", "media"} for part in root.parts):
        raise ManifestError(f"refusing {label} root under protected content: {root}")


def _reject_output_symlink_components(requested: Path) -> None:
    current = Path(requested.anchor)
    for component in requested.parts[1:]:
        current /= component
        metadata = _lstat(current)
        if metadata is None:
            return
        if stat.S_ISLNK(metadata.st_mode):
            raise ManifestError(f"output root path contains a symlink: {current}")


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
            temporary.write(data)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_name = temporary.name
        os.replace(temporary_name, path)
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)
