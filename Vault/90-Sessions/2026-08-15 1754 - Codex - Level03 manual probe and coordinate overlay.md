---
type: session
agent: Codex
date: 2026-08-15
status: complete
tags:
  - sessions/codex
  - milestone/m3
  - implementation/tooling
---

# 2026-08-15 1754 - Codex - Level03 manual probe and coordinate overlay

## Scope

Resume M3.5 with the researcher manually driving Tunnels while Codex probes
read-only PC state, then suspend the route and add a visible coordinate
overlay so the researcher can steer future manual experiments directly.

## Outcome

[[EXP-20260815-126 - Manual Level03 coordinate-guided probe]] records a
bounded natural-route negative. The control process reached the red mushroom,
upper corridor, and within about 36,378 X/Z units of the then-mislabeled
scanner tuple later corrected to descriptor 572's base by EXP-131
center. One raw `4 -> 3` state-counter transition with flag `0x0002` probably
matched user-observed damage, but collision value stayed 0; no reset bit or
nonzero `NextLife` appeared. `KU-057` remains open.

[[EXP-20260815-127 - Read-only PC coordinate overlay]] adds
`scripts/coordinate-overlay.py` 1.0.0 and companion 1.4.0 integration. The
retail-PC live smoke accepts exact ownership, live read/decode, automatic
translucent window creation, and joined cleanup. The pinned pristine launcher
is unchanged.

Coordinate semantics in this historical session are superseded by
[[EXP-20260815-128 - Live Flik position globals]]: the original display read an
auxiliary/reset-coordinate triple at `0x0059D960`; current live XYZ is at
`0x0059D910`.

## Validation and lifecycle

- Focused coordinate/companion tests: 17 passed.
- Complete repository tests: 566 passed.
- Vault lint: 365 notes, 0 errors, 0 warnings; M4 five-anchor compatibility and
  tracked-file audit passed.
- Live smoke: game PID `69474`, overlay PID `69567`, 266×160 at `+24+24`.
- No original, game asset, executable, target memory/register/code, PS1
  source, or privileged kernel state was modified.
- Both runtime arms ended with empty targeted process and private-sink audits.
- Wine `Y:` was restored to `M3-training-51-grains-full-disc`.

## Next action

When the researcher resumes M3.5, run the companion with `--coordinates`,
select Tunnels, and use the visible X/Y/Z display to reach the then-hypothesized descriptor-571
height/region while a separate 100 ms read-only evidence trace remains armed.
CAP-002 replay determinism stays open and is not required for that manual arm.
