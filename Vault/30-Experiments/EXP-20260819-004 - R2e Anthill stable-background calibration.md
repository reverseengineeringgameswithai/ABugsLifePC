---
type: experiment
id: EXP-20260819-004
status: rejected
date: 2026-08-19
updated: 2026-08-19
result: Authorized D1 captured all 121 frames, then rejected on the exact full-frame F0 gate; D2 was not run, no mask was accepted, and EXP-005 supersedes the phase-sensitive protocol.
question: Can two independent retail-DAT controls validate a bounded finite sampled stable-background mask without claiming an animation cycle?
environment: PC auto-hardware derived-build route; D1 runtime rejected and cleaned
binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
evidence:
  - reimplementation/ablpc/r2e_stable_background.py
  - scripts/r2e-run-stable-background-calibration.py
  - scripts/r2e-diagnose-consumed-d1.py
  - tests/test_r2e_stable_background.py
tags:
  - reverse-engineering
  - pc
  - level01
  - terrain
  - runtime-rejected
---

# EXP-20260819-004 - R2e Anthill stable-background calibration

> [!failure] Consumed and superseded
> `D1-SB-AH-001` is a valid fail-closed rejection. Its exact full-frame F0 gate was phase-sensitive even though the required camera crops remained exact. D2 is unrun and obsolete. Do not launch this protocol again; use [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]].

## Question

Can a fresh D1 control define a finite 24-second sampled variability exclusion mask, and can a separate D2 process reproduce every unmasked pixel exactly without any cycle, phase, or exhaustive-nuisance claim?

This packet supersedes the failed exact-period model in [[EXP-20260819-003 - R2d Anthill sampled phase calibration]]. It is a control-only prerequisite and does not run the face-8 localizer or one-byte candidate.

## Authorization boundary

- The user later authorized this exact packet. That authorization was consumed by rejected arm `D1-SB-AH-001` and does not authorize a retry or EXP-005.
- `scripts/r2e-run-stable-background-calibration.py` must not be launched again. The old D2 identity is obsolete.
- The only planned process-memory access is the read-only four-byte Level01 index read at `0x00861C84` before title Return.
- No runtime/debugger/DAT write, SIGSTOP/SIGCONT, stopped-view read, localizer, candidate, or C/L/L/C arm is authorized or reachable.

## Why EXP-003 was replaced

The consumed EXP-003 D1 process captured all 121 frames, then correctly rejected because `lower-right-structure` changed at frame 1. Offline diagnosis proved:

- 121 captures and 121 distinct decoded-RGB hashes;
- no exact sampled period under the frozen EXP-003 detector;
- three crop sequences had one exact hash each;
- `lower-right-structure` had six hashes and first drifted at index 1;
- whole-grid D1 variability was 76,807 pixels (`0.2500227864583333`);
- radius-three dilation was 90,913 pixels (`0.29594075520833335`).

The machine receipt is ignored runtime evidence at `work/copies/EXP-20260819-003/evidence/rejected/D1-AH-001/offline-diagnostic-002/diagnostic.json`, SHA-256 `d17eeda40826280448196a78770d7e1434db6d1ba92b805114597c42b2ad4583`. It binds all capture files/receipts, PNG/RGB hashes, timing, build/DAT/process identity, crop sequences, masks, `exact_sampled_period: null`, and the absence of all four exact old-D2 stage/pending/accepted/rejected paths. D1 remains rejected and is not retroactively accepted.

The new 35% cap was selected after observing the consumed diagnostic's 29.5941% dilation. It is preregistered only for fresh EXP-004 arms and is not independent support from the rejected run.

## Historical frozen identities

