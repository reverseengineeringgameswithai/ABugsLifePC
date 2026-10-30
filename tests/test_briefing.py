"""Tests for `scripts/briefing.py`.

Every test builds a SYNTHETIC vault under ``tmp_path`` and points the tool at
it with ``ABLPC_ROOT``. Nothing here asserts on the real ``Vault/`` content,
which is edited continuously and would make these tests a tripwire for ordinary
research work rather than for the tool.
"""

from __future__ import annotations

import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load_briefing():
    spec = importlib.util.spec_from_file_location("briefing", SCRIPTS / "briefing.py")
    module = importlib.util.module_from_spec(spec)
    # `dataclass` resolves field types through ``sys.modules[cls.__module__]``,
    # so the module must be registered before it is executed.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


briefing = _load_briefing()


# --------------------------------------------------------------------------
# Synthetic vault
# --------------------------------------------------------------------------


SIX_MARKERS = (
    "`Native software render mode is FALSE`, `RenderMode set to Direct3d "
    "render\n  mode`, `Screen mode 640x480x16 selected`, `OnlySystemMemory "
    "status VIDEO\n  MEMORY ONLY`, `D3DAPPCREATE : Mode set to 640x480`, and\n"
    "  `INIT : Starting Direct3D renderer`"
)

START_HERE = f"""---
type: system
---

# START HERE

This synthetic vault is the durable shared memory for the test.

Before any runtime launch, follow
[[Agent Operating Manual#Runtime instance lifecycle]]; close obsolete runtime
and agent instances promptly and prove the final process/sink audit is clear.

## Before touching evidence

- Identify the executable SHA-256 or state explicitly that no binary exists.
- Work only on copies under `work/`; never modify `originals/`.
- For renderer-facing runtime work, select **hardware acceleration**. An
  accepted arm must positively prove all six markers in the same log:
  {SIX_MARKERS}. Reject the arm if any is absent.
- Frame a bounded question.

## End-of-session sequence

1. Update [[Current State]].
"""

CHARTER = """---
type: project-charter
---

# Project Charter

## Mission

Reverse engineer the synthetic subject through reproducible evidence.

The synthetic binary and its controlled behavior are the subject.

## Scope

- Something else entirely.
"""

ROADMAP = """---
type: system
---

# Project Roadmap

## Roadmap status

| Milestone | Status | Outcome | Evidence or entry point |
|---|---|---|---|
| M0 — Foundation | Complete | A reproducible loop | `EXP-0001` |
| M1 — Synthetic reimplementation | Active | Replace one component | `EXP-0002` |
| M2 — Later work | Deferred | Trace a placement | `EXP-0003` |

## M0 — Foundation

**Status:** Complete at the synthetic boundary.

## M1 — Synthetic reimplementation

**Status:** Active with one admitted synthetic module and no second module.

### M1.1 — First packet

**Question:** Does the synthetic selector reproduce its receipts?
"""

CURRENT_STATE = """---
type: system
---

# Current State

## What currently works?

Nothing of consequence in this fixture.

## What should the next agent do?

Run the synthetic grain-gate follow-up and record its receipts before any
runtime launch.

Preserve the completed milestones and do not reopen them by momentum.

## 2026-01-01 an older entry

Historic prose that must not be mistaken for the current packet.
"""

ENVIRONMENT = """---
type: environment
---

# Environment Status

## Human annotations

- **Closure audit, synthetic packet.** The session was offline throughout and
  launched no game.
- KU-065 recurred twice in the synthetic suite: `1 failed, 685 passed` at one
  intermittent node. No fixture changed in that packet.
- **rr cannot record the Wine game while `ntsync` is loaded** (`KU-028`): the
  in-kernel driver's ioctls are not modelled, so `rr record` aborts.
- The accepted arms used manually focused Gamescope `-g` windows, because the
  logic is focus-gated and an unfocused arm records nothing.

<!-- BEGIN GENERATED: doctor -->

```text
ABLPC doctor
Generated: 2026-01-01T00:00:00-00:00

Wine               wine-11.0 (Staging)
Python             Python 3.14.6
strace             not installed
```

<!-- END GENERATED: doctor -->
"""

