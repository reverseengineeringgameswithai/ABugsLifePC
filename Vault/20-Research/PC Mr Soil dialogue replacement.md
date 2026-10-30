---
type: research
status: bounded
created: 2026-09-09
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260909-005]
tags: [re/audio, modding/dialogue]
---

# PC Mr Soil dialogue replacement

## Mechanism

**PC confirmed:** Mr. Soil's Training lessons are standalone PCM WAVs in
`PC/BUGS/CD/AUDIO/`, selected by the native tutorial dispatcher. Replace the
appropriate `LESS*.WAV` in a fresh derived game's content tree, retaining its
filename. The selection and WAV reader require no executable patch or fixed
original file size. [[EXP-20260909-005 - PC Mr Soil dialogue mechanism]] combines
retail disassembly, actual PC file metadata/content and original-x86 emulation.
EXP-20260909-007 installed a replaced `LESS1.WAV` (11.52s, 22050Hz 8-bit stereo
PCM) in a derived copy; the launch's LESS1 content-path log request passed and
initial listening confirmed playback.

Use the content tree the game actually resolves through its configured content
drive. In the bounded native experiment, the assembled path is
`R:\pc\bugs\cd\audio\less1.wav`; editing a different installation's AUDIO
directory will not affect that path. Original `bugs.exe` SHA is above; derived
mod executables are not automatically covered by this exact-binary experiment.

## Which file

Stage is zero-based. Topic labels summarize local ASR of the actual PC files;
they are identification aids, not an exact transcript or independent voice-ID
measurement. Cue/file mappings are verified by executing the retail instructions
at both image bases. Metadata and all fourteen source hashes are in
`reports/audio/EXP-20260909-005-native.json`.

| Stage | Cue | Filename | Topic | Seconds | Channels |
|---:|---:|---|---|---:|---:|
| 0 | 24 | LESS1.WAV | Welcome; berry throw | 15.141 | 2 |
| 1 | 25 | LESS2.WAV | Jumping | 11.544 | 1 |
| 2 | 26 | LESS3.WAV | Abdomen bounce | 10.339 | 1 |
| 3 | 27 | LESS4.WAV | Pick up and drop seeds | 22.242 | 1 |
| 4 | 28 | LESS5.WAV | Fixed seed; crack with bounce | 10.156 | 1 |
| 5 | 29 | LESS6.WAV | Uproot and discard a plant | 7.268 | 1 |
| 6 | 30 | LESS7.WAV | Plant tokens | 16.617 | 1 |
| 7 | 31 | LESS8.WAV | Change seed color | 4.906 | 1 |
| 8 | 32 | LESS8A.WAV | Crack the seed | 2.297 | 1 |
| 9 | 33 | LESS9.WAV | Find another green token | 3.499 | 1 |
| 10 | 34 | LESS10.WAV | Grow a green mushroom | 9.872 | 2 |
| 11 | 35 | LESS11.WAV | Mushroom to leaf to ledge | 7.094 | 2 |
| 12 | 36 | LESS12.WAV | Grain, health, letters and secrets | 20.285 | 1 |
| 13 | 37 | LESS13.WAV | Berry strengths and abilities | 26.674 | 1 |

Cues 38 and 39 also resolve to `LESS13.WAV`, but the initial tutorial-stage
table contains only cues 24 through 37. Do not claim sixteen distinct PC WAVs.
The final-stage repeat branch alternates table entries at `0x004DC320` and
`0x004DC322` (cues 36/37), per `0x0043C940` onward. That repeat branch has static
evidence only in this packet; the native stage probe covers initial dispatch.

## Prepare a replacement

All originals are **RIFF/WAVE, format tag 1, unsigned 8-bit PCM, 22050 Hz**.
Match the original channel count from the table. Example for the first line:

```bash
mkdir -p work/copies/soil-dialogue-overlay/PC/BUGS/CD/AUDIO
ffmpeg -nostdin -n -i /path/to/my-recording.wav -ar 22050 -ac 2 \
  -c:a pcm_u8 -map_metadata -1 \
  work/copies/soil-dialogue-overlay/PC/BUGS/CD/AUDIO/LESS1.WAV
```

