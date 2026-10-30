from __future__ import annotations

from collections import Counter
import hashlib
import struct

import pytest

from reimplementation.ablpc.level_dat import LevelDat
from reimplementation.ablpc.training_letter_mod import (
    DUPLICATE_FLIK_POSITIONS,
    TRAINING_51_GRAINS_DUPLICATE_FLIK_SHA256,
    TrainingLetterModError,
    build_training_duplicate_flik,
    transform_training_letter_records,
)


def _fixture() -> bytes:
    data = bytearray(336)
    struct.pack_into("<i", data, 0, 2)
    struct.pack_into("<hh", data, 4, 5, 0x3F)
    for index, selector in enumerate((0x10, 0x11, 0x12, 0x13, 0x14)):
        struct.pack_into(
            "<iiiBBBB",
            data,
            8 + index * 16,
            100 + index,
            -50,
            200 + index,
            selector,
            0xA0 + index,
            0xB0 + index,
            0xC0 + index,
        )
    struct.pack_into("<hh", data, 88, 1, 11)
    data[92:104] = bytes(range(12))
    struct.pack_into("<i", data, 104, 0)

    # Primary record, sentinel, one-entry index table, secondary record,
    # sentinel, then two payloads and their pointed-to target bytes.
    struct.pack_into("<iiiHHI", data, 108, 1, 2, 3, 4, 0x08, 196)
    struct.pack_into("<H", data, 142, 0xFFFF)
    struct.pack_into("<ii", data, 148, 0, 108)
    struct.pack_into("<iiiHHI", data, 156, 5, 6, 7, 8, 0, 232)
    struct.pack_into("<H", data, 190, 0xFFFF)
    struct.pack_into("<I", data, 196 + 0x1C, 288)
    struct.pack_into("<I", data, 232 + 0x14, 292)
    struct.pack_into("<i", data, len(data) - 4, -1)
    return bytes(data)


def _first_entries(data: bytes) -> list[bytes]:
    parsed = LevelDat.parse(data)
    selected = parsed.top_records[0]
    start = selected.offset + 4
    return [
        data[start + index * 16 : start + (index + 1) * 16]
        for index in range(selected.count)
    ]


def test_public_recipe_pins_output_identity_and_moved_duplicate_positions() -> None:
    assert TRAINING_51_GRAINS_DUPLICATE_FLIK_SHA256 == (
        "e9c75bb24ae0d0f4f74d17ea63431195e49b7e5278c089588d9372b8eb8cae7a"
    )
    assert DUPLICATE_FLIK_POSITIONS == {
        0x10: (4900, -50, 1500),
        0x11: (5100, -50, 1000),
        0x12: (5000, -50, 500),
        0x13: (4900, -50, 0),
    }


def test_letter_edit_moves_duplicates_removes_and_inverts() -> None:
    source = _fixture()
    result, receipt = transform_training_letter_records(
        source,
        expected_source_sha256=hashlib.sha256(source).hexdigest(),
        expected_count=5,
        move_positions={0x10: (1, 2, 3)},
        duplicate_positions={0x11: ((4, 5, 6),), 0x12: ((7, 8, 9),)},
        remove_selectors=(0x13,),
    )

    parsed = LevelDat.parse(result)
    entries = _first_entries(result)
    assert parsed.top_records[0].count == 6
    assert Counter(entry[0x0C] for entry in entries) == Counter(
        {0x10: 1, 0x11: 2, 0x12: 2, 0x14: 1}
    )
    assert struct.unpack_from("<iii", entries[0]) == (1, 2, 3)
    assert struct.unpack_from("<iii", entries[-2]) == (4, 5, 6)
    assert struct.unpack_from("<iii", entries[-1]) == (7, 8, 9)
    # All four non-coordinate bytes survive exact move/duplication.
    assert entries[0][0x0C:] == source[8 + 0x0C : 8 + 0x10]
    assert entries[-2][0x0C:] == source[24 + 0x0C : 24 + 0x10]
    assert receipt["table_size_delta"] == 16
    assert receipt["relocated_pointer_fields"] == 5
    assert receipt["inverse_matches_source"] is True


def test_letter_edit_can_remove_all_four_letters() -> None:
    source = _fixture()
    result, receipt = transform_training_letter_records(
        source,
        expected_source_sha256=hashlib.sha256(source).hexdigest(),
        expected_count=5,
        remove_selectors=(0x10, 0x11, 0x12, 0x13),
    )

    entries = _first_entries(result)
    assert len(entries) == 1
    assert entries[0][0x0C] == 0x14
    assert receipt["table_size_delta"] == -64
    assert receipt["inverse_matches_source"] is True


def test_letter_edit_rejects_ambiguous_or_invalid_operations() -> None:
    source = _fixture()
    source_hash = hashlib.sha256(source).hexdigest()
    with pytest.raises(TrainingLetterModError, match="move and remove"):
        transform_training_letter_records(
            source,
            expected_source_sha256=source_hash,
            expected_count=5,
            move_positions={0x10: (1, 2, 3)},
            remove_selectors=(0x10,),
        )
    with pytest.raises(TrainingLetterModError, match="unsupported"):
        transform_training_letter_records(
            source,
            expected_source_sha256=source_hash,
            expected_count=5,
            duplicate_positions={0x14: ((1, 2, 3),)},
        )
    with pytest.raises(TrainingLetterModError, match="signed 32-bit"):
        transform_training_letter_records(
            source,
            expected_source_sha256=source_hash,
            expected_count=5,
            move_positions={0x10: (1, 2)},
        )


def test_public_recipe_rejects_asset_free_fixture() -> None:
    with pytest.raises(TrainingLetterModError, match="source SHA-256"):
        build_training_duplicate_flik(_fixture())
