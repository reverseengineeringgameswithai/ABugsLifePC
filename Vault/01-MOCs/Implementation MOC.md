---
type: moc
status: active
updated: 2026-10-29
tags: [moc/implementation]
---

# Implementation MOC

[[Current State#Current task handoff]] owns the current source/build and pending
acceptance; [[Environment Status#Current runtime handoff]] owns live bindings.
This map lists maintenance guides and modification requirements, not dated
tasks to execute automatically.

## Original-level reference maps and engine limits

- [[PC original level Blender maps]] — complete reference maps of every other
  original level; [[PC original Training Blender mapping]] keeps Training.
- [[PC Large-Level Engine Roadmap]] — milestone record of native limits measured
  while testing larger levels (actor slot 16 and the camera, the twentieth-plant
  scan, 400-entry collision lists); resident stages accepted, streaming paused.
- [[PC level authoring memory limits]] — retained storage overrunning renderer
  scratch `0076F9A0`, the shared pool at `00598CA8`, the 20-plant scan and
  400-entry candidate lists.
- [[PC general render distance]] — render distance set by three immediates at
  `0x0044BBA3`/`0x0044BBAF`/`0x0044BBC1`, near derived from far, lookup at
  `0x005C0410`.
- [[PC custom distant terrain]] / [[PC custom distant objects]] — secondary
  (distant) geometry: visibility bytes copied at `0044BB70`, traversal at
  `0044D430`, quartered translation/scale and hardware quad/triangle thresholds.

## Anthill object, scenery and actor requirements

- [[PC Anthill remaining object inventory]] — remaining donor candidates,
  texture coverage, animation/collision and allocation gates; research only.
- [[PC Anthill scenery assemblies]] — visual-to-collision correspondence for
  original Anthill scenery records, kind-`0x101` strip collision for leaves and
  the retained page-3 RAW packet.
- [[PC Anthill tree and mound authoring]] — original tree composition (primary
  scenes 5/6/7/8/17, secondary 17/18 needing 4x restoration), mound records and
  signed-byte collision admission windows.
- [[PC leaf statue authoring]] — original leaf statue (primary scene 109,
  geometry 264144), dispatch `0x41`/`0x49` to `0045A7F0` and its paired terrain
  source 89 shell.
- [[PC wooden fence authoring]] — original fence scene 118, billboard dispatch
  to `00453FF0`; the billboard has no collision of its own.
- [[PC reusable scenery mushroom authoring]] — each net-new native scenery
  mushroom needs a new primary record, render object and collision descriptor.
- [[PC animated clover authoring]] — native clover donors, shared geometry
  `0x2BA3C`, object +25 animated-matrix selection (`0x00449C93`) updated by
  `00455710`.
- [[PC Anthill berry and flower authoring]] — berry clusters and flowers
  (scenes 65/66/90/91), dispatch `0x0A` to `00454B70` and the flower sway slot.
- [[PC fixed growable seed authoring]] / [[PC Anthill collectible authoring]] —
  seed placement bytes (+0x0E colour, +0x0F forced plant from table `004DE9F0`)
  and the native pickup selector/limit table.
- [[PC Anthill enemy authoring]] — five native enemy types, the original
  placements they replace and the 53-entry enemy capacity.
- [[PC Dot flight path authoring]] — Dot's route: RAW slot 25, proximity waits in
  `0041DC60`, cursor clamp `004317D0` and the 104-triple path in the DAT.
- [[PC test-area exit placement]] — native exit: descriptor result at source
  +0x28, post-movement query `0x004408AC`, done flag `0x0059A5B0` with no grain
  check.
- [[PC native creature transplant]] — what moves with a creature row (model by
  type via `00445020`, script table `0x004C83F0`, health/flags) and what stays
  level-bound, such as engine-bound boss routines; the engine facts are in
  [[PC boss level routines and creature transplant limits]].
- [[PC terrain collision rules for modified levels]] — what added or moved
  collision must respect, and which original Level01 and LEVEL06 props carry
  collision of their own.

## Training lesson audio and triggers

- [[PC Mr Soil dialogue replacement]] — Training lesson speech is standalone
  PCM WAVs replaced by filename; no executable patch.
- [[PC Mr Soil lesson triggers]] — census of the lesson predicates in retail
  `0043C340` and native speech completion (`0042C110`, `00440F50`).

## Tooling and research boundaries

[[Agent evidence and query tooling]], [[Session control plane]],
[[PC autonomous game control]], [[M1 Tool Support Matrix]] and [[Project Roadmap]].
The source checkpoint preserves existing implementations and their tests; broad
compatibility, complete routes and visual acceptance are not implied.

## Other maintained notes

Toolkit, proof-edit and runtime-tool notes. Each note's own status and date
bound what it claims.

- Training packets: [[Training 51-grain vertical slice]],
  [[Training FLIK letter transformations]], [[Training FLIKFLIK HUD and completion]],
  [[Level03 type-1 row discriminator]].
- Proof edits: [[PC barrier translation prototype]], [[PC floor translation prototype]],
  [[PC automatic Direct3D startup candidate]].
- Grain gates: [[PC grain gate threshold mod]] (`scripts/make-grain-gates`),
  [[PC grain gate opening resolver]] and [[PC type-1 reset placement resolver]] (M5 modules).
- Toolkit milestones and inspectors: [[LEVEL DAT modding vertical slice]]
  (`scripts/ablpc-mod`), [[M4 Exact Whole-file Replacement]], [[M6 Toolkit Release]],
  [[PC TERRAIN ALL inspector]], [[PC ANM inspector]].
- Runtime tools: [[Runtime Tooling]], [[PC input movies]], [[PC coordinate overlay]],
  [[PC Flik teleport procedure]], [[Flight Recorder]] (86Box plan).
- Method: [[Reverse Engineering Capability Gaps]],
  [[Python and C reverse-engineering split]].

## Historical record

[[Implementation MOC history through 2026-09-26]] preserves the previous note verbatim. [[Session Index]] indexes the original session records. Historical permissions and process IDs do not carry forward.
