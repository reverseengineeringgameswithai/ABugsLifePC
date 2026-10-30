#!/usr/bin/env python3
import argparse
from note_utils import VAULT, next_dated_id, now, require_unique, slug, write_new

parser = argparse.ArgumentParser(description="Create a non-overwriting hypothesis note.")
parser.add_argument("hypothesis")
parser.add_argument("--id")
args = parser.parse_args()

evidence_id = args.id or next_dated_id("HYP")
require_unique(evidence_id)
stamp = now().isoformat(timespec="seconds")
path = VAULT / "60-Hypotheses" / f"{evidence_id} - {slug(args.hypothesis)}.md"
content = f"""---
type: hypothesis
id: {evidence_id}
confidence: low
status: open
supporting_evidence: []
contradicting_evidence: []
created: {stamp}
updated: {stamp}
tags:
  - re/hypothesis
---

# {evidence_id}

## Hypothesis

{args.hypothesis}

## Confidence

Low.

## Supporting evidence

None.

## Contradicting evidence

None known.

## What would falsify it?

## Next experiment

## Status

Open.
"""
print(write_new(path, content))
