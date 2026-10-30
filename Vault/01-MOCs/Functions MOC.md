---
type: moc
updated: 2026-10-29
tags: [moc/functions]
---

# Functions MOC

Function dossiers live in `Vault/20-Research/Functions/` and use [[Function]].

## 2026-10-18 frontend and sprite dossiers

- [[FUNC-97C95BA5572D-00441D20]] — Options_Scr (its own log name), opened from the level select's position 0; first row opens the controls screen
- [[FUNC-97C95BA5572D-00430DF0]] — controls screen "define keys"/"define buttons": 14 items label every input action bit (KU-070)
- [[FUNC-97C95BA5572D-00403A10]] — timed frame on atlas sprite `0x7D` (pickup 8, creature event 7); `0x004037F0` animates `0x7C`/`0x7D` like eyes and mouth (KU-072 closed)

## Initial PC-native dossiers

- [[FUNC-97C95BA5572D-004B1670]] - runtime entry dispatch
- [[FUNC-97C95BA5572D-0041F990]] - machine/device capability probe candidate
- [[FUNC-97C95BA5572D-004A7600]] - renderer-choice screen candidate; defaults
  to selector 1/software after performing shared display initialization, with
  the paired static auto-confirm boundary recorded in EXP-143
- [[FUNC-97C95BA5572D-004129A0]] - `candidate_fmv_playback` (renamed 2026-10-02 from the main-loop candidate; its only caller is the video mapper `0x00412F20`)
- [[FUNC-97C95BA5572D-004AE240]] - file-into-buffer loader candidate
- [[FUNC-97C95BA5572D-004B8B50]] - probable CRT open wrapper
- [[FUNC-97C95BA5572D-00411D00]] - DirectDraw resolution setup candidate
- [[FUNC-97C95BA5572D-00423A20]] - Direct3D device setup candidate
- [[FUNC-97C95BA5572D-004119E0]] - selector-2 Direct3D renderer-state
  initializer candidate
- [[FUNC-97C95BA5572D-0049C520]] - selector-1 native-software renderer
  initializer and `0x80`-stride arena owner
- [[FUNC-97C95BA5572D-0049C3F0]] - selector-1 software-window setup helper

## Startup media selection

- [[FUNC-97C95BA5572D-00403B90]] - startup `cd.txt` sentinel gate
- [[FUNC-97C95BA5572D-004ADC30]] - content-root/CD-drive selector

## Level data

- [[FUNC-97C95BA5572D-0044BB70]] - candidate `LEVEL*.DAT` fixup
- [[FUNC-97C95BA5572D-0044D430]] - candidate scene visibility/update
- [[FUNC-97C95BA5572D-004498F0]] - candidate scene-record dispatch
- [[FUNC-97C95BA5572D-0045A7F0]] - candidate payload-target renderer
  whose M1 selector-2 path has ten inline Direct3D allocation arms; M2.35
  classifies every builder-facing input and finds no ID-zero header/range
  provenance

## Gameplay collectibles

- [[FUNC-97C95BA5572D-00432B30]] - candidate internal-Level03/Tunnels
  nine-row grain-gate update; exact resident/template requirements and linked
  rows 0/4 are bounded in EXP-136; row 3's modified threshold is exercised in
  EXP-137 and independently accepted in EXP-138
- [[FUNC-97C95BA5572D-00433790]] - candidate internal-Level04/City Entrance
  indexed grain-gate update; retail requirements are `(10,20,30)` and modified
  gate 0 is exercised in EXP-137 and independently accepted in EXP-138; all
  three call-site argument tuples are pinned statically in EXP-139
- [[FUNC-97C95BA5572D-00416580]] - candidate planar sar-8 proximity test
  shared through thunk `0x00401A37`; supplies the City gate trigger predicate
  and matches the Tunnels inline distance form (EXP-139)
- [[FUNC-97C95BA5572D-004AC460]] - candidate terrain height cell collector
  behind thunk `0x00401659`; bucket lookup, descriptor/group/cell window
  admission, and the reset consumer's Y source (EXP-141)
- [[FUNC-97C95BA5572D-004ACA60]] - candidate terrain height resolver behind
  thunk `0x00401717`; exact plane formula, winding, floor/ceiling selection,
  and the `+0xC80` output offset (EXP-141)
- [[FUNC-97C95BA5572D-004A9290]] - candidate planar half-plane side test
  behind thunk `0x00401500`; the triangle-containment primitive of the
  terrain height resolver (EXP-141)
- [[FUNC-97C95BA5572D-00456A90]] - candidate type-`0x3F` terrain-height
  initializer with a distinct selector-`0x14` branch
- [[FUNC-97C95BA5572D-00417720]] - candidate type-`0x3F` collectible update;
  PC selector `0x14` consumed-y/counter path is independently runtime-confirmed
  in `EXP-20260814-111`, with exact `49 -> 50 -> 51` branch behavior in
  `EXP-20260814-112`; `EXP-20260814-113` confirms letter selectors
  `0x10`–`0x13`, mask bits `1/2/4/8`, independently consumed duplicates, and
  repeated completion when the mask is already `0x0F`; `EXP-20260815-114`
  gives exact original/appended records independent bits and gates reward on
  only the incomplete-to-`0xFF` transition
