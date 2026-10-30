---
type: experiment
id: EXP-20260812-023
date: 2026-08-12
question: Are the exact Training plant 10 +0x20 and adjusted +0x24/+0x26 ranges read after their plant-specific caller adjustment but before resource-batch return or the natural title?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, native GDB, Gamescope
environment_version: wine-11.0-staging; gdb-17.1-6.fc44; gamescope-3.16.25-1.fc44
working_directory: /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS
configuration: Unchanged Training copy; Direct3D hardware 640x480x16; native hardware breakpoints and read watchpoints
artifacts:
  - dynamic/wine/RUN-GDB-20260812-161520/debugger-evidence.txt
  - dynamic/wine/RUN-GDB-20260812-161520/bugs.log
  - dynamic/wine/RUN-GDB-20260812-161520/metadata.json
  - static/exports/BIN-97c95ba5572dce63/M2-plant10-late-init-negative-trace.md
addresses:
  - 0x0044596D
  - 0x00445B01
  - 0x004480FB
  - 0x00448103
  - 0x004679C2
  - 0x004679C7
  - 0x005AAB20
  - 0x005AAB24
  - 0x005AAB70
result: plant10-late-init-pointer-surface-bounded-negative
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
---

# EXP-20260812-023 - Plant10 late-initialization pointer-surface negative

## Question

Does any PC function read the exact Training plant 10 entry pointer surface
after the plant-specific caller adjustment but before the complete scene-
resource batch returns or the natural title pause, and does that reader copy or
derive downstream state?

## Inputs

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Unique plant 10 post-call `0x0044596D`, common resource-loop tail
  `0x00445B01`, resource-batch call/return `0x004679C2/0x004679C7`, and the
  exact two-entry range from
  [[EXP-20260812-022 - Plant10 post-init object-entry negative]].
- Exact watched dwords `0x005AAB20`, `0x005AAB70`, and `0x005AAB24`.

No executable, register, memory value, or game file was modified. No PS1 source
or finding was consulted. Raw GDB text and the title capture remain ignored
under `work/copies/EXP-20260812-023/evidence/`; no raw transcript, capture, or
game bytes are committed.

## Expected discriminator

- A read-watchpoint stop after the plant-specific adjustment supplies a first
  late-initialization reader PC and a concrete copy/derivation path.
- If the `0x004679C7` hardware breakpoint wins and the watches then remain
  untouched through the natural title, the result excludes CPU reads only for
  the exact three ranges in those bounded intervals.

## Procedure

1. Launch the unchanged ignored Training copy through
   `scripts/play-pristine.sh --research`, select hardware acceleration, and
   require the 640×480×16 Direct3D markers.
2. At level selection, attach native GDB and suppress only Wine's expected
   worker `SIGUSR1`/`SIGUSR2` stops.
3. Guard the common loop tail by first stopping at unique plant 10 address
   `0x0044596D`; reproduce resource ID `0x71`, header indices `66/68`, and the
   two exact `+0x20` values.
4. Accept only the immediately following `0x00445B01`, reproduce adjusted
   dword `0xD7E00218`, delete that execution breakpoint, and arm hardware read
   watchpoints on `0x005AAB20`, `0x005AAB70`, and `0x005AAB24` plus a hardware
   execution breakpoint at `0x004679C7`.
5. Record whether a watchpoint or batch-return breakpoint wins. If return wins,
   delete only it and retain all three watches through the natural Training
   title pause.
6. At the title boundary, inspect watchpoint hit state and values, delete all
   watches, confirm none remain, detach, resume, press the title key, and
   require `End InitMainGame` and `NextLife`.

## Observed

### Rejected unguarded stop

The first unguarded `0x00445B01` stop occurred after an earlier resource ID:
the plant 10 slot and all three target dwords were zero. Temporary watches were
therefore outside M2.10. One reported at `0x00448107` immediately after exact
instructions `0x004480FB/0x00448103` populated watched bytes. Registers placed
the destination at entry `0x005AAB00`. The transcript explicitly marks this
window rejected; all temporary break/watchpoints were deleted, and it supports
no downstream-reader conclusion.

