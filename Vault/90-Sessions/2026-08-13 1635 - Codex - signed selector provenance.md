---
type: session
date: 2026-08-13
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/static
---

# Signed selector provenance

## Agent

Codex

## Goal

Execute offline roadmap packet M2.38: classify every native producer for the
20 exact selector words, intersect the producer lineage with the established
M1 record/positive-target route, and test exact signed value `-103`.

## Files inspected

- [[START HERE]], [[Current State]], [[Environment Status]], [[Project Charter]],
  and [[Project Roadmap]]
- [[EXP-20260813-051 - Generic resource-index producer census]] and
  [[EXP-20260813-052 - M2 dependency-gate disposition]]
- [[FUNC-97C95BA5572D-0044CA00]], [[FUNC-97C95BA5572D-0044D430]],
  [[FUNC-97C95BA5572D-0044BB70]], and the Ghidra baseline export
- The canonical-hash derived `bugs.exe` copy under `work/copies/`

## Changes made

- Added [[EXP-20260813-053 - Signed source-record selector provenance]] and
  its detailed static producer report.
- Added [[FUNC-97C95BA5572D-00467E60]] for the sole nonzero writer.
- Added `DEC-20260813-048` to [[Decision Log]].
- Completed M2.38 as a bounded negative and retired the signed-selector
  candidate without opening another family.
- Updated [[Current State]], [[Known Unknowns]], relevant function dossiers,
  MOCs, and the session index.

## Conclusions

- Four native paths only clear selector slots to zero.
- The selector array begins in the PE `.data` zero-fill tail.
- `0x00467E60` is the sole nonzero writer. Its 20-entry image table contains
  only positive selector values `1..14` excluding 12 and never `0xFF99`.
- Both writer call sites consume a fixed 64-record pool. The normal-update call
  occurs before M1 coordinator entry; no M1 record, relocated payload, or
  positive target produces the writer input or destination in that invocation.
- M2.38 is negative, `KU-023` remains unresolved, and the causal M2 gate stays
  unsatisfied.

## New hypotheses

None promoted. Persistent/copied fixed-pool state remains an explicit wider-
lifetime unknown, not evidence for an M1 selector edge.

## Contradictions discovered

No accepted evidence contradiction was found. The candidate's coordinator
proximity does not survive producer tracing: the only normal-update producer
call precedes the M1 coordinator and its table has no `-103` value.

## Tests run

- Verified the derived executable SHA-256 against the canonical hash.
- Enumerated structured references across the exact 20-record range.
- Rechecked every selector store, writer call, table read, and M1 call-order
  anchor with GNU `objdump` 2.44.
- Extracted the 20 image entries and exhaustively over-approximated both
  byte-derived table-index formulas for `0xFF99`.
- Ran Vault metadata/link, whitespace, diff, and Git hygiene checks at
  closeout.

## Unresolved questions

- `KU-023`: the exact M1 placement/positive-target-to-ID-zero resource
  selection edge.
- Persistent/copied state and arbitrary indirect aliases outside M2.38's
  bounded current-invocation producer surface.

## Recommended next action

No successor packet is selected by this negative. Record a separate scope
decision before opening another PC-native dependency candidate; do not resume
index/resource-family widening implicitly.

## Git commit if applicable

`research: retire M2 signed selector candidate`
