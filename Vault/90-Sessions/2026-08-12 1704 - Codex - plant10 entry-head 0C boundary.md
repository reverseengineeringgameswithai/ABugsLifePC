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

# Plant 10 entry-head 0C boundary

## Agent

Codex

## Goal

Execute roadmap packet M2.12 under the START HERE workflow: trace both exact
plant 10 entry `+0x0C` dwords from guarded final population through resource-
batch return and a no-input title endpoint without mutating game-data memory
or general-purpose registers, originals, or Obsidian configuration.

## Files inspected

- Full required START HERE sequence: Current State, Project Roadmap,
  Environment Status, Decision Log, Known Unknowns, Reverse Engineering MOC,
  Agent Operating Manual, and Project Charter.
- [[EXP-20260812-024 - Plant10 entry-head bounded negatives]], its static
  trace, and the `0x00445020`/`0x00448010` dossiers.
- Exact instructions around `0x00446A74–0x00446AAE`,
  `0x0044764F–0x0044766E`, and `0x004480D2–0x0044813C`.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-023 - Plant10 late-initialization pointer-surface negative]]
- [[EXP-20260812-024 - Plant10 entry-head bounded negatives]]
- [[EXP-20260812-025 - Plant10 entry-head 0C bounded negative]]

## Changes made

- Ran one unchanged hardware-gated Training trace,
  `RUN-GDB-20260812-165837`, with both exact entry `+0x0C` dwords watched in
  the same run.
- Required unique `0x0044596D` followed by its immediately following
  `0x00445B01` before arming either watchpoint.
- Retained both watches through resource-batch return `0x004679C7` and an
  unattended, no-input Training title capture; neither watch exposed a read.
- Correlated the static candidates in `0x00446970` with exact `+0x2E` state
  gates and immediate pointer-derived use, without assigning field meaning.
- Deleted every breakpoint/watchpoint, detached, and kept raw debugger text
  and captures ignored under `work/`.
- Updated the experiment, roadmap, function dossiers, Current State, Known
  Unknowns, decision log, MOCs, and session index with Obsidian-safe Markdown,
  frontmatter, and wikilinks. Obsidian configuration was not changed.

## Conclusions

- **Confirmed:** Both plant 10 entry `+0x0C` dwords remain `1` at guarded
  start, resource-batch return, and the no-input title endpoint.
- **Confirmed within the retained window:** No CPU read overlaps either exact
  dword from guarded final population through `0x004679C7` or while execution
  reaches the unattended title.
- **Confirmed static context:** `0x00446A97` and `0x00447668` read selected
  entry `+0x0C` only after comparisons of selected entry `+0x2E`.
- **Unknown:** The field meanings, later consumers, and any M1 placement/
  resource identity remain unresolved.

## New hypotheses

The two exact `+0x2E` words are the narrowest next discriminator because they
gate both statically evidenced `+0x0C` reads. This is a prioritization
inference, not a semantic field name.

## Contradictions discovered

The two static `+0x0C` references did not become exact plant 10 hits in the
bounded runtime window. They remain candidates for other selected entries or
later events.

## Tests run

- Hardware stops at `0x0044596D`, immediately following `0x00445B01`, and
  `0x004679C7` in one unchanged run.
- Two exact hardware read-watchpoint ranges with zero hits through the
  retained no-input title and unchanged terminal values.
- Ignored title capture proving the unattended endpoint.
- Hardware-renderer/no-software-renderer and both plant 10 request log gates.
- Repository tests, Vault lint, tracked-file audit, JSON validation, and final
  Git hygiene recorded after documentation closure.

## Unresolved questions

- Which function first reads either exact plant 10 `+0x2E` word?
- Do gates `0x00446A8A` or `0x00447661` ever select either plant 10 entry?
- Does another entry field connect plant 10 to an M1 placement?

## Recommended next action

Execute [[Project Roadmap#M2.13 — Plant 10 entry +0x2E gate boundary]] with
both exact words in one guarded run and the same return/title bounds.

## Git commit if applicable

Bounded commit message: `research: bound plant10 entry 0c access`.
