---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/dynamic
---

# Plant 10 request suppression

## Agent

Codex

## Goal

Execute roadmap packet M2.7 with a START HERE preflight, one-byte locality,
the mandatory Direct3D hardware gate, and evidence-strength-correct comparison
against the retained M1 placement masks.

## Files inspected

- `Vault/00-System/START HERE.md`, Current State, Environment Status, Project
  Charter, Agent Operating Manual, Project Roadmap, Decision Log, Known
  Unknowns, and relevant MOCs.
- Exact collector instructions `0x00416100–0x0041623D`, selector constants,
  Training DAT selectors, prior M1 masks, and M2.5/M2.6 control medians.
- Exact staged executable, Training DAT, and plant 04/10 resource hashes.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-008 - Training record watchpoints and individual roles]]
- [[EXP-20260812-010 - Training target rebind visible substitution]]
- [[EXP-20260812-015 - Plant pair caller and consumer trace]]
- [[EXP-20260812-016 - Plant request origin and separate DAT table]]
- [[EXP-20260812-019 - Same-size paired plant replacement]]
- [[EXP-20260812-020 - Training plant10 request suppression]]

## Changes made

- Corrected the planned target before mutation: class-specific selector
  cursors make `0x394` removal shift the next `0x2B` to ID 4, so the clean
  one-byte plant-10 suppression is `0x3A4: 0x2B → 0x00`.
- Created ignored matched work trees, proved exact one-byte locality, and left
  every plant file unchanged.
- Ran matched hardware Direct3D Training arms through `NextLife`, retaining
  only game logs and metadata in Git. Screenshots and game bytes remain
  ignored under `work/copies/EXP-20260812-020/`.
- Compared 15 normalized frames per arm, temporal medians, and three
  independent prior control medians.
- Updated the static trace, function dossiers, experiment, roadmap, state and
  unknown registers, decision log, relevant MOCs, and session index.

## Conclusions

- **Confirmed:** Both arms selected 640×480×16 Direct3D hardware, never
  entered `INITSOFTRENDER`, completed `InitMainGame`, and reached `NextLife`.
- **Confirmed:** The one-byte `0x3A4` suppression preserves plant 04 and omits
  both plant 10 request lines. After drive/timing normalization those two
  deletions are the complete log difference.
- **Confirmed within the visual procedure:** No stable start-camera mask is
  discriminated beyond independent control variance, so no M1 correspondence
  is promoted.
- **Unknown:** Direct plant-04 suppression and the M1 placement-to-resource
  identity remain unresolved.

## Contradictions discovered

The original roadmap treated the selector at `0x394` as independently bound
to ID 4. Exact instruction review disproved that edit prediction because the
next same-class selector inherits the unadvanced cursor. The contradiction and
revised target are preserved in `EXP-20260812-020` and
`DEC-20260812-015`.

## Tests run

- Exact SHA-256 checks for executable, control/mutated DAT, and four unchanged
  plant resources.
- Recursive source/control and source/suppression comparisons excluding
  generated `bugs.log`; exact `cmp -l` one-byte receipt.
- Hardware renderer, `InitMainGame`, `NextLife`, and requested-path log gates.
- Normalized log diff: exactly two plant 10 request deletions.
- 15-frame PipeWire capture per arm; 640×480 point normalization; all-pairs
  RMSE/AE; temporal medians; three independent control-median comparisons.
- Repository validation recorded after documentation closure.

## Unresolved questions

- Which runtime object/table entry is populated specifically by plant 10?
- Does a bounded M1 record-124–126 consumer read that state?
- What guarded intervention can isolate plant 04 without shifting the shared
  selector cursor?

## Recommended next action

Execute [[Project Roadmap#M2.8 — Plant 10 runtime consumer-to-placement bridge]]
using an unchanged ignored Training copy and native PC runtime access evidence.

## Git commit if applicable

Bounded commit message: `research: validate plant10 request suppression`.
