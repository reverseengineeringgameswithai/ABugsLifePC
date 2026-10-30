---
type: experiment
id: EXP-20260812-027
date: 2026-08-12
question: Which PC function first reads either exact Training plant 10 entry +0x28 word before the retained title boundary?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, native GDB, Gamescope
environment_version: wine-11.0-staging; gdb-17.1-6.fc44; gamescope-3.16.25-1.fc44
working_directory: /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS
configuration: One unchanged Training run; remotely selected Direct3D hardware 640x480x16; native hardware breakpoints and read watchpoints
artifacts:
  - dynamic/wine/RUN-GDB-20260812-201419/debugger-evidence.txt
  - dynamic/wine/RUN-GDB-20260812-201419/bugs.log
  - dynamic/wine/RUN-GDB-20260812-201419/metadata.json
  - static/exports/BIN-97c95ba5572dce63/M2-plant10-entry-28-negative-trace.md
addresses:
  - 0x0044596D
  - 0x00445B01
  - 0x00448107
  - 0x0044810B
  - 0x0044CE3E
  - 0x004679C7
  - 0x005AAB28
  - 0x005AAB78
result: plant10-both-entry-28-no-read-through-no-input-title
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
---

# EXP-20260812-027 - Plant10 entry 28 bounded negative

## Question

Which PC function first reads either exact Training plant 10 entry `+0x28`
word before the retained resource-batch-return/title boundary?

## Inputs

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Unique plant 10 post-call `0x0044596D`, immediately following common tail
  `0x00445B01`, batch return `0x004679C7`, and exact two-entry range from
  [[EXP-20260812-026 - Plant10 entry 2E bounded negative]].
- Exact watched words `0x005AAB28` and `0x005AAB78`.

No executable byte, general-purpose register, game-data memory value, or
game-data file was modified. No PS1 source or finding was consulted. Raw GDB
text and game-only captures remain ignored under
`work/copies/EXP-20260812-027/evidence/`; no raw transcript, capture, or game
bytes are committed.

## Expected discriminator

- A read-watchpoint stop after the guarded start supplies the first exact
  entry reader PC and immediate use.
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
   `66/68`, and both exact `+0x28` values. Accept only the immediately
   following common-tail `0x00445B01`.
5. Arm read watchpoints on `0x005AAB28` and `0x005AAB78`, plus hardware
   execution breakpoint `0x004679C7`.
6. At return, inspect hit state and values, delete only the return breakpoint,
   and retain both watches without further input through a title capture.
7. Interrupt only to inspect the retained title endpoint; delete all watches,
   confirm none remain, and detach.

The proven scripted launcher, Gamescope capture path, and GDB harness safety
conventions were used. Native GDB drove this packet because the accepted
window requires watches to be staged only after a guard and its immediately
following shared-tail stop in one attachment; the current harness does not
express that dynamic two-stage arm.

## Observed

### Reproduced plant 10 identity and values

At unique post-call `0x0044596D`, the retained stack includes resource ID
`0x71`; slot `0x005B1AA4 == 0x006C342B`; ANM header words are
`1/3/66/68`. Exact words first-entry `0x005AAB28` and second-entry
`0x005AAB78` both equal unsigned zero.

Both values remain zero at the accepted `0x00445B01` stop. Exact instructions
`0x004480B4–0x004480BD` derive entry `+0x20`, and
`0x00448107–0x0044810B` copy a descriptor word to runtime entry `+0x28`.

### Resource-batch-return boundary

In `RUN-GDB-20260812-201419`, `0x004679C7` wins with one hit. Both read
watchpoints remain listed without hit counts, and both watched words remain
zero. Only the return breakpoint is deleted.

### No-input title boundary

No input was sent after the Return used to select Training. Neither
watchpoint stopped execution while the game reached the `Training Level` /
`press a key to start` title. The ignored game-only capture at
2026-08-12T20:18:46.810212628-04:00 has SHA-256
`524654827cd39b09ac7bd55640580cfdb9c262efc45f0da54aaaae669da500b4`.

At final inspection, both watches remain enabled without hit counts and both
words remain zero. Every hardware point is deleted before detach.

### Runtime gates

The complete log contains one `Screen mode 640x480x16 selected`, one
`Starting Direct3D renderer`, no `INITSOFTRENDER`, and one request each for
plant10.anm and plant10.all. The run intentionally ends at the retained title;
`End InitMainGame` and `NextLife` are not claimed.

### Static next-event correlation

M2.9–M2.14 now cover every exact entry field populated by `0x00448010` and
its guarded caller with at least one explicit bounded watch window. This is
not a lifetime absence result.

Static instructions `0x0044CE0D–0x0044CE3E` in address-based function
`0x0044CA00` select a per-resource ANM pointer, derive its start/end indices,
and read selected entry `+0x2E`. The loop advances entries by `0x50` through
`0x0044D1ED`. Plant 10 slot arithmetic and measured header `66/68` make this
an exact post-title candidate, but this run does not prove that a Training
source record supplies selector 10 to it.

## Confirmed

- Both exact plant 10 entry `+0x28` words equal unsigned zero at the guarded
  start, resource-batch return, and retained title endpoint.
- No CPU data read overlaps first-entry `0x005AAB28–0x005AAB29` or second-
  entry `0x005AAB78–0x005AAB79` from guarded final population through batch
  return `0x004679C7`.
- Both ranges remain unread and unchanged while execution reaches the
  unattended Training title.
- Every exact field currently tied by static stores to the plant 10 entries in
  `0x00448010` and its guarded caller has now received a bounded read-watchpoint
  window across M2.9–M2.14.
- The unchanged accepted run passes the exact Direct3D and plant-request
  gates.

## Inferred

An event-specific post-title trace of `0x0044CE3E` is narrower and more
discriminating than widening to entry fields without a static producer or
consumer.

## Unknown and limitations

- The meanings of `+0x28`, `+0x2E`, and the 0x50-byte entry remain unknown.
- Zero values are not classified as padding or unused.
- Later gameplay, copied/derived state, non-CPU consumption, and later events
  are outside this packet.
- No plant 10 entry is connected to an M1 placement or visible outcome.
- Whether `0x0044CA00` receives resource index 10 after the title is untested.

## Contradictions and negative results

The exact statically populated `+0x28` surface did not expose a CPU reader in
the retained window. This closes the planned field-by-field initialization
widening without promoting a field meaning or lifetime-absence claim.

## Result

M2.14 is complete with exact negative windows for both entry `+0x28` words
from guarded final population through resource-batch return and the retained
no-input title.

## Follow-up

At the natural Training title, arm only the exact plant 10 `+0x2E` words and
trace the first controlled post-title transition. Test whether the first read
is `0x0044CE3E`, and record the supplying source-record selector word at
`[edi-0x08]`, ANM slot/header, entry address, branch value, and first called
consumer. Do not assign semantics, mutate memory, consult PS1, or widen to an
unbounded entry sweep.
