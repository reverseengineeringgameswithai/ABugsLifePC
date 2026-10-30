---
type: file-format
id: FMT-PC-LEVEL-DAT-STATIC-MESH
status: confirmed-layout
created: 2026-08-18
updated: 2026-10-02
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence:
  - EXP-20260818-006
  - EXP-20260818-007
  - EXP-20260818-008
  - EXP-20260819-001
  - EXP-20260819-002
tags:
  - re/file-format
  - re/rendering
---

# PC LEVEL DAT static mesh

[[EXP-20260904-007 - Deck visibility and inherited depth offset]] documents a bounded type0x41
object field at+0x12 that adds byte×8 to emitted depth words. EXP-006 retained
value8; [[EXP-20260904-008 - Block depth offset runtime comparison]] now verifies the bounded
zero-offset correction by live removal/restoration. The field also adjusts a
scene distance threshold; clearing every native object is not supported.

[[EXP-20260904-009 - Paused side-view depth interpolation]] finds residual
visibility error with byte0. Original drawing on captured state reproduces the
static buffer's projected vertices and implicates large-face depth interpolation.
A finer prefix improves sampled depth ordering offline; the user-authorized
[[EXP-20260904-010 - Paused subdivision live comparison]] then verifies the
predicted fragment disappearance and exact ROI restoration in that paused view.
Six other boundary samples remain. No general face-size/material rule or
all-view repair follows. Keep EXP-008/010 acceptance bounded.


Bounds-checked layout for the static indexed mesh reached from masked scene
dispatch `0x41`. This dossier confirms a byte grammar and its PC consumer. It
does **not** confirm that every such mesh is terrain, that either selected
causal candidate is visible ground, or the semantic names of colour/texture
fields.

## Bounded visible-ground example — 2026-09-04

[[EXP-20260904-005 - Raised floor and visible ground pairing]] moves17 signed vertex+2 fields
across primary meshes160/213/280 near Level01 spawn. Live scene/object pointers
and complete vertex arrays match the edited file. With identical actor/camera
values, the changed file alters visible ground and restoration reproduces the
entire21,630-pixel static comparison region. This narrows the earlier ground
identity uncertainty for this fixed group on the auto-hardware build. It does
not identify every type0x41 mesh, resolve material fields, complete the primitive
group grammar or stitch render/collision boundaries. The fixed companion uses
the existing guarded setter; no parser reinterpretation was necessary.

## Reference chain

For a scene record whose `+0x0e & 0xbfef == 0x41`:

1. Scene record `+0x10` is a relocated pointer to a 24-byte object.
2. Object `+0x14` is a relocated pointer to the mesh payload.
3. `FUN_004498f0` cases `1` and `0x41` read object `+0x14` at
   `0x00449b2c` and call thunk `0x00401604` to `FUN_0045a7f0` at
   `0x00449b32`.

The object fields at `+0x00/+0x04/+0x08` and the signed-short triple at
`+0x0c/+0x0e/+0x10` feed translation and rotation setup. Object bytes
`+0x12/+0x13` have instruction-bounded arithmetic but no confirmed semantic
names.

## Confirmed payload grammar

```text
int32 vertex_count
vertex_count * 12 bytes:
    int16 component_00
    int16 component_02
    int16 component_04
    int16 field_06
    uint8 field_08, field_09, field_0a, field_0b
uint16 tag
uint16 face_count
face_count records:
    tag bit 0 clear: 4 * uint16 vertex_byte_offset, 4 * uint16 field_word
    tag bit 0 set:   3 * uint16 vertex_byte_offset, 3 * uint16 field_word
```

Each vertex reference is a byte offset from the first 12-byte vertex and must
be divisible by 12 and less than `vertex_count * 12`.

`EXP-20260818-006` validates this over all **2,543/2,543** type-`0x41`
objects in the 21-file retail corpus: 146,030 vertex references, zero invalid.
`EXP-20260818-007` adds a reconstructive round trip through
`StaticMeshPayload.to_bytes()`: all 2,543 payloads reproduce their exact source
span. The parser preserves all offset-named fields and rejects impossible
counts, truncation, misaligned references, and out-of-range references.

## Instruction-level consumer

Raw disassembly of retail `bugs.exe` closes the R0 partial code-to-data link:

- `0x0045a81e`: sets the vertex base to payload `+4`.
- `0x0045a89b`-`0x0045a89e`: advances by `vertex_count * 12` to the tag.
- `0x0045a8c3`-`0x0045a8d7`: reads the tag, masks its low five bits, and
  dispatches on bit 0.
- `0x0045c79c`-`0x0045c7b2`: the even-tag/quad arm skips the four-byte
  tag/count header, extracts `(tag >> 8) & 0x1f` and `tag & 0x60`, and reads
  `face_count`.
- `0x0045c822`-`0x0045c89e`: reads four face `uint16` values and uses them
  directly as byte offsets from the vertex base, loading each vertex's first
  eight bytes. The same function reads vertex `+8` as three byte channels in
  its output construction.

