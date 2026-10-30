---
type: session
date: 2026-08-19
updated: 2026-08-19
agent: Codex
status: complete
tags: [reverse-engineering, level01, terrain, offline]
---

# 2026-08-19 2359 - Codex - EXP-008 mask and D4 packet

## Work

Completed the offline C1/C2-only diagnostic in
[[EXP-20260819-008 - R2j Anthill control-trained successor mask]] and froze the
argument-free, unauthorized D4 packet in
[[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]]. No game or
mutation operation ran.

## Result

The proposal contains 93,445 pixels (`30.418294270833335%`), adds 965 pixels,
and leaves 213,755 eligible. Diagnostic SHA-256 is `83931a8a...9a5`; mask
PNG/raw-byte hashes are `b855df0a...c936` and `9ff27caa...1ba`. James
independently reproduced and accepted the offline artifact only. D4 remains
unauthorized and unrun.

## Boundary

This advances renderer-nuisance discrimination toward another visible-terrain
test. It establishes no terrain, face-8, causal, no-effect, or collision claim.
EXP-007 remains inconclusive and retail R2 remains open.

## Links

- [[EXP-20260819-008 - R2j Anthill control-trained successor mask]]
- [[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]
