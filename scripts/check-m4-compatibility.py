#!/usr/bin/env -S python3 -B
"""Validate an exact, asset-free versioned M4 compatibility statement."""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from reimplementation.ablpc.compatibility import (
    CompatibilityError,
    STATEMENT_RELATIVE,
    check_compatibility_statement,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="validate an exact versioned M4 compatibility statement"
    )
    parser.add_argument(
        "statement",
        nargs="?",
        type=Path,
        help=f"statement path (default: {STATEMENT_RELATIVE.as_posix()})",
    )
    args = parser.parse_args(argv)
    repo_root = REPO_ROOT
    statement_path = args.statement or repo_root / STATEMENT_RELATIVE
    if not statement_path.is_absolute():
        statement_path = Path.cwd() / statement_path
    try:
        statement = check_compatibility_statement(statement_path, repo_root)
    except CompatibilityError as error:
        print(f"M4 compatibility check failed: {error}", file=sys.stderr)
        return 2
    print(
        "M4 compatibility statement valid: "
        f"{statement['statement_id']} ({len(statement['hash_anchors'])} hash anchors)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
