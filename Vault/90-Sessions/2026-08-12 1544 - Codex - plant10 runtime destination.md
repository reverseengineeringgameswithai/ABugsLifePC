---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/dynamic
  - re/rendering
---

# Plant 10 runtime destination

## Agent

Codex

## Goal

Execute roadmap packet M2.8 with the required START HERE preflight, an
unchanged Training work copy, the Direct3D hardware gate, exact plant 10
runtime destinations, and bounded M1 access windows.

## Files inspected

- `Vault/00-System/START HERE.md`, Current State, Environment Status, Project
  Charter, Agent Operating Manual, Project Roadmap, Decision Log, Known
  Unknowns, Naming Conventions, Obsidian Setup, and relevant MOCs/templates.
- Exact `0x00444C40`, `0x00445020`, `0x0044594F–0x004459A1`,
  `0x00449B61–0x00449E25`, and related function dossiers/static exports.
- Prior M1 and M2 evidence through
  [[EXP-20260812-020 - Training plant10 request suppression]].
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-008 - Training record watchpoints and individual roles]]
- [[EXP-20260812-009 - Training payload target structure and reuse census]]
- [[EXP-20260812-010 - Training target rebind visible substitution]]
- [[EXP-20260812-015 - Plant pair caller and consumer trace]]
- [[EXP-20260812-016 - Plant request origin and separate DAT table]]
- [[EXP-20260812-017 - Bounded PC ANM inspector]]
- [[EXP-20260812-020 - Training plant10 request suppression]]
- [[EXP-20260812-021 - Plant10 runtime destination and M1 negative window]]

## Changes made

- Ran unchanged Training as `RUN-GDB-20260812-153150` and used only native
  hardware execution breakpoints/read watchpoints plus read-only inspection.
- Bound resource ID `0x71` to ANM slot `0x005B1AA4`, live ANM
  `0x006C342B`, runtime indices `66–68`, and exact two-entry range
  `[0x005AAB00, 0x005AABA0)`.
- Bracketed the direct dispatch-to-target-renderer path independently for M1
  records 124, 125, and 126 while watching three exact plant 10 pointer
  destinations.
- Kept the raw GDB transcript and screenshots ignored under `work/`; committed
  only curated address/value evidence, metadata, and the ordinary text log.
- Updated the experiment, static trace, function dossiers, roadmap, Current
  State, Known Unknowns, resource/experiment MOCs, and session index using
  Obsidian-compatible Markdown, frontmatter, and wikilinks.

## Conclusions

- **Confirmed:** The exact plant 10 runtime destination includes ANM slot
  `0x005B1AA4` and two Training object entries at
  `[0x005AAB00, 0x005AABA0)`.
- **Confirmed within the exact windows:** No read of the ANM slot or either
  object-entry `+0x20` dword occurs from the record-124, -125, or -126 dispatch
  stop through its target-renderer return.
- **Confirmed:** The run selected 640×480×16 Direct3D hardware, did not enter
  `INITSOFTRENDER`, loaded both plant 10 files, and reached `NextLife`.
- **Unknown:** Other object-entry fields, copied state, later readers, and the
  broader M1 placement/resource identity remain unresolved.

## New hypotheses

The simplest direct-pointer bridge from records 124–126 to the measured plant
10 pointer surface is disfavored. A downstream reader, other field, or copied
state remains a viable PC-native route and must be traced before another visual
identity test.

## Contradictions discovered

The live destination is not one monolithic object pointer. The ANM slot points
to a header bounding two distinct global entries, while four other per-ID
auxiliary slots are zero at the measured boundary. No semantic structure name
was assigned.

## Tests run

- Exact SHA-256 checks for the executable and unchanged Training DAT before
  launch.
- Hardware stops at `0x0044596D`, `0x00445B01`, `0x00449B64`, and
  `0x00449E25`; exact live record/payload/target and plant destination checks.
- Three independent read-watchpoint windows on `0x005B1AA4`, `0x005AAB20`,
  and `0x005AAB70`.
- Hardware renderer, no-software-renderer, plant 10 request, `InitMainGame`,
  and `NextLife` log gates.
- Repository validation recorded after documentation closure.

## Unresolved questions

- Which post-initialization PC function first reads the two plant 10 entries?
- What are the complete `.ALL`-derived entry boundaries and semantics?
- Does later or copied plant 10 state connect to an M1 placement?

## Recommended next action

Execute [[Project Roadmap#M2.9 — Plant 10 downstream object-entry consumer]]
from the natural Training title pause and follow the first actual entry reader
before designing another identity experiment.

## Git commit if applicable

Bounded commit message: `research: bound plant10 runtime destination`.
