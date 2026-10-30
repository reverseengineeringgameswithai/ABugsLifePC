from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
MEMSNAP = SCRIPTS / "memory-snapshot.sh"


def _git_sandbox(tmp_path: Path) -> tuple[Path, Path]:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text("/work/copies/\n")
    copies = tmp_path / "work" / "copies" / "run"
    copies.mkdir(parents=True)
    exe = copies / "bugs.exe"
    exe.write_bytes(b"MZ-dummy")
    return tmp_path, copies


def _stub_gcore(tmp_path: Path, *, succeed: bool = True) -> Path:
    stub = tmp_path / "gcore-stub.sh"
    if succeed:
        body = (
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            'out=""; pid=""; prev=""\n'
            'for a in "$@"; do if [ "$prev" = "-o" ]; then out="$a"; fi; pid="$a"; prev="$a"; done\n'
            'printf "FAKECORE" > "${out}.${pid}"\n'
            "exit 0\n"
        )
    else:
        body = "#!/usr/bin/env bash\nexit 1\n"
    stub.write_text(body)
    stub.chmod(0o755)
    return stub


def _spawn_game(cwd: Path) -> subprocess.Popen:
    return subprocess.Popen(
        ["bugs.exe", "-c", "import time; time.sleep(30)"],
        executable=sys.executable, cwd=str(cwd),
    )


def _run(root: Path, pid: int, evidence: Path, gcore: Path, cwd_prefix: str):
    env = dict(os.environ)
    env["ABLPC_ROOT"] = str(root)
    env["GCORE_BIN"] = str(gcore)
    return subprocess.run(
        ["bash", str(MEMSNAP), "--pid", str(pid), "--evidence-dir", str(evidence),
         "--exe-basename", "bugs.exe", "--loader-re", ".*",
         "--cwd-prefix", cwd_prefix],
        capture_output=True, text=True, env=env, timeout=60,
    )


def test_snapshot_happy_path(tmp_path: Path) -> None:
    root, copies = _git_sandbox(tmp_path)
    evidence = copies / "EXP-test" / "evidence"
    gcore = _stub_gcore(tmp_path, succeed=True)
    child = _spawn_game(copies)
    try:
        result = _run(root, child.pid, evidence, gcore, str(copies) + os.sep)
        assert result.returncode == 0, result.stdout + result.stderr
        runs = list((root / "dynamic" / "wine").glob("RUN-CORE-*"))
        assert len(runs) == 1
        metadata = json.loads((runs[0] / "metadata.json").read_text())
        assert metadata["status"] == "complete"
        assert metadata["core_committed"] is False
        assert metadata["core_sha256"] is not None
        # The core landed in the ignored evidence dir, not the RUN dir.
        assert metadata["core_path"].startswith(str(evidence))
        assert (runs[0] / "maps.txt").exists()
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_refuses_non_ignored_evidence_dir(tmp_path: Path) -> None:
    root, copies = _git_sandbox(tmp_path)
    # A committed-tree path (not under work/copies) is not git-ignored.
    evidence = root / "not-ignored" / "evidence"
    gcore = _stub_gcore(tmp_path, succeed=True)
    child = _spawn_game(copies)
    try:
        result = _run(root, child.pid, evidence, gcore, str(copies) + os.sep)
        assert result.returncode == 3
        payload = json.loads(result.stdout)
        assert payload["reason"] == "evidence_dir_not_ignored"
        assert not list((root / "dynamic" / "wine").glob("RUN-CORE-*"))
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_ownership_refusal_sends_no_gcore(tmp_path: Path) -> None:
    root, copies = _git_sandbox(tmp_path)
    evidence = copies / "EXP-test" / "evidence"
    gcore = _stub_gcore(tmp_path, succeed=True)
    child = _spawn_game(copies)
    try:
        env = dict(os.environ)
        env["ABLPC_ROOT"] = str(root)
        env["GCORE_BIN"] = str(gcore)
        result = subprocess.run(
            ["bash", str(MEMSNAP), "--pid", str(child.pid),
             "--evidence-dir", str(evidence), "--exe-basename", "bugs.exe",
             "--loader-re", "^/nonexistent/wine$",
             "--cwd-prefix", str(copies) + os.sep],
            capture_output=True, text=True, env=env, timeout=60,
        )
        assert result.returncode == 3
        payload = json.loads(result.stdout)
        assert payload["reason"] in ("loader_mismatch",)
    finally:
        child.terminate()
        child.wait(timeout=5)
