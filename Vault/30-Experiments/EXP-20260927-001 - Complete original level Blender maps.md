---
type: experiment
id: EXP-20260927-001
date: 2026-09-27
question: Can every other original PC level be mapped into Blender like Training, with every scene record, pickup and creature?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Offline static readers, Unicorn execution of retail routines, Blender 5.2.0 LTS (flatpak) in background mode
environment_version: Python 3.14.6; Blender 5.2.0 LTS; unicorn/pefile from project venv
working_directory: /home/dev/ABLPC
configuration: scripts/map-original-levels.py (default engines 1..16) over work/copies/BUGS_PC-full-disc/PC/BUGS/CD
artifacts:
  - reports/original-levels/EXP-20260927-001.json
  - work/level-projects/original-levels/
addresses: ["0x004671D0", "0x004498F0", "0x00453FF0", "0x00454B70", "0x0045A7F0", "0x0044F8E0", "0x00417720", "0x00456A90", "0x004ABE00", "0x004AC460", "0x0043E6B0", "0x0041C420", "0x00463C80", "0x004DC7E8"]
file_offsets: []
result: confirmed-bounded
created: 2026-09-27
updated: 2026-10-02
tags:
  - re/experiment
  - implementation/blender
---

# EXP-20260927-001 - Complete original level Blender maps

## Date

2026-09-27.

## Question

The user asked to map "the rest of the OG levels" as was done for Training and
to "make sure you get all the objects". Can the Training mapping generalize to
every remaining original level without dropping scene records, pickups or
creatures, and without inventing identities?

## Binary SHA-256

