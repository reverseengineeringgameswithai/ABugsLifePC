---
type: research
status: confirmed-bounded
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence:
  - EXP-20261001-002
  - FUNC-97C95BA5572D-00402DC0
  - FUNC-97C95BA5572D-00445FF0
  - FMT-PC-ANM-FIRST-LEVEL
created: 2026-10-01
updated: 2026-10-18
tags: [re/animation, re/gameplay, re/resources]
---

# PC Flik animation catalog

The reference for every animation Flik has on PC and what makes each one play.
Static evidence only: retail executable `97c95ba5…` (decompiler plus fresh
disassembly) and the retail `.ANM` files. No runtime arm has confirmed a state
number yet ([[EXP-20261001-002 - Flik animation catalog]]).

- **Machine-readable:** `reports/animation/flik-animation-catalog.json` (every
  slot, state, frame script, footstep event, variant and label) and the
  generated tables in `reports/animation/flik-animation-catalog.md`.
- **Labels:** `config/animation/pc-flik-animations.json`. Each row has its own
  `status` and `evidence`; edit labels there, never in the reports.
- **Regenerate:** `.venv/bin/python scripts/flik-animation-catalog.py`
  (`--check` fails when the reports are stale). It reads only
  `work/copies/BUGS_PC-full-disc`, refuses `originals/`, and writes metadata,
  never pose data.
- **Parser:** `reimplementation/ablpc/anm.py` `AnmFile.records()` reads every
  keyframe of any retail `.ANM`; `reimplementation/ablpc/flik_animation.py`
  reads the state table.

## At a glance

- Flik's player animations live in one file per model: `CHARS/FLICK.ANM` has
  **40 slots, 39 present** (slot 26 is empty). Every slot drives **24 body
  parts**; frame counts run from 8 to 58.
