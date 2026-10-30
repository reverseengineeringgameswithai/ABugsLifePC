"""Guarded PC executable recipe for Tunnels and City Entrance grain gates.

The retail City Entrance routine derives its three requirements with
``10 * (gate_index + 1)``.  This recipe replaces only that derivation with a
three-dword lookup in the function's existing INT3 alignment gap.  The Tunnels
routine already reads nine dword requirements from its resident data
table, so those values are edited in place.

All locations are specific to the exact supported retail ``bugs.exe``.  The
transform preserves every unselected byte and proves an exact inverse before
returning an output.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import struct
from typing import Any, Sequence


BUGS_EXE_SHA256 = (
    "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
)

RETAIL_TUNNELS_REQUIREMENTS = (20, 10, 10, 10, 20, 20, 30, 10, 30)
RETAIL_CITY_ENTRANCE_REQUIREMENTS = (10, 20, 30)

CITY_ENTRANCE_FORMULA_FILE_OFFSET = 0x32BD1
CITY_ENTRANCE_FORMULA_VIRTUAL_ADDRESS = 0x004337D1
CITY_ENTRANCE_REQUIREMENTS_FILE_OFFSET = 0x32CB0
CITY_ENTRANCE_REQUIREMENTS_VIRTUAL_ADDRESS = 0x004338B0

TUNNELS_TABLE_FILE_OFFSET = 0xD95C8
TUNNELS_TABLE_VIRTUAL_ADDRESS = 0x004DA9C8
TUNNELS_TEMPLATE_FILE_OFFSET = 0xD9680
TUNNELS_TEMPLATE_VIRTUAL_ADDRESS = 0x004DAA80
TUNNELS_RECORD_SIZE = 20
TUNNELS_REQUIREMENT_OFFSET = 8

_RETAIL_CITY_ENTRANCE_FORMULA = bytes.fromhex(
    "8d460133d28a15b1d959008d0c80d1e1"
)
_CITY_ENTRANCE_TABLE_FORMULA = bytes.fromhex(
    "0fb615b1d959008b0cb5b03843009090"
)
_RETAIL_CITY_ENTRANCE_REQUIREMENTS_GAP = b"\xcc" * 12

_TUNNELS_FIELDS_04 = (26, 23, 24, 22, 25, 21, 28, 20, 27)
_TUNNELS_XZ = (
    (193754, 131692),
    (505642, -451306),
    (832302, 291075),
    (509676, 510143),
    (833246, 612273),
    (1142934, 1308289),
    (1471643, 1410369),
    (1202034, 1986285),
    (1634925, 2534812),
)


class GrainGateModError(ValueError):
    """Raised when the exact executable transform cannot be applied safely."""


@dataclass(frozen=True)
class _Patch:
    file_offset: int
    virtual_address: int
    expected: bytes
    replacement: bytes
    purpose: str


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _validate_requirements(
    values: Sequence[int],
    *,
    label: str,
    count: int,
) -> tuple[int, ...]:
    result = tuple(values)
    if len(result) != count:
        raise GrainGateModError(f"{label} requires exactly {count} values")
    for index, value in enumerate(result):
        if isinstance(value, bool) or not isinstance(value, int):
            raise GrainGateModError(f"{label} value {index} is not an integer")
        if not 0 <= value <= 50:
            raise GrainGateModError(
                f"{label} value {index} is outside the supported 0..50 range"
            )
    return result


def _tunnels_requirement_offset(index: int, *, template: bool) -> int:
    table_offset = (
        TUNNELS_TEMPLATE_FILE_OFFSET
        if template
        else TUNNELS_TABLE_FILE_OFFSET
    )
    return (
        table_offset
        + index * TUNNELS_RECORD_SIZE
        + TUNNELS_REQUIREMENT_OFFSET
    )


def _tunnels_requirement_address(index: int, *, template: bool) -> int:
    table_address = (
        TUNNELS_TEMPLATE_VIRTUAL_ADDRESS
        if template
        else TUNNELS_TABLE_VIRTUAL_ADDRESS
    )
    return (
        table_address
        + index * TUNNELS_RECORD_SIZE
        + TUNNELS_REQUIREMENT_OFFSET
    )


def _patches_for(
    tunnels_requirements: tuple[int, ...],
    city_entrance_requirements: tuple[int, ...],
) -> tuple[_Patch, ...]:
    patches = [
        _Patch(
            file_offset=CITY_ENTRANCE_FORMULA_FILE_OFFSET,
            virtual_address=CITY_ENTRANCE_FORMULA_VIRTUAL_ADDRESS,
            expected=_RETAIL_CITY_ENTRANCE_FORMULA,
            replacement=_CITY_ENTRANCE_TABLE_FORMULA,
            purpose=(
                "City Entrance: replace 10x indexed formula with a "
                "three-entry lookup"
            ),
        ),
        _Patch(
            file_offset=CITY_ENTRANCE_REQUIREMENTS_FILE_OFFSET,
            virtual_address=CITY_ENTRANCE_REQUIREMENTS_VIRTUAL_ADDRESS,
            expected=_RETAIL_CITY_ENTRANCE_REQUIREMENTS_GAP,
            replacement=struct.pack("<3I", *city_entrance_requirements),
            purpose="City Entrance: three independent gate requirements",
        ),
    ]
    for template in (False, True):
        table_name = "initializer template" if template else "live image table"
        for index, (retail, replacement) in enumerate(
            zip(
                RETAIL_TUNNELS_REQUIREMENTS,
                tunnels_requirements,
                strict=True,
            )
        ):
            patches.append(
                _Patch(
                    file_offset=_tunnels_requirement_offset(
                        index,
                        template=template,
                    ),
                    virtual_address=_tunnels_requirement_address(
                        index,
                        template=template,
                    ),
                    expected=struct.pack("<I", retail),
                    replacement=struct.pack("<I", replacement),
                    purpose=f"Tunnels: {table_name} row {index} requirement",
                )
            )
    return tuple(patches)


def _apply_patches(
    source: bytes,
    *,
    expected_source_sha256: str,
    patches: Sequence[_Patch],
) -> tuple[bytes, dict[str, Any]]:
    source_sha256 = _sha256(source)
    if source_sha256 != expected_source_sha256:
        raise GrainGateModError(
            "source SHA-256 does not match the executable recipe"
        )
    if not patches:
        raise GrainGateModError("grain-gate executable recipe has no patches")

    output = bytearray(source)
    occupied: set[int] = set()
    changes: list[dict[str, Any]] = []
    for patch in patches:
        if not patch.expected or len(patch.expected) != len(patch.replacement):
            raise GrainGateModError(
                f"invalid patch width at file offset 0x{patch.file_offset:x}"
            )
        end = patch.file_offset + len(patch.expected)
        if patch.file_offset < 0 or end > len(source):
            raise GrainGateModError(
                f"patch at file offset 0x{patch.file_offset:x} is outside the source"
            )
        byte_range = set(range(patch.file_offset, end))
        if occupied & byte_range:
            raise GrainGateModError("grain-gate executable recipe patches overlap")
        occupied.update(byte_range)
        observed = source[patch.file_offset:end]
        if observed != patch.expected:
            raise GrainGateModError(
                f"source bytes differ at file offset 0x{patch.file_offset:x}"
            )
        output[patch.file_offset:end] = patch.replacement
        changes.append(
            {
                "file_offset": patch.file_offset,
                "virtual_address": patch.virtual_address,
                "expected_hex": patch.expected.hex(),
                "replacement_hex": patch.replacement.hex(),
                "purpose": patch.purpose,
            }
        )

    result = bytes(output)
    inverse = bytearray(result)
    for patch in patches:
        end = patch.file_offset + len(patch.expected)
        if inverse[patch.file_offset:end] != patch.replacement:
            raise GrainGateModError(
                f"replacement bytes differ at file offset 0x{patch.file_offset:x}"
            )
        inverse[patch.file_offset:end] = patch.expected
    if bytes(inverse) != source:
        raise GrainGateModError("exact inverse reconstruction failed")

    return result, {
        "source_sha256": source_sha256,
        "output_sha256": _sha256(result),
        "source_size": len(source),
        "output_size": len(result),
        "touched_byte_count": sum(len(patch.expected) for patch in patches),
        "changed_byte_count": sum(a != b for a, b in zip(source, result, strict=True)),
        "changes": changes,
        "inverse_matches_source": True,
    }


def _build_grain_gate_executable(
    source: bytes,
    *,
    expected_source_sha256: str,
    tunnels_requirements: Sequence[int],
    city_entrance_requirements: Sequence[int],
) -> tuple[bytes, dict[str, Any]]:
    tunnels = _validate_requirements(
        tunnels_requirements,
        label="Tunnels",
        count=9,
    )
    city = _validate_requirements(
        city_entrance_requirements,
        label="City Entrance",
        count=3,
    )
    result, receipt = _apply_patches(
        source,
        expected_source_sha256=expected_source_sha256,
        patches=_patches_for(tunnels, city),
    )
    receipt["tunnels_requirements"] = list(tunnels)
    receipt["city_entrance_requirements"] = list(city)
    receipt["retail_tunnels_requirements"] = list(RETAIL_TUNNELS_REQUIREMENTS)
    receipt["retail_city_entrance_requirements"] = list(
        RETAIL_CITY_ENTRANCE_REQUIREMENTS
    )
    receipt["tunnels_rows"] = [
        {
            "row": index,
            "field_04": _TUNNELS_FIELDS_04[index],
            "x": _TUNNELS_XZ[index][0],
            "z": _TUNNELS_XZ[index][1],
            "requirement": requirement,
        }
        for index, requirement in enumerate(tunnels)
    ]
    receipt["tunnels_linked_rows"] = [[0, 4]]
    return result, receipt


def build_grain_gate_executable(
    source: bytes,
    *,
    tunnels_requirements: Sequence[int] = RETAIL_TUNNELS_REQUIREMENTS,
    city_entrance_requirements: Sequence[int] = RETAIL_CITY_ENTRANCE_REQUIREMENTS,
) -> tuple[bytes, dict[str, Any]]:
    """Build a configured grain-gate executable from the exact retail PC binary."""

    return _build_grain_gate_executable(
        source,
        expected_source_sha256=BUGS_EXE_SHA256,
        tunnels_requirements=tunnels_requirements,
        city_entrance_requirements=city_entrance_requirements,
    )
