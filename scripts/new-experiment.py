#!/usr/bin/env python3
import argparse
from note_utils import VAULT, next_dated_id, now, require_unique, slug, write_new

parser = argparse.ArgumentParser(description="Create a non-overwriting experiment note.")
parser.add_argument("question")
parser.add_argument("--id")
parser.add_argument("--binary-sha256", default="")
parser.add_argument("--environment", default="unknown")
args = parser.parse_args()

stamp = now()
evidence_id = args.id or next_dated_id("EXP")
require_unique(evidence_id)
if not __import__("re").fullmatch(r"EXP-\d{8}-\d{3}", evidence_id):
    raise SystemExit("Experiment ID must match EXP-YYYYMMDD-NNN")

path = VAULT / "30-Experiments" / f"{evidence_id} - {slug(args.question)}.md"
content = f"""---
type: experiment
id: {evidence_id}
date: {stamp.date().isoformat()}
question: {args.question!r}
binary_sha256: {args.binary_sha256}
environment: {args.environment}
environment_version:
working_directory:
configuration:
artifacts: []
addresses: []
file_offsets: []
result: pending
created: {stamp.isoformat(timespec="seconds")}
updated: {stamp.isoformat(timespec="seconds")}
tags:
  - re/experiment
---

# {evidence_id}

## Question

{args.question}

## Procedure

## Expected

## Observed

## Interpretation

## Result

Pending.

## Follow-up
"""
print(write_new(path, content))
