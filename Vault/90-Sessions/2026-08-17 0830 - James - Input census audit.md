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

# Input census audit

## Agent

James, fresh context, first audit of this packet.

## Goal

Try to break the input census at clean HEAD `67ca1b5`, with particular
attention to the identifier decodings, both function extents, and whether the
author's stated countermeasures against the previous packet's failure modes
actually worked.

## Files inspected

The input export, `EXP-20260817-181`, both new dossiers, the coverage row,
`KU-070`, Current State, the roadmap, the session notes; all 43 markdown
exports and `ghidra-evidence.json`; the parent tree `67ca1b5^` for the novelty
negative. Binary: `work/copies/BUGS_PC-full-disc/bugs.exe`.

## Changes made

None by the auditor. Findings applied afterwards in the commit recording
[[EXP-20260817-182 - Independent input census audit]].

## Conclusions

**REJECT** on one failed completeness claim — the binding-table writer census —
which turns out to conceal a real finding: a key-configuration path with a
Restore Defaults branch. Five smaller defects. Everything else, including the
whole identifier layer, both extents and the novelty negative, reproduced
exactly.

## New hypotheses

None. The joystick button-index reading moves Inferred → Confirmed on
instruction evidence.

## Contradictions discovered

One internal: §4's "no instruction seen here indexes `DIJOYSTATE`" against
`0x0042ED77`, inside the extent §2 establishes.

## Tests run

`make vault-lint` 508/0/0; `make audit-tracked` 0 violations; `make test` 686
passed, reproduced by a second run, qualified by open `KU-065`.

## Unresolved questions

`KU-070` as narrowed; the identity of the configuration screen; the extents
and callers of the three binding-table blocks.

## Recommended next action

Apply the findings — the writer census in particular has to be rewritten as a
positive result — and re-audit from a fresh context.

## Git commit if applicable

None by the auditor.
