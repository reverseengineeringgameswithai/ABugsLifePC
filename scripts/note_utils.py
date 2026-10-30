from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "Vault"
ID_LINE = re.compile(r"^id:\s*([^\s#]+)\s*$", re.MULTILINE)


def now():
    return datetime.now().astimezone()


def existing_ids(vault: Path = VAULT) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for path in vault.rglob("*.md"):
        if "99-Templates" in path.parts:
            continue
        match = ID_LINE.search(path.read_text(encoding="utf-8"))
        if match and match.group(1):
            found[match.group(1)] = path
    return found


def next_dated_id(prefix: str, vault: Path = VAULT) -> str:
    day = now().strftime("%Y%m%d")
    stem = f"{prefix}-{day}-"
    numbers = []
    for evidence_id in existing_ids(vault):
        if evidence_id.startswith(stem) and evidence_id[len(stem):].isdigit():
            numbers.append(int(evidence_id[len(stem):]))
    return f"{stem}{max(numbers, default=0) + 1:03d}"


def require_unique(evidence_id: str, vault: Path = VAULT) -> None:
    match = existing_ids(vault).get(evidence_id)
    if match:
        raise SystemExit(f"ID already exists: {evidence_id} in {match}")


def slug(text: str, limit: int = 60) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (value[:limit].rstrip("-") or "untitled")


def write_new(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(content.rstrip() + "\n")
    except FileExistsError:
        raise SystemExit(f"Refusing to overwrite existing note: {path}")
    return path
