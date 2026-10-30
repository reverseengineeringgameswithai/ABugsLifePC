---
type: session
date: 2026-08-16
agent: Claude
status: worker-complete
tags: [session, milestone/m5, re/gameplay]
---

# M5 entry gate and type-1 reset resolver

## Goal

Start M5. The milestone had been deferred since the roadmap was written, with
no candidate module ever audited against its entry gate, so starting it meant
running that audit, admitting one module, and implementing it.

## What was done

1. **Entry-gate audit.** Ranked candidates against the six criteria in
   [[Project Roadmap#Module entry gate]]. Selected the type-1 reset-placement
   selector; rejected the `.ANM` format (no bounded contract, `KU-022`) and
   anything on the M2 dependency path (`KU-023` still open).
2. **Contract from the binary.** Disassembled `0x00432930` and its variant
   `0x00437A20` from the hash-verified retail work copy with radare2, plus the
   loader slot writes in `0x0044BB70` and the height-query return path. This
   corrected and extended the prior prose description in three ways: the row
   count is read as an unsigned word, the distance is computed with `sar` in
   row space (not truncating division in world space), and ties go to the
   lowest index. Written up in
   `static/exports/BIN-97c95ba5572dce63/M5-type1-reset-selector-static-trace.md`.
3. **Implementation.** `reimplementation/ablpc/type1_reset.py` models the
   contract bit-exactly on the existing parser and the accepted EXP-141/142
   height model. `scripts/type1-reset.py` is a read-only reporting tool.
   Twenty-four focused tests; full suite 647.
4. **Differential validation** against four retained runtime receipts, plus a
   corpus census and a structural cross-check.
5. Vault updated: [[EXP-20260816-153 - M5 entry gate and type-1 reset placement resolver]],
   [[PC type-1 reset placement resolver]], roadmap M5 activation and the M5.1
   packet, `DEC-20260816-133`, `KU-062`/`KU-063`, both function dossiers, three
   MOCs, and [[Current State]].

## Results worth carrying forward

- Every retained receipt reproduces: both natural EXP-129 pit falls select row
  7 and place `(497248, 31176, 547264)`; the EXP-130 walkable point is an
  exact fixed point at `(501696, 30092, 494016)`; the EXP-116/117 candidate
  row reproduces `+4096`.
- Unplanned agreement: the model reports terrain descriptor 543 at the row-7
  placement, and EXP-129's sampler recorded collision `543/0` right after the
  reset. Independent sources.
- New facts: negative record types alias into the same loader pointer slot and
  a later record overwrites an earlier one; a zero row count reaches an
  uninitialised best-index local, and that is the only path to it; Level03's
  18 rows pair one-to-one with the nine grain gates from EXP-136/139
  immediates.
- EXP-129's quoted squared distances were world-unit values; the engine-exact
  numbers at that contact are 7,010 (row 7) and 16,466 (row 6). Same winner,
  corrected values recorded.

## Boundary

Offline only — no game launch, debugger, breakpoint, target write, asset edit,
or `originals/` access, so there was no runtime instance to audit. M2 stays
deferred; M3/M4/M6 and every M4 authority pin are unchanged (`make
m4-compatibility` passes). The confirmed reset role stays Level03/Tunnels and
type 1 is still not named a respawn or checkpoint table.

## Next

M5.2: a fresh-context hard-truth audit of this packet. Re-derive the contract
from the binary, attack the three refusals and the wrapping/tie/shift
arithmetic, re-run the receipts and census, then accept or reject.
