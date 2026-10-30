---
type: session
date: 2026-08-27
agent: Codex
topic: P0E Y-only restoration successor hard-truth checkpoint
status: wip-checkpoint-james-rejected
---

# 2026-08-27 0816 - Codex - P0E Y restoration hard-truth checkpoint

## Outcome

Banked the current P0E Y-only restoration successor as explicit work in
progress so another agent can resume without reconstructing the audit chain.
This checkpoint is not a James acceptance, activation freeze, or runtime
authorization. The current candidate incorporates James's round-26 findings;
James's exact-hash round-27 audit rejected it on two adjacent mapping-repair
defects recorded below.

No game, Wine, Gamescope, emulator launch/control, input, signal, sink,
process-memory, `/proc` collection, mapping, or packet-classification action
occurred during this work. One preliminary James fixture unexpectedly reached
the production read-only session audit; it made no mutation, signal, input, or
mapping action, and his certifying reproductions used a fully isolated fixture.
Runtime state remains the accepted P0E-R1 post-action state: the audit was
clear, original P0E remained pending, `Y:` remained on exact P0E stage
`b9b26839...df44a`, and `R:` remained on P0A.

## Why this is on the terrain/collision path

R2q terrain/collision work remains downstream of a clean mapping baseline.
Consumed P0E-R1 removed the residual processes but failed before restoring
`Y:`. The successor has exactly one mutable target: atomically exchange staged
`Y:` for retail, durably fsync/read back the mapping, and publish only
unverified evidence for James. It cannot launch or control a process, send
input or signals, unload a sink, access process memory, change `R:`, mutate the
original P0E/P0E-R1 packets, or claim terrain/collision evidence.

The user's fresh authority is encoded for one atomic Y-only stage-to-retail
restoration. That authority is deliberately inert until the source is frozen,
the exact clean activation revision is accepted by James, and the immediate
pre-action audit passes.

## Banked candidate

- `reimplementation/ablpc/r2p_p0e_y_restore.py` — SHA-256
  `49c90537f6a9094c667a9708206e44063f8211ee656083249265e24aa76653f3`
- `scripts/r2p-restore-p0e-y.py` — SHA-256
  `9c9dbb28bff966a708bddd267e899ca2d8c7264bf25622b34cd27341b48aea80`
- `scripts/r2p-freeze-p0e-y-restore-activation.py` — SHA-256
  `640aefb10c4b3458f1f1b1a8f11d53ad4d0e35e21c590d2c72f92521c50642bc`
- `tests/test_r2p_p0e_y_restore.py` — SHA-256
  `92ae90bbf35f3fbd27f80e6355fbc27aded207ef19ba96a8977d1a7937eb73a3`

Protocol identity is `ablpc-r2p-p0e-y-only-restoration-v1`; the future
exclusive marker is `P0E-YR1-AH-001.attempted`. The tracked activation anchor
does not yet exist and the wrapper has not run.

Offline verification at this checkpoint:

- `python -m py_compile` passed for the module, wrappers, and tests.
- focused restoration suite: 96 passed in 1.43 seconds.
- combined P0E/P0E-R1/Y-restoration suite: 357 passed in 3.60 seconds.
- full repository `make check`: 3,540 passed in 2,438.22 seconds with 0
  tracked-file violations; Vault lint reported 611 notes / 0 errors / 8
  pre-existing warnings before this result line was added.

## Hard-truth audit history retained for handoff

James is the project's adversarial, independent hard-truth verifier. He does
not implement or soften a candidate; he attempts to falsify its provenance,
state machine, chronology, durability, and failure semantics and returns
`ACCEPT` or concrete reproducible rejection grounds.

The most recent ten correction rounds closed these exact defects:

1. Round 17: a nonzero exchange count could coexist with no syscall entry.
2. Round 18: a committed result could also claim a completed rollback.
3. Round 19: an uncommitted observed exchange could omit rollback evidence.
4. Round 20: a rollback event could carry later cleanup retirement.
5. Round 21: the retirement `before` identity could be substituted instead of
   matching the authenticated post-exchange temporary.
6. Round 22: cleanup could claim a successful move into an occupied quarantine
   name.
7. Round 23: the real rename-complete/parent-fsync-pending cleanup state was
   not representable or repairable.
8. Round 24: a cleanup-only repair could falsely mark mapping durability when
   no exchange occurred.
9. Round 25: a pre-exchange pending-cleanup repair could discard its repair
   provenance when producing a failed envelope.
10. Round 26: cleanup-repair completion had no lower bound against the retained
    journal prefix, and persistent repair errors admitted uncontrolled strings.

The banked successor now requires repair completion at or after the latest
retained prefix timestamp and before the failure snapshot. It also requires a
nonempty, single-line `OSError: ` error with a 1,024-character total bound.
Coherent regressions cover both repairs. James's round-27 audit independently
confirmed that both round-26 fixes close, and the combined suite again passed
357/357. He nevertheless rejected the complete current candidate because the
analogous mapping-parent repair path still has two gaps:

11. Round 27: an isolated valid `mapping-fsync-once` failure packet accepted a
    mapping `repair_completed_monotonic_ns` of zero, predating the retained
    exchange prefix.
12. Round 27: the same packet accepted complete removal of mapping-repair
    provenance even though the retained committed exchange recorded
    `parent_fsynced=false` while top-level durability was true.

James's required correction is exact: mapping-repair provenance must exist
whenever retained durable event/mapping state proves `mapping_replaced=true`
and the event says `parent_fsynced=false`, and its completion time must satisfy
`prefix_latest <= repair_completed_monotonic_ns <= snapshot.observed_monotonic_ns`.
Add a full `mapping-fsync-once` fixture and omission/zero mutations.

## Resume point and stop rule

1. Start from this WIP commit and recheck all four hashes.
2. Implement James's two round-27 mapping-repair requirements and the coherent
   full-packet regressions above. Then recompute hashes and request a read-only
   round-28 audit. If James rejects, reproduce each defect, add coherent
   positive and adversarial regressions, and repeat until a fresh candidate
   receives `ACCEPT`.
3. Once source is accepted for freeze, run the proportionate repository gate,
   commit the immutable source, and run the argument-free exclusive activation
   freezer. Commit the generated activation and documentation, then obtain
   James's exact clean-tree final `ACCEPT`.
4. Do not invoke `scripts/r2p-restore-p0e-y.py` before that final acceptance and
   a fresh `make session-audit`. The runtime wrapper is one-shot and
   argument-free; any invocation consumes its arm.
5. After the sole authorized run, audit immediately, validate the packet, and
   have James classify only the produced evidence before resuming R2q.

No terrain, collision, material, visibility, render-command, task-role, or
retail-executable conclusion follows from this WIP checkpoint.
