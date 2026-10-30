#!/usr/bin/env python3
"""Prove a corrected claim was corrected everywhere in the vault.

This tool exists because of a repeated, expensive defect: a claim is fixed at
the first occurrence of its wording and left stale at the other five.  The
audit ratchet then rejects the packet for an inconsistency that a full-tree
sweep would have shown in one second.

Subcommands::

    sweep   --phrase TEXT [--regex]     every occurrence, with bounded context
    pair    --old TEXT --new TEXT       old vs new wording; mixed state is a
                                        tool-negative (exit 1)
    numbers --pattern REGEX             group locations by captured value; more
                                        than one distinct value is a conflict
                                        (exit 1)

Exit codes: 0 ok, 1 tool-negative, 2 usage, 3 refusal.  Refusals print
``{"refused": true, "tool": "claim-sweep", ...}``.  ``ABLPC_ROOT`` overrides the
repository root.  Output is always bounded by ``--max-hits`` and every result
reports whether it was truncated.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Iterator

TOOL = "claim-sweep"
EXIT_OK = 0
EXIT_NEGATIVE = 1
EXIT_USAGE = 2
EXIT_REFUSAL = 3

DEFAULT_PATH = "Vault"
DEFAULT_GLOB = "*.md"
DEFAULT_MAX_HITS = 200
DEFAULT_CONTEXT = 80


class RefusalError(Exception):
    """Raised when the requested sweep is outside the tool's boundary."""


def repo_root() -> Path:
    """Return the repository root, honoring the ``ABLPC_ROOT`` override."""

    override = os.environ.get("ABLPC_ROOT")
    if override:
        return Path(override).resolve()
    return Path(__file__).resolve().parents[1]


def resolve_search_path(raw: str, root: Path) -> Path:
    """Resolve the search root, refusing anything outside the repository."""

    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = candidate.resolve()
    if candidate != root and not candidate.is_relative_to(root):
        raise RefusalError(f"search path is outside the repository root: {candidate}")
    if not candidate.exists():
        raise RefusalError(f"search path does not exist: {candidate}")
    return candidate


def iter_notes(search_path: Path, glob: str) -> Iterator[Path]:
    """Yield note paths in deterministic order."""

    if search_path.is_file():
        yield search_path
        return
    yield from sorted(p for p in search_path.rglob(glob) if p.is_file())


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def bounded_context(line: str, start: int, end: int, width: int) -> str:
    """Return at most ``width`` characters of ``line`` centered on the match."""

    line = line.rstrip("\r\n")
    if width <= 0:
        return ""
    if len(line) <= width:
        return line.strip()
    span = max(end - start, 0)
    if span >= width:
        return line[start:start + width] + "..."
    lead = (width - span) // 2
    begin = max(0, start - lead)
    finish = min(len(line), begin + width)
    begin = max(0, finish - width)
    snippet = line[begin:finish]
    if begin > 0:
        snippet = "..." + snippet
    if finish < len(line):
        snippet = snippet + "..."
    return snippet


def compile_pattern(text: str, *, regex: bool, label: str) -> re.Pattern[str]:
    if not text:
        raise ValueError(f"{label} must not be empty")
    if not regex:
        return re.compile(re.escape(text))
    try:
        return re.compile(text)
    except re.error as error:
        raise ValueError(f"{label} is not a valid regular expression: {error}") from error


def scan(notes: Iterable[Path], pattern: re.Pattern[str], root: Path,
         *, context: int, group: int = 0) -> list[dict[str, Any]]:
    """Return every match as a hit record; ordering is deterministic."""

    hits: list[dict[str, Any]] = []
    for path in notes:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if pattern.search(text) is None:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            for match in pattern.finditer(line):
                value = match.group(group)
                if value is None:
                    # An optional capture group that did not participate.
                    value = match.group(0)
                hits.append(
                    {
                        "path": display_path(path, root),
                        "line": number,
                        "column": match.start() + 1,
                        "match": value,
                        "context": bounded_context(line, match.start(), match.end(), context),
                        "_span": (match.start(), match.end()),
                    }
                )
    return hits


def strip_spans(hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{key: value for key, value in hit.items() if key != "_span"} for hit in hits]


def truncate(hits: list[dict[str, Any]], max_hits: int) -> tuple[list[dict[str, Any]], bool]:
    if max_hits >= 0 and len(hits) > max_hits:
        return hits[:max_hits], True
    return list(hits), False


def note_count(hits: list[dict[str, Any]]) -> int:
    return len({hit["path"] for hit in hits})


