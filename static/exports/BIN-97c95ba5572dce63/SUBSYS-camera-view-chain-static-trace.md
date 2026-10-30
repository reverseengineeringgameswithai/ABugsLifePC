# PC camera/view-transform static trace

## Evidence identity

- Executable: `work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe`
- SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Image base: `0x00400000`
- `.text`: VA `0x00401000`, file offset `0x00000400`
- GNU objdump: `2.46-3.fc44`
- Checked Ghidra export SHA-256:
  `db2dc35a8dcbc9138a318b5ca07bdc1e5ac2703c5760b7b99207a29703c67f5d`
- Earlier independent PC render-provenance export:
  `M2-positive-target-selector2-input-provenance.md`, SHA-256
  `58f1832c8eaf70f701776c6edaa61e3d1e8c877eadf45aed195034c9729e6856`
- Correction/audit authority: `EXP-20260816-162` and
  `EXP-20260816-164`

All file offsets below use `VA - 0x00401000 + 0x400`. The trace is PC-only;
no PS1 statement establishes any item in it.

## Confirmed native data flow

### 1. Ordered update and view-consumer calls

The sequence at VA `0x00414573`-`0x0041458F` (file
`0x00013973`-`0x0001398F`) does the following in order:

```text
0x00414573  push 0x0059D910
0x00414578  call 0x0040103C -> 0x0043F9E0
0x00414580  call 0x0040119F -> 0x0041B7D0
0x00414585  push 0x00599C90
0x0041458A  call 0x00401848 -> 0x00455710
```

This proves call order and the common-block argument. Static evidence alone
does not prove how often the enclosing sequence executes.

### 2. Flik-relative source update

`0x0041B7D0` pushes source block `0x0059DD90` at `0x0041B8B2` and calls
thunk `0x00401D02 -> 0x0041ADF0` at either `0x0041B8BB` or
`0x0041B90E`. Inside `0x0041ADF0`:

- `0x0041AF3E`/`0x0041AF47` read live Flik Z/X
  `0x0059D918`/`0x0059D910` and compare them with source fields;
- `0x0041B0CC`, `0x0041B10C`, and `0x0041B146` read live Y/X/Z while
  deriving target position values;
- `0x0041B2B2`-`0x0041B2D2` reads all three live coordinates and subtracts
  source position fields `[ESI+0x00]`, `[ESI+0x04]`, `[ESI+0x08]`;
- `0x0041B486`-`0x0041B4B6` moves those three position fields one eighth
  toward fields `[ESI+0x0C]`, `[ESI+0x10]`, `[ESI+0x14]`;
- `0x0041B4DD`-`0x0041B5C0` updates angle-like 12-bit fields at
  `[ESI+0x18]` and `[ESI+0x1A]` using wrap at `0x1000` and sine-table
  address `0x004C2100`.

The confirmed claim is a Flik-relative position/orientation-source update.
Calling it the ordinary gameplay-follow camera remains an inference.

### 3. Flag-selected two-source copy

`0x0041B8AD` reads flag byte `0x0059A5EE` and tests bit 0 at
`0x0041B8B7`:

- bit clear: `0x0041B8C0`-`0x0041B906` copies position
  `0x0059DD90`/`94`/`98` and three words at `0x0059DDA8`/`AA`/`AC`
  into common block `0x00599C90`-`0x00599CA0`;
- bit set: after calling `0x0041ACC0` on `0x0059A5C0`,
  `0x0041B920`-`0x0041B966` copies position
  `0x0059A5C0`/`C4`/`C8` and three words at
  `0x0059A5E4`/`E6`/`E8` into the same common block.

`0x0041ACC0` independently smooths its input block's `[+0x00..+0x08]`
toward `[+0x18..+0x20]` and updates 12-bit fields `[+0x24]` and `[+0x26]`
at `0x0041ACC8`-`0x0041ADA5`. The existence of two source layouts, the flag
test, and the common destination are Confirmed. “Gameplay” and “setpiece”
roles are not.

### 4. Common block becomes a render-consumed origin and matrix

`0x00455710` consumes the common block:

- `0x0045571A`-`0x0045575A` reads its three words at `+0x0C`, `+0x0E`,
  and `+0x10`;
- `0x00455788` pushes output `0x005B58E0` and `0x00455799` calls
  `0x004012BC -> 0x00463C80`;
- `0x00463D55`-`0x00463E48` writes nine signed matrix words at output
  offsets `+0x00` through `+0x10`, proving that `0x005B58E0` receives the
  generated 3x3 matrix;
- `0x0045588D`-`0x004558A5` writes input position `[+0x00..+0x08]` to
  origin `0x005BDB8C`/`90`/`94`;
- `0x00455910` copies eight dwords beginning at `0x005B58E0` into
  `0x005BDBAC`.

The same consumer has exactly two direct thunk calls in the executable:
`0x0041458A` with common global `0x00599C90`, and `0x0043D486` with a local
position/angle block. The second call's higher-level role remains Unknown.

