---
type: experiment
id: EXP-20261018-002
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Offline reanalysis of read-only samples already saved by two hardware arms (EXP-20260913-002 under derived EXEs 0480e36b… and 3d02de3a…; EXP-20261005-002 under c3d8b207…, all six hardware markers in its log), with byte comparison of those EXEs against retail; no new game launch or memory access
question: Do live creature program counters (+0x70) step through the decoded shipped scripts (KU-068)?
result: Yes, for two slots in two arms. Dot's 800 samples hold three values, all decoded instruction starts of script 7, in the order the static model predicts from the first active frame. The moved taxi bug's 55 samples sit in script 23 (and script 13 once dead), and in every one its op-4 target equals the level's list-1 entry at its cursor, shifted left 5
status: complete-bounded
created: 2026-10-18
updated: 2026-10-29
evidence: [EXP-20260913-002, EXP-20261005-002, EXP-20261018-001, EXP-20260816-172]
tags: [experiment/runtime, experiment/static, re/creatures]
---

# EXP-20261018-002 - Creature script counter in saved runtime samples

## Question

KU-068 asked whether any slot's `+0x70` actually advances through the 40
decoded programs while the game runs. Its proposed test was one read-only
sample of an active slot. Two earlier arms already took such samples for
other purposes, so this experiment reads them instead of launching a game.

## Sources

- **Dot.** EXP-20260913-002
  sampled Anthill slot 25 (`0x0059C30C`) for `+0x70`, `+0x5E` and `+0x5C`:
  - 100 samples in each of eight `dot-*.json` files: 300 in `play/`,
    100 in `ready/` and 400 in `summit/`;
  - EXEs `0480e36b…` (play, ready) and `3d02de3a…` (summit);
  - all three arms passed the six hardware markers, per that note.
- **Taxi bug.** EXP-20261005-002's
  `tough-regulars` arm logged the moved taxi bug's whole `0x84`-byte slot
  (type 18, slot 14 of the derived test level) in 55 samples.
  - EXE `c3d8b207…`; its `bugs.log` has all six markers.
  - DAT `14d7fd8d…`, whose list 1 is a 104-row Dot route.

## Are the derived EXEs the retail VM?

`research/creature-rows/script-counter-samples.py` compares eight VA regions
of each EXE with retail:

- the script bodies and table;
- the interpreter and its dispatch tables;
- the initializer `0x0041BD10` and the builder `0x0041C420`;
- the per-frame update `0x0041EC40`;
- thunk `0x004017F8`;
- the visibility pass `0x00456640`;
- the sequence table.

All are byte-identical except six bytes at `0x0041EDB4` in the per-frame
update, the same in all three builds. That is EXP-20260908-001's hook
(`reimplementation/ablpc/dynamic_limits.py`). It sits after
`0x0041EDA2`'s bit-`0x20` test, on the seed arm, which neither Dot (flags
`0x0080`) nor the taxi bug (`0x8042`) takes. The code these slots execute is
therefore the retail code.

## Results

### Dot, script 7

Script 7 decodes as follows (`0x004C7E98`):

| Offset | Instruction |
|---|---|
| `+0x00` | op 22 |
| `+0x06` | op 10 (0): cursor 0, place on the list |
| `+0x0A` | op 12 (−5, 4): set flag 4 |
| `+0x10` | op 13 (0, 2) |
| `+0x16` | op 4: next point |
| `+0x18` | op 9: blocking |
| `+0x1A` | op 16 (1200): Flik within 1200? |
| `+0x1E` | op 8: if so, back to `+0x16` |
| `+0x22` | op −1: back to `+0x18` |
| `+0x26` | op 0 |

The branch target uses `edi + 2 + operand*2` (`0x0041DEA4`–`0x0041DEAC`),
the jump `edi − operand*2` (`0x0041E128`–`0x0041E12E`).

The 800 samples hold exactly three values, all instruction starts:

| `+0x70` | Offset | Samples | Meaning in the static model |
|---|---|---:|---|
| `0x004C7E98` | `+0x00` | 309 | not yet run |
| `0x004C7EB0` | `+0x18` | 187 | op 9 blocked; stored at `0x0041E147` |
| `0x004C7EB2` | `+0x1A` | 304 | op 9 + 2, the step past a block resumed at frame start (`0x0041E13B`–`0x0041E140`) |

The `ready/` arm shows the first activation:

1. 9 samples at `+0x00`, cursor 0, flags `0x80`. Bit `0x4000` is clear, so
   the slot is not yet selected by `0x0041EC40`.
2. Then `+0x18` with cursor 1 and flags `0x4085`.

That is one pass through ops 22, 10, 12 (flag 4 appears), 13 and 4
(cursor 0 → 1), stopping at op 9, exactly as decoded. The summit arm's 300
unselected samples at `+0x00` are the "Dot initially stays at path 0" that
EXP-20260913-002 recorded. Its last file runs at cursor 98.

`0x004317D0` also writes slot 25's cursor (`0x0059C36A` at `0x004318DE` and
`0x004319D7`), so the cursor alone is not VM evidence. No code references
slot 25's `+0x70` (`0x0059C37C`) absolutely: the raw scan finds none, and
neither `0x004317D0` nor its callees `0x00414F80` and `0x00459620` write
`[reg+0x70]`. The `+0x70` values come only from the interpreter's own stores.

### Taxi bug, script 23

Script 23 (`0x004C80E8`) decodes as: op 22, op 13, op 10 (0), then a loop
of op 4 at `+0x10` and op 9 at `+0x12`, with op −1 jumping back.
EXP-20261018-001 found that the taxi bug's row selects list 1.

- **Program counter.**
  - 49 samples at `+0x12`, op 9 blocked.
  - 4 at `+0x14`, op 9 + 2.
  - 2 at `0x004C7F6A`. That is script 13 + 2 (op 7, then a jump back to it),
    taken after the bug died: health `+0x6E` 0, flags `0x88C1`. Fourteen
    sites load script 13's table entry `0x004C8424`. One of them,
    `0x0041CF9F`–`0x0041CFA5`, stores it to `+0x70` beside
    `flags |= 0x0880`. Which one ran here is not traced.
- **Target.** In all 55 samples the target `+0x34/+0x38/+0x3C` equals the
  image's list-1 row at `+0x5E`, shifted left 5.
  - That is op 4's absolute branch, `0x0041DE62`–`0x0041DE8D`.
  - The cursor runs 5 → 37 while the bug moves east to stored X ≈ 19,281.
  - This explains EXP-20261005-002's "ran far east (to x ≈ 19,000)": op 10
    put the bug on Dot's route and op 4 walked it.

## Confirmed, inferred, unknown

- **Confirmed (runtime samples plus static decode).**
  - Live `+0x70` values of two slots are decoded instruction starts of the
    programs their rows name (7 and 23), and of the death script 13.
  - Dot's first activation follows the decoded path step for step.
  - The taxi bug's targets are exactly the op-4 rows of the list its
    `+0x0E` selects.
- **Bounded.**
  - The samples were taken for other questions, without `+0x60`.
  - Two slots and three programs are covered, under derived EXEs whose
    relevant code is byte-identical to retail. The other levels and
    programs are covered statically only.
- **Unknown.**
  - What the five modes do, so how op 9 moves a slot. (Answered statically
    the same day: [[EXP-20261018-003 - Creature VM movement modes]].)
  - Which of the 14 script-13 sites killed the taxi bug.
  - The behaviour of other programs at runtime.

## Consequences

KU-068 is answered at this boundary: the creature VM runs, its program
counter persists as the static model says, and op 4 follows the level's
list. Its remaining scope moves to the mode question.

## Artifacts

- `research/creature-rows/script-counter-samples.py`, which reads the saved
  packets under `work/experiments/` (not committed) and the three EXEs.
- `reports/creatures/EXP-20261018-002.json`: per-build region differences,
  per-arm counter histograms and runs, and the taxi bug's target matches.
  Its `motion` block (speed, landing, arrival distances, home and leash)
  belongs to [[EXP-20261018-003 - Creature VM movement modes]].
