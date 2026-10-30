from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess

import pytest

from reimplementation.ablpc.release import (
    INSTALL_STATE_NAME,
    RELEASE_MANIFEST_NAME,
    RELEASE_SPEC_RELATIVE,
    ReleaseError,
    build_release,
    current_release,
    install_release,
    load_release_spec,
    rollback_release,
    verify_release,
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _spec(version: str) -> dict[str, object]:
    release_id = f"ablpc-toolkit-v{version}"
    return {
        "release_schema_version": 1,
        "release_id": release_id,
        "toolkit_version": version,
        "archive_name": f"{release_id}.tar",
        "package_root": release_id,
        "source_date_epoch": 1786737600,
        "package_files": [RELEASE_SPEC_RELATIVE.as_posix()],
        "supported_inputs": {
            "disc_iso_sha256": _sha256(b"disc"),
            "executable_sha256": _sha256(b"exe"),
            "manifest_schema_versions": [1, 2],
            "compatibility_statements": {"metadata/v0.2.json": _sha256(b"statement")},
            "data_hashes": {"CD/LEVEL07/LEVEL1.DAT": _sha256(b"level")},
            "level_dat_corpus_count": 21,
        },
        "primary_environment": {
            "os": "Linux",
            "distribution": "Fedora Linux 44 (Workstation Edition)",
            "kernel": "7.0.11-200.fc44.x86_64",
            "architecture": "x86_64",
            "python": "3.14.6",
            "wine": "wine-11.0 (Staging)",
            "gamescope_package": "gamescope-3.16.25-1.fc44.x86_64",
            "renderer": "Direct3D",
            "game_surface": "640x480x16",
            "presentation": "fit/nearest",
        },
        "smoke_matrix": [
            {
                "case_id": "training",
                "scope": "Training",
                "manifest": "mods/training.json",
                "workflow": "stage-launch-dry-run-restore",
            },
            {
                "case_id": "level01",
                "scope": "Level 01",
                "manifest": "mods/level01.json",
                "workflow": "stage-launch-dry-run-restore",
            },
        ],
        "limitations": ["Windows is untested."],
    }


def _write_spec(root: Path, version: str) -> Path:
    path = root.joinpath(*RELEASE_SPEC_RELATIVE.parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_spec(version), indent=2) + "\n", encoding="utf-8")
    return path


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def _commit(root: Path, message: str) -> None:
    _git(root, "add", ".")
    _git(
        root,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-m",
        message,
    )


def _repo(tmp_path: Path, version: str = "0.9.0") -> tuple[Path, Path]:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    spec = _write_spec(root, version)
    _commit(root, version)
    return root, spec


