---
type: session
date: 2026-09-06
agent: Codex
status: completed
tags: [session, terrain/collision]
---

# 2026-09-06 - Codex - Additive crossing control diagnosis

Continued [[EXP-20260905-009 - Additive terrain preservation and access ramp]] with user approval to correct the probe call/report hash and continue the offline route diagnosis. The live game was not touched.

## Corrections and gates

- Corrected the native command-audit argument to a parsed `LevelDat`, corrected the validation-report hash transcription to the unchanged build receipt, and removed the redundant overridden hash constant. No asset bytes changed.
- Affected tests: 39/39 in 0.31 seconds. Final eleven-file terrain gate: 224/224 in 26.40 seconds, four workers, repo-local scratch and failed-only retention.
- Native rerun `offline-proof-02.json`: seven accepted arms, four retained exact-point failures, zero probe errors, 11.340866 seconds. Command traversal now passes. The original matrix retains exit code 1; failures were not silently converted to passes.

## Discriminating evidence

`work/experiments/EXP-20260905-009/steering-discriminator.json`: twelve native arms in 2.406522 seconds. Original cell 44140's normal is `(-4304,-14070,7206)`. Near the adaptive target, requested `(156,512,-262)` produces `(0,1,0)` actual movement and remains about 305 units short of the 128-unit tolerance. The request is almost normal-directed. Fixed-forward `(0,512,-900)` crosses the same original surface in retail and additive files; lower-downward adaptive diagnostic arms reach the point tolerance. This supports a bounded target-slowdown/settling explanation, not a missing collision cell. Altered-gravity diagnostics are not retail-physics acceptance.

`work/experiments/EXP-20260905-009/through-route-proof.json`: four continuous crossing/return routes pass in 6.072251 seconds. Their criteria were declared before execution: cross Z<=345600 within X=184000..200000, grounded on preserved source-99 collision, with at most two airborne samples and 220 outward steps; aim beyond the crossing while keeping downward input 512 and max horizontal step 900. Return uses the unchanged existing deck-target helper. Three lanes and the restored fall-landing route cross original cell 44140 and return to appended deck cell 48392, without resets between legs; observed airborne runs during crossing/return are at most one sample.

These are separate through-crossing results, not exact-point parking. Keep the failed exact-point controls and their original receipts. No terrain geometry edit or acceptance-threshold relaxation was used to turn them green.

## Handoff

Current public report: `reports/terrain/EXP-20260905-009-validation.json`; build receipt: `reports/terrain/EXP-20260905-009.json`. Isolated game: `work/copies/EXP-20260905-009/game/PC/BUGS`.

Ready for a controlled fresh file-loaded runtime comparison, not universal authoring completion. Runtime must still check rendering, enlarged-batch visibility/sorting, zero depth bias, old/new overlap and full actor/input behavior. No R2q/full suite, Git/stash action, original-file mutation, launch/close, live input or memory access. Previous live-memory authorization was not reused; existing private snapshots were not rewritten.
