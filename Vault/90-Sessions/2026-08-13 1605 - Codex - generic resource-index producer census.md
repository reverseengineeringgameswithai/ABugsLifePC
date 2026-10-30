---
type: session
date: 2026-08-13
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/level-data
---

# Generic resource-index producer census

## Agent

Codex

## Goal

Execute offline roadmap packet M2.36: classify the native index producers and
thunk callers for the eight retained generic `0x005B18E0` header readers, then
test for an M1 record/payload-derived resource-ID-zero edge on the normal
coordinator route.

## Files inspected

- [[START HERE]], [[Agent Operating Manual]], [[Current State]],
  [[Environment Status]], [[Project Charter]], [[Project Roadmap]],
  [[Decision Log]], and [[Known Unknowns]]
- [[Reverse Engineering MOC]], [[Functions MOC]], and [[Experiments MOC]]
- Existing Ghidra structured evidence and the exact derived work-copy
  `bugs.exe`, verified at the canonical SHA-256

## Experiments inspected

- [[EXP-20260813-035 - Character retained-range first-use bridge]]
- [[EXP-20260813-049 - M2 exit-gate reconciliation]]
- [[EXP-20260813-050 - M1 positive-target selector-2 input provenance]]

## Changes made

- Added [[EXP-20260813-051 - Generic resource-index producer census]].
- Added the reviewable native/structured census at
  `static/exports/BIN-97c95ba5572dce63/M2-generic-resource-index-producer-census.md`.
- Added [[FUNC-97C95BA5572D-00448350]] and updated
  [[FUNC-97C95BA5572D-0044D430]].
- Updated [[Current State]], [[Known Unknowns]], [[Decision Log]],
  [[Project Roadmap]], and the relevant MOCs.
- Completed M2.36 with a finite negative and made offline M2.37 the exact next
  packet.

## Conclusions

- Six generic readers are only possibly reachable in pre-coordinator update
  `0x004144C0`; resource-initialization reader `0x00444EF0` receives exact
  index 11.
- `0x00448350` is the sole generic-reader candidate in the M1 coordinator
  closure, but its call at `0x0044D4E6` precedes M1 root load `0x0044D4FA`
  and record enumeration.
- Neither selected-record dispatcher `0x004498F0` nor positive-target consumer
  `0x0045A7F0` can reach any of the eight readers.
- No current-invocation M1 record/payload-derived generic index proves resource
  ID zero. Persistent/copied cross-frame state remains unknown.

## New hypotheses

The written M2 dependency gate may be category-mismatched with the selected
ID-zero character resource. This remains a scope question for M2.37, not a
factual conclusion from the negative census.

## Contradictions discovered

No evidence contradiction was found. Shared `0x0044D430` membership initially
makes `0x00448350` look adjacent to the record route, but exact order places it
before the root load and walk; that adjacency is not a selection edge.

## Tests run

- Exact `bugs.exe` SHA-256 verification.
- Structured eight-reader xref, thunk/caller, and normalized reachability
  census.
- Native whole-image call/tail-jump scan and exact index/order review with GNU
  `objdump`.
- Repository checks and Git audit recorded at closeout.

## Unresolved questions

- `KU-023`: whether the M2 dependency gate should be revised or retained on a
  different finite PC-native candidate.
- Persistent/copied cross-frame index provenance and indirect function-pointer
  paths remain outside the completed current-invocation census.

## Recommended next action

Execute only [[Project Roadmap#M2.37 — M2 dependency-gate disposition]].
Reconcile the literal gate against `EXP-20260813-049/050/051`; either justify
an explicit evidence-preserving revision/closure or name one new bounded PC-
native candidate before any further analysis.

## Git commit if applicable

Bounded commit message: `research: classify generic resource indices`.
