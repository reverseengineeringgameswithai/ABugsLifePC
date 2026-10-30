---
type: project-charter
status: active
created: 2026-08-11
updated: 2026-10-02
tags:
  - system/charter
  - re/ablpc
---

# Project Charter

## Mission

Reverse engineer the Windows PC release of Disney/Pixar's *A Bug's Life* through reproducible static and runtime evidence. Build a durable technical account of the executable, data formats, platform integration, and observable behavior so that future analysis and independently written tools or compatible implementations can be tested against the original program.

The Windows PC binary and its controlled behavior are the subject. Other ports are comparative evidence, not substitutes for PC evidence.

## Research authority

Use this order when evidence conflicts:

1. Reproducible behavior from the hashed PC executable in a recorded environment.
2. PC runtime observations, addresses, file offsets, and captured artifacts.
3. PC static analysis, cross-references, imports, strings, and comparisons across PC files.
4. Bounded comparisons with another port at a pinned revision.
5. Researcher or AI hypotheses.

A lower tier can suggest an experiment. It cannot overrule a higher tier without new evidence.

## Scope

- Preserve, inventory, and identify user-owned PC media and binaries.
- Map PC executable initialization, platform APIs, subsystems, functions, data, and control flow.
- Establish baseline behavior in 86Box and fast repeatable behavior under Wine.
  The built 86Box baseline is [[86Box Win95 RE harness]] (Windows 95 OSR2, from
  `originals/`); the Windows 98 SE profile in [[86Box Reference Machine]] was
  the first plan and has no installer media (amended 2026-10-02).
- Use a modern Windows VM when debugger or Windows-native telemetry is needed.
- Document file formats and write bounds-checked parsers with synthetic tests where practical.
- Produce address-based dossiers, evidence packets, experiments, and regression tests.
- Develop independently written tooling or reimplementation work only when supported by recorded evidence.

## Non-goals

- Distributing copyrighted game files, disc images, ROMs, Windows media, or extracted assets.
- Modifying originals or treating a patched executable as the behavioral reference.
- Mechanically translating decompiler output into source code.
- Assigning semantic names because they sound plausible.
- Importing another reverse-engineering project's assumptions wholesale.
- Making the PC repository a mirror, submodule, or vendor dump of the PS1 project without a separate recorded decision.
- Declaring compatibility or completeness without reproducible tests.

## PC-first cross-port rule

The PS1 research repository at `~/Downloads/ABL` is external comparative material. Keep it outside this repository and record the exact commit whenever it is consulted.

A PS1 comparison is eligible only when the PC side already has:

- a bounded question;
- the PC executable SHA-256;
- at least one PC address, file offset, string, import, or runtime observation;
- a PC-native dossier or evidence packet;
- an explicit unknown that the comparison may discriminate;
- a plan to verify any proposed correspondence back against the PC binary.

Every resulting note must label statements as `PC confirmed`, `cross-port inferred`, or `unknown`. A PS1 name, type, constant, or control flow never confirms the corresponding PC meaning by itself. Do not copy PS1 symbols into Ghidra in bulk.

The PS1 reference pinned during bootstrap was commit `32e57fa7e7b25f3b5119f8e0fd386df55514e037`. Since 2026-08-15 [[External Source Registry]] records `1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`, which every later cross-port note cites and which was still the external HEAD on 2026-10-02. Reconfirm and record the revision at the time of each future comparison.

## Research phases

1. Provenance and tooling: hash media and executable, establish the vault, triage PE metadata, and create reproducible analysis tooling.
2. PC-native baseline map: categorize imports and high-value strings, identify entry and platform setup paths, and create address-based dossiers.
3. Runtime baseline: capture startup, file access, display/input/audio initialization, and failure behavior under controlled environments.
4. Subsystem and format studies: create bounded evidence packets, discriminating experiments, parsers, and tests.
5. Bounded cross-port comparison: consult pinned PS1 evidence only for a specific PC-native unknown.
6. Independent implementation: implement only behavior supported by evidence and compare it against recorded original behavior.

Phases overlap as evidence develops, but the PC-native gate is not optional.
Operational milestone order, exit gates, and the current work packet live in
[[Project Roadmap]]. The charter remains authoritative if roadmap wording ever
conflicts with mission, evidence hierarchy, scope, or non-goals.

## Evidence completion standard

A significant claim is complete only when its note states:

- whether it is confirmed, inferred, or unknown;
- the binary SHA-256;
- the relevant address, offset, run ID, or experiment ID;
- the environment when runtime behavior is involved;
- the evidence that supports it;
- contradictory evidence or limitations;
- the next discriminating experiment when uncertainty remains.

Important conclusions should use two independent evidence forms where practical.

## Repository hygiene

- `originals/` is immutable source material and never a work area.
- `work/` holds disposable copies, tool databases, prefixes, and VM state.
- `static/`, `dynamic/`, `reports/`, and the Vault hold reviewable evidence and metadata.
- Do not commit downloaded tool binaries or generated machine state.
- Keep external projects external. Record paths and revisions rather than nesting repositories.
- Prefer small, bounded commits whose staged content can be inspected for copyrighted or generated material.

## Durable handoff

Conversation history is disposable. [[Current State]], [[Environment Status]], the decision and unknown registers, MOCs, dossiers, experiments, and session notes are the handoff.

At the end of meaningful work, follow [[START HERE]] and [[Agent Operating Manual]] session-close requirements. If the mission, scope, or evidence hierarchy changes, update this charter and record the decision in [[Decision Log]].
