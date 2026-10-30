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

# Paired plant replacement validation

## Agent

Codex

## Goal

Execute roadmap packet M2.6: replace both plant 04 files with the exact
equal-size plant 10 pair in an ignored staged copy and classify the original-
executable hardware, load, gameplay, and visual result.

## Files inspected

- `Vault/00-System/START HERE.md`, Current State, Environment Status, Project
  Charter, Project Roadmap, Decision Log, Known Unknowns, and relevant MOCs.
- Exact work-copy `bugs.exe`, `PLANT04.ANM`, `PLANT10.ANM`, `PLANT04.ALL`, and
  `PLANT10.ALL` hashes and sizes.
- Prior plant caller/consumer, request-origin, ANM-inspector, and M2.5 evidence.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-015 - Plant pair caller and consumer trace]]
- [[EXP-20260812-016 - Plant request origin and separate DAT table]]
- [[EXP-20260812-017 - Bounded PC ANM inspector]]
- [[EXP-20260812-018 - Same-layout PC ANM replacement]]
- [[EXP-20260812-019 - Same-size paired plant replacement]]

## Changes made

- Created ignored control/replacement trees and copied exact plant 10 `.ANM`
  and `.ALL` bytes over only the two staged plant 04 paths.
- Proved executable/four-source hashes, exact destination/source equality,
  two-path locality, 884 changed ANM bytes, and 3,087 changed ALL bytes.
- Ran matched hardware Direct3D Training arms through `NextLife` and captured
  15 same-size Gamescope frames per accepted arm.
- Rejected an earlier replacement launch that entered the default software
  path; it contributes no retained result.
- Retained two accepted game logs, run metadata, and a metadata-only comparison
  report. Screenshots and staged game bytes remain ignored under `work/`.
- Updated the experiment/resource/function/implementation notes, roadmap,
  state and unknown registers, decision log, session index, and relevant MOCs.

## Conclusions

- **Confirmed:** Both retained arms selected 640×480×16 Direct3D hardware,
  never entered `INITSOFTRENDER`, loaded both plant 04/10 paths, ended
  `InitMainGame`, and reached `NextLife`.
- **Confirmed:** The exact equal-size plant 10 `.ANM`/`.ALL` pair at the plant
  04 paths is accepted by the original executable in this run.
- **Confirmed within the tested visual procedure:** No stable start-camera
  difference is discriminated beyond independent control animation variance.
- **Unknown:** Later/off-camera/nonvisual effects, general pair compatibility,
  complete format semantics, and the direct M1 placement identity.

## Contradictions discovered

No format or runtime contradiction. The expected possibility of a visible
whole-pair identity substitution was not observed at the tested camera. The
software-path false start reinforces the existing renderer log gate and was
discarded rather than normalized into the accepted result.

## Tests run

- Exact SHA-256/size checks for the executable and four plant inputs.
- Recursive control/source and replacement/source comparisons.
- Exact `cmp` proof for both staged destinations and byte-difference spans.
- Hardware log gate plus `InitMainGame`/`NextLife` checks for both retained
  arms.
- Normalized log diff: byte-identical after drive-label/timing normalization.
- 15-frame PipeWire capture per arm; exact 640×480 point normalization;
  all-pairs AE/RMSE; temporal medians; independent M2.5 control-median check.
- Repository validation is recorded after documentation closure.

## Unresolved questions

- Does suppressing the exact level-derived plant 04 selector omit both plant
  04 load requests as predicted?
- If gameplay remains reachable, does its stable visual mask overlap a known
  M1 placement mask?
- Which additional PC evidence can promote any overlap from candidate to a
  direct placement-to-resource identity?

## Recommended next action

Execute [[Project Roadmap#M2.7 — Plant 04 request suppression and visible-mask bridge]]
as a one-byte expected-value-guarded staged experiment.

## Git commit if applicable

Bounded commit message: `research: validate paired plant replacement`.
