---
type: session
date: 2026-08-16
agent: James
status: reject
tags: [session, milestone/m5, re/audit]
---

# Independent M5.1 hard-truth audit

## Goal

Execute M5.2: fresh-context adversarial audit of the M5.1 type-1 reset
resolver at clean HEAD `2ce8686` (subject `9044e24`).

## Verdict

**REJECT** — [[EXP-20260816-154 - Independent M5.1 hard-truth audit]].

Behavior survives: 264,232-trial differential against an independently written
instruction-level simulator (0 mismatches), the mod-4 argument analytically
plus 200,000 samples, all four runtime receipts and the corpus census
recomputed from primary sources, refusals unbypassable, 24/647 tests,
vault-lint 440/0/0, M4 valid, tracked audit 0, no M4 drift.

Two evidence defects block acceptance: `39,619`/`284,005` in a Confirmed claim
do not reproduce (true `39,316`/`303,653`), and the four-fold "slot retains the
previous level's pointer" claim is uncited and contradicted by the
pointer-table clear at `0x00467207-0x00467215`.

The provenance of the two wrong numbers — that they came from the demoted
descriptor-anchor pass — is **worker-attested, not independently established
here**. James's later attempt to reproduce it from result-1 descriptor base
anchors gives a second-nearest minimum of `285,443`: close to `284,005` but
not equal, and the bounds-centre and min-corner variants do not match at all.

## Boundary

Offline: no game launch, Wine, Gamescope, debugger, breakpoint, or target
write. Nothing committed or staged by the audit; `originals/` untouched; tree
clean at start and end.

## Next

M5.3 corrective packet, then a delta re-audit.