Static instructions independently show `0x00445B01` is a common loop tail.
This contradiction corrected the runtime protocol without changing the game
state or restarting the accepted process.

### Accepted plant-specific start

At `0x0044596D`, retained stack arguments identified exact plant 10 path
`0x004DDC6C` and resource ID `0x71`. Read-only values were:

```text
0x005B1AA4 = 0x006C342B
ANM +0x00/+0x02/+0x04/+0x06 = 1/3/66/68
0x005AAB20 = 0x006C3B3B
0x005AAB70 = 0x006C3E57
0x005AAB24 = 0x00000000
```

At the immediately following `0x00445B01`, `0x005AAB24` had become
`0xD7E00218`, with halfwords `0x0218`/`0xD7E0`. This stop at
`2026-08-12T16:17:50.724669406-04:00` is the accepted M2.10 start.

### Resource-batch-return boundary

The hardware breakpoint at `0x004679C7` won. At
`2026-08-12T16:18:12.439777208-04:00`, all three read watchpoints remained
enabled with no hit count, while the return breakpoint had one hit. All three
source dwords were unchanged. Exact instructions independently place
`0x004679C7` immediately after the thunked call from `0x004671D0` to
`0x00445020`.

### Natural-title boundary

After deleting only the return breakpoint, none of the three watches fired
before an ignored native capture proved the natural Training title at
`2026-08-12T16:19:17.788233063-04:00`. The debugger stop again listed all
three with no hit counts; dwords `0x006C3B3B`, `0x006C3E57`, and
`0xD7E00218` and halfwords `0x0218`/`0xD7E0` were unchanged. All watches were
deleted, GDB reported no remaining break/watchpoint, and detached execution
reached logged `End InitMainGame` and `NextLife`.

### Runtime gates

`RUN-GDB-20260812-161520` contains one `Screen mode 640x480x16 selected`, one
`Starting Direct3D renderer`, no `INITSOFTRENDER`, both plant 10 request lines,
one `End InitMainGame`, and one `NextLife`.

## Confirmed

- A direct `0x00445B01` breakpoint is not plant-specific; unique
  `0x0044596D` must guard the immediately following common-tail stop.
- No CPU data read overlaps `0x005AAB20–0x005AAB23`,
  `0x005AAB70–0x005AAB73`, or `0x005AAB24–0x005AAB27` from the accepted
  plant-specific `0x00445B01` through batch return `0x004679C7`.
- The same three ranges remain unread and unchanged from batch return through
  the natural Training title pause.
- The unchanged process passes the Direct3D and `NextLife` gates after all
  debugger points are removed and GDB detaches.

## Inferred

The exact three pointer-surface ranges are now disfavored as a post-population
CPU bridge to Training behavior. Another statically populated entry field is a
more direct next target than a longer watch on these same values.

## Unknown and limitations

- Entry-head dwords `+0x00/+0x04/+0x08/+0x0C`, later entry fields, and their
  semantics remain unknown.
- Non-CPU consumption and an event outside the retained post-title window are
  not excluded.
- No plant 10 entry is connected to an M1 placement or visible outcome.

## Contradictions and negative results

The roadmap described `0x00445B01` as the post-plant-10 start, but runtime and
static evidence show it is shared by earlier resource IDs. The accepted method
now requires `0x0044596D` first. The corrected two-boundary result remains
negative and does not support naming the watched fields or declaring them
unused.

## Result

M2.10 is complete with precise negative windows from the plant-specific caller
adjustment through scene-resource batch return and the natural title. Together
with M2.9, no CPU reader of the exact three source ranges is observed after
their final plant 10 population through the measured gameplay interval.

## Follow-up

Widen only to the statically evidenced entry-head dwords copied by
`0x004480DF/0x004480E5/0x004480EB/0x004480F1`. Guard the start with unique
`0x0044596D` and its immediately following `0x00445B01`, then watch first-
entry `+0x00/+0x04/+0x08` through `0x004679C7` and the title. If negative,
repeat the same matched window for the second entry before adding another
field.
