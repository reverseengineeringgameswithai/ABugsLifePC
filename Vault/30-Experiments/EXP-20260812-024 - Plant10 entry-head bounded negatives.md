---
type: experiment
id: EXP-20260812-024
date: 2026-08-12
question: Are either Training plant 10 entry's exact +0x00/+0x04/+0x08 dwords read after guarded final population, before resource-batch return, or while crossing the title into gameplay?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, native GDB, Gamescope
environment_version: wine-11.0-staging; gdb-17.1-6.fc44; gamescope-3.16.25-1.fc44
working_directory: /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS
configuration: Two unchanged matched Training runs; Direct3D hardware 640x480x16; native hardware breakpoints and read watchpoints
artifacts:
  - dynamic/wine/RUN-GDB-20260812-163111/debugger-evidence.txt
  - dynamic/wine/RUN-GDB-20260812-163111/bugs.log
  - dynamic/wine/RUN-GDB-20260812-163111/metadata.json
  - dynamic/wine/RUN-GDB-20260812-163840/debugger-evidence.txt
  - dynamic/wine/RUN-GDB-20260812-163840/bugs.log
  - dynamic/wine/RUN-GDB-20260812-163840/metadata.json
  - static/exports/BIN-97c95ba5572dce63/M2-plant10-entry-head-negative-trace.md
addresses:
  - 0x0044596D
  - 0x00445B01
  - 0x004480DF
  - 0x004480E5
  - 0x004480EB
  - 0x004480F1
  - 0x004679C7
  - 0x005AAB00
  - 0x005AAB04
  - 0x005AAB08
  - 0x005AAB50
  - 0x005AAB54
  - 0x005AAB58
result: plant10-both-entry-head-first-three-dwords-bounded-negative
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
---

# EXP-20260812-024 - Plant10 entry-head bounded negatives

## Question

Which PC function first reads the exact entry-head dwords copied for either
Training plant 10 entry, and what source/destination boundary does that access
establish?

## Inputs

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Unique plant 10 post-call `0x0044596D`, common resource-loop tail
  `0x00445B01`, batch return `0x004679C7`, and exact two-entry range from
  [[EXP-20260812-023 - Plant10 late-initialization pointer-surface negative]].
- Exact first-entry dwords `0x005AAB00/04/08` and second-entry dwords
  `0x005AAB50/54/58`.

No executable, register, memory value, or game file was modified. No PS1
source or finding was consulted. Raw GDB text and captures remain ignored
under `work/copies/EXP-20260812-024/evidence/`; no raw transcript, capture, or
game bytes are committed.

## Expected discriminator

- A read-watchpoint stop after the guarded start supplies the first exact
  entry/offset reader PC and a concrete source/destination path.
- If `0x004679C7` wins and the watches remain untouched through the title,
  each run excludes CPU reads only for its three exact ranges and bounded
  interval.

## Procedure

1. Launch two unchanged Training runs through
   `scripts/play-pristine.sh --research`; require the 640×480×16 Direct3D log
   markers and reject `INITSOFTRENDER`.
2. Attach native GDB at the Training selector, suppress only expected Wine
   worker `SIGUSR1`/`SIGUSR2` stops, and arm unique guard `0x0044596D`.
3. Reproduce resource ID `0x71`, live ANM pointer `0x006C342B`, indices
   `66/68`, and both four-dword entry heads. Accept only the immediately
   following common-tail `0x00445B01`.
4. In `RUN-GDB-20260812-163111`, watch first-entry
   `0x005AAB00/04/08`; in `RUN-GDB-20260812-163840`, watch second-entry
   `0x005AAB50/54/58`. Use the fourth hardware slot at `0x004679C7`.
5. At return, inspect watchpoint hit state and values, delete only the return
   breakpoint, and retain the three watches across the title transition.
6. At the post-title gameplay endpoint, inspect and delete all watches,
   confirm none remain, detach, and preserve the hardware/plant/`NextLife`
   log gates.

## Observed

