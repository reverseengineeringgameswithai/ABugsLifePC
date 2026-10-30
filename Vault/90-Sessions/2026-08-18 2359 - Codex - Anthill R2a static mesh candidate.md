---
type: session
date: 2026-08-18
agent: Codex
status: complete
tags:
  - session
  - re/level-format
  - re/runtime-pending
---

# 2026-08-18 2359 - Codex - Anthill R2a static mesh candidate

## Goal

Retarget the first type-`0x41` causal runtime test from Level03 to the
repeatable Anthill Level01 start without reopening corpus-wide R0/R1.

## Result

[[EXP-20260818-008 - R2a Anthill static mesh causal candidate]] specifies
primary record 81, face 8, vertex 25. The zero-rotation object arithmetic
produces the original translated-component tuple `(0,-3205,1000)`. A guarded
`4987 → 7035` component edit changes only `0x189FF: 13 → 1B`, has
expected SHA-256
`c76586991cb4cede5d58a3cae8278aca80ba2082130dcf33062b698334db0a4c`,
and affects no other decoded face in the payload. A full Level01 census finds
one reference each to the selected object and geometry, so the edit reaches
one scene instance. Axis semantics and world scale remain open.

The earlier Level03 candidate remains a fallback. The roadmap, current state,
KU-079, feasibility assessment, dossier, and MOCs now name Anthill as the
primary R2 arm.

## Boundary

No derived DAT was written and no runtime process or memory operation was
started. The archived EXP-013 frame supports only a coarse floor-region
hypothesis; it does not contain the camera transform. R2b therefore requires
matched A1/B/A2 captures and must treat an unlocalized no-change result as
ambiguous.

## James hard-truth correction

James rejected the first committed packet because it had not ruled out
object/geometry sharing, called translated tuples world coordinates, and left
capture comparison open to post-hoc frame selection. The corrected packet:

- censuses all 124 Level01 type-`0x41` references and all 624 records, finding
  one reference each to object `0x4860` and geometry `0x188CC`;
- retains only the proven `+2048` second-input-component delta and explicitly
  leaves axis semantics and world scale open;
- binds R2b to [[PC autonomous game control]], keydown -> requested host sleep
  `0.180` -> keyup XTEST calls (not an exact delivered hold-duration claim),
  fixed log/title anchors, 15 frames per arm at fixed monotonic deadlines, and a
  control-stable/candidate-stable pixel rule that forbids hand-selected frames;
- requires a retained clear `make session-audit` immediately before and after
  each of A1, B, and A2, and forbids the next launch after an unclear post-close
  audit.

## Validation

- The guarded edit was evaluated in memory: one changed byte and the recorded
  derived hash.
- `make check` passed before commit.
- The final worktree was committed and clean before audit handoff.

## Next

Obtain fresh explicit user authorization for the exact R2b derived-file
control/candidate/control experiment, then follow EXP-008 without runtime
memory/debugger writes.
