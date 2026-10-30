---
title: 2026-08-20 1840 - Codex - R2o completed-present executor implementation
date: 2026-08-20
agent: Codex
tags:
  - session
  - reverse-engineering
  - r2o
  - tooling
status: complete
---

# 2026-08-20 1840 - Codex - R2o completed-present executor implementation

## Objective

Implement the offline executor for the James-accepted [[EXP-20260820-004 - R2o completed-present state calibration protocol]] without launching or attaching to the game.

## Work completed

- Added `reimplementation/ablpc/r2o_completed_present.py` and the argument-free `scripts/r2o-run-completed-present-calibration.py` wrapper.
- Replaced a rejected whole-register snapshot design with exact-field `PTRACE_PEEKUSER` reads of only `EIP`, `EAX`, and `EFLAGS`.
- Added readback-verified `DR0`-`DR3`/`DR6`/`DR7` programming and restoration, continuous outer-entry guarding, exact hardware-trap classification, ordered phase stops, and the bounded read allowlist.
- Added atomic attempted/completed/validated action journals, all-task-stopped capture anchoring, process/window/task guards around captures, PNG-before/decode/PNG-after binding, relative-path rebinding after evidence classification, independent packet validation, and aggregate quarantine.
- Added `tests/test_r2o_completed_present.py`; 76 targeted tests pass in the current correction. One test builds and traces a tiny non-game i386 ELF fixture to prove the host compat offsets, hardware execution trap, continue path, and exact restoration.

## Hard-truth audit

James rejected the first implementation because it over-read the whole register set, trusted summary receipts, retained pending capture paths, lacked durable pre-verdict evidence and DR readback, anchored capture timing too late, and did not fail closed across aggregate publication. Those mechanisms were replaced rather than waived. The corrected implementation packet still requires final James review.

## Runtime boundary

No game process was launched or attached. No game process-memory read, debugger write, SIGSTOP/SIGCONT, DAT mutation, localizer, or candidate arm occurred. EXP-004 D1/D2 remains unrun and requires fresh explicit user authorization after implementation acceptance.

## Links

- [[EXP-20260820-004 - R2o completed-present state calibration protocol]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Current State]]
- [[Known Unknowns]]
- [[Reverse Engineering MOC]]

## Second hard-truth correction

James rejected the first committed implementation at `0d83c94`. The follow-up replaced aggregate ambiguity handling, expanded the validator, added full guards before all resumes and detach, added wall-clock hit evidence, made final capture observations durable, added aggregate disposition/manifest publication, and derived debugger-write state from the journal. James then rejected `eb28b77` because the validator still accepted an impossible non-interleaved fixture, pre-title chronology and exceptional dispositions were incomplete, rollback failure could retain a false accepted state, and D1 was not revalidated around publication.

The current correction reconstructs and enforces the exact nested journal/trace state machine, exact slot maps and DR transitions, all-task stops, reads, guards, captures, resumes, and final restoration. It adds a bounded Level01-read completion receipt; derives debugger disposition in `finally`; publishes first as `accepted: false` / `published-unverified`; revalidates both controls after D2, before publication, and after publication; and makes the final accepted disposition the last atomic write. It also binds the main task census to guarded PID/start, validates exact open/select/close and result payloads, requires nondecreasing journal/stop time, and demotes terminal evidence to pending on disposition or manifest finalization failure. If the demotion rename itself fails, a separate pending ambiguity receipt records both errors and forces namespace coexistence to remain aggregate-pending. The expanded targeted suite passes 76 tests. No game runtime occurred.
