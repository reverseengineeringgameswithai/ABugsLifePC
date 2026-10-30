---
type: experiment
id: EXP-20260813-039
date: 2026-08-13
question: Which renderer branch owns the inactive 0x80-stride arena, and which direct path from 0x0044F8E0 is active under the proven Direct3D selector?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; static PC-native review
environment_version: GNU objdump; checked Ghidra structured export
working_directory: /home/dev/ABLPC
configuration: Exact unchanged derived executable; no runtime instrumentation; no cross-port evidence
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-direct3d-renderer-path-reconciliation.md
addresses:
  - 0x004056A0
  - 0x004058D0
  - 0x00405FE0
  - 0x00407450
  - 0x004119E0
  - 0x0041F990
  - 0x00421310
  - 0x0043DA40
  - 0x0044F8E0
  - 0x0045A7F0
  - 0x0049C3F0
  - 0x0049C520
  - 0x0059F7F0
  - 0x008082C8
  - 0x0081BC28
  - 0x0081C138
result: positive-direct3d-batch-path-and-software-arena-reclassification
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/rendering
---

# EXP-20260813-039 - Direct3D renderer-path reconciliation

## Question

Which exact PC-native renderer initializer owns the conditional
`0x80`-stride arena, and which direct consumer path from `0x0044F8E0` is
reachable under the proven 640x480x16 Direct3D selector?

## Bounds and procedure

- Reverified exact executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Reviewed only the checked Ghidra structured export and native GNU objdump of
  the unchanged executable in `work/copies/`.
- Traced selector writer `0x0041F990`, main/restart renderer dispatches,
  thunks `0x004014E7/0x0040152D`, arena capacity/base writers, and only the
  direct alternate calls from `0x0044F8E0` reachable for selector 2.
- Followed the two alternate callees only far enough to identify their batch
  storage and exact Direct3D flush edge.
- Performed no runtime instrumentation or execution control, wrote no target
  state, opened no protected payload, parsed no `.ALL` field, assigned no
  primitive or asset identity, and consulted no PS1 source.

## Observed

### Renderer selector

Native `0x00420022-0x0042002E` maps nonzero `0x00573FF4` to selector `1` and
zero to selector `2`. The adjacent diagnostic branch independently maps
selector 1 to `native software render` and selector 2 to `Direct3d render`.

Both main dispatch `0x0043DB15-0x0043DB31` and restart dispatch
`0x00421358-0x00421374` call `0x0049C520` for selector 1 and `0x004119E0`
for selector 2. `0x004119E0` begins with exact diagnostic
`INIT : Starting Direct3D renderer.`

### Arena initializer

`0x0049C520` begins/ends with `INITSOFTRENDER` diagnostics and cites embedded
source path `E:\pc\BUGS\soft.cpp`. It writes capacity `0x2800` at
`0x0049C65E`, allocates `capacity << 7` bytes and stores base
`0x0081BC28` at `0x0049C689`, zeros counter `0x008082C8` at `0x0049C839`,
and clears the list-head array rooted through `0x004E8CC8`.

`0x0049C3F0` logs `InitSoftWindow(%i,%i)`, writes software-window dimension
and clip/scaling globals, and has no reference to the arena triple. Its call
at `0x0040FEBA` is itself gated by selector 1.

### Selected consumer edge

In `0x0044F8E0`, selector 2 routes masked record `0x3C` through call
`0x0044F99D -> 0x00401D66 -> 0x00405FE0` and masked record `0x34` through
`0x0045029F -> 0x00401CCB -> 0x00407450`. Selector 1 instead reaches the
already documented `0x80`-stride arena writers.

The two selector-2 callees append transformed vertices and indices to the
batch families rooted through `0x004C4108/0x004C410C`. Their capacity paths
call `0x004056A0/0x004058D0`; those functions load Direct3D device global
`0x005905F8` and call its vtable `+0x78` slot at `0x00405816/0x0040598B`.
Embedded failure diagnostics name the operation
`lpD3DDevice->DrawIndexedPrimitive`. `0x0045A7F0` independently uses the
same selector split and Direct3D batch/flush families.

## Confirmed

- Selector `1` is native software rendering; selector `2` is Direct3D.
- The conditional capacity/base/counter/list arena is initialized by the
  selector-1 software renderer path.
- `0x0049C3F0` is a selector-1 software-window helper, not an alternate
  renderer initializer and not an arena writer.
- Under selector 2, `0x0044F8E0` bypasses the software arena and reaches
  `0x00405FE0/0x00407450`, which build Direct3D batches capable of reaching
  the device `DrawIndexedPrimitive` slot through exact flush functions.
- The M2.25 coherent all-zero arena state is consistent with, rather than
  contradictory to, the accepted Direct3D runtime state.

## Inferred

The selected Direct3D batch path is the nearest PC-native route capable of
carrying the changed retained streams to M2.20's visible result. Static
reachability does not attribute that result to a particular retained entry,
record, input byte, batch family, or draw.

## Contradiction resolution and limitations

`EXP-20260813-036` correctly established shared conditional arena topology
between `0x0044F8E0` and `0x0045A7F0`, but its “hardware output” label was
unsupported because the selector mapping had not been traced. M2.25 preserved
the contradiction by demonstrating the arena was inactive in Direct3D.
This packet resolves it with exact native selector and initializer evidence:
the shared arena is the software branch, while Direct3D uses separate batch
storage. Historical reports retain a correction notice rather than silently
losing the prior interpretation.

This result does not establish which changed candidate contributes, batch
payload semantics, primitive identity, `.ALL` layout, pixel attribution,
M1 placement identity, or complete renderer architecture.

## Result and follow-up

M2.26 is complete. M2.27 should design the smallest metadata-only comparison
of the two proven Direct3D batch families across exact candidates
`{0-7, 9-23}`, including in-call flush/reset accounting. Runtime points and
execution control require fresh explicit approval. Do not reuse execution
breakpoint `0x0044C898`, retain protected batch bytes, begin general `.ALL`
tooling, assign semantic field/asset/primitive names, or consult PS1.
