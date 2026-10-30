---
type: experiment
id: EXP-20260815-125
date: 2026-08-15
question: Does persistent exact-window XTEST delivery remove the immutable Training movie's desynchronization, and what evidence boundary remains if it does not?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11.0; Gamescope; input-movie.py 1.2.0 live backend, followed by 1.3.0 checkpoint/default-anchor hardening
environment_version: live input-movie.py ff4549f914325561c841dfc633fbafced1ec2c7955d03e0b77a62ffa163b71eb; final input-movie.py ad1250b3570909781bc97eb89e20d158874b3bee3cf085c9326d79edb67536d0; final companion cdbb8f73504c368fa231df4a1d7bc1389887605cd9fb6a403de92fc23204e356
working_directory: /home/dev/ABLPC
configuration: pristine PC work copy; research/windowed/muted; fresh Level Select arms; immutable 300-event Training movie; persistent X11/XTEST sender; mandatory exact-window XSelectInput echo
artifacts:
  - dynamic/wine/RUN-INP-REP-20260815-165621/metadata.json
  - dynamic/wine/RUN-INP-REP-20260815-165853/metadata.json
  - dynamic/wine/RUN-INP-REP-20260815-170119/metadata.json
result: exact-target-input-delivery-confirmed-but-fresh-gameplay-outcomes-still-diverge
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - implementation/tooling
  - input/replay
  - cap/CAP-002
---

# EXP-20260815-125 - Persistent echoed replay and residual gameplay divergence

## Question

Can the CAP-002 replay backend reproduce the immutable Training movie at the
actual PC game window without the event insertion and 15-39 ms distortion
measured in EXP-124? If target input becomes exact but gameplay still differs,
what must a safe future recording/replay contract prove separately?

## Inputs and implementation

The immutable source remained
`work/copies/input-movies/input-20260815-160751.input-movie.json`, SHA-256
`abc45db6a5822c6eeb5f56b045e237b7b8c9a84814de13ed0abf4f79deb17b91`.
It contains 300 normalized events over 54.331244586 seconds with schedule
SHA-256
`23e0dbc0f237199bcf3cc84d08a9d481ccf38213396a1ad60d637e2c9dd119ad`.
No movie event, game byte, original, work-copy asset, or PS1 source was edited.

`scripts/input-movie.py` replaced one focus subprocess plus one send subprocess
per event with one persistent X11/XTEST sender and a separate persistent
`XSelectInput` observer on the proved target window. Each event now requires an
exact echo of action, keysym, mapped keycode, keyboard modifier state, and
`send_event`, within a five-millisecond delivery-drift ceiling. The nested
Xwayland global auto-repeat is disabled only for replay and restored on every
exit. Preparatory unmatched XTEST releases are retained as normalization
metadata; any other extra event fails closed. Focus, executable, process,
window, schedule, cleanup, and create-only boundaries remain unchanged.

## Fail-closed interference arm

`RUN-INP-REP-20260815-165621` rejected after 235/300 exact deliveries when the
observer received an unexpected `Super_L` down at source-relative offset
41.683040589 seconds. The receipt records reason `unexpected_target_event`,
maximum request drift 321,312 ns, maximum delivered drift 512,942 ns, restored
auto-repeat, and all keys released. This arm is not a replay failure to hide:
it demonstrates that unrelated target-window input is not silently folded into
an accepted movie.

## Two accepted exact-delivery arms

Fresh arms `RUN-INP-REP-20260815-165853` and
`RUN-INP-REP-20260815-170119` each dispatched and observed exactly 300/300
events. Both report `target_echo_verified: true`, 150 normalized preparatory
releases, balanced target state before cleanup, all keys released, XTEST 2.2,
and auto-repeat restored. Their maximum request/delivery drifts were:

