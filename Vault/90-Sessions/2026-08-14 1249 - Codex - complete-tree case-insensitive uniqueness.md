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

# Complete-tree case-insensitive uniqueness

## Goal

Implement only exact M4.37 after M4.36 proved that complete restoration accepts
distinct Linux paths that collide under the project's Windows-case model.

## Work and evidence

- Repeated START HERE and the exact M4.37 packet from clean docs-only M4.36
  verdict `7180e4a7d41e125307a2b32a3f1f6cb726d20b3d`.
- Reproduced all eight source/staged file/file, directory/directory,
  file/directory, and nested collision failures before implementation.
- Added one case-folded relative-path uniqueness map to the shared complete-
  tree inventory and moved source inventory ahead of manifest preparation.
- Added eight parameterized snapshot-preserving regressions with explicit
  preparation/content-read/write/unlink traps at the applicable boundary.
- Added two uppercase-first directory cases proving the sibling keys are all
  validated before either ambiguous branch is descended.
- Passed 198 focused, 260 combined, and 448 canonical tests plus the 6-case
  tracked restoration mount/order selector and five-anchor compatibility
  check.
- Repeated the exact 722-file/26-directory stage, launcher dry-run, restore,
  source-preservation, and cleanup lifecycle without game execution.
- Repeated all six sparse local cycles with their prior receipt/output hashes.
  The statement remains byte-exact; only the manifest implementation pin is
  refreshed to `b3480761ac2b4791ccbf1df69f88234532f27956152045b89615dd5ec5bf6d75`.

## Conclusion

Exact M4.37 is worker-complete at
[[EXP-20260814-096 - Complete-tree case-insensitive path uniqueness]]. M4 and
`KU-052` remain open. Only audit/docs M4.38 may follow; statement alignment is
not selected at this worker edge.

## Git commit if applicable

One intentional M4.37 worker commit with implementation, tests, pin refresh,
and required documentation only; no game or protected bytes.

## Disposition

Fresh-context [[EXP-20260814-097 - Independent M4.37 complete-tree-uniqueness hard-truth audit]]
accepts this immutable worker after stronger separate-oracle, bind-mounted
sibling-order, eight-family namespace, local lifecycle, sparse, compatibility,
and canonical checks. `KU-052` resolves only for that demonstrated current-
Linux lifecycle; M4 continues on exact M4.39 statement alignment.
