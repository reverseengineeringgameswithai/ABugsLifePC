# M2 plant 10 entry +0x2E negative trace

## Scope and identity

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Runtime words: first entry `0x005AAB2E`, second entry `0x005AAB7E`
- Runtime evidence: `RUN-GDB-20260812-195759` in
  [[EXP-20260812-026 - Plant10 entry 2E bounded negative]]

No PS1 source or finding was consulted. Field descriptions remain exact
entry-relative offsets.

## Exact population boundary

Address-based function `0x00448010` makes `edx` point to selected runtime
entry `+0x20`, then populates several entry words. The following exact
instructions copy descriptor-relative data into runtime entry `+0x28` and
`+0x2E`, with two conditional changes to `+0x2E`:

```text
004480b4  lea edx,[ecx+ecx*4]
004480ba  shl edx,0x4
004480bd  add edx,0x5a9680
00448107  mov ax,WORD PTR [ecx+0x8]
0044810b  mov WORD PTR [edx+0x8],ax
0044810f  mov di,WORD PTR [ecx-0x22]
00448113  cmp di,0x9
00448117  mov WORD PTR [edx+0xe],di
0044811b  jne 0x00448133
0044812d  mov WORD PTR [edx+0xe],0xc
00448133  mov al,BYTE PTR [ecx+0x14]
00448136  and al,0x40
00448138  cmp al,0x40
0044813a  jne 0x00448141
0044813c  add WORD PTR [edx+0xe],0x2
```

Because `edx == 0x005A9680 + index * 0x50`, `[edx+0x0E]` is entry
`+0x2E`. The accepted run reproduces both exact plant 10 words as unsigned
`1` at unique post-call `0x0044596D` and the immediately following common
tail `0x00445B01`.

## Bounded runtime result

At `0x00445B01`, hardware read watchpoints were armed on both exact two-byte
ranges. Resource-batch return `0x004679C7` won with one hit while neither
watchpoint had a hit count. Both values remained 1.

After deleting only the return breakpoint, both watches remained enabled and
silent until an unattended Training title capture at
2026-08-12T19:59:55.729298233-04:00. At final debugger inspection, neither
watch had a hit count and both values remained unchanged. All hardware points
were deleted before detach.

## Static candidate context

Address-based function `0x00446970` contains the two previously identified
candidate reads. One compares selected entry `+0x2E` with 9 at `0x00446A8A`;
the other compares it with `0xA` at `0x00447661`. Each branch reads entry
`+0x0C` only after its comparison succeeds.

Neither comparison nor any other CPU instruction read the two exact plant 10
words in the retained runtime interval. This excludes those entries only for
the measured window. It does not establish that either branch is unreachable
for other entries or after the retained title endpoint.

## Renderer-preflight correction

One candidate arm was discarded because the opening selector had not received
the required Down input and the user observed that it remained on software.
The accepted run started fresh, used remote Down then Return, and was accepted
only after the complete log proved the 640x480x16 Direct3D path and contained
no `INITSOFTRENDER`. No result from the discarded arm is used here.

## Next exact surface

The same population block copies a descriptor word to runtime entry `+0x28`
at `0x0044810B`. Its exact plant 10 addresses are `0x005AAB28` and
`0x005AAB78`; both were zero in the accepted guarded snapshots. Earlier
packets already bound `+0x20`, combined `+0x24/+0x26`, and `+0x2E` ranges.
Watching only the two exact `+0x28` words is therefore the next narrow
statically populated surface without assigning field meaning.

## Evidence-strength boundary

**Confirmed within the exact window:** No CPU read overlaps either plant 10
entry `+0x2E` word after guarded final population, before scene-resource batch
return, or while execution proceeds to the retained no-input title.

**Inferred:** Neither static gate in `0x00446970` selects either exact plant 10
entry in the measured window, because the comparisons themselves would read
the watched words.

**Unknown:** Field meanings, later consumers, non-CPU use, later events, and
any M1 placement/resource identity.
