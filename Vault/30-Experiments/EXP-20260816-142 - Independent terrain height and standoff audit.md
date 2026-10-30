---
type: experiment
id: EXP-20260816-142
date: 2026-08-16
question: Do EXP-20260816-141's terrain-height pipeline, reimplementation, receipt validation, and standoff claims survive an independent offline hard-truth audit?
status: accepted
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static re-verification with radare2 5.9.8, raw byte reads, and repository Python 3.14; no runtime process
configuration: fresh-context adversarial audit from the existing working tree; read-only toward all game media; no target launch, write, commit, or staging; tamper test performed only on a scratchpad copy
artifacts:
  - reimplementation/ablpc/terrain_height.py
  - scripts/grain-gate-standoffs.py
  - tests/test_terrain_height.py
addresses:
  - "0x00401500"
  - "0x00401659"
  - "0x00401717"
  - "0x004329B4"
  - "0x004329BA"
  - "0x004329E9"
  - "0x004329F1"
  - "0x004A8410"
  - "0x004A84EB"
  - "0x004A84FF"
  - "0x004A8519"
  - "0x004A85DF"
  - "0x004A865B"
  - "0x004A8950"
  - "0x004A8A1A"
  - "0x004A8B28"
  - "0x004A8E96"
  - "0x004A9290"
  - "0x004A93BA"
  - "0x004AC460"
  - "0x004ACA60"
  - "0x004ACC3E"
  - "0x004ACD27"
  - "0x004ACDAB"
result: accept-engine-faithful-height-boundary-with-three-recorded-latent-gaps
created: 2026-08-16
updated: 2026-08-16
tags: [re/experiment, re/static, re/audit]
---

# EXP-20260816-142 - Independent terrain height and standoff audit

## Verdict and authority

**ACCEPT.** This is an independent fresh-context audit of
[[EXP-20260816-141 - Engine-faithful terrain height and gate standoffs]].
Every material claim was re-derived from the repository: the executable
and both terrain files were rehashed, every cited pipeline function was
independently disassembled with radare2 5.9.8 and cross-read as raw bytes
at `VA - 0x400C00`, the reimplementation was reviewed line by line against
the fresh decode, all four receipt queries and the complete standoff
report were rerun, the hash refusal was tampered-tested on a scratchpad
copy only, and every hygiene gate was rerun. No game process, Wine
process, debugger, or target write was used; `originals/` and the work
copies were not modified; nothing was committed or staged.

## Identity and pipeline decode re-derived

`work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe` rehashes to the pinned
`97c95ba5...27b878` at 1,069,056 bytes; the PE section table places
`.text` at VA `0x401000`, raw `0x400`, so `VA - 0x400C00` is exact.
`LEVEL03/TERRAIN.ALL` and `LEVEL04/TERRAIN.ALL` rehash to the two pinned
digests. Thunks re-verified: `0x00401659 -> 0x004AC460`,
`0x00401717 -> 0x004ACA60`, `0x00401500 -> 0x004A9290`.

Confirmed by fresh disassembly, exactly as EXP-141 states:

- **Reset consumer `0x00432930`**: bit-`0x10` gate, nearest-row scan,
  selected X/Z shifted left five into `0x0059D960/68`,
  `0x0059D964 = 0x7FFFFFFF`, one call to `0x00401659` at `0x004329E9`
  with the triple's address, actor Y stored as result minus `0x100` at
  `0x004329F1`. (Precision: the pointer push is at `0x004329BA`;
  `0x004329B4` is the row-pointer load that opens the same setup block.)
- **Collector `0x004AC460`**: stack block `(x, y-0x600, z, w)`; `+0x1000`
  bias; phase-1 bucket records at `0x007F128C` (stride `0x14`, count
  `0x007F3D58`, word lists at `0x007FC8F0`); phase-2 unsigned box test at
  `+0x14/+0x1C` versus spans `+0x24/+0x28` with `+0x2000` slack, tag word
  `+0x2C` nonzero, payload `+0x10`, first group marker `>= 0`; biased
  cell coordinates via `cdq / and edx,0x1f / add / sar 5` (toward zero);
  group windows with `+0x100` slack; cell X window `+0x18/+0x1A`, cell Z
  window `(byte +0x1E << 6) + word +0x0A` with span
  `(byte +0x1F + 4) << 6` (the `+4` term *is* the `0x100` slack);
  accepted cells to `0x007F3F50`/`0x007F267E+2`, count `0x007FC8D4`;
  resolver call with the block address; returns the block's updated Y.
