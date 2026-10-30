---
type: session
date: 2026-08-16
agent: James
status: accepted
tags: [session, re/audit, re/runtime, re/direct3d]
---

# Independent auto-hardware runtime audit

## Goal

Adversarially audit the committed
[[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]] packet
from a fresh context — the fresh James ratchet
[[PC automatic Direct3D startup candidate]] requires before promotion.
Independently reproduce the transform build and disassembly; do **not** relaunch
the game (expensive Gamescope/Wine launch); judge the two retained logs and
three screenshots as the runtime evidence.

## Work completed

- Re-read [[START HERE]], the packet EXP-150, the design
  [[EXP-20260816-143 - Automatic Direct3D startup static audit]],
  [[PC automatic Direct3D startup candidate]], and [[Wine Linux Play Baseline]].
- Rehashed retail `97c95ba5...27b878` (1,069,056 bytes); read the raw bytes at
  file `0x000A6C6B` (`ff d7 2b 05 34 12 7f 00 99`) and `0x000FA912` (`6f 38`).
- Ran the guarded builder on the retail bytes: output `1e1d5099...c41f`, size
  unchanged, an independent byte diff of exactly nine changed offsets (all
  inside the two spans), and exact inverse back to retail. Reviewed
  `auto_hardware_mod.py` (source-SHA refusal first, per-span expected checks,
  atomic both-edit apply with no one-edit path, span-confined changes, proven
  inverse) and `make-auto-hardware` (no-symlink, `work/`-only, create-only,
  distinct paths). `pytest tests/test_auto_hardware_mod.py -q` = 9 passed.
- Disassembled a built copy (capstone 5.0.7, cross-read as bytes): confirmed
  `mov ebp,2` at `0x004A7866`, `mov [esp+0x10],ebp`, `jmp 0x004A7A56`
  (displacement `0x1E2`), and that `0x004A7A56` is the real cleanup (reloads
  `[esp+0x10]`, releases surface globals `0x861ca0..0x861cb8` via `call
  0x4b0270`, COM vtable calls). Parsed the `.reloc` block (PageRVA `0xA7000`):
  entry `0x386F` HIGHLOW → `0x086F` type-0, offset `0x86F` preserved, target
  RVA `0xA786F`, neighbors non-overlapping. Confirmed it enters after
  `0x004A7866` inside `0x004A7600` — not the rejected WinMain whole-chooser
  bypass.
- Grepped both retained logs (`ah1-bugs.log`, `ah2-bugs.log`): all six START
  HERE markers + `Device has hardware acceleration` in each; zero
  `SYSTEM MEMORY ONLY`/`INITSOFTRENDER`; `320x200` only in DDMODE enumeration
  (the sole selected screen mode is `640x480x16`); final-path markers after
  `SwitchDriverScreen`. Viewed the three PNGs: `ah1-t1`/`ah2-early` = full-frame
  carousel, no chooser; `ah1-gameplay` = full-frame Training level.
- Hygiene/lifecycle: clean HEAD `cfd06ed`; commit adds only tool/test + Vault
  files (no game bytes); patched copy + evidence git-ignored; `originals/`
  clean; `Y:` restored to `work/copies/BUGS_PC-full-disc`; candidate note still
  `proposed-static` and START HERE "not implemented" line unchanged (neither in
  the commit). `make check` = Vault 432/0/0, 619 tests, tracked audit 0.

## Verdict

**ACCEPT**, bounded to the derived build hash `1e1d5099...c41f`, recorded in
[[EXP-20260816-151 - Independent auto-hardware runtime audit]]. All six checks
pass. One honest narrowing: the specific host-GPU device identity (`RTX 5090`,
not llvmpipe) is asserted but **not** carried by the two retained `bugs.log`
files — `Device has hardware acceleration` reflects wined3d device caps and does
not by itself distinguish a physical GPU from llvmpipe, and no Gamescope/Vulkan
device log was retained. The accepted boundary is therefore hardware Direct3D at
the game-renderer level (all six markers), not a proof of the physical GPU from
this evidence. No claim otherwise outruns its evidence; the build, disassembly,
relocation, reversibility, no-visible-chooser, playable rendering, integrity,
and no-premature-promotion checks all hold.

## Next steps

- Worker may now promote [[PC automatic Direct3D startup candidate]] from
  `proposed-static` and update the [[START HERE]] "automatic selection is not
  implemented" line, scoped to the derived build hash, keeping the manual
  procedure and full-log gate authoritative for the retail hash.
- If the host-GPU (RTX 5090 vs llvmpipe) distinction is to be claimed, retain a
  Gamescope/Vulkan device log alongside the game log in a future arm.
