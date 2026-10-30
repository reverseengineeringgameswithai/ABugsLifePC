---
type: experiment
id: EXP-20261018-006
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static disassembly (capstone) and data decoding of retail bugs.exe, raw reference scans, the existing Ghidra export for function bounds, and a search of 579 saved bugs.log files; no game launch
question: What is the configuration screen behind the 0x004D9CF9 array, and what does each input action bit mean (KU-070)?
result: It is the controls screen 0x00430DF0 ("define keys" / "define buttons"). The options screen Options_Scr 0x00441D20 opens it from its first row, and the level select's carousel position 0 opens Options_Scr. Its 14-item table names the eleven bindable actions, so each bit of the action word now has the developers' own label. Return (bit 0x8) is the only key the screen cannot rebind
status: complete-bounded
created: 2026-10-18
updated: 2026-10-18
evidence: [EXP-20260817-181, EXP-20261001-003, EXP-20260907-028, EXP-20260930-004, EXP-20260817-187]
tags: [experiment/static, re/input, re/menus]
---

# EXP-20261018-006 - Controls configuration screen and action bits

## Question

KU-070 asked two things
([[EXP-20260817-181 - PC input subsystem static census]]):

- what each bit of the action word `0x00598B10` means;
- which screen owns the `0x18`-stride array at `0x004D9CF9` that write
  block B (`0x00431022`–`0x004310A4`) copies into the key table
  `0x004D8430`.

Section 7 of [[Next Tasks]] marks it the weakest Bounded row of
[[Subsystem Coverage Map]]. Any control-remap feature builds on it.

## Method

- **Locating the screens.**
  - The Ghidra export gives function bounds.
  - Raw rel32 scans find the callers, which go through thunks
    (`0x00401D89` for `0x00430DF0`, `0x004018AC` for `0x00441D20`).
  - The pointers each function pushes were decoded as strings.
- **Tables.** The item table, its pointer list and the default stores of
  `0x0042F0F0` were decoded from the file bytes.
- **Logs.** The 579 saved logs were searched for the options screen's log
  line.

## How the screen is reached

1. **Level select** `0x00443B40` stores carousel index − 3 to `0x00599AF8`
   at `0x004444C6` (EXP-20261001-003). When the result is −3, carousel
   position 0, it calls `0x00441D20` at `0x004444EA`.
2. **Options screen** `0x00441D20` logs "ROUTINE : --- Start Options_Scr ---"
   (`0x004DDB80`). Its prompts are "select option and press enter",
   "() - to change", "press enter to accept changes" and "press esc to go
   back". Its rows sit at y = 70, 95, 120, 145 and 170 (words at
   `0x004DD5A0`). The cursor on the first row, y 70, calls `0x00430DF0` at
   `0x004421E1`.
3. **Controls screen** `0x00430DF0` titles itself "define keys" or "define
   buttons" (`0x004DA590`, `0x004DA57C`).

## The controls screen's items

- **Layout.** 14 items of `0x18` bytes start at `0x004D9CE8`. Each holds X,
  Y, a zero dword and a label pointer at `+0x0C`.
- **Key byte.** The bound key is the byte at `+0x11`, so
  `0x004D9CF9` is item 0's key. It is zero in the file and filled at run
  time by `0x00430B10`, which copies the table back.
- **Order.** The pointer list `0x004D9E38` names the items in order and
  ends with −1.

| Item | Label | Key-table slot (block B store) | Default key (`0x0042F0F0`) | Action bit |
|---:|---|---:|---|---|
| 0 | forward | 0 (`0x00431022`) | Up (`0xC8`) | `0x0010` |
| 1 | back | 1 (`0x00431027`) | Down (`0xD0`) | `0x0040` |
| 2 | left | 2 (`0x0043103E`) | Left (`0xCB`) | `0x0080` |
| 3 | right | 3 (`0x0043104A`) | Right (`0xCD`) | `0x0020` |
| 4 | fire/get/drop | 4 (`0x0043104F`) | left Ctrl (`0x1D`) | `0x8000` |
| 5 | jump/change | 5 (`0x0043106C`) | left Shift (`0x2A`) | `0x4000` |
| 6 | seed color | 9 (`0x00431072`) | left Alt (`0x38`) | `0x1000` |
| 7 | camera | 8 (`0x00431077`) | C (`0x2E`) | `0x0400` |
| 8 | lock camera | 11 (`0x00431099`) | X (`0x2D`) | `0x0800` |
| 9 | walk | 7 (`0x0043109F`) | Space (`0x39`) | `0x0200` |
| 10 | kick | 6 (`0x004310A4`) | Z (`0x2C`) | `0x8200` |
| 11 | game pad | — | — | — |
| 12 | restore defaults | — | — | — |
| 13 | accept | — | — | — |

