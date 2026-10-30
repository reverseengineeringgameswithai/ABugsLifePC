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

# Fixed-pool index producer census

## Agent

Codex

## Goal

Complete exact offline packet M2.40 by classifying every direct or bounded
fixed-pool writer for `0x0059B730/0x0059B7B4`, deciding reader-time zero
reachability, and intersecting the sources with the established M1 route.

## Files inspected

- [[START HERE]], [[Current State]], [[Environment Status]], [[Project Charter]],
  [[Agent Operating Manual]], and [[Project Roadmap]]
- [[Decision Log]], [[Known Unknowns]], and [[Reverse Engineering MOC]]
- The existing Ghidra structured export and exact-hash work-copy executable
- Prior M2 producer/provenance artifacts and relevant function dossiers

## Experiments inspected

- `EXP-20260812-016`
- `EXP-20260813-049` through `EXP-20260813-055`

## Changes made

- Added [[EXP-20260813-056 - Fixed-pool index producer census]] and its static
  evidence report.
- Added conservative address-named dossiers for `0x0041BD10` and
  `0x0041B9F0`; updated the related `0x0041C420` dossier.
- Completed M2.40 with a bounded causal negative, kept `KU-023` open, deferred
  M2 without declaring it complete, and restored exact M4.1 as the sole active
  packet.
- Updated [[Current State]], [[Known Unknowns]], [[Decision Log]], relevant
  MOCs, the roadmap, and this session index.

## Conclusions

- The complete bounded first-dword store set is the pool clear at
  `0x0041C430`, the retained source-byte copy at `0x0041BD24`, and the
  conditional removal zero at `0x0041BBBA`.
- Initial clear zero cannot pass the reader gates, and the source copier cannot
  write zero to a valid initialized record.
- The late removal zero is statically reader-reachable because list insertion
  sets `0x4000` before mode-2 removal, which does not clear that bit.
- That zero is conditional on separate `LEVEL.RAW` and fixed-pool state. It
  has no M1 record, relocated-payload, or positive-target provenance.

## New hypotheses

None promoted. The late zero is a conditional native path, not an observation
about a named scene or a semantic field identity.

## Contradictions discovered

No unresolved evidence contradiction. The result refines both tempting
overstatements: initial zero does not reach the reader, while reader-time zero
is not impossible. Neither produces the required M1 causal edge.

## Tests run

- Exact executable SHA-256 recheck.
- Structured direct-reference and native call-site census.
- Independent GNU objdump 2.46 disassembly for every selected writer, caller,
  reader gate, and main-update ordering edge.
- `python scripts/vault-lint.py`.
- `PYTHONPATH=. .venv/bin/pytest -q tests`.
- `git diff --check`, tracked protected-content audit, staged review, and final
  clean-tree check.

## Unresolved questions

- The exact M1-to-ID-zero causal edge under `KU-023` remains unknown.
- Concrete source/state predicates for slots 2 and 3 in each unchanged scene
  were not observed and are not needed to retire their M1 provenance candidate.

## Recommended next action

Execute M4.1 only: add the fail-closed exact-hash whole-file replacement
manifest operation over user-owned work-copy files. Do not widen M2 unless a
separate PC-native candidate or concrete mod goal supplies a finite
discriminator.

## Git commit if applicable

`research: complete M2 fixed-pool index census`
