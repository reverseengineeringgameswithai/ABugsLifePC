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

# Shared-entry render lineage

## Agent

Codex

## Goal

Execute roadmap packet M2.23 under the START HERE workflow, compare the exact
ID-zero retained-entry handoff with the M1 positive-target renderer lineage,
preserve conservative Obsidian evidence structure, and leave Git clean.

## Files inspected

- The required START HERE sequence, Project Charter, Agent Operating Manual,
  roadmap/state/environment, decision and unknown registers, and relevant
  MOCs.
- Exact structured Ghidra export and GNU `objdump` disassembly of unchanged
  executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact prior M2.20-22 and M1 positive-target evidence.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-009 - Training payload target structure and reuse census]]
- [[EXP-20260812-010 - Training target rebind visible substitution]]
- [[EXP-20260812-033 - Character ALL replacement visible outcome]]
- [[EXP-20260812-034 - Character request and first consumer trace]]
- [[EXP-20260813-035 - Character retained-range first-use bridge]]
- [[EXP-20260813-036 - Shared-entry render-lineage discriminator]]

## Changes made

- Added a reviewable static trace for both exact source lineages and their
  shared hardware output addresses.
- Added `EXP-20260813-036`, the address-based `0x0044F8E0` dossier, and a
  conservative candidate hardware-submission structure dossier.
- Completed M2.23, resolved KU-035 at the hardware-output boundary, added
  KU-036, and recorded `DEC-20260813-031`.
- Advanced M2 to an offline exact-two-file stream-difference localization
  packet without promoting a parser, editor, field meaning, or identity.
- No runtime, debugger, breakpoint, target-state change, or parser was used.

## Conclusions

- **Confirmed:** `0x0044F8EA` loads the retained entry's `+0x20` pointer and
  walks stream-relative records with exact `0x24`/`0x30` strides.
- **Confirmed:** `0x0045A7F0` instead derives a 12-byte table and command
  stream from the M1 positive-target argument. There is no direct source
  pointer copy, call, or address-forming edge between the two walks.
- **Confirmed:** Both hardware paths allocate from the same
  `*(0x0081BC28) + *(0x008082C8) * 0x80` arena, update the same counter, and
  link through the topology rooted via `0x004E8CC8` with common output link
  and flag offsets.
- **Unknown:** which retained stream produces the M2.20 visible difference and
  whether any upstream event binds it to an M1 placement.

## New hypotheses

The accepted character-file difference should be localizable to one or a
small number of exact retained `+0x20` stream intervals. This is a bounded
offline discriminator, not a field or asset interpretation.

## Contradictions discovered

Shared output structures do not imply that the two input pointers alias.
Likewise, separate source address walks do not imply separate renderer output
paths. Both facts are retained explicitly.

## Tests run

- Structured Ghidra data-reference/call-graph queries and native `objdump`
  address-flow checks against the exact executable: passed.
- `git diff --check`: passed.
- `make check`: dependency smoke imports, Vault lint, tests, and tracked-file
  audit passed.

## Unresolved questions

- Which exact retained `+0x20` stream intervals differ between the accepted
  unchanged and replacement files?
- Which changed bytes are reached by the demonstrated `0x0044F8E0` walk?
- Does a later PC-native edge bind one such stream to an M1 placement rather
  than only the shared hardware output arena?

## Recommended next action

Execute [[Project Roadmap#M2.24 — ID-zero stream-difference localization]].
Use only the two exact M2.20 files and the established 24 retained intervals;
do not create a general `.ALL` parser or assign semantic names.

## Git commit if applicable

Bounded commit message: `research: trace shared-entry render lineage`.
