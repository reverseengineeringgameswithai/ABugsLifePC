---
type: session
date: 2026-08-17
agent: Claude
status: complete
tags:
  - session
  - implementation/tooling
  - re/workflow
---

# Agent automation tooling

## Agent

Claude.

## Goal

Answer a question about the project rather than about the game: how well does
this repository support automated reverse-engineering investigation by
Codex/Claude, what is missing, and then build the missing parts.

The investigation phase surveyed the runtime scripts, the recorded practice of
live experiments, and the surrounding harness (instructions, Makefile, tests,
templates, static exports, run directories, CI). The build phase implemented
the gaps that could be closed offline and recorded the ones that could not.

## Files inspected

The startup sequence per [[START HERE]] (re-read this session, per
`DEC-20260814-055`); [[Agent Operating Manual]]; [[Environment Status]];
[[Reverse Engineering Capability Gaps]]; [[Runtime Tooling]];
[[PC autonomous game control]]; [[PC Flik teleport procedure]];
[[PC level roster and numbering]]; every script under `scripts/`; the
2026-08-15/16 runtime experiment packets; ~200 session notes for lifecycle
cost; `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`;
`dynamic/wine/RUN-*`; `Makefile`; `tests/`; `AGENTS.md`; `CLAUDE.md`.

## Experiments inspected

`EXP-20260816-144`, `-148`, `-149`, `-150`, `-151`, `-153`, `-156`, `-157`,
`-163`, `-170`, `-171`, `-173`; `EXP-20260815-119` through `-137`;
`EXP-20260817-182`, `-185`, `-186`.

No new experiment note was created: this packet produced no evidence about the
executable. Its output is tooling, registers, and two new Known Unknowns.

## Changes made

New notes: [[Session control plane]], [[Agent evidence and query tooling]],
[[Ghidra export structure and caveats]], [[Current State Archive]].

New scripts: `session_lib.py`, `game-session.py`, `game-memory.py`,
`send-keys.py`, `wait-for.py`, `briefing.py`, `ghidra-query.py`,
`run-index.py`, `experiment-draft.py`, `claim-sweep.py`,
`install-git-hooks.sh`, `git-hooks/pre-commit`. `game-memory.py`
gained `snapshot`/`restore` (a same-process region checkpoint) and
`criu-feasibility.py` was added (the read-only durable-savestate survey). Extended `vault-lint.py`
(context budget, staleness, orphans, `--json`) preserving its existing checks
and clean exit. New `.github/workflows/check.yml`, `pytest.ini`, `Makefile`
targets.

New tests: `game_fixture.py`, `test_session_lib.py`, `test_game_memory.py`,
`test_game_session.py`, `test_send_keys.py`, `test_wait_for.py`,
`test_briefing.py`, `test_ghidra_query.py`, `test_run_index.py`,
`test_experiment_draft.py`, `test_claim_sweep.py`, `test_vault_lint.py`,
`test_repo_hygiene.py`, `test_install_git_hooks.py`. Fixed three racy sites in
`test_input_movie.py`.

Corrections to existing authorities: [[PC Flik teleport procedure]] (the
write is two vectors, not a contiguous range); [[PC autonomous game control]]
and [[Runtime Tooling]] (implementation cross-references); [[Current State]]
(chronology moved verbatim to the archive; KU-065 resolution recorded).

Registers: CAP-010 through CAP-018 in
[[Reverse Engineering Capability Gaps]]; `KU-074` and `KU-075` added and
`KU-065` resolved for its identified node in [[Known Unknowns]];
`DEC-20260817-139` through `DEC-20260817-143` in [[Decision Log]]. CAP-011
updated with the same-process region checkpoint and the measured CRIU blocker.

## Conclusions

- The evidence and receipt discipline in this repository is strong; the
  **live-session control layer was the gap**, and it was human-shaped. The
  complete recipe existed only as prose, and its three hardest-won findings
  had already been learned and re-learned once.
- The mandated startup reading set (~272,994 estimated tokens) could not be
  read by any agent. That is a structural cause of the missed-content audit
  rounds already recorded in the project, not an incidental inconvenience.
