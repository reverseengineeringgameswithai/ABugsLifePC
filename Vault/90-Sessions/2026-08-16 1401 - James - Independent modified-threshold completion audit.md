---
type: session
date: 2026-08-16
agent: James
status: accepted
tags: [session, re/audit, re/runtime, re/gameplay]
---

# Independent modified-threshold completion audit

## Goal

Adversarially audit the committed
[[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]]
packet from a fresh context, without launching the game (the live session
needs a Gamescope/Wine launch with focus handling and would mean more target
writes). Judge whether each claim is supported by its cited evidence: the
per-gate configured minimums, the gate-open semantics against the
disassembly, the rows-0/4 coupling, the disclosed row-1 gap, the write
boundary, the focus-pause finding, the retained screenshots, and hygiene.

## Work completed

- Re-read [[START HERE]], the Current State "2026-08-16 KU-060" section, the
  packet, EXP-136/137/139, KU-060, [[PC grain gate threshold mod]],
  [[PC autonomous game control]], and [[PC Flik teleport procedure]].
- Rehashed both binaries (modified `69881871...de284b`, retail
  `97c95ba5...27b878`). Read the modified build's nine Tunnels requirement
  dwords at `0x004DA9C8` (rows 0-8 = `1..9`, type `0x10C7`, EXP-136
  `unknown_04`/X/Z) and the three City lookup dwords at `0x004338B0`
  (`1,2,3`).
- Disassembled the Tunnels open branch in `0x00432B30` (`mov edi,0x1068`;
  `cmp 0x10C7`; grain load `0x0059D9B1`; decay `cmp 0x708`/`add -140` to
  `0x0690`), both coupling cross-writes (`0x00432F85` row0->row4 at
  `0x004DAA18`, `0x00432F9D` row4->row0 at `0x004DA9C8`), and the City routine
  `0x00433790` (state `-1` gate at `0x00433798`, decrement at `0x0043384A`,
  animation accumulate at `0x0059F030`). Decoded the three City call-site slot
  immediates in `0x00433900`: gate0->2/3, gate1->4/5, gate2->0/1.
- Read `gate_probe.c` (snapshot reads-only; teleport writes one 24-byte
  current+preceding guarded by level; write_grain writes one byte at
  `0x0059D9B1` guarded by level + expected-old). Visually inspected the five
  640x480 PNGs.
- Ran hygiene gates: clean HEAD `35eef49`, Vault-only commit, `originals/`
  untouched, PNGs/helper git-ignored, `make check` (Vault 428/0/0, 610 tests,
  tracked audit 0, `git diff --check` clean).

## Verdict

**ACCEPT**, recorded in
[[EXP-20260816-149 - Independent modified-threshold completion audit]]. All
nine checks pass. Key confirmations:

- The modified build's Tunnels requirements are exactly `1..9` and the City
  lookup exactly `1,2,3`, matching the packet and EXP-136.
- The open semantics match the disassembly: Tunnels sets `0x1068` decaying to
  `0x0690`; City state `-1 -> 0` with `0x0059F030` animation; slots agree with
  EXP-139 and the packet's gate 1 -> 4/5, gate 2 -> 0/1 (settled values =
  deltas x 32-update countdown).
- The rows-0/4 coupling is an unconditional cross-write; row 0's standoff is
  ~600k units from row 4's center, so grain 1 opening row 4 is the coupling,
  and the packet correctly declines to claim row 4's independent threshold.
- The row-1 gap ("opens above requirement; exact one-below not isolated") is
  disclosed in the table, Result, KU-060, and Current State — not hidden;
  acceptable as a residual, since row 1's mechanism is byte-identical to the
  seven confirmed rows.
- The write boundary is exactly a 24-byte teleport plus a guarded one-byte
  grain write; the focus-pause is framed as an observation, not code-proven;
  the five screenshots are real hardware frames whose grain HUD matches each
  condition.

No defect found; no claim outruns its evidence.

## Next steps

- Worker reconciles Current State and Known Unknowns after this verdict (they
  already reflect the packet at HEAD `35eef49`) and keeps M3 Complete.
- The only KU-060 residual is an optional isolated clean one-below pass for
  Tunnels row 1 (identical mechanism to the seven confirmed rows).
