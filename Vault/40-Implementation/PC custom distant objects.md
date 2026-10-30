---
type: implementation
status: implemented
created: 2026-09-11
updated: 2026-10-29
evidence: [EXP-20260911-018]
tags: [implementation/modding, re/rendering]
---

# PC custom distant objects

EXP-20260911-018 adds distant (secondary) copies of placed mesh scenery and
owns the native and hardware evidence. Near meshes, collision and the other
level files remain unchanged. The earlier terrain-only work is in
[[PC custom distant terrain]].

## Shared geometry

Placed mesh objects reuse their complete original mesh streams. Only new
32-byte objects and 20-byte scene records are added. Both translation and scale
are quartered; rotations, animation selector byte 25 and opaque bytes remain.
The original secondary scaled dispatch at 00448D70/00449473 performs the same
native animation/matrix composition. Object byte 24 marks only the new copies.
Each shared geometry pointer is validated against its complete source record
before it is written.

## Transition and depth

Simply sharing scaled geometry leaves a gap: ordinary small objects end before
the terrain-style distant threshold begins. A negative scene bound changes
admission/software clipping but does not solve the hardware polygon threshold;
that rejected probe is retained. The final objects keep positive bounds.

The EXP-20260911-018 build adds a 228-byte guarded helper at 004BC200 that distinguishes terrain argument 10640
from object argument 20640. Both use the EXP017 depth correction, keeping the
distant draw behind nearby geometry. Only the marked object's hardware quad and
triangle thresholds at 0045CF37 and 004608CD change. They begin at two-thirds of
the configured primary range: 6,144 original stored units at the 2x distance
profile. Original arithmetic, flags and registers remain exact for unmarked
calls. Both tested PE bases and the 1x/2x helper profiles pass native tests.

The native comparison covers 61 placed meshes, five distances and two animation
phases (610 cases). Both representations emit in 244 overlap cases; all 22,712
matched UV/RGB vertices are within one screen pixel. All objects emit at 20,000
stored units in these centered cameras. Different projected face-culling results
are retained; this is bounded alignment evidence, not byte-identical GPU output.

## Scope

These are placed mesh scenery and authored terrain decorations. Interactive
actors, pickups, movable seeds, spawned plants and `berry.red`'s camera-facing
sprite groups retain their native paths. A full billboard/actor distant system
is separate work; no disconnected berry leaves or ghost pickups are generated.
All-angle transitions, software/native-Windows rendering, other resolutions and
other original level exporters remain unvalidated.
