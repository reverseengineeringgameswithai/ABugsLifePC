---
type: experiment
id: EXP-20260817-181
date: 2026-08-17
question: 'Which device objects and formats does the PC input subsystem acquire, and where is per-frame state read?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static analysis; GNU objdump 2.46; rabin2 5.9.8; repository Python 3.14
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: read-only disassembly, import-table reads and direct byte decoding of the exact retail work copy; no runtime process, debugger, breakpoint or target write
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-input-static-census.md
addresses:
  - "0x0042F350"
  - "0x0042EBC0"
  - "0x0042F0F0"
  - "0x00598A10"
  - "0x00598B10"
  - "0x00598B20"
  - "0x005988D0"
  - "0x004D8430"
  - "0x004C0230"
  - "0x004C0220"
  - "0x004AFE90"
  - "0x004AEE70"
  - "0x004A7841"
file_offsets:
  - "0x02E750"
  - "0x02DFC0"
  - "0x02E4F0"
  - "0x0D7030"
  - "0x0BEE30"
  - "0x0BEE20"
  - "0x0AF290"
  - "0x0AE270"
result: input-row-proposed-bounded-with-two-disjoint-paths-and-a-runtime-written-binding-table
created: 2026-08-17T07:30:00
updated: 2026-08-17T07:30:00
tags:
  - re/experiment
  - re/static
  - re/input
  - research/coverage
---

# EXP-20260817-181 - PC input subsystem static census

## Date

2026-08-17.

## Question

[[Subsystem Coverage Map]] lists Input at **Touched**, with one anchor —
`DirectInputCreateA` at `0x0042F43D` inside `0x0042F350`, found incidentally by
the audio census — and the open question "which device objects and formats are
acquired, and where is per-frame state read?". This is the second row of the
recorded Actors/AI → Input → Event/scripting preference.

Bounded reconnaissance. It advances no milestone gate and M5 stays where
`EXP-20260816-171` left it.

## Binary SHA-256

`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`, re-hashed
from `work/copies/BUGS_PC-full-disc/bugs.exe` before analysis.

## Environment

Fedora Linux 44, offline. GNU objdump 2.46 (`-d -M intel`), `rabin2` 5.9.8 for
the import table, and direct little-endian byte decoding from repository
Python 3.14.

## Environment version

`objdump 2.46-3.fc44`, `radare2 5.9.8`.

## Working directory

`/home/dev/ABLPC`.

## Configuration

Read-only. No process launched, no debugger, no breakpoint, no target write, no
`originals/` path, no PS1 source, and no game asset read.

## Procedure

1. Re-hash the work copy and dump `.text`.
2. **Before anything else**, grep every file in the export directory —
   including the generated `ghidra-evidence.json` — and the Vault, for each
   principal address, so the novelty boundary is fixed up front.
3. Establish the extent of each function before scoping any claim to it.
4. Decode GUIDs and `DIDATAFORMAT` structures from raw bytes and compare them
   against the documented DirectInput values rather than naming them by
   guesswork.
5. Follow the device pointers to their consumers and decode the binding tables.

## Expected

Either a DirectInput bring-up with identifiable devices and a locatable
per-frame read — in which case the row's question is answered — or a bring-up
whose consumers cannot be found, in which case the row stays Touched with a
recorded negative.

## Observed

### Confirmed

- **`0x0042F350` (extent `0x0042F350`-`0x0042F565`, one `ret`) is the
  DirectInput bring-up.** It calls `DirectInputCreateA` at `0x0042F43D` with
  version `0x0500` and `hInstance` from `0x0059F730`, storing the object in
  `0x00598B18`.
