"""Pure PC grain-gate opening resolver for the two admitted gate families.

This module models only the opening decisions and direct writes in the exact
retail PC executable:

* the ordered nine-row Tunnels loop at ``0x00432EEA-0x00433043``; and
* one City Entrance call to ``0x00433790`` with its call-site metadata.

It preserves the native signed 32-bit ``sub``/``sar 8``/``imul``/``add``
arithmetic and signed comparison.  Tunnels row order is observable because
opening row 0 writes row 4 before row 4's later visit, while opening row 4
writes row 0 after row 0's visit.  City index 0 includes the address-named
byte write ``[0x00599C69] = 1``; the byte's meaning is Unknown (KU-067).

The returned downstream rules explain the accepted terminal receipts but are
metadata, not a reimplementation of animation, rendering, message/audio
dispatch, callee side effects, persistence, or the rest of either level
update.  The module does not claim these are the only grain-gate families in
the executable: EXP-20260816-146 established only the direct/static census.

Evidence: exact retail SHA-256
``97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878``;
EXP-20260815-137/138/139, EXP-20260816-144/145/148/149/166/168/169.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum


BUGS_EXE_SHA256 = (
    "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
)

TUNNELS_INTERNAL_LEVEL = 3
CITY_ENTRANCE_INTERNAL_LEVEL = 4

TUNNELS_LOOP_START = 0x00432EEA
TUNNELS_LOOP_END = 0x00433043
TUNNELS_GRAIN_COMPARE = 0x00432F12
TUNNELS_PROXIMITY_COMPARE = 0x00432F49
TUNNELS_OPEN_WRITE = 0x00432F6A
TUNNELS_ROW0_COUPLING_WRITE = 0x00432F85
TUNNELS_ROW4_COUPLING_WRITE = 0x00432F9D
TUNNELS_DECAY_COMPARE = 0x00433017
TUNNELS_DECAY_WRITE = 0x00433024
TUNNELS_TABLE_ADDRESS = 0x004DA9C8
TUNNELS_RECORD_SIZE = 20
TUNNELS_RECORD_COUNT = 9
TUNNELS_CLOSED_TYPE = 0x10C7
TUNNELS_OPEN_TYPE = 0x1068
TUNNELS_OPEN_RADIUS = 100
TUNNELS_DECAY_THRESHOLD = 0x708
TUNNELS_DECAY_DELTA = -140

CITY_ROUTINE = 0x00433790
CITY_PROXIMITY_HELPER = 0x00416580
CITY_GRAIN_COMPARE = 0x004337E1
CITY_OPEN_WRITE = 0x004337EF
CITY_INDEX0_BYTE_WRITE = 0x00433807
CITY_DOWNSTREAM_STATE_WRITE = 0x0043384B
CITY_DOWNSTREAM_SLOT_A_WRITE = 0x00433865
CITY_DOWNSTREAM_SLOT_B_WRITE = 0x00433879
CITY_STATE_ADDRESS = 0x0059F020
CITY_ANIMATION_ADDRESS = 0x0059F030
CITY_INDEX0_BYTE_ADDRESS = 0x00599C69
CITY_CLOSED_STATE = -1
CITY_OPEN_STATE = 0x20

SUPPORTED_REQUIREMENT_MIN = 0
SUPPORTED_REQUIREMENT_MAX = 50
I32_MIN = -0x80000000
I32_MAX = 0x7FFFFFFF


class GrainGateResolverError(ValueError):
    """Raised when an input is outside the admitted resolver contract."""


class NonOpeningReason(StrEnum):
    """The first native opening predicate that refuses a gate."""

    ALREADY_NON_CLOSED = "already_non_closed"
    INSUFFICIENT_GRAIN = "insufficient_grain"
    OUTSIDE_PROXIMITY = "outside_proximity"


def _i32(value: int) -> int:
    """The low 32 bits interpreted as a signed two's-complement value."""

    return (value + 0x80000000) % 0x100000000 - 0x80000000


