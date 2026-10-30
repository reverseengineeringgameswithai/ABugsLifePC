---
type: session
date: 2026-09-27
agent: Claude
status: complete
tags:
  - session
---

# Diagnose missing level FMVs

## Agent

Claude (Opus 5.5) in Claude Code.

## Goal

The user asked why the FMV files do not play when a level is entered from the
original level select.

## Files inspected

Ghidra exports for `00403B90`, `004132E0`, `004133B0`, `00412F20`, `004129A0`,
`0049BEA0`, `0049BBF0`, `0049BD20`, `0042E5C0`, `0043DA40`; retained `bugs.log`
files; `scripts/play-pristine.sh`; the September 26 preview command line;
`CD/TEMP/*.BUG` headers; host Wine/GStreamer packages.

## Experiments inspected

[[EXP-20260812-005 - Wine training baseline]], [[EXP-20260812-014 - PC content census and loader context]].

## Changes made

New [[PC FMV playback]]; updated [[Subsystem Coverage Map]], [[Known Unknowns]]
and [[Wine Linux Play Baseline]]. No code, launcher or game file changed.

## Conclusions

The launch word `mpeg` disables all FMV (`004ED2A0`), and every project launch
passes it. Separately, the original game plays a level intro only for the next
unplayed level.

## New hypotheses

Wine's `amstream` plus `winegstreamer` can play the MPEG-1 `.BUG` streams once
`mpeg` is dropped (host decoders are present; untested).

## Contradictions discovered

The launch word's name suggests enabling MPEG; the code disables playback.

## Tests run

Static analysis only; Vault lint 0 errors. No game launched.

## Unresolved questions

See [[Known Unknowns#Level FMV playback]].

## Recommended next action

With user approval, launch once without `mpeg` and enter the next unplayed
level (or start a new game) to confirm playback under Wine; then decide whether
`play-pristine.sh` and preview launches should drop `mpeg`.

## Git commit if applicable

Committed with this note.
