"""Isolated bind-mount regression helper for removal and restoration tests."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, os.fspath(REPO_ROOT))

from reimplementation.ablpc.manifest import (  # noqa: E402
    ManifestError,
    _linux_mount_entries,
    apply_manifest,
    remove_manifest,
    restore_manifest,
    stage_manifest,
)


DESTINATION_PATH = "D/shared/deep/out.bin"
SOURCE_PATH = "SOURCE/replacement.bin"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _snapshot(root: Path) -> tuple[tuple[str, str, object], ...]:
    if not root.exists() and not root.is_symlink():
        return ()
    result: list[tuple[str, str, object]] = []

    def visit(path: Path, relative: str) -> None:
        metadata = path.lstat()
        if stat.S_ISDIR(metadata.st_mode):
            kind = "directory"
            payload: object = None
        elif stat.S_ISREG(metadata.st_mode):
            kind = "regular"
            payload = (path.read_bytes(), metadata.st_nlink)
        elif stat.S_ISLNK(metadata.st_mode):
            kind = "symlink"
            payload = os.readlink(path)
        else:
            kind = "non-regular"
            payload = metadata.st_mode
        metadata_payload = (
            stat.S_IMODE(metadata.st_mode),
            metadata.st_uid,
            metadata.st_gid,
            metadata.st_nlink,
            metadata.st_dev,
            metadata.st_ino,
            metadata.st_size,
            payload,
        )
        result.append((relative, kind, metadata_payload))
        if kind == "directory":
            for child in sorted(path.iterdir(), key=lambda item: item.name):
                child_relative = (
                    f"{relative}/{child.name}" if relative else child.name
                )
                visit(child, child_relative)

    visit(root, "")
    return tuple(result)


def _write_file(root: Path, relative: str, data: bytes) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _manifest(destination: bytes, replacement: bytes) -> dict[str, object]:
    return {
        "schema_version": 2,
        "name": "isolated-mounted-overlay-removal",
        "files": [
            {
                "path": DESTINATION_PATH,
                "sha256": _sha256(destination),
                "format": "opaque-file-v0",
                "edits": [
                    {
                        "operation": "replace-whole-file",
                        "source_path": SOURCE_PATH,
                        "source_sha256": _sha256(replacement),
                    }
                ],
            }
        ],
    }


def _bind(source: Path, destination: Path) -> None:
    try:
        subprocess.run(
            ["mount", "--bind", os.fspath(source), os.fspath(destination)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"host cannot create isolated bind mount: {error}")
        raise SystemExit(77) from error


def _mount_tmpfs(destination: Path) -> None:
    try:
        subprocess.run(
            ["mount", "-t", "tmpfs", "tmpfs", os.fspath(destination)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"host cannot create isolated tmpfs mount: {error}")
        raise SystemExit(77) from error


def _unmount(destination: Path) -> None:
    try:
        subprocess.run(
            ["umount", os.fspath(destination)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"host cannot release isolated mount: {error}")
        raise SystemExit(77) from error


def _mount_entry(path: Path):
    normalized = Path(os.path.normpath(os.fspath(path)))
    matches = [
        entry
        for entry in _linux_mount_entries()
        if entry.mount_point == normalized
    ]
    if len(matches) != 1:
        raise AssertionError(
            f"expected one mount entry for {normalized}, got {len(matches)}"
        )
    return matches[0]


def _run(case: str, case_root: Path) -> None:
    destination = b"original destination"
    replacement = b"authenticated replacement"
    source_root = case_root / "source"
    # The embedded space also exercises mountinfo's \040 path decoding.
    overlay_root = case_root / "overlay root"
    external_root = case_root / "independent target"
    _write_file(source_root, DESTINATION_PATH, destination)
    _write_file(source_root, SOURCE_PATH, replacement)
    _write_file(source_root, "UNRELATED/keep.bin", b"unrelated retained bytes")
    manifest = _manifest(destination, replacement)

    if case.startswith("restore-"):
        staged_root = case_root / "staged root"
        external_root.mkdir(parents=True)
        if case == "restore-root":
            external_stage = external_root / "mounted-stage"
            stage_manifest(manifest, source_root, external_stage)
            staged_root.mkdir(parents=True)
            _bind(external_stage, staged_root)
        else:
            stage_manifest(manifest, source_root, staged_root)
            if case == "restore-output":
                mount_target = staged_root / DESTINATION_PATH
                external_target = external_root / "out.bin"
                mount_target.rename(external_target)
                mount_target.write_bytes(b"hidden mount placeholder")
            elif case == "restore-receipt":
                mount_target = staged_root / ".ablpc/receipt.json"
                external_target = external_root / "receipt.json"
                mount_target.rename(external_target)
                mount_target.write_bytes(b"hidden mount placeholder")
            elif case == "restore-unrelated":
                mount_target = staged_root / "UNRELATED/keep.bin"
                external_target = external_root / "keep.bin"
                mount_target.rename(external_target)
                mount_target.write_bytes(b"hidden mount placeholder")
            else:
                raise AssertionError(f"unsupported restoration mount case: {case}")
            _bind(external_target, mount_target)

        source_before = _snapshot(source_root)
        staged_before = _snapshot(staged_root)
        external_before = _snapshot(external_root)
        try:
            restore_manifest(manifest, source_root, staged_root)
        except ManifestError as error:
            if "game restoration plan contains a mounted path" not in str(error):
                raise AssertionError(f"unexpected refusal: {error}") from error
        else:
            raise AssertionError("mounted game restoration plan was not refused")
        assert _snapshot(source_root) == source_before
        assert _snapshot(staged_root) == staged_before
        assert _snapshot(external_root) == external_before
        return

    if case == "reuse":
        scratch = case_root / "released scratch mount"
        independent_parent = external_root / "independent parent"
        alias_parent = case_root / "reused-id alias parent"
        scratch.mkdir(parents=True)
        independent_parent.mkdir(parents=True)
        alias_parent.mkdir(parents=True)

        _mount_tmpfs(scratch)
        scratch_entry = _mount_entry(scratch)
        _mount_tmpfs(independent_parent)
        independent_entry = _mount_entry(independent_parent)
        independent_overlay = independent_parent / "overlay root"
        apply_manifest(manifest, source_root, independent_overlay)

        _unmount(scratch)
        _bind(independent_parent, alias_parent)
        independent_entry = _mount_entry(independent_parent)
        alias_entry = _mount_entry(alias_parent)
        if alias_entry.mount_id != scratch_entry.mount_id:
            raise AssertionError(
                "kernel did not reuse the released mountinfo ID: "
                f"scratch={scratch_entry.mount_id}, alias={alias_entry.mount_id}"
            )
        if alias_entry.mount_id >= independent_entry.mount_id:
            raise AssertionError(
                "regression did not create a lower reused ID for the later alias"
            )
        if alias_entry.mount_order <= independent_entry.mount_order:
            raise AssertionError(
                "kernel later-mount ordering did not identify the alias as later: "
                f"source={independent_entry}, alias={alias_entry}"
            )

        overlay_root = alias_parent / "overlay root"
        source_before = _snapshot(source_root)
        independent_before = _snapshot(independent_parent)
        alias_before = _snapshot(alias_parent)
        overlay_before = _snapshot(overlay_root)
        assert overlay_before
        try:
            remove_manifest(manifest, source_root, overlay_root)
        except ManifestError as error:
            if "overlay root ancestry contains a mount alias" not in str(error):
                raise AssertionError(f"unexpected refusal: {error}") from error
        else:
            raise AssertionError("reused-ID mount alias was not refused")

        assert _snapshot(source_root) == source_before
        assert _snapshot(independent_parent) == independent_before
        assert _snapshot(alias_parent) == alias_before
        assert _snapshot(overlay_root) == overlay_before
        return

    if case == "stacked":
        hidden_parent = external_root / "hidden independent parent"
        _write_file(hidden_parent, "hidden-marker.bin", b"hidden lower bytes")
        visible_parent = case_root / "stacked parent"
        visible_parent.mkdir(parents=True)
        _bind(hidden_parent, visible_parent)
        _mount_tmpfs(visible_parent)
        visible_empty = _snapshot(visible_parent)
        overlay_root = visible_parent / "overlay root"
        receipt = apply_manifest(manifest, source_root, overlay_root)

        source_before = _snapshot(source_root)
        hidden_before = _snapshot(external_root)
        visible_before = _snapshot(visible_parent)
        overlay_before = _snapshot(overlay_root)
        assert overlay_before

        assert remove_manifest(manifest, source_root, overlay_root) == receipt
        assert not overlay_root.exists()
        assert _snapshot(source_root) == source_before
        assert _snapshot(external_root) == hidden_before
        assert _snapshot(visible_parent) == visible_empty
        assert visible_before != visible_empty
        return

    if case == "ancestor":
        independent_parent = external_root / "independent parent"
        independent_overlay = independent_parent / "overlay root"
        apply_manifest(manifest, source_root, independent_overlay)
        alias_parent = case_root / "alias parent"
        alias_parent.mkdir(parents=True)
        _bind(independent_parent, alias_parent)
        overlay_root = alias_parent / "overlay root"
    elif case == "root":
        external_overlay = external_root / "mounted-overlay"
        apply_manifest(manifest, source_root, external_overlay)
        overlay_root.mkdir(parents=True)
        _bind(external_overlay, overlay_root)
    else:
        apply_manifest(manifest, source_root, overlay_root)
        external_root.mkdir(parents=True)
        if case == "intermediate":
            mount_target = overlay_root / "D"
            external_target = external_root / "D"
            mount_target.rename(external_target)
            mount_target.mkdir()
        elif case == "output":
            mount_target = overlay_root / DESTINATION_PATH
            external_target = external_root / "out.bin"
            mount_target.rename(external_target)
            mount_target.write_bytes(b"hidden mount placeholder")
        elif case == "receipt":
            mount_target = overlay_root / ".ablpc/receipt.json"
            external_target = external_root / "receipt.json"
            mount_target.rename(external_target)
            mount_target.write_bytes(b"hidden mount placeholder")
        else:
            raise AssertionError(f"unsupported mount case: {case}")
        _bind(external_target, mount_target)

    overlay_before = _snapshot(overlay_root)
    source_before = _snapshot(source_root)
    external_before = _snapshot(external_root)
    try:
        remove_manifest(manifest, source_root, overlay_root)
    except ManifestError as error:
        expected_message = (
            "overlay root ancestry contains a mount alias"
            if case == "ancestor"
            else "overlay deletion plan contains a mounted path"
        )
        if expected_message not in str(error):
            raise AssertionError(f"unexpected refusal: {error}") from error
    else:
        raise AssertionError("mounted deletion plan was not refused")

    assert _snapshot(overlay_root) == overlay_before
    assert _snapshot(source_root) == source_before
    assert _snapshot(external_root) == external_before


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: mount_overlay_case.py CASE CASE_ROOT")
    case = sys.argv[1]
    case_root = Path(sys.argv[2])
    case_root.mkdir(parents=True)
    _run(case, case_root)
    print(f"isolated mounted {case} deletion-plan path refused unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
