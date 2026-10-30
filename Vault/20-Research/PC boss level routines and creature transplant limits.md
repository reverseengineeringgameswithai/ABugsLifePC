---
type: research
status: confirmed-bounded
created: 2026-10-29
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20261005-001, EXP-20261005-002, EXP-20260914-010]
tags: [re/actors, re/level-routing, re/combat, re/static, re/runtime]
---

# PC boss level routines and creature transplant limits

Which parts of a boss belong to its creature row and which belong to its home
level's code, the native boss placements, and the per-level routines that run
the fights and hazards. [[PC native creature transplant]] owns the transplant
procedure and its per-donor outcomes; this note keeps the engine facts behind
it. EXP-20261005-001 and EXP-20261005-002 (not in this vault) first recorded
them, from static work on the retail executable and hardware runs of creatures
moved into Level01 (engine 1). EXP-20260914-010 first recorded the Cliffside
bird boundary.

## What a creature row carries

- **Model by type.** The character loader `0x00445020` switches on each pool
  slot's type. Case `0x10` pushes `"chars2\thumper"` (`0x004DDEF0`,
  referenced at `0x0044531F`), so type 16 is Thumper. Case `0x1D` (29) is
  `chars3\molt`. A type-35 row placed in another level made the engine load
  `chars2\thumper.anm` and `.all` by itself (hardware log). Every type's file
  is in [[EXP-20261012-006 - Creature types from the character loader]].
- **Model files.** Council Chamber's RAW packets 0x101/0x102 whose second
  dword is 16 equal `CD/CHARS2/THUMPER.ANM` (34,304 B) and `THUMPER.ALL`
  (11,804 B) after their 8-byte heads, byte for byte. The loader `0x00465030`
  has no case for these tags, so they are inferred unused on PC
  ([[EXP-20261018-010 - Two inert data items]] rechecked the whole image).
- **Texture page.** All 174 Thumper faces use texture page 21, which
  Level01's RAW lacks; the page must come with the creature. City Square's
  roach (type 19) names page 18 on 4 of its 168 faces, a page City Square never
  loads (also in [[EXP-20260927-001 - Complete original level Blender maps]]).
- **Model records.** With Thumper added to Level01, the model records at
  `0x005A9660` were used up to index 200 of 300, and the overflow flag
  `0x005C5960` read 0.
- **Avoid two slots.** Engine 1's update writes through slot 25 (Dot)
  unchecked, and level start special-cases slot 63.
- **Sprites.** Engines 1 and 2 copy byte-identical 50-descriptor sprite
  tables (`0x004DA6B0`, `0x004DA7B8`). The sprite tables share entries 0–49
  across engines 1, 6, 8, 9, 11, 13, 14 and 15; the extra entries 50–52 feed
  only level-routine effects (rain, feathers, crowd).
- **No crash path** (inferred from confirmed parts). The audited boss scripts
  use no op4, op10 or op11 in reachable code; sounds return early when a sample
  is not loaded (`0x0049D820`); kill and release take the default arm for
  types 22, 29, 30 and 36. The taxi bug's script 23 is an exception that does
  use op 4 and op 10; see [[PC native creature transplant]].
- **Respawn byte** (`+0x11`). 101 is a literal 101-frame countdown, 100 uses a
  per-type table delay, and 0 removes the creature for good.
- **Waking.** Every boss gained flag bit 0x0001 once awake, usually with
  0x4000 (for example 0x44 → 0x4045, 0x144 → 0x4145, 0x984 → 0x4985). Bit
  0x0001 is the per-frame in-view bit
  ([[EXP-20261012-004 - Homing target visibility bit]]).
- **Health and immunity.** Health `+0x6E` comes from row `+0x10`; 100 or more
  is immune. See [[PC projectile records, homing and kill accounting]] for
  damage and flags.

## Native boss placements

A census of every type-35 row on the retail disc found eight boss placements
besides Thumper, each a single high-health row driven by its level, plus the
tougher regular types used in EXP-20261005-002:

| Creature | Home (engine, slot) | Type | Script | Health | Respawn byte | Flags |
|---|---|---|---|---:|---:|---|
| Thumper | Council Chamber (2, 1) | 16 | 9 | 50 | 0 | 0x52 |
| Molt | Battle Arena (13, 4) | 29 | 11 | 50 | 0 | 0x42 |
| Hopper | Riverbed Flight (8, 38) | 22 | 18 | 101 | 101 | 0x454 |
| Hopper | Anthill Pt 2 (9, 22) | 22 | 22 | 99 | 0 | 0x44 |
| Hopper | Canyon Showdown (15, 9) | 22 | 28 | 30 | 0 | 0x52 |
| Bird | Cliffside (6, 0) | 30 | 26 | 101 | 0 | 0x984 |
| Bird | Bird Nest (11, 10) | 30 | 26 | 50 | 0 | 0x144 |
| Bird | Canyon Showdown (15, 21) | 30 | 29 | 101 | 0 | 0x84 |
| Thud | Bug Bar (14, 0) | 36 | 19 | 50 | 101 | 0x54 |
| Green grasshopper | Tunnels (3, 36) | 15 | 8 | 6 | 100 | 0x52 |
| Centipede | Tunnels (3, 4) | 41 | 38 | 8 | 100 | 0x4 |
| Fly | City Entrance (4, 11) | 6 | 15 | 8 | 100 | 0x8006 |
| Hspider | City Entrance (4, 10) | 17 | 11 | 4 | 100 | 0x8102 |
| Taxi bug | City Entrance (4, 0) | 18 | 23 | 3 | 100 | 0x8042 |
| Roach | City Square (5, 0) | 19 | 12 | 6 | 100 | 0x42 |

