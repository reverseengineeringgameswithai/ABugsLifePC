"""Exact auto-hardware (auto-Direct3D) PC executable transform.

Applies the hash-locked paired code-plus-relocation transform designed and
James-reviewed as a static candidate in
[[EXP-20260816-143 - Automatic Direct3D startup static audit]] and
[[PC automatic Direct3D startup candidate]]. It auto-confirms renderer
selector 2 (Direct3D) and skips only the chooser's interactive
timing/fade/input/draw loop, entering the chooser's original cleanup — the
temporary DirectDraw/surface setup through ``0x004A7866`` is retained (this is
NOT the rejected whole-chooser bypass).

Two mandatory, exactly reversible edits (retail source only):

- code at file ``0x000A6C6B`` (VA ``0x004A786B``): ``FF D7 2B 05 34 12 7F 00
  99`` -> ``89 6C 24 10 E9 E2 01 00 00`` = ``mov [esp+0x10], ebp`` (ebp was set
  to 2 at ``0x004A7866``) then ``jmp 0x004A7A56`` (displacement ``0x1E2`` from
  next PC ``0x004A7874``);
- relocation entry at file ``0x000FA912``: ``6F 38`` -> ``6F 08``, converting
  the PE HIGHLOW relocation targeting the overwritten operand at RVA
  ``0x000A786F`` into type-zero (ABSOLUTE) padding so rebasing cannot corrupt
  the new relative jump. Offset ``0x86F`` within the block is preserved.

The transform verifies the exact source SHA-256 and both original byte
sequences, applies both edits as one operation, preserves every other byte,
and proves exact inverse reconstruction before returning. Game-bearing
outputs remain ignored and must not be committed.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Sequence

RETAIL_BUGS_EXE_SHA256 = (
    "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
)

CODE_FILE_OFFSET = 0x000A6C6B
CODE_VIRTUAL_ADDRESS = 0x004A786B
_RETAIL_CODE = bytes.fromhex("ffd72b0534127f0099")
_AUTO_HARDWARE_CODE = bytes.fromhex("896c2410e9e2010000")

RELOCATION_FILE_OFFSET = 0x000FA912
_RETAIL_RELOCATION = bytes.fromhex("6f38")
_PADDING_RELOCATION = bytes.fromhex("6f08")


class AutoHardwareModError(ValueError):
    """Raised when the exact executable transform cannot be applied safely."""


@dataclass(frozen=True)
class _Patch:
    file_offset: int
    virtual_address: int | None
    expected: bytes
    replacement: bytes
    purpose: str


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _patches() -> tuple[_Patch, ...]:
    return (
        _Patch(
            file_offset=CODE_FILE_OFFSET,
            virtual_address=CODE_VIRTUAL_ADDRESS,
            expected=_RETAIL_CODE,
            replacement=_AUTO_HARDWARE_CODE,
            purpose=(
                "set chooser result 2 and jump to the original cleanup "
                "0x004A7A56, skipping only the interactive chooser loop"
            ),
        ),
        _Patch(
            file_offset=RELOCATION_FILE_OFFSET,
            virtual_address=None,
            expected=_RETAIL_RELOCATION,
            replacement=_PADDING_RELOCATION,
            purpose=(
                "convert the HIGHLOW relocation for RVA 0x000A786F to "
                "type-zero padding so rebasing cannot corrupt the new jump"
            ),
        ),
    )


def _apply_patches(
    source: bytes,
    *,
    expected_source_sha256: str,
    patches: Sequence[_Patch],
) -> tuple[bytes, dict[str, Any]]:
    source_sha256 = _sha256(source)
    if source_sha256 != expected_source_sha256:
        raise AutoHardwareModError(
            "source SHA-256 does not match the retail executable recipe"
        )
    if not patches:
        raise AutoHardwareModError("auto-hardware recipe has no patches")

    output = bytearray(source)
    occupied: set[int] = set()
    changes: list[dict[str, Any]] = []
    for patch in patches:
        if not patch.expected or len(patch.expected) != len(patch.replacement):
            raise AutoHardwareModError(
                f"invalid patch width at file offset 0x{patch.file_offset:x}"
            )
        end = patch.file_offset + len(patch.expected)
        if patch.file_offset < 0 or end > len(source):
            raise AutoHardwareModError(
                f"patch at file offset 0x{patch.file_offset:x} is outside the source"
            )
        byte_range = set(range(patch.file_offset, end))
        if occupied & byte_range:
            raise AutoHardwareModError("auto-hardware recipe patches overlap")
        occupied.update(byte_range)
        observed = source[patch.file_offset:end]
        if observed != patch.expected:
            raise AutoHardwareModError(
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

    # Prove exact inverse reconstruction before returning.
    inverse = bytearray(result)
    for patch in patches:
        end = patch.file_offset + len(patch.expected)
        if inverse[patch.file_offset:end] != patch.replacement:
            raise AutoHardwareModError(
                f"replacement bytes differ at file offset 0x{patch.file_offset:x}"
            )
        inverse[patch.file_offset:end] = patch.expected
    if bytes(inverse) != source:
        raise AutoHardwareModError("exact inverse reconstruction failed")

    return result, {
        "source_sha256": source_sha256,
        "output_sha256": _sha256(result),
        "source_size": len(source),
        "output_size": len(result),
        "touched_byte_count": sum(len(patch.expected) for patch in patches),
        "changed_byte_count": sum(
            a != b for a, b in zip(source, result, strict=True)
        ),
        "changes": changes,
        "inverse_matches_source": True,
    }


def build_auto_hardware_executable(
    source: bytes,
) -> tuple[bytes, dict[str, Any]]:
    """Build the auto-hardware executable from the exact retail PC binary.

    Returns ``(output_bytes, receipt)``. Both edits are applied atomically or
    an :class:`AutoHardwareModError` is raised; a one-edit result is never
    produced.
    """

    return _apply_patches(
        source,
        expected_source_sha256=RETAIL_BUGS_EXE_SHA256,
        patches=_patches(),
    )


def invert_auto_hardware_executable(
    modified: bytes,
) -> tuple[bytes, dict[str, Any]]:
    """Reconstruct the exact retail source from an auto-hardware output."""

    output = bytearray(modified)
    for patch in _patches():
        end = patch.file_offset + len(patch.expected)
        if end > len(modified) or output[patch.file_offset:end] != patch.replacement:
            raise AutoHardwareModError(
                f"modified bytes differ at file offset 0x{patch.file_offset:x}"
            )
        output[patch.file_offset:end] = patch.expected
    source = bytes(output)
    if _sha256(source) != RETAIL_BUGS_EXE_SHA256:
        raise AutoHardwareModError(
            "reconstructed source SHA-256 does not match retail"
        )
    return source, {"reconstructed_source_sha256": RETAIL_BUGS_EXE_SHA256}
