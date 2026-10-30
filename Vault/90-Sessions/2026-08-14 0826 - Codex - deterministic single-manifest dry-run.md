---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - implementation/modding
  - implementation/compatibility
---

# Deterministic single-manifest dry-run

## Goal

Execute exact M4.25 after M4.24 acceptance: add one deterministic write-free
single-manifest report, retain every existing workflow and compatibility
boundary, document the evidence, and leave one clean worker for James M4.26.

## Work and evidence

- Repeated the complete [[START HERE]] and Obsidian startup sequence and read
  exact M4.25, `EXP-20260814-083`, M4/M1 notes, relevant MOCs, and both
  READMEs before implementation.
- Added `dry_run_manifest` and `ablpc-mod dry-run MANIFEST --source-root ROOT`
  on top of the exact existing in-memory preparation path.
- Added report-only prepared metadata for input/output sizes and authored edit
  ranges without changing ordinary receipt dictionaries or serialization.
- Proved all three LEVEL operations under schemas 1/2, whole-file replacement,
  exact report hashes/sizes/ranges, authored order, repeated byte identity,
  later failures, input/replacement hashes, record guards, protected roots,
  empty stdout on failure, and complete snapshot equality.
- Independently recomputed the changed manifest implementation SHA-256 as
  `ce66bd048e505546c002ebe8a1fdc4477822363cce8e4631618dd157a9c3d243`
  and refreshed only that pin. All 5/5 pins, exactly five membership, exact
  statement, 47 compatibility tests, nine unique reads, and zero protected
  reads survive.
- Pre-documentation gates pass 99 manifest tests, 161 combined manifest/LEVEL/
  compatibility tests, and 349 canonical tests.
- Final `make check` passes Vault lint over 261 notes with zero errors/warnings,
  the five-anchor checker, 349/349 tests, and tracked-file audit with zero
  violations. The 19 changed/new paths are Markdown/plain text or Python
  source/tests and `git diff --check` is clean.

## Conclusion

[[EXP-20260814-084 - Deterministic single-manifest dry-run report]] records
M4.25 worker-complete, not independently accepted. The report covers one
existing manifest only and creates no output, receipt, or persisted report.

Exact fresh-context M4.26 is the sole successor. James must independently
reconstruct report bytes and ranges, instrument mutation surfaces, attack the
full retained failure boundary, verify receipts/workflows and compatibility,
then return one serial-ratchet verdict.

## Git commit if applicable

Intentional worker commit message: `feat: add deterministic manifest dry-run`.
