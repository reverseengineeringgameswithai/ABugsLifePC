---
type: implementation
status: active
created: 2026-08-15
updated: 2026-08-15
tags:
  - implementation/modding
  - milestone/m3
  - gameplay/collectibles
  - gameplay/hud
---

# Training FLIKFLIK HUD and completion

## Outcome

[[EXP-20260815-114 - Training FLIKFLIK HUD and completion]] accepts one exact
PC Training vertical slice that composes the M3.2 `51/50` executable with the
M3.3 eight-letter DAT. The eight pickups own independent bits, completion is
one-shot on the incomplete-to-`0xFF` transition, and both the in-level HUD and
level-complete tally render centered `FLIKFLIK`. The tally reports `8/8` and
reuses the original FLIK emblem without changing its artwork.

This is an exact eight-slot `FLIKFLIK` design, not a general arbitrary-word
engine. Other words, lengths, levels, glyph families, persistence rules, and
new emblem art remain outside the accepted boundary.

## Asset-free implementation

- `reimplementation/ablpc/training_flikflik_mod.py` composes the accepted
  M3.2 counter patch, applies 29 exact spans, verifies the final hash, and
  reconstructs both the M3.2 intermediate and retail executable exactly.
- `scripts/make-training-flikflik` accepts only the retail executable below
  `work/copies/`, refuses overwrite and linked outputs, preserves executable
  mode, and writes a deterministic JSON receipt.
- `tests/test_training_flikflik_mod.py` pins the authored code identity,
  redirects, one-shot scratch operands, complete 256-byte popcount table,
  tally denominator/emblem layout, exact inversion, unknown-byte preservation,
  and refusal paths.

The public output is 1,069,056 bytes at SHA-256
`b572e6d19bc417969c159ba0df7521cbb01b675c260a4dc98d2e6b34475947f4`.
The 576-byte authored packet is SHA-256
`0d32f7fadf1dd7ccbfaba8689e9bb3a95278fcc7e6ab161084359e5eb27f8370`
at VA `0x004BBA00` / file offset `0x0BAE00`, inside original `.text`
`0xCC` linker padding. No PE header or section changes are made.

## State and completion boundary

The original four selector cases still enter at `0x00417A59`, `0x00417AB3`,
`0x00417B3B`, and `0x00417BC3`. The helper distinguishes original record
indices 50–53 from appended indices 63–66 and assigns bits
`1/2/4/8/16/32/64/128` in byte `0x0059D9B2`.

Each pickup clears scratch byte `0x0086396F`, sets it only when a prior
incomplete mask becomes `0xFF`, and leaves it zero if the prior mask was
already complete. The four retained reward gates compare that scratch with
one. The address is the final byte of the original writable `.data` virtual
extent, is zero-initialized outside raw file data, and has no direct reference
in the retail image. The four absolute operands retain existing HIGHLOW
relocations.

## HUD and tally boundary

The in-level helper draws eight slots at x positions
`64, 88, 112, 136, 160, 184, 208, 232`, centered on x=148 as a group. The
tally helper uses x positions `66, 90, 112, 132, 160, 184, 206, 226`, centered
on x=146, retains the retail animation phase, and cycles exact glyph IDs
`0x10`–`0x13` as `FLIKFLIK`.

All four tally count reads use an embedded complete byte-popcount table at
`0x004BBB40`; their existing HIGHLOW relocations are preserved. The displayed
denominator and emblem gate are eight. The count moves above the word and the
existing emblem moves to x=0/y=`0x50`, leaving the centered word unobscured.

## Usage

```bash
./scripts/make-training-flikflik \
  work/copies/BUGS_PC-disc/bugs.exe \
  work/copies/training-flikflik-bugs.exe
```

Stage that generated executable and the accepted M3.3 Training DAT into a
fresh complete ignored `DRIVE:\PC\BUGS` tree. Do not distribute either
generated game file or source content.

This exact M3 recipe does not modify the completed M4/M6 compatibility
authorities.
