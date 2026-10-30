---
type: experiment
id: EXP-20260905-002
date: 2026-09-05
status: bounded-complete-test-arms-closed
question: Does the alternate-diagonal box retain contact and visibility through reversals and other camera views?
environment: Two sequential isolated Wine hardware arms; ordinary XTEST and read-only state; original user game preserved
result: Five valid reversal sweeps stay grounded and outside walls; new paused occluding view has no reconstructed top-depth inversion; one navigation route rejected
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
created: 2026-09-05
updated: 2026-09-05
tags: [re/experiment, re/rendering, re/collision]
---

# EXP-20260905-002 - Box movement and occluding-view validation

The user says “Keep going” after [[EXP-20260905-001 - Box top diagonal live comparison]],
then “continue where you left off” during this work. Continue DEC-238's normal
movement/view tests using file-loaded copies. No new memory-write authority is
inferred or reused. The original paused failure is preserved in game
46701/start 1147812 throughout; only one new research instance runs at a time.

## Confirmed finite movement results

Five eight-second reversal sweeps record 518 position/contact/camera samples
and 107 native frames. Every sampled player reference position stays outside
the tested wall, at deck Y -102403 through -102400 with contact source 99.
This is a measured reference-point/contact result, not a claim about every
animated limb's physical extent or every unsampled frame.

| Placement and wall | Samples | Frames | Tangential reversals | Distinct camera matrices |
| --- | ---: | ---: | ---: | ---: |
| Original-location west | 103 | 21 | 19 | 29 |
| Original-location north | 106 | 22 | 19 | 20 |
| Original-location east | 106 | 22 | 19 | 22 |
| Stationary occluding west | 101 | 21 | 20 | 30 |
| Stationary south | 102 | 21 | 19 | 15 |

Reversal counts ignore adjacent tangential displacements smaller than 32 world
units. They measure the traces, not an assumed count from input intent. Inputs
alternate tangential direction while pressing toward the wall and are recorded
separately. Moving compositor frames and state reads are asynchronous.

In the original-location arm, an ordinary jump lands at
`(179083,-108545,501690)` with top contact pointer 6973639. Flik crosses the top
and steps off to the west; the subsequent settled deck state is
`(150599,-102401,512342)` with contact pointer 6973595. Reapproaches to walls
remain grounded. These extend EXP-006's contact regression without changing
its collision layout or repairing EXP-005's separate floor patch.

## Rejected navigation and corrective test

The first original-location south route is **invalid**, not a fourth accepted
wall test. Its waypoint was reached transiently, but release/settle movement
carried X to 149972. The next press stopped on the west side at
`(163006,-102400,502445)`. The sweep lacked an explicit intended-side gate and
its positive-Z component then ran along/outside the west edge to the finite
deck boundary. The boundary guard stopped the sweep; terminal release state
was `(196363,-102145,581894)`, beyond the deck's Z limit 579200.

Do not label this a hole in the box or a shared-floor defect. Preserve the
failed route, error and all its frames in
`alternate/navigation-rejection.json`, `south-route.log` and the per-step
receipts under `work/experiments/EXP-20260905-002/`.

The later stationary sweep requires the measured intended wall band at every
sample, in addition to level/deck/height limits. Its south retry starts at
`(211878,-102402,473344)` and stays below the south plane Z 473600 through all
102 samples. Original-location south coverage remains unaccepted; south
coverage in the table belongs to the explicitly translated stationary fixture.

## New occluding view and original-instruction check

Several perimeter frames show Flik in front of the box. They cannot by
themselves establish occlusion. Reuse EXP-008's stationary box, between the
initial camera and player, with the same alternate 4x4 top. The new builder
reproduces the old stationary fine-control DAT hash exactly before changing
only the 138 bytes in its top-face table. Geometry, dimensions and collision
match that existing stationary control.

