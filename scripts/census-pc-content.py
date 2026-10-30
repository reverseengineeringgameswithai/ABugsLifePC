#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reimplementation.ablpc.content_census import (
    ContentCensusError,
    build_content_census,
    render_summary,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a metadata-only census of a derived PC game work tree."
    )
    parser.add_argument("source_root", type=Path)
    parser.add_argument("--log", action="append", default=[], metavar="LABEL=PATH")
    parser.add_argument("--json-output", required=True, type=Path)
    parser.add_argument("--summary-output", required=True, type=Path)
    args = parser.parse_args()

    logs: list[tuple[str, Path]] = []
    for value in args.log:
        if "=" not in value:
            parser.error("--log must use LABEL=PATH")
        label, path = value.split("=", 1)
        logs.append((label, Path(path)))

    try:
        census = build_content_census(args.source_root, logs)
    except (OSError, ContentCensusError) as error:
        print(f"census-pc-content: {error}", file=sys.stderr)
        return 2

    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(census, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )
    args.summary_output.write_text(render_summary(census), encoding="utf-8")
    print(
        f"inventoried {census['totals']['file_count']} files; "
        f"fingerprint={census['tree_fingerprint_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
