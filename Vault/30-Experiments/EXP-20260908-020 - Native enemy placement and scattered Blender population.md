---
type: experiment
id: EXP-20260908-020
date: 2026-09-08
question: How are Anthill enemy placements stored in the PC LEVEL.RAW actor table, and can that table be edited to add, move and remove native enemies?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Linux, isolated Wine and Gamescope hardware Direct3D, Unicorn, Blender 5.2
result: Packet 31 decodes through 0049A200 to a type-35 dword plus 64 rows of 28 bytes copied to 00599EB0 (XYZ at +0/+4/+8 scaled x32, type +12, script +13); 0041C420 builds 132-byte actors at 0059B628; the five enemy types map to model families through 00445020; 53 source slots are free once original enemy rows are disabled; edited tables load live with exact source XYZ and script IDs.
status: accepted-bounded
created: 2026-09-08
updated: 2026-10-29
evidence: [EXP-20260908-020]
tags: [experiment/pc, re/actors]
---

# EXP-20260908-020 - Native enemy placement and scattered Blender population

## Provenance

Private artifacts/scripts are under `work/experiments/EXP-20260908-020/` (H).
Asset-free index: `reports/enemies/EXP-20260908-020.json`.
Retail PC exe SHA256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Original PC Anthill RAW: `c07452bafcf3799b55574d1622a37189358f5debcbd1127e167fd0fe0181700e`.
Original comparison used the auto-hardware exe
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
Original DAT: `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
No live memory writes, debugger changes or experimental engine patches occurred.

## Confirmed PC format and actor correspondence

Earlier [[EXP-20260816-172 - PC creature actor pool and behaviour VM census]]
already identifies the actor pool and VM; this experiment adds asset identity,
source placement editing, an independent packet codec and bounded runtime
acceptance. It does not claim discovery of the prior addresses.

PC loader `00465030` walks 14-byte packet headers. Native decoder `0049A200`
expands the payload. Anthill packet31, file offset299129, decodes to1796 bytes:
a type35 dword followed by64 records of28 bytes. Loader `0046574D..0046576A`
copies0x700 bytes to `00599EB0`. Builder `0041C420` skips a zero type byte and
initializes64 actor slots of132 bytes at `0059B628`; `0041BD10` copies stored XYZ
at source+0/+4/+8 into runtime coordinates multiplied by32, plus home and target.
Source+12 is the type byte, +13 the script selector, and the rest of each donor
row is retained. Native builder still performs its original per-type mutations.

| Editor type | Native type | Donor source / script | PC model family, 00445020 |
| --- | --- | --- | --- |
| Spider | 9 | 0 / 1 | `CHARS/BADBUG` |
| Mosquito | 10 | 4 / 4 | `CHARS/MOS` |
| Bee / wasp | 13 | 3 / 5 | `CHARS/WASP` |
| Pill bug | 39 | 2 / 36 | `CHARS3/PROTECT` |
| Caterpillar | 40 | 13 / 37 | `CHARS4/BADWORM` |

The original source table has21 of these enemies:7/4/5/2/3 respectively.
The remaining11 active source records are9 type11 seeds, type14 Dot in slot25,
and type35 in slot63 bound by `00445020` to `CHARS3/FLIKHARV`. Their exact source
rows and slots are preserved; type35's complete gameplay role is not inferred
from its model name. All original placements of the five supported enemy types
are disabled before authored rows are allocated. There are53 available source
slots, independent of the64 scenery slots. This upper authoring limit is not a
full-pool combat/plant-growth acceptance claim.

`actor-census.json`, the original read-only capture and model-binding functions
corroborate the static layout. `native-actors.json` runs original `0041C420` with
0,5 and53 authored enemies and verifies11,16 and64 initialized actors plus exact
XYZ/home/target for authored entries. A paired native `0041DC60` local-target
probe translates mosquito source/home/target consistently under identical random
bytes. It isolates the local-target operation; it is not a full AI replay.
The shipped mosquito is the native roaming source4 variant. Source1's shared
relative patrol was investigated but route editing is not exposed.

## Packet codec, corrections and preservation

`level_raw.py` independently implements a bounded bitstream reader and literal
writer from native-code observations, not copied decompiler pseudocode. Bounds
cover file/packet/output totals, header extents, truncation and backreferences.
Original opaque header bytes8..13 and complete suffixes are preserved. Their
semantics, including any checksum interpretation, remain unknown.
`raw-check.json` and regression tests compare169 decoded packets across PC
Levels01/02/03 with native `0049A200`, including canaries and re-encoded creature
packets. Unchanged packets remain compressed-byte-identical.

An initial production guard incorrectly required Anthill's12-byte suffix on all
levels. The Level03 regression exposed its9-byte suffix. The native loader tests
only the firstFFFFFFFF dword; the corrected parser requires that dword and retains
the remaining bytes. `tests.log` retains the initial121-pass/one-failure result;
`tests-corrected.log` records24 passing enemy tests. `tests-initial.log` separately
records a collection failure caused by missing PYTHONPATH, not a test pass.
The earliest private corpus attempt requested absent LEVEL15; the retained
initial log is superseded by the successful three-level run using LEVEL02.


`level_enemies.py` validates the pinned Anthill source, supported types/counts and
signed coordinates, and changes placement XYZ while preserving donor fields. An
explicit empty enemy list removes this whole enemy set.


## Runtime check

A live run with one edited table loaded all five types; 30 passive samples show
spider/mosquito/bee movement and animation, pill animation, and an idle
caterpillar, with all five visibility flags set. A second edited table with ten
placements (2 spiders, 3 mosquitoes, 2 bees, 2 pill bugs, 1 caterpillar) is
confirmed exactly in both source and runtime actor tables, with exact authored
source XYZ and script IDs (`scattered/live-enemies.json`). That sample mostly
observes offscreen/idle actors and does not itself prove movement for every
placement. Only LEVEL.RAW differs from the preceding build. Final focused
`make check` passes379 tests.

No exhaustive combat/damage/death/respawn, path editing, full-pool gameplay or
performance coverage is claimed. See [[PC Anthill enemy authoring]].

The bounded read-only PS1 comparison is recorded in [[XPORT-20260908-009 - Anthill enemy placement and model correspondences]]. PC evidence remains
authoritative; in particular PC type39 uses PROTECT, not the older PS1 ROLL label.
