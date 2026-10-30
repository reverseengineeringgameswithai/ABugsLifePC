# M2 plant-request origin static trace

## Scope and identities

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Level 01 `CD/LEVEL01/LEVEL.DAT` SHA-256:
  `786b7a964129d4fee6a1983b356e172d406b17663d87b8befe645b92dbf08b53`
- Static sources: the exact-hash work-copy executable, GNU objdump 2.44, the
  existing Ghidra evidence export, and the independent `LevelDat` parser.
- Runtime corroboration: retained Direct3D hardware logs
  `RUN-WINE-20260812-000634` and `RUN-WINE-20260812-114514`.

No runtime was launched or modified for this trace. No PS1 source was
consulted.

## Scene-initialization order

The scene initializer `0x004671D0` establishes both inputs later read by
`0x00416100`:

1. `0x0046720E` clears 64 dword slots rooted at `0x005C5860`.
2. `0x004675AA` calls `0x00465030` for the constructed `LEVEL.RAW` path.
3. `0x0046795D` loads the selected `LEVEL*.DAT` into the buffer whose pointer
   is stored at `0x005BA240`.
4. `0x00467971` calls fixup `0x0044BB70`.
5. `0x004679A0` calls `0x0041C420`, which rebuilds the 64 records rooted at
   `0x0059B628`.
6. `0x004679C2` calls the plant resource batch loader `0x00445020`, which in
   turn calls collector `0x00416100` at `0x00445601`.

## Input 1: separate `LEVEL.RAW` type-35 table

At `0x00465748`, `0x00465030` selects parsed packet type `0x23`. Instructions
`0x0046574D–0x0046576A` clear and copy exactly `0x700` bytes into
`0x00599EB0`. The retained Training and Level 01 hardware logs independently
contain `LOAD: Type 35, CreatListRam.`

`0x0041C420` then:

- clears `0x2100` bytes rooted at `0x0059B628` at
  `0x0041C424–0x0041C430`;
- walks 64 source records at a `0x1C`-byte stride and 64 destination records
  at a `0x84`-byte stride (`0x0041C58A–0x0041C597`);
- stores a pointer back into the copied source record at `0x0041C490`.

This establishes the collector's first input from `LEVEL.RAW`, not from the
M1 `LEVEL*.DAT` scene-record or positive-target ranges. Complete source-field
semantics and which Level 01 entry contributes the early ID 7 remain unknown.

## Input 2: `LEVEL*.DAT` top record type `0x3F`

The global `0x005C595C` is exactly slot 63 of the 64-pointer table rooted at
`0x005C5860`:

```text
0x005C5860 + 63 * 4 = 0x005C595C
```

While walking top records, `0x0044BB70` writes a nonnegative record type's
address to `0x005C5860 + type*4` at `0x0044BCA9`. Type `0x3F` uses the special
`4 + count*16` size branch at `0x0044BCB0–0x0044BCBC`. Therefore a type-63 top
record makes `0x005C595C` point directly into the loaded DAT buffer.

At `0x00416197`, the collector reads that pointer. It reads the count from the
record header, advances by `0x10`, examines one selector byte per `0x10` bytes,
and dispatches selectors `0x29` through `0x2D` at
`0x004161A8–0x0041622A`. Selector `+` (`0x2B`) consumes successive signed
words from `0x004DEA10`; selector `,` (`0x2C`) consumes successive signed
words from `0x004DEA20`. Each class has its own cursor, and a cursor advances
only when that selector class is encountered. Exact instructions
`0x004161EA–0x004161FA`, for example, load, emit, advance, and store only the
`0x2B` cursor. Consequently, removing an earlier same-class selector shifts
the values emitted by later selectors; the table result is not an intrinsic
property of a byte in isolation (`EXP-20260812-020`).

The exact executable constants begin:

```text
0x004DEA10: 4, 10, 9, 1
0x004DEA20: 6, 6, 6, 6
```

## Exact Training binding

The Training DAT has a type-`0x3F` top record at `[0x4, 0x3E8)` with count 62.
Its selected entries are:

| Entry | Entry start | Selector offset | Byte | Collector result |
|---:|---:|---:|---:|---:|
| 56 | `0x388` | `0x394` | `0x2B` (`+`) | 4 |
| 57 | `0x398` | `0x3A4` | `0x2B` (`+`) | 10 |
| 58 | `0x3A8` | `0x3B4` | `0x2C` (`,`) | 6 |

Entries 59–61 contain three more `0x2C` selectors, yielding duplicate ID 6.
Together with literal ID 5 at `0x00416110`, this statically predicts first
occurrences 5, 4, 10, 6. Retained hardware log
`RUN-WINE-20260812-000634` loads plant pairs in exactly that order at lines
1535–1542 and contains both required hardware markers at lines 145 and 196.

## Independent Level 01 correlation

The Level 01 DAT has a type-`0x3F` top record at `[0x4, 0x468)` with count 70.
The same mechanical decode yields:

```text
4, 10, 7, 7, 9, 3, 8, 2, 6
```

The retained hardware log loads first occurrences 5, 7, 4, 10, 9, 3, 8, 2,
6. This is consistent with the separate `LEVEL.RAW`-derived input contributing
ID 7 before the DAT top table and later duplicate IDs being ignored downstream.
The exact Level 01 first-input field remains an inference, not a confirmed
field binding.

## M1 boundary result

Training's M1 primary 20-byte records begin at file offset `0x4B0`. The bound
selector bytes `0x394`, `0x3A4`, and `0x3B4` all lie in the earlier type-`0x3F`
top record. They share the exact DAT file, loaded buffer, and fixup routine with
M1, but do not overlap an M1 primary/secondary 20-byte scene record, relocated
payload, or positive-target block.

The proven dependency boundary is therefore:

```text
LEVEL1.DAT top type-0x3F selector byte
  -> 0x0044BB70 pointer slot 63 / 0x005C595C
  -> 0x00416100 selector table
  -> plant ID
  -> 0x00445020 base-path selection
  -> 0x00444C40 .ANM/.ALL pair request
```

This is a same-DAT separate-table dependency, not the still-unproven M1
placement-record-to-resource dependency.

## Mutation precision from EXP-20260812-020

The original M2.7 plan treated `0x394` as independently bound to ID 4. Exact
instruction review before staging exposed a contradiction: changing that
first `0x2B` to an out-of-range selector leaves the `0x004DEA10` cursor at ID
4, so the second `0x2B` at `0x3A4` would emit 4 rather than 10. The accepted
one-byte test therefore changed `0x3A4`, not `0x394`. Its hardware log retained
plant 04 and omitted only the plant 10 `.ANM`/`.ALL` requests. This dynamically
confirms the per-class cursor model and keeps the `0x394` plant-04 necessity
question untested.
