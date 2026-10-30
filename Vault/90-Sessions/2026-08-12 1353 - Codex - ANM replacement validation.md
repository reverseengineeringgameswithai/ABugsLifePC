---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/resources
  - re/dynamic
---

# ANM replacement validation

## Agent

Codex

## Goal

Execute roadmap packet M2.5: replace exact plant 04 `.ANM` bytes with the
existing same-size/same-first-level-layout plant 10 `.ANM`, retain plant 04
`.ALL`, and classify the original-executable hardware result.

## Files inspected

- `Vault/00-System/START HERE.md`, Current State, Environment Status, Project
  Charter, Project Roadmap, Decision Log, Known Unknowns, and relevant MOCs.
- Exact work-copy `bugs.exe`, `PLANT04.ANM`, `PLANT10.ANM`, `PLANT04.ALL`, and
  `PLANT10.ALL` hashes.
- Existing Wine/Gamescope launcher, prior capture experiments, and M2.4 ANM
  dossiers/tooling.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-015 - Plant pair caller and consumer trace]]
- [[EXP-20260812-016 - Plant request origin and separate DAT table]]
- [[EXP-20260812-017 - Bounded PC ANM inspector]]
- [[EXP-20260812-018 - Same-layout PC ANM replacement]]

## Changes made

- Created ignored control/replacement trees and copied only exact plant 10
  `.ANM` bytes onto staged plant 04 `.ANM`.
- Proved source hashes, destination hash, one-path staging locality, 884
  changed bytes, and unchanged plant 04 `.ALL`.
- Ran matched hardware Direct3D Training arms through `NextLife`, plus a
  same-presentation control rerun.
- Retained two game logs, run metadata, and a metadata-only comparison report;
  screenshots and staged game bytes remain ignored under `work/copies/`.
- Updated the ANM format/function/implementation notes, experiment index,
  roadmap, Current State, Known Unknowns, Decision Log, and MOCs.
- Isolated first-launch Obsidian GUI churn in commit `ea36240`: appearance and
  graph preferences are ignored while the shared core-plugin state is retained.

## Conclusions

- **Confirmed:** Both retained arms selected `640x480x16` Direct3D hardware,
  never entered `INITSOFTRENDER`, loaded both plant 04/10 pairs, ended
  `InitMainGame`, and entered `NextLife`.
- **Confirmed:** The exact `.ANM`-only substitution with destination `.ALL`
  unchanged is accepted by the original executable.
- **Confirmed within the tested visual procedure:** No stable start-camera
  visual change is discriminated beyond control-to-control animation variance.
- **Unknown:** Later/off-camera/nonvisual effects, general ANM
  interchangeability, and complete `.ANM`/`.ALL` pair semantics.

## New hypotheses

The paired `.ALL` may contribute the resource identity or visible difference
not isolated by the `.ANM`-only copy. This is a bounded M2.6 hypothesis, not a
field-semantic claim.

## Contradictions discovered

No structural or runtime contradiction. The initially expected possibility of
a visible ANM-only substitution was not observed at the tested camera. An
initial control compositor capture exposed at 1920×1080 while later arms were
2560×1440; a same-size control rerun resolved presentation-size comparability.

## Tests run

- Exact SHA-256 checks for executable and four plant files.
- Recursive control/source and replacement/source comparisons.
- Exact `cmp` proof that staged plant 04 `.ANM` equals plant 10 `.ANM`.
- Hardware log gate and `InitMainGame`/`NextLife` checks for both arms.
- Normalized log diff: byte-identical after drive-label/timing normalization.
- 15-frame PipeWire capture per primary arm; 640×480 point-sampled
  normalization; all-pairs ImageMagick AE/RMSE; temporal-median control check.
- Repository validation is recorded after documentation closure.

## Unresolved questions

- Does replacing both exact equal-size plant files produce a stable visible
  identity change?
- Is that paired substitution accepted by `0x00448010` despite the still
  unknown `.ALL` embedded layout?
- Which later camera/animation state could expose an `.ANM`-only effect?

## Recommended next action

Execute [[Project Roadmap#M2.6 — Same-size paired plant replacement]] with a
new two-path staged copy and the same hardware/log/control-variance gates.

## Git commit if applicable

Bounded commit message: `research: validate ANM-only plant replacement`.
