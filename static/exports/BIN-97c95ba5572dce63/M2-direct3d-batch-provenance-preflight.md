# M2 Direct3D batch-provenance preflight

> [!IMPORTANT] M2.28 count-label correction
> `EXP-20260813-041` proves that `B4/B3` count completed append paths inferred
> from batch deltas, not every function entry. The exact append equations,
> roots, pages, and flush/reset proof below remain unchanged.

## Provenance and scope

- Executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Sources: exact native GNU `objdump -d -Mintel` disassembly and the checked
  structured Ghidra export.
- Experiment: `EXP-20260813-040`.

This PC-native preflight accounts for the counters and reset/flush edges
reachable from the exact retained-entry call to `0x0044F8E0`. It assigns no
primitive, asset, or source-field meanings. No PS1 evidence was used.

## Builder and family layout

Renderer selector 2 reaches `0x00405FE0` at caller site `0x0044F99D` for the
masked `0x3C` record form and `0x00407450` at `0x0045029F` for `0x34`.
Besides common helper `0x004B0240`, their only direct callees are the thunks to
flush functions `0x004056A0` and `0x004058D0`.

Both builders select one of two fixed-root batch families. Page index is
bounded to `0..31` by the caller/builder masks.

| structural field | root through `0x004C4108` | root through `0x004C410C` |
|---|---:|---:|
| exact root value | `0x004F1730` | `0x00511510` |
| vertex pointer table | `root + page*4` | `root + page*4` |
| vertex count | `root + 0x104 + page*2` | `root + 0x104 + page*2` |
| inline index page | `root + 0x186 + page*0x7D0` | `root + 0x186 + page*0x2580` |
| index count | `root + 0x1FD56 + page*2` | `root + 0x4B186 + page*2` |
| bounded index capacity | 1,000 16-bit values | 4,800 16-bit values |

The first root is written explicitly at `0x0040FEE2`. The second is the
image-initialized pointer value stored at `0x004C410C`; the nearby alternating
values `0x005C5F10/0x00602330` belong to `0x005C5968`, not this root.

`0x00405FE0` checks whether the current vertex count is greater than 493,
flushes if so, then appends four `0x20`-byte vertex records and six indices.
`0x00407450` uses the same precheck and appends three vertex records and three
indices. Thus a measured interval with counts `(V,I)` can be decomposed
structurally as `B4=(I-V)/2`, `B3=(V-4*B4)/3`, where `B4/B3` are completed
four-input and three-input append paths; the names do not assign primitives.

## Complete reset/flush accounting

- Family `0x004C4108`: `0x004056A0` calls the device vtable `+0x78` at
  `0x00405816`. Its write to marker `0x004C4118` at `0x00405831` reports data-
  watch stop PC `0x00405838`, before index reset `0x0040583E` and vertex reset
  `0x0040584D`.
- Family `0x004C410C`: `0x004058D0` calls the same vtable slot at
  `0x0040598B`. Its marker write at `0x004059A5` reports stop PC `0x004059AB`,
  before resets `0x004059B7` and `0x004059C8`.
- Register `ESI` still carries the exact page index at both pre-reset marker
  stops. No other counter reset/flush callee is reachable inside the two
  builders.

One hardware data watch on `0x004C4118`, filtered to those two PCs, therefore
captures every reachable in-call segment before reset. A counter decrease
without such a marker is a terminal contradiction.

## Exact pre/post boundaries

- Pre: a data watch on selector `0x0059F7F0`, filtered to stop PCs
  `0x0044F951/0x0045026C`, observes the first selected record before its
  builder call.
- Caller receipt: native prologue `0x0044F8E4-0x0044F8ED` moves `ESP` by
  `0x58`. `[ESP+0x58]` must be return address `0x0044C89E`; preserved caller
  `ESI` at `[ESP+0x04]` must be on the 24-entry lattice rooted at
  `0x005A9660`, stride `0x50`; preserved caller `EBP` at `[ESP+0x08]` must
  equal its index. The function overwrites its original argument slot at
  `[ESP+0x5C]` with a stream cursor at `0x0044F905`, so that slot is not a
  valid later caller receipt.
- Post: the established data watch on `0x005B18E0`, exact stop PC
  `0x0044C8AB`, observes return from `0x0044F8E0` while `ESI` still carries
  the current entry pointer.

Entry 8 can reach the exact post without any selected pre record and is
outside the M2.24 candidate set. The ordered state machine therefore treats a
candidate post without a pre as an exact zero-builder interval and retains
only candidate rows. Repeated pre stops for records in one entry share one
snapshot. Roots, pointers, counts, page/order/caller receipts, digest bounds,
signals, cleanup, detach, and survival all fail closed.

## Approved runtime design

The user's explicit M2.27 instruction supplied fresh authority for the three
read-only hardware data watches and bounded execution control. Watch-spec
schema 4 hashes only newly appended vertex/index intervals, preserves
pre-reset segment metadata, and never places payload bytes in results. Exact
watch conditions filter unrelated PCs and non-`0x0044C89E` callers. One
warmup rollover and one complete ordered cycle are required in fresh
control/replacement/control Direct3D arms.
