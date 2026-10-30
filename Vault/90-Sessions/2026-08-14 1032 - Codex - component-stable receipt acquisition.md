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

# Component-stable receipt acquisition

## Goal

Complete exact M4.30 by rejecting the M4.29 checked-parent rename/link
substitution through stable component-by-component acquisition, without
changing receipt content, reconstruction, workflow, output, or removal policy.

## Work and evidence

- Repeated the exact pre-change M4.29 bypass twice: both calls followed the
  substituted parent link into a synthetic protected location and created
  output while retaining the same receipt inode.
- Added retained directory descriptors for the root and every lexical parent,
  relative no-link component acquisition, before/open type-device-inode
  checks, complete final-file metadata checks, and a second whole-chain
  acquisition before receipt parsing.
- Added eight focused cases for replay/removal parent link substitution,
  different parent inode, component inspection/open swap, final hard-link and
  metadata drift, execute-only parent success, exact snapshots, and CLI silence.
- Passed 154 focused manifest tests, 216 combined M4/M1/compatibility tests,
  and 404 canonical tests before documentation closure.
- Refreshed only the existing manifest implementation compatibility pin to
  `091a0431c24637fd8e4618bd09b208ac856c3312c3ebe5f1fb6ba7dcdff0f503`.
- Passed all three exact user-owned local families twice with their prior
  receipt/output hashes, byte-identical replay trees, removed replay roots,
  exact external receipts, and unchanged source hashes.
- Passed final `make check`: Vault 271 notes with zero findings, exact five-
  anchor compatibility, 404 canonical tests, tracked audit zero, and clean
  diff checks.
- Recorded the result and limits in
  [[EXP-20260814-089 - Component-stable external receipt acquisition]].

## Conclusion

M4.30 is worker-complete, not accepted. Exact M4.31 is the required
fresh-context hard-truth audit. M4, `KU-051`, and `KU-052` remain open; no
clean-derived-copy lifecycle, transaction, staged-tree removal, runtime, M2,
or PS1 work is selected.

## Git commit if applicable

One intentional M4.30 worker commit after final repository and Vault gates.

## Independent disposition

Fresh-context M4.31 returns `REJECT` in
[[EXP-20260814-090 - Independent M4.30 component-acquisition hard-truth audit]].
The exact parent acceptance bypass remains corrected, but one close error skips
the remaining receipt-chain descriptors and retains seven or six. Exact M4.32
owns only exception-safe exhaustive descriptor release.
