---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/static
  - re/file-format
---

# Plant request origin

## Agent

Codex

## Goal

Complete roadmap M2.3 by mapping both inputs read by plant-ID collector
`0x00416100`, binding selected Training IDs to exact PC source bytes, and
testing whether those bytes overlap an M1 scene-record or positive-target
chain.

## Files and evidence inspected

- Exact-hash Ghidra evidence export and derived work-copy executable
- `0x00416100`, `0x0041C420`, `0x0044BB70`, `0x00465030`, and `0x004671D0`
- Exact Training and Level 01 DAT work-copy bytes and independent parser output
- Retained accepted hardware logs `RUN-WINE-20260812-000634` and
  `RUN-WINE-20260812-114514`
- M1 record, payload, and positive-target boundaries

No runtime was launched or modified. No file under `originals/` was modified.
No PS1 source was consulted.

## Changes made

- Added `EXP-20260812-016` and a reviewable static trace report.
- Added conservative dossiers for the `LEVEL.RAW` type-35 packet parser and
  runtime-table transformer.
- Updated the plant collector, DAT fixup, and DAT-prefix dossiers with the
  exact type-`0x3F` producer path.
- Closed M2.3 with a separate-table result and made the bounded `.ANM`
  inspector M2.4.
- Added `KU-022` for `.ANM` layout limits and `KU-023` for the still-missing
  M1 placement-to-resource identity.

## Conclusions

- **Confirmed:** `0x00465030` and `0x0041C420` establish the collector's first
  input from a copied `LEVEL.RAW` type-35 table.
- **Confirmed:** `0x0044BB70` makes slot 63 at `0x005C595C` point into a
  type-`0x3F` top record in the loaded `LEVEL*.DAT`.
- **Confirmed:** exact Training bytes `0x394`, `0x3A4`, and `0x3B4` map to
  plant IDs 4, 10, and 6; retained hardware request order independently agrees.
- **Confirmed:** those bytes are outside the M1 20-byte scene-record, payload,
  and positive-target ranges.
- **Unknown:** the stronger placement-record-to-resource identity remains an
  M2 exit gate.

## Contradictions and negative results

- The plant selector is in the same DAT and fixup path as M1, but shared file
  membership is not byte-range or semantic identity. It is recorded as a
  separate table.
- Level 01 order indicates an early ID 7 from the `LEVEL.RAW`-derived input,
  but no exact type-35 field is claimed from order correlation alone.
- No dynamic experiment was needed; no software-renderer evidence entered the
  packet.

## Tests and checks

- GNU objdump instructions were checked against the exact executable hash.
- Training and Level 01 DAT hashes and parser boundaries were rechecked.
- Both retained corroborating logs contain the required 640×480×16 and
  Direct3D hardware markers and no `INITSOFTRENDER` marker.
- Vault, tracked-file, diff, and Git checks are recorded in the handoff.

## Recommended next action

Execute [[Project Roadmap#M2.4 — Bounded ANM inspector]]: reproduce the exact
first-level `0x00444B70` walk across plants 04/05/06/10 and implement only a
bounds-checked read-only inspector with synthetic invalid fixtures.

## Git commit if applicable

Bounded commit message: `research: bind plant IDs to DAT selectors`.
