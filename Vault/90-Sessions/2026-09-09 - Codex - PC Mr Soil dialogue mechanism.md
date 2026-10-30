---
type: session
date: 2026-09-09
agent: Codex
status: completed
tags: [session/research, re/audio]
---

# 2026-09-09 - Codex - PC Mr Soil dialogue mechanism

User asked for the PC equivalent of the Mr. Soil line replacement discovered
in the external PS1 project. [[PC Mr Soil dialogue replacement]] is the usable
handoff, with a14-file cue/topic/format table and ffmpeg replacement recipe.

[[EXP-20260909-005 - PC Mr Soil dialogue mechanism]] confirms initial tutorial
stages0..13 select cues24..37, standalone22050Hz8-bit PCM WAVs under
`PC/BUGS/CD/AUDIO`. The native reader consumes the WAV data chunk's declared
length; lesson completion can separately stop speech. Longer content needs no
original-size matching in this read path. Audible replacement and live longer
dialogue behavior remain untested.

Read the required orientation/current handoffs and applicable policy, charter,
MOC/audio notes, plus bounded roadmap/decision/unknown sections. PC-native gate
used the exact retail hash and EXP159 before PS1 comparison. Consulted committed
PS1 blobs at1186eb6 only, recorded in
[[XPORT-20260909-010 - Training speech replacement]]. No external-tree mutation
or artifact copying; full local ASR transcripts and game assets remain ignored.

Original-instruction replay at bases00400000/01000000 passes32 filename
selections,28 initial tutorial calls and6 synthetic reader arms with exact
bytes, end canaries and subsequent EOF. All14 original PC WAV payloads read
completely. Short stereo LESS1 and extended4.5s mono LESS8A tone encoding and
ffmpeg decode pass. Overlay is prepared only, not a full bootable game or live
change. Reports: `reports/audio/EXP-20260909-005-native.json` and
`reports/audio/EXP-20260909-005-encoding.json`; reproducible probe:
`scripts/probe-soil-audio.py`.

Corrected an old census error: **40 populated track slots**, including DEAD at
15/16/22/23 and LESS13 at37/38/39, plus null40. Register stores were missed by
both EXP159 and its EXP160 audit. Updated census, both notes, function dossier,
function index and current memory; the old audit failure is explicitly retained.
Claim sweep checks the old/new wording and targeted searches check synonyms.

Validation: native and encoding probes pass; Python environment, Vault lint,
M4 compatibility, tracked-file audit and whitespace checks pass after creating
this session note. Vault retains8 existing warnings. Initial lint caught the
then-missing session-note link and was rerun after completion. No broad pytest,
full make check, R2q or Git commit. Hooks were already installed.

No game launch/close/input/signal/live-memory operation. Read-only closing
audit observes game26160 absent, no private sinks, two exact old helpers
reaper26076/start672861/group25922 and winedevice26114/start672872. Both match
the old immutable binding and were left untouched. Game exit cause/time is
unknown. [[Environment Status#Current runtime handoff]] now owns that updated
observation instead of claiming the old game is open. Banked mod files and
Blender were not changed by the audio research.

Next test is a fresh full-copy Training run with the synthetic audio overlay:
check actual content path and audible first cue, then full4.5s LESS8A with its
action withheld, and a separate action-interruption arm. Account for inherited
helpers before launching. No live memory write is needed. This is follow-up
acceptance of the established mechanism, not completed runtime evidence.
