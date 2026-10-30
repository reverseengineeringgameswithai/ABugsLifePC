---
type: experiment
id: EXP-20260816-141
date: 2026-08-16
question: 'Can the exact PC terrain height pipeline be reimplemented offline and used to compute candidate teleport standoff coordinates for all twelve grain gates?'
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static analysis; radare2 5.9.8; repository Python 3.14
environment_version: radare2 5.9.8
working_directory: /home/dev/ABLPC
configuration: read-only disassembly, raw byte reads, and asset reads from the exact retail work copy; no runtime process, no target write
artifacts:
  - reimplementation/ablpc/terrain_height.py
  - scripts/grain-gate-standoffs.py
  - tests/test_terrain_height.py
addresses:
  - "0x00401500"
  - "0x00401659"
  - "0x00401717"
  - "0x004329B4"
  - "0x004329E9"
  - "0x004329F1"
  - "0x004A8410"
  - "0x004A84FF"
  - "0x004A850A"
  - "0x004A85DF"
  - "0x004A8950"
  - "0x004A8A1A"
  - "0x004A8B28"
  - "0x004A8E96"
  - "0x004A9290"
  - "0x004AC460"
  - "0x004ACA60"
  - "0x004ACC3E"
  - "0x004ACD27"
result: engine-faithful-height-query-validated-at-four-receipt-points-and-twelve-standoff-candidates-computed
created: 2026-08-16T00:15:00
updated: 2026-08-16T00:15:00
tags:
  - re/experiment
  - re/static
  - re/file-format
  - re/gameplay
---

# EXP-20260816-141 - Engine-faithful terrain height and gate standoffs

## Question

The gate mapping pass wants Flik teleported to a viewing point "in front
of" each grain gate instead of a walked route. Static X/Z centers exist
for all twelve mechanisms ([[EXP-20260815-139 - Static grain-gate trigger geometry]]),
but the gate logic never stores a Y. Can the executable's own terrain
height computation be reimplemented offline, validated against accepted
runtime receipts, and used to compute a candidate standoff XYZ per gate?

This packet is offline static analysis and asset reads only. Exact inputs:
retail `bugs.exe` (hash above), `LEVEL03/TERRAIN.ALL` SHA-256
`b878c378c924fbdb45e450f4314808fdd3506f8685da2c3f255b7e316f4a2d9c`, and
`LEVEL04/TERRAIN.ALL` SHA-256
`9cf8fb6990a955a808f2e4f2c22ffce3fe5d62136f4a9271bdc444a6dd7fc103`, all
under `work/copies/BUGS_PC-full-disc`. `originals/` was not accessed.

## The engine height pipeline

The Level03 reset consumer `0x00432930` is the anchor: after selecting a
type-1 row it writes row X/Z shifted left five into the auxiliary triple
`0x0059D960/68`, sets `0x0059D964 = 0x7FFFFFFF`, calls thunk
`0x00401659 -> 0x004AC460` with the triple's address (push at
`0x004329BA`, call at `0x004329E9`), and stores actor Y as the returned
height minus `0x100` (`0x004329F1`). The pipeline behind that call:

- **Collector `0x004AC460`** copies the query block (x, y-0x600, z, w) to
  its stack, gathers candidate descriptor indices from a zone-bucket table
  at `0x007F128C`/`0x007FC8F0` (built by `0x004A8E96`), then for each
  candidate whose descriptor box at `+0x14/+0x1C/+0x24/+0x28` admits
  `x+0x1000`/`z+0x1000` with `+0x2000` slack and whose tag word `+0x2C` is
  nonzero, walks its payload groups and appends every cell whose group and
  cell windows admit the biased cell coordinates
  (`(x+0x1000-base) / 32` truncated toward zero). Cell windows are
  `+0x18/+0x1A` in X and `(byte +0x1E << 6) + word +0x0A` with span
  `(byte +0x1F + 4) << 6` in Z, each with `+0x100` slack.
- **Resolver thunk `0x00401717 -> 0x004ACA60`** walks the collected cells
  with unbiased local coordinates `(x-base) >> 5` (arithmetic shift). The
  sign of cell word `+0x02` selects the triangle winding; three half-plane
  tests through thunk `0x00401500 -> 0x004A9290` accept vertices
  `V0=(+0x06,+0x0A)`, `V1=V0+(+0x0C,+0x10)`, `V2=V0+(+0x12,+0x16)`. A
  contained cell's plane height is exactly
  `base_y + 4*((h0 << 3) - idiv(((z-z0)*A + (x-x0)*B) << 3, C))` with
  `B,C,A,x0,h0,z0` at words `+0x00..+0x0A` (`0x004ACC3E-0x004ACC7D`,
  `idiv` truncating toward zero).
