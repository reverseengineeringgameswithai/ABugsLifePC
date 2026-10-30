---
type: experiment
id: EXP-20260820-002
title: R2m offline cross-time correspondence diagnostic
date: 2026-08-20
environment: Offline retained-frame analysis only
binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
question: Does exactly one fixed integer lag make every retained L1/L2 pair identical outside the frozen mask while all camera-safe crops remain control-exact?
status: completed
result: Valid diagnostic found no unique fixed lag; wall-clock alignment is nonviable
created: 2026-08-20
updated: 2026-08-20
tags:
  - experiment
  - pc
  - anthill
  - level01
  - static-mesh
  - offline-analysis
---

# EXP-20260820-002 - R2m offline cross-time correspondence diagnostic

## Purpose

[[EXP-20260820-001 - R2l fresh replicated face8 localizer]] was procedurally valid but scientifically inconclusive because L1 and L2 did not reproduce at corresponding capture indices. This offline diagnostic asks only whether a unique exact fixed wall-clock lag explains that retained state mismatch.

It cannot reinterpret or rescue R2l. It performs no launch, game input, DAT creation/write, memory access, signal, mask mutation, localizer/candidate creation, or successor execution.

## Frozen inputs

- R2l aggregate: `work/copies/EXP-20260820-001/evidence/comparison/inconclusive/fresh-replicated-face8-localizer-001/result.json`, SHA-256 `60c38e6719a0768db1e9569542d75ceb8a8b6a8ef51fc67e8cc69b7895cf97fd`.
- L1 quarantined evidence: `work/copies/EXP-20260820-001/evidence/rejected/L1-FRFL-AH-001`.
- L2 quarantined evidence: `work/copies/EXP-20260820-001/evidence/rejected/L2-FRFL-AH-001`.
- L1/L2 dispositions: `c11a69208ce80fae16e15b6e0881532eda3f60e4a317aa55844b402bded3fe72` / `331e77c87d1b7de3aa4d40292401b31d488c28a8af341507ec2c68e28830d285`.
- L1/L2 grid gates: `a868b79391a08945c11b0544d42a6a795b5edf40d7912b2be4aa5413ed944c53` / `6c8a7c2ec70c59ca046899026a4c3ea96d3de7dcba6a04e85b92f8db2d79a73e`.
- Pair receipt/disposition: `23087ee71d4e110a57f645f11a424b7fd4b9b2578a0cf85221f0fc72ed5ea333` / `050a555a751022bc8f42162fa3c10b0d87b84aafee2635d15016460c0a6badcd`.
- L1/L2 creator receipts: `5806baaa3bdad604e0bd3aaad26f3048a8874f4331d15cecd1bb5a4b9f242928` / `295162d8cb181495ef944713a00596ce6c6ce05f1cc18345e3ea61d3da302432`.
- Both localizer DATs: `9942e252028b198dd0c16c6e45a1584620244f7dd9d9aeabe9a53bc04bd11bfd`.
- Mask: `work/copies/EXP-20260819-008/diagnostic/proposed/control-trained-successor-mask-001/proposed-control-trained-mask.png`.
- Mask PNG/decoded SHA-256: `b855df0ac67554737ae990bcb5fdbb14a132eae32af6bddf292c07dba193c936` / `9ff27caa7842b9047c9eebf633f9d280dd820841b81eba5fd491845a66fb71ba`.
- Mask population: `93,445`; eligible pixels: `213,755`.

The aggregate embeds pre-quarantine `evidence/accepted/...` paths. The diagnostic must rebind each index deterministically to the corresponding `evidence/rejected/.../grid/frame-NNN.png` path and reject every other substitution. It validates exactly 121 ordered frames per arm and rehashes each PNG before decode, decoded RGB, and PNG after decode against the aggregate arrays. Sources are validated again before atomic publication.

## Camera-safe crop contract

| Name | Geometry | Frozen decoded RGB SHA-256 |
|---|---:|---|
| `upper-right-structure` | `160x100+480+0` | `41aa36449cae7e735d5476644f670d01eb931490484d22091da1647ad1852bf6` |
| `left-middle-structure` | `120x100+20+220` | `7a87a57c278e09861fada1511c7aac9dd10cfe607d109fb6b48696103998ab14` |
| `lower-left-structure` | `160x100+0+380` | `59e3593b7b487553a63483cf20134aef9be97dae6b73690e5f5ababa8e1541e0` |

`lower-right-structure` remains excluded. No memory-derived camera or player state exists here. “State” means only these retained crop signatures and the capture-index/timing receipts.

## Exact matrix

Compute all `121 x 121` L1/L2 pairs and retain:

- Outside-mask RGB disagreement pixel count, fraction, and exact-equality boolean for each `(i,j)`.
- Separate disagreement and exact-equality matrices for each camera-safe crop.
- Per-frame crop hashes and control-hash matches.
- `j-i` and nominal offset `0.200 * (j-i)` for each evaluated fixed lag.
- Row/column minima, tie counts, and mutual-nearest pairs as explicitly nonselecting diagnostics.

No nearest-neighbor result, approximate minimum, or heatmap may select a future protocol.

## Frozen viability rule

