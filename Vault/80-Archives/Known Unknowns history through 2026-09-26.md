---
type: archive
status: historical
created: 2026-09-26
tags: [archive/project-review]
---

# Known Unknowns history through 2026-09-26

Historical snapshot of [[Known Unknowns]] before the September 26 review. The body
below is preserved, including superseded claims, old process IDs and
consumed permissions. It is evidence of earlier notes, **not a current work
queue or runtime binding**. Use [[Current State#Current task handoff]] and
[[Environment Status#Current runtime handoff]] for current instructions.
2026-09-26 - Codex - Project review and Vault cleanup records the review.

<!-- preserved-body:start -->

## 2026-09-20: compressed storage and cleanup yield

Follow-up 2026-09-20 - Codex - Remove old generated game builds removes122 old builds and observes227.848 MiB more filesystem availability;54.42 GiB of summed build size was largely shared. Exact isolated physical reclaim remains unmeasured. Earlier inspection below predates deletion.

2026-09-20 - Codex - Directory space audit confirms extensive Btrfs sharing and only2.171 GiB raster images under work. Whole-tree FIEMAP accounts21.33 GiB exclusive plus5.14 GiB set-shared, versus867.92 GiB ordinary du. Exact compressed physical usage and cleanup yield remain unknown because compsize requires unavailable privileges. Two named temporary candidates account2.87 GiB exclusive before compression; no deletion performed. Shared build-folder totals are not reclaim estimates.

## 2026-09-16: eastern horizontal-band overflow corrected within checked views

[[EXP-20260916-011 - Terrain camera range guard for horizontal bands]] confirms signed16 camera wrap for admitted western terrain at two failing cameras; tree-only/non-tree-only CPU controls show both contribute. Exact assembled guard removes only the two offending scene486 batch entries among three camera censuses. All92 final hardware frames are viewed and clear of the reproduced broad bands; final exact Up advances3.588s. Wider headings/corners/distant clipping, range-boundary face popping and performance remain unverified. Whole-face rejection is not near-plane clipping. Passive floor errors1.25 below/1.09375 above are not tight settled-contact acceptance; some turns/Up holds stop against grass. All assets/collision/source exact to EXP010, preserving earlier native contacts/relocations without rerunning them. Initial spawn-height selection and EXP010 missing page27 replay context remain unresolved. Appearance/banking pending; EXP005 bank untouched.


## 2026-09-11: real grass boundary has near and distant representations

[[EXP-20260911-016 - Training grass boundary near and distant representations]] confirms current primary255/256 geometry and source25/segment19
collision. Secondary15 represents the boundary farther away; both geometry and
camera are quarter-scaled. EXP015's distant identification remains valid but its
explanation was incomplete. Exact proxy topology, all transition views and a
custom-wall distant version remain unvalidated. No mod/performance change.


## 2026-09-11: user's distant grass identified as secondary geometry

[[EXP-20260911-015 - Training grass uses secondary background geometry]] identifies the crop's grass as secondary15. Quarter camera
translation and a separate clipping path explain why it persists beyond the
ordinary walls. EXP014's panorama/13-primary-plant evidence concerns other
objects. General foliage classification, unlimited range and a usable background
wall proxy are unproven. No mod or performance change.


## 2026-09-11: Training panorama versus remaining wall distance

[[EXP-20260911-014 - Training flower panorama and wall cutoff]] confirms the distant flower strip is a scrolling bitmap, independent
of world translation and ordinary draw-distance globals. From the entrance,
garden wall298 loses21/24 tested quads;299..307 fail outer distance admission
at the installed2x profile. This bounds whole-garden coverage, without changing
EXP013's closer-view success/performance. Beyond2x or a visual wall proxy remains
unimplemented and unmeasured; nearby 3D foliage is distinct from the panorama.
Follow-up native checks place13 initial-direction plant meshes inside2x.
Exhaustive grass identification and per-object GPU occlusion remain unclaimed.


## 2026-09-11: 2x distance implemented with bounded performance acceptance

[[EXP-20260911-013 - Twofold distance and Training performance]] restores the
Training corner in hardware. Matched60s trials show31.23/31.25 FPS and similar
CPU use. The saved shared setting is2x original; earlier EXP012's no-install
status is superseded. Whole-garden coverage, other-level performance, per-frame
GPU times/1% lows and other machines remain unmeasured. The finite cutoff and
last accepted EXP009 bank remain; no new user appearance acceptance is claimed.


## 2026-09-11: Training corner is beyond the polygon depth limit

[[EXP-20260911-012 - Training corner render distance diagnosis]] confirms the
corner passes admission but exceeds the current1.5x profile. Walls already use
the longer group.2x restores the captured corner in original-PC CPU replay;
EXP013 subsequently installs the shared2x setting and confirms this view live
with a bounded performance comparison. Wider camera/performance limits remain.


## 2026-09-11: Training floor/deck occlusion corrected in bounded views

[[EXP-20260911-010 - Training floor occlusion and platform underside]] confirms original floor bias9 contributes to Flik/seed being drawn
through nearer ground. Zeroing16 bytes resolves the retained native depth
samples and the clear hardware view; a subdivided deck bottom also looks solid.
The bias exists in retail and the previous bank, so it is not attributed to the
new platform mesh. Every camera angle, native Windows/software rendering,
precise1ms game-input consumption and user visual acceptance remain unknown.
The floor-subdivision prototype is rejected and absent from production. Grass
can hide the seed and must not serve as floor-occlusion evidence. No new bank.


## Commit validation limitations, 2026-09-10

2026-09-10 - Codex - Commit cannon summit leaf rotation and voice export
records 252 passing focused tests. The broad check stops after 3,449 passes on
`tests/test_r2p_p0e_y_restore.py:923`: synthetic `y:` resolves to `retail` after
the expected refusal, but the assertion expects `stage`. It also fails alone;
test and implementation are unchanged from HEAD11e7b14. Root cause is unassigned.
The previously documented R2q design029/design031 hash mismatch also reproduces
alone. Exact evidence: `work/experiments/commit-20260910-cannon-leaf-audio/`
`make-check.log`, `r2p-baseline.log`, `r2q-baseline.log` and
`baseline-file-identities.json`. These failures need separate investigation;
no frozen expectation or restoration behavior was altered during the checkpoint.
Vault has no link, frontmatter, orphan or stale-state errors; its five existing
historical note-size warnings remain.

## Flik event voices and dormant Super Jump reminder, 2026-09-10

[[EXP-20260910-009 - Flik action pools and preview tail diagnosis]] adds ordinary
grain, shared pickups and nonfatal hurt pools, taking the catalogue to20 distinct
recordings.204 native cases at each of two bases and GUI group/variant checks
pass. Ordinary grain has exactly two candidates in its two handlers, not every
grain-themed quote; Training suppresses grain/shared-pickup chatter. Remaining
callers, combat/ambient/event attribution and live listening remain open. Shared
WAV uses are displayed together; per-event overrides are still unsupported.
Native event rules
and the running game's audio remain unchanged.


The default event filter is not exhaustive: Anthill exposes17 mapped recordings but
already has40 voice files/64 total initial-bank clips under the other filters.
Local ASR matches the user's “Ah, Ant Island!” to `SFX/US1A069.WAV`, sample70
in the native Anthill bank. Its exact play condition remains unverified; neither
wording nor native bank membership proves an entry/idle/location trigger. Full
dialogue labels, character attribution and a clearer default view remain open.
[[2026-09-10 - Codex - Locate Anthill dialogue hidden by event filter]].

[[EXP-20260910-005 - Flik event voice mappings]] originally verified nine native
recording/event bindings: two hint types plus seven pickup responses. Grain
responses are attributed to Tunnels/City Entrance; City Square's updater requests
missing Super Jump periodically. Normal City Square banks9/21/22 omit sample64,
however, while startup bank1 contains it. The user recollection and native
request must not erase this bank contradiction. The UI exposes the event as
dormant, not enabled by importing a replacement. A read-only live observation
of sample ownership/bank/timer around City Square entry and audio reinitialisation
would distinguish remaining audibility paths; no such live test is accepted yet.

Native31-case/two-base execution and GUI per-level import/build are accepted,
not complete-game listening or all voice-speaker identification. Transcribed
wording is automatic and labelled; other US clips remain unidentified. Event
conditions/repeats are read-only. Per-file imports affect every use in their
scope; independently configurable callsites, enable switches, cooldown edits,
new events and dormant-bank restoration remain unsupported. Loaded pickup
recordings do not establish retail placement of every pickup in every level.

## Mr. Soil trigger verification boundaries, 2026-09-10

Repository-wide check caveat from this handoff: the unchanged baseline R2q test
`tests/test_r2q_quiet_census_design.py:5899` expects design029 hash6cd3d734…93da0,
while unchanged production `_frozen_protocol()` at
`reimplementation/ablpc/r2q_quiet_census_design.py:23234` explicitly selects
design031 hash7d826b13…ec554. The failure reproduces alone; both files and the
historical-device adapter are exact to HEAD75a0bf6 (test's latest commit45ae953).
No frozen R2q source/evidence/test was changed to clear this unrelated failure.
It needs a separately scoped expectation/authority review, not a runtime action.
2026-09-10 - Codex - Fix Training count sign and defaults.

[[EXP-20260910-007 - Five-throw Training sign and native defaults]] adds user
acceptance of the corrected five-count initial sign/countdown and continuation.
It fixes the separate0043C250 initial-number path missed by EXP006's countdown
fixture.
The numeric bank is confirmed to have six32×32 frames by live/static RAW matching.
Above6 still needs extended number artwork and bounds-safe lookup; seven has not
been run and no specific crash/rendering outcome is claimed. This bank limit
does not prove a six-count maximum in the native action counter.

[[EXP-20260910-006 - First Soil throw count boundary proof]] adds exact first-
lesson targets1–6, native countdown/lesson execution and negative timer samples
at two PE bases. The fixture starts simulated throw timers; it is not whole-game
input evidence. Live target5 is now user-accepted through EXP007, not all six
targets or every lesson. Automatic mode, when selected, ignores action counts.


EXP-20260910-002 establishes the14 native
predicates and file-built original/goal+speech/speech-only policies. Both PE bases,
adjusted counts, special negative controls, stream cancellation, clock wrap and
terminal behavior pass offline. Hardware all-auto traversal reaches quiet final13;
the log requests all14 original WAVs in order. Detailed full-drain/tail samples
cover stages0–8; a sampling gap omits later transitions. Later completion is
supported by the final state and ordered log, not fabricated per-stage timing.
The sink was muted: user listening acceptance, longer replacement WAVs, live mixed
modes and complete original-goal routes remain open. Higher action counts than6
need a safe numeric-HUD extension. Arbitrary condition expressions/actor targets
and original-map geometry export remain unsupported.
The two-second trail uses wall time, including any pause after the tail begins.

## Original Training mapping limits, 2026-09-09

[[EXP-20260909-012 - Original Training Blender mapping]] delivers all278 stored
scene meshes, original textures and bounded collision/placement layers.
[[EXP-20260909-013 - Populate original Training Blender map]] adds54 native-
initialized pickup positions, nine actor placements and the exit overlay. It
does not establish native animation/camera-dependent deformation, actor heading/
movement/full actor simulation, generated plants, material/lighting parity or
original-level game-file export.147 objects use stored poses for nonzero animation selectors.
Mr. Soil's stored mesh includes helper/alternate parts, not a verified selected
animation pose. Spiders/seeds/grain are editor silhouettes; actor feet are native
floor-query placements, not full actor simulation. The sign/contact association
is geometric inference; result3's native completion dispatch is tested offline.
The43 distant-primary grouping is geometric presentation, not proof those objects
are unused. EXP-20260910-001 now
maps all62 type3F rows: two green tokens, two blueberry records (one off-map),
and four type2C berry-plant seed tokens supplement EXP013. Native setup/blueberry
pickup/lesson12 gate/30-update delay/lesson13 reveal are proven offline with
feedback and plant-refresh callbacks stubbed. Original-goal live lesson route and resulting
plant growth remain untested. Type0B meanings remain unnamed. Only exact retail
Training is exposed by the CLI; the Anthill sprite dispatch explicitly rejects.
Another level or full animated-actor extension needs its own bounded profile/runtime discriminator. Current
mapping and annotation task is delivered in [[PC original Training Blender mapping]].
The later lesson census and live all-auto route are separately established by
[[PC Mr Soil lesson triggers]]; this does not animate the Blender actors.

## Collectible coverage, 2026-09-08

[[EXP-20260908-021 - Native collectibles and Blender placement]] verifies native table/height handling, bounded pickup/progression,
Blender XYZ and add/remove, edited builds, all67 live initial positions and natural
grain collection. Full route/collect-all reachability, every sprite/color close-up,
seed upgrade planting, death/reset/respawn and future placements remain untested.
Offline feedback/audio/HUD callbacks were stubbed and cannot prove presentation.
FLIK slot/bit ordering is native, but individual glyphs were not each newly viewed.
EXP021 left three original30 rows unmanaged; EXP-20260915-005 now confirms
their telescope role. Limits50 grains/one each letter/three tokens per color/32 berries are
profile constraints, not an expanded or universally established native capacity.


## Native enemy authoring coverage, 2026-09-08

[[EXP-20260908-020 - Native enemy placement and scattered Blender population]] confirms PC mappings, codec, native initialization, Blender editing,
original-enemy replacement, exact live counts and user-approved scattered layout.
Combat damage, every death/respawn path, future terrain placements, full53-enemy
plant-growth/crowd behavior, arbitrary rotations/scales and AI/path editing are
not exhaustively validated. The53-slot source limit does not expand native actor
or plant pools. The source1 mosquito relative patrol remains outside authoring;
source4's native roaming script is used. RAW opaque header semantics remain
unknown; suffix lengths vary across PC levels. Blender silhouettes are placement
previews, not a native model editor. PC type35 maps to FLIKHarv; its complete role
is not inferred from that name. No streaming or live-write task is authorized.


## KU-20260908-TERRAIN-PAGE-LIFETIME — native integration open

**Paused by user, 2026-09-08:** the unknowns below remain unresolved and are not
the active work queue. [[PC Large-Level Engine Roadmap]] Milestone4 is paused at
EXP016. Do not continue native actor-release or scattering investigations merely
because their next discriminators are documented. A larger resident-level
acceptance effort is proposed; no map selection/restoration occurred in this
exchange. 2026-09-08 - Codex - Pause streaming and review roadmap.

Latest bounded evidence: [[EXP-20260908-016 - Manual seed ownership and native scattering]] supplies actual full enumerated roots for a new cold seed63 sample and passes
drop/departure/return/re-pickup with205.369s/6418frames of page absence. This closes
the missing plant/selection capture for that sample; asynchronous reads and a
matching .data census still do not prove a safe live release. Original00415E30 can
write slot63 under mode0x80 with an empty queue; the mode was clear in20 live copies.
957 PE actor operands target37 slot regions across50 candidate function entries;
951 match Ghidra/instruction references, six retain the stated export limitations.
Indexed-base operands are not exclusively fixed-slot accesses.

The user's flying seeds coincide with activation of an initially crowded/airborne
cluster. Original0041D390 independently reproduces continuing ±256 X impulses for
the captured edge pair; distance/queue controls stop them. Complete initial-burst
and boundary-trapping attribution remain open. Next discriminator: separately
hashed spacing-only fixture retaining the launch state, before a physics change.
Next lifecycle work: gated fixed-slot/script-index policy and native frame-boundary
release/publication/rollback. No live slot deletion or serialization is installed.

Previous bounded implementation: EXP-20260908-015 stores the demonstrated detached
cold seed profile with stable authored IDs independent of native slots, exact
opaque bytes, known-pointer rebinding and image/world/payload hashes. Captured
moved-state replay passes eight queue/pickup cases, 128 actual-cell reader cases
and six offline slot-reuse simulations. 111 new regressions pass.

Still required before live actor suspension: complete native/renderer/callback
root census and an actual safe frame boundary, destination-slot admission,
transactional native publication/rollback, section/world stable-ID assignment,
held/growing and other actor records, collected-state and respawn/exit semantics.
The enumerated queue/carry/selection/occupied-plant checks are necessary conservative
checks, not a complete release certificate. The cold sample lacks complete plant/
selection roots; empty fixture values are explicitly synthetic. The format admits
at most 64 records and is not a general world manifest or live integration.

Previous completed checkpoint: [[EXP-20260908-014 - Manual moved-seed page persistence]] passes one moved-seed terrain-retire/return cycle and repeat pickup, with actor20/contact21
at exactly(309685,-157709,608401).277 cold observations retain full actor/placement
bytes; a2.106s/66frame interval proves actual page absence. Actor/placement arrays
remain resident. True section serialization, collected items, other actor kinds,
respawn/exit restoration and full callback/release lifetimes remain open.

The user's full20-plant test exposes two defects in the prior authored guard:
skipping ordinary seed update stalls pickup11→12, and one vacancy admits competing
partial growth animations. New private admission cancels rejected/held ten-tick
requests and refunds their partial Y displacement, while reserving vacancies against
live animations.47 native regressions and full-pool hardware release/retry pass.
Already-buried live-state recovery and twelve-way hardware contention are not claimed;
both have native offline coverage. Exact visual glow source remains unisolated.
The normal compiler/preview still uses the earlier policy; this adapter is private.

Four reset and two repeated-initializer cases show that initialization cannot restore
moved state. Ten queue cases distinguish a live null-terminated prefix from stale
trailing pointers.16 recorded queue-base consumers still need complete lifetime
analysis.310 broader numeric candidates remain. Both EXP014 diagnostics are CLOSED;
normal preview, saved Blender, bank and frozen EXP013 packet remain unchanged.

Previous completed checkpoint: [[EXP-20260908-013 - Seed auxiliary budget and distant carry]] identifies the stalled0041DA68 seed request with197 CPU/IP/stack samples and
budgets only two discarded-return emissions against the64-record shared pool.
Reserve8 stops that source consuming the final8 reusable records; unrelated callers
retain native full-pool behavior. Type53 native initialization matches the captured
retained fields, while the stalled request uses template1. Do not infer all record
birth callers from matching fields alone.

Patched contact1/64 distant carry/throw/landing passes, with102/215 suppressed
emissions, exact65 models and all64 placement identities. The unpatched positive
carry-offset8316 control also passes. Trigger dependence on actor0, density, paging
or timing remains open; no deterministic all-run failure claim is justified.
General pool ownership/overflow policy remains open beyond the two guarded calls.

Actual actor/item/collected-state section persistence,310 numeric reference
candidates, full consumer/driver lifetime, world manifests/budgets, wider coordinates
and total-memory bounds remain open. The selected distant-carry interaction gate
is closed for EXP013's finite profile. All four diagnostics close and EXP012's
390 artifacts/19 dependencies reverify; normal preview/exit and bank stay exact.

EXP012 checkpoint: [[EXP-20260908-012 - High-slot seed interaction and native pool limit]] closes the selected native contact2/64 seed pickup/local-carry/throw/landing
check. Both accepted positive-offset controls retain all64 selectors/placements,
valid ground anchors and65 model payloads. This is not section serialization,
every actor kind, or distant carried-actor traversal acceptance.

EXP012 narrows EXP011's770 remaining numeric windows to310 using459 long exact
WAV spans and one initialized PE span.5422 of5732 broader snapshot entries are
now classified. Exact addresses and source offsets are in EXP012
`reference-refinement.json`; numeric candidates are not established pointer owners.
EXP010's separate515-entry census remains accounted for as recorded in EXP011.

New concrete capacity unknown: original0042AA50 loops through64 records at00598CA8,
stride56, when every byte+51 bit0x80 is set and u16+34 is nonzero. The rejected
actor0 control reaches that state.196 read-only CPU IP samples, the pool capture
and192 offline native cases agree. Pool kind, caller/owner lifetimes and overflow
policy remain open;0043EF06 dereferences its return without a null check. The carry
word at0059D96C is a byte offset, with extra branches for zero. A positive-offset
distant-route control is needed before attributing saturation to normal content,
density, contact repair or paging. No patch was installed.

Still open: the310 candidates and complete query/callback/global/heap/driver/
register-stack/trailer provenance; actor/item/collected-state persistence across
section unload/reload, respawn and exit; general manifests and resident/staging
budgets; native capacities, wider coordinates and total-memory bounds. The paired
late RSS discriminator remains accepted in EXP011, without diagnosing EXP009.
[[PC terrain streaming ownership ledger]] owns the covered release boundaries.

All seven EXP012 private copies are CLOSED. Normal preview, level exit, saved
Blender and banked wilderness remain exact. EXP011's569 artifacts and13 source
dependencies reverify; implementation code is unchanged.

Earlier checkpoint: [[EXP-20260908-006 - Native actor and camera contact repair]] repairs the proven actor/camera slot defect for the64-placement
profile: player0, actors1..64, camera65. Native initialization,3960 movement calls
and240 camera-wall comparisons pass. Hardware27-selector/20-plant checks pass;
hardware64-seed selector assignment passed, but high-slot pickup/throw was then
unaccepted. EXP012 now supplies the selected positive-offset interaction control.
Entity initialization still retains cached contacts; do not infer pin release.

EXP-20260908-007 closes a startup integration step: the real hardware game loads compact
page files, allocates and validates them, then binds both native rendering and
collision before bounds construction. All pages remain resident. Controlled
native tests cover startup IO failure/rollback and abort; live failure recovery,
eviction and real level-reload reuse remain unaccepted. Allocation figures are
not total RAM bounds or savings.

Still required: actual frame/query/register/stack/driver/trailer lifetime closure,
combined transition readiness and safe retirement, actor/item persistence across
unload/reload/respawn/exit, wider coordinates and long hardware memory/state/control
acceptance. The normal preview keeps the earlier executable and unchanged assets.
The original24-record/15-actor guard is retained for unrepaired images. Historical
EXP003–005 statements below retain their narrower checkpoint scope.

EXP-20260908-003 confirms
that descriptor rebinding alone leaves cached contact007F3D6C into source189's
old allocation. Original004AB22C faults on offline unmapping; static indexed
reads and004ACFD0 provide independent evidence. Native traversal to source190
permits one bounded old-page retirement with exact next-step parity. Complete
contact-table layout was not established at that checkpoint. EXP-004 below
resolves its initialized extent and bounded query retirement; complete actor,
renderer and primary-trailer lifetimes remain unknown. A caller-supplied boundary
flag cannot establish the actual live frame's safety.

Milestone4 has begun with checked page files and bounded transactional cache
tests. Native frame-boundary file IO/publication, ground readiness, actor/item
persistence, wider coordinates and long hardware memory/state acceptance remain
open. Fresh six-chunk bank compilation fits the existing file budget; area alone
does not force streaming. This does not resolve the bank's reported instability.
[[EXP-20260908-004 - Native terrain page residency]] now verifies all24 initialized
contact slots and concurrent slots16/23, with stable bucket membership and guarded
descriptor deactivation.1750 offline movement steps and24 query comparisons match
resident controls with actual page loads/unmaps. Corrupt second-load rollback
passes. Native actor selector bounds, anticipated queries, inactive-slot release,
live register/stack/frame liveness and persistence remain unproved. The image's
468 preexisting numeric matches are not new page-pointer evidence. Control
straight-line stalls in several lanes remain a fixture/route limitation with
cause unresolved; the matched Z11500 route completes. Full original asset
buffers still load, so48KiB page-mapping residency is not total game-memory
acceptance. [[PC Large-Level Engine Roadmap]] owns the remaining gates.

## KU-20260907-DENSITY-AND-REFINEMENT — current stage 3 profile accepted; broader limits remain

[[EXP-20260907-025 - Native density limits and terrain refinement trial]] retains
5462 vertices/8192 faces per native mesh and a conservative static overlap bound
of300 against the original400-pointer collector at007F3F50. The movement envelope is a
3D delta length<=10000 world units; arbitrary dynamic actors remain unproved.

**Confirmed in [[EXP-20260907-026 - Collision-preserving visual density and frame work]]:** all three saved interior counterexamples first diverge
in support flags at step5, then select airborne`004AA4D0` at step6 and move by
103/51/64 world units relative to control. The current-triangle test`004AAE30`
returns0 after the added edge; the later contact path also returns0. Exact plane
rounding is not established as the sole cause. No general solver repair is claimed.
The new visual-detail option retains original collision bytes and passes286
native routes exactly, including flags/contact/instruction count. Direct authored
collision subdivision still changes native behavior.

The old timer measures render/present only; gameplay precedes its start00405C07.
[[EXP-20260907-028 - Representative update and render headroom]] corrects that scope and adds separate high-resolution update+render
and render intervals, per-frame camera/counters, two routes per build and one
active type5 plant. All11320 captured frames have no probe errors or drops;
paired route p99 whole work0.4921/0.6591ms, active collector peak26. Exact spawn
camera contexts match, while feedback routes are not identical input movies.
This closes representative bounded measurement, not arbitrary headroom.
[[EXP-20260907-027 - Native respawn cycles and exit-aware traversal]] now verifies six finite native reset cycles, both complete four-section
feedback loops and paired completion/re-entry with exact model/chunk pointers.
This closes the missing bounded lifecycle/traversal observations for the current
profile, not all actor/camera behavior. An initial result1 fixture reaches
GameOver after saving a lethal respawn point; result4 can still cause damage at
the returned boundary. Safe interior hazard entry/respawn remains unproved.
[[EXP-20260908-001 - Plant capacity and collision workspace repair]] now confirms
offline that the twentieth construction loops indefinitely and19 overlapping
native mushrooms can overwrite descriptor0 at candidate index400. The new
2048-entry workspace and bounded plant guards pass20-plant native opening,
registration and solving (peak508), with two-base append/constructor checks.
EXP-20260908-002 now confirms full20-plant hardware loading, native pickup/throw/disappearance,
descriptor clearing and waiting-seed reuse. Its13121 captured frames have no
errors/drops; two native bounce runs and exact170-model/four-chunk checks pass.
This closes the simultaneous-pool and consolidated stage3 gates for the current
level. It does not certify arbitrary dynamic classes or enlarged coordinates.
Native appends remain unchecked beyond2048. The Wine arena maps rwxp despite
non-execute PE flags; effective host NX remains unestablished. Wider movement,
coordinate arithmetic, safe hazard placement and conditional streaming remain
open. The4.85× wilderness remains banked; protect the other agent's tree/session.

## KU-20260907-CHUNK-MODEL-STORAGE - Resolved for the pinned profile; broader limits open

[[EXP-20260907-023 - Dedicated asset arena and terrain chunk acceptance]] resolves EXP-022's reproduced model/scratch overlap. Two true native
base operands feed the retained-data cursors; a dedicated 8 MiB PE region preserves
native pointer construction and HIGHLOW relocation. All 170 native model outputs
match at the new addresses, and three hardware arms pass, including the larger
3094194-byte fixture. The old reset root was also overwritten; its new root
stays intact. EXP-020's unexplained exit remains a separate unknown.

EXP-20260907-024 freshly verifies the
original milestone gates. Five completed identical model-load sequences are
logged in the current session and latest resident bytes remain exact; causes
of those reloads and uninterrupted transition behavior are not established.

EXP-025 supplied the initial bounded geometry/density evidence; its incomplete
live route and overlapping manual input remain historical limitations. EXP-027/028
subsequently complete feedback loops and representative frame-work measurements,
and EXP-20260908-002 closes full-pool endurance and the current stage3 gate,
freshly rechecked in EXP-20260908-003. Arbitrary levels, longer actor/transition stress, wider coordinates,
streaming and general allocation safety remain open. [[PC Large-Level Engine Roadmap]].


## KU-20260907-MODEL-STORAGE - Confirmed overlap, bounded authoring budget

[[EXP-20260907-017 - Trunk scenery and character storage overlap repair]]: renderer scratch0076F9A0..AF overwrites body18 when added level
bytes push its polygons over that address. Nine captured poses discriminate
safe/overlapping storage; shared positive meshes repair the current build.
The1000000-byte combined DAT/TERRAIN/PLANT limit is conservative for pinned
resources, not a complete allocator proof. Other load orders/resources and
all subsequent arena occupants need separate bounds evidence. Runtime checks
remain required. Walkable trunk frontage and pebble UV correction are implemented in EXP-018/019.

## KU-20260907-TREE - Complete source meshes versus whole-tree assembly

2026-09-07 - Codex - Original game and trunk sampling, EXP-016: current trunk wall is mapped to scene5/6 by native/live
projection; full adjoining scene5/6/7/8/17 data is resident and privately
exported (467 vertices/358 faces).105 open edges and further scenery joins
prevent a complete freestanding-tree claim. Canopy existence, all constituent
chunks, texture assembly and collision pairing remain unresolved. Capturing
known mesh bytes is immediate; reusable whole-tree authoring is separate work.


## KU-20260907-JOLT - Confirmed contact overflow; actor lifecycle remains open

[[EXP-20260907-014 - Cliff seam and phantom seed collision repair]] resolves the sideways-push mechanism: extreme-position type11 seeds
pass overflowing32-bit distance tests in0x0041C9B0; stores0041CD5B/60 reproduce
two exact live vectors. Guarded64-bit broad-phase arithmetic removes both,
with nearby seed/stomp/type5 construction controls preserved. Source of each
seed's extreme position remains untraced; missing support at retained original
off-layout placements is inference. Exact original EXP-013 actor snapshot was
not captured; fresh same-symptom captures provide the causal discriminator.

The reported floor fall is separately confirmed at east cliff X8448: wall-only
48-unit outward offset leaves an entry strip. Shared wall/floor X/Z edges fix
the native old-start regression at four speeds;49 strip pushes pass.40s live
user play has no gap beyond512world, maximum138. Arbitrary mesh/corner/speed
coverage and complete original actor migration remain open. See
`reports/terrain/EXP-20260907-014.json`; prior EXP-013 observation is retained.


## KU-20260907-DISTANCE - Further distance and broad performance acceptance

[[EXP-20260907-010 - General render distance preview]] installs user-approved
1.5× near/far groups1728/2496, including terrain.48 tests, actual Blender Build,
initializer bounds, eight primary-frame capacity checks and live code/table/data
verification pass. [[PC general render distance]] distinguishes camera depth
from distance to Flik and preserves mushroom object bias. Further expansion is
explicitly deferred.2× has initializer/selected-mushroom offline evidence only;
general-frame/live GPU/performance checks at2× remain open. Every-camera occlusion,
background behavior and sustained FPS are not established by the bounded1.5×
checks. Beyond2× requires new static/native bounds work before relaxing guards.

# Known Unknowns

## KU-20260906-SCENERY-MUSHROOMS - Net-new original scenery props


Third-cluster follow-up in EXP-015 adds same-mesh scenes75/77/78/102/103 and282 exact native/live XYZW matches; five selected resident shells compare fully. Pairing remains geometric inference, not new-copy motion coverage. No new mushroom asset family or production change;15 of22 placements now localized across three views.

Additional reference: EXP-20260906-015 confirms six more original placements of the same mesh at a different user pose.180 native/live XYZW matches and six complete resident shell checks strengthen localization, but those shell pairings remain geometric inference and their new-copy movement coverage remains open. No new mesh/plant type or production allowlist extension is claimed.

[[EXP-20260906-014 - Net-new scenery mushroom instances]] localizes four beige mushrooms to shared mesh179576 and distinct scaled0x19 scene objects. Shape/location and complete resident bytes support source142/146/147/148 shell pairings, not an explicit cross-file pointer. Two tall and one small net-new copies pass native loading/landing, twelve lateral and twelve grounded push-return controls plus exact translated emitted draw-output comparisons.484->487 primary records and189->192 sources prove no old slot replacement; incremental growth is tested.

Remaining: all-camera/performance behavior, arbitrary rotations/scales, automatic shell regeneration, atlas portability and the other two mapped variants' new-copy motion coverage. Full original small-prop west approach contacts floor108 and differs385world units; explicit floor108 removal in private control restores exact correspondence. Retain that environment-dependent difference rather than claiming full-world equality. Scenery tag6 does not establish the seed-grown planttype5 bounce path. EXP-014's three-prop fixture remains an offline control.

## KU-20260906-EXPANDED-VISIBILITY - Corner disappearance after area expansion

Implemented and user-confirmed for the reported issue: [[EXP-20260906-011 - Expanded corner visibility regression]] diagnosed geometric-only bound10087; EXP-20260906-012 shares the PC-aware helper and loads14183 without changing geometry/collision.18 new regressions,798 terrain-selected tests, all142 saved cameras and1792 in-frustum sweep targets pass. User confirms “looks good, just verified”; resident bound/full data match. Remaining: broader camera/profile/performance acceptance, not this reported corner regression. No live GPU branch trace or all-angle theorem. User play overlaps agent menu/movement receipts, so those are not controlled route proof. Recurrence procedure: [[PC terrain visibility growth checklist]]. This is separate from the unknown long-segment collision arithmetic below.

## KU-20260906-PLANT-STATE - Why does seed collision survive while opened-mushroom collision and bounce disappear?

Status: resolved for the observed type 5 mushroom / PLANTTER record 8; broader plant isolation remains open. Evidence: [[EXP-20260906-007 - Plant-state collision regression]] and [[PC seed and mushroom collision state]].

Observed by the user in the isolated EXP-006 runtime: the unopened seed blocks Flik, but after it becomes a mushroom Flik can occupy the mushroom volume and jumping onto it does not bounce him. A private screenshot was captured while the user reported Flik inside the mushroom, but position changed across the capture, so it is visual context rather than an atomic contact proof.

Confirmed: seed type11 uses actor contact at0x0041C9B0; the observed mushroom is plant type5, descriptor193/tag108, template descriptor186 / PLANTTER source8. Original instructions and a failing live census establish the correct transition/origin with an empty template. Restoring two bytes at0x2650 recovers four native lateral routes and contact-dependent bounce (store0x00468406); repaired runtime records five -3328 bounce onsets and user-confirmed jumping. Separate bounce-code loss, bad registration and bad origin are not needed to explain this failure.

Remaining: other emptied plant templates/states/upgrades and an authoring policy that preserves required templates automatically. High0x104 stays disabled. Varied grass is now live in the repaired derivative, but explicit aesthetic feedback, projectile equivalence and the inherited lower-ramp corner limit remain open. Do not generalize type5 acceptance to all plants.

## KU-081 composition follow-up, 2026-09-05

[[EXP-20260905-004 - Playable ramp and box area]] demonstrates a bounded practical
composition: banked deck/top, gentle ramp and connected side profiles, with paired
collision/render output, twelve modeled directional legs and two live out/back
cycles. The full known primary160 stream permits1526 bytes within2234; this does
not authorize writing unidentified adjacent data. The broad floor stays beneath
the solids, not a retessellated Boolean union. General layouts/materials/all-view
coverage and EXP-003's prop-confounded retail source100 crossing remain open.
Next local action is user play/feedback; do not redo standable-box validation or
start R2q as a prerequisite for this terrain work.


## KU-081 follow-up: bounded shared-floor repair, 2026-09-05

[[EXP-20260905-003 - Shared floor return discriminator and stitched patch]]
supersedes the earlier un-reproduced EXP-005 status. Original-instruction return
index10 admits cell47652 to the candidate list but rejects its negative starting
plane side at 004AA646; widening Y bounds does not change the failure. Rigid
perimeter edges have a 2048-world vertical discontinuity, not a new XZ gap.
A fresh normal-input rigid arm reproduces return penetration; connected-star
retail/stitched controls return successfully. This bounds the mechanism at the
tested route, not every historical fall or possible mesh defect.

Remaining: the same three prop-confounded complete-scene modeled routes (13/16
retail and stitched), a live source100 route blocked before its intended seam,
broader velocities/poses and full render/collision correspondence. The complete
mesh-stream census has original-instruction pointer/terminator checks on Level01
and Level03; it is not full renderer validation. General collision/material/level
authoring and the banked diagonal rule's universal validity remain open.


[[Project Roadmap]] prioritizes these questions; this register records their
uncertainty and resolution state rather than scheduling them.

- **KU-001:** Root `bugs.exe` is the installer-designated candidate; its disc-copy hash, architecture, imported libraries, and Ghidra baseline are known. Installed-file equivalence, version resources, imported-symbol roles, compiler/linker provenance, and packaging behavior remain unknown.
- **KU-002:** Required Win98 hardware, graphics adapter, sound adapter, driver versions, DirectX version, and resolution remain unknown. Under [[Decision Log#DEC-20260811-004 - Wine-first modding target]], these are optional historical-validation questions rather than blockers for Wine-targeted mod tooling.
- **KU-003:** Wine 11 staging reaches playable Direct3D training rendering under `EXP-20260812-005`, and Gamescope provides the aspect-preserving host presentation in `EXP-20260812-007`; deviations from Win98 behavior, audio completeness, long-session stability, and other levels remain unknown.
- **KU-004:** Whether a modern Windows debugging VM is necessary is unknown.
- **KU-005:** Whether PCem cross-validation will be necessary is unknown.
- **KU-006:** The remaining Fedora utilities are not installed until sudo authorization is provided.
- **KU-007:** The degree of code, data-format, and behavioral similarity between the PS1 and PC ports is unknown; each proposed correspondence requires a bounded comparison and independent PC evidence.

Do not resolve an item without linking the evidence or experiment that discriminates it.

## PC-native baseline unknowns from EXP-20260811-003

- What game-specific initialization begins at or below `0x0043DA40`?
- Which content root does `0x004129A0` select in each installation/media condition?
- Which startup files reach `0x004AE240`, from which callers, and with what destination capacities?
- Which DirectDraw and Direct3D devices, modes, surface descriptors, and texture formats are selected at runtime?
- Which imported COM class IDs and interfaces are requested?
- Where do DirectInput and DirectSound initialization begin?
- Which parts of the `0x004Bxxxx` region are statically linked runtime code rather than game code?

## Runtime unknowns after EXP-20260811-004

- Why does Wine 11 report the directory-backed volume through `cmd` but not satisfy the game's `GetDriveTypeA == 5` test?
- Does a block-device-backed ISO or physical optical drive select the intended CD-root branch?
- Does the retail installer produce a layout equivalent to the derived `PC\BUGS` test layout?
- Which PC-native runtime mechanism can capture the DirectDraw surface deterministically during mod A/B tests?
- Which WineD3D pixel-format warnings affect rendering rather than diagnostics only?
- Which Quartz/DirectSound failures affect intro movies, music, or game sound?
- Can the confirmed first-CD selection behavior choose the wrong disc in a multi-optical-drive environment?

## Level-data unknowns after EXP-20260812-008

- **KU-008 (resolved):** Matched individual mutations produce three disjoint visible plant-element differences, and native watchpoints route all three records through `0x0044D5B8`. Records 124–126 are not three alternative LOD representations of one on-screen object in the tested Training start state (`EXP-20260812-008`).
- **KU-009:** Semantics of `LEVEL*.DAT` record types, many payload fields,
  negative signed record `+0x0C`, negative-count target blocks, dispatches other
  than the bounded `0x49` path, and non-target suffix sections remain unknown.
  `EXP-20260812-009` through `EXP-20260812-012` resolve the positive target,
  record-center, positive visibility-bound, flags, and relocated-payload roles
  only within their stated PC boundary.
  [[M1 Tool Support Matrix]] deliberately rejects or leaves read-only every
  unsupported part; M1.5 closes the tooling boundary, not these semantics.
- **KU-010:** Direct absolute work-tree paths fault downstream at `0x004A84A4` for both modified and unmodified files; the specific legacy path or loader assumption is unknown. The `X:\PC\BUGS` drive shape is a confirmed workaround.
- **KU-011 (resolved):** A compositor portal capture produced a discriminating cropped control/mod pair in `EXP-20260812-006`; ordinary X11 capture remains unsuitable for these DirectDraw surfaces.
- **KU-014:** `EXP-20260812-010` resolves the guarded-rebind discriminator:
  reciprocal `0x111E4`/`0x1319C` edits change only the selected placement's
  phase-matched visible content. Positive targets are therefore reusable
  render-content inputs for the bounded `0x49` path. Whether a target alone is
  a complete object definition, and how other payload fields affect material,
  animation, or identity, remain unknown.
- **KU-015:** A late 25-second gameplay watch window did not reread record 124, but the full lifetime and revisit conditions for primary scene records remain unknown. Native GDB hardware watchpoints work at the natural Training pause; the causes of native software-breakpoint and WineDbg-proxy faults remain unknown.
- **KU-016:** `0x0045A7F0` has a distinct negative-count target branch, and other masked scene dispatch values use different payload consumers. Their layouts and semantics are unknown and deliberately rejected by the new positive-count/dispatch-`0x49` tooling (`EXP-20260812-009`).
- **KU-017 (resolved within dispatch `0x49`):** The first three record dwords
  are upstream candidate-center components, not the render-placement tuple;
  relocated `+0x10` supplies the payload used for placement. Positive signed
  `+0x0C` is a visibility-bound input (`EXP-20260812-011`,
  `EXP-20260812-012`). Exact center axis names/units, negative `+0x0C`
  semantics, and whether other dispatches share this boundary remain unknown.
- **KU-018:** `EXP-20260812-013` accepts a Level 01 record-261 center edit and
  guarded `0x3703C -> 0x3459C` rebind, but both retain exact control frames at
  the starting camera. When record 261 becomes selectable, what it renders,
  and whether the rebind becomes visible later in the level remain unknown.

## Resource dependency unknowns entering M2

- **KU-019 (partially resolved):** `EXP-20260812-014` records the exact derived
  PC content-family census, five duplicate-hash groups, and the explicit paths
  requested in unchanged Training and Level 01 logs. The mapping from M1
  payload entries to file paths/loaders remains unknown. Inventory membership
  and loader observation are not proof of that dependency.
- **KU-020 (partially resolved):** `EXP-20260812-015` confirms that selected
  `.ANM`/`.ALL` basenames share coordinator `0x00444C40` but use distinct load
  call sites and immediate consumers. `.ANM` has a loader-size boundary and
  first relocation walk; `.ALL` instead advances from embedded lengths without
  consuming file size. `EXP-20260812-017` now bounds the `.ANM` first-level
  walk and safe-inspector behavior only. Complete layouts, pair semantics,
  arena capacity, and original malformed-file behavior remain unknown.
- **KU-021 (resolved at the traced boundary):** `0x00416100` emits plant ID 5
  literally. Exact Training DAT type-`0x3F` selector bytes at `0x394`, `0x3A4`,
  and `0x3B4` produce IDs 4, 10, and 6 through pointer slot `0x005C595C`.
  They share the DAT and `0x0044BB70` fixup with M1 but do not overlap M1
  20-byte records, payloads, or positive targets (`EXP-20260812-016`).
  `EXP-20260812-020` adds an important precision: same-class selector results
  are sequence-dependent because each class advances its own executable-table
  cursor. Changing the second `0x2B` at `0x3A4` omits plant 10 while retaining
  plant 04; changing the first cannot be interpreted independently.
- **KU-022 (partially resolved):** `EXP-20260812-017` bounds the `.ANM`
  first-level count/offset walk, first nonzero referenced header/list, and
  `-2` comparison. A lossless safe inspector passes all 11 PC plant files.
  Complete nested record boundaries, field semantics, original malformed-file
  behavior, and whether `.ANM` represents visible geometry, animation, or
  another behavior remain unknown.
- **KU-023 (narrowed):** A direct dependency from an M1 20-byte placement
  record or positive target to a specific plant/resource identity remains
  unknown. `EXP-20260812-016` proves a level-specific resource table in the
  same DAT, not that stronger bridge. `EXP-20260812-021` resolves plant 10's
  exact runtime ANM slot and two-entry range, then finds no read of the slot or
  either entry `+0x20` dword in the direct dispatch-to-renderer windows for
  records 124–126. `EXP-20260812-023` through `EXP-20260812-027` add guarded
  negative windows for every exact field populated by `0x00448010` and its
  plant caller, but only through their stated initialization/title endpoints.
  `EXP-20260812-028` extends both exact `+0x2E` words through `NextLife` and a
  separate 30.026628-second early-gameplay interval with no access. Copied
  state, event-specific consumers, input-driven events, and later outcomes
  remain open, so this M2 exit-gate question must not be inferred from visible
  shape. `EXP-20260813-049` reconciles all four written M2 gates and retains
  this as the sole milestone blocker: the M1 record/positive-target path and
  ID-zero `CHARS/FLICK.ALL` path have separate PC static/runtime/visible
  anchors, but no exact selection edge. M2.23's shared arena does not close
  the gap because `EXP-20260813-039` proves it is selector-1 software output.
  `EXP-20260813-050` completes the exact `0x0045A7F0` selector-2 builder-input
  slice with a negative: all ten inline Direct3D allocation arms derive their
  page/list, root, flush, index, vertex-base, and emitted-record inputs from
  the M1 target/command stream, exact caller inputs, renderer globals, local
  derived scratch, or existing batch state—not the ID-zero header/range or
  selected resource. The next discriminator was the finite producer census for
  the eight generic `0x005B18E0 + runtime_index * 4` readers retained by
  `EXP-20260813-035`, not another visible comparison, renderer-convergence
  inference, or assumption that a table-base xref selects ID zero.
  `EXP-20260813-051` now completes that census with a second negative: six
  readers are confined to the pre-coordinator update, `0x00444EF0` receives
  exact initialization index 11, and sole coordinator-local reader
  `0x00448350` consumes prebuilt object state before the M1 root load and
  record walk. Neither the selected-record nor positive-target closure reaches
  a candidate. This resolves the declared current-invocation generic-reader
  surface, not persistent/copied cross-frame state or whole-program indirect
  selection. Because the direct, exact renderer-input, and generic xref
  surfaces are now exhausted without an edge, `EXP-20260813-052` completes
  M2.37 by retaining the causal gate rather than merging the parallel M1 and
  ID-zero visible chains. It selects exactly one finite candidate in
  `0x0044CA00`: at most 20 selector words at
  `0x0059D9C0 + i * 0x30`, sign-extended at `0x0044CE0D`. Exact signed value
  `-103` would address ID-zero header `0x005B18E0` through
  `0x005B1A7C + selector * 4`, but no word value or M1 producer is proved.
  `EXP-20260813-053` completes M2.38 with a finite negative: four native paths
  only clear selectors to zero, and sole nonzero writer `0x00467E60` copies
  from 20 positive image-table values with no `0xFF99`. Its two direct calls
  consume the separate fixed 64-record pool; the normal-update call is inside
  pre-coordinator `0x0041EC40`, before M1's `LEVEL*.DAT`-derived record root
  is loaded or walked. No current-invocation M1 record, payload, or positive
  target produces signed `-103`, so this candidate is retired. Persistent or
  copied cross-frame state remains unknown, but supplies no exact edge; no
  other index/resource family is selected implicitly. `EXP-20260813-054`
  preserved this unknown and the causal gate but prematurely moved M2 to
  `Deferred`. The adversarial `EXP-20260813-055` audit found that M2.36 had
  already retained a finite unclassified producer surface: first dwords
  `0x0059B730/0x0059B7B4`, exact slots 2 and 3 of fixed pool
  `[0x0059B628,0x0059D728)` with stride `0x84`, select
  `0x005B18E0 + I * 4` at `0x004372A2/0x00437337`. Zero would select ID zero,
  but reader-time zero and M1 provenance were unproved. `EXP-20260813-056`
  completes M2.40: pool clear `0x0041C430`, retained-source copy
  `0x0041BD24`, and conditional removal zero `0x0041BBBA` are the complete
  bounded store set. Initial zero cannot pass the reader gates; conditional
  removal zero is statically reader-reachable after `0x0041ECF7` sets
  `0x4000`. Its inputs derive from separate `LEVEL.RAW` type-`0x23` fields and
  fixed-pool state, not an M1 record, relocated payload, or positive target.
  This retires the exact candidate without resolving the causal unknown. M2 is
  not deferred after `EXP-20260813-057`: the prior audit explicitly retained
  `0x0059D6A4` as fixed-pool slot 63, while exact arithmetic supplies the
  omitted slot-25 classification for `0x0059C30C`. Both feed exact fixed-
  pointer generic-header readers and were outside M2.40. That left M2 active
  on M2.41 only to decide those consumer gates, reader-time zero, and M1
  intersection. Other pool/list objects, readers, resources, indirect
  aliases, runtime, mutation, and cross-port work remain outside scope.
  `EXP-20260813-058` now completes that exact disposition. Slot 25 zero can
  reach its lookup initially or one update after removal and selects the
  ID-zero header's zero start word. Slot 63 zero is excluded by two explicit
  `I == 0x23` calls but can reach three state-gated calls that select the
  ID-zero retained end index. The common values/removal predicate derive from
  separate `LEVEL.RAW` plus fixed-pool state, while the direct gates are
  counter, scene/update, position, and event state; none is produced by the
  established M1 record/payload/positive-target route. `KU-023` therefore
  remains open. That left M2 active on M2.42 only for a fresh-context
  hard-truth audit of whether any exact finite PC-native successor was
  omitted; no broader candidate family is implied. Independent
  `EXP-20260813-059` completes that
  audit with `ACCEPT`: fresh rehash/disassembly supports M2.41's exact calls,
  reader-time-zero cases, gates, order, and M1 negative, while a separate
  retained-surface audit finds no exact finite successor in the evidence
  already cited through `EXP-20260813-058`. This does not prove whole-program
  absence and does not resolve `KU-023`. M2 is deferred with the causal exit
  gate unchanged. Revisit it only when cited PC-native evidence exposes one
  exact finite candidate, a concrete mod goal supplies a bounded
  discriminator, or a contradiction invalidates a completed negative.
- **KU-024 (resolved at the tested boundary):** Replacing plant 04 `.ANM` with
  exact plant 10 `.ANM` bytes while retaining plant 04 `.ALL` is accepted under
  Direct3D Training and reaches `NextLife`. No stable visible change is
  discriminated at the tested start camera beyond control animation variance.
  Later/off-camera/nonvisual effects and general interchangeability remain
  unknown (`EXP-20260812-018`).
- **KU-025 (resolved at the tested boundary):** Plant 04 and 10 `.ALL` files
  are both `0xE08` bytes. Replacing both plant 04 files with the exact plant 10
  pair is accepted under Direct3D Training and reaches `NextLife`, but no
  stable start-camera difference is discriminated beyond independent control
  animation variance (`EXP-20260812-019`). `EXP-20260812-032` extends this to
  one fixed Training trajectory in fresh unchanged/replacement/unchanged arms:
  the controls match exactly at 11/12 same-index samples, while direct,
  temporal-median, and stable-mask comparisons find no replacement-local
  region. The plant-04/10 direct visible route is therefore retired. Complete
  `.ALL` layout, later or off-camera effects, and general pair compatibility
  remain unknown; equal size and one accepted pair do not resolve them.
- **KU-026 (partially resolved/corrected):** `EXP-20260812-020` proves that
  changing only the second Training `0x2B` selector at `0x3A4` to `0x00`
  removes both plant 10 request lines, otherwise preserves the normalized
  initialization log, and reaches Direct3D `NextLife`. No stable start-camera
  mask is discriminated beyond three independent control baselines. The
  originally proposed `0x394` edit cannot isolate plant 04 because it shifts
  the shared `0x2B` cursor; plant-04 necessity remains untested. Which M1
  placement, if any, consumes plant 10 remains open under `KU-023`.
- **KU-027 (partially bounded):** `EXP-20260812-021` binds the exact Training
  plant 10 destination to ANM slot `0x005B1AA4` and two entries at
  `[0x005AAB00, 0x005AABA0)`. `EXP-20260812-022` finds no CPU read of entry
  `+0x20` dwords `0x006C3B3B`/`0x006C3E57` or adjusted first-entry dword
  `0xD7E00218` from the natural title start through `NextLife` and 71.708
  seconds of gameplay. `EXP-20260812-023` adds plant-specific guarded negative
  windows from the final caller adjustment through resource-batch return
  `0x004679C7` and the natural title. `EXP-20260812-024` adds matched negative
  windows for both entries' exact `+0x00/+0x04/+0x08` dwords through return
  and across the title into live gameplay; both entry heads are `0/0/0/1`.
  `EXP-20260812-025` adds a same-run negative for both nonzero `+0x0C` dwords
  through return and an unattended title; both remain `1`.
  `EXP-20260812-026` adds the same bounded negative for both exact `+0x2E`
  words; both also remain unsigned `1`, so neither plant 10 entry reaches the
  static `0x00446A8A/0x00447661` comparisons in that interval. Exact words
  `+0x28`, populated at `0x0044810B`, also remain zero and unread through the
  same guarded bounds in `EXP-20260812-027`. Thus every exact field populated
  by `0x00448010` and its guarded caller has at least one bounded watch window;
  this is not a lifetime absence result. `EXP-20260812-028` then watches both
  exact `+0x2E` words from the natural title through `NextLife` and for a
  separate 30.026628-second no-input gameplay arm with zero stops. Exact
  static reader `0x0044CE3E` is also inactive in a separate 10.014330-second
  no-input control. Whether a source record ever selects plant 10 at this
  candidate, which event activates it, field meanings, `.ALL` semantics,
  copied state, non-CPU or later-event state, and visible or behavioral
  outcomes remain unknown.

- **KU-032 (resolved at the M2.20 visible boundary):** Retained unchanged
  Training logs explicitly request `CD/CHARS/FLICK.ANM/.ALL`.
  `CHARS/FLICK.ANM` and `CHARS3/FLICKD.ANM` are byte-identical at `0x2C83E`
  bytes, while their `0x34EC`-byte `.ALL` companions differ at 2,115 byte
  positions from zero-based `0x4` through `0x34D2`. `EXP-20260812-033`
  confirms that the one-path `FLICK.ALL <- FLICKD.ALL` replacement is accepted
  and produces a repeated local difference on the input-controlled central
  figure at all four bounded anchors. This resolves acceptance and the exact
  loaded-file-to-render question only; path names and the visible figure do not
  prove identity or `.ALL` semantics.

- **KU-033 (resolved at the M2.21 request/first-consumer boundary):**
  `EXP-20260812-034` binds accepted Training `chars\flick.all` to
  `0x004671D0 -> 0x00445020 -> 0x00444C40 -> 0x00448010 -> 0x004AE240`.
  The selected default arm supplies resource ID zero; the whole-file call is
  `0x00448079`, and `0x00448010` is the first format-specific consumer. For
  exact unchanged `FLICK.ALL` and M2.20 source `FLICKD.ALL`, it materializes
  25 shared entries before the coordinator consumes the final one and records
  retained header indices
  `[0,24)` in slot `0x005B18E0`, mapping to
  `[0x005A9660, 0x005A9DE0)`. Native disassembly, exact file arithmetic, and
  accepted runtime log line 1460 independently support this boundary. `.ALL`
  field meanings, general layout, arena capacity, and filename identity remain
  unknown.

- **KU-034 (resolved at the M2.22 direct-bridge window):**
  `EXP-20260813-035` classifies the first proven unindexed post-initialization
  ID-zero read in one normal `0x0040FFC0` branch. `0x00402DC0` directly loads
  slot `0x005B18E0` at `0x004032F0` and calls `0x00445FF0` with destination
  index zero; that function updates entries rooted at `0x005A9660` with exact
  stride `0x50`. The nearest M1-coordinator-side direct range reader is
  `0x0044C440`, called at `0x0044D4BC`, but the same invocation does not load
  record root `0x005BA7E0` until `0x0044D4FA` or begin record enumeration
  until `0x0044D57F`. The established `0x004498F0 -> 0x0045A7F0` M1 path has
  no direct slot/range reference or call to the first-use functions. This
  resolves only the direct bridge for that branch/order window; generic
  runtime-indexed readers, persistent/copied state, alternate branches, later
  events, contributing entries, `.ALL` fields, and identity remain open.

- **KU-035 (resolved at the M2.23 conditional-output boundary):**
  `EXP-20260813-036` traces the retained-entry and M1 positive-target inputs
  through exact PC address formation. `0x0044F8EA` reads
  `S = *(entry + 0x20)` and walks `0x24`/`0x30` stream records;
  `0x0045A7F0` separately derives table base `T + 4`, positive command pointer
  `T + 4 + count * 12`, and table reads from command-item offsets. No direct
  source-pointer copy, call, or address-forming edge connects `S` and `T`.
  Their conditional branches nevertheless use the same transform scratch,
  `0x80`-stride arena rooted through `0x0081BC28`, counter `0x008082C8`,
  output link/flag offsets, and list topology rooted via `0x004E8CC8`. This
  resolves shared output convergence, not source aliasing, same-head
  membership, or M1 placement-to-resource identity.

- **KU-036 (resolved at the M2.24 record-span boundary):**
  `EXP-20260813-037` maps the exact 24 retained ID-zero intervals to
  `[0x0004,0x2AE8)`. Entry 8 is byte-identical; each entry in
  `{0-7, 9-23}` differs. Those 23 streams contain 2,102 differing positions
  across 183 selected records, and every difference lies inside a record span
  reached identically by both bounded `0x0044F8E0` walks. No continuation or
  contradictory bound occurs. The remaining 13 of 2,115 whole-file
  differences are exact descriptor-table offsets outside the retained
  intervals. This resolves interval and walk-span localization, not
  individual byte reads, visible contribution, identity, or format semantics.

- **KU-037 (resolved negatively at the M2.25 conditional-arena boundary):**
  `EXP-20260813-038` records one complete ordered cycle for exact candidates
  `{0-7, 9-23}` in each of fresh accepted Direct3D control/replacement/control
  arms. Every row has exact pre/post counter zero, record/byte count zero, and
  SHA-256(empty); capacity and base are also zero at the exact safe post-call
  boundary. The changed-emission set in the conditional `0x80`-stride arena
  is empty. This resolves arena provenance only for the tested start-state
  window; it does not identify the active renderer path or visible source.

- **KU-038 (resolved at the M2.26 renderer-path boundary):**
  `EXP-20260813-039` maps selector 1 to `native software render` and selector
  2 to `Direct3d render`. Selector 1 calls `0x0049C520`, whose
  `INITSOFTRENDER`/`soft.cpp` path writes capacity `0x2800`, allocates the
  `0x80`-stride arena, zeros its counter, and clears the list heads.
  `0x0049C3F0` is a selector-1 `InitSoftWindow` helper and does not touch that
  triple. Selector 2 calls `0x004119E0` and routes retained-stream forms
  through `0x00405FE0/0x00407450` into Direct3D batches that can flush through
  `0x004056A0/0x004058D0` to the device `DrawIndexedPrimitive` slot. Thus
  M2.25's all-zero arena is expected, and the prior hardware-arena label is
  corrected without discarding the exact software-branch topology. Exact
  contributing entries, records, bytes, and batch effects remain open.

- **KU-039 (resolved at the M2.27 Direct3D count boundary):**
  `EXP-20260813-040` statically accounts for both selected batch families and
  every reachable in-call flush/reset, then records fresh accepted
  hardware-rendered control/replacement/control metadata. All selected
  additions use root `0x004C4108`, page 16; family `0x004C410C` remains zero,
  and no selected candidate flushes in-call. Replacement vertex/index counts
  outside both controls reduce `{0-7, 9-23}` to exact set
  `{1,2,4,5,6,7,9,10,14,15,18,19,20}`. This is count provenance, not
  individual record/byte causality, identity, or semantic interpretation.

- **KU-040 (resolved at the M2.28 form/count boundary):**
  `EXP-20260813-041` reanalyzes both complete retained cycles in all three
  M2.27 arms and maps the exact pre-call record pointers/forms without a new
  runtime. All 145 changed records in the 13-entry set reach their selected
  `0x00405FE0/0x00407450` builder. Per-form replacement totals outside the
  inclusive two-control envelopes select 18 entry/form groups containing 124
  exact changed records and a minimum aggregate 30-outcome gap. Single-record
  offsets `0x0174`, `0x0858`, and `0x0AA4` have individually discriminated
  bounded append outcomes. The other 121 record identities remain explicit
  aggregate alternatives because the builders apply per-frame runtime
  admission predicates after the recorded pre-call boundary. This corrects
  M2.27's `B4/B3` label: those are completed append-path counts, not all
  function entries; the underlying count measurements remain unchanged.

- **KU-041 (resolved at the fresh per-record outcome boundary):**
  `EXP-20260813-042` maps exact append writes `0x004069A1/0x00407B00` and all
  earlier no-append edges, then accepts fresh metadata-only Direct3D
  control/replacement/control arms. All three audit the complete 168-call plan
  and retain 124 candidate outcomes with no selected flush or payload. Only
  entry 7/file offset `0x0A6C`/form `0x3C` differs outside both controls:
  `0/1/0`. The controls disagree on 13 other records, which remain excluded.
  M2.28's three older single-record outcomes do not reproduce, confirming
  their per-frame scope rather than a source-stable contradiction.

- **KU-042 (resolved at the exact builder-input boundary):**
  `EXP-20260813-043` finds exactly 12 differences in record-relative spans
  `+0x00..+0x02`, `+0x24..+0x26`, `+0x28..+0x2A`, and
  `+0x2C..+0x2E`. Native caller/builder data flow proves all 12 reach four
  separate byte-derived dwords at appended vertex-record `+0x10`, but only
  after successful count write `0x004069A1`. No differing byte distinguishes
  admission: the earlier path consumes unchanged source spans, unchanged
  index byte `+0x2F`, the same sign/zero mode in both files, and per-frame
  state. M2.29's `0/1/0` receipt is exact for its arms but not a source-stable
  append-decision attribution.

- **KU-043 (resolved at the M2.31 admission-slice/design boundary):**
  `EXP-20260813-044` reduces the physical non-source input union for exact
  record `0x0A6C` to 23 locations, with at most 22 read in one native path
  because two thresholds are mutually exclusive. Exact source-derived mode 2
  reduces admission to 12 ordered logical rejection slots and 13 concrete
  reject PCs. The existing selector-read data watch at next PC `0x0044F951`
  and entry-post/count closure can support first-reject, state-digest, and
  predicted/observed metadata without retaining raw values or adding an
  execution point. This resolves the static input/evaluation and receipt-
  design boundary, not which input differed in M2.29's arms.

- **KU-044 (resolved at live evaluator agreement; stable attribution
  rejected):** `EXP-20260813-046` live-validates the exact schema-6 evaluator
  in three accepted post-`NextLife` hardware arms. Prediction equals observed
  count outcome in every arm. Control A and the replacement both reject at
  `0x004065B0` after seven slots, while control B passes all 12 slots and
  appends, yielding fresh pattern `0/0/1`. The unchanged controls disagree and
  the replacement does not pass, so M2.29's retained `0/1/0` is not source-
  stable across launches. The result resolves evaluator/count agreement but
  rejects a stable-control/replacement-pass attribution.

- **KU-045 (resolved at bounded within-process recurrence):**
  `EXP-20260813-047` fixes the M2.33 discriminator at three captured cycles
  after one warmup and fixture-proves its complete-cycle, ceiling, redaction,
  and output-exclusion gates. Freshly authorized `EXP-20260813-048` then
  accepts one unchanged post-`NextLife` arm at 816 stops and observes exact
  reject/pass/reject (`0/1/0`). Both rejects occur at `0x004065B0` after seven
  slots; the pass evaluates all 12, and every prediction matches the native
  count outcome. All three active-state digests differ. This resolves whether
  the boolean/reject receipt can vary and recur within one process. A period,
  distribution, cross-process sequence, equal underlying reject state,
  source/visible causality, and state semantics remain unclaimed rather than
  inferred from one bounded sequence.

## M4 toolkit unknowns

- **KU-046 (resolved at the deterministic planned-path/type boundary):**
  `EXP-20260814-060` proves that schema 2 can copy the exact
  user-owned `CD/CHARS3/FLICKD.ALL` source over exact
  `CD/CHARS/FLICK.ALL` destination with both input hashes preflighted,
  byte-exact sparse/staged output, deterministic input/replacement/output
  receipts, source preservation, path/symlink/same-path/collision rejection,
  and retained M1 operations. The ignored local corpus resolves the two exact
  demonstrated hashes without tracking either asset. Independent
  `EXP-20260814-061` rejects the stronger complete-output-preflight claim:
  `apply` writes its fixed receipt through an existing `output/.ablpc`
  symlink outside the output root, a later non-directory destination parent
  leaves an earlier sparse write, and a staged `.ablpc` file leaves a copied
  and modified tree before receipt failure. These are one bounded planned-
  output containment/preflight defect; `--force` also accepts a directory
  destination and fails after an earlier write. `EXP-20260814-062` supplies
  the exact M4.3 worker correction: every manifest destination plus the fixed
  receipt receives `lstat`-based deterministic topology preflight, `stage`
  checks the topology those planned writes inherit before copying, and all
  four cases now raise `ManifestError` without earlier, outside, receipt, or
  staged output. Positive force-file replacement, 47 focused and 235 complete
  tests, and the exact local recipe remain green. Independent
  `EXP-20260814-063` accepts the correction after reproducing the original
  four and 22 adjacent topology cases with explicit snapshot-equality and
  absence checks, plus 6/6 schema M1 applications and two exact local recipe
  applications. Unpredictable permission, storage, unrelated copy/I/O, or
  concurrent-race failures remain outside the non-transactional preflight
  claim. This does not establish `.ALL` layout or semantics, general file-pair
  compatibility, composition, removal, launch, or a compatibility statement.
- **KU-047 (resolved at exact authored-sequence composition boundary):**
  `EXP-20260814-064` adds `compose LEFT RIGHT --source-root ROOT` for exactly
  two existing schema-1/schema-2 manifests. Inputs are canonical-digest
  ordered and independently guarded against one source tree. Existing
  operations claim exact 12-byte, 2-byte, 4-byte, or whole-destination
  half-open intervals. Disjoint same-file/different-file pairs emit byte-
  identical existing-schema JSON under reversed arguments; overlapping M1
  spans and opaque same-destination pairs emit byte-identical asset-free JSON
  with empty stdout and no filesystem output. Synthetic apply/stage output,
  58 focused and 246 complete tests, and tracked same-file plus M1/schema-2
  local pairs pass with source preservation. Independent
  `EXP-20260814-065` reproduces those boundaries but rejects the complete
  disjoint-composition claim. A valid left input applies in authored payload-
  target-then-position order, and a right field-`0x0C` claim is disjoint; the
  composer nevertheless globally sorts edits by source span, reverses the
  left sequence, and makes combined revalidation fail in both argument
  orders. Exact M4.7 was selected only to preserve intra-input edit-index order
  under deterministic canonical two-input composition. N-way dependency
  ordering, cross-input semantic reconciliation, general dry-run, removal,
  launch, compatibility, and receipt/schema redesign remain explicitly
  unknown/out of scope rather than solved by that correction.
  `EXP-20260814-066` now completes M4.7 at the worker boundary: canonical input
  rank plus original edit index closes the exact `0x98`/`0xA4`/`0x21C`
  failure, saved apply/stage and ordinary receipts match the authored result,
  adjacent multiple-edit/opaque/conflict cases pass, and the focused/full
  suites are 63/251. Both tracked local composition and output hashes remain
  unchanged. Fresh-context `EXP-20260814-067` independently accepts the
  correction after reproducing both input applications, disjoint claims,
  reversed composition, saved apply/stage bytes, receipt equality, and source
  preservation. Both canonical rank orientations, multiple destinations,
  three authored edits/four total shared-destination edits, descending offsets,
  same-span guards, empty/unequal opaque files, multiple conflicts, and the
  complete collision matrix pass. A genuine cross-input guard dependency fails
  closed identically in both argument orders. The scoped suites remain 63/251,
  topology/schema matrices pass 28/28 and 6/6, both local pairs and the exact
  recipe retain their hashes, and the asset-free boundary remains intact. This
  resolves exactly-two-input composition, not N-way ordering or cross-input
  semantic reconciliation.
- **KU-048 (accepted at the exact current-Linux removal boundary):** The ordinary sparse
  overlay contains recorded destination files plus fixed
  `.ablpc/receipt.json`, and the accepted receipt records schema, manifest
  name, exact input/output hashes, normalized applied edit details, and opaque
  replacement hashes. `EXP-20260814-068` now recomputes those results from the
  supplied existing-schema manifest and exact source root, requires strict
  JSON plus byte-exact ordinary receipt equality, verifies every recorded
  output and the receipt as single-link regular files, checks each output's
  recomputed hash, and requires an exact no-extra-content overlay tree before
  deletion. Thirty-two parameter-expanded
  cases cover successful single/multi/composed and empty-output removal;
  changed/missing/symlink/FIFO/hard-linked outputs and receipt; source drift;
  receipt schema/name/path/edit/hash/extra/duplicate/encoding mismatches; extra
  file/directory/symlink/FIFO
  content; staged-tree refusal; protected/symlinked roots; and exact snapshot
  preservation. Focused/full suites pass 95/283, while exact opaque, same-DAT
  composed, and M1-plus-opaque local families each apply/remove twice with
  deterministic receipts and unchanged source hashes. This supports
  sufficiency only at the M4.9 worker boundary. Independent
  `EXP-20260814-069` preserves those ordinary cases but disproves complete
  preflight for one stable topology: a pre-existing bind-mounted intermediate
  overlay directory passes the current no-follow checks, then its output and
  the receipt are deleted before final pruning fails `EBUSY`. Both reproductions
  change the overlay and independent mounted target snapshots.
  `EXP-20260814-070` now supplies the exact worker correction: before overlay
  traversal or unlink, a Linux `/proc/self/mountinfo` guard decodes kernel
  escapes and compares the overlay root plus every planned directory, output,
  and receipt with the current mountpoint set. Isolated same-filesystem bind
  mounts at root/intermediate/output/receipt refuse 4/4 with byte/type/link-
  complete overlay/source/independent-target snapshots unchanged, including a
  live `\040` path escape. Ordinary manifest tests pass 84/84, focused/full
  suites pass 99/287, and all six exact local cycles retain established hashes
  and unchanged sources. Independent `EXP-20260814-071` preserves those exact
  root/intermediate/output/receipt and ordinary results but rejects M4.11's
  universal claim. A disposable James case and Root's independent repeat each
  place an exact overlay below a stable proper-parent alias to an independent
  parent. The overlay root and descendants match no mountpoint, so cleanup
  returns success and removes the independent overlay. Both runs preserve the
  source and change visible-overlay and independent-target snapshots. Static
  inspection independently shows `_validate_unmounted_deletion_plan` builds
  its comparison set from only the resolved overlay root and expected
  descendants, not the proper ancestry traversed to reach it. M4.13 is limited
  to adding the relevant traversed ancestry while retaining an ordinary-
  cleanup positive control and every accepted baseline.
  `EXP-20260814-072` now completes that worker correction. Mountinfo records
  retain mount ID, device, filesystem root, and mountpoint; exact planned paths
  keep unconditional refusal, while proper ancestry rejects only a newer mount
  whose filesystem root is already visible through an older same-device record
  at a different path. The exact proper-parent case refuses before overlay
  content traversal/unlink with visible-overlay/source/independent-target
  snapshots unchanged. A pure classification matrix preserves normal root,
  `/home`, `/tmp`, and same-path nested filesystem mounts while recognizing
  subdirectory and whole-root aliases. All five private namespace cases,
  focused/full 101/289, and six local cycles pass. This was worker evidence
  pending independent M4.14, not a general mount-ownership claim. The guard
  deliberately fails closed when Linux mountinfo cannot be trusted;
  independent `EXP-20260814-073` preserves the uncovered proper-parent alias
  refusal and every retained baseline but rejects the ordinary-ancestry claim
  for one stable stacked topology. A lower bind alias covered at the identical
  pathname by a distinct ordinary top filesystem remains classified, because
  `_mount_alias_points` examines the hidden lower record and reduces its result
  to the shared path. Valid removal on the visible ordinary filesystem refuses
  unchanged. Exact M4.15 is limited to excluding covered lower records using
  the retained mountinfo stack/parent relation while preserving every prior
  refusal and positive control;
  `EXP-20260814-074` now supplies that worker correction. A lower record is
  excluded only when a same-mountpoint covering record names it through
  `parent_id`, and both candidate and source alias comparisons use only the
  resulting visible records. The exact lower-bind/upper-`tmpfs` overlay removes
  completely, the visible parent returns to its pre-overlay snapshot, and the
  source/hidden target remain exact. The uncovered proper-parent alias plus
  all four exact root/descendant mounts still refuse unchanged. Pure controls
  also cover a hidden source record, and the focused/full/local gates pass
  102/290/6. Independent `EXP-20260814-075` preserves those exact results,
  two-/multi-level stack order, hidden candidate/source and visible top alias
  controls, all six namespace cases, 15 fail-closed parser/read cases, ordinary
  removal 32/32, composition 17/17, topology/schema/receipt 33/33, and all six
  local cycles. It nevertheless rejects M4.16 with one uncovered-alias
  falsification: a newer bind reused freed numeric mount ID 1081 while its
  still-mounted source held ID 1082. `_mount_alias_points` treated numeric ID
  order as age, omitted the alias, and removal succeeded through it, changing
  the independent target, alias, and overlay snapshots while preserving the
  source work copy. M4.17 is limited to removing that numeric-ID-as-age
  dependence or failing closed on the exact ambiguity while retaining M4.15;
  `EXP-20260814-076` now supplies that worker correction. Current Linux
  `listmount(2)` later-first unique IDs provide explicit ordering and
  `statmount(2)` maps them to legacy ID, parent, and device. The implementation
  bounds and validates both syscall results, requires complete old-ID set and
  metadata agreement with mountinfo, and rereads mountinfo byte-exact before
  use. The exact newer bind reuses the freed numerically lower ID, but now
  refuses before traversal/unlink with source/independent-target/alias/overlay
  snapshots exact. M4.15 covered-stack success and all prior namespace cases
  survive; targeted/focused/full/local gates pass 10/105/293/6. This is worker
  evidence pending M4.18 and remains neither general mount ownership nor
  portability;
  broader platform compatibility is not inferred. Unpredictable permission/
  storage/I/O changes, concurrent races after preflight, staged-tree removal,
  source restoration/deletion, backup/trash/package management, generalized
  transactions, broad dry-run, launch, compatibility, and receipt redesign
  remain outside this result. Independent `EXP-20260814-077` now accepts the
  exact M4.17 boundary. Current x86_64 UAPI/kernel review, eight listmount
  sequence/error attacks, six statmount result/error attacks, empty/duplicate
  old-ID maps, eight mountinfo change/set/metadata attacks, four escapes, 16
  parser failures, and a separately authored old-ID 1081/1082/1081 namespace
  reproduction all support fail-closed pre-traversal behavior. Complete
  source/independent-target/alias/overlay snapshots remain exact; all seven
  tracked namespaces, 120 tuple permutations, 32/17/37 retained selector
  matrices, explicit M1 6/6, focused/full 105/293, and six exact local cycles
  pass. KU-048 is therefore resolved only for authenticated ordinary sparse-
  overlay removal under the stated current-Linux prerequisites. The excluded
  portability, post-preflight race/I/O, transaction, staged/source, package,
  launch, dry-run, and compatibility surfaces are not silently resolved or
  promoted into new unknowns by this audit; exact M4.19 addresses only the
  written versioned-compatibility statement gate.
- **KU-049 (rejected incomplete executable-authority alignment):**
  [[EXP-20260814-078 - Versioned exact M4 compatibility statement]] publishes
  one canonical asset-free v0.1 statement whose five hash entries are
  demonstrated evidence anchors, not a parser allowlist. It names the existing
  schema/format/operation/workflow surface, exact current Fedora/Python host,
  current-x86_64-Linux removal prerequisites, tested Wine/Gamescope baseline,
  fail-closed topology behavior, and seven unsupported families. A strict
  checker cross-checks tracked launcher/manifest/environment/guidance sources;
  18 drift tests and 311 canonical tests pass. Independent
  [[EXP-20260814-079 - Independent M4.19 compatibility-statement hard-truth audit]]
  confirms the statement bytes, anchors, current declarations, 17/17 family
  mutations, direct-drift cases, and nine-read asset-free boundary, but rejects
  M4.20. An effective `OUTPUT_WIDTH=1` following checked
  `OUTPUT_WIDTH=2560` passes alignment; filter, receipt-constant, and
  Environment-row contradictions pass for the same substring-only reason.
  [[EXP-20260814-080 - Unambiguous effective compatibility-authority declarations]]
  now addresses only that M4.21 class at the worker boundary. Ordered shell
  declarations, Python-AST contract extraction, one generated authority row,
  and scoped keyed Markdown declarations reject the exact four cases and
  adjacent ambiguity; 36/329 tests and the exact nine-read boundary pass.
  Fresh-context
  [[EXP-20260814-081 - Independent M4.21 authority-extraction hard-truth audit]]
  rejects M4.22 because the source-aware extraction remains partial. Post-
  validation Bash indexed/compound writes, post-literal command-array writes,
  post-guard game-directory mutation, Python global/validator rebinding, and
  conflicting duplicate tracked-manifest keys all pass while changing or
  ambiguating effective authority. Exact M4.23 is worker-complete in
  [[EXP-20260814-082 - Closed-world machine-authority byte pins]]. Exact same-
  read SHA-256 pins for the launcher, manifest implementation, and three
  tracked manifests now reject all six residual bypass families; direct pins
  pass 5/5, focused/full suites pass 47/340, and the exact statement/nine-read
  asset-free boundary survive. Generated and Markdown sources retain scoped
  declaration checks. Independent
  [[EXP-20260814-083 - Independent M4.23 machine-authority-pin hard-truth audit]]
  accepts that exact boundary after independent five/no-extra reconstruction,
  10/10 predecessor attacks, 5/5 direct and missing-pin cases, 3/3 human-source
  checks, nine reads, and 47/152/340 tests. This resolves only whether the v0.1
  checker is closed against byte drift in those five claimed machine
  authorities; it does not resolve any unlisted hash or general input policy.
  Unlisted hashes, other Windows/Wine/kernel/architecture/
  filesystem configurations, general `.ALL` compatibility, N-way/dependency
  composition, staged/source removal, rollback/package/transaction behavior,
  general dry-run/launch/runtime automation, and input-type hardening remain
  unsupported or outside that correction rather than silently resolved. Exact
  M4.25 selects only the written bounded single-manifest dry-run affected-file/
  record/byte-range report; general dry-run automation remains unknown and
  unsupported.

- **KU-050 (bounded M4.25 report accepted; general dry-run remains unsupported):**
  [[EXP-20260814-084 - Deterministic single-manifest dry-run report]] adds one
  write-free report for an existing single manifest. It uses
  ordinary preparation, reports authored affected paths/records, input/output
  hashes/sizes and half-open ranges, passes 99/161/349 tests, and preserves
  exact filesystem snapshots. Only the independently reproduced manifest-
  implementation pin changed; five-pin/nine-read compatibility survives.
  [[EXP-20260814-085 - Independent M4.25 single-manifest dry-run hard-truth audit]]
  accepts that exact boundary after direct packed-byte reconstruction,
  primary/secondary sequential/no-op and empty/unequal cases, 91 assertions
  across 20 success/failure/workflow cases, zero trapped writes, exact no-
  follow snapshots, 38 compatibility assertions, and all retained gates.
  Composed/N-way dry-run, semantic diff, output simulation, persistence,
  launch/runtime automation, packaging, rollback, transactions, `.ALL`, M2,
  PS1, and general mount policy remain unsupported rather than silently
  resolved. Exact M4.27 completes the joint audit in
  [[EXP-20260814-086 - M4 v0.1 milestone-closure evidence audit]] and rejects
  milestone closure for the separate receipt-sufficiency and clean-copy
  lifecycle gaps below.

- **KU-051 (resolved at the strict current-receipt/component/closure boundary):**
  The ordinary receipt records schema, manifest name, destination path,
  input/output hashes, contiguous applied edit details, and replacement-source
  path/hash where applicable. `EXP-20260814-077` and `EXP-20260814-085` accept
  its deterministic bytes and exact manifest/source-authenticated removal.
  `EXP-20260814-086` therefore leaves the written receipt-sufficiency
  capability open. `EXP-20260814-087` now completes the exact M4.28 worker:
  strict current ordinary bytes reconstruct an equivalent existing-schema
  manifest, `replay` builds a new dedicated sparse root, and
  `remove-receipt` authenticates/removes that exact overlay without the
  original manifest. All current source/hash/guard/path/topology checks and
  complete recomputation remain. But exact independent
  [[EXP-20260814-088 - Independent M4.28 receipt-reconstruction hard-truth audit]]
  rejects acceptance: after the path-component and placement checks but before
  final file acquisition, a checked parent can change into a directory link
  that reaches the same receipt inode at a changed location. The final-file
  descriptor remains exact and the loader accepts 2/2 deterministic fixtures.
  [[EXP-20260814-089 - Component-stable external receipt acquisition]] now
  completes exact M4.30 at the worker boundary. It retains descriptors for the
  root and every lexical parent, acquires every next component relative to the
  retained parent without following links, binds type/device/inode plus final
  file metadata, revalidates placement, and requires an equal second whole-
  chain acquisition before parsing. The exact bypass and adjacent component/
  final-file changes reject, 154/216/404 tests pass, and all six local cycles
  retain prior hashes. Fresh-context
  [[EXP-20260814-090 - Independent M4.30 component-acquisition hard-truth audit]]
  independently retains those acceptance and no-mutation results but returns
  `REJECT`: one injected close error stops chain cleanup, skips every remaining
  descriptor, and reproducibly retains seven or six descriptors.
  [[EXP-20260814-091 - Exception-safe receipt-handle-chain closure]] now
  completes exact M4.32 at the worker boundary: every owned descriptor receives
  one close attempt despite earlier errors, primary failures remain primary,
  cleanup-only errors stop before parsing, indexed deltas return to zero, and
  161/223/411 tests plus six local cycles pass. Fresh-context
  [[EXP-20260814-092 - Independent M4.32 receipt-chain-closure hard-truth audit]]
  returns `ACCEPT`: it reproduces the parent +7/+6 defect, then passes 28/28
  fresh indexed partial/nested-chain cases with exact close order and one-
  attempt multiplicity, zero real descriptor deltas, exact primary errors,
  parse/source-preparation exclusion, snapshots, CLI silence, all six local
  cycles, five pins, and nine reads. This resolves receipt sufficiency only for
  the strict current schemas, exact-source recomputation, component-stable
  external input, and exhaustive owned-handle closure demonstrated here.
  Authorship, universal reorder detection, migration, embedded output bytes,
  package/transaction semantics, staged-tree removal, and weaker checks remain
  unsupported.

- **KU-052 (resolved: manifest-driven clean-derived-copy lifecycle):**
  Separate accepted evidence covers staged/sparse installation and validation,
  manual runtime launch of modified derived copies, and authenticated sparse-
  overlay removal. No accepted experiment takes the same tool-created
  installation through all four written verbs. Current staged examples live
  below `work/mod-builds/` while the pinned launcher accepts only
  `work/copies/`; staged trees are complete launch inputs but deliberately
  non-removable, and removable sparse overlays are not complete game
  directories. `EXP-20260814-086` leaves this exit gate open, and
  `EXP-20260814-087` explicitly does not address it.
  `EXP-20260814-088` rejects receipt acceptance and therefore does not select
  this lifecycle packet. `EXP-20260814-089` is only the M4.30 worker and also
  does not select it. `EXP-20260814-090` rejects descriptor cleanup and selects
  only exact M4.32, so the lifecycle remains unselected. `EXP-20260814-091` is
  only the M4.32 worker and also does not select it.
  `EXP-20260814-092` accepts that closure and activates only exact M4.34, the
  audit-only clean-derived-copy lifecycle feasibility packet. This unknown and
  M4 remain open pending its same-tree four-verb ledger; no general launch/
  runtime automation or staged-tree deletion is inferred.
  `EXP-20260814-093` completes that ledger and returns `REJECT`. Both complete
  outputs (`stage` and forced apply into a clean copy) preserve the executable,
  exact output, and ordinary receipt and can sit below the launcher's accepted
  `work/copies/` boundary, but dedicated sparse removal rejects their required
  unrelated files before mutation. Both removable outputs (sparse apply and
  receipt replay) lack the executable and complete game tree. Therefore the
  unknown is narrowed to one missing operation: exact manifest/source-
  authenticated restoration of a complete `stage`-produced tree. M4.35 is
  active on that join only; this does not authorize sparse-removal weakening,
  whole-tree deletion, external-receipt restoration, package/backup/rollback/
  transaction behavior, launch automation, or M4 closure at the worker edge.
  `EXP-20260814-094` completes exact M4.35 at the worker boundary. The new
  manifest-driven restore path authenticates complete regular single-link
  source/game path/type/content equivalence except for exact outputs/receipt,
  preflights mounts over every expected game path, and restores only recorded
  destinations. Twenty-seven focused instances, 188/250/438 suites, four
  private mount cases, six retained sparse local cycles, and one exact 722-file
  stage/launcher-dry-run/restore lifecycle pass. This does not resolve the
  unknown: fresh-context M4.36 must independently accept the joined lifecycle.
  The versioned statement also remains conservatively unchanged at the worker
  edge and requires a separate alignment packet after behavioral acceptance.
  `EXP-20260814-095` returns `REJECT` despite retaining the exact local
  lifecycle and every adjacent gate. Complete-tree inventory compares exact
  Linux spellings and accepts both `Case.bin` and `case.bin`; the staged game
  then restores successfully although those paths collide under the project's
  Windows-path model. This unknown remains open on exact M4.37's sole
  correction: reject case-insensitive complete-tree path collisions before
  mount traversal or mutation. Statement alignment is not yet selected.
  `EXP-20260814-096` completes that correction at the worker boundary. A
  shared complete-tree inventory key now rejects all eight source/game
  file/file, directory/directory, file/directory, and nested collision cases
  with exact snapshots and pre-read/pre-mutation traps; two uppercase-first
  directory cases also stop before branch descent; 198/260/448 tests, the
  exact 722-file lifecycle, and six sparse local cycles pass. This does not
  resolve the unknown until fresh-context M4.38 independently accepts the
  joined lifecycle. The unchanged statement still requires a separate
  alignment packet after behavioral acceptance.
  `EXP-20260814-097` independently returns `ACCEPT`. The exact parent
  `7180e4a7...726d20b3d` again accepts `Case.bin`/`case.bin`; immutable M4.37
  worker `8e73a7f5...2d643039` rejects 36 fresh source/game collision cases and
  four bind-mounted colliding-directory order cases with exact snapshots and
  sequencing traps. All eight namespace families, five identity swaps, the
  exact 722-file launcher-dry-run lifecycle, six sparse cycles, five pins/nine
  reads, and 198/260/448 tests pass. This resolves the unknown only for the
  demonstrated current-x86_64-Linux exact-source manifest-driven `stage` ->
  launcher `--dry-run` -> `restore` lifecycle on the same complete derived
  tree. It does not establish game execution automation, external-receipt
  full-tree restoration, staged-tree/source deletion, provenance, POSIX
  metadata equality, backup, rollback, package, transaction, or post-preflight
  concurrency. M4.38 therefore selected exact M4.39 because v0.1 still
  declared restoration unsupported.
  `EXP-20260814-098` preserves that resolution boundary while publishing strict
  v0.2 at the worker edge. It adds only manifest/source-authenticated complete-
  tree restoration on the demonstrated current-x86_64-Linux scope and retains
  every excluded deletion, external-receipt full-tree restoration, platform/
  filesystem, provenance, POSIX-metadata, transaction, automation, Windows-
  path, and concurrency claim as unsupported. This does not reopen `KU-052`.
  `EXP-20260814-099` independently retains that truth boundary but rejects M4
  closure because the selected statement paths accept the complete opposite
  version, reordered object fields pass, and malformed IDs can escape the
  declared error path. Those are compatibility-checker strictness defects, not
  new lifecycle unknowns. M4 remains active only on exact M4.41.
  `EXP-20260814-100` closes those exact checker defects at the worker boundary:
  selected paths require their declared versions, every object key sequence is
  exact, and non-string IDs use `CompatibilityError`; all 151 scalar value and
  151 scalar type attacks reject, both nine-read checks pass, and statement/
  authority bytes remain exact. This still does not reopen `KU-052` or broaden
  its lifecycle boundary. M4 remains active only for independent M4.42's final
  strictness and complete-ledger audit.
  `EXP-20260814-101` retains the resolved lifecycle boundary but returns M4.42
  `REJECT` on compatibility selected-path identity: the default active pathname
  can link to the historical selected file, both expected paths resolve to one
  target, and the checker reports valid v0.1. This is not a new lifecycle
  unknown and does not reopen `KU-051` or `KU-052`. M4 remains active only on
  exact lexical selected-path/regular non-link correction M4.43.
  `EXP-20260814-102` closes that exact checker case at the worker boundary:
  selected identity is lexical, both selected link directions refuse before
  content reads, arbitrary unselected exact links retain existing behavior,
  and 75/288/476 suites pass. This changes no lifecycle unknown.
  [[EXP-20260814-103 - Independent M4.43 selected-path and milestone-closure hard-truth audit]]
  independently accepts that checker boundary after selected nonregular/read-
  timing, alias, unselected-path, exact-contract, pin, and ledger attacks. The
  final compatibility row closes and M4 is Complete at 9/9 capabilities and
  5/5 exit gates, but this creates no new lifecycle conclusion and does not
  widen `KU-051` or `KU-052`: their strict current-receipt and manifest-driven
  current-x86_64-Linux boundaries remain exact. Every broader platform,
  deletion, external-receipt full-tree restoration, provenance, POSIX-metadata,
  packaging, transaction, automation, path-policy, and concurrency question
  remains unsupported or unknown as already recorded.
  [[EXP-20260814-104 - Second independent M4 post-closure verification]] adds
  no resolution or scope expansion. Its hard-link and parent-link cases confirm
  that version bytes remain enforced while only the selected final entry is
  type-gated. General parent-filesystem policy and post-`lstat` concurrency
  remain explicitly unsupported; the bounded M4 closure remains accepted.

## Release unknowns through EXP-20260814-110

- **KU-053 (resolved at the accepted installed lifecycle boundary):** A clean tracked source can
  build the asset-free `ablpc-toolkit-v1.0.0` twice as byte-identical
  378,880-byte canonical tar archives at SHA-256
  `1527281c60d1dd13ad0342a4cef9c8851d882a1cc1301083962f323ed64b62a0`.
  The exact 36-file source tree is
  `423eb946c35b2cc37a2642f9fb69e09304481972529ae63959e18c97dafeada7`;
  strict verification rejects missing, extra, linked, nonregular, forbidden,
  reordered/noncanonical, appended, metadata-drifted, and content-drifted
  archives. On the named Fedora 44/kernel/Python/Wine/Gamescope host, all 21
  PC `LEVEL*.DAT` files and three Training/Level 01/schema-2 complete-stage,
  launcher-dry-run, and exact-restore cases pass with unchanged 747-entry
  source/stage inventories. Those artifact and smoke results survive
  independent `EXP-20260814-106`, but complete installed lifecycle identity
  does not: ordinary installed wrapper use creates five unlisted `.pyc` files;
  linked `releases/` and selected-version roots are accepted; and a dangling
  `state.json` symlink is replaced as though absent. External
  `PYTHONDONTWRITEBYTECODE=1` discriminates the first defect. The next exact
  test is wrapper-level bytecode suppression plus non-following state/root
  admission and full-snapshot regressions. Release reproducibility and
  launcher readiness remain resolved; asset-free toolkit selection/rollback
  remains unresolved until that correction receives independent acceptance.
  `EXP-20260814-107` is worker-complete on that exact discriminator: all four
  installed entry points preserve the full install snapshot without external
  bytecode controls, and dangling state plus linked release/version roots
  reject unchanged across install/current/rollback. Dual 389,120-byte builds,
  source-tree identity, exact smoke, 492 tests, M4, and hygiene gates pass.
  KU-053 remains open only pending fresh-context James reproduction and
  adversarial acceptance; the worker result alone does not resolve it.
  `EXP-20260814-108` rejects that worker result: 20/55 lifecycle cases and 9/10
  adjacent inventory cases expose startup-bytecode, pre-failure topology,
  state hardlink/absence, manifest identity/mode, directory topology/mode, and
  asymmetric retained-version validation defects. `EXP-20260814-109` is
  worker-complete on their combined correction with state schema 2 archive/
  manifest/tree locks, 30 focused/509 canonical tests, matching 399,360-byte
  artifacts, hostile-cache snapshot stability, and exact smoke. At that worker
  edge, KU-053 remained open only for the next independent James verdict.
  `EXP-20260814-110` supplies that verdict: `ACCEPT` after 55/55 lifecycle and
  10/10 installed-inventory refusals preserve complete snapshots, all four
  installed entry points preserve inventory under both cache environments,
  dual artifact/archive/smoke identities reproduce, and all 509-test/M4/Vault/
  hygiene gates pass. KU-053 is resolved for the exact asset-free Fedora/Wine
  launcher-readiness and unsigned local-state-trust boundary.
  It does not establish game execution, automated input, rendered or audio
  output, game-file backup/rollback, Windows behavior, other platforms/
  versions/filesystems, provenance/signing, public distribution, or unlisted
  input compatibility; those remain unsupported or untested rather than
  silently resolved.

## Gameplay unknowns after EXP-20260815-114

- **KU-054 (resolved at retained/displayed `51/50` boundary):**
  `EXP-20260814-111` proves the 51-record table and isolated new pickup.
  `EXP-20260814-112` then proves `49 -> 50` reaches the original exact-50
  event, `50 -> 51` skips that event while retaining 51, and the unmodified
  HUD displays digits `(5,1)`. Its exact reversible three-byte end-tally patch
  retains/displays `51/50`, sets the completion flag, and reaches the bright
  completion/emblem path at animated count 50. The static cap in
  `0x00439E90` was not reached during the Training discriminator and remains
  unidentified rather than a confirmed Training clamp. Resolution does not
  identify the emblem's asset pipeline, redefine the `/50` goal, prove values
  above 51, or generalize the patch to other levels; those surfaces require a
  new concrete goal rather than remaining part of KU-054.

- **KU-055 (resolved for the data-only duplicate-letter boundary):**
  `EXP-20260814-113` proves selectors `0x10`–`0x13` are the four-member
  Training FLIK mask set, that moved copies initialize, and that each duplicate
  can be consumed independently while setting mask bit `1`, `2`, `4`, or `8`
  without consuming its original counterpart. Exact selector-to-visible-glyph
  identity was not separately discriminated. The equality check uses the
  resulting mask rather than the prior transition: with mask already `0x0F`,
  duplicate selector `0x11` retains mask 15 and increments completion/reward
  byte `0x0059D9B0` from 1 to 2. The accepted data recipe therefore has
  repeated-completion behavior. Whether a future authored mod should suppress,
  cap, or redesign that event remains a new executable-behavior goal, not an
  unresolved claim in M3.3.

- **KU-056 (resolved at the exact eight-slot `FLIKFLIK` boundary):**
  `EXP-20260815-114` assigns original Training letter records 50–53 mask bits
  `1/2/4/8` and appended records 63–66 bits `16/32/64/128`. Exact final-hash
  runtime evidence distinguishes the transition: `0x7F -> 0xFF` sets scratch
  byte `0x0086396F` and produces one reward, while a pickup with mask already
  `0xFF` leaves reward unchanged and scratch clear. Centered in-level/tally
  helpers render `FLIKFLIK`; the tally's complete 256-byte popcount table
  reports `8/8`, and the accepted natural tally frame retains `51/50` plus the
  unchanged emblem. This resolves the repeated-completion and presentation
  question for this exact eight-record design only. Arbitrary words, other
  lengths or levels, glyph mapping beyond `FLIK`, persistence/save behavior,
  and new emblem art remain unsupported surfaces, not unfinished M3.4 work.

- **KU-057 (open — natural Level03 row-6 nearest-region selection):**
  `EXP-20260815-116` confirms that exact PC Level03 row 6 is a type-1 signed
  XYZ record at file offset `0x4A4` and that `0x00432930` conditionally scans
  this table, writes selected X/Z shifted left by five, and terrain-recomputes
  Y. `0x0041C8CC` is a static producer of the selector's `0x10` state bit.
  Multiple PC consumers mean type 1 is not a confirmed checkpoint or bespoke
  respawn table. `XPORT-20260815-002` supplies only a bounded PS1-selected
  hypothesis. The exact PC discriminator changes row-6 X by `+128` and
  predicts `+4096` runtime X if selected. `EXP-20260815-129` confirms the
  natural upstream chain at the first grain-gate pit twice: descriptor/value
  `572/1` raises flags `0x14` with `NextLife=2` and selects a row-7-like
  endpoint. The spider is a separate descriptor/value `543/0` death path.
  Remaining: naturally produce material 1 inside row 6's nearest-region and
  apply the existing row-6 source/candidate discriminator, or explicitly
  dispose of that narrower milestone requirement. A negative result must be
  recorded as a contradiction rather than repaired through cross-port naming.

- **KU-058 (resolved at the live-coordinate display boundary):**
  [[EXP-20260815-128 - Live Flik position globals]] uses a controlled visible
  Training jump, ordinary ground movement, and independent static PC
  instructions to confirm current signed Flik XYZ at `0x0059D910`/`14`/`18`.
  The `0x0059D920`/`24`/`28` tuple retains the preceding distinct position in
  the trace. The formerly displayed `0x0059D960`/`64`/`68` tuple stays fixed at
  takeoff throughout the airborne arc and is conservatively an
  auxiliary/reset-coordinate triple. This resolves which addresses the
  coordinate display must read. Exact physics-tick/render-frame cadence,
  coordinate units, and the auxiliary triple's complete update policy remain
  unsupported new surfaces rather than part of the resolved display boundary.

## Presentation unknowns after EXP-20260812-007

- **KU-012:** The exact period-correct texture filtering, display scaling,
  monitor behavior, and WineD3D-versus-Windows rendering differences remain
  unknown. A user-supplied external PC video still, reportedly in hardware
  mode, has a smoother green foreground stem than the brown/green stippled
  native 640×480 Wine capture. The video's build, Windows/GPU/driver state,
  source pixels, scaling, and compression are uncontrolled, so it cannot
  distinguish WineD3D translation from native-driver or capture filtering. A
  matched native-Windows hardware capture is the required discriminator.
- **KU-013 (narrowed by static audit; runtime open):**
  [[EXP-20260816-143 - Automatic Direct3D startup static audit]] proves the
  exact retail executable has no native renderer-selection or chooser-bypass
  argument. The opening chooser defaults to selector 1/software. A first
  whole-chooser bypass is rejected because it omits required shared display
  initialization. The revised paired code/relocation transform in
  [[PC automatic Direct3D startup candidate]] retains setup and cleanup,
  forces local result 2, and skips only the interactive loop; James accepts
  it only as a defensible static candidate. Unknown: fresh runtime behavior,
  actual-surface state, repeat launches, chooser visibility, cleanup, explicit
  hardware-device selection, and host GPU versus llvmpipe. Until those gates
  pass, the launcher deliberately requires manual hardware selection.

## Runtime tooling unknowns

The scripted tools added in `DEC-20260812-019` are live-validated at the
boundaries recorded in `DEC-20260812-020` and [[Runtime Tooling]]. These items
record the remaining environment, perturbation, correlation, and debugger
questions; desired improvements are summarized in
[[Reverse Engineering Capability Gaps]].

- **KU-028 (root cause identified; fix needs one root action):** `rr record`
  cannot capture the Wine 11 run while Wine's in-kernel synchronization driver
  **`ntsync`** is present: Wine issues `ioctl(0x80044e88)` on `anon_inode:ntsync`
  fds that `rr` 5.9.0 does not model, so it FATAL-aborts during Wine init
  (`RUN-RR-20260812-183423`, `DEC-20260812-020`). Confirmed with an
  `ioctl`-logging `LD_PRELOAD` shim showing the fd is `anon_inode:ntsync`;
  `rr record` succeeds on a trivial non-Wine program. This is **not** a GPU or
  disk issue — steering GL/Vulkan to AMD/Mesa and using a tmpfs prefix both
  left it unchanged, and it reproduces with a trivial `wine wineboot`. The Wine
  env toggles `WINENTSYNC=0` and `WINE_DISABLE_FAST_SYNC=1` do not disable
  `ntsync` in this Staging build; no newer `rr` is packaged for Fedora 44.
  `ntsync` is a loadable module (`ntsync.ko`), so the fix is to make
  `/dev/ntsync` absent — `sudo modprobe -r ntsync` (after closing all Wine)
  or an unprivileged `unshare` mount namespace that hides it — after which
  Wine falls back to server-side sync, which `rr` can record. Masking
  `/dev/ntsync` removed the FATAL; the clean Wine fallback needs the device
  truly absent (a `/dev/null` bind lets `open()` succeed and Wine then breaks).
  The `rr-record.sh` wrapper is validated and now refuses when `/dev/ntsync` is
  present. Still to demonstrate end to end: `ntsync` removed → game record →
  `rr replay -a` → replay watchpoint reproduces the plant 10 reads.
  `kernel.perf_event_paranoid` was set to `1` at runtime (see
  [[Environment Status]]).
- **KU-029 (partially resolved):** Freezing the single game PID with `SIGSTOP`,
  capturing a frame via `gamescopectl screenshot`, and resuming works cleanly;
  a re-verification frame was visually confirmed to be the real hardware
  game menu, and the game returns to running (`RUN-FRZ-20260812-183223`).
  RC0-F0-005 independently falsifies X11-root `ffmpeg` as a substitute: its
  live frame and both prior fixture frames are the same uniform black
  `640x480` PNG, not game pixels. The retail RC0 executor remains historical;
  R2c later used `scripts/r2c-f0-auto-hardware.py` with the compositor; that executor is historical
  backend only after exact build, level, timing, and stop-state gates
  (`EXP-20260819-002`).
  Whether the freeze perturbs later game state versus an unfrozen control is
  not yet measured; the phase-locked-vs-free-running comparison against the
  `EXP-20260812-020` variance remains the discriminator.
- **KU-030 (narrowed):** `apitrace --api egl` (not GLX — WineD3D drives GL
  through EGL on this Wayland/XWayland host) captures a valid, `apitrace
  dump`-parseable GL stream with real draws and 2,339 texture uploads
  (`RUN-APITRACE-20260812-184544`). Whether those texture uploads/formats
  expose the brown/green stem stippling of `KU-012` remains to be shown
  against a matched control.
- **KU-031 (narrowed to nearby caller-gate continuation fault):**
  Exploratory `RUN-GDB-20260812-204252` first recorded `SIGSEGV` at hardware-
  breakpoint PC `0x0044D79A` even though its structured result later reported
  cleanup and detach (`EXP-20260812-028`). Fresh
  `RUN-GDB-20260812-211649` then armed the outer gate, `0x0044CA00`, and both
  exact plant 10 watches simultaneously before title advance and reproduced
  the same contradiction (`EXP-20260812-029`). It records one gate stop, raw
  GDB immediately records `SIGSEGV` at that PC, schema 1 continues the signal
  and reports `target_reached`, and Wine reports an unhandled read from
  `FFFFFFFF` at `0x0044D79A` while opening winedbg. A game-only survival frame
  shows the fatal-error dialog. Exact instruction `test al,0x10` has no memory
  operand, so normal execution does not explain the reported read. The broad
  broad non-`SIGINT` continuation branch in harness 1.0 explains the false
  structured status, not the initial fault. `EXP-20260812-030` resolves that
  trustworthiness gap: a synthetic `SIGSEGV` is terminal with signal/PC and
  safe fixture detach, required receipt failure cannot be accepted, routine
  Wine signals still pass, and safe live `RUN-GDB-20260812-214545` reproduces
  the prior watch sequence with five resumed/untraced samples plus live
  gameplay. `EXP-20260812-031` then arms only adjacent same-path
  `0x0044D794` in a fresh unchanged schema-2 run. It records one pre-instruction
  stop followed by structured `SIGSEGV` at that same PC. The arm is rejected,
  its point is deleted, detach succeeds, five samples are state `R` with
  `TracerPid == 0`, and a later game-only frame shows live Training because
  `nopass` suppresses signal delivery. Per M2.18's stop rule, no fresh exact
  arm follows. The independent exact-`0x0044D79A` reproductions plus this
  adjacent result disfavor an explanation confined only to the exact test
  instruction. Root cause remains unknown among nearby-region hardware-
  breakpoint behavior, native GDB, Wine WoW64 continuation, or another
  condition. CAP-001's staged/predicate/register-relative features remain
  open, but this caller-gate region leaves the immediate M2 critical path;
  M2.19 returns to the direct resource-to-rendered outcome instead of adding
  more debugger work.

## 2026-08-15 KU-057 update: natural Level03 reset trigger

The downstream Level03 row-6 consumer is no longer unknown: EXP-116 confirms that `0x00432930` selects the nearest type-1 row and writes row X/Z shifted left by 5. The remaining unknown is upstream and narrower:

- Which natural PC gameplay transition sets actor bit `0x10` at `0x0059D9A0` before `level_done = 2`?
- What controller-only Level03 event reproduces that transition reliably while row 6 is nearest?

Discriminating evidence already obtained: setting `level_done = 2` alone logs `NextLife` but does not reposition; adding bit `0x10` invokes the row consumer and produces the predicted coordinates. Keep KU-057 open until a no-write natural event is captured or the milestone explicitly accepts the forced prerequisite arm. See [[EXP-20260815-116-receipt]].

## 2026-08-15 update - KU-057

Partially resolved by
[[EXP-20260815-117 - Approved Level03 row-6 reset rerun]]:

- Closed: whether the Level03 type-1 row-6 X field causally controls reset X.
  A `+128` DAT edit produced exact runtime delta `+4096` with unchanged Z.
- Open: which natural PC gameplay event produces collision-dispatch result
  `1` / fourth argument `1` at `0x004408EA` -> `0x0041C6C0`.
- Open: whether type-1 rows are user-facing checkpoints, generic reset
  anchors, or another record class.
- Next discriminating experiment: naturally contact one of the loaded
  Level03 collision descriptors with result/material value `1` while a
  row-6-nearest position is active, without debugger writes, and trace the
  resulting flags/NextLife path.

## 2026-08-15 hard-truth disposition - KU-057

The row-6 X/Z causal subclaim is accepted. KU-057 remains open for:

- the natural PC producer of collision-dispatch result/material `1`;
- whether the resulting behavior is semantically a checkpoint;
- whether other rows, levels, and consumers behave equivalently.

## 2026-08-15 update to KU-057

[[EXP-20260815-118 - Natural Level03 material-1 reconnaissance]] reconfirmed live Level03 tag-6/material-1 descriptor entries 570-578 and recorded an ordinary-input red-mushroom route onto the upper corridor. The route ended at `(362499,28410,499117)` with current collision descriptor 552/material 0, `NextLife=0`, and no observed reset-request bit `0x10`. Therefore KU-057 remained open at this point: this run did not identify the natural material-1 producer or checkpoint semantics. Its proposed descriptor-571/black-spider vicinity was later rejected by EXP-129 and its tuple attribution corrected by EXP-131. Retain current descriptor/material, flags, counter, and `NextLife` through recovery. Treat rr as a separate whole-process replay arm.

## 2026-08-15 CAP-002 update to KU-057

[[EXP-20260815-119 - PC input movie recorder and hardware replay]] supplies
the missing bounded PC-native keyboard worker. One exact-window recording and
two fresh replays of a four-event hardware-selector movie agree, dispatch all
events, release all keys, and pass the complete Direct3D/no-software log gate.
This narrows the tooling blocker but does not resolve KU-057: no Level03 user
route or natural material-1 event was recorded, and monotonic input timing is
not internal-frame synchronization. The discriminating experiment remains a
user-recorded route through the then-hypothesized descriptor-571/black-spider-area
contact, replayed in at least two fresh accepted arms alongside the read-only
descriptor/material, flags, counter, and `NextLife` trace. Preserve any route
or state divergence.

## 2026-08-15 companion-controls update to KU-057

[[EXP-20260815-120 - PC input movie companion controls]] removes the manual
PID/display/window-entry burden with a separate exact-session Recording menu.
This reduces a usability blocker only. No live Level03 route, material-1
event, descriptor owner, natural reset producer, or engine-frame source was
observed, and the companion's live discovery has not yet been user-validated.
KU-057 therefore remains open without semantic change. Start its next arm with
the companion, then retain the same two-replay and read-only state-trace gates
recorded above.

## 2026-08-15 first-live replay update to KU-057

[[EXP-20260815-121 - First companion route replay divergence]] confirms that
the first live companion movie is not yet a usable KU-057 route. The accepted
306-event replay reached hardware mode but diverged at Level Select and never
loaded Training, before Level03 or any material-1 state could be observed.
This adds no evidence about the natural reset producer, descriptor 571, or
checkpoint semantics. KU-057 remains unchanged, and its next route must wait
for a shared fresh game-state/log anchor across recording and replay.

## 2026-08-15 anchored-companion update to KU-057

[[EXP-20260815-122 - Anchored companion record and replay controls]] removes
the fixture-level companion blockers identified by EXP-121. Version 1.1.0
defaults record/replay to new bytes containing
`--- Start LevelSelect ---`, exposes backend-confirmed readiness/start states,
preserves recorded post-marker neutral wait, separates saved/next paths, and
retains exact process-group cleanup after leader exit. This is implementation
evidence only. The marker has not yet reproduced Training or Level03 in a fresh
live PC arm, so it is provisional and KU-057 remains open without semantic
change. The next discriminating arm must independently verify the intended
level load before pairing two fresh accepted replays with the read-only
descriptor/material, flags, counter, and `NextLife` trace.

## 2026-08-15 anchored live-replay update to KU-057

[[EXP-20260815-123 - Level Select anchored route gameplay desynchronization]]
accepts the first live shared-marker pair only through Training entry. Fresh
replay dispatches 300/300 events, passes Hardware gates, loads
`gfx\training.raw` and `level07\level1.raw`, and reaches the initial
`NextLife`, but the user observes later gameplay desynchronization. The first
gameplay-looking input follows the second Return release by only 1.338 seconds
while the schedule spans loading/initialization. EXP-123 treated this as a
strong but unmeasured mechanism and proposed a first-post-initialization
`NextLife` anchor. EXP-124 below supersedes that immediate next step. KU-057
remains unchanged.

## 2026-08-15 replay-delivery update to KU-057

[[EXP-20260815-124 - Replay echo identifies target input stream distortion]]
supersedes EXP-123's immediate post-load-anchor recommendation. In the fresh
replay, timestamped `NextLife` precedes the first gameplay `z` by about 954 ms,
so direct loss during loading is not supported. A simultaneous production
observer instead records 304 normalized target events for the 300-event
source, including two inserted `Right` up/down pairs, and multiple 15-39 ms
timing/hold changes. This is confirmed CAP-002 delivery failure, not evidence
about material 1, descriptor ownership, the natural reset producer, or
checkpoint semantics. KU-057 remains unchanged. Correct and echo-validate
delivery before another Level03 route or the deferred phase-anchor test.

## 2026-08-15 persistent-delivery update to KU-057

[[EXP-20260815-125 - Persistent echoed replay and residual gameplay divergence]]
closes EXP-124's measured emitter defect for two fresh arms: both deliver the
same 300/300 target-window events below 0.52 ms maximum delivery drift. Their
gameplay outcomes still disagree, so exact wall-clock keyboard delivery is not
a sufficient KU-057 route contract. This is no evidence about material 1,
descriptor 571 ownership, the natural reset producer, or checkpoint semantics.
KU-057 remains open.

The next KU-057 route must be newly recorded at companion 1.3.0's first fresh
post-initialization `NextLife.` anchor. Require two accepted exact-input
receipts, matching bounded runtime-log/`ROUTINE` checkpoints, and the existing
read-only current descriptor/material, flags, counter, and `NextLife` trace.
Preserve disagreement. Do not convert the old movie, infer engine frames, or
substitute rr without separately satisfying the unchanged `/dev/ntsync`
authorization boundary.

## 2026-08-15 manual-coordinate update to KU-057

[[EXP-20260815-126 - Manual Level03 coordinate-guided probe]] records a fresh
user-driven, no-write control arm. The route reaches the known red mushroom
and upper corridor; its auxiliary/reset-coordinate X/Z comes within about
36,378 units of a scanner tuple later corrected to descriptor 572's base, but
is not current-position evidence. One confirmed raw flag-`0x0002`, counter-
`4 -> 3` transition probably
matches the user's observed health loss, but the health meaning remains
inferred. Current collision value `1`, reset bit `0x10`, and nonzero
`NextLife` each occur zero times. The user stopped before target-height
contact, so this is not route exhaustion and KU-057 remains open.

[[EXP-20260815-127 - Read-only PC coordinate overlay]] removes the researcher's
hidden-coordinate window problem, but its selector-screen smoke did not test
motion and its `0x0059D960` live-coordinate claim is superseded.
[[EXP-20260815-128 - Live Flik position globals]] confirms live XYZ at
`0x0059D910` and corrects overlay 1.2.0. The next user-directed KU-057 arm may
use the corrected in-Gamescope display to steer manually, with a separate
100 ms trace retained as evidence. The overlay does not resolve collision
semantics, provide atomic or engine-frame evidence, or change CAP-002's
still-open deterministic replay boundary.

## 2026-08-15 natural-pit update to KU-057

[[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]] closes
the generic natural-producer subquestion at one bounded PC-native surface.
Two ordinary falls into the single pit revealed by the first grain gate each
captured descriptor/value `572/1`, flags `0x0014`, `NextLife=2`, and the same
first sampled post-reset position `(497247,31299,547255)`. At both contact
samples, authored row 7 was nearer than row 6. Static reads through
`0x004ACF90`, `0x004408EA`, `0x0041C8CC`, and `0x00432930` independently
support the runtime chain.

The same run rejects the prior descriptor-571/black-spider target: the
user-confirmed spider death used descriptor/value `543/0`. EXP-131 later
corrects the tuple in question to descriptor 572's base. The gate was accessed
after one explicitly authorized grain byte write `1 -> 10` at `0x0059D9B1`;
no other target write occurred, and the pit/spider events remained ordinary
input. Do not call retained descriptor tuples geometry centers without layout
proof, and do not repeat this pit for KU-057 because both approaches funnel to
row 7. At this point KU-057 remained open only for a natural material-1
contact inside row 6's nearest-region plus the existing row-6 discriminator,
or an explicit milestone disposition of that remaining requirement.

## 2026-08-15 write-assisted teleport update to KU-057

[[EXP-20260815-130 - Write-assisted Level03 teleport safety boundary]] does
not narrow the remaining natural-event search. The user-authorized arms wrote
position state and therefore cannot establish controller reachability. The
user also corrected a faulty premise: with zero grain, Flik cannot normally
pass the first grain gate to the pit. Teleporting beyond that obstruction is
diagnostic mutation, not a natural death.

The runtime result is still useful for safety. A known walkable row-6 floor
target accepted a current+preceding write, then the engine copied it into the
auxiliary triple about 10 ms later. Equal current+preceding at an unsupported
pit tuple caused the same adoption before a generic descriptor/value `548/0`,
`NextLife=2` loop. Directly writing all three triples to a below-floor point
also looped. Neither arm observed collision value 1.

KU-057 therefore remains exactly where EXP-129 left it: find a different
naturally reachable material-1 surface inside row 6's nearest region, or
explicitly dispose of that remaining milestone requirement. Do not repeat the
single grain-gate pit, use teleportation as natural evidence, or infer that an
unvalidated paused/current-only repair would be safe.

## 2026-08-15 resolution of KU-057 at the M3.5 boundary

[[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]] takes
the explicit-disposition branch and resolves KU-057 as an M3.5 blocker.

The old descriptor-571 target premise contained a concrete instrumentation
error: the EXP-118 scanner began each row at runtime descriptor `+0x10`, so its
printed X/Y/Z belonged to the next descriptor. The tuple
`(471712,64224,537728)` is descriptor 572's base and independently agrees with
the natural first-grain-gate pit; descriptor 571's actual base is
`(470112,64224,-423840)`.

The exact PC `TERRAIN.ALL` source contains nine result-1 regions spatially
paired with all 18 type-1 rows. Descriptor 572 is the only rows-6/7 region.
Its X/Z bounds cross their nearest-row boundary, but both natural EXP-129
contacts lie on the row-7 side, and no distinct row-6-near result-1 descriptor
exists. This supports stopping the route search, not claiming the lower-Z
portion unreachable.

Resolved milestone claims:

- row 6 causally feeds the nearest-row reset consumer under the accepted
  source/candidate discriminator (EXP-117);
- descriptor result 1 naturally reaches the reset-request chain at the first
  pit, selecting row 7 twice (EXP-129);
- no second result-1 descriptor supplies a different row-6 target (EXP-131).

Explicitly unresolved and non-blocking: a controller-only row-6 contact,
user-facing checkpoint semantics, generalization to other rows/levels, and
the complete result-word vocabulary. Reopen KU-057 only if one of those is
promoted into a new bounded milestone requirement or new PC evidence
contradicts this disposition.

## 2026-08-15 M3 worker exit-gate closure claim

[[EXP-20260815-132 - M3 exit-gate reconciliation]] records the worker claim
that M3 closes without silently resolving its retained unknowns. That claim
uses three bounded behavior families, reversible exact recipes, recorded
load/play/failure/restoration scenarios, and the documented DAT-versus-
executable boundary. EXP-133 later rejects independent closure only for the
Training authorization-provenance defect recorded in KU-059 below.

The following remain explicitly unknown and non-blocking for closed M3:

- natural controller-only selection of Level03 row 6 and user-facing semantics
  of the type-1 rows;
- collision result values outside the bounded descriptor-572/result-1 path and
  generalization across levels, rows, or consumers;
- deterministic engine-frame gameplay replay (`CAP-002` remains partial);
- save/persistence effects for the demonstrated gameplay changes;
- generic collectible, word, HUD, trigger, checkpoint, or collision editing;
- whether any demonstrated contract is the right first M5 replacement module.

EXP-132 opened no new KU merely to keep its worker-completed milestone active.
EXP-133 does not promote any semantic item above; it opens only KU-059 because
the evidence-governance defect directly blocks the written first gate.

## 2026-08-15 KU-059 - M3 Training runtime authorization provenance

- **KU-059 (resolved by EXP-135):**
  [[EXP-20260815-133 - Independent M3 closure authorization hard-truth audit]]
  confirms that the cited EXP-111 through EXP-114 durable records disclose
  Training target-state changes and breakpoints but do not record the prior
  explicit approval required by the operating manual. This does not falsify
  their technical observations; it blocks independent milestone acceptance
  under the same rule applied to the first EXP-116 arm.
- **Historical discriminator:** cite a validated durable record of exact prior approval,
  or obtain fresh explicit approval and reproduce one isolated appended-grain
  pickup plus one moved duplicate-letter mask pickup with exact hashes,
  before/after state, survival, and cleanup evidence.
- **Historical stop rule:** do not infer approval, continue from known faulting
  breakpoint sites, alter the accepted recipes or static claims, reopen the
  Level03 packet, or weaken an M3 gate. Resolve KU-059 only after a fresh
  independent closure audit accepts the corrected evidence packet.

### 2026-08-15 worker correction

[[EXP-20260815-134 - Approval-compliant Training runtime receipts]] now
supplies the exact prior-authorization record and two fresh breakpoint-free
runtime arms. One isolated appended-grain entry changes to consumed while
grain changes `0 -> 1`; one moved duplicate-letter entry changes to consumed
while mask changes `0 -> 1`. Exact hashes, comparison-record invariants, 791
read-only samples per arm, zero read failures, `NextLife=0`, target survival,
and scoped cleanup are retained.

The worker could not resolve KU-059 merely by declaring its own authorization
evidence sufficient. [[EXP-20260815-135 - Independent M3 ratchet acceptance audit]]
independently validates the exact prior wording, both raw 791-sample traces,
the byte-identical reviewed helper, isolated transitions, survival/cleanup,
five recipe rebuilds, and all validation gates. KU-059 is resolved only at
that two-arm boundary; the historical EXP-111 through EXP-114 governance
defect is not retroactively erased.

## 2026-08-15 Python/C procedure boundary

[[Python and C reverse-engineering split]] resolves only how the project will
choose an implementation language. It does not claim that any current Python
probe is too slow or that a C helper is needed.

Performance remains unknown per future packet until a representative benchmark
records the requested cadence/budget, latency distribution, missed/partial/
dropped counts, CPU/copy/serialization cost, and target perturbation. A native
ABI requirement can independently select C. Do not open a generic “rewrite in
C” work item without one of those concrete discriminators.

## KU-060 - Modified grain-gate physical transition

- **Status:** effectively resolved. EXP-138 accepted Tunnels row 3 and City
  gate 0; [[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]]
  confirms the remaining gates. Ten of twelve gates (Tunnels rows 0,2,3,5,6,7,8
  and City gates 0,1,2) show the exact closed-at-(min-1)/open-at-(min)
  transition on the modified profile; Tunnels row 1 opens above its
  requirement (exact boundary not isolated); Tunnels row 4 is opened by the
  row-0 coupling and is not independently separable (as EXP-136 predicted).
  The City animation slots activated match EXP-139's static prediction
  (gate 0->2/3, 1->4/5, 2->0/1). A key runtime finding: the game advances its
  logic only while the window is focused ([[PC autonomous game control]]).
  The only residual is an isolated clean one-below pass for row 1 (identical
  mechanism to the seven confirmed rows).
  [[EXP-20260816-149 - Independent modified-threshold completion audit]]
  independently **accepts** EXP-148 with no defects (requirements, open
  semantics, coupling, write boundary, screenshots, and hygiene all
  verified). KU-060 is closed at this boundary.
- **Known:** [[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]]
  proves the corrected Tunnels/City Entrance dispatch mapping, exact retail
  consumers, guarded reversible transform, same-size output identity, and
  configured values resident after both modified PC Direct3D level loads.
- **Accepted result:** [[EXP-20260815-137 - Modified grain-gate threshold behavior]]
  uses the exact profile and accepted PC Direct3D processes. At fixed row-3
  radius, Tunnels remains type `0x10C7`/visibly closed at grain 3 and becomes
  type `0x0690`/visibly open at minimum 4. At one ordinary-proven City trigger
  point, gate 0 remains state `-1`, zero-animation, and visibly closed at
  grain 0; with no movement, minimum 1 drives state/animation to
  `0/-1024/+1024` and visibly opens it. Both retain `NextLife=0`.
- **Write boundary:** the fixed-position comparisons use exact guarded
  current-plus-preceding writes only to already-proven walkable points, then
  one-byte grain changes. They are write-assisted and do not establish
  controller reachability; they are not speculative below-floor targets.
- **Independent audit:** [[EXP-20260815-138 - Independent modified grain-gate threshold audit]]
  accepts only the row-3/gate-0 result after exact raw/helper/profile/static/
  runtime and hygiene review.
- **Remaining:** physical boundaries for Tunnels rows 0–2/4–8 and City gates
  1/2; complete visible Tunnels ordering; and independent presentation of
  linked rows 0/4.
- **Static geometry update:** [[EXP-20260815-139 - Static grain-gate trigger geometry]]
  removes the coordinate unknowns: City gates 1/2 centers/radii are now
  static facts (`(354031,35256)` r=90, `(582271,310212)` r=100), all Tunnels
  rows share one ~25600-unit open radius, and the predicate is byte-pinned
  and cross-checked against the accepted EXP-137 boundary points.
  [[EXP-20260815-140 - Independent static gate geometry and overlay audit]]
  independently accepts that static boundary. What remains open is
  unchanged in kind: visible gate-to-mechanism
  correlation for the unwalked gates, safe walkable approach/Y coordinates,
  and the physical modified-threshold receipts themselves.
- **Standoff update:** [[EXP-20260816-141 - Engine-faithful terrain height and gate standoffs]]
  reimplements the exact terrain height pipeline (validated at four
  accepted receipt points, one exact), pins PC world Y as downward, and
  computes deterministic candidate standoff XYZ for all twelve gates plus
  the two proven runtime points. Candidate walkability and the visible
  correlation still require the guarded live teleport/overlay arms; the
  physical modified-threshold receipts for untested gates remain open.
- **Mapping resolved:** [[EXP-20260816-144 - Runtime grain-gate visual mapping]]
  closes the visible-correlation and standoff-walkability parts. A
  write-assisted teleport pass over the EXP-141 standoffs placed Flik at all
  twelve gates on retail PC Direct3D with `NextLife=0` at every stop
  (so every standoff is walkable) and the engine-exact nearest-gate index
  matching the intended mechanism each time: nine Tunnels wooden-pole gates
  (rows 0–8, "10"/"30" numerals visible on rows 3/6/8) and three City
  Entrance leaf/pillar gates (indices 0–2, states `(-1,-1,-1)`). What still
  remains open is only the **physical modified-threshold receipts** for the
  untested gates (City 1/2 and Tunnels rows other than 3); their confirmed
  approach standoffs now exist. Linked rows 0/4 both present as pole gates
  (req 20) but independent-presentation is still not shown.
  [[EXP-20260816-145 - Independent runtime gate mapping audit]] independently
  accepts that mapping (after correcting two City `dist²` annotations to the
  engine `sar`-8 predicate; no identity or verdict changed).

## KU-061 - Runtime descriptor Z-bounds derivation

- **Status:** open.
- **Known:** the loader bounds pass at `0x004A8A1A` derives tag-6/7/8
  descriptor X/Z boxes from cell fields; for Level03 descriptors 570-578
  the X bounds match EXP-131's group-header table exactly while the Z
  bounds differ (descriptor 570 loader-literal `z_min` 101632 versus the
  table's 98112, with much wider spans). Both derivations are static; the
  EXP-131 table was parser-side and never read from live memory.
  Evidence: [[EXP-20260816-141 - Engine-faithful terrain height and gate standoffs]].
- **Unknown:** the live descriptor `+0x1C/+0x28` values.
- **Discriminating experiment:** one read-only runtime sample of Level03
  descriptor 570's dwords at `0x007F4590 + 570*0x30 + 0x1C/+0x28` after
  level load.
- **Impact boundary:** the box only pre-filters candidates with `+0x2000`
  slack before exact cell tests; EXP-141's four receipt cross-checks
  validate end-to-end outcomes either way.

## KU-062 - Auxiliary query value at the instant of reset selection

- **Status:** open.
- **Known:** `0x00432930` scans type-1 rows using the auxiliary/reset globals
  `0x0059D960`/`0x0059D968`, not the live position triple at `0x0059D910`
  (EXP-20260815-128). The reimplemented selector therefore takes the query as
  an input it cannot derive.
  Evidence: [[EXP-20260816-153 - M5 entry gate and type-1 reset placement resolver]].
- **Unknown:** the exact auxiliary value at the moment the reset-request bit
  `0x10` is honoured. The EXP-20260815-129 sampler captured the current
  position at material contact and the first settled position after the
  write, never the auxiliary triple in between. Both plausible instants — the
  below-floor contact position and the takeoff position — select the same row
  in that trace, so the receipts do not discriminate them.
- **Discriminating experiment:** one read-only sample of
  `0x0059D960`/`64`/`68` at a natural pit contact where the two candidate
  query points fall on opposite sides of a row boundary; Level03's row pairs
  make the near/far boundary at each grain gate a usable place to look.
- **Impact boundary:** the selection contract, the scaling, and the terrain
  relation are unaffected; only the *input* the tool should be given for a
  predictive query is uncertain.

## KU-063 - Which levels use type 1 for reset placement

- **Status:** open (one negative added by runtime capture 2026-08-18).
- **Runtime datapoint (2026-08-18, [[EXP-20260818-003 - Runtime reset and grain-gate captures with the flight recorder]]):**
  a natural death/reset in **Cliffside (internal level 6)** was captured by the
  flight recorder and does **NOT** use the type-1 selector: NextLife `0→2` is
  written by `0x0041c8dc`, Flik`s position is reset by a direct store `0x0042ddf3`
  (`FUN_0042ddb0`), and there is **no writer in the type-1 region
  `0x004328xx–0x004338xx`**. So type-1 reset is not universal — Level06 uses a
  different path. (Consistent with the type-1 role being confirmed only for
  Level03/Tunnels below.)
- **Known:** 14 of 21 retail `LEVEL*.DAT` files carry a type-1 record; seven
  carry none. The loader walk therefore does not write pointer slot
  `0x005C5864` for those seven files, but the accepted level-load path through
  `0x004671D0` first clears the 64-slot table unconditionally at
  `0x00467207`-`0x00467215` before calling the record walk at `0x00467971`
  (EXP-154/155; KU-064). A previous level's type-1 pointer therefore cannot be
  assumed on that path; only a transition that skips `0x004671D0` could retain
  stale state, and no such transition is confirmed. The reset role is
  confirmed only for Level03/Tunnels
  (EXP-20260815-116/117/129/131). Four files contain rows unreachable by this
  selector because a lower index shares their exact X/Z, and in Level04's
  `LEVEL1.DAT`/`LEVEL4.DAT` those duplicates mirror around a pivot into an
  out-and-back sequence — a shape that fits the index-ordered consumers
  (`0x004369B0`, `0x004317D0`) instead.
  Evidence: [[EXP-20260816-153 - M5 entry gate and type-1 reset placement resolver]].
- **Unknown:** whether any level other than Level03 reaches `0x00432930` at
  all, whether any transition can bypass `0x004671D0`, what the seven type-1-
  less levels do on a reset, and which consumer each file's table was authored
  for.
- **Discriminating experiment:** a natural death in one non-Level03 level with
  read-only sampling of the auxiliary triple before and after, compared
  against that file's resolved placements.
- **Impact boundary:** the resolver reports what this selector would do on any
  file; it does not claim the level uses it.

## KU-064 - Type-indexed pointer table state for a level with no such record

- **Status:** open.
- **Known:** `0x0044BB70` writes `0x005C5860 + |type| * 4` only for top records
  that exist in the loaded `LEVEL*.DAT`; seven of the 21 retail files carry no
  type-1 record, so the loader never writes slot `0x005C5864` for them.
  Separately, level-load entry `0x004671D0` contains
  `0x00467207-0x00467215`: `mov ecx,0x40; xor eax,eax; mov edi,0x5C5860;
  rep stosd`, which zeroes all 64 table dwords. A second apparently
  unreferenced copy of that sequence exists at `0x00464F31-0x00464F3D`.
  The delta re-audit adds two facts that narrow this further: the function's
  three prologue branches at `0x004671F2`, `0x004671F7`, and `0x004671FC` all
  converge on `0x00467207`, so the clear is unconditional on every entry; and
  the same function calls the record walk `0x0044BB70` through thunk
  `0x00401D7A` at `0x00467971`. Statically, any load that walks records was
  therefore preceded by the clear in the same invocation, and the only route
  to a stale pointer is a transition that skips `0x004671D0` entirely.
  Evidence: [[EXP-20260816-154 - Independent M5.1 hard-truth audit]],
  [[EXP-20260816-155 - Independent M5.3 delta re-audit]].
- **Unknown:** whether the clear executes on every level load, and therefore
  what a consumer reading `0x005C5864` would find in a level whose data has no
  type-1 record — a zeroed slot, or a pointer left by the previous level.
  `EXP-20260816-153` originally asserted the retained-pointer story without
  evidence; the audit rejected that wording.
- **Discriminating experiment:** one read-only `process_vm_readv` sample of
  `0x005C5864` after loading a level whose file has no type-1 record (for
  example the file backing `LEVEL06`), compared against a sample taken after a
  level that does have one.
- **Impact boundary:** the resolver refuses these files either way, so no
  reported placement depends on the answer; only the explanatory wording did.

## KU-065 - Intermittent single-test failure in the canonical suite

- **Status:** **resolved for the identified node** on 2026-08-17; the identity
  of the four original camera-packet failures remains **open** and is bounded
  below.
- **Resolution (identified node).** The cause is a race in the test
  scaffolding, not in `scripts/input-movie.py`. Three sites in
  `tests/test_input_movie.py` started the recorder or replayer and then slept a
  fixed `time.sleep(0.12)` before appending the anchor line to the log. The
  unordered pair is that sleep against the child reaching
  `LogMilestone.__init__`'s baseline snapshot `self.start_offset =
  path.stat().st_size` (`scripts/input-movie.py:885`). When the append landed
  first, the marker was absorbed into the "old bytes" the tool is required to
  ignore, and the anchor timed out — which is exactly what the test's own name
  asserts must happen to pre-snapshot bytes.
  The product was audited and left unchanged: `armed` is emitted *after* the
  snapshot in both paths (`input-movie.py:1089-1097` record,
  `1748-1756` replay), and `LogMilestone.poll()` re-reads everything from
  `read_offset` to current size on every 10 ms poll, so no marker written after
  the snapshot can be missed.
  Direct measurement over 70 instrumented launches: the child reaches `armed`
  at a median of **104 ms** idle (min 101, max 111) and **120-164 ms** under
  12-worker CPU load. The test was betting 120 ms against a 104 ms median — a
  ~16 ms margin, which vanishes under load.
  The fix makes the ordering deterministic rather than lengthening the sleep:
  each invocation gets its own `--status-fd` pipe and the test appends the
  anchor line only after observing the tool's own `armed` transition. All three
  sites were fixed, including the mismatched-checkpoint replay that had no
  `--status-fd` at all.
- **Before/after evidence**, isolated node, one direct raw redirect per run,
  no live filter: idle 60 runs **59 pass / 1 fail → 60 pass / 0 fail**; under
  12-worker load 20 runs **0 pass / 20 fail → 20 pass / 0 fail**. Both
  historically recorded phases (recording-anchor and replay-anchor) reproduced
  and both fixed. Raw logs and their SHA-256 manifests are retained in ignored
  work-copy evidence.
- **Consequence for gate reporting:** suite results no longer need the KU-065
  qualification for this node. Every previously qualified denominator stays as
  recorded; nothing is retroactively upgraded.
- **Prior status:** open.
- **Known:** during the 2026-08-16 camera packet, `make check` reported
  `1 failed, 647 passed` on four consecutive invocations, then returned
  `648 passed` on twelve subsequent runs (six via `make check` with output
  redirected to a file, two bare `pytest`, one piped through `cat`, and three
  more `make check`). The failing test's name was **not captured**: the
  invocations that failed filtered pytest's output through `grep`/`sed`, so
  the `FAILED` line was discarded; no failure was durably identified in that
  packet.
  Evidence: [[EXP-20260816-161 - PC camera static reconnaissance]].
  [[EXP-20260816-163 - KU-065 canonical-suite reproduction follow-up]] then
  retained every invocation directly to a raw log and found no failure in 13
  canonical host full-suite runs (`13 * 648 = 8,424` executions), 100 complete
  `tests/test_manifest.py` runs (`100 * 198 = 19,800` executions), or 200
  focused system-state runs (`200 * 17 = 3,400` executions). The final broad
  process audit found 32 pre-existing baseline-prefix `winedevice.exe`
  processes (PIDs `68248`-`344284`, parent user systemd PID `1927`) but no
  game, Gamescope, `wineserver`, pytest, or debugger target. Because those
  PIDs predated EXP-163 and were not recorded as owned at launch, they were
  not terminated. The raw-log SHA-256 manifest is `e60f1ff3...63b1e` in
  ignored work-copy evidence.
- **New recurrence:** during the independent M5.6 audit of exact clean subject
  `3504f6a`, one unredirected canonical `make check` produced
  `1 failed, 647 passed in 19.47s` at
  `tests/test_input_movie.py::test_log_anchor_uses_only_new_log_bytes`.
  At `tests/test_input_movie.py:659`, the mismatched replay returned `3` with
  `reason: "anchor_timeout"` and marker/detail `NextLife.` instead of expected
  return `1`; the isolated node then passed `1 passed in 1.68s`. The auditor
  failed to retain the canonical or isolated output to raw files, so no
  byte-exact log or hash exists. This identifies **one** exact-signature
  intermittent failure, not the identity of the four earlier lost failures.
  Evidence: [[EXP-20260816-167 - Independent M5.6 hard-truth audit]].
- **Retained reproduction and identification:** M5.7's first final-subject
  canonical `make check` reproduced exact node
  `tests/test_input_movie.py::test_log_anchor_uses_only_new_log_bytes` as
  `1 failed, 681 passed in 19.51s`. The first replay returned 3 with
  `reason: "anchor_timeout"` / detail `NextLife.` instead of return 0 at
  `tests/test_input_movie.py:610`. Raw unfiltered log SHA-256:
  `9bff94a3e1cce933b4ada34bc07831d1ae61d3033548ea9f53c7c62268176668`.
  Twenty immediately following isolated invocations, each directly redirected
  to a distinct raw log, produced 15 pass / 5 fail. Four failures timed out
  before recording began (“recording anchor was not reached with neutral
  input”); one timed out at the first replay with detail `NextLife.`. Status
  SHA-256 `b80db9e7...93f2f2`; 20-log manifest SHA-256
  `8ceb0d67...7a805`. One canonical retry then passed 682/682, raw-log SHA-256
  `2ef783dd...77f2`. Evidence:
  [[EXP-20260816-170 - M5.7 grain-gate opening resolver]]. This identifies a
  reproducible current flaky node and two timeout phases without proving the
  identity of the four earlier lost camera-packet failures.
- **Third independent recurrence, on a fresh auditor's first invocation:**
  during the creature-census audit at exact clean subject `de7b80d`, the
  auditor's **first** `make test` returned `685 passed, 1 failed` of 686,
  return code 3, at the same node
  `tests/test_input_movie.py::test_log_anchor_uses_only_new_log_bytes` with
  the same `{"reason": "anchor_timeout", "detail": "NextLife.",
  "refused": true, "tool": "input-movie"}` signature. The immediately
  following invocation returned `686 passed in 18.53s`. That packet changed
  **no code and no fixture** — only Vault markdown and one static export — and
  no Wine, Gamescope, or game session preceded it in that context. Evidence:
  [[EXP-20260816-173 - Independent creature census audit]]. This is the third
  recorded appearance of the same exact node and signature, and it further
  supports the node being genuinely intermittent rather than tied to a
  particular packet's changes; it still does not identify the four lost
  camera-packet failures or the timing cause.
- **Fourth independent recurrence, and one false gate report:** during the
  input-census correction pass at `2026-08-17`, `make test` returned
  `1 failed, 685 passed` at the same node
  `tests/test_input_movie.py::test_log_anchor_uses_only_new_log_bytes`, with
  the same `{"reason": "anchor_timeout", "detail": "NextLife.",
  "refused": true, "tool": "input-movie"}` signature, asserting
  `mismatched_replay.returncode == 1` where the return was `3`
  (`tests/test_input_movie.py:659`). Two immediately following runs returned
  `686 passed`. That packet changed **no code and no fixture** — only Vault
  markdown and one static export.
  Recorded separately because of how it was found: the commit
  `102de05` was written asserting "canonical suite 686 passed" **before the
  run had been checked**, and the run had in fact failed. The message was
  corrected by amendment and the episode is kept here rather than smoothed,
  because asserting a gate result without reading it is the same class of error
  as asserting that corrections landed without verifying them. See
  [[EXP-20260817-182 - Independent input census audit]].
- **Fifth recurrence, exhibiting the other timeout phase:** during the second
  input-census correction pass at `2026-08-17`, three consecutive `make test`
  runs gave `1 failed, 685 passed` / `686 passed` / `686 passed`. The failure
  was the same node, but with the **recording-anchor** detail rather than the
  replay one: `{"detail": "recording anchor was not reached with neutral
  input", "reason": "anchor_timeout", "refused": true, "tool":
  "input-movie"}`. That is the phase `EXP-20260816-170` recorded for four of
  its five isolated failures, and this is the first time it has appeared in a
  canonical suite run outside that packet. The packet changed no code and no
  fixture. Raw log retained in ignored work-copy evidence, SHA-256 prefix
  `73ba084eee0a4225`.
- **Unknown:** whether the earlier four failures were this input-movie node,
  which test(s) failed in those runs, and the underlying timing/scheduling
  cause of the now-reproduced node. The
  packet that first observed it changed only Vault markdown — no code, no
  fixtures — so it cannot have introduced the failure, and the suite is not
  otherwise known to be order-dependent.
  The plausible candidates are the tests that touch system state rather than
  pure logic: the M4 mount-namespace family (private namespaces, bind mounts)
  and the receipt-chain descriptor-delta tests, both sensitive to contention.
  The failures occurred in a window shortly after a Gamescope/Wine runtime
  session and several heavy scanning processes. EXP-163's passing runs show
  that a residual background of stale Wine device helpers alone does not make
  the failure immediately reproducible. One separately labelled
  constrained-sandbox full run failed nine tests, including
  `tests/test_manifest.py::test_cli_receipt_cleanup_error_is_silent_and_closes_every_descriptor`:
  its process-global descriptor count fell `15 -> 14` during the test. That
  case passed in every canonical and focused run, and the sandbox signature
  (`9 failed, 639 passed`) is not the lost signature, so it is only an
  **Inferred candidate**, not the identified KU-065 test.
- **Discriminating experiment:** the exact input-movie node now reproduces
  without a preceding Wine/Gamescope session, so no game launch is needed.
  Instrument only its synthetic child/tool timing around process start, log
  baseline establishment, anchor polling, the fixed 120 ms test append, and
  replay start; retain child/tool stdout/stderr and monotonic timestamps for
  one passing and each failing phase. Then replace timing inference with a
  bounded cause and regression fix. Every pytest invocation must still use a
  distinct direct raw redirect (`pytest -q ... > run-N.log 2>&1`), never a
  live filter. If the separate descriptor candidate recurs, capture
  `/proc/self/fd` identities around its final assertion.
- **Impact boundary:** no accepted pre-M5.7 result depends on it; the original
  packets changed only Vault markdown. M5.7 changes no input-movie source or
  test, but its repository gate is still qualified by the reproduced failure.
  A suite that intermittently reports a failure cannot be cited as an
  unqualified gate. Passing runs may be reported only
  with their exact denominator and EXP-163/KU-065 qualification until the
  current node's cause is fixed and the earlier lost-run identity is honestly
  bounded. M5.7's directly retained retry is `682 passed in 18.36s` with
  raw-log SHA-256
  `2ef783dd1bdd272b7dce8c117e575d745f8007c69f605f129d758b070be677f2`
  ([[EXP-20260816-170 - M5.7 grain-gate opening resolver]]); it carries this
  qualification and does not close KU-065.
  The final fresh M5.8 re-audit likewise passes 686/686 with direct raw-log
  SHA-256
  `b1e9a4737585160dd7037b79bcc9511b198904f4c2b2302a1456403348bc713f`
  ([[EXP-20260816-171 - Independent M5.8 grain-gate resolver audits]]). That
  independently accepted denominator remains qualified; it does not identify
  the earlier four lost failures or resolve the current node's timing cause.

## KU-066 - PC camera-source semantics and manual controls

- **Status:** open.
- **Known:** exact PC instructions establish a Flik-relative position/
  orientation updater at `0x0041ADF0`, a bit-0 selector on `0x0059A5EE`
  copying either `0x0059DD90`/`0x0059DDA8` or
  `0x0059A5C0`/`0x0059A5E4` into common block `0x00599C90` at
  `0x0041B8C0`-`0x0041B966`, and consumer `0x00455710` producing origin
  `0x005BDB8C` plus matrix `0x005B58E0`. Renderer `0x0044D430` consumes the
  matrix at `0x0044D4C1` and the origin/matrix copy at `0x0044D4F0`.
  Evidence:
  [[EXP-20260816-164 - PC view-chain correction and coverage reclassification]],
  [[EXP-20260816-165 - Independent PC view-chain correction audit]], and
  [[PC camera view-transform chain]].
- **Confirmed bounded addition:** EXP-20260915-005 binds the alternate source
  and selector bit to a native telescope tour, followed by ordinary Flik-follow
  return, using retail static evidence, original-x86 replay and hardware input.
  Other source uses remain unclassified.
- **Unknown:** selector/source meanings beyond that telescope event;
  whether PC has an unused or undiscovered manual-camera input path; the role
  of the local-block `0x0043D486 -> 0x00455710` call; and the update frequency
  and visual effect of each path.
- **Remaining discriminating experiment:** sample another scripted event
  at a synchronous boundary (the telescope event is covered) to compare `0x0059A5EE`, both source blocks, common
  `0x00599C90`, and output matrix `0x005B58E0`. Separately trace the
  per-frame DirectInput state consumers before concluding whether a manual
  camera path exists. No target write or PS1 promotion is needed.
- **Impact boundary:** the structural view-transform anchor supports Bounded
  Camera coverage without these answers. Do not assign gameplay/setpiece
  function or field names, claim player controls absent, or call the manual-
  controls discrepancy a port difference until PC evidence discriminates it.

## KU-067 - Meaning and consumers of the City gate-0 byte write

- **Status:** open (runtime context added 2026-08-18).
- **Runtime datapoint (2026-08-18, [[EXP-20260818-003 - Runtime reset and grain-gate captures with the flight recorder]]):**
  a live Level03/Tunnels session narrowed the grain-gate globals. **Static-confirmed
  (objdump):** the grain-gate loop reads the grain count at `0x00432f0c`
  (`mov cl,BYTE PTR ds:0x59d9b1; cmp ecx,threshold` against `0x004DA9D0[gate*4]`),
  so `0x0059D9B1` is the operative grain byte; `0x00417d8d` (`FUN_00417720`) writes
  it; `FUN_0042e5c0` writes the flags `0x00599C68/69/6A` at `0x0042e838/83e/844`
  (`mov [flag],bl`); and the gate-open path writes the flag at `0x00433807`
  (`mov BYTE PTR ds:0x599c69,0x1`). **Runtime-confirmed:** an authorized write of
  `0x0059D9B1`→10 made the HUD read 10 and opened the gate (so that byte is the
  grain count the game uses). **Observed live but NOT in the committed trace** (a
  truncated final dump evicted the load-time writes): the grain chain `0→…→4`, the
  flags being 0 at init, and the level index = 3. A narrow-range re-run would
  retain them and the `0x00433807` write. Note `0x00599C60` is a *separate* busy
  object-pointer (18 writer EIPs), not a gate flag.
- **Known:** in City gate routine `0x00433790`, a qualifying opening writes
  state `0x20` at `0x004337EF`; after `test esi,esi` at `0x00433803`, index 0
  additionally executes `mov byte [0x00599C69],1` at `0x00433807` (file
  `0x00032C07`). This is a Confirmed direct branch-local mutation in exact
  retail SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
  Evidence: [[EXP-20260816-167 - Independent M5.6 hard-truth audit]] and
  [[EXP-20260816-168 - M5.6.1 claim and contract correction]].
- **Unknown:** the byte's semantic role, lifetime, readers, and whether any
  called opening helper also changes it. No field or feature name is licensed.
- **Discriminating experiment:** first perform a bounded static writer/reader
  census for exact address `0x00599C69`; only if purpose still matters should a
  separately authorized read-only City trace observe the byte across gate-0
  opening and later level state. No target write or cross-port evidence is
  needed.
- **Impact boundary:** the resolver can emit the address-named write
  as part of its direct opening plan without knowing its meaning. The M5.7
  worker now emits exactly
  `write_u8(address=0x00599C69, value=1, instruction=0x00433807)` for index 0
  only and labels the target `address_0x00599C69`; see
  [[EXP-20260816-170 - M5.7 grain-gate opening resolver]]. That worker remains
  pending fresh-context audit. It does not claim to replace callee effects or
  a broader City update contract, and implementation does not resolve this
  unknown.

## KU-068 - Runtime behaviour of the creature script program counter

- **Status:** open.
- **Known:** in exact retail SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`,
  interpreter `0x0041DC60` loads a program counter from pool slot `+0x70`,
  fetches signed 16-bit opcodes, dispatches through the 26-entry table at
  `0x0041E848`, and stores the counter back at `0x0041E147`. Forty programs
  occupy `[0x004C7D00, 0x004C83F0)` behind the 40-entry pointer table at
  `0x004C83F0`, and all 40 decode with zero misalignment and no off-boundary
  branch target. Unrelated code at `0x004372A8` writes script-33 offset `0x1A`
  into slot 2's `+0x70`, landing exactly on a decoded instruction. The pool
  build at `0x004679A0` is skipped when bit `0x10` of `0x005C5E88` is set.
  Evidence:
  [[EXP-20260816-172 - PC creature actor pool and behaviour VM census]].
- **Unknown:** whether any slot's `+0x70` actually advances through those
  programs while the game runs; which shipped levels build the pool at all;
  and what the five modes selected at `0x0041E14F` do.
- **Discriminating experiment:** with separate authorization, one read-only
  sample of one active slot's `+0x70` and `+0x60` over several seconds on a
  level whose log shows the pool was built, under the six-marker hardware gate
  in [[START HERE]]. Agreement means the sampled values are all decoded
  instruction starts within one program; disagreement falsifies the static
  model. No target write is required.
- **Impact boundary:** the coverage row is **Bounded** on static evidence
  alone. Nothing may cite a runtime creature behaviour, a per-type creature
  identity, or an observed script step until this receipt exists.

## KU-069 - Unbounded table indexes in the creature subsystem

- **Status:** open.
- **Known:** at `0x0041C463`-`0x0041C47D` (file `0x01B863`-`0x01B87D`) the
  builder zero-tests the source type byte and then uses it directly as
  `mov cl,[eax+0x4c881f]` and `mov byte [eax*8+0x599ca8],cl`, with no upper
  bound. The region cleared at `0x0041C432`-`0x0041C43C` is `0x200` bytes at
  `0x00599CA8`, so `type * 8` leaves it for `type >= 64`, and `type = 65`
  writes exactly `0x00599EB0` — the first byte of the source table the loader
  filled at `0x0046574D`. Evidence:
  [[EXP-20260816-172 - PC creature actor pool and behaviour VM census]].
  Three sibling unchecked indexes in the same subsystem were added by
  [[EXP-20260816-173 - Independent creature census audit]] and
  [[EXP-20260817-174 - Second independent creature census audit]]:

  - the slot initializer reads the **40-entry** script pointer table with
    `mov edx,[edx*4+0x4c83f0]` at `0x0041BD45`, where `edx` is the raw source
    `+0x0D` byte, with no bound check — so a byte of 40 or more yields a
    program counter fetched from beyond the table;
  - VM opcode 13 reads the **28-entry** frame-sequence table with
    `mov eax,[eax*4+0x4c8754]` at `0x0041E01A`, where `eax` is the
    sign-extended operand word, likewise unchecked. Opcode 11 is the only
    handler in the interpreter that range-checks its operand;
  - VM opcodes 4 and 10 read the record-type pointer table
    `0x005C5860` with `mov reg,[ecx*4+0x5c5860]` at `0x0041DDD4` and
    `0x0041DEE1`, where `ecx` is the raw source `+0x0E`/`+0x0F` byte. The
    clear at `0x00467207`-`0x00467215` — recorded by `KU-064` and by
    `M2-plant-request-origin-static-trace.md` — zeroes 64 dwords there, which
    bounds the **zeroed region** rather than proving the table's extent; on
    that reading a source byte of 64 or more indexes past it.

  A related open boundary: the extent of the `0x004C881F` byte table is itself
  not established, which is what makes the first index's consequence hard to
  state precisely.
- **Unknown:** whether any shipped `LEVEL.RAW` type-`0x23` packet contains a
  type byte of 64 or more, a `+0x0D` byte of 40 or more, or a `+0x0E`/`+0x0F`
  byte of 64 or more; no PC level file was parsed. The two type switches only *dispatch* on 6..41 and neither of
  them bounds the earlier reads. Whether any shipped script uses an opcode-13
  operand outside 1..24 is answered — none does — but nothing prevents one.
- **Discriminating experiment:** an offline read-only scan of the type-`0x23`
  packet in each retail `LEVEL*.RAW` for the distribution of the `+0x0C`,
  `+0x0D`, `+0x0E` and `+0x0F` bytes. This is metadata-only and needs no
  runtime.
- **Impact boundary:** these are static properties of the original code, not
  defect claims about the shipped game. Any future reimplementation of the
  builder or the interpreter must decide explicitly whether to reproduce or
  refuse each out-of-range index, and say which, per the M5 precedent for the
  type-1 resolver's uninitialised-local case.

## KU-070 - Meaning of the input action bits and the identity of the configuration screen

- **Status:** open.
- **Known:** in exact retail SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`, the
  per-frame read `0x0042EBC0` reduces DirectInput keyboard state at
  `0x00598A10` to one action-bit word at `0x00598B10`, through a twelve-entry
  table over `[0x004D8430, 0x004D8490)` whose defaults are written at runtime
  by `0x0042F0F0`. Joystick buttons share the same mask vocabulary through
  eight pairs at `[0x004D8490, 0x004D84D0)`. The four direction masks
  additionally synthesise `±0x8000` axes into `0x004F0440`/`0x004F0444`.
  Evidence: [[EXP-20260817-181 - PC input subsystem static census]].
  The controls **are** configurable: besides `0x0042F0F0`, two eleven-store
  blocks at `0x00430C3F`-`0x00430CBC` and `0x00431022`-`0x004310A4` write the
  table from a `0x18`-stride byte array at `0x004D9CF9`, `0x00430B10` copies it
  back, and a dispatcher at `0x00430FF6`/`0x00430FFD` selects between applying
  the array and restoring defaults. That was established by the first audit of
  `EXP-20260817-181`, which rejected the packet's original claim that no other
  writer existed. One scoping caveat from the second audit: of the two write
  blocks, only **block B** (`0x00431022`-`0x004310A4`) is demonstrably live, as
  the `je 0x431013` arm of that dispatcher. Block A (`0x00430C3F`-`0x00430CBC`)
  is reached only through thunk `0x00401DF2`, which has zero call sites and
  zero data occurrences, so its reachability is unestablished.
- **Unknown:** what any individual bit of `0x00598B10` means; what consumes it,
  or `0x00598B12`, `0x00598BC0`-`0x00598BC6`, `0x00598B5C`, `0x00598B60` and
  the two synthesised axes; the identity of the configuration screen behind the
  `0x004D9CF9` array; the extents and callers of its three blocks; the layout
  of the `0x18`-stride record beyond its first byte; and why `DIK_RETURN`'s
  slot is excluded from both write blocks.
- **Discriminating experiment:** first static — find the consumers of
  `0x00598B10` and follow one bit. Only if that does not settle it, one
  separately authorized read-only sample of `0x00598B10` while a known key is
  held, under the six-marker hardware gate in [[START HERE]], would bind one
  bit to one key. No target write is required for either.
- **Impact boundary:** the Input coverage row is **Bounded** on static
  evidence alone. Nothing may cite a control name or a runtime input
  observation until this is answered. Any future control-mod work must target
  the `0x004D9CF9` array rather than the live table, which is rewritten from
  three directions.

## KU-071 - Event callback semantics and whether any event is registered outside the two static sites

- **Status:** open.
- **Known:** in exact retail SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`, the event
  table is `[0x005982B0, 0x00598670)` — 16 records of `0x3C` bytes — and each
  record carries an id word at `+0x00`, three native callbacks at `+0x04`
  (**create**, called `0x0042DC2A`), `+0x08` (**unnamed** — no log string
  describes it — called `0x0042D9A5`) and `+0x0C` (**destroy**, called
  `0x0042DB67`/`0x0042DCF6`/`0x0042DAAD`), a name at `+0x10`, and an in-use flag
  at `+0x34`. `create` and `destroy` are the binary's own words, from the log
  strings preceding those calls. Two static registration call sites pass
  `0x004D81A8` (id 2, `"WINDOWS"`) and `0x004D81E8` (id 3, `"DIRECTX"`), at
  `0x0043DAF5` and `0x0043DB10`; whether either executes is not established.
  Evidence:
  [[EXP-20260817-185 - PC event subsystem static census]].
- **Unknown:** what the six callback targets do — `0x004AE580`, `0x004AE780`,
  `0x004AE810` for `"WINDOWS"`, and `0x0042BB30`, `0x0042BB50` for
  `"DIRECTX"` (`0x0042BA60`'s role is prior art from
  `EXP-20260816-159`); whether anything registers an event outside those two
  sites, and so whether slots other than 2 and 3 are ever occupied; the meaning
  of `+0x02`, `+0x30`, `+0x32` and `+0x38`, which are only ever zeroed; what
  `+0x08` is for, which is why it is left unnamed; what `0x005982AC` is for,
  since it is written twice and read nowhere; the width of the name at `+0x10`,
  which is inferred from adjacency; whether an out-of-range id can reach the
  three unchecked `id`-scaled entry points; and the meaning of `0x0059F7F0` in
  the registration sequence.

  Narrowed by the third- and fifth-round audits: the subsystem's only outbound
  **direct** call — the six callback calls are indirect — reaches `0x004ADEA0`,
  which writes the log file `"bugs.log"`. That is confirmed, not inferred: it
  reaches `KERNEL32.dll!DeleteFileA` with the filename through the wrapper
  `0x004B13E0`, one-shot behind `0x004E9170`, before opening in mode `"at"`. Its
  body is gated on `0x008620AC`. Still unknown: the roles of `0x004B0730`,
  `0x004B13A0` and `0x004B04E0`, and what sets `0x008620AC` or `0x004E9170`.
  And nothing outside the seven functions holds an absolute reference to the
  table: all 26,713 type-3 base relocations were
  decoded and the 47 pointing into `[0x005982A0, 0x005986F0)` all lie inside
  `0x0042D950`-`0x0042DD94`. So any unfound registration path must be a computed
  reference, which is what makes the discriminating experiment below the right
  one.
- **Discriminating experiment:** static, and cheap — identify the `"WINDOWS"`
  record's three callbacks, which would say what the event abstraction is for.
  For the registration question, determine whether the register thunk
  `0x004017B2` can be reached by computed dispatch; a scan-based negative is
  exactly what the input census's `GetAsyncKeyState` finding showed can
  mislead. No runtime is required for either.
- **Impact boundary:** the Event/scripting coverage row is **Bounded** on
  static evidence alone. Nothing may cite an event's purpose, a runtime
  registration, or a gameplay trigger role. In particular this subsystem is
  **not** a trigger mechanism: it is a callback registry, and the known
  gameplay-trigger evidence remains the grain-gate family under the separate
  Triggers row.

## KU-072 - Three unidentified creature-VM engine callees

- **Status:** open.
- **Known:** in exact retail SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`, the
  creature behaviour interpreter `0x0041DC60`-`0x0041E845` makes 16 direct calls
  to 15 distinct thunks plus one indirect `call eax` at `0x0041E7C7`. Twelve of
  the fifteen targets appear in authored Vault notes or exports. Evidence:
  [[EXP-20260817-186 - M5 third-module candidacy ranking]].
- **Unknown:** what `0x00464D40`, `0x00403A10` and `0x0041A550` do. They appear
  in no authored Vault note or markdown export.
- **Why it matters:** these three are the reason the creature VM fails M5 entry
  criterion 1 (bounded contract). Identifying them is the concrete step that
  would make the VM a candidate module rather than only a research target.
- **Discriminating experiment:** static and bounded — establish each function's
  extent from its `ret` and padding, enumerate its outbound branches and any
  imports or strings it references, and check `ghidra-evidence.json` for
  existing decompilations **before** analysis, per `DEC-20260817-138`.

## KU-073 - Which variable selects the thrown berry type on PC

- **Status:** RESOLVED for the selector (2026-08-18) — `0x0059D9A7` is the
  equipped berry-type selector, **confirmed causally on the PC**
  ([[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]]).
  Guarded authorized writes to `0x0059D9A7` **changed the thrown berry** (Wine,
  pristine exe, user-observed): `1`=blue/super, `2`=green/homing, `3`=gold,
  `4`=purple/mega-homing (`0`=red/basic default). So it is the **source, not a
  mirror** (`0x0059F500` unchanged) — resolving the two prior unknowns (causal
  role; value→colour). The cross-port shape (PS1 `0x800A6597`, same `−0x0A`
  offset from the grain count, identical `0x23→1` value permutation) is now
  promoted by this independent PC evidence. Still open only: the natural
  pickup-path field semantics beyond the confirmed selector; the `==3`/`==4`
  gates were not separately instrumented (consistent with homing/mega-homing).
- **Known:** in exact retail SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`, the throw
  action bit is `0x8000` (`DIK_LCONTROL`), confirmed at runtime in the raw
  action word `0x00598B10`, the latched current word `0x00861C98` and the
  previous-frame word `0x00861C8C`. A projectile pool with stride `0x38`,
  consistent with 64 records over `[0x00598C00, 0x00599A00)`, is active **only**
  while throwing — 0 dwords active idle, 0 walking, 38 on throw. Evidence:
  [[EXP-20260817-187 - Runtime berry throw reconnaissance]].
- **Static candidate (2026-08-18, Inferred, not confirmed):**
  `candidate_berry_equip_byte` `0x0059D9A7`, written only with the discrete
  values 0-4 by a switch over pickup selector kinds `0x20`-`0x24` in
  `FUN_00417720` (the confirmed pickup path) and `FUN_004292C0`
  (`0x20->0, 0x21->2, 0x22->3, 0x23->1, 0x24->4`, each with a distinct
  `thunk_FUN_00414cc0` id), consumed as the column index of
  `candidate_berry_hit_accumulator` `0x00599B20[row*5 + byte]`
  (`+2` per hit, cap 200, thresholds 100/0x78, decay `-2` above 0x40) in
  `FUN_0041C9B0`/`FUN_0041BD10`/`FUN_004288F0`/`FUN_00429790`, gated `== 3` /
  `== 4` in eight behaviour functions, and mirrored into `0x0059F500` by
  `FUN_00437FD0`. Located by a replay-seeded static search; full record and
  provenance in
  [[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]].
- **Unknown:** which colour each value 0-4 denotes; whether `0x0059D9A7` is
  causally upstream of throw behaviour or itself a mirror; the meaning of the
  `== 3`/`== 4` gates. Ruled out earlier: record field `+0x2C` (rewritten and
  held with no visual change), and `0x0059D918`/`0x0059D928`/`0x0059D968`,
  which are Flik Z coordinates per [[STRUCT-PC-FLIK-POSITION-GLOBALS]], not
  berry state.
- **Why it matters:** it is the entry point to understanding per-type behaviour
  (homing in particular implies target selection), and therefore to any work on
  berry abilities.
- **Discriminating experiment:** first the read-only researcher-labelled A/B —
  the held berry colour named before each read-only sample of `0x0059D9A7`
  (predictions: stable value in {0..4} per colour, pickup transitions per the
  switch, `0x0059F500` mirroring a frame later). Only then, and separately
  authorized under [[Agent Operating Manual#Dynamic analysis]], one
  compare-before-write byte write with revert to prove the byte causally
  upstream. The older pool-record write-watchpoint route remains valid but is
  no longer the cheapest discriminator.
- **Cross-port shape, not evidence:**
  [[XPORT-20260817-005 - Berry contact array and type marker shape]],
  continued by
  [[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]].

## KU-074 - Live semantics of the level-select carousel position counter

- **Status:** open.
- **Known:** the level-select code loads the carousel position from
  `word [0x00599AF8]`, indexes the 16-entry table at `0x004C6A30`, and stores
  the result to the internal level global `0x00861C84`
  (`0x0041475F`-`0x0041476E`). This is static derivation only
  ([[PC level roster and numbering]]).
- **Unknown:** whether `0x00599AF8` reads at runtime as a 16-bit position with
  the update timing that derivation implies — specifically whether it advances
  once per accepted carousel press, and whether it is stable to read between
  presses.
- **2026-08-21 constraint:** P0A-AH-001 falsified the operational assumption
  that its new persistent-X 180 ms Right delivery means one accepted step: it
  loaded internal level07/progression position 10. Static code independently
  shows that the selector tests the live Right bit at `0x00443F54`, increments
  its local position at `0x00443FB3` without a previous-state edge test, and
  writes the confirmed position at `0x004444D6`. Repeated held-state sampling
  on that substituted delivery path is therefore a supported explanation, not
  a proved runtime count or cadence. It does not invalidate the separately
  established direct focused `xdotool` route.
- **2026-08-21 operational correction:** a fresh user-directed PC launch reused
  the established exact direct route after the LevelSelect marker and fixed
  settle: 180 ms Right, one-second gap, 180 ms Return, then final 180 ms
  Return. The log loaded Level01 and reached ClearLoadScreen/InitMainGame/
  NextLife completion; a transient compositor frame visually corroborates
  Anthill gameplay. No process-memory read was needed. This is operational
  reconfirmation, not a frozen counter-semantics experiment.
- **Why it now matters:** [[Session control plane]] reads this counter after
  every carousel press to detect a press dropped between `GetAsyncKeyState`
  polls, which is the EXP-20260816-156 wrong-level failure. If the counter does
  not behave as derived, that detection is unsound even though the final
  acceptance check (the internal level global) remains correct.
- **Discriminating experiment:** in one authorized session, read
  `0x00599AF8` and `0x00861C84` before and after each of three deliberate
  `Right` presses and one `Return`, retaining raw values. Compare the observed
  sequence against the static table. The tool already reports the raw values,
  so this needs no new instrumentation.
- **Impact boundary:** the established direct route and exact Level01 log gate
  permit deterministic navigation without resolving the counter. A read of
  `0x00861C84` remains the stronger loaded-level state confirmation where its
  authorization allows it; per-press counter reads remain useful only for
  dropped-press detection and retry. A no-memory P0B must not inherit the
  stronger state-read claim, but it may use the proved direct route plus exact
  Level01/gameplay log gates.

## KU-075 - Exact log wording of a rejected software-renderer arm

- **Status:** open.
- **Known:** [[START HERE]] requires rejecting an arm that "instead records
  `SYSTEM MEMORY ONLY`, 320x200, or `INITSOFTRENDER`". The first and third are
  verbatim tokens observed in accepted evidence. `INITSOFTRENDER` is confirmed
  by `EXP-20260812-007`/`EXP-20260813-039`.
- **Unknown:** the exact selected-mode wording a software arm emits for
  320x200. [[Session control plane]] implements it as `Screen mode 320x200` and
  `Mode set to 320x200`, derived from the positive 640x480 marker forms rather
  than captured from a software run, and deliberately excludes `DDMODE`
  enumeration lines, which list available modes and are not a reject condition
  ([[PC autonomous game control]]).
- **Discriminating experiment:** capture one complete software-renderer log
  (an ordinary default launch with no chooser input) and record the exact
  selected-mode lines verbatim. This needs no hardware arm and no write.
- **Impact boundary:** the gate is fail-closed on the positive side — all six
  markers must be present — so a wrong reject pattern cannot admit a software
  arm as hardware. It could only fail to add a second, redundant reason for
  rejecting one.

## KU-076 - Cause of the CONVPSXTPAGE8 corrupt-pointer crash under classic Wine

- **Status:** resolved at the environmental boundary — the crash is
  **classic-Wine-9.0-specific**; the same executable and assets load and play the
  level cleanly on **real Win95** (86Box). See the 2026-08-18 resolution below.
- **Known:** under classic 32-bit Wine 9.0 (Ubuntu, in a container), the game
  crashes or hangs loading a level in `FUN_00462c30` (the PSX-tpage→display
  converter, `CONVPSXTPAGE8`): `Unhandled page fault on read access to
  8BA050B8 at address 00462F9D`, immediately after `MEM : SOFT Pixel buffer for
  tpage 0 created`, during `level00\level.raw` load. `0x8BA050B8` is above 2 GB
  — a corrupt/uninitialised pointer, not a memory-size issue. It is intermittent
  (crash vs hang). The same executable and assets run correctly on Wine 11
  (host). Evidence:
  [[2026-08-17 2200 - Claude - rr Wine dead-end and PCem-libTAS pivot]].
- **Inferred:** the corrupt pointer is in the DirectDraw/WineD3D surface path;
  Wine 9.0 provides a surface differently than Wine 11 and the game reads a bad
  pointer. Not confirmed; the exact Wine defect (if it is a Wine defect rather
  than the game relying on Wine-11-accommodated undefined behaviour) is not
  identified.
- **Status label:** **Wine-version-specific, root cause unconfirmed.** Do not
  call it a Wine bug or a game bug without more evidence.
- **Discriminating experiment:** run the same executable and assets under real
  Windows 95 in PCem-st (`DEC-20260817-145`) and exercise the same level load.
  If it passes cleanly there, the failure is strongly environmental (classic
  Wine 9.0), not intrinsic to the game data/code. This is also part of the
  PCem harness's first milestone, so the two goals share one experiment.
- **Impact boundary:** blocks the `rr`-on-classic-Wine path (already abandoned).
  Its resolution is a useful early confirmation for the PCem harness but is not
  on the critical path once PCem determinism is established.
- **Update (2026-08-18):** the real-Win95 substrate now exists —
  [[86Box Win95 RE harness]] — and the game boots to its level-select menu on
  Win95 OSR2 in 86Box. But the CONVPSXTPAGE8 **level load has not been exercised
  yet**: the menu is point-and-click and keyboard could not enter a level in the
  headless container. The direct test is to enter Training and watch the load
  (native launch or an 86Box mouse pass). If it loads cleanly, the crash is
  strongly Wine-9.0-specific. Note the harness is **86Box**, not PCem-st.
- **RESOLVED (2026-08-18) — the level loads and plays cleanly on real Win95.**
  In the 86Box Win95 machine (`abl-win95`, v6.0 gdbstub build), the Training level
  was entered from the menu (mouse click to focus the game window, then `Return`
  selects the carousel item; per [[PC autonomous game control]]) and it loaded to
  full playable 3D gameplay — Flik controllable in the training area, no
  `CONVPSXTPAGE8` page fault, no crash or hang. Evidence: `work/86box/logs/
  lvl_gameplay.png`, `pos_a.png`, `pos_b.png` (Flik + trainer in the rendered
  level). Because the identical `bugs.exe` (sha256 `97c95ba5…`) and assets that
  page-fault in `FUN_00462c30` under classic Wine 9.0 load without fault here, the
  crash is **environmental to classic Wine 9.0**, not intrinsic to the game
  data/code. The exact Wine-9.0 surface/pointer defect is still unidentified (not
  needed — the game's native path is proven correct on real Win95). Cross-ref:
  the live-gameplay memory reads in `KU-077` were taken during this same session.

## KU-077 - Guest-virtual memory access via the 86Box GDB stub (Gate 2)

- **Status:** partly resolved by source/binary evidence; residual tests open.
- **Confirmed (evidence: [[2026-08-17 2330 - Claude - 86Box GDB stub feasibility for guest memory access]]):**
  - The **installed** b9001 AppImage has **no GDB stub**. Direct evidence: empty
    `strings | grep -i gdb` (the `GDB Stub: Listening on port` log string / the
    `gdbstub` symbols would be compiled in if present). The `--help` absence is
    *consistent but not proof* — the stub auto-inits from `machine_init()` (port
    12345), no CLI flag. Corroborated by stable builds shipping `GDBSTUB=OFF`.
    The stub is gated by 86Box's CMake `GDBSTUB` option (default OFF); a source
    build with `-D GDBSTUB=ON` is required.
  - `-D GDBSTUB=ON` forces `DYNAREC=OFF` (disables `NEW_DYNAREC` off ARM64), so
    the build is **interpreter-core, debugger/RE-only** — not evidence about
    determinism or timing vs the normal dynarec build.
  - **Security:** the stub binds `0.0.0.0:12345` (all interfaces, hardcoded
    `INADDR_ANY` at `gdbstub.c` ~L2654). It is a full guest read/write debugger —
    restrict to loopback (host firewall, or a `htonl(INADDR_LOOPBACK)`
    bind-patch) before routine use; **do not expose to the LAN**.
  - With the stub, memory access is **linear/virtual** (`readmembl`/`readmemll`
    /`writemem*l`, `cpl_override=1`, `ABRT_PF`), i.e. paged through the **active
    CR3** — so a read of `0x00861C84` resolves the guest linear address *only
    while the game's address space is current*. Watchpoints Z2/Z3/Z4
    (write/read/access) are supported.
  - The read path uses the normal MMU accessors, which **can set page-table
    A/D bits** in guest RAM; the stub does not use a no-side-effect translate
    path.
- **Open (the Gate-2 tests, once a GDBSTUB build + Win95 + game exist):**
  1. **2B context:** breaking at a known bugs.exe code address puts CR3 in the
     game's space so linear reads resolve — verify, and record CR3.
  2. **2A read/write/watch:** `0x00861C84` and `0x0059D910` read the known
     values in-context; a write is observed by the guest; a write-watch breaks
     on the writing code.
  3. **2C determinism:** does a stub read perturb savestate→inspect→replay
     identity via A/D bits? If yes, patch the stub read to a no-A/D / no-abort
     translate. Measure, don't assume.
  4. Whether the exact release-tag `gdbstub.c` differs from master (confirm
     against the tag actually built), and whether **any** 86Box config is
     deterministic enough to pair the stub with Gate 1 — else 86Box proves the
     mechanism only and PCem-st (or an equivalent host-side reader) carries
     determinism.
- **Discriminating action:** ✅ **built and verified** —
  `tools/86box/86Box-gdbstub-628ce40.AppImage` (commit `628ce40`,
  `GDBSTUB=ON`/`DYNAREC=OFF`, sha256 `7cd47fd1…`). Stub confirmed compiled in
  (strings + symbols) and **listening on `:12345`** with a running machine, and
  the AppImage is portable to the Fedora host. Remaining: install Win95 OSR2 +
  the game in it and run the Gate-2 2A/2B/2C procedure (mind the `mouse_type`
  config gotcha). See the Build record in
  [[2026-08-17 2330 - Claude - 86Box GDB stub feasibility for guest memory access]]
  and [[Decision Log#DEC-20260817-147 - Build a GDBSTUB-enabled 86Box to prove Gate 2 memory access]].

- **Gate-2 first attempt (2026-08-18) — partial success, hard blocker found.**
  Booted `win95_c.img` under the gdbstub build and connected `gdb` to
  `127.0.0.1:12345`. **What works:** the stub connects and exposes the full guest
  register set **including `CR3`, `CR0`–`CR4`, `EFER`, and MMX** — so the Gate-2B
  mechanism (read guest control-registers to know the address-space context) is
  real. The stub also **halts the CPU at the reset vector** (`EIP=0xFFFFFFF0`,
  `CR3=0`) on start and runs only on `continue` — clean debugger control. **The
  blocker:** `GDBSTUB=ON` forces `DYNAREC=OFF`, and the **interpreter core cannot
  get through the 686BX BIOS POST** — on `continue` it runs from reset then halts
  on an *illegal instruction* at `~0xB991/0xBB03` (logged `8B55 (FF)`), an opcode
  the v6.0 **dynarec** build executes fine. So the guest never reaches Win95 or
  the game under the stub, and Gate 2A (read the game's `0x00861C84`/`0x0059D910`)
  could not be exercised. Evidence: `work/86box/logs/gdb_cont.out`, the register
  dump, and two reproductions at the same PC.
- **Implication:** the mechanism is sound but **this stub build is unusable as-is**
  because its interpreter won't boot the reference machine. Next: try a gdbstub
  build from the **v6.0 tag** (the interpreter may differ from master and match the
  working dynarec core), or treat it as a 86Box-interpreter limitation and
  reconsider the memory-access route (PCem's debugger, a custom emulator hook, or
  a non-halting read path). This is the open decision point for the whole
  86Box/PCem Gate-2 direction.
- **Gate 2 RESOLVED via a v6.0 gdbstub build (2026-08-18) — read + write PROVEN.**
  Key insight: **v6.0's `GDBSTUB=ON` does NOT force `DYNAREC=OFF` at the CMake
  level** (v7.0 master does). Built 86Box tag `v6.0`
  (SHA `4fef696a4eead1d55a28d6ac0e5bd2864e5454da`) with `-D GDBSTUB=ON -D SDL2=ON`;
  effective cache `DYNAREC=ON` **and** `GDBSTUB=ON` — the recompiler **and** the
  stub are both compiled. It **boots the reference machine fine** (past the
  `0xBB03` POST instruction that killed the v7.0 build), reaches Win95, and runs
  the game to its menu with the stub attached.
  - **CORRECTION (2026-08-18, source-verified): the stub build runs the
    INTERPRETER at runtime, not the dynarec.** In the v6.0 tree,
    `cpu_exec = exec386_dynarec` is guarded by
    `#if defined(USE_DYNAREC) && !defined(USE_GDBSTUB)` (`src/cpu/cpu.c:1856-1858`),
    so any `GDBSTUB` build **never selects the recompiler loop** — a Pentium falls
    through to `exec386` (`cpu.c:1865`). The compiled-in recompiler
    (`DYNAREC=ON`) is therefore **present but unused**. So v6.0 boots where v7.0
    did not because its **interpreter core** (`exec386`) differs from v7.0's and
    handles the `0xBB03` POST opcode — NOT because it uses dynarec (my earlier
    "with dynarec it boots" wording was wrong). Practical upside: because the
    interpreter routes every guest write through the `mem.c` C accessors that
    carry the watchpoint hook (`GDBSTUB_MEM_ACCESS`, e.g. `mem.c:784/1052/1324`),
    **all writes are observable in software** — there is no dynarec fast-path that
    could bypass a watchpoint or a write-trace. Cost is interpreter speed (runs
    playably, ~118 Hz observed).
  - Results (binary `work/86box/86box-v6-gdbstub`, run in
  `abl-win95`, gdb→`127.0.0.1:12345`):
  - **2B (context):** connect halts the CPU at the reset vector; the stub exposes
    the full register set incl. `CR3`. Breaking with `$pc` in the game code range
    `[0x401000,0x4c0000)` gives `CR3=0x00454000` = the game's process.
  - **2A read — DEFINITIVE (ground truth).** In-context, read 24 bytes at the live
    `$pc=0x0047a039` (RVA `0x7a039`): `81e1ffffff008bc1c1f8104e668b0447668942fe75e58b4c`
    — those exact bytes are in the on-disk retail `bugs.exe`
    (sha256 `97c95ba5…`) at file offset `0x79439` (RVA→raw delta `0xc00`).
    Reproduced at `$pc=0x004111e1` (valid disassembly). The stub reads the game's
    live guest-virtual memory, matched byte-exact to the executable.
  - **2A write — PASS.** Wrote `0x12345678` to `[$esp-0x40]` (`0x00aafbf8`), read
    back `78563412` (LE), restored to `00000000`. Round-trip through guest RAM.
  - **Caveats / still open:** you MUST break with `$pc` in the game range —
    random interrupts often halt in another Win95 process (wrong CR3), where the
    game addresses read `0` or `0xffffffff`. The game's gameplay globals
    (`0x00861C84` level, `0x0059D910` Flik) read `0`/non-resident **at the menu**;
    a *meaningful non-zero* read needs to be IN a level, which needs the
    point-and-click mouse. **Watchpoints** (`Z2/Z3/Z4`) are accepted but firing
    was not cleanly demonstrated. **2C** (A/D side-effect) untested.
  - **CORRECTION (2026-08-18, source-verified): watchpoints are NOT limited to 4,
    and do NOT use the guest's x86 DR0–3 registers.** The stub implements
    write/read/access watchpoints as a **software linked list** of
    `gdbstub_breakpoint_t` nodes (`calloc`-allocated per `Z`, no fixed count) plus
    a **page bitmap** `gdbstub_watch_pages[]`, and the emulator checks each memory
    access against the lists itself (`src/gdbstub.c:142-150, 346-350, 1312-1350,
    1749-1776`). Each watchpoint is a **range** (`addr…end`), not a single
    address. So the real constraint is **per-access checking overhead
    (performance)**, not a hardware-register cap. My earlier "retains DR0–3, they
    exhaust after 4" was a wrong mechanism attribution: the 4-limit I hit is
    almost certainly **stock gdb's own client-side i386 hardware-watchpoint cap**
    (gdb models x86 as 4 debug-register slots for `Z`-packets), NOT the stub.
    *Discriminating test (still open):* set >4 watchpoints via a raw-RSP client
    (or software/`can-use-hw-watchpoints off`) and confirm they all take. Attempted
    in [[EXP-20260818-001 - Watchpoint path and first forensic tuple for Flik position]]
    but **blocked by stub fragility** (below), so the `>4` claim stays source-only.
  - **Watchpoint FIRES — first forensic tuple captured (2026-08-18,
    [[EXP-20260818-001 - Watchpoint path and first forensic tuple for Flik position]]).**
    In-level, a hardware write-watchpoint on `0x0059D910` (Flik X) halted at the
    writer: **`CR3=0x00454000` (ABL, verified match), writer EIP `0x004ab889`
    (`mov [edx],eax`, trap-after `0x004ab88b`), old X `-4378` → new X `-4205`**.
    The writer is one store in a reusable 4-dword vector copy (X,Y,Z,W → `[edx]`,
    `edx=0x0059D910` this frame); runtime disasm matches on-disk `bugs.exe` at
    `0x004ab889` byte-for-byte. The watchpoint **path is proven**. **But** the
    stub is too fragile as a capture transport: it *retains* watchpoints across
    unclean gdb exits (leftover Z2 → "too many"; cleared with a raw `z2` remove),
    emits a **malformed `T` stop-reply** that crashes gdb ≥15 on some hits, and
    gdb`s `continue` is **non-deterministically async** in batch mode — so
    repeat-hit consistency (step 6) and the `>4`-watchpoint test could not run
    cleanly. Implication: a flight-recorder write-trace should be **emulator-side
    C instrumentation** (hook `mem.c` writes), not gdb-watchpoint capture. See
    [[Decision Log#DEC-20260817-147 - Build a GDBSTUB-enabled 86Box to prove Gate 2 memory access]].
- **Fresh James audit (2026-08-18) — READ ACCEPTED, WRITE not reproduced,
  verdict REJECT on the conjunction; stub is fragile.** James independently
  re-derived the PE mapping (`.text` VA `0x401000` raw `0x400` → delta `0xc00`,
  valid only in `.text` `0x401000`–`0x4bf765`) and reproduced the **read** at four
  distinct live PCs (`0x0047a04d`→`0x7944d`, `0x0047ae58`→`0x7a258`,
  `0x0047a049`→`0x79449`, `0x0047ae56`→`0x7a256`), each a **unique** 192-bit match
  at the arithmetically-predicted offset — coincidence excluded. So the read is
  **independently confirmed**. But James could **not** reproduce the **write**
  round-trip: (1) mid-session **gdb 15 chokes on the stub's stop-reply** —
  `Malformed packet(a) (missing colon)` from a `T` packet with a malformed
  trailing register field — so stock gdb becomes unusable; and (2) the stub is
  **single-client, leaks sockets (CLOSE_WAIT), and wedged** — it left the guest
  CPU **frozen** (utime/stime not advancing; port `LISTEN` but not `accept()`ing).
  James's fair point: code-page reads match the file whether served from live RAM
  **or a backing image** — only a write proves live *mutable* RAM, and that proof
  was not independently obtained. My own earlier `write→readback→restore` PASS
  stands as my observation but is **not independently verified**.
- **Write reproduced on a FRESH stub + echo ruled out (post-James).** James's
  `Malformed packet`/wedge all trace to the stub **degrading under repeated
  connections** — it leaks `CLOSE_WAIT` sockets and, after dozens of connects,
  stops `accept()`ing and freezes the guest (reproduced twice, incl. by my own
  client loop). On a **freshly restarted** stub, gdb 15 works: the write
  round-trip PASSes first try (`addr=0x00aafbe0`, wrote `12345678`, read back
  `78563412`, restored). To kill the stub-echo hypothesis, I wrote the 8-byte
  pattern `1122334455667788` and read an **overlapping** window at `addr+2` → got
  `33445566` = `pat[2:6]` exactly; a pure echo cannot return correctly-shifted
  bytes for a different read window, so the data is in **real, correctly-addressed
  guest RAM**. This is **my** re-verification; a fresh-James write pass is still
  the clean way to flip James's verdict.
- **Fresh James WRITE audit (2026-08-18) — ACCEPT.** A second fresh-context James
  independently reproduced the write at three addresses (round-trip + two
  overlapping windows `addr+2`=`33445566` and `addr+5`=`667788`, echo excluded),
  and clinched **live RAM** with a free-run test: a `timeout`-killed gdb left his
  pattern `1122334455667788` at `0x00aafbe0` un-restored; the next connect's first
  read returned `00000000f0000000` — a value never written that session — proving
  the **guest CPU itself overwrote it**. That simultaneously rules out a static
  backing image, a stub echo, AND a stub-side shadow overlay: the write reaches the
  same live RAM the CPU reads/writes. Done in **6 connects**, and this round the
  stub stayed healthy (single `0A`, guest advancing, survived even an undetached
  kill) — so the fragility bites under *dozens* of connects, not economical use.
- **Conclusion (post-James):** the 86Box GDB-stub route **reads and writes** the
  game's live guest-virtual memory — **both read and write independently confirmed
  by fresh James** (read ground-truth byte-exact vs `bugs.exe`; write proven live,
  mutable, correctly-addressed RAM) — using a **v6.0
  `GDBSTUB=ON` build** (dynarec + stub), **not** master (whose interpreter can't
  boot). Load-bearing caveat: **stub fragility** — single-client, leaks sockets, a
  malformed stop-reply that breaks stock gdb ≥15 once degraded, and it
  **wedges/freezes under repeated connects**. A real workflow must connect
  sparingly, restart the stub periodically, and/or use a raw-RSP client and ideally
  a patched (multi-client, non-leaking, correct stop-reply) stub. Gate 2A
  (read + write) is **closed — James-accepted**. Still open (extensions): a
  gameplay-state non-zero read (enter a level), a clean watchpoint, and 2C.
- **Gameplay-state non-zero read + live-tracking DONE (2026-08-18).** With the
  Training level entered (see `KU-076` resolution — proving the level loads on
  real Win95), the stub read the game's live gameplay globals in-context
  (`$pc` in `[0x401000,0x4c0000)`), via `work/86box/probe_lvl.py`:
  - **level `0x00861C84` = 17** — non-zero (reads `0` at the menu, `17` at the
    Training title *and* in-level), i.e. the level-index global tracks the state
    transition menu→level.
  - **Flik position `0x0059D910`/`14`/`18` = (−22044, 15860, −19597)** in-level —
    real signed 3D world coordinates (read `(0,0,0)` at the title screen before
    gameplay starts). This is the meaningful non-zero gameplay read that was the
    open extension.
  - **Live-tracking PROVEN:** holding the forward key moved Flik and the position
    re-read as **(−12793, 11822, −6096)** — a delta that matches the visible
    on-screen movement (`work/86box/logs/pos_a.png` → `pos_b.png`, camera tracks
    Flik walking toward the training sign). The stub read reflects *live*,
    changing gameplay RAM, not a static value. This complements the write proof:
    read tracks the guest as it runs, write reaches the same live RAM the CPU uses.
  - Method note: taken economically (≤8 connects per read, fresh-stub-first) per
    the fragility caveat above; the stub stayed healthy. Still open (extensions):
    a clean watchpoint firing, and **2C** (A/D-bit side-effect of a stub read).

## KU-078 - The 86Box Win95 install is a driven session, not a reproducible script

- **Status:** open (engineering debt, not a research unknown).
- **Known:** the [[86Box Win95 RE harness]] was built by a long human-driven /
  agent-driven sequence (container setup, mtools disk prep, `install-mbr`, a
  two-phase floppy `sys`, an msbatch install with one manual OEM-key entry,
  game extract-to-HDD, DirectX). The **result** is captured (disk images under
  `work/86box/`, the recipe in the harness note), but the **process** is not yet a
  one-command rebuild. If the disk images were lost, rebuilding is hours of driven
  work.
- **Why it matters:** reproducibility is a project value; a golden disk image plus
  a driven recipe is fragile compared with a scripted build.
- **Discriminating action:** turn the recipe into scripts / a `make` target
  (container bring-up + disk prep + unattended install), leaving only the
  genuinely-interactive OEM-key step. Until then, treat `work/86box/disk/
  win95_c_clean.img` and `win95_c_game.img` as the golden artifacts to preserve.
- **Deferred:** not on the Gate-2 critical path; do it once Gate 2 proves the
  harness is worth keeping.

## KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)

- **Status:** narrowed, **R1 complete; fresh derived-build visible-ground example confirmed (EXP-20260904-005)**
  — **the linchpin for new-level authoring**
  ([[New-level authoring feasibility (PC)]]).
- **Known (static; names inferred):** level geometry is drawn from `LEVEL.DAT`
  payloads reached through
  `FUN_0044d430` (scene driver) → `FUN_004498f0` (**type-switch** on
  `*(ushort*)(instance+0xe) & 0xbfef`) → per-type drawer → emit primitives
  `FUN_00405fe0` (quad) / `FUN_00407450`, called **directly** through thunks
  `0x00401d66` / `0x00401ccb` (e.g. `0x454199 call 0x401d66`). Chain:
  instance `+0x10` → object → `+0x14` → geometry payload; relocated by
  `FUN_0044bb70` against buffer pointer `0x005ba240`; instance-array pointer
  `0x005ba7e0`; typed prefix table `0x005c5860`.
  **Container grammar confirmed by raw objdump** (the retail-data chain pins only
  the anchor stride — see below): payload =
  `int32 group_count` + `group_count × 12-byte` anchors (transformed by a 3×3
  `int16` matrix, `>>0xc`, + translation), then per group `int32 prim_count` +
  `prim_count × 44-byte` records. **44-byte record:** nine `int16` at
  `0x00`–`0x11` feeding four overlapping vertex slots, material (5 bits) at byte
  `0x12`, four `int16` UV/attr words at `0x14/0x16/0x18/0x1a`, four `uint32`
  RGB colours at `0x1c/0x20/0x24/0x28`. Tested on retail `LEVEL01/LEVEL.DAT`: all
  **7 type-3 payloads chain exactly end-to-start** (`0x44140`→`0x46e98`) — but that
  chain **only pins the 12-byte anchor stride**: every one of the 193 groups has
  `prim_count == 1`, so the chain gives **zero** discrimination on the split —
  **every** `(skip, rec)` with `skip + rec = 44` chains identically (all 11
  int-aligned combinations). The `skip=0 / rec=44` split rests on **instruction
  evidence**, not the chain.
- **Unknown:** (1) the **semantics of the nine `int16`** — the object code does a
  sliding-window read (v0=s0s1s2, v1=s2s3s4, v2=s4s5s6, v3=s6s7s8 — confirmed for
  **both** emit paths, since `FUN_00405fe0` also reads three shorts at `+0/+2/+4`),
  yet the data reads equally well as four `(x,y)` corner pairs + one spare. Strong
  clue: `s0==s6` **and** `s2==s4` in **193/193** records with `s8 ∈ {0,±1}`, so the
  sliding window yields an axis-aligned footprint from two values `{s0,s2}` plus a
  **degenerate fourth corner in every record**; (2) the **world scale** for vertex positions (no ×32
  evidence — the `<<5` in the record is an RGB channel shift, not a coordinate
  scale); (3) whether the type-2/0xa mesh drawers share this grammar; (4) **what
  carries each level's visible ground — type-3 probably does NOT**: 20 of the 21
  corpus files have zero type-3 records (only `LEVEL01/LEVEL.DAT`, 193 quads, a
  single material `0x62`), those quads are tall/thin (X/Z ≈153 vs Y ≈790, ≈5.2:1,
  clustered 19–32 per instance), **and the drawer is an explicit billboard**: the
  rotation matrix is set once per instance by `FUN_004636c0` from a camera-related
  global (`DAT_005b1ec2`), while `FUN_00453ff0` updates **only** the translation
  (`FUN_00463740`), and all 7 objects carry Euler `(0,0,0)`. So type-3 is almost
  certainly camera-facing vertical panels (candidate foliage/props), not ground.
  **Format and exact consumer linked; ground identification was INFERRED
  at the R0 checkpoint (2026-08-18)** —
  [[EXP-20260818-006 - R0 the static mesh format and where visible ground lives]].
  A **static indexed mesh** format hanging off type-`0x41` instances
  (instance `+0x10` → 24-byte object → `+0x14` → payload) is validated
  **2,543/2,543 (100.00%)** over 146,030 face indices on the **retail** corpus
  (17 of 21 files contain such instances), and a break-test scores every competing
  grammar at 0–42%. [[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]]
  links the exact PC consumer: `FUN_004498F0` dispatches type `0x41` to
  `FUN_0045a7f0`, which advances by `vertex_count * 12`; its face loop
  adds each stored u16 directly to the vertex base. The reconstructive
  implementation round-trips all 2,543 retail payloads byte-for-byte and checks
  all 146,030 face references. Visible-ground identity was circumstantial at
  that R1 checkpoint; [[EXP-20260904-005 - Raised floor and visible ground pairing]] now supplies
  a bounded live example on the auto-hardware build. The first R2b packet completed valid A1/B/A2
  arms, but its `0.75` control-agreement gate failed at `108 / 307200` stable
  pixels before effect classification. It supplies runtime procedure evidence,
  not a joined code/data-to-visible-ground causal result. Tag/material
  semantics, vertex UV/colour semantics, and world scale remain unknown; the
  retail corpus does not exercise `primitive_group_count > 1` or object byte
  `0x13 != 0`.
- **Why it matters:** without it we can compute collision but cannot draw new
  terrain — it gates a *visible* authored level.
- **Historical R2 sequence (banked; current floor priority is DEC-230):** commit and preregister a stable-camera or
  steady-state successor to
  [[EXP-20260819-001 - R2b Anthill static mesh causal runtime]]. That successor
  is frozen as
  [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]:
  under the authorization and later user-directed pivot, calibrate the exact
  auto-hardware-build-scoped `t0 + 3.300 s` process freeze. `F0-AH-005`
  reached the genuine Level One title but rejected before the index read when
  ordinary animation changed the full-frame hash. The then-fresh `-006` packet
  requires two fixed decoded-RGB title regions reproduced across reviewed
  A1/B, A2, and `-005` frames before the single index read. `-006` then completed
  the controlled freeze but its animated entities differed from the retail R2b
  phase. Four fixed camera/terrain regions match all six retained retail and
  derived inputs. `-007` produced no frame because its final full XID guard
  overran the freeze schedule before `SIGSTOP`. `-008` then rejected during
  discovery before any runtime action; its old receipts do not identify the
  changed process field, so it remains an unclassified tooling result rather
  than evidence about the game. Fresh `-009` requires and persists two
  consecutive identical exact-final process observations before input, while
  retaining the 60 ms final-guard reserve, 3 ms signal reserve, unchanged
  regions, and exact `-006` derived-frame gate. A second derived identity ends
  hash extension. `-009` passed the derived-build freeze calibration with the
  exact `-006` frame, all structural regions, and stable authorized view blocks;
  James accepted its committed result. The exact argument-free creator,
  dedicated arm executor, and provenance-bound derived-control comparator are
  frozen offline but must be committed and accepted before DAT creation. Then
  run exact
  control/localizer/control arms
  for the guarded face-8 topology edit. Commit and independently accept the
  localization before returning to the one-byte vertex candidate.
  Any positive result remains scoped to executed build `1e1d5099...a9c41f`;
  a controlled retail-executable intervention is still required for retail R2
  closure or retail-build visible-ground promotion.
  [[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]]
  retains Level03 as a fallback rather than the primary causal target.

### KU-079/KU-080 update - 2026-09-04 failed return and flat testbed

**Finite moving/view extension, 2026-09-05:**
[[EXP-20260905-002 - Box movement and occluding-view validation]] adds five
valid reversal sweeps in two file-loaded placements: 518 grounded state samples,
107 captures, and no sampled reference-point wall crossing. Jump/top/step-off
contact also passes. The new paused occluding-edge classification has zero
analytic-top-before-actor inversions among 485 blue samples with reconstructed
actor coverage; actor-buffer corroboration remains partial (179/355 tuples).
An original-location south navigation route is rejected after overshoot/outside-
deck motion. The guarded stationary south retry passes only for that placement.
This narrows finite movement/view behavior; all-view visibility, universal mesh
rules and EXP-005's shared-floor return failure remain open. Both test games
closed, and the original user's paused state was unchanged at experiment close;
the later banking audit is clean. DEC-239 returns
the next bounded work to the shared-floor defect.

**Live edge discriminator completed, 2026-09-05:**
[[EXP-20260904-011 - Box top diagonal edge discriminator]] changes the finer
top's internal diagonals while preserving vertices and collision. Original
instructions put it ahead at all 259 analytic points and preserve all 255
prior fixes offline; denser grids alone can regress old samples.
[[EXP-20260905-001 - Box top diagonal live comparison]] subsequently executes
the four authorized writes: all six residuals disappear with alternate
diagonals and return with restored finer control, while all 255 earlier fixes
remain hidden. All 15 captures match measured state; both 3,575-pixel control
regions restore exactly. Those six samples are resolved at the preserved pose.
At the EXP-001 boundary, sample placement, actor reconstruction, other views and
oscillating movement remained uncertain; EXP-002 subsequently narrows finite
movement/view behavior above. General mesh rules and EXP-005's floor return stay
open. The original mesh was restored in the paused game at comparison close and
write authority was consumed.

The subsequent [[2026-09-04 2057 - Codex - Terrain research checkpoint]] banks
the bounded experiments and prototypes; it does not close the remaining edge,
other-view, shared-floor or general-authoring questions below.

The checkpoint also records a separate validation limit: the repository-wide
check was interrupted during R2q tests after temporary-storage quota failures.
Its historical-protocol test compares an expected 029 hash against the 031
implementation value; both files match parent commit `0f589de`. That mismatch
and a complete repository-wide green run remain separate follow-up work. The
checkpoint session records the bounded terrain and failed-test rerun.

**Later residual:** after EXP-008's offset correction, the user reports visible
leg fragments during side movement and pauses at the failure.
[[EXP-20260904-009 - Paused side-view depth interpolation]] retains that exact
game without input/restart. Player/contact are on the lower deck outside the
box's side; original renderer outputs and an analytic top intersection implicate
large-face depth ordering. Finer faces improve it offline, with remaining edge
uncertainty. The user-authorized live comparison subsequently completes in
[[EXP-20260904-010 - Paused subdivision live comparison]]: all255 prior
inversion-point fragments disappear and return on restoration; all3,575 ROI
pixels restore, with9 captures matching measured player/contact/camera state.
Six other analytic boundary points stay blue, and general subdivision/other-view
acceptance remains open. EXP-008 and EXP-010 are bounded improvements, not
all-view visibility acceptance. The original mesh is restored in the paused game.

The user reports that walking up and back across EXP-005 causes a fall through
the floor. This invalidates treating its local visual/height correspondence as
reliable traversal; the exact defect is not isolated. [[EXP-20260904-006 - Flat deck and solid block test]]
provides a separate flat deck and clearly raised block, with top/side removal
controls in original instructions and two live jump-off-return cycles.188 tests
pass. This establishes a useful bounded testbed, not a repair of EXP-005 or a
general grouping/seam rule. Its native objects remain; no whole-render/runtime
independence claim is made. The user subsequently confirmed landing/contact
with the block, but reported legs visible over it from the lower deck behind it.
[[EXP-20260904-007 - Deck visibility and inherited depth offset]] corroborates the deck position and
identifies an inherited additive render-depth field. [[EXP-20260904-008 - Block depth offset runtime comparison]]
confirms the demonstrated leak's cause and repair with a one-byte removal and
restoration at matching player/contact/camera state. Smaller faces were not
needed for that bounded result. The field also affects a distance threshold;
general geometry/material rules, full layouts and shared boundaries stay open.

### KU-079 update - 2026-09-04 paired floor and visible-ground proof

The paired fixture was subsequently launched for user verification in [[2026-09-04 1935 - Codex - User paired floor play session]].
This adds no general grouping or edge-stitching result; local correspondence
and remaining limits below are unchanged.

[[EXP-20260904-005 - Raised floor and visible ground pairing]] changes17 vertex Y fields in
Level01 primary meshes160/213/280 while holding the raised collision file fixed.
Live scene/object pointers and all three vertex arrays match the staged files.
At identical current XYZ and camera bytes, restoring LEVEL.DAT restores every
pixel of a21,630-pixel static ground region; the paired edit changes12,057 pixels.
This is a bounded code/data-to-visible-ground causal example on the accepted
auto-hardware build, with an exploratory region selected before the restored
control. Whole-renderer-state equality, retail R2 acceptance and full command
semantics remain open. The R2q bank is unchanged. Next terrain work targets shared
boundaries and a small ramp at this verified site, rather than redoing R1 or R2b.

### KU-079 update - 2026-08-26 P0E additive recovery source boundary

The P0E passive collection reproduced the 16→17 task topology but did not
identify the added task's role and produced no render/terrain discriminator.
Its failed normal close left two exact residual identities and `Y:` staged.
The separately authorized additive recovery is now James-accepted for source
freeze after two rejection rounds, with 101 focused and 809 combined tests
passing. At that source checkpoint it had not run: the one-shot marker was
absent, the original P0E packet remained pending/unchanged apart from allowed
log append, and exact clean activation acceptance remained required. The later
failed run is recorded immediately below. KU-079 remained unchanged because no
R2q runtime observation or visible-ground/terrain result followed.

### KU-079 update - 2026-08-26 P0E-R1 failed evidence

The accepted one-shot recovery removed both residual processes through exact
TERM/KILL receipts, and a post-action audit is clean. It failed its own
two-read post-KILL stability gate before `Y:` restoration, however. James
accepts the 10-entry failed envelope only as failed evidence; P0E-R1 is consumed
and cannot retry. `Y:` remains staged, original P0E remains pending, and no
R2q instruction, process-memory range, presentation boundary, or terrain datum
was observed. KU-079 therefore remains unchanged. A separately authorized and
accepted `Y:`-restoration successor is an environment prerequisite before any
later R2q runtime can be considered.

### KU-079 update - 2026-08-28 YR3 consumed pre-action failure

The sole James-accepted YR3 mapping-restoration invocation consumed marker
`7191e193...e43` but stopped before any mapping event. Its journal is empty,
its reducer remains idle, all action/scratch names are absent, `Y:` remains
staged, `R:` remains P0A, and the post-action host audit is clear. James round
34 accepts those facts only as failed evidence. The retained PipeWire module
listing exposed a multiline short-list parser defect, and the failure validator
incorrectly compared historical predecessor monotonic times from a prior boot
with the current attempt. The overall failed-unverified packet is therefore
not a production-valid terminal envelope, YR3 cannot retry, and a distinct
successor with fresh authority is required. No R2q instruction,
process-memory range, visible-ground discriminator, or terrain/collision datum
was observed, so KU-079 remains open and unchanged.

### KU-079 update - 2026-09-01 R2q-026 offline freeze

R2q-026 corrects the pre-science process-map convergence defect and freezes a
fresh exact successor, but no game or wrapper ran. Therefore it adds no draw-
command, visible-ground, render-grammar, task-role, or causality evidence.
KU-079 remained open; at that checkpoint the next discriminating step would
have been a separately authorized R2q-026 D1-then-D2 runtime after exact
clean-tree acceptance.

### KU-079 update - 2026-09-01 R2q-026 pre-science failure

The authorized D1 arm failed before title navigation because executable maps
device provenance crossed mount namespaces. No quiet census, stopped-memory
capture, PNG batch, or D2 comparison occurred. The distinct accepted recovery
changed only the `Y:` mapping and records `terrain_collision_claim:null`.
KU-079 remains open; a fresh successor must correct the namespace comparison
before it can resume the same discriminator.

## KU-080 - Does PC terrain collision block laterally, or is it height-only?

- **Status:** narrowed, 2026-09-04 — original PC instructions admit real Level01
  triangles and separate X/Z barrier segments and produce lateral response at
  controlled positions, including grounded entry established by original
  landing. One translated barrier now has live loaded-data and walking
  controls (EXP-004); a six-cell raised floor now has original and live height,
  jump/landing and visible-ground companion tests (EXP-005). General surface
  deformation and boundary handling remain open (C2).
- **Earlier survey:** the height-query family (`0x004a8410` loader, `0x004a8950` bounds/
  spatial index, `0x004ac460` collector, `0x004aca60` resolver, `0x004a9290`
  half-plane, `0x004acf90` material reader) implements **ground/ceiling height
  resolution** — selecting a plane and returning a height. A survey of that family
  did not include the lateral-response branch identified below. PS1 uses oriented **swept
  planes** with a 192-unit collision skin for walls (PS1 fact,
  [[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]]).
- **Known now:** `004ab1a0 -> 004aa4d0 -> 004a9860/004a9420` implements
  XYZ plane crossing and vertical-triangle inclusion. Synthetic X/Z wall
  crossings stop at88 instead of−1024; four negative controls per axis reach
  their unconstrained endpoints. The slot0 caller is statically bound to Flik, and prior runtime
  traces independently bind the coordinator's writer `004ab889` to `0059d910`.
  See [[EXP-20260904-001 - Original PC lateral collision and descriptor-store probes]].
- **Real-data extension:**
  [[EXP-20260904-002 - Retail collision admission and separate XZ barriers]]
  runs the full original loader and movement coordinator with original bounds /
  bucket initialization. Level01 source87/cell1000 is admitted and causes X/Z
  deflection; removing descriptor87 removes that response. Kind`0x101` source179
  supplies four X/Z barrier pairs; the first causes response at three widely
  separated heights. Segment removal, triangle removal and moving-away controls
  distinguish the paths. These are synthetic positions and nongrounded flags,
  not observed gameplay.
- **Grounded/grammar extension:**
  [[EXP-20260904-003 - Barrier grammar and landing-seeded grounded movement]]
  decodes the canonical16-segment block/sentinel grammar across65 strips in18
  files, matches108 original collection cases and measures the16-pair cap.
  Original landing supplies contact on real floors; later steep-triangle and
  barrier crossings enter `004aae30`/`004a9ba0`. Specific obstacle removal
  after identical landings removes their return2 responses. Flat floor tests
  separate tangent movement, normal projection and a cleared-ground-flag control.
- **Live authoring extension:**
  [[EXP-20260904-004 - Translated barrier live collision proof]] moves source179
  into the spawn path in a derived file. Live list reads match the changed
  payload exactly. The edited walk avoids its footprint; a restored-file
  control has eight of 50 samples inside it, from identical starting XYZ.
  Original instructions also show response moving from old site to new site.
  This is a four-segment translation, not general mesh or floor authoring.
  The user subsequently confirmed the collision personally in
  [[2026-09-04 1909 - Codex - User barrier play session]]; no new numerical
  measurement or visible-geometry conclusion accompanies that confirmation.
- **Unknown:** noncanonical barrier variants, wider normalization/overflow,
  general slope/edge behavior and other authored-wall configurations. Canonical metadata,
  the measured capacity and the cited grounded-entry fixtures are established;
  no universal gameplay/contact-state contract is claimed.
- **Why it matters:** determines whether a Blender exporter can rely on
  slope-classification (PS1's "one mesh, >45° = wall") or must emit a distinct
  wall structure — a fork in the collision-encoder design (track C3).
- **Discriminating action:** preserve EXP-005’s tested rigid lift and visual
  companion, then make shared boundary heights, normals and bounds agree for a
  connected ramp. Test uphill/downhill crossing, jumping/landing and edge
  transitions in original routines and the game. Keep reset/contact heights
  distinct and reuse the completed loader/barrier evidence. Canonical sequence:
  DEC-230 / [[Project Roadmap]].

### KU-080 update - 2026-09-01 R2q-026 offline freeze

The new activation contains no runtime observation. It does not distinguish
height-only terrain from lateral blocking, so KU-080 remains open and its
discriminating action is unchanged.

### KU-080 update - 2026-09-01 R2q-026 pre-science failure

R2q-026 produced no stopped process-memory or gameplay comparison, and its
mapping-only recovery contains no terrain observation. Height-only versus
lateral blocking remains unresolved; the discriminating action is unchanged.

## KU-081 - Render-side mutation of the collision descriptor table (FUN_0044ca00)

- **Status:** narrowed, 2026-09-04: direct-store destinations proven N..N+19,
  real Level01/Level03 templates and reserved ranges resolved;
  whole-subtree/static-template independence remains open. Found 2026-08-18 by
  independent audit of a wrong "no linkage" claim.
- **Paired authoring scope:** [[EXP-20260904-005 - Raised floor and visible ground pairing]] demonstrates
  a fixed floor/visual companion at one site. It does not resolve renderer-side
  mutation or prove the two datasets independent; deeper coupling remains open.
- **Known:** `FUN_0044ca00` **reads and writes** the collision descriptor table
  `0x007F4590` — e.g. `(&DAT_007f4590)[iVar4 * 0xc] = iVar7` (stride `0xc` ints =
  the `0x30`-byte descriptor), and it re-offsets descriptor coordinates. It is
  reached from **`FUN_0044d430`, the render scene driver**, via
  `thunk_FUN_0044ca00` (`0x0040100a`). So a render-side call tree mutates
  collision data at runtime.
- **Why it matters:** it **refutes** the earlier claim that render and collision
  are wholly disjoint with "no hidden linkage to reproduce". The
  one-mesh-two-independent-encoders authoring design in
  [[New-level authoring roadmap (terrain, collision, materials)]] rests on that
  premise, so the premise must be re-established (or scoped) before the encoder
  design is committed to.
- **Known now:** raw instructions plus27 synthetic branch cases show the direct
  prefix stores only into N..N+19, with N=`DWORD[007f3d30]`. The initializer
  reserves32 entries. The call-site guard is global `005c5edc & 0x10 == 0`,
  not an object-type dispatch. Object creation additionally gates nonzero type,
  loaded resource, flag mask `0x02`, nonnegative template, and changed tag. See
  [[EXP-20260904-001 - Original PC lateral collision and descriptor-store probes]].
- **Real-data extension:** EXP-20260904-002's original loader and initializer
  produce N=191 for Level01 and N=602 for Level03, each including13 PLANTTER
  templates. Those templates occupy178..190 and589..601 respectively and are
  tag-cleared; all terrain descriptors remain below them. The direct twenty-slot
  render destinations are therefore191..210 /602..621 for these exact loads.
- **Unknown:** deeper coupling through omitted render callees, aliased payloads,
  and other file/layout variants. N equals the loaded-record high-watermark in
  the two tested loads, not by universal proof. The source-index code has no
  `<N` check, and initialization separately clears mapped template tags.
- **Discriminating action:** audit reachable payload writes and additional
  loader variants before declaring static encoder independence. Do not repeat
  the completed two-file mapping census or direct-store arithmetic proof.

### KU-081 update - 2026-09-01 R2q-026 offline freeze

The frozen successor has not observed the stopped descriptor table or render-
side mutation at runtime. Dynamic-only versus static-range targeting remains
unresolved, so KU-081 remains open and its discriminating action is unchanged.

### KU-081 update - 2026-09-01 R2q-026 pre-science failure

The arm failed before any stopped descriptor-table range was read, and the
recovery performed no process-memory action. Static versus dynamic descriptor
targeting remains unresolved; the discriminating action is unchanged.

## KU-082 - A project mod artifact has unrelocated object pointers (LEVEL07/LEVEL1.DAT)

- **Status:** open (defect in a working copy, surfaced 2026-08-18 by the R0 mesh
  decode — [[EXP-20260818-006 - R0 the static mesh format and where visible ground lives]]).
- **Known:** `work/copies/M3-training-51-grains/CD/LEVEL07/LEVEL1.DAT`
  (sha256 `8ab9acd4…`, 115,076 B) is 16 bytes larger than retail
  (`494d2818…`, 115,060 B) and its tail is **byte-identical to retail shifted by
  `0x10`** (`mod[0x3f8:] == retail[0x3e8:]`). So the insertion was made **without
  relocating the primary records' `+0x10` object pointers**: those fields are
  stale, and 101 of that file's type-`0x41` objects fail to resolve
  (`0xffffe000`, `0x9`, `0xb`, …). Retail resolves 2,543/2,543.
- **Why it matters:** the file is a *working copy used in analysis*, and its sha is
  recorded **nowhere** in the Vault — it is neither retail nor the accepted
  51-grain output. Any measurement taken over that copy silently mixes in a broken
  file; this experiment's first draft did exactly that.
- **Unknown:** which run produced it, whether it was ever loaded by the game (it
  would likely fault or mis-render), and whether other files in that copy share the
  defect.
- **Discriminating action:** diff every file in `M3-training-51-grains/CD/` against
  retail; identify the producing run via `scripts/run-index.py`; if it is an
  orphan, delete or clearly quarantine it. Prefer retail
  (`work/copies/BUGS_PC-full-disc/PC/BUGS/CD/`) as the corpus for format work.

### KU-079 update - 2026-08-19 R2c localizer remains unresolved

[[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]] ran
a valid derived-build `C1/L/C2` face-collapse comparison. The controls are exact
but L differs in 18,612 pixels across 353 components, and its frame identity is
already present in unmodified retail evidence. The comparator correctly
rejected localization. This neither confirms nor excludes visible contribution
by face 8 and does not identify it as terrain/ground. KU-079 therefore remains
open. **Superseded discriminator history:** this paragraph originally required
an empirically established animation cycle. EXP-003 D1 later found no exact
period, so that requirement is retired. EXP-004 later rejected its full-frame
phase gate. EXP-005 then aggregate-rejected; the active discriminator is the
fresh-D3 holdout design described below. Fresh authorization remains required before either
that D3 control/holdout or any later `C/L/L/C` intervention.
## 2026-08-19 update to KU-079 - exact-cycle model rejected

[[EXP-20260819-003 - R2d Anthill sampled phase calibration]] ran one authorized D1 control. Its 121 decoded-RGB frames were all unique and yielded no exact period. The lower-right camera crop also had six hashes. The exact-cycle and four-crop model is rejected and superseded.

KU-079 remains open. No positive localizer, visible face-8 attribution, terrain identity, or retail causal result exists. EXP-004 rejected its phase-sensitive full-frame gate. [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] then ran two procedurally valid controls but aggregate-rejected on 233 D2 observations at 198 unique pixels outside D1's mask. The residual aligns with Flik's silhouette and does not establish camera instability, terrain behavior, visibility, or causality. [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] later accepted the frozen combined diagnostic mask on one finite grid without expanding it.

## 2026-08-19 update to KU-079 - fresh D3 finite-grid holdout accepted

[[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] independently reproduced every unmasked pixel on the fixed 121-point grid: zero outside-mask observations and zero unique pixels, result SHA-256 `3fe541dfd9973ce1238f603e3fafb28834749db7530f2e27db6efb09e2bc0c19`. This narrows the nuisance-separation problem enough to permit a separately preregistered C/L/L/C localizer design at the exact derived-build/camera/grid scope.

KU-079 remains open. EXP-005 remains rejected, and D3 establishes neither a cycle nor exhaustive nuisance coverage. Face-8 visibility, ground/terrain identity, causal response, coordinate/world-scale semantics, and retail-executable confirmation remain unresolved. No localizer DAT or C/L/L/C runtime is authorized.

## 2026-08-19 update to KU-079 - replicated localizer discriminator prepared

Before runtime, [[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] froze the next discriminator: `C1/L1/L2/C2`, with L1 and L2 independently created from retail but byte-identical at the exact three guarded face-index changes. It required exact control agreement outside the accepted nuisance mask, exact corresponding L1/L2 RGB agreement, and one bounded at-least-25-pixel static core/localized component.

KU-079 remained open at that boundary. No localizer DAT or runtime yet existed, and no face-8 visibility, terrain, material, collision, coordinate, causal, retail-executable, or no-effect result was established. Fresh authorization was required after offline commit and James acceptance; it was later granted and consumed by the inconclusive result recorded below.

## 2026-08-19 EXP-007 update - KU-079 face-8 visibility remains open

[[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] completed procedurally but did not localize face 8. Its aggregate result SHA-256 `723e03ed...a309` has 251 control outside-mask mismatches, 228 L1/L2 disagreements, and zero intersection/static core. L2 frame 35's entire 228-pixel change was reproduced exactly by C2 frame 35, so it is nuisance rather than face-8 evidence. KU-079 remains open: there is no PC-confirmed face-8 visibility, terrain identity, causal effect, or clean no-effect result.

The EXP-006 nuisance mask is scoped to its single accepted D3 holdout and is not exhaustive across fresh controls. The then-required revision had to be derived offline from controls only; EXP-008 supplied it, and EXP-009 later passed its fresh control holdout. A separately authorized later localizer is still required, and neither result can retroactively promote EXP-007.

## 2026-08-19 EXP-008/009 update - D4 finite holdout passed

[[EXP-20260819-008 - R2j Anthill control-trained successor mask]] used only C1 and C2 to propose a 93,445-pixel successor mask. It does not redilate the old mask; diagnostic/mask identities are `83931a8a...9a5`, `b855df0a...c936`, and decoded binary `9ff27caa...1ba`. At that packet boundary it was only a proposal; EXP-009 later promoted it to one finite derived-build/view/grid nuisance reference.

[[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]] completed with exact zero difference across all 121 frames (`bf2b4625...69d8`), and James accepted that one finite holdout. KU-079 remains open: face-8 visibility, terrain/ground identity, causal/no-effect behavior, world scale, and retail confirmation remain unresolved. KU-080 and KU-081 are unchanged; this renderer gate does not advance collision. Any localizer successor requires a new offline packet and fresh authorization.

### 2026-08-20 KU-079 update - D4 accepted; fresh localization executed inconclusively

[[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]] found zero outside-mask mismatch observations on its fixed 121-frame D4 holdout, supporting only a finite mask adequacy statement. [[EXP-20260820-001 - R2l fresh replicated face8 localizer]] then completed fresh C1/L1/L2/C2 arms and two independently derived face-8 work copies. All pair/lifecycle gates passed and controls had zero outside-mask mismatches, but L1/L2 did not replicate (`20,634,078` disagreement observations; zero intersection/core), so the result is scientifically inconclusive. Face 8 is not PC-confirmed visible terrain/ground and is not rejected as no-effect; collision, materials, component axes, world scale, occlusion, and retail-executable causality remain unknown. The next discriminator is offline cross-time/camera-state analysis only.

### 2026-08-20 KU-079 update - R2m diagnostic frozen offline

[[EXP-20260820-002 - R2m offline cross-time correspondence diagnostic]] tested only whether one exact fixed wall-clock lag explains the retained L1/L2 mismatch while all three camera-safe crop signatures remain control-exact. No lag passed: L1 had no eligible-pixel temporal variability, L2 did, and all 121 lags failed. Fixed wall-clock alignment is therefore nonviable. No memory-derived camera/player state exists in this packet. Independently justified PC read-only camera/player/render-state anchors are now required before another runtime design; face visibility, no effect, terrain, materials, collision, and causality remain unknown.

### 2026-08-20 KU-079 update - R2n static state anchors bounded

[[EXP-20260820-003 - R2n PC state-equivalence read candidates]] bounds exact
PC-native equality candidates at upstream PC `0x00414585` and generated-view
PC `0x0041458F`. The address/byte ranges are independently rebound to the
auto-hardware build. The full matrix-copy tail, asynchronous polling, and
`0x0063E888` renderer scratch are excluded; derived origin
`0x005BDB9C/12` is optional/redundant.

KU-079 remains open. These bounds authorize no process-memory read or runtime
and do not establish complete frame/player/camera state, face visibility,
terrain/ground, materials, collision, causality, no effect, or retail
behavior. A future packet must freeze execution control, coherent reads,
exact equality, receipts, cleanup, and fresh authorization.

### 2026-08-20 KU-079 update - R2o completed-present design bounded

[[EXP-20260820-004 - R2o completed-present state calibration protocol]] binds
future R2n snapshots to one normal update and exactly one successful DirectDraw
presentation return before `0x0040FFE3`. The static trace rejects treating
outer completion, EndScene return, or ShowBack return alone as presentation.
It also preserves the distinction between a successful CPU-side buffer method
and later Gamescope compositor exposure.

KU-079 remains open. The two-control protocol and exact three-invocation
sequence are frozen, and its executor is implemented offline but remains under hard-truth audit; no runtime,
debugger, read, execution-control, screenshot, DAT, localizer, or candidate
action is authorized. Even a future pass would calibrate only the tested
derived-build state/display sequence; it would not prove face visibility,
terrain/ground, material, collision, causality, no effect, or retail behavior.

### R2o implementation boundary (2026-08-20)

At its offline implementation checkpoint, [[EXP-20260820-004 - R2o completed-present state calibration protocol]] had an executor and 76 passing targeted tests, including a non-game i386-compat ptrace fixture and exact state-machine, census, result, timestamp, finalization, demotion-failure, and rollback regressions. The controls had not run at that historical boundary. The later first D1 attempt is recorded below; it rejected before attachment and therefore still does not establish whether two fresh Anthill Level01 controls reproduce the preregistered completion-boundary state/image sequence. The result cannot yet localize face 8 or advance terrain, material, collision, or retail-behavior claims.

The first authorized D1 reached hardware Direct3D and Anthill Level01 but
rejected before debugger attachment on post-title focus readiness. The second
authorized D1 again reached those gates but rejected before attachment because
its focus commands were not scoped to the nested X display used by discovery
and guards. D2 did not launch in either packet. No R2o state read, debug-
register write, stopped capture, or DAT action occurred. The third authorized
D1 passed the corrected nested-display focus gate but rejected before ptrace
because the R2o guard used a lowercase host path for the uppercase retail DAT;
its D2 did not launch and no debugger action or R2o read occurred. The fourth
authorized D1 fixed that path, armed only local DR0 on the exact initial
16-task census, and reached one exact outer-entry trap. The immediate stop-all
census differed, so it rejected before measured-TID selection, R2o reads,
stopped captures, or later scientific action; every changed debug register was
restored and read back. This proves only census disagreement, not its cause.

At that historical boundary, `-005` identities and durable exact census-delta
evidence were offline and authorization-gated. The later authorized D1 repeated
the drift and ended R2o retries as recorded below. KU-079 remains open:
completion-boundary reproducibility and every terrain/collision/material
inference remain unknown.

### 2026-08-20 KU-079 update - R2o retries ended on exact task addition

The authorized `-005` D1 repeated the first-trap census rejection and now
identifies the delta exactly: added TID `1648646`, start ticks `28065259`, no
removal or reused TID. [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
authenticates that result offline. The task's name, creator, role, module,
lifetime, and debugger dependence remain unknown; the sole PC `CreateThread`
call is not attribution evidence. R2o retries are closed. KU-079 remains open,
and the next discriminator is a separately authorized passive P0A lifecycle
control, not another terrain/localizer arm.

### 2026-08-20 KU-079 update - passive executor frozen offline

The P0A argument-free executor and independent validator in
[[EXP-20260820-005 - R2p task lifecycle diagnostic]] are implemented and pass
the focused offline suite, including a real isolated non-game X11/XTEST ABI
fixture. Publication now requires one independently authenticated
hardware/Level01/navigation/runtime prefix plus exact audit and `R:` restoration
chronology. They use two persistent X11 connections, one exact
521-point `/proc` grid, before/after task-directory enumerations, immediate
first-seen task metadata, and normal close only. No level-index/process-memory
read, debugger, signal, screenshot, DAT, localizer, candidate, or R2o action is
reachable. At that implementation boundary the executor was unrun,
unauthorized, and awaiting James; all production identities were absent. This
does not narrow KU-079's terrain,
collision, material, visibility, causality, or retail-behavior unknowns.

### 2026-08-20 KU-079 update - first P0A audit rejected and corrected offline

James rejected exact commit `52d9a0f` / tree `8b271be` before runtime because
nine integrity gaps allowed premature terminal publication, under-validated
rejected timing/title failures, unbracketed task metadata, path-unbound asset
guards, synthetic X-connection identity, incomplete outcome names, stale pins,
and a double-read final-log receipt. The corrected candidate closes each gap
and passed 150 focused tests including the real isolated X11/XTEST fixture.
The user had explicitly authorized the bounded 521-point P0A collection, but
the preregistered ordering gate still forbade launch. Stage, pending,
published-unverified, accepted, and rejected identities were all absent; no
runtime occurred. James later rejected that candidate as recorded below.
KU-079 and every terrain/collision/material/visibility/causality/retail unknown
remain open.

### 2026-08-20 KU-079 update - second P0A audit rejected and corrected offline

James rejected exact commit `b24890b` / tree `8ce1cfc3` before runtime despite
passing its 150 focused and 1794 full-repository tests. Five counterexamples
remained: authentic timing failures could not publish as procedural rejection;
manifest creation could mutate semantically validated bytes; unresolved
metadata could duplicate an identity and falsely call an initial task added;
non-hex 64-character executable digests passed partial rejection; and the two X
sockets were not peer-bound to the retained Xwayland process.

The new candidate closes those cases with structural-versus-timing separation,
a post-manifest semantic validation and manifest authentication, both-parent
rename fsync, neutral deduplicated initial/added unresolved categories, exact
lowercase hexadecimal SHA-256 validation, and Linux `SO_PEERCRED` PID/start
binding from both Xlib sockets to the owned Xwayland identity. The focused suite
passes 158/158 including the real isolated Gamescope/Xwayland fixture. The one
authorized P0A arm remains unconsumed and blocked on James acceptance. KU-079
and every terrain/collision/material/visibility/causality/retail unknown remain
open.

### 2026-08-20 KU-079 update - third P0A audit rejected and corrected offline

James rejected exact commit `c05f167` / tree `d60d88bb` before runtime after
confirming all five preceding fixes and 158/158 focused tests. The remaining
root defect used adjacent task deltas rather than each TID's complete history.
It missed changed start ticks across an observed absence, disagreed between
analyzers about later unresolved metadata, and called a baseline identity that
disappeared for one sample and returned short-lived.

The new candidate derives compact ordered per-TID identity/presence histories
across the full 521-sample grid. Reuse survives gaps, unresolved categories use
global first-seen sequence in both analyzers, short-lived excludes baseline,
reappearing, and reuse-endpoint identities, and the same exact identity on both
sides of an absence produces `task-identity-reappearance-unresolved` with
exact interval boundaries. Six paired regressions pass in the 164/164 focused
suite. The authorized P0A arm remains unconsumed pending James acceptance.
KU-079 and every terrain/collision/material/visibility/causality/retail unknown
remain open.

### 2026-08-20 KU-079 update - fourth P0A audit rejected and corrected offline

James rejected exact commit `96e2fdf` / tree `60ab6a3d` before runtime after
confirming the complete-history fix, 164/164 focused tests, and 1808/1808 full
tests. Both analyzers and the scientific fixture still allowed the guarded
process identity to disagree with, or be absent from, the task census. They
accepted process `(10,20)` with leader `(10,1)`, only unrelated workers, an
empty census, or an impossible reused leader.

The new candidate requires the guarded PID in both task enumerations, the
exact `(pid,process.start_ticks)` leader in every stable sample, and no task
whose start ticks predate the process. A missing parsed leader is admitted only
with its exact sample-local identity-read error and becomes unresolved
enumeration drift. Fixtures now keep a permanent leader and put lifecycle
changes on workers. Five counterexamples are paired across the direct,
scientific, and rejected-prefix paths in the 184/184 focused suite. The
authorized P0A arm remains unconsumed pending James acceptance. KU-079 and
every terrain/collision/material/visibility/causality/retail unknown remain
open.

### 2026-08-20 KU-079 update - fifth P0A audit rejected and corrected offline

James rejected exact commit `b8e8d44` / tree `5c48cbb4` before runtime after
confirming the process-leader anchor and all preceding fixes. The one permitted
leader-omission exception was not exact: direct analysis accepted missing,
extra, non-string, empty, and untyped identity-error receipts, while the packet
prefix also accepted empty strings in scientific and rejected validation.

The new candidate shares one metadata-error receipt validator across both
paths before any leader omission or early drift result. It enforces exact
phase fields, positive identities, bounded nonempty single-line typed error
text, a closed exception-type set, and bounded internal `P0AError` prefixes.
Malformed variants reject across direct, scientific, and rejected tests; the
valid local error remains unresolved drift. The analyzer/packet suite is
201/201 and the native X fixture passes separately (202 total). The authorized
P0A arm remains unconsumed pending James acceptance. KU-079 and every terrain/
collision/material/visibility/causality/retail unknown remain open.

### 2026-08-20 KU-079 update - sixth P0A audit rejected and corrected offline

James rejected exact commit `a68076f` / tree `10bdcad9` before runtime after
confirming the shared receipt validator closed every earlier malformed form.
Its internal `P0AError` messages were still a union across phases, so an
initial `identity` failure could claim the metadata-only post-read identity-
change message and omit the process leader in direct, scientific, and rejected
validation.

The new candidate assigns exact internal-error sets by phase. Initial identity
reads admit only the five fixed `/proc/stat` parser messages; new metadata may
also retain the exact post-metadata identity-change message. Paired tests reject
the message under the wrong phase and accept it under the producing phase
across all three paths. The analyzer/packet suite is 207/207 and native X
passes separately (208 total). The authorized P0A arm remains unconsumed
pending James acceptance. KU-079 and every terrain/collision/material/
visibility/causality/retail unknown remain open.

### 2026-08-21 KU-079 update - accepted P0A-AH-001 preflight consumed, runtime pending before collection

James accepted exact pre-run commit `8437c0a` / tree `53241906`. The one
authorized wrapper invocation then passed hardware and Level Select gates and
retained successful focused `Right`/`Return` receipts, but its log loaded
level07 rather than preregistered Level01. The Level01 gate timed out before
`collection.json`, so no passive task sample exists and the lifecycle
discriminator was not exercised.

Normal `Alt_L+F4` delivery completed but did not clear the loading process
within 89 bounded polls. Signal fallback was correctly prohibited. Evidence
and stage remain pending, `R:` remains on stage, and seven Gamescope/Wine
processes plus one private sink remain live and recorded without termination.
The P0A-AH-001 arm is consumed. No retry, recovery, or second arm is authorized.
The retained post-close audit's raw census is not parsed evidence because Make
stderr followed JSON stdout. Runtime identity also names Xwayland
`(1834812,30382270)` while both socket peers are Gamescope
`(1834786,30382246)`, falsifying the fixture-trained Xwayland-peer premise.
The chooser state, close survival, audit stream separation, and real X socket
provenance are now procedural unknowns; any successor must resolve the latter
two before authorization. KU-079 and every task-lifecycle, collision, terrain,
material, visibility, causality, and retail unknown remain open.

### 2026-08-21 KU-079 update - postmortem candidate rejected and corrected offline

James rejected exact postmortem candidate `932627d` / `4742aa21`: JSON
booleans could alias numeric evidence identities, X receipts were not bound by
their complete credential tuple, and impossible peer chronology/PID collisions
were accepted. The offline correction requires strict integer domains, one
complete PID/UID/GID/start peer tuple, distinct chronological identities, and
sample timing validation before enumeration-drift classification. It passes
269/269 non-native focused tests, native X (270 total), and 1914/1914 full
tests, but still awaits James re-audit and creates no runtime authority.

A timestamped read-only audit now records three unattributed helpers and the
private sink with no open session; prior game/Xwayland PIDs are absent for an
unknown reason. This does not produce the missing P0A lifecycle evidence or
narrow KU-079, KU-080, KU-081, terrain, collision, material, visibility,
causality, or retail-behavior unknowns. P0A-AH-001 remains consumed, stage and
evidence remain pending, `R:` remains on stage, and no recovery or successor
run is authorized.

### 2026-08-21 KU-079 update - numeric-alias and task-partition correction

James rejected exact `740cb07` / `56818bd1`: floats still aliased equality-only
integers, direct enumeration drift masked malformed sample structure, direct
metadata-error partitions admitted impossible receipts, and a missing runtime
PID leaked `KeyError`. The next offline correction shares one exact sorted/
unique task and error partition between direct and packet paths, restricts
unresolved metadata to exact first-seen failure receipts, and rejects all
reproduced numeric/runtime-schema aliases. It passes 297/297 non-native focused
tests, native X (298 total), and 1942/1942 full tests pending James re-audit.
This creates no P0B, lifecycle evidence, terrain/collision conclusion, runtime
recovery authority, or successor run.

### 2026-08-21 KU-079 update - postmortem accepted and Level01 route restored

James accepted the complete offline validator correction at exact
`1b61da32c93b1238c108c0a95cb02628f3284949` / tree
`925ce807af1cd4db706a2d6f733ba935b73d30ba`, including 297 non-native focused
tests, native X, 1942 full tests, and 50/50 adversarial replays. The later
operational PC launch restored the already-proved direct focused Level01 route
without a process-memory read. It does not supply lifecycle evidence and does
not narrow KU-079's render grammar, terrain, collision, material, visibility,
or causal unknowns.

James accepted P0B only as an offline design basis, not as a pre-runtime
packet. Direct `xdotool` must send carousel Right and select Return only. The
existing independent worker retains the sole title Return at sample 5 after
the two persistent X connections open and the exact 521-point grid begins.
The next discriminator is implementation under fresh namespaces and a
separate `Y:` stage that never touches P0A pending bytes or `R:`, followed by
immutable tests, James pre-runtime acceptance, and fresh explicit runtime
authorization.

### 2026-08-21 KU-079 update - P0B implemented offline, runtime still barred

The P0B successor now implements the accepted route split and exact 521-point
collector under fresh namespaces. Its wrapper fails closed as not runtime-
authorized. Focused direct `xdotool` is confined to carousel Right/select
Return before Level01; persistent X opens afterward and owns the sole sample-5
title Return and normal post-collection close. P0A stage/pending manifests are
immutable exclusions, and the focused suite passes 308/308 adversarial tests.

This narrows no game unknown. KU-079 carousel semantics remain unknown because
P0B relies on the already-proved operational route rather than interpreting
the counter. Task lifecycle, terrain, collision, material, visibility, and
causality remain open until a separately authorized, James-accepted runtime
produces a valid scientific packet. The currently open operational game is
not admissible.

### 2026-08-21 KU-079 update - first P0B audit rejected and corrected offline

James rejected exact `2277b75` / `cf2f88c` despite its 308 focused and 2250
full passes. The blocker families were evidence mechanics rather than new game
facts: stale cloned-log provenance, drive-specific wrong-level matching,
unscoped xdotool identity, residual JSON aliases, unauthenticated publication,
permissive direct structures, and inconsistent save-state/ptrace/P0A-`R:`
boundaries. The successor correction passes 351/351 focused tests and directly
replays all reproduced cases; the full repository gate passes 2293/2293 with
zero tracked-file violations.

This changes no KU-079 interpretation. It records a stricter future
discriminator only. No lifecycle sample, render grammar, terrain, collision,
material, visibility, causal, or retail conclusion exists; no runtime is
authorized; and the open operational game remains inadmissible.

### 2026-08-21 KU-079 update - second P0B audit rejected and corrected offline

James rejected exact `8b8d19d` / `e8b58c9` after 351/351 focused passes. The
nine counterexample families concerned the shared level parser, exact P0A
nested manifests, final-log Level01 provenance, X observation consistency,
numeric aliases in retained audit/`R:`/publication data, non-object connection
receipts, and canonical terminal-root identity. The successor closes all nine
with paired direct/scientific/rejected regressions and passes 396/396 focused
tests.

This still changes no KU-079 interpretation. The correction authenticates a
future discriminator but supplies no task-lifecycle observation and no render
grammar, terrain, collision, material, visibility, causal, or retail fact.
At that checkpoint P0B was offline-only pending exact-commit James acceptance and fresh
explicit runtime authorization; the open operational game remains
inadmissible.

### 2026-08-21 KU-079 update - third P0B audit rejected and corrected offline

Exact `e0fa61a` / `02550b15` passed 2338/2338 full tests before James rejected
it for an unhashable nested P0A entry-kind exception and acceptance of a fresh
wrong-level load before LevelSelect. The successor closes both in direct,
scientific, rejected, and executor paths and passes 405/405 focused tests.

This is another evidence-boundary correction, not a game finding. No lifecycle
sample or render grammar, terrain, collision, material, visibility, causal, or
retail conclusion exists. P0B was still offline-only and the open operational
game remains inadmissible.

### 2026-08-21 KU-079 update - P0B offline design accepted

The corrected P0B design passed 405/405 focused and 2347/2347 full tests, and
James accepted exact `3c90a6f` / `5fb8ea6` after independent adversarial
replay. This is protocol readiness only. It supplies no lifecycle sample and
no render-grammar, terrain, collision, material, visibility, causal, or retail
fact. At that checkpoint runtime remained unauthorized and the open
operational game remained inadmissible.

### 2026-08-21 KU-079 update - P0B authorized but preflight-blocked

The user authorized one post-ACCEPT P0B-AH-001 invocation, but the prior
operational group `1978654` survives normal close and prevents a clean
preflight. No wrapper invocation, namespace creation, or lifecycle sample has
occurred. This changes no render grammar, terrain, collision, material,
visibility, causal, or retail unknown. James accepted the launch-proof
activation at exact `c3ad480` / `59acd5d`; the old live group was then the sole
remaining gate and that offline acceptance narrowed no unknown.

### 2026-08-21 KU-079 update - P0B provisional task addition; cleanup pending

After exact authorized cleanup of the old group, the sole P0B invocation
completed all 521 passive samples. Direct analysis finds only one persistent
addition: `2086681/34785536`, absent at sequences 0–26 and present from 27
through 520. There are no removals, reuse, short-lived tasks, or acquisition/
metadata/title-input error. James independently accepted this as a provisional
finite-grid task addition.

Normal close failed, so at that checkpoint the 26-file packet remained pending,
group `2086248` remained live, and `Y:` remained staged. The observation does not identify the
task's function or creator and therefore changes no render grammar, terrain,
collision, material, visibility, or causal unknown. At that checkpoint, a
separately authorized, then-unrun signal-recovery candidate could have closed
the environment without relabelling the original run. James had rejected
implementations `575756d` and `d4de863`; the latest correction closed the
remaining nested-alias, deadline, and atomic publication-race cases, passed its
2395/2395 full gate, and remained pending exact commit and James acceptance.

### 2026-08-21 KU-079 update - P0B environment cleared; task identity remains open

The accepted recovery invocation failed closed and is consumed; a separately
authorized, James-accepted operator cleanup subsequently cleared the exact
three residual helpers and restored `Y:` to retail. The final retained audits
contain zero processes, sinks, or sessions. The original P0B packet remains
`pending-cleanup-failed` at its append-preserving 26-file identity
`1092fcb9...25f2`; it is not a recovered or normally completed scientific
packet.

At this cleanup checkpoint, the only lifecycle observation was task
`2086681/34785536`, absent at sequences 0–26 and present at 27–520 in one
finite 521-point collection. Whether the topology would reproduce without a
debugger had not yet been tested; the following P0C update resolves only that
limited point. The task's name, creator, function, later persistence, and
relation to rendering remain unknown. KU-079 therefore remains fully open:
there is still no PC-confirmed render-command grammar, terrain/ground identity,
material, collision, visibility, causal, or no-effect conclusion. No further
runtime is authorized by this cleanup.

### 2026-08-21 KU-079 update - P0C reproduces topology and narrows an audio candidate

Offline P0C confirms a 16→17 post-title task transition in two independent
fresh processes: R2o D1-AH-005 and debugger-free P0B. P0B's sole identity
`2086681/34785536` is absent through sequence 26, present at 27–520, and has
complete generic `bugs.exe`/Tgid/status/executable metadata. This proves that
debugging is not necessary for the lifecycle class, but not that the R2o and
P0B TIDs are the same logical worker.

Static PC evidence makes the Level1a DirectSound stream worker the strongest
role candidate: the authenticated PLAYTRACK path synchronously reaches the
sole direct `CreateThread` call at `0x0042CF04` and worker `0x00440F50`, while
the P0B append records Level1a PLAYTRACK/SETMUSICVOL. The candidate remains an
inference because no receipt binds Linux TID `2086681` to that Windows start
routine. An early immutable 16-task census is disproved; a universal immutable
17-task census is also unsupported.

KU-079 remains open. This adds no render-command grammar, terrain/ground,
material, collision, visibility, causal, or no-effect conclusion. It permits
offline design of an R2q pre-attach quiet-census barrier only; no runtime,
memory, debugger, signal, or dynamic enrollment is authorized.

### 2026-08-22 KU-079 update - R2q quiet-census design frozen offline

R2q freezes a two-control barrier around the future R2o completed-present
observation. It prospectively requires 3,002 census requests per process at a
20 ms cadence, giving a first-to-last request span of 60.020 seconds, followed
by an immediate pre-attach revalidation. It does not freeze 17 tasks, any TID,
or any task role: each run's first post-gameplay census is its own baseline,
and the maximum permitted conclusion is pre-attach stability over the recorded
interval. Accepted acquisition remains separately bounded to 60.000 seconds.

The retained P0B evidence has zero post-gameplay samples and therefore supplies
no quiet-period threshold. At that historical `-011` boundary, the R2q
implementation had no runtime entry point or authorization. KU-079 remains
open in full: no PC render-command grammar,
terrain/ground identity, collision, material, visibility, causality, or
no-effect result follows from this offline protocol.

James rejected the first exact R2q correction `a8840d5` because its direct
builder did not semantically authenticate several retained P0B/P0C fields and
its receipt closure was descriptive. Immutable `-003` closed those raw fields,
but James rejected exact `caeddfd` / `ac853d4` because its runtime census,
manifest, journal, capture, and five-family D1/D2 schemas remained bypassable.
Immutable `-004` (`0f0f7cfe...05f9b`) made those boundaries executable and
cross-bound, but James rejected exact `0606bcf` / `ca7800e`: title chronology,
underlying guard hashes, stage/seize/detach identity, debugger-task lifecycle,
terminal namespaces/publication, D1-before-D2 chronology, process-group reuse,
and numeric aliases remained bypassable. Fresh `-005`
(`a5472f01...31c5e`) closes those cases with executable validators, including
seize-all/interrupt-all attach, selected natural hardware stops, nonselected
`PTRACE_EVENT_STOP`, exact memory/debug-register/detach receipts, authenticated
terminal state, and no-replace publication. It passes 150/150 focused tests;
the full candidate-tree gate passes 2620/2620 in 772.75 seconds with zero
tracked-file violations. At that `-005` freeze boundary, exact commit and
James re-audit remained pending; its later rejection is recorded below.
This changes no KU-079 scientific conclusion or runtime authority.

James then **REJECTED** exact `814ada4` / `b79e885` for ten remaining
executable-contract families. Pre-audit `-006` (`a068f686...1b33`) was
superseded because its D1 accepted-root tree hash was asserted. Fresh `-007`
(`f7cf2346...2d12`) additionally derives that canonical tree manifest and requires one
exact staged-drive Level01 load and unique markers; authenticates the D1→D2
namespace/one-shot/P0A handoff; binds raw audit, normal close, fresh-log inode,
mapping transitions, exact publication rereads/rename identity/durability,
and title tasks; derives breakpoint state from exact register-transition
ledgers with two EndScene resume/stop cycles; restores only from the R2o final
state; authenticates successful failed-action prefixes; keeps every active
cleanup/publication uncertainty pending; and rejects nested numeric aliases.
It passes 163/163 focused and 2633/2633 full candidate-tree tests with zero
tracked-file violations. At that `-007` freeze boundary, exact commit and James
audit remained pending; the later rejection is recorded below. KU-079 remains
fully open. This is still no render-command, terrain, ground, collision,
material, visibility, causality, or no-effect result, and it grants no runtime
authority.

James then **REJECTED** exact `ecf809f` / `71b294f` with authenticated
counterexamples for receipt reordering, unrelated failure cleanup, copied D1
tree/control rereads, ignored malformed later command-line bytes, and raw
two-control `TypeError`. Fresh immutable `-008` (`91401455...e155`) closes
those boundaries with an executable temporal partial order; one named maximal
failure prefix and attach/register-bound nonaccepted cleanup; pending uncertain
attach/partial acquisition; canonical D2 tree bytes and distinct post-D2
control rereads; publication parent/stat chronology; whole-command-line strict
UTF-8/NUL grammar; and `DesignError` aggregate rejection. It passes 175/175
focused and 2645/2645 first full-tree tests in 916.68 seconds with zero tracked-
file violations, pending exact commit/final gate and James re-audit. KU-079
remains fully open: this creates no runtime, render-command, terrain, ground,
collision, material, visibility, causality, or no-effect evidence.

James then **REJECTED** exact `-008` commit `18591f3` / tree `ff65061` for
terminal-state-dependent prefix semantics, later-failed cleanup/close-prefix
identity, action-9 failure-prefix binding, and impossible/unbound successful-
rename parent identity. Fresh immutable `-009` (`c8c451fa...047a1`) applies
title/mapping semantics to every present receipt prefix, cross-binds cleanup
and close receipts independent of later phase failure, binds action-9 timing
and validation before pending classification, and authenticates canonical
same-filesystem source-parent stat identity for terminal/comparison
publication. It passes 192/192 focused tests in 444.74 seconds and the
2662/2662 first full gate in 1102.04 seconds with zero tracked-file violations,
pending exact commit/final gate and James re-audit. KU-079 remains fully open:
none of
these offline validator corrections identifies a render command, terrain,
ground, collision, material, visibility, causality, or no-effect behavior, and
none grants runtime authority.

James then **REJECTED** exact `-009` commit `f81502b` / tree `e56942b` after
independently matching its hashes and passing 192/192 focused tests. A
coherent rejected terminal could drift the title-capture PID or gameplay-log
inode, exposing a broader conditional-reduction gap across every authenticated
dependency family. Terminal/comparison source-parent stat times also remained
unanchored to their enclosing publication or the post-D2 rereads. Fresh
immutable `-010` (`d07d3d5e...effd5c`) puts every dependency-applicable
accepted/rejected/pending relation in one reducer and enforces the complete
validation/outer/stat/fsync/rename/reread chronology. It passes 226/226
focused tests in 727.47 seconds and the 2696/2696 first full repository gate
in 1369.49 seconds with zero tracked-file violations, pending exact
commit/final gate and James re-audit.

KU-079 remains fully open. `-010` is still an offline evidence contract with
no runtime entry point. It identifies no PC render-command grammar, terrain or
ground source, collision linkage, material, visibility, causality, or
no-effect behavior and authorizes no launch, `/proc`, ptrace, memory, signal,
input, screenshot, or mapping mutation.

James then **REJECTED** exact `-010` commit `889f105` / tree `a93c929`: its
nominal executed process and exact same-path/SHA executable asset entry carried
contradictory device/inode/size/mtime identities. Fresh immutable `-011`
(`6a8fd3df...c1022`) cross-binds executable path/SHA/stat identity in the
accepted-control validator and conditional prefix reducer. Coherent direct and
accepted/rejected/pending terminal regressions recompute every dependent
process hash and envelope before rejecting that contradiction. It passes
229/229 focused tests in 740.93 seconds and the 2699/2699 first full gate in
1397.31 seconds with zero tracked-file violations, pending exact commit/final
gate and James re-audit.

KU-079 remains fully open. `-011` is still an offline evidence contract with
no runtime entry point. It identifies no PC render-command grammar, terrain or
ground source, collision linkage, material, visibility, causality, or
no-effect behavior and authorizes no launch, `/proc`, ptrace, memory, signal,
input, screenshot, or mapping mutation.

James then **ACCEPTED** the documentation-inclusive `-011` offline basis at
exact `409cbfb` / `de4fa87`, authenticating the three-note historical `-010`
byte-count correction and unchanged `-011` implementation/artifact hashes.
KU-079 remains fully open. Offline contract acceptance identifies no PC
render-command grammar, terrain or ground source, collision linkage, material,
visibility, causality, or no-effect behavior and grants no launch, `/proc`,
ptrace, memory, signal, input, screenshot, or mapping authority. A live R2q arm
requires fresh explicit user authorization.

### 2026-08-25 KU-079 update - R2q runtime edge remains audit-pending

The accepted `-011` boundary did not certify a runtime. James rejected exact
runtime-edge `-012` (`ac7e0b1` / `2acfa24`, 92,099 bytes /
`7fccf459...b8198`) and `-013` (`c54ed0f` / `cbd2e1b`, 94,739 bytes /
`bd0ec48c...b2b28`) for executable benchmark, journal, deadline, cleanup,
publication, commit, and failure-accounting defects. `-014` (99,092 bytes /
`6ec83b3c...20ff`) was superseded before an immutable James verdict. James
rejected `-015` (`6b2c867` / `bb27926`, 99,249 bytes /
`fe8a7712...a6f5`) after 44/44 independent runtime tests and 107 design tests,
and rejected `-016` (`5217ca0` / `c0420ca`, 99,969 bytes /
`432a4ede...8933`) after authenticating an identity-substitution
counterexample and the incomplete final deadline/ambiguity boundary.

Candidate `-017` moves acceptance to a final self-identity-bound completion
file after receipt durability, complete semantic validation, and a pre-final
tree reread. It validates the post-rename completion and whole tree under the
same runtime deadline, binds every later accepted-envelope tree to the
committed root/file identities, and preserves exact competitor or late-owned
envelopes only as authenticated pending ambiguity. Frozen `-017` is 102,029
canonical bytes / `c6fe10e2...2fa7` and passes 261/261 design plus 59/59
runtime tests. The full repository gate passes 2,790/2,790 in 1,843.51 seconds
with zero tracked-file violations; exact commit and James verdict remain
pending. No runtime occurred.

The user's retained authorization is narrower than R2q: one passive 521-point
P0A `/proc` lifecycle collection, with no process-memory read or write. R2q's
future scope contains ptrace/debug-register operations and eleven post-seize
memory reads per control, so that authorization cannot activate it. KU-079
remains fully open, as do KU-080 and KU-081: this work identifies no PC render
grammar, terrain/ground source, collision linkage, material, visibility,
causality, no-effect behavior, or retail-executable result.

### 2026-08-25 KU-079 update - R2q `-018` complete-publication correction

James rejected exact `-017` `2267cc5` / `8166cc4` after authenticating its
artifact and gates. The blockers were evidentiary, not terrain findings: the
five-second accepted-publication budget had never been benchmarked over either
complete production path and was impossible for the nominal comparison; a
valid complete envelope arriving before attempt construction was unaccounted;
and readable post-rename files were incorrectly treated as durable after the
final directory fsync failed.

Frozen `-018` distinguishes complete-envelope validity from owned durability
and records the exact final fsync/reread/tree/deadline stage. Valid non-owned
competitors, owned durability uncertainty, and genuinely durable-but-late
envelopes have separate pending outcomes. An anchored three-trial production-
path benchmark measures 23.167699052 seconds worst control and 79.340400010
seconds worst comparison under a prospective 180-second publication ceiling.
Frozen artifact: 103,156 bytes / `435df625...d382`; focused tests: 262 design /
68 runtime. The full gate passes 2,800/2,800 in 2,003.33 seconds with zero
tracked-file violations; exact commit and James verdict remain pending.

This resolves only the rejected evidence-publication defects. No live R2q arm
ran and the retained passive P0A authorization cannot activate its broader
scope. KU-079, KU-080, and KU-081 therefore remain open: no PC render grammar,
terrain/ground source, collision linkage, material, visibility, causality,
no-effect behavior, or retail-executable result has been established.

### 2026-08-25 KU-079 update - R2q `-019` deadline and provenance correction

James rejected exact `-018` `7e6a3b0` / `2c99bef` after authenticating its
artifact, benchmark, source/test/wrapper hashes, runtime tests, and clean Git.
The remaining blockers were evidence-accounting defects: owned-late could be
asserted without the actual deadline receipt, the claimed 30-second failure-
recording bound was not end-to-end, and benchmark `-004` did not retain the
production source versions it timed.

Frozen `-019` binds the exact deadline code/value/observation/checkpoint to the
runtime exception, completion deadline, rename chronology, and outer failure.
It accurately limits 30 seconds to the failed/skipped journal-transition tail
and declares the whole failure-accounting path unbounded. Two-phase benchmark
`-005` records clean source commit `3fe4833` / tree `5953ebf` and exact ledger
`01abbe48...341f` before and after three complete control/comparison trials.
Benchmark: 4,563 bytes / `64537622...28fa`, worst 78.945117065 seconds under
180. Frozen artifact: 104,745 bytes / `f3d985a5...eadf`; focused gates: 263
design / 68 runtime. The first full gate passes 2,801/2,801 in 2,205.27 seconds
with zero tracked-file violations; exact final commit and James verdict remain
pending.

This still adds no runtime evidence. KU-079, KU-080, and KU-081 remain open:
no PC render grammar, terrain/ground source, collision linkage, material,
visibility, causality, no-effect behavior, or retail-executable result has
been established. Passive P0A authority cannot activate R2q.

### 2026-08-25 KU-079 update - R2q `-020` outer-failure closure

James authenticated exact `-019` `8e1b989` / `c3334e3` and confirmed all prior
deadline, timing-claim, and source-provenance blockers corrected. He rejected
it because owned final-deadline assertions still admitted impossible outer
exception/phase/chronology combinations, and malformed `stage` could escape as
raw `TypeError`.

Frozen `-020` binds the outer exception type, one exact boundary message,
comparison `commit-marker` phase, and direction-specific start/observation/
completion chronology. It type-checks `stage` before closed lookup and rejects
list, dict, integer, Boolean, and null values as `DesignError`. Benchmark `-006`
is 4,563 bytes / `72373103...e95b`, sourced from clean `9e4ccf7` / `f2502d8`
with ledger `0f184368...bcf27`; worst complete path is 78.864340257 seconds
under 180. Frozen artifact is 105,429 bytes / `462b882d...061a`; the complete
R2q gate passes 331/331 in 1,799.86 seconds. The first full repository gate
passes 2,801/2,801 in 2,458.12 seconds and the documentation-complete exact-tree
gate passes 2,801/2,801 in 2,457.27 seconds, both with zero tracked-file
violations. James **ACCEPTED** exact `4635a53` / `fa5d63d` after independently
confirming provenance, validators, production failure semantics, malformed-
case rejection, runtime tests, and both strengthened terminal arms.

This is still offline evidence-accounting work. KU-079, KU-080, and KU-081
remain open: no PC render grammar, terrain/ground source, collision linkage,
material, visibility, causality, no-effect behavior, or retail-executable
result has been established. Passive P0A authority cannot activate R2q.

### 2026-08-26 KU-079 update - P0D consumed offline; P0E pending James

James rejected the initial P0D design for six attempt/source/publication/Y:/
census/host provenance defects. A test-harness invocation then created P0D's
real exclusive marker and stopped before activation, so P0D is consumed even
though no game or collection ran. The preserved marker is now an explicit
historical exclusion.

Fresh P0E retains the proved PC auto-hardware, `Right`, select-`Return`,
positive Level01 gate, title-`Return-at-sample-5` route. Its corrected offline
boundary has earliest attempt consumption, a two-phase tracked Git/source
anchor, an independent Wine-host identity, atomic bidirectional `Y:` changes,
an immediate complete audit/census before restore, unverified-only runtime
publication, and P0A/P0B/P0D before/after preservation. Focused tests pass
519/519 at the first freeze. James rejected exact `b7777539` / `85799be`
because a byte-identical P0D inode replacement and impossible/copied
publication roots could validate. P0E now pins P0D's original physical
identity and enforces exact roots plus publisher-reachable phases; the expanded
suites pass 542/542; James's independent 106-case matrix also passes. Corrected
source `c7bdd6c` / `e0a5fea` passed 3343 tests and is bound by activation anchor
`7342d72...08c5d`. At that pre-run point P0E was unconsumed and absent. The
final full gate,
commit, and James exact-tree ACCEPT remain prerequisites. KU-079, KU-080, and
KU-081 remain open. This candidate supplies no task-lifecycle observation,
terrain/ground source, collision linkage, material, visibility, causality,
no-effect behavior, or retail-executable result.

### 2026-08-26 KU-079 update - P0E collection accepted; cleanup pending

James accepted exact pre-run `b1896e1` / `a696e48` and the sole authorized P0E
run completed the exact Anthill Level01 route and 521-point passive grid.
Collection `9ed7d8e...456b0` confirms one persistent task addition at sequence
27 through 520 from a 16-identity baseline, without removals or reuse. James
accepted this at collection level only. The added identity belongs to the game
TGID, but its creator/role remains unknown; DirectSound-worker attribution is
still inference.

Normal close failed, so the packet remains pending, `Y:` remains staged, and
the residual game stack/sink remain present at the recorded nonclear audit.
P0E cannot rerun and terminal acceptance is withheld. KU-079, KU-080, and
KU-081 therefore remain open: this narrows lifecycle topology but establishes
no render grammar, terrain/ground source, collision linkage, material,
visibility, or causality. Recovery now requires separate explicit authority and
a frozen additive protocol.

### 2026-08-27 KU-079 update - Y-only restoration successor WIP

Fresh authority now covers one atomic stage-to-retail `Y:` restoration, and a
four-file successor is banked for handoff. Its focused and combined suites pass
96/96 and 357/357. James rejected earlier candidates through round 26; the
current revision applies his cleanup-repair chronology lower bound and
controlled error grammar. Round 27 confirmed those fixes but rejected missing
and ancient mapping-repair provenance on a coherent `mapping-fsync-once`
packet. No activation anchor exists and no wrapper invocation, mapping write,
runtime collection, input, signal, sink, or process-memory action occurred. A
preliminary audit fixture made one read-only production session-audit call and
no mutation.

KU-079, KU-080, and KU-081 remain unchanged. The WIP can restore an environment
prerequisite only; it cannot identify the persistent task, observe a render
grammar, bind visible ground to collision, or establish material, visibility,
causality, no-effect, or retail-executable behavior. See
[[2026-08-27 0816 - Codex - P0E Y restoration hard-truth checkpoint]].

### 2026-08-27 KU-079 update - Y-only restoration source and activation frozen

James rounds 28 through 34 closed all known mapping/cleanup repair provenance,
chronology, durability, and state-consistency gaps in the Y-only successor.
Round 34 accepted exact module `541fbe59...3d57`, wrapper
`9c9dbb28...ea80`, freezer `640aefb1...42bc`, and tests
`bad67fe1...e6111` after independent 98-case focused and 741-case broad P0E
runs. Source `1964eec` / `f0afa1a` passed the 3,542-test repository gate and
is bound by activation anchor `95e632dc...d8307`.

This closes only the offline source and activation prerequisites. The attempt
marker is absent, the wrapper has not run, and `Y:` remains staged. KU-079,
KU-080, and KU-081 remain open: no persistent-task role, render grammar,
terrain/ground source, collision linkage, material, visibility, causality,
no-effect behavior, or retail-executable behavior follows. See
[[2026-08-27 1457 - Codex - P0E Y restoration source and activation freeze]].

### 2026-08-27 KU-079 update - failed v1 preserved; recovery activation frozen

The sole James-authorized Y-only v1 invocation consumed its arm and failed
before a mapping action because the packet inventory did not observe its newly
linked owned authority leaf. James accepts the authority-only packet only as
failed evidence. `Y:` remains staged and v1 cannot retry.

A distinct mapping-only recovery now has James source-freeze acceptance. It
binds the exact v1 closure, uses fresh bound directory descriptions, repairs
exact owned-link bookkeeping, authenticates final packet-fsync chronology, and
binds attempt time in the marker bytes. Its 115 focused and 3,559 repository
tests pass. Source `32d8a83` / `08ea9ad` is frozen by activation
`62e05bb5...be69`; the new marker is absent and the wrapper has not run.

KU-079, KU-080, and KU-081 remain open. This advances only the environment
precondition for the accepted R2q design. It establishes no render grammar,
visible terrain/ground source, collision linkage, material, causality,
no-effect behavior, or retail-executable result. See
[[2026-08-27 1919 - Codex - P0E Y restoration failed v1 and recovery freeze]].

### 2026-08-28 KU-079 update - YR2 consumed; recovery2 activation frozen

YR2 consumed marker `d89441a5...98dd` and stopped with an empty event journal
before mapping; its exact four-leaf pending packet and all terminal absences
are bound into the successor. It cannot retry. `Y:` remains staged and `R:`
remains P0A.

James rounds 31 and 32 accepted the provenance-free cumulative sink journal
and the exact fresh authority-bearing recovery2 source. The 162 focused, 805
broad P0E, and 3,606 full-repository tests pass. Source `14e4a43` /
`3e55361` is bound by 44,957-byte activation `c611240a...b2ead` over 21 exact
files plus the complete YR1/YR2 closure. The YR3 marker is absent and its
wrapper has not run.

KU-079, KU-080, and KU-081 remain open. This advances only the mapping-baseline
prerequisite for R2q; it identifies no persistent-task role, render grammar,
terrain/ground source, collision linkage, material, visibility, causality,
no-effect behavior, or retail-executable behavior. See
[[2026-08-28 1155 - Codex - P0E Y restoration recovery2 activation freeze]].

### 2026-08-28 KU-079 update - recovery3 activation frozen

The distinct YR4 successor binds consumed YR3's exact failed state, correctly
parses retained PipeWire multiline records, keeps prior-boot chronology out of
current-attempt ordering, physically reauthenticates predecessor state across
the allowed Y transition, and cross-binds both copies of YR1/YR2 history.
James rounds 39 and 40 accepted the source and fresh authority. The 202 focused,
845 broad P0E, and 3,646 repository tests pass. Source `9a815a3` / `27b23a`
is frozen by activation `111fbc78...6fcb` over 25 files plus the full closure.

KU-079, KU-080, and KU-081 remain open. The YR4 marker is absent, `Y:` remains
staged, and the wrapper has not run. This advances only the mapping-baseline
prerequisite; it identifies no persistent-task role, render grammar,
terrain/ground source, collision linkage, material, visibility, causality,
no-effect behavior, or retail-executable behavior. See
[[2026-08-28 1704 - Codex - P0E Y restoration recovery3 activation freeze]].

### 2026-08-28 KU-079 update - retail Y restored, unknowns unchanged

The sole YR4 invocation produced consumed marker `b109d6ca...c5e00` and
validated 28-entry published tree `9a4979ca...e46c6`. James round 43 accepts
exactly one durable stage-to-retail Y exchange, P0A `R:` unchanged, preserved
predecessor evidence, and zero runtime/input/signal/sink/process-memory
actions. The post-action audit is exactly clear and `Y:` now points to retail.

KU-079, KU-080, and KU-081 remain open. `terrain_collision_claim` is `null`,
future runtime is unauthorized, and the mapping result identifies no render
grammar, terrain/ground source, collision linkage, material, visibility,
causality, no-effect behavior, or task role. R2q requires separate fresh
runtime authority. See
[[2026-08-28 1704 - Codex - P0E Y restoration recovery3 activation freeze]].

### 2026-08-30 KU-079 update - R2q `-022` frozen offline, unknowns unchanged

Round-91 source now binds full-frame pre/post SHA-256, byte count,
mtime/ctime, and timing around one-shot file fsync; the exact
corruption→fsync→restore-without-fsync discriminator rejects. After preserving
valid immutable design-021, James round 96 accepted the fresh `-022` successor
source at `3998111` / `0c61a85`. Benchmark-008 accepts with worst complete
comparison 80.520710670 seconds, and activated design-022 is 8,061,582 bytes /
`b79f63b0...e6b72`. Runtime/freezer tests pass 157/157 and the full gate passes
3,786/3,786.

KU-079, KU-080, and KU-081 remain open. This work authenticates offline
evidence-accounting and publication behavior only. No game, R2q runtime,
process observation, ptrace, process-memory read, renderer observation,
terrain/ground identification, collision linkage, material, visibility,
causality, no-effect behavior, or task-role evidence was produced. Separate
fresh explicit runtime authority remains mandatory. See
[[2026-08-30 1519 - Codex - R2q hard-truth source and activation freeze]].

### 2026-08-30 KU-079 update - R2q-022 failed; retail mapping recovered

The sole R2q-022 D1 arm stopped during launch identity stabilization and is
consumed failed evidence. It yielded no accepted quiet census, debugger
capture, completed-present comparison, or terrain/collision observation. Its
exact failed closure is preserved; neither its cleanup nor the later mapping
recovery permits a retry.

A separately frozen and authorized mapping-only successor ran exactly once.
Its 28-entry packet tree `f3cf883f...a5824` and mapping receipt
`96baab75...cc2c5b` authenticate one D1-stage-to-retail `Y:` exchange,
parent/quarantine durability, zero rollback, unchanged P0A `R:`, and zero
runtime/input/signal/sink/process-memory action. James returned `ACCEPT
EVIDENCE`; the post-action audit is clear. Live `Y:` inode is `9525237`, the
retired D1 link is quarantine inode `9458103`, and `R:` remains inode
`9054047`. The post-action repository gate passes 3,811/3,811 in 3,270.71
seconds with zero tracked-file violations.

KU-079, KU-080, and KU-081 therefore remain open. The packet explicitly has
`terrain_collision_claim:null`; mapping repair identifies no persistent-task
role, render grammar, terrain/ground source, collision linkage, material,
visibility, causality, no-effect behavior, or retail-executable behavior. A
future terrain/collision runtime design must be a distinct fresh successor
with separate authority; R2q-022 cannot retry. See
[[2026-08-30 2221 - Codex - R2q-022 failed-run mapping recovery]].

### 2026-08-31 KU-079 update - R2q `-024` frozen offline, unknowns unchanged

Immutable `-023` is preserved at 12,035,411 bytes / `be7cf41f...08cd3c`
after its activation suite exposed restore-authority fixture defects and a
valid maximum-shape continuity packet above the old raw fallback ceiling.
James accepted the corrected fresh `-024` source at `022f739` / `9d78651`.
Protocol v6 uses a 320 MiB raw ceiling while retaining the 128 MiB stored-data
reservation. Benchmark-010 accepts with worst complete comparison
79.652494057 seconds; design-024 is 17,336,651 bytes /
`321eb8c6...2288`; the full gate passes 3,843/3,843.

KU-079, KU-080, and KU-081 remain open. This work validates offline
publication, provenance, mapping-authority projection, and capacity behavior
only. It produced no game/process observation, quiet census, persistent-task
role, render grammar, terrain/ground source, collision linkage, material,
visibility, causality, no-effect behavior, or retail-executable result. Any
runtime successor requires distinct fresh explicit authority. See
[[2026-08-31 0648 - Codex - R2q 024 hard-truth activation freeze]].

### 2026-08-31 KU-079 update - R2q-024 failed; `-025` frozen offline

The sole `-024` D1 arm failed during `stage-and-launch` on an exact process-
maps read-binding mismatch. It reached no accepted quiet census, debugger
acquisition, or completed-present comparison and is consumed. Its separately
authorized mapping-only recovery restored retail `Y:` exactly once; James
accepts tree `afacab0a...90bfa` and receipt `ed20963a...033` only as durable
mapping evidence with zero runtime/scientific action.

Fresh source `d23ece3` / `8492bcb` raises one-shot protocol v7 capacity to a
448 MiB raw ceiling and 192 MiB data reservation after exact maximum valid
accounts exceeded `-024`'s bounds. Benchmark-011 and immutable design-025
accept offline at `9ec2ec6a...d79` and `d25acc8c...34a9`; the final full gate
passes 3,878/3,878.

KU-079, KU-080, and KU-081 remain open. The `-024` failure and recovery do not
identify a persistent-task role, render grammar, terrain/ground source,
collision linkage, material, visibility, causality, no-effect behavior, or
retail-executable behavior. The `-025` artifact is runtime-unauthorized and
adds only offline provenance/publication/capacity assurance. A live successor
requires fresh exact authority. See
[[2026-08-31 1849 - Codex - R2q 025 activation freeze]].

### 2026-09-01 KU-079 update - R2q-025 failed; retail mapping recovered

The sole R2q-025 D1 arm failed before science because bounded game-process
maps did not converge during `stage-and-launch`. Its exact terminal packet is
`d1a33753...fa04`; it contains no accepted quiet census, debugger acquisition,
stopped-memory capture, screenshot comparison, or D2 result. The arm is
consumed and cannot retry.

A separately frozen and authorized mapping-only successor ran exactly once.
James accepts its 28-entry packet tree `0b0aa411...f4d2b` and receipt
`f37158da...c383` as one durable D1-stage-to-retail Y exchange, zero rollback,
retail inode `9773754`, retired D1 inode `9770116`, unchanged P0A R inode
`9054047`, and zero runtime/input/signal/sink/process-memory action. The full
post-action gate passes 3,905/3,905 and the session audit is clear.

KU-079, KU-080, and KU-081 remain open. `terrain_collision_claim` is null;
neither the failure nor mapping repair identifies the persistent task, render
grammar, terrain/ground source, collision linkage, material, visibility,
causality, no-effect behavior, or retail-executable behavior. Any continuation
must be a fresh offline successor that preserves this closure and solves the
process-map convergence blocker before seeking new exact runtime authority.
See [[2026-09-01 0317 - Codex - R2q 025 failed-run mapping recovery]].

### 2026-09-02 KU-079/KU-080/KU-081 update - R2q-028 frozen offline

R2q-027 corrected the R2q-026 cross-mount-namespace provenance defect, but its
post-activation gate found two stale anchored test expectations. James
therefore rejected finalization; the immutable design never ran. Fresh
R2q-028 preserves that design and its exact `8375369c...4fb` rejection receipt,
uses only process-namespace executable device/inode identity against process
maps, advances all prospective runtime/publication names, and proves all 28
unused R2q-027 paths absent.

James accepts R2q-028 source `68e0714` / tree `cda3886`, benchmark-014
`83cf0963...d05e`, design-028 `c5840fe9...e087`, and activation. The complete
post-activation repository gate passes 3,972/3,972. This is source and design
evidence only: no game, census, task attribution, stopped-memory capture,
screenshot comparison, or D1/D2 scientific result exists. KU-079's persistent
task identity/role, KU-080's renderer-facing causality, and KU-081's terrain/
collision interpretation therefore remain open. Any runtime requires a later
fresh explicit authorization for the exact accepted R2q-028 activation. See
[[2026-09-02 0056 - Codex - R2q 027 rejection and 028 activation freeze]].

### 2026-09-04 KU-079/KU-080/KU-081 update - R2q-032 activation banked, final gate incomplete

R2q-028 stopped at a read-only pre-lock remount-provenance check. Offline
successors R2q-029 through R2q-031 were preserved after distinct finalization
or activation rejections. James accepts R2q-032 source `45ae953` / tree
`2292c1a` and immutable design-032 `0604d37d...b2b8` at activation commit
`b6abcb2`. Focused final tranches pass, but the full repository gate was
interrupted without a terminal summary and therefore remains unresolved.

No game, quiet census, persistent-task attribution, stopped-memory capture,
screenshot comparison, or D1/D2 scientific result occurred. KU-079's render
grammar/runtime join, KU-080's lateral-versus-height collision behavior, and
KU-081's render-side collision-descriptor linkage all remain open. Resumption
starts with a fresh complete offline full gate, not a wrapper invocation. See
[[2026-09-04 1711 - Codex - R2q 032 activation bank and incomplete final gate]].

## 2026-09-05 bounded original-wall material question

[[EXP-20260905-005 - Original wall texture regions and colour inputs]] confirms
that nearby original steep-face samples select other page-0 UV regions and
varying warm channel triples compared with the authored box's floor region
and uniform neutral channels. The later original runtime extracts page0 and
confirms different floor/wall region pixels, with the wall view confirmed by
the user. The exact screenshot-pixel-to-face join remains open. Next distinguish region-only, colour-only and
combined edits against a baseline; do not promote the untested uniform 3/5
shade draft to an OG match. This does not reopen collision or R2q work.

EXP-005 combined application update: original-region-only, colour-only and
combined fixtures now exist and pass offline preservation regressions. The
combined box preview is running with original wall-region UVs and a deliberately
chosen donor-derived warm vertical gradient. Exact face XYZ, top/ramp/deck
appearance and collision are unchanged. User accepted the combined wall appearance;
independent live four-arm attribution and universal material/mesh
rules are not claimed. No need to reopen banked collision or R2q work.

## 2026-09-05 bounded mesh-growth and texture-density follow-up

[[EXP-20260905-006 - World-scale terrain tiling and checked mesh growth]] narrows
KU-079: a repeated-tile candidate exceeds the original allocation safely in an
original-PC relocation comparison, with its trailing-data base preserved and
collision unchanged. It does not prove cold file allocation, all-view occlusion,
performance or general repacking. Tile size512 is an authoring choice; projected
ramp density and at most1/2-stored-unit vertex rounding require visual inspection.
The current user-approved EXP-005 preview is preserved; EXP-006 is unlaunched.

EXP-006 runtime update: the user-authorized cold-load preview now verifies the
complete enlarged resident mesh, unchanged collision and retained trailing-data
pointer. This closes the unrun cold-load question for this exact343,012-byte
DAT only. Texture-scale approval, movement/view regressions, performance and
generic packaging remain open. 2026-09-05 - Codex - Tiled terrain user preview.

## EXP-007: active floor coverage outside the authored deck

[[EXP-20260905-007 - Retail position control and missing floor footprints]] confirms that retail cells `44140` and `44248`, used during the OG Up control, and cell `45884`, covering the earlier fall endpoint, have no active parsed floor candidate at their footprints in the authored terrain. Source-99 replacement is a concrete coverage difference. The exact earlier-fall admission trajectory and the separate invisible-render/retained-collision location remain unresolved. A latched contact pointer is not sufficient evidence of grounding; the authorized teleport retained its old pointer until movement.

## EXP-008 resolves collision-edit extent, not integrated-layout safety

[[EXP-20260905-008 - Whole-Level01 collision and render coverage audit]] confirms that source 99 alone changed among all 189 TERRAIN.ALL sources. All 134 original source-99 cells are retired, 14 authored cells replace them, and 7,147 other active cells are unchanged. The other 188 payloads, all 262 barrier segments, and the other 14 Level01 files are unchanged. The suspected additional source edits are not present in these hash-pinned copies.

Still open: additive collision/render storage without sacrificing originals, exact earlier-fall native-instruction replay, same-height coverage rather than projected overlap, the user's exact invisible-ground location, and world projection for 28 unchanged rotated/scaled static references. One changed source spans a broad area; this must not be reduced to one small hole. Preserve original render mesh 160 and collision source 99 together when designing the integration candidate, rather than assuming they share a footprint.

## EXP-009 additive allocation: preservation is not traversal acceptance

The corrected writer passes the final 224-test terrain gate, native loader/relocator/command traversal, restored fall landing, banked box movement and four continuous original-floor crossing/return routes. Exact-point controls remain failures, but fixed/adaptive and downward-input discriminators now support a bounded controller explanation: near the target, the 512-downward request becomes almost normal-directed on original cell 44140 and horizontal progress stalls outside the 128-unit tolerance. This is not evidence of a hole. No asset edit was needed to pass the separately declared through-crossings; old failed criteria are retained. Remaining unknowns are runtime old/new geometry overlap, enlarged-batch visibility/sorting, zero depth bias and full actor/input behavior. These finite results do not solve universal additive authoring or exact-point navigation on arbitrary slopes. See [[EXP-20260905-009 - Additive terrain preservation and access ramp]] and `reports/terrain/EXP-20260905-009-validation.json`.

### EXP-009 automatic-renderer menu title

The fresh auto-hardware startup passes six renderer markers and the LevelSelect log gate, but its owned 640x480 window is titled `Loading - A Bugs Life`; the new operator's exact `Bugs` predicate rejects it. The mismatch must be reconciled as a phase/build-scoped control condition, not silently promoted to a global relaxed window guard. No Level01 input or terrain runtime comparison followed. Evidence: `reports/terrain/EXP-20260905-009-runtime.json`. Existing offline terrain acceptance is unaffected.

### EXP-009 runtime-entry boundary (2026-09-06)

The window-title startup blocker is resolved for the exact authorized session; Level01 and resident additive collision/render streams are confirmed. Original-start ground is visible and source-99 cell 47716 is the observed contact. Live uphill/downhill connector traversal, fall onto retained original ground, return, box contacts and combined-mesh visibility/overlap are still unaccepted until playtested. The runtime helper reports `terrain_base=0` even while descriptor-based payload comparison and contact succeed; do not infer missing collision from that field. See `reports/terrain/EXP-20260905-009-runtime-entry.json` and [[EXP-20260905-009 - Additive terrain preservation and access ramp]].

### EXP-009 camera-dependent ramp visibility (2026-09-06)

User ramp crossing report is positive, but visual acceptance now has a reproduced defect: appended ramp cell 49008 remains the sampled contact while the distinct ramp strip is absent in early views and visible after camera rotation, at identical post-tap actor position. Do not mistake visible old ground for the contact source. Root cause remains unresolved among object/bounds culling, face/clipping rejection and draw ordering/overlap. User-reported flashing needs denser temporal evidence. Next: original-PC render-path comparison at recorded cameras to distinguish pre-command, per-face and post-submission visibility loss. Evidence: `reports/terrain/EXP-20260905-009-ramp-visibility.json`; [[EXP-20260905-009 - Additive terrain preservation and access ramp]]. No collision rewrite justified by this observation.

### EXP-009 whole-mesh culling contributor (2026-09-06)

Native offline scene-gate replay now reproduces a specific rejection at `0x0044D677` in two hidden views; 6047 is insufficient at the inherited mesh centre, while offline radius 8192 admits all five sampled cameras. This narrows the previous unselected hypotheses but is not a live causal radius result. Contradiction retained: one intermediate screenshot lacks a distinct ramp although its captured pose passes the gate with 6047. Temporal pairing/framing, per-face rejection and later depth/ordering are unresolved for that sample. Proposed discriminator: exact authorized reversible radius-only live A/B/A, without actor/camera/collision writes, followed by camera sweep and residual analysis if accepted. `reports/terrain/EXP-20260905-009-ramp-culling.json`; [[EXP-20260905-009 - Additive terrain preservation and access ramp]].

### EXP-009 culling cause confirmed live at one fixed pose (2026-09-06)

The exact authorized radius-only A/B/A reversibly restores/removes the ramp surface without changing recorded actor position, camera or appended-ramp contact. Culling is therefore a confirmed contributor at this pose, no longer merely an offline prediction. Radius 6047 is restored and files remain unchanged. General bounds sizing, suitable scene partitioning/recentring, all-angle acceptance, the earlier intermediate discrepancy and flashing frequency remain open. Do not turn the 8192 discriminator into a universal rule. `reports/terrain/EXP-20260905-009-ramp-radius-live.json`; [[EXP-20260905-009 - Additive terrain preservation and access ramp]].

### EXP-20260906-001 bounds fix: offline accepted, live unaccepted

PC view-plane-aware bound8560 replaces6047 in a file-only successor. Native finite sweep rejects0/5152 relevant candidate views versus544 control views;5 historical cameras pass. This does not prove an all-angle quantisation bound, rasterization/depth correctness or resolution-independent authoring. Earlier intermediate-angle discrepancy and reported flashing stay open. Fresh file-loaded runtime is pending scoped cleanup approval for the old session, which did not exit normally. Collision/geometry/control copy remain unchanged. [[EXP-20260906-001 - PC-compatible ramp visibility bounds]]; `reports/terrain/EXP-20260906-001-validation.json`.

### EXP-001 fresh-load prerequisite complete (2026-09-06)

The cleanup/launch blocker is resolved. Corrected bound8560 is confirmed loaded from disk in fresh Level01, with collision and geometry unchanged. User must still repeat the ramp's downhill and short-turn/side-angle views; all-angle visibility, prior intermediate-view discrepancy and flashing remain unaccepted. No additional live memory intervention was used. `reports/terrain/EXP-20260906-001-runtime.json`; [[EXP-20260906-001 - PC-compatible ramp visibility bounds]].

### EXP-002 decorative sides after positive EXP-001 manual feedback (2026-09-06)

The user says the corrected ramp now seems to work. This narrows the live
feedback gap at manual scope, not universal angle/quantisation or flashing
coverage. EXP-20260906-002 adds dark tiled
below-floor skirts with unchanged collision/top/bound8560. Ground-line geometric
coverage and offline preservation tests pass; skirt cold-loading, low-angle
appearance, buried overlap, seams and sorting await a fresh preview. No lateral
collision is implied. The initial helper's false coverage rejection was a field
layout bug corrected with the established parser, not an original-floor hole.
Evidence: `reports/terrain/EXP-20260906-002-validation.json`.

### EXP-002 runtime: absent side blocking and separate ground-join symptom

Cold-load identity is now verified and user appearance feedback is positive.
The requested1-second Up trace crosses both new side planes, confirming absent
lateral blocking for the render-only skirts. Existing floor collision remains
unchanged; matching wall collision is a missing authoring component, not an
unexplained loss of original coverage. Separately, two user screenshots suggest
wall protrusion at the ramp/ground join. Preserve the paused view; exact face
mapping and geometric intersection versus draw-order/overlap cause remain open.
No proposed fix has been applied. EXP-20260906-002;
`reports/terrain/EXP-20260906-002-runtime.json`, `...-ground-join.json`.

### EXP-003: side blocking narrowed, ground-trim appearance still open

Twenty box-style wall cells block all four native-model outside approaches,
where the visual-only controls cross. This does not prove full actor stability:
two western final flags are[1,0]. Original floors remain unchanged. The western
fixed-axis return misses the entrance identically in control/candidate after
normal X drift; three continuous explicitly steered up/down/up routes pass.
Keep the failed criterion rather than editing geometry to hide it.

Original render124/128 contours bound the new trim; one sub-unit west seam is
bridged only in the authored contour.28 rotated references remain unresolved in
the orientation census. Exact screenshot face attribution, depth/overlap cause,
small quantized seams and live trim efficacy remain open. EXP-003 is unlaunched
pending approval to fix a reversed new synthetic test fixture;72 terrain tests
pass. [[EXP-20260906-003 - Solid ramp sides and ground contour trim]];
`reports/terrain/EXP-20260906-003-validation.json`.

## 2026-09-06: wall-clearance/occlusion acceptance after solid-side preview

[[EXP-20260906-003 - Solid ramp sides and ground contour trim]] now has user-confirmed side blocking, but Flik's model visibly enters/disappears behind a side when approached. This is a general **acceptance question**, not yet a general collision defect. Unknown: native wall stop clearance versus body envelope, draw-order/depth contribution, original-wall parity, and any warranted world-space padding. One associated captured root is 267 world units outside the authored west plane; not a collider-radius measurement. Preserve candidate as control and compare original/authored wall stop intervals and views before choosing collision padding or render inset. Ground-trim efficacy remains a separate unconfirmed visual outcome. Evidence and discriminator: `reports/terrain/EXP-20260906-003-runtime.json`, 2026-09-06 - Codex - Solid ramp preview handoff. Earlier correction-pending/unlaunched status is superseded: 138 affected tests pass and Level 1 preview is live.

## 2026-09-06: EXP-004 local clearance trial, visual/corner acceptance open

[[EXP-20260906-004 - Wall clearance comparison and offset trial]] moves only the20 selected side-wall groups outward48 stored units (1536 world units); LEVEL.DAT is unchanged. Selected nearby original/render separations support this local choice, but opposite-sign examples rule out a uniform original-wall offset claim. A supplied-point native case reaches zero wall distance; this is not a measured Flik radius.69 affected tests, both native arms and72-test terrain gate pass; the candidate is file-loaded in Level1. Remaining: user-visible overlap reduction, actor/wall ordering contribution, corner/end entry into the added clearance strip (not exhausted by center-lane foot routes), and separate ground-contour trim efficacy. Live original-wall navigation did not reach a matched control and was stopped after leaving the upper terrain. Report `reports/terrain/EXP-20260906-004.json`.

## 2026-09-06: EXP-005 isolated layout boundary

[[EXP-20260906-005 - Isolated authored terrain and platform spawn]] natively reaches only 36 authored cells, suppresses old scene draws in both dispatchers and preserves new ramp/box routes. No runtime acceptance yet. The initial spawn consumer is now statically identified as executable-table 0x0043E6B0 / Level01 row 0x004DC7F4, not a DAT/type-1 row; observed native coordinates are (192000,-102528,448000). The new proof omitted unchanged heading data from its zeroed image, so the complete spawn/settle arm remains failed pending the disclosed setup correction. Keep that failure distinct from terrain or output executable correctness. Open: actual stripped runtime scenery, dynamic actor remnants, startup/respawn, freestanding ramp skirt appearance and inherited wall-clearance/corner limitations. No universal absence claim about independent actor collision systems.

## 2026-09-06 original foliage boundary reference

[[EXP-20260906-006 - Perimeter barriers and original foliage reference]] saves the user-selected tall-grass view at original Level01 XYZ(292407,-31849,537453), facing979/related angle976. Exact render-record and responsible barrier-segment correspondence are unknown. Visual foliage is not yet proved to carry collision itself. Berries stopping and Flik blocking require separate discriminators. Earlier short-loop perimeter trial remains unaccepted:14/32 positive winding,0/32 negative and0/32 control; no cause selected from that aggregate. EXP-005's formerly pending spawn setup is corrected (10/10 native); its preview is now closed, and the original-asset reference session is deliberately open. No new universal boundary or wall radius claim.

## 2026-09-06 grass reuse and remaining bounds

[[EXP-20260906-006 - Perimeter barriers and original foliage reference]] now identifies original source180 segment160 as the separate XZ response at the saved grass view through original-PC positive/head-cleared arms. The initial14/32 score is not18 falls: all positive samples remained over the floor, and the original blocked control also yields[1,0]. A longer matrix contains32/32 approaches but only31/32 meet straight-release/settle criteria; lower-ramp edge2 needs further characterization, although steered return succeeds. User reports current grass-preview blocking works with no falls. This does not close all-state/perimeter or projectile equivalence questions.

Off-screen file inventory34 placements/31 meshes/439 raw candidates is not an all-foliage or live-RAM census. Filtered381 tall-grass templates support a new202-template visual mix; its collision is identical to the confirmed preview, but aesthetic/culling-angle acceptance is pending a switch. The original Level01 texture pipeline remains a dependency; standalone atlas import/general new-level packaging is not solved here.
<!-- preserved-body:end -->
