---
title: 2026-08-20 1423 - Codex - R2o D1 nested-display rejection
date: 2026-08-20
agent: Codex
tags:
  - session
  - reverse-engineering
  - r2o
  - runtime
status: complete
---

# 2026-08-20 1423 - Codex - R2o D1 nested-display rejection

## Outcome

The authorized `-002` D1 for [[EXP-20260820-004 - R2o completed-present state calibration protocol]] passed the complete six-marker hardware Direct3D gate and retail Anthill Level01 load/title/index gates. Its fixed readiness phase retained the same PID/start/PGID, XID, and `640x480` loading/game window for 26 attempts, but unscoped host-display focus calls returned `BadWindow` while display-scoped discovery and guards continued to observe that window. D1 rejected before attachment; D2 did not launch.

No ptrace session, debug-register write, R2o state read, stopped screenshot,
DAT write, localizer, or candidate action occurred. Cleanup completed, the
final audit was clear, and baseline `R:` was restored to retail. James accepted
the rejection as an executor display-scope defect, not a renderer, window-
disappearance, or R2o state result.

## Offline correction

The fresh `-003` packet scopes every readiness and final pre-attach focus
command to the nested display proven by `runtime-identity-confirmed.json`.
Every attempt retains and validates that receipt's X display, Gamescope
display, PID, start tick, PGID, and cwd binding. Missing or changed provenance
rejects with a durable summary before ptrace. The targeted offline suite
passes 93 tests. Runtime remains unauthorized pending James acceptance and
fresh explicit authorization.

## Evidence

- D1 disposition SHA-256 `01cc7e24cc17ed044ef282433284c8c692aa92fb015df4d7165b6e4bf274ce35`.
- Final log SHA-256 `2e649a1a6bdb28333eb7b61f92621adcaf5af1a08eda8ac8847ff7420ffebeb7`.
- Focus summary SHA-256 `3c46fd8b51f27907771e34870665e46bb29bdf2f2d3d1fed8424bcd08fdb0e7c`.
- Aggregate disposition SHA-256 `2505c0b7d9974f965d0fe8d6ea37c720804d6ac7aa58b8035f07873925c4c5a6`.

## Links

- [[EXP-20260820-004 - R2o completed-present state calibration protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Current State]]
- [[Known Unknowns]]
- [[Reverse Engineering MOC]]
