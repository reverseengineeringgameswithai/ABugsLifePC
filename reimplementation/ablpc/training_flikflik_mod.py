"""Exact PC TRAINING FLIKFLIK executable behavior recipe.

The recipe composes the accepted M3.2 ``51/50`` tally executable with an
authored, position-independent code packet in existing linker padding.  It is
specific to the accepted M3.3 Training table layout: original letter records
occupy indices 50--53 and their four appended copies occupy indices 63--66.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import struct
from typing import Any, Sequence

from .training_grain_counter_mod import (
    BUGS_EXE_SHA256,
    TRAINING_51_COUNTER_EXE_SHA256,
    TrainingGrainCounterModError,
    build_training_51_counter_executable,
)


TRAINING_FLIKFLIK_EXE_SHA256 = (
    "b572e6d19bc417969c159ba0df7521cbb01b675c260a4dc98d2e6b34475947f4"
)

IMAGE_BASE = 0x00400000
TEXT_VIRTUAL_ADDRESS = 0x00001000
TEXT_FILE_OFFSET = 0x00000400
CODE_CAVE_VIRTUAL_ADDRESS = 0x004BBA00
HUD_HELPER_VIRTUAL_ADDRESS = CODE_CAVE_VIRTUAL_ADDRESS
TALLY_HELPER_VIRTUAL_ADDRESS = 0x004BBA64
PICKUP_HELPER_VIRTUAL_ADDRESSES = (
    0x004BBACC,
    0x004BBAD1,
    0x004BBAD6,
    0x004BBADB,
)
POPCOUNT_TABLE_VIRTUAL_ADDRESS = 0x004BBB40
COMPLETION_TRANSITION_FLAG_ADDRESS = 0x0086396F


class TrainingFlikflikModError(ValueError):
    """Raised when the exact FLIKFLIK executable recipe is unsafe."""


@dataclass(frozen=True)
class ExecutablePatch:
    """One exact executable byte-span change with PC-address provenance."""

    file_offset: int
    virtual_address: int
    expected: bytes
    replacement: bytes
    purpose: str


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file_offset(virtual_address: int) -> int:
    return (
        virtual_address
        - IMAGE_BASE
        - TEXT_VIRTUAL_ADDRESS
        + TEXT_FILE_OFFSET
    )


def _relative_call(virtual_address: int, target: int) -> bytes:
    return b"\xE8" + struct.pack("<i", target - (virtual_address + 5))


def _call_and_jump(virtual_address: int, call_target: int, jump_target: int) -> bytes:
    return _relative_call(virtual_address, call_target) + b"\xE9" + struct.pack(
        "<i", jump_target - (virtual_address + 10)
    )


def _call_and_nops(virtual_address: int, call_target: int) -> bytes:
    return _relative_call(virtual_address, call_target) + b"\x90\x90"


# Authored x86 code through the centered tally x-position table.  The final
# 256 bytes are generated below as a complete byte popcount table.  The code
# uses call/pop-relative access for new global references; it therefore adds
# no base-relocation requirement inside the former linker-padding span.  Its
# one-shot scratch byte is the last byte of the original writable ``.data``
# virtual extent; it is zero-initialized, outside raw file data, and has no
# original static reference.
_CODE_PREFIX = bytes.fromhex(
    "6031dbb80100000089d9d3e0e8000000005a8482a11f0e00741f89d883e00383"
    "c0108d3c5bc1e70383c74055505657e8db5ff4ff83c410eb2389d883e00383c0"
    "108d3c5bc1e70383c7406a206a206a4055505657e8b263f4ff83c41c4383fb08"
    "72a161c36031f6b80100000089f1d3e089f7d1e701df83e70f89f283e203c1e2"
    "0401d7e8000000005a8b94b298000000e8000000005984811d1f0e007410576a"
    "326a7452e84e59f4ff83c410eb166a006a606a606a60576a326a7452e89563f4"
    "ff83c4204683fe08729d61c350b001eb0d50b002eb0850b004eb0350b00851e8"
    "0000000059c6818b7e3a000080faff74278b89789e100081c1f403000039cf72"
    "03c0e00408c280faff750de80000000059c6815f7e3a00015958663d000cc3cc"
    "420000005a0000007000000084000000"
    "a0000000b8000000ce000000e2000000"
)
_POPCOUNT_TABLE = bytes(value.bit_count() for value in range(256))
FLIKFLIK_CODE = _CODE_PREFIX + _POPCOUNT_TABLE
FLIKFLIK_CODE_SHA256 = (
    "0d32f7fadf1dd7ccbfaba8689e9bb3a95278fcc7e6ab161084359e5eb27f8370"
)


def _patch(
    virtual_address: int,
    expected: bytes,
    replacement: bytes,
    purpose: str,
) -> ExecutablePatch:
    return ExecutablePatch(
        file_offset=_file_offset(virtual_address),
        virtual_address=virtual_address,
        expected=expected,
        replacement=replacement,
        purpose=purpose,
    )


_ALL_EIGHT_COMPARISONS = (
    (0x00416DDD, "in-level HUD completion animation"),
    (0x00442F64, "end-tally completion-state gate"),
    (0x0044348D, "end-tally one-shot completion sound gate"),
)

_PICKUP_TRANSITION_COMPARISONS = (
    0x00417AA3,
    0x00417AFD,
    0x00417B85,
    0x00417C0D,
)

_POPCOUNT_POINTERS = (
    0x00443473,
    0x004434CD,
    0x004435A3,
    0x004435E5,
)


TRAINING_FLIKFLIK_PATCHES = (
    _patch(
        0x00416DF9,
        bytes.fromhex("f6c1017410556a10566a"),
        _call_and_jump(0x00416DF9, HUD_HELPER_VIRTUAL_ADDRESS, 0x00416EBB),
        "replace four-slot in-level letter drawing with centered eight-slot helper",
    ),
    _patch(
        0x004430BD,
        bytes.fromhex("a8017411536a326a746a"),
        _call_and_jump(0x004430BD, TALLY_HELPER_VIRTUAL_ADDRESS, 0x004431BC),
        "replace four-slot completion-tally letter drawing with centered helper",
    ),
    *(
        _patch(
            virtual_address,
            bytes.fromhex(expected_hex),
            _call_and_nops(virtual_address, helper),
            f"assign independent original/duplicate selector bit {bit:#04x}",
        )
        for virtual_address, expected_hex, helper, bit in (
            (0x00417A65, "80ca01663d000c", 0x004BBACC, 0x01),
            (0x00417ABF, "80ca02663d000c", 0x004BBAD1, 0x02),
            (0x00417B47, "80ca04663d000c", 0x004BBAD6, 0x04),
            (0x00417BCF, "80ca08663d000c", 0x004BBADB, 0x08),
        )
    ),
    *(
        _patch(virtual_address, b"\x0F", b"\xFF", purpose)
        for virtual_address, purpose in _ALL_EIGHT_COMPARISONS
    ),
    *(
        _patch(
            virtual_address,
            struct.pack("<I", 0x0059D9B2) + b"\x0F",
            struct.pack("<I", COMPLETION_TRANSITION_FLAG_ADDRESS) + b"\x01",
            "gate reward on the incomplete-to-all-eight transition only",
        )
        for virtual_address in _PICKUP_TRANSITION_COMPARISONS
    ),
    *(
        _patch(
            virtual_address,
            struct.pack("<I", 0x004DD6C0),
            struct.pack("<I", POPCOUNT_TABLE_VIRTUAL_ADDRESS),
            "redirect four-bit tally lookup to complete eight-bit popcount table",
        )
        for virtual_address in _POPCOUNT_POINTERS
    ),
    _patch(0x004431E3, b"\x04", b"\x08", "render /8 letter denominator"),
    _patch(0x00443328, b"\x04", b"\x08", "gate tally emblem on eight letters"),
    *(
        _patch(virtual_address, b"\x74", b"\x58", "move /8 count above word")
        for virtual_address in (0x004431C4, 0x004431D4, 0x004431E7)
    ),
    *(
        _patch(virtual_address, b"\x64", b"\x50", "move existing emblem to count row")
        for virtual_address in (0x00443330, 0x0044334D, 0x00443371)
    ),
    *(
        _patch(
            virtual_address,
            expected,
            b"\x6A\x00\x90\x90\x90",
            "move existing emblem left without changing its asset or state gate",
        )
        for virtual_address, expected in (
            (0x00443331, bytes.fromhex("68f8000000")),
            (0x0044334E, bytes.fromhex("68f0000000")),
            (0x00443372, bytes.fromhex("68f0000000")),
        )
    ),
    _patch(
        CODE_CAVE_VIRTUAL_ADDRESS,
        b"\xCC" * len(FLIKFLIK_CODE),
        FLIKFLIK_CODE,
        "install position-independent eight-slot draw/pickup helpers and popcount table",
    ),
)


def _apply_exact_patches(
    source: bytes,
    *,
    expected_source_sha256: str,
    expected_output_sha256: str,
    patches: Sequence[ExecutablePatch],
) -> tuple[bytes, dict[str, Any]]:
    """Apply non-overlapping exact spans and prove byte-for-byte inversion."""

    source_sha256 = _sha256(source)
    if source_sha256 != expected_source_sha256:
        raise TrainingFlikflikModError(
            "source SHA-256 does not match the FLIKFLIK executable recipe"
        )
    if not patches:
        raise TrainingFlikflikModError("FLIKFLIK executable recipe has no patches")

    occupied: set[int] = set()
    output = bytearray(source)
    changes: list[dict[str, Any]] = []
    for patch in patches:
        if not patch.expected or len(patch.expected) != len(patch.replacement):
            raise TrainingFlikflikModError(
                f"invalid patch width at file offset 0x{patch.file_offset:x}"
            )
        end = patch.file_offset + len(patch.expected)
        if patch.file_offset < 0 or end > len(source):
            raise TrainingFlikflikModError(
                f"patch at file offset 0x{patch.file_offset:x} is outside the source"
            )
        byte_range = set(range(patch.file_offset, end))
        if occupied & byte_range:
            raise TrainingFlikflikModError("FLIKFLIK executable recipe patches overlap")
        occupied.update(byte_range)
        if source[patch.file_offset:end] != patch.expected:
            raise TrainingFlikflikModError(
                f"source bytes differ at file offset 0x{patch.file_offset:x}"
            )
        output[patch.file_offset:end] = patch.replacement
        changes.append(
            {
                "file_offset": patch.file_offset,
                "virtual_address": patch.virtual_address,
                "width": len(patch.expected),
                "expected_hex": patch.expected.hex(),
                "replacement_hex": patch.replacement.hex(),
                "purpose": patch.purpose,
            }
        )

    result = bytes(output)
    output_sha256 = _sha256(result)
    if output_sha256 != expected_output_sha256:
        raise TrainingFlikflikModError(
            "patched executable SHA-256 does not match the FLIKFLIK recipe"
        )

    inverse = bytearray(result)
    for patch in patches:
        end = patch.file_offset + len(patch.expected)
        if inverse[patch.file_offset:end] != patch.replacement:
            raise TrainingFlikflikModError(
                f"replacement bytes differ at file offset 0x{patch.file_offset:x}"
            )
        inverse[patch.file_offset:end] = patch.expected
    if bytes(inverse) != source:
        raise TrainingFlikflikModError("exact inverse reconstruction failed")

    return result, {
        "source_sha256": source_sha256,
        "output_sha256": output_sha256,
        "source_size": len(source),
        "output_size": len(result),
        "patch_count": len(patches),
        "patched_span_byte_count": sum(len(patch.expected) for patch in patches),
        "changed_byte_count": sum(a != b for a, b in zip(source, result)),
        "code_sha256": FLIKFLIK_CODE_SHA256,
        "changes": changes,
        "inverse_matches_source": True,
    }


def patch_training_flikflik_executable(
    source: bytes,
) -> tuple[bytes, dict[str, Any]]:
    """Patch the exact accepted M3.2 executable with FLIKFLIK behavior."""

    if len(_CODE_PREFIX) != 320 or len(FLIKFLIK_CODE) != 576:
        raise TrainingFlikflikModError("authored FLIKFLIK code layout changed")
    if _sha256(FLIKFLIK_CODE) != FLIKFLIK_CODE_SHA256:
        raise TrainingFlikflikModError("authored FLIKFLIK code identity changed")
    return _apply_exact_patches(
        source,
        expected_source_sha256=TRAINING_51_COUNTER_EXE_SHA256,
        expected_output_sha256=TRAINING_FLIKFLIK_EXE_SHA256,
        patches=TRAINING_FLIKFLIK_PATCHES,
    )


def build_training_flikflik_executable(
    retail_source: bytes,
) -> tuple[bytes, dict[str, Any]]:
    """Compose the accepted M3.2 counter patch and exact M3.4 behavior patch."""

    if _sha256(retail_source) != BUGS_EXE_SHA256:
        raise TrainingFlikflikModError("source SHA-256 does not match retail bugs.exe")
    try:
        counter_executable, counter_receipt = build_training_51_counter_executable(
            retail_source
        )
    except TrainingGrainCounterModError as error:
        raise TrainingFlikflikModError(str(error)) from error
    result, receipt = patch_training_flikflik_executable(counter_executable)
    receipt["retail_source_sha256"] = BUGS_EXE_SHA256
    receipt["composed_counter_sha256"] = counter_receipt["output_sha256"]
    receipt["counter_inverse_matches_retail"] = counter_receipt[
        "inverse_matches_source"
    ]
    return result, receipt
