---
type: session
date: 2026-08-16
agent: James
status: accepted
tags: [session, re/audit, re/static, re/collision]
---

# Independent terrain height audit

## Goal

Treat EXP-141's engine-faithful terrain-height and standoff packet as
hypotheses and independently attack every claim from a fresh context:
rehash, independent disassembly of the complete pipeline, line-by-line
reimplementation review, receipt and standoff reruns, a scratchpad-only
tamper test, hygiene gates, and overclaim review — with no runtime
process and no target write.

## Work completed

- Re-read the startup authority chain, the 2026-08-15/16 grain-gate and
  terrain-height sections of Current State, EXP-129/130/131/136/137/139/
  140/141, the collision-source and implementation notes, KU-060/061,
  and the six function dossiers.
- Rehashed `bugs.exe` (`97c95ba5...27b878`) and both `TERRAIN.ALL`
  files to their pinned digests; confirmed `.text` `VA - 0x400C00` from
  the PE section table and all three thunk targets.
- Independently disassembled and re-verified the reset consumer
  (`0x00432930`), collector (`0x004AC460`), resolver (`0x004ACA60`,
  including both winding edge orders from the raw push sequences, the
  exact plane formula, both tie-breaks, and the `0x004ACD27` final
  selection with the `0x5BD826` sign test), edge test (`0x004A9290`,
  pass epilogue bytes `66 b8 01 00` at file `0xA87BD`), loader clone
  branch, bounds pass, and bucket builder.
- Attacked the bucket-order equivalence argument specifically: proved
  the bucket unions are group-header-derived while phase-2 boxes are
  cell-derived (so one written premise is false in general), derived the
  window-arithmetic argument that actually closes the gap, and scanned
  both files exhaustively — zero cell-window protrusions below group
  minima, so the accepted cell sets are provably identical here.
- Found the engine's unmodeled `+0x10 >= 0x100` loader branch and the
  `eb fe` self-loop trap at `0x004A865B` behind the unregistered-clone
  branch; proved both unexercised/inert for the two audited files;
  corrected the [[FUNC-97C95BA5572D-004A8410]] "skipped" wording in
  place.
- Reran all four receipt queries (30092 exact on descriptor 552;
  +123/+121/+126 settle deltas), verified 30092's engine-reset
  provenance in EXP-116/117, and the descriptor-572 pit orientation
  check at rest 64032.
- Reran the standoff tool twice (byte-identical), matched all twelve
  chosen candidates and spreads against the packet table, verified
  centers against EXP-136/139, and tamper-tested the hash refusal on a
  scratchpad copy only.
- Reran the focused suite (14 passed) and `make check` (Vault 410/0/0,
  M4 anchors valid, 610 tests, tracked audit 0, `git diff --check`
  clean); confirmed no new `dynamic/` receipts and no packet runtime
  processes (three pre-packet `winedevice.exe` stubs noted as
  prior-session residue).

## Verdict

**ACCEPT** at the boundary recorded in
[[EXP-20260816-142 - Independent terrain height and standoff audit]]:
engine-faithful at the height-query interface for the two audited retail
terrain files, four receipt cross-checks, downward Y, KU-061 recording,
and twelve deterministic static standoff candidates with T3/C0 proven
points preferred. Three latent gaps and minor wording items are recorded
for the worker's reconciliation; none changes a validated result.

## Next steps

- Worker reconciles Current State / Known Unknowns with the verdict and
  tightens the recorded wording items (equivalence premise, standoff
  "above/higher" versus "deeper", the `+0x10 >= 0x100` boundary note).
- The guarded teleport-and-view runtime session (KU-060 mapping pass)
  remains the next evidence arm; KU-061's one-read live discriminator
  stays open.
