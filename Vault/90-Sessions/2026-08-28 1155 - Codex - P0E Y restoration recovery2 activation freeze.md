---
type: session
date: 2026-08-28
agent: Codex
topic: P0E Y-only recovery2 source and activation freeze
status: recovery2-consumed-pre-action-failed-evidence
---

# 2026-08-28 1155 - Codex - P0E Y restoration recovery2 activation freeze

## Goal and authority

Continue the terrain/collision prerequisite path by restoring staged `Y:` to
retail, using James as the independent adversarial verifier. After James
accepted the recovery2 architecture for authority, the user supplied the exact
fresh post-YR2 reply `Corret I authorize everything, continue on`. The frozen
scope remains exactly one atomic Y-only stage-to-retail recovery2 mapping
action. It does not authorize a game launch, input, signal, sink action,
process-memory operation, `R:` change, earlier-packet classification, or retry.

## Consumed YR2 boundary

YR2 is consumed and must never run again. Its 104-byte marker has SHA-256
`d89441a52e0a7e4da2c24ee5f0bc7f1a235e223fa64fabf8fd8e47c6b7d298dd`.
The invoking-session report says its first strict `pactl` read failed
transiently. The durable evidence proves the narrower statement: YR2 stopped
with an empty event journal before any mapping action or terminal publication.
Its pending packet contains exactly four leaves:

- `authority.json`: `bec0766242dc469e6e4320c0bfda76d96c3ad7d9bc3bfb03583a250c06f53210`;
- `events.json`: `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570`;
- `plan.json`: `d0739203d11e1bbeb602c017a1ea0bd2e2c19392bdd5f1885c9ce6ce2d00c873`;
- `preserved-pre.json`: `5f3d14b077a0fa553e4826e8acb5ead57c4889e2e84bf77fedcc3c4c366955d7`.

All YR2 terminal, action-account, temporary, and quarantine names remain
absent. `Y:` remains on the P0E stage and `R:` remains on P0A.

## Recovery2 hard-truth result

Protocol `ablpc-r2p-p0e-y-only-restoration-recovery-v2` uses a distinct YR3
marker and packet namespace. It binds the complete immutable YR1/YR2 closure,
requires descriptor-bound namespace and mapping identities, and uses a
cumulative bounded `pactl` observation journal. Each clear gate binds sink
observation starts and completions between the direct census and audit; action
and failure gates carry analogous chronology bounds.

James rejected intermediate revisions for cross-gate stability semantics,
deadline disagreement, unbound observation starts, invalid UTF-8 escape, and
forgeable exception/identity provenance. The accepted journal now durably
records only attempt chronology plus either a closed completed-process result
or `null`. All tool-check and invocation exceptions are the same
provenance-free retryable unavailable result. Only retained return code and raw
base64/size/SHA-bound bytes can derive absent, present, nonzero, malformed,
ambiguous, or decode-error semantics. James round 31 returned
`ACCEPTABLE-FOR-AUTHORITY-AND-SOURCE-FREEZE`; after the exact authority reply
was frozen, round 32 returned `ACCEPTABLE-FOR-SOURCE-FREEZE`.

Exact accepted SHA-256 values are:

- shared restoration mechanism: `172e07605d2dd60ab6abb2224b80a295404c4f8b3938e3ddc9c08068243f4e20`;
- YR2 compatibility layer: `8fdc6f3aa49d99cc7292f3467ef2786df43ba89dd0a997320c79af9411a8273b`;
- recovery2 module: `93c7af5a59404d4d63d6f4ef2e5f53bc6a9e0cf2bd657b91a83730d4fa3608be`;
- recovery2 wrapper: `218bae3f037f83efd0b8a18678765206a0d6edc483d2211811916562a089999a`;
- activation freezer: `ebd1fdfe65cdfb2b0599f6b6eaa1418f0657d8a187c45389ecb1459917f36f39`;
- recovery2 tests: `c5de102b5c18bcc471fdfdef3a1b067722c51c84f98640954159b41f3bb4be22`.

The focused restoration suite passes 162/162 and the broad P0E family passes
805/805. The source-phase full repository gate passes 3,606/3,606 in 2,457.30
seconds with 0 tracked-file violations. Source commit
`14e4a43f60eb5be4f072f06926081c4a90cc0501` / tree
`3e5536191da00dea1cd9e093ee94143b4a56d861` freezes those bytes.