- **Selection** (`0x004ACC80-0x004ACD27`): planes below the adjusted query
  height (`h < y-0x600`) compete for the maximum, tie-broken by greater
  `+0x02`; planes at or above compete for the minimum, winding-1 only.
  The maximum bucket wins when its cell's `+0x02` is negative; otherwise
  the minimum bucket. The winner plus `0xC80` is written back into the
  query block's Y and mirrored to `0x007F29A0`. Only when neither bucket
  produces a winner does the routine write the `0x80000000` failure
  sentinel into the query block's Y (`0x004ACDAB`).
- **Edge test `0x004A9290`** handles axis-aligned edges by direct
  comparison and general edges by an `idiv` cross-slope comparison whose
  major axis is chosen by `|dz| > |dx|`; all quotients truncate toward
  zero.

Every cited instruction was decoded with radare2 and re-read as raw bytes
at `VA - 0x400C00` in the hash-verified executable.

## Descriptor construction and bounds

Loader `0x004A8410` (clone branch `0x004A84FF-0x004A857D`): a record with
word `+0x46 == 1` copies the full `0x30`-byte descriptor of the record
registered under its `+0x44` template id, then substitutes its own base
tuple shifted left five; only non-clone records register template ids
(`0x004A85DF`). Level03 `TERRAIN.ALL` has 463 clones of 592 records;
Level04 has 58 of 233, so clones are the normal case and inherit payload,
tag, and result from their template.

Orchestrator `0x004A8950` selects file name `terrain`/`terr1`/`terr2`/
`terr3` by mode argument; EXP-131's live pointer join pins normal
gameplay to `TERRAIN.ALL`. Its bounds pass (`0x004A8A1A-0x004A8B60`)
recomputes every tag-6/7/8 descriptor's `+0x14/+0x1C/+0x24/+0x28` box
from **cell** fields: X from `+0x18` and `+0x18 + +0x1A`, Z from
`(byte +0x1E << 6) + word +0x0A` and
`(byte +0x1F << 12) + (byte +0x1E << 6) + word +0x0A`, each shifted left
five and rebased.

**Contradiction with EXP-131:** the EXP-131/[[PC TERRAIN ALL collision descriptor source]]
bounds table derived Z bounds from group-header words `+0x08/+0x0A`. For
Level03 descriptors 570-578 the X bounds agree exactly with the
loader-literal derivation, but the Z bounds do not (for example descriptor
570: loader-literal `z_min` 101632 versus the table's 98112, and much
wider spans). The instruction stream is unambiguous, and the EXP-131 table
was parser-derived rather than read from live descriptor memory, but per
policy the contradiction is recorded, not silently normalized. A future
runtime arm can settle it by reading descriptor 570's live
`+0x1C/+0x28` dwords. Wider boxes only admit more candidates into the
exact cell tests, and the receipt cross-checks below validate end-to-end
outcomes.

## Reimplementation and receipt validation

`reimplementation/ablpc/terrain_height.py` mirrors the pipeline bit-exactly
at that boundary on top of the lossless EXP-131 parser: 32-bit wrapping
arithmetic, toward-zero `idiv`, arithmetic shifts, the biased/unbiased
coordinate split, winding, tie-breaks, and the `+0xC80`/`-0x100` offsets.
Descriptors iterate in index order instead of bucket order. The
equivalence argument, corrected by EXP-142's attack: each descriptor
belongs to exactly one zone, but the bucket unions derive from
group-header extents while the phase-2 boxes are cell-derived, so
containment is not automatic. EXP-142's exhaustive scan of both modeled
retail files proves no cell window protrudes below its group extent
(the only possible seam is at most 31 units and unoccupied), so the
accepted cell set is identical for these exact files, and height ties
resolve to the same height either way (ties are surfaced as an
`ambiguous` flag). Two further documented boundaries: the live table may
append a second source family (`plantter.all`), so results are
terrain-surface heights; and the loader's `+0x10 >= 0x100` branch
(`0x004A84EB-0x004A84F4`) appends no descriptor at all, while the model
builds a height-ineligible descriptor instead — both retail files carry
such records only after every tag-6/7/8 record (Level03 records 589-591,
Level04 229-232, tags 257/260), so indices and query results are
unchanged (EXP-142).

Validation against independently accepted runtime receipts:

| Point | Level | Computed rest Y (`height - 0x100`) | Observed | Delta |
| --- | ---: | ---: | ---: | ---: |
| `(501696, 494016)` row-6 walkable (EXP-130) | 03 | **30092** | 30092 | **0** |
| `(497247, 547255)` natural reset endpoint (EXP-129) | 03 | 31176 | 31299 | +123 |
| `(-87622, -182181)` City trigger (EXP-137) | 04 | 796 | 917 | +121 |
| `(-92603, -181281)` City approach (EXP-137) | 04 | 972 | 1098 | +126 |