def _snapshot(root: Path) -> dict[str, tuple[object, ...]]:
    if not root.exists() and not root.is_symlink():
        return {}
    snapshot: dict[str, tuple[object, ...]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        metadata = path.lstat()
        mode = stat.S_IMODE(metadata.st_mode)
        if stat.S_ISLNK(metadata.st_mode):
            snapshot[relative] = ("symlink", mode, os.readlink(path))
        elif stat.S_ISDIR(metadata.st_mode):
            snapshot[relative] = ("directory", mode)
        elif stat.S_ISREG(metadata.st_mode):
            snapshot[relative] = ("file", mode, path.read_bytes())
        else:
            snapshot[relative] = ("other", metadata.st_mode)
    return snapshot


def _copy_exact_release_repo(tmp_path: Path) -> tuple[Path, Path]:
    source_root = Path(__file__).resolve().parents[1]
    source_spec = source_root.joinpath(*RELEASE_SPEC_RELATIVE.parts)
    spec = load_release_spec(source_spec)
    root = tmp_path / "exact-release-repo"
    root.mkdir()
    _git(root, "init", "-q")
    for item in spec["package_files"]:
        source = source_root.joinpath(*Path(item).parts)
        destination = root.joinpath(*Path(item).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    _commit(root, "exact release sources")
    return root, root.joinpath(*RELEASE_SPEC_RELATIVE.parts)


def test_release_build_is_byte_reproducible_and_verifiable(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    first = build_release(spec, root, tmp_path / "a")
    second = build_release(spec, root, tmp_path / "b")
    assert first["archive_sha256"] == second["archive_sha256"]
    assert first["source_tree_sha256"] == second["source_tree_sha256"]
    assert first["file_count"] == 1
    assert first["archive"].read_bytes() == second["archive"].read_bytes()
    verified = verify_release(first["archive"])
    assert verified["release_id"] == "ablpc-toolkit-v0.9.0"
    assert verified["file_count"] == 1


def test_release_build_rejects_dirty_or_untracked_source(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    spec.write_text(spec.read_text(encoding="utf-8") + " ", encoding="utf-8")
    with pytest.raises(ReleaseError, match="working tree"):
        build_release(spec, root, tmp_path / "out")

    _git(root, "restore", ".")
    value = json.loads(spec.read_text(encoding="utf-8"))
    value["package_files"].append("untracked.txt")
    value["package_files"].sort()
    spec.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    _git(root, "add", spec.relative_to(root).as_posix())
    _git(
        root,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-m",
        "spec selects untracked",
    )
    (root / "untracked.txt").write_text("asset-free", encoding="utf-8")
    with pytest.raises(ReleaseError, match="not tracked"):
        build_release(spec, root, tmp_path / "out")


def test_release_install_migrate_and_rollback(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    old = build_release(spec, root, tmp_path / "old")

    _write_spec(root, "1.0.0")
    _commit(root, "1.0.0")
    new = build_release(spec, root, tmp_path / "new")

    install_root = tmp_path / "install"
    old_result = install_release(old["archive"], install_root)
    assert old_result["current"] == "ablpc-toolkit-v0.9.0"
    with pytest.raises(ReleaseError, match="no prior release"):
        rollback_release(install_root)
    new_result = install_release(new["archive"], install_root)
    assert new_result["rollback"] == ["ablpc-toolkit-v0.9.0"]
    assert current_release(install_root)["current"] == "ablpc-toolkit-v1.0.0"
    rolled_back = rollback_release(install_root)
    assert rolled_back["previous"] == "ablpc-toolkit-v1.0.0"
    assert rolled_back["current"] == "ablpc-toolkit-v0.9.0"
    assert (install_root / "releases" / "ablpc-toolkit-v1.0.0").is_dir()
    assert current_release(install_root)["current"] == "ablpc-toolkit-v0.9.0"


def test_failed_archive_and_empty_rollback_preserve_state(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    built = build_release(spec, root, tmp_path / "out")
    install_root = tmp_path / "install"
    install_release(built["archive"], install_root)
    before = _snapshot(install_root)

    corrupt = tmp_path / "corrupt.tar"
    data = bytearray(built["archive"].read_bytes())
    data[1024] ^= 0xFF
    corrupt.write_bytes(data)
    with pytest.raises(ReleaseError):
        install_release(corrupt, install_root)
    assert _snapshot(install_root) == before

    appended = tmp_path / "appended.tar"
    appended.write_bytes(built["archive"].read_bytes() + b"undeclared trailing bytes")
    with pytest.raises(ReleaseError, match="exact canonical tar encoding"):
        verify_release(appended)
    with pytest.raises(ReleaseError, match="exact canonical tar encoding"):
        install_release(appended, install_root)
    assert _snapshot(install_root) == before

    with pytest.raises(ReleaseError, match="no prior release"):
        rollback_release(install_root)
    assert _snapshot(install_root) == before


def test_tampered_prior_release_refuses_rollback_without_state_change(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    old = build_release(spec, root, tmp_path / "old")
    _write_spec(root, "1.0.0")
    _commit(root, "1.0.0")
    new = build_release(spec, root, tmp_path / "new")
    install_root = tmp_path / "install"
    install_release(old["archive"], install_root)
    install_release(new["archive"], install_root)

    old_spec = install_root.joinpath(
        "releases", "ablpc-toolkit-v0.9.0", *RELEASE_SPEC_RELATIVE.parts
    )
    old_spec.write_bytes(old_spec.read_bytes() + b" ")
    state_before = (install_root / INSTALL_STATE_NAME).read_bytes()
    with pytest.raises(ReleaseError, match="installed release file disagrees"):
        rollback_release(install_root)
    assert (install_root / INSTALL_STATE_NAME).read_bytes() == state_before


def test_installed_entry_points_preserve_complete_inventory(tmp_path: Path) -> None:
    root, spec = _copy_exact_release_repo(tmp_path)
    built = build_release(spec, root, tmp_path / "artifact")
    install_root = tmp_path / "install"
    installed = install_release(built["archive"], install_root)["install_path"]
    before = _snapshot(install_root)
    environment = os.environ.copy()
    environment.pop("ABLPC_PYTHON", None)
    environment.pop("PYTHONDONTWRITEBYTECODE", None)
    environment.pop("PYTHONPYCACHEPREFIX", None)
    commands = [
        [str(installed / "scripts/ablpc-mod"), "--help"],
        [
            str(installed / "scripts/ablpc-release"),
            "current",
            "--install-root",
            str(install_root),
        ],
        [str(installed / "scripts/m6-smoke"), "--help"],
        [str(installed / "scripts/check-m4-compatibility.py")],
    ]
    hostile_environment = environment.copy()
    hostile_environment["PYTHONDONTWRITEBYTECODE"] = "0"
    hostile_environment["PYTHONPYCACHEPREFIX"] = str(installed / "hostile-cache")
    for invocation_environment in (environment, hostile_environment):
        for command in commands:
            result = subprocess.run(
                command,
                cwd=tmp_path,
                env=invocation_environment,
                text=True,
                capture_output=True,
                check=False,
            )
            assert result.returncode == 0, (command, result.stdout, result.stderr)
            assert _snapshot(install_root) == before
            assert current_release(install_root)["current"] == "ablpc-toolkit-v1.0.0"


def test_dangling_install_state_refuses_without_mutation(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    built = build_release(spec, root, tmp_path / "out")
    install_root = tmp_path / "install"
    install_root.mkdir()
    (install_root / INSTALL_STATE_NAME).symlink_to("missing-state-target")
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="install state is not a canonical single-link"):
        install_release(built["archive"], install_root)
    assert _snapshot(tmp_path) == before


def test_linked_releases_root_refuses_lifecycle_without_mutation(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    old = build_release(spec, root, tmp_path / "old")
    _write_spec(root, "1.0.0")
    _commit(root, "1.0.0")
    new = build_release(spec, root, tmp_path / "new")
    install_root = tmp_path / "install"
    install_release(old["archive"], install_root)
    install_release(new["archive"], install_root)
    releases = install_root / "releases"
    external = tmp_path / "external-releases"
    releases.rename(external)
    releases.symlink_to(external, target_is_directory=True)

    for operation in (current_release, rollback_release):
        before = _snapshot(tmp_path)
        with pytest.raises(ReleaseError, match="release directory is not a directory non-link"):
            operation(install_root)
        assert _snapshot(tmp_path) == before


def test_linked_releases_root_refuses_install_without_mutation(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    built = build_release(spec, root, tmp_path / "out")
    install_root = tmp_path / "install"
    install_root.mkdir()
    external = tmp_path / "external-releases"
    external.mkdir()
    (install_root / "releases").symlink_to(external, target_is_directory=True)
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="release directory is not a directory non-link"):
        install_release(built["archive"], install_root)
    assert _snapshot(tmp_path) == before


def test_linked_installed_version_refuses_lifecycle_without_mutation(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    old = build_release(spec, root, tmp_path / "old")
    _write_spec(root, "1.0.0")
    _commit(root, "1.0.0")
    new = build_release(spec, root, tmp_path / "new")
    install_root = tmp_path / "install"
    install_release(old["archive"], install_root)
    install_release(new["archive"], install_root)
    releases = install_root / "releases"

    current = releases / "ablpc-toolkit-v1.0.0"
    external_current = tmp_path / "external-current"
    current.rename(external_current)
    current.symlink_to(external_current, target_is_directory=True)
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="installed release .* is not a directory non-link"):
        current_release(install_root)
    assert _snapshot(tmp_path) == before
    current.unlink()
    external_current.rename(current)

    prior = releases / "ablpc-toolkit-v0.9.0"
    external_prior = tmp_path / "external-prior"
    prior.rename(external_prior)
    prior.symlink_to(external_prior, target_is_directory=True)
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="installed release .* is not a directory non-link"):
        rollback_release(install_root)
    assert _snapshot(tmp_path) == before


def test_linked_current_version_refuses_migration_without_mutation(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    old = build_release(spec, root, tmp_path / "old")
    _write_spec(root, "1.0.0")
    _commit(root, "1.0.0")
    new = build_release(spec, root, tmp_path / "new")
    install_root = tmp_path / "install"
    install_release(old["archive"], install_root)
    current = install_root / "releases" / "ablpc-toolkit-v0.9.0"
    external = tmp_path / "external-current"
    current.rename(external)
    current.symlink_to(external, target_is_directory=True)
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="installed release .* is not a directory non-link"):
        install_release(new["archive"], install_root)
    assert _snapshot(tmp_path) == before


def test_missing_releases_root_refuses_migration_without_mutation(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    old = build_release(spec, root, tmp_path / "old")
    _write_spec(root, "1.0.0")
    _commit(root, "1.0.0")
    new = build_release(spec, root, tmp_path / "new")
    install_root = tmp_path / "install"
    install_release(old["archive"], install_root)
    releases = install_root / "releases"
    releases.rename(tmp_path / "moved-releases")
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="release directory does not exist"):
        install_release(new["archive"], install_root)
    assert _snapshot(tmp_path) == before


def test_missing_state_with_populated_releases_refuses_install_without_mutation(
    tmp_path: Path,
) -> None:
    root, spec = _repo(tmp_path)
    old = build_release(spec, root, tmp_path / "old")
    _write_spec(root, "1.0.0")
    _commit(root, "1.0.0")
    new = build_release(spec, root, tmp_path / "new")
    install_root = tmp_path / "install"
    install_release(old["archive"], install_root)
    (install_root / INSTALL_STATE_NAME).rename(tmp_path / "moved-state.json")
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="missing a selection"):
        install_release(new["archive"], install_root)
    assert _snapshot(tmp_path) == before


def test_hardlinked_state_refuses_every_lifecycle_operation(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    old = build_release(spec, root, tmp_path / "old")
    _write_spec(root, "1.0.0")
    _commit(root, "1.0.0")
    new = build_release(spec, root, tmp_path / "new")
    _write_spec(root, "1.1.0")
    _commit(root, "1.1.0")
    future = build_release(spec, root, tmp_path / "future")
    install_root = tmp_path / "install"
    install_release(old["archive"], install_root)
    install_release(new["archive"], install_root)
    os.link(install_root / INSTALL_STATE_NAME, tmp_path / "linked-state.json")
    operations = (
        lambda: current_release(install_root),
        lambda: rollback_release(install_root),
        lambda: install_release(future["archive"], install_root),
    )
    for operation in operations:
        before = _snapshot(tmp_path)
        with pytest.raises(ReleaseError, match="install state is not a canonical single-link"):
            operation()
        assert _snapshot(tmp_path) == before


def test_installed_inventory_rejects_extra_empty_directory_without_mutation(
    tmp_path: Path,
) -> None:
    root, spec = _repo(tmp_path)
    built = build_release(spec, root, tmp_path / "out")
    install_root = tmp_path / "install"
    installed = install_release(built["archive"], install_root)["install_path"]
    (installed / "unlisted-empty").mkdir()
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="missing or extra topology"):
        current_release(install_root)
    assert _snapshot(tmp_path) == before


@pytest.mark.parametrize("relative", [RELEASE_MANIFEST_NAME, RELEASE_SPEC_RELATIVE.as_posix()])
def test_installed_inventory_rejects_hardlinked_file_without_mutation(
    tmp_path: Path, relative: str
) -> None:
    root, spec = _repo(tmp_path)
    built = build_release(spec, root, tmp_path / "out")
    install_root = tmp_path / "install"
    installed = install_release(built["archive"], install_root)["install_path"]
    os.link(installed.joinpath(*Path(relative).parts), tmp_path / "external-hardlink")
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="single-link regular"):
        current_release(install_root)
    assert _snapshot(tmp_path) == before


def test_installed_manifest_mode_drift_refuses_without_mutation(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    built = build_release(spec, root, tmp_path / "out")
    install_root = tmp_path / "install"
    installed = install_release(built["archive"], install_root)["install_path"]
    os.chmod(installed / RELEASE_MANIFEST_NAME, 0o600)
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="canonical single-link regular"):
        current_release(install_root)
    assert _snapshot(tmp_path) == before


@pytest.mark.parametrize("scope", ["state", "releases", "version", "package"])
def test_installed_directory_and_state_mode_drift_refuses_without_mutation(
    tmp_path: Path, scope: str
) -> None:
    root, spec = _repo(tmp_path)
    built = build_release(spec, root, tmp_path / "out")
    install_root = tmp_path / "install"
    installed = install_release(built["archive"], install_root)["install_path"]
    target = {
        "state": install_root / INSTALL_STATE_NAME,
        "releases": install_root / "releases",
        "version": installed,
        "package": installed / "reimplementation",
    }[scope]
    os.chmod(target, 0o700 if scope == "state" else 0o750)
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="canonical|mode"):
        current_release(install_root)
    assert _snapshot(tmp_path) == before


def test_unlisted_release_root_entry_refuses_without_mutation(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    built = build_release(spec, root, tmp_path / "out")
    install_root = tmp_path / "install"
    install_release(built["archive"], install_root)
    (install_root / "releases" / "unexpected").mkdir()
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="installed release directory name"):
        current_release(install_root)
    assert _snapshot(tmp_path) == before


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("toolkit_version", "9.9.9"),
        ("release_spec_path", "README.md"),
    ],
)
def test_installed_manifest_identity_drift_refuses_without_mutation(
    tmp_path: Path, field: str, value: object
) -> None:
    root, spec = _repo(tmp_path)
    built = build_release(spec, root, tmp_path / "out")
    install_root = tmp_path / "install"
    installed = install_release(built["archive"], install_root)["install_path"]
    manifest_path = installed / RELEASE_MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest[field] = value
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="manifest lock disagrees"):
        current_release(install_root)
    assert _snapshot(tmp_path) == before


def test_invalid_inactive_prior_refuses_every_lifecycle_operation(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    old = build_release(spec, root, tmp_path / "old")
    _write_spec(root, "1.0.0")
    _commit(root, "1.0.0")
    new = build_release(spec, root, tmp_path / "new")
    _write_spec(root, "1.1.0")
    _commit(root, "1.1.0")
    future = build_release(spec, root, tmp_path / "future")
    install_root = tmp_path / "install"
    install_release(old["archive"], install_root)
    install_release(new["archive"], install_root)
    prior = install_root / "releases" / "ablpc-toolkit-v0.9.0"
    (prior / "unlisted-empty").mkdir()
    operations = (
        lambda: current_release(install_root),
        lambda: rollback_release(install_root),
        lambda: install_release(future["archive"], install_root),
    )
    for operation in operations:
        before = _snapshot(tmp_path)
        with pytest.raises(ReleaseError, match="missing or extra topology"):
            operation()
        assert _snapshot(tmp_path) == before


def test_missing_outgoing_current_refuses_rollback_without_mutation(tmp_path: Path) -> None:
    root, spec = _repo(tmp_path)
    old = build_release(spec, root, tmp_path / "old")
    _write_spec(root, "1.0.0")
    _commit(root, "1.0.0")
    new = build_release(spec, root, tmp_path / "new")
    install_root = tmp_path / "install"
    install_release(old["archive"], install_root)
    install_release(new["archive"], install_root)
    current = install_root / "releases" / "ablpc-toolkit-v1.0.0"
    current.rename(tmp_path / "moved-current")
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="state and release directory disagree"):
        rollback_release(install_root)
    assert _snapshot(tmp_path) == before


def test_content_and_manifest_rebaseline_refuses_state_lock_without_mutation(
    tmp_path: Path,
) -> None:
    root, spec = _repo(tmp_path)
    built = build_release(spec, root, tmp_path / "out")
    install_root = tmp_path / "install"
    installed = install_release(built["archive"], install_root)["install_path"]
    target = installed.joinpath(*RELEASE_SPEC_RELATIVE.parts)
    target.write_bytes(target.read_bytes() + b" ")
    manifest_path = installed / RELEASE_MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    item = next(
        item for item in manifest["files"] if item["path"] == RELEASE_SPEC_RELATIVE.as_posix()
    )
    item["size"] = target.stat().st_size
    item["sha256"] = _sha256(target.read_bytes())
    tree_digest = hashlib.sha256()
    for entry in manifest["files"]:
        tree_digest.update((json.dumps(entry, indent=2) + "\n").encode("utf-8"))
    manifest["source_tree_sha256"] = tree_digest.hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    before = _snapshot(tmp_path)
    with pytest.raises(ReleaseError, match="manifest lock disagrees"):
        current_release(install_root)
    assert _snapshot(tmp_path) == before


def test_spec_rejects_protected_and_binary_package_paths(tmp_path: Path) -> None:
    root = tmp_path / "root"
    spec_path = _write_spec(root, "1.0.0")
    for forbidden in ("originals/game.dat", "payload.exe"):
        value = copy.deepcopy(_spec("1.0.0"))
        value["package_files"].append(forbidden)
        value["package_files"].sort()
        spec_path.write_text(json.dumps(value), encoding="utf-8")
        with pytest.raises(ReleaseError):
            load_release_spec(spec_path)


def test_current_on_missing_root_is_non_mutating(tmp_path: Path) -> None:
    missing = tmp_path / "missing"
    with pytest.raises(ReleaseError, match="does not exist"):
        current_release(missing)
    assert not missing.exists()
