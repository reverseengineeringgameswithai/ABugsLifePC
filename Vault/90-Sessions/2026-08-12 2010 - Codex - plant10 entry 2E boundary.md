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

# Plant 10 entry 2E boundary

## Agent

Codex

## Goal

Execute roadmap packet M2.13 under the START HERE workflow: trace both exact
plant 10 entry `+0x2E` words from guarded final population through resource-
batch return and a no-input title endpoint without mutating game-data memory,
general-purpose registers, originals, or Obsidian configuration.

## Files inspected

- Full required START HERE sequence: Current State, Project Roadmap,
  Environment Status, Decision Log, Known Unknowns, Reverse Engineering MOC,
  Agent Operating Manual, Project Charter, and Cross-Port Evidence Policy.
- [[EXP-20260812-025 - Plant10 entry-head 0C bounded negative]],
  [[Runtime Tooling]], and the `0x00446970`/`0x00448010` dossiers.
- Exact PC instructions around `0x004480B4–0x0044813C`,
  `0x00446A8A`, and `0x00447661`.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-023 - Plant10 late-initialization pointer-surface negative]]
- [[EXP-20260812-024 - Plant10 entry-head bounded negatives]]
- [[EXP-20260812-025 - Plant10 entry-head 0C bounded negative]]
- [[EXP-20260812-026 - Plant10 entry 2E bounded negative]]

## Changes made

- Ran one accepted unchanged hardware-gated Training trace,
  `RUN-GDB-20260812-195759`, with both exact entry `+0x2E` words watched in
  the same run.
- Used Gamescope/XWayland remote control to send Down then Return at the
  opening selector, then accepted the run only after the complete log proved
  640x480x16 Direct3D and contained no `INITSOFTRENDER`.
- Required unique `0x0044596D` followed by its immediately following
  `0x00445B01` before arming either watchpoint.
- Retained both watches through resource-batch return `0x004679C7` and an
  unattended, no-input Training title capture; neither watch exposed a read.
- Correlated the negative with exact population instructions in `0x00448010`
  and static comparisons in `0x00446970`, without assigning field meaning.
- Deleted every breakpoint/watchpoint, detached, stopped the isolated game,
  and kept raw debugger text and captures ignored under `work/`.
- Updated the experiment, roadmap, function dossiers, Current State, Known
  Unknowns, MOCs, and session index with Obsidian-safe Markdown, frontmatter,
  and wikilinks. Obsidian configuration was not changed.

## Conclusions

- **Confirmed:** Both plant 10 entry `+0x2E` words remain unsigned `1` at
  guarded start, resource-batch return, and the no-input title endpoint.
- **Confirmed within the retained window:** No CPU read overlaps either exact
  word from guarded final population through `0x004679C7` or while execution
  reaches the unattended title.
- **Confirmed consequence:** Neither exact plant 10 entry reaches the
  `0x00446A8A` or `0x00447661` comparisons during that window.
- **Unknown:** Field meanings, later consumers, and any M1 placement/resource
  identity remain unresolved.

## New hypotheses

Exact entry `+0x28` is the narrowest next surface because `0x0044810B`
statically populates it and prior packets already bound `+0x20`, combined
`+0x24/+0x26`, entry-head, `+0x0C`, and `+0x2E` ranges. This is a
prioritization inference, not a semantic field name.

## Contradictions discovered

An initial candidate arm was rejected after the user observed that the opening
selector still had software selected: remote Down had not been sent. All
breakpoints were deleted and that process was stopped. The accepted fresh run
used explicit Down then Return and the complete log gate. This reinforces that
intended input or early driver-enumeration lines are not renderer proof.

The static `+0x2E` comparisons also did not become exact plant 10 hits in the
bounded runtime window. They remain confirmed entry-relative accesses, not
exact plant 10 consumers.

## Tests run

- Hardware stops at `0x0044596D`, immediately following `0x00445B01`, and
  `0x004679C7` in one unchanged accepted run.
- Two exact two-byte hardware read-watchpoint ranges with zero hits through
  the retained no-input title and unchanged terminal values.
- Ignored title capture proving the unattended endpoint.
- Remote Down/Return plus complete hardware-renderer/no-software-renderer and
  both plant 10 request log gates.
- `make check`: Python smoke imports, Vault lint (121 notes, zero errors or
  warnings), 119 tests, tracked-file audit (zero violations), and Git diff
  whitespace checks all passed.

## Unresolved questions

- Which function first reads either exact plant 10 `+0x28` word?
- Does either entry become active after the retained title endpoint?
- Does another entry field connect plant 10 to an M1 placement?

## Recommended next action

Execute [[Project Roadmap#M2.14 — Plant 10 entry +0x28 boundary]] with both
exact words in one guarded run and the same return/title bounds.

## Git commit if applicable

Bounded commit message: `research: bound plant10 entry 2e access`.