The observed tag values therefore have these **structural**, not semantic,
fields: `tag & 1` selects triangle/quad arity; `tag & 0x1f` selects an internal
branch; `tag & 0x60` contributes output flags; `(tag >> 8) & 0x1f` indexes
`DAT_005836a4`. Whether these mean culling, material, texture page, or another
render state remains unknown.

## Exact R2 causal candidate

Retail `CD/LEVEL03/LEVEL.DAT`:

- SHA-256: `bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b`
- primary scene record 167 at `0x23a0`, flags `0x0051`
- object at `0x3cd4`, geometry payload at `0xc504`
- 474 vertices, tag `0x0060`, 205 quads
- vertex 0 at `0xc508`: `(476,-891,-3470)` plus offset-named bytes
  `00 00 08 14 18 00`
- face 0 at `0xdb44`: vertex byte offsets `(0,12,24,36)`

The guarded candidate changes only vertex-0 component `+0x02` at file offset
`0xc50a`, from `-891` (`85 fc`) to `1157` (`85 04`), a `+2048` local-axis
delta. Only byte `0xc50b` differs. The predicted derived DAT SHA-256 is
`492a53e8f32a2416a400ac4127c01938d3438bf3bc5fe8b5b5a34639581adf80`.
Because the object Euler triple is `(0,0,0)`, the bounded prediction is that
one corner of face 0 moves by `+2048` along the transform's second input axis;
screen direction, world scale, surface identity, and visibility remain Gate-C
unknowns. No derived file was launched in R1.

## Tooling boundary

`reimplementation/ablpc/level_dat.py` exposes `static_mesh_reference()`,
`static_mesh_references()`, reconstructive `to_bytes()`, and
`set_static_mesh_vertex_component()`. The edit requires record index, vertex
index, component offset, and expected original signed value. It edits a returned
byte string only; packaging/insertion and runtime acceptance are unsupported.

*Update (2026-10-02 audit):* insertion is no longer wholly unsupported.
[[EXP-20260905-006 - World-scale terrain tiling and checked mesh growth]] adds
checked growth: `terrain_texture_tiling.append_mesh()` appends a mesh before a
moved final end-relative dword and repoints object `+0x14`, checked against
the retail `0x0044BB70` relocator. `terrain_foliage.append_scene_mesh()`
(EXP-20260906-011/012) also rewrites the scene bound and requires an
unrotated, unscaled target. In-place resizing with relocation of every
file-relative pointer is still not implemented.

## Remaining gates

- R2: open. The first explicitly authorized control/candidate/control Direct3D
  run was procedurally valid but failed its control-agreement gate before
  effect classification. A successor must establish a stable camera or steady
  state and independently prove the selected face is in view.
  *Narrowed 2026-09-04:* EXP-20260904-005 (top of this note) gives one bounded
  visible-ground example; face 8 and general mesh identity stay open.
- R3: insertion/resizing and all affected file-relative relocations.
  *Narrowed 2026-09-05:* append-only growth exists (Tooling boundary above);
  in-place resizing does not.
- Field semantics: coordinate/world scale, `field_08..0a`, face field words,
  and tag branch meanings.
- Type-`0x01` variants remain outside this confirmed type-`0x41` scope.

## Anthill R2a primary candidate

[[EXP-20260818-008 - R2a Anthill static mesh causal candidate]] selects the
retail Level01 / Anthill primary record 81 rather than reopening the
corpus-wide grammar:

- source SHA-256
  `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`;
- record/object/geometry offsets `0x1B58 → 0x4860 → 0x188CC`;
- face 8 references vertex-byte offsets `(300,312,264,324)`;
- vertex 25 at `0x189FC` is referenced by face 8 only;
- guard component bytes `7B 13` at `0x189FE`, replace with
  `7B 1B`; the sole physical change is `0x189FF: 13 → 1B`;
- expected derived SHA-256
  `c76586991cb4cede5d58a3cae8278aca80ba2082130dcf33062b698334db0a4c`.

The zero-rotation object arithmetic predicts the selected object-translated
tuple changes from `(0,-3205,1000)` to `(0,-1157,1000)` while no
other face changes. The object and geometry offsets each have one Level01
scene reference. Axis semantics, world scale, and calling this a visible
ground corner remain R2 unknowns.

## Anthill R2b runtime result

[[EXP-20260819-001 - R2b Anthill static mesh causal runtime]] completed valid
retail/candidate/retail hardware-Direct3D arms with the exact one-byte Level01
candidate. The frozen comparison found only `108 / 307200` pixels identical
across all 30 control frames, so its `0.75` control-agreement gate failed before
effect classification. The result is inconclusive: it neither rejects the
candidate nor confirms that the selected mesh is visible ground. Face 8 was not
independently proven to be in view.

## Anthill R2c independent localizer

