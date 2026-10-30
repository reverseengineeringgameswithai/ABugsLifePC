# M3 Training FLIKFLIK static trace

Retail PC authority: `bugs.exe`, 1,069,056 bytes, SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Accepted M3.4 output: 1,069,056 bytes, SHA-256
`b572e6d19bc417969c159ba0df7521cbb01b675c260a4dc98d2e6b34475947f4`.

## Retail consumers

- `0x00416890` reads letter mask byte `0x0059D9B2`; retail draws four slots at
  `0x00416DF9` through `0x00416EBB` and tests completion against `0x0F` at
  `0x00416DDD`.
- `0x00417720` consumes type-`0x3F` records. Selector cases at
  `0x00417A59`, `0x00417AB3`, `0x00417B3B`, and `0x00417BC3` OR retail bits
  `1/2/4/8`; their reward gates compare the result with `0x0F` through
  operands at `0x00417AA3`, `0x00417AFD`, `0x00417B85`, and `0x00417C0D`.
- `0x00442E70` draws the level-complete tally. Retail four-letter drawing
  begins at `0x004430B5`, denominator literal four is at `0x004431E3`, and
  emblem gate literal four is at `0x00443328`.
- Tally count consumers at `0x00443473`, `0x004434CD`, `0x004435A3`, and
  `0x004435E5` address retail table `0x004DD6C0`. Only its first 16 bytes are
  the four-bit popcount values needed by the retail mask; later bytes are
  unrelated data and cannot safely count arbitrary eight-bit masks.

## Authored exact packet

The recipe applies 29 non-overlapping spans totaling 686 bytes; 677 bytes
change. Major claims are:

| Purpose | VA/file offset | Width |
|---|---:|---:|
| centered in-level eight-slot helper redirect | `0x00416DF9` / `0x0161F9` | 10 |
| centered tally eight-slot helper redirect | `0x004430BD` / `0x0424BD` | 10 |
| four pickup helper redirects | `0x00417A65`, `0x00417ABF`, `0x00417B47`, `0x00417BCF` | 7 each |
| three all-eight comparisons | `0x00416DDD`, `0x00442F64`, `0x0044348D` | 1 each |
| four transition-scratch gates | `0x00417AA3`, `0x00417AFD`, `0x00417B85`, `0x00417C0D` | 5 each |
| four full-popcount pointers | `0x00443473`, `0x004434CD`, `0x004435A3`, `0x004435E5` | 4 each |
| `/8`, emblem gate, and layout literals | `0x004431C4`–`0x00443372` | 11 spans |
| helper/code/table packet | `0x004BBA00` / `0x0BAE00` | 576 |

The code packet has SHA-256
`0d32f7fadf1dd7ccbfaba8689e9bb3a95278fcc7e6ab161084359e5eb27f8370`.
It contains:

- in-level renderer `0x004BBA00`;
- tally renderer `0x004BBA64`;
- selector entry points `0x004BBACC`, `0x004BBAD1`, `0x004BBAD6`, and
  `0x004BBADB`;
- eight tally x positions at `0x004BBB20`;
- a complete 256-byte popcount table at `0x004BBB40`.

All new code-side global reads use call/pop-relative addressing, so the cave
adds no absolute base-relocation requirement. The eight modified absolute
operands listed above already have type-3 HIGHLOW entries in the retail
relocation directory; no redirect or cave span overlaps another relocation.

## Scratch and PE boundary

`0x0086396F` is exactly the final byte before the original writable `.data`
virtual end at `0x00863970`. It is zero-initialized, beyond `.data` raw bytes,
and the retail file contains no direct little-endian reference to that
address. Runtime evidence is still required because absence of a direct
static reference does not prove absence of computed access.

Retail and output PE headers plus all six section tuples are byte-identical.
The file size is unchanged. The builder proves M3.4 inverse reconstruction to
the accepted M3.2 intermediate and independently proves the M3.2 inverse to
retail.

## Scope

This trace supports exact Training `FLIKFLIK` only. It does not establish a
general text engine, arbitrary glyph mapping, more than eight slots, other
levels, new emblem assets, or save-format compatibility.
