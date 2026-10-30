"""Repository hygiene gates.

These are cheap structural invariants that nothing else enforces:

* ``AGENTS.md`` and ``CLAUDE.md`` must stay byte-identical, because an agent
  that reads only one of them would otherwise follow a diverged policy;
* the note templates, the ``scripts/new-*.py`` generators, and the frontmatter
  keys ``scripts/vault-lint.py`` requires must agree;
* every executable Python script must at least parse.
"""

from __future__ import annotations

import ast
import importlib.util
import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TEMPLATES = ROOT / "Vault" / "99-Templates"
FRONTMATTER_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):", re.MULTILINE)
GENERATOR_FRONTMATTER = re.compile(r'"""---\n(.*?)\n---\n', re.DOTALL)
TEMPLATE_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def load_vault_lint():
    """Import scripts/vault-lint.py by path (its name is not importable)."""

    path = SCRIPTS / "vault-lint.py"
    spec = importlib.util.spec_from_file_location("vault_lint_under_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frontmatter_keys(block: str) -> set[str]:
    return set(FRONTMATTER_KEY.findall(block))


def frontmatter_type(block: str) -> str | None:
    match = re.search(r"^type:\s*(\S+)\s*$", block, re.MULTILINE)
    return match.group(1) if match else None


def test_agents_and_claude_instructions_are_identical() -> None:
    agents = ROOT / "AGENTS.md"
    claude = ROOT / "CLAUDE.md"
    assert agents.is_file() and claude.is_file()
    assert agents.read_bytes() == claude.read_bytes(), (
        "AGENTS.md and CLAUDE.md have diverged. Both files are read as the root "
        "instruction surface, so an agent that opens only one would follow stale "
        "policy. Decide which file is authoritative and resync with "
        "`cp AGENTS.md CLAUDE.md` (or `cp CLAUDE.md AGENTS.md`), then re-run this test."
    )


def test_templates_generators_and_lint_requirements_agree() -> None:
    if not TEMPLATES.is_dir():
        pytest.skip("Vault/99-Templates is not present")
    lint = load_vault_lint()
    required = lint.REQUIRED

    templates: dict[str, tuple[Path, set[str]]] = {}
    for path in sorted(TEMPLATES.glob("*.md")):
        block = TEMPLATE_FRONTMATTER.search(path.read_text(encoding="utf-8"))
        assert block, f"{path.relative_to(ROOT)} has no YAML frontmatter block"
        note_type = frontmatter_type(block.group(1))
        if note_type:
            templates[note_type] = (path, frontmatter_keys(block.group(1)))

    generators: dict[str, tuple[Path, set[str]]] = {}
    for path in sorted(SCRIPTS.glob("new-*.py")):
        block = GENERATOR_FRONTMATTER.search(path.read_text(encoding="utf-8"))
        assert block, f"{path.relative_to(ROOT)} emits no recognizable frontmatter block"
        note_type = frontmatter_type(block.group(1))
        assert note_type, f"{path.relative_to(ROOT)} emits frontmatter without a type"
        generators[note_type] = (path, frontmatter_keys(block.group(1)))

    paired = sorted(set(templates) & set(generators))
    assert paired, "no note type has both a template and a scripts/new-*.py generator"

    for note_type in paired:
        template_path, template_keys = templates[note_type]
        generator_path, generator_keys = generators[note_type]
        needed = required.get(note_type, set())
        assert needed <= template_keys, (
            f"{template_path.relative_to(ROOT)} is missing frontmatter keys required by "
            f"scripts/vault-lint.py for type {note_type}: "
            f"{sorted(needed - template_keys)}"
        )
        assert needed <= generator_keys, (
            f"{generator_path.relative_to(ROOT)} emits notes that vault-lint would reject: "
            f"missing required keys for type {note_type}: {sorted(needed - generator_keys)}"
        )
        assert template_keys <= generator_keys, (
            f"{generator_path.relative_to(ROOT)} drops frontmatter keys documented in "
            f"{template_path.relative_to(ROOT)} for type {note_type}: "
            f"{sorted(template_keys - generator_keys)}"
        )


def test_generator_id_prefixes_match_linter_patterns() -> None:
    """A dated-ID generator must emit IDs the linter's pattern accepts."""

    lint = load_vault_lint()
    checked = 0
    for path in sorted(SCRIPTS.glob("new-*.py")):
        source = path.read_text(encoding="utf-8")
        block = GENERATOR_FRONTMATTER.search(source)
        assert block, f"{path.relative_to(ROOT)} emits no recognizable frontmatter block"
        note_type = frontmatter_type(block.group(1))
        pattern = lint.ID_PATTERNS.get(note_type)
        prefix = re.search(r'next_dated_id\(\s*"([A-Z]+)"', source)
        if pattern is None or prefix is None:
            continue
        sample = f"{prefix.group(1)}-20260101-001"
        assert pattern.fullmatch(sample), (
            f"{path.relative_to(ROOT)} mints {sample!r} for type {note_type}, which "
            f"scripts/vault-lint.py rejects with {pattern.pattern!r}"
        )
        checked += 1
    assert checked, "no dated-ID generator was checked"


def executable_python_scripts() -> list[Path]:
    found = []
    for path in sorted(SCRIPTS.iterdir()):
        if not path.is_file() or not os.access(path, os.X_OK):
            continue
        try:
            first = path.open("rb").readline().decode("utf-8", errors="replace")
        except OSError:  # pragma: no cover - unreadable file
            continue
        if first.startswith("#!") and "env python3" in first:
            found.append(path)
    return found


def test_executable_python_scripts_parse() -> None:
    scripts = executable_python_scripts()
    assert scripts, "no executable python3 scripts found in scripts/"
    failures = []
    for path in scripts:
        source = path.read_text(encoding="utf-8", errors="replace")
        try:
            ast.parse(source, filename=str(path))
        except SyntaxError as error:
            failures.append(f"{path.relative_to(ROOT)}: {error}")
    assert not failures, "scripts fail to parse:\n" + "\n".join(failures)


def test_new_hygiene_scripts_are_executable_with_a_shebang() -> None:
    for name in ("vault-lint.py", "claim-sweep.py"):
        path = SCRIPTS / name
        assert path.is_file(), f"{name} is missing"
        assert os.access(path, os.X_OK), f"{name} is not executable"
        assert path.open("rb").readline().startswith(b"#!/usr/bin/env python3")
