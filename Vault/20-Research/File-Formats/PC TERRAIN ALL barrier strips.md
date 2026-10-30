---
type: file-format
status: confirmed-bounded-reader
created: 2026-09-04
updated: 2026-10-02
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260904-002, EXP-20260904-003]
tags: [re/file-format, re/collision]
---

# PC TERRAIN ALL barrier strips

[[PC barrier translation prototype]] now edits this canonical representation
without resizing it. [[EXP-20260904-004 - Translated barrier live collision proof]]
adds live evidence for one four-segment relocation; the grammar evidence and
reader from EXP-003 below remain unchanged.

## Confirmed source layout

This is the payload grammar of terrain source kind **0x101**, not the complete
0x4C-byte source descriptor. Reuse the existing
[[PC TERRAIN ALL collision descriptor source]] directory walk. The high-kind loader links these payloads
through `007f3d3c`; the movement coordinator consumes the list at
`004ab60f..004ab73a`. Evidence and measurements:
[[EXP-20260904-003 - Barrier grammar and landing-seeded grounded movement]].

All fields are little-endian. Offsets below are relative to the payload.

| Offset | Width | Role |
| --- | --- | --- |
| `+0x00` | u32 | source magic `0x12345678`; replaced in emulated/runtime memory with the next-node pointer |
| `+0x04` | u16 | segment count N, read by `004ab626` |
| `+0x06` | u16 | unknown; preserved (zero in all 65 examined retail strips) |
| `+0x08` | `(N+1)*12` | connected point array |
| after points | remaining payload bytes | preserved trailer; empty in the examined corpus |

A point contains signed 32-bit **X**, a **middle dword**, and signed 32-bit
**Z**. Coordinates are multiplied by32 in the collision response; the middle
dword is not a world-Y coordinate. Segment i joins points i and i+1. There is
no extra implicit closing edge: an authored closed strip must provide its
closing point. The runtime list head points to payload+4, so the next-node
pointer is at head-4; the point array is at head+4.

## Bounds interleaved with point data

Segments are visited in blocks of16 (`004ab71b..004ab729`). Block k begins at
point `16*k`. A full block uses the middle dwords of its first four points:

| Point within block | Middle dword |
| --- | --- |
| 0 | minimum X |
| 1 | X span |
| 2 | minimum Z |
| 3 | Z span |

These fields bound all17 endpoints of that block, including its shared endpoint
with the next block. They can be loose: do not normalize them to tight bounds.
The original collector reads them at `004ab634..004ab666`. A passing full-block
gate scans exactly16 segments, then advances by192 bytes (16 points).

A final block with1..15 segments instead places **INT32_MIN (`0x80000000`)**
in its first point's middle dword. The sentinel branch at `004ab671` scans to
N rather than to `block_start+16`. All other middle words remain preserved;
their roles outside these accesses are unknown.

The reader deliberately admits the observed canonical form: bounds for every
full block, sentinel for a short tail, nonnegative spans. An early sentinel can
make the native loop scan all remaining segments and revisit later blocks;
a short tail without the sentinel can read past its declared endpoints. Those
forms are rejected rather than silently repaired. This rejection is a bounded
reader contract, not a claim that every other byte sequence necessarily crashes.

## Original candidate limits and ordering

The padded query rectangle is based on the requested movement magnitude plus
`0x1880`. The block gates are unsigned interval tests; endpoint interval overlap
is inclusive. The independent test oracle covers the fixed nonoverflowing
experiment domain, including truncation toward zero when converting negative
positions to stored units. It is not a general movement solver.

The original code (`004ab6c5..004ab704`) admits at most **32 endpoints /16
segment pairs**, preserving traversal order and silently omitting later passing
segments. The loader prepends records, so within a loaded file the list visits
later source records first. Point order determines each segment's blocking
orientation (EXP-002); it must not be sorted geometrically by a future writer.

## Coverage and use

All18 retail `TERRAIN.ALL`/`TERR1.ALL` files under `CD/LEVEL00..LEVEL10` parse:
65 strips,6,722 segments,396 bounded blocks and62 sentinel tails. Every stored
block bound covers its endpoints. Full source hashes are in the EXP-003 report.
108 Level01/Level03 query cases match original ordered collection; five
synthetic sizes4/16/17/32/33 verify boundaries and the16-pair cap.

Read-only API:

```python
from ablpc.terrain_all import TerrainAll
from ablpc.terrain_barriers import BarrierPayload

terrain = TerrainAll.from_path(work_copy_path)
strip = BarrierPayload.from_terrain(terrain, source_record_index)
```

The parser bounds-checks the header, count and point array; retains complete
raw bytes, unknown header/middle words and trailer; and rejects wrong source
kinds and unsupported block layouts. It provides no serializer or writer.
Collision normalization limits, overflow behavior outside the tested domain,
unobserved record variants and live authored-geometry acceptance remain open.

*Update (2026-10-02 audit):* writers now exist outside this reader.
`terrain_barrier_edit.py` translates a strip without resizing it (one live
fixture, EXP-20260904-004). `terrain_perimeter.py` builds bounded orthogonal
closed loops from this grammar; [[EXP-20260906-006 - Perimeter barriers and original foliage reference]]
reached a file-loaded grass-boundary preview with user-confirmed blocking. Its
first native winding arms were not accepted, and no general strip writer or
universal contact rule is claimed.
