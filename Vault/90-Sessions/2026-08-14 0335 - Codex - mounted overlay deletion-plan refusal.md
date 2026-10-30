---
type: session
date: 2026-08-14
agent: Codex
status: completed
tags:
  - session
  - implementation/modding
  - implementation/manifest
---

# Mounted overlay deletion-plan refusal

## Goal

Execute exact corrective packet M4.11 after James rejected M4.9, close only the
pre-existing bind-mounted deletion-plan defect, retain all ordinary and local
M4 baselines, update the durable Vault, and leave one clean worker commit for
fresh-context M4.12 review.

## Startup and scope

After M4.10 `REJECT`, read the complete [[START HERE]] chain: full
[[Current State]], full [[Project Roadmap]], full [[Environment Status]], full
[[Decision Log]], full [[Known Unknowns]], relevant implementation/experiment/
reverse-engineering MOCs, [[Agent Operating Manual]], and [[Project Charter]].
Also read `EXP-20260814-068/069`, [[M4 Exact Whole-file Replacement]],
[[M1 Tool Support Matrix]], the M4.9/M4.10 sessions, both READMEs, and the full
manifest/CLI implementation before acting. M2 remained deferred; no game
runtime, original, or external PS1 source was consulted or modified.

## Work performed

- Factored the complete expected overlay directory set before removal
  validation.
- Added a removal-only `/proc/self/mountinfo` reader with fail-closed parsing
  and kernel octal path decoding.
- Checked the overlay root, necessary directories, recorded outputs, and fixed
  receipt against current mountpoints before overlay traversal or unlink.
- Added an asset-free isolated helper and four private user/mount-namespace
  regressions for root, intermediate, output, and receipt bind mounts.
- Proved byte/type/link-complete overlay/source/independent-target snapshot
  equality after every refusal, including live `\040` path decoding.
- Re-ran ordinary manifest/removal, focused/full, and all six exact local
  apply/remove gates with established deterministic hashes.
- Updated roadmap, state, unknown, decision, implementation/M1 notes, MOCs,
  READMEs, experiment, and session surfaces for exact M4.12.

## Evidence and validation

- [[EXP-20260814-070 - Mounted sparse-overlay deletion-plan path refusal]]
- Isolated mounted paths: 4/4 refused unchanged.
- Manifest tests: 84/84.
- Focused manifest/LEVEL suite: 99/99.
- Complete canonical suite before documentation: 287/287.
- Final `make check`: 287/287; Vault lint 233 notes with 0 errors/warnings;
  tracked-file audit 0 violations; diff checks passed.
- Exact local apply/remove: 2/2 for each of opaque, same-DAT composed, and
  M1-plus-opaque composed families; source hashes unchanged.
- Executable SHA-256 reconfirmed as
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`;
  it was not read for analysis, launched, or modified.
- No game byte, mount artifact, receipt, temporary manifest, or local output
  was added to Git.

One first local harness stopped after an incorrectly transcribed expected
same-DAT output digest. Its disposable output was removed automatically and
source hashes remained unchanged. A fresh apply supplied the exact digest;
the corrected complete six-cycle run then passed. The stopped run is disclosed
in `EXP-20260814-070` and is not counted as evidence.

## Conclusion

M4.11 is worker-complete at the exact Linux pre-existing mounted-plan-path
boundary, not independently accepted. Exact fresh-context M4.12 hard-truth
review is the sole next packet. Broader platform compatibility, concurrent
races, transactions, unmounting, staged/source deletion, dry-run, launch,
N-way composition, `.ALL`, runtime, M2, and PS1 remain outside scope.

## Git commit if applicable

Intentional worker commit: `fix: reject mounted overlay removal paths`.
