---
type: research
status: confirmed-bounded
created: 2026-10-29
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260915-005, EXP-20260915-006]
tags: [re/camera, re/level-data, re/static, re/runtime]
---

# PC telescope camera paths

How a telescope pickup starts a scripted camera tour, the LEVEL.DAT record that
holds each tour's path, and what a changed path must respect. First recorded
in EXP-20260915-005 (static queries, original-instruction replay at image
bases `0x00400000` and `0x01000000`, and hardware jump/tour/return runs in
Level01), with path measurements from EXP-20260915-006. Neither note is in this
vault. Related notes: [[PC camera view-transform chain]] (the eye source and
the common view), [[EXP-20261012-003 - Scripted camera flag census]] (the flags
word `0x0059A5EE`) and [[EXP-20261018-012 - Telescope hide flags]].

## Trigger

- Pickup selector `0x30` in the DAT type-63 table is the telescope. The pickup
  walker `0x00417720` counts telescope rows before its visibility checks,
  requires a near and active row (`+13` == 1) and proximity, and then sets the
  timer `0x00599AE8` = −1 and the ordinal `0x0059A5B8`
  ([[FUNC-97C95BA5572D-00417720]]).
- A telescope's Y bobs near floor − 800.
- Flik activates it by jumping into it, observed with normal Shift jumps in
  hardware.
- The ordinal follows table order: the first telescope row is ordinal 1. The
  hide flags `0x00599C68`–`0x00599C6B` remove the nth telescope
  ([[EXP-20261018-012 - Telescope hide flags]]). In Level01, `0x004317D0`
  sets `0x00599C69` (the second telescope) when the berry type `0x0059D9A7`
  is 3, gold ([[FUNC-97C95BA5572D-004317D0]]). That is static evidence plus
  flag-level replay, not a live gold-acquisition test.

## Path record grammar

- Ordinals 1, 2 and 3 use the positive DAT top-record types 11, 12 and 13.
- In the original `LEVEL01/LEVEL.DAT` these records are at file offsets 2380,
  2576 and 2772.
- Each is a 4-byte count/type header followed by 16 signed XYZ triples (196
  bytes, consistent with the 4 + count × 12 size rule for nonnegative types
  in [[PC LEVEL DAT prefix]]).
- Point 0 is the fixed look target. Points 1..15 are absolute camera
  positions.
- `0x0041A620` reads the matching pointer at `0x005C5888 + ordinal*4` and
  scales the coordinates by 32 (stored to runtime units).

## Tour

- **Start.** Entry waits for the fade to black, then starts the timer at 252.
- **Eye motion.** Native interpolation and `0x0041ACC0` smoothing move the
  eye `0x0059A5C0`. Selector `0x0059A5EE & 1` sends that source through the
  common view `0x00599C90`, and bit 1 freezes Flik through player flag 4.
- **Return.** Timer 13 requests the return; the ordinary Flik-follow view
  resumes, then a cooldown prevents immediate reuse.
- **Native checks.** Input cancellation and the native suppression flags pass
  original-instruction tests. A replay of a changed DAT at both bases gave
  240 active updates with 240 distinct eye positions, the exact target, Flik
  frozen and the ordinary view restored. Its floor, audio and ordinary-camera
  stubs and completed-fade fixtures mean it does not measure presentation
  timing.
- **Hardware.** Each normal Shift jump selected the right ordinal. A tour gave
  97 sampled moving-camera positions with the exact target, then timer 0 with
  Flik unfrozen, and ordinary Up moved him afterward. The passive reads are
  not atomic and do not prove whole-frame agreement.
- **Pitch.** The camera's pitch uses squared vertical and horizontal
  distances, not a conventional look-at. EXP-20260915-005's first paths
  framed their subjects poorly until they allowed for this, so framing has to
  be tuned in game.
- **Cue.** The first telescope keeps the level's native exit cue.

A separate observation in EXP-20260915-005 recorded 55 passive samples over
16.2 s of a level loaded as engine 1 with an inherited third telescope:
ordinal 3 and its target matched original path 13, and the tour, cooldown and
retrigger repeated while Flik stayed nearby. Four retail code regions matched
the loaded process exactly.

## Original path shapes

EXP-20260915-006 measured two original Level01 paths as a 166.61-degree spiral
(radius 7319 → 1067, height range 1912) and a 117.39-degree arc (radius
2265 → 966, height range 756). The note does not say which path number each
is; the original coordinates are in its private packet
`work/experiments/EXP-20260915-006/`.

## Requirements for a changed path

- **Shape.** A record holds exactly one target and fifteen camera positions.
  EXP-20260915-005 sampled shorter routes to fifteen positions, which keeps the
  original per-point timing.
- **Relocation.** Its compiler guarded the original rows' and paths' hashes,
  counts, signs and bounds before relocating the pointer tables, and replayed
  the changed DAT natively.
- **No camera collision.** The tour does not handle camera collision or
  occlusion; keeping the eye clear of terrain is the path author's job.
- **Second telescope.** In Level01 the second telescope row is the one the
  level routine hides once gold is equipped.