- **The keyboard device is created from `GUID_SysKeyboard`.** The 16 bytes at
  `0x004C0230` decode to `{6F1D2B61-D5A0-11CF-BFC7-444553540000}`, the
  documented value. `CreateDevice` at `0x0042F45D` stores the device in
  `0x00598B20`; `SetDataFormat` at `0x0042F471` passes `0x004AFE90`;
  `SetCooperativeLevel` at `0x0042F489` passes the window handle `0x0059F73C`
  and flags `6` (`DISCL_NONEXCLUSIVE | DISCL_FOREGROUND`); `Acquire` at
  `0x0042F498`. Success sets `[0x00598BC8] = 1`.
- **The two data formats are `c_dfDIKeyboard` and `c_dfDIJoystick`.**
  `0x004AFE90` decodes to `dwSize 24, dwObjSize 16, dwFlags 0x2, dwDataSize
  256, dwNumObjs 256`; `0x004AEE70` to `dwSize 24, dwObjSize 16, dwFlags 0x1,
  dwDataSize 80, dwNumObjs 44`. Both match the documented layouts, and both
  match the buffer sizes their consumers actually pass.
- **Joysticks are enumerated and promoted to `IDirectInputDevice2A`.**
  `EnumDevices` at `0x0042F4BA` passes `dwDevType 4` (`DIDEVTYPE_JOYSTICK`),
  callback thunk `0x00401979`, `pvRef 0x005987D0`, flags `1`. The loop at
  `0x0042F4C5`-`0x0042F551` then, per device, calls `CreateDevice`,
  `QueryInterface` for `0x004C0220` — which decodes to
  `{5944E682-C92E-11CF-BFC7-444553540000}`, `IID_IDirectInputDevice2A` —
  `SetDataFormat(0x004AEE70)`, `SetCooperativeLevel(hwnd, 5)` and `Acquire`.
  Flags `5` is `DISCL_EXCLUSIVE | DISCL_FOREGROUND`, a **different**
  cooperative level from the keyboard's.
- **Per-frame state is read at `0x0042EBC0`** (code extent
  `0x0042EBC0`-`0x0042EEBB`, one `ret`, followed by its own jump and byte
  tables). It is reached only through thunk `0x00401B5E`, whose call sites are
  `0x00464E1C` and `0x0049BDB7`. It clears a 256-byte buffer, calls `Acquire`
  at `0x0042EC1C` and `GetDeviceState(0x100, 0x00598A10)` at `0x0042EC31`. So
  **`0x00598A10` is the 256-byte keyboard state buffer** and a key is
  `0x00598A10 + scancode`.
- **Right-hand modifiers are folded onto left-hand ones** before the binding
  walk: `0x36 RSHIFT → 0x2A LSHIFT`, `0x9D RCONTROL → 0x1D LCONTROL`,
  `0xB8 RMENU → 0x38 LMENU`. Only the left-hand scancodes appear in the binding
  table, which is consistent.
- **The binding table is walked at `0x0042EC86`-`0x0042ECDF`**: twelve 8-byte
  entries over `[0x004D8430, 0x004D8490)`, each a scancode dword and a mask
  dword; a pressed key ORs its mask into an accumulator stored to
  `0x00598B10`. `DIK_TAB` is handled separately just before the loop and ORs
  the same mask slot `0x004D8474` that the loop's entry 8 (0-based) uses.
- **The four direction keys synthesise a two-axis value.** Masks in
  `[0x10, 0x80]` index a byte table at `0x0042EED0` and a five-arm jump table
  at `0x0042EEBC`. Decoded: `UP → edx += 0x8000`, `RIGHT → ebp += 0x8000`,
  `DOWN → edx -= 0x8000`, `LEFT → ebp -= 0x8000`, everything else falls to the
  loop-continue arm. `ebp` is stored to `0x004F0440` and `edx` to `0x004F0444`.
  Every other mask in the table is outside `[0x10, 0x80]` and fails the bound
  check, so exactly those four participate.
