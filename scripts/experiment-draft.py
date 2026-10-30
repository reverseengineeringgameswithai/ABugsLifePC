#!/usr/bin/env python3
"""Draft an experiment note pre-filled from the run receipts that back it.

``scripts/new-experiment.py`` scaffolds an empty note: ``binary_sha256``,
``environment``, ``working_directory``, ``artifacts``, ``addresses`` and the
rest are left blank for a human to hand-type, even though the
``dynamic/wine/RUN-*`` receipt for the run already records every one of those
values. Hand transcription across that gap has produced real audit failures in
this project, so this tool closes it: it reads the receipts and writes the
facts, leaving the author to write only prose.

The generated note deliberately asserts nothing. It transcribes receipt fields
and marks every section a human must still write with an explicit ``TODO:``
line, so a reviewer can see at a glance what is unwritten. ``result`` stays
``pending`` and the Interpretation section stays empty by construction: a
generator has no evidence with which to interpret anything.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import evidence_lib as ev
import note_utils


TOOL = "experiment-draft"
TOOL_VERSION = "1.0.0"

EXP_ID_RE = re.compile(r"^EXP-\d{8}-\d{3}$")

# Receipt files worth naming individually in ``artifacts``; anything else in a
# run directory is still covered by the directory entry itself.
NOTABLE_FILES = (
    "metadata.json",
    "result.json",
    "spec.resolved.json",
    "stops.jsonl",
    "experiment.md",
    "debugger-evidence.txt",
    "curation.txt",
    "manifest-receipt.json",
    "input-receipt.txt",
    "position-trace.tsv",
    "selected-events.tsv",
    "frame-hashes.txt",
    "write-receipts.txt",
    "bugs.log",
)

# A YAML plain scalar must not be mistaken for another type or start a
# structure. These characters force a double-quoted scalar anywhere in the
# value; the START set additionally forces one only in first position, where
# it would otherwise be read as an indicator.
YAML_UNSAFE_ANYWHERE = set(":#\"'{}[]\n\t\\")
YAML_UNSAFE_AT_START = set("-?,|>*&!%@`") | set(" \t")
YAML_KEYWORDS = {
    "true", "false", "yes", "no", "on", "off", "null", "none", "~", "y", "n",
}


def _load_run_index():
    """Load the sibling ``run-index.py`` (hyphenated, so not importable)."""

    path = Path(__file__).resolve().parent / "run-index.py"
    spec = importlib.util.spec_from_file_location("_ablpc_run_index", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


run_index = _load_run_index()


class Refusal(Exception):
    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(detail or reason)
        self.reason = reason
        self.detail = detail


# --------------------------------------------------------------------------
# YAML emission (stdlib only; must survive yaml.safe_load in vault-lint.py)
# --------------------------------------------------------------------------


def yaml_scalar(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    text = str(value)
    if not text:
        return ""
    unsafe = (
        any(char in YAML_UNSAFE_ANYWHERE for char in text)
        or text[0] in YAML_UNSAFE_AT_START
        or text != text.strip()
        or text.lower() in YAML_KEYWORDS
    )
    if unsafe:
        return json.dumps(text, ensure_ascii=False)
    return text


def yaml_key(key: str, value: object) -> str:
    """``key: value``, or a bare ``key:`` when the receipts recorded nothing."""

    return f"{key}: {yaml_scalar(value)}".rstrip()


def yaml_block(key: str, values: list[str]) -> str:
    if not values:
        return f"{key}: []"
    lines = [f"{key}:"]
    lines += [f"  - {yaml_scalar(value)}" for value in values]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Receipt gathering
# --------------------------------------------------------------------------


def gather_runs(run_ids: list[str], root: Path) -> list[dict]:
    """Extract every requested run, refusing rather than drafting blanks."""

    records: list[dict] = []
    seen: set[str] = set()
    for run_id in run_ids:
        if run_id in seen:
            continue
        seen.add(run_id)
        if Path(run_id).is_absolute() or ".." in Path(run_id).parts or "/" in run_id:
            raise Refusal("bad_run_id", f"{run_id!r} is not a bare run directory name")
        run_dir = root / run_index.RUN_ROOT / run_id
        if not run_dir.is_dir():
            raise Refusal(
                "run_not_found",
                f"{run_index.RUN_ROOT}/{run_id} is not a directory under {root}",
            )
        record = run_index.extract_run(run_dir, root=root, hashes=True)
        if record["unreadable"]:
            raise Refusal(
                "metadata_unreadable",
                f"{run_id}: {record['unreadable']['file']} "
                f"{record['unreadable']['reason']}",
            )
        records.append(record)
    if not records:
        raise Refusal("no_runs", "at least one --run is required")
    return records


def _distinct(records: list[dict], key: str) -> list[str]:
    values: list[str] = []
    for record in records:
        value = record.get(key)
        if isinstance(value, str) and value and value not in values:
            values.append(value)
    return values


def _joined(records: list[dict], key: str) -> str:
    return "; ".join(_distinct(records, key))


def environment_version_text(records: list[dict]) -> str:
    """Prefer the receipt's own ``environment_version``; else its tool stamps."""

    recorded = _distinct(records, "environment_version")
    if recorded:
        return "; ".join(recorded)
    parts: list[str] = []
    for record in records:
        if record["tool"] and record["tool_version"]:
            stamp = f"{record['tool']} {record['tool_version']}"
            if record["spec_schema_version"] is not None:
                stamp += f" schema {record['spec_schema_version']}"
            if stamp not in parts:
                parts.append(stamp)
    for debugger in _distinct(records, "debugger"):
        if debugger not in parts:
            parts.append(debugger)
    return "; ".join(parts)


