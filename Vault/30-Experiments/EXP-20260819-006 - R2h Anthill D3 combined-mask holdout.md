---
type: experiment
id: EXP-20260819-006
status: complete
date: 2026-08-19
updated: 2026-08-19
result: Accepted finite-grid D3 holdout; zero observations outside the frozen combined mask across all 121 frames.
question: Can one fresh independent D3 control reproduce every pixel outside the frozen EXP-005 combined diagnostic mask without expanding that mask?
environment: PC auto-hardware derived-build route; authorized D3 runtime complete
binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
evidence:
  - reimplementation/ablpc/r2h_d3_combined_holdout.py
  - scripts/r2h-run-d3-combined-holdout.py
  - tests/test_r2h_d3_combined_holdout.py
  - reimplementation/ablpc/r2g_exp005_diagnostic.py
  - work/copies/EXP-20260819-006/evidence/accepted/D3-CM-SB-AH-001/disposition.json
  - work/copies/EXP-20260819-006/evidence/holdout/accepted/combined-mask-d3-holdout-001/result.json
tags:
  - reverse-engineering
  - pc
  - level01
  - terrain
  - runtime
---

# EXP-20260819-006 - R2h Anthill D3 combined-mask holdout

## Question

Can one fresh D3 process independently reproduce every sampled pixel outside the already frozen EXP-005 combined D1+D2 diagnostic mask, without selecting, widening, or regenerating that mask from D3?

This is a control-only prerequisite for later localizer design. It does not create or modify a DAT and cannot launch a localizer, candidate, or C/L/L/C arm.

## Authorization boundary

- The user explicitly authorized one frozen EXP-006 D3 run after the offline packet and James audit were complete. That authorization was consumed by the accepted run documented below and does not authorize a rerun or successor.
- The only process-memory access was one read-only four-byte Level01 index read at `0x00861C84` before title Return.
- No runtime/debugger/DAT write, SIGSTOP/SIGCONT, stopped-view read, localizer, candidate, or C/L/L/C arm was authorized or reached.
- The wrapper is argument-free. Operator-supplied paths, hashes, mask choices, or thresholds are rejected.

## Frozen source evidence

The runner must validate all source evidence before creating a stage and again during analysis:

| Item | Frozen identity |
|---|---|
| EXP-005 offline diagnostic JSON | SHA-256 `1640615be9df20d640dab77a740ce2221d822dba3c94354616ac3e42f857a283` |
| Combined radius-three mask PNG | SHA-256 `ed8f43e54597a6d0f5d25bdd9c381319b1ed62bdededd4a0d28c4a67ff838c50` |
| Decoded binary mask bytes | SHA-256 `2a07565016efd050129e7d53b9f71942b2503cec8fffc7cbc592e0d619373cb6` |
| Exact mask population | 92,480 of 307,200 pixels (`30.104166666666664%`) |
| D1 reference PNG | SHA-256 `05f5691cab126962715d94857fd5085f7013353b3982a7d6e9d350215506ad1c` |
| D1 reference decoded RGB | SHA-256 `2ea6564339c406cbcd92ca32faaf4e6c1b177119939aee569f0cfc1223b9d26c` |
| D1 process identity | PID/start `1072590/19909757` |
| D2 process identity | PID/start `1073849/19920889` |

The mask decoder requires canonical nonsymlink 640x480 binary pixels, exactly 92,480 selected pixels, and both exact PNG and decoded-byte hashes. The D1 reference independently requires its canonical path, dimensions, PNG hash, and decoded-RGB hash. The source diagnostic must continue to label EXP-005 aggregate-rejected and the combined mask design/training evidence only.

## Fresh identities

- Experiment root: ignored `work/copies/EXP-20260819-006/`.
- D3 stage: `D3-combined-mask-holdout-retail-001`.
- D3 evidence: `D3-CM-SB-AH-001` under pending/accepted/rejected namespaces.
- Holdout result: `combined-mask-d3-holdout-001` under separate pending/accepted/rejected namespaces.
- All seven exact stage/evidence/result paths must be initially absent.
- D3's `(PID,start_ticks)` must differ from both frozen EXP-005 controls.

## Frozen D3 acquisition

1. Require a clean immediate pre-launch audit, retail baseline `R:`, exact source/cache/DAT/CD identities, fresh paths, and the complete frozen-source preflight above.
2. Launch only `play-pristine.sh --auto-hardware`; require all six Direct3D markers, `VIDEO MEMORY ONLY`, 640x480, and no software/mixed terminal marker.
3. Use exact chronological Right, Return, Return navigation to Anthill Level01. Each key receipt must prove at least the requested `0.180 s` interval and no overlap. The authorized index-read guard must occur after level-select key-up and before title-Return key-down.
4. Define `t0` as validated title-Return key-up. Send no later input.
5. Capture 121 live compositor frames at `t0 + 3.300 + 0.200*i`, `i=0..120`, with the existing request-start, file-stability, hash, uniqueness, and no-overlap limits.
6. Require the same three exact camera-control crops in every frame. There is no full-frame phase-reference gate.
7. Require exact process/build/DAT/window identity before and after the grid, clear close/audit/restoration, and a D3 process identity distinct from D1 and D2.

Acquisition receipts keep their immutable pending paths. Post-close validation resolves classified files without rewriting historical commands. Cleanup, quarantine, or atomic-publication uncertainty stays pending and cannot publish a result.

