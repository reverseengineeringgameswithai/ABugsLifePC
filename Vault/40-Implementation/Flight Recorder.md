---
type: implementation
updated: 2026-10-02
tags:
  - implementation/flight-recorder
  - environment/86box
---

# Flight Recorder (runtime forensic write-trace)

Durable plan + **resume point** for the emulator-side flight recorder
([[Decision Log#DEC-20260818-149 - Build the runtime flight recorder as emulator-side C instrumentation, not gdb watchpoints]]).
If context is lost, read this note first, then the linked DEC/EXPs.

## Goal & principle

Record write-**evidence** during one playthrough, analyse it offline (**forensic
replay**: "who wrote X? value timeline? group by writer"). This is separate from
**experimental replay** (restore a moment, change X, continue), which needs a
machine checkpoint and is deferred to Phase 3. Determinism is **not** required.
DuckStation/PS1 is out of scope (cross-port).

Why C-side, not gdb watchpoints: the gdb/RSP transport is too fragile
([[EXP-20260818-001 - Watchpoint path and first forensic tuple for Flik position]]).
The v6 stub build runs the **interpreter**, so every guest write goes through the
`mem.c` accessors — a reliable hook point.

## Phases & status

- **Phase 0 — DONE ✅** ([[EXP-20260818-002 - Flight-recorder Phase 0 write-trace]]).
  Hook the 32-bit write accessors for a fixed Flik-position window, ring buffer,
  `SIGUSR1` dump. Reproduced `0x004ab889 → 0x0059D910` reliably (53 hits) without
  gdb; captured the full writer set for Flik`s struct at ~119 Hz.
- **Phase 1 — DONE ✅** (verified in-level, dump `work/86box/logs/ablrec.txt`).
  Generalised: **all widths** (byte/word/long — 6 hook sites), a **configurable
  range table** of 4 globals (Flik pos, level `0x00861C84`, carousel `0x00599AF8`,
  NextLife `0x0059A5B0`; all their pages marked at init), `cr3` kept in each record
  (offline filter: 1437 game `cr3=00454000` vs 36 boot `cr3=0` in one run), and a
  richer dump header (`nranges`, `dump_eip`, `dump_cr3`, range list). Regression
  held (`0x004ab889 → 0x0059D910`, 52 hits) and new writers surfaced — e.g.
  `0x0043dabb` sets the level global to `1`; a byte-wise writer `0x00419123`
  touches Flik`s struct. Still ~119 Hz. **Deferred to Phase 1b:** the full
  `dump_mark()` RAM+frame bookmark package, and qword (8-byte) writes.
- **Phase 2 — DONE ✅** (`scripts/ablrec-analyze.py`, tests
  `tests/test_ablrec_analyze.py`). Offline query tool over a dump:
  `who-wrote <addr>` (writers grouped by EIP, byte-overlap match),
  `timeline <addr>` (chronological old→new; first old is `?`, the ring window
  edge), `writers` (census), `cr3-split` (game vs boot), and **`--name`/`name`**
  which resolves each writer EIP to its **containing Ghidra function** (nearest
  entry ≤ EIP, approximate — the export has no sizes) plus the live `objdump`
  instruction. Parsing/queries are pure and fixture-tested; `--name` is live
  (needs `objdump` + `bugs.exe` + the Ghidra index). Already earning its keep:
  `FUN_00410100` sets the level global `0x00861C84` to `0x11` (=17), and
  `FUN_0043f9e0` writes the `0x0059D920` coord triple via `[esi+0x10/14/18]`.
  Examples:
  `python3 scripts/ablrec-analyze.py who-wrote 0059d910 --width 4 --name`;
  `… timeline 00861c84`; `… writers --name`; `… cr3-split`. Default dump is
  `work/86box/logs/ablrec.txt`; default cr3 filter is the game space `0x00454000`
  (`--cr3 all` to include boot).
- **Phase 3 — deferred.** Full-machine checkpoint at a mark for
  restore→modify→continue. Requires testing whether 86Box savestates reliably
  restore the running game (never assumed).

## How it works (Phase 0 mechanism — the load-bearing details)

- **Hook:** `ablrec_hook(addr, val, width)` in `mem.c`, called right after
  `GDBSTUB_MEM_ACCESS` in the write accessors. `addr` is guest-**linear**; record
  `{tsc, cr3, cpu_state.pc, cpu_state.oldpc (=writer EIP), addr, val, width}` to a
  64K circular buffer when `addr` is in a watched range.
- **Fast-write-cache defeat (critical):** 86Box has a fast-write cache
  (`writelookup2`); the op-side macro in `cpu/386_common.h` writes directly to the
  page backing on a cache hit, **bypassing the accessors** (this is why a naive
  hook caught only the level-load init write). Fix: on first use, mark each
  watched page in `gdbstub_watch_pages` and call `flushmmucache_write()`; and gate
  `addwritelookup` to `return` early for any page in `gdbstub_watch_pages`, so
  marked pages are never cached and every write to them stays on the slow path.
  (The gdb watchpoint only worked because gdb re-inserts it each `continue`,
  re-flushing the cache.)
- **`cpu_state.oldpc`** = the writer`s instruction start (better than the
  watchpoint`s trap-after `pc`). `cr3` global = active CR3 (game = `0x00454000`).
  `tsc` = ordering counter. All are in `cpu/cpu.h`; `mem.c` includes it. NB:
  `#include <signal.h>` must go **before** `cpu.h` (cpu.h `#define cs …` collides
  with signal.h`s `sigcontext.cs`).
- **Dump:** `SIGUSR1` → `ablrec_dump()` writes the ring to `/vm/logs/ablrec.txt`
  (host `work/86box/logs/ablrec.txt`). Handler registers on first hook call (any
  write), so `SIGUSR1` is safe after boot. Best-effort, not async-signal-safe.

## Source of record & build/deploy

- **Patch (tracked):** `tools/86box/patches/86box-v6.0-ablrec.patch`
  (+ `tools/86box/patches/README.md`). The built binary is **git-ignored** at
  `work/86box/v6/86Box` (backup of the pre-recorder stub: `…/86Box.pre-ablrec`).
- **Build container:** `abl-86box-v6`, source at `/root/86Box` (git tag `v6.0`,
  `4fef696`), build dir `/root/86Box/build` (ninja). Edit `src/mem/mem.c`,
  `cd build && ninja` (incremental ~seconds), then
  `podman cp abl-86box-v6:/root/86Box/build/src/86Box work/86box/v6/86Box`.
- **Runtime container:** `abl-win95`. `work/86box` is bind-mounted to `/vm`;
  `tools/86box` to `/tools`. Launch (headless):
  `setsid … DISPLAY=:99 … /vm/v6/86Box -R /tools/roms -P /vm/config -L /vm/logs/emu.log -N`
  (needs `QT_QPA_PLATFORM=xcb`; `libvulkan.so` symlink present; comm is
  `qt_thread`, so kill by `/proc/*/exe` path, not name).

## Getting into a level to test (the input recipe)

Stub build halts the CPU at reset → boot-kick with one
`gdb -batch -ex "target remote :12345" -ex continue` (killing gdb leaves the guest
running). Win95 runs ScanDisk after an unclean stop (~95 s to desktop). Then, all
keys via XTEST with the **host pointer parked over the canvas** (PointerRoot focus;
no WM on `:99`):

1. Start→Run (`Ctrl+Esc`, `r`) → `command.com`. In the DOS box, cd in single
   components (`cd \`, `cd pc`, `cd bugs` — one backslash flakes) then
   `bugs.exe log cheat`. Type with `xdotool type --delay 90` (fast typing drops
   chars). There is **no PLAY.BAT**; the only exe is `BUGS.EXE`.
2. Carousel: `Right`/`Left` taps (training = start). Confirm with a **held**
   `Return` (`keydown; sleep 0.5; keyup` — the menu polls), then a held `Space`
   to advance the title into gameplay. `xset r off/on` around held keys.
3. Move Flik with held `Up`. `SIGUSR1` the 86Box main PID (thread-group leader
   whose `/proc/PID/exe` is 86Box), then read `work/86box/logs/ablrec.txt`.

Full recipe: [[86Box Win95 RE harness]], [[PC autonomous game control]].

## Key addresses (watched globals)

- Flik position struct `0x0059D910` X / `…14` Y / `…18` Z / `…1c` W;
  a second coord triple at `0x0059D920/24/28`.
- Level global `0x00861C84`; carousel counter `0x00599AF8`; NextLife `0x0059A5B0`.
- Added by [[EXP-20260818-003 - Runtime reset and grain-gate captures with the flight recorder]]:
  the tracked patch's table now has seven ranges, adding the auxiliary/reset
  triple `0x0059D960..6C` (KU-062), Tunnels grain-gate state `0x00599C60..80`
  (KU-067) and the grain-count candidate range `0x0059D9B0..C0`.
- Known writers (from EXP-002): `0x004ab889…899` (Flik XYZW vector copy),
  `0x00440802…811` (the `0x0059D920` triple), `0x0043e6ee…731` (level-load init).

## Record format (Phase 1 text dump)

Header: `# ABLREC total=N shown=M nranges=K dump_eip=<8hex> dump_cr3=<8hex>` then
`K` lines `# range i [lo,hi)`. Then per record:
`<tsc> cr3=<8hex> pc=<8hex> oldpc=<8hex> addr=<8hex> val=<8hex> w=<width>`.
`oldpc` is the writer EIP; `pc` is the next instruction; `val` is the low 32 bits
of the new value. Old value is not stored — derive offline as the previous
record`s `val` for the same `addr`. Filter to the game by `cr3=00454000`.
