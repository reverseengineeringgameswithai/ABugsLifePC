---
type: experiment
id: EXP-20260904-009
date: 2026-09-04
status: bounded-diagnosis-candidate-not-applied
question: Why do leg fragments remain visible through the zero-offset box in the user's paused side view?
environment: Existing Wine hardware game read-only; original x86 renderer in offline captured memory
result: Large-face depth ordering explains sampled residual fragments; subdivision improves offline ordering; live comparison pending
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
created: 2026-09-04
updated: 2026-09-04
tags: [re/experiment, re/rendering, re/collision]
---

# EXP-20260904-009 - Paused side-view depth interpolation

## Authorized follow-up completed

The user subsequently authorized the prepared writes.
[[EXP-20260904-010 - Paused subdivision live comparison]] completes the
temporary swap/capture/restoration in this same paused process. It confirms
disappearance of all255 prior inversion-point fragments and exact3,575-pixel
ROI restoration. Six other analytic boundary samples remain. The diagnostic
record below describes the earlier read-only boundary; its report is unchanged.

## Result and scope correction

The user reports that EXP-008's corrected box looks better, but oscillating
left/right against its side exposes parts of Flik. They paused the game at the
failure and asked that it be investigated before a restart loses the state.
**The same game remains paused. No gameplay input, restart, process suspension,
debugger, save-state operation or live write was performed.**

The read-only position is on the lower deck, just outside the box's left plane.
Original renderer execution against a copy of that paused state produces a
large top triangle whose interpolated depth lies behind visible leg fragments,
although an analytic camera ray meets the box before those fragments. Dividing
the box into smaller faces substantially reduces that depth error offline.

**Strongly supported inference:** oversized face depth interpolation contributes
to this residual view-dependent visibility defect. The user-triggered motion
was not replayed, and no changed/restored live frame has yet verified the
candidate at this pose. Some physically exposed model pixels should remain
visible; the analysis does not classify every blue pixel as a defect.

EXP-008's one-byte removal/restoration remains valid for its demonstrated major
leak. It is a **partial correction**, not proof that all side views are fixed.
This finding does not resolve EXP-005's separate return-floor failure.

## Preserved live evidence

- Session `USER-20260904-deck-depth-play-001`, game PID/start46701/1147812,
  group46458, display`:2`, owned window14680071, sink`ablpc_mute_46458`.
