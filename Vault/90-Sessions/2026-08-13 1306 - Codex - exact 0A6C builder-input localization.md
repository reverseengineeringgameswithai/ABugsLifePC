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

# Exact 0A6C builder-input localization

## Agent

Codex

## Goal

Execute roadmap packet M2.30 under the START HERE workflow, remain offline
and PC-native, map exact record `0x0A6C`'s source differences through the
four-input Direct3D builder, preserve contradictions and conclusions in
Obsidian, and leave Git clean.

## Files inspected

- The required START HERE sequence, Project Charter, Agent Operating Manual,
  roadmap/state/environment, decision and unknown registers, and relevant
  MOCs.
- Exact native disassembly of `0x0044F8E0`, call site `0x0044F99D`, and
  `0x00405FE0` through its admission and four append-input construction paths.
- Only record `[0x0A6C,0x0A9C)` in M2.20's exact unchanged/replacement work
  copies, plus M2.29's retained evidence.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments

- [[EXP-20260813-042 - Per-record Direct3D append discriminator]]
- [[EXP-20260813-043 - Exact 0A6C builder-input localization]]

## Changes made

- Added a static address/offset report for the exact record comparison,
  caller argument construction, admission slice, and post-admission inputs.
- Added `EXP-20260813-043`, completed M2.30, resolved KU-042, recorded
  DEC-20260813-038, and made offline M2.31 the active packet.
- Updated the caller/builder and Direct3D batch dossiers, Current State,
  roadmap, session index, and relevant MOCs.
- Added no parser, editor, runtime instrumentation, source edit, or public
  tooling.

## Conclusions

- **Confirmed:** exact record `0x0A6C` has 12 differences in record-relative
  spans `+0x00..+0x02`, `+0x24..+0x26`, `+0x28..+0x2A`, and
  `+0x2C..+0x2E`.
- **Confirmed:** all 12 reach four separate byte-derived dwords at
  vertex-record `+0x10`, but only after successful count write
  `0x004069A1`.
- **Confirmed:** none distinguishes an admission predicate. The earlier path
  uses unchanged source spans, the same page index and caller mode in both
  files, and non-source per-frame state.
- **Unknown:** which non-source admission input first differed across M2.29's
  accepted arms and whether the conditional appended values contribute to a
  visible pixel.

## Contradiction

M2.29's exact `0/1/0` append receipt remains valid for its retained arms, but
the 12 source differences cannot cause that decision through the mapped
native path. They affect only values built after admission. The receipt is
therefore arm-local admission evidence, not a source-stable attribution.

## Tests run

- Exact executable and source-file SHA-256 verification.
- Exact restricted record comparison and native instruction-order/data-flow
  review.
- Full repository `make check`, Obsidian link checks, `git diff --check`,
  protected-path audit, and post-commit Git cleanliness check.

## Unresolved questions

- Which smallest non-source, per-frame input controls the first divergent
  `0x00405FE0` admission predicate?
- Can an existing safe data-watch boundary support a payload-free predicate
  receipt, or is a narrower tooling change required?
- Whether any of the four conditional outputs contributes to M2.20's visible
  result and what any source field means.

## Recommended next action

Execute [[Project Roadmap#M2.31 — Exact `0x0A6C` admission-state localization]]
offline. Backward-slice only the mapped no-append conditions to the smallest
non-source input/evaluation set and design a fail-closed metadata-only
first-divergent-predicate receipt. Do not begin live capture without fresh
explicit authority.

## Git commit if applicable

Bounded commit message: `research: localize exact 0A6C builder inputs`.
