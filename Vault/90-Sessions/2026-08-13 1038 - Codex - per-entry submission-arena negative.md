---
type: session
date: 2026-08-13
agent: Codex
status: completed
tags:
  - session
  - re/dynamic
  - re/resources
  - re/rendering
  - implementation/tooling
---

# Per-entry submission-arena negative

## Agent

Codex

## Goal

Execute explicitly approved roadmap packet M2.25 under the START HERE
workflow, compare metadata-only per-entry output intervals for the exact M2.24
candidate set in matched Direct3D arms, preserve the evidence in Obsidian, and
leave Git clean.

## Files inspected

- The required START HERE sequence, Project Charter, Agent Operating Manual,
  roadmap/state/environment, decision and unknown registers, and relevant
  MOCs.
- Exact M2.20 control/replacement/control staging under `work/copies/`.
- Native disassembly and existing Ghidra exports for `0x0044C440`,
  `0x0044F8E0`, its caller boundary, and the conditional arena initializer.
- Prior M2.20 through M2.24 evidence and directly related function/structure
  dossiers.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-033 - Character ALL replacement visible outcome]]
- [[EXP-20260812-034 - Character request and first consumer trace]]
- [[EXP-20260813-035 - Character retained-range first-use bridge]]
- [[EXP-20260813-036 - Shared-entry render-lineage discriminator]]
- [[EXP-20260813-037 - ID-zero stream-difference localization]]
- [[EXP-20260813-038 - Per-entry submission-arena negative]]

## Changes made

- Extended the read-only GDB harness to version 1.2/result and watch-spec
  schema 3 with fail-closed ordered submission capture, one-MiB digest bounds,
  exact stop-PC filters, coherent inactive-arena handling, and no retained
  payload bytes.
- Added compiled synthetic regressions for paired digest capture and
  coherent-zero post capture, including cleanup/detach/survival checks.
- Retained one rejected execution-point arm and three accepted fresh matched
  Direct3D arms plus a curated comparison under `dynamic/wine/`.
- Added `EXP-20260813-038`, completed M2.25, resolved KU-037 negatively, added
  KU-038 and `DEC-20260813-033`, and advanced the roadmap to static-first M2.26.
- Downgraded the prior active “hardware submission” interpretation throughout
  current dossiers/MOCs while preserving the exact static convergence and the
  runtime contradiction.

## Conclusions

- **Confirmed:** all 23 candidate calls in each accepted arm return with
  coherent `(counter, capacity, base) = (0, 0, 0)`.
- **Confirmed:** every per-entry interval has zero records/bytes and
  SHA-256(empty); the exact changed-emission set in this arena is empty.
- **Confirmed:** all three arms pass Direct3D, exact load, `NextLife`, ordered
  capture, cleanup/detach, no-signal, and five-sample survival gates.
- **Confirmed:** execution breakpoint `0x0044C898` produces a structured
  same-PC `SIGSEGV` on this Wine/GDB setup and is not a safe continuation-
  evidence point.
- **Inferred:** the conditional arena is not the active route carrying
  M2.20's replacement-local visible result. Its renderer ownership remains
  unknown.

## New hypotheses

The selected Direct3D path uses a different initialized consumer/output route,
or `0x0044F8E0` carries relevant state through a non-arena edge. M2.26 must
discriminate these statically before any new live instrumentation.

## Contradictions discovered

M2.23's conditional static convergence remains exact, but its former active-
hardware interpretation is contradicted by three independent all-zero
Direct3D arms. The contradiction is retained explicitly rather than resolved
by semantic naming.

## Tests run

- Focused schema/harness suite: 73 passed.
- Fresh matched Direct3D capture: three accepted arms; one unsafe preflight
  rejected with verified cleanup/detach/survival.
- `git diff --check`: passed.
- `make check`: Vault lint 154 notes with zero errors/warnings, 144 tests
  passed, and tracked-file audit found zero violations.

## Unresolved questions

- Which exact initialization path owns the inactive conditional arena?
- Which renderer consumer is active under the proven Direct3D selector?
- Which nearest alternate PC-native edge can carry the changed retained-entry
  streams to M2.20's visible result?

## Recommended next action

Execute [[Project Roadmap#M2.26 — Direct3D renderer-path reconciliation]] as a
static-first PC-native trace. Do not reuse execution breakpoint `0x0044C898`,
assign renderer/primitive/asset semantics, parse `.ALL`, or consult PS1.

## Git commit if applicable

Bounded commit message: `research: record inactive submission arena`.
