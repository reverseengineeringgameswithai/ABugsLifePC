---
type: experiment
id: EXP-20261012-004
date: 2026-10-12
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static only. Full raw capstone decode of .text and the existing Ghidra export (decompiled text, cross-references, thunk-following callers) over retail bugs.exe, plus a scan of production c3d8b207…'s added sections; no game launch or memory access
question: What sets actor flags bit 0x0001 (+0x5C), which homing selection 0x00428400 requires but no donor creature row carries?
result: 0x00456640, called each frame from the actor updater 0x0041EC40, clears bit 0 for every active actor and sets it again when the actor passes a view-frustum test against the camera matrix 0x005B58E0. Homing therefore targets the nearest on-screen live actor. The EXP-20261005-001 contradiction is resolved; the static audit misread a per-frame visibility bit as row data
status: complete-bounded
created: 2026-10-12
updated: 2026-10-12
evidence: [EXP-20261005-001, EXP-20261005-002, EXP-20261012-001]
tags: [experiment/static, re/combat, mod/creature-transplant]
---

# EXP-20261012-004 - Homing target visibility bit

## Question

This is section 5.1 of [[Next Tasks]], the contradiction recorded in
EXP-20261005-001.

- **Static side.** Homing selection `0x00428400` walks the active-actor list
  `0x0059D7E0`. It accepts an actor whose word `+0x5C` has bit `0x0001` set
  and bits `0xA0` clear, then aims through `0x00464D40` and spawns the shot
  with `0x0042B020`.
- **Runtime side.** No donor row has bit 1, yet every boss gained it "once
  awake" (EXP-20261005-002).
  Examples: `0x52` → `0x4053`, `0x44` → `0x4045`, `0x984` → `0x4985`.

## Writers of `+0x5C`, all of them

A full decode of `.text` lists 94 writes with displacement `0x5C`. Those not
based on the stack, in actor code:

| Site | Function | Effect |
|---|---|---|
| `0x41bd5c` | `0x0041BD10` (row initializer) | Word = the creature row's `+0x12` |
| `0x41dff2`, `0x41e004` | `0x0041DC60`, creature-script opcode 12 | `(flags & op+2) \| op+4` |
| `0x41cf9b`, `0x429db0` | Contact kill, berry kill | Clear 2, set `0x880` |
| `0x428a7a` | `0x00428A60` | Clear 2, set `0x80` |
| `0x41d13c`, `0x429ca4`, `0x428955` | Contact, berry, `0x004288F0` | Set 2 |
| `0x43f1a5` / `0x43f47e`, `0x41d6fc`… | `0x0043ED60`, `0x0041D5B0` | Set or clear `0x40` |
| `0x41d02a` (`+0x5D`) / `0x43408c` | `0x0041C9B0` / `0x00433F90` | Set or clear `0x1000` |
| **`0x456665`, `0x45679f`** | **`0x00456640`** | **Clear bit 0, then `inc` the word when the test passes** |

Nothing else sets bit 0:

- **Constants.** No instruction sets it with a constant.
- **Scripts.** The 40 creature scripts (`0x004C7D00`–`0x004C83B8`, through
  table `0x004C83F0`) use opcode-12 values 0, 2, 4, 6, `0x40` and `0x8C0`
  only.
- **Added sections.** None of production's added sections writes `+0x5C`.

## `0x00456640`

It is called from the actor updater `0x0041EC40`, its only caller. For each
pointer in `0x0059D7E0` it does the following:

1. It clears bit 0 (`and byte [ecx+0x5c], 0xfe` at `0x00456665`).
2. It skips actors whose type has no model (`0x005B18E0[type]` = 0).
3. It transforms the actor's position, raised by `+0x66`, by the camera
   matrix rows at `0x005B58E0`. It requires the depth to exceed
   −radius (`+0x6A`). It also requires the absolute horizontal and vertical
   offsets, less the radius, to fall within depth × (`0x00861C60` / 2) /
   `0x00511508`.
4. If all of that passes, it runs `inc` on the word
   (`0x0045679a`–`0x0045679f`), which sets bit 0.

Both forms agree: the decompiled text and the raw decoding.

## Confirmed, inferred, unknown

- **Confirmed (static, two forms).**
  - Bit `0x0001` of actor `+0x5C` is recomputed every frame. It means "inside
    the camera's view frustum".
  - Homing `0x00428400` picks the nearest such actor whose bits `0x80` and
    `0x20` are clear.
  - The donor rows' lack of the bit is expected. The bit appeared when the
    bosses came into view.
- **Inferred.**
  - Homing never targets an off-screen enemy, and an enemy that leaves the
    view mid-flight drops out of later selections.
  - The airborne hits in EXP-20261005-002 locked on because those bosses were
    on screen.
- **Unknown.**
  - The writer of `0x4000`. No direct `+0x5C`/`+0x5D` write in code, scripts
    or added sections sets it, so it may come from a block copy. Homing does
    not test it.
  - The projectile sample suggested in EXP-20261005-001 (`+0x10` target,
    `+0x33` bit `0x08`) would still confirm lock-on live.
