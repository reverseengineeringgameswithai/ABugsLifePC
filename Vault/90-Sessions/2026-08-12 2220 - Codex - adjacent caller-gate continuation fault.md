---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/dynamic
  - re/resources
---

# Adjacent caller-gate continuation fault

## Agent

Codex

## Goal

Execute roadmap packet M2.18 under the START HERE workflow, check whether the
fresh caller-gate continuation fault is confined to exact `0x0044D79A`, keep
the work aligned with M2's resource-to-rendered outcome, document the result in
the Obsidian Vault, and leave runtime and Git state clean.

## Files inspected

- Full required START HERE sequence, Project Charter, Roadmap, Current and
  Environment State, operating manual, relevant MOCs, Runtime Tooling,
  capability-gap register, KU-031, and prior M2.15–M2.17 experiments/static
  exports.
- `scripts/play-pristine.sh` and the GDB harness control loop used by the
  bounded schema-2 arm.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-028 - Plant10 post-title selected-entry negative]]
- [[EXP-20260812-029 - Fresh selected-entry chain debugger fault]]
- [[EXP-20260812-030 - Unexpected-signal-safe GDB control]]
- [[EXP-20260812-031 - Adjacent caller-gate continuation fault]]

## Changes made

- Rejected an initial preflight after its complete log proved software
  rendering; no debugger was attached to that preflight.
- Relaunched with `scripts/play-pristine.sh --research --windowed --mute`, sent
  Down and Return separately only to the isolated game window, and required
  exact 640x480x16 Direct3D markers with no `INITSOFTRENDER`.
- Selected unchanged Training, retained game-only selector/title frames, and
  attached schema-2 `RUN-GDB-20260812-221224` at the natural title with only
  hardware execution breakpoint `0x0044D794`.
- The arm stopped once at `0x0044D794`, captured exact registers/globals/plant
  slot, then received structured same-PC `SIGSEGV`. It correctly rejected the
  arm, deleted its point, detached, and recorded five resumed/untraced samples.
- Captured and visually checked a later 640×480 isolated game-surface frame
  showing live Training gameplay. No desktop or whole-screen capture occurred.
  All PNGs and raw GDB transcripts remain ignored under
  `work/copies/EXP-20260812-031/evidence/`.
- Honored M2.18's stop rule and did not run the conditional fresh exact-address
  arm. Curated the structured run/log and created a reviewable static boundary.
- Stopped only the resolved game/run tree. The wrapper and one Wine device
  process did not exit after bounded TERM waits, so their verified exact PIDs
  were killed and the private sink module was explicitly unloaded. Final
  process/sink audits were clean.
- Updated the roadmap, current/environment state, KU-031, decision log,
  capability/tooling notes, MOCs, experiment index, and session index. M2.19
  now returns directly to the missing visible plant-resource outcome.

## Conclusions

- **Confirmed:** Adjacent-only breakpoint `0x0044D794` also receives a
  structured same-PC `SIGSEGV`; the tested failure is not confined only to
  exact `0x0044D79A`.
- **Confirmed:** The hardened controller rejects that debugger arm while
  cleanup/detach, five independent samples, and a later game-only frame prove
  target survival under `nopass`.
- **Confirmed:** No normal load/test/store/call completion or downstream
  resource semantics are established.
- **Decision:** Further caller-gate breakpoint/tooling exploration leaves M2's
  critical path. M2.19 reuses the accepted paired replacement and a bounded
  matched trajectory to seek the resource-linked rendered outcome directly.

## Contradictions and negative results

The first launch was software-rendered and rejected. In the accepted arm,
`NextLife` and live gameplay coexist with a terminal debugger signal because
`nopass` prevents pending signal delivery at detach; this is not a status
contradiction and does not make the continuation evidence acceptable. The
conditional exact-address arm was deliberately skipped after adjacent failure.

## Tests run

- Final `make check`: Python smoke imports, Vault lint (135 notes, zero errors
  or warnings), 130 tests, and tracked-file audit (zero violations) passed.
- `git diff --check`: passed.
- Runtime audit found no scoped game, debugger, winedbg, Gamescope wrapper, or
  private PipeWire sink after cleanup.

## Recommended next action

Execute [[Project Roadmap#M2.19 — Direct visible plant-family outcome]]. Use
fresh unchanged/replacement/unchanged hardware arms, one identical bounded
camera trajectory, and game-only frames. Do not extend the caller-gate chain or
build new tooling in that packet.

## Git commit if applicable

Bounded commit message: `research: bound adjacent caller gate fault`.
