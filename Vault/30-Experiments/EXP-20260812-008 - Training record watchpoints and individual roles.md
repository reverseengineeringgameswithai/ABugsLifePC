---
type: experiment
id: EXP-20260812-008
date: 2026-08-12
question: Do training primary records 124-126 reach a common PC runtime consumer, and are they alternative representations of one object or distinct placements?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora, Wine, native GDB, Gamescope
environment_version: wine-11.0-staging, gdb-17.1-6.fc44
result: common-consumer-and-distinct-visible-elements-confirmed
created: 2026-08-12
updated: 2026-08-12
tags:
  - re/experiment
  - re/dynamic
  - re/file-format
---

# EXP-20260812-008 - Training record watchpoints and individual roles

## Question

Do training primary records 124–126 reach a common PC runtime consumer, and
are they alternative representations of one object or distinct placements?

## Inputs

- Exact PC executable SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Training `CD/LEVEL07/LEVEL1.DAT` SHA-256: `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Primary record file offsets: 124 at `0x0E60`, 125 at `0x0E74`, and 126 at `0x0E88`
- Static functions: `0x0044BB70` and `0x0044D430`
- Runtime debugger evidence: `RUN-GDB-20260812-021920`
- Matched visual runs: `RUN-WINE-20260812-022322`, `RUN-WINE-20260812-022549`, `RUN-WINE-20260812-022649`, and control `RUN-WINE-20260812-022754`

## Expected

A watchpoint should identify the PC-native consumer of each first dword. Moving
one record at a time should distinguish three placements from one group of
alternative representations.

## Procedure

1. Confirm the post-fixup live mapping without writing memory: load the pointer
   stored at `0x005BA240`, add each file offset, and inspect the relocated
   `+0x10` payload pointers.
2. Record failed debugger methods rather than attributing their faults to the
   game.
3. Select Training, stop at the game's natural “press a key to start” title,
   attach native GDB, and place a one-byte hardware read watchpoint on each
   record's first dword in sequence.
4. Continue after each hit, remove all watchpoints, detach, and confirm the game
   completes `InitMainGame` and enters `NextLife`.
5. Stage three separate work-tree copies using hash-locked manifests. Change
   only one record's first dword to `50000` in each copy and preserve its other
   two position candidates.
6. Run every variant and an untouched control in the Direct3D hardware renderer
   through the known-good `X:\PC\BUGS` drive shape.
7. Capture the first stationary Training scene through Gamescope PipeWire,
   normalize each centered 4:3 image to 640×480, and compute exact pixel
   differences against the matched control.

## Observed

### Runtime mapping and consumer

- `*(uint32_t *)0x005BA240` was `0x006590D7`; the global stores a pointer to the
  loaded DAT rather than the DAT bytes themselves.
- Live record addresses were `0x00659F37`, `0x00659F4B`, and `0x00659F5F`.
- Record payload pointers were fixed up to `base+0x26DC`, `base+0x26FC`, and
  `base+0x271C`.
- The last dword in record 124's 32-byte payload pointed to `base+0x1319C`.
  Records 125 and 126 both pointed to `base+0x111E4` at the corresponding
  location.
- Every watchpoint stopped at PC `0x0044D5BA`, immediately after
  `0x0044D5B8: mov eax,DWORD PTR [esi]`, with `ESI` equal to the watched record
  address. This instruction is inside `0x0044D430`.
- After watchpoint removal and detach, the unchanged run reached `NextLife`.

Evidence: `dynamic/wine/RUN-GDB-20260812-021920/`.

### Individual mutations

| Record | Output DAT SHA-256 | Differing pixels | Exact difference box | Visible result |
|---:|---|---:|---|---|
| 124 | `10e42b43…e64c7` | 2,942 | `52x241+369+0` | Thin, top-clipped plant element absent |
| 125 | `4d3caae85…457b6` | 642 | `24x99+616+124` | Separate element at right frame edge absent |
| 126 | `6425f88bf…be965` | 8,265 | `109x250+438+0` | Prominent flower and stalk absent |

All three output hashes are recorded in full in their manifest receipts. Every
run completed `InitMainGame` and entered `NextLife`. The three exact difference
boxes are disjoint; outside each box, that variant matches the control.

Evidence: `dynamic/wine/EXP-20260812-008-comparison.txt` and the four cited
`RUN-WINE` directories.

## Confirmed

- All three first dwords reach the same PC instruction at `0x0044D5B8` during
  the observed Training initialization/update path.
- Moving each record independently removes a different visible plant element
  in the matched starting camera. Records 124–126 are not three alternative
  LOD representations of one on-screen object in this state.
- Records 125 and 126 share the same observed internal payload target at file
  offset `0x111E4`; record 124 instead targets `0x1319C` at that payload field.
- The hardware-renderer edit-test loop, staged manifests, and natural-pause
  native-GDB watchpoints are reproducible without modifying the original files.

## Inferred

- The records are separate visible scene selections. Records 125 and 126 likely
  reuse a common referenced definition, but the target's semantics remain
  unknown at this experiment boundary.
- At this point the first dword was interpreted as an X-position or spatial-
  center component. `EXP-20260812-011` later discriminates those alternatives:
  it is an upstream candidate-center component for dispatch `0x49`, not that
  dispatch's render-placement input.

## Unknown

- Formal identities of the three plant elements and whether payload targets
  `0x111E4` and `0x1319C` identify geometry, an object definition, or another
  structure.
- Whether and when these primary records are revisited after initialization; a
  late 25-second gameplay watch window did not produce a read.
- Why native GDB software breakpoints and WineDbg's GDB proxy destabilize this
  WoW64 target while native hardware watchpoints at a natural pause succeed.

## Contradictions and negative results

- `EXP-20260812-006` described the joint visual effect as removal of one central
  flower cluster and left an LOD hypothesis open. The wider matched hardware
  view and disjoint individual differences discriminate that hypothesis: three
  separate visible placements were jointly moved.
- A native software breakpoint at `0x00467976` hit but faulted on continue.
  WineDbg's proxy later faulted in its injected thread at `0xFFBF0D6C`. These
  are recorded as debugger interference, not game defects.

## Result

Completed. The common runtime consumer and three distinct visible roles are
confirmed for the tested Training start state. The shared payload target of
records 125 and 126 is the next bounded structural lead.

## Follow-up

Trace the consumers and bounded structure of payload targets `0x111E4` and
`0x1319C` in the exact PC executable, then design one PC-native experiment to
test whether the shared target represents reusable object content.

## Artifacts

- `dynamic/wine/RUN-GDB-20260812-021920/`
- `dynamic/wine/EXP-20260812-008-comparison.txt`
- `dynamic/wine/RUN-WINE-20260812-022322/`
- `dynamic/wine/RUN-WINE-20260812-022549/`
- `dynamic/wine/RUN-WINE-20260812-022649/`
- `dynamic/wine/RUN-WINE-20260812-022754/`
- `mods/training-primary-record-124-candidate-far.json`
- `mods/training-primary-record-125-candidate-far.json`
- `mods/training-primary-record-126-candidate-far.json`
