# PC input subsystem static census

## Scope and evidence boundary

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Work copy read: `work/copies/BUGS_PC-full-disc/bugs.exe` (hash re-verified
  before analysis).
- Tools: GNU objdump 2.46 (`-d -M intel`), `rabin2` 5.9.8 for imports, and
  direct little-endian byte decoding of the same file.
- Offline only. No process was launched, no debugger attached, no target memory
  written, no `originals/` path opened, no PS1 source consulted, and no game
  asset was read.

Section-to-file mapping used throughout (from `objdump -h`):

| Section | VMA | Size | File offset |
|---|---|---|---|
| `.text` | `0x00401000` | `0x000BE765` | `0x000400` |
| `.rdata` | `0x004C0000` | `0x00000E88` | `0x0BEC00` |
| `.data` | `0x004C1000` | `0x0002C400` | `0x0BFC00` |

`.data`'s raw content ends at `0x004ED400`. Addresses between that and the
next section with file content (`.idata` at `0x00864000`) are `.bss`-class and
are named by address only; the lowest such address this document cites is
`0x004F0440`. `0x0086478C` in §5 is an `.idata` IAT slot, and no file bytes are
decoded at any address above `0x004ED400`.

This census claims **no** runtime behaviour and assigns no gameplay meaning to
any action bit. Where a DirectInput identifier is named, that name is derived
by comparing the bytes against the documented value, and the comparison is
shown.

## 0. Relation to earlier work

Grepped across **every** file in `static/exports/BIN-97c95ba5572dce63/`, plus
the Vault, for each principal address of this subsystem.

**Prior art, authored:**

- `SUBSYS-audio-static-census.md` records that `0x0042BA60` brings up
  DirectSound and, at `0x0042BAED`, calls `0x0042F350`. `EXP-20260816-159`
  words that fact as "the function `0x0042F350` that holds the executable's
  only `DirectInputCreateA` call site (`0x0042F43D`)"; the export itself says
  "which is the function containing the sole `DirectInputCreateA` call site at
  `0x0042F43D`". That is the anchor the Input coverage row already carried.
  This census confirms the "sole" part: `0x0042F43D` is the only call to the
  import thunk `0x004AFEA8` in the image.
- [[PC autonomous game control]] records the second input path in full: "The
  renderer chooser and menus read input with `GetAsyncKeyState`", "The menus
  poll `GetAsyncKeyState`", and "(chooser at `0x004A7600`, import loaded at
  `0x004A7841`)", together with the ~180 ms hold finding.
  [[EXP-20260816-145 - Independent runtime gate mapping audit]] names that
  chooser `SwitchDriverScreen` at `0x004A7600`. §5 below is **restatement** of
  that, not a new result.

**Prior art, generated:** `ghidra-evidence.json` contains decompilations that
mention every **principal** address used here (not every intra-function
instruction address the sections below cite), including `FUN_0042f350`, `FUN_0042ebc0`,
`0x00598A10`, `0x00598B10`, `0x004C0230`, `0x004AFE90`, `0x004D8490` and
`0x005988D0`. As with the creature census, the addresses were latent in that
generated artifact; per [[Agent Operating Manual]] decompiler output is
evidence, not a stated claim.

**No authored Vault note or markdown export mentions any of:** `0x0042EBC0`,
`0x0042F0F0`, `0x00598A10`, `0x00598B10`, `0x005988D0`, `0x004D8430`,
`0x004C0230`, `0x004C0220`, `0x004AFE90` or `0x004AEE70`.

What is new here is therefore the **authored, verified model**: which device
objects are created and with which GUIDs, which data formats and cooperative
levels are set, where per-frame state is read, the default key binding table
and its runtime origin, and the fact that the two input paths are disjoint.

## 1. DirectInput bring-up — `0x0042F350`

**Extent:** `0x0042F350`-`0x0042F565` (file `0x02E750`-`0x02E965`). One `ret`,
at `0x0042F565`; `nop` then `int3` padding follows to the next function at
`0x0042F600`. Only two branch targets leave the range — `0x004016AE` (§3) and
`0x004AFEA8`, the `DirectInputCreateA` import thunk.

Reached from `0x0042BAED` in `0x0042BA60`, i.e. brought up as a sibling of
DirectSound (prior art, §0).

### 1.1 Object creation

