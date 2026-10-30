from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
APITRACE = SCRIPTS / "apitrace-capture.sh"


def _sandbox(tmp_path: Path) -> tuple[Path, Path, Path]:
    (tmp_path / "work" / "wine" / "baseline").mkdir(parents=True)
    copies = tmp_path / "work" / "copies" / "run"
    copies.mkdir(parents=True)
    exe = copies / "bugs.exe"
    exe.write_bytes(b"MZ-dummy")
    wrappers = tmp_path / "wrappers"
    wrappers.mkdir()
    return tmp_path, exe, wrappers


def _stub_apitrace(tmp_path: Path, log: Path) -> Path:
    # Emulates `apitrace version` and `apitrace trace --api gl --output T -- ...`,
    # producing two trace files to exercise multi-trace hashing.
    stub = tmp_path / "apitrace-stub.sh"
    stub.write_text(
        "#!/usr/bin/env bash\n"
        'if [ "${1:-}" = "version" ]; then echo "apitrace 11.0-stub"; exit 0; fi\n'
        f'printf "%s\\n" "$@" >> "{log}"\n'
        'out=""; prev=""\n'
        'for a in "$@"; do if [ "$prev" = "--output" ]; then out="$a"; fi; prev="$a"; done\n'
        'if [ -n "$out" ]; then printf "TRACE" > "$out"; printf "TRACE1" > "${out%.trace}.1.trace"; fi\n'
        "exit 0\n"
    )
    stub.chmod(0o755)
    return stub


def _run(exe: Path, root: Path, apitrace: str, wrappers: Path,
         api: str | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["ABLPC_ROOT"] = str(root)
    env["APITRACE_BIN"] = apitrace
    env["APITRACE_WRAPPER_DIR"] = str(wrappers)
    argv = ["bash", str(APITRACE)]
    if api:
        argv += ["--api", api]
    argv += ["--", str(exe)]
    return subprocess.run(argv, capture_output=True, text=True, env=env, timeout=60)


def test_wrapper_names_per_api(tmp_path: Path) -> None:
    # Regression: GL uses glxtrace.so but EGL uses egltrace.so (not eglxtrace.so).
    root, exe, wrappers = _sandbox(tmp_path)
    log = tmp_path / "argv.log"
    stub = _stub_apitrace(tmp_path, log)
    # Only egltrace.so present: gl must refuse, egl must proceed.
    (wrappers / "egltrace.so").write_bytes(b"stub")
    gl = _run(exe, root, str(stub), wrappers, api="gl")
    assert gl.returncode == 3 and json.loads(gl.stdout)["reason"] == "wrapper_missing"
    egl = _run(exe, root, str(stub), wrappers, api="egl")
    assert egl.returncode == 0, egl.stdout + egl.stderr
    meta = json.loads(next((root / "dynamic" / "wine").glob("RUN-APITRACE-*")).joinpath("metadata.json").read_text())
    assert meta["api"] == "egl"
    assert meta["wrapper_path"].endswith("egltrace.so")


def test_wrapper_missing_refusal(tmp_path: Path) -> None:
    root, exe, wrappers = _sandbox(tmp_path)
    log = tmp_path / "argv.log"
    stub = _stub_apitrace(tmp_path, log)
    # wrappers dir is empty → glxtrace.so absent.
    result = _run(exe, root, str(stub), wrappers)
    assert result.returncode == 3
    payload = json.loads(result.stdout)
    assert payload["reason"] == "wrapper_missing"


def test_happy_path_hashes_all_traces(tmp_path: Path) -> None:
    root, exe, wrappers = _sandbox(tmp_path)
    (wrappers / "glxtrace.so").write_bytes(b"\x7fELF-stub")
    log = tmp_path / "argv.log"
    stub = _stub_apitrace(tmp_path, log)
    result = _run(exe, root, str(stub), wrappers)
    assert result.returncode == 0, result.stdout + result.stderr

    runs = list((root / "dynamic" / "wine").glob("RUN-APITRACE-*"))
    assert len(runs) == 1
    metadata = json.loads((runs[0] / "metadata.json").read_text())
    assert metadata["tracer"] == "apitrace"
    assert metadata["tracer_version"] == "apitrace 11.0-stub"
    assert metadata["api"] == "gl"
    # Both the primary and the .1 trace are hashed.
    assert len(metadata["traces"]) == 2
    for entry in metadata["traces"]:
        assert entry["path"].startswith("work/apitrace/RUN-APITRACE-")
        assert len(entry["sha256"]) == 64

    argv = log.read_text()
    assert "trace" in argv
    assert "--api" in argv
    assert "gl" in argv


def test_apitrace_missing_refusal(tmp_path: Path) -> None:
    root, exe, wrappers = _sandbox(tmp_path)
    (wrappers / "glxtrace.so").write_bytes(b"stub")
    result = _run(exe, root, "/nonexistent/apitrace", wrappers)
    assert result.returncode == 3
    payload = json.loads(result.stdout)
    assert payload["reason"] == "apitrace_missing"
