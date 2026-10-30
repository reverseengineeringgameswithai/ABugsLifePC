from __future__ import annotations

import hashlib
import struct

import pytest

from reimplementation.ablpc.level_dat import LevelDat
from reimplementation.ablpc.training_grain_mod import (
    TrainingGrainModError,
    _insert_type_3f_entry,
    build_training_51_grains,
)


def _fixture() -> bytes:
    data = bytearray(272)
    struct.pack_into("<i", data, 0, 2)
    struct.pack_into("<hh", data, 4, 2, 0x3F)
    data[8:40] = bytes(range(32))
    struct.pack_into("<hh", data, 40, 1, 11)
    data[44:56] = bytes(range(12))
    struct.pack_into("<i", data, 56, 0)

    # Primary record, sentinel, one-entry index table, secondary record,
    # sentinel, then two payloads and their pointed-to target bytes.
    struct.pack_into("<iiiHHI", data, 60, 1, 2, 3, 4, 0x08, 148)
    struct.pack_into("<H", data, 94, 0xFFFF)
    struct.pack_into("<ii", data, 100, 0, 60)
    struct.pack_into("<iiiHHI", data, 108, 5, 6, 7, 8, 0, 184)
    struct.pack_into("<H", data, 142, 0xFFFF)
    struct.pack_into("<I", data, 148 + 0x1C, 240)
    struct.pack_into("<I", data, 184 + 0x14, 244)
    struct.pack_into("<i", data, len(data) - 4, -1)
    return bytes(data)


def test_insert_type_3f_entry_relocates_and_preserves_unknown_bytes() -> None:
    source = _fixture()
    result, receipt = _insert_type_3f_entry(
        source,
        expected_source_sha256=hashlib.sha256(source).hexdigest(),
        expected_count=2,
        position=(100, -200, 300),
        selector=0x14,
    )

    parsed = LevelDat.parse(result)
    assert len(result) == len(source) + 16
    assert parsed.top_records[0].count == 3
    assert parsed.top_records[1].offset == 56
    assert parsed.primary_records_offset == 76
    assert parsed.primary_records[0].payload_offset_candidate == 164
    assert parsed.index_table_values == (76,)
    assert parsed.secondary_records[0].payload_offset_candidate == 200
    assert struct.unpack_from("<I", result, 164 + 0x1C)[0] == 256
    assert struct.unpack_from("<I", result, 200 + 0x14)[0] == 260
    assert struct.unpack_from("<iiiI", result, 40) == (100, -200, 300, 0x14)
    assert receipt["relocated_pointer_fields"] == 5
    assert receipt["inverse_matches_source"] is True


def test_insert_type_3f_entry_rejects_wrong_hash() -> None:
    source = _fixture()
    with pytest.raises(TrainingGrainModError, match="SHA-256"):
        _insert_type_3f_entry(
            source,
            expected_source_sha256="0" * 64,
            expected_count=2,
            position=(0, 0, 0),
            selector=0x14,
        )


def test_public_recipe_rejects_non_training_asset_free_fixture() -> None:
    with pytest.raises(TrainingGrainModError, match="SHA-256"):
        build_training_51_grains(_fixture())
