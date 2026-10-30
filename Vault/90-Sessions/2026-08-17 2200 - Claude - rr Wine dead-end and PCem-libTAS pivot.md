---
type: session
date: 2026-08-17
agent: Claude
status: complete
tags:
  - session
  - re/runtime
  - implementation/tooling
  - decision
---

# rr Wine dead-end and PCem-libTAS pivot

## Agent

Claude.

## Goal

Establish whether deterministic record/replay/rewind of the PC game is
achievable, to decide whether PC runtime investigation is viable or whether to
move dynamic work to PS1. This ran long; the outcome is a settled architecture,
recorded here and in [[Decision Log#DEC-20260817-145 - Deterministic replay via libTAS + single-threaded PCem, not rr]].

## What was tried and what happened

The user removed the `ntsync` kernel module (`sudo modprobe -r ntsync`) so that
`rr` could record Wine.

- **`rr` works on the game — proven.** But not on the host Wine 11. Wine 11's
  new **WoW64** flips the CPU between 32/64-bit inside one process, which `rr`
  cannot follow; both packaged `rr` 5.9 and a from-source `rr` master segfault
  on any Wine 11 command. The working combination is **classic 32-bit Wine
  (Ubuntu 9.0) inside a podman container**, where the game is a genuine 32-bit
  process. `rr` **master** had to be built (Ubuntu's `rr` 5.7 FATAL-aborts:
  it does not know this CPU — Ryzen 9800X3D, Zen 5, CPU code `0x40f40`
  ext-family `0xb`; master maps it). With that stack, `rr record wine cmd /c
  ver` records and `rr replay -a` replays deterministically (both exit 0), and
  a full **game** trace replays deterministically (`rr replay -a` exit 0) with
  **reverse execution proven at the instruction level**: forward 150 then
  `reverse-stepi 150` returns the PC to the exact starting instruction (C==A),
  and a re-step reproduces it (B'==B) — including on 32-bit game code
  (`0xf7ef…` addresses).

- **But the game does not run under the classic Wine `rr` needs.** Under
  classic Wine 9.0 it boots to the intro but **crashes/hangs loading a level**
  (see the CONVPSXTPAGE8 reproduction below). On Wine 11 (host) it runs. So
  there is no available environment where the game both **runs** and is
  **rr-recordable**: the Wine that records it (9.0) crashes it; the Wine that
  runs it (11) cannot be recorded. Bridging that gap would mean building
  classic 32-bit Wine 11 from source — large, uncertain — and even then the
  ergonomics are poor (rr crawls on this game, an 8.3 GB trace for 60 s, VNC
  needed to view the headless container).

## CONVPSXTPAGE8 crash — exact reproduction (preserve)

- **Status:** Wine-version-specific, root cause **unconfirmed**. Reproduces on
  classic Wine 9.0; absent on Wine 11. Not yet compared under Win95/PCem, which
  is the discriminating third data point.
- **Fault:** `wine: Unhandled page fault on read access to 8BA050B8 at address
  00462F9D`. The read target `0x8BA050B8` is above 2 GB (the inaccessible
  "kernel" half of the 32-bit space) — a corrupt/uninitialised pointer, not a
  memory-size issue.
- **Location:** inside `FUN_00462c30` (the PSX-tpage→display converter,
  `CONVPSXTPAGE8`), during `level00\level.raw` load, immediately after the log
  line `MEM : SOFT Pixel buffer for tpage 0 created`. It is intermittent
  (sometimes the page-fault crash, sometimes a hang), the signature of an
  uninitialised pointer.
- **Interpretation (inferred):** the corrupt pointer is in the
  DirectDraw/WineD3D surface path; Wine 9.0 sets up a surface differently than
  Wine 11 and the game grabs a bad pointer. Recorded as `KU-076`.

## Container reproduction recipe (preserve; then teardown)

Reproducible from `ubuntu:24.04`:

```
podman run -d --name rr-abl --net=host \
  --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --security-opt label=disable \
  ubuntu:24.04 sleep infinity
# inside: dpkg --add-architecture i386; apt install wine wine32:i386 wine64 xvfb x11vnc \
#   cmake g++ g++-multilib pkg-config libcapnp-dev capnproto zlib1g-dev libzstd-dev libzstd-dev:i386 ninja-build python3
# build rr master: cmake -G Ninja -DBUILD_TESTS=OFF -DWILL_RUN_TESTS=OFF <src>; ninja
#   (full 32-bit build required to REPLAY the 32-bit tracee; needed for Zen-5 CPU support)
# game: WINEARCH=win32 prefix, LIBGL_ALWAYS_SOFTWARE=1, WINEESYNC=0 WINEFSYNC=0
```

Host prerequisite: `/dev/ntsync` absent (`sudo modprobe -r ntsync`); restore
with `sudo modprobe ntsync`. `perf_event_paranoid <= 1`.

## Conclusion and pivot

`rr` on Wine is a dead end for this game. The user's goal is **modding the PC
executable**, which is materially easier and less memory-constrained than PS1
(so PS1 is not a substitute — only a bounded cross-port reference). The missing
capability was deterministic reproducible replay for investigation and
regression, not a debugger per se.

**Settled architecture** (`DEC-20260817-145`):

- **Fedora + Wine** — primary: asset/exe analysis, mod development, fast
  iteration, the session-control/query tooling built earlier today.
- **libTAS + pinned single-threaded PCem + Win95** — the deterministic
  reference/replay harness on the real PC executable. Pin the TASVideos
  **PCem 17+st** release (regular PCem is not deterministic). Required ROMs per
  TASVideos: `ga686bx/6BX.F2a`, `voodoo3_3000/3k12sd.rom`, `awe32.raw`; set
  `confirm_on_stop_emulation=0`, `confirm_on_reset_machine=0` in `~/.pcem/pcem.cfg`.
  User must supply Win95 media/license.
- **86Box** — optional, only after PCem determinism is proven: test whether it
  stays deterministic while adding its better debugger; a bonus, never a
  dependency.

## Acceptance / first milestone (narrow)

Not "full TAS environment." The go/no-go is: boot the game under Win95/PCem-st,
reproduce the CONVPSXTPAGE8 level load (does it crash like Wine 9.0, or run like
Wine 11 — the discriminating test for `KU-076`), capture a **level-start
savestate**, record a short input movie, and demonstrate **repeated
synchronized playback from that savestate**.

Determinism verification is **progressive**, not a single whole-region hash:
1. replay the same movie repeatedly from the exact savestate;
2. check already-understood gameplay globals at fixed frames (position
   `0x0059D910`, level `0x00861C84`, collision, `NextLife`, RNG if located);
3. try hashing the full writable `.data` region `0x004C1000`–`0x00864000`;
4. if the full hash differs, diff and **classify** the changing ranges rather
   than declaring desync;
5. build a normalised, state-specific fingerprint excluding volatile/irrelevant
   fields.

This progressively teaches which bytes constitute meaningful deterministic game
state — evidence that feeds directly back into the RE work.

## Files inspected

Container (podman `rr-abl`), `rr` source, `Vault/10-Environment/*` (86Box),
`static/pe/BIN-97c95ba5572dce63/objdump.txt` and the Ghidra export for
`FUN_00462c30`, `Vault/40-Implementation/Reverse Engineering Capability Gaps.md`.

## Changes made

This session note; `DEC-20260817-145`; `KU-076` in [[Known Unknowns]]. No repo
code changed. Host `ntsync` is removed pending restore. The `rr-abl` container
and its image are to be torn down after this record.

## Unresolved questions

`KU-076` (CONVPSXTPAGE8 corrupt-pointer cause; and whether Win95/PCem avoids
it). Whether PCem-st replays *this* game deterministically (the first
milestone). Whether the game's software renderer or the Voodoo-3 path is the
better deterministic config under PCem-st.

## Recommended next action

Restore `ntsync`, tear down the `rr-abl` container/image, then scope PCem-st:
acquire the ROMs and Win95 media, install Win95 in PCem-st, install the game,
reach the CONVPSXTPAGE8 load, and run the first synchronized-replay go/no-go.

## Process audit

No game/Wine/Gamescope ran on the host in a way that persisted; all game
execution was inside the podman container. Host state changed: `ntsync`
removed (restore pending). No `originals/` access. The container holds a copy
of the game tree under its own overlay (not the repo).