[[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
freezes an orthogonal topology test before any new one-byte vertex run. Face 8
at `0x18d38` has byte-offset tuple `(300,312,264,324)`, selecting vertices
`(25,26,22,27)`. The guarded localizer changes only three low bytes to produce
`(300,300,300,300)`, making both quad triangles zero-area without relying on
axis, scale, colour, UV, material, or tag semantics. A new bounds-checked API
requires exact record/object/geometry/face identity, arity, alignment, range,
original tuple, and reconstructive reparse.

Historical pre-run plan: the localizer was then unwritten and unrun. After explicit authorization, an
evidence-backed retail-only freeze calibration must pass before exact
control/localizer/control arms. A positive, localized surface hole would prove
that exact face contributes visible pixels at the frozen state; it would be
called ground only if the retained visual localization lies on the floor.

## Links

- [[PC LEVEL DAT prefix]]
- [[EXP-20260818-006 - R0 the static mesh format and where visible ground lives]]
- [[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]]
- [[EXP-20260818-008 - R2a Anthill static mesh causal candidate]]
- [[EXP-20260819-001 - R2b Anthill static mesh causal runtime]]
- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)]]

## 2026-08-19 face-8 causal-localizer result

[[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
completed a derived-build `C1/L/C2` intervention with exact controls and clean
provenance. The comparison rejected localization: 18,612 changed pixels form
353 components and the largest contains only 53.3957% of the change. The L
image identity also exists in unmodified retail evidence. This leaves face-8
visibility, terrain identity, and the type-`0x41` retail causal link unconfirmed;
it is neither a positive nor a no-effect result.
## 2026-08-19 causal-status addendum

The type-`0x41` static decode and face-8 topology facts remain unchanged, but runtime visibility is still open. The auto-hardware C1/L/C2 packet was procedurally valid and inconclusive because it lacked an accepted repeatable live-control phase; it did not confirm or reject face 8 as rendered ground.

EXP-003 D1 rejected and established no exact sampled period or mask. EXP-004 then rejected its phase-sensitive full-frame gate. [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] ran two procedurally valid controls but rejected because D2 had 233 observations at 198 unique pixels outside D1's mask; visual review aligns the residual with Flik's silhouette. No accepted mask exists. This does not promote or reject face 8, terrain, material, world scale, collision, causality, or retail behavior.

[[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] accepted the frozen combined design mask on one fresh finite-grid control without expanding it. This remains control calibration and does not promote any mesh semantic or causal claim.

## 2026-08-19 R2h finite-grid prerequisite

EXP-006 produced zero observations outside the frozen combined nuisance mask on one fresh 121-frame derived-build holdout. This does not identify face 8 as visible terrain or alter the static type-0x41 decode claims. It only permits preparation of a separate bracketed face-8 localizer packet; R2 and retail confirmation remain open.

## 2026-08-19 R2i replicated face-8 packet

[[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] freezes two independent applications of the exact face-8 tuple mutation `(300,312,264,324)->(300,300,300,300)` at geometry `0x188CC`. The packet can test whether that tuple contributes a reproducible localized rendered region in the derived build. It does not change the static type-0x41 grammar or establish terrain semantics.

## 2026-08-19 replicated face-8 runtime boundary

[[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] independently created two byte-identical guarded Level01 DATs at SHA-256 `9942e252...11bfd`, each changing only face 8 from `(300,312,264,324)` to `(300,300,300,300)`. All four `C1/L1/L2/C2` runtime lifecycles passed on derived auto-hardware build `1e1d...c41f`, but the localization gate was inconclusive.

The aggregate result (`723e03ed...a309`) records 251 control mismatches outside the EXP-006 mask, 228 L1/L2 disagreements, and zero static core. L1 had no outside-mask difference; L2's sole 228-pixel frame-35 difference was exactly reproduced by C2 frame 35. Therefore this packet does not prove that face 8 is visible, ground, terrain, or causally connected to those pixels, and it does not prove no effect. The static face grammar and exact guarded mutation remain valid; the runtime visibility join remains open under KU-079.

## Fixed replacement stream — 2026-09-04

[[EXP-20260904-006 - Flat deck and solid block test]] replaces primary160’s first394 bytes with24
vertices and six tag0x60 quads, followed by0xffff. Retail0045A8B0/0045A8B4
confirm the group-word terminator; live bytes and the visible deck/block validate
this single-group construction. Remaining old bytes stay unreachable after the
terminator. This does not decode every tag or multi-group stream variant.

## Training ground depth offset, EXP-20260911-010

[[EXP-20260911-010 - Training floor occlusion and platform underside]] independently
isolates0x41 object byte+18:00449B22–00449B32 passes byte×8 to0045A7F0, while the
surrounding dispatcher temporarily adjusts its threshold. Training primary57..72
use9 in retail and the bank. An offline original-x86 byte-only9→0 comparison
retains all259 emitted X/Y/RHW/color entries and indices and decreases every Z
by exactly72/4096. Clear hardware views then cover Flik/seed with nearer ground.
This establishes the field's depth effect for this dispatch; do not transfer its
layout to rotated0x59 objects. Production changes16 object bytes, not floor meshes.
The experiment retains interpolation, grass, camera-phase and coverage limits.
