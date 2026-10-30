---
type: session
date: 2026-09-06
agent: Codex
status: completed
tags: [session, terrain/rendering]
---

# 2026-09-06 - Codex - Ramp culling discriminator

## Bounded question

Follow the user's request to investigate EXP-009's camera-dependent ramp disappearance. Continue the owned live Level01 session read-only and reuse the recorded camera poses. No new fixture, launch, collision edit or full-suite work.

## Evidence and result

Guarded readback identifies mesh 160 centre `(4243,-570,16018)`, radius 6047, projection 640x480 with focal 320. The original renderer's whole-scene gate is confirmed by bounded Ghidra queries and copied-retail raw disassembly. Independently authored `work/experiments/EXP-20260905-009/ramp-culling-probe.py` runs the original instructions from `0x0044D59F` through accept/reject, including transform `0x00448230`, offline against retail SHA `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

The hidden baseline and early post-tap views fail the horizontal branch `0x0044D677 -> 0x0044D728`; the visible late and settled poses pass. Radius-only 8192 makes all five sampled poses pass. Original Euler conversion `0x00463C80` reproduces the settled current camera matrix exactly. The intermediate visually unclear view already passes with 6047: preserve that discrepancy and the sparse, non-frame-synchronous camera/capture limitation. No general mesh-size rule or complete live remedy follows.

Public result: `reports/terrain/EXP-20260905-009-ramp-culling.json`; previous visual/contact pairing: `reports/terrain/EXP-20260905-009-ramp-visibility.json`. Full arithmetic, file offsets, pointers and bounds are in [[EXP-20260905-009 - Additive terrain preservation and access ramp]]. Private native report and read receipts stay under `work/experiments/EXP-20260905-009/`.

## Next exact experiment and lifecycle

Proposed, not executed: user-authorized two-byte radius A/B/A at RAM `0x0064CA47`, 6047 (`9f 17`) -> 8192 (`00 20`) -> 6047, compare-before-write each transition and record receipts/captures in the same owned PID 23853/start 183505. Do not change collision, actor, camera, code, files, registers or process execution. Current user permission for conditional writes is not treated as exact authorization for this newly specified use.

No live writes, asset edits, tests, R2q/full suite, Git, launch or close. Game remains open. A helper-import attempt failed on the CLI's missing argument before performing the requested memory read; supported read commands completed the readback without modifying the operator. Run session-audit after eventual close.
