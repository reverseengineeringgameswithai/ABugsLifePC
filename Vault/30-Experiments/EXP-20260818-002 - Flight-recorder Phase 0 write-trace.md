---
type: experiment
id: EXP-20260818-002
date: 2026-08-18
question: 'Can an emulator-side C write-trace (DEC-20260818-149 Phase 0) reliably capture every write to a game global — reproducing the EXP-20260818-001 watchpoint finding (writer 0x004ab889 → 0x0059D910) without gdb — and is it the right foundation for the flight recorder?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: 86Box v6.0 GDBSTUB build (exec386 interpreter) PATCHED with the ABLREC Phase-0 hook, running real Win95 OSR2 + A Bug`s Life in podman container abl-win95; source-built in abl-86box-v6
environment_version: 86Box tag v6.0 (4fef696), patch tools/86box/patches/86box-v6.0-ablrec.patch
working_directory: /home/dev/ABLPC
configuration: in-level Training gameplay; write-trace window [0x0059D900,0x0059D930); Flik moved ~3 s via XTEST-held Up; dumped via SIGUSR1
artifacts:
  - tools/86box/patches/86box-v6.0-ablrec.patch
  - work/86box/logs/ablrec.txt
  - work/86box/logs/ablrec2_gameplay.png
addresses:
  - "0x004ab889"
  - "0x004ab88f"
  - "0x004ab896"
  - "0x00440802"
  - "0x0043e6ee"
  - "0x0059D910"
  - "0x0059D920"
  - "0x00454000"
file_offsets: []
result: phase-0-PASS-c-write-trace-reproduces-writer-reliably-and-reveals-full-writer-set
created: 2026-08-18T20:00:00
---

# Flight-recorder Phase 0 write-trace

## Question

`DEC-20260818-149` decided the flight recorder must be **emulator-side C
instrumentation**, not the fragile gdb-watchpoint transport
([[EXP-20260818-001 - Watchpoint path and first forensic tuple for Flik position]]).
Phase 0 is the go/no-go: does a C write-hook on 86Box reliably capture **every**
write to a game global — reproducing the EXP-001 writer `0x004ab889 → 0x0059D910`
without gdb?

## Method

Patched the v6.0 GDBSTUB build (`tools/86box/patches/86box-v6.0-ablrec.patch`):
a hook on the 32-bit write accessors records `{tsc, cr3, pc, oldpc, addr, val,
width}` for writes into `[0x0059D900,0x0059D930)` (Flik position struct) to a 64K
ring; `SIGUSR1` dumps it. Built in `abl-86box-v6`, deployed to `abl-win95`,
booted Win95, entered Training gameplay (PointerRoot input recipe,
[[86Box Win95 RE harness]]), moved Flik ~3 s, sent `SIGUSR1`.

**Key obstacle solved.** A first build hooked only `writememll`/`writememll_no_mmut`
and caught just **1** write (the level-load init). 86Box has a fast-write cache
(`writelookup2`): the op-side macro (`cpu/386_common.h`) writes **directly to the
page backing** on a cache hit, bypassing the accessors. (The gdb watchpoint fired
repeatedly only because gdb re-inserts it each `continue`, and each insert calls
`flushmmucache()`.) Fix: mark the Flik page in `gdbstub_watch_pages` at init and
gate `addwritelookup` to never cache a marked page — so every write to that page
stays on the slow path through the hooked accessors.

## Evidence

After the fix, one ~3 s movement produced **987 records** (range only). The
writer histogram:

| writer (oldpc) | count | writes |
| --- | ---: | --- |
| `0x004ab889` / `88f` / `896` / `899` | 53 each | `0x0059D910`/`14`/`18`/`1c` (X,Y,Z,W vector copy) |
| `0x00440802` / `80b` / `811` | 210 each | `0x0059D920`/`24`/`28` (a second coord triple) |
| `0x0043e6ee`, `0x0043e708…731` | few | level-load init writes |
| `0x00003626`, `0x00003707` | 12 each | low-address bulk writers over the whole window |

The EXP-001 writer reproduced exactly, many times:

```
cr3=00454000 pc=004ab88b oldpc=004ab889 addr=0059d910 val=ffffaa20 w=4
cr3=00454000 pc=004ab88b oldpc=004ab889 addr=0059d910 val=ffffa9e4 w=4
```

`oldpc=0x004ab889` (the `mov [edx],eax` store), `pc=0x004ab88b` (trap-after, as in
EXP-001), `cr3=0x00454000` (ABL). In-game FPS stayed ~119 Hz — the hook is not a
perceptible cost.

> **Artifact note (added post-James):** the `SIGUSR1` dump overwrites one file, so
> `work/86box/logs/ablrec.txt` was later replaced by the **Phase 1** run
> (1473 records / 52 `0x004ab889` hits; preserved at
> `work/86box/logs/ablrec-phase1.txt`). The Phase-0 numbers above (987 records /
> 53 hits) are as-recorded here and are **not** re-derivable from the current live
> file. Every writer named here still appears in the Phase-1 dump; the
> fresh-context James audit re-confirmed the qualitative findings. Future runs
> should dump to per-run filenames.

## Result — Phase 0 PASS

- The C write-trace **reliably** captures the movement writer (`0x004ab889 →
  0x0059D910`, 53 hits) — reproducing EXP-20260818-001 without gdb, and without
  any of its fragility (no leftover watchpoints, malformed stop-replies, or
  async non-determinism). The recorder foundation of `DEC-20260818-149` is
  validated.
- It also delivers **new forensic value the watchpoint could not**: the *full*
  set of writers to Flik`s position struct in one capture — the X/Y/Z/W vector
  copy at `0x004ab889`, a **second** writer (`0x00440802…`) owning the
  `0x0059D920` triple, the level-load initialisers, and low-address bulk writers.
  Naming these and their callers is downstream analysis; `oldpc` gives each
  writer`s exact EIP.
- Open questions resolved for Phase 0: `cpu_state.oldpc` = the writer`s EIP
  (matches the EXP-001 store); `cr3` global is correct at the write site
  (`0x00454000` for all game writes); FPS impact negligible.

## Boundaries / next (Phase 1)

Window, widths (only 4-byte hooked), CR3 filter, and dump format are hard-coded;
old-value is not recorded (derive offline from consecutive same-addr records, or
add a pre-write backing read in Phase 1). The `SIGUSR1` dump is best-effort
(not async-signal-safe) and overwrites one file. Phase 1: all widths, a
configurable range set + CR3 filter, and a full `dump_mark()` bookmark package
(trace window + guest RAM + registers + frame). Phase 2: offline query tools.

## Links

- [[Decision Log#DEC-20260818-149 - Build the runtime flight recorder as emulator-side C instrumentation, not gdb watchpoints]],
  [[EXP-20260818-001 - Watchpoint path and first forensic tuple for Flik position]],
  `tools/86box/patches/README.md`, [[86Box Win95 RE harness]], `KU-077`.
