#!/usr/bin/env python3
import argparse
from note_utils import VAULT, next_dated_id, now, require_unique, slug, write_new

parser = argparse.ArgumentParser(description="Create a non-overwriting ADR note.")
parser.add_argument("decision")
parser.add_argument("--id")
args = parser.parse_args()

evidence_id = args.id or next_dated_id("DEC")
require_unique(evidence_id)
stamp = now().isoformat(timespec="seconds")
path = VAULT / "50-Decisions" / f"{evidence_id} - {slug(args.decision)}.md"
content = f"""---
type: decision
id: {evidence_id}
status: proposed
created: {stamp}
updated: {stamp}
tags:
  - decision
---

# {evidence_id} - {args.decision}

## Context

## Decision

{args.decision}

## Alternatives

## Reasoning

## Consequences

## Revisit when
"""
print(write_new(path, content))
