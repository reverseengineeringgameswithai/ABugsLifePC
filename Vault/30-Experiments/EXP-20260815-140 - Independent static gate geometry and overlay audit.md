---
type: experiment
id: EXP-20260815-140
date: 2026-08-15
question: Do EXP-139's static grain-gate geometry claims and the overlay 1.3.0 gate readout survive an independent offline hard-truth audit?
status: accepted
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static re-verification with radare2 5.9.8 and raw byte reads; no runtime process
configuration: fresh-context adversarial audit from the existing working tree; read-only toward all game media; no target launch, write, commit, or staging
artifacts:
  - scripts/coordinate-overlay.py
  - tests/test_coordinate_overlay.py
  - reimplementation/ablpc/grain_gate_mod.py
addresses:
  - "0x00401A37"
  - "0x00401D52"
  - "0x00416580"
  - "0x00432B30"
  - "0x00432EEC"
  - "0x00432EF8"
  - "0x00432F0C"
  - "0x00432F49"
  - "0x00432F85"
  - "0x00432F9D"
  - "0x00432FEB"
  - "0x00433017"
  - "0x0043301E"
  - "0x00433790"
  - "0x00433798"
  - "0x004337D1"
  - "0x004337EF"
  - "0x00433900"
  - "0x00433944"
  - "0x00433962"
  - "0x0043397F"
  - "0x004338B0"
  - "0x004DA9C8"
  - "0x004DAB38"
  - "0x0059D910"
  - "0x0059F020"
  - "0x0059F030"
result: accept-full-static-geometry-and-overlay-boundary
created: 2026-08-15
updated: 2026-08-15
tags: [re/experiment, re/static, re/audit]
---

# EXP-20260815-140 - Independent static gate geometry and overlay audit

## Verdict and authority

**ACCEPT.** This is an independent fresh-context audit of
[[EXP-20260815-139 - Static grain-gate trigger geometry]]. Every material
claim was re-derived from the repository: the executable was rehashed, every
cited file-offset byte string was re-read raw, every cited instruction was
independently disassembled, all cross-check arithmetic was recomputed, and
the overlay diff and gates were re-run. No game process, Wine process,
debugger, or target write was used; `originals/` was not touched; nothing
was committed or staged.

## Executable identity and mapping

`work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe` rehashes to exactly
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
at 1,069,056 bytes. The PE section table places `.text` at VA `0x401000`,
raw `0x400`, so the packet's `VA - 0x400C00` file-offset relation is exact.
The `.data` section (VA `0x4C1000`, raw `0xBFC00`) was used for the table
reads below with its own `VA - 0x401400` relation.

## City Entrance call sites re-derived

Disassembly of `0x00433900` shows `ebx` zeroed at `0x00433901` and exactly
three immediate-argument calls to thunk `0x00401D52` (`e9 39 1a 03 00`,
verified `jmp 0x433790`). A binary-wide `e8` census over all of `.text`
finds no other call to that thunk and no direct call to `0x00433790`:
the three sites at `0x00433944`, `0x00433962`, `0x0043397F` are the complete
caller set. The push block raw bytes at file `0x32D2F` match the packet's
quoted string byte for byte.

Decoding with cdecl right-to-left push order (arg1 pushed last), the tuples
`(index, x, z, radius, delta_a, delta_b, slot_a, slot_b)` are exactly
`(0, -71129, -184314, 80, -32, +32, 2, 3)`,
`(1, 354031, 35256, 90, +44, -34, 4, 5)`, and
`(2, 582271, 310212, 100, -28, +32, 0, 1)`; I independently converted every
immediate (`0xFFFEEA27`, `0xFFFD3006`, `0x566EF`, `0x89B8`, `0x8E27F`,
`0x4BBC4`).

The X/Z assignment was attacked directly. Inside `0x00433790`, tracing exact
stack offsets shows arg2 stored at local `+0x00` and arg3 at local `+0x08`
(the `mov [esp+0x18], ecx` after three pushes resolves to local `+0x08`);
helper `0x00416580` reads `+0x00` and `+0x08` of both structs, and the live
Flik base `0x0059D910` passed as the first argument has X at `+0x00` and Z
at `+0x08` per EXP-128. A deliberate swap test falsifies the alternative:
with X/Z exchanged, the accepted EXP-137 trigger point computes shifted
`dx = 377`, far outside `80^2`, contradicting the accepted inside receipt;
the Tunnels swap yields 4,933, not the receipt's exact 4,993. The claimed
assignment is the only one consistent with the independently accepted
runtime evidence.

