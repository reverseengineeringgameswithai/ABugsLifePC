---
type: file-format
id: FMT-PC-LEVEL-DAT-PREFIX
status: inferred
confidence: medium
evidence:
  - EXP-20260812-006
  - EXP-20260812-008
  - EXP-20260812-009
  - EXP-20260812-010
  - EXP-20260812-011
  - EXP-20260812-012
  - EXP-20260812-013
  - EXP-20260812-016
  - EXP-20260814-111
  - EXP-20260815-116
  - EXP-20260815-131
  - EXP-20260818-006
  - EXP-20260818-007
  - FUNC-97C95BA5572D-0044BB70
  - FUNC-97C95BA5572D-00417720
  - FUNC-97C95BA5572D-00456A90
  - FUNC-97C95BA5572D-00432930
created: 2026-08-12
updated: 2026-10-02
tags:
  - re/file-format
---

# PC LEVEL DAT prefix

## Known magic/signature

No magic is confirmed. The first little-endian signed dword is a top-record count.

## Extensions and observed files

Twenty-one `LEVEL*.DAT` files across `CD/LEVEL00` through `CD/LEVEL10` were parsed in `EXP-20260812-006`. This dossier does not apply to every `.DAT` file; `RAND.DAT` is a counterexample.

## Endianness

Little-endian, confirmed by the x86 loader walk at executable address `0x0044BB70` and matching corpus boundaries.

## Confirmed prefix layout

1. Signed dword top-record count.
2. Variable top records, each beginning with signed 16-bit count and type.
3. Signed dword count followed by count × 128 bytes.
4. Primary 20-byte records, terminated when the signed word at record offset `+0x0E` is negative; the sentinel occupies 20 bytes.
5. Signed dword index maximum followed by maximum + 1 dwords when maximum is nonnegative.
6. Secondary 20-byte records with the same sentinel rule.
7. Unknown suffix retained verbatim.

*Update (2026-10-02 audit):* [[EXP-20260905-006 - World-scale terrain tiling and checked mesh growth]]
later found that `0x0044BB70` reads the file's final signed dword at
`0x0044BECA`, subtracts it from base + file size at `0x0044BF0C`, stores the
result in `0x005B7100` at `0x0044BF18`, and copies 256 bytes from result+0x18.
The final dword is therefore an end-relative span, and appending data must
move it. A value of `-1` takes a separate branch at `0x0044BECD` that skips
the copy (fresh retail disassembly in this audit; `terrain_texture_tiling.append_mesh`
also treats `-1` as absent). The trailing data it locates stays unnamed.

At `0x0044BB70`, top-record size is `4 + count*16` for type `0x3F`, `4 + count*12` for other nonnegative types, and `16 + align4(count*6)` for negative types.

## Level03 type-1 coordinate rows

For `CD/LEVEL03/LEVEL.DAT` SHA-256
`bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b`,
top-record index 1 begins at `0x458`, has type 1 and count 18, and occupies
220 bytes. Its entries begin at `0x45C` and are 12-byte signed XYZ triples.
Row 6 begins at `0x4A4` with `(15678,0,15438)`.

`0x0044BB70` stores type 1 in pointer slot `0x005C5864`.
[[FUNC-97C95BA5572D-00432930]] conditionally scans its rows by X/Z distance,
then writes selected X/Z shifted left by five and terrain-recomputes Y.
Other functions at `0x004317D0`, `0x004323A8`, `0x004369B0`, and
`0x0043CE60` also consume type 1. The table is therefore a bounded coordinate
row structure, not a confirmed checkpoint or bespoke respawn format.

`EXP-20260815-116` defines one exact row-6 X+128 runtime discriminator. It
does not promote a general type-1 editing grammar.

[[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]] maps
nine exact Level03 `TERRAIN.ALL` result-1 regions whose centers' two nearest
rows cover the 18 type-1 entries as pairs. Descriptor 572 is the sole rows-6/7
region. This is a PC-native spatial relationship, not proof that the rows are
user-facing checkpoints or that every row has the same behavior.

[[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]] adds a
natural PC consumer observation for row 7. Row 7 begins at `0x4B0` with raw
XYZ `(15539,0,17102)`, giving scaled X/Z `(497248,547264)`. Two ordinary
falls into the first grain-gate pit each produced a first sampled post-reset
position `(497247,31299,547255)`, retaining the `(-1,-9)` X/Z residual because
the 50 ms sampler missed the exact write instant. This confirms a bounded
nearest-row reset use; it does not rename the whole type-1 table as
checkpoints or prove the same role for every consumer.

`EXP-20260812-016` confirms one use of the type-`0x3F` special case without
naming the complete record. `0x0044BB70` stores its loaded address in pointer
slot 63 at `0x005C595C`. `0x00416100` reads the record count and one selector
byte at record-relative `0x10 + index*0x10` to derive selected plant resource
IDs from executable tables.

## Twenty-byte record

