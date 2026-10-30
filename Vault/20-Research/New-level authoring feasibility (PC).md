---
type: research
id: RES-20260818-newlevel-feasibility
date: 2026-08-18
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
status: historical
updated: 2026-10-29
tags:
  - research/assessment
  - re/level-format
  - re/collision
---

# New-level authoring feasibility (PC)

> [!warning] Superseded snapshot (2026-10-02 audit)
> This is the 2026-08-18 assessment, kept as a record. Its "Not today" answer
> and gap list no longer describe the project. Visible ground has a bounded
> causal example ([[EXP-20260904-005 - Raised floor and visible ground pairing]]);
> lateral blocking exists through steep triangles and kind-`0x101` barriers
> ([[EXP-20260904-002 - Retail collision admission and separate XZ barriers]]);
> Blender exports paired render and collision data
> (EXP-20260907-007, PC Blender level authoring);
> and nine generated levels were built and entered in hardware
> (EXP-20260928-001).
> Larger-level limits are owned by [[PC Large-Level Engine Roadmap]]. Open
> limits are tracked in [[Known Unknowns]] (KU-079, KU-080, KU-081).

Standing assessment: **can we author new level layouts (terrain + collision +
geometry) on the PC port, and how far are we?** Synthesised from a 2026-08-18
three-way survey (PC level format, PC collision, PS1 authoring pipeline). The
ultimate project goal is new layouts; terrain/collision is the hardest half.

> [!summary] Bottom line
> **Not today.** We can *edit within* existing levels (byte-exact, engine-accepted),
> reconstruct the bounded type-`0x41` static-mesh payload, and *read* collision
> bit-exactly, but we cannot yet *author new* terrain and collision as a coupled
> level. The immediate linchpin is causal proof that the consumer-linked
> type-`0x41` meshes carry visible ground.

## Current PC decode state

| Subsystem | Decoded? (confirmed) | Writable today? | Evidence |
| --- | --- | --- | --- |
| Object/pickup placement (`LEVEL.DAT`, `type-0x3F`) | Partial — lossless parser | **Yes**, specific fields (positions, type-1 rows, grain/letter tables, dispatch-0x49 retarget); retail exe accepts them | [[PC LEVEL DAT prefix]] `FMT-PC-LEVEL-DAT-PREFIX`; `reimplementation/ablpc/level_dat.py`; `KU-009`/`KU-014`/`KU-023` |
| Terrain collision (`TERRAIN.ALL`) | **Read side solved** — triangulated height-field; engine height math reproduced bit-exactly | **No writer** (read-only parser); material vocab `{0=ground,1=pit}` only | [[PC TERRAIN ALL collision descriptor source]]; `terrain_all.py`, `terrain_height.py`; `EXP-20260816-141`; `KU-061` |
| Visible render mesh / terrain geometry | **Partial** — type-`0x41` payload grammar and exact PC consumer linked; first R2 run valid but causally inconclusive | Reconstructive guarded edits only; no terrain-authoring claim before Gate C | [[PC LEVEL DAT static mesh]]; `EXP-20260818-006`/`007`/`008`; [[EXP-20260819-001 - R2b Anthill static mesh causal runtime]]; `KU-079` |
| `LEVEL.RAW` (actor/creature records) | Mostly opaque (one record type) | No | loader `0x004AE240`, parser `0x00465030`, actor pool `0x0041C420` |
| `LEVEL.BIN` / `*.SPL` / `*.VB`/`*.VH` | Opaque | No | no Vault analysis |

**Collision functions (confirmed behaviour, candidate names, `EXP-20260816-141`):**
loader `0x004A8410`, bounds+spatial-index `0x004A8950`, height collector
`0x004AC460`, resolver `0x004ACA60`, half-plane `0x004A9290`, material/result
reader `0x004ACF90`. Level dispatcher `0x00418780` switches on internal index
`0x00861C84` (17 entries, [[PC level roster and numbering]]).

**Sectioning:** confirmed PC-native — collision uses **32-unit cells** grouped
into runtime **zone buckets** (`0x007F128C`), a two-phase broadphase. This is
"sectioned like PS1" in the grid sense, but built at load from `TERRAIN.ALL`;
there is **no stored PS1-style sector table** in `LEVEL.DAT` beyond its 64-typed
prefix.

## PC vs PS1 — and the "more room" question

PS1 is the answer key: it **did** ship a constrained new level (full-corridor
LEVEL01 replacement, cold-boot + movie validated) via a homegrown Blender→native
pipeline (see [[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]]).
Comparing the two ports:

- **PC advantage (real):** PS1 keeps collision inside the **LZ-compressed**
  `LEVEL.RAW` chunk-32, fighting decompress/recompress and a ~260 KB decompressed
  cap. **PC moved collision into its own uncompressed `TERRAIN.ALL`**, which we
  already model bit-exactly — no compression fight, and PC's per-cell triangulated
  height-field is arguably *more* expressive than PS1's per-sector-flat + 6 swept
  planes. So the "PC has more room / is friendlier" intuition holds **for
  collision specifically** (uncompressed, no VRAM/GTE/CD-sector budget).
- **PC deficit (real):** PS1 had its **visible-floor payload format decoded and
  rewritable** (`FUNC_80010000`) — that is exactly what let it author terrain the
  player can see. On PC that same layer — the render-geometry command grammar — is
  our biggest undecoded gap. **PC is ahead on collision-read, behind on
  drawable-geometry.**
