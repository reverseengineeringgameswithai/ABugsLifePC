---
type: session
date: 2026-09-05
agent: Codex
status: recorded
evidence:
  - EXP-20260905-004
---

# Playable ramp and box area

Started clean at23978fe7df3d93f6b085a2ee8c81c818b10d31ba with no live runtime.
The user explicitly chose a small playable area from the working pieces: ground,
gentle ramp, banked standable box and normal return. Terrain-only validation;
no R2q or full-suite rerun. Run/index checked before assigning EXP-20260905-004;
the existing14 uncited runs and one dangling historical citation remain separate.

## Delivered

[[EXP-20260905-004 - Playable ramp and box area]] provides the bounded builder
`reimplementation/ablpc/terrain_play_area.py`, reproducible build/staging/probe
script `scripts/terrain-play-area.py` and19 new regressions. The exact banked
4x4 alternate top is retained. A rise192/run1400 east ramp and connected side
profiles fit source99 and primary160's established allocations; unknown bytes
outside the selected prefixes and opaque vertex fields are preserved.

The fresh playable copy is `work/copies/EXP-20260905-004/game/`; launch with
`work/copies/EXP-20260905-004/play.sh`. Its README explains normal Anthill entry,
ramp location, controls and rebuilding into fresh destinations. It is an elevated
local test deck, not a completed retail-level replacement or landscape connection.

## Evidence and validation

Six paired original-instruction routes (three lanes, two speeds) pass with
explicit deck/ramp/top transitions, plus natural-spawn approach, landing and
step-off. The original closed-wall control blocks the intended ascent.
One rejected bootstrap seed is recorded, not silently counted as a geometry test.

A fresh normal-input runtime completes two ascent/descent cycles without jumping,
then a top jump/landing and a west step-off.554 state samples and13 captures are
retained, with loaded-byte checks before/after and exact compositor/process guards.
No live writes, teleport, debugger, STOP/CONT, registers or save states; no PS1.
All2251 staged files were hashed; only the two intended level files differ.

New regressions19/19 in17.29seconds; seven-file terrain gate118/118 in26.51seconds.
R2q/full suite deliberately not run. Public report:
`reports/terrain/EXP-20260905-004.json`; private snapshot provenance:
`reports/terrain/EXP-20260905-004-preservation.json`.
The test instance is closed and the unrestricted final runtime audit is clean.

## Decision and handoff

DEC-242: compose a useful playable area from the banked pieces, preserving finite
scope instead of repeating the box/blob demonstrations. Ask for play feedback
before adding features. EXP-003's blocked source100 route, general layouts and
all-view/material guarantees remain separate unknowns.

Current State, Environment Status, Project Roadmap, authoring roadmap, Known
Unknowns, Decision Log, relevant MOCs and Session Index are updated. Originals,
protected stash76db1c9ee1ffffce52cea6aee591c24ab6a1c39a, and older snapshots are
not modified. Private assets, screenshots and prefixes stay under ignored work/.
