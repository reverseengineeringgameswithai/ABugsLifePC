---
type: experiment
id: EXP-20260812-028
date: 2026-08-12
question: Does the first controlled Training post-title transition read either exact plant 10 entry +0x2E word at candidate 0x0044CE3E?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, GDB harness, Gamescope
environment_version: wine-11.0-staging; gdb-17.1-6.fc44; gamescope-3.16.25-1.fc44
working_directory: /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS
configuration: One unchanged Training run; remotely selected Direct3D hardware 640x480x16; read-only hardware watches and breakpoints
artifacts:
  - dynamic/wine/RUN-GDB-20260812-203714/metadata.json
  - dynamic/wine/RUN-GDB-20260812-203714/bugs.log
  - dynamic/wine/RUN-GDB-20260812-203820/metadata.json
  - dynamic/wine/RUN-GDB-20260812-203930/metadata.json
  - dynamic/wine/RUN-GDB-20260812-204252/curation.txt
  - dynamic/wine/RUN-GDB-20260812-204333/curation.txt
  - static/exports/BIN-97c95ba5572dce63/M2-plant10-post-title-selected-entry-negative-trace.md
addresses:
  - 0x0040100A
  - 0x004012C6
  - 0x0044CA00
  - 0x0044CE0D
  - 0x0044CE3E
  - 0x0044CFC4
  - 0x0044D079
  - 0x0044D79A
  - 0x0044D7A4
  - 0x00463770
  - 0x005AAB2E
  - 0x005AAB7E
  - 0x005B1AA4
  - 0x006C342B
result: no-plant10-entry-2e-access-through-nextlife-plus-30-seconds
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
---

# EXP-20260812-028 - Plant10 post-title selected-entry negative

## Question

Does the first controlled Training post-title transition read either exact
plant 10 entry `+0x2E` word at static candidate `0x0044CE3E`?

## Inputs and authority

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Exact watched words `0x005AAB2E` and `0x005AAB7E`, measured as unsigned
  `1` in [[EXP-20260812-026 - Plant10 entry 2E bounded negative]].
- Static candidate reader `0x0044CE3E` from
  [[EXP-20260812-027 - Plant10 entry 28 bounded negative]].

No executable byte, general-purpose register, game-data memory value, or game
file was modified. No PS1 source or finding was consulted. Screenshots were
limited to the isolated 640x480 Gamescope game surface and remain ignored
under `work/copies/EXP-20260812-028/evidence/`; no screenshot, raw game bytes,
core, or trace is committed.

## Expected discriminator

- A watchpoint hit at `0x0044CE42`, immediately after the read instruction,
  would identify the exact entry and allow the source selector, branch, and
  first downstream call to be recorded.
- Zero stops through `NextLife` and a separate elapsed gameplay arm would be a
  bounded no-access result, not a lifetime absence claim.
- A hardware execution breakpoint on `0x0044CE3E` distinguishes an inactive
  candidate from a candidate that executes only for other resource entries.

## Procedure

1. Launch the unchanged copy through `scripts/play-pristine.sh --research`.
2. Target only the isolated Gamescope window. Send Down then Return at the
   renderer selector and accept the run only after the complete log proves
   `Screen mode 640x480x16 selected`, `Starting Direct3D renderer`, and no
   `INITSOFTRENDER`.
3. Select Training, wait for the natural `Training Level` / `press a key to
   start` title, and visually verify that game-only endpoint.
4. At that pause, run GDB harness arm `RUN-GDB-20260812-203714` with exact
   two-byte read watches on `0x005AAB2E/0x005AAB7E`, `NextLife` as the bounded
   milestone, and fixed read-only snapshots of the plant slot/header, both
   entries, and source-record table region. Send one Return to start.
5. After `NextLife`, run a second 30-second no-input watch arm,
   `RUN-GDB-20260812-203820`.
6. Run a separate ten-second hardware execution control at exact instruction
   `0x0044CE3E`, `RUN-GDB-20260812-203930`.
