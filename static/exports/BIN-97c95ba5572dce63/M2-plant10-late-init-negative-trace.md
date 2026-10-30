# M2 plant 10 late-initialization negative trace

## Scope and identity

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Static anchors: `0x0044596D`, `0x00445B01`, `0x004679C2`, and
  `0x004679C7`
- Runtime evidence: `RUN-GDB-20260812-161520` in
  [[EXP-20260812-023 - Plant10 late-initialization pointer-surface negative]]

No PS1 source or finding was consulted. All field descriptions remain exact
entry-relative offsets.

## Why the plant-specific guard is required

`0x00445B01` is the common tail of the resource-ID loop in `0x00445020`:

```text
00445626  mov eax,DWORD PTR [eax]
00445628  dec eax
00445629  cmp eax,0xd
0044562c  ja 0x00445b01
00445632  jmp DWORD PTR [eax*4+0x445c44]
...
00445b01  mov ecx,DWORD PTR [edi+0x4]
00445b04  add edi,0x4
00445b07  test ecx,ecx
00445b09  mov eax,edi
00445b0b  jge 0x00445626
```

Consequently an unguarded breakpoint there can stop after an earlier resource
ID. That occurred in `RUN-GDB-20260812-161520`: all plant 10 destinations were
zero. The later reported stop at `0x00448107` followed exact population writes
at `0x004480FB` and `0x00448103`, so that entire pre-plant interval is rejected
as initialization rather than treated as a consumer read.

The accepted boundary first stops at the unique plant 10 post-call address
`0x0044596D`, verifies resource ID `0x71` and indices `66/68`, then accepts only
the immediately following `0x00445B01`. This binds the start to the caller
adjustment at `0x00445988`/`0x00445AFA` and reproduced dword
`0xD7E00218`.

## First accepted boundary

The caller of the resource batch has an exact static return boundary:

```text
004679b2  lea edx,[esp+0x14]
004679b6  lea eax,[esp+0x18]
004679ba  push edx
004679bb  push eax
004679c2  call 0x00401ca8
004679c7  add esp,0x8
```

Prior static evidence resolves thunk `0x00401CA8` to `0x00445020`. The
hardware breakpoint at `0x004679C7` therefore bounds return from the complete
scene-resource batch. It won while the three exact read watchpoints remained
enabled with no hits and unchanged values.

## Natural-title boundary

After deleting only the return breakpoint, the same three watches remained
active until an ignored native capture proved the natural Training title
pause. None fired; the exact source dwords and two adjusted halfwords remained
unchanged. Combined with `EXP-20260812-022`, the accepted runtime evidence now
covers the exact three source ranges from plant-10-specific caller-adjustment
completion through the title and a later 71.708-second gameplay interval.

## Next statically evidenced surface

The `.ALL` consumer copies four exact descriptor dwords into the entry head
before writing entry-relative `+0x20`:

```text
004480df  mov DWORD PTR [edx-0x20],ebx
004480e5  mov DWORD PTR [edi+0x4],ebx
004480eb  mov DWORD PTR [edi+0x8],ebx
004480f1  mov DWORD PTR [edi+0xc],eax
004480f6  mov DWORD PTR [edx],eax
```

Here `edi == edx - 0x20`, so these are exact entry offsets `+0x00`, `+0x04`,
`+0x08`, and `+0x0C`. They are the narrowest statically evidenced expansion
after the three pointer-surface negatives. Their meanings remain unknown.

## Evidence-strength boundary

**Confirmed within the exact boundaries:** No CPU read overlaps the two plant
10 entry `+0x20` dwords or the adjusted first-entry `+0x24/+0x26` dword after
the plant-specific `0x00445B01`, through resource-batch return
`0x004679C7`, or before the natural title pause.

**Inferred:** A bridge to behavior is more likely to use another entry field
than a late copy of the three tested ranges. This is a prioritization inference,
not an unused-field claim.

**Unknown:** The first downstream readers and meanings of entry-head offsets
`+0x00/+0x04/+0x08/+0x0C`, other entry fields, and any M1 placement/resource
identity.
