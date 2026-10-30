---
type: experiment
id: EXP-20260908-021
date: 2026-09-08
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Native PC static and offline Unicorn; Wine hardware renderer; Blender 5.2
question: How does the PC Anthill DAT store native grains, FLIK letters, seed tokens and berry pickups, and what constrains editing their placement?
result: The first DAT table holds 70 rows of 16 bytes (signed32 XYZ, selector +12, active flag +13, floor short +14) bound by 0044BB70 to 005C595C; 00456A90 keeps grain Y but derives other Y from height presets at 004C6A88, so literal XYZ needs an initializer change; 00417720 gates and dispatches pickups; tokens keep three per colour; edited tables relocate and load live
status: complete
created: 2026-09-08
updated: 2026-10-29
evidence: [EXP-20260908-021]
tags: [experiment/modding, re/collectibles]
---

# EXP-20260908-021 - Native collectibles and Blender placement

This experiment establishes the native collectible table and pickup logic in the
original Anthill files and executable, and checks what an edited table must
preserve. [[PC Anthill collectible authoring]] owns the editing workflow.

Private packet: `work/experiments/EXP-20260908-021/` (H below).
Public metadata: `reports/collectibles/EXP-20260908-021.json`.
Authoritative retail PC executable SHA256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Original Anthill DAT SHA256:
`786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
Original PC memory is the verified, asynchronous EXP020 capture (`memory.json`,
RAM region hashes), reused offline with pristine executable text. No PS1 source
was consulted for this experiment and no live writes were made.

## Confirmed PC evidence

The first DAT table at offset4 has70 rows, stride16, entries starting8. XYZ are
signed32; selector is+12, runtime active flag+13 and initialized floor short+14.
Native relocation `0044BB70` binds `005C595C`. Source inventory and SHA-pinned
bytes agree with native code:50 selector14 grains, one10–13 letter each,
one21–24 berry each, three29/2A/2B tokens each, three30 rows retained unmanaged.

`00456A90` keeps grain Y but derives every other Y from ground minus
`004C6A88[-sourceY/50]`. Original offsets0..-450 demonstrate height presets,
not literal world height. This makes unrestricted literal XYZ unsafe without
adaptation. `00456BA0` culls/render-scans the table and sets byte13 to0/1.
`tests/test_level_collectibles.py` executes pristine/patched initializer in Unicorn
with a fixed-floor callback: unmarked parity, all marked literal XYZ, empty table,
and output guards pass. Fresh live initialized XYZ/flags independently agree.

`00417720` gates active/non-consumed records, checks proximity to Flik minus230
stored Y units, marks consumed Y as INT_MIN, and dispatches counters/letters/
seed upgrades/berry selection. `H/native-pickup.json` executes all12 kinds through
original native proximity/consume/progression branches. `H/native-progression.json`
confirms grain50, letter mask15, life3→4, yellow/blue/green seed bytes68/51/51,
berry mode4, no double collection, and distant/inactive negative controls.
Feedback/audio/HUD callbacks are explicitly stubbed; this is native logic evidence,
not a rendered or audible full-progression test. The initial full-set run hit an
unmapped resource read in a random grain voice callback; the final probe also
stubs `0041A2B0` and reports it rather than representing that path as executed.

`00416100` queues plant resources per token occurrence. Preserve the original
three-per-color bounds; do not infer unlimited tiers from a byte counter.
`H/native-sprites.json` records native sprite descriptor pointers and the selector
ordering. Renderer tint code plus PC RGB bytes at004C7908 identify29 yellow,
2A blue,2B green. Berry selector/equip evidence agrees with
[[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]].
The four letter slots preserve native bit/sprite ordering; this experiment does
not independently identify each individual glyph by a new close-up.

## Edited-table checks

Edited exports with13 and0 items compile to16-row and3-row DAT tables; pointer
relocation, exact unmanaged records and unchanged terrain/plant/RAW are checked in
`H/edited-builds.json`. A full-set table keeps70 rows with every other DAT byte
exact; the executable changes only a guarded initializer hook/helper so marked
rows keep literal XYZ. In a live run, `H/runtime/pickups-*.json` verifies all67
initialized authored XYZ and selectors, and ordinary Up input for0.55 seconds
collected two grains (inventory0→2). No live memory writes.

All colors, letters, upgrades, reset/death behavior and placement near scenery
need further gameplay coverage. The three original selector30 records are
retained; their complete behavior is not newly solved. Native rewards/goals are
unchanged and duplicate letters or tiers beyond the native three-per-colour
bounds are rejected. Focused `make check` passes429 tests.
