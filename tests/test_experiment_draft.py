from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import note_utils  # noqa: E402

from test_run_index import (  # noqa: E402
    GDB_METADATA, GDB_RESULT, GDB_SPEC, POS_METADATA, WINE_METADATA,
    write_note, write_run,
)


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


draft = _load("experiment_draft", "experiment-draft.py")

GDB_RUN = "RUN-GDB-20260813-101022"
WINE_RUN = "RUN-WINE-20260812-150528"
POS_RUN = "RUN-POS-20260815-181852"


@pytest.fixture()
def sandbox(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    write_run(tmp_path, GDB_RUN, {
        "metadata.json": GDB_METADATA,
        "result.json": GDB_RESULT,
        "spec.resolved.json": GDB_SPEC,
        "stops.jsonl": '{"seq": 1}\n{"seq": 2}\n',
        "debugger-evidence.txt": "cleanup verified\n",
        "gdb-stdout.txt": "raw\n",
    })
    write_run(tmp_path, WINE_RUN, {
        "metadata.json": WINE_METADATA,
        "experiment.md": "# run\n",
        "bugs.log": "NextLife\n",
    })
    write_run(tmp_path, POS_RUN, {"metadata.json": POS_METADATA})
    (tmp_path / "Vault" / "30-Experiments").mkdir(parents=True)
    monkeypatch.setenv("ABLPC_ROOT", str(tmp_path))
    return tmp_path


def run_cli(args: list[str], root: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ, ABLPC_ROOT=str(root))
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "experiment-draft.py"), *args],
        capture_output=True, text=True, env=env,
    )


def frontmatter(text: str) -> dict:
    import yaml

    assert text.startswith("---\n")
    end = text.find("\n---\n", 4)
    assert end > 0
    return yaml.safe_load(text[4:end])


# --------------------------------------------------------------------------
# YAML scalar safety
# --------------------------------------------------------------------------


@pytest.mark.parametrize("value", [
    "plain text",
    "/home/dev/ABLPC/work/copies/EXP/control/PC/BUGS",
    "Fedora Linux 44, wine-11.0 (Staging)",
    "gdb-harness 1.5.0; GNU gdb (Fedora Linux) 17.1-6.fc44",
    "Does the reader bound counts?",
    "a: colon",
    "# hash",
    "- leading dash",
    "  padded  ",
    "true",
    "null",
    'quote " inside',
    "brace {a} bracket [b]",
    "back\\slash",
])
def test_yaml_scalar_round_trips(value: str) -> None:
    import yaml

    emitted = f"key: {draft.yaml_scalar(value)}"
    assert yaml.safe_load(emitted)["key"] == value


def test_yaml_block_list() -> None:
    import yaml

    assert yaml.safe_load(draft.yaml_block("artifacts", [])) == {"artifacts": []}
    parsed = yaml.safe_load(draft.yaml_block("artifacts", ["a/b", "c: d"]))
    assert parsed == {"artifacts": ["a/b", "c: d"]}


# --------------------------------------------------------------------------
# Frontmatter completeness and fidelity
# --------------------------------------------------------------------------