UNKNOWNS = """---
type: register
---

# Known Unknowns

- **KU-001:** The first synthetic question is unanswered and stays open.
- **KU-002 (resolved at the tested boundary):** The second synthetic question
  was answered by `EXP-0007`.
- **KU-005 (partially resolved):** Half of the fifth question is answered.

## Level-data unknowns

- **KU-006 (narrowed):** The sixth question is narrower but still live.

## KU-003 - Third synthetic question

- **Status:** open.
- **Known:** something at `0x00401000`.

## KU-004 - Fourth synthetic question

- **Status:** resolved by `EXP-0008`.
- **Known:** something at `0x00402000`.
"""

DECISIONS = """---
type: register
---

# Decision Log

## DEC-20260101-001 - First synthetic decision

- **Context:** Something needed deciding.
- **Decision:** Keep one synthetic repository. Everything else follows.
- **Revisit when:** Never.

## DEC-20260102-002 - Second synthetic decision

- **Context:** Something else needed deciding.
- **Worker decision:** Implement the synthetic evaluator as one ordered pass.

## DEC-20260103-003 - Third synthetic decision

- **Context:** A third thing.
- **Decision:** Reject the third proposal at exact commit `abc1234`.
"""

SESSION_INDEX = """---
type: index
---

# Session Index

- [[2026-01-03 1200 - Claude - third synthetic session]]

- [[2026-01-01 0900 - Codex - first synthetic session]]

- [[2026-01-02 1000 - James - second synthetic session]]
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_vault(root: Path) -> Path:
    write(root / "Vault/00-System/START HERE.md", START_HERE)
    write(root / "Vault/00-System/Project Charter.md", CHARTER)
    write(root / "Vault/00-System/Project Roadmap.md", ROADMAP)
    write(root / "Vault/00-System/Current State.md", CURRENT_STATE)
    write(root / "Vault/00-System/Environment Status.md", ENVIRONMENT)
    write(root / "Vault/70-Known-Unknowns/Known Unknowns.md", UNKNOWNS)
    write(root / "Vault/50-Decisions/Decision Log.md", DECISIONS)
    write(root / "Vault/90-Sessions/Session Index.md", SESSION_INDEX)
    write(
        root / "Vault/01-MOCs/Reverse Engineering MOC.md",
        "# Reverse Engineering MOC\n\nA general entry point.\n",
    )
    write(
        root / "Vault/01-MOCs/Subsystems MOC.md",
        "# Subsystems MOC\n\nGrain gate resolver evidence and grain thresholds.\n",
    )
    write(
        root / "Vault/30-Experiments/EXP-20260101-001 - Grain gate resolver.md",
        "# Grain gate resolver\n\nThe grain gate opening resolver receipts.\n",
    )
    write(
        root / "Vault/30-Experiments/EXP-20260102-002 - Camera reconnaissance.md",
        "# Camera reconnaissance\n\nUnrelated camera prose.\n",
    )
    return root


def run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["ABLPC_ROOT"] = str(root)
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "briefing.py"), *args],
        capture_output=True,
        text=True,
        env=env,
    )


@pytest.fixture()
def vault(tmp_path: Path) -> Path:
    return make_vault(tmp_path)


# --------------------------------------------------------------------------
# Well-formed parsing
# --------------------------------------------------------------------------


def test_every_section_parses_from_a_well_formed_vault(vault: Path) -> None:
    result = run(vault, "brief")
    assert result.returncode == 0, result.stdout + result.stderr
    out = result.stdout
    assert "UNPARSED" not in out
    for heading in (
        "## Mission and authority",
        "## Hard runtime rules",
        "## Where the project is",
        "## Environment facts that change behavior",
        "## Open questions (Known Unknowns)",
        "## Recent decisions",
        "## Recent sessions",
        "## Where the detail actually lives",
        "## Briefing budget",
    ):
        assert heading in out


def test_briefing_states_it_is_generated_and_not_authoritative(vault: Path) -> None:
    out = run(vault, "brief").stdout
    assert "NOT AUTHORITATIVE" in out
    assert "verified in the cited note" in out


def test_mission_quotes_the_charter(vault: Path) -> None:
    out = run(vault, "brief").stdout
    assert "Reverse engineer the synthetic subject" in out
    assert "`Vault/00-System/Project Charter.md` heading `Mission`" in out


def test_hard_rules_carry_the_gates_verbatim(vault: Path) -> None:
    out = run(vault, "brief").stdout
    assert "never modify `originals/`" in out
    assert "Work only on copies under `work/`" in out
    assert "Runtime instance lifecycle" in out
    for marker in briefing.SIX_D3D_MARKERS:
        assert marker in out
        assert f"`{marker}` (present in source)" in out
    assert "6/6 located in the source note" in out


def test_active_milestone_and_current_packet(vault: Path) -> None:
    out = run(vault, "brief").stdout
    assert "ACTIVE: M1 — Synthetic reimplementation" in out
    assert "Active with one admitted synthetic module" in out
    assert "Run the synthetic grain-gate follow-up" in out
    # One line for each non-active milestone, no packet detail for them.
    assert "**M0 — Foundation** — Complete" in out
    assert "**M2 — Later work** — Deferred" in out
    assert "Complete at the synthetic boundary" not in out
    # Older Current State headings must not be mistaken for the packet.
    assert "Historic prose" not in out


def test_environment_reports_versions_and_blocking_limitations(vault: Path) -> None:
    out = run(vault, "brief").stdout
    assert "Wine: wine-11.0 (Staging)" in out
    assert "strace: not installed" in out
    assert "rr / ntsync" in out and "in-kernel driver's ioctls" in out
    assert "focus-gated" in out
    assert "KU-065" in out


@pytest.mark.parametrize("path,title,legacy", [
    (briefing.P_CURRENT_STATE, "Current task handoff", "Run the synthetic grain-gate follow-up"),
    (briefing.P_ENVIRONMENT, "Current runtime handoff", "Closure audit, synthetic packet"),
])
def test_current_handoff_precedes_legacy_guidance(vault: Path, path: str, title: str, legacy: str) -> None:
    original = (vault/path).read_text()
    write(vault/path, original + f"\n<!-- briefing: {title} -->\n## {title}\n\n"
          "Use the approved synthetic successor.\n\nKeep its rollback.\n\n"
          "Third paragraph: do not resume paused work.\n")
    result = run(vault, "brief")
    assert result.returncode == 0, result.stdout
    assert "Use the approved synthetic successor." in result.stdout
    assert "Third paragraph: do not resume paused work." in result.stdout
    assert legacy not in result.stdout
    assert f'heading `{title}`' in result.stdout
    if path == briefing.P_CURRENT_STATE:
        assert "ACTIVE: M1" not in result.stdout
        assert "Roadmap gate:" not in result.stdout
    else:
        assert "Recent annotation:" not in result.stdout
        assert "Wine: wine-11.0" not in result.stdout


@pytest.mark.parametrize("path,title,legacy", [
    (briefing.P_CURRENT_STATE, "Current task handoff", "Run the synthetic grain-gate follow-up"),
    (briefing.P_ENVIRONMENT, "Current runtime handoff", "Closure audit, synthetic packet"),
])
@pytest.mark.parametrize("damage", ["empty", "duplicate", "renamed", "wrong_level"])
def test_broken_current_handoff_never_revives_history(vault: Path, path: str, title: str, legacy: str, damage: str) -> None:
    heading = f"## {title}\n\nCurrent synthetic handoff.\n"
    if damage == "empty":
        heading = f"## {title}\n\n"
    elif damage == "duplicate":
        heading += "\n" + heading
    elif damage == "renamed":
        heading = "## Renamed handoff\n\nCurrent synthetic handoff.\n"
    elif damage == "wrong_level":
        heading = "#" + heading
    write(vault/path, (vault/path).read_text() + f"\n<!-- briefing: {title} -->\n" + heading)
    result = run(vault, "brief")
    assert result.returncode == briefing.EXIT_TOOL_NEGATIVE
    assert f"UNPARSED: {path}" in result.stdout
    assert legacy not in result.stdout


def test_current_handoffs_survive_budget_pressure(vault: Path) -> None:
    for path, title in ((briefing.P_CURRENT_STATE, "Current task handoff"),
                        (briefing.P_ENVIRONMENT, "Current runtime handoff")):
        write(vault/path, (vault/path).read_text() + f"\n## {title}\n\n"
              f"Preserve all instructions in {title}, including the last paragraph.\n")
    result = run(vault, "brief", "--format", "json", "--budget-tokens", "900")
    payload = json.loads(result.stdout)
    sections = {s['key']: s for s in payload['sections']}
    for key in ('current_task', 'current_runtime'):
        assert sections[key]['dropped_blocks'] == 0
        assert sections[key]['elidable'] is False
        assert 'including the last paragraph' in ' '.join(sections[key]['fixed'])
    for marker in briefing.SIX_D3D_MARKERS:
        assert marker in ' '.join(sections['hard_rules']['fixed'])


def test_fenced_handoff_heading_is_not_a_duplicate(vault: Path) -> None:
    path = vault/briefing.P_CURRENT_STATE
    write(path, path.read_text() + "\n## Current task handoff\n\nApproved synthetic work.\n\n"
          "## Example\n\n```markdown\n## Current task handoff\n```\n")
    result = run(vault, 'brief')
    assert result.returncode == 0, result.stdout


def test_current_handoff_keeps_child_sections_and_command_format(vault: Path) -> None:
    path = vault/briefing.P_CURRENT_STATE
    command = '```bash\nrun-builder \\\n  --fresh successor\n```'
    write(path, path.read_text() + '\n## Current task handoff\n\n'
          '### Build the approved copy\n\n' + command + '\n\n'
          '### Limits\n\nKeep streaming paused.\n\n'
          '## History\n\nDo not surface this old instruction.\n')
    result = run(vault, 'brief')
    assert result.returncode == 0, result.stdout
    assert command in result.stdout
    assert '### Limits\n\nKeep streaming paused.' in result.stdout
    assert 'Do not surface this old instruction.' not in result.stdout


def test_date_named_decisions_are_not_hidden_by_legacy_ids(vault: Path) -> None:
    path = vault/briefing.P_DECISIONS
    write(path, "## 2026-02-02: Current choice\n\nKeep the approved successor.\n\n"
          "## 2026-02-02: Previous same-day choice\n\nPreserve the original.\n\n"
          "## 2026-02-01: Earlier date\n\nLeave earlier work paused.\n\n" + path.read_text())
    result = run(vault, 'brief', '--decisions', '3')
    assert result.returncode == 0, result.stdout
    assert result.stdout.index('Current choice') < result.stdout.index('Previous same-day choice') < result.stdout.index('Earlier date')
    assert 'Keep the approved successor.' in result.stdout
    assert 'DEC-20260103-003' not in result.stdout


@pytest.mark.parametrize('heading,body', [('2026-02-30: Impossible date', 'Some text.'),
                                          ('2026-02-02: Empty decision', '')])
def test_invalid_date_named_decisions_are_reported(vault: Path, heading: str, body: str) -> None:
    path = vault/briefing.P_DECISIONS
    write(path, path.read_text() + f'\n## {heading}\n\n{body}\n')
    result = run(vault, 'brief')
    assert result.returncode == briefing.EXIT_TOOL_NEGATIVE
    assert f'UNPARSED: {briefing.P_DECISIONS}' in result.stdout


def test_recent_decisions_are_newest_first_with_one_line_each(vault: Path) -> None:
    out = run(vault, "brief").stdout
    assert out.index("DEC-20260103-003") < out.index("DEC-20260101-001")
    assert "Keep one synthetic repository" in out
    assert "Worker decision: Implement the synthetic evaluator" in out
    # The one line is the decision only, not the whole entry.
    assert "Revisit when" not in out


def test_recent_sessions_are_sorted_by_date_not_file_order(vault: Path) -> None:
    out = run(vault, "brief").stdout
    third = out.index("third synthetic session")
    second = out.index("second synthetic session")
    first = out.index("first synthetic session")
    assert third < second < first


def test_pointers_name_every_source_file(vault: Path) -> None:
    out = run(vault, "brief").stdout
    for rel, _ in briefing.MANDATED_STARTUP_SET:
        assert rel in out


# --------------------------------------------------------------------------
# Open vs resolved filtering
# --------------------------------------------------------------------------


def test_open_versus_resolved_known_unknowns(vault: Path) -> None:
    out = run(vault, "brief").stdout
    assert "KU-001 — The first synthetic question" in out
    assert "KU-003 — Third synthetic question" in out
    assert "KU-005" in out  # partially resolved still counts as open
    assert "KU-006" in out  # narrowed still counts as open
    assert "KU-002" not in out
    assert "KU-004" not in out
    assert "3 recorded as resolved and omitted" not in out
    assert "4 open of 6 parsed (2 recorded as resolved and omitted)" in out


@pytest.mark.parametrize(
    "status,expected",
    [
        ("open", "open"),
        ("open.", "open"),
        ("resolved at the tested boundary", "resolved"),
        ("effectively resolved", "resolved"),
        ("partially resolved", "open"),
        ("narrowed by static audit; runtime open", "open"),
        ("rejected incomplete alignment", "open"),
        ("resolved at live agreement; stable attribution rejected", "resolved"),
        ("", "open"),
        ("something nobody anticipated", "open"),
    ],
)
def test_status_classifier(status: str, expected: str) -> None:
    assert briefing.classify_ku_status(status) == expected


def test_status_text_is_carried_into_the_output(vault: Path) -> None:
    out = run(vault, "brief").stdout
    assert "[partially resolved]" in out
    assert "[narrowed]" in out


# --------------------------------------------------------------------------
# Degradation: missing files and malformed structures
# --------------------------------------------------------------------------


def test_missing_file_yields_unparsed_and_does_not_crash(vault: Path) -> None:
    (vault / "Vault/50-Decisions/Decision Log.md").unlink()
    result = run(vault, "brief")
    assert result.returncode == briefing.EXIT_TOOL_NEGATIVE
    assert "UNPARSED: Vault/50-Decisions/Decision Log.md" in result.stdout
    assert "read it directly." in result.stdout
    # Everything else still comes through.
    assert "## Recent sessions" in result.stdout
    assert "never modify `originals/`" in result.stdout


def test_missing_every_optional_note_still_produces_a_briefing(vault: Path) -> None:
    for rel in (
        "Vault/00-System/Project Charter.md",
        "Vault/00-System/Project Roadmap.md",
        "Vault/00-System/Current State.md",
        "Vault/00-System/Environment Status.md",
        "Vault/70-Known-Unknowns/Known Unknowns.md",
        "Vault/50-Decisions/Decision Log.md",
        "Vault/90-Sessions/Session Index.md",
    ):
        (vault / rel).unlink()
    result = run(vault, "brief")
    assert result.returncode == briefing.EXIT_TOOL_NEGATIVE
    assert result.stdout.count("UNPARSED:") >= 6
    for marker in briefing.SIX_D3D_MARKERS:
        assert marker in result.stdout


def test_missing_start_here_refuses(vault: Path) -> None:
    (vault / "Vault/00-System/START HERE.md").unlink()
    result = run(vault, "brief")
    assert result.returncode == briefing.EXIT_REFUSAL
    payload = json.loads(result.stdout)
    assert payload["refused"] is True
    assert payload["tool"] == "briefing"
    assert payload["reason"] == "hard_rules_unparsed"


def test_malformed_milestone_table_degrades_gracefully(vault: Path) -> None:
    write(
        vault / "Vault/00-System/Project Roadmap.md",
        "# Project Roadmap\n\n## Roadmap status\n\nM1 is active, probably.\n",
    )
    result = run(vault, "brief")
    assert result.returncode == briefing.EXIT_TOOL_NEGATIVE
    assert "UNPARSED: Vault/00-System/Project Roadmap.md" in result.stdout
    assert "no milestone table" in result.stdout
    # It must not invent a milestone.
    assert "ACTIVE:" not in result.stdout
    # The current packet still arrives from Current State.
    assert "Run the synthetic grain-gate follow-up" in result.stdout


def test_table_without_an_active_row_is_reported(vault: Path) -> None:
    text = (vault / "Vault/00-System/Project Roadmap.md").read_text()
    write(
        vault / "Vault/00-System/Project Roadmap.md",
        text.replace("| Active |", "| Planned |"),
    )
    result = run(vault, "brief")
    assert result.returncode == briefing.EXIT_TOOL_NEGATIVE
    assert "lists no `Active` milestone" in result.stdout


def test_renamed_current_state_heading_degrades(vault: Path) -> None:
    text = (vault / "Vault/00-System/Current State.md").read_text()
    write(
        vault / "Vault/00-System/Current State.md",
        text.replace("## What should the next agent do?", "## Next steps"),
    )
    result = run(vault, "brief")
    assert result.returncode == briefing.EXIT_TOOL_NEGATIVE
    assert "UNPARSED: Vault/00-System/Current State.md" in result.stdout
    # The milestone table still parses.
    assert "ACTIVE: M1 — Synthetic reimplementation" in result.stdout


def test_missing_doctor_block_degrades(vault: Path) -> None:
    text = (vault / "Vault/00-System/Environment Status.md").read_text()
    write(
        vault / "Vault/00-System/Environment Status.md",
        text.split("<!-- BEGIN GENERATED: doctor -->")[0],
    )
    result = run(vault, "brief")
    assert result.returncode == briefing.EXIT_TOOL_NEGATIVE
    assert "BEGIN GENERATED: doctor" in result.stdout  # named in the UNPARSED line
    assert "rr / ntsync" in result.stdout  # annotations still parsed


def test_empty_session_index_falls_back_to_filenames(vault: Path) -> None:
    write(vault / "Vault/90-Sessions/Session Index.md", "# Session Index\n")
    write(vault / "Vault/90-Sessions/2026-01-04 1400 - Codex - fallback.md", "x\n")
    result = run(vault, "brief")
    assert "2026-01-04 1400 - Codex - fallback" in result.stdout
    assert "fell back to session filenames" in result.stdout


def test_completely_empty_vault_does_not_crash(tmp_path: Path) -> None:
    result = run(tmp_path, "brief")
    assert result.returncode == briefing.EXIT_REFUSAL
    assert json.loads(result.stdout)["refused"] is True
    result = run(tmp_path, "measure")
    assert result.returncode == briefing.EXIT_TOOL_NEGATIVE
    payload = json.loads(result.stdout)
    assert payload["mandated_startup_set"]["total_bytes"] == 0


# --------------------------------------------------------------------------
# Budget enforcement
# --------------------------------------------------------------------------


def _bulk_vault(root: Path) -> Path:
    make_vault(root)
    sessions = ["---\ntype: index\n---\n\n# Session Index\n"]
    for index in range(40):
        sessions.append(f"- [[2026-02-{index % 28 + 1:02d} 1200 - Codex - bulk {index}]]")
    write(root / "Vault/90-Sessions/Session Index.md", "\n".join(sessions) + "\n")

    decisions = ["---\ntype: register\n---\n\n# Decision Log\n"]
    for index in range(1, 41):
        decisions.append(
            f"## DEC-20260201-{index:03d} - Bulk decision {index}\n\n"
            f"- **Decision:** Do the bulk thing number {index} and nothing more.\n"
        )
    write(root / "Vault/50-Decisions/Decision Log.md", "\n".join(decisions))

    unknowns = ["---\ntype: register\n---\n\n# Known Unknowns\n"]
    for index in range(1, 41):
        unknowns.append(
            f"- **KU-{index:03d}:** Bulk synthetic question {index} is unanswered "
            "and remains entirely open for now."
        )
    write(
        root / "Vault/70-Known-Unknowns/Known Unknowns.md",
        "\n".join(unknowns) + "\n",
    )
    return root


def test_generous_budget_truncates_nothing(tmp_path: Path) -> None:
    root = _bulk_vault(tmp_path)
    payload = json.loads(
        run(
            root,
            "brief",
            "--format",
            "json",
            "--budget-tokens",
            "100000",
            "--decisions",
            "40",
            "--sessions",
            "40",
        ).stdout
    )
    assert payload["truncated_sections"] == []
    assert payload["budget_met"] is True


def test_budget_truncates_lowest_priority_sections_first(tmp_path: Path) -> None:
    root = _bulk_vault(tmp_path)
    payload = json.loads(
        run(
            root,
            "brief",
            "--format",
            "json",
            "--budget-tokens",
            "900",
            "--decisions",
            "40",
            "--sessions",
            "40",
        ).stdout
    )
    sections = {item["key"]: item for item in payload["sections"]}
    sessions = sections["recent_sessions"]
    decisions = sections["recent_decisions"]
    unknowns = sections["open_unknowns"]

    assert sessions["dropped_blocks"] > 0
    # A higher-priority section is only touched once the lower one is empty.
    if decisions["dropped_blocks"]:
        assert sessions["blocks"] == []
    if unknowns["dropped_blocks"]:
        assert decisions["blocks"] == []
    if sections["environment"]["dropped_blocks"]:
        assert unknowns["blocks"] == []


def test_budget_never_elides_the_safety_rules(tmp_path: Path) -> None:
    root = _bulk_vault(tmp_path)
    result = run(
        root,
        "brief",
        "--budget-tokens",
        str(briefing.MIN_BUDGET_TOKENS),
        "--decisions",
        "40",
        "--sessions",
        "40",
    )
    out = result.stdout
    for marker in briefing.SIX_D3D_MARKERS:
        assert marker in out
    assert "never modify `originals/`" in out
    assert "Runtime instance lifecycle" in out

    payload = json.loads(
        run(
            root,
            "brief",
            "--format",
            "json",
            "--budget-tokens",
            str(briefing.MIN_BUDGET_TOKENS),
        ).stdout
    )
    rules = next(s for s in payload["sections"] if s["key"] == "hard_rules")
    assert rules["dropped_blocks"] == 0
    assert rules["elidable"] is False
    assert len(rules["fixed"]) >= 8
    mapping = next(s for s in payload["sections"] if s["key"] == "map")
    assert mapping["elidable"] is False


def test_truncation_is_reported_in_the_output(tmp_path: Path) -> None:
    root = _bulk_vault(tmp_path)
    out = run(
        root, "brief", "--budget-tokens", "900", "--sessions", "40"
    ).stdout
    assert "Truncated `recent_sessions`" in out
    assert "entries omitted" in out
    assert "Budget: 900 estimated tokens" in out


def test_reported_token_estimate_matches_the_output(tmp_path: Path) -> None:
    root = _bulk_vault(tmp_path)
    payload = json.loads(
        run(root, "brief", "--format", "json", "--budget-tokens", "3000").stdout
    )
    markdown = run(root, "brief", "--budget-tokens", "3000").stdout
    # The markdown run prints a trailing newline the estimate does not count.
    assert payload["estimated_tokens"] <= math.ceil(
        len(markdown.encode("utf-8")) / briefing.BYTES_PER_TOKEN
    )
    assert payload["estimated_tokens"] <= 3000


# --------------------------------------------------------------------------
# --task selection
# --------------------------------------------------------------------------


def test_task_selects_the_matching_moc_and_experiment(vault: Path) -> None:
    out = run(vault, "brief", "--task", "grain gate resolver thresholds").stdout
    assert "## Suggested reading for: grain gate resolver thresholds" in out
    assert "Vault/01-MOCs/Subsystems MOC.md" in out
    assert "Vault/30-Experiments/EXP-20260101-001 - Grain gate resolver.md" in out
    assert "Camera reconnaissance" not in out
    assert "Keywords matched: grain, gate, resolver, thresholds" in out


def test_task_without_a_match_names_the_default_moc(vault: Path) -> None:
    out = run(vault, "brief", "--task", "zzzqqq wwwvvv yyyxxx").stdout
    assert "No MOC matched the task keywords" in out
    assert briefing.P_DEFAULT_MOC in out
    assert "No recent experiment note matched" in out


def test_task_section_absent_without_the_flag(vault: Path) -> None:
    assert "Suggested reading" not in run(vault, "brief").stdout


def test_task_of_only_stopwords_degrades(vault: Path) -> None:
    result = run(vault, "brief", "--task", "the and of it")
    assert result.returncode == briefing.EXIT_TOOL_NEGATIVE
    assert "UNPARSED: --task" in result.stdout


# --------------------------------------------------------------------------
# measure
# --------------------------------------------------------------------------


def test_measure_output_shape(vault: Path) -> None:
    result = run(vault, "measure")
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["tool"] == "briefing"
    assert "bytes / 4" in payload["token_estimate_method"]

    mandated = payload["mandated_startup_set"]
    assert len(mandated["files"]) == len(briefing.MANDATED_STARTUP_SET)
    for item in mandated["files"]:
        assert {"path", "exists", "bytes", "lines", "estimated_tokens"} <= set(item)
    assert mandated["total_bytes"] == sum(i["bytes"] for i in mandated["files"])
    assert mandated["total_lines"] == sum(i["lines"] for i in mandated["files"])
    assert mandated["total_estimated_tokens"] == sum(
        i["estimated_tokens"] for i in mandated["files"]
    )

    start_here = next(
        item for item in mandated["files"] if item["path"].endswith("START HERE.md")
    )
    on_disk = (vault / "Vault/00-System/START HERE.md").read_bytes()
    assert start_here["bytes"] == len(on_disk)
    assert start_here["estimated_tokens"] == math.ceil(len(on_disk) / 4)

    brief_stats = payload["briefing"]
    assert brief_stats["estimated_tokens"] > 0
    assert brief_stats["budget_tokens"] == briefing.DEFAULT_BUDGET_TOKENS
    assert brief_stats["unparsed"] == []
    assert payload["reduction"]["estimated_tokens_saved"] >= 0


def test_measure_flags_a_missing_mandated_file(vault: Path) -> None:
    (vault / "Vault/70-Known-Unknowns/Known Unknowns.md").unlink()
    result = run(vault, "measure")
    assert result.returncode == briefing.EXIT_TOOL_NEGATIVE
    payload = json.loads(result.stdout)
    missing = next(
        item
        for item in payload["mandated_startup_set"]["files"]
        if item["path"].endswith("Known Unknowns.md")
    )
    assert missing["exists"] is False
    assert any("Known Unknowns.md" in line for line in payload["briefing"]["unparsed"])


# --------------------------------------------------------------------------
# Formats, output, CLI surface
# --------------------------------------------------------------------------


def test_json_format_shape(vault: Path) -> None:
    result = run(vault, "brief", "--format", "json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["tool"] == "briefing"
    assert payload["status"] == "ok"
    assert payload["unparsed"] == []
    assert "NOT AUTHORITATIVE" in payload["notice"]
    keys = [section["key"] for section in payload["sections"]]
    assert keys == [
        "mission",
        "hard_rules",
        "milestones",
        "environment",
        "open_unknowns",
        "recent_decisions",
        "recent_sessions",
        "map",
    ]
    for section in payload["sections"]:
        assert {"key", "title", "elidable", "blocks", "pointers"} <= set(section)


def test_json_status_is_degraded_when_a_section_is_unparsed(vault: Path) -> None:
    (vault / "Vault/90-Sessions/Session Index.md").unlink()
    payload = json.loads(run(vault, "brief", "--format", "json").stdout)
    assert payload["status"] == "degraded"
    assert any("UNPARSED:" in line for line in payload["unparsed"])


def test_out_writes_the_briefing_to_a_file(vault: Path, tmp_path: Path) -> None:
    target = tmp_path / "out" / "brief.md"
    target.parent.mkdir()
    result = run(vault, "brief", "--out", str(target))
    assert result.returncode == 0
    assert "# ABLPC session briefing" in target.read_text()
    summary = json.loads(result.stdout)
    assert summary["out"] == str(target)
    assert summary["status"] == "ok"


def test_capabilities(vault: Path) -> None:
    result = run(vault, "--capabilities")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["tool"] == "briefing"
    assert payload["verbs"] == ["brief", "measure"]
    assert payload["limits"]["default_budget_tokens"] == 6000
    assert payload["limits"]["elision_order"][0] == "recent_sessions"
    assert "hard_rules" in payload["limits"]["non_elidable_sections"]
    assert set(payload["exit_codes"]) == {"0", "1", "2", "3"}


@pytest.mark.parametrize(
    "args",
    [
        ("nonsense",),
        ("brief", "--format", "xml"),
        ("brief", "--budget-tokens", "1"),
        ("brief", "--budget-tokens", "notanumber"),
        ("brief", "--sessions", "-1"),
        ("--capabilities", "brief"),
        (),
    ],
)
def test_usage_errors_exit_two(vault: Path, args: tuple[str, ...]) -> None:
    assert run(vault, *args).returncode == briefing.EXIT_USAGE


# --------------------------------------------------------------------------
# Unit-level parser behavior
# --------------------------------------------------------------------------


def test_parse_table_rejects_a_non_table() -> None:
    assert briefing.parse_table(["not a table", "at all"]) is None
    assert briefing.parse_table(["| a | b |", "no separator", "| 1 | 2 |"]) is None


def test_parse_table_reads_a_table() -> None:
    header, rows = briefing.parse_table(
        ["| A | B |", "|---|---|", "| 1 | 2 |", "| 3 | 4 |"]
    )
    assert header == ["A", "B"]
    assert rows == [["1", "2"], ["3", "4"]]


def test_split_headings_ignores_fenced_code() -> None:
    headings = briefing.split_headings(
        "# Title\n\n```\n# not a heading\n```\n\n## Real\n"
    )
    assert [h.title for h in headings] == ["Title", "Real"]
    assert "# not a heading" in "\n".join(headings[0].body)


def test_first_sentence_cuts_at_the_first_sentence_after_the_floor() -> None:
    text = (
        "This first sentence is comfortably longer than the forty-character "
        "floor. This second one must not appear."
    )
    assert briefing.first_sentence(text).endswith("floor.")
    assert "second one" not in briefing.first_sentence(text)
    # Below the floor nothing is cut, so an early abbreviation cannot truncate
    # a bullet down to a misleading fragment.
    assert briefing.first_sentence("Short one. Second one.") == (
        "Short one. Second one."
    )


def test_first_sentence_marks_truncation() -> None:
    assert briefing.first_sentence("x" * 400, 100).endswith("…")


def test_unparsed_line_names_the_file_and_the_instruction() -> None:
    line = briefing.unparsed("Vault/00-System/Thing.md", "no heading")
    assert line.startswith("UNPARSED: Vault/00-System/Thing.md")
    assert line.endswith("read it directly.")


def test_estimate_tokens_is_bytes_over_four() -> None:
    assert briefing.estimate_tokens("a" * 400) == 100
    assert briefing.estimate_tokens("") == 0
