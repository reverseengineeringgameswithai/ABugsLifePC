---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/static
  - re/file-format
  - system/roadmap
---

# Positive payload target roadmap packet

## Agent

Codex

## Goal

Execute a substantial first packet from [[Project Roadmap]]: bound the Training
payload targets and their PC consumer, enumerate reuse, validate the supported
class across files, promote only demonstrated structure into safe tooling, and
leave the next runtime discriminator ready.

## Files inspected

- Exact-hash PC executable work copy and static export at `0x0044BB70`,
  `0x004498F0`, and `0x0045A7F0`
- Exact Training `CD/LEVEL07/LEVEL1.DAT` work copy, including record payloads
  and targets `0x111E4` and `0x1319C`
- All 21 local PC `LEVEL*.DAT` work copies through a hash-reporting,
  same-dispatch metadata scan
- Existing parser, manifest implementation, tests, roadmap, evidence notes,
  function dossiers, MOCs, state, decision, hypothesis, and unknown registers

No file under `originals/` was modified. No PS1 source was consulted.

## Experiments inspected

- [[EXP-20260812-006 - LEVEL DAT prefix and manifest mod]]
- [[EXP-20260812-008 - Training record watchpoints and individual roles]]
- New packet: [[EXP-20260812-009 - Training payload target structure and reuse census]]

## Changes made

- Added a complete Training primary reference/block report and a 21-file
  dispatch-`0x49` corpus report containing metadata only.
- Added bounds-checked parsing for the positive-count target layout consumed by
  `0x0045A7F0`, including command-group and table-reference validation.
- Added read-only CLI inspection and corpus scanning.
- Added an exact-source-/expected-old-offset-guarded target-rebind manifest
  operation for the bounded dispatch class; no arbitrary byte patch exists.
- Added reciprocal record-124/125 target candidates and verified their staged
  hashes and exact field locality without claiming runtime acceptance.
- Added two function dossiers, one structure dossier, one hypothesis, and the
  `Structures MOC`.
- Closed roadmap packet M1.1 and made the matched rebind experiment M1.2 the
  sole active packet.
- Reconciled [[Current State]], [[Known Unknowns]], [[Decision Log]], the
  format/implementation notes, and relevant MOCs.

## Conclusions

- **Confirmed:** for Training flags `0x0059`, the PC fixup relocates payload
  `+0x1C`, masked dispatch `0x49` passes it to `0x0045A7F0`, and the latter
  consumes the bounded positive-count table/command grammar in `EXP-009`.
- **Confirmed:** Training has 262 primary references to 109 unique positive
  target blocks; 19 are shared, including 11 references to `0x111E4` and 17 to
  `0x1319C`.
- **Confirmed:** 990 same-dispatch records across 14 PC files validate with
  zero errors. The claim is deliberately limited to that dispatch/layout.
- **Inferred:** shared targets provide reusable render content. Complete object
  identity and exact entry/command semantics remain unknown.

## New hypotheses

- [[HYP-20260812-001 - shared payload targets identify reusable render content]]

## Contradictions discovered

No contradiction was found in the active Training layout. The negative-count
branch in `0x0045A7F0` contradicts any attempt to treat all targets as the same
positive layout; tooling therefore rejects that branch rather than normalizing
it.

## Tests run

- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=. .venv/bin/pytest -q`: 14 passed.
- Both committed Training candidates staged from the exact source hash. Record
  124 output: `b8012a95…f720e`; record 125 output: `b8ea00be…0ed9`.
- Exact byte comparison: each candidate changed only its selected four-byte
  pointer field; for these offsets only the low two bytes differ.
- `scripts/ablpc-mod scan-payload-targets ... --json`: 21 files scanned, 990
  matching records, 990 parsed references, zero errors.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 make check`: dependency smoke test, Vault
  lint (`73` notes, `0` errors, `0` warnings), pytest (`14` passed), tracked-file
  audit (`0` violations), and Git whitespace checks all passed.

## Unresolved questions

- Whether the reciprocal rebinds cause only the selected placement to adopt
  the contrasting target's visible render content.
- Exact 12-byte entry fields, command mode bits, and item suffixes.
- Negative-count blocks and other scene dispatch classes.
- Whether one target is a complete object definition or only one reusable
  render component.

## Recommended next action

Execute [[Project Roadmap#M1.2 — Guarded target rebind and visible reuse]] with
the prepared manifests and an unchanged matched Direct3D control. Preserve
receipts, logs, captures, and exact output hashes.

## Git commit if applicable

Bounded commit message: `research: bound positive level payload targets`.