def _require_int(value: int, *, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise GrainGateResolverError(f"{label} is not an integer")
    return value


def _require_i32(value: int, *, label: str) -> int:
    value = _require_int(value, label=label)
    if value < I32_MIN or value > I32_MAX:
        raise GrainGateResolverError(f"{label} is outside signed int32")
    return value


def _require_requirement(value: int, *, label: str) -> int:
    value = _require_int(value, label=label)
    if not SUPPORTED_REQUIREMENT_MIN <= value <= SUPPORTED_REQUIREMENT_MAX:
        raise GrainGateResolverError(
            f"{label} is outside the supported authored 0..50 range"
        )
    return value


def _require_grain(value: int) -> int:
    value = _require_int(value, label="grain_count")
    if not 0 <= value <= 0xFF:
        raise GrainGateResolverError("grain_count is outside unsigned byte")
    return value


def _imul32(left: int, right: int) -> int:
    return _i32(left * right)


def proximity_distance_sq(
    flik_x: int,
    flik_z: int,
    center_x: int,
    center_z: int,
) -> int:
    """Distance accumulator used inline at ``0x00432F33-0x00432F47``.

    The subtractions wrap before the arithmetic shifts.  Both products and
    their addition also wrap to signed 32-bit values.
    """

    flik_x = _require_i32(flik_x, label="flik_x")
    flik_z = _require_i32(flik_z, label="flik_z")
    center_x = _require_i32(center_x, label="center_x")
    center_z = _require_i32(center_z, label="center_z")
    dx = _i32(flik_x - center_x) >> 8
    dz = _i32(flik_z - center_z) >> 8
    return _i32(_imul32(dx, dx) + _imul32(dz, dz))


def proximity_radius_sq(radius: int) -> int:
    """The wrapping ``imul radius, radius`` at ``0x004165B0``."""

    return _imul32(_require_i32(radius, label="radius"), radius)


def inside_proximity(
    flik_x: int,
    flik_z: int,
    center_x: int,
    center_z: int,
    radius: int,
) -> bool:
    """Native signed ``distance_sq < radius_sq`` verdict."""

    return proximity_distance_sq(flik_x, flik_z, center_x, center_z) < (
        proximity_radius_sq(radius)
    )


@dataclass(frozen=True)
class MemoryWrite:
    """One direct write performed by an admitted opening branch."""

    address: int
    width_bits: int
    value: int
    instruction_address: int
    target: str


@dataclass(frozen=True)
class GateDecision:
    """One row/index's opening decision in native evaluation order."""

    gate_index: int
    opens: bool
    reason: NonOpeningReason | None
    state_at_visit: int
    distance_sq: int | None
    radius_sq: int | None


@dataclass(frozen=True)
class TunnelsRecord:
    """One ordered 20-byte resident row at ``0x004DA9C8``.

    ``unknown_04`` is deliberately address-named and preserved.  No semantic
    interpretation has been established for it.
    """

    type_value: int
    unknown_04: int
    requirement: int
    center_x: int
    center_z: int

    def __post_init__(self) -> None:
        _require_i32(self.type_value, label="Tunnels type_value")
        _require_i32(self.unknown_04, label="Tunnels unknown_04")
        _require_requirement(self.requirement, label="Tunnels requirement")
        _require_i32(self.center_x, label="Tunnels center_x")
        _require_i32(self.center_z, label="Tunnels center_z")


@dataclass(frozen=True)
class TunnelsRequest:
    """Explicit inputs for one ordered pass over the nine opening tests."""

    internal_level: int
    flik_x: int
    flik_z: int
    grain_count: int
    records: tuple[TunnelsRecord, ...]
    radius: int = TUNNELS_OPEN_RADIUS

    def __post_init__(self) -> None:
        _require_int(self.internal_level, label="internal_level")
        if self.internal_level != TUNNELS_INTERNAL_LEVEL:
            raise GrainGateResolverError(
                "Tunnels resolver requires internal level 3"
            )
        _require_i32(self.flik_x, label="flik_x")
        _require_i32(self.flik_z, label="flik_z")
        _require_grain(self.grain_count)
        _require_i32(self.radius, label="radius")
        if not isinstance(self.records, tuple):
            raise GrainGateResolverError("Tunnels records must be an ordered tuple")
        if len(self.records) != TUNNELS_RECORD_COUNT:
            raise GrainGateResolverError("Tunnels requires exactly nine records")
        if not all(isinstance(record, TunnelsRecord) for record in self.records):
            raise GrainGateResolverError("Tunnels records contain a non-record value")


@dataclass(frozen=True)
class TunnelsDecayRule:
    """Downstream rule metadata from ``0x00433017-0x00433024``."""

    signed_type_greater_than: int = TUNNELS_DECAY_THRESHOLD
    wrapping_delta: int = TUNNELS_DECAY_DELTA
    compare_instruction: int = TUNNELS_DECAY_COMPARE
    write_instruction: int = TUNNELS_DECAY_WRITE
    ordered_row_visits: bool = True
    follows_non_closed_opening_refusal: bool = True


@dataclass(frozen=True)
class TunnelsResult:
    """Opening decisions and writes; no message/callee/decay execution."""

    family: str
    internal_level: int
    decisions: tuple[GateDecision, ...]
    direct_writes: tuple[MemoryWrite, ...]
    records_after_direct_writes: tuple[TunnelsRecord, ...]
    downstream_rule: TunnelsDecayRule
    newly_coupled_rows_entering_decay_later_this_pass: tuple[int, ...]

    @property
    def opened_rows(self) -> tuple[int, ...]:
        return tuple(decision.gate_index for decision in self.decisions if decision.opens)


def _tunnels_type_address(row_index: int) -> int:
    return TUNNELS_TABLE_ADDRESS + row_index * TUNNELS_RECORD_SIZE


def resolve_tunnels(request: TunnelsRequest) -> TunnelsResult:
    """Reproduce the opening half of the ordered Tunnels nine-row loop.

    Opening writes are applied to a private record copy so later rows observe
    earlier row-0/4 coupling exactly.  The function does not execute the
    downstream decay path; it reports that rule separately.
    """

    records = list(request.records)
    decisions: list[GateDecision] = []
    writes: list[MemoryWrite] = []
    later_coupled: list[int] = []
    radius_sq = proximity_radius_sq(request.radius)

    for row_index in range(TUNNELS_RECORD_COUNT):
        record = records[row_index]
        if record.type_value != TUNNELS_CLOSED_TYPE:
            decisions.append(
                GateDecision(
                    gate_index=row_index,
                    opens=False,
                    reason=NonOpeningReason.ALREADY_NON_CLOSED,
                    state_at_visit=record.type_value,
                    distance_sq=None,
                    radius_sq=None,
                )
            )
            continue

        # Tunnels compares grain before it evaluates the opening radius.
        if request.grain_count < record.requirement:
            decisions.append(
                GateDecision(
                    gate_index=row_index,
                    opens=False,
                    reason=NonOpeningReason.INSUFFICIENT_GRAIN,
                    state_at_visit=record.type_value,
                    distance_sq=None,
                    radius_sq=None,
                )
            )
            continue

        distance_sq = proximity_distance_sq(
            request.flik_x,
            request.flik_z,
            record.center_x,
            record.center_z,
        )
        if distance_sq >= radius_sq:
            decisions.append(
                GateDecision(
                    gate_index=row_index,
                    opens=False,
                    reason=NonOpeningReason.OUTSIDE_PROXIMITY,
                    state_at_visit=record.type_value,
                    distance_sq=distance_sq,
                    radius_sq=radius_sq,
                )
            )
            continue

        decisions.append(
            GateDecision(
                gate_index=row_index,
                opens=True,
                reason=None,
                state_at_visit=record.type_value,
                distance_sq=distance_sq,
                radius_sq=radius_sq,
            )
        )
        records[row_index] = replace(record, type_value=TUNNELS_OPEN_TYPE)
        writes.append(
            MemoryWrite(
                address=_tunnels_type_address(row_index),
                width_bits=32,
                value=TUNNELS_OPEN_TYPE,
                instruction_address=TUNNELS_OPEN_WRITE,
                target=f"tunnels_record[{row_index}].type",
            )
        )

        if row_index == 0:
            records[4] = replace(records[4], type_value=TUNNELS_OPEN_TYPE)
            writes.append(
                MemoryWrite(
                    address=_tunnels_type_address(4),
                    width_bits=32,
                    value=TUNNELS_OPEN_TYPE,
                    instruction_address=TUNNELS_ROW0_COUPLING_WRITE,
                    target="tunnels_record[4].type",
                )
            )
            later_coupled.append(4)
        elif row_index == 4:
            records[0] = replace(records[0], type_value=TUNNELS_OPEN_TYPE)
            writes.append(
                MemoryWrite(
                    address=_tunnels_type_address(0),
                    width_bits=32,
                    value=TUNNELS_OPEN_TYPE,
                    instruction_address=TUNNELS_ROW4_COUPLING_WRITE,
                    target="tunnels_record[0].type",
                )
            )

    return TunnelsResult(
        family="tunnels",
        internal_level=request.internal_level,
        decisions=tuple(decisions),
        direct_writes=tuple(writes),
        records_after_direct_writes=tuple(records),
        downstream_rule=TunnelsDecayRule(),
        newly_coupled_rows_entering_decay_later_this_pass=tuple(later_coupled),
    )


@dataclass(frozen=True)
class CityGate:
    """One exact ``0x00433900``-style call-site descriptor."""

    index: int
    state: int
    requirement: int
    center_x: int
    center_z: int
    radius: int
    delta_a: int
    delta_b: int
    slot_a: int
    slot_b: int

    def __post_init__(self) -> None:
        _require_int(self.index, label="City gate index")
        if not 0 <= self.index <= 2:
            raise GrainGateResolverError("City gate index is outside 0..2")
        _require_i32(self.state, label="City state")
        _require_requirement(self.requirement, label="City requirement")
        _require_i32(self.center_x, label="City center_x")
        _require_i32(self.center_z, label="City center_z")
        _require_i32(self.radius, label="City radius")
        _require_i32(self.delta_a, label="City delta_a")
        _require_i32(self.delta_b, label="City delta_b")
        for name, slot in (("slot_a", self.slot_a), ("slot_b", self.slot_b)):
            _require_int(slot, label=f"City {name}")
            if not 0 <= slot <= 5:
                raise GrainGateResolverError(f"City {name} is outside 0..5")


@dataclass(frozen=True)
class CityRequest:
    """Explicit inputs for one admitted City gate call."""

    internal_level: int
    flik_x: int
    flik_z: int
    grain_count: int
    gate: CityGate

    def __post_init__(self) -> None:
        _require_int(self.internal_level, label="internal_level")
        if self.internal_level != CITY_ENTRANCE_INTERNAL_LEVEL:
            raise GrainGateResolverError(
                "City Entrance resolver requires internal level 4"
            )
        _require_i32(self.flik_x, label="flik_x")
        _require_i32(self.flik_z, label="flik_z")
        _require_grain(self.grain_count)
        if not isinstance(self.gate, CityGate):
            raise GrainGateResolverError("City request gate is not a CityGate")


@dataclass(frozen=True)
class CityDownstreamRule:
    """The positive-state countdown/slot-delta rule after the opening branch."""

    state_address: int
    signed_state_greater_than: int
    wrapping_state_delta: int
    state_write_instruction: int
    slot_a: int
    slot_a_address: int
    wrapping_delta_a: int
    slot_a_write_instruction: int
    slot_b: int
    slot_b_address: int
    wrapping_delta_b: int
    slot_b_write_instruction: int
    opening_state: int
    steps_from_opening_state_to_zero: int
    aggregate_delta_a_from_zero: int
    aggregate_delta_b_from_zero: int
    first_step_occurs_in_opening_call: bool


@dataclass(frozen=True)
class CityResult:
    """One City opening decision, direct write plan, and downstream metadata."""

    family: str
    internal_level: int
    decision: GateDecision
    direct_writes: tuple[MemoryWrite, ...]
    downstream_rule: CityDownstreamRule


def city_retail_requirement(gate_index: int) -> int:
    """Retail ``10 * (index + 1)`` from ``0x004337D1-0x004337DF``."""

    gate_index = _require_int(gate_index, label="City gate index")
    if not 0 <= gate_index <= 2:
        raise GrainGateResolverError("City gate index is outside 0..2")
    return 10 * (gate_index + 1)


def _city_downstream_rule(gate: CityGate) -> CityDownstreamRule:
    return CityDownstreamRule(
        state_address=CITY_STATE_ADDRESS + gate.index * 4,
        signed_state_greater_than=0,
        wrapping_state_delta=-1,
        state_write_instruction=CITY_DOWNSTREAM_STATE_WRITE,
        slot_a=gate.slot_a,
        slot_a_address=CITY_ANIMATION_ADDRESS + gate.slot_a * 4,
        wrapping_delta_a=gate.delta_a,
        slot_a_write_instruction=CITY_DOWNSTREAM_SLOT_A_WRITE,
        slot_b=gate.slot_b,
        slot_b_address=CITY_ANIMATION_ADDRESS + gate.slot_b * 4,
        wrapping_delta_b=gate.delta_b,
        slot_b_write_instruction=CITY_DOWNSTREAM_SLOT_B_WRITE,
        opening_state=CITY_OPEN_STATE,
        steps_from_opening_state_to_zero=CITY_OPEN_STATE,
        aggregate_delta_a_from_zero=_i32(gate.delta_a * CITY_OPEN_STATE),
        aggregate_delta_b_from_zero=_i32(gate.delta_b * CITY_OPEN_STATE),
        first_step_occurs_in_opening_call=True,
    )


def resolve_city(request: CityRequest) -> CityResult:
    """Reproduce one City opening decision and its ordered direct writes."""

    gate = request.gate
    rule = _city_downstream_rule(gate)
    if gate.state != CITY_CLOSED_STATE:
        decision = GateDecision(
            gate_index=gate.index,
            opens=False,
            reason=NonOpeningReason.ALREADY_NON_CLOSED,
            state_at_visit=gate.state,
            distance_sq=None,
            radius_sq=None,
        )
        return CityResult(
            family="city_entrance",
            internal_level=request.internal_level,
            decision=decision,
            direct_writes=(),
            downstream_rule=rule,
        )

    # City evaluates proximity before its grain comparison.
    distance_sq = proximity_distance_sq(
        request.flik_x,
        request.flik_z,
        gate.center_x,
        gate.center_z,
    )
    radius_sq = proximity_radius_sq(gate.radius)
    if distance_sq >= radius_sq:
        decision = GateDecision(
            gate_index=gate.index,
            opens=False,
            reason=NonOpeningReason.OUTSIDE_PROXIMITY,
            state_at_visit=gate.state,
            distance_sq=distance_sq,
            radius_sq=radius_sq,
        )
        return CityResult(
            family="city_entrance",
            internal_level=request.internal_level,
            decision=decision,
            direct_writes=(),
            downstream_rule=rule,
        )

    if request.grain_count < gate.requirement:
        decision = GateDecision(
            gate_index=gate.index,
            opens=False,
            reason=NonOpeningReason.INSUFFICIENT_GRAIN,
            state_at_visit=gate.state,
            distance_sq=distance_sq,
            radius_sq=radius_sq,
        )
        return CityResult(
            family="city_entrance",
            internal_level=request.internal_level,
            decision=decision,
            direct_writes=(),
            downstream_rule=rule,
        )

    writes = [
        MemoryWrite(
            address=CITY_STATE_ADDRESS + gate.index * 4,
            width_bits=32,
            value=CITY_OPEN_STATE,
            instruction_address=CITY_OPEN_WRITE,
            target=f"city_state[{gate.index}]",
        )
    ]
    if gate.index == 0:
        writes.append(
            MemoryWrite(
                address=CITY_INDEX0_BYTE_ADDRESS,
                width_bits=8,
                value=1,
                instruction_address=CITY_INDEX0_BYTE_WRITE,
                target="address_0x00599C69",
            )
        )

    return CityResult(
        family="city_entrance",
        internal_level=request.internal_level,
        decision=GateDecision(
            gate_index=gate.index,
            opens=True,
            reason=None,
            state_at_visit=gate.state,
            distance_sq=distance_sq,
            radius_sq=radius_sq,
        ),
        direct_writes=tuple(writes),
        downstream_rule=rule,
    )
