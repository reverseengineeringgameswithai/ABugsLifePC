# R2n PC state-equivalence read-candidate trace

## Evidence identity

- Retail executable: `work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe`
- Retail SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Auto-hardware executable: `work/copies/auto-hardware/bugs.exe`
- Auto-hardware SHA-256: `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`
- Image base: `0x00400000`
- `.text`: VA `0x00401000`, file offset `0x00000400`
- Checked Ghidra export SHA-256: `db2dc35a8dcbc9138a318b5ca07bdc1e5ac2703c5760b7b99207a29703c67f5d`
- Predecessor camera trace SHA-256: `d96e6b52936ef9b32011a49426ce34ff1bae1668d160599d02cab976b956db3d`

This is offline PC-static evidence. It launches no target, reads no process
memory, writes no DAT or executable, and authorizes no later runtime action.
The Ghidra export is a search surface only; every admitted range below is
cross-checked against native retail instructions.

## Auto-hardware address rebind

Recent R2 arms execute the auto-hardware build, not retail. Direct comparison
proves both files are exactly `1,069,056` bytes and their PE section tables,
sizes, VMAs, and file offsets are identical. Global `cmp -l` reports only nine
changed physical bytes: eight within the startup patch at file
`0x000A6C6B..0x000A6C73` and one relocation byte at `0x000FA913`. The code
span is VA `0x004A786B..0x004A7873`; it does not overlap any instruction or
data locator in this trace. All other physical bytes, including every cited
consumer instruction, are identical. This binds the addresses below to both
exact hashes without claiming behavioral equivalence beyond those unchanged
ranges.

## Exact phase anchors

These candidates are coherent only at named instruction boundaries:

- **Upstream completion:** PC `0x00414585`, immediately after return from
  `0x00414580 -> 0x0041B7D0` and before the common-block transform call at
  `0x0041458A`. Compare selector bit, common input, and live coordinates here.
- **Generated-view completion:** PC `0x0041458F`, immediately after return
  from `0x0041458A -> 0x00455710` and before subsequent main-loop calls.
  Compare generated matrix, origin, copied matrix, and optional derived origin
  here.

An asynchronous `/proc` poll has no supported equality meaning because the
renderer temporarily mutates origin-family globals and repeatedly reloads
scratch. A later protocol must stop at the exact owned-process PC and define
one coherent read operation; this packet authorizes neither action.

## Admitted equality candidates

All intervals are half-open. Widths are exact static bounds, not permission to
read them.

| Phase | Range | Width | Static role and evidence |
|---|---|---:|---|
| upstream | `[0x0059A5EE,0x0059A5EF)` | 1 | Read one byte but compare bit 0 only. `0x0041B8AD` reads it and `0x0041B8B7` selects the copy branch. Multiple writers exist; no gameplay-mode name is assigned. |
| upstream | `[0x00599C90,0x00599CA2)` | 18 | Three dwords plus three words written by the two branches at `0x0041B8D1..0x0041B906` / `0x0041B931..0x0041B966`, then consumed by `0x00455710`. Other writers include `0x0041AB40` and `0x004341DF` at `+4`, so only the named phase is admitted. |
| upstream | `[0x0059D910,0x0059D91C)` | 12 | Confirmed live Flik-coordinate triplet, not complete player state. Direct writer functions are `0x0042DDB0`, `0x00433900`, `0x00434E10`, `0x00436170`, and `0x004388B0`; `0x0041ADF0` is one confirmed consumer. Equality means coordinate equality only. |
| generated | `[0x005B58E0,0x005B58F2)` | 18 | Nine signed matrix words written through `0x00455799 -> 0x00463C80` at `0x00463D55..0x00463E48`, with selector-1 conditional modifications inside `0x00455710`; consumed at `0x0044D4C1 -> 0x004636C0`. |
| generated | `[0x005BDB8C,0x005BDB98)` | 12 | Three input-position/origin dwords written at `0x00455894/0x0045589D/0x004558A5`; `0x004A3990` subtracts them from render-object coordinates. `0x0044D430` temporarily rewrites/restores them, so asynchronous polling is excluded. |
| generated | `[0x005BDBAC,0x005BDBBE)` | 18 | Nine-word matrix copy. `0x00455910` performs the physical copy; `0x004A3990` reads exactly nine signed words at `0x004A3A22..0x004A3AB0`. |

The main-path ordering supports these as two provenance-linked snapshots. It
does not prove an exhaustive camera, player, animation, input, or frame state.

