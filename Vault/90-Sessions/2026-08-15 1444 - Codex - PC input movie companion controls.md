---
type: session
agent: Codex
date: 2026-08-15
status: complete
tags:
  - sessions/codex
  - cap-002
  - input-movies
---

# PC input movie companion controls

## Scope

Make CAP-002 recording convenient during a normal pristine windowed PC run,
without confusing the PS1-only DuckStation path with this repository's
authoritative Windows PC workflow. Preserve the Obsidian evidence trail, the
hash-pinned launcher, and repository hygiene.

## Implementation

Added `scripts/play-pristine-with-inputs.py` 1.0.0. The new entry point accepts
the familiar `--research --windowed --mute` invocation, starts the unchanged
`scripts/play-pristine.sh` in an isolated process session, and opens an
**ABLPC Input Recorder** Tk window. Its Recording menu and buttons provide:

- Choose Movie;
- Start Recording (`Ctrl+R`);
- Stop Recording (`F12`); and
- Close Game and Controls.

Discovery is limited to exactly one owned 640x480 `bugs.exe` window in the
isolated launch session and exact game work-copy directory. Output remains
create-only and confined below `work/copies/`. The companion delegates capture
to the existing strict `scripts/input-movie.py` implementation and does not
capture host/display-wide input or claim engine-frame synchronization.

The original `scripts/play-pristine.sh` remains byte-identical with SHA-256
`68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e`.

## Verification

- 11 companion-control fixture regressions pass.
- 22 combined companion/input-movie focused regressions pass.
- The complete repository gate passes 556 tests outside the workspace sandbox.
- The first sandboxed full run had seven GDB failures because ptrace yielded no
  stops; the same complete gate passed when rerun with the required ptrace
  permission. This was an environment restriction, not a product failure.
- No game, Wine, Gamescope, or Tk runtime was launched for this packet.

## Durable outcome

[[EXP-20260815-120 - PC input movie companion controls]] records the offline
fixture evidence and
[[Decision Log#DEC-20260815-114 - Keep the pinned launcher immutable and add companion input controls]]
records the isolation decision. CAP-002 remains partial and
[[Known Unknowns#KU-057]] remains open.

## Next action

Run `scripts/play-pristine-with-inputs.py --research --windowed --mute` for the
first live usability check. Then record the user-directed Level03 route and
retain the existing two-fresh-replay plus read-only state-trace gates.