After stationary west reversals, a normally paused triplet preserves the close
edge view for classification. All three RGB regions x 260–354, y 275–339 match
exactly. Read-only copying captures 55 low-address mappings, 131,002,368 bytes
over 6.887 seconds; position/contact/camera match before and after. The copy is
**non-atomic and not a restorable save state**. No signal or debugger is used.

Reuse EXP-009's original-instruction operator unchanged on that captured copy:

| Original entry | Instructions | Output | Match against retained live vertex tuples |
| --- | ---: | --- | --- |
| 0x004498F0 | 22,586 | 84 mesh vertices | 84/84 tuples, no full consecutive run |
| 0x0044C440 | 128,735 | 355 actor vertices | 179/355 tuples, no full consecutive run |

Both calls return within their 2,000,000-instruction ceiling. Retail `.text`
is hash-verified; stack/table and output counters are synthetic offline setup.
No drawing/API replacement is used. Depth-store anchors remain EXP-007/009's
0x0045D005 and 0x0045E9BF–0x0045E9D4.

**Bounded classification:** 485 blue pixels are inspected below the pause menu;
all 485 have reconstructed actor coverage. Twenty-eight also intersect the
analytic box-top footprint. At all 28, the reconstructed actor is in front of
that top intersection; the other 457 rays miss the top footprint. Zero samples
show the earlier analytic-top-before-actor inversion. The edge pixels in this
paused diagnostic therefore do not supply a new demonstrated depth leak.

This is exploratory post-hoc classification at integer pixel positions, with
partial actor-buffer corroboration. It does not simulate texture alpha,
rasterization rules or every animated view. Keep EXP-001's exact control/alternate/
restoration result distinct from these normal moving observations.

## Provenance, controls and final handoff

Both new arms execute auto-hardware build SHA-256
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
Fresh logs pass all six hardware markers plus the exact R-drive content
identities. The route is settled LevelSelect, held Right, Anthill screenshot,
held Return, exact loaded Level01/title, then held Return into gameplay.
Copied prefixes have private R mappings; historical mappings are unchanged.

- Original-location candidate DAT:
  `572d244f1cc053ef29d2c343e4311a6ff20237c2259c5e84867bade53d57c247`.
  TERRAIN.ALL: `26f3e0235533419a80b2a0eff18f423fadc20617a6c2ed2be445abeae87b35d5`.
  All 2,251 staged files excluding the fresh log match the user stage except DAT.
- Stationary candidate DAT:
  `fcadd51a941e0ec46990d4dbff8a9a881f4595d24c98991ef30ea1dd7622f895`.
  TERRAIN.ALL: `4b07d2d253964e1685558014c0100d56ba09294dd71a28a8030d8330a829c57e`.
  The reproduced stationary fine control is `4388dba5...cdfb25` (EXP-008).
- Exact loaded render/collision prefixes, instance/object fields and pointers
  match before and after each arm. Capture sockets are bound by SO_PEERCRED
  to each owned Gamescope group, using `gamescope-1` on nested display `:3`.
  The user's `gamescope-0` / `:2` is never sent input or captured here.
- Original-location game 120500/start 6076269, group 120246, and the stationary
  arm's exact identities are retained in their launch/discovery/close receipts.
  Both arms close with identity-guarded normal-close/termination cleanup.
  Each post-close audit exactly equals the original seven-process/sink baseline.
- Final read-only original-user preflight equals the initial one: the old mesh,
  collision, player/contact/camera and paused game are unchanged. No live memory
  write, process suspension, breakpoint or register operation occurred here.

`reports/terrain/EXP-20260905-002.json` retains numeric summaries and 728 hashed
artifacts; companion operator text preserves the procedures. Raw frames,
memory and geometry remain under ignored `work/`. The interactive viewer is
`work/experiments/EXP-20260905-002/comparison.html` (unaltered captures, CSS
scaling). Its JavaScript and all frame references are checked.

DEC-239 retains this finite regression and advances the next bounded task to
EXP-005's shared-floor return failure. Universal mesh rules, every-view
occlusion, arbitrary layouts and original-location south traversal are not
claimed complete.
