"""Exact, asset-free recipe for the validated TRAINING 51-grain experiment."""

from __future__ import annotations

from collections import Counter
import hashlib
import struct
from typing import Any

from .level_dat import LevelDat


TRAINING_LEVEL1_SHA256 = (
    "494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22"
)
TRAINING_51_GRAINS_SHA256 = (
    "20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40"
)
TRAINING_GRAIN_POSITION = (4950, -1301, 1127)
TYPE_3F = 0x3F
GRAIN_SELECTOR = 0x14
ENTRY_SIZE = 16
_EXPECTED_SELECTOR_COUNTS = {
    0x10: 1,
    0x11: 1,
    0x12: 1,
    0x13: 1,
    0x14: 50,
    0x23: 2,
    0x2B: 2,
    0x2C: 4,
}


class TrainingGrainModError(ValueError):
    """Raised when the exact TRAINING recipe cannot be applied safely."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _shifted(offset: int, insertion_offset: int) -> int:
    return offset + ENTRY_SIZE if offset >= insertion_offset else offset


def _u32(data: bytes, offset: int, label: str) -> int:
    if offset < 0 or offset + 4 > len(data):
        raise TrainingGrainModError(f"{label} is outside the source file")
    return struct.unpack_from("<I", data, offset)[0]


def _insert_type_3f_entry(
    source: bytes,
    *,
    expected_source_sha256: str,
    expected_count: int,
    position: tuple[int, int, int],
    selector: int,
) -> tuple[bytes, dict[str, Any]]:
    """Insert one first-table entry and relocate the PC loader's known offsets.

    This helper remains exact-hash and exact-layout locked. It is separated
    from the public TRAINING recipe only so its byte-preservation behavior can
    be exercised with asset-free synthetic fixtures.
    """

    source_sha256 = _sha256(source)
    if source_sha256 != expected_source_sha256:
        raise TrainingGrainModError("source SHA-256 does not match the recipe")
    if len(position) != 3 or any(
        not -(1 << 31) <= value < (1 << 31) for value in position
    ):
        raise TrainingGrainModError("position components must be signed 32-bit values")
    if not 0 <= selector <= 0xFF:
        raise TrainingGrainModError("selector must fit in one byte")

    try:
        parsed = LevelDat.parse(source)
    except ValueError as error:
        raise TrainingGrainModError(str(error)) from error
    if not parsed.top_records:
        raise TrainingGrainModError("LEVEL DAT has no top record")
    selected = parsed.top_records[0]
    if (
        selected.offset != 4
        or selected.type_id != TYPE_3F
        or selected.count != expected_count
        or selected.size != 4 + expected_count * ENTRY_SIZE
    ):
        raise TrainingGrainModError("first type-0x3F table does not match the recipe")

    insertion_offset = selected.offset + selected.size
    entry = struct.pack("<iiiI", *position, selector)
    output = bytearray(source[:insertion_offset] + entry + source[insertion_offset:])
    struct.pack_into("<h", output, selected.offset, expected_count + 1)

    pointer_fields: dict[int, tuple[int, int]] = {}

    def record_pointer(field_offset: int, value: int, label: str) -> None:
        if value > len(source) - 4:
            raise TrainingGrainModError(f"{label} target is outside the source file")
        new_value = _shifted(value, insertion_offset)
        prior = pointer_fields.setdefault(field_offset, (value, new_value))
        if prior != (value, new_value):
            raise TrainingGrainModError(
                f"contradictory pointer claim at source offset 0x{field_offset:x}"
            )

    for section in ("primary", "secondary"):
        for record in parsed.records(section):
            payload_offset = record.payload_offset_candidate
            record_pointer(
                record.offset + 0x10,
                payload_offset,
                f"{section} record {record.index} payload",
            )
            target_delta = 0x1C if record.flags & 0x08 else 0x14
            target_field = payload_offset + target_delta
            target_value = _u32(
                source,
                target_field,
                f"{section} record {record.index} target field",
            )
            record_pointer(
                target_field,
                target_value,
                f"{section} record {record.index} target",
            )
            if record.flags & 0x20:
                extra_delta = 0x20 if record.flags & 0x08 else 0x18
                extra_field = payload_offset + extra_delta
                extra_value = _u32(
                    source,
                    extra_field,
                    f"{section} record {record.index} extra field",
                )
                record_pointer(
                    extra_field,
                    extra_value,
                    f"{section} record {record.index} extra target",
                )

    for index, value in enumerate(parsed.index_table_values):
        if value < 0:
            raise TrainingGrainModError(f"index-table entry {index} is negative")
        if value != 0:
            record_pointer(
                parsed.index_table_offset + 4 + index * 4,
                value,
                f"index-table entry {index}",
            )

    for old_field_offset, (old_value, new_value) in pointer_fields.items():
        new_field_offset = _shifted(old_field_offset, insertion_offset)
        observed = _u32(output, new_field_offset, "relocated pointer field")
        if observed != old_value:
            raise TrainingGrainModError(
                f"pointer source mismatch at 0x{old_field_offset:x}: "
                f"expected 0x{old_value:x}, found 0x{observed:x}"
            )
        struct.pack_into("<I", output, new_field_offset, new_value)

    result = bytes(output)
    try:
        reparsed = LevelDat.parse(result)
    except ValueError as error:
        raise TrainingGrainModError(str(error)) from error
    if reparsed.top_records[0].count != expected_count + 1:
        raise TrainingGrainModError("inserted table count did not reparse")
    if len(reparsed.primary_records) != len(parsed.primary_records):
        raise TrainingGrainModError("primary record count changed")
    if len(reparsed.secondary_records) != len(parsed.secondary_records):
        raise TrainingGrainModError("secondary record count changed")
    if reparsed.final_dword != parsed.final_dword:
        raise TrainingGrainModError("final dword changed")

    inverse = bytearray(result)
    for old_field_offset, (old_value, _new_value) in pointer_fields.items():
        struct.pack_into(
            "<I", inverse, _shifted(old_field_offset, insertion_offset), old_value
        )
    struct.pack_into("<h", inverse, selected.offset, expected_count)
    del inverse[insertion_offset : insertion_offset + ENTRY_SIZE]
    if bytes(inverse) != source:
        raise TrainingGrainModError("exact inverse reconstruction failed")

    return result, {
        "source_sha256": source_sha256,
        "output_sha256": _sha256(result),
        "source_size": len(source),
        "output_size": len(result),
        "table_offset": selected.offset,
        "insertion_offset": insertion_offset,
        "source_table_count": expected_count,
        "output_table_count": expected_count + 1,
        "new_entry_index": expected_count,
        "new_entry_position": list(position),
        "new_entry_selector": selector,
        "relocated_pointer_fields": len(pointer_fields),
        "inverse_matches_source": True,
    }


def build_training_51_grains(source: bytes) -> tuple[bytes, dict[str, Any]]:
    """Build the one validated TRAINING mod from the exact retail PC DAT."""

    if _sha256(source) != TRAINING_LEVEL1_SHA256:
        raise TrainingGrainModError("source SHA-256 does not match the recipe")
    parsed = LevelDat.parse(source)
    if not parsed.top_records:
        raise TrainingGrainModError("LEVEL DAT has no top record")
    selected = parsed.top_records[0]
    if selected.offset + selected.size > len(source):
        raise TrainingGrainModError("type-0x3F table is truncated")
    selector_counts = Counter(
        source[selected.offset + 4 + index * ENTRY_SIZE + 0x0C]
        for index in range(selected.count)
    )
    if dict(selector_counts) != _EXPECTED_SELECTOR_COUNTS:
        raise TrainingGrainModError("TRAINING selector census does not match the recipe")

    result, receipt = _insert_type_3f_entry(
        source,
        expected_source_sha256=TRAINING_LEVEL1_SHA256,
        expected_count=62,
        position=TRAINING_GRAIN_POSITION,
        selector=GRAIN_SELECTOR,
    )
    if receipt["relocated_pointer_fields"] != 556:
        raise TrainingGrainModError("TRAINING relocation census changed")
    if receipt["output_sha256"] != TRAINING_51_GRAINS_SHA256:
        raise TrainingGrainModError("TRAINING output identity changed")

    result_parsed = LevelDat.parse(result)
    result_selected = result_parsed.top_records[0]
    grain_count = sum(
        result[result_selected.offset + 4 + index * ENTRY_SIZE + 0x0C]
        == GRAIN_SELECTOR
        for index in range(result_selected.count)
    )
    if grain_count != 51:
        raise TrainingGrainModError("output does not contain exactly 51 grain selectors")
    receipt["grain_selector_count"] = grain_count
    return result, receipt
