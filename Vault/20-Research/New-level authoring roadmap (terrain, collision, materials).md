---
type: plan
id: PLAN-20260818-newlevel
date: 2026-08-18
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
status: historical
updated: 2026-10-29
tags:
  - plan/roadmap
  - re/level-format
  - re/collision
---

# New-level authoring roadmap (terrain, collision, materials)

> [!warning] No longer the active plan (2026-10-02 audit)
> The dated entries below run to 2026-09-06 and are kept as records. Their
> "current", "next" and "IMMEDIATE NEXT ACTION" instructions are historical.
> Larger levels moved to [[PC Large-Level Engine Roadmap]].
> The R2q screenshot track behind Track R was dropped by the user on 2026-09-27
> as too slow ([[Project Roadmap]]); do not resume it from this note.
> Current work is chosen in [[Current State]].

## Opened-plant collision gate (2026-09-06)

EXP-20260906-007 now resolves the observed mushroom: type5 / PLANTTER record8, separate seed collider, bounds-checked two-byte restoration, original-PC seed/opening/lateral/landing/bounce/return tests and normal-input live confirmation. Keep isolated terrain, other emptied plant templates/high0x104 and the failing EXP-006 control unchanged. General plant-isolation policy and other plant types remain open; do not call the entire platform plant-complete. [[PC seed and mushroom collision state]] and [[2026-09-06 - Codex - Mushroom collision restoration and varied grass]].

## 2026-09-05 terrain priority update

[[EXP-20260905-003 - Shared floor return discriminator and stitched patch]] now
reproduces EXP-005's return fall offline and live and demonstrates a bounded
connected six-cell repair with paired render heights. This supersedes prior
instructions to start by reproducing that return. Next compare a normal-input
route around unchanged props across source99/source100, then broaden finite
velocity/pose coverage. The 16/16 isolated model result is not 16/16 complete-scene
or live coverage: retail/stitched are 13/16 complete-scene and the extra live seam
route was blocked. Keep rigid EXP-005, flat EXP-006 and banked box fixtures intact.


**Pickup note for another agent.** The factual, dependency-ordered program to get
from where we are now to authoring good-looking, walkable new levels. Companion to
the analytical assessment [[New-level authoring feasibility (PC)]]; this note is
the *plan*. Read that + this + the linked dossiers and you can start cold.

## Goal
Author new level layouts (visible terrain + collision + materials) for the PC
port. Ultimate delivery shape: a Blender→native pipeline (PS1 proved this works,
[[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]]).

## Current priority — 2026-09-04

Proceed with offline Track C independently of unfinished R2q screenshot
calibration. [[EXP-20260904-001 - Original PC lateral collision and descriptor-store probes]]
demonstrates player-connected lateral response in original instructions and
bounds the render-side direct descriptor stores to N..N+19.
[[EXP-20260904-002 - Retail collision admission and separate XZ barriers]]
completes real candidate admission: a Level01 steep triangle and a separate
kind`0x101` X/Z barrier each cause original movement response under controls.
Level01/Level03 loading resolves actual plant templates and reserved indices.
[[EXP-20260904-003 - Barrier grammar and landing-seeded grounded movement]]
now completes that grammar/grounded step with a bounded reader and original
landing-seeded controls. The first authored fixture now has live proof in
[[EXP-20260904-004 - Translated barrier live collision proof]]: exact loaded
barrier relocation and a restored-file walking control. DEC-229 is now complete
in [[EXP-20260904-005 - Raised floor and visible ground pairing]]: raised floor movement and a
fixed visible-ground companion have live changed/restored controls. Next is
connected boundary handling for a small ramp (DEC-230). This narrows KU-079 with
one visible-ground causal example; general authoring gates remain open.
The R2q-032 source/activation bank stays intact, without final clean-tree
acceptance or new R2q runtime authority. Canonical sequencing:
[[Project Roadmap]], DEC-226/227/228/229/230.

## Manual failure and clearer fixture — 2026-09-04

The user reports EXP-005 fails return traversal and its shallow lift is visually
confounded by the native slope. Keep its coordinate/pixel evidence scoped.
[[EXP-20260904-006 - Flat deck and solid block test]] supplies a flat deck and solid block,
with original negative controls and two live jump-off-return cycles. DEC-231
banks it as a clearer testbed; shared-edge repair and general grouping remain open.

## New solid geometry needs explicit object settings — 2026-09-04

[[EXP-20260904-008 - Block depth offset runtime comparison]] confirms that copying primary160's
object byte+0x12=8 into the new block caused Flik's lower legs/shadow to draw
through it. Removal to0 hides the leak; restoration brings it back with matching
player/contact/camera state. Use the corrected fixture and failing control as
an occlusion regression, and choose depth/distance settings explicitly for new
solids. Keep native retail fields intact unless their own change is validated.
Subdivision was not required for this correction and changed textured pixels;
large-face clipping/material rules still need their own bounded evidence.

The user then reports residual leg fragments during side movement.
[[EXP-20260904-009 - Paused side-view depth interpolation]] preserves that
paused view and finds large-face depth errors in original renderer output.
Subdivision improves the offline comparison; some boundary samples remain
uncertain. The user-authorized [[EXP-20260904-010 - Paused subdivision live comparison]]
then removes all255 prior inversion-point fragments and restores them with the
original mesh. DEC-235 retains that regression and requires remaining edge/view
checks before general layout work. At EXP-010 close, the user game had its
original mesh restored; the later banking audit is clean. Neither correction establishes a universal mesh-sizing rule, and
EXP-005's return-floor failure remains separate.

[[EXP-20260904-011 - Box top diagonal edge discriminator]] then keeps the
finer vertices/faces and rotates top corners to use the opposite diagonals.
[[EXP-20260905-001 - Box top diagonal live comparison]] confirms the six
remaining fragments disappear and return with the control, retaining all 255
earlier fixes. All 15 captures match state; both control ROIs restore exactly.
The original mesh was restored at comparison close. DEC-238 put oscillating
movement and other-view acceptance next; EXP-002 below completes that bounded
step before the separate floor-return repair. This selected view supplies no
universal subdivision/diagonal rule.

[[EXP-20260905-002 - Box movement and occluding-view validation]] completes
that next step at a finite scope: five valid reversal sweeps, 518 grounded
state samples and 107 frames, plus jump/top/step-off contact. A new paused
occluding-edge diagnostic demonstrates no reconstructed top-depth inversion.
Keep the rejected original-location south route and placement-specific retry
explicit. DEC-239 advances to EXP-005's shared-floor return defect while
retaining all-view/general-authoring limits. Both scientific games closed; the
original paused user failure was preserved through those experiments. The later
banking audit is clean and cannot attribute the intervening closure.

## Confirmed foundation (do not re-derive)
- **Render and collision are separate DATASETS, co-registered in one world grid**
  — but **NOT proven free of runtime linkage** (corrected 2026-08-18 after an
  independent audit refuted the stronger claim).
  - *Confirmed, scoped:* the render instance-array pointer `0x005ba7e0` is
    referenced only by relocator `0x0044bb70` and scene driver `0x0044d430`;
    `FUN_00453ff0` (render) names zero terrain addresses and `FUN_004AC460`
    (collision height query) names zero render addresses. Collision source is its
    own uncompressed file (`TERRAIN.ALL`), render geometry lives in `LEVEL.DAT`.
  - *Refuted:* "the collision descriptor table `0x007F4590` is referenced only by
    the collision family." **`FUN_0044ca00` reads and writes `0x007F4590`**
    (`(&DAT_007f4590)[iVar4 * 0xc] = iVar7`) and is reached from the **render**
    scene driver `FUN_0044d430`. See `KU-081`.
  - **Consequence for the design:** the one-mesh → TWO-independent-encoders plan
    is still the working shape, but its "no hidden linkage" premise is **not
    established**. `KU-081` must be resolved (likely dynamic/instanced collision
    for moving objects, which would leave the plan intact for *static* terrain)
    **before** the encoder design is committed to.
