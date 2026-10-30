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

# Unambiguous compatibility authorities

## Goal

Execute exact M4.21 after the fresh M4.20 rejection: replace only ambiguous
substring authority alignment, retain the exact compatibility statement and
all game-facing behavior, document the evidence, and leave one clean immutable
worker for James M4.22.

## Work and evidence

- Repeated the complete startup sequence and read the exact M4.21 packet plus
  `EXP-20260814-078/079`, M4/M1 implementation notes, relevant MOCs, and both
  compatibility-authority sources and READMEs.
- Replaced generic fragment presence with exact ordered shell declarations,
  launcher command/guard extraction, Python AST contract extraction, one
  generated Environment block/row per claimed field, and scoped unique
  Markdown declarations.
- Added the four exact M4.20 regressions before adjacent cases across every
  extraction family. The focused suite now passes 36/36.
- Preserved the 6,177-byte v0.1 JSON and all authority/manifest/launcher bytes.
  The compatibility command still reports the same five anchors.
- A read-tracing harness observed exactly nine unique tracked asset-free reads
  and no path under `originals/`, `media/`, or `work/`.
- Final `make check` passes Python doctor, Vault lint over 253 notes with zero
  errors/warnings, the five-anchor check, 329/329 tests, tracked-file audit
  with zero violations, and both diff checks. All changed/new paths are text
  or Python source; protected authority/asset paths are unchanged. No game,
  original, media, work-copy, runtime, M2, PS1, or unscoped pytest action
  occurred.

## Conclusion

[[EXP-20260814-080 - Unambiguous effective compatibility-authority declarations]]
records M4.21 worker-complete, not independently accepted. The exact
width/filter/receipt/kernel counterexamples now reject, as do adjacent
competing declaration cases, without changing the statement or game-facing
behavior.

Exact fresh-context M4.22 is the sole successor. James must audit the immutable
worker, independently reconstruct and attack each extraction family, confirm
the nine-read boundary and retained gates, then return one serial-ratchet
verdict.

## Git commit if applicable

Intentional worker commit message: `fix: require unambiguous M4 authorities`.
