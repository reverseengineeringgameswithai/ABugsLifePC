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

# Direct3D retained-entry batch provenance

## Agent

Codex

## Goal

Execute roadmap packet M2.27 under the START HERE workflow, prove that every
accepted renderer-facing arm uses hardware Direct3D rather than software,
bound selected batch flush/reset behavior, compare exact retained-entry
metadata, preserve the result in Obsidian, and leave Git clean.

## Files inspected

- The required START HERE sequence, Project Charter, Agent Operating Manual,
  roadmap/state/environment, decision and unknown registers, and relevant
  MOCs.
- Exact native disassembly and checked Ghidra exports for `0x0044F8E0`,
  `0x00405FE0`, `0x00407450`, `0x004056A0`, `0x004058D0`, their roots,
  counters, append sites, marker writes, and reset edges.
- M2.20 staging plus M2.24–M2.26 static/runtime evidence.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments

- [[EXP-20260813-037 - ID-zero stream-difference localization]]
- [[EXP-20260813-038 - Per-entry submission-arena negative]]
- [[EXP-20260813-039 - Direct3D renderer-path reconciliation]]
- [[EXP-20260813-040 - Direct3D retained-entry batch provenance]]

## Changes made

- Strengthened [[START HERE]] so every future renderer-facing arm must prove
  four exact positive hardware Direct3D markers and reject any
  `INITSOFTRENDER` or missing-marker arm.
- Added a static two-family layout/flush-reset preflight and
  [[STRUCT-PC-DIRECT3D-BATCH-FAMILIES]].
- Extended the read-only GDB harness to 1.3.0/watch-result schema 4 with exact
  caller/root/page/order/count bounds, pre-reset segment capture, and
  metadata-only hashes.
- Added synthetic controller/schema regressions and retained all bounded calibration
  and accepted run receipts.
- Updated function dossiers, tooling/environment notes, roadmap/current state,
  decision/unknown registers, and relevant MOCs.

## Conclusions

- **Confirmed:** both selected Direct3D families have 32 bounded pages; exact
  roots are `0x004F1730` via `0x004C4108` and `0x00511510` via
  `0x004C410C`.
- **Confirmed:** `0x00405FE0` adds four vertices/six indices and
  `0x00407450` adds three/three; marker stops precede every reachable in-call
  reset.
- **Confirmed:** all three accepted arms positively prove hardware Direct3D
  and reject software rendering.
- **Confirmed:** selected retained-entry additions use root `0x004C4108`,
  page 16, and no selected entry flushes in-call.
- **Confirmed:** replacement counts outside both controls reduce the 23-entry
  set to `{1,2,4,5,6,7,9,10,14,15,18,19,20}`.
- **Inferred:** this 13-entry set is the strongest current provenance set for
  the bounded M2.20 visible result; counts alone do not prove individual
  record/byte causality.

## Contradictions and rejected runs

Bounded calibration runs corrected an overwritten argument-slot assumption,
nullable inactive pages, the second exact root, entry-8 no-pre behavior,
unrelated callers, and stop limits. Each cleaned up, detached, received no
target signal, and passed survival, but none is candidate evidence. Control
hashes vary in transformed batch data, so hashes remain audit metadata and do
not enlarge the count-based set.

## Tests run

- Exact executable and staged-file SHA-256 verification.
- Native disassembly/Ghidra cross-check of roots, counters, append equations,
  flush markers, reset order, and caller receipts.
- Focused evidence-library and compiled GDB-harness regressions.
- Full repository `make check` and `git diff --check` before commit.
- Post-runtime process, audio-sink, Wine-drive, originals, and Git cleanliness
  audits.

## Unresolved questions

- Which exact changed record offsets/forms inside the 13 candidates account
  for each measured four-input/three-input builder-count delta?
- Which source bytes contribute to the bounded visible result?
- Meanings of the record forms, batch families, and `.ALL` fields.

## Recommended next action

Execute [[Project Roadmap#M2.28 — Changed-record form localization]] offline.
Use only the proven `0x24/0x30` walks and native builder-call conditions inside
the exact 13 candidates. Do not assign semantics, create a general `.ALL`
parser, inspect another family, consult PS1, or begin another live arm without
a fresh exact question and authority.

## Git commit if applicable

Bounded commit message: `research: localize Direct3D batch provenance`.
