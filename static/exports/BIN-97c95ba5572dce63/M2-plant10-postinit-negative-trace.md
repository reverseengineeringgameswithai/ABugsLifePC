# M2 plant 10 post-initialization negative trace

## Scope and identity

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Static anchors: `0x00444D06`, `0x004480BD–0x00448103`, and
  `0x00445968–0x00445B01`
- Runtime evidence: `RUN-GDB-20260812-155922` in
  [[EXP-20260812-022 - Plant10 post-init object-entry negative]]

No PS1 source or finding was consulted. The trace uses exact `objdump -d
-Mintel` instructions from the hashed PC executable and the unchanged live PC
run. Field names remain offset-based.

## Exact watched-address construction

At `0x00444D06`, the pair coordinator stores the loaded ANM pointer through
the resource-ID-scaled base `0x005B18E0`. Resource ID `0x71` therefore selects
`0x005B1AA4`. Its header words `+0x04/+0x06` are written at `0x00444D1D` and
`0x00444DDC`; live values `66/68` again bound the two 0x50-byte entries rooted
at `0x005A9660`.

Within `0x00448010`, exact instructions calculate an entry-relative `+0x20`
destination and store the arena pointer there:

```text
004480b4  lea edx,[ecx+ecx*4]
004480ba  shl edx,0x4
004480bd  add edx,0x5a9680
...
004480f4  mov eax,DWORD PTR [esi]
004480f6  mov DWORD PTR [edx],eax
00448141  add edx,0x50
```

Because `0x005A9680 == 0x005A9660 + 0x20`, entries 66 and 67 select exact
dwords `0x005AAB20` and `0x005AAB70`. `RUN-GDB-20260812-155922` reproduced
their values as `0x006C3B3B` and `0x006C3E57`.

The plant-10-specific caller then reads ANM slot `0x005B1AA4`, converts header
index `+0x04` to the same 0x50-byte stride, and writes its two local words:

```text
0044596d  mov ecx,DWORD PTR ds:0x5b1aa4
00445976  movsx eax,WORD PTR [ecx+0x4]
0044597a  lea edx,[eax+eax*4]
00445985  shl edx,0x4
00445988  mov WORD PTR [edx+0x5a9684],ax
...
00445997  movsx eax,WORD PTR [ecx+0x4]
0044599b  lea ecx,[eax+eax*4]
0044599e  shl ecx,0x4
00445afa  mov WORD PTR [ecx+0x5a9686],dx
```

For index 66, the two destinations are `0x005AAB24` and `0x005AAB26`.
Their reproduced combined dword is `0xD7E00218`.

## Runtime boundary

The three hardware read watchpoints were armed only after the exact values
above were stable and the unchanged game had reached the natural Training
title pause. Thus they exclude the initialization reads/writes shown above.
The four-byte watch at `0x005AAB24` covers CPU reads overlapping either caller-
adjusted halfword.

From the start key at `2026-08-12T16:03:54.126557089-04:00` through the stop
at `2026-08-12T16:05:05.834761548-04:00`, none of the three hardware read
watchpoints fired. The game log places `End InitMainGame` and `NextLife` in
this accepted run, and the watched values were unchanged at the terminal stop.

## Evidence-strength boundary

**Confirmed within the exact window:** No CPU data read overlaps the two exact
entry `+0x20` dwords or the first-entry `+0x24/+0x26` dword during the
71.708-second post-title gameplay interval.

**Inferred:** If these values affect later gameplay, a viable route is state
copied during late initialization, another entry field, or an event outside
the observed interval. The negative result does not choose among those routes.

**Unknown:** Whether any first read occurs after `0x00445B01` but before the
title pause. That interval is the next direct discriminator; no semantic field
name or placement identity is supported.
