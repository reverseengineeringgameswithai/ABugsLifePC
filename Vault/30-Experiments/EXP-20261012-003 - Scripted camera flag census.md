---
type: experiment
id: EXP-20261012-003
date: 2026-10-12
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static only. Raw capstone decoding, the existing Ghidra export (decompiled text and thunk-following callers) and EXP-20261012-001's reference list over retail bugs.exe; no game launch or memory access
question: Who reads and writes the flags word 0x0059A5EE, and what do its bits 0 and 1 do beyond the telescope tour?
result: It is the flags word of the scripted-camera block 0x0059A5C0–0x0059A5EF. Three setters write it; 0x0041B7D0's fade state machine sets and clears bit 0. Bit 0 swaps the camera source to the block and hides the HUD (0x0044D472 skips the HUD call 0x0044D47D). Bit 1 sets 0x0059D9A0 bit 4 for the view. Ten level and boss routines start such views through 0x0041A9D0
status: complete-bounded
created: 2026-10-12
updated: 2026-10-29
evidence: [EXP-20261012-001, EXP-20260915-005, EXP-20260910-005, EXP-20260930-007]
tags: [experiment/static, re/camera]
---

# EXP-20261012-003 - Scripted camera flag census

## Question

Section 5.5 of [[Next Tasks]]. Two open items ask about bit 0 of
`0x0059A5EE`:

- KU-066's camera source selector: [[PC camera view-transform chain]]
  confirmed it only for telescope tours.
- The HUD skip: EXP-20260930-007 found the HUD path testing it.

One census of the word's readers and writers was expected to answer both.

## Method

- **Reference list.** All 11 code references come from
  [[EXP-20261012-001 - REA Ghidra analysis trial]]: Ghidra's 10 plus the raw
  scan's `0x41a992`.
- **Decompiled text.** The export's text for each containing function.
- **Callers.** `ghidra-query callers`, which follows thunks.
- **Raw checks.** Raw decoding of the HUD test, the unrecognised setter, and
  raw `E8`/`E9` and pointer scans for its callers.

## Findings

### The block

`0x0059A5C0`–`0x0059A5EF` holds the scripted camera:

- the eye at `+0`/`+4`/`+8`;
- the target at `+0xC`/`+0x10`/`+0x14`;
- a second point at `+0x18`/`+0x1C`/`+0x20`;
- angle words at `+0x24`/`+0x26`/`+0x28`;
- state word `0x0059A5EC`;
- flags word `0x0059A5EE`.

### Writers of the flags word

| Site | Function | What it writes |
|---|---|---|
| `0x41a6d4` | `0x0041A620`, the telescope and path tour, with paths from `0x005C5888` (EXP-20260915-005) | The word 2 (bit 1), state 2 |
| `0x41aa7d` | `0x0041A9D0(x, y, z, angle, distance, flags)`, a point-and-heading view | The caller's flags word, state 2 |
| `0x41a992` | `0x0041A910` (thunk `0x00401023`), an eye-and-target view. Ghidra never made it a function | A flags argument, state 2 |
| `0x41b80f`, `0x41b86f` | `0x0041B7D0`, every frame | Sets bit 0 (`or 1`) and clears it (`and 0xFE`) |

### State machine in `0x0041B7D0`

- **Entering a view.**
  - State 2 fades to black through `0x00418860(0,0,0,0x10)` and moves to
    state 1. If bit 1 is set, it also sets `0x0059D9A0` bit 4.
  - State 1, once the fade ends (`0x005BA648` == 0), fades up, **sets bit
    0** and moves to state 0.
- **Leaving a view.** States 4 then 3 do the reverse: fade out, fade up,
  **clear bit 0**, and clear `0x0059D9A0` bit 4 if bit 1 was set.
- **Every frame.** With bit 0 set, the common camera `0x00599C90`… is copied
  from the scripted block (`0x0041ACC0`). Otherwise it comes from the player
  camera `0x0059DD90`.

### Readers

| Site | Function | Use |
|---|---|---|
| `0x44d472` | `0x0044D430`, the gameplay render | `test bit 0; jne` skips the HUD call `0x0044D47D` |
| `0x41b831`, `0x41b876`, `0x41b8ad` | `0x0041B7D0` | Bit 1 and the selection above |
| `0x438eb0` | `0x00438A80` | Bit 0 |
| `0x413a96` | `0x00413900` | `test` with a register mask |

### Who starts views

`0x0041A9D0` has ten callers:

| Caller | Call sites |
|---|---|
| `0x00431CB0` (Thumper's fight routine) | `0x0043200a` |
| `0x00433900` | `0x004339eb`, `0x00433c03` |
| `0x00434170` | `0x00434370` |
| `0x00434E10` | `0x004351d3`, `0x00435a78` |
| `0x00438040` | `0x00438404` |
| `0x004388B0` | `0x004389fc` |
| `0x00438A80` | `0x00438d02` |
| `0x00439410` | `0x004396ba` |
| `0x00439E90` | `0x00439fab` |
| `0x0043AE00` (Canyon Showdown Hopper) | `0x0043affc`, `0x0043b332` |

`0x0041A910` has no direct call or jump to its thunk, and no stored pointer
to either address.

## Confirmed, inferred, unknown

- **Confirmed (static, two forms: decompiled text and raw decoding).**
  - Bit 0 is the scripted-camera source selector for every view these setters
    start, not only telescope tours.
  - While bit 0 is set, the gameplay render skips the HUD call, so the HUD,
    and any added drawing that wraps that call, is hidden during scripted
    views.
  - Bit 1 holds `0x0059D9A0` bit 4 for the view.
- **Inferred.**
  - The ten callers are cutaway views in level and boss routines. Thumper and
    Canyon Showdown are identified; the others are named only by address.
  - `0x0041A910` is unused in retail. A computed call through the thunk area
    cannot be ruled out statically.
  - `0x0059D9A0` bit 4 is the event-voice blocker listed in
    [[EXP-20260910-005 - Flik event voice mappings]]. Its other readers are
    not surveyed.
- **Unknown.**
  - `0x00413900`'s mask.
  - Which levels' routines the eight unnamed callers belong to.
