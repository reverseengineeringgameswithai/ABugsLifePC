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

# Strict receipt reconstruction for replay and removal

## Goal

Complete exact M4.28: make one current ordinary receipt plus exact source
sufficient for dedicated sparse replay and removal without the original
manifest, while retaining current bytes, schemas, operations, guards, topology
checks, and manifest-driven workflows.

## Work and evidence

- Added strict descriptor-based external receipt acquisition, exact ordinary
  byte validation, current-operation receipt-to-manifest reconstruction, and
  complete source/preparation/recomputed-receipt equality before mutation.
- Added `ablpc-mod replay` with a new-root-only sparse destination and
  `ablpc-mod remove-receipt` using the shared accepted removal implementation.
- Kept the receipt and manifest schemas, four operations, receipt bytes, and
  existing manifest commands unchanged.
- Added 47 focused cases across schemas 1/2, every operation, no-op and unequal
  opaque extents, composition, malformed/duplicate/reordered authority,
  hashes/indices/paths, descriptor races, nonregular topology, later failure,
  removal drift, exact snapshots, and CLI silence.
- Passed 146 focused, 208 combined M4/M1/compatibility, and 396 canonical tests.
- Passed final `make check`: Vault lint 267 notes with zero findings, exact
  five-anchor compatibility valid, 396 canonical tests, and tracked audit zero.
- Refreshed only the manifest implementation compatibility pin to
  `59c275c5a6d7f539b4664130102035d90ecc6c0d587a09e90688115268e0e240`;
  the exact statement/five-pin membership/nine-read boundary remains.
- Replayed and removed all three established user-owned local families twice
  from external receipts with deterministic prior receipt/output hashes and
  unchanged source hashes.
- Recorded the full worker result and limits in
  [[EXP-20260814-087 - Strict receipt reconstruction for replay and removal]].

## Conclusion

M4.28 is worker-complete and exact M4.29 is the required fresh-context
hard-truth audit. The receipt is a bounded operational authority, not a
signature/provenance proof, and post-preflight I/O remains non-transactional.
M4 remains active because the separate clean-derived-copy lifecycle gate is
still open.

## Git commit if applicable

Intentional M4.28 worker commit after final Vault and repository gates.
