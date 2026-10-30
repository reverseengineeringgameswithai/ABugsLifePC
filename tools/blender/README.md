# Blender reference maps of the original levels

These scripts build Blender scenes of the original PC levels for mapping and
annotation. Each map is extracted from hash-checked private copies of the
retail level files and executable. Nothing here compiles back into a game file,
launches the game or reads live memory. Game files, decoded texture pages and
saved `.blend` files stay in ignored folders under `work/`.

Evidence and per-level detail are in the Vault:
`Vault/40-Implementation/PC original level Blender maps.md`,
`Vault/40-Implementation/PC original Training Blender mapping.md`, and
EXP-20260909-012, EXP-20260909-013 and EXP-20260927-001 in
`Vault/30-Experiments/`.

## Files

| File | Runs in | Role |
| --- | --- | --- |
| `scripts/map-original-levels.py` | Python | Extracts engines 1–16, runs the offline native queries, then calls `original_level_map.py` in background Blender; `--publish-report` writes asset-free metadata |
| `tools/blender/original_level_map.py` | Blender | Builds, saves, renders and re-verifies one complete level map |
| `tools/blender/original_map.py` | Blender | Base Training scene (`create`), shared coordinate/material/framing helpers and the **N → ABLPC Map** sidebar (`register`) |
| `scripts/populate-original-map.py` | Python | Adds Training pickups, actors and the exit marker to a fresh copy of a saved Training map |
| `tools/blender/populate_original.py` | Blender | Blender half of that population; fingerprints every existing object and requires it unchanged |
| `tools/blender/verify_original_map.py` | Blender | Saved-file check of a base Training map plus a landmark save/reopen trial |
| `tools/blender/verify_original_population.py` | Blender | Census and preservation check of a populated Training map plus an annotation save/reopen trial |

The Python side uses `reimplementation/ablpc/original_level.py` (Training
extraction, texture pages, native matrices), `original_levels.py` (all levels),
`original_population.py` (actor rows, stored models, letter pixels, initialized
placements), `collectible_preview.py` and `enemy_preview.py` (editor
silhouettes) and the bounded DAT/RAW/terrain readers. Native queries reuse the
offline Unicorn harness in `scripts/terrain-retail-probe.py`.

## Requirements

- The retail executable, SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
  (default `work/copies/BUGS_PC-disc/bugs.exe`).
- A CD copy at `work/copies/BUGS_PC-full-disc/PC/BUGS/CD` whose DAT, RAW and
  terrain files match the pinned hashes in `original_levels.SOURCE_SHA256`
  (Training: `original_level.TRAINING`).
- `unicorn` and `pefile` from the project environment.
- Blender. Blender 5.2.0 LTS (Flatpak) is the tested version
  (EXP-20260909-012, EXP-20260927-001).

Inputs and outputs must stay under `work/`, map projects under
`work/level-projects/` and published metadata under `reports/`. Every
destination must be fresh; existing maps and their annotations are never
overwritten.

## Opening a map and building the base Training map

`scripts/original-map.py` locates Blender (`ABLPC_BLENDER` if set, else
`blender` on `PATH`, else the `org.blender.Blender` Flatpak) for both drivers,
and `scripts/original-map.py edit <map folder>` opens a saved map with the
**N → ABLPC Map** sidebar. Opening `level.blend` directly also works; its
textures are packed.

The base Training staging folder that `populate-original-map.py` copies was
written by the workspace's level-authoring tool, which is not part of this
repository. Engines 1–16 (`map-original-levels.py`) do not need it.

## Coordinates and level files

One Blender unit is 256 stored PC units (8,192 runtime units), with origin 0.
Blender XYZ is `(stored X, stored Z, −stored Y) / 256`, so Blender Z is up.
The sidebar converts the active object's location back to stored X/Y/Z.

Level files follow the `0x004671D0` rule: engines 1–10 read
`LEVELnn/LEVEL.DAT`, `LEVEL.RAW` and `TERRAIN.ALL`; engines 11–17 read
`LEVEL(n−10)/LEVEL1.DAT`, `LEVEL1.RAW` and `TERR1.ALL`. Training is engine 17
and the first carousel selection (no Right press), so the PC stores it in
`LEVEL07/LEVEL1.DAT` with `LEVEL1.RAW` and `TERR1.ALL`. `LEVEL00/LEVEL.DAT` on
disk is a different file, not the Training gameplay scene. Load evidence:
`dynamic/wine/RUN-WINE-20260812-102953/bugs.log` lines 1189–1192 and
1456–1457 (EXP-20260812-010).

## Map engines 1–16

