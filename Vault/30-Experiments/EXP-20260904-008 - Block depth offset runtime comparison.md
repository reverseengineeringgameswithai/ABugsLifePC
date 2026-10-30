---
type: experiment
id: EXP-20260904-008
date: 2026-09-04
status: completed-bounded
question: Does the inherited object offset cause the block to draw behind Flik, and are smaller faces needed for this defect?
environment: Fedora 44; Wine 11 Staging; Gamescope; accepted auto-hardware Direct3D build
result: One-byte removal hides the demonstrated lower-leg and shadow leak; restoration reproduces it at matching player and camera state; corrected original fixture left open
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
created: 2026-09-04
updated: 2026-09-04
tags: [re/experiment, re/rendering, re/collision]
---

# EXP-20260904-008 - Block depth offset runtime comparison

## Later user residual: partial correction

The user subsequently reports smaller leg fragments during left/right movement
against the corrected box and pauses at the failure.
[[EXP-20260904-009 - Paused side-view depth interpolation]] preserves that
game and investigates large-face depth interpolation. The controlled major-leak
removal/restoration below remains valid; it does not establish all-view repair.
The user game46701/1147812 is now paused at the residual side view, not at spawn.

## Result and authoring consequence

**PC confirmed for this fixture:** inherited type0x41 object byte`+0x12=8`
causes the demonstrated lower-leg/shadow visibility error. Changing only that
byte to0 hides those parts behind the box. Restoring8 reproduces the error.
All16 comparison captures have identical measured player XYZ, contact, camera
matrix and camera translation. These are four fresh stationary arms; actor
animation phase and complete renderer state are not asserted identical.

The field at LEVEL.DAT18690 (`0x4902`) was copied from primary160's original
terrain object. [[EXP-20260904-007 - Deck visibility and inherited depth offset]]
retains retail instructions and isolated original-instruction checks:8 adds64
to emitted depth words, or0.015625 at the observed hardware scale. The dispatcher
also temporarily changes distance-threshold global`0x005B56D0` by minus8 times
the byte (`0x00449B04–0x00449B1C`), restoring it after the call. It is not a
globally depth-only field. No change to retail terrain elsewhere is implied.

**Decision for future authoring:** choose and validate this object field
explicitly for new solid geometry. Do not blindly inherit the terrain object's
value. Preserve the failing fixture as an occlusion regression. Collision data
and renderer settings require separate validation; this case does not establish
a general one-to-one grouping or fix EXP-005's return-fall/shared-edge defect.

## First live test at the user's original box

The previous user game40214/965017 was closed with a clean audit. The first
fresh arm `zero` changed only byte18690 across2,251 compared files excluding
the runtime log. Geometry, texture data and TERRAIN.ALL were identical to EXP-006.
Read-only checks verified the loaded collision prefix, complete render prefix,
scene center, object bytes and object-to-mesh pointer, including the zero byte.

Normal Up/jump input landed on the box at`(175348,-108546,519146)`.
Walking off its far side landed on the deck at`(173883,-102401,520660)`;
moving farther away settled at`(171872,-102401,522740)`. Captures now hide the
feet and shadow behind the box. Other side views and deck movement were retained.
These views do not match the earlier user's camera exactly; the stationary
comparison below supplies the controlled visual intervention/restoration.

## Stationary discriminator and subdivision control

To avoid requiring an exact keyboard replay, a common fixture places the same
box between the initial camera and Flik. Both its visible geometry and collision
move together to stored X6275..6925, Z14800..15500, topY−3392. The broad deck,
natural spawn and other assets remain. No player-memory edits or teleport.

Compared four valid stationary arms in order8, split0, unsplit0, restored8:

| Arm | Object byte | Visible quads | Outcome in lower-leg/shadow region |
| --- | --- | --- | --- |
| `stationary8` | 8 | 6 | Legs and shadow draw over the box |
| `stationary4` | 0 | 33 | Lower legs and shadow hidden |
| `stationary0b` | 0 | 6 | Lower legs and shadow hidden |
| `restored8` | 8 | 6 | Visibility error returns |

The8/unsplit0 pair differs only at18690. Restored8 is byte-identical to its
control DAT. Collision is byte-identical across all four stationary arms.
The subdivision arm retains the same six surface planes, total area, winding,
endpoint texture coordinates and object setting; its top is4×4, sides have4
horizontal segments each, and the broad deck is one quad. Shared vertex
positions keep its45 vertices/33 faces within the original known mesh span.

