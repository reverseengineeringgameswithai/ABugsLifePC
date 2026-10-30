---
type: file-format
id: FMT-PC-TERRAIN-ALL-COLLISION-SOURCE
status: inferred
confidence: high
evidence:
  - EXP-20260815-131
  - FUNC-97C95BA5572D-004A8410
  - FUNC-97C95BA5572D-004A8950
created: 2026-08-15
updated: 2026-09-05
tags: [re/file-format, milestone/m3]
---

# PC TERRAIN ALL collision descriptor source

## Subsequent EXP-003 result (2026-09-05)

[[EXP-20260905-003 - Shared floor return discriminator and stitched patch]]
reproduces the rigid EXP-005 return fall numerically and with normal live input.
The original-instruction witness distinguishes a vertical discontinuity and
entry from beneath a one-sided plane from an XZ gap or Y-window-only cause. A
connected six-cell star with paired render heights passes finite modeled and
live return paths. This is a successor experiment, not a change to this original
fixture or a universal authoring rule; its prop-confounded and blocked routes
remain explicitly open. Earlier unresolved wording below describes this note's
historical checkpoint, not the new experiment's result.


## Raised floor and visible companion — 2026-09-04

[[EXP-20260904-005 - Raised floor and visible ground pairing]] subtracts64 stored units from
six h0 fields at cell+8 in source99/group47640. Original landing/walking and live
spawn height rise2,048 world units; normal jumps land on the patch. Relative Y
bounds, normals, edge vectors and all other bytes remain unchanged. A fixed
LEVEL.DAT companion also changes visible ground under restored-file controls.
See [[PC floor translation prototype]]; boundary stitching and general surface
writing remain open.

## First live barrier edit — 2026-09-04

[[EXP-20260904-004 - Translated barrier live collision proof]] relocates one
four-segment kind-0x101 strip into the natural spawn path. Exact loaded-data
reads and changed/restored-file walking traces confirm response at the new
location. [[PC barrier translation prototype]] preserves file size and all
unrelated bytes. General mesh writing and universal contact behavior
remain open; the earlier loader/grammar results below are unchanged.

## Barrier grammar and grounded movement — 2026-09-04

[[PC TERRAIN ALL barrier strips]] now documents the kind`0x101` connected
X/Z-point layout, interleaved16-segment block bounds, sentinel tails and
16-pair collection cap. The lossless reader is `terrain_barriers.py`.
[[EXP-20260904-003 - Barrier grammar and landing-seeded grounded movement]]
matches original collection and tests both real obstacle families after the
original coordinator establishes grounded contact by landing. Directory,
triangle, height and EXP-002 loader implementations are reused unchanged.
EXP-003 alone supplied no writer; EXP-004 above adds a scoped translation
prototype without claiming a universal gameplay contract.

## Real-data movement and templates — 2026-09-04

[[EXP-20260904-002 - Retail collision admission and separate XZ barriers]]
runs the original loader, bounds/bucket slice and movement coordinator with
real Level01/Level03 plus PLANTTER. Level01 source87/cell1000 is admitted and
causes lateral deflection at a synthetic nongrounded position. A separate
kind`0x101` linked list supplies X/Z barriers; source179's first pair causes
response at three different Y values. Their 12-byte entries contain middle
dwords used as bounds/sentinels; do not label those dwords world Y. At EXP-002
the block grammar was still open; EXP-003 above now supplies its bounded reader.
No general segment writer is admitted; EXP-004's scoped prototype is documented above.

Movement also narrows cell fields left unknown by the height-only analysis:
`+0x0e/+0x14` are Y edge arguments (`004aa650..004aa666`), and
`+0x1c/+0x1d` are signed bytes contributing a local Y admission minimum
`h0 + byte[1c]*64` and span `byte[1d]*64`, before movement padding
(`004ab527..004ab547`). These are consumer-derived roles.

All13 mapped object templates come from PLANTTER, occupying descriptors178..190
for Level01 and589..601 for Level03. Original initialization clears their tags;
N is191 /602, followed by32 reserved slots. Thus EXP-001's direct twenty-slot
render stores are disjoint from static terrain and templates for these exact
loads. Other variants and whole-render-subtree payload effects remain unknown.
The original descriptor bases, payload identities and bounds agree with the
independent height model across both tested terrain files.

