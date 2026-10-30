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
  - offline
---

# 2026-08-19 1943 - Codex - R2h D3 holdout packet

## Work

Prepared [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] as the offline successor to the accepted EXP-005 procedural rejection. The argument-free runner freezes the exact diagnostic, binary combined mask, D1 reference, prior D1/D2 process identities, one fresh D3 stage/evidence identity, and the existing auto-hardware/Level01/grid/crop/lifecycle gates.

D3 must differ from both prior process identities and may not expand or select the mask. The real analyzer binds each frame's PNG and decoded RGB to the control packet before and after comparison, then retains observation/unique-pixel/frame/component/bounds data plus a residual mask and overlay on success or rejection. Cleanup, quarantine, or publication uncertainty stays pending. The code has no localizer, candidate, signal, or write continuation.

## Offline evidence

The source preflight reproduced diagnostic SHA-256 `1640615be9df20d640dab77a740ce2221d822dba3c94354616ac3e42f857a283`, mask PNG `ed8f43e54597a6d0f5d25bdd9c381319b1ed62bdededd4a0d28c4a67ff838c50`, decoded mask bytes `2a07565016efd050129e7d53b9f71942b2503cec8fffc7cbc592e0d619373cb6`, 92,480 selected pixels, D1 reference PNG/RGB, prior process identities, and all seven fresh path absences.

The focused R2h/R2g/R2f/R2e/R2d suites passed 113 tests after the fail-closed PNG/RGB frame-binding, publication, and production-schema integration regressions. No EXP-006 runtime path, process-memory read, signal, write, DAT, localizer, or candidate occurred during this offline session. At that point fresh explicit authorization was required after commit and James acceptance; it was later granted and consumed by [[2026-08-19 2019 - Codex - R2h D3 holdout accepted]].

The shared production control validator now returns the recomputed PNG hash array it already verifies. A real retained EXP-005 control packet flows through that validator into the real D3 analyzer in regression coverage, preventing synthetic packet fixtures from masking schema drift.

## Links

- [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]]
- [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]
