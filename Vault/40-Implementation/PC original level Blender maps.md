---
type: implementation
status: implemented-bounded
created: 2026-09-27
updated: 2026-10-29
evidence: [EXP-20260927-001, EXP-20260909-012, EXP-20260909-013, EXP-20260914-010, EXP-20260926-001]
tags: [implementation/blender, re/terrain]
---

# PC original level Blender maps

Complete reference maps of every original PC level except Training, which keeps
[[PC original Training Blender mapping]]. Evidence and limits:
[[EXP-20260927-001 - Complete original level Blender maps]].

## Open and use

Folders are named by Flik's Journey progression (see [[PC level roster and numbering]]):

| Folder under `work/level-projects/original-levels/` | Level | Engine | Source DAT |
|---|---|---:|---|
| `01-anthill` | Anthill | 1 | `LEVEL01/LEVEL.DAT` |
| `02-tunnels` | Tunnels | 3 | `LEVEL03/LEVEL.DAT` |
| `03-council-chamber` | Council Chamber | 2 | `LEVEL02/LEVEL.DAT` |
| `04-cliffside` | Cliffside | 6 | `LEVEL06/LEVEL.DAT` |
| `05-riverbed-canyon` | Riverbed Canyon | 10 | `LEVEL10/LEVEL.DAT` |
| `06-bird-nest` | Bird Nest | 11 | `LEVEL01/LEVEL1.DAT` |
| `07-city-entrance` | City Entrance | 4 | `LEVEL04/LEVEL.DAT` |
| `08-city-square` | City Square | 5 | `LEVEL05/LEVEL.DAT` |
| `09-bug-bar` | Bug Bar | 14 | `LEVEL04/LEVEL1.DAT` |
| `10-clover-forest` | Clover Forest | 7 | `LEVEL07/LEVEL.DAT` |
| `11-the-tree` | The Tree | 12 | `LEVEL02/LEVEL1.DAT` |
| `12-battle-arena` | Battle Arena | 13 | `LEVEL03/LEVEL1.DAT` |
| `13-anthill-pt-2` | Anthill Pt 2 | 9 | `LEVEL09/LEVEL.DAT` |
| `14-riverbed-flight` | Riverbed Flight | 8 | `LEVEL08/LEVEL.DAT` |
| `15-canyon-showdown` | Canyon Showdown | 15 | `LEVEL05/LEVEL1.DAT` |
| `engine16-special-stage` | no carousel slot | 16 | `LEVEL06/LEVEL1.DAT` |

Open `level.blend` directly, or run `.venv/bin/python scripts/ablpc-level edit <folder>`
for **N → ABLPC Map** (frame, top view, layer toggles, landmarks, source offsets).
Each folder also has `overview.png`, `overview-cutaway.png` (clipped 2,048
stored units above Flik's start so roofs do not hide interiors), `README.md`,
`original-map.json`, `import-report.json`, `blender-check.json`, `inputs/` and
`textures/`. Keep the whole folder. Ctrl+S saves annotations.

The earlier Cliffside reference map (`work/level-projects/cliffside-original-map`)
is unchanged; `04-cliffside` is the complete successor with pickups, creatures
and start.

## Layers

Visible: **Original scenery**, pickups (**Grain**, **FLIK letters**, **Berries**,
**Seed tokens**, **Telescopes**, **Other pickups**), one **Creatures •** layer
per type, **Flik start** and **Landmarks**. Hidden: **Secondary scene**,
**Distant source objects**, **Undispatched records**, **Creature offset model
parts**, **Collision surfaces**, **Collision • special results** (non-zero
result words, coloured), **XZ barriers**, **Other stored rows**.

Every object carries its PC locators (`pc_record_offset`, `pc_object_offset`,
`pc_geometry_offset`, `pc_raw_hex`, flags/dispatch, stored origin, angles,
scale, selector) and a `mapping_note` for your own notes.

## What each object is

- **Scenery:** every primary/secondary record in stored pose. Sprite batches
  (fences, berry lobes, billboards) are crossed textured planes; the game turns
  them toward the camera. Negative-count meshes keep their opaque span in JSON.
- **Pickups:** preview meshes at original `00456A90` initialized positions.
  Letters extrude the native frame-zero pixels; grain/berries/tokens use the
  existing editor previews; other selectors use coloured markers.
- **Creatures:** each slot's original RAW model in stored pose at its literal
  stored XYZ, including script/lesson-gated spawns. Names are used only where
  earlier evidence exists (spider, mosquito, seed, bee, Dot, harvester, pill
  bug, caterpillar). Other types are numbered; fourteen carry "looks like"
  appearance hints. Parts stored more than 2,048 units from a model origin
  (seed's second copy at X−5000) go to the hidden offset-parts layer.
- **Creature identities (2026-10-05):** loader `00445020` loads character
  files by type: type 16 is Thumper (`chars2\thumper`, Council Chamber slot 1)
  and type 29 is Molt (`chars3\molt`, the Battle Arena "grasshopper"). See
  EXP-20261005-001.
- **All 41 types (2026-10-12).** [[EXP-20261012-006 - Creature types from the character loader]] reads each type's character file from
  the loader `0x00445020`: types 1–41, `chars\gypsy` … `chars4\badcent`.
  - 26 types are also confirmed by saved runtime logs.
  - The map script still labels types from `original_levels.CREATURES` and
    `APPEARANCE`. Hints 31 ("flytrap plant", file `acorn`) and 37 ("dandelion
    seed", file `weevil`) disagree with their files.
- **Flik start:** spawn-table X/Z/heading with `0043E6B0`'s own height rule.

## Rebuild or extend

```bash
.venv/bin/python scripts/map-original-levels.py --engines 2 --out work/level-projects/my-maps
.venv/bin/python scripts/map-original-levels.py --publish-report reports/original-levels/EXP-20260927-001.json
```

Destinations must be fresh folders under `work/level-projects/`; existing maps
are never overwritten. Sources must match the pinned retail hashes.
`tests/test_original_levels.py` covers the file rule, every dispatch path,
sprite scaling, undispatched rows, normal tables, creature rows, 128-pixel
pages, pickup joins and the private retail corpus.

## Limits

Reference maps only; nothing compiles back into the game. No animation,
lighting, particles, generated plants, AI or script timing. Texture and
vertex-colour previews are approximate. See the experiment for unknowns.
