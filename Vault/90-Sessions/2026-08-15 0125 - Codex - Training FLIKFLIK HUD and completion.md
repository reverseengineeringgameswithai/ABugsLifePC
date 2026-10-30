---
type: session
date: 2026-08-15
agent: Codex
topic: Training FLIKFLIK HUD and completion
updated: 2026-08-15
tags:
  - session
  - milestone/m3
  - re/gameplay
  - re/hud
---

# Training FLIKFLIK HUD and completion

## Goal

Complete M3.4 for the user's accepted eight-letter Training demo: assign all
eight records independent collectible state, suppress repeated completion,
and center `FLIKFLIK` in both the in-level HUD and level-complete tally with
an `8/8` count.

## Work completed

- Refreshed START HERE, current/environment state, charter, operating manual,
  roadmap, and relevant MOCs/dossiers.
- Traced the retail four-slot consumers in `0x00416890`, `0x00417720`, and
  `0x00442E70`, including the unsafe four-bit-only tally lookup boundary.
- Added an exact composed executable recipe with eight independent mask bits,
  an incomplete-to-`0xFF` transition latch, centered HUD/tally helpers, and a
  complete 256-byte popcount table in original linker padding.
- Preserved every applicable existing HIGHLOW relocation, PE headers, section
  tuples, file size, unknown bytes, and exact two-stage inversion to retail.
- Added a work-copy-only builder and asset-free regression tests.
- Booted the exact final hash through Direct3D, proved `0x7F -> 0xFF` rewards
  once and an already-complete pickup does not retrigger, and captured the
  natural end tally at `51/50`, `8/8`, and centered `FLIKFLIK`.
- Rejected an initial emblem placement that overlapped the first letter and
  accepted the corrected x=0 layout.

## Evidence

- [[EXP-20260815-114 - Training FLIKFLIK HUD and completion]]
- `dynamic/wine/EXP-20260815-114-receipt.md`
- `static/exports/BIN-97c95ba5572dce63/M3-training-flikflik-static-trace.md`
- [[Training FLIKFLIK HUD and completion]]
- [[FUNC-97C95BA5572D-00416890]]
- [[FUNC-97C95BA5572D-00417720]]
- [[FUNC-97C95BA5572D-00442E70]]
- [[Decision Log#DEC-20260815-111 - Complete exact eight-slot FLIKFLIK behavior]]

## Method correction

Wine WOW64 did not safely continue from execution breakpoints inside the hot
HUD/tally loops, and an inferior function call was also rejected after a GDB
internal backtrace. Accepted visual evidence uses the natural tally caller and
external scheduling, not either failed method.

## Cleanup

All owned runtime/debugger/helper instances and private sinks were closed by
exact identity. The Wine mapping was restored. Generated executables, DATs,
logs, dumps, and captures remain ignored under `work/`; `originals/` was not
modified.

## Scope decision

M3.4 closes exact `FLIKFLIK` at eight slots. It does not claim arbitrary words,
slot counts, glyph families, other levels, persistence, or new emblem art.
M3 remains Active so the next packet should preferably exercise another
gameplay stream.
