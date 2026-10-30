---
type: experiment
id: EXP-20261018-003
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static disassembly (capstone) of the retail interpreter tail 0x0041E147–0x0041E845 and its callees, checked against the moved taxi bug's saved slot records from EXP-20261005-002 (EXE c3d8b207…, interpreter byte-identical to retail per EXP-20261018-002); no game launch
question: What do the five modes chosen after a blocking script opcode do, and so how does a creature move?
result: Mode 1 steers toward the target with jitter and accelerates to source +0x1B << 4. Mode 2 does the same until within source +0x14 << 4, then resumes the script. Modes 3 and 4 wait until a ground creature lands. A chase bit makes the target Flik while he is within source +0x16 << 4 of home. Every mode applies friction, a leash at +0x16 << 4, gravity or flight easing, and animation. The taxi bug's samples match the speed cap, arrival radius and landing
status: complete-bounded
created: 2026-10-18
updated: 2026-10-29
evidence: [EXP-20260816-172, EXP-20261018-001, EXP-20261018-002, EXP-20261012-004, EXP-20261005-002]
tags: [experiment/static, re/creatures]
---

# EXP-20261018-003 - Creature VM movement modes

## Question

[[EXP-20260816-172 - PC creature actor pool and behaviour VM census]] read the
interpreter `0x0041DC60` through `0x0041E1A8`. It left the rest of the
function, where the modes act, unanalysed. That gap is the remaining scope
of KU-068 ([[Known Unknowns#Creature rows and the script VM]]), and the part
a boss port needs.

## Method

- **Disassembly.** `0x0041E147`–`0x0041E845` was disassembled in full with
  capstone and read instruction by instruction. All the callees were
  already identified:
  - `0x00464D40`: heading toward a target, masked to 4095 (thunk
    `0x00401271`; KU-072);
  - `0x0041A550`: the speech-idle query (`0x004010C3`;
    EXP-20260910-009);
  - `0x00403A10`: the HUD face frame (`0x00401D61`;
    [[FUNC-97C95BA5572D-00403A10]]);
  - `0x004ABE00`: the ground query (`0x00401721`);
  - `0x0042AA50`: the drop/effect allocator (`0x00401A9B`;
    EXP-20261001-006).
- **Runtime check.** The moved taxi bug's saved slot records were compared
  with the decoded rules by
  `research/creature-rows/script-counter-samples.py` (the `motion` block of
  `reports/creatures/EXP-20261018-002.json`).

## The frame tail

The interpreter's prologue (`0x0041DC82`–`0x0041DCC9`) loads five source
parameters. The tail uses them as follows.

| Source field | Kept as | Used for |
|---|---|---|
| `+0x14` word | `<< 4` | op 3's wander radius; mode 2's arrival radius (`0x0041E1D7`–`0x0041E1DE`) |
| `+0x16` word | `<< 4` | chase range and leash radius around home `+0x28/+0x30` |
| `+0x18` byte | as is (16 while `+0x6C > 0`) | sideways friction per frame |
| `+0x19` byte | as is (16 while `+0x6C > 0`) | forward friction per frame |
| `+0x1A` byte | as is | acceleration (plus forward friction) |
| `+0x1B` byte | `<< 4` | top speed; op 15 rewrites it |

Distances are taken in world units shifted right 5.

### Mode selection (EXP-172 §5.3)

| Mode | Blocking opcodes | Extra |
|---:|---|---|
| 0 | 0, 7, any non-blocking | none |
| 1 | 5, 17 | none |
| 2 | 9, 18 | none |
| 3 | 20 | `+0x60 = 10`, `+0x50 = 0x80000000` |
| 4 | 6 | `+0x60 = 10` |

The tail runs every frame for an active slot. While the wait counter `+0x60`
holds, the interpreter skips the program (`0x0041DCD8`) but still selects
the mode from the pending opcode.

### Mode 2: go to the target

`0x0041E1A8`–`0x0041E1F0`:

- The mode becomes 1 for the rest of the frame.
- **Arrived** (the XZ distance from position to target `+0x34/+0x3C` is
  below the `+0x14` radius): the program counter steps past the blocking
  opcode (`+2`, `0x0041E1EB`) and `+0x60 = 0`, so the script resumes next
  frame.
- **Not arrived:** `+0x60 = 10`.

### Chase

`0x0041E1F4`–`0x0041E314`. The chase applies when all of these hold:

- flag bit `0x0002` is set;
- the mode is below 3;
- word `0x0059DD80` is 0;
- Flik (`0x0059D910`/`0x0059D918`) is within the `+0x16` range of home.

Its effects:

- **Target:** this frame's steering target becomes Flik's X and Z. A local
  copy is used; the record's target is unchanged.
- **Pending op 17 or 18:** if the creature is within 200 of Flik, the
  program counter jumps 6 bytes and `+0x60 = 0`.
- **Otherwise:** the target Y becomes Flik's Y − `0x800` when he is within
  `0x10000` vertically, else home Y, and `+0x60` grows by 1.
- **Then:** the mode becomes 1. If `0x0041A550` reports no speech, it calls
  `0x00403A10(7, 0x1E)`, or refreshes the face timer `0x0059D9B7` to `0x1E`
  when frame 7 already shows. That is the HUD face reacting, the "frame 7 on
  a creature event" of [[FUNC-97C95BA5572D-00403A10]].

The initializer clears bit `0x0002` at `0x0041BE7B` when all of these hold:

- source `+0x11` is 100;
- byte `0x00599B20[type*5 + equipped berry]` is above 99;
- the type is not 15.

That table's meaning is open ([[FUNC-97C95BA5572D-0041BD10]]).

### Every mode: friction, steering, speed

1. **Friction** (`0x0041E31B`–`0x0041E3D3`). The velocity `+0x1C/+0x24` is
   split into sideways and forward parts along the heading `+0x14`, using
   the sine table `0x004C2100` (amplitude `0x4000`). Each part decays toward
   0 by its friction.
2. **Mode 1 only** (`0x0041E3E8`–`0x0041E479`):
   - **Steering**, unless flag `0x0400` is set. The turn is
     `heading(0x00464D40) + rand byte − heading + 0x780`, wrapped to ±`0x800`.
     That is the bearing to the target with jitter of about ±128. It is
     added `>> 3`, or `>> 4` with flag `0x0100`. The random byte comes from
     the shared `rand.dat` cursor `0x00599C60`.
   - **Speed:** below the top speed, forward speed grows by `+0x1A` plus
     the forward friction.
3. **Spin.** `+0x4A > 0` adds `+0x4A << 4` to the heading each frame.
4. **Move.** The heading is masked to 12 bits, the velocity rebuilt, and X/Z
   integrated (`0x0041E494`–`0x0041E516`).
5. **Leash** (`0x0041E519`–`0x0041E580`). Beyond the `+0x16` radius from
   home, the position is put back on that circle along the bearing from
   home. This is EXP-20261005-002's "wanders around home".
   - Op 4 copies the old target into home (`0x0041DE09`–`0x0041DE12`), so a
     path walker is leashed to its previous waypoint.
   - It can therefore only progress along segments shorter than the leash
     plus the arrival radius. Every shipped list, and the list 1 of
     EXP-20261005-002's derived test level, meet that for the taxi bug's
     304 + 304: their longest segments are 451 and 561.

### Every mode: height

- **Flag `0x0004` (flying),** `0x0041E591`–`0x0041E639`:
  - Y eases a 32nd of the way toward the target Y each frame.
  - A ground query with a per-type offset `word [0x004C87C6 + type*2]`
    keeps it above ground, rising at most `0x800` a frame.
- **Otherwise,** `0x0041E63E`–`0x0041E6B6`:
  - gravity adds `0x100` to `+0x20` (at most `0x1000`);
  - the ground query snaps Y;
  - flag `0x2000` uses target Y after the query instead.
- **Landing** (`0x0041E6B9`, `0x0041E7D4`–`0x0041E7FE`). Within `0x200` of
  the ground, Y eases down and `+0x20 = 0`.
  - In modes 3 and 4 that ends the wait: `+0x70 += 2`, `+0x60 = 0`.
  - Mode 3 also keeps waiting while `+0x20` is negative (rising) and
    records the ground in `+0x50`. What makes `+0x20` negative is not in
    this function.
- **Skid effect.** When sideways speed exceeds forward speed, or forward
  speed is negative, and source `+0x1B` is nonzero, `0x0042AA50` is called
  with the position and `(1, 1)`.

### Every mode: animation and the type handler

`0x0041E6E6`–`0x0041E7C7`:

- **Rate byte.** The rate comes from `+0x48` when the landing block ran this
  frame, else from `+0x49`. Op 22 sets both.
  - A positive byte gives a rate of byte × forward speed × 2 (at most
    `0x10000`).
  - A negative byte gives a fixed rate: −byte `<< 10`.
- **Frames.** The 16.16 phase `+0x40` advances. Each whole step moves the
  frame pointer `+0x4C`.
  - Byte `0xFF` loops back by the next byte.
  - Bytes `0x80` and above set `+0x7A = 0x100 − byte` and are skipped.
- **Handler.** The per-type handler `+0x7C` is then called. It gets the
  frame byte, the moving and landed bits, the record, and the sideways and
  forward speeds (EXP-172 §5.5).

## Runtime check: the moved taxi bug

Retail City Entrance slot 0 has:

- `+0x14 = 19`: arrival radius 304;
- `+0x16 = 19`;
- `+0x18 = 64`, `+0x19 = 16`, `+0x1A = 32`;
- `+0x1B = 64`: top speed 1024.

Its 53 live samples in the tough-regulars arm (EXE `c3d8b207…`):

| Prediction | Observed |
|---|---|
| Speed held at the cap: below 1024 it gains 48 (`+0x1A + +0x19`) | 1024–1070 |
| A ground creature lands every frame: `+0x20 = 0` | 0 in all 53 |
| At op 9 the distance was at least 304 when checked, so the sample (after at most 33.4 of travel) is at least 270 | 275–646 |
| At op 9 + 2 it arrived, so the sample is under 304 | 242–259 |
| Home is the previous list row (op 4's copy) | 53 of 53 |
| The leash keeps it within 304 of home | at most 230 |

The taxi bug's flag `0x0002` is set (`0x8042`). These samples were not
examined for a chase: the chase target is a local copy that the record does
not keep.

## Confirmed, inferred, unknown

- **Confirmed (static).** The mode semantics above, at their instruction
  addresses.
- **Confirmed (static plus runtime, one creature).** These match the saved
  samples:
  - the top speed `+0x1B << 4`;
  - the arrival radius `+0x14 << 4` that releases op 9;
  - grounding with `+0x20 = 0`;
  - home following the path and the leash around it.
- **Inferred.**
  - The roles "friction", "acceleration" and "leash" describe what the
    arithmetic does.
  - The HUD face reaction to a chase is the frame-7 call; nobody has seen it
    in game for this reason.
- **Unknown.**
  - What `0x0059DD80` is. It has eight absolute references (seven reads and
    one pointer comparison) and no direct writer was found.
  - What drives `+0x20` negative for mode 3.
  - The meaning of `0x00599B20[type*5 + berry]` in the chase gate.
  - What the ten per-type handlers do with the record they get.

## Consequences

- **KU-068's remaining scope narrows** to the per-type handlers and the
  undriven inputs above.
- **For a boss port.** The script VM gives a moved boss only these
  behaviours: wander, path, chase while Flik is near home, and wait to land.
  The fights in EXP-20261005-002's list are level routines writing `+0x70`
  and `+0x5E` from outside, as the Canyon Showdown routine does.
