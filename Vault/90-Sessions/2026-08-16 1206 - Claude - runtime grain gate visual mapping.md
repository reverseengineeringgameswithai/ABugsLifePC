---
type: session
date: 2026-08-16
agent: Claude
status: independently-accepted-after-correction
tags: [session, re/runtime, re/gameplay]
---

# Runtime grain gate visual mapping

## Goal

Teleport Flik to the EXP-141 standoffs on the live retail game and correlate
every visible grain gate with its mechanism, replacing the manual walking
pass — autonomously, no human at the keyboard.

## Worker result

- All twelve gates mapped ([[EXP-20260816-144 - Runtime grain-gate visual mapping]]):
  nine Tunnels wooden-pole gates (internal level 3, rows 0–8) and three City
  Entrance leaf/pillar gates (internal level 4, indices 0–2). Every teleport
  read `NextLife=0` (all standoffs walkable) with the engine-exact
  nearest-gate index matching the intended mechanism; City states
  `(-1,-1,-1)`. Numerals visible on Tunnels rows 3/6/8.
- Established the autonomous control recipe in [[PC autonomous game control]]:
  **XTEST** input is required (the chooser reads `GetAsyncKeyState`, which
  ignores synthetic `xdotool key --window`); chooser polls VK_DOWN / VK_RETURN
  with a 60 s software-default timeout; the researcher-provided 15-level
  carousel order (City Entrance = Right ×7); carousel position ≠ internal
  level (confirm via `0x00861C84`); no in-level return to select.
- `gate_probe` helper (snapshot + guarded teleport) under the ignored work
  dir; evidence screenshots retained under `evidence/tunnels/` and
  `evidence/city/`.

## Mutation and lifecycle boundary

Retail executable only; the sole target writes were guarded 24-byte
current+preceding teleports ([[PC Flik teleport procedure]]). No grain,
executable, asset, register, or `originals/` write. Ran alongside a separate
researcher/Codex instance; concurrent nested Gamescope sessions conflict, so
that instance was closed with explicit authorization before the solo City
run. Only owned process groups and the owned private sink were terminated;
final audit clean; Wine `Y:` unchanged.

## Durable changes

- New: [[EXP-20260816-144 - Runtime grain-gate visual mapping]],
  [[PC autonomous game control]].
- Updated: [[Known Unknowns#KU-060 - Modified grain-gate physical transition]],
  [[Current State]], [[Experiments MOC]], and this index.

## Audit

[[EXP-20260816-145 - Independent runtime gate mapping audit]] (James)
verified standoffs, distances, verdicts, screenshots, disassembly, write
boundary, and hygiene; REJECT on one isolated defect (two City `dist²`
annotations used truncation, not the engine `sar` helper), corrected in
place to `sar`-8 from settled current (3482/9216/11885) with no identity or
verdict change, then **ACCEPT**.

## Next

- Physical modified-threshold receipts for the untested gates now have
  confirmed approach standoffs.
