---
type: session
date: 2026-08-26
agent: Codex
topic: P0E additive residue recovery source freeze
status: consumed-failed-evidence-accepted
---

# 2026-08-26 1900 - Codex - P0E additive recovery source freeze

## Goal and authority

Continue the terrain/collision investigation by safely recovering the residue
from consumed P0E before returning to R2q. The user's exact fresh authority is:
“Sure sounds good, go for that. Make sure Git is clean and Obsidian is respected
at the end.” This permits the bounded cleanup developed here; it does not permit
a P0E rerun, process-memory access, packet classification, or an R2q runtime.

## Read-only starting state

P0E's collection is already James-accepted at collection level only. The
original packet remains in `evidence/pending/P0E-AH-001`, `Y:` points to the
P0E stage, and `R:` points to P0A. The original normalized 33-name packet tree
is `edcd8269...031`. An inherited writer appended 359 bytes to
`launch.stderr`, producing current append-aware tree `53aa3b5a...a396c` and
size 11,706 while preserving the frozen 11,347-byte prefix. The P0E stage and
`Y:` are exact tree `b9b26839...df44a`.

A read-only 18:59 `game-session audit` reports only PIDs 310463
(`gamescopereaper`, original group 310283) and 310509 (`winedevice.exe`, its
original group), no null sink, no open session, and `clean:false`. The module's
independent exact census agrees. The recovery marker and all recovery packet
roots are absent. These observations caused no signal, input, sink change,
mapping change, or process-memory operation.

## Additive recovery design

The new wrapper consumes `P0E-R1-AH-001.attempted` with exclusive creation
before any project import or preflight. It requires `/usr/bin/python3.14 -I`, a
closed environment, pinned Git, globally clean exact committed sources, and a
tracked generated activation. It first authenticates the append-aware P0E
packet, exact P0E stage/retail/P0A trees and mappings, original marker and
collection/disposition bytes, and all namespace-parent identities.

The executor freezes 12 original PID/start/group/session/command/cwd/executable
contracts and an independent Wine/Gamescope helper census. It sends individual
TERM only after exact reauthentication, polls five seconds, then sends
individual KILL only to freshly reauthenticated survivors and requires two
timely absence observations. It unloads only mute module `536870916` if its
exact name/arguments still exist. Repeated direct census, exact sink, and full
session-audit gates must all be clear before an authenticated same-parent
temporary link atomically replaces `Y:` with retail and fsyncs/rereads it.
`R:` and all original P0E bytes remain preserved. Success publishes only
`p0e-recovery-published-unverified`; James owns later result review.

There is no process-memory read/write, ptrace, debugger, screenshot, save-state,
new game input, DAT edit, terrain intervention, or P0E classification path.

## James rejection rounds

James's first hard-truth audit rejected three blocker families:

1. a corrupt or mismatched stage snapshot could reach cleanup action;
2. a failed envelope could bless forged retained receipts; and
3. publication did not fully bind physical source/destination parents and the
   moved root.

The correction moved coherent append-aware stage validation before census or
signal, made the failure validator accept only the exact semantically valid
run-receipt prefix, and used authenticated directory descriptors plus
rename-at semantics and fsync for publication.

James's second audit found a remaining crash-durability defect. If
pending→published renamed successfully but its original pending-parent fsync
failed, `_record_failure` could move published→failed and validate that later
terminal without repairing or recording the first rename's source parent.

The final correction authenticates the retained predecessor
`publication.json` against its exact root and planned parent identities. If its
pending-parent durable bit is false, failure finalization reopens and binds that
exact parent, fsyncs it before any published→failed rename, and records the
predecessor hash, three publication bits, both parent identities, repair
requirement/completion/time, and later published-parent fsync. A persistent
repair error leaves the packet in published-unverified with explicit incomplete
repair state; it cannot create or validate a failed terminal.

## Verification and boundary

Exact candidate hashes:

- module `a1a854cf64d64d2e8ee06fe0a20aff1cd9071418d09157bf035bcd73b11bb024`;
- wrapper `c14ed69ab6193aa584bbfd98542ccabcc083470fec6572bcc18a20994713f951`;
- activation freezer `fafc5acc4fd63e02c6bfb685dd649a96fbd080bb189f2272895cccd8717630b0`;
- tests `c58068edc925aca276e0acffee810b84fdd06804d839e1705a010be0d692299f`.

