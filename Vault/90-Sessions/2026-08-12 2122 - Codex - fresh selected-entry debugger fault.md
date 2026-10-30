---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/dynamic
  - implementation/tooling
---

# Fresh selected-entry debugger fault

## Agent

Codex

## Goal

Execute roadmap packet M2.16 under the START HERE workflow using the preferred
windowed/muted pristine launcher, document the result throughout the Obsidian
Vault, and leave both runtime and Git state clean.

## Files inspected

- Required START HERE sequence, Project Charter, relevant MOCs, Roadmap,
  Environment Status, Runtime Tooling, capability-gap register, prior plant 10
  experiment, and both caller/callee function dossiers.
- Exact PC static chain `0x0044D79A -> 0x0044D7A4 -> 0x0040100A ->
  0x0044CA00` and schema-1 GDB signal-control loop.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-028 - Plant10 post-title selected-entry negative]]
- [[EXP-20260812-029 - Fresh selected-entry chain debugger fault]]

## Changes made

- Validated `scripts/play-pristine.sh --research --windowed --mute` by syntax,
  dry run, and live use. The accepted game used a 1280x960 Gamescope window;
  its live audio sink input was attached to a private null sink that unloaded
  at cleanup.
- Rejected one launcher preflight that entered software mode after renderer
  inputs were sent too close together. The accepted arm separated Down and
  Return and passed exact hardware Direct3D/no-software log gates.
- At the natural unchanged Training title, installed outer-gate and callee-
  entry hardware breakpoints plus both exact plant 10 `+0x2E` read watches in
  one fresh arm.
- Preserved the one gate snapshot, then rejected all caller/callee/data
  interpretation after raw GDB recorded `SIGSEGV` at `0x0044D79A`, schema 1
  continued it, and the game-only post-detach frame showed Wine's fatal-error
  dialog.
- Curated the structured run and game log. Raw GDB transcripts and game-only
  captures remain ignored under the experiment work directory.
- Updated the roadmap, current/environment state, known unknowns, decision
  log, capability/tooling notes, function dossiers, MOCs, experiment index,
  and Linux play baseline. M2.17 is now the active harness-safety packet.
- Stopped only exact resolved launcher/game/debugger/Gamescope PIDs. TERM
  required a final KILL for exact remaining Gamescope/reaper PIDs; the private
  sink unloaded and no scoped process remained.

## Conclusions

- **Confirmed:** Fresh simultaneous instrumentation reproduces KU-031 at
  `0x0044D79A`; the game does not survive normally.
- **Confirmed:** Harness cleanup/detach and `NextLife` are insufficient
  survival receipts when direct fatal-signal/process evidence contradicts
  them.
- **Static only:** Captured `AL == 0x40` would leave the following `jne`
  untaken and expose the call at `0x0044D7A4`.
- **Unknown:** The initial fault's root cause and every runtime consumer claim
  beyond the outer-gate snapshot.

## New hypotheses

The schema-1 broad signal continuation explains the false structured success,
but not the initial fault. A synthetic fatal-signal fixture plus safe live
control is the lowest-risk discriminator before another caller trace.

## Contradictions discovered

The structured run says `target_reached`, cleanup verified, and detached; the
log appends `NextLife`. Raw GDB records `SIGSEGV`, Wine starts winedbg, and the
game-only frame is a fatal-error dialog. The arm is therefore tooling-fault
evidence only.

## Tests run

- `bash -n scripts/play-pristine.sh`.
- Windowed/muted research dry run and live renderer/audio-routing gates.
- `RUN-GDB-20260812-211649`: one outer-gate stop, reproduced fatal signal,
  rejected caller-chain result.
- Scoped process and PipeWire sink cleanup checks.
- `make check`: Python smoke imports, Vault lint (131 notes, zero errors or
  warnings), 119 tests, and tracked-file audit (zero violations) all passed.
- `git diff --check`: passed.

## Unresolved questions

- Can GDB detach safely from a synthetic unexpected fatal-signal stop without
  delivering or masking the signal?
- Which signals must be terminal versus explicitly allowlisted as normal Wine
  signaling?
- After fixture proof, does a previously safe game watchpoint retain normal
  survival under the new behavior?

## Recommended next action

Execute [[Project Roadmap#M2.17 — Unexpected-signal-safe debugger control]].
Implement and test the fatal-signal terminal record and independent survival
receipt on a synthetic fixture, then revalidate a known-safe live watchpoint.
Do not return to `0x0044D79A` until both gates pass.

## Git commit if applicable

Bounded commit message: `research: reproduce selected-entry debugger fault`.
