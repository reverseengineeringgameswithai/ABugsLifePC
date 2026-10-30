---
type: implementation
status: exact-pc-executable-recipe
updated: 2026-08-15
tags: [implementation/gameplay, mod/executable]
---

# PC grain gate threshold mod

`scripts/make-grain-gates` builds a fresh same-size `bugs.exe` work copy with
configured Tunnels and/or City Entrance grain requirements.

```bash
./scripts/make-grain-gates \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe \
  work/copies/bugs-grain-gates.exe \
  --tunnels 1,2,3,4,5,6,7,8,9 \
  --city-entrance 1,2,3
```

An omitted option stays at retail. Tunnels requires exactly nine values;
City Entrance requires exactly three. Every value must be in `0..50`.

## Exact support boundary

- source SHA-256 must be
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`;
- source and output must be distinct non-linked paths below `work/`;
- output must not already exist;
- every source byte, range, and patch width is pinned;
- the transform checks non-overlap/bounds, preserves all unselected bytes,
  and proves exact inverse reconstruction before returning;
- game-bearing outputs remain ignored and must not be committed or
  distributed by this repository.

The Tunnels edit patches the nine requirement dwords in both active image
table `0x004DA9C8` and initializer template `0x004DAA80`. Rows 0 and 4 have
linked opening behavior and should not be presented as visually independent
without another runtime discriminator.

The City Entrance edit replaces the retail indexed formula at
`0x004337D1` with a three-dword lookup at existing alignment gap
`0x004338B0`. Exact retail values `(10,20,30)` are differentially equivalent
to the old formula for every gate index and grain count `0..50`.

## Validation boundary

The `(1..9)`/`(1,2,3)` profile has same-size output SHA-256
`69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b`.
Both visible levels loaded in PC Direct3D with their configured tables
resident after initialization. EXP-137 validates Tunnels row 3's physical
`3 closed / 4 open` boundary and City gate 0's same-position
`0 closed / 1 open` boundary; EXP-138 independently accepts only that exact
scope. [[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]]
then confirms the remaining gates: ten of twelve show the exact
closed-at-(min-1)/open-at-(min) transition, row 1 opens above its
requirement, and the rows-0/4 coupling is directly demonstrated (opening row
0 opens row 4). See
[[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]],
[[EXP-20260815-137 - Modified grain-gate threshold behavior]],
[[EXP-20260815-138 - Independent modified grain-gate threshold audit]], and
[[Known Unknowns#KU-060 - Modified grain-gate physical transition]].

## Saved runtime coordinates

- Tunnels row 3: `(501696,30092,494016)`, already accepted as walkable in
  EXP-130 and within the row-3 open radius in EXP-137.
- City first-gate approach: `(-92603,1098,-181281)`. The researcher reached
  this ordinarily; it visibly frames the gate but is just outside the trigger.
- City first-gate trigger: `(-87622,917,-182181)`. The researcher/Codex route
  reached this by one short forward step from the approach point; EXP-137 then
  reused it as a known walkable fixed-position discriminator.

Coordinates are level-specific PC runtime values, not portable spawn points.
Follow [[PC Flik teleport procedure]] and require matching internal level,
exact current-plus-preceding write/readback, no auxiliary write, survival, and
fresh state. Never use the approach point as proof that the City proximity
predicate is true.

## Gate mapping pass support

[[EXP-20260815-139 - Static grain-gate trigger geometry]], independently
accepted by
[[EXP-20260815-140 - Independent static gate geometry and overlay audit]],
pins every
mechanism's static trigger center and radius: all nine Tunnels rows share
an open radius of about 25600 units around their table X/Z, and the three
City gates use immediates `(-71129,-184314)` r=80, `(354031,35256)` r=90,
and `(582271,310212)` r=100 (about `r << 8` units). The geometry bytes are
identical in retail and the accepted `(1..9)/(1,2,3)` profile.

`scripts/coordinate-overlay.py` 1.3.0 adds an opt-in `--gates` readout
(nearest mechanism, requirement, live type/state, world distance versus
effective radius, engine-exact IN/out) and accepts exactly the retail hash
or the accepted profile hash. Use it for the mapping pass that correlates
each visible gate with its Tunnels row or City index and saves verified
approach coordinates. Static centers are trigger geometry, not teleport
destinations.

## Candidate teleport standoffs (EXP-20260816-141)

`scripts/grain-gate-standoffs.py` computes deterministic candidate
standoff XYZ per gate from the engine-faithful terrain height query
(`reimplementation/ablpc/terrain_height.py`, validated at four accepted
receipt points; PC world Y grows downward). Chosen candidates:

| Gate | Candidate (x, restY, z) | Gate | Candidate (x, restY, z) |
|---|---|---|---|
| T0 | (205067, 33916, 143005) | T5 | (1126934, 31480, 1308289) |
| T1 | (489642, 32092, -451306) | T6 | (1471643, 32820, 1426369) |
| T2 | (843615, 33812, 302388) | T7 | (1202034, 31492, 1970285) |
| T3 | prefer proven (501696, 30092, 494016) | T8 | (1646238, 33792, 2546125) |
| T4 | (840401, 33940, 626583) | C1 | (354031, 2540, 10716) |
| C0 | prefer proven (-87622, 917, -182181) | C2 | (601433, 1132, 329374) |

These are **static candidates**, not proven walkable points: apply them
only through [[PC Flik teleport procedure]] (current-plus-preceding
write, readback, survival, fresh state), expect standing Y to settle
121-129 units deeper than the written rest Y (observed extremes; EXP-20260816-156
widened this from 121-126), and treat any reset loop as
a rejected candidate, not a defect. Tunnels standoffs sit outside the
message radius and inside the open radius (harmless at grain 0); City
standoffs sit just outside their trigger radii, and C0's computed
candidate likely rests on the gate structure itself — use the proven
points for C0.
