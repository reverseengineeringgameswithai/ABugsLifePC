"""Tests for the exact auto-hardware executable transform (EXP-20260816-143)."""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reimplementation"))

from ablpc.auto_hardware_mod import (  # noqa: E402
    AutoHardwareModError,
    CODE_FILE_OFFSET,
    RELOCATION_FILE_OFFSET,
    RETAIL_BUGS_EXE_SHA256,
    _apply_patches,
    _patches,
    build_auto_hardware_executable,
    invert_auto_hardware_executable,
)

RETAIL_EXE = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe"
EXPECTED_OUTPUT_SHA256 = (
    "1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f"
)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _synthetic_source() -> bytes:
    """A buffer carrying the two exact expected spans at their real offsets."""
    size = RELOCATION_FILE_OFFSET + 0x100
    buf = bytearray(b"\x5a" * size)
    for patch in _patches():
        buf[patch.file_offset:patch.file_offset + len(patch.expected)] = patch.expected
    return bytes(buf)


def test_patch_constants_pin_the_exact_transform() -> None:
    assert CODE_FILE_OFFSET == 0x000A6C6B
    assert RELOCATION_FILE_OFFSET == 0x000FA912
    code, reloc = _patches()
    assert code.expected.hex() == "ffd72b0534127f0099"
    assert code.replacement.hex() == "896c2410e9e2010000"
    assert code.virtual_address == 0x004A786B
    assert reloc.expected.hex() == "6f38"
    assert reloc.replacement.hex() == "6f08"


def test_apply_patches_on_synthetic_source_is_exact_and_reversible() -> None:
    src = _synthetic_source()
    result, receipt = _apply_patches(
        src, expected_source_sha256=_sha(src), patches=_patches()
    )
    # exactly the two spans changed, everything else preserved
    assert len(result) == len(src)
    assert result[CODE_FILE_OFFSET:CODE_FILE_OFFSET + 9] == bytes.fromhex(
        "896c2410e9e2010000"
    )
    assert result[RELOCATION_FILE_OFFSET:RELOCATION_FILE_OFFSET + 2] == bytes.fromhex(
        "6f08"
    )
    diff = [i for i in range(len(src)) if src[i] != result[i]]
    assert set(diff) <= (
        set(range(CODE_FILE_OFFSET, CODE_FILE_OFFSET + 9))
        | set(range(RELOCATION_FILE_OFFSET, RELOCATION_FILE_OFFSET + 2))
    )
    assert receipt["inverse_matches_source"] is True
    assert receipt["touched_byte_count"] == 11
    assert receipt["changed_byte_count"] == 9  # one code byte and one reloc byte equal


def test_wrong_source_sha_is_refused() -> None:
    src = _synthetic_source()
    with pytest.raises(AutoHardwareModError, match="source SHA-256"):
        _apply_patches(src, expected_source_sha256="00" * 32, patches=_patches())


def test_public_build_requires_the_exact_retail_sha() -> None:
    with pytest.raises(AutoHardwareModError, match="source SHA-256"):
        build_auto_hardware_executable(_synthetic_source())


def test_wrong_expected_bytes_are_refused_before_any_write() -> None:
    src = bytearray(_synthetic_source())
    # corrupt one byte inside the code span so the expected check fails
    src[CODE_FILE_OFFSET + 3] ^= 0xFF
    with pytest.raises(AutoHardwareModError, match="source bytes differ"):
        _apply_patches(
            bytes(src), expected_source_sha256=_sha(bytes(src)), patches=_patches()
        )


def test_reloc_edit_is_required_no_one_edit_result() -> None:
    # A source with the code span but a wrong relocation span must be refused,
    # proving both edits are mandatory (never a one-edit output).
    src = bytearray(_synthetic_source())
    src[RELOCATION_FILE_OFFSET + 1] = 0x99  # not 0x38
    with pytest.raises(AutoHardwareModError, match="source bytes differ"):
        _apply_patches(
            bytes(src), expected_source_sha256=_sha(bytes(src)), patches=_patches()
        )


def test_invert_round_trips_and_rejects_foreign_bytes() -> None:
    src = _synthetic_source()
    result, _ = _apply_patches(
        src, expected_source_sha256=_sha(src), patches=_patches()
    )
    # invert on a synthetic buffer uses the retail-sha guard, so it must fail
    # the final identity check (synthetic != retail) — proving the guard bites.
    with pytest.raises(AutoHardwareModError, match="reconstructed source"):
        invert_auto_hardware_executable(result)


# --- integration against the real retail copy (skipped if absent) ---


def _retail_source() -> bytes:
    if not RETAIL_EXE.is_file():
        pytest.skip("ignored retail-derived executable is not present")
    data = RETAIL_EXE.read_bytes()
    assert _sha(data) == RETAIL_BUGS_EXE_SHA256
    return data


def test_retail_build_pins_output_hash_and_preserves_all_other_bytes() -> None:
    src = _retail_source()
    result, receipt = build_auto_hardware_executable(src)
    assert receipt["output_sha256"] == EXPECTED_OUTPUT_SHA256
    assert receipt["source_sha256"] == RETAIL_BUGS_EXE_SHA256
    assert receipt["output_size"] == receipt["source_size"] == len(src)
    assert receipt["changed_byte_count"] == 9
    changed = [i for i in range(len(src)) if src[i] != result[i]]
    assert set(changed) <= (
        set(range(CODE_FILE_OFFSET, CODE_FILE_OFFSET + 9))
        | set(range(RELOCATION_FILE_OFFSET, RELOCATION_FILE_OFFSET + 2))
    )


def test_retail_build_inverse_reconstructs_retail_exactly() -> None:
    src = _retail_source()
    result, _ = build_auto_hardware_executable(src)
    back, info = invert_auto_hardware_executable(result)
    assert back == src
    assert info["reconstructed_source_sha256"] == RETAIL_BUGS_EXE_SHA256
