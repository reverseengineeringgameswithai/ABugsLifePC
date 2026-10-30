#!/usr/bin/env python3
import argparse
import re
from note_utils import VAULT, now, require_unique, write_new

parser = argparse.ArgumentParser(description="Create a non-overwriting function dossier.")
parser.add_argument("address", help="virtual address, for example 0x00418A20")
parser.add_argument("--binary-sha256", default="")
parser.add_argument("--id")
parser.add_argument("--name", default="")
args = parser.parse_args()

address = args.address.upper().replace("0X", "")
if not re.fullmatch(r"[0-9A-F]+", address):
    raise SystemExit("Address must be hexadecimal")
binary_prefix = args.binary_sha256[:12].upper() if args.binary_sha256 else "UNKNOWN"
evidence_id = args.id or f"FUNC-{binary_prefix}-{address}"
require_unique(evidence_id)
stamp = now().isoformat(timespec="seconds")
path = VAULT / "20-Research" / "Functions" / f"{evidence_id}.md"
content = f"""---
type: function
id: {evidence_id}
binary_sha256: {args.binary_sha256}
address: 0x{address}
proposed_name: {args.name}
status: unknown
confidence: low
subsystem:
evidence: []
related: []
created: {stamp}
updated: {stamp}
tags:
  - re/function
---

# Function 0x{address}

## Summary

## Confirmed

## Inferred

## Unknown

Function semantics are unknown.

## Callers

## Callees

## Relevant strings

## Relevant imports

## Structure accesses

## Dynamic evidence

## Related experiments

## Next discriminating experiment
"""
print(write_new(path, content))
