---
type: session
date: 2026-08-13
agent: Codex (independent M2.42 verifier)
status: completed
tags:
  - session
  - re/resources
  - re/static
  - re/milestone-audit
---

# Independent M2 disposition audit

## Agent

Codex, acting as the independent fresh-context M2.42 verifier in the required
serial ratchet.

## Goal

Adversarially audit M2.41 and its proposed stronger milestone disposition,
then record exactly `ACCEPT` or `REJECT` without weakening M2's exit gates.

## Files inspected

- `AGENTS.md`, [[START HERE]], every startup note it requires,
  [[Project Charter]], [[Agent Operating Manual]], and all current MOCs
- [[EXP-20260813-049 - M2 exit-gate reconciliation]] through
  [[EXP-20260813-058 - Residual fixed-pool index reader disposition]]
- The M1 record, relocated-payload, and positive-target closures; `KU-023`;
  relevant address-based dossiers; and prior M2 disposition reports
- The exact read-only work-copy executable through independent rehash and
  native disassembly
- The existing Ghidra structured evidence export

## Changes made

- Added [[EXP-20260813-059 - Independent M2.41 disposition hard-truth audit]]
  and its detailed static evidence report.
- Independently reproduced the exact slot-25/slot-63 call census, actual call
  gates, ID-zero reader paths, normal update/M1 order, and M1 negative.
- Audited every finite retained surface in the cited evidence, including
  current/list readers, mode-2 pointer-list compaction, and the alternate
  update branch.
- Recorded [[Decision Log#DEC-20260813-054 - Accept the M2.41 disposition and defer M2 without closure]].
- Completed M2.42 with `ACCEPT`, deferred M2 without closing it, kept M3
  planned, and activated exact M4.1.
- Updated [[Project Roadmap]], [[Current State]], [[Known Unknowns]], relevant
  MOCs, and this session index.

## Conclusions

- M2.41 survives independent falsification at its declared conditional static
  boundary. Slot 25 zero can reach its selected read and return through the
  ID-zero header's zero start; slot 63 zero is excluded by two `I == 0x23`
  calls but can reach three state-gated reads of the ID-zero end index.
- The selected values and direct gates remain separate from the established
  M1 record/payload/positive-target route.
- "No successor was ranked" was not treated as evidence. The separate audit
  found no exact finite PC-native successor still retained in the already
  cited evidence.
- Persistent/copied state, indirect aliases, and unreviewed resource families
  remain limitations, not exact bounded successors. This is not a
  whole-program absence proof.
- Verdict: **ACCEPT**. M2 remains incomplete and is `Deferred`; its causal
  dependency exit gate and `KU-023` remain open. M4/M4.1 are `Active`.

## New hypotheses

None. No new technical family or semantic interpretation is selected.

## Contradictions discovered

No contradiction invalidates M2.41. The audit confirmed its own explicit
limitation: reader-time zero is a conditional static reachability result, not
evidence that a named shipped scene realizes every combined predicate.

## Tests run

- Exact executable SHA-256 recheck and file-format/size verification.
- Independent native disassembly and exact direct-call census for the bounded
  M2.41 readers/callers, plus M1-order and retained-list checks.
- Structured-export reference queries for selected M1 closures and state.
- `python scripts/vault-lint.py`: 210 notes, 0 errors, 0 warnings.
- `PYTHONPATH=. .venv/bin/pytest -q tests`: 203 passed.
- `python scripts/audit-tracked-files.py`: 0 violations.
- `git diff --check`, staged review, and final clean-tree check: passed.

## Unresolved questions

- `KU-023`: the exact PC-native causal edge from an M1 scene record or
  positive target to the selected ID-zero resource path.
- The first M2 exit gate remains unmet; M2 is not complete.

## Recommended next action

Execute exact M4.1. Add only the hash-guarded, asset-free whole-file
replacement operation over user-owned work-copy files, integrated with the
existing staging/receipt contract and synthetic tests. Do not parse `.ALL`,
claim general compatibility, or reopen M2 without its recorded revisit
condition.

## Git commit if applicable

`research: accept independent M2 disposition audit`
