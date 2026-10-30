---
type: research
status: confirmed-bounded
created: 2026-10-29
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260909-002, EXP-20260928-001, EXP-20260930-002, EXP-20260930-004, EXP-20260930-005, EXP-20260930-006, EXP-20260930-007, EXP-20261001-003]
tags: [re/gameplay, re/player, re/timing, re/static, re/runtime]
---

# PC gameplay loop and player event sites

Where the retail executable runs a level frame by frame, and the single native
sites at which a jump, a berry throw, a hit, a death, a letter and a seed token
happen. These were first located to count player events in test builds; the
experiments are cited as plain IDs. Their native checks executed the original
instructions at image bases `0x00400000` and `0x14000000`, and their hardware
arms used XTEST key presses with read-only memory samples.

## Outer loop `0x0043DA40`

Confirmed static, first recorded in EXP-20260930-002, with the death path from
EXP-20260930-006 and LEVELDONE from EXP-20260928-001:

- **Start.** ReStart calls `0x00410010`, then InitMainGame through thunk
  `0x00401BC7` at `0x0043DBB2`. NextLife clears level-done `0x0059A5B0` and
  pause `0x0059A5F0`.
- **Gameplay loop** (`0x0043DC15`–`0x0043DC5F`). It calls
  `0x004014E2`→`0x0040FFC0` at `0x0043DC27`. It keeps running frames while
  level-done is 0, or while the 0x2D-frame death countdown `0x0059D9B8` is
  nonzero (`0x0043DC1E`).
- **Death.** Every death path writes level-done 2 together with the countdown
  (for example `0x0041C7FF`/`0x0041C806` and `0x0041C8DC`/`0x0041C8E3`; see
  [[FUNC-97C95BA5572D-0041C6C0]]). After the loop, level-done 2 calls the
  respawn and re-enters at `0x0043DBB7`, after the InitMainGame call, so
  InitMainGame does not run again on a respawn.
- **Completion.** The loop exits at `0x0043DC61`. Level-done 1 enters
  LEVELDONE; at `0x0043DD6A`–`0x0043DD94` that path raises the progress
  position `0x0059D8E4` when the current stage equals it.
- **Level-done values.** 0 playing, 1 completed, 2 death; EXP-20260930-002
  counted 2 and 3 together as the death and quit states. Value 6 sets the
  special-stage flag ([[PC level roster and numbering]]).

## One gameplay frame `0x0040FFC0`

- It writes the frame cap `0x004F1710 = 0x1E` (30) every frame, then runs the
  pause handler `0x00413900` instead of the game update `0x004144C0` while
  `0x0059A5F0` is set (EXP-20260930-002). EXP-20260930-007 records the update
  call as `0x004017B7`.
- It then runs the render `0x00401B81`→`0x0044D430` every gameplay frame,
  paused or not (EXP-20260930-007).
- The render calls the HUD `0x00401BB3`→`0x00416890` at `0x0044D47D`
  (`push 0x40`) unless `0x0059A5EE` bit 0 is set (EXP-20260930-007; bit 0 is
  read in [[EXP-20261012-003 - Scripted camera flag census]]).
- **Measured rate.** In hardware the gameplay timer advanced 30.52, 30.53 and
  30.88 frames per wall second (EXP-20260930-002) and 30.4–30.7
  (EXP-20260930-004). [[EXP-20261018-007 - Frame wait rounding]] traces the
  excess over 30 to the frame wait `0x00405AD0`, which caps the rate at
  31.25 fps. A limit counted in frames is therefore game time, and a slower
  machine runs it slower.

## Flik's record and movement state

The update `0x004144C0` does `push 0x0059D910; call 0x0040103C` at
`0x00414578`, the thunk to the player controller `0x0043F9E0`. So the
controller's record is Flik's `0x0059D910`
([[STRUCT-PC-FLIK-POSITION-GLOBALS]]): `+0x30` is the vertical velocity
`0x0059D940` and `+0x80` the movement state word `0x0059D990`. First recorded
in EXP-20260930-004.

- **Jump input.** The controller tests input bit 0x4000 in the current word
  `0x00599AF4`, with the previous word `0x0059DD8C` for edges.
  [[EXP-20260907-028 - Representative update and render headroom]] maps that
  bit to left Shift through `0x004D8458`.
- **Two jump starts.** A grounded jump sets state 1 on the branch taken when
  Shift is held, the state is 0, 2 or 3, and Flik is within 0x400 of the
  ground. A special-mode branch, on a fresh Shift edge, also sets state 1 and
  subtracts 0x800 from the velocity.
- **No other writer stores 1.** Every absolute write to `0x0059D990` in
  `.text` stores 5 or 0. State 5 comes from the plant and mushroom code
  `0x00468010`/`0x00468BF0` ([[PC seed and mushroom collision state]]), seed
  contact `0x0041C9B0`, and from `0x0041C6C0`, `0x00434E10`, `0x00436B40`
  (DI = 5 from `0x004373AA`) and `0x00439E90`, whose roles were not
  established. State 0 comes from the respawn reset `0x0042DDB0`.
- **Meaning.** So a jump is an unpaused gameplay frame on which the state
  becomes 1. State 2 is falling, 5 a bounce or launch, 0 a respawn, and 4 is a
  hover-dive ground pound ([[EXP-20261012-005 - Flik movement state 4 ground pound]]).
  In hardware each Shift press showed states 0 → 1 → 2. Holding Shift makes
  Flik re-launch on landing, and each launch sets state 1 again. A hit's
  knockback sets state 5 (EXP-20260930-006).

## Berry throw

First recorded in EXP-20260930-005:

- `0x0043EB60(record)` is the berry throw. It takes the launch point from the
  heading, the projectile class from the berry type `+0x97`, increments the
  owner count `+0x96`, spawns through `0x0042B020` and plays throw sound 2
  (`0x004148A0`). See [[PC projectile records, homing and kill accounting]].
- Its only thunk is `0x00401EAB`. The only call to that thunk is in the
  player controller at `0x00440555`: `cmp word [esi+0x86],0xA` (throw
  animation frame 10), `jne`, `push esi`, `call 0x00401EAB`, `add esp,4`.
  ESI is Flik's record `0x0059D910`.
- One call is one throw. A volley that spawns several projectiles is still one
  call, and pauses never reach the controller. In hardware, four and seven left
  Ctrl presses counted four and seven calls, and the movement state stayed 0
  through every throw.
- The controller's throw path tests `0x0300` and `0x8000` in `0x00599AF4`
  (`0x0044048E`–`0x0044049E`; EXP-20261001-003).

## Input words

The poll `0x00464E10` copies the previous action word to `0x00861C8C` and the
new one, from `0x00598B10`, to `0x00861C98`. The update `0x004144C0` copies it
into the frame's input word `0x00599AF4` at `0x004144E0`, then applies the
native masks (EXP-20261001-003).
[[EXP-20261018-006 - Controls configuration screen and action bits]] maps the
action bits: `0x8000` left Ctrl, `0x0200` Space, `0x8200` Z. EXP-20261001-003
found the default gamepad binding for `0x8200` to be button 3, which it inferred
to be triangle in both the raw DualShock and XInput-style orders (no controller
was used in its arms).

## Health, hits and deaths

[[FUNC-97C95BA5572D-0041C6C0]] holds the hit handler: the only health decrement
`dec word [0x0059D9A4]` at `0x0041C7A5`, the `JNS` at `0x0041C7E1`, and modes
0, 1 and 2. EXP-20260930-006 found the other writers of health from the Ghidra
data references: the HUD clamp to 4 (`0x00416A83`), refills to 4
(`0x00417E56`, `0x00418D48`, the respawn `0x0042DEFB`) and one increment
(`0x004293F1`). A fall out of the world kills without touching health, so a
death is visible as level-done 2, not as a health change. In hardware one native
hit took health 4 → 3 and set movement state 5; one fall at timer frame 511
set level-done 2, left health at 4, and Flik respawned at frame 534
(EXP-20260930-006).

## Timed protection

First recorded in EXP-20260909-002 (static disassembly and original-instruction
pickup and damage tests; no live power-up was collected):

- The pickup walker `0x004292C0` consumes a dynamic-pool type `0x0C` record
  and writes signed `0x0059D98E` = 400 at `0x00429432`.
- Positive values block ordinary damage in `0x0041C6C0`; the controller
  `0x0043F9E0` decrements positive values each update.
- Type `0x2E` writes −3 instead, and eligible hits consume that negative
  counter.
- The ordinary hurt cooldown `0x0059D9A2` is separate.
- The instant-death argument to `0x0041C6C0` bypasses all of these.

Calling the positive timed effect "invincibility" is a semantic
correspondence. Its original icon, name and natural availability were not
established.

## Letters and seed tokens

- **Letters.** Bit k of the letter mask `0x0059D9B2` is letter k of the level's
  word. The OR sites are in [[FUNC-97C95BA5572D-00417720]]. In hardware, one
  native pickup per position set the mask 0x01, 0x03 … 0xFF in order. The
  letters survived a respawn, and lives went up by one when the word completed,
  the native letter bonus (EXP-20260930-006).
- **Pickup table.** `[0x005C595C]` holds a count word, the type word 63, then
  16-byte rows (X, Y, Z dwords; selector byte at +12) (EXP-20260930-007; the
  row size is the type-0x3F rule in [[PC LEVEL DAT prefix]]). A taken pickup
  keeps its row, with Y set to `0x80000000` (`0x00417A30`).
- **Seed tokens.** Selectors 0x29–0x2C are cases 10–13 of `0x00417720`'s
  switch and add 17 to `0x0059D9A8`–`0x0059D9AB`
  ([[FUNC-97C95BA5572D-00417720]]). In hardware, two green tokens took the green
  byte 0x00 → 0x22 and four berry tokens the berry byte 0x00 → 0x44.
- **Training's hidden tokens.** `0x0043C040` registers Training's two green
  and four berry token rows (`0x0059F694`/`698`, `0x0059F6A0`–`6AC`) and adds
  8000 to their Y and to their word at +0x0E, so they start 8000 units down.
  The lesson reveal `0x0043C880`–`0x0043C8E6` adds −8000 to both. Lessons are
  dispatched by `0x0043C340` (EXP-20260930-007). `0x0043C040` is engine 17's
  entry in the level init table ([[PC boss level routines and creature transplant limits]]).
- **Levels without tokens or grain.** A bounds-checked census of each level's
  type-3F pickup table, in a build whose tables for these two levels are
  inferred to be the original ones, found no seed tokens in Bug Bar or
  Riverbed Flight and no grain in Bug Bar (EXP-20261001-003).

## Hook points with no side effect

A call to thunk `0x00401E6F`, whose target is the bare `ret` at `0x00459A80`,
sits after each frame's draws in two loops: the results loop at `0x00443408`
and the level select at `0x00444416` (EXP-20260930-001, EXP-20261001-003).
Replacing either call adds per-frame work without displacing native code. The
render thunk `0x00401B81` (called at `0x0040FFD9`) and the HUD call at
`0x0044D47D` are the gameplay equivalents. Hooks that replace a relocated
instruction must retire its fixup (for example the HIGHLOW fixup at RVA
`0x1C7A8`, offset 3 of the 7-byte decrement at `0x0041C7A5`; EXP-20260930-006).
