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
  - audit/hard-truth
---

# Independent M6 release hard-truth audit

## Agent

Codex, with an independent fresh-context hard-truth verifier.

## Goal

Verify whether M6 is truly complete before selecting any successor roadmap
agenda, while preserving Obsidian evidence discipline and a clean Git tree.

## Files inspected

- Required system notes, charter, roadmap, decision/unknown registers, MOCs,
  M6 implementation note, release contract, implementation, wrappers, and
  tests.
- Exact tracked-clean HEAD
  `61ab0f9400173e6137c93bae4e7ccb8cf00349e4` and its M6 implementation
  ancestors `f4e94e4` and `5daee2b`.

## Work performed

- Independently rebuilt and strictly verified the exact artifact twice.
- Attacked tar canonicalization and protected-content boundaries.
- Re-ran the exact primary-host 21-file/three-case smoke matrix.
- Exercised fresh exact and synthetic install/current/rollback paths, failure
  snapshots, installed wrappers, release-root substitutions, and dangling
  state identity.
- Kept tracked files read-only during verification; generated artifacts remain
  ignored under `work/`.

## Conclusions

- M6 receives `REJECT`, not `ACCEPT`.
- Exact artifact reproducibility, strict archive verification, smoke, M4
  compatibility, protected-content, and hygiene results survive.
- Normal installed-wrapper use creates five unlisted `.pyc` files and makes
  the artifact fail its own complete-inventory verification.
- Rollback/current accept linked selected-version or `releases/` roots, and
  install overwrites a dangling `state.json` symlink.
- M6 is Active only for the smallest installed-wrapper bytecode and installed-
  path-identity correction. No successor milestone begins.

## Contradictions discovered

The isolated installed-wrapper, immutable installed-version, and complete
failure/rollback claims in `EXP-20260814-105` do not survive ordinary use and
symlink/dangling-entry attacks. External `PYTHONDONTWRITEBYTECODE=1` makes the
wrapper case pass with zero bytecode, bounding that correction.

## Tests observed

- Two exact 378,880-byte archives at SHA-256 `1527281c...b62a0` with exact
  source-tree SHA-256 `423eb946...ada7`.
- Seven strict tar adversaries plus corrupt content reject.
- Exact 21-file/three-case smoke passes with 747-entry inventories and report
  SHA-256 `2f015813...37eb1`.
- Canonical 486 tests, five M4 anchors, Vault 304/0/0, tracked audit 0, diff,
  staged-diff, and clean-tree gates pass at the audited HEAD.

## Recommended next action

Apply only the correction in
[[EXP-20260814-106 - Independent M6 release hard-truth audit]], retain every
passing gate, and request another independent audit before roadmap progression.

## Git commit if applicable

- documentation-only audit commit pending at note creation
