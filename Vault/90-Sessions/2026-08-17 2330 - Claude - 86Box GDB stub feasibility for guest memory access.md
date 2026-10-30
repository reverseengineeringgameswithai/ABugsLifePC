---
type: session
date: 2026-08-17
agent: Claude
status: complete
tags:
  - session
  - re/runtime
  - environment/86box
  - decision
---

# 86Box GDB stub feasibility for guest memory access

## Agent

Claude.

## Goal

Answer the concrete question behind Gate 2 (guest-virtual read/write/watch, see
[[Decision Log#DEC-20260817-146 - Guest memory read write watch is a hard prerequisite, tested before the determinism build]]):
does the **installed** 86Box build expose a GDB stub that can operate on the
game's Win95 **linear/virtual** addresses, and would ChatGPT's proposed first
experiment — break inside known ABL code, then read `0x00861C84` and
`0x0059D910` as linear addresses — actually work? Verify by evidence, not
assumption.

## What was checked and found (confirmed)

**1. The installed b9001 AppImage has NO GDB stub compiled in.**
- Binary `tools/86box/86Box-Linux-x86_64-b9001.AppImage` (v6.0 build 9001),
  main ELF `usr/local/bin/86Box`, BuildID sha1 `fa70f555…`, stripped.
- `strings usr/local/bin/86Box | grep -i gdb` → **empty**. No `gdbstub`, no
  "GDB Stub: Listening on port", no `--gdbstub` option string.
- `86Box --help` (run offscreen: `QT_QPA_PLATFORM=offscreen`) enumerates every
  option; there is **no** stub option. The full set is
  `-A/-E/-F/-G/-I/-L/-M/-N/-P/-O/-R/-S/-V/-W/-X/-Z` — asset/vm/rom/log/lang/
  settings paths only.
- **Evidence weighting (corrected).** The **string scan is the direct
  evidence**: the stub's log string `GDB Stub: Listening on port %d` and the
  `gdbstub` symbols would be compiled into the ELF if `gdbstub.c` were built,
  and they are absent. The **`--help` absence is *consistent* but not
  independent proof** — 86Box calls `gdbstub_init()` automatically from
  `machine_init()` when the stub is compiled in (port `gdbstub_port`, default
  12345), so a stub build adds **no** CLI activation flag and `--help` looks
  identical either way. The corroborating fact is that packaged/stable builds
  ship `GDBSTUB=OFF`. So: strings = direct evidence; the `GDBSTUB=OFF`
  convention = corroboration; `--help` = not evidence either way.

**2. The stub is gated behind a CMake option that stable releases ship OFF.**
- `src/CMakeLists.txt` (86Box master, fetched 2026-08-17):
  ```cmake
  if(GDBSTUB)
      add_compile_definitions(USE_GDBSTUB)
      target_sources(86Box PRIVATE gdbstub.c)
  endif()
  ```
  Option `GDBSTUB`, default OFF. So a release AppImage never has it; to run any
  Gate-2A experiment we must **build 86Box from source with `-D GDBSTUB=ON`**
  (or obtain a dev build that has it). This is the single blocking finding.
- **Build consequence:** `-D GDBSTUB=ON` forces `DYNAREC=OFF` (and disables
  `NEW_DYNAREC` off ARM64). The resulting binary runs the **interpreter core**,
  not the dynamic recompiler. That is fine — arguably better — for
  single-stepping and watchpoints, but it means this binary is a
  **debugger/RE build only**: its timing and any determinism behaviour are
  **not** evidence about the normal dynarec build. Gate 1 (determinism) stays a
  separate build/emulator question.

**3. IF built with the stub, it does exactly what Gate 2 needs — confirmed from
`src/gdbstub.c` (master):**
- **Linear/virtual addressing.** Memory read packets go through
  `readmembl/readmemwl/readmemll/readmemql`; writes through the `writemem*l`
  family. These are the **paged** accessors — the code sets `cpl_override = 1`
  and checks `ABRT_PF`, i.e. full x86 MMU translation is active. So an `m`/`M`
  packet on `0x00861C84` reads the **guest linear** address, translated by the
  **currently active CR3**. ChatGPT's "read `0x00861C84` directly as a linear
  address" works — *provided the game's address space is the active context at
  the moment of the read* (see the CR3 caveat below).
- **Hardware watchpoints.** Z2/Z3/Z4 supported: write (`first_wwatch`), read
  (`first_rwatch`), access (`first_awatch`), matched in `gdbstub_mem_access()`.
  So "set a write watchpoint and break on the game code that writes it" is a
  real capability, not a hope.

**4. The determinism side-effect ChatGPT flagged is real — confirmed.**
- The stub's read path uses the **normal** `readmembl`-family accessors, which
  perform ordinary MMU translation and therefore **can set page-table Accessed
  (and, on write, Dirty) bits** in guest RAM. The stub does **not** use a
  no-side-effect translation path; 86Box's MMU has `mmutranslate_noabrt`-style
  helpers but `gdbstub.c` does not call them for reads.
- Consequence for strict savestate→inspect→replay identity: a debugger `x`
  executes no guest instruction, but it can still mutate guest-visible paging
  metadata (A/D bits live in guest RAM, which a savestate serialises). This is
  the Gate-2C test: measure whether it actually perturbs replay; if it does, the
  fix is a small stub patch to route reads through a no-A/D / no-abort translate
  path. **Test, don't assume.**

## Corrections to the prior plan's assumptions

- **No-ASLR ⇒ stable *virtual* addresses, NOT identical virtual→physical
  mapping.** DEC-146 leaned on "Win9x pre-ASLR makes the CR3 page-table walk
  tractable." That is still true, but the cleaner consequence is: because the
  stub translates **linear** addresses for us, we should depend **only** on the
  game's linear addresses and **never** on physical addresses — the physical
  backing may differ run to run even with identical virtual layout. This removes
  the need to hand-write a CR3/page-table walker for the read/write path; the
  stub is the walker. (A CR3 *read* is still wanted for Gate 2B context proof.)

- **The active-CR3 requirement is load-bearing.** The stub translates through
  whatever CR3 is current when GDB reads. Halt at an arbitrary point and the
  active address space may be another Win9x process/driver, where linear
  `0x00861C84` is unmapped or unrelated. That is exactly why the first
  experiment must **break inside known bugs.exe code first**: when a breakpoint
  at a game code address fires, CR3 == the game's address space and the linear
  read resolves correctly. This is a designed constraint of the experiment, not
  a limitation to fix.

## Emulator determinism vs debugger — the tension to resolve after 2A

86Box gives the **best debugger** (confirmed linear stub + watchpoints) but is
**not** a TAS/deterministic emulator; the determinism route (Gate 1) is PCem
17+st, whose debugger capability is unverified. So 86Box's role here is to prove
the **address-access mechanism** cheaply and decoupled from determinism, exactly
as the 2A/2B/2C ordering intends. Whether the final harness is (a) a
deterministic 86Box config with the stub, (b) PCem-st plus an equivalent
host-side reader, or (c) split roles, is decided **after** 2A shows the mechanism
is real. Not resolved now.

## Gate 2 experiment procedure (ready to run once Win95 + game are installed)

Prereq: run `tools/86box/86Box-gdbstub-628ce40.AppImage`; Win95 OSR2 + the game
installed; the game running at a level (globals populated). **First prove the
existing 86Box GDB path operates on the known ABL linear addresses** — nothing
else. Explicitly **not yet**: no custom CR3 walker, no custom guest-memory
backend, no PCem/libTAS work, no side-effect-free (no-A/D) debugger patch. Fixed
run order:

1. **Launch** the GDBSTUB build with the **debugger port restricted to
   localhost** (see the Security note in the Build record — the stub binds
   `0.0.0.0` by default; use a firewall rule or the loopback bind-patch first).
2. **Connect** GDB: `gdb -ex 'set architecture i386' -ex 'target remote
   127.0.0.1:12345'` (guest is 32-bit protected mode; port `gdbstub_port`
   default 12345, +instance offset).
3. **Break** at a known instruction inside `bugs.exe` (a code address from the
   Ghidra map — e.g. a routine known to touch the level/position globals).
4. **Record `EIP` and `CR3`** at the stop — this proves ABL's address space is
   the active context, so linear reads will resolve (they only resolve
   in-context).
5. **Read `0x00861C84`** (`x/1wx 0x00861C84`) and verify it matches the expected
   internal level/game state. **If this succeeds while stopped inside
   `bugs.exe`, that is the major architecture validation we are after** — it
   proves the stock stub reaches the game's Win95 virtual globals with no custom
   tooling.
6. **Read `0x0059D910`** (`x/3wx`, three int32 XYZ; `0x0059D91C` is a distinct
   dword per the teleport-write bug fix) and verify it corresponds to Flik's
   mapped state/position. Cross-check against `game-memory.py state` semantics.
7. **One deliberately safe write** (`set {int}0x00861C84 = <safe value>`), resume
   one frame, confirm the guest observes the change (HUD/behaviour or a re-read).
8. **Restore** the original value.
9. **Write watchpoint** (`watch *0x0059D910`, Z2), continue, and confirm it
   breaks at sensible ABL code when the game modifies that address.
10. **Only after 5-9 succeed**, investigate the A/D-bit side-effect **separately
    and non-blockingly** (reframed 2C, below). It must not gate the read/write/
    watch proof.

**2C (A/D side-effect) — reframed, does not assume a savestate workflow.** The
only question is: do ordinary stub reads have guest-visible page-table
Accessed/Dirty side effects, and would that matter to the later deterministic
workflow? Probe it directly without relying on any 86Box savestate feature —
e.g. find a mapped guest page whose PTE Accessed bit is currently 0, do a stub
read of it, then re-read the PTE and see whether A flipped. If ordinary GDB
reads are **not** observationally pure, **record that result** and **plan a small
no-A/D / no-abort peek path later** (the stub's `readmembl` path can set A/D;
86Box has `mmutranslate_noabrt`-style helpers it does not currently use). This is
a follow-up for when determinism identity actually matters — not a Gate-2
blocker.

**Gate-2 pass criterion:** steps 5-9 succeed — reads match known values while
stopped in-context, a write is observed by the guest and restored, and a
watchpoint breaks on the writing code. The A/D question (step 10) is recorded,
not required to pass.

## Build record (86Box GDBSTUB AppImage, 2026-08-17)

Built in a throwaway `podman` container (`ubuntu:24.04`), matching the rr-container
pattern; no host `sudo`/dnf, no host state changed, stock b9001 untouched.

- **Source pin:** 86Box `github.com/86Box/86Box`, commit
  `628ce4030691109a1134fdd9e2d052bcd9691448` (shallow master tip; version string
  reports `v7.0` in its logfile banner). Confirm this exact commit's
  `src/gdbstub.c` matches the master claims above if a behaviour ever surprises.
- **Build deps (apt, noble):** `build-essential cmake extra-cmake-modules
  pkg-config ninja-build libfreetype-dev libsdl2-dev libzstd-dev libpng-dev
  libopenal-dev librtmidi-dev libfluidsynth-dev libsndfile1-dev libserialport-dev
  qtbase5-dev qtbase5-private-dev qttools5-dev libevdev-dev libxkbcommon-dev
  libxkbcommon-x11-dev libslirp-dev libx11-dev libwayland-dev wayland-protocols
  libgl-dev` (official guide list with `libsdl3-dev`→`libsdl2-dev`, since SDL3 is
  absent on noble). MUNT/mt32emu is **vendored** (`MUNT_EXTERNAL` OFF by
  default), so no mt32emu package is needed.
- **CMake invocation:** `cmake -B build -S . -G Ninja -D
  CMAKE_BUILD_TYPE=RelWithDebInfo -D GDBSTUB=ON -D SDL2=ON` then `cmake --build
  build -j16`. **Verbatim `grep` of `build/CMakeCache.txt`** (the actual cache
  values, not a summarized field — 86Box has **no `NEW_NT` option**; the
  interpreter-forcing pair is `DYNAREC`/`NEW_DYNAREC`):
  ```
  CMAKE_BUILD_TYPE:STRING=RelWithDebInfo
  DYNAREC:BOOL=OFF
  GDBSTUB:BOOL=ON
  MUNT:BOOL=ON
  NEW_DYNAREC:BOOL=OFF
  SDL2:BOOL=ON
  USE_QT6:BOOL=OFF
  ```
  Both `DYNAREC` and `NEW_DYNAREC` are `OFF`, forced by `GDBSTUB=ON` at
  `CMakeLists.txt:165-169`; Qt is 5.15.13 (`USE_QT6=OFF`); MUNT is vendored.
- **Artifacts + hashes:**
  - Raw ELF `build/src/86Box`, 103,956,552 bytes, not stripped
    (has `debug_info`), BuildID sha1 `eab90d8f1f9ba0bcd6c6a6091d2c8a37a93604ec`,
    sha256 `fafa0af4e39d011130c0cf484a29deaea3de6a939f67532b67f5aab94756b4ae`.
  - Packaged with `linuxdeploy` + `linuxdeploy-plugin-qt` into
    **`tools/86box/86Box-gdbstub-628ce40.AppImage`** (git-ignored via
    `/tools/86box/*`), 49,076,728 bytes, sha256
    `7cd47fd11c5963fcbf854586f4584990b898822a20e1b100dc453b7c85fef8f7`.
- **Verification — stub present (Tier 1):** the built binary contains the stub
  log strings (`GDB Stub: Listening on port %d`, `GDB Stub: Failed to bind on
  port %d`, `GDBSTUB_BREAK_RWATCH/AWATCH`) and symbols (`gdbstub_init`,
  `gdbstub_client_thread`, `gdbstub_client_read_reg`, …) — all **absent** from
  stock b9001.
- **Verification — stub listening (Tier 2):** launched headless in-container
  (Xvfb + `LIBGL_ALWAYS_SOFTWARE=1`) on a minimal 430vx config; `ss` showed
  `LISTEN 0.0.0.0:12345` owned by 86Box's `qt_thread`, the logfile printed
  `GDB Stub: Listening on port 12345`, and the machine started
  (`Allocated 16.00 megabytes of large pages for RAM`). The socket is bound at
  the top of `machine_init()` (before `machine_init_ex()` loads any ROM), so it
  opens whenever emulation starts.
- **Verification — host portability:** the AppImage **runs on Fedora 44**
  (`--help` prints usage, rc 0) despite being built on Ubuntu 24.04, and
  `--appimage-extract` works FUSE-free. Bundles the `xcb` Qt platform (not
  `wayland`), so run it under X (`QT_QPA_PLATFORM=xcb`, or the game's
  Gamescope/Xwayland), not bare Wayland.
- **Security — the GDB listener binds `0.0.0.0:12345` (ALL interfaces),
  hardcoded `INADDR_ANY` at `src/gdbstub.c` ~L2654-2658.** That exposes a full
  guest memory + register read/write debugger to the LAN whenever a machine is
  running. **Do not expose it to the network.** Before any routine use, restrict
  port 12345 to loopback: either a host firewall rule dropping 12345 on
  non-loopback interfaces, or (preferred) a one-line debugger-build-only patch
  changing `.sin_addr.s_addr = INADDR_ANY` to `htonl(INADDR_LOOPBACK)` (the
  `htonl()` matters — a bare `INADDR_LOOPBACK` binds the wrong address) and
  rebuild. Gate-2 launch step 1 enforces this. The current artifact is
  **unpatched**, but there is no live exposure while nothing runs it — the socket
  opens only when 86Box starts a machine.
- **Config gotcha for the Gate-2 run:** a minimal 86Box config **must** set
  `[Input devices] mouse_type = 2_button` (any non-empty value). With
  `mouse_type` absent, `config_load` passes `NULL` to
  `tablet_get_from_internal_name` (`config.c:787`) and 86Box **segfaults on
  startup** — a real 86Box bug, unrelated to the stub. Also give the chosen
  machine a real BIOS ROM so it starts cleanly to "no boot device".
- **Teardown:** container `abl-86box-build` removed; the `ubuntu:24.04` base
  image is left cached (prunable). The AppImage was copied out before teardown.

## Files inspected

`tools/86box/86Box-Linux-x86_64-b9001.AppImage` (extracted to scratchpad:
`usr/local/bin/86Box`, `net.86box.86Box.desktop`, `AppRun`);
`Vault/10-Environment/86Box Reference Machine.md`;
`Vault/00-System/Environment Status.md`; 86Box master `src/gdbstub.c` and
`src/CMakeLists.txt` via WebFetch. No repo binaries or `originals/` touched; the
AppImage was extracted read-only into the session scratchpad.

## Changes made

This session note (incl. the Build record above); `DEC-20260817-147`; `KU-077`
in [[Known Unknowns]]. No repo **code** changed. One git-ignored artifact added:
`tools/86box/86Box-gdbstub-628ce40.AppImage`. A GDBSTUB-enabled 86Box was built
and run in a disposable podman container (now torn down); a stock `86Box --help`
and the new AppImage were run headless on the host (both exit cleanly).

## Unresolved questions

`KU-077` (the residual Gate-2 tests: reliable in-context reads at a code
breakpoint, the A/D side-effect impact on replay identity, whether any 86Box
config is deterministic enough to pair the stub with Gate 1). Whether the
b9001-matching source tag's `gdbstub.c` differs from master (confirm against the
exact tag we build). Whether PCem-st exposes any equivalent linear read/watch.

## Recommended next action

**Done:** the GDBSTUB build exists and is verified (see Build record) —
`tools/86box/86Box-gdbstub-628ce40.AppImage`. **Next (blocked on user):**
interactively install Win95 OSR2 + the game in that build, then run the Gate-2
procedure above (2B code-breakpoint → 2A read/write/watch of `0x00861C84` and
`0x0059D910` → 2C A/D side-effect). Remember the `mouse_type` config gotcha. Do
not invest in the PCem-st determinism build until Gate 2A shows the
address-access mechanism is real.

## Process audit

The 86Box build and its headless test runs happened **inside a disposable
podman container** (`abl-86box-build`, now removed); the emulator that started
there was killed and the container torn down. On the **host**: the stock
`86Box --help` and the new AppImage were run headless (offscreen/`--help`), and
both the stock and new AppImages were `--appimage-extract`ed into scratchpad —
all read-only, no VM left running, no game/Wine/Gamescope session. No
`originals/` access. Host state change: one git-ignored file added under
`tools/86box/`; the `ubuntu:24.04` base image is cached (prunable). `ntsync`
restore (from the rr session) remains a pending user action, unrelated to this
work.