def configuration_text(records: list[dict]) -> str:
    parts = []
    for record in records:
        fields = []
        if record["tool"]:
            fields.append(record["tool"] + (f" {record['tool_version']}" if record["tool_version"] else ""))
        if record["spec_schema_version"] is not None:
            fields.append(f"spec schema {record['spec_schema_version']}")
        if record["addresses"]:
            fields.append(f"{len(record['addresses'])} hardware points")
        if record["status"]:
            fields.append(f"status {record['status']}")
        parts.append(f"{record['run_id']} ({', '.join(fields) or 'no tool fields recorded'})")
    return "; ".join(parts)


def artifact_paths(records: list[dict]) -> list[str]:
    paths: list[str] = []
    for record in records:
        base = record["path"]
        paths.append(base)
        present = {entry["name"] for entry in record["files"]}
        for name in NOTABLE_FILES:
            if name in present:
                paths.append(f"{base}/{name}")
    return paths


def merged_addresses(records: list[dict]) -> list[str]:
    found: list[str] = []
    for record in records:
        for address in record["addresses"]:
            if address not in found:
                found.append(address)
    return sorted(found)


def merged_file_offsets(records: list[dict]) -> list[str]:
    found: list[str] = []
    for record in records:
        for offset in record["file_offsets"]:
            if offset not in found:
                found.append(offset)
    return sorted(found)


def draft_date(records: list[dict]) -> str:
    stamps = sorted(
        record["timestamps"]["stamp_iso"]
        for record in records
        if record["timestamps"].get("stamp_iso")
    )
    if stamps:
        return stamps[0][:10]
    return note_utils.now().date().isoformat()


# --------------------------------------------------------------------------
# Note rendering
# --------------------------------------------------------------------------


def _cell(value: object) -> str:
    if value is None:
        return "not recorded"
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value).replace("|", "\\|").replace("\n", " ").strip()
    return text or "not recorded"


def run_table(records: list[dict]) -> list[str]:
    lines = [
        "| run | kind | tool | tool version | status | accepted | stops observed | stop records | spec schema |",
        "| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: |",
    ]
    for record in records:
        lines.append(
            "| "
            + " | ".join(
                _cell(value)
                for value in (
                    f"`{record['run_id']}`",
                    record["kind"],
                    record["tool"],
                    record["tool_version"],
                    record["status"],
                    record["accepted"],
                    record["stops_observed"],
                    record["stop_records"],
                    record["spec_schema_version"],
                )
            )
            + " |"
        )
    return lines


