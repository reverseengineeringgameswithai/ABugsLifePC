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

# ID-zero stream-difference localization

## Agent

Codex

## Goal

Execute roadmap packet M2.24 under the START HERE workflow, localize the exact
accepted `FLICK.ALL`/`FLICKD.ALL` differences across only the 24 retained
ID-zero stream intervals, preserve conservative Obsidian evidence structure,
and leave Git clean.

## Files inspected

- The required START HERE sequence, Project Charter, Agent Operating Manual,
  roadmap/state/environment, decision and unknown registers, and relevant
  MOCs.
- Exact accepted files under the derived read-only work copy:
  `PC/BUGS/CD/CHARS/FLICK.ALL` and `PC/BUGS/CD/CHARS3/FLICKD.ALL`.
- Native GNU `objdump` disassembly of unchanged executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact prior M2.20, M2.21, and M2.23 evidence.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-033 - Character ALL replacement visible outcome]]
- [[EXP-20260812-034 - Character request and first consumer trace]]
- [[EXP-20260813-036 - Shared-entry render-lineage discriminator]]
- [[EXP-20260813-037 - ID-zero stream-difference localization]]

## Changes made

- Added a metadata-only static report containing every exact retained
  interval, record start, selector mode, terminal offset, and difference-
  offset signature without file payload byte values.
- Added `EXP-20260813-037` and updated the two directly relevant function
  dossiers.
- Completed M2.24, resolved KU-036 at the record-span boundary, added KU-037,
  and recorded `DEC-20260813-032`.
- Advanced M2 to approval-gated M2.25 without creating a parser, editor,
  renderer tool, semantic field name, runtime result, or cross-port claim.
- No runtime, debugger, breakpoint, execution control, target-state change, or
  parser was used.

## Conclusions

- **Confirmed:** the 24 retained stream intervals form exact file range
  `[0x0004,0x2AE8)` in both accepted files.
- **Confirmed:** entry 8 is unchanged; exact candidate entries
  `{0-7, 9-23}` contain 2,102 differing positions across 183 selected records.
- **Confirmed:** every one of those 2,102 differences lies in a record span
  reached identically by both in-bounds `0x0044F8E0` walks. No continuation or
  bound contradiction occurs.
- **Confirmed:** 13 descriptor-table differences outside the retained
  intervals reconcile the known 2,115 whole-file count.
- **Unknown:** which of the 23 candidates emits changed hardware output or
  accounts for the M2.20 repeated local visible region.

## New hypotheses

Comparing metadata digests of the `0x80`-stride records emitted per exact
entry may shrink the 23-entry source set without retaining game data. This is
a runtime provenance hypothesis, not an identity or field interpretation.

## Contradictions discovered

The exact offline result does not select one stream: nearly every retained
stream differs and is record-span reached. The full 23-entry ambiguity is
retained rather than collapsed from filename or visible appearance.

## Tests run

- Exact SHA-256 and size checks for both files: passed.
- Independent descriptor/cursor partition and bounded two-file walk: passed
  for all 24 retained intervals with no contradiction.
- Independent GNU `cmp -l` offset/count reconciliation: 2,115 total, 2,102
  retained, 13 outside.
- Native `objdump` checks for `0x00448010` cursor arithmetic and
  `0x0044F8E0` walk rules: passed.
- `git diff --check`: passed.
- `make check`: Vault lint 152 notes with zero errors/warnings, 130 tests
  passed, and tracked-file audit found zero violations.

## Unresolved questions

- Which candidate entries produce differing hardware-submission records in a
  matched Direct3D frame?
- Which changed emission, if any, accounts for the repeated local visible
  result?
- Does any later PC-native edge bind that emission to an M1 placement?

## Recommended next action

Prepare [[Project Roadmap#M2.25 — Per-entry hardware-submission delta capture]]
and obtain explicit approval before any breakpoint or execution-control
change. Limit the packet to exact candidates `{0-7, 9-23}`, the safe
`0x0044C898-0x0044C89E` boundary, and metadata-only pre/post submission
digests.

## Git commit if applicable

Bounded commit message: `research: localize ID-zero stream differences`.
