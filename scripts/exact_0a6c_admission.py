"""Exact, payload-free admission evaluator for entry 7 / file offset 0x0A6C.

This module is intentionally not a general record or geometry evaluator.  It
implements only the PC-native signed arithmetic and ordered rejection chain
specified by EXP-20260813-044 for executable BIN-97c95ba5572dce63.  Raw source,
global, and projected values are transient inputs; the only serializable
product is the metadata receipt built by :func:`reconcile_receipt`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import struct
from typing import Callable


RECEIPT_SCHEMA_VERSION = 1
EXACT_EXE_SHA256 = (
    "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
)
EXACT_RECORD_PLAN_COUNT = 168
EXACT_RECORD_PLAN_SHA256 = (
    "5eb280a7bd54b56a9654fed7984e9677a15618c5376be703a85718ea3bb2ffec"
)
EXACT_CONSECUTIVE_CAPTURE_CYCLES = 3
EXACT_ALLOWED_CAPTURE_CYCLES = (1, EXACT_CONSECUTIVE_CAPTURE_CYCLES)
EXACT_ENTRY_INDEX = 7
EXACT_FILE_OFFSET = 0x0A6C
EXACT_FORM = 0x3C
EXACT_PAGE = 16
EXACT_CALLER_MODE = 2

PAGE_CLASS_BASE = 0x005836A4
ROOT_POINTER_ADDRESS = 0x004C4108
ROW_COEFFICIENT_ADDRESSES = (
    (0x0063E888, 0x0063E88C, 0x0063E890),
    (0x0063E898, 0x0063E89C, 0x0063E8A0),
    (0x0063E8A8, 0x0063E8AC, 0x0063E8B0),
)
ROW_OFFSET_ADDRESSES = (0x0063E8B8, 0x0063E8BC, 0x0063E8C0)
SCALE_ADDRESS = 0x00511508
PROJECTION_OFFSET_ADDRESSES = (0x00861DD8, 0x00861DDC)
MAX_P_ADDRESS = 0x00861C60
MAX_Q_ADDRESS = 0x00861DAC
DEPTH_SELECTOR_ADDRESS = 0x005BA120
DEPTH_MODE_0_THRESHOLD_ADDRESS = 0x005B56D0
DEPTH_MODE_1_THRESHOLD_ADDRESS = 0x005BA80C

REJECT_PCS = (
    0x00405FFF,
    0x0040600F,
    0x004064E4,
    0x00406502,
    0x00406533,
    0x0040654E,
    0x004065B0,
    0x00406636,
    0x00406660,
    0x00406672,
    0x0040668B,
    0x004066A4,
    0x004066BD,
)
_REJECT_SLOT_BY_PC = {
    pc: slot for pc, slot in zip(
        REJECT_PCS, (1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12)
    )
}

_DIGEST_DOMAIN = b"ABLPC exact-0a6c active-state v1\x00"
_UINT32_MASK = (1 << 32) - 1
_INT32_MIN = -(1 << 31)


class AdmissionEvaluationError(RuntimeError):
    """The exact evaluator could not produce an admissible receipt."""


@dataclass(frozen=True)
class ProjectedInputs:
    """Transient structural intermediates used by the exact predicate chain."""

    p: tuple[int, int, int, int]
    q: tuple[int, int, int, int]
    r: tuple[int, int, int, int]


@dataclass(frozen=True)
class PredicateDecision:
    first_reject_pc: int | None
    evaluated_predicate_count: int

    @property
    def predicted_append(self) -> bool:
        return self.first_reject_pc is None


@dataclass(frozen=True)
class AdmissionEvaluation:
    """Payload-free pre-call result plus private addresses for re-digesting."""

    active_state_sha256: str
    evaluated_predicate_count: int
    first_reject_pc: int | None
    predicted_append: bool
    active_addresses: tuple[int, ...] = field(repr=False)


class _ActiveState:
    def __init__(self, read_u32: Callable[[int], int]) -> None:
        self._read_u32 = read_u32
        self._digest = hashlib.sha256(_DIGEST_DOMAIN)
        self._addresses: list[int] = []

    def read(self, address: int) -> int:
        try:
            value = self._read_u32(address)
        except Exception as exc:
            raise AdmissionEvaluationError(
                "active-state read failed closed"
            ) from exc
        if (
            not isinstance(value, int)
            or isinstance(value, bool)
            or not 0 <= value <= _UINT32_MASK
        ):
            raise AdmissionEvaluationError("active-state read failed closed")
        self._digest.update(struct.pack("<II", address, value))
        self._addresses.append(address)
        return value

    @property
    def addresses(self) -> tuple[int, ...]:
        return tuple(self._addresses)

    def hexdigest(self) -> str:
        return self._digest.hexdigest()


def signed16(value: int) -> int:
    value &= 0xFFFF
    return value - (1 << 16) if value & 0x8000 else value


def signed32(value: int) -> int:
    value &= _UINT32_MASK
    return value - (1 << 32) if value & (1 << 31) else value


def wrap32(value: int) -> int:
    return signed32(value)


def trunc_div_signed32(numerator: int, denominator: int) -> int:
    """Reproduce x86 signed ``idiv`` quotient behavior or fail closed."""

    numerator = signed32(numerator)
    denominator = signed32(denominator)
    if denominator == 0 or (
        numerator == _INT32_MIN and denominator == -1
    ):
        raise AdmissionEvaluationError("native signed division failed closed")
    quotient = abs(numerator) // abs(denominator)
    return -quotient if (numerator < 0) != (denominator < 0) else quotient


def _mul32(left: int, right: int) -> int:
    return wrap32(left * right)


def _add32(left: int, right: int) -> int:
    return wrap32(left + right)


def _sub32(left: int, right: int) -> int:
    return wrap32(left - right)


def _transform_row(
    source: tuple[int, int, int],
    coefficients: tuple[int, int, int],
    offset: int,
) -> int:
    value = _mul32(source[0], coefficients[0])
    value = _add32(value, _mul32(source[1], coefficients[1]))
    value = _add32(value, _mul32(source[2], coefficients[2]))
    value = _add32(value, 0xFFF if value < 0 else 0)
    value = value >> 12
    return signed16(_add32(value, offset))


def _project_inputs(
    source_words: tuple[tuple[int, int, int], ...],
    active: _ActiveState,
) -> ProjectedInputs:
    coefficients = tuple(
        tuple(signed32(active.read(address)) for address in row)
        for row in ROW_COEFFICIENT_ADDRESSES
    )
    row_offsets = tuple(
        signed32(active.read(address)) for address in ROW_OFFSET_ADDRESSES
    )
    scale = signed32(active.read(SCALE_ADDRESS))
    projection_offsets = tuple(
        signed32(active.read(address))
        for address in PROJECTION_OFFSET_ADDRESSES
    )
    half = trunc_div_signed32(scale, 2)

    transformed = []
    for source in source_words:
        transformed.append(tuple(
            _transform_row(source, coefficients[row], row_offsets[row])
            for row in range(3)
        ))

    p_values = []
    q_values = []
    r_values = []
    for row_0, row_1, row_2 in transformed:
        denominator = max(half, row_2)
        projected_p = trunc_div_signed32(_mul32(row_0, scale), denominator)
        projected_q = trunc_div_signed32(_mul32(row_1, scale), denominator)
        p_values.append(signed16(_add32(projected_p, projection_offsets[0])))
        q_values.append(signed16(_add32(projected_q, projection_offsets[1])))
        r_values.append(row_2)
    return ProjectedInputs(
        tuple(p_values), tuple(q_values), tuple(r_values)  # type: ignore[arg-type]
    )


def _orientation_reject(projected: ProjectedInputs) -> bool:
    p = projected.p
    q = projected.q
    a = _sub32(
        _mul32(_sub32(q[0], q[1]), _sub32(p[2], p[1])),
        _mul32(_sub32(p[0], p[1]), _sub32(q[2], q[1])),
    )
    if a >= 0:
        return False
    b = _sub32(
        _mul32(_sub32(p[2], p[3]), _sub32(q[1], q[3])),
        _mul32(_sub32(q[2], q[3]), _sub32(p[1], p[3])),
    )
    return b < 0


def _evaluate_projected_chain(
    projected: ProjectedInputs,
    active: _ActiveState,
) -> PredicateDecision:
    p = projected.p
    q = projected.q
    r = projected.r

    max_p = signed32(active.read(MAX_P_ADDRESS))
    if all(value > max_p for value in p):
        return PredicateDecision(0x004064E4, 3)
    if all(value < 0 for value in p):
        return PredicateDecision(0x00406502, 4)

    max_q = signed32(active.read(MAX_Q_ADDRESS))
    if all(value > max_q for value in q):
        return PredicateDecision(0x00406533, 5)
    if all(value < 0 for value in q):
        return PredicateDecision(0x0040654E, 6)
    if _orientation_reject(projected):
        return PredicateDecision(0x004065B0, 7)

    depth_selector = signed32(active.read(DEPTH_SELECTOR_ADDRESS))
    if depth_selector == 1:
        threshold = signed32(active.read(DEPTH_MODE_1_THRESHOLD_ADDRESS))
        if all(value < threshold for value in r):
            return PredicateDecision(0x00406636, 8)
    elif depth_selector == 0:
        threshold = wrap32(
            4 * signed32(active.read(DEPTH_MODE_0_THRESHOLD_ADDRESS))
        )
        if all(value > threshold for value in r):
            return PredicateDecision(0x00406660, 8)

    absolute_reject_pcs = (
        0x00406672,
        0x0040668B,
        0x004066A4,
        0x004066BD,
    )
    for index, value in enumerate(p):
        if abs(value) > 10000:
            return PredicateDecision(absolute_reject_pcs[index], 9 + index)
    return PredicateDecision(None, 12)


def evaluate_projected_chain(
    projected: ProjectedInputs,
    read_u32: Callable[[int], int],
) -> PredicateDecision:
    """Exercise slots 3..12 of the exact chain with transient test inputs."""

    return _evaluate_projected_chain(projected, _ActiveState(read_u32))


def evaluate_exact_0a6c(
    source_words: tuple[tuple[int, int, int], ...],
    classification_word: int,
    read_u32: Callable[[int], int],
) -> AdmissionEvaluation:
    """Evaluate the exact pre-call chain and retain no raw input values."""

    if len(source_words) != 4 or any(len(item) != 3 for item in source_words):
        raise AdmissionEvaluationError("source input shape validation failed")
    normalized_source = tuple(
        tuple(signed16(value) for value in item) for item in source_words
    )
    classification = signed16(classification_word)
    page = (classification >> 8) & 0x1F
    caller_mode = 2 if classification > 0 else 0
    if page != EXACT_PAGE or caller_mode != EXACT_CALLER_MODE:
        raise AdmissionEvaluationError("source classification validation failed")

    active = _ActiveState(read_u32)
    page_class = active.read(PAGE_CLASS_BASE + page * 4)
    if signed32(page_class) != 3:
        decision = PredicateDecision(0x00405FFF, 1)
    else:
        root = active.read(ROOT_POINTER_ADDRESS)
        page_pointer = active.read((root + page * 4) & _UINT32_MASK)
        if page_pointer == 0:
            decision = PredicateDecision(0x0040600F, 2)
        else:
            projected = _project_inputs(normalized_source, active)
            decision = _evaluate_projected_chain(projected, active)

    return AdmissionEvaluation(
        active_state_sha256=active.hexdigest(),
        evaluated_predicate_count=decision.evaluated_predicate_count,
        first_reject_pc=decision.first_reject_pc,
        predicted_append=decision.predicted_append,
        active_addresses=active.addresses,
    )


def digest_active_state(
    read_u32: Callable[[int], int],
    addresses: tuple[int, ...],
) -> str:
    active = _ActiveState(read_u32)
    for address in addresses:
        active.read(address)
    return active.hexdigest()


def reconcile_receipt(
    evaluation: AdmissionEvaluation,
    observed_append: bool,
    post_read_u32: Callable[[int], int],
) -> dict:
    """Re-digest state and return only the M2.31 metadata receipt fields."""

    if not isinstance(observed_append, bool):
        raise AdmissionEvaluationError("observed append validation failed")
    expected_count = (
        12
        if evaluation.first_reject_pc is None
        else _REJECT_SLOT_BY_PC.get(evaluation.first_reject_pc)
    )
    if (
        expected_count is None
        or evaluation.evaluated_predicate_count != expected_count
        or evaluation.predicted_append
        != (evaluation.first_reject_pc is None)
    ):
        raise AdmissionEvaluationError("evaluation metadata validation failed")
    post_digest = digest_active_state(post_read_u32, evaluation.active_addresses)
    if post_digest != evaluation.active_state_sha256:
        raise AdmissionEvaluationError("active-state digest changed")
    return {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "entry_index": EXACT_ENTRY_INDEX,
        "file_offset": EXACT_FILE_OFFSET,
        "form": EXACT_FORM,
        "page_16_validated": True,
        "caller_mode_2_validated": True,
        "active_state_sha256": evaluation.active_state_sha256,
        "evaluated_predicate_count": evaluation.evaluated_predicate_count,
        "first_reject_pc": (
            None
            if evaluation.first_reject_pc is None
            else f"0x{evaluation.first_reject_pc:08X}"
        ),
        "predicted_append": evaluation.predicted_append,
        "observed_append": observed_append,
        "prediction_matches_observation": (
            evaluation.predicted_append == observed_append
        ),
        "raw_inputs_retained": False,
        "payload_bytes_retained": 0,
    }
