---
type: experiment
id: EXP-20260812-029
date: 2026-08-12
question: Does a fresh simultaneous outer-gate, callee-entry, and two-data-watch arm complete without the M2.15 debugger fault?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, GDB harness, windowed muted Gamescope
environment_version: wine-11.0-staging; gdb-17.1-6.fc44; gamescope-3.16.25-1.fc44
working_directory: /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS
configuration: Fresh unchanged Training run; Direct3D hardware 640x480x16; 1280x960 window; private null audio sink; four simultaneous read-only hardware points
artifacts:
  - dynamic/wine/RUN-GDB-20260812-211649/metadata.json
  - dynamic/wine/RUN-GDB-20260812-211649/result.json
  - dynamic/wine/RUN-GDB-20260812-211649/stops.jsonl
  - dynamic/wine/RUN-GDB-20260812-211649/debugger-evidence.txt
  - dynamic/wine/RUN-GDB-20260812-211649/curation.txt
  - dynamic/wine/RUN-GDB-20260812-211649/bugs.log
  - static/exports/BIN-97c95ba5572dce63/M2-fresh-selected-entry-chain-debugger-fault.md
addresses:
  - 0x0040100A
  - 0x0044CA00
  - 0x0044D79A
  - 0x0044D7A4
  - 0x0059D9C0
  - 0x005AAB2E
  - 0x005AAB7E
  - 0x005B1AA4
  - 0x005BA80C
  - 0x005C5EDC
  - 0x006C342B
result: fresh-simultaneous-arm-reproduces-debugger-sigsegv-no-caller-chain
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
  - implementation/tooling
---

# EXP-20260812-029 - Fresh selected-entry chain debugger fault

## Question

Does one fresh unchanged Training process, with the outer gate, callee entry,
and two exact plant 10 data watches armed simultaneously before title advance,
produce an ordered caller chain and survive normally without reproducing the
M2.15 instrumentation fault?

## Inputs and authority

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Outer gate/callee static chain
  `0x0044D79A -> 0x0044D7A4 -> 0x0040100A -> 0x0044CA00`.
- Exact plant 10 candidate words `0x005AAB2E/0x005AAB7E` from the measured
  `0x005B1AA4 -> 0x006C342B`, `66/68` range.

No executable byte, register, game memory, or game file was modified. No PS1
source or finding was consulted. All screenshots targeted only the isolated
Gamescope game surface, never the desktop or whole screen, and remain ignored
under `work/copies/EXP-20260812-029/evidence/`. Raw GDB stdout/stderr remain
ignored beside them; only structured bounded evidence and hashes are committed.

## Expected discriminator

- A normal gate -> `0x0044CA00` -> exact word access sequence plus a live
  post-detach game endpoint would establish the runtime chain at that boundary.
- A bounded absence of one link would narrow the chain only if the game
  survived normally.
- Recurrence of the same-address fault or a failed survival receipt would
  reject all post-gate consumer inference and make CAP-001 the active blocker.

## Procedure

1. Validate and launch `scripts/play-pristine.sh --research --windowed --mute`.
   The windowed default was 1280x960. `--mute` created a private per-run
   PipeWire null sink while retaining the game's audio subsystem.
2. Target only the isolated Gamescope window. Send Down and Return as separate
   inputs, accepting the arm only after the complete log proves
   `Screen mode 640x480x16 selected`, `Starting Direct3D renderer`, and no
   `INITSOFTRENDER`.
3. Select unchanged Training and wait for its natural title.
4. Attach read-only harness arm `RUN-GDB-20260812-211649` before advancing the
   title. Install execution breakpoints `0x0044D79A/0x0044CA00` and two-byte
   read watches `0x005AAB2E/0x005AAB7E`, consuming all four hardware slots.
   Record bounded registers, caller globals, plant slot/header/entries, and
   four fixed source-table address blocks on each stop.
5. Send one Return. Reconcile structured completion, raw debugger signals,
   the appended game log, process survival, and a game-only post-detach frame.
6. Stop only the resolved run PIDs and verify the private sink unloads.

A preliminary launcher check sent Down and Return without enough separation
and entered `INITSOFTRENDER`; it was immediately rejected and stopped. It is
not part of this experiment's runtime conclusion. The accepted fresh arm used
separate renderer inputs and passed all three exact renderer log gates.

## Observed

### Launch and endpoint gates

The accepted log records hardware mode at line 76, Direct3D initialization at
line 127, plant10 `.ANM`/`.ALL` requests at lines 1470/1471,
`---End InitMainGame---` at line 1476, and `NextLife` at line 1478. It contains
no `INITSOFTRENDER`; committed SHA-256 is
`e23f290155552d729a290214459b23386a58c55d5c0074c26442c262e25dc0b4`.

