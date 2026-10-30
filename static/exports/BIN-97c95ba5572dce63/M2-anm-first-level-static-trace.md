# M2 PC `.ANM` first-level static trace

## Scope and identity

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Loader/coordinator: `0x00444C40`
- First consumer: `0x00444B70`
- Static sources: exact-hash work-copy executable, GNU objdump 2.44, and the
  existing Ghidra evidence export.

No runtime was launched or modified. No PS1 source or findings were consulted.

## Caller boundary

`0x00444C40` constructs the `.anm` path and loads the complete file at
`0x00444CD8`. The loader returns its byte size; instructions
`0x00444CDD–0x00444CF7` advance the caller-owned arena cursor by that size
rounded up to four bytes. The size is not passed to `0x00444B70`.

Before the first consumer runs, the caller modifies the in-memory header:

- `0x00444D0E` writes word `1` at file-relative `+0x00`;
- `0x00444D13–0x00444D1D` copies a caller value to word `+0x04`;
- `0x00444D16` pushes nonzero flag `1` and `0x00444D21` calls the consumer.

The checked PC files contain zero in both fields on disk. Their runtime values
at the consumer are therefore caller state, not file-format constants.

## First-level walk at `0x00444B70`

The function treats its first argument as a file base:

1. Reads a signed 16-bit count at `+0x02`
   (`0x00444B7C–0x00444B80`).
2. Reads `count` file-relative dword offsets beginning at `+0x08`
   (`0x00444B82–0x00444BA0`).
3. Leaves zero entries unchanged; adds the file base to every nonzero entry in
   place at `0x00444B91–0x00444B95`.
4. Retains only the first nonzero relocated pointer for the remaining walk
   (`0x00444B93–0x00444B99`).
5. If that pointer and the second argument are nonzero, reads an unsigned
   16-bit nested count at first-record `+0x08`, sets one global to
   first-record `+0x0C`, and another to the address immediately after
   `count*2` bytes (`0x00444BA2–0x00444BC8`).
6. Scans those signed 16-bit items and handles only value `-2`
   (`0x00444BCE–0x00444C05`).

The routine does not inspect nested content for every first-level offset. It
follows the first nonzero reference only. It also receives no file size, so an
independent safe inspector must add bounds checks that the original routine
cannot perform at this call boundary.

## Bounded disk layout

```text
+0x00  u16  unknown on-disk field; caller overwrites with 1
+0x02  i16  first-level offset count
+0x04  u16  unknown on-disk field; caller overwrites before consumer
+0x06  u16  unknown field
+0x08  u32[count] file-relative offsets; zero is permitted by code

first nonzero referenced record:
+0x00  8 bytes unknown to this consumer
+0x08  u16 signed-item count
+0x0A  2 bytes unknown to this consumer
+0x0C  i16[count] items; only -2 is distinguished here
```

This is a consumer-read boundary, not a complete `.ANM` semantic model.

## Independent corpus observations

The bounds-checked implementation accepted all 11 PC `CD/PLANTS/*.ANM` files
with zero failures. Across that corpus:

- on-disk words `+0x00`, `+0x04`, and `+0x06` are all zero;
- the first-level count is 3 or 4;
- every first-level offset is nonzero, in range, even, and strictly increasing;
- the first offset equals the exact end of the offset table;
- the first referenced record's nested count ranges from 1 through 7;
- only `PLANT03.ANM` contains a `-2` in the inspected list, at item index 6.

These whole-corpus regularities are observations, not parser requirements
unless directly required for memory-safe access. Exact metadata and hashes are
in `reports/resources/pc-plant-anm-first-level.md`.

## Independent implementation boundary

`reimplementation/ablpc/anm.py`:

- preserves the complete input byte string unchanged;
- bounds-checks the header, offset table, every nonzero offset, the first
  referenced header, and its signed-item list;
- rejects negative/impossible counts and out-of-file offsets;
- reports offset-named fields and `-2` indices without exposing unknown bytes;
- does not relocate, serialize changes, or expose editing.

Synthetic tests cover truncation, negative/impossible counts, zero offsets,
out-of-range offsets, truncated nested headers, impossible nested counts,
lossless preservation, and metadata-only CLI output.
