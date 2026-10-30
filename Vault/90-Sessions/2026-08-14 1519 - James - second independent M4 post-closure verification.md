---
type: session
date: 2026-08-14
agent: James
status: completed
tags:
  - session
  - implementation/modding
  - implementation/compatibility
  - audit/hard-truth
---

# Second independent M4 post-closure verification

## Goal

Independently recheck whether M4 remains accepted as recorded at exact
post-closure HEAD, without presuming the prior verdict.

## Result

- Verified exact clean HEAD `33c7c25cd867830af2621f6b7254dc7d8d80bdba`
  over direct parent `6659f865960d56b0ccafcdd44bffd7e96a5333a8`.
- Reconstructed the full 9/9-capability and 5/5-exit-gate ledger from the
  accepted receipt, lifecycle, compatibility, and scope evidence.
- Passed a separately authored 663-assertion temporary-tree matrix covering
  normal/alias/link/nonregular/hard-link/parent-link/unselected paths, read
  timing, CLI behavior, exact statements, recursive order/leaves, strict JSON,
  five pins, and exact nine-read behavior.
- Passed 75 focused, 288 combined, and 476 canonical tests, compatibility,
  `make check`, and repository hygiene gates.
- Returned `ACCEPT` only at the existing asset-free, current-x86_64-Linux,
  explicit-unsupported boundary. Post-`lstat` races and general parent-
  filesystem policy remain unsupported; no successor milestone begins.
- Changed Markdown/README documentation only and did not read or execute any
  game/protected input.

## Durable evidence

See [[EXP-20260814-104 - Second independent M4 post-closure verification]] and
`DEC-20260814-099`.
