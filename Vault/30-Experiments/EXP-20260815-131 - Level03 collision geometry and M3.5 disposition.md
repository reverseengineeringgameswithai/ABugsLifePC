---
type: experiment
id: EXP-20260815-131
date: 2026-08-15
question: What PC asset geometry belongs to Level03 result-1 descriptors, and does it identify a distinct natural row-6 target?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline exact retail-derived PC work copy
configuration: static executable trace; lossless bounds-checked TERRAIN.ALL parser; no live game process
artifacts:
  - reimplementation/ablpc/terrain_all.py
  - tests/test_terrain_all.py
addresses:
  - "0x004A8410"
  - "0x004A8950"
  - "0x004ACF90"
  - "0x007F4590"
  - "0x007F45BE"
file_offsets:
  - "LEVEL03/TERRAIN.ALL:0x3688C"
  - "LEVEL03/TERRAIN.ALL:0x411C8-0x41473"
  - "LEVEL03/TERRAIN.ALL:0x324F8-0x32B4B"
result: scanner-layout-corrected-nine-result1-regions-m3.5-row6-natural-arm-disposed
created: 2026-08-15
updated: 2026-08-15
tags: [re/experiment, re/static, re/file-format, milestone/m3]
---

# EXP-20260815-131 - Level03 collision geometry and M3.5 disposition

## Question

Can the exact PC `TERRAIN.ALL` bytes and executable loader assign real X/Z
bounds to Level03 collision result-1 descriptors 570–578? Does that map reveal
a different naturally reachable result-1 surface inside row 6's nearest
region, justifying another live Tunnels arm?

## Inputs and safety

- Exact `bugs.exe` SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact Level03 `TERRAIN.ALL` SHA-256:
  `b878c378c924fbdb45e450f4314808fdd3506f8685da2c3f255b7e316f4a2d9c`.
- Exact Level03 `LEVEL.DAT` SHA-256:
  `bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b`.
- All game assets were read from `work/copies/BUGS_PC-full-disc`; `originals/`
  was not accessed or modified.
- No Wine/game process, target-memory write, debugger, input, life, grain, or
  renderer instance was used.

## Scanner correction

The EXP-118 helper began each purported 48-byte row at `0x007F45A0`. Static
PC code proves the actual descriptor base is `0x007F4590`, stride `0x30`.
Therefore the helper's source pointer, tag, and result columns were correct,
but its `row+0x20/+0x24/+0x28` tuple was descriptor `index+1` base X/Y/Z.

The most consequential correction is:

- the tuple `(471712,64224,537728)` printed on scanner row 571 is descriptor
  **572's** base, not descriptor 571's retained position;
- descriptor 572 is the natural first-grain-gate pit descriptor captured in
  EXP-129;
- descriptor 571's correct base is `(470112,64224,-423840)`.

This is an explicit supersession, not a silent reinterpretation of the old
runtime artifact.

The runtime source-pointer series independently joins the file payloads. For
descriptors 570, 571, 572, and 578, each live pointer minus its parsed payload
offset equals the same loaded-file base `0x0068DA33`. Descriptor 572, for
example, uses live pointer `0x006C0093` and file payload `0x32660`.

## Static PC layout

[[FUNC-97C95BA5572D-004A8410]] reads the file's word-scaled directory offset,
walks `0x4C`-byte source records, builds `0x30`-byte runtime descriptors, shifts
base coordinates left five, stores the payload pointer at descriptor `+0x10`,
and copies source result word `+0x28` to descriptor `+0x2E`.

[[FUNC-97C95BA5572D-004A8950]] then consumes tag values 6/7/8. It walks
12-byte group headers plus `count*0x20` cells and computes descriptor X/Z
minimum/span fields from group words `+0x04/+0x06/+0x08/+0x0A`, shifted left
five and added to the descriptor base. `0x004ACF90` later returns descriptor
`+0x2E` for the current collision index.

## Level03 result-1 map

The source directory begins at `0x3688C`, contains 592 records, and ends at
EOF. Records 570–578 each have field/tag 6, result 1, and a 180-byte collision
payload:

| Desc. | Source record | Payload | X bounds | Z bounds | Two nearest type-1 rows at center |
| ---: | ---: | ---: | --- | --- | --- |
| 570 | `0x411C8` | `0x324F8` | `176384..236416` | `98112..161088` | 1, 0 |
| 571 | `0x41214` | `0x325AC` | `470112..528288` | `-452928..-423840` | 2, 3 |
| 572 | `0x41260` | `0x32660` | `471712..529888` | `508672..537728` | 7, 6 |
| 573 | `0x412AC` | `0x32714` | `1111712..1169888` | `1307072..1336128` | 11, 10 |
| 574 | `0x412F8` | `0x327C8` | `1174272..1203360` | `1961280..2019456` | 15, 14 |
| 575 | `0x41344` | `0x3287C` | `1615456..1674144` | `2494560..2558240` | 17, 16 |
| 576 | `0x41390` | `0x32930` | `816864..875936` | `259424..322976` | 4, 5 |
| 577 | `0x413DC` | `0x329E4` | `1454496..1515104` | `1378304..1440896` | 12, 13 |
| 578 | `0x41428` | `0x32A98` | `811648..880288` | `571936..644032` | 9, 8 |

The nine result-1 surfaces form an exact spatial pairing with all 18 authored
type-1 coordinate rows. This does not prove a user-facing checkpoint name.

Descriptor 572 is the only result-1 descriptor near rows 6/7. Its rectangle
crosses their nearest-row boundary: the boundary Z rises from approximately
`518321` at X `471712` to `523181` at X `529888`; lower Z selects row 6 and
higher Z selects row 7. EXP-129's natural contacts `(494438,526143)` and
`(505717,526449)` are both above that boundary and correctly select row 7.
The descriptor's lower-Z area is geometrically inside row 6's nearest region,
but controller access to it remains unproved. Two natural approaches already
funneled into the same pit's row-7 side.

## Tool validation

The new read-only parser:

- retains the complete file, raw `0x4C` records, payloads, cells, trailers,
  unknown fields, and suffix;
- bounds-checks every read and rejects impossible offsets/counts, payload
  chain mismatches, group overruns, negative cell counts, missing terminators,
  and negative spans when bounds are requested;
- passes 9 focused tests using two synthetic group layouts and three available
  retail-derived files;
- parsed all 18 available `TERRAIN.ALL`/`TERR1.ALL` files in the work-copy
  corpus at the source-record level.

The final repository gate passes 576 tests. Vault lint reports 380 notes with
zero errors and zero warnings; the M4 compatibility statement and tracked-
file audit also pass unchanged.

The bounded group grammar parsed the tested Level03 result-1 records and the
non-clone tag-6/7/8 payloads in Levels 01–10. Eight Level00 tag-6 records reject
that group grammar and ten further Level00 groups contain negative spans. Those
contradictions remain explicit; no general Level00 collision-payload claim is
made.

## Result and M3.5 disposition

No distinct row-6-near result-1 descriptor exists. Descriptor 572 is the sole
rows-6/7 region, and repeating or teleporting into that same grain-gate pit
would not satisfy the requested independent natural target.

M3.5 therefore adopts the roadmap's explicit alternative disposition:

- retain EXP-117's accepted causal row-6 source/candidate result;
- retain EXP-129's twice-observed natural descriptor-572/result-1 upstream
  chain and natural row-7 selection;
- do **not** claim natural row-6 selection, controller reachability of
  descriptor 572's lower-Z portion, checkpoint semantics, or generalization;
- remove natural row-6 selection as an M3.5 completion blocker because the
  consumer causality and natural upstream producer are already independently
  established, and static geometry supplies no distinct safe route target.

This is a milestone-scope disposition, not proof that a natural row-6 contact
is impossible. M3 remains active pending its final exit-gate reconciliation.

## Evidence

- [[PC TERRAIN ALL collision descriptor source]]
- [[PC TERRAIN ALL inspector]]
- [[EXP-20260815-117 - Approved Level03 row-6 reset rerun]]
- [[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]]
- [[EXP-20260815-130 - Write-assisted Level03 teleport safety boundary]]