- **Render pipeline mapped (Gate A, static):** `FUN_0044d430` → `FUN_004498f0`
  (type-switch on `instance+0xe & 0xbfef`) → `FUN_00453ff0` (type-3/0x43
  quad batch — a billboard path, *not* a grid) → `thunk_FUN_00405fe0`. Type-3 payload = count-prefixed nested vertex
  array in `LEVEL.DAT` (`0x005ba240`); record = 44 B (nine vertex `int16`, four
  16-bit UV/attr words, four `u32` per-vertex colours, 5-bit material at record
  byte `0x12`). **Container grammar established** (Gate B: instruction evidence,
  plus a retail-data chain that pins the anchor stride); vertex-short semantics,
  world scale, and *which type draws visible ground* all still open. See [[EXP-20260818-005 - Decode the render-geometry command grammar (scope)]], `KU-079`.
- **Collision height-query subset implemented:** `TERRAIN.ALL` parsed + height math
  reproduced for the audited scope (`terrain_height.py`, `EXP-20260816-141`).
  Movement response is a distinct branch, now probed but not reimplemented.
  **No floor/mesh writer.** A size-preserving barrier translation prototype
  now exists with one live-tested fixture (EXP-004).
  See [[PC TERRAIN ALL collision descriptor source]] and
  [[PC barrier translation prototype]].
- **What exists as tools:** `reimplementation/ablpc/level_dat.py` (lossless
  `LEVEL.DAT` parse + edit of *specific existing fields*, with relocation for some
  record types); `terrain_all.py`/`terrain_height.py` (read-only).

## Three tracks that converge in Blender

### Track R — draw new terrain (render geometry) — the critical-path spine
- **R1 · Gate B decode [RE] — DONE offline**
  ([[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]]).
  The authoring target is the type-`0x41` static indexed mesh found by R0, not
  type-3. The exact `instance → object+0x14 → FUN_0045a7f0` consumer is closed at
  instruction level; all 2,543 retail payloads reconstruct byte-for-byte; and
  the tag is structurally split into face-arity bit 0, low-five branch selector,
  bits 5-6, and upper-byte low-five table index. The parser preserves all
  still-unknown fields and rejects invalid counts/references. **Still unknown:**
  whether a selected mesh is visible ground, world/screen scale, colour/UV
  meanings, and tag-field semantics.
- **R2 · Gate C causal proof [runtime]** — open. The first authorized Anthill
  A1/B/A2 run was procedurally valid but causally inconclusive because only
  `108 / 307200` control pixels passed the frozen stability rule; see
  [[EXP-20260819-001 - R2b Anthill static mesh causal runtime]]. A successor
  must establish control agreement and prove the edited face is in view.
  **Gate on render causal closure and live authoring acceptance**, not on
  independent offline collision analysis.
- **R3 · Geometry writer [engineering — hardest]** — extend `level_dat.py` to
  insert/resize static-mesh vertices/faces and their instances, solving the relocation chain
  (`FUN_0044bb70` baked `+buffer-base` offsets, typed prefix table `0x005c5860`,
  instance array `0x005ba7e0`). *Accept:* add a new quad to a real level; cold-boots
  and renders; synthetic-fixture regression tests.
- **R4 · Packaging [engineering]** — repack `CD/LEVELxx/` so the retail game
  loads it; confirm any size/checksum gate (PS1 had a hard CD-sector cap; expect a
  PC analogue).

### Track C — make it walkable (collision) — parallelizable
- **C1 · Finish the cell grammar [RE]** — close `KU-061` (Z-bounds), the unknown
  cell fields, material vocabulary beyond `{0=ground,1=pit}`.
- **C2 · The wall question [RE/runtime]** — original instructions demonstrate
  real Level01 steep-triangle and kind`0x101` barrier response from both
  nongrounded and original-landing grounded entry (EXP-20260904-002/003).
  Canonical barrier metadata and the 16-pair cap are decoded. EXP-004 adds
  live acceptance of one translated barrier with a restored-file control.
  Broader contact/overflow and other authoring cases remain open under KU-080;
  do not repeat the completed grammar, grounded or translation fixtures.
- **C3 · `TERRAIN.ALL` writer [engineering]** — invert the bit-exact read model:
  heightfield → cells/groups/directory. *Accept:* author raised terrain; engine
  loads it and the height query returns the new heights (predicted by
  `terrain_height.py`, confirmed by a runtime read).
- **C4 · Causal proof [runtime]** — walk the authored surface; player Y follows the
  hill.

### Track M — make it good-looking (materials/texture) — "good looking" lives here
- **M1 · Decode the material/texture system [RE]** — 5-bit index →
  `DAT_005836a4` / `PTR_DAT_004c4108` → texture-pages/CLUTs; locate texture assets.
