---
type: experiment
id: EXP-20260816-159
date: 2026-08-16
question: 'Where does the PC audio subsystem live, and can a static census give the Subsystem Coverage Map real PC anchors for a row that had none?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static analysis; radare2 5.9.8; rabin2; repository Python 3.14
environment_version: radare2 5.9.8
working_directory: /home/dev/ABLPC
configuration: read-only disassembly, import-table and string reads, and a metadata-only disc listing from the exact retail work copy; no runtime process, debugger, or target write
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-audio-static-census.md
addresses:
  - "0x004A3480"
  - "0x0049DD00"
  - "0x0042BA60"
  - "0x0042BB90"
  - "0x0042F350"
  - "0x0042C3B0"
  - "0x004D81E8"
  - "0x0042C130"
  - "0x004AFEAE"
  - "0x004AFEB4"
  - "0x007EDAE8"
  - "0x007ECA40"
  - "0x00596528"
  - "0x00596960"
result: audio-row-bounded-after-audit-corrections-to-six-claims
created: 2026-08-16T21:30:00
updated: 2026-08-16T21:30:00
tags:
  - re/experiment
  - re/static
  - re/audio
  - research/coverage
---

# EXP-20260816-159 - PC audio subsystem static census

## Question

[[Subsystem Coverage Map]] lists audio as **Untouched**: no PC evidence
beyond the subsystem plausibly existing. This is the first packet chosen from
that map rather than from milestone momentum. Where does the PC audio
subsystem actually live, and what anchors can a purely static pass establish?

Audio was picked because it is the cheapest untouched row to open: the import
table was already exported by `EXP-20260811-003`, so the census starts from an
existing artifact and needs no runtime session.

This is bounded reconnaissance. It advances no milestone gate and claims no
subsystem model.

## Method

Offline only, on the exact retail work copy at hash
`97c95ba5...a27b878`: import table via `rabin2 -i`, strings via `rabin2 -z`,
disassembly via radare2, and direct byte decoding for call-site and
table extraction. Complete evidence is in
`static/exports/BIN-97c95ba5572dce63/SUBSYS-audio-static-census.md`.

Three structural facts made the census possible and are worth recording for
the next subsystem pass. **No DirectSound import has a direct
`call dword [IAT]` site** — they are reached through `jmp dword [IAT]` thunks
at `0x004AFEA8`-`0x004AFEB4`. **Module functions are called through the
`0x00401xxx` `jmp` thunk table**, not directly. And **some functions are
reached only through `.data` function-pointer records**, so resolving thunks
in both directions is still not sufficient; see the `0x004D81E8` record below.
A naive cross-reference search finds nothing in any of the three cases.

## Confirmed

Each item is a static fact with an address; none assigns behaviour beyond what
the instructions show.

- **DirectSound bring-up is `0x004A3480`**, reached via thunk `0x00401B95`
  from `0x00412CAB`, `0x00412DE5`, and `0x0042BAD0`. It clears two
  `0x300`-dword tables (`0x007EDF08`, `0x007ECE58`), enumerates devices with
  callback `0x0049DD00`, creates the object into `0x007EDAE8` using the GUID
  pointer at `0x007EDA60`, calls vtable `+0x18` with the window handle from
  `0x0059F73C` and argument 1, then sets `0x007ECA40` to 1 — a flag written
  only on success.
- **Audio and input are brought up together.** `0x0042BA60` calls the
  DirectSound initializer at `0x0042BAD0` and, at `0x0042BAED`, the function
  `0x0042F350` that holds the executable's only `DirectInputCreateA` call
  site (`0x0042F43D`).
- **A track-name table exists at `0x00596528`**, 8-byte stride, built by
  `0x0042BB90` (callers `0x0041A1FF`, `0x0049D35A`, `0x0049D41B`). Forty
  name pointers are written (corrected by EXP-20260909-005): indices 0-14 are `Level1a`-`Level5c` (five levels
  by a/b/c), 17-21 are `levcom`, `title`, `bugs2mb`, `bugs2ma`, `bugs2mc`, and
  24-36 are `less1`-`less12` including `less8a`. Indices15/16/22/23 are DEAD;
  indices37/38/39 are LESS13; index40 is null. Register stores were omitted
  in this original census; fresh disassembly and native replay correct it.