- **Return.** Slot 10, Return (`0x1C`, bit `0x0008`), is written by the
  defaults and by neither block. Return is the menus' accept key, which is
  why the screen leaves it alone. That answers KU-070's "why `DIK_RETURN`'s
  slot is excluded".
- **The dispatcher** (`0x00430FEC`–`0x0043100E`) acts on the chosen item:
  - item 11 goes to `0x004310E4` (the "define buttons" mode);
  - item 12 restores defaults (`0x004310D0`: `0x0042F0F0`, then
    `0x00430B10`);
  - item 13 applies block B;
  - items 0–10 wait for a key (`0x0059EE08 = 10`, `0x004017CB`).

## Agreement with earlier evidence

- **Runtime, two bits.**
  - Bit `0x4000` on left Shift is jump
    ([[EXP-20260907-028 - Representative update and render headroom]],
    EXP-20260930-004); the label is
    "jump/change".
  - Bit `0x8000` on Ctrl was observed live when throwing
    ([[EXP-20260817-187 - Runtime berry throw reconnaissance]]); the label is
    "fire/get/drop".
- **Static.**
  - The defaults match [[PC Flik animation catalog#Controls]] key for key.
  - "kick" = `0x8200` is the catalog's "Z = Ctrl + Space in one key".
- **Not agreeing at first.** The catalog calls C (`0x0400`) "turn in
  place"; the game's label is "camera". Resolved below: the key does both.
  - **Discriminating check:** find the consumer of bit `0x0400` in Flik's
    controller (`0x0043F9E0`) and in the camera code (`0x0041ADF0`, EXP-164),
    or watch C in game. Done statically the same day; see the resolution
    below.

## Resolution: "camera" and "turn in place" are both right (later the same day)

Both consumers of bit `0x0400` read `0x00599AF4`, the gameplay copy of the
action word. It is stored from `0x00861C98` at `0x004144E0`, then masked
per state at `0x0041450E`–`0x00414565`.

- **Camera.** `0x0041ADF0` loads it at `0x0041AE1E`.
  - Bit `0x0400` selects camera mode 2 (`0x00572F04 = 2`,
    `0x0041AE74`–`0x0041AEEE`), with its own distance values.
  - Bit `0x0800` ("lock camera") selects mode 3 (`0x0041AEF3`–`0x0041AF1A`).
- **Flik's controller** `0x0043F9E0`, at `0x0044056D`–`0x0044059A`. While
  bit `0x0400` is held:
  - Left (`0x80`) subtracts `0x20` from Flik's heading `+0x28`, and Right
    (`0x20`) adds it;
  - normal movement is skipped (`jmp 0x004405CE`).

So holding C changes the camera view and makes the arrows turn Flik in
place. The game's label and the animation catalog's reading describe the
same key. The contradiction is resolved.

## Confirmed, inferred, unknown

- **Confirmed (static).**
  - The call path from the level select to the controls screen.
  - The item labels and coordinates.
  - The item-to-slot mapping, the default keys and bits.
  - The dispatcher's arms.
  - Return's exclusion.
- **Confirmed (static plus earlier runtime).** Jump (`0x4000`) and fire
  (`0x8000`).
- **Inferred.**
  - "seed color" (`0x1000`) cycles the equipped berry (`0x0059D9A7`).
  - What camera modes 2 and 3 look like. "Lock camera" (`0x0800`) selects
    mode 3; see the resolution above.
  - What "change" in "jump/change" does.

  These are the developers' words, and no handler was traced here.
- **Unknown.**
  - The joystick "define buttons" mode and block A (`0x00430C3F`, reached
    only through the uncalled thunk `0x00401DF2`).
  - The options screen's four other rows.
  - Whether `0x00598B12`, `0x00598BC0`–`0x00598BC6`, `0x00598B5C` and
    `0x00598B60` have consumers.
  - **Runtime.** No saved log contains "Options_Scr", so neither screen has
    been seen in a run. (Later the same day: seen, read only, with the
    mapping confirmed in live memory, [[EXP-20261018-013 - Options screens and the creature gate live]].)

## Consequences

- **KU-070** is answered for the configuration screen's identity and the
  meaning of the bits.
- **Control-remap work.** A remap should write the item key bytes, or the
  key table through block B's mapping. It must keep slot 10 (Return) as is,
  since the menus rely on it.
