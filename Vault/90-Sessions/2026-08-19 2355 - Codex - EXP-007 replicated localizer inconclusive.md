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

# 2026-08-19 2355 - Codex - EXP-007 replicated localizer inconclusive

## Work

Ran [[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] under the user's exact authorization. The creator made two independently derived, byte-identical guarded face-8 DATs at SHA-256 `9942e252...11bfd`. Fresh `C1/L1/L2/C2` processes each passed the auto-hardware Direct3D, Anthill Level01 index `1`, exact 121-frame grid, permitted-input/read, cleanup, and retail-`R:` restoration gates.

## Result

Aggregate result SHA-256 `723e03ed43d6133e65df25655954ba779767800b3b010f603a0b2d482e25a309` is inconclusive. Controls had 251 outside-mask mismatches; L1/L2 had 228 disagreements; intersection and static core were zero. L1 had no outside-mask difference. L2's only difference was 228 pixels at frame 35, exactly reproduced by C2 frame 35 in positions and RGB. The EXP-006 mask is not exhaustive across fresh controls.

All arms were quarantined only at the aggregate scientific gate. No runtime/debugger write, signal, candidate, or successor arm occurred. Final and independent audits were clean. James accepted the procedure and inconclusive interpretation only.

## Boundary

No face-8 visibility, terrain, causal, or no-effect claim is supported. R2 remains open, the authorization is consumed, and the one-byte candidate remains unauthorized. A mask revision must begin as offline control-only analysis and later pass a fresh authorized holdout; it cannot retroactively rescue EXP-007.

## Links

- [[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]]
- [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC LEVEL DAT static mesh]]
- [[Known Unknowns]]
