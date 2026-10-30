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

# M2 deferral hard-truth audit

## Agent

Codex

## Goal

Adversarially verify the prior conclusion that M2 should be deferred and M4.1
should become the sole active packet.

## Files inspected

- [[START HERE]], [[Current State]], [[Environment Status]], [[Project Charter]],
  [[Agent Operating Manual]], and [[Project Roadmap]]
- [[Decision Log]], [[Known Unknowns]], [[Reverse Engineering MOC]], and
  [[Implementation MOC]]
- Existing M2.34-M2.39 experiment notes and their cited static exports
- Native `bugs.exe` disassembly for `0x0041C420` and the ignored user-owned
  M4.1 work-copy files

## Experiments inspected

- `EXP-20260813-049` through `EXP-20260813-054`
- `EXP-20260812-033`

## Changes made

- Added [[EXP-20260813-055 - M2 deferral hard-truth audit]] and its static
  premise matrix.
- Marked `EXP-20260813-054` and the affected part of `DEC-20260813-049` as
  superseded rather than silently replacing their historical conclusions.
- Added `DEC-20260813-050`.
- Restored M2 to `Active`, selected exact offline packet M2.40, and returned
  M4/M4.1 to `Planned` while preserving M4.1's evidence-backed boundary.
- Updated [[Current State]], [[Known Unknowns]], relevant MOCs, the roadmap,
  and the session index.

## Conclusions

- The prior decision does not survive intact. M2's causal gate remains open,
  but deferral was premature.
- M2.36 had already preserved exact unresolved inputs
  `0x0059B730/0x0059B7B4`. They are first dwords of fixed-pool slots 2 and 3
  and directly select `0x005B18E0 + I * 4`; their producers were not censused.
- Initial pool zero is not evidence of reader-time zero or M1 provenance.
  M2.40 must decide both at a finite offline boundary.
- M4.1 remains a valid exact-hash user-owned-file packet, but that supports
  technical viability rather than exclusive priority.

## New hypotheses

None promoted. The fixed-pool words are exact candidate inputs, not claimed
M1-derived selectors or semantic fields.

## Contradictions discovered

M2.39 said that no successor had been ranked, which was true, but used that to
support the stronger conclusion that no finite candidate remained. M2.36's
own retained unknowns contradict that stronger premise.

## Tests run

- Recalculated fixed-pool slot arithmetic and independently checked native
  pool clear/stride instructions.
- Rehashed the exact executable and both M4.1 files in the ignored user-owned
  work copy, then checked Git-tracked paths for protected game-data
  extensions.
- `python scripts/vault-lint.py`.
- `PYTHONPATH=. .venv/bin/pytest -q tests`: 203 passed.
- `git diff --check`, staged protected-content review, and final Git hygiene.

## Unresolved questions

- Whether either exact word is zero at its reader.
- The complete bounded producer and source lineage for fixed-pool slots 2 and
  3.
- Whether either lineage derives from the established M1 record/payload route.

## Recommended next action

Execute M2.40 offline only. Classify the native direct and bounded fixed-pool
writers for `0x0059B730/0x0059B7B4`, decide reader-time zero reachability, and
intersect their sources with the M1 closure. Stop at an exact edge or precise
negative without widening the surface.

## Git commit if applicable

`research: correct premature M2 deferral`
