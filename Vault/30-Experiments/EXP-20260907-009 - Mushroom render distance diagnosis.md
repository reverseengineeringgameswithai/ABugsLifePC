---
type: experiment
id: EXP-20260907-009
date: 2026-09-07
updated: 2026-10-29
status: investigated
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Existing Wine hardware Direct3D session of a derived Anthill-engine build; original PC instructions under Unicorn
question: What rejects nearby mushrooms, and can their render distance increase?
result: Sampled pop-in is polygon depth rejection; longer-group and global-distance candidates work in offline replay only
tags: [re/experiment, re/rendering, terrain/authoring]
---

> Lifecycle update: the historical 550760 preview described below is CLOSED for [[EXP-20260907-010 - General render distance preview]], which runs the same layout at 1.5× general distance. Earlier runtime/installation statements are historical.


# EXP-20260907-009 - Mushroom render distance diagnosis

The user requests RAM/static inspection of the existing Bugs session and short,
periodic forward taps to observe mushroom pop-in. [[PC scenery render distance]]
records the resulting controls and next-step options. The build is unchanged.
No PS1 material, live writes, debugger, pause, teleport or new game launch.

## Live arm

Existing game 550760/start 5083559, group 550524, display `:2`, window 14680071,
private sink `ablpc_mute_550524`. Controller/prefix remains
`work/experiments/EXP-20260907-008/preview-01`; exact derived executable
`e4ff4340b845bd3769b9946b2b52a252b5f31b16e953f814ca6903d73ee2ab2c`.
DAT `89ba7d700daadda5554e1c41634fa5a7e7c0c2f6333cea7c863cfbb7cfcc12c4`.
Same-PC renderer code regions match original retail instructions in RAM.
The private controller checks executable/stage/code and six hardware markers;
all seven generic audit processes and the private sink are independently bound.

All 28 mushroom scene/object/mesh records match their staged bytes before
movement. Stable initial copied RAM includes camera pose; the bounded low-address
snapshot is private, asynchronous and not a save state. Eight requested Up
presses of 180 ms, each followed by at least 700 ms release, retain nine game
captures and intermediate RAM samples. Flik goes from runtime XYZ
`(223518,-102276,456338)` to `(218517,-101836,490442)`, remaining in Level 1.
All keys released. A cap appears after the first tap; another appears after
the fourth. No further input after this eight-press arm.

## Native discriminator

336 scene/camera/variant cases execute original object admission and mesh
emission independently. This allows an admitted-but-zero-polygons case to be
distinguished from scene culling. Seven additional traced cases watch the
hardware depth comparison at `0x0045CF63..0x0045CF89`.

| Scene and pose | Object admitted | Passing/rejected quads at depth gate | Emitted vertices |
| --- | --- | --- | --- |
| 486, initial | Yes | 0 / 25 | 0 |
| 486, first Up | Yes | 10 / 15 | 40 |
| 488, initial | Yes | 0 / 29 | 0 |
| 488, fourth Up | Yes | 9 / 19 | 36 |
| 486, initial, longer group | Yes | 25 / 0 | 100 |
| 488, initial, longer group | Yes | 29 / 0 | 116 |

Initial scene 486 minimum tested vertex depth is 4501 against cutoff 4480;
after the first tap its minimum becomes 4383. Scene 488 goes from 4921 to 4391
by the fourth tap. Native projected bounds match the newly appearing cap
locations: scene 486 first-tap X191..245/Y216..259, scene 488 fourth-tap
X353..403/Y224..255. Captures and sampling are asynchronous, not a live branch
trace. A final copied-buffer comparison finds 16/100 and 112/116 exact XYZW
matches for scenes 486/488 at the final pose; other sampled objects have zero
matches. Idle counters are already reset, so retained page-byte matches do not
prove current submission counts or complete frame equality.

All mushroom object bytes `+0x18` are 4. The active base distance 1152 is reduced
by 32 for their draw, making the actual cutoff 4480. Existing longer group 1664
therefore gives 6528, a 45.7% effective depth increase. At the initial camera,
existing settings produce 4 emitting mushrooms; longer-group flags produce 11,
and proportional global pairs 1728/2496 and 2304/3328 produce 11 and 16.
Newly emitted target vertices retain alpha 255. This is native CPU output,
not a candidate live/GPU/performance acceptance.

## Retained corrections and limits

The first gate replay loaded camera translation but failed to replace the
rotation scratch left by the previous mushroom draw. It falsely rejected
forward objects as behind the camera. `native-replay-01.json` is retained and
invalid for scene admission. The corrected arm loads the captured camera using
original `0x004636C0` before every case; mesh output was separately initialized.
`native-replay-02.json` and seven clip traces contain the accepted results.

The first report draft labelled nominal 4608/6656 group depths as the mushroom
cutoffs. Native traces always contained the correct 4480/6528. The authored
report now includes the retained per-object adjustment; the initial draft is
preserved privately. The approximate 44% early update referred to nominal group
ratio; actual effective mushroom ratio is 45.7%.

Full-frame order/occlusion, GPU behavior and performance of any candidate remain
unverified. General expansion must account for lookup-table bounds, signed
transforms and packet allocation; these selected cases do not establish an
arbitrary maximum render distance.

## Evidence and handoff

Public authored index: `reports/render-distance/EXP-20260907-009.json`.
Private root: `work/experiments/EXP-20260907-009`, containing the pre-registered
plan, guarded observation code, copied-RAM capture, static queries/disassembly,
both native arms, seven clip traces, final code/buffer checks and exact hashes.
Frame files stay in the existing preview controller's directory and are linked
by `up-01.json`. No code or data change is inferred.
