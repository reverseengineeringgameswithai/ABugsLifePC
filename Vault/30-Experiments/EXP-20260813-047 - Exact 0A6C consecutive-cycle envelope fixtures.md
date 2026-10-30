---
type: experiment
id: EXP-20260813-047
date: 2026-08-13
question: What is the smallest payload-free consecutive-cycle envelope that preserves exact 0A6C closure and the accepted stop ceiling?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline controller and validator audit with synthetic fixtures
environment_version: gdb-harness 1.6.0; watch/result schema 6 fixture-only extension
working_directory: /home/dev/ABLPC
configuration: Exact entry 7 offset 0x0A6C form 0x3C; one warmup plus three captured cycles; no runtime
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-exact-0a6c-consecutive-cycle-envelope.md
  - scripts/exact_0a6c_admission.py
  - scripts/evidence_lib.py
  - scripts/gdb-harness.py
  - tests/test_evidence_lib.py
  - tests/test_gdb_harness.py
addresses:
  - 0x0044F951
  - 0x0044C8AB
  - 0x004065B0
  - 0x004069A1
file_offsets:
  - 0x0A6C
result: fixed-three-cycle-envelope-fixture-proven-payload-free
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/dynamic-design
  - re/rendering
  - implementation/tooling
---

# EXP-20260813-047 - Exact 0A6C consecutive-cycle envelope fixtures

## Question

What is the smallest fixed consecutive-cycle count that can express stable
rejection, stable passage, and recurrence while remaining inside the accepted
exact-mode stop/time envelope and retaining only the existing payload-free
receipt?

## Scope and authority

This was only M2.33's offline design gate. The game was not launched or
instrumented, no debugger attached, and no process was controlled. No source
file, target state, original, raw value, other record/family, general `.ALL`
tool, semantic name, or PS1 evidence entered the packet. A live repeated-cycle
arm remains separately authorized work.

## Procedure

1. Reaudited schema-6 validation, exact controller rollover and plan closure,
   result construction, stop redaction, and the existing 1,000-stop/90-second
   ceilings.
2. Recounted all stops in accepted M2.32 exact arms
   `RUN-GDB-20260813-142433`, `-142708`, and `-142853`.
3. Selected three captured cycles after one warmup as the smallest recurrence-
   capable sequence with stop-budget margin.
4. Extended exact mode without changing schema 6 or adding receipt fields.
   Harness 1.6.0 accepts only the legacy one-cycle or fixed three-cycle exact
   bounds.
5. Added fixtures for stable reject, stable pass, alternating reject/pass/
   reject, incomplete-cycle exclusion, unclosed-cycle rejection, exact-bound
   drift, and multi-cycle output exclusion. Existing evaluator fixtures retain
   the within-call digest-drift failure proof.

The complete audit is
`static/exports/BIN-97c95ba5572dce63/M2-exact-0a6c-consecutive-cycle-envelope.md`.

## Observed

Every accepted M2.32 arm used exactly 400 stops for one warmup plus one
captured cycle: 336 pre-selector, 48 entry-post, and 16 flush-marker stops.
The observed rhythm is therefore 200 stops per complete cycle in all three
independent runs. One warmup plus three captured cycles projects to 800 stops,
leaving 200 below the unchanged 1,000-stop ceiling. Four captured cycles would
project to the ceiling with no margin.

The controller appends a cycle only after all 168 plan calls and the exact
candidate sequence close. A synthetic partial third cycle does not appear in
the result and remains `completed: false`. Stable reject, stable pass, and
reject/pass/reject sequences each close only on the third captured cycle.
Serialized results retain only the existing exact receipt metadata and zero-
payload declarations.

The focused exact/evidence/harness suite passes 132 tests.

## Confirmed

- Three is the smallest fixed sequence that can demonstrate an `A/B/A`
  recurrence; two observations can show only one transition.
- The fixed three-cycle envelope remains purpose-specific, uses the same three
  data watches, and adds no raw value or receipt field.
- Schema 6 remains compatible: exact mode accepts legacy one or audited three,
  while other counts fail closed.
- Complete-plan/candidate closure and partial-cycle exclusion already enforce
  the required result boundary.

## Unknown and limitations

This packet produces no live temporal evidence. Whether exact `0x0A6C`
rejects, passes, alternates, or changes its state digest across three cycles in
one unchanged process remains KU-045. The 800-stop figure is a projection from
three independent accepted one-cycle runs, not a newly observed multi-cycle
runtime. No source or visible causality is promoted.

## Result and follow-up

M2.33's offline design gate is complete without a controller or ceiling
blocker. Stop until fresh explicit authority is supplied for a live phase. If
authorized, use one unchanged post-`NextLife` process and change only exact
`capture_cycles` from 1 to 3; preserve every executable, watch, plan, root/
page, renderer, no-raw-output, cleanup/detach, signal, and survival gate.

## Follow-up live result

Freshly authorized
[[EXP-20260813-048 - Exact 0A6C consecutive-cycle live receipt]] executes that
exact arm. It completes at 816 stops and observes reject/pass/reject (`0/1/0`)
with prediction/count agreement, all safety/redaction gates, and distinct
active-state digests. This closes M2.33 at bounded within-process recurrence;
it does not establish a period, distribution, source, visible, or semantic
claim.

## Final validation

- Focused exact/evidence/harness suite: 132 passed.
- Full `make check`: dependency audit passed; Vault lint found 178 notes with
  0 errors and 0 warnings; 203 tests passed; tracked-file audit found 0
  violations.
