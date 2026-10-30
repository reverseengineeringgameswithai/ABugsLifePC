---
type: research
status: confirmed-bounded
created: 2026-10-29
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260911-020, EXP-20260928-001, EXP-20261001-004]
tags: [re/level-routing, re/load-screen, re/rendering, re/static, re/runtime]
---

# PC level start, special slot and load screen

What happens between choosing a level and playing it: how the carousel
position becomes an engine index, how the special index-16 slot is reached,
and how the level start draws its load screen and fades it. The roster tables
themselves are in [[PC level roster and numbering]]. Experiments cited as plain
IDs are not in this vault.

## Carousel to engine index

[[PC level roster and numbering]] records the 16-entry table at `0x004C6A30`,
`(17,1,3,2,6,10,11,4,5,14,7,12,13,9,8,15)`, and the special index 16 reached
when `0x004F0680` is nonzero. EXP-20260911-020 adds the instruction-level
detail (confirmed static plus original-instruction execution):

- `0x0041012D..0x00410165` reads the signed carousel word `0x00599AF8`,
  selects the table entry, copies a progress byte from `0x0059D8F8`, and
  overwrites the engine index `0x00861C84` with 16 at `0x0041015B` when dword
  `0x004F0680` is nonzero.
- The outer loop `0x0043DA40` sets that flag after level-done value 6. A fresh
  disassembly of `0x0043DE69..0x0043DE7E` shows the compare against 6, the
  flag write at `0x0043DE73` and the jump back to restart.
- The per-frame dispatcher has a real index-16 handler, `0x0043BD10`.
- 64 cases ran exactly that instruction range in an isolated emulator: sixteen
  carousel positions × flag 0/1 × loaded PE bases `0x00400000`/`0x01400000`,
  relocated through the PE relocations, with EBX = 0 as the preceding native
  code leaves it. Each stopped at `base+0x10165`; the engine index equalled the
  table entry for flag 0 and 16 for flag 1, and the copied progress value
  stayed `slot & 7`. This is not a full initialization replay or a playthrough
  of the special stage.
- **Requirement.** Absence from the carousel does not make index 16 free. Its
  exact name and full semantics are unknown. Finishing it plays the `ALT_*`
  videos ([[PC FMV playback]]).

## Progress after a level

When a level ends with level-done 1, LEVELDONE at `0x0043DD6A`–`0x0043DD94`
raises the progress position `0x0059D8E4` when the current stage equals it
(EXP-20260928-001, static). [[PC gameplay loop and player event sites]] has the
rest of the outer loop.

## Level start `0x0042E5C0`

Besides the intro video ([[PC FMV playback]]), the spawn copy `0x0043E6B0`
([[EXP-20260906-005 - Isolated authored terrain and platform spawn]]) and the
clearing of the telescope hide flags at `0x0042E838`–`0x0042E84A`
([[EXP-20261018-012 - Telescope hide flags]], [[PC telescope camera paths]]), the level start draws the load
screen. First recorded in EXP-20261001-004 (static, native execution of the
call site at two bases, and hardware captures):

- **Picture.** `0x0042E5C0` inlines InitLoadScreen (string `0x004D834C`). It
  loads the picture through `0x004634E0`, chosen by the engine level
  `0x00861C84`; level 1, the default case, is `gfx\level1a.raw` (94,088
  bytes). The log shows `Start InitLoadScreen`, `Loading packet data
  gfx\level1a.raw, level 1`, the level RAW load, then
  `Start/End ClearLoadScreen`.
- **Loop.** InitLoadScreen runs 24 frames: fade step `0x004188A0`, frame
  begin `0x00405BE0`, the picture `0x0040ADE0(0x21,0x22)` at `0x0042E6AE` and
  the loading sprite `0x00408980(0x20,200,0x80,0)` at `0x0042E6C7`. Then come
  the level load `0x004671D0` and ClearLoadScreen `0x0042E150` (picture draw at
  `0x0042E1DC`). ClearLoadScreen has an automatic mode that fades to black over
  24 frames.
- **Fade.** `0x00418860` stores a target RGB and speed, and `0x004188A0`
  steps the tint words `0x005BA648`/`0x005BD738`/`0x005BA11C` toward it.
  `0x0042E5C0` zeroes the current values (`0x0042E610`–`0x0042E61E`), then
  `0x0042E68A` sets the target to 0x80 with speed 6 (`e85a31fdff`, call
  `0x004017E9`). The picture's quad drawer `0x0040A090` colours with
  fade × 0xE0 >> 7; the sky `0x00404AE0` scales its material by fade >> 7;
  the panorama strip `0x00404410` also references `0x005BA648`.
- **The sky behind the picture.** The Direct3D frame begin `0x00405D20` calls
  the sky `0x00404AE0` and the panorama `0x00405410`. During InitLoadScreen no
  panorama is loaded yet. During ClearLoadScreen the level's data is loaded
  and `0x004DE09C`/`0x004DE0A0` = 0 pin the panorama to the top of the screen;
  natively the picture covers it.
- **Training.** Engine 17 loads `gfx\training.raw` and shows its "Training
  Level" picture through a native wait for a button press (hardware).

### What changing it showed

- **Retargeting the fade.** Rewriting the three colour arguments of the call
  at `0x0042E68A` to 0 (speed 6 kept) for one context left every captured
  load-screen frame pure black (maximum luminance 0, 16 frames), and the level
  then faded in natively over about 0.7 s. The picture was still loaded,
  unseen.
- **Skipping the draws instead.** Skipping the picture draws (`0x0042E6AE`,
  `0x0042E1DC`) and the sprite (`0x0042E6C7`) removed the picture, but
  ClearLoadScreen then showed the level's own sky and a hill strip at the top
  of the screen, fading out (captured maximum luminance 168).
- **Fade coverage.** Every load-screen draw seen in hardware was fade-scaled
  (`0x0040A090`, `0x00404AE0`; `0x00404410` references the fade). An overlay
  drawn there without the fade would still show.
- **Log timing.** In a capture started before launch, black frames ran from
  18.05 s to 21.68 s and the log's `Start InitLoadScreen` line was first seen
  at 20.95 s. EXP-20261001-004 concludes that `bugs.log` flushes late, so it
  is not a frame clock.
