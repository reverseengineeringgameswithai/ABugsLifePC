---
type: experiment
id: EXP-20260911-015
date: 2026-09-11
status: confirmed-bounded
created: 2026-09-11
updated: 2026-09-11
binary_sha256: f55c3612f60fb1fba373c55d8cab6afcac96cf00d4156c542963234aa58b7059
environment: Same owned muted Wine Gamescope hardware run; copied-state original PC execution
question: Why does the grass strip remain visible from the farther user position?
result: Target is secondary scene15 background geometry with quarter camera translation and distinct clipping; both views match live vertex buffers
tags: [experiment/training, re/rendering]
---

# Training grass uses secondary background geometry

> Relationship clarified by [[EXP-20260911-016 - Training grass boundary near and distant representations]]: this is the simplified distant version
> of a real grass boundary with detailed primary meshes. Geometry and camera
> are both quarter-scaled; the pass label does not imply decorative scenery.

**Confirmed:** the grass strip selected in the user's crop is secondary scene15,
not the flower panorama or the13 primary plants measured by EXP014's follow-up.
It remains visible because the PC handles it as distant background geometry,
with geometry and camera both in quarter coordinates and a separate
admission/rendering pass. EXP016 relates it to the detailed physical boundary.
It is not subject to the primary walls' distance rules on the same coordinates.

## Correct the object identification

[[EXP-20260911-014 - Training flower panorama and wall cutoff]] established two valid but differently scoped facts: the large
flower strip is panorama artwork, and13 selected primary plants fit the2x
range at the initial pose. Neither identifies the user's thin grass strip.
The crop resolves this ambiguity. Earlier replies applied results from other
objects to the intended target; do not repeat the13-primary-plant measurement
as the explanation for this grass. The panorama result remains valid for flowers.

## PC evidence

Same EXP013 game91321/start5734777/group91091; EXE
`f55c3612f60fb1fba373c55d8cab6afcac96cf00d4156c542963234aa58b7059`, Training DAT
`d5ed5105a41814ae7a0acfc1d25793eb589428494373dd98046a67542a995bcc`.
The new read-only capture brackets unchanged Flik(17699,-5761,446467), camera
(12776,-19271,474844) and matrix `3cf000004afd01000010fbffb602faff3cf0`.
No new game input, live write, suspension, launch, close or asset/settings edit.

Original retail SHA256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Resident secondary code0044D83D..0044DBEE and00448D70..004498F0 equals retail.
Original secondary admission runs directly from0044D83D to the renderer call;
then each admitted scene runs00448D70 separately on the resulting context.
Current pass translates camera to(3194,-4817,118711), stored(99,-150,3709),
sets secondary flag005BA120=1 and scratch005B56D0=400. It temporarily changes
far3328 to3069. Shared far still affects secondary admission; this layer is
not unlimited or completely independent of the setting.

Secondary15 uses object offset17384, geometry116176 and page4
UV rectangle(192,192)..(255,224), the original alpha-cutout grass tile. Its
current screen extent is X230..576/Y200..239; triangles over the passage opening
sample that tile. Selected transparent samples expose the blue panorama, while
opaque grass samples are green. Pixel interpolation alone is not asserted as
exact final shaded colour.

Strong runtime corroboration: **92/92 complete emitted32-byte vertices** match
captured live page4 buffers in the farther view. Replaying the original EXP014
initial capture gives **60/60 complete matches** for the same secondary scene.
Both admit the target through the original secondary tail. These are native
CPU/resident-buffer results plus source texture and visible capture evidence;
no GPU command tracing is claimed. The primary candidate search is retained to
show why the earlier primary-only explanation did not identify the strip.

## Scope and next action

Asset-free report `reports/render-distance/EXP-20260911-015.json` hashes the
private capture, user crop, source texture, native scripts, pixel candidates
and code verification. This is a corrected diagnosis only. No larger distance,
wall proxy or renderer change is installed, and no new performance result is
claimed. Moving real walls into this layer is not validated; their perspective,
collision and occlusion requirements differ. Next: user feedback.
[[2026-09-11 - Codex - Identify the distant Training grass layer]] owns validation and closure.
