---
type: experiment
id: EXP-20260906-004
date: 2026-09-06
status: live-trial-visual-acceptance-pending
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 43 native PC instruction probes and isolated Wine runtime comparison
question: "Does a collision-only outward offset reduce visible Flik and wall overlap while preserving the ramp route?"
result: bounded-clearance-trial-preserved-for-later-layout-design
---

# EXP-20260906-004 - Wall clearance comparison and offset trial

## Question and authority

Does a small **collision-only** outward offset reduce EXP-003's visible Flik/wall overlap while preserving the tested ramp routes? Original PC instructions remain authoritative. Offline executable SHA `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`; live accepted auto-hardware derivative SHA `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`. No PS1 consultation, live memory writes, teleport, save state or debugger control.

Canonical report: `reports/terrain/EXP-20260906-004.json`. The unchanged [[EXP-20260906-003 - Solid ramp sides and ground contour trim]] fixture remains the control.

## Confirmed observations

- A normal one-second Up hold in the EXP-003 control retained 50 read-only state samples with Flik's root **124..294 world units outside** west X=184000. This did not measure his visible body envelope. Receipt `work/experiments/EXP-20260906-004/authored-approach.json`.
- A synthetic nongrounded 512-unit horizontal approach through the original PC coordinator reached **zero** signed plane distance for the authored axis-aligned wall. The original oblique source87/cell1000 comparison behaved differently. These are finite point/motion cases, not a general actor-radius estimate. `native-clearance-initial.json` in the same evidence directory.
- Query evidence for `0x004AB1A0 -> 0x004AA4D0` concerns the supplied point/motion crossing branch. Fresh decoded instructions at `0x004AA7B3..0x004AA802` include the `-0xC0` response term at `0x004AA7C2`. Do not rename that term a body radius. Private query output is retained as `static-query-output.txt`.
- Geometric normal-line intersections found selected original source99 collision surfaces outside nearby primary128 render faces. Cell45168/face221724 separation is 46.371 stored units; cell45200/face222984 is45.928; cell45232/face222584 is43.697; cell45264/face223000 is42.298. Their render surfaces are inward, opposite the outward collision normal. The authored primary160 face361308 is exactly on the west collision plane X=5750 stored units at the sampled query height/footprint.

## Contrary evidence and limits

The original geometry is **not uniform**. Cells44676 and44708 have selected intersections on the other side of their collision planes (+3.419 and+11.476 stored units). The census selected55 steep source87/99 cells, found matches for32, traversed10,130 translational render triangles and excluded28 rotated references. Matching required absolute normal alignment >=0.96 and an intersection within500 stored units; quads used012/023. These geometric candidates are not runtime face-identity proofs. Full selection, coordinates and offsets: `work/experiments/EXP-20260906-004/original-render-clearance.json`.

A bounded24-press ordinary-input attempt to reach an original-wall neighborhood took Flik off the upper terrain and did not reach its target. The user reported the fall; subsequent read-only state was Level1, position `(164797,-46735,406202)`, contact `[99,7005747]`. Movement stopped. Retain `original-wall-navigation.json` as a failed navigation receipt, **not** a matched clearance test or evidence of a new collision defect/death. The useful original comparison in this packet is offline.

## Local trial

Choose48 stored units (1536 world units), just beyond the four selected roughly42..46-unit separations. This is an **authoring trial**, not a measured Flik radius, pixel conversion or universal original-wall rule.

`terrain_wall_clearance.py` shifts exactly three established X words for each of20 selected one-cell groups in source99: group+4 minimum, cell+6 origin, cell+24 window minimum. Group offsets49084..49920, stride44; cell offsets49096..49932. West plane184000 ->182464; east200000 ->201536. All normals, edges, relative extents, unknown bytes, other collision, ramp-floor cells, file size and directory remain unchanged. The original loader rebuilds derived bounds. The complete LEVEL.DAT is byte-identical to EXP-003.

