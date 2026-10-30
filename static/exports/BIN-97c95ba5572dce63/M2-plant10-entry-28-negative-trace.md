# M2 plant 10 entry +0x28 negative trace

## Scope and identity

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Runtime words: first entry `0x005AAB28`, second entry `0x005AAB78`
- Runtime evidence: `RUN-GDB-20260812-201419` in
  [[EXP-20260812-027 - Plant10 entry 28 bounded negative]]

No PS1 source or finding was consulted. Field descriptions remain exact
entry-relative offsets.

## Exact population boundary

Address-based function `0x00448010` derives selected runtime entry `+0x20`
and copies three descriptor words into entry `+0x24`, `+0x26`, and `+0x28`:

```text
004480b4  lea edx,[ecx+ecx*4]
004480ba  shl edx,0x4
004480bd  add edx,0x5a9680
004480f8  mov ax,WORD PTR [ecx]
004480fb  mov WORD PTR [edx+0x4],ax
004480ff  mov ax,WORD PTR [ecx+0x10]
00448103  mov WORD PTR [edx+0x6],ax
00448107  mov ax,WORD PTR [ecx+0x8]
0044810b  mov WORD PTR [edx+0x8],ax
```

Because `edx == 0x005A9680 + index * 0x50`, `[edx+0x08]` is entry
`+0x28`. Plant 10 ANM header indices `66/68` therefore identify exact words
`0x005AAB28` and `0x005AAB78`. The accepted run reproduces both as unsigned
zero at unique post-call `0x0044596D` and the immediately following common
tail `0x00445B01`.

## Bounded runtime result

At `0x00445B01`, hardware read watchpoints were armed on both exact two-byte
ranges. Resource-batch return `0x004679C7` won with one hit while neither
watchpoint had a hit count. Both values remained zero.

After deleting only the return breakpoint, both watches remained enabled and
silent until an unattended Training title capture at
2026-08-12T20:18:46.810212628-04:00. At final debugger inspection, neither
watch had a hit count and both values remained unchanged. All hardware points
were deleted before detach.

## Exhausted initialization surfaces

The exact entry fields populated by `0x00448010` are
`+0x00/+0x04/+0x08/+0x0C`, `+0x20`, `+0x24/+0x26`, `+0x28`, and `+0x2E`.
M2.9-M2.14 now provide explicit read-watchpoint windows for each of those
surfaces. This exhausts those statically tied fields only for the measured
initialization/title intervals. It does not classify zero words as padding,
exclude later reads, or define the rest of the 0x50-byte entry.

## Next event-specific candidate

Address-based function `0x0044CA00` contains a narrower post-title candidate:

```text
0044ce0d  movsx ecx,WORD PTR [edi-0x8]
0044ce11  mov eax,DWORD PTR [ecx*4+0x5b1a7c]
0044ce18  movsx ecx,WORD PTR [eax+0x4]
0044ce1c  movsx edx,WORD PTR [eax+0x6]
0044ce20  lea esi,[ecx+ecx*4]
0044ce27  shl esi,0x4
0044ce2a  add esi,0x5a9660
0044ce3e  movsx eax,WORD PTR [esi+0x2e]
...
0044d1d8  add esi,0x50
0044d1e7  movsx ecx,WORD PTR [edx+0x6]
0044d1ed  jl 0x0044ce3a
```

The exact code selects a per-resource pointer from table `0x005B1A7C`, reads
its header start/end words, derives a 0x50-byte entry range, and reads each
entry `+0x2E` word. Plant 10's measured slot is
`0x005B1A7C + 10 * 4 == 0x005B1AA4`, with header bounds `66/68`.

This supplies a statically exact candidate for a controlled post-title trace.
It does not prove that a Training source record supplies selector 10 to
`[edi-0x08]`, that `0x0044CE3E` executes for plant 10, or that the read causes
a visible outcome. Those are the discriminators for the next packet.

## Evidence-strength boundary

**Confirmed within the exact window:** No CPU read overlaps either plant 10
entry `+0x28` word after guarded final population, before scene-resource batch
return, or while execution proceeds to the retained no-input title.

**Confirmed across the packet sequence:** Every exact entry field currently
tied by static stores to `0x00448010` and its guarded plant caller has at least
one explicit bounded read-watchpoint window in M2.9-M2.14.

**Unknown:** Field meanings, post-title consumers, copied/derived state,
non-CPU use, later events, and any M1 placement/resource identity.