## Activation freeze and stop rule

From that clean source commit, the argument-free dedicated freezer created the
44,957-byte canonical activation anchor, SHA-256
`c611240a3967e7c591a23bc7fc88eb7d0781b947652d9eff5a7482fe866b2ead`.
It binds 21 exact source files plus the composite YR1/YR2 closure, including
markers `567cdf3f...14c7` and `d89441a5...98dd` and YR2's exact four-leaf
pending inventory.

The activation is inert provenance. `P0E-YR3-AH-001.attempted`, all recovery2
packet roots, its action-account prefix, and both mapping scratch names remain
absent. The wrapper has not run. A documentation-inclusive full gate,
activation/docs commit, James exact clean-tree acceptance, and fresh accounted
`make session-audit` remain mandatory before the single authorized mapping
action. No game, mapping change, R2q action, process-memory access, terrain,
collision, render grammar, or task-role result follows from this freeze.

## Sole YR3 invocation and consumed result

Activation/docs commit `1bc9bcd535ed1c9b5d718db290cf62412490999f` /
tree `e0d90708875429f3d8596aa6dd392a2acae3d31f` passed the
documentation-inclusive 3,606-test gate with 0 tracked-file violations. The
activation validator reauthenticated all 21 source files and the predecessor
closure. James round 33 returned
`ACCEPT-EXACTLY-ONE-YR3-INVOKE-AFTER-FRESH-CLEAR-AUDIT`; the fresh pre-action
`make session-audit` was exactly clear.

The sole command
`/usr/bin/python3.14 -I scripts/r2p-restore-p0e-y-recovery2.py` then exited 2
after 20.74 seconds. It reported a malformed strict `pactl` observation and,
while recording failure, `Y-only retained packet durability changed`. The
108-byte consumed marker has SHA-256
`7191e19393383740ae545dbc904cb3653bc77831d27854275533916d97b51e43`.
The pending path is a 58-byte placeholder with SHA-256
`0c0a027d8a7313bc69586dedd1a7a9110583f1017bbcba91b749c6278022f152`.
The 11-entry failed-unverified directory has immutable tree SHA-256
`69daa4a722da5e7a7a545c37464c37167e53795f1424e47e9dc9999e012a0589`.
Its empty event journal has SHA-256
`37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570`;
`mapping_replaced` and `y_parent_fsynced` are false and the reducer action is
`idle`. Every YR3 action-prefix, temporary, and quarantine name is absent.
`Y:` remains staged and `R:` remains P0A. The immediate post-action session
audit was exactly clear, and Git remained clean.

The retained observations are both return-code-zero results with identical
raw PipeWire multiline module listings. The classifier incorrectly treats
continuation lines as standalone `pactl list short modules` rows and therefore
labels the listing malformed. A second defect prevents the production failure
validator from accepting the packet: `_receipt_content_monotonic_lower`
recursively promotes historical predecessor timestamps from an earlier boot
into the current attempt's lower bound. It obtains
`118593490774571` from preserved predecessor content, above current failure
observation `15783718417410` and retained-packet fsync completion
`15783718417180`; monotonic clocks from different boots are not comparable.

James round 34 returned `ACCEPT-AS-FAILED-EVIDENCE`. The exact marker,
authority, plan, preserved-pre closure, empty events, idle reducer, unchanged
mappings, absent scratch/action names, and clear post-audit prove only that the
authorized attempt was consumed before a mapping action. The overall
failed-unverified packet is not production-valid and must not be promoted.
YR3 must never retry. Any successor requires a distinct protocol and marker,
an immutable YR3 failed-state closure, corrected multiline parsing, explicit
separation of historical authenticated chronology from current-boot ordering,
fresh James acceptance, and fresh user authority. No restoration, R2q,
terrain, collision, render-grammar, or task-role result follows.

## Links

- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
- [[Decision Log#DEC-213 - Preserve consumed YR2 and freeze provenance-free recovery2|DEC-213]]
- [[Decision Log#DEC-214 - Preserve consumed YR3 failed evidence and require a distinct recovery3|DEC-214]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)|KU-079]]
- [[2026-08-27 1919 - Codex - P0E Y restoration failed v1 and recovery freeze]]
- [[Current State]]
