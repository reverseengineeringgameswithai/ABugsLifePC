---
type: experiment
id: EXP-20260909-012
date: 2026-09-09
created: 2026-09-09
updated: 2026-09-09
status: completed-bounded
question: Can original PC Training be opened as a textured Blender mapping scene using the established PC readers?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux, repository Python3.14.6, offline Unicorn2.1.4, Flatpak Blender5.2.0 LTS
result: Original Training scenery, textures and collision imported; saved coordinates and UVs verified; landmark persistence passes
tags: [re/experiment, implementation/blender]
---

# Original Training Blender mapping

The user requested original LEVEL00 Training for mapping in Blender, specifying
the first Flik's Adventure selection without a Right press. Existing native
Training receipts resolve its PC paths as `LEVEL07/LEVEL1.DAT`, `LEVEL1.RAW`
and `TERR1.ALL`; `LEVEL00/LEVEL.DAT` is a different file and was not imported.
Evidence: [[EXP-20260812-010 - Training target rebind visible substitution]],
`dynamic/wine/RUN-WINE-20260812-102953/bugs.log`:1189,1456,1457.

## Inputs and procedure

All reads used existing copies in `work/copies/BUGS_PC-full-disc/PC/BUGS/CD/`
and retail EXE `work/copies/BUGS_PC-disc/bugs.exe`; no PS1 source was consulted.

| File | SHA256 |
| --- | --- |
| LEVEL07/LEVEL1.DAT | 494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22 |
| LEVEL07/LEVEL1.RAW | c5f81eed3c9d1a01cc188ead50fc10a5ae0f213b0ca165764fa7b311a02a0926 |
| LEVEL07/TERR1.ALL | 97141bdc9953e963329fe968f4263478dffd74af041d6a4676a984239c4dfd8c |

`scripts/ablpc-level import-original --level LEVEL00 --out work/level-projects/original-training-map`
composes existing checked readers. DAT object pointers use the documented24/32-byte
layouts; complete positive mesh streams are decoded. Offline original00463C80
produces Euler matrices; existing per-column scaling and signed truncation give
the stored-pose preview. Unknown object/scene bytes and original inputs remain.
Sources: [[PC LEVEL DAT prefix]], [[PC LEVEL DAT static mesh]],
PC Blender level authoring, [[PC TERRAIN ALL barrier strips]].

Native00462C30/00466260 and EXP-20260905-005 establish texture conversion.
The new reader reproduces earlier captured Anthill page0 indices
`da6ed96650d2a3464f6d8af8d37f6088222d744ae95b322bff0031d9e14caf85`
and palette `0e848743ea7fcae70325a8a71b9691a65f048d4634781212860627120d57e1dc`.
This independently checks low-nibble order and64-square palette banks. Training's
four referenced pages are extracted and packed into the Blender file.

## Observed and limits

All278 scene objects decode:262 primary and16 secondary,12414 vertices and7953
faces. Terrain yields1360 triangles across25 sources and an80-segment XZ barrier.
78 markers preserve62 type3F and16 type0B rows. Stored selectors label50 grains
and the four FLIK letters; remaining selectors and type0B semantics stay unknown.

The initial framing trial included43 distant primary records and made the map
small. Those objects are now retained in a separate hidden layer, with all16
secondary objects preserved separately.219 nearby original objects frame the
complete visible bowl. The grouping is inferred presentation only. The first
trial remains under `work/level-projects/original-training/`.

Final project and overview are in `work/level-projects/original-training-map/`.
The blend hash at delivery is
`dce82b6777c0d59e07f197b797c6d2cf5f7e82e53ffea0a959343ff89becc9f5`;
overview hash `e500fba3c4dbbdef9187dd6d32bbbdec9287cae62421a00ff15a481af6b02415`.
Private import/report JSONs record source offsets, pages, counts and native matrix
cases. [[PC original Training Blender mapping]] owns the user workflow.

No new game-renderer fidelity claim:147 animation selectors are shown at stored
pose, brightness/transparency are approximate, dynamic actors and scripts are
omitted, and native placement Y initialization is not applied. Barrier display Y
is arbitrary0. There is no original-level game-file exporter or other-level profile.

## Validation and lifecycle

`PYTEST_ADDOPTS='-k "original_level or level_dat or terrain_all or level_scene_cli"' make check`
passes73 tests (6075 deselected), compatibility and tracked-file gates; Vault
lint has zero errors and eight existing warnings. Hooks were already installed.
Tests cover synthetic both-layout/shared geometry, bad pointers/indices/counts,
truncation, opacity, texture-bank boundaries, duplicates/missing pages, wrong EXE,
fresh-output guards, full Training and an explicit Anthill sprite-dispatch rejection.

Real Blender verification reopens the saved map and checks12414 positions,
30875 UV corners,1360 collision faces, four packed textures and78 markers.
Adding a named landmark then saving/reopening a separate file passes.
Receipt: `work/experiments/EXP-20260909-012/annotation-check.json`;
reproducer: `tools/blender/verify_original_map.py`.

The new mapping editor was launched separately. No game launch, close, key input,
debugger action or live memory read/write occurred. The seven audited game rows
match EXP011's existing user session, with no private sink. Existing Blender13435
and approved mod/bank remain preserved. [[Environment Status]] owns the live handoff.
