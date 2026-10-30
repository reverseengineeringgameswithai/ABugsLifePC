---
type: experiment
id: EXP-20260905-001
date: 2026-09-05
status: completed-bounded-original-restored
question: Do alternate top diagonals remove the six remaining fragments at the preserved paused pose?
environment: Existing Wine hardware game; four guarded mesh writes with brief stops and exact restoration
result: Six residual fragments disappear and return on control restoration; all 255 prior fixes retained; 15 matched-state captures
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
created: 2026-09-05
updated: 2026-09-05
tags: [re/experiment, re/rendering, re/collision]
---

# EXP-20260905-001 - Box top diagonal live comparison

**Subsequent movement/view evidence:**
[[EXP-20260905-002 - Box movement and occluding-view validation]] supplies
five finite reversal sweeps and a new paused occluding-edge diagnostic. Its
limits and rejected navigation route remain explicit; DEC-239 returns the
next bounded task to EXP-005's separate shared-floor failure.

**PC confirmed at this paused view:** changing the finer box's top diagonals
removes all six retained residual fragments. Restoring the finer control brings
all six back. All 255 samples corrected by subdivision remain hidden in both
fine variants. All 15 captures match the measured player/contact/camera state;
both restored controls match their initial 3,575-pixel regions exactly.

This executes the unchanged plan and operator prepared in
[[EXP-20260904-011 - Box top diagonal edge discriminator]]. Its authorization,
write and capture receipts remain under `work/experiments/EXP-20260904-011/`;
this dated follow-up keeps the prior offline report and pinned plan unchanged.
No consumed EXP-010 transaction was rerun.

## Authorization, identity and intervention

The user explicitly authorized “four guarded memory writes, brief process
stops/register reads, and exact restoration afterward.” Fresh authorization
records the complete user text, time, plan SHA-256
`3c808a26cfca977045b23aabf8c8323ead9d10c2ceafcde22875aef7b076063f`
and operator SHA-256
`3bd8d81482ce7760070c2a57b61a8ce6bde65e18803f14838887ce03481ceae3`.
All 25 prepared artifact hashes passed before execution. An exclusive start
receipt consumes this transaction; do not rerun it or reuse this authorization.

The same session `USER-20260904-deck-depth-play-001` remains live:
game 46701/start 1147812, group 46458, display `:2`, window 14680071,
sink `ablpc_mute_46458`. Guards check process/cwd, mapped instructions, object
pointers, zero depth-offset byte and all six hardware log markers. Executed
auto-hardware SHA-256:
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.

Position `(163024,-102401,509900)`, contact `(99,6973595)`, terrain base 0,
barrier head 7152075, camera translation `(190254,-115203,500135)` and matrix
`81050000050f000000100000fbf000008105` match the previous evening's failure.

| Write | Address | Bytes | Transition |
| --- | --- | ---: | --- |
| apply_control | 0x006662A7 | 1,078 | Original six-quad mesh → finer control |
| apply_diagonal | 0x006664DB | 256 | Finer control → alternate top diagonals |
| restore_control | 0x006664DB | 256 | Alternate → finer control |
| restore_original | 0x006662A7 | 1,078 | Finer control → original mesh |

Every write passes full-prefix comparison, complete write length and full-prefix
readback. All 45 vertex records, 33 faces, collision, dimensions, shared-edge
positions and object depth offset are identical between the fine variants.
Only 138 bytes differ in their 256-byte top-face table: cyclic corner rotation
of each of 16 top quads, with corresponding UV fields. The 530-byte collision
prefix at 0x006A6863 is checked around every phase and after restoration.

Fifteen scoped process stops include read-only ptrace register inspection;
four satisfy the retained EXP-010 frame-limiter gate, first game return
0x00405B74 and enclosing renderer return 0x0044DBF3. The longest stop was
65.964 ms. No breakpoint or register write was used. Final inspection finds
all 16 threads running/sleeping, none stopped, and TracerPid 0.

## Frozen measurements and controls

The native ROI is x 285–349, y 285–339. Retain the existing blue classifier
`B > R + 6 and B > G + 2` and EXP-009/010/011 sample selection unchanged.
Each table value is reproduced in all three captures for that arm.

| Blue sample count | Original | Finer control | Alternate | Control restored | Original restored |
| --- | ---: | ---: | ---: | ---: | ---: |
| Six residuals | 6 | 6 | 0 | 6 | 6 |
| All 259 analytic samples | 259 | 6 | 0 | 6 | 259 |
| Prior 255 inversion samples | 255 | 0 | 0 | 0 | 255 |

The six points are (342,315), (344,315), (298,319), (299,319), (300,319),
(301,319). The report retains their RGB values in every capture. Each arm's
three ROI byte strings are identical. Both original/restored-original and
control/restored-control pairs restore every ROI pixel. Original and fine-control
ROIs also exactly match the corresponding EXP-010 triplets from the prior day.
This is measured ROI agreement, not full-frame equality.

**Supported mechanism:** original PC 0x004498F0 drawing instructions in EXP-011
predict the six ordering changes, and this live diagonal-only comparison
agrees. Residual depth interpolation error is strongly supported. Triangle/UV
ordering also changes texture interpolation; total texture differences alone
are not disappearance evidence or a complete renderer model.

## Evidence, validation and handoff

- `reports/terrain/EXP-20260905-001.json`: numeric result, write summaries,
  capture references, sample colors, restoration check and 41 hashed artifacts.
- `reports/terrain/EXP-20260905-001-analyze-operator.txt`: independent read-only
  analysis procedure; verifies receipts, all 15 image hashes/states and frozen
  acceptance criteria. Its assertions pass using system Python/Pillow.
- `work/experiments/EXP-20260905-001/comparison.html`: interactive five-arm
  comparison; unaltered captures, CSS magnification only.
- `work/experiments/EXP-20260904-011/authorized-restoration-check.json` and
  `authorized-postflight.json`: exact original prefix and unchanged collision,
  pose and camera; no tracer/stopped thread remains.

Pre/post `make session-audit` results match exactly. The fixture ledger reports
seven unattributed processes and one sink (exit 2); all are the same accounted
direct user-session identities as EXP-010, not newly created or orphaned work.
Vault lint and tracked-file audit pass (zero errors/violations; eight existing
Vault warnings); whitespace and claim-sweep checks pass. All prepared/runtime
artifact hashes revalidate. See the session and its `checks.json` receipt.

The original 1,078-byte prefix is restored to SHA-256
`6741aab66d6a191f1e9285a92a0ca4edc3fb5157a384062a6ba52c79b9fe1554`.
Collision prefix remains
`068f8a4925848faabe608e04631aacac93d2597594c1f8bc8701e271bc94413f`.
The game stays open and paused with the original six-quad, zero-offset box.
No gameplay input, launch, restart, close, player/camera write or asset-file
installation occurred. Private buffers and frames remain outside Git.

**Open:** this candidate was selected using the known failure view. Other
camera angles and oscillating movement still need runtime acceptance. The
analytic mask, sample-position sensitivity and partial actor-buffer match keep
their EXP-009/011 limitations. A general mesh rule, EXP-005 return-floor repair
and full level layouts do not follow from this result. DEC-238 records the next
gate: moving/other-view validation, followed by the separate shared-floor task.
