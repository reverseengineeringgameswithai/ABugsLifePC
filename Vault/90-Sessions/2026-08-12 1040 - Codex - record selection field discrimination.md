---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/dynamic
  - re/rendering
  - re/file-format
  - implementation/modding
---

# Record selection field discrimination

## Agent

Codex

## Goal

Continue roadmap M1.3: discriminate record `+0x04`, `+0x08`, and `+0x0C`
through exact PC reads, guarded byte-local edits, and matched hardware runtime
evidence; reconcile existing `+0x0E`/`+0x10` evidence and advance the canonical
packet only if the field boundary is supported.

## Files and evidence inspected

- Required system notes, charter, roadmap, decisions, unknowns, and relevant
  MOCs
- Exact-hash `bugs.exe`, Training DAT, Ghidra export, and native `objdump`
  disassembly around `0x0044D430` and dispatch `0x004498F0`
- `EXP-20260812-008` through `EXP-20260812-010`
- Parser, manifest implementation, tests, and prior Training manifests
- Native Gamescope captures, receipts, and hardware-gated game logs under
  ignored work storage

No file under `originals/` was modified. No PS1 source was consulted.

## Changes made

- Recorded reviewable exact field-read disassembly.
- Added two hash-locked record-126 center candidates and one guarded record-125
  `+0x0C` candidate.
- Added an expected-value-guarded, signed, offset-named
  `set-scene-record-field-0c` operation plus synthetic locality/manifest tests.
- Ran unchanged and candidate arms only through the logged 640×480×16
  Direct3D path.
- Reconciled the candidate-center, positive visibility-bound, flags/sentinel,
  and relocated-payload boundary across dossiers and implementation notes.
- Replaced the inspector's disproven position/angle labels with conservative
  candidate-center components and signed `field_0c` output.
- Closed M1.3 and made non-Training same-dispatch validation the sole active
  M1.4 packet.

## Conclusions

- **Confirmed:** record `+0x04` and `+0x08` feed candidate selection in
  `0x0044D430`. Dispatch `0x49` switches to relocated record `+0x10` at
  `0x00449B61` before its render-placement calculations.
- **Confirmed:** record-126 `+512` candidates are accepted and have a frame
  byte-identical to the unchanged hardware control. They do not visibly move
  the content in the tested start camera (`EXP-20260812-011`).
- **Confirmed:** positive record `+0x0C` contributes the visibility bound.
  Reducing record 125 from `1259` to zero excludes only its partially visible
  right-edge element in matched phases (`EXP-20260812-012`).
- **Inferred:** the first three record dwords are candidate-center components;
  exact world-axis names and units remain unknown.
- **Unknown:** the convention for 508 negative signed `+0x0C` values and
  whether other dispatches preserve this record/payload boundary.

## New hypotheses

No new hypothesis. M1.4 remains the next discriminator for the cross-file
scope of [[HYP-20260812-001 - shared payload targets identify reusable render content]].

## Contradictions and negative results

- Earlier position/angle labels are contradicted within the bounded dispatch.
  The large first-dword edits removed records by crossing selection thresholds;
  they did not demonstrate render translation.
- One `+0x08` attempt did not accept the Training menu input and was rejected.
- Two `+0x0C` capture sequences were rejected because one remained on the
  title and the next began too late for phase matching. The retained rerun ties
  capture timing to accepted input and reaches `NextLife`.
- Animation-phase differences remain in unselected frames; conclusions use
  exact whole-frame identity or differences confined to the independently
  isolated record region.

## Tests run

- Exact manifest staging and source/output SHA verification for all three new
  candidates.
- `cmp -l`: `+0x04` and `+0x08` candidates change one byte each inside their
  four-byte fields; `+0x0C` changes only `0x0E80–0x0E81`.
- Four retained Wine/Gamescope runs pass both hardware log markers, omit
  `INITSOFTRENDER`, load Training, complete `InitMainGame`, and enter
  `NextLife`.
- ImageMagick exact comparison: EXP011 frame 08 has zero differing pixels for
  both candidates; EXP012 frame 02 has 756 differences only within
  `25x109+615+158`.
- `make check`: Vault lint reports 78 notes with zero errors/warnings, all 16
  tests pass, and the tracked-file audit reports zero violations.

## Unresolved questions

- Exact candidate-center axis names and units.
- The sign convention and semantics of negative record `+0x0C`.
- Whether non-Training records reproduce the bounded Training target-rebind
  result and whether other dispatches preserve the same pointer boundary.

## Recommended next action

Execute [[Project Roadmap#M1.4 — Non-Training same-dispatch validation]]:
identify a non-Training loaded DAT from the unchanged game log, then isolate
and rebind one valid positive dispatch-`0x49` record in that exact file.

## Git commit if applicable

Bounded commit message: `research: resolve scene record selection fields`.