def test_frontmatter_is_filled_from_receipts(sandbox: Path) -> None:
    records = draft.gather_runs([GDB_RUN], sandbox)
    note = draft.render_note("EXP-20260813-050", "Does the harness bound stops?", records)
    data = frontmatter(note)

    assert data["type"] == "experiment"
    assert data["id"] == "EXP-20260813-050"
    assert data["question"] == "Does the harness bound stops?"
    assert data["binary_sha256"] == GDB_METADATA["executable_sha256"]
    assert data["environment"] == GDB_METADATA["environment"]
    assert data["working_directory"] == GDB_METADATA["working_directory"]
    assert "gdb-harness 1.2.0" in data["environment_version"]
    assert GDB_METADATA["debugger"] in data["environment_version"]
    assert GDB_RUN in data["configuration"]
    assert data["result"] == "pending"
    # date comes from the run stamp, not from today.
    assert str(data["date"]) == "2026-08-13"

    # Addresses use the Vault's existing unquoted 0x form, so YAML resolves
    # them to ints on load; the emitted text is what the corpus is written in.
    assert "addresses:\n  - 0x0044C898\n  - 0x0059F7F0\n  - 0x005B18E0\n" in note
    assert "file_offsets:\n  - 0x0A6C\n" in note
    assert data["addresses"] == [0x0044C898, 0x0059F7F0, 0x005B18E0]
    assert data["file_offsets"] == [0x0A6C]
    assert f"dynamic/wine/{GDB_RUN}" in data["artifacts"]
    assert f"dynamic/wine/{GDB_RUN}/spec.resolved.json" in data["artifacts"]
    # Raw debugger output is not a notable receipt file.
    assert f"dynamic/wine/{GDB_RUN}/gdb-stdout.txt" not in data["artifacts"]

    # None of the template's keys is left out.
    template = frontmatter((REPO / "Vault/99-Templates/Experiment.md").read_text())
    assert set(template) <= set(data)


def test_multiple_runs_merge_addresses_and_flag_divergence(sandbox: Path) -> None:
    records = draft.gather_runs([GDB_RUN, POS_RUN], sandbox)
    note = draft.render_note("EXP-20260813-051", "Two shapes?", records)
    data = frontmatter(note)

    # Both environments are transcribed, and the divergence is surfaced.
    assert GDB_METADATA["environment"] in data["environment"]
    assert "host Fedora Linux 44" in data["environment"]
    assert "## Generator warnings" in note
    assert "more than one environment or working directory" in note
    assert f"dynamic/wine/{POS_RUN}" in data["artifacts"]


def test_receipt_without_spec_yields_empty_address_lists(sandbox: Path) -> None:
    records = draft.gather_runs([WINE_RUN], sandbox)
    note = draft.render_note("EXP-20260812-020", "Wine?", records)
    data = frontmatter(note)
    assert data["addresses"] == []
    assert data["file_offsets"] == []
    assert data["binary_sha256"] == WINE_METADATA["executable_sha256"]
    # The wine receipt records no tool stamp at all, so the key is left blank
    # rather than filled with a guess -- exactly as the template leaves it.
    assert "environment_version:\n" in note
    assert data["environment_version"] is None


def test_missing_executable_sha_is_warned_not_invented(sandbox: Path) -> None:
    write_run(sandbox, "RUN-CORE-20260814-101010", {
        "metadata.json": {"run_id": "RUN-CORE-20260814-101010", "status": "complete"},
    })
    records = draft.gather_runs(["RUN-CORE-20260814-101010"], sandbox)
    note = draft.render_note("EXP-20260814-001", "No hash?", records)
    data = frontmatter(note)
    assert data["binary_sha256"] is None
    assert "binary_sha256:\n" in note
    assert "no receipt recorded an executable SHA-256" in note
    # A blank key is surfaced, never quietly shipped.
    assert "no receipt recorded environment or working_directory" in note


# --------------------------------------------------------------------------
# Body: evidence tables, TODOs, and asserting nothing
# --------------------------------------------------------------------------


def test_body_has_the_standard_headings(sandbox: Path) -> None:
    records = draft.gather_runs([GDB_RUN], sandbox)
    note = draft.render_note("EXP-20260813-052", "Bounded?", records)
    for heading in (
        "## Question", "## Procedure", "## Expected", "## Observed",
        "## Interpretation", "## Result", "## Follow-up",
    ):
        assert f"\n{heading}\n" in note


