---
type: roadmap
status: active
created: 2026-09-07
updated: 2026-10-29
tags: [implementation/modding, terrain/authoring, system/roadmap]
---

# PC Large-Level Engine Roadmap

This note records the native PC limits that a larger or denser level runs into:
terrain sections and mesh encoding, retained-asset storage, collision candidate
and plant capacity, actor contacts and the shared auxiliary pool. They were
measured on 2026-09-07..08 while testing larger levels. Each is a modification
requirement: a change that enlarges a level must stay inside it or change the
code that enforces it. [[Project Roadmap]] is the project-wide index;
[[PC level authoring memory limits]] holds the storage measurements and
[[PC terrain streaming ownership ledger]] the reference map.

## Terrain sections and mesh encoding

- **Several terrain objects are admitted.** The native scene format accepts
  independent terrain objects, each with its own origin, visibility bounds and
  paired collision source. Whole faces split between sections keep geometry,
  UVs, colours, collision, props, roots and exit behaviour. Evidence: 124 native floor
  crossings, 24 wall pushes, 12 renderer contexts and all four sections resident
  in [[EXP-20260907-022 - Terrain chunk prototype and model stream freeze]] and
  [[EXP-20260907-023 - Dedicated asset arena and terrain chunk acceptance]].
  Splitting does not lift total geometry or coordinate limits; it is not
  unlimited world size.
- **Per-mesh vertex limit.** Positive-count faces carry unsigned 16-bit byte
  offsets into 12-byte vertex rows (consumer `0045A7F0`), so one mesh can
  reference at most 5462 vertices
  ([[EXP-20260907-025 - Native density limits and terrain refinement trial]]).
  The tested profile kept 5462 vertices/8192 faces/4096 collision cells per
  section with the signed-coordinate and 1 MiB per-file checks. Only the vertex
  bound is derived from the native encoding; these are rejection limits, not a
  certified content maximum.
- **Collision retessellation changes behaviour.**
  [[EXP-20260907-026 - Collision-preserving visual density and frame work]]
  identifies support loss across added slope collision edges. Refining only the
  visual mesh after collision construction leaves all 286 native routes identical
  in position, contact, flags and instruction counts, and twelve renderer
  contexts stay within checked native buffer/index bounds.

## Retained-asset storage

The native load cursor base `0063E998` is carried by exactly two HIGHLOW
operands (`004634EA`, `004672E5`). The space from that base to the next known
engine global at `0076F998` is 1,249,280 bytes. RAW staging still ends at
`0076F998`, which scalar engine state also uses, so it must not be
indiscriminately relocated. A four-section test load of 997,042 bytes froze when
shared-entry 37 MOS.ALL geometry crossed renderer scratch `0076F9A0..AF`
(EXP-022). Moving the retained-data base to a separate read/write section in
EXP-023 preserved both relocations; native RAW/DAT/ALL/ANM loading then built
dependent pointers normally, with RAW staging and renderer scratch at their old
addresses. That check covers two offline image bases, 35 native file loads, 170
model-entry comparisons and three hardware arms. It is finite capacity, not
general heap safety for arbitrary content.

## Collision candidates, plants and frame work

`004AB1A0` and `004ABE00` append triangle pointers at `007F3F50` without a
400-entry check (EXP-025).
[[EXP-20260908-001 - Plant capacity and collision workspace repair]] reproduces
offline the original twentieth-plant infinite free-slot scan and the index-400
descriptor overwrite when overlapping native mushrooms exceed the 400-entry
lists. A static allowance alone did not establish dynamic safety; arbitrary
dynamic actors remain unproved.

The earlier millisecond timer covers render/present only; gameplay update runs
before its timestamp
([[EXP-20260907-028 - Representative update and render headroom]]). Native
instruction counts and paced frame intervals must not be relabelled as GPU
timing. [[EXP-20260907-027 - Native respawn cycles and exit-aware traversal]]
verifies six native reset cycles and a deliberate exit/re-entry with exact
resident model checks; damage-fixture boundary safety remains unproved, and one
initial instant-death fixture reached GameOver and is rejected.

## Actor contacts and the shared pool

- **Contact records and cached pages.** `004A9078–004A908D` initialize 24
  twenty-byte contact records from `007F3D68`; record +4 caches the cell pointer
  used by `004AB1A0` and its solvers
  ([[EXP-20260908-004 - Native terrain page residency]]). The original x86
  movement path faults at `004AB22C` if a descriptor is rebound and its
  still-referenced old page is unmapped (EXP-20260908-003). A natural contact
  transition permits retirement in one bounded native arm. No comprehensive
  pointer-lifetime proof exists.
- **Actor selectors.** Original `0041C420` assigns selectors without a contact
  table bound: assignment 16 aliases camera slot 16 and assignment 24 is outside
  the initialized table
  ([[EXP-20260908-005 - Compact terrain storage and actor selector limits]]).
  Four solver comparisons (`004A9F44`, `004AA027`, `004AA862`, `004AA983`)
  recognize the camera record; blindly relocating the table would retain the
  wrong camera behaviour
  ([[EXP-20260908-006 - Native actor and camera contact repair]]).
- **Shared 64-record pool.** The allocator search at `0042AA50` cycles through
  64 records at `00598CA8` and has no full-cycle termination branch
  ([[EXP-20260908-012 - High-slot seed interaction and native pool limit]]).
  [[EXP-20260908-013 - Seed auxiliary budget and distant carry]] identifies call
  `0041DA68` inside seed update `0041D5B0` as the stalled request. The other
  native callers can still reach the full-pool cycle; do not return null to
  unchecked consumers. Trigger attribution remains open because an unpatched
  positive-offset control also completes.
- **Seed hazards.** [[EXP-20260908-016 - Manual seed ownership and native scattering]]
  replays original `00415E30` writing slot 63 XYZ when mode bit 0x80 at
  `0059D9A0` is set (all twenty live `.data` captures have it clear), and
  original `0041D390` adding opposite -256/+256 X velocity per call to two
  crowded seeds without moving them. No live actor retirement or burst fix is claimed.

## Open requirements

- Complete query/callback/heap/global/driver/register-stack/trailer reference
  coverage before freeing any terrain storage. Inactivity or entity
  initialization alone is not a release rule.
- Establish shared-pool caller/owner lifetimes and a tested capacity policy
  before raising population.
- Validate wider coordinate arithmetic/rebasing and native descriptor/scene
  limits before increasing world extent.

Host free RAM does not change native arrays, arithmetic or per-frame work.
Earlier failures and finite passes stay in their experiment notes.