```text
42f392: a1 30 f7 59 00    mov  eax,ds:0x59f730     ; hInstance
42f397: 68 18 8b 59 00    push 0x598b18            ; &ppDI
42f39c: be 01 00 00 00    mov  esi,0x1             ; used as a flag below
42f3a1: 68 00 05 00 00    push 0x500               ; DIRECTINPUT_VERSION
42f3a6: 50                push eax
...
42f43d: e8 66 0a 08 00    call 0x4afea8            ; DirectInputCreateA
42f442: 85 c0             test eax,eax
42f444: 0f 85 14 01 00 00 jne  0x42f55e            ; bail on failure
```

The version constant is `0x0500`. The object pointer lands in `0x00598B18`.

### 1.2 Keyboard device

```text
42f44a: a1 18 8b 59 00    mov  eax,ds:0x598b18
42f44f: 57                push edi                 ; edi = 0 (pUnkOuter)
42f450: 68 20 8b 59 00    push 0x598b20            ; &device
42f455: 68 30 02 4c 00    push 0x4c0230            ; rguid
42f45a: 8b 08             mov  ecx,DWORD PTR [eax]
42f45c: 50                push eax
42f45d: ff 51 0c          call DWORD PTR [ecx+0xc] ; CreateDevice
```

then, each result-checked and each bailing to `0x0042F4A5` on failure:

| Site | vtable | Method | Argument |
|---|---|---|---|
| `0x0042F471` | `+0x2C` | `SetDataFormat` | `0x004AFE90` |
| `0x0042F489` | `+0x34` | `SetCooperativeLevel` | `hwnd = [0x0059F73C]`, flags `6` |
| `0x0042F498` | `+0x1C` | `Acquire` | — |

On the fully successful path `0x0042F49F` sets `[0x00598BC8] = 1`.

Flags `6` is `DISCL_NONEXCLUSIVE | DISCL_FOREGROUND` (`2 | 4`). The window
handle `0x0059F73C` is the same global the audio census recorded for the
DirectSound cooperative level.

### 1.3 Identifier verification

Decoded from the file bytes and compared against the documented values:

| Address | Bytes decode to | Documented as |
|---|---|---|
| `0x004C0230` (file `0x0BEE30`) | `{6F1D2B61-D5A0-11CF-BFC7-444553540000}` | `GUID_SysKeyboard` |
| `0x004C0220` (file `0x0BEE20`) | `{5944E682-C92E-11CF-BFC7-444553540000}` | `IID_IDirectInputDevice2A` |

The two `DIDATAFORMAT` structures decode as:

| Address | dwSize | dwObjSize | dwFlags | dwDataSize | dwNumObjs | Documented as |
|---|---:|---:|---|---:|---:|---|
| `0x004AFE90` (file `0x0AF290`) | 24 | 16 | `0x2` (`DIDF_RELAXIS`) | 256 | 256 | `c_dfDIKeyboard` |
| `0x004AEE70` (file `0x0AE270`) | 24 | 16 | `0x1` (`DIDF_ABSAXIS`) | 80 | 44 | `c_dfDIJoystick` |

`dwDataSize` 256 with 256 objects is the keyboard scancode array;
`dwDataSize` 80 is `sizeof(DIJOYSTATE)`. Both agree with the buffer sizes the
consumers actually pass (§2).

### 1.4 Joystick enumeration and devices

```text
42f4a5: a1 18 8b 59 00    mov  eax,ds:0x598b18
42f4aa: 56                push esi                 ; esi = 1  (DIEDFL_ATTACHEDONLY)
42f4ab: 68 d0 87 59 00    push 0x5987d0            ; pvRef
42f4b0: 68 79 19 40 00    push 0x401979            ; lpCallback (thunk)
42f4b5: 8b 10             mov  edx,DWORD PTR [eax]
42f4b7: 6a 04             push 0x4                 ; dwDevType = DIDEVTYPE_JOYSTICK
42f4b9: 50                push eax
42f4ba: ff 52 10          call DWORD PTR [edx+0x10] ; EnumDevices
```

The loop at `0x0042F4C5`-`0x0042F551` then runs `edi` from `0` while
`edi < [0x00598B14]`, with `ebx` stepping `0x005987D0` by `0x10` and `ebp`
stepping `0x00598B28` by `4`. Per device:

