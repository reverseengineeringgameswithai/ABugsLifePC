from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
WINE_CAPTURE = SCRIPTS / "wine-capture.sh"


def _sandbox(tmp_path: Path) -> tuple[Path, Path, Path]:
    for name in ("baseline", "instrumented"):
        (tmp_path / "work" / "wine" / name).mkdir(parents=True)
    copies = tmp_path / "work" / "copies" / "run"
    copies.mkdir(parents=True)
    exe = copies / "bugs.exe"
    exe.write_bytes(b"MZ-dummy")
    bindir = tmp_path / "bin"
    bindir.mkdir()
    return tmp_path, exe, bindir


def _stub_wine(bindir: Path, log: Path) -> None:
    wine = bindir / "wine"
    wine.write_text(
        "#!/usr/bin/env bash\n"
        f'printf "%s\\n" "$*" >> "{log}"\n'
        'case "${1:-}" in\n'
        '  --version) echo "wine-11.0 (stub)"; exit 0 ;;\n'
        '  reg)\n'
        '    if [ "${2:-}" = "query" ]; then exit 1; fi\n'  # value absent
        '    exit 0 ;;\n'
        '  *) exit 0 ;;\n'
        'esac\n'
    )
    wine.chmod(0o755)


def _run(exe: Path, root: Path, bindir: Path, *args) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["ABLPC_ROOT"] = str(root)
    env["PATH"] = f"{bindir}{os.pathsep}{env['PATH']}"
    return subprocess.run(
        ["bash", str(WINE_CAPTURE), *args, "--", str(exe)],
        capture_output=True, text=True, env=env, timeout=60,
    )


def _only_run(root: Path) -> Path:
    runs = list((root / "dynamic" / "wine").glob("RUN-WINE-*"))
    assert len(runs) == 1, runs
    return runs[0]


def test_plain_run_is_backward_compatible(tmp_path: Path) -> None:
    root, exe, bindir = _sandbox(tmp_path)
    log = tmp_path / "wine.log"
    _stub_wine(bindir, log)
    result = _run(exe, root, bindir)
    assert result.returncode == 0, result.stderr

    metadata = json.loads((_only_run(root) / "metadata.json").read_text())
    # Existing keys unchanged.
    for key in ("run_id", "executable_sha256", "wine_debug_channels",
                "syscall_capture", "status", "environment_version"):
        assert key in metadata
    # No new keys on a plain run.
    for key in ("relay_include", "relay_exclude", "relay_prior_include",
                "relay_registry_restored", "file_trace"):
        assert key not in metadata


def test_file_trace_appends_channel(tmp_path: Path) -> None:
    root, exe, bindir = _sandbox(tmp_path)
    log = tmp_path / "wine.log"
    _stub_wine(bindir, log)
    result = _run(exe, root, bindir, "--file-trace")
    assert result.returncode == 0, result.stderr

    metadata = json.loads((_only_run(root) / "metadata.json").read_text())
    assert metadata["file_trace"] is True
    assert "+file" in metadata["wine_debug_channels"]
    assert "relay_include" not in metadata


def test_relay_refused_on_baseline(tmp_path: Path) -> None:
    root, exe, bindir = _sandbox(tmp_path)
    log = tmp_path / "wine.log"
    _stub_wine(bindir, log)
    result = _run(exe, root, bindir, "--relay-include", "ntdll.*")
    assert result.returncode == 2
    assert "baseline" in result.stderr
    assert not list((root / "dynamic" / "wine").glob("RUN-WINE-*"))


def test_relay_requires_relay_channel(tmp_path: Path) -> None:
    root, exe, bindir = _sandbox(tmp_path)
    log = tmp_path / "wine.log"
    _stub_wine(bindir, log)
    result = _run(exe, root, bindir, "--prefix", "instrumented",
                  "--relay-include", "ntdll.*")
    assert result.returncode == 2
    assert "+relay" in result.stderr


def test_relay_happy_path_sets_and_restores(tmp_path: Path) -> None:
    root, exe, bindir = _sandbox(tmp_path)
    log = tmp_path / "wine.log"
    _stub_wine(bindir, log)
    result = _run(exe, root, bindir, "--prefix", "instrumented", "--deep",
                  "--relay-include", "ntdll.RtlEnterCriticalSection")
    assert result.returncode == 0, result.stderr

    metadata = json.loads((_only_run(root) / "metadata.json").read_text())
    assert metadata["relay_include"] == "ntdll.RtlEnterCriticalSection"
    assert metadata["relay_exclude"] is None
    assert metadata["relay_prior_include"] is None
    # The EXIT trap restored the registry and patched metadata.
    assert metadata["relay_registry_restored"] is True

    text = log.read_text()
    assert "reg add HKCU\\Software\\Wine\\Debug /v RelayInclude" in text
    assert "reg delete HKCU\\Software\\Wine\\Debug /v RelayInclude" in text
