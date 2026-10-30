---
type: cross-port
id: XPORT-20260818-007
date: 2026-08-18
source_id: SRC-PS1-ABL
source_commit: 1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
status: open
updated: 2026-10-02
tags:
  - research/cross-port
  - re/level-format
  - re/collision
  - re/gameplay
---

# XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads

> [!info] Policy
> Every PS1 item below is a **PS1 fact only**, cited to commit
> `1186eb6…` + relative path in the external read-only `SRC-PS1-ABL`. Nothing
> here is a confirmed PC claim; the "Transferable leads" are **cross-port
> inference** until independently confirmed on PC. No external content is copied
> into ABLPC. See [[Cross-Port Evidence Policy]], [[External Source Registry]].

## Bounded question

New PC level layouts are the project's ultimate goal, and terrain/collision is
the hardest half. The PS1 port is a **fully-RE'd sibling that already achieved a
constrained new-level replacement** — so: how did PS1 author/replace a level,
what were the enablers and blockers, and which format shapes transfer to the PC
as search leads? (Motivated by the 2026-08-18 three-way survey of PC level
format, PC collision, and PS1 authoring.)

## PS1 facts (cited @ `1186eb6`)

**Level = two on-disc files.** `LEVEL01/LEVEL.DAT` (objects + the *visible*
floor + geometry/instance tables) and `LEVEL01/LEVEL.RAW` (an **LZ-compressed
chunk container** holding collision, the occluded model arena, and the sky
table). Visible floor ≠ collision (`src_re_geometry/re_findings_backup.yaml`).

- **`LEVEL.RAW` chunk container.** Loader `fcn.8003a318` walks chunks; each has a
  0xe-byte header, is decompressed by LZ/LZSS `fcn.8001a1dc`, dispatched by
  subtype (`docs/GEOMETRY_RE_PLAN.md`). Chunk 32 = collision planes + sky;
  chunk 34/35 = occluded/actor model arena.
- **Runtime collision grid.** Converter `FUNC_80030F60` builds a **sector table
  at `0x800a7e48`** from chunk-32: LEVEL01 = 223 records, **0x30-byte stride**;
  each = origin XYZ @+0/4/8, block-ptr @+0x10, AABB @+0x14/+0x1c/+0x24/+0x28
  (`src_re/collision_grid_builder_800313a8.c`).
- **Collision surface = per-sector-flat origin-Y + a few oriented SWEPT PLANES**,
  *not* a scalar height and *not* a triangle mesh. LEVEL01 has exactly **6
  planes**. Plane record = **0x20 bytes, all s16**: normal XYZ (unit `0x4000`),
  reference point (stored `<<5`), face-extent/edge fields
  (`src_re/collision_plane_resolver_800345cc.c`). Resolver `FUNC_800345CC` =
  swept segment-vs-plane with a −0xc0 (192-unit) collision skin.
- **Object spawn table (`type-0x3f`)** = first `LEVEL.DAT` top record at off
  `0x4`, header `46 00 3f 00` = 70 entries × 0x10: `{s32 X, s32 Y, s32 Z, u8
  kind}`; **runtime = file `<<5`**. Kind enum: `0x14` grain, `0x10–13` FLIK
  letters, `0x21–24` berries, `0x29–2b` seed tokens, `0x30` checkpoint
  (`docs/LEVEL01_TYPE3F_MAP.md`). Append needs relocating **1248 baked offset
  fields** (`tools/dat_reloc.py`, `docs/DAT_FORMAT_AND_RELOCATION.md`).
- **Material** = 5-bit index in a chunk-35 primitive's last byte → runtime table
  `0x800A7DD8` (model layer); texpage/CLUT + per-vertex gouraud (DAT floor
  layer) (`docs/CHUNK35_MASTER_MESH_DECODE.md`).

**"Fast64" was never actually used.** It appears only as a *style analogy*
("SM64-romhack / Fast64 style"); the team explicitly rejected SM64/Fast64's real
formats (which rely on SM64 being fully decompiled) and built a **homegrown
Blender→disc pipeline** (`tools/TIER3_AUTHORING.md`,
`ObsidianVault/Mods/Other/MOD_native_blender_level_layout_export.md`).

**The pipeline (two tracks, `docs/TIER3_RENDERER_TRACKS.md`):**
- **Track A — custom CPU renderer + "cave" collision — RETIRED 2026-08-11.**
  Cold-booted a walkable authored level but *overdrew* native terrain and capped
  at ~700 tris. Its per-face segment-plane collision is the portable idea.
- **Track B — rewrite the game's own native structures — the live target.**
  Blender heightfield → profile JSON → `tools/build_g3_native.py` rewrites the
  native `FUNC_80010000` floor payloads (real GTE floor) **and** authors the
  collision sectors. One mesh; **slope classifies faces** (≤~45° walkable, >~45°
  wall); Blender Z-up → ABL −Y-up; 1 BU = 1000 ABL units.

