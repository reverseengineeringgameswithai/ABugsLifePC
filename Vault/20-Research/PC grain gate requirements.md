---
type: research
status: active
updated: 2026-10-02
tags: [re/gameplay, re/static, re/runtime]
---

# PC grain gate requirements

## Confirmed

- Visible Tunnels is internal Level03 and dispatches to `0x00432B30`; visible
  City Entrance is internal Level04 and dispatches to `0x00433900`.
  Evidence: dispatcher `0x00418780`, live `0x00861C84`, and
  [[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]].
- **All directly referenced grain-gate families are in these two levels.** All
  22 direct/static code references to the grain byte `0x0059D9B1` are
  enumerated; only the two inside
  `0x00432B30` (Tunnels) and `0x00433790` (City) are positional
  grain-vs-requirement barrier comparisons, the 17-level dispatcher routes
  only L3/L4 to the gate routines, and the gate tables/state arrays bind to
  L3/L4 alone. This does not exclude address-computed, aliased, or cached
  consumers; global family exclusivity is Inferred. Evidence:
  [[EXP-20260816-146 - Grain-gate level exclusivity static proof]].
- Tunnels reads nine dword requirements at record `+0x08` from the 20-byte
  active table at `0x004DA9C8`. Retail values are
  `(20,10,10,10,20,20,30,10,30)`.
- `0x00432810` initializes that table from template `0x004DAA80`, so an
  executable edit must update both copies. Rows 0 and 4 have linked opening
  behavior in `0x00432B30`.
- City Entrance routine `0x00433790` derives three retail requirements as
  `10 * (index + 1)`: `(10,20,30)`. Its only observed level-specific callers
  in this update path are the three calls from `0x00433900`.
- Both routines compare against unsigned grain byte `0x0059D9B1`.
- The exact test executable with Tunnels `(1..9)` and City `(1,2,3)` loaded
  both levels in PC Direct3D, retaining the configured values in memory.
- EXP-137's independently accepted receipts join those values to physical
  behavior. Tunnels row 3 at known walkable `(501696,30092,494016)` remains
  `0x10C7` and visibly
  closed at grain 3, then settles to `0x0690` and visibly open at configured
  minimum 4. City gate 0 at fixed `(-87622,917,-182181)` remains state `-1`
  with zero animation and visibly closed at grain 0, then changes through
  state 28 with animation `-128/+128` to state 0 and `-1024/+1024`, visibly
  open, at configured minimum 1. `NextLife` stays zero. EXP-138 independently
  accepts this exact row-3/gate-0 evidence boundary.
- [[EXP-20260815-139 - Static grain-gate trigger geometry]] pins the full
  static trigger geometry. City Entrance passes immediates from three
  `0x00433900` call sites: gate 0 `(-71129,-184314)` r=80, gate 1
  `(354031,35256)` r=90, gate 2 `(582271,310212)` r=100, with state dwords at
  `0x0059F020 + i*4` (armed at `-1`, set to `0x20` on trigger, decremented
  per update) and animation accumulators at `0x0059F030` (gate 0 slots 2/3
  deltas -32/+32, gate 1 slots 4/5 deltas +44/-34, gate 2 slots 0/1 deltas
  -28/+32). Proximity helper `0x00416580` computes
  `((dx>>8)^2 + (dz>>8)^2) < r^2` on X/Z only, so effective radii are about
  `r << 8` world units. Tunnels uses the same distance form inline with one
  shared open threshold `0x2710` (about 25600 units) and message threshold
  `0x640` (about 10240 units); row types run `0x10C7 -> 0x1068 -> -140` per
  update down to `0x690`; the rows-0/4 link is the cross-type writes at
  `0x00432F85`/`0x00432F9D`. The static predicate reproduces EXP-137's
  inside/outside boundary at all three accepted points.
  [[EXP-20260815-140 - Independent static gate geometry and overlay audit]]
  independently accepts this static geometry (not any new physical claim).

## Inferred

- The Tunnels resident rows are gate descriptors, but their exact
  player-facing ordering is only bounded by coordinates and behavior. The
  first EXP-129 gate is strongly associated with row 3 by its X/Z proximity
  and retail count-10 outcome.
- Tunnels rows 0/4 are a coupled visible mechanism because either open branch
  updates both active types and an object/animation index. The exact visual
  composition remains unobserved in the modified profile.

## Unknown

*Update (2026-10-02 audit):* the first three items below were later narrowed.
[[EXP-20260816-144 - Runtime grain-gate visual mapping]] visually maps all
twelve gates (Tunnels rows 0–8, City indices 0–2) at walkable standoffs.
[[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]]
records physical modified-threshold receipts for every gate: ten show the exact
closed/open transition, including City gates 1/2 whose animation slots match
EXP-139; Tunnels row 1 opens above its requirement (exact boundary not
isolated); row 4 opens through the row-0 coupling and is not separable. The
items below are the 2026-08-15 state.

- Physical modified-threshold behavior remains untested for Tunnels rows
  0–2/4–8 and City gates 1/2. Tunnels row 3 and City gate 0 are independently
  accepted through EXP-137/138; see
  [[Known Unknowns#KU-060 - Modified grain-gate physical transition]].
- The visible player-facing identity of each Tunnels row and City index is
  unmapped except row 3 and gate 0. Static centers exist for all twelve
  mechanisms (EXP-139), but no safe walkable approach/Y coordinate exists for
  the unwalked ones, and raw centers are not teleport destinations.
- Complete semantics of the Tunnels `+0x04` field and the exact visible order
  of all nine rows remain unknown. Gate 1/2 animation-slot composition is
  static-only; City gates 1/2 have no runtime receipts.
- Generalization to another executable version or another port is unsupported.

## Related

- [[PC grain gate threshold mod]]
- [[FUNC-97C95BA5572D-00432B30]]
- [[FUNC-97C95BA5572D-00433790]]
- [[FUNC-97C95BA5572D-00416580]]
- [[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]]
- [[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]]
- [[EXP-20260815-137 - Modified grain-gate threshold behavior]]
- [[EXP-20260815-138 - Independent modified grain-gate threshold audit]]
- [[EXP-20260815-139 - Static grain-gate trigger geometry]]
- [[EXP-20260815-140 - Independent static gate geometry and overlay audit]]
- [[EXP-20260816-144 - Runtime grain-gate visual mapping]]
- [[EXP-20260816-146 - Grain-gate level exclusivity static proof]]
- [[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]]
- [[PC autonomous game control]]
