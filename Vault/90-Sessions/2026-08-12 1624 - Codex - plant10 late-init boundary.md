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

# Plant 10 late-init boundary

## Agent

Codex

## Goal

Execute roadmap packet M2.10 under the START HERE workflow: test the exact
plant 10 pointer surface from its final caller adjustment through scene-
resource batch return and the natural Training title, while preserving
Obsidian and Git hygiene.

## Files inspected

- Full required START HERE sequence: Current State, Project Roadmap,
  Environment Status, Decision Log, Known Unknowns, Reverse Engineering MOC,
  Agent Operating Manual, and Project Charter.
- [[EXP-20260812-022 - Plant10 post-init object-entry negative]], its static
  trace, and the `0x00445020`, `0x00444C40`, and `0x00448010` dossiers.
- Exact instructions around `0x00445626–0x00445632`,
  `0x00445B01–0x00445B0B`, `0x004480DF–0x00448107`, and
  `0x004679C2–0x004679C7`.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-015 - Plant pair caller and consumer trace]]
- [[EXP-20260812-021 - Plant10 runtime destination and M1 negative window]]
- [[EXP-20260812-022 - Plant10 post-init object-entry negative]]
- [[EXP-20260812-023 - Plant10 late-initialization pointer-surface negative]]

## Changes made

- Ran unchanged Training trace `RUN-GDB-20260812-161520` through the required
  640×480×16 Direct3D path.
- Rejected an unguarded `0x00445B01` stop after runtime proved it preceded
  plant 10, then corrected the protocol using unique plant 10 post-call
  `0x0044596D` and only its immediately following common-tail stop.
- Retained three exact hardware read watches through scene-resource batch
  return `0x004679C7` and the natural Training title; neither boundary exposed
  a read.
- Deleted every accepted and rejected breakpoint/watchpoint, detached, resumed
  normally, and confirmed logged `End InitMainGame` and `NextLife`.
- Kept raw debugger text and the title capture ignored under `work/`; committed
  only curated evidence, metadata, the ordinary log, and static instructions.
- Updated the experiment, roadmap, Decision Log, function dossiers, Current
  State, Known Unknowns, MOCs, and session index with Obsidian-safe Markdown,
  frontmatter, and wikilinks. Obsidian configuration was not changed.

## Conclusions

- **Confirmed:** `0x00445B01` is a common resource-ID loop tail and requires
  the unique `0x0044596D` plant 10 guard for a resource-specific experiment.
- **Confirmed within the accepted windows:** No CPU read overlaps either plant
  10 entry `+0x20` dword or the adjusted first-entry dword from the guarded
  final adjustment through `0x004679C7` or the natural title.
- **Confirmed:** The unchanged run passes hardware, plant-request,
  `End InitMainGame`, and `NextLife` gates after clean debugger detach.
- **Unknown:** Entry-head and later fields, non-CPU state, and any M1
  placement/resource identity remain unresolved.

## New hypotheses

The statically copied entry-head dwords are a narrower next target than another
long observation of the already negative pointer surface.

## Contradictions discovered

The roadmap's shorthand treated `0x00445B01` as plant-specific. Live zero
destinations and exact loop instructions contradict that. The rejected stop
and population-time report are preserved explicitly; only the corrected
guarded interval supports M2.10.

## Tests run

- Hardware execution stops at `0x0044596D`, its immediately following
  `0x00445B01`, and `0x004679C7`.
- Three exact read watchpoints with zero accepted hits through both required
  boundaries and unchanged terminal values.
- Native ignored capture of the natural Training title.
- Hardware renderer/no-software-renderer, both plant 10 requests,
  `End InitMainGame`, and `NextLife` log gates.
- Repository tests, Vault lint, tracked-file audit, JSON validation, and final
  Git hygiene recorded after documentation closure.

## Unresolved questions

- Which function first reads entry-head dwords `+0x00/+0x04/+0x08/+0x0C`?
- Do the two entries share a reader and downstream destination?
- Does another entry field connect plant 10 to an M1 placement?

## Recommended next action

Execute [[Project Roadmap#M2.11 — Plant 10 entry-head consumer boundary]] with
the corrected plant-specific start guard and matched first-/second-entry
windows.

## Git commit if applicable

Bounded commit message: `research: bound plant10 late-init access window`.
