---
type: research
status: active
created: 2026-09-27
updated: 2026-09-27
evidence: [EXP-20260812-005, EXP-20260812-014]
addresses: ["0x00403B90", "0x004ED2A0", "0x0055C784", "0x004132E0", "0x004133B0", "0x00412F20", "0x004129A0", "0x0049BEA0", "0x0049BBF0", "0x0049BD20", "0x0042E5C0", "0x0043DA40"]
tags: [research/fmv, re/static]
---

# PC FMV playback

Static diagnosis for "level FMVs do not play when entering levels from the
original level select" (2026-09-27). No runtime launch was made for this note.

## Why the videos are skipped

**Confirmed (static, two routes):** the command-line word `mpeg` turns FMV **off**.
`00403B90` tokenizes the command line (`" -"` separators) and compares each word:
`cheat` → `005A923C=1`, `log` → `008620AC=1`, `mpeg` → `004ED2A0=1` and logs
`ONEINIT : Mpeg play OFF.`, `high` → `0055C784=1` and logs
`ONEINIT : Hi quality mpeg playing ON.` Both video entry points skip the
player when `004ED2A0` is nonzero: `004132E0` (every in-game cutscene request)
and the FMV-options loop `004133B0`.

**Confirmed (runtime logs):** all 692 retained `bugs.log` files under
`dynamic/wine/` contain `ONEINIT : Mpeg play OFF.` and none contains the
`high` line. The project launchers pass the word:
`scripts/play-pristine.sh` uses `mpeg` for ordinary play and `log cheat mpeg`
for research; the September 26 woodland preview recorded
`bugs.exe log cheat mpeg --classic-level-select`. The word dates back to the
first Wine baseline ([[EXP-20260812-005 - Wine training baseline]]); no note
records a Wine playback failure that motivated it.

## When the original game plays a level video

`00412F20` maps a video index to `CD\TEMP\*.BUG`: 0 `tt_logo`, 1 `disney`,
2 `ad`, 0x0A..0x29 `LEV_1A`..`LEV_15D` (0x10 is `LEV_5A` and 0x12 is `LEV_4A`,
swapped relative to their neighbours), 0x2A..0x2C `ALT_1..3`, 0x2D `INTRO-1`,
0x2E `LOSE`. The per-position tables are `004D8337` (before: 0, 0x0A, 0x0C ..
0x26) and `004DC68F` (after: 0, 0x0B, 0x0D .. 0x27).

- **Before a level:** `0042E5C0` plays `004D8337[carousel position]` only when
  `00599B1C == 0`, the special-stage flag `004F0680 == 0`, the selected
  position equals the progress position `0059D8E4`, and game-complete bit 0 of
  `0059D908` is clear. Replaying an already-passed level from the level select
  therefore shows no intro, even with FMV enabled.
- **After a level:** `0043DA40` plays `004DC68F[position]` on level-done
  results 1 or 5 when the level's status byte `0059D8F8[position]` is 7 and
  `00572BF8 != 7`; it also plays index 0x29 when all sixteen status bytes sum
  to 0x70, 0x28 at game completion and 0x2E at game over. Finishing the
  engine-16 special stage plays `0059D90A + 0x29` (the `ALT_*` videos).
- **Start-up:** `0043DA40` requests indices 1, 0 and 0x2D (`disney`, `tt_logo`,
  `INTRO-1`) before the menu, so those also stay silent under `mpeg`.

## Player and format

`004129A0` builds `cd\temp\<name>` and calls `0049BEA0`. That uses DirectShow
multimedia streaming: `CoCreateInstance(CLSID_AMMultiMediaStream)` at `0049BBF0`,
`AddMediaStream` for `MSPID_PrimaryVideo` into the DirectDraw object and
`MSPID_PrimaryAudio` with its default renderer, `OpenFile`, then an
`IDirectDrawMediaStream` sample `Update` loop in `0049BD20` (GUIDs at
`0x004C0170..0x004C01B0`). `.BUG` files are MPEG-1 system streams: `LEV_1A.BUG`
probes as `mpeg1video` 352×288 with `mp2` audio, 14.04 s.

## Unknown

Whether Wine 11's `amstream`/`quartz` with `winegstreamer` plays these streams
correctly in this game. The host has the WoW64 32-bit DLLs and GStreamer
`mpegpsdemux`, `mpeg2dec`, `mpg123audiodec` and `avdec_mp2float`. The
discriminator is one launch without `mpeg` that enters the next unplayed level
(or starts a new game), looking for the video and checking `bugs.log` for the
absence of `Mpeg play OFF`.