**What shipped (WORKING, cold-boot + movie validated):** a **full-corridor
replacement of LEVEL01** — 7,800×37,100-unit authored world, **171/189 collision
sectors** + **42/42 visual payloads** regenerated with harvested material,
cold-boots, walkable, **contains Flik** (442,767 units driven, stayed inside)
(`docs/LEVEL_REPLACEMENT_STATUS.md`).

**Blockers (all format-shaped, none "unblockable"):** LEVEL.RAW LZ compression
(decompress→edit→recompress); collision is planes-not-tris (awkward walls,
fragile jump-containment); double size cap (decompressed chunk-32 ≲260 KB;
LEVEL.DAT under a ~388 KB / CD-sector budget); authored **render coverage pinned
to the 42 pre-existing floor-payload bboxes** until an undecoded cull/registration
record is cracked (a marker-flip experiment to add payloads was NEGATIVE)
(`docs/LEVEL_REPLACEMENT_BLOCKER_TRIAGE.md`).

## Transferable leads to PC (cross-port INFERENCE — confirm on PC before use)

- **Two-file split heuristic:** objects in a relocation-baked DAT-like structure;
  collision/mesh in a separate container. *PC divergence already observed:* PC
  put **collision in its own uncompressed `TERRAIN.ALL`**, and PC `LEVEL.RAW`
  holds **actor records**, not collision — so the PC split is *different* and, for
  collision, *friendlier* (no LZ).
- **Object spawn-table shape** `{s32 XYZ, u8 kind}` @0x10 stride with the small
  kind enum (grain `0x14`, letters `0x10–13`, berries `0x21–24`, tokens
  `0x29–2b`, checkpoint `0x30`) — the enum is the most likely thing to survive to
  PC. PC `type-0x3F` records are 0x10-stride grain/plant selectors (consistent).
- **`<<5` file→runtime scale** for objects and collision reference points — a
  candidate PC constant. (PC type-1 reset writes X/Z `<<5`, consistent —
  `FUNC-…-00432930`.)
- **0x30-byte collision descriptor stride** on both ports at runtime (PS1 sector
  table `0x800a7e48`; PC descriptor table `0x007F4590`) — a structural echo worth
  testing.
- **Authoring strategy** (the reusable asset, not any Fast64 tooling): one
  authored mesh, slope-classified faces, **rewrite native structures** rather than
  inject a custom renderer.

## PC outcome of the leads (2026-10-02 audit pointer)

Later PC-native evidence, recorded without promoting any PS1 item:

- **`<<5` scale.** Confirmed on PC for type-1 reset rows
  ([[EXP-20260815-117 - Approved Level03 row-6 reset rerun]]: `+128` stored X
  gives `+4096` reset X). PC `TERRAIN.ALL` descriptor bases are also shifted
  left five (`0x004A85AD`–`0x004A85DC`,
  [[PC TERRAIN ALL collision descriptor source]]).
- **`0x30` descriptor stride.** PC static evidence gives `0x30`-byte runtime
  descriptors at `0x007F4590` ([[FUNC-97C95BA5572D-004A8410]]). The stride
  matches; no shared field meaning follows from that.
- **Kind enum.** PC `0x00417720` cases label `0x10`–`0x13` letters, `0x14`
  grain, `0x20` weapon reset, `0x21`–`0x24` berries, `0x29`–`0x2D` seed-token
  counters, `0x30` telescope and `0x31` a persistent row
  ([[EXP-20260927-001 - Complete original level Blender maps]];
  EXP-20260915-005). Letters, grain,
  berries `0x21`–`0x24` and tokens `0x29`–`0x2B` match the PS1 labels. The
  PS1 list above has no `0x20`, `0x2C`–`0x2D` or `0x31`.
- **Contradiction kept.** `0x30` is the telescope on PC, not a checkpoint. On
  the PS1 side, `docs/LEVEL01_TYPE3F_MAP.md` marks `0x30` only as a
  checkpoint/trigger *candidate*, while the PS1 operator correction in
  `analysis/mechanics_baseline.yaml:846-861` calls it a telescope (see
  [[XPORT-20260815-002 - Level03 type-1 row respawn hypothesis]]). The
  "checkpoint" lead above overstated the PS1 doc. PC evidence settles only the
  PC side.
- **Authoring strategy.** PC independently built a Blender to PC-native
  writer pipeline (EXP-20260907-007,
  PC Blender level authoring) and has since shipped new rooms such as
  EXP-20260928-001.
- **Policy gap.** This note never recorded explicit unknowns or a
  discriminating PC experiment. The PC results above now test the leads they
  name. Everything else here remains cross-port inference.

## Links

- Cross-port siblings: [[XPORT-20260814-001 - Training grain selector and count]],
  [[XPORT-20260817-005 - Berry contact array and type marker shape]],
  [[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]].
- PC side: [[New-level authoring feasibility (PC)]] (the assessment this feeds),
  [[Cross-Port Evidence Policy]], [[External Source Registry]].
