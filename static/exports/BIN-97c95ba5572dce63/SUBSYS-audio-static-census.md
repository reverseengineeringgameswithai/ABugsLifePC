# PC audio subsystem static census

Binary SHA-256:
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`

Offline census read from `work/copies/BUGS_PC-full-disc/bugs.exe` (hash
verified) with radare2 5.9.8, `rabin2`, and direct byte decoding. No runtime,
debugger, or target write. Section mapping used for file offsets: `.text`
file `0x400` -> VA `0x00401000`; `.rdata` `0xBEC00` -> `0x004C0000`; `.data`
`0xBFC00` -> `0x004C1000`.

## Import surface

`rabin2 -i` reports three audio-relevant DLL families:

| DLL | Import | IAT |
|---|---|---|
| DSOUND.dll | `DirectSoundCreate` | `0x00864538` |
| DSOUND.dll | `DirectSoundEnumerateA` | `0x0086453C` |
| WINMM.dll | `mmioOpenA`, `mmioClose`, `mmioRead`, `mmioWrite`, `mmioSeek`, `mmioDescend`, `mmioAscend`, `mmioCreateChunk`, `mmioAdvance`, `mmioGetInfo`, `mmioSetInfo` | `0x00864858`-`0x00864880` |
| WINMM.dll | `timeGetTime` | `0x00864884` |

Neither DirectSound import has a direct `call dword [IAT]` site. Both are
reached through an import jump-thunk table: `jmp dword [IAT]` at
`0x004AFEA8` (DirectInputCreateA), `0x004AFEAE` (DirectSoundCreate), and
`0x004AFEB4` (DirectSoundEnumerateA). Internal calls likewise route through
the `0x00401xxx` `jmp` thunk table, so no function in the audio module has a
direct caller.

## DirectSound bring-up (`0x004A3480`)

Reached through thunk `0x00401B95`; callers `0x00412CAB`, `0x00412DE5`,
`0x0042BAD0`.

```
0x004A3480  push ecx / push edi
0x004A3482  call 0x00401D2F
0x004A348E  mov edi, 0x007EDF08 ; rep stosd 0x300 dwords -> zeroed
0x004A349F  mov edi, 0x007ECE58 ; rep stosd 0x300 dwords -> zeroed
0x004A34A6  mov [0x007ECA44], 0
0x004A34AB  mov [0x007ECA40], 0
0x004A34B5  push 0x004017C1     ; enumeration callback (thunk -> 0x0049DD00)
0x004A34BA  call 0x004AFEB4     ; DirectSoundEnumerateA
0x004A34BF  mov ecx, [0x007EDA60]   ; selected device GUID pointer
0x004A34C7  push 0x007EDAE8         ; out: IDirectSound *
0x004A34CD  call 0x004AFEAE     ; DirectSoundCreate
0x004A34D2  mov eax, [0x007EDAE8]
0x004A34D9  je  0x004A34FE      ; skip when creation failed
0x004A34DB  mov ecx, [0x0059F73C]   ; window handle
0x004A34E7  call dword [edx+0x18]   ; vtable +0x18 (obj, hwnd, 1)
0x004A34EC  mov dword [0x007ECA40], 1
0x004A34F6  call 0x0040123A     ; with argument 1
0x004A3500  ret
```

Globals established here:

| Address | Role (address-named) |
|---|---|
| `0x007EDAE8` | DirectSound object pointer |
| `0x007EDA60` | device GUID pointer consumed by create |
| `0x0059F73C` | window handle passed to vtable `+0x18` |
| `0x007ECA40` | set to 1 only after successful creation |
| `0x007ECA44` | cleared at bring-up; role unknown |
| `0x007EDDF8` | single dword cleared at `0x004A3493`; role unknown |
| `0x007EDF08` | `0x300`-dword table cleared at bring-up |
| `0x007ECE58` | `0x300`-dword table cleared at bring-up |

`0x0049DD00` is the real enumeration callback behind thunk `0x004017C1`.

## Device initializer (`0x0042BA60`)

`0x0042BAD0` calls the DirectSound bring-up thunk and `0x0042BAED` calls
thunk `0x00401582` -> `0x0042F350`, which is the function containing the sole
`DirectInputCreateA` call site at `0x0042F43D`. Audio and input creation are
therefore siblings under one initializer.

## Track-name table (`0x00596528`)

Function `0x0042BB90` (thunk `0x00401DBB`; callers `0x0041A1FF`,
`0x0049D35A`, `0x0049D41B`) writes 40 track-name pointers into an 8-byte
stride table based at `0x00596528`, with immediate and register-based stores,
and zeros into `slot+4`. EXP-20260909-005 corrects the earlier immediate-only census:

| Index range | Names |
|---|---|
| 0-14 | `audio\Level1a.wav` .. `audio\Level5c.wav` (five levels x a/b/c) |
| 15-16 | `dead` |
| 17-21 | `levcom`, `title`, `bugs2mb`, `bugs2ma`, `bugs2mc` |
| 22-23 | `dead` |
| 24-36 | `less1` .. `less8`, `less8a`, `less9` .. `less12` |
| 37-39 | `less13` |
| 40 | explicitly null |

Correction, EXP-20260909-005: **40 populated track slots**. The stores through
EAX at `0x0042BBAF`..`0x0042BBBE` and `0x0042BDF8`/`0x0042BE08`/`0x0042BE13`
were omitted previously. Fresh disassembly and native execution at both PE
bases confirm DEAD and LESS13 are populated. See `reports/audio/EXP-20260909-005-native.json`.

The disc directory `PC/BUGS/CD/AUDIO` contains exactly 35 `.WAV` files, and
the string forms use the `audio\` prefix, matching that layout.

## Track path assembly and playback log

Inside the same function, a path is concatenated into the buffer at
`0x00596960` using the literal `\pc\bugs\cd\` (`0x004E9070`) plus the selected
`audio\NAME.wav`, then logged with
`PLAYTRACK : Attempting to play track %s.\n` (`0x004D744C`, referenced at
`0x0042BEF6`).

## DSStream and volume

- `DSStreamWndClass` (`0x004D73E0`) has exactly **one** reference in the whole
  image: the `push` at `0x0042C3B0`, feeding `UnregisterClassA`. That is a
  **cleanup** site. No registration site referencing this string was found; if
  registration exists it goes through a structure field, which this census did
  not trace. `DSStream` (`0x004D73F8`) is the paired string.
- `0x0042C3B0` lies inside the function beginning `0x0042C130` — the same
  DSStream token parser recorded in `EXP-20260816-143`, not a separate
  function. `0x0042C29F` is a `je` target inside a byte-scan loop in that
  function, not an entry point.
- `SETMUSICVOL : Vol %d` and `SETMUSICVOL : Failed to set volume - error is
  %s.` indicate a volume path with DirectSound error-to-string mapping; the
  DirectSound error text block sits at `0x004C64A8` onward.
- `CONFIG : Base CD track is %d.` is pushed at `0x0042BA1E` and `0x0042BABE`.

Address convention: sites are cited at the **instruction start**. Earlier
revisions of this census cited some operand bytes instead
(`0x0042C3B1`, `0x0042BA1F`, `0x0042BABF`).

## RIFF/`mmio` cluster (`0x004AD000`-`0x004ADB20`)

All 37 `mmio*` call sites fall inside one contiguous region:

| Import | Call sites |
|---|---|
| `mmioOpenA` | `0x004AD02D`, `0x004AD3FB` |
| `mmioClose` | `0x004AD1A1`, `0x004AD3B5`, `0x004AD6F6`, `0x004ADA41` |
| `mmioRead` | `0x004AD89B` |
| `mmioWrite` | `0x004AD467`, `0x004AD48D`, `0x004AD4D7`, `0x004AD6CE`, `0x004AD8A8` |
| `mmioSeek` | `0x004AD246`, `0x004AD694`, `0x004AD767`, `0x004AD801`, `0x004AD9A2` |
| `mmioDescend` | `0x004AD25D`, `0x004AD6A0`, `0x004AD6BA`, `0x004AD9C1` |
| `mmioAscend` | `0x004AD162`, `0x004AD66E`, `0x004AD683`, `0x004AD6D9`, `0x004AD6E5`, `0x004AD7DD`, `0x004AD8BB` |
| `mmioCreateChunk` | `0x004AD56C`, `0x004AD885`, `0x004ADAFC` |
| `mmioGetInfo` | `0x004AD293`, `0x004AD57F`, `0x004ADB15` |
| `mmioSetInfo` | `0x004AD308`, `0x004AD655` |
| `mmioAdvance` | `0x004AD5D7` |

The presence of `mmioCreateChunk` and `mmioWrite` means this region can
author RIFF chunks, not only read them. Whether the game ever writes audio at
runtime is unknown, and this region sits in the address range the project has
already flagged as possibly statically linked runtime code.

## Audio-module entry points

**Twelve** functions in `0x0042B000`-`0x0042C600` have an entry in the
`0x00401xxx` thunk table: `0x0042B020`, `0x0042B1F0`, `0x0042B9C0`,
`0x0042BA60`, `0x0042BB30`, `0x0042BB50`, `0x0042BB90`, `0x0042C0D0`,
`0x0042C110`, `0x0042C130`, `0x0042C4C0`, `0x0042C4F0`.

| Function | Thunk | Direct call sites |
|---|---|---:|
| `0x0042B020` | `0x00401E60` | 34 (32 outside the module, plus `0x0042B747` and `0x0042B781` inside it) |
| `0x0042C0D0` | `0x004015C3` | 23 |
| `0x0042C110` | `0x004012AD` | 19 |
| `0x0042BB90` | `0x00401DBB` | 3 (`0x0041A1FF`, `0x0049D35A`, `0x0049D41B`) |
| `0x0042C4F0` | `0x00401915` | 2 (`0x004AE8B5`, `0x004AE920`) |
| `0x0042B1F0` | `0x00401B22` | 1 (`0x0041459C`) |
| six others | — | 0 direct call sites |

An earlier revision said seventeen, by counting ordinary `jmp` instructions
*inside* module functions as thunk-table entries. Only `E9` entries within
`0x00401000`-`0x00402000` are thunks.

`0x0042C130` is the DSStream command-line token parser already recorded in
`EXP-20260816-143`.

## Indirect dispatch record (`0x004D81E8`)

The direct-call census above cannot see every caller. At `.data`
`0x004D81E8` sits a record of a count and three code pointers:

```
0x004D81E8  dd 0x00000003
0x004D81EC  dd 0x00401B04   ; thunk -> 0x0042BA60  (device initializer)
0x004D81F0  dd 0x004011D1   ; thunk -> 0x0042BB30
0x004D81F4  dd 0x00401299   ; thunk -> 0x0042BB50
0x004D81F8  db "DIRECTX",0
```

This is how `0x0042BA60` is reached: it has **zero** direct call sites, so
under a direct-call-only method the packet's central initializer would look
unreferenced. Any subsystem census must therefore check `.data`
function-pointer records as well as call instructions. Register-indirect
dispatch (`FF D0`-family) was not traced and could hide further callers.

## Not established here

What `0x0042B020`, `0x0042C0D0`, and `0x0042C110` do; whether sound effects
use a path separate from the music tracks; the meaning of the track entry's
second dword; how DSStream buffers or streams; which non-tutorial callers select DEAD and the extra LESS13 aliases; and
audible runtime behaviour, since no process was started. EXP-20260909-005
further resolves tutorial PCM selection and bounded native data reads.
