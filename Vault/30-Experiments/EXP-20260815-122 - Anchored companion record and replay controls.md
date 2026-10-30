---
type: experiment
id: EXP-20260815-122
date: 2026-08-15
question: Can the PC companion replace its ambiguous fixed delay with one explicit shared game-state anchor and a safe replay/lifecycle workflow?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Python 3.14.6; Tk 9.0; xdotool; offline synthetic fixture validation
environment_version: input-movie.py 1.1.0 2c7b3650d50a032f0e5ee2f83eba664171e46fa9089a0f394c6b2ca4e16281cc; companion 1.1.0 7997c53dffd39a02172df4e3a654ce73e8af2704d3a6a2e8f7be1ad704161918
working_directory: /home/dev/ABLPC
configuration: no game runtime launched; baseline commit 2333177425568adf6e7534e2600916f75aade60a; unchanged pinned pristine launcher; synthetic record/replay and Linux process-group fixtures
artifacts:
  - scripts/input-movie.py
  - scripts/play-pristine-with-inputs.py
  - tests/test_input_movie.py
  - tests/test_input_movie_controls.py
result: fixture-accepted-shared-anchor-companion-live-route-pending
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - implementation/tooling
  - input/replay
  - cap/CAP-002
---

# EXP-20260815-122 - Anchored companion record and replay controls

## Question

Can the corrective boundary from
[[EXP-20260815-121 - First companion route replay divergence]] be implemented
without changing the pinned launcher, widening exact-window input authority, or
claiming that accepted dispatch proves gameplay agreement?

## Boundary

- This is an implementation and synthetic-fixture packet. No game, Wine,
  Gamescope, private sink, or Tk window was launched for evidence.
- `scripts/play-pristine.sh` remains byte-identical at SHA-256
  `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e`.
- The authoritative target remains the retail Windows PC executable. No
  DuckStation, PS1 source, game-byte edit, debugger write, original asset, or
  input-movie payload is committed.
- The previous 306-event manual-delay movie and EXP-121 result remain
  immutable. This packet does not reinterpret their accepted dispatch as a
  successful route.

## Corrective design

Companion 1.1.0 makes `--- Start LevelSelect ---` the default recording
milestone. The user starts recording while the renderer selector is visible,
waits for **ARMED**, and then selects Hardware. Renderer selection is therefore
setup rather than movie content. Recording begins only when a newly appended
marker, exact focus, and neutral input agree. Manual delay remains a visible,
explicitly weaker radio choice.

The worker now exposes an optional inherited-descriptor NDJSON protocol with
three bounded events: `armed`, `recording-started`, and `replay-started`. The
companion derives **ARMED**, **RECORDING NOW**, and **REPLAYING NOW** from those
backend events instead of inferring readiness from a local countdown or child
process existence.

The new Replay menu validates a selected strict movie and reuses its recorded
anchor type. A log-anchored replay watches the movie's exact marker in new log
bytes. It also waits the movie's recorded `neutral_wait_ns` after that marker
before defining schedule zero; record and replay therefore share the same
post-marker zero-point definition. A manual-delay movie requires an explicit
warning before replay.

The UI separately labels the create-only **Next recording output** and stable
**Last saved** path. Active recording still stops by re-proving and sending F12
only to the exact game window. An armed recorder or replay stops through
SIGINT to its proved isolated process group.

Session cleanup now enumerates the retained process-group ID even when the
original launcher leader has exited, then applies bounded TERM/KILL cleanup to
that exact group. SIGINT and SIGTERM received by the Tk process request this
same cleanup path instead of raising through the polling callback.

## Fixture evidence

The focused suites pass 23/23 tests:

- default log-marker and explicit manual record command construction;
- log-anchored and manual-delay replay command construction;
- inherited-descriptor `armed` and start-event ordering for record/replay;
- new-log-byte-only marker matching;
- recorded post-marker neutral-wait preservation during replay;
- target/window/output confinement and no host/display-wide input authority;
- exact isolated worker cleanup and non-isolated-process refusal; and
- retained-group cleanup after the launcher leader exits while a child remains.

Machine-readable capabilities report the default marker, manual fallback,
supervisor events, replay backend, and distinct stop actions. Both scripts
compile. The complete `make check` gate passes 557 tests, Vault lint at 355
notes/zero errors/zero warnings, the five-anchor M4 compatibility statement,
and the tracked-file audit. `git diff --check` passes, and pre/post runtime
audits find no owned game, Wine, Gamescope, companion, input-movie, or
`ablpc_mute_*` residue.

## Result

**Confirmed by implementation and fixtures:** all five corrections required by
EXP-121 exist at the bounded worker/UI/lifecycle boundary. Record and replay
share one new PC-native log marker; readiness is explicit and backend-driven;
saved versus next output is unambiguous; replay is available from the same
window; and cleanup retains the exact group after leader exit.

**Not confirmed live by this packet:** `--- Start LevelSelect ---` was a
provisional route anchor at completion. No evidence in this packet shows that
it reproduces Training entry,
completion, Level03 contact, or KU-057 state. A fresh user record/replay must
visibly and log-independently verify the intended level load. Input receipt
acceptance alone remains insufficient, and monotonic offsets remain distinct
from engine frames.

## Live follow-up

[[EXP-20260815-123 - Level Select anchored route gameplay desynchronization]]
accepts the marker for Hardware/Training entry but rejects it as a complete
gameplay-route anchor: 300/300 events dispatch and Training loads, then the user
observes later desynchronization. This preserves the fixture claims above while
retiring the provisional long-route interpretation.

## Links

- Design contract: [[PC input movies#Convenient companion window]]
- Decision: [[Decision Log#DEC-20260815-115 - Default companion routes to a shared PC log milestone]]
- Capability register:
  [[Reverse Engineering Capability Gaps#CAP-002 — Deterministic PC input movies]]