def test_evidence_table_carries_receipt_facts_and_hashes(sandbox: Path) -> None:
    records = draft.gather_runs([GDB_RUN], sandbox)
    note = draft.render_note("EXP-20260813-053", "Bounded?", records)

    assert "| run | kind | tool | tool version | status | accepted |" in note
    assert "| `RUN-GDB-20260813-101022` | GDB | gdb-harness | 1.2.0 | capture_complete | true | 400 | 2 | 3 |" in note

    table = note.split("| artifact | bytes | sha256 |", 1)[1].split("\n## ", 1)[0]
    # Every retained file in the run directory is hashed in the table, not
    # only the ones named in the frontmatter artifacts list.
    for name in ("metadata.json", "result.json", "spec.resolved.json",
                 "stops.jsonl", "debugger-evidence.txt", "gdb-stdout.txt"):
        assert f"`dynamic/wine/{GDB_RUN}/{name}`" in table
    assert len(re.findall(r"\| `[0-9a-f]{64}` \|", table)) == 6
    # The hashes are the real digests of the sandbox files.
    import hashlib
    digest = hashlib.sha256(
        (sandbox / "dynamic/wine" / GDB_RUN / "stops.jsonl").read_bytes()
    ).hexdigest()
    assert f"`{digest}`" in table


def test_every_unwritten_section_is_marked_todo(sandbox: Path) -> None:
    records = draft.gather_runs([GDB_RUN], sandbox)
    note = draft.render_note("EXP-20260813-054", "Bounded?", records)
    for heading in ("Procedure", "Expected", "Observed", "Interpretation",
                    "Result", "Follow-up"):
        section = note.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]
        assert "TODO:" in section, heading


def test_generator_asserts_no_interpretation_or_result(sandbox: Path) -> None:
    records = draft.gather_runs([GDB_RUN, WINE_RUN], sandbox)
    note = draft.render_note("EXP-20260813-055", "Bounded?", records)

    interpretation = note.split("## Interpretation\n", 1)[1].split("\n## ", 1)[0]
    assert interpretation.strip().startswith("TODO:")
    assert "cannot interpret" in interpretation

    result = note.split("## Result\n", 1)[1].split("\n## ", 1)[0]
    assert "Pending." in result
    assert frontmatter(note)["result"] == "pending"

    # Provenance names the tool, its version, and every source run id.
    assert "Generated by `scripts/experiment-draft.py` 1.0.0" in note
    assert f"`{GDB_RUN}`" in note and f"`{WINE_RUN}`" in note


def test_note_emits_no_wikilinks(sandbox: Path) -> None:
    records = draft.gather_runs([GDB_RUN, WINE_RUN, POS_RUN], sandbox)
    note = draft.render_note("EXP-20260813-056", "Bounded?", records)
    assert "[[" not in note


# --------------------------------------------------------------------------
# Id allocation and no-overwrite
# --------------------------------------------------------------------------


def test_allocates_the_next_free_id(sandbox: Path) -> None:
    day = note_utils.now().strftime("%Y%m%d")
    write_note(sandbox, f"30-Experiments/EXP-{day}-004 - prior.md",
               f"---\ntype: experiment\nid: EXP-{day}-004\n---\n")
    proc = run_cli(["--question", "Does it allocate?", "--run", GDB_RUN], sandbox)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["id"] == f"EXP-{day}-005"
    assert Path(payload["path"]).name == f"EXP-{day}-005 - does-it-allocate.md"
    assert Path(payload["path"]).exists()


def test_refuses_to_overwrite_an_existing_note(sandbox: Path) -> None:
    out = "Vault/30-Experiments/taken.md"
    (sandbox / out).write_text("mine\n", encoding="utf-8")
    proc = run_cli(["--question", "Q?", "--run", GDB_RUN, "--out", out], sandbox)
    assert proc.returncode == 3
    payload = json.loads(proc.stdout)
    assert payload["refused"] is True
    assert payload["reason"] == "note_exists"
    assert (sandbox / out).read_text() == "mine\n"


