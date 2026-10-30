---
type: experiment
id: EXP-20260904-011
date: 2026-09-04
status: offline-complete-live-followup-verified
question: Can the six remaining box-edge samples be discriminated by changing top-face diagonals while preserving vertices and collision?
environment: Captured Wine hardware state in offline Unicorn; existing paused game guarded read-only
result: Same 4x4 vertices and face count with alternate top diagonals win all 259 prior analytic comparisons offline; live comparison prepared
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
created: 2026-09-04
updated: 2026-09-05
tags: [re/experiment, re/rendering, re/collision]
---

# EXP-20260904-011 - Box top diagonal edge discriminator

**Subsequent live result:** fresh four-write/brief-stop authorization was given
on 2026-09-05. [[EXP-20260905-001 - Box top diagonal live comparison]] executes
this unchanged plan: the six samples disappear with alternate diagonals and
return with the fine control, all 255 prior fixes remain hidden, and both
control ROIs restore exactly. The original mesh is restored in the paused game.
The offline report and plan below retain their preparation-time hashes/status;
execution receipts are separately indexed by the live follow-up report.

The user asks to start the next banked task: the residual box-edge visibility.
Reuse EXP-009's captured RAM/actor output and EXP-010's native comparison;
do not recreate the failure or restart the user's game.

**Confirmed offline:** cyclically rotate each of the 16 top quads by one corner,
keeping each vertex offset paired with its UV fields. The original renderer
then splits it across the other diagonal. The candidate keeps all 45 vertex
records byte-identical, all 33 faces, dimensions, winding, surface coverage,
matching top/wall edges, object depth byte 0 and collision bytes. Only 138 bytes
differ from the banked finer fixture, within its 256-byte top-face table.

**Inference:** the six residual samples are consistent with remaining depth
interpolation error inside the existing 4x4 top cells. The alternate diagonal
improves the original emitted depth ordering without adding geometry.
Live causality was unverified at preparation; the follow-up above now confirms
the six-sample effect at this pose. The saved analytic mask and actor
reconstruction are not a complete rasterizer or physical-visibility oracle.

## Evidence and comparisons

The six retained samples are native coordinates (342,315), (344,315),
(298,319), (299,319), (300,319), (301,319). They remain blue in EXP-010's finer
mesh captures. Their original integer-sample box/actor depth differences are
small. Moving the hypothetical sample by +0.5 in Y changes all six ordering
predicates; this is sensitivity analysis, not a claim about the GPU's pixel
center convention. Reciprocal-depth reconstruction is exploratory only.

Ten bounded calls to original PC entry 0x004498F0 run over EXP-009's captured
memory with verified retail text, synthetic stack and cleared batch counters.
All return below the 2,000,000-instruction ceiling, in 21,209–25,799 instructions.
The 4x4 control emits batches exactly equal to EXP-009's retained result.
The alternate 4x4 takes 21,211 instructions. The original depth stores and
integer projection are anchored by EXP-007/009, including 0x0045D005 and
0x0045E9BF–0x0045E9E3.

| Top grid | Mesh prefix bytes | Prior 259 samples: normal / alternate diagonal wins | Prior 255 fixes preserved: normal / alternate |
| --- | ---: | ---: | ---: |
| 4x4 | 1,078 | 253 / 259 | 255 / 255 |
| 4x5 | 1,258 | 258 / 259 | 254 / 255 |
| 5x4 | 1,258 | 254 / 259 | 254 / 255 |
| 3x6 | 1,202 | 256 / 259 | 255 / 255 |
| 6x3 | 1,202 | 259 / 259 | 255 / 255 |

All use the same box and remain within the original known 1,336-byte mesh span.
The normal 4x5 and 5x4 grids respectively regress old samples (308,315) and
(343,316). Preserve these negative results: more faces alone is not an
acceptance rule. Select the alternate 4x4 for the live discriminator because it
isolates the diagonal while preserving the existing vertices and face count.
Its selection uses the known failure view; no other-view acceptance follows.

The fixed builder is `scripts/terrain-deck-grid-probe.py`.
Candidate `work/copies/EXP-20260904-011/alternate-diagonal/LEVEL.DAT` SHA-256:
`572d244f1cc053ef29d2c343e4311a6ff20237c2259c5e84867bade53d57c247`.
The finer control retains EXP-009's DAT hash
`8ba384541d80da2e82a3016cf99638476229b4da7d445a9edfafdc34e365b6e5`.
TERRAIN.ALL remains
`26f3e0235533419a80b2a0eff18f423fadc20617a6c2ed2be445abeae87b35d5`.

## Prepared runtime comparison

Read-only preflight confirms the same game 46701/start 1147812, position
(163024,-102401,509900), contact (99,6973595), camera and original mesh as
EXP-010. The audit exactly matches the seven user-session processes and sink;
its fixture-ledger nonzero status is accounted against the direct handoff.

The prepared new operator uses hash-bound EXP-010 helper functions; it never
invokes EXP-010's consumed main transaction. It requires a fresh authorization
bound to this plan and operator, and an absent start receipt.

1. Original → banked finer control: 1,078 bytes at 0x006662A7.
2. Finer control → alternate diagonals: 256 bytes at 0x006664DB.
3. Alternate → finer control: the same 256-byte range.
4. Finer control → original: the original 1,078-byte prefix restored.

Each uses a compare-before-write guard, full-prefix readback and receipt.
The retained frame-limiter gate uses brief scoped stops/read-only registers.
Take five triplets: original, control, alternate, restored control, restored
original. Require matching player/contact/camera and exact paired control ROI
restoration. Classify both the 259 analytic points and 255 prior inversion
points, including the six residuals. On early failure the reserved final
restoration may restore a verified old/new byte mixture. No attempted phase
may be retried; unrelated mutations reject restoration.

At the preparation boundary no memory write, stop, debugger attachment,
gameplay input, capture, launch, close or restart had run here. Fresh explicit
authorization was required under AGENTS.md; EXP-010's permission was consumed.
The later authorized execution is documented above and cannot be rerun.

## Validation and limits

33 tests pass across the new grid invariants and existing visual fixture tests.
They cover exact 4x4 reproduction, unchanged vertices/corner attributes,
surface coverage/winding, matching shared edges, collision preservation,
capacity and unsafe outputs. Five synthetic byte-buffer operator cases pass:
exact slices/restoration, compare refusal, outside-slice refusal, short-write
detection/restoration and phase-replay refusal. They perform no OS/game writes.

`reports/terrain/EXP-20260904-011.json` retains numeric comparisons, hashes,
preflight, plan and limits; companion operator text preserves the procedures.
Memory, meshes and game images stay under ignored `work/`. Prior reports and
originals are unchanged. No full make check or new Git commit is claimed.

EXP-009's actor output still only partially matches its non-atomic live buffer
(75/387 tuples). Other camera angles, oscillating movement and a general
subdivision/diagonal rule remain open. EXP-005's floor-return failure remains
the next separate terrain task after this visibility discriminator.
