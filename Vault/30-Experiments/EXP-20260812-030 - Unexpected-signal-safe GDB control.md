---
type: experiment
id: EXP-20260812-030
date: 2026-08-12
question: Can the read-only GDB harness surface fatal target signals without continuing them and independently prove post-detach survival?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, native GDB fixtures, Wine, windowed muted Gamescope
environment_version: python-3.14.6; gdb-17.1-6.fc44; wine-11.0-staging; gamescope-3.16.25-1.fc44
working_directory: /home/dev/ABLPC
configuration: gdb-harness 1.1.0; result schema 2; backward-compatible watch-spec schemas 1 and 2; schema-2 required survival receipt
artifacts:
  - scripts/gdb-harness.py
  - scripts/evidence_lib.py
  - tests/test_gdb_harness.py
  - tests/test_evidence_lib.py
  - dynamic/wine/RUN-GDB-20260812-214545/metadata.json
  - dynamic/wine/RUN-GDB-20260812-214545/result.json
  - dynamic/wine/RUN-GDB-20260812-214545/stops.jsonl
  - dynamic/wine/RUN-GDB-20260812-214545/debugger-evidence.txt
  - dynamic/wine/RUN-GDB-20260812-214545/curation.txt
  - dynamic/wine/RUN-GDB-20260812-214545/bugs.log
addresses:
  - 0x00444C58
  - 0x00444D0C
  - 0x00445089
  - 0x00445973
  - 0x005B1AA4
  - 0x006C342B
result: fatal-signal-structured-no-pass-survival-receipt-proven-safe-live-control-passes
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - implementation/tooling
---

# EXP-20260812-030 - Unexpected-signal-safe GDB control

## Question

Can the read-only GDB harness terminate and report an unexpected fatal target
signal without blindly continuing it, fail closed when required survival is
absent, and still preserve the previously safe Wine hardware-watchpoint path?

## Inputs and authority

- Exact unchanged PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Incident evidence [[EXP-20260812-029 - Fresh selected-entry chain debugger fault]]:
  raw `SIGSEGV` at `0x0044D79A` was hidden by schema-1's broad signal continue.
- Prior safe live control `RUN-GDB-20260812-182412`: four exact access stops
  on plant 10 slot `0x005B1AA4`, including value `0x006C342B`.