- **Joystick state uses `Poll`.** Gated on `[0x00598B28]`, the sequence is
  `Poll` (`+0x64`) at `0x0042ED0E`, `Acquire` on failure, `GetDeviceState` of
  `0x50` bytes into `0x00598B60` at `0x0042ED2F`, `Acquire` on failure. `+0x64`
  is `Poll`, which exists only on `IDirectInputDevice2A` — the interface the
  bring-up queried for, and the `0x50` matches `c_dfDIJoystick`'s `dwDataSize`.
- **The binding table is not stored data, and it is remappable.**
  `[0x004D8430, 0x004D8490)` is all zero in the file image and is written by
  `0x0042F0F0`, reached only through thunk `0x004016AE`, which has **two** call
  sites: `0x0042F37D` inside the bring-up, and `0x004310D0`. It is **also**
  written from 22 further stores outside that function, in two blocks of
  eleven (`0x00430C3F`-`0x00430CBC` and `0x00431022`-`0x004310A4`), each
  copying scancodes out of a `0x18`-stride byte array based at `0x004D9CF9`;
  `0x00430B10` is the exact inverse, eleven byte reads copying the live table
  back into that array. A dispatcher at `0x00430FF6`/`0x00430FFD` selects
  between the defaults writer and the array-apply block. So the controls are
  configurable, and a one-shot patch of the live table would be overwritten
  from both directions. Scoping caveat: only block B is demonstrably live, as
  the `je 0x431013` arm; block A is reached only through thunk `0x00401DF2`,
  which has zero call sites and zero data occurrences, so its reachability is
  unestablished. The twelve defaults are UP/DOWN/LEFT/RIGHT,
  LCONTROL, LSHIFT, Z, SPACE, C, LMENU, RETURN, X, with masks `0x0010`,
  `0x0040`, `0x0080`, `0x0020`, `0x8000`, `0x4000`, `0x8200`, `0x0200`,
  `0x0400`, `0x1000`, `0x0008`, `0x0800`. `0x8200` for Z is the only
  multi-bit mask.
- **Joystick buttons share the keyboard's action-bit vocabulary.** The bring-up
  also writes eight pairs at `[0x004D8490, 0x004D84D0)` — outside the range the
  per-frame loop walks — whose masks are exactly the eight non-direction
  keyboard masks.
- **`GetAsyncKeyState`'s import thunk is dead.** The IAT slot `0x0086478C` has
  exactly two little-endian occurrences in the image: the `mov esi,...` at
  `0x004A7841` and the `jmp` thunk at `0x004AEB1C`. **No `call` or `jmp`
  anywhere targets `0x004AEB1C`**, and its address occurs nowhere as data. The
  import is reached only by loading the slot into `esi` and calling the
  register, at eight sites between `0x004A793B` and `0x004A7A19`; `esi` is not
  reloaded between the load and any of them. Two of the eight poll `0x20` and
  `0x0D` (`VK_SPACE`, `VK_RETURN`).
- **The two input paths are disjoint.** The chooser path uses no DirectInput
  object; `0x0042EBC0` uses no `GetAsyncKeyState`.

- **The joystick pair table's first column is a `DIJOYSTATE` button index.**
  The eight-iteration loop at `0x0042ED6F`-`0x0042ED8C` reads that column and
  tests `[esi + 0x00598B90]`, where `0x00598B90 = 0x00598B60 + 0x30` is
  `DIJOYSTATE.rgbButtons`; `0x30 + 32 = 0x50` is the `dwDataSize` decoded in
  §1.3, so the layout is self-consistent. `0x0042F320` independently scans the
  same array for indices in `[1, 0x20)`.

### Inferred

That the disjointness of the two paths explains the recorded runtime finding —
menu key *taps* unreliable while in-game input is not — is consistent but not
demonstrated here; that finding is `PC autonomous game control`'s, from
runtime.

### Unknown

