---
type: implementation
status: m5-independently-accepted
created: 2026-08-16
updated: 2026-10-02
tags: [implementation, re/gameplay, milestone/m5]
---

# PC grain gate opening resolver

`reimplementation/ablpc/grain_gate_resolver.py` is the M5.7 worker
implementation of the second module admitted by
[[EXP-20260816-169 - Independent M5.6.1 delta audits]]. It evaluates gate
opening decisions offline from explicit state; it never reads a game asset,
launches a target, or writes executable/target state. The read-only reporting
surface is `scripts/grain-gate-resolver.py`.

The first fresh-context M5.8 audit rejected exact
commit `efad1c255dcfda31e225c7fdf62608bc59f63e5a` only because the reporting
CLI accepted duplicate JSON member names despite claiming strict JSON. The
bounded correction rejects duplicates at every object nesting level; all
resolver arithmetic, ordering, write, downstream, receipt, and scope claims
survived unchanged. A wholly new path-bounded James verifier then returned
**ACCEPT** for exact correction commit
`dfd3af31c845939aa972babfd0f44a60e54b6487`, tree
`8b7d4234e3a517ed63032bd2d9c9ab8770801714`. The implementation boundary and
validation are recorded in
[[EXP-20260816-170 - M5.7 grain-gate opening resolver]] and the independent
verdict in [[EXP-20260816-171 - Independent M5.8 grain-gate resolver audits]].

## Exact boundary

| Family | Native decision | Resolver output |
| --- | --- | --- |
| Tunnels / internal 3 | ordered nine-row loop `0x00432EEA-0x00433043`; closed type `0x10C7`; grain first at `0x00432F0C-0x00432F14`; signed proximity at `0x00432F33-0x00432F4F` | one decision per row in native order; direct type `0x1068` writes and row-0/4 coupling; private post-direct-write records; downstream decay metadata |
| City Entrance / internal 4 | state `-1` at `0x00433798`; helper `0x00416580`; grain at `0x004337D6-0x004337E3` | one decision; direct state `0x20`; index-0-only `write_u8(0x00599C69, 1)`; downstream state/slot rule metadata |

Inputs are signed int32 Flik X/Z, unsigned byte grain, supported authored
requirement `0..50`, current state, and exact center/radius data. Tunnels
requires all nine ordered 20-byte records and preserves address-named unknown
`+0x04`. City requires gate index plus both animation slots/deltas.

The arithmetic is the low signed 32 bits after each `sub`, `imul`, and `add`,
with arithmetic `sar 8` before the products and a final signed `<` comparison.
This matters even for synthetic overflow cases; Python's unbounded integer
arithmetic is never used as a silent substitute. Static derivation is retained
in
`static/exports/BIN-97c95ba5572dce63/M5-grain-gate-resolver-static-trace.md`
against exact retail SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

## Evaluation order and refusals

The explicit refusal is the first native opening predicate that fails:

- Tunnels: already non-closed → insufficient grain → outside proximity.
  Insufficient grain has no opening-distance result because the native opening
  arm does not compute that distance before branching (`0x00432F14`).
- City: already non-closed → outside proximity → insufficient grain. City
  calls `0x00416580` before loading/comparing grain (`0x004337C5-0x004337E3`).

Tunnels is deliberately a whole ordered nine-row evaluation. If row 0 opens,
its own direct write at `0x00432F6A` precedes the row-4 coupling write at
`0x00432F85`; row 4 later observes type `0x1068` and refuses as already
non-closed. If row 4 opens after row 0 has failed, its own write precedes the
reverse coupling at `0x00432F9D`; row 0's earlier decision does not change.
The result distinguishes independently eligible rows from rows changed only
by coupling. It also reports row 4 as entering the downstream decay path later
in the same pass after row-0 coupling; the reverse row-4 coupling reaches row 0
only after row 0's visit, so no same-pass decay is attached to that write.

## Downstream metadata is not executed

Tunnels reports signed `type > 0x708` then wrapping `type += -140` from
`0x00433017-0x00433024`. City reports positive-state decrement plus the two
wrapping slot deltas at `0x0043383B-0x00433879`; the first of 32 steps occurs
in the same call that writes state `0x20`. The zero-based 32-step aggregates
are:

| City index | Slots | Per-step deltas | Aggregate deltas |
| ---: | --- | --- | --- |
| 0 | 2 / 3 | `-32 / +32` | `-1024 / +1024` |
| 1 | 4 / 5 | `+44 / -34` | `+1408 / -1088` |
| 2 | 0 / 1 | `-28 / +32` | `-896 / +1024` |

These rules explain EXP-137/148 terminal receipts. The resolver returns the
metadata but does not run animation, rendering, messages/audio, opening-helper
side effects, control, save persistence, or other per-frame update logic.

## Asset-free reporting

The reporting tool accepts one strict JSON request from a named file or stdin
and prints deterministic JSON. Duplicate member names at the request or any
nested-object level fail with exit 2, empty stdout, and a deterministic error;
the first M5.8 audit caught and rejected the previous last-value-wins parser.
Tunnels requests contain nine records; City
requests contain one complete call-site descriptor. Unknown or missing keys,
wrong internal levels, non-int32 values, grain outside `0..255`, requirements
outside `0..50`, and invalid gate/slot indices fail closed.

```bash
.venv/bin/python scripts/grain-gate-resolver.py request.json
.venv/bin/python scripts/grain-gate-resolver.py - < request.json
```

The report states that it does not execute downstream rules, write files or
target state, claim global family exclusivity, or assign semantics to
`0x00599C69`.

The correction is covered by 38 resolver tests and a 64/64 focused combined
run. One directly retained canonical gate reports 686/686, Vault 482/0/0, and
tracked audit 0 (raw-log SHA-256
`617e71f15af9f3697bcb3e79a4974324aebc219f00152fef90fd1844caf0adb5`).
The suite observation remains explicitly qualified by open KU-065. (KU-065
was resolved for its identified test node on 2026-08-17, a race in
`tests/test_input_movie.py`; the four original camera-packet failures stay
open. See [[Known Unknowns]].)
James's independent acceptance gate is likewise a qualified 686/686, raw-log
SHA-256
`b1e9a4737585160dd7037b79bcc9511b198904f4c2b2302a1456403348bc713f`.

## Receipt coverage and limits

Asset-free tests reproduce:

- the EXP-139 distances `4993`, `4289`, and `7177`;
- exact min-1/min outcomes for Tunnels rows 0,2,3,5,6,7,8 and City indices
  0,1,2 from EXP-137/138/148/149;
- row 1 only at its accepted “opens above minimum” boundary; and
- row 4 only through the accepted row-0 coupling receipt.

No test invents the absent row-1 exact min-1 runtime pair or an independently
separable row-4 threshold. The evaluator models the native code for those
inputs, while the evidence status of those two original-runtime observations
remains narrower.

This module covers twelve confirmed mechanisms, not every possible grain
consumer or a general trigger system. EXP-146 established 22 direct/static
references and two known positional gate families; global absence of
indirect/cached families remains Inferred. The meaning, readers, and lifetime
of `0x00599C69` remain Unknown in KU-067.

Related: [[PC grain gate requirements]], [[PC grain gate threshold mod]],
[[Python and C reverse-engineering split]],
[[EXP-20260816-166 - M5 second-module entry-gate audit]], and
[[EXP-20260816-168 - M5.6.1 claim and contract correction]].
