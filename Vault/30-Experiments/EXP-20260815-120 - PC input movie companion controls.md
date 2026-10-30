---
type: experiment
id: EXP-20260815-120
date: 2026-08-15
question: Can PC input recording be exposed through a convenient companion menu without changing the pinned pristine launcher or weakening exact-window scope?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Python 3.14.6; Tk 9.0; xdotool; offline synthetic fixture validation
environment_version: companion 1.0.0 at 7ebcedebafe27ab54f8b55b85952269873492bb6ddcf35b29b67ef438e4ba3b7
working_directory: /home/dev/ABLPC
configuration: no game runtime launched; pinned pristine launcher retained byte-for-byte; GUI-independent command/discovery/path/process tests
artifacts:
  - scripts/play-pristine-with-inputs.py
  - tests/test_input_movie_controls.py
result: fixture-accepted-companion-workflow-live-user-route-pending
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - implementation/tooling
  - input/replay
  - cap/CAP-002
---

# EXP-20260815-120 - PC input movie companion controls

## Question

Can the already accepted PC input recorder be made convenient through a small
menu window while preserving the exact pristine launcher and CAP-002's
one-game-window authority boundary?

## Boundary

- This is an implementation/fixture packet. No game, Wine, Gamescope, private
  sink, or GUI session was launched for evidence.
- `scripts/play-pristine.sh` remains byte-for-byte unchanged at SHA-256
  `68c9171749bd7b207a15b4202193ccfddd2661fbb383deb34b1a5a5a4049977e`.
  Its completed M4 compatibility authority is not revised.
- New `scripts/play-pristine-with-inputs.py` 1.0.0 is SHA-256
  `7ebcedebafe27ab54f8b55b85952269873492bb6ddcf35b29b67ef438e4ba3b7`.
- The companion launches the pinned script with `--windowed` in a new process
  session. It does not inject a menu into `bugs.exe` or Gamescope.
- Production recording remains delegated to `scripts/input-movie.py` 1.0.0;
  no host-input, display-wide, controller, or internal-frame capability is
  added.

## Implemented workflow

The familiar invocation is:

```bash
scripts/play-pristine-with-inputs.py --research --windowed --mute
```

The Tk companion supplies Recording and Session menus plus visible buttons. It
automatically discovers only an Xwayland display in the isolated launch
process group, then selects exactly one 640×480 `bugs.exe` window whose PID,
process group, exact work-copy CWD, Wine loader, command line, and retail
executable hash pass the existing ownership proof. A 1×1 same-class Wine IME
surface is rejected by geometry.

Start Recording re-discovers identity at the write boundary and invokes the
strict recorder with the exact PID/display/window. Output defaults to a unique
timestamped `work/copies/input-movies/*.input-movie.json`; existing, linked,
missing-parent, and outside-`work/copies/` paths refuse. Stop re-proves the
stored exact target before sending F12. Closing the session sends
SIGINT/TERM/KILL only after
verifying that the recorder and pristine launcher each own their isolated
process group.

## Fixture evidence

`tests/test_input_movie_controls.py` passes 11/11 cases covering:

- machine-readable no-host/no-display-wide/no-engine-frame scope;
- Linux `/proc/PID/stat` process-group parsing, including complex command text;
- nested display selection limited to one owned process group and ambiguous-
  display refusal;
- pinned-launcher command construction with exactly one `--windowed`;
- exact target/movie arguments passed to `input-movie.py`;
- create-only work-copy-confined movie paths and same-second unique naming;
- rejection of the 1×1 IME surface and selection of one exact 640×480 target;
- familiar `--research --windowed --mute --dry-run` behavior;
- exact isolated-recorder cleanup and refusal to signal a non-isolated child.

The focused companion plus recorder suites pass 22/22. The final unsandboxed
`make check` passes 556 tests, Vault lint, the unchanged five-anchor M4
compatibility statement, tracked-content audit, and both diff checks. The
workspace sandbox run's seven GDB fixture failures were environmental ptrace
refusals; the same full tree passed when those fixtures could attach to their
own children.

## Result

**Confirmed by implementation and synthetic fixtures:** the companion removes
manual PID/display/window entry, preserves the pinned launcher, scopes target
discovery and stop input to one owned PC game window, confines movie creation,
and cleans up only isolated owned processes.

**Live follow-up:** [[EXP-20260815-121 - First companion route replay divergence]]
confirms exact-window discovery and one accepted 306-event recording, but
rejects the companion's current manual-delay workflow for a launch-to-gameplay
route. The output entry advances to the next unused name immediately after a
save, the three-second pre-anchor interval can omit intended setup input, and
terminal Ctrl-C can interrupt the Tk polling callback without completing
session cleanup. These are live usability/lifecycle findings, not failures of
the fixture claims above.

## Links

- Usage and safety contract: [[PC input movies#Convenient companion window]]
- Prior production recorder validation:
  [[EXP-20260815-119 - PC input movie recorder and hardware replay]]
- Capability register:
  [[Reverse Engineering Capability Gaps#CAP-002 — Deterministic PC input movies]]
