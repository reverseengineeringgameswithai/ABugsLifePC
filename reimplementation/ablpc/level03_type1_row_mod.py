"""Exact Level03 type-1 coordinate-row discriminator.

This module intentionally exposes one hash-locked experiment recipe rather
than a general type-1 editor. Type 1 has multiple PC consumers and is not
named as a checkpoint table.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import struct

from .level_dat import LevelDat


LEVEL03_DAT_SHA256 = (
    "bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b"
)
LEVEL03_OUTPUT_SHA256 = (
    "4894b6159e5a36a37fb9a3f50243cdd816fa4e7f28e169bcadf45b48792d4c12"
)
TYPE_ID = 1
TABLE_INDEX = 1
TABLE_OFFSET = 0x458
TABLE_COUNT = 18
ROW_INDEX = 6
ROW_OFFSET = 0x4A4
SOURCE_POSITION = (15678, 0, 15438)
OUTPUT_POSITION = (15806, 0, 15438)


class Level03Type1RowModError(ValueError):
    """Raised when the exact experiment recipe cannot be applied safely."""


@dataclass(frozen=True)
class Level03Type1RowModResult:
    output_bytes: bytes
    receipt: dict[str, object]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _require_s32_triplet(name: str, value: tuple[int, int, int]) -> None:
    if len(value) != 3:
        raise Level03Type1RowModError(f"{name} must contain exactly three values")
    for component in value:
        if not isinstance(component, int) or isinstance(component, bool):
            raise Level03Type1RowModError(f"{name} components must be integers")
        if component < -(1 << 31) or component > (1 << 31) - 1:
            raise Level03Type1RowModError(f"{name} component is outside signed 32-bit range")


def _walk_nonnegative_top_records(source: bytes) -> list[tuple[int, int, int, int]]:
    if len(source) < 4:
        raise Level03Type1RowModError("source is too short for a top-record count")
    (top_count,) = struct.unpack_from("<i", source, 0)
    if top_count < 0 or top_count > 64:
        raise Level03Type1RowModError("impossible top-record count")

    records: list[tuple[int, int, int, int]] = []
    cursor = 4
    for _ in range(top_count):
        if cursor + 4 > len(source):
            raise Level03Type1RowModError("truncated top-record header")
        count, type_id = struct.unpack_from("<hh", source, cursor)
        if count < 0 or type_id < 0:
            raise Level03Type1RowModError(
                "this exact recipe does not support negative top-record layouts"
            )
        stride = 16 if type_id == 0x3F else 12
        size = 4 + count * stride
        if cursor + size > len(source):
            raise Level03Type1RowModError("top record extends beyond the source")
        records.append((cursor, count, type_id, size))
        cursor += size
    return records


def _edit_exact_type1_row(
    source: bytes,
    *,
    expected_source_sha256: str,
    expected_table_index: int,
    expected_table_offset: int,
    expected_count: int,
    row_index: int,
    expected_position: tuple[int, int, int],
    output_position: tuple[int, int, int],
) -> Level03Type1RowModResult:
    """Apply one exact row edit with full-file and inverse guards."""

    source_sha256 = _sha256(source)
    if source_sha256 != expected_source_sha256:
        raise Level03Type1RowModError(
            f"source SHA-256 mismatch: expected {expected_source_sha256}, got {source_sha256}"
        )
    _require_s32_triplet("expected_position", expected_position)
    _require_s32_triplet("output_position", output_position)

    # The repository parser supplies the complete bounds-checked layout gate.
    LevelDat.parse(source)
    records = _walk_nonnegative_top_records(source)
    if expected_table_index < 0 or expected_table_index >= len(records):
        raise Level03Type1RowModError("expected table index is outside the top-record table")
    table_offset, count, type_id, size = records[expected_table_index]
    if table_offset != expected_table_offset:
        raise Level03Type1RowModError(
            f"type-1 table offset mismatch: expected {expected_table_offset:#x}, "
            f"got {table_offset:#x}"
        )
    if type_id != TYPE_ID or count != expected_count or size != 4 + count * 12:
        raise Level03Type1RowModError("type-1 table identity/count/size mismatch")
    if row_index < 0 or row_index >= count:
        raise Level03Type1RowModError("row index is outside the exact type-1 table")

    row_offset = table_offset + 4 + row_index * 12
    old_position = struct.unpack_from("<iii", source, row_offset)
    if old_position != expected_position:
        raise Level03Type1RowModError(
            f"row value mismatch: expected {expected_position}, got {old_position}"
        )

    output = bytearray(source)
    struct.pack_into("<iii", output, row_offset, *output_position)
    output_bytes = bytes(output)
    if len(output_bytes) != len(source):
        raise Level03Type1RowModError("row edit changed file size")
    LevelDat.parse(output_bytes)

    changed_offsets = [
        offset
        for offset, (before, after) in enumerate(zip(source, output_bytes, strict=True))
        if before != after
    ]
    row_range = range(row_offset, row_offset + 12)
    if any(offset not in row_range for offset in changed_offsets):
        raise Level03Type1RowModError("row edit changed a byte outside the selected row")

    inverse = bytearray(output_bytes)
    inverse_position = struct.unpack_from("<iii", inverse, row_offset)
    if inverse_position != output_position:
        raise Level03Type1RowModError("inverse guard did not observe the requested row")
    struct.pack_into("<iii", inverse, row_offset, *expected_position)
    if bytes(inverse) != source:
        raise Level03Type1RowModError("inverse did not reconstruct the source byte-for-byte")

    return Level03Type1RowModResult(
        output_bytes=output_bytes,
        receipt={
            "recipe": "exact-type1-coordinate-row",
            "source_sha256": source_sha256,
            "output_sha256": _sha256(output_bytes),
            "size": len(source),
            "table_index": expected_table_index,
            "table_offset": table_offset,
            "type_id": type_id,
            "table_count": count,
            "row_index": row_index,
            "row_offset": row_offset,
            "source_position": list(expected_position),
            "output_position": list(output_position),
            "changed_offsets": changed_offsets,
            "inverse_verified": True,
        },
    )


def build_level03_type1_row6_x_plus_128(source: bytes) -> Level03Type1RowModResult:
    """Build the exact Level03 row-6 X+128 PC discriminator."""

    result = _edit_exact_type1_row(
        source,
        expected_source_sha256=LEVEL03_DAT_SHA256,
        expected_table_index=TABLE_INDEX,
        expected_table_offset=TABLE_OFFSET,
        expected_count=TABLE_COUNT,
        row_index=ROW_INDEX,
        expected_position=SOURCE_POSITION,
        output_position=OUTPUT_POSITION,
    )
    output_sha256 = _sha256(result.output_bytes)
    if output_sha256 != LEVEL03_OUTPUT_SHA256:
        raise Level03Type1RowModError(
            f"output SHA-256 mismatch: expected {LEVEL03_OUTPUT_SHA256}, got {output_sha256}"
        )
    if result.receipt["changed_offsets"] != [ROW_OFFSET]:
        raise Level03Type1RowModError("exact recipe must change only byte 0x4A4")

    receipt = dict(result.receipt)
    receipt.update(
        {
            "recipe": "level03-type1-row6-x-plus-128",
            "predicted_runtime_x_delta_if_selected": 4096,
            "prediction_basis": "PC 0x00432930 stores authored X shifted left by 5",
        }
    )
    return Level03Type1RowModResult(result.output_bytes, receipt)
