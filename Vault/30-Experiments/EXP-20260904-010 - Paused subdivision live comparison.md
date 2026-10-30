---
type: experiment
id: EXP-20260904-010
date: 2026-09-04
status: completed-bounded-original-restored
question: Does the prepared finer mesh hide the residual fragments in the exact user-paused side view?
environment: Existing Wine hardware game; authorized guarded mesh swap and restoration; paused compositor captures
result: All255 prior inversion-point fragments disappear and return on restoration; identical state in9 captures;6 other boundary samples remain
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
created: 2026-09-04
updated: 2026-09-04
tags: [re/experiment, re/rendering, re/collision]
---

# EXP-20260904-010 - Paused subdivision live comparison

## Result

**PC confirmed for this paused view:** subdividing the box's render mesh removes
the255 blue fragment pixels identified by EXP-009's depth-order analysis.
Restoring the original mesh brings all255 back. All3,575 RGB pixels in the
comparison region match exactly between all three initial and three restored
captures. All nine captures have identical measured player position, contact,
camera matrix and camera translation. The three candidate-region images also
match one another exactly.

Together with [[EXP-20260904-009 - Paused side-view depth interpolation]]'s
original instructions, live-buffer match and geometric ray/depth comparison,
this establishes a bounded rendering improvement and strongly supports
large-face depth interpolation as the remaining major cause. Collision and
box dimensions were unchanged. The original zero-offset six-quad mesh is
**restored**, and the same game is still paused at the user's failure pose.

**Not complete occlusion acceptance:** six other blue samples remain among
EXP-009's259 analytically occluded boundary points. Some visible model parts
also legitimately project above the box. No oscillating gameplay replay, other
camera-angle sweep or universal subdivision rule is claimed. EXP-005's
return-floor fall remains a separate unresolved defect.

## Authorization and exact scope

After review of the prepared swap/capture/restoration plan, the user replied:
“go for it. I authorize memory writes ehre”. This authorized the two specified
writes and brief process suspension/resumption. No additional permission was
requested. The authorization text and plan hash are retained in the report.

The existing session is `USER-20260904-deck-depth-play-001`, game46701/1147812,
group46458, display`:2`, window14680071, sink`ablpc_mute_46458`. Executed
auto-hardware SHA-256:
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
Every guard verifies identity/cwd, mapped code and all six hardware log markers.

Exactly two writes to primary160's1,078-byte render prefix at`0x006662A7`
(LEVEL.DAT offset113136):

| Write | Expected prefix SHA-256 | Verified resulting prefix SHA-256 |
| --- | --- | --- |
| Apply finer mesh | `6741aab66d6a191f1e9285a92a0ca4edc3fb5157a384062a6ba52c79b9fe1554` | `9f953f2edd1f4e4a6fa0f58e1d3c40ef55afcf9a7b9b61301e4c60393a35d1f1` |
| Restore saved mesh | `9f953f2edd1f4e4a6fa0f58e1d3c40ef55afcf9a7b9b61301e4c60393a35d1f1` | `6741aab66d6a191f1e9285a92a0ca4edc3fb5157a384062a6ba52c79b9fe1554` |

The prepared candidate has45 vertices/33 quads:4×4 top, four strips per side,
one deck quad.777 bytes differ in the replaced span. Object byte+0x12 remains0.
Both writes have compare-before-write and readback receipts, with restoration
in the transaction's finalization path. No asset file was installed or changed
in the user's stage. Source LEVEL.DAT remains
`b0e6a65a353e7a33c0e72399659a8f3ee6d08380fe45893232281d93c06805cb`;
candidate file SHA-256 is
`8ba384541d80da2e82a3016cf99638476229b4da7d445a9edfafdc34e365b6e5`.
TERRAIN.ALL remains
`26f3e0235533419a80b2a0eff18f423fadc20617a6c2ed2be445abeae87b35d5`.

## Avoiding an interrupted mesh read

Simply replacing the vertex count and stream while a renderer is halfway
through reading them can leave a mixed layout. Before either write, all threads
of the owned game are briefly stopped; a read-only register inspection checks
the main thread's actual call chain. No execution breakpoint or register write.

