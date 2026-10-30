# Exact `0x0A6C` admission-predicate evaluator

## Scope and evidence

This is the offline implementation gate for M2.32, limited to executable
`BIN-97c95ba5572dce63` (SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`),
entry 7/file offset `0x0A6C`/form `0x3C`. The native model comes from the
exact instruction and data-reference audit in
`M2-exact-0a6c-admission-state-localization.md` and `EXP-20260813-044`.
Implementation evidence is `scripts/exact_0a6c_admission.py`, the schema-6
validation/controller changes in `scripts/evidence_lib.py` and
`scripts/gdb-harness.py`, and the synthetic regressions in
`tests/test_exact_0a6c_admission.py`, `tests/test_evidence_lib.py`, and
`tests/test_gdb_harness.py`.

No game was launched or instrumented. No source file, target state, original,
or external repository was changed. No source/global/derived/vertex/index
payload was retained, no new breakpoint or watch slot was introduced, and no
field, primitive, asset, policy, coordinate, or pixel meaning is assigned.

## Purpose-specific native evaluator

`scripts/exact_0a6c_admission.py` implements only the M2.31 exact-record
model. It:

1. validates the source-derived page as 16 and caller mode as 2;
2. reads the 23-location static influence union lazily, with at most 22 active
   dwords because the two depth thresholds are mutually exclusive;
3. reproduces signed-32 low-product/add/subtract wrap, the native negative
   rounding correction before `sar 12`, signed-16 truncation, signed `idiv`
   truncation toward zero, and fail-closed zero-divisor/overflow behavior;
4. evaluates the 12 logical rejection slots in native order, returning one of
   the 13 concrete reject PCs or null;
5. hashes each canonical active address/value pair under a versioned digest
   domain, then retains only the SHA-256 and address list needed for a private
   post-call re-digest; and
6. produces a serialized receipt with no raw source, global, projected, batch,
   vertex, or index value.

The post-call reconciliation repeats the digest over exactly the active
addresses and fails closed on drift. The existing form-specific count delta
remains the observed append authority; a prediction/count mismatch rejects
the capture rather than selecting a predicate.

## Schema-6 fail-closed envelope

Harness 1.5.0 accepts schemas 1 through 6. Its new
`exact_0a6c_admission` mode is not a general expression or predicate engine.
Validation requires all of the following exact values before GDB can attach:

- the executable hash above and an already running, positive PID whose
  `bugs.exe`/Wine-loader/cwd identity matches a work copy (spawn is refused);
- the existing three access data watches only: selector/pre-call
  `0x0059F7F0`, pre-reset marker `0x004C4118`, and entry-post header
  `0x005B18E0`;
- no execution breakpoints, on-stop registers, or on-stop memory reads, and a
  backtrace limit no greater than two PCs;
- the two M2.29 record forms and both audited Direct3D batch-family layouts;
- candidate entry 7, candidate offset `0x0A6C`, allowed root family
  `0x004C4108`, and page 16;
- the accepted 1,000-stop/90-second window, one warmup rollover, one captured
  cycle, and exact required five-sample survival configuration; and
- the complete 168-call plan, canonical SHA-256
  `5eb280a7bd54b56a9654fed7984e9677a15618c5376be703a85718ea3bb2ffec`.

Independent offline comparison of the accepted M2.29 control A, replacement,
and control B specs shows the same 168 items, plan digest, watchpoints, forms,
families, root/page gates, one-rollover/one-cycle bounds, and five-sample
survival configuration in all three. Schema mutation tests reject a changed
plan, watch address, candidate set, executable hash, or raw-output request.

Exact-mode stop records retain trigger identity, PC, timestamps, and bounded
backtrace PCs, but forcibly emit empty register/memory-read collections and a
null watched value. The target row contains only:

```text
schema_version
entry_index=7, file_offset=0x0A6C, form=0x3C
page_16_validated=true, caller_mode_2_validated=true
active_state_sha256, evaluated_predicate_count
first_reject_pc=null|one_of_the_13_concrete_reject_PCs
predicted_append, observed_append, prediction_matches_observation
raw_inputs_retained=false, payload_bytes_retained=0
```

## Synthetic results

The fixture suite passes every specified offline gate:

- early page-class and page-pointer rejects;
- projected slots 3 through 12, covering every concrete reject PC;
- depth mode 0, depth mode 1, and the neither-branch skip, including proof
  that an inactive threshold is not read;
- signed-16 truncation, signed-32 wrap, negative shift correction, signed
  division truncation, zero divisor, and `INT_MIN / -1` failure;
- exact pre/post digest agreement and a changed-state rejection;
- prediction/count disagreement rejection;
- complete-plan acceptance and envelope-mutation rejection;
- a synthetic pre-call/entry-post exact-record path that emits only the
  receipt; and
- forced stop-record redaction plus a serialized receipt key scan.

`make test` passes all 197 repository tests at this implementation gate.

## Confirmed and still unknown

Confirmed offline: the purpose-specific implementation reproduces every
specified native arithmetic/rejection path in fixtures, the accepted M2.29
plan and safety envelope are hash-locked, and retained exact-mode output is
payload-free by construction and regression test.

Not confirmed: agreement against a live exact call, a stable first-reject PC
across two fresh controls, replacement passage, runtime stability of any
input, source causality, or visible causality. Those are still KU-044. A fresh
control/replacement/control capture remains the live phase of M2.32 and
requires new explicit authority; it must preserve renderer/source-hash,
plan/order, root/page, no-flush, signal, cleanup/detach, and survival gates.
