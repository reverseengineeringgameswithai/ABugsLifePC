"""Real bytes stay local; instruction tests skip if the work copies are absent."""
import importlib.util
from pathlib import Path
import struct

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("terrain_retail_probe", ROOT / "scripts/terrain-retail-probe.py")
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


@pytest.fixture(scope="module")
def text():
    if not probe.p.DEFAULT_BINARY.exists():
        pytest.skip("retail executable work copy unavailable")
    return probe.p.load_text(probe.p.DEFAULT_BINARY)


@pytest.fixture(scope="module", params=("level01", "level03"))
def initialized(request, text):
    for key in (request.param, "plantter"):
        if not (probe.SOURCE_ROOT / probe.SOURCES[key][0]).exists():
            pytest.skip("retail terrain work copy unavailable")
    return probe.RetailProbe(request.param, text)


@pytest.fixture(scope="module")
def level01(text):
    for key in ("level01", "plantter"):
        if not (probe.SOURCE_ROOT / probe.SOURCES[key][0]).exists():
            pytest.skip("retail terrain work copy unavailable")
    return probe.RetailProbe("level01", text)


def test_census_keeps_nontriangle_payload_opaque():
    payload = struct.pack("<hhhhhh16hhh", 0, 1, 0, 100, 0, 100,
                          16384, 0, 0, *([0]*13), -1, 123)
    opaque = b"unidentified!!!!"
    offset = 4 + len(payload) + len(opaque)
    records = []
    for size, kind, clone in ((len(payload), 6, 0), (0, 6, 1), (len(opaque), 257, 0)):
        raw = bytearray(76)
        struct.pack_into("<I", raw, 0, size//2)
        struct.pack_into("<i", raw, 16, kind)
        struct.pack_into("<hh", raw, 68, 0, clone)
        records.append(raw)
    raw = struct.pack("<I", offset//2) + payload + opaque + struct.pack("<I", 3) + b"".join(records)
    terrain = probe.TerrainAll.parse(raw)
    result = probe.census(terrain)
    assert result["stored_cells"] == result["vertical_normal_cells"] == 1
    assert result["clone_records"] == 1
    assert result["opaque_high_kinds"] == [{"source_record": 2, "kind": 257,
                                            "payload_offset": 4+len(payload), "payload_size": len(opaque)}]
    assert terrain.data == raw


def test_source_hash_mismatch_rejected_before_emulation(tmp_path):
    path = tmp_path / probe.SOURCES["level01"][0]
    path.parent.mkdir(parents=True)
    path.write_bytes(b"not retail terrain")
    with pytest.raises(probe.p.ProbeError, match="level01 SHA-256 mismatch"):
        probe.load_source("level01", tmp_path)


def test_original_loader_template_mapping_and_reservation(initialized):
    r = initialized.initialization_report()
    count = 191 if initialized.level == "level01" else 602
    terrain_count = count - 13
    assert r["loaded_descriptor_count"] == r["boundary_N"] == count
    assert r["reserved_end_exclusive"] == count+32
    assert r["bucket_members_cover_loaded_records"]
    assert r["unique_bucket_members"] == r["bucket_members"] == count
    assert r["cleared_loaded_indices"] == list(range(terrain_count, count))
    assert sorted(t["descriptor_index"] for t in r["template_map"]) == list(range(terrain_count, count))
    assert sorted(t["source_record"] for t in r["template_map"]) == list(range(13))
    assert all(t["source"] == "plantter" for t in r["template_map"])
    assert all(initialized.initialized_tags[i] == 0 for i in range(terrain_count, 700))


def test_original_descriptor_bytes_agree_with_independent_height_model(initialized):
    from ablpc.terrain_height import TerrainHeightModel
    model = TerrainHeightModel(initialized.sources[0])
    for d in model.descriptors:
        if not d.height_eligible:
            continue
        address = probe.p.DESCRIPTORS + d.index*48
        assert probe.p.get(initialized.cpu, address, "3i") == (d.base_x, d.base_y, d.base_z)
        assert probe.p.get(initialized.cpu, address+20, "i")[0] == d.x_min
        assert probe.p.get(initialized.cpu, address+28, "i")[0] == d.z_min
        assert probe.p.get(initialized.cpu, address+36, "2i") == (d.x_span, d.z_span)
        pointer = probe.p.get(initialized.cpu, address+16, "I")[0]
        assert initialized.locate(pointer)["source_record"] == d.payload_source_index


@pytest.mark.parametrize("axis", (0, 2))
@pytest.mark.parametrize("case", probe.CASES)
def test_real_triangle_is_admitted_and_causes_deflection(level01, axis, case):
    r = level01.movement("triangle", case, axis=axis)
    active = case in ("retail", "without_segments")
    assert r["changed_endpoint"] == active
    assert r["segment_candidate_pairs"] == 0
    assert r["best_triangle_updates"] == ([{"source": "level01", "source_record": 87, "file_offset": 1000}] if active else [])
    if active:
        assert len(r["triangle_candidates"]) == 8
        assert r["position_after"] == ([-8164, -86582, 250188] if axis == 0 else [-9569, -86609, 250551])
        assert r["execution"]["entry_visits"]["0x004aa4d0"] == 2
    else:
        assert r["position_after"] == r["unconstrained_endpoint"]
        assert r["velocity_after"] == r["requested_delta"]
    if case == "without_record87":
        assert len(r["triangle_candidates"]) == 4
        assert all(c["descriptor_index"] != 87 for c in r["triangle_candidates"])


@pytest.mark.parametrize("y", (-200000, 0, 200000))
@pytest.mark.parametrize("case", ("retail", "without_triangles", "without_segments", "moving_away"))
def test_real_xz_segment_response_and_height_controls(level01, y, case):
    r = level01.movement("segment", case, y=y)
    active = case in ("retail", "without_triangles")
    assert r["changed_endpoint"] == active
    assert r["triangle_candidates"] == []
    assert r["best_triangle_updates"] == []
    assert r["best_segment_updates"] == ([0] if active else [])
    assert r["segment_candidate_pairs"] == (0 if case == "without_segments" else 4)
    if r["segment_candidate_pairs"]:
        assert r["segment_source_matches"][0] == [{"source": "level01", "source_record": 179, "file_offset": 219640}]
    assert r["position_after"][1] == y
    if active:
        assert r["position_after"] == [110402, y, -129376]
        assert r["execution"]["entry_visits"]["0x00464ca0"] == 8
    else:
        assert r["position_after"] == r["unconstrained_endpoint"]


def test_cases_restore_all_private_state_and_trace_order(level01):
    first = level01.movement("triangle", "retail")
    level01.movement("segment", "without_triangles", y=200000)
    level01.movement("triangle", "without_record87", axis=2)
    assert level01.movement("triangle", "retail") == first


def test_instruction_bound_cannot_be_reported_as_completed(level01):
    with pytest.raises(probe.p.ProbeError, match="instruction/time bound"):
        level01.run(0x004AB1A0, probe.p.STOP, instruction_limit=1)
    assert level01.movement("triangle", "retail")["changed_endpoint"]


@pytest.mark.parametrize("kwargs", ({"axis": True}, {"y": True}, {"axis": 1}, {"y": 1}))
def test_invalid_fixture_parameters_rejected(level01, kwargs):
    with pytest.raises(probe.p.ProbeError, match="unsupported"):
        level01.movement("triangle", "retail", **kwargs)


def test_work_copy_sources_remain_hash_exact(level01):
    level01.movement("segment", "retail")
    for key in probe.SOURCES:
        probe.load_source(key)
