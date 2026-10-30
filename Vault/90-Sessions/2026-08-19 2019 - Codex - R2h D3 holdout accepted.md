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

# 2026-08-19 2019 - Codex - R2h D3 holdout accepted

## Work

Ran the user-authorized D3 arm from [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] through the frozen argument-free runner. The exact auto-hardware build passed the complete Direct3D gate, entered Anthill Level01 through the preregistered input sequence, performed only the authorized read-only four-byte level-index read, captured the fixed 121-frame grid, closed cleanly, and restored retail `R:`.

The fresh process identity was PID/start/process-group `1121774/20272136/1121501`. The accepted result JSON has SHA-256 `3fe541dfd9973ce1238f603e3fafb28834749db7530f2e27db6efb09e2bc0c19` and records zero outside-mask observations, unique pixels, affected frames, components, or bounds. The zero residual-mask PNG is `136af9d0ad549e0c0cee4161ece2ab0e00dfe309a53124729bcaf5956c76fbe1`; the overlay is `2071fdfe8f8a52e15fb9a2ba06bf61e9b097e89ab13dfb429c619ec671808d84` and decodes identically to the frozen D1 reference.

## Boundary

James independently accepted the runtime packet for documentation. The result validates only the preselected nuisance mask on one fresh derived-build finite-grid holdout. [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] remains aggregate-rejected. No cycle, exhaustive coverage, terrain, face visibility, causality, no-effect, or retail-executable claim follows.

No signal, write, localizer, candidate, or C/L/L/C action occurred. A separate offline C/L/L/C protocol, James acceptance, and fresh user authorization are required before any successor runtime.

## Links

- [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]]
- [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC LEVEL DAT static mesh]]
- [[Known Unknowns]]