The row-6 point reproduces exactly because its accepted Y originated from
the engine's own reset placement; the other three receipts are settled
standing positions 121-126 units deeper. PC world Y therefore grows
**downward**: the nine Level03 result-1 reset surfaces (descriptors
570-578) rest near 64032, deeper than the ~30000-32000 walkable ground,
and a pit interior point `(500000, 522000)` matches only descriptor 572's
reset plane. The winning ground descriptor at the row-6 point is 552, the
same descriptor EXP-118/126 observed live in that area.

## Standoff candidates

`scripts/grain-gate-standoffs.py` (read-only, refuses unpinned terrain
files) evaluates 16 fixed integer directions per gate. Plane heights are
engine-exact; the selection policy is a documented tool-level heuristic:
reference ground = deepest result-0 plane at the gate center; per
candidate choose the result-0 plane closest to that reference, reject
candidates with a non-zero-result plane at or above the standing plane or
with 512-unit probes deviating beyond 512; rank by reference closeness,
flatness, direction order. Tunnels standoff distance is 16000 (outside
the 10240 message radius, inside the 25600 open radius — harmless at
grain 0); City distance is the effective trigger radius plus 1500.

| Gate | Requirement (retail) | Candidate standoff (x, restY, z) | Spread |
|---|---:|---|---:|
| T0 | 20 | (205067, 33916, 143005) | 104 |
| T1 | 10 | (489642, 32092, -451306) | 112 |
| T2 | 10 | (843615, 33812, 302388) | 100 |
| T3 | 10 | (495365, 32232, 502987) — prefer proven (501696, 30092, 494016) | 248 |
| T4 | 20 | (840401, 33940, 626583) | 152 |
| T5 | 20 | (1126934, 31480, 1308289) | 164 |
| T6 | 30 | (1471643, 32820, 1426369) | 192 |
| T7 | 10 | (1202034, 31492, 1970285) | 224 |
| T8 | 30 | (1646238, 33792, 2546125) | 100 |
| C0 | 10 | (-55587, -20, -168772) — prefer proven (-87622, 917, -182181) | 52 |
| C1 | 20 | (354031, 2540, 10716) | 208 |
| C2 | 30 | (601433, 1132, 329374) | 196 |

City gate 0's own center rests about 800 units above the proven approach
ground, so its computed candidate likely sits on the gate structure; the
independently accepted trigger/approach points remain the recommended C0
coordinates. All computed rows are **static candidates**: walkability is
proven only by the guarded live procedure ([[PC Flik teleport procedure]]
write/readback, survival, fresh state), and observed standing Y settles
121-126 units deeper than the written rest Y.

## Validation

- 14 new focused tests (synthetic plane/winding/tie/window/clone cases,
  toward-zero division, retail receipt points, EXP-131 bounds
  cross-check, pit orientation, deterministic complete standoff report);
- receipt points reproduce exactly as tabulated above;
- full `make check` passes with the complete suite and Vault gates.

## Result

The exact terrain height pipeline is reimplemented and validated at four
independently accepted receipt points, the world-Y orientation is pinned
(downward), and all twelve gates have deterministic candidate standoff
coordinates plus two proven runtime points. Remaining limits: plantter
family excluded, the EXP-131 Z-bounds contradiction awaits a live
descriptor read, and candidate walkability awaits the guarded teleport
arms.

## Follow-up

- Runtime session: guarded teleports to the candidate standoffs with the
  1.3.0 `--gates` overlay to label every visible gate and bank verified
  approach coordinates (KU-060 mapping pass).
- Optional live read of Level03 descriptor 570's `+0x1C/+0x28` to settle
  the EXP-131 Z-bounds contradiction (KU-061).
- Independent fresh-context audit (James) before this packet is accepted.

## 2026-10-12: descriptor 570 from the emulated original loader

- **Method.** Offline, with no game, the full original loader `0x004A8410`
  and the initializer slice `0x004A89F8`–`0x004A908F` ran through
  `scripts/terrain-retail-probe.py`'s `RetailProbe`. The slice includes the
  bounds pass at `0x004A8A1A`. Its input was the hash-checked retail
  `LEVEL03/TERRAIN.ALL` (`original_levels.read_inputs(cd, 3)`).
- **Values read.** 602 descriptors loaded. Descriptor 570 reads
  `+0x1C` = **101632** and `+0x28` = 2250208. Descriptors 571 and 578 read
  −452928 / 1706400 and 574752 / 2646816.
- **Conclusion.** The loader-literal derivation above is what the loader
  stores. EXP-131's table value, 98112, is a parser-side derivation and not
  the stored bound.
- **Remaining step.** A live read would add a third form; the original x86
  ran here, but in emulation.
- **Impact.** Low, as stated above: the box only pre-filters candidates,
  with `+0x2000` slack.
