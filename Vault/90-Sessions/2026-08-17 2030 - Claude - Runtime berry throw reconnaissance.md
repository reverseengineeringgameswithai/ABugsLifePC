---
type: session
date: 2026-08-17
agent: Claude
status: partial
tags:
  - session
  - re/runtime
  - research/coverage
---

# Runtime berry throw reconnaissance

## Agent

Claude.

## Goal

Locate the thrown-berry projectile state on PC and identify the variable that
selects berry type (red / blue / green-homing / purple-mega-homing / gold), at
the researcher's direction, using the live Training session they had launched.

## Files inspected

`Vault/00-System/` startup notes; [[Cross-Port Evidence Policy]] before touching
the external PS1 source; [[STRUCT-PC-FLIK-POSITION-GLOBALS]]; the accepted input
census; live memory of PID 57939; `work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.log`.

External, read-only, cited not copied: `SRC-PS1-ABL` at commit
`1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`.

## Experiments inspected

`EXP-20260817-181`/`-184` (input census, for the binding table),
`EXP-20260816-172` (creature pool, to exclude it).

## Changes made

New [[EXP-20260817-187 - Runtime berry throw reconnaissance]];
[[XPORT-20260817-005 - Berry contact array and type marker shape]]; `KU-073`;
entries in [[Current State]], the MOCs, and this index.

No repository code, script, test or asset changed. No `originals/` path touched.
**Live target writes were made** to the running game under explicit in-session
approval; see the outstanding-state note below.

## Conclusions

Two solid results and one honest failure.

The **throw action bit is `0x8000`**, binding the static input model to observed
runtime values for the first time. A **throw-exclusive projectile pool** exists
with stride `0x38`, consistent with 64 records over
`[0x00598C00, 0x00599A00)` — 0 dwords active idle, 0 walking, 38 on throw. It
has no absolute static references, which is why the static censuses never found
it.

The **berry type selector was not found** (`KU-073`).

## New hypotheses

That the stride-`0x38` pool is specifically the berry pool. Throw exclusivity is
strong, but the pool demonstrably holds more than one object class, so this
stays Inferred.

## Contradictions discovered

PS1 reads berry type as a byte at record `+0x2C`; the PC field at `+0x2C` is a
dword that is not the visible colour. Recorded as a cross-port difference in
`XPORT-20260817-005`, not smoothed over.

## Tests run

No repository suite is affected — no code changed. Method checks: injection
verified before trusting any write (1701 samples of `0x8000` from synthetic
presses); the idle/walk/throw discrimination repeated; the `+0x2C` negative
obtained by continuous rewrite over 45s with the researcher observing the screen.

Five memory-diff oracles failed, each for a different reason, and all are
tabulated in the experiment note. The shared cause: no read-only signal
distinguishes berry type, so candidate testing had no ground truth. Two claimed
"results" during the session were withdrawn on inspection — a 25/25 hit rate
that was an artefact of comparing counters, and a candidate set that turned out
to be Flik's Z coordinates.

## Unresolved questions

`KU-073`; the pool's exact base and slot count; the throw handler and spawn code.

## Outstanding state

The tint test left **21 sites** written with `0x00000071` instead of
`0x00710000`; the engine reverted the other 28. The live session was not
restored to pristine state. A relaunch clears it.

Three of the poked candidates were Flik position globals already solved in the
Vault. The Vault should have been checked for known addresses **before** poking,
not after.

## Recommended next action

Either a single hardware write-watchpoint on a pool record during one throw —
which reports the spawning instruction and yields the type dispatch as readable
code — or a researcher-labelled A/B naming the held berry colour before each
sample. The first needs explicit approval under
[[Agent Operating Manual#Dynamic analysis]].

Note that `scripts/game-memory.py` and `scripts/game-session.py` appeared in the
working tree during this session and are the sanctioned tools for this work;
this packet hand-rolled equivalents in the scratchpad because they were not
present when it began.

## Git commit if applicable

One intentional commit covering Vault notes only. Unrelated in-progress work by
another author was present in the tree and was deliberately left uncommitted.
