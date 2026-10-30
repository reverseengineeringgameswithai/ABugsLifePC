---
type: implementation
status: test-build
created: 2026-10-05
updated: 2026-10-29
evidence: [EXP-20261005-001, EXP-20261005-002, EXP-20261018-001, EXP-20261018-003, EXP-20261018-004]
tags: [implementation/modding, re/actors]
---

# PC native creature transplant

Moves native creatures, bosses included, from their home levels into another
level's RAW as test images. First use: Council Chamber's Thumper
(EXP-20261005-001). Then every
other boss and six tough regulars
(EXP-20261005-002).

A moved boss is an ordinary enemy run by its own script; its fight stays in
its home level's routine. Purple hits do −3. Health 101 makes a moved creature
immune (the Riverbed flight Hopper and the Cliffside and Canyon birds); Thud
respawns after about 101 frames, and regular enemies respawn natively. At home,
the Canyon Hopper's level routine makes him immune in stages (EXP-20261005-002).

## What a transplant copies

A transplant copies the donor's 28-byte type-35 row into the first free target
slot, changing only XYZ. It copies byte for byte the 0x101/0x102 packets whose
second dword is the type, and every texture page the model's faces name. A page
the donor level itself never loads is recorded rather than invented. A type the
target already has, a differing or ambiguous page with the same number, a
missing pair, a full table and impossible positions are refused. Only the
target level's `LEVEL.RAW` and `LEVEL.DAT` change; the EXE is unchanged.

## What moves with the row, and what does not

**Moves:** the model (00445020 loads character files by type), the script
(EXE table `0x004C83F0` by script byte), health (+0x10), flags (+0x12) and
the per-type handler (`0041C420`).

**Does not move:** level routines. Thumper's boss fight is `0x00431CB0`
(per-frame) and `0x00431BF0` (init), dispatched only for engine 2 and bound
to slot 1. Outside Council Chamber he is a heavy ordinary enemy: no health bar,
no thrown projectiles, no voices, no win at health < 21. At 0 he is killed and
removed like any enemy (−3 per purple hit, so 17 hits; red bounces off).

## Limits

- Donor names: [[EXP-20261012-006 - Creature types from the character loader]] gives every type's character file, for example 22
  `hopper`, 29 `molt`, 30 `bbird`, 36 `thud`.
- Avoid target slots 25 (engine 1 writes through Dot's slot) and 63.
- Check a donor's pages against the target.
- Homing (2026-10-12): purple and green berries lock on to the nearest
  on-screen live enemy. The bit they need is computed each frame from the
  camera's view, so a moved boss is targetable whenever it is in view
  ([[EXP-20261012-004 - Homing target visibility bit]]).
- Check a donor's drops against the target's sprite list (2026-10-12).
  Engine 1's list lacks entry `0x33`. A drop that
  reaches the pickup walker's default case spawns type `0x40` and would crash
  ([[EXP-20261012-002 - Sprite table census]]).
  Scripts, contact and kill paths spawn only drops on
  sprites below 50. The level routines and retirement chains that use
  sprites 50–52 do not move with a creature.
- Model records were at index 200 of 300 after the Thumper transplant.
- Bank-specific sounds and level routines need porting per boss. A real
  Thumper boss in another level means a guarded engine-1 port of `0x00431CB0`
  bound to the new slot, with his projectile slots and voices remapped.
- Homing: static rules and runtime flags disagree, but airborne bosses took
  purple hits (EXP-002); see [[Known Unknowns]].
- Immune donors (health 101) keep the target level's enemies-left count above 0.
- **Path lists (2026-10-18).** A donor whose script runs op 4 or op 10 walks
  the target level's list of the slot its `+0x0E` (or `+0x0F` with flag
  bit 3) names, and faults at `0x0041DDDE` if that slot is empty. In the test
  image the moved taxi bug followed the target's slot 1 list, Dot's route
  ([[EXP-20261018-001 - Creature row index census]],
  [[EXP-20261018-002 - Creature script counter in saved runtime samples]]).
  Check the donor's script and the target DAT before moving a walker.
- **When a donor thinks (2026-10-18).** Rows with `+0x11 = 100` run their
  script only while on screen. Movement, chase range and leash come from
  source `+0x14`–`+0x1B`
  ([[EXP-20261018-003 - Creature VM movement modes]]). The per-type
  handler moves with the type. For example, the long-legged spider fires
  aimed shots and badbugs bury and emerge
  ([[EXP-20261018-004 - Creature type handlers and opcode-11 subroutines]]).
  Opcode-11 operands 3–6 write fixed globals of the home level's routine,
  for example Thumper's `0x0059EF70 = 60`. In another level those addresses
  belong to whatever that level keeps there.