- The dominant audit-rejection cause is not wrong models but corrections that
  land at one occurrence out of several. That is mechanically detectable and
  now is (`claim-sweep pair`).
- `ghidra-evidence.json` was unreadable in practice and is also structurally
  misleading in three specific ways; both problems mattered and only one was
  known.
- Save states are feasible in-process but not via CRIU here: every game
  global lives in the single writable `.data` section, so a memory-only
  same-process checkpoint works, while CRIU is blocked by the `ntsync` fd that
  also defeats `rr`. The feasibility survey turned that from an assumption
  into a measured fact against the live process.

## New hypotheses

None about the executable. Two inferences are now load-bearing enough to be
tracked as `KU-074` (live semantics of the carousel counter `0x00599AF8`) and
`KU-075` (the exact software-arm 320x200 log wording).

## Contradictions discovered

The accepted teleport boundary said "one 24-byte `process_vm_writev` call"
covering current and preceding XYZ, but those triples are not contiguous: an
unidentified dword sits at `0x0059D91C`. A literal contiguous 24-byte write
would overwrite it and misalign the second triple. Recorded and corrected in
[[PC Flik teleport procedure]] rather than resolved silently; the earlier
EXP-130 helper's own behaviour was not re-examined here and its receipts are
unaffected by this correction to the wording.

## Tests run

Canonical suite `1109 passed` (previously 686 + new). Focused session-control
regressions: `test_session_lib.py` 66, `test_game_memory.py` 36 (incl.
snapshot/restore), `test_game_session.py` 21, `test_wait_for.py` 19,
`test_send_keys.py` 15, `test_criu_feasibility.py` 5.
KU-065 node before/after: idle 59/60 → 60/60, 12-worker load 0/20 → 20/20,
each run directly redirected to its own raw log.
`scripts/vault-lint.py`: 534 notes, 0 errors, 4 warnings.

## Unresolved questions

CAP-010 (live validation of the session tools), CAP-011 (checkpoint/restore),
CAP-012 (focus-gated logic), CAP-013 (level switching without relaunch),
CAP-014 (coverage tracing), CAP-015 (visual verification), and the residuals
on CAP-016 through CAP-018. `KU-074`, `KU-075`, and the identity of KU-065's
four original failures.

## Recommended next action

Do **not** cite any session-control tool as runtime evidence yet. The next
runtime work should begin with CAP-010's acceptance arm, kept as small as
possible: `game-session launch --auto-hardware --dry-run`, then one authorized
launch with `--keep-on-reject`, comparing the tool's gate verdict against a
hand-read log and its discovered PID/window/display against the manual
procedure, and confirming `close` leaves an empty targeted audit. Only after
that agrees should `level` navigation or any write verb be used live.

A save-state capability exists as a same-process `.data` region checkpoint
(`game-memory.py snapshot`/`restore`). At the user's request it was then
**tested live** against the running game
([[EXP-20260817-188 - Live game-memory read save restore validation]]): the
read/save/restore path works, including a full snapshot→change→restore→
verify cycle that reverted a real global exactly. `game-session`,
`send-keys`, and `wait-for` remain fixture-only. `criu-feasibility.py check`
shows the durable CRIU path is blocked here by `ntsync` (`KU-028`).

Independently of runtime work, `make briefing` is now the intended way to
start a session, and `claim-sweep pair` should be run after every correction
before an audit.

## Git commit if applicable

Not committed by this session; the working tree carries the packet for review.

## Process audit

This session was offline throughout. No game, Gamescope, Wine, or debugger
session was launched, and no `originals/` path was read or written. Its
subprocesses were `python3`, `pytest`, `git`, `grep`/`rg`, and the synthetic
test fixtures, which spawn short-lived `python3` children named `bugs.exe` and
`Xwayland` inside `pytest` temporary directories. Those are test fixtures, not
game or display processes; each is terminated by its own context manager, and
the suite completes with none surviving. No private audio sink was created.

A later follow-up (EXP-188), with explicit user authorization, read the
running EXP-187 leftover game session and made one guarded position write
that was immediately reverted; that session was left healthy and
position-as-found and is recorded-not-owned in [[Environment Status]].
