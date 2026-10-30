"""Reproducible, asset-free release archives and non-destructive installs."""

from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile
from typing import Any


RELEASE_SPEC_RELATIVE = PurePosixPath(
    "reimplementation/release/m6-v1.0.0.json"
)
RELEASE_MANIFEST_NAME = "RELEASE-MANIFEST.json"
INSTALL_STATE_NAME = "state.json"
MAX_ARCHIVE_FILE_SIZE = 2 * 1024 * 1024
MAX_ARCHIVE_SIZE = 64 * 1024 * 1024
MAX_PACKAGE_FILES = 256
FORBIDDEN_SUFFIXES = {
    ".bin",
    ".core",
    ".cue",
    ".dmp",
    ".exe",
    ".img",
    ".iso",
    ".qcow2",
    ".raw",
    ".rom",
    ".vdi",
    ".vhd",
    ".vhdx",
    ".vmdk",
}
PROTECTED_TOP_LEVELS = {"media", "originals", "work"}
RELEASE_ID_PATTERN = re.compile(r"ablpc-toolkit-v[0-9]+\.[0-9]+\.[0-9]+")


class ReleaseError(ValueError):
    """Raised when a release input or lifecycle state is invalid."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def _parse_json(data: bytes, label: str) -> Any:
    def reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ReleaseError(f"{label} contains duplicate key {key!r}")
            result[key] = value
        return result

    try:
        return json.loads(
            data,
            object_pairs_hook=reject_duplicate,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ReleaseError(f"{label} contains invalid JSON number {value}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReleaseError(f"cannot parse {label}: {error}") from error


def _relative_path(value: object, label: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise ReleaseError(f"{label} must be a non-empty string")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ReleaseError(f"{label} must be a normalized relative path: {value!r}")
    if path.parts[0] in PROTECTED_TOP_LEVELS:
        raise ReleaseError(f"{label} enters protected path {path.parts[0]!r}")
    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        raise ReleaseError(f"{label} has forbidden release suffix {path.suffix!r}")
    return path


def _digest(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ReleaseError(f"{label} must be a lowercase SHA-256")
    return value


def _release_id(value: object, label: str) -> str:
    if not isinstance(value, str) or RELEASE_ID_PATTERN.fullmatch(value) is None:
        raise ReleaseError(f"{label} must be ablpc-toolkit-v<major>.<minor>.<patch>")
    return value


def load_release_spec(path: Path) -> dict[str, Any]:
    """Load the exact M6 release schema without following a final symlink."""

    try:
        metadata = path.lstat()
    except OSError as error:
        raise ReleaseError(f"cannot inspect release spec {path}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ReleaseError(f"release spec is not a regular non-link file: {path}")
    if metadata.st_size > MAX_ARCHIVE_FILE_SIZE:
        raise ReleaseError(f"release spec exceeds size bound: {path}")
    try:
        data = path.read_bytes()
    except OSError as error:
        raise ReleaseError(f"cannot read release spec {path}: {error}") from error
    value = _parse_json(data, f"release spec {path}")
    _validate_release_spec(value)
    return value


def _validate_release_spec(value: object) -> None:
    if not isinstance(value, dict):
        raise ReleaseError("release spec root must be an object")
    expected = {
        "release_schema_version",
        "release_id",
        "toolkit_version",
        "archive_name",
        "package_root",
        "source_date_epoch",
        "package_files",
        "supported_inputs",
        "primary_environment",
        "smoke_matrix",
        "limitations",
    }
    if set(value) != expected:
        raise ReleaseError("release spec fields do not match schema 1")
    if value["release_schema_version"] != 1:
        raise ReleaseError("release_schema_version must be 1")
    for key in ("release_id", "toolkit_version", "archive_name", "package_root"):
        if not isinstance(value[key], str) or not value[key]:
            raise ReleaseError(f"{key} must be a non-empty string")
    _release_id(value["release_id"], "release_id")
    if re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", value["toolkit_version"]) is None:
        raise ReleaseError("toolkit_version must be numeric major.minor.patch")
    if value["release_id"] != f"ablpc-toolkit-v{value['toolkit_version']}":
        raise ReleaseError("release_id and toolkit_version disagree")
    if value["package_root"] != value["release_id"]:
        raise ReleaseError("package_root must equal release_id")
    if value["archive_name"] != f"{value['release_id']}.tar":
        raise ReleaseError("archive_name must be <release_id>.tar")
    epoch = value["source_date_epoch"]
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch <= 0:
        raise ReleaseError("source_date_epoch must be a positive integer")

    package_files = value["package_files"]
    if (
        not isinstance(package_files, list)
        or not package_files
        or len(package_files) > MAX_PACKAGE_FILES
    ):
        raise ReleaseError("package_files must be a non-empty array")
    paths = [
        _relative_path(item, f"package_files[{index}]").as_posix()
        for index, item in enumerate(package_files)
    ]
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise ReleaseError("package_files must be sorted and unique")
    if RELEASE_SPEC_RELATIVE.as_posix() not in paths:
        raise ReleaseError("package_files must contain the canonical release spec")

    supported = value["supported_inputs"]
    supported_keys = {
        "disc_iso_sha256",
        "executable_sha256",
        "manifest_schema_versions",
        "compatibility_statements",
        "data_hashes",
        "level_dat_corpus_count",
    }
    if not isinstance(supported, dict) or set(supported) != supported_keys:
        raise ReleaseError("supported_inputs fields do not match schema 1")
    _digest(supported["disc_iso_sha256"], "disc_iso_sha256")
    _digest(supported["executable_sha256"], "executable_sha256")
    if supported["manifest_schema_versions"] != [1, 2]:
        raise ReleaseError("manifest_schema_versions must be exactly [1, 2]")
    if supported["level_dat_corpus_count"] != 21:
        raise ReleaseError("level_dat_corpus_count must be exactly 21")
    for mapping_name in ("compatibility_statements", "data_hashes"):
        mapping = supported[mapping_name]
        if not isinstance(mapping, dict) or not mapping:
            raise ReleaseError(f"{mapping_name} must be a non-empty object")
        for key, digest in mapping.items():
            _relative_path(key, f"{mapping_name} key")
            _digest(digest, f"{mapping_name}[{key!r}]")

    environment = value["primary_environment"]
    if not isinstance(environment, dict) or set(environment) != {
        "os",
        "distribution",
        "kernel",
        "architecture",
        "python",
        "wine",
        "gamescope_package",
        "renderer",
        "game_surface",
        "presentation",
    }:
        raise ReleaseError("primary_environment fields do not match schema 1")
    if any(not isinstance(item, str) or not item for item in environment.values()):
        raise ReleaseError("primary_environment values must be non-empty strings")

    smoke = value["smoke_matrix"]
    if not isinstance(smoke, list) or len(smoke) < 2:
        raise ReleaseError("smoke_matrix must contain at least two cases")
    case_ids: list[str] = []
    for index, case in enumerate(smoke):
        if not isinstance(case, dict) or set(case) != {
            "case_id",
            "scope",
            "manifest",
            "workflow",
        }:
            raise ReleaseError(f"smoke_matrix[{index}] fields do not match schema 1")
        if any(not isinstance(case[key], str) or not case[key] for key in case):
            raise ReleaseError(f"smoke_matrix[{index}] values must be strings")
        _relative_path(case["manifest"], f"smoke_matrix[{index}].manifest")
        if case["workflow"] != "stage-launch-dry-run-restore":
            raise ReleaseError(f"smoke_matrix[{index}] has unsupported workflow")
        case_ids.append(case["case_id"])
    if len(case_ids) != len(set(case_ids)):
        raise ReleaseError("smoke_matrix case_id values must be unique")

    limitations = value["limitations"]
    if (
        not isinstance(limitations, list)
        or not limitations
        or any(not isinstance(item, str) or not item for item in limitations)
    ):
        raise ReleaseError("limitations must be a non-empty string array")


def _tracked_package_sources(repo_root: Path, paths: list[PurePosixPath]) -> None:
    relative = [path.as_posix() for path in paths]
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--", *relative],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise ReleaseError(f"cannot enumerate tracked release sources: {error}") from error
    tracked = sorted(
        item.decode("utf-8") for item in result.stdout.split(b"\0") if item
    )
    if tracked != sorted(relative):
        missing = sorted(set(relative) - set(tracked))
        raise ReleaseError(f"release source is not tracked: {', '.join(missing)}")
    for cached in (False, True):
        command = ["git", "diff", "--quiet"]
        if cached:
            command.append("--cached")
        command.extend(["--", *relative])
        status = subprocess.run(command, cwd=repo_root, check=False).returncode
        if status != 0:
            location = "index" if cached else "working tree"
            raise ReleaseError(f"release sources differ from clean HEAD in the {location}")


def _source_inventory(
    repo_root: Path, paths: list[PurePosixPath]
) -> tuple[list[dict[str, object]], dict[str, bytes]]:
    inventory: list[dict[str, object]] = []
    content: dict[str, bytes] = {}
    for relative in paths:
        source = repo_root.joinpath(*relative.parts)
        try:
            metadata = source.lstat()
        except OSError as error:
            raise ReleaseError(f"cannot inspect release source {source}: {error}") from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise ReleaseError(f"release source is not a regular non-link file: {source}")
        try:
            data = source.read_bytes()
        except OSError as error:
            raise ReleaseError(f"cannot read release source {source}: {error}") from error
        if len(data) > MAX_ARCHIVE_FILE_SIZE:
            raise ReleaseError(f"release source exceeds size bound: {relative}")
        mode = 0o755 if metadata.st_mode & 0o111 else 0o644
        item = {
            "path": relative.as_posix(),
            "size": len(data),
            "sha256": _sha256(data),
            "mode": f"{mode:04o}",
        }
        inventory.append(item)
        content[relative.as_posix()] = data
    return inventory, content


def _tree_id(inventory: list[dict[str, object]]) -> str:
    digest = hashlib.sha256()
    for item in inventory:
        digest.update(_canonical_json(item))
    return digest.hexdigest()


def _canonical_tar_bytes(
    spec: dict[str, Any],
    inventory: list[dict[str, object]],
    content: dict[str, bytes],
    manifest_data: bytes,
) -> bytes:
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w", format=tarfile.GNU_FORMAT) as archive:
        members = [(RELEASE_MANIFEST_NAME, manifest_data, 0o644)]
        members.extend(
            (
                item["path"],
                content[item["path"]],
                int(item["mode"], 8),
            )
            for item in inventory
        )
        for relative, data, mode in sorted(members, key=lambda item: item[0]):
            info = tarfile.TarInfo(f"{spec['package_root']}/{relative}")
            info.size = len(data)
            info.mtime = spec["source_date_epoch"]
            info.mode = mode
            info.uid = 0
            info.gid = 0
            info.uname = "root"
            info.gname = "root"
            archive.addfile(info, io.BytesIO(data))
    data = output.getvalue()
    if len(data) > MAX_ARCHIVE_SIZE:
        raise ReleaseError("canonical release archive exceeds size bound")
    return data


def build_release(spec_path: Path, repo_root: Path, output_dir: Path) -> dict[str, Any]:
    """Build a byte-reproducible uncompressed tar from clean tracked files."""

    repo_root = repo_root.resolve()
    spec = load_release_spec(spec_path)
    paths = [PurePosixPath(value) for value in spec["package_files"]]
    _tracked_package_sources(repo_root, paths)
    inventory, content = _source_inventory(repo_root, paths)
    release_manifest = {
        "release_manifest_schema_version": 1,
        "release_id": spec["release_id"],
        "toolkit_version": spec["toolkit_version"],
        "release_spec_path": RELEASE_SPEC_RELATIVE.as_posix(),
        "source_date_epoch": spec["source_date_epoch"],
        "source_tree_sha256": _tree_id(inventory),
        "files": inventory,
    }
    manifest_data = _canonical_json(release_manifest)
    archive_data = _canonical_tar_bytes(spec, inventory, content, manifest_data)

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / spec["archive_name"]
    temporary = output_dir / f".{spec['archive_name']}.tmp-{os.getpid()}"
    try:
        with temporary.open("xb") as raw:
            raw.write(archive_data)
            raw.flush()
            os.fsync(raw.fileno())
        os.replace(temporary, archive_path)
    finally:
        temporary.unlink(missing_ok=True)

    archive_sha256 = _sha256(archive_path.read_bytes())
    sidecar = archive_path.with_name(f"{archive_path.name}.sha256")
    sidecar.write_text(f"{archive_sha256}  {archive_path.name}\n", encoding="ascii")
    return {
        "release_id": spec["release_id"],
        "archive": archive_path,
        "archive_sha256": archive_sha256,
        "source_tree_sha256": release_manifest["source_tree_sha256"],
        "file_count": len(inventory),
    }


def _archive_files(archive_path: Path) -> tuple[str, dict[str, tuple[tarfile.TarInfo, bytes]]]:
    try:
        archive_size = archive_path.stat().st_size
    except OSError as error:
        raise ReleaseError(f"cannot inspect release archive {archive_path}: {error}") from error
    if archive_size <= 0 or archive_size > MAX_ARCHIVE_SIZE:
        raise ReleaseError(f"release archive size is outside the accepted bound: {archive_size}")
    try:
        archive = tarfile.open(archive_path, mode="r:")
    except (OSError, tarfile.TarError) as error:
        raise ReleaseError(f"cannot open release archive {archive_path}: {error}") from error
    with archive:
        members: dict[str, tuple[tarfile.TarInfo, bytes]] = {}
        roots: set[str] = set()
        for info in archive.getmembers():
            path = PurePosixPath(info.name)
            if path.is_absolute() or len(path.parts) < 2 or any(
                part in {"", ".", ".."} for part in path.parts
            ):
                raise ReleaseError(f"unsafe archive member path: {info.name!r}")
            roots.add(path.parts[0])
            relative = PurePosixPath(*path.parts[1:])
            _relative_path(relative.as_posix(), "archive member")
            if info.name != f"{path.parts[0]}/{relative.as_posix()}":
                raise ReleaseError(f"archive member path is not canonical: {info.name!r}")
            if not info.isreg() or info.issym() or info.islnk():
                raise ReleaseError(f"archive member is not a regular file: {info.name}")
            if relative.as_posix() in members:
                raise ReleaseError(f"duplicate archive member: {relative}")
            if info.size < 0 or info.size > MAX_ARCHIVE_FILE_SIZE:
                raise ReleaseError(f"archive member exceeds size bound: {relative}")
            extracted = archive.extractfile(info)
            if extracted is None:
                raise ReleaseError(f"cannot read archive member: {relative}")
            data = extracted.read(MAX_ARCHIVE_FILE_SIZE + 1)
            if len(data) != info.size:
                raise ReleaseError(f"archive member size changed while reading: {relative}")
            members[relative.as_posix()] = (info, data)
        if len(roots) != 1:
            raise ReleaseError("release archive must contain exactly one package root")
        return next(iter(roots)), members


def verify_release(archive_path: Path) -> dict[str, Any]:
    """Verify archive topology, strict spec, inventory, bytes, modes, and epoch."""

    package_root, members = _archive_files(archive_path)
    if RELEASE_MANIFEST_NAME not in members:
        raise ReleaseError("release archive lacks RELEASE-MANIFEST.json")
    manifest_data = members[RELEASE_MANIFEST_NAME][1]
    manifest = _parse_json(manifest_data, "release archive manifest")
    if not isinstance(manifest, dict) or set(manifest) != {
        "release_manifest_schema_version",
        "release_id",
        "toolkit_version",
        "release_spec_path",
        "source_date_epoch",
        "source_tree_sha256",
        "files",
    }:
        raise ReleaseError("release archive manifest fields do not match schema 1")
    if manifest["release_manifest_schema_version"] != 1:
        raise ReleaseError("release archive manifest schema must be 1")
    _digest(manifest["source_tree_sha256"], "source_tree_sha256")
    if manifest_data != _canonical_json(manifest):
        raise ReleaseError("release archive manifest is not canonically encoded")

    spec_relative = _relative_path(manifest["release_spec_path"], "release_spec_path")
    if spec_relative != RELEASE_SPEC_RELATIVE:
        raise ReleaseError("release archive selects an unknown release spec path")
    if spec_relative.as_posix() not in members:
        raise ReleaseError("release archive lacks its selected release spec")
    spec = _parse_json(members[spec_relative.as_posix()][1], "archived release spec")
    _validate_release_spec(spec)
    if (
        package_root != spec["package_root"]
        or manifest["release_id"] != spec["release_id"]
        or manifest["toolkit_version"] != spec["toolkit_version"]
        or manifest["source_date_epoch"] != spec["source_date_epoch"]
    ):
        raise ReleaseError("release archive identity fields disagree")

    files = manifest["files"]
    if not isinstance(files, list):
        raise ReleaseError("release archive files must be an array")
    paths: list[str] = []
    normalized: list[dict[str, object]] = []
    for index, item in enumerate(files):
        if not isinstance(item, dict) or set(item) != {"path", "size", "sha256", "mode"}:
            raise ReleaseError(f"release archive files[{index}] is malformed")
        relative = _relative_path(item["path"], f"files[{index}].path")
        if (
            not isinstance(item["size"], int)
            or isinstance(item["size"], bool)
            or item["size"] < 0
            or item["size"] > MAX_ARCHIVE_FILE_SIZE
        ):
            raise ReleaseError(f"files[{index}].size is invalid")
        digest = _digest(item["sha256"], f"files[{index}].sha256")
        if item["mode"] not in {"0644", "0755"}:
            raise ReleaseError(f"files[{index}].mode is invalid")
        path_text = relative.as_posix()
        paths.append(path_text)
        normalized.append(
            {
                "path": path_text,
                "size": item["size"],
                "sha256": digest,
                "mode": item["mode"],
            }
        )
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise ReleaseError("release archive file inventory must be sorted and unique")
    if paths != spec["package_files"]:
        raise ReleaseError("release archive file inventory disagrees with release spec")
    if set(members) != set(paths) | {RELEASE_MANIFEST_NAME}:
        raise ReleaseError("release archive contains missing or unlisted content")
    if _tree_id(normalized) != manifest["source_tree_sha256"]:
        raise ReleaseError("release archive source tree digest disagrees")

    manifest_info = members[RELEASE_MANIFEST_NAME][0]
    if (
        manifest_info.mtime != spec["source_date_epoch"]
        or manifest_info.uid != 0
        or manifest_info.gid != 0
        or manifest_info.uname != "root"
        or manifest_info.gname != "root"
        or stat.S_IMODE(manifest_info.mode) != 0o644
    ):
        raise ReleaseError("release archive manifest metadata disagrees")
    content: dict[str, bytes] = {}
    for item in normalized:
        info, data = members[item["path"]]
        if (
            info.mtime != spec["source_date_epoch"]
            or info.uid != 0
            or info.gid != 0
            or info.uname != "root"
            or info.gname != "root"
        ):
            raise ReleaseError(f"release member metadata disagrees: {item['path']}")
        if stat.S_IMODE(info.mode) != int(item["mode"], 8):
            raise ReleaseError(f"release member mode disagrees: {item['path']}")
        if len(data) != item["size"] or _sha256(data) != item["sha256"]:
            raise ReleaseError(f"release member bytes disagree: {item['path']}")
        content[item["path"]] = data

    canonical_archive = _canonical_tar_bytes(spec, normalized, content, manifest_data)
    actual_archive = archive_path.read_bytes()
    if actual_archive != canonical_archive:
        raise ReleaseError("release archive is not the exact canonical tar encoding")

    return {
        "release_id": spec["release_id"],
        "toolkit_version": spec["toolkit_version"],
        "package_root": package_root,
        "archive_sha256": _sha256(actual_archive),
        "source_tree_sha256": manifest["source_tree_sha256"],
        "file_count": len(normalized),
        "manifest": manifest,
        "members": members,
    }


def _install_state(path: Path) -> dict[str, Any] | None:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return None
    except OSError as error:
        raise ReleaseError(f"cannot inspect install state {path}: {error}") from error
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_nlink != 1
        or stat.S_IMODE(metadata.st_mode) != 0o644
    ):
        raise ReleaseError(
            f"install state is not a canonical single-link regular file: {path}"
        )
    if metadata.st_size > MAX_ARCHIVE_FILE_SIZE:
        raise ReleaseError(f"install state exceeds size bound: {path}")
    data = path.read_bytes()
    value = _parse_json(data, f"install state {path}")
    if not isinstance(value, dict) or list(value) != [
        "install_state_schema_version",
        "current",
        "rollback",
        "installed_releases",
    ]:
        raise ReleaseError("install state fields do not match schema 2")
    if value["install_state_schema_version"] != 2:
        raise ReleaseError("install state schema must be 2")
    if data != _canonical_json(value):
        raise ReleaseError("install state is not canonically encoded")
    if value["current"] is not None and (
        not isinstance(value["current"], str) or not value["current"]
    ):
        raise ReleaseError("install state current value is invalid")
    if not isinstance(value["rollback"], list) or any(
        not isinstance(item, str) or not item for item in value["rollback"]
    ):
        raise ReleaseError("install state rollback history is invalid")
    if value["current"] is not None:
        _release_id(value["current"], "install state current")
    for index, item in enumerate(value["rollback"]):
        _release_id(item, f"install state rollback[{index}]")
    if len(value["rollback"]) != len(set(value["rollback"])):
        raise ReleaseError("install state rollback history contains duplicates")
    if value["current"] in value["rollback"]:
        raise ReleaseError("install state current release also appears in rollback history")
    if value["current"] is None and value["rollback"]:
        raise ReleaseError("install state without a current release cannot retain rollback history")
    installed_releases = value["installed_releases"]
    if not isinstance(installed_releases, dict):
        raise ReleaseError("install state installed_releases must be an object")
    if list(installed_releases) != sorted(installed_releases):
        raise ReleaseError("install state installed_releases keys are not canonical")
    for release_id, lock in installed_releases.items():
        _release_id(release_id, "install state installed release ID")
        if not isinstance(lock, dict) or list(lock) != [
            "archive_sha256",
            "manifest_sha256",
            "source_tree_sha256",
        ]:
            raise ReleaseError(f"install state lock fields disagree: {release_id}")
        for field in ("archive_sha256", "manifest_sha256", "source_tree_sha256"):
            _digest(lock[field], f"install state {release_id} {field}")
    selected_ids = set(value["rollback"])
    if value["current"] is not None:
        selected_ids.add(value["current"])
    if not selected_ids.issubset(installed_releases):
        raise ReleaseError("install state selection references an unlocked release")
    if value["current"] is None and installed_releases:
        raise ReleaseError("install state without a current release cannot retain releases")
    return value


def _write_state(path: Path, value: dict[str, Any]) -> None:
    descriptor = -1
    temporary: Path | None = None
    try:
        descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.tmp-", dir=path.parent)
        temporary = Path(name)
        with os.fdopen(descriptor, "wb") as output:
            descriptor = -1
            os.fchmod(output.fileno(), 0o644)
            output.write(_canonical_json(value))
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
        temporary = None
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _directory_non_link(
    path: Path,
    *,
    label: str,
    create: bool,
    parents: bool = False,
    expected_mode: int | None = None,
) -> Path:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        if not create:
            raise ReleaseError(f"{label} does not exist: {path}") from None
        try:
            path.mkdir(parents=parents)
            if expected_mode is not None:
                os.chmod(path, expected_mode)
            metadata = path.lstat()
        except OSError as error:
            raise ReleaseError(f"cannot create {label} {path}: {error}") from error
    except OSError as error:
        raise ReleaseError(f"cannot inspect {label} {path}: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ReleaseError(f"{label} is not a directory non-link: {path}")
    if expected_mode is not None and stat.S_IMODE(metadata.st_mode) != expected_mode:
        raise ReleaseError(
            f"{label} mode is not canonical {expected_mode:04o}: {path}"
        )
    return path


def _verify_install_root(root: Path, *, create: bool) -> Path:
    return _directory_non_link(
        root.absolute(), label="install root", create=create, parents=True
    )


def _verify_releases_root(root: Path, *, create: bool) -> Path:
    return _directory_non_link(
        root / "releases",
        label="release directory",
        create=create,
        expected_mode=0o755,
    )


def _verify_installed_release(
    path: Path, expected_id: str, expected_lock: dict[str, str]
) -> dict[str, Any]:
    _directory_non_link(
        path,
        label=f"installed release {expected_id}",
        create=False,
        expected_mode=0o755,
    )
    manifest_path = path / RELEASE_MANIFEST_NAME
    try:
        metadata = manifest_path.lstat()
    except OSError as error:
        raise ReleaseError(f"cannot inspect installed release {expected_id}: {error}") from error
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_nlink != 1
        or stat.S_IMODE(metadata.st_mode) != 0o644
    ):
        raise ReleaseError(
            f"installed release manifest is not a canonical single-link regular file: "
            f"{manifest_path}"
        )
    if metadata.st_size > MAX_ARCHIVE_FILE_SIZE:
        raise ReleaseError(f"installed release manifest exceeds size bound: {expected_id}")
    try:
        manifest_data = manifest_path.read_bytes()
    except OSError as error:
        raise ReleaseError(
            f"cannot read installed release manifest {expected_id}: {error}"
        ) from error
    manifest = _parse_json(manifest_data, f"installed release {expected_id}")
    if manifest_data != _canonical_json(manifest):
        raise ReleaseError(f"installed release manifest is not canonical: {expected_id}")
    if _sha256(manifest_data) != expected_lock["manifest_sha256"]:
        raise ReleaseError(f"installed release manifest lock disagrees: {expected_id}")
    if not isinstance(manifest, dict) or set(manifest) != {
        "release_manifest_schema_version",
        "release_id",
        "toolkit_version",
        "release_spec_path",
        "source_date_epoch",
        "source_tree_sha256",
        "files",
    }:
        raise ReleaseError(f"installed release manifest fields disagree: {expected_id}")
    if manifest["release_manifest_schema_version"] != 1:
        raise ReleaseError(f"installed release manifest schema disagrees: {expected_id}")
    release_id = _release_id(manifest["release_id"], "installed release manifest ID")
    if release_id != expected_id:
        raise ReleaseError(f"installed release identity disagrees: {expected_id}")
    _release_id(expected_id, "installed release ID")
    toolkit_version = manifest["toolkit_version"]
    if (
        not isinstance(toolkit_version, str)
        or re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", toolkit_version) is None
        or expected_id != f"ablpc-toolkit-v{toolkit_version}"
    ):
        raise ReleaseError(f"installed release toolkit version disagrees: {expected_id}")
    spec_relative = _relative_path(
        manifest["release_spec_path"], "installed release_spec_path"
    )
    if spec_relative != RELEASE_SPEC_RELATIVE:
        raise ReleaseError(f"installed release spec path disagrees: {expected_id}")
    source_date_epoch = manifest["source_date_epoch"]
    if (
        not isinstance(source_date_epoch, int)
        or isinstance(source_date_epoch, bool)
        or source_date_epoch <= 0
    ):
        raise ReleaseError(f"installed release source epoch is invalid: {expected_id}")
    _digest(manifest["source_tree_sha256"], "installed source_tree_sha256")
    files = manifest.get("files")
    if not isinstance(files, list):
        raise ReleaseError(f"installed release inventory is invalid: {expected_id}")
    expected_paths = {RELEASE_MANIFEST_NAME}
    expected_directories: set[str] = set()
    normalized: list[dict[str, object]] = []
    content: dict[str, bytes] = {}
    for index, item in enumerate(files):
        if not isinstance(item, dict) or set(item) != {"path", "size", "sha256", "mode"}:
            raise ReleaseError(f"installed release inventory item {index} is invalid")
        relative = _relative_path(item["path"], f"installed files[{index}].path")
        relative_text = relative.as_posix()
        if relative_text == RELEASE_MANIFEST_NAME or relative_text in expected_paths:
            raise ReleaseError(f"installed release inventory contains duplicate path: {relative}")
        if (
            not isinstance(item["size"], int)
            or isinstance(item["size"], bool)
            or item["size"] < 0
            or item["size"] > MAX_ARCHIVE_FILE_SIZE
        ):
            raise ReleaseError(f"installed release file size is invalid: {relative}")
        _digest(item["sha256"], f"installed files[{index}].sha256")
        if item["mode"] not in {"0644", "0755"}:
            raise ReleaseError(f"installed release file mode is invalid: {relative}")
        target = path.joinpath(*relative.parts)
        try:
            target_metadata = target.lstat()
        except OSError as error:
            raise ReleaseError(f"cannot inspect installed release file {relative}: {error}") from error
        if (
            stat.S_ISLNK(target_metadata.st_mode)
            or not stat.S_ISREG(target_metadata.st_mode)
            or target_metadata.st_nlink != 1
        ):
            raise ReleaseError(
                f"installed release file is not single-link regular: {relative}"
            )
        if target_metadata.st_size != item["size"]:
            raise ReleaseError(f"installed release file disagrees: {relative}")
        try:
            data = target.read_bytes()
        except OSError as error:
            raise ReleaseError(f"cannot read installed release file {relative}: {error}") from error
        if (
            len(data) != item["size"]
            or _sha256(data) != item["sha256"]
            or stat.S_IMODE(target_metadata.st_mode) != int(item["mode"], 8)
        ):
            raise ReleaseError(f"installed release file disagrees: {relative}")
        expected_paths.add(relative_text)
        content[relative_text] = data
        for parent in relative.parents:
            if parent != PurePosixPath("."):
                expected_directories.add(parent.as_posix())
        normalized.append(item)
    normalized_paths = [item["path"] for item in normalized]
    if normalized_paths != sorted(normalized_paths) or len(normalized_paths) != len(
        set(normalized_paths)
    ):
        raise ReleaseError(f"installed release inventory order disagrees: {expected_id}")
    if _tree_id(normalized) != manifest["source_tree_sha256"]:
        raise ReleaseError(f"installed release tree digest disagrees: {expected_id}")
    if manifest["source_tree_sha256"] != expected_lock["source_tree_sha256"]:
        raise ReleaseError(f"installed release tree lock disagrees: {expected_id}")

    spec_data = content.get(RELEASE_SPEC_RELATIVE.as_posix())
    if spec_data is None:
        raise ReleaseError(f"installed release lacks its canonical spec: {expected_id}")
    spec = _parse_json(spec_data, f"installed release spec {expected_id}")
    _validate_release_spec(spec)
    if (
        spec["release_id"] != expected_id
        or spec["toolkit_version"] != toolkit_version
        or spec["source_date_epoch"] != source_date_epoch
        or spec["package_files"] != normalized_paths
    ):
        raise ReleaseError(f"installed release manifest and spec disagree: {expected_id}")
    installed_archive = _canonical_tar_bytes(spec, normalized, content, manifest_data)
    if _sha256(installed_archive) != expected_lock["archive_sha256"]:
        raise ReleaseError(f"installed release archive lock disagrees: {expected_id}")

    actual_paths: set[str] = set()
    actual_directories: set[str] = set()
    try:
        for target in path.rglob("*"):
            relative = target.relative_to(path).as_posix()
            target_metadata = target.lstat()
            if stat.S_ISLNK(target_metadata.st_mode):
                raise ReleaseError(
                    f"installed release contains unsupported entry: {relative}"
                )
            if stat.S_ISDIR(target_metadata.st_mode):
                if stat.S_IMODE(target_metadata.st_mode) != 0o755:
                    raise ReleaseError(
                        f"installed release directory mode disagrees: {relative}"
                    )
                actual_directories.add(relative)
            elif stat.S_ISREG(target_metadata.st_mode):
                actual_paths.add(relative)
            else:
                raise ReleaseError(
                    f"installed release contains unsupported entry: {relative}"
                )
    except OSError as error:
        raise ReleaseError(f"cannot enumerate installed release {expected_id}: {error}") from error
    if actual_paths != expected_paths or actual_directories != expected_directories:
        raise ReleaseError(
            f"installed release contains missing or extra topology: {expected_id}"
        )
    return manifest


def _empty_install_state() -> dict[str, Any]:
    return {
        "install_state_schema_version": 2,
        "current": None,
        "rollback": [],
        "installed_releases": {},
    }


def _install_releases_root(root: Path, state: dict[str, Any]) -> Path:
    releases_path = root / "releases"
    try:
        releases_path.lstat()
    except FileNotFoundError:
        if state["current"] is not None:
            raise ReleaseError(f"release directory does not exist: {releases_path}") from None
        return _verify_releases_root(root, create=True)
    except OSError as error:
        raise ReleaseError(
            f"cannot inspect release directory {releases_path}: {error}"
        ) from error

    releases = _verify_releases_root(root, create=False)
    if state["current"] is None:
        try:
            next(releases.iterdir())
        except StopIteration:
            pass
        except OSError as error:
            raise ReleaseError(
                f"cannot enumerate unselected release directory {releases}: {error}"
            ) from error
        else:
            raise ReleaseError(
                "install state is missing a selection for a non-empty release directory"
            )
    return releases


def _verify_release_repository(releases: Path, state: dict[str, Any]) -> None:
    required_ids = set(state["rollback"])
    if state["current"] is not None:
        required_ids.add(state["current"])
    actual_ids: set[str] = set()
    try:
        entries = sorted(releases.iterdir(), key=lambda item: item.name)
    except OSError as error:
        raise ReleaseError(f"cannot enumerate release directory {releases}: {error}") from error
    for entry in entries:
        release_id = _release_id(entry.name, "installed release directory name")
        lock = state["installed_releases"].get(release_id)
        if lock is None:
            raise ReleaseError(f"installed release lacks a state lock: {release_id}")
        _verify_installed_release(entry, release_id, lock)
        actual_ids.add(release_id)
    expected_ids = set(state["installed_releases"])
    missing = sorted(expected_ids - actual_ids)
    extra = sorted(actual_ids - expected_ids)
    if missing or extra or not required_ids.issubset(actual_ids):
        detail = []
        if missing:
            detail.append(f"missing: {', '.join(missing)}")
        if extra:
            detail.append(f"unlocked: {', '.join(extra)}")
        raise ReleaseError(
            f"install state and release directory disagree ({'; '.join(detail)})"
        )


def _verification_lock(verification: dict[str, Any]) -> dict[str, str]:
    return {
        "archive_sha256": verification["archive_sha256"],
        "manifest_sha256": _sha256(_canonical_json(verification["manifest"])),
        "source_tree_sha256": verification["source_tree_sha256"],
    }


def install_release(archive_path: Path, install_root: Path) -> dict[str, Any]:
    """Verify and install one immutable version, then atomically select it."""

    verification = verify_release(archive_path)
    release_lock = _verification_lock(verification)
    root = _verify_install_root(install_root, create=True)
    state_path = root / INSTALL_STATE_NAME
    state = _install_state(state_path) or _empty_install_state()
    releases = _install_releases_root(root, state)
    _verify_release_repository(releases, state)

    release_id = verification["release_id"]
    destination = releases / release_id
    if destination.exists() or destination.is_symlink():
        raise ReleaseError(f"release is already installed: {release_id}")
    temporary = Path(tempfile.mkdtemp(prefix=".install-", dir=releases))
    installed = False
    try:
        manifest = verification["manifest"]
        members = verification["members"]
        for relative in [RELEASE_MANIFEST_NAME] + [
            item["path"] for item in manifest["files"]
        ]:
            target_relative = _relative_path(relative, "install member")
            target = temporary.joinpath(*target_relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            info, data = members[target_relative.as_posix()]
            with target.open("xb") as output:
                output.write(data)
            os.chmod(target, stat.S_IMODE(info.mode))
        os.chmod(temporary, 0o755)
        for target in temporary.rglob("*"):
            if target.is_dir():
                os.chmod(target, 0o755)
        _verify_installed_release(temporary, release_id, release_lock)
        os.replace(temporary, destination)
        installed = True
        rollback = list(state["rollback"])
        if state["current"] is not None:
            rollback.append(state["current"])
        installed_releases = dict(state["installed_releases"])
        installed_releases[release_id] = release_lock
        installed_releases = dict(sorted(installed_releases.items()))
        next_state = {
            "install_state_schema_version": 2,
            "current": release_id,
            "rollback": rollback,
            "installed_releases": installed_releases,
        }
        try:
            _write_state(state_path, next_state)
        except Exception:
            shutil.rmtree(destination)
            installed = False
            raise
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    if not installed:
        raise ReleaseError(f"release installation did not complete: {release_id}")
    return {
        "release_id": release_id,
        "current": release_id,
        "rollback": next_state["rollback"],
        "install_path": destination,
    }


def rollback_release(install_root: Path) -> dict[str, Any]:
    """Atomically select the last verified installed version without deleting files."""

    root = _verify_install_root(install_root, create=False)
    state_path = root / INSTALL_STATE_NAME
    state = _install_state(state_path)
    if state is None or state["current"] is None:
        raise ReleaseError("no current release is installed")
    if not state["rollback"]:
        raise ReleaseError("no prior release is available for rollback")
    releases = _verify_releases_root(root, create=False)
    _verify_release_repository(releases, state)
    candidate = state["rollback"][-1]
    next_state = {
        "install_state_schema_version": 2,
        "current": candidate,
        "rollback": state["rollback"][:-1],
        "installed_releases": state["installed_releases"],
    }
    _write_state(state_path, next_state)
    return {
        "previous": state["current"],
        "current": candidate,
        "rollback": next_state["rollback"],
        "install_path": releases / candidate,
    }


def current_release(install_root: Path) -> dict[str, Any]:
    """Return the current verified release selection."""

    root = _verify_install_root(install_root, create=False)
    state = _install_state(root / INSTALL_STATE_NAME)
    if state is None or state["current"] is None:
        raise ReleaseError("no current release is installed")
    releases = _verify_releases_root(root, create=False)
    path = releases / state["current"]
    _verify_release_repository(releases, state)
    return {
        "current": state["current"],
        "rollback": state["rollback"],
        "install_path": path,
    }
