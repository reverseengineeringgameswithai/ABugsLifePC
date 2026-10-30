---
type: session
date: 2026-09-01
agent: Codex
topic: R2q 025 failed-run mapping recovery
status: complete-final-clean-tree-james-audit-pending
---

# 2026-09-01 0317 - Codex - R2q 025 failed-run mapping recovery

## Goal and authority boundary

Preserve the sole consumed R2q-025 arm, complete exactly one separately
authorized mapping-only recovery, authenticate the post-action state, pass the
full repository gate, update durable research memory, and obtain James's final
clean-tree verdict.

The original R2q wrapper was not retried. The game was not launched again.
The restoration wrapper ran exactly once under activation
`5ff648a2a5e8a66d4aa87c1fc177d4e2f378aee0120d1928a07997755da42e90`
and must never run again. The retained round-91 stash remains `stash@{0}`,
object `76db1c9ee1ffffce52cea6aee591c24ab6a1c39a`, and was not dropped.

## Consumed R2q-025 failure

The sole D1 arm exited 2 during `stage-and-launch` with
`ProcessMapConvergenceError: game process maps did not converge in the bounded
window`. Normal close and the immediate audit could not prove clean state; no
quiet census, debugger acquisition, stopped process-memory range, screenshot
batch, D2 control, or comparison completed. The arm is consumed and cannot
retry.

The retained terminal packet is 118,724,996 bytes /
`d1a337530fed514274e3e6dba8f8e76d3becdd91c6360a5e551a5c27f8bffa04`.
Its pending tree is 22 entries / `4d075fdd...466f`, unverified tree one entry /
`4842c4f1...496d`, journal tree 12 entries / `6918dea8...298`, and emergency
cleanup is `da267c78...1abf`. The exact 201,330,816-byte one-shot lock and
fallback share one inode and SHA `f34a863c...28b0`. The D1 stage and retail
trees remain 2,339 entries at `73da1129...61c` and `78b0a30c...a210`.

## Identity-guarded cleanup

The user separately authorized cleanup of exactly seven PID/start-tick pairs:
`1392949/20167276`, `1392975/20167305`, `1393099/20167326`,
`1393103/20167327`, `1393112/20167344`, `1393142/20167368`, and
`1393185/20167476`. Every target matched before action. TERM cleared four;
after the bounded wait, KILL targeted only matching survivors `1392949`,
`1393099`, and `1393142`. All were then absent. PulseAudio module
`536870916` was already absent. The audit was exactly clear. No relaunch,
mapping mutation, or other process target occurred in cleanup.

## Mapping-only source, activation, and authority

James accepted the distinct recovery source. Source commit
`3ac52dc1036566be92db6cab28a1c43db3d38328` / tree
`675d5b198e076c5668ce542ff4c4cad96b64ba0a` is bound by the 1,188,247-byte
activation above, committed at `43a7310cba28a3a5061e9053ac4faef16745acfd`.
The exact 3,360-byte, mode-0600 authority receipt is
`e9e1710aa331ba823922dca3ca9ce2f861961441f5e728012d5ebf7c73ddd922`.
It binds user item `01a05ace-4d1e-7422-a854-47fd62889052`, prompt item
`msg_0e5b11cd4ba30095016a9637ebc90087d18f0feadfed00e7f8`, and the exact
reply `R2Q025-AUTH:5ff648a2...2e90`. James accepted both activation and
authority.

## Sole mapping result

The mapping wrapper was invoked exactly once and exited 0. Attempt marker
inode `9773594` is 116 bytes / `870a6eabd1858d63045ffe7109f645c6309c5a3d2dc017bd25b007ca5d963c68`.
Published-unverified packet `R2Q-025-YR1-AH-001` has 28 entries and stable
tree `0b0aa4113289df6a8f2e2922b4b833bc10408e819d3889c3c02b79fe94ff4d2b`.
Mapping receipt `f37158da86038bd793ce65c995adf5ea227cb631524d560c5bc44c2423dec383`
records one exchange, zero rollback, parent fsync, stable reread, D1 inode
`9770116` before/retired, and retail inode `9773754` after. P0A R remains
inode `9054047`. Result `243f8966d734b182f93b5711c8817e891a26f89f2fb834489e3b5fdee55722a4`
records mapping-actions one and runtime/input/signals/sink/process-memory zero,
with `terrain_collision_claim:null` and future runtime unauthorized. James
returned `ACCEPT EVIDENCE`.

## Test and adversarial chronology

The first post-action full gate reported 3,885 passed, seven failed, and 13
setup errors. All were stale historical mapping-phase assumptions. A proposed
edit to `tests/test_r2q_quiet_census_design.py` was rejected by James because
that file is benchmark-011 executed source; it was restored exactly to
`c556df9309b55ee2595f7f41cf0cd9d8145e0130c00b966738eb82517a625155`.
James then rejected a test adapter that projected every activation validation
to `require_current=False`; that projection was removed.

The accepted correction exact-gates the post-action mapping, retains the
benchmarked source bytes, supplies the immutable design's historical
predecessor phase only to its offline tests, and leaves the production
current-state validator untouched. Checkpoint commit
`c851110f7fd7be16775667c16fa0da9e745f80c8` / tree
`9c2a495db4d05fc0a83e55c9566a73c345e1b8a3` received James `ACCEPT`.
The unmodified strict success validator passes on that clean tree.

Final full `make check` passes 3,905/3,905 in 6,213.97 seconds and the tracked-
file audit reports zero violations. The final session audit is exactly clear:
no processes, sinks, or open sessions.

## Scientific disposition and next step

R2q-025 produced no accepted quiet census, persistent-task classification,
render grammar, terrain/ground source, collision linkage, material,
visibility, causality, no-effect, or retail-executable result. KU-079, KU-080,
and KU-081 remain open. The next legitimate terrain/collision step is a fresh
offline successor that preserves the full failed-025 and recovery-025 closure,
addresses the process-map convergence blocker, freezes new identities, and
obtains new exact authority before any live action.
