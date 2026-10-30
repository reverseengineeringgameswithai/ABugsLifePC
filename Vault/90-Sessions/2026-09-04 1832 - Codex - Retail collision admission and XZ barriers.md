---
type: session
date: 2026-09-04
agent: Codex
topic: Retail collision admission and XZ barriers
status: completed-offline-not-independently-audited
---

# 2026-09-04 1832 - Codex - Retail collision admission and XZ barriers

The user asked to inspect the current state and continue toward a better
terrain/collision approach. Initial HEAD was `0f589de`, clean. Read the Vault
orientation, charter, operating manual, current priority, relevant MOCs,
collision/height code and dossiers, EXP-20260904-001, its session addendum,
KU-080/081 and Ghidra caveats. The latest top-of-note priority supersedes the
generated briefing's stale actors/input pickup. R2q-032 remains banked with an
incomplete final gate.

Completed DEC-226's real-cell/template step in
[[EXP-20260904-002 - Retail collision admission and separate XZ barriers]].
Added `scripts/terrain-retail-probe.py`, a report containing measurements and
locators, and35 regression tests. Original retail instructions load both
Level01/Level03 plus PLANTTER, construct bounds and spatial buckets, and run
the full movement coordinator on controlled positions. Loader and movement
have no stubs; initializer slice boundaries and synthetic preconditions are
explicit. All original assets and source files remain unchanged.

Level01 source87/cell1000 is admitted and causes X/Z deflection, with specific
descriptor removal and moving-away controls. Kind`0x101` source179 independently
supplies four X/Z segment candidates; its first pair causes the measured
response at three widely separated Y values. Plant templates load below N and
are cleared before movement, while the direct dynamic-store range starts at N.
Both terrain files' descriptor bases/payload identities/bounds match the
independent height model. Counts, locators, hashes and limits are in EXP-002.

DEC-227 makes segment grammar and grounded-contact controls the next offline
packet. Updated Current State, Known Unknowns, Environment Status, relevant
research/implementation notes and MOCs. No external PS1 repository, game,
renderer, live debugger, mapping, recovery wrapper or live memory write was
used. No subagent review was requested or claimed. No commit was made.

Verification:105 focused tests passed in4.03s, none skipped. The full repository
suite was not run for this bounded offline change; it does not complete the
banked R2q full gate. Git hooks were already installed through
`core.hooksPath=scripts/git-hooks`.

Final import, Vault, compatibility, tracked-file and whitespace gates pass.
Vault lint reports0 errors and8 existing budget/staleness/orphan warnings.
An independent second invocation reproduces the complete JSON report byte-for-byte
(this is a repeat invocation, not an independent agent review).
Claim sweeps find zero instances of the superseded unknown-cell-word and
real-cell-reachability wording. The closing session audit is clean: zero
processes, null sinks or open sessions. No cleanup or mapping action was needed.
