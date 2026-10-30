---
type: session
date: 2026-08-15
agent: Codex
status: completed
tags:
  - session
  - implementation/tooling
---

# 2026-08-15 2033 - Codex - Python C probe split procedure

## Goal

Record a durable procedure for choosing Python versus C during static and
runtime reverse-engineering work.

## Work completed

- Added [[Python and C reverse-engineering split]] as the canonical measured
  language-selection procedure.
- Kept Python as the default reference/controller for offline parsing,
  orchestration, receipts, and low-rate probes.
- Required measured promotion of only the hot loop to C for native ABI,
  high-rate sampling, repeated large scans, or a profiled bottleneck.
- Required a versioned interchange schema, loss accounting, Python/C
  differential fixtures, compiler provenance, runtime ownership, normal write
  authorization, and complete cleanup.
- Linked the procedure from [[Research Method]], [[Runtime Tooling]],
  [[Reverse Engineering MOC]], and [[Implementation MOC]].
- Ran the complete repository gate: 576 tests passed, Vault lint reported
  384 notes/0 errors/0 warnings, all five M4 compatibility anchors remained
  valid, and the tracked-file audit reported 0 violations.

## Result

The project now distinguishes execution speed from investigation throughput
and evidence quality. C is available where measurement justifies it; Python
remains the readable oracle and policy layer unless a later evidence packet
explicitly changes that boundary.

## Next action

Apply the procedure to the next concrete probe. Do not build a C helper until
the packet states a cadence/throughput contract and the Python reference
demonstrates a measured shortfall or native ABI requirement.