| Site | vtable | Method | Argument |
|---|---|---|---|
| `0x0042F4EB` | `+0x0C` | `CreateDevice` | `rguid = ebx` (enumerated GUID), out to a stack slot |
| `0x0042F504` | `+0x00` | `QueryInterface` | `0x004C0220`, out to `0x005988D0 + edi*4` |
| `0x0042F514` | `+0x2C` | `SetDataFormat` | `0x004AEE70` |
| `0x0042F529` | `+0x34` | `SetCooperativeLevel` | `hwnd = [0x0059F73C]`, flags `5` |
| `0x0042F535` | `+0x1C` | `Acquire` | — |

On full success `0x0042F53C` sets `[ebp] = 1`, i.e.
`[0x00598B28 + edi*4] = 1`.

Flags `5` is `DISCL_EXCLUSIVE | DISCL_FOREGROUND` (`1 | 4`) — a **different**
cooperative level from the keyboard's `6`. The `QueryInterface` to
`IID_IDirectInputDevice2A` is what makes `Poll` available; §2.3 uses it.

`0x0042F558` sets `[0x00598B1C] = 1` when the enumeration path completes.

### 1.5 Global map established by §1

| Address | Role as shown by the instructions |
|---|---|
| `0x0059F730` | `hInstance` passed to `DirectInputCreateA` |
| `0x0059F73C` | window handle passed to both `SetCooperativeLevel` calls |
| `0x00598B18` | the `IDirectInputA` object |
| `0x00598B20` | the keyboard device |
| `0x00598BC8` | set to 1 only on the fully successful keyboard path |
| `0x00598B1C` | set to 1 only after the enumeration path completes |
| `0x005987D0` | enumerated joystick GUIDs, `0x10` stride |
| `0x00598B14` | joystick count; zeroed at `0x0042F437`, written by the enumeration callback, and read as the device loop's bound at `0x0042F4C5` and `0x0042F543` |
| `0x005988D0` | `IDirectInputDevice2A` pointers, `4` stride |
| `0x00598B28` | per-joystick acquired flags, `4` stride |

## 2. Per-frame read — `0x0042EBC0`

**Extent:** code `0x0042EBC0`-`0x0042EEBB` (file `0x02DFC0`-`0x02E2BB`), one
`ret` at `0x0042EEBB`, followed by its own jump table at `0x0042EEBC` and byte
table at `0x0042EED0` (§2.2), then `nop` padding from `0x0042EF41`. Every
target in that jump table lies inside the code range, so nothing after the
`ret` is separately entered.

Reached only through thunk `0x00401B5E`, whose call sites are `0x00464E1C`
and `0x0049BDB7`. Their enclosing functions were not analysed.

Entry gates on `[0x00598BC8]` (the keyboard-ready flag of §1.2) and zeroes the
output words `0x00598B10`, `0x00598B12`, `0x00598BC0`, `0x00598BC2`,
`0x00598BC4`, `0x00598BC6` and `0x00598B5C`.

### 2.1 Keyboard state

```text
42ec04: 57                push edi                 ; edi = 0
42ec05: 6a 40             push 0x40                ; 0x40 dwords = 256 bytes
42ec07: 68 10 8a 59 00    push 0x598a10
42ec0c: e8 49 2e fd ff    call 0x401a5a            ; clear the buffer
42ec11: a1 20 8b 59 00    mov  eax,ds:0x598b20
...
42ec1c: ff 51 1c          call DWORD PTR [ecx+0x1c] ; Acquire
42ec1f: a1 20 8b 59 00    mov  eax,ds:0x598b20
42ec24: 68 10 8a 59 00    push 0x598a10            ; buffer
42ec29: 68 00 01 00 00    push 0x100               ; 256 bytes
42ec2e: 50                push eax
42ec2f: 8b 10             mov  edx,DWORD PTR [eax]
42ec31: ff 52 24          call DWORD PTR [edx+0x24] ; GetDeviceState
```

So **`0x00598A10` is the 256-byte DirectInput keyboard state buffer**, and an
individual key is `0x00598A10 + scancode`. The `0x100` here matches the
`dwDataSize` of `0x004AFE90` in §1.3.

Three right-hand modifiers are then folded onto their left-hand equivalents —
each reads one byte and, if non-zero, stores `1` into another:

