---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - implementation/release
  - implementation/compatibility
  - milestone/m6
---

# M6 installed lifecycle identity correction

## Agent

Codex

## Goal

Close only the three `EXP-20260814-106` installed-lifecycle contradictions,
validate the retained M6 evidence, and freeze a clean worker result for James.

## Changes made

- Made all four packaged Python entry points suppress bytecode generation.
- Replaced state `exists()` admission with non-following `lstat()` identity.
- Added reusable non-link directory admission for install/release/version roots
  and applied it across install/current/rollback.
- Added exact installed-entry-point and full topology/content snapshot tests
  across dangling state and linked root/version attacks.
- Updated machine and user documentation with the corrected boundary and
  explicit concurrency/filesystem limits.

## Conclusions

- All original hard-truth failures and adjacent lifecycle forms now reject or
  preserve the exact installed inventory as declared.
- Exact implementation commit `580a1cb` produces matching 389,120-byte
  archives at `7a1ede97...fcd2`, source tree `fa6a3ee4...c85ea`.
- The exact 21-file/three-case smoke report passes at `1a8a3b57...323e`.
- 492 tests, five M4 anchors, Vault, protected-content, diff, and clean gates
  pass without changing M4 or game-facing behavior.
- M6 remains Active pending fresh-context James acceptance.

## Contradictions discovered

The first dangling-state regression exposed that install created an empty
`releases/` directory before rejecting the state link. Reordering state
admission before release-directory creation restored full snapshot
preservation. No contradiction remains at the worker boundary.

## Recommended next action

Have James independently reproduce the original and adjacent attacks at the
exact clean worker boundary. A rejection becomes the next smallest correction;
only acceptance closes M6.

## Git commit if applicable

- `580a1cb` - `fix: harden M6 installed lifecycle`
- worker evidence documentation commit pending at note creation