- The game never picks a slot directly. Flik's **action state**
  `0x0059D998` (35 values, `0x00`–`0x22`) indexes a table at `0x004C1CE8`
  that names one or two slots, a frame script, a playback speed and an
  idle-family flag ([[#How it works]]).
- **Coverage is complete.** The executable has exactly four calls to the pose
  sampler `0x00445FF0`; only `0x00402DC0` plays Flik's player file, and every
  slot it can reach is listed below. Slots **7 and 12** exist but nothing
  references them; state **`0x20`** names the empty slot 26 and nothing ever
  sets it. The entity path plays the two non-player Flik models, also listed.
- **Riverbed Flight is the exception on screen:** there Flik is hidden and the
  ATTAFLIK model is drawn in his place ([[#ATTAFLIK — the player in Riverbed Flight]]).
- All four player models share the slots and frame counts
  ([[#Player models per level]]). Two more models contain Flik and are
  animated as entities: ATTAFLIK and the FLIKHARV harvester
  ([[#Non-player Flik models]]).

## Quick reference

Keys are the defaults written at `0x0042F100` ([[#Controls]]). "Upd" is one
game update; the game is capped at 30 updates per second, so 30 upd ≈ 1 s.
Status applies to the gameplay name; triggers are read from code.

### Moving

| What Flik does | State | Slot(s) | Frames, timing | Trigger | Status |
|---|---|---|---|---|---|
| Run | `0x00` | 0 upper + 1 lower | 17; loops 16 steps, speed scales with ground speed | Arrow keys on the ground, hands empty | confirmed |
| Walk | `0x1D` | 33 | 24; speed scales with ground speed | Space held while moving (target speed `0x300` not `0x700`) | confirmed |
| Turn in place left / right | `0x14` / `0x15` | 24 / 25 | 8 each, half speed | C held with Left / Right (heading ±`0x20` per upd) | confirmed |
| Stand still | `0x16` | 4 | 12, half speed loop | No input | confirmed |

Run, walk and the turns place footstep dust and sounds on fixed script
steps (run: steps 2 and 10; walk: 5 and 17; turns: 3 and 7).

### Jumping and air

| What Flik does | State | Slot(s) | Frames, timing | Trigger | Status |
|---|---|---|---|---|---|
| Jump / launched upward | `0x03` | 5 upper + 6 lower | frames 0–5, holds 5 | Shift, or any bounce/launch (mushroom, enemy stomp, plant growth, level bumpers) | confirmed |
| Falling | `0x04` | 5 + 6 | frames 6–11, holds 11 | Vertical velocity turns positive | confirmed |
| Landing | `0x05` | 5 + 6 | frames 12–17, then ends | Ground contact returns; landing sound 3 except Riverbed Flight | confirmed |
| Hover then dive | `0x02` (`0x07` if falling fast) | 3 | 12, holds the last frame | Shift again while falling more than `0x2000` up | candidate |
| Pound impact | `0x1C` | 34 | 12, half speed | Landing from the dive (ring of particles, sound `0x10`) | candidate |
| Pound recovery | `0x06` | 10 | 12 | The 11 updates after the impact | candidate |
| Slow fall | `0x12` | 16 | 12 | Touching a type-8 plant top, or holding an uprooted propeller high up | confirmed |
| Propeller updraft | `0x0D` | 15 | 12 | Rising in a grown propeller's updraft | confirmed |
| Swing on a strand | — | 32 | 24; frame follows the swing, not time | Airborne within reach of a hanging strand's node: the grab is automatic (`0x004A5B83`, `0x0059D99C`) | confirmed |

### Throwing, carrying and plants

| What Flik does | State | Slot(s) | Frames, timing | Trigger | Status |
|---|---|---|---|---|---|
| Berry throw while moving or jumping | overlay | 2 (layer A) | 18 upd; berry leaves near frame 8 | Ctrl | confirmed |
| Berry throw standing | overlay | 11 | 18 upd | Ctrl while idle | confirmed |
| Berry throw in a slow fall | overlay | 23 | 18 upd | Ctrl in state `0x12` (not with a propeller) | confirmed |
| Pick up a seed / uproot a plant | `0x09` | 8 | 17, holds the last frame | Ctrl beside a seed or grown plant | confirmed |
| Carry, standing | `0x0C` | 17 | 8, each frame twice | Object in hand | confirmed |
| Carry, walking | `0x0B` | 14 | 24, speed scales; steps 5 and 17 | Object in hand, moving | confirmed |
| Throw the carried object | `0x0E` | 18 | 8, then ends | Ctrl while carrying a plant or a light seed | confirmed |
| Hang from a heavy seed | `0x10` | 20 | 18; frames 12–17 repeat | Ctrl on a seed in seed-state ≥ 3 | candidate |
| Let go of the seed | `0x11` | 21 | 12 | Ctrl again while hanging | confirmed |

### Damage, enemies and death

| What Flik does | State | Slot(s) | Frames, timing | Trigger | Status |
|---|---|---|---|---|---|
| Hurt recoil | `0x08` | 9 | about 12 upd | A non-fatal hit (invulnerability `0x2D` > `0x21`) | confirmed |
| Tired idle, no hits left | `0x1F` | 39 | 12 at one-third speed; sound `0x50` repeats | Health `0x0059D9A4` = 0 while standing | candidate |
| Death | `0x0F` | 19 | 16 at one-third speed, freezes on 15 | Health underflow, or the bird | confirmed |
| Shove a stunned enemy | `0x1E` | 36 | 8, then ends | Touching a faced enemy while carrying or during the Z move | confirmed |
| Z move | `0x01` | 35 | 16, holds the last frame | Z (or Space+Ctrl) on the ground, hands empty; repels enemies for 16 upd | candidate |

### Idle fidgets

While standing, each pass through idle frame 11 has a 1-in-4 chance to start a
random fidget from the level's table. Each fidget plays once, then idle resumes.

| State | Slot | Frames | Speed | In tables |
|---|---|---|---|---|
| `0x17` | 29 | 36 | 1 | all three |
| `0x18` | 30 | 32 | ½ | default, Cliffside group |
| `0x19` | 27 | 48 | 1 | all three |
| `0x1A` | 28 | 48 | 1 | all three |
| `0x1B` | 31 | 24 | 1 | default, Cliffside group |
| `0x21` | 37 | 58 | 1 | default, Cliffside group |
| `0x22` | 38 | 36 | 1 | Cliffside group, City group |

Tables: default `0x004C1FA8`; Cliffside, Riverbed Canyon, Bird Nest and Canyon
Showdown use `0x004C1FB8`; City Entrance and City Square use `0x004C1FC8`.
Duplicates in a table weight the pick. In Bug Bar (index 14), idle-family and
turn states are replaced by state 0 at full speed (`0x00403137`,
`0x00403237`); how that looks in play is unverified.

### Level-specific

| What Flik does | State | Slot | Frames | Trigger | Status |
|---|---|---|---|---|---|
| Carried off by the bird | `0x13` | 22 | 12, loops until death | Cliffside bird hazard (`0x00434620`) | confirmed |
| Bounce off an Anthill Pt 2 actor | `0x0A` | 13 | 8 | Landing from more than `0x1000` up on actor slot 2 or 3 | confirmed (actor unidentified) |

### Unused

| Slot or state | Frames | Finding |
|---|---|---|
| Slot 7 | 24 | No reference anywhere in the executable |
| Slot 12 | 13 | No reference anywhere in the executable |
| Slot 26 / state `0x20` | — | Slot empty in every model; nothing sets state `0x20` |

## How it works

1. **Choosing a state.** Every update `0x00402DC0` picks the action state from
   Flik's record at `0x0059D910` (ground contact, speeds, carry counter,
   timers, input). Other code also sets it directly: the controller
   (`0x0043F9E0`), actor contact (`0x0041C9B0`), plants (`0x00468010`,
   `0x00468BF0`) and level updaters. In the air it only advances 3→4 and
   8→4 before the overrides that apply everywhere (impact timer, hurt, death,
   hanging, slow fall); movement-driven choices are made on the ground.
2. **The table row.** State × 20 bytes at `0x004C1CE8`: frame-script pointer,
   slot A, slot B, speed, idle-family flag (`0x00403181`–`0x0040319C`). 35 rows
   end at a `0xFFFFFFFF` word, followed by the three idle tables.
3. **Frame scripts.** One byte per step: the low seven bits are the ANM frame.
   `0x82`, `0x83`, `0x85` add left-foot dust and sound 0; `0x87`, `0x8A`,
   `0x91` add right-foot dust and sound 1 (only within `0x400` of the ground).
   `0xFF n` jumps back n steps (a loop, or a hold when n = 1); `0xFE` ends the
   action and the state is chosen again.
4. **Speed.** 16.16 steps per update. Negative values scale with ground speed
   `0x0059D948` (run ×`0x30`, walk and carry ×`0x60`), clamped to one step per
   update. A changed state restarts its script.
5. **Layering.** When slots A and B differ, both are sampled at the same
   frame: A drives parts 9–20 and B parts 0–8, each marking the other's parts
   `-3` (left as the other layer posed them). Calling A the upper body and B
   the legs is inferred: the berry-throw overlay replaces A, and B's part 8
   carries the extra channel.
6. **Berry-throw overlay.** Ctrl sets `0x0059D996` = `0x12`
   (`0x00440541`); the berry leaves when it reaches 10 (`0x00440555`). While it
   counts down, `0x00402DC0` swaps layer A for slot 2 at frame `0x12` minus the
   counter, or slot 11 (idle-family states) or 23 (slot-16 states) for the
   whole body.
7. **Strand swing.** While `0x0059D99C` holds a grabbed strand, slot 32 is
   sampled at a frame from Flik's offset along his heading
   (`0x00403327`–`0x004033D9`), so the pose follows the swing.
8. **Sampling.** `0x00445FF0` writes each driven part's three linear words and
   three 12-bit angles (plus three extra words where the record's bitmask says
   so) into the shared part entries at `0x005A9660`, interpolating toward the
   next frame; the last frame blends back into frame 0.

The record layout is in [[PC ANM first-level#Slot records (2026-10-01)]].

## Controls

Default keyboard bits (`0x0042F100`–`0x0042F1E6`, scan codes through
`0x004D8430`): Up `0x10`, Right `0x20`, Down `0x40`, Left `0x80`, Ctrl
`0x8000` (throw, pick up, release), Shift `0x4000` (jump), Space `0x200`
(walk), Z `0x8200` (Ctrl+Space in one key), C `0x400` (turn in place), Alt
`0x1000`, Return `0x8`, X `0x800`. (2026-10-18: the game's controls screen
labels these "forward", "back", "left", "right", "fire/get/drop",
"jump/change", "walk", "kick" (Z), "camera" (C), "seed color" (Alt) and
"lock camera" (X); Return cannot be rebound. "Turn in place" for C is
right as well: the key also selects camera mode 2, and while it is held
Left/Right turn Flik at `0x0044056D`–`0x0044059A`:
[[EXP-20261018-006 - Controls configuration screen and action bits]].) The right-hand Shift, Ctrl and Alt copy the
left ones; Tab copies C. Bit `0x100` has no default binding.

## Player models per level

`0x00445020` loads one player model as resource ID 0, chosen by level index
`0x00861C84` ([[PC level roster and numbering]]):

| Model | Levels | Parts | Absent slots |
|---|---|---|---|
| `CHARS/FLICK.ANM` | all others, including Training and Anthill | 24 | 26 |
| `CHARS3/FLICKD.ANM` (byte-identical to FLICK) | Council Chamber, Tunnels | 24 | 26 |
| `CHARS4/FLICKP.ANM` | City Entrance, City Square | 29 | 26, 30, 31, 37 |
| `CHARS3/FLICKP.ANM` | Cliffside, Riverbed Canyon, Bird Nest, Bug Bar | 29 | 26 |

Every present slot has the same frame count as FLICK's, so one state table
drives all four. The FLICKP files carry five extra parts. CHARS4's missing
slots are exactly the fidgets its levels' idle table (`0x004C1FC8`) never
picks. The model lists and the idle-table lists do not coincide: Bug Bar uses
FLICKP with the default table, Canyon Showdown FLICK with the Cliffside table.

## Non-player Flik models

Two other models contain Flik. Both are entities: creature-VM opcode `0x0D`
(`0x0041E00D`) or helper `0x0041DC20` sets the slot (actor `+0x44`) and a frame
script from `0x004C8754`, and `0x00448569` samples them. No entity reuses the
player headers (`0x0044515B` zeroes the word that `0x0044846D` tests).

### ATTAFLIK — the player in Riverbed Flight

`CHARS2/ATTAFLIK.ANM` (4 slots, 50 parts: Atta and Flik together) is actor
slot 39 in Riverbed Flight only (`LEVEL08/LEVEL.RAW`). Level handler
`0x004362D0` copies Flik's position and heading into it every update and sets
`0x0059D9A0` bit 0 (`0x0043634A`), which makes Flik's renderer skip him
(`0x0044C51A`). **In that level these are the player's visible animations**;
Flik's own state machine still runs underneath.

| Slot | Frames | What it shows | Trigger | Status |
|---|---|---|---|---|
| 0 | 12 | Flight loop | Default; restored after hurt and throw | candidate name |
| 1 | 28 | Hurt | A fresh hit (invulnerability `0x2C`), returns at frame 27 | confirmed |
| 2 | 18 | Berry throw | Throw counter `0x12` (Ctrl), returns at frame 17 | confirmed |
| 3 | 32 | Death | Health below 0; half rate, holds frame 30 | confirmed |

### FLIKHARV — the rideable harvester

`CHARS3/FLIKHARV.ANM` (3 slots, 31 parts) is actor slot 63, run by the
global hook `0x00415E30`, in Anthill, Tunnels, City Square, Clover Forest,
Riverbed Canyon and The Tree. Ctrl beside it on the ground mounts it
(`0x0059D9A0 |= 0x80`, sound `0x32`, part modes through `0x00446870`);
Shift or a hit dismounts.

| Slot | Frames | What it shows | Trigger | Status |
|---|---|---|---|---|
| 0 | 24 | Ridden, moving | Rate scales with Flik's ground speed (`0x00416038`) | confirmed |
| 1 | 12 | Ridden, standing | One frame per update (`0x00416014`) | confirmed |
| 2 | 6 | Parked | Unoccupied, half rate; after a dismount | confirmed |

Whether Flik's own model is drawn while riding, and what the part-mode change
shows, is unverified.

## Confirmed, inferred, unknown

**Confirmed (static, two forms where load-bearing):**

- The record grammar, from the sampler's disassembly and from 303 records in
  60 retail files that end with zero slack.
- The state table, its scripts and the idle tables, read from the retail bytes
  and from the instructions that index them.
- The trigger conditions above, each at the cited instruction addresses
  (`config/animation/pc-flik-animations.json`).
- The complete set of sampler call sites, and no reference to slots 7 or 12.

**Inferred:**

- The gameplay names of the candidate rows, especially the hover-dive-pound
  chain (`0x02`/`0x07`/`0x1C`/`0x06`), the Z move, hanging from a seed and the
  tired idle.
- That Flik's part 8 extra words are a 4.12 scale: they run 3420→4096 on the
  Y axis in slot 3. Other models' extra words include 0, 2 and negative values,
  so this is not a general rule.

**Unknown:**

- What each of the 24 parts is (needs the `.ALL` model and its hierarchy).
- The axis order and units of the linear words and angles.
- The Z move's name, plant type 8, the actors in the Anthill Pt 2 bounce, and
  which seeds reach seed-state 3.
- Any runtime confirmation of a state number.

## Contradictions

(2026-10-12: resolved statically for the hover-dive-pound reading by [[EXP-20261012-005 - Flik movement state 4 ground pound]].
Landing fires 8 radial shots through `0x0042B020`, and no part of the state
slows a fall.)
EXP-20260930-004 calls movement state 4
(`0x0059D990`) "gliding". This trace reads the same path as a hover (vertical
velocity held at 0 for the countdown at `0x0044033C`) then a dive at maximum
fall speed ending in a pound (`0x00440390`–`0x00440419`). Both readings stand
until a runtime arm watches `0x0059D994`, `0x0059D940` and `0x0059D998`
through a second Shift press. Light Feet's counting rule is unaffected.

## Next experiments

1. **Runtime state check.** In a private Training copy, read `0x0059D998` and
   `0x0059D996` (no writes) while running, walking, turning, jumping, double-
   jumping, throwing, picking up and idling, and compare with the table.
2. **Visual previews.** Decode the `.ALL` part hierarchy so each slot can be
   drawn as a contact sheet; then the part names and channel meanings follow.
3. **Slots 7 and 12.** Render them once previews exist; a forced-state arm
   would need fresh write authorization.
