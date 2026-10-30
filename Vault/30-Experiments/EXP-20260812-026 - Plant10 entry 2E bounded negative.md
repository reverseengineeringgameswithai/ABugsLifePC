---
type: experiment
id: EXP-20260812-026
date: 2026-08-12
question: Which PC function first reads either exact Training plant 10 entry +0x2E word, and do the 0x00446970 gates select either entry before the retained title boundary?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, native GDB, Gamescope
environment_version: wine-11.0-staging; gdb-17.1-6.fc44; gamescope-3.16.25-1.fc44
working_directory: /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS
configuration: One unchanged Training run; remotely selected Direct3D hardware 640x480x16; native hardware breakpoints and read watchpoints
artifacts:
  - dynamic/wine/RUN-GDB-20260812-195759/debugger-evidence.txt
  - dynamic/wine/RUN-GDB-20260812-195759/bugs.log
  - dynamic/wine/RUN-GDB-20260812-195759/metadata.json
  - static/exports/BIN-97c95ba5572dce63/M2-plant10-entry-2e-negative-trace.md
addresses:
  - 0x0044596D
  - 0x00445B01
  - 0x00446970
  - 0x00446A8A
  - 0x00447661
  - 0x00448117
  - 0x004679C7
  - 0x005AAB2E
  - 0x005AAB7E
result: plant10-both-entry-2e-no-read-through-no-input-title
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
---

# EXP-20260812-026 - Plant10 entry 2E bounded negative

## Question

Which PC function first reads either exact Training plant 10 entry `+0x2E`
word, and do the gates in `0x00446970` select either exact entry before the
retained boundary?

## Inputs

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Unique plant 10 post-call `0x0044596D`, immediately following common tail
  `0x00445B01`, batch return `0x004679C7`, and exact two-entry range from
  [[EXP-20260812-025 - Plant10 entry-head 0C bounded negative]].
- Exact watched words `0x005AAB2E` and `0x005AAB7E`.

No executable byte, general-purpose register, game-data memory value, or
game-data file was modified. No PS1 source or finding was consulted. Raw GDB
text and captures remain ignored under
`work/copies/EXP-20260812-026/evidence/`; no raw transcript, capture, or game
bytes are committed.

## Expected discriminator

- A read-watchpoint stop after the guarded start supplies the first exact
  entry reader PC and the immediate comparison or transition.
- If `0x004679C7` wins and both watches remain untouched through a no-input
  title capture, the run excludes CPU reads only for the two exact ranges and
  bounded interval.

## Procedure

1. Launch one unchanged Training run through
   `scripts/play-pristine.sh --research`.
2. Remotely send Down then Return at the opening selector; require the complete
   run log to contain the 640x480x16 and Direct3D markers and no
   `INITSOFTRENDER`.
3. Attach native GDB at the Training selector, suppress only expected Wine
   worker `SIGUSR1`/`SIGUSR2` stops, and arm unique guard `0x0044596D`.
4. Reproduce resource ID `0x71`, live ANM pointer `0x006C342B`, indices
   `66/68`, and both exact `+0x2E` values. Accept only the immediately
   following common-tail `0x00445B01`.
5. Arm read watchpoints on `0x005AAB2E` and `0x005AAB7E`, plus hardware
   execution breakpoint `0x004679C7`.
6. At return, inspect hit state and values, delete only the return breakpoint,
   and retain both watches without further input through a title capture.
7. Interrupt only to inspect the retained title endpoint; delete all watches,
   confirm none remain, and detach.

## Renderer-preflight correction

One candidate arm was rejected because the required Down input had not been
sent and the user observed that the opening selector remained on software.
Every breakpoint was deleted, GDB detached, and the candidate process was
stopped. No result from that run is promoted.

