---
type: archive
status: historical
created: 2026-09-26
tags: [archive/project-review]
---

# Current State history through 2026-09-26

Historical snapshot of [[Current State]] before the September 26 review. The body
below is preserved, including superseded claims, old process IDs and
consumed permissions. It is evidence of earlier notes, **not a current work
queue or runtime binding**. Use [[Current State#Current task handoff]] and
[[Environment Status#Current runtime handoff]] for current instructions.
2026-09-26 - Codex - Project review and Vault cleanup records the review.

<!-- preserved-body:start -->

## Storage inspection, 2026-09-20

User subsequently authorized old-build deletion: 2026-09-20 - Codex - Remove old generated game builds removes122 old timestamped outputs and keeps30 required/current builds. Receipts/settings/EXEs retained in `work/storage-cleanup/20260920/`; deleted game-data trees are not backed up. Observed filesystem free-space increase227.848 MiB despite54.42 GiB summed folder size. Current production/source hashes still match. Earlier inspection paragraph below records the pre-cleanup state.

2026-09-20 - Codex - Directory space audit finds extensive Btrfs sharing: ordinary du867.92 GiB versus whole-tree FIEMAP21.33 GiB exclusive plus5.14 GiB set-shared; exact compressed physical usage remains unmeasured. Raster images in work total2.171 GiB. Two temporary-directory candidates total2.87 GiB exclusive before compression; no files deleted or game state changed.

## Previous task: populated original Training and Blender lesson controls

Original Training is open with pickups, actors and adjustable Mr. Soil lessons:
`work/level-projects/original-training-soil-triggers/level.blend`.
[[PC original Training Blender mapping]] owns its workflow; use
`.venv/bin/python scripts/ablpc-level edit work/level-projects/original-training-soil-triggers`
and **N → ABLPC Map** for layers, top view, source offsets and saved landmarks.
`overview.png` supplies a standalone top-down image.

[[EXP-20260909-012 - Original Training Blender mapping]] imports278 original
scene records, four packed textures,1360 collision triangles,80 barrier segments
and78 stored-placement markers.73 selected checks and saved Blender position/UV/
landmark persistence verification pass. Training's PC files are in
`LEVEL07/LEVEL1.DAT`, `LEVEL1.RAW`, `TERR1.ALL`; the on-disk LEVEL00 directory
is not Training gameplay. This is a reference/annotation workflow with stored
scenery poses, approximate lighting and no original-level game-file exporter.

[[EXP-20260909-013 - Populate original Training Blender map]] adds50 grains,
F/L/I/K, four spiders, four seeds, original textured Mr. Soil in stored pose and
an exit-sign/contact overlay. Pickups use original offline00456A90 initialization;
actor feet use native floor queries. Other meshes are editor representations,
not animated rigs. All383 preexisting objects remain exact in the successor;
saved-file placement/annotation checks and89 selected make checks pass.


[[PC Mr Soil lesson triggers]] solves all14 native predicates and adds per-lesson
Original goal / Goal + full speech / Full speech only, counts/special timing and
height controls. Default successor is all-auto with2-second tails. Its sidebar
builds fresh original-Training copies; geometry export remains unsupported.
EXP-20260910-002 passes23 focused
tests, two-base routes and477-object/settings persistence. Live hardware RC1
plays all14 instructions in order without gameplay actions, then stays at13;
full drain and approximately2s tails are directly sampled for stages0–8.
Final six tokens are revealed, weapon remains0. RC0 software arm was rejected.
Actual Flatpak sidebar Build succeeds and reproduces EXE9587108f…c300d3.
Final focused make check:173 pass; Vault878 notes,0 errors,8 preexisting warnings.

Current mapping Blender13806/start3783313/group13781 is intentionally OPEN.
Predecessor Blenders10133/start2988878 and9585/start2951205 are preserved for
possible unsaved work. Both owned test games and private sinks were closed;
fresh session-audit is clean. Live observation was read-only, with ordinary
Return/Down setup keys; no gameplay-action inputs or live RAM writes.
[[Environment Status#Current runtime handoff]] owns
process accounting. Latest: 2026-09-10 - Codex - Make Mr Soil lesson triggers editable.

## Milestone 4: actual seed owners and scattering mechanism, 2026-09-08

[[EXP-20260908-016 - Manual seed ownership and native scattering]] confirms the user's drop/departure/return/pickup of seed63. Its actor bytes
stay exact through205.369s /6418 frames of terrain-page absence. The actual queue,
all20 plant links, selected pointer and carry roots now accompany a cold capture;
this closes EXP015's synthetic-root gap for a new sample. Eight native pickup and
128 actual-cell replays pass. Actor storage itself remained resident.

Original code also demonstrates two remaining hazards: mode0x80 can write slot63
outside the active queue, and a close pair of seeds at the boundary accumulates
opposing velocity. Eight fixed-slot and eight pair controls pass. The user's flying
seeds have a supported native mechanism; complete burst attribution and a fix remain
open. Milestone4 still needs safe actor release/publication, other state and broader
world/memory gates. No live serializer or normal-build change is installed.

Diagnostic26409 is CLOSED; final game/sink audit is clean, desktop GNOME Xwayland is
accounted for and preserved. Normal project/bank files and frozen EXP014/015 remain
exact. No game preview is running and no manual control is needed now. Latest:
[[2026-09-08 - Codex - Manual seed ownership and scattering]]. Older banners are historical checkpoints.


## Milestone4: seed growth repair and moved-state cycle verified, 2026-09-08

[[EXP-20260908-014 - Manual moved-seed page persistence]] repairs the private20-plant capacity policy after the user found stuck pickups and disappearing seeds.
Full-pool or held ten-tick growth requests now cancel, undo partial sinking and run
ordinary seed update. Partial growth animations reserve vacancies. A new stomp is
required after freeing a slot; the old automatic deferred-growth policy is superseded
for this private image. Native twelve-way contention/recovery and live contact64
rejection/pickup/carry/throw, mushroom release and successful retry pass.

Actor20/contact21 then retains its exact moved position through actual terrain page2
absence and return, and can be picked up again.277 cold observations preserve its
actor/placement bytes; the minimum verified interval is2.106s/66frames. The old page
allocation is reused by another managed page. Actor and placement arrays themselves
remain resident, so this does not close actor/item storage persistence.

47 new regressions,138 focused tests and selected make check1682 pass. Admission64
has8266 page observations and8702 checks of all65 models. Both diagnostics are
CLOSED:466588 and479714. Normal154936 remains open;721 normal files, saved Blender and760 bank
files remain exact; EXP013's300 artifacts/22 dependencies reverify. No external live
writes, debugger stops or level exits. The user reauthorized automated controls
while away; that authorization persists. Normal preview remains on its earlier build.

Milestone4 remains open for actor/item serialization and lifecycle,310 numeric
reference candidates, full consumer/driver coverage, world budgets/coordinates and
total-memory bounds. Latest: [[2026-09-08 - Codex - Manual seed persistence investigation]]. Older banners below are historical checkpoints.

## Milestone4: seed budget and distant carry verified, 2026-09-08

User handoff: the live investigation is finished. The user will control Flik in
the existing normal preview; leave movement/input to the user and perform analysis.
The seed-budget image remains a private test build, not that normal preview.

[[EXP-20260908-013 - Seed auxiliary budget and distant carry]] adds a private guard at two discarded-return seed emissions. It preserves8 reusable records against that
source and skips excess requests. Native allocators and other callers are unchanged;
this is not a general pool-full solution.197 CPU/stack samples identify the stalled
request at0041DA68. Native template53 can produce the captured retained fields.

Patched actor0/contact1 and actor63/contact64 copies complete distant carry, throw
and landing.697/691 page observations and708/707 checks of all65 models pass;
102/215 emissions are suppressed and all64 placement identities survive. The
unpatched positive-offset control also passes; the trigger's dependence on actor
identity, density, paging or timing remains unresolved. No exits occur.

59 focused tests and selected make check1635 pass. All four diagnostics are CLOSED;
normal154936,721 normal files, saved Blender,760 bank files and the frozen EXP012
390-artifact/19-dependency packet remain exact. Latest: [[2026-09-08 - Codex - Seed auxiliary budget and distant carry]].

[[PC Large-Level Engine Roadmap]] remains incomplete for general pool/caller
lifetimes, actual actor/item section persistence,310 numeric reference candidates,
world budgets/coordinates and total-memory/driver coverage. Normal compiler and
preview are unchanged. Older banners below are historical checkpoints.

## Milestone4: selected high-slot interaction passes, 2026-09-08

[[EXP-20260908-012 - High-slot seed interaction and native pool limit]] passes native contact2/64 seed pickup, local carry, throw and landing.
Both positive-offset controls preserve all64 selector/placement identities and
all65 loaded model payloads; each has72 page observations and74 model checks.
No exits occur. The selected high-slot interaction gate is closed; broader actor
and item section persistence remains open.

A rejected actor0 distant-route control exposes an unchanged native64-entry pool
search that loops when full at0042AA5C..0042AA7E.196 CPU-clock IP samples, a complete
pool capture and192 original-code cases agree. No pool patch or cause beyond the
observed full-pool condition is claimed. The carry word is a byte offset; zero's
additional branches make actor0 a confounded comparison control.

Source evidence narrows the prior770 unexplained memory windows to310:459 more
match long WAV spans and one matches initialized PC bytes. Six span regressions
and eight native initialization/camera cases pass. Implementation sources are
unchanged. [[PC Large-Level Engine Roadmap]] retains full reference provenance,
section persistence, pool/capacity policy, budgets/coordinates and total-memory gates.

All seven private copies are CLOSED. Normal154936 remains open;721 normal files,
saved Blender,760 bank files and all569 EXP011 artifacts remain exact. Normal exit
unchanged; no external live writes or debugger stops. Latest:
[[2026-09-08 - Codex - High-slot interaction and native pool limit]]. Older banners
below are historical checkpoints, including EXP011's then-remaining770 candidates.


## Milestone 4: native contacts repaired and in-process page loading, 2026-09-08

[[EXP-20260908-006 - Native actor and camera contact repair]] separates all64 native actor selectors from camera65 in a66-record table.
The chunk/arena compiler installs the guarded repair;3960 native movement calls
and240 camera-wall comparisons preserve original results. Hardware27-selector/
20-plant checks pass. The64-seed interaction route remains unaccepted; assignment
alone does not prove high-slot live movement or complete actor lifecycle.


All four private hardware arms are closed. Normal154936/start2024608/group154693
remains open, with721 normal files, saved Blender and760 bank files unchanged.
No external live writes, debugger stops, originals or other-worktree changes.
Selected `make check`:1467 tests pass in169.86s. Latest session:
2026-09-08 - Codex - Native contact repair and page loading. Older banners below are historical.


## Milestone 4: compact native storage and persistent CPU rendering, 2026-09-08

[[EXP-20260908-005 - Compact terrain storage and actor selector limits]] removes
305,340 managed geometry bytes from the current resident DAT/TERRAIN files.
Compact native loading preserves scene/source identity and passes1,750 exact
movement comparisons. Persistent CPU rendering passes36 frames over three
camera cycles with real mesh file loads/unmaps and corrupt-load rollback.
Driver calls remain stubbed; total game RAM and live integration are unaccepted.

Native actor assignment16 conflicts with camera slot16; assignment24 exceeds the
initialized table. The normal packet has9 selectors, the earlier crowd packet27.
The new offline guard rejects populations above15. Earlier crowd observations
remain finite passes and do not prove all later seed movement safe. Entity
reinitialization does not clear cached contacts. [[PC Large-Level Engine Roadmap]]
keeps Milestone4 open for actual frame/reference closure, combined live loading,
persistent state, wider coordinates and long hardware acceptance.

Normal game154936/start2024608/group154693 remains open; passive position changed
while no agent input was sent. All721 normal files, saved Blender and760 banked
files remain exact. No launch, close, external memory write, debugger stop or
other-worktree change. Latest session:
[[2026-09-08 - Codex - Compact terrain pages and native selector limits]].
Selected `make check`:1,344 tests pass in158.09s; the frozen report records the
selection and evidence hashes. Older banners below are historical.

## Milestone 4: native collision page transitions verified offline, 2026-09-08

[[EXP-20260908-004 - Native terrain page residency]] adds guarded collision-page
publication and conservative movement readiness. Native landings verify all24
initialized contact slots; cached contacts prevent retirement.1750 prescribed
movement steps across six corridor legs per executable and24 native query
comparisons match resident controls, including movement instruction counts.
Actual page files load, retired pages unmap, and corrupt second-file loads roll
back staged allocation/publication. Dedicated collision mappings peak48KiB on
the route; the original full buffers remain resident, so no total RAM saving.
Twelve native CPU-renderer contexts also preserve exact geometry packets and
admissions with culled meshes unmapped; D3D calls are stubbed and live/GPU
frame lifetime remains open.

Milestone4 remains open for complete actual actor/query/reference inventory,
live frame/file IO integration, persistent state, wider coordinates and long
hardware acceptance. Control-only straight-line stalls and numeric-census false
positives remain recorded. The normal game/project and banked wilderness remain
unchanged; no live input, memory write, launch or debugger stop was needed.
Latest session: [[2026-09-08 - Codex - Native terrain page residency]].
Selected `make check`:1313 tests pass in157.28s, Vault0 errors/8 existing
warnings and tracked audit0 violations. EXP-004 freezes47 private artifacts;
fresh preservation checks match721 normal files, saved Blender and760 bank files.
[[PC Large-Level Engine Roadmap]] remains the canonical gate list. Older banners
below are historical.

## Milestone 3: representative headroom measured, 2026-09-08

[[EXP-20260907-028 - Representative update and render headroom]] adds8978 contiguous paired-route frames and2342 active-mushroom frames. Both builds complete two four-section loops without
transition/death; whole update+render/present p99 is0.4921/0.6591ms, maximum
1.5033/1.6506ms, before native pacing. One native seed opens into type5 and
repeated mushroom contacts/bounces pass; collector peak26, batch vertices499.
All four chunks and170 models remain exact. The old EXP026 timer covered only
render/present; its note/report now state the narrower boundary.

The normal visual-detail project and721 files are unchanged; wilderness remains
banked. Measurement checkpoint passed, **Milestone3 remains in progress** for
broader simultaneous actor/candidate density and a consolidated acceptance gate.
Check wider coordinate arithmetic before extent grows. [[PC Large-Level Engine Roadmap]].

Normal game133402/start1484892, group133160 is OPEN at spawn on`:2`;
controller `work/experiments/EXP-20260907-028/handoff-detail/control.py`.
EXP027 game119064 and EXP028 diagnostics128004/130413 are CLOSED. Protected
other-agent tree/session remains untouched. Latest session: [[2026-09-08 - Codex - Representative frame work and active plant contact]].
Selected `make check`:1219 tests pass in151.45s, Vault0 errors/8 existing
warnings and tracked-file audit0 violations. Earlier runtime/status banners below are historical.


## Milestone 3: native lifecycle and controlled traversal, 2026-09-07

[[EXP-20260907-027 - Native respawn cycles and exit-aware traversal]] verifies six native death/respawn cycles, three each on control and
visual-detail copies, with constant arena roots/cursors and all 170 sampled model
payloads intact. Both normal builds complete all four terrain sections and return
to spawn; each then completes the authored exit and reloads Level01 with exact
resident chunks/models. Ordinary routes explicitly avoid the exit. One initial
instant-death fixture reached GameOver and is retained as rejected evidence.
Damage-fixture respawns can still take boundary damage; no safe-hazard claim.

The saved `work/level-projects/moonlit-cliffs-visual-detail/level.blend` is unchanged:
7244 encoded chunk vertices/9249 faces, 2365 collision triangles, 15 clovers and 28
mushrooms. The wilderness remains banked. Stage 3 remains **in progress** for
representative camera/frame-work headroom and broader actor/candidate endurance;
wider coordinates need validation before extent grows. Loop times are not GPU
or frame-time evidence. [[PC Large-Level Engine Roadmap]].

Normal game 119064/start1237365, group 118809 is OPEN at spawn on
`:2`; controller `work/experiments/EXP-20260907-027/normal-detail/control.py`.
EXP026 game 100253 and all four preceding EXP027 games are CLOSED. Other-agent
aqua-glow worktree/processes remain untouched. Latest session: [[2026-09-07 - Codex - Native lifecycle and controlled traversal]].
Selected `make check`: 1219 tests pass, Vault0 errors/8 existing warnings and
tracked-file audit0 violations. Earlier banners below are historical.

## Dedicated storage and terrain chunks accepted for the earlier layout, 2026-09-07

[[EXP-20260907-023 - Dedicated asset arena and terrain chunk acceptance]] repairs the reproduced model/scratch overlap with a dedicated 8 MiB
PE region and two native base changes, preserving relocation and an exact inverse.
The earlier pebble layout now uses four terrain chunks; the 4.85× wilderness
remains banked. All 170 model payloads match native controls in three hardware
arms, including a 3094194-byte stress load. Normal final build contains no padding.
Shared-control movement visits all four collision sections; the main sampled
route has a maximum floor gap of 117 world units and two unfinished waypoints.
The user reported overlapping manual input, so route timing and obstruction
causes are not established. Native and model-memory checks remain valid.
No arbitrary stability/performance or all-level claim is made.

**Gate audit, EXP-024:** EXP-20260907-024
confirms both original milestone gates against fresh builds, source/native checks,
and read-only live memory: 1,197 tests, two identical Blender builds, 124 floor
crossings, 24 wall pushes, 12 renderer contexts and all 170 models. Larger-load
history is independently rechecked. Stage 3 measurement may begin; full timed
live traversal and broader stability remain outside this bounded acceptance.

Current project: `work/level-projects/moonlit-cliffs-chunks-arena/level.blend`.
Current game 19999/start 161865/group 19764 is OPEN in EXP-023/preview-03, actual
EXE431ec953b67bd3233f8fa58e7a22edbfabaeb153e3ee322d760c45f2a44c7d8f.
Both preceding EXP-023 arms are CLOSED with clean switch audits. EXP-021 game 716312
and all its recorded identities were already absent before this task's launch;
its exit cause is unknown. No live writes or PS1 consultation.

The newly named [[PC Large-Level Engine Roadmap]] owns these four milestones.
Stages 1 and 2 have bounded acceptance; stage 3 density engineering is now in
progress in EXP-025. Its expanded compiler limits remain bounded and its full
acceptance is pending. Earlier lifecycle/status banners below are
historical. 2026-09-07 - Codex - Dedicated asset storage and chunk acceptance.
Latest session: 2026-09-07 - Codex - Verify first two engine milestones.


## Trunk and character geometry repair, 2026-09-07

[[EXP-20260907-017 - Trunk scenery and character storage overlap repair]]: scaled sampled trunk and15 editable clovers are saved in
`work/level-projects/moonlit-cliffs-trunk/level.blend`. Oversized first build
corrupted Flik geometry by overlapping renderer scratch0076F9A0..AF; native
nine-pose causal replay confirms it. Shared meshes save56376 bytes;1138 selected
checks pass and live model bytes remain exact. Corrected643454/start8723576,
group643206 OPEN; OG628920 and rejected634669 CLOSED with clean switch audits.
User accepts appearance and now requests walkable ground through the grass
frontage to the trunk; that follow-up is active. Older runtime banners below
are historical. Work remains uncommitted.

## Original game and current trunk sample, 2026-09-07

2026-09-07 - Codex - Original game and trunk sampling: user-requested OG Anthill628920/start8485507/group628682 OPEN;
fixed mod625497 CLOSED with clean switch audits, its files/source preserved.
Original content plus accepted startup-only EXE1e1d5099...a9c41f; resident/code
checks pass. EXP-016 samples the user's bark wall: scene5/6 native/live projection
matches, five complete adjoining meshes467 vertices/358 faces saved privately.
Whole-tree/canopy completeness and reusable textured/collision assembly remain
unresolved. No gameplay keys or live writes. Earlier lifecycle banners are historical.


## Current collision fixes, 2026-09-07

[[EXP-20260907-014 - Cliff seam and phantom seed collision repair]] saves the requested floor-fall clip and repairs two confirmed defects:
cliff walls now share floor X/Z edges; a guarded64-bit actor distance check
blocks phantom pushes from extreme-position seeds.81 affected tests and49/49
native cliff pushes pass; exact captured seed velocities reproduce before and
vanish after the patch. Nearby seed/stomp/plant creation remains working.
New625497/start8349368/group625261 OPEN, old600258 CLOSED after clean switch
audits. Both fixes and terrain are verified resident.40s user-controlled play,
2643 samples: max floor gap138world, no sample beyond512, max horizontal component2068.
No agent keys in new game or live writes. Saved clover project/build uses the
repaired compiler; assets/private evidence remain in work/. Changes uncommitted.
2026-09-07 - Codex - Floor fall and phantom collision fixes records evidence and remaining actor-lifecycle/all-corner limits.
Earlier current-runtime and unresolved-jolt banners below are historical.


## General render distance, 2026-09-07

[[EXP-20260907-010 - General render distance preview]] installs 1.5× original
terrain/scenery groups (1728/2496), with all721 game data files unchanged.
48 tests, actual Blender Build/roundtrip, eight native primary-frame packet
checks and complete resident data/code/lookup checks pass. [[PC general render distance]]
records tuning and restoration. User says this looks good; further expansion
is explicitly deferred. 2× has initial offline evidence only, not broader live
or performance acceptance. No banking request; source remains uncommitted.
Historical game588527/start7780125, group588291 is CLOSED for EXP-011; old550760 CLOSED after clean switch
audits. EXP-010/preview-01 owns stage/controller/prefix;14 identities account
seven generic rows/one sink. Editors537419/513914 preserved. No agent keys or
RAM writes in the new session. Earlier runtime banners are historical.

## Prior terrain test-area handoffs, 2026-09-05 to 2026-09-06


> **Historical initial mushroom authoring:** [[EXP-20260906-014 - Net-new scenery mushroom instances]] built a three-prop offline control after the EXP-013 OG switch.33 new/831 terrain tests and bounded native loading/contact/draw gates passed with the documented floor108 discriminator. EXP-016 supersedes its pending preview and deferred banking instructions with the user-approved six-prop layout.


> **Active grass authoring handoff, 2026-09-06:** [[EXP-20260906-006 - Perimeter barriers and original foliage reference]] now has a file-loaded first grass preview, with user confirmation that Flik is not falling off. It remains OPEN as game158153/start1883339, group157921, display`:2`; OG reference game is CLOSED. Off-screen file census34 placements/31 meshes yields381 filtered tall-grass templates; a less repetitive visual-only successor uses202 distinct templates, preserves both collision files, and is UNLAUNCHED.62 affected/72 focused tests and original-PC relocation/stream pass. One synthetic lower-ramp straight-release case remains numerically unsettled; steered return succeeds. No R2q/full suite or Git. Earlier active banners are historical. 2026-09-06 - Codex - Reusable grass and off-screen variety.


> **Active terrain reference, 2026-09-06:** [[EXP-20260906-006 - Perimeter barriers and original foliage reference]] supersedes earlier active-preview banners. EXP-005 passed its corrected native gate10/10, ran as a user preview, and is now CLOSED with assets preserved. A clean switch launched original Level01 assets in isolated OG game131707/start1699630, group131459, display`:2`; it remains OPEN for the user. Passive foliage reference: XYZ(292407,-31849,537453), facing979, related angle976, screenshot and camera saved without input/focus/writes. Exact foliage render/barrier mapping remains open. Earlier perimeter trial accepted neither winding (14/32 positive,0/32 negative); no candidate launch. No capture-time tests, R2q/full suite or Git. See the experiment and [[2026-09-06 - Codex - Original foliage boundary reference]] for evidence and lifecycle limits.


> **Active terrain continuation, 2026-09-06: EXP-20260906-005 is offline only.** [[EXP-20260906-005 - Isolated authored terrain and platform spawn]] builds a separate stripped landscape: 36 authored cells, 807 faces, old scene draws/collision streams deactivated, private executable spawn X/Z (192000,448000). 53 affected and 72 focused terrain tests pass; 9 native arms pass, but the new spawn-test setup omitted unchanged heading data and needs the disclosed correction. Overall native gate is not green and no launch occurred. EXP-004 remains the untouched live preview; its current pose is not asserted. No R2q/full suite, Git or live-memory actions. Earlier active-preview banners below are historical.


> **Active terrain handoff, 2026-09-06: EXP-004 clearance trial live.** Earlier latest/active banners below are historical. [[EXP-20260906-004 - Wall clearance comparison and offset trial]] shifts only20 ramp-side collision groups outward48 stored units (1536 world units); render, floor and original collision stay unchanged.69 affected tests pass, both native arms pass, focused terrain gate72/72 in26.68s. User visual overlap and lower-corner/clearance-strip acceptance are still pending; not a universal wall radius. EXP-003 preview is closed and its fixture retained as control. New game **71867/start1283745**, group **71598**, left at the normal Level1 start. No R2q/full suite, Git operations or commit. [[2026-09-06 - Codex - Wall clearance trial]]; `reports/terrain/EXP-20260906-004.json`.


> **Active terrain continuation, 2026-09-06: EXP-003 live; visible wall clearance open.** Earlier latest-update banners below are historical. This entry supersedes correction-pending/unlaunched EXP-003 and live-EXP-002 status. [[EXP-20260906-003 - Solid ramp sides and ground contour trim]] is file-loaded in Level 1. User confirms side blocking but Flik partially disappears into/behind a wall when approached. Keep geometry as control; compare original/authored stop clearance and view dependence before padding. Ground-join trim efficacy is separately unconfirmed. Corrected affected tests: **138 passed in 0.56 s**; prior five-file gate **72 passed in 26.29 s**. No R2q/full suite, Git operations or commit. Game **42212**, start **1016972**, group **41955** deliberately remains open. Evidence, process accounting and native-test limits: 2026-09-06 - Codex - Solid ramp preview handoff, `reports/terrain/EXP-20260906-003-runtime.json`.


> **Latest terrain runtime update, 2026-09-05:** EXP-007 OG control is open: retail Level01, PID/start `313931/10570967`, group `313689`, isolated `og-preview-02` prefix. The earlier EXP-006 preview is closed. Earlier EXP-006 live-session descriptions below are historical and superseded by [[EXP-20260905-007 - Retail position control and missing floor footprints]]. The OG four-second Up control retained 301 RAM samples with no sampled NextLife trigger; active retail floor omissions in authored source 99 are confirmed at selected footprints, not yet by a full earlier-fall replay.


# Current State

## Mushroom and foliage research checkpoint, 2026-09-06

Commit `afd3f81cfe55b112c61019de51206794473d7e3d` banks [[2026-09-06 - Codex - Mushroom and foliage research checkpoint]] before further research, as requested by the user. Its empty worktree was verified before EXP-008. Pre-commit non-R2q `make check`:3990 passed/one unchanged known R2p failure in442.79s; fast hygiene gates pass. Protected stash/private evidence and the open repaired-variety preview are preserved. Earlier uncommitted descriptions are historical.

## Earlier 2026-09-06 terrain foliage checkpoint

The following records the earlier bank, not the current runtime. EXP-007 has since resolved the mushroom mapping/repair and launched the banked varied LEVEL.DAT with the two-byte PLANTTER fix. Its latest banner and session note supersede the pending/unlaunched/no-live-game statements here.

- Banking validation: the focused five-file terrain gate passed 72/72 in 26.98 seconds and the nine newly authored terrain/foliage test files passed 300/300 in 0.66 seconds. A two-worker, repo-local `make check` with `tests/test_r2q*.py` deliberately excluded reached 3950 passed and one unrelated R2p failure in 435.24 seconds; the same test failed alone in 0.16 seconds, and its test plus both imported R2p implementation files are unchanged from the parent checkpoint.
- EXP-20260906-006 produced an isolated playable platform/ramp with authored perimeter collision and reusable original-PC grass geometry. The first live grass arm was visually repetitive but the user confirmed that its boundary collision prevented Flik from falling off. A more varied foliage arm is built offline under `work/copies/EXP-20260906-006/grass-variety-fixture`; it uses 202 distinct selections across 259 placements and has not been launched.
- The EXP-006 preview is closed. The post-close `make session-audit` was clean after a scoped shutdown of its recorded process group and exact Wine prefix; no live game is being handed off.
- A newly reported regression is banked as planned EXP-20260906-007: seed-state collision works, but after the seed opens into a mushroom the user can stand inside it and jumping on it does not bounce Flik. This is a user runtime observation, not yet an instrumented trajectory.
- The leading static clue is bounded: the isolated-area builder empties tag 6/7/8 collision payloads and unlinks high collision streams in both `TERRAIN.ALL` and `PLANTTER.ALL`. That can explain a missing opened-plant template, but it does not by itself explain why the seed state still collides. The next work must map the mushroom state transition to its exact PC object type/template before restoring anything.
- Continue from [[EXP-20260906-007 - Plant-state collision regression]] and 2026-09-06 - Codex - Terrain foliage and plant collision handoff.

## 2026-09-05 whole-Level01 collision audit complete

[[EXP-20260905-008 - Whole-Level01 collision and render coverage audit]]
confirms source 99 is the only changed collision payload among all 189 records.
Its 134 original active cells were replaced by 14 authored cells; 7,147 other
active cells and all 262 barrier segments are unchanged. Only static render
reference 160 changes, but its footprint differs from source 99's collision.
The earlier fall footprint retains mesh 213 with no authored floor candidate.
Next: a non-destructive collision/render integration plan preserving originals,
then exact native-instruction fall and exit/landing/return proofs. No assets,
game state, tests or Git were touched; the prior OG session was left alone.
Report: `reports/terrain/EXP-20260905-008.json`; private offset inventory and
map: `work/experiments/EXP-20260905-008/`.

## 2026-09-05 tiled terrain preview open for the user

EXP-006 preview was open; it is now closed for EXP-007 in Level01 after the user requested switching over.
The old EXP-005 game closed with clean post-close/prelaunch audits. Full new
mesh, unchanged collision and the trailing-data pointer are verified read-only;
the captured spawn view shows repeated ground and warm walls. Leave the new
game309701/start10311098, group309445, display`:2` open. Keys are released.
No movement sweep, user aesthetic approval or general mesh rule is claimed.
No code/assets changed or tests rerun during this launch. Next: user feedback.
See 2026-09-05 - Codex - Tiled terrain user preview and
`reports/terrain/EXP-20260905-006-runtime.json`.

## Earlier 2026-09-05 tiled terrain candidate, offline bank

[[EXP-20260905-006 - World-scale terrain tiling and checked mesh growth]] adds
atlas-local 512-stored-unit tiling and checked render growth: 324 vertices,
524 triangles, collision byte-identical. Original PC relocation preserves the
end-relative trailing data; 34 new tests and the 185-test terrain gate pass.
At the offline bank, no R2q/full suite or runtime action occurred and EXP-006
was unlaunched. The later user-authorized preview above supersedes that state.
Next offer a normal file-loaded preview switch, then inspect texture scale,
seams, depth and performance before composing a different connected layout.
This is not general repacking or live visual acceptance. Banking details:
[[2026-09-05 - Codex - Terrain texture tiling and mesh growth]].

## 2026-09-05 combined box wall material preview

[[EXP-20260905-005 - Original wall texture regions and colour inputs]] now
includes the user-requested combined box preview: original wall UV region plus
a donor-derived warm vertical gradient on24 wall quads. All face XYZ,
top/ramp/deck appearance and collision remain unchanged.33 affected tests and
the151-test terrain-only gate passed; no R2q/full suite. Original comparison
game CLOSED cleanly; combined material game OPEN for the user, controls
released: group299129, game299378/start10038768, display`:2`.
User accepted the combined wall appearance. This increment is included in the
terrain tiling checkpoint; EXP-006's separate live visual acceptance is pending.

## Earlier 2026-09-05 original wall material investigation

[[EXP-20260905-005 - Original wall texture regions and colour inputs]] finds
different page-0 UV regions and warm varying vertex colours on nearby original
steep faces versus EXP-004's uniform floor-region assignment. Exact screenshot
localization remains open at exact face level. A later user-authorized original
runtime now supplies a confirmed wall view and read-only extracted page pixels:
the floor and wall regions differ before vertex tinting. The test copy was
closed and a fresh original-assets game was opened for the user
(group277987, game278243/start9423624), then closed for the combined preview
above. The uniform 3/5 draft was not selected or applied; its control tests now
pass. No universal material-edit acceptance or R2q/full-suite run is claimed.

## Playable ground-ramp-box area, 2026-09-05

[[EXP-20260905-004 - Playable ramp and box area]] completes the user's chosen
composition step: an isolated deck, gentle east ramp and banked4x4 box top.
Six paired original-PC routes and two normal-input live ascent/descent cycles
pass, plus jump/landing and step-off. The terrain-only gate passes118/118 in
26.51seconds; no R2q/full-suite run. All test runtime processes/sinks are closed.
Play with `work/copies/EXP-20260905-004/play.sh`; rebuild with
`scripts/terrain-play-area.py`. Next is user play/feedback, not another box proof.
This elevated local area does not close EXP-003's separate prop/source100 question
or establish arbitrary-level/all-view rules. Report and exact limits are in the
experiment note; DEC-242 records the composition-first choice.


## User-directed terrain-only validation, 2026-09-05

The user clarified that these terrain tests must not rerun R2q. The once-started
full `make check` trial was cancelled with SIGINT after 360.849 seconds wall time;
pytest reported 885 passed and the one known pre-existing R2q historical SHA
mismatch in 359.80 seconds before interruption. All test processes exited.
There is no completed full-repository verdict and no serial/full-suite retry.
The exact terrain gate passed 72/72 in 27.66 seconds; the 27 added regressions
passed in 6.44 seconds. This session uses those terrain-only gates, not a claim
that the repository suite passed. See `reports/terrain/EXP-20260905-003-validation.json`
and [[EXP-20260905-003 - Shared floor return discriminator and stitched patch]].


## 2026-09-05 shared-floor return follow-up

[[EXP-20260905-003 - Shared floor return discriminator and stitched patch]]
supersedes the EXP-005 next-target status below. The return fall is reproduced
by original PC instructions and a fresh rigid runtime control. A six-cell connected
star with deliberately paired LEVEL.DAT heights passes 16/16 isolated modeled
boundary directions and two normal-input live out/back cycles plus jump/landing.
Retail and stitched both pass 13/16 complete-scene modeled routes; the same three
are prop-confounded. A live source100 extension stalls beside a rock before the
seam and is not a pass. Next: prop-aware source100 comparison and broader finite
coverage, not a universal geometry rule. Rigid EXP-005 and EXP-006 remain controls.

All games are closed; unrestricted session audit is clean. Initial sandbox audits
missed an older game, subsequently closed with explicit user permission. DEC-241
records the bounded repair. Final gate/full-suite duration and result, audits and
remaining failures: `reports/terrain/EXP-20260905-003-validation.json`.


Canonical sequencing and milestone gates live in [[Project Roadmap]]. This note
records only the present snapshot.

## Terrain diagonal/movement checkpoint banked — 2026-09-05

The completed EXP-011/EXP-001/EXP-002 diagonal and finite movement/view work is
banked under the expected local commit subject
`terrain: bank diagonal and movement validation`. The public reports and
source/tests are tracked; their exact private artifacts and authored fixture
files are preserved in a verified archive under `work/snapshots/`. The next
bounded target is now prop-aware broader seam coverage after EXP-20260905-003's return repair. See
[[2026-09-05 1126 - Codex - Terrain diagonal and movement checkpoint]].

The focused terrain/deck suite passes 72/72. The required `make check` runs for
11,089.48 seconds and reaches its terminal summary, but `/tmp` quota exhaustion
causes a late cascade: 4,090 passed, 166 failed and 42 errors. Clean-storage
discriminators leave the unchanged R2q-029/031 line-5899 expectation mismatch;
the affected fake-process modules pass 110/110 outside the workspace sandbox.
No green full-tree gate is claimed. Exact validation is in
`reports/terrain/terrain-20260905-bank-checks.txt`.

The banking `make session-audit` is clean: no game/Wine process, session ledger,
or audio sink remains. EXP-002's statement that game 46701/1147812 remained
paused is its last experiment-time observation. The current audit cannot
attribute when or how that session closed. No runtime action occurred during
the bank.

## Box movement/view regression expanded — 2026-09-05

[[EXP-20260905-002 - Box movement and occluding-view validation]] runs two
sequential file-loaded arms while preserving the user's paused failure.
Five valid reversal sweeps yield 518 grounded state samples and 107 captures;
every sampled reference point stays outside the tested wall. Jump/top/step-off
contact also passes. A new paused occluding-edge diagnostic has no analytic
top-before-actor inversion among 485 blue samples with reconstructed coverage.
The original-location south route overshot and was rejected; an explicitly
guarded south retry passes in the stationary placement only. Keep this limit.
Both research instances closed with audits exactly matching the original seven
user processes/sink. At experiment close, original game 46701/1147812 and its
mesh/collision/pose/camera remained unchanged and paused. No live memory writes
or debugger control occurred.
DEC-241 records EXP-20260905-003's bounded stitched-floor repair; universal geometry
and all-view guarantees remain open. See
[[2026-09-05 1042 - Codex - Box movement and occluding views]].

## Box-edge diagonal comparison verified and restored — 2026-09-05

[[EXP-20260905-001 - Box top diagonal live comparison]] completes EXP-011's
unchanged plan under fresh explicit four-write/brief-stop authorization.
The six residual fragments disappear with alternate top diagonals and return
with the finer control; all 255 prior fixes remain hidden. All 15 captures
match measured player/contact/camera state. Both restored controls match all
3,575 ROI pixels exactly, including the previous day's EXP-010 controls.
The original six-quad mesh was restored with collision unchanged, and the same
game remained paused at comparison close. Final TracerPid 0, no stopped threads, identical accounted
seven-process/sink audit. The four-write authority is consumed; do not rerun.
Its next movement/view step is now completed at the bounded scope above;
the separate EXP-005 shared-floor return defect follows. No general mesh rule
or whole-layout acceptance.
See [[2026-09-05 0903 - Codex - Box diagonal runtime verified]], DEC-238.

## Box-edge diagonal candidate preparation — 2026-09-04

[[EXP-20260904-011 - Box top diagonal edge discriminator]] reuses the saved
paused failure. Rotating the 16 finer top quads to the opposite diagonal,
with identical vertices/collision, wins all 259 prior analytic comparisons
and preserves all 255 earlier corrected samples offline. Normal 4x4 wins
253/259; two denser grids regress an old sample. No general mesh rule follows.
33 tests and five synthetic operator cases pass. At preflight, the same paused
game, pose, mesh and seven-process/sink audit were verified read-only.
A four-write control/alternate/control/original comparison was prepared;
the subsequent authorized execution and restoration are recorded above.
See [[2026-09-04 2207 - Codex - Box edge diagonal candidate]].

## Terrain research checkpoint banked — 2026-09-04

The user requested banking the completed terrain/collision research.
[[2026-09-04 2057 - Codex - Terrain research checkpoint]] records the
local Git checkpoint, validation receipts and verified private evidence archive.
All 222 terrain tests pass. A serial rerun clears 59 quota-affected failures;
one pre-existing R2q 029/031 hash expectation still fails. The full `make check`
was run but interrupted, so no complete green suite is claimed.
This preserves EXP-002–010 without closing their documented edge,
view, floor-boundary or general-authoring unknowns. No new game action is part
of the bank; the last verified paused/restored handoff remains below.

## Paused subdivision comparison verified and restored — 2026-09-04 20:47

The user reports residual leg fragments after moving against EXP-008's box.
[[EXP-20260904-009 - Paused side-view depth interpolation]] preserves that
already-triggered state and finds strong evidence for large-face depth
interpolation. The user then explicitly authorized the prepared live swap and
restoration. [[EXP-20260904-010 - Paused subdivision live comparison]] removes
all255 prior inversion-point fragments and brings them back on restoration;
all3,575 comparison-region pixels restore exactly. All9 captures match measured
player/contact/camera state. Six other boundary samples remain uncertain;
all-view repair and a general subdivision rule remain open.

Current position`(163024,-102401,509900)` is on the lower deck just outside the
box's side. Both authorized1,078-byte writes completed with verification and
brief frame-limiter stops/read-only register inspection. The original zero-offset
six-quad mesh is restored; the same game remains paused. Final TracerPid0,
no stopped threads, unchanged loaded collision and identical process/sink audit.
No gameplay input or restart occurred. The candidate is retained offline.

## Block depth-offset correction, bounded result — 2026-09-04

[[EXP-20260904-008 - Block depth offset runtime comparison]] confirms the inherited object byte18690
caused the demonstrated lower-leg/shadow leak. Removing8→0 hides it; restoring8
reproduces it. All16 stationary captures match measured player/contact/camera
state. Smaller faces are not needed for this bounded correction.197 focused
tests pass. The user's later side-view report above limits this to a partial
repair. General level layouts and EXP-005's return-fall defect remain open.

## Corrected user game open — 2026-09-04 20:21

`USER-20260904-deck-depth-play-001` is open in Level01; the user has moved and
paused at the residual defect above. It has the original box geometry/collision and only its depth byte
corrected. Game46701/1147812, group46458, display`:2`, sink`ablpc_mute_46458`.
Loaded data and ownership are verified in
`work/experiments/USER-20260904-deck-depth-play-001/handoff.json`. Leave it open
for the user. The previous game40214/965017 and all six EXP-008 scientific/
rejected arms closed with clean audits. Historical mappings/R2q are unchanged.

## User-reported floor failure and replacement testbed — 2026-09-04

The user reports that returning across EXP-005's raised spawn patch makes Flik
fall through the floor. Its coordinate/pixel effects do not establish reliable
traversal or complete grouping; the exact defect is unresolved. EXP-006 supplies
a separate flat deck and obvious solid block. Original top/side removal controls
and two live jump-off-return cycles pass;188 focused tests pass. The user
subsequently confirmed block contact and reported a visibility defect (EXP-007).
This does not repair EXP-005's shared edges.

## Current terrain/collision priority — 2026-09-04

The original-instruction route now works with real collision data:
[[EXP-20260904-002 - Retail collision admission and separate XZ barriers]]
loads Level01/Level03 plus PLANTTER, builds original bounds/buckets, and runs
the full movement coordinator at synthetic nongrounded positions. Level01
source87/cell1000 is admitted and deflects X/Z movement; removing descriptor87
removes the response. Separate kind`0x101` source179 supplies X/Z barriers with
the same measured response at three Y values. Plant templates and reserved
dynamic destinations are disjoint from static terrain in both tested loads.
Those EXP-002 results narrowed KU-080/KU-081; EXP-005 below now also narrows
visible-ground KU-079. None of the three is fully closed.

**Barrier grammar and grounded tests are now complete at the bounded offline
scope:** [[EXP-20260904-003 - Barrier grammar and landing-seeded grounded movement]]
adds a lossless kind`0x101` reader covering65 strips across18 terrain files,
108 original-collector comparisons, and ten movement/control cases whose
ground contact is established by original landing instructions. Blocks carry
16 segments with interleaved bounds and a sentinel tail; collection caps at
16 segment pairs. Both real obstacle families respond from grounded entry.

**First live authored-barrier proof is complete:**
[[EXP-20260904-004 - Translated barrier live collision proof]] relocates one
four-segment barrier into the natural spawn walking path. The live loaded
payload matches the edited file; the edited trajectory skirts its footprint,
while a restored-file control crosses it from identical starting XYZ. Only
TERRAIN.ALL differs among 2,251 files compared excluding the game log.
A bounded translation prototype and 174 passing focused tests are retained.
The user also manually confirmed the collision after testing the fresh play
session; see [[2026-09-04 1909 - Codex - User barrier play session]]. This is
user acceptance of this barrier, not a broader format or independent audit.

**Raised floor and visible-ground pairing now have bounded live proof:**
[[EXP-20260904-005 - Raised floor and visible ground pairing]] changes six floor h0 fields by−64
stored units. Original landings/walks and the live spawn rise by2,048 world units;
41 live samples at25 matched X/Z positions retain that exact Y difference.
Normal jumps land on the edited group. A17-vertex LEVEL.DAT companion changes
visible ground with identical actor/camera values; restoring LEVEL.DAT restores
all21,630 pixels in a static ground region. Live scene/object pointers and full
vertex arrays match the staged edits.177 focused tests pass.

**Next (DEC-235):** retain the verified subdivision regression, investigate its
remaining edge samples and validate other views before general layout work.
Keep DEC-233's explicit offset choice and regression;
then extend EXP-20260905-003's prop-aware seam coverage. Keep the
synthetic deck separate from the original slope patch; general grouping,
normal/bounds rebuilding and terrain deformation remain open. Reuse completed
loader/barrier/format work. EXP-002–006 have no independent audits. R2q remains
banked with its previous incomplete final gate. See
[[EXP-20260904-006 - Flat deck and solid block test]].

## What currently works?

- The project workspace, shared Vault, evidence templates, ingestion workflow, PE triage, and Ghidra headless export workflow exist.
- **Agent automation tooling (2026-08-17, fixture-validated only).**
  [[Session control plane]] implements the live-session recipe as
  `scripts/game-session.py`, `game-memory.py`, `send-keys.py`, and
  `wait-for.py` over `scripts/session_lib.py`, with a per-session ownership
  ledger at `dynamic/wine/RUN-SESSION-<stamp>/session.json`, and a same-process
  memory checkpoint (`game-memory.py snapshot`/`restore`) that saves and
  reloads the `.data` game-state section within one session — the durable
  cross-launch savestate (CRIU) is blocked here by the `ntsync` driver, shown
  by `criu-feasibility.py`. `game-memory`'s read/save/restore path is now
  **partially live-validated** against the running game
  ([[EXP-20260817-188 - Live game-memory read save restore validation]]): a
  full `snapshot`→change→`restore`→verify cycle reverted a real global
  exactly. `game-session`, `send-keys`, and `wait-for` have **not** run
  against the real game. `scripts/savestate-hotkeys.py` adds emulator-style
  in-game save-state hotkeys (grabbed on the game's nested display, F5
  save / F9 load by default); its key-grab was confirmed live on the
  running game, the interactive popup flow is its remaining acceptance test; live validation is CAP-010's acceptance test
  and until it passes, [[PC autonomous game control]] remains the authoritative
  procedure. On 2026-08-21 the user reported that save states do not currently
  work; this was not independently exercised in that session and is treated as
  an operational constraint, so the active R2p pickup does not rely on either
  save-state mechanism. [[Agent evidence and query tooling]] adds the offline half:
  `briefing.py` (mandated reading set ~272,994 tokens → a 4,615-token
  briefing), `ghidra-query.py` (0.07 s function lookup over the 7.7 MB export),
  `run-index.py`, `experiment-draft.py`, `claim-sweep.py`, a vault-lint context
  budget, CI with retained raw logs, and a pre-commit hook. 1,091 tests pass.
- **86Box GDB-stub build available (2026-08-17) — Gate-2 memory-access probe
  ready.** A GDBSTUB-enabled 86Box (interpreter core; `DYNAREC` forced off) was
  built from source (commit `628ce40`) in a disposable podman container and
  packaged as the git-ignored `tools/86box/86Box-gdbstub-628ce40.AppImage`
  (sha256 `7cd47fd1…`), distinct from and not replacing the untouched stock
  b9001. Its GDB stub is verified **compiled in and listening on `:12345`**,
  translating **guest-linear** addresses through the active-CR3 MMU with
  read/write/access watchpoints — the mechanism needed to read the game's Win95
  virtual globals (`0x00861C84` level, `0x0059D910` Flik position) host-side.
  This is the Gate-2 harness of
  [[Decision Log#DEC-20260817-147 - Build a GDBSTUB-enabled 86Box to prove Gate 2 memory access]]
  / `KU-077`; the actual 2A/2B/2C probe is blocked on the interactive Win95 OSR2
  + game install. It is a **debugger/RE build only**, not a determinism
  datapoint (Gate 1 stays PCem-st). See
  [[2026-08-17 2330 - Claude - 86Box GDB stub feasibility for guest memory access]].
- **Win95 OSR2 + A Bug's Life run in 86Box (2026-08-18).** [[86Box Win95 RE harness]]
  documents a reproducible headless 86Box machine (i430VX / Pentium-200 / S3
  Trio64V2 / SB16) on which **the real PC executable boots to its level-select
  menu on real Win95** at 640×480 DirectDraw. Built unattended (msbatch; only the
  OEM certificate number typed by hand) after solving a chain of blockers — the
  FAT16 2 GB partition limit, the Award boot order, a **missing MBR boot loader**
  (`install-mbr`), and the game's CD sentinel gate. The game is deployed to the
  HDD at `C:\PC\BUGS\` (extract-to-HDD, `DEC-20260818-148`) to bypass 86Box CD
  regression [#5432](https://github.com/86Box/86Box/issues/5432); with no CD drive
  present it loads locally and passes the `cd.txt` gate, matching
  [[EXP-20260811-004 - Wine launch and CD sentinel gate]]. The disk image is
  portable between the stock build (play) and the gdbstub build (Gate 2);
  `work/86box/launch-on-host.sh` opens it natively on the Fedora desktop. See
  [[2026-08-18 0330 - Claude - Win95 and A Bug's Life installed in 86Box]]. The
  build is a driven session, not a script (`KU-078`).
- **Gate 2A PROVEN — the stub reads AND writes the game's live guest memory
  (2026-08-18, James-accepted).** A **v6.0** `GDBSTUB=ON` build (whose `exec386`
  interpreter boots the machine where v7.0 master's did not; the recompiler is
  compiled but a `GDBSTUB` build never selects it at runtime — source-verified,
  see `KU-077`) attaches its GDB stub to the running game. Two fresh-context **James** audits independently confirmed
  it: the **read** is byte-exact vs on-disk `bugs.exe` at four live PCs, and the
  **write** reaches live, mutable, correctly-addressed guest RAM (overlap windows +
  a free-run test where the guest CPU itself overwrote a left-in value — ruling out
  image/echo/shadow). Load-bearing caveat: the stub is **fragile** (single-client,
  leaks sockets, malformed stop-reply breaks gdb ≥15 once degraded, wedges/freezes
  under *dozens* of connects) — connect sparingly, restart periodically, or patch
  it. This validates the [[86Box Win95 RE harness]] as a runtime RE tool. `KU-077`
  has the full evidence; open extensions: a clean watchpoint, and the 2C
  A/D-side-effect check.
- **Live gameplay read + KU-076 resolved (2026-08-18).** The Training level was
  entered from the menu (mouse-click to focus, `Return` to select) — it loaded to
  full playable 3D **with no `CONVPSXTPAGE8` crash**, proving that Wine-9.0 level-
  load fault is **environmental, not intrinsic** (`KU-076` resolved). In-level, the
  v6.0 stub read the live gameplay globals in-context: **level `0x00861C84` = 17**
  and **Flik position `0x0059D910` = (−22044, 15860, −19597)** (real signed world
  coordinates; both read `0` at the menu). Holding forward moved Flik and the
  position re-read as **(−12793, 11822, −6096)**, a delta matching the visible
  on-screen movement (`work/86box/logs/pos_a.png`→`pos_b.png`) — the stub reads
  **live, changing** gameplay RAM. Taken economically (≤8 connects/read). `KU-077`
  has the full evidence; remaining Gate-2 extensions: a clean watchpoint, and 2C.
- **Watchpoint path PROVEN + first forensic tuple (2026-08-18,
  [[EXP-20260818-001 - Watchpoint path and first forensic tuple for Flik position]]).**
  A hardware write-watchpoint on `0x0059D910` fired at the writing instruction:
  **CR3 `0x00454000` (ABL, verified), writer EIP `0x004ab889` (`mov [edx],eax`),
  old X `-4378` → new X `-4205`** — one store in a 4-dword vector copy (X,Y,Z,W),
  runtime disasm byte-exact vs on-disk `bugs.exe`. The mechanism works, **but** the
  stub is too fragile as a capture *transport* (retains watchpoints across unclean
  exits → "too many"; malformed `T` stop-reply crashes gdb ≥15; non-deterministic
  async `continue`) — so repeat-hit consistency and the `>4`-watchpoint test could
  not run cleanly. Decisive for the recorder: build the write-trace as
  **emulator-side C instrumentation** (hook `mem.c` writes), not gdb-watchpoint
  capture. Input recipe for driving the game headless (PointerRoot focus, held
  `Return`/`Space`) is in [[86Box Win95 RE harness]].
- **Flight recorder Phases 0 + 1 — PASSED, James-accepted (2026-08-18).** Per
  [[Decision Log#DEC-20260818-149 - Build the runtime flight recorder as emulator-side C instrumentation, not gdb watchpoints]],
  a C write-trace was patched into the v6 86Box build
  (`tools/86box/patches/86box-v6.0-ablrec.patch`): it hooks the byte/word/long
  write accessors, keeps each watched page off 86Box`s fast-write cache
  (`writelookup2`, via `gdbstub_watch_pages` + a gated `addwritelookup`), and dumps
  a ring buffer on `SIGUSR1`.
  **Phase 0** ([[EXP-20260818-002 - Flight-recorder Phase 0 write-trace]]) proved
  it reliably reproduces the EXP-001 writer **`0x004ab889 → 0x0059D910`** without
  gdb (plus the full writer set for Flik`s struct) at ~119 Hz.
  **Phase 1** generalised it to all widths and a configurable **range table** of
  4 globals (Flik pos, level `0x00861C84`, carousel `0x00599AF8`, NextLife
  `0x0059A5B0`); one in-level run captured **1473 records** with `cr3` per record
  separating 1437 game (`00454000`) from 36 boot writes, and surfaced the
  level-global writer `0x0043dabb` (`mov ds:0x861c84,esi`, sets it to 1). A
  fresh-context **James** audit independently reproduced every claim (dump records,
  the objdump `89 02` store + XYZW offsets, the cache-defeat mechanism, the benign
  `gdbstub_mem_access` no-op) and returned **ACCEPT**. Plan/resume:
  [[Flight Recorder]]. **Phase 2 (offline query tools) is also DONE** —
  `scripts/ablrec-analyze.py` (`who-wrote`/`timeline`/`writers`/`cr3-split`, with
  `--name` resolving each writer EIP to its containing Ghidra function + `objdump`
  instruction); it already named `FUN_00410100` as the writer that sets the level
  global to `0x11` (=17). Deferred to Phase 1b: the full `dump_mark()` RAM+frame
  bookmark package and qword writes. The built binary stays git-ignored under
  `work/86box/v6/`; the patch is the tracked source.
- **Replay-seeded static candidate for the berry-type variable (2026-08-18,
  KU-073 narrowed).** A deterministic PS1 interpreter input movie
  (`Hopper_white_berry_death`, 642 frames, anchor hash-verified) was replayed
  in the external DuckStation fork with an access watch on the PS1 equip
  marker; the captured contact-time arithmetic (`table[row*5 + marker]`, `+2`,
  cap 200, threshold 100) was translated into a static Ghidra-export search
  that located PC `candidate_berry_equip_byte` `0x0059D9A7` (written 0-4 by a
  pickup-kind `0x20`-`0x24` switch in the confirmed pickup path
  `FUN_00417720` and `FUN_004292C0`) and `candidate_berry_hit_accumulator`
  `0x00599B20[row*5+type]`, with `== 3`/`== 4` behaviour gates and a
  `0x0059F500` mirror. **CONFIRMED on the PC (2026-08-18).** Guarded,
  user-authorized compare-before-write pokes to `0x0059D9A7` under the pristine
  Wine build **changed the thrown berry** (user-observed): `1`=blue/super,
  `2`=green/homing, `3`=gold, `4`=purple/mega-homing (`0`=red default). So
  `0x0059D9A7` is the causal berry-type **selector** (source, not mirror —
  `0x0059F500` stayed 0); `KU-073` is resolved for the selector + causality +
  the 1-4 map. Record:
  [[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]].
  Cross-port lead and provenance:
  [[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]].
  First end-to-end demonstration of the replay→constants→PC-static cross-port
  loop; the external repository was read-only throughout and the isolated
  emulator instance was closed with a clean process check.
- Original ISO `BUGS_PC.ISO` is inventoried with SHA-256 `b0c3da82688c511f920a5559bdc3dcb8354d253182790a239665c8cd080d9ed9`.
- PC executable `bugs.exe` is `BIN-97c95ba5572dce63`, SHA-256 `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- A Ghidra project, reviewable static export, import/string maps, and address-based dossiers exist.
- `EXP-20260811-004` confirms the executable launches under Wine; the user visually confirmed a working game state from the derived `PC\BUGS` layout.
- An unchanged executable copy run from the derived `PC\BUGS` content layout passes the `cd.txt` gate, initializes DirectDraw/Direct3D, creates a window/event, loads level data, and reaches a user-confirmed working state.
- The external PS1 repository remains outside ABLPC. One committed-object-only
  comparison seeded the Training grain selector/count hypothesis in
  `XPORT-20260814-001`; PC static and runtime evidence independently confirms
  the PC result, so no PS1 fact is used as PC authority.
- `EXP-20260812-005` confirms software and Direct3D training-level rendering under Wine; the Direct3D path reaches playable gameplay.
- `EXP-20260812-007` confirms the Linux presentation baseline: select the game's 640×480×16 Direct3D hardware path and use Gamescope `fit` scaling to retain 4:3 on the 2560×1440 host.
- `scripts/play-pristine.sh` verifies the known executable hash, refuses paths
  outside `work/copies/`, and reproduces the tested Gamescope/Wine launch. The
  user-preferred research invocation is now `--research --windowed --mute`:
  it uses a 1280x960 window by default and routes the game's still-running
  audio subsystem to a private per-run null sink. Retail chooser state must
  not be assumed from an alleged default or inferred from pixels; each
  renderer-facing experiment pre-registers its selector input and accepts
  hardware only from the complete six-marker log. The historical retail R2c
  chooser branch used no-direction RC0 and a sole one-Down RC1 fallback; the
  active user-directed branch supersedes it with the accepted auto-hardware
  executable and no chooser interaction.
- [[EXP-20260816-143 - Automatic Direct3D startup static audit]] proves the
  exact retail executable exposes no native renderer-selection argument:
  game parser `0x00403B90` recognizes only `cheat/log/mpeg/high`, while the
  separate DSStream parser at `0x0042C130` recognizes only its five audio
  tokens. A paired exact-byte candidate at code file offset `0xA6C6B` plus
  relocation-entry offset `0xFA912` retains chooser initialization, writes
  selector 2, skips only its interactive loop, and resumes original cleanup.
  James rejects the simpler whole-chooser bypass and accepts the paired form
  only as a static candidate. Nothing has been built or launched; manual
  hardware selection and the six-marker gate remain authoritative under
  [[PC automatic Direct3D startup candidate]] and KU-013.
- `scripts/input-movie.py` 1.3.0 partially resolves CAP-002 with PC-native,
  executable-hash-gated keyboard record/validate/replay/compare on one proved
  Gamescope X11 game window. Replay now uses one persistent X11/XTEST sender,
  temporarily disables and restores nested-display auto-repeat, and requires
  an exact target-window echo for every normalized event. Log-anchored replay
  schema-2 movies bind a bounded post-anchor log segment and `ROUTINE` trace;
  replay and comparison reject input or runtime-log disagreement. Schema-1
  movies remain readable and unchanged. `EXP-20260815-125`
  live-accepts two fresh 300/300 exact target streams below 0.52 ms maximum
  delivery drift, but their gameplay outcomes differ. Exact input delivery is
  therefore accepted while deterministic gameplay remains open. The tool does
  not capture host input devices or supply internal-frame synchronization.
- `scripts/play-pristine-with-inputs.py` 1.4.0 adds a fixture-validated
  companion Recording/Replay menu around the unchanged hash-pinned pristine launcher.
  The familiar `--research --windowed --mute` command automatically discovers
  the one owned 640×480 PC game window, creates unique movies only under
  `work/copies/`, and exposes Start/Stop without manual PID/display/window
  entry. Gameplay recording now defaults to the first fresh `NextLife.` after
  level initialization; Hardware and level selection are setup. Level Select
  remains available as a labeled menu-only anchor, and old movies retain their
  recorded anchor. Twenty-seven focused input/companion tests pass. A fresh
  user `NextLife` movie and two replay/runtime-checkpoint agreements remain the
  next live discriminator.
- `EXP-20260815-126` records a user-driven read-only Tunnels control arm. It
  reaches the red mushroom/upper corridor; its auxiliary/reset-coordinate
  X/Z comes within about 36,378 units of a tuple then mislabeled as descriptor
  571; EXP-131 proves it is descriptor 572's base. It is not a current-position
  trace. One raw flag-`0x0002`, counter-`4 -> 3`
  transition probably matched user-observed damage, but current collision
  value stayed 0 and no reset bit or nonzero `NextLife` appeared. The user
  ended the route before target-height contact, so `KU-057` remained open at
  that point; EXP-131 later resolves its milestone disposition.
- `EXP-20260815-128` corrects the coordinate source with a controlled pristine
  Training jump and ground movement. Current live Flik XYZ is
  `0x0059D910`/`14`/`18`; `0x0059D920`/`24`/`28` retains the preceding distinct
  tuple in the trace; `0x0059D960`/`64`/`68` is an auxiliary/reset-coordinate
  triple that stays fixed while airborne. Static PC reads/copies independently
  support the separation. Overlay 1.2.0 and companion 1.5.0 now show compact
  X/Y/Z inside the owned Gamescope display, with raw fields opt-in through
  `--details`. EXP-127 remains authority only for read-only access and joined
  cleanup. Click-through, atomic evidence capture, and engine-frame cadence
  are not claimed.
- `EXP-20260815-129` supplies the natural Level03 reset producer missing from
  M3.5 at the first grain-gate pit. Two ordinary falls read current collision
  descriptor/value `572/1`, flags `0x0014`, and `NextLife=2`, then repeated a
  row-7-like endpoint `(497247,31299,547255)` consistent with the nearest-row
  consumer at `0x00432930`. A user-confirmed spider death in the same run used
  descriptor/value `543/0`, so the former descriptor-571/black-spider route is
  rejected. One explicitly authorized byte write changed grain count
  `1 -> 10` only to lower the first gate; it is disclosed and means this was
  not an unchanged-state gate-access arm. At this point KU-057 was narrowed to
  natural row-6-region selection or explicit disposition; EXP-131 later takes
  the disposition branch. Repeating the same pit is not useful.
- `EXP-20260815-130` bounds user-authorized Level03 teleport diagnostics. A
  24-byte current+preceding write to known walkable point
  `(501696,30092,494016)` was stable, but the engine adopted it into auxiliary
  about 10 ms later. An all-three write and an equal current+preceding write
  to unsupported below-floor/pit points each created a repeating generic
  `NextLife=2`, descriptor/value `548/0` reset loop. Teleporting beyond the
  zero-grain gate is write-assisted, not natural, and supplies no KU-057
  row-6 evidence. Routine teleport is now limited by [[PC Flik teleport procedure]].
- `EXP-20260815-131` maps the exact PC `TERRAIN.ALL` collision source and
  corrects EXP-118's 16-byte scanner misalignment. Level03 result-1 descriptors
  570–578 form nine regions paired spatially with all 18 type-1 rows.
  Descriptor 572 is the sole rows-6/7 region; its bounds cross the nearest-row
  boundary, but both natural EXP-129 contacts lie on the row-7 side and no
  second row-6-near result-1 descriptor exists. M3.5 explicitly disposes of
  natural row-6 selection as a blocker without claiming it impossible.
- `EXP-20260816-153` activates M5 with its first admitted module. The type-1
  reset-placement selector at `0x00432930` (byte-identical variant
  `0x00437A20`) is reimplemented engine-exactly in
  `reimplementation/ablpc/type1_reset.py`, with the read-only reporting tool
  `scripts/type1-reset.py`. It reproduces both natural EXP-129 pit falls
  (row 7, `(497248, 31176, 547264)`), the EXP-130 walkable fixed point
  `(501696, 30092, 494016)` exactly, and the EXP-116/117 `+4096` candidate
  delta; its terrain descriptor 543 at the row-7 placement independently
  matches the collision descriptor EXP-129 sampled after the reset. Three new
  facts: the loader aliases a negative record type into the same pointer slot
  and a later record overwrites an earlier one (`0x0044BC8B`/`0x0044BCA9`);
  the original reads an uninitialised best-index local when the row count is
  zero, reachable only that way; and Level03's 18 rows pair one-to-one with
  the nine grain gates taken from independent executable immediates. The
  module refuses zero-count, negative-type-alias, and missing-record inputs
  instead of emulating them. Confirmed reset role stays Level03/Tunnels;
  `KU-062` and `KU-063` are open. The complete M5.1→M5.5.1 chain is
  independently accepted by EXP-158; all four exit gates hold at that bounded
  Level03 contract.
- [[EXP-20260816-170 - M5.7 grain-gate opening resolver]] and
  [[EXP-20260816-171 - Independent M5.8 grain-gate resolver audits]] complete
  M5's second admitted module. The first audit rejected exact commit `efad1c2`
  only because the CLI accepted conflicting duplicate JSON keys despite
  claiming strict JSON;
  a duplicate-detecting parser plus top-level/nested/path regressions now pass
  64/64 focused fixtures. A directly retained canonical gate is a KU-065-
  qualified 686/686 with Vault 482/0/0 and tracked audit 0 (SHA-256
  `617e71f1...db5`). Wholly fresh James then **ACCEPTED** exact correction
  `dfd3af3` (tree `8b7d423`) after independently reproducing all literal and
  escaped duplicate refusals, valid input modes, 38/38 and 64/64 fixtures, and
  a KU-065-qualified canonical 686/686 gate (SHA-256 `b1e9a473...bc713f`). All
  native arithmetic, ordering, write, receipt, lifecycle, and evidence-limit
  claims survived unchanged. The pure
  module `reimplementation/ablpc/grain_gate_resolver.py` evaluates the ordered
  nine-row Tunnels loop `0x00432EEA-0x00433043` and one City call at
  `0x00433790` using exact signed-int32 `sub`/`sar 8`/`imul`/`add` arithmetic.
  It emits ordered direct writes—including row-0/4 coupling and index-0-only
  `write_u8(0x00599C69,1)` at `0x00433807`—plus separate downstream rule
  metadata and explicit native-order refusals. The address byte stays
  semantic-Unknown under KU-067; EXP-146 remains direct/static scope only.
  Thirty-eight new asset-free tests reproduce every usable accepted receipt
  and exact overflow/order edges; 64/64 combined resolver/threshold/coordinate
  fixtures pass in a retained raw log. The worker does not alter the threshold
  builder, execute decay/animation, read assets, or generalize a trigger VM.
- [[Python and C reverse-engineering split]] now makes language choice a
  measured procedure: Python remains the reference/controller for offline
  parsing, orchestration, receipts, and low-rate observation; C is reserved
  for a demonstrated hot loop or required native ABI and must preserve a
  versioned, loss-accounted, differentially tested boundary. This changes no
  evidence authority or target-write permission.
- A bounds-checked independent `LEVEL*.DAT` prefix parser, manifest editor, sparse overlay builder, staged-tree builder, CLI, and regression tests exist under `reimplementation/ablpc/`.
- `EXP-20260814-111` activates M3 with an exact Training 51-grain vertical
  slice. The source DAT's first type-`0x3F` table has 50 selector-`0x14`
  records. A dedicated exact-hash recipe inserts entry 62 at `(4950,-1301,
  1127)`, relocates 556 known file-relative fields, reparses, inverses exactly,
  and emits SHA-256 `20d0f9b...fd40` with 51 selector-`0x14` records. The
  unchanged executable boots the complete staged tree through Direct3D; the
  new record alone enters consumed sentinel state while counter `0x0059D9B1`
  increments `0 -> 1`. The initial black level-select screenshot was a
  reproduced incomplete-drive-shape staging regression: absolute
  `\PC\BUGS\CD\LEVEL00\LEVEL.RAW` was missing. A complete mapped
  `DRIVE:\PC\BUGS` tree corrects it and renders normal menus/gameplay.
- `EXP-20260814-112` completes M3.2 at a bounded `51/50` bonus boundary.
  Controlled `49 -> 50` and `50 -> 51` pickups prove the original exact-50
  event fires once while the counter retains 51; the unchanged in-level HUD
  caches digits `(5,1)`. An exact reversible three-byte tally patch at file
  offsets `0x422CB`, `0x422CF`, and `0x42327` emits executable SHA-256
  `8ececef...4456`, retains 51, sets the original completion flag, reaches the
  bright completion/emblem path at 50, and visibly renders `51/50`. The
  previously inferred Training clamp in `0x00439E90` was not reached and is
  reclassified as an unidentified mode/level cap. `KU-054` is resolved. M2
  remains Deferred and M4/M6 remain Complete and unchanged.
- `EXP-20260814-113` completes M3.3 at a bounded Training FLIK-letter edit
  boundary. The exact 51-grain DAT contains singleton type-`0x3F` selectors
  `0x10`–`0x13`; a dedicated hash/layout-locked transformation can move,
  duplicate, or remove those records while preserving unknown bytes,
  relocating 556 fields, reparsing, and inverting exactly. The accepted
  115,140-byte demo DAT is SHA-256 `e9c75bb2...cae7a`, duplicates all four at
  moved positions, boots the unchanged executable through Direct3D, and
  independently produces letter-mask bits `1`, `2`, `4`, and `8` while the
  four originals remain intact. A duplicate collected after mask `0x0F`
  retriggers the existing completion/reward path (`0x0059D9B0: 1 -> 2`);
  one-shot duplicate reward behavior is explicitly outside this data-only
  packet. M2/M5 remain Deferred and completed M4/M6 authorities are unchanged.
- `EXP-20260815-114` completes M3.4 at the exact eight-slot Training
  `FLIKFLIK` boundary. A deterministic executable recipe composes the accepted
  M3.2 counter patch with the M3.3 DAT and maps original/appended letter
  records to eight independent bits. Exact final-hash runtime discriminators
  prove `0x7F -> 0xFF` produces the completion/reward transition once, while
  an already-complete pickup leaves reward unchanged. The in-level and tally
  helpers render centered `FLIKFLIK`; the tally visibly reports `8/8` beside
  the unchanged emblem and preserves `51/50`. The 1,069,056-byte output is
  SHA-256 `b572e6d1...47f4`, PE headers/sections are unchanged, and two-stage
  exact inversion reconstructs retail. This is not a generic word engine.
  `EXP-20260815-115` independently accepts that exact claim after reproducing
  the build/inverse, auditing x86/PE/relocations/state and runtime linkage,
  attacking the CLI boundary, and passing all 530 tests plus Vault/M4/hygiene
  gates. M3 was still Active at that packet; EXP-132 later supplies the worker
  closure ledger, EXP-133 rejects its Training authorization provenance, and
  EXP-134 supplies the exact two-arm correction. Independent EXP-135 accepts
  the corrected four-gate ledger and closes M3 at the existing boundaries.
  M2/M5 remain Deferred and M4/M6 stay unchanged.
- `EXP-20260815-116` activated M3.5 on a separate Level03 type-1 coordinate
  stream. PC `0x00432930` conditionally scans the type-1 pointer at
  `0x005C5864`, selects by X/Z distance, stores X/Z shifted left by five, and
  terrain-recomputes Y; `0x0041C8CC` is a static producer of its `0x10` state
  bit. Exact `LEVEL03/LEVEL.DAT` row 6 is `(15678,0,15438)` at `0x4A4`.
  A guarded recipe changes only its X by `+128` and predicts `+4096` runtime
  X if selected. Multiple PC consumers prevent naming type 1 as a checkpoint
  or bespoke respawn table. `XPORT-20260815-002` is experiment-selection
  inference only. EXP-129 later confirms the natural first-pit-to-row-7 path;
  natural row-6-region selection remained open as `KU-057` until EXP-131's
  explicit disposition.
- `EXP-20260814-060` adds worker-complete schema-2
  `replace-whole-file` support at one exact opaque-file boundary. Its exact
  schema/hash, ordinary sparse/staged, deterministic-receipt, M1-compatibility,
  local-corpus, and no-game-bytes results survive independent M4.2 review.
  `EXP-20260814-061` nevertheless rejects M4.1 acceptance: the complete output
  plan is not preflighted. An existing `output/.ablpc` symlink can receive the
  fixed receipt outside the requested root, and deterministic later
  destination/receipt-parent failures can leave earlier sparse or staged
  writes. `EXP-20260814-062` completes the M4.3 worker correction: all planned
  destinations and the fixed receipt now receive deterministic topology
  preflight, all four cases fail with `ManifestError` before mutation, 47
  focused and 235 full tests pass, and the exact local recipe remains green.
  Independent `EXP-20260814-063` now accepts that correction: all four
  original and 22 adjacent topology cases pass with explicit no-mutation
  checks, M1 schema applications pass 6/6, and the exact recipe passes twice.
  The accepted claim remains deterministic planned-path/type preflight, not
  general rollback. `EXP-20260814-064` now completes the exact M4.5 worker:
  exactly two manifests compose at disjoint byte claims or produce
  deterministic asset-free conflict JSON before output. Reversed-order
  success/conflict, synthetic apply/stage, 58 focused and 246 complete tests,
  and tracked same-file/different-file local pairs pass. Fresh-context
  `EXP-20260814-065` rejects acceptance: span sorting can reverse edits inside
  one independently valid input. Both inputs in the exact synthetic
  falsification apply alone and have disjoint cross-input claims, but both
  compose argument orders fail combined revalidation. `EXP-20260814-066`
  completes the exact M4.7 worker correction: canonical input rank followed by
  original edit index preserves each authored sequence, the falsification and
  four adjacent regressions pass, the focused/full suites are 63/251, and both
  tracked local hash sets remain unchanged. Fresh-context
  `EXP-20260814-067` now accepts that correction after both rank orientations,
  a three-edit authored chain, exact conflict/collision cases, and a genuine
  cross-input dependency all preserve the declared behavior. The scoped suites
  remain 63/251, topology/schema gates pass 28/28 and 6/6, both local pairs and
  the opaque recipe retain exact hashes. `EXP-20260814-068` now completes the
  exact M4.9 worker packet: ordinary sparse overlays are removed only after
  recomputed manifest/source receipt equality, byte-exact receipt encoding,
  regular single-link output/hash validation, and an exact no-extra-content
  tree. Thirty-two new cases raise the focused/full suites to 95/283; all
  mismatch cases
  preserve exact snapshots, and three exact local manifest families apply and
  remove twice with unchanged source hashes. Fresh-context
  `EXP-20260814-069` preserves those ordinary baselines but rejects M4.9:
  twice, a pre-existing bind-mounted intermediate overlay directory passed
  the complete preflight, lost its recorded file through the mount, and left
  a partially removed overlay when final directory removal failed `EBUSY`.
  `EXP-20260814-070` completes exact M4.11 at the worker boundary: a Linux
  `/proc/self/mountinfo` guard decodes escaped mount paths and checks the
  overlay root plus every planned directory, output, and receipt before
  traversal or unlink. Four private-namespace bind cases preserve complete
  overlay/source/independent-target snapshots; focused/full suites pass
  99/287 and all six tracked local cycles retain exact hashes. Exact
  fresh-context `EXP-20260814-071` rejects M4.11 acceptance: the guard checks
  only the exact resolved overlay root and descendants, so a pre-existing
  alias at a proper parent traversed to reach that root can remove the
  independent overlay and return success. James and Root reproduced that same
  stable layout once each; sources stayed unchanged while visible-overlay and
  independent-target snapshots changed. Exact corrective packet M4.13 is
  active on the omitted traversed ancestry only.
  `EXP-20260814-072` now completes that worker correction. Mountinfo parsing
  retains mount ID, device, filesystem root, and mountpoint; exact planned
  mountpoints still refuse, while proper ancestry rejects a newer mount whose
  filesystem root is already reachable at a different older same-device path.
  The exact alias case and four retained mounted paths pass with complete
  snapshots unchanged. Normal root, `/home`, `/tmp`, and same-path filesystem
  mounts remain usable; focused/full suites pass 101/289 and all six local
  cycles retain exact hashes. M4.13 is worker-complete, not independently
  accepted. Fresh-context `EXP-20260814-073` preserves the uncovered exact
  alias refusal and every baseline but rejects M4.14: a hidden lower bind alias
  covered by a distinct ordinary top filesystem at the same parent pathname
  still taints that visible ordinary ancestry. `EXP-20260814-074` completes
  exact M4.15 at the worker boundary. Alias comparison now excludes a lower
  record only when a same-mountpoint covering record names it through the
  retained parent relation. The exact stacked ordinary-top overlay removes
  completely with source and hidden target unchanged; the uncovered ancestor
  and four exact root/descendant mount cases still refuse unchanged. Focused/
  full suites pass 102/290 and all six local cycles retain exact hashes. M4.15
  is worker-complete but not independently accepted. Fresh-context
  `EXP-20260814-075` preserves those results and every retained baseline but
  rejects M4.16: after a disposable lower-ID mount is released, Linux can
  reuse that numeric ID for a newer uncovered bind alias while the source
  remains mounted at a higher ID. `_mount_alias_points` treats numeric mount
  IDs as creation order, misses the alias, and authenticated removal succeeds
  through it, changing the independent mounted target. Exact corrective M4.17
  became worker-complete in `EXP-20260814-076`: `listmount(2)` later-first
  unique IDs plus `statmount(2)` old-ID/parent/device mapping supply verified
  `mount_order`, while mountinfo is reread and cross-checked before use. The
  exact reused-lower-ID case now refuses with source/independent-target/alias/
  overlay snapshots unchanged; the targeted mount family passes 10/10,
  focused/full suites pass 105/293, and all six local cycles retain exact
  hashes. Fresh-context `EXP-20260814-077` accepts M4.17 after independent
  current-x86_64 UAPI/kernel review, adversarial syscall/mapping/table
  injection, a separate old-ID 1081/1082/1081 namespace reproduction, all
  seven tracked namespaces, 120 tuple permutations, 105/293 focused/full
  tests, explicit M1 6/6, and six exact local cycles. The reused alias refuses
  before overlay traversal with all four snapshots exact. M4.19 is worker-
  complete in `EXP-20260814-078`: canonical strict v0.1 metadata names five
  demonstrated anchors, existing schema/operation/workflow limits, current-
  Linux removal prerequisites, exact Wine/Gamescope scope, and unsupported
  surfaces. Its asset-free checker passes 18 drift tests and the canonical
  suite passes 311. Fresh-context `EXP-20260814-079` nevertheless rejects
  M4.20. The checked-in statement and authorities agree, 17/17 independent
  declaration-family mutations and eleven direct authority/input attacks
  reject, and static/read tracing finds only nine asset-free tracked reads.
  But a disposable launcher containing `OUTPUT_WIDTH=2560` immediately
  followed by effective `OUTPUT_WIDTH=1` still passes alignment because the
  width is checked only as a substring. Filter, receipt-constant, and
  Environment-row contradictions reproduce the same class. Exact M4.21 is now
  worker-complete in `EXP-20260814-080`. Ordered shell declarations,
  Python-AST contract extraction, one generated Environment row, and scoped
  keyed Markdown declarations reject those four cases plus adjacent ambiguity;
  focused/full suites pass 36/329 and the read set remains exactly nine tracked
  asset-free inputs. The statement and game-facing behavior are unchanged.
  Exact fresh-context `EXP-20260814-081` nevertheless rejects M4.22. Standard
  post-declaration Bash indexed/compound/array writes, post-guard game-directory
  mutation, Python global/validator rebinding, and conflicting duplicate
  tracked-manifest keys can all change or ambiguate claimed effective authority
  while alignment succeeds. The exact statement, four M4.20 rejections, scoped
  declarative checks, 36/329 suites, and nine-read boundary survive. Exact M4.23
  is worker-complete in `EXP-20260814-082`. The checker now verifies exact
  SHA-256 for the launcher, manifest implementation, and three tracked
  manifests from their same already-read raw bytes before semantic alignment.
  Direct pin checks and all six residual bypass families pass; focused/full
  suites are 47/340, the statement remains byte-exact, and the read boundary
  remains exactly nine asset-free paths. No authority, parser/input, or game-
  facing behavior changed. Fresh-context `EXP-20260814-083` independently
  accepts that immutable correction: the exact five/no-extra pin set, 10/10
  predecessor attacks, 5/5 direct mutations, 5/5 missing-pin failures, 3/3
  scoped human checks, nine unique reads, 47/152/340 tests, and every hygiene
  gate survive. `EXP-20260814-084` now completes exact M4.25 at the worker
  boundary: one single-manifest library/CLI dry-run reports authored files,
  records, hashes, sizes, and half-open ranges from ordinary preparation with
  exact snapshot equality. Focused/combined/full suites pass 99/161/349. Only
  the independently reproduced manifest-implementation pin changed; exact
  five-pin/nine-read compatibility survives. Fresh-context
  `EXP-20260814-085` now independently accepts that immutable report after 91
  assertions across 20 adversarial cases, zero trapped writes, exact snapshots
  on success and ten failure families, exact retained receipt/workflow bytes,
  38 compatibility assertions, nine reads, and 99/161/349 tests. Exact M4.27
  then audits all nine required capabilities and five exit gates in
  `EXP-20260814-086` and returns `REJECT`: eight capabilities and four gates
  survive, but current receipts are deliberately insufficient without the
  original manifest, and no accepted test joins one tool-created clean-copy
  install through validation, launch, and removal. `EXP-20260814-087` now
  completes exact M4.28 at the worker boundary: strict external ordinary
  receipts reconstruct only current existing-schema manifests, drive new-root
  sparse replay and shared receipt-authenticated removal, pass 146/208/396
  tests and six deterministic local cycles, and refresh only the manifest pin.
  Fresh-context `EXP-20260814-088` rejects M4.29 acceptance at one exact
  parent-component consistency boundary: a checked receipt parent can change
  into a directory link before final file acquisition and still reach the same
  accepted inode at a changed location. Exact component-stable acquisition
  correction M4.30 is worker-complete in `EXP-20260814-089`; exact M4.31
  retains the acceptance fix but rejects exception-unsafe descriptor cleanup
  in `EXP-20260814-090`. Exact M4.32 is worker-complete in
  `EXP-20260814-091`; exact M4.33 is independently accepted in
  `EXP-20260814-092`. `KU-051` is resolved at the current receipt/component/
  closure boundary. Exact M4.34 then returns `REJECT` in
  `EXP-20260814-093`: complete staged/forced-copy outputs reach the launcher
  boundary but fail sparse removal unchanged, while removable apply/replay
  outputs are not complete game trees. `KU-052` and M4 remain open on exact
  M4.35 manifest-driven clean-copy restoration. `EXP-20260814-094` now
  completes that worker with exact full-tree equivalence/mount preflight,
  188/250/438 tests, six retained sparse local cycles, and one 722-file
  stage/launcher-dry-run/restore lifecycle. Fresh-context
  `EXP-20260814-095` retains the parent refusal, 11 ordinary restoration
  variants, 18 deterministic refusals, five inode-change traps, eight private
  namespace cases, the exact local lifecycle, six sparse cycles, five pins,
  nine reads, and 188/250/438 tests, but returns `REJECT`: complete source/game
  inventories accept both `Case.bin` and `case.bin` and restore the ambiguous
  Windows tree successfully. M4 and `KU-052` remain open on exact M4.37's
  case-insensitive complete-tree path-uniqueness correction.
  `EXP-20260814-096` now completes that correction at the worker boundary.
  Every source/game file and directory receives one case-folded relative-path
  key; all eight file/file, directory/directory, file/directory, and nested
  source/game collision regressions reject with exact snapshots and read/
  mutation traps. Two additional uppercase-first directory cases refuse
  before descending into either ambiguous branch. Focused/combined/canonical
  totals are 198/260/448, the exact 722-file lifecycle and all six sparse local
  cycles retain prior hashes, and only the manifest pin changes to
  `b3480761...6d75`. M4 and `KU-052` remain
  open on independent exact M4.38; the statement remains unchanged.
  `EXP-20260814-097` now independently returns `ACCEPT`. The exact parent
  again accepts `Case.bin`/`case.bin`; the immutable worker rejects 36 fresh
  source/game collision cases and four bind-mounted colliding-directory cases
  under both lexical orders without ambiguous branch descent. All eight
  namespace families, five identity swaps, the exact 722-file lifecycle, six
  sparse cycles, five pins/nine reads, statement bytes, and 198/260/448 tests
  pass. `KU-052` resolves only for the demonstrated manifest-driven current-
  Linux lifecycle, and M4.38 selects exact M4.39 v0.2 statement alignment.
  `EXP-20260814-098` now completes M4.39 at the worker boundary. Historical
  v0.1 remains exactly 6,177 bytes at SHA-256 `c3427d44...af0`; canonical v0.2
  is 7,677 bytes at SHA-256 `dacfcab8...ccb2`. It adds only the accepted
  manifest/source-authenticated current-Linux complete-tree restoration
  boundary and retains every unsupported deletion, external-receipt full-tree
  restoration, untested-platform/filesystem, provenance, POSIX-metadata,
  transaction, automation, Windows-path, and concurrency limit. The same five
  pins and exactly-nine-read asset-free boundary survive; all 151 v0.2 scalar
  value drifts reject. `EXP-20260814-099` independently preserves those bytes,
  pins, reads, restoration limits, and 58/271/459 retained suites but returns
  M4.40 `REJECT`: reordered object fields are accepted, each canonical selected
  path accepts the complete opposite version, and unhashable `statement_id`
  escapes as `TypeError`. The worker's combined count 266 was stale; the exact
  pre-correction collection is 271. `EXP-20260814-100` completes sole M4.41 at
  the worker boundary: both paths are version-bound, every object key sequence
  is checked, typed IDs fail normally, 151/151 value and 151/151 type attacks
  reject, and suites pass 71/284/472. Statements, five pins, nine reads, and
  behavior remain exact. `EXP-20260814-101` independently retains those facts
  but returns M4.42 `REJECT`: if the canonical active pathname is a relative
  symbolic link to the canonical historical file, resolved-path selection
  chooses v0.1 and the default checker succeeds. The reconciled ledger is eight
  of nine capabilities and four of five exit gates. `EXP-20260814-102` closes
  that exact worker boundary with lexical identity, selected regular non-link
  admission, retained unselected links, and 75/288/476 suites.
  `EXP-20260814-103` independently accepts that correction after selected
  link/nonregular no-read attacks, lexical-alias/unselected-path checks, exact
  statement/order/leaf/pin reconstruction, and full ledger reconciliation.
  The final ledger is 9/9 capabilities and 5/5 exit gates. M4 is Complete only
  at its documented asset-free, current-x86_64-Linux, explicit-unsupported
  boundary; no successor milestone was active at that closure point. The later
  concrete Training collectible goal activates M3 through `EXP-20260814-111`.
- `EXP-20260814-104` independently rechecks that completed state at exact clean
  post-closure HEAD. Its separate 663-assertion synthetic matrix adds hard-link
  and parent-link boundary cases to the prior path/read attacks, reconstructs
  the complete ledger and contracts, and passes 75/288/476 tests plus all
  hygiene gates. The verdict remains `ACCEPT` without widening final-entry,
  parent-filesystem, concurrency, platform, workflow, or unsupported scope.
- `EXP-20260814-105` initially accepted M6 at one exact asset-free Wine/Linux
  release boundary. Final clean source `5daee2bc...37a4c` builds two byte-identical
  378,880-byte toolkit archives at SHA-256 `1527281c...b62a0` from 36 exact
  tracked files plus one generated canonical inventory; strict reconstruction
  rejects unlisted, noncanonical, appended, linked, nonregular, forbidden, or
  metadata/content-drifted archives. The exact Fedora 44/kernel/Python/Wine/
  Gamescope smoke matrix passes 21/21 `LEVEL*.DAT` files and three complete
  Training/Level 01/schema-2 stage -> launcher-dry-run -> restore cases with
  exact 747-entry source/stage inventories. Isolated installed wrappers,
  two-version migration/rollback, corrupt/appended/no-history/tampered-prior
  refusals, 486 tests, M4 compatibility, Vault, tracked, diff, and clean gates
  pass at that worker boundary. `EXP-20260814-106` independently retains the
  dual-build/archive, smoke, M4, and hygiene results but rejects M6 closure:
  normal installed-wrapper use creates five unlisted `.pyc` files and
  invalidates the complete inventory, lifecycle verification accepts linked
  `releases/` or selected-version roots, and installation replaces a dangling
  `state.json` symlink as though no state existed. M6 is Active only for the
  exact installed-wrapper bytecode and installed-path-identity correction.
- `EXP-20260814-107` completes that exact correction at the worker boundary.
  Three shell entry points now enforce Python `-B` plus
  `PYTHONDONTWRITEBYTECODE=1`; the direct compatibility entry point disables
  bytecode before package import. State admission uses `lstat`, and lifecycle
  inventory traversal admits lexical `releases/` and selected-version roots
  only as real directories. The installed-package regression runs all four
  entry points with external bytecode controls removed and preserves one exact
  38-file install snapshot after every call. Dangling state, linked releases
  root across install/current/rollback, and linked selected versions across
  install/current/rollback reject with full snapshots unchanged. Exact clean
  commit `580a1cb` builds two byte-identical 389,120-byte archives at
  `7a1ede97...fcd2`, source tree `fa6a3ee4...c85ea`; smoke remains 21/21 and
  3/3 at report `1a8a3b57...323e`; 492 tests, five M4 anchors, and all hygiene
  gates pass. M6 remains Active until fresh-context James acceptance.
- `EXP-20260814-108` independently rejects that first correction at exact HEAD
  `23ff833`. The three original `EXP-106` defects close, but James's 55-case
  lifecycle matrix has 20 improper successes and 12 snapshot changes:
  missing `releases/` is recreated before failed migration; hostile in-tree
  `PYTHONPYCACHEPREFIX` writes 30 startup bytecode files through the direct
  checker; hardlinked/missing state is accepted; outgoing-current and inactive-
  prior invalidity is treated asymmetrically; and 9/10 adjacent inventory/
  manifest/topology/mode attacks pass. Exact artifact, tar-adversary, smoke,
  M4, and hygiene evidence remains retained.
- `EXP-20260814-109` completes the combined second correction at clean HEAD
  `7d8594e`. It moves direct-checker `-B` to interpreter startup, validates
  state before creating topology, verifies every installed version, requires
  canonical single-link files plus exact directory topology/modes, and adds
  canonical state schema 2 locks for the verified archive, release manifest,
  and source tree. The state lock rejects content plus a recomputed in-tree
  manifest. All 30 focused release tests and 509 canonical tests pass. Two
  399,360-byte archives match at `68d3d31a...060b`, source tree
  `2644263f...bef9`; hostile-cache entry points preserve install snapshot
  `15ce25c5...60e4`; and exact smoke report `c1fb6903...98dc` passes.
- `EXP-20260814-110` independently returns `ACCEPT` at exact clean audited HEAD
  `64d8ac1`. James reproduces the exact dual artifact/tree hashes, 13/13
  strict archive refusals, and smoke report `c1fb6903...98dc`; obtains 55/55
  required lifecycle refusals and 10/10 inventory/manifest/topology/mode
  refusals with every complete snapshot unchanged; and runs all four installed
  entry points under both cache-environment families with zero bytecode or
  snapshot drift. The 509-test, M4, Vault 312/0/0, tracked-content, diff,
  staged-diff, and clean-tree gates pass. M6 is Complete at the documented
  asset-free Fedora/Wine launcher-readiness and local-state-trust boundary.
- The parser accepts all 21 PC `LEVEL*.DAT` files tested. The three-record training example is accepted through `InitMainGame` and `NextLife` under the known-good Wine drive layout.
- `EXP-20260812-008` provides a stable native-GDB hardware-watchpoint method at the Training title pause and matched individual hardware-renderer manifests/captures for primary records 124–126.
- `EXP-20260812-009` bounds the positive-count payload-target layout used by the masked `0x49` scene dispatch, provides a complete Training primary reference/block census, and validates 990 same-dispatch records across 14 PC files with zero errors.
- `EXP-20260812-010` confirms both reciprocal record-124/125 target rebinds
  under the Direct3D hardware path. The original executable accepts both, and
  phase-matched captures change only the independently identified placement
  regions.
- Read-only target inspection, same-dispatch corpus scanning, and a guarded
  four-byte target-rebind operation now have staging, byte-locality, original-
  executable acceptance, and visible-result evidence for the exact Training
  hash.
- `EXP-20260812-011` separates the first three record dwords from render
  placement for dispatch `0x49`: they form an upstream candidate-center tuple,
  while relocated `+0x10` supplies the payload placement data.
- `EXP-20260812-012` confirms that positive signed record `+0x0C` contributes
  the visibility bound. An expected-value-guarded, offset-named edit operation
  and regression tests cover only this demonstrated field boundary.
- `EXP-20260812-013` binds `ant hill` to the exact Level 01 DAT and confirms
  that byte-local record-center and guarded positive-target edits are accepted
  by the unchanged executable on a second file under Direct3D. Both retain
  exact control frames at the tested start camera.
- M1 tooling is promoted at the bounded surface in [[M1 Tool Support Matrix]].
  Supported-target inspection filters to masked dispatch `0x49`; the manifest
  schema rejects unknown root/operation fields, duplicate Windows targets,
  unsafe paths, wrong hashes, and unsupported layouts. Eighteen synthetic
  tests pass, both accepted exact recipes reproduce their prior bytes, and the
  corpus remains 990/990 valid supported references with zero errors.
- `scripts/census-pc-content.py` reproducibly generates the metadata-only
  [[PC Content Census]] for a derived work copy. The checked report inventories
  721 files without embedding payload bytes, matches explicit retained loader
  paths, and refuses protected roots, symlinks, and case-insensitive collisions.
- `EXP-20260812-015` maps the PC plant pair request path and immediate
  consumers. Exact base strings flow through `0x00445020` and `0x00444C40`;
  `.ANM` first reaches `0x00444B70`, while `.ALL` is interpreted by
  `0x00448010`. [[Functions MOC]] indexes the new address dossiers.
- `EXP-20260812-016` binds Training plant IDs 4, 10, and 6 to exact bytes
  `0x394`, `0x3A4`, and `0x3B4` in the type-`0x3F` top table of the exact
  Training DAT. The table shares the DAT/fixup path with M1 but is outside the
  20-byte scene-record and positive-target ranges.
- `EXP-20260812-017` maps the first-level PC `.ANM` consumer at `0x00444B70`.
  A lossless, bounds-checked read-only inspector, two CLI commands, 16
  synthetic tests, and a metadata-only 11-file corpus report now exist. All 11
  PC plant `.ANM` files pass with zero failures.
- `EXP-20260812-018` confirms that exact plant 10 `.ANM` bytes are accepted at
  the staged plant 04 path with plant 04 `.ALL` unchanged. Matched hardware
  logs reach Training `NextLife`; no stable start-camera visual change is
  discriminated beyond measured control-to-control animation variance.
- `EXP-20260812-019` confirms that the exact equal-size plant 10 `.ANM`/`.ALL`
  pair is also accepted at the two staged plant 04 paths. The accepted
  Direct3D logs normalize byte-identically and reach `NextLife`; the paired
  start-camera visual delta remains inside independent control variance.
- `EXP-20260812-020` corrects the selector model and confirms exact plant 10
  request suppression. Same-class selectors consume a shared occurrence
  cursor, so the original `0x394` plant-04 plan would instead shift the second
  selector to ID 4. Changing only `0x3A4` from `0x2B` to `0x00` preserves
  plant 04, removes both plant 10 request lines, otherwise preserves the
  normalized initialization log, and reaches hardware `NextLife`. No stable
  start-camera mask is discriminated beyond three independent control
  baselines.
- `EXP-20260812-021` resolves plant 10's live ANM slot and exact two-entry
  Training object range. Three hardware-gated M1 dispatch-to-renderer windows
  find no read of the ANM slot or either entry `+0x20` dword, narrowing but not
  resolving the placement/resource identity.
- `EXP-20260812-022` reproduces the exact range and finds no CPU read of either
  entry `+0x20` dword or the adjusted first-entry dword from the natural title
  start through `NextLife` and 71.708 seconds of gameplay. The late-
  initialization copy boundary remains open.
- `EXP-20260812-023` corrects the shared `0x00445B01` boundary with a unique
  plant 10 `0x0044596D` guard. The same three exact ranges remain unread
  through scene-resource batch return `0x004679C7` and the natural title, so
  M2.11 widens only to statically copied entry-head dwords.
- `EXP-20260812-024` reproduces both plant 10 entry heads as `0/0/0/1` and
  records matched negative windows for both entries' exact
  `+0x00/+0x04/+0x08` dwords through batch return and into post-title
  gameplay. M2.12 narrows to the remaining nonzero `+0x0C` dwords.
- `EXP-20260812-025` watches both nonzero entry `+0x0C` dwords in one guarded
  run. Neither is read before `0x004679C7` or while execution reaches a
  retained unattended Training title; both remain `1`. Static candidates in
  `0x00446970` first gate on entry word `+0x2E`, defining M2.13's exact next
  surface without assigning field meaning.
- `EXP-20260812-026` watches both exact entry `+0x2E` words in one guarded
  hardware run. Neither is read before `0x004679C7` or while execution reaches
  a retained unattended Training title; both remain unsigned `1`. Thus neither
  exact plant 10 entry reaches the `0x00446A8A/0x00447661` comparisons within
  that window.
- `EXP-20260812-027` watches both exact entry `+0x28` words in one guarded
  hardware run. Neither is read before `0x004679C7` or while execution reaches
  a retained unattended Training title; both remain unsigned zero. M2.9–M2.14
  now bound every exact field populated by `0x00448010` and its guarded caller
  for at least one explicit interval. Static reader `0x0044CE3E` derives an
  entry range from a per-resource ANM header, defining the event-specific
  M2.15 follow-up without assigning field or function semantics.
- `EXP-20260812-028` watches both exact plant 10 `+0x2E` words from the
  natural Training title through `NextLife` with zero stops, then records a
  separate 30.026628-second no-input gameplay arm with zero stops. Exact
  candidate reader `0x0044CE3E` is also inactive in a separate 10.014330-
  second control. A later exploratory caller-gate arm is explicitly rejected:
  raw GDB output records `SIGSEGV` at `0x0044D79A` even though the harness
  later reports cleanup/detach; Wine prints the matching fault. M2.16
  therefore requires a fresh process, simultaneous caller/callee/data points,
  and a live post-detach receipt.
- `EXP-20260812-029` executes that exact fresh simultaneous four-point arm.
  It reaches outer gate `0x0044D79A` once with `AL == 0x40`, but raw GDB then
  records `SIGSEGV` at the same PC. The structured harness incorrectly reports
  `target_reached` after continuing that unexpected signal, and the isolated
  post-detach game surface shows Wine's fatal-error dialog. No callee or data
  negative is accepted. M2.16 closes under its fault-reproduction condition
  and makes CAP-001's fatal-signal subset blocking until M2.17 below.
- `EXP-20260812-030` upgrades `gdb-harness` to 1.1.0/result schema 2 while
  retaining strict watch-spec schema 1 compatibility. A triggered synthetic
  `SIGSEGV` now ends as structured `target_signal` with signal/PC and no blind
  continuation; required survival failure forces rejection. Safe live
  `RUN-GDB-20260812-214545` reproduces the prior four-stop plant-slot sequence,
  then independently records five resumed/untraced post-detach samples and
  live Training gameplay. This resolves the false-status/survival subset of
  CAP-001, not the origin of the exact `0x0044D79A` fault.
- `EXP-20260812-031` runs M2.18's fresh adjacent-only schema-2 arm at
  `0x0044D794`. It stops once, then reports structured `SIGSEGV` at the same
  PC and correctly rejects the arm. Its point is deleted, detach succeeds,
  five samples record state `R` with `TracerPid == 0`, and a later isolated
  game frame shows live Training under `nopass`. Per the packet stop rule, no
  new exact-`0x0044D79A` arm follows. Together with the independent exact-PC
  reproductions, the limitation is not confined only to that one instruction;
  no downstream caller/callee/data conclusion is promoted.
- `EXP-20260812-032` completes M2.19 with fresh unchanged/replacement/
  unchanged Direct3D arms and one fixed, timestamped Training trajectory. The
  controls are byte-identical at 11 of 12 same-index samples. Sparse
  replacement residuals follow player/plant/ground animation and camera edges;
  no stable replacement-local region survives direct, temporal-median, or
  three-sample mask comparisons. The plant-04/10 direct visible route is
  retired under its bounded-negative stop rule.
- `EXP-20260812-033` completes M2.20 with a positive one-path character-family
  discriminator. Exact equal-size `CHARS/FLICK.ALL <- CHARS3/FLICKD.ALL` is
  accepted in fresh control/replacement/control Direct3D arms; all normalized
  logs are byte-identical and reach `NextLife`. An 18-way all-phase mask
  retains a repeated difference only on the input-controlled central figure at
  all four tested anchors. This confirms the exact loaded-file-to-render link,
  not `.ALL` layout or filename identity.
- `EXP-20260812-034` completes M2.21 without a new runtime. `0x004671D0`
  supplies initial object index zero to `0x00445020`; its default
  `chars\flick`, resource-ID-zero arm reaches pair coordinator `0x00444C40`,
  first `.ALL` consumer `0x00448010`, and whole-file loader `0x004AE240` at
  call site `0x00448079`. Exact arithmetic for both M2.20 files bounds 30
  source descriptors and 25 initially materialized entries. The coordinator consumes
  the final entry and leaves ID-zero slot `0x005B18E0` with retained indices
  `[0,24)`, corresponding to `[0x005A9660, 0x005A9DE0)`. Native disassembly,
  exact file bytes, and retained accepted log line 1460 independently agree;
  no `.ALL` field or filename semantics are assigned.
- `EXP-20260813-035` completes M2.22 without a new runtime. In one normal
  `0x0040FFC0` update, `0x00402DC0` is the first proven unindexed
  post-initialization reader of ID-zero slot `0x005B18E0`; it calls
  `0x00445FF0` with shared-entry destination index zero. The later M1
  coordinator calls exact retained-range reader `0x0044C440`, but does so
  before loading record root `0x005BA7E0` or enumerating any 20-byte record.
  The established M1 record/payload route has no direct slot/range reference
  or call to the first-use functions. This rules out only a direct bridge in
  that branch/order window. `0x0044C440` exposes the next exact discriminator:
  a retained-entry argument passed to `0x0044F8E0` at `0x0044C898`.
- `EXP-20260813-036` completes M2.23 without a new runtime. The retained-entry
  path reads `S = *(entry + 0x20)` at `0x0044F8EA` and walks `0x24`/`0x30`
  stream records; the M1 path separately derives a 12-byte table and command
  stream from target `T` in `0x0045A7F0`. No direct source-pointer edge
  connects them. Both conditional branches converge on the exact same transform
  scratch, `0x80`-stride submission arena rooted through `0x0081BC28`, counter
  `0x008082C8`, output link/flag offsets, and list topology rooted via
  `0x004E8CC8`. This is shared conditional output topology, not active
  renderer ownership, source aliasing, or placement-to-resource identity.
- `EXP-20260813-037` completes M2.24 without a new runtime. Exact doubled-
  length cursor arithmetic partitions the 24 retained ID-zero streams into
  `[0x0004,0x2AE8)`. Entry 8 is unchanged; entries `{0-7, 9-23}` contain
  2,102 differences across 183 records, and every difference lies in a record
  span reached identically by both files' bounded `0x0044F8E0` walks. Thirteen
  remaining whole-file differences are descriptor-table offsets outside the
  retained intervals. This carries a 23-entry candidate set, not one source
  identity or a `.ALL` format interpretation.
- `EXP-20260813-038` completes M2.25 with fresh accepted control/replacement/
  control Direct3D arms. All 23 candidates in every arm return with exact
  counter/capacity/base zero, so every per-entry interval is empty and the
  changed-emission set is empty. The prior shared-arena path is conditional
  static convergence, not the active explanation for M2.20's visible result.
  A rejected execution breakpoint at `0x0044C898` also produces structured
  same-PC `SIGSEGV`; accepted arms use a safe post-call data watch, clean
  detach, and five-sample survival receipts.
- `EXP-20260813-039` completes M2.26 without a new runtime. Native selector
  arithmetic and diagnostics map value 1 to native software and value 2 to
  Direct3D. Selector-1 initializer `0x0049C520` logs `INITSOFTRENDER`, cites
  `soft.cpp`, and allocates/zeros the exact `0x80`-stride arena; helper
  `0x0049C3F0` only updates software-window state. Selector 2 calls
  `0x004119E0`; `0x0044F8E0` then routes its two record forms through
  `0x00405FE0/0x00407450` into separate Direct3D batches that can flush to the
  device `DrawIndexedPrimitive` slot. This resolves the inactive-arena
  contradiction and corrects the earlier hardware-arena label.
- `EXP-20260813-040` completes M2.27 with a static flush/reset proof and fresh
  accepted hardware-rendered control/replacement/control arms. Conditioned
  data watches capture metadata only and retain no batch payload bytes. All
  selected additions use Direct3D root `0x004C4108`, page 16; no selected
  entry flushes in-call. Replacement counts outside both controls reduce the
  exact candidate set to `{1,2,4,5,6,7,9,10,14,15,18,19,20}`. Harness 1.3.0
  and watch/result schema 4 preserve caller, root, page, order, bounds,
  cleanup/detach, signal, and survival checks.
- `EXP-20260813-041` completes offline M2.28. Both retained cycles in all
  three M2.27 arms reproduce the same exact pre-call set: all 145 changed
  records in the 13 entries reach their selected builder. Per-form control
  envelopes narrow the count-relevant surface to 18 entry/form groups and
  124 exact changed records, with a minimum aggregate 30-outcome gap. Exact
  single-record offsets `0x0174`, `0x0858`, and `0x0AA4` have individually
  discriminated bounded append outcomes; 121 record identities remain
  unresolved behind per-frame builder admission gates. This also corrects
  M2.27's `B4/B3` label from all builder calls to completed append paths;
  the measured M2.27 counts and 13-entry result remain unchanged.
- `EXP-20260813-042` completes M2.29. Static PC disassembly maps the only
  selected vertex-count writes to `0x004069A1/0x00407B00`, accounts for every
  earlier no-append return, and preserves the complete flush/reset boundary.
  Harness 1.4.0/schema 5 audits all 168 exact calls while retaining only 124
  candidate booleans/counts. Fresh accepted Direct3D
  control/replacement/control arms select one exact outcome outside both
  controls: entry 7/file offset `0x0A6C`/form `0x3C`, outcomes `0/1/0`.
  Thirteen records vary between controls. M2.28's three prior single-record
  outcomes do not reproduce, independently confirming per-frame admission
  variation rather than source-stable behavior.
- `EXP-20260813-043` completes offline M2.30. Exact record `0x0A6C` contains
  12 differences in four three-byte spans. Caller/builder data flow maps all
  12 to four separate byte-derived dwords in appended vertex records, but the
  builder first reads them only after successful count write `0x004069A1`.
  Every earlier admission input is identical at the source boundary or is
  per-frame state. M2.29's `0/1/0` receipt is therefore exact for those arms
  but not a source-stable append-decision attribution.
- `EXP-20260813-049` completes offline M2.34 with a cited four-gate matrix.
  The `.ANM` first-level format satisfies the multi-file/synthetic and unknown-
  preservation gates, and M2.20's exact whole-file `.ALL` copy is accepted and
  distributable as hash-guarded asset-free instructions. That audit kept M2
  active because no exact PC edge makes an M1 record or positive target select
  the ID-zero `CHARS/FLICK.ALL` path. M2.39 later deferred that unchanged gate,
  but `EXP-20260813-055` supersedes the deferral after finding an omitted exact
  finite producer surface.
  M2.23's shared arena cannot supply that edge: M2.26 proves it is selector-1
  software output.
- `EXP-20260813-050` completes offline M2.35 with a full negative for the
  exact M1 positive-target selector-2 surface. `0x0045A7F0` uses ten inline
  Direct3D allocation arms rooted through `0x004C4108/0x004C410C`; every
  page/list, root, flush, index, vertex-base, and emitted-record input derives
  from the M1 target/command stream, exact caller inputs, renderer globals,
  local derived scratch, or existing batch state. Structured xrefs and native
  tracing find no provenance from ID-zero header `0x005B18E0`, retained range
  `[0x005A9660,0x005A9DE0)`, or exact selected-resource state.
- `EXP-20260813-051` completes offline M2.36 with a finite current-invocation
  route negative for all eight retained generic header readers. Six are only
  possibly reachable in
  pre-coordinator update `0x004144C0`; `0x00444EF0` is initialization with
  exact index 11; and sole coordinator-local reader `0x00448350` runs before
  M1 root load `0x0044D4FA` and first record test `0x0044D57F`. Neither the
  `0x004498F0` selected-record closure nor `0x0045A7F0` positive-target
  closure contains a candidate. No M1-derived ID-zero selection is proved.
  Its consumer classification explicitly leaves the persistent values at
  `0x0059B730/0x0059B7B4` without a producer census; that omission is the
  bounded M2.40 surface, not a contradiction of the declared route negative.
- `EXP-20260813-052` completes offline M2.37 with an explicit gate-retention
  decision. The separate M1 and ID-zero renderer-facing chains cannot be
  merged without dropping the causal selection requirement. One finite
  `0x0044CA00` candidate remains: at most 20 selector words at
  `0x0059D9C0 + i * 0x30`; exact signed value `-103` would make the native
  header formula address ID-zero slot `0x005B18E0`. No such value or M1
  producer is yet proved.
- `EXP-20260813-053` completes offline M2.38 with a finite negative. Four
  native paths only clear the 20 exact selector words; sole nonzero writer
  `0x00467E60` copies one of 20 positive image-table values and has no
  `0xFF99` entry. Both direct writer calls consume the separate fixed
  64-record `0x84`-stride pool. The normal-update call occurs in
  pre-coordinator `0x0041EC40`, before `0x0044D430` loads and walks M1's
  `LEVEL*.DAT`-derived record root. No M1 record, relocated payload, or
  positive target produces signed `-103`; the candidate is retired.
- `EXP-20260813-054` completed M2.39 but is superseded in part by the
  adversarial `EXP-20260813-055` audit. The M2 gate and M4.1 technical
  boundary survive. Deferral does not: M2.36 had preserved exact index words
  `0x0059B730/0x0059B7B4`, slots 2 and 3 of the already bounded 64-record
  fixed pool, but M2.39 never censused their producers. Each directly selects
  `0x005B18E0 + I * 4` in `0x00436B40`, making zero an exact ID-zero
  discriminator. M2 is active on offline M2.40; M4.1 returns to planned.
- `EXP-20260813-056` completes the omitted M2.40 census. The complete bounded
  first-dword store set is pool clear `0x0041C430`, retained-source copy
  `0x0041BD24`, and conditional removal zero `0x0041BBBA`. Initial clear zero
  cannot pass the reader gates; late removal zero is statically
  reader-reachable because it occurs after active-list flag `0x4000` is set
  and does not clear that flag. Its value and predicate inputs derive from a
  separate `LEVEL.RAW` type-`0x23` record plus fixed-pool state, not an M1
  record, relocated payload, or positive target. The candidate is retired,
  M2 returns to deferred with `KU-023` open, and exact M4.1 is active.
- `EXP-20260813-057` rejects that second deferral without disturbing M2.40's
  slot-2/slot-3 result. The first audit had explicitly retained
  `0x0059D6A4` as lower-ranked slot 63, and M2.40 excluded it. Exact arithmetic
  also supplies the omitted classification of `0x0059C30C` as fixed-pool slot
  25:
  `0x0059B628 + 25 * 0x84 = 0x0059C30C`. Both first dwords feed exact generic
  `0x005B18E0 + I * 4` readers through fixed-pointer calls. M2 is active on
  offline M2.41; M4.1 returns to planned with its technical boundary intact.
- `EXP-20260813-058` completes M2.41 with a bounded causal negative. Slot 25
  zero can reach `0x00459620` initially or one update after removal; it selects
  the ID-zero header and takes that reader's zero-return arm because the
  header start word is zero. Slot 63 zero is excluded at two explicit
  `I == 0x23` calls but can reach three state-gated `0x004467E0` calls that use
  the ID-zero retained end index. The values and direct gates remain separate
  `LEVEL.RAW`, fixed-pool, scene/update, counter, and event state rather than
  M1 record/payload/positive-target data. M2 remains active only on independent
  fresh-context disposition audit M2.42; no worker-authored deferral is yet
  accepted.
- `EXP-20260813-059` independently completes M2.42 with verdict `ACCEPT`.
  Fresh rehash/disassembly reproduces M2.41's exact slot-25/slot-63 calls,
  gates, reader-time-zero paths, update order, and M1 negative. A separate
  retained-surface audit finds no exact finite PC-native successor in the
  evidence already cited through M2.41. This is not a whole-program absence
  proof. M2 is deferred with its causal exit gate and `KU-023` unchanged;
  exact hash-guarded, asset-free M4.1 is active.
- A scripted read-only runtime-evidence tooling suite exists under `scripts/`
  and is documented in [[Runtime Tooling]] (`DEC-20260812-019`): a GDB
  hardware-watchpoint harness, an `rr` record wrapper, `wine-capture.sh` relay
  and file-trace extensions, a frozen-frame capture, a `gcore` snapshot with a
  read-only core scanner, and an `apitrace` GL arm. All debugger automation is
  read-only (`write_verbs: []`).
- All six tools are **live-validated against the running game**
  (`DEC-20260812-020`, [[Runtime Tooling#Live validation results (2026-08-12)]]).
  The GDB harness and `core-grep` independently reproduced plant 10 slot value
  `0x006C342B` at `0x005B1AA4` (`RUN-GDB-20260812-182412`,
  `RUN-CORE-20260812-182803`), agreeing with the prior manual
  `RUN-GDB-20260812-153150`. Frozen-capture uses `gamescopectl screenshot`;
  apitrace needs `--api egl`; relay set/restore and metadata keys are
  confirmed. `rr` recording is blocked by Wine 11's in-kernel `ntsync` driver,
  whose ioctls `rr` cannot model (`KU-028`; not a GPU/disk issue); the fix is
  to remove `/dev/ntsync` (`sudo modprobe -r ntsync`) so Wine uses server-side
  sync. The `rr-record.sh` wrapper is validated and now refuses when
  `/dev/ntsync` is present. Three bugs found live were fixed with regression
  tests. This tooling did not change the active M2 packet.
- [[Reverse Engineering Capability Gaps]] now records the observed tooling
  limitations, current workarounds, acceptance tests, and authority boundaries
  that matter for continued RE. Fatal-signal control and the independent
  survival receipt are now proven; staged/predicate capture, deterministic
  reusable deterministic input replay, and an `rr`-compatible Wine environment
  remain. It is
  descriptive; [[Project Roadmap]] remains authoritative.

## What are we investigating?

**New-level authoring feasibility (2026-08-18 assessment).** A three-way survey
(PC level format, PC collision, PS1 authoring pipeline) is captured in
[[New-level authoring feasibility (PC)]] with cross-port leads in
[[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]].
Verdict: we can *edit within* existing levels and *read* collision bit-exactly,
but cannot *author new* geometry/collision. The linchpin is decoding the
render-geometry command grammar (`0x00405FE0`/`0x00407450` from `LEVEL.DAT`
command bytes; now tracked as `KU-079`). Collision is the *more* tractable half on
PC (uncompressed `TERRAIN.ALL`, read model exact). PS1 shipped a constrained new
level via a homegrown Blender→native pipeline (Fast64 the addon was never used —
only a naming analogy). **Experiment #1 is scoped** with go/no-go gates:
[[EXP-20260818-005 - Decode the render-geometry command grammar (scope)]] —
an early recon claim of an opcode function-pointer table was **refuted** — emission
is a type-switch feeding drawers that call the emit primitives directly. Gate A is
**complete** (walker `FUN_0044d430`→
`FUN_004498f0`→`FUN_00453ff0`→`thunk_FUN_00405fe0`; type-switch on `instance+0xe`,
reframed from a fn-ptr table to a count-prefixed vertex array in `LEVEL.DAT`). The
collision-writer + wall question is the lower-risk parallel track. Render and
collision are separate **datasets** co-registered in world space, but **not proven
free of runtime linkage**: `FUN_0044ca00` writes the collision descriptor table
`0x007F4590` and is reached from the render scene driver (`KU-081`), which refuted
a stronger "no index link" claim. **Gate B (2026-08-18)** tested the container grammar
against retail data — all 7 `LEVEL01` type-3 payloads chain exactly end-to-start —
but that chain only pins the 12-byte anchor stride (every group has
`prim_count == 1`, so every `skip + rec = 44` split chains identically — zero
discrimination); the record layout rests on instruction evidence. Semantics of the nine vertex `int16` and the world scale stay open. For this superseded type-3 branch,
Gate C (causal) is unrun. Important scope finding: **20 of 21 corpus files have no
type-3 records at all**, and `LEVEL01`'s are tall thin clustered quads (≈5.2:1) drawn by an
**explicit billboard** path (rotation set once per instance from a camera-related
global; only translation updates per group; objects carry Euler `(0,0,0)`), so
**type-3 is almost certainly camera-facing panels, not terrain**. **R0 and offline R1 have since decoded and consumer-linked the likely ground format**
([[EXP-20260818-006 - R0 the static mesh format and where visible ground lives]]):
a **static indexed mesh format**, validated **2,543/2,543 (100.00%)** over 146,030
face indices on the **retail** corpus (17 of 21 files carry the type) — `int32 vertex_count` + 12-byte vertices (three offset-named `int16` components + pad + three colour-plausible bytes *named by
position, not proven* + flag)
+ `u16 tag` + `u16 face_count` + faces whose indices are vertex **byte** offsets
(tag bit 0 = tri/quad). Large flat instances of it are the **candidate** ground
(circumstantial, not runtime-confirmed). [[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate|R1]]
links that payload to the exact PC drawer instructions, reconstructs all 2,543
retail type-`0x41` payloads byte-for-byte, and records one guarded Level03
fallback. [[EXP-20260818-008 - R2a Anthill static mesh causal candidate|R2a]]
selects the primary Anthill test at Level01 primary record 81, face 8, vertex
25: one guarded byte at `0x189FF` changes only that face by `+2048` on
consumer input component `+0x02`. The object and geometry are each referenced
once in Level01. Axis semantics and world scale remain open.
[[EXP-20260819-001 - R2b Anthill static mesh causal runtime|R2b]] completed
valid A1/B/A2 hardware-Direct3D arms, but only `108 / 307200` pixels were stable
across all 30 control frames, so the frozen `0.75` agreement gate failed before
effect classification. This is an inconclusive causal result, not a candidate
rejection, no-effect finding, or ground confirmation. R1 remains complete and
R2 remains open. Its successor needed a frozen observation state and an
independent test that the edited face contributes visible pixels.
[[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol|R2c]]
adds a bounds-checked guarded face-index editor, selects the evidenced
`t0 + 3.300 s` retail frame for per-process `SIGSTOP` calibration, requires
exact retail control-image and bounded view-block agreement, and specifies a
separate face-8 degeneration from `(300,312,264,324)` to
`(300,300,300,300)`. Runtime authorization is on record. F0-001 and F0-002
were software-renderer setup rejections before F0: neither sent carousel/title
input, signaled the process, read process memory, or wrote a DAT. At that
historical RC-branch point, F0 remained unrun and the derived localizer was
uncreated and prohibited until a
hardware-qualified F0 result is committed and James-accepted. The committed
next action at that time was RC0: a fresh no-direction chooser calibration classified only
by the complete renderer log, with one fresh one-Down RC1 fallback if RC0 is
software. Before that launch, map the exact full-disc arm through
`work/wine/baseline/dosdevices/r:` and require the frozen `CD.TXT` sentinel and
exact `App run from R:\PC\BUGS` plus `R:\PC\BUGS\cd\cd.txt` log identities.
`No CD-ROM found` alone is nondiscriminating. `$HOME/.wine/dosdevices/r:` does
not affect this launcher. RC0 preparations through RC0-F0-003 sent no renderer
or level input; the last exposed this prefix-scope error through `App run from
.`, a drive-less `\cd\cd.txt` fallback, and the fatal missing-file/CD prompt.
RC0-F0-004 then passed the installed-layout gate and
reached the actual owned `640x480` `Bugs` chooser, but an interactive
ImageMagick capture waited until its timeout selected software; no input was
sent, so it did not consume RC0. RC0-F0-005 passed the source/prefix/CD/PID/
window gates but disproved the X11-root capture: its live frame and both
`capture-fixture-002` frames are the same uniform black PNG
`724319c36...c6931`, not game pixels. Receipt/guard failures then allowed the
chooser timeout; no experiment input, signal, read, or DAT write occurred, and
the fully retained cleanup ended clear with retail `R:` restored. The raw
packet is in the rejected namespace and RC0 remains unconsumed. Active capture
is restored to asynchronous `gamescopectl screenshot`, with strict non-black,
non-uniform, exact-`640x480`, stable, known-chooser presence gates. The
historical `scripts/r2c-rc0-executor.py` owned the retail RC0 lifecycle; the
RC0-F0-006 executor run then rejected before Return when its three captures
showed two startup/fade transitions (`9124b62c...d6413`,
`64a124c5...94359`) followed by the known stable chooser. Those transition
hashes are not allowlisted; no direction, Return, F0 signal, memory read, or DAT
write occurred, and guarded cleanup ended with a clean audit and retail `R:`.
The RC0/RC1 branch and its `RC0-F0-retail-007` /
`evidence/pending/RC0-F0-007` pickup are now superseded history and must not be
launched.
It requires baseline `R:` to start at retail, bounds `gamescopectl` itself to
`3.000 s`, uses the direct guarded XTEST Return sequence rather than
fixture-only `send-keys.py`, rehashes immediately before input, and performs a
fixed `4.000 s` guarded no-input settle plus three captures inside one absolute
`45.000 s` launch-to-Return deadline. Per-capture command receipts and image
observations are persisted atomically before the triplet verdict. It performs
a final live PID/window/mapping/hash guard before hardware handoff. Handoff is
committed only after its receipt writes successfully, and every disposition
records Return delivery as not attempted, failed before keydown, attempted
ambiguous, or completed. Fresh guards must resolve the current
`SELECTOR_WINDOW` and require the same-PID `640x480` `Bugs` window. The
localizer result/evidence packet must be committed and accepted
before the one-byte vertex candidate resumes; derived game data remains
excluded from git.

Historical R2c freeze-calibration pickup was the argument-free
`scripts/r2c-f0-auto-hardware.py`. It stages exact retail assets at
`F0-auto-hardware-retail-009` but executes the canonical accepted cache
`work/copies/auto-hardware/bugs.exe`, exact hash `1e1d5099...a9c41f`.
The executor proves both patched spans, the exact nine-byte difference set, and
inverse-to-retail hash; maps the exact stage through baseline `R:`; requires all
six Direct3D markers; sends only `Right`, `Return`, `Return`; freezes the exact
PID at title-keyup `t0 + 3.300000000 s`; performs only the authorized bounded
reads `(0x00861c84, 4)` before title Return and `(0x005b58e0, 18)` plus
`(0x005bdb8c, 12)` while stopped; requires the exact Level01 load/ClearLoadScreen
log identities and two independently reproduced decoded-RGB title-region hashes
(`360x150+275+120` -> `da63e765...1eddb3` and `590x70+25+285` ->
`0ae2bd62...48efe`);
uses a process-bound `pidfd` for `SIGSTOP`/`SIGCONT` while continuously guarding
the same focused owned window with every X11 query bounded by the remaining
freeze deadline; creates its canonical accepted/rejected evidence namespace
parents itself while requiring each final arm path to be fresh; requires all
three stopped captures to match four exact retail/derived camera regions and
the derived `-006` reproducibility reference PNG
`05f5691c...506ad1c` / RGB `2ea65643...23b9d26c`; resumes, closes, audits, and
restores retail `R:`. Unresolved cleanup or restoration leaves evidence pending.
A pass supports only a hash-scoped derived-build claim.

`F0-AH-008` is retained under `evidence/pending/` as an unclassified
pre-action identity-tooling rejection. It failed immediately after discovery,
before the renderer gate, input, signal, memory read, capture, or DAT/write
boundary. The old packet did not retain the compared discovery candidates, so
the exact changed field is unknown; its otherwise clear process/device cleanup
and retail-`R:` restoration must not be converted into an invented diagnosis.
Fresh `F0-AH-009` persists every candidate and exact field diff, permits only
same-PID/start/process-group startup command/cwd stabilization, and assigns the
game only after two consecutive identical exact-final observations. Missing
`bugs.log` is explicitly receipted and benign only before the renderer/log gate.
The previous PID's raw current identity is compared before filtering, and
post-snapshot plus post-receipt timestamps must remain before the absolute
pre-Return deadline; either identity drift or deadline crossing blocks all
later action.

`F0-AH-009` then passed the complete derived-build freeze calibration. All six
Direct3D markers, exact Level01/title/index gates, exact-pid stop/resume, all-17-
tasks-`T` gate, authorized view snapshots, four structural regions, and three
identical reference frames passed. The frozen frame is PNG
`05f5691c...506ad1c` / decoded RGB `2ea65643...23b9d26c`, and visual review
shows non-faded Anthill Level01 gameplay. Final and independent post-run audits
are clean, retail `R:` is restored, and no DAT/runtime/debugger write occurred.
This is a derived-build calibration result only. James accepted its committed
result. The next offline packet freezes an argument-free exact face-8 creator,
fresh C1/L/C2 executor, and provenance-bound comparator anchored to the accepted
derived frame/view hashes. No localizer DAT or arm exists yet; create/launch
remain blocked until that post-F0 packet is committed and James-accepted. No
causal, ground, retail, or R2-closure claim follows from F0.

`F0-AH-001` is a consumed pre-input rejection: exact identities and the full
hardware log passed, but a single main-window query immediately after the sixth
marker found zero windows. No input, signal, process-memory read, capture, or
DAT write occurred; cleanup and retail `R:` restoration are clear. The `-002`
executor now waits within the existing absolute launch deadline for exactly one
same-PID, named `Bugs`, `640x480` main window. Zero means not-ready; multiple,
wrong identity, process drift, software/mixed evidence, or deadline expiry
rejects. Every launched packet retains its final `bugs.log` before cleanup.

`F0-AH-002` is also a consumed pre-input rejection. It retained the complete
hardware log but counted two same-PID Wine windows before inspecting their main-
window properties. Its `-003` successor historically added complete per-poll
window receipts; those receipts then disproved the assumed exact-`Bugs` title
and established the loading-title contract described below. Neither gate is
active.

`F0-AH-003` is a consumed pre-input rejection that retained 485 consistent
polls of exact same-PID `640x480` XID `14680071` titled
`Loading - A Bugs Life`, plus only a 1x1 IME helper; its log reached LevelSelect.
The `-004` gate accepts that exact initial title/XID, never rediscovers a
replacement, targets only it for `Right`/`Return`/`Return`, and permits only a
retained same-XID title transition between `Loading - A Bugs Life` and `Bugs`.
Unknown title, replacement/disappearance, duplicate qualifying window,
PID/owner drift, or geometry drift rejects before the next action.

`F0-AH-004` is a consumed navigation-readiness rejection. Guarded Right and
Return completed, but the log remained Level00/LevelSelect with no Level01 or
`Start ClearLoadScreen`; the later index `0` therefore does not prove a read
race. The `-005` executor waited for exact LevelSelect, performed a fixed
`1.000 s` no-input settle before Right, then requires exact Level01 plus
ClearLoadScreen log markers within `10.000 s` before any title capture or
memory read. Only a reviewed title and fresh full identity guard permit the
single authorized level-index read; non-`1` then means state inconsistency.
Marker observation/poll count are retained before guards or settles, and every
success-path guard/settle plus its post-check must remain inside the same
navigation deadline; expiry prohibits the next action.

`F0-AH-005` is a consumed title-identity rejection, not a navigation failure.
It reached the genuine Level One title after the exact Level01/ClearLoadScreen
markers, but ordinary nonidentity animation produced a new full-frame PNG/RGB
pair. James accepted its rejection and cleanup; no index read, title Return,
signal, stopped read, or DAT write occurred. That `-006` gate does not
allowlist that whole frame. It requires exact `640x480` decoded RGB and the two
fixed title regions reproduced across the independently reviewed A1/B, A2, and
`-005` frames. Full-frame hashes are retained only as evidence. Failure of
either region stops before every later runtime action.

`F0-AH-006` is a consumed whole-frame transport rejection after an otherwise
successful controlled freeze. It passed index `1`, pidfd `SIGSTOP` timing, all
17 task states, four stable authorized view snapshots, and three identical
stopped captures; it resumed and cleaned without a write. The derived frame
`05f5691c...506ad1c` / `2ea65643...23b9d26c` differs from the retail R2b phase
reference at 18,613 pixels, primarily animated entities, while four fixed
camera/terrain crops are exact across all six retained retail/derived inputs.
Historical F0 packet `-007` required those four hashes and exact reproduction of the
derived frame. A second derived whole-frame identity ends hash extension and
requires a new state predicate/mask design. The localizer remains blocked.
`F0-AH-007` is separately consumed as a pre-signal scheduler rejection, not a
reproducibility result. Of 80 total main-window guard receipts, 70 are post-`t0`
freeze-interval iterations (`011` through `080`); their old in-memory aggregate
focus receipt was lost. Final process identity completed with `4.346 ms`
remaining, then the full XID guard consumed most of that budget before geometry
launched with a `0.255 ms` timeout and failed. No signal,
stopped read, or frame exists. Historical `-008` ended periodic sampling at
`deadline-0.060`, completes the final full guard by `deadline-0.003`, reserves
the last 3 ms for pidfd signal scheduling, and immediately persists every focus
sample and any pre-signal failure. Its four region and derived-frame hashes are
unchanged.
Retail confirmation remains mandatory before visible-ground, retail behavior,
or retail-R2 promotion. The localizer and one-byte candidate remain blocked.
The full dependency-ordered program (render/collision/materials tracks,
acceptance gates, and historical program context; current R2 state is recorded
in the dated updates below) is
the **pickup note**
[[New-level authoring roadmap (terrain, collision, materials)]] — resume there.

Roadmap milestone M4 is Complete. Exact independent M4.44 accepts M4.43's
selected-link identity correction while retaining M4.41's recursive-order and
typed-ID corrections and every accepted M4 boundary.
M4.38 independently accepted M4.37's complete-tree case-
insensitive path-uniqueness correction. Exact M4.33 independently accepts
M4.32's exception-safe receipt-chain closure after M4.31 retained M4.30's
parent-change refusal but rejected its stop-on-first-close cleanup. The M4.27 evidence ledger in
`EXP-20260814-086` rejects milestone closure: current documentation explicitly
said the receipt alone was insufficient, and the clean-derived-copy install/
validate/launch/remove gate also remains unjoined.
`EXP-20260814-069` rejects M4.9's complete-preflight claim because a
pre-existing bind-mounted directory inside an otherwise exact overlay can be
mutated before removal fails `EBUSY`. `EXP-20260814-070` supplies only the
bounded M4.11 worker correction and four isolated root/intermediate/output/
receipt cases. Independent `EXP-20260814-071` preserves those exact-path and
ordinary results but rejects the universal claim: `_validate_unmounted_deletion_plan`
does not inspect the proper parents traversed to reach the resolved overlay
root, and a stable alias there can remove an independent overlay while cleanup
returns success. M4.13 adds that proper-ancestry classification, but independent
`EXP-20260814-073` finds one ordinary-filesystem false positive: a lower alias
covered at the same pathname by a distinct ordinary top filesystem remains in
the pathname-only alias set. `EXP-20260814-074` supplies the bounded M4.15
worker correction: same-path parent-stack coverage removes only hidden lower
records from both candidate and source comparisons. The exact ordinary-top
case now removes safely and every prior refusal/positive control survives.
Independent `EXP-20260814-075` preserves that exact correction but falsifies
the “every uncovered alias” condition. Linux reused freed mount ID 1081 for a
newer bind alias to a still-mounted ID-1082 source; numeric-ID ordering omitted
the alias and removal changed the independent target. M4.17 was limited to
that reuse-order defect while retaining all covered-stack and accepted gates.
`EXP-20260814-076` completes that bounded worker correction. Current Linux
`listmount(2)` supplies explicit later-first unique IDs and `statmount(2)` maps
them back to the mountinfo legacy ID, parent, and device; invalid, incomplete,
inconsistent, or changing snapshots fail closed. Alias comparison now uses the
verified order, so the exact reused-lower-ID alias refuses unchanged while the
covered ordinary-top success and prior refusals survive. Independent
`EXP-20260814-077` verifies the exact current-x86_64 ABI/order, exhausts the
declared fail-closed injections, independently reproduces old-ID reuse and
pre-traversal refusal with all four snapshots unchanged, and retains every
namespace/parser/removal/M4/M1/local gate. M4.18 returns `ACCEPT`.
`EXP-20260814-078` completes exact M4.19 at the worker boundary with one strict
asset-free v0.1 statement/checker. `EXP-20260814-079` independently confirms
its bytes, anchors, current declarations, and no-game-read boundary, but
rejects the claimed authority-drift gate because an expected substring can
coexist with a later effective override. `EXP-20260814-080` completes only that
M4.21 correction at the worker boundary through source-aware shell/Python/
generated-row/scoped-Markdown extraction. All four exact contradictions and
adjacent cases reject. `EXP-20260814-081` preserves those results but rejects
M4.22 because post-declaration shell/Python changes and duplicate manifest keys
still pass alignment. `EXP-20260814-082` completes exact M4.23 at the worker
boundary: five same-read machine-authority pins reject all six residual
families, focused/full suites pass 47/340, and the exact statement/nine-read
asset-free scope survives. Exact M4.24 then owned independent acceptance.
Fresh-context `EXP-20260814-083` returns `ACCEPT`: independent statement/hash/
pin-set reconstruction, all ten predecessor attacks, five direct mutations,
five missing-pin cases, three scoped human checks, exactly nine unique reads,
47/152/340 tests, and every hygiene gate pass. `EXP-20260814-084` now supplies
the bounded dry-run affected-file/record/byte-range report at the worker
boundary with 99/161/349 tests and exact snapshots. Fresh-context
`EXP-20260814-085` returns `ACCEPT`: direct packed-byte reconstruction covers
schema-valid operations, primary/secondary records, sequential/no-op and
empty/unequal cases; 91 assertions across 20 cases, 38 compatibility
assertions, write traps, exact snapshots, exact receipts, and every hygiene
gate pass. Exact M4.27 then reconciles all 14 written rows in
`EXP-20260814-086`. Eight of nine capabilities and four of five exit gates are
supported. Receipt sufficiency is directly contradicted by the manifest-
required removal contract, and staged launch versus sparse removal does not
form one accepted clean-copy lifecycle. `EXP-20260814-087` completes only the
smaller M4.28 worker correction. `replay` requires a new sparse root;
`remove-receipt` shares current-Linux authenticated removal; strict descriptor
and ordinary-byte checks precede exact current-schema reconstruction and full
receipt recomputation. Forty-seven new focused cases pass, totals are
146/208/396, and all three local families replay/remove twice with prior hashes
and unchanged sources. The receipt is not a provenance/signature claim and
post-preflight I/O remains non-transactional. `EXP-20260814-088` now returns
`REJECT`: both current format mappings, 80/80 strict input cases, 146/208/396
tests, a 37-case removal/mount/topology selector, six local cycles, five pins,
and nine reads pass, but 2/2 deterministic parent-change fixtures are accepted
instead of rejected. The final receipt descriptor remains the same inode, so
its checks cannot observe that an already checked parent changed into a
directory link and moved below a disallowed location before `open`.
`EXP-20260814-089` now retains and reacquires every no-link component before
parsing, rejects the exact bypass and adjacent changes, and passes 154/216/404
tests plus six local cycles. Independent `EXP-20260814-090` preserves all of
that evidence but returns `REJECT`: an injected first close error skips six
later closes and leaves seven descriptors open; the next-close injection
leaves six. Exact M4.32 owns only exhaustive exception-safe chain release;
`EXP-20260814-091` now attempts every owned descriptor once, preserves primary
errors, blocks parsing on cleanup-only failure, passes 161/223/411 tests and
six local cycles. Independent `EXP-20260814-092` reproduces the parent +7/+6
defect, then passes 28/28 fresh indexed close cases with exact identity/order/
multiplicity and zero real descriptor deltas, retains all workflow/local/
compatibility gates, and returns `ACCEPT`. `KU-051` is resolved. `KU-052` and
M4 remain open. Exact M4.34 independently rebuilds the four-route same-tree
ledger and returns `REJECT`: full staged/forced-copy trees are structurally
launcher-ready but sparse removal rejects their required extra content before
mutation; sparse apply/replay trees remove correctly but contain no executable.
`EXP-20260814-094` now completes the exact M4.35 worker. One new `restore`
command authenticates complete source/game path/type/content equivalence except
for exact outputs/receipt, rejects mounted or nonordinary full-tree paths, and
restores only recorded destinations. Twenty-seven focused instances pass;
focused/combined/canonical totals are 188/250/438; the retained local sparse
cycles and one exact 722-file stage/launcher-dry-run/restore lifecycle pass.
Fresh-context `EXP-20260814-095` retains those ordinary, mount, local, and
canonical results but returns `REJECT`: exact-spelling inventories allow both
`Case.bin` and `case.bin`, and restoration accepts the resulting ambiguous
Windows tree. `EXP-20260814-096` completes only the M4.37 correction: a shared
case-fold key spans every source/game file and directory, source collision
checks precede preparation, eight collision families refuse unchanged, and
198/260/448 tests plus the exact local lifecycle and sparse recipes pass.
`EXP-20260814-097` independently accepts that exact worker after 36 fresh
collision cases, four bind-mounted sibling-order cases, all eight namespace
families, five identity swaps, the exact local lifecycle, six sparse cycles,
five pins/nine reads, and 198/260/448 tests. `KU-052` resolves only at the
demonstrated current-Linux manifest-driven lifecycle. The v0.1 statement
remains immutable; `EXP-20260814-098` publishes strict v0.2 at the worker
boundary with only that accepted restoration scope and five unchanged pins.
`EXP-20260814-099` retains the restoration truth, both exact statement hashes,
five pins, and exactly nine asset-free reads but rejects final closure for
cross-version selected-path acceptance, reordered-object-field acceptance,
and an uncaught unhashable-ID error. Exact suites pass 58/271/459; the prior
combined count 266 was stale. `EXP-20260814-100` rejects those exact attacks,
all 151 value and type mutations, and retains both nine-read normal checks;
exact suites pass 71/284/472. `EXP-20260814-101` retains the statement bytes,
semantic boundary, pins, ordinary reads, and accepted ledger evidence but
returns `REJECT` on the default-active-path link case. `EXP-20260814-102`
rejects both selected link directions before reads and preserves arbitrary
unselected exact links; exact suites pass 75/288/476. `EXP-20260814-103`
independently retains those results, extends the selected nonregular/alias/read
matrix, reconstructs both exact contracts and pins, and closes the last
compatibility row. The M4 ledger is 9/9 capabilities and 5/5 exit gates only at
the documented current-Linux/asset-free boundary; no new milestone is active.

M2 is deferred, not complete. `EXP-20260813-059` accepts M2.41 and finds no
exact finite PC-native successor retained in the already cited evidence, but
the causal dependency exit gate and `KU-023` remain open. Revisit M2 only for
an exact cited PC-native candidate, a bounded discriminator supplied by a
concrete mod goal, or a contradiction to a completed negative.

## What is confirmed?

- PE image base `0x00400000`; entry VA `0x004B1670`.
- `0x00403B90` displays the CD dialog only when `0x004AE240("cd.txt", buffer)` returns zero.
- `0x004ADC30` checks the current drive and then scans `C:` through `Z:` for the first `GetDriveTypeA` result 5.
- Wine's directory-backed `R:` type override was not accepted by that game scan.
- From disc root, fallback loading attempted missing `R:\\cd\cd.txt`.
- From `R:\PC\BUGS`, the same executable hash loaded `R:\PC\BUGS\CD\CD.TXT` and continued.
- The continued run selected Direct3D HAL through WineD3D, 640×480×16 fullscreen mode, and loaded `level00\level.raw`.
- The software renderer starts a 320×200 surface, whereas the selected hardware path starts Direct3D at 640×480×16. Under the tested Gamescope `fit` configuration, compositor captures measured an approximately 1920×1440 centered 4:3 presentation on the 2560×1440 host (`EXP-20260812-007`).
- Training loads `CD/LEVEL07/LEVEL1.DAT` and reaches playable rendering under Wine 11 staging (`EXP-20260812-005`).
- `0x0044BB70` walks the bounded `LEVEL*.DAT` prefix documented in [[PC LEVEL DAT prefix]]; `0x0044D430` independently consumes the 20-byte records spatially.
- Manifest output changing the first candidate-center components at `0x0E60`,
  `0x0E74`, and `0x0E88` is accepted by the original executable under
  `S:\PC\BUGS` and visibly removes a central foreground flower cluster
  (`EXP-20260812-006`, interpretation corrected by `EXP-20260812-011`).
- Global `0x005BA240` stores the loaded DAT buffer pointer; it is not the buffer itself. Native read watchpoints confirm records 124–126 all reach `0x0044D5B8` inside `0x0044D430` (`RUN-GDB-20260812-021920`).
- Individually forcing record 124, 125, or 126 outside selection produces a
  distinct, disjoint visible plant-element difference in matched 640×480
  Direct3D captures. They are not three alternative LOD representations of one
  on-screen object in the tested Training start state (`EXP-20260812-008`,
  `EXP-20260812-011`).
- Records 125 and 126 share the observed internal payload target at file offset `0x111E4`; record 124 instead targets `0x1319C` at the same payload field (`EXP-20260812-008`). `EXP-20260812-010` confirms a placement-local visible-content role while complete target semantics remain unknown.
- For flags `0x0059`, `0x0044BB70` relocates payload `+0x1C`; the masked `0x49` path in `0x004498F0` passes that pointer to `0x0045A7F0`. The latter consumes a positive count, a `count × 12` entry table, variable 12-/16-byte command items, and a `0xFFFF` terminator (`EXP-20260812-009`).
- Training's 262 primary records reference 109 unique positive-count target blocks. Nineteen are shared; `0x111E4` has 11 primary references and `0x1319C` has 17. All 109 bounded blocks are adjacent from `0x38DC` to `0x19E00` (`EXP-20260812-009`).
- Across the local 21-file PC corpus, all 990 records in 14 files satisfying `(flags & 0xBFEF) == 0x49` resolve to valid positive-count target blocks under the bounded inspector. This claim does not cover other dispatches or negative-count blocks (`EXP-20260812-009`).
- Rebinding record 124 from target `0x1319C` to `0x111E4` changes 2,980
  phase-matched pixels only within `61x242+369+0`; rebinding record 125 in the
  opposite direction changes 1,076 pixels only within `24x127+616+101`.
  Both regions overlap the placements independently isolated by move-away
  edits in `EXP-20260812-008`; no pixels outside the unions differ
  (`EXP-20260812-010`).
- Renderer-facing RE uses the second initial option and must prove
  `Screen mode 640x480x16 selected` plus `Starting Direct3D renderer` in the
  game log. `INITSOFTRENDER` runs are not hardware controls
  (`DEC-20260812-009`).
- In `0x0044D430`, record `+0x00`/`+0x04`/`+0x08` feed candidate-center tests;
  `+0x0C` feeds the center-distance and projected-screen bounds. At
  `0x00449B61`, dispatch `0x49` switches to relocated record `+0x10` before
  reading the payload placement tuple (`EXP-20260812-011`).
- Record-126 `+512` edits at `+0x04` and `+0x08` are accepted and have an exact
  control-identical hardware frame; they do not move its rendered content in
  the tested camera (`EXP-20260812-011`).
- Reducing record 125 positive signed `+0x0C` from `1259` to zero removes only
  its partially visible right-edge content in matched phases. The first local
  comparison differs by 756 pixels within `25x109+615+158`; outside it, zero
  pixels differ (`EXP-20260812-012`).
- The hardware-gated `ant hill` menu selection loads
  `CD/LEVEL01/LEVEL.DAT`, SHA-256
  `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
  Record 261 begins at `0x2968`, uses payload `0x4E00`, and points at positive
  target `0x3703C`; guarded rebind target `0x3459C` is also a valid same-file
  positive block (`EXP-20260812-013`).
- Record-261 center and target candidates change only `0x2968–0x2969` and
  `0x4E1C–0x4E1D`, respectively. Both load Level 01 and reach `NextLife` under
  Direct3D. Frame 03 is byte-identical across unchanged, center, and rebind
  runs, so neither edit is visible at the tested start camera
  (`EXP-20260812-013`).
- M1.5 re-staging reproduces Training record-124 target output SHA-256
  `b8012a95…f720e` and Level 01 record-261 target output SHA-256
  `80649462…9965b`, with receipts byte-identical to their retained accepted-run
  receipts. No runtime rerun was required because emitted bytes did not change.
- `inspect --payload-targets primary` now succeeds on the exact Level 01 DAT
  and reports its nine supported references/four unique targets; unrelated
  dispatch/negative layouts are outside that view. The unchanged corpus scan
  remains 21 files, 14 with supported records, 990 parsed references, and zero
  errors.
- `EXP-20260812-014` inventories 721 files / 460,306,509 bytes in the exact
  derived PC tree with fingerprint
  `b145e2aa5fbf7e3350cf437985bbc76c764c36f2d954105d5282af4831738986`.
  The Training log has 25/25 matched explicit paths and the Level 01 log has
  45/45; their union is 51 files and their intersection is 19.
- `CD/PLANTS` contains 11 basename-matched `.ANM`/`.ALL` pairs. Nine pairs are
  observed in at least one retained log, and plant 04, 05, 06, and 10 pairs
  occur in both. This confirms only a useful PC-native trace set, not common
  layout semantics or a dependency from an M1 record.
- `0x00416100` builds the plant-ID request list; `0x00445020` maps IDs to exact
  base strings and calls `0x00444C40`. Selected call sites are plant 04
  `0x0044575E`, 05 `0x004457B5`, 06 `0x0044580C`, and 10 `0x00445968`
  (`EXP-20260812-015`).
- `0x00444C40` appends `.anm` at `0x004DDC14`, loads at `0x00444CD8`, advances
  its caller's arena cursor by aligned file size, and calls relocator
  `0x00444B70`. `0x00448010` appends `.all` at `0x004DE028`, loads at
  `0x00448079`, and advances the same cursor from embedded lengths without
  consuming the loader's returned byte size (`EXP-20260812-015`).
- For plant 10 resource ID `0x71`, the ANM pointer destination is exact slot
  `0x005B1AA4`. In `RUN-GDB-20260812-153150` it holds `0x006C342B`; runtime
  ANM words `+0x04/+0x06 == 66/68` bound two `0x50`-byte entries at
  `[0x005AAB00, 0x005AABA0)` (`EXP-20260812-021`).
- Training requests plant pairs 05, 04, 10, 06; Level 01 requests 05, 07, 04,
  10, 09, 03, 08, 02, 06. Every `.anm` immediately precedes its `.all`,
  independently matching the static coordinator sequence. The four shared
  `.ANM` files pass a first-level offset-bound check and are selected for the
  active bounded inspection packet; `.ALL` is not yet promoted.
- `0x00465030` copies a `LEVEL.RAW` type-35 block into `0x00599EB0`, and
  `0x0041C420` transforms it into the 64-entry table rooted at `0x0059B628`.
  Separately, `0x0044BB70` writes a type-`0x3F` DAT top-record pointer to slot
  63 at `0x005C595C`, the second input read by `0x00416100`
  (`EXP-20260812-016`).
- In Training, type-`0x3F` selectors `+`, `+`, and `,` at exact file offsets
  `0x394`, `0x3A4`, and `0x3B4` map through executable tables to plant IDs 4,
  10, and 6. Their first-occurrence order after literal 5 matches the retained
  hardware load log. Level 01 supplies an independent same-code/file-layout
  correlation (`EXP-20260812-016`).
- Those selectors lie in `[0x4, 0x3E8)`, before Training's primary record start
  at `0x4B0`. This confirms a same-DAT separate-table dependency, not an M1
  scene-placement/payload-to-resource identity (`EXP-20260812-016`).
- `0x00444B70` reads signed count `+0x02`, relocates nonzero dwords from
  `+0x08`, retains the first nonzero reference, then reads an unsigned nested
  count at referenced `+0x08` and signed words from `+0x0C`. Only `-2` is
  distinguished in this routine (`EXP-20260812-017`).
- Caller `0x00444C40` overwrites in-memory ANM words `+0x00` and `+0x04`
  before the consumer; their zero values across all 11 files are therefore not
  runtime semantic constants. The consumer receives no file-size argument,
  while the independent inspector bounds every read against exact size.
- `ablpc-mod inspect-anm` and `scan-anm` preserve the exact input bytes, emit
  metadata only, and expose no editing. Sixteen synthetic ANM tests and all 11
  exact PC plant files pass; the full repository suite is 38 tests
  (`EXP-20260812-017`).
- Replacing only staged `PLANT04.ANM` with exact `PLANT10.ANM` bytes changes
  884 bytes at offsets `0x26–0x708`, leaves `PLANT04.ALL` unchanged, and is
  accepted by the exact executable under the Direct3D hardware path. Both
  matched logs load plant 04/10 pairs, end `InitMainGame`, and reach `NextLife`
  (`EXP-20260812-018`).
- After drive-letter and diagnostic timing normalization, the M2.5 control and
  replacement logs are byte-identical. Closest-frame and temporal-median
  differences do not expose a stable replacement-only region and are
  comparable to control-to-control animation variance. This is confirmed only
  as accepted-no-visible-change at the tested Training start camera, not as
  general `.ANM` interchangeability or irrelevance (`EXP-20260812-018`).
- Replacing both staged plant 04 paths with exact plant 10 `.ANM`/`.ALL` bytes
  changes only those two paths: 884 ANM byte positions at `0x26–0x708` and
  3,087 ALL positions at `0x4–0xDEF`. The exact executable accepts the pair
  under Direct3D and reaches Training `NextLife` (`EXP-20260812-019`).
- The accepted M2.6 logs each contain 1,480 lines and normalize byte-identically
  to SHA-256 `73a6a08e…25110`. The temporal-median replacement RMSE
  `0.0357224` lies within the independent M2.5 control-to-current-control range
  `0.0267928–0.0387554`; no stable paired-replacement start-camera region is
  discriminated (`EXP-20260812-019`).
- Runtime payload-pointer watchpoints route records 124–126 through
  `0x00449B61 → 0x00449E20` with expected targets `0x0066C273`,
  `0x0066A2BB`, and `0x0066A2BB`. From each dispatch stop through renderer
  return `0x00449E25`, no read occurs at plant 10 slot `0x005B1AA4` or the
  two object-entry `+0x20` dwords. This is a three-address, three-window
  negative result, not a whole-range or lifetime absence claim
  (`EXP-20260812-021`).
- In `RUN-GDB-20260812-155922`, hardware read watchpoints on
  `0x005AAB20`, `0x005AAB70`, and `0x005AAB24` remain unhit from the natural
  Training title start through logged `NextLife` and exactly 71.708204459
  seconds of live gameplay. Static instructions `0x004480B4–0x004480F6` map
  the first two ranges to entry-relative `+0x20`; `0x0044596D–0x00445AFA`
  maps the third to caller-adjusted `+0x24/+0x26` (`EXP-20260812-022`).
- In `RUN-GDB-20260812-161520`, accepted watches begin only after unique plant
  10 post-call `0x0044596D` and its immediately following common-tail
  `0x00445B01`. None fires before batch return `0x004679C7` or the natural
  title; all values remain unchanged. Static instructions prove
  `0x00445B01` is shared, so the earlier unguarded zero-value stop is rejected
  (`EXP-20260812-023`).
- In matched `RUN-GDB-20260812-163111` and `RUN-GDB-20260812-163840`, both
  plant 10 entry heads are exactly `0/0/0/1`. No CPU read overlaps either
  entry's `+0x00/+0x04/+0x08` dwords after guarded final population, through
  `0x004679C7`, or while execution crosses the title to captured live
  gameplay. Input advanced both titles, so no unattended title-pause capture
  is claimed (`EXP-20260812-024`).
- In `RUN-GDB-20260812-165837`, neither exact plant 10 entry `+0x0C` dword is
  read after guarded final population, before `0x004679C7`, or while
  execution reaches a retained no-input Training title. Both values remain
  `1`. Static instructions place candidate reads `0x00446A97/0x00447668`
  behind selected-entry `+0x2E` gates (`EXP-20260812-025`).
- In `RUN-GDB-20260812-195759`, neither exact plant 10 entry `+0x2E` word is
  read after guarded final population, before `0x004679C7`, or while
  execution reaches a retained no-input Training title. Both values remain
  unsigned `1`. Therefore neither exact entry reaches the comparisons at
  `0x00446A8A/0x00447661` within the retained window
  (`EXP-20260812-026`).
- In `RUN-GDB-20260812-201419`, neither exact plant 10 entry `+0x28` word is
  read after guarded final population, before `0x004679C7`, or while
  execution reaches a retained no-input Training title. Both values remain
  unsigned zero. Exact store `0x0044810B` independently identifies the watched
  field; zero is not classified as padding or unused (`EXP-20260812-027`).
- Exact instructions `0x0044CE0D–0x0044CE3E` select a pointer from
  `0x005B1A7C` using a source-record-relative signed word, read header bounds
  `+0x04/+0x06`, derive `0x005A9660 + start * 0x50`, and read entry `+0x2E`.
  Plant 10's measured slot/header make this a static post-title candidate, not
  a runtime-confirmed plant 10 consumer (`EXP-20260812-027`).
- In `RUN-GDB-20260812-203714`, neither exact plant 10 `+0x2E` word produces
  an access stop from the natural title through `NextLife`. A separate
  30.026628-second post-`NextLife` watch arm also records zero stops, and a
  separate 10.014330-second exact-reader control records no execution of
  `0x0044CE3E` (`EXP-20260812-028`).
- Static value-1 handling after `0x0044CE3E` branches to `0x0044CFC4`; its
  first call is `0x0044D079 -> 0x004012C6 -> 0x00463770`, where three dwords
  are copied between exact argument-relative offsets. The accepted M2.15 arms
  do not reach this branch for plant 10, so no semantic name is assigned.
- Exploratory `RUN-GDB-20260812-204252/204333` do not establish a caller chain:
  raw GDB output records `SIGSEGV` at instrumented PC `0x0044D79A`, which the
  structured cleanup/detach result does not surface; Wine prints the matching
  fault. They are incident evidence only
  (`EXP-20260812-028`, `KU-031`).
- Fresh `RUN-GDB-20260812-211649` reproduces the contradiction with both
  caller/callee breakpoints and both exact data watches armed simultaneously.
  The only valid stop is outer gate `0x0044D79A`, with `AL == 0x40`, caller
  byte `0x40`, caller dword `0x00000680`, and the plant 10 slot/header still
  `0x006C342B` and `1/3/66/68`. Raw GDB immediately records `SIGSEGV` at that
  PC; Wine opens its debugger, and the game-only survival frame is a fatal-
  error dialog. Structured `target_reached`, cleanup/detach, and appended
  `NextLife` are therefore insufficient survival proof (`EXP-20260812-029`,
  `KU-031`).
- In synthetic M2.17 validation, a trigger-file-controlled `SIGSEGV` after
  GDB attachment produces `target_signal`, records signal/PC and
  `stop-print-nopass`, deletes its point, detaches, and leaves the fixture live,
  resumed, and untraced in three samples. A real exited-process probe fails
  closed, while the routine `SIGUSR1` case retains normal pass-through
  (`EXP-20260812-030`).
- Safe live `RUN-GDB-20260812-214545` watches exact slot `0x005B1AA4` and
  reproduces PCs `0x00445089/0x00444C58/0x00444D0C/0x00445973`, with the last
  two samples containing little-endian `0x006C342B`. After deletion/detach,
  five independent samples report process state `R` and `TracerPid == 0`; a
  later game-only frame shows live Training gameplay. This validates the
  hardened controller on a prior safe path, not at `0x0044D79A`
  (`EXP-20260812-030`).
- Fresh adjacent-only `RUN-GDB-20260812-221224` stops once before instruction
  `0x0044D794` with `AL == 0x40`, `RCX == 0`, caller dword `0x00000680`, and
  plant slot `0x006C342B`, then records structured `SIGSEGV` at the same PC.
  The result is rejected, its point is deleted, detach succeeds, five samples
  are state `R` with `TracerPid == 0`, and a later game-only frame shows live
  Training under `nopass`. This widens KU-031 beyond exact `0x0044D79A`; it
  does not prove the load or downstream chain completed (`EXP-20260812-031`).
- `RUN-WINE-20260812-223223`, `RUN-WINE-20260812-223921`, and
  `RUN-WINE-20260812-224252` are fresh control/replacement/control Direct3D
  arms for the exact plant-04-to-10 pair. All three normalized logs are
  byte-identical, reach `NextLife`, and complete the same timestamped
  trajectory. The controls match at 11/12 same-index 640x480 game-surface
  frames; the replacement yields no stable local difference across direct,
  temporal-median, and three-sample intersection comparisons
  (`EXP-20260812-032`).
- `RUN-WINE-20260812-230859`, `RUN-WINE-20260812-231216`, and
  `RUN-WINE-20260812-231403` are fresh control/one-path replacement/control
  Direct3D arms for exact `CHARS/FLICK.ALL <- CHARS3/FLICKD.ALL`. All three
  normalized logs are byte-identical, explicitly load `FLICK.ANM/.ALL`, reach
  `NextLife`, and complete the fixed trajectory. Intersecting all 18
  replacement-to-control frame pairings at each anchor leaves only the moving
  central figure: 689, 466, 89, and 532 pixels at a 5% grayscale threshold
  (`EXP-20260812-033`).
- For the exact unchanged selected file, retained entries 0-23 receive word
  `+0x2E == 1` from the bounded descriptor values and store `0x00448117`.
  When `0x0044C440`'s outer conditions pass, the test at
  `0x0044C661-0x0044C666` therefore routes a symbolic current retained entry
  through `0x0044C898 -> 0x0044F8E0` (`EXP-20260813-036`).
- `0x0044F8EA` reads the current entry's `+0x20` pointer and thereafter forms
  only stream-relative addresses. `0x0045A7F0` instead forms table base
  `T + 4`, positive command pointer `T + 4 + count * 12`, and table reads from
  command-item offsets. Neither function contains a direct source-pointer
  copy or call edge to the other (`EXP-20260813-036`).
- On their conditional output branches, both functions allocate
  `*(0x0081BC28) + *(0x008082C8) * 0x80`, increment `0x008082C8`, write the
  previous list pointer at output `+0x70`, write a mode/flag word at output
  `+0x74`, and link through the head topology reached via `0x004E8CC8`.
  Exact same-head membership still depends on separately derived offsets and
  depths (`EXP-20260813-036`).
- In fresh accepted Direct3D control/replacement/control arms, exact candidates
  `{0-7, 9-23}` all return from `0x0044F8E0` with
  `(0x008082C8, 0x0081C138, 0x0081BC28) = (0,0,0)`. Every exact interval has
  count/bytes zero and SHA-256(empty), so the changed-emission set in this
  arena is empty (`EXP-20260813-038`).
- `0x00420022-0x00420044` maps renderer selector 1 to native software and 2
  to Direct3D. Main/restart dispatches call `0x0049C520` for value 1 and
  `0x004119E0` for value 2. The former owns the
  `0x0081C138/0x0081BC28/0x008082C8` arena setup; the latter does not touch
  that triple (`EXP-20260813-039`).
- Under selector 2, `0x0044F8E0` calls `0x00405FE0` for masked record `0x3C`
  and `0x00407450` for `0x34`. Both build Direct3D vertex/index batches rooted
  through `0x004C4108/0x004C410C` and can flush through
  `0x004056A0/0x004058D0` to the device `DrawIndexedPrimitive` vtable slot
  (`EXP-20260813-039`).
- The two Direct3D roots resolve to `0x004F1730` and image-initialized
  `0x00511510`, each with 32 pages. `0x00405FE0` appends four `0x20`-byte
  vertices and six indices; `0x00407450` appends three and three. Exact marker
  stops `0x00405838/0x004059AB` precede all reachable counter resets
  (`EXP-20260813-040`).
- Fresh accepted hardware Direct3D control/replacement/control arms prove all
  four positive renderer markers and no `INITSOFTRENDER`. All selected
  additions occur at root `0x004C4108`, page 16, with no selected in-call
  flush. Replacement counts outside both controls select exact candidates
  `{1,2,4,5,6,7,9,10,14,15,18,19,20}` (`EXP-20260813-040`).
- Both retained cycles in all three M2.27 arms map the same 168 exact builder
  calls. All 145 changed records inside the 13 candidates reach their selected
  builder. Per-form control envelopes select 18 groups containing 124 exact
  changed records; single-record offsets `0x0174`, `0x0858`, and `0x0AA4`
  have individually discriminated bounded append outcomes
  (`EXP-20260813-041`).
- Exact selected vertex-count writes are `0x004069A1` (+4) and `0x00407B00`
  (+3); all mapped earlier exits are no-append paths. Fresh schema-5 arms
  retain exact per-record outcomes for all 124 candidates. Only entry 7/file
  offset `0x0A6C`/form `0x3C` is replacement-local outside both controls,
  with append pattern `0/1/0` (`EXP-20260813-042`).
- Exact record `0x0A6C` differs only at record-relative
  `+0x00..+0x02`, `+0x24..+0x26`, `+0x28..+0x2A`, and
  `+0x2C..+0x2E`. All four spans reach separate byte-derived dwords at
  vertex-record `+0x10` after `0x004069A1`; none distinguishes a mapped
  admission predicate (`EXP-20260813-043`).
- Exact record `0x0A6C`'s admission path has a 23-location physical
  non-source input union, with at most 22 values active on one path. For its
  source-derived mode 2, native disassembly reduces no-append admission to 12
  ordered logical slots and 13 concrete reject PCs. The existing safe pre-
  call selector data watch and entry-post/count closure can support a first-
  reject receipt without retaining raw values or adding an execution point
  (`EXP-20260813-044`).
- Harness 1.5.0/schema 6 implements only that exact evaluator and receipt.
  Synthetic fixtures cover every concrete reject PC, both depth branches and
  skip, signed arithmetic/failure paths, digest drift, count mismatch, exact
  closure, complete-plan/envelope drift, and raw-output exclusion. The
  validator locks the existing three data watches and accepted 168-call plan
  at SHA-256
  `5eb280a7bd54b56a9654fed7984e9677a15618c5376be703a85718ea3bb2ffec`.
  `EXP-20260813-045` confirms this implementation and fixture boundary
  offline.
- `EXP-20260813-046` live-validates the exact schema-6 envelope in three
  accepted post-`NextLife` hardware Direct3D arms. Prediction matches observed
  append count in all three. Control A and the replacement reject at
  `0x004065B0` after seven slots; control B passes all 12 slots and appends,
  producing fresh pattern `0/0/1`. The unchanged controls disagree and the
  replacement does not uniquely pass, so M2.29's retained `0/1/0` is exact
  for its arms but not source-stable across launches. No raw values or payload
  are retained, and no source/visible attribution is promoted.
- Harness 1.6.0 preserves schema 6 and the legacy one-cycle exact envelope,
  while accepting exactly three captured cycles after one warmup for M2.33.
  Three is the smallest recurrence-capable sequence. The accepted M2.32 exact
  runs establish 200 stops per complete cycle, so four total cycles project
  to 800 of the unchanged 1,000-stop ceiling. Stable reject/pass, reject/pass/
  reject, digest drift, unclosed/incomplete cycles, exact-bound drift, and
  multi-cycle output exclusion pass offline fixtures. Only complete existing
  payload-free receipts are emitted (`EXP-20260813-047`).
- Freshly authorized `EXP-20260813-048` live-validates that fixed three-cycle
  envelope in one unchanged post-`NextLife` Direct3D process. The arm accepts
  at 816 stops with four rollovers and ordered reject/pass/reject (`0/1/0`).
  Cycles 0 and 2 reject at `0x004065B0` after seven slots; cycle 1 passes all
  12 and appends. Every prediction matches the native count outcome, while
  all three active-state digests differ. Only the existing three data watches
  are installed/deleted; cleanup/detach, no-signal, and five resumed/untraced
  samples pass. Stop rows and receipts retain no raw values or payload, and
  the raw GDB console stream is not curated.
- `EXP-20260813-049` confirms that three written M2 gates are already
  supported at narrow, non-transferable boundaries. The `.ANM` format evidence
  does not validate `.ALL`; the exact `.ALL` replacement instructions contain
  no game bytes. The sole remaining M2 gate is the missing M1 record/positive-
  target-to-ID-zero-resource selection edge preserved by `KU-023`.
- `EXP-20260813-050` classifies every exact M1 `0x0045A7F0` selector-2
  builder-facing input and finds no ID-zero header/range or selected-resource
  provenance. The negative closes only this function surface; it does not
  establish whole-program or lifetime independence.
- `EXP-20260813-051` classifies all eight retained generic header readers.
  Six occur only before the M1 coordinator, one initialization call uses exact
  index 11, and the sole coordinator-local reader precedes the record root and
  walk. This closes the declared current-invocation census, not persistent or
  copied cross-frame state.

Runtime claims above are scoped to `EXP-20260811-004`, `EXP-20260812-005`,
`EXP-20260812-006`, `EXP-20260812-007`, `EXP-20260812-008`,
`EXP-20260812-010`, `EXP-20260812-011`, `EXP-20260812-012`, or
`EXP-20260812-013` through `EXP-20260812-016`, or `EXP-20260812-018` through
`EXP-20260812-033` as cited.
M2.4 `EXP-20260812-017`, M2.21 `EXP-20260812-034`, M2.22
`EXP-20260813-035`, M2.23 `EXP-20260813-036`, M2.24
`EXP-20260813-037`, and M2.26 `EXP-20260813-039` are static/offline only;
M2.25 `EXP-20260813-038` and M2.27 `EXP-20260813-040` are accepted
metadata-only Direct3D runtimes; M2.28 `EXP-20260813-041` is an offline
reanalysis of exact files and retained M2.27 metadata;
M2.29 `EXP-20260813-042` combines an offline append/return proof with fresh
accepted metadata-only Direct3D arms;
M2.30 `EXP-20260813-043` is an offline exact file comparison and native
caller/builder data-flow proof;
M2.31 `EXP-20260813-044` is an offline exact admission-state backward slice
and metadata-only receipt design;
M2.32 `EXP-20260813-045` supplies the offline evaluator/schema gate and
`EXP-20260813-046` supplies the accepted metadata-only live matched phase;
M2.33 `EXP-20260813-047` supplies the offline fixed-three-cycle design and
`EXP-20260813-048` supplies the accepted one-process live recurrence;
M2.34 `EXP-20260813-049` is an offline evidence/repository audit only;
M2.35 `EXP-20260813-050` is an offline selector-2 input-provenance trace only;
M2.36 `EXP-20260813-051` is an offline generic-index producer/caller census;
M2.37 `EXP-20260813-052` is an offline gate disposition and bounded native
signed-selector candidate selection;
M2.38 `EXP-20260813-053` is an offline exact-selector writer census, image-
table value test, and M1-route intersection;
M2.39 `EXP-20260813-054` is a superseded offline roadmap/evidence scope
disposition; `EXP-20260813-055` is its read-only hard-truth audit and selects
offline M2.40; `EXP-20260813-056` completes that offline producer census;
`EXP-20260813-057` rejects the second premature deferral and selects exact
offline M2.41; `EXP-20260813-058` completes M2.41 and selects independent
fresh-context disposition audit M2.42; `EXP-20260813-059` completes M2.42
with `ACCEPT`, defers M2 without closing its causal gate, and activates exact
M4.1; `EXP-20260814-060` completes the M4.1 worker implementation;
independent `EXP-20260814-061` rejects its complete-output-preflight claim and
activates exact corrective packet M4.3; `EXP-20260814-062` completes that
worker correction and activates independent verifier packet M4.4;
`EXP-20260814-063` accepts M4.3 and activates exact M4.5;
`EXP-20260814-064` completes the M4.5 worker and activates exact independent
verifier packet M4.6; `EXP-20260814-065` rejects M4.5 acceptance and activates
exact corrective packet M4.7; `EXP-20260814-066` completes that worker
correction and activates independent verifier packet M4.8;
`EXP-20260814-067` accepts that correction and activates exact sparse-overlay
removal packet M4.9; `EXP-20260814-068` completes that worker implementation
and activates independent verifier packet M4.10; `EXP-20260814-069` rejects
M4.9 acceptance and activates exact corrective packet M4.11;
`EXP-20260814-070` completes that worker correction and activates exact
independent verifier packet M4.12; `EXP-20260814-071` rejects M4.11 acceptance
and activates exact corrective packet M4.13; `EXP-20260814-072` completes that
worker correction and activates exact independent verifier packet M4.14;
`EXP-20260814-073` rejects M4.13 acceptance and activates exact corrective
packet M4.15; `EXP-20260814-074` completes that worker correction and
activates exact independent verifier packet M4.16; `EXP-20260814-075` rejects
M4.15 acceptance and activates exact corrective packet M4.17;
`EXP-20260814-076` completes that worker correction and activates exact
independent verifier packet M4.18; `EXP-20260814-077` accepts the exact current-
Linux correction and activates only versioned-compatibility packet M4.19;
`EXP-20260814-078` completes that statement/checker worker and activates exact
independent verifier packet M4.20; `EXP-20260814-079` rejects its ambiguous
authority alignment and activates exact corrective packet M4.21;
`EXP-20260814-080` completes that correction and activates exact independent
verifier packet M4.22; `EXP-20260814-081` rejects incomplete effective-
authority extraction and activates exact same-read byte-pin correction M4.23;
`EXP-20260814-082` completes that correction and activates independent M4.24;
`EXP-20260814-083` accepts the exact five-pin boundary and activates only the
written deterministic single-manifest dry-run/report capability M4.25;
`EXP-20260814-084` completes that worker and activates independent M4.26;
`EXP-20260814-085` accepts that exact report boundary and activates only the
bounded milestone-closure evidence audit M4.27; `EXP-20260814-086` rejects
closure after its 14-row ledger exposes receipt insufficiency and an unjoined
clean-copy lifecycle, then activates only strict receipt reconstruction M4.28;
`EXP-20260814-087` completes that worker boundary and activates exact
independent verifier M4.29; `EXP-20260814-088` rejects its parent-component
consistency boundary and activates only exact corrective M4.30;
`EXP-20260814-089` completes that worker and activates only exact verifier
M4.31; `EXP-20260814-090` rejects descriptor cleanup and activates only exact
corrective M4.32; `EXP-20260814-091` completes that worker and activates only
exact verifier M4.33; `EXP-20260814-092` accepts that closure and activates
audit-only M4.34; `EXP-20260814-093` rejects the unjoined clean-copy lifecycle
and activates exact restoration M4.35; `EXP-20260814-094` completes that
worker and activates verifier M4.36; `EXP-20260814-095` rejects case-colliding
complete-tree admission and activates exact correction M4.37;
`EXP-20260814-096` completes that worker and activates verifier M4.38;
`EXP-20260814-097` accepts it, resolves only `KU-052` at the demonstrated
current-Linux lifecycle, and activates only v0.2 statement alignment M4.39;
M2.21 reuses the retained accepted M2.20 log as an independent request check,
while M2.22-24 use the M2.20 and M1 dynamic results only as independent
anchors for their static lineages and localization.

## What are the leading hypotheses?

- The `PC\BUGS` tree is compatible with the retail installed layout.
- A real CD block-device mapping would cause `0x004ADC30` to use the CD-root branch.
- Current audio warnings are Wine compatibility candidates after successful game initialization.
- A user-supplied external PC video still reportedly using hardware mode has a
  smoother green foreground stem than the native Wine capture. WineD3D legacy
  texture/dither translation is one candidate, but native driver behavior and
  capture/resampling remain uncontrolled; no Linux-specific defect is
  confirmed (`KU-012`).
- Positive targets provide reusable visible render content for the bounded
  dispatch-`0x49` path. `EXP-20260812-010` raises
  `HYP-20260812-001` to high-confidence supported status; whether a target is a
  complete object definition remains unknown.
- The record-center and positive-bound roles likely generalize across the 990
  statically valid same-dispatch records. Level 01 supplies second-file
  acceptance but not a visible placement at its start camera; later record-261
  selection remains unknown (`EXP-20260812-013`, `KU-018`).
- The coordinated `.ANM`/`.ALL` requests are related resource inputs, but their
  complete layouts and semantic relationship remain unconfirmed. The traced
  plant ID producer is a separate DAT top table, so the stronger M1 placement-
  record/payload-to-resource identity remains open (`EXP-20260812-016`,
  `KU-023`).
- Plant 04 and 10 `.ANM` files have equal size/first-level layout, and their
  `.ALL` files are both `0xE08` bytes. Both the `.ANM`-only and whole-pair
  substitutions are accepted without a stable start-camera change. The fixed
  M2.19 trajectory likewise produces no stable replacement-local region, so
  this direct plant route is retired (`EXP-20260812-018`,
  `EXP-20260812-019`, `EXP-20260812-032`).
- Training explicitly loads `CHARS/FLICK.ANM/.ALL`. Exact one-path replacement
  with equal-size `CHARS3/FLICKD.ALL` is accepted and produces a repeated local
  difference on the input-controlled central figure along all four bounded
  anchors. This supports a causal file-to-render contribution; filename
  identity and `.ALL` layout remain unassigned. The exact request/first-
  consumer chain now ends in retained ID-zero range
  `[0x005A9660, 0x005A9DE0)`. M2.22 rules out a direct M1 bridge within one
  normal branch/order window. M2.23 proves that the exposed entry handoff and
  positive-target path use distinct source walks but one exact conditional
  `0x80`-stride arena/list topology. M2.24 localizes all retained-file
  differences to exact candidate set `{0-7, 9-23}` and proves that every one
  lies in a record span reached by both bounded walks. M2.25 then finds that
  none emits into that arena in the tested Direct3D window because the arena
  remains inactive. M2.26 resolves that arena as selector-1 software output
  and identifies selector-2 Direct3D batching as the active alternate path.
  M2.27 narrows the changed-count provenance to exact 13-entry set
  `{1,2,4,5,6,7,9,10,14,15,18,19,20}`. M2.28 then narrows the
  count-relevant surface to 18 entry/form groups and 124 exact changed
  records. M2.29 then reduces fresh replacement-local append behavior to
  exact entry 7/offset `0x0A6C`/form `0x3C`; its non-reproduction of M2.28's
  three earlier single-record outcomes preserves their per-frame scope.
  M2.30 maps all 12 exact source differences to four post-admission append
  inputs and proves that none distinguishes admission. M2.31 reduces the
  non-source union and exact ordered admission chain and proves the existing
  safe data-watch boundaries can support a payload-free first-reject receipt.
  M2.32's evaluator agrees with native outcomes, but its fresh `0/0/1` pattern
  rejects source-stable attribution across processes. M2.33 then accepts one
  unchanged process with reject/pass/reject (`0/1/0`), proving bounded
  within-process variation and recurrence without establishing a period,
  distribution, source/visible causality, or state semantics
  (`EXP-20260812-033`, `EXP-20260812-034`, `EXP-20260813-035` through
  `EXP-20260813-052`, `KU-023`, `KU-032` through `KU-045`). The M2.34 gate
  audit accepts the narrow `.ANM` and distribution evidence, while M2.35
  rules out a hidden ID-zero selector in the exact M1 Direct3D renderer input
  slice and M2.36 rules it out across the finite generic-reader set for the
  declared current-invocation route. The missing M1-to-ID-zero resource-
  selection edge remains the sole milestone blocker. M2.37 retains that
  causal gate: merging the separately visible M1 and ID-zero paths would
  weaken the outcome. M2.38 then retires the finite `0x0044CA00` candidate:
  four native writer paths only clear to zero, while sole nonzero writer
  `0x00467E60` draws from 20 positive image values and runs from separate
  fixed-pool state before M1 coordinator entry. Signed `-103` and an M1
  producer are both negative at the declared boundary. No new family is
  selected by that result. M2.39 preserved the causal gate but prematurely
  deferred M2 and activated exact-hash M4.1. `EXP-20260813-055` supersedes
  that priority conclusion: the already cited first dwords
  `0x0059B730/0x0059B7B4` are a finite unresolved producer surface in fixed-
  pool slots 2 and 3. M2 returns active on their offline producer census;
  M4.1 remains planned without promoting `.ALL` semantics or compatibility.
  `EXP-20260813-056` then completes that census: a conditional reader-time
  zero exists through `0x0041BBBA`, but its lineage is separate `LEVEL.RAW`
  plus fixed-pool state and has no M1 record/payload/positive-target edge.
  M2 returns to deferred and M4.1 becomes active without weakening either
  evidence boundary. `EXP-20260813-057` then rejects that priority conclusion:
  explicitly retained slot 63 remained excluded, and exact arithmetic places
  supposedly separate `0x0059C30C` at slot 25. Both have finite fixed-pointer
  generic-header reads, so M2 returns active on M2.41 while M4.1 remains
  planned. `EXP-20260813-058` closes both residual reader paths: zero is
  statically reachable at the declared state-gated reads, but neither value nor
  direct gate is M1-derived. Because two prior worker dispositions omitted
  finite candidates, M2 remains active on independent hard-truth audit M2.42
  rather than accepting another worker-authored deferral. Independent
  `EXP-20260813-059` now reproduces those exact conclusions and separately
  finds no finite successor retained in the cited surface. Possibilities such
  as persistent/copied state, indirect aliases, and unreviewed families remain
  honest limitations, not exact already-retained candidates. M2 is therefore
  deferred with its causal gate unchanged, and exact M4.1 became active.
  `EXP-20260814-060` then produced the worker implementation, while independent
  `EXP-20260814-061` rejected its complete-output-plan claim and activated
  corrective M4.3 without weakening the exact replacement evidence.
  `EXP-20260814-062` closes all four deterministic topology reproductions at
  the worker boundary, and independent `EXP-20260814-063` accepts the result
  after 26/26 topology cases, 47/47 focused tests, 235/235 complete tests,
  explicit schema compatibility, and two exact local applications.
  `EXP-20260814-064` adds only the exact two-input composition boundary: 12/2/
  4-byte M1 and whole-destination claims, deterministic reversed output,
  existing-schema apply/stage, and asset-free conflict JSON. Independent
  `EXP-20260814-065` preserves those single-edit/conflict results but rejects
  the general done claim: canonical span sorting can reverse a valid
  intra-input sequence. `EXP-20260814-066` now preserves that existing
  sequence under deterministic exactly-two-input composition at the worker
  boundary, without changing claims, schemas, receipts, or revalidation.
  Independent `EXP-20260814-067` accepts that result after the exact pair,
  both canonical rank orientations, more-than-two-edit and collision cases,
  28/28 topology, 6/6 schema, tracked local, opaque-recipe, and asset-free
  gates pass. A cross-input guard dependency still fails closed in both
  argument orders, so no semantic ordering solver is implied.
  `EXP-20260814-068` then adds only dedicated sparse-overlay removal. It
  recomputes the unchanged ordinary receipt from the supplied manifest/source,
  requires byte-exact receipt and output-hash equality plus an exact single-
  link regular-file tree, and deletes only recorded outputs/receipt and empty
  parents. The 95 focused and 283 complete tests pass before documentation,
  and three exact local manifest families pass apply/remove twice with source
  hashes unchanged.
  Independent `EXP-20260814-069` preserves all ordinary success/refusal and
  local-recipe checks but rejects the complete-preflight claim: a pre-existing
  bind-mounted intermediate directory passes current `lstat`/tree validation,
  then removal deletes through the mount and partially prunes the overlay
  before `rmdir` fails `EBUSY`. This remains neither staged-tree removal nor a
  general transaction/rollback request. `EXP-20260814-070` now adds only the
  fail-closed M4.11 mounted-plan-path preflight correction. It recognizes the
  exact overlay root and descendant planned mountpoints from Linux mountinfo
  before overlay traversal. Independent `EXP-20260814-071` preserves that
  boundary but rejects the stronger claim because the check omits a proper
  parent traversed to reach the overlay root. M4.13 adds only that ancestry
  discriminator while retaining ordinary removal usability and every accepted
  baseline. `EXP-20260814-072` now closes the exact reproduction at the worker
  boundary through mount ID/device/root/path alias classification. All five
  namespace cases, 101/289 tests, and six local cycles pass; normal filesystem
  mounts are positive controls. Fresh-context `EXP-20260814-073` preserves
  those controls except for one stable stacked layout: a hidden lower alias
  covered by an ordinary top filesystem still classifies their shared path as
  an alias, so valid ordinary overlay removal refuses unchanged. Exact M4.15 is
  limited to ignoring covered lower records while retaining all prior refusals
  and positive controls. `EXP-20260814-074` now closes that exact worker
  reproduction: same-mountpoint parent stacking filters hidden lower candidate
  and source records, the visible top overlay removes completely, the hidden
  target/source remain exact, and the five retained mounted cases still refuse.
  Six namespace cases, 102/290 tests, and six local cycles pass. Independent
  `EXP-20260814-075` preserves that evidence but rejects M4.16 after a newer
  uncovered bind reuses freed numeric mount ID 1081 below its still-mounted
  ID-1082 source. The numeric age comparison misses the alias; removal returns
  success and changes the independent target. `EXP-20260814-076` replaces only
  that age comparison with verified explicit kernel later-mount order. The
  reused-lower-ID alias refuses with all four snapshots exact, covered-stack
  removal and all six other namespace families remain correct, 105/293 tests
  pass, and six local cycles retain exact hashes. Independent
  `EXP-20260814-077` accepts that boundary after a separate namespace
  reproduction, ABI/kernel audit, adversarial fault injection, and every
  retained baseline. `EXP-20260814-078` completes the exact versioned
  statement/checker worker with five evidence anchors, current-Linux removal
  scope, tested Wine/Gamescope fields, 18 drift tests, and 311 canonical tests.
  Independent `EXP-20260814-079` retains those boundaries but rejects
  substring-only authority alignment after effective launcher/filter and
  receipt overrides plus a contradictory Environment row pass.
  `EXP-20260814-080` confines M4.21 to source-aware authority extraction and
  synthetic regressions. `EXP-20260814-081` rejects M4.22 because effective
  Bash/Python mutation and duplicate manifest keys remain accepted;
  `EXP-20260814-082` supplies exact same-read pins for the five machine
  authorities, and `EXP-20260814-083` independently accepts that bounded
  correction. `EXP-20260814-084` confines M4.25 to deterministic write-free
  reporting for one existing manifest, and `EXP-20260814-085` independently
  accepts that exact boundary. `EXP-20260814-086` completes the M4.27 ledger
  and rejects closure: current receipt bytes authenticate manifest/source-
  recomputed removal but were not an accepted reproduction/removal authority,
  while the clean-copy lifecycle gate also remains open. `EXP-20260814-087`
  completes only the M4.28 worker correction with strict external receipt
  replay/removal. `EXP-20260814-088` rejects acceptance because a checked
  parent can change into a directory link before final receipt acquisition and
  still reach the same accepted inode. `EXP-20260814-089` completes only exact
  M4.30: root, every lexical parent, and the final receipt are acquired through
  retained relative descriptors, compared across inspection/open/read, and
  reacquired as one identical no-link chain before parsing. The exact bypass
  and adjacent component/final-file changes now reject; 154/216/404 tests and
  all six local cycles pass. Independent `EXP-20260814-090` retains the exact
  parent and adjacent refusals, mappings, 154/216/404 tests, six local cycles,
  five pins, and nine reads, but rejects the claim that every descriptor closes
  on failure: first/second close-error injections retain seven/six descriptors.
  `EXP-20260814-091` now completes only exception-safe exhaustive release:
  indexed cleanup attempts are unique and complete, descriptor deltas are zero,
  primary errors survive, and 161/223/411 tests plus six local cycles pass.
  Exact M4.33 independently accepts it in `EXP-20260814-092` after 28/28 fresh
  indexed cases, 161/223/411 tests, and all six local cycles. `KU-051` is
  resolved. `EXP-20260814-093` then rejects M4 closure after no one same
  current output spans full-tree launch readiness and supported removal;
  exact M4.35 implements bounded complete-tree restoration at the worker
  boundary in `EXP-20260814-094`; `EXP-20260814-095` rejects its exact-spelling
  tree admission because Windows-case-equivalent paths coexist and restore;
  `EXP-20260814-096` supplies the bounded M4.37 worker correction.
  `EXP-20260814-097` independently accepts the correction and resolves
  `KU-052` only for the exact manifest-driven current-Linux lifecycle. M4
  remained active on M4.39 because v0.1 still declared restoration unsupported;
  M4.39 supplies strict v0.2, exact M4.40 rejects checker strictness, M4.41
  closes its regular-file cases, and exact M4.42 rejects resolved-path identity.
  M4.43 closes that worker boundary, and exact M4.44 independently accepts it
  in `EXP-20260814-103`. M4 is Complete without reopening or broadening either
  resolved unknown.
- The `0x2B` selector table is occurrence-cursor based, not independently
  keyed by DAT offset. The second Training occurrence at `0x3A4` is necessary
  for plant 10 requests in the unchanged sequence: its one-byte suppression
  removes exactly the plant 10 pair lines while retaining plant 04 and
  `NextLife`. The absence of a stable visual mask leaves the direct M1
  placement identity unresolved (`EXP-20260812-020`, `KU-023`, `KU-026`).
- The simplest direct-pointer dependency from records 124–126 to the measured
  plant 10 ANM slot or entry `+0x20` dwords is disfavored by the three bounded
  runtime windows. The exact source dwords also remain unread throughout the
  71.708-second post-title window and the corrected late-initialization
  windows. Both entries' first three head dwords also remain unread in matched
  guarded windows, both nonzero `+0x0C` dwords remain unread through a
  retained no-input title, and both `+0x2E` and `+0x28` words remain unread
  through the same bounds. This exhausts the exact fields populated by
  `0x00448010` and its guarded caller only for the measured intervals. The
  M2.15 adds a title-to-`NextLife` and elapsed post-title negative and finds
  exact reader `0x0044CE3E` inactive in a separate no-input control. M2.16's
  fresh simultaneous outer-gate/callee/data arm reproduces the same-address
  debugger fault and fails its live survival receipt. M2.17 repairs the false
  structured status and independently validates a safe live control. M2.18's
  adjacent-only arm then signals at `0x0044D794`, so the tested continuation
  limitation is broader than exact `0x0044D79A`. M2.19 then exhausts the
  accepted plant-pair route with its fixed matched trajectory and a bounded
  negative. M2.20 then produces a positive one-path character-family render
  link without resuming debugger work. M2.21 then binds that selected path's
  PC request and first consumer/runtime destination without a new runtime or
  general layout work. M2.22 then identifies the first direct ID-zero use and
  rules out the direct M1 bridge in one normal update while preserving a
  downstream entry-pointer discriminator. M2.23 then resolves that exact
  render-lineage comparison at the shared conditional-output boundary while
  keeping the sources separate. M2.24 exhausts the accepted two-file offline
  localization; M2.25 records an all-candidate inactive-arena negative; M2.26
  reconciles that arena to the software branch and exposes the Direct3D batch
  route; M2.27 reduces per-entry Direct3D count provenance to 13 exact
  candidates; M2.28 completes offline changed-record form localization;
  M2.29 selects exact fresh append outcome `0x0A6C`; M2.30 proves its source
  differences are post-admission append inputs; M2.31 completes the offline
  non-source admission-state localization and receipt design; M2.32 then live-
  validates exact evaluator/count agreement while preserving fresh `0/0/1`
  temporal ambiguity; and M2.33 fixture-proves and live-validates the fixed
  three-cycle stability envelope (`EXP-20260812-021` through
  `EXP-20260813-048`,
  `KU-023`, `KU-027`, `KU-031` through `KU-045`).

## What is blocked?

- Period-correct 86Box/Windows 98 execution depends on user-owned Windows 98 SE media and legitimate firmware requirements recorded in [[86Box Reference Machine]].
- The modern Windows debugging VM depends on Windows media/license.
- Full Wine system-call capture is limited because host `strace` is not installed.
- No cross-port comparison should begin without a bounded PC-native question satisfying [[Project Charter]].
- M2 cannot close while `KU-023` lacks an exact PC data-flow edge from an M1
  scene record or positive target to the selected ID-zero resource path.
  `EXP-20260813-052` rejects a wording-only closure, and
  `EXP-20260813-053` now retires its sole finite signed-selector candidate:
  the exact native producer table contains no `-103`, and its normal-update
  lineage precedes and remains separate from the M1 record walk. Shared
  software/Direct3D output topology, overlapping rendered outcomes,
  persistent-state possibility, and an addressable selector do not establish
  the missing selection. `EXP-20260813-055` correctly exposed fixed-pool
  slots 2 and 3 as an unresolved finite surface; `EXP-20260813-056` completes
  that census and finds a conditional reader-time zero derived from separate
  `LEVEL.RAW` plus fixed-pool state, not M1. M2 remains incomplete but is
  not deferred after `EXP-20260813-057` exposes exact residual slots 25 and 63
  in the same bounded pool/reader family. `EXP-20260813-058` completes their
  fixed-pointer consumer disposition with another M1 negative.
  `EXP-20260813-059` independently accepts that result and finds no exact
  finite successor retained in the cited evidence. M2 remains incomplete and
  is now deferred; the exact revisit conditions are a cited finite PC-native
  candidate, a concrete-goal bounded discriminator, or contradictory evidence.
- The GDB harness now supports bounded paired/coherent-zero submission capture
  under schema 3, purpose-specific Direct3D batch capture under schema 4, and
  exact-plan payload-free per-record outcomes under schema 5. Schema 6 adds
  one fixture- and live-validated exact-`0x0A6C` evaluator plus a live-
  validated fixed three-cycle bound, not a general predicate or repeated-
  cycle API.
  The harness still cannot stage a general new arm after a guard or evaluate
  general stop predicates/register-relative expressions.
  The broader feature/workaround record is [[Reverse Engineering Capability Gaps]].
- Hardware execution-breakpoint continuation at both adjacent `0x0044D794`
  and exact `0x0044D79A` has produced a same-PC `SIGSEGV` in independent fresh
  runs. Schema 2 rejects and safely detaches the tested adjacent arm, but root
  cause remains unexplained. Do not use this caller-gate region as an M2
  consumer-evidence path without a separately demonstrated workaround.
- Hardware execution-breakpoint continuation at `0x0044C898` also produces
  structured same-PC `SIGSEGV` in fresh `RUN-GDB-20260813-101022`. Accepted
  M2.25 evidence uses a data watch at the post-call header load instead. Do
  not reuse this execution point without a separately proven workaround.

## Historical next-agent directive — 2026-08-17

Historical M5 handoff retained for provenance. It is superseded as a work queue
by [[Current State#Current task handoff]]; do not treat the instructions below
as a current selection.

[[EXP-20260816-171 - Independent M5.8 grain-gate resolver audits]] records
final **ACCEPT** for exact correction commit
`dfd3af31c845939aa972babfd0f44a60e54b6487`, tree
`8b7d4234e3a517ed63032bd2d9c9ab8770801714`, after one bounded strict-JSON
rejection. M5.7/M5.8 are complete at the optional offline twelve-mechanism
boundary. Do not reopen the accepted model by momentum or promote runtime
replacement, downstream execution, global family exclusivity, City-byte
semantics, or missing row-1/row-4 original receipts.

The researcher's next coverage preference remains **Enemies, actors and AI →
Input → Event/scripting system**. The next agent should start with a bounded
PC-native Actors/AI reconnaissance question selected from
[[Subsystem Coverage Map]], name executable/data locators and a discriminating
result before work, and use fresh James for the hard-truth audit. This
preference does not itself admit a third M5 module; any implementation
candidate must independently pass all six M5 entry criteria.

The accepted audit remained offline and path-bounded: no game/Wine/Gamescope/
debugger, target write, `originals/`, external PS1 evidence, threshold-builder
change, semantic name for `0x00599C69`, other trigger family, or M2/M3/M4/M6
reopening. The accepted implementation boundary is twelve confirmed
mechanisms and EXP-146 direct/static evidence, not global grain-family
exclusivity.

`KU-065` is **resolved for its identified node** as of 2026-08-17: the cause
was a fixed `time.sleep(0.12)` in three `tests/test_input_movie.py` sites
racing the tool's log-baseline snapshot, now replaced by waiting on the tool's
own `--status-fd` `armed` transition. Measured before/after on the isolated
node: idle 59/60 → 60/60, and under 12-worker load 0/20 → 20/20.
`scripts/input-movie.py` was audited and left unchanged. The identity of the
four original camera-packet failures remains open and is bounded in the
register. Suite denominators no longer need the KU-065 qualification for this
node; previously qualified results stay as recorded.
[[EXP-20260816-163 - KU-065 canonical-suite reproduction follow-up]] observed
13/13 canonical full suites, 100/100 whole
manifest runs, and 200/200 focused system-state runs pass with direct raw
logs, but did not reproduce the original `1 failed, 647 passed` signature.
The descriptor-count failure seen in a separately constrained nine-failure
sandbox run is only a candidate. Do not quote the suite as an unqualified
clean gate; state the exact passing denominator and KU-065 qualification.

EXP-167 later observed a new unredirected exact-signature recurrence:
`1 failed, 647 passed` at
`tests/test_input_movie.py::test_log_anchor_uses_only_new_log_bytes`, where a
mismatched replay returned `3`/`anchor_timeout` for `NextLife.` instead of
expected return 1. The isolated node passed, and the auditor retained no raw
log or hash. This names one intermittent node but does not identify the four
earlier lost failures or close KU-065. M5.6.1's directly retained validation
then passed that node 1/1 and one canonical 648/648; both observations remain
qualified by KU-065.

EXP-170 now reproduces and durably identifies that same exact node on the
M5.7 final subject: one canonical run is `1 failed, 681 passed`, and 20
isolated direct-log runs are 15 pass / 5 fail. Four failures time out before
recording reaches its anchor; one times out at the first replay `NextLife.`
anchor. A canonical retry is 682/682. This makes a preceding runtime session
unnecessary for the next discriminator: instrument the synthetic test's
process/log/poll/120-ms-append timing and retain passing plus both failure
phases. The underlying cause and identity of the four original camera-packet
failures remain Unknown; KU-065 stays open.

Final closure audit found 32 pre-existing baseline-prefix `winedevice.exe`
processes, PIDs `68248`-`344284`, parented by user systemd PID `1927`; sampled
working directories name earlier `work/copies/` experiments. No game,
Gamescope, `wineserver`, pytest, or debugger target was active. These PIDs
predate EXP-163 and were not recorded as owned at launch, so they were not
terminated by broad name. Establish exact ownership before any later runtime
launch; the passing EXP-163 runs therefore include this residual device-helper
background rather than a process-empty Wine state.

M5 remains Active with two admitted modules. The first module's M5.1-M5.5.1
chain is closed by EXP-158; EXP-169 closes the second module's entry ratchet;
EXP-170 is its corrected worker implementation and EXP-171 is exact acceptance.
No third packet is admitted. Do not extend either module or promote
`checkpoint`/`respawn` semantics for type 1.

After the completed M5.7/M5.8 implementation/audit sequence, retain the
researcher's non-binding coverage preference as **Enemies, actors and AI →
Input → Event/scripting system**. This queue records intent without widening
M5.8; each future subsystem still needs its own bounded PC-native packet and
cannot earn claims through inference alone.

Preserve completed M3/M4/M6 and the exact EXP-135 acceptance boundary; M2
stays deferred with `KU-023` open. Do not repeat the Level03 grain-gate pit,
widen `FLIKFLIK`, or generalize the two write-assisted EXP-134 pickups into
controller reachability or generic gameplay tooling. CAP-002 remains partial
and separate. Before and after any future runtime work, follow
[[Agent Operating Manual#Runtime instance lifecycle]] and leave no obsolete
agent, game, Wine, Gamescope, or private-sink instance.

## Packet chronology

Dated packet narratives live in [[Current State Archive]]; per-session detail
lives in [[Session Index]]. Keep this note to the present snapshot so the
mandated startup reading set stays inside a working session.

## 2026-08-19 R2c face-8 localizer result

[[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
completed its derived-build `C1/L/C2` block with clean lifecycle and provenance
gates. James accepted the procedure and the fail-closed comparison. C1/C2 are
exact full-frame controls; L is internally stable but differs across 18,612
pixels and 353 components, with only 53.3957% in the largest component. The L
frame identity also exists in unmodified retail R2b evidence. Therefore the
comparison is nondiscriminating and R2c localization is unresolved: face 8 is
not confirmed visible or terrain, no no-effect claim is supported, and retail
R2 remains open.

**Superseded pickup history:** the earlier instruction required an empirically
established animation cycle before another localizer. EXP-003 D1 later proved
no exact period on its 121-frame grid, so that requirement is retired. The
historical finite-mask pickup is the consumed EXP-005 block below. Do not rerun the current
comparator or prepare the one-byte candidate.
## 2026-08-19 - R2d sampled phase calibration rejected and superseded

R2c remains procedurally accepted but causally inconclusive. [[EXP-20260819-003 - R2d Anthill sampled phase calibration]] was authorized and ran D1 only. D1 captured all 121 frames, then rejected because the lower-right structural crop contained live temporal content. D2 did not run and its old identity is obsolete.

The consumed D1 diagnostic found 121 unique RGB frames and no exact sampled period. Therefore the exact-cycle requirement is not the active design. It also found 76,807 raw variable pixels and 90,913 radius-three pixels, with three invariant crop sequences and six hashes in the excluded lower-right crop.

[[EXP-20260819-004 - R2e Anthill stable-background calibration]] was authorized and consumed by rejected `D1-SB-AH-001`. It captured all 121 frames, but its exact full-frame F0 equality gate rejected a different live-animation phase even though all three camera-control crops remained exact. D2 did not run; its old identity is obsolete; no accepted mask or intervention exists.

The EXP-004 diagnostic binds 78,593 raw changing pixels and 92,630 radius-three pixels (`30.152994791666665%`), 121 unique full-frame hashes, no exact sampled period, exact camera-control crops, and absent old-D2 paths. Its two preserved diagnostic receipts are byte-identical at SHA-256 `4d54e41a99f729f042dd75bc00c1a4ada464acab9b85ab7938deb4acfe706fef`. They remain diagnostics over a rejected arm.

[[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] was authorized and ran both controls. D1 and D2 each passed the exact auto-hardware build, all six Direct3D markers with no software marker, retail Level01 DAT, Anthill navigation/index, chronological input, 121-frame timing, three camera-crop, process, and lifecycle gates. Only the authorized read-only `(0x00861C84,4)` read occurred per arm. Distinct process identities were D1 `1072590/19909757` and D2 `1073849/19920889`.

D1's mask was 77,038 raw and 91,060 radius-three pixels (`29.641927083333336%`), but D2 produced 233 observations at 198 unique pixels outside it. The aggregate correctly rejected, quarantined both provisional controls, and published no accepted mask. The residual spans five frames and seven components in `x=268..400`, `y=269..332`; visual review aligns it with Flik's animation silhouette, not terrain or the pinned camera crops.

The durable diagnostic is SHA-256 `1640615be9df20d640dab77a740ce2221d822dba3c94354616ac3e42f857a283`. Its combined D1+D2 design-only mask has 78,838 raw and 92,480 radius-three pixels (`30.104166666666664%`), raw-byte SHA-256 `2a07565016efd050129e7d53b9f71942b2503cec8fffc7cbc592e0d619373cb6`, and PNG SHA-256 `ed8f43e54597a6d0f5d25bdd9c381319b1ed62bdededd4a0d28c4a67ff838c50`. [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] later accepted that frozen mask on one fresh finite-grid D3 holdout without expansion. Retail R2 remains open; face 8, terrain, and causality remain unconfirmed.

## 2026-08-19 update - EXP-006 D3 combined-mask holdout accepted

[[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] completed under its exact authorization on auto-hardware build `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`. Fresh D3 PID/start `1121774/20272136` passed the full renderer, Level01, provenance, grid, and lifecycle gates. Across all 121 finite-grid frames it produced zero observations and zero unique pixels outside the frozen 92,480-pixel EXP-005 combined diagnostic mask. Result JSON SHA-256 is `3fe541dfd9973ce1238f603e3fafb28834749db7530f2e27db6efb09e2bc0c19`.

This accepts the frozen mask only as a nuisance-exclusion reference for that exact derived-build/camera/grid scope. [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] remains aggregate-rejected; no cycle, exhaustive coverage, visibility, terrain, causality, no-effect, or retail-executable claim is promoted. R2 remains open.

The next action at that point was preparation of a separate offline C/L/L/C localizer protocol using the accepted mask without widening it. [[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] supplied that packet; localizer DAT creation and all runtime arms were still unauthorized at the offline boundary. The later authorized result is recorded below.

## 2026-08-19 update - EXP-007 replicated face-8 packet prepared offline

[[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] was the active offline R2 packet. Its frozen design required exact `C1 -> L1 -> L2 -> C2` order: two retail controls and two separately published, byte-identical guarded face-8 DATs created independently from retail. All four arms were to use the exact 121-frame auto-hardware grid; controls had to reproduce D1 outside the accepted mask, while L1/L2 had to reproduce each other's RGB exactly outside it and yield one bounded static localized component.

Before runtime, the offline creator, runner, comparator, and regression packet were implemented and James-accepted. L1/L2 publish as one fail-closed atomic pair; comparator evidence is retained separately for both localizers, their disagreement, and per-arm inside-mask observations. DAT-install progress is explicit, completed receipts have an exact one-file contract, accepted/pending pair ambiguity blocks launch, and corrupt accepted pairs demote to pending; even a failed demotion retains explicit pending ambiguity evidence. That pre-runtime packet passed 33 focused tests and full `make check` passed 1,418 tests with zero Vault-lint errors and zero tracked-file violations. At that point no production EXP-007 artifact or runtime arm existed; the later result is recorded immediately below.

## 2026-08-19 update - EXP-007 replicated localizer inconclusive

[[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] completed its authorized `C1 -> L1 -> L2 -> C2` sequence on four fresh processes. The independently created L1/L2 DATs are byte-identical at `9942e252...11bfd`; all four renderer, Level01, 121-frame, bounded-read, and lifecycle packets passed. Aggregate result SHA-256 `723e03ed...a309` is procedurally accepted but scientifically inconclusive: controls produced 251 outside-mask mismatches, L1/L2 disagreed at 228 pixels, intersection/static core were zero, and L2 frame 35's entire 228-pixel change was reproduced exactly by C2 frame 35.

The EXP-006 mask is therefore non-exhaustive across fresh controls. There is no face-8 visibility, terrain, causal, or no-effect claim. The authorization is consumed; the one-byte candidate remains unauthorized and R2 remains open. **Consumed successor instruction:** only an offline control-only diagnostic could propose a revised nuisance mask; EXP-008 later completed that step. The revision does not rescue EXP-007 and still requires the separately authorized EXP-009 D4 holdout before any localizer successor.

## 2026-08-19 update - EXP-008 proposed mask and EXP-009 D4 packet

[[EXP-20260819-008 - R2j Anthill control-trained successor mask]] completed the offline control-only diagnostic. It used only validated C1/C2 frames, found 251 observations at 249 unique pixels outside the EXP-006 mask, and applied `old_mask OR dilate(raw_new, radius=3)` without redilating the old mask. The proposal has 93,445 pixels (`30.418294270833335%`), decoded-mask SHA-256 `9ff27caa...1ba`, PNG `b855df0a...c936`, and diagnostic `83931a8a...9a5`. James accepted the independently reproduced offline artifact only.

[[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]] completed on fresh process `1267141/21477936/1266881`. All 121 frames produced zero observations and zero unique pixels outside the fixed mask; result SHA-256 is `bf2b4625...69d8`. James independently reproduced and accepted this one finite derived-build/view/grid holdout. The authorization is consumed and no localizer follows automatically. R2, terrain/ground identity, face-8 visibility, causality, retail confirmation, and collision remain open.

## 2026-08-20 pickup - R2l face-8 localizer executed inconclusively

[[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]] is accepted with zero observations outside the fixed 93,445-pixel control-trained mask over its 121-frame D4 holdout. That is a finite sampled-control claim, not exhaustive nuisance coverage and not a terrain result.

[[EXP-20260820-001 - R2l fresh replicated face8 localizer]] executed its authorized guarded pair and fresh C1/L1/L2/C2 sequence. The pair and all four lifecycles passed, and C1/C2 had zero outside-mask mismatches. The scientific gate was inconclusive: L1/L2 had `20,634,078` outside-mask disagreement observations, union `211,650` pixels (`68.896%`), zero all-frame intersection/core, three large components, and `0.537916` dominance. James independently reproduced and accepted that procedural/inconclusive interpretation. [[EXP-20260820-002 - R2m offline cross-time correspondence diagnostic]] then computed the frozen full cross-time matrix and found no unique fixed lag: L1 has no eligible-pixel temporal variability, L2 does, all 121 lags fail, and individual exact pairs/minima remain nonselecting. James independently accepted the result. Fixed wall-clock alignment is closed as nonviable. [[EXP-20260820-003 - R2n PC state-equivalence read candidates]] now bounds six equality candidates at exact PCs `0x00414585` and `0x0041458F`, rebinds them to the auto-hardware build, and excludes asynchronous polling and transient renderer scratch. No face visibility, no-effect, terrain, collision, material, causal, or retail claim follows. Its offline-design pickup is consumed by EXP-004; no runtime or process-memory read is authorized. R2 remains open.

## 2026-08-20 pickup - R2o `-005` exact-census amendment frozen offline

[[EXP-20260820-004 - R2o completed-present state calibration protocol]] now
binds the R2n phase snapshots to one normal `0x0040FFC0` invocation, a
successful EndScene return, exactly one successful fullscreen Flip or windowed
Blt return, and outer completion PC `0x0040FFE3`. The exact instruction spans
are byte-identical between retail and auto-hardware builds. Static evidence
does not prove Gamescope compositor timing.

The design uses two fresh retail-DAT controls, exactly three
complete invocations per process plus one completion-to-next-phase screenshot-
equality check, exact
corresponding state/image equality, and no nearest-state selection. The
argument-free executor was subsequently implemented and James-accepted.
Authorized `-001`, `-002`, and `-003` D1 attempts rejected before attachment
on focus readiness, nested-display scoping, and host-path casing respectively.
The authorized `-004` D1 then reached one exact `0x0040FFC0` hardware trap
after arming local DR0 on an exact 16-task census, but its immediate all-task-
stop census differed. It rejected before TID selection, R2o process-memory
reads, stopped captures, or further scientific action; D2 did not launch.
All 16 register sets were restored and read back, cleanup and retail `R:`
restoration are clear, and James accepted the procedural rejection. The
evidence does not identify why the census differed. R2 remains open.

### R2o offline executor implementation (2026-08-20)

The James-accepted R2o static/protocol design in [[EXP-20260820-004 - R2o completed-present state calibration protocol]] has an argument-free executor and regression suite. The consumed `-001` D1 rejected safely because focus had not settled. The separately authorized `-002` D1 then passed hardware Direct3D and Anthill Level01 but rejected safely before attachment because discovery/guards used the nested X display while the focus commands incorrectly used the unscoped host environment; D2 did not launch. James accepted both rejection boundaries. Neither run produced a ptrace session, debug-register write, R2o state read, stopped screenshot, DAT/localizer, or candidate action.

The display-bound `-003` D1 passed hardware Direct3D, Anthill Level01, and
focus, then rejected before ptrace because the R2o pre-attach asset guard used
a lowercase Linux path for the physically uppercase Level01 DAT. D2 did not
launch. No debugger action, R2o state read, stopped capture, DAT/localizer, or
candidate action occurred; James accepted the rejection. The consumed `-004`
amendment fixed those paths and reached the first exact hardware trap, then
rejected on a changed task census before selection/read/capture. The active
offline `-005` amendment retains the exact no-churn rule and adds atomic
per-check census receipts with independently recomputed added, removed, and
reused-TID/start deltas plus a terminal failed stop-all record. Only cleanup
may follow a mismatch. Rejected packets authenticate their full journal prefix
against the exact R2o action/value grammar and exact baseline restores;
accepted packets require physically adjacent, action-ID-bound one-to-one
inline open, stop, and capture census bindings with no unused receipt. Every
census is bound to the immutable open `(TID,start_ticks)` list, and rejected
prefixes bind exact raw-stop/slot/DR6/active-debug transitions. The attachment
list itself must equal that complete immutable `(TID,start_ticks)` census, and
stop receipts accept only one supported recorded register layout with a
derived three-native-word payload held constant across the packet; this
matches the retained `-004` `x86_64`/24-byte stop evidence rather than a
synthetic fixed-layout assumption. Raw breakpoint stops must additionally have
zero ptrace event and independently decode from `wait_status` as stopped
`SIGTRAP`; the completed ptrace-open list must already be in the exact
immutable sorted order rather than being normalized during validation. At that
pre-run boundary, `-005` stage/evidence/aggregate paths were uncreated and
unauthorized. The later consumed D1 repeated census drift and ended retries;
the result is recorded below. A separate task-lifecycle diagnostic is now the
active route. No terrain, collision,
material, visibility, causal, or retail inference follows.

Historically, James rejected the `eb28b77` correction because its evidence fixture still had impossible debugger ordering, its pre-title chronology and exceptional debugger dispositions were incomplete, rollback failure could retain false acceptance, and D1 was not revalidated around publication. Later audits required guarded PID/start in the task census, exact open/select/close and result payloads, nondecreasing journal time, pending demotion on terminal finalization failure, and finally a pending ambiguity receipt even when that demotion rename fails. The accepted executor enforces those plus the exact interleaved journal/trace state machine, published-unverified aggregate, and repeated control validation. The `-001`, `-002`, and `-003` D1 attempts are consumed pre-attach rejections; `-004` and `-005` are consumed first-trap task-census rejections; every D2 arm is obsolete and unrun. R2o retries are closed, and P0A below is the sole active audit boundary.

## 2026-08-20 pickup - R2p passive task-lifecycle diagnostic

The authorized R2o `-005` D1 again reached the first exact `0x0040FFC0`
hardware trap and then rejected on the immutable task census. Its authenticated
delta is one addition, TID `1648646`, start ticks `28065259`, with no removal
or reused TID. It rejected before R2o reads/captures; all 32 permitted
debug-register actions completed and restored the original 16 tasks, cleanup
and retail `R:` restoration were clear, and D2 was never created. James
accepted the rejection. This ends R2o retries under the frozen rule.

[[EXP-20260820-005 - R2p task lifecycle diagnostic]] authenticates `-004` and
`-005` offline. Its result is
`diagnostic-valid-task-addition-identity-unresolved`, SHA-256
`8d35c6b68a21d881ad98981db6842b8d050a17d7900c29fec4ea319378f70e43`.
The analyzer binds every classified-manifest entry, exact file-set closure,
and the accepted R2o grammar before interpreting the task delta. The earlier
`b407bcf2...2d5` output is retained as obsolete and is not an active result.
The added task's name, creator, role, module, lifetime, and debugger dependence
remain unknown. PC static evidence finds one direct `CreateThread` call at
`0x0042CF04`, but does not bind it to the Linux task.

At the final pre-run audit boundary, the sole active pickup was the frozen P0A
passive `/proc` lifecycle control. Its argument-free executor and independent
validator were implemented offline and remained unrun. The hardened
publication gate authenticates the
complete hardware/Level01/navigation/runtime prefix, exact audit and `R:`
restoration chronology, and a real isolated X11/XTEST ABI fixture before either
scientific or rejected classification. Rejected classification additionally
requires an authenticated retained sample prefix, one enumerated runtime-failure
class, exact title success/failure chronology, sample-local one-of-two metadata
outcomes, an exact enumeration-to-identity-read partition, and exact
derived-error/disposition agreement. The analyzer contract requires exactly 521
requests at 20 ms cadence,
start within 2 ms, completion within 10 ms, no overlap, and strictly increasing
timestamps. It permits no debugger, signal, memory read, screenshot, DAT,
localizer, candidate, or R2o action. At that boundary it remained unrun; the
user had explicitly authorized the exact P0A collection, but launch was blocked
until corrected James acceptance. All five production identities (stage,
pending, published-unverified, accepted, rejected) were absent. Failed normal close stays pending
and permits no signal recovery. No terrain, collision, material, visibility, causal, or
retail claim follows; R2 remains open.

James's first P0A implementation audit rejected exact commit `52d9a0f` / tree
`8b271be` before runtime on nine evidence-integrity defects. Commit `b24890b` /
tree `8ce1cfc3` closed those nine and passed James's 150/150 focused and
1794/1794 full gates, but his second audit still **REJECTED** five reproduced
integrity gaps: timing-rejection self-invalidation, a manifest-time semantic
mutation window, duplicated/mislabeled unresolved metadata, non-hex executable
digests on partial rejection, and X sockets not peer-bound to Xwayland.

The second correction admits an exact timing miss only as its derived
procedural-rejection reason, revalidates current bytes after manifest creation,
fsyncs both parents after terminal rename, deduplicates unresolved identities
under neutral initial/added categories, requires lowercase hexadecimal
SHA-256s, and records both sockets' `SO_PEERCRED` PID/UID/GID plus peer start
ticks bound to the owned Xwayland PID/start. Its focused suite is 158/158,
including the real isolated Gamescope/Xwayland X11/XTEST fixture. No live game
or production evidence was created at that boundary; the authorization remained
unconsumed.
James audited that second correction at exact commit `c05f167` / tree
`d60d88bb`. He confirmed its five fixes, matching pins, 158/158 focused tests,
absent production identities, and clean git/session state, but **REJECTED** one
remaining lifecycle-partition flaw. Adjacent deltas missed changed start ticks
across a one-sample absence, disagreed on the later identity's unresolved
category, and mislabeled a baseline identity that returned after absence as
short-lived.

The third correction derives complete ordered per-TID/identity histories across
all 521 samples, detects reuse across gaps, partitions metadata by global
first-seen sequence in both analyzers, restricts short-lived identities to
post-baseline non-reappearing/non-reuse cases, and fails closed on the same
identity returning after absence with exact interval boundaries. Its focused
suite is 164/164. James audited exact commit `96e2fdf` / tree `60ab6a3d` and
confirmed those corrections plus the 1808/1808 full gate, but **REJECTED** one
remaining identity-anchor defect: both analyzers and the scientific fixture
accepted a process `(pid=10,start_ticks=20)` without the exact matching leader
task, including an empty census or a reused leader identity.

The fourth correction requires both per-sample enumerations to contain the
guarded PID, every stable sample to parse exactly
`(pid,process.start_ticks)`, and every task start to be no earlier than the
process start. Only an exact sample-local leader identity-read error permits a
missing parsed leader, and it makes the sample unresolved enumeration drift.
All lifecycle fixtures now retain a permanent process leader and exercise
changes on worker TIDs. Paired direct, scientific, and rejected-prefix
regressions cover all five counterexamples; the focused suite is 184/184. No
live game or production evidence was created; the 1829/1829 full repository
gate passes and the authorization remains
unconsumed. The next action is James re-audit of the next immutable commit;
only ACCEPT allows the authorized P0A launch.

James audited that fourth correction at exact commit `b8e8d44` / tree
`5c48cbb4`. He confirmed the process-leader anchor and every earlier fix, but
**REJECTED** the sole leader-omission exception because it was not exact. Direct
analysis accepted missing, extra, non-string, empty, or untyped leader
identity-error receipts; scientific and rejected-prefix validation also
accepted an empty error string.

The fifth correction validates every metadata-error receipt through one shared
gate before leader omission or early drift classification. Phase-specific
field sets and positive identities are exact; error text must be nonempty,
single-line, typed, at most 4096 characters, and in a closed exception-type
set, with bounded internal `P0AError` prefixes. Direct/scientific/rejected
regressions cover the malformed variants while a valid local leader error
still yields unresolved enumeration drift. The analyzer/packet suite is
201/201 and the separate native X fixture passes (202 total). No live game or
production evidence was created; the full repository gate passes 1846/1846
and authorization remains unconsumed. The next
action is James re-audit of the next immutable commit; only ACCEPT allows the
authorized P0A launch.

James audited that fifth correction at exact commit `a68076f` / tree
`10bdcad9`. He confirmed every earlier malformed-record fix, but **REJECTED**
one phase-provenance mismatch: the shared internal-error union let an initial
`identity` failure claim the metadata-only `task identity changed during
first-seen metadata capture` message. That impossible receipt could omit the
leader in direct, scientific, and rejected validation.

The sixth correction uses exact phase-specific internal-error sets. Initial
identity reads admit only five fixed `/proc/stat` parser messages; the
new-metadata phase admits those five post-read parser failures plus the exact
post-metadata identity-change message. Paired direct/scientific/rejected tests
reject the wrong-phase receipt and retain the valid new-metadata case. The
analyzer/packet suite is 207/207 and native X passes separately (208 total).
No live game or production evidence was created; the full repository gate
passes 1852/1852 and authorization remains
unconsumed. The next action is James re-audit of the next immutable commit;
only ACCEPT allows the authorized P0A launch.

James then returned **ACCEPT** on exact commit `8437c0a` / tree `53241906`,
independently passing 207/207 analyzer/packet tests, native X, and 1852/1852
full tests. The single exact argument-free wrapper invocation was consumed on
2026-08-21 after a clean pre-launch audit. Hardware and Level Select gates
passed and focused `Right`/`Return` receipts completed, but the retained log
loaded level07 rather than Level01 and reached `Start ClearLoadScreen`.
The Level01 gate timed out before `collection.json`; therefore P0A-AH-001 has
zero task-lifecycle samples and no scientific lifecycle result.

Guarded `Alt_L+F4` delivery completed on the focused loading window, but the
runtime survived 89 bounded polls. The executor used no signal fallback,
retained the stage and evidence as pending, and did not restore `R:`. The
retained post-close audit has a raw census but `parsed: null` because Make's
stderr followed the JSON stdout; the immediate post-wrapper read-only audit
recorded seven Gamescope/Wine processes and private sink
`ablpc_mute_1834769` as live and unattributed. Runtime identity records
Xwayland `(1834812,30382270)`, but both real Xlib sockets peer with Gamescope
`(1834786,30382246)`, so the isolated fixture did not reproduce live socket
provenance and terminal validation would also have rejected. Pending
disposition `ca2dfaa3...0d80` records the Level01
timeout, normal-close failure, `baseline_r_restored: false`, and null process-
memory read/write, debugger, signal, screenshot, DAT, localizer, candidate,
and R2o fields. No retry, close retry, signal, restore, publication, or second
launch is authorized. A cleanup/recovery decision and any corrected passive
successor require fresh explicit authorization; a successor must also separate
audit stdout/stderr and resolve/re-freeze the Gamescope/Xwayland peer binding.
All terrain/collision and task-lifecycle questions remain open.

The first offline postmortem correction retires the consumed argument-free
P0A wrapper: it now fails closed and no P0B identity or successor arm exists.
Audit receipts preserve and authenticate stdout/stderr independently and parse
JSON from stdout only. Runtime provenance now records both X sockets' actual
common Gamescope peer as a bounded `/proc/stat` + cmdline identity with exact
owned command; the display is separately authenticated by the sole exact
Xwayland launch marker. The corrected focused lifecycle/analyzer/packet/native
suite passes 215/215 and the full repository gate passes 1859/1859 with zero
tracked-file violations, without controlling any live runtime process.

Static postmortem evidence also closes the tempting timing-only repair. On the
path that enters Level Select, retail instruction `0x0043DB83` resets
`word [0x00599AF8]` to zero. The selector tests the current Right bit at
`0x00443F54`, increments its local position at `0x00443FB3` without a
previous-state edge test, and stores the selected position at `0x004444D6`.
The retained 180 ms hold followed by level07/progression position 10 is
consistent with repeated held-state polls, not proof of their exact count.
Because approximately 12 ms taps were already observed to drop, shortening
P0A's substituted persistent-X hold is not a deterministic repair. Save states
are user-reported unavailable and are not used. The separately established
direct focused `xdotool` route remained valid and was later operationally
reconfirmed below. A new passive packet still requires a new frozen identity,
fresh explicit authorization, and a new James verdict. No runtime recovery or
retry was implied by this offline work.

James **REJECTED** that first postmortem candidate at exact commit `932627d` /
tree `4742aa21`. Its packet schemas accepted JSON booleans as integers in
launch, process, X-peer, connection, and audit identities; the two X receipts
were cross-bound only by peer PID/start rather than the complete
PID/UID/GID/start tuple; and peer chronology and launcher/game/peer identity
collisions were not excluded. A fresh read-only audit during that review also
showed that the earlier seven-process census was no longer current.

The first correction attempted strict `type(value) is int` domains and complete
peer binding. Paired direct/scientific/rejected and executor regressions passed
269/269, the separate native X fixture passed (270 focused total), and the full
repository gate passed 1914/1914 with zero tracked-file violations. Its
collector/validator SHA-256 was
`71f9099aa2040e8cb141523f9114d38f9b972622b37dc935f513213995d528bd`.
James then **REJECTED** exact commit `740cb07` / tree `56818bd1`: equality-only
numeric fields still admitted JSON floats, `owned.polls` was ignored, direct
enumeration drift could mask forged sequence/request grids and unsorted or
duplicate task evidence, direct metadata-error partitions were weaker than the
packet path, and a missing runtime PID escaped as a raw `KeyError`.

The next correction makes every equality-only numeric field an exact JSON
integer, including collection count, title/navigation holds, plan contract,
settle duration, and owned-clear identity/polls. One shared task-partition gate
now enforces sorted unique enumerations/tasks, exact identity-error gaps,
unique first-seen metadata failures, the leader anchor, and sequence/request
grid validation before any unresolved drift return in both analyzers. A
malformed or contradictory metadata success raises `EvidenceError`; only an
exact bound metadata-failure receipt produces an unresolved identity. Missing
runtime fields also fail as evidence errors. The suite passes 297/297
non-native focused tests plus native X (298 total), and 1942/1942 full tests
with zero tracked-file violations. Current collector/validator SHA-256 is
`415fe20a699a3491735c9cbbb8f169da65ee067ef842811125964dc098085e4e`.
At that checkpoint the corrected immutable candidate still required James
re-audit and created no successor identity or runtime authority. The later
ACCEPT verdict is recorded below.

At `2026-08-21T05:35:13-04:00`, a new read-only `make session-audit` recorded
three unattributed runtime helpers—Gamescope `1834786`, gamescopereaper
`1834935`, and winedevice `1834980`—plus sink `ablpc_mute_1834769`, with no open
managed session. An independent process-existence check found launcher shell
`1834769` and those three helpers present, while recorded Xwayland `1834812`
and game `1835030` were absent. This is a timestamped state transition only;
their exit cause is unknown. Pending evidence, stage, `R:` targeting the stage,
and the absence of accepted/rejected/published terminal paths are unchanged.
No close, signal, process-memory access, restoration, or launch occurred.

James subsequently returned **ACCEPT** for the complete offline P0A postmortem
validator at exact commit `1b61da32c93b1238c108c0a95cb02628f3284949` / tree
`925ce807af1cd4db706a2d6f733ba935b73d30ba`. His independent gate passed
297/297 non-native focused tests, native X (298 focused total), 1942/1942 full
tests, and 50/50 reproduced adversarial counterexamples. That verdict closes
the validator correction only: P0A-AH-001 remains consumed/pending with zero
samples and no P0B identity or runtime authorization follows.

The prior pickup's statement that a deterministic Level01 route remained
unknown was incorrect. With explicit user direction on 2026-08-21, the exact
abandoned P0A group and winedevice were recovered after TERM failed, using
KILL only on those verified targets; the private sink disappeared and the
next session audit was clear. P0A pending evidence/stage bytes and `R:` were
not changed. A fresh non-evidentiary PC launch then used the accepted
auto-hardware image `1e1d5099...c41f` and the established direct focused
`xdotool` sequence: 180 ms Right after the LevelSelect marker and one-second
settle, one-second gap, 180 ms Return, then final focused 180 ms Return. The
log loaded `Y:\PC\BUGS\cd\level01\level.dat` and reached Start/End
ClearLoadScreen, End InitMainGame, and NextLife. Transient 640x480 compositor
frame `77f6eeff...84f598` visually shows live Anthill gameplay. No
process-memory access, save state, debugger, DAT mutation, or `R:` change
occurred. Game PID `1978909` in process group `1978654` remains intentionally
open for the user and is prohibited as P0B evidence.

This operational reconfirmation preserves KU-074: the live semantics of
carousel counter `0x00599AF8` remain unknown. It corrects only the route
boundary. P0A regressed by substituting its new persistent-X held-state input
for the already proved direct focused `xdotool` delivery. The next offline
work is a fresh P0B packet that retains the accepted 521-point passive `/proc`
collector and packet validator, never touches P0A pending bytes, reuses the
proved pre-collection route, and receives new identities, tests, James
acceptance, and explicit runtime authorization before launch.

### 2026-08-21 P0B first immutable audit rejected and corrected offline

The fresh `ablpc-r2p-p0b-passive-lifecycle-v1` source, argument-free wrapper,
and P0B test suites now implement that route under new P0B stage/evidence
namespaces and `Y:` without changing P0A's pending stage/evidence or `R:`.
Complete P0A tree manifests are pinned and checked before/after. Direct
`xdotool` performs only carousel Right and select Return before persistent
connections open; the existing independent worker retains the sole title
Return at sample 5 of the exact 521-point grid. Wrong-level loads, nonexact
settles/keys/windows, log-prefix drift, and missing/reordered/duplicate
post-grid gameplay markers reject.

The wrapper is intentionally offline-only and refuses launch. Scientific
publication requires a valid grid plus the exact post-grid gameplay gate;
collection failures may publish only as exact procedural rejections, while
precollection/gameplay-gate and cleanup failures remain pending without a
lifecycle claim or signal fallback.

James **REJECTED** the first immutable implementation at exact commit
`2277b75ecf8170fb2e1fc28f9cb24d19c0b8471b` / tree
`cf2f88cb64cca22bd811751318ae8ee8ef2f1b21`. He reproduced seven boundary
families: a cloned stale `bugs.log` with no reset/file identity; `Y:`-specific
wrong-level detection; xdotool receipts not bound to the nested display;
remaining boolean/float/null/list schema aliases; unauthenticated publication
receipts/manifest extras; a structurally permissive direct analyzer; and
inconsistent save-state/ptrace plus unauthenticated P0A `R:` exclusions.

The successor correction removes the staged log before launch, authenticates
its prior state and the newly created regular file's stable inode plus exact
UTF-8 append prefixes, recognizes every path spelling of a fresh level load,
binds xdotool to `runtime.x_display`, shares strict collection schemas before
all lifecycle outcomes, authenticates each publication phase, and uses one
save-state-inclusive prohibited-action map plus exact pre/post/current `R:`
mapping checks. The focused analyzer/packet/native-X suite passes 351/351,
including every reproduced counterexample and a real `_prepare` stale-log
regression. The full repository gate passes 2293/2293 in 663.10 seconds with
zero tracked-file violations. At that checkpoint the exact-commit James
re-audit was next; the following audit rejected it as recorded below.
The live operational Level01 process remains user-visible and is prohibited as P0B
input or evidence.

### 2026-08-21 P0B second immutable audit rejected and corrected offline

James **REJECTED** the corrected immutable candidate at exact commit
`8b8d19df0dd8d1db76ef26302753add2938039b0` / tree
`e8b58c9f26dea6473648b71017ad0ff5b05f3ede`. The nine reproduced blockers
were: a backslash-only pre-input level-load guard; incomplete nested P0A
manifest validation; acceptance of a later Level02 gameplay load; duplicate
XIDs or multiple focused windows; Python numeric aliases in retained audit
parses, the P0A `R:` boolean, and publication results; a non-object X
connection receipt leaking `AttributeError`; and a lexical `..` alias bypass
of terminal publication completeness. His independent focused suite passed
351/351; broad numeric/boolean/object-root sweeps found no tenth family. No
runtime or authorization was consumed.

The offline successor uses one any-drive/either-slash level parser through
navigation, gameplay, and packet validation; requires one total Level01 load;
validates exact P0A entries/count/order, unique window XIDs and one retained
focus, retained audit types, exact `R:` boolean domains, canonical result
bytes, object connection receipts, and canonical absolute packet roots.
Paired direct/scientific/rejected regressions pass in a 396/396 focused suite.
Collector/validator source SHA-256 is
`b50a81d847eb225b25b75f4f5baf6260ecb17b456e6005132be6a219489eb4e5`.
The wrapper remains offline-only; the live operational game remains untouched
and inadmissible. A new clean exact-commit James acceptance and fresh explicit
runtime authorization are still required before any P0B launch.

### 2026-08-21 P0B third immutable audit rejected and corrected offline

The preceding 396-test correction passed the complete repository gate at
2338/2338 in 666.31 seconds with zero tracked-file violations and was frozen
as exact commit `e0fa61a4e634a47e811bbe0a94b161a0aefca06a`, tree
`02550b15d3ed588f87b790f585057d130fc2233e`. James **REJECTED** it after
independently passing 396/396 focused tests and broad schema sweeps. A JSON
list/dict in a P0A entry `type` leaked raw `TypeError`, and a fresh wrong-level
load before the sole LevelSelect marker was ignored by executor and packet
route checks.

The successor type-checks an entry kind before dictionary membership and
rejects any parsed level load anywhere in the fresh LevelSelect prefix before
input, while still requiring the sole later Level01 load through gameplay.
Direct/scientific/rejected and executor regressions pass in a 405/405 focused
suite. Collector/validator source SHA-256 is
`347fd5062aff61c7302ced489621fa6b3caec7460b170150f6568969f413e014`.
No runtime action or authorization was consumed; the wrapper and live-game
exclusion remain unchanged. A new exact commit, James acceptance, and fresh
explicit runtime authorization remain required.

### 2026-08-21 P0B immutable offline design accepted

The third correction passed 405/405 focused tests and the complete 2347/2347
repository gate in 663.90 seconds with zero tracked-file violations. James
then returned **ACCEPT** for exact commit
`3c90a6f1e2291f21e756be7c7f339bd2bdbd33e9`, tree
`5fb8ea633f4401e471d29aaced69bb148afe37d5`, after independently passing the
focused suite and replaying prior/adjoining boundaries. Source SHA-256 is
`347fd5062aff61c7302ced489621fa6b3caec7460b170150f6568969f413e014`.

This was acceptance of the immutable offline P0B pre-runtime design only. At
that checkpoint it did not authorize runtime, and the wrapper remained unable
to launch. The fresh authorization recorded in the next section still requires
a clear pre-audit and the exact accepted direct Right/Return route,
sample-5 title Return, 521-point passive `/proc` grid, normal close, and
authenticated classification. The open operational game remains untouched and
inadmissible.

### 2026-08-21 P0B runtime consumed; valid collection pending on cleanup

Immediately after being told that the James-accepted P0B design still required
fresh explicit authorization, the user replied `okay continue on`. This is
recorded as authorization for one `P0B-AH-001` wrapper process invocation only,
with no process-memory access. The first exact invocation consumes the identity
regardless of pre-plan failure or exit and must never be retried. If it creates
pending or terminal evidence, the activated source bytes remain pinned because
the packet authenticates them and the namespaces enforce replay exclusion. If
it exits before any P0B namespace exists, the entrypoint may then be retired,
but the authorization remains consumed.

The old operational group was subsequently recovered under the user's explicit
`can't you alsojust use pkill or something` signal authorization. Exact group
`1978654` received `SIGTERM`; only surviving `gamescopereaper 1978824/33236126`
and `winedevice 1978862/33236135` then received guarded `SIGKILL`. The next
session audit was exactly clear. All five P0B namespaces were absent, P0A's
2339/17-entry trees and `R:` mapping matched, baseline `Y:` targeted retail,
the accepted source hash matched, and git was clean.

The exact argument-free P0B wrapper was then invoked once and is now consumed.
It reached hardware Direct3D, Anthill Level01, the sample-5 title Return, all
521 requested 20 ms samples, and the ordered gameplay gate with no acquisition,
metadata, or title-input error. Direct analysis returns only
`diagnostic-valid-task-added`: `(TID 2086681,start_ticks 34785536)` first
appears at sequence 27 and persists through 520. There are no removals, reused
TIDs, short-lived tasks, or mixed lifecycle class. Collection SHA-256 is
`d8ff0e76d62cb9ce133dc48845aa00ef0ac92a7083b48d9c187d312c8d44bc2f`.

Normal `Alt_L+F4` delivery completed, but process group `2086248` survived all
bounded polls. The runner therefore exited 2, used no signal, left baseline
`Y:` at the P0B stage, and retained the exact 26-file packet under pending.
Scientific and rejected validators both refuse the incomplete cleanup/
publication inventory. James **ACCEPTED** the collection only as a provisional
finite-grid task-addition result and **ACCEPTED** the fail-closed pending
interpretation. At that P0B checkpoint it proved neither task creator/function,
post-grid persistence, cross-run reproduction, nor a terrain/collision fact;
the later P0C section below updates only the reproduction/debugger-necessity
boundary.

### 2026-08-21 P0B authorized-signal recovery candidate

The same user message authorizes exact post-run signal recovery, not a second
P0B invocation. James accepted an additive recovery design that leaves all 26
pending files and all four plan-pinned sources unchanged. New protocol
`ablpc-r2p-p0b-authorized-signal-recovery-v1` pins the pending tree at 26
entries / `323c958d...451661`, revalidates every frozen PID/start before TERM
and any survivor KILL, records every signal/poll and exact sink action, requires
a clear audit before atomic/fsynced baseline-`Y:` restoration, then requires a
second clear audit, unchanged P0A/`R:`, exact assets, a closed manifest, and a
separate `recovered-out-of-band-after-authorized-signal` result. It can never
relabel the original run as normal-clean or authorize another runtime.

James rejected first implementation `575756d` / `004bf35d`: its validator
accepted numeric aliases, forged commands and contradictory event histories;
group enumeration could omit unresolved `/proc` rows; individual signals used
stale poll identities; immutable-tree/manifest checks were incomplete; and
publication plus one-shot failure state were not genuine. No recovery action
or signal occurred during that audit.

The successor freezes the exact command for all 12 process identities, retains
and rejects every unresolved group-enumeration row, rereads the full exact
identity immediately before every individual signal, authenticates consecutive
bounded poll contracts and monotonic present-to-absent histories, validates
complete current immutable trees and mappings, consumes an exclusive attempt
namespace before preflight, retains a separate stable failure namespace, and
publishes through a fresh unverified namespace with phase-derived canonical
receipts. Unbound operator Git claims were removed. Recovery module/wrapper
James then rejected exact successor `d4de863` / `208e6fd` for three remaining
counterexamples: type-insensitive comparison of the retained original-pending
receipt, acceptance of a poll after a prior exact-deadline poll, and ordinary
directory renames that could overwrite a namespace created in the
check/rename race. No recovery action occurred.

The next correction uses exact recursive comparison for the pending receipt,
forbids every post-deadline poll, and performs both publication moves with
Linux `renameat2(RENAME_NOREPLACE)`, failing closed if unavailable. SHA-256
values are now `d1b3e4af...3c38a` and `2b26e74d...fa2e1`. Recovery tests pass
48/48, the complete non-native P0B set passes 482/482, native X passes
separately, and full `make check` passes 2395/2395 in 672.58 seconds with zero
tracked-file violations. At that checkpoint the corrected recovery had not
run; exact commit and James pre-execution ACCEPT remained required. The live
P0B group/sink were untouched and `Y:` still targeted the P0B stage.

### 2026-08-21 P0B recovery failed consumed; operator cleanup completed

James accepted the corrected recovery at exact commit
`fae9b2f4c4e840f64f41d92dfc8efb21d7edaa45` / tree
`a6e9148d84d56effb32b532327c35a1e4b79f33e`. Its sole invocation is now
consumed. It sent the authorized group TERM, then failed closed when exiting
processes still existed but exposed cleared command lines during the next
identity guard. It did not restore `Y:` or publish recovered evidence. The
separate recovery-pending and recovery-failed trees remain exact at 6 entries /
`444b221e...f309e` and 1 entry / `8e2fb90e...f5d1`.

Between the authenticated pre-recovery and post-TERM states, 160 bytes of
shutdown text were appended to the original P0B `launch.stderr`. Chronology,
content, and retained-FD provenance make attribution to recovery shutdown
consistent, but it remains an inference. The suffix SHA-256 is
`aa26aff2...da66`. That historical 26-file pre-recovery packet was
`323c958d...451661`; its current, append-preserving identity is 26 files /
`1092fcb9...25f2`, with `launch.stderr` exactly 11,423 bytes /
`fb2ba241...eaf5`. The append is preserved, not repaired or truncated. The
remaining exact census was Gamescope `2086265/34784563`, gamescopereaper
`2086416/34784596`, and winedevice `2086454/34784605`; there was no sink or
open session.

The user-authorized operator cleanup was implemented at exact commit
`4de8b085f856a54fec315a078dc4f07dc8161852` / tree
`666cd92f5cdb933ebe68efb04a308387d7d6d528`, passed 30/30 operator tests,
266/266 focused tests, and 2425/2425 full tests, and received James
pre-execution **ACCEPT**. Its sole invocation sent individual SIGTERM and then
fresh-identity-guarded SIGKILL to only those three survivors. Both retained
post-signal and post-restore audits are exactly clear; `Y:` is atomically
restored to retail `BUGS_PC-full-disc`, while `R:` remains on the exact P0A
stage. The operator added no later log suffix.

James independently returned terminal **ACCEPT** for the 15-entry operator
envelope, tree SHA-256 `24df2fb7da89effca3e72a9b52e4bcb1ea15184bcd0401841b6954ce3a23d65b`.
The accepted disposition is only `operator cleanup after failed recovery`:
the recovery attempt is `failed-consumed`, the original P0B packet is
`pending-cleanup-failed`, the original run is not relabelled, and no future
runtime is authorized. The provisional finite-grid task addition remains
unchanged and does not identify the task's creator/function or establish any
terrain, collision, material, visibility, or causal claim.

The first post-cleanup `make check` correctly exposed six operator-test
fixtures that read the real `Y:` link while constructing a synthetic
pre-cleanup/staged invariant. No production source or evidence defect was
involved. The test helper now supplies the staged `Y:` identity explicitly,
leaving the accepted operator source and retained packet bytes unchanged. The
focused operator suite passes 30/30 in the retail-`Y:` environment and the
complete final-state gate passes 2425/2425 in 673.91 seconds with zero tracked-
file violations.

### 2026-08-21 P0C reproduces the post-title addition; role remains unbound

Offline P0C authenticates both R2o D1-AH-005 and the append-preserving P0B
packet. P0B is exactly 16 tasks at sequences 0–26 and 17 at 27–520, with sole
added identity `2086681/34785536`; first-seen metadata is a generic sleeping
`bugs.exe` task in game Tgid `2086503`. R2o independently changes from 16 to
17 between its open-and-arm and first-trap censuses. Because P0B uses no
debugger, debugging is not necessary for this lifecycle class. The two Linux
identities are not proven to be the same logical task.

PC-native bytes place the sole direct `CreateThread` call inside the Level1a
DirectSound stream-start path: `FUN_0042BB90` PLAYTRACK/buffer setup ->
synchronous `WM_COMMAND 0x9C46` -> `0x00401276 -> 0x0042CE80` ->
`CreateThread` at `0x0042CF04` -> worker `0x00440F50`. The P0B append contains
the corresponding Level1a PLAYTRACK/SETMUSICVOL lines. This makes the PC audio
stream worker the strongest candidate for TID `2086681`, but no evidence binds
the Linux TID to the Windows start routine, so attribution remains inference.

The first P0C implementation passed 28/28 focused and 2453/2453 full tests but
James rejected exact `f362fae` / `de8f1af` for no-replace/directory-durability,
hard-coded topology/no-debugger/log-chronology, incomplete static-path/source-
ledger, unsupported BPF-environment, and one timing-wording boundary. Its
`task-attribution-001` output remains preserved at `ecd92bfd...9c7`.

The `task-attribution-002` correction is SHA-256 `6156b968...1f88` and passed
44/44 focused plus 2469/2469 full tests, but James rejected exact `923ffb2` /
`4db811a`: its complete executed-source claim omitted imported intermediary
`r2c_f0.py`. It remains preserved as rejected evidence.

Fresh `task-attribution-003` is SHA-256 `62af5c09...d6ff`;
analyzer/wrapper SHA-256 values are `a3f35182...813b` and
`68410c5c...8563`. It retains the canonical no-replace publisher, exact 16/17
and no-debugger/log semantics, complete static spans, and now pins both
`r2c_f0.py` and its active `r2c_localizer.py` dependency. It also pins package
initialization and the two parser modules that initialization executes. An
independent AST import-closure regression requires the wrapper, analyzer, and
all nine transitively imported local modules to equal the pinned set. Its
focused suite passes 45/45 and the full gate passes 2470/2470 in 647.23 seconds
with zero tracked-file violations. The final exact-tree gate passes 2470/2470
in 648.20 seconds with zero tracked-file violations. James independently
**ACCEPTED** exact commit `f2629944b9163ae39e608320e60e7fed76fabb09`,
tree `9c7c1294e60f3c0ed6bb47f9f8575362d9ac1d45`.
It rejects both an immutable 16-task census and a universal 17-task census.
Offline R2q census-barrier design is justified, but runtime is not ready or
authorized: it must use an authenticated gameplay transition, a prospectively
fixed quiet interval, a census described only as pre-attach stable, immediate
pre-attach revalidation, and continued fail-closed checks. No live session,
runtime `/proc`, memory, debugger, signal, or terrain/collision action occurred.

## 2026-08-22 R2q offline quiet-census design

At the 2026-08-22 `-011` boundary, R2q was frozen and implemented offline as
the prerequisite barrier for a future completed-present terrain/collision
observation. The retained P0B
collection ends `51,903,350 ns` before the authenticated gameplay marker, so
it contains zero post-gameplay census samples and cannot itself establish a
quiet interval. The design therefore fixes 3,002 per-process census summaries
at 20 ms request spacing: the first-to-last request span is
`(3,002 - 1) * 20 ms = 60.020 s`, while accepted acquisition remains capped at
60.000 s from its durable attempted-action timestamp through debug-register
restore, detach, and the post-detach census. It makes no fixed task-count or
TID claim; the first post-gameplay census is each run's baseline.

The future protocol is two independent controls, D1 then D2, under fresh
`-008` namespaces. It stages and restores `Y:` while preserving P0A's exact
`R:` target, records the actual first `PTRACE_SEIZE` syscall separately from
its durable receipt, and retains the entire first request and task inventory.
Each control includes three complete four-phase stopped invocations, six
triplicate stopped batches, and one pre-title gate PNG: 19 PNGs per control,
38 total. Timing validation can conclude only that timing boundaries pass;
scientific acceptance stays undetermined until the complete packet validates.

James rejected immutable design `quiet-census-design-001` SHA-256
`529a798f...217` for validator, timing, receipt, capture, topology, anchored-
read, and source-closure defects. The `-002` correction, SHA-256
`7de8d565...3ad`, passed 69/69 focused and 2539/2539 candidate-tree tests, but
James **REJECTED** exact `a8840d5` / `b0cdfb3`: direct construction still
accepted forged P0B title, metadata, pre-title-log, and P0C cross-bind fields;
its advertised closed receipt grammar was descriptive rather than executable;
and one Vault coverage sentence contradicted the timing validator.

Immutable `quiet-census-design-003`, SHA-256 `c41256e5...3931d`, closed the raw
P0B/P0C title, metadata, and log defects, but James **REJECTED** exact commit
`caeddfd45d5d9c6524908cd258070ff40265171d`, tree
`ac853d4960bfeaa987e9832747f6dd427a83e99d`. Its runtime schemas still accepted
empty or late censuses, unauthenticated manifest contents, action after failed
preflight, reversed/unanchored captures, and a D1/D2 comparison that omitted
four of five result families and independent process identity.

Immutable `quiet-census-design-004` is SHA-256 `0f0f7cfe...05f9b`. James
**REJECTED** exact commit `0606bcf8d94e6d1d26eaa8e95f2993ba8e319914`,
tree `ca7800e516b324c6954bf45bc02f0b090b666b85`. The rejected validator allowed
a 1 ns three-key title envelope and post-final-Return pre-title evidence;
unbound census process/window/mapping/log hashes; unrelated stage, seize, and
detach identities; pre-seize/post-detach chronology inversions; descriptive
rather than executable task/debugger/memory/detach schemas; descriptive
namespace/publication/invariant/terminal rules; no executable D1-before-D2
state machine; process-group reuse; and boolean/float/range aliases in direct
auxiliary validation.

Fresh `quiet-census-design-005` is SHA-256 `a5472f01...31c5e`.
Analyzer/wrapper/test SHA-256 values at publication are `01e5af9e...8db6f`,
`cf02db6b...ccb5`, and `9bd72b48...f81e`. It preserves the complete `-004`
correction and makes all newly rejected boundaries executable: exact
Right/Return/capture/read/final-Return ordering with 180 ms holds and 100 ms
settles; underlying process/window/mapping/asset/raw-log cross-binding; exact
per-task seize-all, interrupt-all, `PTRACE_EVENT_STOP`, hardware-breakpoint,
memory-read, debug-register readback/restore, signal-zero detach, and task-
identity lifecycles; fresh namespace and `RENAME_NOREPLACE` publication
receipts; accepted/rejected/pending terminal validation; and an authenticated
D1-terminal-before-D2 two-control state machine that forbids PID/start and
process-group reuse. Direct numeric types and ranges are closed. The corrected
attach path preserves allowed baseline DR6/DR7 bits, continues every task
before accepting the selected task's natural hardware stop, then interrupts
only nonselected tasks. The focused suite passes 150/150. The full repository
gate passes 2620/2620 in 772.75 seconds with zero tracked-file violations.
James's subsequent exact rejection is recorded immediately below. No runtime
entry point or authority existed, and this added no terrain, collision,
material, visibility, or causal conclusion.

James **REJECTED** exact `814ada4054be6fa345bff39cc83d37eea6887381` /
tree `b79e88587a5bbc99337eeab3d45e540bbbc58eaf`. The `-005` validator still
accepted wrong/duplicate Level01 loads and duplicate markers; could not enter
D2 after D1 acceptance; did not authenticate reset-log, session-audit,
game-close, mapping-transition, rename-identity/reread, or both-parent
durability facts; treated asserted breakpoint PCs as register state; omitted
the second EndScene continue/wait; could classify cleanup uncertainty as
rejected; discarded successful failed-action receipt prefixes; admitted
nested boolean/float aliases; failed to bind D1/D2 P0A invariants; and allowed
an arbitrary title task list.

`quiet-census-design-006` SHA-256 `a068f686...1b33` was frozen but superseded
before James audit when final self-review found that its D1 accepted-root tree
hash was only cross-control equal, not recomputed from an authenticated tree
manifest. Immutable `quiet-census-design-007` is SHA-256
`f7cf2346245a4eb43eae1453e5cdd02257b462d79a58f8f691a3796ceba62d12`.
Analyzer/wrapper/test SHA-256 values at publication are `f489d3b2...e828`,
`cf02db6b...ccb5`, and `6a334143...7ae`. The correction parses one exact
staged-drive Level01 load and one occurrence of every gameplay marker; uses a
state-specific D1/D2 namespace and exclusive authenticated one-shot identity;
cross-binds fresh-log inode, raw clean-audit inventories, normal-close receipt,
and compare-before stage/restore transitions; authenticates canonical
published envelopes by exact destination reread, rename inode identity, both
parent-directory fsyncs, and a canonical one-entry accepted-root tree manifest;
and binds that exact D1 tree into D2 preflight.
Only the selected debugger task is armed. Every scientific register change has
an exact before/desired/readback ledger, EndScene has two complete
transition/continue/wait cycles, and cleanup restores the R2o-derived final
register state without self-certification. Failed actions authenticate and
dispatch their successful receipt prefix; any active cleanup or classification
uncertainty remains pending. Title capture is bracketed by stable leader-bound
task inventories, and all direct/nested integer and boolean domains reject
aliases. The focused suite passes 163/163; the exact-tree repository gate
passes 2633/2633 with zero tracked-file violations. At that `-007` freeze
boundary, exact commit and James verdict remained pending; the subsequent
rejection is recorded below. No runtime occurred and no runtime,
terrain, collision, material, visibility, or causal authority follows.

James then **REJECTED** exact commit
`ecf809f70af0a94c9d62ba21ce2a18e3ac8b43ab`, tree
`71b294f5a2b89c9262d217bb846c4e1309e92c10`, while independently confirming
the `-007` artifact/source/test/wrapper hashes and 163/163 focused tests. Five
blocking counterexamples remained: cross-receipt chronology was not enforced;
nonaccepted cleanup was shape-checked rather than bound to the authenticated
attach and maximal failed-action prefix; D2 and the aggregate copied rather
than independently reread canonical publication/tree bytes; malformed UTF-8
after `argv0` was ignored; and a pending action-9 control raised raw
`TypeError` through the two-control API.

Fresh immutable `quiet-census-design-008` is SHA-256
`9140145545fcd03dad674a3a8face8c645679d0e1f86d3a91cc3c60334dae155`.
Analyzer/wrapper/test SHA-256 values at publication are
`a67ee14f5a837ebc1bebeeb8447ec0bb6375f46d52233cbc4fa0a172d1b57e3d`,
`cf02db6beecf4fd8c4a52e7036bb7d1762f2ade1c209aa7bf74486a59316ccb5`,
and `bf351af82884d6549fad3368dbe7732e4c7a19b53fbc59e1117f66bb7af7d623`.
It enforces a closed action/receipt temporal partial order, including durable
one-shot before preflight, stage/log preparation before process identity, and
normal close → first clean audit → mapping restoration → second clean audit →
final invariant. Nonaccepted terminals now reconstruct the authenticated
launch/attach/register state, require an exact named failed-next kind/ordinal,
fully validate cleanup when attach was reached, and keep uncertain attach or
partial acquisition pending. D2 recomputes canonical D1 tree-manifest bytes;
the aggregate requires distinct post-D2 D1/D2 reread receipts with exact
bytes, timestamps, and file/parent identities. Terminal/comparison publication
binds source-parent identity and destination reread chronology/stat identity.
The whole command line is strict UTF-8 with exact NUL-separated arguments, and
nonaccepted aggregate inputs fail with `DesignError`. The focused suite passes
175/175; the first full repository gate passes 2645/2645 in 916.68 seconds
with zero tracked-file violations. Exact commit identity, final exact-tree
gate, and James re-audit remain pending. No runtime or terrain/collision claim
follows.

James **REJECTED** that exact `-008` subject at commit
`18591f3424f01eaaa69e0b5430889678df1c09d6`, tree
`ff65061f6cf3e67ea3c774852f39f3c4a9ffe7bf`. He independently matched the
published/source/test/wrapper hashes and passed 175/175 focused tests, then
reproduced five remaining semantic families: impossible Right-after-first-
Return and unrelated mapping/asset prefixes in coherent rejected terminals;
unrelated debugger cleanup or game-close receipts hidden by a later failure in
the same phase; an unbound timing/control-validation prefix before action-9
publication failure; and impossible or unbound source-parent device/inode
claims for successful terminal/comparison renames. Vault lint remained 608
notes, zero errors, and eight pre-existing warnings; Git was clean and no
runtime occurred.

Fresh immutable `quiet-census-design-009` is SHA-256
`c8c451fae413e2adb93f867723ff865185d700f697089a073029c9d4d13047a1`.
Analyzer/wrapper/test SHA-256 values at publication are
`1dc00b7f1fd0fd85359d18ffd40af4fc42359f976eacb38760bb3440b654e09e`,
`cf02db6beecf4fd8c4a52e7036bb7d1762f2ade1c209aa7bf74486a59316ccb5`,
and `a9e99944c252bf36547ad12e323a1854daebdd393132e543371cf629a74c07bb`.
The shared prefix validator now applies every present title-route and
mapping/asset relationship to accepted, rejected, and pending terminals.
Successful cleanup and normal-close receipts are cross-bound even if a later
receipt makes their enclosing phase fail. Action-9 timing and validation
prefixes are bound to the actual preceding receipt/manifests before any
pending return. Terminal and comparison publications include an authenticated
canonical-directory stat for the exact temporary parent, bind its inode, and
require one filesystem device across the temporary, both parents,
destination, reread, and terminal tree. Seventeen new coherent/direct
regressions bring the focused suite to 192/192 in 444.74 seconds. The first
full repository gate passes 2662/2662 in 1102.04 seconds with zero tracked-file
violations. Exact commit, final exact-tree gate, and James re-audit remain
pending. This is still an
offline prerequisite only: no game/emulator session, `/proc`, ptrace, memory,
signal, input, screenshot, mapping mutation, or terrain/collision evidence was
produced.

James then **REJECTED** exact `-009` commit
`f81502bd2cbe4915be21d313d1ea1c411c4cd11e`, tree
`e56942bc2f6fc2b5a0235c5bc469eb05c5c5f9bb`. He independently matched the
artifact/analyzer/test/wrapper hashes, passed 192/192 focused tests in 448.16
seconds, and left Git clean. Two blocker families remained. First, the shared
prefix helper covered only selected aggregate relations: coherent rejected
terminals could substitute the title-capture PID or gameplay-log inode, and
the same conditional-reduction gap extended across census, process, guard,
R2o, stopped-capture, cleanup, mapping, timing, and action-9 dependencies.
Second, terminal/comparison `source_parent_stat` times were internally ordered
but not anchored to the publication outer receipt or the two post-D2 rereads,
so ancient `1..2` timestamps still passed.

Fresh immutable `quiet-census-design-010` is SHA-256
`d07d3d5e9e71095080eaf854e1c1822720fb1791ea6b8ae3899dde7b85effd5c`.
Analyzer/wrapper/test SHA-256 values at publication are
`113fe44276bdb8ae1013d4a2910b4a59c695d3afae65987764f4bdcf4e46d13d`,
`cf02db6beecf4fd8c4a52e7036bb7d1762f2ade1c209aa7bf74486a59316ccb5`,
and `e4d7d0b4d6d089b652f22c24d8908cf613721d64be6a011ef95f70d2f5abaad0`.
One conditional reducer now applies every authenticated dependency-applicable
relation in accepted, rejected, and pending terminals. Coherent rehashed
rejected/pending fixtures cover process, census, title, log, asset, mapping,
R2o, continued/stopped capture, completion-image, cleanup, and invariant
families. Terminal publication now requires control validation before its
outer start and places source-parent stat inside that outer receipt before
fsync/rename/reread; comparison publication begins only after the ordered D1
and D2 post-D2 rereads. The focused suite passes 226/226 in 727.47 seconds; the
first full repository gate passes 2696/2696 in 1369.49 seconds with zero
tracked-file violations. Exact commit, final exact-tree gate, and James
re-audit remain pending. No live session, game/emulator launch, `/proc`,
ptrace, memory, signal, input, screenshot, mapping mutation, or
terrain/collision observation occurred.

James then **REJECTED** exact `-010` commit
`889f105aadb0eb55dfb4677750b186540235163c`, tree
`a93c929f275f58e4a8b55a047e057d6135c62e8f`. He independently authenticated
the 72,752-byte artifact and published hashes, passed 226/226 focused tests in
726.14 seconds, left Vault lint at 608 notes / 0 errors / 8 pre-existing
warnings, and left Git clean. The certifying counterexample was internal to
the nominal packet: its executed `PC/BUGS/bugs.exe` process record used
device/inode/size/mtime `401/402/403/404`, while the exact same-path and
same-SHA asset entry used `412/422/3/432`. Accepted controls and
dependency-applicable rejected/pending prefixes all admitted that impossible
composition because no validator cross-bound the two stat tuples.

Fresh immutable `quiet-census-design-011` is SHA-256
`6a8fd3df00406e0ed045b4bd16e94d3255cefdcf025a9d9862cf7e8fbcdc1022`
and is 73,008 canonical bytes. Analyzer/wrapper/test SHA-256 values are
`e8895a9bddf749650e1e292e103379e364b5083e6bc92baf456e3e5140791bfd`,
`cf02db6beecf4fd8c4a52e7036bb7d1762f2ade1c209aa7bf74486a59316ccb5`,
and `472cbabdf20114d3d392fe2a62e7865048965b821cd54b3229f83f83e36b332f`.
One shared validator now requires the executed path and SHA plus
device/inode/size/mtime to equal the exact `PC/BUGS/bugs.exe` asset entry in
the accepted-control path and conditional prefix reducer. The nominal fixture
derives its process stat tuple from that entry. Coherent direct,
accepted-terminal, rejected-terminal, and pending-terminal regressions change
the process inode and recompute every dependent process-guard and envelope
hash, then reject only on the new process/asset binding. The focused suite
passes 229/229 in 740.93 seconds; the first full repository gate passes
2699/2699 in 1397.31 seconds with zero tracked-file violations. Exact commit,
final exact-tree gate, and James re-audit remain pending. No runtime or
terrain/collision evidence or authority follows.

James then **ACCEPTED** the documentation-inclusive `-011` offline design
basis at exact commit `409cbfbe2b56c271909228d55ea340759b5c6435`, tree
`de4fa877e4aadae12b64e190ba313dca6e9a8d37`. He authenticated the docs-only
parent correction as exactly three `73,752` → `72,752` edits, confirmed zero
old and exactly three corrected occurrences, independently measured preserved
`-010` at 72,752 bytes / `d07d3d5e...effd5c`, and reauthenticated unchanged
`-011` at 73,008 bytes / `6a8fd3df...c1022`. Analyzer, tests, wrapper,
artifact, namespaces, and implementation bytes were unchanged; Vault lint was
608 notes / 0 errors / 8 pre-existing warnings and Git was clean. This ACCEPT
certifies only the immutable offline prerequisite. It grants no runtime
authorization and establishes no terrain/collision result. Any live R2q arm
still requires a fresh explicit user authorization under the accepted exact
contract.

### 2026-08-25 R2q runtime-edge correction through `-020`

The James-accepted `-011` artifact was an offline design only. The subsequent
runtime edge has not run. James **REJECTED** exact `-012` commit
`ac7e0b178b68408c26b9f007ffa785ccdb70eb22`, tree
`2acfa249e4e9e465c369e755ec9cda0b1c0e2e4a`, with its 92,099-byte artifact
`7fccf459...b8198`: the benchmark omitted production semantic validators and
the executable path still had pre-journal, ordering, publication, receipt-
prefix, deadline, cleanup, and provenance gaps. He then **REJECTED** exact
`-013` `c54ed0f79e149dfce215f723fec3fa90dc1cc7ac` / tree
`cbd2e1be001f8f21755338bc6f66378ef303bb2a`, artifact 94,739 bytes /
`bd0ec48c...b2b28`, for incomplete cleanup timing, unsafe accepted-rename
rollback, missing ancestor durability, incomplete partial-journal evidence,
no exact accepted-packet commit, and unauthenticated comparison-failure state.
`-014`, 99,092 bytes / `6ec83b3c...20ff`, was an intermediate correction
superseded without an immutable James verdict.

James **REJECTED** exact `-015` `6b2c867e125c9302bb5b28b18fb7333d03b4ab29`
/ tree `bb279267d00f2c9b0b00a854ab9d581d0547a449`, artifact 99,249 bytes /
`fe8a7712...a6f5`, after independently passing 44/44 runtime tests and
stopping the design run at 107 passed / 362.19 seconds. It did not retain the
complete validated packet, durably finalize and reread the marker, reread the
full post-D2 envelope, account for partial D1-lock/D2-admission failures,
reject a Boolean comparison alias, or execute the declared five-second bound
over the full publication. James next **REJECTED** exact `-016`
`5217ca08aa4ee7d4beefe49f7c040db36333f477` / tree
`c0420caeaaf3d462a72a553d412946b5b5f3c048`, artifact 99,969 bytes /
`432a4ede...8933`. He authenticated the artifact and a coherent direct
two-control counterexample: post-D2 file identities remained substitutable,
the five-second boundary ended before receipt/final reconstruction work, an
exact competitor could become unclassifiable, and the canonical Vault still
described `-011` as current.

The active `-017` candidate makes `acceptance-completion.json` the final
`RENAME_NOREPLACE` boundary. Before that rename, it writes/fsyncs/rereads the
durability receipt, reconstructs and semantically validates the complete
packet, rereads the pre-final envelope, and records the exact root and every
file's device/inode/count/hash. The completion file self-binds its prepared
device/inode. After rename, runtime fsyncs the accepted root, stably rereads
the completion, reconstructs the final tree, and enforces the same exact
five-second runtime deadline. Exact competitor and post-rename deadline cases
are retained as authenticated `ambiguous-nonowned-valid-envelope` or
`ambiguous-owned-late-envelope` pending outcomes rather than lost or promoted.
Post-D2, D2-namespace, control-failure, and comparison-failure validators bind
their observed trees to those committed identities. The artifact has frozen at
102,029 canonical bytes / SHA-256
`c6fe10e278f83f43a60d841c3d1be8dcd68aa63ecd0977ae5517fbe707c92fa7`.
Focused gates pass 261/261 design tests in 1,188.42 seconds and 59/59 runtime
tests. The full repository gate passes 2,790/2,790 in 1,843.51 seconds with
zero tracked-file violations; exact commit and James verdict remain pending.

The user's unconsumed explicit authority covers only one 521-point passive
P0A `/proc` task-lifecycle collection and explicitly excludes process-memory
reads and writes. The R2q wrapper is broader: its frozen future request includes
ptrace/debug-register work and eleven post-seize memory-read ranges per
control. Therefore the current authorization cannot activate R2q, even after
a James acceptance. No live operation occurred in this correction, and
KU-079, KU-080, KU-081, terrain, collision, material, visibility, causality,
no-effect, and retail-behavior conclusions remain unchanged.

James subsequently **REJECTED** exact `-017` commit
`2267cc5101c1f82222d72154f94b9899185b417f` / tree
`8166cc4a12e6f7fd02aa280350a7525284d27c08`. He authenticated its 102,029-
byte artifact `c6fe10e2...2fa7`, source hashes, 59/59 runtime tests, two focused
design tests, Vault 608/0/8, and clean Git, then demonstrated three blockers:
the retained 2.100-second benchmark did not execute either complete terminal
publication path and nominal comparison publication exceeded five seconds; a
valid complete envelope arriving during marker preparation lacked an owned
attempt and became unaccountable; and failure of the final accepted-root fsync
was falsely classified as durable/late merely because all files were readable.

Frozen `-018` corrects those exact boundaries. `PublicationDeadlineError`
records the actual deadline stage; the final completion attempt independently
records rename, final-directory-fsync, completion-reread, tree-reconstruction,
tree-verification, and final-deadline outcomes. Failure schemas v3 separately
derive complete-envelope validity and owned durability. A complete valid
envelope with no owned successful rename is
`ambiguous-nonowned-valid-envelope`; an owned post-rename fsync/reread/tree
failure is `ambiguous-owned-durability-uncertain-envelope`; only a fully
fsynced/reread/verified envelope that then misses the final deadline is
`ambiguous-owned-late-envelope` and durability-confirmed. Stable file identity
now compares device/inode/mode/size/mtime/ctime and deliberately excludes
atime, matching `_stable_regular_read` rather than treating a harmless atime
update as substitution.

The new anchored `terminal-publication-benchmark-004` executes three complete
control and three complete comparison publication paths on the experiment
filesystem, including production material construction, every semantic
validator, serialization, file/directory fsync, exact rereads, tree
reconstruction, and the final no-replace completion boundary. It is 3,233
bytes / SHA-256 `4cb6ed3491f98aaaea35249c880dffc231b9af0a89462a4708d0a28ecd0d7b2c`.
Worst control is 23.167699052 seconds; worst comparison is 79.340400010 seconds;
the prospectively fixed 180-second ceiling retains 100.659599990 seconds of
margin. A deterministic schema-valid synthetic activation ledger breaks the
design-source self-reference, and rebuilt seed hashes exactly reproduce
`67471eb9...f001` / `42f8d398...e58` after the design source changes.

Frozen `quiet-census-design-018/design.json` is 103,156 canonical bytes /
SHA-256 `435df6253370efcce1308dae2f0e038be0b45665dbd9456415d51bd70130d382`.
Design/runtime source hashes are `32d124f6...86d4` / `7ebee18d...f5a5`;
design/runtime test hashes are `89ca9599...125e` / `5401c46a...f69`; the new
benchmark generator is `f760f2a2...ce90`; runtime/freezer wrappers remain
`6803358b...a297` / `cf02db6b...ccb5`. Focused gates pass 262/262 design tests
in 1,386.74 seconds and 68/68 runtime tests. The full repository gate passes
2,800/2,800 in 2,003.33 seconds with zero tracked-file violations; exact commit
and James verdict remain pending. No live operation occurred; the retained
passive P0A authorization still cannot activate this broader R2q wrapper, and
no terrain/collision conclusion follows.

James **REJECTED** exact `-018` commit
`7e6a3b0f1a5c801399c19396aecff71646ac5e02` / tree
`2c99beff21048e5a5f42df4ee619e7bf83ee74a7`. He authenticated the 103,156-
byte artifact `435df625...d382`, 3,233-byte benchmark `4cb6ed34...d7b2c`, all
reported source/test/wrapper hashes, `validate_published_design`, 68/68 runtime
tests, Git objects, and a clean tree. Three blockers remained: a stage/Boolean
pair could assert owned-late without retaining the underlying deadline error;
the frozen 30-second failure-recording claim covered neither completed-action
nor comparison failure and started too late on ordinary failure; and benchmark
`-004` did not record the production design/runtime source bytes it timed.

Frozen `-019` retains a canonical nested deadline receipt with exact error code,
deadline, observed monotonic time, and checkpoint label. Runtime classifies
owned-late only when that receipt equals the chained `PublicationDeadlineError`;
the design validator additionally requires `observed > deadline`, binds the
deadline to `acceptance-completion.json`, and cross-binds rename and outer-
failure chronology for both control and comparison. The 30-second value is now
named and enforced only as the absolute failed/skipped durable journal-
transition tail. The frozen protocol explicitly sets the end-to-end failure-
accounting deadline to null and excludes receipt/manifest construction, packet
validation, serialization, fsync, reread, and publication from the narrow tail.

The two-phase source freeze committed immutable benchmark code as `3fe4833` /
tree `5953ebf`, then ran three complete control and three complete comparison
paths from that clean identity. `terminal-publication-benchmark-005/result.json`
is 4,563 bytes / SHA-256 `645376228b51dd1cfeac50e77b369f6ca1a153f0a972303dc4e6e9a5bf5c28fa`;
its tracked 1,363-byte data anchor is
`e6b542a297f73814281796a85108a5a542ab1d0cc6e64c5622ade7a5b95fe4de`.
The exact five-file ledger is `01abbe48...341f`; design/runtime/generator/test
hashes are `711db3a8...f4e4` / `e8eb63e9...f94b` / `b871395f...5b4c` /
`837b0ee1...9085`. Worst control/comparison paths are 22.983197250 /
78.945117065 seconds, retaining 101.054882935 seconds under 180 seconds.

Frozen `quiet-census-design-019/design.json` is 104,745 canonical bytes /
SHA-256 `f3d985a51d60adee3a63545d7209c7e214e58a7788f2dffe24b7fd959f5aeadf`.
Focused gates pass 263/263 design tests in 1,545.22 seconds and 68/68 runtime
tests. The first full repository gate passes 2,801/2,801 in 2,205.27 seconds
with zero tracked-file violations; exact final commit and James verdict remain
pending. No live operation occurred; passive P0A authorization still cannot
activate R2q, and no terrain/collision conclusion follows.

James **REJECTED** exact `-019` commit
`8e1b98958382886f4df9f39dc5046a9259ac0279` / tree
`c3334e33f8550c478a10a5a17b7747138e92fa1f`. He authenticated Git integrity
and cleanliness, the artifact, benchmark, tracked anchor, two-phase source
provenance, all prior corrections, and 68/68 runtime tests. Two certifying
defects remained: an owned final-deadline attempt could retain an impossible
outer `DesignError` or comparison phase instead of production's exact boundary
exception, and a list-valued attempt `stage` escaped the closed validator as
raw `TypeError`.

Frozen `-020` moves failure protocols to v5. A final-deadline attempt now
requires outer `R2qRuntimeError` plus the one exact production boundary message;
comparison additionally requires phase `commit-marker`. Control requires the
deadline observation at or before failure-accounting start, while comparison
requires it at or after comparison start; both retain observation at or before
failure completion. Attempt `stage` must be an exact string in the closed stage
set before membership or indexing. Direct control/comparison and full pending-
terminal regressions reject forged `DesignError`, wrong message/phase/code,
impossible chronology, and list/dict/integer/Boolean/null stages as
`DesignError`.

The immutable benchmark source commit is
`9e4ccf724f61ec0c4c22a341654c1d8f40de3a99` / tree
`f2502d873aa60bcf2d848cf169292835a4f36aab`. Benchmark `-006` is 4,563 bytes /
SHA-256 `72373103dfedaced6d176a306257545ac6a868150dcaac5e94a384fda17de95b`;
its 1,363-byte tracked anchor is `53c3f811...b7c3` and its exact five-file
ledger is `0f184368...bcf27`. Design/runtime/generator/test hashes are
`ff9b3342...04f1` / `f90d42a1...ed92` / `b871395f...5b4c` /
`d8b060e3...c273`. Worst control/comparison paths are 23.035894094 /
78.864340257 seconds, retaining 101.135659743 seconds under 180 seconds.

Frozen `quiet-census-design-020/design.json` is 105,429 canonical bytes /
SHA-256 `462b882d24922fa86520b9811f18f2ade9ca5dc154827a4f8d8667283966061a`.
`validate_published_design` passes; the complete R2q gate passes 331/331
(263 design plus 68 runtime) in 1,799.86 seconds. The first full repository
gate passes 2,801/2,801 in 2,458.12 seconds with zero tracked-file violations;
the documentation-complete exact-tree gate also passes 2,801/2,801 in
2,457.27 seconds with zero tracked-file violations.

James then **ACCEPTED** exact commit
`4635a5320ba48f87ee26923b3f31ce697d74e791` / tree
`fa5d63dacef3b98799927d016669c338b90aa5c0`. He independently confirmed Git
integrity and cleanliness, every source/artifact/benchmark hash, both published
validators, the exact runtime deadline exception chain, fail-closed forged
outer semantics and malformed stage values, 68/68 runtime tests, and both
coherent strengthened terminal arms. Vault lint remained 608 notes / 0 errors /
8 pre-existing warnings. This ACCEPT certifies only the immutable offline R2q
design/runtime edge as publication-grade. No live operation occurred; passive
P0A authorization cannot activate R2q, and no terrain/collision conclusion
follows.

## 2026-08-26 P0D consumed offline; P0E successor pending James

James rejected the first P0D pre-freeze candidate on six exact grounds:
one-shot consumption followed fallible setup, executed source was not anchored
to earlier Git blobs or its full local closure, terminal publication could
survive a durability failure, both `Y:` changes had unlink/symlink gaps, the
pre-restore owned-runtime census was stale, and the Wine host executable was
not frozen independently. Namespace isolation, the direct Level01 route, the
521-point grammar, passive-only authority, historical preservation, and
normal-close-only behavior were otherwise aligned.

While correcting the wrapper test, a legacy `runpy(..., "__main__")` fixture
created the real exclusive `P0D-AH-001.attempted` marker before failing on the
absent activation anchor. The 30-byte mode-0600 marker is retained at device
54 / inode 9281337 with SHA-256
`89883723f4cc51269caae0d46a13cba57a14ae58056c4826d60eaa18edc23f19`.
That consumes P0D. No game, launch, input, mapping change, `/proc` lifecycle
sample, process-memory access, or other runtime action occurred; the session
audit remained exactly clear.

Fresh P0E now implements the corrected offline boundary. The bootstrap creates
`P0E-AH-001.attempted` with exclusive open before every project import or
preflight; partial write, file/parent fsync, stat, reread, import, source,
configuration, path, and mkdir failures all leave the arm consumed. A
two-phase tracked activation anchor freezes exact Git blobs and SHA-256 values
for the wrapper-rooted local import closure and launcher closure. The separate
Wine host anchor is `/usr/lib64/wine-wow64/wine/x86_64-unix/wine-preloader`,
SHA-256 `3adeb326...1734f`, size 18072, device 38, inode 3825178, mode 0755,
mtime 1768608000000000000 ns.

Both `Y:` directions prepare and authenticate a same-parent temporary symlink,
reauthenticate the old mapping, atomically replace it, fsync the parent, and
stably reread the moved identity. Restoration also repeats the complete owned
process/session audit immediately before replacement. Runtime publication can
only move pending evidence to `published-unverified`; it never creates an
accepted or rejected terminal. P0E authenticates the consumed P0D marker,
P0A stage/pending/`R:`, and all five P0B trees before and after.

Focused P0E tests pass 519/519, including every James-requested adversarial
boundary. The exact source-phase tree passed `make check` with 3320 tests and
0 tracked-file violations, then committed as
`01902e0c7bff99bc17f10e9c21c2b4082112a14e` / tree
`aa80c5a2eb1ed49433cbb7b481f72f7d6ef5299b`. The exclusive activation freezer
generated canonical anchor SHA-256
`8ea16668f6da72d888ff35ce9cf9f59239716b86488b709cfc893af19ebddcbe`
from that commit. At that pre-run point P0E was unconsumed and all production
namespaces were absent. The final gate/commit and James acceptance of that revision
remain mandatory before the sole live attempt. No terrain/collision conclusion
follows.

James then **REJECTED** exact commit `b77775397bead19e6e31a9a3d97d71662b73ff14`
/ tree `85799bef2374b762a52f9c5122e7758b973cad35`. He confirmed the six original
P0D blockers were otherwise closed, but reproduced a byte-identical replacement
of P0D's physical marker and two publication-root/phase bypasses. Corrected P0E
pins the documented P0D device/inode/mtime in plan and receipts, accepts only
the four exact production packet roots, permits only publisher-reachable phase
prefixes, and binds terminal roots to their validator class. Focused tests now
pass 542/542. No live action occurred; a new source/activation freeze, full
gate, exact-tree James ACCEPT, and fresh clear pre-launch audit remain required.

James's non-certifying pre-audit then passed 542/542 plus a separate 106-case
adversarial matrix and returned `ACCEPTABLE-FOR-FREEZE`. The corrected
source-phase full gate passed 3343 tests in 2481.11 seconds with 0 tracked-file
violations. Source commit `c7bdd6c8b15c3697cc5ffeeea0a51e79d66ca60a` /
tree `e0a5fea3d0412bed8d674e4fd916705e328dd76c` is frozen by activation
anchor SHA-256 `7342d729cd91214bc820d19fa70e93a4b18cc312c1acd6548cda49167ad08c5d`.
The documentation-inclusive full gate, final commit, and James exact-tree
ACCEPT remain mandatory before the fresh pre-launch audit or live arm.

James **ACCEPTED** final exact `b1896e1ef650076a64ba2e15143bd4637c6587e9`
/ tree `a696e48d0c51d49ec7927c87c2b2647d8c803575` after independently
authenticating all eight blocker families and 542/542 focused tests. A fresh
pre-launch audit was exactly clear, and the sole P0E invocation consumed marker
`b3638ebd...f5235`. The proved PC route reached Anthill Level01 and completed
all 521 passive samples. Collection `9ed7d8e...456b0` finds one persistent task
addition: TID/start `(310752,9973602)`, absent sequences 0–26 and present
27–520, with no removal, reuse, acquisition/title error, unstable enumeration,
metadata error, or timing failure. James returned **ACCEPT — collection-level
only**. This reproduces the 16→17 topology; task role remains inference and no
terrain/collision claim follows.

Normal Alt+F4 delivery succeeded but the game did not exit. After 89 polls the
owned census was nonclear; the post-close audit recorded seven unattributed
game-stack processes and mute sink `ablpc_mute_310283`. P0E correctly omitted
final cleanup/restore receipts and remains pending; no publication namespace
exists, `Y:` remains P0E stage, and `R:` remains P0A. P0E is consumed and must
never rerun. At that checkpoint no further input, signal, sink unload, or
mapping restoration was authorized; agent recovery required the later fresh
explicit user authority and separately frozen, James-accepted additive protocol
recorded below.

### 2026-08-26 P0E additive recovery source accepted for freeze

The user explicitly authorized the separate P0E residue recovery. Candidate
protocol `ablpc-r2p-p0e-authorized-residual-recovery-v1` is additive: it never
modifies, renames, or classifies the original pending P0E packet. Its one-shot
wrapper consumes `P0E-R1-AH-001.attempted` before project import, requires an
isolated pinned Python 3.14 process and a clean exact Git activation, and has no
process-memory or game-input path. The recovery can signal only a frozen set of
12 original process identities after exact `/proc` reauthentication, unload
only exact mute module `536870916` if still present, prove repeated direct and
session-audit clearance, then compare-before-replace/fsync restore `Y:` while
preserving P0A/`R:` and all original P0E bytes. A successful execution may
publish only `p0e-recovery-published-unverified` for later James review.

James rejected two successive source candidates: first for pre-action stage
snapshot, failed-prefix, and namespace-parent binding gaps; then because a
failed source-parent fsync during pending→published publication could be hidden
by a later published→failed move. The corrected exact four-file candidate
(`r2p_p0e_recovery.py` SHA-256 `a1a854cf...bb024`) authenticates the retained
predecessor publication, repairs the exact pending parent before any failure
move, records the predecessor hash/bits/parents/repair chronology, and makes a
persistent repair failure incapable of producing a validated failed terminal.
Focused tests pass 101/101 and the combined P0E/passive/lifecycle set passes
809/809. James independently passed 101/101 and returned
`ACCEPTABLE-FOR-SOURCE-FREEZE` for the exact four hashes. The source-phase
full repository gate passes 3,444/3,444 in 2,500.62 seconds with 0 tracked-file
violations.

At the source-freeze checkpoint no live recovery action had occurred and the
recovery marker was absent. A
read-only 18:59 audit reports only unattributed PIDs 310463 and 310509, no null
sink, no open session, and `clean:false`; direct authenticated census agrees.
The original packet is current tree `53aa3b5a...a396c` solely because
`launch.stderr` is an allowed append from 11,347 to 11,706 bytes; its normalized
original tree remained `edcd8269...031`. `Y:` and the P0E stage remained exact
at `b9b26839...df44a`; `R:` remained P0A. The activation/docs commit, clean
exact-tree James ACCEPT, and fresh accounted audit were mandatory before the
single live recovery invocation and were later satisfied as recorded below.
This source boundary supplied no terrain/collision or task-role conclusion and
did not activate R2q.

The source phase is now immutable at commit
`dc2481be6479333878774dd9194cb02d9f7912f9` / tree
`ba664464977ef600076b666a204f940017a1fc88`. The exclusive freezer generated
the 2,501-byte canonical activation anchor with SHA-256
`df1def843f3d0c51f2de61c5d6f544390101de660e74e69be4405b145a103556`.
The activation/docs commit, exact clean-tree James acceptance, and fresh audit
remained prerequisites at that freeze boundary; their later disposition is
recorded below.

### 2026-08-26 P0E-R1 consumed failed recovery result

The activation/docs candidate passed the documentation-inclusive full gate
3,444/3,444 in 2,481.05 seconds with 0 tracked-file violations and committed
as `3aa9127db4312338a090ae1e096326b020b8e7f0` / tree
`1be8a4a5baef013a3f4686e1d5c20b0476c50419`. James authenticated clean Git,
the activation/source closure, 101/101 focused tests, absent recovery names,
and every action/publication boundary, then **ACCEPTED** exactly one
argument-free recovery invocation after an accounted audit. That fresh audit
contained only frozen residuals 310463/310509, no sink or open session.

The sole invocation consumed the 34-byte marker (SHA-256
`2e8a0f3a...51d94`). It exact-reauthenticated and successfully sent individual
TERM to both residuals. Both remained exact through 23 polls over the full
five-second budget, so the executor freshly reauthenticated each and sent
individual KILL. They disappeared between the first two post-KILL census
reads. The strict stability gate therefore raised `residual census was
unstable` before it could journal a post-KILL poll or prove two consecutive
absence samples. No sink unload occurred because the sink was already absent;
no `Y:` operation was reached.

The owned recovery packet moved durably to the failed namespace. Production
`validate_failure_envelope` accepts its exact 10-entry tree
`0be8f7be...43f89`, including 32-event maximal prefix `cad13b38...58056` and
both failure-publication parent fsyncs. James independently returned
**ACCEPT-AS-FAILED-EVIDENCE**. The failure snapshot records all 12 frozen
identities and the sink absent, supporting removal of the two residuals; the
post-action session audit independently reports exactly clean. This is not a
successful recovery and does not supply the missing protocol clear proof.

Original P0E remains pending at current/normalized trees
`53aa3b5a...a396c` / `edcd8269...031`; `launch.stderr` remains 11,706 bytes.
`Y:` remains on exact P0E stage `b9b26839...df44a`; `R:` remains P0A. P0E-R1
is consumed and must not retry. Any separate `Y:` restoration requires fresh
explicit authority and a new frozen/James-accepted successor. No P0E
classification, R2q execution, task-role, terrain, or collision conclusion
follows.

## 2026-08-27 P0E Y-only restoration successor banked for handoff

Fresh authority is now encoded for exactly one atomic restoration of staged
`Y:` to retail, but no restoration or mutating live action has occurred. One
preliminary James fixture unexpectedly invoked the production read-only session
audit; it performed no mutation, input, signal, or mapping action. The WIP
successor is deliberately narrower than P0E-R1: it cannot launch or control a
process, send input or signals, unload a sink, access process memory, change
`R:`, or classify/mutate earlier evidence. Success can publish only unverified
evidence for later James review.

Current hashes are `49c90537...53f3` (module), `9c9dbb28...a80` (wrapper),
`640aefb1...42bc` (activation freezer), and `92ae90bb...3a3` (tests). Focused
tests pass 96/96 and the combined P0E/P0E-R1/Y-restoration set passes 357/357.
The WIP checkpoint also passes the full repository gate at 3,540/3,540 in
2,438.22 seconds with 0 tracked-file violations.
James rejected predecessor revisions through round 26; the current revision
adds the requested cleanup repair-timestamp lower bound and controlled
single-line `OSError: ` grammar. Round 27 independently confirmed both fixes
and 357/357 combined tests, then rejected the analogous mapping-repair path:
repair provenance can be omitted despite retained `parent_fsynced=false`, and
its completion timestamp can predate the retained prefix. No activation anchor
exists and the one-shot wrapper has not run.

Runtime state is unchanged from the accepted P0E-R1 post-action record: the
last audit is clear, original P0E remains pending, `Y:` remains exact P0E stage
`b9b26839...df44a`, and `R:` remains P0A. Do not activate the wrapper until
the source/activation sequence is frozen and James accepts the exact clean
tree. See [[2026-08-27 0816 - Codex - P0E Y restoration hard-truth checkpoint]].
No R2q, task-role, terrain, or collision conclusion follows.

## 2026-08-27 P0E Y-only restoration source and activation frozen

James rounds 28 through 34 closed the round-27 mapping-repair rejection and
six further hard-truth gaps: inverse mapping provenance invention, unfinished
journal semantics and incomplete prefix chronology, contradictory nested
parent-durability state, inverse cleanup provenance invention, event-absent
cleanup ambiguity, and reversed ordering between mapping and cleanup repairs.
The accepted source requires bidirectional durable-event/provenance binding,
conservative repair of unfinished events, complete prefix chronology,
cross-bound parent durability, and ordered repair completion. A coherent
`mapping-fsync-once` fixture exercises omission and zero mutations.

Exact accepted hashes are `541fbe59...3d57` (module), unchanged
`9c9dbb28...ea80` (wrapper), unchanged `640aefb1...42bc` (activation freezer),
and `bad67fe1...e6111` (tests). The accepted source passes 98/98 focused,
359/359 combined, 741/741 broad P0E, and 3,542/3,542 full-repository tests.
James independently passed 98/98 and 741/741 and returned **ACCEPT** in round
34. Source commit `1964eec` / tree `f0afa1a` freezes those bytes.

With that source commit clean, the dedicated freezer created the 2,701-byte
activation anchor, SHA-256 `95e632dc...d8307`, binding 13 exact executed local
sources to `1964eec` / `f0afa1a`. The activation anchor is not a runtime result
or permission to act. The attempt marker remains absent and the one-shot
wrapper has not run. No emulator/game launch or control, process mutation,
input, signal, sink, process-memory, mapping, packet, R2q, terrain, or collision
action occurred. The wrapper remains barred until James accepts the exact
clean documentation-inclusive activation tree. See
[[2026-08-27 1457 - Codex - P0E Y restoration source and activation freeze]].

## 2026-08-27 P0E Y-only v1 failed; distinct recovery activation frozen

After James accepted exact clean commit `788e6fa` for one Y-only restoration,
the sole v1 invocation consumed marker `567cdf3f...14c7` and failed before any
mapping action because its retained packet inventory omitted the newly linked
owned `authority.json`. James accepted that outcome only as failed evidence.
The v1 packet remains pending with exactly one 749-byte authority receipt,
SHA-256 `b7a61db3...b599`; its published, failure, action-account, temporary,
and quarantine namespaces remain absent. `Y:` therefore remains staged and
`R:` remains P0A. The v1 wrapper is consumed and must never run again.

The user authorized a distinct one-shot mapping-only successor. Its immutable
predecessor closure binds the exact v1 marker, pending directory and authority
inode/bytes, two fresh action-parent inventories, and absence of every other
v1 terminal, version, action-account, temporary, and quarantine name. Fresh
directory descriptions replace retained-description enumeration throughout
the shared packet logic. Same-inode/same-byte post-link failures are reconciled
as owned leaves before error propagation; terminal failure durability binds
the exact lexical retained identity set and a final packet fsync after the
failure snapshot and all mapping/cleanup repairs. The recovery marker also
binds its claimed monotonic time in the fsynced marker bytes, including the
production-reachable authority-only failure state.

James adversarially rejected intermediate candidates for link-repair ledger
provenance and chronology, then accepted the exact final hashes for source
freeze. The focused suite passes 115/115. The source-phase full repository gate
passes 3,559/3,559 in 2,485.28 seconds with 0 tracked-file violations. Source
commit `32d8a839d6894ddc9b0b40fb6aebc3851449d4ca` / tree
`08ea9ade4279cb731cea7996534cf7af52aa5e9f` freezes those bytes.

From that clean commit, the dedicated freezer created the 9,270-byte recovery
activation anchor, SHA-256
`62e05bb578fcb503c934aa0af33c28d4dd4013e631fb4a3c7aa809e3c4efbe69`.
It binds 18 exact source files and the immutable v1 closure. This is inert
provenance only. `P0E-YR2-AH-001.attempted` remains absent and the recovery
wrapper has not run. The documentation-inclusive full gate, activation commit,
and James exact clean-tree acceptance remain mandatory before one recovery
action. No game, R2q, process-memory, terrain, collision, or task-role result
follows. See
[[2026-08-27 1919 - Codex - P0E Y restoration failed v1 and recovery freeze]].

## 2026-08-28 P0E YR2 consumed; recovery2 source and activation frozen

The sole YR2 invocation consumed marker `d89441a5...98dd` and stopped before
any mapping action. Its pending packet has exact four-leaf inventory
`authority.json`, `events.json`, `plan.json`, and `preserved-pre.json`; the
event journal is empty and every YR2 terminal/action/scratch name remains
absent. The invoking-session report attributes the stop to a transient strict
`pactl` read failure, while the durable packet proves only the narrower
pre-mapping stop. `Y:` remains staged, `R:` remains P0A, and YR2 must not retry.

The user then gave exact fresh reply `Corret I authorize everything, continue
on` for one atomic Y-only stage-to-retail recovery2 mapping action. YR3 binds
the complete YR1/YR2 closure and replaces forgeable exception provenance with
a cumulative bounded sink journal whose attempts retain only chronology and a
closed completed-process result or provenance-free `null`. Observation starts
and completions are bracketed at clear, action, and failure gates. James round
31 accepted the architecture for authority/source freeze; round 32 accepted
the exact authority-bearing source.

Focused restoration tests pass 162/162, broad P0E tests pass 805/805, and the
source full gate passes 3,606/3,606 in 2,457.30 seconds with 0 tracked-file
violations. Source commit `14e4a43f60eb5be4f072f06926081c4a90cc0501` /
tree `3e5536191da00dea1cd9e093ee94143b4a56d861` is frozen by the
44,957-byte activation anchor `c611240a...b2ead`, which binds 21 source files
and the exact composite predecessor closure.

This is inert provenance only. The YR3 marker, packet roots, action prefix,
temporary, and quarantine names are absent; no wrapper or mapping action has
run. The documentation-inclusive full gate, activation/docs commit, James
exact clean-tree acceptance, and a fresh accounted pre-action session audit
remain mandatory. No R2q, terrain, collision, render-grammar, or task-role
conclusion follows. See
[[2026-08-28 1155 - Codex - P0E Y restoration recovery2 activation freeze]].

## 2026-08-28 P0E YR4 restored retail Y successfully

Activation/docs/test commit `29ed6d9` / tree `4494ec8` passed clean current
activation validation. James round 42 accepted exactly one YR4 invocation
after a fresh clear audit. That audit reported zero processes, sinks, and open
sessions with `clean:true`; the sole argument-free isolated wrapper then exited
0 and published unverified success evidence.

Consumed marker `b109d6ca...c5e00` and 28-entry packet tree
`9a4979ca...e46c6` bind one entered-and-returned stage-to-retail exchange,
Y-parent durability, durable retirement of the original stage link into
quarantine, exact P0E/P0E-R1 preservation, and unchanged P0A `R:`. Two
explicit manifest validations pass exactly. The immediate post-action audit is
again exactly clear, Git is clean, and `Y:` now points to `BUGS_PC-full-disc`.

James round 43 returned `ACCEPT-AS-SUCCESS-EVIDENCE` only for that mapping
action. Runtime/input/signal/sink/process-memory counts are zero;
`terrain_collision_claim=null`; no promotion, retry, or future authority
exists. The convenience recovery3 success-validator omits keyword-only
`phase` and raises read-only `TypeError`; the executed phase-specific state
machine and explicit manifest validations pass, so James does not lower the
classification. R2q runtime still requires its own fresh explicit authority.
No terrain, collision, rendering, causality, or task-role result follows. See
[[2026-08-28 1704 - Codex - P0E Y restoration recovery3 activation freeze]].

Post-action gates required test-only phase compatibility. James round 44
required exact consumed-success bindings plus static activation validation in
the dirty pre-commit test; round 45 required recovery2 to authenticate YR4
success independently and use its committed historical closure after retail
Y. Production source remains unchanged. Recovery2/recovery3 test hashes are
`d0a28cd7...4ab7a` / `e72c7a92...a8937`; 47 recovery2, 40 recovery3, 202
combined restoration, and 845 broad P0E tests pass in the consumed state.
The final post-action full repository gate passes 3,646/3,646 in 2,531.25
seconds with 0 tracked-file violations.

## 2026-08-28 P0E recovery3 source and activation frozen

YR4 now binds the exact consumed YR3 failed state while parsing the retained
PipeWire multiline output correctly and separating authenticated historical
monotonic fields from current-boot ordering. James round 39 accepted the
corrected source after physical predecessor reauthentication and an exact
cross-binding between both copies of the YR1/YR2 history. The user's exact
fresh post-acceptance reply `i confirm this too keep going` is frozen only for
one atomic Y-only stage-to-retail recovery3 mapping action; James round 40
accepted the authority-bearing source.

The four restoration generations pass 202/202 tests, the broad P0E family
passes 845/845, and the source full gate passes 3,646/3,646 in 2,461.37 seconds
with 0 tracked-file violations. Source `9a815a3` / `27b23a` is bound by the
119,469-byte activation anchor `111fbc78...6fcb`, covering 25 exact source
files plus the full YR1/YR2/YR3 closure.

The first post-freeze targeted gate found that one unledgered test still
asserted activation absence. James round 41 rejected that activation-phase
tree and accepted only a phase-aware test correction: absent is valid before
freeze; present must bind marker absence, exact anchor SHA/source commit/tree,
canonical static validation, and stable reread. Production source and anchor
bytes remain unchanged. Corrected test `f22edde5...b94c` passes with all 202
restoration and 845 broad P0E tests.

The documentation-inclusive full gate passes 3,646/3,646 in 2,491.18 seconds
with 0 tracked-file violations.

This is inert pre-action provenance. The YR4 marker, packet roots, action
prefix, temporary, and quarantine names are absent; the wrapper has not run;
`Y:` remains staged and `R:` remains P0A. The activation/docs commit, James
exact clean-tree acceptance, and fresh clear session audit remain mandatory.
No R2q, terrain, collision, render-grammar, material, visibility, causality,
or task-role conclusion follows. See
[[2026-08-28 1704 - Codex - P0E Y restoration recovery3 activation freeze]].

## 2026-08-28 P0E YR3 consumed before mapping; recovery3 required

Activation/docs commit `1bc9bcd535ed1c9b5d718db290cf62412490999f` /
tree `e0d90708875429f3d8596aa6dd392a2acae3d31f` passed the 3,606-test
documentation-inclusive gate. After James round-33 exact-tree acceptance and
an exactly clear pre-action session audit, the sole YR3 invocation exited 2
before mapping. Its 108-byte marker is `7191e193...e43`; its 58-byte pending
placeholder is `0c0a027d...f152`; and its 11-entry failed-unverified tree is
`69daa4a7...0589`. Events are exactly empty, the reducer is idle,
`mapping_replaced=false`, `y_parent_fsynced=false`, and all YR3 action,
temporary, and quarantine names are absent. `Y:` is still staged, `R:` is
still P0A, and the immediate post-action session audit is exactly clear.

The retained PipeWire `pactl` output is return-code-zero but multiline; the
classifier wrongly treats continuation lines as independent short-list rows.
The production failure validator also mixes historical predecessor monotonic
timestamps from an earlier boot into current-attempt ordering, producing lower
bound `118593490774571` above current fsync/failure times near
`15783718417xxx`. James round 34 returned `ACCEPT-AS-FAILED-EVIDENCE`: the
packet proves only a consumed pre-action failure and is not a valid terminal
envelope. YR3 must never retry. A distinct recovery3 successor must bind the
immutable failed state, correct both defects under adversarial fixtures, pass
the full freeze/acceptance sequence, and obtain fresh authority. No R2q,
terrain, collision, render-grammar, or task-role conclusion follows. See
[[2026-08-28 1155 - Codex - P0E Y restoration recovery2 activation freeze]].

## 2026-08-30 R2q hard-truth source and activation freeze through `-022`

The banked round-91 candidate was restored without dropping stash object
`76db1c9ee1ffffce52cea6aee591c24ab6a1c39a`. It closes James's round-90
file-fsync provenance rejection by authenticating full-frame pre/post SHA-256,
size, mtime/ctime, and timing around fsync; the corruption→fsync→restore-without-
fsync discriminator now rejects. James round 91 accepted the exact source,
frozen at `eececd7`; rounds 92 and 94 then accepted the fresh benchmark-007
source chain and corrected benchmark continuity inputs (`40bee21`, `ec46c9a`).

Benchmark `-007` accepted at 4,562 bytes / `69c64794...27d07`, and immutable
offline `quiet-census-design-021` was published at 3,515,140 bytes /
`5891e93f...13fac`. The first activation-phase full gate then exposed only
stale test/environment assumptions: the restored retail `Y:` inode is
`9343702`, the current namespace is not `-020`, the link-receipt contract was
renamed, published fixtures require the predecessor closure, and mapping
projection fixtures must carry the journaled restore transition. It reported
3,764 passed, 9 failed, and 13 setup errors; no production runtime action was
involved.

Because the corrected design test and runtime module are benchmarked source,
`-021` remains immutable and is now exact predecessor evidence. James round 96
accepted the successor source; commit `3998111bb08e72dd1ddbc32a4c1c735c0f500f11`
/ tree `0c61a8556dbcded344d7b28c5e9149b23fb2c247` advances every prospective
runtime namespace to fresh `-022` and benchmark ledger `-008`. Benchmark
`-008` is 4,562 bytes / `eb930b77...9cfd9`; its final 1,363-byte anchor is
`1049049c...b7a1`, source ledger `6f0c6ac2...37a9`, and worst control /
comparison totals are 25.740025121 / 80.520710670 seconds, leaving
99.479289330 seconds below 180 seconds.

Fresh immutable `quiet-census-design-022/design.json` is 8,061,582 canonical
bytes / `b79f63b004596aea8f0e32def0f76a602502ef9d5902f72b41b47f383f8e6b72`.
It embeds every byte of `-021`, separately retains the failed-runtime `-020`
operator/physical closure, and validates with outcome
`offline-r2q-design-frozen-runtime-unauthorized`. The formerly failing 11-node
tranche passes, runtime/freezer tests pass 157/157, and the full repository gate
passes 3,786/3,786 in 3,276.94 seconds with zero tracked-file violations.

No game, restoration wrapper, R2q wrapper, live R2q `/proc` census, ptrace,
process-memory, input, signal, screenshot, save-state, stage-mapping, or
terrain/collision action occurred. Retail `Y:` and P0A `R:` remain the last
accepted runtime facts. `-022` is an offline activation only and still requires separate fresh
explicit runtime authority. KU-079, KU-080, and KU-081 remain open. See
[[2026-08-30 1519 - Codex - R2q hard-truth source and activation freeze]].

## 2026-08-30 R2q-022 failed run preserved; Y mapping recovered

The sole activated R2q-022 D1 attempt is consumed failed evidence and must not
retry. It stopped during launch identity stabilization after repeated launcher
`/proc/<pid>/maps` reads drifted; every quiet-census, debugger-seize,
completed-present acquisition, and scientific comparison phase was skipped.
The retained failed closure binds design `b79f63b0...e6b72`, lock/fallback
`18cc4341...9de5`, journal tree `6fcc1fb1...d9a9`, pending tree
`65988790...894`, emergency cleanup `21c52e9b...aabd`, exact absent/reused
process identities, staged D1 tree `1a25a4a7...3ae3`, and retail tree
`78b0a30c...a210`. The cleanup account's wrong expected-retail-Y assumption
was handled only through separately James-accepted identity-guarded cleanup;
it does not validate the original runtime arm.

The retained D1 `Y:` stage was then restored by a distinct, exactly-once,
mapping-only protocol. James accepted source after rounds 101-105; source
`70b9ba0` / `1dd5518` is bound by activation2 SHA-256
`5648ff8c55cc728273da0ee1f69939b82de1b7a19f062038e35ae5ab0be6471d`
committed at `e457a00`. Frozen authority receipt `d0630d6e...d736` binds the
exact short reply to that activation. James accepted the clean activation and
authorized one invocation; the wrapper ran exactly once and will not run
again.

Published-unverified recovery packet `R2Q-022-YR1-AH-001` has 28 entries and
tree `f3cf883f83bc386dd4474dcdef732b7744a3738f86e4c6df2c8e7a4b215a5824`.
Its mapping receipt `96baab75...cc2c5b` records one exchange, zero rollbacks,
parent fsync, stable reread, D1 inode `9458103` before, retail inode `9525237`
after, and durable quarantine of the D1 link. P0A `R:` remains inode
`9054047`; all runtime/input/signal/sink/process-memory counts are zero;
`terrain_collision_claim` is null. Pre/post audits are clear. James round 111
returned `ACCEPT EVIDENCE`.

The standalone convenience validator supplies a placeholder authority string
and is defective, but production executed and validated under the exact
receipt-derived authority. Preserve the activated production source. The
documented read-only procedure loads activation2 and the frozen authority,
derives the exact reply, configures the inherited validator with that reply,
and validates the manifest; this passes. James accepted a test-only
post-action phase correction after a full gate exposed hard-coded historical
YR4 inode assumptions: 112 focused tests pass, and the three changed tests are
outside activation2's 31-file source ledger. The final full repository gate
passes 3,811/3,811 in 3,270.71 seconds with zero tracked-file violations.

This is environment recovery only. R2q-022 remains failed and consumed; it
produced no accepted runtime census, task role, render grammar, terrain,
collision, material, visibility, causality, or no-effect result. KU-079,
KU-080, and KU-081 remain open. See
[[2026-08-30 2221 - Codex - R2q-022 failed-run mapping recovery]].

## 2026-08-31 R2q `-024` offline activation frozen

The next source-hardening pass preserved immutable `-023` rather than
overwriting it. Source `fbba31f` / tree `480abf0`, benchmark-009
`95478c34...9a38b`, and 12,035,411-byte design-023
`be7cf41f...08cd3c` are exact predecessor evidence. Its activation suite
exposed stale mapping-authority projections and a real maximum-shape packet
above the old 256 MiB raw fallback ceiling; no runtime action occurred.

Fresh `-024` corrects the restore authority and D2-continuity fixtures, keeps
historical public namespace aliases exactly `-022`, binds all historical
`-023` names absent, advances every prospective name to `-024`, and ratchets
one-shot frame protocol v6 to a 320 MiB raw ceiling while retaining the 128 MiB
stored-data reservation. James accepted exact staged diff `86b737d4...e8976`
for source freeze after independently validating source identities,
predecessor closure, namespace absence, projection authority, and capacity.
Source commit `022f739bbca7b83146b57e45a81a9f2bb2b63e3c` / tree
`9d786514a9bdb552f8c2def0816a0bf964462710` freezes those bytes.

Benchmark-010 is 4,563 bytes / `592ac4a7...d3e7`; final 1,363-byte anchor is
`10264047...fb7`; worst control/comparison totals are 23.341496257 /
79.652494057 seconds, leaving 100.347505943 seconds below 180 seconds. Fresh
immutable `quiet-census-design-024/design.json` is 17,336,651 canonical bytes /
`321eb8c6681e88c19ab43aa04cc35179897ac0f89dfb48602ab01a7180ec2288`
and validates as `offline-r2q-design-frozen-runtime-unauthorized`. Runtime
tests pass 160/160; full `make check` passes 3,843/3,843 in 4,000.96 seconds
with zero tracked-file violations.

No game, restoration wrapper, R2q wrapper, live census, ptrace,
process-memory, input, signal, screenshot, save-state, or mapping action ran.
Retail `Y:` and P0A `R:` remain the last accepted runtime facts. There is no
new terrain/collision or task-role result; KU-079, KU-080, and KU-081 remain
open. Activation/docs commit `621e2c1` completed, but James rejected its stale
pre-final-anchor capacity figures and gate wording. Docs-only commit `db3aff4`
completed that correction. This paragraph records the historical freeze; the
later consumed failure, mapping recovery, and fresh successor are recorded
immediately below. See
[[2026-08-31 0648 - Codex - R2q 024 hard-truth activation freeze]].

## 2026-08-31 R2q-024 consumed; mapping recovered; `-025` frozen offline

The sole R2q-024 D1 arm is consumed failed evidence and must not retry. It
failed in `stage-and-launch` with exact receipt message `R2q process maps read
binding mismatch`; the title/gameplay gate, quiet census, debugger acquisition,
and scientific comparison never completed. A separately authorized,
identity-guarded cleanup cleared the matching residuals. The distinct
mapping-only recovery then ran exactly once under activation
`f735879235faa2f7de11807b39eeea85ab61e554e9e04310c8850b7965d11dcc`,
source `a53291bc62d92044bedd8c3e6fbfcd1980ea6cb9` / tree
`f99b91a579556f0083c7306a1061cfa5777bb628`, and activation commit
`45c286af15f3362e72ecd1868a91b3b9355417e1`.

James accepted the recovery as mapping evidence only. Its stable 28-entry
packet tree is
`afacab0a705802e2a214b44ccf8ec5d955c007eb7a7fe04ff1c174a55e790bfa`;
result SHA-256 is
`14e29a9e4bc5d47ff305c33eb5aa402e94ec47a12639d45b6beffb8693c128a9`;
and mapping receipt SHA-256 is
`ed20963a2e64970320b225369caba99f622c983c82829f290f97fe87124eb033`.
It records one exchange, zero rollbacks, parent fsync, stable reread, retired
D1 inode `9731469`, current retail-Y inode `9733762`, and unchanged P0A-R inode
`9054047`. All runtime, input, signal, sink, and process-memory counts are zero;
`terrain_collision_claim` is null.

The fresh offline successor preserves the complete failed-024/recovery-024
closure. Measured maximum valid failure-material and continuity accounts are
379,306,355 / 153,758,493 and 428,420,338 / 166,728,453 raw/compressed bytes,
respectively. Protocol `ablpc-r2q-one-shot-authority-v7` therefore raises the
raw ceiling to 448 MiB and the stored-data reservation to 192 MiB, deriving an
exact 201,330,816-byte frame. James accepted source patch
`c0114ada12fe779d95a66f88f703bf8b120699103f6c2f019570d3c8adc7fd3c`;
source is frozen at `d23ece3ce10231c29290d37f6272acfeeffa46f0` /
tree `8492bcb29eb0cf6b6406baa0266e9860696a1ae3`.

Benchmark-011 is 4,568 bytes /
`9ec2ec6aa5333443ce0b0a9252dd609ea6e443678478281345d5488738992d79`;
its final 1,364-byte anchor is
`9997ac75bf6f264ac6e9b8f23c89edcde85acb332f5693aa04fecf1abb7ee588`.
Worst control/comparison totals are 37.446760533 / 128.966455183 seconds,
leaving 51.033544817 seconds below 180 seconds. Fresh immutable
`quiet-census-design-025/design.json` is 25,557,671 canonical bytes /
`d25acc8ceb90a5166130788e1b5b95e5d8fe124e0d3f71188ae9def7b44934a9`;
its canonical predecessor closure is 24,558,434 bytes /
`c71147ff568b4e6efd03cfa436f0664d6a81012b3e44e55ffc33a69bb298884e`,
and activation source manifest is 5,966 bytes /
`6bfe57476c0f4c5b1b648a9af60fad193dc08836ccbf10b0d9a0c4d8028a2451`.
Published validation passes with outcome
`offline-r2q-design-frozen-runtime-unauthorized`.

The first full gate exposed only stale historical YR2/YR3 test assumptions
about the accepted current retail-Y inode: 3,864 passed, one failed, and 13
setup errors. James accepted the bounded two-test correction at diff
`b4910678336b36a3a75ea4663c2871fb8db5d1796d203c53e241ff7328687d4a`;
48 affected local tests and his independent 87-test tranche pass. A second
full run was invalidated by `Errno 122` after old completed pytest scratch was
left in `/tmp`; its 3,658 passed / 178 failed / 42 errors are environment
failure, not a source verdict. After removing only completed scratch, the
unchanged clean run passes 3,878/3,878 in 6,571.36 seconds with zero tracked-
file violations.

No game or R2q wrapper ran while producing `-025`. The freeze supplies no
accepted quiet census, task-role, render-grammar, terrain, collision, material,
visibility, causality, no-effect, or retail-executable result. KU-079, KU-080,
and KU-081 remain open; any R2q-025 runtime requires a distinct fresh explicit
authorization after the final clean-tree audit. See
[[2026-08-31 1849 - Codex - R2q 025 activation freeze]].

## 2026-09-01 R2q-025 consumed; retail mapping recovered

The sole R2q-025 D1 arm is consumed failed evidence and must never retry. It
failed closed in `stage-and-launch` because the bounded game-process maps did
not converge. The retained 118,724,996-byte terminal packet is
`d1a337530fed514274e3e6dba8f8e76d3becdd91c6360a5e551a5c27f8bffa04`;
its exact failure says `ProcessMapConvergenceError`, records the failed normal
close/audit cleanup, and remains pending. No quiet census, debugger capture,
stopped memory range, screenshot batch, D2 comparison, or terrain/collision
science completed.

The separately authorized identity-guarded cleanup matched only the seven
frozen PID/start-tick identities. TERM cleared four; KILL cleared matching
survivors `1392949`, `1393099`, and `1393142`; PulseAudio module `536870916`
was already absent. The audit was then exactly clear. This cleanup does not
repair or validate the consumed R2q arm.

James accepted the distinct mapping-only recovery source at
`3ac52dc1036566be92db6cab28a1c43db3d38328` / tree
`675d5b198e076c5668ce542ff4c4cad96b64ba0a`. Activation
`5ff648a2a5e8a66d4aa87c1fc177d4e2f378aee0120d1928a07997755da42e90`
and authority receipt `e9e1710aa331ba823922dca3ca9ce2f861961441f5e728012d5ebf7c73ddd922`
bound the exact user reply. The recovery wrapper ran exactly once and must
never run again. Attempt marker `870a6eab...c68` and 28-entry packet tree
`0b0aa4113289df6a8f2e2922b4b833bc10408e819d3889c3c02b79fe94ff4d2b`
authenticate one exchange, zero rollback, parent fsync, stable reread, retail
Y inode `9773754`, retired D1 inode `9770116`, and unchanged P0A R inode
`9054047`. Mapping receipt `f37158da...c383` and result `243f8966...22a4`
record zero runtime/input/signal/sink/process-memory action and
`terrain_collision_claim:null`. James returned `ACCEPT EVIDENCE`.

The benchmark-011 test source remains byte-exact at `c556df93...5155`.
Post-action tests authenticate the new mapping phase without modifying that
activated benchmark source or intercepting its current-state validator.
Checkpoint `c851110` / tree `9c2a495` received James `ACCEPT`; the unmodified
strict success validator passes on that clean tree. Final full `make check`
passes 3,905/3,905 in 6,213.97 seconds with zero tracked-file violations, and
the final session audit is clear.

This is environment recovery only. KU-079, KU-080, and KU-081 remain open.
The next terrain/collision step requires a fresh offline successor (nominally
R2q-026) that preserves the complete failed-025/recovery-025 closure and
addresses the process-map convergence blocker before any separately authorized
runtime. See
[[2026-09-01 0317 - Codex - R2q 025 failed-run mapping recovery]].

## 2026-09-01 R2q `-026` offline activation frozen

Fresh `-026` preserves the complete failed-025 and mapping-recovery-025
closure. It replaces the ineffective eight-times-50 ms process-map loop with
protocol `ablpc-r2q-process-maps-convergence-v2`: at most eight retained
three-read cohorts, a frozen 625 ms stability interval, the same 5-second
absolute deadline, and nonconvergence valid only after the real deadline has
elapsed. The exact `-025` failure trace completed in only 417,319,810 ns and is
now rejected rather than accepted as durable nonconvergence.

The enlarged v4 predecessor closure is 36,241,115 canonical bytes /
`f3e777b25d3366e2e02eac467d891b2a8490d9777fb3427cd49d2f2f6c928d2e`.
Finalized maximum-shape tests prove both nested accounts exceed the old 448 MiB
raw limit, the larger exceeds 512 MiB, compressed payloads exceed the old
192 MiB reservation, and all valid forms fit fresh protocol v8's 640 MiB raw /
256 MiB stored bounds. The derived one-shot frame is 268,439,680 bytes.

James accepted the source and the later bounded historical-test correction.
Source is frozen at `812b6d055d1c5680c29a985444aca432ed2a5f62` / tree
`37353bf86f4097264d2c0f78b7a05d6f18d82fee`. Benchmark-012 is 4,563 bytes /
`afc246e8a8ea47446f78d05c44816dce7d875ff64f42663b845739bf9ad75ae3`;
its final 1,364-byte anchor is
`408812ebd234972d2079d0a2cf9911d6f3f06f855bcf61a741840e03f8183638`.
Worst control/comparison totals are 23.367732980 / 80.813913839 seconds,
leaving 99.186086161 seconds below 180 seconds. Immutable
`quiet-census-design-026/design.json` is 37,673,716 bytes /
`a7eb768b962b795c4c73ba9d09e35219b30238ed79ee3cf60a1ae8b92ff52d7b`;
its 5,966-byte activation manifest is
`a1f56b67ae0de62565500193a927e504963582528390c0c25edd5fb5a20dbe8d`.
Published validation returns `offline-r2q-design-frozen-runtime-unauthorized`.

The finalized design and runtime suites pass 350/350 and 160/160. The first
full gate reached 3,122 passes before one historical consumed-R2q-025 manifest
test recaptured predecessor state through the active `-026` namespace. James
accepted a test-only exact-activation projection that leaves the production
validator strict. The complete rerun passes 3,908/3,908 in 4,632.89 seconds
with zero tracked-file violations.

No game, R2q wrapper, restoration wrapper, live `/proc` census, ptrace,
process-memory, input, signal, screenshot, save-state, or mapping action ran.
At that offline freeze boundary R2q-026 was unconsumed and had no runtime
authority. KU-079, KU-080, and KU-081 remained open, and no terrain/collision
or task-role conclusion followed. The next historical gate was the clean
documentation-inclusive activation commit and James's exact clean-tree
verdict. See
[[2026-09-01 1524 - Codex - R2q 026 convergence and activation freeze]].

## 2026-09-01 R2q-026 consumed; cross-namespace failure; mapping recovered

The sole R2q-026 D1 arm is consumed failed evidence and must never retry. It
passed the corrected five-second process-map convergence loop, but failed in
`stage-and-launch` before the title/navigation gate because executable
provenance compared `/proc/<pid>/maps` device `00:24` (major/minor `0/36` in
the process mount namespace) with host `stat()` device minor `38`. The mapped
preloader path, inode, and SHA-256 were otherwise exact. The 170,486,748-byte
terminal packet is
`741fbd362c9c2f5d15c842e2b5deb34bedc6cf73d271e8f14b7df59429c2b14e`.
No quiet census, debugger capture, stopped memory range, screenshot batch, D2
comparison, or terrain/collision science completed.

The separately authorized identity-guarded cleanup matched only the seven
frozen PID/start-tick identities. TERM cleared four; KILL cleared matching
survivors `1801271`, `1801424`, and `1801463`. PulseAudio module `536870916`
was already absent, and the final audit was exactly clean. James accepted the
cleanup, failed-evidence classification, and mount-namespace root cause.

James then accepted distinct mapping-only recovery source
`9cf28fa81b27a41e2ce595e38141e2ac0ae885b1` / tree
`746e9d447a5aed712a6a927f461fe83eac418f0b`. Activation
`16bbcfcc45ad0bde13ad3058963d073fd26a50492f3a59ebecd89d745eced1de`
and authority receipt
`d1150b39fd776bf676c2c6dd6f19e00b0dc56a0545663b4e16765229b1de4cfe`
bound the exact user reply. The recovery wrapper ran exactly once and must
never run again. Marker `9864c643...d0b3` and 28-entry packet tree
`264ecdacb4c0168f1edd3dadd29eddb5ffcee062a880f705db970b31ebc2780c`
authenticate one exchange, zero rollback, parent fsync, stable reread, retail
Y inode `9998033`, retired D1 inode `9997058`, and unchanged P0A R inode
`9054047`. Mapping receipt `be0a3633...80c4` and result
`d81c6f2b...c142` record zero runtime/input/signal/sink/process-memory action
and `terrain_collision_claim:null`. James returned
`ACCEPT R2Q-026 RECOVERY EVIDENCE`.

Post-action historical adapters exact-gate that mapping, retired link, packet,
receipt, and frozen predecessor phase while preserving all source/blob/
activation checks. Focused recovery coverage passes 143/143; complete
`make check` passes 3,937/3,937 in 4,792.33 seconds with zero tracked-file
violations. James accepted the final adapter. This remains failed pre-science
evidence plus environment recovery. KU-079, KU-080, and KU-081 are still open.
The next successor must use fresh identities and compare executable mapping
provenance within one namespace (or avoid treating namespace-local device
numbers as host-global identity) before any separately authorized runtime. See
[[2026-09-01 1718 - Codex - R2q 026 failed-run mapping recovery]].

## 2026-09-02 R2q-027 rejected at finalization; R2q-028 frozen offline

R2q-027 corrected the cross-mount-namespace executable-provenance defect by
hashing and statting the executable through the retained process root, then
comparing `/proc/<pid>/maps` device/inode identity only with that same process-
namespace result. James accepted source commit
`ee6c6084897ee08565eb074fcbbfd682215c42e8` / tree
`3815f9413b5f6e5e07b83b347f11c823cdfeef53`, benchmark-013
`0559c257...a6524`, and immutable 54,983,457-byte design-027
`499e5fda...f211`. James also returned `ACCEPT R2Q-027 ACTIVATION`.

The post-activation design/runtime suite then exposed two genuine stale
anchored tests: a mapping fixture still required `retail-026`/`D2-AH-026`,
and a failed-025 regression did not admit the current v3 `field set mismatch`
rejection. The same run's other 28 failures were a 15 GiB pytest scratch quota
cascade. The exact 1,588-byte rejection receipt is
`8375369c...4fb`; James returned `REJECT R2Q-027 FINALIZATION`. The design is
preserved as immutable offline predecessor evidence and was never run.

Fresh R2q-028 corrects those tests, advances all active prospective names to
`-028`, and rejects appearance of all 28 never-used `-027` runtime/publication
paths. It binds design-027 plus its finalization rejection in predecessor
closure v6, and raises the measured maximum-shape one-shot bounds to protocol
v10: 1,280 MiB raw and 576 MiB stored. James accepted source commit
`68e0714f8f1e8bac6ed4c106ce32c6db8c3aa2ee` / tree
`cda3886ef3194043e7982784c24a4db8bc8e402d`. Benchmark-014 is 4,563 bytes /
`83cf0963...d05e`; final anchor-014 is 1,364 bytes /
`00466897...756`; its 81.894036244-second maximum leaves 98.105963756 seconds
below the 180-second ceiling. Immutable design-028 is 78,066,492 bytes /
`c5840fe9...e087`, activation manifest `fb3e8292...5fa8`, and validates as
`offline-r2q-design-frozen-runtime-unauthorized`. James returned
`ACCEPT R2Q-028 ACTIVATION`.

The complete post-activation repository gate passes 3,972/3,972 in 6,102.42
seconds with zero tracked-file violations. Its scratch was isolated under
`/dev/shm` and removed after completion. Pre/post session audits are exactly
clear. No game, restoration wrapper, R2q wrapper, live census, ptrace,
process-memory, signal, input, screenshot, save-state, or mapping action ran.
KU-079, KU-080, and KU-081 remain open. The documentation-inclusive activation
commit completed at `1aa45392ae87dcfc90f5630e25e992d75b05f976` / tree
`8c308ba77982ac1b53214c6c765801b86a1277e4`. James rejected that clean tree
only because these notes still described the completed commit as future work;
all artifact, validator, closure, capacity, stash, cleanliness, and session-
audit checks otherwise passed. This bounded docs-only correction leaves only
James's exact clean-tree re-audit. See
[[2026-09-02 0056 - Codex - R2q 027 rejection and 028 activation freeze]].

## 2026-09-04 R2q-028 pre-lock rejection through R2q-032 bank

The authorized R2q-028 wrapper invocation stopped at its read-only activation
edge because a host remount changed only historical device-number fields. It
did not reach the one-shot lock or any launch, mapping, process-memory, input,
signal, screenshot, or scientific action. The exact 2,022-byte pre-lock
receipt is `322cb1b1...5cb`; James accepted that bounded disposition.

R2q-029 introduced raw-retaining device projection and was accepted through
activation, but its full gate exposed historical recovery tests that still
equated frozen device 54 with current device 51. Immutable design-029 is
108,849,231 bytes / `6cd3d734...3da0`; its 1,636-byte finalization rejection is
`694d0f7f...7f20`. R2q-030 added a remount-stable historical adapter and
received source acceptance, but its sole freezer invocation rejected before
publication because it changed historical design-029 bytes. No design-030
exists; the 1,699-byte activation rejection is `440a7e9b...2403`.

R2q-031 corrected active-design dispatch without rewriting historical bytes.
James accepted source `5f5b25e` / tree `2ce6bce`, benchmark-017
`1c5688dd...ef04`, and activation. Immutable design-031 is 149,901,603 bytes /
`7d826b13...c554`. Its complete full gate reported 4,071 passed, one failed,
and two errors: stale `-030` mapping suffixes and an overbroad mocked
`os.fstat` that broke Python 3.14 teardown. The exact 2,763-byte finalization
rejection is `f4481e28...aa2`; R2q-031 remains immutable and unrun.

R2q-032 corrects those two defects, advances the active namespace, preserves
all historical artifacts, and binds the unused R2q-031 paths absent. James
accepted source `45ae9539d200786064309ffb9a249e526de0897d` / tree
`2292c1a419212fe7f14c3b846e939c690ee830d5`. Benchmark-018 is 5,023 bytes /
`c93ea507...7bb9`; final anchor-018 is 1,730 bytes / `d6951e11...ab70`.
Immutable design-032 is 204,641,846 bytes /
`0604d37daab86378a730724e54a2bc7ddcc07dbbbd8461db81000cf498e1b2b8`,
with 6,332-byte activation manifest `d3dc03ae...f402`. James returned
`ACCEPT R2Q-032 SOURCE` and `ACCEPT R2Q-032 ACTIVATION`; activation commit is
`b6abcb2b547d2b59288af6327711dcfc1cbb0f06` / tree
`e65362de1d30b3ab1f510ba8da02a07e099802ea`.

Final focused evidence passes: runtime/freezer 163/163,
predecessor/one-shot/continuity 124/124, post-anchor 17/17, and the exact
capacity case 1/1. The final maximum-shape accounts are 2,689,803,574 and
3,095,391,713 raw bytes plus 1,245,497,694 and 1,422,137,007 zlib9 bytes;
the 3,072 MiB raw and 1,472 MiB stored limits retain positive margins.

The final full `make check` attempt is **incomplete, not accepted**. It reached
79%, displayed one failure marker, and was interrupted before pytest emitted a
terminal summary or traceback. No final pass/fail classification may be
inferred. Its scratch is absent and the closing session audit is exact-clean.
R2q-032 therefore has accepted source and activation but no final clean-tree
James acceptance. KU-079, KU-080, and KU-081 remain open; no game, wrapper,
live census, ptrace, process-memory, input, signal, screenshot, save-state,
mapping action, or terrain/collision observation occurred in this offline
sequence. See
[[2026-09-04 1711 - Codex - R2q 032 activation bank and incomplete final gate]].

## 2026-09-06: EXP-009 bounded offline crossing acceptance; runtime next

[[EXP-20260905-009 - Additive terrain preservation and access ramp]] passes the final 224/224 terrain gate (26.40 seconds), native preservation/loader/DAT relocation/command traversal, box/landing/step-off/fall checks and four separately declared continuous-crossing/return routes. Three deck lanes and the restored-landing route cross onto original cell 44140 and return without resets. The old exact-point targets still fail: native controls isolate adaptive slowdown against fixed downward input on that original slope, not missing collision. Those failures remain preserved, rather than being relabelled as passes. The fresh copy at `work/copies/EXP-20260905-009/game/PC/BUGS` is ready for controlled runtime comparison; rendering/visibility/overlap and full actor behavior remain unaccepted. See `reports/terrain/EXP-20260905-009-validation.json`. No live action, R2q/full suite or Git operation.

### EXP-009 runtime startup, after the offline checkpoint above

One user-authorized isolated auto-hardware launch passed the clean pre-audit, staged hashes, both R: log identities and six hardware markers. It reached Start LevelSelect, but discovery stopped on a title mismatch: owned window 14680071 is `Loading - A Bugs Life` (640x480), not the required `Bugs`. No menu input or Level01 confirmation occurred. Preserve game `23853/183505` in group 23606 on `:2`; do not relaunch. Pending title-guard correction approval is the immediate next step. The seven processes/sink reported by the non-clean postlaunch audit are explicitly accounted for in `reports/terrain/EXP-20260905-009-runtime.json`. No terrain runtime acceptance yet.

### EXP-009 runtime entry completed (2026-09-06 continuation)

The preceding title-guard stop is resolved with explicit user approval, restricted to PID 23853/start 183505. The same session is now in Level01 at the original start and remains open for user playtesting. Normal menu input only; read-only RAM confirms level 1, complete resident source-99/source-100 payload equality and mesh streams 128/160/213/280. Original-start contact maps to source-99 cell 47716. No live movement acceptance is claimed. Next: original-ground preservation, connector crossing/return, deck-edge landing and box checks. Evidence: `reports/terrain/EXP-20260905-009-runtime-entry.json` and [[2026-09-06 - Codex - Additive runtime startup]]. No R2q/full suite, memory writes, relaunch or Git operations in this continuation.

### EXP-009 ramp playtest: collision report positive, visibility defect open (2026-09-06)

The user reports the requested ramp crossings work without falling through or sideways sliding. Agent read-only sampling confirms appended-ramp cell 49008 remains the recorded contact while a camera turn makes the ramp disappear/reappear at a fixed post-tap actor position. This is not a missing-collision observation. Live visual acceptance is blocked pending discrimination among mesh/bounds culling, face/clipping rejection and draw ordering/overlap. No cause selected and no asset edit made. Evidence: `reports/terrain/EXP-20260905-009-ramp-visibility.json`; [[2026-09-06 - Codex - Ramp visibility reproduction]]. Same game session left open. No tests or R2q/full suite.

### EXP-009 renderer diagnosis narrowed (2026-09-06)

Original-instruction offline replay rejects mesh 160 at whole-mesh horizontal cull `0x0044D677` for two hidden camera poses with inherited centre `(4243,-570,16018)` and radius 6047. An offline radius-only 8192 arm passes all five sampled cameras. One intermediate visually unclear sample already passes at 6047, so this is not a complete live fix or explanation of flashing. Evidence: `reports/terrain/EXP-20260905-009-ramp-culling.json`; [[2026-09-06 - Codex - Ramp culling discriminator]]. Next: obtain exact approval for a reversible live radius-only comparison at `0x0064CA47`, 6047 -> 8192 -> 6047. No live writes, asset edits or tests yet; same session open.

### EXP-009 live radius discriminator accepted at one pose (2026-09-06)

Fresh exact authorization was obtained and the two-byte `6047 -> 8192 -> 6047` scene-radius A/B/A completed in the existing session. Two candidate captures show the ramp surface; both initial and both restored controls lack it, with identical actor position, camera and appended-ramp contact. This confirms a causal mesh-bound/culling contribution at this pose, not a general 8192 repair or an all-angle result. Original radius restored; asset files unchanged. Next: PC-compatible bounds/partitioning design, offline regressions and a file-loaded camera comparison. Evidence: `reports/terrain/EXP-20260905-009-ramp-radius-live.json`; [[2026-09-06 - Codex - Live ramp radius comparison]]. No tests or full/R2q suite. Exact write authorization is consumed.

### EXP-20260906-001 file visibility correction ready; runtime switch pending

[[EXP-20260906-001 - PC-compatible ramp visibility bounds]] changes only the scene bound from6047 to computed8560 in a new isolated copy; EXP-009 collision, geometry and failing copy are preserved. Future additive builds use the PC view-plane-aware bound. Affected tests73/73 (.33s), exact terrain gate72/72 (26.17s); native finite sweep0 candidate rejections versus544 control rejections across5152 relevant cameras, plus5/5 historical poses. No full/R2q suite or Git. Evidence: `reports/terrain/EXP-20260906-001-validation.json`.

Runtime remains **unlaunched**: old owned PID23853/start183505 did not exit via normal input/window close. Scoped termination approval is needed before replacement; same seven owned-but-generic-ledger-unattributed processes/sink remain. New prefix not created, no new RAM writes. Next: approved cleanup/audit, fresh hardware file load, resident-bound confirmation and live camera-angle test.

### EXP-20260906-001 now file-loaded in Level01 (2026-09-06 continuation)

Scoped old-session cleanup was approved/completed; post-cleanup and prelaunch audits clean. One fresh hardware launch entered Level01; read-only RAM confirms file-loaded bound8560 and exact retained collision/mesh streams. Game32550/start646434/group32301 is intentionally open **at the original start, not the ramp**, for user downhill/turn/side-angle checks. No new RAM writes/teleport or test reruns. Fresh camera-angle acceptance remains pending. Evidence: `reports/terrain/EXP-20260906-001-runtime.json`; 2026-09-06 - Codex - Corrected ramp build runtime handoff. Earlier cleanup blocker is resolved.

## 2026-09-06 EXP-003 solid sides staged, test-fixture correction pending

[[EXP-20260906-003 - Solid ramp sides and ground contour trim]] adds20 matching
wall cells and clips the new side faces to selected original ground contours,
retaining original floor/top geometry and bound8560. Native blocking, landing,
step-off/return, command traversal and relocation checks pass. One fixed-axis
western return fails identically in the unchanged control; a separately declared
steered three-lane up/down/up test passes9/9. Do not relabel the old failure.
137 affected tests pass with1 new synthetic-fixture winding error; correction
approval was requested and remains pending. The terrain gate passes72/72.
EXP-002 remains user-paused and untouched. EXP-003 game/prefix are staged but
unlaunched; after the test-only correction and affected pass, perform the user's
requested audited switch. No R2q/full suite, Git or live writes. Ground-trim
appearance remains a hypothesis awaiting preview. Evidence:
`reports/terrain/EXP-20260906-003-validation.json`.
<!-- preserved-body:end -->