def test_refuses_a_colliding_explicit_id(sandbox: Path) -> None:
    write_note(sandbox, "30-Experiments/EXP-20260813-060 - taken.md",
               "---\ntype: experiment\nid: EXP-20260813-060\n---\n")
    proc = run_cli(
        ["--question", "Q?", "--run", GDB_RUN, "--id", "EXP-20260813-060"], sandbox
    )
    assert proc.returncode == 3
    assert json.loads(proc.stdout)["reason"] == "id_collision"


def test_refuses_a_malformed_explicit_id(sandbox: Path) -> None:
    proc = run_cli(["--question", "Q?", "--run", GDB_RUN, "--id", "EXP-2026-1"], sandbox)
    assert proc.returncode == 3
    assert json.loads(proc.stdout)["reason"] == "bad_id"


# --------------------------------------------------------------------------
# Refusals
# --------------------------------------------------------------------------


def test_refuses_a_missing_run_rather_than_drafting_blanks(sandbox: Path) -> None:
    proc = run_cli(["--question", "Q?", "--run", "RUN-GDB-19700101-000000"], sandbox)
    assert proc.returncode == 3
    payload = json.loads(proc.stdout)
    assert payload["reason"] == "run_not_found"
    assert payload["tool"] == "experiment-draft"
    assert not list((sandbox / "Vault/30-Experiments").glob("*.md"))


def test_refuses_when_one_of_several_runs_is_missing(sandbox: Path) -> None:
    proc = run_cli(
        ["--question", "Q?", "--run", GDB_RUN, "--run", "RUN-WINE-19700101-000000"],
        sandbox,
    )
    assert proc.returncode == 3
    assert json.loads(proc.stdout)["reason"] == "run_not_found"


def test_refuses_unreadable_metadata(sandbox: Path) -> None:
    write_run(sandbox, "RUN-GDB-20260814-121212", {"metadata.json": "{ broken"})
    proc = run_cli(["--question", "Q?", "--run", "RUN-GDB-20260814-121212"], sandbox)
    assert proc.returncode == 3
    payload = json.loads(proc.stdout)
    assert payload["reason"] == "metadata_unreadable"
    assert "malformed JSON" in payload["detail"]


def test_refuses_absent_metadata(sandbox: Path) -> None:
    write_run(sandbox, "RUN-GDB-20260814-131313", {"other.txt": "x"})
    proc = run_cli(["--question", "Q?", "--run", "RUN-GDB-20260814-131313"], sandbox)
    assert proc.returncode == 3
    assert json.loads(proc.stdout)["reason"] == "metadata_unreadable"


def test_refuses_a_run_id_with_a_path_separator(sandbox: Path) -> None:
    proc = run_cli(["--question", "Q?", "--run", "../../etc"], sandbox)
    assert proc.returncode == 3
    assert json.loads(proc.stdout)["reason"] == "bad_run_id"


def test_usage_errors(sandbox: Path) -> None:
    assert run_cli(["--run", GDB_RUN], sandbox).returncode == 2
    assert run_cli(["--question", "Q?"], sandbox).returncode == 2


def test_stdout_mode_writes_nothing(sandbox: Path) -> None:
    proc = run_cli(["--question", "Q?", "--run", GDB_RUN, "--stdout"], sandbox)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.startswith("---\ntype: experiment\n")
    assert not list((sandbox / "Vault/30-Experiments").glob("*.md"))


def test_capabilities(sandbox: Path) -> None:
    proc = run_cli(["--capabilities"], sandbox)
    assert proc.returncode == 0
    caps = json.loads(proc.stdout)
    assert caps["tool"] == "experiment-draft"
    assert caps["asserts_interpretation"] is False
    assert caps["asserts_result"] is False
    assert caps["overwrites_existing_notes"] is False
    assert caps["emits_wikilinks"] is False


def test_script_is_executable() -> None:
    assert os.access(SCRIPTS / "experiment-draft.py", os.X_OK)


# --------------------------------------------------------------------------
# The generated note must survive the real linter
# --------------------------------------------------------------------------


