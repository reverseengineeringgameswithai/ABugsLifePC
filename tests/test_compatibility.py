from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from reimplementation.ablpc.compatibility import (
    CompatibilityError,
    EXPECTED_MACHINE_AUTHORITY_SHA256,
    EXPECTED_STATEMENT,
    EXPECTED_STATEMENT_V0_1,
    EXPECTED_STATEMENT_V0_2,
    HISTORICAL_STATEMENT_RELATIVE,
    STATEMENT_RELATIVE,
    check_compatibility_statement,
    load_compatibility_statement,
    validate_compatibility_statement,
    validate_repository_alignment,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
STATEMENT_PATH = REPO_ROOT / STATEMENT_RELATIVE
HISTORICAL_STATEMENT_PATH = REPO_ROOT / HISTORICAL_STATEMENT_RELATIVE
ALIGNMENT_PATHS = (
    Path("mods/training-primary-record-124-target-111e4.json"),
    Path("mods/level01-primary-record-261-target-3459c.json"),
    Path("mods/chars-flick-all-from-chars3-flickd-all.json"),
    Path("scripts/play-pristine.sh"),
    Path("reimplementation/ablpc/manifest.py"),
    Path("Vault/00-System/Environment Status.md"),
    Path("Vault/10-Environment/Wine Linux Play Baseline.md"),
    Path("reimplementation/README.md"),
)


def _copy_alignment_sources(destination: Path) -> None:
    for relative in ALIGNMENT_PATHS:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO_ROOT / relative, target)


def _load_checker_script():
    script_path = REPO_ROOT / "scripts/check-m4-compatibility.py"
    spec = importlib.util.spec_from_file_location("check_m4_compatibility", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_statement_is_canonical_and_repository_aligned() -> None:
    statement = load_compatibility_statement(STATEMENT_PATH)

    assert statement == EXPECTED_STATEMENT
    validate_repository_alignment(REPO_ROOT, statement)


def test_historical_v0_1_statement_is_byte_exact_and_repository_aligned() -> None:
    raw = HISTORICAL_STATEMENT_PATH.read_bytes()
    statement = load_compatibility_statement(HISTORICAL_STATEMENT_PATH)

    assert len(raw) == 6_177
    assert hashlib.sha256(raw).hexdigest() == (
        "c3427d44cf32619a1f9bbcab7c51e67c0846b35d9d53eab7632ff6356c0beaf0"
    )
    assert raw == (json.dumps(EXPECTED_STATEMENT_V0_1, indent=2) + "\n").encode(
        "utf-8"
    )
    assert statement == EXPECTED_STATEMENT_V0_1
    validate_repository_alignment(REPO_ROOT, statement)


def test_checker_cli_accepts_the_tracked_statement() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check-m4-compatibility.py"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "ablpc-m4-compatibility-v0.2 (5 hash anchors)" in result.stdout
    assert result.stderr == ""


def test_checker_cli_accepts_the_historical_statement_explicitly() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/check-m4-compatibility.py",
            str(HISTORICAL_STATEMENT_RELATIVE),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "ablpc-m4-compatibility-v0.1 (5 hash anchors)" in result.stdout
    assert result.stderr == ""


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda value: value.__setitem__("statement_schema_version", 2),
            "statement_schema_version",
        ),
        (
            lambda value: value.__setitem__("unexpected", True),
            "unsupported field 'unexpected'",
        ),
        (
            lambda value: value["hash_anchors"][0].__setitem__("sha256", "0" * 64),
            "hash_anchors[0].sha256",
        ),
        (
            lambda value: value["manifest_contract"]["schema_versions"].append(3),
            "schema_versions has 3 items",
        ),
        (
            lambda value: value["manifest_contract"]["formats"][0][
                "operations"
            ].append("arbitrary-byte-patch"),
            "operations has 4 items",
        ),
        (
            lambda value: value["manifest_contract"]["workflows"][3].__setitem__(
                "status", "portable"
            ),
            "workflows[3].status",
        ),
        (
            lambda value: value["tested_tool_environment"].__setitem__(
                "architecture", "aarch64"
            ),
            "tested_tool_environment.architecture",
        ),
        (
            lambda value: value["tested_wine_gamescope_scope"].__setitem__(
                "wine", "wine-12.0"
            ),
            "tested_wine_gamescope_scope.wine",
        ),
        (
            lambda value: value["manifest_contract"]["workflows"][4].__setitem__(
                "scope", "arbitrary-tree"
            ),
            "workflows[4].scope",
        ),
        (
            lambda value: value["restoration_boundary"].__setitem__(
                "path_uniqueness", "exact-host-spelling"
            ),
            "restoration_boundary.path_uniqueness",
        ),
        (
            lambda value: value["unsupported"].remove(
                "general-all-file-layout-identity-or-compatibility"
            ),
            "unsupported has 10 items",
        ),
    ],
)
def test_statement_rejects_exact_contract_drift(mutate, message: str) -> None:
    statement = copy.deepcopy(EXPECTED_STATEMENT)
    mutate(statement)

    escaped_message = message.replace("[", r"\[").replace("]", r"\]")
    with pytest.raises(CompatibilityError, match=escaped_message):
        validate_compatibility_statement(statement)


