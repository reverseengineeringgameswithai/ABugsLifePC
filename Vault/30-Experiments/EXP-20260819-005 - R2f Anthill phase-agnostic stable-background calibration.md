---
type: experiment
id: EXP-20260819-005
status: rejected
date: 2026-08-19
updated: 2026-08-19
result: Authorized D1/D2 controls were procedurally valid, but D2 had 233 observations at 198 unique pixels outside D1's mask; the aggregate rejected and published no accepted mask.
question: Can two fresh retail-DAT controls validate a bounded 24-second stable-background mask without requiring a predetermined full-frame animation phase?
environment: PC auto-hardware derived-build route; D1/D2 runtime completed, aggregate rejected, cleanup clear
binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
evidence:
  - reimplementation/ablpc/r2f_phase_agnostic_background.py
  - scripts/r2f-run-phase-agnostic-background.py
  - scripts/r2f-diagnose-consumed-d1.py
  - tests/test_r2f_phase_agnostic_background.py
  - reimplementation/ablpc/r2g_exp005_diagnostic.py
  - scripts/r2g-diagnose-exp005-controls.py
  - tests/test_r2g_exp005_diagnostic.py
tags:
  - reverse-engineering
  - pc
  - level01
  - terrain
  - runtime-rejected
---

# EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration

> [!failure] Consumed aggregate rejection
> `D1-PA-SB-AH-001` and `D2-PA-SB-AH-001` each passed their complete hardware/control lifecycle, but the frozen D1 mask failed the independent D2 holdout at 233 frame-pixel observations. Both controls were quarantined, no accepted mask was published, and this protocol must not be rerun or widened post hoc.

## Question

Can a fresh D1 process define a bounded finite variability mask relative to its own first sampled frame, and can a separate D2 process reproduce every unmasked D1-reference pixel exactly without requiring either process to begin at a preselected full-frame animation phase?

This is a control-only prerequisite for a future face-8 localizer. It does not create a DAT, run a localizer, test the one-byte vertex candidate, or establish terrain identity.

## Authorization boundary

- The user explicitly authorized this packet after its committed James acceptance. That authorization was consumed by D1 and D2 and does not authorize a retry, D3, localizer, or candidate.
- `scripts/r2f-run-phase-agnostic-background.py` must not launch again; its stage/evidence identities are consumed.
- The only planned process-memory access is one read-only four-byte Level01 index read at `0x00861C84` before title Return in each arm.
- No runtime/debugger/DAT write, SIGSTOP/SIGCONT, stopped-view read, localizer, candidate, or C/L/L/C arm is authorized or reachable.

## Why EXP-004 was replaced

[[EXP-20260819-004 - R2e Anthill stable-background calibration]] captured its complete 121-frame D1 grid but rejected because frame zero did not equal a full-frame F0 image from a different live-animation phase. The three camera-control crops remained exact throughout the grid. The retained evidence therefore falsifies exact full-frame phase equality as a camera-readiness gate while supporting the narrower crop gates.

The consumed-run diagnostic found 78,593 raw changing pixels and 92,630 pixels after radius-three dilation, or `30.152994791666665%` of the frame. It also found 121 unique full-frame RGB hashes and no exact sampled period. The two preserved diagnostic receipts are byte-identical at SHA-256 `4d54e41a99f729f042dd75bc00c1a4ada464acab9b85ab7938deb4acfe706fef`. They are design diagnostics over rejected evidence, not an accepted mask or independent support.

## Historical frozen identities

- Executed auto-hardware image: SHA-256 `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
- Retail Anthill Level01 DAT: SHA-256 `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
- D1 stage/evidence: `D1-phase-agnostic-stable-retail-001` / `D1-PA-SB-AH-001` beneath ignored `work/copies/EXP-20260819-005/`.
- D2 stage/evidence: `D2-phase-agnostic-stable-retail-001` / `D2-PA-SB-AH-001` beneath the same root.
- Aggregate identity: `phase-agnostic-stable-background-mask-001`.
- Every stage, pending, accepted, rejected, and aggregate final path must be initially absent.
- EXP-004's old D2 identity is unrun-obsolete and must never launch.

## Historical camera and acquisition gates

