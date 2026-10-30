from __future__ import annotations

from dataclasses import asdict, replace
import json
from pathlib import Path
import subprocess

import pytest

from reimplementation.ablpc.grain_gate_resolver import (
    BUGS_EXE_SHA256,
    CITY_ANIMATION_ADDRESS,
    CITY_INDEX0_BYTE_ADDRESS,
    CITY_INDEX0_BYTE_WRITE,
    CITY_OPEN_STATE,
    CITY_OPEN_WRITE,
    CITY_STATE_ADDRESS,
    TUNNELS_OPEN_TYPE,
    TUNNELS_ROW0_COUPLING_WRITE,
    TUNNELS_ROW4_COUPLING_WRITE,
    TUNNELS_TABLE_ADDRESS,
    CityGate,
    CityRequest,
    GrainGateResolverError,
    NonOpeningReason,
    TunnelsRecord,
    TunnelsRequest,
    city_retail_requirement,
    inside_proximity,
    proximity_distance_sq,
    proximity_radius_sq,
    resolve_city,
    resolve_tunnels,
)


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "grain-gate-resolver.py"
PYTHON = ROOT / ".venv" / "bin" / "python"

RETAIL_TUNNELS_ROWS = (
    # (type, unknown +0x04, retail requirement, X, Z), EXP-136/139.
    (0x10C7, 26, 20, 193754, 131692),
    (0x10C7, 23, 10, 505642, -451306),
    (0x10C7, 24, 10, 832302, 291075),
    (0x10C7, 22, 10, 509676, 510143),
    (0x10C7, 25, 20, 833246, 612273),
    (0x10C7, 21, 20, 1142934, 1308289),
    (0x10C7, 28, 30, 1471643, 1410369),
    (0x10C7, 20, 10, 1202034, 1986285),
    (0x10C7, 27, 30, 1634925, 2534812),
)

TUNNELS_STANDOFFS = {
    # Accepted walkable points from EXP-144/145. Y is unused by the engine.
    0: (205067, 143005),
    1: (489642, -451306),
    2: (843615, 302388),
    3: (501696, 494016),
    4: (840401, 626583),
    5: (1126934, 1308289),
    6: (1471643, 1426369),
    7: (1202034, 1970285),
    8: (1646238, 2546125),
}

CITY_GATES = (
    # index, state, modified requirement, X, Z, r, da, db, sa, sb
    (0, -1, 1, -71129, -184314, 80, -32, 32, 2, 3),
    (1, -1, 2, 354031, 35256, 90, 44, -34, 4, 5),
    (2, -1, 3, 582271, 310212, 100, -28, 32, 0, 1),
)

CITY_INSIDE_POINTS = (
    (-87622, -182181),  # EXP-137/138.
    (343031, 22256),  # EXP-148/149.
    (601271, 309212),  # EXP-148/149.
)


def _tunnels_records(*, modified: bool = True) -> tuple[TunnelsRecord, ...]:
    return tuple(
        TunnelsRecord(
            type_value=type_value,
            unknown_04=unknown_04,
            requirement=(index + 1 if modified else requirement),
            center_x=x,
            center_z=z,
        )
        for index, (type_value, unknown_04, requirement, x, z) in enumerate(
            RETAIL_TUNNELS_ROWS
        )
    )


def _tunnels_request(
    row: int,
    grain: int,
    *,
    records: tuple[TunnelsRecord, ...] | None = None,
) -> TunnelsRequest:
    x, z = TUNNELS_STANDOFFS[row]
    return TunnelsRequest(
        internal_level=3,
        flik_x=x,
        flik_z=z,
        grain_count=grain,
        records=_tunnels_records() if records is None else records,
    )


def _city_gate(index: int, *, state: int = -1) -> CityGate:
    values = list(CITY_GATES[index])
    values[1] = state
    return CityGate(*values)


def _city_request(index: int, grain: int, *, state: int = -1) -> CityRequest:
    x, z = CITY_INSIDE_POINTS[index]
    return CityRequest(
        internal_level=4,
        flik_x=x,
        flik_z=z,
        grain_count=grain,
        gate=_city_gate(index, state=state),
    )


def test_exact_binary_and_native_geometry_anchors_are_pinned() -> None:
    assert BUGS_EXE_SHA256 == (
        "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
    )
    assert TUNNELS_TABLE_ADDRESS == 0x004DA9C8
    assert CITY_STATE_ADDRESS == 0x0059F020
    assert CITY_ANIMATION_ADDRESS == 0x0059F030
    assert CITY_INDEX0_BYTE_ADDRESS == 0x00599C69


def test_proximity_reproduces_accepted_exp139_cross_checks() -> None:
    assert proximity_distance_sq(501696, 494016, 509676, 510143) == 4993
    assert proximity_distance_sq(-87622, -182181, -71129, -184314) == 4289
    assert proximity_distance_sq(-92603, -181281, -71129, -184314) == 7177
    assert proximity_radius_sq(80) == 6400


