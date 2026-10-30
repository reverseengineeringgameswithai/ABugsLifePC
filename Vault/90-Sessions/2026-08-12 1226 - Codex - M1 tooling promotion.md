---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - implementation/modding
  - re/file-format
---

# M1 tooling promotion

## Agent

Codex

## Goal

Complete roadmap M1.5 by auditing the parser, manifest schema, CLI, tests,
dossiers, and operator workflow against the exact M1 evidence boundary.

## Files and evidence inspected

- M1 experiments `EXP-20260812-006` and `EXP-20260812-008` through
  `EXP-20260812-013`
- `reimplementation/ablpc/`, `scripts/ablpc-mod`, all manifests and tests
- Exact Training and Level 01 work-copy DATs and retained accepted receipts
- Relevant file-format, implementation, roadmap, state, and unknown notes

No file under `originals/` was modified. No PS1 source was consulted.

## Changes made

- Added [[M1 Tool Support Matrix]] with explicit inspection, edit, rejection,
  preservation, runtime-acceptance, and distribution boundaries.
- Corrected `inspect --payload-targets` to filter to the evidenced PC masked
  dispatch-`0x49` class instead of walking unrelated records and aborting on a
  negative layout.
- Centralized the supported dispatch mask/value shared by inspection, scanning,
  and target rebinding.
- Made manifests reject unknown root fields and duplicate case-insensitive file
  paths, matching fail-closed Windows target semantics.
- Added synthetic regressions for filtered inspection and strict root/path
  validation.
- Expanded `reimplementation/README.md` with the support matrix, exact guarded
  operations, author/apply/stage flow, hardware runtime gate, and no-game-bytes
  distribution rule.

## Conclusions

- **Confirmed:** the real Level 01 supported-target inspection now reports nine
  references and four unique targets without parsing unrelated layouts.
- **Confirmed:** the Training and Level 01 target recipes reproduce output
  SHA-256 values `b8012a95…f720e` and `80649462…9965b`; their receipts are
  byte-identical to retained accepted-run receipts.
- **Confirmed:** the corpus remains 21 scanned files, 14 matching files, 990
  supported references parsed, and zero errors.
- **Confirmed:** implementation, tests, CLI help, dossiers, and author workflow
  now agree on the M1 supported/rejected boundary.
- **Unknown:** negative-count targets, other dispatches, complete target
  semantics, and many record/payload fields remain outside M1.

## Contradictions and negative results

- Before the fix, `inspect --payload-targets primary` failed on Level 01 with
  an unrelated negative payload-target count. The command's help promised the
  bounded positive path, so walking all dispatches contradicted its supported
  scope.
- No new runtime run was performed: the corrected inspector/schema do not alter
  edit emission, and exact outputs/receipts reproduce prior accepted bytes.

## Tests run

- 18 synthetic/regression tests pass.
- Real Level 01 inspection: nine supported references, four unique targets.
- Full target corpus: 990 parsed references, zero errors.
- Exact Training and Level 01 recipe outputs and receipts reproduce.
- Final Vault, tracked-file, diff, JSON, and Git checks are recorded in the
  handoff.

## Unresolved questions

- Which PC resource family is directly reachable from an M1 payload chain.
- Which content files are observed by unchanged Training and Level 01 loader
  logs.

## Recommended next action

Execute [[Project Roadmap#M2.1 — PC content census and loader-context baseline]]
without consulting another port: create the metadata-only inventory, reconcile
unchanged loader paths, and select a family only from a direct PC anchor.

## Git commit if applicable

Bounded commit message: `feat: promote bounded LEVEL DAT tooling`.
