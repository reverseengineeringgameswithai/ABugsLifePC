---
type: session
date: 2026-08-20
agent: Codex
topic: R2o -005 rejection and R2p task-lifecycle pivot
status: completed
tags:
  - session
  - reverse-engineering
  - level01
  - terrain
---

# 2026-08-20 1800 - Codex - R2p task lifecycle pivot

## Runtime outcome

Ran the user-authorized frozen R2o `-005` D1 then D2 command. D1 reached the
first exact `0x0040FFC0` trap, then the immutable 16-task census gained TID
`1648646`, start ticks `28065259`. It rejected before R2o reads or stopped
captures. All permitted debug-register changes were restored, cleanup and
retail `R:` restoration were clear, and D2 was not created. James accepted the
procedural rejection. The frozen rule ends R2o retries.

## Offline follow-up

Created [[EXP-20260820-005 - R2p task lifecycle diagnostic]] and an
argument-free analyzer. The corrected analyzer authenticates the complete
classified manifests and accepted R2o action grammar before recomputing the
task delta, and bounds the PC-static `CreateThread` path without attributing
the Linux task. Corrected output SHA-256:
`8d35c6b68a21d881ad98981db6842b8d050a17d7900c29fec4ea319378f70e43`.

The original analysis `b407bcf2...2d5` is preserved unchanged under an
`obsolete/` evidence namespace because it did not bind complete manifest
closure. Publication now uses a fresh temp-file/fsync/re-read/atomic-rename
path. The future passive contract now requires exactly 521 samples on the
20 ms grid, start within 2 ms, completion within 10 ms, no overlap, and
strictly increasing timestamps. Focused offline coverage passed 41 tests,
including full-chain raw-trap, debug-value, extra-action, and manifest
forgeries.

The future P0A passive collector is frozen but unauthorized and unrun. It
allows no debugger, signal, memory read, screenshot, DAT, localizer, candidate,
or R2o action.

## Links

- [[EXP-20260820-004 - R2o completed-present state calibration protocol]]
- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
- [[Decision Log#DEC-181 - End R2o retries and require passive task-lifecycle evidence|DEC-181]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)|KU-079]]
- [[Current State]]