Evaluate only integer lags `k in [-60,60]`. Each has at least 61 overlapping pairs. A lag passes only when all conditions hold:

1. Every overlapping `L1[i]` versus `L2[i+k]` pair has exactly zero RGB disagreements across all 213,755 eligible pixels.
2. Every paired crop is byte-exact for all three camera-safe crops.
3. Every paired crop in both arms equals its frozen control hash.
4. Both arms have nonzero temporal variability across eligible pixels.
5. Exactly one lag passes the preceding gates.

No tie-breaking, threshold relaxation, rotation, warping, registration, per-frame remapping, adaptive extension, or manual selection is permitted.

## Outcomes

- `diagnostic-valid-unique-fixed-lag`: permits designing, but not running, an all-fresh validation packet at that predeclared lag.
- `diagnostic-valid-no-unique-fixed-lag`: wall-clock alignment is not scientifically viable; do not repeat this protocol.
- `diagnostic-invalid`: any source, path, hash, crop, mask, dimension, timing, decode, or publication failure.
- Incomplete publication remains under `diagnostic/pending/`; valid complete publication is atomic under `diagnostic/accepted/`.

Every outcome records `future_runtime_authorized: false`. Even a unique lag proves no face-8 localization, terrain, collision, material, visibility, causality, retail behavior, or no effect.

## Evidence outputs

- Frozen-source receipt with all 242 frame hash arrays and deterministic path rebindings.
- Full outside-mask count/fraction/exact matrices in JSON and CSV.
- Three independent crop matrices and per-frame hashes.
- Fixed-lag summary with exact pass/fail reasons and overlap counts.
- Row/column minima, tie table, and mutual-nearest relationships marked nonselecting.
- Deterministic heatmaps marked visualization-only.
- Output SHA-256 manifest and final result.

## Implementation

- `reimplementation/ablpc/r2m_cross_time_correspondence.py`
- `scripts/r2m-run-cross-time-correspondence.py`
- `tests/test_r2m_cross_time_correspondence.py`

The permanent tests cover unique/no/multiple lag, constant scene, crop drift, one-pixel eligible mismatch, mask-contained changes, insufficient overlap, path/source/hash mutation, publication pending behavior, argument-free execution, and static prohibition of runtime/mutation reachability. Production output absence is preregistration evidence, not a permanent test.

## Result

The committed argument-free diagnostic completed under `diagnostic/accepted/l1-l2-cross-time-correspondence-001` with outcome `diagnostic-valid-no-unique-fixed-lag`.

### Durable anchors

- Result: `work/copies/EXP-20260820-002/diagnostic/accepted/l1-l2-cross-time-correspondence-001/result.json`, SHA-256 `f5c43ea2ea742f891b8bcec9caf0352e9bd582a2de5bf775a4d3e0950c1b4174`.
- Output manifest: SHA-256 `bac7229dddfa9152fe018df9beeae59c05de218755faf76b776f88e0790cf160`.
- Fixed-lag summary: SHA-256 `aab278a771dfbfb9e8b2e21f4809131f143149c14b966c880ad974c291a5ae84`.
- Outside-mask matrix: SHA-256 `d37aee34fa9440f1a8e229a82d11586b5ac702e02ab6e5b33713957ebd17f19a`.
- Nonselecting minima/ties: SHA-256 `b4f68c164e6599128c6b090650f87563d4a6e226e676f9e67d56f37ab1c89263`.
- Frozen-source receipt: SHA-256 `46dfaaeb247d978854855d492131a777df3e491b8803898dd158669458a62b28`.

### Findings

- Passing lags: none.
- L1 eligible-pixel temporal variability: false; L2: true.
- Every one of the 121 frozen lags failed outside-mask exactness, all-crop pair exactness, all-crop control-hash equality, and the nonconstant-arm requirement.
- The full matrix contains `1,815` exact individual frame pairs, but no fixed lag makes every overlap exact. These pairs are nonselecting and cannot seed a protocol.
- Global outside-mask disagreement range: `0` through `200,544` pixels.
- Unique crop signatures, L1/L2: upper-right `1/106`, left-middle `1/21`, lower-left `1/21`.
- `future_runtime_authorized` is false; the mask was not widened or selected.

James independently rehashed all 242 PNG/RGB bindings and recomputed the matrix, crop signatures, all lag failures, and minima/ties exactly, then returned `ACCEPTED` for this interpretation.

## Interpretation

Fixed wall-clock lag alignment is not scientifically viable and this protocol must not be repeated. Individual exact pairs, nearest minima, ties, and heatmaps cannot be selected post hoc. R2l remains inconclusive and is not rescued or reinterpreted.

No face visibility, no-effect, terrain, ground, material, collision, causal, camera-memory, player-state, or retail-behavior claim follows. The next defensible work is offline/static identification of independently justified PC camera/player/render-state read candidates. Any later experiment must preregister exact bounded read-only addresses, source/consumer provenance, state-equivalence gates, fresh arms, James acceptance, and fresh user authorization.

## Links

- [[EXP-20260820-001 - R2l fresh replicated face8 localizer]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns]]
- [[Reverse Engineering MOC]]
- [[Current State]]
