---
type: session
date: 2026-08-19
updated: 2026-08-19
agent: Codex
status: complete
tags:
  - reverse-engineering
  - level01
  - terrain
  - offline
---

# 2026-08-19 1734 - Codex - R2d sampled phase calibration packet

## Scope

Prepared the next offline/static R2d packet after the accepted-but-inconclusive R2c C1/L/C2 run. James reviewed the design boundary before implementation.

## Work completed

- Measured the retained R2b controls and found no same-process exact recurrence on their short `t0+0.5..3.3` grids. Their cross-launch equal endpoints do not establish a cycle.
- Froze a broad, non-adaptive 121-frame live grid for two independent auto-hardware control processes.
- Implemented exact sampled-period detection, one-way D1 nuisance-mask construction, fixed three-pixel dilation, coverage cap, D1 holdout, and independent D2 holdout.
- Added an argument-free control-only runner with no SIGSTOP, localizer, or candidate path.
- Added focused regression coverage; 123 targeted tests passed before the first repository-wide gate.
- Created [[EXP-20260819-003 - R2d Anthill sampled phase calibration]].

## Runtime and authorization boundary

No game launch, process signal, process-memory read, runtime write, or derived DAT creation occurred in this session. D1/D2 require fresh explicit user authorization. The planned runtime operation includes only the read-only four-byte Level01 index read at `0x00861C84`; it includes no SIGSTOP/SIGCONT and no stopped view-block reads.

## Result

The offline R2d packet is ready for repository checks and James audit. A sampled cycle and nuisance mask remain unestablished until both newly authorized controls pass.

## James audit revision

James rejected commit `4060a43` because it did not compare retained D1/D2 process identities, some capture failures raised before their receipts were durable, post-run validator failure could leave an arm accepted, result vocabulary differed from the protocol, and lifecycle/forgery regressions were incomplete.

The first correction made arm acceptance provisional, retained capture failures and ordered timestamps, bound nested receipts, and quarantined incomplete pairs. James's second audit found that observation-analysis exceptions still preceded their receipt, `clean: true` alone was accepted without checking empty audit fields, and matching PID/start-ticks could pass when PGID differed.

The second correction atomically retains observation attempts and decode/analysis failures, validates the exact empty `game-session` pre/post structure, and requires distinct `(PID, start_ticks)` identities while retaining PGID separately. The expanded focused suite passes 145 tests. No runtime action occurred during either revision.

## Later runtime disposition

The user subsequently authorized EXP-003. D1 captured all 121 frames and rejected on live `lower-right-structure` drift; D2 did not run. Offline diagnosis found no exact sampled period. The packet is consumed and superseded by [[EXP-20260819-004 - R2e Anthill stable-background calibration]]. See [[2026-08-19 1817 - Codex - EXP-003 rejection and R2e replacement]].

## Links

- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[EXP-20260819-003 - R2d Anthill sampled phase calibration]]
- [[Known Unknowns]]
