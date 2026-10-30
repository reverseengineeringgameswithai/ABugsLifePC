---
type: implementation
status: active
created: 2026-08-15
updated: 2026-10-02
tags:
  - implementation/tooling
  - re/dynamic
  - input/replay
---

# PC input movies

`scripts/input-movie.py` 1.3.0 records and replays keyboard events delivered
to one explicitly identified PC `bugs.exe` window inside Gamescope. It is the
bounded worker result for [[Reverse Engineering Capability Gaps#CAP-002 — Deterministic PC input movies]].
It is not DuckStation or PS1 tooling.

## Safety and identity boundary

Before recording or replay, the tool proves the live game PID, retail
executable SHA-256, work-copy working directory, exact X11 window owner,
window class and geometry, common process group, and focus. Production record
uses `XSelectInput` only on that target window. It does not open `/dev/input`,
use XRecord, observe the host desktop, or capture display-wide input. Replay
uses one persistent X11/XTEST sender and a separate `XSelectInput` observer on
the same explicit window, rechecks focus before every event, and accepts only
an exact action/keysym/keycode/modifier/`send_event` echo within the configured
delivery-drift ceiling. It disables nested-display auto-repeat only during
replay, restores it on every exit, and releases every held key after success,
refusal, focus loss, or interruption.

`make input-movie-caps` prints the machine-readable capability boundary. The
tool reports `internal_game_frame_synchronization: false`; monotonic wall-clock
offsets must not be described as engine frames.

## Convenient companion window

For normal interactive recording, use the companion launcher instead of
copying a PID, nested display, and window ID by hand:

```bash
scripts/play-pristine-with-inputs.py --research --windowed --mute
```

Add `--coordinates` to open the read-only translucent coordinate display
automatically after exact target discovery. It can also be toggled with the
**View → Show Coordinate Overlay** menu or matching button. See
[[PC coordinate overlay]]; coordinate sampling is independent of movie timing
and does not supply engine-frame synchronization.

`--windowed` is accepted for familiarity but is automatic. This command starts
the unchanged, hash-pinned `scripts/play-pristine.sh` in its own process
session and opens a small **ABLPC Input Recorder** desktop window. It is a
separate companion, not a menu injected into the game executable or Gamescope.

The companion waits for exactly one owned 640×480 `bugs.exe` surface, then
shows its PID, nested display, and window ID. Its **Recording**, **Replay**, and
**Session** menus and buttons provide:

- **Choose Movie…** — defaults to a new timestamped file under
  `work/copies/input-movies/` and refuses overwrite or paths outside
  `work/copies/`;
- **Start Recording** (`Ctrl+R`) — re-verifies the target and, by default,
  arms the strict gameplay recorder on the first newly appended `NextLife.`
  after level initialization;
- **Stop Recording** (`F12`) — sends F12 only to that verified game window;
- **Replay Movie…** (`Ctrl+P`) — validates a selected strict movie, uses its
  recorded anchor type, and delegates exact-window replay to the same worker;
- **Show Coordinate Overlay** — launches the exact-target read-only
  `process_vm_readv` display in a separate translucent window;
- **Close Game and Controls** — interrupts an owned recorder through its
  emergency-release path, closes the coordinate worker, and terminates only
  the isolated launcher session.

For the default workflow, choose **Start Recording** before selecting
**Hardware**, return focus to the game, select Hardware, then select the
desired level. The companion first displays **ARMED**, then displays a red
**RECORDING NOW** only after the new post-initialization `NextLife.` marker,
exact focus, and neutral-input gate agree. Begin gameplay only at that
transition. End with F12 in the game or the companion's Stop button. Replay
follows the same sequence: choose the movie before selecting Hardware, wait
for **REPLAY ARMED**, select Hardware and the same level, then do not add game
input after **REPLAYING NOW** appears.

The **Level Select (menu only)** radio choice remains available for menu/level-
entry movies and old movies replay from their stored anchor. It is not the
recommended long-gameplay boundary. The manual-delay radio option remains an
explicitly weaker fallback. Its delay is an arming interval, not recorded
input and not a game-state anchor. The UI names the create-only **Next
recording output** separately from the stable **Last saved** path.

### Evidence and remaining limitation

[[EXP-20260815-121 - First companion route replay divergence]] confirms that
live discovery and strict recording work, but rejects the earlier manual-delay
UI for a launch-to-gameplay route. Version 1.1.0 implements its required
correction packet in
[[EXP-20260815-122 - Anchored companion record and replay controls]]: shared
fresh-marker record/replay, explicit backend-driven readiness, saved/next path
separation, a replay menu, recorded post-marker neutral-wait preservation, and
cleanup of the retained isolated group after launcher-leader exit. These are
fixture-accepted implementation claims.

[[EXP-20260815-123 - Level Select anchored route gameplay desynchronization]]
then live-tests the marker. A fresh replay accepts 300/300 events, passes every
Hardware gate, and loads Training, so the marker is accepted for menu/level
entry. The user observes later gameplay desynchronization.

[[EXP-20260815-124 - Replay echo identifies target input stream distortion]]
supersedes the initial loading explanation. Timestamped replay evidence places
the first gameplay `z` about 954 ms after `NextLife`, while a simultaneous
production observer on the target window records 304 normalized events for
the 300-event source, two inserted `Right` up/down pairs, and several 15-39 ms
timing/hold changes. The replay receipt records `dispatched_ns` before its
synchronous `xdotool` send process, so accepted drift is not target-arrival
fidelity. Do not use this backend for complete long-gameplay synchronization.
Correct and echo-validate delivery before a post-load-anchor experiment.

[[EXP-20260815-125 - Persistent echoed replay and residual gameplay divergence]]
implements that correction. Two fresh arms each observe exactly 300/300 source
events below 0.52 ms maximum target-delivery drift and agree on the input
receipt, but one returns to Level Select while the other remains in Training.
This accepts the corrected emitter and rejects the stronger inference that
wall-clock-exact input alone yields deterministic gameplay. Version 1.3.0
therefore defaults new gameplay movies to `NextLife.` and captures a bounded
post-anchor raw-log segment plus normalized `ROUTINE` trace for every log-
anchored replay. `compare` fails if input delivery or either runtime-log digest
differs. The checkpoint detects state disagreement; it is not complete engine
state or internal-frame synchronization.

The immutable Level Select movie cannot be safely converted because its
record-time `NextLife` phase was not observed. Record a fresh movie at the new
default and require at least two exact-input plus runtime-checkpoint agreements
before using a long evidence route. Retain divergence rather than repairing it
with another fixed delay.

Automatic discovery is scoped by the new launcher's process group, exact game
working directory, retail executable hash, Wine ownership proof, class, and
640×480 geometry. It ignores the host `:0` display and the 1×1 Wine IME
surface. It does not weaken any [[#Safety and identity boundary]]. See
[[EXP-20260815-120 - PC input movie companion controls]].

The version-1.3.0 implementation hashes produced by EXP-125 are:

- `scripts/input-movie.py`:
  `ad1250b3570909781bc97eb89e20d158874b3bee3cf085c9326d79edb67536d0`;
- `scripts/play-pristine-with-inputs.py`:
  `cdbb8f73504c368fa231df4a1d7bc1389887605cd9fb6a403de92fc23204e356`.

EXP-127 changes only the companion to 1.4.0 for coordinate display; its
accepted hash is
`c3668646abb50018bd6ebe1b1fb3ffc358fe19c1141c9d84cdf12728f714dd41`.
The input-movie worker and its 1.3.0 hash above are unchanged.
Superseded the same day by [[EXP-20260815-128 - Live Flik position globals]]:
the current companion is 1.5.0 (`3c4e54d5…`, commit `bfd4f3b`);
[[PC coordinate overlay]] owns its hash. The worker is still 1.3.0 at the
hash above (checked 2026-10-02).

## Recording

Launch one fresh muted/windowed research instance, then identify the internal
Gamescope X display, focused 640×480 `bugs.exe` window, and game PID. Record to
a new path outside `originals/`:

```bash
.venv/bin/python scripts/input-movie.py record \
  --pid GAME_PID --window-id WINDOW_ID --display :N \
  --cwd-prefix /home/dev/ABLPC/work/copies/ \
  --movie /home/dev/ABLPC/work/copies/EXP-NAME/route.input-movie.json \
  --start-milestone 'NextLife.' \
  --log /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.log \
  --max-duration 900
```

F12 ends a recording by default and is omitted from the movie. Only bytes
appended after the arm begins can satisfy the log anchor. An optional
`--anchor-frame FILE` stores and later requires the exact independently
captured file hash. The output is create-only; an existing or linked final path
is refused. `--start-now --arm-delay 3` remains a manual fallback; those first
three seconds are deliberately outside the movie.

## Movie and replay contract

Schemas 1 and 2 preserve the executable hash, stable window signature,
recording backend, anchor receipt, ordered monotonic-nanosecond offsets,
explicit keydown/keyup pairs, keycodes and modifiers, duration, termination
reason, and a canonical schedule SHA-256. New schema-2 log-anchored movies also
bind the recording's bounded log-segment and `ROUTINE` trace digests; replay
refuses a mismatch automatically. Existing schema-1 movies remain readable
and unchanged. Validation rejects unknown keys, empty or unpaired event
streams, impossible counts/offsets, unsupported backends, checkpoint drift,
and schedule drift. Synthetic JSONL is fixture-only and replay-refused by
default.

Replay the immutable movie only in a fresh verified game arm:

```bash
.venv/bin/python scripts/input-movie.py replay \
  --pid GAME_PID --window-id WINDOW_ID --display :N \
  --cwd-prefix /home/dev/ABLPC/work/copies/ \
  --movie /path/to/route.input-movie.json --log /path/to/fresh/bugs.log
```

For a log-anchored movie, replay watches the movie's exact recorded marker and
reproduces its recorded post-marker neutral interval before the schedule zero
point. For a manual-delay movie, use `--arm-delay`; it remains vulnerable to
later game-state timing differences.

Each record/replay writes a JSON receipt under `dynamic/wine/RUN-INP-*` with
the implementation hash, ownership/window snapshots, movie and schedule
hashes, event count, request and target-delivery drift, exact echoed events,
auto-repeat restoration, held-key cleanup, and acceptance result. A log-
anchored replay also writes `runtime-log-segment.bin` and records its digest
plus the extracted `ROUTINE` trace/digest. Compare at least two fresh accepted
replays with:

```bash
.venv/bin/python scripts/input-movie.py compare \
  dynamic/wine/RUN-INP-REP-A/metadata.json \
  dynamic/wine/RUN-INP-REP-B/metadata.json
```

## Demonstrated boundary

[[EXP-20260815-119 - PC input movie recorder and hardware replay]] records a
four-event Down/Return hardware-selector movie from the unchanged retail PC
executable, then accepts it in two fresh process groups. Both replays dispatch
all four events, release all keys, remain below 1.8 ms maximum absolute
schedule drift, and pass the complete Direct3D/no-software log gate.

This proves bounded exact-window keyboard recording and replay at the opening
renderer selector. It does not prove a long Level03 route, controller/gamepad
recording, a live log-anchored gameplay event, atomic frame correlation, or
internal-frame determinism. CAP-002 therefore remains partially resolved, and
[[Known Unknowns#KU-057]] still needs the user route through deliberate
material-1 contact paired with the read-only state trace.

EXP-122 adds offline fixture acceptance for the anchored companion and status
protocol. EXP-123 live-accepts its menu/level-entry boundary but rejects a
complete gameplay-route claim. EXP-124 proves the former replay backend
transforms the target event stream. EXP-125 corrects that emitter and accepts
two fresh exact 300/300 deliveries, but their reached game states differ. CAP-
002 remains partial until a fresh `NextLife`-anchored user movie produces two
accepted input receipts, matching runtime-log checkpoints, and the intended
task-specific read-only state trace.

Companion 1.4.0 adds only the coordinate View/button and automatic
`--coordinates` option. [[EXP-20260815-127 - Read-only PC coordinate overlay]]
live-accepts the exact retail-process read and joined cleanup. It does not
change the input movie worker, replay contract, or CAP-002 status.
