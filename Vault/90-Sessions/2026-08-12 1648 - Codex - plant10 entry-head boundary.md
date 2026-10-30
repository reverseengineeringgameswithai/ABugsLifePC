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

# Plant 10 entry-head boundary

## Agent

Codex

## Goal

Execute roadmap packet M2.11 under the START HERE workflow: trace both plant
10 entries' exact `+0x00/+0x04/+0x08` dwords through matched guarded windows
without modifying game state, originals, or Obsidian configuration.

## Files inspected

- Full required START HERE sequence: Current State, Project Roadmap,
  Environment Status, Decision Log, Known Unknowns, Reverse Engineering MOC,
  Agent Operating Manual, and Project Charter.
- [[EXP-20260812-023 - Plant10 late-initialization pointer-surface negative]],
  its static trace, and the `0x00445020`/`0x00448010` dossiers.
- Exact instructions around `0x004480D2–0x00448117`, indexed shared-array
  references in the Ghidra export, and static `+0x0C` reads at
  `0x00446A97/0x00447668`.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-021 - Plant10 runtime destination and M1 negative window]]
- [[EXP-20260812-022 - Plant10 post-init object-entry negative]]
- [[EXP-20260812-023 - Plant10 late-initialization pointer-surface negative]]
- [[EXP-20260812-024 - Plant10 entry-head bounded negatives]]

## Changes made

- Ran two unchanged, hardware-gated Training traces:
  `RUN-GDB-20260812-163111` for first-entry `+0x00/+0x04/+0x08` and
  `RUN-GDB-20260812-163840` for the matched second-entry ranges.
- Used unique `0x0044596D` followed by its immediately following
  `0x00445B01` in both runs before arming any read watchpoint.
- Retained each three-watch arm through scene-resource batch return
  `0x004679C7` and across the title transition into captured live gameplay;
  neither arm exposed a read.
- Recorded that queued input advanced the first title and user input advanced
  the second. No unattended title-pause capture is claimed.
- Deleted every breakpoint/watchpoint, detached, and confirmed both logs pass
  the hardware, plant-request, `End InitMainGame`, and `NextLife` gates.
- Kept raw debugger text and captures ignored under `work/`; retained only
  curated evidence, metadata, ordinary logs, and static instructions.
- Updated the experiment, roadmap, function dossiers, Current State, Known
  Unknowns, MOCs, and session index with Obsidian-safe Markdown, frontmatter,
  and wikilinks. Obsidian configuration was not changed.

## Conclusions

- **Confirmed:** Both plant 10 entry heads are
  `0/0/0/1` at exact offsets `+0x00/+0x04/+0x08/+0x0C` in both runs.
- **Confirmed within the matched windows:** No CPU read overlaps either
  entry's first three dwords from guarded final population through
  `0x004679C7` or across the title transition into captured gameplay.
- **Confirmed:** Both unchanged runs pass Direct3D and `NextLife` gates after
  clean debugger closure.
- **Unknown:** The `+0x0C` consumer/meaning, later fields, non-CPU state, and
  any M1 placement/resource identity remain unresolved.

## New hypotheses

The observed nonzero `+0x0C` dword is the narrowest remaining statically
copied entry-head discriminator. This is a prioritization inference only.

## Contradictions discovered

The planned unattended title-pause endpoint was not retained: input advanced
both runs. The watches nevertheless remained active across that transition to
a later gameplay endpoint. The deviation is recorded rather than restated as
an unattended title capture.

## Tests run

- Matched hardware stops at `0x0044596D`, immediately following
  `0x00445B01`, and `0x004679C7` in two unchanged runs.
- Six exact hardware read-watchpoint ranges with zero hits through the
  retained endpoints and unchanged terminal values.
- Ignored gameplay captures proving each later endpoint.
- Hardware renderer/no-software-renderer, both plant 10 requests,
  `End InitMainGame`, and `NextLife` log gates in both runs.
- Repository tests, Vault lint, tracked-file audit, JSON validation, and final
  Git hygiene recorded after documentation closure.

## Unresolved questions

- Which function first reads either exact `+0x0C` dword?
- Do static candidates at `0x00446A97/0x00447668` ever select plant 10?
- Does another entry field connect plant 10 to an M1 placement?

## Recommended next action

Execute [[Project Roadmap#M2.12 — Plant 10 entry-head +0x0C consumer boundary]]
with both exact dwords in one guarded run and preserve a no-input title capture
when possible.

## Git commit if applicable

Bounded commit message: `research: bound plant10 entry-head access`.
