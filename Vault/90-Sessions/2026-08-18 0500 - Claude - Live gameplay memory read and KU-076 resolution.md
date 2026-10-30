---
type: session
date: 2026-08-18
agent: Claude
status: complete
tags:
  - session
  - re/runtime
  - environment/86box
---

# Live gameplay memory read and KU-076 resolution

## Agent

Claude.

## Goal

Enter an actual level in the 86Box/Win95 game and read the **live** level and Flik
values through the v6.0 GDB stub — the gameplay-state non-zero read left open as a
Gate-2 extension in `KU-077`, and by the same action exercise the level load that
`KU-076` needed (does the `CONVPSXTPAGE8` path fault on real Win95?).

Substrate: [[86Box Win95 RE harness]] running in container `abl-win95`, v6.0
`GDBSTUB=ON` build (`work/86box/86box-v6-gdbstub`, dynarec + stub), game at
`C:\PC\BUGS\`, stub on `127.0.0.1:12345`. Continues
[[2026-08-18 0330 - Claude - Win95 and A Bug's Life installed in 86Box]] and the
read+write proof in `KU-077`.

## Outcome

**Both open questions closed.**

1. **KU-076 resolved.** From the level-select menu I focused the game window (mouse
   click, per [[PC autonomous game control]] — headless keys are dropped when the
   game lacks focus) and selected Training with `Return`. The level **loaded to full
   playable 3D with no `CONVPSXTPAGE8` page fault** — Flik and the trainer rendered
   in the training area. The identical `bugs.exe` (sha256 `97c95ba5…`) and assets
   that page-fault in `FUN_00462c30` under classic Wine 9.0 load cleanly here, so
   that crash is **environmental to Wine 9.0, not intrinsic** to the game.

2. **Live gameplay read + live-tracking (KU-077 extension).** In-context
   (`$pc` in `[0x401000,0x4c0000)`), the stub read:
   - **level `0x00861C84` = 17** (reads `0` at the menu → `17` at title and in-level)
   - **Flik `0x0059D910`/`14`/`18` = (−22044, 15860, −19597)** in-level
     (reads `(0,0,0)` at the title before gameplay starts)

   Holding the forward key moved Flik and the position re-read as
   **(−12793, 11822, −6096)** — the delta matches the visible on-screen movement.
   The stub reads **live, changing** gameplay RAM, complementing the earlier write
   proof (write reaches the same live RAM the CPU uses).

## Method / evidence

- Read tool: `work/86box/probe_lvl.py` (gdb-python; gates on `$pc` in the game
  range, then reads level + Flik XYZ + carousel `0x00599AF8` + nextlife
  `0x0059A5B0`). Run economically — a small retry loop, ≤8 connects per read,
  fresh-stub-first — per the stub-fragility caveat in `KU-077`. The stub stayed
  healthy throughout.
- Screenshots (git-ignored `work/86box/logs/`): `lvl_gameplay.png` (Flik + trainer
  in the loaded level), `pos_a.png` → `pos_b.png` (camera tracks Flik walking toward
  the training sign after the forward-hold — the visual counterpart of the position
  delta).
- Navigation gotcha (already in [[PC autonomous game control]]): the level-select
  carousel is keyboard-driven, but keys are **dropped unless the game window has
  focus**; click the game first. Tapped movement keys did nothing at first — a held
  key (`keydown`/sleep/`keyup`) actually moved Flik.

## State transition observed (one table)

| Global | Address | Menu | Title screen | In-level | After holding ↑ |
|---|---|---|---|---|---|
| Level index | `0x00861C84` | 0 | 17 | 17 | 17 |
| Flik X | `0x0059D910` | — | 0 | −22044 | −12793 |
| Flik Y | `0x0059D914` | — | 0 | 15860 | 11822 |
| Flik Z | `0x0059D918` | — | 0 | −19597 | −6096 |

## Still open (Gate-2 extensions)

- A **clean watchpoint** firing on a game write. (Source-verified since:
  watchpoints are a software linked list + page bitmap, range-capable, with **no**
  4-address / DR-register limit — `src/gdbstub.c:142-150,1749-1776`; the 4-limit
  seen earlier was stock gdb's client-side i386 cap, not the stub. See the
  `KU-077` correction.)
- **2C**: does a stub read set page-table A/D bits (perturbing a
  savestate→inspect→replay identity)? Measure, don't assume.

## Links

- `KU-076`, `KU-077` (updated with this evidence).
- [[86Box Win95 RE harness]], [[PC autonomous game control]].
- [[Decision Log#DEC-20260817-147 - Build a GDBSTUB-enabled 86Box to prove Gate 2 memory access]].
