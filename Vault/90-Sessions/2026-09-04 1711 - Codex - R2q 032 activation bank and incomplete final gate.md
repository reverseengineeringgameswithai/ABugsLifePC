---
type: session
date: 2026-09-04
agent: Codex
topic: R2q 032 activation bank and incomplete final gate
status: banked-activation-final-gate-incomplete
---

# 2026-09-04 1711 - Codex - R2q 032 activation bank and incomplete final gate

## Goal and authority boundary

Bank the completed offline R2q work and leave Git and the Obsidian Vault clean.
Do not launch the game or invoke the R2q/restoration wrappers. Preserve every
immutable predecessor and the round-91 stash. This session does not seek new
runtime or mapping authority and does not treat an interrupted test process as
an accepted gate.

## Preserved predecessor outcomes

The sole R2q-028 wrapper invocation had already stopped at the read-only
activation edge because remount-only device fields changed from frozen 54 to
current 51. James accepted its pre-lock disposition. No one-shot lock,
fallback, game launch, mapping action, or runtime path was created.

R2q-029 source/activation was accepted, then finalization rejected when its
full gate exposed literal frozen-device assumptions in historical recovery
tests. Design-029 is 108,849,231 bytes / `6cd3d734...3da0`; rejection receipt
is 1,636 bytes / `694d0f7f...7f20`.

R2q-030 source was accepted, but the only freezer invocation rejected before
design publication because active dispatch changed historical design-029
bytes. No design-030 exists. The 1,699-byte activation rejection is
`440a7e9b...2403`.

R2q-031 source and activation were accepted. Its 149,901,603-byte design is
`7d826b13...c554`. The full gate found one stale active mapping expectation
and two Python 3.14 teardown errors caused by replacing `os.fstat` for real
descriptors. The 2,763-byte finalization rejection is `f4481e28...aa2`.

## R2q-032 accepted boundary

R2q-032 corrects the active mapping suffixes, scopes the synthetic `fstat`
mock to pidfd 91 while delegating real descriptors, preserves historical
dispatch, and adds the unused R2q-031 absence closure. James returned
`ACCEPT R2Q-032 SOURCE` for commit
`45ae9539d200786064309ffb9a249e526de0897d` / tree
`2292c1a419212fe7f14c3b846e939c690ee830d5`.

Benchmark-018 ran once and is 5,023 bytes /
`c93ea50755377274c01216bce79a4313a83a4cc63f2dfdfb4392c82c084e7bb9`.
Its maximum total is 83,225,718,565 ns, leaving 96,774,281,435 ns below the
180-second ceiling. Final anchor-018 is 1,730 bytes /
`d6951e1178d3372c98975db16ef6a271db55e536d33ba35d87429442c53cab70`.

The design freezer ran once. Immutable design-032 is 204,641,846 bytes /
`0604d37daab86378a730724e54a2bc7ddcc07dbbbd8461db81000cf498e1b2b8`;
its 6,332-byte activation manifest is
`d3dc03ae97f1af91d7827d42c085557c0c1717af26dd68cacfdd328aa9f8f402`.
James returned `ACCEPT R2Q-032 ACTIVATION` at commit
`b6abcb2b547d2b59288af6327711dcfc1cbb0f06` / tree
`e65362de1d30b3ab1f510ba8da02a07e099802ea`.

## Verification and incomplete full gate

Completed final tranches:

- runtime/freezer: 163/163 passed;
- predecessor, one-shot, and continuity: 124/124 passed;
- post-anchor historical/current/benchmark/manifest: 17/17 passed;
- exact maximum-shape capacity: 1/1 passed.

The final capacity accounts are raw 2,689,803,574 / 3,095,391,713 bytes and
zlib9 1,245,497,694 / 1,422,137,007 bytes. The frozen limits are 3,072 MiB raw
and 1,472 MiB stored, with positive margins of 125,833,759 and 121,366,865
bytes for the larger case.

The final command was
`TMPDIR=/dev/shm/ablpc-r2q-032-make-check PYTEST_ADDOPTS='-o tmp_path_retention_policy=failed' make check`.
It reached 79% and displayed one failure marker, but the process was
interrupted before a terminal summary or traceback was captured. It is not an
accepted pass and not a reproducible rejection. The process is gone and the
dedicated scratch directory is absent. A later continuation must run a fresh,
complete full gate.

## Closure and next exact action

The final session audit reports no runtime processes, null sinks, or open
sessions. No game, emulator, restoration wrapper, R2q runtime wrapper, live
census, ptrace, debug-register, process-memory, signal, input, screenshot,
save-state, or mapping action occurred during the offline correction/freeze
sequence after R2q-028's read-only pre-lock stop.

The round-91 stash remains `stash@{0}`, object
`76db1c9ee1ffffce52cea6aee591c24ab6a1c39a`, and was not dropped. KU-079,
KU-080, and KU-081 remain open; there is no new terrain/collision or
persistent-task result.

Next: run a fresh complete full `make check` from isolated scratch. On a real
failure, preserve the traceback and advance to a new immutable successor. On
pass, update this checkpoint, commit the final Vault closure, and request
James's exact clean-tree acceptance before any runtime proposal.

## Links

- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
- [[Decision Log#DEC-225 - Preserve R2q-029 through R2q-031 and bank accepted R2q-032 activation without finalizing it|DEC-225]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)|KU-079]]
- [[Known Unknowns#KU-080 - Does PC terrain collision block laterally, or is it height-only?|KU-080]]
- [[Known Unknowns#KU-081 - Render-side mutation of the collision descriptor table (FUN_0044ca00)|KU-081]]
