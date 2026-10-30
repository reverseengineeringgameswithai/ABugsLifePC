from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))


def _load_run_index():
    spec = importlib.util.spec_from_file_location("run_index", SCRIPTS / "run-index.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


run_index = _load_run_index()


# --------------------------------------------------------------------------
# Sandbox construction
# --------------------------------------------------------------------------


GDB_METADATA = {
    "run_id": "RUN-GDB-20260813-101022",
    "experiment_id": "EXP-20260813-038",
    "tool": "gdb-harness",
    "tool_version": "1.2.0",
    "schema_version": 3,
    "executable_sha256": "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878",
    "environment": "Fedora Linux 44, wine-11.0 (Staging)",
    "debugger": "GNU gdb (Fedora Linux) 17.1-6.fc44",
    "working_directory": "/sandbox/work/copies/EXP/control/PC/BUGS",
    "target_pid": 4242,
    "status": "capture_complete",
}

GDB_RESULT = {
    "tool": "gdb-harness",
    "tool_version": "1.2.0",
    "schema_version": 3,
    "spec_schema_version": 3,
    "time_window_start": "2026-08-13T10:10:22.533090-04:00",
    "time_window_end": "2026-08-13T10:10:24.900000-04:00",
    "log_start_offset": 64723,
    "completion": {
        "completed": True,
        "accepted": True,
        "stop_reason": "capture_complete",
        "stops_observed": 400,
        "cleanup_verified": True,
        "detached": True,
    },
}

GDB_SPEC = {
    "schema_version": 5,
    "experiment_id": "EXP-20260813-038",
    "target": {
        "mode": "pid",
        "expected_exe_sha256": "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878",
    },
    "watchpoints": [
        {"id": "batch_pre", "address": "0x0059F7F0", "kind": "access", "size": 2},
        {"id": "entry_post", "address": "0x005B18E0", "kind": "access", "size": 4},
    ],
    "breakpoints": [{"id": "entry_pre", "address": 0x0044C898}],
    "direct3d_batch_capture": {"candidate_record_offsets": [0x0A6C]},
}

WINE_METADATA = {
    "run_id": "RUN-WINE-20260812-150528",
    "experiment": "EXP-20260812-020",
    "capture_sequence_started": "2026-08-12T15:05:28.497781425-04:00",
    "capture_sequence_ended": "2026-08-12T15:05:32.318801420-04:00",
    "executable_sha256": "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878",
    "environment": "Fedora Linux 44, Wine 11.0 Staging, Gamescope 3.16.25",
    "working_directory": "/sandbox/work/copies/EXP/control/PC/BUGS",
    "status": "captured then intentionally terminated",
    "tracked_artifacts": ["bugs.log", "experiment.md", "metadata.json"],
}

# The POS receipt shape records environment as an object and the executable
# hash under target.sha256 rather than at the top level.
POS_METADATA = {
    "schema": 1,
    "run_id": "RUN-POS-20260815-181852",
    "started_at": "2026-08-15T18:18:52-04:00",
    "environment": {"host": "Fedora Linux 44", "wine": "11.0 Staging"},
    "target": {
        "path": "work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe",
        "sha256": "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878",
    },
    "experiment": "EXP-20260815-128",
}

# The input-movie receipt shape records acceptance at the top level and the
# executable hash only inside the ownership proof.
INP_METADATA = {
    "run_id": "RUN-INP-REP-20260815-170119",
    "tool": "input-movie",
    "tool_version": "1.2.0",
    "schema_version": 1,
    "mode": "replay",
    "accepted": False,
    "status": "complete",
    "ownership": {
        "pid": 55300,
        "exe_sha256": "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878",
        "verified": True,
    },
}


def write_run(root: Path, run_id: str, files: dict[str, object]) -> Path:
    run_dir = root / "dynamic" / "wine" / run_id
    run_dir.mkdir(parents=True)
    for name, payload in files.items():
        path = run_dir / name
        if isinstance(payload, (dict, list)):
            path.write_text(json.dumps(payload), encoding="utf-8")
        else:
            path.write_text(str(payload), encoding="utf-8")
    return run_dir


def write_note(root: Path, rel: str, body: str) -> Path:
    path = root / "Vault" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


@pytest.fixture()
def sandbox(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A synthetic repo root with one run of each receipt shape."""

    write_run(tmp_path, "RUN-GDB-20260813-101022", {
        "metadata.json": GDB_METADATA,
        "result.json": GDB_RESULT,
        "spec.resolved.json": GDB_SPEC,
        "stops.jsonl": '{"seq": 1}\n{"seq": 2}\n{"seq": 3}\n',
        "debugger-evidence.txt": "cleanup verified\n",
    })
    write_run(tmp_path, "RUN-WINE-20260812-150528", {
        "metadata.json": WINE_METADATA,
        "experiment.md": "# RUN-WINE-20260812-150528\n",
        "bugs.log": "NextLife\n",
    })
    write_run(tmp_path, "RUN-POS-20260815-181852", {
        "metadata.json": POS_METADATA,
        "position-trace.tsv": "x\ty\tz\n",
    })
    write_run(tmp_path, "RUN-INP-REP-20260815-170119", {"metadata.json": INP_METADATA})

    write_note(tmp_path, "30-Experiments/EXP-20260813-038 - gdb.md", (
        "---\ntype: experiment\nid: EXP-20260813-038\n---\n\n"
        "The accepted run is `RUN-GDB-20260813-101022`.\n"
        "See also dynamic/wine/RUN-WINE-20260812-150528 for the control.\n"
    ))
    write_note(tmp_path, "30-Experiments/EXP-20260815-128 - pos.md", (
        "---\ntype: experiment\nid: EXP-20260815-128\n---\n\n"
        "Wikilinked evidence: [[dynamic/wine/RUN-POS-20260815-181852]].\n"
        "A citation with no directory: RUN-GDB-20991231-235959.\n"
    ))
    monkeypatch.setenv("ABLPC_ROOT", str(tmp_path))
    return tmp_path


# --------------------------------------------------------------------------
# Run id parsing
# --------------------------------------------------------------------------


def test_parse_run_id_plain_and_suffixed() -> None:
    plain = run_index.parse_run_id("RUN-GDB-20260813-101022")
    assert plain["kind"] == "GDB"
    assert plain["suffix"] is None
    assert plain["stamp_iso"] == "2026-08-13T10:10:22"

    suffixed = run_index.parse_run_id("RUN-WINE-20260811-232606-WINDOW-PROBE")
    assert suffixed["kind"] == "WINE"
    assert suffixed["suffix"] == "WINDOW-PROBE"

    multi = run_index.parse_run_id("RUN-INP-REP-20260815-170119")
    assert multi["kind"] == "INP-REP"

    assert run_index.parse_run_id("RUN-GDB-notastamp") is None


# --------------------------------------------------------------------------
# Extraction, per receipt shape
# --------------------------------------------------------------------------


def test_extracts_gdb_receipt_shape(sandbox: Path) -> None:
    run_dir = sandbox / "dynamic/wine/RUN-GDB-20260813-101022"
    record = run_index.extract_run(run_dir, root=sandbox)

    assert record["kind"] == "GDB"
    assert record["tool"] == "gdb-harness"
    assert record["tool_version"] == "1.2.0"
    assert record["experiment_id"] == "EXP-20260813-038"
    assert record["target_exe_sha256"] == GDB_METADATA["executable_sha256"]
    assert record["target_exe_sha256_source"] == "metadata.executable_sha256"
    assert record["accepted"] is True
    assert record["completed"] is True
    assert record["stops_observed"] == 400
    assert record["stop_records"] == 3
    assert record["timestamps"]["time_window_end"].startswith("2026-08-13T10:10:24")
    # Watchpoints and breakpoints, normalized and de-duplicated.
    assert record["addresses"] == ["0x0059F7F0", "0x005B18E0", "0x0044C898"]
    assert record["file_offsets"] == ["0x0A6C"]
    assert record["path"] == "dynamic/wine/RUN-GDB-20260813-101022"
    assert record["unreadable"] is None
    assert record["run_id_matches_metadata"] is True

    names = {entry["name"]: entry for entry in record["files"]}
    assert set(names) == {
        "metadata.json", "result.json", "spec.resolved.json",
        "stops.jsonl", "debugger-evidence.txt",
    }
    assert names["debugger-evidence.txt"]["size_bytes"] == len("cleanup verified\n")
    assert all(len(entry["sha256"]) == 64 for entry in record["files"])
    assert record["total_size_bytes"] == sum(e["size_bytes"] for e in record["files"])


def test_extracts_wine_receipt_shape(sandbox: Path) -> None:
    record = run_index.extract_run(
        sandbox / "dynamic/wine/RUN-WINE-20260812-150528", root=sandbox
    )
    # The wine receipt names its experiment under "experiment", not
    # "experiment_id", and records no tool/result at all.
    assert record["experiment_id"] == "EXP-20260812-020"
    assert record["tool"] is None
    assert record["accepted"] is None
    assert record["stops_observed"] is None
    assert record["status"] == "captured then intentionally terminated"
    assert record["timestamps"]["capture_sequence_ended"].startswith("2026-08-12T15:05:32")
    assert record["unreadable"] is None


def test_extracts_object_environment_and_nested_sha(sandbox: Path) -> None:
    record = run_index.extract_run(
        sandbox / "dynamic/wine/RUN-POS-20260815-181852", root=sandbox
    )
    assert record["environment"] == "host Fedora Linux 44; wine 11.0 Staging"
    assert record["target_exe_sha256"] == POS_METADATA["target"]["sha256"]
    assert record["target_exe_sha256_source"] == "metadata.target.sha256"
    assert record["schema_version"] == 1


def test_extracts_top_level_accepted_and_ownership_sha(sandbox: Path) -> None:
    record = run_index.extract_run(
        sandbox / "dynamic/wine/RUN-INP-REP-20260815-170119", root=sandbox
    )
    assert record["kind"] == "INP-REP"
    assert record["accepted"] is False
    assert record["target_exe_sha256_source"] == "metadata.ownership.exe_sha256"


def test_no_hashes_flag_skips_digests(sandbox: Path) -> None:
    record = run_index.extract_run(
        sandbox / "dynamic/wine/RUN-GDB-20260813-101022", root=sandbox, hashes=False
    )
    assert all("sha256" not in entry for entry in record["files"])
    assert record["total_size_bytes"] > 0


# --------------------------------------------------------------------------
# Malformed / absent receipts
# --------------------------------------------------------------------------


def test_malformed_metadata_is_recorded_not_raised(sandbox: Path) -> None:
    run_dir = write_run(sandbox, "RUN-GDB-20260814-000000", {
        "metadata.json": "{ this is not json",
        "result.json": GDB_RESULT,
    })
    record = run_index.extract_run(run_dir, root=sandbox)
    assert record["unreadable"]["file"] == "metadata.json"
    assert "malformed JSON" in record["unreadable"]["reason"]
    # The rest of the record is still extracted from what could be read.
    assert record["kind"] == "GDB"
    assert record["accepted"] is True
    assert record["file_count"] == 2


def test_absent_metadata_is_recorded_not_raised(sandbox: Path) -> None:
    run_dir = write_run(sandbox, "RUN-FRZ-20260814-000001", {"notes.txt": "nothing"})
    record = run_index.extract_run(run_dir, root=sandbox)
    assert record["unreadable"] == {"file": "metadata.json", "reason": "absent"}
    assert record["tool"] is None
    assert record["addresses"] == []


def test_non_object_and_empty_receipts_are_tolerated(sandbox: Path) -> None:
    run_dir = write_run(sandbox, "RUN-CORE-20260814-000002", {
        "metadata.json": ["a", "list", "not", "an", "object"],
        "result.json": "",
        "spec.resolved.json": "3",
    })
    record = run_index.extract_run(run_dir, root=sandbox)
    assert "not an object" in record["unreadable"]["reason"]
    assert record["receipt_errors"]["result.json"] == "empty"
    assert record["addresses"] == []


def test_unrecognized_directory_name_still_indexed(sandbox: Path) -> None:
    run_dir = write_run(sandbox, "RUN-not-a-real-stamp", {"metadata.json": {"run_id": "x"}})
    record = run_index.extract_run(run_dir, root=sandbox)
    assert record["recognized_name"] is False
    assert record["kind"] is None
    assert record["run_id_matches_metadata"] is False


def test_build_survives_a_bad_directory_among_good_ones(sandbox: Path) -> None:
    write_run(sandbox, "RUN-GDB-20260814-000003", {"metadata.json": "{{{"})
    index = run_index.build_index(sandbox, hashes=False)
    assert index["summary"]["run_directories"] == 5
    assert index["summary"]["unreadable_metadata"] == 1
    # Every other run is still fully extracted.
    good = [r for r in index["runs"] if r["run_id"] == "RUN-GDB-20260813-101022"][0]
    assert good["tool"] == "gdb-harness"


def test_missing_run_root_yields_an_empty_index(tmp_path: Path) -> None:
    index = run_index.build_index(tmp_path, hashes=False)
    assert index["summary"]["run_directories"] == 0
    assert index["runs"] == []
    assert index["dangling_citations"] == []


# --------------------------------------------------------------------------
# Citation scanning and the two orphan directions
# --------------------------------------------------------------------------


def test_citations_found_in_plain_text_backticks_and_wikilinks(sandbox: Path) -> None:
    citations = run_index.scan_vault_citations(sandbox / "Vault", root=sandbox)
    assert citations["RUN-GDB-20260813-101022"] == [
        "Vault/30-Experiments/EXP-20260813-038 - gdb.md"
    ]
    assert citations["RUN-WINE-20260812-150528"] == [
        "Vault/30-Experiments/EXP-20260813-038 - gdb.md"
    ]
    # Extracted out of a [[wikilink]] target.
    assert citations["RUN-POS-20260815-181852"] == [
        "Vault/30-Experiments/EXP-20260815-128 - pos.md"
    ]


def test_orphans_reports_both_directions_separately(sandbox: Path) -> None:
    index = run_index.build_index(sandbox, hashes=False)

    # Direction 1: evidence with no home.
    assert index["uncited_run_directories"] == ["RUN-INP-REP-20260815-170119"]
    # Direction 2: a citation with no directory.
    assert index["dangling_citations"] == [{
        "run_id": "RUN-GDB-20991231-235959",
        "cited_by": ["Vault/30-Experiments/EXP-20260815-128 - pos.md"],
    }]
    assert index["summary"]["uncited_run_directories"] == 1
    assert index["summary"]["dangling_citations"] == 1


def test_cited_by_is_attached_to_each_record(sandbox: Path) -> None:
    index = run_index.build_index(sandbox, hashes=False)
    by_id = {record["run_id"]: record for record in index["runs"]}
    assert by_id["RUN-GDB-20260813-101022"]["cited_by"] == [
        "Vault/30-Experiments/EXP-20260813-038 - gdb.md"
    ]
    assert by_id["RUN-INP-REP-20260815-170119"]["cited_by"] == []


def test_clean_vault_reports_no_orphans(tmp_path: Path) -> None:
    write_run(tmp_path, "RUN-GDB-20260813-101022", {"metadata.json": GDB_METADATA})
    write_note(tmp_path, "30-Experiments/note.md", "RUN-GDB-20260813-101022\n")
    index = run_index.build_index(tmp_path, hashes=False)
    assert index["uncited_run_directories"] == []
    assert index["dangling_citations"] == []


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def run_cli(args: list[str], root: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ, ABLPC_ROOT=str(root))
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "run-index.py"), *args],
        capture_output=True, text=True, env=env,
    )


def test_cli_build_writes_json_and_markdown(sandbox: Path) -> None:
    proc = run_cli(
        ["build", "--out", "reports/idx.json", "--markdown", "reports/idx.md", "--no-hashes"],
        sandbox,
    )
    assert proc.returncode == 0, proc.stderr
    summary = json.loads(proc.stdout)
    assert summary["summary"]["run_directories"] == 4
    assert summary["index_bytes"] > 0

    index = json.loads((sandbox / "reports/idx.json").read_text())
    assert index["tool"] == "run-index"
    assert len(index["runs"]) == 4

    table = (sandbox / "reports/idx.md").read_text()
    assert "| run id | kind | tool |" in table
    assert "`RUN-GDB-20260813-101022`" in table
    assert "## Dangling citations" in table
    # A run cited by nothing is visibly marked in the human-readable table.
    assert "(none)" in table


def test_markdown_caps_the_citation_column(tmp_path: Path) -> None:
    write_run(tmp_path, "RUN-GDB-20260813-101022", {"metadata.json": GDB_METADATA})
    for i in range(run_index.MAX_MARKDOWN_CITATIONS + 3):
        write_note(tmp_path, f"30-Experiments/note{i}.md", "RUN-GDB-20260813-101022\n")
    index = run_index.build_index(tmp_path, hashes=False)
    table = run_index.markdown_table(index)
    assert "+3 more" in table
    # The JSON index keeps every citing note.
    assert len(index["runs"][0]["cited_by"]) == run_index.MAX_MARKDOWN_CITATIONS + 3


def test_cli_build_to_stdout(sandbox: Path) -> None:
    proc = run_cli(["build", "--out", "-", "--no-hashes"], sandbox)
    assert proc.returncode == 0, proc.stderr
    index = json.loads(proc.stdout)
    assert index["summary"]["run_directories"] == 4
    assert not (sandbox / "reports").exists()


def test_cli_orphans_is_tool_negative_when_broken(sandbox: Path) -> None:
    proc = run_cli(["orphans"], sandbox)
    assert proc.returncode == 1
    payload = json.loads(proc.stdout)
    assert payload["clean"] is False
    assert payload["uncited_run_directories"]["count"] == 1
    assert payload["dangling_citations"]["count"] == 1
    assert (
        payload["uncited_run_directories"]["runs"][0]["run_id"]
        == "RUN-INP-REP-20260815-170119"
    )


def test_cli_orphans_is_ok_when_clean(tmp_path: Path) -> None:
    write_run(tmp_path, "RUN-GDB-20260813-101022", {"metadata.json": GDB_METADATA})
    write_note(tmp_path, "30-Experiments/note.md", "RUN-GDB-20260813-101022\n")
    proc = run_cli(["orphans"], tmp_path)
    assert proc.returncode == 0
    assert json.loads(proc.stdout)["clean"] is True


def test_cli_show_returns_one_record(sandbox: Path) -> None:
    proc = run_cli(["show", "--run", "RUN-GDB-20260813-101022"], sandbox)
    assert proc.returncode == 0, proc.stderr
    record = json.loads(proc.stdout)
    assert record["run_id"] == "RUN-GDB-20260813-101022"
    assert record["cited_by"] == ["Vault/30-Experiments/EXP-20260813-038 - gdb.md"]


def test_cli_show_refuses_unknown_run(sandbox: Path) -> None:
    proc = run_cli(["show", "--run", "RUN-GDB-19700101-000000"], sandbox)
    assert proc.returncode == 3
    payload = json.loads(proc.stdout)
    assert payload == {
        "refused": True,
        "tool": "run-index",
        "reason": "run_not_found",
        "detail": payload["detail"],
    }


def test_cli_show_refuses_path_traversal(sandbox: Path) -> None:
    proc = run_cli(["show", "--run", "../../etc"], sandbox)
    assert proc.returncode == 3
    assert json.loads(proc.stdout)["reason"] in {"bad_run_id", "run_not_found"}


def test_cli_no_verb_is_usage(sandbox: Path) -> None:
    proc = run_cli([], sandbox)
    assert proc.returncode == 2


def test_cli_capabilities(sandbox: Path) -> None:
    proc = run_cli(["--capabilities"], sandbox)
    assert proc.returncode == 0
    caps = json.loads(proc.stdout)
    assert caps["tool"] == "run-index"
    assert caps["verbs"] == ["build", "orphans", "show"]
    assert caps["modifies_run_directories"] is False
    assert set(caps["exit_codes"]) == {"0", "1", "2", "3"}


def test_script_is_executable() -> None:
    assert os.access(SCRIPTS / "run-index.py", os.X_OK)


@pytest.mark.skipif(
    not (REPO / "dynamic" / "wine").is_dir(),
    reason="real dynamic/wine tree is absent",
)
def test_real_tree_indexes_without_crashing() -> None:
    index = run_index.build_index(REPO, hashes=False)
    assert index["summary"]["run_directories"] > 0
    # Every record is complete regardless of receipt shape.
    for record in index["runs"]:
        assert record["run_id"].startswith("RUN-")
        assert isinstance(record["files"], list)
        assert isinstance(record["cited_by"], list)
