---
type: session
date: 2026-08-15
agent: Codex
status: worker-complete-pending-independent-audit
tags: [session, re/runtime, mod/gameplay]
---

# Modified grain gate runtime thresholds

## Goal

Behaviorally test the EXP-136 profile below and at one configured Tunnels and
City Entrance grain minimum, save useful coordinates, strengthen renderer
validation, and submit the result to James's reject/correct/accept ratchet.

## Worker result

- Tunnels row 3 at known walkable `(501696,30092,494016)` stayed type
  `0x10C7` and visibly closed at grain 3, then settled to `0x0690` and visibly
  open at configured minimum 4; `NextLife=0`.
- The researcher ordinarily reached City first-gate approach
  `(-92603,1098,-181281)`, then a short forward step first triggered around
  `(-87622,917,-182181)`.
- A fresh same-position City arm at that proven trigger left state `-1`, zero
  animation, and the visible gate closed at grain 0. With no movement, grain 1
  drove state 28 to 0 and animation `-128/+128` to `-1024/+1024`, visibly
  opening the gate; `NextLife=0`.
- The retail `10` numeral remains visible because the executable recipe does
  not edit that graphic.

## Correction

The first City route control was just outside the proximity trigger, so it was
not treated as a same-position count discriminator. A later candidate arm
printed the early Direct3D selection summary but entered 320x200 system-memory
software rendering. It made no target write and was rejected. The replacement
arm passed video-memory status, 640x480 creation, explicit Direct3D start, and
visible 640x480 gameplay. [[START HERE]] now records this stronger gate.

## Mutation and lifecycle boundary

Accepted writes were limited to guarded current-plus-preceding XYZ setup at
already-proven walkable coordinates and exact one-byte grain changes. No
auxiliary, gate state, animation, life, register, code, asset, or original
write occurred. All owned processes/reapers and private sinks were closed;
Wine `Y:` was restored and final scoped audits were empty. Raw game-bearing
evidence remains ignored under `work/copies/`.

## Durable changes

- [[EXP-20260815-137 - Modified grain-gate threshold behavior]]
- [[PC grain gate requirements]]
- [[PC grain gate threshold mod]]
- [[FUNC-97C95BA5572D-00432B30]]
- [[FUNC-97C95BA5572D-00433790]]
- [[Known Unknowns#KU-060 - Modified grain-gate physical transition]]
- [[START HERE]]

## Pending

Worker evidence awaits James's independent hard-truth audit. Any rejection
must be corrected and resubmitted until accepted.
