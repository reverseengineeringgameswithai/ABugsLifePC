---
type: session
date: 2026-08-12
agent: Codex
status: completed
tags:
  - session
  - re/dynamic
  - re/resources
---

# Character ALL visible link

## Agent

Codex

## Goal

Execute roadmap packet M2.20 under the START HERE workflow, determine whether
exact one-path `CHARS/FLICK.ALL <- CHARS3/FLICKD.ALL` is accepted and has a
repeated stable Training render outcome, preserve Obsidian evidence structure,
and leave Wine and Git state clean.

## Files inspected

- The full required START HERE sequence, Project Charter, Agent Operating
  Manual, roadmap packet, decision/unknown registers, relevant MOCs, PC content
  census, capability-gap register, and preceding M2.19 evidence.
- Exact derived PC files under `work/copies/BUGS_PC-full-disc/`, retained
  Training logs, `scripts/play-pristine.sh`, and the prior fixed-trajectory
  receipts/comparison method.
- No file under `originals/` was modified. No PS1 source was opened or used.

## Experiments inspected

- [[EXP-20260812-014 - PC content census and loader context]]
- [[EXP-20260812-032 - Fixed trajectory paired plant replacement]]
- [[EXP-20260812-033 - Character ALL replacement visible outcome]]

## Changes made

- Built fresh ignored unchanged/replacement/unchanged trees. The replacement
  changed only `PC/BUGS/CD/CHARS/FLICK.ALL` to exact equal-size
  `CHARS3/FLICKD.ALL`; both companion `.ANM` inputs remained byte-identical.
- Verified the executable, resource hashes, 2,115-byte difference census,
  recursive control equality, and one-path staging locality before launch.
- Recorded accepted hardware runs `RUN-WINE-20260812-230859`,
  `RUN-WINE-20260812-231216`, and `RUN-WINE-20260812-231403`. Every complete
  log proves 640x480x16 Direct3D, exact `FLICK.ANM/.ALL` loads,
  `End InitMainGame`, and `NextLife`, with no `INITSOFTRENDER`.
- Applied the same receipt-bearing 12-frame Training trajectory to each arm.
  Captured only the isolated 640x480 Gamescope surface; all PNGs/masks remain
  ignored under `work/copies/EXP-20260812-033/`.
- Compared normalized logs, same-index controls, temporal medians, and all 18
  replacement-to-control frame pairings at each anchor. Curated only logs,
  metadata, timestamps, hashes, metrics, and bounding boxes.
- Corrected the initial line-1474 interpretation: isolated surface evidence
  shows `Start ClearLoadScreen` is the natural Training title waiting for the
  start key, not a post-load fault. A distinct 954-line pre-resource attempt
  remains rejected and non-evidentiary.
- Restored Wine drive `R:` to the pristine derived tree, stopped the exact
  scoped processes/prefix server, and verified that no private mute sink
  remained.
- Added `EXP-20260812-033`, closed M2.20 positively, resolved KU-032 only at
  its visible boundary, added KU-033, recorded `DEC-20260812-028`, and made the
  exact character request/first-consumer trace M2.21. Updated Current State,
  roadmap, census, capability gaps, relevant MOCs, and this session index.

## Conclusions

- **Confirmed:** The exact one-path equal-size replacement is accepted by the
  unchanged executable and all accepted normalized logs are byte-identical.
- **Confirmed:** At all four anchors, the 18-way 5% grayscale intersection is
  confined to the input-controlled central figure: 689, 466, 89, and 532
  pixels in the recorded local boxes. This establishes the exact loaded-file-
  to-render link at the tested boundary.
- **Inferred:** The changed `.ALL` bytes likely affect resource data used to
  draw the figure. No model, texture, animation, or structure meaning is
  assigned.
- **Unknown:** Exact request origin, first format consumer/runtime destination,
  `.ALL` layout, general replacement compatibility, filename identity, and the
  M1 placement/payload bridge remain unresolved.

## New hypotheses

The selected `.ALL` path contributes data to the bounded central-figure render
region. M2.21 must trace the PC request and first consumer before narrowing
which resource component or layout could explain that contribution.

## Contradictions discovered

- The first line-1474 control attempt was stopped as a suspected post-load
  stall. The accepted retry plus isolated title capture disproves that
  classification; the experiment records it as an incomplete operator
  rejection rather than a game failure.
- Timestamped input did not keep the two later control trajectories globally
  phase-identical. This does not erase the positive local result because the
  intersection requires every replacement frame to differ from all six
  control frames at each anchor, but it keeps deterministic replay open.
- The repeated 5% local region largely disappears at 10%, so the demonstrated
  delta is bounded as moderate color/intensity change rather than described as
  an arbitrary-threshold invariant.

## Tests run

- Exact executable/resource hash, recursive staging-locality, load-line,
  renderer, `NextLife`, and no-software gates: passed for all accepted arms.
- Three run metadata JSON documents: parsed successfully with `jq`.
- Clock-normalized logs: byte-identical, SHA-256
  `f47d9d3d648f0d9c3a951ea0135fa4fed29a91089ba653e0dcaf13fbc97cad18`.
- `git diff --check`: passed.
- Final `make check`: dependency smoke imports, Vault lint (139 notes, zero
  errors or warnings), 130 tests, and tracked-file audit (zero violations)
  passed.
- Final runtime audit: no scoped game/Gamescope process or private mute sink
  remained; `R:` resolved to the pristine derived tree.

## Unresolved questions

- Which exact PC caller or data origin constructs/requests
  `CD/CHARS/FLICK.ALL`?
- What first format-specific consumer and runtime destination receive its
  loaded bytes?
- Can that path later be tied to a level record/payload without assigning
  semantics from filenames or reusing the plant runtime model?

## Recommended next action

Execute [[Project Roadmap#M2.21 — Character request and first-consumer trace]].
Start from existing PC static exports around `0x004AE240`; trace the exact path
backward to its request origin and forward only to the first bounded consumer/
destination. Use safe read-only runtime evidence only if static candidates
remain ambiguous, and do not parse `.ALL` fields in advance.

## Git commit if applicable

Bounded commit message: `research: link character asset to rendered outcome`.
