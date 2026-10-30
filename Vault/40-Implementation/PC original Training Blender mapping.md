---
type: implementation
status: implemented-bounded
created: 2026-09-09
updated: 2026-10-29
evidence: [EXP-20260927-001, EXP-20260910-001, EXP-20260909-013, EXP-20260909-012, EXP-20260812-010, EXP-20260905-005]
tags: [implementation/blender, re/terrain]
---

# PC original Training Blender mapping

[[PC original level Blender maps]] maps every other original level with the
same coordinates and sidebar; this Training map and its importer are unchanged.

## Open and use

Saved map projects live under `work/level-projects/` (`original-training-map`,
then `original-training-populated`). `tools/blender/original_map.py` provides
the **N → ABLPC Map** sidebar. It supports orbit/top views, layer switches,
selectable original objects with PC source offsets, per-object notes and named
landmarks at the cursor. Ctrl+S saves the mapping work. The packed textures also
work when opening the blend directly. [[PC Mr Soil lesson triggers]] records the
native lesson predicates behind the tutorial objects shown here.

The top-down `overview.png` is a standalone private mapping image. Preserve the
complete folder, including `inputs/`, `original-map.json`, `import-report.json`
and `blender-check.json`. Game files and derived assets remain ignored by Git.
The earlier `work/level-projects/original-training/` is a framing trial, not the
selected deliverable. No original game files are changed by this workflow.

## PC identity and evidence

**Confirmed:** Training is the first carousel entry, selected with
zero Right presses. On PC the assets are `LEVEL07/LEVEL1.DAT`, `LEVEL1.RAW`
and `TERR1.ALL`, not the on-disk `LEVEL00/LEVEL.DAT`. Earlier accepted native
log `dynamic/wine/RUN-WINE-20260812-102953/bugs.log` records those loads at
lines1189–1192 and1456–1457, including the engine's packet-level number17.
The naming distinction is documented in [[EXP-20260812-010 - Training target rebind visible substitution]].

[[EXP-20260909-012 - Original Training Blender mapping]] records the exact
source hashes and extraction. There are262 primary and16 secondary objects,
12414 vertices,7953 faces, four referenced texture pages (0/1/2/4),25 terrain
collision sources with1360 triangles,80 barrier segments and78 placement
markers (62 type3F, including50 grains;16 type0B position rows).

The importer uses existing bounded DAT/RAW/terrain readers and offline native
Euler routine00463C80 from the hash-locked retail executable. Complete original
input bytes and offset-named fields remain available. Native palette/index
decoding independently reproduces the earlier original-PC Anthill page0 memory
capture in EXP-20260905-005 byte-for-byte. This is a texture-reader check, not
a claim of live Training image parity.

Blender keeps219 primary objects near the collision envelope visible;43 distant
primary records and16 secondary records are in initially hidden collections.
That grouping is geometric presentation, not a confirmed native visibility rule.
Collision, XZ barriers and stored placements are independently switchable.
One Blender unit is256 stored PC units (8192 runtime units), with origin0 and
axes `(PC X, PC Z, -PC Y)`.

## Pickups, actors and exit

[[EXP-20260909-013 - Populate original Training Blender map]] augments the saved
base without rebuilding its383 objects. The previous `original-training-map`
project and editor remain unchanged. To create another fresh populated successor:

```bash
.venv/bin/python scripts/populate-original-map.py \
  work/level-projects/my-training-map work/level-projects/my-training-populated
```

Separate layers hold50 grains, four FLIK letters, four spiders, four seeds,
Mr. Soil, the original exit-side leaf sign and source24's exit contact outline.
All54 pickup positions come from original00456A90 in offline Unicorn, with
native terrain loading and004ABE00 height queries. File Y stays preserved in the
raw markers. Letter initialized stored Y is F−1707, L−1860, I−1788, K−1620.

