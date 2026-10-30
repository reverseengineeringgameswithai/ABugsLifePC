"""Tests for scripts/claim-sweep.py.

All vaults are SYNTHETIC and built under ``tmp_path``; the real ``Vault/`` is
edited concurrently, so nothing here asserts on its content.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "claim-sweep.py"

EXIT_OK = 0
EXIT_NEGATIVE = 1
EXIT_USAGE = 2
EXIT_REFUSAL = 3


def write(vault: Path, rel: str, text: str) -> Path:
    path = vault / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """A synthetic repository root containing a small vault."""

    vault = tmp_path / "Vault"
    write(vault, "00-System/Current State.md",
          "# Current State\n\nThe census confirms 571 creatures.\n")
    write(vault, "20-Research/census.md",
          "# Census\n\nline one\nThe census confirms 571 creatures in the pool.\n")
    write(vault, "90-Sessions/2026-01-02 0900 - Codex - session.md",
          "# Session\n\nThe census confirms 572 creatures.\n")
    write(vault, "90-Sessions/notes.txt", "The census confirms 999 creatures.\n")
    return tmp_path


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["ABLPC_ROOT"] = str(repo)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def run_json(repo: Path, *args: str) -> tuple[dict, int]:
    result = run(repo, *args, "--json")
    assert result.stdout, result.stderr
    return json.loads(result.stdout), result.returncode


# --- sweep -------------------------------------------------------------------


def test_sweep_finds_every_occurrence(repo: Path) -> None:
    payload, code = run_json(repo, "sweep", "--phrase", "census confirms")
    assert code == EXIT_OK
    assert payload["tool"] == "claim-sweep"
    assert payload["subcommand"] == "sweep"
    assert payload["total_hits"] == 3
    assert payload["notes_with_hits"] == 3
    assert payload["notes_scanned"] == 3  # notes.txt is not a *.md note
    assert payload["hits_truncated"] is False
    assert payload["search_path"] == "Vault"
    assert [hit["path"] for hit in payload["hits"]] == [
        "Vault/00-System/Current State.md",
        "Vault/20-Research/census.md",
        "Vault/90-Sessions/2026-01-02 0900 - Codex - session.md",
    ]
    census = payload["hits"][1]
    assert census["line"] == 4
    assert census["column"] == 5
    assert "571 creatures" in census["context"]


def test_sweep_human_output_lists_path_and_line(repo: Path) -> None:
    result = run(repo, "sweep", "--phrase", "571 creatures")
    assert result.returncode == EXIT_OK
    assert "2 occurrences in 2 notes" in result.stdout
    assert "Vault/20-Research/census.md:4:" in result.stdout


def test_sweep_reports_zero_hits_without_failing(repo: Path) -> None:
    payload, code = run_json(repo, "sweep", "--phrase", "no such claim")
    assert code == EXIT_OK
    assert payload["total_hits"] == 0
    assert payload["hits"] == []


def test_sweep_regex_mode(repo: Path) -> None:
    payload, code = run_json(repo, "sweep", "--phrase", r"57[12] creatures", "--regex")
    assert code == EXIT_OK
    assert payload["regex"] is True
    assert payload["total_hits"] == 3
    assert {hit["match"] for hit in payload["hits"]} == {"571 creatures", "572 creatures"}


def test_sweep_literal_mode_does_not_interpret_metacharacters(repo: Path) -> None:
    payload, code = run_json(repo, "sweep", "--phrase", "57[12] creatures")
    assert code == EXIT_OK
    assert payload["total_hits"] == 0


def test_sweep_invalid_regex_is_a_usage_error(repo: Path) -> None:
    result = run(repo, "sweep", "--phrase", "(unclosed", "--regex")
    assert result.returncode == EXIT_USAGE
    assert "valid regular expression" in result.stderr


def test_sweep_empty_phrase_is_a_usage_error(repo: Path) -> None:
    result = run(repo, "sweep", "--phrase", "")
    assert result.returncode == EXIT_USAGE


def test_missing_required_argument_is_a_usage_error(repo: Path) -> None:
    assert run(repo, "sweep").returncode == EXIT_USAGE
    assert run(repo, "pair", "--old", "a").returncode == EXIT_USAGE
    assert run(repo, "numbers").returncode == EXIT_USAGE
    assert run(repo).returncode == EXIT_USAGE


def test_max_hits_truncates_and_reports_truncation(repo: Path) -> None:
    write(repo / "Vault", "20-Research/many.md",
          "# Many\n" + "The census confirms 571 creatures.\n" * 20)
    payload, code = run_json(repo, "sweep", "--phrase", "571 creatures", "--max-hits", "5")
    assert code == EXIT_OK
    assert payload["total_hits"] == 22
    assert len(payload["hits"]) == 5
    assert payload["hits_truncated"] is True


def test_context_is_bounded(repo: Path) -> None:
    write(repo / "Vault", "20-Research/long.md", "# Long\n\n" + "x" * 400 + " 571 creatures " + "y" * 400 + "\n")
    payload, code = run_json(repo, "sweep", "--phrase", "571 creatures", "--context", "40")
    assert code == EXIT_OK
    long_hit = [hit for hit in payload["hits"] if hit["path"].endswith("long.md")][0]
    assert "571 creatures" in long_hit["context"]
    assert len(long_hit["context"]) <= 40 + 6


def test_negative_max_hits_is_a_usage_error(repo: Path) -> None:
    assert run(repo, "sweep", "--phrase", "x", "--max-hits", "-1").returncode == EXIT_USAGE


def test_glob_and_path_options(repo: Path) -> None:
    payload, code = run_json(repo, "sweep", "--phrase", "census confirms",
                             "--path", "Vault/90-Sessions", "--glob", "*.txt")
    assert code == EXIT_OK
    assert payload["total_hits"] == 1
    assert payload["hits"][0]["path"] == "Vault/90-Sessions/notes.txt"


# --- pair --------------------------------------------------------------------


def test_pair_mixed_state_is_tool_negative(repo: Path) -> None:
    payload, code = run_json(repo, "pair", "--old", "571 creatures", "--new", "572 creatures")
    assert code == EXIT_NEGATIVE
    assert payload["state"] == "mixed"
    assert payload["mixed"] is True
    assert payload["old_total_hits"] == 2
    assert payload["old_notes"] == 2
    assert payload["new_total_hits"] == 1
    assert [hit["path"] for hit in payload["old_hits"]] == [
        "Vault/00-System/Current State.md",
        "Vault/20-Research/census.md",
    ]
    assert payload["hits_truncated"] is False


def test_pair_human_output_names_the_defect(repo: Path) -> None:
    result = run(repo, "pair", "--old", "571 creatures", "--new", "572 creatures")
    assert result.returncode == EXIT_NEGATIVE
    assert "MIXED: both wordings are present" in result.stdout
    assert "Vault/00-System/Current State.md:3:" in result.stdout


def test_pair_fully_propagated_is_ok(repo: Path) -> None:
    for rel in ("00-System/Current State.md", "20-Research/census.md"):
        path = repo / "Vault" / rel
        path.write_text(path.read_text(encoding="utf-8").replace("571", "572"), encoding="utf-8")
    payload, code = run_json(repo, "pair", "--old", "571 creatures", "--new", "572 creatures")
    assert code == EXIT_OK
    assert payload["state"] == "new_only"
    assert payload["old_total_hits"] == 0
    assert payload["new_total_hits"] == 3


def test_pair_uncorrected_tree_is_old_only(repo: Path) -> None:
    path = repo / "Vault" / "90-Sessions/2026-01-02 0900 - Codex - session.md"
    path.write_text(path.read_text(encoding="utf-8").replace("572", "571"), encoding="utf-8")
    payload, code = run_json(repo, "pair", "--old", "571 creatures", "--new", "572 creatures")
    assert code == EXIT_OK
    assert payload["state"] == "old_only"
    assert payload["old_total_hits"] == 3


def test_pair_absent_from_tree(repo: Path) -> None:
    payload, code = run_json(repo, "pair", "--old", "111 grains", "--new", "222 grains")
    assert code == EXIT_OK
    assert payload["state"] == "absent"


def test_pair_ignores_old_contained_in_new(tmp_path: Path) -> None:
    vault = tmp_path / "Vault"
    write(vault, "a.md", "The pool holds 572 confirmed creatures.\n")
    write(vault, "b.md", "The pool holds 572 confirmed creatures.\n")
    payload, code = run_json(tmp_path, "pair", "--old", "572", "--new", "572 confirmed")
    assert code == EXIT_OK
    assert payload["state"] == "new_only"
    assert payload["old_total_hits"] == 0
    assert payload["new_total_hits"] == 2
    assert payload["overlap_rule"] == "old hits contained in a new occurrence are ignored"


def test_pair_ignores_new_contained_in_old(tmp_path: Path) -> None:
    vault = tmp_path / "Vault"
    write(vault, "a.md", "The pool holds 572 confirmed creatures.\n")
    payload, code = run_json(tmp_path, "pair", "--old", "572 confirmed", "--new", "572")
    assert code == EXIT_OK
    assert payload["state"] == "old_only"
    assert payload["old_total_hits"] == 1
    assert payload["new_total_hits"] == 0
    assert payload["overlap_rule"] == "new hits contained in an old occurrence are ignored"


def test_pair_identical_wordings_is_a_usage_error(repo: Path) -> None:
    result = run(repo, "pair", "--old", "same", "--new", "same")
    assert result.returncode == EXIT_USAGE
    assert "must differ" in result.stderr


# --- numbers -----------------------------------------------------------------


def test_numbers_reports_conflicting_values(repo: Path) -> None:
    payload, code = run_json(repo, "numbers", "--pattern", r"confirms (\d+) creatures")
    assert code == EXIT_NEGATIVE
    assert payload["conflict"] is True
    assert payload["distinct_values"] == 2
    assert payload["capture_group"] == 1
    values = {entry["value"]: entry for entry in payload["values"]}
    assert set(values) == {"571", "572"}
    assert values["571"]["total_hits"] == 2
    assert values["571"]["notes"] == 2
    assert [hit["path"] for hit in values["572"]["hits"]] == [
        "Vault/90-Sessions/2026-01-02 0900 - Codex - session.md"
    ]
    assert payload["values"][0]["value"] == "571"  # numeric ordering


def test_numbers_human_output_flags_conflict(repo: Path) -> None:
    result = run(repo, "numbers", "--pattern", r"confirms (\d+) creatures")
    assert result.returncode == EXIT_NEGATIVE
    assert "CONFLICT: the pattern yields more than one distinct value" in result.stdout
    assert "value '571'" in result.stdout


def test_numbers_single_value_is_ok(repo: Path) -> None:
    path = repo / "Vault" / "90-Sessions/2026-01-02 0900 - Codex - session.md"
    path.write_text(path.read_text(encoding="utf-8").replace("572", "571"), encoding="utf-8")
    payload, code = run_json(repo, "numbers", "--pattern", r"confirms (\d+) creatures")
    assert code == EXIT_OK
    assert payload["conflict"] is False
    assert payload["distinct_values"] == 1
    assert payload["values"][0]["total_hits"] == 3


def test_numbers_without_capture_group_uses_whole_match(repo: Path) -> None:
    payload, code = run_json(repo, "numbers", "--pattern", r"57\d creatures")
    assert code == EXIT_NEGATIVE
    assert payload["capture_group"] == 0
    assert {entry["value"] for entry in payload["values"]} == {"571 creatures", "572 creatures"}


def test_numbers_no_match_is_ok(repo: Path) -> None:
    payload, code = run_json(repo, "numbers", "--pattern", r"nothing (\d+) here")
    assert code == EXIT_OK
    assert payload["distinct_values"] == 0
    assert payload["conflict"] is False


def test_numbers_truncates_per_value(repo: Path) -> None:
    write(repo / "Vault", "20-Research/many.md",
          "# Many\n" + "The census confirms 571 creatures.\n" * 10)
    payload, code = run_json(repo, "numbers", "--pattern", r"confirms (\d+) creatures",
                             "--max-hits", "3")
    assert code == EXIT_NEGATIVE
    values = {entry["value"]: entry for entry in payload["values"]}
    assert values["571"]["total_hits"] == 12
    assert len(values["571"]["hits"]) == 3
    assert values["571"]["hits_truncated"] is True
    assert payload["hits_truncated"] is True


def test_numbers_invalid_pattern_is_a_usage_error(repo: Path) -> None:
    result = run(repo, "numbers", "--pattern", "(")
    assert result.returncode == EXIT_USAGE


# --- refusals ----------------------------------------------------------------


def test_path_outside_repository_is_refused(repo: Path, tmp_path: Path) -> None:
    outside = tmp_path.parent / "definitely-outside"
    result = run(repo, "sweep", "--phrase", "x", "--path", str(outside))
    assert result.returncode == EXIT_REFUSAL
    payload = json.loads(result.stdout)
    assert payload == {
        "refused": True,
        "tool": "claim-sweep",
        "reason": payload["reason"],
    }
    assert "outside the repository root" in payload["reason"]


def test_missing_path_is_refused(repo: Path) -> None:
    result = run(repo, "sweep", "--phrase", "x", "--path", "Vault/00-Nope")
    assert result.returncode == EXIT_REFUSAL
    payload = json.loads(result.stdout)
    assert payload["refused"] is True
    assert payload["tool"] == "claim-sweep"
    assert "does not exist" in payload["reason"]


def test_ablpc_root_override_is_honored(repo: Path, tmp_path: Path) -> None:
    payload, code = run_json(repo, "sweep", "--phrase", "census confirms")
    assert code == EXIT_OK
    assert all(hit["path"].startswith("Vault/") for hit in payload["hits"])
