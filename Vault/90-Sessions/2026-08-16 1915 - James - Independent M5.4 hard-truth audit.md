---
type: session
date: 2026-08-16
agent: James
status: reject
tags: [session, milestone/m5, re/audit]
---

# Independent M5.4 hard-truth audit

## Verdict

**REJECT** narrowly — [[EXP-20260816-157 - Independent M5.4 hard-truth audit]].

Survives: pre-registration integrity (`git diff a58f962 b861376` touches only
frontmatter and appends below the rule), the independently re-derived
prediction, the proof that `31768` requires the composed terrain model, the
unambiguous aux transition at 6.2 ms, the three-writes-per-arm boundary, the
lifecycle, and the gate-4 scoping.

Defects: a "7 seconds" no-loop window unsupported by the retained trace (which
ends at 2.47 s), and a settle band widened in the Vault but left contradicted
by the shipped tool, whose emitted band excluded the accepted receipt.

## Boundary

Offline: nothing run, no debugger, no target write, nothing committed or
modified; tree clean at `b861376`.

## Next

M5.5 correction, then a delta re-audit.
