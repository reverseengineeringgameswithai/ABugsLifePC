from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
FROZEN = SCRIPTS / "frozen-capture.sh"


def _git_sandbox(tmp_path: Path) -> tuple[Path, Path]:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text("/work/copies/\n")
    copies = tmp_path / "work" / "copies" / "run"
    copies.mkdir(parents=True)
    (copies / "bugs.exe").write_bytes(b"MZ-dummy")
    return tmp_path, copies


def _capture_stub(tmp_path: Path, state_file: Path) -> Path:
    # $1 = target pid, $2 = output path. Records the target's process state
    # (should be 'T' while frozen), then writes a tiny fake PNG.
    stub = tmp_path / "capture-stub.sh"
    stub.write_text(
        "#!/usr/bin/env bash\n"
        'pid="$1"; out="$2"\n'
        f'awk \'{{print $3}}\' "/proc/$pid/stat" > "{state_file}" 2>/dev/null || echo "?" > "{state_file}"\n'
        'printf "\\x89PNG\\r\\n" > "$out"\n'
        "exit 0\n"
    )
    stub.chmod(0o755)
    return stub


def _failing_capture_stub(tmp_path: Path) -> Path:
    stub = tmp_path / "capture-fail.sh"
    stub.write_text("#!/usr/bin/env bash\nexit 7\n")
    stub.chmod(0o755)
    return stub


def _spawn_game(cwd: Path) -> subprocess.Popen:
    return subprocess.Popen(
        ["bugs.exe", "-c", "import time; time.sleep(30)"],
        executable=sys.executable, cwd=str(cwd),
    )


def _state(pid: int) -> str:
    try:
        return Path(f"/proc/{pid}/stat").read_text().split()[2]
    except (OSError, IndexError):
        return "?"


def _run(root: Path, pid: int, evidence: Path, capture_cmd: str, cwd_prefix: str, *extra):
    env = dict(os.environ)
    env["ABLPC_ROOT"] = str(root)
    return subprocess.run(
        ["bash", str(FROZEN), "--pid", str(pid), "--evidence-dir", str(evidence),
         "--exe-basename", "bugs.exe", "--loader-re", ".*",
         "--cwd-prefix", cwd_prefix, "--capture-cmd", capture_cmd, *extra],
        capture_output=True, text=True, env=env, timeout=60,
    )


def test_freeze_capture_resume(tmp_path: Path) -> None:
    root, copies = _git_sandbox(tmp_path)
    evidence = copies / "EXP-test" / "evidence"
    state_file = tmp_path / "state.txt"
    stub = _capture_stub(tmp_path, state_file)
    child = _spawn_game(copies)
    try:
        cmd = f"bash {stub} {child.pid} {{out}}"
        result = _run(root, child.pid, evidence, cmd, str(copies) + os.sep)
        assert result.returncode == 0, result.stdout + result.stderr

        # The target was frozen (state 'T') at capture time.
        assert state_file.read_text().strip() == "T"

        runs = list((root / "dynamic" / "wine").glob("RUN-FRZ-*"))
        assert len(runs) == 1
        metadata = json.loads((runs[0] / "metadata.json").read_text())
        assert metadata["status"] == "complete"
        assert metadata["frame_committed"] is False
        assert metadata["frame_sha256"] is not None
        assert metadata["capture_cmd"] == cmd

        # The frame lives in the ignored evidence dir.
        assert Path(metadata["frame_path"]).exists()
        assert str(evidence) in metadata["frame_path"]

        # The target was resumed.
        time.sleep(0.3)
        assert child.poll() is None
        assert _state(child.pid) != "T"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_capture_failure_still_resumes(tmp_path: Path) -> None:
    root, copies = _git_sandbox(tmp_path)
    evidence = copies / "EXP-test" / "evidence"
    stub = _failing_capture_stub(tmp_path)
    child = _spawn_game(copies)
    try:
        cmd = f"bash {stub} {{out}}"
        result = _run(root, child.pid, evidence, cmd, str(copies) + os.sep)
        assert result.returncode == 1
        # Despite the failure, the trap resumed the target.
        time.sleep(0.3)
        assert child.poll() is None
        assert _state(child.pid) != "T"
        metadata = json.loads(
            next((root / "dynamic" / "wine").glob("RUN-FRZ-*")).joinpath("metadata.json").read_text()
        )
        assert metadata["status"] == "capture-failed"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_missing_capture_backend_refuses(tmp_path: Path) -> None:
    root, copies = _git_sandbox(tmp_path)
    evidence = copies / "EXP-test" / "evidence"
    child = _spawn_game(copies)
    try:
        env = dict(os.environ)
        env["ABLPC_ROOT"] = str(root)
        result = subprocess.run(
            ["bash", str(FROZEN), "--pid", str(child.pid),
             "--evidence-dir", str(evidence), "--exe-basename", "bugs.exe",
             "--loader-re", ".*", "--cwd-prefix", str(copies) + os.sep],
            capture_output=True, text=True, env=env, timeout=60,
        )
        assert result.returncode == 3
        payload = json.loads(result.stdout)
        assert payload["reason"] == "capture_backend_not_established"
        # Nothing was frozen.
        assert _state(child.pid) != "T"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_ownership_refusal_no_freeze(tmp_path: Path) -> None:
    root, copies = _git_sandbox(tmp_path)
    evidence = copies / "EXP-test" / "evidence"
    stub = _failing_capture_stub(tmp_path)
    child = _spawn_game(copies)
    try:
        env = dict(os.environ)
        env["ABLPC_ROOT"] = str(root)
        result = subprocess.run(
            ["bash", str(FROZEN), "--pid", str(child.pid),
             "--evidence-dir", str(evidence), "--exe-basename", "bugs.exe",
             "--loader-re", "^/nonexistent/wine$", "--cwd-prefix", str(copies) + os.sep,
             "--capture-cmd", f"bash {stub} {{out}}"],
            capture_output=True, text=True, env=env, timeout=60,
        )
        assert result.returncode == 3
        payload = json.loads(result.stdout)
        assert payload["reason"] == "loader_mismatch"
        assert _state(child.pid) != "T"
    finally:
        child.terminate()
        child.wait(timeout=5)


def test_milestone_timeout_refuses(tmp_path: Path) -> None:
    root, copies = _git_sandbox(tmp_path)
    evidence = copies / "EXP-test" / "evidence"
    state_file = tmp_path / "state.txt"
    stub = _capture_stub(tmp_path, state_file)
    log = copies / "bugs.log"
    log.write_text("nothing interesting\n")
    child = _spawn_game(copies)
    try:
        cmd = f"bash {stub} {child.pid} {{out}}"
        result = _run(root, child.pid, evidence, cmd, str(copies) + os.sep,
                      "--milestone", "NEVER_APPEARS", "--milestone-timeout", "1",
                      "--log", str(log))
        assert result.returncode == 3
        payload = json.loads(result.stdout)
        assert payload["reason"] == "milestone_timeout"
        assert _state(child.pid) != "T"
        assert not list((root / "dynamic" / "wine").glob("RUN-FRZ-*"))
    finally:
        child.terminate()
        child.wait(timeout=5)