Routine mechanics verified in the decode: `cmp dword [esi*4+0x59F020], -1`
at `0x00433798` with `jne` past the trigger test (only state `-1` proceeds);
proximity called and tested at `0x004337CD` **before** the grain comparison
at `0x004337D1`; state set to `0x20` at `0x004337EF` (raw bytes
`c7 04 b5 20 f0 59 00 20 00 00 00` at file `0x32BEF`); decrement at
`0x0043384A` while positive; animation dwords `0x0059F030 + slot*4`
accumulate `delta_a`/`delta_b` (slot_b confirmed via `[esp+0x38]` = arg8).

## Proximity helper re-derived

Thunk `0x00401A37` jumps to `0x00416580`; the 59 bytes at file `0x15980`
match the packet exactly and decode to precisely
`dx = (a->x - b->x) >> 8` (sar), `dz = (a->z - b->z) >> 8`,
`return (dx*dx + dz*dz) < (r*r)` via `setl` — strict signed less-than, Y
never read. Effective radii approximately `r << 8` (20480/23040/25600) are
correctly hedged as approximate.

## Tunnels loop re-derived

In `0x00432B30` (prologue zeroes `ebp`), the nine-row loop uses stride
`add esi, 5` with bound `cmp esi, 0x2D`. Verified against raw bytes at their
computed offsets: type filter `cmp eax, 0x10C7` at `0x00432EF8`
(file `0x322F8`), `mov edi, 0x1068` at `0x00432EEC` (file `0x322EC`), grain
byte load/compare at `0x00432F0C`/`0x00432F12` **before** the inline sar-8
distance math, open threshold `cmp edx, 0x2710` at `0x00432F49`
(file `0x32349`), message threshold `cmp edx, 0x640` at `0x00432FEB`
(file `0x323EB`), cross-writes `mov [0x4DAA18], edi` at `0x00432F85`
(file `0x32385`) on the row-0 branch (`cmp esi, ebp`) and
`mov [0x4DA9C8], edi` at `0x00432F9D` (file `0x3239D`) on the row-4 branch
(`cmp esi, 0x14`), decay gate `cmp eax, 0x708` at `0x00433017`
(file `0x32417`) and `add eax, -140` at `0x0043301E` (file `0x3241E`).
`0x1068 - 18*140 = 0x690` recomputed. The nine 20-byte rows read from
`.data` at `0x004DA9C8` match EXP-136's table exactly, all type `0x10C7`.

The separate table at `0x004DAB38` was independently confirmed as a
16-byte-stride, `-1`-terminated zone selector (`add edx, 0x10`, sar-10
math, per-row pre-squared threshold `0x1000` at `+0x08`, zone value `+0x0C`
written to `0x0059EFE8`) — correctly recorded as not a gate table.

## Cross-check arithmetic recomputed

Python `>>` on negatives was explicitly checked equal to floor division by
256 (x86 `sar` semantics) for every operand used. Recomputed from scratch:

- Tunnels row 3 `(509676,510143)` vs walkable `(501696,494016)`:
  `(-32)^2 + (-63)^2 = 4993`, inside `0x2710`, outside `0x640`.
- City gate 0 vs accepted trigger `(-87622,-182181)`:
  `(-65)^2 + 8^2 = 4289 < 6400` — inside.
- City gate 0 vs saved approach `(-92603,-181281)`:
  `(-84)^2 + 11^2 = 7177 >= 6400` — outside.

All three coordinates were re-read from the tracked
`dynamic/wine/EXP-20260815-137-receipt.md`, whose animation receipts
`(0,0,-128,128,0,0)` then `(0,0,-1024,1024,0,0)` independently confirm
gate 0's slots 2/3 with deltas `-32/+32` over the `0x20` state countdown
(4 then 32 updates). The static predicate reproduces the accepted
inside/outside boundary of
[[EXP-20260815-137 - Modified grain-gate threshold behavior]] /
[[EXP-20260815-138 - Independent modified grain-gate threshold audit]]
at all three points.

## Modified-profile invariance verified

