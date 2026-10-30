---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - implementation/modding
  - implementation/manifest
  - audit/correction
---

# Complete output plan preflight correction

## Goal

Execute exact corrective packet M4.3 after James rejected M4.1's complete
output-preflight claim, preserve the surviving exact replacement boundary, and
leave a clean worker commit for fresh-context M4.4 verification.

## Files inspected

- The complete startup sequence and relevant Implementation MOC
- `DEC-20260814-055/056`, exact M4.3 roadmap packet, and
  `EXP-20260814-060/061`
- [[M4 Exact Whole-file Replacement]] and [[M1 Tool Support Matrix]]
- `reimplementation/ablpc/manifest.py`, `tests/test_manifest.py`, existing M1
  tests, CLI documentation, tracked manifest, and ignored local corpus

## Work performed

- Added a complete planned-write preflight containing every manifest
  destination and `.ablpc/receipt.json`.
- Added `lstat`-based rejection for symlinked/non-directory ancestors and
  symlinked/non-regular destinations, including forced destinations.
- Rejected symlinks in the requested output-root path before canonicalization.
- Preflighted the source topology that `stage` would copy for all planned
  destinations and the fixed receipt before `copytree`.
- Routed the receipt through the retained output containment helper.
- Added the four exact M4.2 regressions, a positive forced-regular-file test,
  and an adjacent output-root symlink regression.
- Updated CLI documentation and durable Vault records while preserving the
  explicit non-transactional limitation.

## Conclusion

M4.3 is worker-complete in
[[EXP-20260814-062 - Complete planned-output containment preflight correction]].
All four James reproductions now raise `ManifestError` before mutation, and the
surviving M4.1 behavior remains green. This is not independent acceptance;
exact fresh-context M4.4 is next under the M4 ratchet.

## Tests run

- Focused manifest/LEVEL suite: 47 passed.
- Full repository suite: 235 passed.
- Explicit schema-2 M1 operations: 3/3 passed with source preservation and
  receipt/output-hash agreement.
- Exact ignored local recipe: input/source/output hashes, byte equality,
  sparse locality, receipt equality, and source preservation passed.
- Vault lint, tracked-file audit, diff checks, staged review, and final clean-
  tree check are required after all Vault edits.

## Exact next action

Commit M4.3 intentionally with a clean tree, then send that immutable commit
to a fresh-context James session for exact M4.4. Do not begin another technical
M4 capability before the verdict.

## Git commit if applicable

`fix: preflight complete M4 output plan`
