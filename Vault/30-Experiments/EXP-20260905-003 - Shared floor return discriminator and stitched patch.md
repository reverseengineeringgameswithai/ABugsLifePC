---
type: experiment
id: EXP-20260905-003
date: 2026-09-05
question: Can the EXP-005 return fall be reproduced numerically and removed by a connected PC-native floor edit?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Original PC instructions offline; isolated file-loaded Direct3D Wine copies, normal XTEST input and read-only capture
result: Bounded return failure reproduced offline and live; six-cell stitched patch passes modeled seams and two live return cycles; extra live seam route blocked before crossing
---

# Shared floor return discriminator and stitched patch

## User-directed terrain-only validation, 2026-09-05

The user clarified that these terrain tests must not rerun R2q. The once-started
full `make check` trial was cancelled with SIGINT after 360.849 seconds wall time;
pytest reported 885 passed and the one known pre-existing R2q historical SHA
mismatch in 359.80 seconds before interruption. All test processes exited.
There is no completed full-repository verdict and no serial/full-suite retry.
The exact terrain gate passed 72/72 in 27.66 seconds; the 27 added regressions
passed in 6.44 seconds. This session uses those terrain-only gates, not a claim
that the repository suite passed. See `reports/terrain/EXP-20260905-003-validation.json`
and [[EXP-20260905-003 - Shared floor return discriminator and stitched patch]].


## Result and scope

EXP-005's return fall is now reproduced in an original-PC-instruction trajectory
and a fresh file-loaded runtime arm. This supersedes the un-reproduced status at
the diagonal/movement checkpoint, not its finite box result. The rigid edit is
preserved unchanged as a failure control. A connected six-cell vertex-star edit
removes this failure in the tested paths. This is not a universal mesh rule or a
finished level editor. EXP-006 remains a separate flat-deck regression fixture.

Evidence: `reports/terrain/EXP-20260905-003.json` (census, exact offsets, hashes,
all motion states and original-instruction plane-sign witness),
`reports/terrain/EXP-20260905-003-runtime.json` (normal-input traces, identity and
loaded-file checks, screenshot hashes and audits). The complete private model
report is `work/experiments/EXP-20260905-003/offline-v2.json`, hash-pinned by the
public projection. Version 1 is retained as a rejected topmost-plane seed control.

## Boundary and render census

Source 99 group 47640 contains six 32-byte cells, starting at 47652, 47684,
47716, 47748, 47780 and 47812. All eight perimeter edges have exact retail XYZ
neighbors. The rigid h0-only -64 edit creates a 64-stored/2048-world vertical
separation on every perimeter edge without changing XZ adjacency. The inclusive
projected boundary census resolves 68 active collision cells, including prop
and clone overlaps. Inactive templates are not active collision instances.

| Target cell | Stored boundary endpoints, XYZ | Exact neighbor |
| --- | --- | --- |
| 47652 | (5511,-110,16494) to (5588,-47,15594) | source99 cell47544 |
| 47652 | (5511,-110,16494) to (6103,16,16174) | source100 cell48856 |
| 47748 | (5588,-47,15594) to (6169,-19,15109) | source99 cell46548 |
| 47812 | (6103,16,16174) to (6488,49,16488) | source100 cell48856 |
| 47780 | (6169,-19,15109) to (6657,-53,15155) | source99 cell46292 |
| 47812 | (6488,49,16488) to (6893,-56,15972) | source99 cell48240 |
| 47780 | (6497,-54,15500) to (6657,-53,15155) | source99 cell48208 |
| 47684 | (6497,-54,15500) to (6893,-56,15972) | source99 cell48016 |

The render census walks complete 0x41 mesh streams, not only their first face
group. Original instructions at 0045A8B0/B4, 0045C783/787, 0046024A/4E and
0046025E/60 independently check group/face pointers and the ffff terminator for
124 Level01 and 8 Level03 meshes, with emission disabled. This is a stream-walk
proof, not full renderer validation. Nonzero rotations use the original Euler
builder 00463C80 and on-disc sine table at 004C2100. Alternate runtime-matrix
references are excluded only when a conservative full signed-short-matrix bound
cannot reach the footprint; unsupported nearby transforms must fail closed.

