---
type: experiment
id: EXP-20260812-006
date: 2026-08-12
question: Can a bounded PC LEVEL DAT prefix be parsed safely, edited through a hash-locked manifest, and accepted by the original executable under Wine?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora and Wine
environment_version: wine-11.0-staging
result: parser-runtime-and-visible-effect-confirmed
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/file-format
  - implementation/modding
---

# EXP-20260812-006 - LEVEL DAT prefix and manifest mod

## Question

Can a bounded PC `LEVEL*.DAT` prefix be parsed safely, edited through a hash-locked manifest, and accepted by the original executable under Wine?

## Inputs

- Training file: `CD/LEVEL07/LEVEL1.DAT`
- Input SHA-256: `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Example manifest: `mods/training-central-flower-cluster-candidate-far.json`
- Static evidence: functions `0x0044BB70`, `0x0044D430`, and loader `0x004AE240` in `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`

## Procedure

1. Reproduce the prefix walk performed at `0x0044BB70` without assigning unknown semantics.
2. Parse all PC files named `LEVEL*.DAT` under the derived work copy.
3. Add synthetic truncation, impossible-count, path-traversal, hash, round-trip, and sparse-edit tests.
4. Change the first signed 32-bit candidate of primary records 124–126 to `50000` at file offsets `0x0E60`, `0x0E74`, and `0x0E88`.
5. Compare direct `Z:` staging with a drive mapping preserving the known-good `S:\PC\BUGS` shape.
6. Run untouched and modified staged trees through training initialization using the software renderer.
7. Capture each compositor-visible game surface, crop only the 320×200 game area, and compare the stationary scene elements.

## Observed

- The bounded parser accepts all 21 PC `LEVEL*.DAT` files and rejects unrelated `RAND.DAT` when explicitly parsed.
- Training `LEVEL1.DAT` has two top records, zero 128-byte records, 262 primary 20-byte records, an empty index table, and 16 secondary 20-byte records before offset `0x1A94`. Bytes after that offset remain uninterpreted and untouched.
- The example output SHA-256 is `880ae29a3dbfe658fc163e41c96a1a5857a226d0a061068dbcd4cbcae8e698dc`. Only the three requested signed X dwords differ from the input.
- Direct-path runs `RUN-WINE-20260812-002146` (edited) and `RUN-WINE-20260812-002252` (restored input hash) both fault at `0x004A84A4`. The control discriminates the path/layout fault from the edit.
- With the exact drive layout `S:\PC\BUGS`, `RUN-WINE-20260812-004544` (unmodified) and `RUN-WINE-20260812-005110` (modified) load `level07\level1.dat`, finish `InitMainGame`, and enter `NextLife` under the software renderer.
- Exit status 58 in those runs records intentional capture termination after the target state, not an observed game failure.
- `training-control.png` shows the central foreground flower cluster. `training-records-124-126-far.png` shows that cluster absent while the terrain, sign, two ants, and seed remain rendered. Character and plant animations introduce smaller incidental pixel differences, but they do not explain the stationary cluster removal.

## Confirmed

- The parser's section boundaries reproduce a static executable walk and generalize across 21 PC files.
- The manifest tool validates the exact input hash and changes only the requested coordinate bytes.
- The original executable accepts and initializes the modified file under the known-good Wine drive layout.
- Jointly perturbing primary records 124–126 causes a visible, reproducible removal of the central foreground flower cluster.

## Inferred

- The first three dwords of each 20-byte record are position or spatial-center candidates: `0x0044D430` uses offsets 0, 4, and 8 in spatial/render calculations, the corpus contains plausible coordinate ranges, and the three-field perturbation changes visibility. The exact distinction between object transform and culling center remains unknown.
- Records 124–126 may be LOD variants or another grouped representation of the same cluster.

## Unknown

- The individual roles of primary records 124, 125, and 126.
- Semantics of the remaining fields and the unparsed suffix.
- Why direct absolute `Z:` staging destabilizes the downstream loader at `0x004A84A4`.

## Result

Completed. Parser, lossless preservation, manifest application, runtime acceptance, and a visible scene-object change are confirmed under Wine.

## Follow-up

Use a PC runtime watchpoint to distinguish LOD, culling, and transform roles for records 124–126.

## Later discrimination

[[EXP-20260812-008 - Training record watchpoints and individual roles]] performs that follow-up. Native watchpoints route all three records through `0x0044D5B8`, while matched individual mutations produce three disjoint visible plant-element differences. This rejects the specific hypothesis that records 124–126 are alternative LOD representations of one on-screen object in the tested Training start state. The joint “central flower cluster” description above remains the original software-renderer observation, not an individual-role assignment.

## Artifacts

- `dynamic/wine/RUN-WINE-20260812-004544/training-control.png`
- `dynamic/wine/RUN-WINE-20260812-005110/training-records-124-126-far.png`
- Corresponding `bugs.log` and `metadata.json` files in each run directory.

## Uncited intermediate runs (added 2026-10-12)

`RUN-WINE-20260812-002704` and `RUN-WINE-20260812-003358` were cited nowhere.
They fall between the direct-path runs above and the accepted `S:` layout
runs, use the same `work/mod-builds/training-disc-root` working directory,
and log `level07\level1.raw` loading through `\pc\bugs\cd\…`. `003358`
reaches `NextLife`; `002704` logs failed texture-surface restores. They are
recorded for provenance only. The conclusions above rest on the four runs
already cited.