| Read | scancode | Store | scancode |
|---|---|---|---|
| `0x00598A46` | `0x36` `DIK_RSHIFT` | `0x00598A3A` | `0x2A` `DIK_LSHIFT` |
| `0x00598AAD` | `0x9D` `DIK_RCONTROL` | `0x00598A2D` | `0x1D` `DIK_LCONTROL` |
| `0x00598AC8` | `0xB8` `DIK_RMENU` | `0x00598A48` | `0x38` `DIK_LMENU` |

Consequently only the left-hand scancodes need appear in the binding table of
§3, and they are the ones that do.

### 2.2 Binding walk and direction synthesis

```text
42ec86: b8 34 84 4d 00    mov  eax,0x4d8434
42ec8b: 8b 48 fc          mov  ecx,DWORD PTR [eax-0x4]   ; scancode
42ec8e: 8a 99 10 8a 59 00 mov  bl,BYTE PTR [ecx+0x598a10] ; key state
42ec94: 84 db             test bl,bl
42ec96: 74 3f             je   0x42ecd7
42ec98: 8b 08             mov  ecx,DWORD PTR [eax]
42ec9a: 66 0b 30          or   si,WORD PTR [eax]         ; accumulate mask
42ec9d: 83 c1 f0          add  ecx,0xfffffff0
...
42ecd7: 83 c0 08          add  eax,0x8
42ecda: 3d 94 84 4d 00    cmp  eax,0x4d8494
42ecdf: 7c aa             jl   0x42ec8b
```

Twelve iterations: `eax` takes `0x004D8434`, `0x004D843C`, … `0x004D848C`, so
the table entries are 8 bytes each — a scancode dword followed by a mask
dword — spanning `[0x004D8430, 0x004D8490)`. The accumulated mask is stored to
**`0x00598B10`** at `0x0042ECE3`.

`DIK_TAB` is handled separately before the loop, at
`0x0042EC68`-`0x0042EC7F`: it reads `0x00598A1F` (`0x0F`) and ORs the mask at
`0x004D8474` — the same slot the loop's entry 8 uses.

Masks in the range `[0x10, 0x80]` additionally steer a switch:
`ecx = mask - 0x10`, bounded by `cmp ecx,0x70 / ja`, then a byte table at
`0x0042EED0` selects one of five arms through the jump table at `0x0042EEBC`.
Decoded from the bytes:

| Byte-table index (`mask - 0x10`) | Case | Arm | Effect |
|---:|---:|---|---|
| `0x00` | 0 | `0x0042ECB9` | `edx += 0x8000` |
| `0x10` | 1 | `0x0042ECD1` | `ebp += 0x8000` |
| `0x30` | 2 | `0x0042ECC1` | `edx -= 0x8000` |
| `0x70` | 3 | `0x0042ECC9` | `ebp -= 0x8000` |
| the remaining 0x6D of the table's 0x71 indices | 4 | `0x0042ECD7` | loop continue |

With the §3 masks that resolves to `UP → +edx`, `RIGHT → +ebp`,
`DOWN → -edx`, `LEFT → -ebp`, and only those four: every other mask in §3 is
outside `[0x10, 0x80]` and fails the `ja`.

The axis store at `0x0042ECEC`-`0x0042ECF2` is **not** gated on a direction
having fired. Its guard is `edi`, set to `1` at `0x0042ECA0` for *any* pressed
binding entry, before the `[0x10, 0x80]` bound check. So pressing a
non-direction binding alone still writes `ebp` to `0x004F0440` and `edx` to
`0x004F0444`, with both at their initial values.

The engine therefore synthesises a two-axis `±0x8000` value from the digital
direction keys. What consumes `0x004F0440`/`0x004F0444` was not traced.

### 2.3 Joystick state

