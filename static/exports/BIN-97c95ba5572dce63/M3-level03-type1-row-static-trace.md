# M3 Level03 type-1 row static trace

Binary SHA-256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`

Level data SHA-256:
`bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b`

## Loader identity

- `0x0044BB70` walks top records and writes their relocated addresses into the
  pointer table rooted at `0x005C5860`.
- Type 1 is pointer slot `0x005C5864`.
- Level03 top-record index 1 begins at file offset `0x458`, has type 1, count
  18, and 12-byte signed XYZ rows. Row 6 begins at `0x4A4` and is
  `(15678,0,15438)`.

## Candidate selection path

- `0x00432930` first tests bit `0x10` in word `0x0059D9A0`.
- The function reads the type-1 pointer from `0x005C5864` and scans its
  12-byte rows by squared X/Z distance from the current player globals
  `0x0059D960` and `0x0059D968` after the matching scale conversion.
- It writes the selected row X and Z shifted left by five to those globals and
  recomputes Y through the existing terrain-height path before applying its
  fixed vertical adjustment.
- `0x00437A20` contains a near-identical mode/character-specific path.
- `0x0042DDB0` dispatches to these variants based on `0x00861C84` and later
  clears state bits through `and word [0x0059D9A0],0x20`.

## Candidate state producer

- `0x0041C6C0` is an address-named collision/reset coordinator candidate.
- At `0x0041C8CC` its nonzero, non-2 fourth-argument branch ORs `0x14` into
  `0x0059D9A0`. The exact-2 branch ORs only `0x04`.
- This joins the `0x10` selector gate statically, but does not yet prove which
  natural PC event reaches it in Level03.

## Multiple-consumer boundary

Type 1 is not promoted as a bespoke respawn or checkpoint table:

- `0x004317D0` consumes neighboring type-1 coordinate rows in another update
  path.
- `0x004323A8` scans type-1 rows using three-coordinate proximity and retains
  row indices.
- `0x004369B0` initializes from the first type-1 row and advances through
  indexed rows.
- `0x0043CE60` consumes type 1 together with type 2.

## Exact discriminator

Change only Level03 row-6 X at file offset `0x4A4` from `15678` to `15806`.
If `0x00432930` selects that row, its left shift predicts a `+4096` runtime X
change, unchanged authored Z, and terrain-recomputed Y. This prediction is not
yet PC runtime evidence.
