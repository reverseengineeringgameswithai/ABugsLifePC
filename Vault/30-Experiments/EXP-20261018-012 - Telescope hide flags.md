---
type: experiment
id: EXP-20261018-012
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static, whole image. Raw absolute-reference scan and a skip-data capstone sweep of retail bugs.exe, with the Ghidra export for function bounds; no game launch
question: What is the byte 0x00599C69 that City's gate-0 opening sets (KU-067), and who reads it?
result: It is the second of four per-level telescope hide flags, 0x00599C68–0x00599C6B. The pickup walker 0x00417720 is their only reader. For the nth telescope row (selector 0x30, counted in table order) it reads 0x00599C67 + n and, if set, parks that telescope at Y 0x80000000 so it is gone. A level-start routine clears all four, and level routines set them when a telescope's job is done
status: complete-bounded
created: 2026-10-18
updated: 2026-10-18
evidence: [EXP-20260816-167, EXP-20260816-168, EXP-20260818-003, EXP-20260927-001]
tags: [experiment/static, re/level-data]
---

# EXP-20261018-012 - Telescope hide flags

## Question

City's gate routine `0x00433790` writes `0x00599C69 = 1` when gate 0 opens
(`0x00433807`). KU-067 asked what the byte means, and proposed a static
writer/reader census as the first step. On 2026-10-12,
[[FUNC-97C95BA5572D-004317D0]] found Level01 writing the same byte as
"second-telescope suppression".

## The reader

The pickup walker `0x00417720` counts telescope rows (selector `0x30`) in
`[esp+0x14]` as it walks the pickup table (`0x0041779D`–`0x004177A5`).

For a telescope row (`0x0041787A`–`0x00417899`) it then reads
`byte [0x00599C67 + n]`:

- nonzero: it stores Y `0x80000000` in the row's `+4` and skips it;
- zero: the telescope bobs as usual (`0x0041789E` onward).

So `0x00599C68`, `69`, `6A` and `6B` hide the first to fourth telescopes. No
other instruction reads any of the four bytes.

## The writers

| Site | Function | Writes |
|---|---|---|
| `0x0042E838`–`0x0042E84A` | `0x0042E5C0`, which also calls the level load at `0x0042E6ED` | all four = 0 |
| `0x00437E21`–`0x00437E3A` | `0x00437B70` | `6B`, `6A`, `69` = `bl` |
| `0x00431A4B`, `0x00431A5B` | Anthill `0x004317D0` | 2 and 3 = 1 |
| `0x004332E5` | `0x00432B30` | 2 = 1 |
| `0x00433807` | City gate routine `0x00433790`, gate 0 | 2 = 1 |
| `0x00433D63` | `0x00433900` | 3 = 1 |
| `0x00434005`, `0x00434D8C` | `0x00433F90`, `0x00434BE0` | `[edx + 0x00599C68]` = 1 (indexed) |
| `0x00436F32`, `0x004375D4`, `0x004375E6` | Anthill Pt 2 `0x00436B40` | 1, 2 and 3 = 1 |
| `0x00439123` | `0x00438A80` | 2 = 1 |
| `0x0043B87B` | Canyon Showdown `0x0043AE00` | 2 = 1 |

`0x0041788A`'s `0x00599C67` is the reader's base, one below the array.
Nothing else references `0x00599C66`–`0x00599C6B`.

## Confirmed, inferred, unknown

- **Confirmed (static, whole image).** The four bytes are telescope hide
  flags, with one reader and the writers above. City's gate-0 opening hides
  the level's second telescope.
- **Inferred.**
  - Which telescope is "second" is table order. City's map would show which
    one that is ([[EXP-20260927-001 - Complete original level Blender maps]]
    keeps the table order).
  - That a routine hides a telescope once its view has served its purpose is
    a reading of the call sites, not traced per level.
- **Unknown.**
  - The counter's start value (`edx` at `0x00417771`) was not traced, so the
    1-based mapping rests on the base `0x00599C67`.
  - **Runtime.** No live observation. KU-067's proposed read-only City
    trace would add it.

## Consequences

KU-067 is answered statically: the byte is "hide telescope 2", not a
City-only gate flag.
