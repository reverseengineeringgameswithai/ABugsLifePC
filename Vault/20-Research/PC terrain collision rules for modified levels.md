---
type: research
status: confirmed-bounded
created: 2026-10-29
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260907-007, EXP-20260909-002, EXP-20260911-002, EXP-20260914-010, EXP-20260914-012, EXP-20260928-001, EXP-20261005-003]
tags: [re/collision, terrain/authoring, re/level-data, re/static]
---

# PC terrain collision rules for modified levels

What the original collision code requires of added or moved collision, and
which original objects in Level01 (Anthill) and LEVEL06 (Cliffside) have
collision of their own. The grammar of the files is in
[[PC TERRAIN ALL collision descriptor source]] and
[[PC TERRAIN ALL barrier strips]]. Experiments cited as plain IDs are not in
this vault; they added floors, walls and hazards to test builds.

## Units and the contact offset

- A stored coordinate is 32 runtime world units ([[PC scenery render distance]]).
- Collision floors sit 96 stored units below the visible surface: floor and
  top collision is visible Y − 96
  ([[EXP-20260905-004 - Playable ramp and box area]]). Floor triangles built
  from visible terrain triangles are written with their winding reversed
  (EXP-20260907-007, checked against the original loader `0x004A8410`, the
  movement coordinator `0x004AB1A0`, DAT relocation `0x0044BB70` and the
  scene gate `0x0044D59F`).
- **Measured.** Floor cells whose planes were at stored Y −378 supported
  Flik's feet at Y −282 (runtime −9024), with small native settling
  differences (EXP-20260914-012). New floor records there reused the guarded
  original source-99 descriptor fields as tag 6 / result 0 records, leaving
  every original source record, payload and suffix exact.

## Descriptors and result words

- **Descriptor numbering.** The loader `0x004A8410` assigns one descriptor per
  source of kind below 256; high-kind records take none, so an added source 229
  became descriptor 216 in one build ([[FUNC-97C95BA5572D-004A8410]]). Source
  and descriptor indices are not interchangeable.
- **Result words.** Result 1 is instant death and result 4 damage, and the
  safe-position update `0x004189E0` excludes result 4
  ([[FUNC-97C95BA5572D-004ACF90]],
  [[EXP-20260907-027 - Native respawn cycles and exit-aware traversal]]).
  EXP-20260907-027 also found that result-1 terrain can become the native saved
  return, which causes repeated deaths. EXP-20260909-002 therefore gave an
  added hazard floor result 4, which keeps it out of the saved return, and
  made it lethal through a hook on the collision query.
- **Where a hazard can hook.** Flik's post-movement collision query is the call
  at `0x004408AC` ([[STRUCT-PC-FLIK-POSITION-GLOBALS]],
  [[PC test-area exit placement]]). After a death the outer loop's reset call
  at `0x0043DCA1` runs the native respawn `0x0042DDB0`, which places Flik from
  the auxiliary XYZ `0x0059D960`/`64`/`68` and the heading word `0x0059D988`.
  EXP-20260909-002 wrapped both. It saved those values, installed a local
  return point for one death, called `0x0042DDB0`, and restored them, so the
  next ordinary death used the normal reset. In hardware, two deaths on the
  added floor took lives 5 → 4 → 3 and reset Flik to the chosen safe contact.
- **Protection timers.** The instant-death argument of `0x0041C6C0` bypasses
  both protection timers; see [[PC gameplay loop and player event sites]].
- **Code room.** EXP-20260909-002 placed its helper in existing CC padding at
  `0x004BC000` in `.text`.
- **Fixture caveat.** In original-instruction replay, constant-Y 512 fixture
  movement over sloped ordinary and lethal surfaces showed isolated one-frame
  airborne flags. An "every frame grounded" check is too strict; landing and
  result-4 contact discriminate continuity (EXP-20260909-002).

## Barrier strips

- Kind-0x101 strips are linked through `0x007F3D3C` for the movement
  coordinator ([[FUNC-97C95BA5572D-004A8410]]). The normal terrain loader leaves
  `0x007F3D60` zero, so code that needs the strips has to follow the chain from
  `0x007F3D3C` (EXP-20260911-002 bounded it at 128 links). The native collector
  sites are `0x004AB5B7`, `0x004AB626` and `0x004AB731`.
- **Height-independent.** A strip blocks across its X/Z boundary at any
  height, so a closed strip also stops a jump over it (EXP-20260911-002; the
  original response at three widely separated heights is in KU-080's history,
  [[Known Unknowns history through 2026-09-26]]).
- **Moving a strip.** EXP-20260911-002 lowered an added strip by 22 stored Y
  units per update over 50 updates. It stayed solid the whole way, as a
  height-independent barrier should, until its count was set to 0 at 1100
  units of travel; hardware runs confirmed the closed and opened states.