The accepted gate requires the first original-code return reached through a
bounded EBP chain to be`0x00405B74`, with the enclosing renderer return at
`0x0044DBF3`. Original instructions show the timer call at`0x00405B72` inside
the frame-limiter loop. The scene driver's final call at`0x0044DBEE` reaches
that routine through thunk`0x004017CB`; geometry processing has finished.
`reports/terrain/EXP-20260904-010-safe-stop.asm` retains these instructions.
This is specific to the captured process/call layout, not a generic safe-stop API.

The helper uses scoped SIGSTOP/SIGCONT and
PTRACE_SEIZE/INTERRUPT/GETREGS/DETACH. Five preliminary read-only stop probes
established the call chain. The transaction needed13 stops, of which two
passed the gate and wrote; the other11 resumed without writing. Across all18
stops, the longest measured stop context was3.578ms. Read-only ptrace attachment
is explicitly accounted for; this was not a debugger-free run.

An isolated disposable Python child passed stop/register-read/detach/resume
validation. Three recorded valid call chains pass the gate and three versions
with a corrupted enclosing return reject. The helper never installs breakpoints.

## Captures and numeric comparison

Three captures before, three with the candidate, three after exact restoration.
The pause menu continues to render, so no gameplay unpause was necessary.
Every capture records:

- Player position`(163024,-102401,509900)`; contact source99/pointer6973595.
- Camera matrix bytes`81050000050f000000100000fbf000008105`.
- Camera translation`(190254,-115203,500135)`.

The ROI and blue classifier were inherited from EXP-009 before this live test:
native X285..349,Y285..339; blue means B>R+6 and B>G+2. They originated as an
exploratory selection, not an independent holdout. The255 sampled inversion
points came from the earlier original-instruction depth comparison.

| Observation, same value in all3 captures per arm | Before | Finer mesh | Restored |
| --- | ---: | ---: | ---: |
| Blue pixels at255 prior inversion points | 255 | 0 | 255 |
| Blue pixels at259 analytic-top occlusion points | 259 | 6 | 259 |
| Blue pixels in full3,575-pixel ROI | 1,034 | 779 | 1,034 |

The candidate changes764 ROI pixels; subdivision also changes texture
interpolation, so the changed-pixel total alone is not an occlusion measurement.
The prior inversion-point disappearance and restoration are the relevant join.
At`(339,325)`, RGB changes`(57,65,90)`→`(82,69,41)`→`(57,65,90)`.
Boundary sample`(301,319)` stays`(24,28,41)` throughout, consistent with the
earlier candidate's remaining uncertainty. Full-frame hashes differ because
other screen elements can animate; no full-frame equality is claimed.

ROI RGB SHA-256 before/restored:
`e91e53ad293c765759ac459e02290974fdd073e9d24fd923089aa5388339a842`.
Candidate:
`4af5055892f27632268e90a66544406e9712540b592ae7a84719af66109f366f`.

Interactive original/finer/restored captures, with CSS magnification only:
`work/experiments/EXP-20260904-010/comparison.html`.
Images are unaltered native game captures. Memory, image and mesh assets remain
under ignored`work/`; public report/operator files contain metadata and evidence.

## Final accounting and next boundary

The transaction succeeds with two verified writes and no error. Final guarded
reads verify the restored render/object/collision prefixes and unchanged pose.
Pre/post session audits are identical: the same seven processes and private
sink are intentionally open and accounted against the direct handoff, despite
the fixture-only ledger's unattributed label. Final TracerPid is0; all16 game
threads are running/sleeping rather than stopped. No restart, game launch,
close, gameplay key, collision/player/camera write, save-state or mapping action.

`reports/terrain/EXP-20260904-010.json` retains receipts, hashes, selected
measurements and limitations. Companion operator text reproduces the fixed
procedure; the already-consumed live transaction must not be rerun. Prior
EXP-008/009 reports remain unchanged. No production code changed; EXP-008's197
focused tests are prior validation of the candidate builder, not new test runs.
No full make check, commit or independent audit is claimed.

DEC-235 retains the subdivision result as a regression and keeps all-view/edge
validation open before choosing general authoring defaults. The authorized
temporary comparison is complete; the finer mesh has not been left installed.
