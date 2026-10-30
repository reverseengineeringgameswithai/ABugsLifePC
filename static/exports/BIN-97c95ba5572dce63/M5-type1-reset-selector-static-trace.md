# M5 type-1 reset selector static trace

Binary SHA-256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`

Disassembly read directly from `work/copies/BUGS_PC-full-disc/bugs.exe`
(verified hash above) with radare2 5.9.8. Section mapping: `.text` file
`0x400` -> VA `0x00401000`, so `file = VA - 0x401000 + 0x400`.

## Loader pointer table (`0x0044BB70`)

Per top record, with `ecx` pointing at the record header and `esi = 0x3F`:

```
0x0044BC7F  mov  ax, word [ecx + 2]        ; type_id (int16)
0x0044BC83  cmp  ax, bx                    ; bx = 0
0x0044BC86  movsx edx, ax
0x0044BC89  jge  0x0044BCA9                ; nonnegative type
0x0044BC8B  shl  edx, 2                    ; negative type: edx = type * 4
0x0044BC8E  mov  eax, 0x005C5860
0x0044BC93  sub  eax, edx                  ; 0x005C5860 + |type| * 4
0x0044BC95  mov  dword [eax], ecx
...
0x0044BCA9  mov  dword [edx*4 + 0x005C5860], ecx
```

Confirmed consequences:

- type `N >= 0` occupies slot `0x005C5860 + N*4`; type 1 is `0x005C5864`;
- type `-N` **aliases into the same slot as `+N`**, although its element
  layout is the `0x10`-header/6-byte form advanced at
  `0x0044BC97-0x0044BCA3`, not the 12-byte row form;
- the walk overwrites, so the **last** record claiming a slot wins;
- advance strides: `0x3F` uses `4 + count*16` (`0x0044BCB9`), other
  nonnegative types `4 + count*12` (`0x0044BCC2`).

## Selector (`0x00432930`, file `0x031D30`)

```
0x00432930  mov  al, byte [0x0059D9A0]
0x00432938  test al, 0x10                  ; reset-request gate
0x0043293A  je   0x004329FF
0x00432940  mov  edx, dword [0x005C5864]   ; type-1 record pointer
0x00432946  xor  eax, eax
0x0043294A  mov  ax, word [edx]            ; row count, UNSIGNED word
0x0043294D  xor  edi, edi                  ; index = 0
0x00432953  mov  esi, 0x7FFFFFFF           ; best distance seed
0x00432958  mov  dword [esp + 0x14], eax   ; count
0x0043295C  jle  0x004329B0                ; count == 0 -> skip the loop
0x0043295E  mov  ecx, dword [0x0059D968]   ; aux Z
0x00432964  mov  ebx, dword [0x0059D960]   ; aux X
0x0043296A  sar  ecx, 5
0x0043296D  sar  ebx, 5
0x00432974  add  edx, 0xC                  ; row 0: X at [edx-8], Z at [edx]
0x0043297D  mov  ebp, dword [edx - 8]      ; row.x
0x00432982  sub  eax, ebp                  ; (auxX >> 5) - row.x
0x00432984  mov  ebp, dword [edx]          ; row.z
0x00432986  sar  eax, 3
0x00432989  sub  ecx, ebp                  ; (auxZ >> 5) - row.z
0x0043298D  sar  ecx, 3
0x00432990  imul ebp, eax                  ; dx * dx   (32-bit, wraps)
0x00432995  imul eax, ecx                  ; dz * dz   (32-bit, wraps)
0x00432998  add  eax, ebp                  ; wraps
0x0043299A  cmp  eax, esi
0x0043299C  jge  0x004329A4                ; strictly smaller wins -> first index wins ties
0x0043299E  mov  esi, eax
0x004329A0  mov  dword [esp + 0x18], edi   ; best index
0x004329AE  jl   0x00432979                ; while ++index < count
0x004329B0  mov  eax, dword [esp + 0x18]   ; best index
0x004329B4  mov  ecx, dword [0x005C5864]
0x004329BA  push 0x0059D960                ; &aux triple
0x004329C2  mov  edx, dword [ecx + edx*4 + 4]  ; row.x at record + 12*i + 4
0x004329C6  shl  edx, 5
0x004329CA  mov  dword [0x0059D960], edx
0x004329D3  mov  ecx, dword [ecx + eax*4]      ; row.z at record + 12*i + 12
0x004329D6  mov  dword [0x0059D964], 0x7FFFFFFF   ; query sentinel Y
0x004329E0  shl  ecx, 5
0x004329E3  mov  dword [0x0059D968], ecx
0x004329E9  call 0x00401659                ; -> 0x004AC460 terrain height
0x004329F1  sub  eax, 0x100
0x004329F6  mov  dword [0x0059D964], eax
```

Row layout: header word at `record + 0`; row `i` occupies
`record + 4 + 12*i` with X at `+0`, an unread middle dword at `+4`, and Z at
`+8`.

### Uninitialised index on a zero count

`0x0043295C` skips the loop when the count is zero, and `0x004329B0` then
reads local `[esp + 0x18]`, which is written only inside the loop at
`0x004329A0`. The prologue is `sub esp, 0xC` plus four pushes, so that local
lies in the uninitialised frame area. With a zero-count type-1 record the
original indexes the record with stale stack data. The reimplementation
refuses this case instead of reproducing it.

### The `0x7FFFFFFF` seed is always beaten

Two squares sum to 0, 1 or 2 modulo 4; truncation by `2**32` preserves that
residue and nothing can exceed `0x7FFFFFFF` after truncation, while
`0x7FFFFFFF` is 3 modulo 4. Any non-empty row list therefore selects a row.

## Second variant (`0x00437A20`, file `0x036E20`)

Bytes `0x00432930-0x004329E8` and `0x00437A20-0x00437AD8` are identical
(185 bytes compared directly in the file), both `call`s resolve to
`0x00401659`, and the tails `0x004329EE-0x004329FE` /
`0x00437ADE-0x00437AEE` are identical. Only `0x00432930`'s shared exit adds
`mov edx,[0x0059EFE4]; mov [0x0059EFE8],edx`. `0x0042DDB0` dispatches between
them on `0x00861C84`, so the modelled selection is variant-independent.

## Terrain height return path

`0x00401659` is a jump thunk to `0x004AC460`. `0x004AC695-0x004AC69A` calls
`0x00401717` (-> `0x004ACA60`) with the query block, and `0x004AC6B8` returns
`dword [esp + 0x24]`, i.e. the block's Y field. `0x004ACD41` stores
`height + 0xC80` on success; `0x004ACDB2` stores `0x80000000` when no plane
is found. The selector's `sub eax, 0x100` therefore yields `0x7FFFFF00` for a
failed query.

## Pointer-table clear (added by the M5.2 audit)

Level-load entry `0x004671D0` ends its prologue with:

```
0x00467207  mov  ecx, 0x40                 ; 64 dwords
0x0046720C  xor  eax, eax
0x0046720E  mov  edi, 0x005C5860           ; pointer-table root
0x00467213  xor  esi, esi
0x00467215  rep  stosd
```

This zeroes the whole type-indexed pointer table. A second, apparently
unreferenced copy of the same sequence is at `0x00464F31-0x00464F3D`.
Consequence: for a level whose data carries no type-1 record, the slot is not
simply left holding the previous level's pointer. Whether the clear runs on
every load is undetermined offline and is recorded as `KU-064`.

An additional live reader of slot `0x005C5864` exists at `0x00436D25`
(unsigned count read plus `lea [edx+edx*2]` row indexing), beyond the
consumers listed above.