7. Explore the outer caller gate in two later arms. Preserve but reject those
   arms from the accepted result after raw GDB output records a `SIGSEGV` at
   the instrumented PC and Wine reports the matching unresolved fault; see
   [[#Exploratory instrumentation incident]].

## Observed

### Accepted title-to-NextLife arm

`RUN-GDB-20260812-203714` ran from
2026-08-12T20:37:14.169787-04:00 through
2026-08-12T20:37:25.688602-04:00. `NextLife` won with zero stops. Both
watchpoints were installed and deleted, cleanup was verified, and the harness
detached. The ignored post-milestone 640x480 capture at
2026-08-12T20:37:49.614212131-04:00 has SHA-256
`6295fbe13b8dea9ad7f0f5504b2297f54626ea56834ae6d8f0abce8b54d2e7f8`
and visually showed live early Training gameplay.

The committed log contains one hardware 640x480x16 selection, one Direct3D
renderer start, no `INITSOFTRENDER`, the plant10 `.ANM` and `.ALL` requests,
`---End InitMainGame---`, and `NextLife`; its SHA-256 is
`8b331970c547406864ce26d1afee9367683cf34b62b39bd379206fa6ffcfd500`.

### Accepted elapsed gameplay arm

`RUN-GDB-20260812-203820` retained the same two exact watches for
30.026628 seconds from 2026-08-12T20:38:20.552948-04:00 through
2026-08-12T20:38:50.579576-04:00. It timed out with zero stops, deleted both
watches, verified cleanup, and detached. No gameplay input was sent.

### Accepted candidate-reader control

`RUN-GDB-20260812-203930` retained a hardware execution breakpoint at exact
reader `0x0044CE3E` for 10.014330 seconds. It timed out with zero stops,
deleted the breakpoint, verified cleanup, and detached. Within this separate
no-input interval, the candidate reader itself did not execute; the result is
not evidence that it executed for a different resource.

### Static branch correlation

At `0x0044CE3E`, the candidate reads signed entry word `+0x2E`. The exact
following decrement/branch chain sends value `1` to `0x0044CFC4`, value `2`
to `0x0044CFAB`, and value `3` through `0x0044CE57`. For value `1`, the first
call in the selected branch is `0x0044D079 -> 0x004012C6 -> 0x00463770`.
Exact `0x00463770` copies three dwords from its second argument offsets
`+0x00/+0x04/+0x08` to its first argument offsets `+0x14/+0x18/+0x1C`.
These are static facts only; the accepted runtime arms never reached this
branch for plant 10, so no semantic name is assigned.

### Exploratory instrumentation incident

`RUN-GDB-20260812-204252` placed a hardware execution breakpoint at outer
gate `0x0044D79A` and recorded one stop before timeout. At that stop,
`AL == 0x40`, byte `0x005C5EDC == 0x40`, dword `0x005BA80C == 0x00000680`,
plant slot `0x005B1AA4 == 0x006C342B`, and the header remained
`1/3/66/68`. Static `test al,0x10` would leave the following `jne` untaken and
reach call site `0x0044D7A4`; this is a static interpretation of the captured
state, not proof that the call completed.

The ignored raw GDB output for that same run then records thread 1 receiving
`SIGSEGV` at `0x0044D79A`. The harness nevertheless continued to its timeout
and reported breakpoint deletion, clean detach, and no structured error. A
later paired entry/reader arm, `RUN-GDB-20260812-204333`, therefore began after
the unresolved signal and its zero-stop interval is rejected. During shutdown,
Wine also reported `Unhandled page fault on read access to FFFFFFFF at address
0044D79A` and began its debugger. The instruction at `0x0044D79A` is
`test al,0x10` and has no memory operand, so the observed fault cannot be
explained as an ordinary read performed by that instruction. Both arms are
retained for diagnosis but excluded from the accepted M2.15 negative and
cannot promote the caller, callee, or branch. No later live-game claim is made
from them.

## Confirmed

- No access trap overlapped either exact plant 10 entry `+0x2E` word from the
  natural title through `NextLife` in `RUN-GDB-20260812-203714`.
- Neither exact word produced an access stop during a separate 30.026628-
  second no-input post-`NextLife` arm.
- Exact candidate reader `0x0044CE3E` did not execute during a separate
  10.014330-second no-input early-gameplay arm.
- The accepted run used the exact unchanged executable and Training data,
  passed the hardware Direct3D gates, loaded the plant 10 pair, and reached
  `NextLife`.
- The exploratory caller-gate arms have an unresolved instrumentation fault
  and are not accepted as downstream runtime evidence.

## Inferred

The static selected-entry loop is event-specific or otherwise inactive during
the measured no-input early-gameplay intervals. A fresh session with the
caller gate, callee entry, and exact data watches armed simultaneously is a
narrower discriminator than extending another wall-clock idle window.

## Unknown and limitations

- Whether a Training source record ever supplies selector 10 to
  `0x0044CA00` remains unknown.
- The event that activates the outer caller path and selected-entry loop is
  unknown.
- Field `+0x2E`, function `0x0044CA00`, and branches 1/2/3 have no promoted
  semantic names.
- Later input-driven gameplay, copied/derived state, non-CPU use, and any M1
  placement/resource identity remain outside the accepted windows.
- Whether the exploratory Wine fault is caused by the harness, native GDB,
  Wine WoW64 exception handling, or another condition remains unknown.

## Contradictions and negative results

The predicted plant 10 candidate did not read either exact word across the
controlled transition or early idle window. The later outer-gate stop does not
resolve that negative because its continuation lacks an accepted survival
receipt and ended in a contradictory Wine fault report.

## Result

M2.15 is complete with a precise no-access window from the natural title
through `NextLife`, an additional 30.026628-second no-input gameplay window,
and a separate 10.014330-second candidate-reader execution negative. No
consumer or semantic field is promoted.

## Follow-up

In a fresh unchanged hardware-gated run, arm the outer gate `0x0044D79A`,
callee entry `0x0044CA00`, and both exact plant 10 `+0x2E` watches
simultaneously before advancing the title. Require a post-detach live-game
survival receipt. If the gate and entry chain completes, bind its source
selector and selected range; if the instrumentation fault reproduces, stop
the consumer trace and fix CAP-001 before further claims.
