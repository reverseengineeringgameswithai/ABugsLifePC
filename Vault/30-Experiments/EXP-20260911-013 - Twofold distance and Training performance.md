---
type: experiment
id: EXP-20260911-013
date: 2026-09-11
status: implemented-bounded
created: 2026-09-11
updated: 2026-10-29
binary_sha256: bf9d83ae735505fcfd4acef62bf8343f641e8553213ca2b112a04a6d09353a0a
environment: Owned muted Wine Gamescope hardware Direct3D; native PC primary-scene replay
question: What does raising both render-distance groups to 2x require in the executable, and what does it cost in native capacity and measured performance?
result: Five initializer bytes at 0044BBA3/0044BBAF (2496 to 3328) and 0044BBC1 (-768 to -1024) give near 2304/far 3328 and the live lookup table matches; primary emission rises 3281 to 3728 vertices with maximum batch 497 of 500; matched 60 s runs in one view show 31.23 versus 31.25 FPS with similar CPU and RSS
tags: [experiment/training, re/rendering, implementation/modding]
---

# Twofold distance and Training performance

This implements the 2x profile proposed in
[[EXP-20260911-012 - Training corner render distance diagnosis]]: near2304/far3328
instead of the 1.5x 1728/2496, through the existing shared initializer, and
measures its cost in one Training view where the 1.5x setting left a hole in a
distant corner.

## Executable change

Only five EXE bytes change relative to the 1.5x build, within immediates
0044BBA3,0044BBAF (2496→3328) and0044BBC1 (-768→-1024); frontmatter EXE hash.
Every CD file remains byte-identical, including the Training DAT
`d5ed5105a41814ae7a0acfc1d25793eb589428494373dd98046a67542a995bcc`.
`preservation.json` records complete inventories and exact executable spans.

## Native capacity and live visibility

The two distance initializers run against copied EXP012 state, then every one
of371 primary scenes passes through original admission and the appropriate
draw pass/group. Both profiles admit37 scenes. Original projection, emission,
automatic flush and counter reset emit3281→3728 vertices (+13.6%), with nine
batches in each case; maximum batch size496→497 stays within500. Indices and
finite projected values pass. Six COM sites return synthetic success while
the original flush logic runs. Actors/background and GPU timing are outside
this offline primary-scene check.

Two private builds use identical guarded file-built start and camera hooks
from the EXP012 view. Their complete CD trees match, and the EXEs
differ only in the same five initializer bytes. Camera hook401B81 chains the
prior target through cave004BBE00; startup43C1D1 chains through004BBD00.
Neither diagnostic hook is part of the normal build.

All six hardware markers pass for both launches. Baseline
`base-play/frame-1789159349958581035.png` reproduces the hole; candidate
`candidate-play/frame-1789159585494192641.png` shows a continuous corner.
Live near/far globals match2304/3328, and all4095 lookup words match the native
initializer reference. Hardware evidence therefore confirms the previously
offline-only remedy in this view.

## Measured performance

Each profile receives a60s stationary trial after menu/startup and speech settle.
Flik remains at runtime(42261,-32961,581896) in both. The same file-built camera
is supplied immediately before every world draw. Samples and screenshots are
asynchronous:240/241 baseline camera samples match the fixed pose; one catches
a different translation between updates. Candidate has241/241. This does not
justify an assertion that every live camera read was identical.

Gamescope3.16.25 reports FPS per300 compositor paint calls; the first report
overlapping the measurement start is excluded. The installed version matches
the [upstream sampling logic](https://raw.githubusercontent.com/ValveSoftware/gamescope/3.16.25/src/steamcompmgr.cpp).
Linux `/proc` counters supply CPU and resident-memory measurements. These are
coarse output-rate windows, not individual GPU frame times or1% lows.

| Measurement | Previous1.5x | New2x |
| --- | ---: | ---: |
| Trial duration | 60.070s | 60.068s |
| Complete sampled FPS windows | 5 | 6 |
| Median reported FPS | 31.227 | 31.250 |
| Window FPS minimum–maximum | 31.221–31.279 | 31.243–31.257 |
| Game CPU, percent of one core | 101.581% | 101.684% |
| Maximum game RSS | 395.688MiB | 396.313MiB |

**Bounded conclusion:** no material slowdown is observed in this comparison.
The+0.073% FPS change is not evidence that greater distance improves speed.
CPU differs by0.103 percentage points and RSS by0.625MiB; one pair of trials
does not attribute these small differences causally. Other views,
movement-heavy scenes and other machines are unmeasured.
The2x setting still has a finite cutoff; this is not unlimited distant rendering.

79 selected render-distance/Training/Soil/occlusion tests pass through make check
in39.30s. The initializer checks cover original/1.5x/2x at both renderer
branches and retain table bounds. `reports/render-distance/EXP-20260911-013.json`
contains asset-free fingerprints, settings, measurements and evidence paths.
Private binaries/captures remain in `work/experiments/EXP-20260911-013/`. No
external live RAM writes, PS1 comparison or original modification.