- M2.17 contract in [[Project Roadmap#M2.17 — Unexpected-signal-safe debugger control]].

No executable byte, game memory, register, or game file was modified. No PS1
source or finding was consulted. Fixture target signaling is synthetic and
confers no game semantics. Live captures targeted only the isolated Gamescope
game surface, never the desktop or whole screen, and remain ignored under
`work/copies/EXP-20260812-030/evidence/`.

## Expected discriminator

- A synthetic `SIGSEGV` after attach must produce structured terminal reason
  `target_signal`, signal name and PC, no further continue, cleanup/detach, and
  a live resumed/untraced fixture when `nopass` safely suppresses that injected
  signal.
- A required failed survival probe must force `accepted == false` even when the
  primary debugger window otherwise completed.
- Existing timeout, milestone, hardware-watchpoint, and routine Wine-style
  `SIGUSR1` cases must remain green.
- A live run on previously safe slot `0x005B1AA4` must reproduce prior stops,
  contain no target signal, pass a required independent receipt, and retain a
  live game-only endpoint.

## Implementation

`gdb-harness` 1.1.0 emits result schema 2 and continues to accept strict watch-
spec schema 1. Watch-spec schema 2 adds an optional bounded `survival` object:

- required/optional acceptance;
- settle delay, sample count, and sample interval, capped to 30 seconds total;
- repeated target identity, `/proc` state, and `TracerPid` checks;
- configurable requirements that the process be resumed and untraced.

Fatal signals `SIGSEGV`, `SIGILL`, `SIGBUS`, `SIGFPE`, `SIGABRT`, and `SIGSYS`
are configured `stop print nopass`. Any non-allowlisted signal stop is terminal
and recorded as `target_signal`; routine Wine `SIGUSR1/SIGUSR2` remain the only
explicit pass-through signals. Signal inspection precedes a concurrently
observed log milestone, closing the exact M2.16 false-success race.

The CLI gathers the survival receipt only after the controller has deleted its
hardware points, detached, and exited. A required failed receipt changes an
otherwise completed result to `survival_failed`, retains its primary stop
reason, and forces both `completed` and `accepted` false.

## Procedure

1. Extend the synthetic sentinel fixture with a trigger-file-controlled
   `raise(SIGSEGV)` path. Start the harness, wait until `/proc` proves GDB is
   attached, then create the trigger.
2. Assert structured signal name/classification/PC and `stop-print-nopass`,
   hardware-point cleanup, detach, a passing three-sample survival receipt,
   and continued fixture life.
3. Preserve the routine `SIGUSR1`, timeout, milestone, max-stop, ownership,
   read-only allowlist, and schema-1 regressions. Add schema-2 validation and
   a real exited-process survival failure.
4. Launch the unchanged game with
   `scripts/play-pristine.sh --research --windowed --mute`. Reject the first
   preflight after its complete log shows `INITSOFTRENDER`.
5. Relaunch, target only its isolated window, send Down and Return separately,
   and accept only exact 640x480x16 Direct3D markers with no `INITSOFTRENDER`.
6. At the Training selector, attach `RUN-GDB-20260812-214545` to previously
   safe access watch `0x005B1AA4`, then select Training. Require `NextLife`,
   deletion/detach, the schema-2 survival receipt, and a game-only live frame.
7. Stop only the resolved launcher/game/Gamescope process tree and verify the
   private audio sink unloads.

## Observed

### Synthetic fatal-signal and survival controls

The focused fixture/schema suite passes 59 tests. The fatal fixture raises
`SIGSEGV` only after its `TracerPid` proves GDB attached. The harness returns tool-
negative with `stop_reason == target_signal`, `completed == false`, and
`accepted == false`; it records fatal classification, a non-null PC, and
`stop-print-nopass`. Its point is deleted, detach succeeds, and three post-
detach samples find the fixture resumed with `TracerPid == 0` and still alive.

A real exited fixture fails identity and `/proc` sampling. Applying that
required receipt changes primary `timeout` into `survival_failed` and forces
`completed/accepted == false`. The existing Wine-style `SIGUSR1` fixture still
reaches its normal max-stop bound.

### Accepted safe live control

`RUN-GDB-20260812-214545` spans
2026-08-12T21:45:45.328435-04:00 through
2026-08-12T21:46:11.163568-04:00. It records the same four PCs and values as
prior safe `RUN-GDB-20260812-182412`:

| Sequence | PC | Slot bytes |
|---:|---:|---:|
| 1 | `0x00445089` | `00000000` |
| 2 | `0x00444C58` | `00000000` |
| 3 | `0x00444D0C` | `2b346c00` |
| 4 | `0x00445973` | `2b346c00` |

The third/fourth bytes decode little-endian to exact prior plant 10 pointer
`0x006C342B`. The run reports `target_reached`, no target signal, its one point
deleted, cleanup verified, detached, completed, and accepted.

The independent receipt begins after detach. It re-verifies the executable
identity and records five samples from 21:46:11.724632 through 21:46:12.525318,
all process state `R`, `TracerPid == 0`, and passed. A separate isolated game-
surface frame at 21:46:27.652686791, SHA-256
`cbb437fea77643a7989ee26ee121dcf1c0342603fc24c1ade85250af31fd7062`,
visually shows live Training gameplay.

The committed log, SHA-256
`8b331970c547406864ce26d1afee9367683cf34b62b39bd379206fa6ffcfd500`,
contains the hardware Direct3D gates, no `INITSOFTRENDER`, both plant10
requests, `End InitMainGame`, and `NextLife`. During execution, the game's sink
input was routed to the private mute sink; it unloaded during scoped cleanup.

## Confirmed

- Fatal target signals are no longer blindly continued or hidden by a
  concurrent log milestone; they produce a structured terminal signal/PC.
- `nopass` plus harness cleanup/detach safely preserves the synthetic injected-
  signal fixture, proven by independent resumed/untraced samples.
- A required failed survival receipt cannot be accepted.
- Schema-1 specs remain accepted; schema 2 adds a strict bounded receipt.
- The previously safe real-game watchpoint retains its exact four-stop/value
  behavior under hardware Direct3D and passes both machine-readable and visual
  post-detach survival evidence.

## Inferred

The harness false-success mechanism from M2.16 is resolved at the tested
fixture/live-control boundaries. This makes another bounded investigation of
the faulting caller region safe to conduct, but does not make that region's
hardware-breakpoint continuation itself safe or explain its fault.

## Unknown and limitations

- Root cause of the `0x0044D79A` same-PC fault remains unknown among exact-
  address hardware-breakpoint behavior, native GDB, Wine WoW64 continuation,
  or another condition.
- `/proc` identity/state/tracer sampling proves existence, resumed state, and
  absence of a tracer during its bounded interval; it is not proof of future
  gameplay correctness or progress at every game subsystem.
- Staged phases, predicates, and register-relative memory expressions remain
  unimplemented CAP-001 work.

## Contradictions and negative results

The first live preflight entered software rendering without the required early
input and was rejected. It supplies no live-control evidence. No contradiction
occurred in the accepted hardware arm: structured status, five `/proc` samples,
the exact prior watch sequence, complete log, and live game-only frame agree. A
final process audit found a sleeping `gamescopereaper` plus `winedevice.exe`
from the rejected preflight; exact command-line/PID verification and scoped
termination removed both. No game, debugger, scoped wrapper, or private sink
remained.

## Result

M2.17 is complete. The blocking fatal-signal/survival subset of CAP-001 is
resolved at synthetic and safe-live boundaries; the broader staged-capture gap
remains open. KU-031 narrows to the origin of the exact caller-gate fault, not
structured-status trustworthiness. Full `make check` passes 130 tests, Vault
lint on 133 notes, and the tracked-file audit with no violations.

## Follow-up

Execute [[Project Roadmap#M2.18 — Adjacent caller-gate continuation discriminator]].
Use fresh matched hardware runs and the required schema-2 receipt to compare a
hardware breakpoint at a nearby instruction proven on the same natural path
against exact faulting PC `0x0044D79A`. Treat any `target_signal` as the end of
that arm and do not infer callee/data behavior beyond it.
