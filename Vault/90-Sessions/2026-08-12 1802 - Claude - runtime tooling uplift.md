---
type: session
date: 2026-08-12
agent: Claude
status: completed
tags:
  - session
  - re/dynamic
  - implementation/tooling
---

# Runtime tooling uplift

## Agent

Claude

## Goal

Implement a bounded, scripted, read-only runtime-evidence tooling suite that
automates the manual Wine capture methods, adapting design patterns from the
researcher's DuckStation `external-debugger-control` fork. Tooling and staged
procedures only; no live-game validation in this packet.

## Files inspected

- Read the required startup sequence: [[START HERE]], [[Current State]],
  [[Project Roadmap]], [[Environment Status]], [[Decision Log]], and
  [[Known Unknowns]], plus [[Cross-Port Evidence Policy]] and
  [[External Source Registry]] before recording the tooling reference.
- Existing house patterns: `scripts/wine-capture.sh`, `scripts/play-pristine.sh`,
  `scripts/doctor.sh`, `scripts/note_utils.py`, `tests/test_anm.py`,
  `dynamic/wine/RUN-GDB-20260812-161520/{metadata.json,debugger-evidence.txt}`,
  `Makefile`, and `.gitignore`.
- `/home/dev/duckstation` at branch `external-debugger-control`
  (`fe0cca16b`) as a tooling-methodology reference only.
- No file under `originals/` was modified. No PS1 source was opened or used;
  the DuckStation fork was consulted for engineering patterns, not game
  semantics.

## Experiments inspected

- [[EXP-20260812-008 - Training record watchpoints and individual roles]] and
  the `DEC-20260812-006` natural-pause hardware-watchpoint method that the GDB
  harness automates.

## Changes made

- Added `scripts/evidence_lib.py` (ownership proof, run-dir stamping, watch-spec
  validation, ELF core iteration) and `scripts/gdb-harness.py` (dual-mode
  read-only hardware-watchpoint harness with structured completion,
  `--capabilities`, JSONL stops, and a metadata superset of the hand-written
  RUN-GDB shape).
- Added `scripts/rr-record.sh`, `scripts/frozen-capture.sh`,
  `scripts/memory-snapshot.sh`, `scripts/core-grep.py`, and
  `scripts/apitrace-capture.sh`; extended `scripts/wine-capture.sh` with
  additive relay and file-trace flags.
- Added `.gitignore` entries `/work/rr/` and `/work/apitrace/`; new
  `scripts/doctor.sh` rows (GDB, rr, apitrace, perf_event_paranoid,
  ptrace_scope); `Makefile` targets `harness-caps` and `rr-help`.
- Added tests: `tests/test_evidence_lib.py`, `test_gdb_harness.py`,
  `test_rr_record.py`, `test_wine_capture.py`, `test_frozen_capture.py`,
  `test_memory_snapshot.py`, `test_apitrace_capture.py`.
- Vault: `DEC-20260812-019`; `SRC-DUCKSTATION-DBG`; [[Runtime Tooling]]; new
  `KU-028`/`KU-029`/`KU-030`; [[Environment Status]] annotations; a
  [[Current State]] tooling bullet; and an [[Implementation MOC]] link.

## Conclusions

- **Confirmed:** All seven tools pass synthetic-fixture tests, including the
  GDB harness driving real gdb against a compiled C sentinel (max-stops,
  timeout, milestone, cleanup, and detach-resume). The harness exposes no
  write verbs (`write_verbs: []`).
- **Confirmed:** `rr 5.9.0` and `apitrace` are installed;
  `kernel.perf_event_paranoid` is `2`, so `rr-record.sh` refuses recording
  until the user applies `sudo sysctl kernel.perf_event_paranoid=1`.
- **Unknown:** Every tool's live-game behavior. `KU-028`/`KU-029`/`KU-030`
  record the staged validation questions; none is executed in this packet.

## New hypotheses

- None promoted; the staged validations are recorded as known unknowns rather
  than hypotheses.

## Contradictions discovered

- None.

## Tests run

- `.venv/bin/python -m pytest -q tests`: 113 passed before the vault notes;
  the full suite plus vault lint and the tracked-file audit are re-run via
  `make check` at close. Ran `bash -n` on every new/edited shell script. Did
  not regenerate the `doctor.sh` block in the committed tree, because this
  environment's PATH lacks some tools (e.g. `rg`) and would falsely mark them
  uninstalled; the row additions take effect when the user runs `doctor.sh`.

## Unresolved questions

- The exact live PipeWire/gamescope screenshot command for `frozen-capture.sh`
  remains to be established and committed as the default `CAPTURE_CMD`.

## Recommended next action

Execute the staged validations in [[Runtime Tooling]], beginning with the GDB
harness against an unchanged Training copy to reconcile
`RUN-GDB-20260812-153150`, then the `rr` validation (`KU-028`) after the
`perf_event_paranoid` sysctl. Keep the active M2 packet in
[[Project Roadmap#M2 — Resource dependency graph and one editable asset family]]
unchanged.

## Git commit if applicable

Bounded commits in house style, e.g. `feat: add gdb watch harness with
structured stop evidence` and `docs: record runtime tooling uplift decision and
procedures`.