Compilation passes. Focused recovery tests pass 101/101 and the combined
P0E/passive/lifecycle set passes 809/809. The one-shot regression proves the
exact pending parent is reopened and repair is recorded; the persistent-failure
regression proves no completed failed terminal is possible. James independently
passed 101/101, authenticated the four hashes and all predecessor semantics,
and returned `ACCEPTABLE-FOR-SOURCE-FREEZE`. The source-phase `make check`
then passed 3,444/3,444 in 2,500.62 seconds with 0 tracked-file violations;
Vault lint remained 610 notes / 0 errors / 8 pre-existing warnings.

The source phase committed as
`dc2481be6479333878774dd9194cb02d9f7912f9` / tree
`ba664464977ef600076b666a204f940017a1fc88`. With Git clean, the dedicated
freezer produced canonical 2,501-byte
`r2p_p0e_recovery_activation.json`, SHA-256
`df1def843f3d0c51f2de61c5d6f544390101de660e74e69be4405b145a103556`.
It binds exact Git blobs and SHA-256 values for all 12 executed local sources
to the earlier immutable source commit. The documentation-inclusive tree then
passed 3,444/3,444 tests in 2,481.05 seconds with 0 tracked-file violations and
committed as `3aa9127db4312338a090ae1e096326b020b8e7f0` / tree
`1be8a4a5baef013a3f4686e1d5c20b0476c50419`.

At that checkpoint no live recovery action had occurred. The packet remained
pending and the marker absent. James then independently authenticated the clean
exact activation/source closure, 101/101 focused tests, absent recovery names,
and every action/publication boundary, and returned **ACCEPT** for exactly one
argument-free invocation after a fresh accounted audit.

## Sole run and failed-evidence disposition

The fresh pre-action audit contained only exact frozen residuals 310463 and
310509, no sink, no session, and no unknown process. The exact accepted command
ran once and consumed a 34-byte mode-0600 marker at device/inode 54/9296988,
SHA-256 `2e8a0f3a8ebac7b1b941db53cef8f7603e91b99207ffe7f4943ceb8adde51d94`.
It will not be invoked again.

Events 0–31 record exact initial identity, successful authenticated TERM to
each residual, 23 polls over the complete five-second TERM budget with both
still exact, fresh exact pre-KILL identity, and successful authenticated KILL
to each. Both processes then disappeared between the first two post-KILL
census reads. Because those reads differed, the strict stable-census helper
raised `RecoveryError: residual census was unstable` before a poll event or
`pending-after-kill.json` could be persisted. The wrapper exited 2 after 6.97
seconds. It did not unload a sink (none was present), touch `Y:`, change `R:`,
send input, or access process memory.

The fail-closed handler durably moved the owned recovery packet from pending to
failed and fsynced both parents. Production `validate_failure_envelope` accepts
the exact 10-entry tree
`0be8f7be1f2da2a417774ed702db2c803b94fd0a525d9855cd3c679216543f89`.
Key receipts are events `cad13b386c1e9314713c360ff50c87df8dc150a117b6c58ee5ffb0d8ef258056`,
failure `4f64f610...18d46f`, failure-publication `d16e2e95...d8376e`, and
failure-manifest `82fb238e...f23316`. The failure snapshot records all 12
frozen identities and the sink absent. The required post-action session audit
independently reports exactly clear.

James independently returned **ACCEPT-AS-FAILED-EVIDENCE**. The receipts
support removal of residuals 310463/310509, but not the missing protocol
two-consecutive-poll clear proof; this is not a successful recovery. Original
P0E remains pending at current/normalized trees `53aa3b5a...a396c` /
`edcd8269...031`; `Y:` remains exact P0E stage `b9b26839...df44a`; `R:` remains
P0A. P0E-R1 is consumed with no retry. Any mapping restoration requires fresh
explicit authority and a new frozen/James-accepted successor. No P0E
classification, R2q execution, task-role, terrain, or collision result follows.

## Links

- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
- [[Decision Log#DEC-208 - Recover P0E residue only through a predecessor-durable additive envelope|DEC-208]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)|KU-079]]
- [[2026-08-26 1134 - Codex - P0D consumed and P0E passive successor]]
- [[Current State]]
