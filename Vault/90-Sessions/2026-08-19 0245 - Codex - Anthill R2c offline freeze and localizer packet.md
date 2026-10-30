---
type: session
date: 2026-08-19
agent: Codex
topic: Anthill R2c offline freeze and localizer packet
tags:
  - session
  - re/runtime
  - re/level-format
---

# 2026-08-19 0245 - Codex - Anthill R2c offline freeze and localizer packet

## Goal

Prepare the next R2 stage after the inconclusive R2b comparison, use James as a
hard-truth verifier, and stop before any unauthorized derived-file or runtime
action.

## Work completed

- Bound the failure to R2b's global fade interval and froze the exact retained
  retail frame at `t0 + 3.300 s` as the next control reference.
- Added a guarded static-mesh face-index editor with triangle/quad fixtures,
  identity and original-value guards, alignment/range checks, byte-locality
  checks, and reconstructive reparse.
- Defined an orthogonal face-8 localizer that changes only three low bytes and
  degenerates the quad without relying on unknown axis/material semantics.
- Added a committed comparator for stopped-capture identity, exact full-frame
  controls, reference hashing, raw XOR, masks, overlays, and connected-component
  gates.
- Split the runtime into retail-only F0 calibration and later
  C1/localizer/C2, with a commit and James gate before any one-byte successor.

## Boundary

No game was launched and no derived DAT was written. Fresh authorization must
explicitly cover the guarded work-copy write, exact-PID `SIGSTOP`/`SIGCONT`,
four launches at most (F0 and conditionally C1/L/C2), and bounded read-only
view-block snapshots. No runtime memory or debugger write is requested.

## Links

- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[EXP-20260819-001 - R2b Anthill static mesh causal runtime]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC LEVEL DAT static mesh]]