def test_loader_rejects_duplicate_keys(tmp_path: Path) -> None:
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text(
        '{"statement_schema_version":1,"statement_schema_version":1}\n',
        encoding="utf-8",
    )

    with pytest.raises(CompatibilityError, match="duplicate JSON key"):
        load_compatibility_statement(duplicate)


def test_statement_rejects_unknown_version() -> None:
    statement = copy.deepcopy(EXPECTED_STATEMENT_V0_2)
    statement["statement_id"] = "ablpc-m4-compatibility-v9.9"

    with pytest.raises(CompatibilityError, match="expected one of"):
        validate_compatibility_statement(statement)


@pytest.mark.parametrize("statement_id", [[], {}, 1], ids=("list", "object", "integer"))
def test_statement_rejects_non_string_id(statement_id) -> None:
    statement = copy.deepcopy(EXPECTED_STATEMENT_V0_2)
    statement["statement_id"] = statement_id

    with pytest.raises(CompatibilityError, match=r"\$\.statement_id has type"):
        validate_compatibility_statement(statement)


@pytest.mark.parametrize("nested", [False, True], ids=("top-level", "nested"))
def test_loader_rejects_reordered_object_fields(
    tmp_path: Path, nested: bool
) -> None:
    statement = copy.deepcopy(EXPECTED_STATEMENT_V0_2)
    reordered = statement["restoration_boundary"] if nested else statement
    first_key = next(iter(reordered))
    first_value = reordered.pop(first_key)
    reordered[first_key] = first_value
    path = tmp_path / "reordered.json"
    path.write_text(json.dumps(statement, indent=2) + "\n", encoding="utf-8")

    with pytest.raises(CompatibilityError, match="object field order"):
        load_compatibility_statement(path)


@pytest.mark.parametrize(
    ("selected_relative", "replacement_path", "expected_id"),
    [
        (
            STATEMENT_RELATIVE,
            HISTORICAL_STATEMENT_PATH,
            "ablpc-m4-compatibility-v0.2",
        ),
        (
            HISTORICAL_STATEMENT_RELATIVE,
            STATEMENT_PATH,
            "ablpc-m4-compatibility-v0.1",
        ),
    ],
    ids=("active-downgrade", "historical-upgrade"),
)
def test_selected_statement_path_rejects_cross_version_replacement(
    tmp_path: Path,
    selected_relative: Path,
    replacement_path: Path,
    expected_id: str,
) -> None:
    selected = tmp_path / selected_relative
    selected.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(replacement_path, selected)

    with pytest.raises(CompatibilityError, match=f"requires {expected_id!r}"):
        check_compatibility_statement(selected, tmp_path)


