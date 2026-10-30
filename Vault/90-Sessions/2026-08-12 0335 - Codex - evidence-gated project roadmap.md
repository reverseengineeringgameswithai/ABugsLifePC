---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - system/roadmap
---

# Evidence-gated project roadmap

## Agent

Codex

## Goal

Create one robust, durable roadmap from the current reverse-engineering state to
practical modding, and integrate it with the Vault without duplicating the roles
of the charter, state, unknown, evidence, and chronology notes.

## Files inspected

- `AGENTS.md`
- [[START HERE]], [[Project Charter]], [[Agent Operating Manual]],
  [[Current State]], and [[Environment Status]]
- [[Research Method]], [[Evidence Standard]], [[Knowledge Hygiene]], and
  [[Cross-Port Evidence Policy]]
- [[Decision Log]], [[Known Unknowns]], and the relevant MOCs

## Experiments inspected

- `EXP-20260811-001` through `EXP-20260812-008` at the summary and current-state
  level needed to assign roadmap status.
- No binary, original file, external port, or new reverse-engineering evidence
  was inspected or changed.

## Changes made

- Added [[Project Roadmap]] as the canonical prioritization layer.
- Defined six evidence-gated milestones from the completed foundation through
  scene records, resources, gameplay, a mod toolkit, selective
  reimplementation, and compatibility/releases.
- Added explicit work packages, entry/exit gates, cross-cutting safety rules,
  prioritization rules, and active packet M1.1.
- Linked the roadmap from [[START HERE]], [[Project Charter]], [[Current State]],
  [[Known Unknowns]], and the relevant MOCs.
- Recorded [[Decision Log#DEC-20260812-007 - Evidence-gated canonical roadmap]].

## Conclusions

- The project foundation is complete for Wine-first PC-native research and the
  first safe modding vertical slice.
- Milestone M1 is active. The exact next packet is a PC-native structural and
  consumer trace of Training payload targets `0x111E4` and `0x1319C`.
- Windows 98 remains a conditional compatibility discriminator, not a blocker
  for the active path.
- Selective reimplementation remains gated per module; a full rewrite and a
  global implementation-language decision are not prerequisites for modding.

## New hypotheses

None. The roadmap schedules existing evidence and unknowns without promoting a
new game-semantic interpretation.

## Contradictions discovered

None. The roadmap reconciles the charter's broad phases with the more advanced
current Wine/modding state under existing decisions.

## Tests run

- `make check`: Python dependency smoke test, Vault lint (`66` notes, `0`
  errors, `0` warnings), `pytest` (`10` passed), tracked-file audit (`0`
  violations), and Git whitespace checks all passed.

## Unresolved questions

The research unknowns remain in [[Known Unknowns]]. In particular, M1.1 must
discriminate the structure and meaning of targets `0x111E4` and `0x1319C` before
parser expansion or cross-port comparison.

## Recommended next action

Execute [[Project Roadmap#M1.1 — Shared payload-target structure]] using the PC
anchors and completion gate recorded there.

## Git commit if applicable

Bounded commit message: `docs: add evidence-gated project roadmap`.
