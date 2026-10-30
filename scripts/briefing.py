#!/usr/bin/env python3
"""Generate a bounded, current, agent-facing startup briefing from the Vault.

`Vault/00-System/START HERE.md` mandates a startup reading sequence whose
combined size exceeds any practical context window, so agents skim it
unpredictably. This tool parses the same authoritative notes and emits a
budgeted briefing plus explicit pointers back to where each detail lives.

Every emitted line is derived from text that exists in a source note. Nothing
is invented: when a heading, table, or block cannot be found, the tool emits an
``UNPARSED: <path> — ... read it directly.`` line instead of a plausible guess,
and exits tool-negative so the gap is visible. The briefing is a map, never a
replacement, and never an authority.

The fail-closed runtime gates extracted from `START HERE.md` (the six Direct3D
hardware markers, the `originals/` and `work/` rules, and the runtime instance
lifecycle requirement) are non-elidable: budget pressure truncates recent
sessions, then decisions, then unknowns, and never those rules.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime
import json
import math
import os
from pathlib import Path
import re
import sys
from typing import Callable, Iterable, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import evidence_lib as ev


TOOL = "briefing"
TOOL_VERSION = "1.1.0"

EXIT_OK = ev.EXIT_OK
EXIT_TOOL_NEGATIVE = ev.EXIT_TOOL_NEGATIVE
EXIT_USAGE = ev.EXIT_USAGE
EXIT_REFUSAL = ev.EXIT_REFUSAL

DEFAULT_BUDGET_TOKENS = 6000
MIN_BUDGET_TOKENS = 500
BYTES_PER_TOKEN = 4
TOKEN_ESTIMATE_METHOD = (
    "estimated tokens = bytes / 4 (a rough proxy, not a real tokenizer)"
)

NOTICE = (
    "GENERATED BRIEFING — NOT AUTHORITATIVE. Every line below is extracted "
    "from the cited note by `scripts/briefing.py`. It is a map, not a "
    "replacement: any claim you intend to rely on must be verified in the "
    "cited note before use."
)

# Paths, relative to the repository root.
P_START_HERE = "Vault/00-System/START HERE.md"
P_CHARTER = "Vault/00-System/Project Charter.md"
P_CURRENT_STATE = "Vault/00-System/Current State.md"
P_ROADMAP = "Vault/00-System/Project Roadmap.md"
P_ENVIRONMENT = "Vault/00-System/Environment Status.md"
P_DECISIONS = "Vault/50-Decisions/Decision Log.md"
P_UNKNOWNS = "Vault/70-Known-Unknowns/Known Unknowns.md"
P_SESSION_INDEX = "Vault/90-Sessions/Session Index.md"
P_SESSION_DIR = "Vault/90-Sessions"
P_MOC_DIR = "Vault/01-MOCs"
P_EXPERIMENT_DIR = "Vault/30-Experiments"
P_DEFAULT_MOC = "Vault/01-MOCs/Reverse Engineering MOC.md"

# The reading sequence `START HERE.md` mandates, in its stated order.
MANDATED_STARTUP_SET: tuple[tuple[str, str], ...] = (
    (P_START_HERE, "step 1"),
    (P_CURRENT_STATE, "step 2"),
    (P_ROADMAP, "step 3"),
    (P_ENVIRONMENT, "step 4"),
    (P_DECISIONS, "step 5"),
    (P_UNKNOWNS, "step 6"),
    (P_DEFAULT_MOC, "step 7 (task MOC; default shown)"),
)

# The six Direct3D hardware markers the runtime gate requires. These strings
# are searched for in `START HERE.md`; they are reported as MISSING FROM SOURCE
# rather than asserted when the note no longer contains them.
SIX_D3D_MARKERS: tuple[str, ...] = (
    "Native software render mode is FALSE",
    "RenderMode set to Direct3d render mode",
    "Screen mode 640x480x16 selected",
    "OnlySystemMemory status VIDEO MEMORY ONLY",
    "D3DAPPCREATE : Mode set to 640x480",
    "INIT : Starting Direct3D renderer",
)

# Lowest priority first: budget pressure drops blocks from these sections in
# this order. Sections absent from this list are non-elidable.
ELISION_ORDER: tuple[str, ...] = (
    "recent_sessions",
    "recent_decisions",
    "open_unknowns",
    "task_reading",
    "environment",
    "milestones",
    "mission",
)

STOPWORDS = frozenset(
    """
    the a an and or of for to in on at by with from into over under is are was
    were be been being do does did done how what which who whom whose why when
    where can could should would may might must will shall this that these
    those it its as if then than not no but so we you i our your their they
    them he she his her him us me my mine ours yours about after before during
    while within without across between per via any all some each every more
    most less least much many few other another same such only just also
    """.split()
)


# --------------------------------------------------------------------------
# Small text helpers. All are defensive: they never raise on odd input.
# --------------------------------------------------------------------------


def repo_root() -> Path:
    """Repository root, honoring ``ABLPC_ROOT`` (see ``evidence_lib.repo_root``)."""

    return ev.repo_root()


def estimate_tokens(text: str) -> int:
    """Approximate token count as bytes / 4 (documented as an estimate)."""

    return math.ceil(len(text.encode("utf-8")) / BYTES_PER_TOKEN)


def read_text(path: Path) -> str | None:
    """Return file text, or ``None`` when missing or unreadable."""

    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return None


def strip_frontmatter(text: str) -> str:
    """Drop a leading YAML frontmatter block if one is present."""

    if not text.startswith("---"):
        return text
    lines = text.splitlines()
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[index + 1:])
    return text


def normalize_ws(text: str) -> str:
    return " ".join(text.split())


def unparsed(path: str, detail: str) -> str:
    return f"UNPARSED: {path} — {detail}; read it directly."


def first_sentence(text: str, cap: int = 300) -> str:
    """First sentence of ``text``, capped. Truncation is marked with an ellipsis.

    Only source characters are emitted; the ellipsis marks that the quotation
    is incomplete so a reader never mistakes it for the whole claim.
    """

    flat = normalize_ws(text)
    if not flat:
        return ""
    match = re.search(r"\.\s", flat[40:]) if len(flat) > 40 else None
    if match:
        flat = flat[: 40 + match.start() + 1]
    if len(flat) > cap:
        flat = flat[:cap].rstrip() + " …"
    return flat.rstrip()


def trim_period(text: str) -> str:
    """Drop a single trailing full stop, keeping an ellipsis marker intact."""

    trimmed = text.rstrip()
    if trimmed.endswith(".") and not trimmed.endswith("…"):
        return trimmed[:-1]
    return trimmed


def bold_field(name: str) -> re.Pattern[str]:
    """Match a ``- **Name:** value`` bullet, tolerating `**Name**:` too."""

    return re.compile(
        rf"^[-*]\s+\*\*\s*{name}\s*:?\s*\*\*\s*:?\s*(.*)$", re.IGNORECASE
    )


STATUS_FIELD_RE = bold_field(r"Status")
DECISION_FIELD_RE = re.compile(
    r"^[-*]\s+\*\*\s*([^*:]*decision)\s*:?\s*\*\*\s*:?\s*(.*)$", re.IGNORECASE
)


@dataclass(frozen=True)
class Heading:
    level: int
    title: str
    body: tuple[str, ...]


def split_headings(text: str) -> list[Heading]:
    """Split markdown into ATX headings with their body lines.

    Lines inside fenced code blocks are never treated as headings.
    """

    headings: list[Heading] = []
    level = 0
    title = ""
    body: list[str] = []
    fenced = False
    for line in strip_frontmatter(text).splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            fenced = not fenced
        match = None if fenced else re.match(r"^(#{1,6})\s+(.*)$", line)
        if match:
            if level or body:
                headings.append(Heading(level, title, tuple(body)))
            level = len(match.group(1))
            title = match.group(2).strip()
            body = []
        else:
            body.append(line)
    if level or body:
        headings.append(Heading(level, title, tuple(body)))
    return headings


def find_heading(
    headings: Sequence[Heading], predicate: Callable[[Heading], bool]
) -> Heading | None:
    for heading in headings:
        if predicate(heading):
            return heading
    return None


def heading_titled(headings: Sequence[Heading], title: str) -> Heading | None:
    want = title.strip().lower()
    return find_heading(headings, lambda h: h.title.strip().lower() == want)


def paragraphs(lines: Iterable[str]) -> list[str]:
    """Group body lines into blank-line-separated paragraphs, verbatim."""

    out: list[str] = []
    current: list[str] = []
    for line in lines:
        if line.strip():
            current.append(line.rstrip())
        elif current:
            out.append("\n".join(current))
            current = []
    if current:
        out.append("\n".join(current))
    return out


def bullets(lines: Iterable[str]) -> list[str]:
    """Collect top-level ``-``/``*`` bullets, joining their continuation lines."""

    out: list[str] = []
    current: list[str] | None = None
    for line in lines:
        if re.match(r"^\s{0,3}[-*]\s+", line):
            if current is not None:
                out.append("\n".join(current))
            current = [line.rstrip()]
        elif current is not None:
            if not line.strip():
                out.append("\n".join(current))
                current = None
            elif line.startswith((" ", "\t")):
                current.append(line.rstrip())
            else:
                out.append("\n".join(current))
                current = None
    if current is not None:
        out.append("\n".join(current))
    return out


def bullet_text(bullet: str) -> str:
    return re.sub(r"^\s{0,3}[-*]\s+", "", normalize_ws(bullet))


def parse_table(lines: Sequence[str]) -> tuple[list[str], list[list[str]]] | None:
    """Parse the first pipe table in ``lines``. Returns ``None`` if absent."""

    header: list[str] | None = None
    rows: list[list[str]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            if header is not None:
                break
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if header is None:
            if index + 1 >= len(lines):
                return None
            separator = lines[index + 1].strip()
            if not re.fullmatch(r"\|[\s:|-]+\|?", separator):
                return None
            header = cells
            continue
        if re.fullmatch(r"[\s:|-]*", stripped.strip("|")):
            continue
        rows.append(cells)
    if header is None or not rows:
        return None
    return header, rows


# --------------------------------------------------------------------------
# Section model
# --------------------------------------------------------------------------


@dataclass
class Section:
    key: str
    title: str
    blocks: list[str] = field(default_factory=list)
    fixed: list[str] = field(default_factory=list)
    pointers: list[str] = field(default_factory=list)
    unparsed: list[str] = field(default_factory=list)
    dropped: int = 0

    @property
    def elidable(self) -> bool:
        return self.key in ELISION_ORDER

    @property
    def original_block_count(self) -> int:
        return len(self.blocks) + self.dropped

    def render(self) -> str:
        out = [f"## {self.title}"]
        out.extend(self.unparsed)
        out.extend(self.fixed)
        out.extend(self.blocks)
        if self.dropped:
            out.append(
                f"*[budget] {self.dropped} of {self.original_block_count} "
                f"entries omitted — read the source note for the rest.*"
            )
        out.extend(self.pointers)
        return "\n".join(out)

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "title": self.title,
            "elidable": self.elidable,
            "unparsed": list(self.unparsed),
            "fixed": list(self.fixed),
            "blocks": list(self.blocks),
            "dropped_blocks": self.dropped,
            "pointers": list(self.pointers),
        }


def pointer(path: str, anchor: str | None = None, note: str = "") -> str:
    target = f"`{path}`" if not anchor else f"`{path}` heading `{anchor}`"
    suffix = f" {note}" if note else ""
    return f"Read in full: {target}.{suffix}".rstrip()


# --------------------------------------------------------------------------
# Parsers — one per briefing section
# --------------------------------------------------------------------------


def build_current_handoff(
    root: Path, path: str, heading_title: str, key: str
) -> Section | None:
    """Prefer an explicit current section to historical format-specific extracts.

    The marker keeps a missing/renamed heading tool-negative rather than silently
    reviving legacy guidance. Older vaults without either heading or marker retain
    their legacy parser. Current handoffs are copied in full and never budget-elided.
    """
    text = read_text(root / path)
    if text is None:
        return None  # The legacy parser reports the missing file.
    headings = split_headings(text)
    matches = [i for i, h in enumerate(headings)
               if h.title.casefold() == heading_title.casefold()]
    marker = f"<!-- briefing: {heading_title} -->"
    if not matches and marker not in text:
        return None
    section = Section(key, heading_title)
    section.pointers.append(pointer(path, heading_title))
    if len(matches) != 1 or headings[matches[0]].level != 2:
        section.unparsed.append(unparsed(
            path, f"expected exactly one `## {heading_title}` heading"
        ))
        return section
    body = list(headings[matches[0]].body)
    has_content = bool(paragraphs(body))
    for child in headings[matches[0] + 1:]:
        if child.level <= 2:
            break
        has_content = has_content or bool(paragraphs(child.body))
        body.extend(["#" * child.level + " " + child.title, *child.body])
    if not has_content:
        section.unparsed.append(unparsed(path, f"`## {heading_title}` is empty"))
        return section
    section.fixed.append("\n".join(body).strip() + "\n")
    return section


def build_mission(root: Path) -> Section:
    section = Section("mission", "Mission and authority")
    section.pointers.append(pointer(P_CHARTER, "Mission"))
    section.pointers.append(pointer(P_START_HERE))

    start_text = read_text(root / P_START_HERE)
    if start_text is None:
        section.unparsed.append(unparsed(P_START_HERE, "file is missing"))
    else:
        headings = split_headings(start_text)
        top = find_heading(headings, lambda h: h.level == 1)
        paras = paragraphs(top.body) if top else []
        if paras:
            section.blocks.append(normalize_ws(paras[0]))
        else:
            section.unparsed.append(
                unparsed(P_START_HERE, "no opening paragraph under the H1")
            )

    charter_text = read_text(root / P_CHARTER)
    if charter_text is None:
        section.unparsed.append(unparsed(P_CHARTER, "file is missing"))
        return section
    mission = heading_titled(split_headings(charter_text), "Mission")
    if mission is None:
        section.unparsed.append(
            unparsed(P_CHARTER, "no `## Mission` heading")
        )
        return section
    paras = paragraphs(mission.body)
    if not paras:
        section.unparsed.append(unparsed(P_CHARTER, "`## Mission` is empty"))
        return section
    for para in paras[:2]:
        section.blocks.append(normalize_ws(para))
    return section


def build_hard_rules(root: Path) -> Section:
    """Extract the fail-closed runtime gates. Never elided, never summarized."""

    section = Section(
        "hard_rules", "Hard runtime rules — non-elidable, verbatim from source"
    )
    section.pointers.append(
        pointer(P_START_HERE, "Before touching evidence")
    )

    text = read_text(root / P_START_HERE)
    if text is None:
        section.unparsed.append(unparsed(P_START_HERE, "file is missing"))
        return section

    headings = split_headings(text)
    flat = normalize_ws(strip_frontmatter(text))

    # 1. The runtime instance lifecycle requirement (stated in the intro).
    lifecycle = None
    for heading in headings:
        for para in paragraphs(heading.body):
            if "Runtime instance lifecycle" in para:
                lifecycle = normalize_ws(para)
                break
        if lifecycle:
            break
    if lifecycle:
        section.fixed.append(f"- {lifecycle}")
    else:
        section.unparsed.append(
            unparsed(
                P_START_HERE,
                "no paragraph naming `Runtime instance lifecycle`",
            )
        )

    # 2/3/4. The `originals/`, `work/`, and hardware-gate bullets, verbatim.
    evidence_heading = heading_titled(headings, "Before touching evidence")
    if evidence_heading is None:
        section.unparsed.append(
            unparsed(P_START_HERE, "no `## Before touching evidence` heading")
        )
        rule_bullets: list[str] = []
    else:
        rule_bullets = bullets(evidence_heading.body)

    wanted_keys = ("originals/", "work/", "hardware acceleration", "Direct3D")
    kept = [
        bullet
        for bullet in rule_bullets
        if any(key in bullet for key in wanted_keys)
    ]
    if kept:
        for bullet in kept:
            section.fixed.append(f"- {bullet_text(bullet)}")
    else:
        section.unparsed.append(
            unparsed(
                P_START_HERE,
                "no `originals/`, `work/`, or Direct3D bullet under "
                "`Before touching evidence`",
            )
        )

    # 5. The six Direct3D markers, each confirmed present in the source.
    found = [marker for marker in SIX_D3D_MARKERS if marker in flat]
    missing = [marker for marker in SIX_D3D_MARKERS if marker not in flat]
    section.fixed.append(
        f"- An accepted hardware arm must positively prove all six markers "
        f"in the same log ({len(found)}/6 located in the source note):"
    )
    for marker in SIX_D3D_MARKERS:
        state = "present in source" if marker in found else "MISSING FROM SOURCE"
        section.fixed.append(f"  - `{marker}` ({state})")
    if missing:
        section.unparsed.append(
            unparsed(
                P_START_HERE,
                f"{len(missing)} of the six Direct3D markers were not found "
                "in this note, so the gate above may be stale",
            )
        )
    return section


def build_milestones(root: Path) -> Section:
    current = build_current_handoff(
        root, P_CURRENT_STATE, "Current task handoff", "current_task"
    )
    if current is not None:
        current.pointers.append(pointer(P_ROADMAP))
        return current
    section = Section("milestones", "Where the project is")
    section.pointers.append(pointer(P_ROADMAP, "Roadmap status"))
    section.pointers.append(
        pointer(P_CURRENT_STATE, "What should the next agent do?")
    )

    roadmap_text = read_text(root / P_ROADMAP)
    active_names: list[str] = []
    if roadmap_text is None:
        section.unparsed.append(unparsed(P_ROADMAP, "file is missing"))
    else:
        headings = split_headings(roadmap_text)
        table = None
        for heading in headings:
            parsed = parse_table(heading.body)
            if parsed is None:
                continue
            header_lower = [cell.lower() for cell in parsed[0]]
            if "milestone" in header_lower and "status" in header_lower:
                table = parsed
                break
        if table is None:
            section.unparsed.append(
                unparsed(
                    P_ROADMAP,
                    "no milestone table with `Milestone` and `Status` columns",
                )
            )
        else:
            header, rows = table
            lower = [cell.lower() for cell in header]
            name_col = lower.index("milestone")
            status_col = lower.index("status")
            outcome_col = lower.index("outcome") if "outcome" in lower else None
            active_blocks: list[str] = []
            other_blocks: list[str] = []
            for row in rows:
                if len(row) <= max(name_col, status_col):
                    continue
                name = row[name_col]
                status = row[status_col]
                outcome = (
                    row[outcome_col]
                    if outcome_col is not None and len(row) > outcome_col
                    else ""
                )
                line = f"- **{name}** — {status}"
                if outcome:
                    line += f" — {outcome}"
                if status.strip().lower() == "active":
                    active_names.append(name)
                    active_blocks.append(f"- **ACTIVE: {name}** — {status}")
                    if outcome:
                        active_blocks.append(f"  - Outcome: {outcome}")
                else:
                    other_blocks.append(line)
            section.blocks.extend(active_blocks)
            if not active_names:
                section.unparsed.append(
                    unparsed(
                        P_ROADMAP,
                        "the milestone table lists no `Active` milestone",
                    )
                )

            # The active milestone's own status paragraph, verbatim.
            for name in active_names:
                token = name.split()[0].strip()
                heading = find_heading(
                    headings,
                    lambda h, t=token: h.level == 2 and h.title.startswith(t),
                )
                if heading is None:
                    section.unparsed.append(
                        unparsed(
                            P_ROADMAP,
                            f"no `## {token} …` section for the active milestone",
                        )
                    )
                    continue
                status_para = next(
                    (
                        para
                        for para in paragraphs(heading.body)
                        if para.lstrip().startswith("**Status:")
                    ),
                    None,
                )
                if status_para is None:
                    section.unparsed.append(
                        unparsed(
                            P_ROADMAP,
                            f"`## {heading.title}` has no `**Status:**` paragraph",
                        )
                    )
                else:
                    section.blocks.append(
                        f"- Roadmap gate: {normalize_ws(status_para)}"
                    )
            section.blocks.extend(other_blocks)

    # The current packet, from Current State.
    state_text = read_text(root / P_CURRENT_STATE)
    if state_text is None:
        section.unparsed.append(unparsed(P_CURRENT_STATE, "file is missing"))
        return section
    packet = heading_titled(
        split_headings(state_text), "What should the next agent do?"
    )
    if packet is None:
        section.unparsed.append(
            unparsed(
                P_CURRENT_STATE,
                "no `## What should the next agent do?` heading",
            )
        )
        return section
    paras = paragraphs(packet.body)
    if not paras:
        section.unparsed.append(
            unparsed(P_CURRENT_STATE, "the current-packet section is empty")
        )
        return section
    packet_blocks = [
        f"- Current packet: {normalize_ws(paras[0])}"
    ]
    for para in paras[1:2]:
        packet_blocks.append(f"- {normalize_ws(para)}")
    section.blocks = packet_blocks + section.blocks
    return section


def build_environment(root: Path) -> Section:
    current = build_current_handoff(
        root, P_ENVIRONMENT, "Current runtime handoff", "current_runtime"
    )
    if current is not None:
        return current
    section = Section("environment", "Environment facts that change behavior")
    section.pointers.append(pointer(P_ENVIRONMENT, "Human annotations"))

    text = read_text(root / P_ENVIRONMENT)
    if text is None:
        section.unparsed.append(unparsed(P_ENVIRONMENT, "file is missing"))
        return section

    lines = strip_frontmatter(text).splitlines()

    # Blocking limitations first: they must survive truncation longer than the
    # tool-version rows below them.
    annotations = heading_titled(
        split_headings(text), "Human annotations"
    )
    limitation_keys = (
        ("rr / ntsync", ("ntsync",)),
        ("focus-gated runtime logic", ("focus",)),
        ("flaky canonical test (KU-065)", ("KU-065",)),
    )
    if annotations is None:
        section.unparsed.append(
            unparsed(P_ENVIRONMENT, "no `## Human annotations` heading")
        )
        annotation_bullets: list[str] = []
    else:
        annotation_bullets = bullets(annotations.body)

    if not annotation_bullets:
        section.unparsed.append(
            unparsed(P_ENVIRONMENT, "no bullets under `## Human annotations`")
        )
    else:
        seen: set[int] = set()
        for label, keys in limitation_keys:
            hit = next(
                (
                    index
                    for index, bullet in enumerate(annotation_bullets)
                    if any(key.lower() in bullet.lower() for key in keys)
                ),
                None,
            )
            if hit is None:
                section.blocks.append(
                    f"- Blocking limitation `{label}`: not found in "
                    f"`{P_ENVIRONMENT}` — check the note directly."
                )
                continue
            seen.add(hit)
            section.blocks.append(
                f"- Blocking limitation `{label}`: "
                f"{first_sentence(bullet_text(annotation_bullets[hit]), 320)}"
            )
        # Most recent human annotations (the note keeps newest at the top).
        for index, bullet in enumerate(annotation_bullets[:3]):
            if index in seen:
                continue
            section.blocks.append(
                f"- Recent annotation: {first_sentence(bullet_text(bullet), 320)}"
            )

    # Generated doctor block: installed tool versions.
    try:
        begin = next(
            index
            for index, line in enumerate(lines)
            if "BEGIN GENERATED: doctor" in line
        )
        end = next(
            index
            for index, line in enumerate(lines)
            if "END GENERATED: doctor" in line and index > begin
        )
    except StopIteration:
        section.unparsed.append(
            unparsed(
                P_ENVIRONMENT,
                "no `<!-- BEGIN GENERATED: doctor -->` block",
            )
        )
        return section

    rows: list[str] = []
    for line in lines[begin + 1: end]:
        stripped = line.rstrip()
        if not stripped.strip() or stripped.strip().startswith("```"):
            continue
        if stripped.strip() == "ABLPC doctor":
            continue
        parts = re.split(r"\s{2,}", stripped.strip(), maxsplit=1)
        if len(parts) == 2:
            rows.append(f"- {parts[0]}: {parts[1]}")
        else:
            rows.append(f"- {stripped.strip()}")
    if not rows:
        section.unparsed.append(
            unparsed(P_ENVIRONMENT, "the generated doctor block is empty")
        )
        return section
    section.blocks.append("- Installed tooling, from the generated `doctor` block:")
    section.blocks.extend(f"  {row}" for row in rows)
    return section


# ---- Known Unknowns -------------------------------------------------------


RESOLVED_LEADS = ("resolved", "accepted", "closed", "answered", "superseded")
OPEN_LEADS = (
    "open",
    "partially",
    "partial",
    "narrowed",
    "unresolved",
    "not resolved",
    "incomplete",
    "rejected",
    "bounded",
    "blocked",
)
LEAD_ADVERBS = re.compile(
    r"^(effectively|fully|largely|mostly|now|deliberately|provisionally)\s+"
)


def classify_ku_status(status: str) -> str:
    """Classify a Known Unknown's recorded status as ``open`` or ``resolved``.

    The leading word of the recorded status decides, because the note writes
    qualifications after it ("resolved at the tested boundary", "partially
    resolved", "narrowed by static audit; runtime open"). The rule is
    deliberately conservative — anything not clearly led by a resolution word
    counts as open, so the briefing never hides a live question — and the raw
    status text is always carried into the output so a reader can check it.
    """

    lower = normalize_ws(status).lower().lstrip("(").strip()
    lead = LEAD_ADVERBS.sub("", lower)
    if lead.startswith(OPEN_LEADS):
        return "open"
    if lead.startswith(RESOLVED_LEADS):
        return "resolved"
    if any(token in lower for token in OPEN_LEADS):
        return "open"
    if any(token in lower for token in RESOLVED_LEADS):
        return "resolved"
    return "open"


@dataclass
class KnownUnknown:
    ku_id: str
    title: str = ""
    status: str = ""
    summary: str = ""

    @property
    def sort_key(self) -> tuple[int, str]:
        match = re.search(r"(\d+)", self.ku_id)
        return (int(match.group(1)) if match else 0, self.ku_id)


def parse_known_unknowns(text: str) -> list[KnownUnknown]:
    """Collect KU entries from both the bullet form and the section form."""

    entries: dict[str, KnownUnknown] = {}

    def entry(ku_id: str) -> KnownUnknown:
        return entries.setdefault(ku_id, KnownUnknown(ku_id))

    # Section form: `## KU-060 - Title` with a `- **Status:** …` bullet.
    for heading in split_headings(text):
        match = re.match(
            r"^(KU-\d+)\s*[-—:]\s*(.+)$", heading.title.strip()
        )
        if match:
            item = entry(match.group(1))
            item.title = normalize_ws(match.group(2))
            for bullet in bullets(heading.body):
                status_match = STATUS_FIELD_RE.match(normalize_ws(bullet))
                if status_match and status_match.group(1).strip():
                    item.status = trim_period(
                        first_sentence(status_match.group(1), 120)
                    )
                    break

    # Bullet form: `- **KU-014:** …` or `- **KU-008 (resolved):** …`.
    for line_block in bullets(strip_frontmatter(text).splitlines()):
        flat = normalize_ws(line_block)
        match = re.match(
            r"^[-*]\s+\*\*(KU-\d+)\s*(\(([^)]*)\))?\s*:?\*\*:?\s*(.*)$", flat
        )
        if not match:
            continue
        item = entry(match.group(1))
        qualifier = (match.group(3) or "").strip()
        if qualifier and not item.status:
            item.status = trim_period(first_sentence(qualifier, 120))
        if not item.summary:
            item.summary = first_sentence(match.group(4), 160)

    for item in entries.values():
        if not item.status:
            item.status = "open (no status recorded in the note)"
    return sorted(entries.values(), key=lambda item: item.sort_key)


def build_unknowns(root: Path) -> Section:
    section = Section("open_unknowns", "Open questions (Known Unknowns)")
    section.pointers.append(pointer(P_UNKNOWNS))

    text = read_text(root / P_UNKNOWNS)
    if text is None:
        section.unparsed.append(unparsed(P_UNKNOWNS, "file is missing"))
        return section
    entries = parse_known_unknowns(text)
    if not entries:
        section.unparsed.append(
            unparsed(
                P_UNKNOWNS,
                "no `KU-NNN` bullet or `## KU-NNN - Title` section found",
            )
        )
        return section

    open_entries = [
        item for item in entries if classify_ku_status(item.status) == "open"
    ]
    resolved = len(entries) - len(open_entries)
    section.blocks.append(
        f"- {len(open_entries)} open of {len(entries)} parsed "
        f"({resolved} recorded as resolved and omitted)."
    )
    for item in open_entries:
        label = item.title or item.summary or "(no title recorded)"
        section.blocks.append(f"- {item.ku_id} — {label} [{item.status}]")
    return section


# ---- Decisions ------------------------------------------------------------


def build_decisions(root: Path, count: int) -> Section:
    section = Section("recent_decisions", f"Recent decisions (latest {count})")
    section.pointers.append(pointer(P_DECISIONS))

    text = read_text(root / P_DECISIONS)
    if text is None:
        section.unparsed.append(unparsed(P_DECISIONS, "file is missing"))
        return section

    found: list[tuple[tuple[str, int], str, str, str]] = []
    for position, heading in enumerate(split_headings(text)):
        match = re.match(
            r"^(DEC-(\d{8})-(\d+))\s*[-—:]\s*(.+)$", heading.title.strip()
        )
        if not match:
            dated = re.fullmatch(r"(\d{4}-\d{2}-\d{2}):\s*(.+)", heading.title.strip())
            if dated and heading.level == 2:
                try:
                    datetime.strptime(dated.group(1), "%Y-%m-%d")
                except ValueError:
                    section.unparsed.append(unparsed(P_DECISIONS, f"invalid decision date in `{heading.title}`"))
                    continue
                paras = paragraphs(heading.body)
                if not paras:
                    section.unparsed.append(unparsed(P_DECISIONS, f"`## {heading.title}` is empty"))
                    continue
                found.append((
                    (dated.group(1).replace("-", ""), -position),
                    dated.group(1), normalize_ws(dated.group(2)),
                    first_sentence(paras[0], 260),
                ))
            continue
        decision_line = ""
        for bullet in bullets(heading.body):
            field_match = DECISION_FIELD_RE.match(normalize_ws(bullet))
            if field_match and field_match.group(2).strip():
                label = normalize_ws(field_match.group(1))
                decision_line = (
                    f"{label}: {first_sentence(field_match.group(2), 260)}"
                )
                break
        found.append(
            (
                (match.group(2), int(match.group(3))),
                match.group(1),
                normalize_ws(match.group(4)),
                decision_line,
            )
        )
    if not found:
        section.unparsed.append(
            unparsed(P_DECISIONS, "no `## DEC-YYYYMMDD-NNN - Title` or `## YYYY-MM-DD: Title` headings")
        )
        return section

    found.sort(key=lambda item: item[0], reverse=True)
    for _, dec_id, title, decision_line in found[:count]:
        section.blocks.append(f"- **{dec_id}** — {title}")
        if decision_line:
            section.blocks.append(f"  - {decision_line}")
    return section


# ---- Sessions -------------------------------------------------------------


SESSION_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:\s+(\d{3,4}))?")


def build_sessions(root: Path, count: int) -> Section:
    section = Section("recent_sessions", f"Recent sessions (latest {count})")
    section.pointers.append(pointer(P_SESSION_INDEX))

    names: list[str] = []
    source = P_SESSION_INDEX
    text = read_text(root / P_SESSION_INDEX)
    if text is not None:
        names = [
            normalize_ws(name)
            for name in re.findall(r"\[\[([^\]|#]+)", strip_frontmatter(text))
        ]
    if not names:
        source = P_SESSION_DIR
        directory = root / P_SESSION_DIR
        try:
            names = [
                path.stem
                for path in directory.glob("*.md")
                if path.stem != "Session Index"
            ]
        except OSError:
            names = []
        if names:
            section.unparsed.append(
                unparsed(
                    P_SESSION_INDEX,
                    "no wiki-links found; fell back to session filenames",
                )
            )
    if not names:
        section.unparsed.append(
            unparsed(
                P_SESSION_INDEX,
                "no session entries in the index or in "
                f"`{P_SESSION_DIR}/`",
            )
        )
        return section

    dated: list[tuple[str, str, str]] = []
    for name in names:
        match = SESSION_DATE_RE.match(name)
        key = (
            f"{match.group(1)} {match.group(2) or '0000'}"
            if match
            else "0000-00-00 0000"
        )
        dated.append((key, name, source))
    dated.sort(key=lambda item: item[0], reverse=True)
    if all(key == "0000-00-00 0000" for key, _, _ in dated):
        section.unparsed.append(
            unparsed(
                source,
                "no session entry carries a leading `YYYY-MM-DD` date, so "
                "recency ordering is unavailable",
            )
        )
    for _, name, _ in dated[:count]:
        section.blocks.append(f"- {name}")
    return section


# ---- Task-directed reading ------------------------------------------------


def keywords_from(task: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9_]{3,}", task.lower())
    seen: list[str] = []
    for token in tokens:
        if token in STOPWORDS or token in seen:
            continue
        seen.append(token)
    return seen[:12]


def score_file(path: Path, keys: Sequence[str]) -> int:
    text = read_text(path)
    if text is None:
        return 0
    lower = text.lower()
    stem = path.stem.lower()
    score = 0
    for key in keys:
        score += min(lower.count(key), 5)
        if key in stem:
            score += 5
    return score


def build_task_reading(root: Path, task: str) -> Section:
    section = Section("task_reading", f"Suggested reading for: {task}")
    section.pointers.append(pointer(P_MOC_DIR))
    section.pointers.append(pointer(P_EXPERIMENT_DIR))

    keys = keywords_from(task)
    if not keys:
        section.unparsed.append(
            unparsed(
                "--task",
                "no usable keywords in the task text after stopword removal",
            )
        )
        return section
    section.blocks.append(f"- Keywords matched: {', '.join(keys)}")

    moc_dir = root / P_MOC_DIR
    try:
        mocs = sorted(moc_dir.glob("*.md"))
    except OSError:
        mocs = []
    if not mocs:
        section.unparsed.append(
            unparsed(P_MOC_DIR, "no MOC notes found in this directory")
        )
    else:
        ranked = sorted(
            ((score_file(path, keys), path) for path in mocs),
            key=lambda item: (-item[0], item[1].name),
        )
        hits = [item for item in ranked if item[0] > 0][:3]
        if hits:
            for score, path in hits:
                rel = path.relative_to(root).as_posix()
                section.blocks.append(f"- MOC (score {score}): `{rel}`")
        else:
            section.blocks.append(
                "- No MOC matched the task keywords. `START HERE.md` directs "
                f"you to start from `{P_DEFAULT_MOC}` when the relevant MOC "
                "is unclear."
            )

    exp_dir = root / P_EXPERIMENT_DIR
    try:
        experiments = sorted(exp_dir.glob("*.md"), reverse=True)[:40]
    except OSError:
        experiments = []
    if not experiments:
        section.unparsed.append(
            unparsed(P_EXPERIMENT_DIR, "no experiment notes found")
        )
        return section
    ranked_exp = sorted(
        ((score_file(path, keys), path) for path in experiments),
        key=lambda item: (-item[0], item[1].name),
    )
    hits = [item for item in ranked_exp if item[0] > 0][:5]
    if not hits:
        section.blocks.append(
            "- No recent experiment note matched the task keywords."
        )
        return section
    for score, path in hits:
        rel = path.relative_to(root).as_posix()
        section.blocks.append(f"- Experiment (score {score}): `{rel}`")
    return section


def build_map(root: Path) -> Section:
    """The pointer map: the mandated set, with its measured cost."""

    section = Section("map", "Where the detail actually lives")
    for rel, step in MANDATED_STARTUP_SET:
        stats = file_stats(root / rel)
        if stats["exists"]:
            section.fixed.append(
                f"- `{rel}` ({step}) — {stats['bytes']} bytes, "
                f"{stats['lines']} lines, ~{stats['estimated_tokens']} "
                "estimated tokens"
            )
        else:
            section.fixed.append(f"- `{rel}` ({step}) — MISSING from this repo")
    section.fixed.append(
        f"- Task MOC: pick from `{P_MOC_DIR}`; `{P_START_HERE}` names "
        f"`{P_DEFAULT_MOC}` as the default when the relevant MOC is unclear."
    )
    return section


# --------------------------------------------------------------------------
# Assembly, budget enforcement, rendering
# --------------------------------------------------------------------------


def build_sections(
    root: Path, *, task: str | None, decisions: int, sessions: int
) -> list[Section]:
    order = [
        build_mission(root),
        build_hard_rules(root),
        build_milestones(root),
        build_environment(root),
        build_unknowns(root),
        build_decisions(root, decisions),
        build_sessions(root, sessions),
    ]
    if task:
        order.append(build_task_reading(root, task))
    order.append(build_map(root))
    return order


def render_markdown(
    sections: Sequence[Section],
    *,
    task: str | None,
    generated_at: str,
    budget: int,
    footer: bool = True,
) -> str:
    out = ["# ABLPC session briefing (generated)", "", f"> {NOTICE}", ""]
    out.append(
        f"Generated {generated_at} by `scripts/{TOOL}.py` {TOOL_VERSION}."
        + (f" Task: {task}" if task else "")
    )
    out.append("")
    for section in sections:
        out.append(section.render())
        out.append("")
    if footer:
        out.append("## Briefing budget")
        out.append(f"- Budget: {budget} estimated tokens.")
        out.append(f"- Token estimate method: {TOKEN_ESTIMATE_METHOD}.")
        truncated = [s for s in sections if s.dropped]
        if truncated:
            for section in truncated:
                out.append(
                    f"- Truncated `{section.key}`: dropped {section.dropped} "
                    f"of {section.original_block_count} entries."
                )
        else:
            out.append("- Truncated sections: none.")
        unparsed_keys = [s.key for s in sections if s.unparsed]
        out.append(
            "- Unparsed sections: "
            + (", ".join(f"`{key}`" for key in unparsed_keys) or "none")
            + "."
        )
        out.append("")
    return "\n".join(out)


def enforce_budget(
    sections: Sequence[Section],
    *,
    task: str | None,
    generated_at: str,
    budget: int,
) -> tuple[str, int, bool]:
    """Drop blocks from the lowest-priority sections until the budget is met.

    Returns ``(markdown, estimated_tokens, budget_met)``. Non-elidable sections
    — above all the hard runtime rules — are never touched, so an impossibly
    small budget yields ``budget_met=False`` rather than an unsafe briefing.
    """

    by_key = {section.key: section for section in sections}
    order = [by_key[key] for key in ELISION_ORDER if key in by_key]
    while True:
        text = render_markdown(
            sections, task=task, generated_at=generated_at, budget=budget
        )
        tokens = estimate_tokens(text)
        if tokens <= budget:
            return text, tokens, True
        victim = next((s for s in order if s.blocks), None)
        if victim is None:
            return text, tokens, False
        victim.blocks.pop()
        victim.dropped += 1


def file_stats(path: Path) -> dict:
    try:
        data = path.read_bytes()
    except OSError:
        return {
            "path": path.as_posix(),
            "exists": False,
            "bytes": 0,
            "lines": 0,
            "estimated_tokens": 0,
        }
    text = data.decode("utf-8", errors="replace")
    return {
        "path": path.as_posix(),
        "exists": True,
        "bytes": len(data),
        "lines": len(text.splitlines()),
        "estimated_tokens": math.ceil(len(data) / BYTES_PER_TOKEN),
    }


def capabilities() -> dict:
    return {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "verbs": ["brief", "measure"],
        "writes": ["--out path only"],
        "reads": [rel for rel, _ in MANDATED_STARTUP_SET]
        + [P_CHARTER, P_SESSION_INDEX, P_MOC_DIR, P_EXPERIMENT_DIR],
        "formats": ["markdown", "json"],
        "authority": (
            "none — output is generated and must be verified in the cited note"
        ),
        "token_estimate_method": TOKEN_ESTIMATE_METHOD,
        "limits": {
            "default_budget_tokens": DEFAULT_BUDGET_TOKENS,
            "min_budget_tokens": MIN_BUDGET_TOKENS,
            "bytes_per_token": BYTES_PER_TOKEN,
            "elision_order": list(ELISION_ORDER),
            "non_elidable_sections": ["header", "hard_rules", "map", "current_task", "current_runtime"],
        },
        "fabrication_policy": (
            "sections that cannot be parsed emit an UNPARSED line naming the "
            "file; no content is inferred or restated from the tool's own "
            "knowledge"
        ),
        "exit_codes": {
            "0": "briefing produced, every section parsed, budget met",
            "1": "produced but degraded: a section is UNPARSED or the budget "
                 "could not be met without eliding non-elidable rules",
            "2": "usage error",
            "3": "refused: the non-elidable runtime rules could not be "
                 "extracted from START HERE.md",
        },
    }


def cmd_brief(args: argparse.Namespace) -> int:
    root = repo_root()
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    sections = build_sections(
        root,
        task=args.task,
        decisions=args.decisions,
        sessions=args.sessions,
    )

    hard_rules = next(s for s in sections if s.key == "hard_rules")
    if not hard_rules.fixed:
        payload = {
            "refused": True,
            "tool": TOOL,
            "reason": "hard_rules_unparsed",
            "detail": (
                f"no fail-closed runtime rule could be extracted from "
                f"{P_START_HERE}; a briefing without them would be unsafe"
            ),
            "unparsed": hard_rules.unparsed,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return EXIT_REFUSAL

    markdown, tokens, budget_met = enforce_budget(
        sections,
        task=args.task,
        generated_at=generated_at,
        budget=args.budget_tokens,
    )
    unparsed_lines = [line for section in sections for line in section.unparsed]
    degraded = bool(unparsed_lines) or not budget_met

    if args.format == "json":
        payload = {
            "tool": TOOL,
            "tool_version": TOOL_VERSION,
            "generated_at": generated_at,
            "repo_root": root.as_posix(),
            "notice": NOTICE,
            "task": args.task,
            "budget_tokens": args.budget_tokens,
            "budget_met": budget_met,
            "estimated_tokens": tokens,
            "token_estimate_method": TOKEN_ESTIMATE_METHOD,
            "status": "degraded" if degraded else "ok",
            "unparsed": unparsed_lines,
            "truncated_sections": [
                {
                    "key": section.key,
                    "dropped": section.dropped,
                    "kept": len(section.blocks),
                }
                for section in sections
                if section.dropped
            ],
            "sections": [section.to_dict() for section in sections],
        }
        output = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    else:
        output = markdown

    if args.out:
        try:
            Path(args.out).write_text(output, encoding="utf-8")
        except OSError as exc:
            print(
                json.dumps(
                    {
                        "refused": True,
                        "tool": TOOL,
                        "reason": "out_unwritable",
                        "detail": str(exc),
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
            return EXIT_REFUSAL
        print(
            json.dumps(
                {
                    "tool": TOOL,
                    "out": args.out,
                    "estimated_tokens": tokens,
                    "budget_met": budget_met,
                    "status": "degraded" if degraded else "ok",
                    "unparsed": unparsed_lines,
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        sys.stdout.write(output if output.endswith("\n") else output + "\n")

    return EXIT_TOOL_NEGATIVE if degraded else EXIT_OK


def cmd_measure(args: argparse.Namespace) -> int:
    root = repo_root()
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")

    files = []
    for rel, step in MANDATED_STARTUP_SET:
        stats = file_stats(root / rel)
        stats["path"] = rel
        stats["startup_step"] = step
        files.append(stats)
    total_bytes = sum(item["bytes"] for item in files)
    total_lines = sum(item["lines"] for item in files)
    total_tokens = sum(item["estimated_tokens"] for item in files)

    sections = build_sections(
        root, task=args.task, decisions=args.decisions, sessions=args.sessions
    )
    markdown, tokens, budget_met = enforce_budget(
        sections,
        task=args.task,
        generated_at=generated_at,
        budget=args.budget_tokens,
    )
    unparsed_lines = [line for section in sections for line in section.unparsed]

    payload = {
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "generated_at": generated_at,
        "repo_root": root.as_posix(),
        "token_estimate_method": TOKEN_ESTIMATE_METHOD,
        "mandated_startup_set": {
            "source": f"{P_START_HERE} — Required startup sequence",
            "files": files,
            "total_bytes": total_bytes,
            "total_lines": total_lines,
            "total_estimated_tokens": total_tokens,
        },
        "briefing": {
            "budget_tokens": args.budget_tokens,
            "budget_met": budget_met,
            "bytes": len(markdown.encode("utf-8")),
            "lines": len(markdown.splitlines()),
            "estimated_tokens": tokens,
            "truncated_sections": [
                {"key": s.key, "dropped": s.dropped} for s in sections if s.dropped
            ],
            "unparsed": unparsed_lines,
        },
        "reduction": {
            "estimated_tokens_saved": max(total_tokens - tokens, 0),
            "briefing_fraction_of_mandated": (
                round(tokens / total_tokens, 6) if total_tokens else None
            ),
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return EXIT_TOOL_NEGATIVE if unparsed_lines else EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="briefing.py",
        description=(
            "Generate a bounded startup briefing from the authoritative Vault "
            "notes. Output is generated and never authoritative."
        ),
    )
    parser.add_argument(
        "--capabilities",
        action="store_true",
        help="print machine-readable capabilities and exit",
    )
    sub = parser.add_subparsers(dest="command")

    def add_common(target: argparse.ArgumentParser) -> None:
        target.add_argument(
            "--budget-tokens",
            type=int,
            default=DEFAULT_BUDGET_TOKENS,
            help=f"token budget for the briefing (default {DEFAULT_BUDGET_TOKENS})",
        )
        target.add_argument(
            "--task",
            default=None,
            help="task text; adds keyword-selected MOC and experiment reading",
        )
        target.add_argument(
            "--decisions",
            type=int,
            default=5,
            help="how many recent decisions to include (default 5)",
        )
        target.add_argument(
            "--sessions",
            type=int,
            default=5,
            help="how many recent sessions to include (default 5)",
        )

    brief = sub.add_parser("brief", help="emit the briefing")
    add_common(brief)
    brief.add_argument(
        "--format", choices=("markdown", "json"), default="markdown"
    )
    brief.add_argument("--out", default=None, help="write the briefing here")
    brief.set_defaults(func=cmd_brief)

    measure = sub.add_parser(
        "measure", help="report the mandated startup set's cost as JSON"
    )
    add_common(measure)
    measure.set_defaults(func=cmd_measure)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.capabilities:
        if args.command:
            parser.error("--capabilities cannot be combined with a subcommand")
        print(json.dumps(capabilities(), indent=2, sort_keys=True))
        return EXIT_OK
    if not args.command:
        parser.error("a subcommand is required (brief or measure)")
    if args.budget_tokens < MIN_BUDGET_TOKENS:
        parser.error(
            f"--budget-tokens must be at least {MIN_BUDGET_TOKENS}"
        )
    if args.decisions < 0 or args.sessions < 0:
        parser.error("--decisions and --sessions must be non-negative")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
