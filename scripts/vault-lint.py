#!/usr/bin/env python3
"""Lint the ABLPC vault and report its mandated-reading context budget.

Original checks (unchanged): YAML frontmatter presence, required frontmatter
keys per note type, evidence ID patterns, duplicate evidence IDs, function-note
evidence locators, and wikilink resolution.  Errors still exit 1.

Added checks are advisory (warnings only) so the gated tree stays green:

* a context-budget report over the startup sequence mandated by
  ``Vault/00-System/START HERE.md`` (estimated tokens = bytes / 4);
* ``updated:`` staleness for ``type: system`` / ``type: system-state`` notes
  measured against the newest session-note date;
* orphan notes that nothing links to, excluding entry points.

Use ``--budget-only`` for the budget report alone as JSON, ``--json`` for the
whole lint result, and ``--list-orphans`` for orphan detail.  ``ABLPC_ROOT``
overrides the repository root; ``--vault`` overrides the vault directory.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

import yaml

DEFAULT_ROOT = Path(__file__).resolve().parents[1]


def repo_root() -> Path:
    """Return the repository root, honoring the ``ABLPC_ROOT`` override."""

    override = os.environ.get("ABLPC_ROOT")
    if override:
        return Path(override).resolve()
    return DEFAULT_ROOT


ROOT = repo_root()
VAULT = ROOT / "Vault"
ID_PATTERNS = {
    "experiment": re.compile(r"^EXP-\d{8}-\d{3}$"),
    "function": re.compile(r"^FUNC-[A-Z0-9]+-[0-9A-F]+$"),
    "hypothesis": re.compile(r"^HYP-\d{8}-\d{3}$"),
    "decision": re.compile(r"^DEC-\d{8}-\d{3}$"),
}
REQUIRED = {
    "experiment": {"type", "id", "date", "question", "binary_sha256", "environment", "result"},
    "function": {"type", "id", "binary_sha256", "address", "status", "confidence", "evidence"},
    "hypothesis": {"type", "id", "confidence", "status", "supporting_evidence", "contradicting_evidence"},
    "decision": {"type", "id", "status"},
}
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")

TOKEN_BYTES = 4
TOKEN_METHOD = "estimated_tokens = bytes // 4"
DEFAULT_NOTE_TOKEN_BUDGET = 40_000
DEFAULT_SESSION_TOKEN_BUDGET = 120_000
STARTUP_SECTION = re.compile(r"(?ms)^## Required startup sequence\s*$\n(.*?)(?=^## |\Z)")
BACKTICK_NOTE = re.compile(r"`([^`\n]+\.md)`")
START_HERE_REL = "00-System/START HERE.md"
DEFAULT_TASK_MOC_REL = "01-MOCs/Reverse Engineering MOC.md"
STARTUP_FALLBACK = (
    START_HERE_REL,
    "00-System/Current State.md",
    "00-System/Project Roadmap.md",
    "00-System/Environment Status.md",
    "50-Decisions/Decision Log.md",
    "70-Known-Unknowns/Known Unknowns.md",
)
STATE_TYPES = {"system", "system-state"}
ENTRY_POINT_DIRS = {"00-System", "99-Templates"}
ENTRY_POINT_TYPES = {"moc"}


def frontmatter(text: str):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    data = yaml.safe_load(text[4:end]) or {}
    return data if isinstance(data, dict) else None


def confirmed_body(text: str) -> str:
    match = re.search(r"(?ms)^## Confirmed\s*$\n(.*?)(?=^## |\Z)", text)
    if not match:
        return ""
    lines = [line.strip() for line in match.group(1).splitlines()]
    return "\n".join(line for line in lines if line and line not in {"None.", "None", "Unknown."})


def as_date(value) -> date | None:
    """Coerce a frontmatter date value to ``datetime.date`` when possible."""

    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        match = re.match(r"(\d{4})-(\d{2})-(\d{2})", text)
        if match:
            try:
                return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except ValueError:
                return None
    return None


def resolve_link(target: str, source: Path, vault: Path, by_rel: set[str],
                 by_stem: dict[str, list[Path]]) -> list[Path]:
    """Resolve a wikilink target to candidate notes.

    Resolution order matches the original linter exactly; an empty list means
    the link is broken.
    """

    normalized = target[:-3] if target.endswith(".md") else target
    if normalized.startswith("Vault/"):
        normalized = normalized[6:]
    if normalized in by_rel:
        return [vault / f"{normalized}.md"]
    if "/" not in normalized:
        stems = by_stem.get(Path(normalized).name, [])
        if stems:
            return list(stems)
    candidate = (source.parent / normalized).with_suffix(".md")
    if candidate.exists():
        return [candidate]
    return []


def startup_documents(vault: Path) -> list[str]:
    """Return vault-relative paths for the START HERE startup sequence."""

    documents: list[str] = []
    start_here = vault / START_HERE_REL
    if start_here.is_file():
        text = start_here.read_text(encoding="utf-8", errors="replace")
        section = STARTUP_SECTION.search(text)
        if section:
            for raw in BACKTICK_NOTE.findall(section.group(1)):
                rel = raw.strip()
                if rel.startswith("Vault/"):
                    rel = rel[6:]
                if rel and rel not in documents:
                    documents.append(rel)
    if not documents:
        documents = [rel for rel in STARTUP_FALLBACK if (vault / rel).is_file()]
    if (vault / DEFAULT_TASK_MOC_REL).is_file() and DEFAULT_TASK_MOC_REL not in documents:
        # START HERE step 7 is "whichever MOC relates to the current task" and
        # names this MOC as the default entry point.
        documents.append(DEFAULT_TASK_MOC_REL)
    return documents


def budget_report(vault: Path, *, note_token_budget: int,
                  session_token_budget: int) -> dict:
    """Measure the mandated startup reading set."""

    documents = []
    total_bytes = 0
    total_lines = 0
    for rel in startup_documents(vault):
        path = vault / rel
        exists = path.is_file()
        if exists:
            data = path.read_bytes()
            size = len(data)
            lines = data.count(b"\n") + (0 if data.endswith(b"\n") or not data else 1)
        else:
            size = 0
            lines = 0
        tokens = size // TOKEN_BYTES
        total_bytes += size
        total_lines += lines
        documents.append(
            {
                "path": f"Vault/{rel}",
                "exists": exists,
                "bytes": size,
                "lines": lines,
                "estimated_tokens": tokens,
                "over_note_budget": tokens > note_token_budget,
            }
        )
    total_tokens = total_bytes // TOKEN_BYTES
    return {
        "method": TOKEN_METHOD,
        "note_token_budget": note_token_budget,
        "session_token_budget": session_token_budget,
        "documents": documents,
        "total": {
            "documents": len(documents),
            "bytes": total_bytes,
            "lines": total_lines,
            "estimated_tokens": total_tokens,
            "over_session_budget": total_tokens > session_token_budget,
        },
    }


def format_budget_table(report: dict) -> list[str]:
    lines = [
        f"Context budget ({TOKEN_METHOD}; startup sequence from START HERE):",
        f"  {'tokens':>8}  {'bytes':>9}  {'lines':>6}  note",
    ]
    for entry in report["documents"]:
        flag = " *" if entry["over_note_budget"] else ""
        missing = "" if entry["exists"] else "  (missing)"
        lines.append(
            f"  {entry['estimated_tokens']:>8}  {entry['bytes']:>9}  "
            f"{entry['lines']:>6}  {entry['path']}{flag}{missing}"
        )
    total = report["total"]
    lines.append(
        f"  {total['estimated_tokens']:>8}  {total['bytes']:>9}  "
        f"{total['lines']:>6}  TOTAL of {total['documents']} mandated notes "
        f"(session budget {report['session_token_budget']})"
    )
    return lines


def lint(vault: Path, *, note_token_budget: int = DEFAULT_NOTE_TOKEN_BUDGET,
         session_token_budget: int = DEFAULT_SESSION_TOKEN_BUDGET) -> dict:
    """Run every check and return a machine-readable result."""

    display_root = vault.parent
    notes = list(vault.rglob("*.md"))
    by_stem: dict[str, list[Path]] = defaultdict(list)
    by_rel: set[str] = set()
    for path in notes:
        rel = path.relative_to(vault).with_suffix("").as_posix()
        by_rel.add(rel)
        by_stem[path.stem].append(path)

    errors: list[str] = []
    warnings: list[str] = []
    ids: dict[str, list[Path]] = defaultdict(list)
    linked: set[Path] = set()
    state_notes: list[tuple[Path, date]] = []
    session_dates: list[date] = []
    note_types: dict[Path, str] = {}

    for path in notes:
        rel = path.relative_to(display_root)
        text = path.read_text(encoding="utf-8")
        template = "99-Templates" in path.parts
        data = frontmatter(text)
        if data is None:
            errors.append(f"{rel}: missing or malformed YAML frontmatter")
            continue
        note_type = data.get("type")
        evidence_id = data.get("id")
        if isinstance(note_type, str):
            note_types[path] = note_type
        if evidence_id and not template:
            ids[str(evidence_id)].append(path)
        if not template and note_type in REQUIRED:
            missing = sorted(key for key in REQUIRED[note_type] if key not in data)
            if missing:
                errors.append(f"{rel}: missing frontmatter keys: {', '.join(missing)}")
            pattern = ID_PATTERNS.get(note_type)
            if pattern and evidence_id and not pattern.fullmatch(str(evidence_id)):
                errors.append(f"{rel}: malformed {note_type} ID {evidence_id!r}")
        if not template and note_type == "function":
            evidence = data.get("evidence")
            if not evidence:
                warnings.append(f"{rel}: function note has no evidence references")
            body = confirmed_body(text)
            locator = re.search(r"\b(?:EXP|RUN|BIN)-[A-Z0-9-]+\b|0x[0-9A-Fa-f]+|\boffset\b|static/|dynamic/", body)
            if body and not evidence and not locator:
                warnings.append(f"{rel}: Confirmed section has claims without a concrete evidence locator")

        if not template and note_type in STATE_TYPES:
            updated = as_date(data.get("updated"))
            if updated is not None:
                state_notes.append((path, updated))
        if not template and note_type == "session":
            session_date = as_date(data.get("date"))
            if session_date is not None:
                session_dates.append(session_date)

        for target in WIKILINK.findall(text):
            target = target.strip()
            if not target or "{{" in target:
                continue
            resolved = resolve_link(target, path, vault, by_rel, by_stem)
            if not resolved:
                errors.append(f"{rel}: broken wikilink [[{target}]]")
                continue
            for destination in resolved:
                if destination != path:
                    linked.add(destination)

    for evidence_id, paths in sorted(ids.items()):
        if len(paths) > 1:
            errors.append(
                f"duplicate ID {evidence_id}: "
                + ", ".join(str(p.relative_to(display_root)) for p in paths)
            )

    # --- advisory checks (warnings only) -------------------------------------
    report = budget_report(
        vault,
        note_token_budget=note_token_budget,
        session_token_budget=session_token_budget,
    )
    for entry in report["documents"]:
        if not entry["exists"]:
            warnings.append(f"{entry['path']}: mandated startup document does not exist")
        elif entry["over_note_budget"]:
            warnings.append(
                f"{entry['path']}: {entry['estimated_tokens']} estimated tokens "
                f"exceeds the {note_token_budget}-token note budget"
            )
    total = report["total"]
    if total["over_session_budget"]:
        warnings.append(
            f"mandated startup sequence totals {total['estimated_tokens']} estimated tokens "
            f"across {total['documents']} notes, exceeding the "
            f"{session_token_budget}-token session budget"
        )

    newest_session = max(session_dates, default=None)
    stale = []
    if newest_session is not None:
        for path, updated in sorted(state_notes):
            if updated < newest_session:
                rel = path.relative_to(display_root)
                stale.append(str(rel))
                warnings.append(
                    f"{rel}: updated: {updated.isoformat()} is older than the newest "
                    f"session note date {newest_session.isoformat()}"
                )

    orphans = []
    for path in sorted(notes):
        if path in linked:
            continue
        if ENTRY_POINT_DIRS.intersection(path.parts):
            continue
        if note_types.get(path) in ENTRY_POINT_TYPES:
            continue
        orphans.append(str(path.relative_to(display_root)))
    if orphans:
        warnings.append(
            f"{len(orphans)} notes have no inbound wikilink "
            "(entry points excluded; use --list-orphans for detail)"
        )

    return {
        "tool": "vault-lint",
        "vault": str(vault),
        "counts": {
            "notes": len(notes),
            "errors": len(errors),
            "warnings": len(warnings),
            "orphans": len(orphans),
            "stale_state_notes": len(stale),
        },
        "errors": errors,
        "warnings": warnings,
        "orphans": orphans,
        "stale_state_notes": stale,
        "newest_session_date": newest_session.isoformat() if newest_session else None,
        "budget": report,
        "ok": not errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint the ABLPC vault and report its mandated-reading context budget."
    )
    parser.add_argument("--vault", type=Path, default=None,
                        help="vault directory (default: $ABLPC_ROOT/Vault)")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="emit the full lint result as JSON")
    parser.add_argument("--budget-only", action="store_true",
                        help="emit only the context-budget report as JSON and exit 0")
    parser.add_argument("--list-orphans", action="store_true",
                        help="list every note with no inbound wikilink")
    parser.add_argument("--note-token-budget", type=int, default=DEFAULT_NOTE_TOKEN_BUDGET,
                        help=f"per-note estimated-token budget (default {DEFAULT_NOTE_TOKEN_BUDGET})")
    parser.add_argument("--session-token-budget", type=int, default=DEFAULT_SESSION_TOKEN_BUDGET,
                        help=f"startup-sequence estimated-token budget (default {DEFAULT_SESSION_TOKEN_BUDGET})")
    args = parser.parse_args(argv)

    vault = args.vault if args.vault is not None else repo_root() / "Vault"
    if args.budget_only:
        report = budget_report(
            vault,
            note_token_budget=args.note_token_budget,
            session_token_budget=args.session_token_budget,
        )
        report["tool"] = "vault-lint"
        report["report"] = "context-budget"
        report["vault"] = str(vault)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    result = lint(
        vault,
        note_token_budget=args.note_token_budget,
        session_token_budget=args.session_token_budget,
    )
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1 if result["errors"] else 0

    for line in format_budget_table(result["budget"]):
        print(line)
    for message in result["warnings"]:
        print(f"WARNING: {message}")
    if args.list_orphans:
        for orphan in result["orphans"]:
            print(f"ORPHAN: {orphan}")
    for message in result["errors"]:
        print(f"ERROR: {message}")
    counts = result["counts"]
    print(
        f"Vault lint: {counts['notes']} notes, {counts['errors']} errors, "
        f"{counts['warnings']} warnings"
    )
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