Every captured state is XYZ`(197108,-102400,492895)`, contact source99/cell6973551,
camera matrix`dd090000990c00000010000067f30000dd09`, translation
`(219785,-115200,475141)`. Four no-input captures per arm are separated by0.6s.
Memory and images are sequential, not atomic paused snapshots.

The lower-body ROI `(270,330,365,410)` was selected before the first stationary
capture. Of its7,600 pixels,6,902 have identical RGB across all eight original/
restored control captures. The unsplit zero arm changes1,308 of those pixels
in every capture. An exploratory blue-dominance count falls from697–747 pixels
in controls to4–8 in unsplit0 and0–4 in split0. That classifier and the invariant
mask were computed after observation; neither is an independently calibrated
acceptance gate. They describe the visible effect, supported independently by
the one-byte intervention, restoration and original instructions.

Smaller faces were not required to eliminate the demonstrated major leak.
Subdivision also changes textured-surface pixels, so it is not a texture-neutral
control and proves no universal face-size rule. Large-face projection/clipping,
arbitrary sizes, material families and full level layouts remain untested.
The corrected play fixture keeps the original six quads.

## Runtime validity and ownership

Retail executable hash is in frontmatter. Every arm executes the accepted
auto-hardware build`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`
under a private copied prefix with all six required hardware markers. Direct
XTEST guards the exact window/PID/start/group/cwd; process-memory access is
read-only and checks mapped movement instructions. No debugger, live writes,
save state, freezing or R2q/historical mapping changes. CAP-010 remains open.

| Arm | Game PID/start | Group | Final status |
| --- | --- | --- | --- |
| `zero` | 42786/1086969 | 42535 | closed, clean audit |
| `stationary8` | 43806/1113563 | 43563 | closed, clean audit |
| `stationary0` | 44300/1118409 | 44054 | rejected Training17, closed cleanly |
| `stationary4` | 44853/1124531 | 44610 | closed, clean audit |
| `stationary0b` | 45415/1131729 | 45170 | closed, clean audit |
| `restored8` | 45925/1136830 | 45680 | closed, clean audit |

The rejected attempt confirmed too soon during the carousel transition and
entered Training17. Its captures/reads are excluded from science. The successor
checks the visible menu and permits the selection to settle. This was one
discarded menu-entry attempt, not an additional accepted control.

**User handoff remains open:** `USER-20260904-deck-depth-play-001`,
game46701/1147812, group46458, display`:2`, sink`ablpc_mute_46458`, module536870916.
It has the original EXP-006 box position with only its depth byte corrected.
Normal menu input only; Flik is at the initial deck position. Full ownership,
including private-prefix helpers outside the group, is in its`handoff.json`.
The audit's nonclean fixture-ledger classification is accounted for by that
receipt, not treated as orphaned processes.

## Files, reproduction and limits

- Original deck TERRAIN.ALL remains
  `26f3e0235533419a80b2a0eff18f423fadc20617a6c2ed2be445abeae87b35d5`.
- Corrected original-position LEVEL.DAT is
  `b0e6a65a353e7a33c0e72399659a8f3ee6d08380fe45893232281d93c06805cb`.
- `scripts/terrain-deck-visual-probe.py` defaults to that one-byte correction;
  optional `--stationary`, `--depth-offset 8`, and `--divisions 4` reproduce the
  bounded comparison fixtures. Assets require a new output under work/copies.
- `reports/terrain/EXP-20260904-008.json` retains exact arm hashes, loaded-byte
  receipts, movement traces, captures, audits, source provenance and handoff.
  Previous EXP-006/007 reports and the original EXP-006 builder are unchanged.
- Raw images, game logs, assets and private prefixes stay under work. The
  interactive raw-capture comparison is
  `work/experiments/EXP-20260904-008/comparison.html`.
- 197 focused tests pass in37.05s, including9 new cases for rejected settings,
  unchanged physics, exact one-byte diff, span preservation and geometric
  coverage/winding. Full`make check` and independent review were not run; no commit.

Next: retain this byte-choice/occlusion regression for new geometry, then resume
the separate connected-floor boundary investigation. Do not claim complete
renderer/collision independence or arbitrary level-authoring support.
