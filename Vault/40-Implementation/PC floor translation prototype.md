---
type: implementation
status: bounded-prototype
created: 2026-09-04
updated: 2026-10-02
tags: [implementation, re/collision, re/rendering]
---

# PC floor translation prototype

[[EXP-20260904-005 - Raised floor and visible ground pairing]] validates a
six-cell rigid floor lift through original PC instructions and four live game
arms. A fixed visual companion gives a restored-control visible-ground effect.
This extends the [[PC barrier translation prototype]] using existing parsers,
height math and original loading; no movement replacement is introduced.

## Supported operation

`reimplementation/ablpc/terrain_floor_edit.py` exposes:

```python
translate_floor_group(raw, index, group_index, dy) -> bytes
```

`dy` is an integer in stored units (32 world units); negative raises the floor.
Only signed cell h0 at+8 changes for every cell in the selected group. Preserve
normals, edge vectors, relative bounds, directory and unknown bytes. This is a
rigid translation, so recomputing normals or X/Z buckets is unnecessary.

The prototype deliberately supports only kind6 non-template/non-clone sources
with upward floor normals. It rejects invalid types/indices, missing/empty
groups, malformed payloads, origin overflow and world-Y wrap. It returns new
bytes and leaves caller input unchanged even on failure. A source group shared
with neighboring geometry can develop a step; the API does not stitch it.

## Reproduction

Run `.venv/bin/python scripts/terrain-floor-authoring-probe.py` for the fixed
source99/group47640 height/landing/walking report. `--write-terrain` creates the
raised fixture only at a new path under work/copies. It refuses overwrite.

Run `.venv/bin/python scripts/terrain-floor-visual-fixture.py` for the17 selected
vertex fields in primary meshes160/213/280. `--write-level` similarly writes a
new file under work/copies. This fixed companion requires the exact retail
Level01 hash and verifies the exact output hash; it is not a generalized spatial
matcher. The live-tested paired content is retained under
`work/copies/EXP-20260904-005/paired`.

## Validation and limits

Twenty-eight new tests cover synthetic invariants, negative inputs, two retail
terrain files, original landing and leaving-edge behavior, and fixed visual
preservation/reversal.177 combined focused tests pass (exact command in EXP-005).
Live loaded groups and mesh arrays match staged files; stationary actor/camera
values match across the visual changed/restored comparison.

Interior translation and visible-ground causality are established at this site.
The render mesh has extra vertices and different boundaries; surrounding render
triangles blend to unchanged vertices while the collision group has a step.
Arbitrary height deformation, normal/bounds rebuilding, vertical side faces,
shared-edge stitching, prop attachments and other levels are not live-validated.
The next implementation should solve those connected-boundary requirements while
keeping this fixture as a regression baseline. See DEC-230 and [[Project Roadmap]].
(Later, 2026-09-07: PC Blender level authoring compiles whole authored
floors and walls with matched edges instead of extending this rigid API.)

## Failed manual acceptance and separate testbed

The user subsequently reports a fall through EXP-005 when returning across the
patch. Its local height/visual effects do not establish reliable traversal.
[[EXP-20260904-006 - Flat deck and solid block test]] provides `scripts/terrain-deck-probe.py` as a
separate fixed flat deck and solid-block fixture. It does not repair this rigid
translation API’s missing boundary handling.
