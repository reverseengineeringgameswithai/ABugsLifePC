---
type: experiment
id: EXP-20260812-021
date: 2026-08-12
question: What exact runtime destination does the Training plant 10 pair request populate, and do M1 records 124-126 read its pointer surface during direct dispatch?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, native GDB, Gamescope
environment_version: wine-11.0-staging; gdb-17.1-6.fc44; gamescope-3.16.25-1.fc44
working_directory: /home/dev/ABLPC/work/copies/BUGS_PC-full-disc/PC/BUGS
configuration: Unchanged Training copy; Direct3D hardware 640x480x16; native hardware breakpoints and read watchpoints
artifacts:
  - dynamic/wine/RUN-GDB-20260812-153150/debugger-evidence.txt
  - dynamic/wine/RUN-GDB-20260812-153150/bugs.log
  - dynamic/wine/RUN-GDB-20260812-153150/metadata.json
  - static/exports/BIN-97c95ba5572dce63/M2-plant10-runtime-destination-trace.md
addresses:
  - 0x0044596D
  - 0x00445B01
  - 0x00449B61
  - 0x00449E20
  - 0x00449E25
  - 0x005B1AA4
  - 0x005AAB00
  - 0x005AABA0
file_offsets:
  - 0x0E60
  - 0x0E74
  - 0x0E88
result: plant10-destination-resolved-direct-m1-pointer-surface-negative
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/resources
  - re/rendering
---

# EXP-20260812-021 - Plant10 runtime destination and M1 negative window

## Question

What exact runtime object/table destination is populated by the Training plant
10 call through `0x00444C40`, and do the already bounded M1 records 124–126
read its pointer surface during their direct dispatch-to-target-renderer paths?