| Run | Request drift | Target delivery drift |
| --- | ---: | ---: |
| `RUN-INP-REP-20260815-165853` | 342,932 ns | 457,552 ns |
| `RUN-INP-REP-20260815-170119` | 427,423 ns | 519,113 ns |

The version-1.2.0 input-only receipt comparison agreed on the immutable movie/
schedule, anchor, target signature, complete dispatch, complete exact echo,
and key cleanup. Version 1.3.0 now correctly rejects this historical pair as
overall agreement because neither old receipt has a runtime-log checkpoint.
This closes the specific delivered-stream defect established by EXP-124 for
these two arms without retroactively claiming game-state or engine-frame
agreement.

## Runtime result contradicts deterministic gameplay

The first accepted arm passed the Hardware/Direct3D and Training-load gates
and a live log audit observed a later second
`--- Start LevelSelect ---`, consistent with completing and leaving Training.
The second accepted arm passed the same Hardware/Direct3D and Training-load
gates but remained inside Training after the movie plus an eight-second
observation interval. Its retained fresh `bugs.log`, SHA-256
`a8770f1985c471a0493d8da0b3030c4301d795e4ddaf136138b63a1ca76abd45`,
ends after initial `NextLife.` and contains no second Level Select marker. A
bounded screenshot captured Flik standing in the lower trench; that derived
game image remains ignored under `work/` and is not committed.

Therefore exact target-window input delivery is necessary but not sufficient
for deterministic PC gameplay. The two fresh arms agree on every input event
and sub-millisecond delivery timing yet disagree on the reached game state.
The current evidence does not identify whether the remaining cause is
record-versus-replay phase, internal frame sampling, simulation timing, or
another nondeterministic engine/runtime input. It must not be silently labeled
as one of those mechanisms.

## Contract hardening after the discriminator

Version 1.3.0 makes the first newly appended `NextLife.` after level
initialization the companion's recommended/default **Gameplay** anchor. The
user arms before Hardware, selects Hardware and the level as setup, and begins
route input only after **RECORDING NOW**. The older Level Select choice remains
available and is labeled **menu only**; old movies replay from their stored
anchor unchanged.

Schema 2 stores the new log-anchored recording's bounded raw post-anchor
`bugs.log` and normalized `ROUTINE` digests/trace in the movie itself. Replay
captures the corresponding runtime segment and automatically refuses a digest
mismatch. Receipt comparison also fails when exact input delivery or runtime-
log checkpoint digests differ. Schema-1 movies remain readable and unchanged.
This is a state-agreement detector, not a claim that the trace is complete
engine state. The existing immutable movie cannot be safely converted to a
`NextLife` movie because its original record-time phase at that marker was not
measured; a new user recording is required.

Focused input-movie and companion coverage passes 27 tests; the canonical
repository suite passes 561. Vault and hygiene gates are recorded in the
linked session note.

## Boundary and next discriminator

CAP-002 remains partial. The corrected backend is accepted for exact target-
window keyboard delivery, but long gameplay requires a fresh `NextLife`-
anchored user movie, two accepted replay receipts, matching runtime-log
checkpoints, and the task-specific read-only game-state trace. Monotonic
nanoseconds remain host scheduling offsets, not engine frames. Controller
input and atomic per-frame game state remain unsupported.

`rr` remains complementary whole-process evidence, not a replacement for
these input/state receipts. `/dev/ntsync` was not altered in this experiment;
the existing explicit module-removal authorization boundary remains in force.

## Lifecycle

All three exact launcher groups, game/Wine/Gamescope processes, input workers,
and private sinks were closed. Each retained Wine device process was handled
by exact PID after its owned session ended; the final process and sink audit
was clear.

## Links

- Prior defect: [[EXP-20260815-124 - Replay echo identifies target input stream distortion]]
- Contract: [[PC input movies]]
- Capability register: [[Reverse Engineering Capability Gaps#CAP-002 — Deterministic PC input movies]]
- Open route semantics: [[Known Unknowns#KU-057]]