def test_proximity_is_strict_at_exact_radius() -> None:
    assert proximity_distance_sq(100 << 8, 0, 0, 0) == 10000
    assert inside_proximity((100 << 8) - 1, 0, 0, 0, 100) is True
    assert inside_proximity(100 << 8, 0, 0, 0, 100) is False


def test_proximity_wraps_subtract_products_and_add_as_signed_int32() -> None:
    # INT32_MIN - INT32_MAX wraps to +1 before sar 8.
    assert proximity_distance_sq(-0x80000000, 0, 0x7FFFFFFF, 0) == 0
    # 32768^2 + 32768^2 wraps to INT32_MIN, so signed comparison says inside.
    delta = 32768 << 8
    assert proximity_distance_sq(delta, delta, 0, 0) == -0x80000000
    assert inside_proximity(delta, delta, 0, 0, 0) is True


@pytest.mark.parametrize("row", [0, 2, 3, 5, 6, 7, 8])
def test_tunnels_exact_min_minus_one_and_min_receipts(row: int) -> None:
    minimum = row + 1
    closed = resolve_tunnels(_tunnels_request(row, minimum - 1))
    assert closed.decisions[row].reason == NonOpeningReason.INSUFFICIENT_GRAIN
    assert closed.decisions[row].distance_sq is None

    opened = resolve_tunnels(_tunnels_request(row, minimum))
    assert opened.decisions[row].opens is True
    assert row in opened.opened_rows
    assert opened.decisions[row].distance_sq is not None
    assert opened.decisions[row].distance_sq < 10000


def test_tunnels_row1_matches_accepted_opens_above_minimum_only() -> None:
    result = resolve_tunnels(_tunnels_request(1, 9))
    assert result.opened_rows == (1,)
    assert result.decisions[1].opens is True
    # EXP-148/149 did not retain the exact grain-1/grain-2 runtime pair.
    assert result.decisions[1].distance_sq == 3969


def test_tunnels_row0_couples_row4_before_its_later_visit() -> None:
    original = _tunnels_records()
    result = resolve_tunnels(_tunnels_request(0, 1, records=original))

    assert result.opened_rows == (0,)
    assert [(write.target, write.instruction_address) for write in result.direct_writes] == [
        ("tunnels_record[0].type", 0x00432F6A),
        ("tunnels_record[4].type", TUNNELS_ROW0_COUPLING_WRITE),
    ]
    assert result.decisions[4].reason == NonOpeningReason.ALREADY_NON_CLOSED
    assert result.decisions[4].state_at_visit == TUNNELS_OPEN_TYPE
    assert result.records_after_direct_writes[0].type_value == TUNNELS_OPEN_TYPE
    assert result.records_after_direct_writes[4].type_value == TUNNELS_OPEN_TYPE
    assert result.newly_coupled_rows_entering_decay_later_this_pass == (4,)
    assert result.records_after_direct_writes[4].unknown_04 == original[4].unknown_04


def test_tunnels_row4_couples_row0_after_row0_was_already_visited() -> None:
    result = resolve_tunnels(_tunnels_request(4, 5))
    assert result.decisions[0].reason == NonOpeningReason.OUTSIDE_PROXIMITY
    assert result.opened_rows == (4,)
    assert [(write.target, write.instruction_address) for write in result.direct_writes] == [
        ("tunnels_record[4].type", 0x00432F6A),
        ("tunnels_record[0].type", TUNNELS_ROW4_COUPLING_WRITE),
    ]
    assert result.records_after_direct_writes[0].type_value == TUNNELS_OPEN_TYPE
    assert result.newly_coupled_rows_entering_decay_later_this_pass == ()


def test_tunnels_preserves_order_when_multiple_synthetic_rows_open() -> None:
    records = list(_tunnels_records())
    records[0] = replace(records[0], type_value=0)
    for row in (1, 2):
        records[row] = replace(
            records[row], requirement=0, center_x=1234, center_z=-5678
        )
    result = resolve_tunnels(
        TunnelsRequest(
            internal_level=3,
            flik_x=1234,
            flik_z=-5678,
            grain_count=0,
            records=tuple(records),
        )
    )
    assert result.opened_rows == (1, 2)
    assert [write.target for write in result.direct_writes] == [
        "tunnels_record[1].type",
        "tunnels_record[2].type",
    ]


