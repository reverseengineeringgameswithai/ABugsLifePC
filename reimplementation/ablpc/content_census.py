"""Metadata-only census for a derived PC game work tree.

This module reads and hashes files but never copies their contents into a report.
Runtime loader context is limited to explicit ``LOAD : Loading file`` log lines.
"""

from __future__ import annotations

from collections import defaultdict
import hashlib
from pathlib import Path, PurePosixPath
from typing import Iterable


class ContentCensusError(ValueError):
    """Raised when a work tree or loader path is unsafe or ambiguous."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_loaded_path(line: str) -> str | None:
    """Extract a PC/BUGS-relative path from an explicit game load-log line."""

    marker = "load : loading file "
    stripped = line.lstrip()
    if not stripped.casefold().startswith(marker):
        return None
    value = stripped[len(marker) :].strip()
    if value.endswith("."):
        value = value[:-1]
    value = value.replace("/", "\\")
    lowered_value = value.casefold()
    root_marker = "\\pc\\bugs\\"
    root_index = lowered_value.find(root_marker)
    if root_index < 0:
        return None
    relative = value[root_index + len(root_marker) :].replace("\\", "/")
    path = PurePosixPath(relative)
    if not relative or path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ContentCensusError(f"unsafe loaded path in log line: {line!r}")
    return path.as_posix()


def loaded_paths_from_log(path: Path | str) -> tuple[str, ...]:
    log_path = Path(path)
    observed: set[str] = set()
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        relative = normalize_loaded_path(line)
        if relative is not None:
            observed.add(relative)
    return tuple(sorted(observed, key=str.casefold))


def build_content_census(
    source_root: Path | str,
    logs: Iterable[tuple[str, Path | str]] = (),
    *,
    excluded_paths: Iterable[str] = ("bugs.log",),
) -> dict[str, object]:
    source = Path(source_root).resolve()
    if not source.is_dir():
        raise ContentCensusError(f"source root is not a directory: {source}")
    if any(part.casefold() in {"originals", "media"} for part in source.parts):
        raise ContentCensusError(
            f"refusing protected content root; census a derived work copy: {source}"
        )

    excluded = {PurePosixPath(value).as_posix().casefold() for value in excluded_paths}
    files: list[dict[str, object]] = []
    path_by_casefold: dict[str, str] = {}
    for path in sorted(source.rglob("*"), key=lambda item: item.as_posix().casefold()):
        if path.is_symlink():
            raise ContentCensusError(f"refusing symlink in census source: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(source).as_posix()
        if relative.casefold() in excluded:
            continue
        folded = relative.casefold()
        if folded in path_by_casefold:
            raise ContentCensusError(
                f"case-insensitive duplicate paths: {path_by_casefold[folded]!r} "
                f"and {relative!r}"
            )
        path_by_casefold[folded] = relative
        size = path.stat().st_size
        files.append(
            {
                "path": relative,
                "size": size,
                "sha256": sha256_file(path),
                "extension": _extension(relative),
                "family": _family(relative),
                "observed_in": [],
            }
        )

    log_reports: list[dict[str, object]] = []
    labels: set[str] = set()
    file_by_folded_path = {entry["path"].casefold(): entry for entry in files}
    for label, log_path_value in logs:
        if not label or label in labels:
            raise ContentCensusError(f"log labels must be non-empty and unique: {label!r}")
        labels.add(label)
        log_path = Path(log_path_value)
        observed_paths = loaded_paths_from_log(log_path)
        matched: list[str] = []
        unmatched: list[str] = []
        for observed in observed_paths:
            entry = file_by_folded_path.get(observed.casefold())
            if entry is None:
                unmatched.append(observed)
                continue
            matched.append(entry["path"])
            entry["observed_in"].append(label)
        log_reports.append(
            {
                "label": label,
                "path": log_path.as_posix(),
                "sha256": sha256_file(log_path),
                "observed_path_count": len(observed_paths),
                "matched_paths": sorted(matched, key=str.casefold),
                "unmatched_paths": sorted(unmatched, key=str.casefold),
            }
        )

    extensions = _summarize(files, "extension")
    families = _summarize(files, "family")
    hashes: dict[tuple[str, int], list[str]] = defaultdict(list)
    for entry in files:
        hashes[(entry["sha256"], entry["size"])].append(entry["path"])
    duplicate_groups = [
        {
            "sha256": digest,
            "size": size,
            "file_count": len(paths),
            "paths": sorted(paths, key=str.casefold),
        }
        for (digest, size), paths in hashes.items()
        if len(paths) > 1
    ]
    duplicate_groups.sort(key=lambda group: (-group["file_count"], group["sha256"]))

    fingerprint = hashlib.sha256()
    for entry in files:
        fingerprint.update(entry["path"].encode("utf-8"))
        fingerprint.update(b"\0")
        fingerprint.update(str(entry["size"]).encode("ascii"))
        fingerprint.update(b"\0")
        fingerprint.update(entry["sha256"].encode("ascii"))
        fingerprint.update(b"\n")

    observed_files = sum(bool(entry["observed_in"]) for entry in files)
    return {
        "schema_version": 1,
        "source_root": source.as_posix(),
        "excluded_paths": sorted(excluded),
        "tree_fingerprint_sha256": fingerprint.hexdigest(),
        "totals": {
            "file_count": len(files),
            "byte_count": sum(entry["size"] for entry in files),
            "observed_file_count": observed_files,
            "duplicate_hash_group_count": len(duplicate_groups),
            "files_in_duplicate_hash_groups": sum(
                group["file_count"] for group in duplicate_groups
            ),
        },
        "extensions": extensions,
        "families": families,
        "loader_logs": log_reports,
        "duplicate_hash_groups": duplicate_groups,
        "files": files,
    }


def render_summary(census: dict[str, object]) -> str:
    totals = census["totals"]
    lines = [
        "# PC content census",
        "",
        f"Source root: `{census['source_root']}`",
        "",
        f"Tree fingerprint SHA-256: `{census['tree_fingerprint_sha256']}`",
        "",
        f"Explicit exclusions: `{', '.join(census['excluded_paths'])}`",
        "",
        "## Totals",
        "",
        f"- Files: {totals['file_count']}",
        f"- Bytes: {totals['byte_count']}",
        f"- Files observed in supplied loader logs: {totals['observed_file_count']}",
        f"- Duplicate hash groups: {totals['duplicate_hash_group_count']}",
        f"- Files in duplicate hash groups: {totals['files_in_duplicate_hash_groups']}",
        "",
        "## Extensions",
        "",
        "| Extension | Files | Bytes | Loader-observed files |",
        "|---|---:|---:|---:|",
    ]
    for entry in census["extensions"]:
        lines.append(
            f"| `{entry['name']}` | {entry['file_count']} | {entry['byte_count']} | "
            f"{entry['observed_file_count']} |"
        )
    lines.extend(
        [
            "",
            "## Families",
            "",
            "| Family | Files | Bytes | Loader-observed files |",
            "|---|---:|---:|---:|",
        ]
    )
    for entry in census["families"]:
        lines.append(
            f"| `{entry['name']}` | {entry['file_count']} | {entry['byte_count']} | "
            f"{entry['observed_file_count']} |"
        )
    lines.extend(["", "## Loader logs", ""])
    for log in census["loader_logs"]:
        lines.extend(
            [
                f"### {log['label']}",
                "",
                f"- Path: `{log['path']}`",
                f"- SHA-256: `{log['sha256']}`",
                f"- Explicit loaded paths: {log['observed_path_count']}",
                f"- Matched inventory paths: {len(log['matched_paths'])}",
                f"- Unmatched paths: {len(log['unmatched_paths'])}",
                "",
            ]
        )
    lines.extend(
        [
            "The companion JSON contains every relative path, size, SHA-256,",
            "extension/family label, duplicate group, and loader-log match. It",
            "contains metadata only, not game-file payload bytes.",
            "",
        ]
    )
    return "\n".join(lines)


def _extension(relative: str) -> str:
    suffix = PurePosixPath(relative).suffix
    return suffix[1:].casefold() if suffix else "[none]"


def _family(relative: str) -> str:
    parts = PurePosixPath(relative).parts
    if len(parts) == 1:
        return "[root]"
    if parts[0].casefold() != "cd":
        return parts[0].upper()
    if len(parts) == 2:
        return "CD/[root]"
    return f"CD/{parts[1].upper()}"


def _summarize(files: list[dict[str, object]], key: str) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, int]] = defaultdict(
        lambda: {"file_count": 0, "byte_count": 0, "observed_file_count": 0}
    )
    for entry in files:
        group = grouped[entry[key]]
        group["file_count"] += 1
        group["byte_count"] += entry["size"]
        group["observed_file_count"] += bool(entry["observed_in"])
    return [
        {"name": name, **values}
        for name, values in sorted(grouped.items(), key=lambda item: item[0].casefold())
    ]