## Earlier synthetic movement extension — 2026-09-04

The height-query model below is not the full movement solver.
[[EXP-20260904-001 - Original PC lateral collision and descriptor-store probes]]
identifies `004ab1a0 -> 004aa4d0` as a player-connected XYZ plane-crossing
branch. `004a9860` consumes all triangle edge coordinates, including cell
`+0x0e/+0x14` as Y edge components in its argument list, and projects by
dominant normal axis. Synthetic vertical triangles change X/Z response in
original instructions. At EXP-001, real-level candidate reachability and
authoring remained open; EXP-002 above now demonstrates selected real candidates.
Neither experiment widens `terrain_height.py`'s conformance claim.

The same experiment bounds `0044ca00`'s direct descriptor stores to N..N+19.
It does not prove whole-render-subtree independence or that all template
indices lie below N. See KU-080/KU-081 before designing a writer.

## Boundary

This dossier covers the bounded source-descriptor walk used by the exact PC
executable for `TERRAIN.ALL` and `TERR1.ALL`. It is separate from the plant
resource `.ALL` files whose first consumer begins at `0x00448010`.

The exact Level03 `TERRAIN.ALL` used here is 268,368 bytes at SHA-256
`b878c378c924fbdb45e450f4314808fdd3506f8685da2c3f255b7e316f4a2d9c`.

## Confirmed source walk

All integers are little-endian.

1. The unsigned dword at file `+0x00`, multiplied by two, gives the source-
   record directory offset.
2. Bytes from `+0x04` to that directory are consecutive payloads. Each
   record's `+0x00` dword gives its payload size in 16-bit words.
3. The directory begins with an unsigned record count followed by `0x4C`-byte
   records.
4. Unknown record fields, payload bytes, and any suffix remain preserved.

[[FUNC-97C95BA5572D-004A8410]] performs this walk. For a non-clone record it
constructs a `0x30`-byte runtime descriptor at `0x007F4590 + index*0x30`:

| Source offset | Width | Bounded role | Static evidence |
| ---: | ---: | --- | --- |
| `+0x00` | 4 | payload size in 16-bit words | cursor advance after `0x004A8631` |
| `+0x04/+0x08/+0x0C` | 4 each | base components, shifted left five in runtime descriptor `+0x00/+0x04/+0x08` | `0x004A85AD–0x004A85DC` |
| `+0x10` | 4 | low word copied to runtime descriptor `+0x2C` | `0x004A8595–0x004A859B` |
| `+0x28` | 2 | result word copied to runtime descriptor `+0x2E` | `0x004A859F–0x004A85A3` |
| `+0x44` | 2 | reference field used by the clone branch | `0x004A850A–0x004A852F` |
| `+0x46` | 2 | value 1 selects the clone branch | `0x004A84FF–0x004A8508` |

These names describe byte flow only. `field_10`, the complete clone semantics,
and the many untouched words are not identified game concepts.

## Bounded collision payload grammar

For the Level03 material/result-1 records, and for the tested non-clone
tag-6/7/8 records in Levels 01 through 10, a payload contains groups followed
by a negative signed marker:

| Group offset | Width | Bounded role |
| ---: | ---: | --- |
| `+0x00` | 2 | nonnegative group marker, or negative terminator |
| `+0x02` | 2 | cell count |
| `+0x04` | 2 | local minimum X in 32-unit cells |
| `+0x06` | 2 | local X span |
| `+0x08` | 2 | local minimum Z in 32-unit cells |
| `+0x0A` | 2 | local Z span |
| `+0x0C` | `count*0x20` | cells with mostly unknown fields |

