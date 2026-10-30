---
type: implementation
status: implemented
updated: 2026-10-29
tags: [implementation/modding, terrain/authoring]
---

# PC reusable scenery mushroom authoring

[[EXP-20260906-014 - Net-new scenery mushroom instances]] supplies a checked
net-new placement path for the beige Anthill scenery mushrooms. It is separate
from [[PC seed and mushroom collision state]] and does not allocate plant actors.

`ablpc.terrain_scenery.mushroom_template` extracts hash-pinned original Level01
mesh/object/collision bytes from private work copies. `append_instances`
returns new DAT and TERRAIN bytes plus an allocation receipt. Each instance has
a new primary record, render object and collision descriptor/payload. Old slots
remain; repeated calls add more. Source/descriptor indices can change with
composition; read them from each fresh receipt. Rotation/scale, materials, render pass/depth,
visibility bound and collision clearance are retained. No game assets are
embedded in source or tests.

`scripts/terrain-scenery-fixture.py` accepts a flat three-file base fixture,
original copied LEVEL01 directory, and a JSON placement list:

```json
[{"variant": "tall", "origin": [6000, -3200, 17000]}]
```

`origin` is the render object's absolute stored-unit position (32 world units
per stored unit), not Flik's live position. `tall` uses scene344/source147;
`small-back` uses396/146. `small-front`342/142 and `small-far`400/148 have
localization/resident-byte evidence but are not exercised by the current new-copy
movement fixture. Supply fresh `--out` under work/copies and `--report` under work.
Outputs are LEVEL.DAT, TERRAIN.ALL and unchanged PLANTTER.ALL, not a launched game.

## Validation and bounds

The initial three-instance fixture preserves the expanded platform, separated
foliage, bound14183, segmented boundary and bouncing-plant repair. Original-PC
relocation and emitted-draw-output gates accompany finite landing, lateral and
grounded push/return tests. The experiment records a floor108-confounded original
side route and its explicit discriminator; do not claim every original-world
route is identical. EXP-20260906-016 then loads six independently verified
instances.42 scenery tests include 0/1/5/6/7-instance rebuilds and the exact
six-instance hashes. No arbitrary binary deletion API is claimed.

Scope limits: original Level01 texture resources, retained donor transforms,
unindexed/fixed-record-free DATs without extra-pointer variants, unique objects,
bounds-checked pointers/counts and explicit experiment capacities. Arbitrary
rotation/scale, automatic collision rebuilding and general level repacking are
not implemented. New large meshes must still follow
[[PC terrain visibility growth checklist]].
