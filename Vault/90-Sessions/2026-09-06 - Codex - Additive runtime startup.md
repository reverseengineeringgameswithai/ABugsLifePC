---
type: session
date: 2026-09-06
agent: Codex
status: completed
tags: [session, terrain/runtime]
---

# 2026-09-06 - Codex - Additive runtime startup

User authorized switching to the isolated EXP-009 build. The initial and immediate prelaunch audits were clean; no previous game needed closing. Checked staged retail exe, auto-hardware exe, CD sentinel and both candidate assets. Created a fresh prefix under `work/experiments/EXP-20260905-009/preview-01`, without modifying the source prefix, and mapped its R: drive to the candidate stage.

One normal auto-hardware launch passed both content-drive identities and all six renderer markers, reached Start LevelSelect and waited one second. Actual executable is the established auto-hardware image, not the unchanged retail image retained in the stage.

The new window-name predicate stopped discovery: game `23853/183505`, group 23606, owns window 14680071 at 640x480, titled `Loading - A Bugs Life`, not `Bugs`. Same-PID window 14680072 is the 1x1 Default IME window. No active.json, menu input, RAM access, screenshot or Level01 confirmation followed. The guard has not been altered after that failure; correction approval is pending. Preserve this same running session rather than relaunching.

The postlaunch audit reports seven generic-ledger unattributed processes and private sink `ablpc_mute_23606` (module 536870916). All are accounted for through the launch group or independently checked exact-prefix/PID-start identities. The session remains open and the audit is not clean. No R2q/full suite, Git/stash, original-file mutation, debugger, signal, teleport or memory-write action occurred.

Evidence: `reports/terrain/EXP-20260905-009-runtime.json`, private `preview-01/pre-launch-audit.json`, `pre-input-log-gate.json`, `launch.json`, `pending-window-binding.json`, `post-launch-audit.json` and per-action receipts. Experiment: [[EXP-20260905-009 - Additive terrain preservation and access ramp]].

## Continuation: authorized title guard and Level01 handoff

The user approved the scoped title correction. Discovery succeeded in the same game PID 23853/start 183505; no relaunch. Normal Right (0.18 s) selected visually confirmed Anthill, Return (0.18 s) loaded Level One, and final Return (0.18 s) entered gameplay. Read-only level global `0x00861C84=1`; source-99/source-100 payloads and mesh streams 128/160/213/280 match the staged additive files. Original-start position `(197091,2734,492897)`, source-99 contact at file offset 47716; gameplay image shows the original terrain present.

The previous pending/no-input/no-RAM/no-capture facts above describe the initial startup checkpoint, not the completed continuation. Current evidence is `reports/terrain/EXP-20260905-009-runtime-entry.json`; the older report now retains its original contents under `startup_checkpoint` and points to that continuation. Three private screenshots and their hashes are listed in the entry report. No agent gameplay movement, writes, teleport, debugger control, close or second launch. No tests, full/R2q suite or Git operations. The game remains open for user checks of original ground, connector crossings and return, deck-edge fall/landing and box contact. Runtime terrain acceptance remains pending; run session-audit after eventual close.
