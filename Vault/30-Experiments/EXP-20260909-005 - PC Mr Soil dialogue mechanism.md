---
type: experiment
id: EXP-20260909-005
date: 2026-09-09
question: How can Mr. Soil's spoken lessons be replaced in the Windows PC port?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Linux host; offline retail-x86 Unicorn emulation; local CPU ASR; ffmpeg
working_directory: /home/dev/ABLPC
configuration: No game launch, input, debugger or process-memory operation
artifacts:
  - reports/audio/EXP-20260909-005-native.json
  - reports/audio/EXP-20260909-005-encoding.json
addresses: ["0x0043C340", "0x004DC308", "0x0049D320", "0x0042BB90", "0x0042C9C0", "0x004AD280", "0x00440F50"]
result: PC file-replacement mechanism established; audible game acceptance remains open
tags: [re/experiment, re/audio]
---

# EXP-20260909-005 - PC Mr Soil dialogue mechanism

[[PC Mr Soil dialogue replacement]] owns the mechanism, cue/filename/topic
table, practical encoding recipe, contradiction correction and remaining test.
The bounded question was opened from PC-native EXP159, the verified retail
hash and `0x0042BB90`/`audio\less1.wav` before consulting the external PS1 source.

## Evidence and reproduction

```bash
.venv/bin/python scripts/probe-soil-audio.py
```

The probe hash-guards the retail copy, maps its original instructions with PE
relocations, and runs at `0x00400000` and `0x01000000`. Win32 logging,
critical-section, message and stream-open calls are stubbed. It verifies:

- 40 populated track slots and a null index40, including the seven previously
  missed register stores;
- 16 cue-to-path selections, IDs24..39, at each base;
- 14 initial tutorial-stage calls, each selecting `stage+24`;
- native WAV data reads for three synthetic lengths, exact bytes, exhausted
  count, end canaries and a subsequent zero-byte EOF read at each base;
- all14 PC lesson files' complete readable PCM payloads and exact hashes.

This is original-instruction emulation with host API stubs, **not a Wine run**.
The native reader receives a synthetic mmio buffer/descriptor; it does not test
Windows mmio parsing or DirectSound output. Both shorter and longer synthetic
WAVs were separately encoded/decoded by ffmpeg successfully. No claim of
audible timing, full Training completion, or arbitrary WAV-format support.

Private evidence under `work/experiments/EXP-20260909-005/`: three bounded
objdump extracts, native report, source ASR script and transcripts, claim-sweep
and environment receipts. ASR uses locally cached `base.en`, CPU int8, four
threads and no external upload. Full dialogue and game assets stay ignored.
Only topic summaries, metadata, source tools and evidence notes enter Git.

## Contradiction

EXP159 and its independent EXP160 audit missed register stores when counting
immediate stores. Fresh disassembly and native execution show **40 populated
track slots**, including DEAD and LESS13. The old claims are corrected at all
identified surfaces; the historical audit's mistake is explicitly retained as
a correction rather than silently presented as a new successful old audit.
PS1 archive/canon notes also disagree about extension status; the dated,
bounded 2s-to-4.5s test is cited in [[XPORT-20260909-010 - Training speech replacement]].

## Environment and limits

No launch, close, signal, gameplay input or live-memory action occurred. The
closing audit independently finds the previously recorded game26160 absent,
no private sinks, and two surviving prior-session processes: reaper26076 /
start672861 / group25922 and winedevice26114 / start672872. Both exactly match
the existing `live-handoff-binding.json`; they were left untouched. The audit
is non-clean, not an unknown ownership claim. Do not claim the old game remains
open. Its exit timing/cause was not observed.

Validation: native probe passes; two ffmpeg encode/decode arms pass. Repository
metadata gates and claim sweep are recorded in the session note. No broad
pytest/R2q suite or live-audio acceptance was run.
