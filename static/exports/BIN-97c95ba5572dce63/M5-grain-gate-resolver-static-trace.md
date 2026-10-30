# M5 grain-gate opening resolver static trace

Binary SHA-256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`

This trace was re-derived with radare2 from the permitted exact-hash work copy
`work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe`. No game, Wine, Gamescope, or
debugger ran; no target or game file was written; `originals/` and the external
PS1 tree were not accessed. `.text` addresses use the established relation
`file = VA - 0x00400C00`.

## Shared signed proximity arithmetic

City helper `0x00416580` (file `0x00015980`) reads X at `+0` and Z at `+8`
from both coordinate blocks:

```text
0x00416590  sub eax, esi          ; X difference, low 32 bits
0x00416595  sar eax, 8
0x00416598  sub ecx, esi          ; Z difference, low 32 bits
0x0041659C  sar ecx, 8
0x0041659F  imul edx, eax         ; low 32 bits
0x004165A5  imul eax, ecx         ; low 32 bits
0x004165A8  add edx, eax          ; low 32 bits
0x004165B0  imul ecx, eax         ; radius squared, low 32 bits
0x004165B5  cmp edx, ecx
0x004165B7  setl al               ; signed distance² < signed radius²
```

The Tunnels opening arm duplicates the same wrapping `sub`, arithmetic
`sar 8`, two wrapping products, wrapping sum, and signed comparison at
`0x00432F33-0x00432F4F`, using fixed squared threshold `0x2710` (100²).

## Tunnels ordered nine-row loop

The loop starts with `esi = 0` at `0x00432EEA`; each record occupies five
dwords / 20 bytes at `0x004DA9C8`; `esi += 5` at `0x0043303D`; and the loop
ends when `esi == 0x2D` at `0x00433040-0x00433043`.

```text
0x00432EF1  mov eax, [esi*4 + 0x004DA9C8] ; type +0x00
0x00432EF8  cmp eax, 0x10C7                ; only closed type qualifies
0x00432F03  mov eax, [esi*4 + 0x004DA9D0] ; requirement +0x08
0x00432F0C  mov cl, [0x0059D9B1]           ; unsigned grain byte
0x00432F12  cmp ecx, eax
0x00432F14  jl 0x00432FB0                  ; signed insufficient refusal first
0x00432F1A  mov eax, [0x0059D910]          ; Flik X
0x00432F26  mov ecx, [0x0059D918]          ; Flik Z
0x00432F49  cmp edx, 0x2710
0x00432F4F  jge 0x0043303D                 ; signed outside refusal
0x00432F6A  mov [esi*4 + 0x004DA9C8], edi  ; type = 0x1068
```

The direct write order inside a qualifying row is the row's own type first,
then any coupling:

```text
0x00432F7F  cmp esi, ebp                    ; ebp = 0, row 0
0x00432F85  mov [0x004DAA18], edi           ; row 0 -> row 4 type
0x00432F93  cmp esi, 0x14                   ; row 4 dword index
0x00432F9D  mov [0x004DA9C8], edi           ; row 4 -> row 0 type
```

Therefore row-0 coupling is visible to row 4's later visit in the same pass;
row-4 coupling occurs after row 0 was already visited. The resolver applies
only those direct writes to its private state copy. It reports, but does not
execute, the downstream rule at `0x00433017-0x00433024`: if the signed type is
greater than `0x708`, add `-140` with 32-bit wrapping and write it back. This
rule explains `0x1068 -> 0x0690` after 18 eligible decrements.

## City Entrance one-call transition

Routine `0x00433790` (file `0x00032B90`) evaluates state, then proximity, then
grain:

```text
0x00433798  cmp dword [esi*4 + 0x0059F020], -1
0x004337A0  jne 0x0043383B                 ; already non-closed
0x004337C5  call 0x00401A37                ; thunk -> 0x00416580
0x004337CD  test eax, eax
0x004337CF  je 0x0043383B                  ; outside before grain
0x004337D6  mov dl, [0x0059D9B1]           ; unsigned grain byte
0x004337E1  cmp edx, ecx
0x004337E3  jl 0x00433810                  ; insufficient
0x004337EF  mov dword [esi*4 + 0x0059F020], 0x20
0x00433803  test esi, esi
0x00433807  mov byte [0x00599C69], 1       ; index 0 only; semantics Unknown
```

After the opening branch rejoins at `0x0043383B`, positive state is decremented
at `0x0043384A-0x0043384B` and call-site deltas are added with wrapping to
slot A at `0x0043385C-0x00433865` and slot B at
`0x00433870-0x00433879`. Thus the first of 32 downstream steps occurs in the
same call that wrote `0x20`; the direct opening write is still separately
addressable from the downstream rule.

The three direct call sites at `0x0043392F-0x0043397F` supply:

| Index | Center X/Z | Radius | Slot A / delta | Slot B / delta |
| ---: | --- | ---: | --- | --- |
| 0 | `(-71129,-184314)` | 80 | `2 / -32` | `3 / +32` |
| 1 | `(354031,35256)` | 90 | `4 / +44` | `5 / -34` |
| 2 | `(582271,310212)` | 100 | `0 / -28` | `1 / +32` |

At 32 steps these yield accepted zero-based terminal deltas
`(-1024,+1024)`, `(+1408,-1088)`, and `(-896,+1024)` respectively
(EXP-20260815-137/138 and EXP-20260816-148/149).

## Evidence boundary

The trace covers the twelve admitted Tunnels/City mechanisms only. EXP-146's
22-reference census is direct/static evidence and does not prove the absence
of address-computed, aliased, or cached grain consumers. Calls inside the
opening branches, message/audio work, rendering, controller reachability,
persistence, semantic meaning of `0x00599C69`, and unrelated update logic are
outside this trace and the resolver.
