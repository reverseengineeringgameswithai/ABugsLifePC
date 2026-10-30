---
type: session
date: 2026-08-13
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/rendering
---

# Positive-target selector-2 provenance

## Agent

Codex

## Goal

Execute offline roadmap packet M2.35: classify every selector-2 Direct3D
builder-facing input in exact M1 positive-target consumer `0x0045A7F0` and
test for provenance from the selected ID-zero `CHARS/FLICK.ALL` state.

## Files inspected

- [[START HERE]], [[Agent Operating Manual]], [[Current State]],
  [[Environment Status]], [[Project Charter]], [[Project Roadmap]],
  [[Decision Log]], and [[Known Unknowns]]
- [[Reverse Engineering MOC]], [[Functions MOC]], and
  [[FUNC-97C95BA5572D-0045A7F0]]
- Existing structured export and M2.23/M2.26 static traces under
  `static/exports/BIN-97c95ba5572dce63/`
- Exact derived work-copy `bugs.exe`, verified at the canonical SHA-256

## Experiments inspected

- [[EXP-20260812-034 - Character request and first consumer trace]]
- [[EXP-20260813-035 - Character retained-range first-use bridge]]
- [[EXP-20260813-036 - Shared-entry render-lineage discriminator]]
- [[EXP-20260813-039 - Direct3D renderer-path reconciliation]]
- [[EXP-20260813-049 - M2 exit-gate reconciliation]]

## Changes made

- Added [[EXP-20260813-050 - M1 positive-target selector-2 input provenance]].
- Added the reviewable native/structured trace
  `static/exports/BIN-97c95ba5572dce63/M2-positive-target-selector2-input-provenance.md`.
- Updated [[FUNC-97C95BA5572D-0045A7F0]], [[Current State]],
  [[Known Unknowns]], [[Decision Log]], and the relevant MOCs.
- Completed M2.35 with a negative and made offline M2.36 the exact next packet.
- Corrected the stale [[Functions MOC]] note that said M2.32 had not measured
  a live first reject; `EXP-20260813-046/048` already supplied live receipts.

## Conclusions

- Both `0x0045A7F0` selector checks enter Direct3D only for value 2.
- Ten inline allocation arms use roots `0x004C4108/0x004C410C` and flushers
  `0x004056A0/0x004058D0`; `0x00405FE0/0x00407450` are not called here.
- Every reviewed page/list, root, flush, index, vertex-base, and emitted-record
  input derives from the M1 target/command stream, exact M1 caller inputs,
  renderer globals, local derived scratch, or existing batch state.
- No input derives from ID-zero header `0x005B18E0`, retained range
  `[0x005A9660,0x005A9DE0)`, or exact selected-resource state. `KU-023` and M2
  remain open.

## New hypotheses

If an M1-derived ID-zero selection edge exists, the finite generic indexed
reader set from `EXP-20260813-035` is now a narrower candidate surface than
the exhausted positive-target renderer.

## Contradictions discovered

No evidence contradiction was found. Nearby scratch `0x005B1ED0` was
explicitly distinguished from header `0x005B18E0`. One documentation-drift
sentence in [[Functions MOC]] was corrected against existing live evidence.

## Tests run

- Exact `bugs.exe` SHA-256 verification.
- Structured xref count for `FUN_0045a7f0`: zero references to
  `0x005B18E0`, zero references into `[0x005A9660,0x005A9DE0)`.
- Native selector, caller-input, call-set, thunk, allocation-arm, and batch-
  input review with GNU `objdump`.
- Repository checks and Git audit recorded at closeout.

## Unresolved questions

- `KU-023`: which, if any, M1 record/payload-derived runtime index selects the
  ID-zero resource path?
- Whole-program copied-state and wider-lifetime links remain unknown.

## Recommended next action

Execute only offline M2.36. For the eight generic readers named in
[[Project Roadmap#M2.36 — Generic resource-index producer census]], resolve
their thunk callers and native index expressions, then test for M1 record/
payload-derived ID-zero provenance on the normal coordinator route.

## Git commit if applicable

Bounded commit message: `research: trace M1 selector-2 provenance`.
