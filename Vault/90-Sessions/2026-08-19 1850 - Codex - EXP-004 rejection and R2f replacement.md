---
type: session
date: 2026-08-19
updated: 2026-08-19
agent: Codex
status: complete
tags:
  - reverse-engineering
  - level01
  - terrain
  - runtime
---

# 2026-08-19 1850 - Codex - EXP-004 rejection and R2f replacement

## Authorized runtime disposition

The user explicitly authorized [[EXP-20260819-004 - R2e Anthill stable-background calibration]] to run fresh D1 then D2, including only the read-only four-byte Level01 index read at `0x00861C84`. No runtime/debugger/DAT writes, SIGSTOP/SIGCONT, stopped-view reads, localizer, candidate, or C/L/L/C arm was authorized.

The exact argument-free runner launched D1 after a clean audit. D1 passed build, retail DAT, Direct3D, Anthill Level01, input/index, process, timing, and capture gates and retained all 121 requested 640x480 frames. It then failed closed at the exact full-frame F0 frame-zero comparison. D2 never launched. No accepted mask or intervention was published. Cleanup ended with a clear audit and retail `R:` restored. James accepted the rejection and cleanup only.

## Offline diagnosis

The consumed D1 frame zero is PNG `4a5bfde15d2221e3fbe97334856d52cf13e25e99d8fab7c979dc8e921f62f88b` and RGB `b8290da48f462b414857a26c89f0fe1f8486a6ffbaeeb106b04dbba829ab6451`. All three required camera-control crops remained exact across all 121 frames. The whole-grid diagnostic found 121 unique full-frame hashes, no exact sampled period, 78,593 raw changing pixels, and 92,630 radius-three pixels (`30.152994791666665%`). All old D2 paths were absent.

Two diagnostic directories exist because the first asynchronous run completed before its path was rechecked. Both `diagnostic.json` files are byte-identical at SHA-256 `4d54e41a99f729f042dd75bc00c1a4ada464acab9b85ab7938deb4acfe706fef`; both remain preserved under ignored work evidence. Neither turns D1 into an accepted control.

## Replacement

Created [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]]. It retains fresh two-process controls, the fixed grid and timing receipts, exact camera-control crops, radius-three dilation, 35% cap, and D2 holdout. It removes the falsified predetermined full-frame phase gate: fresh D1's actual first capture becomes its fixed reference without frame hunting or semantic phase claims.

Verifier audit then exposed that the shared packet validator accepted impossible synthetic input timestamps. The common validator now requires positive key-down/key-up order, at least the requested 180 ms interval, non-overlapping Right/Return/Return chronology, and the immediate-before-read identity-guard timestamp strictly between level selection and title Return. Reversed, short, overlapping, and out-of-order receipt regressions cover that boundary; the focused suites passed 187 tests. At that handoff no EXP-005 runtime had occurred; the later consumed result is recorded below. Any localizer remains a separate packet and authorization boundary.

## Links

- [[EXP-20260819-004 - R2e Anthill stable-background calibration]]
- [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]

## Later EXP-005 disposition

EXP-005 was subsequently authorized. D1 and D2 both passed the complete hardware/control lifecycle, but the aggregate rejected on 233 D2 outside-mask observations at 198 unique pixels and published no accepted mask. The residual diagnostic aligns those pixels with Flik's silhouette. A fresh D3 holdout against the frozen combined diagnostic mask is the next offline design boundary; the consumed EXP-005 authorization does not transfer.