Thumper's row (EXP-20261005-001) is stored at (141, −1857, 101); the native
floor below is 1693.5, so he starts 3,550 units above it. His respawn byte 0
is static (row `+0x11`); his flags 0x52 are the hardware read of the moved
row. Other single-placement characters (circus bugs, Atta, Dot,
Soil, Tuck and Roll, acorns, blue scouts) have health 1 or 101 with scripted
roles and were not treated as bosses.

## The fights are level routines

Each level's init and per-frame routines are reached through the init table
`0x004186FC` and the per-frame table `0x004187E8` (dispatcher `0x00418780`,
called at `0x004145BB` with `[0x00861C84]`; the per-frame entries are listed in
[[EXP-20260816-146 - Grain-gate level exclusivity static proof]]). None of this
code moves with a creature row.

| Engine, level | Init | Per-frame | What it does |
|---|---|---|---|
| 1, Anthill | `0x00431730` | `0x004317D0` | among creature slots and paths, touches only slot 25 and path 1; it also sets telescope hide flags ([[FUNC-97C95BA5572D-004317D0]]) |
| 2, Council Chamber | `0x00431BF0` | `0x00431CB0` | Thumper: reads slot 1 (`0x0059B6AC`) and slots 2/3; plays hit voices; makes slot 2 or 3 his thrown projectile; below health 21 runs a camera cut, script 13 and `[0x0059A5B0] = 1` (won). The HUD health bar (`0x00416890`, at `0x0041725A`) draws only in engine 2. |
| 6, Cliffside | `0x004345F0` | `0x00434620` | the bird tracks Flik and kills him when he falls into a band (an enforcer, not a fight); boundary below |
| 8, Riverbed Flight | `0x004361C0` | `0x004362D0` | Hopper follows Flik's trail and taunts |
| 9, Anthill Pt 2 | `0x004369B0` | `0x00436B40` | Hopper flies a path, lowers per hit and releases Atta at health 90; the win comes from slot 23 |
| 11, Bird Nest | `0x00437FD0` | `0x00438040` | the bird chases high; below 21 the level is won |
| 13, Battle Arena | `0x004393C0` | `0x00439410` | hurt animation, crowd projectiles; win below 21 |
| 14, Bug Bar | `0x00439D30` | `0x00439E90` | Thud shuttles and throws; hits count only at the two ends; 8 counted hits win |
| 15, Canyon Showdown | `0x0043AD00` | `0x0043AE00` | staged immunity and a waypoint run, below; the bird carries Hopper off with a movie |

EXP-20261005-002 listed one address per level, and for Cliffside and Riverbed
Flight it gave `0x004345F0` and `0x004361C0`, which differ from the per-frame
entries `0x00434620` and `0x004362D0`. A read of the retail executable's jump
tables on 2026-10-29 (SHA `97c95ba5…`, entry → thunk → routine) resolves this.
The init dispatcher `0x00418690` does `cmp eax,0x11; ja; jmp [0x004186FC +
eax*4]` on the engine index, and entry 6 → `0x004011DB` → `0x004345F0`, entry
8 → `0x00401C2B` → `0x004361C0`, so those two are the init routines. The full
init table for engines 0–17 is `0x00441D00`, `0x00431730`, `0x00431BF0`,
`0x00432810`, `0x004335C0`, `0x00433F50`, `0x004345F0`, `0x00434980`,
`0x004361C0`, `0x004369B0`, `0x00437B40`, `0x00437FD0`, `0x00438720`,
`0x004393C0`, `0x00439D30`, `0x0043AD00`, `0x0043BC00`, `0x0043C040`. The
same read reproduces the per-frame entries of EXP-20260816-146 for engines
1–17. Two cross-checks agree: `0x00432810` is the Tunnels routine that
initializes the gate table ([[PC grain gate requirements]]), and `0x0043C040`
is the Training routine that registers the hidden seed tokens
([[PC gameplay loop and player event sites]]). The Ghidra export shows
`0x004345F0` as a short routine that writes `0x0059F080`, `0x0059F084` and
the bird state `0x0059F07C`. Except for Council Chamber and Canyon Showdown,
which of the two routines carries each behaviour in the last column was not
traced.

## Thumper's script and handler

- Script 9 (`0x004C7EE8`..`0x004C7F08`): a frame sequence, a blocking fall
  (op6, mode 4) that spawns dust type 1 on landing, op11 subroutine 4
  (`0x00431C90`: `[0x0059EF70] = 60`, read only by `0x00431CB0`), then a loop
  of random waits and random targets around home. Nothing reads the engine.
