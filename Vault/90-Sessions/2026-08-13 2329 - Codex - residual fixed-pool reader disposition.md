---
type: session
date: 2026-08-13
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/static
---

# Residual fixed-pool reader disposition

## Agent

Codex

## Goal

Complete exact offline M2.41 for fixed-pool slots 25 and 63, then leave a
clean committed Obsidian handoff to the independent hard-truth verifier.

## Files inspected

- [[START HERE]], [[Current State]], [[Environment Status]], [[Project Charter]],
  [[Agent Operating Manual]], and [[Project Roadmap]]
- [[Decision Log]], [[Known Unknowns]], [[Reverse Engineering MOC]], and
  [[Implementation MOC]]
- `EXP-20260813-049` through `EXP-20260813-057`
- The M2 generic-reader and fixed-pool producer reports
- The exact-hash work-copy executable through read-only native disassembly
- The existing Ghidra structured evidence export

## Changes made

- Added [[EXP-20260813-058 - Residual fixed-pool index reader disposition]]
  and its static evidence report.
- Corrected the exact slot-25 call gate from the earlier `0x00431804` premise
  to the later `0x004318E4-0x00431900` reload/test sequence.
- Classified all five fixed slot-63 calls, including two explicit
  `I == 0x23` exclusions and three state-gated zero possibilities.
- Added address-based dossiers for `0x004317D0`, `0x00459620`,
  `0x004467E0`, and `0x00446870` without semantic renaming.
- Recorded [[Decision Log#DEC-20260813-053 - Require an independent hard-truth ratchet for M2 disposition]].
- Completed M2.41 and made exact offline M2.42 the sole active packet.
- Updated the roadmap, current state, `KU-023`, relevant MOCs, and session
  index.

## Conclusions

- Slot 25 zero can reach the ID-zero lookup initially or one update after
  conditional removal. The ID-zero header's zero start word makes
  `0x00459620` return zero.
- Slot 63 zero cannot pass the two explicit `I == 0x23` calls but can pass the
  three state-gated calls, conditional on their exact route state; those calls
  use the ID-zero retained end index.
- The values and direct gates derive from separate `LEVEL.RAW`, fixed-pool,
  counter, scene/update, position, and event state rather than the established
  M1 record/payload/positive-target route.
- M2's causal gate and `KU-023` remain unresolved. No milestone disposition is
  accepted until the independent M2.42 verifier rules.

## New hypotheses

No new technical family is selected. The independent audit must determine
whether the existing evidence already retains another finite M2 candidate.

## Contradictions discovered

`EXP-20260813-057` cited `0x00431804` as the relevant slot-25 flag test, but
native control flow shows the selected call uses the later reload and opposite
`0x4000` gate at `0x004318E4-0x004318F3`. The audit's selection of slot 25
remains valid; only its unresolved gate premise required correction.

## Tests run

- Exact executable SHA-256 recheck.
- Independent native disassembly of the slot-25 caller/reader, all five fixed
  slot-63 calls, both slot-63 readers, and normal update order.
- Structured-reference checks for the slot-25 counter/route globals and the
  slot-63 state byte.
- `python scripts/vault-lint.py`.
- `PYTHONPATH=. .venv/bin/pytest -q tests`: the sandboxed pass completed 196
  tests and blocked seven GDB fixtures with `ptrace: Operation not permitted`;
  the required outside-sandbox rerun passed all 203 tests.
- `python scripts/audit-tracked-files.py`.
- `git diff --check`, staged review, and final clean-tree check.

## Unresolved questions

- Whether an exact finite PC-native M2 successor remains in already cited
  evidence.
- Whether the independent verifier accepts a deferred disposition or rejects
  it with one bounded successor.

## Recommended next action

Execute exact offline M2.42 in fresh context. Reread the full startup sequence,
attempt to falsify M2.41 and the proposed M2 disposition, and either accept or
name one exact bounded successor. After rejection, refresh through
[[START HERE]] again before continuing.

## Git commit if applicable

`research: close residual fixed-pool reader paths`