The RAW actor packet at336937 has nine nonzero slots: Soil38, four seeds11 and
four spiders9. Actor feet are editor-snapped using native floor queries; raw
XYZ and script selectors remain on each object. The four spider spawns are
shown together, not a simulation of tutorial lesson gating or actor movement.
Soil uses original textured SOIL.ALL primitives with stored descriptor offsets
(778 vertices,207 faces), not native animation matrices. This includes stored
helper/alternate parts, so it is not a claim of the game's selected rendered pose.
Grain, spiders and seeds use editor silhouettes; FLIK meshes extrude the original
frame-zero pixels. The sign mesh is unchanged primary.117, additionally linked
to the exit layer; hide its original scenery layer too to hide that shared mesh.
The exit association is geometric inference; native result3→completion is tested.

`population.json` owns source locators, preserved unknown bytes, native receipts
and preview limits. `population-check.json` owns saved-file hash and383 original
object fingerprints. `original-map.json` and base report counts describe EXP012's
unchanged base extraction, not the full augmented population.

## Seed tokens and blueberry lesson

EXP-20260910-001 corrects the
pickup-selection omission in EXP013. **Seeds and seed tokens are separate:**
the four seeds are RAW actors; the two green tokens are DAT selector2B rows56/57.
Four additional selector2C rows58–61 are berry-plant seed tokens. Selector23 rows
54/55 are blueberries; row55 lies outside the mapped scenery and is retained in
the hidden **Distant pickups** layer, without claiming it is unused.

All62 original type3F placements now have editor meshes. **Seed tokens** holds
the two green tokens, **Berry seed tokens** the four later tokens, and
**Blueberries** the in-map pickup. Tokens are editor silhouettes at the original
00456A90 initialized positions, not native animated sprite art. Unknown type0B
position records remain untouched in the original raw-marker layer.

Original0043C040 hides both green and four berry tokens by adding8000 to Y/floor.
0043C340 reveals the greens during lessons6/9. With weapon byte0059D9A7=0,
lesson12 stays active; original blueberry pickup00417720 sets it to1. The lesson
then advances to13, waits30 updates, and restores all four type2C tokens to their
initialized positions. These are pre-existing placements, not newly allocated
spawns. The actual lesson12 gate is any nonzero berry weapon. A bounded offline
proof executes those branches with feedback/audio/HUD/plant-refresh callbacks
stubbed; it does not replace live route or plant-growth acceptance.

The current map shows all lesson-gated tokens together. `seed-tokens.json`,
`seed-token-check.json`, `berry-pickups.json` and `berry-pickup-check.json` supplement
the earlier population files. The latter embeds the native lesson proof. Previous
projects remain unchanged; ordinary full population now includes these pickups.
For an older already-populated file, use fresh destinations for the two increments:

```bash
.venv/bin/python scripts/populate-original-map.py \
  work/level-projects/original-training-populated work/level-projects/my-token-map --tokens-only
.venv/bin/python scripts/populate-original-map.py \
  work/level-projects/my-token-map work/level-projects/my-full-map --berry-pickups-only --open
```

The final increment preserves465 preexisting objects. Saved reopen checks all71
pickup/actor placements, seven packed textures and annotation persistence.104
selected checks pass, including native token initialization, blueberry lesson,
30-update delay and four type2C pickups advancing seed byte0059D9AB to68.

## Limits and verification

This is mapping and annotation, not a compiler back into the original level.
147 objects have nonzero animation selectors; all scenery uses its stored pose.
Native animation, camera-dependent deformations, Flik, particles, generated
plants, script simulation and full native material/lighting parity are omitted.
Raw placement markers preserve file Y separately from initialized pickups. XZ-only
barriers are drawn at an arbitrary Y=0, never treating their middle words as Y.
Other scene dispatches, indexed/fixed-record variants and other levels reject.

73 focused checks and selected `make check` pass. Real Blender5.2 verifies all
12414 saved vertices,30875 UV corners,1360 collision faces, four packed textures,
78 markers and landmark add/save/reopen. The annotation trial is isolated at
`work/experiments/EXP-20260909-012/annotation-check.blend` with a JSON receipt.
No new PC game launch or live memory access was needed.

EXP013 passes89 selected make checks, all63 added pickup/actor positions after
reopen, seven packed textures and annotation add/save/reopen. Its standalone
overview and Soil/exit close-ups were inspected. Full animated actor poses,
tutorial sequencing and another exact PC level profile remain possible extensions,
preserving the mapping-only boundary until export has its own evidence and tests.