## Optional redundant derived-origin candidate

At the generated-view phase, `[0x005BDB9C,0x005BDBA8)` is an optional 12-byte
candidate. `0x00455710` writes position divided by 32 at
`0x004558C0`/`0x004558DC`/`0x004558FD`; `0x004498F0` supplies this block to
`0x0045A7F0`. Renderer `0x0044D430` also mutates it, so it is not safe outside
PC `0x0041458F`. Its equality is redundant and carries no new semantics.

## Why the copied matrix stops at 18 bytes

`0x004558B1` sets `ECX=8` and `0x00455910` executes `rep movsd`, so the
physical copy spans 32 bytes `[0x005BDBAC,0x005BDBCC)`. That does not give
all 32 bytes one semantic role. The independently traced consumer
`0x004A3990` reads only nine words through `0x005BDBBC`, ending at exclusive
address `0x005BDBBE`. Bytes `+0x12..+0x13` remain unknown; `+0x14`, `+0x18`,
and `+0x1C` are dwords consumed by `0x00463740` as translations and mutated in
the renderer. They are excluded from matrix equality.

## Rejected broad render-scratch candidate

`0x004636C0` sign-extends matrix words into three noncontiguous 12-byte rows
at `0x0063E888`, `0x0063E898`, and `0x0063E8A8`. `0x00463740` separately
writes a fourth 12-byte translation span at `0x0063E8B8`.

These are real transform values but not persistent state anchors. Renderer
`0x0044D430` and other callers repeatedly invoke both loaders with different
inputs. `0x00405FE0` locally consumes the scratch matrix and translations from
`0x0040605F`; `0x0045A7F0` is not its caller and does not directly consume
`0x005B58E0`, although it independently reads the expanded scratch at 14
recorded base-row sites plus translations. Without the exact predecessor load
and exact target-record dispatch, arbitrary scratch equality is
nondiscriminating. No broad range beginning at `0x0063E888` is admitted.

## Future fail-closed boundary

A later experiment may propose the admitted ranges only after a separate
committed protocol, fresh James audit, and fresh explicit user authorization.
It must bind the exact auto-hardware hash, exact PC completion anchors, owned
process identity, stop/read lifecycle, coherent read receipts, and the
retail-to-derived address proof above. It must require exact cross-arm byte
equality and exact within-snapshot equality of the two nine-word matrix
copies. Any mismatch rejects state equivalence; no nearest state,
normalization, tolerance, asynchronous polling, or post-hoc expansion is
allowed.

Even complete equality proves only equality of these bounded values at the
sampled boundaries. It does not prove face 8 is in view or unoccluded,
establish terrain/material/collision semantics, rescue R2l, or authorize a
localizer or candidate arm.

## Native locators

| VA | File offset | Use |
|---|---:|---|
| `0x00414585` | `0x00013985` | upstream completion PC |
| `0x0041458F` | `0x0001398F` | generated-view completion PC |
| `0x0041B8AD` | `0x0001ACAD` | selector-byte read |
| `0x0041B8D1` | `0x0001ACD1` | first common-block copy arm |
| `0x0041B931` | `0x0001AD31` | second common-block copy arm |
| `0x00455710` | `0x00054B10` | common-block transform consumer |
| `0x00455910` | `0x00054D10` | eight-dword physical copy |
| `0x0044D4C1` | `0x0004C8C1` | renderer matrix-load call site |
| `0x0044D4F0` | `0x0004C8F0` | renderer origin/matrix-copy call site |
| `0x004636C0` | `0x00062AC0` | nine-word sign-extension loader |
| `0x00463740` | `0x00062B40` | translation-scratch loader |
| `0x004A3990` | `0x000A2D90` | origin/matrix-copy consumer |
| `0x004A3A22` | `0x000A2E22` | first copied-matrix word read |

## Reproduction

```bash
python scripts/ghidra-query.py xrefs --to 0x005B58E0
python scripts/ghidra-query.py xrefs --to 0x005BDB8C
python scripts/ghidra-query.py xrefs --to 0x005BDBAC
python scripts/ghidra-query.py function --addr 0x00455710
python scripts/ghidra-query.py function --addr 0x0044D430
python scripts/ghidra-query.py function --addr 0x004A3990
cmp -l work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe \
  work/copies/auto-hardware/bugs.exe
objdump -d -Mintel --start-address=0x455710 --stop-address=0x455920 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x44d430 --stop-address=0x44d520 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x4a3990 --stop-address=0x4a3ad0 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
```
