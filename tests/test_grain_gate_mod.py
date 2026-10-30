from __future__ import annotations

import hashlib
import struct

import pytest

from reimplementation.ablpc.grain_gate_mod import (
    BUGS_EXE_SHA256,
    CITY_ENTRANCE_FORMULA_FILE_OFFSET,
    CITY_ENTRANCE_REQUIREMENTS_FILE_OFFSET,
    GrainGateModError,
    RETAIL_CITY_ENTRANCE_REQUIREMENTS,
    RETAIL_TUNNELS_REQUIREMENTS,
    TUNNELS_RECORD_SIZE,
    TUNNELS_REQUIREMENT_OFFSET,
    TUNNELS_TABLE_FILE_OFFSET,
    TUNNELS_TEMPLATE_FILE_OFFSET,
    _CITY_ENTRANCE_TABLE_FORMULA,
    _RETAIL_CITY_ENTRANCE_FORMULA,
    _RETAIL_CITY_ENTRANCE_REQUIREMENTS_GAP,
    _build_grain_gate_executable,
    build_grain_gate_executable,
)


def _fixture() -> bytes:
    size = TUNNELS_TEMPLATE_FILE_OFFSET + 9 * TUNNELS_RECORD_SIZE
    source = bytearray(b"\xa5" * size)
    source[
        CITY_ENTRANCE_FORMULA_FILE_OFFSET : CITY_ENTRANCE_FORMULA_FILE_OFFSET
        + len(_RETAIL_CITY_ENTRANCE_FORMULA)
    ] = _RETAIL_CITY_ENTRANCE_FORMULA
    source[
        CITY_ENTRANCE_REQUIREMENTS_FILE_OFFSET : CITY_ENTRANCE_REQUIREMENTS_FILE_OFFSET
        + len(_RETAIL_CITY_ENTRANCE_REQUIREMENTS_GAP)
    ] = _RETAIL_CITY_ENTRANCE_REQUIREMENTS_GAP
    for table_offset in (
        TUNNELS_TABLE_FILE_OFFSET,
        TUNNELS_TEMPLATE_FILE_OFFSET,
    ):
        for index, requirement in enumerate(RETAIL_TUNNELS_REQUIREMENTS):
            offset = (
                table_offset
                + index * TUNNELS_RECORD_SIZE
                + TUNNELS_REQUIREMENT_OFFSET
            )
            source[offset : offset + 4] = struct.pack("<I", requirement)
    return bytes(source)


def _build_fixture(
    *,
    tunnels: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 9),
    city: tuple[int, int, int] = (3, 17, 41),
) -> tuple[bytes, bytes, dict[str, object]]:
    source = _fixture()
    result, receipt = _build_grain_gate_executable(
        source,
        expected_source_sha256=hashlib.sha256(source).hexdigest(),
        tunnels_requirements=tunnels,
        city_entrance_requirements=city,
    )
    return source, result, receipt


def test_retail_layout_and_requirements_are_exact() -> None:
    assert BUGS_EXE_SHA256 == (
        "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
    )
    assert RETAIL_TUNNELS_REQUIREMENTS == (
        20,
        10,
        10,
        10,
        20,
        20,
        30,
        10,
        30,
    )
    assert RETAIL_CITY_ENTRANCE_REQUIREMENTS == (10, 20, 30)
    assert CITY_ENTRANCE_FORMULA_FILE_OFFSET == 0x32BD1
    assert CITY_ENTRANCE_REQUIREMENTS_FILE_OFFSET == 0x32CB0
    assert TUNNELS_TABLE_FILE_OFFSET == 0xD95C8
    assert TUNNELS_TEMPLATE_FILE_OFFSET == 0xD9680


def test_transform_preserves_unselected_bytes_and_proves_inverse() -> None:
    source, result, receipt = _build_fixture()
    selected = set()
    for change in receipt["changes"]:
        start = change["file_offset"]
        width = len(bytes.fromhex(change["expected_hex"]))
        selected.update(range(start, start + width))

    assert all(
        source[index] == result[index]
        for index in range(len(source))
        if index not in selected
    )
    assert receipt["inverse_matches_source"] is True
    assert receipt["tunnels_requirements"] == list(range(1, 10))
    assert receipt["city_entrance_requirements"] == [3, 17, 41]
    assert receipt["tunnels_linked_rows"] == [[0, 4]]
    assert receipt["tunnels_rows"][3] == {
        "row": 3,
        "field_04": 22,
        "x": 509676,
        "z": 510143,
        "requirement": 4,
    }


