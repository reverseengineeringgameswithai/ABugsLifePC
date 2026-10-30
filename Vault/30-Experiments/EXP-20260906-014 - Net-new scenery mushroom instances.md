---
type: experiment
id: EXP-20260906-014
date: 2026-09-06
status: offline-candidate-validated
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: guarded read-only Wine reference and offline original PC instructions under Unicorn
question: Can the visible scenery mushrooms be paired with collision and added as independent new instances?
result: three-copy offline control passes bounded gates; six-copy live acceptance follows in EXP-016
tags: [re/experiment, terrain/authoring, re/rendering, re/collision]
---

# EXP-20260906-014 - Net-new scenery mushroom instances

**Continuation:** EXP-20260906-016 uses
these donors/writer for six scattered copies, closes OG384409, verifies all
six resident instances and receives user approval/banking authorization.
This experiment's three-copy fixture remains unlaunched as a retained control;
its pending-preview/deferred-banking instructions below are historical.

User asks to map the mushrooms in the current original Level1 session and make
them addable as new instances, not reused original slots. Reference runtime is
EXP-20260906-013; no controls, live
writes, stops, debugger or original/mod-control-file mutations were used.
Candidate is offline only; banking is deferred.

## Render localization and separately bounded collision pairing

Private `work/experiments/EXP-20260906-014/memory.json` captures readable RAM
and a compositor frame over7.425s. Before/after/frame pose and camera agree:
XYZ(112885,-10389,577785), heading972, ground source108. This is asynchronous,
not atomic. Frame `og-preview-01/frame-1788750723757445624.png`, under EXP-013,
SHA `bbaaad90aa5e0780e94f8538c2b7a7a5a5edf297452608173c288a9cd937ca40`.

**Confirmed render localization:** original PC dispatcher0x004498F0 ->0x0045A7F0
executes in captured private RAM with retail .text restored, per-object draw
lists and cleared batches. `map.py` / `mapping.json` retain emitted geometry.
Mesh file offset179576,1626bytes,SHA
`6548dfda5403e8a7d3b8a2ddcae4a84ad3ca4bfdacebde7f308ba0a1cea2108e` is shared
by22 original primary placements:65 vertices,30 command0x60 quads and22
command0x8064 quads. Texture pixels remain external; the Level01 page0 resource
setup is required, not an arbitrary-level atlas importer.

| Visible prop | Primary scene / object offset | Native screen bounds X/Y | Collision source / payload |
| --- | --- | --- | --- |
| Tall right of Flik |344 /23384 |320..451 /140..278 |147 /174208,1464bytes |
| Foreground-left cap |342 /24120 |-4..268 /294..495 |142 /166888,1476bytes |
| Small behind Flik |396 /24336 |242..311 /234..286 |146 /172732,1476bytes |
| Further small mushroom |400 /22960 |225..280 /228..267 |148 /175672,1476bytes |

The four native silhouettes align with the captured mushrooms. Six emitted
XYZW values from scene396 occur exactly in retained live buffers; most emitted
vertices are not present in those asynchronously retained buffers. Do not claim
full live draw/GPU equivalence. Native Euler0x00463C80 plus the dispatcher’s
per-column scaling supplies a separate world-geometry census.

**Strongly supported pairing, not a direct cross-file pointer:** collision
sources are uniquely nearby with matching shape, footprint, orientation and
vertical extent. They are larger/simpler shells:40 triangles each,15 or16
groups, not vertex-identical render surfaces. Native landing/side tests below
support the tall344/147 and small396/146 pairs; the other two pairs have
localization/resident-byte evidence, not this new placement's movement gate.
Keep donor clearance; do not regenerate collision from the visible mesh or infer
a universal expansion radius. `final-runtime.json` verifies all four complete
scene/object/mesh records and full collision payloads against guarded live RAM.

These are scaled scenery objects: flags0x19 (masked case9, pass0x10),32-byte
objects, XYZ+0, rotation+12, scale+18, depth4 at+24, selector+25, mesh pointer+28.
Their static tag6 collision is distinct from seed-grown planttype5 /PLANTTER8
and its contact-dependent bounce. [[PC seed and mushroom collision state]].
A top landing here is support, not evidence of automatic plant bounce.

## Additive implementation and reproducible fixture

