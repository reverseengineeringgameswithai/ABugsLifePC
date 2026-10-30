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

# Mount generation order correction

## Goal

Execute exact corrective packet M4.17 after the M4.16 hard-truth rejection:
remove reusable legacy mount IDs from ancestry-age decisions, reproduce the
exact lower-ID reuse case, retain every accepted M4/M1/local boundary, update
the durable Vault, and leave one intentional clean worker commit for James
M4.18.

## Work and evidence

- Repeated the complete required startup refresh and read the immutable M4.15/
  M4.16 evidence, M4/M1 notes, MOCs, READMEs, implementation, and tests.
- Reproduced legacy mount-ID reuse inside a private user/mount namespace, then
  confirmed the current kernel exposes explicit later-first unique mount order
  and old-ID/parent/device mapping through `listmount(2)` plus `statmount(2)`.
- Added bounded, bounds-checked syscall readers that fail closed on syscall,
  sequence, mapping, metadata, or mount-table-snapshot disagreement.
- Changed only `_mount_alias_points` age comparison from reusable
  `mount_id` to the verified explicit `mount_order`; M4.15 covered same-path
  parent-stack filtering remains unchanged.
- Added a private-namespace regression that requires a newly bound alias to
  reuse a lower numeric ID than its still-mounted source and requires refusal
  with source/independent-target/alias/overlay snapshots exact.
- Added tuple-order pure regressions and retained the six prior namespace
  families. The targeted mount boundary passes 10/10.
- Passed 105 focused and 293 canonical tests plus all six exact local apply/
  remove cycles with established hashes and unchanged sources.
- Final `make check` passed Vault lint over 245 notes with 0 errors/warnings,
  all 293 tests, tracked-file audit with 0 violations, and both diff checks;
  the complete worker scope is text-only and outside protected/game-content
  trees.
- An initial local harness selected the wrong accepted M1 manifest for the
  mixed-family expectation and stopped in its disposable root; the corrected
  established record-124-target plus opaque family then passed 2/2. No source
  or repository file was changed by that harness mistake.
- Updated the required experiment, state, roadmap, decision, unknown, M4/M1,
  MOCs, READMEs, prior audit disposition, and session index surfaces.

## Conclusion

[[EXP-20260814-076 - Mount generation order for ancestry aliases]] records
M4.17 worker-complete. The exact reused-lower-ID alias now refuses before
traversal/unlink with all four snapshots unchanged. Covered ordinary-top
removal, normal uncovered/visible-top/exact-plan refusals, ordinary removal,
composition, M1, local, and asset-free results remain intact. This is a
current-Linux classifier correction, not a broad portability or ownership
policy, and it changes no schema, receipt, operation, deletion target/order,
source/staged behavior, transaction boundary, runtime, M2, or PS1 claim.

Exact fresh-context M4.18 is the sole next packet. James must independently
try to falsify the immutable worker commit and either accept with one written-
exit-gate successor or reject with one bounded correction.

## Git commit if applicable

Intentional worker commit: `fix: use verified mount generation order`.
