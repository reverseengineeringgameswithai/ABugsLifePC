---
type: experiment
id: EXP-20260815-116
date: 2026-08-15
question: Does the PC Level03 type-1 row-6 coordinate feed the natural death/reset selector at 0x00432930?
status: superseded
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; offline PC static analysis and repository LevelDat parser
environment_version: repository state at session start d025d3a8bbf04da436d07348a8df990c3e9f9c46
working_directory: /home/dev/ABLPC
configuration: exact user-owned PC Level03 DAT work copy; no runtime launched
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M3-level03-type1-row-static-trace.md
addresses:
  - 0x0041C6C0
  - 0x0041C8CC
  - 0x0042DDB0
  - 0x004317D0
  - 0x004323A8
  - 0x00432930
  - 0x004369B0
  - 0x00437A20
  - 0x0043CE60
  - 0x0044BB70
  - 0x0059D960
  - 0x0059D964
  - 0x0059D968
  - 0x0059D9A0
  - 0x005C5864
file_offsets:
  - 0x458
  - 0x45C
  - 0x4A4
result: pc-static-and-exact-data-discriminator-ready; runtime-arms-diagnostic-only-superseded-by-EXP-20260815-117
created: 2026-08-15
updated: 2026-10-02
tags:
  - re/experiment
  - re/static
  - re/gameplay
  - milestone/m3
---

# EXP-20260815-116 - Level03 type-1 row discriminator

> Superseded 2026-08-15 by [[EXP-20260815-117 - Approved Level03 row-6 reset rerun]]: the
> runtime arms below used unapproved forced writes, so they are diagnostic only;
> EXP-117 is the approved rerun. The "M3.5 is active" result below is historical.

## Question

Does exact PC Level03 type-1 row 6 feed the natural death/reset selection path
at `0x00432930`?

## Exact PC boundary

- Executable: `bugs.exe`, 1,069,056 bytes, SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Data: `CD/LEVEL03/LEVEL.DAT`, 274,812 bytes, SHA-256
  `bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b`.
- Top-record index 0 is type `0x3F`, count 69, at `0x4` with size
  `0x454`. Index 1 is type 1, count 18, at `0x458` with size 220.
- Type-1 rows are 12-byte signed XYZ triples beginning at `0x45C`. Row 6 is
  at `0x4A4` and is `(15678,0,15438)`.

A metadata census parsed 21 PC `LEVEL*.DAT` files with the existing
bounds-checked parser. Multiple files contain type 1 with varying counts;
Training does not. This supports only a cross-level coordinate-table
classification.

## PC static evidence

`0x0044BB70` relocates type 1 into pointer slot `0x005C5864`.
`0x00432930` gates on `0x0059D9A0 & 0x10`, scans the 12-byte rows for nearest
X/Z distance, stores selected X/Z shifted left by five to `0x0059D960` and
`0x0059D968`, and recomputes `0x0059D964` through the existing terrain path.
`0x00437A20` is a near-identical variant selected through `0x0042DDB0`.

`0x0041C6C0` provides a static state join: at `0x0041C8CC`, its nonzero,
non-2 fourth-argument branch ORs `0x14` into `0x0059D9A0`, while exact 2
ORs only `0x04`.

Type 1 is not a bespoke respawn table. `0x004317D0`, `0x004323A8`,
`0x004369B0`, and `0x0043CE60` have additional coordinate-row consumers.
See the static trace and the two function dossiers.

## Bounded cross-port hypothesis

[[XPORT-20260815-002 - Level03 type-1 row respawn hypothesis]] records the
committed PS1 evidence at external commit
`1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`. It selects the exact row-6
mutation as a discriminator but establishes no PC behavior.

## Candidate recipe

Change raw row-6 X from `15678` to `15806` (`+128`), leaving Y/Z unchanged.
Only physical byte `0x4A4` changes (`0x3E -> 0xBE`). The same-size output is
SHA-256
`4894b6159e5a36a37fb9a3f50243cdd816fa4e7f28e169bcadf45b48792d4c12`,
reparses, and inverses exactly.

If `0x00432930` selects this row, the PC static shift predicts runtime X
changes by `+4096`, Z remains unchanged, and Y is terrain-recomputed.

## Implementation

- `reimplementation/ablpc/level03_type1_row_mod.py` supplies the exact guarded
  recipe and inverse proof.
- `scripts/make-level03-type1-row6-x-plus-128` writes only a fresh output
  under `work/`.
- `tests/test_level03_type1_row_mod.py` supplies asset-free regression cases.

Tests were not executed in this session. No game, Wine, debugger, or capture
process was launched.

## Interpretation

PC data and static code independently support a precise candidate selector.
They do not prove natural PC death/respawn reaches row 6, and they do not prove
an in-world checkpoint activation system.

## Result

**M3.5 is active, not complete.** The exact offline discriminator is ready.
PC runtime causality remains `KU-057`.

## Follow-up

After explicit runtime approval and lifecycle preflight, build a complete
ignored source/control pair with the unchanged executable. Induce the same
natural Level03 death/reset without debugger mutation, bind exact run identity,
and accept only a row-specific `+4096` X effect or record the contradiction.

## 2026-08-15 causal runtime update

Status: **PC row-to-reset consumer confirmed; natural trigger still open.**

The control and one-byte row-6-X candidate were executed under Wine with matching Level03 identity gates. The successful arms explicitly reproduced the natural path's prerequisite state with two debugger writes: actor bit `0x10` at `0x0059D9A0` and `level_done = 2` at `0x0059A5B0`.

- control row 6 `(15678, 0, 15438)` produced reset `(501696, 30092, 494016)`;
- candidate row 6 `(15806, 0, 15438)` produced reset `(505792, 30120, 494016)`;
- DAT delta `+128` X produced runtime delta `+4096` X, exactly `128 << 5`;
- Z remained `494016` in both arms;
- the candidate trace contained no control-coordinate hit.

This confirms the Level03 type-1 row-6 X/Z consumer at `0x00432930` on PC. It does not confirm the upstream natural death trigger. See [[EXP-20260815-116-receipt]] and [[2026-08-15 0920 - Codex - Level03 type-1 row causal runtime]].

## 2026-08-15 hard-truth correction and supersession

- The forced prerequisite writes in this experiment lacked prior explicit user
  approval, so this receipt is diagnostic evidence only and is not the
  governance-valid milestone discriminator.
- The accepted control injection point and candidate injection point did not
  match. Both were inside row 6's nearest-region; endpoint equality must not be
  claimed.
- [[EXP-20260815-117 - Approved Level03 row-6 reset rerun]] supersedes the
  governance aspect with fresh control/candidate processes after explicit
  approval of the exact writes.
- The semantic label `checkpoint` remains unconfirmed even after the approved
  coordinate-consumer result.
