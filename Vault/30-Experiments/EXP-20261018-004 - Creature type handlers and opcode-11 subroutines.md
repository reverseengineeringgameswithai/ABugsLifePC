---
type: experiment
id: EXP-20261018-004
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static disassembly (capstone) of retail bugs.exe, raw reference scans, and the creature census of EXP-20261018-001 for which rows run which script; no game launch
question: What do the ten per-type handlers (record +0x7C) and the nine opcode-11 subroutines do, the last unread parts of creature behaviour?
result: The handlers are small. Most play an event (0x004148A0) on chosen animation frames or every frame, and the events now have file names (WASPBUZZ, ERUPTION, THROW01, SPIDER01 and others). The badbug/weevil handler pins a buried creature at its spawn with dust. The long-legged spider fires kind-0x7A shots toward Flik every 40–103 frames. The mosquito dashes, and the "protect" type turns to face Flik. Opcode 11's subroutines are emerge and burrow actions (bursts, jumps, hittable and chase bits), a wasp's eight-way ring, and level hooks for Tunnels, Thumper, Canyon Showdown, Anthill Pt 2 and Mr. Soil's sign
status: complete-bounded
created: 2026-10-18
updated: 2026-10-29
evidence: [EXP-20260816-172, EXP-20261018-001, EXP-20261018-003, EXP-20261012-002, EXP-20260910-008, EXP-20261005-002]
tags: [experiment/static, re/creatures]
---

# EXP-20261018-004 - Creature type handlers and opcode-11 subroutines

## Question

