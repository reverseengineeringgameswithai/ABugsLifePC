---
type: experiment
id: EXP-20261018-013
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Two read-only hardware arms under Wine/Gamescope on reflink copies of a derived build (EXE c3d8b207…), auto-hardware with all six markers before input, classic level select, private null sink, controllers disabled; XTEST key holds; no memory writes
question: Do the controls screen and the creature VM gate behave at runtime as EXP-20261018-006 and EXP-20261018-001/003 read them statically?
result: Yes on both. Three Lefts from Training reach "options", which logs "Start Options_Scr" and stores −3. Its first row, "change controls", opens "define keys", whose copy-back fills the item key bytes exactly per the static item-to-slot mapping. The live key table equals the defaults. In City Square, every selected but off-screen regular enemy stayed frozen, phase and position unchanged, in all 15 sample pairs. The fly changed in every pair while on screen and froze once Flik turned away
status: complete-bounded
created: 2026-10-18
updated: 2026-10-29
evidence: [EXP-20261018-006, EXP-20261018-001, EXP-20261018-003, EXP-20261012-004]
tags: [experiment/runtime, re/input, re/menus, re/creatures]
---

# EXP-20261018-013 - Options screens and the creature gate live

## Question

Two static results of the same day lacked a runtime form:

- the controls screen and its item-to-slot mapping
  ([[EXP-20261018-006 - Controls configuration screen and action bits]],
  KU-070);
- the gate that runs a regular enemy's script only while it is on screen
  ([[EXP-20261018-001 - Creature row index census]],
  [[EXP-20261018-003 - Creature VM movement modes]]).

The user, unavailable for manual review, left the choice of next work to
the agent. This bundled read-only arm needed no review and no memory writes.

## Setup

The pre-registration (`work/experiments/EXP-20261018-013/preregistration.md`)
was written before the first launch.

- **Builds.** `work/copies/EXP-20261018-013-options` and `-citysquare` are
  reflink copies of a derived build (EXE `c3d8b207…`). The build itself was
  not run or changed.
- **Code checked against retail.** These regions are byte-identical:
  - Options_Scr, the controls screen and its copy-back;
  - the defaults and the item table and labels;
  - CallOptions and the dispatcher;
  - the input read and poll;
  - the interpreter, the initializer and the visibility pass.

  The level select differs only in the medal and panel hooks
  (`0x00444231`–`0x0044429D`, `0x00444416`), and the frame update only in
  the seed-arm hook `0x0041EDB4`.
- **Data.** The derived build's City Square differs from retail only by an
  added packet 87. Its creature table is retail.
- **Each arm:**
  - `make session-audit` clean before launch;
  - `soil-trigger-runtime-probe.py launch --expect-auto-hardware
    --classic-level-select --disable-controllers`;
  - all six hardware markers in the log before any input;
  - XTEST holds and read-only samples through
    `work/experiments/EXP-20261018-013/drive.py`;
  - close through the probe, `bugs.log` moved into the packet, audit clean
    after.

## Arm A: options and controls

Packet `work/experiments/EXP-20261018-013/options/`, summarised in
`reports/input/EXP-20261018-013-controls.json`.

| Step | Observed |
|---|---|
| Select start | "training" centred. Live key table `0x004D8430` = `0xC8:0x10, 0xD0:0x40, 0xCB:0x80, 0xCD:0x20, 0x1D:0x8000, 0x2A:0x4000, 0x2C:0x8200, 0x39:0x200, 0x2E:0x400, 0x38:0x1000, 0x1C:0x8, 0x2D:0x800`, the defaults of `0x0042F0F0` slot for slot. Item key bytes all 0 |
| Left ×3 | "options" centred, next to an audio and a save icon |
| Return | Log `ROUTINE : --- Start Options_Scr ---`; carousel exit `0x00599AF8` = −3. The screen lists "change controls", "music volume", "sfx volume" and "graphics options", with "select option and press enter" |
| Return on the first row | "define keys". The item key bytes become `C8 D0 CB CD 1D 2A 38 2E 2D 39 2C` for items 0–10 and 0 for items 11–13 |
| Escape ×2 | Back at the level select |

The item bytes are the key-table slots in block B's order: seed color ← slot
9 (Alt), camera ← 8 (C), lock camera ← 11 (X), walk ← 7 (Space), kick ← 6
(Z). The screen draws the same labels, keys and columns as the decoded item
table.

**Side observation.** After Options_Scr the log shows Wine refusing the
8-bit palettized texture format: "FAILURE to map tpage 22 as a 8 bit
palettized surface - searching for 16bit instead". The game falls back to
16-bit ARGB 1-5-5-5. That bears on
[[EXP-20261018-009 - Four-bit page palette rows]]'s untraced note about
palettized textures.

## Arm B: the creature gate in City Square

Packet `work/experiments/EXP-20261018-013/citysquare/`. Analysis by
`research/creature-rows/vm-gate-samples.py`, report
`reports/creatures/EXP-20261018-013-gate.json`.

- **Run.** Right ×8 brought "city square" to the centre; Return twice
  loaded level 5 (35 slots). There were six idle samples about 1.5 s apart,
  a 1 s Left hold that turned Flik, then six more.
- **Pre-registered rule.** A slot is "predicted frozen" in a pair of
  consecutive samples when, in both, it is selected (`0x4000`) and off
  screen (`0x0001` clear), with source `+0x11` = 100, type ≠ 15 and flag
  `0x20` clear.

| Class | Pairs | Changed (phase, position, wait or PC) |
|---|---:|---:|
| predicted frozen | 15 | 0 |
| runs | 5 | 5 |
| not selected | 330 | 0 |

- **The fly** (slot 4, type 6) is the contrast. While on screen (flags
  `0x4005`) its phase, position and wait changed in all 5 idle pairs; it is
  visible top right in `frame-idle1`. After the turn it was selected but off
  screen (`0x4004`), and nothing changed in 5 pairs over about 7.5 s.
- **Others.** The roach (slot 0, type 19) and the long-legged spider (slot
  5, type 17) stayed frozen whenever selected and off screen.
- **Falsifiers:** none.

## Confirmed, inferred, unknown

- **Confirmed (runtime, matching the static reading).**
  - The level select's index 0 opens Options_Scr.
  - Options_Scr's first row opens the controls screen.
  - The item-to-slot mapping, and the defaults in the live key table.
  - Regular enemies (`+0x11 = 100`) do not run their script, move or
    animate while selected but off screen. They do while on screen.
- **Bounded.**
  - Every selected slot sampled had `+0x11 = 100`. The rule that rows with
    another `+0x11`, or type 15, run regardless was not exercised.
  - "Frozen" is measured at about 1.5 s intervals; a brief on-screen moment
    between samples cannot be excluded, though none would leave every field
    unchanged.
- **Unknown.**
  - The joystick "define buttons" mode.
  - The other options rows.
  - Whether the controls screen saves anything on "accept", which was not
    pressed.

## Consequences

- KU-070 has its runtime form. Since the screen has now been seen, the
  options screen's row labels are known.
- The creature gate is confirmed two ways. A moved regular enemy placed
  where the camera rarely looks will mostly sit still, which matters for
  [[PC native creature transplant]].
