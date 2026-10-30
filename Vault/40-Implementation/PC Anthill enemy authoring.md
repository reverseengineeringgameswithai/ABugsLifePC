---
type: implementation
status: implemented
created: 2026-09-08
updated: 2026-10-29
evidence: [EXP-20260908-020]
tags: [implementation/modding, re/actors]
---

# PC Anthill enemy authoring

## Native placement limits

EXP-20260908-020 places five native enemy types: Spider, Mosquito, Pill bug,
Caterpillar and Bee / wasp. The original animated models, behavior scripts and
contact callbacks remain in-game. Translation is supported, not rotation, scale,
mesh deformation or AI/patrol editing. Enemy capacity is53, separate from64
scenery placements; native actor/plant limits still apply. The mosquito uses the
original roaming source4/script4 behavior.

## Original-enemy replacement contract

An authored enemy population owns the entire population of these five types.
The compiler disables all21 original placements before allocating authored
entries. An empty authored population stays empty; original enemies do not
silently return. Seeds, Dot and the FLIKHarv model entry retain their exact
source slots.

## Implementation and evidence

`level_raw.py` bounds-checks and preserves packet metadata; the enemy edit
changes only the mapped creature packet, using pinned PC donors.

[[EXP-20260908-020 - Native enemy placement and scattered Blender population]] cites PC decoder0049A200, loader00465030/0046574D, source00599EB0,
initializer0041C420/0041BD10, VM0041DC60 and model binding00445020. Evidence includes
169 native packet comparisons,0/5/53 native initialization,
6/0 edited builds and exact live10-enemy accounting. Combat and
arbitrary terrain/placement behavior remain bounded by the original engine;
exhaustive gameplay and full-pool plant growth are untested.
