---
type: session
date: 2026-08-16
agent: Claude
status: worker-complete-pending-independent-audit
tags: [session, re/runtime, re/direct3d, workflow/play]
---

# Auto-hardware Direct3D runtime acceptance

## Goal

Build and runtime-validate the EXP-143 auto-hardware paired transform so the
game boots straight into hardware Direct3D without the manual chooser — the
runtime acceptance packet the candidate note required.

## Worker result

[[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]]. Built a
guarded builder (`reimplementation/ablpc/auto_hardware_mod.py`,
`scripts/make-auto-hardware`, 9 tests) that applies the exact paired code
(`0x000A6C6B`) + relocation (`0x000FA912`) edits, refuses non-retail sources,
applies both atomically, preserves every other byte, and proves exact
inverse; output SHA-256
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.

Two fresh restarts of the patched full-disc copy (retail tree hardlinked,
only the exe replaced) booted straight into hardware Direct3D with **no
chooser input and no visible chooser** — all six START-HERE markers plus
`Device has hardware acceleration`, host NVIDIA RTX 5090, playable
Training-level rendering, reproducible. Retail exe and `originals/` untouched.

## Mutation and lifecycle boundary

Only the derived patched copy was launched; no target-memory write. Wine `Y:`
repointed to the auto-hardware full-disc copy and restored to
`work/copies/BUGS_PC-full-disc`; owned process groups and the private sink
closed; final audit clean.

## Durable changes

- New: [[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]],
  `reimplementation/ablpc/auto_hardware_mod.py`, `scripts/make-auto-hardware`,
  `tests/test_auto_hardware_mod.py`.
- Updated: [[Current State]], the Experiments MOC, this index.
- Held pending James: promoting [[PC automatic Direct3D startup candidate]]
  and updating [[START HERE]].

## Next

- Independent James reject/correct/accept ratchet; on acceptance, promote the
  candidate note and update START HERE, and optionally add an opt-in
  `--auto-hardware` launcher wrapper.
