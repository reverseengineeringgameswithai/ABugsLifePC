---
type: experiment
id: EXP-20261018-001
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static only. Capstone disassembly of retail bugs.exe, a raw rel32/absolute scan of .text, the existing Ghidra export, and the hash-checked retail RAW and DAT of all 17 engines through original_levels and level_dat; no game launch or memory access
question: Does any shipped creature row drive one of the creature subsystem's unbounded table indexes out of range (KU-069)?
result: No. In all 534 retail rows the type byte is 1–41, the script byte 0–39, and every script that walks a path list selects list 1–6, which exists in its level's DAT; opcode 10's start index stays below the list count. The bytes are multi-purpose, so the census models which byte each row really uses. Bit 0x20 rows (all 130 seeds) never run their script, and rows with byte +0x11 = 100 run it only on screen
status: complete-bounded
created: 2026-10-18
updated: 2026-10-29
evidence: [EXP-20260816-172, EXP-20261012-004, EXP-20261012-006, EXP-20260816-153]
tags: [experiment/static, re/creatures]
---

# EXP-20261018-001 - Creature row index census

## Question

KU-069 lists four creature-subsystem reads that index a table with a raw
level byte and no bound ([[EXP-20260816-172 - PC creature actor pool and behaviour VM census]]).
Its discriminating test was an offline scan of every retail type-`0x23` row.
This is section 7 of [[Next Tasks]].

| Source byte | Read | Table |
|---|---|---|
| `+0x0C` type | `0x0041C468`, `0x0041C476` | `0x004C881F` bytes; `0x00599CA8 + type*8` (`0x200` bytes cleared) |
| `+0x0D` script | `0x0041BD45` | 40 script pointers at `0x004C83F0` |
| `+0x0E` or `+0x0F` | `0x0041DDCD` (op 4), `0x0041DEDD` (op 10) | 64-dword list table `0x005C5860` |

## Method

`research/creature-rows/creature-row-census.py`, run with the project venv,
writes `reports/creatures/EXP-20261018-001.json`.

1. **Scripts.** The 40 shipped programs are decoded with EXP-172's
   instruction sizes. For each, the census records op 4 and op 10, op 10's
   operand, and whether op 12 changes flag bit 3.
2. **Rows.** Each engine's RAW creature packet is read through
   `original_levels.creature_rows` (hash-checked).
3. **Lists.** The DAT's top records are mapped to list slots the way
   `0x0044BB70` does: `|type|`, last record wins (`0x0044BC8B`,
   `0x0044BCA9`). The loader bounds `|type|` no more than the VM does.
4. **Which byte is used.** The new disassembly below decides which byte each
   row actually feeds to which table.

## What the code does with the bytes (retail disassembly)

- **List selector.** Op 4 and op 10 load
  `byte [source + 0x0E + ((+0x5C >> 3) & 1)]`
  (`0x0041DDB6`–`0x0041DDCD`, `0x0041DED2`–`0x0041DEDD`). Flag bit 3 picks
  `+0x0F`, otherwise `+0x0E`. No script's op 12 clears or sets bit 3, so the
  initial flags fix the choice.
- **List forms.** Both handlers test `word [list + 2] > 0x8000`, which is a
  negative record type (`0x0041DE15`, `0x0041DEE8`).
  - **Negative type:** 6-byte deltas from `+0x10`, added to the current
    target.
  - **Positive type:** absolute 12-byte XYZ rows from `+4`, shifted left 5.
  - Op 4 wraps the cursor `+0x5E` at the count and sets the condition to −1
    one step before the end (`0x0041DDE8`–`0x0041DE01`).
  - Op 10 with a nonzero operand starts the cursor at `+0x0F`
    (`0x0041DEC1`), with no check against the count.
- **`+0x0F` has other uses.**
  - **Seed rows:** for bit-`0x20` rows the initializer stores
    `+0x0E = +0x0F & 0x0F` (`0x0041BE1F`–`0x0041BE25`).
  - **Countdown:** the per-type handler at `0x0041C2C0` decrements `+0x0F`
    and reloads it with `(rand & 0x3F) + 0x28` (`0x0041C2DC`–`0x0041C30A`).

  The raw byte's range therefore says nothing by itself.
- **Seeds never run a script.** The interpreter `0x0041DC60` has one caller.
  Its thunk `0x004017F8` is called once, at `0x0041EE9F`. The Ghidra export
  and a raw scan of every `E8`/`E9` rel32 and absolute dword in the image
  agree on that single site. It lies on the arm that `0x0041EDA2`
  (`test cl,0x20 / je`) takes only when bit `0x20` is clear.
- **The VM gate.** With bit `0x20` clear, `0x0041EE89`–`0x0041EE9C` calls
  the interpreter when any of these holds:
  - flag bit `0x0001` is set: "on screen this frame", recomputed by
    `0x00456640` at `0x0041ED75` just before this loop
    ([[EXP-20261012-004 - Homing target visibility bit]]);
  - source `+0x11` is not `0x64`;
  - the type is 15.

  So a regular enemy (`+0x11 = 100`) runs its script only on frames it is on
  screen. The green grasshopper (type 15) is the exception.