- **Resolver `0x004ACA60`**: unbiased per-descriptor locals
  `(x - base) sar 5` (floor — the deliberate contrast with the
  collector's biased toward-zero form is real); winding by the sign of
  cell word `+0x02`; edge orders re-derived from the push sequences:
  negative `V0->V1, V2->V0, V1->V2`, positive `V1->V0, V0->V2, V2->V1`,
  zero never contained; plane height exactly
  `base_y + 4*((h0 << 3) - idiv(((z-z0)*A + (x-x0)*B) << 3, C))` at
  `0x004ACC3E-0x004ACC7D`; planes with `h < y-0x600` compete for the
  maximum with the greater-`+0x02` tie-break (stored `0x5BD824/28`),
  others for the minimum, winding-1 only (`0x5BD818/1C`); the final
  block (`0x004ACD27`) selects the maximum only when saved word
  `0x5BD826` is negative, else the minimum, each `+0xC80`; else the
  `0x80000000` sentinel is written at `0x004ACDAB`.
- **Edge test `0x004A9290`**: all six branches match the
  [[FUNC-97C95BA5572D-004A9290]] table exactly, including both
  axis-aligned inequality directions, the `|dz| > |dx|` major-axis
  choice, and the four toward-zero `idiv` cross-slope forms; the shared
  pass epilogue at `0x004A93BA` carries `66 b8 01 00` at file `0xA87BD`.
- **Loader `0x004A8410` clone branch**: `+0x46 == 1` selects the clone
  path; `rep movsd` copies the registered template's full `0x30`-byte
  descriptor; the clone overwrites `+0x00/04/08` with its own base and
  `+0x0C` with its own dword `+0x10`, then shifts the base left five;
  only non-clone records with `+0x44 >= 0` register (`0x004A85DF`).
  Clone counts re-verified: Level03 463 of 592, Level04 58 of 233.
- **Bounds pass `0x004A8A1A-0x004A8B60`**: tag 6/7/8 filter; X from cell
  `+0x18` and `+0x18 + +0x1A`; Z from `(byte +0x1E << 6) + word +0x0A`
  and `(byte +0x1F << 12) + (byte +0x1E << 6) + word +0x0A`; mins/maxes
  shifted left five and rebased to `+0x14/+0x1C` with spans at
  `+0x24/+0x28` (writeback at `0x004A8B28`), inits
  `0x7FFFFFFF/0x80000000`, 700 slots, stride `0x30`.
- **Bucket builder (`0x004A8E96` and the pass before it)**: each tag-6/7/8
  descriptor receives exactly one zone word; per zone, one bucket record
  unions member minima/maxima and appends member indices to one word
  list; empty zones emit no bucket. The packet's exactly-one-zone claim
  is confirmed. See the equivalence finding below for what the union is
  a union *of*.

## KU-061 and receipt validation rerun

The loader-literal bounds recomputed through the reimplementation match
[[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]]'s
X table exactly for Level03 descriptors 570-578 and contradict its Z
table exactly as recorded: descriptor 570 loader-literal Z
`101632..2351840` versus the table's `98112..161088` (the `z_min`
101632-versus-98112 example in the packet and
[[Known Unknowns#KU-061 - Runtime descriptor Z-bounds derivation]] is
verified). The recorded-not-normalized handling is correct: the
`byte +0x1F << 12` term in the instruction stream is unambiguous, and
the EXP-131 table was parser-derived, never read from live memory.

Receipt queries rerun from scratch through the model:

| Point | Computed rest Y | Observed | Delta | Descriptor |
| --- | ---: | ---: | ---: | ---: |
| `(501696, 494016)` L03 | 30092 | 30092 | 0 | 552 |
| `(497247, 547255)` L03 | 31176 | 31299 | +123 | 543 |
| `(-87622, -182181)` L04 | 796 | 917 | +121 | 84 |
| `(-92603, -181281)` L04 | 972 | 1098 | +126 | 84 |

Provenance re-verified: the 30092/`(501696,494016)` Y originates from the
engine's own reset placement (EXP-20260815-116/117 both record control
row 6 producing exactly `(501696, 30092, 494016)` through this height
path), which is why it alone reproduces with delta 0; the other three are
settled standing samples (EXP-129 endpoint, both EXP-137 receipts). The
pit interior `(500000, 522000)` matches exactly one plane — descriptor
572, result 1, winding 1, rest 64032 — internally consistent with
downward-growing PC world Y (EXP-129's below-floor samples 68730/66713
against ~31000 floors agree independently).

## Bucket-order equivalence attacked

The packet's documented deviation (descriptor index order instead of
bucket order) was attacked directly, and its written justification is
imprecise in one step:

