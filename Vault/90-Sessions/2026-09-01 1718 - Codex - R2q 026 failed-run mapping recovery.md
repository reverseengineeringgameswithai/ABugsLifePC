---
type: session
date: 2026-09-01
agent: Codex
topic: R2q 026 failed-run mapping recovery
status: post-recovery-full-gate-passed-final-clean-tree-james-pending
---

# 2026-09-01 1718 - Codex - R2q 026 failed-run mapping recovery

## Goal and authority boundary

Preserve the sole consumed R2q-026 failure, clean up only its exact residual
identities under explicit user authority, determine the pre-science failure,
freeze and run exactly one separately authorized mapping-only recovery, and
close the result through tests, Vault, a clean commit, and James. No retry of
the R2q wrapper was authorized. The retained round-91 stash remains
`stash@{0}`, object `76db1c9ee1ffffce52cea6aee591c24ab6a1c39a`, and was
not dropped.

## Consumed failure and cleanup

R2q-026 D1 passed the corrected process-map convergence window but failed in
`stage-and-launch` with `game executable provenance is not exact`. Its
170,486,748-byte terminal packet is
`741fbd362c9c2f5d15c842e2b5deb34bedc6cf73d271e8f14b7df59429c2b14e`.
The title/navigation gate, quiet census, debugger acquisition, eleven stopped
ranges, PNG batches, D2, and scientific comparison never completed.

The user authorized cleanup only for these PID/start-tick identities:
`1801271/26731246`, `1801298/26731272`, `1801424/26731287`,
`1801428/26731287`, `1801437/26731295`, `1801463/26731301`, and
`1801516/26731418`. All seven matched before action. TERM cleared four; after
the bounded wait, KILL cleared only surviving `1801271`, `1801424`, and
`1801463`. PulseAudio module `536870916` was already absent. The session audit
was then exactly clean. James returned `ACCEPT R2Q-026 CLEANUP` and
`ACCEPT R2Q-026 FAILED-EVIDENCE`.

The executable path, inode, and SHA-256 matched, but the process's maps entry
used device `00:24` (`0/36`) while host `stat()` used minor `38`. Device IDs
are mount-namespace-relative here; the runtime incorrectly compared values
from different namespaces. James returned `ACCEPT R2Q-026 ROOT-CAUSE`.

## Distinct mapping-only recovery

James accepted recovery source commit
`9cf28fa81b27a41e2ce595e38141e2ac0ae885b1` / tree
`746e9d447a5aed712a6a927f461fe83eac418f0b`. Activation commit
`6134da8260f7f356ed0f2b9fbba45f2c3b860797` freezes the 1,189,260-byte
activation at
`16bbcfcc45ad0bde13ad3058963d073fd26a50492f3a59ebecd89d745eced1de`.
The exact user reply produced mode-0600 authority receipt
`d1150b39fd776bf676c2c6dd6f19e00b0dc56a0545663b4e16765229b1de4cfe`.
James accepted source, activation, and authority separately.

The wrapper ran exactly once and must never run again. It published marker
`9864c6439cb30bba3ac765d0edb9d531fbf71150f70e4eb0d63d6ad4dbdcd0b3`
and stable 28-entry tree
`264ecdacb4c0168f1edd3dadd29eddb5ffcee062a880f705db970b31ebc2780c`.
Mapping receipt
`be0a3633071250178a8c39be2ce1972ac57f5fe4cf55fd64fc1d3ca2c42580c4`
records one exchange, zero rollback, parent fsync, stable reread, before/
retired inode `9997058`, after retail-Y inode `9998033`, and unchanged P0A-R
inode `9054047`. Result
`d81c6f2bc73e2c50cc7f731f4c4da11d3c84b0c9d3a1ab2decd4cd667b61c142`
records one mapping action, zero runtime/input/signal/sink/process-memory
actions, and `terrain_collision_claim:null`. The audit is clear. James returned
`ACCEPT R2Q-026 RECOVERY EVIDENCE`.

## Post-action validation

Historical recovery adapters exact-gate the current mapping, retired link,
packet tree, receipt, and frozen predecessor closure. The design adapter uses
the complete production success validator; during pre-commit closure it may
project only the global Git-clean answer after proving every dirty path is
disjoint from the activation's frozen source ledger. Source/blob/activation,
mapping, packet, and evidence checks remain strict.

The focused historical/recovery suite passes 143/143 in 36.87 seconds. An
individual design validation passes in 163.87 seconds. Complete `make check`
passes 3,937/3,937 in 4,792.33 seconds with zero tracked-file violations.
James returned `ACCEPT R2Q-026 POST-RECOVERY TEST ADAPTER FINAL`.

## Scientific disposition and next step

This is failed pre-science evidence plus mapping recovery. It supplies no
quiet census, persistent-task role, render grammar, terrain, collision,
material, visibility, causality, no-effect, or retail-executable result.
KU-079, KU-080, and KU-081 remain open.

After the clean closure and James verdict, the next nominal successor must use
fresh identities and fix executable mapping provenance within a common mount
namespace (or avoid treating namespace-local device numbers as host-global).
Any later wrapper execution requires a new frozen design, activation, clean
gate, James acceptance, and fresh explicit user authority.
