---
type: experiment
id: EXP-20260815-136
date: 2026-08-15
question: Can the retail PC Tunnels and City Entrance grain-gate minimums be independently changed with one guarded reversible executable recipe?
status: completed-with-independently-accepted-physical-follow-up
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
modified_binary_sha256: 69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b
environment: Fedora Linux 44; Wine 11 Staging; Gamescope 3.16.25; Direct3D 640x480x16
configuration: Tunnels rows 0..8 set to 1..9; City Entrance gates 0..2 set to 1,2,3; read-only runtime inspection; ordinary menu input
artifacts:
  - reimplementation/ablpc/grain_gate_mod.py
  - scripts/make-grain-gates
  - tests/test_grain_gate_mod.py
  - work/copies/grain-gates-test-123-1to9-full-disc/evidence/city-entrance-hardware-arm.log
  - work/copies/grain-gates-test-123-1to9-full-disc/evidence/tunnels-hardware-arm.log
addresses:
  - "0x00418780"
  - "0x0041879B"
  - "0x004187A0"
  - "0x00432810"
  - "0x00432B30"
  - "0x00433790"
  - "0x00433900"
  - "0x004338B0"
  - "0x004DA9C8"
  - "0x004DAA80"
  - "0x0059D9B1"
  - "0x00861C84"
result: exact-edit-and-load-accepted-with-independent-row3-gate0-follow-up
created: 2026-08-15
updated: 2026-08-15
tags: [re/experiment, re/static, re/runtime, mod/gameplay]
---

# EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements

## Question and boundary

Can a fresh work copy of exact retail PC `bugs.exe` expose independent minimum
grain requirements for the visible Tunnels and City Entrance gates without
editing assets or `originals/`? This experiment accepts the exact executable
transform and both modified levels' hardware-mode load. EXP-137 separately
adds physical threshold evidence for Tunnels row 3 and City Entrance gate 0,
independently accepted by EXP-138; that later boundary is not retroactively
part of EXP-136.

No PS1 source was consulted. The PC executable and PC runtime are the only
authorities used here.

## Corrected title-to-code mapping

The first static pass associated the two gate routines with the wrong visible
titles. Live PC level identity discriminated them:

- visible **Tunnels** sets `0x00861C84 = 3`; dispatcher `0x00418780` case 3
  at `0x0041879B` reaches `0x00432B30` through thunk `0x00401429`;
- visible **City Entrance** sets `0x00861C84 = 4`; dispatcher case 4 at
  `0x004187A0` reaches `0x00433900` through thunk `0x004012F8`.

The initial reversed association is rejected, not silently normalized.

## Tunnels static surface

Function `0x00432B30` loops over nine 20-byte resident records at
`0x004DA9C8`. Each record's dword at `+0x08` is compared with the unsigned
grain byte at `0x0059D9B1`. Exact retail requirements by resident row are:

| Row | Unknown `+0x04` | Requirement | X | Z |
|---:|---:|---:|---:|---:|
| 0 | 26 | 20 | 193754 | 131692 |
| 1 | 23 | 10 | 505642 | -451306 |
| 2 | 24 | 10 | 832302 | 291075 |
| 3 | 22 | 10 | 509676 | 510143 |
| 4 | 25 | 20 | 833246 | 612273 |
| 5 | 21 | 20 | 1142934 | 1308289 |
| 6 | 28 | 30 | 1471643 | 1410369 |
| 7 | 20 | 10 | 1202034 | 1986285 |
| 8 | 27 | 30 | 1634925 | 2534812 |

Initializer `0x00432810` copies 45 dwords from `0x004DAA80` to
`0x004DA9C8`: source load at `0x00432818`, destination load at `0x0043281D`,
count setup immediately afterward, and `rep movsd` at `0x00432822`.
Therefore a persistent executable recipe must patch both the image table and
its initializer template. Opening logic also links rows 0 and 4: either arm
updates the other's active type and animation/object. They remain separately
editable table entries, but independent visible behavior for that pair is not
claimed.

## City Entrance static surface

Function `0x00433900` contains the three calls found to thunk `0x00401D52`,
whose target is shared gate routine `0x00433790`. At
`0x004337D1–0x004337E3`, retail code computes and compares
`10 * (gate_index + 1)`, giving exact requirements 10, 20, and 30.