- Executed auto-hardware SHA-256
  `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
  Guarded reads verify executable bytes, PID/start/group/cwd and all six
  required hardware log markers. Session audit matches the existing handoff's
  seven processes and private sink; these are intentionally open, not orphans.
- Position at`0x0059D910`: `(163024,-102401,509900)`.
  Contact at`0x007F3D68`: source99/pointer6973595, the second deck triangle.
  The box's world X span is163200..184000: the player reference point is176
  units outside its left plane. Its Z span is497600..520000; visible topY is
  −108544 and deckY is−102400. This is a point/contact observation, not a
  proof about every animated limb's physical extent.
- Camera matrix at`0x005B58E0`:
  `81050000050f000000100000fbf000008105`; camera translation at`0x005BDB8C`:
  `(190254,-115203,500135)`. These values, position and contact agree before
  and after memory capture and at the subsequent candidate preflight.
- Loaded LEVEL.DAT SHA-256
  `b0e6a65a353e7a33c0e72399659a8f3ee6d08380fe45893232281d93c06805cb`;
  object byte18690 remains0. TERRAIN.ALL remains
  `26f3e0235533419a80b2a0eff18f423fadc20617a6c2ed2be445abeae87b35d5`.
- Native paused640×480 image:
  `work/experiments/USER-20260904-deck-depth-play-001/frame-1788567836037465925.png`,
  SHA-256`acf58e566b9712c17c9e32ae4abf6d2be74490a823023db28183ccfd318c2c09`.
  The user's supplied image is separately retained under EXP-009.

Captured55 readable low-address mappings,131,133,440 bytes, over6.832 seconds
with read-only `/proc/46701/mem` access. Per-region lengths and hashes are in
`work/experiments/EXP-20260904-009/paused-memory.json`. This is **not atomic**
and **not a restorable process save state**. Rendering can continue behind the
game's pause menu. All dumps and image/mesh assets remain in ignored`work/`.

## Original drawing instructions on the captured copy

`offline_mesh.py` maps the captured regions into Unicorn, verifies their hashes,
then installs the hash-verified retail `.text`. It uses a synthetic stack and
one scene-pointer table outside the captured address space. The only other
setup changes are the scene driver's threshold/pass values and cleared batch
counters. The changed-mesh arm replaces primary160's render prefix **offline**.

Each call stays inside original executable code, has a2,000,000-instruction
ceiling and returns normally. No API stubs or replacement drawing routines:

| Original entry | Input | Instructions | Emitted vertices / indices |
| --- | --- | ---: | ---: |
| `0x004498F0` | Current primary160 | 3,958 | 12 / 18 on page0 |
| `0x004498F0` | Four-way subdivided primary160 | 21,209 | 72 / 108 on page0 |
| `0x0044C440` | Flik's captured pose/state | 131,857 | 387 / 549 on page16 |

The first entry reaches the original mesh renderer`0x0045A7F0`. The current
mesh's12 emitted `(x,y,z,rhw)` tuples match the captured live page0 buffer
**consecutively at vertex slots232..243**, confirming the static projection.
For the actor, only75/387 tuples match the retained page16 buffer. Its earlier
slots contain different projected geometry, and the captured batch counts are0
after flushing. Do not claim an exact complete live actor-batch match. The
original actor routine uses the captured pose tables; its output remains an
offline reconstruction, corroborated by visible fragment positions.

EXP-007's retained retail instruction evidence establishes camera-Z/4
truncation at`0x0045CFE8–0x0045D05F` and the scaled hardware depth store at
`0x0045E9BF–0x0045E9D4`, with scale1/4096 at`0x004C00E8`. Perspective reciprocal
and hardware depth are separate emitted values. The current bias byte is0;
the original additive offset is not responsible for this residual arithmetic.

## Depth discriminator at the user's visible fragments

Compare screen-space barycentric depth interpolation with a camera ray through
the authored box's exact top plane. Smaller depth means nearer in this model.
At native pixel`(339,325)`, visibly blue in the paused capture:

| Surface | Depth |
| --- | ---: |
| Analytic box-top intersection | 0.04781566 |
| Subdivided box, original emitted depths interpolated | 0.04787632 |
| Flik, original emitted depths interpolated | 0.05444336 |
| Current large box face, original emitted depths interpolated | 0.05570231 |

The ray meets the top at world`(167222.22,-108544,510160.65)`, inside the box's
X/Z footprint. The current large triangle places this nearer surface behind
Flik in the depth comparison; subdivision puts it back in front. Native pixels
`(305,319)`, `(308,320)` and`(312,321)` supply additional retained examples.
Changing camera angle or limb pose can change which surface wins this comparison;
that explains the reported motion dependence as an inference, not a replay result.

An exploratory blue filter in native ROI X285..349,Y285..339 identifies1,034
pixels. Of259 samples where the analytic top is inside the box and ahead of the
reconstructed actor, the current face loses all259 depth comparisons; the
subdivided face still loses6. These remaining near-boundary samples include
`(301,319)`. **The candidate is not claimed to eliminate every pixel defect.**
The filter and ROI were chosen after viewing the image. This model does not
simulate texture/alpha, culling, raster edge rules, depth quantization, or the
complete GPU; counts are explanatory, not an acceptance test.

## Concrete next comparison, not executed

Prepared `work/copies/EXP-20260904-009/subdivided/LEVEL.DAT`, SHA-256
`8ba384541d80da2e82a3016cf99638476229b4da7d445a9edfafdc34e365b6e5`.
The existing tested fixed builder produces45 vertices/33 quads: a4×4 top,
four strips per side, and the unchanged deck quad. Box dimensions, collision,
object byte0 and all bytes outside its1,078-byte mesh prefix remain identical.
UV interpolation changes textured pixels; it is not a texture-neutral control.

`candidate-plan.json` records a read-only live preflight for that prefix at
`0x006662A7` (LEVEL.DAT offset113136),777 differing bytes in a1,078-byte span.
Both exact byte buffers are saved privately: original SHA-256
`6741aab66d6a191f1e9285a92a0ca4edc3fb5157a384062a6ba52c79b9fe1554`, candidate
`9f953f2edd1f4e4a6fa0f58e1d3c40ef55afcf9a7b9b61301e4c60393a35d1f1`.

To compare without losing the user's pose: explicitly authorized temporary
process suspension, compare-before-write of that prefix, replacement, verified
readback and resume to the existing pause menu; capture, then the separately
authorized guarded restoration of the saved prefix with another brief suspension.
No gameplay input or restart. If the paused renderer does not refresh, report
inconclusive rather than silently unpausing. **Neither write is authorized or
executed at this boundary.** AGENTS.md requires fresh explicit authorization per
memory-write use; the operating manual also requires explicit debugger/execution
change approval. A memory dump or this prepared plan grants neither.

## Evidence and validation

`reports/terrain/EXP-20260904-009.json` contains selected numeric evidence,
provenance, hashes, execution counts, limitations and the candidate plan.
Companion `EXP-20260904-009-*-operator.txt` files retain the offline procedures.
Full actor geometry, memory and images stay under`work/`; no originals changed.

All three bounded original-instruction calls and candidate byte/collision
invariants pass. No production code changed in EXP-009; the fixed builder already
has EXP-008's9 regression cases and197 passing focused tests. Documentation and
tracked-artifact gates are run separately; no full make check, commit or
independent audit is claimed. DEC-234 preserves this paused-state discriminator
before general layout work.