Gated on `[0x00598B28]` (joystick 0's acquired flag) at `0x0042ECFA`:

| Site | vtable | Method | Argument |
|---|---|---|---|
| `0x0042ED0E` | `+0x64` | `Poll` | — |
| `0x0042ED1D` | `+0x1C` | `Acquire` | on `Poll` failure |
| `0x0042ED2F` | `+0x24` | `GetDeviceState` | `0x50` bytes into `0x00598B60` |
| `0x0042ED3E` | `+0x1C` | `Acquire` | on `GetDeviceState` failure |

`+0x64` is `Poll`, which exists only on `IDirectInputDevice2A` — the interface
§1.4 queried for. The `0x50` matches `c_dfDIJoystick`'s `dwDataSize` in §1.3,
so `0x00598B60` is a `DIJOYSTATE`. A second accumulator is ORed from
`[esi*8+0x004D8434]` at `0x0042EE9D`, i.e. the same table §2.2 walks.

The button contribution is a separate eight-iteration loop at
`0x0042ED6F`-`0x0042ED8C`, quoted in §4, which walks the joystick pair table
and tests `DIJOYSTATE.rgbButtons` with each pair's first column.

## 3. The binding table is written at runtime, not stored

`[0x004D8430, 0x004D8490)` is **all zero in the file image** (file
`0x0D7030`-`0x0D7090`). It is filled by `0x0042F0F0`, which is reached only
through thunk `0x004016AE`. That thunk has **two** call sites: `0x0042F37D`,
inside the bring-up of §1, and `0x004310D0`, whose enclosing function was not
analysed. So the defaults are (re)applied from two places, not one.
`0x0042F0F0` also fills `0x005988E0` with `0xFFFFFFFF` for `0x40` dwords
before writing the table.

The twelve pairs it writes, listed in **address** order (the store order
differs: `0x004D8468`/`0x004D846C` are written at `0x0042F178`/`0x0042F182`,
before `0x004D8460`/`0x004D8464` at `0x0042F18C`/`0x0042F196`):

| Slot | scancode | DIK name | mask |
|---|---|---|---|
| `0x004D8430` | `0xC8` | `DIK_UP` | `0x0010` |
| `0x004D8438` | `0xD0` | `DIK_DOWN` | `0x0040` |
| `0x004D8440` | `0xCB` | `DIK_LEFT` | `0x0080` |
| `0x004D8448` | `0xCD` | `DIK_RIGHT` | `0x0020` |
| `0x004D8450` | `0x1D` | `DIK_LCONTROL` | `0x8000` |
| `0x004D8458` | `0x2A` | `DIK_LSHIFT` | `0x4000` |
| `0x004D8460` | `0x2C` | `DIK_Z` | `0x8200` |
| `0x004D8468` | `0x39` | `DIK_SPACE` | `0x0200` |
| `0x004D8470` | `0x2E` | `DIK_C` | `0x0400` |
| `0x004D8478` | `0x38` | `DIK_LMENU` | `0x1000` |
| `0x004D8480` | `0x1C` | `DIK_RETURN` | `0x0008` |
| `0x004D8488` | `0x2D` | `DIK_X` | `0x0800` |

Because the values are written rather than stored, this is the **default**
binding, and it is re-applied whenever `0x0042F0F0` runs — from either of the
two call sites above.

### 3.1 The table is also written from a configuration array — the controls are remappable

An earlier draft of this census claimed "no other writer was found". That was
**false**, and the scan it claimed to rest on is exactly what disproves it.
Counting every `mov` whose destination is a fixed address in
`[0x004D8430, 0x004D8490)`, the image contains **46** such stores: 24 in
`0x0042F0F0` and **22 outside it**, in two blocks of eleven:

```text
block A  0x00430C3F 0x00430C44 0x00430C5B 0x00430C67 0x00430C6C 0x00430C89
         0x00430C8F 0x00430C94 0x00430CAB 0x00430CB7 0x00430CBC
block B  0x00431022 0x00431027 0x0043103E 0x0043104A 0x0043104F 0x0043106C
         0x00431072 0x00431077 0x00431099 0x0043109F 0x004310A4
```

Both blocks copy scancodes out of a byte array based at `0x004D9CF9` with a
`0x18` stride:

```text
431013: 33 c0             xor  eax,eax
431015: 33 c9             xor  ecx,ecx
431017: a0 f9 9c 4d 00    mov  al,ds:0x4d9cf9
43101c: 8a 0d 11 9d 4d 00 mov  cl,BYTE PTR ds:0x4d9d11
431022: a3 30 84 4d 00    mov  ds:0x4d8430,eax
431027: 89 0d 38 84 4d 00 mov  DWORD PTR ds:0x4d8438,ecx
```

Each block writes eleven of the twelve scancode slots — every one except
`0x004D8480` (`DIK_RETURN`) — and never touches a mask slot.

`0x00430B10` is the **exact inverse**, and it is eleven byte reads, not the
single read the earlier draft listed:

```text
430b10: a0 30 84 4d 00    mov  al,ds:0x4d8430
430b15: 8a 0d 38 84 4d 00 mov  cl,BYTE PTR ds:0x4d8438
430b1b: 8a 15 40 84 4d 00 mov  dl,BYTE PTR ds:0x4d8440
430b21: a2 f9 9c 4d 00    mov  ds:0x4d9cf9,al
```

— it copies the live table back into the same `0x004D9CF9` array. The eleven
read addresses are `0x00430B10`, `0x00430B15`, `0x00430B1B`, `0x00430B26`,
`0x00430B31`, `0x00430B3D`, `0x00430B48`, `0x00430B53`, `0x00430B67`,
`0x00430B72`, `0x00430B7D`.

Both directions are reached from one dispatcher:

```text
430ff5: 48                dec  eax
430ff6: 0f 84 d4 00 00 00 je   0x4310d0      ; -> 0x0042F0F0 (defaults)
430ffc: 48                dec  eax
430ffd: 74 14             je   0x431013      ; -> block B (apply array)
```

`0x004310D0` is the second call site of the defaults writer already noted
above. So `[0x004D8430, 0x004D8490)` is the **live** binding table, `0x004D9CF9`
is a `0x18`-stride configuration copy, and a menu selects between applying the
copy and restoring the defaults.

**The controls are therefore remappable**, and any control mod must target the
`0x004D9CF9` array or the paths above rather than patching the live table,
which is rewritten from both directions.

One scoping caveat on that conclusion. Block **B** is demonstrably live: it is
the `je 0x431013` arm of the dispatcher above. Block **A** is not — `0x00430C30`
is reached only through thunk `0x00401DF2`, and **that thunk has zero call
sites and zero data occurrences in the image**, so block A's reachability is
unestablished. The remappability finding rests on block B and on
`0x00430B10`; block A is recorded as a third writer of the same range, not as
a demonstrated path.

What this census does **not** establish: the identity of that menu screen, the
full extent or callers of `0x00430C30`, `0x00430B10` and the function
containing `0x00431013`, the layout of the `0x18`-stride record beyond its
first byte, or why `DIK_RETURN`'s slot is excluded from both blocks.

Note `0x8200` for `DIK_Z` is two bits (`0x8000 | 0x0200`), the only
multi-bit mask in the table.

## 4. Joystick button table

The bring-up of §1 also writes eight pairs at `[0x004D8490, 0x004D84D0)`,
which is **outside** the range §2.2 walks (`jl 0x4d8494` stops first). These
are zero in the file image too. Written values, listed in **address** order
(the store order differs: `0x004D84C0`/`0x004D84C4` are written first, at
`0x0042F388`/`0x0042F38D`, and `0x004D84A8` precedes `0x004D84A0`). A second
writer of the same eight pairs, using immediates, exists at
`0x0042F250`-`0x0042F2EB`:

| Slot | value | mask | Same mask as |
|---|---:|---|---|
| `0x004D8490` | 0 | `0x8000` | `DIK_LCONTROL` |
| `0x004D8498` | 1 | `0x4000` | `DIK_LSHIFT` |
| `0x004D84A0` | 3 | `0x8200` | `DIK_Z` |
| `0x004D84A8` | 4 | `0x0200` | `DIK_SPACE` |
| `0x004D84B0` | 6 | `0x0400` | `DIK_C` |
| `0x004D84B8` | 2 | `0x1000` | `DIK_LMENU` |
| `0x004D84C0` | 8 | `0x0008` | `DIK_RETURN` |
| `0x004D84C8` | 7 | `0x0800` | `DIK_X` |

Every mask is one that also appears in §3, so keyboard and joystick feed the
same action-bit vocabulary.

The first column **is** a `DIJOYSTATE` button index, and this is Confirmed by
instruction, not inferred. An earlier draft of this census said "no instruction
seen here indexes `DIJOYSTATE` with it"; that was false, and the instruction
lies inside the extent §2 establishes:

```text
42ed6f: b9 94 84 4d 00       mov ecx,0x4d8494
42ed74: 8b 71 fc             mov esi,DWORD PTR [ecx-0x4]      ; the first column
42ed77: 80 be 90 8b 59 00 00 cmp BYTE PTR [esi+0x598b90],0x0  ; DIJOYSTATE.rgbButtons
42ed7e: 74 03                je  0x42ed83
42ed80: 66 0b 39             or  di,WORD PTR [ecx]            ; the mask
42ed83: 83 c1 08             add ecx,0x8
42ed86: 81 f9 d4 84 4d 00    cmp ecx,0x4d84d4
42ed8c: 7c e6                jl  0x42ed74
```

Eight iterations over `[0x004D8490, 0x004D84D0)`, indexing
`0x00598B90 = 0x00598B60 + 0x30`. `0x30` is the offset of `rgbButtons` in
`DIJOYSTATE`, and `0x30 + 32 = 0x50`, the `dwDataSize` §1.3 decoded — so the
buffer layout is self-consistent. `0x0042F320` independently scans
`[eax+0x00598B90]` for `eax` in `[1, 0x20)`, i.e. across 32 buttons.

## 5. The second input path — `GetAsyncKeyState` (prior art)

`GetAsyncKeyState` is imported at IAT slot `0x0086478C`. The image contains
exactly **two** little-endian occurrences of that address, at file `0x0A6C43`
and `0x0ADF1E` — the operands of:

- `0x004A7841`: `mov esi,DWORD PTR ds:0x86478c`, inside the chooser
  `0x004A7600` (no `ret` between `0x004A7600` and the load; the function's
  first `ret` is `0x004A7C06`);
- `0x004AEB1C`: `jmp DWORD PTR ds:0x86478c`, the ordinary import thunk.

**The thunk is dead**: no `call` or `jmp` anywhere in the image targets
`0x004AEB1C`, and the value `0x004AEB1C` occurs nowhere as data. The import is
reached only by loading the IAT slot into `esi` and calling the register, at
eight sites: `0x004A793B`, `0x004A7944`, `0x004A79A7`, `0x004A79B0`,
`0x004A79DD`, `0x004A79E6`, `0x004A7A10`, `0x004A7A19`. Two of them poll
`0x20` and `0x0D` (`VK_SPACE`, `VK_RETURN`).

All of this restates [[PC autonomous game control]] and
`EXP-20260816-145`, which already record the chooser, the polling and the
`0x004A7841` load. The additions here are only the dead thunk and the eight
call sites.

**The two paths are disjoint.** The chooser path uses no DirectInput object,
and `0x0042EBC0` uses no `GetAsyncKeyState`. That is consistent with the
recorded runtime finding that menu key *taps* are unreliable while in-game
input is not.

## 6. Other consumers found

- `0x0042F680` clears the same 256-byte buffer, calls `Acquire` (`+0x1C`) at
  `0x0042F699` and `GetDeviceState` (`+0x24`) at `0x0042F6AE` with `0x100` and
  `0x00598A10` — a second keyboard-only poll, with no binding walk.
- `0x0042F600` releases: keyboard `Unacquire` (`+0x20`) at `0x0042F616` and
  `Release` (`+0x08`) at `0x0042F621`, then walks a list at `0x00598B40`.

Neither function's full extent nor its callers were established.

## 7. What this census does not establish

- Any runtime fact. Nothing was launched; no device was observed created,
  acquired or read, and no key was observed producing a bit.
- What each action bit in `0x00598B10` means. No bit is given a gameplay name.
- What consumes `0x00598B10`, `0x00598B12`, `0x00598BC0`-`0x00598BC6`,
  `0x00598B5C`, or the synthesised axes `0x004F0440`/`0x004F0444`.
- The identity of the configuration screen behind §3.1, the extents and
  callers of `0x00430C30`, `0x00430B10` and the function containing
  `0x00431013`, the layout of the `0x18`-stride record at `0x004D9CF9` beyond
  its first byte, and why `DIK_RETURN`'s slot is excluded from both write
  blocks.
- The enumeration callback `0x00401979` (→ `0x0042F040`) beyond the fact that
  it writes `0x00598B14` at `0x0042F077`; what it stores at `0x005987D0`; the
  meaning of `0x005988E0`.
- The joystick button-index reading in §4, and how `0x00598B60` is consumed.
- The enclosing functions of the two per-frame call sites, and the extents of
  `0x0042F600` and `0x0042F680`.
- Whether register-indirect dispatch reaches any of these functions from
  callers this census did not find. Call instructions, both thunk directions
  and absolute-value scans were used; §5's own finding — an import reached only
  by a register load — is a concrete demonstration that scan-based methods miss
  computed dispatch.
