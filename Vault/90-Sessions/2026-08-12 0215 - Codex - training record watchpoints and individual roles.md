---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/dynamic
  - re/file-format
---

# Training record watchpoints and individual roles

## Agent

Codex

## Goal

Execute the next bounded PC-native reverse-engineering step: identify the
runtime consumer and individual visible roles of Training primary records
124–126, then bank the result under the project's evidence policy.

## Files inspected

- Exact-hash `bugs.exe` work copy and static disassembly around `0x0044D430`,
  `0x0044BB70`, and caller `0x004671D0`
- `CD/LEVEL07/LEVEL1.DAT` work copy, especially file offsets `0x0E60`,
  `0x0E74`, `0x0E88`, `0x26DC`, `0x26FC`, and `0x271C`
- Existing parser, manifest workflow, function dossiers, format dossier, and
  `EXP-20260812-006`

## Experiments inspected

- [[EXP-20260812-006 - LEVEL DAT prefix and manifest mod]]
- [[EXP-20260812-008 - Training record watchpoints and individual roles]]

## Changes made

- Recorded `RUN-GDB-20260812-021920`, including live pointer mapping, three
  hardware watchpoint hits, and negative WineDbg/software-breakpoint results.
- Added three conservative, hash-locked one-record manifests under `mods/`.
- Recorded a matched untouched Direct3D control and three individual Direct3D
  variant runs with logs, receipts, captures, hashes, and exact difference
  metrics.
- Updated the two function dossiers, file-format dossier, Current State, Known
  Unknowns, Environment Status, Decision Log, implementation note, and MOCs.

## Conclusions

- **Confirmed:** `0x005BA240` stores the allocated DAT-buffer pointer.
- **Confirmed:** records 124–126 all reach the first-dword read at
  `0x0044D5B8` inside `0x0044D430` during the observed initialization/update
  path.
- **Confirmed:** individual mutations produce three disjoint visible plant
  differences. These records are not alternative LOD representations of one
  on-screen object in the tested Training start state.
- **Confirmed:** records 125 and 126 share the observed internal payload target
  `0x111E4`; record 124 uses `0x1319C` at the corresponding field.
- **Inferred:** records 125 and 126 are separate placements reusing a referenced
  definition. The referenced structure's semantics remain unknown.

## New hypotheses

- The shared target at `0x111E4` may identify reusable object content used by
  separate scene placements, but it must not be named as geometry or an object
  definition without another PC-native discriminator.

## Contradictions discovered

- The earlier joint software-renderer result looked like removal of one central
  flower cluster and left an LOD hypothesis open. Matched individual 640×480
  captures instead show three disjoint affected elements.
- WineDbg's proxy and a native software breakpoint caused debugger-side faults;
  the unchanged game succeeded when restarted and traced using hardware
  watchpoints at its natural title pause.

## Tests run

- Three `ablpc-mod stage` operations against the exact source DAT hash; every
  receipt changed only its requested record and produced the recorded output
  hash.
- Native GDB read watchpoints for records 124, 125, and 126; every hit stopped
  after `0x0044D5B8` with `ESI` at the expected live address.
- Four Wine 11 Direct3D Training runs; all logs reached `InitMainGame` and
  `NextLife`.
- ImageMagick exact AE/RMSE/bounding-box comparison against the matched control.
- Reapplied all three committed manifests from the exact source hash; output
  hashes matched the recorded runtime receipts.
- `make check`: Python dependency smoke test, Vault lint (`64` notes, `0`
  errors, `0` warnings), `pytest` (`10` passed), tracked-file audit (`0`
  violations), and Git whitespace checks all passed.

## Unresolved questions

- What structures begin at payload targets `0x111E4` and `0x1319C`?
- Which code consumes those targets, and do they identify reusable object
  content?
- Under what conditions are primary records revisited after initialization?
- What exact WoW64 debugger limitation caused the proxy/software-breakpoint
  faults?

## Recommended next action

Trace static and runtime consumers of `base+0x111E4` and `base+0x1319C`, compare
their bounded structures, and design one PC-native test of the reusable-content
hypothesis before extending the parser.

## Git commit if applicable

Bounded commit message: `research: identify training record roles`.
