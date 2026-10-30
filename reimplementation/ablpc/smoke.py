"""Primary Linux clean-copy smoke matrix for the bounded M6 release."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import stat
import subprocess
import sys
import tempfile
from typing import Any

from .compatibility import check_compatibility_statement
from .level_dat import LevelDat
from .manifest import load_manifest, restore_manifest, stage_manifest
from .release import RELEASE_SPEC_RELATIVE, ReleaseError, load_release_spec


class SmokeError(ValueError):
    """Raised when the M6 smoke matrix cannot establish a passing result."""


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        raise SmokeError(f"cannot hash {path}: {error}") from error
    return digest.hexdigest()


def _regular_non_link(path: Path, label: str) -> None:
    try:
        metadata = path.lstat()
    except OSError as error:
        raise SmokeError(f"cannot inspect {label} {path}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise SmokeError(f"{label} is not a regular non-link file: {path}")


def _tree_inventory(root: Path) -> list[dict[str, object]]:
    inventory: list[dict[str, object]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        try:
            metadata = path.lstat()
        except OSError as error:
            raise SmokeError(f"cannot inspect game-tree entry {path}: {error}") from error
        if stat.S_ISLNK(metadata.st_mode):
            raise SmokeError(f"game tree contains a symbolic link: {relative}")
        if stat.S_ISDIR(metadata.st_mode):
            inventory.append({"path": relative, "kind": "directory"})
        elif stat.S_ISREG(metadata.st_mode):
            inventory.append(
                {
                    "path": relative,
                    "kind": "file",
                    "size": metadata.st_size,
                    "sha256": _sha256_path(path),
                }
            )
        else:
            raise SmokeError(f"game tree contains unsupported entry: {relative}")
    return inventory


def _command_output(command: list[str], cwd: Path) -> str:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        stderr = getattr(error, "stderr", "")
        raise SmokeError(f"command failed: {' '.join(command)}: {stderr}") from error
    return (result.stdout + result.stderr).strip()


def _validate_primary_environment(spec: dict[str, Any], repo_root: Path) -> dict[str, str]:
    expected = spec["primary_environment"]
    os_release: dict[str, str] = {}
    try:
        for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                os_release[key] = value.strip().strip('"')
    except OSError as error:
        raise SmokeError(f"cannot read /etc/os-release: {error}") from error
    observed = {
        "os": platform.system(),
        "distribution": os_release.get("PRETTY_NAME", ""),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "wine": _command_output(["wine", "--version"], repo_root).splitlines()[-1],
        "gamescope_package": _command_output(["rpm", "-q", "gamescope"], repo_root).splitlines()[-1],
    }
    for key in (
        "os",
        "distribution",
        "kernel",
        "architecture",
        "python",
        "wine",
        "gamescope_package",
    ):
        if observed[key] != expected[key]:
            raise SmokeError(
                f"primary environment mismatch for {key}: "
                f"expected {expected[key]!r}, observed {observed[key]!r}"
            )
    return observed


def _validated_game_root(repo_root: Path, game_root: Path) -> Path:
    copies_root = (repo_root / "work" / "copies").resolve()
    try:
        resolved = game_root.resolve(strict=True)
    except OSError as error:
        raise SmokeError(f"cannot resolve game root {game_root}: {error}") from error
    if resolved == copies_root or copies_root not in resolved.parents:
        raise SmokeError(f"game root must be below {copies_root}: {resolved}")
    if not resolved.is_dir():
        raise SmokeError(f"game root is not a directory: {resolved}")
    return resolved


def _validate_supported_inputs(
    spec: dict[str, Any], repo_root: Path, game_root: Path
) -> dict[str, object]:
    supported = spec["supported_inputs"]
    executable = game_root / "bugs.exe"
    _regular_non_link(executable, "game executable")
    executable_sha256 = _sha256_path(executable)
    if executable_sha256 != supported["executable_sha256"]:
        raise SmokeError(f"unsupported bugs.exe SHA-256: {executable_sha256}")

    for relative, expected_sha256 in supported["compatibility_statements"].items():
        path = repo_root.joinpath(*PurePosixPath(relative).parts)
        _regular_non_link(path, "compatibility statement")
        if _sha256_path(path) != expected_sha256:
            raise SmokeError(f"compatibility statement hash disagrees: {relative}")
    for relative, expected_sha256 in supported["data_hashes"].items():
        path = game_root.joinpath(*PurePosixPath(relative).parts)
        _regular_non_link(path, "supported game data")
        if _sha256_path(path) != expected_sha256:
            raise SmokeError(f"unsupported game-data SHA-256: {relative}")

    level_paths = sorted(
        path
        for path in game_root.rglob("*.DAT")
        if path.is_file() and path.name.upper().startswith("LEVEL")
    )
    if len(level_paths) != supported["level_dat_corpus_count"]:
        raise SmokeError(
            "LEVEL*.DAT corpus count disagrees: "
            f"expected {supported['level_dat_corpus_count']}, observed {len(level_paths)}"
        )
    for path in level_paths:
        LevelDat.from_path(path)
    return {
        "executable_sha256": executable_sha256,
        "level_dat_files": len(level_paths),
        "data_hashes": len(supported["data_hashes"]),
    }


def _launcher_dry_run(
    repo_root: Path, game_root: Path, prefix: Path, executable_sha256: str
) -> dict[str, object]:
    launcher = repo_root / "scripts" / "play-pristine.sh"
    _regular_non_link(launcher, "launcher")
    command = [
        str(launcher),
        "--game-dir",
        str(game_root),
        "--prefix",
        str(prefix),
        "--research",
        "--windowed",
        "--mute",
        "--dry-run",
    ]
    output = _command_output(command, repo_root)
    required = [
        f"Verified bugs.exe: {executable_sha256}",
        "At the renderer selector, press Down once",
        "-w 640 -h 480",
        "-S fit -F nearest",
        "PULSE_SINK=ablpc_mute_",
        "wine ./bugs.exe log cheat mpeg",
    ]
    missing = [fragment for fragment in required if fragment not in output]
    if missing:
        raise SmokeError(f"launcher dry-run lacks required markers: {missing}")
    return {
        "validated": True,
        "hardware_selection": "manual Down then confirm",
        "window": "1280x960",
        "game_surface": "640x480",
        "scaling": "fit/nearest",
        "audio": "private null-sink command validated; no audio was played",
    }


def run_smoke_matrix(
    repo_root: Path,
    game_root: Path,
    prefix: Path,
    spec_path: Path | None = None,
) -> dict[str, object]:
    """Run the exact M6 clean-copy stage/launch-dry-run/restore matrix."""

    repo_root = repo_root.resolve()
    spec_path = spec_path or repo_root.joinpath(*RELEASE_SPEC_RELATIVE.parts)
    try:
        spec = load_release_spec(spec_path)
    except ReleaseError as error:
        raise SmokeError(str(error)) from error
    game_root = _validated_game_root(repo_root, game_root)
    try:
        prefix = prefix.resolve(strict=True)
    except OSError as error:
        raise SmokeError(f"cannot resolve Wine prefix {prefix}: {error}") from error
    if not prefix.is_dir():
        raise SmokeError(f"Wine prefix is not a directory: {prefix}")

    environment = _validate_primary_environment(spec, repo_root)
    supported = _validate_supported_inputs(spec, repo_root, game_root)
    active_statement = repo_root / "reimplementation" / "compatibility" / "m4-v0.2.json"
    compatibility = check_compatibility_statement(active_statement, repo_root)
    source_inventory = _tree_inventory(game_root)

    copies_root = repo_root / "work" / "copies"
    case_results: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="m6-smoke-", dir=copies_root) as temporary:
        scratch = Path(temporary)
        for case in spec["smoke_matrix"]:
            manifest_path = repo_root.joinpath(*PurePosixPath(case["manifest"]).parts)
            manifest = load_manifest(manifest_path)
            staged_root = scratch / case["case_id"]
            receipt = stage_manifest(manifest, game_root, staged_root)
            launcher = _launcher_dry_run(
                repo_root,
                staged_root,
                prefix,
                supported["executable_sha256"],
            )
            restored = restore_manifest(manifest, game_root, staged_root)
            if restored != receipt:
                raise SmokeError(f"restore receipt disagrees for {case['case_id']}")
            if _tree_inventory(staged_root) != source_inventory:
                raise SmokeError(f"restored staged tree differs for {case['case_id']}")
            case_results.append(
                {
                    "case_id": case["case_id"],
                    "scope": case["scope"],
                    "manifest": case["manifest"],
                    "manifest_schema_version": manifest["schema_version"],
                    "workflow": case["workflow"],
                    "receipt_files": len(receipt["files"]),
                    "launcher": launcher,
                    "restored_tree_exact": True,
                    "result": "PASS",
                }
            )

    if _tree_inventory(game_root) != source_inventory:
        raise SmokeError("source game tree changed during the smoke matrix")
    return {
        "smoke_report_schema_version": 1,
        "release_id": spec["release_id"],
        "result": "PASS",
        "environment": environment,
        "supported_inputs": supported,
        "m4_statement_id": compatibility["statement_id"],
        "source_tree_entries": len(source_inventory),
        "cases": case_results,
        "limitations": spec["limitations"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="m6-smoke")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--game-root", type=Path, required=True)
    parser.add_argument("--prefix", type=Path, required=True)
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    try:
        report = run_smoke_matrix(
            args.repo_root,
            args.game_root,
            args.prefix,
            spec_path=args.spec,
        )
    except (OSError, SmokeError, ValueError) as error:
        print(f"m6-smoke: {error}", file=sys.stderr)
        return 2
    encoded = json.dumps(report, indent=2) + "\n"
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.report.with_name(f".{args.report.name}.tmp-{os.getpid()}")
        try:
            temporary.write_text(encoded, encoding="utf-8")
            os.replace(temporary, args.report)
        finally:
            temporary.unlink(missing_ok=True)
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
