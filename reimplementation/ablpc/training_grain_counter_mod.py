"""Exact, asset-free recipe for the PC TRAINING 51-grain end tally."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Sequence


BUGS_EXE_SHA256 = (
    "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878"
)
TRAINING_51_COUNTER_EXE_SHA256 = (
    "8ececefbe1e5747322bd635830f4125500c087d3769094b79545bd7a7b6a4456"
)


class TrainingGrainCounterModError(ValueError):
    """Raised when the exact executable recipe cannot be applied safely."""


@dataclass(frozen=True)
class BytePatch:
    """One exact executable byte change with its PC address provenance."""

    file_offset: int
    virtual_address: int
    expected: bytes
    replacement: bytes
    purpose: str


TRAINING_51_COUNTER_PATCHES = (
    BytePatch(
        file_offset=0x422CB,
        virtual_address=0x00442ECB,
        expected=b"\x32",
        replacement=b"\x33",
        purpose="end-of-level tally counter upper-bound comparison",
    ),
    BytePatch(
        file_offset=0x422CF,
        virtual_address=0x00442ECF,
        expected=b"\x32",
        replacement=b"\x33",
        purpose="end-of-level tally counter clamped value",
    ),
    BytePatch(
        file_offset=0x42327,
        virtual_address=0x00442F27,
        expected=b"\x75",
        replacement=b"\x72",
        purpose="preserve the at-least-50 grain completion milestone at count 51",
    ),
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _apply_exact_byte_patches(
    source: bytes,
    *,
    expected_source_sha256: str,
    expected_output_sha256: str,
    patches: Sequence[BytePatch],
) -> tuple[bytes, dict[str, Any]]:
    """Apply non-overlapping exact byte patches and prove their exact inverse."""

    source_sha256 = _sha256(source)
    if source_sha256 != expected_source_sha256:
        raise TrainingGrainCounterModError(
            "source SHA-256 does not match the executable recipe"
        )
    if not patches:
        raise TrainingGrainCounterModError("executable recipe has no patches")

    occupied: set[int] = set()
    output = bytearray(source)
    changes: list[dict[str, Any]] = []
    for patch in patches:
        if not patch.expected or len(patch.expected) != len(patch.replacement):
            raise TrainingGrainCounterModError(
                f"invalid patch width at file offset 0x{patch.file_offset:x}"
            )
        end = patch.file_offset + len(patch.expected)
        if patch.file_offset < 0 or end > len(source):
            raise TrainingGrainCounterModError(
                f"patch at file offset 0x{patch.file_offset:x} is outside the source"
            )
        byte_range = set(range(patch.file_offset, end))
        if occupied & byte_range:
            raise TrainingGrainCounterModError("executable recipe patches overlap")
        occupied.update(byte_range)
        observed = source[patch.file_offset:end]
        if observed != patch.expected:
            raise TrainingGrainCounterModError(
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
    output_sha256 = _sha256(result)
    if output_sha256 != expected_output_sha256:
        raise TrainingGrainCounterModError(
            "patched executable SHA-256 does not match the recipe"
        )

    inverse = bytearray(result)
    for patch in patches:
        end = patch.file_offset + len(patch.expected)
        if inverse[patch.file_offset:end] != patch.replacement:
            raise TrainingGrainCounterModError(
                f"replacement bytes differ at file offset 0x{patch.file_offset:x}"
            )
        inverse[patch.file_offset:end] = patch.expected
    if bytes(inverse) != source:
        raise TrainingGrainCounterModError("exact inverse reconstruction failed")

    return result, {
        "source_sha256": source_sha256,
        "output_sha256": output_sha256,
        "source_size": len(source),
        "output_size": len(result),
        "changed_byte_count": sum(len(patch.expected) for patch in patches),
        "changes": changes,
        "inverse_matches_source": True,
    }


def build_training_51_counter_executable(
    source: bytes,
) -> tuple[bytes, dict[str, Any]]:
    """Retain 51 in the exact retail PC executable's Training end tally."""

    return _apply_exact_byte_patches(
        source,
        expected_source_sha256=BUGS_EXE_SHA256,
        expected_output_sha256=TRAINING_51_COUNTER_EXE_SHA256,
        patches=TRAINING_51_COUNTER_PATCHES,
    )
