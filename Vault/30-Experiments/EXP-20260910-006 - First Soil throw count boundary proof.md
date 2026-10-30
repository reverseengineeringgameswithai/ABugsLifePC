---
type: experiment
id: EXP-20260910-006
date: 2026-09-10
environment: Fedora host, Python 3.14.6, offline Unicorn at two PE bases
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
question: Where does the first native Soil lesson set its six-throw advancement boundary, and does changing it change actual advancement rather than only the display?
result: Immediate byte 0043C3C2 (compare at 0043C3C0) sets the boundary and 0043C3CF the separate display constant; stock six and every configured count 1-6 advance exactly on their target event at both bases; no live input test.
status: accepted-bounded
created: 2026-09-10
updated: 2026-10-29
tags: [experiment/tutorial, re/native]
---

# First Soil throw count boundary proof

Follow-up correction: [[EXP-20260910-007 - Five-throw Training sign and native defaults]]
found that the separate initial-sign function0043C250 was not covered here.
The two-byte comparison and countdown-only traces below describe this earlier
build, not the later sign-hook build. EXP007 adds the missing initial-sign check,
original-policy defaults and a confirmed six-frame numeric resource.

This note tests whether the first original Training instruction, throwing six
berries, is a native advancement boundary that can be lowered or raised by
changing its immediate. It extends EXP-20260910-002.

## Confirmed static evidence

Authoritative original PC executable is the exact hash above, read only from
`work/copies/BUGS_PC-disc/bugs.exe`. No PS1 evidence. Fresh objdump of
0043C340–0043C400 confirms:

- Entry0043C3AF sets the stage-local counter to1 after starting LESS1.
- 0043C3B1 compares word0059D996 with17; other values skip the increment.
- 0043C3BF increments the counter. 0043C3C0 compares it with6, and0043C3C3
  keeps the lesson active while the counter is≤6. Thus six event samples,
  not five, are needed to reach counter7 and advance.
- Immediate byte0043C3C2 controls that boundary. The separate display constant
  at0043C3CF is6 too. The existing guarded patch changes both.
- Throw countdown slice00403274–004032E6 reads0059D996, skips zero and
  decrements nonzero through004032DD/004032DF. This is countdown-event sampling,
  not enemy hits or a count of arbitrary button presses.

For target3 versus the existing original-policy target6 build, exactly two
executable bytes differ: file offsets0003B7C2 and0003B7CF each change06→03.
All other patch/profile bytes are identical. This comparison is between two
Soil policy builds; it does not claim only two bytes differ from retail, since
the existing Soil framework adds its guarded sections/hooks.

## Native execution proof

`tests/test_soil_triggers.py::throw_count_proof` uses the existing offline
Tutorial harness. It executes whole native lesson0043C340 and countdown
slice00403274–004032E6. The fixture supplies timer18 at each simulated throw
start and bounded animation-register inputs, then native code decrements through
17 to0. It never supplies the lesson counter or a completed-stage state.
Win32/audio/HUD backends remain explicit stubs. This is **not** keyboard input,
actual berry spawning, whole-game scheduling or live audiovisual acceptance.

Before any event, timer values0,1,16,18 leave stage0/counter1 unchanged. Between
throws, the full countdown16→0 does not increment again. Native event17
increments once in each simulated cycle. The first instruction advances to
stage1 exactly at the configured target and retains the original30-update
inter-lesson pause.

| Target | Last event still in first instruction | Event advancing to second |
| --- | --- | --- |
| 1 | 0 | 1 |
| 2 | 1 | 2 |
| 3 | 2 | 3 |
| 4 | 3 | 4 |
| 5 | 4 | 5 |
| 6, stock and configured | 5 | 6 |

Both image bases00400000 and01000000 produce identical traces. Stock and the
target6 policy build agree exactly. The native numeric-HUD request frames are
also captured; target3 requests[1,0], target5[3,2,1,0], target6[4,3,2,1,0],
preserving original off-by-one/frame semantics without claiming rendered pixels.
Each configured image passes the builder's exact-inverse check.

Reproduce with `.venv/bin/python scripts/probe-soil-throw-count.py`; it requires
the private retail executable and refuses to overwrite its existing report.
`reports/soil-triggers/EXP-20260910-006.json` retains original/configured traces,
both bases, all six configurations/output hashes and exact changed-byte offsets.
No executable/game assets are added to tracked evidence. Derived images exist
only in the offline process; no full game copy or user project is rewritten.

## Limits

Supported action counts remain1–6. Increasing from3 to5 or6 is verified; raising
above the original6 is not enabled. Unchecked numeric-strip access at00410A20
still requires a safe HUD extension before increasing the supported range.
Live gameplay with changed throw targets remains untested; this result does not
retroactively turn EXP002's all-auto live route into an action-count proof.

Focused `make check` (`soil_triggers or studio`):49 pass,6204 deselected; M4 and
tracked-file audit pass. Initial direct pytest omitted the repository PYTHONPATH
and failed collection; using the canonical make target fixed invocation only.
No game launched or live memory accessed. Changing the goal does not rewrite the
spoken wording. Session: [[2026-09-10 - Codex - Verify first Soil throw count]].
