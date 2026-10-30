# M2 plant 10 entry-head +0x0C negative trace

## Scope and identity

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Runtime dwords: first entry `0x005AAB0C`, second entry `0x005AAB5C`
- Runtime evidence: `RUN-GDB-20260812-165837` in
  [[EXP-20260812-025 - Plant10 entry-head 0C bounded negative]]

No PS1 source or finding was consulted. Field descriptions remain exact
entry-relative offsets.

## Exact population boundary

Address-based function `0x00448010` copies descriptor `+0x0C` to runtime
entry `+0x0C`:

```text
004480d2  lea eax,[ecx-0x2e]
004480dc  lea edi,[edx-0x20]
004480ee  mov eax,DWORD PTR [eax+0xc]
004480f1  mov DWORD PTR [edi+0xc],eax
```

The guarded Training run reproduces both dwords as `0x00000001` at unique
plant 10 post-call `0x0044596D` and the immediately following common tail
`0x00445B01`.

## Bounded runtime result

At `0x00445B01`, hardware read watchpoints were armed on both exact dwords.
Resource-batch return `0x004679C7` won with one hit while neither watchpoint
had a hit count. Both values remained `0x00000001`.

After deleting only the return breakpoint, both watches remained enabled and
silent until an unattended Training title capture at
2026-08-12T17:00:57.008841846-04:00. At the final debugger inspection, neither
watch had a hit count and both values remained unchanged. All hardware points
were deleted before detach.

## Static candidate context

Both candidate reads are in address-based function `0x00446970`. The first
selects a `0x50`-byte entry through a signed word in the table rooted at
`0x005B17D8`, then gates the `+0x0C` read on entry word `+0x2E == 9`:

```text
00446a74  mov ecx,DWORD PTR [esp+0x24]
00446a78  movsx eax,WORD PTR [ecx]
00446a7b  lea eax,[eax+eax*4]
00446a7e  shl eax,0x4
00446a81  add eax,0x5a9660
00446a8a  cmp WORD PTR [eax+0x2e],0x9
00446a8f  je 0x00446a97
00446a97  mov ecx,DWORD PTR [eax+0xc]
00446a9a  mov WORD PTR [eax+0x2e],0xa
00446aa0  movsx edx,WORD PTR [ecx]
00446aa3  lea edx,[ecx+edx*8+0x4]
00446aa7  add ecx,0x4
00446aaa  mov DWORD PTR [esp+0x64],edx
00446aae  mov DWORD PTR [esp+0x1c],ecx
```

The second uses the same base/stride construction and gates its read on
entry word `+0x2E == 0xA`:

```text
0044764f  movsx eax,WORD PTR [ecx]
00447652  lea eax,[eax+eax*4]
00447655  shl eax,0x4
00447658  add eax,0x5a9660
00447661  cmp WORD PTR [eax+0x2e],0xa
00447666  jne 0x00447672
00447668  mov ecx,DWORD PTR [eax+0xc]
0044766b  add ecx,0x4
0044766e  mov DWORD PTR [esp+0x1c],ecx
```

Thus the static source is selected entry `+0x0C`; its immediate destination
is `ecx`, then pointer-derived locals at stack `+0x64/+0x1C`. The runtime
negative proves neither instruction nor any other CPU instruction read the
two exact plant 10 dwords in the retained window. It does not prove those
static branches are unreachable for other entries or later events.

## Next exact surface

The candidate branches independently read entry word `+0x2E` before deciding
whether to read `+0x0C`. Function `0x00448010` populates that word at
`0x00448117`, may replace value 9 with 12 at `0x0044812D`, and may add 2 at
`0x0044813C`. The exact plant 10 addresses are `0x005AAB2E` and
`0x005AAB7E`. Watching only those words is a narrower discriminator than
broadening to unrelated later fields.

## Evidence-strength boundary

**Confirmed within the exact window:** No CPU read overlaps either plant 10
entry `+0x0C` dword after guarded final population, before scene-resource
batch return, or while execution proceeds to the retained no-input title.

**Inferred:** The state-gating `+0x2E` words are the most direct next access
surface because both static `+0x0C` candidates read them first.

**Unknown:** The field meanings, first exact plant 10 reader after the title,
later entry fields, and any M1 placement/resource identity.
