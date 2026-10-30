---
type: session
date: 2026-08-17
agent: James
status: reject-corrected
tags:
  - session
  - re/audit
  - research/coverage
---

# Fourth creature census audit

## Agent

James, fresh context.

## Goal

Try to break the three-times-corrected creature census at clean HEAD
`1c499bf`, re-deriving each prior correction rather than assuming it, checking
whether `0x0041E845` is really the function's end, and checking every quoted
disassembly block.

## Files inspected

The census export, all four experiment notes, the five function dossiers, the
three MOCs, `KU-065`/`KU-068`/`KU-069`, Current State, the roadmap and the
session notes. Every file in `static/exports/BIN-97c95ba5572dce63/` was
grepped for the pool base, and `ghidra-evidence.json`'s decompilation of
`FUN_0041dc60` was read. Binary: `work/copies/BUGS_PC-full-disc/bugs.exe`.

## Changes made

None by the auditor — read-only, nothing committed. Findings applied afterwards
in the commit recording
[[EXP-20260817-176 - Fourth independent creature census audit]].

## Conclusions

**REJECT**, on the accounting layer alone. The numeric core reproduced a
fourth time; the extent `0x0041DC60`-`0x0041E845` was confirmed with nothing
extending further; the four `+0x70` writers are exactly four; the flag
enumeration is complete and correct; the nine-artifact prior-art list and every
quoted attribution check out; and, for the first time, all six quoted
disassembly blocks match objdump byte for byte.

Nine defects remained, all arithmetic, counting or attribution: a wrong
percentage, an unreproducible "thirteen sites", the third draft's errors
attributed to the second, an understatement of the generated Ghidra export in
the direction that flatters the packet, a two-of-four enumeration of the mode
slot's readers, stale "64-entry" text in two artifacts, a superseded extent
asserted as fact in an audit note, a self-contradictory sentence naming a
non-existent `ret`, and a three-of-at-least-four record-index count.

## New hypotheses

None.

## Contradictions discovered

Several internal to the packet — §0 against §0.1 on draft attribution, §0.1
against §10 on how much was read, §5.3 against §5.1 on the mode slot — all
recorded and fixed.

## Tests run

`make vault-lint` 494/0/0; `make audit-tracked` 0 violations; `make test` 686
passed, single invocation, qualified by open `KU-065`.

## Unresolved questions

The interpreter region past `0x0041E1A8`, the ten `+0x7C` handlers, the nine
opcode-11 subroutines, `KU-068`, and `KU-069`.

## Recommended next action

Apply the findings — replacing derived percentages and aggregate counts with
enumerations wherever possible — and re-audit from a fresh context.

## Git commit if applicable

None by the auditor.
