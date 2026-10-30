from __future__ import annotations

from dataclasses import fields
import json
from pathlib import Path
import sys

import pytest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import exact_0a6c_admission as admission  # noqa: E402


def _projected(
    *,
    p: tuple[int, int, int, int] = (0, 0, 0, 0),
    q: tuple[int, int, int, int] = (0, 0, 0, 0),
    r: tuple[int, int, int, int] = (0, 0, 0, 0),
) -> admission.ProjectedInputs:
    return admission.ProjectedInputs(p=p, q=q, r=r)


def _predicate_reader(
    *, max_p: int = 20_000, max_q: int = 20_000,
    depth_selector: int = 2, mode_0_threshold: int = 0,
    mode_1_threshold: int = 0,
):
    values = {
        admission.MAX_P_ADDRESS: max_p & 0xFFFFFFFF,
        admission.MAX_Q_ADDRESS: max_q & 0xFFFFFFFF,
        admission.DEPTH_SELECTOR_ADDRESS: depth_selector & 0xFFFFFFFF,
        admission.DEPTH_MODE_0_THRESHOLD_ADDRESS:
            mode_0_threshold & 0xFFFFFFFF,
        admission.DEPTH_MODE_1_THRESHOLD_ADDRESS:
            mode_1_threshold & 0xFFFFFFFF,
    }
    reads = []

    def read(address: int) -> int:
        reads.append(address)
        return values[address]

    return read, reads


@pytest.mark.parametrize(
    ("projected", "reader_kwargs", "reject_pc", "count"),
    [
        (_projected(p=(2, 2, 2, 2)), {"max_p": 1}, 0x004064E4, 3),
        (_projected(p=(-1, -2, -3, -4)), {}, 0x00406502, 4),
        (_projected(q=(2, 2, 2, 2)), {"max_q": 1}, 0x00406533, 5),
        (_projected(q=(-1, -2, -3, -4)), {}, 0x0040654E, 6),
        (
            _projected(p=(0, 0, 10, 0), q=(0, 10, 0, 20)),
            {}, 0x004065B0, 7,
        ),
        (
            _projected(r=(-2, -2, -2, -2)),
            {"depth_selector": 1, "mode_1_threshold": -1},
            0x00406636, 8,
        ),
        (
            _projected(r=(5, 5, 5, 5)),
            {"depth_selector": 0, "mode_0_threshold": 1},
            0x00406660, 8,
        ),
        (_projected(p=(10001, 0, 0, 0)), {}, 0x00406672, 9),
        (_projected(p=(0, -10001, 0, 0)), {}, 0x0040668B, 10),
        (_projected(p=(0, 0, 10001, 0)), {}, 0x004066A4, 11),
        (_projected(p=(0, 0, 0, -10001)), {}, 0x004066BD, 12),
    ],
)
def test_every_projected_rejection_path(
    projected: admission.ProjectedInputs,
    reader_kwargs: dict,
    reject_pc: int,
    count: int,
) -> None:
    reader, _reads = _predicate_reader(**reader_kwargs)
    result = admission.evaluate_projected_chain(projected, reader)
    assert result.first_reject_pc == reject_pc
    assert result.evaluated_predicate_count == count
    assert result.predicted_append is False


@pytest.mark.parametrize("depth_selector", [0, 1, 2])
def test_depth_branches_and_skip_can_pass(depth_selector: int) -> None:
    reader, reads = _predicate_reader(
        depth_selector=depth_selector,
        mode_0_threshold=1,
        mode_1_threshold=-1,
    )
    result = admission.evaluate_projected_chain(_projected(), reader)
    assert result == admission.PredicateDecision(None, 12)
    if depth_selector == 0:
        assert admission.DEPTH_MODE_0_THRESHOLD_ADDRESS in reads
        assert admission.DEPTH_MODE_1_THRESHOLD_ADDRESS not in reads
    elif depth_selector == 1:
        assert admission.DEPTH_MODE_1_THRESHOLD_ADDRESS in reads
        assert admission.DEPTH_MODE_0_THRESHOLD_ADDRESS not in reads
    else:
        assert admission.DEPTH_MODE_0_THRESHOLD_ADDRESS not in reads
        assert admission.DEPTH_MODE_1_THRESHOLD_ADDRESS not in reads


def _exact_values() -> dict[int, int]:
    values = {
        admission.PAGE_CLASS_BASE + admission.EXACT_PAGE * 4: 3,
        admission.ROOT_POINTER_ADDRESS: 0x1000,
        0x1000 + admission.EXACT_PAGE * 4: 0x2000,
        admission.SCALE_ADDRESS: 2,
        admission.MAX_P_ADDRESS: 100,
        admission.MAX_Q_ADDRESS: 100,
        admission.DEPTH_SELECTOR_ADDRESS: 2,
        admission.DEPTH_MODE_0_THRESHOLD_ADDRESS: 0,
        admission.DEPTH_MODE_1_THRESHOLD_ADDRESS: 0,
    }
    for row in admission.ROW_COEFFICIENT_ADDRESSES:
        for address in row:
            values[address] = 0
    values[admission.ROW_COEFFICIENT_ADDRESSES[0][0]] = 4096
    values[admission.ROW_COEFFICIENT_ADDRESSES[1][1]] = 4096
    values[admission.ROW_COEFFICIENT_ADDRESSES[2][2]] = 4096
    for address in admission.ROW_OFFSET_ADDRESSES:
        values[address] = 0
    for address in admission.PROJECTION_OFFSET_ADDRESSES:
        values[address] = 0
    return values


