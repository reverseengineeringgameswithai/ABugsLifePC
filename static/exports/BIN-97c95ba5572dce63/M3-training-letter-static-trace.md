# M3 Training FLIK-letter static trace

Binary SHA-256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`

Source Training DAT SHA-256:
`20d0f9b143a4fceeb058d5ce81680b3e6317995abc3d5ac4103fc85e79b5fd40`

## Exact records

The first type-`0x3F` table has count 63. Its four singleton selector records
are:

| Index | File offset | Selector | Source position |
|---:|---:|---:|---|
| 50 | `0x328` | `0x10` | `(-2733,-50,5061)` |
| 51 | `0x338` | `0x11` | `(4821,-50,2773)` |
| 52 | `0x348` | `0x12` | `(3205,-50,-4510)` |
| 53 | `0x358` | `0x13` | `(-5366,-50,-3184)` |

The selector bytes collectively identify the Training FLIK-letter set through
their common pickup mask path. Exact selector-to-visible-glyph identity was not
separately discriminated, so the individual records remain selector-addressed.

The accepted recipe copies all 16 bytes of each source record, changes only
the copied coordinate tuple, and appends indices 63–66 at output offsets
`0x3F8`, `0x408`, `0x418`, and `0x428`. The type-`0x3F` count becomes 67 and
the remainder of the physical file moves by `0x40`; the same 556 known PC
file-relative pointer fields move by `0x40`.

## Initialization

`0x00456A90` walks the relocated table at `0x005C595C`. Selectors other than
`0x14`, including `0x10`–`0x13`, take its alternate terrain/correction route.
The accepted live table initializes duplicate indices 63–66 as:

| Index | Selector | Live `(x,y,z)` | Live signed word `+0x0E` |
|---:|---:|---|---:|
| 63 | `0x10` | `(4900,-1853,1500)` | `-1053` |
| 64 | `0x11` | `(5100,-1849,1000)` | `-1049` |
| 65 | `0x12` | `(5000,-1842,500)` | `-1042` |
| 66 | `0x13` | `(4900,-1854,0)` | `-1054` |

This runtime result shows that authored `y=-50` is transformed for the moved
copies rather than blindly retaining an original placement height.

## Pickup mask and repeated completion

`0x00417720` writes consumed sentinel `0x80000000` to entry dword `+0x04` at
`0x00417A30`, then dispatches on selector byte `+0x0C`:

| Selector | Case address | OR mask written to `0x0059D9B2` |
|---:|---:|---:|
| `0x10` | `0x00417A59` | `0x01` |
| `0x11` | `0x00417AB3` | `0x02` |
| `0x12` | `0x00417B3B` | `0x04` |
| `0x13` | `0x00417BC3` | `0x08` |

Each case compares the resulting byte with `0x0F`. The equality path records
player state, calls the existing event path, and increments byte
`0x0059D9B0` while it is below nine (`0x00417C5A–0x00417C77`). There is no
transition-only guard: if the mask is already `0x0F`, a later duplicate again
reaches the completion path. `EXP-20260814-113` independently confirms this
with a duplicate pickup that retains mask 15 and changes the byte `1 -> 2`.

## Mod boundary

The data transformation can move, duplicate, or remove the exact singleton
letter records and reconstruct its source byte-for-byte. The accepted demo
duplicates all four at moved positions. It does not claim one-shot completion
semantics for duplicate letters; suppressing the repeated reward would require
a separately authorized and validated gameplay-code change.