- **Zero magic word.** The loader expects the magic `0x12345678` at a strip's
  `+0x00` ([[PC TERRAIN ALL barrier strips]]). EXP-20261005-003 treats a strip
  with a zero magic word as inactive (inferred from that grammar). In the
  project's pinned base terrain the original Level01 strips 179–187, including
  the large barrier 180, already had a zero magic word; where that was done is
  not traced.

## Original Level01 prop collision

Static, first recorded in EXP-20261005-003. Each enabled original scene object
was posed in world space by the retail matrix routine `0x00463C80`. Each kind-6
source's cells gave world triangles (record XYZ + first vertex + two edge
vectors), and each shell was paired with the overlapping object whose mesh lay
closest. Small kind-0x101 strips paired with the object at their centre.

- **Fit.** 70 sources pair with one object each. The median distance from
  shell vertex to object mesh is 59–177 stored units; the five pairings already
  in use fit at 59–165. Every source below has kind 6, `+0x44` = −1, `+0x46` =
  0 and result 0.
- **Pairing is inferred.** The pairing rests on spatial fit, not on an
  explicit scene-to-terrain link.

| Family (primary) | Placements with their own collision | Sources | Shape |
|---|---|---|---|
| Loose leaf (p14) | 4 of 4 | 127 (record 232228, payload 140156, 1548 bytes), 128, 129, 174 | 35–47 triangles, mostly facing up: a standable leaf |
| Hollow plant (p209) | 2 of 2 | 87 (229188 / 988, 1056 bytes), 170 | 28 triangles, 24 facing sideways: walls round the cup |
| Broad leaf (p227) | 1 of 1 | 175 (235876 / 213992, 1932 bytes) | 55 triangles |
| Yellow upright leaves (p196/197/198/201) | 8 of 8 | kind-0x101 strips 183, 182, 181, 179 (records 236180–236484) and 184–187 | a 4-segment loop about 250×200 round each stem, centre 14–64 units from the leaf origin; blocks sideways, no top |
| Mushrooms, large stones, forked twigs | every placement | 131–152, 153–158/163/165/171, 168/169/173 | |
| Thorny vine | 3 of 13 | 90, 91, 176 | |
| Leaf statue; offering stone and curled leaf; curved stone and branch | 1 each | 89, 88, 130 | |

No dedicated collision was found for clovers (28 placements), flowers (15),
daisies (8), green shoots (114), two-leaf sprouts (7), any of the 18 grass
patches, the end-of-stage marker or the plant base (p214, inside source 87's
footprint). Near the three original telescope pickups there are only ground
sections (101, 107, 108, 113). Small and round stones (112 placements) have no
paired shell at these thresholds, and four small unpaired sources (159–162,
10–16 triangles) lie among stones. [[PC Anthill scenery assemblies]] lists the
record and payload offsets of the shells that were later moved with their
objects.

## Original LEVEL06 collision

LEVEL06 is Cliffside, engine 6 ([[PC level roster and numbering]]). Its
original map has 126 resolved collision sources with 10,089 triangles and 340
barrier segments, among 134 source records (EXP-20260914-010, EXP-20260914-012;
the face count is reproduced in
[[EXP-20260927-001 - Complete original level Blender maps]]). Its scene layout
is in [[PC scene admission and DAT layout rules]]. The bird's
height band that ends a run there is a level routine, not collision; see
[[PC boss level routines and creature transplant limits]].

## Plants as platforms

First recorded in EXP-20260928-001 (static queries and original-instruction
runs; hardware in a test level). [[FUNC-97C95BA5572D-00467E60]] holds the
forced-seed index rule and the plant type table `0x004DE9F0`.

- **Forced bytes in original data.** Fixed and pre-grown seeds carry forced
  bytes, for example LEVEL03 slot 15 (`04 02 12`) and LEVEL09 slot 5
  (`03 01 11`). The LEVEL06 `LEVEL1.RAW` ring covers every type.
- **Colour sequences.** With no forced byte, brown (colour 0) steps through
  the mushroom, the propeller, type 8 and the cannon; green (colour 2) through
  types 7, 4, 10, 9 and 1.
- **Updraft.** The plant update `0x00468010` gives type 3 an updraft of radius
  40 in units of 256, over the vertical band `0x3000`–`0xA000`. Type 3 has no
  PLANTTER template.
- **Passive platforms.** Types 1, 4, 9 and 10 have no update case.
- **Heights.** PLANTTER record 0 (type 1) has cell heights clustered at about
  335, 655, 945 and 1,235 units above the base. Record 1 (type 10) is a flat
  leaf at about 790.
- **Reach.** In hardware a forced brown seed grew type 3 and its updraft
  carried Flik onto a plateau 1000 units up. A forced green seed grew type 1
  and Flik hopped up its leaves to the same height; that climb was seen only
  in an arm where a physical controller may also have been driving.
