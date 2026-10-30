---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - implementation/release
  - milestone/m6
---

# M6 state-locked lifecycle consistency correction

## Goal

Close the complete James `EXP-108` rejection packet, retain all passing M6
gates, and freeze the next clean ratchet tooth.

## Changes made

- Added interpreter-start `-B` for the direct compatibility entry point.
- Made state/release creation ordering fail without topology mutation.
- Enforced canonical single-link files and exact release/package topology and
  modes across every installed version and lifecycle operation.
- Added canonical state schema 2 archive/manifest/tree locks and canonical
  archive reconstruction for installed content.
- Made state temporary ownership unique and cleanup local.
- Expanded full-snapshot release regressions from 13 to 30.

## Conclusions

- James's accepted invalid families and the content/manifest rebaseline now
  reject at the worker boundary.
- Exact clean HEAD `7d8594e` produces matching 399,360-byte artifacts at
  `68d3d31a...060b`, exact smoke `c1fb6903...98dc`, and 509 passing tests.
- M6 remains Active for James re-audit only.

## Git commits

- `46fa294` - `fix: enforce M6 lifecycle consistency`
- `7d8594e` - `fix: lock M6 installed release identities`
- worker evidence documentation commit pending at note creation
