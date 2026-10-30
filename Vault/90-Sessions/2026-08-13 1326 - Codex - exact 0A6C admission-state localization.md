---
type: session
date: 2026-08-13
agent: Codex
status: completed
tags:
  - session
  - re/static
  - re/resources
  - re/rendering
---

# Exact 0A6C admission-state localization

## Agent

Codex

## Goal

Execute roadmap packet M2.31 under the START HERE workflow, remain offline
and PC-native, reduce exact record `0x0A6C`'s non-source admission state and
ordered rejection chain, design a metadata-only discriminator, preserve the
result in Obsidian, and leave Git clean.

## Files inspected

- The required START HERE sequence, Agent Operating Manual, Project Charter,
  current state/environment, roadmap, decision and unknown registers, and
  relevant MOCs.
- Exact native disassembly of caller `0x0044F8E0` through call
  `0x0044F99D`, and builder `0x00405FE0` through final admission rejection
  `0x004066BD`.
- The Ghidra data references and decompiler export for `0x00405FE0`, M2.29's
  retained metadata, and the M2.30 exact-source data-flow report.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments

- [[EXP-20260813-043 - Exact 0A6C builder-input localization]]
- [[EXP-20260813-044 - Exact 0A6C admission-state localization]]

## Changes made

- Added a static report with the exact input lattice, native arithmetic,
  ordered predicate chain, and payload-free receipt schema.
- Added `EXP-20260813-044`, completed M2.31, resolved KU-043, opened KU-044,
  recorded DEC-20260813-039, and made offline-first M2.32 active.
- Updated Current State, roadmap, the caller/builder and Direct3D batch
  dossiers, relevant MOCs, and the session index.
- Added no runtime instrumentation, source edit, parser, editor, payload, or
  public tooling.

## Conclusions

- **Confirmed:** the physical non-source union contains 23 locations; at
  most 22 are read in one native path because the two policy thresholds are
  mutually exclusive.
- **Confirmed:** exact source-derived mode 2 reduces admission to 12 ordered
  logical rejection slots and 13 concrete reject PCs.
- **Confirmed:** existing selector-read pre-call and entry-post/count data-
  watch boundaries are sufficient for a future first-reject receipt. No new
  execution point, watch slot, full predicate vector, or raw retained values
  are required.
- **Unknown:** whether the exact arithmetic evaluator will match actual count
  outcomes and which first-reject PC, if any, is stable across fresh controls.

## Contradiction

No new contradiction was introduced. M2.29's `0/1/0` outcome still cannot
select an admission predicate because those arms retained only append
metadata. A future receipt must preserve any control disagreement, state-
digest change, or prediction/count mismatch rather than infer causality.

## Tests run

- Authoritative executable SHA-256 verification.
- Independent native-disassembly and Ghidra data-reference review.
- Full repository `make check`, Obsidian link checks, `git diff --check`,
  protected-path audit, and post-commit Git cleanliness check.

## Unresolved questions

- Can a native signed-wrap/truncation evaluator reproduce every synthetic
  rejection and the observed exact-record counter result?
- In fresh separately authorized controls, is the first-reject PC stable?
- Whether any conditional append contributes to M2.20's visible result and
  what any source or state value means.

## Recommended next action

Execute [[Project Roadmap#M2.32 — Exact `0x0A6C` admission-predicate receipt]]
offline first. Implement and fixture-test only the purpose-specific native
evaluator and payload-free schema. Do not begin live capture without fresh
explicit authority.

## Git commit if applicable

Bounded commit message: `research: localize exact 0A6C admission state`.