- The handler `0x0041C100` only plays looping sound row 0x1A (sample 31,
  `WASPBUZZ.WAV`, present in banks 1–18). It deals no damage.
- In hardware in Level01: the moved row read type 16, health 50, flags 0x52,
  script PC `0x004C7EE8`; awake, flags 0x4053/0x5053/0x1053 and PC
  `0x004C7F02`; dead, type 0, health 0, flags 0x18D1 (0x880 set), respawn 0,
  PC `0x004C7F6A`. His health persisted across Flik's deaths and reset on
  level re-entry, and the enemy total read 11 (10 + Thumper).

## Canyon Showdown staged immunity

Static, retail disassembly (EXP-20261005-002). Engine 15's per-frame routine
`0x0043AE00` makes Hopper immune by restoring his health after a hit, not by
flags. He is slot 9 (record `0x0059BACC`: `+0x44` animation group
`0x0059BB10`, `+0x5E` `0x0059BB2A`, `+0x6E` health `0x0059BB3A`, `+0x70`
program counter `0x0059BB3C`).

- **Remembered health.** Init `0x0043AD00` stores his row health (30) in
  `0x0059F640`. Each frame `0x0043B145`–`0x0043B156` compares the current
  health with it and does nothing while they match.
- **Stage 1, health 30 down to 20.** A counted hit plays a voice and calls
  `0x0041DC20(rec, 3, 4)` at `0x0043B1BD`–`0x0043B1C6`, which sets `+0x44` =
  3, the hurt animation. While `+0x44` is 3, `0x0043B15C`–`0x0043B163` jumps
  to `0x0043B347` and writes the remembered health back, undoing any further
  hit. Health ≥ 20 is then remembered (`0x0043B33C`–`0x0043B33F`). When the
  window ends was not traced.
- **Stage 2, below 20.** At `0x0043B1D4`–`0x0043B20B` a hit that would leave
  him below 0x14 switches his program counter to script 28's tail
  (`0x004C8198` + 0x1A, a path run) and clears `+0x5E`. Then
  `0x0043B211`–`0x0043B21E` always restores the remembered health. With −3
  hits that freezes him at 21.
- **Progress only at stops.** `0x0043B224`–`0x0043B242` advances only when
  `+0x5E` equals the next entry of `0x004DC018`: 26, 55, 84, 113, 135, 177,
  216, 268, 297, then −1. `+0x5E` is inferred to be his position along the
  path.
- **Stage 3.** After the ninth stop his program counter moves to the tail's
  `+0x34`. Then `0x0059F660` steps to 0x7000 and the level sets
  `[0x0059A5B0] = 1` (won) at `0x0043B322`, and the bird carries him off
  (`level05\level5cc`, script 13).

Moved to engine 1, the same Hopper died to 10 plain −3 hits.

## Cliffside bird boundary

Confirmed PC evidence, first recorded in EXP-20260914-010 (static, 63 offline
original-PC boundary cases, and a hardware arm):

- Dispatcher case `0x004187AA` reaches thunk `0x004013CA` → `0x00434620`.
- Its activation branch `0x004346A2`–`0x00434707` requires runtime
  X > −1249440 and either X < −114688 or Y > −52026. It also requires a nonzero
  word `0x0059D992`, the idle bird state `0x0059F07C` and a zero next-life word
  `0x0059A5B0`.
- In stored units (runtime ÷ 32) the band is X > −39045, and X < −3584 or
  Y > −1625.8125. The branch has no Z comparison. The state gates belong to
  the rule as much as the band does.
- In hardware a start placed inside the basin triggered the native bird
  phases 0 → 1 → 2, next-life 2 and the original restart.
- Cliffside's spawn row in `0x004DC7E8` + 6×12 holds X, Z and heading
  `(93783, −134554, 3063)`, not XYZ. Flik rests at runtime XYZ
  `(93795, −83609, −134646)`. See
  [[EXP-20260906-005 - Isolated authored terrain and platform spawn]] for the
  table.

## Requirements for moving a creature

- The row brings the model (by type), the script (by script byte, table
  `0x004C83F0`), health, flags and the per-type handler. It does not bring the
  level routine, so a moved boss is an ordinary enemy: no health bar, thrown
  projectiles, voices or win condition.
- Bring the texture pages its faces name, and check its drops against the
  target level's sprite list ([[EXP-20261012-002 - Sprite table census]]).
- Immune donors (health 101) keep the target level's enemies-left count
  `0x0059D99E` above 0, so an all-enemies trigger cannot fire.
- Opcode-11 operands write fixed globals that belong to the home level's
  routine, for example Thumper's `0x0059EF70 = 60`
  ([[EXP-20261018-004 - Creature type handlers and opcode-11 subroutines]]).
- A real boss fight elsewhere needs its level routine ported and bound to the
  new slot, with projectile slots and voices remapped to the target's sound
  bank ([[PC sound banks and per-level audio routing]]).
