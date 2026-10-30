---
type: experiment
id: EXP-20260818-006
date: 2026-08-18
question: 'R0 of the new-level authoring program: what actually draws each level''s visible ground, given that type-3 is a camera-facing billboard batch absent from 20 of 21 corpus files? Identify the payload format.'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: 'static analysis (scripts/ghidra-query.py + raw objdump) plus offline decode of the RETAIL LEVEL*.DAT corpus at work/copies/BUGS_PC-full-disc/PC/BUGS/CD/; no game execution, no target writes'
environment_version: 'ghidra-query current; export static/exports/BIN-97c95ba5572dce63/'
working_directory: /home/dev/ABLPC
configuration: 'offline; 21 retail LEVEL*.DAT files, of which 17 contain type-0x41 instances'
artifacts: []
addresses:
  - "0x0044D430"
  - "0x004498F0"
  - "0x0045A7F0"
  - "0x00448350"
  - "0x0044DE20"
  - "0x00405FE0"
  - "0x00407450"
file_offsets: []
result: 'Static mesh format for type-0x41 objects DECODED and validated 2543/2543 (100.00%) over 146,030 face indices on the RETAIL corpus, with a break-test showing competing grammars score 0-42%. Large flat instances of this type are the CANDIDATE visible ground (no runtime evidence; Gate C unrun). Also surfaced a non-relocated mod artifact (KU-082).'
created: 2026-08-18T23:30:00
---

# R0 — the static mesh format, and where visible ground lives

Executes **R0** of [[New-level authoring roadmap (terrain, collision, materials)]].
Gate A/B decoded the type-3 path and then established it is the **wrong target**
for terrain (a camera-facing billboard batch, present in only 1 of 21 corpus
files — [[EXP-20260818-005 - Decode the render-geometry command grammar (scope)]],
`KU-079`). R0 asks what actually draws visible ground.

## Method

Static-first, then data-driven. Enumerated every caller of the emit thunks and
mapped the scene driver's call tree; then, rather than descend a 150 KB drawer,
**followed the data**: in `LEVEL03` (which has **no** type-2/3/0xa instance at
all, yet obviously has ground), ranked instances by the `+0x0c` cull/bound value and decoded
what their objects point at. The resulting grammar was then validated across the
whole retail corpus and **adversarially break-tested** against competing
grammars.

## Confirmed — the object chain

- **Instance** (20 B, in the array whose pointer is `0x005ba7e0`): `+0x00` X,
  `+0x04` Y, `+0x08` Z, `+0x0c` `int16` cull/bound value, `+0x0e` type/flags,
  `+0x10` → object. (`+0x0c` is used for the scene driver's distance cull; on this
  corpus it tracks the mesh's XZ **diameter**, median ratio 0.967 — it is *not* a
  bounding-sphere radius, whose ratio would be ≈0.32.)
- **Object** — for masked types `1, 2, 3, 4, 0x41` the stride is **24 bytes**
  (corpus adjacency, n≈4,429). Masked types `9, 0xa, 0xc, 0x49, 0x4c` use **28 or
  32 bytes** (n≈4,647), so 24 B is *not* universal.

  ```
  +0x00 int32 x      +0x0c int16 rot_x     +0x12 uint8  candidate_depth_bias_scale
  +0x04 int32 y      +0x0e int16 rot_y     +0x13 uint8  candidate_matrix_select (low 5 bits)
  +0x08 int32 z      +0x10 int16 rot_z     +0x14 uint32 geo_ptr
  (the +0x12 / +0x13 names here are CANDIDATE-grade, not established)
  ```

  **`+0x0c/+0x0e/+0x10` are the Euler triple, not padding/flags.** Code:
  `FUN_004498f0` reads `(short)piVar2[3]`, `*(short*)((int)piVar2+0xe)` and
  `(short)piVar2[4]` into `_DAT_005bd808/80a/80c`, and reads
  `*(byte*)((int)piVar2+0x13) & 0x1f` as an index into `&DAT_005c0300`, and
  `*(byte*)((int)piVar2+0x12)` as a scale on `DAT_005b56d0 ± v*8`. **Both `+0x12`
  and `+0x13` names are candidate-grade**: the instructions establish the
  *arithmetic*, not the semantics, and on this corpus `+0x13 & 0x1f` is 0 in all
  214 Level03 objects while `+0x12` takes only {4, 8}. Data: `+0x0c` is
  nonzero in 72 of 214 Level03 type-1/0x41 objects and `+0x10`'s low `int16` in
  76 — so neither is padding. This **agrees with** the already-accepted finding in
  `EXP-20260818-005` that objects carry Euler angles at `obj+0xc/0xe/0x10`; an
  earlier draft of this note wrote `{pad, flags}` and contradicted it. Corrected.
