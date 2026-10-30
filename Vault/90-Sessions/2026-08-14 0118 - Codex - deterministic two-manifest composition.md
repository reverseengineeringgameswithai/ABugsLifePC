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

# Deterministic two-manifest composition

## Goal

Execute exact worker packet M4.5 after independent M4.4 acceptance, preserve
all accepted output-topology/schema/receipt boundaries, and leave one clean
worker commit for fresh-context M4.6.

## Files inspected

- The complete [[START HERE]] startup sequence, Project Charter, and Agent
  Operating Manual
- `DEC-20260814-055/058`, exact M4.5 roadmap packet, and
  `EXP-20260814-060` through `EXP-20260814-063`
- [[M4 Exact Whole-file Replacement]] and [[M1 Tool Support Matrix]]
- Manifest/CLI/LEVEL code, all manifest/LEVEL tests, tracked exact manifests,
  and the ignored user-owned local corpus

## Work performed

- Added `compose LEFT RIGHT --source-root ROOT` for exactly two existing
  schema-1/schema-2 manifests.
- Canonicalized input hashes/order, derived exact half-open claims from the
  existing offset-located operations, and emitted an existing-schema combined
  manifest only for disjoint cross-manifest claims.
- Added deterministic compact JSON conflicts for M1 byte overlap, opaque
  same-destination claims, Windows-path ambiguity, format/hash mismatch, and
  cross-manifest replacement-source/destination collision.
- Added reversed-order success/conflict, exact 12/2/4-byte spans, no-output
  rejection, apply/stage equivalence, source preservation, schema-selection,
  hash normalization, and CLI tests.
- Documented the exact two-manifest and asset-free boundary.
- Composed and applied the two tracked same-DAT manifests and an M1-plus-exact-
  opaque pair against the ignored local work copy using only hashes and byte
  equality.

## Conclusion

[[EXP-20260814-064 - Deterministic two-manifest composition and conflict report]]
records M4.5 worker-complete. Reversed success and conflict outputs are
deterministic, synthetic apply/stage results match independently calculated
bytes, and the exact local pairs preserve source hashes and sparse locality.
This is not independent acceptance; exact fresh-context M4.6 is next under the
M4 ratchet.

## Tests run

- Focused manifest/LEVEL suite: 58 passed.
- Complete scoped repository suite: 246 passed.
- Exact same-file local pair: forward/reverse JSON equal; sparse output and
  source preservation pass.
- Exact different-file M1/schema-2 pair: forward/reverse JSON, independent M1
  output equality, opaque output hash, sparse locality, and source preservation
  pass.
- Vault lint, tracked-file audit, diff checks, staged review, and final clean-
  tree check are required after all Vault edits.

## Exact next action

Commit M4.5 intentionally with a clean tree, then send that immutable commit
to a fresh-context James session for exact M4.6. Do not begin another technical
M4 capability before the verdict.

## Git commit if applicable

`feat: compose exactly two manifests`
