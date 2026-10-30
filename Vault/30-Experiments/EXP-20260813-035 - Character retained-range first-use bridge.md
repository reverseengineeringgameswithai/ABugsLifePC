---
type: experiment
id: EXP-20260813-035
date: 2026-08-13
question: Which first safe post-initialization PC consumer reads the exact ID-zero header or retained range, and does one normal update connect it to an M1-supported Training record or positive target?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora static analysis with retained Wine evidence
environment_version: GNU objdump 2.44; Ghidra baseline export; retained Wine 11.0 Staging evidence
working_directory: /home/dev/ABLPC
configuration: Exact ID-zero xref classification and one normal 0x0040FFC0 update branch
artifacts:
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
  - static/exports/BIN-97c95ba5572dce63/M2-character-retained-range-first-use-static-trace.md
addresses:
  - 0x00402DC0
  - 0x004032F0
  - 0x00445FF0
  - 0x0040FFC0
  - 0x0044C440
  - 0x0044D430
  - 0x005A9660
  - 0x005B18E0
result: first-id-zero-use-bounded-m1-direct-bridge-negative
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/rendering
---

# EXP-20260813-035 - Character retained-range first-use bridge

## Question

Which first safe PC consumer after scene-resource initialization reads exact
ID-zero slot `0x005B18E0` or retained entries
`[0x005A9660,0x005A9DE0)`, and does one normal update connect that use to an
M1-supported Training record or positive payload target?

## Inputs and procedure

- Used exact executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Queried every function in the existing structured Ghidra export with a
  direct data reference to table base `0x005B18E0`, then separated unindexed
  ID-zero loads from generic `base + runtime_index * 4` accesses.
- Ranked only post-`0x004679C7` candidates and traced their callers through
  the normal `0x0040FFC0` branch where `0x0059A5F0 == 0`.
- Independently checked the relevant calls, thunk targets, address formation,
  entry stride, and M1 record-list order with GNU `objdump` against the exact
  derived work-copy executable.
- Compared the accepted candidates with the M1 paths established by
  `EXP-20260812-009` through `EXP-20260812-012` and the positive resource
  outcome/range established by `EXP-20260812-033/034`.

No runtime was launched, no debugger or breakpoint was used, no file or
memory was modified, and no PS1 source was consulted.

## Candidate classification

The xref set contains initialization functions, generic indexed readers, and
two direct ID-zero readers. References in `0x00436AF0`, `0x00436B40`,
`0x00444EF0`, `0x004467E0`, `0x00446870`, `0x00448350`, `0x00456640`, and
`0x00459620` use a runtime resource index. Their reference to base
`0x005B18E0` does not prove the index is zero. `0x00444C40` and `0x00445020`
are in the initialization path and are outside the post-initialization rank.

`0x00402DC0` and `0x0044C440` directly load `0x005B18E0` without a resource
index. They are the accepted exact ID-zero candidates.

## Result

### First direct ID-zero use

In one normal `0x0040FFC0` update, native calls at `0x0040FFD9` and
`0x0040FFDE` order `0x004144C0` before M1 coordinator `0x0044D430`.
`0x004144C0` calls `0x00402DC0` at `0x00414653` through thunk `0x00401019`.

`0x00402DC0` directly reads ID-zero slot `0x005B18E0` at `0x004032F0`
(with additional direct loads at `0x0040330E/0x004033C5`), selects a pointer
within that header, and calls `0x00445FF0` through thunk `0x00401B86` with
starting destination index zero. `0x00445FF0` forms
`0x005A9660 + index * 0x50` at `0x0044608D-0x004460AC` and writes the dynamic
shared-entry values. This is the first proven unindexed post-initialization
ID-zero use in the declared branch.

### Nearest M1-side consumer and negative bridge

