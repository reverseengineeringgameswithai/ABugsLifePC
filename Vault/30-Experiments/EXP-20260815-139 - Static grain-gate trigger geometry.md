---
type: experiment
id: EXP-20260815-139
date: 2026-08-15
question: 'What are the exact static trigger centers, radii, and state mechanics for every Tunnels row and City Entrance grain gate?'
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static analysis; radare2 5.9.8 and raw byte reads
environment_version: radare2 5.9.8
working_directory: /home/dev/ABLPC
configuration: read-only disassembly and byte dumps of the exact retail work copy; no runtime process, no target write, no asset access
artifacts:
  - scripts/coordinate-overlay.py
  - tests/test_coordinate_overlay.py
addresses:
  - "0x00416580"
  - "0x00432B30"
  - "0x00432EEC"
  - "0x00432EF8"
  - "0x00432F49"
  - "0x00432F85"
  - "0x00432F9D"
  - "0x00432FEB"
  - "0x00433017"
  - "0x0043301E"
  - "0x00433790"
  - "0x004337EF"
  - "0x00433900"
  - "0x0043392F"
  - "0x00433944"
  - "0x0043394C"
  - "0x00433962"
  - "0x0043396A"
  - "0x0043397F"
  - "0x004DA9C8"
  - "0x004DAB38"
  - "0x0059F020"
  - "0x0059F030"
file_offsets:
  - "0x15980"
  - "0x322EC"
  - "0x322F8"
  - "0x32349"
  - "0x32385"
  - "0x3239D"
  - "0x323EB"
  - "0x32417"
  - "0x3241E"
  - "0x32BEF"
  - "0x32D2F"
result: static-geometry-extracted-and-cross-checked-against-accepted-runtime
created: 2026-08-15T23:55:00
updated: 2026-08-15T23:55:00
tags:
  - re/experiment
  - re/static
  - re/gameplay
---

# EXP-20260815-139 - Static grain-gate trigger geometry

## Question

What are the exact static trigger centers, radii, and state mechanics for
every Tunnels row and City Entrance grain gate, so a gate-by-gate mapping
pass can proceed without walking blind? This packet is offline static
analysis only; it launches no game process and writes nothing to a target.

`.text` virtual addresses map to file offsets as `VA - 0x400C00`, the same
relation already pinned by [[PC grain gate threshold mod]]
(`0x004337D1 <-> 0x32BD1`). Every instruction cited below was decoded by
radare2 5.9.8 and independently re-read as raw bytes at its computed file
offset from the hash-verified retail work copy.

## City Entrance trigger geometry (three static call sites)

`0x00433900` makes exactly three calls to shared gate routine `0x00433790`
through thunk `0x00401D52` (EXP-136). All arguments are immediates. The
push block spans VA `0x0043392F`–`0x00433984`, file offset `0x32D2F`, raw
bytes:

```
6a 03 6a 02 6a 20 6a e0 6a 50 68 06 30 fd ff 68 27 ea fe ff 53
e8 09 e4 fc ff 83 c4 20
6a 05 6a 04 6a de 6a 2c 6a 5a 68 b8 89 00 00 68 ef 66 05 00 6a 01
e8 eb e3 fc ff 83 c4 20
6a 01 53 6a 20 6a e4 6a 64 68 c4 bb 04 00 68 7f e2 08 00 6a 02
e8 ce e3 fc ff 83
```

Decoded per gate (cdecl, arg1 pushed last; `ebx = 0` throughout):

| Gate | Call VA | arg1 index | arg2 X | arg3 Z | arg4 r | arg5 delta_a | arg6 delta_b | arg7 slot_a | arg8 slot_b |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | `0x00433944` | 0 | -71129 (`0xFFFEEA27`) | -184314 (`0xFFFD3006`) | 80 | -32 | +32 | 2 | 3 |
| 1 | `0x00433962` | 1 | 354031 (`0x566EF`) | 35256 (`0x89B8`) | 90 | +44 | -34 | 4 | 5 |
| 2 | `0x0043397F` | 2 | 582271 (`0x8E27F`) | 310212 (`0x4BBC4`) | 100 | -28 | +32 | 0 | 1 |