The recipe replaces 16 bytes at file offset `0x32BD1`, VA `0x004337D1`, with
an index lookup while preserving the existing unsigned grain-byte load. Its
three dwords occupy a 12-byte `INT3` alignment gap at file offset `0x32CB0`,
VA `0x004338B0`. The replacement bytes are exact-source guarded and the
whole transform proves an inverse before output.

## EXP-129 correction

The first visible Tunnels gate trace in
[[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]] occurred
near X/Z `(493260,509766)`. That is approximately 16,420 units from Tunnels
resident row 3 `(509676,510143)` and hundreds of thousands from every other
row. Its authorized grain change `1 -> 10` agrees with row 3's retail
requirement 10. EXP-129's attribution of that gate to `0x00433790` is therefore
rejected: Level03/Tunnels uses `0x00432B30`; `0x00433790` belongs to
Level04/City Entrance.

## Guarded transform and tests

`scripts/make-grain-gates` accepts exactly nine Tunnels requirements and/or
three City Entrance requirements, each in `0..50`, and keeps an unspecified
level at retail values. It requires exact retail SHA-256, source/output below
`work/`, distinct non-linked paths, a new output path, exact expected source
bytes, non-overlapping in-bounds edits, equal patch widths, and exact inverse
reconstruction.

The test profile sets Tunnels rows to `1,2,3,4,5,6,7,8,9` and City Entrance
to `1,2,3`. It produces same-size SHA-256
`69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b`,
touches 100 guarded bytes, changes 46 bytes, and exactly reconstructs retail.
Twelve asset-free tests cover layout pins, preservation, inverse, both
Tunnels tables, initializer copy behavior, invalid values/counts, source-byte
failure, public hash rejection, and exhaustive equivalence of the retail City
lookup to the old formula for all three indices and grain counts `0..50`.

## PC runtime receipts

The first launch arm is explicitly rejected because its log later entered
`INITSOFTRENDER`; it is not hardware evidence.

Two fresh hardware-selector arms used the modified full-disc work copy:

- City Entrance log SHA-256
  `374450a423d610488993a287e1cd0aa3b08f55973d63e6f7686d6ce3106cb2de`
  records Hardware selection, `Starting Direct3D`, Level04 load, and
  `NextLife`. Read-only inspection found internal level 4, grain 0, City table
  `(1,2,3)`, and the Tunnels active/template values `(1..9)`.
- Tunnels log SHA-256
  `323450265028218f10217035793664e0c75a12b046a06a19abfe2a33701952f3`
  records Hardware selection, `Starting Direct3D`, and Level03 load.
  Read-only inspection found internal level 3, grain 0, both Tunnels tables
  `(1..9)`, and the City table `(1,2,3)`.

Only ordinary menu input and a small ordinary steering attempt were used.
There was no target-memory write, debugger, breakpoint, executable mutation
during execution, asset edit, or `originals/` access. Each scoped process and
private sink was closed, and Wine `Y:` was restored to the ordinary full-disc
work copy.

## Result and limitations

Accepted at the exact-edit and hardware-level-load boundary: the visible
title mapping, retail consumers, reversible recipe, output identity, and
modified values resident after each relevant level load are PC-confirmed.

[[EXP-20260815-137 - Modified grain-gate threshold behavior]] now supplies a
below-minimum/exact-minimum transition for Tunnels row 3 and City Entrance
gate 0, independently accepted by EXP-138. Remaining unknowns include the
other eight Tunnels rows, other two City gates, complete player-facing
Tunnels ordering, and whether linked rows 0/4 can present independently. The
unknown `+0x04` field is not renamed. These limits are tracked in
[[Known Unknowns#KU-060 - Modified grain-gate physical transition]].

## Validation

- focused grain-gate suite: 12 passed;
- complete `make check`: Python doctor passed, Vault 396/0/0, five M4 hash
  anchors valid, 588 tests passed, and tracked-file audit 0;
- `git diff --check`: passed;
- final retail/profile hashes and equal 1,069,056-byte sizes: reverified;
- final Wine `Y:`, scoped process, and private-sink cleanup: reverified.