### 5. Renderer loads the matrix used by game-code transforms

At `0x0044D4C1` (file `0x0004C8C1`) renderer function `0x0044D430`
pushes `0x005B58E0` and calls thunk `0x00401C4E -> 0x004636C0`.
`0x004636C0`-`0x00463717` sign-extends all nine matrix words into scratch
globals `0x0063E888`-`0x0063E8B0`. At `0x0044D4F0` the same renderer also
passes origin `0x005BDB8C` and the matrix copy `0x005BDBAC` to
`0x004A3990`, an independent render-consumption edge visible in the checked
Ghidra export.

`0x00405FE0` (file `0x000053E0`) is not downstream of an already-completed
screen transform. After reading four pointer arguments at
`0x00406015`, `0x00406028`, `0x00406035`, and `0x00406046`, it begins a
signed 3x3 multiply at `0x0040605F`. The first complete result at
`0x00406069`-`0x004060A1` multiplies by `0x0063E888`/`8C`/`90`, performs
signed division by 4096, adds `0x0063E8B8`, and stores a transformed word.
The next components use `0x0063E898`-`0x0063E8B0` plus translations
`0x0063E8BC`/`C0`. Thus the builder performs a game-code transform locally.

This supports a bounded view-transform chain. It does not prove that every
writer of the scratch matrix is a camera path or that every builder call sees
the uncomposed matrix directly.

## Corrected adjacent claims

### Viewport locator

The full create/add/setup sequence is `0x00423E73`-`0x00423F71`. The
44-byte viewport structure is zeroed and populated at
`0x00423EDE`-`0x00423F3F` and submitted by the indirect call at
`0x00423F43` (file `0x000232DE`-`0x00023343`). The rejected values
`0x00423E93` and `0x00423F55` are bytes inside immediates belonging to
instructions that begin at `0x00423E92` and `0x00423F54`; they are not
instruction boundaries.

### Known TL-vertex boundary

The three reviewed Direct3D calls at `0x004047E9`, `0x00405816`, and
`0x0040598B` each receive vertex-type argument `3`. Their error strings at
`0x004C4B28`, `0x004C4EF8`, and `0x004C5190` explicitly name
`D3DVT_TLVERTEX`. Those known submissions consume transformed/lit vertices,
so their relevant transforms are game code. Three sites do not prove that no
Direct3D view state exists anywhere in the program.

### Terrain-query census

Thunk `0x00401659 -> 0x004AC460` has exactly seven direct calls:

| Call | Containing function | Disposition |
|---|---|---|
| `0x004329E9` | `0x00432930` | known reset consumer |
| `0x004336D5` | `0x004336A0` | unmapped |
| `0x00433BA2` | `0x00433900` | known City dispatcher |
| `0x0043507E` | `0x00434E10` | unmapped; enclosing function reads Flik |
| `0x00437AD9` | `0x00437A20` | known reset consumer |
| `0x0043E716` | `0x0043E6B0` | unmapped |
| `0x0044085A` | `0x0043F9E0` | unmapped; enclosing function reads Flik |

After the two reset consumers and known City dispatcher are removed, four
functions remain unmapped. Exactly two of those enclosing functions read
live Flik coordinates: `0x00434E10` at `0x00435912`/`0x00435920`, and
`0x0043F9E0` at `0x004409BB`-`0x004409DB`. Their query arguments are not
thereby Flik's live point: the call at `0x0043507E` follows a constant-X and
`EBP`-Y overwrite of global block `0x0059D910`, while `0x0044085A` receives
the function's `ESI` object.

## Evidence classes and limits

- **Confirmed:** exact calls, thunks, reads, writes, flag-selected copies,
  angle-to-matrix output, render consumption, scratch-matrix load, local
  fixed-point transform, viewport instruction boundaries, three known
  TL-vertex submissions, and the seven/four/two terrain counts above.
- **Inferred:** `0x0059DD90` is the ordinary follow-camera source;
  `0x0059A5C0` is a scripted/setpiece source; the selector bit's gameplay
  meaning; the player-facing term “camera” for every path in the structural
  chain.
- **Unknown:** manual camera controls on PC; the semantic role of the local
  `0x0043D486 -> 0x00455710` call; update frequency; all indirect callers;
  and whether Direct3D view state exists outside the three known TL-vertex
  submissions.

## Reproduction commands

```bash
sha256sum work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x414540 --stop-address=0x4145b0 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x41acc0 --stop-address=0x41adf0 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x41adf0 --stop-address=0x41b5c8 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x41b7d0 --stop-address=0x41b970 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x455710 --stop-address=0x455920 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x4636c0 --stop-address=0x463760 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x463c80 --stop-address=0x463e53 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x405fe0 --stop-address=0x406120 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x423e70 --stop-address=0x423f80 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe | \
  rg 'call.*0x401659|call.*0x401848'
```
