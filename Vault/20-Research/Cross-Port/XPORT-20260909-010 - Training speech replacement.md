---
type: cross-port-comparison
id: XPORT-20260909-010
created: 2026-09-09
updated: 2026-10-02
status: bounded
tags: [research/cross-port, re/audio]
---

# XPORT-20260909-010 - Training speech replacement

Question: does the PS1 Mr. Soil replacement suggest how the PC stores/selects
the same Training speech? PC-native gate: retail SHA
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`, EXP159
audio census, `0x0042BB90`, track table `0x00596528`, `audio\less1.wav`.
Unknown at entry: whether those PC files are Soil and whether replacement
length is fixed outside the file. Verify against PC disassembly and files.

SRC-PS1-ABL remained external/read-only. HEAD is still
`1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`; dirty working-tree content was not
used as evidence. Committed blobs consulted through `git show`:

- `ObsidianVault/Canon/Systems/SYS_xa_voice_streaming.md`, `0x80046828` and
  its dated 2026-07-04 extension observation;
- `ObsidianVault/Archive/Unsorted Legacy/Plan_-_Longer_XA_voice_lines.md`,
  verification section: AUDIO5 channel0 EOF sector344 moved to672;
- `ObsidianVault/Archive/Superseded/Findings_Finding_-_SFX_replacement.md`,
  Training NPC and XA sections, for discovery/history only.

**PS1 source reports:** Training speech uses AUDIO4/5 XA channels. An AUDIO5
channel0 extension from approximately2s to4.5s was heard and traced beyond the
old EOF; extension converts existing gap8 data slots and moves EOF. An older
archive says the extension is merely planned; the canon source also retains
an older plan paragraph. Preserve this chronology conflict: only the explicit
dated size-preserving test is used, not a claim of unrestricted XA re-mux.

**Cross-port inferred:** the ports retain comparable lesson concepts and
streamed cue selection. No binary/table identity follows from that similarity.

**PC confirmed independently:** fourteen PCM WAVs, cues24..37 in the initial
tutorial, with additional aliases38/39 to LESS13. WAV `data` size controls the
native reader. PC has mono/stereo22050Hz8-bit recordings, not a PS1 XA sector
layout. [[EXP-20260909-005 - PC Mr Soil dialogue mechanism]] supplies hashes,
instructions and emulated original-code results. No PS1 artifacts were copied.

**Unknown:** audible PC replacement acceptance and live longer-line behavior.
Discriminator: fresh full PC game copy with a4.5s LESS8A tone; capture playback
while withholding its completion action, then separately test interruption.

2026-10-02 audit pointer: audible acceptance is answered for the first line.
EXP-20260909-007 built the
replacement and the user approved playback. Live timing of a longer line is
still unknown, and the user accepts normal interruptions
([[PC Mr Soil dialogue replacement]]). Both results are PC evidence only.