The game's live PipeWire sink input was routed to private sink
`ablpc_mute_2549983` during the run. That proves the requested launcher route,
not the complete semantics of game audio. The sink unloaded during cleanup.

### Structured stop

`RUN-GDB-20260812-211649` spans
2026-08-12T21:16:49.509467-04:00 through
2026-08-12T21:17:05.935709-04:00. It records exactly one breakpoint stop at
`0x0044D79A` at 21:17:05.903919:

- `RAX/AL == 0x40`, `RCX == 0x680`, `RDI == 0`, `RIP == 0x0044D79A`;
- `[0x005C5EDC] == 0x40` and `[0x005BA80C] == 0x00000680`;
- `[0x005B1AA4] == 0x006C342B` with header words `1/3/66/68`;
- both exact 80-byte entries retain the values recorded in `stops.jsonl`;
- four configured fixed blocks `[0x0059D9C0,0x0059DD88)` are zero.

The last observation is only a bounded read of the configured static range;
it does not establish that no live source records exist elsewhere. Static
`0x40 & 0x10 == 0` would leave the following `jne` untaken and expose the call
at `0x0044D7A4`. This is static interpretation of the captured gate state, not
proof that the call executed or completed.

### Fatal-signal contradiction and failed survival

The structured result reports `target_reached`, one stop, all four points
deleted, cleanup verified, and detach. Raw GDB stdout from the same run instead
records `SIGSEGV` at `0x0044D79A` immediately after the breakpoint stop. The
harness code path at `scripts/gdb-harness.py:257-272` treats an unclassified
non-`SIGINT` signal as a signal to continue, so schema 1 does not expose that
fatal stop in its result.

Wine then reported `Unhandled page fault on read access to FFFFFFFF at address
0044D79A` and opened winedbg. The game-only post-detach capture at
2026-08-12T21:17:40.750698754-04:00, SHA-256
`d528b1c97d8820b6e62a36a4e327602276c1244bd8a4b72e6b16618da7105a3b`,
showed Wine's fatal-error dialog rather than live gameplay. Therefore the
appended `NextLife` log milestone is not a survival receipt.

No structured stop exists at `0x0044CA00` or either exact watch. Those zero
counts occur after a failed continuation and are not accepted negatives.

## Confirmed

- A fresh process with all four caller/callee/data hardware points armed
  simultaneously reproduced `SIGSEGV` at the instrumented outer gate.
- The gate's one pre-continuation register/memory snapshot is retained exactly.
- The structured `target_reached`/cleanup/detach result is a false survival
  signal for this arm; raw debugger output and a Wine crash dialog independently
  disprove normal survival.
- The accepted launch used unchanged PC inputs, hardware Direct3D, a 1280x960
  game-only window, and private-sink audio routing.
- No runtime-completed call to `0x0044CA00` and no plant 10 data access or
  no-access result is established by this arm.

## Inferred

Native GDB/Wine continuation at this exact instrumented location is unsafe
under the current harness behavior. The harness's broad signal-continue branch
explains why `SIGSEGV` is omitted from structured completion; it does not by
itself explain the initial same-address fault.

## Unknown and limitations

- Whether the initial fault originates in the harness, native GDB, Wine WoW64
  debug continuation, or another condition remains unknown.
- Normal uninstrumented execution of the call edge is static, not measured by
  this rejected arm.
- The activating source event/selector, plant 10 field semantics, selected
  branches, and M1 dependency remain unknown.
- Fixed zero source-table snapshots do not locate the live source-record pool.

## Contradictions and negative results

`target_reached`, hardware-point cleanup, detach, and `NextLife` appear in
structured/log artifacts, while raw GDB and a game-only frame show a fatal
exception and winedbg. The latter are direct survival evidence, so the arm is
rejected as a caller-chain or bounded no-access result.

## Result

M2.16 is complete under its fault-reproduction done condition. The fresh
simultaneous arm reproduces KU-031 and makes CAP-001 a blocker before further
selected-entry interpretation. No function or field receives a semantic name.

## Follow-up

Execute [[Project Roadmap#M2.17 — Unexpected-signal-safe debugger control]].
First add a synthetic fatal-signal fixture and make the harness surface an
unexpected fatal signal as a structured terminal result without blindly
continuing it. Add a configurable, independent post-detach survival receipt.
Revalidate on a previously safe known watchpoint before returning to
`0x0044D79A`; do not use another live caller-chain arm until that behavior is
proven.