[[EXP-20261018-003 - Creature VM movement modes]] read the interpreter's
tail. Two pieces of creature behaviour remained unread
([[Known Unknowns#Creature rows and the script VM]]):

- the ten per-type handlers that the builder installs in `+0x7C` and the
  tail calls each frame (`0x0041E7C7`);
- the nine subroutines behind opcode 11 (EXP-172 §5.4).

Creature identities follow
[[EXP-20261012-006 - Creature types from the character loader]].

## Method

- **Disassembly.** Each function was disassembled with capstone from its
  entry to its `ret`. Thunks were resolved by their `jmp`, and globals
  checked with a raw scan of absolute references.
- **Usage.** Which scripts use which opcode-11 operand comes from decoding
  the 40 programs. Which rows run those scripts comes from
  `reports/creatures/EXP-20261018-001.json`, counting only rows whose VM
  runs.
- **Calls.**
  - `0x004148A0` (thunk `0x004017E4`) is the event call. For id ≥ 0 it
    reads a 16-byte entry at `0x004C6E08 + id*16`; for id < 0 it queues a
    positional script from `0x004C6DC8`. Flik's code uses it for sounds
    (EXP-20261012-005), so ids are reported as event ids, not sound names.
  - `0x0042B020` (thunk `0x00401E60`) is the projectile allocator; its
    arguments are XYZ, velocity, one word and a kind.
  - `0x0042AA50` (thunk `0x00401A9B`) is the drop allocator.
  - Both read the 20-byte kind table `0x004D64C4`, whose field 0 is the
    sprite entry.

## The handler call

The tail passes a pointer to a stack record (`0x0041E7A5`–`0x0041E7C2`):

| Offset | Content |
|---|---|
| `+0` | the frame byte just reached, or −1 when the animation did not step |
| `+2` | bit 0 "steering this frame", bit 1 "landed this frame" |
| `+4` | the pool record |
| `+8` | sideways speed |
| `+0xA` | forward speed |

`+0x44` below is the animation group that op 13 sets. Every handler returns
0, and the tail ignores the return value.

## Per-type handlers

| Handler | Types | Behaviour |
|---|---|---|
| `0x0041BEF0` | 9 badbug, 37 weevil | Event 7 on frame 0. While `+0x48` is 0, pins the creature at its source XYZ and spawns drop `0x59` (sprite 1) `0x3200` up, at one random offset of up to ±`0x2000` added to both X and Z. Leans `+0x18` toward ±`0x80` while sideways speed exceeds forward speed, else lets it decay |
| `0x0041C050` | 15 green grasshopper | In group 0, event `0x26` on frames 10 and 22; in group 1, event `0x1A` every frame |
| `0x0041C0C0` | 29 Molt | In group 0, event `0x26` on frames 1 and 10 |
| `0x0041C100` | 16 Thumper, 22 Hopper, 36 Thud | Event `0x1A` every frame |
| `0x0041C130` | 31 acorn | Event `0x7D` every frame |
| `0x0041C160` | 6 fly, 13 wasp | Event `0x28` every frame while the group is below 2 |
| `0x0041C190` | 10 mosquito | Event `0x2A` every frame in group 1. When flag `0x1000` is set it clears it; in group 1 it also doubles the velocity and sets `+0x6C = 25`, which holds both frictions at 16 for 25 frames: a dash |
| `0x0041C210` | 34 dragonfly | Event `0x2A` every frame |
| `0x0041C240` | 39 "protect" | Turns a 16th of the way toward Flik each frame (bearing from `0x00464D40`) |
| `0x0041C2C0` | 17 long-legged spider | See below |

**The spider's shot** (`0x0041C2C0`–`0x0041C3B9`) runs only while `+0x4A`
is 0, the hurt counter.

1. It counts source `+0x0F` down. At 0 it reloads it with
   `(rand & 0x3F) + 0x28`: 40 to 103 frames.
2. It takes the bearing to Flik. If that is within ±`0x100` of its heading
   it aims there, otherwise straight ahead.
3. It fires one projectile:
   `0x0042B020(x, y − 0x4000, z, sin >> 3, −0x100, cos >> 3, 0x10, 0x7A)`.
4. It plays event `0x19`.

Kind `0x7A` draws sprite entry 118.

## Opcode 11's subroutines

| Operand | Subroutine | Script (rows that run it) | Behaviour |
|---:|---|---|---|
| 1 | `0x004288F0` | 1 (badbug, weevil) | **Emerge.** 8 drops `0x15`–`0x17` (sprites 5, 6) at `0x1CC0` up; `+0x20 = −0xC00` (a jump); event `0x18`; sets chase bit `0x02` unless `0x00599B20[type*5 + berry]` exceeds 99; clears `0x80` (now hittable) |
| 7 | `0x00428A60` | 1 (badbug, weevil) | **Burrow.** Clears `0x02`, sets `0x80` (unhittable), `+0x50 = (Y − 0x4000) & ~1` |
| 8 | `0x00428990` | 37, 38 (bad worm, centipede) | **Emerge.** 8 drops `0x15`–`0x17` at the creature; event `0x18`; type 40 also turns to face Flik |
| 2 | `0x004287D0` | 2, 5 (wasp) | **Ring.** 8 projectiles of kind `0x1E` (sprite 1), one per eighth of a turn; `+0x20 = −0xC00`; event `0x14` |
| 3 | `0x00432A50` | 8 (Tunnels grasshopper) | Faces Flik from home; `+0x50 = Y \| 1`. Once per group (source `+0x0F` indexes the latch words at `0x0059EF90`, a Tunnels routine array cleared at `0x0043282D`): widens the activation radius `+0x6A` by `0x960`, 8 drops `0x15`–`0x17`, `+0x20 = −0x800`, event `0x66` |
| 4 | `0x00431C90` | 9 (Thumper) | Sets `0x0059EF70 = 60`, a timer of the Council Chamber routine: init sets 1000 (`0x00431C24`), and `0x004320B5`–`0x0043211B` counts it down and re-arms it |
| 5 | `0x0043ADD0` | 28 (Canyon Showdown Hopper) | Condition: the Hopper's cursor `0x0059BB2A` is not yet the next stop in `0x004DC018` (EXP-20261005-002) |
| 6 | `0x00436AF0` | 33 (Tuck, Roll) | Through the type's descriptor `[0x005B18E0 + type*4]`, sets `+0x2E = 1` on 21 consecutive `0x50`-byte part entries at `0x005A9660` and clears the 22nd |
| 9 | `0x0043C250` | 39 (Mr. Soil) | Mr. Soil's sign frames from stage `0x0059F6B8` ([[EXP-20260910-008 - Replaceable Soil sign images]]) |

Subroutines 1, 2 and 3 are the writers that make `+0x20` negative, which
mode 3 waits out ([[EXP-20261018-003 - Creature VM movement modes]]).

## What the events play

`research/creature-rows/creature-events.py` writes
`reports/creatures/EXP-20261018-004.json`.

- **The entry.** An event entry's first word `s` selects the sample:
  - **`s > 0`:** sample `s`, one-shot. `0x00414A42` passes `s − 1`, and
    `0x00419966` adds 1 back.
  - **`s < 0`:** sample `−s` on a keyed channel. `0x00414A52` passes
    `−1 − s`, and `0x00419BEB` adds 1. The entry's `+2` word is the key and
    the pitch base. A repeat call for the same key reuses its slot in the
    channel table `0x00572C88`, slews the pitch by `0x40` and replays, so
    every-frame calls keep one sound going per key.
- **Same id space.** The loader `0x0049DF90` stores sample `s` at
  `0x007EDF08 + s*24`, and the player `0x0049D820` reads that slot. So `s`
  is the bank `sample_id` of EXP-20260910-004's
  native census, and ids 1–66 name the same files in every level's bank.

| Event | Played by | Sample | File | `+2` |
|---|---|---:|---|---:|
| `0x07` | badbug/weevil, frame 0 | 28 | `SPIDER01.WAV` | 4800 |
| `0x14` | wasp ring | 27 | `SEEDROLL.WAV` | 5600 |
| `0x18` | emerge (subroutines 1, 8) | 11 | `ERUPTION.WAV` | 4800 |
| `0x19` | spider shot | 29 | `THROW01.WAV` | 4000 |
| `0x1A` | Thumper, Hopper, Thud; grasshopper group 1 | 31, keyed | `WASPBUZZ.WAV` | 1136 |
| `0x26` | grasshopper and Molt footsteps | 2 | `BOULDER.WAV` | 4000 |
| `0x28` | fly, wasp | 31, keyed | `WASPBUZZ.WAV` | 4096 |
| `0x2A` | mosquito, dragonfly | 31, keyed | `WASPBUZZ.WAV` | 6000 |
| `0x66` | Tunnels grasshopper burst | 7 | `CANNPLNT.WAV` | 3200 |
| `0x7D` | acorn | 9, keyed | `DANDLION.WAV` | 400 |

**Two forms agree.** The file names match the readings above, reached
independently from the code:

- the emerge event plays `ERUPTION.WAV`;
- the spider's shot plays `THROW01.WAV`;
- the flyers' every-frame events share one buzz, `WASPBUZZ.WAV`, at three
  pitches;
- the type-9 footstep plays `SPIDER01.WAV`, matching the earlier
  appearance label "spider" for `chars\badbug`.

**A data point, not a decision.** The acorn (type 31) holds
`DANDLION.WAV` on a keyed channel at pitch 400. EXP-20261012-006 recorded
the opposite hints: "flytrap plant" for 31 and "dandelion seed" for 37.
This sound bears on that contradiction but does not settle it.

## Confirmed, inferred, unknown

- **Confirmed (static).** Each behaviour above, at its addresses, and which
  rows reach each subroutine. Subroutine 9 matches the earlier Soil sign
  analysis, which ran it natively.
- **Confirmed (static, with EXP-20260910-004's native census).** Each
  creature event's sample file.
- **Inferred.**
  - The readings "emerge", "burrow", "dash", "shot", "ring" and "dust"
    describe the arithmetic and the effects. No arm has filmed them.
  - Events on fixed frames are likely footsteps; every-frame events are
    likely loops, since `0x004148A0` gets the position each time.
- **Unknown.**
  - The meaning of the event entry's fields after `+2`: volume and the
    shake maxima at `+0xA`/`+0xC` are inferred from where they are stored.
  - What sets mosquito flag `0x1000`.
  - What the 21 part entries of subroutine 6 control. The table is the
    shared part pose table (`0x005A9660`, [[PC Flik animation catalog]]).
  - Whether the kind-`0x7A` shot hurts Flik.

## Consequences

- **Moved creatures and sprites.**
  [[EXP-20261012-002 - Sprite table census]]'s extension
  listed what scripts and generic routines spawn. The handlers add kind
  `0x7A` (sprite 118, which the shared setter `0x00456860` fills in every
  engine with a nonzero index) and drop `0x59` (sprite 1). Its conclusion,
  that a moved creature draws no missing sprite, still holds.
- **Moved spiders shoot.** A long-legged spider moved to another level keeps
  its type handler, so it should shoot there while on screen (its `+0x11` is
  100). The `tough-regulars` image of EXP-20261005-002 moved one, and that
  experiment did not report shots.
- **Creature behaviour is now read end to end:**
  - the builder ([[EXP-20260816-172 - PC creature actor pool and behaviour VM census]]);
  - the gate and lists ([[EXP-20261018-001 - Creature row index census]]);
  - the program counter ([[EXP-20261018-002 - Creature script counter in saved runtime samples]]);
  - movement ([[EXP-20261018-003 - Creature VM movement modes]]);
  - the handlers and subroutines (here).

  What remains are the level routines.