def test_tunnels_refusal_order_and_decay_rule_are_explicit() -> None:
    records = list(_tunnels_records())
    records[0] = replace(records[0], type_value=0x1068)
    already = resolve_tunnels(_tunnels_request(0, 0, records=tuple(records)))
    assert already.decisions[0] == already.decisions[0].__class__(
        gate_index=0,
        opens=False,
        reason=NonOpeningReason.ALREADY_NON_CLOSED,
        state_at_visit=0x1068,
        distance_sq=None,
        radius_sq=None,
    )
    insufficient = resolve_tunnels(_tunnels_request(8, 0))
    assert insufficient.decisions[8].reason == NonOpeningReason.INSUFFICIENT_GRAIN
    assert insufficient.decisions[8].distance_sq is None
    outside = resolve_tunnels(_tunnels_request(8, 50))
    assert outside.decisions[0].reason == NonOpeningReason.OUTSIDE_PROXIMITY
    assert outside.downstream_rule.signed_type_greater_than == 0x708
    assert outside.downstream_rule.wrapping_delta == -140
    assert outside.downstream_rule.follows_non_closed_opening_refusal is True


@pytest.mark.parametrize("index", [0, 1, 2])
def test_city_exact_min_minus_one_and_min_receipts(index: int) -> None:
    minimum = index + 1
    closed = resolve_city(_city_request(index, minimum - 1))
    assert closed.decision.reason == NonOpeningReason.INSUFFICIENT_GRAIN
    assert closed.decision.distance_sq is not None

    opened = resolve_city(_city_request(index, minimum))
    assert opened.decision.opens is True
    assert opened.direct_writes[0].value == CITY_OPEN_STATE
    assert opened.direct_writes[0].instruction_address == CITY_OPEN_WRITE


def test_city_gate0_includes_only_address_named_byte_write() -> None:
    result = resolve_city(_city_request(0, 1))
    assert [asdict(write) for write in result.direct_writes] == [
        {
            "address": CITY_STATE_ADDRESS,
            "width_bits": 32,
            "value": 0x20,
            "instruction_address": CITY_OPEN_WRITE,
            "target": "city_state[0]",
        },
        {
            "address": CITY_INDEX0_BYTE_ADDRESS,
            "width_bits": 8,
            "value": 1,
            "instruction_address": CITY_INDEX0_BYTE_WRITE,
            "target": "address_0x00599C69",
        },
    ]
    rule = result.downstream_rule
    assert (rule.slot_a, rule.slot_b) == (2, 3)
    assert (rule.aggregate_delta_a_from_zero, rule.aggregate_delta_b_from_zero) == (
        -1024,
        1024,
    )
    assert rule.steps_from_opening_state_to_zero == 32
    assert rule.first_step_occurs_in_opening_call is True


@pytest.mark.parametrize(
    ("index", "slots", "per_step", "terminal"),
    [
        (1, (4, 5), (44, -34), (1408, -1088)),
        (2, (0, 1), (-28, 32), (-896, 1024)),
    ],
)
def test_city_gate1_gate2_slot_delta_receipts(
    index: int,
    slots: tuple[int, int],
    per_step: tuple[int, int],
    terminal: tuple[int, int],
) -> None:
    result = resolve_city(_city_request(index, index + 1))
    assert len(result.direct_writes) == 1
    rule = result.downstream_rule
    assert (rule.slot_a, rule.slot_b) == slots
    assert (rule.wrapping_delta_a, rule.wrapping_delta_b) == per_step
    assert (rule.aggregate_delta_a_from_zero, rule.aggregate_delta_b_from_zero) == terminal


def test_city_refusal_order_matches_native_state_proximity_then_grain() -> None:
    already = resolve_city(_city_request(0, 0, state=0x20))
    assert already.decision.reason == NonOpeningReason.ALREADY_NON_CLOSED
    assert already.decision.distance_sq is None

    # EXP-137's approach point is outside; City checks that before grain.
    outside = resolve_city(
        CityRequest(
            internal_level=4,
            flik_x=-92603,
            flik_z=-181281,
            grain_count=0,
            gate=_city_gate(0),
        )
    )
    assert outside.decision.reason == NonOpeningReason.OUTSIDE_PROXIMITY
    assert outside.decision.distance_sq == 7177
    assert outside.direct_writes == ()

    insufficient = resolve_city(_city_request(0, 0))
    assert insufficient.decision.reason == NonOpeningReason.INSUFFICIENT_GRAIN
    assert insufficient.decision.distance_sq == 4289


def test_city_retail_formula_is_bounded_to_three_indices() -> None:
    assert tuple(city_retail_requirement(index) for index in range(3)) == (10, 20, 30)
    with pytest.raises(GrainGateResolverError, match="outside 0..2"):
        city_retail_requirement(3)


