---
type: system-state
status: active
updated: 2026-10-29
tags: [system/state]
---

# Current State

Where the reverse-engineering research on the Windows PC release stands on
2026-10-29. The subject is retail `bugs.exe`, SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
([[BIN-97c95ba5572dce63 - bugs.exe]],
[[EXP-20260811-001 - PC disc census and executable identification]]).
This note summarises; the linked notes hold the evidence. [[Known Unknowns]]
owns open questions, [[Project Roadmap]] owns milestones and gates, and
[[Next Tasks]] proposes an order for the open work.

<!-- briefing: Current task handoff -->
## Current task handoff

**2026-10-29: no research packet is in progress.** No game is running
([[Environment Status#Current runtime handoff]]).

The last research session
([[2026-10-18 - Claude - Static research on creature rows and the script VM]])
added static results EXP-20261018-001 to EXP-20261018-012 and two read-only
hardware arms ([[EXP-20261018-013 - Options screens and the creature gate live]]).
It read the creature rows, the script VM's modes, type handlers and event
sounds, the event callbacks, the controls screen, the frame cap, the default
depth rule, 4-bit palette rows, the type-indexed list table and the telescope
hide flags. The survey before it
([[2026-10-12 - Claude - Survey and prioritize next tasks]]) settled the homing
bit, movement state 4, the scripted-camera flag and the seed record height,
and named all 41 creature types.

[[Next Tasks]] lists what is open. The cheapest decisive items are runtime
arms (CAP-010 acceptance, FMV without `mpeg`, a read-only Training arm for
Flik's action states); each needs a launch the user approves, with
`make session-audit` before and after.

## Research status by subsystem

Status words follow [[Subsystem Coverage Map]]: **Mapped** (a bounded PC model
with static and runtime evidence), **Bounded** (real PC evidence at a
documented boundary, major parts open), **Touched**, **Untouched**. That map
holds each row's anchors and top open question; this table is a digest.

| Subsystem | Status | Confirmed, in brief | Main evidence |
|---|---|---|---|
| Startup and renderer selection | Mapped | Entry `0x004B1670`, capability selection `0x0041F990`, chooser `0x004A7600`. Retail has no native Direct3D argument; a derived auto-hardware build boots straight into Direct3D | [[EXP-20260816-143 - Automatic Direct3D startup static audit]], [[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]], [[EXP-20260816-151 - Independent auto-hardware runtime audit]] |
| Media root, CD gate, file loading | Mapped | CD sentinel `0x00403B90`, root selector `0x004ADC30`, whole-file loader `0x004AE240`; content families and loaded paths censused | [[EXP-20260811-004 - Wine launch and CD sentinel gate]], [[PC Content Census]], [[PC level roster and numbering]] |
| `LEVEL*.DAT` | Mapped | Scene records and payload targets (M1); type-`0x3F` and type-1 tables; the type-`0x41` static mesh decoded over all 2,543 retail payloads; the type-indexed list table is written only by the DAT walk `0x0044BB70` after an unconditional clear | [[PC LEVEL DAT prefix]], [[PC LEVEL DAT static mesh]], [[EXP-20260818-006 - R0 the static mesh format and where visible ground lives]], [[EXP-20261018-011 - Type-indexed list table writers and readers]] |
| `LEVEL.RAW` | Bounded | Packet codec modelled on `0x0049A200`; every original level's type-35 creature table, `0x102` packets and texture pages decoded; 4-bit page palette rows reproduce a live index buffer byte for byte; tags `0x101`/`0x102` match no loader branch | [[EXP-20260927-001 - Complete original level Blender maps]], [[EXP-20261018-009 - Four-bit page palette rows]], [[EXP-20261018-010 - Two inert data items]] |
| Resource binding (`.ALL`, `.ANM`) | Bounded | Character loader `0x00445020` names a file for each creature type 1–41; `.ANM` first-level walk bounded; no proven edge yet from a placement record to a resource identity (`KU-023`, M2 deferred) | [[PC ANM inspector]], [[PC ANM first-level]], [[EXP-20261012-006 - Creature types from the character loader]], [[EXP-20260813-059 - Independent M2.41 disposition hard-truth audit]] |
| Scene rendering and Direct3D | Bounded | Batch builders `0x00405FE0`/`0x00407450`, transform `0x0045A7F0` (narrows transformed camera coordinates to signed 16 bits, so far geometry can wrap to the other side); no `SetRenderState` call touches the depth states, so the device default applies; visible-ground causality from the R2 runtime track stayed inconclusive | [[EXP-20260813-042 - Per-record Direct3D append discriminator]], [[EXP-20260916-011 - Terrain camera range guard for horizontal bands]], [[EXP-20261018-008 - Direct3D render states and the depth rule]], [[EXP-20260820-005 - R2p task lifecycle diagnostic]] |
| Collision and terrain height | Mapped | `TERRAIN.ALL` parsed; height query `0x004AC460` delegates to `0x004ACA60` (both Inferred, high confidence); original instructions respond to real triangles and separate X/Z barrier segments at the tested boundary (`KU-080` narrowed); plant-state collision and the mushroom bounce bounded | [[PC TERRAIN ALL barrier strips]], [[EXP-20260816-141 - Engine-faithful terrain height and gate standoffs]], [[EXP-20260904-002 - Retail collision admission and separate XZ barriers]], [[PC seed and mushroom collision state]] |
| Reset placement | Mapped | `0x00432930` selects type-1 rows; Level03 row 6 shown causally | [[EXP-20260815-116 - Level03 type-1 row discriminator]], [[EXP-20260816-153 - M5 entry gate and type-1 reset placement resolver]] |
| Triggers and grain gates | Bounded | Twelve confirmed Tunnels/City Entrance mechanisms (`0x00432B30`, `0x00433790`, `0x00416580`); thresholds and standoffs measured; global family exclusivity is Inferred | [[PC grain gate requirements]], [[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]], [[EXP-20260816-171 - Independent M5.8 grain-gate resolver audits]] |
| Collectibles, counters, HUD | Bounded | Pickup walker `0x00417720`; grain count `0x0059D9B1`; Training letters and `FLIKFLIK`; four telescope hide flags `0x00599C68`–`0x00599C6B` | [[EXP-20260814-111 - Training 51st grain collectible vertical slice]], [[EXP-20260818-003 - Runtime reset and grain-gate captures with the flight recorder]], [[EXP-20261018-012 - Telescope hide flags]] |
| Player movement and animation | Bounded | Position globals `0x0059D910`; controller `0x0043F9E0`; equipped berry selector `0x0059D9A7`; every Flik animation mapped to its action state statically; movement state 4 is a hover, dive and ground pound; frames last at least 32 ms (31.25 fps cap) | [[STRUCT-PC-FLIK-POSITION-GLOBALS]], [[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]], [[PC Flik animation catalog]], [[EXP-20261012-005 - Flik movement state 4 ground pound]], [[EXP-20261018-007 - Frame wait rounding]] |
| Input | Bounded | DirectInput keyboard and joystick bring-up `0x0042F350`; per-frame read `0x0042EBC0` reduces to action bits at `0x00598B10`; the controls screen `0x00430DF0` labels every bit and cannot rebind Return (static); its key mapping was confirmed live | [[EXP-20260817-184 - Third independent input census audit]], [[EXP-20261018-006 - Controls configuration screen and action bits]], [[EXP-20261018-013 - Options screens and the creature gate live]] |
| Camera | Bounded | View chain from `0x0041ADF0` to matrix `0x005B58E0`; `0x0059A5EE` is the scripted-camera flag, which also hides the HUD | [[PC camera view-transform chain]], [[EXP-20260816-165 - Independent PC view-chain correction audit]], [[EXP-20261012-003 - Scripted camera flag census]] |
| Creatures and AI | Bounded | 64-slot pool at `0x0059B628` (stride `0x84`), builder `0x0041C420`, update `0x0041EC40`, word-code VM `0x0041DC60`; all 41 types named; no retail row overflows an index; the VM runs as decoded in saved samples of two slots; modes, handlers and event sounds read; off-screen regular enemies stay frozen (live); homing targets the nearest on-screen actor | [[EXP-20260816-172 - PC creature actor pool and behaviour VM census]], [[EXP-20261018-001 - Creature row index census]] to [[EXP-20261018-004 - Creature type handlers and opcode-11 subroutines]], [[EXP-20261012-004 - Homing target visibility bit]] |
| Event registry | Bounded | 16-slot callback table at `0x005982B0`, not a VM (its census closed unaccepted, so re-derive its addresses before use); only WINDOWS (window, message pump) and DIRECTX (renderer, input, sound) register, in 579 saved logs | [[EXP-20260817-185 - PC event subsystem static census]], [[EXP-20261018-005 - Event callbacks and registrations]] |
| Audio and speech | Bounded | DirectSound bring-up `0x004A3480`, track table `0x00596528`; Mr Soil's lessons are PCM files with a file-replacement mechanism (audible acceptance open); Flik's event voices mapped; creature events play named bank samples | [[EXP-20260816-159 - PC audio subsystem static census]], [[EXP-20260909-005 - PC Mr Soil dialogue mechanism]], [[EXP-20260910-005 - Flik event voice mappings]] |
| FMV | Bounded | The `mpeg` word disables FMV; the player uses DirectShow `AMMultiMediaStream` on MPEG-1 `.BUG` files | [[PC FMV playback]] |
| Menus and level flow | Bounded | Level select `0x00443B40`; Options_Scr `0x00441D20` opens the controls screen; `NextLife` `0x0059A5B0` and the level-done log line; pause and save screens unmapped | [[EXP-20261018-006 - Controls configuration screen and action bits]], [[PC autonomous game control]] |

**Original content.** Every original level has a Blender reference map with
its creatures, pickups and texture pages ([[PC original level Blender maps]],
[[PC original Training Blender mapping]]). The Anthill scenery is censused
statically ([[PC Anthill remaining object inventory]]), and the unused disc
items (`COPYOFLE.RAW`, `TEST`, `PLANT12`) were checked offline
([[EXP-20261012-007 - Unused disc content checked offline]]).

## Modification requirements

What the original engine requires, permits or limits when its files or code
change, with the proof edits that established it:

- **Whole-file replacement and release (M4, M6).** Exact manifests, sparse
  overlays, receipts and clean-copy restoration on derived copies only
  ([[M4 Exact Whole-file Replacement]], [[M6 Toolkit Release]]).
- **Scene records (M1).** Guarded target rebinds and record edits in
  `LEVEL.DAT` ([[M1 Tool Support Matrix]], [[LEVEL DAT modding vertical slice]]).
- **Asset swaps.** Same-layout `.ANM` and same-size paired plant swaps are
  accepted (no visible change at the tested start camera), and a character
  `.ALL` swap shows one bounded render link
  ([[EXP-20260812-018 - Same-layout PC ANM replacement]],
  [[EXP-20260812-019 - Same-size paired plant replacement]],
  [[EXP-20260812-033 - Character ALL replacement visible outcome]]).
- **Gameplay proofs (M3).** A 51st Training grain, duplicate FLIK letters,
  `FLIKFLIK`, a moved Level03 reset row and modified grain-gate thresholds
  ([[Training 51-grain vertical slice]],
  [[Training FLIK letter transformations]],
  [[Training FLIKFLIK HUD and completion]],
  [[Level03 type-1 row discriminator]], [[PC grain gate threshold mod]]).
- **Terrain and collision edits.** Barrier grammar and translated barriers,
  floor translation with its visible-ground companion, the inherited depth
  offset byte, face subdivision and diagonals for depth order, wall texture
  regions and tiling
  ([[EXP-20260904-003 - Barrier grammar and landing-seeded grounded movement]],
  [[EXP-20260904-005 - Raised floor and visible ground pairing]],
  [[EXP-20260904-008 - Block depth offset runtime comparison]],
  [[EXP-20260905-001 - Box top diagonal live comparison]],
  [[EXP-20260905-005 - Original wall texture regions and colour inputs]],
  [[PC terrain visibility growth checklist]]).
- **Render distance and visibility.** Sampled pop-in is polygon depth
  rejection; scene visibility bounds and doubled distances, with their
  frame-rate cost
  ([[EXP-20260907-009 - Mushroom render distance diagnosis]],
  [[EXP-20260911-013 - Twofold distance and Training performance]],
  [[PC scenery render distance]], [[PC general render distance]]).
- **Capacities and pools.** Native density, plant capacity, actor selector and
  pool limits ([[PC level authoring memory limits]],
  [[EXP-20260907-025 - Native density limits and terrain refinement trial]],
  [[EXP-20260908-001 - Plant capacity and collision workspace repair]],
  [[EXP-20260908-012 - High-slot seed interaction and native pool limit]]).
- **Placing native content.** Type-35 creature rows, collectibles and the
  end-of-stage marker ([[EXP-20260908-020 - Native enemy placement and scattered Blender population]],
  [[EXP-20260908-021 - Native collectibles and Blender placement]],
  [[EXP-20260909-001 - Native end-of-stage marker and Blender placement]],
  [[PC native creature transplant]]).
- **Speech and signs.** The PCM lesson-file replacement mechanism (audible
  acceptance open), Soil's throw-count boundary and the sign image frames, each
  bounded as its note states ([[PC Mr Soil dialogue replacement]],
  [[EXP-20260910-006 - First Soil throw count boundary proof]],
  [[EXP-20260910-008 - Replaceable Soil sign images]]).

[[Implementation MOC]] indexes the procedures.

## Tooling and gates

- **Static.** Ghidra exports with `scripts/ghidra-query.py`; read
  [[Ghidra export structure and caveats]] first. A census of a global's
  writers and readers also needs a raw scan of the executable sections
  ([[Decision Log]] 2026-10-12, [[EXP-20261012-001 - REA Ghidra analysis trial]]).
- **Runtime.** [[PC autonomous game control]] is the authoritative procedure.
  The session tools ([[Session control plane]]) are fixture-validated only
  (CAP-010); `game-memory`'s read, snapshot and restore are live-validated
  ([[EXP-20260817-188 - Live game-memory read save restore validation]]).
  Input movies, the coordinate overlay and the flight recorder have their own
  bounded acceptance ([[PC input movies]], [[PC coordinate overlay]],
  [[Flight Recorder]]).
- **Evidence.** Saved samples from a derived build count as runtime evidence
  for retail only after the sampled path is compared byte for byte with retail
  ([[Decision Log]] 2026-10-18). [[Agent evidence and query tooling]] covers
  run indexing and receipts. A local Kev classifier is an advisory pilot only
  ([[EXP-20261007-001 - Local Kev evidence classification probe]]).
- **Regression.** `make check` is the gate. R2p and R2q tests are opt-in
  through `pytest.ini`; R2c–R2o stay in the default run ([[Decision Log]]
  2026-10-12).

## Historical record

[[Current State Archive]] keeps the dated packet chronology moved out of this
note. [[Current State history through 2026-09-26]] preserves the pre-review
note. [[Session Index]] indexes original records. Historical permissions and
process IDs do not carry forward.
