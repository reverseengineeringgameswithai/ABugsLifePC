---
type: implementation
status: bounded
created: 2026-09-07
updated: 2026-10-29
evidence: [EXP-20260907-017, EXP-20260907-022, EXP-20260907-023, EXP-20260908-001, EXP-20260908-012, EXP-20260908-013]
tags: [implementation/modding, re/rendering, terrain/authoring]
---

# Level authoring memory limits

Free host RAM is separate from the old program's chosen addresses and from the
limits enforced inside it. The limits below are native; more host memory cannot
change the stores or relocate the pointers involved.
[[PC Large-Level Engine Roadmap]] lists the related terrain, collision and actor
limits.

## Renderer scratch overlap

**Confirmed:** [[EXP-20260907-017 - Trunk scenery and character storage overlap repair]]
reproduces Flik's polygons overlapping renderer scratch `0076F9A0..0076F9AF`.
Nine native captured-pose replays distinguish overlap from safe storage. Original
PC stores `004063CB`/`0040640C`/`0040644B`/`00406491` and related sites overwrite
geometry at the overlapping address. Additional free host memory cannot change
those stores or relocate existing pointers automatically. Sharing exact prop
meshes removed that overlap without changing object transforms, animation
selectors or collision shells.

A combined LEVEL.DAT/TERRAIN.ALL/PLANTTER.ALL size cap of 1,000,000 bytes was
then used as a conservative guardrail for the pinned resource profile. It is not
a measurement of the game's total RAM use, a general engine maximum, or the
host's available RAM, and EXP-022 below shows it is insufficient as a
storage-safety gate.

## Retained storage overrun

In [[EXP-20260907-022 - Terrain chunk prototype and model stream freeze]] a
four-section test build with unchanged world geometry loads 997,042 bytes and
freezes on shared-entry 37 MOS.ALL geometry crossing `0076F9A0..AF`. The 100-byte
stream matches source offset `0x7E8` except 13 corrupted scratch bytes. Read-only
PC samples and a native offline replay prove the non-advancing invalid-selector
loop. Flik's 436 checked bytes remain exact, which does not certify other models.
The restored EXP-019 reference also places later entry 49 at `0076F99F`; its
usage remains unresolved.

[[EXP-20260907-023 - Dedicated asset arena and terrain chunk acceptance]]
reconstructs an earlier test build's retained layout: 1,406,871 bytes starting
at `0063E998`, exceeding the 1,249,280-byte space before the next known engine
global (`0076F998`) by 157,591 bytes. Its reset root `0076F9B0` was overwritten
as well as the MOS.ALL stream. The three-file 995,276-byte sum omitted 48,927
retained RAW bytes and 380,232 model/animation bytes, and included some
directories that the native loader discards, so a file-size sum never measured
the full retained footprint. `EXP-023/load-layout.json` indexes that
reconstruction. The base is carried by two HIGHLOW operands; original RAW
staging and renderer scratch stay at their old addresses when it is moved.

Native face offsets and signed local coordinates impose separate format bounds.
The native multi-object scene format supports several terrain sections; making
the affected load storage larger requires tracing/revising its allocation and all
dependent pointers and checking renderer buffers.

## Plant pool and collision candidates

[[EXP-20260908-001 - Plant capacity and collision workspace repair]] demonstrates
why host RAM alone does not resolve engine limits. The twentieth native plant
traps the original free-slot scan, and 19 overlapping mushrooms exceed the
400-entry candidate lists and overwrite a terrain descriptor.

## Shared native pool

[[EXP-20260908-012 - High-slot seed interaction and native pool limit]] and
[[EXP-20260908-013 - Seed auxiliary budget and distant carry]] confirm two
allocators sharing 64 records of 56 bytes at `00598CA8`. The native full-pool
scan has no cycle escape. EXP-013 identifies call `0041DA68` as the stalled seed
request; budgeting that call alone is neither pool expansion nor a proven demand
bound for the other callers.

## Terrain storage references

Source 99's 4458-byte trailer must be retained along with the compiler's collision
body. Original `004AB22C` demonstrates why terrain storage cannot be freed solely
because its descriptor was rebound: a cached contact still references the old
allocation (EXP-20260908-003,
[[EXP-20260908-004 - Native terrain page residency]]). Native pin enumeration,
state persistence and real long-traversal memory bounds are open.

## Density and frame work

[[EXP-20260907-026 - Collision-preserving visual density and frame work]]
separates visual detail from collision topology: native rendering work rises
while collision work stays identical. A file-size sum is still not total
retained memory, and stationary pre-pacing samples do not establish
representative worst-case headroom.
[[EXP-20260907-028 - Representative update and render headroom]] measures work
headroom on its routes; that does not expand native indices, candidate arrays or
coordinate arithmetic, and wider extent still requires its own validation.
Present can submit work asynchronously; GPU completion is unmeasured.