`terrain_scenery.py` and `terrain-scenery-fixture.py` add independent primary
records,32-byte objects and76-byte collision descriptors with copied payloads.
Original placements are not replaced. Retain rotation/scale, material words,
render pass/depth and complete shell; translate scene center, render origin and
collision origin together. Reusing the output as input adds more later. No new
seed/plant actor is allocated, and repaired PLANTTER stays byte-identical.

Original relocation stores0x0044BD12/21/47/57 and0x0044BE70/79/94/9D establish
the two pointer layouts;0x0044BB50 is a no-op. Insert primary entries before the
sentinel, rebase known old pointers, preserve the secondary table/unknown bytes,
and retain end-relative trailing data. Reject fixed/indexed tables, bit0x20
extra-pointer variants, overlapping/aliased objects, invalid pointers/counts,
coordinate overflow and explicit experiment budgets. This is not a general
level repacker; budgets are not established native format maxima.

Candidate `work/copies/EXP-20260906-014/mushroom-fixture` adds two tall props
at stored origins(6000,-3200,17000),(8000,-3200,17000), and a small one at
(4000,-3200,19000).484->487 primary records,189->192 collision source records;
source indices189..191 and scene indices484..486 are newly allocated. Native
runtime descriptors178..180 have tag6; high-kind original source records do not
consume matching descriptor slots. Original floor,473 foliage blades,15-segment
boundary, visibility bound14183 and repaired PLANTTER are preserved.

Rebuild with `.venv/bin/python scripts/terrain-scenery-fixture.py`, arguments:
`--base work/copies/EXP-20260906-012/fixture`,
`--original work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01`,
`--placements work/experiments/EXP-20260906-014/placements.json`,
and fresh `--out work/copies/...` /`--report work/experiments/...` targets.
Placements contain `variant` and absolute stored-unit `origin`; scale/rotation
editing and automatic collision-shell regeneration are deliberately unsupported.

Candidate DAT SHA `9529802b03e16506678bc40bd68362e3e806101aba3fe5a2aa060b4b0f13644b`;
terrain `cfb247925cee40979b294187b3ec43ca4439efb27015d31b5e5a9853695c00f3`;
PLANTTER `c8251790b317e0458525d898237a54a88d473aac0758d01f36effcebeb38a762`.

## Validation, contradiction and limits

- 33 new tests pass in0.73s: synthetic byte/pointer/footer preservation,
  invalid-input guards, incremental additions, original and banked-mod native
  relocation. Initial test invocation omitted PYTHONPATH and failed collection;
  corrected invocation ran all33, not a code failure.
- Terrain-selected `make check`:831 passed in38.99s, two workers, repository-local
  scratch; R2q deliberately excluded. No full-suite/R2p/R2q work or commit.
- `native-04.json`,20.596s: original full collision loader/initializer and DAT
  relocator preserve old records/payloads and resolve all three new objects.
  Three translated cap landings are coordinate/flag-identical to their donors.
  Twelve lateral comparisons pass at the stated control scope. Twelve paired
  grounded push/retreat cases differ from the same authored floor with only the
  target prop removed and return to floor99 successfully.
- **Retained contradiction:** full original-world small-prop west approach
  differs by385world units; it also contacts source108/file82120. Removing only
  that ground source’s first marker in private emulated control removes the
  difference, without changing donor or candidate. `native-01/02.json` preserve
  the rejection; `native-03/04.json` preserve the complete-scene mismatch as a
  non-required observation and require the explicit floor-removal discriminator.
  Do not describe all complete-scene comparisons as passing.
- `projection-candidate.json`: exact emitted XYZW, diffuse colour, UV and index
  equality for104+104+100 vertices at object/camera-translated captured views.
  Original draw instructions execute; no raster/GPU/pixel identity is claimed.

Native motion uses synthetic displacements/cadence, not input or a whole actor
replay. Arbitrary rotations/scales, all views, other levels/resources, projectile
behavior and live visual/contact acceptance remain open. Candidate not launched.
Next is a separately agreed mod preview switch and user appearance/contact test.
OG game384409 remains open; the current final audit accounts14 present identities,
three departed image-loader helpers, seven generic processes and one sink.

Public metadata and private evidence hashes: `reports/terrain/EXP-20260906-014.json`.
User offers further mushroom reference poses; take a fresh read-only capture
when they signal arrival. Current captured pose remains historical evidence,
not a requirement to keep Flik stationary during subsequent asset logging.
