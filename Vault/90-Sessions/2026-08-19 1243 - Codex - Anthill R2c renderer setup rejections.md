---
type: session
date: 2026-08-19
agent: Codex
topic: Anthill R2c renderer setup rejections
tags:
  - session
  - re/runtime
  - re/level-format
---

# 2026-08-19 1243 - Codex - Anthill R2c renderer setup rejections

## Goal

Begin the authorized R2c retail-only F0 calibration, fail closed on renderer or
lifecycle defects, and use James to audit the next runtime boundary.

## Authorization and boundary

The user authorized exact-PID `SIGSTOP`/`SIGCONT`, the two bounded read-only
view-block snapshots, and conditional guarded localizer creation plus C1/L/C2.
They explicitly prohibited runtime memory and debugger writes.

F0-001 and F0-002 did not reach F0. Each fresh retail setup used the exact
retail executable and Level01 identities and stopped after the complete log
selected the software path: `SYSTEM MEMORY ONLY`, `320x200`, and
`INITSOFTRENDER`. Neither setup sent carousel/title input, signaled a process,
read `/proc/<pid>/mem`, or wrote a DAT.

## Evidence and cleanup

- Raw setup packets are retained under the ignored
  `work/copies/EXP-20260819-002/evidence/rejected/` boundary.
- Both runs retained their clean pre-audit, stable chooser captures, guarded
  input receipt, complete renderer log, and accounted post-close audits.
- Normal Alt+F4 did not terminate either rejected process. The exact owned
  launch groups were cleaned explicitly. Residual Wine-device processes were
  recorded by the intervening audits, including PID, start tick, command, and
  name, before exact-PID cleanup. Final post-close audits are clean.
- The Wine `R:` mapping was restored to the recorded original target. No game
  or generated evidence artifact entered git.

## Decision and next action

Recurring chooser screenshot hashes remain forensic only and do not prove the
selected renderer. Commit `ae13c10611afd775a686e92cff9efde58d9e4b8a` freezes a
bounded log-classified amendment: fresh RC0 sends no direction before Return;
if RC0 is software, fresh RC1 is the sole one-Down fallback. A hardware result
graduates in-process into F0. There is no third attempt.

At that session checkpoint, the guarded face-8 localizer remained uncreated and prohibited until a
hardware-qualified F0 completes, its result is documented and committed, and
James accepts that packet.

## Links

- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[2026-08-19 0245 - Codex - Anthill R2c offline freeze and localizer packet]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[PC autonomous game control]]
