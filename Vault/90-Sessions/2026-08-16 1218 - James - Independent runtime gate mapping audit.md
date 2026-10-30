---
type: session
date: 2026-08-16
agent: James
status: rejected-then-accepted-after-correction
tags: [session, re/audit, re/runtime, re/gameplay]
---

# Independent runtime gate mapping audit

## Goal

Adversarially audit the committed EXP-144 runtime grain-gate visual-mapping
packet from a fresh context, without reproducing the live session (nested
Gamescope crashes; re-teleporting means more target writes). Judge whether
each claim is supported by its cited evidence: standoff agreement with
EXP-141, engine-exact nearest-gate distances, the retained screenshots, the
control-recipe disassembly, the carousel framing, the write boundary, and
hygiene.

## Work completed

- Re-read the startup authority chain, the Current State runtime-mapping
  section, the packet, [[PC autonomous game control]], EXP-136/138/139/141,
  [[PC grain gate threshold mod]], [[PC Flik teleport procedure]],
  [[Wine Linux Play Baseline]], and KU-060.
- Ran `scripts/grain-gate-standoffs.py --compact`; matched all twelve
  chosen standoffs to the EXP-144 tables and to EXP-141 candidates / the
  T3 and C0 proven points.
- Recomputed every stated Tunnels and City distance in Python under both
  `sar` (`>>`) and truncation semantics; confirmed the nearest gate is the
  minimum for each standoff.
- Rehashed `bugs.exe` (`97c95ba5...27b878`); disassembled the chooser and
  confirmed `GetAsyncKeyState` load at `0x004A7841`, the VK_DOWN/UP/
  RETURN/SPACE polls, and `cmp dword [0x7f1170], 0xea60` at `0x004A797A`.
- Read `gate_probe.c` (writes only 24-byte current+preceding; computes the
  Tunnels distance with `sar`; computes no City distance); visually
  inspected the retained 640x480 PNGs (T0/T3/T6/T8, C0/C1/C2, briefing).
- Ran hygiene gates: clean HEAD `6dd9b12`, Vault-only commit, `originals/`
  untouched, PNGs/helper git-ignored, `make check` (Vault 419/0/0, 610
  tests, tracked audit 0).

## Verdict

**REJECT**, recorded in
[[EXP-20260816-145 - Independent runtime gate mapping audit]]. Sole cause:
the City "nearest dist²" for gate 0 (`4160`) and gate 1 (`9025`) are
computed with truncation-toward-zero, not the engine `sar`-8 helper
`0x00416580` the packet cites. Correct engine values are `4289`/`3482`
(gate 0) and `9216` (gate 1); gate 0's `4160` also silently contradicts
EXP-139's accepted `4289`. The City dist² column is additionally
reference-position-inconsistent (gate 2's `10952` is standoff-based, not
from the settled-current column shown beside it). No inside/outside
verdict, nearest-gate identity, or correlation conclusion changes.

Every other claim verified: standoff agreement, all nine Tunnels distances
(`sar`-correct), the inside/outside verdicts, the screenshots (real,
hardware-resolution, not overclaimed), the control-recipe disassembly, the
carousel-vs-internal-level framing, the write-assisted 24-byte boundary,
M3 Complete, KU-060's open receipts, and hygiene.

**Correction confirmed (post-verdict).** The worker recomputed the City
table with the engine `sar`-8 helper `0x00416580` from a consistent
settled-current reference: gate 0 `3482` (inside 6400), gate 1 `9216`
(just outside 8100), gate 2 `11885` (just outside 10000) — matching my
independently computed values, with the caption now stating the reference
and predicate and citing EXP-145. The sole defect is resolved; **verdict
upgraded to ACCEPT**. The worker reconciles Current State/KU-060 and
commits.

## Next steps

- Worker recomputes City gate 0/1 distances with the engine `sar`
  (`4289`/`3482` and `9216`), states the City dist² reference position
  consistently, then reconciles Current State and Known Unknowns and
  resubmits.
- The physical modified-threshold receipts for the untested gates (City
  1/2, Tunnels rows other than 3) remain the open part of KU-060.