Retail `bugs.exe` `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
(`work/copies/BUGS_PC-disc/bugs.exe`). All 51 level source hashes (DAT, RAW,
terrain for engines 1–17) are pinned in `reimplementation/ablpc/original_levels.py`
and repeated per level in the report. They match earlier notes for LEVEL01,
LEVEL03, LEVEL06 and Training.

## Environment

No game, emulator or debugger ran. No live memory was read or written. Native
routines ran only in Unicorn on the hash-locked retail image, through the
existing `scripts/terrain-retail-probe.py` harness. Blender ran headless.

## Configuration

`.venv/bin/python scripts/map-original-levels.py` maps engines 1..16 into fresh
folders below `work/level-projects/original-levels/`. `--publish-report` writes
the asset-free summary. Training (engine 17) keeps its existing richer map
([[PC original Training Blender mapping]]).

## Procedure

1. **Engine to file rule (static).** `004671D0` subtracts 10 and adds `0x140`
   to `005C5E88` for engines above 10. Bits 6–7 choose the RAW name and bits
   8–9 choose DAT (`level1.dat` at `0x004DE5B4`, `level.dat` at `0x004DE5E4`)
   and terrain (`004A8950`, `terr1` at `0x004E7AA4`). The rule is therefore
   engines 1..10 → `LEVELnn/LEVEL.*` + `TERRAIN.ALL`; 11..17 →
   `LEVEL(n−10)/LEVEL1.*` + `TERR1.ALL`. The flag is zeroed at the end of the
   load. Earlier runtime logs independently confirm engines 1, 3, 6 and 17.
2. **Scene records.** Census of all 17 DATs: masked dispatches 1, 2, 3, 4, 9,
   0x0A, 0x0C, 0x41, 0x49, 0x4C and one 0x83. `004498F0` cases: 1/9/0x41/0x49
   ordinary meshes (`0045A7F0`, selector +19/+25); 4/0x0C/0x4C meshes with
   camera-relative origin and no selector (mostly negative-count meshes,
   decoded as in [[EXP-20260926-001 - Static Anthill remaining object inventory]]);
   2/0x0A camera-facing sprites (`00454B70`); 3 yaw-facing sprites (`00453FF0`).
   For dispatch 0x0A the sprite matrix is diag(object +0x12, +0x14, 0); the last
   `00454B70` argument (+0x16) multiplies quad +16 into depth, not size.
   Masked 0x83 has no case and is kept as a marker. The 0x20 family (cases
   0x21/0x24/0x29/0x2C) has no retail instance and is refused. Index tables
   between the scene lists (engines 3, 4, 14, 15) are preserved.
3. **Pickups.** Every type `0x3F` row. `00417720` cases give the selector
   labels: 0x10–0x13 letters, 0x14 grain, 0x20 weapon reset, 0x21–0x24 berries,
   0x29–0x2D seed-token counters `0059D9A8..0059D9AC`, 0x30 telescope, 0x31 a
   persistent, non-collected row sharing the telescope fall-through. Positions
   come from executing original `00456A90` over each level's table (XZ must stay
   unchanged).
4. **Creatures.** Every nonzero slot of the RAW type-35 table (the executable's
   "CreatListRam"). Every present type has exactly one RAW `0x102` packet whose
   second dword equals the type; its textured 36/48-byte ALL primitives are the
   displayed model in stored pose. Floor height below each slot uses `004ABE00`
   at the slot's own position, as `0041C420` does for flag 0x20 (no retail slot
   sets it). (Corrected 2026-10-02: `0x0041C52A` tests `+0x12` of the 28-byte
   row, raw byte 18. Over the 17 engines, read and hash-checked with this note's
   own `original_levels.read_inputs`/`creature_rows`, 130 seed rows (type 11)
   carry 0x38 there, which includes 0x20. No row has 0x20 in `+0x0E`, the
   reader's `flags`, which is the likely source of the original remark. See
   [[FUNC-97C95BA5572D-0041C420]].)
5. **Model tails.** Bytes after some model terminators were first drawn as
   geometry and produced giant white hexagons around seeds. Checking the corpus
   showed every vector has length 4096±64 and the index count equals the
   preceding primitives' corners (3 per triangle, 4 per quad), e.g. Anthill
   seed record 3: 18 triangles + 66 quads = 318 indices. They are recorded as
   per-corner normal tables and not drawn. Two Clover Forest type-27 tails
   do not fit and stay opaque with offset/length/hash.
6. **Flik start.** `0043E6B0` copies X/Z/heading from `0x004DC7E8 + engine*12`,
   sets Y to `0x80000000`, calls `004AC460`, then subtracts `0x100`. The same
   routine runs offline for the start marker.
7. **Blender.** `tools/blender/original_level_map.py` builds each scene, saves,
   renders `overview.png` and an unsaved-camera `overview-cutaway.png`, reopens
   the file and verifies every source object origin, mesh vertex, polygon count
   (plus dropped degenerate faces), pickup and creature location/raw bytes,
   collision triangle count and packed page count.

## Expected

All 9,673 scene records in engines 1..16 either drawn or explicitly kept; every
pickup and creature slot placed; Training and Cliffside counts reproduced by
the generalized path.

## Observed

- **Cross-checks.** The generalized extractor reproduces Training's
  12,414 vertices/7,953 faces/1,360 collision triangles (EXP-20260909-012) and
  Cliffside's 29,308/17,093 (EXP-20260914-010). The spawn table's Cliffside X/Z
  equals the runtime-confirmed 2930.71875/−4204.8125 exactly. The offline start
  rule gives Y −2617.25 against the live resting −2612.78 (Flik settles after
  the −0x100 placement).
- **Totals (engines 1..16).** 9,673 scene records: 9,672 drawn and one
  undispatched (Battle Arena `primary.165`, flags `0x93`). 936 pickups,
  525 creature slots of 40 types, 2,747 other stored rows, 108,972 collision
  triangles. Native pickup initialization succeeded in all levels.
- **Every level saved and reopened** with `save_reopen: passed`. Per-level
  counts, hashes and verification receipts are in the report.
- **Degenerate faces.** 100 source faces with fewer than three distinct corners
  (City Entrance 60 in 20 meshes; Battle Arena 40 in three meshes) exist only in
  `original-map.json`, not as Blender polygons.
- **Missing page.** City Square creature type 19 references page 18, absent
  from that RAW; it uses vertex colours only.
- **Interiors.** Top views show roofs (Council Chamber). Pickups there are
  present beneath overhangs, as confirmed by a close-up with the camera clipped
  just above the grain arc; own-position floor queries place those grains
  250–540 units above their floor.

## Artifacts

- `reimplementation/ablpc/original_levels.py`, `scripts/map-original-levels.py`,
  `tools/blender/original_level_map.py`, `tests/test_original_levels.py`.
- `reports/original-levels/EXP-20260927-001.json` (metadata only).
- Private: `work/level-projects/original-levels/<progression>-<name>/` with
  inputs, pages, `original-map.json`, reports, `level.blend`, overviews.

## Addresses

`004671D0`, `004A8950`, `004498F0`, `00453FF0`, `00454B70`, `0045A7F0`,
`0044F8E0`, `00417720`, `00456A90`, `0041C420`, `004ABE00`, `004AC460`,
`0043E6B0`, `00463C80`, table `004DC7E8`.

## File offsets

Per-object record/object/geometry offsets, pickup row offsets and creature
packet offsets are stored on each Blender object and in `original-map.json`.

## Interpretation

**Confirmed:** the file rule, dispatch coverage, pickup/creature placement
inputs and the offline native initializers above. **Inferred:** the normal-table
reading of model tails (structural fit, consumer not localized); fourteen
"looks like" creature hints from rendered model galleries; the engine-16 stage
looks like a circus tent. **Unknown:** identities of 32 creature types (14 carry appearance hints), selector
0x31's role, the undispatched 0x83 row's purpose and the seed's far-offset parts.

## Result

Confirmed within its bounds: sixteen complete reference maps exist and pass
their save/reopen checks. They are maps, not compilers; no runtime appearance
comparison was made in this experiment.

## Follow-up

[[PC original level Blender maps]] owns use and maintenance. Candidate
discriminators: localize the normal-table consumer; watch one creature type's
spawn in a live session to name it; compare one level's live pickup Y with the
offline `00456A90` result.
