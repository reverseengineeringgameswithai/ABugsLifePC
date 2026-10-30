---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/static
---

# Plant pair caller trace

## Agent

Codex

## Goal

Complete roadmap M2.2 by mapping the PC callers, constructed paths, arena
ownership, size boundaries, and first downstream consumers for the plant
`.ANM`/`.ALL` pairs shared by retained Training and Level 01 runs.

## Files and evidence inspected

- Exact-hash Ghidra evidence export and derived work-copy executable
- `0x00416100`, `0x00444B70`, `0x00444C40`, `0x00445020`, `0x00448010`,
  `0x004671D0`, and `0x004AE240`
- Exact plant base/extension strings and GNU objdump instruction listings
- Accepted hardware logs `RUN-WINE-20260812-000634` and
  `RUN-WINE-20260812-114514`
- Metadata and first-level header/offset observations for the four shared
  `.ANM` files

No runtime was launched or modified. No file under `originals/` was modified.
No PS1 source was consulted.

## Changes made

- Added `EXP-20260812-015` and a reviewable static trace report.
- Added conservative address dossiers for the plant-ID collector, scene batch
  loader, pair coordinator, and `.ALL` first consumer.
- Updated the whole-file loader's complete static thunk-call list and runtime
  correlation.
- Closed M2.2, selected `.ANM` for later bounded inspection, and made the exact
  plant-ID producer/M1 bridge question M2.3.

## Conclusions

- **Confirmed:** one coordinator constructs both extensions from one base path;
  the files do not share the same immediate consumer.
- **Confirmed:** `.ANM` cursor advancement uses aligned file size before
  `0x00444B70` relocates in place.
- **Confirmed:** `.ALL` is parsed by `0x00448010`, which discards loader byte
  size and advances the shared cursor from embedded lengths.
- **Confirmed:** Training and Level 01 request orders match the static
  `.anm`-then-`.all` sequence for each selected ID.
- **Unknown:** the producer fields behind later plant IDs and any M1-to-file
  dependency.

## Contradictions and negative results

- Basename pairing predicts coordination, which static analysis confirms, but
  it does not imply one common parser or size contract.
- `.ALL` exposes more downstream fields but has the weaker independent bound;
  it is not selected as the first parser target.
- No new dynamic experiment was necessary, so no software-renderer evidence
  entered the packet.

## Tests and checks

- Exact instruction and string addresses were cross-checked with GNU objdump.
- Four selected `.ANM` files have in-range first-level offsets under the
  `0x00444B70` walk.
- Vault, tracked-file, diff, and Git checks are recorded in the handoff.

## Recommended next action

Execute [[Project Roadmap#M2.3 — Plant request origin and M1 dependency bridge]]:
trace Training ID 4, 10, or 6 from `0x00416100` back to an exact producer and
test whether that source lies in the M1 DAT path or a separate runtime table.

## Git commit if applicable

Bounded commit message: `research: trace plant resource pair loading`.
