"""Exact, asset-free TRAINING FLIK-letter record transformations."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import struct
from typing import Any, Iterable, Mapping, Sequence

from .level_dat import LevelDat


TRAINING_51_GRAINS_SHA256 = (
    "20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40"
)
TRAINING_51_GRAINS_DUPLICATE_FLIK_SHA256 = (
    "e9c75bb24ae0d0f4f74d17ea63431195e49b7e5278c089588d9372b8eb8cae7a"
)
TYPE_3F = 0x3F
ENTRY_SIZE = 16
LETTER_SELECTORS = (0x10, 0x11, 0x12, 0x13)
DUPLICATE_FLIK_POSITIONS = {
    0x10: (4900, -50, 1500),
    0x11: (5100, -50, 1000),
    0x12: (5000, -50, 500),
    0x13: (4900, -50, 0),
}
_EXPECTED_SOURCE_SELECTOR_COUNTS = {
    0x10: 1,
    0x11: 1,
    0x12: 1,
    0x13: 1,
    0x14: 51,
    0x23: 2,
    0x2B: 2,
    0x2C: 4,
}


class TrainingLetterModError(ValueError):
    """Raised when an exact TRAINING letter transformation is unsafe."""


@dataclass(frozen=True)
class _PointerClaim:
    field_offset: int
    old_value: int
    new_value: int


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _u32(data: bytes, offset: int, label: str) -> int:
    if offset < 0 or offset + 4 > len(data):
        raise TrainingLetterModError(f"{label} is outside the source file")
    return struct.unpack_from("<I", data, offset)[0]


def _shifted(offset: int, boundary: int, delta: int) -> int:
    return offset + delta if offset >= boundary else offset


def _position(value: Sequence[int], label: str) -> tuple[int, int, int]:
    if len(value) != 3 or any(
        not isinstance(component, int)
        or not -(1 << 31) <= component < (1 << 31)
        for component in value
    ):
        raise TrainingLetterModError(
            f"{label} must contain three signed 32-bit integers"
        )
    return value[0], value[1], value[2]


def _selector(entry: bytes) -> int:
    return entry[0x0C]


def _with_position(entry: bytes, position: tuple[int, int, int]) -> bytes:
    result = bytearray(entry)
    struct.pack_into("<iii", result, 0, *position)
    return bytes(result)


def _pointer_claims(
    source: bytes,
    parsed: LevelDat,
    *,
    old_table_end: int,
    delta: int,
) -> tuple[_PointerClaim, ...]:
    claims: dict[int, _PointerClaim] = {}

    def record(field_offset: int, value: int, label: str) -> None:
        if value > len(source) - 4:
            raise TrainingLetterModError(f"{label} target is outside the source file")
        claim = _PointerClaim(
            field_offset=field_offset,
            old_value=value,
            new_value=_shifted(value, old_table_end, delta),
        )
        prior = claims.setdefault(field_offset, claim)
        if prior != claim:
            raise TrainingLetterModError(
                f"contradictory pointer claim at source offset 0x{field_offset:x}"
            )

    for section in ("primary", "secondary"):
        for record_entry in parsed.records(section):
            payload_offset = record_entry.payload_offset_candidate
            record(
                record_entry.offset + 0x10,
                payload_offset,
                f"{section} record {record_entry.index} payload",
            )
            target_delta = 0x1C if record_entry.flags & 0x08 else 0x14
            target_field = payload_offset + target_delta
            record(
                target_field,
                _u32(
                    source,
                    target_field,
                    f"{section} record {record_entry.index} target field",
                ),
                f"{section} record {record_entry.index} target",
            )
            if record_entry.flags & 0x20:
                extra_delta = 0x20 if record_entry.flags & 0x08 else 0x18
                extra_field = payload_offset + extra_delta
                record(
                    extra_field,
                    _u32(
                        source,
                        extra_field,
                        f"{section} record {record_entry.index} extra field",
                    ),
                    f"{section} record {record_entry.index} extra target",
                )

    for index, value in enumerate(parsed.index_table_values):
        if value < 0:
            raise TrainingLetterModError(f"index-table entry {index} is negative")
        if value:
            record(
                parsed.index_table_offset + 4 + index * 4,
                value,
                f"index-table entry {index}",
            )
    return tuple(claims.values())


def _rewrite_type_3f_entries(
    source: bytes,
    *,
    expected_source_sha256: str,
    expected_count: int,
    entries: Sequence[bytes],
) -> tuple[bytes, dict[str, Any]]:
    """Replace the first exact type-0x3F entry sequence and prove its inverse."""

    source_sha256 = _sha256(source)
    if source_sha256 != expected_source_sha256:
        raise TrainingLetterModError("source SHA-256 does not match the recipe")
    if len(entries) > 0x7FFF:
        raise TrainingLetterModError("replacement table count exceeds signed 16-bit")
    if any(len(entry) != ENTRY_SIZE for entry in entries):
        raise TrainingLetterModError("every replacement entry must be 16 bytes")

    try:
        parsed = LevelDat.parse(source)
    except ValueError as error:
        raise TrainingLetterModError(str(error)) from error
    if not parsed.top_records:
        raise TrainingLetterModError("LEVEL DAT has no top record")
    selected = parsed.top_records[0]
    if (
        selected.offset != 4
        or selected.type_id != TYPE_3F
        or selected.count != expected_count
        or selected.size != 4 + expected_count * ENTRY_SIZE
    ):
        raise TrainingLetterModError("first type-0x3F table does not match the recipe")

    old_table_end = selected.offset + selected.size
    new_table = struct.pack("<hh", len(entries), TYPE_3F) + b"".join(entries)
    delta = len(new_table) - selected.size
    result = bytearray(
        source[: selected.offset] + new_table + source[old_table_end:]
    )
    claims = _pointer_claims(
        source,
        parsed,
        old_table_end=old_table_end,
        delta=delta,
    )
    for claim in claims:
        new_field_offset = _shifted(claim.field_offset, old_table_end, delta)
        if _u32(result, new_field_offset, "relocated pointer field") != claim.old_value:
            raise TrainingLetterModError(
                f"pointer source mismatch at 0x{claim.field_offset:x}"
            )
        struct.pack_into("<I", result, new_field_offset, claim.new_value)

    output = bytes(result)
    try:
        reparsed = LevelDat.parse(output)
    except ValueError as error:
        raise TrainingLetterModError(str(error)) from error
    if reparsed.top_records[0].count != len(entries):
        raise TrainingLetterModError("replacement table count did not reparse")
    if len(reparsed.primary_records) != len(parsed.primary_records):
        raise TrainingLetterModError("primary record count changed")
    if len(reparsed.secondary_records) != len(parsed.secondary_records):
        raise TrainingLetterModError("secondary record count changed")
    if reparsed.final_dword != parsed.final_dword:
        raise TrainingLetterModError("final dword changed")

    inverse = bytearray(output)
    for claim in claims:
        new_field_offset = _shifted(claim.field_offset, old_table_end, delta)
        if _u32(inverse, new_field_offset, "inverse pointer field") != claim.new_value:
            raise TrainingLetterModError(
                f"inverse pointer mismatch at 0x{claim.field_offset:x}"
            )
        struct.pack_into("<I", inverse, new_field_offset, claim.old_value)
    new_table_end = selected.offset + len(new_table)
    inverse = bytearray(
        inverse[: selected.offset]
        + source[selected.offset:old_table_end]
        + inverse[new_table_end:]
    )
    if bytes(inverse) != source:
        raise TrainingLetterModError("exact inverse reconstruction failed")

    return output, {
        "source_sha256": source_sha256,
        "output_sha256": _sha256(output),
        "source_size": len(source),
        "output_size": len(output),
        "table_offset": selected.offset,
        "source_table_count": expected_count,
        "output_table_count": len(entries),
        "table_size_delta": delta,
        "relocated_pointer_fields": len(claims),
        "inverse_matches_source": True,
    }


def transform_training_letter_records(
    source: bytes,
    *,
    expected_source_sha256: str,
    expected_count: int,
    move_positions: Mapping[int, Sequence[int]] | None = None,
    duplicate_positions: Mapping[int, Sequence[Sequence[int]]] | None = None,
    remove_selectors: Iterable[int] = (),
) -> tuple[bytes, dict[str, Any]]:
    """Move, duplicate, or remove exact unique letter-selector records.

    This asset-free helper deliberately requires an exact source hash and one
    source occurrence of each selector 0x10–0x13. It preserves every non-
    coordinate byte of moved and duplicated records.
    """

    move_positions = dict(move_positions or {})
    duplicate_positions = dict(duplicate_positions or {})
    remove_set = set(remove_selectors)
    operation_selectors = set(move_positions) | set(duplicate_positions) | remove_set
    unknown = operation_selectors - set(LETTER_SELECTORS)
    if unknown:
        raise TrainingLetterModError(
            f"unsupported letter selector: 0x{min(unknown):02x}"
        )
    if set(move_positions) & remove_set:
        raise TrainingLetterModError("cannot move and remove the same source letter")

    if _sha256(source) != expected_source_sha256:
        raise TrainingLetterModError("source SHA-256 does not match the recipe")
    try:
        parsed = LevelDat.parse(source)
    except ValueError as error:
        raise TrainingLetterModError(str(error)) from error
    if not parsed.top_records:
        raise TrainingLetterModError("LEVEL DAT has no top record")
    selected = parsed.top_records[0]
    if selected.count != expected_count or selected.type_id != TYPE_3F:
        raise TrainingLetterModError("first type-0x3F table does not match the recipe")
    entries_start = selected.offset + 4
    entries = [
        source[entries_start + index * ENTRY_SIZE : entries_start + (index + 1) * ENTRY_SIZE]
        for index in range(expected_count)
    ]
    sources: dict[int, bytes] = {}
    for selector in LETTER_SELECTORS:
        matches = [entry for entry in entries if _selector(entry) == selector]
        if len(matches) != 1:
            raise TrainingLetterModError(
                f"source must contain exactly one selector 0x{selector:02x} record"
            )
        sources[selector] = matches[0]

    normalized_moves = {
        selector: _position(position, f"move 0x{selector:02x}")
        for selector, position in move_positions.items()
    }
    normalized_duplicates = {
        selector: tuple(
            _position(position, f"duplicate 0x{selector:02x}")
            for position in positions
        )
        for selector, positions in duplicate_positions.items()
    }

    rewritten: list[bytes] = []
    removed: list[dict[str, Any]] = []
    moved: list[dict[str, Any]] = []
    for index, entry in enumerate(entries):
        selector = _selector(entry)
        if selector in remove_set:
            removed.append({"source_index": index, "selector": selector})
            continue
        if selector in normalized_moves:
            old_position = struct.unpack_from("<iii", entry, 0)
            new_position = normalized_moves[selector]
            entry = _with_position(entry, new_position)
            moved.append(
                {
                    "source_index": index,
                    "selector": selector,
                    "old_position": list(old_position),
                    "new_position": list(new_position),
                }
            )
        rewritten.append(entry)

    duplicated: list[dict[str, Any]] = []
    for selector in LETTER_SELECTORS:
        for position in normalized_duplicates.get(selector, ()):
            new_index = len(rewritten)
            rewritten.append(_with_position(sources[selector], position))
            duplicated.append(
                {
                    "source_selector": selector,
                    "new_index": new_index,
                    "new_position": list(position),
                }
            )

    result, receipt = _rewrite_type_3f_entries(
        source,
        expected_source_sha256=expected_source_sha256,
        expected_count=expected_count,
        entries=rewritten,
    )
    receipt.update(
        {
            "moved_letters": moved,
            "duplicated_letters": duplicated,
            "removed_letters": removed,
        }
    )
    return result, receipt


def build_training_duplicate_flik(source: bytes) -> tuple[bytes, dict[str, Any]]:
    """Duplicate all four exact Training letter records at moved positions."""

    if _sha256(source) != TRAINING_51_GRAINS_SHA256:
        raise TrainingLetterModError("source SHA-256 does not match the recipe")
    parsed = LevelDat.parse(source)
    selected = parsed.top_records[0]
    entries_start = selected.offset + 4
    counts = Counter(
        source[entries_start + index * ENTRY_SIZE + 0x0C]
        for index in range(selected.count)
    )
    if dict(counts) != _EXPECTED_SOURCE_SELECTOR_COUNTS:
        raise TrainingLetterModError("TRAINING selector census does not match the recipe")

    result, receipt = transform_training_letter_records(
        source,
        expected_source_sha256=TRAINING_51_GRAINS_SHA256,
        expected_count=63,
        duplicate_positions={
            selector: (position,)
            for selector, position in DUPLICATE_FLIK_POSITIONS.items()
        },
    )
    if receipt["relocated_pointer_fields"] != 556:
        raise TrainingLetterModError("TRAINING relocation census changed")
    if receipt["output_sha256"] != TRAINING_51_GRAINS_DUPLICATE_FLIK_SHA256:
        raise TrainingLetterModError("TRAINING output identity changed")

    reparsed = LevelDat.parse(result)
    result_start = reparsed.top_records[0].offset + 4
    result_counts = Counter(
        result[result_start + index * ENTRY_SIZE + 0x0C]
        for index in range(reparsed.top_records[0].count)
    )
    expected_counts = dict(_EXPECTED_SOURCE_SELECTOR_COUNTS)
    for selector in LETTER_SELECTORS:
        expected_counts[selector] = 2
    if dict(result_counts) != expected_counts:
        raise TrainingLetterModError("duplicate FLIK selector census changed")
    receipt["letter_selector_counts"] = {
        f"0x{selector:02x}": result_counts[selector]
        for selector in LETTER_SELECTORS
    }
    return result, receipt
