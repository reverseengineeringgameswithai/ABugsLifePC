"""Regression tests for scripts/audit-tracked-files.py provenance rules,
including the tools/86box/patches/ source-patch exception (DEC-20260818-149)."""

from __future__ import annotations

import importlib.util
from pathlib import Path, PurePosixPath

_SPEC = importlib.util.spec_from_file_location(
    "audit_tracked_files",
    Path(__file__).resolve().parents[1] / "scripts" / "audit-tracked-files.py",
)
_MOD = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
_SPEC.loader.exec_module(_MOD)
violations = _MOD.violations


def _flagged(path: str) -> bool:
    return bool(violations([PurePosixPath(path)]))


def test_downloaded_emulator_binary_flagged() -> None:
    assert _flagged("tools/86box/86Box")


def test_tools_86box_readme_allowed() -> None:
    assert not _flagged("tools/86box/README.md")


def test_source_patch_under_patches_allowed() -> None:
    assert not _flagged("tools/86box/patches/86box-v6.0-ablrec.patch")


def test_patches_readme_allowed() -> None:
    assert not _flagged("tools/86box/patches/README.md")


def test_binary_in_patches_still_flagged() -> None:
    # the patches exception must not become a loophole for binaries/media
    assert _flagged("tools/86box/patches/sneaky.exe")


def test_protected_work_path_flagged() -> None:
    assert _flagged("work/86box/v6/86Box")
