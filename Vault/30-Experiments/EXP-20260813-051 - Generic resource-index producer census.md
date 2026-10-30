---
type: experiment
id: EXP-20260813-051
date: 2026-08-13
question: Does any of the eight retained generic resource-header indices derive from an M1 record or payload on the normal coordinator route and prove resource ID zero?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline PC-native static analysis
environment_version: GNU objdump 2.44; existing Ghidra baseline export
working_directory: /home/dev/ABLPC
configuration: Exact eight-reader census; normalized thunk reachability from the normal M1 update; no runtime, mutation, parser, semantics, other family, or cross-port evidence
artifacts:
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
  - static/exports/BIN-97c95ba5572dce63/M2-generic-resource-index-producer-census.md
addresses:
  - 0x00436AF0
  - 0x00436B40
  - 0x00444EF0
  - 0x004467E0
  - 0x00446870
  - 0x00448350
  - 0x00456640
  - 0x00459620
  - 0x0040FFC0
  - 0x004144C0
  - 0x0044D430
  - 0x004498F0
  - 0x0045A7F0
  - 0x005B18E0
result: all-eight-classified-current-m1-route-id-zero-negative
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/level-data
---

# EXP-20260813-051 - Generic resource-index producer census

## Question

Among the eight generic readers retained by `EXP-20260813-035`, does any
`0x005B18E0 + runtime_index * 4` access on the normal M1 coordinator and
selected-record route derive its index from an M1 record or payload and prove
resource ID zero?

## Inputs and procedure

- Verified the exact executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Rechecked structured references for only readers `0x00436AF0`,
  `0x00436B40`, `0x00444EF0`, `0x004467E0`, `0x00446870`, `0x00448350`,
  `0x00456640`, and `0x00459620`.
- Resolved all eight native thunks and every direct call/tail-jump site.
- Recorded each native scaled-index expression and its immediate producer.
- Normalized thunk edges in the structured call graph, then intersected each
  reader with the possible closures of normal update `0x0040FFC0`, its early
  update `0x004144C0`, M1 coordinator `0x0044D430`, record dispatcher
  `0x004498F0`, and positive-target consumer `0x0045A7F0`.
- Independently checked native call order and the positive first-dword gate
  used to build the active object-pointer list.

No game was launched or instrumented. No executable, asset, parser, schema,
runtime tool, source, or target was modified. No index/object/resource
semantics were assigned, no ninth reader or other family was inspected, and
no PS1 source was consulted.

## Result

The exact caller census contains 12 direct call/tail-jump sites through eight
thunks. Six readers are possible only in the `0x004144C0` update that returns
before the normal branch calls M1 coordinator `0x0044D430`:

- `0x00436AF0` reads the first dword of its object argument;
- `0x00436B40` reads persistent dwords `0x0059B730` and `0x0059B7B4`;
- `0x004467E0` and `0x00446870` read the first dword of object
  `0x0059D6A4`;
- `0x00456640` walks object pointers rooted at `0x0059D7E0`; and
- `0x00459620` reads the first dword of its second object argument.

`0x00444EF0` is outside the normal-update closure. Its sole caller is the
resource-batch initializer `0x00445020`, and native instruction
`0x0044528E` supplies exact index `0x0B`, not zero.

`0x00448350` is the sole candidate in the M1 coordinator closure. It walks
the same `0x0059D7E0` object-pointer list and uses each object's first dword
as its header index. The coordinator calls it at `0x0044D4E6`, before loading
M1 record root `0x005BA7E0` at `0x0044D4FA` and before the first 20-byte-record
test at `0x0044D57F`. Therefore the selected record or payload in that
invocation cannot produce its index.

The normal branch independently orders `0x004144C0` at `0x0040FFD9` before
`0x0044D430` at `0x0040FFDE`. The earlier update calls active-list producer
`0x0041EC40`; it reads each fixed-pool object's first dword at `0x0041EC6A`,
requires it to be positive at `0x0041EC6C-0x0041EC6E`, and appends the pointer
at `0x0041ECF1`. This bounds the immediate list-builder routes without
promoting a whole-lifetime invariant.

Neither the normalized `0x004498F0` selected-record closure nor the complete
`0x0045A7F0` positive-target closure contains any of the eight readers. The
full table, exact thunks/callers, native expressions, and limitations are in
`static/exports/BIN-97c95ba5572dce63/M2-generic-resource-index-producer-census.md`.

## Independent checks

- Structured xrefs enumerate the exact reader set, thunks, direct callers,
  data references, and normalized call closures.
- A native whole-image call/tail-jump scan independently reproduces all 12
  caller sites and each thunk target.
- Native disassembly independently confirms all scaled-index expressions,
  exact index 11 at `0x00444EF0`, normal-update order, active-list positive
  gate, coordinator-local call, record-root load, and first record test.
- `EXP-20260813-035` independently classifies direct versus generic header
  references, while `EXP-20260813-050` independently supplies the complete
  negative inside the exact positive-target consumer.

## Confirmed

- All eight retained generic readers are classified for the declared normal
  current-invocation M1 route.
- None receives an M1 record/payload-derived index and proves resource ID
  zero on that route.
- A possible generic index, shared update function, or table-base xref remains
  insufficient evidence for the M2 dependency gate.

## Inferred

The reviewed generic readers operate on pre-coordinator object/global state or
resource-initialization inputs rather than the selected M1 positive target in
the same invocation. This is the most economical interpretation of the exact
order and data flow, but it is not promoted into whole-program independence.

## Unknown and limitations

- Persistent or copied state across frames could connect wider-lifetime
  producer/consumer paths; none is proved here.
- The first dwords at `0x0059B730`, `0x0059B7B4`, `0x0059D6A4`, fixed-pool
  objects, and `0x0059C30C` retain offset/address descriptions rather than
  semantic names.
- The positive active-list insertion gate is not claimed as a lifetime
  invariant after insertion.
- Indirect function-pointer routes, other resource families, and other header
  readers were outside the declared packet.

## Contradictions and negative results

No prior evidence contradiction was found. The sole coordinator-local generic
reader initially appears close to the M1 record route, but native instruction
order separates it from the later record-root load and enumeration. Treating
that shared coordinator membership as a record-derived selection would
contradict the exact order.

## Result and follow-up

M2.36 is complete with a finite negative. `KU-023` remains the sole M2 exit
blocker, but the direct ID-zero readers, exact positive-target selector-2
inputs, and all eight generic header readers are now exhausted at their
declared PC-native boundaries.

The smallest next packet is an offline dependency-gate disposition: reconcile
the now-exhausted ID-zero selection surfaces with the written M2 gate and
choose explicitly between a justified milestone-gate revision/closure and one
new finite PC-native dependency candidate. Do not widen silently to more
xrefs, launch a runtime, inspect another family, or consult PS1 before that
scope decision.
