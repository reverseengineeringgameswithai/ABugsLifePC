"""Command-line interface for the bounded ABL PC modding slice."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .anm import ANM_HEADER_SIZE, AnmFile, AnmFormatError
from .level_dat import (
    DatFormatError,
    LevelDat,
    SUPPORTED_SCENE_DISPATCH_MASK,
    SUPPORTED_SCENE_DISPATCH_VALUE,
)
from .manifest import (
    ManifestCompositionConflict,
    ManifestError,
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ablpc-mod")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser(
        "inspect", help="inspect a confirmed LEVEL*.DAT prefix"
    )
    inspect_parser.add_argument("path", type=Path)
    inspect_parser.add_argument("--json", action="store_true")
    inspect_parser.add_argument(
        "--records", choices=("primary", "secondary"), help="include scene records"
    )
    inspect_parser.add_argument(
        "--payload-targets",
        choices=("primary", "secondary"),
        help="include positive-count targets for the supported PC dispatch-0x49 class",
    )

    scan_parser = subparsers.add_parser(
        "scan", help="validate every LEVEL*.DAT below a directory"
    )
    scan_parser.add_argument("root", type=Path)

    target_scan_parser = subparsers.add_parser(
        "scan-payload-targets",
        help="validate positive-count targets used by the PC 0x49 scene dispatch",
    )
    target_scan_parser.add_argument("root", type=Path)
    target_scan_parser.add_argument("--json", action="store_true")

    anm_inspect_parser = subparsers.add_parser(
        "inspect-anm", help="inspect the bounded PC .ANM first-level layout"
    )
    anm_inspect_parser.add_argument("path", type=Path)
    anm_inspect_parser.add_argument("--json", action="store_true")

    anm_scan_parser = subparsers.add_parser(
        "scan-anm", help="validate PC .ANM files below a directory"
    )
    anm_scan_parser.add_argument("root", type=Path)
    anm_scan_parser.add_argument("--json", action="store_true")

    apply_parser = subparsers.add_parser(
        "apply", help="build a sparse overlay from a manifest"
    )
    apply_parser.add_argument("manifest", type=Path)
    apply_parser.add_argument("--source-root", required=True, type=Path)
    apply_parser.add_argument("--output-root", required=True, type=Path)
    apply_parser.add_argument("--force", action="store_true")

    stage_parser = subparsers.add_parser(
        "stage", help="copy a game work tree and apply a manifest"
    )
    stage_parser.add_argument("manifest", type=Path)
    stage_parser.add_argument("--source-root", required=True, type=Path)
    stage_parser.add_argument("--game-root", required=True, type=Path)

    restore_parser = subparsers.add_parser(
        "restore", help="restore an exact complete staged game tree"
    )
    restore_parser.add_argument("manifest", type=Path)
    restore_parser.add_argument("--source-root", required=True, type=Path)
    restore_parser.add_argument("--game-root", required=True, type=Path)

    remove_parser = subparsers.add_parser(
        "remove", help="remove an exact receipt-validated sparse overlay"
    )
    remove_parser.add_argument("manifest", type=Path)
    remove_parser.add_argument("--source-root", required=True, type=Path)
    remove_parser.add_argument("--overlay-root", required=True, type=Path)

    replay_parser = subparsers.add_parser(
        "replay", help="reproduce a sparse overlay from an exact ordinary receipt"
    )
    replay_parser.add_argument("receipt", type=Path)
    replay_parser.add_argument("--source-root", required=True, type=Path)
    replay_parser.add_argument("--output-root", required=True, type=Path)

    remove_receipt_parser = subparsers.add_parser(
        "remove-receipt",
        help="remove an exact sparse overlay using an external ordinary receipt",
    )
    remove_receipt_parser.add_argument("receipt", type=Path)
    remove_receipt_parser.add_argument("--source-root", required=True, type=Path)
    remove_receipt_parser.add_argument("--overlay-root", required=True, type=Path)

    compose_parser = subparsers.add_parser(
        "compose", help="compose exactly two manifests or report a byte conflict"
    )
    compose_parser.add_argument("left", type=Path)
    compose_parser.add_argument("right", type=Path)
    compose_parser.add_argument("--source-root", required=True, type=Path)

    dry_run_parser = subparsers.add_parser(
        "dry-run", help="validate one manifest and report affected byte ranges"
    )
    dry_run_parser.add_argument("manifest", type=Path)
    dry_run_parser.add_argument("--source-root", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "inspect":
            return _inspect(args)
        if args.command == "scan":
            return _scan(args)
        if args.command == "scan-payload-targets":
            return _scan_payload_targets(args)
        if args.command == "inspect-anm":
            return _inspect_anm(args)
        if args.command == "scan-anm":
            return _scan_anm(args)
        if args.command == "compose":
            composed = compose_manifests(
                load_manifest(args.left),
                load_manifest(args.right),
                args.source_root,
            )
            print(json.dumps(composed, indent=2, sort_keys=True))
            return 0
        if args.command == "replay":
            receipt = replay_receipt(
                args.receipt, args.source_root, args.output_root
            )
            print(json.dumps(receipt, indent=2))
            return 0
        if args.command == "remove-receipt":
            receipt = remove_receipt(
                args.receipt, args.source_root, args.overlay_root
            )
            print(json.dumps(receipt, indent=2))
            return 0
        manifest = load_manifest(args.manifest)
        if args.command == "dry-run":
            report = dry_run_manifest(manifest, args.source_root)
            print(json.dumps(report, indent=2))
            return 0
        if args.command == "apply":
            receipt = apply_manifest(
                manifest, args.source_root, args.output_root, force=args.force
            )
        elif args.command == "stage":
            receipt = stage_manifest(manifest, args.source_root, args.game_root)
        elif args.command == "restore":
            receipt = restore_manifest(
                manifest, args.source_root, args.game_root
            )
        else:
            receipt = remove_manifest(manifest, args.source_root, args.overlay_root)
        print(json.dumps(receipt, indent=2))
        return 0
    except ManifestCompositionConflict as error:
        print(
            json.dumps(error.report, sort_keys=True, separators=(",", ":")),
            file=sys.stderr,
        )
        return 2
    except (
        OSError,
        AnmFormatError,
        DatFormatError,
        ManifestError,
        IndexError,
        ValueError,
    ) as error:
        print(f"ablpc-mod: {error}", file=sys.stderr)
        return 2


def _inspect(args: argparse.Namespace) -> int:
    level = LevelDat.from_path(args.path)
    summary = level.summary()
    if args.records:
        summary[f"{args.records}_records"] = [
            {
                "index": record.index,
                "offset": record.offset,
                "candidate_center_components": [
                    record.center_component_00,
                    record.center_component_04,
                    record.center_component_08,
                ],
                "field_0c_signed": record.field_0c_signed,
                "flags": record.flags,
                "payload_offset_candidate": record.payload_offset_candidate,
            }
            for record in level.records(args.records)
        ]
    if args.payload_targets:
        references = level.supported_payload_target_references(args.payload_targets)
        reference_counts: dict[int, int] = {}
        for reference in references:
            reference_counts[reference.target_offset] = (
                reference_counts.get(reference.target_offset, 0) + 1
            )
        blocks = [
            level.positive_payload_target_block(offset)
            for offset in sorted(reference_counts)
        ]
        summary[f"{args.payload_targets}_payload_target_references"] = [
            {
                "record_index": reference.record_index,
                "record_offset": reference.record_offset,
                "payload_offset": reference.payload_offset,
                "target_field_offset": reference.target_field_offset,
                "target_offset": reference.target_offset,
            }
            for reference in references
        ]
        summary[f"{args.payload_targets}_positive_payload_target_blocks"] = [
            {
                "offset": block.offset,
                "reference_count": reference_counts[block.offset],
                "entry_count": block.entry_count,
                "entries_offset": block.entries_offset,
                "command_stream_offset": block.command_stream_offset,
                "command_groups": [
                    {
                        "index": group.index,
                        "offset": group.offset,
                        "mode": group.mode,
                        "item_count": group.item_count,
                        "item_size": group.item_size,
                        "items_offset": group.items_offset,
                        "end_offset": group.end_offset,
                    }
                    for group in block.command_groups
                ],
                "terminator_offset": block.terminator_offset,
                "end_offset": block.end_offset,
            }
            for block in blocks
        ]
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"path: {args.path}")
        for key, value in summary.items():
            if key != "top_records":
                print(f"{key}: {value}")
        print("top_records:")
        for record in level.top_records:
            print(
                f"  [{record.index}] offset=0x{record.offset:x} "
                f"type={record.type_id} count={record.count} size={record.size}"
            )
    return 0


def _scan(args: argparse.Namespace) -> int:
    paths = sorted(
        path
        for path in args.root.rglob("*.DAT")
        if path.is_file() and path.name.upper().startswith("LEVEL")
    )
    if not paths:
        raise ManifestError(f"no LEVEL*.DAT files found below {args.root}")
    failures = 0
    for path in paths:
        try:
            parsed = LevelDat.from_path(path)
            print(
                f"ok {path}: primary={len(parsed.primary_records)} "
                f"secondary={len(parsed.secondary_records)} sha256={parsed.sha256}"
            )
        except (OSError, DatFormatError) as error:
            failures += 1
            print(f"error {path}: {error}", file=sys.stderr)
    print(f"scanned={len(paths)} failures={failures}")
    return 1 if failures else 0


def _scan_payload_targets(args: argparse.Namespace) -> int:
    paths = sorted(
        path
        for path in args.root.rglob("*.DAT")
        if path.is_file() and path.name.upper().startswith("LEVEL")
    )
    if not paths:
        raise ManifestError(f"no LEVEL*.DAT files found below {args.root}")

    files: list[dict[str, object]] = []
    totals = {
        "files_scanned": len(paths),
        "files_with_dispatch_0x49_records": 0,
        "matching_records": 0,
        "parsed_references": 0,
        "unique_positive_target_blocks": 0,
        "errors": 0,
    }
    for path in paths:
        parsed = LevelDat.from_path(path)
        references = []
        errors = []
        for section in ("primary", "secondary"):
            for record in parsed.records(section):
                if (
                    record.flags & SUPPORTED_SCENE_DISPATCH_MASK
                ) != SUPPORTED_SCENE_DISPATCH_VALUE:
                    continue
                try:
                    reference = parsed.payload_target_reference(section, record.index)
                    parsed.positive_payload_target_block(reference.target_offset)
                    references.append(reference)
                except (DatFormatError, IndexError, ValueError) as error:
                    errors.append(
                        {
                            "section": section,
                            "record_index": record.index,
                            "record_offset": record.offset,
                            "flags": record.flags,
                            "error": str(error),
                        }
                    )
        matching_records = len(references) + len(errors)
        unique_targets = len({reference.target_offset for reference in references})
        if matching_records:
            totals["files_with_dispatch_0x49_records"] += 1
        totals["matching_records"] += matching_records
        totals["parsed_references"] += len(references)
        totals["unique_positive_target_blocks"] += unique_targets
        totals["errors"] += len(errors)
        files.append(
            {
                "path": path.relative_to(args.root).as_posix(),
                "sha256": parsed.sha256,
                "matching_records": matching_records,
                "parsed_references": len(references),
                "unique_positive_target_blocks": unique_targets,
                "errors": errors,
            }
        )

    result = {
        "dispatch_mask": SUPPORTED_SCENE_DISPATCH_MASK,
        "dispatch_value": SUPPORTED_SCENE_DISPATCH_VALUE,
        "totals": totals,
        "files": files,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for entry in files:
            if entry["matching_records"]:
                print(
                    f"{entry['path']}: matching={entry['matching_records']} "
                    f"parsed={entry['parsed_references']} "
                    f"targets={entry['unique_positive_target_blocks']} "
                    f"errors={len(entry['errors'])}"
                )
        print(" ".join(f"{key}={value}" for key, value in totals.items()))
    return 1 if totals["errors"] else 0


def _inspect_anm(args: argparse.Namespace) -> int:
    anm = AnmFile.from_path(args.path)
    summary = anm.summary()
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"path: {args.path}")
        print(f"sha256: {anm.sha256}")
        print(f"file_size: {len(anm.data)}")
        print(
            f"header: field_00={anm.field_00} offset_count={anm.offset_count} "
            f"field_04={anm.field_04} field_06={anm.field_06}"
        )
        print(
            f"offset_table: 0x{ANM_HEADER_SIZE:x}..0x{anm.offset_table_end:x}"
        )
        for reference in anm.offset_references:
            value = (
                "null"
                if reference.relative_offset is None
                else f"0x{reference.relative_offset:x}"
            )
            print(
                f"  [{reference.index}] field=0x{reference.field_offset:x} "
                f"relative={value}"
            )
        first = anm.first_referenced_record
        if first is None:
            print("first_referenced_record: none")
        else:
            print(
                f"first_referenced_record: offset=0x{first.offset:x} "
                f"item_count={first.item_count} "
                f"items=0x{first.items_offset:x}..0x{first.items_end_offset:x} "
                f"minus_two_indices={list(first.minus_two_indices)}"
            )
    return 0


def _scan_anm(args: argparse.Namespace) -> int:
    paths = sorted(
        path
        for path in args.root.rglob("*")
        if path.is_file() and path.suffix.upper() == ".ANM"
    )
    if not paths:
        raise ManifestError(f"no .ANM files found below {args.root}")

    files: list[dict[str, object]] = []
    failures = 0
    for path in paths:
        relative_path = path.relative_to(args.root).as_posix()
        try:
            anm = AnmFile.from_path(path)
            files.append({"path": relative_path, **anm.summary()})
            if not args.json:
                print(
                    f"ok {relative_path}: offsets={anm.offset_count} "
                    f"size={len(anm.data)} sha256={anm.sha256}"
                )
        except (OSError, AnmFormatError) as error:
            failures += 1
            files.append({"path": relative_path, "error": str(error)})
            if not args.json:
                print(f"error {relative_path}: {error}", file=sys.stderr)

    result = {
        "format_scope": "PC .ANM first-level walk at executable 0x00444B70",
        "files_scanned": len(paths),
        "failures": failures,
        "files": files,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"scanned={len(paths)} failures={failures}")
    return 1 if failures else 0
