---
type: research
status: confirmed-bounded
created: 2026-10-29
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260930-001, EXP-20260930-002, EXP-20260930-006, EXP-20260930-007, EXP-20261001-003]
tags: [re/ui, re/rendering, re/static, re/runtime]
---

# PC results screen and level select internals

The stack layout of the end-of-level results loop, how its sprites are drawn
and ordered, and the level-select carousel. First located while adding draws to
both screens in test builds (experiments cited as plain IDs). Native checks
executed the original results function to its return at image bases
`0x00400000` and `0x14000000`, with presentation stubbed and draws, sounds and
input observed at their thunks. Medal storage is in
[[PC save record and medal bytes]].

## Path and loop layout

Results are reached only through LEVELDONE → `0x00410310(4)` → `0x004447C0`
case 4 → `0x00442E70` ([[FUNC-97C95BA5572D-00442E70]]). The loop's locals,
proven by the bytes at `0x0044340D`, `0x0044353C`, `0x00443549`,
`0x004435A7`, `0x004435AF` and `0x004435B9` (EXP-20260930-001):

| Location | Contents |
|---|---|
| `[esp+0x10]` | animated letters |
| `[esp+0x14]` | countdown: 800; fade at 0x17; a completed skip sets 0x18 |
| `[esp+0x2C]` | enemies killed |
| `[esp+0x30]` | frame counter |
| EDI | animated grain |
| EBP | animated enemies |

- **Countdown store.** `0x00442FD3` is `mov [esp+0x18],0x320`, after the three
  medal decisions; a `push 0x11` precedes it, which is why the offset differs
  from the loop's `[esp+0x14]` (EXP-20260930-001, EXP-20260930-006).
- **Letter local.** EDI is zeroed at `0x00442E83` and stored to `[esp+0x20]`
  at `0x00442F07`. When the letter mask is complete, `0x00442F74` stores 2
  (earned before) or `0x00442F84` stores 1 (new) (EXP-20260930-006).
- **Letter targets.** The letter target table is a popcount table: retail
  `0x004DD6C0` has 16 entries ([[FUNC-97C95BA5572D-00442E70]]).
- **Tally sound.** The tally sample is 0x0E, played through `0x00419950`.
- **Length.** The unmodified screen lasts 800 frames; with a skip press at
  frame 100 it lasts 155 (native execution, EXP-20260930-001).
- **Frame rate.** The results screen runs at a 60 fps cap. EXP-20260930-001
  placed the store at `0x00441D3B`, but
  [[EXP-20261018-007 - Frame wait rounding]] corrects the address: CallOptions
  writes 60 at `0x0041032D` before dispatching to the results, and
  `0x00441D3B` is in Options_Scr. In hardware, results frames 2 to 276,
  counted by an added per-frame hook, took 4.40 s, about 62 fps
  (EXP-20260930-001).
- **Free hook.** The call at `0x00443408` goes to `0x00401E6F`, a thunk to the
  bare `ret` at `0x00459A80`, after each frame's draws.

## Sprite draws and page order

- **Two quad routines.** `0x00401A0F`→`0x00409150` and
  `0x004013F7`→`0x00408980` build the same textured quad. `0x00409150` writes
  depth 0.0; `0x00408980` writes `0x0055C78C` × scale (EXP-20260930-001).
- **System pages.** RAW types `0x30..0x57` load as system tpage `type - 0x24`
  (`0x00465030`, logged at `0x004DE240`; see [[FUNC-97C95BA5572D-00465030]]).
  The end-of-frame flush `0x00405EF0` draws tpages 0..63 in order.
- **Results pages.** The game log of a results screen shows tpages 0, 4, 22,
  23, 32 (the type-90 background) and 48–50 (types 84–86). Type 87 (tpage 51)
  is used in no logged level (EXP-20260930-001).
- **Type 87 is free everywhere.** No gameplay RAW, no `GFX/*.RAW`, and not the
  startup `LEVEL00/LEVEL.RAW` (system types 48–86) holds type 87, so tpage 51
  is free during play too (EXP-20260930-007).
- **Ordering in hardware.** A page appended as type 87 and drawn through
  `0x00409150` appeared above every other results sprite in hardware
  captures, the second evidence form for the tpage order and the depth-0
  draw. [[EXP-20261018-008 - Direct3D render states and the depth rule]]
  explains it: the depth test stays at the device default (LESSEQUAL, writes
  on).
- **Page format.** A system page is 4-bit, one 16-colour bank per 64×64 block,
  with index 0 as the colour key (recorded with EXP-20260930-001; the
  per-block palette row is traced in
  [[EXP-20261018-009 - Four-bit page palette rows]]).
- **Draw budget, unresolved wording.** EXP-20260930-006 recorded that
  `0x00409150` drops draws past its buffer, while noting that every hardware
  draw arrived in full. A later note recorded with EXP-20261001-003 narrows
  this: the Direct3D path flushes a page at 494 vertices, about 123 sprites,
  and only the software path drops draws. No hardware test drew past 494
  vertices.

## Level select

The select is `0x00443B40`. First recorded in EXP-20261001-003:

- **Carousel index.** At `0x00444416`, the per-frame call to the no-op thunk
  `0x00401E6F` after every carousel draw, the carousel index is `[esp+0x10]`
  (guards `0x00444331`, `0x0044439C`). Indexes 0–2 are the options, save and
  load icons; the exit stores index − 3 to the carousel word `0x00599AF8` at
  `0x004444C6`.
- **Quit question and leaving.** `0x0059A5F0`, the gameplay pause word, is
  set during the select's quit question; `0x005A9234` is set once the select
  is leaving.
- **Medal display.** It indexes the 12-byte table `0x004DD758` with the whole
  medal byte ([[PC save record and medal bytes]]).
- **Save prompt.** It reads `0x00572BFC` at `0x00443B51` (EXP-20260930-002).
- **Art reload.** CallOptions (`0x00410310`) reloads `LEVEL00\LEVEL.RAW`
  before every level select. That RAW's system pages are 12–30 and 33–50.
- **Tint.** In daytime levels and on the select the sprite colour words
  `0x005BA648`/`0x005BD738`/`0x005BA11C` are 128 (neutral); see
  [[PC sky, panorama origin and distant pass depth]].
- **Navigation.** The load/save entry is two Lefts from Training on the
  carousel (EXP-20261001-001).
