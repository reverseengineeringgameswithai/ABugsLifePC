---
type: session
date: 2026-08-14
agent: Codex
topic: Training FLIK letter transformations
updated: 2026-08-14
tags:
  - session
  - milestone/m3
  - re/gameplay
---

# Training FLIK letter transformations

## Goal

Continue M3 with the user's requested letter-pickup mod. Preserve the original
intent beyond simple append: support moving, duplicating, and removing exact
letter records, while the accepted demo duplicates all four existing FLIK
selectors at deliberately moved collectible positions.

## Work completed

- Refreshed START HERE, current/environment state, charter, operating manual,
  roadmap, and relevant MOCs/dossiers.
- Mapped the four exact singleton records and selector-specific pickup mask
  branches in PC functions `0x00456A90` and `0x00417720`.
- Added a hash/layout-locked table rewrite that supports signed table growth or
  shrink, relocates 556 known fields, reparses, and proves exact inversion.
- Added the exact duplicate-FLIK recipe, work-copy-only CLI, and asset-free
  synthetic tests for move/duplicate/remove behavior.
- Built a complete candidate whose only game-content difference from the
  accepted M3.1 tree is Training `LEVEL1.DAT`.
- Booted the unchanged executable through hardware Direct3D and confirmed
  type-`0x3F` count 67 plus all four terrain-initialized moved copies.
- Independently collected all four duplicate selectors and observed mask bits
  `1`, `2`, `4`, and `8`, while each original counterpart remained intact.
- Confirmed the hard boundary: a duplicate pickup with mask already `0x0F`
  increments the existing completion/reward byte `1 -> 2`.

## Evidence

- [[EXP-20260814-113 - Training FLIK letter transformations]]
- `dynamic/wine/EXP-20260814-113-receipt.md`
- `static/exports/BIN-97c95ba5572dce63/M3-training-letter-static-trace.md`
- [[FUNC-97C95BA5572D-00417720]]
- [[FUNC-97C95BA5572D-00456A90]]
- [[Decision Log#DEC-20260814-110 - Complete M3.3 with explicit duplicate-letter retrigger behavior]]

## Method correction

Wine's WOW64 guest faulted when GDB continued from execution breakpoints at
`0x00417A59` and `0x00417C77`, including a hardware-breakpoint continuation.
Those arms are rejected. Accepted discriminators use one hardware breakpoint,
record the state, and detach without debugger continuation.

## Cleanup

All owned game, Wine, Gamescope, reaper, debugger, capture-helper, and private
sink instances were closed by exact identity. The Wine `Y:` mapping was
restored to the prior M3.1 complete-tree candidate. Game bytes, logs, dumps,
and captures remain ignored under `work/`; `originals/` was untouched.

## Scope decision

M3.3 is complete as a data-edit packet even though duplicate letters retrigger
the normal completion/reward. That behavior is documented, not suppressed.
A one-shot reward would be a distinct executable-code goal.

## Next packet

Prefer a different gameplay stream—trigger/checkpoint or collision/traversal—
unless the user explicitly asks to redesign duplicate-letter completion.
