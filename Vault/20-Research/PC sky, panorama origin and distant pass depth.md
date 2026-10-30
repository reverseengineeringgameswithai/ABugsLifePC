---
type: research
status: confirmed-bounded
created: 2026-10-29
updated: 2026-10-29
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260907-001, EXP-20260907-002, EXP-20260911-017, EXP-20260911-019, EXP-20260915-001, EXP-20260915-002, EXP-20260915-003, EXP-20261001-004]
tags: [re/rendering, re/static, re/runtime]
---

# PC sky, panorama origin and distant pass depth

How the retail executable draws the sky fill and the scrolling panorama behind
a level, which loaded value places them vertically, how the tint and fade scale
them, and how depth orders the distant scenery pass against the nearby one.
Experiments cited as plain IDs are not in this vault. They changed the backdrop
of Level01 (Anthill) in test builds; the routines below are retail.

## Sky and panorama routines

Confirmed, first recorded in EXP-20260907-001 to EXP-20260907-003 unless
marked:

- **Sky fill `0x00404AE0`.** It clears the sky and ground. Its colour records
  advance 8 bytes and its rectangles 16 bytes. It writes the signed horizon
  `0x004F0384` and builds the clear rectangles from the panorama origin (see
  below; EXP-20260911-019).
- **Colour cache.** The six `.data` colour initializers are overwritten from
  loaded backdrop data, so changing their file bytes alone is insufficient in
  the tested type-36 loader replay. The type-36 loader writes the cache at
  `0x004DE04C..0x004DE060` ([[FUNC-97C95BA5572D-00465030]]).
- **Panorama `0x00405410`.** It updates the unwrapped phase `0x004F0558` and
  draws through `0x00404410`, which submits textured TL vertices through the
  native Direct3D device. It scrolls with the camera heading
  ([[EXP-20260911-014 - Training flower panorama and wall cutoff]]).
- **Negative horizon.** The panorama crops a negative horizon to 0 for texture
  submission (`0x0040550B..0x00405521`); `0x004F0384` itself stays signed
  (EXP-20260915-002, with a live capture at pitch 541: raw horizon −136,
  cropped 0).
- **Call order.** The Direct3D frame begin `0x00405D20` calls `0x00404AE0` and
  `0x00405410` (EXP-20261001-004); the call to `0x00405410` is at
  `0x00405E7A`. The gameplay render itself is reached through the thunk
  `0x00401B81` ([[PC gameplay loop and player event sites]]).
- **Level01 panorama.** Decoded record 29, type 36. Compressed file offset
  `0x45198` (283032) in the retail `LEVEL01/LEVEL.RAW`; decoded 128×96 with 256
  RGB palette entries; first and last indexed pixels give 49/89/219 and
  162/130/105, matching the loaded Level01 cache. Its marker is visible only
  after decompression; a failed raw-byte search does not mean a different
  container. The decoded record is 13,072 bytes (shape 128×96, palette 768,
  format 1), decoded SHA-256
  `1984c86c70abb0814c9e596c397fb49f081dd501d43226c3e3f501c44e5b8795`
  (EXP-20260911-019).
- **Geometry check.** EXP-20260907-002 found identical clear rectangles and
  panorama XYZW/UV/indices between the original and a tinted build at a
  captured camera and five angle overrides; both place the captured quad at
  native Y 76..268.

## The panorama origin

Confirmed, first recorded in EXP-20260911-019 (static, original-PC replay and a
hardware preview):

- The type-36 record's decoded dword at `+4` is the vertical origin: 76 for
  Level01. The loader stores it into `0x004DE048` at `0x004657E2`.
- The sky `0x00404AE0` uses that origin to form the shared horizon
  `0x004F0384` and the matching clear rectangles. The panorama `0x00405410`
  draws from the same horizon. Draws added to a test build and anchored to
  `0x004F0384` moved with it as well.
- **Data-only change.** Setting the origin to 140 moved every panorama vertex
  down exactly 64 pixels at 640×480 in native loader, sky, matrix and panorama
  replay at pitch −128, −64, 0, 64 and 128. X/Z/W, UV, RGB, depth and indices
  stayed exact and the clears matched. Samples at ±256 kept the native
  clipping; a horizon clamped to 0 need not show the full 64-pixel change in
  its stored value. Native pitch, heading and clipping stay in charge. No
  executable change is needed.
- **Re-encoding.** Only decoded byte 4 changed (76 → 140). The original decoder
  `0x0049A200` reproduces the rewritten packet; palette, pixels and the other
  68 packets stayed exact. Re-encoding the packet with a literal-only writer
  grew `LEVEL01/LEVEL.RAW` by 7,745 bytes and preserved the six opaque
  compression header bytes and the suffix. In the rebuilt RAW the packet began
  at offset 321683.
- Validated only at origin 140 and 640×480; other offsets, resolutions and
  camera angles are open.

## Tint, fade and view clock

- **Tint words.** `0x005BA648`/`0x005BD738`/`0x005BA11C` are 16-bit, with 128
  neutral. `0x004188A0` steps them toward targets that fade and transition
  code owns (EXP-20260907-001); `0x00418860` stores the target RGB and speed
  (EXP-20261001-004).
- **Who scales by them.** The quad drawer `0x0040A090` colours with
  fade × 0xE0 >> 7; the sky `0x00404AE0` scales its material by fade >> 7;
  the panorama `0x00404410` references `0x005BA648` (EXP-20261001-004). See
  [[PC level start, special slot and load screen]] for the load-screen fade.
- **View clock.** `0x004558E8` increments the 16-bit word `0x005B1EB8` by 32
  on each view update (static evidence in EXP-20260915-001, live timing in
  EXP-20260915-003). A value that cycles on `(clock >> 6) & 63` therefore repeats every
  128 view updates, about 4.1 s in one live sample (EXP-20260915-001).

## Distant pass depth

[[PC custom distant terrain]] and [[PC custom distant objects]] own the
quarter-scaled secondary (distant) pass and its depth rule;
[[EXP-20260911-015 - Training grass uses secondary background geometry]] and
[[EXP-20260911-016 - Training grass boundary near and distant representations]]
show original geometry in both representations. EXP-20260911-017 adds these
measurements (original-PC execution at bases `0x00400000`/`0x01400000`):

- **Naive copies sort wrongly.** At world depth 12000 the original primary and
  distant passes emit Z 0.732421875 and 0.57373046875 for the same screen XY,
  so a distant copy of nearby terrain draws in front of it at a 2× range. A
  marker-specific correction gave distant Z 0.8616790771484375, behind the
  nearby draw.
- **Overlap band.** On the test plane, at 11000 only the near mesh emits;
  12000 and 13300 overlap; at 14000, 20000 and 30000 only the distant mesh
  remains after the primary draw stops. This is a bounded plane
  discriminator, not exhaustive transition coverage.
- **Relocation and batching.** The DAT initializer `0x0044BB70` relocated all
  1414 final pointer fields of the extended file. Four synthetic cameras
  produced 9782, 12469, 0 and 5877 vertices, with native auto-flush batches at
  or below 500 vertices (CPU render probes, not GPU benchmarks).
- **Quarter translation.** In 3 of 241 hardware samples the camera translation
  read exactly one quarter of the full value, during `0x0044D83D`'s secondary
  pass; all matrices and Flik positions were identical.
- **Camera override caveat.** A diagnostic hook that pinned the camera
  translation and matrix omitted the derived stored translation `0x005BDB9C`;
  EXP-20260911-018 replaced that fixture with native `0x00455710` at render
  entry. Raw measurements taken under the partial override are observations,
  not a controlled comparison.
