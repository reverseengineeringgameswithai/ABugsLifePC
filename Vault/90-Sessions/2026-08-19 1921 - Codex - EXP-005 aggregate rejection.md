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

# 2026-08-19 1921 - Codex - EXP-005 aggregate rejection

## Authorized runtime

The user authorized [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] to run fresh D1 then D2 with only one read-only four-byte Level01 index read at `0x00861C84` per arm. No runtime/debugger/DAT writes, SIGSTOP/SIGCONT, localizer, candidate, or C/L/L/C arm was authorized.

The immediate pre-launch audit and git state were clean. The exact argument-free runner completed both controls. D1 and D2 independently retained all six Direct3D markers, `VIDEO MEMORY ONLY`, no software marker, exact derived build and retail DAT, Anthill Level01/index/input chronology, 121 timing-valid frames, three camera-control crops, distinct process identities, and clean lifecycle/restoration receipts. This was definitively the hardware Direct3D route.

## Aggregate rejection

D1's raw mask contained 77,038 pixels and its radius-three mask contained 91,060 (`29.641927083333336%`). D2 produced 233 observations outside that frozen mask. The runner failed closed, quarantined both provisional controls, published no accepted mask, and did not continue to any intervention. The final audit was clear and retail `R:` restored.

Aggregate receipt SHA-256: `ffae8b73194974319495c5e3b9094b92356292634eb8690ab2b01f2f65a3c27e`. James independently accepted the raw procedural rejection and recomputed the counts.

## Offline diagnostic

The durable diagnostic distinguishes 233 observations from 198 unique pixels across five frames and seven components. Inclusive bounds are `x=268..400`, `y=269..332`; the largest component contains 125 pixels. Visual inspection aligns the residual with Flik's animation silhouette, not terrain or a camera-control crop.

Diagnostic SHA-256: `1640615be9df20d640dab77a740ce2221d822dba3c94354616ac3e42f857a283`. The combined D1+D2 design-only mask contains 92,480 radius-three pixels (`30.104166666666664%`), raw-byte SHA-256 `2a07565016efd050129e7d53b9f71942b2503cec8fffc7cbc592e0d619373cb6`, and PNG SHA-256 `ed8f43e54597a6d0f5d25bdd9c381319b1ed62bdededd4a0d28c4a67ff838c50`.

EXP-005 remains rejected and cannot be retroactively widened. At this handoff the next step was offline commitment of a fresh D3 holdout against that exact combined mask; [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] later ran and accepted the mask on one finite grid. Localizer and candidate work remain separate and unauthorized.

## Links

- [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]
- [[PC autonomous game control]]