- **M2 · Reuse the game's own textures [RE + creative]** — map new geometry onto
  existing in-level textures (PS1's "harvested material") + vertex colour/UV for
  shading. *New-texture import (VRAM/atlas) is deferred — harder, separate.*

### Convergence — Blender pipeline (cheap once encoders exist)
- **P1 front-end [easy]** one mesh, slope-classify floor/wall, assign materials,
  spawn/goal empties. **P2 exporter** Blender → `LEVEL.DAT` geometry+instances
  (R3/R4) + `TERRAIN.ALL` cells (C3) + materials (M1/M2), co-registered in world
  space (collision uses 32-unit cells; the render-side scale is not yet established). **P3** boot + validate (cold-boot, walkable, native look), within size caps.

## Critical path, parallelism, risks
- **Spine:** R1 → R2 → R3 → R4 ("can we draw a new surface at all").
- **Independent offline work now:** Track C candidate admission and template
  mapping; bounded Track M analysis may also proceed without R2. Live causal
  acceptance remains necessary for each authored/rendered/walkable claim.
- **Biggest risks:** the relocation chain (R3); the wall question (C2); whether
  texture *reuse* suffices before texture *import* (M2); packaging/size caps (R4).
- **Discipline:** a claim counts only once its causal gate (R2/C4) passes.
- **Effort:** a multi-session program; all ordinary RE + engineering — PS1 closed
  every equivalent, so nothing is unknown-in-principle.

## >>> IMMEDIATE NEXT ACTION (start here) <<<
*Historical (see the banner at the top); not a current instruction.*

**Current action is the offline Track C discriminator above.** The render
history below is preserved for resuming its separate evidence gate.

**R0 and offline R1 are DONE.** R0
([[EXP-20260818-006 - R0 the static mesh format and where visible ground lives]])
found the type-`0x41` candidate; R1
([[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]])
closed its PC consumer, added a bounds-checked reconstructive parser, and selected
one exact guarded Level03 fallback. R2a
([[EXP-20260818-008 - R2a Anthill static mesh causal candidate]]) selects the
primary Anthill test: Level01 primary record 81, face 8, vertex 25, with one
guarded byte and one-face connectivity. The
**static mesh format is decoded and validated 2,543/2,543 (100.00%)** over
146,030 face indices on the **retail** corpus (17 of 21 files contain the type) — `int32 vertex_count` + 12-byte vertices (three offset-named `int16` components + pad + three colour-plausible
bytes *named by position, not proven* + flag) + `u16 tag` + `u16 face_count` + indexed faces (tag bit 0 = tri 12 B / quad
16 B) whose indices are vertex **byte** offsets. Large flat instances of this type
(reached from type-`0x41` instances) are the **candidate visible ground** —
circumstantially strong, **not** runtime-confirmed. Use the **retail** corpus for
format work: one file in `M3-training-51-grains/` has unrelocated pointers
(`KU-082`).

**NEXT: R2 / Gate C on THIS format** (not type-3) — authorization for Stage 1
of [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
is on record. F0-001 and F0-002 were software-renderer setup rejections before
F0; no carousel/title input, signal, process-memory read, or DAT write occurred.
Historical state before the auto-hardware pivot: F0 was unrun and the
localizer was uncreated. The retail RC0/RC1
chooser branch below is preserved history but is superseded by the
user-directed auto-hardware pivot. The then-frozen instruction was to run only the committed argument-free
F0 auto-hardware script: stage exact retail assets, execute canonical
cache hash `1e1d5099...a9c41f`, require all six Direct3D markers, send exactly
`Right`, `Return`, `Return`, then perform the evidence-backed
Level01/title gates. The only authorized process-memory reads are
`(0x00861c84, 4)` before title Return and stopped view blocks
`(0x005b58e0, 18)` plus `(0x005bdb8c, 12)`. The stop/resume is bound to the
verified process with a `pidfd`, and owned-window focus must remain continuous.
`F0-AH-001` is a retained pre-input rejection caused by querying the main game
window once before it was ready; its identities are consumed. The fresh
`F0-AH-002` is a second retained pre-input rejection: its gate counted two
same-PID Wine windows before filtering main-window identity. The fresh
`F0-AH-003` is a third retained pre-input rejection whose 485 polls prove the
valid LevelSelect main XID is titled `Loading - A Bugs Life`, not `Bugs`, with a
1x1 IME helper. `F0-AH-004` then proved the retained-XID inputs but rejected
with index `0` while its log remained Level00/LevelSelect, so it is a consumed
navigation-readiness failure. `F0-AH-005` reached the genuine Level One title
after exact Level01/ClearLoadScreen markers, but correctly rejected before the
index read because ordinary animation produced a new whole-frame hash. Its
cleanup is accepted and its identities are consumed. The fresh
`F0-auto-hardware-retail-006` / `F0-AH-006` packet retained full-frame hashes as
evidence only. It requires exact `640x480` decoded RGB plus both title regions
reproduced across the reviewed A1/B, A2, and `-005` frames:
`360x150+275+120` -> `da63e765...1eddb3`, and `590x70+25+285` ->
`0ae2bd62...48efe`. Either crop mismatch stops before the single authorized
level-index read, title Return, signal, or stopped reads.
That run then completed the `t0 + 3.300 s` exact-PID freeze but rejected because
its identical stopped frame `05f5691c...506ad1c` / `2ea65643...23b9d26c`
differed from the retail R2b phase reference in animated entities. Four exact
camera/terrain regions match all three retail frame-14 inputs and all three
`-006` captures. `F0-AH-007` then rejected before `SIGSTOP`: final identity
completed with `4.346 ms` remaining, and the subsequent full XID guard consumed
most of that budget before geometry launched with a `0.255 ms` timeout. Its 70
post-`t0` focus iterations were not durably aggregated. It produced no stopped
frame and does not trigger the second-identity stop rule. `F0-AH-008` then
rejected during runtime-identity discovery before the renderer gate or any
runtime action. Its old receipts do not preserve the compared candidates, so
the exact changed field is unknown; it remains an unclassified pre-action
tooling rejection under `evidence/pending/`. The fresh
`F0-auto-hardware-retail-009` / `F0-AH-009` requires two consecutive identical
exact-final process observations and persists every candidate plus field-level
diff before input. It preserves the 60 ms final-guard reserve, 3 ms pidfd signal
reserve, unchanged regions, and exact derived-frame reproduction. Another
whole-frame variant stops hash extension and requires a state predicate/mask.
`F0-AH-009` passed with three exact derived-reference frames, stable authorized
view blocks, all structural regions, and clean resume/cleanup/restoration. Its
committed result is James-accepted. NEXT: commit and obtain James acceptance of
the argument-free exact creator plus dedicated C1/L/C2 executor and provenance-
bound derived-control comparator. Then create the already-authorized guarded
face-8 localizer and run C1/L/C2. F0 alone makes no causal, ground, retail-
behavior, or R2-closure claim.
The resulting claim is scoped to that derived PC build; a later controlled
retail intervention remains mandatory for retail R2 closure. Map the exact
full-disc stage at
`work/wine/baseline/dosdevices/r:`, not `$HOME/.wine/dosdevices/r:`, and require
the frozen `CD.TXT` sentinel plus exact `App run from R:\PC\BUGS` and
`R:\PC\BUGS\cd\cd.txt` log identities before any renderer input.
`No CD-ROM found` alone is nondiscriminating. RC0-F0-003 proved the wrong-prefix failure
signature through `App run from .`, the drive-less `\cd\cd.txt` fallback, and
the fatal missing-file/CD prompt; it sent no input and did not consume RC0.
RC0-F0-004 passed the installed-layout gate but an interactive root capture waited
until chooser timeout selected software; it also sent no input and did not
consume RC0. For the next fresh RC0, wait past the `177x63` transient setup
window, resolve the current `SELECTOR_WINDOW`, require that exact window to be
the same-PID `640x480` `Bugs` chooser. RC0-F0-005 then disproved the X11-root
backend: its live frame and both `capture-fixture-002` frames are the same
uniform black PNG, not game pixels; no experiment input was sent and RC0 is
still unconsumed. RC0-F0-006 then stopped before Return: two startup/fade
captures preceded the already-known stable chooser, so neither transition
hash was allowlisted. It sent no direction/Return, signal, read, or DAT write
and cleaned to a clear audit with retail `R:` restored. The historical
RC0 executor, `RC0-F0-retail-007`, and
`evidence/pending/RC0-F0-007` pickup must not be launched. It had restored
asynchronous `gamescopectl screenshot`, waits for file stability, rejects
black/wrong-size/unstable/unknown images, first enforces a fixed `4.000 s`
guarded no-input settle, and keeps all three captures and Return inside one
absolute `45.000 s` launch-to-Return deadline. Each capture command receipt and
image observation is retained before the triplet verdict. It sends no
direction before Return and classifies only complete terminal renderer logs.
The executor accepts no
path overrides, requires baseline `R:` initially retail, bounds the compositor
subprocess, uses the direct guarded XTEST Return sequence, rehashes immediately
before input, and revalidates exact live identity/window/mapping/hashes before
hardware handoff. Create no
localizer until the F0 result is committed and
James-accepted. Only then may fresh C1/localizer/C2 arms test the guarded
three-byte face-collapse localizer. Commit and obtain James acceptance of the
localizer result/evidence packet before preparing another one-byte candidate
packet; never commit the derived DAT. Preserve every
retail-executable, hardware-renderer, level, audit, PID, view-state, and identity
gate. Keep EXP-007 Level03 as fallback, not the primary arm.
The code-to-data consumer link and structural tag split are already closed;
semantic tag/material/UV decoding remains after the causal surface identity.

*(superseded R0 brief, kept for context)* **R0 — find what actually draws visible ground.**
Gate A/B decoded the type-3 path, then established it is almost certainly the
**wrong target for terrain**: type-3 is a camera-facing billboard batch
(`KU-079`), 20 of 21 corpus files contain no type-3 records, and **16 of 21
contain no type-2/3/0xa either** — so visible ground probably is not drawn from the
`LEVEL.DAT` instance array at all. Concrete start: take a level with plainly
visible ground and no type-2/3/0xa instances (e.g. `LEVEL03`), and trace what
submits its ground geometry — candidates include the other `FUN_004498f0` drawers
(`FUN_0045a7f0`, `FUN_00454b70`), the `TERRAIN.ALL` runtime descriptors (does
anything *render* from them?), `LEVEL.RAW`, and the software display-list path.
Identify the drawer + its payload before decoding another record format.

The superseded R0 brief below is retained only as history. The first Gate C run
is complete but did not pass its causal acceptance path: the control-agreement
gate failed before effect classification. Gate C and R2 remain open; no
visible-ground claim counts as confirmed until R2 passes.

## Links
- [[New-level authoring feasibility (PC)]] (assessment/where-we-stand),
  [[EXP-20260818-005 - Decode the render-geometry command grammar (scope)]] (Gate A
  results + Gate B/C plan), `KU-079`,
  [[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]],
  [[PC TERRAIN ALL collision descriptor source]], [[PC LEVEL DAT prefix]],
  [[Project Roadmap]].

## R2c localizer outcome - 2026-08-19

The completed derived-build localizer in
[[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]] is a
valid but causally inconclusive run. Exact C1/C2 controls bracketed L and all
view/lifecycle gates passed, but the L/control XOR contains 18,612 pixels in 353
components; the largest contains only 53.3957%. The L image is also an earlier
unmodified retail identity. Do not promote face 8 to visible terrain and do not
interpret the result as no effect. R2 remains open.

**Superseded Track-R gate:** this block originally required a timestamp grid
spanning an empirically established animation cycle. EXP-003 D1 later found no
exact period, so that cycle requirement is retired. EXP-004 later rejected its
phase-sensitive full-frame gate; the consumed EXP-005 phase-agnostic
stable-background history appears below. The completed D3 finite-grid result follows it. A later C/L/L/C block and one-byte
A1/B/A2 remain out of scope and unauthorized.
## R2d superseded history - exact sampled phase calibration

[[EXP-20260819-003 - R2d Anthill sampled phase calibration]] was authorized and consumed by rejected D1-AH-001. Its exact-period model is superseded; its old D2 identity must not run.

The consumed 121-frame D1 set had no exact sampled period. One of four prior camera crops also contained live animation. Those facts reject reuse of the cycle/crop gates; they are not a no-effect or mesh result.

EXP-004 outcome: [[EXP-20260819-004 - R2e Anthill stable-background calibration]] captured all 121 authorized D1 frames but rejected because exact full-frame F0 equality was phase-sensitive. All three camera-control crops remained exact. D2 did not run, no mask was accepted, and the old D2 identity is obsolete.

EXP-005 outcome: [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] ran fresh D1/D2 controls. Both independently passed the complete hardware/Level01/crop/timing/lifecycle gates, but D2 had 233 observations at 198 unique pixels outside D1's 91,060-pixel radius-three mask. The aggregate rejected and published no mask. The residual visually aligns with Flik's animation silhouette; it is not terrain or camera evidence.

Completed gate: [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] accepted one fresh D3 holdout against the diagnostic combined D1+D2 radius-three mask: 92,480 pixels (`30.104166666666664%`), raw-byte SHA-256 `2a07565016efd050129e7d53b9f71942b2503cec8fffc7cbc592e0d619373cb6`, PNG SHA-256 `ed8f43e54597a6d0f5d25bdd9c381319b1ed62bdededd4a0d28c4a67ff838c50`. D3 did not expand that post-EXP-005 training mask. A later C/L/L/C packet remains separate and unauthorized. Do not promote auto-hardware results to retail confirmation.

## 2026-08-19 R2 update - D3 nuisance-mask holdout passed

[[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] passed its single fresh derived-build holdout: 121/121 frames validated and zero pixels changed outside the frozen 92,480-pixel combined mask. The accepted result is finite-grid nuisance-separation evidence only; EXP-005 remains aggregate-rejected and R2 remains open.

At that point the next step was offline preparation of a separate C/L/L/C face-8 localizer packet. [[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] supplied that authorization-gated packet with the accepted mask and reference frozen without expansion or D3-derived adaptation. No localizer creation or runtime arm was authorized at that pre-runtime boundary; the later result appears below.

## 2026-08-19 R2i update - replicated face-8 localizer packet

[[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] was the active offline gate. It froze `C1/L1/L2/C2`, two independently created exact face-8 topology DATs, the accepted EXP-006 nuisance mask, the D1 reference, and the live 121-point grid. A pass could have established only a reproducible localized rendered change for the exact face tuple in the derived auto-hardware build.

Before runtime, EXP-007 passed its focused 33-test suite, full 1,418-test repository gate, and James audit. Its creator publishes L1/L2 only as one validated atomic pair, ambiguous/corrupt/demotion-failed pair state blocks launch, DAT-install receipts are exact and stateful, and its comparator retains separate L1/L2/disagreement masks. At that point localizer creation and all arms remained unauthorized and unrun. The later authorized result is recorded immediately below; the one-byte candidate remained outside EXP-007 throughout.

## 2026-08-19 R2i runtime update - replicated localizer inconclusive

[[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] then completed under fresh authorization. All four arms passed procedurally, but the causal comparator failed: 251 control outside-mask mismatches, 228 L1/L2 disagreements, zero intersection, and zero static core. L2 frame 35's entire 228-pixel change was reproduced exactly by C2 frame 35, so it is nuisance rather than face-8 localization evidence. Aggregate result SHA-256 is `723e03ed43d6133e65df25655954ba779767800b3b010f603a0b2d482e25a309`.

R2 remains open. Do not launch the one-byte candidate and do not call this a face-8 no-effect result. At that boundary, the next step was an offline control-only diagnostic. EXP-008 later completed it; the proposal still requires the fresh EXP-009 control holdout and later localizer authorization and cannot reinterpret EXP-007 as a pass.

## 2026-08-19 R2j/R2k update - control-trained mask awaits D4

[[EXP-20260819-008 - R2j Anthill control-trained successor mask]] completed the control-only offline step. C1 contributed zero observations; C2 contributed 251 observations at 249 unique pixels. The fixed transform adds only the radius-three dilation of those new control pixels to the old mask, producing a 93,445-pixel proposal (`30.418294270833335%`; decoded SHA-256 `9ff27caa...1ba`; PNG `b855df0a...c936`). This is proposed, not accepted, and does not rescue EXP-007.

**Completed finite holdout:** [[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]] passed all 121 frames with exact zero difference outside the fixed mask (`bf2b4625...69d8`). This advances only renderer-nuisance discrimination; collision Track C is unchanged. The next action is an offline, separately committed and audited localizer-successor packet. DAT creation and every runtime arm remain unauthorized until that new packet is frozen and explicitly authorized.

## 2026-08-20 R2l pickup - fresh replicated face-8 localization

D4 in [[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]] accepted the fixed 93,445-pixel nuisance mask only for its finite sampled grid. [[EXP-20260820-001 - R2l fresh replicated face8 localizer]] then created two independently derived work-copy DATs and completed fresh `C1 -> L1 -> L2 -> C2` arms under the exact auto-hardware build and 121-frame grid.

The pair and lifecycles passed, and controls matched outside the mask, but L1/L2 did not replicate: `20,634,078` disagreement observations, `211,650` union pixels (`68.896%`), zero intersection/core, three large components, and `0.537916` dominance. The frozen positive gates therefore failed and the result is inconclusive, not negative or causal. Next is an offline-only cross-time L1/L2 correspondence matrix plus separately frozen camera-safe crop/state comparisons under the unchanged mask. Publish no successor runtime packet unless that diagnostic finds a unique reproducible correspondence; otherwise preregister independent read-only camera/player anchors first.

## 2026-08-20 R2m pickup - offline cross-time correspondence

[[EXP-20260820-002 - R2m offline cross-time correspondence diagnostic]] freezes the non-runtime discriminator. It binds the exact R2l aggregate, pair/final dispositions, grid gates, creator receipts, all 242 frame PNG/RGB hashes, unchanged 93,445-pixel mask, and three independently accepted camera-safe crop hashes. It computes every `121 x 121` L1/L2 comparison and evaluates only integer lags `[-60,60]` with at least 61 overlapping pairs.

A lag was viable only when every overlapping pair had zero disagreement across all 213,755 eligible pixels, all three crops were byte-exact and equal their control hashes, both arms varied temporally, and exactly one lag passed. The result was `diagnostic-valid-no-unique-fixed-lag`: L1 did not vary outside the mask, L2 did, and all 121 lags failed. Although 1,815 individual pairs were exact, they are nonselecting and no fixed lag closes. Fixed wall-clock alignment is nonviable and must not be repeated. Next work is offline/static PC camera/player/render-state consumer analysis to justify exact bounded read-only anchors; no runtime is authorized.

## 2026-08-20 R2n pickup - PC state-equivalence candidates bounded

[[EXP-20260820-003 - R2n PC state-equivalence read candidates]] completes the
offline/static consumer analysis and rebinds its retail trace to the unchanged
addresses in auto-hardware build `1e1d5099...c41f`. At upstream completion PC
`0x00414585`, candidates are selector bit `0x0059A5EE & 1`, common input
`0x00599C90/18`, and live Flik coordinates `0x0059D910/12`. At generated-view
completion PC `0x0041458F`, candidates are matrix `0x005B58E0/18`, origin
`0x005BDB8C/12`, and matrix copy `0x005BDBAC/18`; derived origin
`0x005BDB9C/12` is optional/redundant.

Do not expand `0x005BDBAC` to the physical 32-byte copy. Do not use the
repeatedly clobbered `0x0063E888` scratch family. Do not poll these globals
asynchronously.

**EXP-004 active pickup:** four authorized D1 attempts are consumed.
`-001` rejected before ptrace while focus settled; `-002` rejected because
focus commands used the host display; `-003` passed the corrected focus gate
and then rejected before ptrace on a lowercase host path for the uppercase
Level01 DAT. `-004` fixed that path, attached to an exact 16-task census,
armed only local DR0 on those tasks, and reached one exact outer-entry trap;
the immediate stop-all census differed, so it rejected before TID selection,
R2o state reads, stopped captures, or later scientific action. Its 16 initial
register changes were restored and read back. Every D2 arm remained unrun.
The cause of the changed census is unknown.

At that pre-run boundary, the next action was to commit and obtain James
acceptance for `-005` identities and durable per-check census/delta evidence
before requesting D1/D2 authorization. The later authorized D1 repeated census
drift, so R2o retries stopped and R2p below superseded this pickup. The exact
no-churn gate remains: never enroll, ignore, or remove a later task.

## 2026-08-20 R2o pickup - completed-present calibration protocol

[[EXP-20260820-004 - R2o completed-present state calibration protocol]]
freezes the offline successor. `0x0040FFE3` is admitted only after the same
normal invocation passes both R2n phase PCs, a successful EndScene return, and
exactly one successful fullscreen Flip or windowed Blt return. The static
chain establishes CPU order and DirectDraw return status, not Gamescope
compositor-latch timing.

The future control-only sequence is exactly D1 then D2, three complete normal
invocations per fresh process, and one terminal completion-to-next-
`0x00414585` screenshot-equality check.
It requires exact corresponding state tuples and images, internally identical
stopped triplicates, and at least one completed-frame image change per process.
No nearest-state search, adaptive extension, DAT mutation, localizer, or
candidate is permitted.

**Historical closure:** James accepted both `-004` and `-005` first-trap
task-census rejections. The later `-005` result consumed its authorization and
ended R2o retries under the frozen no-churn rule. Its validator independently
recomputed deltas, authenticated the full rejected journal prefix and exact
restores, required the exact action/value grammar through failure, and forbade
scientific action after mismatch. All census receipts repeated the immutable
open task identity, while failed prefixes bound exact stop/slot/DR6/active-
debug and chained debug-write state.
The attachment/open list must equal that immutable sorted
`(TID,start_ticks)` census, including start ticks rather than only TIDs. Stop
receipts accept only a supported recorded register layout, derive the payload
as three native words, and require the layout to remain constant; retained
`-004` evidence is `x86_64` with 24 payload bytes.
No further D1/D2 completed-present retry is active or requestable from this
packet. R2p supersedes it.

### R2o implementation checkpoint (2026-08-20)

The completed-present calibration design is frozen in [[EXP-20260820-004 - R2o completed-present state calibration protocol]], and its argument-free executor plus offline tests are implemented. The first authorized D1 is a consumed pre-attach focus rejection, not an R2o sample. The implementation does not change the agenda or close R2: it exists to obtain reproducible completion-boundary controls before returning to a face-8 localizer. A successful future D1/D2 packet would calibrate bounded CPU/display-pipeline state equality only, not terrain, collision, materials, face visibility, or compositor latch.

The first executor audit correction was James-accepted before runtime. The
third authorized D1 consumed `D1-AH-003` and aggregate `-003` as pre-attach
host-path-case rejections. The fourth consumed `D1-AH-004` and aggregate
`-004` after one exact hardware trap because its task census changed before
selection/read/capture. The fresh offline correction pins
`D1-AH-005`/`D2-AH-005` and aggregate `-005`, retains each exact census and
independently validates its delta and allowed post-failure action ceiling.
The eighth audit correction additionally binds the completed ptrace-open
`(TID,start_ticks)` list to the open census and validates the retained
`x86_64` stop layout through the supported-layout table rather than a fixed
synthetic layout.
The ninth audit correction additionally derives stopped `SIGTRAP` from the raw
wait status, requires zero ptrace event, and compares the completed ptrace-open
task list in its recorded order to the immutable sorted census. A ptrace-event
stop, inconsistent stopped signal, or reordered attachment receipt rejects.
That sequencing is historical: the second D1 census drift occurred, ended
retries, and required the separate R2p diagnostic below. Do not begin a
localizer or candidate.

## 2026-08-20 R2p pickup - task-lifecycle diagnostic

The separately authorized `-005` D1 repeated the first-trap census rejection.
Its new exact evidence identifies one addition `(TID 1648646, start_ticks
28065259)` between the 16-task open census and immediate stop-all census. No
task was removed or reused. D2 was not created, cleanup was clear, and James
accepted the rejection. R2o retries are closed under the preregistered rule.

[[EXP-20260820-005 - R2p task lifecycle diagnostic]] is now the sole active
offline packet. Its argument-free analyzer authenticates both rejected runs
and publishes `diagnostic-valid-task-addition-identity-unresolved`, SHA-256
`8d35c6b68a21d881ad98981db6842b8d050a17d7900c29fec4ea319378f70e43`.
That corrected result binds each packet's complete classified manifest and
the accepted R2o action grammar. The earlier `b407bcf2...2d5` analysis is
retained as obsolete rather than overwritten.
The PC imports `CreateThread` and has one direct call at `0x0042CF04`, but no
evidence links that PC path to the added Linux task.

**P0A pre-run audit history:** James rejected the first committed P0A implementation (`52d9a0f`,
tree `8b271be`) on nine evidence-integrity defects. Commit `b24890b` / tree
`8ce1cfc3` closed those nine and passed 150 focused plus 1794 full tests, but
James rejected five further counterexamples before runtime. The second
correction at `c05f167` passed 158 focused tests and closed all five, but
James rejected its adjacent-delta lifecycle partition before runtime. James then
rejected exact `96e2fdf` / tree `60ab6a3d` because neither analyzer nor the
fixture anchored every task census to the guarded process leader. The packet requires a common
authenticated hardware/Level01/navigation/runtime prefix for scientific and
rejected publication, monotonic audit and `R:` restoration receipts, and a
real isolated X11/XTEST ABI fixture. A rejected collection must authenticate
its retained sample prefix and bind one enumerated runtime failure exactly to
the disposition; arbitrary validator failures remain pending. At that
historical pre-run boundary it was unrun. The user explicitly authorized the
exact 521-point P0A passive
`/proc` collector. Each request is 20 ms apart, must start within 2 ms and
complete within 10 ms without overlap; missed, duplicate, backward, late, or
extra samples reject. P0A
performs no debugger attachment/write, signal, process-memory read, screenshot,
or DAT action. No R2o retry, localizer, or candidate is authorized. Terrain,
collision, materials, face visibility, causality, and retail behavior remain
open.

The second correction kept incomplete packets nonterminal under
`published-unverified`; admitted an exact timing miss only as its derived
procedural-rejection reason; performed post-manifest semantic validation,
authentication, packet fsync, and both-parent rename fsync; bracketed task
metadata identity; deduplicated unresolved initial/added categories; rejected
non-hex executable digests; bound live asset paths; and bound both X sockets'
`SO_PEERCRED` PID/start to the owned Xwayland identity. Its focused suite is
historical at 158/158. The third correction additionally derived complete
per-TID identity histories, detected reuse across absence, partitioned unresolved
metadata by global first-seen sequence, restricted short-lived classification,
and failed closed with exact intervals when one identity reappeared after an
absence. The fourth correction additionally required both enumerations to
contain the guarded PID, every stable sample to contain exactly
`(pid,process.start_ticks)`, and every task to start no earlier than the
process. It rebuilds fixtures around a permanent leader and pairs five
leader-anchor counterexamples through direct, scientific, and rejected-prefix
validation. James confirmed that anchor at `b8e8d44` / `5c48cbb4` but rejected
the one leader-omission exception because malformed or empty identity-error
receipts could invoke it. The fifth correction used one shared exact,
nonempty, single-line typed metadata-error validator before omission or early
drift classification. Direct/scientific/rejected regressions bring the
analyzer/packet suite to 201/201, with the native X fixture passing separately.
James confirmed those malformed forms were closed at `a68076f` / `10bdcad9`
but rejected one impossible cross-phase internal message. The sixth correction
bound the five exact `/proc/stat` parser errors to initial identity
reads and admitted the one post-metadata identity-change message only in its
producing phase. Paired three-path tests bring the analyzer/packet suite to
207/207, with native X passing separately (208 total). The explicit
authorization could not be consumed at that historical boundary until James
returned ACCEPT on the immutable correction.

James accepted the immutable correction at `8437c0a` / `53241906`, and the one
authorized P0A-AH-001 wrapper invocation was consumed. It passed hardware and
Level Select gates plus focused `Right`/`Return` delivery, but the retained log
loaded level07 instead of Level01. The Level01 gate timed out before
`collection.json`; no passive lifecycle sample exists. Normal `Alt+F4`
delivery did not clear the loading process within the bounded polls, so stage,
evidence, and `R:` remain pending and the live runtime was recorded without
signal cleanup. No retry, recovery, second arm, lifecycle conclusion, or
terrain/collision inference is authorized. The live sockets peer with Gamescope
rather than the frozen Xwayland identity, so the isolated fixture did not model
production provenance; the retained post-close audit is also unparsed because
Make stderr followed JSON stdout. Fresh explicit authorization and a new frozen
packet are required for any cleanup/recovery decision or corrected passive
successor, which must resolve/re-freeze the peer binding and separate audit
stdout/stderr first.

The offline postmortem now implements those two provenance corrections without
creating a successor arm: audit stdout/stderr are separately authenticated,
and both X sockets bind to the exact owned Gamescope peer while the display
binds independently to the sole Xwayland launch marker. The consumed wrapper
fails closed. Bounded retail disassembly also shows that the Level Select path
resets carousel position zero, tests the live Right bit, and can increment its
local selection without a previous-state edge test. Thus level07 after the
retained 180 ms hold is consistent with repeated held-state polls, while known
dropped short taps rule out a timing guess as a deterministic repair. The user
reports save states unavailable, and this pickup does not depend on them. No
P0B identity, runtime authorization, lifecycle sample, or terrain/collision
conclusion followed at that checkpoint. The separately established direct
focused `xdotool` route was later restored to the design; fresh explicit
authorization and James pre-runtime acceptance were later supplied as recorded
below.

James rejected the first offline postmortem candidate (`932627d` / `4742aa21`)
because boolean numeric aliases and incomplete X-peer credential/chronology
binding could admit impossible evidence identities. The corrected offline
validator closes those paths and passes 269/269 non-native focused tests,
native X (270 total), and 1914/1914 full tests before James re-audit. A later
read-only audit records no open session, only three unattributed helpers plus
the private sink, and absent prior game/Xwayland PIDs; their exit cause is
unknown. This changes no terrain/collision result or authorization boundary.

James then rejected `740cb07` / `56818bd1` for float numeric aliases, ignored
owned polls, drift-masked sample structure, asymmetric metadata-error
partitions, and a raw missing-PID exception. The corrected offline validator
shares one exact task/error partition and rejects every reproduced alias. Its
297/297 non-native focused tests, native X (298 total), and 1942/1942 full gate
passed before the later James re-audit. No terrain/collision evidence or
runtime authority followed.

James later **ACCEPTED** the complete postmortem correction at exact
`1b61da32c93b1238c108c0a95cb02628f3284949` / tree
`925ce807af1cd4db706a2d6f733ba935b73d30ba`, independently passing 297
non-native focused tests, native X, all 1942 repository tests, and 50/50
adversarial replays. This closes only the offline validator audit.

The Level01-route blocker recorded above was wrong. A fresh user-directed
operational launch reused the established direct focused `xdotool` path—fixed
LevelSelect settle, 180 ms Right, one-second gap, 180 ms Return, final 180 ms
Return—and reached live Anthill gameplay under auto-hardware image
`1e1d5099...c41f`. The log loaded Level01 and reached ClearLoadScreen,
InitMainGame, and NextLife completion markers; transient compositor frame
`77f6eeff...84f598` visually corroborates gameplay. No memory/save-state or
DAT action occurred. This is not P0B evidence and the game remains open for
the user.

James accepted this as an **offline design basis, not pre-runtime acceptance**.
P0B must preserve the existing sample-5 title Return: direct `xdotool` sends
only carousel Right and select Return, then the two persistent X connections
open after exact Level01/Start ClearLoadScreen. The independent worker sends
the sole title Return at sample 5; the 521-point grid then completes before
ordered gameplay-log validation. Fresh namespaces and a separate `Y:` stage
must never touch P0A pending bytes or `R:`. The open operational process is
ineligible and must close before a future clean P0B pre-audit.

The corrected pickup now has an offline P0B implementation: it preserves the
accepted 521-point passive `/proc` collection and validators, allocates fresh
identities, authenticates complete P0A exclusion manifests before/after, and
replaces only the unproved persistent-X navigation delivery with the
established precollection direct route. Its wrapper refuses runtime.

James rejected first immutable `2277b75` / `cf2f88c` for stale cloned-log
provenance, drive-specific level filtering, unscoped xdotool identity, strict-
schema/publication/direct-analysis holes, and inconsistent save-state/ptrace/
P0A-`R:` boundaries. The successor correction establishes a fresh stable log
file and append chain, drive-independent route grammar, display binding, shared
exact schemas, authenticated publication phases, and one exact prohibited/P0A
boundary; 351/351 focused tests passed. Carousel-counter semantics remain open,
but no longer block exact Level01 navigation. The full gate passed 2293/2293
with zero tracked-file violations. The next audit below then rejected that
exact candidate; terrain/collision remain open.

James next rejected exact `8b8d19d` / `e8b58c9` for nine adjacent protocol
defects. Most relevant to this roadmap, a forward-slash wrong-level load could
escape the pre-input guard and a coherent later Level02 load could satisfy the
gameplay chain. The successor uses one shared path-spelling-independent parser
and requires exactly one total Level01 load through the final log; it also
closes nested P0A-manifest, X-observation, numeric-alias, connection-root, and
terminal-root boundaries. The focused suite passes 396/396. No lifecycle or
terrain/collision evidence was collected, so KU-079 and all terrain/collision
claims remain unchanged.

The 396-test correction passed 2338/2338 full tests and was frozen at
`e0fa61a` / `02550b15`, which James rejected for two more protocol defects: an
unhashable P0A entry kind leaked `TypeError`, and a fresh pre-LevelSelect
wrong-level load was ignored. The successor type-checks the nested kind and
requires zero level loads anywhere in the fresh pre-input prefix; its focused
suite passes 405/405. This remains protocol evidence only and narrows no
terrain, collision, material, or render-grammar unknown.

The successor passed 2347/2347 full tests and James **ACCEPTED** exact
`3c90a6f` / `5fb8ea6` as the immutable offline P0B pre-runtime design. This
authorizes no runtime and adds no lifecycle, render-grammar, terrain,
collision, material, visibility, or causality evidence. At that checkpoint
fresh authorization remained required.

The user then authorized one P0B-AH-001 invocation. Later explicit signal
direction allowed exact guarded cleanup of old group `1978654`, after which the
sole P0B invocation completed 521/521 passive samples. It provisionally found
one added task `2086681/34785536` from sequence 27 through 520, with no other
lifecycle class or acquisition error. Normal close failed, so at that
checkpoint the original packet remained pending, new group `2086248` was live,
and `Y:` remained staged.
James accepted only the provisional finite-grid task addition and fail-closed
pending interpretation. This does not identify the task, its creator, or any
terrain/collision function. James rejected first recovery implementation
`575756d`, then rejected `d4de863` for one nested alias, post-deadline polling,
and publication rename races. Its then-unrun successor added
exact pending-receipt comparison and atomic no-replace publication; its full
gate passed 2395/2395, while exact commit and James acceptance remained
required at that checkpoint.

That recovery was later James-accepted and invoked once, but failed closed
after its authorized group TERM when exiting processes exposed cleared command
lines. It remains consumed and did not restore `Y:` or publish recovered
evidence. Between the authenticated pre-recovery and post-TERM states, 160
bytes of shutdown text were appended to the original P0B `launch.stderr`.
Chronology, content, and retained-FD provenance make attribution to recovery
shutdown consistent, but it remains an inference. The packet's append-
preserving current identity is `1092fcb9...25f2`.

A separately authorized operator-only cleanup then sent individual TERM and
guarded survivor KILL to exactly Gamescope `2086265/34784563`,
gamescopereaper `2086416/34784596`, and winedevice `2086454/34784605`. James
accepted the final 15-entry envelope at `24df2fb7...d65b`; both final audits are
clear, `Y:` is retail, and `R:` remains P0A. This resolves only environmental
cleanup. The provisional task's identity/function and every render-grammar,
terrain, material, collision, visibility, and causal question remain open; no
runtime successor is authorized.

Offline P0C subsequently authenticates the P0B collection against R2o
D1-AH-005 and confirms a 16→17 post-title task transition in two fresh
processes, including debugger-free P0B. It therefore disproves the old early
16-task census as stable, but neither proves a universal 17-task census nor
binds the two Linux identities to one logical worker. PC-native PLAYTRACK and
DirectSound bytes make worker `0x00440F50` the strongest role candidate for
P0B TID `2086681`; that remains inference because there is no TID-to-start-
routine receipt. The safe return path is offline R2q design around an
authenticated gameplay transition and a prospectively fixed pre-attach
quiet-census interval, followed by an immediate census recheck and continued
fail-closed checks. Dynamic enrollment remains forbidden. This still grants
no runtime and changes none of the roadmap's terrain, collision, material,
visibility, render-grammar, or causal unknowns.

James subsequently rejected exact R2q `-009` (`f81502b` / `e56942b`) because
its terminal-state-independent reducer still omitted dependency-applicable
receipt relations and because source-parent stat time was not anchored to the
terminal publication outer receipt or the ordered post-D2 rereads. Fresh
immutable offline `-010` (`d07d3d5e...effd5c`) consolidates those relations
and exact chronologies, passes 226/226 focused tests and the 2696/2696 first
full gate, and awaits exact commit/final gate plus James re-audit. This is
still only a prerequisite for a future completed-present observation: it adds
no terrain, ground, collision, material, visibility, render-command, causal,
or no-effect evidence and grants no runtime authority.

James then rejected exact `-010` commit `889f105` / tree `a93c929` because the
nominal executed process and exact `PC/BUGS/bugs.exe` asset entry shared path
and SHA but contradicted each other on device/inode/size/mtime. Fresh immutable
offline `-011` (`6a8fd3df...c1022`) cross-binds all six executable provenance
facts in accepted and dependency-applicable nonaccepted prefixes. Coherent
direct and accepted/rejected/pending terminal regressions recompute every
dependent process-guard and envelope hash before the binding rejects. The
focused suite passes 229/229 in 740.93 seconds; the first full repository gate
passes 2699/2699 in 1397.31 seconds with zero tracked-file violations. Exact
commit/final gate and James re-audit remain pending. This still identifies no
terrain, ground, collision, material, visibility, render command, causal, or
no-effect behavior and grants no runtime authority.

James then **ACCEPTED** the documentation-inclusive `-011` offline basis at
exact `409cbfb` / `de4fa87`. The accepted diff from rejected `ed2e655` was
exactly three historical `-010` byte-count corrections; `-011` remained
73,008 bytes / `6a8fd3df...c1022` with unchanged implementation, test,
wrapper, and namespace bytes. This closes only the offline prerequisite audit.
It grants no runtime authority and still identifies no terrain, ground,
collision, material, visibility, render command, causal, or no-effect
behavior.

## 2026-09-01 R2q-026 outcome - pre-science namespace failure

The sole `-026` D1 arm did not reach the experiment. Its real five-second
process-map convergence correction worked, but launch provenance then compared
a process-mount-namespace maps device (`00:24`) with the host namespace's
device minor (`38`) for an otherwise exact preloader path/inode/SHA-256 and
failed closed. D2, quiet census, ptrace capture, stopped ranges, PNG batches,
and comparison never occurred.

Exact cleanup and a distinct user-authorized mapping-only successor restored
retail `Y:` while preserving the displaced D1 link and P0A `R:`. James accepts
only that failure/root-cause/recovery boundary. The packet explicitly records
`terrain_collision_claim:null`; therefore R2 and collision Track C do not
advance, and KU-079/080/081 remain open. The next nominal successor must first
bind executable-mapping provenance within a single namespace, then pass the
same offline source/activation/full-gate/James sequence before any new runtime
authority.

## 2026-09-05 material fidelity follow-up

[[EXP-20260905-005 - Original wall texture regions and colour inputs]] opens a
bounded appearance pass on the deck/ramp/box fixture of
[[EXP-20260905-004 - Playable ramp and box area]]. Near-spawn original
steep faces select different page-0 coordinate regions and warm varying vertex
colours; the authored box uses the floor region uniformly. First localize the
original-wall reference and distinguish texture-region-only,
colour-only and combined arms. Collision stays banked and unchanged. The
uniform darkening draft is not accepted or applied.

EXP-005 application update: a combined native wall-region and donor-derived
warm-gradient box candidate was built. Separate region and tint file arms pass
offline preservation tests;151 terrain tests passed. No collision redesign,
full-suite/R2q run or universal material acceptance.

[[EXP-20260905-006 - World-scale terrain tiling and checked mesh growth]] then
provides an offline-tested 512-unit candidate, collision-preserving tiling and
original-instruction-checked pointer/footer growth. 185 terrain tests pass;
no R2q or full-suite rerun. Fresh cold-load and resident checks later pass for
the exact tiled candidate. EXP-006 does not close general R3/R4 packaging,
arbitrary geometry, all-view rendering or EXP-003's separate prop-aware seam.

## EXP-007 - Layout coverage is not solved by a working isolated box

[[EXP-20260905-007 - Retail position control and missing floor footprints]]: the OG Up control crossed source-99 cells `44140` and `44248`; their footprints have no active parsed floor in the authored fixture. The earlier fall endpoint is covered by retail cell `45884`, likewise absent from authored active traversal. The fixture replaced source 99 rather than adding independent collision. Preserve needed original groups or deliberately replace their render and collision coverage together; prove exit/landing and the exact earlier fall in the PC instruction model before claiming an integrated layout fixed. The separate missing-render/retained-collision report still needs exact face/cell localization.

## EXP-008 - Global edit scope confirmed; additive integration is next

[[EXP-20260905-008 - Whole-Level01 collision and render coverage audit]] compares all 16 Level01 files, all 189 TERRAIN.ALL sources, resolved active cells and barriers, and 124 supported static render references. Only collision source 99 and render reference 160 are replaced. The source's 134 original cells become inactive, including 116 with intact bytes after the earlier terminator; 7,147 other cells and all barriers remain unchanged. The collision and render chunks cover different footprints.

The next authoring gate is retaining needed original geometry while adding the new playable area through checked storage/descriptor paths. First establish the smallest required capacity/relocation change if the existing writers cannot accommodate both. Then prove native-instruction overlap selection, exit/landing/return and the earlier fall. This is not another standalone box proof and not permission to patch a second native terrain chunk blindly. The full private offset inventory and top-down map are under `work/experiments/EXP-20260905-008/`.

### EXP-009: additive preservation candidate

[[EXP-20260905-009 - Additive terrain preservation and access ramp]] stages the append path: retain all 134 original source-99 cells, append fourteen working-area cells plus two connector cells, and retain original mesh-160 geometry in the expanded mesh. The final terrain gate passes 224/224. Native allocation/relocation/command traversal and box/fall checks pass; the same synthetic fall stays airborne in the replacing control but lands first on original cell 45884 in the additive candidate. Four separately declared continuous-crossing/return routes now pass without resetting between legs. The old exact-point failures remain recorded: on original cell 44140, target slowdown plus fixed downward input approaches normal-directed motion, while fixed forward input traverses the same ground. Do not edit geometry to hide that controller artifact or relabel the failed criteria. Next is controlled runtime comparison of zero depth bias, render visibility/sorting/overlap and full actor behavior. Terrain/collision and general additive authoring are not marked solved.

### 2026-09-06 visibility-authoring gate

[[EXP-20260906-001 - PC-compatible ramp visibility bounds]] adds PC view-plane-aware bounds to the additive builder and an isolated two-byte file candidate, preserving all collision/geometry. Bounded tests and native camera sweep pass; fresh runtime remains pending old-session cleanup approval. Do not treat a geometric sphere alone as sufficient for this PC scene gate, or the current conservative profile/rounding allowance as a universal renderer rule. Next acceptance: file-loaded bound identity and live ramp camera angles, retaining EXP-009 as control.

### EXP-003 paired-side candidate

Visual-only ground-reaching ramp side faces (EXP-20260906-002) passed a fresh
cold-load identity check, but a RAM-recorded Up test crossed both visual side
planes, so the next step paired the new sides with established wall collision.
[[EXP-20260906-003 - Solid ramp sides and ground contour trim]] stages matching
vertical collision and a separate selected-ground trim, retaining controls and
all working floors/top. Native blocking, landing/step-off, steered returns and
storage gates pass; the old western fixed-axis drift failure remains reproduced
in the unchanged control.72 terrain tests pass, with one new synthetic fixture
winding correction awaiting approval in the affected gate. Next finish that
test-only correction and run a fresh runtime check; neither live side behavior
nor the ground-join appearance is accepted yet.

## 2026-09-06 solid-side preview: next acceptance gap

[[EXP-20260906-003 - Solid ramp sides and ground contour trim]] is live after 138 affected tests and the 72-test terrain gate; user confirms side blocking. New bounded defect: Flik's visible model partially enters/disappears behind the authored wall at contact. Add body clearance/occlusion to wall-authoring acceptance, separately from blocking and ground-join trim. Next measure original versus authored stop intervals and rendering before declaring collision padding necessary; isolate collision-only and render-only variants if supported. Existing candidate remains the control. Full evidence/limits: `reports/terrain/EXP-20260906-003-runtime.json`. No universal wall rule or completed terrain/collision authoring claim.

## 2026-09-06: wall-clearance trial ready for user acceptance

[[EXP-20260906-004 - Wall clearance comparison and offset trial]] is file-loaded in Level1: a local collision-only48-stored-unit side offset, render/floor/original collision unchanged.69 affected tests,30 native outcome groups across two arms and72-test terrain gate pass. User still needs to check visible body overlap and lower-corner/clearance-strip entry. Original geometry is nonuniform, and the live original-wall navigation failed to reach a matched comparison. Do not promote this margin or the point-based branch observation into a universal wall/actor-radius rule. Next acceptance remains visual clearance and end/corner behavior, not a new terrain grammar rewrite.

## 2026-09-06: stripped authored-layout trial

[[EXP-20260906-005 - Isolated authored terrain and platform spawn]] separates the new 36-cell/807-face area from the old landscape and adds a private executable-table platform spawn. 53 affected and 72 focused terrain tests pass; 9 native arms pass, with the spawn arm stopped by a disclosed omitted-heading setup bug. No runtime switch or acceptance yet. Next: approved probe correction, complete native spawn proof, then fresh staged runtime comparison. Preserve EXP-004. New container/layout APIs, actor placement, runtime respawn and freestanding skirt finish are not claimed complete.

## 2026-09-06 next gate: original foliage and a reliable no-fall perimeter

EXP-005's isolated pieces have a corrected10/10 native gate; their open edge remains the control, not a bug concealed by restoring old terrain. [[EXP-20260906-006 - Perimeter barriers and original foliage reference]] preserves an unaccepted short-loop trial and an exact original tall-grass reference view. Next map that view to original render records and blocking segments, diagnose failed midpoint/corner/airborne cases, and prove player/projectile behavior separately before pairing a new visible perimeter. No general level-authoring or foliage-collision completion is claimed.

EXP-006 later establishes that original-PC source180 segment160 gives separate XZ response at that original reference, and that the original Level01 grass materials/geometry are reusable without new artwork; an off-screen file catalogue supplies381 filtered templates. A file-loaded grass boundary paired with explicit perimeter collision blocked the player. General texture-package export and a bounded lower-ramp straight-release oddity remain open.