What any action bit in `0x00598B10` means; what consumes `0x00598B10`,
`0x00598B12`, `0x00598BC0`-`0x00598BC6`, `0x00598B5C`, or the synthesised axes
`0x004F0440`/`0x004F0444`; the identity of the configuration screen behind the
`0x004D9CF9` array and the extents and callers of its three blocks; the layout
of that `0x18`-stride record beyond its first byte; why `DIK_RETURN`'s slot is
excluded from both write blocks; the enumeration callback `0x00401979` and what
it stores at
`0x005987D0` and `0x00598B14`; the meaning of `0x005988E0`; how `0x00598B60`
is consumed; the enclosing functions of the two per-frame call sites; and
every runtime fact, since nothing was run.

## Artifacts

`static/exports/BIN-97c95ba5572dce63/SUBSYS-input-static-census.md` carries the
full derivation, the quoted disassembly, both decoded tables, the identifier
comparisons and the extent statements.

## Addresses

Bring-up `0x0042F350`; per-frame read `0x0042EBC0`; binding writer
`0x0042F0F0`; keyboard state buffer `0x00598A10`; action-bit accumulator
`0x00598B10`; keyboard device `0x00598B20`; joystick device array `0x005988D0`;
binding table `0x004D8430`; `GUID_SysKeyboard` `0x004C0230`;
`IID_IDirectInputDevice2A` `0x004C0220`; `c_dfDIKeyboard` `0x004AFE90`;
`c_dfDIJoystick` `0x004AEE70`; chooser import load `0x004A7841`.

## File offsets

`0x02E750` (bring-up), `0x02DFC0` (per-frame read), `0x02E4F0` (binding
writer), `0x0D7030` (binding table), `0x0BEE30` and `0x0BEE20` (the two GUIDs),
`0x0AF290` and `0x0AE270` (the two data formats).

## Interpretation

The row's question is answered on both halves. The devices are a
`GUID_SysKeyboard` keyboard at `c_dfDIKeyboard` with a non-exclusive
foreground cooperative level, and zero or more enumerated joysticks promoted to
`IDirectInputDevice2A` at `c_dfDIJoystick` with an exclusive foreground level.
Per-frame state is read at `0x0042EBC0` into `0x00598A10` (keyboard) and
`0x00598B60` (joystick 0), and reduced to one action-bit word at `0x00598B10`
through a twelve-entry binding table plus a four-direction analog synthesis.

Two findings are worth carrying beyond this row. First, the binding table is
**written at runtime from three places** — the defaults writer `0x0042F0F0`,
itself called from two sites, and two eleven-store blocks that apply a
`0x18`-stride configuration array at `0x004D9CF9`, with `0x00430B10` copying
the live table back into that array. The controls are configurable, and the
array rather than the live table is what a control mod would have to target.
Second, `GetAsyncKeyState`'s ordinary import thunk is **dead code**: the only
path to that import is a register load. A scan-based caller census would have
concluded the import was unused, which is a concrete instance of the limitation
the audio census's method note warns about — and, as the first audit of this
packet showed, an address-range reference scan can produce a false negative in
the same way if it is not actually run to completion.

Novelty is bounded honestly in §0 of the export: the `0x0042F350`/`0x0042F43D`
anchor is the audio census's, the whole `GetAsyncKeyState`-in-the-chooser
finding is `PC autonomous game control`'s and `EXP-20260816-145`'s, and the
generated `ghidra-evidence.json` already contains decompilations mentioning
every address used. What is new is the authored, verified model.

## Result

The coverage row **Input** is proposed to move Touched → **Bounded** with the
anchors above. No milestone status changes and no runtime claim is made.
`KU-070` records what the action bits mean and what consumes them.

## Follow-up

The cheapest next step is static: identify what consumes `0x00598B10` — that
is the single edge between this subsystem and gameplay, and naming even one bit
would convert the whole table from addresses into controls.

The cheapest *decisive* step is runtime and read-only, and needs separate
authorization: sample `0x00598B10` while holding one known key under the
six-marker hardware gate. One receipt would bind one bit to one key and confirm
the table is live, and it would discriminate `KU-070`.
