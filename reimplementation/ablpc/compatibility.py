"""Strict validation for versioned asset-free M4 compatibility statements."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from typing import Any

from .manifest import ManifestError, _validate_manifest


class CompatibilityError(ValueError):
    """Raised when the versioned compatibility statement or its sources drift."""


HISTORICAL_STATEMENT_RELATIVE = Path(
    "reimplementation/compatibility/m4-v0.1.json"
)
STATEMENT_RELATIVE = Path("reimplementation/compatibility/m4-v0.2.json")

EXPECTED_MACHINE_AUTHORITY_SHA256: dict[Path, str] = {
    Path("mods/training-primary-record-124-target-111e4.json"): (
        "315320bc524986348167ca556b178ef41fe1e8ac961e482610f8f734f34b2434"
    ),
    Path("mods/level01-primary-record-261-target-3459c.json"): (
        "358998cd326f68fcf7e10593e8ec895915b558252c300464e8fe74177280198f"
    ),
    Path("mods/chars-flick-all-from-chars3-flickd-all.json"): (
        "5aaa6e9a4fa79c303ee0920e7f87e00e87bd1dfef412a32c55e36efcc947b607"
    ),
    Path("scripts/play-pristine.sh"): (
        "0965241132af6e15e9b19db9e8dc0b821ec85ff1f14f292e86037618c75f6051"
    ),
    Path("reimplementation/ablpc/manifest.py"): (
        "b3480761ac2b4791ccbf1df69f88234532f27956152045b89615dd5ec5bf6d75"
    ),
}

EXPECTED_STATEMENT_V0_1: dict[str, Any] = {
    "statement_schema_version": 1,
    "statement_id": "ablpc-m4-compatibility-v0.1",
    "toolkit_version": "0.1",
    "status_vocabulary": ["demonstrated", "fail-closed", "unsupported"],
    "hash_anchors": [
        {
            "id": "pc-executable",
            "path": "bugs.exe",
            "sha256": "97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878",
            "role": "tested-executable",
            "status": "demonstrated",
            "evidence_ids": ["EXP-20260811-001", "EXP-20260812-007"],
        },
        {
            "id": "training-level-dat",
            "path": "CD/LEVEL07/LEVEL1.DAT",
            "sha256": "494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22",
            "role": "tested-manifest-input",
            "status": "demonstrated",
            "evidence_ids": ["EXP-20260812-006", "EXP-20260812-010"],
        },
        {
            "id": "level01-level-dat",
            "path": "CD/LEVEL01/LEVEL.DAT",
            "sha256": "786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53",
            "role": "tested-manifest-input",
            "status": "demonstrated",
            "evidence_ids": ["EXP-20260812-006", "EXP-20260812-013"],
        },
        {
            "id": "flick-all-destination",
            "path": "CD/CHARS/FLICK.ALL",
            "sha256": "a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6",
            "role": "tested-replacement-destination",
            "status": "demonstrated",
            "evidence_ids": ["EXP-20260812-033", "EXP-20260814-060"],
        },
        {
            "id": "flickd-all-source",
            "path": "CD/CHARS3/FLICKD.ALL",
            "sha256": "6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4",
            "role": "tested-replacement-source",
            "status": "demonstrated",
            "evidence_ids": ["EXP-20260812-033", "EXP-20260814-060"],
        },
    ],
    "manifest_contract": {
        "schema_versions": [1, 2],
        "formats": [
            {
                "name": "pc-level-dat-prefix-v0",
                "schema_versions": [1, 2],
                "operations": [
                    "set-scene-record-position",
                    "set-scene-record-field-0c",
                    "set-scene-record-payload-target-offset",
                ],
                "status": "demonstrated",
            },
            {
                "name": "opaque-file-v0",
                "schema_versions": [2],
                "operations": ["replace-whole-file"],
                "status": "demonstrated",
            },
        ],
        "workflows": [
            {
                "id": "apply",
                "scope": "dedicated-sparse-overlay",
                "status": "demonstrated",
            },
            {
                "id": "stage",
                "scope": "new-derived-full-tree",
                "status": "demonstrated",
            },
            {
                "id": "compose",
                "scope": "exactly-two-existing-schema-manifests",
                "status": "demonstrated",
            },
            {
                "id": "remove",
                "scope": "receipt-validated-dedicated-sparse-overlay-on-declared-linux-environment",
                "status": "demonstrated",
            },
        ],
        "failure_policy": "fail-closed",
        "receipt_path": ".ablpc/receipt.json",
        "tracked_recipes": [
            {
                "manifest": "mods/training-primary-record-124-target-111e4.json",
                "schema_version": 1,
                "format": "pc-level-dat-prefix-v0",
                "operation": "set-scene-record-payload-target-offset",
                "destination_anchor": "training-level-dat",
            },
            {
                "manifest": "mods/level01-primary-record-261-target-3459c.json",
                "schema_version": 1,
                "format": "pc-level-dat-prefix-v0",
                "operation": "set-scene-record-payload-target-offset",
                "destination_anchor": "level01-level-dat",
            },
            {
                "manifest": "mods/chars-flick-all-from-chars3-flickd-all.json",
                "schema_version": 2,
                "format": "opaque-file-v0",
                "operation": "replace-whole-file",
                "destination_anchor": "flick-all-destination",
                "replacement_anchor": "flickd-all-source",
            },
        ],
    },
    "tested_tool_environment": {
        "status": "demonstrated",
        "distribution": "Fedora Linux 44 (Workstation Edition)",
        "kernel": "7.0.11-200.fc44.x86_64",
        "architecture": "x86_64",
        "python": "3.14.6",
        "evidence_ids": ["EXP-20260814-077"],
    },
    "removal_boundary": {
        "status": "demonstrated",
        "platform_scope": "current-x86_64-linux-only",
        "required_interfaces": [
            "/proc/self/mountinfo",
            "listmount(2)-LISTMOUNT_REVERSE",
            "statmount(2)-STATMOUNT_SB_BASIC|STATMOUNT_MNT_BASIC",
        ],
        "on_unavailable_or_inconsistent_topology": "fail-closed",
        "supported_overlay_kind": "ordinary-dedicated-sparse-apply-overlay",
        "non_transactional_after_preflight": True,
        "evidence_ids": ["EXP-20260814-068", "EXP-20260814-077"],
    },
    "tested_wine_gamescope_scope": {
        "status": "demonstrated",
        "launcher": "scripts/play-pristine.sh",
        "executable_anchor": "pc-executable",
        "wine": "wine-11.0 (Staging)",
        "gamescope": "gamescope-3.16.25-1.fc44.x86_64",
        "source_policy": "derived-work-copy-below-work/copies",
        "game_working_directory": "R:\\PC\\BUGS",
        "gamescope_game_surface": "640x480",
        "default_output": "2560x1440",
        "scaler": "fit",
        "default_filter": "nearest",
        "renderer_selection": "manual-down-then-confirm-hardware-acceleration",
        "required_log_markers": [
            "Native software render mode is FALSE",
            "RenderMode set to Direct3d render mode",
            "Screen mode 640x480x16 selected",
            "Starting Direct3D renderer",
        ],
        "rejected_log_marker": "INITSOFTRENDER",
        "evidence_ids": ["EXP-20260812-007", "EXP-20260812-029"],
    },
    "unsupported": [
        "unlisted-executable-or-game-input-hashes-as-demonstrated-anchors",
        "untested-windows-wine-kernel-architecture-or-filesystem-configurations",
        "general-all-file-layout-identity-or-compatibility",
        "n-way-manifest-composition-or-cross-input-dependency-resolution",
        "staged-tree-or-source-removal-and-restoration",
        "rollback-backup-trash-package-or-general-transaction-semantics",
        "general-mod-dry-run-launch-or-runtime-automation",
    ],
}

EXPECTED_STATEMENT_V0_2: dict[str, Any] = copy.deepcopy(EXPECTED_STATEMENT_V0_1)
EXPECTED_STATEMENT_V0_2["statement_id"] = "ablpc-m4-compatibility-v0.2"
EXPECTED_STATEMENT_V0_2["toolkit_version"] = "0.2"
EXPECTED_STATEMENT_V0_2["manifest_contract"]["workflows"].append(
    {
        "id": "restore",
        "scope": (
            "manifest-and-source-authenticated-complete-staged-tree-"
            "on-declared-linux-environment"
        ),
        "status": "demonstrated",
    }
)
_tested_wine_gamescope_scope = EXPECTED_STATEMENT_V0_2.pop(
    "tested_wine_gamescope_scope"
)
EXPECTED_STATEMENT_V0_2.pop("unsupported")
EXPECTED_STATEMENT_V0_2["restoration_boundary"] = {
    "status": "demonstrated",
    "platform_scope": "current-x86_64-linux-only",
    "authority": "existing-schema-manifest-plus-exact-source-root",
    "supported_tree_kind": "complete-stage-produced-derived-game-tree",
    "required_tree_entries": "directories-and-regular-single-link-files-only",
    "source_reserved_path": ".ablpc-must-be-absent",
    "game_tree_equivalence": (
        "exact-path-type-and-content-except-recomputed-outputs-and-receipt"
    ),
    "path_uniqueness": "relative-posix-path-casefold-unique",
    "required_interfaces": [
        "/proc/self/mountinfo",
        "listmount(2)-LISTMOUNT_REVERSE",
        "statmount(2)-STATMOUNT_SB_BASIC|STATMOUNT_MNT_BASIC",
    ],
    "on_unavailable_or_inconsistent_topology": "fail-closed",
    "recorded_outputs": "exact-recomputed-output-hashes",
    "receipt": "exact-ordinary-.ablpc/receipt.json-bytes",
    "success": (
        "restore-recorded-destinations-from-exact-source-and-remove-"
        "receipt-metadata"
    ),
    "non_transactional_after_preflight": True,
    "evidence_ids": ["EXP-20260814-094", "EXP-20260814-097"],
}
EXPECTED_STATEMENT_V0_2["tested_wine_gamescope_scope"] = (
    _tested_wine_gamescope_scope
)
EXPECTED_STATEMENT_V0_2["unsupported"] = [
    "unlisted-executable-or-game-input-hashes-as-demonstrated-anchors",
    "untested-windows-wine-kernel-architecture-or-filesystem-configurations",
    "general-all-file-layout-identity-or-compatibility",
    "n-way-manifest-composition-or-cross-input-dependency-resolution",
    "whole-staged-tree-or-source-deletion",
    "external-receipt-full-tree-restoration",
    "rollback-backup-trash-package-or-general-transaction-semantics",
    "restoration-provenance-or-posix-metadata-equality",
    "general-windows-path-policy-beyond-project-casefold-uniqueness",
    "general-mod-dry-run-launch-or-runtime-automation",
    "post-preflight-concurrency-guarantees",
]

EXPECTED_STATEMENTS_BY_ID: dict[str, dict[str, Any]] = {
    EXPECTED_STATEMENT_V0_1["statement_id"]: EXPECTED_STATEMENT_V0_1,
    EXPECTED_STATEMENT_V0_2["statement_id"]: EXPECTED_STATEMENT_V0_2,
}
EXPECTED_STATEMENT_ID_BY_RELATIVE_PATH: dict[Path, str] = {
    HISTORICAL_STATEMENT_RELATIVE: EXPECTED_STATEMENT_V0_1["statement_id"],
    STATEMENT_RELATIVE: EXPECTED_STATEMENT_V0_2["statement_id"],
}
EXPECTED_STATEMENT = EXPECTED_STATEMENT_V0_2


def _reject_constant(value: str) -> None:
    raise CompatibilityError(f"non-standard JSON constant {value!r} is not allowed")


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CompatibilityError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _first_difference(expected: Any, actual: Any, path: str = "$") -> str | None:
    if type(expected) is not type(actual):
        return f"{path} has type {type(actual).__name__}; expected {type(expected).__name__}"
    if isinstance(expected, dict):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        if missing:
            return f"{path} is missing field {missing[0]!r}"
        if extra:
            return f"{path} has unsupported field {extra[0]!r}"
        if list(actual) != list(expected):
            return (
                f"{path} object field order is {list(actual)!r}; "
                f"expected {list(expected)!r}"
            )
        for key in expected:
            difference = _first_difference(expected[key], actual[key], f"{path}.{key}")
            if difference:
                return difference
        return None
    if isinstance(expected, list):
        if len(expected) != len(actual):
            return f"{path} has {len(actual)} items; expected {len(expected)}"
        for index, (expected_item, actual_item) in enumerate(zip(expected, actual)):
            difference = _first_difference(expected_item, actual_item, f"{path}[{index}]")
            if difference:
                return difference
        return None
    if expected != actual:
        return f"{path} is {actual!r}; expected {expected!r}"
    return None


def validate_compatibility_statement(statement: Any) -> dict[str, Any]:
    """Require one exact, immutable supported M4 statement contract."""

    if not isinstance(statement, dict):
        raise CompatibilityError(
            f"$ has type {type(statement).__name__}; expected dict"
        )
    statement_id = statement.get("statement_id")
    if not isinstance(statement_id, str):
        raise CompatibilityError(
            f"$.statement_id has type {type(statement_id).__name__}; expected str"
        )
    expected = EXPECTED_STATEMENTS_BY_ID.get(statement_id)
    if expected is None:
        raise CompatibilityError(
            f"$.statement_id is {statement_id!r}; expected one of "
            f"{sorted(EXPECTED_STATEMENTS_BY_ID)!r}"
        )
    difference = _first_difference(expected, statement)
    if difference:
        raise CompatibilityError(difference)
    return statement


def load_compatibility_statement(
    path: Path, *, expected_statement_id: str | None = None
) -> dict[str, Any]:
    """Load strict canonical JSON and validate an exact versioned contract."""

    try:
        raw = path.read_bytes()
    except OSError as error:
        raise CompatibilityError(f"cannot read compatibility statement: {error}") from error
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CompatibilityError("compatibility statement is not UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except CompatibilityError:
        raise
    except json.JSONDecodeError as error:
        raise CompatibilityError(f"invalid compatibility JSON: {error.msg}") from error
    statement = validate_compatibility_statement(value)
    if (
        expected_statement_id is not None
        and statement["statement_id"] != expected_statement_id
    ):
        raise CompatibilityError(
            f"selected compatibility statement path requires {expected_statement_id!r}; "
            f"found {statement['statement_id']!r}"
        )
    canonical = (json.dumps(statement, indent=2) + "\n").encode("utf-8")
    if raw != canonical:
        raise CompatibilityError("compatibility statement is not canonical JSON")
    return statement


def _anchor_map(statement: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {entry["id"]: entry for entry in statement["hash_anchors"]}


def _require_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise CompatibilityError(f"cannot read evidence source {path}: {error}") from error


def _decode_evidence_text(raw: bytes, path: Path) -> str:
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CompatibilityError(f"evidence source {path} is not UTF-8") from error


def _read_machine_authorities(repo_root: Path) -> dict[Path, bytes]:
    authorities: dict[Path, bytes] = {}
    for relative, expected_digest in EXPECTED_MACHINE_AUTHORITY_SHA256.items():
        raw = _require_bytes(repo_root / relative)
        actual_digest = hashlib.sha256(raw).hexdigest()
        if actual_digest != expected_digest:
            raise CompatibilityError(
                f"machine authority {relative} SHA-256 drifted: {actual_digest}"
            )
        authorities[relative] = raw
    return authorities


def _load_tracked_manifest(raw: bytes, relative: Path) -> dict[str, Any]:
    text = _decode_evidence_text(raw, relative)
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise CompatibilityError(
            f"tracked manifest {relative} is invalid: {error}"
        ) from error
    try:
        _validate_manifest(value)
    except ManifestError as error:
        raise CompatibilityError(
            f"tracked manifest {relative} is invalid: {error}"
        ) from error
    return value


def _validate_recipe_alignment(
    statement: dict[str, Any], authorities: dict[Path, bytes]
) -> None:
    anchors = _anchor_map(statement)
    for recipe in statement["manifest_contract"]["tracked_recipes"]:
        relative = Path(recipe["manifest"])
        manifest = _load_tracked_manifest(authorities[relative], relative)
        if manifest["schema_version"] != recipe["schema_version"]:
            raise CompatibilityError(f"{recipe['manifest']} schema version drifted")
        if len(manifest["files"]) != 1:
            raise CompatibilityError(f"{recipe['manifest']} must contain exactly one file")
        file_entry = manifest["files"][0]
        destination = anchors[recipe["destination_anchor"]]
        if file_entry["path"] != destination["path"]:
            raise CompatibilityError(f"{recipe['manifest']} destination path drifted")
        if file_entry["sha256"].lower() != destination["sha256"]:
            raise CompatibilityError(f"{recipe['manifest']} destination hash drifted")
        if file_entry["format"] != recipe["format"]:
            raise CompatibilityError(f"{recipe['manifest']} format drifted")
        if len(file_entry["edits"]) != 1:
            raise CompatibilityError(f"{recipe['manifest']} must contain exactly one edit")
        edit = file_entry["edits"][0]
        if edit["operation"] != recipe["operation"]:
            raise CompatibilityError(f"{recipe['manifest']} operation drifted")
        if "replacement_anchor" in recipe:
            replacement = anchors[recipe["replacement_anchor"]]
            if edit["source_path"] != replacement["path"]:
                raise CompatibilityError(f"{recipe['manifest']} replacement path drifted")
            if edit["source_sha256"].lower() != replacement["sha256"]:
                raise CompatibilityError(f"{recipe['manifest']} replacement hash drifted")


def _require_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise CompatibilityError(f"cannot read evidence source {path}: {error}") from error


def _require_unique_fragment(text: str, fragment: str, label: str) -> None:
    count = text.count(fragment)
    if count != 1:
        raise CompatibilityError(
            f"{label} must contain exactly one {fragment!r}; found {count}"
        )


def _shell_assignment_values(text: str, name: str) -> list[str]:
    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(name)}=([^;\n]+)")
    return [match.group(1).strip() for match in pattern.finditer(text)]


def _require_shell_assignments(
    text: str, expected: dict[str, list[str]], label: str
) -> None:
    for name, expected_values in expected.items():
        actual_values = _shell_assignment_values(text, name)
        if actual_values != expected_values:
            raise CompatibilityError(
                f"{label} {name} assignments are ambiguous or changed: "
                f"{actual_values!r}"
            )
        indirect_patterns = (
            rf"\$\{{{re.escape(name)}(?::?=)",
            rf"(?:^|[;\s])unset(?:\s+--)?\s+{re.escape(name)}(?:\s|;|$)",
            rf"\bprintf\s+-v\s+{re.escape(name)}(?:\s|$)",
            rf"\bread(?:\s+-[^\s]+\s+)*{re.escape(name)}(?:\s|$)",
        )
        if any(re.search(pattern, text, re.M) for pattern in indirect_patterns):
            raise CompatibilityError(f"{label} changes {name} indirectly")


def _require_launcher_structure(
    text: str, game_surface: str, scaler: str, label: str
) -> None:
    command_blocks = re.findall(r"^COMMAND=\(\n(.*?)^\)$", text, re.M | re.S)
    if len(command_blocks) != 1:
        raise CompatibilityError(f"{label} COMMAND declaration is ambiguous")
    command = command_blocks[0]
    width, height = game_surface.split("x", 1)
    surfaces = re.findall(r"(?<!\S)-w\s+(\S+)\s+-h\s+(\S+)", command)
    if surfaces != [(width, height)]:
        raise CompatibilityError(f"{label} game-surface declaration changed")
    scalers = re.findall(r"(?<!\S)-S\s+(\S+)\s+-F\s+(\S+)", command)
    if scalers != [(scaler, '"$FILTER"')]:
        raise CompatibilityError(f"{label} scaler/filter declaration changed")

    guard = """case "$GAME_DIR/" in
    "$ROOT/work/copies/"*) ;;
    *) echo "Refusing game directory outside work/copies/: $GAME_DIR" >&2; exit 2 ;;
