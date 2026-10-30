---
type: experiment
id: EXP-20260812-034
date: 2026-08-12
question: Which exact PC origin requests accepted Training CHARS/FLICK.ALL, and what first consumer and bounded destination follow its whole-file load?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora static analysis and retained Wine evidence
environment_version: GNU objdump 2.44; Ghidra baseline export; Wine 11.0 Staging retained log
working_directory: /home/dev/ABLPC
configuration: Exact character request and first-consumer trace with address-directed selected-file checks
artifacts:
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
  - static/exports/BIN-97c95ba5572dce63/M2-character-resource-static-trace.md
  - dynamic/wine/RUN-WINE-20260812-231216/bugs.log
addresses:
  - 0x00445020
  - 0x00444C40
  - 0x00448010
  - 0x004AE240
  - 0x005A9660
  - 0x005B18E0
file_offsets:
  - 0x0000
  - 0x2C00
  - 0x2C04
  - 0x34EC
result: exact-character-request-and-retained-24-entry-destination-bounded
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/file-access
---

# EXP-20260812-034 - Character request and first consumer trace

## Question

Which exact PC caller/origin requests accepted Training
`CD/CHARS/FLICK.ALL`, and what first bounded consumer and runtime destination
follow its whole-file load?

## Inputs and procedure

- Used exact executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Queried data references and decompilation from the existing Ghidra evidence
  export for `0x004671D0`, `0x00445020`, `0x00444C40`, and `0x00448010`.
- Independently checked every relevant branch, push, thunk, call, stride,
  cursor update, and destination address using GNU `objdump` against the exact
  derived work-copy executable.
- Read only address-selected values that the traced code consumes from both
  exact `0x34EC`-byte M2.20 inputs: unchanged `CHARS/FLICK.ALL`, SHA-256
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`,
  and replacement source `CHARS3/FLICKD.ALL`, SHA-256
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
- Correlated the predicted request with accepted Direct3D replacement run
  `RUN-WINE-20260812-231216`, whose lines 1459-1460 request
  `chars\flick.anm` then `chars\flick.all` and which reaches `NextLife`.

No runtime was launched, no debugger or breakpoint was used, no file or
memory was modified, and no PS1 source was consulted.

## Result

`0x004671D0` clears the local object index to zero at `0x0046782C` and calls
`0x00445020` through thunk `0x00401CA8` at `0x004679C2`. After clearing the
shared resource tables, `0x00445020` reads `0x00861C84`. Its default arm pushes
built-in base string `chars\flick` at `0x004450EC`, always passes numeric
resource ID zero, and calls pair coordinator `0x00444C40` through thunk
`0x004018A7` at `0x00445143`.

The coordinator first handles the matching `.anm`, then calls `0x00448010` at
`0x00444D69`. That helper appends `.all` and invokes whole-file loader
`0x004AE240` through thunk `0x00401082` at `0x00448079`. The loader is the
producer of the exact runtime log line. Thus the accepted character request
is not a generic inference from the loader's ten call sites: it is the exact
`0x00445020` ID-zero default branch through the paired coordinator and
`.all` helper.

`0x00448010` is the first format-specific consumer. In both exact M2.20
files, its doubled first dword selects a 30-count table at `0x2C00`; the 30
`0x4C`-byte source descriptors beginning at `0x2C04` end exactly at file end
`0x34EC`. The comparison path at `0x004480C3-0x004480CC` materializes 25
shared entries at root `0x005A9660` and stride `0x50`. The final materialized
entry is converted to value 12 at destination `+0x2E` by
`0x00448111-0x0044812D`.

The immediate coordinator boundary then detects that value at
`0x00444D97-0x00444DA7`, decrements the current index from 25 to 24, and
stores the retained end index in the ID-zero ANM header reached through slot
`0x005B18E0`. Its start index is zero. The exact retained range is therefore
24 entries at `[0x005A9660, 0x005A9DE0)`. One additional entry at
`[0x005A9DE0, 0x005A9E30)` is written and immediately consumed, but is not in
the retained header range.

## Independent checks

- Native disassembly verifies the Ghidra-derived chain, including thunk
  targets, exact selector arms, ID zero, initial index zero, calls, and range
  arithmetic.
- Native `.data` bytes verify the four base strings and `.anm`/`.all`
  extension strings at their exact VAs.
- Both exact selected-file byte streams independently satisfy the per-file bounds:
  `0x2C04 + 30 * 0x4C == 0x34EC`. Twenty-four compared dwords are `1`, five
  are `287`, and the last is `9`, predicting the observed static count of 25
  materialized entries and the final coordinator adjustment to 24. In both
  files the 30 consumed length dwords also sum to `0x15FE`, placing the final
  arena cursor at table offset `0x2C00`.
- Retained accepted log order independently agrees with the exact static path:
  Flick `.anm` then `.all`, before the later selected resources.

## Confirmed

- The exact accepted request originates in `0x00445020`'s default
  `chars\flick`, ID-zero arm, reached from `0x004671D0`.
- The `.all` load call is `0x00448079` to thunk `0x00401082`, whose target is
  whole-file loader/log producer `0x004AE240`.
- `0x00448010` is the first format-specific consumer.
- For this exact file and initialization, slot `0x005B18E0` records retained
  shared-entry indices `[0,24)`, corresponding to
  `[0x005A9660, 0x005A9DE0)`.

## Inferred

The selected bytes contribute through the ID-zero resource range to the
M2.20 visible result. The evidence does not establish which subrange or field
causes that render difference.

## Unknown and limitations

- The meanings of all `.ALL` values and runtime entry fields remain unknown.
- The original consumer has no explicit file-size or destination-capacity
  bound; the arithmetic above bounds only the two exact M2.20 files.
- The semantic meaning of selector `0x00861C84`, resource ID zero, and the
  path names remains unassigned.
- No M1 20-byte scene record or positive payload target is yet connected to
  the ID-zero header or retained entry range.

## Contradictions and negative results

- The first consumer writes 25 entries, but the retained per-resource header
  ends at 24 after the coordinator consumes the final entry. Reporting either
  number without its exact boundary would be incomplete.
- A runtime debugger was unnecessary: two independent static forms, exact
  file arithmetic, and the retained accepted load line discriminated the
  request and destination without entering the unsafe caller-gate region.

## Result and follow-up

M2.21 is complete. The next bounded packet should start from exact ID-zero
slot `0x005B18E0` and retained range `[0x005A9660, 0x005A9DE0)`, then ask
which first post-initialization PC consumer can connect that range to one
M1-supported Training record/payload or explicitly rule out the candidate
within one declared event window. It must retain address-based names, avoid
unsafe `0x0044D794/0x0044D79A`, and not begin general `.ALL` parsing.
