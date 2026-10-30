---
type: experiment
id: EXP-20260815-123
date: 2026-08-15
question: Does the corrected Level Select anchored PC movie preserve the user's route through Training in a fresh pristine replay?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11.0; Gamescope; input-movie.py 1.1.0; companion 1.1.0
environment_version: input-movie.py 2c7b3650d50a032f0e5ee2f83eba664171e46fa9089a0f394c6b2ca4e16281cc; companion 7997c53dffd39a02172df4e3a654ce73e8af2704d3a6a2e8f7be1ad704161918
working_directory: /home/dev/ABLPC
configuration: pristine PC work copy; research/windowed/muted; fresh replay; disclosed exact-window Hardware setup before movie anchor
artifacts:
  - dynamic/wine/RUN-INP-REC-20260815-160815/metadata.json
  - dynamic/wine/RUN-INP-REP-20260815-161221/metadata.json
result: level-entry-reproduced-input-dispatch-accepted-later-gameplay-desynchronized
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - implementation/tooling
  - input/replay
  - cap/CAP-002
---

# EXP-20260815-123 - Level Select anchored route gameplay desynchronization

## Question

Does the first user movie recorded with the corrected shared Level Select
anchor reproduce its Training route in one fresh unchanged-PC replay?

## Inputs and boundary

- The new create-only movie is
  `work/copies/input-movies/input-20260815-160751.input-movie.json`, retained
  under ignored `work/` and not committed.
- Strict validation accepts schema 1, production backend
  `x11-window-select-v1`, 300 paired events, duration 54,331,244,586 ns,
  movie SHA-256
  `abc45db6a5822c6eeb5f56b045e237b7b8c9a84814de13ed0abf4f79deb17b91`,
  and schedule SHA-256
  `23e0dbc0f237199bcf3cc84d08a9d481ccf38213396a1ad60d637e2c9dd119ad`.
- `RUN-INP-REC-20260815-160815` accepts the recording with the exact marker
  `--- Start LevelSelect ---`, `start_offset: 2777`,
  `matched_offset: 30105`, and `neutral_wait_ns: 0`.
- The original recording session was closed through the corrected scoped
  signal path. A fresh companion/session was then launched. The replay worker
  was armed before renderer selection; one exact-window Down press and one
  Return press selected Hardware as disclosed setup outside the movie.
- No game/file/debugger mutation, host/display-wide input, PS1 evidence, or
  input-movie edit was used.

## Replay receipt

`RUN-INP-REP-20260815-161221` accepts:

- 300/300 events dispatched;
- exact movie and schedule hashes;
- all held keys released;
- maximum absolute dispatch drift 23,009,341 ns;
- no input-layer failure; and
- the same marker, start offset, matched offset, and zero neutral wait as the
  recording.

The fresh replay `bugs.log`, SHA-256
`ed79b01324f80fdf1507cbaa89b796d37e0e8ee1e9bc25c1872f06ac22439dc7`,
independently proves the correct startup branch:

- lines 74-76: native software mode false, Direct3D mode, and 640×480×16;
- line 127: Direct3D renderer started;
- line 669: `--- Start LevelSelect ---`;
- line 1093: `gfx\training.raw`, level 17;
- lines 1189-1192: `level07\level1.raw`, level 17; and
- line 1478: `NextLife` after `---End InitMainGame---`.

Thus the corrected marker resolves the earlier EXP-121 menu divergence: the
fresh replay enters the intended Training data and begins its gameplay state.

## Timing observation and contradiction

The immutable movie's first three press pairs are:

- Return at 3.129806090 s;
- Return at 5.101086261 s; and
- `z` at 6.498976937 s.

Only 1.337545224 seconds separate the second Return release and the first
gameplay-looking `z` press. The movie retains one uninterrupted Level Select
clock while the game destroys the menu state, loads `gfx\training.raw`, loads
`level07\level1.raw` plus data/assets, initializes the main game, and reaches
`NextLife`.

The user independently observed that playback “gets desynced.” The exact first
visible divergent event was not timestamped, so it remains unknown.

**Confirmed:** exact dispatch, Hardware mode, Level Select entry, Training
selection, Training data load, and the initial `NextLife` boundary all occur.
The later visible route does not stay synchronized.

**Superseded inference:** this packet originally proposed that the first
gameplay input's fixed delay across loading was the concrete mechanism. The
timestamped follow-up in
[[EXP-20260815-124 - Replay echo identifies target input stream distortion]]
measured the fresh replay's `NextLife` 953.942 ms before that `z`, so direct
loss of that key during loading is not supported. The original recording's
post-load phase remains unknown, but target-window echo now proves a separate
replay-delivery defect.

## Result and next discriminator

The Level Select marker is accepted only as a menu/level-entry anchor, not as a
complete gameplay-route synchronization point. CAP-002 remains partial and
KU-057 gains no gameplay-state evidence from this replay.

The immediate discriminator is no longer an anchor change. First correct and
echo-validate target delivery so the normalized sequence and close event
timing survive replay. Then use this immutable movie for an A/B rerun. A first
new `NextLife` anchor remains a later phase-control experiment if exact target
delivery still diverges.

## Lifecycle

Both companion sessions, their exact launcher groups, game/Wine/Gamescope
processes, input worker, and private `ablpc_mute_*` sinks were closed. The final
process/sink audit was clear. The complete repository gate passes 557 tests,
Vault lint at 357 notes/zero errors/zero warnings, the five-anchor M4
compatibility statement, and the tracked-file audit.

## Links

- Corrective worker packet:
  [[EXP-20260815-122 - Anchored companion record and replay controls]]
- Earlier menu divergence:
  [[EXP-20260815-121 - First companion route replay divergence]]
- Contract: [[PC input movies]]
- Capability register:
  [[Reverse Engineering Capability Gaps#CAP-002 — Deterministic PC input movies]]
