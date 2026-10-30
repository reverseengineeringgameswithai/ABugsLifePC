---
type: experiment
id: EXP-20260816-150
date: 2026-08-16
question: Does the EXP-143 auto-hardware paired transform, built and launched, boot the game straight into hardware Direct3D across fresh restarts without the manual chooser?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
modified_binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
environment: Fedora Linux 44; Wine 11 Staging; Gamescope 3.16.25; NVIDIA RTX 5090; Direct3D 640x480x16
configuration: auto-hardware patched full-disc copy; no renderer-selection input sent; two fresh restarts
working_directory: /home/dev/ABLPC
artifacts:
  - reimplementation/ablpc/auto_hardware_mod.py
  - scripts/make-auto-hardware
  - tests/test_auto_hardware_mod.py
  - work/copies/EXP-20260816-144-gate-mapping/evidence/auto-hardware/
addresses:
  - "0x004A786B"
  - "0x004A7A56"
file_offsets:
  - "0x000A6C6B"
  - "0x000FA912"
result: auto-hardware-transform-built-and-runtime-accepted-across-two-fresh-restarts
status: completed
created: 2026-08-16T14:20:00
updated: 2026-08-16T14:20:00
tags:
  - re/experiment
  - re/runtime
  - re/direct3d
  - workflow/play
---

# EXP-20260816-150 - Automatic Direct3D startup runtime acceptance

## Question

[[EXP-20260816-143 - Automatic Direct3D startup static audit]] designed a
hash-locked paired code-plus-relocation transform that auto-confirms Direct3D
and skips only the chooser's interactive loop, accepted by James **only as a
static candidate pending runtime validation**
([[PC automatic Direct3D startup candidate]]). Does the built transform, when
launched, boot straight into hardware Direct3D without the manual chooser,
reproducibly?

## Builder

`reimplementation/ablpc/auto_hardware_mod.py` and `scripts/make-auto-hardware`
apply the exact transform to a derived retail copy:

- code at file `0x000A6C6B` (VA `0x004A786B`):
  `FF D7 2B 05 34 12 7F 00 99` -> `89 6C 24 10 E9 E2 01 00 00`
  (`mov [esp+0x10], ebp` with `ebp==2`, then `jmp 0x004A7A56` cleanup);
- relocation at file `0x000FA912`: `6F 38` -> `6F 08` (HIGHLOW -> type-zero).

The builder refuses any non-retail source SHA-256, refuses unless both
original byte sequences match, applies both edits atomically (never a
one-edit output), preserves every other byte, records the output SHA-256
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`, and
proves exact inverse reconstruction of retail. Nine focused tests pass
(constants, synthetic apply/preserve/inverse, wrong-SHA and wrong-byte and
missing-reloc refusals, retail hash pin, retail inverse). Exactly 9 bytes
differ (8 code + 1 relocation), size unchanged.

The auto-hardware full-disc copy was made by hardlink-copying the retail
tree and replacing only `PC/BUGS/bugs.exe` with the patched build; the retail
executable remains `97c95ba5...27b878` and `originals/` was not touched.

## Runtime arms (no chooser input sent)

Two fresh Gamescope/Wine restarts of the patched copy, with Wine `Y:`
repointed to the auto-hardware full-disc copy and restored to retail
afterward. **No Down/Return/renderer-selection input was sent in either arm.**

Both arms' logs contain all six [[START HERE]] hardware markers plus
`INFO Direct3D - Device has hardware acceleration.`, and neither contains
`SYSTEM MEMORY ONLY`, `INITSOFTRENDER`, or a 320x200 selected surface:

```
INFO Direct3D - Device has hardware acceleration.
INFO Native software render mode is FALSE.
INFO RenderMode set to Direct3d render mode.
INFO Screen mode 640x480x16 selected.
SYSTEM : OnlySystemMemory status VIDEO MEMORY ONLY.
D3DAPPCREATE : Mode set to 640x480.
INIT : Starting Direct3D renderer.
```

- **No visible chooser:** within a few seconds of launch (no input), both
  arms rendered the "fliks journey" level-select carousel crisp at full
  640x480 (`ah1-t1.png`, `ah2-early.png`) — the software renderer's 320x200
  corner surface never appeared. Only a brief display-mode blank precedes it.
- **Playable rendering:** arm 1 loaded the Training level, which rendered at
  full 640x480 hardware (`ah1-gameplay.png`).
- **Host GPU (observed, not retained):** the live Gamescope startup output
  named physical device `NVIDIA GeForce RTX 5090` (not llvmpipe), but that
  Gamescope/Vulkan log was not saved; the retained `bugs.log` evidence
  establishes hardware Direct3D at the game-renderer level (the six markers +
  `Device has hardware acceleration`, which reflects wined3d device caps), not
  the physical GPU. The accepted boundary is renderer-level hardware Direct3D.
- **Reproducible:** identical marker set across the two fresh restarts.

Evidence and both full logs are retained under
`work/copies/EXP-20260816-144-gate-mapping/evidence/auto-hardware/`.

## Result

The auto-hardware transform is **built and runtime-accepted at this
boundary**: it boots straight into renderer-level hardware Direct3D across
two fresh restarts with no chooser input and no visible chooser, and renders
playable gameplay, while preserving retail identity and exact reversibility.
(Physical-GPU vs host-software-renderer identity was observed live but not
retained; it is outside the accepted boundary.)
This is the runtime acceptance packet the candidate note required. The manual
procedure and full log gate remain authoritative for the retail hash;
this transform produces a distinct build hash.

## Mutation and lifecycle boundary

Only the derived patched copy was launched; no target-memory write,
debugger, or asset/`originals/` mutation. Wine `Y:` was repointed to the
auto-hardware full-disc copy and restored to `work/copies/BUGS_PC-full-disc`;
owned process groups and the private sink were closed; the final audit was
clean.

## Follow-up

- Independent James reject/correct/accept ratchet, then promote
  [[PC automatic Direct3D startup candidate]] from `proposed-static` and
  update the [[START HERE]] "automatic selection is not implemented" note.
- Optional: expose `--auto-hardware` as an opt-in wrapper option on the
  launcher (never a native `bugs.exe` argument).
