from __future__ import annotations

import hashlib
import struct

import pytest

from ablpc.level03_type1_row_mod import (
    Level03Type1RowModError,
    _edit_exact_type1_row,
    build_level03_type1_row6_x_plus_128,
)
from ablpc.level_dat import LevelDat


def _synthetic_level_dat() -> bytes:
    data = bytearray(120)
    struct.pack_into("<i", data, 0, 2)

    struct.pack_into("<hh", data, 4, 2, 0x3F)
    struct.pack_into("<hh", data, 40, 2, 1)
    struct.pack_into("<iii", data, 44, 10, 0, 20)
    struct.pack_into("<iii", data, 56, 30, 0, 40)

    struct.pack_into("<i", data, 68, 0)
    struct.pack_into("<h", data, 72 + 0x0E, -1)
    struct.pack_into("<i", data, 92, -1)
    struct.pack_into("<h", data, 96 + 0x0E, -1)
    struct.pack_into("<i", data, 116, -1)
    return bytes(data)


def test_synthetic_exact_row_edit_is_local_and_reversible() -> None:
    source = _synthetic_level_dat()
    result = _edit_exact_type1_row(
        source,
        expected_source_sha256=hashlib.sha256(source).hexdigest(),
        expected_table_index=1,
        expected_table_offset=40,
        expected_count=2,
        row_index=1,
        expected_position=(30, 0, 40),
        output_position=(158, 0, 40),
    )

    LevelDat.parse(result.output_bytes)
    assert struct.unpack_from("<iii", result.output_bytes, 56) == (158, 0, 40)
    assert result.output_bytes[:56] == source[:56]
    assert result.output_bytes[68:] == source[68:]
    assert result.receipt["inverse_verified"] is True
    assert all(56 <= offset < 68 for offset in result.receipt["changed_offsets"])


def test_synthetic_edit_rejects_wrong_hash() -> None:
    source = _synthetic_level_dat()
    with pytest.raises(Level03Type1RowModError, match="SHA-256 mismatch"):
        _edit_exact_type1_row(
            source,
            expected_source_sha256="0" * 64,
            expected_table_index=1,
            expected_table_offset=40,
            expected_count=2,
            row_index=1,
            expected_position=(30, 0, 40),
            output_position=(158, 0, 40),
        )


def test_synthetic_edit_rejects_wrong_old_position() -> None:
    source = _synthetic_level_dat()
    with pytest.raises(Level03Type1RowModError, match="row value mismatch"):
        _edit_exact_type1_row(
            source,
            expected_source_sha256=hashlib.sha256(source).hexdigest(),
            expected_table_index=1,
            expected_table_offset=40,
            expected_count=2,
            row_index=1,
            expected_position=(31, 0, 40),
            output_position=(158, 0, 40),
        )


def test_public_recipe_rejects_synthetic_fixture() -> None:
    with pytest.raises(Level03Type1RowModError, match="SHA-256 mismatch"):
        build_level03_type1_row6_x_plus_128(_synthetic_level_dat())
