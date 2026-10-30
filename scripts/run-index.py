#!/usr/bin/env python3
"""Cross-reference ``dynamic/wine/RUN-*`` receipt directories with Vault notes.

Every runtime tool in this repository writes a machine-readable receipt into a
``dynamic/wine/RUN-<KIND>-<stamp>/`` directory. Nothing until now tied those
directories back to the ``Vault/`` notes that cite them, so an agent had to
grep the Vault to learn which run backs which experiment, and a run that no
note cites (evidence with no home) or a run id cited by a note but absent from
disk (a dangling citation) were both invisible.

This tool only reads. It extracts what each receipt actually records -- it does
not infer, normalize away, or repair disagreements between receipt shapes. A
directory whose ``metadata.json`` is missing or malformed is reported as
``unreadable`` with the reason rather than skipped or crashed on, because a
receipt that cannot be read is itself an audit finding.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import evidence_lib as ev


TOOL = "run-index"
TOOL_VERSION = "1.0.0"
INDEX_SCHEMA_VERSION = 1

RUN_ROOT = "dynamic/wine"
VAULT_DIR = "Vault"
DEFAULT_OUT = "reports/run-index.json"

# Run ids are ``RUN-<KIND tokens>-<YYYYMMDD>-<HHMMSS>[-<SUFFIX tokens>]``; the
# on-disk directory names carry both forms (``RUN-GDB-20260813-101022`` and
# ``RUN-WINE-20260811-232606-WINDOW-PROBE``).
RUN_ID_RE = re.compile(
    r"RUN-[A-Z0-9]+(?:-[A-Z0-9]+)*-(\d{8})-(\d{6})(?:-[A-Z0-9]+)*"
)
RUN_DIR_RE = re.compile(
    r"^RUN-(?P<kind>[A-Z0-9]+(?:-[A-Z0-9]+)*)"
    r"-(?P<day>\d{8})-(?P<time>\d{6})"
    r"(?:-(?P<suffix>[A-Z0-9]+(?:-[A-Z0-9]+)*))?$"
)

# Every ``sha256`` the receipt shapes in this repository use to name the
# executable under test, in the order they are trusted when several are present.
EXE_SHA_PATHS: tuple[tuple[str, ...], ...] = (
    ("executable_sha256",),
    ("ownership", "exe_sha256"),
    ("binary_sha256",),
    ("target", "sha256"),
    ("spec", "target", "expected_exe_sha256"),
)

# Receipt-recorded wall-clock fields, by the key each tool family uses.
TIMESTAMP_KEYS = (
    "started",
    "ended",
    "capture_sequence_started",
    "capture_sequence_ended",
    "started_at",
    "frozen_at",
    "resumed_at",
    "pause_started",
    "pause_ended",
)

MAX_INVENTORY_FILES = 512
MAX_MARKDOWN_CITATIONS = 4


class RunIndexError(Exception):
    """Raised for a refusal-worthy condition (bad root, unknown run id)."""

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(detail or reason)
        self.reason = reason
        self.detail = detail


# --------------------------------------------------------------------------
# Defensive receipt reading
# --------------------------------------------------------------------------


def read_json_file(path: Path) -> tuple[object | None, str | None]:
    """Return ``(parsed, error)``; never raises for a bad or absent file."""

    if not path.exists():
        return None, "absent"
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return None, f"unreadable: {exc}"
    if not raw.strip():
        return None, "empty"
    try:
        return json.loads(raw), None
    except json.JSONDecodeError as exc:
        return None, f"malformed JSON: {exc}"


def dig(data: object, *keys: str):
    """Walk a nested mapping, returning ``None`` at the first missing hop."""

    node = data
    for key in keys:
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def parse_run_id(name: str) -> dict | None:
    """Split a run directory name into kind/stamp parts, or ``None``."""

    match = RUN_DIR_RE.match(name)
    if not match:
        return None
    day = match.group("day")
    clock = match.group("time")
    return {
        "kind": match.group("kind"),
        "suffix": match.group("suffix"),
        "stamp": f"{day}-{clock}",
        "stamp_iso": (
            f"{day[0:4]}-{day[4:6]}-{day[6:8]}"
            f"T{clock[0:2]}:{clock[2:4]}:{clock[4:6]}"
        ),
    }


def _environment_text(value: object) -> str | None:
    """Flatten the two recorded ``environment`` shapes into one string."""

    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        parts = [
            f"{key} {sub}"
            for key, sub in value.items()
            if isinstance(sub, (str, int, float))
        ]
        return "; ".join(parts) or None
    return None


def _file_inventory(run_dir: Path, *, hashes: bool) -> tuple[list[dict], int, list[str]]:
    entries: list[dict] = []
    problems: list[str] = []
    total = 0
    try:
        names = sorted(p.name for p in run_dir.iterdir())
    except OSError as exc:
        return [], 0, [f"inventory failed: {exc}"]
    for name in names[:MAX_INVENTORY_FILES]:
        path = run_dir / name
        record: dict = {"name": name}
        try:
            if path.is_dir():
                record["kind"] = "directory"
                entries.append(record)
                continue
            size = path.stat().st_size
        except OSError as exc:
            record["error"] = str(exc)
            entries.append(record)
            problems.append(f"{name}: {exc}")
            continue
        record["size_bytes"] = size
        total += size
        if hashes:
            try:
                record["sha256"] = ev.sha256_file(path)
            except OSError as exc:
                record["sha256"] = None
                record["error"] = str(exc)
                problems.append(f"{name}: {exc}")
        entries.append(record)
    if len(names) > MAX_INVENTORY_FILES:
        problems.append(
            f"inventory truncated at {MAX_INVENTORY_FILES} of {len(names)} entries"
        )
    return entries, total, problems


def _count_lines(path: Path) -> int | None:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return sum(1 for line in handle if line.strip())
    except OSError:
        return None


def _normalize_address(value: object) -> str | None:
    """Render a spec address as ``0x`` + uppercase hex, or ``None``."""

    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = ev.parse_hex_u64(value)
        except ValueError:
            return None
    else:
        return None
    if parsed < 0:
        return None
    return f"0x{parsed:08X}"


def spec_addresses(spec: object) -> list[str]:
    """Watchpoint and breakpoint addresses declared by a resolved spec."""

    found: list[str] = []
    for group in ("watchpoints", "breakpoints"):
        items = dig(spec, group)
        if not isinstance(items, list):
            continue
        for item in items:
            address = _normalize_address(dig(item, "address"))
            if address and address not in found:
                found.append(address)
    return found


def spec_file_offsets(spec: object) -> list[str]:
    """Record-plan file offsets a resolved spec pins, if it pins any."""

    offsets: list[str] = []
    candidates = dig(spec, "direct3d_batch_capture", "candidate_record_offsets")
    if not isinstance(candidates, list):
        return offsets
    for value in candidates:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            continue
        text = f"0x{value:04X}"
        if text not in offsets:
            offsets.append(text)
    return offsets


def extract_run(run_dir: Path, *, root: Path, hashes: bool = True) -> dict:
    """Extract one run directory's record, tolerating any receipt defect."""

    run_id = run_dir.name
    parts = parse_run_id(run_id) or {}
    files, total_size, file_problems = _file_inventory(run_dir, hashes=hashes)
    present = {entry["name"] for entry in files}

    metadata, meta_error = read_json_file(run_dir / "metadata.json")
    result, result_error = read_json_file(run_dir / "result.json")
    resolved, spec_error = read_json_file(run_dir / "spec.resolved.json")
    if not isinstance(metadata, dict):
        if metadata is not None:
            meta_error = f"metadata.json is a {type(metadata).__name__}, not an object"
        metadata = {}
    if not isinstance(result, dict):
        if result is not None:
            result_error = f"result.json is a {type(result).__name__}, not an object"
        result = {}
    if not isinstance(resolved, dict):
        if resolved is not None:
            spec_error = f"spec.resolved.json is a {type(resolved).__name__}, not an object"
        resolved = None

    unreadable = None
    if meta_error:
        unreadable = {"file": "metadata.json", "reason": meta_error}

    exe_sha = None
    exe_sha_source = None
    for path_keys in EXE_SHA_PATHS:
        value = dig(metadata, *path_keys)
        if isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{64}", value):
            exe_sha = value.lower()
            exe_sha_source = "metadata." + ".".join(path_keys)
            break

    timestamps: dict[str, object] = {
        "stamp": parts.get("stamp"),
        "stamp_iso": parts.get("stamp_iso"),
    }
    for key in TIMESTAMP_KEYS:
        value = metadata.get(key)
        if isinstance(value, str) and value:
            timestamps[key] = value
    for key in ("time_window_start", "time_window_end"):
        value = result.get(key) or metadata.get(key)
        if isinstance(value, str) and value:
            timestamps[key] = value

    completion = result.get("completion")
    if not isinstance(completion, dict):
        completion = {}

    accepted = completion.get("accepted")
    if not isinstance(accepted, bool):
        accepted = metadata.get("accepted") if isinstance(metadata.get("accepted"), bool) else None
    completed = completion.get("completed")
    if not isinstance(completed, bool):
        completed = None

    stops_observed = completion.get("stops_observed")
    if isinstance(stops_observed, bool) or not isinstance(stops_observed, int):
        stops_observed = None
    stop_records = None
    if "stops.jsonl" in present:
        stop_records = _count_lines(run_dir / "stops.jsonl")

    spec_source = resolved if resolved is not None else metadata.get("spec")

    experiment_id = None
    for key in ("experiment_id", "experiment"):
        value = metadata.get(key)
        if isinstance(value, str) and value:
            experiment_id = value
            break
    if experiment_id is None:
        value = dig(spec_source, "experiment_id")
        if isinstance(value, str) and value:
            experiment_id = value

    record = {
        "run_id": run_id,
        "kind": parts.get("kind"),
        "suffix": parts.get("suffix"),
        "path": run_dir.resolve().relative_to(root.resolve()).as_posix()
        if _is_relative(run_dir, root)
        else str(run_dir),
        "recognized_name": bool(parts),
        "unreadable": unreadable,
        "receipt_errors": {
            key: value
            for key, value in (
                ("metadata.json", meta_error),
                ("result.json", result_error),
                ("spec.resolved.json", spec_error),
            )
            if value and value != "absent"
        },
        "run_id_matches_metadata": (
            metadata.get("run_id") == run_id if "run_id" in metadata else None
        ),
        "tool": _string_or_none(
            metadata.get("tool")
            or result.get("tool")
            or metadata.get("tracer")
            or metadata.get("recorder")
        ),
        "tool_version": _string_or_none(
            metadata.get("tool_version")
            or result.get("tool_version")
            or metadata.get("tracer_version")
            or metadata.get("recorder_version")
        ),
        "schema_version": metadata.get("schema_version", metadata.get("schema")),
        "spec_schema_version": result.get("spec_schema_version", dig(spec_source, "schema_version")),
        "experiment_id": experiment_id,
        "timestamps": timestamps,
        "target_exe_sha256": exe_sha,
        "target_exe_sha256_source": exe_sha_source,
        "status": _string_or_none(metadata.get("status")),
        "accepted": accepted,
        "completed": completed,
        "stop_reason": _string_or_none(completion.get("stop_reason")),
        "stops_observed": stops_observed,
        "stop_records": stop_records,
        "environment": _environment_text(metadata.get("environment")),
        "environment_version": _string_or_none(metadata.get("environment_version")),
        "debugger": _string_or_none(metadata.get("debugger")),
        "working_directory": _string_or_none(metadata.get("working_directory")),
        "addresses": spec_addresses(spec_source),
        "file_offsets": spec_file_offsets(spec_source),
        "files": files,
        "file_count": len(files),
        "total_size_bytes": total_size,
        "file_problems": file_problems,
        "cited_by": [],
    }
    return record


