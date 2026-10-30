"""Tests for ``scripts/ghidra-query.py`` against a synthetic Ghidra export.

Correctness is proven on a small fixture built in ``tmp_path`` so the suite
never depends on the real 7.7 MB export; one optional test touches the real
file and skips when it is absent.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import evidence_lib as ev  # noqa: E402


def _load_ghidra_query():
    spec = importlib.util.spec_from_file_location(
        "ghidra_query", SCRIPTS / "ghidra-query.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gq = _load_ghidra_query()

REAL_EXPORT = (Path(__file__).resolve().parents[1]
               / "static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json")


# --------------------------------------------------------------------------
# Fixture
# --------------------------------------------------------------------------


def _func(address: str, name: str, *, callers: list[str] | None = None,
          callees: list[str] | None = None,
          data_references: list[dict[str, str]] | None = None,
          decompiler: str = "") -> dict[str, Any]:
    return {
        "address": address,
        "name": name,
        "prototype": f"undefined {name}()",
        "callers": callers or [],
        "callees": callees or [],
        "data_references": data_references or [],
        "decompiler": decompiler or f"\nvoid {name}(void)\n\n{{\n  return;\n}}\n\n",
    }


def build_export() -> dict[str, Any]:
    functions = [
        # A thunk whose only structured edge is a call site inside FUN_00403000.
        _func("00401000", "thunk_FUN_00402000", callers=["00403010"],
              decompiler="\nvoid thunk_FUN_00402000(void)\n\n{\n  FUN_00402000();\n}\n"),
        # Structured data reference to 005c5864 plus textual mentions.
        _func("00402000", "FUN_00402000", callees=["00404000"],
              data_references=[{"from": "00402004", "to": "005c5864", "type": "READ"},
                               {"from": "00402008", "to": "005c5868", "type": "WRITE"}],
              decompiler=("\nvoid FUN_00402000(void)\n\n{\n"
                          "  if (*DAT_005c5864 != 0) {\n"
                          "    puVar1 = (uint *)0x5c5864;\n"
                          "    puVar2 = (uint *)0x15c5864;\n"
                          "  }\n  return;\n}\n")),
        _func("00403000", "FUN_00403000", callees=["00401000"],
              decompiler="\nvoid FUN_00403000(void)\n\n{\n  thunk_FUN_00402000();\n}\n"),
        # Self-call: traversal must terminate.
        _func("00404000", "FUN_00404000", callees=["00404000"],
              callers=["00404010"]),
        # Two-cycle A -> B -> A.
        _func("00405000", "FUN_cycle_a", callees=["00406000"], callers=["00406010"]),
        _func("00406000", "FUN_cycle_b", callees=["00405000"], callers=["00405010"]),
        # Duplicate names.
        _func("00407000", "dup_name"),
        _func("00408000", "dup_name"),
        # A six-deep chain c1 -> c2 -> ... -> c6 for the depth cap.
        _func("00410000", "FUN_c1", callees=["00411000"]),
        _func("00411000", "FUN_c2", callees=["00412000"]),
        _func("00412000", "FUN_c3", callees=["00413000"]),
        _func("00413000", "FUN_c4", callees=["00414000"]),
        _func("00414000", "FUN_c5", callees=["00415000"]),
        _func("00415000", "FUN_c6"),
        # Big body for decompiler truncation, and an EXTERNAL callee.
        _func("00420000", "FUN_big", callees=["EXTERNAL:00000074"],
              decompiler="void FUN_big(void)\n" + ("x" * 5000)),
        # Many data references, for the data_references cap.
        _func("00430000", "FUN_many_refs",
              data_references=[{"from": f"0043{i:04x}", "to": "005c5900",
                                "type": "READ"} for i in range(20)]),
    ]
    return {
        "program": {"name": "synth.exe", "executable_sha256": "ab" * 32,
                    "image_base": "00400000"},
        "functions": functions,
        "strings": [
            {"address": "004c0000", "value": "Level01"},
            {"address": "004c0010", "value": "LEVEL02"},
            {"address": "004c0020", "value": "sound.wav"},
            {"address": "004c0030", "value": "x" * 900},
        ],
        "imports": [],
    }


@pytest.fixture()
def export_path(tmp_path: Path) -> Path:
    path = tmp_path / "ghidra-evidence.json"
    path.write_text(json.dumps(build_export()))
    return path


def call(capsys, args: list[str], export: Path | None = None
         ) -> tuple[int, dict[str, Any]]:
    argv = list(args)
    if export is not None:
        argv += ["--export", str(export)]
    argv += ["--compact"]
    code = gq.main(argv)
    out = capsys.readouterr().out.strip()
    return code, json.loads(out)


# --------------------------------------------------------------------------
# Address normalization
# --------------------------------------------------------------------------


@pytest.mark.parametrize("text", ["0x00432930", "00432930", "432930", "0x432930",
                                  "0X432930", "0x00432930  ", "0043 2930".replace(" ", "")])
def test_normalize_address_variants(text: str) -> None:
    assert gq.normalize_address(text) == "00432930"


def test_normalize_address_is_case_insensitive() -> None:
    assert gq.normalize_address("0x005C5864") == "005c5864"
    assert gq.normalize_address("005c5864") == "005c5864"


def test_normalize_address_external_form() -> None:
    assert gq.normalize_address("EXTERNAL:74") == "EXTERNAL:00000074"


@pytest.mark.parametrize("text", ["", "   ", "zzz", "0x", "0xdeadbeefcafe", "12g4"])
def test_normalize_address_rejects_garbage(text: str) -> None:
    with pytest.raises(gq.UsageError):
        gq.normalize_address(text)


def test_address_text_pattern_rejects_longer_number() -> None:
    pattern = gq.address_text_pattern("005c5864")
    assert pattern.search("DAT_005c5864")
    assert pattern.search("0x5c5864")
    assert pattern.search("0x005C5864")
    assert not pattern.search("0x15c5864")
    assert not pattern.search("005c58640")


# --------------------------------------------------------------------------
# function
# --------------------------------------------------------------------------


def test_function_lookup_by_address_variants(capsys, export_path: Path) -> None:
    for form in ("0x00402000", "00402000", "402000", "0x402000"):
        code, payload = call(capsys, ["function", "--addr", form], export_path)
        assert code == ev.EXIT_OK
        assert payload["function"]["address"] == "00402000"
        assert payload["function"]["name"] == "FUN_00402000"
        assert "DAT_005c5864" in payload["function"]["decompiler"]


def test_function_lookup_by_name(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["function", "--name", "FUN_00403000"], export_path)
    assert code == ev.EXIT_OK
    assert payload["function"]["address"] == "00403000"


def test_function_missing_is_tool_negative(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["function", "--addr", "0x00499999"], export_path)
    assert code == ev.EXIT_TOOL_NEGATIVE
    assert payload["found"] is False


def test_function_ambiguous_name_refuses(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["function", "--name", "dup_name"], export_path)
    assert code == ev.EXIT_REFUSAL
    assert payload["refused"] is True
    assert payload["tool"] == "ghidra-query"
    assert payload["reason"] == "ambiguous_name"
    assert "00407000" in payload["detail"] and "00408000" in payload["detail"]


def test_function_no_decompiler_omits_body(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["function", "--addr", "0x00420000",
                                  "--no-decompiler"], export_path)
    assert code == ev.EXIT_OK
    assert "decompiler" not in payload["function"]
    assert payload["function"]["decompiler_omitted"] is True
    assert payload["function"]["decompiler_bytes"] > 5000


def test_function_decompiler_truncation_is_flagged(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["function", "--addr", "0x00420000",
                                  "--max-decompiler-bytes", "100"], export_path)
    assert code == ev.EXIT_OK
    func = payload["function"]
    assert func["decompiler_truncated"] is True
    assert len(func["decompiler"].encode("utf-8")) <= 100
    assert func["decompiler_bytes"] > 100

    code, payload = call(capsys, ["function", "--addr", "0x00420000"], export_path)
    assert payload["function"]["decompiler_truncated"] is False


def test_function_data_reference_cap_is_flagged(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["function", "--addr", "0x00430000",
                                  "--max-data-references", "3",
                                  "--no-decompiler"], export_path)
    assert code == ev.EXIT_OK
    func = payload["function"]
    assert len(func["data_references"]) == 3
    assert func["data_reference_count"] == 20
    assert func["data_references_truncated"] is True


def test_function_reports_thunk_target_as_inference(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["function", "--addr", "0x00401000",
                                  "--no-decompiler"], export_path)
    assert code == ev.EXIT_OK
    assert payload["function"]["thunk_target"] == "00402000"
    assert payload["function"]["thunk_target_evidence"] == "thunk_name_bridge"


# --------------------------------------------------------------------------
# callers / callees
# --------------------------------------------------------------------------


def test_callees_are_structured_edges(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["callees", "--addr", "0x00403000"], export_path)
    assert code == ev.EXIT_OK
    by_addr = {n["address"]: n for n in payload["nodes"]}
    assert by_addr["00401000"]["evidence"][0]["kind"] == "callee_edge"
    assert by_addr["00401000"]["evidence"][0]["exact"] is True
    # The thunk bridge reaches the real target and is labelled as inference.
    assert by_addr["00402000"]["evidence"][0]["kind"] == "thunk_name_bridge"
    assert by_addr["00402000"]["evidence"][0]["exact"] is False


def test_no_follow_thunks_drops_the_bridge(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["callees", "--addr", "0x00403000",
                                  "--no-follow-thunks"], export_path)
    assert code == ev.EXIT_OK
    assert [n["address"] for n in payload["nodes"]] == ["00401000"]


def test_callers_resolve_callsites_and_flag_inference(capsys, export_path: Path) -> None:
    # 00403010 is a call site inside FUN_00403000, not a function entry.
    code, payload = call(capsys, ["callers", "--addr", "0x00401000"], export_path)
    assert code == ev.EXIT_OK
    by_addr = {n["address"]: n for n in payload["nodes"]}
    kinds = {e["kind"] for e in by_addr["00403000"]["evidence"]}
    assert "callee_edge" in kinds
    assert "callsite_owner" in kinds
    site = [e for e in by_addr["00403000"]["evidence"]
            if e["kind"] == "callsite_owner"][0]
    assert site["exact"] is False
    assert site["callsites"] == ["00403010"]
    assert site["corroborated"] is True


def test_callers_bridge_thunks_to_the_real_function(capsys, export_path: Path) -> None:
    # FUN_00402000 has no recorded callers; only the thunk naming bridges it.
    code, payload = call(capsys, ["callers", "--addr", "0x00402000"], export_path)
    assert code == ev.EXIT_OK
    node = {n["address"]: n for n in payload["nodes"]}["00403000"]
    assert all(e["kind"] == "thunk_name_bridge" for e in node["evidence"])
    assert node["evidence"][0]["via_thunk"] == "00401000"


def test_callees_of_leaf_is_tool_negative(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["callees", "--addr", "0x00415000"], export_path)
    assert code == ev.EXIT_TOOL_NEGATIVE
    assert payload["nodes"] == []


def test_self_call_terminates(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["callees", "--addr", "0x00404000",
                                  "--depth", "4"], export_path)
    assert code == ev.EXIT_TOOL_NEGATIVE
    assert payload["nodes"] == []


def test_two_cycle_terminates(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["callees", "--addr", "0x00405000",
                                  "--depth", "4"], export_path)
    assert code == ev.EXIT_OK
    assert [n["address"] for n in payload["nodes"]] == ["00406000"]
    assert payload["truncated_at_depth"] is False

    code, payload = call(capsys, ["callers", "--addr", "0x00405000",
                                  "--depth", "4"], export_path)
    assert code == ev.EXIT_OK
    assert [n["address"] for n in payload["nodes"]] == ["00406000"]


def test_depth_cap_marks_truncation(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["callees", "--addr", "0x00410000",
                                  "--depth", "9"], export_path)
    assert code == ev.EXIT_OK
    assert payload["requested_depth"] == 9
    assert payload["depth"] == gq.MAX_DEPTH == 4
    assert payload["depth_capped"] is True
    assert payload["truncated_at_depth"] is True
    assert [n["depth"] for n in payload["nodes"]] == [1, 2, 3, 4]
    assert [n["address"] for n in payload["nodes"]] == [
        "00411000", "00412000", "00413000", "00414000"]


def test_depth_below_cap_completes_without_truncation(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["callees", "--addr", "0x00413000",
                                  "--depth", "4"], export_path)
    assert code == ev.EXIT_OK
    assert payload["truncated_at_depth"] is False
    assert len(payload["nodes"]) == 2


def test_external_callee_is_reported(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["callees", "--addr", "0x00420000"], export_path)
    assert code == ev.EXIT_OK
    assert payload["nodes"][0]["address"] == "EXTERNAL:00000074"
    assert payload["nodes"][0]["name"] is None
    assert any("EXTERNAL" in c for c in payload["caveats"])


# --------------------------------------------------------------------------
# xrefs
# --------------------------------------------------------------------------


def test_xrefs_separates_structured_and_textual_evidence(capsys,
                                                         export_path: Path) -> None:
    code, payload = call(capsys, ["xrefs", "--to", "0x005C5864"], export_path)
    assert code == ev.EXIT_OK
    structured = payload["data_references"]["functions"]
    assert [f["address"] for f in structured] == ["00402000"]
    assert structured[0]["references"][0]["to"] == "005c5864"
    textual = payload["decompiler_text"]["functions"]
    assert [f["address"] for f in textual] == ["00402000"]
    # DAT_005c5864 and 0x5c5864 match; the decoy 0x15c5864 does not.
    assert textual[0]["match_count"] == 2
    assert payload["evidence_kinds"] == ["data_references", "decompiler_text"]


def test_xrefs_text_only_target_has_no_structured_evidence(capsys,
                                                           export_path: Path) -> None:
    code, payload = call(capsys, ["xrefs", "--to", "0x005c5868"], export_path)
    assert code == ev.EXIT_OK
    assert payload["data_references"]["function_count"] == 1
    assert payload["decompiler_text"]["function_count"] == 0


def test_xrefs_unknown_target_is_tool_negative(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["xrefs", "--to", "0x00999999"], export_path)
    assert code == ev.EXIT_TOOL_NEGATIVE
    assert payload["data_references"]["function_count"] == 0
    assert payload["decompiler_text"]["function_count"] == 0


def test_xrefs_hit_cap_is_flagged(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["xrefs", "--to", "0x005c5900",
                                  "--max-hits-per-function", "2"], export_path)
    assert code == ev.EXIT_OK
    entry = payload["data_references"]["functions"][0]
    assert len(entry["references"]) == 2
    assert entry["references_truncated"] is True


# --------------------------------------------------------------------------
# grep / strings
# --------------------------------------------------------------------------


def test_grep_decompiler_bounds_context(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["grep", "--pattern", "DAT_005c5864"], export_path)
    assert code == ev.EXIT_OK
    assert payload["hit_count"] == 1
    hit = payload["hits"][0]
    assert hit["address"] == "00402000"
    assert hit["matches"][0]["field"] == "decompiler"
    assert hit["matches"][0]["line"] == 5
    assert len(hit["matches"][0]["context"]) <= gq.DEFAULT_CONTEXT_CHARS + 8


def test_grep_hit_cap_sets_hits_truncated(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["grep", "--pattern", "void", "--max-hits", "2"],
                         export_path)
    assert code == ev.EXIT_OK
    assert payload["hit_count"] == 2
    assert payload["hits_truncated"] is True

    code, payload = call(capsys, ["grep", "--pattern", "void"], export_path)
    assert payload["hits_truncated"] is False


def test_grep_per_function_cap(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["grep", "--pattern", "x", "--in", "decompiler",
                                  "--max-hits-per-function", "3"], export_path)
    assert code == ev.EXIT_OK
    big = [h for h in payload["hits"] if h["address"] == "00420000"][0]
    assert len(big["matches"]) == 3
    assert big["match_count"] > 3
    assert big["matches_truncated"] is True


def test_grep_in_name_and_prototype(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["grep", "--pattern", "cycle", "--in", "name"],
                         export_path)
    assert code == ev.EXIT_OK
    assert {h["address"] for h in payload["hits"]} == {"00405000", "00406000"}

    code, payload = call(capsys, ["grep", "--pattern", "undefined FUN_c1",
                                  "--in", "prototype"], export_path)
    assert code == ev.EXIT_OK
    assert payload["hits"][0]["address"] == "00410000"


def test_grep_no_match_is_tool_negative(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["grep", "--pattern", "no_such_token_anywhere"],
                         export_path)
    assert code == ev.EXIT_TOOL_NEGATIVE
    assert payload["hit_count"] == 0


def test_strings_search(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["strings", "--pattern", "Level", "--ignore-case"],
                         export_path)
    assert code == ev.EXIT_OK
    assert [h["address"] for h in payload["hits"]] == ["004c0000", "004c0010"]

    code, payload = call(capsys, ["strings", "--pattern", "Level"], export_path)
    assert [h["address"] for h in payload["hits"]] == ["004c0000"]


def test_strings_value_is_bounded(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["strings", "--pattern", "^x+$"], export_path)
    assert code == ev.EXIT_OK
    hit = payload["hits"][0]
    assert len(hit["value"]) == gq.MAX_STRING_VALUE_CHARS
    assert hit["value_truncated"] is True


def test_strings_no_match_is_tool_negative(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["strings", "--pattern", "zzz-not-present"],
                         export_path)
    assert code == ev.EXIT_TOOL_NEGATIVE


# --------------------------------------------------------------------------
# index
# --------------------------------------------------------------------------


def test_index_build_is_small_and_complete(capsys, tmp_path: Path,
                                           export_path: Path) -> None:
    out = tmp_path / "idx.json"
    code, payload = call(capsys, ["index", "--out", str(out)], export_path)
    assert code == ev.EXIT_OK
    assert payload["index_bytes"] == len(out.read_bytes())
    index = json.loads(out.read_text())
    assert index["counts"]["functions"] == 16
    assert index["counts"]["thunks"] == 1
    assert set(index["functions"]) == {f["address"] for f in build_export()["functions"]}
    entry = index["functions"]["00402000"]
    assert entry["name"] == "FUN_00402000"
    assert entry["decompiler_bytes"] > 0
    assert entry["first_line"] == "void FUN_00402000(void)"
    assert "decompiler" not in entry
    assert index["names"]["FUN_00402000"] == "00402000"
    assert "dup_name" not in index["names"]
    assert index["ambiguous_names"]["dup_name"] == ["00407000", "00408000"]
    # Reverse call map: who lists 00401000 as a callee.
    assert index["reverse_calls"]["00401000"] == ["00403000"]
    assert index["source"]["sha256"] == ev.sha256_file(export_path)


def test_index_is_greppable_one_record_per_line(tmp_path: Path,
                                                export_path: Path) -> None:
    out = tmp_path / "idx.json"
    assert gq.main(["index", "--export", str(export_path), "--out", str(out),
                    "--compact-index"]) == ev.EXIT_OK
    text = out.read_text()
    assert len(text.splitlines()) == 1  # --compact-index is a single line
    assert json.loads(text)

    assert gq.main(["index", "--export", str(export_path), "--out", str(out)]) \
        == ev.EXIT_OK
    text = out.read_text()
    assert json.loads(text)  # still valid JSON
    matched = [ln for ln in text.splitlines() if ln.startswith('"00402000":')]
    assert len(matched) == 1
    assert "FUN_00402000" in matched[0]


def test_index_check_detects_staleness(capsys, tmp_path: Path,
                                       export_path: Path) -> None:
    out = tmp_path / "idx.json"
    assert gq.main(["index", "--export", str(export_path), "--out", str(out),
                    "--compact"]) == ev.EXIT_OK
    capsys.readouterr()

    code, payload = call(capsys, ["index", "--check", "--out", str(out)], export_path)
    assert code == ev.EXIT_OK
    assert payload["stale"] is False

    data = build_export()
    data["functions"][0]["name"] = "renamed_thunk"
    export_path.write_text(json.dumps(data))

    code, payload = call(capsys, ["index", "--check", "--out", str(out)], export_path)
    assert code == ev.EXIT_TOOL_NEGATIVE
    assert payload["stale"] is True
    assert "sha256 differs" in payload["reasons"]


def test_index_check_without_index_is_tool_negative(capsys, tmp_path: Path,
                                                    export_path: Path) -> None:
    code, payload = call(capsys, ["index", "--check", "--out",
                                  str(tmp_path / "absent.json")], export_path)
    assert code == ev.EXIT_TOOL_NEGATIVE
    assert payload["present"] is False
    assert payload["stale"] is True


def test_index_check_refuses_malformed_index(capsys, tmp_path: Path,
                                             export_path: Path) -> None:
    out = tmp_path / "idx.json"
    out.write_text("{not json")
    code, payload = call(capsys, ["index", "--check", "--out", str(out)], export_path)
    assert code == ev.EXIT_REFUSAL
    assert payload["reason"] == "index_malformed"


def test_index_default_path_is_a_sidecar(export_path: Path) -> None:
    assert gq.index_path_for(export_path).name == "ghidra-evidence.index.json"


# --------------------------------------------------------------------------
# stats / capabilities / plumbing
# --------------------------------------------------------------------------


def test_stats_warns_about_empty_imports(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["stats", "--top", "3"], export_path)
    assert code == ev.EXIT_OK
    assert payload["counts"]["imports"] == 0
    assert payload["counts"]["functions"] == 16
    assert payload["counts"]["strings"] == 4
    assert any("imports table is empty" in w for w in payload["warnings"])
    assert any("not unique" in w for w in payload["warnings"])
    largest = payload["largest_functions"]
    assert len(largest) == 3
    assert largest[0]["address"] == "00420000"
    assert largest[0]["decompiler_bytes"] >= largest[1]["decompiler_bytes"]


def test_capabilities_describes_the_source(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["--capabilities"], export_path)
    assert code == ev.EXIT_OK
    assert payload["tool"] == "ghidra-query"
    assert payload["mode"] == "read-only"
    assert "xrefs" in payload["verbs"]
    assert payload["limits"]["max_depth"] == gq.MAX_DEPTH
    assert payload["source"]["exists"] is True
    assert payload["source"]["sha256"] == ev.sha256_file(export_path)
    assert payload["exit_codes"]["refusal"] == ev.EXIT_REFUSAL


def test_capabilities_without_the_export_present(capsys, tmp_path: Path) -> None:
    code, payload = call(capsys, ["--capabilities"], tmp_path / "absent.json")
    assert code == ev.EXIT_OK
    assert payload["source"]["exists"] is False


def test_missing_export_refuses(capsys, tmp_path: Path) -> None:
    code, payload = call(capsys, ["stats"], tmp_path / "absent.json")
    assert code == ev.EXIT_REFUSAL
    assert payload["reason"] == "export_missing"


def test_malformed_export_refuses(capsys, tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text('{"program": {}, "functions": "nope"}')
    code, payload = call(capsys, ["stats"], bad)
    assert code == ev.EXIT_REFUSAL
    assert payload["reason"] == "export_malformed"


def test_export_with_missing_function_key_refuses(capsys, tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"program": {}, "functions": [{"address": "00401000"}],
                               "strings": [], "imports": []}))
    code, payload = call(capsys, ["stats"], bad)
    assert code == ev.EXIT_REFUSAL
    assert payload["reason"] == "export_malformed"
    assert "missing" in payload["detail"]


def test_ablpc_root_override_locates_the_default_export(monkeypatch, tmp_path: Path,
                                                        capsys) -> None:
    target = tmp_path / gq.DEFAULT_EXPORT
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps(build_export()))
    monkeypatch.setenv("ABLPC_ROOT", str(tmp_path))
    assert gq.default_export_path() == target
    code = gq.main(["stats", "--compact"])
    payload = json.loads(capsys.readouterr().out)
    assert code == ev.EXIT_OK
    assert payload["program"]["name"] == "synth.exe"


# --------------------------------------------------------------------------
# Usage errors
# --------------------------------------------------------------------------


def test_usage_error_when_addr_and_name_both_given(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["function", "--addr", "0x00402000",
                                  "--name", "FUN_00402000"], export_path)
    assert code == ev.EXIT_USAGE
    assert payload["error"] == "usage"


def test_usage_error_when_neither_addr_nor_name(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["function"], export_path)
    assert code == ev.EXIT_USAGE


def test_usage_error_for_bad_address(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["function", "--addr", "not-hex"], export_path)
    assert code == ev.EXIT_USAGE
    assert "not a hex address" in payload["detail"]


def test_usage_error_for_bad_regex(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["grep", "--pattern", "([unclosed"], export_path)
    assert code == ev.EXIT_USAGE
    assert "invalid regex" in payload["detail"]


def test_usage_error_for_zero_depth(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["callers", "--addr", "0x00401000", "--depth", "0"],
                         export_path)
    assert code == ev.EXIT_USAGE


def test_usage_error_for_negative_decompiler_budget(capsys, export_path: Path) -> None:
    code, payload = call(capsys, ["function", "--addr", "0x00402000",
                                  "--max-decompiler-bytes", "-1"], export_path)
    assert code == ev.EXIT_USAGE


def test_usage_error_without_a_subcommand(capsys) -> None:
    code = gq.main([])
    payload = json.loads(capsys.readouterr().out)
    assert code == ev.EXIT_USAGE
    assert payload["error"] == "usage"


def test_argparse_rejects_unknown_grep_field(export_path: Path) -> None:
    with pytest.raises(SystemExit) as excinfo:
        gq.main(["grep", "--pattern", "x", "--in", "bogus",
                 "--export", str(export_path)])
    assert excinfo.value.code == ev.EXIT_USAGE


# --------------------------------------------------------------------------
# Optional: the real export
# --------------------------------------------------------------------------


@pytest.mark.skipif(not REAL_EXPORT.exists(), reason="real export not present")
def test_real_export_known_function(capsys) -> None:
    code, payload = call(capsys, ["function", "--addr", "0x00432930",
                                  "--no-decompiler"], REAL_EXPORT)
    assert code == ev.EXIT_OK
    assert payload["function"]["name"] == "FUN_00432930"
    assert payload["function"]["callees"] == ["00401659"]