An existing ignored profile build
(`work/copies/bugs-grain-gates-test-123-1to9.exe`) rehashes to the accepted
`69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b`.
A full byte diff against retail shows exactly 46 changed bytes in exactly
the ranges pinned by `reimplementation/ablpc/grain_gate_mod.py`: 16 bytes at
file `0x32BD1` (VA `0x004337D1`), 12 bytes at file `0x32CB0`
(VA `0x004338B0`, inside a longer INT3 pad, holding lookup dwords
`(1,2,3)`), and the 18 requirement dwords at `+0x08` in both Tunnels tables.
Programmatic overlap testing against every geometry-bearing range (call-site
block, helper, Tunnels loop code, state write, table type/X/Z fields)
returns no overlap. The geometry is byte-identical in retail and the
accepted profile, as claimed by [[PC grain gate threshold mod]].

## Overlay 1.3.0 audit

`git diff scripts/coordinate-overlay.py tests/test_coordinate_overlay.py`
reviewed in full:

- No write path exists: the only backend remains `process_vm_readv`; no
  `process_vm_writev`, `ptrace`, attach, signal, or `/proc/*/mem` use.
- The identity boundary changed from pinned-retail to
  `ALLOWED_EXECUTABLE_SHA256S = {retail, accepted EXP-136 profile}`;
  `ev.ownership_proof(expected_sha256=None)` still enforces Wine loader,
  cmdline, and `work/copies/` cwd checks and always hashes the executable,
  and any other hash raises before memory access — fails closed.
- Short reads raise: `read_many` rejects `received != expected`, plans of
  0 or >32 ranges, and nonpositive/oversized addresses.
- Constants match the verified evidence: table/state addresses, thresholds,
  the three City tuples, retail requirements `(10,20,30)`, and the
  `engine_gate_distance_sq` predicate with Python arithmetic `>>`.
- Adversarial cases checked: unknown hash in `resolve_city_requirements`
  yields `(None,None,None)` with zero reads (defense in depth behind the
  identity refusal); levels other than 3/4 return no gate and perform no
  reads; nearest-selection ties resolve deterministically to the lowest
  index via strict `<`; the strict `<` inside-verdict matches the engine's
  `setl`/`jge` at exact equality; negative-coordinate shifts are covered by
  the pinned boundary-point tests; the City lookup at `0x004338B0` is read
  only on the exact profile hash and never on retail; the default readout
  without `--gates` is unchanged (gate text and the startup requirement
  read are both gated on the flag).

## Gates and hygiene

- `.venv/bin/python -m pytest tests/test_coordinate_overlay.py -q`:
  14 passed.
- `make check`: Vault lint 403 notes / 0 errors / 0 warnings, M4
  compatibility statement valid (5 hash anchors), 596 tests passed,
  tracked-file audit 0 violations.
- `git diff --check`: clean. Nothing staged; untracked files are three
  Vault notes only; no game-bearing bytes newly tracked; `originals/`
  contains no tracked content and was not modified; no EXP-139 runtime
  artifacts exist under `dynamic/` or `work/copies/`, consistent with the
  offline-static-only claim.

## Overclaim review

[[PC grain gate requirements]], [[PC grain gate threshold mod]],
[[FUNC-97C95BA5572D-00433790]], [[FUNC-97C95BA5572D-00432B30]],
[[FUNC-97C95BA5572D-00416580]], KU-060, Current State, MOCs, and the worker
session note were read against the evidence. City gates 1/2 are presented
only as single-evidence-form static facts with no physical claim; KU-060
remains open for every unwalked mechanism; M3 remains Complete and no
milestone is reopened; static centers are consistently barred from use as
walkable points or teleport destinations. The
[[EXP-20260815-136 - Tunnels and City Entrance grain-gate requirements]]
lineage is cited accurately throughout.

Minor observations, not defects: EXP-139 cites `0x00432F0C` (the grain
load) as the start of the grain comparison whose `cmp` is at `0x00432F12`,
and the `0x004338B0` INT3 pad extends beyond the 12 bytes the mod uses;
both wordings describe the load-bearing facts accurately.

## Accepted boundary

Accepted as static facts with two-form byte evidence: the three City call
tuples and their state/animation mechanics, the shared proximity predicate,
the Tunnels thresholds/lifecycle/cross-writes, and the profile invariance.
The predicate and gate 0's center additionally carry accepted runtime
agreement. Gates 1/2 centers/radii and all unwalked Tunnels rows remain
static-only until walked under
[[Known Unknowns#KU-060 - Modified grain-gate physical transition]]; no
physical behavior is claimed for them, and this audit adds none.
