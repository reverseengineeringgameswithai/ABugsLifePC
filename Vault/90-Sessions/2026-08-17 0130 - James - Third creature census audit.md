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

# Third creature census audit

## Agent

James, fresh context.

## Goal

Try to break the twice-corrected creature census at clean HEAD `3f0debd`,
re-deriving each prior correction rather than assuming it, and probing the
ground both earlier audits declared unchecked.

## Files inspected

The census export, all three experiment notes, the five function dossiers, the
coverage map, the MOCs, `KU-065`/`KU-068`/`KU-069`, Current State, the roadmap
and both session notes. Every file in
`static/exports/BIN-97c95ba5572dce63/` was grepped for the packet's principal
addresses — **including the generated `ghidra-evidence.json`**. Binary:
`work/copies/BUGS_PC-full-disc/bugs.exe`.

## Changes made

None by the auditor — read-only, nothing committed. Findings applied afterwards
in the commit recording
[[EXP-20260817-175 - Third independent creature census audit]].

## Conclusions

**REJECT.** The numeric analysis reproduced in full for the third time, and the
auditor ran the published §6.1 reproduction snippet verbatim to confirm it.

Three Confirmed-level statements were contradicted by the bytes: the function
extent (`0x0041DC60` continues to `0x0041E845` past its only `ret`), the
`+0x70` writer count (four, not three — `0x0041E7FE` was missed because the
sweep stopped at the wrong extent), and the flag table's completeness over its
own scope (a bit-`0x20` test at `0x0041BD6C` inside `0x0041BD10`).

The novelty boundary failed a third time, and decisively:
`ghidra-evidence.json` — generated, 8 MB, in the same directory since the
earliest baseline — already decompiles the whole interpreter including its
26-way dispatch and the indirect call through record `+0x7C`. The prior-art
list also named a file containing no occurrence of the pool base and omitted
one publishing §1.1's arithmetic verbatim.

## New hypotheses

None.

## Contradictions discovered

None with accepted prior work.

## Tests run

`make vault-lint` 492/0/0; `make audit-tracked` 0 violations; `make test` 686
passed, single invocation, qualified by open `KU-065`.

## Unresolved questions

The interpreter region past `0x0041E1A8`, the ten `+0x7C` handlers, the nine
opcode-11 subroutines, `KU-068`, and `KU-069`.

## Recommended next action

Apply the findings, withdraw the address-based novelty framing in favour of
what the packet actually contributes, and re-audit from a fresh context.

## Git commit if applicable

None by the auditor.
