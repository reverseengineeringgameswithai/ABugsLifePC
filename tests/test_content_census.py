from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from reimplementation.ablpc.content_census import (
    ContentCensusError,
    build_content_census,
    normalize_loaded_path,
)


def test_normalize_loaded_path_requires_explicit_load_line() -> None:
    assert (
        normalize_loaded_path(
            r"LOAD : Loading file R:\PC\BUGS\cd\chars\flick.all."
        )
        == "cd/chars/flick.all"
    )
    assert (
        normalize_loaded_path(
            r"LOAD : Getting length of file \pc\bugs\cd\chars\flick.all."
        )
        is None
    )
    assert normalize_loaded_path("LOAD: Type 34, anim 12 setup.") is None


def test_content_census_hashes_metadata_and_matches_logs(tmp_path: Path) -> None:
    source = tmp_path / "PC" / "BUGS"
    (source / "CD" / "CHARS").mkdir(parents=True)
    first = source / "CD" / "CHARS" / "FLICK.ALL"
    second = source / "CD" / "CHARS" / "COPY.ALL"
    first.write_bytes(b"same")
    second.write_bytes(b"same")
    (source / "bugs.exe").write_bytes(b"exe")
    (source / "bugs.log").write_bytes(b"generated")
    log = tmp_path / "bugs.log"
    log.write_text(
        "LOAD : Loading file R:\\PC\\BUGS\\cd\\chars\\flick.all.\n"
        "LOAD : Loading file R:\\PC\\BUGS\\cd\\missing.raw.\n",
        encoding="utf-8",
    )

    census = build_content_census(source, [("control", log)])

    assert census["totals"] == {
        "file_count": 3,
        "byte_count": 11,
        "observed_file_count": 1,
        "duplicate_hash_group_count": 1,
        "files_in_duplicate_hash_groups": 2,
    }
    assert census["excluded_paths"] == ["bugs.log"]
    file_by_path = {entry["path"]: entry for entry in census["files"]}
    assert file_by_path["CD/CHARS/FLICK.ALL"]["sha256"] == hashlib.sha256(
        b"same"
    ).hexdigest()
    assert census["loader_logs"][0]["matched_paths"] == ["CD/CHARS/FLICK.ALL"]
    assert census["loader_logs"][0]["unmatched_paths"] == ["cd/missing.raw"]
    assert census["duplicate_hash_groups"][0]["file_count"] == 2


def test_content_census_rejects_case_collisions(tmp_path: Path) -> None:
    (tmp_path / "name.raw").write_bytes(b"a")
    (tmp_path / "NAME.RAW").write_bytes(b"b")

    with pytest.raises(ContentCensusError, match="case-insensitive duplicate"):
        build_content_census(tmp_path)


def test_content_census_rejects_protected_source_root(tmp_path: Path) -> None:
    protected = tmp_path / "originals" / "game"
    protected.mkdir(parents=True)

    with pytest.raises(ContentCensusError, match="protected content root"):
        build_content_census(protected)