- **`+0x14` → geometry payload** (a `LEVEL.DAT` file offset, relocated at load).
  Confirmed twice: by data (all 2,543 payloads parse) and by code —
  `FUN_004498f0` case 1/0x41 passes `piVar2[5]` (= obj `+0x14`) to
  `thunk_FUN_0045a7f0`.
- For type-9/`0x49` objects `+0x14` is **not** a pointer (Level03: 98 of 266 hold
  `0x10001000`; all values far past EOF), so the field is type-dependent.

## Confirmed — the static mesh grammar (type-`0x41` objects)

```
int32   vertex_count
vertex_count × 12 B:  int16 x, int16 y, int16 z, int16 pad(=0),
                      uint8 c0, uint8 c1, uint8 c2, uint8 flag(=0)
uint16  tag                 (bit 0: 0 = quad faces, 1 = triangle faces)
uint16  face_count
face_count × :
   quad (tag bit0 = 0), 16 B:  uint16 v0,v1,v2,v3   uint16 w0,w1,w2,w3
   tri  (tag bit0 = 1), 12 B:  uint16 v0,v1,v2      uint16 w0,w1,w2
```

**`vN` are vertex BYTE offsets** into the vertex array (`index × 12`).
`pad` and `flag` are `0` in all 115,469 vertices, so neither is exercised.
`c0/c1/c2` are **plausibly RGB** (values are multiples of 4) — *named by
position, not proven*. `w0…` likewise are **presumed UV/attribute words, not
proven**; the break-test below shows only that they are **not** vertex offsets.

> [!success] Validation — 2,543 / 2,543 (100.00%) on the RETAIL corpus
> Every object reached from a type-`0x41` instance across the **21 retail
> `LEVEL*.DAT` files** (`work/copies/BUGS_PC-full-disc/PC/BUGS/CD/`; 17 of the 21
> contain such instances) was decoded and **every** face index checked for
> `offset % 12 == 0` **and** `offset < vertex_count*12`:
> **2,543 reached, 2,543 valid, 0 unparseable, 146,030 face indices, zero errors.**
> The denominator counts every object *reached*, not only those that parsed.

### Break-test — is the 100% discriminating?

Competing grammars scored on the same 2,543 objects (each hypothesis bounded
consistently with its own stride):

| Grammar | Clean |
| --- | ---: |
| **baseline: 12 B vertex, quad 16 B / tri 12 B, byte offsets ÷12** | **100.00 %** |
| triangles also 16 B | 99.10 % |
| vertex stride 8 / 16 / 20 | 35.08 / 2.79 / 11.60 % *(vacuous — see below)* |
| quad face 12 B / 20 B | 9.24 / 9.24 % |
| plain vertex index (`v < count`) | 3.89 % |
| stride-6 offsets / stride-4 offsets / stride-24 offsets | 42.23 / 23.24 / 0.00 % |
| read words 4–7 as the indices | 0.00 % |

**The vertex-stride rows overstate their competitors:** those "clean" objects
check **zero** face indices between them (the mis-strided header lands on
`face_count = 0`), so their true non-vacuous score is **0 %**. The baseline has no
vacuous passes.

So the test genuinely discriminates — unlike the `EXP-005` payload chain, which
this note previously (and correctly) contrasted: there, **11** alternative splits
passed identically. Here every alternative fails, and 146,030 independent `u16`
must each land on a 12-byte boundary inside a per-mesh array.

Code-side corroboration: `FUN_0044de20` — a part drawer reached from the model
renderer `FUN_00448350` — calls **both** emit primitives, `FUN_00405fe0` (quad,
via `0x44e071 call 0x401d66`) and `FUN_00407450` (tri, via
`0x44ec26 call 0x401ccb`), matching the tag's tri/quad bit.

### How the tri/quad bit was found (derived, not assumed)

Parsing everything as quads left exactly **49** failures on retail, whose tags
were **all odd** (97:41, 99:1, 353:5, 355:2). Re-parsing odd tags as 12-byte
triangles took the corpus to 100%. Tag values observed on retail:
**96, 97, 98, 99, 100, 352, 353, 354, 355, 356, 608, 610** — the upper bits are
**undecoded**.

## Where ground lives (Level03, the level with no type-2/3/0xa)

