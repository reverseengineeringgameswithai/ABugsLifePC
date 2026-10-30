---
type: experiment
id: EXP-20260816-163
date: 2026-08-16
question: 'Can KU-065''s lost one-test canonical-suite failure be reproduced with complete unfiltered logs, and can the failing test be identified?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; repository Python 3.14.6; pytest 9.1.1; canonical host capabilities plus one separately labelled constrained-sandbox diagnostic
environment_version: Python 3.14.6; pytest 9.1.1
working_directory: /home/dev/ABLPC
configuration: clean subject HEAD 02946af; every pytest invocation redirected directly to its own raw log before any grep; no Wine, Gamescope, game, or debugger target launched; 32 pre-existing baseline-prefix winedevice processes discovered by the final broad process audit
artifacts:
  - work/copies/EXP-20260816-163-ku065-evidence/SHA256SUMS
addresses: []
file_offsets: []
result: original-single-failure-not-reproduced-ku065-open-one-sandbox-only-descriptor-delta-candidate
created: 2026-08-16T18:59:16-04:00
updated: 2026-10-02
tags:
  - re/experiment
  - testing
  - known-unknown
---

# EXP-20260816-163 - KU-065 canonical-suite reproduction follow-up

> Later 2026-08-17: KU-065 was resolved for its identified node (a fixed sleep in
> `tests/test_input_movie.py` racing the recorder's baseline snapshot); the four
> original camera-packet failures stay unidentified. See
> [[Known Unknowns history through 2026-09-26#KU-065 - Intermittent single-test failure in the canonical suite]].

## Verdict

**The original `1 failed, 647 passed` event did not reproduce in the canonical
host environment, so its test is not identified and KU-065 stays open.** A
constrained-sandbox full run did make one receipt-chain descriptor-count test
fail, but it also produced eight unrelated GDB/input failures. That different
signature is a candidate lead, not authority for the original event.

No pytest process was piped through `grep`, `sed`, `cat`, or any other filter.
Every invocation wrote directly to one raw `*.log`; searches happened only
after the process exited. This experiment started no game, Wine, Gamescope, or
debugger target.

## Exact retained method

All logs are retained locally under ignored work-copy evidence directory
`work/copies/EXP-20260816-163-ku065-evidence/`. Its 317-log manifest is
`SHA256SUMS`, SHA-256
`e60f1ff372ee19fc953e57e2795032f7c6e4272aa5d6b2fa45108ae82bd63b1e`.
It is deliberately not committed because `work/copies/` is the project's
ignored work area.

The canonical invocation was exactly:

```bash
PYTHONPATH=/home/dev/ABLPC/reimplementation \
  .venv/bin/python -m pytest -q tests > full-host-N.log 2>&1
```

The focused and module invocations changed only the final test selector; they
used the same direct redirection and one new file per run.

## Canonical host results

- **13 full-suite runs:** all `648 passed`, durations 17.75-18.30 seconds.
  This is 8,424 full-suite test executions with no failure line.
- **100 whole-manifest runs:** all `198 passed`, including every receipt-chain
  descriptor-delta and private mount-namespace case in native module order.
  This is 19,800 manifest test executions.
- **200 focused runs:** all `17 passed, 181 deselected` for
  `-k 'mounted or descriptor or cleanup_error'`. This is 3,400 executions of
  the selected descriptor and mounted-path cases. The whole-module loop above
  covers the two adjacent cases not selected by that expression as well.
- One earlier whole-manifest baseline also passed `198 passed`.

A broader closure audit found 32 pre-existing `winedevice.exe` processes,
PIDs `68248` through `344284`, parented by user systemd PID `1927`. Their
start times span 2026-08-15 17:39:48 through 2026-08-16 16:51:32 EDT, their
environment names project prefix `work/wine/baseline`, and sampled working
directories name earlier `work/copies/` experiments. No game, Gamescope,
`wineserver`, pytest, or debugger target was active. These PIDs predate this
experiment and were not recorded as owned at launch, so the lifecycle policy
forbids terminating them by broad process name. The runs therefore rule out
an immediately reproducible failure in the two suspected families and exact
suite while this residual Wine-device background is present. They do not rule
out contention immediately after an active game/Gamescope session, delayed
cleanup, or another test family.

## The separately bounded sandbox lead

Before host capabilities were restored, one full-suite run in the constrained
execution sandbox produced `9 failed, 639 passed` in 17.00 seconds, raw-log
SHA-256 `68b7a301544922f3cd8046efa4327d1005caf4f456a9c2538d4dfa235bbed81f`.
Seven GDB harness cases could not attach, one input-movie timing case returned
an anchor timeout, and this receipt-chain case failed:

`tests/test_manifest.py::test_cli_receipt_cleanup_error_is_silent_and_closes_every_descriptor`

Its final assertion observed `_open_descriptor_count() == 14` after recording
`before_descriptors == 15`. The same case passed in all canonical full runs,
all 100 whole-manifest runs, and all focused selections. Because the sandbox
run has nine failures rather than KU-065's one and materially different ptrace
and timing capabilities, the evidence supports only this statement:

- **Confirmed:** that descriptor-count assertion can fail when an unrelated
  process descriptor disappears during the test window in the constrained
  environment.
- **Inferred candidate:** it is a plausible identity for KU-065 because it is
  the only observed failure in the exact system-state-sensitive family and
  compares a process-global count across work it does not exclusively own.
- **Unknown:** whether it was any of the four original lost failures.

## Disposition

Do not close KU-065 and do not cite `648 passed` as an unqualified gate. The
honest wording remains: thirteen complete host runs passed during EXP-163,
while an earlier one-test intermittent failure remains unidentified.

The cheapest next discriminator is opportunistic, not a reason to launch the
game solely for stress: after the next separately authorized Wine/Gamescope
research session, run the canonical suite again with direct per-run logs. If
the descriptor candidate recurs, capture the `/proc/self/fd` identities before
and after that one assertion to identify the disappearing descriptor; if a
different `FAILED` line appears, update KU-065 with that exact node ID and raw
log hash.
