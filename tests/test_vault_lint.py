"""Tests for scripts/vault-lint.py.

Every functional test builds a SYNTHETIC vault under ``tmp_path``.  The real
``Vault/`` is edited concurrently by other agents, so only one tolerant
integration test touches it and that test asserts nothing about its content.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "vault-lint.py"
SUMMARY = "Vault lint:"


def run_lint(vault: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--vault", str(vault), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def write(vault: Path, rel: str, text: str) -> Path:
    path = vault / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


START_HERE = """---
type: system
status: active
updated: 2026-01-02
---

# START HERE

## Required startup sequence

1. Read `Vault/00-System/START HERE.md` (this note).
2. Read `Vault/00-System/Current State.md`.

## Before touching evidence

Nothing here.
"""

CURRENT_STATE = """---
type: system-state
updated: 2026-01-02
---

# Current State

See [[EXP-20260101-001 - synthetic probe]] and
[[2026-01-02 0900 - Codex - synthetic session]].
"""

EXPERIMENT = """---
type: experiment
id: EXP-20260101-001
date: 2026-01-01
question: does the linter still work
binary_sha256: abc123
environment: synthetic
result: pass
---

# EXP-20260101-001

## Result

Pass.
"""

SESSION = """---
type: session
date: 2026-01-02
agent: Codex
status: complete
---