Inside `0x0044D430`, the nearest direct retained-range consumer is
`0x0044C440`, called at `0x0044D4BC` through thunk `0x0040185C` when bit
`0x10` of `0x005C5EDC` is clear. It reads ID-zero header start/end at
`0x0044C635`, derives `0x005A9660 + start * 0x50`, iterates exact stride
`0x50`, and passes an entry pointer downstream at `0x0044C898-0x0044C899`.

That call occurs before `0x0044D430` loads M1 record-list root `0x005BA7E0`
at `0x0044D4FA` and before the first 20-byte-record test at `0x0044D57F`.
The established selected-record route later enters `0x004498F0`; its `0x49`
path reads payload `+0x1C` at `0x00449E1A` and calls positive-target consumer
`0x0045A7F0` at `0x00449E20` through thunk `0x00401604`.

The structured export contains no direct ID-zero slot/range reference in
`0x0044D430`, `0x004498F0`, or `0x0045A7F0`, and no call from those M1 record
or payload functions to `0x00402DC0` or `0x00445FF0`. The no-argument
`0x0044C440` call is earlier than record enumeration. Therefore this one
normal update has no exact direct M1 record/payload-to-first-ID-zero data flow.

## Independent checks

- Ghidra's structured xrefs distinguish the two unindexed ID-zero readers
  from the generic indexed sites and expose the relevant thunk call graph.
- Native disassembly independently confirms the exact call order at
  `0x0040FFD9/0x0040FFDE`, ID-zero loads at
  `0x004032F0/0x0044C635`, shared-entry root/stride arithmetic, and the
  `0x0044D4BC -> 0x0044D4FA -> 0x0044D57F` ordering.
- `EXP-20260812-033` independently proves that replacing the exact loaded
  `.ALL` path changes a bounded rendered region, while
  `EXP-20260812-009/010` independently support the M1 selected-record and
  positive-target route. Those dynamic results anchor the two sides but do
  not create a missing address flow between them.

## Confirmed

- `0x00402DC0` is the first proven direct ID-zero reader in the declared
  normal update branch; `0x00445FF0` is its immediate shared-range updater.
- `0x0044C440` is the nearest direct ID-zero retained-range consumer within
  the M1 coordinator, but it executes before that invocation loads or walks
  the M1 20-byte-record list.
- No direct M1 record/payload-to-ID-zero bridge exists within this exact
  branch/order window.

## Inferred

The two paths likely contribute separately to one update's rendered output.
That ordering does not establish whether persistent or copied state connects
them across a wider lifetime.

## Unknown and limitations

- The alternate `0x0059A5F0 != 0` branch skips `0x004144C0`; its first direct
  ID-zero use is not classified here.
- A generic indexed reader could receive index zero in another event, but no
  reviewed M1 input proves that value.
- Persistent globals, copied state, later events, exact contributing entries,
  `.ALL` layout, and filename/resource identity remain unknown.
- The static negative does not claim that the ID-zero range has no rendered
  effect; `EXP-20260812-033` establishes the opposite at its file-replacement
  boundary.

## Contradictions and negative results

Several xrefs execute before `0x00402DC0`, but they use unknown runtime
indices. Treating the table-base symbol as an exact ID-zero access would
contradict the native indexed address formation. They remain generic
candidates rather than evidence against the first direct ID-zero result.

The closest M1-side reader is inside `0x0044D430`, but native order places it
before record-root load and record enumeration. Shared coordinator membership
is therefore sequencing evidence, not record-to-resource data flow.

## Result and follow-up

M2.22 is complete with an interval- and address-bounded negative for the
direct M1 bridge. The precise next discriminator is to trace the exact
shared-entry argument at `0x0044C898` through `0x0044F8E0`, beginning with its
entry `+0x20` read, and compare that address lineage with the exact positive
target argument at `0x00449E20`. If static evidence remains ambiguous, design
one separately approved read-only natural-pause capture for those exact
arguments within one normal update. Do not use `0x0044D794/0x0044D79A` or
widen to unrelated entries.
