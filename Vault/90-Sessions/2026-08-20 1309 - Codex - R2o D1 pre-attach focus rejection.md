---
title: 2026-08-20 1309 - Codex - R2o D1 pre-attach focus rejection
date: 2026-08-20
agent: Codex
tags:
  - session
  - reverse-engineering
  - r2o
  - runtime
status: complete
---

# 2026-08-20 1309 - Codex - R2o D1 pre-attach focus rejection

## Outcome

The first authorized [[EXP-20260820-004 - R2o completed-present state calibration protocol]] D1 passed the complete six-marker hardware Direct3D gate, retail Anthill Level01 load/title, and read-only index value `1`. The immediate pre-attach guard then rejected because the retained game window was not focused about 27 ms after title keyup. D2 did not launch.

No ptrace session existed. No debug-register write, R2o process-memory read,
stopped screenshot, DAT write, localizer, or candidate action occurred. The
rejected arm and aggregate are retained under their consumed `-001`
identities. Cleanup completed, the final audit was clear, and baseline `R:`
was restored to retail. James accepted this rejection and interpretation.

## Offline correction

The fresh `-002` packet adds a fixed `2.000 s` post-title readiness phase. It
revalidates exact process/window identity, activates and focuses only the
retained game XID without game-key input, retains every attempt, and rejects
before ptrace if focus equality is not established. A new runtime requires
James acceptance of the committed amendment and fresh explicit user
authorization. James rejected the first amendment because a command could
return after the deadline and because earlier attempts were not fully rebound.
The correction applies one absolute deadline throughout and validates every
attempt and attempt-file census. A second audit found that summarized focus
was not yet bound to command stdout and runtime timeouts could produce packets
the validator rejected. Focus is now derived from stdout, while timeout and
generic command exceptions terminate before attach with durable receipts. The
amended targeted offline suite passes 90 tests.

## Links

- [[EXP-20260820-004 - R2o completed-present state calibration protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Current State]]
- [[Known Unknowns]]
- [[Reverse Engineering MOC]]
