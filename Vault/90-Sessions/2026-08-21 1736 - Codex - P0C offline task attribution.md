---
type: session
date: 2026-08-21
agent: Codex
topic: P0C offline task attribution and R2 census boundary
status: complete
---

# 2026-08-21 1736 - Codex - P0C offline task attribution

## Scope

Continue from the accepted P0B operator cleanup using retained evidence only.
No game/emulator launch, live `/proc` read, memory access, debugger action,
signal, save state, asset change, or terrain/collision experiment occurred.

## Implemented analysis

Added the strict argument-free offline analyzer
`scripts/r2p-analyze-p0c-task-attribution.py`, backed by
`reimplementation/ablpc/r2p_p0c_attribution.py`. The first implementation had
28 focused regressions; the correction has 44.
It authenticates the append-preserving P0B tree `1092fcb9...25f2`, collection
`d8ff0e76...44bc2f`, accepted R2o D1-AH-005 evidence, retail/auto-hardware PC
binaries, static export, exact Ghidra source, and the production P0B/R2o
validators before deriving any comparison.

James rejected exact first implementation `f362fae` / tree `de8f1af` for six
publication/semantic/static/ledger/wording families. Its generated `-001`
result remains unchanged at SHA-256 `ecd92bfd...9c7`. The first correction
published only to fresh `task-attribution-002/analysis.json`, SHA-256
`6156b96847936f778577a7ef5fae8a223a0e9c424514b5f324759007ad841f88`.
James rejected exact `923ffb2` / `4db811a` because its complete executed-source
claim omitted imported intermediary `r2c_f0.py`. That output remains preserved.
Fresh `task-attribution-003/analysis.json` is `62af5c09...d6ff`; analyzer and
wrapper SHA-256 values are `a3f35182...813b` and `68410c5c...8563`.

## Result

P0B has exactly 16 tasks at sequences 0–26 and 17 at 27–520. Its sole added
identity is `2086681/34785536`. The last-absent and first-present sample starts
occur `239.282435 ms` and `259.282684 ms` after title keyup; these are
observation bounds, not exact task-read or creation times. The identity remains
observed for an exact `9.859999646 s` first-to-last sample-start span. R2o
D1-AH-005 independently
changes from 16 tasks at open-and-arm to 17 at its first trap. This confirms
the lifecycle topology in two fresh processes and shows that a debugger is not
necessary for the class. It does not prove that the two TIDs are the same
logical worker.

PC-native evidence places the sole direct `CreateThread` call in the Level1a
DirectSound PLAYTRACK path at `0x0042CF04`, targeting worker `0x00440F50`.
P0B's authenticated log append contains Level1a PLAYTRACK then SETMUSICVOL.
That audio-stream worker is the strongest role candidate, but attribution
remains inference: no evidence binds Linux TID `2086681` to the Windows start
routine.

## Decision and boundary

The early 16-task census is not stable; a universal immutable 17-task census
is also unsupported. Offline R2q redesign is justified around an authenticated
gameplay transition, a prospectively fixed repeated-census quiet interval, a
claim no stronger than **pre-attach stable**, an immediate pre-attach recheck,
and continued fail-closed census checks. Dynamic enrollment remains forbidden.
The quiet interval and acquisition budget still require exact freezing and
James audit. No R2q runtime is ready or authorized.

James independently reviewed the retained evidence and agreed that the
correct verdict is **attribution unresolved**: the lifecycle/topology is
confirmed, while neither an immutable census nor creator/role is established.
The rejected first tree passed 2453/2453 before its protocol defects were
found. The rejected second tree added canonical fresh-directory/no-replace
publication, exact topology and no-debugger semantics, log chronology/schema,
complete decoder/thunk/builder spans, expanded source/static pins, and 16
adversarial regressions.
Its 44/44 focused suite and 2469/2469 full gate passed, the latter in 647.40
seconds with zero tracked-file violations, but its source ledger omitted the
`r2c_f0.py` import intermediary. The fresh successor also pins `r2c_f0.py`,
active `r2c_localizer.py`, and the package-init/parser chain; an independent
wrapper-rooted AST closure regression brings its suite to 45/45; the full gate
passes 2470/2470 in 647.23 seconds with zero tracked-file violations. The exact
tree gate passes 2470/2470 in 648.20 seconds with zero tracked-file violations.
James independently regenerated `-003`, matched its 11-entry source ledger to
the actually loaded local modules, replayed the prior counterexamples, and
**ACCEPTED** exact `f2629944b9163ae39e608320e60e7fed76fabb09`, tree
`9c7c1294e60f3c0ed6bb47f9f8575362d9ac1d45`.

## Links

- [[EXP-20260820-005 - R2p task lifecycle diagnostic]]
- [[Decision Log#DEC-194 - Treat the post-title addition as reproduced but the audio role as inferential|DEC-194]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
- [[Known Unknowns#KU-079 - The render-geometry command grammar (the LEVEL.DAT draw-command stream)|KU-079]]
