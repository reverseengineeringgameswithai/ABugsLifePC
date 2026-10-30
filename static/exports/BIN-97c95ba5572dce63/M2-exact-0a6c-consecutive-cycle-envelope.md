# Exact `0x0A6C` consecutive-cycle envelope

## Scope and evidence

This is M2.33's offline design and fixture gate for executable
`BIN-97c95ba5572dce63` (SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`),
entry 7/file offset `0x0A6C`/form `0x3C`. It extends only the exact schema-6
receipt implemented in `EXP-20260813-045` and live-validated for one captured
cycle per process in `EXP-20260813-046`.

Implementation evidence is the fixed bound in
`scripts/exact_0a6c_admission.py`, exact-envelope validation in
`scripts/evidence_lib.py`, controller/capability output in
`scripts/gdb-harness.py`, and regressions in `tests/test_evidence_lib.py`,
`tests/test_gdb_harness.py`, and `tests/test_exact_0a6c_admission.py`.

No game was launched or instrumented. No process, source file, target state,
original, or external repository was changed. No raw source, global,
projected, vertex, index, or watched value was retained, and no watchpoint,
execution point, record, family, semantic name, or general `.ALL` surface was
added.

## Fixed bound

The exact consecutive envelope is three captured cycles after the existing
one warmup rollover:

```text
warmup cycle (not retained)
captured cycle 0 -> exact payload-free receipt
captured cycle 1 -> exact payload-free receipt
captured cycle 2 -> exact payload-free receipt -> capture_complete
```

Three is the smallest useful temporal sequence. Two observations can show one
transition, but cannot show recurrence; three can encode stable reject,
stable pass, or an `A/B/A` alternating pattern without widening the receipt.

The count also stays inside the accepted M2.32 ceiling. Each accepted exact
M2.32 arm (`RUN-GDB-20260813-142433`, `-142708`, and `-142853`) completes one
warmup plus one captured cycle in exactly 400 stops, identically divided into
336 pre-selector, 48 entry-post, and 16 flush-marker stops. That is 200 stops
per complete cycle in all three independent runs. One warmup plus three
captured cycles therefore projects to 800 stops, leaving 200 stops beneath
the unchanged 1,000-stop bound. Four captured cycles would project to exactly
1,000 stops and leave no stop-budget margin, so it is rejected by the exact
validator even though the generic batch controller permits larger counts.
The unchanged 90-second timeout remains a separate fail-closed ceiling; the
projection is a design bound, not new live evidence.

## Controller and result audit

The existing record controller already provides the required closure:

- a rollover is accepted only after all 168 canonical plan calls have been
  consumed in order;
- the captured candidate offset sequence must equal exactly `[0x0A6C]`;
- only then is one `{cycle_index, records}` object appended;
- `capture_complete` occurs only after the requested number of complete
  captured cycles; and
- `current_records` and `pending` are not serialized, so a timeout or
  max-stops endpoint during the third cycle retains only the prior two
  complete cycles and reports `completed: false`.

Harness 1.6.0 keeps watch/result schema 6 and schemas 1 through 5 compatible.
Exact mode accepts only `capture_cycles=1` for the already live-validated
legacy envelope or `capture_cycles=3` for M2.33. Counts 2, 4, and 8 are
explicitly rejected. All other exact locks remain unchanged: executable and
paused work-copy identity, the existing three data watches, no execution
breakpoints or raw on-stop output, forms/families/root/page, one warmup,
1,000 stops, 90 seconds, required survival receipt, and canonical 168-call
plan SHA-256
`5eb280a7bd54b56a9654fed7984e9677a15618c5376be703a85718ea3bb2ffec`.

Every captured cycle retains only the existing receipt fields:

```text
schema_version
entry_index=7, file_offset=0x0A6C, form=0x3C
page_16_validated=true, caller_mode_2_validated=true
active_state_sha256, evaluated_predicate_count
first_reject_pc=null|one_of_the_13_concrete_reject_PCs
predicted_append, observed_append, prediction_matches_observation
raw_inputs_retained=false, payload_bytes_retained=0
```

## Fixture results

Synthetic regressions prove:

- three stable slot-7 rejection receipts close in order;
- three stable full-pass receipts close in order;
- reject/pass/reject closes in order and preserves the three outcomes;
- pre/post active-state digest drift fails closed before a receipt can be
  appended;
- a cycle that does not consume the complete record plan is rejected;
- an incomplete final cycle is not emitted and cannot be marked complete;
- exact counts other than legacy one or fixed three are rejected; and
- serialized multi-cycle results exclude source/classification/projected,
  vertex/index, watched, register, memory-read, and payload values.

The focused exact/evidence/harness suite passes 132 tests. The repository-wide
count is recorded in `EXP-20260813-047` after the final full check.

## Confirmed and still unknown

Confirmed offline: three captured cycles is a fixed, purpose-specific,
payload-free envelope with complete-cycle closure, fail-closed partial-cycle
handling, and stop-budget margin under the previously observed exact rhythm.

Still unknown: whether one unchanged process is stable, alternates, or changes
its first reject or active-state digest; whether another process follows the
same sequence; and whether any temporal behavior has source or visible
causality. A live M2.33 arm remains separately authorized. If authorized, it
must attach only after the logged `NextLife` boundary and change only
`capture_cycles` from 1 to 3 inside this locked envelope.