- Executed auto-hardware image: SHA-256 `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
- Retail Anthill Level01 DAT: SHA-256 `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
- D1 stage/evidence: `D1-stable-background-retail-001` / `D1-SB-AH-001` under ignored `work/copies/EXP-20260819-004/`.
- D2 stage/evidence: `D2-stable-background-retail-001` / `D2-SB-AH-001` under the same root.
- Aggregate result identity: `stable-background-mask-001`.
- All stage, pending, accepted, rejected, and aggregate final paths must be initially absent.
- The old unrun EXP-003 `D2-AH-001` identity is obsolete and must never be launched.

## Historical camera gate and rejected full-frame clause

The consumed protocol required every fresh arm's frame zero to equal the exact accepted derived-build F0 reference:

- PNG SHA-256 `05f5691cab126962715d94857fd5085f7013353b3982a7d6e9d350215506ad1c`;
- decoded RGB SHA-256 `2ea6564339c406cbcd92ca32faaf4e6c1b177119939aee569f0cfc1223b9d26c`.

Every one of the 121 frames must reproduce these exact crop coordinates and hashes:

| Region | Rectangle `(x,y,w,h)` | Decoded-RGB SHA-256 |
|---|---|---|
| `upper-right-structure` | `(480,0,160,100)` | `41aa36449cae7e735d5476644f670d01eb931490484d22091da1647ad1852bf6` |
| `left-middle-structure` | `(20,220,120,100)` | `7a87a57c278e09861fada1511c7aac9dd10cfe607d109fb6b48696103998ab14` |
| `lower-left-structure` | `(0,380,160,100)` | `59e3593b7b487553a63483cf20134aef9be97dae6b73690e5f5ababa8e1541e0` |

`lower-right-structure` at `(480,380,160,100)` is explicitly excluded because the consumed control proved it contains temporal content. It is not a view invariant or a renderer-selection signal.

That exact full-frame clause rejected a valid camera-stable D1 at a different live-animation phase. It is not an active requirement. The three crop identities below did remain exact across all 121 consumed frames and carry forward only as camera-control gates in EXP-005.

## Historical frozen arm procedure - do not run

1. Require a clean pre-launch audit, retail baseline `R:` mapping, exact source/cache/DAT/CD identities, and fresh namespaces.
2. Launch only the exact `play-pristine.sh --auto-hardware` route and require all six Direct3D markers with no software/mixed terminal marker.
3. Use the frozen Right, Return, Return sequence to Anthill Level01. Define `t0` as title-Return key-up and send no later input.
4. Capture 121 live 640x480 compositor frames at `t0 + 3.300 + 0.200*i`, `i=0..120`, through `t0+27.300`.
5. Require request-start error at most `0.005 s`, file stability by target plus `0.150 s`, hashing by target plus `0.180 s`, and no overlap. Retain atomic attempt/result receipts before every verdict.
6. The consumed procedure required its full-frame and camera gates, process/build/DAT/window identity before and after the grid, and a clean post-close audit with retail `R:` restored.
7. Treat each clean arm as provisional until independent validation and the complete D1/D2 analysis pass.

Acquisition receipts and compositor commands remain immutably bound to their original `evidence/pending/...` paths. After lifecycle classification, existence and hash recomputation use the corresponding `evidence/accepted/...` files. Raw receipts are never rewritten to pretend acquisition occurred in the accepted namespace.

## Historical D1 finite variability mask

1. Compare every D1 frame `1..120` against D1 frame zero by exact decoded RGB.
2. Mark the union of every unequal pixel across the complete 121-frame grid.
3. Require at least one marked pixel.
4. Dilate with a clipped Chebyshev square of radius exactly three pixels.
5. Require dilated coverage at or below exactly 35% of 307,200 pixels.

This construction makes every D1 sampled pixel outside its own union equal to D1 frame zero by definition. It is not an independent D1 holdout and must not be described as one. No period detection, phase rotation, frame hunting, normalization, registration, or adaptive extension occurs.

## Historical independent D2 holdout

