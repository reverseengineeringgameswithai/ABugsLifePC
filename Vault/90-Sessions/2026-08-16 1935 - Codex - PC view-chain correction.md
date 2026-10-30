---
type: session
date: 2026-08-16
agent: Codex
status: worker-complete-accepted-by-exp165
tags: [session, re/camera, re/correction, research/coverage]
---

# PC view-chain correction

## Goal and boundary

Execute the single correction ordered by
[[EXP-20260816-162 - Independent camera reconnaissance audit]], then submit a
clean worker commit to a fresh-context James verifier. This session is the
worker half only; it cannot self-accept the Camera row.

The mandatory startup sequence, Current State head/recent sections, roadmap
operating model and M5 sections, Environment Status, Agent Operating Manual,
Project Charter, cross-port policy/registry, relevant decision and unknown,
root instructions, MOCs, EXP-161/162, XPORT-004, and prior James precedent
were read at clean subject HEAD
`0238cccf1e73d8b04c576d2047da5e393b9f240e` before substantive work.

Scope remained offline and PC-static: this work launched no new game, Wine,
Gamescope, debugger, or target; made no target write, implementation change,
or semantic rename; and performed no external PS1 read or mutation. The 32
pre-existing unowned `winedevice.exe` helpers recorded by EXP-163 remained and
were not terminated by broad name.

## Result

[[EXP-20260816-164 - PC view-chain correction and coverage reclassification]]
is worker-complete. The exact binary remains
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

The strongest independently reproducible join is now explicit:

- `0x00455788` pushes output `0x005B58E0` and `0x00455799` calls the
  angle-to-matrix thunk;
- `0x00463D55`-`0x00463E48` writes nine matrix words to that output;
- renderer `0x0044D4C1` pushes the exact same `0x005B58E0`, and
  `0x0044D4C6` calls `0x00401C4E -> 0x004636C0` to load all nine words into
  transform scratch `0x0063E888`-`0x0063E8B0`.

The rest of the structural chain reproduces: `0x0041ADF0` reads live Flik XYZ
and updates a position/orientation source; `0x0041B7D0` selects two source
layouts into common `0x00599C90`; `0x00455710` stores origin
`0x005BDB8C` and matrix/copy `0x005B58E0`/`0x005BDBAC`; and
`0x00405FE0` performs the signed fixed-point transform locally beginning at
`0x0040605F`.

The static call census reproduced 7 calls to terrain thunk `0x00401659`, 2
calls to view-consumer thunk `0x00401848`, and 12 calls to builder thunk
`0x00401D66`. Removing two reset functions and known City dispatcher
`0x00433900` leaves four unmapped terrain functions; two enclosing functions
read Flik position without proving their query point is Flik.

## Evidence discipline

- **Confirmed:** exact instruction/data flow, corrected viewport range
  `0x00423EDE`-`0x00423F43`, known-only TL-vertex scope, local transform,
  non-caller disposition for `0x0045A7F0`, and the exact counts.
- **Inferred:** ordinary follow-source and scripted/setpiece-source roles.
- **Unknown:** source/selector gameplay meanings, manual PC camera controls,
  second `0x0043D486` consumer, update frequency, visual causality, complete
  indirect paths, and Direct3D view state beyond three known submissions.

KU-066 records those open semantics. XPORT-004 now says the PC independently
supports structural similarities; PS1 still confirms no PC fact, and manual
controls remain an open discrepancy rather than a port difference.

## Live propagation

Updated EXP-161's live status, XPORT-004, Current State, Project Roadmap,
Subsystem Coverage Map, Subsystems/Experiments/Reverse Engineering MOCs,
DEC-134, KU-066, and the historical worker session. Added
[[PC camera view-transform chain]] plus exact static export
`static/exports/BIN-97c95ba5572dce63/SUBSYS-camera-view-chain-static-trace.md`.

Per DEC-134, this worker commit left Camera administratively Untouched for the
fresh audit. EXP-165 subsequently returns ACCEPT at the exact clean commit and
authorizes propagation to Bounded.

## Validation

- Static counts asserted: terrain/view-consumer/builder thunk calls =
  `7`/`2`/`12`.
- `make check` ran with direct raw redirection to
  `/tmp/ablpc-exp164-make-check.log`, SHA-256
  `209d9d12a3e10f3d88ec5820f3414591bef55c4af06bc539ef1d1cb6bcbbc9fb`.
- That observed run reported Vault `467/0/0`, five valid M4 hash anchors,
  tracked-file audit 0, and `648 passed in 18.06s`.
- The suite result remains qualified by open KU-065; it is not an
  unqualified clean gate.
- `git diff --check` and Vault lint pass after live propagation.
- Closure audit found no game, Gamescope, `wineserver`, pytest, debugger
  target, or private sink; the same 32 pre-existing unowned Wine device
  helpers remain recorded under the lifecycle-policy boundary.

## Next

The worker delta was committed as `0336d14` and independently accepted by
[[EXP-20260816-165 - Independent PC view-chain correction audit]]. Camera is
Bounded; future semantic/runtime work remains governed by KU-066.