### Reproduced entry heads

Both guarded runs reproduce identical values before and after the common tail:

```text
entry 66 at 0x005AAB00: 0x00000000 0x00000000 0x00000000 0x00000001
entry 67 at 0x005AAB50: 0x00000000 0x00000000 0x00000000 0x00000001
```

Static instructions `0x004480D2–0x004480F1` independently map these to exact
entry offsets `+0x00/+0x04/+0x08/+0x0C`. The first three zero dwords are
observed values, not inferred padding.

### First-entry arm

In `RUN-GDB-20260812-163111`, watches on `0x005AAB00`, `0x005AAB04`, and
`0x005AAB08` began at the guarded `0x00445B01`. Hardware breakpoint
`0x004679C7` won with one hit and all three read watches had no hit counts.
After deleting only the return breakpoint, the watches stayed enabled with no
stop while execution crossed the title and reached logged `NextLife` plus
captured live gameplay. All values remained zero.

A queued load-phase Return advanced the title before an unattended pause
capture could be retained. The exact endpoint is therefore the later gameplay
capture, not a title-pause screenshot.

### Second-entry arm

In `RUN-GDB-20260812-163840`, watches on `0x005AAB50`, `0x005AAB54`, and
`0x005AAB58` began at the matched guarded `0x00445B01`. Again,
`0x004679C7` won with one hit and all three read watches had no hit counts.
They remained enabled with no stop while execution crossed the title and
reached logged `NextLife` plus captured live gameplay. All values remained
zero.

User input advanced this title before an unattended pause capture was
retained. The input is recorded explicitly; it does not invalidate the
earlier guarded or return boundaries, and the later gameplay endpoint
encompasses the title transition.

### Runtime gates

Each run contains one `Screen mode 640x480x16 selected`, one
`Starting Direct3D renderer`, no `INITSOFTRENDER`, both plant 10 requests, one
`End InitMainGame`, and one `NextLife`. All hardware points were deleted before
detach.

## Confirmed

- At the guarded plant 10 start, both entries' exact first three dwords are
  zero and `+0x0C == 1`.
- No CPU data read overlaps first-entry `0x005AAB00–0x005AAB0B` or second-
  entry `0x005AAB50–0x005AAB5B` from their matched guarded starts through
  batch return `0x004679C7`.
- The same six ranges remain unread and unchanged while both runs cross the
  title transition and reach captured live gameplay.
- Both unchanged runs pass the exact Direct3D, plant-request, and `NextLife`
  gates.

## Inferred

The remaining nonzero entry-head dword `+0x0C` is a narrower next
discriminator than widening to later unknown fields. Static indexed reads at
`0x00446A97` and `0x00447668` make it independently reviewable without
establishing an exact plant 10 hit or field meaning.

## Unknown and limitations

- The meaning and first exact plant 10 reader of `+0x0C` remain unknown.
- Neither run retains an unattended title-pause capture; both retain a later
  gameplay endpoint after recorded input advanced the title.
- Later entry fields, non-CPU consumption, and events after the captured
  gameplay endpoint remain open.
- No plant 10 entry is connected to an M1 placement or visible outcome.

## Contradictions and negative results

No runtime reader was found for any of the six exact first-three-dword ranges.
The zero values do not justify renaming them as padding. The planned title
pause was advanced in each arm—by queued input in the first and user input in
the second—so the experiment retains and labels the later endpoint rather
than silently claiming an unattended pause.

## Result

M2.11 is complete with matched negative windows for both entries'
`+0x00/+0x04/+0x08` ranges from guarded final population through resource-
batch return and across the title into live gameplay.

## Follow-up

Watch only the two exact nonzero `+0x0C` dwords, `0x005AAB0C` and
`0x005AAB5C`, from the same guarded boundary. Use `0x004679C7` as the return
bound, retain the watches through a no-input title capture when possible, and
correlate any hit with exact static instructions. Do not assign semantics,
mutate memory, parse/edit `.ALL`, or consult PS1.
