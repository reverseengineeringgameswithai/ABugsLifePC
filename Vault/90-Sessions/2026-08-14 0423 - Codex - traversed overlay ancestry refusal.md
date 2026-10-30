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

# Traversed overlay ancestry refusal

## Goal

Execute exact corrective packet M4.13 after the M4.12 hard-truth rejection:
reject the reproduced proper-parent mount alias before sparse-overlay mutation,
retain ordinary cleanup under normal filesystem mounts, update the durable
Vault, and leave one intentional clean worker commit for James M4.14.

## Work and evidence

- Repeated the complete required startup refresh and read the immutable M4.11/
  M4.12 evidence, M4/M1 notes, MOCs, READMEs, implementation, and tests.
- Extended Linux mountinfo parsing to retain mount ID, device, filesystem root,
  and mountpoint while preserving the existing fail-closed parser and exact-
  plan mountpoint set.
- Added a removal-only alias classifier: a newer mount exposing an already
  reachable same-device filesystem root at a different visible path is refused
  only when that alias lies in the proper ancestry of the overlay root.
- Added a pure classification regression proving ordinary root, `/home`,
  `/tmp`, and same-path nested mounts remain usable while subdirectory and
  whole-root aliases are classified.
- Added the exact private-namespace proper-parent reproduction to the existing
  helper. The root/descendant case set is now five and all preserve complete
  overlay/source/independent-target snapshots.
- Passed 101 focused tests, 289 canonical tests, and all six exact local
  apply/remove cycles with established hashes and unchanged sources.
- Final `make check` passed 289 tests, Vault lint over 237 notes with 0
  errors/warnings, and tracked-file audit with 0 violations; all 19 changed
  paths are text-only and outside protected/game-content trees.
- Updated the required experiment, state, roadmap, decision, unknown, M4/M1,
  MOCs, READMEs, prior audit disposition, and session index surfaces.

## Conclusion

[[EXP-20260814-072 - Traversed overlay-root ancestry mount-alias refusal]]
records M4.13 worker-complete. The exact M4.12 proper-parent alias now refuses
before overlay content traversal/unlink, the four exact M4.11 mounted paths
still refuse, and ordinary cleanup below normal filesystem ancestry remains
usable. No general mount policy, schema, receipt, operation, deletion target,
unmount, staged/source deletion, transaction, broad toolkit, runtime, M2, PS1,
or game-content boundary changed.

Exact fresh-context M4.14 is the sole next packet. James must independently
falsify the immutable worker commit and either accept with one exit-gate-backed
successor or reject with one bounded correction.

## Git commit if applicable

Intentional worker commit: `fix: reject traversed overlay mount aliases`.