## Results

534 rows in 17 engines:

| Byte | Shipped range | Bound that matters | Out of range |
|---|---|---|---|
| `+0x0C` type | 1–41 | 48 (the part of `0x004C881F` examined) and 64 (`0x00599CA8`) | none |
| `+0x0D` script | 0–39 | 40 | none |
| `+0x0E` | 0–6 | 64 | none |
| `+0x0F` | 0–246 | used as a selector only when bit 3 is set | none: bit 3 is set only on seed rows, which never run |
| DAT top-record type | −7 to 63 | 64 slots | none |

How often each row runs its script: never for 130 rows (all bit `0x20`,
all seeds, type 11); only on screen for 321; on every active frame for 83.

**Rows that walk a list.** 19 rows run a script containing op 4 or op 10.
Each names a list slot that its level's DAT fills:

| Engine | Creature (EXP-20261012-006) | Script | List slot | DAT record | Count |
|---|---|---:|---|---|---:|
| 1 Anthill | Dot (14) | 7 | 1 | type 1, absolute | 104 |
| 1 Anthill | mosquito (10) ×3 | 3 | 2, 3, 5 | types −2, −3, −5, relative | 48, 88, 65 |
| 4 City Entrance | taxi bug (18) ×6 | 23 | 1–6, one each | types 1–6, absolute | 84, 48, 66, 36, 150, 66 |
| 7 Clover Forest | mosquito (10) | 3 | 1 | type 1, absolute | 60 |
| 12 The Tree | acorn (31) ×7 | 27 | 1 | type 1, absolute | 251 |
| 15 Canyon Showdown | Hopper (22) | 28 | 1 | type 1, absolute | 313 |

The Tree's acorns use op 10 with a nonzero operand. They start at cursor
25, 50, 75, 100, 125, 150 and 200 on one 251-row list, all below the count.

**Seed rows.** Seeds keep bit 3 and a `+0x0F` of 0 or 1 (17 in one Anthill
Pt 2 row). A seed's script would select list 0, absent from every DAT but
Bug Bar's, or list 17. Because the gate keeps seeds out of the interpreter,
that read never happens.

## Confirmed, inferred, unknown

- **Confirmed (static, two forms: code and shipped data).** No retail row
  drives any of the four unbounded reads out of range. The reads remain
  unbounded in the code.
- **Confirmed (static).**
  - The interpreter's only caller is `0x0041EE9F` (Ghidra export and raw
    scan).
  - Bit-`0x20` rows never reach it.
  - The `+0x11 = 0x64` gate needs the visibility bit, except for type 15.
- **Confirmed (static).** Script 7 is Dot's flight on Anthill's type-1
  list. This agrees with [[FUNC-97C95BA5572D-004317D0]] and
  [[PC Dot flight path authoring]], which reached slot 25 and path 1 from
  other code, `0x004317D0`. EXP-20261018-002 adds the runtime form.
- **Inferred.**
  - `+0x11` is the respawn delay
    (EXP-20261001-006). Its
    value 100 also acts as "only think on screen", but nothing names that
    role. (Later the same day the gate itself was confirmed live:
    [[EXP-20261018-013 - Options screens and the creature gate live]].)
  - The relative lists move a mosquito from its own spawn: op 10 starts a
    relative list at the source XYZ (`0x0041DEF0`–`0x0041DF02`).
- **Unknown.**
  - The extent of the `0x004C881F` table (only 48 entries examined).
  - Which byte a row would use after an op 12 changed bit 3. No shipped
    script does that.
  - The `0x004C881F` table's meaning.

## Consequences

- **KU-069** is answered for shipped data. The code properties remain, so a
  reimplementation or mod must still choose to reproduce or refuse each
  out-of-range index.
- **Creature transplants.** A moved row that walks a list follows the list of
  the same slot in the target level. If that slot is empty, op 4 reads
  `word [0]` at `0x0041DDDE` and the game faults.
  - The derived test level of EXP-20261005-002 keeps Anthill's list 1 (Dot's
    route) and lists 2–7.
  - So the moved taxi bug of EXP-20261005-002 followed Dot's route, which
    EXP-20261018-002 confirms from that arm's saved samples.
  - The Canyon Showdown Hopper's list walk lives in script 28's tail. Only
    engine 15 enters that tail, so moved to a level on another engine he
    never walks.
- **KU-063.** Creatures consume type-1 lists in Anthill, City Entrance,
  Clover Forest, The Tree and Canyon Showdown. Five other levels hold a
  type-1 list that no creature walks: Council Chamber, Tunnels (the reset
  table, EXP-20260816-153), Riverbed Flight, Anthill Pt 2 and Riverbed
  Canyon. Bug Bar's lists 0–5 are walked by no creature either.

## Side correction

[[EXP-20261012-006 - Creature types from the character loader]] says 525
rows. Its own report's placements sum to 534, as this census counts. 525 is
534 minus Training's 9 rows.

## Artifacts

- `research/creature-rows/creature-row-census.py`
- `reports/creatures/EXP-20261018-001.json`: per-row bytes, flags, the gate
  class, the selector and list, and per-script opcode facts. These are
  numbers only, with no asset bytes.
