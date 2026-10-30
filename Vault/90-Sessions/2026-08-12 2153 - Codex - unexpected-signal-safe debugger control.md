---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/dynamic
  - implementation/tooling
---

# Unexpected-signal-safe debugger control

## Agent

Codex

## Goal

Execute roadmap packet M2.17 under the START HERE workflow, harden fatal-signal
and post-detach acceptance behavior, validate it on synthetic fixtures and a
previously safe hardware-rendered game watch, document the result in the
Obsidian Vault, and leave runtime and Git state clean.

## Files inspected

- Full required START HERE sequence, Project Charter, relevant MOCs, Roadmap,
  Environment Status, Runtime Tooling, capability-gap register, KU-031, and the
  prior M2.16 experiment/static export.
- `scripts/evidence_lib.py`, `scripts/gdb-harness.py`, and their complete test
  modules before modification.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-029 - Fresh selected-entry chain debugger fault]]
- [[EXP-20260812-030 - Unexpected-signal-safe GDB control]]

## Changes made

- Upgraded `gdb-harness` to 1.1.0/result schema 2 while preserving strict
  watch-spec schema 1 compatibility.
- Added schema-2 bounded survival configuration, repeated post-detach ownership,
  process-state, and `TracerPid` sampling, and fail-closed acceptance when a
  required receipt fails.
- Made fatal target signals structured terminal results with signal/PC and
  `nopass`; preserved explicit routine Wine `SIGUSR1/SIGUSR2` pass-through and
  made signal inspection precede a concurrent log milestone.
- Added a trigger-controlled synthetic `SIGSEGV` fixture, safe-detach/liveness
  assertions, schema compatibility/validation coverage, required-failure logic,
  and a real exited-process receipt negative.
- Rejected one live preflight after its complete log proved software rendering.
  Relaunched with `scripts/play-pristine.sh --research --windowed --mute`, sent
  separately timed Down/Return events only to the isolated game window, and
  required exact 640x480x16 Direct3D markers with no `INITSOFTRENDER`.
- Ran safe live `RUN-GDB-20260812-214545` on exact plant slot `0x005B1AA4`.
  It reproduced the prior four PCs/values, detached cleanly, and passed five
  independent resumed/untraced samples plus a later live game-only frame.
- Curated structured metadata and the accepted game log. Raw GDB transcripts
  and every game-only screenshot remain ignored under
  `work/copies/EXP-20260812-030/evidence/`; no whole-screen capture was taken.
- Stopped only the resolved launcher/game/Gamescope process trees. A final
  process audit found rejected-preflight `gamescopereaper` PID 2555302 and its
  `winedevice.exe` child 2555340 still sleeping after the game had exited; their
  exact rejected-run command lines were re-verified, TERM then final KILL
  removed them. The private sinks, game, debugger, and scoped wrappers are gone.
- Updated the roadmap, current/environment state, KU-031, decision log,
  capability/tooling notes, MOCs, experiment index, and session index. M2.18 is
  now the exact next packet.

## Conclusions

- **Confirmed:** A synthetic fatal target signal can no longer be blindly
  continued or hidden by a simultaneous log milestone; it is a structured,
  tool-negative endpoint with signal and PC.
- **Confirmed:** `stop print nopass`, point deletion, and detach preserve the
  deliberately injected fixture, which is independently resumed/untraced.
- **Confirmed:** Required survival failure cannot produce an accepted run;
  routine Wine-style signals and schema-1 specs remain compatible.
- **Confirmed:** The prior safe live plant-slot watch retains the exact
  four-stop/value behavior and normal post-detach gameplay under schema 2.
- **Unknown:** Why hardware-breakpoint continuation at exact `0x0044D79A`
  faults. M2.17 does not promote caller/callee/data semantics or declare that
  address safe.

## Contradictions and negative results

The first live preflight reached `INITSOFTRENDER` and was rejected. The accepted
hardware arm has no contradiction: structured status, exact prior stop values,
five `/proc` samples, complete log, and the later isolated gameplay frame agree.
The rejected preflight also left a wrapper/device process after its earlier
cleanup; the final exact-PID audit found and removed both without affecting the
accepted run or repository evidence.

## Tests run

- Focused evidence/harness suite: 59 passed.
- Final `make check`: Python smoke imports, Vault lint (133 notes, zero errors
  or warnings), 130 tests, and tracked-file audit (zero violations) passed.
- `git diff --check`: passed.
- Scoped game/debugger/process and private PipeWire sink cleanup checks passed.

## Recommended next action

Execute [[Project Roadmap#M2.18 — Adjacent caller-gate continuation discriminator]].
Use separate fresh schema-2 hardware runs at adjacent same-path `0x0044D794`
and, only after adjacent survival, exact `0x0044D79A`. End either arm at the
first `target_signal`; require an independent receipt and do not combine
consumer interpretation into the discriminator.

## Git commit if applicable

Bounded commit message: `tooling: harden gdb signal handling`.
