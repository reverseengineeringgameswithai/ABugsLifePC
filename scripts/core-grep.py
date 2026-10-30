#!/usr/bin/env python3
"""Read-only scan of an ELF core dump for a byte pattern or dword value.

Reports the virtual addresses where a pattern occurs inside the core's PT_LOAD
segments, so a control-vs-mod snapshot pair can locate where specific bytes
landed in memory. This tool only reads; it never writes the core or any process.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import evidence_lib as ev


DEFAULT_CHUNK = 8 << 20  # 8 MiB


def scan_core(data: bytes, pattern: bytes, *, max_matches: int = 256,
              chunk_size: int = DEFAULT_CHUNK) -> dict:
    if not pattern:
        raise ValueError("empty search pattern")
    overlap = len(pattern) - 1
    matches: list[dict] = []
    segments_scanned = 0
    truncated_segments: list[int] = []
    capped = False

    for seg in ev.iter_core_load_segments(data):
        segments_scanned += 1
        if seg.truncated:
            truncated_segments.append(seg.index)
        avail = min(seg.file_size, len(data) - seg.file_offset)
        if avail <= 0:
            continue
        base = seg.file_offset
        pos = 0
        while pos < avail:
            end = min(pos + chunk_size, avail)
            window = data[base + pos:base + end]
            start = 0
            while True:
                found = window.find(pattern, start)
                if found < 0:
                    break
                seg_off = pos + found
                matches.append({
                    "vaddr": f"0x{seg.vaddr + seg_off:x}",
                    "segment": seg.index,
                    "p_flags": seg.flags_str,
                })
                if len(matches) >= max_matches:
                    capped = True
                    break
                start = found + 1
            if capped:
                break
            if end >= avail:
                break
            pos = end - overlap if overlap else end
        if capped:
            break

    return {
        "pattern_hex": pattern.hex(),
        "matches": matches,
        "match_count": len(matches),
        "capped": capped,
        "segments_scanned": segments_scanned,
        "truncated_segments": truncated_segments,
    }


def _parse_pattern(args: argparse.Namespace) -> bytes:
    if args.hex is not None:
        text = args.hex.strip().lower().replace("0x", "")
        if len(text) % 2 != 0:
            raise ValueError("--hex needs an even number of hex digits")
        if not 2 <= len(text) <= 64:
            raise ValueError("--hex must be 1..32 bytes")
        try:
            return bytes.fromhex(text)
        except ValueError as exc:
            raise ValueError(f"invalid --hex value: {exc}") from exc
    value = ev.parse_hex_u64(args.dword) if isinstance(args.dword, str) else args.dword
    if not 0 <= value <= 0xFFFFFFFF:
        raise ValueError("--dword must be in 0..0xFFFFFFFF")
    return int(value).to_bytes(4, "little")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan an ELF core for bytes")
    parser.add_argument("core")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--hex", help="byte pattern as hex (1..32 bytes)")
    group.add_argument("--dword", help="little-endian u32 value (0x-prefixed or decimal)")
    parser.add_argument("--max-matches", type=int, default=256)
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.dword is not None and args.dword.isdigit():
        args.dword = int(args.dword)

    try:
        pattern = _parse_pattern(args)
    except ValueError as exc:
        print(json.dumps({"error": "usage", "detail": str(exc)}))
        return ev.EXIT_USAGE

    try:
        data = Path(args.core).read_bytes()
    except OSError as exc:
        print(json.dumps({"error": "io", "detail": str(exc)}))
        return ev.EXIT_USAGE

    try:
        result = scan_core(data, pattern, max_matches=args.max_matches,
                           chunk_size=max(args.chunk_size, len(pattern)))
    except ev.ElfCoreError as exc:
        print(json.dumps({"error": "elf", "detail": str(exc)}))
        return ev.EXIT_USAGE

    print(json.dumps(result, indent=None if args.json else 2))
    return ev.EXIT_OK if result["match_count"] else ev.EXIT_TOOL_NEGATIVE


if __name__ == "__main__":
    sys.exit(main())
