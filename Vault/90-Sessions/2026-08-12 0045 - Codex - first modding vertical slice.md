---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
---

# First modding vertical slice

## Agent

Codex

## Goal

Implement the Wine-first plan through a safe PC level-data parser, manifest workflow, and original-executable runtime test while keeping Windows 98 off the critical path.

## Files inspected

Exact `bugs.exe` static export; 21 PC `LEVEL*.DAT` files; training `CD/LEVEL07/LEVEL1.DAT`; Wine logs and screenshots.

## Experiments

[[EXP-20260812-005 - Wine training baseline]] and [[EXP-20260812-006 - LEVEL DAT prefix and manifest mod]].

## Changes made

- Established `make check` and tracked-content auditing in commit `4947e11`.
- Added Wine game-log capture.
- Added `reimplementation/ablpc/`, `scripts/ablpc-mod`, tests, an evidence-backed manifest example, and implementation documentation.
- Added function and file-format dossiers without semantic overnaming.
- Recorded runtime control/mod evidence and kept all game-derived outputs ignored.

## Conclusions

Wine is sufficient for the current Linux edit-test loop. The bounded DAT prefix and three-record manifest edit are accepted by the original executable. A compositor-level A/B confirms that the edit removes the central foreground flower cluster.

## Contradictions discovered

Early edited runs faulted at `0x004A84A4`, but an unmodified control faulted identically. Preserving the `X:\PC\BUGS` drive layout made both control and edited runs initialize, discriminating path layout from file validity.

## Tests run

Unit/regression suite, Vault lint, tracked-content audit, `git diff --check`, 21-file corpus scan, Wine software/hardware baseline, direct-path negative control, and exact-layout control/mod runs.

## Unresolved questions

The individual roles of primary records 124–126, the remaining DAT suffix, and the direct-path loader fault remain unknown. See KU-008 through KU-010 in [[Known Unknowns]].

## Recommended next action

Attach PC-native watchpoints to records 124–126 and determine whether they are LOD variants, culling records, or transforms.
