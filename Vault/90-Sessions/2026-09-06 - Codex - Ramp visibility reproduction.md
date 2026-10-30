---
type: session
date: 2026-09-06
agent: Codex
status: completed
tags: [session, terrain/rendering]
---

# 2026-09-06 - Codex - Ramp visibility reproduction

## Scope and result

Continued [[EXP-20260905-009 - Additive terrain preservation and access ramp]] in the existing isolated Level01 session. User reported the requested ramp crossings work without falling through or sideways sliding, then reported terrain disappearing on descent or at some angles, flashing after a very short Down tap and appearing after turning. User clarified that Flik was on the new ramp near original ground, not on the original floor.

Normal input and read-only RAM/captures reproduced a camera-dependent visual difference. Contact `[99,6991679]` maps to appended ramp cell 49008. A requested 1 ms tap gave no observed pose/camera change; an announced 50 ms tap registered. All three post-tap frames retained position `(192863,-97167,359200)` and that contact while camera rotation changed the ramp from not distinctly visible to visible. Sparse samples do not establish continuous contact or reproduce the flashing frequency.

## Evidence and remaining work

Public report: `reports/terrain/EXP-20260905-009-ramp-visibility.json`. It records camera matrices/translations, exact contact conversion, capture hashes and input timing limitations. Private screenshots and per-action receipts are in `work/experiments/EXP-20260905-009/preview-01/`.

Culling/bounds, face-facing/clipping and draw ordering/overlap remain hypotheses. Next discriminator: offline original-PC render-stage comparison at the captured camera poses, then isolated established-field A/B if justified. Retain the failing visual fixture and working collision. No asset changes, memory writes, teleport, debugger control, tests, full/R2q suite or Git operations. Game PID 23853/start 183505 remains open for the user; no launch/close, and audit remains required after eventual close.
