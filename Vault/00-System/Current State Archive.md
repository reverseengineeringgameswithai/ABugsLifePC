---
type: archive
status: historical
updated: 2026-10-29
tags:
  - system/state
  - system/archive
---

# Current State Archive

Dated packet chronology moved verbatim out of [[Current State]] on 2026-08-17.

[[Agent Operating Manual]] requires that [[Current State]] stay concise and
that chronology live in session notes; the state note had instead accumulated
every packet narrative in place, which made the mandated startup reading set
larger than any agent session can hold. Nothing was rewritten or dropped in
this move: the sections below are the original text, in the original order.

This is the earlier archive, not a current state note. The September 26
compaction and newer snapshots are indexed by [[Project history MOC]]. Use
[[Current State#Current task handoff]] for current work and
[[Environment Status#Current runtime handoff]] for runtime observations.

## 2026-08-15 M3 Level03 row-6 causal runtime

EXP-116 now has a PC-native causal control/candidate pair for the type-1 reset consumer. A one-byte Level03 DAT change at `0x4A4` changed row-6 X `15678 -> 15806`; the reset written by `bugs.exe` changed `501696 -> 505792`, exactly `+128 << 5`, while Z stayed `494016`. The successful arms used two disclosed debugger writes to reproduce prerequisite death state, so natural death remains unconfirmed. See [[EXP-20260815-116-receipt]].

At the EXP-116 point, row-to-reset semantics were confirmed for Level03 row 6
while the natural upstream trigger remained open. EXP-129/131 later close that
milestone boundary, and EXP-135 completes the final hard-truth ratchet.

## 2026-08-15 - Approval-compliant Level03 row-6 reset rerun

- [[EXP-20260815-117 - Approved Level03 row-6 reset rerun]] repeated the
  control/candidate discriminator after the user explicitly approved byte
  `0x18` at `0x0059D9A0` and word `0x0002` at `0x0059A5B0`.
- Control reset X/Z was `(501696, 494016)`; candidate reset X/Z was
  `(505792, 494016)`.
- The observed X delta `+4096` is exactly the DAT edit `+128 << 5`; unchanged
  row Z remained exact. Y was terrain-recomputed as static analysis predicts.
- This is confirmed PC evidence for the Level03 type-1 row-6 reset-coordinate
  consumer. Hard-truth re-audit is pending.
- Do not promote `type-1 row` to `checkpoint` yet. [[Known Unknowns#KU-057]]
  remains open for the natural producer and semantic classification.

## 2026-08-15 - M3 row-6 causal ratchet accepted

James returned `ACCEPT` for the bounded result in
[[EXP-20260815-117 - Approved Level03 row-6 reset rerun]]: PC Level03 type-1
row 6 supplies X/Z to the reset-coordinate consumer at `0x00432930`; changing
row X by `+128` changes reset X by exactly `+4096`, and unchanged row Z yields
unchanged reset Z.

The acceptance does not identify checkpoints or a natural trigger and does not
generalize beyond the tested row, level, and consumer. [[Known Unknowns#KU-057]]
remains the next M3 research boundary.

## 2026-08-15 KU-057 natural material-1 reconnaissance

[[EXP-20260815-118 - Natural Level03 material-1 reconnaissance]] completed a fresh no-write Level03 control run. Live descriptor indices 570-578 again carried tag 6/material 1; its scanner labeled `(471712,64224,537728)` as index 571, but EXP-131 later proves this tuple is descriptor 572's base. Ordinary input established a red-mushroom transition to the upper corridor and reached `(362499,28410,499117)`, but current collision material remained 0, `NextLife` remained 0, and no reset-request bit `0x10` was observed. This is a bounded negative, not evidence that material 1 is unreachable or non-gameplay.

This route left KU-057 open at the time. EXP-129 supersedes its proposed
descriptor-571/spider target by identifying the first grain-gate pit as a
natural material-1 producer. The earlier bounded negative remains valid.
`rr` is a separate complementary whole-process replay arm: `rr 5.9.0` and
`perf_event_paranoid=1` are ready, but `/dev/ntsync` remains present; the
existing KU-028 module-removal boundary still applies, and no privileged
action was taken.

## 2026-08-15 KU-057 natural pit reset

[[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]] captures
the natural upstream chain twice. The first grain-gate pit produced
descriptor/value `572/1`, flags `0x14`, `NextLife=2`, and a repeated
row-7-like endpoint; the user-confirmed spider control used `543/0` and did
not select an authored type-1 endpoint. The static join through
`0x004ACF90`, call site `0x004408EA`, `0x0041C8CC`, and `0x00432930`
independently supports the runtime order. Access to the gate used one exact,
explicitly authorized grain-byte write `1 -> 10` at `0x0059D9B1`; no other
target write occurred. KU-057 is narrowed to natural row-6-region selection or
an explicit milestone disposition, not another repetition of this single pit.

## 2026-08-15 Level03 teleport safety boundary

[[EXP-20260815-130 - Write-assisted Level03 teleport safety boundary]] records
the first durable Flik teleport procedure. Current and preceding XYZ may be
written together only to an already-confirmed walkable target. At the tested
Level03 row-6 floor point, the engine adopted the equal tuple into auxiliary
about 10 ms later. At unsupported targets, that same adoption—or directly
writing auxiliary—created a repeating generic fall/reset and consumed lives.

The user correctly distinguished the zero-grain closed-gate state from normal
pit access. Forced placement beyond it is diagnostic mutation, not a natural
death. EXP-130 observed no material-1 collision and leaves KU-057 unchanged.
See [[PC Flik teleport procedure]] before any future position write.

## 2026-08-15 Level03 collision geometry and M3.5 disposition

[[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]] traces
the exact PC `TERRAIN.ALL` source through `0x004A8410` and `0x004A8950` and
adds a bounds-checked, lossless read-only parser. It corrects EXP-118's live
scanner: `0x007F45A0` is descriptor base `+0x10`, so the printed X/Y/Z tuple
belonged to the next descriptor. `(471712,64224,537728)` is descriptor 572's
base, consistent with the natural first-grain-gate pit, not descriptor 571's.

Level03 result-1 descriptors 570–578 map to nine X/Z regions whose centers
pair with all 18 type-1 rows. Descriptor 572 alone covers rows 6/7. Its bounds
cross their nearest-row boundary, but both natural EXP-129 contacts are on the
row-7 side, and no distinct row-6-near result-1 descriptor exists. M3.5 adopts
the roadmap's explicit disposition option: retain the accepted causal row-6
consumer and separately natural upstream/row-7 chain, remove natural row-6
selection as a milestone blocker, and make no claim of impossibility,
controller reachability, checkpoint semantics, or cross-level behavior.
`KU-057` is resolved at that exact milestone boundary. M3 remained Active until
its final exit-gate reconciliation; EXP-132 supplied the worker closure,
EXP-133 rejected it on authorization provenance, and EXP-135 later accepts the
exact EXP-134 correction.

## 2026-08-15 CAP-002 PC input-movie worker

[[EXP-20260815-119 - PC input movie recorder and hardware replay]] adds
`scripts/input-movie.py` 1.0.0 and [[PC input movies]]. Production capture
selects keyboard events only on one verified internal Gamescope `bugs.exe`
window; replay is executable/movie/window/focus gated and always releases
held keys. The accepted hardware-selector movie is SHA-256
`07b5c351...24b28c8`; fresh replay runs `RUN-INP-REP-20260815-125230` and
`RUN-INP-REP-20260815-125312` agree with 4/4 events and pass the complete
hardware renderer gate. CAP-002 is partial until the user Level03 route is
recorded and repeated with the KU-057 trace; log/frame anchors have fixture,
not live gameplay, coverage, and no internal-frame claim is made.

## 2026-08-15 CAP-002 companion input controls

[[EXP-20260815-120 - PC input movie companion controls]] adds an asset-free Tk
companion without changing `scripts/play-pristine.sh` or its M4 pin. Run
`scripts/play-pristine-with-inputs.py --research --windowed --mute`; the
separate **ABLPC Input Recorder** window discovers only the isolated launch
session's exact 640×480 `bugs.exe` surface and supplies Choose/Start/Stop/Close
actions. Eleven focused fixtures and the complete 556-test gate pass. No live
GUI/game arm was opened inside EXP-120 itself; EXP-121 below supplies the first
live result, and KU-057 remains unchanged.

## 2026-08-15 first live companion replay

[[EXP-20260815-121 - First companion route replay divergence]] validates the
first user movie as 306 paired events over 49.447 seconds. Its renderer Down is
absent before the first Return, consistent with input during the unrecorded
three-second arm interval. A fresh replay with one disclosed pre-highlight
Down accepted 306/306 events, released all keys, and passed the complete
Direct3D gate, but the user saw Flik's Journey move back and forth without
entering Training; `bugs.log` likewise reached Level Select without a Training
load. Input dispatch is confirmed; gameplay repetition is rejected. No KU-057
state was reached. Exact cleanup removed all observed process and sink residue.

## 2026-08-15 anchored companion correction

[[EXP-20260815-122 - Anchored companion record and replay controls]] implements
the complete fixture-level correction required by EXP-121. Input worker and
companion are now version 1.1.0. The companion defaults recording to a newly
appended PC `--- Start LevelSelect ---` research-log marker, reuses the movie's
anchor for Replay, displays backend-confirmed **ARMED**, **RECORDING NOW**, and
**REPLAYING NOW** states, preserves the recorded post-marker neutral interval,
separates **Last saved** from **Next recording output**, and cleans the retained
isolated group after launcher-leader exit. Manual delay remains only as a
labeled weaker fallback.

Twenty-three focused fixtures and the complete 557-test repository gate pass.
The marker has not yet been live-accepted as a Training/Level03 route anchor,
no game runtime was launched for EXP-122, and KU-057 remains unchanged. The
next evidence step is one fresh companion
record/replay usability arm: start Record or Replay at the renderer selector,
select Hardware while **ARMED**, begin route input only at **RECORDING NOW**,
and verify the intended level load independently from the dispatch receipt.

## 2026-08-15 Level Select anchored live replay

[[EXP-20260815-123 - Level Select anchored route gameplay desynchronization]]
validates the first version-1.1.0 movie as 300 production events over 54.331
seconds. Record `RUN-INP-REC-20260815-160815` and fresh replay
`RUN-INP-REP-20260815-161221` share exact Level Select marker offsets. Replay
accepts 300/300 events, releases every key, and stays below 23.1 ms maximum
absolute dispatch drift. Its SHA-256 is `abc45db...17b91`.

The fresh log passes every Hardware/Direct3D gate and loads
`gfx\training.raw` plus `level07\level1.raw`, reaching `NextLife`. This fixes
EXP-121's failure to enter Training. The user nevertheless reports later
visible desynchronization. The movie's first gameplay-looking `z` begins only
1.337545224 seconds after the second Return release, so its uninterrupted
Level Select clock spans variable level loading and initialization. EXP-123
treated that as a strong mechanism without a measured load boundary; EXP-124
below supersedes that inference for the tested replay.

CAP-002 remains partial and KU-057 gains no gameplay-state result. Retain Level
Select only as a menu/level-entry anchor. The next discriminator is the first
new `NextLife` after level initialization, with renderer and level selection
outside the movie. EXP-124 below supersedes that immediate next-step ordering.
Both live sessions and all owned runtime/sink residue were closed.

## 2026-08-15 target-window replay echo diagnosis

[[EXP-20260815-124 - Replay echo identifies target input stream distortion]]
replays the same immutable 300-event movie while a second production observer
records the exact game window. The timestamped PC log places `NextLife` at
5.545035213 seconds and the source's first gameplay `z` at 6.498976937 seconds,
so direct loss of that key during loading is rejected for this arm.

The accepted replay receipt timestamps before its send subprocess, not at
target arrival. Target echo contains 304 normalized events, including two
inserted `Right` up/down pairs, and stretches several source transitions under
0.053 ms to about 15.1 ms. Measured holds shift by 20-35 ms. This proves a
current replay-backend fidelity defect capable of causing the visible route
desynchronization; the exact altered event responsible for the user's first
visible divergence remains unknown. DEC-117 therefore places persistent,
echo-validated delivery before the deferred post-load-anchor discriminator.
CAP-002 and KU-057 remain open. The fresh runtime and private sink were closed.

## 2026-08-15 persistent target echo and residual phase divergence

[[EXP-20260815-125 - Persistent echoed replay and residual gameplay divergence]]
replaces CAP-002's per-event `xdotool` send/focus subprocesses with a persistent
X11/XTEST sender and a second persistent observer on the exact game window.
One fresh arm correctly fails on an unrelated `Super_L` target event. Two more
fresh arms each dispatch and observe all 300 immutable source events, normalize
the expected 150 preparatory releases, restore nested-display auto-repeat,
release all keys, and remain below 0.52 ms maximum target-delivery drift.

The exact input receipts agree, but gameplay does not: the first arm returns
to Level Select, while the second remains inside Training after the movie and
an eight-second observation interval. The second retained fresh log reaches
initial `NextLife.` but no second Level Select. This separates the corrected
emitter defect from an unresolved phase/frame/runtime mechanism. Do not label
that mechanism as loading, frame sampling, or general nondeterminism without a
discriminating PC experiment.

Input worker and companion are now 1.3.0. The companion defaults gameplay
recording to fresh post-initialization `NextLife.` and labels Level Select as
menu only. Future log-anchored replay receipts capture a bounded raw log
segment and `ROUTINE` trace, and comparison requires state-checkpoint as well
as exact-input agreement. The old Level Select movie is not convertible
because its original `NextLife` phase was not measured. CAP-002 remains partial
until a new user movie passes two fresh exact-input and runtime-checkpoint arms;
KU-057 still requires its task-specific read-only state trace. `rr` remains
blocked by the unchanged `/dev/ntsync` authorization boundary; no privileged
action was taken. All live processes and private sinks were closed.

## 2026-08-15 M3 exit-gate reconciliation

[[EXP-20260815-132 - M3 exit-gate reconciliation]] supports all four written
M3 exit gates at the exact M3.1–M3.5 boundaries. Three distinct PC gameplay
families combine static/data and runtime evidence: Training grain/count/
completion, Training letter-mask/reward/HUD behavior, and Level03 nearest-row
reset selection. Exact local rebuilds reproduce all five accepted M3 output
hashes and byte-exact inverse receipts; their focused asset-free suites pass
25/25. The complete repository gate passes 576 tests with Vault 382/0/0, all
five M4 anchors valid, and zero tracked-file violations.

Load, controlled play, fail-closed staging/tool behavior, and exact-byte
restoration are all represented. The data-versus-executable boundary remains
explicit: DAT records own authored population/position/selector or the tested
Level03 row, while executable logic owns terrain initialization, nearest-row
selection, counters, masks, HUD/tally layout, and completion conditions.

EXP-132's worker result marked M3 Complete. Independent
[[EXP-20260815-133 - Independent M3 closure authorization hard-truth audit]]
retains the recipes and gates 2–4 but rejects the first gate:
the durable Training receipts disclose target-state changes and breakpoints
without proving their required prior explicit authorization. EXP-134 supplies
the exact approval-compliant two-arm correction, and EXP-135 independently
accepts it. M3 is Complete at the documented ledger boundary. M2 and M5 remain
Deferred, M4/M6 remain Complete, and no successor activates automatically.

## 2026-08-15 M3.7 authorization-compliant correction and acceptance

[[EXP-20260815-134 - Approval-compliant Training runtime receipts]] completes
the exact two-arm worker correction required by EXP-133. After the precise
mutation surface was presented and the researcher delegated the mechanical
approval decision and said to assume yes, two fresh retail-executable
Direct3D Training processes each received one 24-byte current-plus-preceding
XYZ write. No debugger, breakpoint, register, code, auxiliary, counter, mask,
reward, or live-record write was used.

The grain arm consumed only appended entry 62 and changed grain `0 -> 1`; its
two neighbors remained unchanged. The duplicate-letter arm consumed only
moved entry 63 and changed mask `0 -> 1`; original entry 50 remained unchanged.
Each read-only 10 ms observer retained 791 samples, zero read failures,
`NextLife=0`, and terminal target survival. Exact executable/DAT/log/raw-
receipt hashes and complete cleanup are retained in
`dynamic/wine/EXP-20260815-134-receipt.md`. Wine `Y:` is restored to the
ordinary full-disc work copy and no arm-owned runtime/sink process remains.

[[EXP-20260815-135 - Independent M3 ratchet acceptance audit]] rehashes and
independently parses both 791-sample traces, rebuilds the exercised helper
byte-for-byte from reviewed C source, reproduces all five recipes and their
inverse authority, and passes 25/25 focused, 9/9 terrain, and all 576 complete
tests. It records that the engine later adopts each target into auxiliary but
no direct auxiliary write occurred. All four exit gates pass, KU-059 resolves,
and M3 is Complete. M2/M5 remain Deferred and M4/M6 remain Complete.

## 2026-08-15 post-closure grain-gate threshold packet

[[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]]
corrects the visible-title mapping and adds one exact reversible PC executable
recipe. Tunnels is internal Level03 and reads nine resident requirement dwords
through `0x00432B30`; City Entrance is internal Level04 and derives three
indexed requirements through `0x00433790`. Retail values are respectively
`(20,10,10,10,20,20,30,10,30)` and `(10,20,30)`.

`scripts/make-grain-gates` accepts nine and/or three independent values in
`0..50`, patches both Tunnels image/template tables, replaces the City formula
with an exact three-dword lookup, preserves all unselected bytes, and proves an
exact inverse. Its `(1..9)`/`(1,2,3)` profile has SHA-256
`69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b`.
Twelve focused asset-free tests pass.

Fresh PC Direct3D arms load visible Tunnels as internal level 3 and City
Entrance as internal level 4 with the configured tables resident after level
initialization. EXP-137 supplies physical-transition evidence for Tunnels row
3 and City gate 0; EXP-138 independently accepts that exact boundary.
This is a bounded executable mod after M3 closure, not a reopened M3 packet or
an M5 selective replacement module.

## 2026-08-15 modified grain-gate threshold behavior

[[EXP-20260815-137 - Modified grain-gate threshold behavior]] tests the exact
EXP-136 profile at one Tunnels and one City mechanism. At known walkable
Tunnels `(501696,30092,494016)`, row 3 stays type `0x10C7` and visibly closed
at grain 3, then settles to `0x0690` and visibly open at configured minimum 4.
At fixed City first-gate trigger `(-87622,917,-182181)`, grain 0 retains state
`-1`, zero animation, and a visibly closed gate; grain 1, without movement,
drives state 28 to 0 and animation `-128/+128` to `-1024/+1024`, visibly open.
Both keep `NextLife=0`.

The researcher's ordinarily reached City approach point
`(-92603,1098,-181281)` is saved separately and is just outside the trigger.
The fixed-point arms are write-assisted current-plus-preceding setup, not
controller-reachability evidence. A candidate City rerun that entered 320x200
software rendering was rejected before any target write. [[START HERE]] now
requires video-memory status, 640x480 creation, and explicit Direct3D start in
addition to the early selection summary. [[EXP-20260815-138 - Independent modified grain-gate threshold audit]]
rehashes all 69 evidence files, rebuilds the helper/profile, verifies the
static and runtime joins, and returns **ACCEPT** only for the two tested
mechanisms. Other gates remain open under KU-060.

## 2026-08-15 static grain-gate trigger geometry

[[EXP-20260815-139 - Static grain-gate trigger geometry]] completes the
offline static half of the gate-by-gate mapping pass with no runtime process
or target write. The three City Entrance call sites in `0x00433900` pass only
immediates: gate 0 `(-71129,-184314)` r=80, gate 1 `(354031,35256)` r=90,
gate 2 `(582271,310212)` r=100, with per-gate state at `0x0059F020 + i*4`
and animation accumulators at `0x0059F030`. Proximity helper `0x00416580`
computes `((dx>>8)^2 + (dz>>8)^2) < r^2` on X/Z, so effective radii are
about `r << 8` units. Tunnels applies the same form inline with one shared
open threshold `0x2710` (~25600 units) and message threshold `0x640`
(~10240); row types run `0x10C7 -> 0x1068 -> -140` per update to `0x690`,
and the rows-0/4 link is the exact cross-writes at
`0x00432F85`/`0x00432F9D`. Every claim carries decoder plus raw-byte
evidence at pinned file offsets, and the extracted predicate reproduces
EXP-137's accepted inside/outside boundary at all three receipt points.

`scripts/coordinate-overlay.py` 1.3.0 adds an opt-in `--gates` nearest-
mechanism readout (live Tunnels rows, live City states, requirement, world
distance versus effective radius, engine-exact IN/out) and widens its target
boundary to exactly {retail, accepted EXP-136 profile}; reads remain
`process_vm_readv` only. The overlay test suite grows to 14, pinning the
geometry constants, the sar-exact predicate against the accepted boundary
points, read plans, requirement sources, and the two-hash boundary. The
researcher walking pass to correlate visible gates with mechanisms, save
safe approach coordinates, and physically test City gates 1/2 plus the
remaining Tunnels rows stays open under KU-060. M3 remains Complete; no
milestone is reopened.

[[EXP-20260815-140 - Independent static gate geometry and overlay audit]]
independently accepts this packet. James rehashes the executable, re-reads
every cited byte at its file offset, re-derives the disassembly, proves
the "exactly three" City call-site claim with a binary-wide census,
falsifies the X/Z-swap alternative against the accepted receipts,
recomputes all cross-check arithmetic including sar/Python-shift
equivalence, byte-diffs the accepted profile against every geometry range
(zero overlap), reviews the overlay diff for read-only and fail-closed
two-hash behavior, and passes all hygiene gates (Vault 405/0/0, 596 tests,
tracked audit 0, no runtime artifacts). Two minor wording observations are
corrected in place; the accepted boundary is unchanged: gates 1/2 remain
single-form static facts until physically walked.

## 2026-08-16 engine-faithful terrain height and gate standoffs

[[EXP-20260816-141 - Engine-faithful terrain height and gate standoffs]]
reimplements the exact PC terrain height pipeline offline so the mapping
pass can teleport instead of walk. The reset consumer's Y source is
pinned end to end: `0x00432930` queries thunk `0x00401659 -> 0x004AC460`
(bucket/descriptor/group/cell collection), `0x00401717 -> 0x004ACA60`
resolves the exact plane formula
`base_y + 4*((h0<<3) - idiv(((z-z0)*A + (x-x0)*B)<<3, C))` with
floor/ceiling selection and a `+0xC80` offset, `0x004A9290` supplies the
half-plane tests, and actor Y is the result minus `0x100`. Descriptor
construction including the majority clone branch and the cell-derived
bounds recompute is modeled bit-exactly in
`reimplementation/ablpc/terrain_height.py` on top of the EXP-131 parser.

Validation: the EXP-130 walkable point reproduces exactly
(rest Y 30092, delta 0 — it originated from this engine path), and three
settled standing receipts (EXP-129 endpoint, both EXP-137 City points)
land 121-126 units deeper, pinning PC world Y as downward; the Level03
result-1 reset surfaces rest near 64032 below the ~30000-32000 ground.
Two contradictions/limits are recorded rather than normalized: EXP-131's
descriptor Z-bounds table derives from group headers while the loader
uses cell fields (new `KU-061`, live-readable discriminator), and the
appended `plantter.all` descriptor family is out of scope.

`scripts/grain-gate-standoffs.py` computes deterministic candidate
teleport standoffs for all twelve gates (engine-exact plane enumeration
plus a documented center-referenced selection heuristic); T3/C0 keep
their independently accepted proven points. Fourteen new focused tests
pass and the candidates live in [[PC grain gate threshold mod]].
Candidate walkability, the visible gate correlation, and the untested
physical thresholds remain open under KU-060; the runtime
teleport-and-view session is the next arm. M3 remains Complete.

[[EXP-20260816-142 - Independent terrain height and standoff audit]]
independently accepts the packet. James re-disassembles the complete
pipeline, reviews the reimplementation line by line, attacks and repairs
the bucket-order equivalence argument (bucket unions are group-header
derived while phase-2 boxes are cell-derived; an exhaustive scan proves
zero cell-below-group protrusions in both modeled files), reruns the
receipt and standoff computations with a scratchpad tamper test, and
passes all hygiene gates (610 tests, Vault 412/0/0, tracked audit 0).
Three latent gaps he surfaced are reconciled without changing any
result: the loader's `+0x10 >= 0x100` no-descriptor branch is now
documented (both files carry such records only after every tag-6/7/8
record), the `0x004A865B` unregistered-clone target is an infinite-loop
trap rather than a skip (dossier corrected; the reimplementation fails
loudly and no retail clone triggers it), and the equivalence/settle
wording is tightened. The accepted boundary is unchanged: heights are
terrain-surface values for the two exact files, standoffs remain static
candidates, and KU-060/KU-061 stay open.

## 2026-08-16 runtime grain-gate visual mapping

[[EXP-20260816-144 - Runtime grain-gate visual mapping]] completes the
runtime half of the gate mapping. Driving retail PC `bugs.exe` under
Gamescope autonomously (XTEST input, hardware selection, level-select
navigation — recipe in [[PC autonomous game control]]), a write-assisted
teleport pass over the EXP-141 standoffs placed Flik at all twelve gates:
nine Tunnels wooden-pole gates (internal level 3, rows 0–8) and three City
Entrance leaf/pillar gates (internal level 4, indices 0–2). Every teleport
read `NextLife=0` at the post-teleport snapshot (so every EXP-141 standoff
is walkable), the engine-exact nearest-gate index matched the intended
mechanism at every stop, and City states read `(-1,-1,-1)` at grain 0.
Grain-requirement numerals are visible on Tunnels rows 3/6/8 ("10"/"30").

Only guarded 24-byte current+preceding teleports were written; no grain,
executable, asset, or `originals/` mutation occurred. A key methodology
result: menu input must be delivered via XTEST because the chooser reads
`GetAsyncKeyState`, which ignores synthetic `XSendEvent`; the chooser has a
60 s software-default timeout. Evidence screenshots are retained under the
ignored `work/copies/EXP-20260816-144-gate-mapping/evidence/`. This closes
the KU-060 visible-correlation and standoff-walkability items; only the
physical modified-threshold receipts for the untested gates remain. M3
stays Complete; this is post-closure mapping, not a reopened milestone.

[[EXP-20260816-145 - Independent runtime gate mapping audit]] independently
verifies the standoff agreement, all nine Tunnels distances, every
nearest-gate identity and inside/outside verdict, the retained screenshots,
the control-recipe disassembly (`GetAsyncKeyState`, VK polls, 60 s timeout),
the write boundary, and hygiene. It first returned REJECT on one isolated
defect — two City `dist²` annotations used truncation instead of the engine
`sar` helper — which was corrected in place to engine `sar`-8 from the
settled current position (gate 0 `3482`, gate 1 `9216`, gate 2 `11885`); no
nearest-gate identity or verdict changed. James then upgraded to **ACCEPT**.

**Lifecycle note:** this ran alongside a separate researcher/Codex game
instance. Concurrent nested Gamescope sessions conflict (the second crashes
with an X `BadWindow`/broken-pipe), so the researcher's instance was closed
with explicit authorization before the solo City run. Only owned process
groups and the owned private sink were terminated; the final audit was
clean and Wine `Y:` remained `work/copies/BUGS_PC-full-disc`.

## 2026-08-16 KU-060 modified grain-gate thresholds completed

[[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]]
closes the KU-060 physical modified-threshold receipts. On the modified
`(1..9)/(1,2,3)` profile (`Y:` temporarily repointed to the modified
full-disc copy, then restored to retail), ten of twelve gates show the exact
closed-at-(min-1)/open-at-(min) transition (Tunnels rows 0,2,3,5,6,7,8 and
City gates 0,1,2); Tunnels row 1 opens above its requirement (exact boundary
not isolated); Tunnels row 4 is opened by the row-0 coupling and is not
independently separable, as EXP-136 predicted. City animation slots activated
(gate 1 -> 4/5, gate 2 -> 0/1) match EXP-139's static call-site prediction,
cross-validating it against runtime behavior.

A key runtime finding, now in [[PC autonomous game control]]: this
Gamescope/Wine game advances its logic/physics loop **only while its window
is focused**. Memory reads/writes work regardless, but gate opening, gravity,
and menu input only advance under focus; carousel presses drop when focus
lapses. All threshold observations held focus. Only guarded teleports and
disclosed one-byte grain writes were used; owned processes/sink were closed
and the final audit was clean. M3 remains Complete; this is post-closure
follow-up.

[[EXP-20260816-149 - Independent modified-threshold completion audit]]
independently **accepts** the packet with no defects: the modified build's
Tunnels requirements read `1..9` and the City lookup `1,2,3`; the open
semantics match the disassembly (Tunnels `0x1068 -> 0x0690`, City state
`-1 -> 0` with the animation slots, call-site slots gate0->2/3, 1->4/5,
2->0/1); the rows-0/4 cross-writes are unconditional so row 4 is correctly
not claimed independent; the row-1 residual is honestly disclosed; the
write boundary is one 24-byte teleport plus a guarded one-byte grain write;
the screenshots are 640x480 hardware frames matching their grain HUD; and
hygiene is clean. KU-060 is closed.

## 2026-08-16 auto-hardware Direct3D startup built and runtime-accepted

[[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]] builds
and runtime-validates the EXP-143 auto-hardware transform. New
`reimplementation/ablpc/auto_hardware_mod.py` + `scripts/make-auto-hardware`
apply the exact paired code (`0x000A6C6B`) plus relocation (`0x000FA912`)
edits to a derived retail copy, refusing any non-retail source, applying both
atomically, preserving every other byte, and proving exact inverse; output
SHA-256 `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`,
nine focused tests pass.

Two fresh Gamescope/Wine restarts of the patched full-disc copy (retail tree
hardlinked, only the exe replaced; `Y:` repointed then restored) boot
**straight into hardware Direct3D with no chooser input and no visible
chooser** — all six START-HERE markers plus `Device has hardware
acceleration`, host NVIDIA RTX 5090, playable Training-level rendering, and
no `SYSTEM MEMORY ONLY`/`INITSOFTRENDER`/320x200.
[[EXP-20260816-151 - Independent auto-hardware runtime audit]] independently
**accepts** this at the derived build hash, reproducing the builder,
disassembly (`mov [esp+0x10],ebp` / `jmp 0x004A7A56`), the HIGHLOW->ABSOLUTE
relocation, and both retained logs; it narrows the physical-GPU claim to
renderer-level hardware Direct3D (the Gamescope/Vulkan device log was not
retained). [[PC automatic Direct3D startup candidate]] is promoted to
`runtime-accepted` and the [[START HERE]] renderer note is updated
accordingly. The retail hash still has no renderer argument, so the manual
procedure stays authoritative for retail; the auto-hardware build is a
distinct hash used only via `scripts/make-auto-hardware`. Retail exe and
`originals/` untouched; final process/sink audit clean; `Y:` restored to
`work/copies/BUGS_PC-full-disc`.

`scripts/play-pristine.sh` now has an opt-in `--auto-hardware` flag: it
builds/reuses the cached patched copy (`work/copies/auto-hardware/bugs.exe`)
and runs it from the retail game directory (retail assets and `Y:`
unchanged), so a launch boots straight into hardware Direct3D with no manual
chooser. Live-validated end to end through the launcher (all six markers, no
chooser) and covered by four dry-run tests; a plain launch still uses the
retail exe and the manual procedure. The default launcher behavior is
unchanged. Because `play-pristine.sh` is a pinned M4 machine authority whose
structure check enforces the renderer echo and `COMMAND` surface/scaler, the
pinned echo was kept verbatim (the auto-hardware note is a separate line) and
only its byte pin in `reimplementation/ablpc/compatibility.py` was re-pinned
(`68c91717… -> 6ca3c657…`); the M4 v0.2 canonical statement and every semantic
claim are unchanged and `check-m4-compatibility.py` passes.
[[EXP-20260816-152 - Independent launcher auto-hardware flag audit]]
independently **accepts** the change with no defects (re-pin matches the file,
canonical statement and structure check unchanged and genuinely satisfied, no
falsified history, hygiene clean).

## 2026-08-16 M5 activated with the type-1 reset resolver

[[EXP-20260816-153 - M5 entry gate and type-1 reset placement resolver]]
audits candidate modules against the six M5 entry-gate criteria and admits
one: the type-1 reset-placement selector. The contract was re-derived from
the exact retail binary (radare2, verified hash) rather than from prior prose,
which corrected and extended it — the row count is read as an unsigned word,
distances use `sar` in row space (not truncating division in world space),
ties go to the lowest index, and the `0x00437A20` variant is byte-identical
so the mode dispatch cannot change the result.

`reimplementation/ablpc/type1_reset.py` models it bit-exactly (32-bit wrapping
`imul`/`add`, arithmetic shifts, `<< 5` placement, `height - 0x100`, and the
`0x80000000 -> 0x7FFFFF00` failed-query relation) on top of the existing
parser and the accepted EXP-141/142 height model. `scripts/type1-reset.py`
reports one query or every row as deterministic JSON with source hashes.
Twenty-four focused tests pass; the full suite is 647.

Differential agreement with retained receipts: both EXP-129 pit falls select
row 7 and place `(497248, 31176, 547264)` against an observed settled sample
`(497247, 31299, 547255)` inside the accepted 121-126 band; the EXP-130
walkable point is an exact fixed point at `(501696, 30092, 494016)`; the
EXP-116/117 candidate row reproduces `+4096`. Unplanned: the model's terrain
descriptor 543 at the row-7 placement matches the collision descriptor that
trace sampled after the reset.

Corpus census (metadata only): 14 of 21 files carry a type-1 record, seven
carry none, four contain rows this selector can never reach, and Level04's
duplicates mirror around a pivot into an out-and-back sequence. Level03's 18
rows pair one-to-one with the nine grain gates from EXP-136/139 immediates
(near row 13,729-17,993 units, far row 37,231-39,316, next gate 303,653+).
The pairing numbers are confirmed; near/far reset intent is inference and
type 1 keeps its address-based description.

Offline only: no game launch, debugger, breakpoint, target write, asset edit,
or `originals/` access. M2 stays deferred; M3/M4/M6 and every M4 authority pin
are unchanged.

**M5.2 rejected this packet; M5.3 corrected it.** See the dated M5.2/M5.3
section below.

## 2026-08-16 M5.2 rejects M5.1; M5.3 corrects it

[[EXP-20260816-154 - Independent M5.1 hard-truth audit]] returns **REJECT** at
clean HEAD `2ce8686`. The module's behavior survives every attack: James wrote
an independent instruction-level simulator from his own disassembly and
matched it against `type1_reset.py` across 264,232 trials with zero
mismatches; the mod-4 seed argument held analytically and over 200,000
samples; all four runtime receipts and the corpus census reproduced from
primary sources; the refusals cannot be bypassed; and every hygiene gate
passed with no M4 authority drift.

Two evidence defects blocked acceptance. First, the far-side maximum `39,619`
and the next-nearest-gate floor `284,005`, both under a **Confirmed** label,
do not reproduce — the true values are `39,316` (row 11 to gate 5) and
`303,653` (row 9 to gate 2). The worker attests both wrong numbers came from
the descriptor-anchor pass it had explicitly decided not to rely on; the audit
could not reproduce that provenance exactly (result-1 base anchors give
`285,443`, close to `284,005` but not equal), so it stands as worker-attested
rather than confirmed. The worker's own test bound of `39,400` should have
caught the contradiction regardless. Second, the
"slot retains whatever the previous level left there" wording, repeated in
four artifacts without a citation, is contradicted by live code: level-load
entry `0x004671D0` zeroes all 64 pointer-table dwords at
`0x00467207-0x00467215`, with an unreferenced copy at `0x00464F31`.

M5.3 corrects both in place. The numbers are fixed at all four sites and now
pinned by exact-extreme assertions in `tests/test_type1_reset.py` instead of
loose bounds; fixing that test surfaced one further precision point — near
versus far within a pair is not fixed by index parity, since at gate 1 the odd
row is nearer. All four retention statements are rebounded and `KU-064`
records the clear routine with a read-only discriminator. Three minor findings
are folded in: the imprecise "distinct surfaces" wording (all 18 rows resolve
at distinct positions, but descriptors 558/517/484 each win twice), the
missing consumer `0x00436D25`, and the implementation note's premature
`status`. Selector arithmetic, refusals, and every receipt are untouched;
focused 24, full suite 647.

## 2026-08-16 M5.3 accepted

[[EXP-20260816-155 - Independent M5.3 delta re-audit]] returns **ACCEPT** at
clean HEAD `66d1ad4`. The corrected numbers appear at every live site, with
`39,619`/`284,005` surviving only as deliberate quotations of the rejected
values; the new test pins match figures the auditor had derived from the
`0x004DA9C8` gate records before the commit existed, so they pin an
independent derivation rather than the code's output; all six retention
statements avoid overclaiming in either direction; and the module diff is
exactly the three-line error-message change, with both receipts re-running
identically.

The audit also strengthened the `KU-064` evidence rather than weakening it:
the three prologue branches of `0x004671D0` all converge on the clear at
`0x00467207`, and the same function calls the record walk `0x0044BB70` through
thunk `0x00401D7A` at `0x00467971`, so statically any load that walks records
was preceded by the clear in the same invocation. The unknown stays open on
its runtime discriminator.

One attribution correction was applied: the claim that both wrong numbers came
from the demoted descriptor-anchor pass is **worker-attested, not
independently established** — reproduction from result-1 base anchors gives
`285,443`, close to `284,005` but not equal. The roadmap, this note, and the
session note that had stated it flatly in the auditor's voice are corrected.

Three of M5's four exit gates are now supported at the module's boundary. The
fourth — that replacement is demonstrably safer and more useful than the
original path — is untested by construction, and M5.4 is the packet for it.

## 2026-08-16 M5.4 predictive receipt confirms the resolver at runtime

[[EXP-20260816-156 - M5.4 predictive reset placement receipt]] closes M5's
fourth exit gate for the first module. The prediction was committed at
`a58f962` **before any launch**, so it could not be fitted to the result.

Editing row 6's Z by `+256` — one byte at file offset `0x4AD`, candidate DAT
`91a27776...cb8965`, `TERRAIN.ALL` untouched — moved the engine's reset
placement to `(501696, 31768, 502208)`. All three components match the offline
prediction exactly, 6.2 ms after the trigger. The Y is the load-bearing part:
it is a terrain recompute at the moved point, `+1676` from the control, and no
shift of the edited field could produce it. The selected row stayed 6 and
`NextLife` returned to 0 and stayed there, confirming the predicted result-0
destination with no reset loop.

Two limits are recorded rather than smoothed. The control arm's query point
equals its predicted output, so it cannot distinguish a write from a no-op and
serves only as a trigger baseline. And Flik settled `+129` below the written
Y — three units outside the previously recorded 121-126 band. The band is
restated as the observed extremes over five cited receipts, **121-129**, and
`scripts/type1-reset.py` plus the implementation note now publish that same
range so the tool cannot emit a band excluding an accepted receipt. No
prediction depends on it.

Both arms used the guarded auto-hardware build with all six markers, exactly
three target writes each (the accepted 24-byte teleport plus the EXP-117
trigger setup), no debugger or breakpoint, both owned process groups and
private sinks closed with empty final audits, Wine `Y:` restored, and retail
DAT/executable/`originals/` hashes unchanged.

Methodology, now in [[PC autonomous game control]]: menu key **taps** are
unreliable because the chooser polls `GetAsyncKeyState` and a ~12 ms synthetic
press falls between polls; two of three carousel presses were dropped that
way. A ~180 ms hold landed every press.

M5 stays Active: all four gates hold for this one module on Level03, and any
second module must pass its own six-criterion entry gate.

## 2026-08-16 M5.4 rejected on evidence retention; M5.5 corrects it

[[EXP-20260816-157 - Independent M5.4 hard-truth audit]] returns **REJECT**
narrowly, with the runtime result standing. The pre-registration is genuine —
`git diff a58f962 b861376` touches only frontmatter and appends below the
pre-registration rule — the predicted triple re-derives independently, the
`31768` Y provably requires the composed terrain model (every shift and linear
function of the edited field misses), the aux transition is unambiguous, and
the write/lifecycle boundary and gate-4 scoping survive attack.

Two quantitative claims did not reproduce from retained evidence. The
"stayed 0 for the remaining 7 seconds" no-loop window is contradicted by the
trace, whose final row is at `3076.1 ms`, giving about **2.47 s**. And the
band widened to 121-129 in the Vault was left at 121-126 in
`scripts/type1-reset.py` and the implementation note, so the shipped tool
emitted `[31889, 31894]` for the accepted candidate row — excluding the
observed `31897`.

M5.5 corrects both: the no-loop claim is now the retained window with the
reason the trace ends stated; the band is restated as observed extremes over
five cited receipts everywhere it appears, including the tool's constants; a
new focused test rebuilds the exact candidate DAT and asserts `31897` falls
inside the emitted band; and the volatile control log is retained at
`85b39abf...` with its six markers re-verified. Suites are 25 focused and 648
full. Historical experiment notes keep the band accepted at their time.

## 2026-08-16 M5.5 rejected at one residual site; M5.5.1 closes it

The M5.5 delta re-audit confirmed the no-loop window, the retained control
log, five of six band sites, the new test as a genuine pin (it fails under the
old constant), and clean scope — nothing above the pre-registration rule
changed. It rejected on one residual: `scripts/grain-gate-standoffs.py` still
published `121-126` in its docstring and inside its deterministic JSON
`rest_y_note`, so an operator reading that report would treat an accepted
`+129` settle as an anomaly. The sibling implementation note had been
corrected in the same commit, leaving tool and documentation disagreeing.

M5.5.1 fixes both strings to the wording the type-1 tool already uses and adds
the four establishing receipts to the report's `evidence` list. The acceptance
search now leaves 19 occurrences, all historical, receipt-specific, or explicit
quotations of the superseded value.

Worth recording as a process lesson: M5.5 asserted the band was consistent
"everywhere it appears" without running a repository-wide search. The claim was
made in good faith and was wrong, which is exactly the failure mode the
audit ratchet exists to catch — an unverified assertion, not a wrong analysis.

## 2026-08-16 M5 first module closed at its Level03 boundary

[[EXP-20260816-158 - Independent M5.5 and M5.5.1 delta audits]] returns
**ACCEPT** at `f0ea760`, closing the M5.1 → M5.2 → M5.3 → M5.4 → M5.5 →
M5.5.1 chain. All four M5 exit gates now hold for the type-1 reset resolver at
its documented Level03 boundary: the contract is address-cited and derived
from disassembly rather than decompiler text, the regression tests compare
observed original behaviour against independent output, and `EXP-20260816-156`
supplied the missing fourth gate with a prediction committed before launch and
confirmed exactly.

One non-gating erratum was folded in rather than banked: the acceptance-search
tally recorded as 18 is **19** at the committed HEAD, because the sentences
recording the fix themselves contain the superseded string. The property that
mattered — every occurrence historical, receipt-specific, or an explicit
quotation — was independently verified for all 19.

The chain cost four rejections across six packets, and every one was a claim
that outran its evidence rather than a wrong analysis: two numbers copied from
a computation the note had itself demoted, an uncited retention story
contradicted by live code, an evidence window taken from a sampler's
configuration instead of its output, and a band corrected in prose but not in
the tool that publishes it. The module's behaviour was never once wrong.

M5 stays Active with one admitted module. The next packet is **M5.6**: audit
whether any second module passes the six-criterion entry gate on existing PC
evidence — candidates include the grain-gate opening resolver and the
index-ordered type-1 consumers — or record a deliberate rest state. "No
candidate passes" is a valid outcome.

## 2026-08-16 first coverage-driven packet: PC audio census

[[EXP-20260816-159 - PC audio subsystem static census]] is the first packet
chosen from [[Subsystem Coverage Map]] instead of from milestone momentum, and
the first to open a row that had no PC evidence at all. Offline throughout: no
runtime, debugger, or target write.

Confirmed anchors: DirectSound bring-up at `0x004A3480` (enumeration callback
`0x0049DD00`, object stored at `0x007EDAE8`, GUID pointer `0x007EDA60`,
window handle `0x0059F73C`, ready flag `0x007ECA40` written only on success);
a track-name table at `0x00596528` with 8-byte entries, built by `0x0042BB90`
with 33 `audio\*.wav` names (indices 0-14 `Level1a`-`Level5c`, 17-21 `levcom`/
`title`/`bugs2m*`, 24-36 `less1`-`less12`); track paths assembled at
`0x00596960` from `\pc\bugs\cd\` plus the name, logged by `PLAYTRACK`; the
`DSStream` token parser at `0x0042C130`; and all 37 WINMM `mmio*` call sites
inside `0x004AD000`-`0x004ADB20`, a region that can author RIFF chunks as well
as read them.

Structural finding: `0x0042BA60` brings up DirectSound (`0x0042BAD0`) and
DirectInput (`0x0042BAED` -> `0x0042F350`) as siblings. That is why the map
now carries **Input** as its own row — folding it into movement was a
condensation error in the map's first draft, since `DINPUT.dll` is a distinct
import surface on PC.

Method facts worth carrying to the next subsystem: this executable reaches
imports through `jmp dword [IAT]` thunks, its own functions through the
`0x00401xxx` `jmp` table, and *some* functions only through `.data`
function-pointer records — the audio census's own central initializer
`0x0042BA60` has zero direct call sites and is dispatched from the
`"DIRECTX"` record at `0x004D81E8`. A naive cross-reference search finds
**nothing** in any of the three cases. Rows anchored in the import table
(audio, input, FMV, the DirectDraw side of rendering) remain far cheaper to
open than rows with no import surface.

The audio row moves Untouched -> Bounded. No milestone status changed; M5.6
remains available whenever the second-module question is worth answering. The
cheapest next step here is still static: identify `0x0042B020`, the module's
busiest entry point at 34 call sites.

## 2026-08-16 audio census audited and corrected

[[EXP-20260816-160 - Independent audio census audit]] returns **REJECT** at
`00c5ae5` and the corrections are applied in the same commit. The anchors and
most counts survived independent re-derivation; six Confirmed-level claims did
not:

- `38` `mmio` call sites is **37** — the census's own per-import table summed
  to 37 and only the headline was wrong;
- `seventeen` thunk-reachable module functions is **12** — ordinary `jmp`
  instructions inside functions were counted as thunk-table entries;
- "every caller outside the module" is false: `0x0042B020` has in-module
  callers `0x0042B747` and `0x0042B781`, and the census's own tooling had
  printed "32 from outside" of 34;
- `0x0042C29F` is a `je` target inside a byte-scan loop, not a function start;
  the containing function is `0x0042C130`, the DSStream parser already known;
- "a DSStream window class is registered" describes a site that actually feeds
  **`UnregisterClassA`** — a cleanup, not a registration;
- "music track table" sat under Confirmed while the note's own Inferred
  section said no instruction distinguishes music from effects. It is now
  "track-name table" everywhere.

The material finding is a completeness miss: `0x0042BA60`, the packet's own
central initializer, has **zero** direct call sites and is dispatched from a
`.data` record at `0x004D81E8` (count 3, three thunk pointers, then
`"DIRECTX"`). The census disclosed that it had not scanned indirect forms but
did not follow the consequence — that a claim of caller completeness could not
stand. The coverage map's method note now says to check call instructions,
both thunk directions, **and** `.data` function-pointer records, while warning
that register-indirect dispatch can still hide callers.

The audio row stays **Bounded**: the auditor was offered a downgrade to
Touched and declined it, requiring only that the row's anchors drop the bad
address. One further offered item — an index bound read from a `cmp` — was
deliberately **not** recorded, because the disassembly at that address did not
cleanly reproduce during the correction.

## 2026-08-16 historical camera worker result

[[EXP-20260816-161 - PC camera static reconnaissance]] originally reported no
camera anchor and kept the row Untouched. EXP-162 rejected its transform
placement, viewport locators, universal D3D statement, caller attribution, and
coverage disposition. EXP-164 corrects the historical note and every live
propagation site. The surviving facts are the no-string/import difficulty,
D3DApp provenance, three known TL-vertex submissions, seven terrain calls,
cross-port separation, and the manual-control caution. This section is
history, not authority for the superseded worker claims.

## 2026-08-16 camera reconnaissance rejected; static correction required

The section above is now historical worker state.
[[EXP-20260816-162 - Independent camera reconnaissance audit]] returns
**REJECT** at subject commit `02946af`.

What survives: D3DApp provenance, the known `D3DVT_TLVERTEX` submissions and
their game-code transform boundary, the exact seven calls to terrain thunk
`0x00401659`, the containing-function assignments, the PS1/PC evidence
separation, and the decision to keep the manual-controls discrepancy open.

What fails: `0x00423E93` and `0x00423F55` are immediate-operand bytes rather
than instruction addresses; the viewport structure setup is
`0x00423EDE`-`0x00423F43`. `0x00405FE0` does not merely receive transformed
vertices — beginning at `0x0040605F` it multiplies them by
`0x0063E888`-`0x0063E8B0`, reduces by 4096, and adds translation
`0x0063E8B8`/`BC`/`C0`. `0x0045A7F0` does not call that builder and already
had a static export saying it transforms and fills batches inline. The
universal "no Direct3D view matrix exists" wording also exceeds what three
known TL-vertex submissions prove.

Most importantly, following the matrix finds a PC-native structural chain.
`0x0041ADF0` updates a Flik-relative position/orientation source;
`0x0041B7D0` selects between two position/angle blocks into common block
`0x00599C90`; `0x00455710` turns that common block into origin
`0x005BDB8C` and matrix `0x005B58E0`; render code copies the matrix through
`0x004636C0` to the transform globals consumed by `0x00405FE0`. Gameplay-
follow, setpiece, and camera field meanings remain **Inferred**, but the
two-source view-transform data flow is Confirmed PC evidence. It is enough to
support a Bounded row after the one correction packet propagates it.

The terrain census contains four unmapped functions after subtracting two
known reset consumers and known City dispatcher `0x00433900`, not five.
Exactly two of those four enclosing functions read Flik's position, but their
terrain-query arguments are not thereby proved to be Flik.

EXP-164's static trace tightens the critical join by showing
`0x00455799` writes the generated matrix directly to `0x005B58E0`, which
renderer call `0x0044D4C1` passes to `0x004636C0`. It also corrects XPORT-004,
EXP-161, the worker session, and every live index. EXP-165 independently
returns **ACCEPT** at clean subject `0336d14`, reproducing the direct join,
source/update order, local transform, caller and terrain counts, locator
corrections, XPORT boundary, and live-claim hygiene. Camera is therefore
Bounded, not Mapped. Do **not** treat the verdict as source-role, manual-
control, runtime-frequency, visual-causality, or indirect-path evidence.

## 2026-08-16 KU-065 reproduction follow-up remains negative

[[EXP-20260816-163 - KU-065 canonical-suite reproduction follow-up]] did not
reproduce the original `1 failed, 647 passed` signature. Direct unfiltered
logs retain 13/13 canonical full suites at 648 passed, 100/100 complete
manifest-module runs at 198 passed, and 200/200 focused system-state runs at
17 passed. Raw-log hashes are retained locally in ignored work-copy evidence.

One constrained-sandbox run produced nine failures, including a
`15 -> 14` process-descriptor delta in
`test_cli_receipt_cleanup_error_is_silent_and_closes_every_descriptor`.
Because that run also had seven ptrace-blocked GDB failures and an input timing
failure, it is a candidate lead only and does not identify the lost one-test
failure. `KU-065` stays open. Passing suite runs must carry their exact
denominator and this qualification rather than being cited as an unqualified
gate.

The final process audit additionally found 32 pre-existing
`work/wine/baseline` `winedevice.exe` helpers (PIDs `68248`-`344284`, parent
user systemd PID `1927`) but no active game, Gamescope, `wineserver`, pytest,
or debugger target. They predate EXP-163 and lack an exact ownership ledger,
so they were recorded rather than broadly terminated. This means the passing
runs cover that residual helper background; it does not identify KU-065 or
authorize a future runtime launch without a new ownership audit.

## 2026-08-16 M5 second-module proposal rejected, corrected, and accepted

[[EXP-20260816-166 - M5 second-module entry-gate audit]] proposed one second
module offline against exact retail SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
[[EXP-20260816-167 - Independent M5.6 hard-truth audit]] rejects exact subject
`3504f6a`; admission does not yet stand. The corrected candidate remains
bounded to the twelve confirmed Tunnels/City mechanisms at functions
`0x00432B30`, `0x00433790`, and `0x00416580`. Its proposed direct-write output
now includes Tunnels row-0/4 coupling and City index-0 byte
`[0x00599C69] = 1` at `0x00433807`, whose semantics remain Unknown, plus
downstream decay or City state/slot-delta rule metadata. Global family
exclusivity, callee effects, messages, audio, rendering, controller
reachability, persistence, and unrelated update logic are not claimed.

The index-ordered type-1 path at `0x004369B0`/`0x00436D25` remains a real
static PC candidate. Its decisive first failure is the original-runtime-
observation criterion; the other criteria are unassessed. At `0x00436D50`,
`0x00436D5F`, and `0x00436D6F`, it loads X/Y/Z from one indexed row, not
indexed and next rows. The smallest future discriminator is one separately
authorized, read-only internal-level-9 trace across a natural index advance;
that receipt would trigger a new six-criterion audit, not automatic admission.
KU-063 is also corrected against the already-
accepted pointer-table clear at `0x00467207`-`0x00467215`: a load through
`0x004671D0` does not preserve the preceding type-1 pointer.

M5.6.1 is independently accepted at `dd034c9`; M5.7 is Active. The accepted
entry boundary is twelve confirmed mechanisms, not global family exclusivity.
The later coverage preference remains Actors/AI, then Input, then
Event/scripting, without overriding the current milestone packet or allowing
future agents to turn inference into PC confirmation.

## 2026-08-16 M5.7 grain-gate resolver worker complete

[[EXP-20260816-170 - M5.7 grain-gate opening resolver]] implements the second
admitted M5 module without a runtime or asset read. The worker independently
rehashes the permitted retail work copy and rederives Tunnels
`0x00432EEA-0x00433043`, City `0x00433790`, and proximity helper
`0x00416580`. The Python evaluator preserves signed 32-bit wrapping and native
predicate order; Tunnels evaluates nine records in order so row-0/4 coupling
is stateful, while City emits state `0x20` and index-0-only address write
`[0x00599C69] = 1`. Downstream decay/countdown/slot deltas are metadata, not
executed behavior.

The tests reproduce EXP-139 distances, all ten exact accepted min-1/min
runtime transitions, row 1 only at its accepted “opens above minimum” scope,
row 4 only through its accepted coupling scope, and all three City aggregate
slot deltas. Thirty-four new fixtures and 60/60 combined grain/coordinate
fixtures pass in directly retained raw logs. The strict JSON reporting surface
states that global family exclusivity is not claimed and the City byte's
semantics remain Unknown. `KU-067` therefore stays open.

The first M5.8 audit of exact worker commit `efad1c2` independently retained
all native/model/receipt/scope claims but returned **REJECT** because default
`json.loads` accepted conflicting duplicate keys despite the strict-JSON
contract. The bounded correction rejects duplicates at request, nested gate,
and nested record levels, retains valid named-file/stdin input, and passes
38 new / 64 combined fixtures. One directly retained correction gate is
686/686 with Vault 482/0/0 and tracked audit 0, qualified by open KU-065. No
evaluator or evidence boundary changed.

Wholly fresh James then **ACCEPTS** exact correction `dfd3af3`, tree
`8b7d423`, in EXP-171. Independent literal and decoded-equivalent duplicate
cases, valid stdin/path identity, prior refusals, exact hashes, resolver 38/38,
combined 64/64, and a KU-065-qualified canonical 686/686 gate all survive.
The evaluator/static trace/threshold/standoff/coordinate surfaces are blob-
identical to the rejected worker. M5.7/M5.8 are complete at this boundary.

KU-065 remains open and qualifies both final-subject suite observations
recorded in EXP-170: the first reproduces its input-movie node
(`1 failed, 681 passed`), 20 isolated runs are
15 pass / 5 fail, and one canonical retry is 682/682.

## 2026-08-16 second coverage-driven packet: creature/actor pool and its script VM

[[EXP-20260816-172 - PC creature actor pool and behaviour VM census]] opens the
first row of the recorded Actors/AI → Input → Event/scripting preference.
Offline throughout: no runtime, debugger, breakpoint, or target write, and no
game asset beyond one metadata-level disc listing.

The row's open question — "where is the actor pool, and is there a state
machine or program list?" — is answered as both. Confirmed anchors: a 64-slot
pool at `[0x0059B628, 0x0059D728)` with stride `0x84`; a one-to-one binding to
64 `0x1C`-byte records that the loader copies to `[0x00599EB0, 0x0059A5B0)` on
record type `0x23` at `0x0046574D`, logged by the executable itself as
`LOAD: Type 35, CreatListRam.`; a build at `0x0041C420` called once from
`0x004679A0` inside level-load `0x004671D0` and gated on bit `0x10` of
`0x005C5E88`; a type-id domain of exactly 6..41 shared by the builder switch
and the release switch `0x0041B9F0`; a camera-radius activation pass in
`0x0041EC40` that fills the pointer list at `0x0059D7E0`; and a word-code
interpreter at `0x0041DC60` whose program counter lives in slot `+0x70`, whose
26-entry dispatch at `0x0041E848` covers opcodes `-1` to `24`, and seven of
whose eight no-body opcodes double as states through a second dispatch at
`0x0041E14F` (opcode 0 is the eighth and selects no mode).

Forty programs ship at `[0x004C7D00, 0x004C83F0)`. The instruction-size model
is the load-bearing claim and it is checked four independent ways: the 40
bodies are contiguous and end exactly at their pointer table, a linear decode
gives 463 instructions with zero misalignment, all 69 branch targets land on
instruction boundaries, and an entry offset written by unrelated code at
`0x004372A8` (script 33 `+0x1A`) lands on a decoded boundary.

Two cross-checks tie the static model to accepted evidence from other packets.
Opcode 16 compares squared XZ distance to `0x0059D910`/`0x0059D918`, the live
Flik X and Z identified at runtime by `EXP-20260815-128`. The "random" opcodes
read through cursor `0x00599C60`, which is initialised to the `rand.dat` load
buffer `0x0081B428` — a shipped file, and a cursor referenced 380 times of
which 197 write a computed value back, so it is shared rather than private to
this subsystem.

Honesty about novelty — **superseded twice below; the figure "three" and the
identity claim are both retracted**: the pool itself was already visible in three M2 exports
that recorded its extent, its `+0x7C` callback, its removal store and the
`0x004144C0 -> 0x0041EC40 -> 0x0041DC60` chain while chasing resource indices.
New here are the subsystem's identity, its level-data source binding, the
per-type tables, and the whole script layer. **Enemies, actors and AI** moves
Untouched → Bounded; **Event/scripting** moves Untouched → Touched on an
incidental find of five `EVENT : Event >>>%s<<< ...` log strings at
`0x004D823C`-`0x004D830C`, with no event code read. No milestone status
changes; M5 stays where `EXP-20260816-171` left it.

`KU-068` records that no runtime fact is claimed — nothing may cite an observed
script step, a creature identity, or per-type behaviour until one read-only
`+0x70` sample exists. `KU-069` records that the builder indexes
`0x004C881F` and `0x00599CA8` with the raw type byte and no upper bound, so
`type = 65` would write the first byte of the source table; no PC level file
was parsed, so nothing claims a shipped level reaches it.

Hygiene at this packet: Vault lint 488/0/0, tracked-file audit 0 violations,
canonical suite 686 passed — the suite figure carries the standing `KU-065`
qualification. No repository code changed.

This packet is worker-complete and **not** independently audited.

## 2026-08-16 creature census rejected on register and attribution; corrected

[[EXP-20260816-173 - Independent creature census audit]] returns **REJECT** at
`de7b80d`, and every finding is applied in the same commit that records it.

The analysis was not what failed. A fresh-context auditor re-derived every
opcode handler's PC advance from the disassembly without reading the worker's
table, re-ran the 40-program decode from raw bytes, and reproduced 463
instructions, zero misalignment, 69 branch/jump instructions with zero
off-boundary targets, and an identical per-opcode histogram. Both switch
tables, both loop terminations, every thunk and caller, the `KU-069`
arithmetic, and the `CreatListRam` anchor all survived. The auditor
strengthened one claim: `0x004671D0` is an `int3`-padded function head with no
`ret` anywhere in `[0x004671D0, 0x004679A0)`.

Seven defects, all in the register rather than the analysis:

- "Per type, the builder writes a count **and** a thunk" was false — of the 36
  types, 9 get both, 5 a thunk only, 5 a count only, and **17 neither**. The
  export's table was right; the Confirmed bullet and the `0x0041C420` dossier
  dropped the "—" cells.
- Operand spans were credited to "each handler's own range check". Opcode 11
  is the **only** handler with one; opcode 13 indexes `[eax*4+0x4c8754]` with
  the sign-extended operand and no check, so its 1..24 span is a data property
  — and a second instance of the very class `KU-069` exists for.
- Export §9 said "four" `EVENT` strings while listing five, contradicting the
  three notes that said five — and that is the sole evidence for the
  Event/scripting row.
- The cursor `0x00599C60` figure drifted: the export correctly said
  *referenced* 380 times, three notes said *advanced from* 380 sites. It is
  181 reads and 199 writes, of which 2 are the initialisation, so **197**
  sites write a value back.
- The novelty boundary under-credited `M2-fixed-pool-index-producer-census.md`,
  which had already published essentially all of §1.2 — the item §0 listed as
  new. No contradiction with any accepted M2 claim was found.
- Two quoted disassembly blocks silently dropped the one instruction that made
  each block mean what its prose said.
- §4's frame-array description ("terminated by `0xFF`, then two bytes") holds
  for 4 of 25 arrays; the measured trailing-byte distribution runs 1 to 8, and
  `0xFC` was omitted from the special values.

The audit also found a **third** unbounded index — source `+0x0D` into the
40-entry script table at `0x0041BD45` — so `KU-069` now covers three, and it
recorded the extent of the `0x004C881F` table and the producer of the `+0x6E`
value `0x3E6` as newly open rather than smoothing either.

Both row promotions survive: Bounded for Enemies/actors/AI and Touched for
Event/scripting, judged against the map's own status definitions.

`KU-065` gained a third independent recurrence: the auditor's **first**
`make test` returned `685 passed, 1 failed` of 686 at the same
`test_log_anchor_uses_only_new_log_bytes` node with the same `anchor_timeout`
/ `NextLife.` signature, on a packet that changed no code and no fixture; the
next run passed 686/686.

## 2026-08-17 creature census rejected a second time; scope and prior art corrected

[[EXP-20260817-174 - Second independent creature census audit]] returns
**REJECT** at `47d447f`, and every finding is applied in the commit that
records it. The analysis reproduced in full for the second time — 463
instructions, zero misalignment, 69 branch targets on boundaries, an identical
histogram, both switch tables, both loop terminations, the 380/181/199/2/197
split, the trailing-byte histogram, the five `EVENT` strings, every caller
claim, and every correction from the first audit. No derived number has ever
been wrong in this packet.

Two root causes, both methodological:

**The census read 45% of a function and made completeness claims over all of
it.** `0x0041DC60` runs to its only `ret` at `0x0041E7D3`; both prior drafts
stopped at `0x0041E1A8`. In the unread tail: flag bit `0x0002` **is** tested
(`0x0041E208`), refuting a Confirmed cell that said it never is — an error the
first audit introduced and the correction propagated; four more tested bits
(`0x0004`, `0x0100`, `0x0400`, `0x2000`); two further `+0x70` writers,
`0x0041E1EB` (`+2`) and `0x0041E2E1` (`+6`), refuting "the only place a
blocking instruction is ever stepped over"; record fields `+0x14`, `+0x1C`,
`+0x20`, `+0x24`, `+0x7A` described as merely zeroed; and — materially — the
**`call eax` at `0x0041E7C7`** through slot `+0x7C`, the only found edge from
the interpreter to the ten per-type handlers. That edge is register-indirect,
so no scan of the kind this project relies on would ever have found it.

**The headline novelty claim was prior art in an export the packet never
cited.** `M2-plant-request-origin-static-trace.md` already published the pool
rebuild, both 64s, the `0x700` copy, and the `LOAD: Type 35, CreatListRam.`
string — the last observed in retained hardware logs, i.e. with runtime
corroboration this offline census lacks. **Eight** exports reference the pool
base, not the three both drafts claimed. What is actually new is now stated by
address: no earlier export mentions `0x0041E848`, `0x004C83F0`, `0x004C8758`,
`0x0041C600` or `0x0041BC48`, and the two naming `0x0041DC60` treat it only as
a pointer-forwarding function.

Also corrected: a third silently truncated disassembly block (`0x0041DCEC`,
the only definition of the saved-PC slot the next block annotates); "two
consumers" where three sites were cited; and a **fourth** unbounded index —
opcodes 4 and 10 read the 64-entry table `0x005C5860` at `0x0041DDD4` and
`0x0041DEE1` with a raw source byte — so `KU-069` now covers four.
`EXP-20260816-173`'s own two wrong statements are corrected in place.

Both row promotions survive again, judged against the map's own definitions.
The coverage map gains two method rules: grep **every** export for the
principal addresses and distinguishing strings before claiming novelty, and
establish a function's extent before making claims scoped to it.

## 2026-08-17 creature census rejected a third time; extent, prior art and novelty corrected

[[EXP-20260817-175 - Third independent creature census audit]] returns
**REJECT** at `3f0debd`. The numeric analysis reproduced in full for the third
time — 463 instructions, zero misalignment, 69 branch targets on boundaries, an
identical histogram, every switch table, both loop terminations, the
380/181/199/2/197 split, every file offset — and the auditor confirmed the
published §6.1 reproduction snippet runs verbatim. **No derived number has been
wrong at any point in this packet.** All findings are applied in the commit
that records the audit.

**The function extent was still wrong.** `0x0041DC60`'s only `ret` is at
`0x0041E7D3`, but that is not its end: `0x0041E7D4`-`0x0041E845` is entered
from `0x0041E6CD` and `0x0041E6D8`, shares the frame, and returns with
`jmp 0x41e6e6` at `0x0041E841`. The extent is `0x0041DC60`-`0x0041E845`. Three
drafts got this wrong three different ways — first by reading under 40% of the
function, then by taking the first `ret` as the end. The consequence: a
**fourth** `+0x70` writer at `0x0041E7FE` (`+2`, entered when the mode local
exceeds 2), which the previous draft's enumeration explicitly denied.

**The flag table missed a site in its own declared scope.** Bit `0x0020` is
also tested at `0x0041BD6C` (`test bl,dl`, `bl = 0x20` from `0x0041BD17`)
inside `0x0041BD10` — the test that gates the block §2.1 itself discusses.
Thirteen sites, not twelve.

**The prior-art list was wrong in both directions.** It named
`M2-generic-resource-index-producer-census.md`, which contains **no**
occurrence of `0x0059B628`, and omitted `M2-second-deferral-hard-truth-audit.md`,
which publishes §1.1's headline arithmetic verbatim — "The 64-record pool is
`[0x0059B628,0x0059D728)` with stride `0x84`" and
`0x0059B628 + 63 * 0x84 = 0x0059D6A4` — plus `+0x5C` as a flags field.

**The novelty claim is withdrawn in its address-based form.**
`ghidra-evidence.json` — 8 MB, machine-generated, committed in the same
directory at the earliest baseline — already contains a decompilation of
`FUN_0041dc60` rendering the 26-way opcode switch, the nine-way opcode-11
sub-switch, `&DAT_004c8754 + operand * 4`, the `0x005C5860` indexing, the call
through record `+0x7C`, and both extra program-counter advances, plus an
explicit `0041dcf9 -> 0041e848` reference. What remains genuinely this
packet's is narrower and now stated as such: the two byte case tables
`0x0041C600` and `0x0041BC48`, which appear in no artifact here because a
decompiler renders a `switch` without exposing its case-index table; and the
authored, validated model — instruction sizes, the decoded 40-program listing,
and the four structural validations — which decompiler output does not contain
and which, per [[Agent Operating Manual]], is the difference between evidence
and a stated claim.

Also corrected: a fourth silently truncated disassembly block (`0x0041C47D`,
the `jmp` that makes §3.3's two stores mutually exclusive); the condition slot
is written by opcode 11 operand 5 as well; eight further `+0x5C` sites reached
by the absolute form `0x0059B684` outside the five analysed functions; the
`0x005C5860` "64 entries" restated as the bound of the zeroed region; and
`EXP-20260816-172`'s stale "rejected once" audit history. `EXP-20260817-174`'s
own two errors are corrected in place.

Both row promotions survive a third time. The coverage map gains a rule that
generalises well beyond this packet: **grep the generated
`ghidra-evidence.json`, not just the authored exports** — it is effectively
unread and it can contain a whole subsystem.

## 2026-08-17 creature census rejected a fourth time; accounting layer corrected

[[EXP-20260817-176 - Fourth independent creature census audit]] returns
**REJECT** at `1c499bf` — on the accounting layer alone. The numeric core
reproduced for the fourth time, and two things closed for the first time: **all
six quoted disassembly blocks now match objdump byte for byte** (the defect
class that recurred in all three previous rounds), and the extent correction
`0x0041DC60`-`0x0041E845` was independently verified with **nothing extending
further** — four `+0x70` writers and no more, a complete and correct flag
enumeration, and a nine-artifact prior-art list whose every attribution checks
out line by line.

Nine defects, all arithmetic, counting or attribution, and all in the sections
whose subject is honesty:

- "under 40%" is **44.4%** (1,352 of the extent's 3,046 bytes), and disagreed with four
  artifacts saying 45% and with the export's own "more than half" for the
  remainder. Byte counts replace the percentage.
- "Thirteen sites in total" is unreproducible: twelve bits carried by **21
  distinct instructions**. The count is withdrawn and the 21 addresses are
  enumerated instead.
- The eight-file prior-art list and the "no earlier export mentions …" claim
  were blamed on the **second** draft; both first appear in the **third**
  (`3f0debd`), which the same export's §0.1 already said.
- The generated Ghidra export renders **three** extra program-counter
  advances, not two — and the third is `0x0041E7FE`, exactly the writer the
  previous audit presented as its discovery. It was already there, guard and
  all. Understating it flattered this packet, so it is now quoted in full.
- The mode slot `[esp+0x4c]` is read at **four** sites, not two; the fourth is
  the load §5.1's own table cites.
- `KU-069` and one dossier still called `0x005C5860` "64-entry" after §1.4
  withdrew that framing.
- `EXP-20260816-173`'s appended section still asserted the superseded extent
  as fact.
- `EXP-20260816-172` contained a sentence that both asserted and denied the
  same thing and named a `ret` at `0x0041E845`, which is the last byte of a
  `jmp`.
- §1.1's "three" record-index sites is **at least four**: `0x0041519B` does the
  same arithmetic in different registers and reads `+0x5C` at `0x004151B0`.

Both row promotions survive a fourth time. Four fresh contexts have now
re-derived the analysis independently and **no derived number in it has ever
changed**; every rejection has been about scope, register, counting or
attribution around correct work.

## 2026-08-17 creature census rejected a fifth time; a declared correction had not landed

[[EXP-20260817-177 - Fifth independent creature census audit]] returns
**REJECT** at `a540dc7`. The analysis layer is flawless for a fifth time —
every number re-derived from the bytes without reference to the text, and not
one disagreed, including all six quoted disassembly blocks byte for byte and
the published §6.1 snippet run verbatim.

The rejection is that **a correction declared applied was not applied**. The
fourth audit's flagship defect — a Confirmed-register sentence naming a `ret`
at `0x0041E845`, an address holding the last byte of a `jmp` — was reported
fixed in `EXP-20260817-176`'s Correction section and in the commit message.
The edit had re-anchored the sentence's second half and left the broken first
half untouched. Two minors were likewise declared applied and were not: the
interpreter dossier still asserted the "movement modes" reading at
`status: confirmed, confidence: high` after the export withdrew it in the same
commit, and the Experiments MOC still narrated the superseded extent directly
above the bullet correcting it.

Four further defects, all counting or attribution: four rejection counts
disagreed across artifacts ("three times", "all three auditors", "rejected
once" against a roadmap saying four); §0.0 blamed the **third** draft for a
phrase that first appears in the **fourth**, in the section whose subject is
accurate attribution and as the mirror image of the defect the previous round
rejected for; the coverage map introduced **six** method rules as "three",
inside the paragraph that now carries "prefer enumerations to aggregate
counts"; and the scope note cited `0x00572000` as the lowest address used when
the document never uses it — the lowest cited is `0x00599B20`.

Two structural changes were made to reduce these classes. Rejection counts are
**removed** from the coverage map and the Experiments MOC in favour of a
pointer to the packet's own Audit history, and the rule list's count was
dropped. (Both were installed imperfectly and the sixth audit caught it: the
rule lead-in acquired a different wrong count, and the Audit history it
delegates to omitted the fifth audit. Corrected there — and the claim that
they "cannot go stale again" is retracted, since it was itself the kind of
assertion this ratchet exists to catch.) And the coverage map gains
the rule this round earned: **verify each edit landed before reporting it
applied.** "All findings applied" is a claim like any other, and it has now
been false here once.

Both row promotions survive a fifth time. Five fresh contexts have re-derived
the analysis independently and **no derived number in it has ever changed**.

## 2026-08-17 creature census rejected a sixth time; the audit register itself

[[EXP-20260817-178 - Sixth independent creature census audit]] returns
**REJECT** at `2ceef9c`. The analysis reproduced for a sixth time — every
number re-derived from the bytes, all six quoted disassembly blocks byte-exact,
the §6.1 snippet run verbatim, and the auditor additionally confirmed the
`+0x5C` enumeration is exactly 21 instructions with 5 of the interpreter's 10
past `0x0041E1A8`, so "missed half" is exact. The §0/§0.0 prior-art and
novelty accounting is now judged **honest** on membership, content and
self-history — the first round at which that section has passed.

Both defects are in the bookkeeping the fifth round introduced:

- The coverage map's rule lead-in replaced "three further things generalise"
  with "Its **four** audit rounds produced the rules below … which is why it is
  no longer introduced by a count" — a wrong count (there were five) inside a
  sentence claiming there is no count, in a list that includes a fifth-round
  rule. Current State then asserted that remedy as accomplished. The lead-in
  now carries no number and records both failures instead.
- `EXP-20260816-172`'s Audit history — the register the coverage map now
  points to *instead* of a count — omitted the fifth audit entirely and stated
  "all findings applied in the commit recording each one", which
  `EXP-20260817-176`'s amended Correction section, edited in the same commit,
  explicitly denies. It now lists every round and states the one documented
  exception plainly.

Minors applied: the third draft's novelty sentence is now quoted verbatim; the
record-index draft history is stated accurately (drafts 1-2 said "two" while
listing three addresses, drafts 3-4 said "three"); §0.1 says "three drafts,
two ways" and separates the two wrong
percentages; and `+0x40` has **ten** stores across the five functions, three of
them in the unanalysed region — more than either the packet or the auditor had
listed. The extent reads 3,046 bytes everywhere outside the audit notes, which
correctly retain 3,045 as the superseded figure.

Both row promotions survive a sixth time. Six fresh contexts have re-derived
the analysis and **no derived number in it has ever changed**; every rejection
has been on the surrounding prose, and the last two on the machinery built to
stop the prose going wrong.

## 2026-08-17 creature census rejected a seventh time; audit history made a fact table

[[EXP-20260817-179 - Seventh independent creature census audit]] returns
**REJECT** at `f13da89`. The analysis reproduced a seventh time, verified more
finely again: all 69 branch targets land inside their **own** script as well as
on instruction boundaries; the `+0x5C` enumeration is exactly 21 after checking
every rebased base register in all five functions for other forms; `+0x40` is
exactly the ten listed stores; and §10's "more than half" is 1,694/3,046 =
55.6%. The prior-art and novelty accounting passed a second time, including the
now-verbatim third-draft quotation.

All three defects are in this packet's description of **its own audit
history** — the layer the last two rounds also failed on:

- `EXP-20260816-172`'s Audit history asserted "one documented exception" and
  "Every other round's findings did land". False: `EXP-20260817-178` records in
  the same commit that `EXP-20260817-177`'s extent-figure minor landed only in
  the export, so **two** rounds had unapplied findings. Verified at `2ceef9c`,
  where `3,045` still stood in `EXP-172` and Current State.
- `EXP-20260817-177`'s Correction section was never amended, breaking a
  convention applied to rounds 1-4, and still asserted four things round 6
  falsified.
- The coverage map's rule said "'All findings applied' … has been false here
  **once**"; it has been false twice.

The durable fix: **the Audit history is now a per-round fact table that makes
no global claim about whether findings landed.** Three successive drafts made
such a claim and each was falsified by the next round — the failure was
structural, not clerical. A table row states what one round found and whether
that round's commit applied what it declared; adding a row is mechanical and
cannot be globally wrong. The coverage map's rule is updated to match: prefer
recording per-item facts over asserting completeness.

Minors applied: the rule list "has grown over the rounds" rather than "with
every round"; the rule drops its false "nine defects, three not applied" count
and describes the two failed correction passes qualitatively instead; Current State says 3,046 "everywhere outside the audit
notes"; the roadmap no longer opens with a stale total; and §0.1's
"arithmetically impossible for any endpoint" is replaced by the two computed
figures.

Both row promotions survive a seventh time. Seven fresh contexts have
re-derived the analysis and **no derived number in it has ever changed**.

## 2026-08-17 creature census ACCEPTED with zero defects

[[EXP-20260817-180 - Eighth independent creature census audit]] returns
**ACCEPT** at `2cb6b07` with **zero defects**, closing the chain opened by
[[EXP-20260816-172 - PC creature actor pool and behaviour VM census]].

Every number re-derived an eighth time from the retail bytes without trusting
the text, including two checks finer than any earlier round: all 69 branch
targets land inside their **own script** as well as on instruction boundaries,
and reachability shows **zero** stored little-endian pointers to any of the
five functions or their thunks. The prior-art accounting is judged honest in
both directions — the nine-artifact membership is exactly the set of files
containing the pool base, and the two byte case tables really are the only two
of the five addresses absent from every artifact. All seven Audit-history rows
check out, and every correction the seventh round required landed.

**One new fact about the binary** arrived as a minor and is now recorded: an
**eighth writer of the mode slot** at `0x0041E2E9`
(`mov DWORD PTR [esp+0x50],0x1`), which reaches the same storage as
`[esp+0x4c]` only because `push 0x59d910` at `0x0041E2E4` displaced `esp` by 4.
No search on the displacement finds it; `ghidra-evidence.json` corroborates it
independently as `param_3 = (int *)0x1;`. It falsifies nothing — the site
writes `1`, consistent with the mode-`> 2` gate — and §5.3 now carries the
`esp`-delta caution for any future sweep of that slot.

**Accepted state.** Enemies, actors and AI stands at **Bounded**;
Event/scripting at **Touched**; `KU-068` keeps every runtime claim closed and
`KU-069` records four unbounded table indexes. No milestone status changed and
M5 stays where `EXP-20260816-171` left it.

**The chain, honestly.** Eight fresh contexts re-derived the analysis and **no
derived number in it ever changed**. Of the seven rejections, three were on
substance — a scope claim over a function only partly read, an unread function
tail hiding an indirect call, and prior-art attribution — and four were on the
prose describing the packet and its own audit history. The durable lessons are
in [[Subsystem Coverage Map]]: grep every export including the generated
`ghidra-evidence.json`; establish a function's extent before scoping claims to
it, and do not assume the first `ret` is the end; prefer enumerations to
aggregate counts and derived percentages; verify each edit landed before
reporting it applied, and prefer per-item facts to completeness assertions.

The next packet under the recorded preference is **Input**, whose row already
carries `0x0042F350` and the single `DirectInputCreateA` site from
`EXP-20260816-159` — an import-anchored row, and so a cheaper one by the audio
census's own method note.

## 2026-08-17 third coverage-driven packet: PC input subsystem

[[EXP-20260817-181 - PC input subsystem static census]] opens the second row of
the recorded Actors/AI → Input → Event/scripting preference. Offline
throughout: no runtime, debugger, breakpoint, target write, or asset read.

The row's question — "which device objects and formats are acquired, and where
is per-frame state read?" — is answered on both halves.

**Bring-up `0x0042F350`** (extent `0x0042F350`-`0x0042F565`, one `ret`) calls
`DirectInputCreateA` at `0x0042F43D` with version `0x0500`, then creates a
keyboard device from the GUID at `0x004C0230` — whose bytes decode to
`{6F1D2B61-D5A0-11CF-BFC7-444553540000}`, `GUID_SysKeyboard` — with data format
`0x004AFE90` (decodes to `c_dfDIKeyboard`: 24/16/`0x2`/256/256) and cooperative
level `6` (`DISCL_NONEXCLUSIVE | DISCL_FOREGROUND`). It then enumerates
joysticks (`dwDevType 4`), and for each one calls `QueryInterface` for
`0x004C0220` — `{5944E682-C92E-11CF-BFC7-444553540000}`,
`IID_IDirectInputDevice2A` — with data format `0x004AEE70` (`c_dfDIJoystick`:
24/16/`0x1`/80/44) and cooperative level `5`
(`DISCL_EXCLUSIVE | DISCL_FOREGROUND`) — a **different** level from the
keyboard's.

**Per-frame read `0x0042EBC0`** (code extent `0x0042EBC0`-`0x0042EEBB`, reached
through thunk `0x00401B5E` from `0x00464E1C` and `0x0049BDB7`) clears and fills
the 256-byte keyboard buffer at `0x00598A10`, folds the three right-hand
modifiers onto their left-hand scancodes, walks a twelve-entry binding table
over `[0x004D8430, 0x004D8490)`, and stores the accumulated action bits to
`0x00598B10`. The four direction masks additionally synthesise `±0x8000` axes
into `0x004F0440`/`0x004F0444`. Joystick 0 is read with `Poll` (`+0x64`) then
`GetDeviceState` of `0x50` bytes into `0x00598B60` — `Poll` exists only on
`IDirectInputDevice2A`, the interface the bring-up queried for, and `0x50` is
`c_dfDIJoystick`'s own `dwDataSize`.

Two findings worth carrying beyond the row:

- **The binding table is written at runtime, not stored, and the controls are
  configurable.** `[0x004D8430, 0x004D8490)` is all zero in the file image;
  `0x0042F0F0` writes the twelve defaults (UP/DOWN/LEFT/RIGHT, LCONTROL,
  LSHIFT, Z, SPACE, C, LMENU, RETURN, X) and is reached from two call sites.
  Twenty-two further stores, in blocks at `0x00430C3F`-`0x00430CBC` and
  `0x00431022`-`0x004310A4`, apply a `0x18`-stride byte array at `0x004D9CF9`;
  `0x00430B10` copies the live table back into it; and a dispatcher at
  `0x00430FF6`/`0x00430FFD` selects between applying the array and restoring
  defaults. A control mod must target the array, not the live table.
- **`GetAsyncKeyState`'s import thunk is dead code.** The IAT slot `0x0086478C`
  has exactly two little-endian occurrences in the image; nothing anywhere
  targets the `jmp` thunk `0x004AEB1C`. The import is reached only by loading
  the slot into `esi` at `0x004A7841` and calling the register, at eight sites
  in chooser `0x004A7600`. A scan-based caller census would have called the
  import unused — a concrete instance of the limitation the audio census's
  method note warns about. The chooser path and `0x0042EBC0` are disjoint.

Novelty is bounded in §0 of the export: the `0x0042F350`/`0x0042F43D` anchor is
the audio census's, the whole `GetAsyncKeyState`-in-the-chooser finding is
[[PC autonomous game control]]'s and `EXP-20260816-145`'s, and
`ghidra-evidence.json` already contains decompilations mentioning every address
used. What is new is the authored, verified model.

**Input** moves Touched → **Bounded**. `KU-070` records what the action bits
mean, what consumes them, and whether the bindings are remappable — and keeps
every runtime and control-name claim closed. No milestone status changed; M5
stays where `EXP-20260816-171` left it.

This packet is worker-complete and **not** independently audited.

## 2026-08-17 input census rejected; the controls turn out to be configurable

[[EXP-20260817-182 - Independent input census audit]] returns **REJECT** at
`67ca1b5`, and the correction makes the packet materially better: the thing the
census said it could not find is there.

Everything else reproduced — both GUID and both `DIDATAFORMAT` decodings with
their flag names, every vtable offset, both cooperative levels, both function
extents with every direct branch enumerated, the twelve binding pairs, the
direction tables, the right-modifier folding, the dead-thunk claim in full, and
every quoted disassembly block byte for byte. The §0 novelty negative verified
**exactly**: 0 hits for all ten addresses across all 504 Vault notes and all 43
markdown exports of the parent tree `0f69566`. The previous packet's prior-art failure
mode did not recur.

**The gating defect:** §3 claimed "no other writer was found" for the binding
table. The image has **22 further stores** into it, in blocks at
`0x00430C3F`-`0x00430CBC` and `0x00431022`-`0x004310A4`, each applying a
`0x18`-stride byte array at `0x004D9CF9`; `0x00430B10` is the exact inverse,
eleven byte reads copying the live table back; and a dispatcher at
`0x00430FF6`/`0x00430FFD` selects between applying the array and restoring
defaults. **The controls are configurable**, and the census had declared that
question open on the strength of a scan which, run correctly, answers it. The
false negative had propagated into `KU-070`, the coverage row, this note and
the modding guidance; all are corrected.

Five more: `1` is `DIEDFL_ATTACHEDONLY`, not `DIEDFL_ALLDEVICES`; the joystick
pair table's first column **is** a `DIJOYSTATE` button index by instruction
(`0x0042ED77` tests `rgbButtons` at `0x00598B90 = 0x00598B60 + 0x30`, and
`0x30 + 32 = 0x50` is the decoded `dwDataSize`), so that reading moves Inferred
→ Confirmed; both "instruction order" claims were false, the tables are in
address order; "the two reads in §2" undercounted its own three; and one
`GetDeviceState` was cited at `0x0042F6AC` instead of `0x0042F6AE`.

The lesson is narrower than the previous chain's and worth stating exactly: the
extents were right and were verified, but **an extent being correct is not the
same as the range having been read**. `0x0042ED6F`-`0x0042ED8C` sat inside a
stated extent, went undocumented, and falsified an unhedged negative written
over it. Where a negative is asserted about a range, the range has to be read,
not just bounded.

Input stays at **Bounded**; the row's open question is rewritten now that the
remapping half is answered. `KU-070` narrows to what the action bits mean, what
consumes them, and the identity of the configuration screen.

## 2026-08-17 input census rejected a second time; two address-level claims

[[EXP-20260817-183 - Second independent input census audit]] returns **REJECT**
at `afee530`. The substance — including the whole §3.1 correction the first
round required — reproduced in full: a byte-level scan found **62**
little-endian occurrences of an address in `[0x004D8430, 0x004D8490)`, all in
`.text`, none as data, accounting for all 46 stores, the 11 inverse reads and
the loop references, with **no hidden writer of any kind**. Both blocks, the
`0x18` stride, the eleven pairwise read/array mappings and the dispatcher's two
arms all checked out, as did both GUIDs, both `DIDATAFORMAT`s, every vtable
offset, both extents by whole-image branch analysis, and the §0 novelty
negative re-derived from scratch.

Two defects, both address-level:

- **`0x0042F38E` does not exist.** §4's store-order parenthetical cited it; the
  store is at `0x0042F38D`, and the export's own §1.1 block proves it. That
  line was added by the *previous* correction pass, inside the sentence written
  to fix the first audit's ordering defect.
- **"`0x00598B14` … not read here" was false**, and contradicted §1.4 of the
  same document, which already said the device loop runs while
  `edi < [0x00598B14]`. It is read at `0x0042F4C5` and `0x0042F543`.

Minors applied: the joystick-pair store span in the `0x0042F350` dossier
(`0x0042F388`-`0x0042F421`, last store ending `0x0042F42A`); §0's
`EXP-20260816-159` quotation now verbatim; the novelty negative covers **504**
parent-tree notes, not 508 — 508 is the count at the audited commit, which
would have included the packet's own notes; `Environment Status` now records
**three** `KU-065` denominators (648, 682, 686); and the Subsystems MOC's Input
block, the one artifact that had missed the §3.1 correction, now carries it.

One **scoping refinement** rather than a defect, now in §3.1: block A
(`0x00430C3F`-`0x00430CBC`) is reached only through thunk `0x00401DF2`, which
has **zero** call sites and zero data occurrences, so block A's reachability is
unestablished. The remappability finding rests on block B, which is live off
the dispatcher, and on `0x00430B10`.

The pattern is worth naming: both defects were introduced or left by the
correction of the previous round, and both are of the same class the round
before named as its lesson. Corrections are themselves claims and need the same
verification as the work they correct.

## 2026-08-17 input census ACCEPTED with zero defects

[[EXP-20260817-184 - Third independent input census audit]] returns **ACCEPT**
at `52a9024` with **zero defects**, closing the input packet.

Every numeric and completeness claim was recomputed from the binary: the
46/24/22 store census, both block address lists, the `0x18`-stride array and
its eleven pairwise inverse mappings, both dispatcher arms, both extents, both
GUIDs, both `DIDATAFORMAT`s, every vtable offset, the twelve binding pairs, the
direction tables, the button loop, the dead-thunk claim, the eight `call esi`
sites, and the §0 negative re-run against the correct parent tree. **Every
cited `.text` address was checked to be a real instruction start** — all 140 of
them, with five correctly-explained exceptions — which was the class that
caused the second rejection.

The new block-A caveat, the highest-risk text in the audited commit because the
correction pass wrote it, is independently true: `0x00401DF2` has zero call
sites and zero data occurrences, and nothing enters block A except that thunk.

The auditor verified two claims **beyond** their stated scope — `0x00598BC8`
and `0x00598B1C` each have exactly two writers image-wide — and located the
enumeration callback's write of `0x00598B14` at `0x0042F077`.

Nine minors applied, several of which had erred *against* the packet's own
novelty: `ghidra-evidence.json` mentions every **principal** address, not every
address; the `.data` preamble was over-broad, since `.idata`/`.rsrc`/`.reloc`
lie above `0x004ED400` and do have file content; an ownerless quoted gloss in
§0 now has an owner; and the block-A caveat has propagated to `KU-070`,
`EXP-181` and the Subsystems MOC.

**Accepted state.** Input stands at **Bounded**. `KU-070` keeps every runtime
and control-name claim closed and now records that the controls are
configurable, with block B as the demonstrated path and block A's reachability
open. No milestone status changed; M5 stays where `EXP-20260816-171` left it.

**The chain, honestly.** Two rejections. The first was a false completeness
claim — "no other writer was found" — which concealed a real finding: the
binding table is applied from a configuration array with a defaults/apply
dispatcher, so the controls are remappable. The second was two address-level
claims, **both introduced or left by the first correction**. The identifier
layer, both function extents and the §0 prior-art boundary reproduced at every
round, and the prior-art failure mode that cost the creature census four rounds
did not recur once.

The lesson this packet adds to [[Subsystem Coverage Map]]: an extent being
correct is not the same as the range having been read, and a correction is
itself a claim needing the same verification as the work it corrects.

The next row under the recorded preference is **Event/scripting**, which
already has an anchor: the five `EVENT : Event >>>%s<<< ...` log strings at
`0x004D823C`-`0x004D830C`, with `0x004D82CC` pushed at `0x0042DC14`, found
incidentally by the creature census.

## 2026-08-17 fourth coverage-driven packet: PC event subsystem

[[EXP-20260817-185 - PC event subsystem static census]] opens the last row of
the recorded Actors/AI → Input → Event/scripting preference. Offline
throughout: no runtime, debugger, breakpoint, target write or asset read.

The row's question — "does the PC port have an event VM or data-driven trigger
stream, and is it the same machinery as the creature scripts or separate?" —
gets a clean negative on both halves.

**There is no VM and no trigger stream.** The event table is
`[0x005982B0, 0x00598670)`: 16 records of `0x3C` bytes, base and stride both
taken from `0x0042DB10`'s `rep movs` of 15 dwords to `[eax*4+0x5982b0]`, and
`0x005982B0 + 16 * 0x3C = 0x00598670` is exactly where a buffer whose first 128
bytes are zeroed begins (128 is the width of the write, not a known object
size). A record holds an id word at `+0x00`, **three native callbacks** at
`+0x04` (**create**, called `0x0042DC2A`), `+0x08` (**unnamed**, called
`0x0042D9A5`) and `+0x0C` (**destroy**, called at three sites), a name at
`+0x10`, and an in-use flag at `+0x34`. `create` and `destroy` are the binary's
own words, taken from log calls a few instructions before them;
`+0x08` has no such string and is left unnamed. There is no opcode, no
instruction stream and no interpreter anywhere in the subsystem. "Event" here
names a subsystem lifecycle slot, not a gameplay trigger.

The layout is cross-checked from a second addressing form: derived from the
`id`-scaled absolute addresses, then re-read off the destroy pass, which walks
the same records backwards with `esi` on `+0x34` — all **nine** of its distinct
displacements resolve consistently, reaching every field but `+0x00`. The
origin is imported from the first derivation, so this confirms the relative
layout, not the anchor.

**It is disjoint from the creature machinery**, tested by address intersection
in both directions: none of `0x0041DC60`, `0x004C83F0`, `0x0041E848`,
`0x0059B628` or `0x004C8758` appears in `0x0042D950`-`0x0042DD90`, and none of
`0x005982B0`, `0x005982B4`, `0x005982AC` or `0x00598670` appears in
`0x0041DC60`-`0x0041E845`.

Seven functions, every extent established from its single `ret` and padding,
with every direct branch enumerated — the only outbound target from any of them
is `0x00401CF8` (→ `0x004ADEA0`, which writes the log file `"bugs.log"` — it
reaches `KERNEL32.dll!DeleteFileA` with that filename through `0x004B13E0` —
and whose body is gated on `0x008620AC`). **Four of the seven
have no reachable caller**: `0x0042D950`, `0x0042D9D0`, `0x0042DA00` and
`0x0042DCA0` are each reached only through a thunk (`0x0040169F`, `0x0040179E`,
`0x00401217`, `0x00401140`) that itself has zero callers, and neither thunk nor
function occurs anywhere in the file as a little-endian dword — all eight scans
return zero.

Three negatives worth carrying: `0x005982AC` is written twice and **read
nowhere**; the id is **never bounds-checked** at any of the three `id`-scaled
entry points; and `+0x00` and `+0x10` **survive every clear**.

There are **two** static registration call sites, `0x0043DAF5` and
`0x0043DB10`, passing `0x004D81A8` id 2 `"WINDOWS"` and `0x004D81E8` id 3
`"DIRECTX"`. Whether either executes is not established — the enclosing
function is unanalysed.

**This closes a loose end in the audio census.** `EXP-20260816-159` recorded
that its own central initializer `0x0042BA60` has zero direct call sites and is
reached only through the `.data` record at `0x004D81E8`. That record is an
event record, and `0x0042BA60` is its `+0x04` field — the slot the register
function calls at `0x0042DC2A`. That is a static path, not an observation that
it runs, and it is why a direct-call census could not find an entry point. One
field reading is refined: the record's leading `3` is the event id, not "a count
of 3". That census's offsets were exactly right.

**Event/scripting** moves Touched → **Bounded**. `KU-071` records what the six
callbacks do, whether any event is registered outside the two static sites, and
the four never-read fields — and states explicitly that this subsystem is not a
trigger mechanism, so the known gameplay-trigger evidence remains the grain-gate
family under the separate Triggers row. No milestone status changed; M5 stays
where `EXP-20260816-171` left it.

Prior art is credited more precisely than the first draft managed:
`ghidra-evidence.json` already carries decompiled bodies for `0x0042DB10`,
`0x0042D980` and `0x0042DA70` that render the base, the `0x3c` stride, the three
callback slots, the flag and the name, so the table geometry and record layout
were **re-derived here from instructions, not first found here**. What is new is
the four dead entry points (ghidra has no entry for those four at all), the two
reachers its lists omit (`0x004AE863`, `0x004121A1`), the decoded records, the
relocation result of §2.1 — which is a negative on the absolute addressing form
only, **not** a closure proof, and which the second-round audit found rather
than this census — the disjointness result, the audio
cross-link and the negatives above. **Not** the caller analysis in general — the
file's three `thunk_FUN_` entries carry populated `callers` lists covering 7 of
the 9 reachers — and **not** the log-formatter reading, which it also carries.

**Five** fresh James audits rejected this packet in succession — 12, then 10,
then 16, then 12, then 15 defects — before it reached its current state. Each round's findings
were re-verified against the binary before correcting, and each round the
*model* survived: geometry, layout, extents, records and disjointness were
re-derived independently by every auditor and held throughout. What kept failing
was the writing around it.

- **Round 1 (12):** a false "every log site" claim and a misread of
  `0x00598670`'s role, a missed fourth thunk, a short reacher list, a wrong
  "except the name", eight displacements where there are nine, an incomplete
  flag-site list, the prior-art under-attribution, the unsupported name
  "update", two inferences inside a set declared inference-free, and three
  missing negatives.
- **Round 2 (10):** four round-1 fixes had landed **only at the first
  occurrence** of the wording, and one over-corrected into a fresh false claim
  about the prior-art file's `callers` lists.
- **Round 3 (16):** the same partial-propagation failure a third time; a count
  adopted from the round-2 audit that mixed two address ranges; a causal
  sentence about the surviving name that is false at two of its three sites; and
  a third under-crediting of `ghidra-evidence.json`, which also carries the
  `0x004ADEA0` log-formatter reading.

- **Round 4 (12):** three fixes got a fact wrong that the audit requesting them
  had stated correctly; and a defect-phrase sweep could not find carriers where
  the corrected phrasing was simply absent.
- **Round 5 (15):** a dropped qualifier that made a §2.1 sentence false, a
  withdrawn closure claim, a wrong "none is an import" about the prior-art file,
  and one file asserting both sides of its own Confirmed/Inferred boundary.
- **Round 6 (14):** a false description of `0x004B13E0` inside the fix for round
  5's finding about it, and three withdrawals that reached the export and
  stopped there.

The durable lesson, recorded because it recurred in six consecutive rounds:
**a fix applied at the first occurrence is not a fix applied**, and a correction
is a claim needing the same verification and the same sweep as the work it
corrects. Retractions need sweeping too, not just corrections.

The structural response, adopted at round 6 on the auditor's recommendation:
the **export is normative** and the Vault carriers point to it rather than
paraphrase it. Ten paraphrases of one finding meant every correction was ten
rewrites and ten chances to be wrong.

**The packet is closed unaccepted** at round 6 (`DEC-20260817-138`). No
milestone gates on the row, and the Vault codifies no acceptance requirement.
The export carries a status header stating the position plainly: the
conclusions are confirmed by six independent re-derivations and can be cited
normally; the individual addresses, offsets and enumerations have a
demonstrated defect rate and must be re-derived from the binary before use,
particularly in any milestone-gating claim.

Round 3 corrected the §2.1 result the round-2 audit had found; round 5 then
withdrew the closure claim built on it. What survives is a negative on the
absolute addressing form: 47 absolute references into
`[0x005982A0, 0x005986F0)`, all inside the seven functions. Computed references
and indexed bases outside the range are not covered. All 26,713 type-3
base relocations were decoded: exactly 47 point into `[0x005982A0, 0x005986F0)`
and all 47 lie inside the seven functions. Because a PE loader must relocate
every absolute 32-bit reference, that is exhaustive for the absolute form.

## 2026-08-17 M5 third-module candidacy

[[EXP-20260817-186 - M5 third-module candidacy ranking]] opens M5.9, the first
step of M5's own procedure: rank candidate modules against the six entry-gate
criteria before deriving any contract. Offline throughout.

**The creature behaviour VM is rejected on criterion 1.** It looked like the
obvious candidate — the actors/AI census that mapped it was accepted with zero
defects — but its code range `0x0041DC60`-`0x0041E845` makes **16 direct calls
to 15 distinct engine thunks** plus one indirect `call eax` at `0x0041E7C7`.
Three of those targets — `0x00464D40`, `0x00403A10`, `0x0041A550` — appear in
no authored Vault note or export at all. A module depending on fifteen engine
services, a quarter unidentified, has no bounded contract. `KU-072` records the
three.

**The input action-bit resolver is selected.** In `0x0042EBC0`-`0x0042EEBB` the
last outbound transfer of any kind is the DirectInput vtable call at
`0x0042ED3E`; everything from `0x0042ED41` to the end — the whole binding walk
and axis path — contains **zero calls**. Its contract reads straight off the
instructions: the keyboard pass at `0x0042ED6F`-`0x0042ED8C` walks
`[0x004D8490, 0x004D84D0)` in `0x08` steps, indexes the state array at
`0x00598B90` by each record's scancode, ORs the record's 16-bit mask into the
accumulator, and stores the result to `0x00598B10` at `0x0042ED9B`. The axis
path reduces by `sar 8`/`and 0xFF`/`sub 0x80`/`shl 8` and compares against
`±11200`.

The other four criteria are met from recorded evidence: the accepted input
census supplies addresses and offsets, the CAP-002 input movies supply runtime
observations, both binding tables are executable data so fixtures need no game
content, and the census records the live table's zero-in-image state and its
two runtime writers.

**Selection is not admission.** M5 stays Active. The named next packet is
**M5.10 — input action-bit resolver contract and implementation**, which must
re-derive the contract from the binary rather than from this summary.

One methodological note, applying the event packet's lesson immediately: the
`8`-stride binding table looked like a new find and is already documented at
line 430 of the accepted input census. Checked before claiming, not after.

## 2026-08-17 runtime berry-throw reconnaissance

[[EXP-20260817-187 - Runtime berry throw reconnaissance]] is the first runtime
work of this session and the first target write. It adopted a Training session
the researcher had already launched (PID 57939) rather than starting a competing
instance.

**It bound the static input model to observed values.** The throw action bit is
`0x8000` — derived statically from the default binding table in the accepted
input census, and now observed in all three action words while Ctrl is held. The
latch at `0x00464E10`-`0x00464E2F` copies current to previous and reloads from
`0x00598B10`, which is the current/previous pair the edge-detection idiom
consumes.

**It located something static analysis could not.** A projectile pool with
stride `0x38`, consistent with 64 records over `[0x00598C00, 0x00599A00)`, is
active **only** while throwing: 0 dwords active idle, 0 walking, 38 on throw. It
carries no absolute references anywhere in the image and no global holds a
slot-aligned pointer to it, so its base is computed inline — which is precisely
why the static censuses never reached it. It is **not** the creature actor pool.

**It failed to find the berry-type selector**, and that is recorded as `KU-073`
rather than papered over. Five successive memory-diff oracles each failed for a
different reason — noise subtraction removing the target, allocation signatures
missing pooled reuse, a modal comparison swamped by stale records, one-shot
writes losing the race against the engine's per-frame rewrite, and a fingerprint
built on fields that turned out to be counters. The common cause is that **no
read-only signal distinguishes berry type**, so candidate testing had no ground
truth.

Two negatives worth keeping: record field `+0x2C` is **not** the visible colour
(all 49 occurrences rewritten and held continuously, no visual change), and
`0x0059D918`/`0x0059D928`/`0x0059D968` are **Flik Z coordinates** per
[[STRUCT-PC-FLIK-POSITION-GLOBALS]], not berry state — they were poked before
the Vault was checked for known addresses, which is the wrong order.

Cross-port structure is recorded separately in
[[XPORT-20260817-005 - Berry contact array and type marker shape]]. The PS1
contact array is 64x`0x38`, matching the PC stride and slot count measured
independently here — the strongest structural correspondence found between the
ports so far. Its `+0x2C` type byte does **not** transfer. Running score: one
structural hit, one miss.

**Session state:** the tint test left 21 sites written with `0x00000071` instead
of `0x00710000`; the engine reverted the other 28. The live session was not
returned to pristine state and a relaunch clears it. No `originals/` path, game
asset, or repository file was modified.

## 2026-08-17 agent automation tooling packet

Offline tooling packet, no runtime. The question was not a game question: how
well does this project support automated reverse-engineering investigation by
Codex/Claude, and what is missing?

**Live-session control.** The complete recipe existed only as prose in
[[PC autonomous game control]]; every arm re-derived it, and three findings
(XTEST-only delivery, ~180 ms held presses, focus-gated logic) had been
learned and then re-learned at the cost of a wrong-level arm in
`EXP-20260816-156`. It is now [[Session control plane]]: `game-session`,
`game-memory`, `send-keys`, `wait-for` over `session_lib`, with a per-session
ownership ledger recording process group, game PID with start ticks, display,
window, private sink, and the pre-existing runtime inventory. Session identity
is `(pid, process group, start ticks)`, so cleanup can refuse a recycled PID —
the check the `EXP-20260816-163` closure audit lacked when it found 32
unattributable `winedevice.exe` processes. Carousel navigation reads
`0x00599AF8` after every press and `0x00861C84` after confirming, so a dropped
press is detected and retried instead of silently selecting the wrong level.
**Fixture-validated only; nothing has run against the game.** 129 focused
regressions run against a synthetic fixture that maps the real global address
window and drives a stub `xdotool` that refuses to count a `key --window`
press as delivered.

**One correction the fixture forced.** The current and preceding position
triples are not contiguous — an unidentified dword sits at `0x0059D91C`
between `0x0059D918`+4 and `0x0059D920`. The accepted "one 24-byte
`process_vm_writev`" is therefore one call with two 12-byte vectors; a
contiguous 24-byte write would clobber that dword and misalign the second
triple. [[PC Flik teleport procedure]] is corrected (`DEC-20260817-140`).

**KU-065 resolved for its identified node.** The cause was test scaffolding,
not the product: three sites slept a fixed 120 ms before appending the anchor
line, racing the child's `LogMilestone` baseline snapshot at a measured 104 ms
median (120-164 ms under load). Fixed by waiting on the tool's own
`--status-fd` `armed` transition. Isolated-node tallies: idle 59/60 → 60/60,
12-worker load 0/20 → 20/20. `scripts/input-movie.py` unchanged.

**Context economy.** The mandated startup set measured ~272,994 estimated
tokens — larger than a 200K context window, so no agent could comply as
written. `scripts/briefing.py` produces a 4,615-token briefing with
non-elidable safety rules and loud `UNPARSED` failures; `vault-lint
--budget-only` makes the budget a metric; this note is itself the result, with
[[Current State]]'s chronology moved here verbatim (241 KB → 131 KB).

**Static export.** `ghidra-evidence.json` (7.7 MB, one line) now has a query
surface at 0.07 s per lookup, and its structural defects are recorded in
[[Ghidra export structure and caveats]]: `imports` is empty, `callers` holds
call-site rather than entry addresses (4,464 of 4,468), and the call graph
breaks at 486 thunks — so `FUN_00432930`, M5's first admitted module, appears
to have **zero** callers while `thunk_FUN_00432930` has one.

**Evidence and gates.** `run-index.py` found 14 orphaned run directories and 0
dangling citations. `experiment-draft.py` fills a note from receipts without
asserting anything. `claim-sweep.py pair` reports a tree carrying both an old
and a corrected wording as tool-negative — the exact defect that cost the
census packets repeated rounds. CI now retains raw unfiltered pytest logs as
artifacts, a pre-commit hook runs the fast gates, and `pytest.ini` stops a
bare `pytest` from following `tmp/wine-smoke-*/dosdevices/z: -> /` out of the
repository.

Canonical suite: **1,091 passed**. Vault lint: 533 notes, 0 errors. New
registers: CAP-010 through CAP-018, `KU-074`, `KU-075`, `DEC-20260817-139`
through `DEC-20260817-142`. No game, Wine, Gamescope, debugger, target write,
`originals/` access, or external PS1 evidence was involved.

### 2026-08-17 save states (same-session region checkpoint)

Follow-up within the same tooling packet, answering "can we save and reload
it". `game-memory.py snapshot`/`restore` capture and rewrite curated game-data
regions — by default the whole writable `.data` section
(`0x004C1000`–`0x00864000`), which holds every identified global and is
neither code nor stack — with a `SIGSTOP` freeze for atomicity and
same-process-only restore (PID plus start ticks), refusing a different process,
a level change, or an executable mismatch by default. It is a memory-only state
checkpoint, not a savestate: it does not survive a crash, a close, or a
relaunch, and carries no renderer/GPU/sound/thread/kernel state. Within one
session it amortizes a boot-plus-carousel across many experiment arms, which is
the `CAP-011` cost.

The durable path (CRIU) was surveyed read-only by `criu-feasibility.py` against
the live game and reported **blocked**: an open `/dev/ntsync` fd and `ntsync`
anonymous inodes — the same driver that defeats `rr` (`KU-028`) — plus a GPU
DRM fd and open X11/Wayland/PulseAudio sockets, 35 hard fds, and no
`CAP_CHECKPOINT_RESTORE`. `criu` 4.2 and the kernel flags are present, so the
blocker is the process shape, not the tooling. `DEC-20260817-143`; canonical
suite `1109 passed`; still no live run.

## Handoff entries 2026-09-28 to 2026-10-02

Moved verbatim from [[Current State#Current task handoff]] on 2026-10-12
([[2026-10-12 - Claude - Survey and prioritize next tasks]]). It was current
then; later notes supersede it where they disagree.

**Flik animation catalogue (2026-10-01, research only):**
[[PC Flik animation catalog]] maps every animation in Flik's player model:
`CHARS/FLICK.ANM` has 40 slots (39 present, 8–58 frames, 24 parts). Flik's
action state `0x0059D998` indexes a 35-row table at `0x004C1CE8` (frame script,
one or two slots, speed, idle flag). Every row now has a trigger, cited by
address: run, walk, turns, jump, the hover-dive chain, berry-throw overlays,
carrying, hurt, death, the bird, the strand swing and seven idle fidgets.
Slots 7 and 12 are unreferenced, and state `0x20` is unreachable. In
Riverbed Flight the ATTAFLIK model (4 animations) is drawn in Flik's place, and
the FLIKHARV harvester has 3. The evidence
is static ([[EXP-20261001-002 - Flik animation catalog]]); no runtime arm or
game-file change was made. Machine-readable:
`reports/animation/flik-animation-catalog.json`, regenerated by
`scripts/flik-animation-catalog.py` from `config/animation/pc-flik-animations.json`.
