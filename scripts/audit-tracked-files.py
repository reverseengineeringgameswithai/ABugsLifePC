#!/usr/bin/env python3
"""Reject tracked files that violate the repository's provenance boundary."""

from __future__ import annotations

import subprocess
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {
    ".cue",
    ".dmp",
    ".exe",
    ".img",
    ".iso",
    ".qcow2",
    ".rom",
    ".vdi",
    ".vhd",
    ".vhdx",
    ".vmdk",
}


def tracked_paths() -> list[PurePosixPath]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [PurePosixPath(raw.decode()) for raw in result.stdout.split(b"\0") if raw]


def violations(paths: list[PurePosixPath]) -> list[str]:
    found: list[str] = []
    for path in paths:
        parts = path.parts
        if parts and parts[0] in {"originals", "media", "work"} and path.name != ".gitkeep":
            found.append(f"protected work/source path is tracked: {path}")
        if (
            parts[:2] == ("tools", "86box")
            and path.name != "README.md"
            and parts[:3] != ("tools", "86box", "patches")
        ):
            # tools/86box holds the git-ignored downloaded/built emulator binaries;
            # tools/86box/patches/ is an allowed exception for tracked source patches
            # (still subject to the forbidden-binary-suffix check below).
            found.append(f"downloaded tool is tracked: {path}")
        if parts[:2] in {
            ("tools", "ghidra"),
            ("tools", "jdk"),
            ("tools", "pcem"),
            ("tools", "windows"),
        } and path.name != "README.md":
            found.append(f"downloaded tool is tracked: {path}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            found.append(f"forbidden binary/media extension is tracked: {path}")
    return found


def main() -> int:
    found = violations(tracked_paths())
    for message in found:
        print(f"ERROR: {message}")
    print(f"Tracked-file audit: {len(found)} violation(s)")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