@pytest.mark.parametrize(
    ("selected_relative", "target_relative"),
    [
        (STATEMENT_RELATIVE, HISTORICAL_STATEMENT_RELATIVE),
        (HISTORICAL_STATEMENT_RELATIVE, STATEMENT_RELATIVE),
    ],
    ids=("active-to-historical", "historical-to-active"),
)
def test_selected_statement_path_rejects_link_before_content_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    selected_relative: Path,
    target_relative: Path,
) -> None:
    selected = tmp_path / selected_relative
    target = tmp_path / target_relative
    selected.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REPO_ROOT / target_relative, target)
    selected.symlink_to(target.name)
    original_read_bytes = Path.read_bytes

    def reject_selected_read(candidate: Path) -> bytes:
        assert candidate != selected, "selected link content was read"
        return original_read_bytes(candidate)

    monkeypatch.setattr(Path, "read_bytes", reject_selected_read)

    with pytest.raises(CompatibilityError, match="regular non-link file"):
        check_compatibility_statement(selected, tmp_path)

    checker = _load_checker_script()
    monkeypatch.setattr(checker, "REPO_ROOT", tmp_path)
    monkeypatch.chdir(tmp_path)
    arguments = [] if selected_relative == STATEMENT_RELATIVE else [str(selected_relative)]
    status = checker.main(arguments)
    output = capsys.readouterr()

    assert status == 2
    assert output.out == ""
    assert "regular non-link file" in output.err
    assert "Traceback" not in output.err


@pytest.mark.parametrize(
    "source_path", [STATEMENT_PATH, HISTORICAL_STATEMENT_PATH], ids=("v0.2", "v0.1")
)
def test_unselected_exact_statement_link_retains_existing_behavior(
    tmp_path: Path, source_path: Path
) -> None:
    unselected = tmp_path / "unselected.json"
    unselected.symlink_to(source_path)

    statement = check_compatibility_statement(unselected, REPO_ROOT)

    assert statement["statement_id"] == json.loads(
        source_path.read_text(encoding="utf-8")
    )["statement_id"]


@pytest.mark.parametrize(
    "malformed_id", [[], {}], ids=("list-id", "object-id")
)
def test_checker_cli_reports_typed_id_without_traceback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    malformed_id,
) -> None:
    statement = copy.deepcopy(EXPECTED_STATEMENT_V0_2)
    statement["statement_id"] = malformed_id
    path = tmp_path / "typed-id.json"
    path.write_text(json.dumps(statement, indent=2) + "\n", encoding="utf-8")
    checker = _load_checker_script()
    monkeypatch.setattr(checker, "REPO_ROOT", tmp_path)

    status = checker.main([str(path)])
    output = capsys.readouterr()

    assert status == 2
    assert output.out == ""
    assert "statement_id has type" in output.err
    assert "Traceback" not in output.err


@pytest.mark.parametrize(
    ("selected_relative", "replacement_path", "arguments"),
    [
        (STATEMENT_RELATIVE, HISTORICAL_STATEMENT_PATH, []),
        (
            HISTORICAL_STATEMENT_RELATIVE,
            STATEMENT_PATH,
            [str(HISTORICAL_STATEMENT_RELATIVE)],
        ),
    ],
    ids=("default-downgrade", "explicit-historical-upgrade"),
)
def test_checker_cli_rejects_selected_cross_version_without_traceback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    selected_relative: Path,
    replacement_path: Path,
    arguments: list[str],
) -> None:
    selected = tmp_path / selected_relative
    selected.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(replacement_path, selected)
    checker = _load_checker_script()
    monkeypatch.setattr(checker, "REPO_ROOT", tmp_path)
    monkeypatch.chdir(tmp_path)

    status = checker.main(arguments)
    output = capsys.readouterr()

    assert status == 2
    assert output.out == ""
    assert "selected compatibility statement path requires" in output.err
    assert "Traceback" not in output.err


