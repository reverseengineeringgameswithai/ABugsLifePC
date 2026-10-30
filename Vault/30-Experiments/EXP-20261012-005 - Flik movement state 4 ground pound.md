---
type: experiment
id: EXP-20261012-005
date: 2026-10-12
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static only. Raw capstone decoding of the player controller 0x0043F9E0 and its helper thunks, plus the existing Ghidra export, over retail bugs.exe; no game launch or memory access
question: Is Flik's movement state 4 (0x0059D990) a glide, as EXP-20260930-004 labelled it, or a hover, dive and ground pound, as the Flik animation catalogue reads it?
result: Hover, dive and pound. State 4 starts only from falling state 2, more than 0x2000 above the floor. Vertical speed is held at 0 while a countdown runs, then set to the maximum 0x1000. Landing sets action 0xC and a negative cooldown, fires 8 radial shots through 0x0042B020, spawns drop type 0x5B and plays event 0x10. No reduced-fall glide exists in this state
status: complete-bounded
created: 2026-10-12
updated: 2026-10-12
evidence: [EXP-20261001-002, EXP-20260930-004]
tags: [experiment/static, re/player]
---

# EXP-20261012-005 - Flik movement state 4 ground pound

## Question

Section 5.2 of [[Next Tasks]]. Two notes disagree on movement state 4:

- EXP-20260930-004 calls it "gliding";
- [[PC Flik animation catalog]] reads it as a hover, then a dive, then a
  ground pound.

## Evidence

All of the following comes from raw decoding of the player controller
`0x0043F9E0`, on Flik's record `0x0059D910` (`esi`):

| Offset | Address | Meaning |
|---|---|---|
| `+0x30` | `0x0059D940` | Vertical speed |
| `+0x80` | `0x0059D990` | Movement state |
| `+0x84` | `0x0059D994` | Countdown |
| `+0x88` | `0x0059D998` | Action state |

The code runs in three stages.

1. **Entry (`0x00440245`–`0x00440293`).**
   - It runs only when the movement state is 2 (falling) and Flik is more
     than `0x2000` above the floor (`+0x48` − `+0x04` > `0x2000`).
   - It calls event `0x004148A0(0x1B, 0)` through thunk `0x004017E4`, sets
     the countdown from `bx`, and sets **state 4**.
   - The action becomes 7 if vertical speed exceeds `0x100`, otherwise 2.
     That matches the catalogue's row: "Shift again while falling more than
     `0x2000` up".
2. **Hover, then dive (`0x0044033C`–`0x00440373`).**
   - While the countdown is above 1, it decrements and vertical speed stays
     **0**.
   - At 1, vertical speed becomes **`0x1000`**, the cap the normal fall path
     also enforces (`0x0044032A`).
   - A negative countdown recovers by `+0x200` per frame.
3. **Landing (`0x00440390`–`0x00440419`).**
   - The countdown becomes `0xE800` (−`0x1800`, so 12 frames to recover).
   - Speed becomes 0, action `+0x7A` becomes `0xC`, and the state becomes 1.
   - A loop over the angle table `0x004C2100` in steps of `0x400` calls
     `0x0042B020` (thunk `0x00401E60`) **8 times**, once per heading, with
     arguments `(x, y, z, cos>>4, 0, sin>>4, −0x10, 0xF)`.
   - It calls `0x0042AA50` (thunk `0x00401A9B`) for drop type **`0x5B`**,
     motion 3, at `y − 0x1000`.
   - It plays event `0x004148A0(0x10, 0)`.

## Confirmed, inferred, unknown

- **Confirmed (static).** State 4 holds Flik still in the air, then drops him
  at full speed. On landing it emits a ring of 8 radial shots through the
  same allocator berry shots use (`0x0042B020`, [[EXP-20261012-004 - Homing target visibility bit]]),
  plus a type-`0x5B` effect and a sound. No part of the state slows a fall,
  so "gliding" is a mislabel.
- **Inferred.**
  - The ring is a shockwave. Whether those shots damage enemies depends on
    their type and flags in `0x0042B020`, which were not traced.
  - The countdown's start value comes from `bx`, set earlier in the
    controller and not traced, so the hover length is unknown.
- **Unknown.**
  - The hover length.
  - What drop `0x5B` looks like.
  - Whether the ring hurts enemies.
  - Event sounds `0x1B` and `0x10`.

The catalogue's planned read-only Training arm, which reads `0x0059D990`,
`0x0059D994` and `0x0059D940` through a second Shift press, would settle the
first and third.
