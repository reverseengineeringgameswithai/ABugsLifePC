---
type: session
date: 2026-08-18
agent: Claude
status: complete
tags:
  - session
  - re/static
  - re/level-format
  - re/collision
---

# Berry confirmation and new-level authoring Gate A/B

## Agent

Claude.

## Goal

Two user-directed threads: (1) bank the PC confirmation of the berry-type
selector; (2) answer "can we solve terrain/collision well enough to author new
levels?", then execute the first experiment toward it.

## What happened

1. **KU-073 confirmed on PC** ([[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]]).
   Four user-authorized guarded pokes to `0x0059D9A7` under `play-pristine`
   changed the thrown berry (user-observed): `1` blue/super, `2` green/homing,
   `3` gold, `4` purple/mega; `0` red default. Source, not mirror. Reverted.
2. **Feasibility assessment** ([[New-level authoring feasibility (PC)]]) from a
   three-way survey, plus the PS1 pipeline and transferable leads
   ([[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]]).
   Verdict: cannot author levels today; the linchpin is the render-geometry
   grammar. Durable pickup plan:
   [[New-level authoring roadmap (terrain, collision, materials)]].
3. **Gate A + Gate B** ([[EXP-20260818-005 - Decode the render-geometry command grammar (scope)]],
   `KU-079`). Located the walker chain and type-switch dispatch; resolved a
   vertex-packing contradiction at instruction level; decoded the 44-byte record;
   tested the container grammar against retail `LEVEL01/LEVEL.DAT`.
4. **Four independent James audit rounds — REJECT ×3, then ACCEPT.** Round 1 caught a
   false universal ("collision table referenced only by the collision family"),
   a malformed KU insertion, a misattributed `<<5`, and a wrong post-mortem cause.
   Round 2 refuted the headline evidential claim by counterexample (below). Round 3
   corrected the claim's magnitude (zero discrimination, not five-way), a
   non-reproducing statistic, and surfaced the billboard evidence. Round 4
   **ACCEPTED**, having re-derived every data claim independently.

## Key results

- **Render/collision are NOT provably decoupled.** `FUN_0044ca00` reads *and
  writes* the collision descriptor table `0x007F4590` and is reached from the
  **render** scene driver `FUN_0044d430` → filed as `KU-081`; the
  one-mesh/two-encoder design is now gated on resolving it.
- **The 7/7 payload chain is real but NOT conclusive.** All 193 groups have
  `prim_count == 1`, so the chain gives zero discrimination on the split (every
  `skip + rec = 44` chains). It pins only the 12-byte anchor stride; the 44-byte
  record rests on instruction evidence.
- **Type-3 is almost certainly not the terrain path.** 20 of 21 corpus files have
  zero type-3 records; `LEVEL01`'s are tall thin quads (≈5.2:1) drawn by an
  explicit billboard path (per-instance rotation from a camera-related global,
  per-group translation only, objects at Euler `(0,0,0)`). 16 of 21 files have no
  type-2/3/0xa at all, so ground likely is not in the instance array. What draws visible ground is still unidentified.

## Decisions

- Record contradictions rather than resolving them by plausibility (applied twice:
  the vertex-packing overlap, and the sliding-window vs corner-pairs reading).
- Gate C (causal, user in-game) remains **unrun**; no geometry claim is treated as
  confirmed without it.

## Next

**R0 is done** ([[EXP-20260818-006 - R0 the static mesh format and where visible ground lives]]):
the static indexed mesh format is decoded and validated 2,543/2,543 (100.00%) over
146,030 face indices on the retail corpus, and large flat instances of it are the
**candidate** ground (no runtime evidence). It also surfaced `KU-082`, a working
copy with unrelocated object pointers. Next is **Gate C on
that format**. *(Superseded R0 brief:)* identify what actually draws visible ground — `FUN_00454b70`
(type-2/`0xa`) is only a weak candidate, since 16 of 21 corpus files contain no
type-2/3/0xa record at all, so ground likely is not in the `LEVEL.DAT` instance
array. Only then the Gate C discriminator (poke one vertex short, observe which
corner moves). See the roadmap's immediate-next-action block.
