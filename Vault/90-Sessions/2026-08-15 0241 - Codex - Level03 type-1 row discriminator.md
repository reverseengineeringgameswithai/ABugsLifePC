---
type: session
date: 2026-08-15
agent: Codex
status: completed
updated: 2026-08-15
tags:
  - session
  - milestone/m3
  - re/gameplay
---

# Level03 type-1 row discriminator

## Agent

Codex

## Goal

Continue M3 on the user's clarified trigger/checkpoint direction without
reopening the independently accepted FLIKFLIK packet.

## Files inspected

- Exact PC `bugs.exe` and the derived-copy `LEVEL*.DAT` corpus.
- Required system/state/manual/roadmap notes and relevant MOCs.
- Committed blobs only from external `SRC-PS1-ABL` at
  `1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`.

## Changes made

- Added PC dossiers for `0x00432930` and `0x0041C6C0` plus a durable static
  trace.
- Added an exact-hash Level03 row-6 X+128 recipe, work-only CLI, and asset-free
  synthetic regression file.
- Opened `EXP-20260815-116`/`KU-057` and documented bounded cross-port
  experiment selection in `XPORT-20260815-002`.
- Updated Current State, roadmap, decision log, format/implementation notes,
  relevant MOCs, and this session index.

## Conclusions

PC type 1 contains 12-byte signed coordinate rows and has several consumers.
`0x00432930` is a candidate authored respawn-row selector because it gates on
bit `0x10`, selects by X/Z distance, writes shifted coordinates, and joins a
bit producer at `0x0041C8CC`. This is not yet natural PC runtime causality and
does not identify an in-world checkpoint object.

## Contradictions discovered

The prior checkpoint framing is too strong for current PC evidence, and the
committed PS1 baseline explicitly rejects an in-world checkpoint-object
interpretation there. The packet retains coordinate-row/candidate-selector
naming.

## Tests run

None. Per session instruction, regression tests were authored but not run.
No runtime process was launched.

## Unresolved questions

Whether a natural PC Level03 death/reset selects row 6 and produces the exact
predicted `+4096` X effect.

## Recommended next action

With explicit runtime approval, preflight process/sink state and run matched
unchanged-executable source/candidate Level03 deaths without debugger mutation.

## Git commit if applicable

Asset-free M3.5 discriminator packet; commit recorded at session close.
