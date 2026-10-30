---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/dynamic
  - re/rendering
  - re/file-format
  - implementation/modding
---

# Level 01 cross-file validation

## Agent

Codex

## Goal

Execute roadmap M1.4 against one log-identified non-Training PC scene using
the hardware renderer, exact-hash manifests, byte-local receipts, and matched
native captures.

## Files and evidence inspected

- Required system notes, charter, roadmap, decisions, unknowns, and relevant
  MOCs
- Exact-hash `bugs.exe`, Level 01 DAT, prior parser/corpus report, manifests,
  and `EXP-20260812-009` through `EXP-20260812-012`
- Hardware-gated logs, receipts, and native Gamescope captures under ignored
  work storage

No file under `originals/` was modified. No PS1 source was consulted.

## Changes made

- Bound the `ant hill` menu selection to the logged exact Level 01 DAT.
- Screened the file's nine positive dispatch-`0x49` references at the start
  camera and retained record 261 for the reproducible experiment.
- Added hash-locked record-261 center and guarded target-rebind manifests.
- Recorded three accepted hardware runs and `EXP-20260812-013`.
- Reconciled the no-visible-change Level 01 result with the visible Training
  result and advanced the roadmap to M1.5.
- Recorded the user's external hardware-mode still showing a smoother stem as
  an unresolved Wine/driver/capture fidelity question; no visual-equivalence
  claim was promoted.

## Conclusions

- **Confirmed:** `ant hill` loads `CD/LEVEL01/LEVEL.DAT`, SHA-256
  `786b7a96…f08b53`.
- **Confirmed:** record 261 center and `0x3703C -> 0x3459C` target edits are
  byte-local and accepted under 640×480×16 Direct3D.
- **Confirmed:** unchanged, center, and rebind frame 03 are byte-identical;
  neither edit is visible at the Level 01 start camera.
- **Inferred:** the file's nine matching records are outside selection or
  visually inactive at that camera. Later in-level behavior remains unknown.
- **Unknown:** whether the brown/green stippling on large stems is a WineD3D
  legacy-format difference, native driver behavior, or capture/resampling.

## Contradictions and negative results

- No eligible Level 01 record produced Training-like visible substitution at
  the start camera.
- Several input/capture attempts were rejected because focus remained on the
  research window, timing did not phase-match, or the run entered the default
  software renderer. Retained conclusions use only hardware-gated logs.

## Tests run

- Exact manifest staging and receipt verification for record 261.
- `cmp -l`: center changes only `0x2968–0x2969`; rebind changes only
  `0x4E1C–0x4E1D`.
- Three retained runs pass both Direct3D markers, omit `INITSOFTRENDER`, load
  Level 01, complete `InitMainGame`, and enter `NextLife`.
- ImageMagick exact comparison finds frame 03 identical across all arms.
- Repository checks are recorded in the final handoff.

## Unresolved questions

- When and where Level 01 record 261 becomes selectable.
- Whether its target rebind becomes visible in a later camera.
- Exact WineD3D-versus-native-Windows texture/dither fidelity.

## Recommended next action

Execute [[Project Roadmap#M1.5 — Tooling boundary audit and promotion]]: audit
the CLI/schema/tests/docs against the M1 evidence boundary, add only missing
synthetic rejection/locality coverage, and publish a no-game-bytes authoring
workflow.

## Git commit if applicable

Bounded commit message: `research: validate Level 01 target rebind`.
