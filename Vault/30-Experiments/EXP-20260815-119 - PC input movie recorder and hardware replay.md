---
type: experiment
id: EXP-20260815-119
date: 2026-08-15
question: Can exact-window PC keyboard input be safely recorded and replayed with fresh hash-gated agreement?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11 Staging; Gamescope internal Xwayland; libX11; xdotool
environment_version: Python 3.14.6; input-movie 1.0.0; implementation a168485131bc54e7c8bdff5cf43f0be17310f0fed77d75d5cb32d3d538ebbeee
working_directory: /home/dev/ABLPC
configuration: one production record and two fresh muted/windowed Direct3D replays of the retail PC executable
artifacts:
  - dynamic/wine/RUN-INP-REC-20260815-125142/metadata.json
  - dynamic/wine/RUN-INP-REC-20260815-125142/hardware-selector.input-movie.json
  - dynamic/wine/RUN-INP-REP-20260815-125230/metadata.json
  - dynamic/wine/RUN-INP-REP-20260815-125312/metadata.json
result: cap-002-partial-exact-window-keyboard-replay-accepted
created: 2026-08-15
updated: 2026-08-15
tags:
  - experiment/runtime
  - tooling/input-replay
  - cap/CAP-002
---

# EXP-20260815-119 - PC input movie recorder and hardware replay

## Question

Can CAP-002 safely record keyboard events from only the verified Gamescope PC
game window, preserve explicit press/release timing in a hash-gated movie, and
replay the same movie in two fresh unchanged-PC hardware-selection arms with
machine-readable agreement?

## Boundaries

- Authority is the retail Windows PC executable at SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- The game ran from
  `work/copies/BUGS_PC-full-disc/PC/BUGS`; `originals/` was not read or
  modified during runtime work.
- `scripts/input-movie.py` 1.0.0 was used at implementation SHA-256
  `a168485131bc54e7c8bdff5cf43f0be17310f0fed77d75d5cb32d3d538ebbeee`.
- Record observes `KeyPress`/`KeyRelease` through `XSelectInput` on one exact
  internal Gamescope X11 window. It does not use DuckStation, `/dev/input`,
  XRecord, or a display-wide/host keyboard hook.
- Replay can emit only exact-window `xdotool` keydown/keyup events after
  process, executable, window-owner, process-group, class, geometry, and focus
  checks. Every held key is released on every exit path.
- This packet tests the opening hardware selector only. It does not claim a
  Level03 gameplay route, controller/gamepad support, log-anchored live event,
  or internal game-frame synchronization.

## Fixture gate

`tests/test_input_movie.py` supplies 11 asset-free cases. They cover exact
capability scope, strict hash-gated record/validate, the XTEST preparatory
release normalization observed live, empty/unpaired movie refusal, synthetic
replay refusal, emergency release on focus loss, new-log-byte-only anchoring,
window process-group mismatch, frame-hash mismatch, accepted replay dispatch,
and rejection of comparison with fewer than two receipts. The focused suite
passed 11/11 before live work.

Final `make check` passed all 545 tests, Vault
lint over 349 notes with zero errors/warnings, the exact five-anchor M4
compatibility check, tracked-file audit, and diff checks. The test target now
sets the repository's `reimplementation/` package path explicitly so the gate
is reproducible from a clean shell.

## Live recording

One fresh muted/windowed research arm used process group `547629`, game PID
`547872`, internal display `:2`, and focused 640×480 window `14680071`. The
movie captured Down and Return with explicit holds:

| Sequence | Offset ns | Action | Keysym |
| ---: | ---: | --- | --- |
| 0 | 6,172,407,829 | down | Down |
| 1 | 6,393,734,263 | up | Down |
| 2 | 7,414,543,707 | down | Return |
| 3 | 7,630,724,996 | up | Return |

The recorder normalized two unmatched preparatory release events emitted by
the live XTEST path. They remain in receipt metadata and were not promoted
into the replay schedule. The accepted 12.004-second movie is committed as
`dynamic/wine/RUN-INP-REC-20260815-125142/hardware-selector.input-movie.json`:

- movie SHA-256:
  `07b5c3516b86d72add02639a12bb52781848d8b7d890f1b811311eee324b28c8`
- canonical schedule SHA-256:
  `f2caa3e98a147f6a58fded45827d4c2ddff88980150a3cecc5ddba6688187247`
- record metadata SHA-256:
  `ae49e3079b334915b9de3ede1c7e54ad9a92873b0afc46e39433ec85803d25b4`

The complete 954-line `bugs.log` passed the required hardware gates at lines
74, 75, 76, and 127 and contained no `INITSOFTRENDER`; its SHA-256 was
`773430683b0b78e8aee07d8b0b51029ed68181fb157fb89ac344c48ba56ef62c`.

## Fresh replay controls

The record arm was closed before each replay. Both new arms used the same
retail executable/work copy and stable window signature but distinct process
groups and game PIDs:

| Run | PGID | game PID | Events | Max absolute drift | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| `RUN-INP-REP-20260815-125230` | 548156 | 548399 | 4/4 | 1,609,762 ns | accepted |
| `RUN-INP-REP-20260815-125312` | 548572 | 548815 | 4/4 | 1,781,163 ns | accepted |

Both receipts report the exact implementation/movie/schedule hashes, all four
events dispatched, all keys released, an unchanged stable window signature,
and no failure. Their metadata SHA-256 values are respectively
`6b1737a80c76954238d683395d712170e39a21b37860896cce9a6c15e62bc24d`
and
`99bf34012bce110c882d5022f687ad9822cdd158962a55d9ad8a734c8eb664cd`.
`input-movie.py compare` returned `agreement: true` with no reasons.

Each replay's complete 954-line log passed all four hardware markers and no
software marker. Replay A's log SHA-256 was
`ce0f292cf10302e3fc473b588bca84f1f423021b3c6210103c88efc2c570d4ca`;
replay B's was
`684625f1edc5c249ec5ca931fcca6eac4ede7215d551be83863031eab4db243c`.

## Result

**Confirmed at this boundary:** production recording is scoped to one verified
PC game window; movie validation is strict and executable-hash gated; explicit
Down/Return press/releases replay with bounded monotonic timing in two fresh
process groups; receipt comparison agrees; and all three arms enter the
hardware Direct3D path without a held-key leak.

**Not established:** an input movie is not an engine-frame movie. Manual-delay
timing can still diverge in longer animated/gameplay sequences. The log anchor
and optional frame-hash checks have fixture coverage but were not live-
validated here. No user Level03 route, deliberate material-1 contact, or
read-only KU-057 state trace was recorded. CAP-002 is therefore partially
resolved, not closed.

## Lifecycle and evidence

Each owned game/Gamescope process group was closed before the next arm. The
private mute sink was absent after each scoped cleanup, and the final audit
found no live owned game or Gamescope process.

- Tool contract and use: [[PC input movies]]
- Capability register: [[Reverse Engineering Capability Gaps#CAP-002 — Deterministic PC input movies]]
- Open gameplay question: [[Known Unknowns#KU-057]]
- Record receipt:
  `dynamic/wine/RUN-INP-REC-20260815-125142/metadata.json`
- Replay receipts:
  `dynamic/wine/RUN-INP-REP-20260815-125230/metadata.json` and
  `dynamic/wine/RUN-INP-REP-20260815-125312/metadata.json`
- Ignored working evidence: `work/copies/EXP-CAP-002/` and the current
  work-copy `bugs.log`