# Synthetic session
"""


@pytest.fixture()
def clean_vault(tmp_path: Path) -> Path:
    """A synthetic vault that must lint with zero errors and zero warnings."""

    vault = tmp_path / "Vault"
    write(vault, "00-System/START HERE.md", START_HERE)
    write(vault, "00-System/Current State.md", CURRENT_STATE)
    write(vault, "30-Experiments/EXP-20260101-001 - synthetic probe.md", EXPERIMENT)
    write(vault, "90-Sessions/2026-01-02 0900 - Codex - synthetic session.md", SESSION)
    return vault


# --- preserved behavior ------------------------------------------------------


def test_clean_vault_passes_with_no_errors_or_warnings(clean_vault: Path) -> None:
    result = run_lint(clean_vault)
    assert result.returncode == 0, result.stdout
    assert "ERROR:" not in result.stdout
    assert "WARNING:" not in result.stdout
    assert result.stdout.strip().splitlines()[-1] == "Vault lint: 4 notes, 0 errors, 0 warnings"


def test_broken_wikilink_is_still_an_error(clean_vault: Path) -> None:
    write(
        clean_vault,
        "20-Research/probe.md",
        "---\ntype: research\n---\n\n# Probe\n\nSee [[No Such Note]].\n",
    )
    result = run_lint(clean_vault)
    assert result.returncode == 1
    assert "ERROR: Vault/20-Research/probe.md: broken wikilink [[No Such Note]]" in result.stdout
    assert result.stdout.strip().splitlines()[-1].startswith(SUMMARY)


def test_duplicate_ids_are_still_an_error(clean_vault: Path) -> None:
    write(clean_vault, "30-Experiments/EXP-20260101-001 - copy.md", EXPERIMENT)
    result = run_lint(clean_vault)
    assert result.returncode == 1
    assert "ERROR: duplicate ID EXP-20260101-001" in result.stdout


def test_malformed_frontmatter_is_still_an_error(clean_vault: Path) -> None:
    write(clean_vault, "20-Research/no-frontmatter.md", "# Just a heading\n")
    result = run_lint(clean_vault)
    assert result.returncode == 1
    assert "missing or malformed YAML frontmatter" in result.stdout


def test_missing_required_keys_is_still_an_error(clean_vault: Path) -> None:
    text = EXPERIMENT.replace("result: pass\n", "")
    write(clean_vault, "30-Experiments/EXP-20260101-002 - partial.md",
          text.replace("EXP-20260101-001", "EXP-20260101-002"))
    result = run_lint(clean_vault)
    assert result.returncode == 1
    assert "missing frontmatter keys: result" in result.stdout


def test_malformed_id_is_still_an_error(clean_vault: Path) -> None:
    text = EXPERIMENT.replace("id: EXP-20260101-001", "id: EXP-1-1")
    write(clean_vault, "30-Experiments/EXP-1-1 - bad id.md", text)
    result = run_lint(clean_vault)
    assert result.returncode == 1
    assert "malformed experiment ID 'EXP-1-1'" in result.stdout


def test_function_note_without_evidence_warns_but_does_not_error(clean_vault: Path) -> None:
    write(
        clean_vault,
        "20-Research/Functions/FUNC-ABC123-00418A20.md",
        "---\n"
        "type: function\n"
        "id: FUNC-ABC123-00418A20\n"
        "binary_sha256: abc123\n"
        "address: 0x00418A20\n"
        "status: unknown\n"
        "confidence: low\n"
        "evidence: []\n"
        "---\n\n"
        "# Function 0x00418A20\n\n"
        "## Confirmed\n\n"
        "It updates something.\n",
    )
    result = run_lint(clean_vault)
    assert result.returncode == 0
    assert "function note has no evidence references" in result.stdout


# --- context budget ----------------------------------------------------------


def test_budget_table_lists_mandated_documents(clean_vault: Path) -> None:
    result = run_lint(clean_vault)
    assert "Context budget" in result.stdout
    assert "Vault/00-System/START HERE.md" in result.stdout
    assert "Vault/00-System/Current State.md" in result.stdout
    assert "TOTAL of 2 mandated notes" in result.stdout


def test_budget_only_emits_json_and_exits_zero(clean_vault: Path) -> None:
    result = run_lint(clean_vault, "--budget-only")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["tool"] == "vault-lint"
    assert payload["report"] == "context-budget"
    assert payload["method"] == "estimated_tokens = bytes // 4"
    paths = [entry["path"] for entry in payload["documents"]]
    assert paths == ["Vault/00-System/START HERE.md", "Vault/00-System/Current State.md"]
    for entry in payload["documents"]:
        assert entry["exists"] is True
        assert entry["estimated_tokens"] == entry["bytes"] // 4
        assert entry["lines"] > 0
    total = payload["total"]
    assert total["documents"] == 2
    assert total["bytes"] == sum(entry["bytes"] for entry in payload["documents"])
    assert total["estimated_tokens"] == total["bytes"] // 4
    assert total["over_session_budget"] is False


def test_note_budget_warning_triggers_at_threshold(clean_vault: Path) -> None:
    report = json.loads(run_lint(clean_vault, "--budget-only").stdout)
    largest = max(report["documents"], key=lambda entry: entry["estimated_tokens"])
    tokens = largest["estimated_tokens"]

    below = run_lint(clean_vault, "--note-token-budget", str(tokens))
    assert below.returncode == 0
    assert "exceeds the" not in below.stdout

    above = run_lint(clean_vault, "--note-token-budget", str(tokens - 1))
    assert above.returncode == 0
    assert (
        f"{largest['path']}: {tokens} estimated tokens exceeds the "
        f"{tokens - 1}-token note budget" in above.stdout
    )


def test_session_budget_warning_triggers_at_threshold(clean_vault: Path) -> None:
    report = json.loads(run_lint(clean_vault, "--budget-only").stdout)
    total = report["total"]["estimated_tokens"]

    below = run_lint(clean_vault, "--session-token-budget", str(total))
    assert below.returncode == 0
    assert "exceeding the" not in below.stdout

    above = run_lint(clean_vault, "--session-token-budget", str(total - 1))
    assert above.returncode == 0
    assert f"mandated startup sequence totals {total} estimated tokens" in above.stdout
    assert f"exceeding the {total - 1}-token session budget" in above.stdout


def test_missing_mandated_document_warns(clean_vault: Path) -> None:
    text = START_HERE.replace(
        "2. Read `Vault/00-System/Current State.md`.",
        "2. Read `Vault/00-System/Current State.md`.\n3. Read `Vault/00-System/Ghost.md`.",
    )
    write(clean_vault, "00-System/START HERE.md", text)
    result = run_lint(clean_vault)
    assert result.returncode == 0
    assert "Vault/00-System/Ghost.md: mandated startup document does not exist" in result.stdout
    report = json.loads(run_lint(clean_vault, "--budget-only").stdout)
    ghost = [d for d in report["documents"] if d["path"].endswith("Ghost.md")][0]
    assert ghost == {
        "path": "Vault/00-System/Ghost.md",
        "exists": False,
        "bytes": 0,
        "lines": 0,
        "estimated_tokens": 0,
        "over_note_budget": False,
    }


def test_budget_falls_back_when_start_here_has_no_sequence(tmp_path: Path) -> None:
    vault = tmp_path / "Vault"
    write(vault, "00-System/START HERE.md", "---\ntype: system\n---\n\n# START HERE\n")
    write(vault, "00-System/Current State.md", "---\ntype: system-state\n---\n\n# Current State\n")
    report = json.loads(run_lint(vault, "--budget-only").stdout)
    paths = [entry["path"] for entry in report["documents"]]
    assert paths == ["Vault/00-System/START HERE.md", "Vault/00-System/Current State.md"]
    assert all(entry["exists"] for entry in report["documents"])


# --- staleness ---------------------------------------------------------------


def test_stale_state_note_warns(clean_vault: Path) -> None:
    write(clean_vault, "00-System/Current State.md",
          CURRENT_STATE.replace("updated: 2026-01-02", "updated: 2026-01-01"))
    result = run_lint(clean_vault)
    assert result.returncode == 0
    assert (
        "Vault/00-System/Current State.md: updated: 2026-01-01 is older than "
        "the newest session note date 2026-01-02" in result.stdout
    )


def test_state_note_current_with_newest_session_is_quiet(clean_vault: Path) -> None:
    write(clean_vault, "90-Sessions/2026-01-01 0900 - Codex - older session.md",
          SESSION.replace("date: 2026-01-02", "date: 2026-01-01"))
    write(clean_vault, "00-System/Current State.md",
          CURRENT_STATE.replace(
              "[[2026-01-02 0900 - Codex - synthetic session]]",
              "[[2026-01-02 0900 - Codex - synthetic session]] and\n"
              "[[2026-01-01 0900 - Codex - older session]]",
          ))
    result = run_lint(clean_vault)
    assert result.returncode == 0
    assert "older than the newest session note date" not in result.stdout


def test_iso_timestamp_updated_values_parse(clean_vault: Path) -> None:
    write(clean_vault, "00-System/Current State.md",
          CURRENT_STATE.replace("updated: 2026-01-02", "updated: 2026-01-01T22:33:44+01:00"))
    result = run_lint(clean_vault)
    assert "updated: 2026-01-01 is older than" in result.stdout


# --- orphans -----------------------------------------------------------------


def test_orphan_notes_are_warned_and_listable(clean_vault: Path) -> None:
    write(clean_vault, "20-Research/lonely.md", "---\ntype: research\n---\n\n# Lonely\n")
    result = run_lint(clean_vault)
    assert result.returncode == 0
    assert "1 notes have no inbound wikilink" in result.stdout
    assert "ORPHAN:" not in result.stdout

    listed = run_lint(clean_vault, "--list-orphans")
    assert "ORPHAN: Vault/20-Research/lonely.md" in listed.stdout


def test_entry_points_are_not_orphans(clean_vault: Path) -> None:
    write(clean_vault, "00-System/Naming Conventions.md", "---\ntype: policy\n---\n\n# Naming\n")
    write(clean_vault, "99-Templates/Session.md", "---\ntype: session\ndate:\n---\n\n# Session\n")
    write(clean_vault, "01-MOCs/Reverse Engineering MOC.md", "---\ntype: moc\n---\n\n# RE MOC\n")
    result = run_lint(clean_vault)
    assert result.returncode == 0
    assert "no inbound wikilink" not in result.stdout


def test_self_link_does_not_rescue_an_orphan(clean_vault: Path) -> None:
    write(clean_vault, "20-Research/selfish.md",
          "---\ntype: research\n---\n\n# Selfish\n\nSee [[selfish]].\n")
    result = run_lint(clean_vault)
    assert "1 notes have no inbound wikilink" in result.stdout


# --- json --------------------------------------------------------------------


def test_json_result_shape(clean_vault: Path) -> None:
    result = run_lint(clean_vault, "--json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["tool"] == "vault-lint"
    assert payload["ok"] is True
    assert payload["errors"] == []
    assert payload["warnings"] == []
    assert payload["orphans"] == []
    assert payload["stale_state_notes"] == []
    assert payload["newest_session_date"] == "2026-01-02"
    assert payload["counts"] == {
        "notes": 4,
        "errors": 0,
        "warnings": 0,
        "orphans": 0,
        "stale_state_notes": 0,
    }
    assert payload["budget"]["total"]["documents"] == 2
    assert "documents" in payload["budget"]


def test_json_result_reports_errors_and_exit_one(clean_vault: Path) -> None:
    write(clean_vault, "20-Research/probe.md",
          "---\ntype: research\n---\n\n# Probe\n\nSee [[Nope]].\n")
    result = run_lint(clean_vault, "--json")
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["counts"]["errors"] == 1
    assert "broken wikilink [[Nope]]" in payload["errors"][0]
    assert payload["counts"]["orphans"] == 1
    assert payload["orphans"] == ["Vault/20-Research/probe.md"]


def test_unknown_flag_is_a_usage_error(clean_vault: Path) -> None:
    result = run_lint(clean_vault, "--no-such-flag")
    assert result.returncode == 2


# --- tolerant integration ----------------------------------------------------


def test_real_vault_still_lints_clean() -> None:
    vault = ROOT / "Vault"
    if not vault.is_dir():
        pytest.skip("Vault/ is not present")
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        check=False,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip().splitlines()[-1].startswith(SUMMARY)
    assert " 0 errors," in result.stdout.strip().splitlines()[-1]