def _scalar_paths(value, path=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _scalar_paths(child, path + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _scalar_paths(child, path + (index,))
    else:
        yield path


def _mutate_scalar_at_path(value, path) -> None:
    parent = value
    for component in path[:-1]:
        parent = parent[component]
    key = path[-1]
    original = parent[key]
    if isinstance(original, bool):
        parent[key] = not original
    elif isinstance(original, int):
        parent[key] = original + 1
    elif isinstance(original, str):
        parent[key] = original + "-drift"
    else:  # pragma: no cover - the exact statement has no other scalar types
        raise AssertionError(f"unsupported scalar type {type(original).__name__}")


def _mutate_scalar_type_at_path(value, path) -> None:
    parent = value
    for component in path[:-1]:
        parent = parent[component]
    key = path[-1]
    original = parent[key]
    if isinstance(original, bool):
        parent[key] = "true" if original else "false"
    elif isinstance(original, int):
        parent[key] = str(original)
    elif isinstance(original, str):
        parent[key] = [original]
    else:  # pragma: no cover - the exact statement has no other scalar types
        raise AssertionError(f"unsupported scalar type {type(original).__name__}")


def test_v0_2_rejects_drift_at_every_scalar_leaf() -> None:
    paths = list(_scalar_paths(EXPECTED_STATEMENT_V0_2))
    assert len(paths) == 151

    for path in paths:
        statement = copy.deepcopy(EXPECTED_STATEMENT_V0_2)
        _mutate_scalar_at_path(statement, path)
        with pytest.raises(CompatibilityError):
            validate_compatibility_statement(statement)


def test_v0_2_rejects_type_drift_at_every_scalar_leaf() -> None:
    paths = list(_scalar_paths(EXPECTED_STATEMENT_V0_2))
    assert len(paths) == 151

    for path in paths:
        statement = copy.deepcopy(EXPECTED_STATEMENT_V0_2)
        _mutate_scalar_type_at_path(statement, path)
        with pytest.raises(CompatibilityError):
            validate_compatibility_statement(statement)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: value.pop("restoration_boundary"),
        lambda value: value["manifest_contract"]["workflows"].reverse(),
        lambda value: value["restoration_boundary"]["required_interfaces"].reverse(),
        lambda value: value["unsupported"].append("invented-unsupported-surface"),
    ],
)
def test_v0_2_rejects_structural_drift(mutate) -> None:
    statement = copy.deepcopy(EXPECTED_STATEMENT_V0_2)
    mutate(statement)

    with pytest.raises(CompatibilityError):
        validate_compatibility_statement(statement)


def test_loader_rejects_noncanonical_encoding(tmp_path: Path) -> None:
    noncanonical = tmp_path / "noncanonical.json"
    noncanonical.write_text(json.dumps(EXPECTED_STATEMENT), encoding="utf-8")

    with pytest.raises(CompatibilityError, match="not canonical JSON"):
        load_compatibility_statement(noncanonical)


@pytest.mark.parametrize(
    ("relative", "old", "new", "message"),
    [
        (
            Path("scripts/play-pristine.sh"),
            "EXPECTED_EXE_SHA256=97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878",
            "EXPECTED_EXE_SHA256=" + "0" * 64,
            "SHA-256 drifted",
        ),
        (
            Path("mods/training-primary-record-124-target-111e4.json"),
            "494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22",
            "0" * 64,
            "SHA-256 drifted",
        ),
        (
            Path("Vault/00-System/Environment Status.md"),
            "Kernel             7.0.11-200.fc44.x86_64",
            "Kernel             7.0.12-200.fc44.x86_64",
            "Kernel declaration",
        ),
        (
            Path("reimplementation/README.md"),
            "Native software render mode is FALSE",
            "Native software render mode is TRUE",
            "Native software",
        ),
    ],
)
def test_repository_alignment_rejects_authority_drift(
    tmp_path: Path, relative: Path, old: str, new: str, message: str
) -> None:
    _copy_alignment_sources(tmp_path)
    path = tmp_path / relative
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new), encoding="utf-8")

    with pytest.raises(CompatibilityError, match=message):
        validate_repository_alignment(tmp_path, EXPECTED_STATEMENT)


@pytest.mark.parametrize(
    ("relative", "anchor", "addition", "message"),
    [
        (
            Path("scripts/play-pristine.sh"),
            "OUTPUT_WIDTH=2560\n",
            "OUTPUT_WIDTH=1\n",
            "SHA-256 drifted",
        ),
        (
            Path("scripts/play-pristine.sh"),
            "FILTER=nearest\n",
            "FILTER=linear\n",
            "SHA-256 drifted",
        ),
        (
            Path("reimplementation/ablpc/manifest.py"),
            '_RECEIPT_RELATIVE = PurePosixPath(".ablpc", "receipt.json")\n',
            '_RECEIPT_RELATIVE = PurePosixPath(".ablpc", "other.json")\n',
            "SHA-256 drifted",
        ),
        (
            Path("Vault/00-System/Environment Status.md"),
            "Kernel             7.0.11-200.fc44.x86_64\n",
            "Kernel             1.0.0-contradiction.x86_64\n",
            "Kernel declaration",
        ),
    ],
)
def test_repository_alignment_rejects_exact_m4_20_competing_declarations(
    tmp_path: Path,
    relative: Path,
    anchor: str,
    addition: str,
    message: str,
) -> None:
    _copy_alignment_sources(tmp_path)
    path = tmp_path / relative
    text = path.read_text(encoding="utf-8")
    assert text.count(anchor) == 1
    path.write_text(text.replace(anchor, anchor + addition, 1), encoding="utf-8")

    with pytest.raises(CompatibilityError, match=message):
        validate_repository_alignment(tmp_path, EXPECTED_STATEMENT)


