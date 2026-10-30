"""Tests for the play-pristine.sh launcher --auto-hardware wiring.

Uses --dry-run so no game process is launched. Skips if the retail work copy
is absent.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "scripts" / "play-pristine.sh"
RETAIL_EXE = ROOT / "work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe"
CACHE_EXE = ROOT / "work/copies/auto-hardware/bugs.exe"
AUTO_HARDWARE_SHA256 = (
    "1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f"
)


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(LAUNCHER), *args],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=str(ROOT),
    )


def test_help_documents_auto_hardware() -> None:
    result = _run("--help")
    assert result.returncode == 0
    assert "--auto-hardware" in result.stdout


def _require_retail() -> None:
    if not RETAIL_EXE.is_file():
        pytest.skip("ignored retail-derived executable is not present")


def test_plain_dry_run_uses_the_retail_exe() -> None:
    _require_retail()
    result = _run("--windowed", "--dry-run")
    assert result.returncode == 0
    # dry-run prints the command to stdout
    assert "wine ./bugs.exe" in result.stdout
    assert "auto-hardware" not in result.stdout


def test_auto_hardware_dry_run_builds_cache_and_runs_patched_exe() -> None:
    _require_retail()
    result = _run("--auto-hardware", "--windowed", "--research", "--dry-run")
    assert result.returncode == 0, result.stderr
    # the printed command runs the cached patched exe, not ./bugs.exe
    assert str(CACHE_EXE) in result.stdout
    assert "wine ./bugs.exe" not in result.stdout
    # the launcher announced the auto-hardware build in the message stream
    assert AUTO_HARDWARE_SHA256 in result.stderr
    # the cache was built with the exact expected hash
    assert CACHE_EXE.is_file()
    assert (
        hashlib.sha256(CACHE_EXE.read_bytes()).hexdigest() == AUTO_HARDWARE_SHA256
    )
    # cwd stays the retail game dir (assets unchanged; only the exe differs)
    assert "work/copies/BUGS_PC-full-disc/PC/BUGS" in result.stdout


def test_auto_hardware_reuses_a_correct_cache() -> None:
    _require_retail()
    # First call ensures the cache exists; second must succeed reusing it.
    _run("--auto-hardware", "--dry-run")
    mtime_before = CACHE_EXE.stat().st_mtime
    result = _run("--auto-hardware", "--dry-run")
    assert result.returncode == 0
    # a correct cache is reused, not rebuilt
    assert CACHE_EXE.stat().st_mtime == mtime_before