def identity_table(records: list[dict]) -> list[str]:
    lines = [
        "| run | executable sha256 | sha256 source | working directory | environment |",
        "| --- | --- | --- | --- | --- |",
    ]
    for record in records:
        lines.append(
            "| "
            + " | ".join(
                _cell(value)
                for value in (
                    f"`{record['run_id']}`",
                    f"`{record['target_exe_sha256']}`" if record["target_exe_sha256"] else None,
                    record["target_exe_sha256_source"],
                    f"`{record['working_directory']}`" if record["working_directory"] else None,
                    record["environment"],
                )
            )
            + " |"
        )
    return lines


def artifact_table(records: list[dict]) -> list[str]:
    lines = [
        "| artifact | bytes | sha256 |",
        "| --- | ---: | --- |",
    ]
    for record in records:
        for entry in record["files"]:
            if entry.get("kind") == "directory":
                continue
            digest = entry.get("sha256")
            lines.append(
                "| "
                + " | ".join(
                    _cell(value)
                    for value in (
                        f"`{record['path']}/{entry['name']}`",
                        entry.get("size_bytes"),
                        f"`{digest}`" if digest else None,
                    )
                )
                + " |"
            )
    return lines


def render_note(evidence_id: str, question: str, records: list[dict]) -> str:
    stamp = note_utils.now()
    run_ids = [record["run_id"] for record in records]
    sha_values = _distinct(records, "target_exe_sha256")
    env_values = _distinct(records, "environment")
    wd_values = _distinct(records, "working_directory")

    todos: list[str] = []
    if len(sha_values) > 1:
        todos.append(
            "TODO: the receipts record more than one executable SHA-256; "
            "state which arm used which, or split this note."
        )
    if not sha_values:
        todos.append(
            "TODO: no receipt recorded an executable SHA-256; supply it from "
            "independent evidence or say why none exists."
        )
    if len(env_values) > 1 or len(wd_values) > 1:
        todos.append(
            "TODO: the receipts record more than one environment or working "
            "directory; confirm that is intended."
        )
    blank = [
        name for name, values in (("environment", env_values),
                                  ("working_directory", wd_values))
        if not values
    ]
    if blank:
        todos.append(
            "TODO: no receipt recorded " + " or ".join(blank)
            + "; fill the key by hand rather than leaving it blank."
        )

    frontmatter = "\n".join([
        "---",
        "type: experiment",
        f"id: {evidence_id}",
        f"date: {draft_date(records)}",
        yaml_key("question", question),
        yaml_key("binary_sha256", "; ".join(sha_values)),
        yaml_key("environment", "; ".join(env_values)),
        yaml_key("environment_version", environment_version_text(records)),
        yaml_key("working_directory", "; ".join(wd_values)),
        yaml_key("configuration", configuration_text(records)),
        yaml_block("artifacts", artifact_paths(records)),
        yaml_block("addresses", merged_addresses(records)),
        yaml_block("file_offsets", merged_file_offsets(records)),
        "result: pending",
        f"created: {stamp.isoformat(timespec='seconds')}",
        f"updated: {stamp.isoformat(timespec='seconds')}",
        "tags:",
        "  - re/experiment",
        "  - re/dynamic",
        "---",
    ])

    provenance = (
        f"Generated by `scripts/{TOOL}.py` {TOOL_VERSION} from run receipts "
        + ", ".join(f"`{run_id}`" for run_id in run_ids)
        + ". Every value in the frontmatter and in the generated tables below is "
        "transcribed from those receipts. The generator asserts no "
        "interpretation and no result; each `TODO:` marks a section that is "
        "still unwritten."
    )

    body: list[str] = [
        f"# {evidence_id} - {question.strip()}",
        "",
        provenance,
        "",
        "## Question",
        "",
        question.strip(),
        "",
        "## Procedure",
        "",
        "TODO: describe what was actually done, in the order it was done, "
        "including how each run below was launched, gated, and closed.",
        "",
        "### Runs (generated from receipts)",
        "",
        *run_table(records),
        "",
        "### Identity and environment (generated from receipts)",
        "",
        *identity_table(records),
        "",
        "## Expected",
        "",
        "TODO: state the prediction that was made before these runs, and what "
        "outcome would have falsified it.",
        "",
        "## Observed",
        "",
        "TODO: state what the receipts show, citing the specific fields above.",
        "",
        "### Artifact hashes (generated from receipts)",
        "",
        *artifact_table(records),
        "",
        "## Interpretation",
        "",
        "TODO: not written. The generator transcribes receipts only and cannot "
        "interpret them.",
        "",
        "## Result",
        "",
        "Pending.",
        "",
        "TODO: not written. Replace `result: pending` in the frontmatter only "
        "once this section states an outcome backed by the evidence above.",
        "",
        "## Follow-up",
        "",
        "TODO: name the next discriminating experiment, or say that none is "
        "needed and why.",
    ]
    if todos:
        body += ["", "## Generator warnings", ""] + [f"- {item}" for item in todos]
    return frontmatter + "\n\n" + "\n".join(body) + "\n"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def capabilities() -> dict:
    return {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "verbs": ["draft"],
        "reads": [f"{run_index.RUN_ROOT}/RUN-*", "Vault/**/*.md (id allocation only)"],
        "writes": ["one new Vault/30-Experiments note"],
        "overwrites_existing_notes": False,
        "asserts_interpretation": False,
        "asserts_result": False,
        "frontmatter_keys_filled": [
            "date", "question", "binary_sha256", "environment",
            "environment_version", "working_directory", "configuration",
            "artifacts", "addresses", "file_offsets", "result",
        ],
        "emits_wikilinks": False,
        "id_allocation": "note_utils.next_dated_id",
        "root_override_env": "ABLPC_ROOT",
        "exit_codes": {"0": "ok", "2": "usage", "3": "refusal"},
    }