Four nearby complete streams contain 22 selected faces with an explicit
32-stored-unit correspondence margin; 10 have exact projected overlap with the
target footprint. Primary128 has 3 groups, 95 faces and terminator 223080;
primary160 has 5/69/115368; primary213 has 6/148/60176; primary280 has
6/95/63216. Every selected face, participating vertex field offset, opaque face
word and duplicate owner is in the report. The margin is not an assertion that
render and collision topology are identical.

## Discrimination, including contrary evidence

The original movement entry is 004AB1A0. The synthetic route uses the EXP-005
XZ seed, original landing, 35 forward steps (-900,512,700), 35 reverse steps
(900,512,-700), then 15 settling steps (0,512,0). Positive Y is downward.

- **Raw vertical step:** confirmed geometrically at all eight rigid boundaries.
  It predicts a longer outbound drop and entry from underneath on return.
- **Gap or overlap:** no new projected XZ gap is introduced. There is a vertical
  discontinuity, plus unchanged overlapping prop collision in the complete scene.
- **One-sided admission:** on rigid reverse index 10, cell47652 is in the native
  candidate list. Its signed plane distances at 004AA60B and 004AA646 are negative;
  the latter original `js 004AA74E` rejects entry from underneath. This is not a
  candidate-collection miss. The report retains the complete witness.
- **Stale normal/bounds:** reconstructed integer normals exactly match all seven
  original target-plus-neighbor cells. Translation does not rotate the planes.
  Widening rigid Y windows to (-16,32) produces the same complete motion state
  sequence. That control contradicts a Y-window-only explanation at this route.
- **Render-only mismatch:** contradicted by the collision-only original-instruction
  failure. Paired runtime mesh verification and captures provide a separate visual
  check, but do not prove every-view render/collision identity.

Retail and stitched have longest airborne runs of 1 in each traveling leg and
finish grounded. Rigid loses contact at reverse index 9: 26 remaining reverse
samples and all 15 settling samples are airborne. Its final stored contact still
names the old cell; a stale contact pointer must not be called grounded contact.

All eight edges are crossed in both directions, with explicit source/cell/flag
transitions. Retail and stitched each pass 16/16 with only emulated static sources
99/100 enabled, and 13/16 in the complete scene. The same three complete-scene
routes are confounded by unchanged prop contacts: source73 cell908 on the inward
48240-to-47812 route, and source0 cell16 on both directions of the
47684/48016 boundary. Rigid passes 0/16 under the strict maximum-two-airborne-step
criterion, though its outbound drops can eventually land. Prop-disabled results
are clearly labeled offline controls, never runtime edits.

## Connected edit and preservation

Move stored vertex (6103,16,16174) upward by 64 in its entire incident star:
source99 cells47652/47684/47716/47748/47812 and source100 cell48856. Leave
nonincident cell47780 and every exterior star vertex unchanged. Recompute only
established normal, h0/dy1/dy2 and signed Y-window fields; preserve all other
bytes, topology, edge fields and unidentified words. Bounds checks reject
unsupported source kinds, non-upward/degenerate planes and integer overflow.

Pair LEVEL.DAT through the same continuous piecewise-barycentric displacement,
without adding geometry or changing materials/object settings. Six vertex-Y
fields change: primary160 vertex8 at113238 (-29), vertex9 at113250 (-64),
vertex10 at113262 (-23), vertex20 at113382 (-5), primary280 vertex27 at60510
(-23), vertex97 at61350 (-29). Exact duplicate vertices receive equal changes.
This is deliberate pairing on the existing distinct mesh, not a universal weld.

Candidate TERRAIN.ALL SHA-256:
`2522c75a8f8156d9a7ef2a9538e2f04aa721be1ddca7588959c41a44c70b3d9b`.
Candidate LEVEL.DAT SHA-256:
`96445ece4da941a637db84bd9f0fd790b0f96557e599b33d68b95ea429aa00c6`.
Authored files remain under `work/copies/EXP-20260905-003/`.

