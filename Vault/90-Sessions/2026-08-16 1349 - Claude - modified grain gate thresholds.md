---
type: session
date: 2026-08-16
agent: Claude
status: worker-complete-pending-independent-audit
tags: [session, re/runtime, re/gameplay]
---

# Modified grain gate thresholds

## Goal

Finish KU-060: physically confirm the remaining modified grain gates
(Tunnels rows 0-2/4-8, City gates 1-2) close one below and open at their
configured minimum on the `(1..9)/(1,2,3)` profile.

## Worker result

[[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]].
Ten of twelve gates confirmed at the exact closed-at-(min-1)/open-at-(min)
boundary (Tunnels rows 0,2,3,5,6,7,8; City gates 0,1,2). Tunnels row 1 opens
above its requirement (exact boundary not isolated). Tunnels row 4 opened by
the row-0 coupling (opening row 0 opens row 4) — the EXP-136 linked behavior,
directly demonstrated. City animation slots (gate 1 -> 4/5, gate 2 -> 0/1)
match EXP-139's static prediction.

## Key finding

The game advances its logic/physics **only while the window is focused**
(this Gamescope/Wine setup). Diagnosed by gravity (Flik above the floor did
not fall unfocused; walked only under held focus) and by the gate routine
not running unfocused. This also drops carousel key presses; navigation was
verified by screenshot before selecting. Recorded in
[[PC autonomous game control]].

## Mutation and lifecycle boundary

Modified profile only. `Y:` temporarily repointed to the modified full-disc
copy and restored to `work/copies/BUGS_PC-full-disc`. Only guarded 24-byte
current+preceding teleports and disclosed one-byte grain writes at
`0x0059D9B1`. No auxiliary, executable, asset, or `originals/` write. Owned
process groups and the private sink were closed; final audit clean.

## Durable changes

- New: [[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]].
- Updated: [[Known Unknowns#KU-060 - Modified grain-gate physical transition]]
  (resolved), [[PC autonomous game control]] (focus behavior),
  [[PC grain gate requirements]], [[PC grain gate threshold mod]],
  [[Current State]], the Experiments MOC and this index.

## Next

- Independent audit.
- Optional isolated clean pass for Tunnels row 1.
