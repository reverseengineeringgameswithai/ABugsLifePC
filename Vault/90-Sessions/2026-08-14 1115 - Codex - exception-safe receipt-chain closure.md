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

# Exception-safe receipt-chain closure

## Goal

Complete exact M4.32 by attempting every owned receipt descriptor close once
despite earlier close errors, preserving primary failures, and failing cleanup-
only errors before parsing or mutation.

## Work and evidence

- Refreshed through START HERE and all updated Obsidian control/evidence
  surfaces after M4.31 `REJECT` commit `3ed0ff45969d28bc7a8a46c3e16fa8e16e6b30e5`.
- Reproduced the exact pre-change eight-handle deltas: first close retained +7;
  second close retained +6.
- Added one exhaustive no-retry descriptor-release helper and managed-chain
  error propagation for partial acquisition, reacquisition, and retained
  acquisition.
- Added seven indexed synthetic cases proving each descriptor is attempted
  once, deltas return to zero, primary errors remain primary, cleanup-only
  errors stop before parsing, snapshots remain exact, and CLI stdout is empty.
- Passed 161 focused, 223 combined M4/M1/compatibility, and 411 canonical tests
  before documentation closure.
- Refreshed only the manifest implementation pin to
  `f7fd01144b99f4b93cbbb05faa382c53279114bb60b1a71b0793a755279ad111`.
- Retained all six exact local cycles with prior receipt/output hashes and
  unchanged source hashes.
- Passed final `make check`: Vault 275 notes with zero findings, exact five-
  anchor compatibility, 411 canonical tests, tracked audit zero, and clean
  diff checks.
- Recorded the full result in
  [[EXP-20260814-091 - Exception-safe receipt-handle-chain closure]].

## Conclusion

M4.32 is worker-complete, not accepted. Exact M4.33 is the required
fresh-context audit. M4, `KU-051`, and `KU-052` remain open; no lifecycle,
transaction, runtime, M2, or PS1 work is selected.

## Git commit if applicable

One intentional M4.32 worker commit after final Vault and repository gates.

## Independent disposition

[[EXP-20260814-092 - Independent M4.32 receipt-chain-closure hard-truth audit]]
returns `ACCEPT` after the parent +7/+6 reproduction, 28/28 fresh indexed
partial/nested cleanup cases, exact descriptor order/multiplicity/deltas,
161/223/411 tests, six local cycles, five pins, and nine reads. `KU-051` is
resolved only at this strict boundary. M4 and `KU-052` remain open; exact
M4.34 is the sole clean-derived-copy lifecycle audit successor.