- Independently compute and record D2's own whole-grid variability, but never add it to or expand the D1 mask.
- Compare every pixel of every D2 frame against D1 frame zero outside the frozen, dilated D1 mask.
- Require exactly zero outside-mask mismatches.
- Require a distinct `(PID, start_ticks)` process identity; retain both PGIDs separately as launch provenance.

## Historical outcomes

| Observation | Disposition |
|---|---|
| Both control packets validate; D1 nonzero mask is at most 35%; all D2 outside-mask comparisons are exact | `accepted-stable-background-mask` |
| D1 mask is zero/over cap or D2 has any outside-mask mismatch | `stable-background-mask-rejected` |
| Identity, renderer, level, timing, frame-zero, crop, receipt, or lifecycle gate fails | `control-packet-rejected` |
| Cleanup or retail mapping restoration is unclear | pending |

Any failure quarantines provisionally accepted controls and publishes no accepted mask. Cleanup uncertainty remains pending.

## Historical accepted-claim ceiling

A success would establish only an exact-view/build, 24-second sampled stable-background mask for the derived executable. It would not establish:

- an animation cycle or period;
- exhaustive nuisance coverage outside the sampled interval/view;
- face-8 visibility;
- terrain, ground, material, world-scale, or collision identity;
- a causal localizer result;
- authoritative retail-executable behavior.

A successful result must be committed and James-accepted before a separate C/L/L/C packet is designed. That later packet requires fresh authorization.

## Offline implementation receipt

- Module: `reimplementation/ablpc/r2e_stable_background.py`.
- Runtime wrapper: `scripts/r2e-run-stable-background-calibration.py`.
- Consumed-run diagnostic: `scripts/r2e-diagnose-consumed-d1.py`.
- Regression suite: `tests/test_r2e_stable_background.py` plus shared R2d/F0/RC0 suites.
- Focused result after James's first replacement-packet audit: 162 passed.
- No EXP-004 runtime arm was launched while preparing the offline packet. The later authorized D1 disposition is recorded below.

## Runtime result - 2026-08-19

The user authorized fresh D1 then D2 under this packet's exact read-only boundary. D1 used the exact derived build and retail Level01 DAT, passed the renderer, Anthill Level01, input, index-read, timing, process, and lifecycle gates, and captured all 121 requested frames. The post-capture observation rejected at frame zero because the live full-frame PNG/RGB did not equal the separately frozen F0 identity. D2 did not launch.

The retained D1 frame zero is PNG `4a5bfde15d2221e3fbe97334856d52cf13e25e99d8fab7c979dc8e921f62f88b` and decoded RGB `b8290da48f462b414857a26c89f0fe1f8486a6ffbaeeb106b04dbba829ab6451`. All three required camera-control crops remained exact across all 121 frames. No runtime/debugger/DAT write, SIGSTOP/SIGCONT, stopped-view read, localizer, candidate, or D2 arm occurred. Cleanup and retail `R:` restoration ended clear. James accepted this rejection and cleanup only.

Two offline diagnostic namespaces were produced because the first completed asynchronously before its initially absent path was rechecked. Their `diagnostic.json` files are byte-identical, SHA-256 `4d54e41a99f729f042dd75bc00c1a4ada464acab9b85ab7938deb4acfe706fef`; both are preserved rather than rewritten. They bind 121 unique full-frame RGB hashes, 78,593 raw changing pixels (`25.58365885416667%`), 92,630 radius-three pixels (`30.152994791666665%`), no exact sampled period, and absence of all four obsolete D2 paths. These are diagnostics over a rejected arm, not an accepted control or mask.

The failure is the protocol's exact full-frame phase requirement, not the camera, renderer, navigation, or capture route. [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] preserves fresh independent controls but uses each new D1's actual first capture as its reference and makes no full-frame phase-equality demand.

## Links

- [[EXP-20260819-003 - R2d Anthill sampled phase calibration]]
- [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC LEVEL DAT static mesh]]
- [[Known Unknowns]]
- [[PC autonomous game control]]
