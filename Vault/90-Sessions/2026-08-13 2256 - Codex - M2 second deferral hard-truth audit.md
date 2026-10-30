---
type: session
date: 2026-08-13
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/milestone-audit
---

# M2 second deferral hard-truth audit

## Agent

Codex

## Goal

Adversarially test whether the post-M2.40 evidence actually supports deferring
M2 and activating M4.1.

## Files inspected

- [[START HERE]], [[Current State]], [[Environment Status]], [[Project Charter]],
  [[Agent Operating Manual]], and [[Project Roadmap]]
- [[Decision Log]], [[Known Unknowns]], and [[Reverse Engineering MOC]]
- `EXP-20260813-049` through `EXP-20260813-056`
- The eight-reader, first hard-truth, and M2.40 static reports
- The exact-hash work-copy executable through read-only native disassembly

## Changes made

- Added [[EXP-20260813-057 - M2 second deferral hard-truth audit]] and its
  static evidence report.
- Added the missing structural classification of `0x0059C30C`: it is a
  distinct object at fixed-pool slot 25, not an outside-pool surface.
- Recorded residual exact slot-25 and slot-63 generic-header reader surfaces.
- Restored M2 as active on bounded offline M2.41 and returned M4.1 to planned.
- Updated the roadmap, current state, `KU-023`, decision log, MOCs, and session
  index.

## Conclusions

- M2.40 remains complete and negative at slots 2/3.
- The subsequent deferral is premature because slot 63 was explicitly retained
  and excluded, while slot 25 remained structurally unclassified.
- Both residual first dwords feed exact generic header-index readers and can be
  investigated in one finite offline packet.
- No M1-derived edge, reader-time zero, or field semantic is claimed by this
  audit.

## New hypotheses

Conditional late zero may remain visible at the slot-25 reader because its
`+0x5C` gate survives M2.40's removal store. M2.41 must decide this rather than
assuming it.

## Contradictions discovered

The first hard-truth report's “separate object” label is compatible with a
distinct record but cannot justify leaving `0x0059C30C` outside the finite
pool. Exact arithmetic supplies the missing slot-25 classification without
rewriting M2.40's valid slot-2/slot-3 result.

## Tests run

- Exact executable SHA-256 recheck.
- Independent fixed-pool arithmetic.
- Native disassembly of the slot-25/slot-63 readers, dispatcher, and direct
  call sites.
- `python scripts/vault-lint.py`.
- `PYTHONPATH=. .venv/bin/pytest -q tests`.
- `python scripts/audit-tracked-files.py`.
- `git diff --check`, staged review, and final clean-tree check.

## Unresolved questions

- Whether either residual word can be zero at its exact reader.
- Whether any value or enabling predicate intersects the established M1
  record/payload/positive-target route.

## Recommended next action

Execute exact offline M2.41 only. Do not widen to other fixed-pool objects or
generic readers.

## Git commit if applicable

`research: reject second premature M2 deferral`
