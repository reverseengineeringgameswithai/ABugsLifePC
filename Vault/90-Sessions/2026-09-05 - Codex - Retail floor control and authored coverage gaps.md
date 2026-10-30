---
type: session
date: 2026-09-05
agent: Codex
status: complete
created: 2026-09-05
updated: 2026-09-05
tags:
  - session
  - terrain/collision
---

# Retail floor control and authored coverage gaps

## Goal

Use the user's current authored-level position/facing in OG to investigate missing floor support, with explicit authorization for the one-time transfer and RAM-backed normal-input observation.

## Experiment and conclusions

[[EXP-20260905-007 - Retail position control and missing floor footprints]] records the authoritative scope, evidence, failed setup gates, and open session. The retail four-second Up control completed with 301 RAM samples and no sampled NextLife trigger. Runtime references to retail source-99 cells `44140` and `44248` agree with offline footprint queries; neither footprint has an active floor candidate in the authored terrain. Retail cell `45884` covers the earlier fall endpoint; authored traversal has no candidate there.

The test supports a layout-assembly coverage problem caused by replacement of source 99, not a universal failure of authored box contact. It is not an exact earlier-fall replay. The setup's cached old contact pointer persisted while stationary and refreshed only after normal movement; the initial movement transient limits trajectory matching.

## Changes and lifecycle

Only private experiment operators/evidence and documentation were added. No terrain assets or shared implementation code were edited. The original authored preview and first wrong-level retail attempt were closed with clean audits. The second retail launch reached Level01 and remains open for the user at the end of the control, PID/start `313931/10570967`, group `313689`.

The user-authorized 24-byte two-vector position transfer and separate eight-byte two-vector facing transfer were consumed exactly once, with guards and readback. The subsequent Up control performed zero memory writes. No debugger, ptrace, process stop, register access, save state, or PS1 evidence was used.

## Tests run

No pytest, R2q suite, or full `make check` was run. This was a runtime comparison/documentation session, not an implementation bank or commit. Native resident-asset checks, session audits at launch/close boundaries, the bounded input/observation controls, and selected offline geometry queries are recorded in EXP-007. Historical run-index debt remains 14 uncited runs and one dangling citation; it was not repaired here.

## Recommended next action

Prove the earlier fall's exact native-instruction trajectory and design continuous authored/retail collision coverage with deliberately paired rendering. The user has also approved the EXP-006 area's general playability; that does not close the newly reported outside-deck coverage defects.

## Git commit

None. Documentation and private runtime evidence are not newly banked. Prior checkpoint `0db2b6c373cd62eaa824ee59e3b12cb37604e4ce` and protected stash were not modified by this work.