[[FUNC-97C95BA5572D-004A8950]] populates the runtime minimum/span fields.
**Correction (EXP-20260816-141):** the actual bounds pass at `0x004A8A1A`
derives them from *cell* fields (`+0x18/+0x1A` in X;
`(byte +0x1E << 6) + word +0x0A` and
`(byte +0x1F << 12) + (byte +0x1E << 6) + word +0x0A` in Z), shifted left
five and rebased — not from the group-header words. For Level03
descriptors 570-578 the X bounds coincide with the group-header table
below; the Z bounds do not (see
[[Known Unknowns#KU-061 - Runtime descriptor Z-bounds derivation]]). The
Z-bounds columns below therefore describe the group headers, not proven
runtime descriptor words. Eight Level00 records do not satisfy this
bounded group walk and are retained as a format variant/contradiction
rather than normalized into it.

## Height-query cell grammar (EXP-20260816-141)

The height pipeline (`0x004AC460` collector, `0x004ACA60` resolver,
`0x004A9290` edge test) gives several cell fields bounded roles: words
`+0x00/+0x02/+0x04` are the plane numerator slopes and signed divisor
(the divisor's sign selects triangle winding), `+0x06/+0x0A` a vertex
origin, `+0x08` the plane base height, `+0x0C/+0x10` and `+0x12/+0x16`
the two edge deltas, `+0x18/+0x1A` the X window, and bytes `+0x1E/+0x1F`
the Z window. A contained cell's plane height is
`base_y + 4*((h0 << 3) - idiv(((z-z0)*A + (x-x0)*B) << 3, C))`. PC world
Y grows downward; clones (source `+0x46 == 1`, the majority of records)
copy their template's descriptor and substitute their own shifted base.
Words `+0x0E/+0x14/+0x1C` are outside the height-query model;
their movement consumers are now narrowed by EXP-20260904-002 above.

## Level03 material/result-1 map

Level03 has 592 source records at directory `0x3688C`. Records 570 through
578 have runtime/source field `6`, result word `1`, non-clone payloads of 180
bytes, and the following PC-native X/Z bounds:

| Descriptor | Record offset | Payload offset | Base X/Z | X bounds | Z bounds |
| ---: | ---: | ---: | --- | --- | --- |
| 570 | `0x411C8` | `0x324F8` | `(176352,117088)` | `176384..236416` | `98112..161088` |
| 571 | `0x41214` | `0x325AC` | `(470112,-423840)` | `470112..528288` | `-452928..-423840` |
| 572 | `0x41260` | `0x32660` | `(471712,537728)` | `471712..529888` | `508672..537728` |
| 573 | `0x412AC` | `0x32714` | `(1111712,1336128)` | `1111712..1169888` | `1307072..1336128` |
| 574 | `0x412F8` | `0x327C8` | `(1174240,1961280)` | `1174272..1203360` | `1961280..2019456` |
| 575 | `0x41344` | `0x3287C` | `(1615424,2512384)` | `1615456..1674144` | `2494560..2558240` |
| 576 | `0x41390` | `0x32930` | `(816864,277568)` | `816864..875936` | `259424..322976` |
| 577 | `0x413DC` | `0x329E4` | `(1454496,1397760)` | `1454496..1515104` | `1378304..1440896` |
| 578 | `0x41428` | `0x32A98` | `(811616,593280)` | `811648..880288` | `571936..644032` |

Their centers' two nearest authored Level03 type-1 rows are respectively
`(1,0)`, `(2,3)`, `(7,6)`, `(11,10)`, `(15,14)`, `(17,16)`, `(4,5)`,
`(12,13)`, and `(9,8)`. This exact nine-descriptor/eighteen-row pairing is a
PC data relationship, not proof that the rows are user-facing checkpoints.

## Tooling

`reimplementation/ablpc/terrain_all.py` provides a read-only, bounds-checked,
lossless parser and inspector. It rejects impossible offsets/counts, payload
overruns, malformed cell groups, missing terminators, and unsupported bounds.
Its tests use two synthetic layouts plus three ignored retail-derived files;
the EXP-131 corpus arm parsed 18 available `TERRAIN.ALL`/`TERR1.ALL` files.

`reimplementation/ablpc/terrain_height.py` adds the engine-faithful
height query on top of the parser, validated at four accepted runtime
receipt points in
[[EXP-20260816-141 - Engine-faithful terrain height and gate standoffs]].

See [[PC TERRAIN ALL inspector]] and
[[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]].

## Fixed constructed deck — 2026-09-04

[[EXP-20260904-006 - Flat deck and solid block test]] replaces a bounded source99 prefix with12
one-cell groups and a negative terminator: flat deck, block top and four sides.
Axis normals, directed edges and conservative admission bounds survive original
loading/movement and live tests. This is a fixed synthetic authoring fixture;
the old EXP-005 return failure and general seam/normal rebuilding remain open.
