---
type: moc
updated: 2026-10-29
tags: [moc/file-formats]
---

# File Formats MOC

File-format dossiers live in `Vault/20-Research/File-Formats/` and use [[File Format]].
Format expansion follows the gates in [[Project Roadmap#M1 — Scene records and reusable payloads]] and [[Project Roadmap#M2 — Resource dependency graph and one editable asset family]]
(M1 is complete and M2 deferred; see [[Project Roadmap#Roadmap status]]).

## Level resources, save files, lesson assets and plant collision

- [[EXP-20260910-008 - Replaceable Soil sign images]] — Training type 0x26/id 50: thirteen 64×64 index frames, page 17 palette and a separate id 51 live number bank; PNG import and exact packet inverse.

- [[PC Mr Soil dialogue replacement]] — PCM WAV lesson replacement, exact original formats and metadata, larger-file reader evidence and recipe.

- [[EXP-20260908-020 - Native enemy placement and scattered Blender population]] — bounded PC LEVEL.RAW codec and type 35 enemy placement records (64 × 28 bytes); unchanged packets and opaque metadata retained. [[XPORT-20260908-009 - Anthill enemy placement and model correspondences]].

- [[PC save record and medal bytes]] — 540-byte save files (`game0.sav`): a 0x18-byte slot header and the
  0x204-byte record `0x004D8428`, its layout, the 16 medal bytes and the flags byte `0x0059D908`.

- [[PC telescope camera paths]] — LEVEL.DAT top-record types 11, 12 and 13: a
  4-byte header and 16 signed XYZ triples per telescope tour, scaled by 32.

- [[PC scene admission and DAT layout rules]] — the end-of-file footer, free
  texture pages and the original LEVEL06 layout.

- [[PC sound banks and per-level audio routing]] — disc audio files, sample
  path building and per-level replacement.

- [[PC seed and mushroom collision state]] / [[EXP-20260906-007 - Plant-state collision regression]] - type5 mushroom -> PLANTTER record8; two-byte marker restoration recovers contact/bounce in native and live tests. Directory/unknown bytes and high0x104 unchanged; other plant types remain outside the repair.

## Level01 ramp and box composition (2026-09-05)

- [[EXP-20260905-004 - Playable ramp and box area]]: deck/top plus gentle ramp and matching sides; six paired PC-model routes, two live normal-input cycles, jump/landing and step-off; 118 terrain tests pass; no R2q.
- [[2026-09-05 1804 - Codex - Playable ramp and box area]]: rebuild instructions, evidence and runtime handoff.

## Shared-floor evidence (2026-09-05)

- [[EXP-20260905-003 - Shared floor return discriminator and stitched patch]]: 68-cell boundary census, complete mesh groups/duplicate vertices, original-PC return discriminator, six-cell connected patch and normal-input runtime comparison. Isolated floor 16/16; complete scene 13/16 with unchanged prop confounds; two live return cycles pass, separate source100 extension blocked.
- [[2026-09-05 1659 - Codex - Shared floor return and stitched patch]]: audit visibility correction, final validation and preservation record.

- [[EXP-20260904-010 - Paused subdivision live comparison]] — authorized same-pose
  mesh swap/restoration removes255 predicted fragments;9 matched-state captures,
  exact ROI restoration; 6 boundary samples remain.

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

- [[PC barrier translation prototype]] — canonical barrier translation with
  metadata preservation and a live-tested four-segment fixture (EXP-004).

- [[PC TERRAIN ALL barrier strips]] — canonical kind`0x101` reader, interleaved
  block metadata, sentinel tails and collection limits; EXP-20260904-003.

- [[EXP-20260904-002 - Retail collision admission and separate XZ barriers]] —
  original loading of Level01/Level03 plus PLANTTER, real steep-triangle
  admission, distinct kind`0x101` X/Z barriers, and bounded movement cell fields.

## LEVEL DAT and TERRAIN.ALL dossiers

- [[PC LEVEL DAT prefix]] - bounded prefix walk plus dispatch-`0x49` candidate-center, positive visibility-bound, flags, and relocated-payload roles; other dispatch/sign semantics remain unknown.
- [[PC LEVEL DAT static mesh]] - reconstructive type-`0x41` static-mesh
  grammar, exact consumer, retail coverage, and the authorization-gated causal
  boundary.
- [[PC TERRAIN ALL collision descriptor source]] - bounded source directory,
  `0x4C`-byte records, runtime `0x30`-byte descriptor mapping, and collision
  X/Z group bounds. EXP-131 maps Level03 result-1 descriptors 570–578 and
  retains incompatible Level00 payload variants explicitly.
- Its type-`0x3F` top table now has a bounded plant-selector use: exact
  Training bytes produce IDs 4, 10, and 6 through `0x00416100`. This is a
  separate table in the same DAT, not an M1 scene-record/payload bridge
  (`EXP-20260812-016`). Same-class results are occurrence-cursor dependent:
  changing only the second `0x2B` at `0x3A4` omits plant 10, preserves plant
  04, and reaches `NextLife` (`EXP-20260812-020`). This does not establish a
  public selector-editing grammar.
- `EXP-20260814-111` adds a separate exact Training grain boundary: selector
  `0x14` is independently PC-confirmed through terrain initialization and an
  isolated consumed-y/counter pickup. Inserting entry 62 at original `0x3E8`
  plus 556 known pointer relocations produces 51 collectible records and an
  exact inverse. This remains one hash/layout-locked recipe, not a general
  type-`0x3F` insertion grammar.
- `EXP-20260814-113` adds an exact Training letter boundary: singleton
  selectors `0x10`–`0x13` can be moved, duplicated, or removed with signed
  16-byte table growth/shrink, the same 556-field relocation census, preserved
  unknown tail bytes, and an exact inverse. Four moved duplicates initialize
  and collect under the unchanged executable. This remains hash/layout-locked,
  not a general public type-`0x3F` record grammar.
- `EXP-20260815-116` adds an exact Level03 type-1 coordinate-row boundary:
  top-record index 1 is at `0x458` with count 18 and 12-byte signed XYZ rows.
  Row 6 at `0x4A4` is the hash-locked PC runtime discriminator. Multiple PC
  consumers prevent promotion as a checkpoint/respawn table or general editor.
- [[STRUCT-PC-LEVEL-DAT-POSITIVE-PAYLOAD-TARGET]] - positive-count target grammar, masked dispatch-`0x49` consumer boundary, and placement-local visible rebind result; negative-count and other dispatch layouts remain unsupported.

## Candidate resource formats

- [[PC ANM first-level#Slot records (2026-10-01)]] - whole slot records as read by
  sampler `0x00445FF0`: frames, parts, words per frame, part list (`-3`/`-2`/`-1`),
  per-part bitmask and frames; 303 records in 60 of 61 retail files end with zero
  slack. `AnmFile.records()` parses them. [[PC Flik animation catalog]].
- [[PC ANM first-level]] - lossless, bounds-checked read-only inspection of the
  exact header/offset/first-reference walk at `0x00444B70`; all 11 PC plant
  files pass. Exact `.ANM`-only and equal-size `.ANM`/`.ALL` pair substitutions
  are accepted without a stable Training start-camera change; nested semantics
  and editing remain unsupported (`EXP-20260812-018`, `EXP-20260812-019`).
- Plant-resource `.ALL` remains below the tooling gate because `0x00448010` does not consume
  the whole-file byte size while walking embedded offsets and lengths. Exact
  pair acceptance is not a layout proof or parser boundary. Guarded runtime
  negatives now cover plant 10 entry heads, `+0x0C`, and `+0x2E` only through
  their stated return/title windows (`EXP-20260812-024` through
  `EXP-20260812-026`); they do not establish field semantics or safe editing.
  `EXP-20260812-034` independently bounds only exact unchanged `FLICK.ALL`
  and M2.20 source `FLICKD.ALL`: in each, 30 source descriptors end at file
  size `0x34EC`, 25 entries are initially materialized, and the coordinator
  retains indices `[0,24)`. This two-file address/count result does not
  promote a general layout, parser, or editor. `EXP-20260813-037` further
  maps only those 24 exact stream intervals: entry 8 is unchanged, entries
  `{0-7, 9-23}` contain all 2,102 retained-stream differences, and every one
  lies in a record span reached by both identical bounded downstream walks.
  `EXP-20260813-040` further reduces Direct3D count provenance to exact
  entries `{1,2,4,5,6,7,9,10,14,15,18,19,20}`. `EXP-20260813-041` further
  localizes the count-relevant boundary to 18 entry/form groups and 124 exact
  records while leaving 121 individual outcomes unresolved. These are
  exact-pair localization/count boundaries, not a field grammar or safe edit
  surface.

## M2 exit-gate boundary

`EXP-20260813-049` confirms that the selected `.ANM` first-level format
satisfies M2's multi-file plus synthetic-invalid and unknown-preservation gates
through `EXP-20260812-017`. That result does not transfer to the visible
`FLICK.ALL` family: `.ALL` remains bounded only for the exact two files and has
no general parser, invalid-input suite, field grammar, or editor. M2 remains
active on `KU-023`'s record/positive-target-to-resource selection edge, not on
a promoted `.ALL` format claim. `EXP-20260813-052` retains that causal gate
and selects only `0x0044CA00`'s finite 20-word signed-selector surface for
offline M2.38; exact `-103` would address ID-zero header `0x005B18E0`, but no
source value or M1 producer is yet proved.

Superseded 2026-08-13: [[EXP-20260813-059 - Independent M2.41 disposition hard-truth audit]]
found no finite cited successor and deferred M2 with the causal gate retained
([[Project Roadmap#Roadmap status]]).

## 2026-08-15 Level03 type-1 runtime link

- [[Level03 type-1 row discriminator]]: row-6 X at physical offset `0x4A4` now has a PC causal reset-coordinate receipt.

- [[EXP-20260815-117 - Approved Level03 row-6 reset rerun]] - PC runtime
  consumption evidence for Level03 `LEVEL.DAT` type-1 row 6; semantic record
  naming remains open.

## 2026-08-18 New-level authoring feasibility

- [[New-level authoring feasibility (PC)]] - the 2026-08-18 assessment of whether we
  can author new level layouts (terrain/collision/geometry); decode-state table,
  PC-vs-PS1 comparison, dependency-ordered gaps, and the render-geometry-grammar
  linchpin. Now status `historical`: EXP-20260904-002/005 and later terrain and
  collision experiments superseded its "not today" answer. Its companion
  [[New-level authoring roadmap (terrain, collision, materials)]] is historical too.
- [[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]]
  - how the PS1 port shipped a constrained new level and which format shapes
  transfer to PC as leads (cross-port inference).

## 2026-09-05 wall material inputs

- [[EXP-20260905-005 - Original wall texture regions and colour inputs]]:
  bounded PC face UV/vertex-colour census; screenshot localization and actual
  texture-page pixel comparison remain open.

EXP-005 runtime addendum: original-PC page0/palette pixels are now extracted
read-only. Floor/wall regions have different decoded pixels before vertex
shading; exact screenshot-pixel-to-face identity remains open.

EXP-005 application preserves known mesh grammar and unknown fields:24 wall
quad UV regions change,17 boundary vertices duplicate for colour isolation,
78 vertices/49 quads fit1730 bytes within the2234-byte allocation. All face
XYZ and collision remain unchanged; no general mesh/material rule follows.

## Terrain texture tiling and mesh growth, 2026-09-05

- [[EXP-20260905-006 - World-scale terrain tiling and checked mesh growth]]: atlas-local repetition, checked object-pointer/end-relative-footer growth, original x86 relocation comparison and185 passing terrain tests; collision preserved; live visual acceptance pending.
- [[2026-09-05 - Codex - Terrain texture tiling and mesh growth]]: EXP-005/006 evidence scope, private archive and focused validation.

- [[EXP-20260905-007 - Retail position control and missing floor footprints]]: retail RAM control and selected active-floor coverage differences after source-99 replacement; exact earlier fall and invisible-ground face mapping remain open.

- [[EXP-20260905-008 - Whole-Level01 collision and render coverage audit]]: complete Level01 edit inventory confirms source 99 alone replaces 134 original cells with 14 authored cells; 7,147 cells and all barriers are unchanged. Render mesh 160 alone changes but covers a different footprint.

- [[EXP-20260905-009 - Additive terrain preservation and access ramp]]: final 224/224 terrain gate; native preservation, relocation, command traversal, fall/box checks and four continuous-crossing/return routes pass. Exact-point controller failures retained and diagnosed. Evidence: `reports/terrain/EXP-20260905-009-validation.json`.

- [[EXP-20260906-001 - PC-compatible ramp visibility bounds]]: file-only radius6047 ->8560, collision/geometry preserved;73 affected and72 focused tests pass, native sweep0/5152 relevant candidate rejections versus544 control. [[2026-09-06 - Codex - File-based ramp visibility bounds]]. The runtime continuation loaded the corrected bound 8560 from file in Level01 with collision/geometry verified read-only, not yet all-view acceptance: `reports/terrain/EXP-20260906-001-runtime.json`.

- [[EXP-20260906-003 - Solid ramp sides and ground contour trim]]: established vertical32-byte cells and0x61 meshes only;20 cells appended, unknown fields/top preserved, native relocation/command traversal pass. No new grammar or universal ground classification.

- EXP-003 live continuation: complete resident TERRAIN.ALL source 99/100 payloads and LEVEL.DAT meshes 128/160/213/280 matched the isolated candidate; DAT+8592 bound remains 8560. A visible wall overlap is not evidence for renaming unknown fields or modifying format semantics. `reports/terrain/EXP-20260906-003-runtime.json`.

- [[EXP-20260906-004 - Wall clearance comparison and offset trial]] - size-preserving selected group+4/cell+6/cell+24 X translation; all other bytes and LEVEL.DAT unchanged. Original loader rebuilds derived bounds. No unknown field is renamed or recomputed.

- [[EXP-20260906-005 - Isolated authored terrain and platform spawn]]: bounded old scene/collision deactivation, exact authored pieces retained and private executable-table spawn. 53 affected/72 focused tests pass; native 9 accepted/1 setup failure, later corrected to 10/10. See the experiment for offsets and proof limitation.

- [[EXP-20260906-006 - Perimeter barriers and original foliage reference]]: bounded grass reuse retains page1 primitive tags0x162/0x8163/0x8166, source UVs and12-byte vertex suffixes. Copy-on-write LEVEL.DAT growth preserves old offsets/trailing-data base, verified by original-PC relocation and complete command traversal.381 filtered blade templates are candidate geometry classifications, not a newly decoded foliage-specific file format.