Inside `0x00433790`:

- arg1 indexes the per-gate state dword at `0x0059F020 + index*4`; only
  state `-1` reaches the trigger test (`cmp` at `0x00433798`).
- arg2/arg3 are copied into a Flik-layout local (X at `+0x00`, Z at
  `+0x08`); the local's address, `0x0059D910` (live Flik XYZ, EXP-128),
  and arg4 are passed to proximity helper thunk `0x00401A37 -> 0x00416580`.
- On trigger with sufficient grain, state is set to `0x20` at
  `0x004337EF` (file `0x32BEF`, bytes `c7 04 b5 20 f0 59 00 20 00 00 00`)
  and decremented once per update at `0x0043384A`; while positive,
  animation dwords `0x0059F030 + slot_a*4` and `+ slot_b*4` accumulate
  `delta_a`/`delta_b` per update.
- The grain comparison (`0x004337D1`, retail `10 * (index + 1)`) runs only
  after the proximity test passes.

## Proximity helper `0x00416580`

Thunk `0x00401A37` jumps to `0x00416580` (file `0x15980`, 59 bytes,
raw-verified). It is exactly:

```
dx = (a->x - b->x) >> 8        ; sar, arithmetic
dz = (a->z - b->z) >> 8
return (dx*dx + dz*dz) < (r*r) ? 1 : 0
```

Effective planar world radius is therefore approximately `r << 8`:
gate 0 about 20480, gate 1 about 23040, gate 2 about 25600 units. Y is not
read.

## Tunnels trigger geometry (`0x00432B30`)

The nine-row loop (`esi += 5` dwords, bound `0x2D`) over the 20-byte
records at `0x004DA9C8` (type `+0x00`, unknown `+0x04`, requirement
`+0x08`, X `+0x0C`, Z `+0x10`; values re-verified identical to EXP-136):

- Only rows with type `0x10C7` (cmp at `0x00432EF8`, file `0x322F8`) are
  candidate closed gates.
- Grain is compared first (byte load at `0x00432F0C`, compare at
  `0x00432F12`); with sufficient grain, inline
  proximity math identical in form to `0x00416580` (sar 8, squared sum)
  compares against constant `0x2710` = 10000 = 100^2 at `0x00432F49`
  (file `0x32349`, bytes `81 fa 10 27 00 00`). The open radius is the
  same for all nine rows: about `100 << 8` = 25600 world units.
- With insufficient grain, the same math compares against `0x640` = 1600 =
  40^2 at `0x00432FEB` (file `0x323EB`): the "need more grain" message
  radius is about `40 << 8` = 10240 units.
- Opening sets the row type to `0x1068` (`edi` load at `0x00432EEC`);
  each later update, any row with type greater than `0x708`
  (`0x00433017`) adds `-140` (`0x0043301E`, bytes `05 74 ff ff ff`).
  `0x1068` - 18*140 = `0x690`, where the countdown stops. This exactly
  reproduces EXP-137's observed row-3 lifecycle `0x10C7 -> 0x0690`.
- Row coupling: the row-0 open branch also writes `0x1068` into row 4's
  type at `0x004DAA18` (`0x00432F85`, file `0x32385`, bytes
  `89 3d 18 aa 4d 00`); the row-4 branch writes row 0's type at
  `0x004DA9C8` (`0x00432F9D`, file `0x3239D`, bytes `89 3d c8 a9 4d 00`).
  This is the exact static form of the EXP-136 rows-0/4 link.

A separate 16-byte-stride table at `0x004DAB38` (X, Z, pre-squared
threshold `0x1000`, zone value) feeds `0x0059EFE8` earlier in the same
function using `sar 10` distance math. It selects a region value, not a
gate; it is recorded here only so the two tables are not conflated.

## Cross-checks against independently accepted runtime evidence

