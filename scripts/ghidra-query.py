#!/usr/bin/env python3
"""Read-only query CLI over the Ghidra JSON export of ``bugs.exe``.

``static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`` is a single-line
7.7 MB document.  Any naive read pulls the whole thing into an agent's
context, so the export has in practice been unreadable and several audit
rounds were spent on questions the export already answered.  This tool makes
it queryable: every verb returns bounded machine-readable JSON, and nothing
here writes to the export.

Export schema (verified against the real file, not assumed)::

    {"program": {"name", "executable_sha256", "image_base"},
     "functions": [{"address": "00432930",        # bare lower 8-hex
                    "name", "prototype",
                    "callers":  ["0042ddc7", ...],
                    "callees":  ["00401659", "EXTERNAL:00000074", ...],
                    "data_references": [{"from", "to", "type"}],
                    "decompiler": "<C pseudocode>"}],
     "strings": [{"address", "value"}],
     "imports": []}

Three schema facts drive the design and are surfaced in the output rather
than smoothed over:

- ``callers`` holds *call-site instruction addresses*, not function entry
  addresses (4464 of 4468 entries in the real export are not function
  entries).  Naming the calling function therefore requires resolving a site
  to its containing function, which this tool does with a
  nearest-preceding-entry heuristic and labels ``exact: false``.  Each such
  edge is cross-checked against the candidate owner's ``callees`` list and
  reported as ``corroborated`` or not.
- ``callees`` holds function entry addresses plus ``EXTERNAL:<ordinal>``
  pseudo-addresses for imported routines.  ``imports`` is empty, so those
  ordinals cannot be resolved to API names from this export alone.
- The call graph breaks at thunks: ``thunk_FUN_00432930`` (0x004019f1) has
  an empty ``callees`` list, so ``FUN_00432930`` looks uncalled.  The
  ``thunk_FUN_<addr>`` naming convention bridges it (486 thunks, all
  bridgeable in the real export).  That bridge is name-derived inference and
  is labelled ``thunk_name_bridge``, never merged into structured evidence.

Likewise ``xrefs`` reports structured ``data_references`` separately from
decompiler *text* matches; a text match is weaker evidence and is never
conflated with a recorded reference.

Exit codes follow ``evidence_lib``: 0 ok, 1 tool-negative (nothing found),
2 usage error, 3 structured refusal.
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import evidence_lib as ev  # noqa: E402


TOOL = "ghidra-query"
TOOL_VERSION = "1.0.0"
SCHEMA_VERSION = 1
INDEX_SCHEMA_VERSION = 1

DEFAULT_EXPORT = "static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json"
INDEX_SUFFIX = ".index.json"

MAX_DEPTH = 4
DEFAULT_MAX_DECOMPILER_BYTES = 200_000
DEFAULT_MAX_HITS = 50
DEFAULT_MAX_HITS_PER_FUNCTION = 5
DEFAULT_CONTEXT_CHARS = 160
DEFAULT_MAX_DATA_REFERENCES = 500
DEFAULT_TOP = 10
MAX_FIRST_LINE_CHARS = 120
MAX_STRING_VALUE_CHARS = 512

EXTERNAL_PREFIX = "EXTERNAL:"
THUNK_PREFIX = "thunk_FUN_"

GREP_FIELDS = ("decompiler", "name", "prototype", "all")


class UsageError(ValueError):
    """Raised for a malformed request that the caller can fix."""


class Refusal(Exception):
    """Raised when the tool cannot answer trustworthily."""

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(detail or reason)
        self.reason = reason
        self.detail = detail


# --------------------------------------------------------------------------
# Addresses
# --------------------------------------------------------------------------


def normalize_address(text: str) -> str:
    """Normalize an address to the export's bare lowercase 8-hex form.

    Accepts ``0x00432930``, ``00432930``, ``432930``, ``0X432930``,
    ``0x432930``, and the export's ``EXTERNAL:<ordinal>`` pseudo-addresses.
    """

    if not isinstance(text, str):
        raise UsageError(f"address must be a string, got {type(text).__name__}")
    value = text.strip()
    if not value:
        raise UsageError("empty address")
    if value.upper().startswith(EXTERNAL_PREFIX):
        tail = value[len(EXTERNAL_PREFIX):]
        try:
            ordinal = int(tail, 16)
        except ValueError as exc:
            raise UsageError(f"not an EXTERNAL ordinal: {text!r}") from exc
        if not 0 <= ordinal <= 0xFFFFFFFF:
            raise UsageError(f"EXTERNAL ordinal out of range: {text!r}")
        return f"{EXTERNAL_PREFIX}{ordinal:08x}"
    if value[:2].lower() == "0x":
        value = value[2:]
    if not value:
        raise UsageError(f"not an address: {text!r}")
    if any(ch not in "0123456789abcdefABCDEF" for ch in value):
        raise UsageError(f"not a hex address: {text!r}")
    parsed = int(value, 16)
    if parsed > 0xFFFFFFFF:
        raise UsageError(f"address out of 32-bit range: {text!r}")
    return f"{parsed:08x}"


def address_text_pattern(addr: str) -> re.Pattern[str]:
    """Regex matching the textual forms of ``addr`` in decompiler output.

    Covers ``0x005c5864``, ``0x5c5864``, ``005c5864`` and identifier suffixes
    such as ``DAT_005c5864`` / ``FUN_005c5864``, while rejecting a longer
    number that merely ends in the same digits (``0x15c5864``).
    """

    core = addr.lstrip("0") or "0"
    return re.compile(
        r"(?<![0-9A-Fa-f])(?:0[xX])?0*" + re.escape(core) + r"(?![0-9A-Fa-f])",
        re.IGNORECASE,
    )


def thunk_target(name: str) -> str | None:
    """Return the address a ``thunk_FUN_<addr>`` name points at, else None."""

    if not name.startswith(THUNK_PREFIX):
        return None
    tail = name[len(THUNK_PREFIX):]
    if len(tail) != 8 or any(ch not in "0123456789abcdef" for ch in tail):
        return None
    return tail


# --------------------------------------------------------------------------
# Export loading
# --------------------------------------------------------------------------


def default_export_path(root: Path | None = None) -> Path:
    return (root or ev.repo_root()) / DEFAULT_EXPORT


def index_path_for(export_path: Path) -> Path:
    return export_path.with_name(export_path.name.rsplit(".json", 1)[0] + INDEX_SUFFIX)


def _first_line(decompiler: str) -> str:
    fallback = ""
    for raw in decompiler.splitlines():
        line = raw.strip()
        if not line:
            continue
        if not fallback:
            fallback = line
        if line.startswith("/*") or line.startswith("*") or line.startswith("//"):
            continue
        return line[:MAX_FIRST_LINE_CHARS]
    return fallback[:MAX_FIRST_LINE_CHARS]


class Export:
    """A parsed export plus the derived maps the verbs need."""

    def __init__(self, path: Path, data: dict[str, Any], load_seconds: float) -> None:
        self.path = path
        self.data = data
        self.load_seconds = load_seconds
        self.program: dict[str, Any] = data.get("program") or {}
        self.functions: list[dict[str, Any]] = data["functions"]
        self.strings: list[dict[str, Any]] = data.get("strings") or []
        self.imports: list[Any] = data.get("imports") or []

        self.by_address: dict[str, dict[str, Any]] = {}
        self.by_name: dict[str, str] = {}
        self.ambiguous_names: dict[str, list[str]] = {}
        self.thunks: dict[str, str] = {}
        self.reverse_calls: dict[str, list[str]] = {}

        name_hits: dict[str, list[str]] = {}
        for func in self.functions:
            addr = func["address"]
            self.by_address[addr] = func
            name_hits.setdefault(func["name"], []).append(addr)
        for name, addrs in name_hits.items():
            if len(addrs) == 1:
                self.by_name[name] = addrs[0]
            else:
                self.ambiguous_names[name] = sorted(addrs)

        for func in self.functions:
            target = thunk_target(func["name"])
            if target is not None and target in self.by_address:
                self.thunks[func["address"]] = target
            for callee in func["callees"]:
                self.reverse_calls.setdefault(callee, []).append(func["address"])
        for addrs in self.reverse_calls.values():
            addrs.sort()

        # thunk address -> thunks that bridge to it, for reverse traversal.
        self.thunks_for_target: dict[str, list[str]] = {}
        for thunk_addr, target in self.thunks.items():
            self.thunks_for_target.setdefault(target, []).append(thunk_addr)
        for addrs in self.thunks_for_target.values():
            addrs.sort()

        self.entries: list[str] = sorted(self.by_address)

    # -- lookups ----------------------------------------------------------

    def owner_of_site(self, site: str) -> str | None:
        """Nearest preceding function entry for a call-site address.

        Heuristic: the export records no function extents, so a site that
        falls in a gap resolves to the function before the gap.  Callers must
        treat the result as inference (see ``exact: false``).
        """

        if site.startswith(EXTERNAL_PREFIX):
            return None
        index = bisect.bisect_right(self.entries, site) - 1
        if index < 0:
            return None
        return self.entries[index]

    def name_of(self, addr: str) -> str | None:
        func = self.by_address.get(addr)
        return func["name"] if func else None

    def resolve_name(self, name: str) -> str:
        if name in self.ambiguous_names:
            raise Refusal(
                "ambiguous_name",
                f"{name!r} names {len(self.ambiguous_names[name])} functions: "
                + ", ".join(self.ambiguous_names[name]),
            )
        addr = self.by_name.get(name)
        if addr is None:
            raise KeyError(name)
        return addr


def load_export(path: Path) -> Export:
    try:
        raw = path.read_bytes()
    except FileNotFoundError as exc:
        raise Refusal("export_missing", f"no such export: {path}") from exc
    except OSError as exc:
        raise Refusal("export_unreadable", f"{path}: {exc}") from exc
    started = time.perf_counter()
    try:
        data = json.loads(raw)
    except ValueError as exc:
        raise Refusal("export_malformed", f"{path}: {exc}") from exc
    elapsed = time.perf_counter() - started
    if not isinstance(data, dict) or not isinstance(data.get("functions"), list):
        raise Refusal("export_malformed",
                      f"{path}: expected an object with a 'functions' list")
    for i, func in enumerate(data["functions"]):
        if not isinstance(func, dict):
            raise Refusal("export_malformed", f"{path}: functions[{i}] is not an object")
        for key in ("address", "name", "prototype", "callers", "callees",
                    "data_references", "decompiler"):
            if key not in func:
                raise Refusal("export_malformed",
                              f"{path}: functions[{i}] missing {key!r}")
    return Export(path, data, elapsed)


def source_stamp(path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "path": str(path),
        "sha256": ev.sha256_file(path),
        "size_bytes": stat.st_size,
        "mtime": round(stat.st_mtime, 6),
    }


# --------------------------------------------------------------------------
# Index
# --------------------------------------------------------------------------


def build_index(export: Export) -> dict[str, Any]:
    functions: dict[str, Any] = {}
    for func in export.functions:
        entry: dict[str, Any] = {
            "name": func["name"],
            "prototype": func["prototype"],
            "decompiler_bytes": len(func["decompiler"].encode("utf-8")),
            "data_reference_count": len(func["data_references"]),
            "first_line": _first_line(func["decompiler"]),
        }
        if func["callers"]:
            entry["callers"] = list(func["callers"])
        if func["callees"]:
            entry["callees"] = list(func["callees"])
        target = export.thunks.get(func["address"])
        if target is not None:
            entry["thunk_target"] = target
        functions[func["address"]] = entry

    return {
        "schema_version": INDEX_SCHEMA_VERSION,
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "source": source_stamp(export.path),
        "program": export.program,
        "counts": {
            "functions": len(export.functions),
            "strings": len(export.strings),
            "imports": len(export.imports),
            "thunks": len(export.thunks),
            "data_references": sum(len(f["data_references"]) for f in export.functions),
        },
        "notes": [
            "'callers' entries are call-site instruction addresses, not "
            "function entries; resolve them with the 'callers' verb.",
            "'callees' entries are function entries plus EXTERNAL:<ordinal> "
            "pseudo-addresses; the export's imports table is empty.",
            "thunk functions carry no callees; 'thunk_target' is derived from "
            "the thunk_FUN_<addr> name and is inference, not a recorded edge.",
        ],
        "functions": functions,
        "names": export.by_name,
        "ambiguous_names": export.ambiguous_names,
        "reverse_calls": export.reverse_calls,
    }


INDEX_LINE_KEYS = ("functions", "names", "ambiguous_names", "reverse_calls")


def render_index(index: dict[str, Any], *, compact: bool = False) -> str:
    """Serialize the index so that each function entry is one greppable line.

    Pretty-printing the whole thing with ``indent`` would bloat it; a single
    line would be ungreppable.  One record per line keeps the file small and
    lets an agent grep it without loading the export.
    """

    if compact:
        return json.dumps(index) + "\n"
    parts: list[str] = []
    for key, value in index.items():
        if key in INDEX_LINE_KEYS and isinstance(value, dict):
            if not value:
                parts.append(f"{json.dumps(key)}: {{}}")
                continue
            inner = ",\n".join(
                f"{json.dumps(str(k))}: {json.dumps(v)}" for k, v in value.items()
            )
            parts.append(f"{json.dumps(key)}: {{\n{inner}\n}}")
        else:
            parts.append(f"{json.dumps(key)}: {json.dumps(value, indent=1)}")
    return "{\n" + ",\n".join(parts) + "\n}\n"


def index_staleness(index: dict[str, Any], export_path: Path) -> dict[str, Any]:
    recorded = index.get("source") or {}
    try:
        current = source_stamp(export_path)
    except OSError as exc:
        return {"stale": True, "reason": f"export unreadable: {exc}"}
    reasons: list[str] = []
    if recorded.get("sha256") != current["sha256"]:
        reasons.append("sha256 differs")
    if recorded.get("size_bytes") != current["size_bytes"]:
        reasons.append("size differs")
    if recorded.get("mtime") != current["mtime"]:
        reasons.append("mtime differs")
    if index.get("schema_version") != INDEX_SCHEMA_VERSION:
        reasons.append("index schema_version differs")
    # mtime alone is not proof of a content change; sha256 decides staleness.
    content_changed = recorded.get("sha256") != current["sha256"]
    return {
        "stale": bool(content_changed or index.get("schema_version") != INDEX_SCHEMA_VERSION),
        "reasons": reasons,
        "recorded": recorded,
        "current": current,
    }


# --------------------------------------------------------------------------
# Verbs
# --------------------------------------------------------------------------


def function_record(export: Export, addr: str, *, include_decompiler: bool = True,
                    max_decompiler_bytes: int = DEFAULT_MAX_DECOMPILER_BYTES,
                    max_data_references: int = DEFAULT_MAX_DATA_REFERENCES,
                    ) -> dict[str, Any]:
    func = export.by_address[addr]
    decompiler = func["decompiler"]
    encoded = decompiler.encode("utf-8")
    record: dict[str, Any] = {
        "address": func["address"],
        "name": func["name"],
        "prototype": func["prototype"],
        "callers": list(func["callers"]),
        "callees": list(func["callees"]),
        "caller_count": len(func["callers"]),
        "callee_count": len(func["callees"]),
        "decompiler_bytes": len(encoded),
        "first_line": _first_line(decompiler),
        "data_reference_count": len(func["data_references"]),
    }
    target = export.thunks.get(addr)
    if target is not None:
        record["thunk_target"] = target
        record["thunk_target_name"] = export.name_of(target)
        record["thunk_target_evidence"] = "thunk_name_bridge"
    refs = func["data_references"]
    record["data_references"] = [dict(r) for r in refs[:max_data_references]]
    record["data_references_truncated"] = len(refs) > max_data_references
    if include_decompiler:
        if len(encoded) > max_decompiler_bytes:
            record["decompiler"] = encoded[:max_decompiler_bytes].decode("utf-8", "ignore")
            record["decompiler_truncated"] = True
        else:
            record["decompiler"] = decompiler
            record["decompiler_truncated"] = False
    else:
        record["decompiler_omitted"] = True
    return record


CALLER_CAVEATS = [
    "callsite_owner edges resolve a call-site address to the nearest "
    "preceding function entry; the export records no function extents, so "
    "they are inference (exact=false) and are cross-checked against the "
    "owner's callees list via 'corroborated'.",
    "thunk_name_bridge edges are derived from the thunk_FUN_<addr> naming "
    "convention, not from a recorded call edge.",
]

CALLEE_CAVEATS = [
    "EXTERNAL:<ordinal> callees are imported routines; the export's imports "
    "table is empty, so no API name is available here.",
    "thunk_name_bridge edges are derived from the thunk_FUN_<addr> naming "
    "convention, not from a recorded call edge.",
]


def _merge_edge(bucket: dict[str, dict[str, Any]], addr: str, name: str | None,
                evidence: dict[str, Any]) -> None:
    node = bucket.setdefault(addr, {"address": addr, "name": name, "evidence": []})
    if node.get("name") is None:
        node["name"] = name
    node["evidence"].append(evidence)


def callers_of(export: Export, addr: str, *, follow_thunks: bool = True,
               ) -> list[dict[str, Any]]:
    bucket: dict[str, dict[str, Any]] = {}
    func = export.by_address.get(addr)

    for caller in export.reverse_calls.get(addr, []):
        _merge_edge(bucket, caller, export.name_of(caller),
                    {"kind": "callee_edge", "exact": True})

    if func is not None:
        sites: dict[str, list[str]] = {}
        unresolved: list[str] = []
        for site in func["callers"]:
            owner = export.owner_of_site(site)
            if owner is None:
                unresolved.append(site)
                continue
            sites.setdefault(owner, []).append(site)
        for owner, owner_sites in sites.items():
            owner_func = export.by_address[owner]
            _merge_edge(bucket, owner, owner_func["name"], {
                "kind": "callsite_owner",
                "exact": False,
                "callsites": sorted(owner_sites),
                "corroborated": addr in owner_func["callees"],
            })
        for site in unresolved:
            _merge_edge(bucket, site, None,
                        {"kind": "unresolved_callsite", "exact": False})

    if follow_thunks:
        for thunk_addr in export.thunks_for_target.get(addr, []):
            for edge in callers_of(export, thunk_addr, follow_thunks=False):
                for evidence in edge["evidence"]:
                    bridged = dict(evidence)
                    bridged["kind"] = "thunk_name_bridge"
                    bridged["exact"] = False
                    bridged["via_thunk"] = thunk_addr
                    bridged["via_thunk_name"] = export.name_of(thunk_addr)
                    bridged["underlying_kind"] = evidence["kind"]
                    _merge_edge(bucket, edge["address"], edge["name"], bridged)

    return [bucket[key] for key in sorted(bucket)]


def callees_of(export: Export, addr: str, *, follow_thunks: bool = True,
               ) -> list[dict[str, Any]]:
    bucket: dict[str, dict[str, Any]] = {}
    func = export.by_address.get(addr)
    if func is None:
        return []
    for callee in func["callees"]:
        _merge_edge(bucket, callee, export.name_of(callee),
                    {"kind": "callee_edge", "exact": True})
        target = export.thunks.get(callee)
        if target is not None:
            bucket[callee]["thunk_target"] = target
            if follow_thunks:
                _merge_edge(bucket, target, export.name_of(target), {
                    "kind": "thunk_name_bridge",
                    "exact": False,
                    "via_thunk": callee,
                    "via_thunk_name": export.name_of(callee),
                    "underlying_kind": "callee_edge",
                })
    if follow_thunks:
        target = export.thunks.get(addr)
        if target is not None and target not in bucket:
            _merge_edge(bucket, target, export.name_of(target), {
                "kind": "thunk_name_bridge",
                "exact": False,
                "via_thunk": addr,
                "via_thunk_name": func["name"],
                "underlying_kind": "thunk_body",
            })
    return [bucket[key] for key in sorted(bucket)]


def walk_calls(export: Export, addr: str, *, direction: str, depth: int,
               follow_thunks: bool = True) -> dict[str, Any]:
    """Breadth-first traversal with a depth cap and cycle protection."""

    step = callers_of if direction == "callers" else callees_of
    seen: set[str] = {addr}
    nodes: list[dict[str, Any]] = []
    frontier: list[str] = [addr]
    truncated = False
    for level in range(1, depth + 1):
        next_frontier: list[str] = []
        for current in frontier:
            for edge in step(export, current, follow_thunks=follow_thunks):
                node_addr = edge["address"]
                if node_addr in seen:
                    continue
                seen.add(node_addr)
                record = dict(edge)
                record["depth"] = level
                record["from"] = current
                nodes.append(record)
                if node_addr in export.by_address:
                    next_frontier.append(node_addr)
        frontier = next_frontier
        if not frontier:
            break
    else:
        truncated = bool(frontier)
    return {"nodes": nodes, "truncated_at_depth": truncated}


def _bounded_context(text: str, start: int, end: int, context_chars: int) -> dict[str, Any]:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end < 0:
        line_end = len(text)
    line = text[line_start:line_end]
    line_number = text.count("\n", 0, start) + 1
    if len(line) > context_chars:
        offset = start - line_start
        left = max(0, offset - context_chars // 2)
        line = ("..." if left else "") + line[left:left + context_chars] + "..."
    return {"line": line_number, "context": line, "match": text[start:end][:context_chars]}


def xrefs_to(export: Export, target: str, *, max_hits: int = DEFAULT_MAX_HITS,
             max_hits_per_function: int = DEFAULT_MAX_HITS_PER_FUNCTION,
             context_chars: int = DEFAULT_CONTEXT_CHARS) -> dict[str, Any]:
    structured: list[dict[str, Any]] = []
    structured_truncated = False
    for func in export.functions:
        matched = [r for r in func["data_references"]
                   if r.get("to") == target or r.get("from") == target]
        if not matched:
            continue
        if len(structured) >= max_hits:
            structured_truncated = True
            break
        structured.append({
            "address": func["address"],
            "name": func["name"],
            "reference_count": len(matched),
            "references": [dict(r) for r in matched[:max_hits_per_function]],
            "references_truncated": len(matched) > max_hits_per_function,
        })

    pattern = address_text_pattern(target)
    textual: list[dict[str, Any]] = []
    text_truncated = False
    for func in export.functions:
        decompiler = func["decompiler"]
        found = list(pattern.finditer(decompiler))
        if not found:
            continue
        if len(textual) >= max_hits:
            text_truncated = True
            break
        matches = [_bounded_context(decompiler, m.start(), m.end(), context_chars)
                   for m in found[:max_hits_per_function]]
        textual.append({
            "address": func["address"],
            "name": func["name"],
            "match_count": len(found),
            "matches": matches,
            "matches_truncated": len(found) > max_hits_per_function,
        })

    return {
        "target": target,
        "evidence_kinds": ["data_references", "decompiler_text"],
        "data_references": {
            "functions": structured,
            "function_count": len(structured),
            "hits_truncated": structured_truncated,
        },
        "decompiler_text": {
            "functions": textual,
            "function_count": len(textual),
            "hits_truncated": text_truncated,
            "note": "a text match is weaker evidence than a recorded "
                    "data reference and is reported separately on purpose",
        },
    }


def grep_functions(export: Export, pattern: re.Pattern[str], *, field: str = "decompiler",
                   max_hits: int = DEFAULT_MAX_HITS,
                   max_hits_per_function: int = DEFAULT_MAX_HITS_PER_FUNCTION,
                   context_chars: int = DEFAULT_CONTEXT_CHARS) -> dict[str, Any]:
    fields = ("decompiler", "name", "prototype") if field == "all" else (field,)
    hits: list[dict[str, Any]] = []
    truncated = False
    for func in export.functions:
        if len(hits) >= max_hits:
            truncated = True
            break
        entry_matches: list[dict[str, Any]] = []
        total = 0
        for name in fields:
            text = func[name]
            found = list(pattern.finditer(text))
            if not found:
                continue
            total += len(found)
            room = max(0, max_hits_per_function - len(entry_matches))
            for match in found[:room]:
                context = _bounded_context(text, match.start(), match.end(), context_chars)
                context["field"] = name
                entry_matches.append(context)
        if not entry_matches:
            continue
        hits.append({
            "address": func["address"],
            "name": func["name"],
            "match_count": total,
            "matches": entry_matches,
            "matches_truncated": total > len(entry_matches),
        })
    return {
        "fields": list(fields),
        "hits": hits,
        "hit_count": len(hits),
        "hits_truncated": truncated,
    }


def grep_strings(export: Export, pattern: re.Pattern[str], *,
                 max_hits: int = DEFAULT_MAX_HITS) -> dict[str, Any]:
    hits: list[dict[str, Any]] = []
    truncated = False
    for entry in export.strings:
        value = entry.get("value", "")
        if not pattern.search(value):
            continue
        if len(hits) >= max_hits:
            truncated = True
            break
        hits.append({
            "address": entry.get("address"),
            "value": value[:MAX_STRING_VALUE_CHARS],
            "value_truncated": len(value) > MAX_STRING_VALUE_CHARS,
        })
    return {"hits": hits, "hit_count": len(hits), "hits_truncated": truncated}


def stats(export: Export, *, top: int = DEFAULT_TOP) -> dict[str, Any]:
    sizes = sorted(
        ((len(f["decompiler"].encode("utf-8")), f["address"], f["name"])
         for f in export.functions),
        reverse=True,
    )
    external = 0
    for func in export.functions:
        external += sum(1 for c in func["callees"] if c.startswith(EXTERNAL_PREFIX))
    total_bytes = sum(size for size, _, _ in sizes)
    warnings: list[str] = []
    if not export.imports:
        warnings.append(
            f"imports table is empty; {external} callee entries use the "
            "EXTERNAL:<ordinal> form and cannot be resolved to API names "
            "from this export alone"
        )
    if export.ambiguous_names:
        warnings.append(
            f"{len(export.ambiguous_names)} function name(s) are not unique; "
            "--name lookups for them are refused"
        )
    return {
        "program": export.program,
        "counts": {
            "functions": len(export.functions),
            "strings": len(export.strings),
            "imports": len(export.imports),
            "thunks": len(export.thunks),
            "data_references": sum(len(f["data_references"]) for f in export.functions),
            "external_callee_edges": external,
        },
        "decompiler_bytes": {
            "total": total_bytes,
            "mean": total_bytes // len(sizes) if sizes else 0,
            "max": sizes[0][0] if sizes else 0,
        },
        "largest_functions": [
            {"address": addr, "name": name, "decompiler_bytes": size}
            for size, addr, name in sizes[:max(0, top)]
        ],
        "warnings": warnings,
        "load_seconds": round(export.load_seconds, 4),
    }


def capabilities(export_path: Path) -> dict[str, Any]:
    source: dict[str, Any] = {"path": str(export_path), "exists": export_path.exists()}
    if source["exists"]:
        try:
            source.update(source_stamp(export_path))
        except OSError as exc:  # pragma: no cover - unreadable but present
            source["error"] = str(exc)
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL,
        "tool_version": TOOL_VERSION,
        "mode": "read-only",
        "verbs": ["index", "function", "callers", "callees", "xrefs", "grep",
                  "strings", "stats"],
        "write_verbs": ["index"],
        "writes": "only the sidecar index file named by 'index --out'",
        "limits": {
            "max_depth": MAX_DEPTH,
            "default_max_decompiler_bytes": DEFAULT_MAX_DECOMPILER_BYTES,
            "default_max_hits": DEFAULT_MAX_HITS,
            "default_max_hits_per_function": DEFAULT_MAX_HITS_PER_FUNCTION,
            "default_context_chars": DEFAULT_CONTEXT_CHARS,
            "default_max_data_references": DEFAULT_MAX_DATA_REFERENCES,
            "max_string_value_chars": MAX_STRING_VALUE_CHARS,
        },
        "address_forms_accepted": ["0x00432930", "00432930", "432930",
                                   "case-insensitive", "EXTERNAL:00000074"],
        "address_form_emitted": "bare lowercase 8-hex (the export's own form)",
        "evidence_kinds": {
            "callee_edge": "recorded in the export's callees list (exact)",
            "callsite_owner": "call-site address resolved to the nearest "
                              "preceding function entry (inference)",
            "unresolved_callsite": "call-site address with no preceding entry",
            "thunk_name_bridge": "edge derived from the thunk_FUN_<addr> "
                                 "naming convention (inference)",
            "data_references": "structured reference recorded by Ghidra",
            "decompiler_text": "textual match in decompiler output (weakest)",
        },
        "refusal_reasons": ["export_missing", "export_unreadable",
                            "export_malformed", "ambiguous_name",
                            "index_missing", "index_malformed"],
        "exit_codes": {"ok": ev.EXIT_OK, "tool_negative": ev.EXIT_TOOL_NEGATIVE,
                       "usage": ev.EXIT_USAGE, "refusal": ev.EXIT_REFUSAL},
        "source": source,
        "index_path": str(index_path_for(export_path)),
        "index_schema_version": INDEX_SCHEMA_VERSION,
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _emit(payload: dict[str, Any], args: argparse.Namespace) -> None:
    compact = getattr(args, "compact", False)
    print(json.dumps(payload, indent=None if compact else 2, sort_keys=False))


def _export_path(args: argparse.Namespace) -> Path:
    override = getattr(args, "export", None)
    if override:
        return Path(override).expanduser()
    return default_export_path()


def _compile(pattern: str, ignore_case: bool) -> re.Pattern[str]:
    try:
        return re.compile(pattern, re.IGNORECASE if ignore_case else 0)
    except re.error as exc:
        raise UsageError(f"invalid regex {pattern!r}: {exc}") from exc


def _resolve_target(export: Export, args: argparse.Namespace) -> str | None:
    """Return the requested function address, or None if it is absent."""

    if getattr(args, "name", None):
        try:
            return export.resolve_name(args.name)
        except KeyError:
            return None
    return normalize_address(args.addr)


def _cmd_index(args: argparse.Namespace) -> int:
    export_path = _export_path(args)
    out = Path(args.out).expanduser() if args.out else index_path_for(export_path)
    if args.check:
        if not out.exists():
            _emit({"tool": TOOL, "index": str(out), "present": False, "stale": True,
                   "reason": "index has not been built"}, args)
            return ev.EXIT_TOOL_NEGATIVE
        try:
            index = json.loads(out.read_text())
        except (OSError, ValueError) as exc:
            raise Refusal("index_malformed", f"{out}: {exc}")
        status = index_staleness(index, export_path)
        _emit({"tool": TOOL, "index": str(out), "present": True, **status}, args)
        return ev.EXIT_TOOL_NEGATIVE if status["stale"] else ev.EXIT_OK

    export = load_export(export_path)
    index = build_index(export)
    text = render_index(index, compact=args.compact_index)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    _emit({
        "tool": TOOL,
        "index": str(out),
        "index_bytes": len(text.encode("utf-8")),
        "counts": index["counts"],
        "source": index["source"],
    }, args)
    return ev.EXIT_OK


def _cmd_function(args: argparse.Namespace) -> int:
    if bool(args.addr) == bool(args.name):
        raise UsageError("give exactly one of --addr or --name")
    if args.max_decompiler_bytes < 0:
        raise UsageError("--max-decompiler-bytes must be >= 0")
    if args.max_data_references < 0:
        raise UsageError("--max-data-references must be >= 0")
    export = load_export(_export_path(args))
    addr = _resolve_target(export, args)
    if addr is None or addr not in export.by_address:
        _emit({"tool": TOOL, "query": {"addr": args.addr, "name": args.name},
               "normalized_address": addr, "found": False,
               "detail": "no such function in the export"}, args)
        return ev.EXIT_TOOL_NEGATIVE
    record = function_record(
        export, addr,
        include_decompiler=not args.no_decompiler,
        max_decompiler_bytes=args.max_decompiler_bytes,
        max_data_references=args.max_data_references,
    )
    _emit({"tool": TOOL, "found": True, "function": record}, args)
    return ev.EXIT_OK


def _cmd_calls(args: argparse.Namespace, direction: str) -> int:
    if bool(args.addr) == bool(args.name):
        raise UsageError("give exactly one of --addr or --name")
    if args.depth < 1:
        raise UsageError("--depth must be >= 1")
    depth = min(args.depth, MAX_DEPTH)
    export = load_export(_export_path(args))
    addr = _resolve_target(export, args)
    if addr is None or addr not in export.by_address:
        _emit({"tool": TOOL, "query": {"addr": args.addr, "name": args.name},
               "found": False, "detail": "no such function in the export"}, args)
        return ev.EXIT_TOOL_NEGATIVE
    walk = walk_calls(export, addr, direction=direction, depth=depth,
                      follow_thunks=not args.no_follow_thunks)
    payload = {
        "tool": TOOL,
        "direction": direction,
        "root": {"address": addr, "name": export.name_of(addr)},
        "requested_depth": args.depth,
        "depth": depth,
        "depth_capped": args.depth > MAX_DEPTH,
        "max_depth": MAX_DEPTH,
        "follow_thunks": not args.no_follow_thunks,
        "count": len(walk["nodes"]),
        "nodes": walk["nodes"],
        "truncated_at_depth": walk["truncated_at_depth"],
        "caveats": CALLER_CAVEATS if direction == "callers" else CALLEE_CAVEATS,
    }
    _emit(payload, args)
    return ev.EXIT_OK if walk["nodes"] else ev.EXIT_TOOL_NEGATIVE


def _cmd_xrefs(args: argparse.Namespace) -> int:
    target = normalize_address(args.to)
    export = load_export(_export_path(args))
    result = xrefs_to(export, target, max_hits=args.max_hits,
                      max_hits_per_function=args.max_hits_per_function,
                      context_chars=args.context_chars)
    result["tool"] = TOOL
    _emit(result, args)
    found = result["data_references"]["function_count"] or \
        result["decompiler_text"]["function_count"]
    return ev.EXIT_OK if found else ev.EXIT_TOOL_NEGATIVE


def _cmd_grep(args: argparse.Namespace) -> int:
    if args.field not in GREP_FIELDS:
        raise UsageError(f"--in must be one of {', '.join(GREP_FIELDS)}")
    pattern = _compile(args.pattern, args.ignore_case)
    export = load_export(_export_path(args))
    result = grep_functions(export, pattern, field=args.field,
                            max_hits=args.max_hits,
                            max_hits_per_function=args.max_hits_per_function,
                            context_chars=args.context_chars)
    result["tool"] = TOOL
    result["pattern"] = args.pattern
    _emit(result, args)
    return ev.EXIT_OK if result["hit_count"] else ev.EXIT_TOOL_NEGATIVE


def _cmd_strings(args: argparse.Namespace) -> int:
    pattern = _compile(args.pattern, args.ignore_case)
    export = load_export(_export_path(args))
    result = grep_strings(export, pattern, max_hits=args.max_hits)
    result["tool"] = TOOL
    result["pattern"] = args.pattern
    _emit(result, args)
    return ev.EXIT_OK if result["hit_count"] else ev.EXIT_TOOL_NEGATIVE


def _cmd_stats(args: argparse.Namespace) -> int:
    export = load_export(_export_path(args))
    result = stats(export, top=args.top)
    result["tool"] = TOOL
    _emit(result, args)
    return ev.EXIT_OK


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--export", default=argparse.SUPPRESS,
                        help=f"export JSON to query (default: {DEFAULT_EXPORT})")
    parser.add_argument("--compact", action="store_true", default=argparse.SUPPRESS,
                        help="emit single-line JSON")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=TOOL, description="Query the Ghidra JSON export of bugs.exe")
    _add_common(parser)
    parser.add_argument("--capabilities", action="store_true",
                        help="print machine-readable capabilities and exit")
    sub = parser.add_subparsers(dest="command")

    idx = sub.add_parser("index", help="build or check the compact sidecar index")
    _add_common(idx)
    idx.add_argument("--out", help="index path (default: <export>.index.json)")
    idx.add_argument("--check", action="store_true",
                     help="report staleness instead of writing")
    idx.add_argument("--compact-index", action="store_true",
                     help="write the index as one line")

    fn = sub.add_parser("function", help="print one function record")
    _add_common(fn)
    fn.add_argument("--addr", help="function address (0x-prefixed or bare hex)")
    fn.add_argument("--name", help="function name")
    fn.add_argument("--no-decompiler", action="store_true",
                    help="omit the decompiler body")
    fn.add_argument("--max-decompiler-bytes", type=int,
                    default=DEFAULT_MAX_DECOMPILER_BYTES)
    fn.add_argument("--max-data-references", type=int,
                    default=DEFAULT_MAX_DATA_REFERENCES)

    for verb in ("callers", "callees"):
        cmd = sub.add_parser(verb, help=f"list {verb} of a function")
        _add_common(cmd)
        cmd.add_argument("--addr", help="function address")
        cmd.add_argument("--name", help="function name")
        cmd.add_argument("--depth", type=int, default=1,
                         help=f"transitive depth, capped at {MAX_DEPTH}")
        cmd.add_argument("--no-follow-thunks", action="store_true",
                         help="do not bridge thunk_FUN_<addr> naming edges")

    xr = sub.add_parser("xrefs", help="find references to an address")
    _add_common(xr)
    xr.add_argument("--to", required=True, help="target address")
    xr.add_argument("--max-hits", type=int, default=DEFAULT_MAX_HITS)
    xr.add_argument("--max-hits-per-function", type=int,
                    default=DEFAULT_MAX_HITS_PER_FUNCTION)
    xr.add_argument("--context-chars", type=int, default=DEFAULT_CONTEXT_CHARS)

    gr = sub.add_parser("grep", help="regex search over function records")
    _add_common(gr)
    gr.add_argument("--pattern", required=True)
    gr.add_argument("--in", dest="field", default="decompiler",
                    choices=GREP_FIELDS)
    gr.add_argument("--ignore-case", action="store_true")
    gr.add_argument("--max-hits", type=int, default=DEFAULT_MAX_HITS)
    gr.add_argument("--max-hits-per-function", type=int,
                    default=DEFAULT_MAX_HITS_PER_FUNCTION)
    gr.add_argument("--context-chars", type=int, default=DEFAULT_CONTEXT_CHARS)

    st = sub.add_parser("strings", help="regex search over the strings table")
    _add_common(st)
    st.add_argument("--pattern", required=True)
    st.add_argument("--ignore-case", action="store_true")
    st.add_argument("--max-hits", type=int, default=DEFAULT_MAX_HITS)

    sd = sub.add_parser("stats", help="counts, largest functions, warnings")
    _add_common(sd)
    sd.add_argument("--top", type=int, default=DEFAULT_TOP)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if getattr(args, "capabilities", False):
        _emit(capabilities(_export_path(args)), args)
        return ev.EXIT_OK
    if not getattr(args, "command", None):
        parser.print_usage(sys.stderr)
        print(json.dumps({"error": "usage", "detail": "a subcommand is required"}))
        return ev.EXIT_USAGE

    handlers = {
        "index": _cmd_index,
        "function": _cmd_function,
        "callers": lambda a: _cmd_calls(a, "callers"),
        "callees": lambda a: _cmd_calls(a, "callees"),
        "xrefs": _cmd_xrefs,
        "grep": _cmd_grep,
        "strings": _cmd_strings,
        "stats": _cmd_stats,
    }
    try:
        return handlers[args.command](args)
    except UsageError as exc:
        print(json.dumps({"error": "usage", "detail": str(exc)}))
        return ev.EXIT_USAGE
    except Refusal as exc:
        print(json.dumps({"refused": True, "tool": TOOL,
                          "reason": exc.reason, "detail": exc.detail}))
        return ev.EXIT_REFUSAL


if __name__ == "__main__":
    sys.exit(main())
