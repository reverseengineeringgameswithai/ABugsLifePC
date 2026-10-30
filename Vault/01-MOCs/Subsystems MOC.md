---
type: moc
updated: 2026-10-29
tags: [moc/subsystems]
---

# Subsystems MOC

Subsystem dossiers were planned for `Vault/20-Research/Subsystems/`, which is still empty; they live in `Vault/20-Research/` and `Vault/40-Implementation/` instead. No complete game subsystem is confirmed; [[Subsystem Coverage Map]] gives each row's bounded PC status.
Subsystem selection is gated by [[Project Roadmap#M3 — Gameplay and level-logic systems]]
(M3 is now complete; [[Project Roadmap#Roadmap status]] has current milestone status).

This note indexes the PC evidence we **have**. For the complementary view —
which subsystems exist to be solved at all, and which have no PC evidence yet
— see [[Subsystem Coverage Map]].

## Plant collision, Anthill objects and lesson audio

- [[PC seed and mushroom collision state]] / [[EXP-20260906-007 - Plant-state collision regression]] - separate type11 seed collider, type5 mushroom/source8 transition, and contact-dependent -3328 bounce; minimal template restoration confirmed native/live.

- [[PC Anthill tree and mound authoring]] — original tree composition, mound records and native collision admission windows.

- [[PC Mr Soil dialogue replacement]] / [[EXP-20260909-005 - PC Mr Soil dialogue mechanism]] — 14 PCM lesson files, native cue/stage/length evidence and the 40-slot census correction.

## Gameplay, frontend, audio and modification rules

Engine notes whose evidence was first gathered in test builds; each cites its
experiments and states its own confidence.

- [[PC gameplay loop and player event sites]] — outer loop `0x0043DA40`, one
  gameplay frame, Flik's record and the single native sites for jumps, throws,
  hits, deaths, letters and seed tokens.
- [[PC level start, special slot and load screen]] — carousel to engine index,
  the special index-16 slot and the level start `0x0042E5C0` load screen.
- [[PC results screen and level select internals]] — results loop layout,
  sprite draw order and the level-select carousel.
- [[PC save record and medal bytes]] — save/load routines, the `0x004D8428`
  record and per-level medal bytes.
- [[PC projectile records, homing and kill accounting]] — the shared 64-record
  pool at `0x00598CA8`, aim and homing, and berry-versus-enemy `0x00429790`.
- [[PC boss level routines and creature transplant limits]] — what a creature
  row carries, native boss placements and the level routines that run fights.
- [[PC sound banks and per-level audio routing]] — per-level sound bank
  selection, sample paths, streamed tracks and replacement requirements.
- [[PC sky, panorama origin and distant pass depth]] — sky and panorama
  routines, the type-36 vertical origin and distant-pass depth.
- [[PC telescope camera paths]] — telescope trigger, the DAT camera-path
  records and the scripted tour.
- [[PC scene admission and DAT layout rules]] — primary-gate coordinate range,
  object rotation, the end-of-file footer and free texture pages.
- [[PC terrain collision rules for modified levels]] — units, descriptors,
  barrier strips and the original props that carry collision.

## PC platform initialization leads

- Process entry: [[FUNC-97C95BA5572D-004B1670]]
- Capability and driver selection: [[FUNC-97C95BA5572D-0041F990]]
- Renderer chooser/default and proposed static auto-confirm boundary:
  [[FUNC-97C95BA5572D-004A7600]],
  [[EXP-20260816-143 - Automatic Direct3D startup static audit]], and
  [[PC automatic Direct3D startup candidate]]
- Loop/display transition: [[FUNC-97C95BA5572D-004129A0]]
- File access: [[FUNC-97C95BA5572D-004AE240]] and [[FUNC-97C95BA5572D-004B8B50]]
- DirectX display/device setup: [[FUNC-97C95BA5572D-00411D00]] and [[FUNC-97C95BA5572D-00423A20]]

## Media and content-root selection

- CD sentinel gate: [[FUNC-97C95BA5572D-00403B90]]
- Drive/root selector: [[FUNC-97C95BA5572D-004ADC30]]
- Whole-file loader: [[FUNC-97C95BA5572D-004AE240]]
- Runtime evidence: [[EXP-20260811-004 - Wine launch and CD sentinel gate]]

## Resource loading

- Metadata inventory and observed paths: [[PC Content Census]]
- Evidence packet: [[EXP-20260812-014 - PC content census and loader context]]
- Caller/consumer trace: [[EXP-20260812-015 - Plant pair caller and consumer trace]]
- Whole-file loader candidate: [[FUNC-97C95BA5572D-004AE240]]
- Active trace set: shared `CD/PLANTS/PLANT{04,05,06,10}.{ANM,ALL}`
- Plant-ID collector: [[FUNC-97C95BA5572D-00416100]]
- Batch/pair path: [[FUNC-97C95BA5572D-00445020]] and
  [[FUNC-97C95BA5572D-00444C40]]
- `.ALL` first consumer: [[FUNC-97C95BA5572D-00448010]]

The paired plant basenames share a confirmed coordinating call path and
distinct immediate consumers. Complete format semantics and the M1 dependency
bridge remain unconfirmed.

## Audio and input bring-up

- DirectSound bring-up: [[FUNC-97C95BA5572D-004A3480]] (object `0x007EDAE8`,
  ready flag `0x007ECA40`, enumeration callback `0x0049DD00`)
- Track-name table `0x00596528` and its builder:
  [[FUNC-97C95BA5572D-0042BB90]]; assembled path buffer `0x00596960`
- `DSStream` token parser `0x0042C130` (`EXP-20260816-143`); the only
  `DSStreamWndClass` reference is the `UnregisterClassA` cleanup at
  `0x0042C3B0` inside it
- Indirect dispatch record `0x004D81E8` (`"DIRECTX"`): thunks to
  `0x0042BA60`, `0x0042BB30`, `0x0042BB50`. `EXP-20260817-185` identifies it as
  an **event record** — the leading `3` is the event id, not a count — and
  `0x0042BA60` as its create callback — the slot called at `0x0042DC2A`, a static
  path rather than an observed call; that is the
  missing caller this census recorded as absent
- RIFF `mmio` cluster `0x004AD000`-`0x004ADB20`, able to author chunks as well
  as read them
- Input creation `0x0042F350`, brought up beside audio by `0x0042BA60`
- Census and boundary: [[EXP-20260816-159 - PC audio subsystem static census]]

## Player berry throw

- Runtime reconnaissance:
  [[EXP-20260817-187 - Runtime berry throw reconnaissance]]
- Throw action bit `0x8000` (`DIK_LCONTROL`), observed live in `0x00598B10`,
  `0x00861C98` and `0x00861C8C`
- Input latch `0x00464E10`-`0x00464E2F`: current -> previous, then reload
- Throw-exclusive projectile pool, stride `0x38`, consistent with 64 records
  over `[0x00598C00, 0x00599A00)`; no absolute static references
- Not the creature actor pool; `+0x2C` is not the visible colour
- Berry-type selector: static candidate `0x0059D9A7` (values 0-4, pickup-kind
  switch `0x20`-`0x24`, accumulator `0x00599B20[row*5+type]`) in
  [[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]];
  `KU-073` open pending the read-only labelled A/B. Resolved 2026-08-18:
  [[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]]
  confirms `0x0059D9A7` as the equipped berry-type selector on PC. Earlier cross-port shape in
  [[XPORT-20260817-005 - Berry contact array and type marker shape]]

## Event registry

- Census and boundary:
  [[EXP-20260817-185 - PC event subsystem static census]]
- Table `[0x005982B0, 0x00598670)`, 16 records, stride `0x3C`; `0x005982AC` is
  written with the current record pointer and never read; `0x00598670` is a
  buffer whose first 128 bytes are zeroed, passed as a log vararg
- Record: id word `+0x00`, create `+0x04`, `+0x08` (unnamed — no log string
  describes it), destroy `+0x0C`, name `+0x10` (32 bytes by adjacency, not by
  any decoded width), in-use flag `+0x34`. `+0x00` and `+0x10` survive every
  clear; the id is never bounds-checked
- Table geometry, record layout, **7 of the 9 reachers** (in the three
  `thunk_FUN_` entries' `callers` lists) and the `0x004ADEA0` reading (it writes
  `"bugs.log"`, reaching `KERNEL32.dll!DeleteFileA` through `0x004B13E0`; body
  gated on `0x008620AC`) are all in `ghidra-evidence.json`; re-derived, not
  first found, by `EXP-20260817-185`. New there: the four dead entry points (no ghidra entry at
  all), the two omitted reachers `0x004AE863` and `0x004121A1`, the decoded
  records, the relocation result of §2.1 (a negative on the absolute addressing
  form only — **not** a closure proof; and found by the second-round audit, not
  by this census), the disjointness test and
  the negatives
- Register [[FUNC-97C95BA5572D-0042DB10]]; dispatch pass
  [[FUNC-97C95BA5572D-0042D980]]; destroy-all `0x0042DA70`
- Dead entry points: `0x0042D950`, `0x0042D9D0`, `0x0042DA00`, `0x0042DCA0` —
  each reached only through a thunk (`0x0040169F`, `0x0040179E`, `0x00401217`,
  `0x00401140`) that itself has no callers
- Two static registration call sites, `0x0043DAF5` and `0x0043DB10`, in an
  unanalysed enclosing function — whether either executes is not established:
  `0x004D81A8` `"WINDOWS"` and `0x004D81E8` `"DIRECTX"`
- Cross-link: `0x0042BA60`, the audio/input bring-up whose missing caller
  `EXP-20260816-159` recorded, is the `"DIRECTX"` event's create callback

**Not a VM and not a trigger stream** — a callback registry, and disjoint from
the creature script machinery by address in both directions. Static only; no
callback has been observed run, and none is named beyond where it is called
from, until `KU-071` is answered.

## Input

- Census and boundary:
  [[EXP-20260817-181 - PC input subsystem static census]]
- Bring-up [[FUNC-97C95BA5572D-0042F350]] (`0x0042F350`-`0x0042F565`), from
  `0x0042BAED` in `0x0042BA60`
- Object `0x00598B18`; keyboard device `0x00598B20`; ready flags
  `0x00598BC8` and `0x00598B1C`
- `GUID_SysKeyboard` `0x004C0230`; `IID_IDirectInputDevice2A` `0x004C0220`;
  `c_dfDIKeyboard` `0x004AFE90`; `c_dfDIJoystick` `0x004AEE70`
- Enumerated joystick GUIDs `0x005987D0` (`0x10` stride), devices
  `0x005988D0`, acquired flags `0x00598B28`, count `0x00598B14`
- Per-frame read [[FUNC-97C95BA5572D-0042EBC0]] (`0x0042EBC0`-`0x0042EEBB`),
  from thunk `0x00401B5E` at `0x00464E1C` and `0x0049BDB7`
- Keyboard state `0x00598A10` (256 bytes); joystick-0 state `0x00598B60`
  (`DIJOYSTATE`, 80 bytes); action bits `0x00598B10`; synthesised axes
  `0x004F0440`/`0x004F0444`
- Binding table `[0x004D8430, 0x004D8490)`, zero in the image, written by
  `0x0042F0F0` from two call sites **and** from a `0x18`-stride configuration
  array at `0x004D9CF9` by blocks at `0x00430C3F` and `0x00431022`, with
  `0x00430B10` copying the live table back and a dispatcher at
  `0x00430FF6`/`0x00430FFD` selecting apply-vs-defaults — so the controls are
  configurable, though only the `0x00431022` block is demonstrably live
  (`0x00430C3F`'s thunk `0x00401DF2` has zero call sites); joystick button pairs `[0x004D8490, 0x004D84D0)`, also written
  at `0x0042F250`
- Second, disjoint path: `GetAsyncKeyState` reached only by a register load at
  `0x004A7841` in chooser `0x004A7600`; its import thunk `0x004AEB1C` is dead
  code (prior art: [[PC autonomous game control]])

Static only. No device was observed created or acquired, no frame observed,
and no action bit is given a control name until `KU-070` is answered.
Later evidence names two bits: [[EXP-20260817-187 - Runtime berry throw reconnaissance]]
observed throw bit `0x8000` (left Ctrl) live in `0x00598B10`, and
[[EXP-20260907-028 - Representative update and render headroom]] /
EXP-20260930-004 tie jump bit `0x4000` to left
Shift through `0x004D8458`. `KU-070` stays open for the rest.

## Creature/actor instance pool and behaviour VM

- Census and boundary:
  [[EXP-20260816-172 - PC creature actor pool and behaviour VM census]]
- Instance pool `[0x0059B628, 0x0059D728)`, 64 slots, stride `0x84`
- Level-supplied source records `[0x00599EB0, 0x0059A5B0)`, 64 × `0x1C`,
  copied at `0x0046574D` from loader record type `0x23`
  (`LOAD: Type 35, CreatListRam.`, string `0x004DE2FC`)
- Builder `0x0041C420`, called once from `0x004679A0` inside level-load
  `0x004671D0`, gated on bit `0x10` of `0x005C5E88`
- Slot initializer `0x0041BD10`; release/reinitialise `0x0041B9F0`
- Per-frame update `0x0041EC40` (from `0x00414597` in `0x004144C0`);
  camera-radius activation list `0x0059D7E0`
- Type id domain 6..41, shared by the builder switch (`0x0041C600` /
  `0x0041C5B0`) and the release switch (`0x0041BC48` / `0x0041BC18`)
- Word-code interpreter `0x0041DC60`-`0x0041E845` (its only `ret` at
  `0x0041E7D3` is not the end); program counter in slot
  `+0x70`; opcode dispatch `0x0041E848` (opcodes `-1`..`24`); state dispatch
  `0x0041E14F` (`0x0041E8F4` / `0x0041E8D4`); per-type handler invoked by
  `call eax` at `0x0041E7C7` through slot `+0x7C`. The tail implementing the
  five modes is **not** analysed
- Forty programs `[0x004C7D00, 0x004C83F0)` behind pointer table `0x004C83F0`;
  frame-sequence table `0x004C8758`
- Shared byte cursor `0x00599C60`, initialised to the `rand.dat` buffer
  `0x0081B428`

Static only. No slot was observed live, no creature identity is assigned to
any type id, and nothing here licenses a runtime or per-type behaviour claim
until `KU-068` has its read-only receipt.
(2026-10-18: `KU-068` now has that receipt for two slots, from samples
saved by earlier hardware arms:
[[EXP-20261018-002 - Creature script counter in saved runtime samples]].
[[EXP-20261012-006 - Creature types from the character loader]] names the
types, and [[EXP-20261018-001 - Creature row index census]] shows which
rows run their script and which lists they walk.)

Independently accepted with zero defects in
[[EXP-20260817-180 - Eighth independent creature census audit]] after seven
rejections and corrections.

## Camera/view-transform candidate

- Corrected worker packet:
  [[EXP-20260816-164 - PC view-chain correction and coverage reclassification]]
- Independent acceptance:
  [[EXP-20260816-165 - Independent PC view-chain correction audit]]
- Bounded dossier: [[PC camera view-transform chain]]
- Flik-relative updater `0x0041ADF0`; selector/copy function `0x0041B7D0`
- Common position/angle block `0x00599C90`; consumer `0x00455710`
- Generated matrix `0x005B58E0`, origin `0x005BDB8C`, renderer consumption at
  `0x0044D4C1`/`0x0044D4F0`
- Scratch-matrix loader `0x004636C0`; local builder transform begins
  `0x0040605F`

The structural PC data flow and Bounded coverage disposition are independently
accepted at clean subject commit `0336d14`. Ordinary-follow and
scripted-source roles are Inferred; controls, selector meaning,
second-consumer semantics, and runtime frequency remain Unknown under KU-066.
On 2026-09-15 EXP-20260915-005 confirmed
the selector's role within the telescope event only (bit 0 of `0x0059A5EE`
picks the `0x0059A5C0` source); other users stay open.

## Candidate gameplay collectible path

- Type-`0x3F` initialization: [[FUNC-97C95BA5572D-00456A90]]
- Pickup/mask/counter update: [[FUNC-97C95BA5572D-00417720]]
- Grain vertical slice: [[EXP-20260814-111 - Training 51st grain collectible vertical slice]]
- Grain counter/tally boundary: [[EXP-20260814-112 - Training 51 counter and tally boundary]]
- FLIK letter transformations: [[EXP-20260814-113 - Training FLIK letter transformations]]
- Eight-slot HUD/completion: [[EXP-20260815-114 - Training FLIKFLIK HUD and completion]]

The PC Training table has independently confirmed grain and letter-mask paths.
M3.3 proves moved duplicates and exposes repeated completion after mask
`0x0F`; M3.4 gives the exact eight-record design independent bits, one-shot
completion, and centered `FLIKFLIK`/`8/8`. This remains a bounded candidate
subsystem, not a complete or generic inventory/progression architecture.

## Candidate scene rendering path

- Visibility/selection: [[FUNC-97C95BA5572D-0044D430]]
- Record dispatch: [[FUNC-97C95BA5572D-004498F0]]
- Positive target consumer: [[FUNC-97C95BA5572D-0045A7F0]]
- Retained-entry stream consumer: [[FUNC-97C95BA5572D-0044F8E0]]
- Native-software output boundary:
  [[STRUCT-PC-CANDIDATE-HARDWARE-SUBMISSION-RECORD]]
- Direct3D batch builders: [[FUNC-97C95BA5572D-00405FE0]] and
  [[FUNC-97C95BA5572D-00407450]]
- Direct3D batch layout: [[STRUCT-PC-DIRECT3D-BATCH-FAMILIES]]
- Renderer initializers: [[FUNC-97C95BA5572D-004119E0]] and
  [[FUNC-97C95BA5572D-0049C520]]
- Bounded structure: [[STRUCT-PC-LEVEL-DAT-POSITIVE-PAYLOAD-TARGET]]
- Evidence packet: [[EXP-20260812-009 - Training payload target structure and reuse census]]
- Runtime substitution: [[EXP-20260812-010 - Training target rebind visible substitution]]
- Selection-center boundary: [[EXP-20260812-011 - Training record center candidates]]
- Positive visibility bound: [[EXP-20260812-012 - Training record visibility bound]]

These labels identify two PC-static source paths with bounded visible runtime
corroboration. `EXP-20260813-036` proves conditional convergence on one output
arena/list topology while their source pointers remain separate static
lineages. `EXP-20260813-038` finds that arena inactive for every exact
retained-entry call in three Direct3D arms. `EXP-20260813-039` resolves the
former active-hardware contradiction: the arena belongs to selector-1 native
software, while selector 2 reaches separate Direct3D batch storage and an
exact `DrawIndexedPrimitive` edge. `EXP-20260813-040` then bounds selected
Direct3D additions to root `0x004C4108`, page 16, records no selected in-call
flush, and reduces count provenance to exact 13-entry set
`{1,2,4,5,6,7,9,10,14,15,18,19,20}`. `EXP-20260813-041` proves all 145
changed records in those entries reach a selected builder, then narrows the
count-relevant surface to 18 entry/form groups and 124 exact records. Three
single-record append outcomes are exact for those retained arms but do not
reproduce across fresh launches. `EXP-20260813-042` maps exact append and
no-append boundaries, records every candidate outcome in three fresh arms,
and selects only entry 7/file offset `0x0A6C` outside both controls. A complete
rendering subsystem boundary, pixel causality, and placement-to-resource
identity are not confirmed. `EXP-20260813-043` maps all 12 exact record
differences to four post-admission append inputs and proves none distinguishes
admission. `EXP-20260813-044` reduces that exact admission path to a
23-location physical non-source union and 12 ordered logical rejection slots,
then proves existing safe data-watch boundaries can support a payload-free
first-reject receipt. `EXP-20260813-045` completes M2.32's offline evaluator/
fixture gate; its live first-reject phase remains separately authorized.

## Level01 terrain coverage and ramp visibility, 2026-09-05/06

- [[EXP-20260905-007 - Retail position control and missing floor footprints]]: retail RAM control and selected active-floor coverage differences after source-99 replacement; exact earlier fall and invisible-ground face mapping remain open.

- [[EXP-20260905-008 - Whole-Level01 collision and render coverage audit]]: complete Level01 edit inventory confirms source 99 alone replaces 134 original cells with 14 authored cells; 7,147 cells and all barriers are unchanged. Render mesh 160 alone changes but covers a different footprint.

- [[EXP-20260905-009 - Additive terrain preservation and access ramp]]: final 224/224 terrain gate; native preservation, relocation, command traversal, fall/box checks and four continuous-crossing/return routes pass. Exact-point controller failures retained and diagnosed. Evidence: `reports/terrain/EXP-20260905-009-validation.json`.

- [[2026-09-06 - Codex - Additive runtime startup]]: the EXP-009 build reached the hardware/LevelSelect log gates; a title-guard mismatch stopped input (`reports/terrain/EXP-20260905-009-runtime.json`). The continuation loaded EXP-009 in Level01 with resident collision/render identity verified read-only (`reports/terrain/EXP-20260905-009-runtime-entry.json`).

- 2026-09-06 EXP-009 ramp visibility: successful collision crossings, but camera-dependent disappearance/reappearance is reproduced with a fixed post-tap position and appended-cell contact 49008. [[2026-09-06 - Codex - Ramp visibility reproduction]]; `reports/terrain/EXP-20260905-009-ramp-visibility.json`.

- 2026-09-06 EXP-009 culling discriminator: original instructions reject mesh 160 at `0x0044D677` for two hidden views; offline radius 8192 admits all five sampled poses, but an intermediate visually unclear sample already passes with 6047. [[2026-09-06 - Codex - Ramp culling discriminator]]; `reports/terrain/EXP-20260905-009-ramp-culling.json`.

- 2026-09-06 EXP-009 live radius A/B/A: exact authorized 6047 -> 8192 -> 6047 reversibly changes ramp visibility at fixed actor/camera/contact. Culling contributor confirmed at one pose; original restored, files unchanged. [[2026-09-06 - Codex - Live ramp radius comparison]]; `reports/terrain/EXP-20260905-009-ramp-radius-live.json`.

- [[EXP-20260906-001 - PC-compatible ramp visibility bounds]]: file-only radius 6047 -> 8560, collision/geometry preserved; 73 affected and 72 focused tests pass; native sweep 0/5152 relevant candidate rejections versus 544 control. [[2026-09-06 - Codex - File-based ramp visibility bounds]]. The runtime continuation loaded bound 8560 from file in Level01 with collision/geometry verified read-only, not yet all-view acceptance: `reports/terrain/EXP-20260906-001-runtime.json`.

- [[EXP-20260906-003 - Solid ramp sides and ground contour trim]]: paired wall blocking passes offline; render-contour clipping is a separate appearance discriminator; the fixed-axis control failure is preserved.

- Wall collision versus rendering: in the EXP-003 live check the sides block but a visible model overlap remains. Bounded observation, no universal padding rule; compare original stop clearance and draw order. [[EXP-20260906-003 - Solid ramp sides and ground contour trim]].

- Wall body clearance: [[EXP-20260906-004 - Wall clearance comparison and offset trial]] separates blocking from visible overlap. Nonuniform original collision/render separations support a local trial, not a universal rule; visual ordering and corner/end entry remain open.

- [[EXP-20260906-005 - Isolated authored terrain and platform spawn]]: bounded old scene/collision deactivation, exact authored pieces retained and a private executable-table spawn; 53 affected/72 focused tests pass; native 9 accepted/1 setup failure. See the experiment for offsets and proof limitation.

## Terrain perimeter and original foliage, 2026-09-06

- [[EXP-20260906-006 - Perimeter barriers and original foliage reference]]: original Level01 tall-grass reference at XYZ(292407,-31849,537453), facing979, read-only camera/capture provenance. Original render-to-barrier correspondence and projectile/player equivalence remain unresolved; short-loop candidate is not accepted.

- 2026-09-06 grass/perimeter successor: original-PC source180 segment160 supplies the separate XZ response at the OG reference. The first authored grass boundary blocks Flik live. Visual variation now uses an off-screen original-shape catalogue, not new collision. [[EXP-20260906-006 - Perimeter barriers and original foliage reference]]; projectile equivalence and a synthetic lower-ramp straight-release case remain open.
