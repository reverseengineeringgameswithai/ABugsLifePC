---
type: session
agent: Codex
date: 2026-08-15
status: completed
tags:
  - m3
  - runtime
  - level-dat
---

# 2026-08-15 1129 - Codex - Approved Level03 row-6 reset rerun

## Scope

Resolve the hard-truth governance rejection of the Level03 type-1 row causal
diagnostic, rerun control and candidate after explicit authorization, preserve
runtime hygiene, and avoid promoting the table to checkpoint semantics without
natural PC evidence.

## Work completed

- Obtained explicit prior approval for byte `0x18` at `0x0059D9A0` and word
  `0x0002` at `0x0059A5B0`.
- Ran fresh isolated control and candidate Level03 processes.
- Required internal level ID `3` and a row-6-nearest pre-arm endpoint on both
  sides.
- Captured continuous read-only route and reset traces.
- Observed control `(501696, *, 494016)` and candidate
  `(505792, *, 494016)` reset coordinates.
- Confirmed X delta `+4096 = 128 << 5` and exact unchanged Z.
- Preserved the Y distinction as terrain recomputation, not noise to erase.
- Investigated the natural producer far enough to bound collision-dispatch
  result `1` at `0x004408EA` and helper `0x004ACF90`; semantics remain open.
- Cleaned both process groups and private sinks and restored the baseline Wine
  `Y:` mapping.

## Evidence

- [[EXP-20260815-117 - Approved Level03 row-6 reset rerun]]
- [[EXP-20260815-116 - Level03 type-1 row discriminator]]
- [[FUNC-97C95BA5572D-0041C6C0]]
- [[FUNC-97C95BA5572D-00432930]]
- `work/copies/EXP-20260815-117-approved-row6-reset/`

## Boundary

The result confirms a row-based reset-coordinate consumer. It does not confirm
the natural trigger, the user-facing checkpoint behavior, or the semantic name
of the type-1 table.

## Hard-truth result

James returned `ACCEPT` for the bounded Level03 row-6 reset-coordinate claim.
He explicitly excluded checkpoint semantics, a natural trigger, semantic
identification of material/result `1`, and generalization beyond the tested
row, level, and consumer. His requested Decision Log supersession cleanup was
recorded in the same session.