- [[FUNC-97C95BA5572D-00416890]] - candidate HUD/status renderer whose decimal
  cache and two-digit path retain/display grain count 51; exact M3.4 redirects
  its four-letter span to centered eight-slot `FLIKFLIK`
- [[FUNC-97C95BA5572D-00442E70]] - candidate level-completion tally containing
  the end-tally cap, completion flag, and bright completion/emblem path; exact
  M3.4 adds complete eight-bit popcount, centered `FLIKFLIK`, and `8/8`
- [[FUNC-97C95BA5572D-00439E90]] - unidentified level/mode update containing a
  literal-50 cap; not reached in the controlled Training transition

## Candidate audio bring-up and track table

- [[FUNC-97C95BA5572D-004A3480]] - creates the DirectSound object, stores it
  at `0x007EDAE8`, and sets ready flag `0x007ECA40` on the success path only
- [[FUNC-97C95BA5572D-0042BB90]] - writes 40 `audio\*.wav` names into the
  8-byte-stride table at `0x00596528` and assembles the track path at
  `0x00596960`

## Candidate death/reset row selection

- [[FUNC-97C95BA5572D-00432930]] - conditional nearest type-1 coordinate-row
  auxiliary/reset-coordinate initializer; EXP-116/117 confirm exact row X/Z
  causality, while EXP-128 proves its `0x0059D960` destination is not current
  airborne position; natural producer semantics remain open. EXP-153 pins the
  exact scan arithmetic (unsigned count word, `sar`-based row-space distance,
  lowest-index tie-break, 32-bit wrap), proves `0x00437A20` byte-identical,
  and reimplements it in [[PC type-1 reset placement resolver]]
- [[FUNC-97C95BA5572D-0041C6C0]] - address-named collision/reset coordinator
  candidate whose nonzero/non-2 arm sets the selector's `0x10` state bit
- [[FUNC-97C95BA5572D-004A8410]] - candidate terrain source-descriptor loader;
  maps `0x4C`-byte source records into `0x30`-byte runtime descriptors
- [[FUNC-97C95BA5572D-004A8950]] - candidate collision-bounds initializer over
  descriptor tags 6/7/8 and their bounded group payloads
- [[FUNC-97C95BA5572D-004ACF90]] - candidate current collision result reader;
  returns signed runtime descriptor word `+0x2E`

## Event registry

- [[FUNC-97C95BA5572D-0042DB10]] - registers a 60-byte event record into slot
  `id`, destroying any occupant first and calling the create callback last
- [[FUNC-97C95BA5572D-0042D980]] - dispatch pass: calls the `+0x08` callback
  of every in-use slot
- [[FUNC-97C95BA5572D-0042BA60]] - `"DIRECTX"` create callback: base CD track
  from `cd.txt`, then DirectSound, three unidentified calls and DirectInput
  (dossier added 2026-10-02)
- Census and boundary:
  [[EXP-20260817-185 - PC event subsystem static census]]

## Input

- [[FUNC-97C95BA5572D-0042F350]] - DirectInput bring-up: object, keyboard
  device, enumerated joysticks, and the default bindings
- [[FUNC-97C95BA5572D-0042EBC0]] - per-frame keyboard/joystick read and the
  binding walk that produces the action bits at `0x00598B10`
- Census and boundary:
  [[EXP-20260817-181 - PC input subsystem static census]]

## Creature/actor instance pool

- [[FUNC-97C95BA5572D-0041DC60]] - resumable 16-bit word-code interpreter for
  one pool slot; program counter in `+0x70`, dispatch `0x0041E848`, state
  dispatch `0x0041E14F`; 40 programs at `[0x004C7D00, 0x004C83F0)`
- [[FUNC-97C95BA5572D-0041EC40]] - per-frame pass: camera-radius selection into
  the list at `0x0059D7E0`, then per-slot advance and release
- [[FUNC-97C95BA5572D-0041C420]] - builds the 64 slots from the type-35
  `CreatListRam` records; per-type tables `0x0041C600`/`0x0041C5B0`
- [[FUNC-97C95BA5572D-0041BD10]] - source-record to slot initializer, including
  the `+0x70` program pointer
- [[FUNC-97C95BA5572D-0041B9F0]] - reinitialise (mode 1) and release/unlink
  (mode 2); per-type tables `0x0041BC48`/`0x0041BC18`
- Census and boundary:
  [[EXP-20260816-172 - PC creature actor pool and behaviour VM census]]

## Resource loading

- [[FUNC-97C95BA5572D-00416100]] - candidate plant resource-ID collector
- [[FUNC-97C95BA5572D-0041C420]] - candidate `LEVEL.RAW` type-35 table transformer
- [[FUNC-97C95BA5572D-0041BD10]] - address-named retained-source-to-fixed-pool
  record copier; M2.40 proves its first-dword source is the nonzero-gated
  `LEVEL.RAW` byte at source `+0x0C`