- TERRAIN.ALL: `26e7076fa4027e1a81a1c8d29260944c04e584486ef886d8ab85e1f5e5f8dfcc`.
- Unchanged LEVEL.DAT: `f6cfa7883a902af5f43362356b7731adf9708ee5164c454b489e266867b048b2`.
- Fixture `work/copies/EXP-20260906-004/fixture`; isolated game `work/copies/EXP-20260906-004/game`.

Reproduce into fresh paths:

```bash
PYTHONPATH="$PWD/reimplementation:${PYTHONPATH:-}" .venv/bin/python \
  scripts/terrain-wall-clearance-probe.py \
  --fixture work/copies/EXP-20260906-004/reproduction \
  --report work/experiments/EXP-20260906-004/reproduction-native.json \
  --clearance 48
```

## Validation

- **69 affected tests passed in0.15s**:47 new synthetic writer/storage cases plus existing solid-ramp tests. Covers two directory/payload layouts, unknown-byte preservation, exact group selection, duplicates, unsupported geometry/clones, bad counts/truncation and signed overflow.
- **Original-PC gate accepted both arms in31.294611875s.** Per arm:6 nongrounded clearance cases,4 landing-seeded side approaches,3 three-leg ramp routes (9 uphill/downhill/return legs) and2 step-off/landing/open-foot returns. Side criterion is blocking/clearance, not continuously settled full-actor behavior.
- Steered routes use X correction clamped to+/-384, Z+/-900 and Y+512 with no leg reset. This does not turn the retained failed EXP-003 fixed-axis route into a pass.
- **Five-file terrain gate:72 passed in26.68s**, four loadfile workers, repo-local scratch and failed-only retention.
- Receipts: `affected-tests.xml`, `native-validation.json`, `focused-tests.xml` under `work/experiments/EXP-20260906-004`.
- No R2q/full-suite run or Git commit. Full-suite and Git banking audits remain deferred, not claimed clean.

## Fresh file-loaded preview

EXP-003 was closed through the existing normal-request/scoped-fallback operator; no survivors remained, but normal-close-only success was not independently established. Post-close and immediate prelaunch audits were clean. EXP-004 launched **once** with a cold copied isolated prefix. All six hardware markers and R-drive content/LevelSelect gates passed. Anthill carousel and Level One title were inspected before their Return inputs. No gameplay movement was sent in the new trial.

Level1 handoff position `(197091,2734,492897)` is the normal start. Game71867/start1283745, group71598; Gamescope71616/start1283614, display`:2`, window14680071; prefix `work/experiments/EXP-20260906-004/preview-01/prefix`. Sink `ablpc_mute_71598`; module536870916 is reusable and not identity by itself.

Complete resident source99/100 payloads and mesh streams128/160/213/280 matched the candidate, with bound8560 at DAT+8592 unchanged. This is not an all-resident-assets audit. The generic postlaunch audit is **not clean** while the preview is deliberately open: seven processes and one sink were independently bound to this preview. Receipts `preview-01/resident-verification.json`, `audit-after-launch.json`, `live-handoff-binding.json`; native640x480 handoff capture SHA `89a1cc325670cc8867c7c07daf330d1e21b5fb6818674018da9b84b7c074565c`, file stable across200ms.

## Acceptance still needed

The predicted visual improvement is **not yet confirmed live**. User should press against both sides and inspect Flik's body, then round the lower corners and approach from inside/outside the added clearance strip. Corner/end-entry coverage is not exhausted by the tested center-lane open-foot routes. Draw-order contribution and the earlier ground-contour trim outcome remain separate unknowns. If overlap persists despite the verified additional clearance, compare actor/render ordering rather than repeatedly widening the invisible margin.

## 2026-09-06 stripped-layout successor, no live switch

[[EXP-20260906-005 - Isolated authored terrain and platform spawn]] derives a separate private candidate retaining this experiment's exact authored collision/render pieces while deactivating old landscape/scenery traversal and adding a file-backed platform spawn. This fixture and its live preview are unchanged. EXP-005's nine native accepted arms do not close this experiment's wall-visual/corner limitations; its complete spawn arm still needs the disclosed test-setup correction before any fresh launch.
