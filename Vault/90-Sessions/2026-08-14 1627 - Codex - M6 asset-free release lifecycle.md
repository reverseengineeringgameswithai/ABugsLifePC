---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - implementation/release
  - implementation/compatibility
  - milestone/m6
---

# M6 asset-free release lifecycle

## Agent

Codex

## Goal

Progress through M6 while preserving Obsidian evidence discipline, protected
content boundaries, and a clean Git worktree.

## Files inspected

- Required system notes, charter, roadmap, decision/unknown registers, and
  implementation/reverse-engineering MOCs.
- M4 compatibility statements/checker, manifest implementation, CLI, launcher,
  tests, supported manifests, and the exact local derived game tree.

## Experiments inspected

- `EXP-20260814-103` and `EXP-20260814-104` for the accepted M4 entry gate.
- Prior Wine/Gamescope and clean-copy lifecycle evidence cited by M4.

## Changes made

- Added strict M6 v1.0.0 release metadata, deterministic canonical tar build/
  verify, isolated immutable version install/current/rollback CLI, and exact
  primary-host clean-copy smoke automation.
- Added 10 focused release/smoke regressions and portable release wrappers.
- Corrected appended-tar-content acceptance before closure.
- Updated release/user docs, roadmap/state/unknown/decision registers, MOCs,
  and experiment/session indexes.

## Conclusions

- Exact clean HEAD `5daee2bc...37a4c` produces identical 378,880-byte archives
  at SHA-256 `1527281c...b62a0` with source-tree digest `423eb946...ada7`.
- The exact primary-host 21-file/three-case matrix, isolated artifact, bounded
  migration/rollback, failure snapshots, 486 tests, compatibility, and hygiene
  gates pass.
- M6 is Complete only for asset-free toolkit release and primary-Linux
  launcher readiness. No gameplay/render/audio/game-rollback/Windows or
  unlisted environment/input claim follows.

## New hypotheses

None.

## Contradictions discovered

Member-only tar verification could ignore appended undeclared content. Exact
canonical archive reconstruction now rejects that case and has a regression.

## Tests run

- 10/10 focused release/smoke tests.
- 3/3 exact migration/failure rerun.
- 486/486 canonical tests.
- Dual-build byte comparison, strict verification, exact three-case smoke,
  isolated installed wrappers, M4 compatibility, Vault lint, tracked audit,
  diff, and clean-tree gates.

## Unresolved questions

See `KU-053` for the retained unsupported/untested release surfaces and the
existing presentation/runtime unknowns.

## Recommended next action

No packet is active. Select future work through a separate evidence-gated
roadmap decision without widening M4 or M6.

## Git commit if applicable

- `f4e94e4` - `feat: add bounded M6 release lifecycle`
- `5daee2b` - `fix: require canonical M6 release bytes`
- final documentation commit pending at note creation
