---
type: experiment
id: EXP-20260813-045
date: 2026-08-13
question: Does the purpose-specific exact-0A6C evaluator reproduce every specified native path while retaining only the payload-free receipt?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline Python implementation and synthetic fixtures
environment_version: gdb-harness 1.5.0; watch/result schema 6 fixture-only
working_directory: /home/dev/ABLPC
configuration: Exact entry 7 offset 0x0A6C form 0x3C; no runtime
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-exact-0a6c-admission-predicate-evaluator.md
  - scripts/exact_0a6c_admission.py
  - tests/test_exact_0a6c_admission.py
addresses:
  - 0x00405FFF
  - 0x0040600F
  - 0x004064E4
  - 0x004066BD
  - 0x0044F951
  - 0x0044C8AB
file_offsets:
  - 0x0A6C
result: offline-native-path-and-payload-free-schema-gates-pass
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/dynamic-design
  - re/rendering
  - implementation/tooling
---

# EXP-20260813-045 - Exact 0A6C admission evaluator fixtures

## Question

Does the purpose-specific native-arithmetic evaluator specified by M2.31
reproduce every exact `0x0A6C` rejection path, preserve the accepted M2.29
capture envelope, fail closed on incoherence, and serialize no protected raw
values?

## Scope and authority

This was only M2.32's offline implementation gate. The game was not launched
or instrumented, no debugger attached, and no process was controlled. No
source file, target state, original, payload, other record/family, general
`.ALL` tool, semantic name, or PS1 evidence entered the packet. Live matched
arms remain separately authorized work.

## Procedure

1. Reverified the exact work-copy executable hash and M2.31 arithmetic,
   predicate, and receipt specification.
2. Implemented a standalone exact-record evaluator with explicit signed-32
   wrap, signed-16 truncation, native signed division, active-state digesting,
   and the ordered first-reject result.
3. Extended the compatible read-only harness to 1.5.0/schema 6 with an
   `exact_0a6c_admission` mode. Its validator hash-locks the executable and
   168-call plan, requires the existing three data watches and M2.29 batch
   gates, and forbids raw stop output.
4. Independently compared all three accepted M2.29 specs. Each has the same
   canonical 168-call plan digest
   `5eb280a7bd54b56a9654fed7984e9677a15618c5376be703a85718ea3bb2ffec`
   and the same fixed watch/form/family/order/root/page/survival envelope.
5. Added fixtures for every reject PC, depth branch/skip, arithmetic and
   digest failure, count mismatch, plan/envelope drift, exact controller
   closure, and retained-output exclusion.

The complete implementation and fixture audit is in
`static/exports/BIN-97c95ba5572dce63/M2-exact-0a6c-admission-predicate-evaluator.md`.

## Observed

All 13 concrete reject PCs across the 12 logical slots are selected at the
expected evaluated-slot counts. Both depth threshold branches and the skip
pass; the skip does not read either threshold. Zero divisor and signed
division overflow fail closed. A pre/post digest change fails closed, and a
prediction/count disagreement is rejected.

The schema-6 exact envelope accepts the unchanged audited 168-call plan and
rejects mutations to the plan, data watches, candidate set, executable hash,
or raw register/memory output. Synthetic exact pre-call/entry-post closure
emits only the M2.31 row. Stop-record redaction emits no register, watched, or
memory-read value. `make test` passes all 197 tests.

## Confirmed

- The exact evaluator and receipt schema satisfy every specified offline
  M2.32 gate.
- The implementation is purpose-specific and compatible with schemas 1–5.
- Retained exact-mode output contains first-reject/count/digest/append
  metadata and explicit zero-payload declarations, not protected raw values.
- No new breakpoint or watch slot is needed by the implementation.

## Unknown and limitations

No fixture proves live agreement, temporal stability, a control first reject,
replacement passage, source causality, or pixel causality. Harness 1.5.0/
schema 6 exact mode is fixture-validated only; schemas through 5 retain their
prior live status. KU-044 remains active for the separately authorized live
control/replacement/control phase of M2.32.

## Result and follow-up

M2.32's offline gate is complete without a mismatch. Stop here until fresh
explicit authority is supplied for its live phase. Any accepted arms must use
the exact schema-6 envelope and preserve the M2.29 renderer/source-hash,
plan/order, root/page, no-flush, signal, cleanup/detach, and five-sample
survival gates. If controls disagree, prediction/count differs, or the digest
changes, record that ambiguity rather than selecting an input.

## Subsequent live result

The user's later explicit instruction authorized
[[EXP-20260813-046 - Exact 0A6C live admission receipt]]. Schema 6 agrees with
the native count outcome in all three accepted arms, but the fresh pattern is
`0/0/1`: control A and the replacement reject at `0x004065B0`, while control B
passes. M2.32 therefore completes under its temporal-ambiguity condition; this
offline fixture result remains unchanged.
