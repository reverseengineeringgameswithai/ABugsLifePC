---
type: implementation
status: runtime-accepted
created: 2026-08-16
updated: 2026-08-16
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
modified_binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
evidence:
  - EXP-20260816-143
  - EXP-20260816-150
  - EXP-20260816-151
tags:
  - implementation/launcher
  - re/direct3d
  - workflow/play
---

# PC automatic Direct3D startup candidate

## Current status

**Built and runtime-accepted at the derived build-hash boundary.**
`reimplementation/ablpc/auto_hardware_mod.py` + `scripts/make-auto-hardware`
apply the exact transform below; output SHA-256
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
[[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]] launched
the patched copy across two fresh restarts with **no chooser input**: both
reached renderer-level hardware Direct3D (all six [[START HERE]] markers +
`Device has hardware acceleration`), rendered playable gameplay, and showed no
visible chooser; [[EXP-20260816-151 - Independent auto-hardware runtime audit]]
independently **accepts** that at the derived build hash (recording that the
physical-GPU-vs-llvmpipe identity is asserted, not carried by the retained
`bugs.log`, so the accepted boundary is renderer-level hardware Direct3D).

The retail hash retains **no** renderer-selection argument, and the manual
hardware-selection procedure in [[Wine Linux Play Baseline]] remains
authoritative for the retail executable. This transform produces a distinct
build hash; use it only through the guarded builder on a derived copy under
`work/`.

The complete static evidence, rejected shortcut, exact startup control flow,
relocation reasoning, and static James verdict are in
[[EXP-20260816-143 - Automatic Direct3D startup static audit]].

## Exact proposed transform

Source identity:

```text
SHA-256  97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
```

Both edits are mandatory and exactly reversible:

```text
file 0x000A6C6B
  expect: FF D7 2B 05 34 12 7F 00 99
  write:  89 6C 24 10 E9 E2 01 00 00

file 0x000FA912
  expect: 6F 38
  write:  6F 08
```

The first change writes chooser result 2 and jumps from `0x004A786F` to the
original cleanup at `0x004A7A56`. The second converts the PE HIGHLOW
relocation targeting overwritten RVA `0x000A786F` into type-zero padding so
rebasing cannot corrupt the new relative jump.

## Required builder contract

Any future implementation must:

1. refuse every input except the exact source SHA-256 above;
2. refuse unless both original byte sequences match at their exact offsets;
3. read only from a user-owned work copy and write only a new derived copy
   under `work/`; never touch `originals/`;
4. apply both changes as one operation and never emit a one-edit result;
5. verify every output byte outside the two declared spans is unchanged;
6. verify the two new spans, record the output SHA-256, and prove exact inverse
   reconstruction of the source;
7. use create-only output and receipt paths, fail closed on collisions, and
   clean incomplete temporary output;
8. expose any convenience spelling such as `--auto-hardware` as a wrapper
   option, never as a purported native `bugs.exe` parameter;
9. retain `0x0041F990` and the pre-loop portion of `0x004A7600`; do not use
   the rejected whole-chooser bypass.

## Runtime acceptance packet — satisfied

The builder contract above is implemented in
`reimplementation/ablpc/auto_hardware_mod.py` and `scripts/make-auto-hardware`
(nine focused tests, exact inverse). The runtime packet below was satisfied
by [[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]] and
independently accepted by
[[EXP-20260816-151 - Independent auto-hardware runtime audit]] at the derived
build-hash boundary — except that the physical-GPU claim is narrowed to
renderer-level hardware Direct3D (the Gamescope/Vulkan device log was not
retained). The original requirements were:

- explicit `INFO Direct3D - Device has hardware acceleration.`;
- all six renderer markers in [[START HERE]];
- no `SYSTEM MEMORY ONLY`, 320x200, or `INITSOFTRENDER`;
- playable rendering and correct actual-surface behavior;
- no visibly rendered chooser, with only a brief display-mode blank/flash
  permitted;
- expected `Examining Machine` and later loading windows;
- complete process, Wine-server, Gamescope, and audio-sink cleanup;
- host GPU rather than llvmpipe when physical GPU acceleration is part of the
  claim.

The James ratchet is satisfied (EXP-151 ACCEPT). The opt-in
`--auto-hardware` wrapper is now implemented on `scripts/play-pristine.sh`
(it builds/reuses the cached patched copy and runs it; retail assets and `Y:`
unchanged; four dry-run tests cover the wiring). It is never a native
`bugs.exe` argument. Changing the *default* launcher to auto-hardware remains
a separate decision, and if physical-GPU proof is later needed, retain the
Gamescope/Vulkan device log.
