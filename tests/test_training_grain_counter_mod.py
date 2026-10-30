from __future__ import annotations

import hashlib

import pytest

from reimplementation.ablpc.training_grain_counter_mod import (
    BytePatch,
    TRAINING_51_COUNTER_EXE_SHA256,
    TRAINING_51_COUNTER_PATCHES,
    TrainingGrainCounterModError,
    _apply_exact_byte_patches,
    build_training_51_counter_executable,
)


def _fixture() -> bytes:
    return bytes(range(64))


def test_public_recipe_declares_only_the_three_accepted_tally_bytes() -> None:
    assert TRAINING_51_COUNTER_EXE_SHA256 == (
        "8ececefbe1e5747322bd635830f4125500c087d3769094b79545bd7a7b6a4456"
    )
    assert [
        (
            patch.file_offset,
            patch.virtual_address,
            patch.expected,
            patch.replacement,
        )
        for patch in TRAINING_51_COUNTER_PATCHES
    ] == [
        (0x422CB, 0x00442ECB, b"\x32", b"\x33"),
        (0x422CF, 0x00442ECF, b"\x32", b"\x33"),
        (0x42327, 0x00442F27, b"\x75", b"\x72"),
    ]


def test_exact_byte_patches_preserve_unknown_bytes_and_invert() -> None:
    source = _fixture()
    expected = bytearray(source)
    expected[7] = 0xA7
    expected[31:33] = b"\xB1\xB2"
    result, receipt = _apply_exact_byte_patches(
        source,
        expected_source_sha256=hashlib.sha256(source).hexdigest(),
        expected_output_sha256=hashlib.sha256(expected).hexdigest(),
        patches=(
            BytePatch(7, 0x00401007, b"\x07", b"\xA7", "fixture one"),
            BytePatch(31, 0x0040101F, b"\x1F\x20", b"\xB1\xB2", "fixture two"),
        ),
    )

    assert result == bytes(expected)
    assert receipt["changed_byte_count"] == 3
    assert receipt["inverse_matches_source"] is True
    assert [change["file_offset"] for change in receipt["changes"]] == [7, 31]


def test_exact_byte_patches_reject_wrong_source_hash() -> None:
    source = _fixture()
    with pytest.raises(TrainingGrainCounterModError, match="source SHA-256"):
        _apply_exact_byte_patches(
            source,
            expected_source_sha256="0" * 64,
            expected_output_sha256="0" * 64,
            patches=(BytePatch(0, 0x00401000, b"\x00", b"\x01", "fixture"),),
        )


def test_exact_byte_patches_reject_overlap() -> None:
    source = _fixture()
    with pytest.raises(TrainingGrainCounterModError, match="overlap"):
        _apply_exact_byte_patches(
            source,
            expected_source_sha256=hashlib.sha256(source).hexdigest(),
            expected_output_sha256="0" * 64,
            patches=(
                BytePatch(2, 0x00401002, b"\x02\x03", b"\xA2\xA3", "one"),
                BytePatch(3, 0x00401003, b"\x03", b"\xB3", "two"),
            ),
        )


def test_public_recipe_rejects_nonretail_asset_free_fixture() -> None:
    with pytest.raises(TrainingGrainCounterModError, match="source SHA-256"):
        build_training_51_counter_executable(_fixture())
