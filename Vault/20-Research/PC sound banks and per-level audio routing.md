---
type: research
status: confirmed-bounded
created: 2026-10-29
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260910-004, EXP-20260911-002, EXP-20261005-001]
tags: [re/audio, re/static, re/runtime]
---

# PC sound banks and per-level audio routing

How the retail executable picks a sound bank for a level, how it builds and
loads sample paths, where its streamed tracks are chosen, and what file and
executable replacements must respect. First recorded in EXP-20260910-004 (not
in this vault), which executed the original x86 at image bases `0x00400000`
and `0x01000000` with Win32, device and file-loading calls as explicit stubs:
that is routing evidence, not listening evidence. Related notes:
[[FUNC-97C95BA5572D-0042BB90]] (streamed track table),
[[EXP-20260910-005 - Flik event voice mappings]] (voice cues) and
[[PC Mr Soil dialogue replacement]] (lesson speech).

## Sound banks

- **Bank choice.** `0x004A3310` selects a sound bank from the internal level
  index (`0x00861C84`).
- **Bank loading.** `0x0049E3E0` loads the common and per-bank sample paths
  through `0x0049DF90`; 23 banks were run.
- **Initial banks.** In carousel order the sixteen levels start with banks
  2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17. Training (engine 17)
  and Anthill (engine 1) both select bank 2.
- **Scene banks.** Other scene paths through `0x00419810` can request banks
  19–23. The per-level list is therefore a census of initial banks, not of
  every event or speaker.
- **Paths and the WAV loader.** `0x0049DF90` builds the path and calls the WAV
  loader `0x004AD950` through thunk `0x004011B8`. The loader allocates the
  data chunk's actual size before reading through `0x004AD280`. The addresses
  and an objdump of `0x0049DF90`/`0x0049E3E0` independently identify this as
  the sample path, separate from the streamed-track table.
- **Bank membership matters.** A sample that is not in the level's bank does
  not play: the request returns early (`0x0049D820`;
  [[EXP-20260910-005 - Flik event voice mappings]]).
  - Training's bank 2 omits sample 61 (`SFX/USGN083.WAV`, cue 76, "I need
    more grain"), which the hint dispatcher `0x00414EE0` handles. A build that
    wanted it in Training loaded `USGN083.WAV` through `0x0049DF90` at level
    reset before requesting it normally (EXP-20260911-002).
  - Sample 31, `WASPBUZZ.WAV`, is in banks 1–18 (EXP-20261005-001).

## Streamed tracks

- `0x0042BB90` fills the filename table at `0x00596528`, stride 8
  ([[FUNC-97C95BA5572D-0042BB90]]).
- The entry slice `0x0042E9B5`–`0x0042EA31` selects cues 0–14 for carousel
  positions 1–15. Position 0 (Training) skips looping background music, and
  the special branch at `0x0042EA15` requests cue 21. Both bases agree for the
  normal slice.
- Streamed music and lesson speech share one channel.

## Disc audio files

- The disc has 35 WAVs in `AUDIO` and 309 in `SFX`. Three SFX files are not
  referenced.
- **Formats.** Streamed files are 22050 Hz unsigned 8-bit, mono or stereo.
  Short clips are 22050 or 44100 Hz, unsigned 8-bit or signed 16-bit.
- **Names.** The US filenames identify voice assets only; the speakers are
  unverified.

## Replacing audio per level

- **Hook sites.** EXP-20260910-004 replaced two 7-byte instructions with calls
  that return another path pointer for the current level:
  - `0x0042BE8F` (`MOV EDX,[ESI*8+00596528]`), whose HIGHLOW relocation at
    RVA `0x2BE92` had to be retired;
  - `0x0049E033` (`MOV EDI,[ESP+120]`).
  The wrappers kept every other register, the flags and the stack. Each new
  file was written in the original's format, and the original `AUDIO` and
  `SFX` files stayed byte-identical.
- **Hardware.** On entering Anthill, the game streamed cue 0 from the
  replacement path `\pc\bugs\cd\studio\0001.wav`. Read-only samples showed the
  stream playing with advancing byte counts and six nonzero DirectSound buffer
  slots. That is allocation evidence, not proof of what was heard.
- **Open.** New audio events, bank budgets for large custom files, and
  listening coverage of every level remain open.

## Adding an executable section

A replacement like this needs code room. The retail PE header has its section
table at `0x178`, six sections and SizeOfHeaders `0x400` (read from retail
`bugs.exe` on 2026-10-29). Sixteen 40-byte headers end at `0x3F8`, so at most
sixteen sections fit without moving the first section's data. EXP-20260910-004
added a sixteenth header (ending at `0x3F8`) to a fifteen-section build; that
section sat at RVA `0xC85000` and the image grew to SizeOfImage `0xC86000`.
Once a build has sixteen sections, further code has to go into unused space in
existing sections, as EXP-20260911-002 did.