def _evaluate(values: dict[int, int]) -> admission.AdmissionEvaluation:
    return admission.evaluate_exact_0a6c(
        ((0, 0, 0),) * 4,
        0x1001,
        values.__getitem__,
    )


def test_exact_evaluator_covers_early_rejects_and_full_pass() -> None:
    values = _exact_values()
    passed = _evaluate(values)
    assert passed.first_reject_pc is None
    assert passed.evaluated_predicate_count == 12
    assert passed.predicted_append is True

    page_reject = dict(values)
    page_reject[admission.PAGE_CLASS_BASE + admission.EXACT_PAGE * 4] = 2
    result = _evaluate(page_reject)
    assert result.first_reject_pc == 0x00405FFF
    assert result.evaluated_predicate_count == 1

    pointer_reject = dict(values)
    pointer_reject[0x1000 + admission.EXACT_PAGE * 4] = 0
    result = _evaluate(pointer_reject)
    assert result.first_reject_pc == 0x0040600F
    assert result.evaluated_predicate_count == 2


def test_native_wrap_truncation_and_failure_edges() -> None:
    assert admission.signed16(0x8000) == -32768
    assert admission.signed16(0x10001) == 1
    assert admission.signed32(0xFFFFFFFF) == -1
    assert admission.wrap32(0x80000000) == -(1 << 31)
    assert admission.trunc_div_signed32(-3, 2) == -1
    assert admission.trunc_div_signed32(3, -2) == -1
    assert admission._transform_row((-4095, 0, 0), (1, 0, 0), 0) == 0
    assert admission._transform_row((-4097, 0, 0), (1, 0, 0), 0) == -1
    assert admission._transform_row((0, 0, 0), (0, 0, 0), 0x8000) == -32768
    with pytest.raises(admission.AdmissionEvaluationError, match="failed closed"):
        admission.trunc_div_signed32(1, 0)
    with pytest.raises(admission.AdmissionEvaluationError, match="failed closed"):
        admission.trunc_div_signed32(-(1 << 31), -1)

    zero_divisor = _exact_values()
    zero_divisor[admission.SCALE_ADDRESS] = 0
    with pytest.raises(admission.AdmissionEvaluationError, match="failed closed"):
        _evaluate(zero_divisor)


def test_source_classification_fails_closed() -> None:
    values = _exact_values()
    with pytest.raises(
        admission.AdmissionEvaluationError,
        match="classification validation failed",
    ):
        admission.evaluate_exact_0a6c(
            ((0, 0, 0),) * 4, 0x0F01, values.__getitem__
        )
    with pytest.raises(
        admission.AdmissionEvaluationError,
        match="classification validation failed",
    ):
        admission.evaluate_exact_0a6c(
            ((0, 0, 0),) * 4, 0x9001, values.__getitem__
        )


def test_receipt_digest_coherence_mismatch_and_count_mismatch() -> None:
    values = _exact_values()
    evaluation = _evaluate(values)
    receipt = admission.reconcile_receipt(
        evaluation, True, values.__getitem__
    )
    assert receipt["prediction_matches_observation"] is True
    assert receipt["raw_inputs_retained"] is False
    assert receipt["payload_bytes_retained"] == 0

    count_mismatch = admission.reconcile_receipt(
        evaluation, False, values.__getitem__
    )
    assert count_mismatch["prediction_matches_observation"] is False

    changed = dict(values)
    changed[admission.SCALE_ADDRESS] = 3
    with pytest.raises(
        admission.AdmissionEvaluationError, match="digest changed"
    ):
        admission.reconcile_receipt(evaluation, True, changed.__getitem__)


def test_receipt_rejects_incoherent_evaluation_metadata() -> None:
    values = _exact_values()
    evaluation = _evaluate(values)
    forged = admission.AdmissionEvaluation(
        active_state_sha256=evaluation.active_state_sha256,
        evaluated_predicate_count=7,
        first_reject_pc=None,
        predicted_append=True,
        active_addresses=evaluation.active_addresses,
    )
    with pytest.raises(
        admission.AdmissionEvaluationError,
        match="metadata validation failed",
    ):
        admission.reconcile_receipt(forged, True, values.__getitem__)


def test_serialized_receipt_has_only_payload_free_schema_fields() -> None:
    values = _exact_values()
    evaluation = _evaluate(values)
    receipt = admission.reconcile_receipt(
        evaluation, True, values.__getitem__
    )
    assert set(receipt) == {
        "schema_version", "entry_index", "file_offset", "form",
        "page_16_validated", "caller_mode_2_validated",
        "active_state_sha256", "evaluated_predicate_count",
        "first_reject_pc", "predicted_append", "observed_append",
        "prediction_matches_observation", "raw_inputs_retained",
        "payload_bytes_retained",
    }
    serialized = json.dumps(receipt, sort_keys=True)
    for forbidden in (
        "source", "global", "projected", "vertex",
        "coefficient", "threshold", "0x1000", "0x2000",
    ):
        assert forbidden not in serialized.lower()
    assert {item.name for item in fields(admission.AdmissionEvaluation)} == {
        "active_state_sha256", "evaluated_predicate_count",
        "first_reject_pc", "predicted_append", "active_addresses",
    }
