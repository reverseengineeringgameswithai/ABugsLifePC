---
type: session
date: 2026-08-16
agent: Claude
status: worker-complete-pending-independent-audit
tags: [session, re/static, re/collision, re/gameplay]
---

# Terrain height and gate standoffs

## Goal

Replace the gate-mapping walking pass with teleports: reimplement the
engine's own terrain height computation offline, validate it against
accepted runtime receipts, and compute a candidate standoff XYZ in front
of each of the twelve grain gates. Static analysis and asset reads only.

## Worker result

- Pinned the complete height pipeline: reset consumer `0x00432930` →
  collector `0x004AC460` (thunk `0x00401659`) → resolver `0x004ACA60`
  (thunk `0x00401717`) → edge test `0x004A9290` (thunk `0x00401500`),
  plus loader clone branch (`0x004A84FF`) and the cell-derived descriptor
  bounds recompute (`0x004A8A1A`). Actor Y = query result − `0x100`.
- `reimplementation/ablpc/terrain_height.py` mirrors it bit-exactly
  (32-bit wrap, toward-zero idiv, winding, tie-breaks, `+0xC80` offset);
  descriptor index order replaces bucket order with a recorded
  height-equivalence argument.
- Receipt validation: EXP-130 walkable point exact (rest Y 30092, delta
  0); EXP-129 endpoint and both EXP-137 City points settle 121-126 units
  deeper. PC world Y grows downward; Level03's nine result-1 reset
  surfaces rest near 64032 under ~30000-32000 ground.
- Contradiction recorded, not normalized: EXP-131's descriptor Z-bounds
  used group headers, the loader uses cell fields (`KU-061`, one live
  dword read will settle it). `plantter.all` descriptors are documented
  out of scope.
- `scripts/grain-gate-standoffs.py` emits deterministic candidate
  standoffs for all twelve gates (engine-exact planes + documented
  center-referenced heuristic); T3/C0 prefer their proven points; C0's
  computed candidate likely sits on the gate structure and is flagged.
- Fourteen new focused tests; full `make check` green.

## Evidence

[[EXP-20260816-141 - Engine-faithful terrain height and gate standoffs]];
new dossiers [[FUNC-97C95BA5572D-004AC460]],
[[FUNC-97C95BA5572D-004ACA60]], [[FUNC-97C95BA5572D-004A9290]]; updated
[[FUNC-97C95BA5572D-004A8410]], [[FUNC-97C95BA5572D-004A8950]],
[[FUNC-97C95BA5572D-00432930]], and
[[PC TERRAIN ALL collision descriptor source]].

## Limits

Standoffs are static candidates: walkability requires the guarded
teleport arms ([[PC Flik teleport procedure]]); the visible gate
correlation and untested physical thresholds stay open under KU-060.

## Next

Independent fresh-context James audit; on acceptance, the runtime
teleport-and-view session with the 1.3.0 `--gates` overlay.