```bash
.venv/bin/python scripts/map-original-levels.py --engines 2 --out work/level-projects/my-maps
.venv/bin/python scripts/map-original-levels.py \
  --publish-report reports/original-levels/EXP-20260927-001.json
```

`--engines` defaults to 1..16; Training keeps its own map below. `--cd` and
`--exe` default to the paths above and `--out` to
`work/level-projects/original-levels`. An existing level folder is refused.
Each level is built in a hidden `.<folder>.partial` staging folder and renamed
only after the Blender check. `--publish-report` reads the existing projects
under `--out` and writes hashes, counts, censuses and native receipts without
running Blender.

For each level the Python stage:

- reads and hash-checks the three source files and decodes the texture pages;
- extracts every primary and secondary scene record with Euler matrices from
  original `0x00463C80` executed offline, plus collision, XZ barriers and the
  other stored terrain rows;
- runs original `0x00456A90` over the type-`0x3F` table for pickup positions;
- queries `0x004ABE00` for the floor below each creature slot;
- places Flik's start by the `0x0043E6B0` rule: X/Z/heading from the spawn
  table at `0x004DC7E8 + engine*12`, Y = `0x80000000` through `0x004AC460`,
  minus `0x100`.

`original_level_map.py` then builds the scene, saves `level.blend`, renders
`overview.png` and an unsaved-camera `overview-cutaway.png` (clipped 2,048
stored units above Flik's start so roofs do not hide interiors), reopens the
file and checks every source object origin and vertex, polygon counts
(including dropped degenerate faces), every pickup and creature location and
raw bytes, the collision triangle count and the packed page count. The results
go to `blender-check.json`.

Each folder holds `inputs/`, `textures/`, `original-map.json` (version 2),
`import-report.json`, `README.md`, `level.blend`, `overview.png`,
`overview-cutaway.png` and `blender-check.json`. Folders are named by carousel
progression (`01-anthill` … `15-canyon-showdown`) plus
`engine16-special-stage`; the Vault note has the full table.

Visible layers: **Original scenery**, **Grain**, **FLIK letters**,
**Berries**, **Seed tokens**, **Telescopes**, **Other pickups**, one
**Creatures •** layer per type, **Flik start** and **Landmarks**. Hidden
layers: **Secondary scene**, **Distant source objects**, **Undispatched
records**, **Creature offset model parts**, **Collision surfaces**,
**Collision • special results**, **XZ barriers** and **Other stored rows**.
Empty layers other than **Landmarks** are removed. Every object carries its PC locators and an editable
`mapping_note`.

Recorded result over engines 1–16 (EXP-20260927-001): 9,673 scene records,
9,672 drawn and one undispatched (Battle Arena `primary.165`, flags `0x93`);
936 pickups; 525 creature slots of 40 types; 2,747 other stored rows; 108,972
collision triangles; every level saved and reopened. Asset-free metadata:
`reports/original-levels/EXP-20260927-001.json`.

Limits recorded in every map: scenery uses stored poses and records native
animation selectors without playing them; sprite batches are crossed planes,
while the game turns them toward the camera; creatures are original RAW `0x102`
models in stored pose at literal stored XYZ, including script- or lesson-gated
spawns, with no headings or movement; creature names come only from earlier
evidence and "looks like" hints describe appearance only; per-corner normal
tables are recorded as metadata; texture and vertex-colour previews do not
reproduce the native renderer or lighting.

## Original Training map

`original_map.py create` builds the base Training scene from
`original_level.extract` output (EXP-20260909-012). It holds all 278 scene
records (262 primary, 16 secondary), texture pages 0/1/2/4, 1,360 collision
triangles from 25 sources, 80 XZ barrier segments and 78 stored placement
markers (62 type `0x3F`, 16 type `0x0B`). The 43 distant primary records, the
secondary records, collision, barriers and markers start hidden. Distant
records are classified by geometry outside the collision envelope; that is
presentation, not a confirmed native visibility rule or proof of unused data.
The texture reader independently reproduces the EXP-20260905-005 Anthill
page-0 capture; Blender brightness and transparency remain a preview.
`create` refuses a populated project and a saved `level.blend` whose hash no
longer matches its report.

Populate a fresh successor of a saved base map:

```bash
.venv/bin/python scripts/populate-original-map.py \
  work/level-projects/my-training-map work/level-projects/my-training-populated
```

The source's `inputs/` and `bugs.exe` are re-hash-checked, and its
`level.blend` must be unchanged at the end. The successor adds
(EXP-20260909-013 and EXP-20260910-001):

- 50 grains (type-`0x3F` rows 0–49, selector `0x14`) and F/L/I/K (rows 50–53,
  selectors `0x10`–`0x13`);
- two green seed tokens (selector `0x2B`, rows 56/57) and four berry seed
  tokens (`0x2C`, rows 58–61);
- blueberries (`0x23`, rows 54/55); row 55 lies outside the mapped scenery and
  sits in the hidden **Distant pickups** layer, without a claim that it is
  unused;
- the nine nonzero RAW actor slots: Mr. Soil (type 38), four seeds (type 11)
  and four spiders (type 9);
- Mr. Soil from the original `SOIL.ALL` primitives in stored pose (778
  vertices, 207 faces); stored helper and alternate parts are included, so
  this is not the game's selected rendered pose;
- the original exit-side leaf sign `primary.117` in **Level ending marker**,
  with the result-3 contact triangles of terrain source 24 as an outline.

Pickup positions come from original `0x00456A90`; actor feet use native floor
queries (`0x004ABE00`). Grain, spiders, seeds and tokens are editor
silhouettes; letter meshes extrude the original frame-zero pixels. Animation,
headings, script movement and lesson visibility are not simulated: the four
spider spawns and all lesson-gated tokens are shown together. The sign
association is geometric inference. The script stops if the census differs
from the recorded one: actor types 38×1, 11×4 and 9×4, the two `0x2B` tokens,
result-3 terrain sources `[24]`, and `primary.117` at geometry offset 90780
with origin [416, −651, 8915].

`population.json` holds source locators, preserved unknown bytes, native
receipts and limits; `population-check.json` holds the saved-file hash and the
fingerprints of all 383 base objects. `original-map.json` and the base counts
in `import-report.json` still describe the unchanged base extraction.

A map populated before tokens and blueberries were included takes them in two
fresh steps:

```bash
.venv/bin/python scripts/populate-original-map.py \
  work/level-projects/original-training-populated work/level-projects/my-token-map --tokens-only
.venv/bin/python scripts/populate-original-map.py \
  work/level-projects/my-token-map work/level-projects/my-full-map --berry-pickups-only --open
```

`--tokens-only` writes `seed-tokens.json` and `seed-token-check.json`.
`--berry-pickups-only` writes `berry-pickups.json` and
`berry-pickup-check.json` and embeds the offline lesson proof: the four berry
tokens are pre-existing placements revealed after the blueberry lesson, not
newly allocated at pickup time. The Training Vault note records the routines
involved. `--open` opens the result with the sidebar.

## Open a map

Opening `level.blend` directly shows the packed textured map. Loading
`original_map.py` with `register` adds the **N → ABLPC Map** sidebar:

```bash
blender --disable-autoexec work/level-projects/original-levels/02-tunnels/level.blend \
  --python tools/blender/original_map.py -- register
```

The sidebar offers **Frame level**, **Top view**, a hide switch per layer
(complete maps declare their own layer list), **Add named landmark at cursor**
and, for the active object, its stored PC X/Y/Z, record/object/geometry
offsets, source ID and `mapping_note`. Numpad 7 gives a top view and Numpad .
frames the selection. Save annotations with Ctrl+S and keep the complete
folder, including `inputs/` and the JSON reports.

## Verification

```bash
PYTHONPATH=reimplementation .venv/bin/python -m pytest -q tests/test_original_levels.py
```

This covers the file rule, every dispatch path, sprite scaling, undispatched
rows, normal tables, creature rows, 128-pixel pages and pickup joins, plus the
private retail corpus when it is present.

The two Training check scripts run inside Blender on a saved map:

```bash
blender --background --disable-autoexec work/level-projects/my-training-map/level.blend \
  --python-exit-code 1 --python tools/blender/verify_original_map.py -- \
  work/level-projects/my-training-map work/experiments/my-map-check/annotation-check.blend
blender --background --disable-autoexec work/level-projects/my-full-map/level.blend \
  --python-exit-code 1 --python tools/blender/verify_original_population.py -- \
  work/level-projects/my-full-map work/experiments/my-population-check
```

`verify_original_map.py` checks every saved vertex, polygon index list, face
tag and UV corner against `original-map.json`, plus four packed pages, 1,360
collision faces and 78 markers. It then adds a landmark, saves it to the given
fresh `.blend` (its directory must exist), reopens it and writes a JSON
receipt beside it. The recorded run checked 12,414 vertices and 30,875 UV
corners (EXP-20260909-012).

`verify_original_population.py` compares the preserved-object fingerprints
with the latest check receipt, checks the role census, every placement's
location and raw/initialized bytes, actor positions, Mr. Soil's 778/207 mesh,
1,360 collision faces, 78 markers and seven packed textures, then runs a
landmark save/reopen. It writes `annotation-check.blend`, `soil-closeup.png`,
`exit-closeup.png` and `verification.json` into the output folder
(EXP-20260909-013).
