---
type: roadmap
status: active
updated: 2026-10-29
tags: [system/roadmap]
---

# Project Roadmap

## Purpose

Canonical milestone order and gates for evidence-backed research on the
Windows PC release, including the modification requirements and the M1–M6
file-replacement toolkit. [[Project Charter]] owns scope; [[Current State]]
summarises where the research stands; [[Known Unknowns]] owns unresolved
questions. Chronology is linked below rather than repeated as current
instructions.

## Current work packet

No research packet is active on 2026-10-29. The last one was the static
creature and platform session of 2026-10-18
([[2026-10-18 - Claude - Static research on creature rows and the script VM]]),
closed with two read-only hardware arms
([[EXP-20261018-013 - Options screens and the creature gate live]]).
[[Next Tasks]] (2026-10-29) proposes an order for the open research tasks,
starting with CAP-010's acceptance arm; this note still owns sequencing. A new
packet follows [[#Work-packet rules]].

## Research phases

[[Project Charter#Research phases]] defines six overlapping phases. Their
standing on 2026-10-29:

| Phase | Standing | Entry point |
|---|---|---|
| 1. Provenance and tooling | Done for the retail disc and executable; tooling grows per packet | [[EXP-20260811-001 - PC disc census and executable identification]], [[EXP-20260811-002 - Ghidra static baseline]] |
| 2. PC-native baseline map | Imports, strings, entry and platform setup mapped; dossiers per function | [[EXP-20260811-003 - PC-native import string and function map]], [[Functions MOC]] |
| 3. Runtime baseline | Wine/Gamescope hardware baseline and the 86Box Windows 95 harness exist; the Windows debug VM is blocked on media | [[Environment Status]] |
| 4. Subsystem and format studies | Ongoing; per-row status in [[Subsystem Coverage Map]] | [[Current State#Research status by subsystem]] |
| 5. Bounded cross-port comparison | Ten comparison notes, each at a pinned PS1 commit | [[External Source Registry#SRC-PS1-ABL]] |
| 6. Independent implementation | M5 active with two admitted modules | [[#Admitted modules]] |

## Roadmap status

These are the existing **project-wide** milestone dispositions, not new
September 26 acceptance.


| Milestone | Status | Outcome | Evidence or entry point |
|---|---|---|---|
| M0 — Research and runtime foundation | Complete | Reproducible PC evidence and a fast Linux loop | `EXP-20260811-001` through `EXP-20260812-008` |
| M1 — Scene records and reusable payloads | Complete | Explain and safely edit the scene-selection-to-payload path | [[M1 Tool Support Matrix]] |
| M2 — Resource dependency graph and one editable asset family | Deferred | Trace one level placement through loaded resources to rendered content | [[EXP-20260813-059 - Independent M2.41 disposition hard-truth audit]]; causal gate retained |
| M3 — Gameplay and level-logic systems | Complete | Identify and edit selected actors, interactions, collision, triggers, camera, and progression | [[EXP-20260815-135 - Independent M3 ratchet acceptance audit]]; all four gates accepted after exact authorization correction |
| M4 — Mod toolkit v0.1 | Complete | Deliver a non-destructive, composable Linux mod workflow | [[EXP-20260814-103 - Independent M4.43 selected-path and milestone-closure hard-truth audit]]; 9/9 capabilities and 5/5 exit gates at the documented boundary |
| M5 — Selective reimplementation | Active | Replace only well-specified components with independently written code | [[EXP-20260816-171 - Independent M5.8 grain-gate resolver audits]] accepts the second optional module at exact `dfd3af3`; no third module is admitted |
| M6 — Compatibility validation and releases | Complete | Publish reproducible Wine-scoped tools/mods with honest compatibility claims | [[EXP-20260814-110 - Independent M6 state-locked lifecycle acceptance audit]]; all four exit gates accepted at the documented boundary |

## Paused tracks

The historical R2q-032 activation is an offline checkpoint, not fresh runtime
permission. Its immutable design and failed/incomplete validation history remain
in the archive. The user dropped the R2q track on 2026-09-27 as too slow, so
its packets and gate tests may be outdated. A future task must select and
authorize its own bounded packet.

[[PC Large-Level Engine Roadmap]] numbers its own stages separately; do not
confuse its paused stage 4 (streaming, paused on 2026-09-08) with project M4,
or resume it by reading an old next-agent directive.

## Work-packet rules

- Keep one active milestone and one exact next work packet in this note and
  [[Current State]].
- Ask one bounded question that available evidence can discriminate.
- Cite the exact PC executable or file hash and at least one PC locator.
- Define the expected observation and what competing interpretations it
  distinguishes.
- Prefer two independent evidence forms for important claims.
- End with reviewable evidence, updated unknowns, and a specific follow-up.
- Extend parsers or reimplementation only after the relevant behavior or layout
  is demonstrated.
- Obtain explicit approval before debugger changes to memory, registers, code,
  execution, or breakpoints, as required by [[Agent Operating Manual]].

## Module entry gate

A candidate module needs:

- a bounded input/output or state-transition contract;
- cited PC addresses, offsets, and original runtime observations;
- fixtures that do not require committing copyrighted game content;
- known error and edge behavior;
- a differential test against the original program where practical;
- a written reason that replacement advances an actual modding outcome.

Language and architecture decisions are made per module after this gate. They
are not selected globally from decompiler aesthetics.

## Admitted modules

| Module | Entry evidence | Boundary |
|---|---|---|
| Type-1 reset placement resolver | [[EXP-20260816-153 - M5 entry gate and type-1 reset placement resolver]] | Level03/Tunnels reset role only; refuses zero-count, negative-type-alias, and missing-record inputs; not a level editor |
| Grain-gate opening resolver | Corrected entry [[EXP-20260816-168 - M5.6.1 claim and contract correction]] accepted by EXP-169; implementation independently accepted by [[EXP-20260816-171 - Independent M5.8 grain-gate resolver audits]] | Twelve confirmed Tunnels/City Entrance mechanisms only; direct opening writes include row-0/4 coupling and City index-0 `[0x00599C69] = 1`; global family exclusivity and byte semantics are not claimed |

## Historical record

[[Project Roadmap history through 2026-09-26]] preserves the previous note verbatim. [[Session Index]] indexes the original session records. Historical permissions and process IDs do not carry forward.

## Historical heading links

These headings retain existing Obsidian links; their details are historical.

## M1 — Scene records and reusable payloads

See [[Project Roadmap history through 2026-09-26#M1 — Scene records and reusable payloads]].

## M1.1 — Shared payload-target structure

See [[Project Roadmap history through 2026-09-26#Work packages]].

## M1.2 — Guarded target rebind and visible reuse

See [[Project Roadmap history through 2026-09-26#M1.2 — Guarded target rebind and visible reuse]].

## M1.3 — Record selection and payload discrimination

See [[Project Roadmap history through 2026-09-26#M1.3 — Record selection and payload discrimination]].

## M1.4 — Non-Training same-dispatch validation

See [[Project Roadmap history through 2026-09-26#M1.4 — Non-Training same-dispatch validation]].

## M1.5 — Tooling boundary audit and promotion

See [[Project Roadmap history through 2026-09-26#M1.5 — Tooling boundary audit and promotion]].

## M2 — Resource dependency graph and one editable asset family

See [[Project Roadmap history through 2026-09-26#M2 — Resource dependency graph and one editable asset family]].

## M2.1 — PC content census and loader-context baseline

See [[Project Roadmap history through 2026-09-26#M2.1 — PC content census and loader-context baseline]].

## M2.10 — Plant 10 late-initialization consumer boundary

See [[Project Roadmap history through 2026-09-26#M2.10 — Plant 10 late-initialization consumer boundary]].

## M2.11 — Plant 10 entry-head consumer boundary

See [[Project Roadmap history through 2026-09-26#M2.11 — Plant 10 entry-head consumer boundary]].

## M2.12 — Plant 10 entry-head +0x0C consumer boundary

See [[Project Roadmap history through 2026-09-26#M2.12 — Plant 10 entry-head +0x0C consumer boundary]].

## M2.13 — Plant 10 entry +0x2E gate boundary

See [[Project Roadmap history through 2026-09-26#M2.13 — Plant 10 entry +0x2E gate boundary]].

## M2.14 — Plant 10 entry +0x28 boundary

See [[Project Roadmap history through 2026-09-26#M2.14 — Plant 10 entry +0x28 boundary]].

## M2.15 — Plant 10 post-title selected-entry event

See [[Project Roadmap history through 2026-09-26#M2.15 — Plant 10 post-title selected-entry event]].

## M2.16 — Fresh-session selected-entry caller chain

See [[Project Roadmap history through 2026-09-26#Work packages]].

## M2.17 — Unexpected-signal-safe debugger control

See [[Project Roadmap history through 2026-09-26#M2.17 — Unexpected-signal-safe debugger control]].

## M2.18 — Adjacent caller-gate continuation discriminator

See [[Project Roadmap history through 2026-09-26#M2.18 — Adjacent caller-gate continuation discriminator]].

## M2.19 — Direct visible plant-family outcome

See [[Project Roadmap history through 2026-09-26#M2.19 — Direct visible plant-family outcome]].

## M2.2 — Plant resource caller and consumer trace

See [[Project Roadmap history through 2026-09-26#M2.2 — Plant resource caller and consumer trace]].

## M2.20 — Training character-family discriminator

See [[Project Roadmap history through 2026-09-26#M2.20 — Training character-family discriminator]].

## M2.21 — Character request and first-consumer trace

See [[Project Roadmap history through 2026-09-26#M2.21 — Character request and first-consumer trace]].

## M2.22 — Character retained-range first-use bridge

See [[Project Roadmap history through 2026-09-26#M2.22 — Character retained-range first-use bridge]].

## M2.23 — Shared-entry render-lineage discriminator

See [[Project Roadmap history through 2026-09-26#M2.23 — Shared-entry render-lineage discriminator]].

## M2.24 — ID-zero stream-difference localization

See [[Project Roadmap history through 2026-09-26#M2.24 — ID-zero stream-difference localization]].

## M2.25 — Per-entry hardware-submission delta capture

See [[Project Roadmap history through 2026-09-26#M2.25 — Per-entry submission-arena delta capture]].

## M2.26 — Direct3D renderer-path reconciliation

See [[Project Roadmap history through 2026-09-26#M2.26 — Direct3D renderer-path reconciliation]].

## M2.27 — Direct3D retained-entry batch provenance

See [[Project Roadmap history through 2026-09-26#M2.27 — Direct3D retained-entry batch provenance]].

## M2.28 — Changed-record form localization

See [[Project Roadmap history through 2026-09-26#M2.28 — Changed-record form localization]].

## M2.29 — Per-record Direct3D append discriminator

See [[Project Roadmap history through 2026-09-26#M2.29 — Per-record Direct3D append discriminator]].

## M2.3 — Plant request origin and M1 dependency bridge

See [[Project Roadmap history through 2026-09-26#M2.3 — Plant request origin and M1 boundary]].

## M2.30 — Exact `0x0A6C` builder-input localization

See [[Project Roadmap history through 2026-09-26#M2.30 — Exact `0x0A6C` builder-input localization]].

## M2.31 — Exact `0x0A6C` admission-state localization

See [[Project Roadmap history through 2026-09-26#M2.31 — Exact `0x0A6C` admission-state localization]].

## M2.32 — Exact `0x0A6C` admission-predicate receipt

See [[Project Roadmap history through 2026-09-26#M2.32 — Exact `0x0A6C` admission-predicate receipt]].

## M2.33 — Exact `0x0A6C` consecutive-cycle stability bound

See [[Project Roadmap history through 2026-09-26#M2.33 — Exact `0x0A6C` consecutive-cycle stability bound]].

## M2.34 — M2 exit-gate reconciliation

See [[Project Roadmap history through 2026-09-26#M2.34 — M2 exit-gate reconciliation]].

## M2.36 — Generic resource-index producer census

See [[Project Roadmap history through 2026-09-26#M2.36 — Generic resource-index producer census]].

## M2.37 — M2 dependency-gate disposition

See [[Project Roadmap history through 2026-09-26#M2.37 — M2 dependency-gate disposition]].

## M2.38 — Signed source-record selector provenance

See [[Project Roadmap history through 2026-09-26#M2.38 — Signed source-record selector provenance]].

## M2.4 — Bounded ANM inspector

See [[Project Roadmap history through 2026-09-26#M2.4 — Bounded ANM inspector]].

## M2.5 — Same-layout ANM replacement validation

See [[Project Roadmap history through 2026-09-26#M2.5 — Same-layout ANM replacement validation]].

## M2.6 — Same-size paired plant replacement

See [[Project Roadmap history through 2026-09-26#M2.6 — Same-size paired plant replacement]].

## M2.7 — Plant 04 request suppression and visible-mask bridge

See [[Project Roadmap history through 2026-09-26#M2.7 — Plant 04 request suppression and visible-mask bridge]].

## M2.8 — Plant 10 runtime consumer-to-placement bridge

See [[Project Roadmap history through 2026-09-26#M2.8 — Plant 10 runtime consumer-to-placement bridge]].

## M2.9 — Plant 10 downstream object-entry consumer

See [[Project Roadmap history through 2026-09-26#M2.9 — Plant 10 downstream object-entry consumer]].

## M3 — Gameplay and level-logic systems

See [[Project Roadmap history through 2026-09-26#M3 — Gameplay and level-logic systems]].

## M3.1 — Exact Training 51st grain vertical slice

See [[Project Roadmap history through 2026-09-26#M3.1 — Exact Training 51st grain vertical slice]].

## M3.2 — Retained/displayed 51 and original 50 milestone

See [[Project Roadmap history through 2026-09-26#M3.2 — Retained/displayed 51 and original 50 milestone]].

## M3.3 — Training FLIK letter transformations

See [[Project Roadmap history through 2026-09-26#M3.3 — Training FLIK letter transformations]].

## M3.4 — Training FLIKFLIK HUD and completion

See [[Project Roadmap history through 2026-09-26#M3.4 — Training FLIKFLIK HUD and completion]].

## M3.5 — Level03 type-1 candidate respawn-row discriminator

See [[Project Roadmap history through 2026-09-26#M3.5 — Level03 type-1 candidate respawn-row discriminator]].

## M3.7 — Approval-compliant Training runtime receipts

See [[Project Roadmap history through 2026-09-26#M3.7 — Approval-compliant Training runtime receipts]].

## M4 — Mod toolkit v0.1

See [[Project Roadmap history through 2026-09-26#M4 — Mod toolkit v0.1]].

## M4.25 — Deterministic single-manifest dry-run report

See [[Project Roadmap history through 2026-09-26#M4.25 — Deterministic single-manifest dry-run report]].

## M4.27 — M4 v0.1 milestone-closure evidence audit

See [[Project Roadmap history through 2026-09-26#M4.27 — M4 v0.1 milestone-closure evidence audit]].

## M4.34 — Clean-derived-copy lifecycle feasibility hard-truth audit

See [[Project Roadmap history through 2026-09-26#M4.34 — Clean-derived-copy lifecycle feasibility hard-truth audit]].

## M4.40 — Independent M4.39 statement and milestone-closure hard-truth audit

See [[Project Roadmap history through 2026-09-26#M4.40 — Independent M4.39 statement and milestone-closure hard-truth audit]].

## M4.41 — Version-bound canonical statement strictness correction

See [[Project Roadmap history through 2026-09-26#M4.41 — Version-bound canonical statement strictness correction]].

## M4.42 — Independent M4.41 strictness and milestone-closure hard-truth audit

See [[Project Roadmap history through 2026-09-26#M4.42 — Independent M4.41 strictness and milestone-closure hard-truth audit]].

## M4.43 — Lexical selected-statement identity and non-link file correction

See [[Project Roadmap history through 2026-09-26#M4.43 — Lexical selected-statement identity and non-link file correction]].

## M4.44 — Independent M4.43 selected-path and milestone-closure hard-truth audit

See [[Project Roadmap history through 2026-09-26#M4.44 — Independent M4.43 selected-path and milestone-closure hard-truth audit]].

## M5 — Selective reimplementation

See [[Project Roadmap history through 2026-09-26#M5 — Selective reimplementation]].

## M5.8 — Independent M5.7 grain-gate resolver hard-truth audit

See [[Project Roadmap history through 2026-09-26#M5.8 — Independent M5.7 grain-gate resolver hard-truth audit]].

## M6 — Compatibility validation and releases

See [[Project Roadmap history through 2026-09-26#M6 — Compatibility validation and releases]].

## R2q — Freeze the post-gameplay quiet-census barrier

See [[Project Roadmap history through 2026-09-26#R2q — Freeze the post-gameplay quiet-census barrier]].