def test_generated_note_passes_the_real_vault_lint(sandbox: Path, tmp_path: Path) -> None:
    """Run the repository's own vault-lint.py over a sandbox Vault.

    ``vault-lint.py`` derives its root from its own location, so the real
    script is copied into the sandbox rather than reimplemented; this asserts
    against the actual linter, not a stand-in for it.
    """

    proc = run_cli([
        "--question", "Does the resolved spec bound every hardware point?",
        "--run", GDB_RUN, "--run", WINE_RUN, "--run", POS_RUN,
    ], sandbox)
    assert proc.returncode == 0, proc.stderr
    note_path = Path(json.loads(proc.stdout)["path"])
    assert note_path.is_relative_to(sandbox / "Vault")

    lint_root = tmp_path / "lint-root"
    (lint_root / "scripts").mkdir(parents=True)
    shutil.copy2(SCRIPTS / "vault-lint.py", lint_root / "scripts" / "vault-lint.py")
    shutil.copytree(sandbox / "Vault", lint_root / "Vault")

    lint = subprocess.run(
        [sys.executable, str(lint_root / "scripts" / "vault-lint.py")],
        capture_output=True, text=True,
    )
    assert "ERROR" not in lint.stdout, lint.stdout
    assert lint.returncode == 0, lint.stdout + lint.stderr
    assert "0 errors" in lint.stdout


def test_generated_note_lints_clean_beside_other_notes(sandbox: Path, tmp_path: Path) -> None:
    """A second generated note must not collide with the first one's id."""

    first = run_cli(["--question", "First question?", "--run", GDB_RUN], sandbox)
    assert first.returncode == 0, first.stderr
    second = run_cli(["--question", "Second question?", "--run", WINE_RUN], sandbox)
    assert second.returncode == 0, second.stderr
    assert json.loads(first.stdout)["id"] != json.loads(second.stdout)["id"]

    lint_root = tmp_path / "lint-two"
    (lint_root / "scripts").mkdir(parents=True)
    shutil.copy2(SCRIPTS / "vault-lint.py", lint_root / "scripts" / "vault-lint.py")
    shutil.copytree(sandbox / "Vault", lint_root / "Vault")
    lint = subprocess.run(
        [sys.executable, str(lint_root / "scripts" / "vault-lint.py")],
        capture_output=True, text=True,
    )
    assert lint.returncode == 0, lint.stdout + lint.stderr
    assert "ERROR" not in lint.stdout, lint.stdout
    assert len(list((lint_root / "Vault").rglob("*.md"))) == 2


@pytest.mark.skipif(
    not (REPO / "dynamic" / "wine" / "RUN-GDB-20260813-101022").is_dir(),
    reason="real run directory is absent",
)
def test_real_receipt_drafts_and_lints(tmp_path: Path) -> None:
    env = dict(os.environ)
    env.pop("ABLPC_ROOT", None)
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "experiment-draft.py"),
         "--question", "Does the real receipt fill the note?",
         "--run", "RUN-GDB-20260813-101022", "--stdout"],
        capture_output=True, text=True, env=env,
    )
    assert proc.returncode == 0, proc.stderr
    data = frontmatter(proc.stdout)
    assert data["binary_sha256"] == (
        "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
    )
    assert "addresses:\n  - 0x0044C898\n  - 0x0044C89E\n" in proc.stdout
    assert str(data["date"]) == "2026-08-13"

    lint_root = tmp_path / "lint-real"
    (lint_root / "scripts").mkdir(parents=True)
    (lint_root / "Vault" / "30-Experiments").mkdir(parents=True)
    shutil.copy2(SCRIPTS / "vault-lint.py", lint_root / "scripts" / "vault-lint.py")
    (lint_root / "Vault" / "30-Experiments" / "generated.md").write_text(
        proc.stdout, encoding="utf-8"
    )
    lint = subprocess.run(
        [sys.executable, str(lint_root / "scripts" / "vault-lint.py")],
        capture_output=True, text=True,
    )
    assert lint.returncode == 0, lint.stdout + lint.stderr
