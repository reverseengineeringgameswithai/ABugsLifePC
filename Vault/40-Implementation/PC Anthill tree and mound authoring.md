---
type: implementation
status: implemented-bounded
created: 2026-09-16
updated: 2026-10-29
evidence: [EXP-20260916-001]
tags: [terrain/scenery, terrain/collision, re/pc]
---

# PC Anthill tree and mound authoring

EXP-20260916-001 identifies the original Anthill main roots, projecting root
arch and upper trunk, and the dirt anthill beneath the arch, and imports them at
original PC size relative to Flik. No PS1 source was consulted.

## PC source evidence

Retail EXE SHA256 `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`; original DAT `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`; original terrain `62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868`. Native coordinate transform00463C80 and distant-scenery00448D70 evidence is retained in the existing trunk/distant work and this packet's source census.

**Confirmed tree composition:** detailed primary scenes 5/6/7/8/17 contain467 vertices/358 faces. Secondary 17/18 supply23 additional upper faces at geometry 307524/309372; their coordinates require4x restoration before placement. Source meshes have SHA `77c0ac2c79f729eb0dce9ee0ace9a95b26c9f15316b4fe848e9effe8d319b04d` and `e3dd7a8102d0ea80a3a61fbed68fc9cdf5e26d930fb14b98968a6e0d6adac134`. Remaining secondary faces duplicate low-detail roots and are excluded. For the original tree, all selected face commands/UVs/vertex colors/opaque fields remain intact. A21-triangle authored strip joins the detailed14-edge rim to the upper7-edge rim; total 506 vertices/402 faces. Source census, seam tests and original/native textured views are in the private experiment packet (`census.py`, `original-meshes.json`, `tests.log` and the rendered images).

**Confirmed mound identity:** the marked original-game point has Flik world(−186110,−150463,−208109). Screenshot `original-preview/frame-1789577342552511237.png`, `mound-site.json`, `og-root-opening.png` and independently matched live resident bytes identify five adjacent ground objects beneath the arch. These became one 737-vertex/617-face mound, preserving every source vertex/face field in EXP001.

| Primary scene | DAT record | Object | Geometry | Bytes |
| --- | ---: | ---: | ---: | ---: |
| 0 | 5380 | 18048 | 45868 | 5018 |
| 1 | 5400 | 18072 | 50888 | 4254 |
| 3 | 5440 | 18312 | 78136 | 4710 |
| 15 | 5680 | 18288 | 74192 | 3942 |
| 18 | 5740 | 20032 | 230728 | 806 |

`bindings.json` records hashes and exact resident pointers/bytes for all five. The original area includes separate native collision sources; a unique automatic visual-to-shell association was not established. **New tree/mound collision is authored from the editable visual faces, not copied original collision.**

## Coordinate and collision requirements

Every encoded local coordinate must fit a signed16-bit word; the placed
original-size upper trunk reached Y−39284, so EXP001 used an explicit coordinate profile
(Y down to−40960, Z up to40959, east X40959) within that limit. Native
total/per-mesh vertex, face, collision, density and resource caps remain
enforced.

Solid-scenery quads use an authored0–2 collision diagonal; faces retain
the existing Y−96 floor convention. Overly large collision triangles must be
bisected until the signed-byte64-unit Y/Z admission windows fit. This changes
collision subdivision only, without relaxing native gates or altering original
visual faces. The initial unpartitioned tall collision was rejected by the
existing admission bounds and was corrected before publication.

## Native validation

Nine native004AB1A0 landing cases support Flik on the approach/mound. Eight
full-terrain collision/removal comparisons pass: four root walls block and four
mound surfaces support while the same visual-only control passes through
(`og-size/blocking.json`).

Three original-x86 renderer contexts emit73/104/48 upper-bark vertices with bounded buffers (`og-size/native-render.json`). COM driver calls are stubbed, so this verifies native culling/transforms/material dispatch/flush, not GPU behavior or performance. The initial farther elevated camera omitted upper bark through distance clipping; closer camera contexts pass without changing the mesh or range settings.

## Limits

The identified tree has an open top/back and no 3D leafy crown. Additional
connected roots scattered around original Anthill are separate level pieces and
are not all included. Arbitrary new arrangements, distant transitions and full
hardware play remain unverified. No live RAM writes or mixer changes were used.
Original assets remain private under `work/`.
