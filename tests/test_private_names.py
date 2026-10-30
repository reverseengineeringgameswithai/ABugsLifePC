"""scripts/git-hooks/private_names.py: every encoding is caught, reports stay redacted."""
from __future__ import annotations

import base64
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts/git-hooks/private_names.py"
NAME = "zorbelquin"  # synthetic; never a real name


def git(repo: Path, *args: str, data: bytes | None = None) -> str:
    env = {**os.environ, "GIT_AUTHOR_NAME": "Tester", "GIT_AUTHOR_EMAIL": "t@example.invalid",
           "GIT_COMMITTER_NAME": "Tester", "GIT_COMMITTER_EMAIL": "t@example.invalid"}
    return subprocess.run(["git", *args], cwd=repo, input=data, capture_output=True,
                          check=True, env=env).stdout.decode()


def check(repo: Path, *args: str, stdin: str = "") -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CHECKER), *args], cwd=repo, input=stdin.encode(),
                          capture_output=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q", "-b", "main")
    (tmp_path / ".git/info/private-names").write_text(f"# local list\n{NAME}\n")
    (tmp_path / "clean.txt").write_text("nothing to see\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "clean")
    return tmp_path


def commit_bytes(repo: Path, data: bytes, path: str = "leak.bin", message: str = "add") -> str:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD").strip()


def b64(text: bytes, urlsafe: bool = False) -> bytes:
    return (base64.urlsafe_b64encode if urlsafe else base64.b64encode)(text)


ENCODINGS = {
    "plain mixed case": f"path /home/{NAME.capitalize()}/x".encode(),
    "plain upper": NAME.upper().encode(),
    "utf-16le": f"C:\\users\\{NAME}".encode("utf-16-le"),
    "utf-16be": f"C:\\users\\{NAME.upper()}".encode("utf-16-be"),
    "hex lower": NAME.encode().hex().encode(),
    "hex spaced upper": " ".join(f"{b:02X}" for b in NAME.encode()).encode(),
    "hex 0x prefixed": ",".join(f"0x{b:02x}" for b in NAME.encode()).encode(),
    "base64 align 0": b64(f"{NAME}/rest".encode()),
    "base64 align 1": b64(f"a{NAME}/rest".encode()),
    "base64 align 2": b64(f"ab{NAME.capitalize()}/rest".encode()),
    "base64 urlsafe": b64(f"ab/{NAME.upper()}??>>".encode(), urlsafe=True),
}


@pytest.mark.parametrize("kind", sorted(ENCODINGS))
def test_history_finds_every_encoding(repo: Path, kind: str) -> None:
    commit_bytes(repo, b"header\x00\x01" + ENCODINGS[kind] + b"\x02trailer")
    result = check(repo, "history")
    assert result.returncode == 1, (kind, result.stderr)
    assert b"content: leak.bin" in result.stderr


def test_clean_history_passes(repo: Path) -> None:
    assert check(repo, "history").returncode == 0


def test_path_message_and_identity_are_checked_and_redacted(repo: Path) -> None:
    commit_bytes(repo, b"ok\n", path=f"notes/{NAME}-log.txt", message=f"from {NAME}")
    result = check(repo, "history")
    assert result.returncode == 1
    assert b"path: notes/<private>-log.txt" in result.stderr
    assert b"message or identity" in result.stderr
    assert NAME.encode() not in result.stderr.lower()


def test_staged_mode_checks_the_index(repo: Path) -> None:
    (repo / "staged.txt").write_text(f"by {NAME}\n")
    git(repo, "add", "staged.txt")
    result = check(repo, "staged")
    assert result.returncode == 1
    assert b"staged content: staged.txt" in result.stderr


def test_push_mode_checks_only_the_pushed_range(repo: Path) -> None:
    base = git(repo, "rev-parse", "HEAD").strip()
    head = commit_bytes(repo, NAME.encode())
    leaked = check(repo, "push", stdin=f"refs/heads/main {head} refs/heads/main {base}\n")
    assert leaked.returncode == 1
    clean = check(repo, "push", stdin=f"refs/heads/main {base} refs/heads/main {'0' * 40}\n")
    assert clean.returncode == 0


def test_pending_mode_ignores_commits_already_on_a_remote(repo: Path) -> None:
    head = commit_bytes(repo, NAME.encode())
    assert check(repo, "pending").returncode == 1
    git(repo, "update-ref", "refs/remotes/origin/main", head)
    assert check(repo, "pending").returncode == 0


def test_missing_list_fails_closed_only_when_required(repo: Path) -> None:
    (repo / ".git/info/private-names").unlink()
    commit_bytes(repo, NAME.encode())
    assert check(repo, "history").returncode == 0
    assert check(repo, "history", "--require-list").returncode == 3


def test_usage_error(repo: Path) -> None:
    assert check(repo, "everything").returncode == 2
