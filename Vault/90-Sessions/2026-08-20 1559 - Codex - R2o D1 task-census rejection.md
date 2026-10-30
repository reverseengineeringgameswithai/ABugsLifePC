---
type: session
date: 2026-08-20
agent: Codex
topic: R2o D1 task-census rejection and exact-census amendment
status: completed
tags:
  - session
  - reverse-engineering
  - runtime
  - anthill
  - level01
---

# 2026-08-20 1559 - Codex - R2o D1 task-census rejection

## Scope

Run the user-authorized frozen `-004` D1 then D2 completed-present calibration
and submit its outcome to James. Preserve the authorization ceiling: local
execution-breakpoint writes only to `DR0-DR3/DR6/DR7`, bounded owned-task
control, listed reads, and compositor captures; prohibit all other writes and
all DAT/localizer/candidate work.

## Outcome

D1 passed hardware Direct3D, retail Anthill Level01/title/index, nested-display
focus, physical asset, process, and pre-attach guards. Ptrace opened an exact
16-task census and armed only local `DR0 = 0x0040FFC0` on those tasks. The first
exact trap occurred on main TID `1592467` at `EIP = 0x0040FFC0`, with
`SIGTRAP`, `si_code = 4`, and only `DR6.B0` set.

The immediate stop-all census differed from the initial census. The arm
rejected before TID selection, later breakpoint programming, R2o
process-memory reads, or stopped screenshots. D2 did not launch. All 16 changed
debug-register sets were restored and read back; no attachment or runtime
residue remained, and retail `R:` was restored. James accepted this as a
truthful procedural rejection. It does not establish why the census differed
and is not an R2 state, renderer, terrain, collision, material, visibility, or
causal result.

## Durable evidence

- D1 disposition: `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-004/disposition.json`, SHA-256 `553bf96d083a06c55c89748587f77502377c904c712432d9eed8f049b8c3f0ff`.
- Final game log: `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-004/bugs-final.log`, SHA-256 `a238705e3894c53ced8b19a9bd6a74d842f9f4588eb33b91633ec8e23f657d44`.
- Pretrace validation: `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-004/r2o-pretrace-guard.json`, SHA-256 `10b6b3fd2e38b41a3fbd13c70f83e8c9be7f27752615d88a3e37815493941ace`.
- Debugger cleanup: `work/copies/EXP-20260820-004/evidence/rejected/D1-AH-004/debugger-cleanup.json`, SHA-256 `cc5bfe046ae3d71ca7bc74b92bdca76299efd808da901b931bdb1cccaf990431`.
- Aggregate disposition: `work/copies/EXP-20260820-004/evidence/comparison/rejected/completed-present-state-calibration-004/disposition.json`, SHA-256 `df90a7e18b0b62158f2694b18cb058437837df9b56da0023705bd72c26f26938`.

## Follow-up

At that session boundary, `-005` identities were frozen offline. Each census check received an
atomic receipt and complete attempted/completed/validated-or-failed journal
history. The validator independently recomputes task additions, removals, and
TID reuse, authenticates the complete rejected journal prefix, binds exact
baseline restores, parses the exact permitted action/value grammar through the
failure, and requires physically adjacent action-ID-bound census placement for
every accepted open/stop/capture. All receipts repeat the immutable open task
identity; failed prefixes bind complete raw-stop/slot/DR6/active-debug and
chained debug-state transitions. The final audit correction requires the
completed ptrace-open list to match the exact sorted `(TID,start_ticks)`
census, accepts only supported recorded stop layouts, derives the payload as
three native words, and holds the layout constant across the packet. This
matches the retained `x86_64`/24-byte `-004` evidence. If a separately
authorized `-005` D1 repeats drift, stop completed-present retries and design a
separate task-lifecycle diagnostic.

The ninth audit correction further requires raw wait-status proof of a stopped
`SIGTRAP` with zero ptrace event and compares the completed ptrace-open list in
its recorded order to the immutable sorted census. This prevents a ptrace-event
stop, inconsistent raw status, or reordered attachment receipt from being
normalized into a valid rejected packet. It authorizes no runtime action.

## Links

- [[EXP-20260820-004 - R2o completed-present state calibration protocol]]
- [[Decision Log#DEC-180 - Preserve exact R2o task-census disagreement before verdict|DEC-180]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]
- [[Current State]]
