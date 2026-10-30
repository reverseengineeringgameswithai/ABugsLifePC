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

# Direct3D renderer-path reconciliation

## Agent

Codex

## Goal

Execute roadmap packet M2.26 under the START HERE workflow, reconcile the
proven Direct3D selector with the inactive conditional arena, identify the
nearest active retained-entry consumer, preserve the evidence in Obsidian,
and leave Git clean.

## Files inspected

- The required START HERE sequence, Project Charter, Agent Operating Manual,
  roadmap/state/environment, decision and unknown registers, and relevant
  MOCs.
- Native disassembly and the checked Ghidra export for `0x0041F990`, the
  main/restart renderer dispatches, `0x004119E0`, `0x0049C520`,
  `0x0049C3F0`, `0x0044F8E0`, `0x0045A7F0`, and the nearest Direct3D
  batching/flush functions.
- Prior M2.20 through M2.25 evidence and directly related function/structure
  dossiers.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-007 - Gamescope hardware presentation baseline]]
- [[EXP-20260812-033 - Character ALL replacement visible outcome]]
- [[EXP-20260813-036 - Shared-entry render-lineage discriminator]]
- [[EXP-20260813-038 - Per-entry submission-arena negative]]
- [[EXP-20260813-039 - Direct3D renderer-path reconciliation]]

## Changes made

- Added a PC-native static trace and `EXP-20260813-039`.
- Classified selector 1 as native software and selector 2 as Direct3D from
  exact native arithmetic, diagnostics, and dispatch calls.
- Reclassified the conditional `0x80`-stride structure as software-renderer
  output and documented its exact initializer.
- Added function dossiers for the selected Direct3D initializer, software
  initializer/window helper, and two nearest Direct3D batch builders.
- Corrected relevant historical notes, dossiers, MOCs, current state,
  decision/unknown registers, and roadmap without erasing the earlier
  contradiction.

## Conclusions

- **Confirmed:** `0x0049C520` is the selector-1 software renderer initializer
  and is the only proven writer of the arena capacity/base/counter setup.
- **Confirmed:** `0x0049C3F0` is a selector-1 software-window helper and does
  not initialize the arena.
- **Confirmed:** selector 2 calls `0x004119E0`, whose exact diagnostic starts
  the Direct3D renderer.
- **Confirmed:** selector-2 `0x0044F8E0` calls
  `0x00405FE0/0x00407450`; their batches can flush through
  `0x004056A0/0x004058D0` to the Direct3D device
  `DrawIndexedPrimitive` vtable slot.
- **Inferred:** this separate Direct3D batch route is capable of carrying the
  M2.20 retained-file difference, but exact contributing entries and records
  remain unknown.

## Contradictions discovered

No new unresolved contradiction remains in M2.26. M2.23's structural
convergence was correct but its hardware label was unsupported; M2.25's
all-zero result preserved that mismatch. Exact selector/initializer evidence
now identifies the arena as software-only and the active Direct3D path as
separate batching storage.

## Tests run

- Exact executable SHA-256 verification.
- Native disassembly/Ghidra cross-check of selector, thunk, writer, batch, and
  Direct3D vtable-call edges.
- `git diff --check` and full repository `make check` before commit.

## Unresolved questions

- Which members of exact candidate set `{0-7, 9-23}` alter Direct3D batch
  metadata or invoke a flush in the matched replacement arm?
- Which record and input bytes cause the bounded M2.20 visible result?
- Meanings of the Direct3D batch families and `.ALL` fields.

## Recommended next action

Execute [[Project Roadmap#M2.27 — Direct3D retained-entry batch provenance]]
only after designing exact metadata and flush/reset bounds. Any runtime points
or execution control require fresh explicit approval. Do not reuse execution
breakpoint `0x0044C898`, retain protected batch payloads, assign semantic
field/asset/primitive names, begin general `.ALL` tooling, or consult PS1.

## Git commit if applicable

Bounded commit message: `research: reconcile Direct3D renderer path`.
