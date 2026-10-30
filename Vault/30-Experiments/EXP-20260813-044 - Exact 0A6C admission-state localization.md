---
type: experiment
id: EXP-20260813-044
date: 2026-08-13
question: Which smallest non-source inputs and ordered predicates determine exact record 0x0A6C admission before the four-input builder appends?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline native disassembly and Ghidra export review
working_directory: /home/dev/ABLPC
configuration: Exact entry 7 offset 0x0A6C form 0x3C; no runtime
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-exact-0a6c-admission-state-localization.md
addresses:
  - 0x00405FE0
  - 0x00405FFF
  - 0x0040600F
  - 0x004064E4
  - 0x004066BD
  - 0x004069A1
  - 0x0044F951
  - 0x0044F99D
file_offsets:
  - 0x0A6C
result: twenty-three-location-union-twelve-slot-chain-and-payload-free-first-reject-design
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/rendering
---

# EXP-20260813-044 - Exact 0A6C admission-state localization

## Question

Which smallest non-source inputs can affect the mapped no-append branches of
`0x00405FE0` for exact record `0x0A6C`, what is their native evaluation
order, and can an existing safe stop support a metadata-only first-reject
receipt?

## Scope

This packet was offline and PC-native. It backward-sliced only the exact
record's path from builder entry through the last mapped admission rejection.
No game launch, debugger action, source edit, payload retention, parser,
semantic naming, other record/family, original modification, or PS1 evidence
was used.

## Procedure

1. Reverified the authoritative executable hash in a work copy.
2. Reviewed exact native instructions `0x00405FE0..0x004066BD` and caller
   `0x0044F8E0..0x0044F99D`.
3. Independently enumerated the builder's data references from the Ghidra
   export and classified reads versus derived scratch writes.
4. Reduced source-invariant inputs, mutually exclusive conditions, and
   derived values to an ordered exact-record predicate chain.
5. Audited M2.29's existing selector-read pre-call and entry-post boundaries
   for a payload-free future discriminator.

The complete input, arithmetic, predicate, and receipt specification is in
`static/exports/BIN-97c95ba5572dce63/M2-exact-0a6c-admission-state-localization.md`.

## Observed

The union of physical non-source state that can affect admission contains 23
locations: three early page/root values, 17 transform/projection/bounds
dwords, and one depth-policy selector plus two mutually exclusive thresholds.
Native-order
evaluation reads at most 22 values because only one threshold can be active;
it reads 21 when policy mode skips both thresholds.

For exact source-derived mode 2, the no-append path reduces to 12 ordered
logical slots: two page/root gates, four all-input screen-bound gates, one
two-stage orientation gate, one mutually exclusive depth-policy gate, and
four per-input absolute-bound gates. These correspond to 13 concrete reject
PCs because the depth slot has separate mode-0 and mode-1 instructions.

The existing selector-read data watch stops at next PC `0x0044F951` with
`ESI=S` before caller mode construction and the builder call. It is early
enough to transiently evaluate the exact chain without a new execution point
or watch slot. Existing entry-post and counter reconciliation can close the
last entry-7 call and compare predicted with observed append behavior.

## Confirmed

- The physical non-source input union and native read order are exact for
  this executable and exact record path.
- First reject plus evaluated-slot count is sufficient retained predicate
  metadata; a full predicate vector and raw source/global/derived values are
  unnecessary.
- A fail-closed future receipt can reuse existing safe data-watch boundaries
  while retaining zero source or batch payload bytes.

## Inference and limits

The proposed active-state digest and entry-post recheck are a future
coherence design, not runtime evidence. If state changes before entry-post,
the arm must be rejected; the design does not infer when it changed.

No non-source input is selected as the explanation for M2.29's `0/1/0`
outcome because those retained arms did not record predicate state. No
meaning is assigned to the coordinate triples, matrices, bounds, policy
values, record form, or emitted data. Pixel causality and format semantics
remain unproved. Static influence also does not prove that every member of
the union changes per frame; runtime stability is unmeasured.

## Result and follow-up

M2.31 is complete offline. M2.32 should first implement and fixture-test the
purpose-specific native arithmetic evaluator and payload-free schema. Any
fresh control/replacement/control capture remains separately authorized and
must preserve all M2.29 renderer, order, counter, no-flush, signal, cleanup,
detach, survival, and protected-data gates.
