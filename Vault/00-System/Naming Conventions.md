---
type: policy
status: active
updated: 2026-10-02
tags:
  - research/naming
---

# Naming Conventions

## Evidence IDs

- `BIN-<sha256-prefix>`: binary identity
- `EXP-YYYYMMDD-NNN`: controlled experiment
- `FUNC-<binary-prefix>-<address>`: function dossier
- `FMT-...`: file-format dossier, as the `id:` property; the filenames read
  `PC <format>.md`
- `STRUCT-...`: structure dossier
- `HYP-YYYYMMDD-NNN`: hypothesis
- `DEC-YYYYMMDD-NNN`: decision. Older entries also use a short `DEC-NNN`; the
  [[Decision Log]] now uses dated headings
- `RUN-WINE-YYYYMMDD-HHMMSS`: Wine capture; other tools use the same shape
  (`RUN-GDB-`, `RUN-INP-`, `RUN-POKE-`, `RUN-RR-` and so on)
- `RUN-WINVM-...`: Windows VM capture
- `RUN-86BOX-...`: 86Box capture
- `XPORT-YYYYMMDD-NNN`: cross-port comparison ([[Cross-Port Evidence Policy]])
- `SRC-...`: external source ([[External Source Registry]]), e.g. `SRC-PS1-ABL`
- `CAP-NNN`: capability gap ([[Reverse Engineering Capability Gaps]])
- `KU-NNN`: legacy numbered unknown; the [[Known Unknowns]] register now uses
  headed sections

The full executable SHA-256 belongs in note properties even when an ID uses a prefix.

## Semantic names

Use `unknown_00418A20` for unknown semantics. Use `candidate_level_reader` or `probable_actor_update` only when cited evidence supports that degree of inference. Remove qualifiers only after confirmation. Apply the same discipline to structure fields and file-format sections.

## Files

Prefer IDs at the start of evidence-note filenames. Session notes use `YYYY-MM-DD - <agent> - <topic>.md`; notes before
2026-09-05 also carry `HHMM` after the date. Both forms stay as cited. Paths and artifact names should remain stable after being cited.
