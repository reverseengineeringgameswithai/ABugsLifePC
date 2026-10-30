---
type: session
date: 2026-09-06
agent: Codex
status: completed
tags: [session, terrain/runtime]
---

# 2026-09-06 - Codex - Live ramp radius comparison

## Exact scope and authorization

The user approved changing only the two-byte mesh-160 scene radius at `0x0064CA47` in game PID 23853/start 183505 from 6047 to 8192 and restoring 6047. A normal 50 ms Down tap prepared the hidden view; no input occurred during the three comparison arms. No collision, actor, camera, code, register, asset or process-control intervention was authorized or used.

## Result

Both initial control captures lack the distinct ramp strip beneath Flik. Both candidate captures show that surface. Both restored controls lack it again. Six captured states plus bracketing readbacks have identical position `(192607,-97057,358628)`, source-99 contact pointer 6991679 mapping to appended cell 49008, camera matrix `84f10000cc0600000010000034f9000084f1` and camera translation `(204439,-109864,384878)`. PNG size stability over 200 ms was recorded; all six images were visually inspected. Continuing actor and vegetation animation prevents an exact full-frame restoration claim; no calibrated pixel mask was used.

This confirms a radius/culling contribution to the fixed-pose disappearance, corroborating [[2026-09-06 - Codex - Ramp culling discriminator]]. The original 6047 value was restored and read back. No permanent file correction exists yet. The intermediate captured-view discrepancy, flashing frequency, robust bounds design and camera sweeps remain unresolved.

## Evidence and lifecycle

`reports/terrain/EXP-20260905-009-ramp-radius-live.json` preserves exact authorization, two write intents/readback receipts and all capture identities/states. Private operator: `work/experiments/EXP-20260905-009/ramp-radius-live-ab.py`. Private receipts: `work/experiments/EXP-20260905-009/preview-01/radius-ab-01/`. Full interpretation is in [[EXP-20260905-009 - Additive terrain preservation and access ramp]].

The original fixture remains loaded with radius 6047; session open for user. Two authorized two-byte writes completed, no further write permission inferred. No other live writes, asset edits, debugger/stops, launch/close, tests, full/R2q suite or Git operations. Run session-audit after eventual close. Next: design PC-compatible scene bounds or partitioning, retain the failing fixture, add bounded offline regressions and compare a fresh file-loaded candidate across camera angles.
