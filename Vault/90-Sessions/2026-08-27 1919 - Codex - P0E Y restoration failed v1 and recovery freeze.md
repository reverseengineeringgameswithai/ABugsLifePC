---
type: session
date: 2026-08-27
agent: Codex
topic: P0E Y-only failed v1 and distinct recovery freeze
status: recovery-activation-frozen-runtime-uninvoked
---

# 2026-08-27 1919 - Codex - P0E Y restoration failed v1 and recovery freeze

## Goal and authority

Continue the terrain/collision prerequisite path by restoring the staged `Y:`
mapping, using James as the independent adversarial verifier. The user
authorized a distinct mapping-only recovery after the accepted v1 arm failed,
and separately retained the later exact R2q two-launch scope. The game and R2q
remain barred until retail `Y:` is durably restored and James accepts that
result.

## Consumed v1 failure

James accepted exact clean commit `788e6fa` for one invocation of the original
Y-only restoration. That sole invocation consumed marker
`P0E-YR1-AH-001.attempted`, SHA-256
`567cdf3f20bd06c9320b8bc5cd26e8ab00bd6601e72ead540ba3542c33ee14c7`,
then failed before any mapping action with `Y-only packet contains an unowned
leaf`. Its retained pending packet has exactly one canonical 749-byte
`authority.json`, SHA-256
`b7a61db30c786e31c54348ecb3232a54fb94dadb64bceb203a8e0f7949a3b599`.
All v1 version, published, failure, action-account, temporary, and quarantine
names remain absent. James returned `ACCEPT-AS-FAILED-EVIDENCE`; v1 is consumed
and must never retry. `Y:` remains staged and `R:` remains P0A.

A bounded filesystem reproduction showed that one reused retained directory
description could omit a newly linked entry while independently opened `.`
descriptions were stable. This is evidence for the correction, not a claim
that Btrfs or the kernel is the root cause.

## Distinct recovery and hard-truth audit

The new protocol uses marker `P0E-YR2-AH-001.attempted` and separate recovery
pending, published-unverified, failed-unverified, action-account, temporary,
and quarantine names. Its activation binds an immutable v1 closure captured
twice: exact marker bytes/identity; exact pending directory and authority
bytes/identity; absence of every other base/version/terminal/scratch name; and
two fresh action-parent inventories rejecting every matching prefix.

The shared writer now enumerates directories only through fresh `openat(".")`
descriptions bound to retained descriptors. If a link succeeded but later
bookkeeping failed, exact same-inode/same-byte leaves are reconciled as owned
before propagation, while competitors fail closed. Failure terminals bind the
exact lexical retained identity set and a final packet fsync after the complete
failure snapshot plus mapping and cleanup repairs. The fsync timestamp must be
no earlier than every authenticated pre-fsync monotonic observation and no
later than the failure observation.

James rejected successive candidates for forgeable link-repair ordering,
impossible base/version interleave, incomplete final-fsync chronology, and an
authority-only attempt timestamp not bound by marker bytes. The accepted source
samples claimed time after exclusive marker creation, includes it in the
fsynced payload, and validates those exact bytes. The full authority-only
fixture rejects a claimed-time mutation after failure/manifest rebinding.

Final exact SHA-256 values are:

- shared mechanism `a14fa9c92f465cc41db587fd99daff376202f328926fa731797187ff7c92fe1f`;
- recovery module `52ffde418ed588312a187b7f23c68a5c205f5306301c1224861803a957fa96ff`;
- recovery wrapper `bd51de6b728cb51b7d85a24640906dd93478684be7da0fd08fe110f8080d30da`;
- recovery freezer `2f86d7d67003e17f8ed6c42d20d2d44d038d4c7e049dd5022bb098ed8b201555`;
- shared tests `e58a93b3344d0ec8def7712d670bed592f21ccaf2c007acada39565662d3cdb4`;
- recovery tests `068579db520b6a1c2caf7dae8a73ef7b38fa25ae362d8162cefa07ea18e483e7`.

The focused suite passes 115/115. James authenticated the exact hashes and
returned `ACCEPTABLE-FOR-SOURCE-FREEZE`. The full repository gate passed
3,559/3,559 in 2,485.28 seconds with 0 tracked-file violations. Source commit
`32d8a839d6894ddc9b0b40fb6aebc3851449d4ca` / tree
`08ea9ade4279cb731cea7996534cf7af52aa5e9f` freezes the source.

## Activation freeze and boundary

From that clean source commit, the argument-free dedicated freezer created the
9,270-byte canonical recovery activation, SHA-256
`62e05bb578fcb503c934aa0af33c28d4dd4013e631fb4a3c7aa809e3c4efbe69`.
It binds 18 exact source files plus the immutable v1 closure, including marker
`567cdf3f...14c7` and pending inventory exactly `["authority.json"]`.

This anchor is inert provenance, not permission or a runtime result. The new
attempt marker remains absent and the recovery wrapper has not run. No game,
Wine/Gamescope launch, input, signal, sink, process-memory, mapping, R2q,
terrain, collision, or task-role action occurred during the recovery source or
activation freeze. A documentation-inclusive full gate, activation commit,
James exact clean-tree acceptance, and fresh clear pre-action session audit are
still required before the single authorized recovery action.

## Links

- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
- [[Decision Log#DEC-212 - Preserve failed Y-only v1 and freeze a distinct mapping recovery|DEC-212]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)|KU-079]]
- [[2026-08-27 1457 - Codex - P0E Y restoration source and activation freeze]]
- [[Current State]]