## Fixed holdout analysis

1. Revalidate the diagnostic, mask, D1 reference, and their exact hashes immediately before analysis.
2. Decode the fixed mask only from its canonical binary PNG and verify its decoded-byte hash/population.
3. Bind every D3 frame to the control packet's exact PNG and decoded-RGB hashes before comparison, compare every decoded-RGB pixel to the frozen D1 reference while skipping only the 92,480 preselected mask pixels, then reopen and rehash both representations before publication.
4. Record mismatch observations, unique pixels, affected frame indices/counts, 8-connected components, and inclusive bounds.
5. Always retain `d3-outside-frozen-mask-unique.png` and `d3-residual-overlay-on-d1-reference.png`, including zero-valued success evidence.
6. Revalidate all frozen sources after analysis. D3 cannot add a pixel, alter a hash, select another reference, normalize, register, rotate phase, hunt frames, or extend the grid.

## Outcomes

| Observation | Disposition |
|---|---|
| D3 packet validates and has exactly zero outside-mask observations | `accepted-combined-mask-d3-holdout` |
| D3 has one or more outside-mask observations | `combined-mask-d3-holdout-rejected`; quarantine D3, retain residual evidence, publish no accepted reference |
| Identity, renderer, level, chronology/read, timing, crop, provenance, or analyzer gate fails | `control-packet-rejected`; quarantine D3 |
| Cleanup or retail `R:` restoration is unclear | pending |

## Accepted-claim ceiling

A success establishes only that one independent fresh D3 process reproduced every unmasked pixel on the exact 121-point, 24-second grid under build `1e1d...c41f`, the pinned view, and the frozen combined mask. It does not:

- retroactively accept EXP-005;
- establish an animation cycle or exhaustive nuisance coverage;
- prove face-8 visibility, terrain, ground, material, world-scale, or collision identity;
- establish a causal localizer result or authoritative retail-executable behavior;
- authorize a localizer or weaken the later requirement for fresh bracketed controls.

Any accepted D3 result must be documented, committed, and James-accepted before designing a separate C/L/L/C localizer packet. That later packet requires fresh authorization.

## Offline implementation receipt

- Module: `reimplementation/ablpc/r2h_d3_combined_holdout.py`.
- Argument-free wrapper: `scripts/r2h-run-d3-combined-holdout.py`.
- Regression suite: `tests/test_r2h_d3_combined_holdout.py` plus shared R2g/R2f/R2e/R2d suites.
- The shared production control validator returns its recomputed PNG and decoded-RGB arrays; a real retained control-packet-to-real-analyzer integration regression binds that schema boundary.
- Focused offline result after fail-closed verifier corrections: 113 passed.
- Offline source preflight reproduced every frozen hash, binary mask population, D1/D2 identity, and all seven fresh-path absences.
- No EXP-006 stage/evidence namespace, game process, runtime read, signal, write, DAT, localizer, or candidate was created while preparing this packet.

## Runtime result

The user explicitly authorized only the frozen D3 arm and its read-only four-byte Level01 index read at `0x00861C84`. The argument-free runner completed with outcome `accepted-combined-mask-d3-holdout`.

| Item | Retained result |
|---|---|
| Executed build | auto-hardware derived PC executable SHA-256 `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f` |
| D3 process | PID/start/process-group `1121774/20272136/1121501`; distinct from both EXP-005 controls |
| Grid | 121 live 640x480 frames on the frozen `t0+3.300+0.200*i` schedule |
| Frozen exclusion mask | 92,480 pixels; decoded-byte SHA-256 `2a07565016efd050129e7d53b9f71942b2503cec8fffc7cbc592e0d619373cb6` |
| Outside-mask result | 0 mismatch observations; 0 unique pixels; no affected frames, components, or bounds |
| Result JSON | SHA-256 `3fe541dfd9973ce1238f603e3fafb28834749db7530f2e27db6efb09e2bc0c19` |
| Zero residual mask | SHA-256 `136af9d0ad549e0c0cee4161ece2ab0e00dfe309a53124729bcaf5956c76fbe1` |
| Overlay | SHA-256 `2071fdfe8f8a52e15fb9a2ba06bf61e9b097e89ab13dfb429c619ec671808d84`; decoded RGB equals the frozen D1 reference |
| Lifecycle | retained clean pre/post audits, clean immediate post-close audit, retail `R:` restored |

All six Direct3D markers passed with no software/mixed terminal marker. The production validator accepted every capture and its PNG/RGB provenance. No signal, runtime/debugger/DAT write, stopped-view read, localizer, candidate, or C/L/L/C arm occurred.

## Interpretation and next boundary

One independent derived-build D3 process reproduced every unmasked pixel on this exact finite grid. The frozen mask may therefore be used only as the accepted nuisance-exclusion reference for a separately preregistered successor at the same build/camera/grid scope.

EXP-005 remains aggregate-rejected. This result proves no animation cycle, exhaustive nuisance coverage, face-8 visibility, terrain/material/collision identity, causal effect, no-effect result, or retail-executable behavior. A separate C/L/L/C localizer packet must be prepared and committed offline, accepted by James, and freshly authorized before any localizer DAT creation or runtime arm.

## Links

- [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]]
- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC LEVEL DAT static mesh]]
- [[Known Unknowns]]
- [[PC autonomous game control]]
