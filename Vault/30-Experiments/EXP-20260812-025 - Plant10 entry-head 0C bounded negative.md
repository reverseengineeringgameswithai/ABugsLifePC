---
type: experiment
id: EXP-20260812-025
date: 2026-08-12
question: Are either Training plant 10 entry's exact nonzero +0x0C dwords read after guarded final population, before resource-batch return, or while reaching a no-input title capture?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, native GDB, Gamescope
environment_version: wine-11.0-staging; gdb-17.1-6.fc44; gamescope-3.16.25-1.fc44
working_directory: /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS
configuration: One unchanged Training run; Direct3D hardware 640x480x16; native hardware breakpoints and read watchpoints
artifacts:
  - dynamic/wine/RUN-GDB-20260812-165837/debugger-evidence.txt
  - dynamic/wine/RUN-GDB-20260812-165837/bugs.log
  - dynamic/wine/RUN-GDB-20260812-165837/metadata.json
  - static/exports/BIN-97c95ba5572dce63/M2-plant10-entry-head-0c-negative-trace.md
addresses:
  - 0x0044596D
  - 0x00445B01
  - 0x00446970
  - 0x00446A97
  - 0x00447668
  - 0x004480F1
  - 0x004679C7
  - 0x005AAB0C
  - 0x005AAB5C
result: plant10-both-entry-head-0c-no-read-through-no-input-title
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
---

# EXP-20260812-025 - Plant10 entry-head 0C bounded negative

## Question

Which PC function first reads either exact nonzero Training plant 10 entry
`+0x0C` dword, and what source/destination boundary does that access
establish?

## Inputs

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Unique plant 10 post-call `0x0044596D`, immediately following common tail
  `0x00445B01`, batch return `0x004679C7`, and exact two-entry range from
  [[EXP-20260812-024 - Plant10 entry-head bounded negatives]].
- Exact watched dwords `0x005AAB0C` and `0x005AAB5C`.

No executable byte, general-purpose register, game-data memory value, or
game-data file was modified. No PS1 source or finding was consulted. Raw GDB
text and captures remain ignored
under `work/copies/EXP-20260812-025/evidence/`; no raw transcript, capture, or
game bytes are committed.

## Expected discriminator

- A read-watchpoint stop after the guarded start supplies the first exact
  entry reader PC and a source/destination path.
- If `0x004679C7` wins and both watches remain untouched through a no-input
  title capture, the run excludes CPU reads only for the two exact ranges and
  bounded interval.

## Procedure

1. Launch one unchanged Training run through
   `scripts/play-pristine.sh --research`; require the 640×480×16 Direct3D log
   markers and reject `INITSOFTRENDER`.
2. Attach native GDB at the Training selector, suppress only expected Wine
   worker `SIGUSR1`/`SIGUSR2` stops, and arm unique guard `0x0044596D`.
3. Reproduce resource ID `0x71`, live ANM pointer `0x006C342B`, indices
   `66/68`, and both four-dword entry heads. Accept only the immediately
   following common-tail `0x00445B01`.
4. Arm read watchpoints on `0x005AAB0C` and `0x005AAB5C`, plus hardware
   execution breakpoint `0x004679C7`.
5. At return, inspect hit state and values, delete only the return breakpoint,
   and retain both watches without further input through a title capture.
6. Interrupt only to inspect the retained title endpoint; delete all watches,
   confirm none remain, and detach.

## Observed

### Reproduced plant 10 identity and values

At unique post-call `0x0044596D`, the retained stack includes resource ID
`0x71`; slot `0x005B1AA4 == 0x006C342B`; ANM header words are
`1/3/66/68`. Both entry heads are:

```text
entry 66 at 0x005AAB00: 0x00000000 0x00000000 0x00000000 0x00000001
entry 67 at 0x005AAB50: 0x00000000 0x00000000 0x00000000 0x00000001
```

The heads remain identical at the accepted `0x00445B01` stop. Exact
instructions `0x004480EE–0x004480F1` independently map descriptor `+0x0C` to
runtime entry `+0x0C`.

### Resource-batch-return boundary

In `RUN-GDB-20260812-165837`, `0x004679C7` wins with one hit. Both read
watchpoints remain listed without hit counts, and both watched values remain
`0x00000001`. Only the return breakpoint is deleted.

### No-input title boundary

No input was sent after the Return used to select Training. Neither watchpoint
stopped execution while the game reached the Training title. The ignored
title capture at `2026-08-12T17:00:57.008841846-04:00` has SHA-256
`1d14ff734dd17201c3315391e9f3b3c4ca79ebddbbd6444840cfc57af2389ce1`.

At final inspection, both watches remain enabled without hit counts and both
dwords remain `0x00000001`. Every hardware point is deleted before detach.

### Static candidate correlation

Both exact indexed candidate reads are in address-based function
`0x00446970`. At `0x00446A8A`, selected entry word `+0x2E` must equal 9
before `0x00446A97` loads dword `+0x0C` into `ecx`; the following instructions
read a signed word through that pointer and retain pointer-derived locals. At
`0x00447661`, selected entry word `+0x2E` must equal `0xA` before
`0x00447668` loads `+0x0C`, advances it by four, and retains that value in a
local.

Neither candidate nor any other CPU instruction reads the two exact plant 10
dwords in the retained runtime interval. Their static source/destination
behavior is confirmed only for whatever entries satisfy their selection and
gate conditions, not for plant 10.

### Runtime gates

The log contains one `Screen mode 640x480x16 selected`, one
`Starting Direct3D renderer`, no `INITSOFTRENDER`, and both plant 10 requests.
The run intentionally ends at the retained title; `End InitMainGame` and
`NextLife` are not claimed.

## Confirmed

- Both exact plant 10 entry `+0x0C` dwords equal `0x00000001` at the guarded
  start, resource-batch return, and retained title endpoint.
- No CPU data read overlaps first-entry `0x005AAB0C–0x005AAB0F` or second-
  entry `0x005AAB5C–0x005AAB5F` from the guarded final population through
  batch return `0x004679C7`.
- Both ranges remain unread and unchanged while execution reaches the
  unattended Training title.
- The unchanged run passes the exact Direct3D and plant-request gates.

## Inferred

The exact `+0x2E` words are the narrowest next discriminator because both
static `+0x0C` candidates read and compare that field before accessing
`+0x0C`.

## Unknown and limitations

- The meanings of `+0x0C` and `+0x2E` remain unknown.
- Later gameplay, later entry fields, non-CPU consumption, and later events
  are outside this packet.
- No plant 10 entry is connected to an M1 placement or visible outcome.
- The static candidate branches may select other entries during this window;
  the exact watched addresses prove only that they do not select either plant
  10 entry far enough to read its `+0x0C` dword.

## Contradictions and negative results

Neither statically identified `+0x0C` candidate reads the exact plant 10
dwords in the bounded run. Static field references therefore remain
candidates and are not promoted into an exact plant 10 consumer claim.

## Result

M2.12 is complete with exact negative windows for both nonzero entry-head
`+0x0C` dwords from guarded final population through resource-batch return and
the retained no-input title.

## Follow-up

Watch only the two exact plant 10 entry `+0x2E` words at `0x005AAB2E` and
`0x005AAB7E` from the same guarded boundary. Correlate any first hit with the
gates at `0x00446A8A` and `0x00447661`. Do not assign state semantics, mutate
memory, parse/edit `.ALL`, or consult PS1.