esac"""
    _require_unique_fragment(text, guard, label)
    renderer_guidance = """echo "At the renderer selector, use only the experiment's preregistered sequence;" >&2
echo "do not infer selection from pixels or an assumed default." >&2"""
    _require_unique_fragment(text, renderer_guidance, label)


def _parse_python_source(text: str, label: str) -> ast.Module:
    try:
        return ast.parse(text)
    except SyntaxError as error:
        raise CompatibilityError(f"{label} is not valid Python: {error.msg}") from error


def _target_names(target: ast.expr) -> set[str]:
    if isinstance(target, ast.Name):
        return {target.id}
    if isinstance(target, (ast.Tuple, ast.List)):
        return set().union(*(_target_names(item) for item in target.elts))
    return set()


def _assignment_values(tree: ast.AST, name: str) -> list[ast.expr | None]:
    values: list[ast.expr | None] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            name in _target_names(target) for target in node.targets
        ):
            values.append(node.value)
        elif isinstance(node, ast.AnnAssign) and name in _target_names(node.target):
            values.append(node.value)
        elif isinstance(node, (ast.AugAssign, ast.NamedExpr)) and name in _target_names(
            node.target
        ):
            values.append(None)
    return values


def _require_python_assignment(
    tree: ast.AST, name: str, expression: str, label: str
) -> None:
    values = _assignment_values(tree, name)
    expected = ast.parse(expression, mode="eval").body
    if len(values) != 1 or values[0] is None or ast.dump(values[0]) != ast.dump(expected):
        raise CompatibilityError(
            f"{label} {name} declaration is ambiguous or changed"
        )


def _require_function(tree: ast.AST, name: str, label: str) -> ast.FunctionDef:
    matches = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    if len(matches) != 1:
        raise CompatibilityError(
            f"{label} must define exactly one {name}; found {len(matches)}"
        )
    return matches[0]


def _compare_constant(
    node: ast.AST, subject: ast.AST, operator: type[ast.cmpop]
) -> str | None:
    if not isinstance(node, ast.Compare) or len(node.ops) != 1:
        return None
    if not isinstance(node.ops[0], operator) or ast.dump(node.left) != ast.dump(subject):
        return None
    if len(node.comparators) != 1 or not isinstance(
        node.comparators[0], ast.Constant
    ):
        return None
    value = node.comparators[0].value
    return value if isinstance(value, str) else None


def _require_manifest_contract(tree: ast.Module) -> None:
    label = "manifest implementation"
    for name, expression in (
        ("_RECEIPT_RELATIVE", 'PurePosixPath(".ablpc", "receipt.json")'),
        ("_LISTMOUNT_REVERSE", "1"),
        ("_STATMOUNT_SB_BASIC", "1"),
        ("_STATMOUNT_MNT_BASIC", "2"),
        (
            "_STATMOUNT_ORDER_FIELDS",
            "_STATMOUNT_SB_BASIC | _STATMOUNT_MNT_BASIC",
        ),
        ("mountinfo_path", 'Path("/proc/self/mountinfo")'),
    ):
        _require_python_assignment(tree, name, expression, label)

    manifest_validator = _require_function(tree, "_validate_manifest", label)
    _require_python_assignment(
        manifest_validator,
        "schema_version",
        'value.get("schema_version")',
        label,
    )
    schema_tests = [
        node
        for node in ast.walk(manifest_validator)
        if isinstance(node, ast.Compare)
        and len(node.ops) == 1
        and isinstance(node.ops[0], ast.NotIn)
        and isinstance(node.left, ast.Name)
        and node.left.id == "schema_version"
        and len(node.comparators) == 1
        and isinstance(node.comparators[0], (ast.Tuple, ast.List))
    ]
    all_schema_comparisons = [
        node
        for node in ast.walk(manifest_validator)
        if isinstance(node, ast.Compare)
        and isinstance(node.left, ast.Name)
        and node.left.id == "schema_version"
    ]
    schema_values = (
        [item.value for item in schema_tests[0].comparators[0].elts]
        if len(schema_tests) == 1
        and all(
            isinstance(item, ast.Constant)
            for item in schema_tests[0].comparators[0].elts
        )
        else None
    )
    if schema_values != [1, 2] or all_schema_comparisons != schema_tests:
        raise CompatibilityError(f"{label} schema declaration is ambiguous or changed")

    file_validator = _require_function(tree, "_validate_file_entry", label)
    _require_python_assignment(
        file_validator,
        "supported_formats",
        '{"pc-level-dat-prefix-v0"}',
        label,
    )
    format_mutations = [
        (node.func.attr, [ast.dump(argument) for argument in node.args])
        for node in ast.walk(file_validator)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "supported_formats"
    ]
    expected_format_addition = ast.dump(ast.Constant(value="opaque-file-v0"))
    if format_mutations != [("add", [expected_format_addition])]:
        raise CompatibilityError(f"{label} format declaration is ambiguous or changed")
    format_name_tests = [
        node
        for node in ast.walk(file_validator)
        if isinstance(node, ast.Compare)
        and isinstance(node.left, ast.Name)
        and node.left.id == "format_name"
    ]
    format_subject = ast.Name(id="format_name")
    format_value_tests = [
        node
        for node in format_name_tests
        if _compare_constant(node, format_subject, ast.Eq) == "opaque-file-v0"
    ]
    format_membership_tests = [
        node
        for node in format_name_tests
        if len(node.ops) == 1
        and isinstance(node.ops[0], ast.NotIn)
        and len(node.comparators) == 1
        and isinstance(node.comparators[0], ast.Name)
        and node.comparators[0].id == "supported_formats"
    ]
    if (
        len(format_name_tests) != 2
        or len(format_value_tests) != 1
        or len(format_membership_tests) != 1
    ):
        raise CompatibilityError(f"{label} format checks are ambiguous or changed")

    edit_validator = _require_function(tree, "_validate_level_dat_edit", label)
    _require_python_assignment(edit_validator, "operation", 'edit.get("operation")', label)
    first_operation_test = next(
        (
            node
            for node in edit_validator.body
            if isinstance(node, ast.If)
            and _compare_constant(node.test, ast.Name(id="operation"), ast.Eq)
            is not None
        ),
        None,
    )
    operations: list[str] = []
    branch = first_operation_test
    while branch is not None:
        value = _compare_constant(branch.test, ast.Name(id="operation"), ast.Eq)
        if value is None:
            break
        operations.append(value)
        branch = (
            branch.orelse[0]
            if len(branch.orelse) == 1 and isinstance(branch.orelse[0], ast.If)
            else None
        )
    if operations != [
        "set-scene-record-position",
        "set-scene-record-payload-target-offset",
        "set-scene-record-field-0c",
    ]:
        raise CompatibilityError(f"{label} level operation declaration changed")

    whole_validator = _require_function(tree, "_validate_whole_file_edit", label)
    operation_subject = ast.parse('edit["operation"]', mode="eval").body
    whole_operation_tests = [
        node
        for node in ast.walk(whole_validator)
        if isinstance(node, ast.Compare)
        and ast.dump(node.left) == ast.dump(operation_subject)
    ]
    if len(whole_operation_tests) != 1 or _compare_constant(
        whole_operation_tests[0], operation_subject, ast.NotEq
    ) != "replace-whole-file":
        raise CompatibilityError(f"{label} whole-file operation declaration changed")


def _marked_block(text: str, begin: str, end: str, label: str) -> str:
    if text.count(begin) != 1 or text.count(end) != 1:
        raise CompatibilityError(f"{label} generated-block markers are ambiguous")
    before, remainder = text.split(begin, 1)
    block, after = remainder.split(end, 1)
    if begin in before or end in before or begin in after or end in after:
        raise CompatibilityError(f"{label} generated-block markers are out of order")
    return block


def _require_labeled_rows(
    text: str, expected: dict[str, str], label: str
) -> None:
    for key, expected_value in expected.items():
        matches = re.findall(rf"^{re.escape(key)}\s{{2,}}(.+)$", text, re.M)
        if matches != [expected_value]:
            raise CompatibilityError(
                f"{label} {key} declaration is ambiguous or changed: {matches!r}"
            )


def _markdown_section(text: str, heading: str, label: str) -> str:
    marker = f"## {heading}"
    if len(re.findall(rf"^{re.escape(marker)}$", text, re.M)) != 1:
        raise CompatibilityError(f"{label} section {heading!r} is ambiguous")
    start = text.index(marker) + len(marker)
    next_heading = re.search(r"^## ", text[start:], re.M)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end]


def _require_prefixed_lines(
    text: str, expected: dict[str, str], label: str
) -> None:
    lines = text.splitlines()
    for prefix, expected_line in expected.items():
        matches = [line for line in lines if line.startswith(prefix)]
        if matches != [expected_line]:
            raise CompatibilityError(
                f"{label} declaration {prefix!r} is ambiguous or changed"
            )


def validate_repository_alignment(repo_root: Path, statement: dict[str, Any]) -> None:
    """Cross-check versioned metadata against tracked asset-free authorities."""

    validate_compatibility_statement(statement)
    machine_authorities = _read_machine_authorities(repo_root)
    _validate_recipe_alignment(statement, machine_authorities)
    scope = statement["tested_wine_gamescope_scope"]
    environment = statement["tested_tool_environment"]
    executable = _anchor_map(statement)[scope["executable_anchor"]]
    default_width, default_height = scope["default_output"].split("x", 1)

    launcher_relative = Path(scope["launcher"])
    launcher = _decode_evidence_text(
        machine_authorities[launcher_relative], launcher_relative
    )
    _require_shell_assignments(
        launcher,
        {
            "EXPECTED_EXE_SHA256": [executable["sha256"]],
            "GAME_DIR": [
                '"$ROOT/work/copies/BUGS_PC-full-disc/PC/BUGS"',
                "$2",
                '$(readlink -f -- "$GAME_DIR")',
            ],
            "OUTPUT_WIDTH": [default_width, "${2%%x*}", "1280"],
            "OUTPUT_HEIGHT": [default_height, "${2#*x}", "960"],
            "FILTER": [scope["default_filter"], "$2"],
        },
        scope["launcher"],
    )
    _require_launcher_structure(
        launcher,
        scope["gamescope_game_surface"],
        scope["scaler"],
        scope["launcher"],
    )

    manifest_relative = Path("reimplementation/ablpc/manifest.py")
    manifest_source = _decode_evidence_text(
        machine_authorities[manifest_relative], manifest_relative
    )
    _require_manifest_contract(
        _parse_python_source(manifest_source, "manifest implementation")
    )

    environment_text = _require_text(repo_root / "Vault/00-System/Environment Status.md")
    doctor_block = _marked_block(
        environment_text,
        "<!-- BEGIN GENERATED: doctor -->",
        "<!-- END GENERATED: doctor -->",
        "Environment Status",
    )
    _require_labeled_rows(
        doctor_block,
        {
            "Fedora": environment["distribution"],
            "Kernel": environment["kernel"],
            "Architecture": environment["architecture"],
            "Python": f"Python {environment['python']}",
            "Wine": scope["wine"],
            "Gamescope": scope["gamescope"],
        },
        "Environment Status doctor block",
    )

    wine_baseline = _require_text(repo_root / "Vault/10-Environment/Wine Linux Play Baseline.md")
    supported = _markdown_section(
        wine_baseline, "Supported configuration", "Wine Linux Play Baseline"
    )
    _require_prefixed_lines(
        supported,
        {
            "- unchanged `bugs.exe`": (
                f"- unchanged `bugs.exe`, SHA-256 `{executable['sha256']}`;"
            ),
            "- derived content under": (
                "- derived content under `work/copies/`, never `originals/`;"
            ),
            "- Wine ": (
                f"- {scope['wine'].replace('wine-', 'Wine ')} with `work/wine/baseline`;"
            ),
            "- the game working directory": (
                f"- the game working directory shaped as `{scope['game_working_directory']}` through the prefix mapping established by `EXP-20260811-004`;"
            ),
            "- **hardware acceleration**": (
                "- **hardware acceleration**, the second option in the opening renderer selector;"
            ),
            "- Gamescope nested at": (
                f"- Gamescope nested at {scope['gamescope_game_surface'].replace('x', '×')} with aspect-preserving `{scope['scaler']}` scaling to the host output."
            ),
            "The default output is": (
                f"The default output is the tested {scope['default_output'].replace('x', '×')} display. On another display:"
            ),
        },
        "Wine Linux Play Baseline supported configuration",
    )
    renderer = _markdown_section(
        wine_baseline, "Renderer selection matters", "Wine Linux Play Baseline"
    )
    normalized_renderer = " ".join(renderer.split())
    _require_unique_fragment(
        normalized_renderer,
        "Do not assume the retail chooser's current/default selection and do not infer it from chooser pixels.",
        "Wine Linux Play Baseline renderer selection",
    )
    _require_unique_fragment(
        normalized_renderer,
        "Every renderer-facing retail experiment must pre-register its exact selector sequence and classify the result only from the complete log.",
        "Wine Linux Play Baseline renderer selection",
    )
    _require_unique_fragment(
        normalized_renderer,
        "The historical R2c retail branch used fresh RC0 with no directional input before Return.",
        "Wine Linux Play Baseline renderer selection",
    )
    _require_prefixed_lines(
        renderer,
        {
            "- require `Native software": "- require `Native software render mode is FALSE`;",
            "- require `RenderMode": "- require `RenderMode set to Direct3d render mode`;",
            "- require `INFO Screen": "- require `INFO Screen mode 640x480x16 selected.`;",
            "- require `INIT :": "- require `INIT : Starting Direct3D renderer.`;",
            "- reject the run": "- reject the run if it enters `INITSOFTRENDER`.",
        },
        "Wine Linux Play Baseline renderer markers",
    )
    scaling = _markdown_section(
        wine_baseline, "Scaling and filtering", "Wine Linux Play Baseline"
    )
    _require_prefixed_lines(
        scaling,
        {
            "The wrapper defaults to": (
                f"The wrapper defaults to `{scope['default_filter']}`, which is crisp:"
            )
        },
        "Wine Linux Play Baseline scaling",
    )

    readme = _require_text(repo_root / "reimplementation/README.md")
    compatibility_section = _markdown_section(
        readme, "Exact M4 compatibility statements", "reimplementation README"
    )
    for fragment in (
        HISTORICAL_STATEMENT_RELATIVE.as_posix(),
        STATEMENT_RELATIVE.as_posix(),
        "scripts/check-m4-compatibility.py",
    ):
        _require_unique_fragment(
            compatibility_section, fragment, "reimplementation README compatibility section"
        )
    normalized_compatibility = " ".join(compatibility_section.split())
    for prefix in (
        "The tested Wine/Gamescope scope is",
        "Hardware selection remains manual:",
    ):
        _require_unique_fragment(
            normalized_compatibility,
            prefix,
            "reimplementation README compatibility section",
        )
    for fragment in (
        "Wine 11.0 (Staging), Gamescope 3.16.25-1.fc44.x86_64, a 640x480 game surface, `fit` scaling, and the default `nearest` filter.",
        "press Down, then confirm.",
    ):
        _require_unique_fragment(
            normalized_compatibility,
            fragment,
            "reimplementation README compatibility section",
        )
    _require_prefixed_lines(
        compatibility_section,
        {
            "- `Native software": "- `Native software render mode is FALSE`",
            "- `RenderMode": "- `RenderMode set to Direct3d render mode`",
            "- `Screen mode": "- `Screen mode 640x480x16 selected`",
            "- `Starting Direct3D": "- `Starting Direct3D renderer`",
            "Reject a run containing": (
                "Reject a run containing `INITSOFTRENDER`. This scope does not establish other"
            ),
        },
        "reimplementation README compatibility markers",
    )
    if statement["toolkit_version"] == "0.2":
        normalized_compatibility = " ".join(compatibility_section.split())
        for fragment in (
            "v0.1 remains immutable historical evidence.",
            "v0.2 adds only the independently accepted manifest/source-authenticated complete-tree restoration boundary on current x86_64 Linux.",
            "External-receipt full-tree restoration, whole staged-tree or source deletion, provenance, POSIX metadata equality, backup, rollback, packaging, transactions, general launch/runtime automation, and post-preflight concurrency guarantees remain unsupported.",
        ):
            _require_unique_fragment(
                normalized_compatibility,
                fragment,
                "reimplementation README v0.2 restoration boundary",
            )


def check_compatibility_statement(path: Path, repo_root: Path) -> dict[str, Any]:
    selected_path = Path(os.path.abspath(path))
    lexical_repo_root = Path(os.path.abspath(repo_root))
    expected_statement_id = next(
        (
            statement_id
            for relative, statement_id in EXPECTED_STATEMENT_ID_BY_RELATIVE_PATH.items()
            if selected_path == Path(os.path.abspath(lexical_repo_root / relative))
        ),
        None,
    )
    if expected_statement_id is not None:
        try:
            selected_metadata = path.lstat()
        except OSError as error:
            raise CompatibilityError(
                f"cannot inspect selected compatibility statement: {error}"
            ) from error
        if not stat.S_ISREG(selected_metadata.st_mode):
            raise CompatibilityError(
                "selected compatibility statement must be a regular non-link file"
            )
    statement = load_compatibility_statement(
        path, expected_statement_id=expected_statement_id
    )
    validate_repository_alignment(repo_root, statement)
    return statement
