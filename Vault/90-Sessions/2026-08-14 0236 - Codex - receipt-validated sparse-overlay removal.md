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

# Receipt-validated sparse-overlay removal

## Goal

Execute exact M4.9 after the mandatory post-M4.8 startup refresh, implement
only receipt-validated removal of dedicated ordinary sparse overlays, preserve
all source and accepted M4 behavior, update the durable Vault, and leave one
clean worker commit for fresh-context James review.

## Startup and scope

Read the complete [[START HERE]] chain: full [[Current State]], full
[[Project Roadmap]], full [[Environment Status]], full [[Decision Log]], full
[[Known Unknowns]], relevant implementation/experiment MOCs,
[[Agent Operating Manual]], and [[Project Charter]]. Also read exact
`EXP-20260814-067`,
[[M4 Exact Whole-file Replacement]], [[M1 Tool Support Matrix]], the M4.8
session, README, manifest/CLI implementation, and existing tests. M2 remained
deferred and the external PS1 tree was not consulted.

## Work performed

- Added `remove MANIFEST --source-root SOURCE --overlay-root ROOT`.
- Reused `_prepare_manifest` and factored the unchanged ordinary receipt into
  shared construction/encoding helpers.
- Added strict receipt parsing, byte-exact ordinary receipt comparison, output
  hash checks, regular-file topology checks, and a no-follow exact-tree walk.
- Preflighted the complete deletion plan before unlinking only recorded sparse
  outputs and the receipt, then pruning authenticated empty directories/root.
- Added 32 parameter-expanded synthetic cases for success, empty output,
  composition, hard-link refusal, receipt/source/output drift, missing/symlink/
  FIFO paths, extra content,
  staged-tree refusal, root safety, exact snapshots, and CLI behavior.
- Ran three exact user-owned local manifest families twice through apply/remove
  with deterministic receipts, complete overlay removal, and unchanged source
  hashes.
- Updated the required implementation, roadmap, state, unknown, decision,
  MOC, README, experiment, and session surfaces.

## Evidence and tests

- [[EXP-20260814-068 - Receipt-validated sparse-overlay removal]]
- Focused manifest/LEVEL suite: 95 passed.
- Complete scoped suite: 283 passed in 6.72 seconds before documentation.
- Final `make check`: 283 passed in 6.05 seconds; Vault lint 229 notes with 0
  errors/warnings; tracked-file audit 0 violations.
- Exact local apply/remove: 2/2 for each of opaque, same-DAT composed, and
  M1-plus-opaque composed families.
- Post-hard-link local reproduction repeated all three families at 2/2 with
  every overlay absent and all source hashes unchanged.
- Local source hashes remained `494d...5a22`, `a2f2...4ac6`, and
  `6e5a...79a4`.
- No original, game asset, runtime state, external source, schema, or receipt
  field changed.

## Conclusion

M4.9 is worker-complete at the dedicated current-version sparse-overlay
boundary, not independently accepted. Exact M4.10 fresh-context hard-truth
review is the sole next packet. General rollback, staged-tree removal, source
restoration/deletion, launch, compatibility, dry-run, `.ALL`, M2, and PS1
remain outside scope.

## Git commit if applicable

Intentional worker commit: `feat: remove authenticated sparse overlays`.
