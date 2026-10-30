# M2 plant 10 post-title selected-entry negative trace

## Scope and identity

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Runtime words: first entry `0x005AAB2E`, second entry `0x005AAB7E`
- Accepted runtime evidence: `RUN-GDB-20260812-203714`,
  `RUN-GDB-20260812-203820`, and `RUN-GDB-20260812-203930` in
  [[EXP-20260812-028 - Plant10 post-title selected-entry negative]]

No PS1 source or finding was consulted. Field and function descriptions remain
address-based. Exploratory runs `RUN-GDB-20260812-204252/204333` are retained
for an instrumentation contradiction and are not part of the accepted
runtime result.

## Exact candidate selection

```text
0044ce0d  movsx ecx,WORD PTR [edi-0x08]
0044ce11  mov eax,DWORD PTR [ecx*4+0x005b1a7c]
0044ce18  movsx ecx,WORD PTR [eax+0x04]
0044ce1c  movsx edx,WORD PTR [eax+0x06]
0044ce20  lea esi,[ecx+ecx*4]
0044ce27  shl esi,0x04
0044ce2a  add esi,0x005a9660
0044ce30  cmp ecx,edx
0044ce32  jge 0x0044d1f3
0044ce3e  movsx eax,WORD PTR [esi+0x2e]
```

The source-record-relative signed word selects a pointer from table
`0x005B1A7C`; header words `+0x04/+0x06` bound a 0x50-byte entry range. Plant
10's exact slot is `0x005B1AA4`, whose measured pointer/header are
`0x006C342B` and `66/68`. This makes `0x005AAB2E/0x005AAB7E` exact candidate
reads only if a source record supplies selector 10.

## Exact branch and first value-1 call

```text
0044ce3e  movsx eax,WORD PTR [esi+0x2e]
0044ce42  dec eax
0044ce43  je 0x0044cfc4
0044ce49  dec eax
0044ce4a  je 0x0044cfab
0044ce50  dec eax
0044ce51  jne 0x0044d1d0
0044ce57  ...                         ; original value 3 path
0044cfc4  ...                         ; original value 1 path
0044d079  call 0x004012c6
004012c6  jmp 0x00463770
```

For original value 1, the first call in that branch is
`0x0044D079 -> 0x004012C6 -> 0x00463770`. Exact `0x00463770` copies dwords
from second argument offsets `+0x00/+0x04/+0x08` to first argument offsets
`+0x14/+0x18/+0x1C`. The accepted runtime windows do not establish that this
branch executes for plant 10.

## Accepted bounded runtime result

- `RUN-GDB-20260812-203714`: both exact two-byte read watches installed at the
  natural Training title; `NextLife` wins after 11.518815 seconds with zero
  stops; both watches deleted and detach verified.
- `RUN-GDB-20260812-203820`: both watches retained for a separate 30.026628-
  second no-input post-`NextLife` window; zero stops; cleanup and detach
  verified.
- `RUN-GDB-20260812-203930`: exact hardware breakpoint `0x0044CE3E` retained
  for 10.014330 seconds; zero stops; cleanup and detach verified.

Therefore no accepted access overlaps either exact plant 10 `+0x2E` word
from title through `NextLife` or in the additional elapsed arm, and the exact
candidate reader itself is inactive in its separate no-input control window.
This is not a lifetime absence result.

## Caller gate and rejected exploratory continuation

```text
0044d78f  mov al,BYTE PTR [0x005c5edc]
0044d794  mov ecx,DWORD PTR [0x005ba80c]
0044d79a  test al,0x10
0044d79c  mov DWORD PTR [0x005b56d0],ecx
0044d7a2  jne 0x0044d7a9
0044d7a4  call 0x0040100a
0040100a  jmp 0x0044ca00
```

Exploratory `RUN-GDB-20260812-204252` records one gate stop with `AL` and
`[0x005C5EDC]` equal to `0x40`. Static evaluation would leave the `jne`
untaken. However, ignored raw GDB output then records `SIGSEGV` at
`0x0044D79A`, while the structured result still reports cleanup/detach; Wine
later prints the matching unhandled read fault. The instruction has no memory
operand, and the paired later arm does not supply an accepted continuation.
Those runs cannot establish that the call or callee completed.

## Evidence-strength boundary

**Confirmed within accepted windows:** no access to either exact plant 10
`+0x2E` word through the first title transition and stated elapsed arm; exact
reader `0x0044CE3E` inactive in its stated control interval.

**Static only:** selector/header arithmetic, the value 1/2/3 branch chain, the
first value-1 call, and outer caller gate control flow.

**Unknown:** a live selector-10 source record, event trigger, accepted outer
gate-to-callee continuation, field meanings, and any visible or M1 placement
effect.
