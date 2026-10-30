---
type: session
date: 2026-08-16
agent: Claude
status: worker-complete
tags: [session, re/static, re/gameplay]
---

# Grain gate level exclusivity

> [!correction] EXP-167 later narrows this packet's authority. The 22
> direct/static references, classification, dispatcher routing, and known
> L3/L4 structures are Confirmed; absence of indirect/aliased/cached gate
> families is Inferred. The historical worker wording below is not live global
> exclusivity evidence.

## Goal

Confirm offline that Tunnels (internal level 3) and City Entrance (internal
level 4) are the only levels with grain gates, and bank it.

## Worker result

[[EXP-20260816-146 - Grain-gate level exclusivity static proof]]. The proof
is exhaustive: every grain gate must read the grain byte `0x0059D9B1`, and
all 22 code references to it were enumerated with radare2 reference analysis
and classified. Only two (`0x00432F0C` in Tunnels `0x00432B30`, `0x004337D6`
in City `0x00433790`) are positional grain-vs-requirement barrier
comparisons; the rest are pickups, Training's 50-grain completion, HUD
counter display, clamps, and level-scripted grain events (level 8
counter-change, level 14 grain-`<40` event) — none a gate.

The 17-level dispatcher `0x00418780` routes only level 3 to `0x00432B30` and
level 4 to `0x00433900 -> 0x00433790`. The gate data structures confirm it:
the Tunnels table `0x004DA9C8`/template `0x004DAA80` are referenced only by
the Tunnels routine/initializer, and the City state array `0x0059F020` only
by City code (its `-1` initializer at `0x00433606` and the gate routine).

## Durable changes

- New: [[EXP-20260816-146 - Grain-gate level exclusivity static proof]] and
  [[PC level roster and numbering]]. The latter's full internal↔progression
  mapping is statically derived from the level-select table at `0x004C6A30`
  (indexed by carousel position `0x00599AF8`, written to `0x00861C84` at
  `0x00414766`), independently re-confirming City Entrance = internal 4
  (position 7) and resolving the 15-vs-17 dispatcher-slot question (training
  = internal17, internal16's identity unresolved at that date).
  **2026-09-11 correction:** index16 is outside the carousel but reached by a special initialization path.
  EXP-20260911-020
  supersedes the former uncertainty about whether it was used.
- Updated: [[PC grain gate requirements]] (Confirmed + Related),
  [[PC autonomous game control]] (progression↔internal-index pointer), and
  the Experiments MOC and this index.

## Next

- Optional independent audit (mechanically reproducible from two radare2
  queries).