def drop_contained(inner: list[dict[str, Any]], outer: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop ``inner`` hits whose span sits inside an ``outer`` hit on the same line."""

    spans: dict[tuple[str, int], list[tuple[int, int]]] = {}
    for hit in outer:
        spans.setdefault((hit["path"], hit["line"]), []).append(hit["_span"])
    kept = []
    for hit in inner:
        start, end = hit["_span"]
        covering = spans.get((hit["path"], hit["line"]), ())
        if any(other_start <= start and end <= other_end for other_start, other_end in covering):
            continue
        kept.append(hit)
    return kept


def run_sweep(args: argparse.Namespace, root: Path, notes: list[Path]) -> tuple[dict[str, Any], int]:
    pattern = compile_pattern(args.phrase, regex=args.regex, label="--phrase")
    hits = scan(notes, pattern, root, context=args.context)
    shown, truncated = truncate(hits, args.max_hits)
    payload = {
        "tool": TOOL,
        "subcommand": "sweep",
        "phrase": args.phrase,
        "regex": bool(args.regex),
        "notes_scanned": len(notes),
        "total_hits": len(hits),
        "notes_with_hits": note_count(hits),
        "hits": strip_spans(shown),
        "hits_truncated": truncated,
    }
    return payload, EXIT_OK


def run_pair(args: argparse.Namespace, root: Path, notes: list[Path]) -> tuple[dict[str, Any], int]:
    old_pattern = compile_pattern(args.old, regex=False, label="--old")
    new_pattern = compile_pattern(args.new, regex=False, label="--new")
    if args.old == args.new:
        raise ValueError("--old and --new must differ")
    old_hits = scan(notes, old_pattern, root, context=args.context)
    new_hits = scan(notes, new_pattern, root, context=args.context)
    # One wording can contain the other ("572" inside "572 confirmed").  The
    # longer literal wins so a contained occurrence is not double-counted.
    if len(args.new) >= len(args.old):
        overlap_rule = "old hits contained in a new occurrence are ignored"
        old_hits = drop_contained(old_hits, new_hits)
    else:
        overlap_rule = "new hits contained in an old occurrence are ignored"
        new_hits = drop_contained(new_hits, old_hits)

    old_shown, old_truncated = truncate(old_hits, args.max_hits)
    new_shown, new_truncated = truncate(new_hits, args.max_hits)
    if old_hits and new_hits:
        state = "mixed"
    elif old_hits:
        state = "old_only"
    elif new_hits:
        state = "new_only"
    else:
        state = "absent"
    payload = {
        "tool": TOOL,
        "subcommand": "pair",
        "old": args.old,
        "new": args.new,
        "overlap_rule": overlap_rule,
        "notes_scanned": len(notes),
        "state": state,
        "mixed": state == "mixed",
        "old_total_hits": len(old_hits),
        "old_notes": note_count(old_hits),
        "old_hits": strip_spans(old_shown),
        "new_total_hits": len(new_hits),
        "new_notes": note_count(new_hits),
        "new_hits": strip_spans(new_shown),
        "hits_truncated": old_truncated or new_truncated,
        "old_hits_truncated": old_truncated,
        "new_hits_truncated": new_truncated,
    }
    return payload, EXIT_NEGATIVE if state == "mixed" else EXIT_OK


def run_numbers(args: argparse.Namespace, root: Path, notes: list[Path]) -> tuple[dict[str, Any], int]:
    pattern = compile_pattern(args.pattern, regex=True, label="--pattern")
    group = 1 if pattern.groups >= 1 else 0
    hits = scan(notes, pattern, root, context=args.context, group=group)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for hit in hits:
        grouped.setdefault(hit["match"], []).append(hit)

    def sort_key(value: str):
        try:
            return (0, float(value), value)
        except ValueError:
            return (1, 0.0, value)

    values = []
    any_truncated = False
    for value in sorted(grouped, key=sort_key):
        value_hits = grouped[value]
        shown, truncated = truncate(value_hits, args.max_hits)
        any_truncated = any_truncated or truncated
        values.append(
            {
                "value": value,
                "total_hits": len(value_hits),
                "notes": note_count(value_hits),
                "hits": strip_spans(shown),
                "hits_truncated": truncated,
            }
        )
    shown_values, values_truncated = truncate(values, args.max_hits)
    payload = {
        "tool": TOOL,
        "subcommand": "numbers",
        "pattern": args.pattern,
        "capture_group": group,
        "notes_scanned": len(notes),
        "total_hits": len(hits),
        "distinct_values": len(values),
        "conflict": len(values) > 1,
        "values": shown_values,
        "values_truncated": values_truncated,
        "hits_truncated": any_truncated,
    }
    return payload, EXIT_NEGATIVE if len(values) > 1 else EXIT_OK


def print_hits(hits: list[dict[str, Any]], indent: str = "  ") -> None:
    for hit in hits:
        print(f"{indent}{hit['path']}:{hit['line']}: {hit['context']}")


def print_human(payload: dict[str, Any]) -> None:
    subcommand = payload["subcommand"]
    if subcommand == "sweep":
        print(
            f"sweep {payload['phrase']!r}: {payload['total_hits']} occurrences in "
            f"{payload['notes_with_hits']} notes ({payload['notes_scanned']} scanned)"
        )
        print_hits(payload["hits"])
        if payload["hits_truncated"]:
            print(f"  ... output truncated to {len(payload['hits'])} hits")
    elif subcommand == "pair":
        print(
            f"OLD {payload['old']!r}: {payload['old_total_hits']} occurrences in "
            f"{payload['old_notes']} notes"
        )
        print_hits(payload["old_hits"])
        if payload["old_hits_truncated"]:
            print(f"  ... output truncated to {len(payload['old_hits'])} hits")
        print(
            f"NEW {payload['new']!r}: {payload['new_total_hits']} occurrences in "
            f"{payload['new_notes']} notes"
        )
        print_hits(payload["new_hits"])
        if payload["new_hits_truncated"]:
            print(f"  ... output truncated to {len(payload['new_hits'])} hits")
        if payload["mixed"]:
            print("MIXED: both wordings are present; the correction did not propagate")
        else:
            print(f"state: {payload['state']}")
    else:
        print(
            f"numbers {payload['pattern']!r}: {payload['distinct_values']} distinct values, "
            f"{payload['total_hits']} occurrences ({payload['notes_scanned']} notes scanned)"
        )
        for entry in payload["values"]:
            print(
                f"value {entry['value']!r}: {entry['total_hits']} occurrences in "
                f"{entry['notes']} notes"
            )
            print_hits(entry["hits"], indent="    ")
            if entry["hits_truncated"]:
                print(f"    ... output truncated to {len(entry['hits'])} hits")
        if payload["values_truncated"]:
            print(f"... value groups truncated to {len(payload['values'])}")
        if payload["conflict"]:
            print("CONFLICT: the pattern yields more than one distinct value")


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--path", default=DEFAULT_PATH,
                        help=f"search root inside the repository (default {DEFAULT_PATH})")
    parser.add_argument("--glob", default=DEFAULT_GLOB,
                        help=f"file glob under the search root (default {DEFAULT_GLOB})")
    parser.add_argument("--max-hits", type=int, default=DEFAULT_MAX_HITS,
                        help=f"maximum hits reported per list (default {DEFAULT_MAX_HITS})")
    parser.add_argument("--context", type=int, default=DEFAULT_CONTEXT,
                        help=f"maximum context characters per hit (default {DEFAULT_CONTEXT})")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="emit the result as JSON")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="claim-sweep",
        description="Find every location of a claim so a correction can be proven complete.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    sweep = subparsers.add_parser("sweep", help="report every occurrence of a phrase")
    sweep.add_argument("--phrase", required=True, help="literal text, or a regex with --regex")
    sweep.add_argument("--regex", action="store_true", help="treat --phrase as a regular expression")
    add_common(sweep)

    pair = subparsers.add_parser("pair", help="compare an old wording against its replacement")
    pair.add_argument("--old", required=True, help="the superseded literal wording")
    pair.add_argument("--new", required=True, help="the corrected literal wording")
    add_common(pair)

    numbers = subparsers.add_parser("numbers", help="group locations by a captured numeric value")
    numbers.add_argument("--pattern", required=True,
                         help="regex; group 1 is the value when the pattern has groups")
    add_common(numbers)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.max_hits < 0:
        parser.error("--max-hits must not be negative")
    if args.context < 0:
        parser.error("--context must not be negative")

    root = repo_root()
    try:
        search_path = resolve_search_path(args.path, root)
    except RefusalError as error:
        print(json.dumps({"refused": True, "tool": TOOL, "reason": str(error)}))
        return EXIT_REFUSAL

    notes = list(iter_notes(search_path, args.glob))
    runners = {"sweep": run_sweep, "pair": run_pair, "numbers": run_numbers}
    try:
        payload, code = runners[args.subcommand](args, root, notes)
    except ValueError as error:
        parser.error(str(error))
        raise AssertionError("unreachable")  # pragma: no cover
    payload["search_path"] = display_path(search_path, root)
    payload["exit_code"] = code
    if args.as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_human(payload)
    return code


if __name__ == "__main__":
    sys.exit(main())
