---
type: experiment
id: EXP-20261018-011
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static, whole image. Raw scans of call/jmp rel32 targets and absolute references, a skip-data capstone sweep of all of .text, and the Ghidra export for function bounds; no game launch
question: Can the list table 0x005C5860 hold a pointer from an earlier level when the current level's DAT lacks that record type (KU-064)?
result: No, by every static route. The table is written only by the DAT record walk 0x0044BB70. Its one call site, 0x00467971, sits in the level-load function 0x004671D0 after that function's unconditional 64-dword clear. The second clear sequence is in an uncalled function. Every other absolute reference to the table is a read. A level without a type-N record therefore sees slot N = 0
status: complete-bounded
created: 2026-10-18
updated: 2026-10-18
evidence: [EXP-20260816-153, EXP-20260816-154, EXP-20260816-155, EXP-20261018-001]
tags: [experiment/static, re/level-data]
---

# EXP-20261018-011 - Type-indexed list table writers and readers

## Question

The DAT loader stores each top record's address in
`0x005C5860 + |type|*4`. KU-064 asks what a reader of slot 1 (`0x005C5864`)
finds in a level whose DAT has no type-1 record: zero, or a pointer left by
the previous level.

EXP-20260816-154/155 showed that `0x004671D0` clears the table
unconditionally before it calls the walk, so "the only route to a stale
pointer is a transition that skips `0x004671D0`". This experiment closes
that route statically. KU-064 is part of section 7 of [[Next Tasks]].

## Writers

- **The walk.** `0x0044BB70` stores at `0x0044BC8B`–`0x0044BC95` (negative
  types) and `0x0044BCA9` (positive). Its only entry is thunk `0x00401D7A`,
  whose only call is `0x00467971`, inside `0x004671D0`. Raw rel32 scan and
  thunk table agree.
- **The live clear.** `0x00467207`–`0x00467215` (64 dwords) in the same
  function, before that call on every entry (EXP-155).
- **The duplicate clear.** `0x00464F31` starts the function `0x00464F30`.
  Its thunk `0x00401A82` has no callers and nothing holds its address.
- **Nothing else.** The absolute references to `0x005C5860` and
  `0x005C5864` (raw scan of the image) are those writes plus reads.

## Readers

| Site | Function | Reads |
|---|---|---|
| `0x0041DDD7`, `0x0041DEE4` | creature VM, opcodes 4 and 10 | slot by `+0x0E`/`+0x0F` ([[EXP-20261018-001 - Creature row index census]]) |
| `0x0043A75D` | Bug Bar's routine `0x00439E90` | a slot indexed by a loop counter |
| `0x004318B8` | Anthill `0x004317D0` | slot 1 (Dot's path) |
| `0x004323A8` | Council Chamber `0x00431CB0` | slot 1 |
| `0x00432940`, `0x004329B4` | reset selector `0x00432930` | slot 1 |
| `0x00437A30`, `0x00437AA4` | twin selector `0x00437A20` | slot 1 |
| `0x004369B3`, `0x00436D25` | Anthill Pt 2 `0x004369B0` and `0x00436B40` (EXP-20261005-002) | slot 1 |
| `0x0043CE7B` | `0x0043CE60` | slot 1 |

## Callers of the level load

`0x004671D0` is reached only through thunk `0x004019EC`, from six sites:

- `0x00410352` in CallOptions `0x00410310`;
- `0x004133E7` and `0x0041349B` in `0x004133B0`;
- `0x004162F8` in `0x004162C0`;
- `0x0042D3F2` in `0x0042D2D0`;
- `0x0042E6ED` in `0x0042E5C0`.

Each call clears the table and walks the new DAT in the same invocation. No
other code walks a DAT into the table.

## Confirmed, inferred, unknown

- **Confirmed (static, whole image).**
  - The table's only writes are the walk (only inside `0x004671D0`) and that
    function's clear.
  - In any level, slot N holds the current DAT's last type-±N record, or 0.
  - So in the seven retail DATs without a type-1 record, `0x005C5864` is 0.
- **Inferred.** A slot-1 reader running in such a level would dereference
  0. Each reader above is a level routine or a selector gated to its own
  levels, which is why that does not happen in retail. Not traced per
  reader.
- **Unknown.**
  - **Runtime.** No live read of the slot after loading a level without
    type 1, which would be the second form (KU-064's proposed sample).
  - Which lists Bug Bar's routine walks.

## Consequences

- KU-064 is answered statically: zero, not stale.
- KU-063 gains a consumer: Bug Bar's level routine `0x00439E90` reads the
  table by index, the likely user of its lists 0–5, which no creature walks.
