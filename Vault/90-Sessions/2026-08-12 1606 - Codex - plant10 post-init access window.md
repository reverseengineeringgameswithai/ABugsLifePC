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

# Plant 10 post-init access window

## Agent

Codex

## Goal

Execute roadmap packet M2.9 on the unchanged Training copy: reproduce plant
10's exact two-entry surface, trace its first post-initialization reader or
retain a precise negative, and preserve the Vault/Git evidence boundary.

## Files inspected

- Required START HERE sequence, Agent Operating Manual, Project Charter,
  Project Roadmap, Known Unknowns, Decision Log, and relevant MOCs.
- [[EXP-20260812-021 - Plant10 runtime destination and M1 negative window]],
  `M2-plant10-runtime-destination-trace.md`, and the `0x00444C40`,
  `0x00445020`, and `0x00448010` function dossiers.
- Exact executable instructions at `0x00444D06`,
  `0x004480B4–0x00448103`, `0x00445968–0x00445B01`, and
  `0x004679C2–0x004679C7`.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-015 - Plant pair caller and consumer trace]]
- [[EXP-20260812-020 - Training plant10 request suppression]]
- [[EXP-20260812-021 - Plant10 runtime destination and M1 negative window]]
- [[EXP-20260812-022 - Plant10 post-init object-entry negative]]

## Changes made

- Ran accepted unchanged Training trace `RUN-GDB-20260812-155922` through the
  required 640×480×16 Direct3D hardware path.
- Reproduced plant 10 header indices `66/68`, exact two-entry range, two
  entry-relative `+0x20` values, and caller-adjusted first-entry words.
- Armed three hardware read watchpoints at the natural Training title pause
  and retained them through `NextLife` and a measured 71.708-second gameplay
  interval.
- Kept raw GDB text and captures ignored under `work/`; committed only the
  ordinary game log, curated address/value evidence, metadata, and static
  instruction trace.
- Updated the experiment, two function dossiers, roadmap, Current State,
  Known Unknowns, Decision Log, MOCs, and session index using Obsidian-safe
  Markdown/frontmatter/wikilinks. Obsidian configuration was not changed.

## Conclusions

- **Confirmed:** The accepted run exactly reproduces the plant 10 values from
  M2.8 and passes the Direct3D, plant-request, `End InitMainGame`, and
  `NextLife` gates.
- **Confirmed within the exact window:** No CPU read overlaps
  `0x005AAB20–0x005AAB23`, `0x005AAB70–0x005AAB73`, or
  `0x005AAB24–0x005AAB27` from the title start key through 71.708204459
  seconds of gameplay.
- **Unknown:** A reader/copy may exist between caller-adjustment end
  `0x00445B01` and the title, in another entry field, or after an unobserved
  event. No semantic field or placement identity is assigned.

## New hypotheses

A late-initialization read/copy is now a more direct discriminator than a
longer idle gameplay window. Resource-batch return `0x004679C7` provides an
exact intermediate boundary for that test.

## Contradictions discovered

The expected likely post-initialization reader did not appear on any of the
three exact source ranges. This is retained as a bounded negative rather than
silently converted into an unused-resource claim.

## Tests run

- Exact executable and Training DAT identity inherited and reread for the
  unchanged work copy.
- Hardware execution stops at `0x0044596D` and `0x00445B01`.
- Three exact hardware read watchpoints from the natural title start through
  a 71.708204459-second gameplay window; zero hits and unchanged terminal
  values.
- Hardware renderer/no-software-renderer, both plant 10 requests,
  `End InitMainGame`, and `NextLife` log gates.
- Repository unit tests, Vault lint, tracked-file audit, JSON validation, and
  final Git hygiene recorded after documentation closure.

## Unresolved questions

- Does a first read/copy occur after `0x00445B01` but before
  `0x004679C7` or the title pause?
- Which other entry fields, if any, carry downstream state?
- Does any derived state connect plant 10 to an M1 placement?

## Recommended next action

Execute [[Project Roadmap#M2.10 — Plant 10 late-initialization consumer boundary]]
with the same exact watches armed at `0x00445B01` and explicit return/title
bounds.

## Git commit if applicable

Bounded commit message: `research: bound plant10 post-init access window`.
