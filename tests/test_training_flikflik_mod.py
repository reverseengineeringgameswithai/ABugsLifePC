from __future__ import annotations

import hashlib

import pytest

from reimplementation.ablpc.training_flikflik_mod import (
    CODE_CAVE_VIRTUAL_ADDRESS,
    COMPLETION_TRANSITION_FLAG_ADDRESS,
    ExecutablePatch,
    FLIKFLIK_CODE,
    FLIKFLIK_CODE_SHA256,
    POPCOUNT_TABLE_VIRTUAL_ADDRESS,
    TRAINING_FLIKFLIK_EXE_SHA256,
    TRAINING_FLIKFLIK_PATCHES,
    TrainingFlikflikModError,
    _apply_exact_patches,
    build_training_flikflik_executable,
)


def _fixture() -> bytes:
    return bytes(range(64))


def test_public_recipe_pins_code_output_and_complete_popcount_table() -> None:
    assert TRAINING_FLIKFLIK_EXE_SHA256 == (
        "b572e6d19bc417969c159ba0df7521cbb01b675c260a4dc98d2e6b34475947f4"
    )
    assert len(FLIKFLIK_CODE) == 576
    assert hashlib.sha256(FLIKFLIK_CODE).hexdigest() == FLIKFLIK_CODE_SHA256
    assert FLIKFLIK_CODE[-256:] == bytes(value.bit_count() for value in range(256))
    assert FLIKFLIK_CODE[-1] == 8


def test_public_recipe_has_exact_redirects_and_only_one_code_cave_claim() -> None:
    by_address = {patch.virtual_address: patch for patch in TRAINING_FLIKFLIK_PATCHES}
    assert len(TRAINING_FLIKFLIK_PATCHES) == 29
    assert by_address[0x00416DF9].replacement.hex() == "e8024c0a00e9b8000000"
    assert by_address[0x004430BD].replacement.hex() == "e8a2890700e9f5000000"
    assert [by_address[address].replacement.hex() for address in (
        0x00417A65,
        0x00417ABF,
        0x00417B47,
        0x00417BCF,
    )] == [
        "e862400a009090",
        "e80d400a009090",
        "e88a3f0a009090",
        "e8073f0a009090",
    ]
    cave = by_address[CODE_CAVE_VIRTUAL_ADDRESS]
    assert cave.expected == b"\xCC" * 576
    assert cave.replacement == FLIKFLIK_CODE


def test_all_tally_count_consumers_use_the_complete_table() -> None:
    replacement = POPCOUNT_TABLE_VIRTUAL_ADDRESS.to_bytes(4, "little")
    by_address = {patch.virtual_address: patch for patch in TRAINING_FLIKFLIK_PATCHES}
    for address in (0x00443473, 0x004434CD, 0x004435A3, 0x004435E5):
        assert by_address[address].replacement == replacement
    assert by_address[0x004431E3].replacement == b"\x08"
    assert by_address[0x00443328].replacement == b"\x08"
    for address in (0x00443331, 0x0044334E, 0x00443372):
        assert by_address[address].replacement == b"\x6a\x00\x90\x90\x90"


def test_pickup_completion_uses_one_shot_transition_scratch() -> None:
    by_address = {patch.virtual_address: patch for patch in TRAINING_FLIKFLIK_PATCHES}
    expected = (0x0059D9B2).to_bytes(4, "little") + b"\x0f"
    replacement = COMPLETION_TRANSITION_FLAG_ADDRESS.to_bytes(4, "little") + b"\x01"
    for address in (0x00417AA3, 0x00417AFD, 0x00417B85, 0x00417C0D):
        assert by_address[address].expected == expected
        assert by_address[address].replacement == replacement


def test_authored_code_uses_no_new_absolute_global_operands() -> None:
    assert bytes.fromhex("b2d95900") not in FLIKFLIK_CODE
    assert bytes.fromhex("5c595c00") not in FLIKFLIK_CODE


def test_exact_patch_engine_preserves_unknown_bytes_and_inverts() -> None:
    source = _fixture()
    expected = bytearray(source)
    expected[7] = 0xA7
    expected[31:33] = b"\xB1\xB2"
    result, receipt = _apply_exact_patches(
        source,
        expected_source_sha256=hashlib.sha256(source).hexdigest(),
        expected_output_sha256=hashlib.sha256(expected).hexdigest(),
        patches=(
            ExecutablePatch(7, 0x00401007, b"\x07", b"\xA7", "fixture one"),
            ExecutablePatch(
                31, 0x0040101F, b"\x1F\x20", b"\xB1\xB2", "fixture two"
            ),
        ),
    )
    assert result == bytes(expected)
    assert receipt["patch_count"] == 2
    assert receipt["patched_span_byte_count"] == 3
    assert receipt["changed_byte_count"] == 3
    assert receipt["inverse_matches_source"] is True


def test_exact_patch_engine_rejects_wrong_source_overlap_and_wrong_bytes() -> None:
    source = _fixture()
    with pytest.raises(TrainingFlikflikModError, match="source SHA-256"):
        _apply_exact_patches(
            source,
            expected_source_sha256="0" * 64,
            expected_output_sha256="0" * 64,
            patches=(ExecutablePatch(0, 0x00401000, b"\x00", b"\x01", "x"),),
        )
    with pytest.raises(TrainingFlikflikModError, match="overlap"):
        _apply_exact_patches(
            source,
            expected_source_sha256=hashlib.sha256(source).hexdigest(),
            expected_output_sha256="0" * 64,
            patches=(
                ExecutablePatch(2, 0x00401002, b"\x02\x03", b"\xA2\xA3", "x"),
                ExecutablePatch(3, 0x00401003, b"\x03", b"\xB3", "y"),
            ),
        )
    with pytest.raises(TrainingFlikflikModError, match="source bytes differ"):
        _apply_exact_patches(
            source,
            expected_source_sha256=hashlib.sha256(source).hexdigest(),
            expected_output_sha256="0" * 64,
            patches=(ExecutablePatch(4, 0x00401004, b"\xFF", b"\x00", "x"),),
        )


def test_public_composed_recipe_rejects_asset_free_fixture() -> None:
    with pytest.raises(TrainingFlikflikModError, match="retail bugs.exe"):
        build_training_flikflik_executable(_fixture())
