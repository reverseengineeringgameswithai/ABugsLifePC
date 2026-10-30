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

# Manifest-driven clean-copy restoration

## Goal

Close the sole M4.34 same-tree lifecycle join without weakening dedicated
sparse removal: restore one exact complete staged copy from its authenticated
manifest and clean source.

## Work and evidence

- Repeated START HERE and exact M4.35 from clean M4.34 commit
  `a8012745183124d5ed84fe915a5867cbb2b8146b`.
- Added `restore MANIFEST --source-root SOURCE --game-root ROOT` with complete
  no-follow source/game inventory, regular single-link enforcement, exact
  unrelated-content equality, recorded output/receipt authentication, and
  full-tree mount/ancestry preflight before mutation.
- Success restores only recorded destinations, removes receipt/empty `.ablpc`,
  preserves source, and leaves full path/type/content equivalence. Sparse
  remove/replay behavior is unchanged.
- Added 27 focused instances across schemas 1/2, all four operations, opaque/
  multi/composed success, deterministic authority/tree/nonregular failures,
  CLI silence, and four private mount namespaces. Tests pass 188/250/438.
- Ran one exact 722-file full-tree lifecycle below `work/copies/`: stage,
  accepted launcher dry-run, restore, exact content snapshot, exact source,
  and automatic cleanup. No game ran.
- Repeated all six retained sparse local cycles with prior hashes. The exact
  five-pin/nine-read compatibility contract survives with manifest pin
  `4707c93e5d57b7d8b833547bb3c5d7e5c0b735ba1c772ceb3e43a5546e2b004d`.

## Conclusion

M4.35 is worker-complete. [[EXP-20260814-094 - Manifest-driven clean-copy restoration]]
records the exact boundary and limitations. M4 and `KU-052` remain open until
fresh-context M4.36. The compatibility statement remains conservatively
unchanged at this unverified worker edge and will require a separate alignment
packet after behavioral acceptance.

## Git commit if applicable

Intentional M4.35 worker commit with implementation, focused tests, pin refresh,
and documentation only; no game bytes or protected content.
