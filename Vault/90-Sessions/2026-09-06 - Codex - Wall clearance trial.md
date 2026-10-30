---
type: session
date: 2026-09-06
agent: Codex
status: completed
tags: [session, terrain/collision]
---

# 2026-09-06 - Codex - Wall clearance trial

## Outcome

[[EXP-20260906-004 - Wall clearance comparison and offset trial]] is now live at the normal Level1 start for the user. This is a collision-only1536-world-unit outward clearance trial on the20 ramp-side groups. Render data and original collision are unchanged. Visible-overlap improvement remains unconfirmed until user testing.

## Evidence and limits

Report `reports/terrain/EXP-20260906-004.json` records the live control's50 samples (124..294 world units outside the west plane), original-PC point/motion cases, original/render geometric separation, contradictory original offsets, exact modified words and complete candidate hashes. Original geometry supports a local trial, not a universal radius. Native original-wall comparison is offline: the24-press live navigation attempt left the upper terrain without reaching its target; user reported the fall, read-only state retained ground contact, and navigation stopped. That receipt is retained as unsuccessful navigation, not a matched runtime test.

New bounds-checked writer and reproducible probe are `reimplementation/ablpc/terrain_wall_clearance.py` and `scripts/terrain-wall-clearance-probe.py`. Tests `tests/test_terrain_wall_clearance.py` add47 synthetic cases across two layouts. **69 affected tests passed in0.15s**, both native arms accepted their15 outcome groups each in**31.294611875s**, and the focused terrain gate passed**72/72 in26.68s**. Original EXP-003 fixed-axis route failure remains historical; only the declared steering-controlled routes were accepted here. No R2q/full suite or Git commit.

## Runtime handoff

EXP-003 closed with no survivors through the existing normal-request/scoped-fallback procedure; normal-close-only success not independently established. Clean post-close and immediate prelaunch audits. Cold prefix copy, isolated stage and fresh staged log; one auto-hardware launch. Anthill/title screenshots gated each Return. No new-trial gameplay movement or live memory writes.

Game **71867/start1283745**, group/leader **71598/start1283612**. Gamescope71616/start1283614, Xwayland71642/start1283639, display`:2`, window14680071. Sink **ablpc_mute_71598**, observed reusable module536870916. Prefix `work/experiments/EXP-20260906-004/preview-01/prefix`. Full sources99/100 and listed render streams match candidate files; bound8560 unchanged. Seven generic-registry processes and one sink independently accounted, not a clean postlaunch audit. New preview deliberately remains open.

## Next

User visual test: press into both ramp sides, inspect body overlap and walk around the lower corners/clearance strip. Visual success, corner/end-entry coverage, draw-order contribution and ground-trim outcome remain bounded/open. Keep EXP-003 as control; do not widen the margin blindly or generalize48 stored units to all walls. Full evidence, exact offsets and receipts are in the experiment/report.
