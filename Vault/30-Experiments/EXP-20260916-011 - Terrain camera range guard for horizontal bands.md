---
type: experiment
id: EXP-20260916-011
date: 2026-09-16
status: implemented-bounded
question: What causes intermittent broad horizontal bands across far terrain, and what minimal guard prevents them without changing geometry or collision?
binary_sha256: 7bd89ae301df163c713e8b18bf3b4cf061ec15b22f43c33c4612cc14eb4c9611
environment: Linux, Studio, Wine hardware Direct3D
result: 0045A7F0 narrows transformed camera coordinates to signed16 while 00463770 keeps full 32-bit translation, so far terrain vertices wrap (camera X -36442 becomes 29094) and emit screen-wide batches; a hook before 0045A7F0's prologue that drops whole faces with any vertex outside [-32768,32767] removes the reproduced batches and the bands in 92 checked hardware frames.
tags: [experiment/terrain, experiment/rendering, re/pc]
---

# EXP-20260916-011 - Terrain camera range guard for horizontal bands

Intermittent broad horizontal bands appear on an authored Level01 layout near an
eastern path. Packet `work/experiments/EXP-20260916-011/`. No PS1 source
consulted. Authoring geometry, collision and assets remain unchanged.

## Reproduction and original-PC diagnosis

`reproduction/walk.json` binds old EXP010 game487797 at(742287,-103548,384691), heading4065. Continuous Up3.583s yields13 captures; before/forward1/2/3 visibly show broad green/dark horizontal bands, then they disappear as Flik moves forward. This confirms intermittency, not an all-heading failure. Preliminary eastern-circle movement is blocked by a large mushroom and is not a full circle.

`native-with-distant.json` replays exact PC primary0044D59F admission,0045A7F0 transform and004498F0 emission at recorded cameras, plus secondary renderer control. Primary scene486 western lower terrain mesh DAT543296 produces page1 spans X[-2553,3193]/Y[87,196] initially and[-2695,3336]/[85,196] at forward2, matching the broad-screen band heights. The forward5 camera no longer emits that unsafe batch. Original00463770 retains full32 translation (`native-translation-static.json`);0045A7F0 repeatedly narrows transformed camera coordinates to signed16 (`native-transform-static.json`, `native-stores-disassembly.txt`). Example full camera X-36442 narrows to29094, reversing its side. At initial/forward2,625 unsafe vertices touch1027 visual faces.

`native-mesh-filter.json` removes complete faces touching out-of-range vertices in a private fixture, eliminating the offending batches. `native-assembled-guard-frame.json` tests the actual new assembled helper; `renderer-comparison.json` shows only the two offending primary scene486 entries change across three cameras, while every other primary/secondary batch summary is exact. These controls separate camera-word wrap from texture-detail assumptions.

`page1-source-census.json` and `tree-versus-ground-control.json` show that both
authored tree and grass faces contribute unsafe vertices (rejecting14 unsafe
tree faces leaves a grass batch; rejecting1013 unsafe non-tree faces leaves tree
output), so the wrap is not specific to one kind of content.

The first quad callback at0045F134 rejects zero faces and leaves the bands unchanged (`native-face-overflow-filter.json`): ineffective/inconclusive, not positive evidence.

## Scoped visual guard

`research/terrain-camera-guard/render.asm` hooks native0045A7F0 before its6-byte prologue. The helper checks level1/hardware and only eight validated positive terrain mesh offsets/counts. It computes all three full32 camera axes with native truncation toward zero; vertices outside[-32768,32767] are unsafe. It copies the mesh header/all12-byte vertex attributes and complete safe12-byte triangles/16-byte quads into private scratch, preserving UV/colors/unknown fields. Empty groups are omitted. Unsupported command tags reject at build time; malformed selected streams fail closed at runtime and count parse aborts. It restores registers/flags and replays the displaced prologue. Resident source/collision bytes are untouched.

`terrain_camera_guard.py` bounds mesh/PE reads, enforces original prologue/non-overlapping relocation/two vacant section slots, and installs PIC700-byte `.camdraw` RX plus331,776-byte `.camdata` RW BSS. Native vertex/face/load/chunk caps are unchanged. Synthetic Unicorn controls cover boundaries/allaxes/negative truncation, groups/attributes/opaque bytes, two load bases/registers/flags, other-level/software/unlisted passthrough, malformed streams and exact PE inverse/drift rejection.

## Live validation

The guarded executable `7bd89ae301df163c713e8b18bf3b4cf061ec15b22f43c33c4612cc14eb4c9611` keeps every CD file byte-exact to the unguarded build; removing the guard restores that build's EXE exactly. A fresh run, whose only other change is the12-byte spawn row at004DC7F4 set to the reproduction point, repeats the original continuous Up from(742287,-103545,384685) to(733662,-160309,561574) (`final-exact-up/walk.json`, 3.588s,13 captures) after six hardware markers. All92 formal final frames are viewed (`final-gpu-inspection.json`) and show no reproduced broad bands. `final-live-validation.json` matches complete native hook/helper code and all8 resident source meshes to disk; accumulating matched-call/rejected-face/unsafe-vertex counters and zero parse aborts prove actual guard activity. No live writes. Scoped make check **154 passed/7130 deselected**, not full suite (`make-check-final.log`).

## Limits

Whole-face rejection conservatively prevents coordinate wrap; it is not near-plane clipping and can pop at the range boundary. Wider headings/corners/distant transitions and performance remain unmeasured, and the guard covers only the validated mesh offsets it lists. Initial spawn-height selection remains unresolved. No affine PC-renderer claim. Public safe metadata `reports/moonlit-ground/EXP-20260916-011.json`; originals and private binaries/assets remain untracked.