## Inputs

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged Training `CD/LEVEL07/LEVEL1.DAT` SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`.
- Exact plant 10 call site `0x00445968`, post-call address `0x0044596D`,
  pair loader `0x00444C40`, and M1 dispatch/renderer path
  `0x00449B61 → 0x00449E20`.
- Prior request and M1 evidence: [[EXP-20260812-020 - Training plant10 request suppression]],
  [[EXP-20260812-008 - Training record watchpoints and individual roles]], and
  [[EXP-20260812-010 - Training target rebind visible substitution]].

No executable, register, memory value, or game file was modified. No PS1 source
or finding was consulted. The raw GDB transcript and screenshots remain under
ignored `work/`; no memory dump or game bytes are committed.

## Expected discriminator

- If the plant 10 pair's exact pointer destinations directly participate in
  an M1 record's dispatch-to-renderer path, a read watchpoint should stop before
  the post-renderer hardware breakpoint at `0x00449E25`.
- If the post-renderer breakpoint wins without a plant watchpoint hit, the run
  supplies a bounded negative window for only the watched pointer surface. It
  does not exclude other entry fields, copied state, or later consumers.

## Procedure

1. Launch the unchanged ignored Training copy through
   `scripts/play-pristine.sh --research`, select hardware acceleration, and
   require the 640×480×16 Direct3D log markers.
2. At the level-selection pause, attach native GDB and ignore Wine's expected
   `SIGUSR1`/`SIGUSR2` worker notifications.
3. Place a hardware execution breakpoint at `0x0044596D`. Select Training and
   record the exact plant 10 arguments, per-ID slot, runtime ANM header, and
   object-table bounds.
4. Stop again at `0x00445B01` after the caller adjustments and re-read only the
   bounded address/offset values.
5. At the natural Training title pause, arm a hardware read watchpoint on each
   record's relocated `+0x10` field in turn. Press a key to enter gameplay and
   confirm its exact dispatch stop immediately after `0x00449B61`.
6. For each record, replace that watchpoint with three read watchpoints on the
   plant 10 ANM slot and both bounded entry `+0x20` dwords, plus a hardware
   execution breakpoint at the `0x00449E25` renderer return.
7. Remove all break/watchpoints, detach, and require `End InitMainGame` and
   `NextLife` in the game log.

## Observed

### Exact runtime destination

At `0x0044596D`, the cdecl arguments still identified exact path
`0x004DDC6C` (`plants\\plant10`), resource ID `0x71`, and the two caller-owned
pointers. The resource-ID-specific slot was:

```text
0x005B18E0 + 0x71 * 4 = 0x005B1AA4
0x005B1AA4 == 0x006C342B
```

The live ANM words at `+0x04/+0x06` were `66/68`. Combined with the exact
`0x50`-byte global table root `0x005A9660`, they bound two entries at
`[0x005AAB00, 0x005AABA0)`. Their nonzero entry-relative `+0x20` dwords were
`0x006C3B3B` and `0x006C3E57`. At `0x00445B01`, the same bounds remained and
the caller-adjusted first-entry dword at `+0x24` was `0xD7E00218`.

Static instructions independently establish the per-ID slot calculation,
header index writes, table stride, and caller adjustment. Runtime values bind
that layout specifically to the exact Training plant 10 request.

### Direct M1 windows

Each record `+0x10` watchpoint stopped at `0x00449B64`, immediately after the
statically identified payload read:

| Record | Live record | Live payload | Live target |
|---:|---:|---:|---:|
| 124 | `0x00659F37` | `0x0065B7B3` | `0x0066C273` |
| 125 | `0x00659F4B` | `0x0065B7D3` | `0x0066A2BB` |
| 126 | `0x00659F5F` | `0x0065B7F3` | `0x0066A2BB` |

For every record, the next stop was `0x00449E25`, immediately after the
target-renderer call. None of the watchpoints on `0x005B1AA4`, `0x005AAB20`,
or `0x005AAB70` fired. The target argument retained at each return was the
corresponding DAT-relative target in the table, and none aliases the ANM buffer
or bounded object range.

### Runtime gates

`RUN-GDB-20260812-153150` contains one `Screen mode 640x480x16 selected`
marker, one `Starting Direct3D renderer` marker, no `INITSOFTRENDER`, both
plant 10 request lines, `End InitMainGame`, and `NextLife`. All debugger
break/watchpoints were deleted before detach.

## Confirmed

- The exact plant 10 call populates ANM slot `0x005B1AA4`; its runtime header
  bounds exactly two `0x50`-byte entries at `[0x005AAB00, 0x005AABA0)` in
  this Training run.
- Records 124–126 reach the exact direct dispatch/renderer path with their
  previously established payloads and targets.
- The plant 10 ANM slot and the two bounded entry `+0x20` dwords are not read
  between each record's `0x00449B64` dispatch stop and `0x00449E25` target-
  renderer return.
- The unchanged executable completes the required Direct3D initialization and
  reaches `NextLife` after debugger detach.

## Inferred

- The two entry `+0x20` values are pointer-like references into the resource
  arena. Their field semantics and the complete `.ALL` layout remain unknown.
- The direct M1 positive-target renderer consumes DAT-resident render content
  without consulting the three watched plant 10 destinations in these exact
  windows. This does not exclude an indirect dependency prepared elsewhere.

## Unknown and limitations

- Whether another dword in the two object entries is read by an M1 path.
- Which later PC functions first consume the two plant 10 entries and whether
  they produce a visible, animated, off-camera, or nonvisual outcome.
- Whether plant state is copied to another runtime structure before the M1
  window. No absence claim is made for copied or derived state.
- The broader direct placement/resource identity in `KU-023` remains unknown.

## Contradictions and negative results

The live destination is not a single monolithic object pointer: one per-ID ANM
slot points to a header that bounds two separate global entries, while four
other per-ID auxiliary slots were zero at the measured post-call boundary.
That distinction is retained rather than naming an unsupported structure.

The three negative windows disfavor the simplest direct-pointer interpretation
for records 124–126, but do not justify claiming that plant 10 is unrelated to
the visible scene or that the complete entry range is unread.

## Result

M2.8 is complete. Plant 10's exact runtime destination is bound with matching
PC static and dynamic evidence, and the already bounded M1 direct path has a
precisely delimited negative access result at the tested pointer surface. No
placement/resource identity is promoted.

## Follow-up

Trace the first post-initialization readers of the two exact plant 10 entry
`+0x20` dwords and the caller-adjusted `+0x24/+0x26` words. Use those PCs and
call stacks to identify a downstream PC-native consumer before attempting
another placement comparison.
