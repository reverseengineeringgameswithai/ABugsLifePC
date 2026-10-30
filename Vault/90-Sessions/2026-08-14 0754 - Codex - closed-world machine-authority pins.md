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

# Closed-world machine-authority pins

## Goal

Execute exact M4.23 after the fresh M4.22 rejection: pin only the five already-
read machine authorities, retain all semantic/scoped checks and exact statement
behavior, document the evidence, and leave one clean immutable worker for
James M4.24.

## Work and evidence

- Repeated the complete [[START HERE]] and Obsidian startup sequence after the
  rejection and read exact M4.23, `EXP-20260814-078` through
  `EXP-20260814-081`, M4/M1 notes, relevant MOCs, and both READMEs.
- Added one closed mapping of exact SHA-256 pins for the launcher, manifest
  implementation, and three tracked manifests. Alignment hashes their already-
  read raw bytes before semantic checks and reuses those bytes for parsing.
- Added direct raw-byte pin tests and the six minimized M4.22 bypass families.
  The focused suite now passes 47/47 and the canonical suite passes 340/340.
- Independently recomputed the unchanged 6,177-byte statement and all five
  authority digests. A read-tracing harness observed exactly nine unique
  tracked asset-free reads and no path under `originals/`, `media/`, or
  `work/`.
- Preserved the statement, launcher, manifest implementation, manifests,
  human authority facts, schema, receipt, operations, workflows, and all game-
  facing behavior byte-exact.
- Final `make check` passes Python doctor, Vault lint over 257 notes with zero
  errors/warnings, the five-anchor checker, 340/340 tests, and tracked-file
  audit with zero violations. All 18 changed/new paths are Markdown/plain text
  or Python source, `git diff --check` is clean, and staged protected/game-byte
  and pinned-authority drift audits report zero paths.

## Conclusion

[[EXP-20260814-082 - Closed-world machine-authority byte pins]] records M4.23
worker-complete, not independently accepted. All six residual bypass families
and exact predecessor regressions now fail closed through the same-read pins.

Exact fresh-context M4.24 is the sole successor. James must audit the immutable
worker, independently reconstruct all five pins and six attack families,
confirm pre-semantic failure plus the nine-read boundary and retained gates,
then return one serial-ratchet verdict.

## Git commit if applicable

Intentional worker commit message: `fix: pin M4 machine authorities`.
