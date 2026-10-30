---
type: experiment
id: EXP-20260819-003
status: rejected
date: 2026-08-19
updated: 2026-08-19
result: Authorized D1 captured all 121 frames and rejected on live lower-right crop drift; D2 was not run, no mask was accepted, and the cycle model is superseded by EXP-20260819-004.
question: Can two independent retail-DAT controls establish the same exact sampled decoded-RGB recurrence and validate a bounded D1-only nuisance mask?
environment: PC auto-hardware derived-build route; D1 runtime rejected and cleaned
binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
evidence:
  - reimplementation/ablpc/r2d_phase_calibration.py
  - scripts/r2d-run-phase-calibration.py
  - tests/test_r2d_phase_calibration.py
tags:
  - reverse-engineering
  - pc
  - level01
  - terrain
  - runtime-rejected
---

# EXP-20260819-003 - R2d Anthill sampled phase calibration

> [!failure] Consumed and superseded
> D1-AH-001 is a valid rejected run. D2 is unrun and obsolete. This protocol must not be launched again; see [[EXP-20260819-004 - R2e Anthill stable-background calibration]].

## Question

Can two independent unmodified-Level01 control processes establish the same exact repeated decoded-RGB sequence on a fixed live sampling lattice, and can the first control alone define a bounded nuisance mask that the second control validates without expansion?

This experiment is a prerequisite for another face-8 localizer. It does not test the localizer or the one-byte vertex candidate.

## Historical offline boundary

- This packet is offline and preregistered. No game process was launched while preparing it.
- The earlier authorization for [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]] does not authorize D1/D2.
- Fresh explicit authorization was required and was later granted for this consumed run. It does not authorize reuse or the EXP-004 successor.
- The only planned process-memory access is the inherited, read-only four-byte Level01 index read at `0x00861C84` before the title Return. D1/D2 perform no runtime write, debugger write, DAT write, SIGSTOP/SIGCONT, or stopped-view-block read.
- The runner ends after control validation and mask analysis. It has no localizer or candidate launch path.

## Frozen identities