def _is_relative(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _string_or_none(value: object) -> str | None:
    if isinstance(value, str) and value:
        return value
    return None


# --------------------------------------------------------------------------
# Vault citation scan
# --------------------------------------------------------------------------


def scan_vault_citations(vault: Path, *, root: Path) -> dict[str, list[str]]:
    """Map every run id mentioned in a Vault note to the notes citing it.

    Both plain text (``dynamic/wine/RUN-GDB-...``, `` `RUN-GDB-...` ``) and
    wikilink (``[[... RUN-GDB-...]]``) forms are found, because the scan runs
    over the raw note text rather than over parsed link targets.
    """

    citations: dict[str, set[str]] = {}
    if not vault.is_dir():
        return {}
    for note in sorted(vault.rglob("*.md")):
        try:
            text = note.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        found = set(match.group(0) for match in RUN_ID_RE.finditer(text))
        if not found:
            continue
        rel = (
            note.resolve().relative_to(root.resolve()).as_posix()
            if _is_relative(note, root)
            else str(note)
        )
        for run_id in found:
            citations.setdefault(run_id, set()).add(rel)
    return {key: sorted(value) for key, value in sorted(citations.items())}


# --------------------------------------------------------------------------
# Index build
# --------------------------------------------------------------------------


def build_index(root: Path, *, hashes: bool = True) -> dict:
    run_root = root / RUN_ROOT
    runs: list[dict] = []
    if run_root.is_dir():
        for entry in sorted(run_root.iterdir()):
            if not entry.is_dir() or not entry.name.startswith("RUN-"):
                continue
            runs.append(extract_run(entry, root=root, hashes=hashes))

    citations = scan_vault_citations(root / VAULT_DIR, root=root)
    on_disk = {record["run_id"] for record in runs}
    for record in runs:
        record["cited_by"] = citations.get(record["run_id"], [])

    dangling = [
        {"run_id": run_id, "cited_by": notes}
        for run_id, notes in citations.items()
        if run_id not in on_disk
    ]
    uncited = [record["run_id"] for record in runs if not record["cited_by"]]

    kinds: dict[str, int] = {}
    for record in runs:
        kinds[record["kind"] or "UNRECOGNIZED"] = kinds.get(record["kind"] or "UNRECOGNIZED", 0) + 1

    return {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "index_schema_version": INDEX_SCHEMA_VERSION,
        "root": str(root),
        "run_root": RUN_ROOT,
        "file_hashes_included": hashes,
        "summary": {
            "run_directories": len(runs),
            "unreadable_metadata": sum(1 for r in runs if r["unreadable"]),
            "unrecognized_names": sum(1 for r in runs if not r["recognized_name"]),
            "kinds": dict(sorted(kinds.items())),
            "notes_citing_runs": len({note for notes in citations.values() for note in notes}),
            "run_ids_cited": len(citations),
            "uncited_run_directories": len(uncited),
            "dangling_citations": len(dangling),
            "total_size_bytes": sum(r["total_size_bytes"] for r in runs),
        },
        "runs": runs,
        "uncited_run_directories": uncited,
        "dangling_citations": dangling,
    }


def _md_cell(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def markdown_table(index: dict) -> str:
    summary = index["summary"]
    lines = [
        "# Run index",
        "",
        f"Generated by `{index['tool']}` {index['tool_version']} "
        f"(index schema {index['index_schema_version']}).",
        "",
        f"- Run directories: {summary['run_directories']}",
        f"- Unreadable metadata: {summary['unreadable_metadata']}",
        f"- Uncited run directories: {summary['uncited_run_directories']}",
        f"- Dangling citations: {summary['dangling_citations']}",
        f"- Total receipt bytes: {summary['total_size_bytes']}",
        "",
        "| run id | kind | tool | version | status | accepted | stops | files | bytes | cited by |",
        "| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for record in index["runs"]:
        stops = record["stops_observed"]
        if stops is None:
            stops = record["stop_records"]
        cited = record["cited_by"]
        # The JSON index holds every citing note; the table shows enough to
        # find the evidence's home without becoming unreadably wide.
        shown = ", ".join(f"`{path}`" for path in cited[:MAX_MARKDOWN_CITATIONS])
        if len(cited) > MAX_MARKDOWN_CITATIONS:
            shown += f", +{len(cited) - MAX_MARKDOWN_CITATIONS} more"
        cited_cell = shown or "(none)"
        status = record["status"]
        if record["unreadable"]:
            status = f"unreadable: {record['unreadable']['reason']}"
        lines.append(
            "| "
            + " | ".join(
                _md_cell(value)
                for value in (
                    f"`{record['run_id']}`",
                    record["kind"],
                    record["tool"],
                    record["tool_version"],
                    status,
                    record["accepted"],
                    stops,
                    record["file_count"],
                    record["total_size_bytes"],
                    cited_cell,
                )
            )
            + " |"
        )
    if index["dangling_citations"]:
        lines += ["", "## Dangling citations", "", "| run id | cited by |", "| --- | --- |"]
        for item in index["dangling_citations"]:
            lines.append(
                f"| `{item['run_id']}` | "
                + ", ".join(f"`{path}`" for path in item["cited_by"])
                + " |"
            )
    lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def capabilities() -> dict:
    return {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "index_schema_version": INDEX_SCHEMA_VERSION,
        "verbs": ["build", "orphans", "show"],
        "reads": [f"{RUN_ROOT}/RUN-*", f"{VAULT_DIR}/**/*.md"],
        "writes": ["the --out JSON index", "the --markdown table"],
        "writes_target_memory": False,
        "modifies_run_directories": False,
        "modifies_vault_notes": False,
        "receipt_files_read": [
            "metadata.json",
            "result.json",
            "spec.resolved.json",
            "stops.jsonl",
        ],
        "citation_forms_detected": ["plain-text", "backticked", "wikilink"],
        "run_id_pattern": RUN_ID_RE.pattern,
        "integrity_checks": ["uncited_run_directories", "dangling_citations"],
        "file_hashes": "sha256 per run-directory file unless --no-hashes",
        "limits": {"max_inventory_files_per_run": MAX_INVENTORY_FILES},
        "root_override_env": "ABLPC_ROOT",
        "exit_codes": {
            "0": "ok",
            "1": "tool-negative (integrity problems found)",
            "2": "usage",
            "3": "refusal",
        },
    }


def _refuse(reason: str, detail: str = "") -> int:
    print(json.dumps({"refused": True, "tool": TOOL, "reason": reason, "detail": detail}))
    return ev.EXIT_REFUSAL


def _resolve_root() -> Path:
    root = ev.repo_root()
    if not root.is_dir():
        raise RunIndexError("root_missing", f"{root} is not a directory")
    return root


def cmd_build(args: argparse.Namespace) -> int:
    root = _resolve_root()
    index = build_index(root, hashes=not args.no_hashes)
    payload = json.dumps(index, indent=2, sort_keys=False) + "\n"

    if args.out == "-":
        sys.stdout.write(payload)
        return ev.EXIT_OK

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = root / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(payload, encoding="utf-8")

    markdown_path = None
    if args.markdown:
        markdown_path = Path(args.markdown)
        if not markdown_path.is_absolute():
            markdown_path = root / markdown_path
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(markdown_table(index), encoding="utf-8")

    print(json.dumps({
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "index_path": str(out_path),
        "index_bytes": len(payload.encode("utf-8")),
        "markdown_path": str(markdown_path) if markdown_path else None,
        "summary": index["summary"],
    }, indent=2))
    return ev.EXIT_OK


def cmd_orphans(args: argparse.Namespace) -> int:
    root = _resolve_root()
    index = build_index(root, hashes=False)
    uncited = [
        {
            "run_id": record["run_id"],
            "kind": record["kind"],
            "path": record["path"],
            "tool": record["tool"],
            "total_size_bytes": record["total_size_bytes"],
        }
        for record in index["runs"]
        if not record["cited_by"]
    ]
    payload = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "uncited_run_directories": {
            "problem": "run directory cited by no Vault note (evidence with no home)",
            "count": len(uncited),
            "runs": uncited,
        },
        "dangling_citations": {
            "problem": "run id cited by a Vault note with no directory on disk",
            "count": len(index["dangling_citations"]),
            "citations": index["dangling_citations"],
        },
        "clean": not uncited and not index["dangling_citations"],
    }
    print(json.dumps(payload, indent=2))
    return ev.EXIT_OK if payload["clean"] else ev.EXIT_TOOL_NEGATIVE


def cmd_show(args: argparse.Namespace) -> int:
    root = _resolve_root()
    if ".." in Path(args.run).parts or Path(args.run).is_absolute():
        return _refuse("bad_run_id", f"{args.run!r} is not a bare run directory name")
    run_dir = root / RUN_ROOT / args.run
    if not run_dir.is_dir():
        return _refuse("run_not_found", f"{run_dir} is not a directory")
    record = extract_run(run_dir, root=root, hashes=not args.no_hashes)
    citations = scan_vault_citations(root / VAULT_DIR, root=root)
    record["cited_by"] = citations.get(record["run_id"], [])
    print(json.dumps(record, indent=2))
    return ev.EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Index RUN-* receipt directories against Vault citations",
    )
    parser.add_argument("--capabilities", action="store_true")
    sub = parser.add_subparsers(dest="command")

    build = sub.add_parser("build", help="write the JSON (and optional Markdown) index")
    build.add_argument("--out", default=DEFAULT_OUT, help="'-' writes the index to stdout")
    build.add_argument("--markdown", help="also write a human-readable Markdown table")
    build.add_argument("--no-hashes", action="store_true")
    build.set_defaults(func=cmd_build)

    orphans = sub.add_parser("orphans", help="report both directions of citation breakage")
    orphans.set_defaults(func=cmd_orphans)

    show = sub.add_parser("show", help="print one run's extracted record")
    show.add_argument("--run", required=True)
    show.add_argument("--no-hashes", action="store_true")
    show.set_defaults(func=cmd_show)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.capabilities:
        print(json.dumps(capabilities(), indent=2, sort_keys=True))
        return ev.EXIT_OK
    if not getattr(args, "command", None):
        parser.print_usage(sys.stderr)
        print(json.dumps({"error": "usage", "detail": "a verb is required"}))
        return ev.EXIT_USAGE
    try:
        return args.func(args)
    except RunIndexError as exc:
        return _refuse(exc.reason, exc.detail)


if __name__ == "__main__":
    sys.exit(main())
