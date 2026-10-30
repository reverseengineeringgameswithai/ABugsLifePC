#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "originals"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


items = []
for path in sorted(p for p in SOURCE.rglob("*") if p.is_file() and p.name != ".gitkeep"):
    try:
        description = subprocess.run(
            ["file", "--brief", "--", str(path)],
            check=True, capture_output=True, text=True
        ).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        description = "file(1) unavailable"
    items.append({
        "path": path.relative_to(SOURCE).as_posix(),
        "size": path.stat().st_size,
        "sha256": sha256(path),
        "file_type": description,
    })

payload = {"source": str(SOURCE), "files": items, "file_count": len(items)}
(REPORTS / "original-file-inventory.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
lines = [
    "# Original file inventory", "",
    f"Source: `{SOURCE}`", "",
    f"Files: {len(items)}", "",
    "| Path | Size | SHA-256 | file(1) |",
    "|---|---:|---|---|",
]
for item in items:
    desc = item["file_type"].replace("|", "\\|")
    lines.append(f"| `{item['path']}` | {item['size']} | `{item['sha256']}` | {desc} |")
lines.extend(["", "This inventory operation did not modify any original.", ""])
(REPORTS / "original-file-inventory.md").write_text("\n".join(lines), encoding="utf-8")
print(f"Inventoried {len(items)} files without modifying originals.")