Applying the extracted predicates (Python `>>` on negatives matches x86
`sar`) to the exact coordinates accepted in EXP-137/EXP-138:

- Tunnels row 3 `(509676,510143)` vs known walkable `(501696,·,494016)`:
  `dx = -32`, `dz = -63`, sum `4993 < 10000` — inside the open radius,
  and `4993 >= 1600` — outside the message radius. EXP-137 opened the
  gate from exactly this point.
- City gate 0 `(-71129,-184314)` vs accepted trigger
  `(-87622,·,-182181)`: `dx = -65`, `dz = 8`, sum `4289 < 6400` — inside.
- City gate 0 vs the saved approach point `(-92603,·,-181281)`:
  `dx = -84`, `dz = 11`, sum `7177 >= 6400` — outside. EXP-137 recorded
  this point as visibly framing the gate while not triggering it.

Static geometry and the accepted runtime receipts agree at all three
tested points, including the inside/outside boundary between the two City
points. This is the required second evidence form for the predicate and
for gate 0's center; gates 1/2 centers and radii remain single-form static
facts until walked.

- City gate 0 animation `slot_a=2, slot_b=3, deltas -32/+32` times the
  state countdown from `0x20` reproduces EXP-137's observed intermediate
  `-128/+128` (4 updates) and terminal `-1024/+1024` (32 updates).

## Modified-profile invariance

The accepted EXP-136 profile
(`69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b`)
changes only the two Tunnels requirement tables, 16 bytes at `0x004337D1`,
and 12 lookup bytes within the INT3 alignment pad at `0x004338B0`. None of
those ranges overlap
the call-site block, the helper, the radii constants, or the coordinates
above, so this geometry is byte-identical in retail and that profile.

## Overlay support

`scripts/coordinate-overlay.py` 1.3.0 adds an opt-in `--gates` readout for
the mapping pass: on internal level 3 it live-reads the nine resident rows
at `0x004DA9C8`; on internal level 4 it live-reads the three state dwords
at `0x0059F020` and uses the static centers above. It shows the nearest
mechanism, its requirement, live type/state, world distance versus
effective radius, and the engine-exact inside/outside verdict. The target
boundary widens from exactly-retail to exactly {retail, accepted EXP-136
profile}; reads remain `process_vm_readv` only. City requirements display
uses the retail formula on retail and a live read of the `0x004338B0`
lookup on the profile build. Regression tests pin the geometry constants,
the sar-exact predicate against the three cross-check points above, the
read plans, and the two-hash boundary.

## Interpretation

The full static candidate map for all twelve mechanisms (nine Tunnels
rows, three City gates) now exists with two-form byte evidence. What
static analysis still does not provide: safe walkable Y/approach
coordinates, the visible player-facing identity of each mechanism, and
physical modified-threshold behavior for the untested gates
([[Known Unknowns#KU-060 - Modified grain-gate physical transition]]).
Raw table centers must not be used as teleport destinations; follow
[[PC Flik teleport procedure]].

## Result

Static extraction complete and cross-checked. City gates 1/2 centers
`(354031,35256)` r=90 and `(582271,310212)` r=100 are new; all Tunnels
rows share open radius ~25600 and message radius ~10240; rows 0/4
coupling, type lifecycle, City state/animation arrays, and the shared
proximity predicate are pinned to exact bytes.

## Follow-up

- Researcher walking pass with the 1.3.0 `--gates` overlay to correlate
  each visible gate with its row/index and save safe approach coordinates.
- Physical threshold arms for City gates 1/2 and remaining Tunnels rows
  under [[Known Unknowns#KU-060 - Modified grain-gate physical transition]].
- Independent fresh-context audit complete:
  [[EXP-20260815-140 - Independent static gate geometry and overlay audit]]
  returns **ACCEPT** after rehash, raw-byte/disassembly re-verification, a
  binary-wide call-site census, an X/Z swap falsification test, recomputed
  cross-checks, a profile-invariance byte diff, and overlay read-only/
  two-hash boundary review.
