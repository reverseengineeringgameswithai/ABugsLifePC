---
type: moc
updated: 2026-10-29
tags: [moc/experiments]
---

# Experiments MOC

Experiment notes live in `Vault/30-Experiments/` and use [[Experiment]]. Runtime artifacts live under `dynamic/` and must be cited by run ID.
Experiment priority and milestone exit gates live in [[Project Roadmap]]; this
MOC remains an evidence index.

Entries describe their experiment-time results and closure states. For current
source, acceptance and liveness use [[Current State#Current task handoff]] and
[[Environment Status#Current runtime handoff]]. Old “open” or “unlaunched” labels
below are historical snapshots.

## 2026-09-26 to 2026-10-18 static and runtime research

- [[EXP-20261018-013 - Options screens and the creature gate live]] — read-only hardware arms: options → "define keys" with live key table and item bytes matching the static mapping; in City Square off-screen regular enemies stay frozen, on-screen ones run (KU-070, VM gate)
- [[EXP-20261018-012 - Telescope hide flags]] — 0x00599C68–6B hide telescopes 1–4; the pickup walker is the only reader; City gate 0 hides telescope 2 (KU-067)
- [[EXP-20261018-011 - Type-indexed list table writers and readers]] — the list table 0x005C5860 is written only by the DAT walk inside the level load, after its clear; a level without type N sees slot N = 0 (KU-064); all readers listed
- [[EXP-20261018-010 - Two inert data items]] — Battle Arena primary.165 is skipped by the scene walker and singled out by no code; the RAW loader handles tags only up to 0x7F, so 0x101/0x102 are never read
- [[EXP-20261018-009 - Four-bit page palette rows]] — the 4-bit converter gives each 64×64 block its own palette row ((v/64)*4+u/64); decoding Anthill page 0 reproduces the live index buffer byte for byte
- [[EXP-20261018-008 - Direct3D render states and the depth rule]] — no SetRenderState call sets a Z state (24 constant-state calls, 15 states); Wine defaults Z on, writes on, LESSEQUAL
- [[EXP-20261018-007 - Frame wait rounding]] — the frame wait passes at 32 ms (1000/33 = 30), capping gameplay at 31.25 fps and explaining the 30.5–30.9 timer rate; Direct3D clears half-rate mode each frame; F1–F5 handling noted
- [[EXP-20261018-006 - Controls configuration screen and action bits]] — the controls screen behind `0x004D9CF9` (via Options_Scr from the level select's position 0); every input action bit labelled; Return is not rebindable (KU-070)
- [[EXP-20261018-005 - Event callbacks and registrations]] — WINDOWS creates the window and pumps messages each frame, DIRECTX wraps renderer/input/sound; only these two register in 579 saved logs (KU-071)
- [[EXP-20261018-004 - Creature type handlers and opcode-11 subroutines]] — the ten per-type handlers (event frames, buried dust, the spider's aimed shot, mosquito dash, "protect" faces Flik) and opcode 11's emerge, burrow, ring and level hooks; event sounds named (WASPBUZZ, ERUPTION, THROW01)
- [[EXP-20261018-003 - Creature VM movement modes]] — the interpreter tail read: steering, arrival, landing, chase near home, friction, leash to the previous waypoint and animation; the taxi bug's samples match
- [[EXP-20261018-002 - Creature script counter in saved runtime samples]] — saved hardware samples show Dot's and a moved taxi bug's program counters on decoded script instructions; the taxi bug walked Dot's route (KU-068)
- [[EXP-20261018-001 - Creature row index census]] — no retail creature row indexes a table out of range; seeds never run a script, regular enemies think only on screen; every walker's list exists (KU-069)
- [[EXP-20261012-007 - Unused disc content checked offline]] — COPYOFLE.RAW's early graphics located; TEST is a mermaid textured only from page 16; PLANT12's petals use the gold-berry art and its bulb plant 7's texels
- [[EXP-20261012-006 - Creature types from the character loader]] — character loader names all 41 creature types; runtime logs confirm 26; TEST is an unreferenced disc model and PLANT12 a real plant
- [[EXP-20261012-005 - Flik movement state 4 ground pound]] — movement state 4 is a hover, dive and ground pound with an 8-shot ring on landing; "gliding" was a mislabel
- [[EXP-20261012-004 - Homing target visibility bit]] — homing's required bit `0x0001` is a per-frame view-frustum bit (`0x00456640`); resolves the transplant contradiction
- [[EXP-20261012-003 - Scripted camera flag census]] — flags word `0x0059A5EE`: three setters, `0x0041B7D0` fade states; bit 0 swaps the camera source and hides the HUD during every scripted view
- [[EXP-20261012-002 - Sprite table census]] — per-level sprite lists from the `0x00467C00` dispatcher: entries `0x7B` and 4 exist in every level; entry `0x33` is absent in 8 engines
- [[EXP-20261012-001 - REA Ghidra analysis trial]] — REA's Ghidra path against the export and a raw scan: same 10 references to `0x0059A5EE`, an 11th found only by the scan; optional, not adopted
- [[EXP-20261007-001 - Local Kev evidence classification probe]] — 36 frozen PC claims, 35/36 primary, option-order and no-evidence controls; advisory research review only
- [[EXP-20261001-002 - Flik animation catalog]] — FLICK.ANM 40 slots / 35 action states at 004C1CE8; slot-record grammar fits 303 records in 60 files; sampler call-site census; variants and non-player models; static only.
- [[EXP-20260927-001 - Complete original level Blender maps]] — engine→file rule,
  all scene dispatches, pickups, creatures and starts for engines 1..16.
- [[EXP-20260926-001 - Static Anthill remaining object inventory]] — all 624 scene
  records, 218 geometry blocks, private previews and bounded import readiness.

## 2026-09 render distance, Training, capacity and memory limits

- [[EXP-20260916-011 - Terrain camera range guard for horizontal bands]] — intermittent horizontal bands traced to static/native camera-range wrap; a scoped full-camera-range guard removes the reproduced batches; tree/grass controls and 92 checked final hardware frames.
- [[PC custom distant objects]] — requirements for distant (secondary) copies of placed objects: quartered translation/scale through `00448D70`/`00449473` and the hardware quad/triangle thresholds at `0045CF37`/`004608CD`.
- [[PC custom distant terrain]] — distant-geometry requirements: visibility bytes copied at `0044BB70`, secondary traversal at `0044D430` and the shared footer terminator.

- [[EXP-20260911-016 - Training grass boundary near and distant representations]] — real collision boundary, detailed near meshes and quarter-coordinate distant representation.
- [[2026-09-11 - Codex - Confirm the solid grass boundary and distant representation]] — corrected background wording; close geometry and copied-state collision verified.

- [[EXP-20260911-015 - Training grass uses secondary background geometry]] — the observed grass strip is secondary scene 15; quarter camera translation and 152/152 live vertex matches across two views.
- [[2026-09-11 - Codex - Identify the distant Training grass layer]] — target identification corrected; build unchanged, muted runtime.

- [[EXP-20260911-014 - Training flower panorama and wall cutoff]] — decoded flower panorama, native translation/distance independence, remaining 2x wall cutoff and 13 initial-view 3D plants within range.
- [[2026-09-11 - Codex - Explain distant flowers and Training walls]] — two scoped Down taps, unchanged build and muted runtime.

- [[EXP-20260911-013 - Twofold distance and Training performance]] — shared 2x render distance (near 2304/far 3328) restores the Training corner in hardware; matched 60 s runs 31.23 versus 31.25 FPS.
- [[EXP-20260911-012 - Training corner render distance diagnosis]] — the far Training corner passes scene admission (`0044D59F`) but its polygons fail the depth test (`0045CF63`); 2x restores it in copied-state CPU replay only; implemented by EXP013.
- [[EXP-20260911-010 - Training floor occlusion and platform underside]] — original Training ground scenes 57..72 carry a type-0x41 object byte +18 depth offset of 9 that lets geometry behind show through; clearing those sixteen bytes passes bounded native and hardware checks.

- [[EXP-20260910-009 - Flik action pools and preview tail diagnosis]] — 204 two-base native cases and three shared native action voice pools; a host playback tail loss leaves the source PCM intact.
- [[EXP-20260910-008 - Replaceable Soil sign images]] — 13 native sign pictures (type `0x26`, 64×64 frames), descriptor table `005BFD70`, two-base decoder/pixel proof and a RAW-only replacement; no new live acceptance.
- [[EXP-20260910-007 - Five-throw Training sign and native defaults]] — separate initial-sign functions `0043C250`/`0043C270`; counts above six fail because `00410A20` indexes a six-frame LEVEL1.RAW resource (id `0x33`) unchecked; the limit is confirmed in live RAM and the original RAW.
- [[EXP-20260910-006 - First Soil throw count boundary proof]] — original six and adjusted 1–6 native advancement boundaries (`0043C3C0`/`0043C3CF`), two-base countdown/lesson execution and exact compare/display edits.
- [[EXP-20260910-005 - Flik event voice mappings]] — nine native Flik event bindings: grain-gate reminder radii and cooldowns, power-up and repeat proof, and a dormant City Square Super Jump request.
- [[EXP-20260909-013 - Populate original Training Blender map]] — 54 pickups, nine actors, original Soil mesh and exit overlay; native placement initialization, unchanged base objects and saved-file checks.
- [[EXP-20260909-012 - Original Training Blender mapping]] — all 278 scene records, native textures, collision/placement overlays, saved Blender geometry/UV and landmark persistence checks.

- [[EXP-20260909-005 - PC Mr Soil dialogue mechanism]] — 40 populated lesson track slots and cue table `0x004DC308`; WAV file replacement needs no executable patch; two-base tutorial/audio checks, no live-audio acceptance.
- [[EXP-20260909-004 - Restore native plant collision]] — an empty PLANTTER template blocks plant contact and activation (`00468010`); `0044CA7F` skips re-registration on an unchanged type/tag, so cached bounds persist; guarded 24-byte template restoration recovers activation, with a wall-like collision caveat.
- [[EXP-20260909-001 - Native end-of-stage marker and Blender placement]] — the original exit leaf sign is scene 82 with dispatch `0x19`; no dedicated collider found; its renderer reads the stored camera at `005BDB9C`.
- [[EXP-20260908-021 - Native collectibles and Blender placement]] — native pickup table (70 rows, stride 16), `00456A90` height presets (literal XYZ unsafe), `00417720` pickup gate and token bounds; live pickup initialization and grain checks.
- [[EXP-20260908-020 - Native enemy placement and scattered Blender population]] — type-35 actor table (64 records of 28 bytes copied to `00599EB0`), type-to-model binding through `00445020`, native 169-packet comparison and live enemy accounting.
- [[EXP-20260908-016 - Manual seed ownership and native scattering]] — actual manual cold-seed owners and return/pickup pass; native fixed-slot and repulsion hazards isolated; diagnostic closed, live actor release still open.
- [[EXP-20260908-014 - Manual moved-seed page persistence]] — full 20-plant growth admission and moved-seed terrain-retire/return pass; both diagnostics closed; actual actor/item storage lifecycle remains open.
- [[EXP-20260908-013 - Seed auxiliary budget and distant carry]] — two-call native seed budget; selected distant contact 1/64 carry passes; passing unpatched positive control retained; general Milestone 4 gates remain open.
- [[EXP-20260908-012 - High-slot seed interaction and native pool limit]] — selected contact 2/64 seed interaction passes; original 64-entry pool-full cycle confirmed; 310 broader numeric candidates remain.

- [[PC terrain streaming ownership ledger]] — covered owners, release boundaries and remaining lifetime gates.
- [[EXP-20260908-006 - Native actor and camera contact repair]] — 66 native contacts separate 64 actors/camera, exact native response and bounded hardware crowd checks; selected high-slot interaction subsequently passes in EXP012.
- [[EXP-20260908-005 - Compact terrain storage and actor selector limits]] — compact native files, 1,750 exact movement calls, 36 persistent CPU-renderer frames; native actor-selector limit identified (`0x0041C420`); live Milestone 4 gates remain open.
- [[EXP-20260908-004 - Native terrain page residency]] — 24 native contact slots, 1750 exact movement steps and 24 query comparisons with actual offline page retirement/reload; live integration and persistence remain open.
- [[EXP-20260908-001 - Plant capacity and collision workspace repair]] — native full-pool and candidate-overwrite reproductions; finite executable repairs; Milestone 3 was open at this checkpoint.
- [[EXP-20260907-028 - Representative update and render headroom]] — native frame structure (update before render/present) and paired repeated-route QPC headroom with one native mushroom interaction; historical checkpoint.
- [[EXP-20260907-027 - Native respawn cycles and exit-aware traversal]] — six native resets, two complete four-section loops and paired exit/re-entry; rejected GameOver fixture preserved; historical stage 3 checkpoint.
- [[EXP-20260907-026 - Collision-preserving visual density and frame work]] — native support transition traced; bounded visual density retains exact collision, native routes pass; frame-work sampling added; historical stage 3 checkpoint.
- [[EXP-20260907-025 - Native density limits and terrain refinement trial]] — 5462 vertices per mesh (16-bit byte offsets), unchecked collision collector at `0x007F3F50`; rejected slope refinements; source/native/live evidence are separate.
- [[EXP-20260907-023 - Dedicated asset arena and terrain chunk acceptance]] — native asset load cursor base `0x0063E998` and load region bounded by `0x0076F998`; a dedicated 8 MiB region passes a native 170-model comparison and three hardware arms; earlier four-chunk layout OPEN.
- [[PC Large-Level Engine Roadmap]] — milestone record of the native limits measured while testing larger levels (actor slot 16 and the camera, the 20-plant scan, 400-entry collision lists); resident stages accepted, streaming paused.
- [[EXP-20260907-022 - Terrain chunk prototype and model stream freeze]] — four-chunk prototype; source/native seams pass; the live trial freezes on the MOS.ALL stream and renderer scratch overlap.
- [[PC level authoring memory limits]] — measured native memory limits: retained storage overrunning renderer scratch `0076F9A0`, the shared pool at `00598CA8`, the 20-plant scan and 400-entry candidate lists.
- [[EXP-20260907-017 - Trunk scenery and character storage overlap repair]] — an oversized level shifts Flik's body polygon stream into renderer scratch `0076F9A0`, which native stores overwrite; shared mesh storage repairs the overlap.
- [[EXP-20260907-014 - Cliff seam and phantom seed collision repair]] — the actor-contact broad phase at `0x0041CA3A` sums squared deltas in 32 bits, so extreme seed coordinates wrap into a false contact; guarded arithmetic passes native regressions and a bounded live observation.
- [[EXP-20260907-010 - General render distance preview]] — 1.5× terrain/scenery distance (1152/1664 to 1728/2496) through executable immediates; native initializer and primary-frame arms stay within batch 498 of 500 and index capacities 1000/4800; far also affects secondary admission in `0x0044D430`. [[PC general render distance]].
- [[EXP-20260907-009 - Mushroom render distance diagnosis]] — eight short taps, 336 native cases and seven clip traces; sampled pop-in is polygon depth rejection.
- [[EXP-20260906-014 - Net-new scenery mushroom instances]] — original scaled mushroom localization, additive slots, native landing/lateral/grounded/draw controls and preserved ground-interference counterexample; candidate offline.
- [[EXP-20260906-011 - Expanded corner visibility regression]] — ground/grass vanish at the far-east corner while sampled floor support remains; the original-PC horizontal cull explains it; bound 14183 admits all 142 observed cameras offline.
- [[EXP-20260906-007 - Plant-state collision regression]] — confirmed type 5/source 8 mushroom template loss; a minimal two-byte repair restores native/live exclusion and bounce.

## 2026-09-04/05 Level01 collision, depth and shared-floor tests

- [[EXP-20260905-004 - Playable ramp and box area]]: deck/top plus gentle ramp and matching sides; six paired PC-model routes, two live normal-input cycles, jump/landing and step-off; 118 terrain tests pass; no R2q.
- [[2026-09-05 1804 - Codex - Playable ramp and box area]]: rebuild instructions, evidence and runtime handoff.

- [[EXP-20260905-003 - Shared floor return discriminator and stitched patch]]: 68-cell boundary census, complete mesh groups/duplicate vertices, original-PC return discriminator, six-cell connected patch and normal-input runtime comparison. Isolated floor 16/16; complete scene 13/16 with unchanged prop confounds; two live return cycles pass, separate source100 extension blocked.
- [[2026-09-05 1659 - Codex - Shared floor return and stitched patch]]: audit visibility correction, final validation and preservation record.

- [[EXP-20260905-002 - Box movement and occluding-view validation]] — five
  finite sweeps, 518 grounded samples/107 captures; new paused edge has no
  reconstructed top-depth inversion. Failed south navigation retained; guarded
  stationary retry passes. Both test arms closed; shared-floor task next.

- [[EXP-20260905-001 - Box top diagonal live comparison]] — four authorized
  writes; six fragments disappear/return with alternate/control, all 255 prior
  fixes retained, 15 matched-state captures; both controls and original mesh
  restored exactly. EXP-002 supplies the subsequent finite movement/view result;
  universal coverage remains open.

- [[EXP-20260904-011 - Box top diagonal edge discriminator]] — alternate
  diagonals on identical finer-box vertices/collision win all prior analytic
  samples offline; its prepared plan is subsequently verified in EXP-20260905-001.

- [[EXP-20260904-010 - Paused subdivision live comparison]] — authorized same-pose
  mesh swap/restoration removes255 predicted fragments;9 matched-state captures,
  exact ROI restoration; 6 boundary samples remained for EXP-011/EXP-001.

- [[EXP-20260904-009 - Paused side-view depth interpolation]] — preserved paused
  side-view residual; original renderer depth comparison supports large-face
  error; its finer candidate is subsequently compared live in EXP-010.

- [[EXP-20260904-008 - Block depth offset runtime comparison]] — inherited object setting causes
  the demonstrated leak; one-byte removal/restoration with matching camera,
  smaller-face control and 197 focused tests.

- [[EXP-20260904-007 - Deck visibility and inherited depth offset]] — confirmed block contact,
  lower-deck occlusion defect and inherited render-depth field; its candidate
  is subsequently verified in EXP-008.

- [[EXP-20260904-006 - Flat deck and solid block test]] — clearer isolated testbed after the
  EXP-005 return-fall report; original top/side controls and repeated live
  jump/off/return tests. Shared-edge repair remains open.

- [[EXP-20260904-005 - Raised floor and visible ground pairing]] — six-cell raised floor, live jump/walk,
  matched-camera visible-ground intervention and restored control; boundary
  stitching remains open. [[PC floor translation prototype]].

- [[EXP-20260904-004 - Translated barrier live collision proof]] — first live
  authored-barrier response, exact loaded-payload verification, restored-file
  walking control and bounded translation prototype, reused by EXP-005.

- [[EXP-20260904-003 - Barrier grammar and landing-seeded grounded movement]] —
  barrier reader over18 files,108 original collection comparisons and grounded
  obstacle controls seeded by original landing; reuses EXP-002 unchanged.

- [[EXP-20260904-002 - Retail collision admission and separate XZ barriers]] —
  two original loading/bucket cases and22 controlled movement cases; real
  triangles and separate X/Z barriers cause distinct offline responses.

## 2026-09-04 original-instruction collision experiments

- [[EXP-20260904-001 - Original PC lateral collision and descriptor-store probes]] —
  synthetic vertical walls and direct render-side descriptor stores, no game launch.

## 2026-08-19/20 R2b–R2o Anthill static-mesh runtime

- [[EXP-20260820-004 - R2o completed-present state calibration protocol]] — D1 runs rejected on owned-task census drift; R2o retries stopped and [[EXP-20260820-005 - R2p task lifecycle diagnostic]] became the active pickup.
- [[EXP-20260820-003 - R2n PC state-equivalence read candidates]] — six exact equality ranges and two completion PCs bounded; renderer scratch excluded.
- [[EXP-20260820-002 - R2m offline cross-time correspondence diagnostic]] — no unique fixed lag; wall-clock alignment is nonviable.
- [[EXP-20260820-001 - R2l fresh replicated face8 localizer]] — valid C1/L1/L2/C2 run; inconclusive because L1 and L2 did not replicate outside the fixed mask.
- [[EXP-20260819-009 - R2k Anthill D4 control-trained mask holdout]] — accepted finite D4 holdout; zero outside-mask observations.
- [[EXP-20260819-008 - R2j Anthill control-trained successor mask]] — 93445-pixel mask proposed from C1/C2 alone; fresh D4 holdout required.
- [[EXP-20260819-007 - R2i Anthill replicated face-8 localizer]] — procedurally complete; inconclusive (control nuisance escaped the frozen mask and the localizer effect did not replicate).
- [[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] — accepted finite-grid D3 holdout; zero observations outside the frozen combined mask.
- [[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] — rejected: D2 had 233 observations outside D1's mask; no mask published.
- [[EXP-20260819-004 - R2e Anthill stable-background calibration]] — rejected on the full-frame F0 gate; superseded by EXP-005.
- [[EXP-20260819-003 - R2d Anthill sampled phase calibration]] — rejected on lower-right crop drift; cycle model superseded by EXP-004.
- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]] — valid C1/L/C2 run with a rejected comparator; face-8 localization causally inconclusive.
- [[EXP-20260819-001 - R2b Anthill static mesh causal runtime]] — type-0x41 vertex edit under A1/B/A2; the control-agreement gate failed (108 of 307200 pixels), so inconclusive.

## 2026-08-18 static-mesh authoring

- [[EXP-20260818-008 - R2a Anthill static mesh causal candidate]]
- [[EXP-20260818-007 - R1 static mesh consumer, round trip, and causal candidate]]
- [[EXP-20260818-006 - R0 the static mesh format and where visible ground lives]]

## 2026-08-17/18 runtime tooling and flight recorder

- [[EXP-20260818-005 - Decode the render-geometry command grammar (scope)]] — walker is a type-switch, not an opcode table; type-3 container grammar from instructions; type-3 is a billboard batch, so R0 (EXP-006) took over the visible-ground question; Gate C not run.
- [[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]] — four authorized pokes confirm the causal equipped-berry selector and its value→colour map (KU-073).
- [[EXP-20260818-003 - Runtime reset and grain-gate captures with the flight recorder]] — grain count 0x0059D9B1 and gate-flag writers confirmed; Cliffside is not type-1 (KU-063); Tunnels value chains lost to truncation.
- [[EXP-20260818-002 - Flight-recorder Phase 0 write-trace]] — emulator-side C write-trace reproduces writer 0x004ab889 reliably and reveals the full writer set.
- [[EXP-20260818-001 - Watchpoint path and first forensic tuple for Flik position]] — 86Box GDB-stub write-watchpoint yields one forensic tuple for 0x0059D910 (writer 0x004ab889); the stub is too fragile for continuous capture.
- [[EXP-20260817-188 - Live game-memory read save restore validation]] — game-memory state/peek/snapshot/restore verified against the running retail game, with one authorized, reverted position write.

## 2026-08-16 subsystem coverage

- [[EXP-20260817-187 - Runtime berry throw reconnaissance]] - runtime: throw
  bit `0x8000` confirmed; throw-exclusive stride-`0x38` projectile pool located;
  berry-type selector not found (`KU-073`)
- [[EXP-20260817-186 - M5 third-module candidacy ranking]] - selects the input
  action-bit resolver; rejects the creature VM on the bounded-contract criterion
- [[EXP-20260817-185 - PC event subsystem static census]] - fourth
  coverage-driven packet and the last row of the recorded
  Actors/AI → Input → Event/scripting preference. Offline census of the
  16-slot event table `[0x005982B0, 0x00598670)` (stride `0x3C`), its
  three-callback record layout, the register/dispatch/destroy-all entry points,
  the four with no reachable caller, and the two static records the executable
  registers. Answers the row's question with a clean negative on both halves:
  **no VM and no trigger stream** — a callback registry — and **disjoint** from
  the creature scripts, tested by address intersection both ways. Closes the
  audio census's open caller question: `0x0042BA60` is the `"DIRECTX"` event's
  create callback. Event/scripting moves Touched → Bounded; `KU-071` opens.
  Worker-complete, pending fresh James audit.

- [[EXP-20260817-184 - Third independent input census audit]] - **ACCEPT** at
  `52a9024` with **zero defects**, closing the input packet. Every numeric and
  completeness claim recomputed from the binary, and all 140 cited `.text`
  addresses checked to be real instruction starts. The new block-A caveat
  verified independently. Two claims confirmed beyond their stated scope
  (`0x00598BC8` and `0x00598B1C` each have exactly two writers image-wide).
  Input stands at Bounded.

- [[EXP-20260817-183 - Second independent input census audit]] - **REJECT** at
  `afee530` on two address-level claims: a cited instruction address
  (`0x0042F38E`) that does not exist, and a "not read here" negative for
  `0x00598B14` falsified twice inside the stated extent and contradicted by the
  same document. Both were introduced or left by the previous correction pass.
  The whole §3.1 writer census reproduced under an independent byte-level scan
  — 62 occurrences, 46 stores, no hidden writer — as did both extents and the
  §0 novelty negative. Adds a scoping caveat: block A's reachability is
  unestablished, so remappability rests on block B.

- [[EXP-20260817-182 - Independent input census audit]] - **REJECT** of
  EXP-181 at `67ca1b5`, with all findings applied in the same commit. The
  identifier layer, both function extents, the direction tables, the dead-thunk
  claim and the §0 novelty negative (0 hits for ten addresses across 504 notes
  and 43 exports of the parent tree) all reproduced exactly. The gating defect: the binding-table
  writer census was false — 22 further stores apply a `0x18`-stride config
  array at `0x004D9CF9`, with an inverse copy-back and a defaults/apply
  dispatcher, so **the controls are configurable**. Five smaller defects,
  including a wrong `DIEDFL_*` constant and a `DIJOYSTATE` button index that is
  Confirmed rather than Inferred.

- [[EXP-20260817-181 - PC input subsystem static census]] - third
  coverage-driven packet and the second row of the recorded
  Actors/AI → Input → Event/scripting preference. Offline census of the
  DirectInput bring-up `0x0042F350` (keyboard at `GUID_SysKeyboard`/
  `c_dfDIKeyboard` non-exclusive, joysticks promoted to
  `IID_IDirectInputDevice2A` at `c_dfDIJoystick` exclusive), the per-frame read
  `0x0042EBC0`, the runtime-written binding table `[0x004D8430,0x004D8490)`,
  and the four-direction analog synthesis. Finds `GetAsyncKeyState`'s import
  thunk **dead** — the import is reached only by a register load — and the two
  input paths disjoint. Input moves Touched → Bounded; `KU-070` opens.
  Worker-complete, pending fresh James audit.

- [[EXP-20260817-180 - Eighth independent creature census audit]] - **ACCEPT**
  at `2cb6b07` with **zero defects**, closing the creature-census chain. Every
  number re-derived an eighth time, including that all 69 branch targets land
  inside their own script and that reachability shows zero stored pointers to
  any of the five functions. The prior-art accounting is honest in both
  directions. One new binary fact arrived as a minor: an eighth mode-slot
  writer at `0x0041E2E9`, reachable only by `esp`-delta accounting and
  corroborated by `ghidra-evidence.json`. Enemies/actors/AI stands at Bounded,
  Event/scripting at Touched.

- [[EXP-20260817-179 - Seventh independent creature census audit]] - **REJECT**
  at `f13da89`, on the packet's description of its own audit history only.
  Every number reproduced a seventh time — all 69 branch targets land inside
  their own script, `+0x5C` is exactly 21 sites, `+0x40` exactly ten stores —
  and the prior-art accounting passed a second time. The Audit history is now a
  per-round fact table making no global claim about whether findings landed,
  because three successive drafts made such a claim and each was falsified.

- [[EXP-20260817-178 - Sixth independent creature census audit]] - **REJECT**
  at `2ceef9c`, on bookkeeping only. Every number reproduced a sixth time and
  the prior-art/novelty accounting passed for the first time. The two defects
  are in the machinery the fifth round built: a wrong round count inside the
  sentence claiming the rule list carries no count, and an Audit history that
  omitted the fifth audit while asserting all findings applied.

- [[EXP-20260817-177 - Fifth independent creature census audit]] - **REJECT**
  at `a540dc7`. Every number reproduced a fifth time and all six quoted
  disassembly blocks are byte-exact. The rejection is that a correction
  declared applied had not landed: the previous round's flagship defect was
  reported fixed while the edit re-anchored only half the sentence, and two
  minors were likewise declared applied and were not. Plus four counting and
  attribution defects. Rejection counts are now removed from the MOCs in favour
  of the packet's Audit history so they cannot go stale again.

- [[EXP-20260817-176 - Fourth independent creature census audit]] - **REJECT**
  at `1c499bf`, on the accounting layer alone. Numeric core reproduced a fourth
  time; the extent `0x0041DC60`-`0x0041E845` verified with nothing extending
  further; four `+0x70` writers confirmed as exactly four; the flag enumeration
  complete; the nine-artifact prior-art list verified line by line; and all six
  quoted disassembly blocks byte-exact for the first time. Nine defects, all
  arithmetic/counting/attribution — including a wrong percentage, an
  unreproducible "thirteen sites", the third draft's errors blamed on the
  second, and an understatement of what `ghidra-evidence.json` contains.

- [[EXP-20260817-175 - Third independent creature census audit]] - **REJECT**
  at `3f0debd`. Numeric analysis reproduced in full a third time, published
  reproduction snippet run verbatim. `0x0041DC60` does not end at its only
  `ret` — `0x0041E7D4`-`0x0041E845` is entered from inside it and jumps back —
  so the extent was wrong packet-wide and a fourth `+0x70` writer at
  `0x0041E7FE` was missed; the flag table also missed a bit-`0x20` test in its
  own scope. The prior-art list named a file with no occurrence of the pool
  base and omitted one publishing the extent arithmetic verbatim, and the
  generated `ghidra-evidence.json` already decompiled the interpreter, so the
  address-based novelty claim is withdrawn. Both row promotions survive.

- [[EXP-20260817-174 - Second independent creature census audit]] - **REJECT**
  of the corrected EXP-172 at `47d447f`. The analysis reproduced in full for
  the second time and every first-audit correction verified. Root cause: the
  census had read `0x0041DC60` only to `0x0041E1A8` while making completeness
  claims over the whole of it (its extent was later established as
  `0x0041DC60`-`0x0041E845`) — the unread tail held a
  flag test refuting a Confirmed cell, four more tested bits, two further
  `+0x70` writers, and the `call eax` at `0x0041E7C7` reaching the ten
  per-type handlers. Separately the headline novelty was prior art in
  `M2-plant-request-origin-static-trace.md`, uncited by either draft; eight
  exports touch the pool, not three. Fourth unbounded index found; both row
  promotions survive.

- [[EXP-20260816-173 - Independent creature census audit]] - **REJECT** of
  EXP-172 with all findings applied in the same commit. The analysis was
  reproduced in full and independently: 463 instructions, zero misalignment,
  69 branch targets on boundaries, identical histogram, both switch tables,
  every caller. Seven register/attribution defects, chiefly a per-type claim
  false for 27 of 36 types, a "range check" attributed to a handler that has
  none, a miscounted string set under a row promotion, a 380-vs-197 drift, and
  an under-credited M2 export. Found a third unbounded index; both row
  promotions survive.

- [[EXP-20260816-172 - PC creature actor pool and behaviour VM census]] -
  worker packet, **rejected and corrected through every audit above**. First
  packet on the recorded
  Actors/AI → Input → Event/scripting preference and the first to open a row
  with no import surface. The 64-slot pool `[0x0059B628, 0x0059D728)` is bound
  one-to-one to the `LOAD: Type 35, CreatListRam.` records at `0x00599EB0`, and
  a resumable word-code interpreter `0x0041DC60` runs 40 shipped programs with
  the program counter in slot `+0x70`. The instruction-size model is validated
  four independent ways. Enemies/actors/AI → Bounded, Event/scripting →
  Touched; `KU-068` keeps every runtime claim closed and `KU-069` records four
  unbounded table indexes.

- [[EXP-20260816-165 - Independent PC view-chain correction audit]] -
  **ACCEPT** at exact clean subject `0336d14`. Independently reproduces the
  source/selector/view-matrix/renderer join, local transform, exact caller and
  terrain counts, corrected viewport/TL-vertex boundaries, XPORT discipline,
  and the Bounded-not-Mapped Camera disposition.

- [[EXP-20260816-164 - PC view-chain correction and coverage reclassification]]
  - accepted correction of EXP-162's single packet.
  Native evidence now joins the flag-selected source copy through common block
  `0x00599C90` and `0x00455710` directly to matrix `0x005B58E0`, renderer load
  `0x0044D4C1 -> 0x004636C0`, and the local builder transform. Live viewport,
  TL-vertex, caller, terrain-count, XPORT, and coverage claims are corrected.
  EXP-165 accepts the exact clean worker commit, so Camera is Bounded while
  source semantics, controls, frequency, and visual causality remain open.

- [[EXP-20260816-163 - KU-065 canonical-suite reproduction follow-up]] - the
  original one-test failure does **not** reproduce: 13/13 canonical full
  suites, 100/100 complete manifest modules, and 200/200 focused system-state
  runs pass with direct raw logs. A constrained nine-failure run exposes a
  `15 -> 14` descriptor-count candidate in one receipt cleanup test, but does
  not identify the original. KU-065 stays open and suite gates stay qualified.

- [[EXP-20260816-162 - Independent camera reconnaissance audit]] - **REJECT**
  of EXP-161 at `02946af`. D3DApp, known TL vertices, the seven terrain calls,
  PS1 separation, and manual-control caution survive. The viewport endpoints
  are operand bytes; `0x00405FE0` performs the transform rather than receiving
  it upstream; `0x0045A7F0` is not its caller; and a PC-native two-source
  position/orientation selector feeds `0x00455710` and the render-consumed
  view matrix. Its exactly one offline correction is EXP-164; EXP-165 accepts
  that clean worker commit and authorizes Camera = Bounded.

- [[EXP-20260816-161 - PC camera static reconnaissance]] - **partial worker
  result rejected by EXP-162**. Its no-string/import observation and surviving
  anchors remain historical evidence, but the Untouched-row conclusion,
  upstream-transform placement, `0x0045A7F0` attribution, viewport locators,
  and rejected terrain-count propagation are not live claims. PS1 camera notes remain
  hypotheses in [[XPORT-20260816-004 - Camera system shape]], never PC
  confirmation.

- [[EXP-20260816-160 - Independent audio census audit]] - **REJECT** of
  EXP-159 with the corrections applied in the same commit. Anchors and most
  counts survived; six Confirmed claims did not, including two counts, a
  registration reading of an `UnregisterClassA` cleanup site, and a "music"
  label contradicted by the note's own Inferred section. Material miss: the
  census's central initializer `0x0042BA60` is dispatched from a `.data`
  pointer record, not a call. Audio stays Bounded.

- [[EXP-20260816-159 - PC audio subsystem static census]] - the first packet
  chosen from [[Subsystem Coverage Map]] rather than from milestone momentum.
  Offline census of the PC audio subsystem: DirectSound bring-up `0x004A3480`,
  the `0x00596528` music track table and its builder `0x0042BB90`, the
  `DSStream` window class, and the `0x004AD000`-`0x004ADB20` RIFF cluster.
  Moves the audio row from Untouched to Bounded and adds a missing Input row.
  Records that this executable reaches both imports and its own functions
  through `jmp` thunks, so naive cross-reference searches find nothing.

## 2026-08-16 M5 selective reimplementation

- [[EXP-20260816-171 - Independent M5.8 grain-gate resolver audits]] - final
  **ACCEPT** at exact clean `dfd3af3`, tree `8b7d423`, after the first audit
  rejected `efad1c2` for duplicate-key acceptance only. Independent literal
  and escaped top/gate/record attacks, valid stdin/path identity, 38/38,
  64/64, KU-065-qualified 686/686, exact delta/hash, lifecycle, and scope gates
  pass; no corrective packet remains

- [[EXP-20260816-170 - M5.7 grain-gate opening resolver]] - independently
  accepted worker/correction history. The first audit
  **REJECTED** exact `efad1c2` only because default JSON parsing accepted
  duplicate keys despite the strict contract; nested/top-level rejection and
  named-path regressions correct that defect without changing resolver logic.
  Implements native-order Tunnels/City
  opening decisions with wrapping signed arithmetic, ordered coupling, City
  index-0 `0x00599C69` address write, separate downstream metadata, and strict
  asset-free reporting. Thirty-eight new / 64 combined fixtures reproduce all
  usable retained receipts without inventing row-1 or row-4 runtime evidence;
  it also retains a KU-065 failure, 15/20 isolated node pass rate, a qualified
  682/682 first-worker retry, and qualified 686/686 correction/audit gates

- [[EXP-20260816-169 - Independent M5.6.1 delta audits]] - first path-bounded
  audit rejects `45cc15b` for one absolute `Grain gates`/`no` table left after
  the prose correction; exact one-file `dd034c9` scopes it to Confirmed
  direct/static families and `none found`; second fresh audit **ACCEPTS** that
  clean commit and activates M5.7
- [[EXP-20260816-168 - M5.6.1 claim and contract correction]] - exact
  documentation/evidence repair after EXP-167; City index-0 direct byte write,
  one-row type-1 expression, first-failed-criterion wording, direct-reference
  scope, KU-065 recurrence, and durable logs only; independently accepted by
  EXP-169 after one residual table-scope correction
- [[EXP-20260816-167 - Independent M5.6 hard-truth audit]] - **REJECT** at
  exact clean subject `3504f6a`; retains the grain resolver's core arithmetic
  and receipts but rejects the omitted City direct write, false two-row type-1
  description, unsupported single-criterion statement, and global-exclusivity
  promotion. Also observes a new unretained `1 failed, 647 passed` KU-065 node
- [[EXP-20260816-166 - M5 second-module entry-gate audit]] - offline worker
  proposal for the pure Tunnels/City grain-gate opening resolver; rejected by
  EXP-167, corrected in M5.6.1, and finally accepted at `dd034c9` by EXP-169
  before any implementation

- [[EXP-20260816-158 - Independent M5.5 and M5.5.1 delta audits]] - **REJECT**
  at `cdef7c7` for one residual live site (the standoffs tool still published
  the superseded settle band in its emitted JSON), then **ACCEPT** at
  `f0ea760`. Closes the M5.1→M5.5.1 chain: all four M5 exit gates hold for the
  type-1 module at its Level03 boundary. One non-gating count erratum folded
  into the banking commit.

- [[EXP-20260816-156 - M5.4 predictive reset placement receipt]] - the
  prediction was committed before any launch and then confirmed exactly: a
  `+256` edit to row 6's Z moved the engine's reset placement to
  `(501696, 31768, 502208)`, all three components matching, including a
  terrain-recomputed Y `+1676` from the control that no shift of the edited
  field could produce.
- [[EXP-20260816-157 - Independent M5.4 hard-truth audit]] - **REJECT**
  narrowly: pre-registration integrity, the prediction, the observation, the
  write boundary, and the gate-4 scoping all survive, but a "7 seconds"
  no-loop window is unretained (the trace ends at 2.47 s) and the widened
  settle band was left contradicted by the shipped tool. Corrective packet
  M5.5 applied.

- [[EXP-20260816-155 - Independent M5.3 delta re-audit]] - **ACCEPT** of the
  M5.3 correction: corrected numbers at every live site, new test pins matching
  values derived before the commit existed, all six retention statements
  bounded in both directions, and a module diff of exactly three lines. Adds
  the convergent-prologue evidence that strengthens `KU-064`, and one
  attribution correction. Three of four M5 exit gates supported at the module
  boundary; M5.4 is the packet for the fourth.

- [[EXP-20260816-154 - Independent M5.1 hard-truth audit]] - fresh-context
  adversarial audit of EXP-153. **REJECT**: the module's behavior survives a
  264,232-trial differential against an independently written
  instruction-level simulator, a 200,000-sample mod-4 attack, all four
  receipts, and the census, but two Confirmed-labelled numbers do not
  reproduce (`39,619`/`284,005` versus true `39,316`/`303,653`) and a
  four-fold retention claim is uncited and contradicted by the pointer-table
  clear at `0x00467207`. Corrective packet M5.3 applied in place.

- [[EXP-20260816-153 - M5 entry gate and type-1 reset placement resolver]] -
  audits candidate modules against the six M5 entry-gate criteria, admits the
  type-1 reset-placement selector, and reimplements `0x00432930` engine-exactly
  in `reimplementation/ablpc/type1_reset.py` plus read-only
  `scripts/type1-reset.py`. Reproduces both natural EXP-129 pit falls, the
  exact EXP-130 walkable fixed point, and the EXP-116/117 `+4096` delta, with
  an unplanned terrain-descriptor 543 agreement. New: negative record types
  alias into the same loader pointer slot, a zero row count reaches an
  uninitialised index, and Level03's 18 rows pair one-to-one with the nine
  grain gates. This was the worker boundary; the later M5.1→M5.5.1 chain is
  independently closed by EXP-158.

## 2026-08-16 runtime gate mapping

- [[EXP-20260816-149 - Independent modified-threshold completion audit]] -
  fresh-context hard-truth audit of EXP-148. **ACCEPT**: the modified build's
  Tunnels requirements read `1..9` and the City lookup `1,2,3`; the open
  semantics match the disassembly (Tunnels `0x1068`->`0x0690` in `0x00432B30`,
  City state `-1`->`0` with `0x0059F030` animation in `0x00433790`, call-site
  slots gate0->2/3, gate1->4/5, gate2->0/1); the rows-0/4 coupling
  (`0x00432F85`/`0x00432F9D`) is unconditional so row 4 is correctly not
  claimed as independently separable; the row-1 "opens above requirement" gap
  is honestly disclosed; the `gate_probe.c` boundary is one 24-byte teleport
  plus a guarded one-byte grain write at `0x0059D9B1`; the five screenshots are
  640x480 hardware frames matching their grain HUD; hygiene clean (610 tests,
  Vault 428/0/0, tracked audit 0)
- [[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]] -
  closes KU-060: on the modified `(1..9)/(1,2,3)` profile, ten of twelve gates
  show the exact closed-at-(min-1)/open-at-(min) transition, row 1 opens above
  its requirement, and the row-0/4 coupling is directly demonstrated; City
  animation slots match EXP-139's static prediction. Records that the game
  advances logic only while the window is focused
- [[EXP-20260816-147 - Independent level-analysis audit]] - fresh-context
  hard-truth audit of EXP-146 and [[PC level roster and numbering]]. Original
  **REJECT** for one isolated defect: the roster note cited the carousel
  position counter as `word [0x00059AF8]`, but the consumer at `0x00414766`
  reads `word [0x00599AF8]` (`0x00059AF8` is below the image base and
  unmapped); the worker corrected all three occurrences to `0x00599AF8` (and
  the propagated session-note copy), so the final disposition is **ACCEPT**.
  All other originally reviewed claims verified at the time: the 22-reference grain-byte census
  and gate classification, the 17-entry dispatcher routing (only L3→`0x00432B30`,
  L4→`0x00433900`→`0x00433790`), the gate-structure L3/L4 binding, the
  `0x004C6A30` roster table values, the progression→internal-index mapping
  (City Entrance = progression 7 = internal 4, training = 17, internal 16 the
  sole non-carousel slot), the direction argument, and the caveats; hygiene
  clean (610 tests, Vault 424/0/0). EXP-167 later narrows the exclusivity
  conclusion to direct/static references; indirect/cached absence was not
  proved. Original fix: `0x00059AF8` → `0x00599AF8`
- [[EXP-20260816-146 - Grain-gate level exclusivity static proof]] - complete
  census of 22 direct/static grain-byte references: only two are positional
  gate-vs-requirement comparisons, the dispatcher and known structures bind
  them to internal levels 3/4, and global absence of indirect/aliased/cached
  gate families remains Inferred after EXP-167's scope correction
- [[EXP-20260816-144 - Runtime grain-gate visual mapping]] - write-assisted
  teleport pass over the EXP-141 standoffs correlates all twelve visible
  gates to their mechanisms (nine Tunnels wooden-pole rows 0–8, three City
  leaf/pillar indices 0–2), each with `NextLife=0` and the engine-exact
  nearest-gate check, confirming every standoff walkable; establishes the
  autonomous XTEST/hardware/carousel control recipe in
  [[PC autonomous game control]]
- [[EXP-20260816-145 - Independent runtime gate mapping audit]] - fresh-context
  hard-truth audit of EXP-144. Original **REJECT** for one isolated defect
  (City gate 0/1 "nearest dist²" used truncation instead of the engine
  `sar`-8 helper `0x00416580`, and mixed the gate-2 reference); the worker
  corrected the City table to engine `sar`-8 from the settled current
  (`3482`/`9216`/`11885`), so the final disposition is **ACCEPT**. Standoff
  agreement, Tunnels distances, inside/outside verdicts, screenshots,
  control-recipe disassembly, write boundary, and hygiene all verified

## 2026-08-16 automatic Direct3D startup audit

- [[EXP-20260816-152 - Independent launcher auto-hardware flag audit]] -
  fresh-context James ACCEPT of the launcher change at HEAD `727b37b` adding an
  opt-in `--auto-hardware` flag to `scripts/play-pristine.sh` (a pinned M4
  machine authority): the M4-checked structure (one `COMMAND` block with `-w 640
  -h 480` / `-S fit -F "$FILTER"`, the exact game-dir guard, one verbatim
  unindented renderer echo) and every M4 v0.2 semantic claim are preserved, with
  only the launcher byte pin re-pinned (`68c91717…`->`6ca3c657…`, equals the new
  `sha256sum`); wiring hash-gates the retail source, builds/reuses the
  `1e1d5099…` cache and runs it from the retail cwd (plain launch still `wine
  ./bugs.exe`); 13 launcher/mod tests, no falsified history, `make check` green
  (623 tests, Vault lint 435/0, 5 M4 anchors, tracked audit 0)
- [[EXP-20260816-151 - Independent auto-hardware runtime audit]] - fresh-context
  James ratchet accepting EXP-150 at the derived build hash `1e1d5099…c41f`:
  independently reproduced the guarded builder (9 changed bytes, exact inverse,
  9 tests), the patched disassembly (`mov [esp+0x10],ebp` / `jmp 0x004A7A56`
  displacement `0x1E2`, `0x004A7A56` surface-release cleanup) and the
  HIGHLOW→ABSOLUTE relocation neutralization, and audited both retained logs
  (all six markers + `Device has hardware acceleration`, no reject markers) and
  the full-frame carousel/gameplay screenshots without relaunching; records one
  narrowing (host-GPU `RTX 5090` identity is asserted, not carried by the two
  retained `bugs.log` files) and confirms no premature candidate/START HERE
  promotion
- [[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]] - builds
  the EXP-143 paired transform (`make-auto-hardware`, output
  `1e1d5099…c41f`, 9 focused tests, exact inverse) and runtime-validates it:
  two fresh restarts boot straight into hardware Direct3D (all six markers +
  `Device has hardware acceleration`, host NVIDIA GPU) with no chooser input
  and no visible chooser, rendering playable gameplay; retail identity and
  reversibility preserved. Pending a fresh James ratchet before promoting the
  candidate note
- [[EXP-20260816-143 - Automatic Direct3D startup static audit]] - proves no
  native renderer argument in either command-line parser; rejects the unsafe
  whole-chooser bypass; and records the independently reviewed paired
  code/relocation candidate, its exact bytes, retained setup/cleanup, and the
  fresh runtime gates required before implementation or default use

## 2026-08-15 grain-gate requirements

- [[EXP-20260816-142 - Independent terrain height and standoff audit]] -
  independent fresh-context audit accepting EXP-141: full pipeline
  re-disassembly, line-by-line reimplementation review, an attacked and
  repaired bucket-order equivalence argument with an exhaustive
  zero-protrusion scan, receipt/standoff reruns with a scratchpad tamper
  test, and three recorded latent gaps (loader `+0x10 >= 0x100` branch,
  the `0x004A865B` trap, equivalence wording), none result-changing
- [[EXP-20260816-141 - Engine-faithful terrain height and gate standoffs]] -
  offline reimplementation of the exact terrain height pipeline
  (collector/resolver/edge test, clones, cell-derived bounds), validated
  at four accepted receipt points with one exact match; pins world Y as
  downward, records the KU-061 Z-bounds contradiction, and computes
  deterministic candidate teleport standoffs for all twelve gates
- [[EXP-20260815-140 - Independent static gate geometry and overlay audit]] -
  independent fresh-context audit accepting EXP-139: rehash, raw-byte and
  disassembly re-verification, call-site census, X/Z swap falsification test,
  recomputed cross-checks, profile-invariance byte diff, and overlay 1.3.0
  read-only/two-hash boundary review
- [[EXP-20260815-139 - Static grain-gate trigger geometry]] - offline static
  extraction of every Tunnels/City trigger center, radius, state array, and
  animation argument with raw-byte pins; cross-checked against the accepted
  EXP-137 boundary points and supported by the overlay 1.3.0 `--gates`
  readout for the mapping pass
- [[EXP-20260815-138 - Independent modified grain-gate threshold audit]] -
  accepts only the exact Tunnels row-3 and City gate-0 same-position
  thresholds after raw/helper/profile/static/runtime and hygiene attacks
- [[EXP-20260815-137 - Modified grain-gate threshold behavior]] -
  independently accepted same-position physical boundaries for Tunnels row 3
  and City gate 0, saved City approach/trigger coordinates, renderer-gate
  correction, and explicit write-assisted limits
- [[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]] -
  corrects Tunnels to internal Level03 and City Entrance to Level04, exposes
  exact independent requirements, and validates modified Direct3D level loads
  with the later physical-transition follow-up separated into EXP-137

## 2026-08-11 disc census and Ghidra baseline

- [[EXP-20260811-001 - PC disc census and executable identification]]: identified the installer-designated PC executable candidate without modifying the ISO.
- [[EXP-20260811-002 - Ghidra static baseline]]: reproducibly imported, analyzed, and exported the exact candidate hash without semantic renaming.

## Static baseline

- [[EXP-20260811-003 - PC-native import string and function map]]

## Runtime baseline

- [[EXP-20260811-004 - Wine launch and CD sentinel gate]]
- [[EXP-20260812-005 - Wine training baseline]]
- [[EXP-20260812-007 - Gamescope hardware presentation baseline]]

## Level-data vertical slice

- [[EXP-20260812-006 - LEVEL DAT prefix and manifest mod]]
- [[EXP-20260812-008 - Training record watchpoints and individual roles]]
- [[EXP-20260812-009 - Training payload target structure and reuse census]]
- [[EXP-20260812-010 - Training target rebind visible substitution]]
- [[EXP-20260812-011 - Training record center candidates]]
- [[EXP-20260812-012 - Training record visibility bound]]
- [[EXP-20260812-013 - Level 01 target rebind no visible start effect]]

## Gameplay and collectibles

- [[EXP-20260814-111 - Training 51st grain collectible vertical slice]]:
  exact-hash insertion and 556 PC fixups produce 51 selector-`0x14` records;
  complete-tree Direct3D runtime and an isolated pickup accept the new record
- [[EXP-20260814-112 - Training 51 counter and tally boundary]]: controlled
  `49 -> 50 -> 51` transitions, natural HUD digits `(5,1)`, and a reversible
  three-byte tally patch preserve the original 50 milestone while rendering
  `51/50`; resolves `KU-054`
- [[EXP-20260814-113 - Training FLIK letter transformations]]: exact
  move/duplicate/remove support, four moved live duplicates with independent
  mask bits `1/2/4/8`, and an explicit repeated-completion boundary when a
  duplicate is collected after mask `0x0F`; resolves `KU-055` only at that
  data-only boundary
- [[EXP-20260815-114 - Training FLIKFLIK HUD and completion]]: exact eight-bit
  ownership, incomplete-to-`0xFF` one-shot completion, centered in-level/tally
  `FLIKFLIK`, and visible `8/8`; resolves `KU-056` only for that exact design
- [[EXP-20260815-115 - Independent M3.4 hard-truth audit]]: accepts the exact
  M3.4 boundary after independent build/inverse, x86/PE/state, runtime-linkage,
  CLI-refusal, full-suite, and hygiene attacks
- [[EXP-20260815-116 - Level03 type-1 row discriminator]]: M3.5 active on an
  exact PC static/data discriminator for Level03 row 6; natural unchanged-PC
  death/reset causality remains pending and no checkpoint-object claim is made
- [[EXP-20260815-117 - Approved Level03 row-6 reset rerun]]: accepted exact
  PC row-6 reset-coordinate consumer causality after the explicitly authorized
  prerequisite-state rerun; natural producer and semantics remain open
- [[EXP-20260815-118 - Natural Level03 material-1 reconnaissance]]: bounded
  no-write upper-corridor route with no material-1/reset event; its scanner
  coordinate labels are corrected by EXP-131
- [[EXP-20260815-119 - PC input movie recorder and hardware replay]]: 11
  asset-free regressions, one exact-window production keyboard recording, and
  two fresh accepted hardware-selector replays; CAP-002 is partial, not an
  engine-frame or Level03-event result
- [[EXP-20260815-120 - PC input movie companion controls]]: separate Tk
  Choose/Start/Stop/Close controls around the unchanged pinned PC launcher and
  strict movie worker; 11 offline fixtures pass, with live behavior in EXP-121
- [[EXP-20260815-121 - First companion route replay divergence]]: first live
  306-event companion movie dispatches completely and reaches hardware after
  one disclosed precondition input, but diverges at Level Select without
  loading Training; manual-delay gameplay acceptance is rejected
- [[EXP-20260815-122 - Anchored companion record and replay controls]]: 23
  focused offline fixtures accept the shared Level Select marker, explicit
  worker readiness, replay menu, saved/next separation, neutral-wait
  preservation, and retained-group cleanup; live route acceptance remains open
- [[EXP-20260815-123 - Level Select anchored route gameplay desynchronization]]:
  fresh 300/300 replay passes Hardware and loads Training, correcting the menu
  race, but later gameplay visibly desynchronizes; its loading inference is
  superseded by EXP-124
- [[EXP-20260815-124 - Replay echo identifies target input stream distortion]]:
  timestamped `NextLife` precedes the first gameplay key, while simultaneous
  exact-window echo proves two inserted normalized events and 15-39 ms timing/
  hold changes in the current replay backend
- [[EXP-20260815-125 - Persistent echoed replay and residual gameplay divergence]]:
  two fresh arms reproduce all 300 target-window events below 0.52 ms delivery
  drift but reach different Training outcomes; persistent echo closes the
  emitter defect, while `NextLife` anchoring plus runtime-log checkpoints are
  required for the next user recording
- [[EXP-20260815-126 - Manual Level03 coordinate-guided probe]]: user-driven
  control route reaches the red mushroom/upper corridor and one probable raw
  damage transition, but no collision value 1, reset bit, or nonzero
  `NextLife`; bounded negative only
- [[EXP-20260815-127 - Read-only PC coordinate overlay]]: focused decoding and
  companion tests plus a live retail smoke accept exact-target
  `process_vm_readv`, translucent coordinate-window creation, and joined
  cleanup without debugger mutation; its coordinate-source claim is
  superseded by EXP-128
- [[EXP-20260815-128 - Live Flik position globals]]: controlled Training jump,
  ground movement, and static PC evidence confirm current XYZ at `0x0059D910`,
  a preceding-position triple at `0x0059D920`, and reject `0x0059D960` as live
  airborne position
- [[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]]: two
  ordinary first-grain-gate pit falls capture descriptor/value `572/1`, flags
  `0x14`, `NextLife=2`, and a repeated row-7-like endpoint; the spider control
  is a distinct `543/0` death path, narrowing KU-057 to natural row-6 selection
- [[EXP-20260815-130 - Write-assisted Level03 teleport safety boundary]]:
  accepts current+preceding relocation only to one known walkable Level03
  point, proves the engine may adopt equal current/preceding as auxiliary in
  about 10 ms, and rejects unsupported-point teleport as natural KU-057
  evidence after two disclosed reset-loop procedure failures
- [[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]]:
  corrects the EXP-118 descriptor-row alignment, maps nine exact Level03
  result-1 X/Z regions to the 18 type-1 rows, identifies descriptor 572 as the
  sole rows-6/7 region, and completes M3.5 by explicit split-evidence
  disposition without claiming a natural row-6 event
- [[EXP-20260815-132 - M3 exit-gate reconciliation]]: reproduces all five
  accepted M3 recipe hashes and inverse receipts, passes 25 focused recipe
  tests, supports all four written exit gates at the worker boundary, and
  marks M3 Complete without widening its semantic or replay boundaries; its
  independent-closure result is superseded by EXP-133
- [[EXP-20260815-133 - Independent M3 closure authorization hard-truth audit]]:
  independently reproduces the five recipes/inverses, focused/full gates,
  Level03 receipts, and data/logic boundary, but rejects gate 1 because the
  cited EXP-111 through EXP-114 records do not preserve prior explicit
  authorization for their Training state changes and breakpoints; opens only
  `KU-059` and corrective packet M3.7
- [[EXP-20260815-134 - Approval-compliant Training runtime receipts]]:
  worker-completes M3.7 with two fresh, explicitly authorized, breakpoint-free
  retail Training position-write arms; appended grain changes `0 -> 1` and
  moved duplicate-letter mask changes `0 -> 1` with isolated records, 791
  read-only samples per arm, survival, exact hashes, and complete cleanup;
  later independently accepted by EXP-135
- [[EXP-20260815-135 - Independent M3 ratchet acceptance audit]]:
  independently rehashes and parses both EXP-134 traces, reproduces the
  exercised helper from reviewed C source, rebuilds all five recipes, passes
  25/25 focused, 9/9 terrain, 576 complete tests plus Vault/M4/tracked gates,
  resolves `KU-059`, and accepts all four M3 gates at their retained limits

## Resource dependency mapping

- [[EXP-20260812-014 - PC content census and loader context]]
- [[EXP-20260812-015 - Plant pair caller and consumer trace]]
- [[EXP-20260812-016 - Plant request origin and separate DAT table]]
- [[EXP-20260812-017 - Bounded PC ANM inspector]]
- [[EXP-20260812-018 - Same-layout PC ANM replacement]]
- [[EXP-20260812-019 - Same-size paired plant replacement]]
- [[EXP-20260812-020 - Training plant10 request suppression]]
- [[EXP-20260812-021 - Plant10 runtime destination and M1 negative window]]
- [[EXP-20260812-022 - Plant10 post-init object-entry negative]]
- [[EXP-20260812-023 - Plant10 late-initialization pointer-surface negative]]
- [[EXP-20260812-024 - Plant10 entry-head bounded negatives]]
- [[EXP-20260812-025 - Plant10 entry-head 0C bounded negative]]
- [[EXP-20260812-026 - Plant10 entry 2E bounded negative]]
- [[EXP-20260812-027 - Plant10 entry 28 bounded negative]]
- [[EXP-20260812-028 - Plant10 post-title selected-entry negative]]
- [[EXP-20260812-029 - Fresh selected-entry chain debugger fault]]
- [[EXP-20260812-030 - Unexpected-signal-safe GDB control]]
- [[EXP-20260812-031 - Adjacent caller-gate continuation fault]]
- [[EXP-20260812-032 - Fixed trajectory paired plant replacement]]
- [[EXP-20260812-033 - Character ALL replacement visible outcome]]
- [[EXP-20260812-034 - Character request and first consumer trace]]
- [[EXP-20260813-035 - Character retained-range first-use bridge]]
- [[EXP-20260813-036 - Shared-entry render-lineage discriminator]]
- [[EXP-20260813-037 - ID-zero stream-difference localization]]
- [[EXP-20260813-038 - Per-entry submission-arena negative]]
- [[EXP-20260813-039 - Direct3D renderer-path reconciliation]]
- [[EXP-20260813-040 - Direct3D retained-entry batch provenance]]
- [[EXP-20260813-041 - Changed-record form localization]]
- [[EXP-20260813-042 - Per-record Direct3D append discriminator]]
- [[EXP-20260813-043 - Exact 0A6C builder-input localization]]
- [[EXP-20260813-044 - Exact 0A6C admission-state localization]]
- [[EXP-20260813-045 - Exact 0A6C admission evaluator fixtures]]
- [[EXP-20260813-046 - Exact 0A6C live admission receipt]]
- [[EXP-20260813-047 - Exact 0A6C consecutive-cycle envelope fixtures]]
- [[EXP-20260813-048 - Exact 0A6C consecutive-cycle live receipt]]
- [[EXP-20260813-049 - M2 exit-gate reconciliation]]
- [[EXP-20260813-050 - M1 positive-target selector-2 input provenance]]
- [[EXP-20260813-051 - Generic resource-index producer census]]
- [[EXP-20260813-052 - M2 dependency-gate disposition]]
- [[EXP-20260813-053 - Signed source-record selector provenance]]
- [[EXP-20260813-054 - M2 continuation scope disposition]]: superseded in part
  by the hard-truth audit; causal-gate and M4.1 technical conclusions retained
- [[EXP-20260813-055 - M2 deferral hard-truth audit]]
- [[EXP-20260813-056 - Fixed-pool index producer census]]
- [[EXP-20260813-057 - M2 second deferral hard-truth audit]]
- [[EXP-20260813-058 - Residual fixed-pool index reader disposition]]
- [[EXP-20260813-059 - Independent M2.41 disposition hard-truth audit]]

## Mod toolkit ratchet

- [[EXP-20260814-060 - Exact whole-file replacement manifest boundary]]
- [[EXP-20260814-061 - Independent M4.1 hard-truth audit]]
- [[EXP-20260814-062 - Complete planned-output containment preflight correction]]
- [[EXP-20260814-063 - Independent M4.3 hard-truth audit]]: accepts the
  deterministic planned-path/type correction and selects exact two-manifest
  composition/conflict packet M4.5
- [[EXP-20260814-064 - Deterministic two-manifest composition and conflict report]]:
  worker-complete exact two-input existing-schema composition/conflict boundary;
  superseded at the complete done-claim boundary by independent rejection
- [[EXP-20260814-065 - Independent M4.5 hard-truth audit]]: rejects M4.5
  acceptance because global span sorting can reverse an independently valid
  input's authored edit sequence; selects exact corrective M4.7
- [[EXP-20260814-066 - Preserve composed manifest edit sequences]]: closes the
  exact order reversal at the M4.7 worker boundary through canonical input
  rank plus original edit index
- [[EXP-20260814-067 - Independent M4.7 hard-truth audit]]: accepts exact
  authored-sequence two-input composition and selects receipt-validated sparse-
  overlay removal as exact M4.9
- [[EXP-20260814-068 - Receipt-validated sparse-overlay removal]]: worker-
  complete exact source/receipt/output/tree-authenticated removal of dedicated
  ordinary sparse overlays; independently rejected by M4.10
- [[EXP-20260814-069 - Independent M4.9 sparse-overlay removal hard-truth audit]]:
  preserves ordinary and local removal baselines but rejects complete
  preflight for a bind-mounted overlay directory; activates exact M4.11
- [[EXP-20260814-070 - Mounted sparse-overlay deletion-plan path refusal]]:
  worker-complete Linux mountinfo guard rejects isolated bind-mounted root,
  intermediate, output, and receipt paths before mutation; activates exact
  fresh-context M4.12
- [[EXP-20260814-071 - Independent M4.11 mounted-plan-path hard-truth audit]]:
  preserves exact-root/descendant and ordinary baselines but rejects M4.11
  acceptance because a proper-parent mount alias is omitted; activates exact
  traversed-overlay-root-ancestry correction M4.13
- [[EXP-20260814-072 - Traversed overlay-root ancestry mount-alias refusal]]:
  worker-complete M4.13 rejects the exact proper-parent alias while preserving
  ordinary filesystem-mount cleanup; independently rejected by M4.14
- [[EXP-20260814-073 - Independent M4.13 traversed-ancestry hard-truth audit]]:
  preserves the uncovered proper-parent and all retained baselines but rejects
  M4.13 acceptance because a hidden lower alias covered by a distinct ordinary
  top filesystem still taints their shared pathname; activates exact M4.15
- [[EXP-20260814-074 - Covered lower mount record exclusion]]: worker-complete
  M4.15 excludes only same-path parent-stack-covered lower records, removes the
  authenticated visible ordinary-top overlay, preserves source/hidden target,
  and retains all five prior mounted-path refusals; activates exact M4.16
- [[EXP-20260814-075 - Independent M4.15 covered-stack hard-truth audit]]:
  preserves M4.15's covered-stack correction and every retained baseline but
  rejects M4.16 because a newer uncovered bind can reuse a freed numerically
  lower mount ID than its source and bypass alias classification; activates
  exact corrective M4.17
- [[EXP-20260814-076 - Mount generation order for ancestry aliases]]: worker-
  complete M4.17 replaces reusable legacy-ID age with verified current-Linux
  later-mount order, rejects the exact reused-lower-ID alias unchanged, retains
  covered-stack and accepted baselines, and activates exact M4.18
- [[EXP-20260814-077 - Independent M4.17 mount-order hard-truth audit]]:
  accepts M4.17 after current-x86_64 ABI/kernel review, adversarial syscall/
  mapping/table injection, an independent old-ID 1081/1082/1081 namespace
  reproduction, all retained namespace/parser/removal/M4/M1/local gates, and
  activates exact versioned-compatibility packet M4.19
- [[EXP-20260814-078 - Versioned exact M4 compatibility statement]]: worker-
  complete strict asset-free M4 v0.1 metadata/checker with five evidence-bound
  hashes, existing schema/operation limits, current-Linux removal and tested
  Wine/Gamescope scope, 18 drift checks, and 311 canonical tests; activates
  exact fresh-context M4.20
- [[EXP-20260814-079 - Independent M4.19 compatibility-statement hard-truth audit]]:
  confirms canonical statement/current-authority/no-game-read boundaries but
  rejects M4.20 because effective competing launcher/implementation values and
  a contradictory Environment row survive substring-only alignment; activates
  exact corrective M4.21
- [[EXP-20260814-080 - Unambiguous effective compatibility-authority declarations]]:
  worker-complete M4.21 replaces substring presence with ordered shell,
  Python-AST, generated-row, and scoped-Markdown extraction; rejects the four
  exact attacks plus adjacent ambiguity with 36/329 tests and activates exact
  fresh-context M4.22
- [[EXP-20260814-081 - Independent M4.21 authority-extraction hard-truth audit]]:
  preserves the exact statement, four predecessor rejections, scoped
  declarative checks, 36/329 tests, and nine reads, but rejects M4.22 because
  effective post-declaration shell/Python changes and duplicate manifest keys
  still pass; activates exact same-read machine-authority pins in M4.23
- [[EXP-20260814-082 - Closed-world machine-authority byte pins]]: worker-
  complete M4.23 pins exactly five already-read machine authorities, rejects
  all six residual bypass families, passes 47/340 tests, preserves the exact
  statement and nine-read asset-free boundary, and activates exact M4.24
- [[EXP-20260814-083 - Independent M4.23 machine-authority-pin hard-truth audit]]:
  accepts the immutable exact-five same-read pin correction after independent
  statement/hash reconstruction, 10/10 predecessor attacks, 5/5 direct and
  missing-pin cases, 3/3 scoped human checks, nine reads, and 47/152/340 tests;
  activates only deterministic single-manifest dry-run report M4.25
- [[EXP-20260814-084 - Deterministic single-manifest dry-run report]]: worker-
  complete M4.25 reuses exact preparation for deterministic authored file/
  record/hash/size/range JSON with zero writes; passes 99/161/349 tests,
  refreshes only the manifest implementation pin, and activates exact M4.26
- [[EXP-20260814-085 - Independent M4.25 single-manifest dry-run hard-truth audit]]:
  accepts exact M4.25 after direct byte/report reconstruction, 91 assertions
  across 20 success/failure/workflow cases, zero trapped writes, exact
  snapshots and receipts, 38 compatibility assertions, nine reads, and
  99/161/349 tests; activates only M4.27 milestone-closure evidence audit
- [[EXP-20260814-086 - M4 v0.1 milestone-closure evidence audit]]: rejects M4
  closure after an explicit nine-capability/five-exit-gate ledger supports
  eight/four rows but exposes receipts as insufficient without the original
  manifest and no joined clean-derived-copy install/validate/launch/remove
  lifecycle; activates only strict receipt reconstruction M4.28
- [[EXP-20260814-087 - Strict receipt reconstruction for replay and removal]]:
  worker-complete M4.28 adds strict external ordinary receipt authority,
  current existing-schema reconstruction, new-root sparse replay, and shared
  authenticated removal without the original manifest; passes 146/208/396
  tests and six exact local cycles, and activates exact independent M4.29
- [[EXP-20260814-088 - Independent M4.28 receipt-reconstruction hard-truth audit]]:
  rejects M4.28 acceptance because a checked receipt parent can change into a
  directory link before final file acquisition while the same accepted inode
  keeps final descriptor checks green; retains mapping, 80/80 strict cases,
  146/208/396 tests, 37 removal/mount cases, six local cycles, five pins, and
  nine reads; activates only component-stable receipt acquisition M4.30
- [[EXP-20260814-089 - Component-stable external receipt acquisition]]:
  worker-complete M4.30 retains and validates every lexical receipt component
  through relative no-link descriptors, reacquires the full chain before
  parsing, rejects the exact parent substitution and adjacent changes, passes
  154/216/404 tests and six exact local cycles, and activates only independent
  M4.31
- [[EXP-20260814-090 - Independent M4.30 component-acquisition hard-truth audit]]:
  exact M4.31 retains the parent/adjacent refusals, 28/28 independent cases,
  154/216/404 tests, six local cycles, five pins, and nine reads, but returns
  `REJECT` because one close error skips later chain descriptors and retains
  seven or six; activates only exception-safe chain closure M4.32
- [[EXP-20260814-091 - Exception-safe receipt-handle-chain closure]]: worker-
  complete M4.32 attempts every owned descriptor close once despite earlier
  errors, preserves primary/cleanup-only behavior, passes 161/223/411 tests
  and six local cycles, and activates only independent M4.33
- [[EXP-20260814-092 - Independent M4.32 receipt-chain-closure hard-truth audit]]:
  accepts exact M4.32 after the parent +7/+6 reproduction, 28/28 fresh indexed
  partial/nested closure cases, 161/223/411 tests, six local cycles, five pins,
  and nine reads; resolves only `KU-051` and activates audit-only M4.34
- [[EXP-20260814-093 - Clean-derived-copy lifecycle feasibility audit]]:
  rejects M4 completion after one four-route same-tree ledger proves complete
  staged/forced-copy outputs are launcher-ready but not sparse-removable, while
  removable apply/replay outputs are not complete game trees; selects only
  manifest-driven clean-copy restoration M4.35
- [[EXP-20260814-094 - Manifest-driven clean-copy restoration]]: worker-
  complete M4.35 authenticates complete source/game path/type/content,
  recorded outputs/receipt, and every expected mount path before restoring only
  recorded destinations; passes 188/250/438 tests, four private mount cases,
  six retained local cycles, and one exact 722-file launcher-dry-run lifecycle;
  activates independent M4.36
- [[EXP-20260814-095 - Independent M4.35 clean-copy-restoration hard-truth audit]]:
  retains ordinary restoration, drift/identity/mount refusals, the exact local
  lifecycle, six sparse cycles, five pins/nine reads, and 188/250/438 tests,
  but rejects acceptance because `Case.bin` and `case.bin` coexist and restore;
  activates only case-insensitive complete-tree uniqueness M4.37
- [[EXP-20260814-096 - Complete-tree case-insensitive path uniqueness]]:
  worker-complete M4.37 assigns every complete-tree file/directory one
  case-folded key, rejects eight source/game collision shapes with exact
  snapshots and read/mutation traps, passes 198/260/448 tests plus the exact
  local lifecycle and six sparse cycles, refreshes only the manifest pin, and
  activates independent audit/docs M4.38
- [[EXP-20260814-097 - Independent M4.37 complete-tree-uniqueness hard-truth audit]]:
  accepts immutable M4.37 after the exact parent reproduction, 36 independent
  collision cases, four bind-mounted sibling-order cases, all eight namespace
  families, five identity swaps, exact 722-file lifecycle, six sparse cycles,
  five pins/nine reads, and 198/260/448 tests; resolves only `KU-052` at the
  demonstrated current-Linux boundary and activates M4.39 statement alignment
- [[EXP-20260814-098 - Strict v0.2 restoration compatibility statement]]:
  preserves 6,177-byte historical v0.1, publishes canonical 7,677-byte v0.2
  with only the accepted restoration boundary, retains five pins/nine reads,
  and activates only exact independent M4.40; its combined count 266 is later
  corrected to 271
- [[EXP-20260814-099 - Independent M4.39 statement and milestone-closure hard-truth audit]]:
  retains exact v0.1/v0.2 bytes, restoration truth, five pins, nine reads, all
  151 scalar-value refusals, and 58/271/459 suites, but rejects M4 closure
  because reordered object fields, selected-path cross-version replacement,
  and an unhashable-ID error survive; activates only corrective M4.41
- [[EXP-20260814-100 - Version-bound canonical compatibility-statement strictness]]:
  worker-complete M4.41 binds selected paths to exact v0.1/v0.2, checks every
  object key sequence, normalizes non-string IDs, rejects all 151 value and
  151 type attacks, preserves both statements/five pins/nine reads, and passes
  71/284/472 tests; activates only independent audit/docs M4.42
- [[EXP-20260814-101 - Independent M4.41 selected-path identity hard-truth audit]]:
  retains exact statement reconstruction, recursive order, typed IDs, five
  pins, normal nine-read behavior, 71/284/472 worker evidence, and accepted
  M4.33/M4.38 ledger boundaries, but rejects M4 closure because a default
  active pathname linked to the historical selected file validates v0.1;
  activates only lexical selected-path/non-link correction M4.43
- [[EXP-20260814-102 - Lexical selected-statement identity and non-link admission]]:
  worker-complete M4.43 selects versions lexically, refuses both selected link
  directions before reads, retains arbitrary unselected exact links, preserves
  statements/five pins/nine reads, and passes 75/288/476 tests; activates only
  independent audit/docs M4.44
- [[EXP-20260814-103 - Independent M4.43 selected-path and milestone-closure hard-truth audit]]:
  accepts immutable M4.43 after parent reproduction, selected link/nonregular
  no-read attacks, lexical aliases, unselected exact contracts, complete
  statement/order/leaf/pin reconstruction, normal nine-read checks, and
  75/288/476 suites; closes the ledger at 9/9 capabilities and 5/5 exit gates
  and marks M4 Complete only at the documented current-Linux/asset-free boundary
- [[EXP-20260814-104 - Second independent M4 post-closure verification]]:
  independently confirms the completed 9/9 and 5/5 ledger at exact post-
  closure HEAD after a separate 663-assertion matrix including hard-link and
  parent-link boundary cases, 75/288/476 tests, and hygiene gates; preserves
  every unsupported limit and activates no successor
- [[EXP-20260814-105 - M6 asset-free release lifecycle]]: initially accepts M6
  after correcting appended-tar-content admission, with closure superseded by
  `EXP-20260814-106`; two clean builds match at
  `1527281c...b62a0`, strict 36-file canonical verification passes, the exact
  Fedora 44 21-file/three-case smoke matrix restores 747-entry trees, bounded
  migration/rollback and four failure families pass, and 486 tests plus all
  hygiene gates close M6 only at the asset-free launcher-readiness boundary
- [[EXP-20260814-106 - Independent M6 release hard-truth audit]]: rejects M6
  closure while retaining exact dual-build/archive, smoke, M4, and hygiene
  evidence; installed wrapper use creates unlisted bytecode, linked release
  roots are accepted, and dangling install state is treated as absent
- [[EXP-20260814-107 - M6 installed lifecycle identity correction]]: completes
  the exact worker correction with four bytecode-stable installed entry points,
  fail-closed state/release/version entry admission, full snapshot regressions,
  matching `7a1ede97...fcd2` archives, exact smoke, and 492 tests; activates
  only fresh-context James audit
- [[EXP-20260814-108 - Independent M6 lifecycle consistency hard-truth audit]]:
  rejects the first correction after 20/55 lifecycle cases, 12 snapshot drifts,
  9/10 inventory attacks, and hostile-prefix startup bytecode contradict the
  complete installed lifecycle; retains artifact, tar, smoke, M4, and hygiene
- [[EXP-20260814-109 - M6 state-locked lifecycle consistency correction]]:
  completes the combined second worker at `7d8594e` with schema-2 state locks,
  symmetric all-version verification, exact package/repository topology and
  modes, hostile-cache stability, matching `68d3d31a...060b` archives, exact
  smoke, and 509 tests; activates only the next James audit
- [[EXP-20260814-110 - Independent M6 state-locked lifecycle acceptance audit]]:
  independently accepts the exact second correction after 55/55 lifecycle and
  10/10 inventory refusals with unchanged snapshots, bytecode-free installed
  entry points, matching `68d3d31a...060b` builds, exact smoke, 509 tests,
  five M4 anchors, Vault 312/0/0, and clean tracked state; closes M6 only at its
  explicit asset-free/local-state-trust/Fedora-Wine boundary

## 2026-08-15 M3 causal runtime

- [[EXP-20260815-116 - Level03 type-1 row discriminator]]
- [[EXP-20260815-116-receipt]]

- [[EXP-20260815-117 - Approved Level03 row-6 reset rerun]] - fresh,
  explicitly authorized control/candidate proof that a `+128` row-6 X edit
  produces exact reset-X delta `+4096` with unchanged Z.

## 2026-08-20/21 R2p passive lifecycle

- **2026-08-26 P0D/P0E authorized-scope successor:** James rejected P0D's
  pre-freeze design on six durability/provenance grounds. A test-harness error
  then consumed the real P0D marker before activation without launching the
  game. The marker is preserved. Fresh P0E retains the proved auto-hardware
  `Right`, select-`Return`, Level01-gate, title-`Return` route and fixes all six
  findings with earliest one-shot consumption, a tracked two-phase source
  anchor, a separate Wine-host anchor, atomic bidirectional `Y:` replacement,
  an immediate full pre-restore audit/census, and unverified-only publication.
  It preserves P0A/P0B/P0D identities before/after. James rejected first exact
  `b7777539` / `85799be` on a replaceable P0D physical identity and
  non-exact/impossible publication states. Corrected P0E pins both; focused
  tests pass 542/542 and James's separate 106-case matrix passes. Corrected
  source `c7bdd6c` / `e0a5fea` passed 3343 tests and anchor
  `7342d72...08c5d` binds it. At that pre-run point P0E was unconsumed. Runtime
  remains barred
  pending the final full gate/commit and exact-revision James ACCEPT. No
  terrain/collision result exists. See
  [[2026-08-26 1134 - Codex - P0D consumed and P0E passive successor]].

- **P0E live result:** James accepted exact `b1896e1` / `a696e48`; the sole run
  completed Anthill Level01's 521-point passive grid. Collection
  `9ed7d8e...456b0` has collection-level ACCEPT and one persistent sequence
  27–520 addition from a 16-task baseline. Normal close failed, leaving the
  packet pending, `Y:` staged, and the recorded runtime/sink audit nonclear.
  P0E cannot rerun. Agent recovery requires fresh authority and a separately
  frozen James-reviewed protocol; no terrain/collision conclusion follows.

- **P0E-R1 recovery source:** Fresh authority is bound to one additive cleanup
  attempt that preserves the original pending packet. James rejected two
  candidates for pre-action/failed-prefix/parent-binding defects and then an
  unrecorded predecessor-parent durability gap. Exact corrected source
  `a1a854cf...bb024` passes 101 focused and 809 combined tests; James returned
  `ACCEPTABLE-FOR-SOURCE-FREEZE`, and the 3,444-test full gate passed. At that
  checkpoint no marker, signal, sink unload, `Y:` write, memory access, or
  terrain/collision result existed. Source `dc2481b` / `ba66446` was bound by
  activation `df1def84...3556`; the later run is recorded below. See
  [[2026-08-26 1900 - Codex - P0E additive recovery source freeze]].

- **P0E-R1 consumed result:** Exact activation/docs `3aa9127d` / `1be8a4a`
  passed 3,444 tests and received one-invocation James ACCEPT. The run sent
  authenticated TERM, then KILL, only to residuals 310463/310509. Their
  disappearance between the first two post-KILL census reads tripped the
  stability gate. James accepts failed tree `0be8f7be...43f89` as evidence of
  residual removal, not successful recovery. Post-audit is clean; original P0E
  remains pending, `Y:` staged, and P0E-R1 consumed without retry. No
  terrain/collision result follows.

- **P0E Y-only restoration WIP:** Fresh authority covers one atomic
  stage-to-retail `Y:` restoration. The four-file successor passes 96 focused
  and 357 combined offline tests. James rejected earlier revisions through
  round 26; its cleanup timestamp/error-grammar findings are corrected. Round
  27 confirmed both, then rejected missing/ancient mapping-repair provenance.
  There is no activation anchor or mutating live action; one preliminary
  fixture invoked only a read-only session audit. See
  [[2026-08-27 0816 - Codex - P0E Y restoration hard-truth checkpoint]].

- **P0E Y-only restoration source/activation freeze:** James rounds 28-34
  closed all known mapping/cleanup repair provenance, chronology, durability,
  and state-consistency gaps. Exact module `541fbe59...3d57`, wrapper
  `9c9dbb28...ea80`, freezer `640aefb1...42bc`, and tests
  `bad67fe1...e6111` received round-34 source **ACCEPT** after 98 focused and
  741 broad P0E tests. Source `1964eec` / `f0afa1a` passed 3,542 full tests and
  is bound by activation `95e632dc...d8307`. The marker is absent; no wrapper,
  mapping, runtime, or terrain/collision action occurred. See
  [[2026-08-27 1457 - Codex - P0E Y restoration source and activation freeze]].

- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]: P0A-AH-001 is consumed
  and pending with zero lifecycle samples after its substituted persistent-X
  navigation loaded Level07. Its offline validator hardening is James-accepted
  at `1b61da3` / `925ce80`. A later operational PC launch reconfirmed the
  established direct focused `xdotool` Level01 route without memory access;
  this is not P0B evidence. James accepts the corrected P0B architecture only
  as an offline design basis: direct carousel/select input, persistent sockets
  after the Level01 gate, sole title Return at sample 5, unchanged 521-point
  grid, fresh `Y:` namespaces, and no contact with P0A pending bytes. That
  first offline P0B implementation passed 308/308 focused and 2250/2250 full
  tests, but James rejected exact `2277b75` / `cf2f88c` for seven provenance,
  route, display, schema, publication, direct-analysis, and prohibited/P0A
  boundary families. The successor correction passes 351/351 focused tests;
  its wrapper still refuses runtime; the full gate passes 2293/2293 with zero
  tracked-file violations. That exact candidate was then audited and rejected
  as recorded in the next sentence.
  James then rejected the exact corrected candidate `8b8d19d` / `e8b58c9`
  for nine adjacent parser, nested-manifest, post-grid level, X-observation,
  numeric-alias, object-root, and canonical-terminal-root defects. The next
  offline correction closes all nine and passes 396/396 focused tests. No
  runtime occurred; fresh exact-commit acceptance and authorization remain
  mandatory.
  That 396-test correction then passed 2338/2338 full tests and was frozen as
  `e0fa61a` / `02550b15`. James rejected it for an unhashable P0A entry-type
  exception and an ignored wrong-level load before LevelSelect. The next
  offline correction passes 405/405 focused tests; runtime remains barred.
  That correction passed 2347/2347 full tests and James **ACCEPTED** exact
  `3c90a6f` / `5fb8ea6` as the immutable offline pre-runtime design. At that
  checkpoint runtime still required fresh authorization; the next sentence
  records it.
  The user then replied `okay continue on`, authorizing one P0B-AH-001 wrapper
  invocation. Later explicit `pkill`/signal direction permitted guarded cleanup
  of old group `1978654`; the next audit was clear and the sole P0B invocation
  ran. Its 521/521 collection provisionally found persistent added task
  `2086681/34785536`, sequences 27–520, but normal close failed. P0B is consumed
  and its exact 26-file packet remained pending with new group `2086248` live
  and `Y:` at the P0B stage. James accepted the provisional collection and pending
  interpretation only. James rejected recovery implementation `575756d` for
  exact-schema, census, per-signal-guard, invariant, consumption, and
  publication defects. James rejected the next exact `d4de863` for a nested
  numeric alias, post-deadline polling, and two directory-rename races. The
  corrected successor passed 48/48 recovery, 482/482 non-native P0B, native-X,
  and 2395/2395 full tests and was accepted at exact `fae9b2f`. Its sole
  invocation failed closed after TERM when exiting identities exposed cleared
  command lines; it remains consumed. A separately authorized operator cleanup
  at `4de8b08` then cleared only the three exact residual helpers and restored
  retail `Y:`. James accepted its terminal 15-entry envelope at
  `24df2fb7...d65b`. The original P0B packet remains
  `pending-cleanup-failed`; no terrain/collision claim or second P0B arm follows.
  Offline P0C then authenticates P0B together with R2o D1-AH-005 and confirms
  that the 16→17 post-title lifecycle topology occurred in two fresh
  processes, including debugger-free P0B. This shows that debugging is not
  necessary for the lifecycle class, but it does not prove the two TIDs are
  the same worker. PC-native PLAYTRACK/DirectSound evidence makes worker
  `0x00440F50` the strongest role candidate without binding it to Linux TID
  `2086681`. James preserved that conclusion but rejected first implementation
  `f362fae` for publication, semantic-guard, static-span/source-ledger, and
  wording defects. Rejected `-001` remains `ecd92bfd...9c7`. James then
  rejected exact `923ffb2` because `-002` (`6156b968...1f88`) claimed a
  complete executed-source ledger while omitting imported `r2c_f0.py`.
  Fresh `-003` (`62af5c09...d6ff`) pins `r2c_f0.py`, active
  `r2c_localizer.py`, and the package-init/parser chain; it passes 45/45
  focused wrapper-rooted import-closure tests and the 2470/2470 full gate with
  zero tracked-file violations. James **ACCEPTED** exact `f2629944` /
  `9c7c1294`; its final exact-tree gate also passes 2470/2470 with zero
  tracked-file violations. Only an offline R2q
  pre-attach quiet-census redesign follows,
  with no runtime or terrain/collision authority.

- **R2q offline quiet-census design (2026-08-23):**
  [[EXP-20260820-005 - R2p task lifecycle diagnostic]] now freezes the future
  two-control post-gameplay barrier: 3,002 requests at 20 ms spacing per
  process (60.020-second first-to-last request span), no fixed task count or
  TID, immediate pre-attach revalidation, and a separate 60.000-second
  acquisition cap. James rejected immutable `-001`; corrected `-002` passes
  69/69 focused tests plus the 2539/2539 candidate-tree repository gate, but
  James rejected exact `a8840d5` for raw P0B/P0C semantic and executable
  receipt-schema gaps. James then rejected exact `caeddfd` / `ac853d4` with
  immutable `-003` (`c41256e5...3931d`) for bypassable runtime census,
  manifest, journal, capture, and comparison schemas. James rejected exact
  `0606bcf` / `ca7800e` with immutable `-004` (`0f0f7cfe...05f9b`) for eight
  remaining title, identity/hash, chronology, task/debugger/memory/detach,
  terminal-publication, two-control, process-group-reuse, and numeric-alias
  gaps. James rejected fresh `-005` (`a5472f01...31c5e`) at exact `814ada4` /
  `b79e885` for ten remaining log, namespace, publication, lifecycle,
  cleanup, failure-prefix, type, invariant, and title-task gaps. Immutable
  pre-audit `-006` (`a068f686...1b33`) made those boundaries executable but
  was superseded because its accepted-root tree hash was asserted. Immutable
  `-007` (`f7cf2346...2d12`) authenticates the exact tree manifest and passes
  163/163 focused plus 2633/2633 full tests, but James rejected exact
  `ecf809f` / `71b294f` for chronology, failure-cleanup, independent-reread,
  command-line, and aggregate error-boundary gaps. Fresh immutable `-008`
  (`91401455...e155`) closes those cases and passes 175/175 focused plus
  2645/2645 exact-tree tests in 916.68/911.92 seconds with zero tracked-file
  violations, but James rejected exact `18591f3` / `ff65061` for bypassable
  title/mapping prefixes, later-failed cleanup/close prefixes, an unbound
  action-9 failure prefix, and impossible/unbound rename-parent provenance.
  Fresh immutable `-009` (`c8c451fa...047a1`) closes those cases with shared
  prefix semantics and authenticated same-filesystem source-parent stats; it
  passes 192/192 focused tests in 444.74 seconds and the 2662/2662 first full
  gate in 1102.04 seconds with zero tracked-file violations. James rejected
  exact `f81502b` / `e56942b` because the conditional reducer omitted further
  authenticated dependency families and source-parent stat time was not
  anchored to terminal/comparison outer chronology. Fresh immutable `-010`
  (`d07d3d5e...effd5c`) consolidates every dependency-applicable accepted,
  rejected, and pending relation into one reducer and requires the full
  validation/outer/stat/fsync/rename/reread order after both post-D2 rereads.
  It passes 226/226 focused tests in 727.47 seconds and the 2696/2696 first
  full gate in 1369.49 seconds with zero tracked-file violations, pending exact
  commit/final gate and James re-audit. It has no runtime entry point or
  terrain/collision claim.
  James rejected exact `-010` commit `889f105` / tree `a93c929` because its
  nominal process record and exact same-path/SHA executable asset entry carried
  contradictory device/inode/size/mtime tuples. Fresh immutable `-011`
  (`6a8fd3df...c1022`) cross-binds executed path/SHA/stat identity in the
  accepted and shared conditional-prefix validators, with coherent direct and
  accepted/rejected/pending terminal regressions. It passes 229/229 focused
  tests in 740.93 seconds and the 2699/2699 first full gate in 1397.31 seconds
  with zero tracked-file violations, pending exact commit/final gate and James
  re-audit. It remains offline and adds no terrain/collision evidence.
  James then **ACCEPTED** the documentation-inclusive `-011` basis at exact
  `409cbfb` / `de4fa87`, after authenticating the three-note `-010` byte-count
  correction, unchanged implementation/artifact hashes, Vault 608/0/8, and a
  clean tree. This is offline acceptance only; runtime still requires fresh
  explicit authorization and no terrain/collision claim follows.
  Runtime-edge `-012`, `-013`, `-015`, and `-016` were subsequently James-
  rejected; intermediate `-014` was superseded without a verdict. Candidate
  James rejected exact `-017` `2267cc5` / `8166cc4` because its five-second
  benchmark did not execute complete terminal/comparison publication, a valid
  pre-attempt competitor was unaccountable, and final-fsync failure was falsely
  durable/late. Frozen `-018` adds staged post-boundary facts, separate
  complete-envelope/durability derivation, atime-independent material identity,
  and `terminal-publication-benchmark-004` (worst 79.340400010 seconds under a
  prospective 180-second ceiling). James then rejected exact `-018` `7e6a3b0` /
  `2c99bef`: late classification lacked an exact deadline receipt, the claimed
  30-second failure-recording budget was not end-to-end, and the benchmark did
  not authenticate timed production source bytes. `-019` corrected all three,
  but James rejected exact `8e1b989` / `c3334e3` because owned deadline records
  still admitted impossible outer semantics and malformed `stage` leaked raw
  `TypeError`. Frozen `-020` uses failure protocols v5, exact outer error/
  message/phase/chronology bindings, and strict string stage validation.
  `-020` is 105,429 bytes / `462b882d...061a`; benchmark `-006` is 4,563 bytes /
  `72373103...e95b`, anchored to `9e4ccf7` / `f2502d8` and ledger
  `0f184368...bcf27`. The complete R2q gate passes 331/331 in 1,799.86 seconds.
  The first and documentation-complete full repository gates pass 2,801/2,801
  in 2,458.12 and 2,457.27 seconds with zero tracked-file violations. James
  **ACCEPTED** exact `4635a53` / `fa5d63d` after independent provenance,
  validator, failure-semantics, malformed-case, runtime-test, and strengthened-
  terminal verification. See
  [[2026-08-22 1553 - Codex - R2q offline quiet-census design]] for exact
  commits, artifact hashes, and blocker chronology. The retained passive-P0A
  authorization excludes R2q's ptrace and process-memory scope; no runtime or
  terrain/collision claim follows.

- **R2q hard-truth source/activation continuation (2026-08-30):**
  [[EXP-20260820-005 - R2p task lifecycle diagnostic]] and
  [[2026-08-30 1519 - Codex - R2q hard-truth source and activation freeze]]
  retain benchmark-007/design-021, then freeze fresh source `3998111` /
  `0c61a85`, benchmark-008 `eb930b77...9cfd9`, anchor
  `1049049c...b7a1`, and design-022 `b79f63b0...e6b72`. The full gate passes
  3,786/3,786. This is offline activation only; no game, runtime, or
  terrain/collision observation occurred.

- **R2q-022 failed arm and mapping-only recovery (2026-08-30):**
  [[2026-08-30 2221 - Codex - R2q-022 failed-run mapping recovery]] records
  the consumed D1 launch-identity failure, skipped scientific phases, exact
  preserved failure closure, and separately authorized one-shot Y mapping
  recovery. James accepts recovery tree `f3cf883f...a5824`; Y is retail, R is
  unchanged P0A, and the session audit is clear. The original experiment
  remains failed and supplies no quiet-census or terrain/collision result.

- [[2026-08-28 1704 - Codex - P0E Y restoration recovery3 activation freeze]]
  - James rounds 39/40 accepted the distinct YR4 source and fresh authority;
    source `9a815a3` / `27b23a` is frozen by inert activation
    `111fbc78...6fcb`. Marker absent, Y staged, no terrain/collision result.

- [[2026-08-28 1704 - Codex - P0E Y restoration recovery3 activation freeze]]
  - Later sole YR4 action succeeded: marker `b109d6ca...c5e00`, packet tree
    `9a4979ca...e46c6`, retail Y, P0A R, clear audit. James accepts mapping
    success only; R2q/terrain/collision remain unrun and separately authorized.

- **R2q `-024` offline activation continuation (2026-08-31):**
  [[EXP-20260820-005 - R2p task lifecycle diagnostic]] and
  [[2026-08-31 0648 - Codex - R2q 024 hard-truth activation freeze]] preserve
  immutable design-023 `be7cf41f...08cd3c`, freeze James-accepted source
  `022f739` / `9d78651`, benchmark-010 `592ac4a7...d3e7`, anchor
  `10264047...fb7`, and design-024 `321eb8c6...2288`. The full gate passes
  3,843/3,843. This remains offline/runtime-unauthorized and adds no
  terrain/collision or task-role result.

- **R2q-024 failure/recovery and `-025` continuation (2026-08-31):**
  [[EXP-20260820-005 - R2p task lifecycle diagnostic]] and
  [[2026-08-31 1849 - Codex - R2q 025 activation freeze]] preserve the
  consumed pre-science `-024` failure, James-accepted mapping-only recovery
  tree `afacab0a...90bfa`, and fresh source `d23ece3` / `8492bcb`. Protocol v7
  raises the measured-safe bounds to 448 MiB raw / 192 MiB stored. Benchmark-
  011 is `9ec2ec6a...d79`; immutable design-025 is `d25acc8c...34a9`; full
  `make check` passes 3,878/3,878. Runtime remains unauthorized and no terrain/
  collision or task-role result exists.

- **R2q-025 failed arm and mapping-only recovery (2026-09-01):**
  [[EXP-20260820-005 - R2p task lifecycle diagnostic]] and
  [[2026-09-01 0317 - Codex - R2q 025 failed-run mapping recovery]] preserve
  the consumed pre-science process-map-convergence failure and the separately
  authorized one-shot Y recovery. James accepts recovery tree
  `0b0aa411...f4d2b`; retail Y is inode `9773754`, P0A R is unchanged, the
  audit is clear, and the 3,905-test full gate passes. No terrain/collision or
  task-role conclusion follows; continuation requires a fresh successor.

- **R2q-026 offline convergence freeze (2026-09-01):**
  [[EXP-20260820-005 - R2p task lifecycle diagnostic]] and
  [[2026-09-01 1524 - Codex - R2q 026 convergence and activation freeze]] bind
  the complete failed/recovered `-025` closure, enforce the real five-second
  process-map deadline, and freeze benchmark-012/design-026. Full `make check`
  passes 3,908/3,908. Runtime remains unauthorized and KU-079/080/081 remain
  open.

## 2026-09-05 original-wall comparison

- [[EXP-20260905-005 - Original wall texture regions and colour inputs]]:
  static census complete; a later original runtime added a close wall view, ten
  captures and read-only page 0 extraction. Authored region/colour comparison
  arms were not run live; the region/tint controls are offline fixtures, not
  live causal arms. 151 terrain tests passed.

## 2026-09-05/06 terrain tiling, Level01 coverage and ramp visibility

- [[EXP-20260905-006 - World-scale terrain tiling and checked mesh growth]]: atlas-local repetition, checked object-pointer/end-relative-footer growth, original x86 relocation comparison and 185 passing terrain tests; collision preserved; live visual acceptance pending.
- [[2026-09-05 - Codex - Terrain texture tiling and mesh growth]]: EXP-005/006 evidence scope, private archive and focused validation.

- [[EXP-20260905-007 - Retail position control and missing floor footprints]]: retail RAM control and selected active-floor coverage differences after source-99 replacement; exact earlier fall and invisible-ground face mapping remain open.

- [[EXP-20260905-008 - Whole-Level01 collision and render coverage audit]]: complete Level01 edit inventory confirms source 99 alone replaces 134 original cells with 14 authored cells; 7,147 cells and all barriers are unchanged. Render mesh 160 alone changes but covers a different footprint.

- [[EXP-20260905-009 - Additive terrain preservation and access ramp]]: final 224/224 terrain gate; native preservation, relocation, command traversal, fall/box checks and four continuous-crossing/return routes pass. Exact-point controller failures retained and diagnosed. Evidence: `reports/terrain/EXP-20260905-009-validation.json`.

- [[2026-09-06 - Codex - Additive runtime startup]]: the EXP-009 build reached the hardware/LevelSelect log gates; a title-guard mismatch stopped input. Operational evidence: `reports/terrain/EXP-20260905-009-runtime.json`. The continuation loaded EXP-009 in Level01 with resident collision/render identity verified read-only: `reports/terrain/EXP-20260905-009-runtime-entry.json`.

- 2026-09-06 EXP-009 ramp visibility: successful collision crossings, but camera-dependent disappearance/reappearance is reproduced with a fixed post-tap position and appended-cell contact 49008. [[2026-09-06 - Codex - Ramp visibility reproduction]]; `reports/terrain/EXP-20260905-009-ramp-visibility.json`.

- 2026-09-06 EXP-009 culling discriminator: original instructions reject mesh 160 at `0x0044D677` for two hidden views; offline radius 8192 admits all five sampled poses, but an intermediate visually unclear sample already passes with 6047. [[2026-09-06 - Codex - Ramp culling discriminator]]; `reports/terrain/EXP-20260905-009-ramp-culling.json`.

- 2026-09-06 EXP-009 live radius A/B/A: exact authorized 6047 -> 8192 -> 6047 reversibly changes ramp visibility at fixed actor/camera/contact. Culling contributor confirmed at one pose; original restored, files unchanged. [[2026-09-06 - Codex - Live ramp radius comparison]]; `reports/terrain/EXP-20260905-009-ramp-radius-live.json`.

- [[EXP-20260906-001 - PC-compatible ramp visibility bounds]]: file-only radius 6047 -> 8560, collision/geometry preserved; 73 affected and 72 focused tests pass; native sweep 0/5152 relevant candidate rejections versus 544 control. [[2026-09-06 - Codex - File-based ramp visibility bounds]]. Its runtime continuation loaded the corrected bound 8560 from file in Level01 with collision/geometry verified read-only, not yet all-view acceptance: `reports/terrain/EXP-20260906-001-runtime.json`.

- [[EXP-20260906-003 - Solid ramp sides and ground contour trim]]: 20 wall cells, clipped side geometry, preserved floors/top, paired native blocking and steered return proofs; 138 affected tests pass. Live, the sides block; a visible model/wall overlap remains open.

- [[EXP-20260906-004 - Wall clearance comparison and offset trial]] - original/render spacing comparison with contrary examples; bounded 1536-world-unit collision-only trial; 69 affected tests, both native arms and 72-test gate pass; live visual/corner acceptance pending.

- [[EXP-20260906-005 - Isolated authored terrain and platform spawn]]: bounded old scene/collision deactivation, exact authored pieces retained and a private executable-table spawn; 53 affected/72 focused tests pass; native 9 accepted/1 setup failure, later corrected to 10/10. See the experiment for offsets and proof limitation.

- [[EXP-20260906-006 - Perimeter barriers and original foliage reference]]: failed perimeter windings retained; an original-PC source180/segment160 discriminator; file-loaded grass blocks without falls; a 202-template visual variety candidate from off-screen original meshes; 62 affected/72 focused tests pass; straight-release numerical limitation retained. No accepted perimeter or exact foliage collision mapping.
