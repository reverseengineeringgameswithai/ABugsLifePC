# M2 character resource static trace

## Provenance

- Executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Selected M2.20 files, both 13,548 (`0x34EC`) bytes:
  `PC/BUGS/CD/CHARS/FLICK.ALL`, SHA-256
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`,
  and replacement source `PC/BUGS/CD/CHARS3/FLICKD.ALL`, SHA-256
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
- Review sources: the existing structured Ghidra export, GNU
  `objdump -d -Mintel`/`objdump -s` against the exact derived work-copy
  executable, and address-directed reads of both exact selected files.
- Runtime correlation: accepted Direct3D run `RUN-WINE-20260812-231216`,
  especially log lines 1456-1465.
- Experiment: `EXP-20260812-034`.

This report records exact PC control/data flow and only those file values read
by the traced instructions. It does not assign structure-field, character,
model, animation, or rendering semantics.

## Exact request origin

1. `0x004671D0` clears its local object index at `0x0046782C`. Immediately
   before the resource-batch call, it stores that zero to `0x0063E990` at
   `0x004679AD`, stores the current scene-arena cursor to `0x005C5D58` at
   `0x004679BC`, and calls thunk `0x00401CA8` at `0x004679C2`. The thunk jumps
   to `0x00445020`.
2. `0x00445020` clears the shared array rooted at `0x005A9660` and the 128
   per-ID slots rooted at `0x005B18E0`. It reads selector global `0x00861C84`
   at `0x004450AE` and selects one of four built-in base strings.
3. The default arm at `0x004450DB-0x004450F1` pushes base-string VA
   `0x004DE018` (`chars\flick`), resource ID zero, the two caller pointers,
   and two local outputs. All four selector arms converge on the one call at
   `0x00445143` through thunk `0x004018A7` to `0x00444C40`.
4. The other exact arms are `chars3\flickd` at `0x004DDFE8` for selector
   values 2/3, `chars4\flickp` at `0x004DDFF8` for 4/5, and
   `chars3\flickp` at `0x004DE008` for 6/10/11/14. The accepted Training log's
   `chars\flick` pair independently selects the default arm; it does not by
   itself establish a semantic identity for selector `0x00861C84`.

Relevant native file offsets are `0x66DC2` for call site `0x004679C2`,
`0x444EC` for the `chars\flick` push at `0x004450EC`, and `0x44543` for the
pair-loader call at `0x00445143`.

## Pair coordinator and whole-file load

- Resource ID zero makes `0x00444C40` use per-ID ANM slot `0x005B18E0`.
- The coordinator first appends `.anm` from `0x004DDC14`, calls loader thunk
  `0x00401082` at `0x00444CD8`, stores the buffer in slot `0x005B18E0`, and
  calls the separate ANM consumer at `0x00444D21`.
- It then passes the unchanged `chars\flick` base path, current object index
  zero, and scene-arena cursor to `0x00448010` at `0x00444D69` (native file
  offset `0x44169`).
- `0x00448010` appends `.all` from `0x004DE028` and calls the same whole-file
  loader thunk at `0x00448079` (native file offset `0x47479`). Thunk
  `0x00401082` jumps to `0x004AE240`, which emits the `LOAD : Loading file`
  line and reads the complete file into the supplied cursor.
- The accepted replacement-arm log records `level07\level1.dat`,
  `terr1.all`, `bits\plantter.all`, `chars\flick.anm`, then
  `chars\flick.all` at lines 1456-1460. This order independently agrees with
  the one static character call preceding later selected resources.

## First consumer and exact selected-file boundary

`0x00448010` is both the `.all` requester and first format-specific consumer.
It does not retain or pass the 13,548-byte loader return. For both exact
M2.20 files, every value used in the following boundary is identical:

- the first dword is `0x1600`; `0x00448085-0x00448087` doubles it, locating a
  table at file offset `0x2C00`;
- the dword at `0x2C00` is 30; the loop at
  `0x0044809B-0x0044818B` walks 30 source descriptors beginning at `0x2C04`
  with exact stride `0x4C`;
- `0x2C04 + 30 * 0x4C == 0x34EC`, exactly the file size;
- the dword compared with `0x100` at `0x004480C3-0x004480CC` is `1` in
  source descriptors 0-23, `287` in descriptors 24-28, and `9` in descriptor
  29. Only values below `0x100` take the shared-entry copy path and increment
  the return count, so this file materializes 25 destination entries;
- the sum of the 30 exact dwords consumed at `0x00448171-0x00448181` is
  `0x15FE`. Doubling that sum and adding the initial four bytes gives
  `0x2C00`, so the supplied arena cursor advances from the blob base to the
  start of the now-consumed descriptor table. This describes cursor behavior,
  not a field meaning or a general `.ALL` invariant.

No destination capacity or loader byte size bounds the original parser. The
file-end equality above independently bounds only these two exact selected
files.

## Runtime destination range

The caller supplies initial object index zero. On the below-`0x100` path,
`0x004480B0-0x00448144` derives a destination at
`0x005A9660 + index * 0x50`, copies selected source values, stores the current
arena pointer at entry `+0x20`, and advances by `0x50` for each materialized
entry.

For both exact M2.20 files:

- the first consumer writes 25 entries, indices 0-24, across
  `[0x005A9660, 0x005A9E30)`;
- source descriptor 29 takes the special `9` branch at
  `0x00448111-0x0044812D`, leaving destination word `+0x2E == 12` in entry
  24;
- immediately after return, `0x00444D97-0x00444DDC` tests that exact final
  word, decrements the caller's object index from 25 to 24, copies two
  address-bounded outputs, and writes 24 as the end index in the ID-zero ANM
  header at slot `0x005B18E0`;
- `0x00444D1D` had already written starting index zero into that header.

The retained ID-zero header range is therefore indices `[0,24)`: 24
`0x50`-byte entries at `[0x005A9660, 0x005A9DE0)`. Entry 24 at
`[0x005A9DE0, 0x005A9E30)` is demonstrably populated and consumed by the
coordinator but excluded from that retained range. These are address/range
claims only.

## Evidence boundary

Confirmed for this exact executable and both M2.20 selected files:

- `0x004671D0 -> 0x00445020 -> 0x00444C40 -> 0x00448010 -> 0x004AE240`
  is the request/load chain for the accepted Training path;
- resource ID zero owns ANM slot `0x005B18E0` and retained shared-entry range
  `[0x005A9660, 0x005A9DE0)` after the first consumer/coordinator boundary;
- the accepted runtime request and ordering agree with the static branch and
  extension construction.

Still unknown:

- semantic meanings of the exact file values, source descriptors, shared
  entries, or ID-zero header fields;
- arena capacity, malformed-file behavior, and whether the same exact
  file-end relationships hold across other `.ALL` files;
- which M1 20-byte scene record or positive payload target, if any, selects or
  consumes this resource range;
- whether filename `flick` or the M2.20 central-figure render box identifies a
  character, model, animation, texture, or other resource role.
