---
type: experiment
id: EXP-20260813-050
date: 2026-08-13
question: Does any value choosing or parameterizing the exact M1 positive-target selector-2 Direct3D output derive from ID-zero FLICK.ALL state?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline PC-native static analysis
environment_version: GNU objdump 2.44; existing Ghidra baseline export
working_directory: /home/dev/ABLPC
configuration: Exact 0x0045A7F0 selector-2 input and inline-batch provenance; no runtime, mutation, parser, semantics, other family, or cross-port evidence
artifacts:
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
  - static/exports/BIN-97c95ba5572dce63/M2-positive-target-selector2-input-provenance.md
addresses:
  - 0x00449E1A
  - 0x00449E20
  - 0x0045A7F0
  - 0x0045A946
  - 0x0045C7FB
  - 0x004056A0
  - 0x004058D0
  - 0x004C4108
  - 0x004C410C
  - 0x005A9660
  - 0x005B18E0
file_offsets:
  - 0x111E4
  - 0x1319C
result: selector-2-input-provenance-complete-id-zero-bridge-negative
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/rendering
---

# EXP-20260813-050 - M1 positive-target selector-2 input provenance

## Question

Within exact M1 positive-target consumer `0x0045A7F0`, does any value used to
choose or parameterize selector-2 Direct3D output derive from ID-zero header
`0x005B18E0`, retained range `[0x005A9660,0x005A9DE0)`, or the exact selected
`CHARS/FLICK.ALL` state?

## Inputs and procedure

- Used exact executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Rechecked `FUN_0045a7f0`'s structured data references and complete callee
  set in the existing Ghidra export.
- Independently traced the two native selector checks, exact M1 call
  arguments, target-relative offset reads, renderer-state decisions, ten
  inline Direct3D allocation arms, capacity/flush calls, index updates, and
  vertex-record writes with GNU `objdump`.
- Compared every input class with the exact ID-zero header/range from
  `EXP-20260812-034` and the distinct retained-entry/positive-target lineages
  from `EXP-20260813-035/036`.

No game was launched or instrumented. No executable, work-copy asset, source,
target, parser, schema, or runtime tool was modified. No source-field,
primitive, asset, identity, or pixel semantics were assigned. No other record
or resource family and no PS1 source were inspected.

## Result

The selector checks at `0x0045A946-0x0045A955` and
`0x0045C7FB-0x0045C80A` enter the reviewed Direct3D branches only when
`0x0059F7F0 == 2`. Those branches allocate and fill Direct3D batches inline;
they do not call builders `0x00405FE0` or `0x00407450`.

Ten allocation arms use roots `0x004C4108` or `0x004C410C`. Six can flush
through thunk `0x00401618 -> 0x004058D0`; four can flush through thunk
`0x0040127B -> 0x004056A0`. The non-fixed page/list argument comes from bits
of the `T`-derived command header. Two special arms use fixed list argument
`0x0E`. Capacity counters, list cursors, vertex pointers, and index updates
come from the chosen Direct3D root.

The values written into the batches derive from:

- positive target `T`, table base `V = T + 4`, its command stream, 16-bit
  table offsets, and packed table-relative values;
- the exact M1 caller's third-input bias and fixed fourth-input address
  `0x005BDB9C`;
- renderer matrices, projection/clip thresholds, page dimensions, color/scale
  modifiers, and renderer switches; and
- scratch/cached values computed from those inputs inside this function.

The second formal input is not read. On the exact M1 route, the third input is
the caller's literal-zero third argument plus `8 * payload[+0x18]`.
`0x005B1ED0`, although numerically near the ID-zero header, is a distinct
cache populated by local command/target/helper flow. It is not
`0x005B18E0` and does not alias the retained range.

The structured export reports zero direct `FUN_0045a7f0` references to exact
header `0x005B18E0` and zero into `[0x005A9660,0x005A9DE0)`. Native tracing
also finds no indirect provenance through the exact caller arguments, page/
list choice, scratch, root choice, flush argument, index append, vertex base,
or emitted record. The complete review is retained in
`static/exports/BIN-97c95ba5572dce63/M2-positive-target-selector2-input-provenance.md`.

## Independent checks

- Structured xrefs provide the zero header/range reference census, both D3D
  roots, and the complete five-callee set.
- Native disassembly independently resolves both flush thunks and verifies
  ten allocation arms, command-derived page/list inputs, fixed `0x0E` arms,
  and three- versus four-record increments.
- `EXP-20260813-036` independently establishes that `T` and the retained-entry
  stream have distinct address lineages; `EXP-20260813-039` independently
  establishes that these roots and flushes are the selector-2 Direct3D path.

## Confirmed

- Every resource-facing selector-2 input in `0x0045A7F0` is classified.
- No reviewed value derives from the exact ID-zero header, retained entry
  range, or selected `CHARS/FLICK.ALL` state.
- Shared Direct3D roots and eventual draw calls are renderer convergence, not
  a record-to-resource selection edge.

## Inferred

The M1 positive target and ID-zero retained-resource path remain parallel
inputs to Direct3D rendering at the reviewed boundary. The negative makes
that interpretation stronger, but does not prove lifetime independence.

## Unknown and limitations

- A copied or indirect resource-selection edge elsewhere in the program or
  across a wider lifetime remains possible.
- The eight generic runtime-indexed `0x005B18E0` readers retained by
  `EXP-20260813-035` have not been tested for M1-derived index provenance.
- Command fields, batch contents, scratch values, and resource identities
  retain address/offset names; their semantics remain unknown.

## Contradictions and negative results

The complete selector-2 review does not expose a contradiction in prior
evidence. It rejects the remaining candidate that Direct3D builder arguments
inside `0x0045A7F0` silently carry the ID-zero selection. Batch-root sharing,
draw-call convergence, and overlapping rendered pixels remain insufficient
for the M2 dependency gate.

## Result and follow-up

M2.35 is complete with a precise negative. `KU-023` and M2 remain open.

The smallest next PC-native discriminator is an offline census of only the
eight generic runtime-indexed header readers already enumerated by
`EXP-20260813-035`: determine whether any resource index on the normal M1
coordinator/selected-record route derives from an M1 record or payload and can
select ID zero. Do not launch a runtime, widen to a new resource family, or
assign resource-index semantics before that finite static provenance pass.
