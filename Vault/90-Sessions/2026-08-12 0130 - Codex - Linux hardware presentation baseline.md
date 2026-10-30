---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
---

# Linux hardware presentation baseline

## Agent

Codex

## Goal

Explain and correct the game's undersized Linux presentation, test the result before adopting it, and preserve the confirmed hardware-accelerated workflow in Git and the Obsidian Vault.

## Files inspected

The unchanged work-copy executable, current and retained game logs, Wine prefix mappings, compositor captures, Gamescope package/help output, project launch scripts, and runtime/environment notes.

## Experiments inspected

[[EXP-20260812-005 - Wine training baseline]] and [[EXP-20260812-007 - Gamescope hardware presentation baseline]].

## Changes made

- Added a hash-verifying `scripts/play-pristine.sh` wrapper for the tested Wine/Gamescope configuration.
- Made 4:3 `fit` scaling and hardware-renderer selection explicit.
- Kept nearest filtering as the tested default and exposed linear filtering as an optional softer resample.
- Added Gamescope to the generated environment inventory.
- Recorded the exact command, renderer log excerpt, capture measurements, decision, limitations, and follow-up unknowns.

## Conclusions

The primary cause of the unexpectedly small, coarse gameplay was selection of the game's 320×200 software renderer. The hardware option starts Direct3D at 640×480×16. Gamescope can fit that surface to display height without stretching it away from 4:3. Evidence: `RUN-WINE-20260812-013633` and `EXP-20260812-007`.

## New hypotheses

Browser/video resampling likely explains some remaining softness in uncontrolled online footage, but the footage's source configuration is unavailable and the claim remains inference.

## Contradictions discovered

None. The full-screen opening movies did not imply that later software-rendered gameplay was also 640×480; the game log discriminated the separate rendering paths.

## Tests run

Live unchanged-executable run in software and hardware modes; compositor PipeWire captures; ImageMagick bounds measurement; executable and log hashing; launcher help/dry-run and negative validation; project checks.

## Unresolved questions

See KU-012 and KU-013 in [[Known Unknowns]]. Exact Windows 98/WineD3D fidelity and persistent renderer selection are not yet established.

## Recommended next action

Resume the PC-native watchpoint experiment on training records 124–126. Treat a controlled Windows 98 visual comparison as optional unless a rendering difference becomes material to mod validation.

## Git commit if applicable

Bounded commit message: `feat: add hardware-accelerated Linux play baseline`.
