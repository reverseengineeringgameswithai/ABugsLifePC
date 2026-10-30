---
type: session
date: 2026-08-19
updated: 2026-08-19
agent: Codex
status: complete
tags: [reverse-engineering, level01, terrain, runtime]
---

# 2026-08-19 2359 - Codex - EXP-009 D4 holdout accepted

## Work

Ran [[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]] under the
user's exact authorization. The argument-free executor used retail Level01 DAT,
the accepted auto-hardware build, one fresh process, the fixed 121-frame grid,
and only the read-only four-byte Level01 index read.

## Result

Process `1267141/21477936/1266881` passed renderer, Level01, input, crop, timing,
frame-binding, lifecycle, and retail-`R:` restoration gates. All 121 frames had
zero observations and zero unique pixels outside the fixed 93,445-pixel mask.
Result SHA-256 is `bf2b4625...69d8`; disposition SHA-256 is
`cc4fdc2c...e1ebe`. James independently reproduced and accepted the result.

## Boundary

The authorization is consumed. No write, signal, localizer, candidate, or
successor ran. This accepts one finite derived-build/view/grid control holdout,
not exhaustive coverage, terrain/ground identity, face-8 visibility, causality,
no effect, collision, or retail-executable behavior.

## Links

- [[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]]
- [[EXP-20260819-008 - R2j Anthill control-trained successor mask]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]
