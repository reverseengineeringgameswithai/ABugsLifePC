---
type: experiment
id: EXP-20260911-012
date: 2026-09-11
status: investigated
created: 2026-09-11
updated: 2026-10-29
binary_sha256: 62a5cb52935d4ff8760b1f224ddcd68effcac8c277d0516f0913aa45df5d6193
environment: Existing muted Wine Gamescope hardware session; original PC x86 in offline Unicorn
question: Why is a far wall corner missing from view in a derived Training build, and can render distance increase?
result: Corner passes scene admission but exceeds polygon depth limit; 2x original settings restore it in copied-state CPU replay only
tags: [experiment/training, re/rendering]
---

Subsequent implementation: [[EXP-20260911-013 - Twofold distance and Training performance]] installs the authorized shared2x setting,
verifies the corner/performance live and closes old game86443. The diagnosis-only
runtime and no-setting-change statements below describe EXP012's earlier stage.


# Training corner render distance diagnosis

The user asked for inspection of a far wall corner missing from view in a
running derived Training build (the EXP011 preview). That session is left in
place with no input, live writes, pause, relaunch or build/settings change.
[[PC general render distance]] already provides the bounded2x setting; this
experiment diagnoses its relevance to the new view, not a live installation.

## Confirmed current view and identity

Game86443/start5551524/group86212 uses the frontmatter EXE, Training DAT
`d5ed5105a41814ae7a0acfc1d25793eb589428494373dd98046a67542a995bcc`, and the
EXP011 private null sink. Six hardware markers and original content paths pass.
`before.png` captures the gap between distant walls. A subsequent6.55s read-only
capture retains equal before/after Flik(42261,-32962,581896), camera translation
(23019,-45769,560462) and matrix. The screenshot and RAM are asynchronous.

All25 wall scene flags are0x59 in both DAT and resident memory: the longer
distance group is **already selected**. Scene/object/mesh identities match.
Current near/far globals at005C02FC/005BA80C are1728/2496, the accepted1.5x
original profile. Object+24 depth adjustment is0 on these walls.

## Native discriminator

Original scene admission0044D59F accepts scenes297..303 at this camera. The
missing corner is scene300, while299/301 are its adjacent wall chunks. Original
quad rejection0045CF63..0045CF89 compares all four signed camera depths to
four times the active group distance. Its current limit is9984 stored units;
scene300's tested depths are11440..11556, so all16 front-facing quads fail.
Adjacent299/301 lose16/20 quads, leaving the visible partial wall ends.

The diagnostic executes every wall independently through admission and draw
under two settings,50 cases total, restoring the captured camera before each.
The2x original pair2304/3328 raises the wall limit to13312,33.3% beyond the
current distance. It restores all52 rejected quads across299..301 without
changing flags, meshes, bounds or transforms:

| Scene | Current emitted vertices | 2x emitted vertices | 2x projected X/Y bounds |
| --- | ---: | ---: | --- |
| 299 | 48 | 112 | X355..430, Y225..293 |
| 300 | 0 | 64 | X309..355, Y228..283 |
| 301 | 32 | 112 | X234..309, Y226..291 |

All admitted wall faces pass the distance test in that candidate at this pose.
Admission results are unchanged. Original instructions at0044D59F..0044D73D,
0044D73E..0044D83F and0045CF63..0045CF8E independently match the running
game byte-for-byte. Disassembly, private capture and native output provide
separate evidence forms. This is CPU output, not a candidate GPU screenshot.

## Retained correction and limits

The first adapted mushroom replay incorrectly selected the shorter draw scratch
unless its optional flag override was supplied, despite these staged walls
already having bit0x40. Its nominal “current”6912 limit did not fit the screenshot.
`resident.json` and the staged writer's final0x59 assignment resolve the conflict.
`diagnosis-superseded-labels.json` and `diagnose-superseded.py` remain private;
only corrected `diagnosis.json`, which respects the actual scene flags, supports
the table above. Do not recommend switching these walls to the longer group:
they are already in it.

The recommendation is a2x distance preview using existing guarded settings.
It fixes this captured corner in CPU replay, but remains a finite distance.
All-camera coverage across the whole derived level, full-frame packet load,
live GPU appearance and performance at2x remain unverified for this build.
The shared initializer changes other levels too unless separately scoped; no
global or Training-only implementation decision is made by this diagnosis.
Larger arbitrary distances exceed the current validator's investigated envelope.

No code, Blender file or game lifecycle changes. Existing render-distance checks and final Vault/audit gates are in
`reports/render-distance/EXP-20260911-012.json`. Assets, copied RAM and detailed
native output stay under `work/experiments/EXP-20260911-012/`. No PS1 work.
[[2026-09-11 - Codex - Diagnose missing Training corner]] records the handoff.