def _refuse(reason: str, detail: str = "") -> int:
    print(json.dumps({"refused": True, "tool": TOOL, "reason": reason, "detail": detail}))
    return ev.EXIT_REFUSAL


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Draft an experiment note pre-filled from run receipts",
    )
    parser.add_argument("--question", help="the question the experiment answers")
    parser.add_argument("--run", action="append", default=[], metavar="RUN-ID")
    parser.add_argument("--id", help="explicit EXP-YYYYMMDD-NNN (default: next free)")
    parser.add_argument("--out", help="destination path (default: Vault/30-Experiments/)")
    parser.add_argument("--stdout", action="store_true", help="print the note, write nothing")
    parser.add_argument("--capabilities", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.capabilities:
        print(json.dumps(capabilities(), indent=2, sort_keys=True))
        return ev.EXIT_OK
    if not args.question or not args.question.strip():
        parser.print_usage(sys.stderr)
        print(json.dumps({"error": "usage", "detail": "--question is required"}))
        return ev.EXIT_USAGE
    if not args.run:
        parser.print_usage(sys.stderr)
        print(json.dumps({"error": "usage", "detail": "at least one --run is required"}))
        return ev.EXIT_USAGE

    root = ev.repo_root()
    vault = root / run_index.VAULT_DIR

    try:
        records = gather_runs(args.run, root)
    except Refusal as exc:
        return _refuse(exc.reason, exc.detail)

    try:
        evidence_id = args.id or note_utils.next_dated_id("EXP", vault)
        if not EXP_ID_RE.fullmatch(evidence_id):
            return _refuse("bad_id", f"{evidence_id!r} must match EXP-YYYYMMDD-NNN")
        note_utils.require_unique(evidence_id, vault)
    except SystemExit as exc:
        return _refuse("id_collision", str(exc))

    content = render_note(evidence_id, args.question, records)
    if args.stdout:
        sys.stdout.write(content)
        return ev.EXIT_OK

    if args.out:
        path = Path(args.out)
        if not path.is_absolute():
            path = root / path
    else:
        path = vault / "30-Experiments" / f"{evidence_id} - {note_utils.slug(args.question)}.md"

    try:
        written = note_utils.write_new(path, content)
    except SystemExit as exc:
        return _refuse("note_exists", str(exc))

    print(json.dumps({
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "id": evidence_id,
        "path": str(written),
        "runs": [record["run_id"] for record in records],
        "addresses": merged_addresses(records),
        "file_offsets": merged_file_offsets(records),
        "artifacts": artifact_paths(records),
        "result": "pending",
    }, indent=2))
    return ev.EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