- [[FUNC-97C95BA5572D-0041B9F0]] - address-named active-list record remover;
  mode 2 conditionally zeros record `+0x00` when `+0x62 == 0`
- [[FUNC-97C95BA5572D-004317D0]] - dispatcher-case-1 update function with the
  exact fixed slot-25 call and its corrected later `+0x5C`/counter gates
- [[FUNC-97C95BA5572D-00459620]] - generic header-index reader whose ID-zero
  header start test produces the exact slot-25 zero-return outcome
- [[FUNC-97C95BA5572D-004467E0]] - generic header-index retained-entry state
  clearer reached by three state-gated fixed slot-63 calls
- [[FUNC-97C95BA5572D-00446870]] - nonzero-state counterpart reached by the
  fixed slot-63 call whose explicit `I == 0x23` gate excludes zero
- [[FUNC-97C95BA5572D-00444B70]] - candidate `.ANM` first-level relocator
- [[FUNC-97C95BA5572D-00445020]] - candidate scene resource batch loader and
  exact ID-zero Flick-path selector
- [[FUNC-97C95BA5572D-00444C40]] - candidate paired resource coordinator and
  retained-range finalizer
- [[FUNC-97C95BA5572D-00448010]] - candidate `.ALL` first consumer; exact
  `FLICK.ALL` destination bounded in `EXP-20260812-034`
- [[FUNC-97C95BA5572D-00402DC0]] - candidate Flik animation-state update:
  action state `0x0059D998`, 35-row table `0x004C1CE8` (EXP-20261001-002)
- [[FUNC-97C95BA5572D-00445FF0]] - candidate `.ANM` pose sampler; slot-record
  grammar confirmed (EXP-20261001-002)
- [[FUNC-97C95BA5572D-0044C440]] - candidate direct ID-zero retained-entry
  consumer before M1 record enumeration
- [[FUNC-97C95BA5572D-00448350]] - unknown generic header reader over the
  prebuilt `0x0059D7E0` object list; sole generic-reader candidate in the M1
  coordinator closure, called before its record root load and enumeration
- [[FUNC-97C95BA5572D-0044F8E0]] - candidate retained-entry stream consumer;
  selector 1 shares a software output arena with the positive-target renderer,
  while selector 2 reaches the Direct3D batch builders below
- [[FUNC-97C95BA5572D-00405FE0]] - candidate selector-2 four-input Direct3D
  batch builder; its exact successful count write adds four vertices after six
  indices, and M2.29 selects only exact record `0x0A6C` outside both fresh
  controls; M2.30 maps its 12 differences to four post-admission inputs and
  none to an admission decision; M2.31 reduces the non-source union to 23
  physical locations and the exact mode-2 rejection chain to 12 logical
  slots; M2.32 fixture-validates the purpose-specific evaluator and payload-
  free receipt; M2.32 then measured three live first-reject/pass outcomes and
  M2.33 measured one accepted reject/pass/reject sequence
- [[FUNC-97C95BA5572D-00407450]] - candidate selector-2 three-input Direct3D
  batch builder; its exact successful count write adds three vertices after
  three indices, while its three older single-record outcomes do not reproduce
  in the fresh M2.29 arms
- [[FUNC-97C95BA5572D-00446970]] - unknown state-gated shared-entry consumer
- [[FUNC-97C95BA5572D-0044CA00]] - unknown bounded per-resource entry-range
  consumer; M2.38 classifies four zero-only writer paths and sole nonzero
  writer `0x00467E60`, whose positive 20-entry table has no signed `-103`;
  the candidate is retired
- [[FUNC-97C95BA5572D-00467E60]] - `candidate_plant_constructor` (renamed
  2026-10-02); sole nonzero writer for the 20
  exact selector words; consumes a fixed `0x84`-stride pool before the M1
  coordinator on the normal update route
- [[FUNC-97C95BA5572D-00465030]] - candidate `LEVEL.RAW` packet parser

## 2026-08-15 reset consumer confirmation

- [[FUNC-97C95BA5572D-00432930]]: nearest type-1 row X/Z consumer, confirmed by control/candidate runtime delta.
- [[FUNC-97C95BA5572D-0041C6C0]]: natural first-pit value-1/flags-`0x14`
  boundary confirmed; complete argument semantics and natural row-6 selection
  remain open.

- [[EXP-20260815-117 - Approved Level03 row-6 reset rerun]] - approval-compliant
  runtime discriminator for [[FUNC-97C95BA5572D-00432930]], plus bounded
  natural-producer evidence for [[FUNC-97C95BA5572D-0041C6C0]].
- [[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]] -
  ordinary descriptor-572/value-1 pit events join `0x0041C6C0` to the repeated
  nearest-row-7-like reset at `0x00432930`.
- [[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]] -
  maps descriptor 572 as the sole rows-6/7 result-1 region and corrects the
  earlier scanner's one-descriptor coordinate shift.