There is deliberately no exact full-frame F0 PNG/RGB gate. D1's actual captured frame zero becomes the fixed comparison reference only after the arm passes its independent identity, renderer, level, timing, and crop gates. It is not selected for favorable animation phase and has no phase or semantic meaning.

Every one of each arm's 121 frames must reproduce these exact decoded-RGB camera-control crops:

| Region | Rectangle `(x,y,w,h)` | Decoded-RGB SHA-256 |
|---|---|---|
| `upper-right-structure` | `(480,0,160,100)` | `41aa36449cae7e735d5476644f670d01eb931490484d22091da1647ad1852bf6` |
| `left-middle-structure` | `(20,220,120,100)` | `7a87a57c278e09861fada1511c7aac9dd10cfe607d109fb6b48696103998ab14` |
| `lower-left-structure` | `(0,380,160,100)` | `59e3593b7b487553a63483cf20134aef9be97dae6b73690e5f5ababa8e1541e0` |

The lower-right `(480,380,160,100)` crop is excluded because both earlier consumed controls show temporal content there. It is neither a camera invariant nor renderer selector.

For each fresh process:

1. Require a clean pre-launch audit, retail baseline `R:`, exact source/cache/DAT/CD identities, and fresh namespaces.
2. Launch only the exact `play-pristine.sh --auto-hardware` route; require all six Direct3D markers and no software/mixed terminal marker.
3. Use the frozen Right, Return, Return sequence to Anthill Level01. Each receipt must prove positive key-down/key-up order and at least the requested `0.180 s` interval; the three inputs must be non-overlapping and chronological. The authorized index read's immediate identity-guard timestamp must fall after level-select Return key-up and before title-Return key-down. Define `t0` as the validated title-Return key-up and send no later input.
4. Capture 121 live 640x480 compositor frames at `t0 + 3.300 + 0.200*i`, `i=0..120`, through `t0+27.300`.
5. Require request-start error at most `0.005 s`, file stability by target plus `0.150 s`, hashing by target plus `0.180 s`, no request overlap, and atomic attempt/result receipts.
6. Require the three camera-control crops in every frame, exact process/build/DAT/window identity before and after the grid, and a clean post-close audit with retail `R:` restored.
7. Treat a clean arm as provisional until independent packet validation and aggregate D1/D2 analysis pass.

Acquisition receipts retain their immutable pending paths; post-lifecycle validation resolves the corresponding classified files without rewriting historical commands.

## Historical D1 finite mask

1. Use D1's actual frame zero as the fixed reference.
2. Across all 121 D1 captures, mark the union of every exact decoded-RGB inequality against that reference.
3. Require at least one marked pixel.
4. Dilate with a clipped Chebyshev square of radius exactly three pixels.
5. Require dilated coverage at or below exactly 35% of 307,200 pixels.

This makes every sampled D1 pixel outside the mask equal to D1 frame zero by construction. It is not an independent D1 holdout. No cycle detection, phase rotation, full-frame reference matching, frame hunting, normalization, registration, optical flow, or adaptive extension occurs.

## Historical independent D2 holdout

- D2 runs in a fresh process and namespace with a distinct `(PID, start_ticks)` identity.
- Compute D2's own whole-grid variability for diagnosis, but never add it to or expand the D1 mask.
- Compare every unmasked pixel of every D2 frame against D1's actual frame zero.
- Require exactly zero outside-mask mismatches.
- D2's own frame zero is not a selectable reference and cannot change D1's mask.

## Historical outcomes and claim ceiling

| Observation | Disposition |
|---|---|
| Both control packets validate; D1's nonzero dilated mask is at most 35%; D2 has zero outside-mask mismatches | `accepted-phase-agnostic-stable-background-mask` |
| D1 mask is zero/over cap or D2 has any outside-mask mismatch | `stable-background-mask-rejected` |
| Identity, renderer, level, timing, crop, receipt, or lifecycle gate fails | `control-packet-rejected` |
| Cleanup or retail mapping restoration is unclear | pending |

Any failure quarantines provisional controls and publishes no accepted mask. A success establishes only an exact-view/build, finite 24-second sampled stable-background mask for the derived executable. It does not establish a cycle, exhaustive nuisance coverage, face-8 visibility, terrain/ground/material/world-scale/collision identity, causality, or authoritative retail-executable behavior.

