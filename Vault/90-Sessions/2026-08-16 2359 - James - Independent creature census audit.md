---
type: session
date: 2026-08-16
agent: James
status: reject-corrected
tags:
  - session
  - re/audit
  - research/coverage
---

# Independent creature census audit

## Agent

James, fresh context, no knowledge of the worker session.

## Goal

Try to break [[EXP-20260816-172 - PC creature actor pool and behaviour VM census]]
at clean HEAD `de7b80d`, re-deriving every claim from the binary rather than
trusting the worker's tables.

## Files inspected

The census export, the experiment note, both new function dossiers and the
three amended ones, the coverage map rows, `KU-068`/`KU-069`, and the
propagated claims in Current State, the roadmap, the MOCs and the worker
session note. For prior art:
`M2-fixed-pool-index-producer-census.md`,
`M2-generic-resource-index-producer-census.md` and
`M2-signed-selector-producer-provenance.md`. Binary:
`work/copies/BUGS_PC-full-disc/bugs.exe`.

## Experiments inspected

`EXP-20260813-056` (the producing experiment for the M2 fixed-pool census) and
`EXP-20260815-128` (for the Flik position globals opcode 16 compares against).

## Changes made

None by the auditor — the audit was read-only and committed nothing. The
corrections it required were applied afterwards by the worker in the commit
that records [[EXP-20260816-173 - Independent creature census audit]].

## Conclusions

**REJECT**, on the register rather than the analysis. Every number in the
packet reproduced: the opcode-size map re-derived independently before reading
the worker's table, 463 instructions, zero misalignment, 69 branch targets on
boundaries, an identical histogram, both switch tables entry by entry, both
loop terminations, every thunk and caller, the `KU-069` arithmetic, and the
`CreatListRam` anchor at its exact site.

Seven defects, listed in the audit note. The two that gate: a Confirmed bullet
claiming the builder writes both a count and a thunk "per type", which is true
for 9 of 36 types and false for 27; and a "handler's own range check"
attributed to opcode 13, which has no check at all — one of the four
validations the packet led with.

## New hypotheses

None. The audit produced no new model, only one new unrecorded fact: a third
unbounded table index at `0x0041BD45`.

## Contradictions discovered

None between this packet and accepted prior work. The strongest candidate —
`M2-fixed-pool-index-producer-census.md`'s claim that `0x0041DC60` never
writes record `+0x00` — was checked and holds.

## Tests run

`make vault-lint` 488/0/0 and `make audit-tracked` 0 violations, both matching
the subject commit. `make test` **first** invocation `685 passed, 1 failed` of
686 at `tests/test_input_movie.py::test_log_anchor_uses_only_new_log_bytes`,
`anchor_timeout` / `NextLife.`; second invocation `686 passed in 18.53s`.
Recorded as a third independent `KU-065` recurrence.

## Unresolved questions

`KU-068`, the broadened `KU-069`, the extent of the `0x004C881F` table, and
the producer of the `+0x6E` value `0x3E6` that gates the `0x0059D99E`
decrement.

## Recommended next action

Apply all findings, then re-audit from a fresh context. Both coverage-row
promotions should survive the correction unchanged.

## Git commit if applicable

None by the auditor. Findings recorded in the worker's correction commit.
