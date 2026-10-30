---
type: research
status: confirmed-bounded
created: 2026-10-29
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260930-001, EXP-20260930-002, EXP-20260930-003, EXP-20260930-007, EXP-20261001-001, EXP-20261001-003]
tags: [re/save-data, re/gameplay, re/static, re/runtime]
---

# PC save record and medal bytes

How the retail executable keeps per-level progress, how it writes that to a
save file, and what a changed file or executable must respect. The experiments
cited as plain IDs are not in this vault. They hooked the save, load and results
code in test builds, and they executed the original instructions at two image
bases (`0x00400000` and `0x14000000`) with presentation and file calls stubbed.

## Save files

Confirmed, static, first recorded in EXP-20261001-001:

- **Save.** `0x0049AB30` builds `[0x00861F20]` + `\save\` + `game0.sav`, with
  the digit replaced by the slot `[0x007C6374]`. It opens the file with `"wb"`
  through `0x004B0730` and writes `0x004B05B0(buffer, 0x21C, 1, file)`. It
  succeeds only when that returns 1 (`0x0049AC8E`). The log strings ("SAVE :
  Attempting to save file %s in path %s") sit beside them.
- **Load.** `0x0049A8E0` is the same with `"rb"` and `0x004B1170`.
- **Root folder.** Under Wine the root is `R:\PC\BUGS`, the game copy's own
  folder. The hardware log of a successful save reads "SAVE : Successfully
  save file R:\PC\BUGS\save\game0.sav".
- **Menu buffers.** The save/load menu `0x0049AE10` reads all eight slot files
  into buffers `0x004E30E8` + 0x220·n for its list (`0x0049AE62`).
- **Saving a slot.** The menu copies the live record `0x004D8428` (0x204
  bytes) to `buffer+0x18` (`0x0049B562`) and writes that buffer
  (`0x0049B572`).
- **Loading a slot.** The menu re-reads the chosen slot (`0x0049B748`) and
  copies `buffer+0x18` over `0x004D8428` (`0x0049B790`–`0x0049B79F`). This is
  the only such copy in `.text`.
- **New game.** The defaults `0x00418FA0` (lives 5, zero medal block) run on
  `0x004D8428`, from `0x00403C57` and `0x0041448D`.

So a save file is 540 bytes: a 0x18-byte slot header, then the 0x204-byte
record. The disc's `SAVE/GAME0–7.SAV` are 540 bytes each, fresh-game records
(5 lives, zero medals) behind a slot header.

The disc's `PC\BUGS` folder has no `save` folder. A game copy made from it
cannot save until one exists, because `fopen("wb")` has nowhere to write. No
earlier note had recorded an in-game save; the first one was made in
EXP-20261001-001's hardware arm after a `save` folder was added.

The C runtime routines the save code calls are `fopen` `0x004B0730`, `fread`
`0x004B1170`, `fwrite` `0x004B05B0` and `fclose` `0x004B04E0`. The executable
also imports `CreateFileA`, `ReadFile`, `WriteFile`, `SetFilePointer` and
`CloseHandle` from KERNEL32 (recorded with EXP-20261001-001).

## Record layout

The save routine `0x00419030` fills the record `0x004D8428`, and the load
routine `0x004190D0` restores from it, around the file calls
`0x00401186`/`0x00401811`. First recorded in EXP-20260930-007:

| Record offset | Filled from | Contents |
|---|---|---|
| `+0xA8` | lives | |
| `+0xA9` | `0x0059D8E4` | progress position ([[PC FMV playback]]) |
| `+0xAA` | 19 bytes at `0x0059D8F8` | 16 medal bytes, the flags byte `0x0059D908` (byte 16), bytes 17 and 18 |
| `+0xBD`–`+0xC3` | option settings | `0x00441D20` reads and writes `0x004D84E5`–`0x004D84EA` |
| `+0xC4` | 320 bytes at `0x00599B20` | |

`0x00419030` and `0x004190D0` copy all 0x13 bytes of the block at `+0xAA`
(EXP-20260930-001; byte copies `0x0041904D`, `0x00419123` in
EXP-20260930-003).

Bytes 17 and 18 (`0x0059D909`, `0x0059D90A`) are native story and progress
state. EXP-20260930-007 names the functions that use them (`0x0041C9B0`,
`0x00429790`, `0x0043DA40`, `0x00468010`). EXP-20260930-002 lists example
sites: byte 17 at `0x0041CF0B`, `0x00429CE7`, `0x0043DE8D` and `0x0046849C`;
byte 18 at `0x0043BD14`, `0x0043D327` and `0x0043DE9F`. After the engine-16
special stage the game plays video `0x0059D90A + 0x29`
([[PC FMV playback]]).

**No free bytes.** The record's gaps are option settings and the bytes after
`0x0059D908` are story state. The only saved bits native code never sets are
masks 0x04–0x80 of `0x0059D908`, which no native code reads either
(EXP-20260930-007), and bits 0x08–0x80 of each medal byte, which native
whole-byte compares still read (EXP-20260930-003; see below).

## Medal bytes

[[FUNC-97C95BA5572D-00442E70]] records the results routine that ORs masks
1/2/4 (grain, letters, enemies) into `0x0059D8F8[word 0x00599AF8]`. Medals
are cumulative: earning the letter medal on one visit and the other two on a
later visit completes the byte on that later visit. The rest of the byte's
life, first recorded in EXP-20260930-001 unless marked:

- **Snapshot.** InitMainGame loads the slot's byte at `0x00410140` and stores
  it in `0x00572BF8` at `0x00410153`, that address's only writer.
- **Full-medal bonus.** LEVELDONE `0x0043DCEE`/`0x0043DDEE` checks
  `byte == 7 && 0x00572BF8 != 7`. It then plays the slot's bonus clip through
  `0x004132E0`→`0x00412F20`, and sets `0x0059D908 |= 2` when all 16 slots sum
  to 0x70. The native code skips the clip call for slot 0 (EXP-20260930-003).
- **Save prompt.** `0x00572BFC` is written when medals change
  (`0x00442F54`/`F92`/`FC9`). The level select `0x00443B40` reads it at
  `0x00443B51` to offer the save prompt (`0x00442C70`) and the save
  (`0x00419030`) (EXP-20260930-002).
- **Level-select display.** The select draws the highlighted level's medals
  by indexing a 12-byte table at `0x004DD758` with the whole medal byte, read
  through base `0x0059D8F5` at `0x00444231`, `0x00444267` and `0x00444298`
  (EXP-20261001-003).

## The flags byte `0x0059D908`

It is byte 16 of the medal block, so save and load copy it. All ten code
references in retail `.text` test or OR only masks 0x01 and 0x02: `0x0042E5E6`,
`0x0043D309`, `0x0043DD30`/`0x0043DD3A`, `0x0043DE30`/`0x0043DE3A`,
`0x0043DEE4`/`0x0043DEF8` and `0x0043E1CC`/`0x0043E1DA` (EXP-20260930-002).
Mask 0x01 is the game-complete bit that suppresses intro videos, and mask 0x02
is set when every level is perfect ([[PC FMV playback]]). LEVELDONE's medal sum
reads bytes 0–15 only.

## Every whole-byte medal read

A raw scan of every executable section for address operands `0x0059D8F8` and
`0x00572BF8` (and a second scan for fixed indexes `0x0059D8F9`–`0x0059D907`,
which found none) gives these sites. First recorded in EXP-20260930-003; the
three level-select reads were missed by that scan and added by
EXP-20261001-003.

| Site | Instruction | Role | Whole byte? |
|---|---|---|---|
| `0x00410140` | `mov dl,[eax+0059D8F8]` after `xor edx,edx` | InitMainGame snapshot to `0x00572BF8` | yes |
| `0x00415D44`/`70`/`9C` | load, then `and 2`/`and 4`/`and 1` | in-level medal markers | no, bitwise |
| `0x0041904D`, `0x00419123` | byte copies | save and load | copy |
| `0x0043D2F5` | `cmp byte [eax+0059D8F8],dl` (DL=7), loop over 16 | per-level "perfect" list, probably the movie clips menu | yes |
| `0x0043DCEE`, `0x0043DDEE` | `cmp byte [eax+0059D8F8],7` | LEVELDONE newly-perfect bonus | yes |
| `0x0043E18C` | `cmp byte [eax+0059D8F8],dl` (DL=7) | third LEVELDONE copy in the same function | yes |
| `0x0043DD1D`, `0x0043DE1D`, `0x0043E1BA` | `mov dl,[eax+0059D8F8]`; `add ecx,edx`; `cmp ecx,0x70` | "every level perfect" sum | yes |
| `0x0043DCF7`, `0x0043DDF7`, `0x0043E194` | `cmp [00572BF8],7`/`edx` | compare with the snapshot | via the snapshot |
| `0x00442F2C`… | `test`/`or` masks 1, 2 and 4 | results routine | no, bitwise |
| `0x00444231`, `0x00444267`, `0x00444298` | `mov al,[edi+0059D8F5]` | level-select medal table index | yes |

The Ghidra export decompiles only two of the three LEVELDONE copies inside
`0x0043DA40`; the raw scan found the third.

## Modification requirements

- **Spare medal bits need masked reads.** A build that stores anything in bits
  0x08–0x80 of a medal byte must mask every whole-byte read above with 7, or
  native medal behaviour changes. EXP-20260930-003 replaced each 6- or 7-byte
  instruction (one HIGHLOW fixup at offset 2) with a call into masking helpers.
  Patched and unpatched windows gave the same results for nine medal-byte
  patterns, slots 0, 3 and 15, at both bases. In hardware a Training byte of
  0x0F went on to the native save prompt. Without the three level-select
  masks, a level saved as 0xFA showed no medal at all on the select
  (EXP-20261001-001's load-arm capture).
- **Unmodified game with extra bits.** A save carrying extra medal bits,
  loaded by an unmodified executable, would make its whole-byte checks treat
  those levels as not perfect. Inferred, not run.
- **Extra data after the record.** The file format has room after the record:
  hooking the save's `fwrite` call `0x0049AC86`, the load's `fread` call
  `0x0049AA36` and the load copy at `0x0049B790` lets each slot carry an
  appended block (EXP-20261001-001). The original bytes at those sites are:

  | Site | Original | In |
  |---|---|---|
  | `0x0049AC86` | `call 004B05B0` (fwrite record, 0x21C, 1, file) | save `0x0049AB30` |
  | `0x0049AA36` | `call 004B1170` (fread record, 0x21C, 1, file) | load `0x0049A8E0` |
  | `0x0049B790` | `add esi,0x18; mov ecx,0x81`, before the copy over `0x004D8428` | save/load menu |
  | `0x00418FA0` | `mov ecx,[esp+4]; xor eax,eax` | defaults entry |

  Native windows `0x0049AC76`–`0x0049AC8E` (save), `0x0049AA26`–`0x0049AA3E`
  (load) and `0x0049B78E`–`0x0049B7A1` (install) were executed. In hardware
  the native menu saved an 804-byte slot (540 bytes plus an 8-byte header
  and 256 bytes), a fresh process loaded it back with the medal byte (0xFA)
  and the appended block intact, and the native list preview read the longer
  file. This also answers EXP-20260930-003's open question of whether an extra
  medal bit survives a save and reload.
- **Open.** The unmodified game loading an 804-byte save: it reads 540 bytes
  with one `fread`, so it should ignore the rest. Not run.
