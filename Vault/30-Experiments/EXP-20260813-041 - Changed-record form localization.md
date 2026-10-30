---
type: experiment
id: EXP-20260813-041
date: 2026-08-13
question: Which exact changed record offsets and forms inside the 13 M2.27 entries are consistent with each measured Direct3D builder-count delta?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora offline exact-two-file and retained-metadata analysis
environment_version: Python 3.14.6; GNU objdump 2.44; retained gdb-harness 1.3.0/schema 4 receipts
working_directory: /home/dev/ABLPC
configuration: Exact M2.20 files; exact M2.27 13-entry set; two retained cycles in each control/replacement/control arm; offsets/forms/counts only
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-changed-record-form-localization.md
  - dynamic/wine/EXP-20260813-040-comparison.txt
  - dynamic/wine/RUN-GDB-20260813-113620
  - dynamic/wine/RUN-GDB-20260813-113842
  - dynamic/wine/RUN-GDB-20260813-113954
addresses:
  - 0x00405FE0
  - 0x00407450
  - 0x0044F8E0
  - 0x0044F951
  - 0x0044F99D
  - 0x0045026C
  - 0x0045029F
file_offsets:
  - 0x0174
  - 0x0858
  - 0x0AA4
  - 0x2578
result: eighteen-entry-form-groups-124-records-three-exact-record-outcomes
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/rendering
---

# EXP-20260813-041 - Changed-record form localization

## Question

Within exact M2.27 candidates
`{1,2,4,5,6,7,9,10,14,15,18,19,20}`, which changed record offsets/forms
reached by the proven retained-stream walk are consistent with each measured
four-input/three-input Direct3D builder-count delta?

## Inputs and procedure

- Reverified executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`,
  unchanged-file SHA-256
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`,
  and replacement-source SHA-256
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
- Reapplied only `EXP-20260813-037`'s exact two-file retained intervals,
  `0x24/0x30` walks, forms, and difference-presence classification.
- Checked native form selection, the `0x3C` pre-call table gate, renderer-
  selector branches, call sites, and the builders' later runtime admission
  gates against exact `objdump` disassembly.
- Reanalyzed the already retained metadata-only stop sequences from both
  complete cycles of all three accepted `EXP-20260813-040` arms. Stop PC
  identifies form; `ESI` identifies the current record pointer. No payload
  memory read was added or retained.
- Compared replacement per-form append totals against the inclusive envelope
  between the two independent controls. Retained only forms outside that
  envelope and recorded the minimum aggregate count gap.

No runtime was launched, no debugger state or file was changed, no parser or
editor was created, no payload byte value was retained, and no PS1 source was
consulted.

## Expected

The offline call predicates and form counts should select the smallest exact
record/form set consistent with every M2.27 delta or expose a precise native
predicate/count contradiction.

## Observed

- Each accepted M2.27 arm retains two complete ordered cycles with 126
  `0x3C` pre-call stops, 42 `0x34` pre-call stops, and 24 entry-post stops per
  cycle. Exact offset/form call sets match across all six cycles.
- Of 183 walked records, 168 reach a builder. All 15 omissions are the five
  `0x3C` records in each of entries 21–23, already outside the 13-entry set.
- Every one of the 145 changed records inside the 13 entries reaches its
  selected builder in every cycle. Pre-call predicates do not explain the
  count deltas.
- This corrects M2.27's `B4/B3` “call” label: the decomposed values are
  completed append paths, not all function entries. M2.27's measurements and
  13-entry discriminator remain unchanged.
- Replacement totals outside both-control per-form envelopes select 18 exact
  entry/form groups containing 124 changed records. Their minimum count gaps
  sum to 30 append outcomes.
- Three single-record groups identify exact bounded append-outcome changes:
  file offsets `0x0174` and `0x0858` append in both controls but not the
  replacement; `0x0AA4` appends in the replacement but neither control.
- The other 121 records remain irreducible alternatives because the builders
  apply per-frame runtime admission predicates and M2.27 retains only whole-
  entry append totals.

The full offset/form/count table is in
`static/exports/BIN-97c95ba5572dce63/M2-changed-record-form-localization.md`.
It contains no payload byte values.

## Independent checks

- Native disassembly independently distinguishes walk selection, the exact
  pre-call stops/call sites, and the builders' later admission gates.
- Both exact files independently reproduce the same 24 retained intervals,
  record forms, and 183 record starts; every record in the 13-entry set has at
  least one differing byte.
- All six complete retained cycles independently reproduce the same exact
  168-record call set.
- Every observed append count is within `0..exact call count`; the aggregate
  result has no arithmetic contradiction.

## Confirmed

- The smallest count-relevant boundary supported by current evidence is 18
  entry/form groups and 124 exact changed records.
- Exact file offsets `0x0174`, `0x0858`, and `0x0AA4` have individually
  discriminated append outcomes in the bounded three-arm evidence.
- The other 21 changed records inside the 13 entries are unnecessary to
  explain form-count totals outside both-control envelopes. This does not
  exclude content changes or visible effects.

## Inferred

At least 30 per-record append outcomes differ between replacement totals and
the nearest control-envelope edges. This is a conservative aggregate lower
bound, not a claim about which 30 records or source bytes are causal.

## Unknown and limitations

- Which individual calls append among the 121 records in the 15 multi-record
  groups.
- Which source bytes affect a builder admission predicate or the bounded
  M2.20 visible result.
- Meanings of record fields, forms, batch families, and the visible figure.
- General `.ALL` grammar, malformed behavior, and any safe edit surface.

## Contradictions and alternatives

No native count contradiction occurs. A terminology contradiction does:
M2.27 called `B4/B3` builder calls, while the exact pre-call set is broader
than the append set. They are now classified as completed append paths because
`0x00405FE0/0x00407450` apply runtime admission gates. Aggregate entry totals
admit multiple exact per-record solutions; control variation at entries 10,
14, 18, and 19 prevents reconstructing per-frame state from file bytes alone.
Those alternatives are preserved explicitly.

## Result and follow-up

M2.28 is complete. M2.29 should remain static-first: map exact append counter
writes and no-append returns, then design a fail-closed metadata-only
per-record discriminator for only the 124-record set. Any live arm requires
fresh explicit authority and the existing Direct3D, no-software, exact-load,
`NextLife`, cleanup, signal, and survival gates. Do not retain payload bytes,
use quarantined execution points, assign semantics, create general `.ALL`
tooling, inspect another family, or consult PS1.