- Executed auto-hardware image: SHA-256 `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
- Retail transform source: SHA-256 `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Retail Anthill Level01 DAT: SHA-256 `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
- D1 stage/evidence: `D1-auto-hardware-retail-001` / `D1-AH-001` beneath `work/copies/EXP-20260819-003/`.
- D2 stage/evidence: `D2-auto-hardware-retail-001` / `D2-AH-001` beneath the same ignored work root.
- Accepted, rejected, and pending namespaces must be initially absent at their exact final paths. A cleanup failure remains pending.
- Each arm's lifecycle acceptance is provisional until independent packet validation and the complete two-arm analysis pass. The aggregate result requires distinct `(PID, start_ticks)` process identities and retains each process-group ID separately as launch provenance. Matching PID/start-ticks rejects the packet even if the PGIDs differ.

The source, exact executable transform and inverse-to-retail proof, cache, DAT, CD sentinel, prefix `R:` mapping, process identity, cwd, main window, six-marker Direct3D path, Level01 log/title/index gates, input receipts, and pre/post lifecycle audits are inherited from the accepted auto-hardware F0 executor. Every identity is rechecked per process.

## Fixed two-control procedure

1. Require a clean `make session-audit`, retail baseline `R:` mapping, and initially absent D1 namespaces.
2. Launch D1 through the exact `play-pristine.sh --auto-hardware` derived-build route and satisfy the complete six-marker Direct3D gate with no software or mixed terminal marker.
3. Use the frozen Right, Return, Return navigation to Anthill Level01. Define `t0` as key-up of the title-screen Return. Send no input after `t0`.
4. Capture 121 live compositor frames at `t0 + 3.300 + 0.200*i` seconds for `i=0..120`. Do not stop the process.
5. Require every request to start within `0.005 s` of its target, the compositor file to stabilize by target plus `0.150 s`, and hashing to complete by target plus `0.180 s`. Requests may not overlap. Retain request, command-return, file-stable, and hash timestamps plus every PNG/RGB hash and structural-crop hash.
6. Close D1 normally through the inherited fail-closed lifecycle and require a clear post-close audit and restored retail `R:` before classification.
7. Independently repeat the exact procedure in a fresh D2 process and namespace. D1 cannot be reused as D2.
8. Validate each retained control packet independently before cycle or mask analysis.

The grid spans `24.000 s`, from `t0+3.300` through `t0+27.300`. There is no adaptive extension, frame hunting, phase rotation, image registration, normalization, optical flow, or evidence-selected cadence.

## Exact sampled-period gate

For each arm, find the smallest integer `P` in `2..60` such that:

```text
RGB[i] == RGB[i + P] for every 0 <= i < 121 - P
```

The arm must also satisfy `121 >= 2P + 1`, so the retained grid contains at least two complete repeated periods plus the repeated start sample. D1 and D2 must independently yield the same smallest `P`, with index zero as the fixed phase origin. Endpoint equality or one repeated segment is insufficient.

This gate can establish only an exact recurrence on the specified 0.200-second sampled lattice. It does not prove a continuous-time or native animation period. If no exact period exists, the periods disagree, or either packet fails, the result is `cycle-not-established` and no accepted nuisance mask is published.

## One-way nuisance-mask construction

1. Use only D1 samples `0..P-1` to mark each pixel whose decoded RGB is not constant across that first period.
2. Require the raw mask to contain at least one pixel.
3. Dilate the raw mask by a clipped square/Chebyshev radius of exactly three pixels.
4. Reject if the dilated mask covers more than 25% of the 640x480 frame.
5. Require every later D1 sample outside the dilated mask to equal D1's first-period sample at phase `i mod P`.
6. Without expanding or changing the mask, require every D2 sample outside it to equal D1's first-period sample at phase `i mod P`.

Only a complete pass may publish an accepted mask, overlay, component receipt, exact control reference sequence, period, and eligible comparison region. D2 can validate or reject the D1 mask; it can never add pixels to it. Localizer and candidate frames are prohibited from period or mask selection.

Every live capture and observation first receives an atomic attempt receipt. Capture-command, timing, file-stability, hashing, PNG decode, region analysis, or view-gate failure updates the retained receipt with the exact rejected disposition before raising. The executor and independent validator both require `started <= command-returned <= file-stable <= target+0.150` and `file-stable <= hash-computed <= target+0.180`; nested compositor timestamps must equal their top-level receipt fields. Pre/post audit validation requires the exact empty `game-session` audit structure, not only a `clean: true` field.

If D1 or D2 execution, independent validation, process-independence comparison, or aggregate mask analysis fails, any provisionally accepted control is moved to the rejected namespace and no accepted mask survives. If cleanup or retail-mapping restoration is unclear, the affected arm and aggregate result remain pending instead.

## Outcome table

| Observation | Result | Next action |
|---|---|---|
| Both control packets valid; same exact sampled `P`; raw/dilated mask and all holdouts pass | `accepted-sampled-phase-mask` | Commit evidence/result and obtain James acceptance before designing any C/L/L/C runtime packet |
| No qualifying exact recurrence in either arm | `cycle-not-established` | Publish no accepted mask; a new committed and authorized design is required |
| Different D1/D2 periods | `cycle-not-established` | Publish no accepted mask |
| Unknown dimensions, timing miss, overlap, view drift, identity/log/input/lifecycle failure | `control-packet-rejected` | Publish no accepted mask |
| Zero raw variability or mask coverage above 25% | `mask-rejected` | Publish no accepted mask |
| D1 later-period or D2 outside-mask mismatch | `mask-rejected` | Publish no accepted mask and do not expand it |
| Cleanup or retail-mapping restoration unclear | pending | Stop; retain the packet in pending and resolve lifecycle state |

## Offline implementation receipt

- Protocol module: `reimplementation/ablpc/r2d_phase_calibration.py`.
- Argument-free wrapper: `scripts/r2d-run-phase-calibration.py`.
- Regression suite: `tests/test_r2d_phase_calibration.py`.
- Focused result after James's second audit corrections: 145 passed.
- The implementation permits repeated image hashes but rejects a non-repeating sequence. Frozen duplicates are not counted as independent controls because both controls must be separate processes.

## Claims not made

- No sampled cycle or nuisance mask is currently established.
- No localizer face is shown in view.
- Face 8 is not confirmed as terrain, ground, or retail-visible geometry.
- No result is transported from the auto-hardware derived executable to authoritative retail behavior.
- The R2c localizer and one-byte candidate remain inconclusive, not negative.

## Links

- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC LEVEL DAT static mesh]]
- [[EXP-20260819-001 - R2b Anthill static mesh causal runtime]]
- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[Known Unknowns]]
- [[PC autonomous game control]]

## Runtime result - 2026-08-19

The user authorized this exact packet. D1 used the exact derived build and retail Level01 DAT, entered Anthill Level01 through the frozen input/read boundary, and acquired all 121 live frames within timing limits. The post-capture observation gate rejected frame 1 because `lower-right-structure` changed while the other three pinned crops remained exact. D2 did not launch; no signal/write/localizer/candidate occurred; no accepted mask was published; cleanup and retail `R:` restoration ended clear.

James accepted the rejection and cleanup only. A machine diagnostic bound all 121 frames and found 121 unique RGB hashes, no exact sampled period, three invariant crops, six lower-right hashes, 76,807 raw variable pixels, and 90,913 radius-three pixels. The corrected receipt also verifies absence of all exact old-D2 paths. Receipt SHA-256: `d17eeda40826280448196a78770d7e1434db6d1ba92b805114597c42b2ad4583`.

The accepted-path validator also had a latent namespace defect: raw receipts correctly named pending acquisition paths, while the validator expected accepted paths after classification. That is corrected and regression-covered for the successor. This rejected run is preserved unchanged and is not an accepted control.