def test_city_formula_uses_independent_three_dword_table() -> None:
    _, result, _ = _build_fixture(city=(0, 11, 50))
    assert result[
        CITY_ENTRANCE_FORMULA_FILE_OFFSET : CITY_ENTRANCE_FORMULA_FILE_OFFSET
        + len(_CITY_ENTRANCE_TABLE_FORMULA)
    ] == _CITY_ENTRANCE_TABLE_FORMULA
    assert result[
        CITY_ENTRANCE_REQUIREMENTS_FILE_OFFSET : CITY_ENTRANCE_REQUIREMENTS_FILE_OFFSET
        + 12
    ] == struct.pack("<3I", 0, 11, 50)


def test_retail_city_table_is_differentially_equal_to_original_formula() -> None:
    for gate_index, requirement in enumerate(RETAIL_CITY_ENTRANCE_REQUIREMENTS):
        for grain_count in range(51):
            original_opens = grain_count >= (gate_index + 1) * 10
            replacement_opens = grain_count >= requirement
            assert replacement_opens is original_opens


def test_tunnels_requirements_are_independent_dwords_in_both_tables() -> None:
    tunnels = (50, 0, 49, 1, 48, 2, 47, 3, 46)
    _, result, _ = _build_fixture(tunnels=tunnels)
    for table_offset in (
        TUNNELS_TABLE_FILE_OFFSET,
        TUNNELS_TEMPLATE_FILE_OFFSET,
    ):
        observed = []
        for index in range(9):
            offset = (
                table_offset
                + index * TUNNELS_RECORD_SIZE
                + TUNNELS_REQUIREMENT_OFFSET
            )
            observed.append(struct.unpack_from("<I", result, offset)[0])
        assert observed == list(tunnels)


def test_tunnels_initializer_copy_preserves_configured_requirements() -> None:
    tunnels = (9, 8, 7, 6, 5, 4, 3, 2, 1)
    _, result, _ = _build_fixture(tunnels=tunnels)
    initialized = bytearray(result)
    table_width = 9 * TUNNELS_RECORD_SIZE
    initialized[
        TUNNELS_TABLE_FILE_OFFSET : TUNNELS_TABLE_FILE_OFFSET
        + table_width
    ] = initialized[
        TUNNELS_TEMPLATE_FILE_OFFSET : TUNNELS_TEMPLATE_FILE_OFFSET
        + table_width
    ]
    observed = []
    for index in range(9):
        offset = (
            TUNNELS_TABLE_FILE_OFFSET
            + index * TUNNELS_RECORD_SIZE
            + TUNNELS_REQUIREMENT_OFFSET
        )
        observed.append(struct.unpack_from("<I", initialized, offset)[0])
    assert observed == list(tunnels)


@pytest.mark.parametrize(
    ("tunnels", "city", "message"),
    [
        (tuple(range(8)), (1, 2, 3), "Tunnels requires exactly 9"),
        ((0, 1, 2, 3, 4, 5, 6, 7, 51), (1, 2, 3), "supported 0..50"),
        (tuple(range(9)), (1, 2), "City Entrance requires exactly 3"),
        (tuple(range(9)), (0, 1, -1), "supported 0..50"),
    ],
)
def test_invalid_requirements_fail_closed(
    tunnels: tuple[int, ...],
    city: tuple[int, ...],
    message: str,
) -> None:
    source = _fixture()
    with pytest.raises(GrainGateModError, match=message):
        _build_grain_gate_executable(
            source,
            expected_source_sha256=hashlib.sha256(source).hexdigest(),
            tunnels_requirements=tunnels,
            city_entrance_requirements=city,
        )


def test_exact_source_bytes_are_checked_after_hash() -> None:
    source = bytearray(_fixture())
    source[CITY_ENTRANCE_FORMULA_FILE_OFFSET] ^= 1
    changed = bytes(source)
    with pytest.raises(GrainGateModError, match="source bytes differ"):
        _build_grain_gate_executable(
            changed,
            expected_source_sha256=hashlib.sha256(changed).hexdigest(),
            tunnels_requirements=RETAIL_TUNNELS_REQUIREMENTS,
            city_entrance_requirements=RETAIL_CITY_ENTRANCE_REQUIREMENTS,
        )


def test_public_recipe_rejects_nonretail_asset_free_fixture() -> None:
    with pytest.raises(GrainGateModError, match="source SHA-256"):
        build_grain_gate_executable(_fixture())