| Offset | Width | Current name | Status |
|---:|---:|---|---|
| `+0x00` | 4 | candidate-center component 0 | inferred |
| `+0x04` | 4 | candidate-center component 1 | inferred |
| `+0x08` | 4 | candidate-center component 2 | inferred |
| `+0x0C` | 2 | signed visibility-bound candidate | inferred |
| `+0x0E` | 2 | flags/sentinel discriminator | inferred |
| `+0x10` | 4 | payload offset candidate | inferred |

`0x0044D430` uses the first three dwords as a candidate center and signed
`+0x0C` in distance/screen-bound tests. For dispatch `0x49`, `0x004498F0`
switches from the selected record to relocated `+0x10` before reading the
render-placement tuple. `0x0044BB70` adds the file base to `+0x10` for
non-sentinel records. Exact center axis names, units, and negative `+0x0C`
semantics remain unconfirmed.

For records with flag bit `0x08` set, `0x0044BB70` then relocates payload
`+0x1C`; otherwise it relocates payload `+0x14`. If flag bit `0x20` is set, an
additional payload dword at `+0x20` or `+0x18`, respectively, is relocated.
Exact instructions are recorded in `EXP-20260812-009` at `0x0044BD03` through
`0x0044BD73`.

At runtime, global `0x005BA240` stores the allocated-buffer pointer; live record and relocated payload addresses are computed as that pointer plus their file offsets. `RUN-GDB-20260812-021920` independently matched primary start `base+0x04B0` and the parsed offsets below.

## Training offsets

For SHA-256 `494d2818…d5a22`: primary records start `0x04B0`, sentinel `0x1928`, index table `0x193C`, secondary records `0x1940`, secondary sentinel `0x1A80`, and unknown suffix `0x1A94` through EOF.

The type-`0x3F` top record occupies `[0x0004, 0x03E8)` with count 62.
Its entries have a 16-byte stride: three signed dwords at `+0x00/+0x04/+0x08`,
a selector byte at `+0x0C`, an active-state byte observed at `+0x0D`, and a
runtime-initialized word at `+0x0E`. In the exact Training source, entries
0–49 have selector `0x14`, so the PC-native source census is 50.

`EXP-20260814-111` confirms the selector's bounded gameplay role through two
independent PC forms. `0x00456A90` has a distinct selector-`0x14` terrain-
height initialization branch; `0x00417720` writes consumed-y sentinel
`0x80000000` and increments counter `0x0059D9B1`. Runtime isolation makes the
new selector-`0x14` record the only one of three adjacent entries consumed
while that counter moves `0 -> 1`. Selector `0x14` is therefore confirmed as
the PC grain collectible at this exact Training boundary.

The accepted 51-record recipe inserts new entry 62 at original offset `0x3E8`
with `(x,y,z) = (4950,-1301,1127)`, raises count 62 to 63, and shifts every
subsequent physical byte by `0x10`. It relocates 556 known file-relative
pointer fields by the same amount. The new output is 115,076 bytes at SHA-256
`20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40`;
it reparses to 262 primary and 16 secondary records and inverses to the source
byte-for-byte. These exact constraints do not define a general insertion
grammar.

`EXP-20260814-113` starts from that exact 51-grain DAT and bounds the four
singleton letter-mask records:

| Index | File offset | Selector | Authored position |
|---:|---:|---:|---|
| 50 | `0x328` | `0x10` | `(-2733,-50,5061)` |
| 51 | `0x338` | `0x11` | `(4821,-50,2773)` |
| 52 | `0x348` | `0x12` | `(3205,-50,-4510)` |
| 53 | `0x358` | `0x13` | `(-5366,-50,-3184)` |

The exact transformation can move, duplicate, or remove those unique records
while retaining all unknown tail bytes. The accepted demo appends one moved
copy of each selector, raises table count 63 to 67, moves the remainder by
`0x40`, relocates 556 known fields, and inverses exactly. Its output is
115,140 bytes at SHA-256
`e9c75bb24ae0d0f4f74d17ea63431195e49b7e5278c089588d9372b8eb8cae7a`.
All four copies initialize and collect under the unchanged PC executable.
Selector-to-individual-glyph identity remains unconfirmed, and the supported
operation remains hash/layout-locked rather than a general type-`0x3F`
grammar.

Selector bytes at file offsets `0x0394`, `0x03A4`, and `0x03B4` are `+`, `+`,
and `,`; the exact `0x00416100` tables map them to plant IDs 4, 10, and 6.
They are part of the same DAT and fixup path but precede, and do not overlap,
the M1 primary 20-byte records or positive-target blocks
(`EXP-20260812-016`).

The mapped result depends on occurrence order within each selector class.
Exact instructions `0x004161EA–0x004161FA` advance the `0x2B` table cursor
only when a `0x2B` is encountered. `EXP-20260812-020` changes only the second
Training `0x2B` at `0x03A4` to `0x00`: the plant 10 pair requests disappear,
plant 04 remains, and the run reaches Direct3D `NextLife`. Removing the first
`0x2B` at `0x0394` would instead shift the second occurrence to ID 4, so these
bytes are not independently editable selector-to-ID fields.

