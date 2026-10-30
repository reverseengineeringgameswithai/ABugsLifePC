---
type: experiment
id: EXP-20260906-006
date: 2026-09-06
created: 2026-09-06
updated: 2026-10-29
status: original boundary localized; positive-winding barrier contained in bounded native and live checks
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 43 original-PC static/native analysis and isolated Wine runtime previews
question: "What blocks Flik at the original Level01 foliage edge, and does an authored kind-0x101 X/Z barrier loop contain him under the original PC collision code?"
result: "The original edge is a kind-0x101 barrier (source180 segment160); clearing only the 0x101 head lets the same path through while triangles remain. Winding decides containment: an authored eight-segment loop contains with positive winding (31/32 native cases, user-reported no falls live) and not with negative winding (0/32)"
tags: [re/experiment, terrain/collision, terrain/authoring]
---

# EXP-20260906-006 - Perimeter barriers and original foliage reference

## Question and scope

The user reported that berries stop at the edge of the isolated EXP-005 platform but Flik can fall off. This experiment asks what forms the original Level01 foliage boundary and whether an authored kind-0x101 X/Z barrier contains Flik. Projectile stopping and player blocking are separate observations, not proof of a shared collision path. This experiment was allocated after checking the existing 2026-09-06 experiment directories through 005. The original-foliage comparison is a successor arm of the same perimeter question, not a duplicate experiment ID.

EXP-005 remains an unchanged control on disk. Original Windows PC assets/instructions are authoritative; no PS1 evidence was used.

## Earlier offline perimeter trial: contradictory evidence retained

`terrain_perimeter.py`, `terrain-perimeter-probe.py`, and synthetic regressions add a checked, allocation-preserving short-loop candidate using the established 0x101 X/Z barrier grammar. The private source178 donor has payload offset220764, size452. The eight-segment outline follows the platform/ramp union, inset64 stored units; it does not place a segment across the shared ramp seam. The candidate preserves unknown fields and unused allocation bytes. This inset is a hypothesis, not an established universal radius.

The earlier affected run passed35 tests in1.88s. The original-PC diagnostic tested32 midpoint/corner/grounded/airborne cases per arm: unbarred control0/32 contained, positive winding14/32, negative winding0/32. Native duration25.035630978s. **Neither winding is accepted.** Driver exit0 reports completion, not acceptance. Failed cases have not yet been localized sufficiently to assign a cause. Receipts: `work/experiments/EXP-20260906-006/affected-tests.xml` and `perimeter-native.json`. No foliage render asset was paired with either candidate.

## Original foliage reference

A fresh isolated original-asset copy was launched through the accepted auto-hardware executable. The user navigated to the foliage and the location and angle were recorded. The capture shows tall, densely packed grass blades directly ahead of Flik, at the outer terrain edge. This visually identifies the reference; by itself it does not identify an exact render record or prove the responsible blocking segment (see the boundary discriminator below).

The passive observation sent **no input, focus command, live write, teleport, process stop, debugger operation or save-state command**. Two read-only samples bracket the asynchronous compositor capture; this is not an atomic frame/RAM snapshot. Position, both angle words and camera data agree across the samples.

- Internal level at `0x00861C84`: **1**.
- Current XYZ at `0x0059D910`: **(292407, -31849, 537453)**, signed world coordinates.
- Preceding XYZ at `0x0059D920` and auxiliary XYZ at `0x0059D960`: same coordinates.
- Facing word at `0x0059D930`: **979** (`0x3D3`).
- Related angle word at `0x0059D938`: **976** (`0x3D0`), retained in the raw actor block; do not conflate it with the current facing word.
- Camera translation at `0x005BDB8C`: **(263125, -44646, 535025)**.
- Camera matrix bytes at `0x005B58E0`: `2d0100000bf0110000100100f50feeff2d01`.
- Contact words at `0x007F3D68`: **(100, 6978815)**. A cached contact pointer alone does not establish grounded state or a foliage collision event.
- 0x101 barrier list head at `0x007F3D3C`: **7152075**; LEVEL.DAT base at `0x005BA240`: **6596791**. These pointers are process-specific.

Position/angle field provenance: [[EXP-20260905-007 - Retail position control and missing floor footprints]], including retail initialization at0x004389BF/0x004389C5 and input-relative angle updates in0x0043F7E0. This reference grants no future teleport authorization.

Private evidence:

- `work/experiments/EXP-20260906-006/og-preview-01/foliage-reference-1788734450118732397.json`
- `work/experiments/EXP-20260906-006/og-preview-01/foliage-reference-1788734449773989301.png`
- Frame SHA-256: `492b11fe73b61a6feed6adccfcd4a30c473d083f4093fd638c560f6fc49785aa`; decoded640x480/nonuniform, size/mtime stable for at least0.2s before hashing; visually inspected.

Original-run provenance:

- Stage: `work/copies/EXP-20260906-006/og-game`; copied original assets, not EXP-005 assets.
- Prefix: `work/experiments/EXP-20260906-006/og-preview-01/prefix`; isolated from the closed preview; R: resolves to the new stage root.
- Executed auto-hardware image SHA-256: `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`. Do not label it unchanged retail executable code.
- Staged retail executable: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Original Level01 TERRAIN.ALL: `62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868`.
- Original Level01 LEVEL.DAT: `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.

All six positive hardware renderer markers passed in the fresh log. Read-only mapped movement bytes at0x004AB1A0 and the original spawn row at0x004DC7F4 match the pinned executed image. The current pose was reached by the user; the assistant did not complete or claim an observed pristine menu-navigation sequence.

The initial launch's discovery command failed before input because its process scan omitted the compositor. This failed discovery is not a renderer or game failure. The later passive receipt independently binds the compositor socket peer and game identity. No retry launch was made.

## Original boundary discriminator

At the saved original pose, the original-PC coordinator admits Level01 source180 segment160, endpoints(9187,16391) and(9221,17067), point file offsets221628/221640. The positive arm has38 segment response updates and blocks/deflects the approach. Clearing only the 0x101 head in private emulated memory removes those updates and lets the same synthetic path pass through the boundary. Original triangles remain present. The first responding candidate pair byte-matches that original segment. Receipt: `original-grass-boundary-native.json` under this experiment's private directory.

The original blocked push also produces flags[1,0]; release/retreat returns[1,1]. Thus the earlier14/32 positive-winding gate must not be paraphrased as18 falls: every positive-winding sample remained over the authored footprint. Its strict contact-state and outward-progress criteria also reject blocked contact and tangential sliding. The old report stays rejected under its original criteria; no aggregate is silently relabelled.

The longer successor matrix contains all32 midpoint/corner/grounded/airborne approaches, and all three ramp lanes complete repeated downhill/uphill routes. However only31/32 cases meet the full straight-release/settle criterion: lower-ramp edge2 stays contained but continues alternating contact states near the corner. A separate explicitly steered return to X6000/Z11900 finishes[1,1] without resetting position. The original matrix remains false; the steered discriminator is additional bounded evidence. Native duration20.051271131s. Receipts: `grass-native.json`, `grass-corner-steered-return.json`. No live memory intervention was used.

## Live barrier check

A file-loaded run of the isolated area with the eight-segment positive-winding 0x101 loop in the source178 allocation at220764 (TERRAIN.ALL `56c167c1786b9fa3bf91963efd5334996a8e6a28d8ca633b66aefacdde9f02ba`) observed initial gameplay position **(192000,-102400,448000)** and heading3505. Read-only verification matched the full source99 payload and the complete8-segment barrier allocation after its loader link. The user subsequently confirmed no falling off. This confirms file loading and a bounded live containment report, not all-route collision. A four-second normal Up attempt and read-only samples are retained in `live-edge-up.json`; it is not used as a controlled whole-perimeter runtime proof. No writes, teleport, debugger or process stops were used.

## Original grass census

`offscreen-grass-census.json` enumerates **34 original scene placements,31 unique meshes and439 raw blade-candidate signatures** from the original Level01 file, including geometry outside the saved view. This is not an all-resident-RAM census or an exhaustive classifier for every plant. Matching tags alone are insufficient: some short decorative plants share them.

## Remaining questions

Map the view and saved pose to exact original render faces/assets, retaining offsets and unknown fields. Compare the visible grass line with the collision line; do not assume the grass mesh itself collides. Test projectile behavior separately. The lower-ramp edge2 release limitation stays recorded. [[EXP-20260906-007 - Plant-state collision regression]] covers the separate plant/mushroom collision path.

No full suite/R2q was performed for the passive reference capture. Private assets, screenshots and raw RAM bytes remain under `work/`; the public report contains only coordinates, hashes and provenance.
