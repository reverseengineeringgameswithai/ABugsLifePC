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

# Plant 10 post-title selected-entry boundary

## Agent

Codex

## Goal

Execute roadmap packet M2.15 under the START HERE workflow, and create a
properly linked Obsidian register/template explaining the capabilities that
would improve continued PC reverse engineering.

## Files inspected

- Full required START HERE sequence, Project Charter, relevant MOCs, Runtime
  Tooling, prior plant 10 experiments, and function dossiers.
- Exact PC instructions around `0x0044CE0D–0x0044D1ED`, caller gate
  `0x0044D78F–0x0044D7A9`, thunks, and `0x00463770`.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-026 - Plant10 entry 2E bounded negative]]
- [[EXP-20260812-027 - Plant10 entry 28 bounded negative]]
- [[EXP-20260812-028 - Plant10 post-title selected-entry negative]]

## Changes made

- Ran one unchanged, hardware-gated Training session and accepted it only
  after exact 640x480x16 Direct3D log proof with no `INITSOFTRENDER`.
- Used only the isolated 640x480 Gamescope surface for renderer steering and
  endpoint captures; no host desktop or whole-monitor screenshot was taken.
- Recorded zero exact plant 10 `+0x2E` access stops from the natural title
  through `NextLife`, zero stops in a separate 30.026628-second early-gameplay
  arm, and zero execution stops at exact candidate reader `0x0044CE3E` in a
  separate 10.014330-second arm.
- Correlated the exact value-1 branch and its first static callee without
  assigning semantic names.
- Preserved and rejected two later exploratory caller-gate arms after raw GDB
  output recorded `SIGSEGV` at `0x0044D79A`, despite harness cleanup/detach
  receipts; Wine later printed the matching fault. No downstream claim uses
  those runs.
- Created [[Reverse Engineering Capability Gaps]] and reusable
  [[Capability Gap]], linked them from the implementation/research/tooling
  indexes, and kept roadmap scheduling authoritative.
- Stopped only the isolated game/wrapper PIDs. TERM did not end the remaining
  wrappers, so exact already-resolved PIDs `2544386/2544224` were killed; no
  game, Gamescope, debugger, or harness process remained.

## Conclusions

- **Confirmed:** Neither exact plant 10 `+0x2E` word was accessed across the
  controlled title-to-`NextLife` transition or the separate elapsed arm.
- **Confirmed:** Exact candidate `0x0044CE3E` did not execute in the stated
  no-input control window.
- **Static only:** Value 1 would branch to `0x0044CFC4`, whose first call is
  `0x0044D079 -> 0x004012C6 -> 0x00463770`.
- **Unknown:** The source event/record that activates `0x0044CA00` for selector
  10 and the cause of the exploratory debugger/Wine fault.

## New hypotheses

The selected-entry path is sparse or event-specific. A fresh process with the
caller gate, callee entry, and two exact data watches armed simultaneously is
more discriminating than another unattended wall-clock extension.

## Contradictions discovered

The harness reported clean deletion/detach for the exploratory caller-gate arm,
but raw GDB output from the same run first recorded `SIGSEGV` at the breakpoint
PC and Wine later printed the matching unhandled read fault. Because
`test al,0x10` has no memory operand, the report cannot be explained as an
ordinary memory read by that instruction. The affected arms are retained but
excluded from M2.15's accepted result.

## Tests run

- `RUN-GDB-20260812-203714`: two watches, zero stops, `NextLife`, clean detach.
- `RUN-GDB-20260812-203820`: two watches, zero stops, 30.026628-second timeout,
  clean detach.
- `RUN-GDB-20260812-203930`: exact reader breakpoint, zero stops,
  10.014330-second timeout, clean detach.
- Renderer, plant-pair, title, `End InitMainGame`, and `NextLife` log gates.
- `make check`: Python smoke imports, Vault lint (129 notes, zero errors or
  warnings), 119 tests, tracked-file audit (zero violations), and staged/
  unstaged whitespace checks all passed.

## Unresolved questions

- Does a fresh simultaneous four-point arm reproduce the outer gate and then
  enter `0x0044CA00` without a Wine exception?
- Does any source record supply selector 10 in that event?
- Which capability gaps are worth implementing before later event traces?

## Recommended next action

Execute [[Project Roadmap#M2.16 — Fresh-session selected-entry caller chain]].
Use one fresh unchanged hardware run and arm `0x0044D79A`, `0x0044CA00`, and
both exact plant 10 watches simultaneously before the title transition.
Require a live-game post-detach receipt; if the fault reproduces, address
CAP-001 before interpreting the chain.

## Git commit if applicable

Bounded commit message: `research: bound plant10 post-title event`.