@pytest.mark.parametrize(
    ("factory", "message"),
    [
        (
            lambda: TunnelsRequest(2, 0, 0, 0, _tunnels_records()),
            "internal level 3",
        ),
        (
            lambda: TunnelsRequest(3, 0, 0, 256, _tunnels_records()),
            "unsigned byte",
        ),
        (
            lambda: TunnelsRequest(3, 0, 0, 0, _tunnels_records()[:-1]),
            "exactly nine",
        ),
        (
            lambda: replace(_tunnels_records()[0], requirement=51),
            "authored 0..50",
        ),
        (
            lambda: CityRequest(3, 0, 0, 0, _city_gate(0)),
            "internal level 4",
        ),
        (
            lambda: replace(_city_gate(0), slot_a=6),
            "outside 0..5",
        ),
        (
            lambda: replace(_city_gate(0), state=0x80000000),
            "signed int32",
        ),
    ],
)
def test_invalid_inputs_fail_closed(factory, message: str) -> None:
    with pytest.raises(GrainGateResolverError, match=message):
        factory()


def _city_json_payload() -> dict[str, object]:
    gate = _city_gate(0)
    return {
        "family": "city_entrance",
        "internal_level": 4,
        "flik_x": CITY_INSIDE_POINTS[0][0],
        "flik_z": CITY_INSIDE_POINTS[0][1],
        "grain_count": 1,
        "gate": asdict(gate),
    }


def test_reporting_surface_is_asset_free_deterministic_and_honest() -> None:
    payload = json.dumps(_city_json_payload())
    command = [str(PYTHON), str(SCRIPT), "-"]
    first = subprocess.run(command, input=payload, text=True, capture_output=True, timeout=10)
    second = subprocess.run(command, input=payload, text=True, capture_output=True, timeout=10)
    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    report = json.loads(first.stdout)
    assert report["contract"] == {
        "address_0x00599C69_semantics": "Unknown",
        "binary_sha256": BUGS_EXE_SHA256,
        "executes_downstream_rules": False,
        "global_family_exclusivity_claimed": False,
        "scope": "twelve_confirmed_tunnels_city_mechanisms",
        "writes_files_or_target_state": False,
    }
    assert report["result"]["decision"]["opens"] is True
    assert report["result"]["direct_writes"][1]["target"] == "address_0x00599C69"


def test_reporting_surface_models_all_nine_tunnels_rows_and_coupling() -> None:
    payload = {
        "family": "tunnels",
        "internal_level": 3,
        "flik_x": TUNNELS_STANDOFFS[0][0],
        "flik_z": TUNNELS_STANDOFFS[0][1],
        "grain_count": 1,
        "radius": 100,
        "records": [asdict(record) for record in _tunnels_records()],
    }
    result = subprocess.run(
        [str(PYTHON), str(SCRIPT), "-"],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)["result"]
    assert len(report["decisions"]) == 9
    assert [write["target"] for write in report["direct_writes"]] == [
        "tunnels_record[0].type",
        "tunnels_record[4].type",
    ]
    assert report["newly_coupled_rows_entering_decay_later_this_pass"] == [4]
    assert report["records_after_direct_writes"][4]["unknown_04"] == 25


def test_reporting_surface_accepts_valid_path_input(tmp_path: Path) -> None:
    request = tmp_path / "city-request.json"
    request.write_text(json.dumps(_city_json_payload()), encoding="utf-8")
    result = subprocess.run(
        [str(PYTHON), str(SCRIPT), str(request)],
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["result"]["decision"]["opens"] is True


@pytest.mark.parametrize("location", ["request", "gate", "record"])
def test_reporting_surface_rejects_duplicate_json_keys(location: str) -> None:
    if location == "request":
        payload = json.dumps(_city_json_payload()).replace(
            '"family": "city_entrance"',
            '"family": "other", "family": "city_entrance"',
            1,
        )
        duplicate_key = "family"
    elif location == "gate":
        payload = json.dumps(_city_json_payload()).replace(
            '"index": 0',
            '"index": 0, "index": 1',
            1,
        )
        duplicate_key = "index"
    else:
        tunnels_payload = {
            "family": "tunnels",
            "internal_level": 3,
            "flik_x": TUNNELS_STANDOFFS[0][0],
            "flik_z": TUNNELS_STANDOFFS[0][1],
            "grain_count": 1,
            "records": [asdict(record) for record in _tunnels_records()],
        }
        payload = json.dumps(tunnels_payload).replace(
            '"requirement": 1',
            '"requirement": 1, "requirement": 50',
            1,
        )
        duplicate_key = "requirement"

    result = subprocess.run(
        [str(PYTHON), str(SCRIPT), "-"],
        input=payload,
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr == f"error: duplicate JSON key: {duplicate_key}\n"


def test_reporting_surface_rejects_unknown_keys() -> None:
    payload = _city_json_payload()
    payload["semantic_name_for_0x00599C69"] = "invented"
    result = subprocess.run(
        [str(PYTHON), str(SCRIPT), "-"],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert result.returncode == 2
    assert "unknown keys" in result.stderr