- Confirmed: each descriptor belongs to exactly one zone, and duplicates
  are impossible.
- **Misstated premise**: the bucket union is built from *group-header*
  boxes (words `+0x04..+0x0A`, the zone-assignment pass before
  `0x004A8E96`), not from the phase-2 *cell-derived* descriptor boxes.
  Because of the `<< 12` Z-max term, the phase-2 box is far wider than
  the group-derived union (589 of 592 Level03 and 225 of 233 Level04
  descriptors have cell-derived `z_max` above their group `z_max`), so
  "any descriptor passing phase-2's own box test is necessarily
  reachable through its zone's bucket" is not established by the union
  argument and is false as a general structural claim.
- **Conclusion nevertheless holds for these files**: what must be
  identical is the accepted *cell* set, and a cell is accepted only
  through the group and cell windows. On the upper edge the arithmetic
  is exact — the group windows' `+0x100` cell slack equals the bucket
  test's `+0x2000` world slack at the 32-unit scale, and floor
  truncation of nonnegative biased offsets closes the bound. The only
  possible divergence is a sub-32-unit lower-edge seam where the
  collector's toward-zero truncation of a *negative* biased offset
  rounds up: it requires a cell window protruding below every group
  window of the descriptor. An exhaustive scan of both files found
  **zero** cell-derived minima below the group-derived minima on either
  axis, so the seam is unoccupied and the engine and model accept
  identical cell sets at every query point for these two files.
- Tie ordering: the resolver tie-breaks re-derived above depend only on
  `(height, divisor)` values, so iteration order can change only the
  reported winning cell attributes when both tie exactly, never the
  returned height; the model surfaces exactly that case as `ambiguous`.

## Reimplementation fidelity

`reimplementation/ablpc/terrain_height.py` was compared line by line with
the fresh decode: 32-bit wrapping (`_i32` at every engine wrap point,
with modular-arithmetic equivalence for the fused products), toward-zero
`_idiv`, the `_trunc_div32` biased form versus the resolver's floored
`>> 5`, both winding edge orders, the floor/ceiling buckets and both
tie-breaks, the saved-divisor final selection, `+0xC80`, `-0x100`, the
clone construction, and the cell-derived bounds recompute (including the
`<< 12` term and the exact wrap order of the span writeback) are all
faithful. The `plantter.all` second-family exclusion is documented in
both the module docstring and the note. The half-plane test reproduces
all six disassembly branches.

## Standoff tool rerun

`scripts/grain-gate-standoffs.py`: read-only (JSON to stdout only); all
nine Tunnels centers/requirements match EXP-136's resident table and all
three City tuples match EXP-139's immediates; the selection policy is
labeled a documented tool-level heuristic in the docstring and the
engine/heuristic boundary is real in the code (plane enumeration
engine-exact, selection center-referenced). Two complete runs are
byte-identical, and all twelve chosen candidates reproduce the packet's
table exactly, including every spread value. T3/C0 carry their proven
points and the compact output prints them alongside. A tampered
`LEVEL03/TERRAIN.ALL` copy (scratchpad only; the work copy was never
touched) is refused before any model construction with exit 1.

