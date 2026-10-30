---
type: session
status: completed-bounded
created: 2026-09-10
updated: 2026-10-29
agent: Codex
tags: [session/codex, re/tutorial, re/native]
---

# Verify first Soil throw count

User asked whether Mr. Soil's first six-berry task was statically understood and
could have its count changed as proof. Rechecked original instructions and ran
new explicit native boundary checks for all1–6 targets at two PE bases.
[[EXP-20260910-006 - First Soil throw count boundary proof]] records the evidence.

Original stage0 samples word0059D996==17, increments a counter starting at1,
and advances when it exceeds6. Existing patch updates both the comparison
immediate0043C3C2 and HUD constant0043C3CF. Between3-count and6-count policy
images these are the only differing bytes. Native timer-decrement slice plus
whole lesson execution confirms each target advances exactly on eventN, never
N-1; other timer values do not count. This is offline simulated throw cycles,
not real keyboard input, berry spawning or a live gameplay demonstration.

Added two-base regressions to `tests/test_soil_triggers.py` and reproducible
`scripts/probe-soil-throw-count.py`; metadata report under reports/soil-triggers.
The proven range is 1–6; a count above 6 still needs safe numeric-HUD support.

Original executable 97c95ba5…a27b878. No media or executable file modified. No
launch/reopen, keys, live memory operation, game-process stop or private sink.
Session audit clean.

Initial direct pytest failed collection because PYTHONPATH was omitted, before
running tests. Canonical focused make check then passes49,6204 deselected;
M4 compatibility and tracked-file audit pass. No full-suite or live-count
acceptance claimed. Relevant guides/handoff, unknowns/decision register, MOCs,
experiment and session index updated. Final Vault lint:887 notes,0 errors,
8 preexisting warnings. Whitespace checks pass. No commit.
