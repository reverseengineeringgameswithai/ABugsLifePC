"""Tests for scripts/install-git-hooks.sh and the tracked pre-commit hook.

Every installation is exercised against a throwaway `git init` repository in
`tmp_path`; nothing here touches the real repository's git configuration.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install-git-hooks.sh"
HOOK = ROOT / "scripts" / "git-hooks" / "pre-commit"
VENV = ROOT / ".venv"
HOOKS_REL = "scripts/git-hooks"


def _env(**extra: str) -> dict[str, str]:
    """Environment for a throwaway repository run.

    `ABLPC_ROOT` is cleared so a copied gate script resolves the throwaway
    tree from its own location rather than the real repository.
    """

    env = {key: value for key, value in os.environ.items() if key != "ABLPC_ROOT"}
    env.update(extra)
    return env


def _throwaway_repo(tmp_path: Path) -> Path:
    """A fresh repository holding copies of the installer and its hooks.

    The two gate scripts the hook calls are copied as well so the hook can run
    to completion against the throwaway tree (each resolves its own root from
    its file location, and an empty tree is a clean subject for both).
    """

    repo = tmp_path / "repo"
    (repo / "scripts" / "git-hooks").mkdir(parents=True)
    shutil.copy2(INSTALLER, repo / "scripts" / "install-git-hooks.sh")
    shutil.copy2(HOOK, repo / "scripts" / "git-hooks" / "pre-commit")
    for gate in ("vault-lint.py", "audit-tracked-files.py"):
        shutil.copy2(ROOT / "scripts" / gate, repo / "scripts" / gate)
    if VENV.is_dir():
        # The hook prefers `<root>/.venv/bin/python`; link the project venv so
        # the throwaway tree runs the gates on the pinned interpreter instead
        # of whatever `python3` the host happens to provide.
        (repo / ".venv").symlink_to(VENV, target_is_directory=True)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    return repo


def _install(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(repo / "scripts" / "install-git-hooks.sh"), *args],
        cwd=repo,
        capture_output=True,
        text=True,
        timeout=30,
        env=_env(),
    )


def _hooks_path(repo: Path) -> str | None:
    result = subprocess.run(
        ["git", "config", "--local", "--get", "core.hooksPath"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def test_hook_script_is_executable_and_syntactically_valid() -> None:
    assert os.access(HOOK, os.X_OK), "scripts/git-hooks/pre-commit must be executable"
    assert os.access(INSTALLER, os.X_OK), "installer must be executable"
    for script in (HOOK, INSTALLER):
        result = subprocess.run(
            ["bash", "-n", str(script)], capture_output=True, text=True
        )
        assert result.returncode == 0, f"{script}: {result.stderr}"


def test_help_prints_usage_and_exits_two() -> None:
    result = subprocess.run(
        [str(INSTALLER), "--help"], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 2
    assert "core.hooksPath" in result.stderr
    assert "--uninstall" in result.stderr


def test_unknown_option_is_a_usage_error(tmp_path: Path) -> None:
    repo = _throwaway_repo(tmp_path)
    result = _install(repo, "--not-an-option")
    assert result.returncode == 2, result.stdout + result.stderr
    assert _hooks_path(repo) is None


def test_install_sets_hooks_path_and_is_idempotent(tmp_path: Path) -> None:
    repo = _throwaway_repo(tmp_path)
    assert _hooks_path(repo) is None

    first = _install(repo)
    assert first.returncode == 0, first.stdout + first.stderr
    assert _hooks_path(repo) == HOOKS_REL
    assert "pre-commit" in first.stdout
    assert "--no-verify" in first.stdout

    second = _install(repo)
    assert second.returncode == 0, second.stdout + second.stderr
    assert _hooks_path(repo) == HOOKS_REL
    assert "already installed" in second.stdout


def test_uninstall_restores_the_default_and_is_idempotent(tmp_path: Path) -> None:
    repo = _throwaway_repo(tmp_path)
    assert _install(repo).returncode == 0

    removed = _install(repo, "--uninstall")
    assert removed.returncode == 0, removed.stdout + removed.stderr
    assert _hooks_path(repo) is None

    again = _install(repo, "--uninstall")
    assert again.returncode == 0, again.stdout + again.stderr
    assert "nothing to remove" in again.stdout
    assert _hooks_path(repo) is None


def test_refuses_to_replace_a_foreign_hooks_path(tmp_path: Path) -> None:
    repo = _throwaway_repo(tmp_path)
    subprocess.run(
        ["git", "config", "--local", "core.hooksPath", "other/hooks"],
        cwd=repo,
        check=True,
    )

    blocked = _install(repo)
    assert blocked.returncode == 3, blocked.stdout + blocked.stderr
    assert "conflicting_hooks_path" in blocked.stdout
    assert _hooks_path(repo) == "other/hooks"

    # Uninstall must not remove configuration this installer did not create.
    blocked_removal = _install(repo, "--uninstall")
    assert blocked_removal.returncode == 3, (
        blocked_removal.stdout + blocked_removal.stderr
    )
    assert "foreign_hooks_path" in blocked_removal.stdout
    assert _hooks_path(repo) == "other/hooks"


def test_refuses_when_the_hook_is_not_executable(tmp_path: Path) -> None:
    repo = _throwaway_repo(tmp_path)
    (repo / "scripts" / "git-hooks" / "pre-commit").chmod(0o644)

    result = _install(repo)
    assert result.returncode == 3, result.stdout + result.stderr
    assert "hook_not_executable" in result.stdout
    assert _hooks_path(repo) is None


def test_installed_hook_runs_and_blocks_a_bad_commit(tmp_path: Path) -> None:
    """End-to-end: the hook must actually be invoked by `git commit`."""

    repo = _throwaway_repo(tmp_path)
    assert _install(repo).returncode == 0
    env = _env(
        GIT_AUTHOR_NAME="Test",
        GIT_AUTHOR_EMAIL="test@example.invalid",
        GIT_COMMITTER_NAME="Test",
        GIT_COMMITTER_EMAIL="test@example.invalid",
    )

    def commit(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "commit", "-m", "subject", *args],
            cwd=repo,
            capture_output=True,
            text=True,
            env=env,
            timeout=180,
        )

    # A clean tree passes every gate, and the hook reports what it ran.
    (repo / "fine.py").write_text("VALUE = 1\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, env=env)
    clean = commit()
    assert clean.returncode == 0, clean.stdout + clean.stderr
    assert "pre-commit: ran" in clean.stdout + clean.stderr
    assert "audit-tracked-files" in clean.stdout + clean.stderr

    # A staged Python file with a syntax error must be rejected by compileall.
    (repo / "broken.py").write_text("def oops(:\n", encoding="utf-8")
    subprocess.run(["git", "add", "broken.py"], cwd=repo, check=True, env=env)
    blocked = commit()
    assert blocked.returncode != 0, blocked.stdout + blocked.stderr
    assert "FAIL  compileall" in blocked.stdout + blocked.stderr

    # --no-verify must still get through.
    bypassed = commit("--no-verify")
    assert bypassed.returncode == 0, bypassed.stdout + bypassed.stderr
