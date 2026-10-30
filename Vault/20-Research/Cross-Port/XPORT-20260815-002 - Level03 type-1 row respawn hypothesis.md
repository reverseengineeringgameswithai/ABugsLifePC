---
type: cross-port-comparison
id: XPORT-20260815-002
status: completed
confidence: high
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
external_source_id: SRC-PS1-ABL
external_commit: 1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51
external_paths:
  - analysis/mechanics_baseline.yaml
  - analysis/phase4_respawn_row_provenance.json
pc_evidence:
  - EXP-20260815-116
  - EXP-20260815-117
  - EXP-20260815-129
  - EXP-20260815-131
  - FUNC-97C95BA5572D-00432930
  - FUNC-97C95BA5572D-0041C6C0
external_evidence:
  - analysis/mechanics_baseline.yaml:846-861
  - analysis/phase4_respawn_row_provenance.json:1391-1458
created: 2026-08-15
updated: 2026-10-02
tags:
  - re/cross-port
  - re/gameplay
  - milestone/m3
---

# XPORT-20260815-002 - Level03 type-1 row respawn hypothesis

## Bounded question

Does committed PS1 evidence identify one exact Level03 coordinate-row mutation
worth discriminating independently against the PC death/reset path?

## PS1 source

External source `SRC-PS1-ABL` at commit
`1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`. The external working tree was
heavily dirty, so only committed blobs were read through `git show`/`git
grep`. No working-tree file was used or modified.

## Confirmed on PS1

- `analysis/mechanics_baseline.yaml:846-861` records the PS1 safe-anchor
  behavior and an operator correction: retail has no in-world checkpoint
  activation object in this account, and kind `0x30` is a telescope rather
  than a respawn object.
- `analysis/phase4_respawn_row_provenance.json:1391-1458` records the
  Level03 type-1 table at offset `0x458` with count 18 and row 6 at
  `0x4A4`, raw XYZ `(15678,0,15438)`.
- That committed PS1 experiment changed row-6 X by `+128` and observed
  safe/live X change by `+4096` while Z remained unchanged and Y was
  ground-recomputed.
- The same evidence explicitly classifies type 1 as a generic DAT table slot,
  not a bespoke respawn table.

These are PS1 facts only.

## Confirmed on PC

- The exact PC `LEVEL03/LEVEL.DAT` independently has top-record index 1,
  type 1, count 18, table offset `0x458`, and row 6 at `0x4A4` with the same
  raw XYZ. Its SHA-256 is
  `bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b`.
- `0x00432930` scans PC type-1 rows by X/Z distance and writes selected X/Z
  shifted left by five; `0x0041C8CC` can set its `0x10` gate.
- Other PC functions consume type 1, so PC static evidence also rejects a
  bespoke-table claim.

## Similarities

The bounded data table, count, row index, file offset, raw coordinates, and
left-shift scale match. This makes the same `+128` authored X edit a precise
PC discriminator.

## Differences

Executables, runtime state machines, platform behavior, and proof status are
separate. The PS1 evidence includes a causal runtime outcome; PC currently has
only static/data evidence. The PS1 operator correction does not itself prove
the absence or presence of any PC checkpoint mechanic.

## Inferred correspondence

PC Level03 row 6 is a high-value candidate for the PC authored safe/respawn
selection path. This inference selected an experiment; it is not a PC
conclusion.

## Unknown

Whether ordinary PC death/reset selects row 6, how the safe row becomes
current, which hazards override it, and what non-respawn PC type-1 consumers
mean.

## Next discriminating PC experiment

Run unchanged-executable Level03 source and exact `+128` row-6 X arms through
the same natural death/reset. The PC prediction is a `+4096` X difference
only if row 6 is selected, with unchanged Z and terrain-recomputed Y.

## Result

The comparison is complete as experiment selection only. PC causality remains
open in `EXP-20260815-116` and `KU-057`.

2026-10-02 audit pointer: the PC discriminator above was run the same day.
[[EXP-20260815-117 - Approved Level03 row-6 reset rerun]] confirmed on PC,
after two authorized prerequisite writes, that the `+128` row-6 X edit moves
the reset X by exactly `+4096` with Z unchanged.
[[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]] reached
the same consumer naturally, selecting row 7 twice.
[[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]] then
resolved `KU-057` at the M3.5 boundary. Still unresolved on PC: a
controller-only row-6 contact, checkpoint semantics, and other rows or levels.
The PS1 observations above did not contribute to these PC results.
