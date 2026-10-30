---
type: experiment
id: EXP-20260909-013
date: 2026-09-09
question: Can all requested Training pickups, actors and the exit be added while preserving the existing mapping scene?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux, offline Unicorn 2.1.4, Blender 5.2.0 LTS Flatpak
result: Populated successor reopened; native pickup initialization, original-object preservation and saved-file checks pass; animation remains out of scope.
status: completed-bounded
created: 2026-09-09
updated: 2026-09-09
tags: [experiment/blender, re/terrain, re/actors]
---

# EXP-20260909-013 - Populate original Training Blender map

## Question and outcome

User requested all grain, letters, enemies, Mr. Soil and the level-ending marker
in the original Training Blender map, then reopening it. Delivered successor:
`work/level-projects/original-training-populated/level.blend`.
It contains50 grain meshes, F/L/I/K, four spider previews, four seed previews,
original textured Mr. Soil in stored pose, the original exit-side leaf sign and
a green exit contact-area outline. All383 preexisting objects are unchanged.
The base `original-training-map` saved project and its open editor are preserved.

## Inputs and PC evidence

All assets are private copies. Retail executable SHA256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Exact Training input identities remain those in
[[EXP-20260909-012 - Original Training Blender mapping]] (LEVEL07/LEVEL1.DAT,
LEVEL1.RAW, TERR1.ALL; initial carousel selection, engine packet level17).

**Confirmed:** DAT type3F at offset4 contains62 rows; rows0–49 selector14 are
grain, rows50–53 selectors10–13 are FLIK. Original00456A90 executes114424
instructions against Training terrain initialized by the original loader and
004A89F8..004A908F slice. Native004ABE00/004ACA60 supply heights; the original
offset table at004C6A88 is loaded from the exact PE. Grain XYZ remains literal.
Initialized letter stored XYZ:

| Letter | X | Y | Z |
| --- | ---: | ---: | ---: |
| F | -2733 | -1707 | 5061 |
| L | 4821 | -1860 | 2773 |
| I | 3205 | -1788 | -4510 |
| K | -5366 | -1620 | -3184 |

This is offline original-instruction execution, not live Training capture.
Ordered pickup-initializer trace SHA256:
`9bda974e7a87cc62bb39e424f463b61c19ed276aedc160fb7e309d5e866b61dd`.

**Confirmed:** RAW packet tag23 at file336937 decodes to1796 bytes: header4
plus64×28 actor slots. Nonzero types are38 once (slot0 Soil),11 four times
(slots1–4 seeds),9 four times (slots5–8 spiders). Packet SHA256:
`0724f2bf76d143e11fabf59fc7ddc17126b7dfd120cb2e4229bf3e44ef66d216`.
0041C420/0041BD10 consume these slots;00445020 binds resources. The historical
native Training log `dynamic/wine/RUN-WINE-20260812-102953/bugs.log`, lines1461–1465,
loads SOIL, SEED and BADBUG. 0043C340 controls tutorial progression; all four
spawns are editor-visible together without simulating its lesson gating.

**Confirmed:** tag102/id38 at RAW532580 embeds SOIL.ALL after its eight-byte
header, identical to `CD/CHARS3/SOIL.ALL`, SHA256
`a64871f3de0657cb1356ab01b3ecb11467026b8758cbf1a162b23f71d128f027`.
Bounded kind1 ALL primitives follow PC0044F8E0's36/48-byte textured triangle/quad
walk and four-byte terminators;26 visual descriptors produce778 vertices and207
faces with texture pages17/19/20. Unknown records and full raw descriptors remain
preserved. Only stored translations are applied, not animation matrices.
The source includes alternate/helper parts; this is not a selected native pose.
The parser also checks the BADBUG corpus (76 faces) and rejects unsupported
commands, missing terminators, bounds violations and unsupported post-terminator data.

**Confirmed:** the only kind6 Training terrain source with result3 is24, origin
(15,-753,8398). The native switch table at00440AE8 maps3 to00440920; a regression
executes original004408CE..00440934, confirming done word0059A5B0=1 and countdown
0059D9B8=23, stopping before audio. This is dispatch evidence, not a full walk-out.
**Inferred sign association:** primary117/object9724/geometry90780 at stored
(416,-651,8915) is the leaf sign next to that contact area; the close-up confirms
its appearance. Its geometry/name/properties are untouched and it receives a
second collection link, not a duplicate mesh.

## Implementation and verification

`scripts/populate-original-map.py` requires exact inputs and a fresh target under
work/level-projects; it copies the saved source, creates population metadata and
augments it with `tools/blender/populate_original.py`. No originals, live memory
or game-facing files are changed. The sidebar exposes independent population
layers. Grain/spiders/seeds use editor silhouettes; FLIK extrudes original
24×24 frame-zero strip pixels with native page29 palette bank7 (EXP011).
Actor feet use native floor queries, with raw XYZ/scripts preserved separately;
they are not complete native actor updates or a heading/animation reconstruction.

89 selected tests pass via:
`PYTEST_ADDOPTS='-k "original_level or original_population or level_dat or terrain_all or level_scene_cli"' make check`.
Compatibility/tracked-asset gates pass. This is not a full-suite pass.
Final Vault lint has zero errors and eight existing warnings; claim sweep finds
only the updated wording for the former omitted-Soil/enemies limitation.
An initial direct pytest invocation omitted PYTHONPATH and failed collection;
the corrected invocation and Makefile checks passed. Saved-image counting was
corrected from8 loaded images to7 retained packed images: page29 only supplies
letter voxel RGB and is not referenced by a saved material.

Private evidence:

- Successor `population.json`: original records, source offsets, native loader/
  initializer/height receipts, mesh data and limits.
- `population-check.json`:383 original object fingerprints, collection counts,
  original source hash and saved successor hash.
- `work/experiments/EXP-20260909-013/verification.json`: all63 added positions and
  raw records after saved-file reopen;383 preserved originals;1360 collision
  triangles;78 raw markers; seven packed textures; annotation add/save/reopen.
- `annotation-check.blend`: isolated annotation trial, never the deliverable.
- Successor `overview.png`, experiment `soil-closeup.png` and `exit-closeup.png`:
  visually inspected. Blender5.2.0 LTS, hashfbe6228777e7; offline processes exited.

Delivered blend SHA256:
`ba33200e2e137361a2ca034a4339a9a9a5f0f01c3efc7aa5c506197a00eb6c73`.
Base remains `dce82b6777c0d59e07f197b797c6d2cf5f7e82e53ffea0a959343ff89becc9f5`.

## Runtime handoff and remaining limits

Populated Blender207941/start2710294/group207916 is OPEN with the sidebar.
Base mapping Blender200992/start2576253 and mod Blender13435/start146871 are
preserved to avoid discarding unsaved work. User game119123/start2092071 remains
untouched. Fresh generic audit's seven game/helper identities exactly match
EXP011's manual binding; no private null sink. This is an accounted non-clean
audit, not a CAP-010 acceptance. [[Environment Status]] owns the live handoff.

No original-level game exporter, native actor animation/heading/tutorial-state
parity, generated plant coverage or full renderer parity is claimed. No PS1
source was consulted. Sources/tests/Vault remain uncommitted because this user
request did not ask for banking. Workflow: [[PC original Training Blender mapping]].