A successful result must be documented, committed, and James-accepted before designing a separate C/L/L/C localizer packet. That later packet requires fresh authorization.

## Offline implementation receipt

- Module: `reimplementation/ablpc/r2f_phase_agnostic_background.py`.
- Argument-free runtime wrapper: `scripts/r2f-run-phase-agnostic-background.py`.
- Consumed EXP-004 D1 diagnostic: `scripts/r2f-diagnose-consumed-d1.py`.
- Regression suite: `tests/test_r2f_phase_agnostic_background.py` plus the shared R2e/R2d/F0/RC0 suites.
- Focused offline result after verifier-requested validator, analyzer, and chronology regressions: 187 passed.
- No EXP-005 runtime arm, signal, process-memory access, DAT creation, or intervention occurred while preparing the offline packet. The later authorized runtime is recorded below.

## Runtime result - 2026-08-19

The exact argument-free runner launched D1 and then D2 under the user's narrow authorization. Both arms independently passed:

- executed auto-hardware build `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`;
- retail Level01 DAT `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`;
- all six Direct3D markers, including `VIDEO MEMORY ONLY` and `INIT : Starting Direct3D renderer`, with no software marker;
- Anthill Level01, exact chronological Right/Return/Return receipts, and only the authorized read-only `(0x00861C84,4)` index read returning `1`;
- 121 unique-path, non-overlapping, timing-valid 640x480 captures with all three camera-control crops exact;
- distinct process identities: D1 `(PID 1072590, start 19909757)` and D2 `(PID 1073849, start 19920889)`;
- clear per-arm/final audits and restored retail `R:`.

No runtime/debugger/DAT write, SIGSTOP/SIGCONT, localizer, candidate, or C/L/L/C action occurred. This directly confirms that both arms used the hardware Direct3D route; the rejection is not a renderer or launch failure.

D1 produced 77,038 raw changing pixels and 91,060 radius-three pixels (`29.641927083333336%`), below the frozen 35% cap. D2 then produced 233 outside-mask frame-pixel observations. The aggregate correctly returned `stable-background-mask-rejected`, quarantined both provisional controls, and published no accepted mask. Aggregate receipt SHA-256: `ffae8b73194974319495c5e3b9094b92356292634eb8690ab2b01f2f65a3c27e`.

## Offline residual diagnostic

The argument-free offline diagnostic at ignored path `work/copies/EXP-20260819-005/evidence/calibration/rejected/phase-agnostic-stable-background-mask-001/offline-diagnostic-001/diagnostic.json` is SHA-256 `1640615be9df20d640dab77a740ce2221d822dba3c94354616ac3e42f857a283`. It binds both quarantined packets and distinguishes:

- 233 mismatch observations across five D2 frames;
- 198 unique pixels in seven 8-connected components;
- inclusive residual bounds `x=268..400`, `y=269..332`;
- largest component 125 pixels;
- a residual overlay visually aligned with Flik's animation silhouette, not terrain or any camera-control crop;
- a combined D1+D2 diagnostic union of 78,838 raw pixels and 92,480 radius-three pixels (`30.104166666666664%`).

The combined mask's raw-byte SHA-256 is `2a07565016efd050129e7d53b9f71942b2503cec8fffc7cbc592e0d619373cb6`; its PNG SHA-256 is `ed8f43e54597a6d0f5d25bdd9c381319b1ed62bdededd4a0d28c4a67ff838c50`. This mask is post-EXP-005 training/design evidence only. It does not retroactively accept EXP-005 and cannot be expanded by a future treatment or holdout.

## Result boundary and next action

The 233 observations do not establish camera instability, terrain behavior, face-8 visibility, causal effect, or retail-executable behavior. R2 remains open. The localizer and one-byte candidate remain unauthorized.

The separately committed [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] later ran against the exact combined diagnostic mask above and accepted it on one finite grid without expansion or selection from D3. EXP-005 remains aggregate-rejected. Any later localizer remains another separate packet and authorization boundary.

## Links

- [[EXP-20260819-004 - R2e Anthill stable-background calibration]]
- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC LEVEL DAT static mesh]]
- [[Known Unknowns]]
- [[PC autonomous game control]]
