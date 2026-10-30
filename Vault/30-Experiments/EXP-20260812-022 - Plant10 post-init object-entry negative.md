---
type: experiment
id: EXP-20260812-022
date: 2026-08-12
question: Which PC function first reads the exact Training plant 10 entry +0x20 dwords or caller-adjusted +0x24/+0x26 words after initialization?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, native GDB, Gamescope
environment_version: wine-11.0-staging; gdb-17.1-6.fc44; gamescope-3.16.25-1.fc44
working_directory: /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS
configuration: Unchanged Training copy; Direct3D hardware 640x480x16; native hardware breakpoints and read watchpoints
artifacts:
  - dynamic/wine/RUN-GDB-20260812-155922/debugger-evidence.txt
  - dynamic/wine/RUN-GDB-20260812-155922/bugs.log
  - dynamic/wine/RUN-GDB-20260812-155922/metadata.json
  - static/exports/BIN-97c95ba5572dce63/M2-plant10-postinit-negative-trace.md
addresses:
  - 0x0044596D
  - 0x00445B01
  - 0x004480BD
  - 0x004480F6
  - 0x005AAB20
  - 0x005AAB24
  - 0x005AAB70
result: plant10-postinit-pointer-surface-bounded-negative
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
---

# EXP-20260812-022 - Plant10 post-init object-entry negative

## Question

Which PC function first reads the exact Training plant 10 object-entry
`+0x20` dwords or caller-adjusted first-entry `+0x24/+0x26` words after
initialization, and what downstream state or behavior does that reader
establish?

## Inputs

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Plant 10 call/post-call `0x00445968/0x0044596D`, caller-adjustment end
  `0x00445B01`, and exact two-entry range `[0x005AAB00, 0x005AABA0)` from
  [[EXP-20260812-021 - Plant10 runtime destination and M1 negative window]].
- Exact watched dwords `0x005AAB20`, `0x005AAB70`, and `0x005AAB24`.

No executable, register, memory value, or game file was modified. No PS1 source
or finding was consulted. Raw GDB text and captures remain ignored under
`work/copies/EXP-20260812-022/evidence/`; no game bytes, raw transcript, or
capture is committed.

## Expected discriminator

- A hardware read-watchpoint stop supplies the first observed reader PC and a
  concrete static consumer to follow.
- If all three watchpoints remain armed through `NextLife` and a stated live-
  gameplay interval, the result is a negative only for those exact byte ranges
  and that time window. It does not exclude copied state, other entry fields,
  GPU-resident state, or later event-driven access.

## Procedure

1. Launch the unchanged ignored Training copy through
   `scripts/play-pristine.sh --research`, select hardware acceleration, and
   require the 640×480×16 Direct3D log markers.
2. At level selection, attach native GDB, ignore Wine's expected worker
   `SIGUSR1`/`SIGUSR2` notifications, and stop at `0x0044596D`.
3. Reproduce the plant 10 ANM slot, header indices, exact two-entry bounds,
   and two `+0x20` values. Stop at `0x00445B01` and reproduce the adjusted
   first-entry words.
4. Continue without watchpoints to the natural Training Level "press a key to
   start" pause. Interrupt execution only long enough to reread the exact
   values and arm hardware read watchpoints on `0x005AAB20`, `0x005AAB70`,
   and dword `0x005AAB24`.
5. Continue, press the start key, and retain all three watchpoints through the
   logged `End InitMainGame`/`NextLife` boundary and a measured gameplay
   interval.
6. Interrupt at the terminal boundary, inspect watchpoint hit state and exact
   values, delete all watchpoints, confirm none remain, and detach.

An earlier navigation pass was rejected because it entered gameplay before
the watchpoints were armed. It contributes no access conclusion. The accepted
run is `RUN-GDB-20260812-155922` only.

## Observed

### Initialization reproduction

At `0x0044596D`, the live slot and header were unchanged from M2.8:

```text
0x005B1AA4 = 0x006C342B
ANM +0x00/+0x02/+0x04/+0x06 = 1/3/66/68
0x005AAB20 = 0x006C3B3B
0x005AAB70 = 0x006C3E57
```

Indices `66/68` again delimit `[0x005AAB00, 0x005AABA0)`. At
`0x00445B01`, `0x005AAB24 == 0xD7E00218`, with halfwords `0x0218` and
`0xD7E0`. Exact executable instructions independently construct and write all
three watched ranges; see the retained static trace.

### Post-initialization window

All three values were reread unchanged at the natural title pause immediately
before the watchpoints were armed. The start key was sent at
`2026-08-12T16:03:54.126557089-04:00`. The accepted log records
`End InitMainGame` and `NextLife`, and an ignored capture confirms live
gameplay after the key.

No read watchpoint fired. At
`2026-08-12T16:05:05.834761548-04:00`, exactly `71.708204459` seconds after
the key, GDB still listed all three enabled watchpoints with no hit count. The
three dwords and both caller-adjusted halfwords remained unchanged. All
watchpoints were deleted and GDB reported no remaining break/watchpoint before
detach.

### Runtime gates

`RUN-GDB-20260812-155922` contains one `Screen mode 640x480x16 selected`, one
`Starting Direct3D renderer`, no `INITSOFTRENDER`, both plant 10 request lines,
one `End InitMainGame`, and one `NextLife`.

## Confirmed

- The unchanged run reproduces plant 10's indices `66/68`, two-entry range,
  both `+0x20` dwords, and adjusted first-entry words exactly.
- No CPU data read overlaps `0x005AAB20–0x005AAB23`,
  `0x005AAB70–0x005AAB73`, or `0x005AAB24–0x005AAB27` from the title-start
  key through the exact 71.708-second gameplay interval.
- The accepted process reached the required Direct3D `NextLife` state with all
  three hardware watchpoints armed and no watchpoint hit.

## Inferred

If the measured entry values contribute to downstream behavior, a viable path
is an earlier late-initialization read/copy, another entry field, or an event
outside the observed interval. The negative window does not choose among
these routes.

## Unknown and limitations

- Whether a first read occurs after `0x00445B01` but before the title pause.
- Whether other dwords in the two entries are copied or consumed.
- Whether an initialization-time copy reaches GPU- or engine-owned state that
  no longer consults these exact source ranges during gameplay.
- The complete `.ALL` layout, field meanings, and broader M1
  placement/resource identity remain unknown.

## Contradictions and negative results

The roadmap expected a first post-initialization reader to be a likely next
anchor. None exists in the exact 71.708-second window on the three tested
ranges. This contradicts only that timing expectation, not the possibility of
an initialization-time consumer or another source field.

## Result

M2.9 is complete with a bounded post-initialization negative. The tested
pointer surface is stable and unread across the required title-to-gameplay
window, so no downstream function or semantic identity is assigned.

## Follow-up

Arm the same three hardware read watchpoints immediately at `0x00445B01`,
after the plant 10 caller adjustments but before the remaining scene-resource
and title initialization. Bound the window with the resource-batch return at
`0x004679C7` and then the natural title pause. Any hit should be correlated to
exact static instructions and its destination state before widening to other
entry fields.
