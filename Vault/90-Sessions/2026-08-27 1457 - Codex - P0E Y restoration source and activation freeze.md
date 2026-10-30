---
type: session
date: 2026-08-27
agent: Codex
topic: P0E Y-only restoration source and activation freeze
status: activation-frozen-runtime-uninvoked
---

# 2026-08-27 1457 - Codex - P0E Y restoration source and activation freeze

## Goal and authority

Continue the terrain/collision prerequisite work from clean commit `390404e`
by correcting James round-27's two mapping-repair gaps, continuing adversarial
source audits until acceptance, and then following the source-freeze and
activation-freeze sequence. The user expressly barred a game launch and the
one-shot restoration wrapper during this work. Any eventual restoration still
depends on James accepting the exact clean activation tree.

## Read-only starting state

Git began exactly clean at
`390404ecb950748a636c60512ec120c620970e53`. The activation anchor and attempt
marker were absent. The banked round-27 hashes were module
`49c90537...53f3`, wrapper `9c9dbb28...ea80`, freezer
`640aefb1...42bc`, and tests `92ae90bb...3a3`; 96 focused, 357 combined,
and 3,540 full-repository tests passed. James accepted the round-26 cleanup
fixes but rejected omitted mapping-repair provenance despite a retained
committed exchange with `parent_fsynced=false`, plus repair completion that
could predate the retained prefix.

No emulator/game launch or control, process mutation, input, signal, sink,
process-memory, mapping, packet, or wrapper action occurred. The accepted
runtime boundary therefore remained unchanged: clear host audit, staged `Y:`,
P0A `R:`, and original P0E pending.

## Correction and James rounds 28-34

The round-27 correction requires mapping-repair provenance when a retained
durable exchange does not prove its parent fsynced and enforces
`prefix_latest <= repair_completed_monotonic_ns <= observed_monotonic_ns`.
It adds a coherent mapping-fsync-once fixture with omission and zero mutations.

James then continued to attack the packet and rejected six successor gaps:

1. round 28: inverse mapping-repair provenance could be invented when the
   retained exchange already proved parent durability;
2. round 29: an unfinished `result=null` event could omit conservative repair,
   and retained-prefix chronology omitted final reauthentication, exchange
   attempt, admission creation, and the seal before result;
3. round 30: nested `y_parent_durability.parent_fsynced` could contradict the
   top-level failure bit;
4. round 31: cleanup-repair provenance could be invented despite a retained
   retirement event proving its parent fsynced;
5. round 32: event-absent cleanup state admitted omission/invention ambiguity;
   the producer now explicitly confirms cleanup durability after a completed
   rename unless a retained durable retirement proves it;
6. round 33: mapping and cleanup repairs could carry individually valid but
   jointly reversed completion times.

The final source cross-binds mapping and cleanup repair provenance to durable
events in both directions, conservatively repairs unfinished events, includes
the complete retained prefix in chronology, binds nested/top-level durability,
removes event-absent cleanup ambiguity, and requires mapping repair no later
than cleanup repair. Regression fixtures cover every rejected mutation.

## Source acceptance and freeze

Final exact hashes are:

- module `541fbe59fc7834dd8fd003b7c2a15f8b87bc6592d825eaa96710c3314fd63d57`;
- wrapper `9c9dbb28bff966a708bddd267e899ca2d8c7264bf25622b34cd27341b48aea80`;
- activation freezer `640aefb10c4b3458f1f1b1a8f11d53ad4d0e35e21c590d2c72f92521c50642bc`;
- tests `bad67fe107ba3998dac097ba914cbcea46d8b26e8255c4b2dd3fef58398e6111`.

Focused tests pass 98/98, the checkpoint combined set passes 359/359, and the
broad five-file P0E set passes 741/741. The source-phase `make check` passed
Vault lint at 611 notes / 0 errors / 8 pre-existing warnings, all 3,542 tests
in 2,473.25 seconds, and the tracked-file audit with 0 violations. James
independently passed 98/98 and 741/741, authenticated the four hashes, and
returned **ACCEPT** in round 34.

Only the module and tests changed. They committed as
`1964eecd6c58c228c2ba94d99dced546912d0641` / tree
`f0afa1ad9c5ec038e5385d20fc4f0bf558d6075d` with message
`Close P0E Y restoration repair provenance`. Git was clean and the activation
anchor plus attempt marker were absent at this source-freeze boundary.

## Activation freeze and boundary

The argument-free dedicated freezer created canonical 2,701-byte
`r2p_p0e_y_restore_activation.json`, SHA-256
`95e632dc76942ffca18b2a2a59c21345c339c72d866c3a487ab292adce7d8307`.
It binds 13 exact executed local sources to source commit `1964eec` / tree
`f0afa1a`, including the accepted module hash. The freezer did not invoke the
restoration wrapper or create the attempt marker.

This activation anchor is inert provenance, not a runtime result and not
independent authority to change `Y:`. The marker
`work/copies/EXP-20260820-005/evidence/P0E-YR1-AH-001.attempted` remains
absent. No game/runtime,
mapping, `R:`, packet, input, signal, sink, process-memory, R2q, terrain, or
collision action occurred. The wrapper remains barred until James accepts the
exact clean documentation-inclusive activation tree.

## Final clean-tree audit correction

James rejected exact activation commit `dd6cef3` / tree `211fc9d` because the
first freeze note named a nonexistent top-level `evidence/attempts/` marker
namespace. Both the wrapper and module instead bind the attempt marker at
`work/copies/EXP-20260820-005/evidence/P0E-YR1-AH-001.attempted`. The real
marker is absent. James otherwise authenticated the exact commit/tree, all
supplied hashes, activation validation/source binding, and Git cleanliness.
The successor correction changes only this durable note and requires a fresh
full gate, commit, and exact-tree James verdict.

## Links

- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
- [[Decision Log#DEC-211 - Freeze the James-accepted Y-only restoration source and activation|DEC-211]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)|KU-079]]
- [[2026-08-27 0816 - Codex - P0E Y restoration hard-truth checkpoint]]
- [[Current State]]