| instance type | n | flatness (Y ÷ max(X,Z) span) | XZ extent | vertices |
| --- | ---: | ---: | ---: | ---: |
| `0x01` | 206 | **1.94** (tall) | 217 | 37 |
| `0x41` (= `1｜0x40`) | **8** | **0.32** (flat) | **6,233** | 254 |

The eight type-`0x41` meshes are large, flat, symmetric slabs — idx167:
X `-4645…4645`, Z `-4931…4931`, Y span 2,439 (flatness 0.247), 474 vertices, 205
quads; idx168 flatness 0.129, 390 vertices. The instance `+0x0c` cull/bound field ≈ the mesh's XZ **diameter** (corpus median ratio **0.967**, n=2,543) — it is *not* a
bounding-sphere radius (that ratio is ≈0.32). Contrast the type-3 billboards:
153 wide × 790 tall, ≈5.2 : 1 the other way.

Corpus-wide, type-`0x41` meshes appear in **17 of 21** retail files (8–449 per
file); per-file median flatness ranges 0.127–1.298, so type `0x41` is the
**general static-mesh type** (ground *and* large props), not a ground-only tag.

## Inferred / not confirmed

- **That these large flat meshes are the visible ground.** Circumstantial but
  strong (only large flat indexed geometry present; in every level; per-vertex
  colour and UVs; the one level with no other mesh type still has 8). **No
  runtime evidence — Gate C would settle it.**
- **The `0x40` bit does not select ground in code.** Verified at instruction
  level: the dispatch is `and edx,0xbfef; lea esi,[edx-1]; mov dl,[esi+0x44b0e4];
  jmp [edx*4+0x44b088]`, and the table entries for type 1 and type 0x41 are the
  **same handler**. The flat/tall correlation is a property of the data.
- **The code↔data link is only partial.** Type-1/`0x41` routes to `FUN_0045a7f0`
  (≈150 KB) → `FUN_00448230`; `FUN_00448350` dispatches to part drawers that call
  the emit primitives. The routine that actually consumes the 12-byte vertices
  and byte-offset faces is **not yet traced**; the grammar rests on data
  validation plus the tri/quad corroboration.
- **Scope:** the grammar is claimed for **type-`0x41`** objects. Applied to
  masked-type-`0x01` objects it gives **1,458 / 1,613 (90.39 %)** — 155 failures,
  counted with the same non-filtering denominator as the headline. **154 are in
  `LEVEL01/LEVEL2.DAT`** (tags 97:29, 99:26, 100:77, 102:22), an unexplained
  variant rather than random noise. The **155th** is `LEVEL00/LEVEL.DAT` instance
  38 → object `0x1a30` → geometry `0xba30`, which is not a mesh but an apparent
  **null/empty-geometry sentinel**: `int32 vertex_count = 0` followed by
  `0xffff 0xffff`, with the real mesh beginning 8 bytes later at `0xba38`
  (`vertex_count = 34`). Neither is investigated further here; both are retail, so
  the format is **not** universal across type-`0x01`.

## Side finding — a non-relocated mod artifact (`KU-082`)

Running the same validation over `work/copies/M3-training-51-grains/CD/` gives
**2,442 / 2,543 (96.03 %)**, with all 101 failures in that copy's
`LEVEL07/LEVEL1.DAT` (sha `8ab9acd4…`, 115,076 B vs retail `494d2818…`,
115,060 B). Its tail is byte-identical to retail shifted by `0x10`
(`mod[0x3f8:] == retail[0x3e8:]`), so the 16-byte insertion was made **without
relocating the object pointers** — the `+0x14` fields are stale. Filed as
`KU-082`; an earlier draft of this note silently excluded these from the
denominator and reported "2,442/2,442 (100 %)", which was wrong.

## Next

1. **Gate C** on this format (not type-3): predict a vertex from bytes, then one
   authorized guarded poke under `play-pristine` with the user watching which
   surface moves.
2. Trace the consuming drawer to close the code↔data link.
3. Decode the tag's upper bits; test the UV interpretation; investigate the
   `LEVEL01/LEVEL2.DAT` type-`0x01` variant.

## Links

- [[EXP-20260818-005 - Decode the render-geometry command grammar (scope)]]
  (Gate A/B; why type-3 was the wrong target), `KU-079`, `KU-082`,
  [[New-level authoring roadmap (terrain, collision, materials)]],
  [[New-level authoring feasibility (PC)]], [[PC LEVEL DAT prefix]].