Use `-ac 1` for a mono entry. This directory is an **audio overlay**, not a
complete bootable game. Copy the resulting file over that same relative path
in a fresh full game copy under `work/copies/`, and point the launch's content
drive at that full copy. Retain the original as rollback. Do not edit
`originals/` to test it. Restart/re-enter Training in the fresh
copy so a previously opened stream cannot retain the old file.

`ffmpeg -n` refuses an existing output. It authors valid WAV chunk sizes and
does not truncate to the old duration. This recipe creates a new PCM file; it
does not claim to retain proprietary metadata from an original recording.

Two synthetic examples are prepared at
`work/copies/EXP-20260909-005-soil-audio-overlay/`: stereo `LESS1.WAV`, 1.25 s at
880 Hz, and mono `LESS8A.WAV`, 4.5 s at 660 Hz (longer than its 2.297 s control).
Both decode successfully; hashes are in
`reports/audio/EXP-20260909-005-encoding.json`. Neither was installed in a live
game, nor is either intended as final dialogue.

## Playback and length evidence

Later [[PC Mr Soil lesson triggers]] maps all14 native lesson goals.
EXP-20260910-002 identifies the worker's native size-minus-refill-block stop
allowance at004412CC. Its live all-auto original-WAV sequence
reaches terminal13; stages0–8 have detailed full-drain/tail samples. This refines
the earlier broad “terminates using stream progress” description below.
It does not yet establish longer replacement-WAV live timing.

- Tutorial dispatcher `0x0043C340` reads a signed 16-bit cue from
  `0x004DC308 + 2*stage` (file `0xDAF08`). Fourteen initial native calls produce
  cues 24..37. Thunk `0x00401A87` reaches `0x0049D320`, which calls
  `0x0042BB90(cue, 0)` through `0x00401DBB`: zero selects non-looping playback.
- `0x0042BB90` builds the name table at `0x00596528`, assembles the path at
  `0x00596960`, and calls stream setup `0x0042C9C0` through `0x004015B9`.
- `0x0042C9C0` requires WAV format tag 1 and passes its format to DirectSound.
  `0x004AD230` locates the `data` chunk via `mmioDescend`; `0x004AD280` limits
  each read to the chunk's remaining byte count and decrements that count
  (`0x004AD29D`..`0x004AD2B4`). Original-x86 probes read synthetic 997-, 2049-
  and 65539-byte payloads exactly at both bases, preserve end canaries, and
  return zero on the subsequent EOF read.
- Refill/termination is in `0x0042CC60` and `0x00440F50`; non-looping EOF pads
  silence and terminates using stream progress. There is no original-lesson
  duration constant in the traced read path.
- **Gameplay can interrupt a longer recording.** When a lesson's action
  condition completes, `0x0043C901` calls stop thunk `0x004015C3`, then advances
  the stage. This is distinct from the WAV reader accepting a larger payload.
  Maximum practical duration and complete live timing for longer replacement
  recordings remain unknown.

## Cross-port comparison and correction

[[XPORT-20260909-010 - Training speech replacement]] pins PS1 commit
`1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`. The PS1 mechanism uses interleaved XA
channels in AUDIO4/5 and moves EOF to extend a voice. PC independently uses
individual PCM WAVs; PS1 sectors and offsets are not PC patch instructions.

EXP-159/160 omitted register-based table stores. **40 populated track slots**
exist, indices 0..39: `dead.wav` at 15/16/22/23, and `less13.wav` at 37/38/39.
Index40 is explicitly null. Stores `0x0042BBAF`..`0x0042BBBE` and
`0x0042BDF8`/`0x0042BE08`/`0x0042BE13`, plus native execution, establish the
correction. Both old evidence notes and the function dossier now record it.

## Next discriminating experiment

*Update (2026-10-02 audit):* partly overtaken.
EXP-20260911-001 played four
replacement recordings (10.44–14.64 s) live in hardware under a file-built
speech-completion policy, each draining fully before a configured 2 s tail
(measured ~2 s). No cited note records the synthetic-overlay run below
or its interruption arm with a longer replacement.

Use a fresh full copy with the synthetic overlay, audited launch and actual
content-path log. In Training, listen to the first-line tone, then reach
`LESS8A` and wait without completing its action: capture its full 4.5 s.
Separately complete the action while it speaks to test interruption. Restore
the original file in another fresh control. No live memory write is needed.
