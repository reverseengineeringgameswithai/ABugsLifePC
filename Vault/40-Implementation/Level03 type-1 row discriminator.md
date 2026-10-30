---
type: implementation
status: complete
updated: 2026-08-15
tags:
  - implementation
  - milestone/m3
  - re/gameplay
---

# Level03 type-1 row discriminator

## Boundary

This implementation exposes one exact Level03 mutation for
`EXP-20260815-116`. It does not expose type 1 through the general manifest
grammar and does not name the table as checkpoints, triggers, or spawn points.
PC type 1 has several static consumers.

## Exact recipe

- Source: `CD/LEVEL03/LEVEL.DAT`, SHA-256
  `bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b`.
- Table: top-record index 1, type 1, offset `0x458`, count 18.
- Row: index 6, offset `0x4A4`, signed XYZ
  `(15678,0,15438) -> (15806,0,15438)`.
- Output: same size, SHA-256
  `4894b6159e5a36a37fb9a3f50243cdd816fa4e7f28e169bcadf45b48792d4c12`.
- Physical diff: only byte `0x4A4` changes, `0x3E -> 0xBE`.

`reimplementation/ablpc/level03_type1_row_mod.py` requires the exact source
hash, validates the full DAT with `LevelDat.parse`, checks table identity,
count, row bounds, and old XYZ, reparses the output, constrains the diff to the
selected 12-byte row, pins the output hash, and reconstructs the input exactly.

`scripts/make-level03-type1-row6-x-plus-128` refuses paths outside `work/`,
linked/non-regular input, an existing output, and same-path input/output.
`tests/test_level03_type1_row_mod.py` is asset-free and covers local mutation,
inverse, wrong hash, wrong old value, and public-recipe refusal. Its four tests
pass in `EXP-20260815-132`; the combined five-family M3 recipe selection passes
25/25.

## Static prediction

[[FUNC-97C95BA5572D-00432930]] reads the selected authored X and Z as signed
dwords and stores them shifted left by five. If ordinary PC death/reset selects
row 6, the candidate therefore predicts post-respawn X changes by `+4096`
while Z is unchanged and Y is recomputed through the existing terrain path.

## Historical runtime gate

The original M3.5 plan required an unchanged PC executable, matched source/
control and candidate Level03 runs, exact run identity, and an observed row-
specific effect. `EXP-20260815-117` accepts that exact causal effect after
prior authorization of its prerequisite-state writes; `EXP-20260815-129/131`
separately supply and disposition the natural upstream boundary. Debugger
memory/register/code mutation is not implemented by this recipe and is not
authorized by this note.

## 2026-08-15 PC causal validation

The generated row-6 candidate is causally distinguished from control in the PC executable:

| build | Level03 row 6 | observed reset X/Z |
|---|---|---|
| control | `(15678, 0, 15438)` | `(501696, 494016)` |
| row-6 X `+128` | `(15806, 0, 15438)` | `(505792, 494016)` |

The runtime delta is exactly `(+128 << 5, 0)`. This validates the physical edit at `0x4A4` for the `0x00432930` consumer path. The receipt used disclosed debugger writes for prerequisite state and does not validate a natural death trigger. See [[EXP-20260815-116-receipt]].

## 2026-08-15 confirmed implementation contract

[[EXP-20260815-117 - Approved Level03 row-6 reset rerun]] confirms the
following PC behavior for reimplementation planning:

- preserve each type-1 row's X/Y/Z fields and unknown semantics;
- compare actor X/Z after signed shift right by 5;
- choose the nearest row under the executable's distance calculation;
- write selected row X/Z after shift left by 5;
- recompute Y through terrain logic rather than copying row Y mechanically.

Do not expose these rows as checkpoints in an API or editor unless future PC
evidence resolves their semantic label.

## Milestone disposition

[[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]] closes
M3.5 without claiming natural row-6 selection or checkpoint semantics.
[[EXP-20260815-132 - M3 exit-gate reconciliation]] retains this exact edit as
one of the independently reversible M3 recipe families and marks M3 Complete.
The recipe remains exact-hash and row-addressed, not a generic type-1 editor.
