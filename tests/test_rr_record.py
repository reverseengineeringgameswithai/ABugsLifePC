from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
RR_RECORD = SCRIPTS / "rr-record.sh"


def _make_sandbox(tmp_path: Path) -> tuple[Path, Path]:
    (tmp_path / "work" / "wine" / "baseline").mkdir(parents=True)
    copies = tmp_path / "work" / "copies" / "run"
    copies.mkdir(parents=True)
    exe = copies / "bugs.exe"
    exe.write_bytes(b"MZ-dummy")
    return tmp_path, exe


def _stub_rr(tmp_path: Path, log: Path) -> Path:
    stub = tmp_path / "rr-stub.sh"
    stub.write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        'if [ "${1:-}" = "--version" ]; then echo "rr version 9.9.9-stub"; exit 0; fi\n'
        f'printf "%s\\n" "$@" >> "{log}"\n'
        "# find -o argument and create the trace dir\n"
        "prev=\"\"\n"
        'for a in "$@"; do if [ "$prev" = "-o" ]; then mkdir -p "$a"; fi; prev="$a"; done\n'
        "exit 0\n"
    )
    stub.chmod(0o755)
    return stub


def _paranoid_file(tmp_path: Path, value: str) -> Path:
    pf = tmp_path / "paranoid"
    pf.write_text(value + "\n")
    return pf


def _run(exe: Path, root: Path, *, rr_bin: str, paranoid: Path,
         ntsync_dev: str = "/nonexistent/ntsync",
         extra_env=None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.update({
        "ABLPC_ROOT": str(root),
        "RR_BIN": rr_bin,
        "ABLPC_PERF_PARANOID_FILE": str(paranoid),
        # Point the ntsync preflight at an absent path so tests exercise the
        # rest of the flow regardless of the host's real /dev/ntsync.
        "ABLPC_NTSYNC_DEV": ntsync_dev,
    })
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        ["bash", str(RR_RECORD), "--", str(exe)],
        capture_output=True, text=True, env=env, timeout=60,
    )


def test_refuses_when_ntsync_present(tmp_path: Path) -> None:
    root, exe = _make_sandbox(tmp_path)
    log = tmp_path / "argv.log"
    stub = _stub_rr(tmp_path, log)
    paranoid = _paranoid_file(tmp_path, "1")
    fake_ntsync = tmp_path / "ntsync"
    fake_ntsync.write_text("")  # present -> should refuse
    result = _run(exe, root, rr_bin=str(stub), paranoid=paranoid,
                  ntsync_dev=str(fake_ntsync))
    assert result.returncode == 3, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["reason"] == "ntsync_present"
    assert "modprobe -r ntsync" in payload["remedy"]
    # Refusal happens before any run dir is created.
    assert not list((root / "dynamic" / "wine").glob("RUN-RR-*"))


def test_refuses_when_paranoid_too_high(tmp_path: Path) -> None:
    root, exe = _make_sandbox(tmp_path)
    log = tmp_path / "argv.log"
    stub = _stub_rr(tmp_path, log)
    paranoid = _paranoid_file(tmp_path, "2")
    result = _run(exe, root, rr_bin=str(stub), paranoid=paranoid)
    assert result.returncode == 3, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["refused"] is True
    assert payload["reason"] == "perf_event_paranoid"
    assert payload["observed"] == 2
    # No run dir created on refusal.
    assert not list((root / "dynamic" / "wine").glob("RUN-RR-*"))


def test_refuses_when_rr_missing(tmp_path: Path) -> None:
    root, exe = _make_sandbox(tmp_path)
    paranoid = _paranoid_file(tmp_path, "1")
    result = _run(exe, root, rr_bin="/nonexistent/rr", paranoid=paranoid)
    assert result.returncode == 3
    payload = json.loads(result.stdout)
    assert payload["reason"] == "rr_missing"


def test_happy_path_records_and_writes_metadata(tmp_path: Path) -> None:
    root, exe = _make_sandbox(tmp_path)
    log = tmp_path / "argv.log"
    stub = _stub_rr(tmp_path, log)
    paranoid = _paranoid_file(tmp_path, "1")
    result = _run(exe, root, rr_bin=str(stub), paranoid=paranoid)
    assert result.returncode == 0, result.stdout + result.stderr

    runs = list((root / "dynamic" / "wine").glob("RUN-RR-*"))
    assert len(runs) == 1
    metadata = json.loads((runs[0] / "metadata.json").read_text())
    assert metadata["recorder"] == "rr"
    assert metadata["recorder_version"] == "rr version 9.9.9-stub"
    assert metadata["forced_env"] == {
        "LIBGL_ALWAYS_SOFTWARE": "1", "WINEESYNC": "0", "WINEFSYNC": "0"
    }
    assert metadata["perf_event_paranoid"] == 1
    assert metadata["trace_dir"].startswith("work/rr/RUN-RR-")
    assert metadata["status"] == "complete"
    assert metadata["exit_status"] == 0

    # rr was invoked with `record -o <trace> wine <exe>`.
    argv = log.read_text()
    assert "record" in argv
    assert "-o" in argv
    assert "wine" in argv
    assert str(exe) in argv

    # The trace lives under the git-ignored work/rr tree.
    trace = root / metadata["trace_dir"]
    assert trace.exists()


def test_refuses_originals_path(tmp_path: Path) -> None:
    root, exe = _make_sandbox(tmp_path)
    originals = root / "originals"
    originals.mkdir(parents=True, exist_ok=True)
    bad = originals / "bugs.exe"
    bad.write_bytes(b"MZ")
    log = tmp_path / "argv.log"
    stub = _stub_rr(tmp_path, log)
    paranoid = _paranoid_file(tmp_path, "1")
    env = dict(os.environ)
    env.update({
        "ABLPC_ROOT": str(root),
        "RR_BIN": str(stub),
        "ABLPC_PERF_PARANOID_FILE": str(paranoid),
        "ABLPC_NTSYNC_DEV": "/nonexistent/ntsync",
    })
    result = subprocess.run(
        ["bash", str(RR_RECORD), "--", str(bad)],
        capture_output=True, text=True, env=env, timeout=60,
    )
    assert result.returncode == 2
    assert "originals" in result.stderr
