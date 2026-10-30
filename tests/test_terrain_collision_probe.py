"""Original-instruction checks with synthetic inputs, not game-runtime tests.

Retail bytes stay in the user's read-only work copy; no executable fixture is
distributed. A missing copy skips these instruction checks, never substitutes
a reimplementation. Structural/hash rejection tests still run without it.
"""

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("terrain_collision_probe", ROOT / "scripts/terrain-collision-probe.py")
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


@pytest.fixture(scope="module")
def text():
    if not probe.DEFAULT_BINARY.exists():
        pytest.skip("retail work-copy executable unavailable")
    return probe.load_text(probe.DEFAULT_BINARY)


def test_wrong_executable_is_rejected(tmp_path):
    path = tmp_path / "not-the-retail-binary"
    path.write_bytes(b"synthetic invalid executable")
    with pytest.raises(probe.ProbeError, match="SHA-256 mismatch"):
        probe.load_text(path)


@pytest.mark.parametrize("boundary", [-1, 0, 669, 700, True, 1.0])
def test_invalid_descriptor_boundary_rejected_before_emulation(boundary):
    with pytest.raises(probe.ProbeError, match="boundary outside"):
        probe.descriptor_case(None, boundary, "create")


@pytest.mark.parametrize("boundary", [1, 64, 668])
@pytest.mark.parametrize("case", probe.DESCRIPTOR_CASES)
def test_original_descriptor_slice_has_only_expected_writes(text, boundary, case):
    result = probe.descriptor_case(text, boundary, case)
    # descriptor_case also checks the whole 33,600-byte synthetic table and
    # memory-write events, including no-op writes invisible to a byte diff.
    assert result["visited_slots"] == list(range(20))
    assert result["prefix_below_N_unchanged"]
    assert result["remaining_reserved_slots_unchanged"]
    creates = case in ("create", "contact_other", "contact_zero")
    clears = case in ("flag_clear", "missing_template")
    assert result["written_indices"] == (list(range(boundary, boundary + 20)) if creates or clears else [])
    assert result["descriptor_store_count"] == (180 if creates else 20 if clears else 0)
    assert result["contact_flag_after"] == (0 if case in ("create", "flag_clear", "missing_template", "contact_zero") else 1)


@pytest.mark.parametrize("axis,index", [("x", 0), ("z", 2)])
@pytest.mark.parametrize("special_contact", [False, True])
def test_original_vertical_triangle_changes_lateral_response(text, axis, index, special_contact):
    result = probe.movement_case(text, normal_axis=axis, candidate=True,
                                start=1024, delta=-2048, special_contact=special_contact)
    assert result["return_eax"] == 2
    assert result["unconstrained_endpoint"][index] == -1024
    assert result["position_after"][index] == 88
    assert result["velocity_after"][index] == (16 if special_contact else 2064)
    assert result["residual_after"][index] == (16 if special_contact else 1128)
    for other in set(range(3)) - {index}:
        assert result["position_after"][other] == result["start"][other]
        assert result["velocity_after"][other] == 0
        assert result["residual_after"][other] == 0
    assert result["entered"] == ["0x004aa4d0", "0x004a9860", "0x004a9420", "0x004a95e0"]


@pytest.mark.parametrize("axis", ["x", "z"])
@pytest.mark.parametrize("overrides", [
    {"candidate": False}, {"delta": 2048}, {"tangent": 6400}, {"reverse_winding": True},
])
def test_original_response_negative_controls(text, axis, overrides):
    kwargs = {"normal_axis": axis, "candidate": True, "start": 1024, "delta": -2048}
    result = probe.movement_case(text, **(kwargs | overrides))
    assert result["return_eax"] == 0
    assert result["position_after"] == result["unconstrained_endpoint"]
    assert result["velocity_after"] == result["requested_delta"]
    assert result["residual_after"] == result["requested_delta"]


def test_instruction_measurements_are_repeatable(text):
    kwargs = {"normal_axis": "x", "candidate": True, "start": 1024, "delta": -2048}
    assert probe.movement_case(text, **kwargs) == probe.movement_case(text, **kwargs)
