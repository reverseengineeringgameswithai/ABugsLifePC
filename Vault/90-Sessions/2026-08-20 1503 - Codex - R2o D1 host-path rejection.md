---
title: 2026-08-20 1503 - Codex - R2o D1 host-path rejection
date: 2026-08-20
agent: Codex
tags:
  - session
  - reverse-engineering
  - r2o
  - runtime
status: complete
---

# 2026-08-20 1503 - Codex - R2o D1 host-path rejection

## Outcome

The authorized `-003` D1 for [[EXP-20260820-004 - R2o completed-present state calibration protocol]] passed hardware Direct3D, retail Anthill Level01 load/title/index, and nested-display focus. The inherited identity guard hashed the exact uppercase physical Level01 DAT successfully. The R2o pre-attach guard then tried nonexistent lowercase `PC/BUGS/cd/level01/level.dat` and rejected before ptrace. D2 did not launch.

No debugger-register write, R2o process-memory read, stopped capture, DAT
write, localizer, or candidate action occurred. Cleanup completed, the final
audit was clear, and baseline `R:` was restored to retail. James accepted the
rejection as a host-path casing defect, not a renderer, level, display, or R2o
state result.

## Offline correction

Fresh `-004` identities use shared constants for exact physical
`PC/BUGS/CD/LEVEL01/LEVEL.DAT` and `PC/BUGS/CD/CD.TXT`. Pre-launch and
pre-attach guards require canonical regular nonsymlink files and exact hashes;
receipts and the independent validator bind their exact relative and canonical
paths. The targeted offline suite passes 97 tests. Runtime remains unauthorized
pending James acceptance and fresh exact authorization.

## Evidence

- D1 disposition SHA-256 `730d368c9469a81470a233688754e79550b6ba1b0ee13538cb90b0abfb10d9ae`.
- Final log SHA-256 `a994bec70758032fc51984108091e8386f705dde3f40defbc6c214d35a7b0d36`.
- Focus summary SHA-256 `9ab4a0c16322c97c8fba63826b28a18df05517a46b70aa8df754bd59eb25b99d`.
- Pre-attach identity SHA-256 `28f79a13d3fb606dfb99aa7d4c0c01f3ce7ba4c66591842d6a5e5b24bf326618`.
- Aggregate disposition SHA-256 `8c0f544f1033386c22827c83436708b5ecf7d78fc23e5e71b66820abb97458d5`.

## Links

- [[EXP-20260820-004 - R2o completed-present state calibration protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Current State]]
- [[Known Unknowns]]
- [[Reverse Engineering MOC]]