- **Track paths are assembled at `0x00596960`** from the literal
  `\pc\bugs\cd\` (`0x004E9070`) plus the selected `audio\NAME.wav`, and logged
  through `PLAYTRACK : Attempting to play track %s.` at `0x0042BEF6`. The disc
  layout `PC/BUGS/CD/AUDIO` matches, and that directory holds exactly 35
  `.WAV` files.
- **`DSStreamWndClass` appears exactly once, at a cleanup site.** Its single
  reference in the whole image is the `push` at `0x0042C3B0` feeding
  `UnregisterClassA`. No registration site referencing the string exists; if
  registration happens it goes through a structure field this census did not
  trace. That `push` lies inside the function beginning `0x0042C130` — the
  same DSStream token parser `EXP-20260816-143` recorded, not a separate
  function.
- **All 37 WINMM `mmio*` call sites lie in one contiguous region**,
  `0x004AD000`-`0x004ADB20`, including `mmioCreateChunk` and `mmioWrite`, so
  that region can author RIFF chunks and not only parse them.
- **Twelve audio-module functions** in `0x0042B000`-`0x0042C600` have an entry
  in the `0x00401xxx` thunk table; six have at least one direct call site and
  six have none. The three most-called are `0x0042B020` (34 sites, of which
  `0x0042B747` and `0x0042B781` are inside the module), `0x0042C0D0` (23) and
  `0x0042C110` (19).
- **`0x0042BA60` is reached indirectly**, through a `.data` record at
  `0x004D81E8`: a count of 3 followed by thunk pointers `0x00401B04`,
  `0x004011D1` and `0x00401299` (to `0x0042BA60`, `0x0042BB30`, `0x0042BB50`),
  followed by the string `"DIRECTX"`. It has zero direct call sites, so a
  direct-call-only census would show the packet's own central initializer as
  unreferenced.

## Inferred

That the `audio\*.wav` table is *music* rather than sound effects is
suggested by the names (`title`, `levcom`, per-level a/b/c) and by the
`SETMUSICVOL` log strings, but no instruction seen here distinguishes a music
path from an effects path. The naming stays address-based: `0x0042BB90` is
described as the track-table builder because it writes the table, not because
its purpose is established.

## Unknown

What `0x0042B020`, `0x0042C0D0`, and `0x0042C110` do, despite being the
module's busiest entry points; whether sound effects use a separate path;
what the track entry's second dword means; how DSStream buffers or streams
audio; selection of non-tutorial cues and extra LESS13 aliases; and audible
runtime behaviour. Later [[EXP-20260909-005 - PC Mr Soil dialogue mechanism]]
confirms the missing register stores, tutorial selection and bounded native
WAV data reads. This original census launched no process.

## Coverage effect

[[Subsystem Coverage Map]] changes in two rows:

- **Audio** moves from Untouched to **Bounded**, with the anchors above and a
  sharper open question than the row previously carried.
- **Input** is added as its own row at Touched with anchor `0x0042F350`.
  Folding input into "player movement and physics" was a condensation error
  in the map's first draft: `DINPUT.dll` is a distinct import surface on PC,
  and this census shows its creation path is a sibling of the audio one.

No other row changes, and no milestone status changes.

## Next discriminating question

The cheapest next step is static, not runtime: identify `0x0042B020`, whose 34
call sites make it the most-used audio entry point in the executable. If it
turns out to be a per-effect trigger, the effects path separates from music
and the row can be split; if it is a per-frame service, the module's shape is
different again. A runtime pass would then be justified, and read-only
sampling of `0x007ECA40` and `0x007EDAE8` after launch would confirm the
bring-up path executes as the static reading predicts.
