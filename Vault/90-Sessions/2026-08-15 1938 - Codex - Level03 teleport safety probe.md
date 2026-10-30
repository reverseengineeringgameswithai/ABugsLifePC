---
type: session
date: 2026-08-15
agent: Codex
status: completed
related:
  - EXP-20260815-130
  - KU-057
tags:
  - session/runtime
  - milestone/m3
---

# 2026-08-15 1938 - Codex - Level03 teleport safety probe

## Goal

Take over the next Tunnels probe with user-authorized Flik teleportation,
add grain only if needed, and leave a durable safe teleport procedure.

## Result

[[EXP-20260815-130 - Write-assisted Level03 teleport safety boundary]] records
three bounded write receipts. The exact known row-6 floor point
`(501696,30092,494016)` accepted a 24-byte current+preceding relocation and
became the engine's auxiliary coordinate about 10 ms later. In contrast, an
all-three write to a below-floor point and a current+preceding write to the
prior pit-contact tuple each produced an unsafe auxiliary anchor followed by
repeating `NextLife=2` falls. Those loops were procedure errors and consumed
lives; they produced collision `548/0`, not material 1.

The user correctly challenged the natural-gameplay premise: with zero grain,
the pit behind the first grain gate is not controller-reachable. A teleport
past that gate is write-assisted and cannot resolve KU-057. The prior natural
10-grain/open-gate run already shows the one pit funnels to row 7 twice, so it
should not be repeated for row 6.

The durable operational note is [[PC Flik teleport procedure]]. Routine
teleport is bounded to already-proven walkable targets. Unsupported targets
must not receive equal current/preceding or all-three writes; a safe paused or
guarded method has not been accepted.

## Setup corrections

- Gamescope `-g` was required for exact internal game-window focus and working
  DirectInput in the accepted arms.
- Menu inputs had to be held for about 200-250 ms; instantaneous Right events
  could be missed.
- One stale-instruction setup arm loaded Training instead of Tunnels. It was
  rejected before any target write and replaced with a visually verified
  Tunnels arm.
- No grain write occurred in this session.

## Lifecycle

All game/Wine/Gamescope process groups and private sinks were closed. Wine
`Y:` targets `/home/dev/ABLPC/work/copies/BUGS_PC-full-disc`. No originals,
game binaries, assets, or disc images were edited. The disclosed position
writes were volatile; ordinary work-copy log/Wine runtime churn is outside
this claim.