The accepted run started fresh. Remote input sent Down then Return before the
Training selector. Its complete log contains exactly one
`Screen mode 640x480x16 selected`, exactly one
`Starting Direct3D renderer`, no `INITSOFTRENDER`, and both plant 10 request
lines. This preserves the gate in
[[Decision Log#DEC-20260812-009 - Hardware renderer evidence gate]].

## Observed

### Reproduced plant 10 identity and values

At unique post-call `0x0044596D`, the retained stack includes resource ID
`0x71`; slot `0x005B1AA4 == 0x006C342B`; ANM header words are
`1/3/66/68`. Exact words first-entry `0x005AAB2E` and second-entry
`0x005AAB7E` both equal unsigned `1`.

Both values remain `1` at the accepted `0x00445B01` stop. Exact instructions
`0x004480B4–0x0044813C` independently map selected runtime entry `+0x2E` to
population store `0x00448117` plus its conditional replacement/increment.

### Resource-batch-return boundary

In `RUN-GDB-20260812-195759`, `0x004679C7` wins with one hit. Both read
watchpoints remain listed without hit counts, and both watched words remain
`1`. Only the return breakpoint is deleted.

### No-input title boundary

No input was sent after the Return used to select Training. Neither
watchpoint stopped execution while the game reached the Training title. The
ignored title capture at `2026-08-12T19:59:55.729298233-04:00` has SHA-256
`bffa032d477a337bb2c4a52876b244124a94e4d2901285052efdfdd006c471a0`.

At final inspection, both watches remain enabled without hit counts and both
words remain `1`. Every hardware point is deleted before detach.

### Static candidate correlation

Both exact indexed candidate reads are in address-based function
`0x00446970`. `0x00446A8A` compares selected entry `+0x2E` to 9 before its
candidate `+0x0C` access; `0x00447661` compares the same relative word to
`0xA` before its own candidate access.

Neither comparison nor any other CPU instruction reads the two exact plant 10
words in the retained runtime interval. This proves only that the two exact
entries do not reach those comparisons in the measured window; the branches
may select other entries or run later.

### Runtime gates

The log contains one `Screen mode 640x480x16 selected`, one
`Starting Direct3D renderer`, no `INITSOFTRENDER`, and both plant 10 requests.
The run intentionally ends at the retained title; `End InitMainGame` and
`NextLife` are not claimed.

## Confirmed

- Both exact plant 10 entry `+0x2E` words equal unsigned `1` at the guarded
  start, resource-batch return, and retained title endpoint.
- No CPU data read overlaps first-entry `0x005AAB2E–0x005AAB2F` or second-
  entry `0x005AAB7E–0x005AAB7F` from guarded final population through batch
  return `0x004679C7`.
- Both ranges remain unread and unchanged while execution reaches the
  unattended Training title.
- Neither exact plant 10 entry reaches the `0x00446A8A` or `0x00447661`
  comparisons in that window.
- The unchanged accepted run passes the exact Direct3D and plant-request
  gates.

## Inferred

The exact `+0x28` words are the narrowest next statically populated entry
surface not already bounded by M2.9–M2.13.

## Unknown and limitations

- The meanings of `+0x2E` and `+0x28` remain unknown.
- Later gameplay, later entry fields, non-CPU consumption, and later events
  are outside this packet.
- No plant 10 entry is connected to an M1 placement or visible outcome.
- The static candidate branches may select other entries during this window.

## Contradictions and negative results

The statically identified `+0x2E` comparisons did not become exact plant 10
hits in the bounded runtime window. They remain confirmed entry-relative
accesses but are not promoted into exact plant 10 consumers.

The first candidate run also demonstrated why intended remote input and early
driver-enumeration lines are insufficient: the accepted run required an
explicit Down action and the complete no-`INITSOFTRENDER` log gate.

## Result

M2.13 is complete with exact negative windows for both entry `+0x2E` words
from guarded final population through resource-batch return and the retained
no-input title.

## Follow-up

Watch only the two exact plant 10 entry `+0x28` words at `0x005AAB28` and
`0x005AAB78` from the same guarded boundary. Correlate any first hit with exact
static instructions. Do not assign state semantics, mutate memory, parse/edit
`.ALL`, or consult PS1.
