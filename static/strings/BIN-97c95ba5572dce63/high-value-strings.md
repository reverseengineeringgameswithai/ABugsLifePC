# High-value PC strings

## Subject

- Binary: `BIN-97c95ba5572dce63`
- SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Source: Ghidra string/data references from `EXP-20260811-003`

Priority means useful for locating PC-native behavior. It does not assign a final semantic name.

## P0: Disc and installation behavior

| Address | String | Why it matters |
|---:|---|---|
| `0x004C47C8` | `Please insert A Bug's Life CD.` | Direct lead for media-presence failure behavior |
| `0x004C47F0` | `A Bug's Life` | Adjacent title/dialog context |
| `0x004C4800` | `cd.txt` | Candidate sentinel/configuration filename; purpose unknown |
| `0x004E9071` | `pc\bugs\cd\` | Referenced by `0x004129A0` and `0x004AE240` path construction |
| `0x004C60C8` | `\cd\temp\` | Referenced by `0x004129A0`; runtime choice remains unknown |

## P0: General file loading

| Address | String | Cross-reference |
|---:|---|---|
| `0x004E93AC` | `LOAD : Loading file %s.\n` | `0x004AE240` |
| `0x004E9398` | `fseek(fin,0,2)` | `0x004AE240` error path |
| `0x004E9350` | `fseek(fin,0,0)` | `0x004AE240` error path |
| `0x004E9340` | `fclose(fin)` | `0x004AE240` error path |
| `0x004E9300` | `FATAL ERROR - Failed to load file %s - error was %s.\n` | `0x004AE240` |

Together with the decompiled call sequence, these strings support a high-confidence file-into-caller-buffer hypothesis. They do not yet prove how path roots are selected.

## P0: Level-family paths

Function `0x004671D0` references:

- `.\level` at `0x004DE5A9`
- `level.dat` at `0x004DE5E4`
- `level1.dat` at `0x004DE5B4`
- `level2.dat` at `0x004DE5C4`
- `level3.dat` at `0x004DE5D4`
- `level.raw` at `0x004DE620`
- `level1.raw` at `0x004DE5F0`
- `level2.raw` at `0x004DE600`
- `level3.raw` at `0x004DE610`

The function calls `0x004AE240`, but the record layout and meaning of each file remain unknown.

## P0: DirectDraw and Direct3D setup

Function `0x0041F990` references diagnostics including:

- `BEGIN EXAMINE MACHINE`
- `DirectDrawEnumerateA(ExamineDDEnumCallback, 0)`
- `BEGIN SELECT DRIVERS`
- `INFO No available DirectDraw devices.`
- `INFO No available Direct3D devices.`
- `INFO Direct3D - Searching for hardware RGB driver.`
- `INFO Direct3D - Using software renderer.`
- `INFO Screen mode %dx%dx%d selected.`

Function `0x00411D00` references diagnostics for `DirectDrawCreate`, `QueryInterface(IID_IDirectDraw2)`, `SetCooperativeLevel`, `SetDisplayMode`, front/back surfaces, and resolution dimensions.

Function `0x00423A20` references diagnostics for system/video memory selection, DirectDraw and Direct3D interface acquisition, fullscreen/windowed cooperative levels, display mode, surface creation, device creation, texture-format enumeration, and viewport setup.

These embedded operation names are strong static evidence for the calls made. Runtime success, selected modes, and actual device identities are still unknown.

## P1: Content path leads

| Address | String |
|---:|---|
| `0x004C5798` | `rand.dat` |
| `0x004C7948` | `PAD\PATH00.BIN` |
| `0x004C7958` | `CD\PAD\PATH00.BIN` |
| `0x004C7970` | `CREAT\CREAT00.BIN` |
| `0x004C63D8` | `disney.bug` |

These are search anchors only. The format and purpose of each file are unknown.

## P1: Build provenance

- `0x004C545C`: `E:\pc\BUGS\bugs.cpp`

This confirms that a build-path string was embedded in this executable. It may help separate game code from runtime code, but it does not prove the original source tree structure beyond the literal string.

## Lower priority noise

Compiler/runtime messages, generic Windows error text, and library diagnostics are useful for identifying statically linked support code but should not be treated as game semantics. Repeated appearance of a plausible word is not confirmation.

## Runtime resolution of the CD-dialog strings

`EXP-20260811-004` mapped all three adjacent strings to `0x00403B90`:

- `cd.txt` is passed to `0x004AE240`.
- A zero return displays `Please insert A Bug's Life CD.` with title `A Bug's Life`.
- Under Wine at disc root, the game logged failed path `R:\\cd\cd.txt`.
- Under the derived `PC\BUGS` layout, the unchanged executable loaded `R:\PC\BUGS\CD\CD.TXT` and continued.

The sentinel's contents and semantics remain unknown.
