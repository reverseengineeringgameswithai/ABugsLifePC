---
type: experiment
id: EXP-20260910-008
date: 2026-09-10
environment: Fedora host, native x86 Unicorn at two PE bases, real Tk GUI and isolated Studio build
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
question: Where are the Training instruction-sign images stored, how does native code select and draw them, and can one be replaced without changing its number or lesson trigger?
result: Training LEVEL1.RAW type 0x26/id 50 holds 13 frames of 64x64 eight-bit indices in the page-17 palette; descriptor table 005BFD70 (initialized by 0043CBE0 from 004DC238) puts the art at atlas (64,0) and the number at (96,16), over the sign's right-centre 32x32; 0043C250 maps stages to frames with the middle two swapped and does not redraw from stage 13; 00410A20 writes the texture atlas; a rewritten packet decodes and draws natively; no new live-game acceptance.
status: accepted-bounded
created: 2026-09-10
updated: 2026-10-29
tags: [experiment/tutorial, re/native, re/graphics]
---

# Replaceable Soil sign images

This note covers the instruction board beside Mr. Soil in Training, not the
level-ending marker: where its pictures are stored, how native code selects and
draws them, and what a replacement must preserve.
[[EXP-20260910-007 - Five-throw Training sign and native defaults]] remains the
count/progression authority.

## Independent PC resource and instruction evidence

Original Training `LEVEL07/LEVEL1.RAW` SHA256
`c5f81eed3c9d1a01cc188ead50fc10a5ae0f213b0ca165764fa7b311a02a0926`:

- Type0x26/id50 (0x32), compressed packet offset0x49694 /300692,
  14039 bytes, decoded53264. Header `2600000032000000400040000d000000`:
  tag/id, width64, height64,13 frames,0 local palette entries. Each frame is
  4096 eight-bit palette indices after the16-byte resource header.
- Separate type0x26/id51 (0x33) at0x4CD6B /314731 is the six32×32 number bank.
  It remains byte-exact here; its range is not extended.
- Palette/texture page17 packet at0x1E04F decodes to66316 bytes. Its header
  is `<I4H` =17,256,256,768,1; RGB palette bytes12..779 precede65536 pixels.
  Palette SHA256 `b92e8d9ed231c3708cdb31fcf952d1ece0228c1d21521c1717fa35cb7f7ec36d`.
  All256 colours are distinct; it is not just a grayscale palette. The complete
  page packet remains unchanged, including unrelated texture pixels.

Static0043CBE0 initializes the005BFD70 descriptor table from004DC238. Executing
that original initializer independently confirms slot50→004DC218 and
slot51→004DC228. Original descriptor bytes are respectively
`11003f3f0000000040000000` and `110010200000000060100000`.
Both target page17: art at atlas(64,0), number at(96,16). Thus the number replaces
the right-centre32×32 rectangle, sign-relative x32..63/y16..47, including its
black background. Changing the picture does not change that rectangle's ownership.

Original0043C250 calls50 then51 for stages0..3; stages4..12 call50 only.
Zero-based stage→image mapping is0,1,2,3,4,5,6,7,9,8,10,11,12: the two
middle frames are swapped. Stage13 and above do not redraw. The final14th
instruction therefore retains lesson13's blueberry picture; no separate import
slot is offered for it. Calls at0043C2A6/0043C2E0 and0043C2BD pass through
004016CC to00410A20. Fresh disassembly and original-x86 execution agree.

00410A20 writes the texture atlas, not a conventional screen-space HUD bitmap.
DAT0059F7F0 selects software1/hardware2. Eight-bit frame source uses
0076F9B8 and payload offset8+local-palette-count×3+frame×width×height.
The software path converts through RGB555; the hardware path either copies
indices or uses its surface's RGB masks/divisors. No unidentified field was
renamed from decompiler interpretation alone.

## Native evidence

Metadata: `reports/studio/EXP-20260910-008.json`. Private complete packet:
`work/experiments/EXP-20260910-008/gui/`, including13 original PNGs and a
diagnostic PNG. No assets enter Git.

`tests/test_soil_sign.py::native_render_proof` executes original0049A200 on a
rewritten packet and compares all decoded bytes plus guard regions. It then
executes0043C250 and00410A20 for every13 frame through software16/hardware8/
hardware16 at PE bases400000 and1000000. Six combinations pass, including the
patched five-throw initial number, other count lessons,8/9 mapping, entire
surrounding atlas unchanged and terminal retention. Surface/COM allocation and
locking are bounded host stubs; these are native pixel-write proofs, not live
GPU screenshots.

A test copy with one replaced frame differs from its base only in
`CD/LEVEL07/LEVEL1.RAW` (replacement RAW SHA256
`2471c509b3b65c58cef667819256bbb22c65e4e5bdf295c23b5299da6d7fd1f5`); all50 other
packets, suffix, palette, number bank and12 other art frames remain exact.
Replacing the edited compressed packet with the original gives the exact input
RAW. The no-override and same-pixel cases return the original bytes. No new
game, live memory access or game input.

## Modification boundary

A replacement frame is 4096 eight-bit indices into the fixed page-17 palette;
the number rectangle keeps its ownership, so the first four lessons still show
their native count over the right-centre32×32. No new palette, sign geometry,
number graphics, arbitrary-resolution texture or separate final-stage picture
is supported. Native RAW reads and every decoded packet/frame extent are bounded;
unknown fields and packets stay exact. A custom-image live playtest is still
required for final in-world visual acceptance.