Six modeled centroid landings return native flags [1,1] on the intended cells.
The subsequent normal impulses remain grounded and are **not a jump model**.
The outbound seam route covers step-off and landing; reverse covers return.

## Runtime comparison

Each arm uses a fresh full-disc copy and isolated prefix. All 2251 staged files
were compared with the source tree; only TERRAIN.ALL and LEVEL.DAT differ in
edited arms. The executed auto-hardware cache image is SHA-256
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`, not the
retail image retained inside each stage. Six hardware markers, exact
PID/start/group/cwd/window, content-drive identities, compositor socket peer and
resident collision source99/100 plus complete four-mesh streams are checked.
The authoritative [[PC autonomous game control]] route is Right, Return,
Return, with Level One title and natural gameplay spawn checked separately.

Normal camera-relative input targets XZ (170000,516000), then (197091,492897),
with an 8-second cap per leg. This is feedback-driven input, not frame-identical
replay; coasting after key release and capture latency are retained in receipts.

- Retail completes one cycle: outbound cell47544, return cell47716.
- Rigid reaches cell47544 outbound, then triggers the below-floor guard on return.
  At release position (180787,2524,509120), the floor plane is -3748 and the
  anchor is 3072 below plane+3200; contact still names cell47544. The sampled
  trigger precedes this release observation. Its screenshot is retained.
- Stitched completes two cycles, returning to cells47748 and47716 respectively,
  without triggering the guard. A normal Shift_L jump has 124 samples, Y range
  -10783..2085, and returns to floor contact near (193914,2085,494638).
- A separately pre-recorded extension toward source100 times out beside a
  visible rock near (195338,1679,512992), before crossing the intended seam.
  Approach/outward/inward attempts are not counted as successful crossings.
  The final return reaches cell47716 safely. Source100's stitched-edge runtime
  validation therefore remains open despite the clean isolated model result.

Live contact globals and floor-relative coordinates are observations, not a newly
validated live grounded-bit contract. There were no memory writes, teleport,
ptrace, STOP/CONT, register access, debugger control or save states. No PS1
source was consulted.

## Environment correction and validation

Initial sandbox session audits reported clean but were not host-complete. After
permissions became unrestricted, the retail post-close audit found older
`USER-20260904-deck-depth-play-001` group46458/game46701 and sink
`ablpc_mute_46458`. The user explicitly authorized closure. Its pinned processes
and exact sink were closed; the unrestricted audit then passed. Retail had run
concurrently with that older instance, using guarded :3/gamescope-1; do not claim
an initially empty host. Rigid and stitched each had clean unrestricted pre/post
audits. The final runtime audit is clean with no game, helper or null sink left.

The route helper uses the existing system Pillow directory through PYTHONPATH
with the project virtualenv (which supplies pefile); no package installation.
An initial virtualenv-only attempt lacked Pillow, and system-only lacked pefile;
neither sent movement. A discovery stdout stream is concatenated JSON, not one
JSON document; evidence packaging must retain that distinction.

New parser/writer, synthetic, multi-file original-stream and movement regressions:
27 passed in 6.44s. The exact five-file terrain gate before runtime: 72 passed in
27.50s. Final focused gate and measured two-worker full `make check`, including
exit status, duration and any pre-existing failures, are recorded in
`reports/terrain/EXP-20260905-003-validation.json`; do not infer a green full suite
from the terrain results. The known isolated R2q historical SHA mismatch is not
attributed to this terrain edit. Protected paths, stash identity, claim sweep and
tracked-file/diff audits are included in the final validation packet.

## Next discriminating work

Navigate a pre-recorded normal-input route around the unchanged prop, comparing
retail and stitched before declaring a live source99/source100 seam pass. Keep
the three complete-scene prop-confounded modeled routes separate from pure floor
admission, and extend velocities/poses only as finite evidence. Do not promote
this star edit or the banked box diagonal result into a general authoring rule.

Links: [[EXP-20260904-005 - Raised floor and visible ground pairing]],
[[EXP-20260904-006 - Flat deck and solid block test]],
[[New-level authoring roadmap (terrain, collision, materials)]],
[[2026-09-05 1659 - Codex - Shared floor return and stitched patch]].