## Gates and hygiene

- `.venv/bin/python -m pytest tests/test_terrain_height.py -q`: 14 passed.
- `make check`: Vault lint 410 notes / 0 errors / 0 warnings, M4
  compatibility statement valid (5 hash anchors), 610 tests passed,
  tracked-file audit 0 violations.
- `git diff --check`: clean. Working tree holds only source/tests/Vault
  changes; no game-bearing bytes are tracked; `originals/` untouched; no
  new receipts under `dynamic/` — consistent with the packet's
  no-runtime claim. Three `winedevice.exe` service stubs from the
  afternoon runtime sessions (started 17:39-18:02, hours before this
  packet's work) were observed still resident; they are prior-session
  residue, not packet runtime evidence, and are left for the owner
  session to close.

## Defects and latent gaps recorded

None of these change a validated height, receipt, candidate, or claim
boundary; the first is corrected in place, the rest are recorded for the
worker's reconciliation:

1. **Corrected in place** — [[FUNC-97C95BA5572D-004A8410]] said an
   unregistered-template clone "is skipped (`0x004A8519`)". The `jl` at
   `0x004A8519` branches to `0x004A865B`, raw bytes `eb fe` (file
   `0xA7A5B`): an infinite self-jump. The engine traps; it does not
   skip. The reimplementation raises `TerrainFormatError` — a fail-loud
   refusal, behaviorally equivalent in that neither produces a height —
   and neither retail file contains such a clone (verified: zero).
2. **Unmodeled loader branch** — records whose source dword `+0x10` is
   `>= 0x100` (signed compare at `0x004A84EB-0x004A84F4`) build *no*
   runtime descriptor in the engine (they take a separate
   `0x12345678`-marker registration path and do not advance the
   descriptor index or register templates). Both files contain such
   records — Level03 589-591, Level04 229-232 — and the model builds
   descriptors for them. Verified inert here: all are trailing records
   (no earlier index shifts), their tag words are 257/260 (never
   height-eligible, so `_collect` skips them at every coordinate), and
   no later clone consumes their template registrations. A hypothetical
   file with such a record *before* height-relevant records would
   misalign model indices; the module boundary should say so.
3. **Equivalence-argument wording** — the module docstring and note
   justify index order with "bucket boxes are unions of member boxes
   tested with the same slack"; the union is of group-header-derived
   boxes, and the phase-2 premise is false in general (see above). The
   conclusion stands for these files via the window-arithmetic argument
   plus the zero-protrusion scan; the wording should be tightened.
4. **Minor wording** — the standoff tool's docstring and report say
   standing Y settles "121-126 units above/higher" than rest Y; the
   observed values are numerically larger, which is *deeper* under the
   packet's own downward-Y result (the note and
   [[PC grain gate threshold mod]] already say "deeper" correctly).
   Also, EXP-141's Selection bullet ends "no candidate writes the
   `0x80000000` failure sentinel", which reads as an engine claim; the
   engine has a real sentinel path at `0x004ACDAB` (the sentence is true
   of the packet's evaluated query points). And the note cites
   `0x004329B4` for the pointer-argument call; the push is at
   `0x004329BA`.

## Accepted boundary

Accepted: the complete height-pipeline decode; the reimplementation as
engine-faithful **at the height-query interface for the two audited
retail terrain files** (every construction-internal deviation above is
proven unexercised or query-invisible for them); the four receipt
cross-checks with the row-6 exact match and its engine-origin
explanation; downward-growing PC world Y; the KU-061
contradiction-recording; and the twelve deterministic standoff
candidates as **static candidates only**, with T3/C0's proven points
preferred and C0's structure-top caveat retained. Candidate walkability,
visible gate correlation, and the untested physical thresholds remain
open under
[[Known Unknowns#KU-060 - Modified grain-gate physical transition]];
KU-061 remains open pending its one-read live discriminator; M3 remains
Complete and no milestone is reopened.
