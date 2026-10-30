---
type: experiment
id: EXP-20261018-009
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static disassembly (capstone) of the retail texture converter, plus a recomputation from the hash-checked retail Anthill LEVEL.RAW compared with the live page that EXP-20260905-005 read in a hardware arm; no new game launch
question: Is the "one palette row per 64×64 block" reading of 4-bit pages (EXP-20260928-001) the executable's own rule?
result: Yes. The 4-bit branch of the converter 0x00462C30 (0x004630D2–0x00463126) gives each source byte the palette row ((byte >> 13) & 3) * 4 + ((byte >> 5) & 3), which on a 256-wide page is (v/64)*4 + u/64, and stores row*16 + nibble, low nibble first. Decoding Anthill's page 0 with that rule reproduces, byte for byte, the live index buffer EXP-20260905-005 read
status: complete-bounded
created: 2026-10-18
updated: 2026-10-29
evidence: [EXP-20260928-001, EXP-20260905-005]
tags: [experiment/static, experiment/runtime, re/graphics]
---

# EXP-20261018-009 - Four-bit page palette rows

## Question

EXP-20260928-001 read, from a hardware observation of derived page-0
palettes, that a 4-bit page uses one 16-colour palette row per 64×64 block,
`(v/64)*4 + u/64`. Its limits say the reading is "not by a traced renderer
routine". Section 7 of [[Next Tasks]] listed it as open.

The code already cited the converter.
`reimplementation/ablpc/original_level.py` `texture_page` has said since
`df7823dd` (2026-09-10) that "00462C30 expands low nibble first, bank =
x//64 + 4*(y//64)", with no instruction range or note behind it. This
experiment supplies both.

## The routine

- **Entry.** `CONVPSXTPAGE4` (`0x00466260`, log "Converting 16 colour
  tpage") copies the page's 768-byte palette to `0x005844F4 + tpage*0x300`.
  It then calls the converter `0x00462C30` through thunk `0x0040178F` with
  mode 0.
- **The converter**, `0x00462C30`:
  - copies the palette to the stack and turns near-pure green (`G ≥ 0xFA`,
    `R = B = 0`) into the colour key (`0x00462C64`–`0x00462C8A`);
  - switches on its mode argument (`0x00462C8C`): 0 is the 4-bit branch
    read here, and 2 reads 16-bit 5-5-5 words. Mode 1's format was not
    checked.
- **The 4-bit branch** (`0x004630D2`–`0x00463126`) runs once per source
  byte, `edi` counting bytes:

  ```text
  row = (((edi >> 13) & 3) * 4 + ((edi >> 5) & 3)) & 15     ; 0x004630DD-0x004630EC
  ```

  A 256-pixel row is 128 bytes, so `(edi >> 5) & 3` is `u/64` and
  `(edi >> 13) & 3` is `v/64`.
  - **Direct3D** (selector 2, `0x004630FE`–`0x00463115`) writes two 8-bit
    indices, `row*16 + (byte & 15)` and then `row*16 + (byte >> 4)`. The
    executable's `CreatePalette`/`SetPalette` strings suggest a palettized
    texture; that was not traced. (Under Wine the game asks for one and
    falls back to 16-bit 1-5-5-5: the log line "FAILURE to map tpage … as a
    8 bit palettized surface", [[EXP-20261018-013 - Options screens and the creature gate live]].)
  - **Software** (selector 1, `0x0046311C`–`0x00463133`) looks up the RGB
    of `row*16 + (byte & 15)` in the stacked palette, with the same row rule.

## Runtime check

[[EXP-20260905-005 - Original wall texture regions and colour inputs]] read
Anthill's live page 0 from a hardware arm:

- the 65,536 index bytes at `[0x00582EB0]`, SHA `da6ed966…`;
- the palette at `0x005844F4`, SHA `0e848743…`.

On the retail disc that page is 4-bit (mode 0). Decoding it with the row
rule (`original_levels.texture_image`) gives index SHA
`da6ed96650d2a3464f6d8af8d37f6088222d744ae95b322bff0031d9e14caf85` and
palette SHA
`0e848743ea7fcae70325a8a71b9691a65f048d4634781212860627120d57e1dc`, both
identical. The page uses all 16 rows.

## Confirmed, inferred, unknown

- **Confirmed (static and runtime).** The palette-row rule for 4-bit pages,
  and the low-nibble-first order.
- **Confirmed (static).** Each branch's output form.
- **Unknown.** Nothing for this rule. The 8-bit and 16-bit branches were not
  re-read here.

## Consequences

- EXP-20260928-001's "not by a traced renderer routine" and the matching line
  in [[Known Unknowns#Engine questions from derived test builds]] are
  superseded.
- The decoders `original_level.texture_page` and
  `original_levels.texture_image` follow the native rule.
