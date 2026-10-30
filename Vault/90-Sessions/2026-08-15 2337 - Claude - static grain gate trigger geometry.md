---
type: session
date: 2026-08-15
agent: Claude
status: worker-complete-pending-independent-audit
tags: [session, re/static, re/gameplay]
---

# Static grain gate trigger geometry

## Goal

Complete the offline static half of the gate-by-gate mapping pass: extract
the remaining City Entrance trigger centers, pin every mechanism's radius
and state mechanics to exact bytes, and give the researcher a nearest-gate
overlay readout for the later walking pass. No runtime process, no target
write.

## Worker result

- All three `0x00433900` call sites pass immediates only. New static facts:
  City gate 1 center `(354031,35256)` radius parameter 90 and gate 2 center
  `(582271,310212)` radius parameter 100; gate 0 `(-71129,-184314)` r=80
  now carries byte evidence for its previously approximate center.
- Proximity helper `0x00416580` (thunk `0x00401A37`) is exactly
  `((dx>>8)^2 + (dz>>8)^2) < r^2` on X/Z, so effective radii are about
  `r << 8` world units. City state dwords live at `0x0059F020 + i*4`
  (armed `-1`, set `0x20`, decremented), animation accumulators at
  `0x0059F030` with per-gate slots/deltas from the call sites.
- Tunnels applies the same distance form inline: shared open threshold
  `0x2710` (~25600 units) at `0x00432F49`, message threshold `0x640`
  (~10240) at `0x00432FEB`, requirement checked before distance, type
  lifecycle `0x10C7 -> 0x1068 -> -140` per update to `0x690`, and the
  rows-0/4 coupling as cross-type writes `0x00432F85`/`0x00432F9D`. A
  separate `0x004DAB38` sar-10 region table is recorded as a non-gate.
- Cross-check: the extracted predicate reproduces EXP-137's independently
  accepted inside/outside boundary at all three receipt points (row-3
  walkable 4993<10000; City trigger 4289<6400; City approach 7177>=6400)
  and gate 0's `-128/+128 -> -1024/+1024` animation arithmetic.
- `scripts/coordinate-overlay.py` 1.3.0 adds opt-in `--gates` (nearest
  mechanism, requirement, live type/state, world distance vs radius,
  engine-exact IN/out) and widens the target boundary to exactly
  {retail, accepted EXP-136 profile}; reads remain `process_vm_readv`.
  Overlay tests grow to 14.

## Evidence

[[EXP-20260815-139 - Static grain-gate trigger geometry]] with decoder plus
raw-byte pins at file offsets `0x32D2F`, `0x15980`, `0x32349`, `0x323EB`,
`0x32385`, `0x3239D`, `0x32BEF`, `0x322EC`, `0x322F8`, `0x32417`,
`0x3241E`. Executable hash reverified before reads.

## Limits

Static centers are trigger geometry, not teleport destinations or walkable
points. Visible gate identity for unwalked mechanisms, safe approach/Y
coordinates, and physical modified thresholds for City gates 1/2 and
Tunnels rows 0–2/4–8 remain open under
[[Known Unknowns#KU-060 - Modified grain-gate physical transition]].

## Next

Independent fresh-context James audit of this packet; on acceptance, the
researcher walking pass with the 1.3.0 `--gates` overlay.
