---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/dynamic
---

# Plant 10 entry 28 boundary

## Agent

Codex

## Goal

Execute roadmap packet M2.14 under the START HERE workflow: trace both exact
plant 10 entry `+0x28` words from guarded final population through resource-
batch return and a no-input title endpoint without mutating game-data memory,
general-purpose registers, originals, or Obsidian configuration.

## Files inspected

- Full required START HERE sequence: Current State, Project Roadmap,
  Environment Status, Decision Log, Known Unknowns, Reverse Engineering MOC,
  Agent Operating Manual, Project Charter, and Cross-Port Evidence Policy.
- [[EXP-20260812-026 - Plant10 entry 2E bounded negative]],
  [[Runtime Tooling]], and the `0x00445020`, `0x00446970`, and `0x00448010`
  dossiers.
- Exact PC instructions around `0x004480B4–0x00448117` and the newly bounded
  candidate loop `0x0044CE0D–0x0044D1ED`.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-023 - Plant10 late-initialization pointer-surface negative]]
- [[EXP-20260812-024 - Plant10 entry-head bounded negatives]]
- [[EXP-20260812-025 - Plant10 entry-head 0C bounded negative]]
- [[EXP-20260812-026 - Plant10 entry 2E bounded negative]]
- [[EXP-20260812-027 - Plant10 entry 28 bounded negative]]

## Changes made

- Ran one accepted unchanged hardware-gated Training trace,
  `RUN-GDB-20260812-201419`, with both exact entry `+0x28` words watched in
  the same run.
- Used remote control to send Down then Return at the opening selector, then
  accepted the run only after the complete log proved 640x480x16 Direct3D and
  contained no `INITSOFTRENDER`.
- Required unique `0x0044596D` followed by its immediately following
  `0x00445B01` before arming either watchpoint.
- Retained both watches through resource-batch return `0x004679C7` and an
  unattended, no-input Training title capture; neither watch exposed a read.
- Used only 640x480 isolated Gamescope captures; no host desktop or whole-
  monitor screenshot was taken.
- Correlated the negative with exact population instructions in `0x00448010`
  and identified address-based function `0x0044CA00` as the narrower
  event-specific follow-up, without assigning field or function semantics.
- Deleted every breakpoint/watchpoint, detached, stopped only the isolated
  game/wrapper processes, and kept raw debugger text and captures ignored
  under `work/`.
- Updated the experiment, roadmap, function dossiers, Current State, Known
  Unknowns, MOCs, decision log, and session index with Obsidian-safe Markdown,
  frontmatter, and wikilinks. Obsidian configuration was not changed.

## Conclusions

- **Confirmed:** Both plant 10 entry `+0x28` words remain unsigned zero at
  guarded start, resource-batch return, and the no-input title endpoint.
- **Confirmed within the retained window:** No CPU read overlaps either exact
  word from guarded final population through `0x004679C7` or while execution
  reaches the unattended title.
- **Confirmed across M2.9–M2.14:** Every entry field currently tied by exact
  static stores to `0x00448010` and its guarded caller now has at least one
  explicit bounded read-watchpoint window.
- **Unknown:** Field meanings, later consumers, and any M1 placement/resource
  identity remain unresolved.

## New hypotheses

The exact `0x0044CE3E` selected-entry `+0x2E` read is a stronger post-title
candidate than further field widening. Plant 10 slot/header arithmetic is
exact, but a Training source record supplying selector 10 remains unobserved.

## Contradictions discovered

The final statically populated `+0x28` surface did not expose a CPU reader in
the initialization/title window. The result closes that widening sequence,
not the entries' later lifetime or relevance.

## Tests run

- Hardware stops at `0x0044596D`, immediately following `0x00445B01`, and
  `0x004679C7` in one unchanged accepted run.
- Two exact two-byte hardware read-watchpoint ranges with zero hits through
  the retained no-input title and unchanged terminal values.
- Ignored game-only title capture proving the unattended endpoint.
- Remote Down/Return plus complete hardware-renderer/no-software-renderer and
  both plant 10 request log gates.
- `make check`: Python smoke imports, Vault lint (125 notes, zero errors or
  warnings), 119 tests, tracked-file audit (zero violations), and Git diff
  whitespace checks all passed.

## Unresolved questions

- Does the first post-title read of either plant 10 `+0x2E` word occur at
  `0x0044CE3E`?
- Which Training source record, if any, supplies selector 10?
- Can that selected-entry branch be connected to an M1 placement and rendered
  or behavioral outcome?

## Recommended next action

Execute [[Project Roadmap#M2.15 — Plant 10 post-title selected-entry event]]
at the natural Training title. Watch both exact `+0x2E` words, advance once,
and capture the first reader plus its source-record selector and downstream
branch.

## Git commit if applicable

Bounded commit message: `research: bound plant10 entry 28 access`.