@pytest.mark.parametrize(
    ("relative", "anchor", "addition", "message"),
    [
        (
            Path("scripts/play-pristine.sh"),
            "OUTPUT_HEIGHT=1440\n",
            "OUTPUT_HEIGHT=1\n",
            "SHA-256 drifted",
        ),
        (
            Path("scripts/play-pristine.sh"),
            'GAME_DIR="$ROOT/work/copies/BUGS_PC-full-disc/PC/BUGS"\n',
            "GAME_DIR=/tmp/outside\n",
            "SHA-256 drifted",
        ),
        (
            Path("scripts/play-pristine.sh"),
            "OUTPUT_WIDTH=2560\n",
            ': "${OUTPUT_WIDTH:=1}"\n',
            "SHA-256 drifted",
        ),
        (
            Path("scripts/play-pristine.sh"),
            "FILTER=nearest\n",
            "unset FILTER\n",
            "SHA-256 drifted",
        ),
        (
            Path("scripts/play-pristine.sh"),
            "    -w 640 -h 480\n",
            "    -w 320 -h 200\n",
            "SHA-256 drifted",
        ),
        (
            Path("scripts/play-pristine.sh"),
            '    -S fit -F "$FILTER" "${FULLSCREEN_FLAG[@]}"\n',
            '    -S stretch -F "$FILTER"\n',
            "SHA-256 drifted",
        ),
        (
            Path("scripts/play-pristine.sh"),
            '    "$ROOT/work/copies/"*) ;;\n',
            '    "$ROOT/"*) ;;\n',
            "SHA-256 drifted",
        ),
        (
            Path("reimplementation/ablpc/manifest.py"),
            "_LISTMOUNT_REVERSE = 1\n",
            "_LISTMOUNT_REVERSE = 0\n",
            "SHA-256 drifted",
        ),
        (
            Path("reimplementation/ablpc/manifest.py"),
            '        supported_formats.add("opaque-file-v0")\n',
            '        supported_formats.add("arbitrary-file-v0")\n',
            "SHA-256 drifted",
        ),
        (
            Path("Vault/00-System/Environment Status.md"),
            "Wine               wine-11.0 (Staging)\n",
            "Wine               wine-12.0\n",
            "Wine declaration",
        ),
        (
            Path("Vault/10-Environment/Wine Linux Play Baseline.md"),
            "- Wine 11.0 (Staging) with `work/wine/baseline`;\n",
            "- Wine 12.0 with `work/wine/other`;\n",
            "declaration '- Wine '",
        ),
        (
            Path("Vault/10-Environment/Wine Linux Play Baseline.md"),
            "The default output is the tested 2560×1440 display. On another display:\n",
            "The default output is the tested 1×1 display.\n",
            "declaration 'The default output is'",
        ),
        (
            Path("reimplementation/README.md"),
            "- `Native software render mode is FALSE`\n",
            "- `Native software render mode is TRUE`\n",
            "Native software",
        ),
        (
            Path("reimplementation/README.md"),
            "The tested Wine/Gamescope scope is the unchanged executable under Wine 11.0\n",
            "The tested Wine/Gamescope scope is an unsupported contradictory setup.\n",
            "tested Wine/Gamescope scope",
        ),
    ],
)
def test_repository_alignment_rejects_adjacent_authority_ambiguity(
    tmp_path: Path,
    relative: Path,
    anchor: str,
    addition: str,
    message: str,
) -> None:
    _copy_alignment_sources(tmp_path)
    path = tmp_path / relative
    text = path.read_text(encoding="utf-8")
    assert text.count(anchor) == 1
    path.write_text(text.replace(anchor, anchor + addition, 1), encoding="utf-8")

    with pytest.raises(CompatibilityError, match=message):
        validate_repository_alignment(tmp_path, EXPECTED_STATEMENT)


