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

# Character retained-range first-use bridge

## Agent

Codex

## Goal

Execute roadmap packet M2.22 under the START HERE workflow, identify the first
safe post-initialization PC use of the exact ID-zero header/retained range,
test one bounded bridge to an M1-supported Training record or positive target,
preserve Obsidian evidence structure, and leave Git clean.

## Files inspected

- The full required START HERE sequence, Project Charter, Agent Operating
  Manual, current roadmap/state/environment, decision and unknown registers,
  relevant MOCs, function dossiers, and M1/M2 experiment evidence.
- Exact structured Ghidra export and GNU `objdump` disassembly of unchanged
  executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- The retained M2.20 visible-outcome evidence and M2.21 request/range trace.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-009 - Training payload target structure and reuse census]]
- [[EXP-20260812-010 - Training target rebind visible substitution]]
- [[EXP-20260812-011 - Training record center candidates]]
- [[EXP-20260812-012 - Training record visibility bound]]
- [[EXP-20260812-033 - Character ALL replacement visible outcome]]
- [[EXP-20260812-034 - Character request and first consumer trace]]
- [[EXP-20260813-035 - Character retained-range first-use bridge]]

## Changes made

- Added a reviewable static trace classifying every `0x005B18E0` xref as
  initialization, generic runtime-indexed access, or direct ID-zero access.
- Added `EXP-20260813-035` and address-based dossiers for `0x00402DC0`,
  `0x00445FF0`, and `0x0044C440`; updated the affected M1 dossiers.
- Closed M2.22 with a normal-update direct-bridge negative, resolved KU-034 at
  that exact boundary, added KU-035, and recorded `DEC-20260813-030`.
- Added M2.23 as the one-pointer renderer-lineage discriminator and updated
  Current State, capability scope, and relevant MOCs.
- No runtime, debugger, breakpoint, target-state change, parser, or editor was
  used.

## Conclusions

- **Confirmed:** In one normal `0x0040FFC0` branch, `0x00402DC0` is the first
  proven unindexed post-initialization ID-zero reader. Its direct load at
  `0x004032F0` selects a header pointer and calls `0x00445FF0` with shared
  destination index zero.
- **Confirmed:** `0x00445FF0` writes dynamic values to entries rooted at
  `0x005A9660` with exact stride `0x50`.
- **Confirmed:** The nearest M1-coordinator-side direct range reader,
  `0x0044C440`, runs at `0x0044D4BC` before `0x0044D430` loads M1 record root
  `0x005BA7E0` at `0x0044D4FA` or enumerates 20-byte records. The established
  M1 record/payload path has no direct slot/range reference or first-use call
  edge. The direct bridge is therefore negative for this branch/order window.
- **Unknown:** persistent/copied state, alternate branches and later events,
  the exact contributing retained entry, `.ALL` fields, and resource identity.

## New hypotheses

The exact retained-entry pointer passed at `0x0044C898` may enter renderer data
lineage that can be compared with the M1 positive-target argument at
`0x00449E20`. This is an address-lineage hypothesis, not an identity or field
interpretation.

## Contradictions discovered

Several generic indexed readers run before `0x00402DC0`, but none has a
statically proven zero index from an M1 input. Treating their table-base xrefs
as exact ID-zero reads would contradict native indexed address formation.

Likewise, `0x0044C440` shares the M1 coordinator but executes before record
enumeration. Shared call context proves sequencing, not record dependence.

## Tests run

- Structured Ghidra xref/call-graph queries and native `objdump` address-flow
  checks against the exact executable: passed.
- `git diff --check`: passed.
- `make check`: dependency smoke imports, Vault lint (146 notes, zero errors
  or warnings), 130 tests, and tracked-file audit (zero violations) passed.

## Unresolved questions

- Does the exact retained-entry argument at `0x0044C898` converge with the M1
  positive-target renderer lineage?
- Which exact retained entry and fields contribute to the M2.20 rendered
  difference?
- Does another branch or later event establish a record-to-resource edge?

## Recommended next action

Execute [[Project Roadmap#M2.23 — Shared-entry render-lineage discriminator]].
Begin with static data flow from the exact `0x0044C898` entry argument into
`0x0044F8E0` entry `+0x20`; compare only with the positive-target argument at
`0x00449E20`. Obtain approval before any runtime/breakpoint change.

## Git commit if applicable

Bounded commit message: `research: trace character retained-range first use`.