- **Fast64 is a red herring:** the Blender addon was never used on PS1; it was a
  naming analogy for a homegrown workflow. "Use Fast64" does not port. What ports
  is the *strategy* (one mesh, slope-classified, rewrite native structures) and
  *format leads*, not tooling.

## Reframing the intuition

The common assumption "collision is the biggest thing to create a new level" is
**half-right on PC**: collision is the biggest *conceptual* piece, but it is the
*more solved* half here (read model exact, file uncompressed, cell = a plane that
maps naturally from a heightfield). For a **playable, visible** new level the
**render-geometry grammar is the larger obstacle** than collision. For a merely
**walkable** new-collision test, collision-first is feasible sooner.

## Dependency-ordered gaps (what it would take)

1. **Causally verify the type-`0x41` visible-ground candidate** — R0 and R1
   bound its grammar and exact PC consumer. The first authorized R2 run was
   procedurally valid but its control-agreement gate failed before effect
   classification. A stable-camera/in-view successor is required. **Linchpin.**
   (`KU-079`.)
2. **Build a `TERRAIN.ALL` writer** — invert the bit-exact read model + nail the
   last unknown cell fields (`KU-061`) and the material vocabulary. More tractable
   than #1; a natural Blender-heightfield target.
3. **Resolve the collision material/result vocabulary** beyond `{0,1}`.
4. **Settle the wall question** — the collision survey found **only vertical
   height resolution on PC, no lateral wall-blocking path**, whereas PS1 uses swept
   planes for walls. Either PC does walls via steep height-field cells or there is
   an undiscovered mechanism. Must be answered before authoring anything with
   walls. (Tracked as `KU-080`.)
5. **(If new actor spawns needed)** crack the `LEVEL.RAW` record grammar +
   compression contract (`0x00465030`, currently one record type).

## Is a Blender authoring pipeline possible on PC?

Yes — it is the right end-goal shape, and PS1 proves it works. Split the effort:

- **Blender front-end = the easy, port-agnostic part.** Heightfield/mesh authoring,
  slope classification (floor vs wall), spawn/goal empties, coordinate conventions
  — writable anytime; most of the PS1 exporter logic transfers conceptually.
  Blender is **not** the bottleneck.
- **Back-end native encoders = the actual work.** Two of them:
  - **Collision encoder** (Blender heightfield → `TERRAIN.ALL` cells): *tractable*
    and a **good Blender fit**, because a PC collision cell already *is* a plane
    (slope A/B, signed divisor C = winding, base height) that maps directly from a
    triangulated heightfield. Gated only on gap #2/#4 above.
  - **Render-geometry encoder** (Blender mesh → `LEVEL.DAT` draw commands): gated on
    gap #1 (the grammar decode). Until then, authored terrain is walkable but the
    *new* surface is not drawn.

So a realistic staged path: **collision-first Blender exporter** (a walkable, if
not-yet-visible, authored surface) as a motivating milestone, with the
render-geometry decode as the parallel long pole that unlocks visuals.

## Recommendation

Pursue new-level authoring as a **program**, gated on gap #1. R0 and offline R1
have bounded the type-`0x41` static-mesh grammar and linked its exact consumer.
R2a selects a byte-local Anthill Level01 candidate near zero on two
object-translated components, with the earlier Level03 candidate retained as
fallback. The first A1/B/A2 run was valid but causally inconclusive. The
highest-leverage next move is the frozen
[[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]:
first an authorized retail-only execution-freeze calibration, then a separate
guarded face-topology control/localizer/control test. The localizer must be
accepted before a one-byte vertex successor. This remains the R2 / Gate C
linchpin, not a reason to widen the editor.
In parallel, the **collision writer + wall question** is a
lower-risk track that yields a walkable Blender→`TERRAIN.ALL` exporter and de-risks
the collision half. Both are ordinary (if large) RE, not unknowns-in-principle —
PS1 closed the equivalent gaps.

**Experiment #1 is scoped:** [[EXP-20260818-005 - Decode the render-geometry command grammar (scope)]]
(tracked as `KU-079`) defines the go/no-go gates and names the confirmed static
anchors — the tri/quad emit twin `FUN_00405fe0`/`FUN_00407450` (via thunks
`0x00401d66`/`0x00401ccb`), the load-path anchors.
Gate A is complete: geometry emission is a **type-switch on a per-instance type
field** feeding per-type drawers that call the emit primitives **directly** through
thunks — *not* an opcode function-pointer table (an early recon claim, since
refuted). Gate B established the container grammar by instruction evidence (the retail-data
chain pins only the 12-byte anchor stride); the
semantics of the nine vertex `int16` and the world scale remain open. The first
Gate C run failed its control-agreement acceptance gate before effect
classification, so Gate C remains open.

## Confirmed vs inferred

- **Confirmed (PC):** the decode-state table's "read side solved / editable
  fields" rows, the collision function identities' *behaviour* (`EXP-20260816-141`
  receipts), grid/zone sectioning, the render-geometry gap.
- **Inferred:** collision function *names* (high-confidence candidates); the
  "no lateral wall collision" conclusion (absence-of-evidence from a function
  survey, not a proof); all cross-port leads (PS1-only until PC-confirmed).

## Links

- [[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]],
  [[PC TERRAIN ALL collision descriptor source]], [[PC LEVEL DAT prefix]],
  [[PC level roster and numbering]], [[Cross-Port Evidence Policy]].
