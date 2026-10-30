---
type: session
date: 2026-08-13
agent: Codex
status: completed
tags:
  - session
  - re/static
  - re/rendering
  - implementation/tooling
---

# Exact 0A6C admission evaluator fixtures

## Agent

Codex

## Goal

Execute the offline implementation gate of roadmap packet M2.32 under the
START HERE workflow: implement and fixture-test only the purpose-specific
exact-`0x0A6C` native evaluator and payload-free receipt, preserve the result
in Obsidian, do not launch or instrument the game, and leave Git clean.

## Files inspected

- The required START HERE sequence, Agent Operating Manual, Project Charter,
  current state/environment, roadmap, decision and unknown registers, and all
  relevant MOCs.
- M2.31's exact native arithmetic/input/receipt report, caller/builder and
  Direct3D batch dossiers, Runtime Tooling, and `EXP-20260813-044`.
- The schema-5 validator/controller/tests and all three accepted M2.29
  `spec.resolved.json` files.
- Exact native disassembly of caller `0x0044F8E0..0x0044F99D` and builder
  `0x00405FE0..0x004066BD` from the hash-verified work copy.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments

- [[EXP-20260813-044 - Exact 0A6C admission-state localization]]
- [[EXP-20260813-045 - Exact 0A6C admission evaluator fixtures]]

## Changes made

- Added `scripts/exact_0a6c_admission.py`, implementing only the exact native
  signed arithmetic, ordered first-reject chain, active-state digest, and
  payload-free receipt.
- Extended the compatible read-only harness to 1.5.0/schema 6 with a hard-
  locked `exact_0a6c_admission` mode at the existing three data watches.
- Added synthetic coverage for every reject PC, depth branch/skip, arithmetic
  and digest failure, prediction/count mismatch, complete-plan/envelope drift,
  exact controller closure, and retained-output redaction.
- Added the implementation report and `EXP-20260813-045`, recorded
  `DEC-20260813-040`, narrowed KU-044 to its live phase, and updated Current
  State, Environment Status, roadmap, Runtime Tooling, dossiers, and MOCs.
- Added no runtime arm, execution point, watch slot, target/source edit,
  payload, semantic name, other record/family, general `.ALL` tool, or
  cross-port evidence.

## Conclusions

- **Confirmed offline:** all 13 concrete reject PCs/12 logical slots and the
  native wrap/truncation/failure behaviors pass synthetic fixtures.
- **Confirmed offline:** the three accepted M2.29 specs independently share
  the canonical 168-call plan SHA-256
  `5eb280a7bd54b56a9654fed7984e9677a15618c5376be703a85718ea3bb2ffec`
  and the same fixed watch/form/family/root/page/survival envelope.
- **Confirmed offline:** schema 6 rejects envelope drift, re-digests active
  state at post, rejects count disagreement, redacts stop values, and emits
  only the M2.31 receipt.
- **Unknown:** live prediction/count agreement and a stable first reject in
  fresh controls. Schema 6 exact mode is not live-validated.

## Contradiction

No implementation contradiction was found. The fixtures deliberately prove
that digest drift and prediction/count disagreement reject the result. A live
control disagreement must likewise be preserved rather than resolved by
inference.

## Tests run

- Reverified authoritative executable SHA-256.
- Compared all three accepted M2.29 plans and fixed gates; all agree at 168
  calls and the canonical digest above.
- `make test`: 197 passed at the implementation gate.
- Final handoff also runs full `make check`, Obsidian link checks,
  `git diff --check`, protected-path audit, and post-commit cleanliness check.

## Unresolved questions

- Does the evaluator reproduce exact live count outcomes in fresh matched
  arms?
- Do both fresh controls share one first-reject PC while replacement passes,
  or does temporal variation remain?
- Whether admission state has any source or visible causal relationship.

## Recommended next action

Keep [[Project Roadmap#M2.32 — Exact `0x0A6C` admission-predicate receipt]]
at its completed offline gate. Do not run its fresh control/replacement/
control phase without explicit authority. If authorized, use only the exact
schema-6 envelope and preserve every M2.29 acceptance gate.

## Git commit if applicable

Bounded commit message: `research: implement exact 0A6C admission receipt`.
