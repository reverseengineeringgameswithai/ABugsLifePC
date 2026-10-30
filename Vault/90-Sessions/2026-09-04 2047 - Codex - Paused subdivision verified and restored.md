---
type: session
date: 2026-09-04
agent: Codex
status: complete-original-restored-user-game-paused
---

# 2026-09-04 2047 - Codex - Paused subdivision verified and restored

The user explicitly authorized the prepared in-place mesh comparison and
restoration. [[EXP-20260904-010 - Paused subdivision live comparison]] completes
both1,078-byte writes at`0x006662A7` with exact comparisons and readback. The
same game stays paused; no input or restart loses the user's failure pose.

Before each write, a brief owned-process stop and read-only register inspection
require the frame-limiter return chain after terrain rendering. The helper
passed a disposable-child lifecycle check and three recorded positive/three
corrupted-return negative checks.18 total stops include five exploratory probes
and13 transaction stops; only two write. No breakpoint or register modification.
The longest stop context is3.578ms. Final ptrace detachment and resumed thread
states are verified.

Three before/finer/restored captures each match the same measured player,
contact and camera state. All255 previously identified depth-inversion sample
pixels cease being blue with the finer mesh and return on restoration. The
complete3,575-pixel comparison ROI returns exactly. Six other analytic boundary
samples remain blue. This proves a bounded rendering improvement and supports
EXP-009's depth-interpolation explanation; it is not all-angle or complete
occlusion acceptance. Collision and dimensions are unchanged.

**Keep open/paused:** USER-20260904-deck-depth-play-001, game46701/1147812,
group46458, display`:2`, sink`ablpc_mute_46458`; position
`(163024,-102401,509900)`. The original zero-offset six-quad mesh is restored.
Final loaded-data checks pass; pre/post process/sink audits are identical and
accounted; TracerPid0; no stopped threads. The two-write authorization is used
for its reviewed comparison, not a permanent installation or another test.

Report24,881 bytes, SHA-256
`4faac2f866bbe034824ca953a1104f421c6744ebf20ad4a8d6b07ac713946a94`.
Interactive unaltered captures:
`work/experiments/EXP-20260904-010/comparison.html`.
Private assets/dumps stay in work; previous reports and user-stage files are
unchanged. No new production code, full make check, commit, independent audit,
R2q, PS1, mapping or save-state action. Updated Current State, Environment,
DEC-235, roadmap, KU-079/080, relevant research/experiment notes and MOCs.

Closing checks pass: python-doctor, vault-lint (0 errors; existing budget and
metadata warnings), M4 compatibility, tracked-file audit (0 violations), report
artifact hashes and diff whitespace. Claim sweep returns old0/new1, `new_only`.
Logs are in EXP-010's `checks.log` and `claim-sweep.json`; prior EXP-008/009
report hashes remain unchanged.