@pytest.mark.parametrize(
    ("relative", "expected_digest"),
    EXPECTED_MACHINE_AUTHORITY_SHA256.items(),
)
def test_machine_authority_pins_match_tracked_bytes(
    relative: Path, expected_digest: str
) -> None:
    raw = (REPO_ROOT / relative).read_bytes()

    assert hashlib.sha256(raw).hexdigest() == expected_digest


@pytest.mark.parametrize(
    ("relative", "mutate"),
    [
        (
            Path("scripts/play-pristine.sh"),
            lambda text: text + "\nOUTPUT_WIDTH[0]=1\n",
        ),
        (
            Path("scripts/play-pristine.sh"),
            lambda text: text + "\nCOMMAND+=( -S stretch -F linear )\n",
        ),
        (
            Path("scripts/play-pristine.sh"),
            lambda text: text + "\nGAME_DIR[0]=/tmp\n",
        ),
        (
            Path("reimplementation/ablpc/manifest.py"),
            lambda text: text
            + '\nglobals()["_RECEIPT_RELATIVE"] = PurePosixPath(".ablpc", "other.json")\n',
        ),
        (
            Path("reimplementation/ablpc/manifest.py"),
            lambda text: text + "\n_validate_manifest = lambda value: None\n",
        ),
        (
            Path("mods/training-primary-record-124-target-111e4.json"),
            lambda text: text.replace(
                '  "schema_version": 1,',
                '  "schema_version": 2,\n  "schema_version": 1,',
                1,
            ),
        ),
    ],
    ids=(
        "indexed-scalar",
        "command-array-append",
        "post-guard-game-directory",
        "globals-receipt-rebind",
        "validator-name-rebind",
        "duplicate-manifest-key",
    ),
)
def test_repository_alignment_rejects_m4_22_machine_authority_bypasses(
    tmp_path: Path, relative: Path, mutate
) -> None:
    _copy_alignment_sources(tmp_path)
    path = tmp_path / relative
    original = path.read_text(encoding="utf-8")
    mutated = mutate(original)
    assert mutated != original
    path.write_text(mutated, encoding="utf-8")

    with pytest.raises(CompatibilityError, match="SHA-256 drifted"):
        validate_repository_alignment(tmp_path, EXPECTED_STATEMENT)


def test_statement_contains_no_game_payload_bytes() -> None:
    raw = STATEMENT_PATH.read_bytes()

    assert raw == (json.dumps(EXPECTED_STATEMENT, indent=2) + "\n").encode("utf-8")
    assert len(raw) < 16_384


@pytest.mark.parametrize(
    "statement_relative",
    [STATEMENT_RELATIVE, HISTORICAL_STATEMENT_RELATIVE],
    ids=("active", "historical"),
)
def test_check_reads_exactly_nine_enumerated_asset_free_paths(
    monkeypatch: pytest.MonkeyPatch,
    statement_relative: Path,
) -> None:
    observed: list[Path] = []
    original_read_bytes = Path.read_bytes
    original_read_text = Path.read_text

    def record(path: Path) -> None:
        observed.append(path.resolve().relative_to(REPO_ROOT.resolve()))

    def recording_read_bytes(path: Path) -> bytes:
        record(path)
        return original_read_bytes(path)

    def recording_read_text(
        path: Path, encoding: str | None = None, errors: str | None = None
    ) -> str:
        record(path)
        return original_read_text(path, encoding=encoding, errors=errors)

    monkeypatch.setattr(Path, "read_bytes", recording_read_bytes)
    monkeypatch.setattr(Path, "read_text", recording_read_text)

    check_compatibility_statement(REPO_ROOT / statement_relative, REPO_ROOT)

    assert observed == [
        statement_relative,
        *EXPECTED_MACHINE_AUTHORITY_SHA256,
        Path("Vault/00-System/Environment Status.md"),
        Path("Vault/10-Environment/Wine Linux Play Baseline.md"),
        Path("reimplementation/README.md"),
    ]
    assert len(observed) == len(set(observed)) == 9