The three records investigated in `EXP-20260812-008` are:

| Record | File offset | Candidate center | Visibility-bound candidate | Flags | Payload offset | Observed final payload target |
|---:|---:|---|---:|---:|---:|---:|
| 124 | `0x0E60` | `(-166, -833, -393)` | `0x05EA` | `0x0059` | `0x26DC` | `0x1319C` |
| 125 | `0x0E74` | `(845, -270, -968)` | `0x04EB` | `0x0059` | `0x26FC` | `0x111E4` |
| 126 | `0x0E88` | `(872, -757, 70)` | `0x05D2` | `0x0059` | `0x271C` | `0x111E4` |

`EXP-20260812-006` jointly moved all three first dwords and described the software-renderer result as removal of a central foreground flower cluster. The discriminating hardware-renderer runs in `EXP-20260812-008` move one record at a time: each removes a different visible plant element within a disjoint exact difference box. They are therefore not three alternative LOD representations of one on-screen object in the tested Training start state.

`EXP-20260812-011` corrects the earlier move/position interpretation for the
bounded dispatch: modest record-126 `+0x04` and `+0x08` changes do not move
render content, while static flow switches to the payload before placement
math. The first three record dwords are candidate-center inputs; the earlier
`+0x00 = 50000` edits crossed selection thresholds and removed content.
`EXP-20260812-012` then reduces record 125 positive bound `+0x0C` from `1259`
to zero and excludes only its partially visible right-edge content. The local
corpus contains 508 negative signed `+0x0C` values whose convention remains
unknown.

`EXP-20260812-009` establishes that flags `0x0059` select masked dispatch `0x49`,
which passes payload `+0x1C` to `0x0045A7F0`. Both targets satisfy the positive
layout in [[STRUCT-PC-LEVEL-DAT-POSITIVE-PAYLOAD-TARGET]]. Target `0x111E4`
has 11 Training primary references and `0x1319C` has 17. Reusable render
content is confirmed for the tested reciprocal edits in `EXP-20260812-010`:
record 124 and record 125 change only their independently identified visible
placement regions when rebound between those targets. Complete object-
definition semantics remain unknown.

## Level 01 cross-file runtime

`EXP-20260812-013` binds the `ant hill` menu selection to
`CD/LEVEL01/LEVEL.DAT`, SHA-256
`786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
The file contains nine valid positive masked dispatch-`0x49` references to
four unique targets.

Primary record 261 begins at `0x2968`, has candidate center
`(4685, -4948, -762)`, positive signed `+0x0C` value `954`, flags `0x0049`,
and payload offset `0x4E00`. Its payload target field is at `0x4E1C` and
points to `0x3703C`, whose positive count is `32`. A guarded rebind to valid
same-file target `0x3459C`, positive count `131`, changes only bytes
`0x4E1C–0x4E1D` and is accepted by the unchanged executable under Direct3D.
A center control changes only `0x2968–0x2969` and is also accepted.

Both candidates retain exact unchanged frames at the tested Level 01 starting
camera. This confirms second-file edit acceptance and byte locality, but does
not identify record 261's visible placement or demonstrate that it is selected
at that camera.

## Parser status and coverage

The suffix now has a separately bounded static-mesh dossier:
[[PC LEVEL DAT static mesh]]. It covers primary-record dispatch type `0x41`,
the object-to-payload chain, the 12-byte vertex array, primitive groups,
byte-offset face references, the exact consuming PC instructions, and the
reconstructive implementation. This does **not** promote those meshes to
confirmed visible ground; Gate C remains authorization-gated.
*Superseded 2026-09-04:* [[EXP-20260904-005 - Raised floor and visible ground pairing]]
confirms one bounded visible-ground example (Level01 primary meshes 160/213/280
with restored-file controls); general mesh identity remains open.

`reimplementation/ablpc/level_dat.py` bounds-checks every read, preserves the full byte string, rejects impossible counts, and edits only explicitly selected fields. It now inspects positive-count payload targets, validates command references, supports guarded target rebinding only for masked dispatch `0x49`, and exposes an expected-value-guarded offset-named `+0x0C` operation. `inspect --payload-targets` filters to that supported masked class so unrelated dispatch/negative layouts cannot be mistaken for supported inspection. Tests include two synthetic prefix layouts, a synthetic positive target, unsupported/invalid target rejection, exact center/field/pointer-edit locality, strict manifest validation, sparse overlays, and staged copies. Prefix corpus scan: 21 files, zero failures. Same-dispatch target scan: 990 records in 14 files, zero failures (`EXP-20260812-009`, revalidated in M1.5). The original executable accepts the exact-hash Training rebinds, center candidates, and positive-bound edit under Direct3D (`EXP-20260812-010` through `EXP-20260812-012`), plus byte-local center and guarded-target edits against the exact Level 01 DAT (`EXP-20260812-013`). The promoted boundary is [[M1 Tool Support Matrix]].
