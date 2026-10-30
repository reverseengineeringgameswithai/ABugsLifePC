---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - implementation/modding
  - audit/hard-truth
---

# Clean-derived-copy lifecycle audit

## Goal

Determine whether one current tool-created tree can complete installation,
exact validation, launcher preflight, and supported removal without borrowing
successes from separate staged and sparse outputs.

## Work and evidence

- Verified clean exact M4.33 verdict
  `1ddb12850a48e4501d60688c6071c7ce2fed8ba1` directly above M4.32 worker
  `e396ab0e90ede2dd29f4c7b98fd434ed867236a5` and repeated the required
  startup/context refresh.
- Built fresh synthetic complete source trees and independently compared
  `stage`, sparse `apply`, `apply --force` into a clean copy, and receipt
  replay. All returned equal receipts and exact output hashes.
- Recorded complete no-follow snapshots. Both complete-tree removal attempts
  failed before mutation at status 2 with empty stdout; both sparse removals
  succeeded and removed their roots.
- Exercised launcher dry-run only. Full trees below `work/copies/` reached the
  deliberately synthetic executable-hash rejection; the documented
  `work/mod-builds/` path rejected at the launcher path gate. No game ran.
- Repeated all three exact local apply/replay/remove families twice with prior
  receipt/output/source hashes; canonical tests passed 411/411 and the exact
  five-anchor compatibility statement remained valid.

## Conclusion

M4.34 returns `REJECT` for M4 completion. Complete derived trees are not
supported removal targets, while supported removal targets are not complete
game trees. [[EXP-20260814-093 - Clean-derived-copy lifecycle feasibility audit]]
records the exact four-route ledger and selects one missing join only:
manifest/source-authenticated restoration of an exact complete staged copy.

## Git commit if applicable

Intentional documentation-only M4.34 verdict commit.
