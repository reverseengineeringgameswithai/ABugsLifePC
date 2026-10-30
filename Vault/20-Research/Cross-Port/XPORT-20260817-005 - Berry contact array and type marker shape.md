---
type: cross-port
id: XPORT-20260817-005
date: 2026-08-17
source_id: SRC-PS1-ABL
source_commit: 1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
status: completed
updated: 2026-10-02
tags:
  - research/cross-port
  - re/runtime
---

# XPORT-20260817-005 - Berry contact array and type marker shape

## 1. Bounded question

The PC port's berry-type selector is unlocated (`KU-073`). Does the PS1 project
describe a berry projectile/contact structure and a type selector whose **shape**
suggests what to look for on PC?

This note records comparative structure only. Under
[[Cross-Port Evidence Policy]] nothing here is a PC claim.

## 2. PS1 source

- Source ID: `SRC-PS1-ABL`, external and read-only.
- Commit: `1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`.
- Paths and locators:
  - `ABL_RE_NOTES.md` line 62 — "contact array `0x800b0d18` (64×0x38)"; also
    "berry marker `0x800a6597`".
  - `ObsidianVault/Canon/Systems/SYS_berry_pickup_render_descriptors.md` — five
    native pickup kinds `0x20`-`0x24` mapping to equip indices, and the
    statement that pickup handlers arm a single equip index byte.
  - `ObsidianVault/Experiments/EXP_2026-08-04_phase4_d17_bird_defeat.md` lines
    118-133 — berry type read as `lbu v1,0x2C(s1)`, feeding a branch chain that
    selects damage. (Locator check 2026-10-02: in the blob at this commit,
    lines 118-133 hold the damage branch chain; the `+0x2C` load is at
    line 160.)

## 3. PC locator

Binary `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Runtime evidence in [[EXP-20260817-187 - Runtime berry throw reconnaissance]]:
throw-exclusive projectile pool with stride `0x38`, consistent with 64 records
over `[0x00598C00, 0x00599A00)`.

## 4. Directly observed similarities

- **Stride.** PS1 contact array records are `0x38` bytes. The PC pool's stride
  was measured independently at `0x38`, from successive record starts
  `0x00599640`/`0x00599678`/`0x005996B0`, **before** the PS1 figure was read.
- **Element count.** PS1 gives 64 records. The PC pool's observed slot alignment
  and `+0x1C == -1` in 58 of 64 slots are consistent with 64.

This is the strongest structural correspondence found between the ports to date,
and it was arrived at independently on each side.

## 5. Directly observed differences

- **`+0x2C` does not correspond.** PS1 reads berry type as a **byte** at record
  `+0x2C`. On PC, `+0x2C` holds a dword identical across all live records, and
  rewriting all 49 occurrences and holding the value produced **no visual
  change**. The PC field at that offset is not the type selector.
- **No PC analogue of the `0x800A6597` marker has been found.** PS1 keeps one
  byte, armed by pickup handlers and read at throw. The PC equivalent, if it
  exists, is unlocated.
- Address spaces do not correspond at all: PS1 MIPS globals at `0x800xxxxx`
  versus PC x86 PE data at `0x004`-`0x005xxxxx`. No mapping between them exists
  or should be attempted.

## 6. What remains unknown

Whether the PC port uses a single type/equip byte at all, or encodes berry type
some other way — a per-record field at a different offset, a pointer to a
per-type descriptor, or separate pools per type. The PS1 shape suggests the
first; nothing on PC confirms it.

## 7. Smallest discriminating PC experiment

A single hardware write-watchpoint on one pool record during one throw. It
reports the spawning instruction directly, from which the type dispatch is
readable as PC code. That is a PC-native answer requiring no cross-port
inference, and it needs explicit approval under
[[Agent Operating Manual#Dynamic analysis]].

Failing that, a researcher-labelled A/B — a named berry colour before each
sample — gives the memory diff the ground truth it currently lacks.

## Standing note on method

Running score for structural transfer between these ports: **one hit** (the
64×`0x38` contact array) and **one miss** (`+0x2C` as the type byte). Structure
transfers often enough to be worth generating hypotheses from, and not reliably
enough to be trusted without PC verification — which is exactly what
[[Cross-Port Evidence Policy]] already requires.

## Continuation (2026-08-18)

[[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]]
answers §6's open shape question with a PC static candidate: an instrumented
interpreter-movie replay captured the PS1 marker's contact-time consumer
(`table[row*5 + marker]`, `+2`, cap 200, threshold 100), and that exact
arithmetic located `candidate_berry_equip_byte` `0x0059D9A7` with
`candidate_berry_hit_accumulator` `0x00599B20` on PC. The running score there
becomes two hits, one miss. `KU-073` remains open pending the read-only
labelled A/B.

2026-10-02 audit pointer: `KU-073` was resolved for the selector the same day.
[[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]]
confirmed `0x0059D9A7` causally on PC with guarded writes, which answers §6
and §7 by PC evidence. This note's status is therefore `completed`. The
`+0x2C` miss and the address-space boundary in §5 stand.
