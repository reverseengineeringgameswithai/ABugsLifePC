---
type: research
status: active
updated: 2026-10-29
tags: [research/anthill, terrain/authoring]
---

# PC Anthill remaining object inventory

**Confirmed static inventory:** [[EXP-20260926-001 - Static Anthill remaining object inventory]]
accounts for all original Anthill scene records, their geometry, texture pages,
RAW actor slots and DAT pickup entries. It compares those with the
then-current importer donors. No assets were added. No game, Blender or
native-code emulation ran in this experiment. [[PC Anthill scenery assemblies]]
records the later import of the useful prop families (EXP-20260926-002).

## Scope and evidence

The inputs are private copies of the original PC Anthill DAT, TERRAIN, EXE and
`LEVEL01/LEVEL.RAW`. Full SHA-256 bindings and all record,
object and geometry offsets are in
`reports/anthill-inventory/EXP-20260926-001.json`.
The private, searchable gallery is
`work/experiments/EXP-20260926-001/verified/index.html`.

The source DAT contains **624 records: 484 primary and 140 secondary**, referencing
**218 different geometry offsets and 218 different complete geometry hashes**.
The independently parsed prefix and 1,248 checked scene/object pointer fields
agree. Geometry consists of 209 positive meshes, one negative-count mesh,
seven yaw-facing sprite batches and one camera-facing berry sprite batch.

| Coverage against explicit importer donors | Primary geometry | Secondary-only geometry |
|---|---:|---:|
| Whole geometry represented | 26 | 0 |
| Partly represented | 0 | 2 |
| Outside donor coverage | 126 | 64 |

This is **not 190 newly identified object types**. Many records share artwork;
many unique geometries are landscape sections, grass arrangements or simpler
secondary versions. “Represented” means a whole geometry falls within a mapped
donor footprint, not that every native placement/scale/animation is exposed.
Upper-tree secondary 17/18 contribute selected faces only. The tree, mound,
eight grass donors, clover variants, two mushrooms, berry pair, two flower
instances, marker, leaf statue and fence donor are explicitly mapped in code.

In an edited DAT, retained original geometry bytes do not show that a record
still draws: `004498F0`'s masked dispatch, rather than mere retained bytes, is
the static discriminator. Drawing eligibility is not a runtime visibility test.

## Useful remaining prop candidates

**Inferred appearance:** names below describe inspected local mesh/UV drawings.
Numbers and offsets are confirmed source metadata; gameplay roles are not
established by resemblance. `p` means original primary record.
Selectors come from original object byte+19 (unscaled) or +25 (scaled).

| Appearance | Original record / geometry offset | Source placements | Selector(s) | Import considerations |
|---|---|---:|---|---|
| Small stone | p19 / `0x2D460` | 93 | 0 | 25 vertices, 21 faces; compact visual donor |
| Larger stone | p120 / `0x2CD74` | 9 | 0 | 41 vertices, 40 faces |
| Second small stone | p121 / `0x2D1D4` | 19 | 0 | Distinct complete mesh from p19 |
| Forked twig | p45 / `0x3459C` | 3 | 0 | 131 vertices, 125 faces; page 3 |
| Large forked branch | p438 / `0x37358` | 1 | 0 | 168 vertices, 160 faces |
| Loose green leaf | p14 / `0x2C3D4` | 4 | 0 | 45 vertices, 36 faces |
| Broad veined leaf | p227 / `0x2C82C` | 1 | 0 | 53 vertices, 46 faces |
| Curled green leaf/stalk | p131 / `0x2E7B4` | 1 | 0 | 51 vertices, 32 faces |
| Arched thorny vine | p245 / `0x2D6EC` | 13 | 0 | 130 vertices, 96 faces; damage/collision role unknown |
| Cap platform on rock-like supports | p132 / `0x30624` | 1 | 0 | 357 vertices, 340 faces; 9,718 stored bytes; collision mapping needed |
| Curved rock/log-like platform | p315 / `0x42338` | 1 | 0 | 151 vertices, 147 faces; collision mapping needed |
| Single green shoot | p24 / `0x2F59C` | 52 | 2, 6, 10, 14 | Retain native matrix selection; 18 vertices, 8 faces |
| Alternate green shoot | p25 / `0x2F2F8` | 62 | 4, 8, 12, 16 | 34 vertices, 16 faces |
| Two-leaf sprout | p84 / `0x2EC28` | 7 | 3, 7, 11, 15 | 72 vertices, 54 faces |
| Alternate daisy flower | p180 / `0x334C4` | 8 | 1, 5, 13 | Distinct 67-vertex/52-face mesh from imported p90/91 |
| Four yellow upright leaves | p196/197/198/201 / `0x353A0`, `0x36A04`, `0x36D20`, `0x3703C` | 2 each | respectively 2/10; 2/14; 6/14; 14 | 32 vertices, 26 faces each; four meshes, not four copies of one |
| Hollow green plant cup | p209/404 / `0x2F700` | 2 | 0 | Negative-count format; see below |
| Brown circular base | p214/405 / `0x3051C` | 2 | 0 | 13 vertices, 6 faces; companion interpretation is provisional |

The practical first batch would be the stones, twig and loose leaves: bounded
ordinary geometry, available pages and no selected animation matrix. This is
a readiness inference, not an existing import command. Donor selection,
material/flag profiles and compiler behavior still need implementation and
verification. Retain opaque bytes and original controls.

## Landscape, fences and secondary artwork

