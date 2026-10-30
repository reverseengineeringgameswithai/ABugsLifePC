---
type: session
date: 2026-08-15
agent: Codex
status: completed
tags: [session, re/static, re/runtime, mod/gameplay]
---

# PC grain gate threshold mod

## Goal

Expose different minimum grain requirements for visible Tunnels and City
Entrance using PC-native evidence and a guarded reversible work-copy recipe.

## Result

- Corrected the initial association: Tunnels is internal Level03 and uses the
  nine-row table consumer `0x00432B30`; City Entrance is internal Level04 and
  uses the three-index formula consumer `0x00433790`.
- Added `reimplementation/ablpc/grain_gate_mod.py` and
  `scripts/make-grain-gates`, with exact retail SHA/source-byte guards,
  `0..50` bounds, work-only output, preservation, and inverse proof.
- Patched both Tunnels active/template copies and replaced the City formula
  with an independent three-dword lookup in an existing alignment gap.
- Added twelve asset-free tests including exhaustive retail City formula/table
  equivalence for indices 0..2 and grain 0..50.
- Built test profile Tunnels `(1..9)`, City `(1,2,3)`, SHA-256
  `69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b`.

## Runtime boundary

One software-renderer arm was rejected. Two fresh Direct3D arms loaded visible
Tunnels/internal Level03 and City Entrance/internal Level04 and retained the
configured requirement tables after initialization. Only ordinary input and
read-only inspection were used; there was no target write, debugger,
breakpoint, asset edit, or `originals/` access.

No gate was physically crossed at a changed threshold. KU-060 records that
remaining discriminator. Tunnels rows 0/4 also retain linked open behavior.

## Lifecycle and project status

Scoped game/reaper/helper processes and private sinks were closed, and Wine
`Y:` was restored to the ordinary full-disc work copy. Game-bearing test
artifacts remain ignored below `work/`. M3 stays Complete; M2/M5 stay Deferred;
M4/M6 stay Complete. No PS1 evidence was consulted.

## Durable changes

- [[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]]
- [[PC grain gate requirements]]
- [[PC grain gate threshold mod]]
- [[FUNC-97C95BA5572D-00432B30]]
- [[FUNC-97C95BA5572D-00433790]]
- [[Known Unknowns#KU-060 - Modified grain-gate physical transition]]

## Validation

- Focused grain-gate suite: 12 passed.
- Complete `make check`: Python doctor passed; Vault 396 notes, 0 errors, 0
  warnings; five M4 hash anchors valid; 588 tests passed; tracked-file audit 0.
- `git diff --check` passed.
- Retail/profile SHA-256 and equal 1,069,056-byte sizes reverified.
- Final scoped process/sink audit was clear and Wine `Y:` resolved to the
  ordinary full-disc work copy.
