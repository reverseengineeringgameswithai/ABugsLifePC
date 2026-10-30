---
type: experiment
id: EXP-20260907-017
date: 2026-09-07
created: 2026-09-07
updated: 2026-10-29
status: implemented-runtime-observed
environment: Wine Gamescope Direct3D, Blender 5.2, offline Unicorn PC instructions
question: Why does Flik's model show moving blue planes after an authored LEVEL.DAT grows, and what storage limit does it reveal?
result: A 654120-byte DAT shifts Flik body18's polygon stream to 0076F923, across renderer scratch 0076F9A0..0076F9AF that native stores overwrite; offline causal replay confirms; sharing byte-identical mesh streams (DAT 597744 bytes) moves body18 clear and its 436 bytes stay intact live.
evidence: [EXP-20260907-016, EXP-20260907-017]
binary_sha256: 3a2e6ca8463752463751c5eefc031e109d17e1ddaa9dc079615446b1f0454a77
tags: [experiment, terrain/authoring, re/rendering, tooling/blender]
---

# Trunk scenery and character storage overlap repair

An authored Level01 layout appended five original PC scene meshes (5/6/7/8/17,
EXP-016) and a decorative apron, growing LEVEL.DAT to654120 bytes. Native scene160
became4985 vertices/117790 bytes/radius20882; eight native camera/animation
contexts pass finite packet, indices and500-vertex batching. Those checks covered
scenery only and **did not establish character safety**.

## Confirmed regression and causal repair

Moving blue planes appear on Flik. `planes-01/moving-planes.mp4` and
`planes-02/trace.json` under `work/experiments/EXP-20260907-017/` preserve the
artifacts, including stationary-position idle poses. A7.37s read-only memory
capture has equal before/after pose/camera; no atomic-frame claim or live write.

The oversized DAT654120 bytes shifts Flik body18's polygon stream to0076F923.
Its436-byte extent crosses renderer scratch0076F9A0..0076F9AF. Original OG
body18 at00704D77 provides the immutable reference. Native writes at004063CB,
0040640C,0040644B,00406491 and0040DE04/3E,0040E230/26A overwrite the stream;
`scratch-store-disassembly.json` independently records the original PC store
instructions. `flik-triangles.json` shows malformed local coordinates10468 and
15104 read from that overlap.

`flik-causal-replay.json` executes nine captured poses with original PC drawing.
Restoring the original bytes at the overlapping address still corrupts them
again. Moving only body18 storage to a safe offline location preserves them
and removes the outliers. Frame108's projected maximum X falls from15192 to356;
frame110 from11034 to363. These are offline Unicorn mutations, never live writes.
The earlier scenery-only acceptance was insufficient, not evidence against the
observed artifact. The defect is model storage overlap, not a collision jolt.

The compiler now reuses complete byte-identical positive mesh streams already
referenced by native objects. Separate object transforms, animation selectors,
collision descriptors and payloads remain intact. Reusing geometry for
duplicate append operations saves56376 bytes. Final DAT597744 bytes;
combined DAT/TERRAIN/PLANT970440 bytes. A conservative1000000-byte authoring
budget rejects the failing1026816-byte load. This is a pinned-resource budget,
**not a derived universal heap limit**; runtime storage checks remain required.

In the replacement live game, body18 is at00761CEB,56065 bytes clear of the
scratch after its complete extent. Repeated18s read-only comparisons preserve
all436 original bytes. A20s188-frame/2525-sample sequence includes idle animation
and movement, with226 unique player snapshots; inspected frames show normal
Flik geometry. The native causal replay is the stronger specific regression
check.

## Validation

1138 selected `make check` tests pass;97 focused sharing/compiler tests pass.
Synthetic sharing, original/mod native relocation, exact UV/opaque preservation,
combined load rejection and unchanged collision/EXE checks cover the changes.
Report `reports/terrain/EXP-20260907-017.json` indexes private evidence/build.
The corrected run's full scene160/source99/perimeter/PLANT resident comparisons
pass; its retained files are in `EXP-017/preview-02` and its executed EXE is
3a2e6ca8...f0454a77. Originals and external PS1 sources are untouched.
