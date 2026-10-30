---
type: experiment
id: EXP-20260813-036
date: 2026-08-13
question: Does the exact retained-entry pointer passed at 0x0044C898 reach a renderer data structure whose address lineage intersects the established M1 positive-target path at 0x00449E20 within one normal update?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora static analysis with retained Wine evidence
environment_version: GNU objdump 2.44; Ghidra baseline export; retained Wine 11.0 Staging evidence
working_directory: /home/dev/ABLPC
configuration: Exact ID-zero retained-entry and dispatch-0x49 positive-target hardware-output lineage comparison
artifacts:
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
  - static/exports/BIN-97c95ba5572dce63/M2-shared-entry-render-lineage-static-trace.md
addresses:
  - 0x0044C898
  - 0x0044F8E0
  - 0x00449E20
  - 0x0045A7F0
  - 0x005A9660
  - 0x005BD740
  - 0x008082C8
  - 0x0081BC28
  - 0x004E8CC8
result: shared-hardware-submission-lineage-distinct-source-streams
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/rendering
---

# EXP-20260813-036 - Shared-entry render-lineage discriminator

> [!IMPORTANT] M2.26 correction
> `EXP-20260813-039` proves that selector 1 is native software and owns the
> shared `0x80`-stride arena documented here. Selector 2 is Direct3D and uses
> separate batch storage. The source-lineage and arena-topology observations
> below remain exact, but the historical “hardware output” label is superseded.

## Question

Does the exact retained-entry pointer passed at `0x0044C898` reach a renderer
data structure whose address lineage intersects the established M1 positive-
target argument passed at `0x00449E20`, within one normal `0x0040FFC0` update?

## Inputs and procedure

- Used exact executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Reused only the exact ID-zero range and descriptor values already bounded by
  `EXP-20260812-034/035`; no unrelated entry or resource family was scanned.
- Traced one symbolic current retained entry from `0x0044C898` into
  `0x0044F8E0`, beginning at the native `+0x20` read at `0x0044F8EA`.
- Traced the exact M1 positive target from payload `+0x1C` at `0x00449E1A`
  through the call at `0x00449E20` into `0x0045A7F0`.
- Intersected both functions' structured Ghidra data-reference sets, then
  independently checked source address formation, hardware output allocation,
  output stride, link offsets, and list-head updates with GNU `objdump`.
- Compared the result with the accepted Direct3D file-to-render outcome in
  `EXP-20260812-033` and the M1 target-to-visible-placement evidence in
  `EXP-20260812-009/010`.

No runtime was launched, no debugger or breakpoint was used, no file or
memory was modified, and no PS1 source was consulted.

## Expected

The static lineage should either expose one exact source or output address
edge shared by the retained entry and M1 positive target, or rule out that
intersection at the reviewed boundary and leave one precise discriminator.

## Observed

### Retained-entry source

For the exact unchanged selected file, retained entries 0-23 carry word
`+0x2E == 1` from the already recorded descriptor values and the exact store
at `0x00448117`. In the declared outer branch, `0x0044C661-0x0044C666`
therefore selects the path that passes current entry `E` at `0x0044C898`.

`0x0044F8EA` loads `S = *(E + 0x20)`. From that point, the function forms only
stream-relative addresses, selects masked byte values `0x34`/`0x3C`, advances
by exact `0x24`/`0x30` strides, and handles the four-byte continuation marker
at `0x004509E6-0x004509EF`.

### M1 positive-target source

`0x00449E1A` loads target `T`; `0x0045A81E` forms `V = T + 4`; and the
bounded nonnegative-count path forms command pointer `V + n * 12` at
`0x0045A897-0x0045A89E`. Command items then supply 16-bit offsets for reads
relative to `V`.

The retained exact reports for targets `0x111E4` and `0x1319C` contain only
even command modes (`0x60`, `0x8062`, `0x8064`, and, for `0x111E4`,
`0x8066`). The exact parity branch at `0x0045A8D1-0x0045A8D7` enters the
hardware-output path containing the representative allocator sequences below.
No semantic mode name is assigned.

There is no direct call, copy, global slot, or address-forming edge carrying
`S` into the M1 target walk or `T` into the retained-entry walk. Static
evidence does not claim universal numeric inequality for all possible pointer
values.

### Shared hardware output

Both functions use the exact transform scratch range
`0x005BD740-0x005BD75C`. More decisively, both test counter `0x008082C8`
against capacity `0x0081C138`, allocate from
`*(0x0081BC28) + counter * 0x80`, increment the same counter, store the prior
list pointer at output `+0x70`, store a mode/flag word at output `+0x74`, and
link through the head-array topology rooted through pointer global
`0x004E8CC8`.

Representative allocator instructions are `0x0045005B-0x0045006F` and
`0x00450838-0x0045084C` in `0x0044F8E0`, and
`0x0045F974-0x0045F987` and `0x0045FFB8-0x0045FFCC` in `0x0045A7F0`.
Representative link sequences are `0x0045020E-0x00450223` and
`0x00450997-0x004509A9` versus `0x0045FFAC-0x0045FFB1` and
`0x00460219-0x0046022E`.

## Independent checks

- The structured Ghidra export reports the same non-stack globals in both
  functions, including the transform scratch, hardware count/capacity/base,
  list-head root, and per-depth flag table.
- Native disassembly independently proves both input formulas and the exact
  shared `base + counter * 0x80` allocator formula.
- `EXP-20260812-033` independently confirms a rendered outcome for the exact
  ID-zero-loaded file, while `EXP-20260812-010` confirms placement-local
  visible changes when only an M1 positive target is rebound.

## Confirmed

- The retained-entry `+0x20` stream and M1 positive-target stream are distinct
  static input lineages with no direct copy or call edge between them.
- Both lineages converge on the same hardware renderer submission arena and
  list topology in the declared normal-update path.
- The convergence is a shared output structure, not evidence that an M1
  record selects the ID-zero file/range or that the two source pointers alias.

## Inferred

`0x0044F8E0` and `0x0045A7F0` are parallel render-data front ends for the
hardware path. Exact primitive and field meanings remain unassigned.

## Unknown and limitations

- Which retained entry/entries and stream bytes cause the repeated M2.20
  replacement-local visible difference.
- Whether a particular retained-entry emission and M1 emission use the same
  list head; the M1 head includes its caller-supplied third-argument offset.
- Whether persistent state or a different event creates a placement-to-
  resource identity upstream of the shared output arena.
- Software-renderer convergence is not claimed; the project baseline and this
  comparison are bounded to the established hardware path.

## Contradictions and negative results

Shared transform scratch and output globals do not make source pointers `S`
and `T` identical. Conversely, the absence of a direct source edge does not
make the render paths independent: their exact hardware allocator and
list-root addresses are shared. The result preserves both facts rather than
promoting either into a stronger identity or separation claim.

## Result and follow-up

M2.23 is complete with a positive hardware-output convergence and a negative
direct-source-edge result. M2 remains active because this does not identify
which retained stream accounts for the accepted file replacement's visible
effect or bind an M1 placement to that resource.

The precise next discriminator is an offline, exact-two-file localization of
the accepted `FLICK.ALL`/`FLICKD.ALL` byte differences across only the 24
retained `+0x20` stream intervals. Retain only bytes reached by the
demonstrated `0x0044F8E0` walk; do not create a general parser or assign
field, asset, primitive, or filename semantics.