The other 99 primary candidates were visually grouped as 38 ground sections,
24 earth walls, 18 grass strips/tufts, 12 bark/root walls, five earth/rock chunks
and two woven-looking walls. These are appearance groupings, not new collision
or material semantics. All 126 primary candidates have gallery cards and
source locators; the six fence arrangements and 21 other prop geometries make
up the remaining 27 candidates.

The seven native fence sprite batches contain 193 quads. p118 (`0x44140`)
supplies the existing 32 variants. The other six batches are p13 (`0x45048`),
p80 (`0x455B0`), p108 (`0x46A20`), p111 (`0x45B54`), p202 (`0x4629C`) and
p267 (`0x448C4`): **161 additional quads**. None exactly matches a donor quad,
even comparing the first 28 bytes without vertex colour/suffix and excluding
group centers. This does not imply 161 new textures or semantic prop types.
They reuse the existing fence artwork with different stored shapes/UV/control
records. Existing sprite parsing can inspect them; exposing their variants
requires an expanded checked donor set and collision policy.

All 66 secondary-only meshes were decoded and visually reviewed too, including
the two partially used upper-tree meshes. Their drawings show simpler ground,
root/wall, grass, yellow-leaf, clover, statue and platform forms. Appearance and
reduced topology suggest distant counterparts; this census does not prove a
one-to-one primary/secondary pairing or native switch distances for each.
The gallery includes them after the primary candidates, so they are not lost
or counted as wholly new prop families.

## Texture and animation dependencies

**Confirmed:** every scenery texture reference resolves to a decoded original
page in the RAW: pages 0,1,2,3,4. The 69-packet traversal locates page 3 later in
the stream at file offset `0x46CD9`; it must not be inferred missing from only
the initial packets. New object support includes its texture decoding and
material interpretation. The existing content cache may reuse already decoded
pages; no missing external texture source blocks this scenery inventory.
Native RAW actor resources are separate from these scenery pages.

`004498F0` distinguishes ordinary unscaled/scaled meshes, yaw-facing sprites,
camera-facing sprites and the dispatch 4 mesh path. Nonzero original selector
values select native matrices; that path and the known clover/prop readers
are evidence for preserving selectors, not for replacing them with static
Euler angles. The current `PropVisual.validate` permits only selectors 0/14
and a bounded material/flag set. The clover path separately handles its known
donors. Shoots, sprouts, alternate daisies and most yellow-leaf profiles need
additional validated support before matching their original motion.

## Negative-count mesh finding

**Confirmed static layout:** p209 and p404 use dispatch 4 and share geometry
`0x2F700`, whose initial signed count is −109. `004498F0` routes this path to
`0045A7F0`. The instruction sequence at `0045A82E..0045A8B4` locates commands at
`geometry + 8 + 18*N - 2*(N & 1)` for `N = -stored_count`; the positive path
uses `geometry + 4 + 12*N`. For this object, 109 ordinary vertex records end
at `0x2FC20`, followed by a **656-byte opaque span**, then commands at `0x2FEB0`.
The bounded research reader validates 102 faces, page 2 and the terminator at
the end of the 3,610-byte stored mesh. Full and auxiliary hashes are in the report.

The temporary positive view exists solely to inspect those stored vertices and
faces. Original bytes remain immutable, and the extra span's offset/length/hash
remain recorded. **Unknown:** auxiliary semantics, its runtime contribution and
the complete functional identity of the plant. Do not silently discard this
span in a production import, name it a launcher, or assume that decoding its
surface preserves native behavior. The next discriminator is a bounded audit
of this consumer's auxiliary-data reads and a separately authorized acceptance
experiment if full support is requested.

## Actors, pickups and collision

RAW tag 35 at file offset `0x49079` contains 64 actor slots: 32 active and 32 empty.
Active types are seven spiders 9, four mosquitoes 10, two pill bugs 39, five bees 13,
three caterpillars 40, nine seeds 11, one Dot 14 and one harvester 35. The five enemy
families, the original seeds and the Dot route each have their own authoring
note (below). The preserved
harvester slot is not a new generic scenery donor. This placement census does
not classify every unused animation/resource packet as an importable actor.

The DAT type `0x3F` list has 70 entries: 50 grain, four letters, four berries,
nine coloured tokens and three selector `0x30` telescopes.
Selectors and actor slots are recorded independently from scenery geometry.
See [[PC Anthill collectible authoring]], [[PC Anthill enemy authoring]],
[[PC fixed growable seed authoring]] and [[PC Dot flight path authoring]].

Original TERRAIN.ALL has 189 descriptors (178 type 6, ten 257, one 260). **Unknown:**
general exact pairing of remaining visual props with native collision sources.
No explicit DAT-scene↔collision link is established by this census; nearby
origins alone did not even reproduce the known leaf/mushroom pairings reliably.
(Later, 2026-10-05: EXP-20261005-003
pairs 70 sources by footprint overlap plus shell-to-mesh distance, which
does reproduce the mushroom, leaf and stone pairings.)
Use known donor evidence or establish each pairing before claiming solid,
walkable, damaging or interactive behavior. The diagnostic gallery omits
collision, native lighting, animation and instance transforms.

## Handoff

The full metadata report is the maintenance surface; private decoded artwork
stays under `work/`.
[[2026-09-26 - Codex - Inventory remaining Anthill objects]] records validation
and corrections to provisional research output. [[Known Unknowns]] retains
the import, collision, animation and resource-budget gates.
