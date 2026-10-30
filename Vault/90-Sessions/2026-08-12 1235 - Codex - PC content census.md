---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/file-access
---

# PC content census

## Agent

Codex

## Goal

Complete roadmap M2.1 by inventorying the exact derived PC content tree as
metadata, reconciling explicit loads from unchanged Training and Level 01
hardware runs, and selecting one PC-evidenced family for a bounded loader
trace.

## Files and evidence inspected

- Derived work copy `work/copies/BUGS_PC-full-disc/PC/BUGS`
- Accepted hardware logs `RUN-WINE-20260812-000634` and
  `RUN-WINE-20260812-114514`
- Disc listing/provenance from `EXP-20260811-001`
- Whole-file loader dossier [[FUNC-97C95BA5572D-004AE240]] and exact log
  string address `0x004E93AC`
- Roadmap, MOCs, current state, unknown register, and M1 evidence boundary

No file under `originals/` was modified. No PS1 source was consulted.

## Changes made

- Added a metadata-only census module and CLI that report relative paths,
  sizes, hashes, extension/family groups, duplicate groups, and explicit
  loader-log matches.
- Added fail-closed checks for protected source roots, symlinks,
  case-insensitive path collisions, unsafe log paths, and duplicate log labels.
- Added synthetic regression tests and generated the reviewable JSON and
  Markdown reports.
- Added [[PC Content Census]] and
  [[EXP-20260812-014 - PC content census and loader context]].
- Closed M2.1 and made the plant resource caller/consumer trace M2.2.

## Conclusions

- **Confirmed:** 721 files totaling 460,306,509 bytes produce tree fingerprint
  `b145e2aa5fbf7e3350cf437985bbc76c764c36f2d954105d5282af4831738986`.
- **Confirmed:** all 25 Training and 45 Level 01 explicit load paths match the
  census; their union contains 51 files and their intersection contains 19.
- **Confirmed:** `CD/PLANTS` contains 11 basename-matched `.ANM`/`.ALL` pairs;
  four pairs are loaded in both retained scenes.
- **Inferred:** the repeated paired names are useful for tracing, but do not
  prove common format semantics or a complete resource relationship.
- **Unknown:** callers, downstream consumers, pair semantics, and any bridge
  from an M1 payload to these files.

## Contradictions and negative results

- The census has no unmatched explicit load paths.
- The explicit loader message does not cover audio/SFX activity, so zero
  observed loads for those families must not be read as runtime non-use.
- M1 visible plant-like placement evidence does not identify a specific plant
  resource file.

## Tests run

- Census regeneration is byte-deterministic with the runtime-generated root
  `bugs.log` excluded.
- Synthetic/regression, compile, JSON, Vault, tracked-file, and Git checks are
  recorded in the handoff.

## Recommended next action

Execute [[Project Roadmap#M2.2 — Plant resource caller and consumer trace]]:
map callers of `0x004AE240` for the shared plant paths, then trace `.ANM` and
`.ALL` buffer ownership and downstream consumers without semantic renaming.

## Git commit if applicable

Bounded commit message: `research: census PC content loader paths`.
