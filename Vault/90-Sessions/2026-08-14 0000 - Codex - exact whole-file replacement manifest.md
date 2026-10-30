---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - implementation/modding
  - implementation/manifest
---

# Exact whole-file replacement manifest

## Agent

Codex

## Goal

Complete exact M4.1, leave a clean committed Obsidian handoff, and make the
independent James M4.2 hard-truth audit the sole next packet.

## Files inspected

- [[START HERE]], [[Current State]], [[Environment Status]], [[Project Charter]],
  [[Agent Operating Manual]], and [[Project Roadmap]]
- [[Decision Log]], [[Known Unknowns]], and [[Implementation MOC]]
- [[M1 Tool Support Matrix]]
- `EXP-20260812-033`, `EXP-20260813-049`, and `EXP-20260813-059`
- Existing manifest, CLI, staging, receipt, test, and documentation code
- The exact two files in the ignored user-owned local corpus, by hash only

## Changes made

- Added schema 2 `opaque-file-v0` plus exact `replace-whole-file` support.
- Added complete-manifest preflight, source/destination collision rejection,
  stricter lexical Windows-target safety, and source symlink containment.
- Preserved schema 1 and allowed existing M1 operations in schema 2.
- Added the exact asset-free FLICK/FLICKD manifest and user documentation.
- Added synthetic sparse, staging, hash, path, collision, preflight,
  compatibility, receipt, and CLI regression tests.
- Completed the ignored local corpus hash/application check.
- Added [[EXP-20260814-060 - Exact whole-file replacement manifest boundary]]
  and [[M4 Exact Whole-file Replacement]].
- Recorded the M4 serial hard-truth ratchet in [[Decision Log]].
- Made exact M4.2 the sole next packet pending James's independent verdict.

## Conclusions

- The exact accepted user-owned pair is expressible without bundling assets or
  parsing `.ALL`.
- Both input hashes are preflighted, source files remain unchanged, sparse
  output writes only the destination plus receipt, and staged output preserves
  the source path.
- Receipt JSON is deterministic and records input, replacement, and output
  hashes.
- M1 schema-1 behavior remains green; schema 2 can retain M1 operations.
- This result is not a general resource compatibility claim and does not close
  M4's remaining exit gates.

## New hypotheses

None. No file semantics, identity, or compatibility rule was inferred.

## Contradictions discovered

None in the declared M4.1 evidence boundary.

## Tests run

- Focused manifest and existing M1 manifest tests.
- Complete repository suite: 228 pytest tests passed; Vault lint reported 213
  notes with 0 errors and 0 warnings; tracked-file audit reported 0 violations.
- Exact local destination/replacement SHA-256 checks before and after sparse
  application, byte comparison, output-file census, and ignore proof.
- Vault lint, tracked-file audit, diff checks, staged review, and clean-tree
  check before handoff.

## Unresolved questions

- Whether independent M4.2 review accepts every M4.1 safety and distribution
  claim.
- Which one exact remaining M4 capability James ranks next if M4.1 is accepted.

## Recommended next action

James must execute exact offline M4.2 from fresh context: reread the complete
startup sequence, attempt to falsify M4.1, and either accept it with one exact
next M4 packet or reject it with one bounded corrective packet. Do not begin
another worker packet before that verdict.

## Git commit if applicable

`implementation: add exact whole-file replacement manifest`
