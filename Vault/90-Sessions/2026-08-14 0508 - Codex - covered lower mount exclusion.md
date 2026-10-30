---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - implementation/modding
  - implementation/manifest
---

# Covered lower mount exclusion

## Goal

Execute exact corrective packet M4.15 after the M4.14 hard-truth rejection:
ignore only hidden lower same-path mount records, retain every prior sparse-
overlay removal refusal and positive control, update the durable Vault, and
leave one intentional clean worker commit for James M4.16.

## Work and evidence

- Repeated the complete required startup refresh and read the immutable M4.13/
  M4.14 evidence, M4/M1 notes, MOCs, READMEs, implementation, and tests.
- Filtered mountinfo records only when a same-mountpoint covering entry names
  the lower record through `parent_id`; both alias candidate and source
  comparisons now use only visible records.
- Added pure regressions for covered lower candidate and covered lower source
  false positives while preserving every ordinary and uncovered alias class.
- Added a private-namespace lower-bind/upper-`tmpfs` reproduction. Its
  authenticated visible overlay removes completely; the source and hidden
  target remain exact and the visible top parent returns to its empty snapshot.
- Retained the uncovered proper-parent refusal and four exact root/descendant
  mounted-path refusals with complete no-follow snapshots unchanged.
- Passed 102 focused and 290 canonical tests plus all six exact local apply/
  remove cycles with established hashes and unchanged sources.
- Final `make check` passed Vault lint over 241 notes with 0 errors/warnings,
  all 290 tests, and tracked-file audit with 0 violations; the 18-path scope is
  text-only and outside protected/game-content trees.
- Updated the required experiment, state, roadmap, decision, unknown, M4/M1,
  MOCs, READMEs, prior audit disposition, and session index surfaces.

## Conclusion

[[EXP-20260814-074 - Covered lower mount record exclusion]] records M4.15
worker-complete. The exact M4.14 stacked ordinary-top overlay now removes
successfully without touching its source or hidden target, while the M4.12
uncovered alias and all four M4.11 exact mounted paths retain fail-closed
refusal. No general mount policy, schema, receipt, operation, deletion target,
unmount, staged/source deletion, transaction, broad toolkit, runtime, M2, PS1,
or game-content boundary changed.

Exact fresh-context M4.16 is the sole next packet. James must independently
falsify the immutable worker commit and either accept with one exit-gate-backed
successor or reject with one bounded correction.

## Git commit if applicable

Intentional worker commit: `fix: ignore covered lower mount records`.
