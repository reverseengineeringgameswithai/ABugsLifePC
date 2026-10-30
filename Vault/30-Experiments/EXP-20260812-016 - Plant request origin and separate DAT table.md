---
type: experiment
id: EXP-20260812-016
date: 2026-08-12
question: Which exact PC data fields produce Training plant IDs 4, 10, and 6, and do they overlap an M1 scene-record or positive-target chain?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora static analysis and retained Wine hardware logs
environment_version: GNU objdump 2.44; Ghidra baseline export; Python 3.14.6
working_directory: /home/dev/ABLPC
configuration: Exact Training and Level 01 DAT bytes correlated with accepted Direct3D request logs
artifacts:
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
  - static/exports/BIN-97c95ba5572dce63/M2-plant-request-origin-static-trace.md
  - dynamic/wine/RUN-WINE-20260812-000634/bugs.log
  - dynamic/wine/RUN-WINE-20260812-114514/bugs.log
addresses:
  - 0x00416100
  - 0x0041C420
  - 0x0044BB70
  - 0x00465030
  - 0x004671D0
  - 0x00599EB0
  - 0x0059B628
  - 0x005C5860
  - 0x005C595C
file_offsets:
  - 0x394
  - 0x3A4
  - 0x3B4
result: training-plant-ids-from-separate-level-dat-top-table
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/static
  - re/resources
  - re/file-format
---

# EXP-20260812-016 - Plant request origin and separate DAT table

## Question

Which exact PC data fields produce Training plant IDs 4, 10, and 6, and do
they overlap an M1 scene-record or positive-target chain?

## Inputs and procedure

- Exact executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Exact Level 01 `CD/LEVEL01/LEVEL.DAT` SHA-256:
  `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`.
- Followed both inputs read by `0x00416100` backward through scene initializer
  `0x004671D0` with the Ghidra export and exact GNU objdump instructions.
- Parsed the two DAT prefixes independently, located type-`0x3F` top records,
  and read only their selector bytes from user-owned work copies.
- Applied the exact executable selector tables and compared predicted first
  occurrences with retained hardware load logs.
- Compared the bound Training offsets with exact M1 primary-record, payload,
  and positive-target ranges.

No runtime was launched or modified. No PS1 source was consulted.

## Expected discriminator

- If a selected ID originates in an M1 scene record or positive target, its
  producer byte and relocation path should lie in that exact range.
- If it originates separately, the trace should identify another loaded table
  and show a non-overlapping source range.

## Observed producer paths

The two collector inputs have distinct file origins:

- `0x00465030` copies a parsed `LEVEL.RAW` type-35 block into `0x00599EB0` at
  `0x0046574D–0x0046576A`. `0x0041C420` transforms its 64 source records into
  the 64 `0x84`-byte records rooted at `0x0059B628`.
- `0x0044BB70` indexes `LEVEL*.DAT` top records by signed type into the
  64-pointer table at `0x005C5860`. A type-`0x3F` record populates slot 63,
  whose address is exactly `0x005C595C`.

Thus the second `0x00416100` input is not a freestanding global: it points
directly into the loaded DAT buffer at a type-`0x3F` top record.

## Exact Training field binding

Training's type-`0x3F` record is `[0x4, 0x3E8)`, count 62. The collector reads
one byte at record-relative `0x10 + index*0x10`.

| Entry | Exact file byte | Selector | Static table result |
|---:|---:|---:|---:|
| 56 | `0x394` | `0x2B` (`+`) | ID 4 |
| 57 | `0x3A4` | `0x2B` (`+`) | ID 10 |
| 58 | `0x3B4` | `0x2C` (`,`) | ID 6 |

The next three selectors also produce ID 6. The static first-occurrence order,
after literal ID 5, is therefore 4, 10, 6. Accepted Direct3D hardware run
`RUN-WINE-20260812-000634` requests plant pairs 05, 04, 10, 06 in exactly that
order. Its log contains `Screen mode 640x480x16 selected` and
`Starting Direct3D renderer` and does not enter `INITSOFTRENDER`.

## Independent Level 01 check

Level 01's type-`0x3F` record decodes mechanically to IDs
`4, 10, 7, 7, 9, 3, 8, 2, 6`. Its retained hardware log requests first
occurrences `5, 7, 4, 10, 9, 3, 8, 2, 6`. This independently agrees with the
DAT-derived subsequence while indicating that the earlier `LEVEL.RAW` input
contributes at least the first unique ID 7. The exact Level 01 type-35 source
field is not identified here.

## M1 overlap test

Training primary 20-byte scene records begin at `0x4B0`; the bound selector
bytes end at `0x3B4` within the top-record region. They therefore share the
same file buffer and `0x0044BB70` fixup with M1 but do not overlap:

- an M1 primary or secondary 20-byte scene record;
- a relocated scene payload; or
- a positive-count dispatch-`0x49` target block.

## Confirmed

- Training IDs 4, 10, and 6 have exact PC file-byte producers at `0x394`,
  `0x3A4`, and `0x3B4` in the exact Training DAT.
- `0x0044BB70` makes `0x005C595C` point at that type-`0x3F` top record, and
  `0x00416100` maps its selectors to those IDs.
- The selected fields enter through a separate DAT top table, outside the M1
  20-byte record and positive-target ranges.
- Retained hardware request order independently matches the static Training
  mapping and the Level 01 DAT-derived subsequence.

## Inferred

- Level 01's separate `LEVEL.RAW`-derived input contributes ID 7 before the
  type-`0x3F` table; this is order correlation, not an exact field binding.
- The type-`0x3F` selector field participates in resource-family selection.
  Complete record and selector semantics remain unnamed.

## Contradictions and limitations

- This is a direct level-file-to-resource dependency, but not the stronger M1
  placement-record/payload-to-resource dependency required by the M2 exit
  outcome. The distinction is retained rather than normalized away.
- The runtime logs corroborate request order but do not constitute a byte
  mutation test. Static instruction flow and exact file bytes establish the
  field mapping without requiring a new debugger or renderer run.
- Duplicate IDs occur in the top table; complete downstream duplicate/cache
  behavior is not analyzed in this packet.

## Result and follow-up

M2.3 is complete with a same-DAT, separate-table result. M2.4 may begin the
bounds-checked `.ANM` inspector because its loader-size and first relocation
boundaries were established in `EXP-20260812-015`. The missing direct M1
scene-record/payload-to-resource identity remains an explicit later M2 gate.
