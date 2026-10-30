---
type: experiment
id: EXP-20260907-026
date: 2026-09-07
binary_sha256: 431ec953b67bd3233f8fa58e7a22edbfabaeb153e3ee322d760c45f2a44c7d8f
environment: Private original-PC Unicorn probes and guarded Wine hardware previews
question: Why does retessellated terrain collision change native ground contact, can visual density increase without changing it, and where can frame work be observed before pacing?
result: 004AAE30 checks the projected endpoint against the current triangle through 004A9860 and 004AB1A0 clears grounded state when neither it nor the collision path reports support, so retessellated collision causes brief airborne transitions; refining only visual triangles with collision bytes unchanged matches 124 floor, 138 interior and 24 wall native routes exactly; the elapsed value at 00405B63 covers render/present only
status: bounded
tags: [terrain/authoring, re/rendering, implementation/modding]
---

# EXP-20260907-026 - Collision-preserving visual density and frame work

This experiment follows the EXP-025 retessellation counterexamples. No PS1
source, debugger stops or live external writes. Artifact index:
`reports/terrain/EXP-20260907-026.json`; private packet:
`work/experiments/EXP-20260907-026/` (prefix below applies to named artifacts).

## Confirmed slope mechanism

`trace-slopes.py`, `slope-calls.json` and `slope-diagnosis.json` replay the three
rejected EXP-025 seam-preserving interior cases against unchanged original PC code.
At stored points (8800,23600), (10000,23600), (11200,23600), zero-based step 5 has
identical positions but different results from `004AAE30`: control returns 1,
refinement returns 0. `004A9BA0` returns 0 in both. The refined flags become [0,0]
while control remains [1,1]. Step 6 then enters `004AA4D0` in the refined arm,
producing the previously observed 103/51/64-world-unit position differences.

Static evidence `004aae30.c`, `004a9860.c`, `004ab1a0.c` comes from the indexed
Ghidra query: `004AAE30` projects the motion and checks the endpoint against the
current triangle through `004A9860`; `004AB1A0` clears grounded state if neither
the current-triangle check nor the subsequent collision path reports support.
This confirms the branch causing the brief airborne transition. It does not prove
that every rejected retessellation difference is caused solely by plane rounding,
nor does it establish a general solver defect or a safe replacement solver.

## Visual-only refinement check

A visual-only refinement splits demonstrated 0x61 triangles with identical
unknown vertex fields at a strictly interior exact integer lattice point into
three faces, after chunk membership, origin, bounds, visibility radius and
collision bytes are fixed. Positions stay on their exact parent plane;
edges/winding stay intact; RGB/UV interpolate; other commands/mixed unknown
fields stay unchanged. No native solver patch is used. Directly subdividing the
authored collision mesh remains behavior-changing.

| Measure | Control | Visual-detail trial |
| --- | ---: | ---: |
| Encoded chunk faces, including scenery commands | 4435 | 9249 |
| Authored collision triangles | 2365 | 2365 |
| Interior native candidate peak | 27 | 27 |
| Emitted vertices across 12 renderer contexts | 31077 | 50841 |
| Native object-render instructions across those contexts | 19733564 | 36302198 |

TERRAIN, PLANTTER and the normal executable are byte-identical to the control.
Chunk origins, radii and collision payloads are unchanged. The visual-detail DAT
SHA is `1b62f9de63db0cca6cb9b6bcbd64a37e4e80b2a8e219f7ed0a27117f05f749c7`.
`native-seams.json`, `native-grid.json`, `native-wall-seams.json`: 124 floor routes,
138 interior routes and 24 wall pushes match exactly in position, contact, flags
and native instruction count, plus five landings and two exit-helper cases.
The grid includes all three previously failing slope starts. `native-frames.json`
executes 12 original renderer contexts, all four chunks, native flush/counter-reset,
finite vertices and valid indices; maximum batch 499 in both arms. Six COM calls
are stubbed, so this is native CPU/buffer evidence, not GPU timing or pixel proof.
In live hardware arms all six log markers pass, every one of the170 native model
payloads verifies, and all four exact resident chunk meshes/colliders match.

## Frame-work measurement and limits

**Scope correction, EXP028:** the old timer measures render/present only.
0040FFC0 calls gameplay004144C0 before renderer0044D430 starts timestamp00405C07;
therefore these samples exclude gameplay update. [[EXP-20260907-028 - Representative update and render headroom]] preserves the old
private artifacts and records both boundaries separately with QPC. The historical
stationary observations below remain valid for their narrower render interval.

Private diagnostic images only: `frame-work.asm`, `build-telemetry.py`,
`telemetry-patch.json`. A guarded five-byte hook at `00405B63` records the existing
elapsed value after `00405AD0`'s hardware present path and before its deliberate
frame pacing. It preserves native division, registers/flags and pacing. Two private
image bases and ring wrap pass; exact inverse restores the normal executable.
The 2048-entry ring is at `0106A000`, within the end of the dedicated arena;
these arms verify the retained cursor below 7 MiB. This is a bounded diagnostic,
not a production allocation reservation. Instrumented EXE SHA:
`2baed7096dabc31c460b7049dfb025d2e63883f7d15bfeb94435c6c8755866f4`.

Both 20-second samples stay at world (192000,-102400,448000), heading 0, with
zero sampled input and unchanged state. Control captures 624 frames: work p99 2,
max 6 ms; detail captures 625: p99 0, max 2 ms. Their paced means are about32.04
and32.00 ms. Receipts: `timing-control/frame-work.json` and
`timing-detail/frame-work.json`. Values are integer-millisecond timer units;
most samples resolve to zero. This establishes measured render/present work before pacing at
spawn, but does not resolve a reliable performance difference, establish effective
sub-millisecond precision, or isolate GPU work. Camera matrices were not logged
with these samples; equal spawn state is not an independently verified identical
camera context. Host activity and native present scheduling remain confounders.
Do not call the dense arm faster or treat these stationary samples as worst-case
headroom. Representative route/camera timing remains open.

## Tests and next discriminator

39 targeted source tests pass, including synthetic sloped topology/area/plane/
winding/attribute checks, malformed input and growth rejection. The broader
selected `make check` passes1219 tests in151.86 seconds.

Full respawn/exit cycles, timed complete traversal, broader actor endurance,
representative hardware headroom and wider-coordinate behavior remain unaccepted.
Next: apply the timer only to equivalent representative camera/route
comparisons, recording camera context/input and model integrity.
