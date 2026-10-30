---
type: session
date: 2026-08-13
agent: Codex
status: completed
tags:
  - session
  - re/static
  - re/dynamic
  - re/resources
  - re/rendering
---

# Per-record Direct3D append discriminator

## Agent

Codex

## Goal

Execute roadmap packet M2.29 under the START HERE workflow, statically prove
exact append/no-append boundaries, use the user's fresh authority for a
payload-free per-record Direct3D discriminator if safe, preserve contradictions
and conclusions in Obsidian, and leave Git clean.

## Files inspected

- The required START HERE sequence, Project Charter, Agent Operating Manual,
  roadmap/state/environment, decision and unknown registers, and relevant
  MOCs.
- Exact native disassembly and checked Ghidra exports for `0x00405FE0`,
  `0x00407450`, their selected counter writes, index increments, admission
  branches, returns, and reachable flush/reset paths.
- M2.20's exact unchanged/replacement files and M2.27–M2.28 evidence.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments

- [[EXP-20260813-040 - Direct3D retained-entry batch provenance]]
- [[EXP-20260813-041 - Changed-record form localization]]
- [[EXP-20260813-042 - Per-record Direct3D append discriminator]]

## Changes made

- Added the complete static counter-write, no-append-return, and reset
  preflight for both selected Direct3D builders.
- Extended the compatible read-only GDB harness to 1.4.0/watch-result schema 5
  with an exact 168-call record plan and count-only candidate outcomes. It
  reads or retains no source, vertex, or index payload.
- Added schema validation and synthetic append/flushed-no-append regressions.
- Retained three accepted fresh control/replacement/control receipts and one
  rejected early-attachment timing receipt.
- Updated builder dossiers, runtime tooling/environment notes, roadmap/current
  state, decision/unknown registers, this session, and relevant MOCs.

## Conclusions

- **Confirmed:** the only selected vertex-count writes are `0x004069A1` (+4)
  and `0x00407B00` (+3); all mapped earlier exits return without a selected
  counter change.
- **Confirmed:** all three accepted arms audit the exact ordered 168-call plan,
  retain 124 candidate outcomes, use only root `0x004C4108`/page 16 for
  positive candidates, record no selected flush, and pass all hardware,
  cleanup, signal, and survival gates.
- **Confirmed:** entry 7/file offset `0x0A6C`/form `0x3C` is the only fresh
  outcome outside both controls: no append / four vertices and six indices /
  no append (`0/1/0`).
- **Unknown:** which exact source byte or caller-built input makes that record
  pass only in the replacement, and whether it contributes to a visible pixel.

## Contradictions and rejected runs

The controls disagree on 13 records, so none is selected. The three M2.28
single-record outcomes at `0x0174`, `0x0858`, and `0x0AA4` do not reproduce in
the fresh arms; they remain exact for their old retained arms but are not
source-stable across launches. Rejected `RUN-GDB-20260813-123859` attached
before the natural title, stopped on 1,000 unmatched flush markers, and failed
closed at `max_stops`; it contributes no candidate evidence.

## Tests run

- Exact executable, control, and replacement SHA-256 verification.
- Native disassembly/Ghidra cross-check of counter writes, index increments,
  admission exits, and reset ordering.
- Focused evidence-library and compiled GDB-harness regressions.
- Full repository `make check` and `git diff --check` before commit.
- Post-runtime process, audio-sink, Wine-drive, originals, and Git cleanliness
  audits.

## Unresolved questions

- Which differing bytes in `[0x0A6C,0x0A9C)` reach builder arguments or
  admission predicates?
- Which alternatives remain indistinguishable through native data flow?
- Whether the append contributes to M2.20's visible result and what any source
  fields mean.

## Recommended next action

Execute [[Project Roadmap#M2.30 — Exact `0x0A6C` builder-input localization]]
offline. Map only exact differing bytes in `[0x0A6C,0x0A9C)` through
`0x0044F8E0` argument construction into `0x00405FE0`. Do not assign semantics,
inspect another record or family, create general `.ALL` tooling, consult PS1,
or begin another live arm without a new exact question and fresh authority.

## Git commit if applicable

Bounded commit message: `research: discriminate per-record Direct3D appends`.
