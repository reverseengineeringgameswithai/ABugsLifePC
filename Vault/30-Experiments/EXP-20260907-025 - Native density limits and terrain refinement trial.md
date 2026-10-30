---
type: experiment
id: EXP-20260907-025
date: 2026-09-07
binary_sha256: 431ec953b67bd3233f8fa58e7a22edbfabaeb153e3ee322d760c45f2a44c7d8f
environment: Native PC instructions in Unicorn and guarded Wine hardware previews
question: Which native limits bound terrain mesh density, collision candidate collection and per-step movement, and does retessellating terrain preserve native collision outcomes?
result: Mesh faces carry unsigned 16-bit byte offsets into 12-byte rows (5462 vertices per mesh); 004AB1A0/004ABE00 append to the 400-entry collector at 007F3F50 without a bound check, 1600 bytes before descriptor storage; the movement envelope is a 3D delta <=10000 world units; broad retessellation changes native collision trajectories while flat-only refinement passes bounded gates
status: partial-acceptance
created: 2026-09-07
updated: 2026-10-29
evidence: [EXP-20260907-024, EXP-20260907-023]
tags: [experiment, implementation/modding, terrain/authoring, re/rendering]
---

# Native density limits and terrain refinement trial

This experiment measures the native limits that bound denser authored terrain:
mesh vertex addressing, the movement collision collector and the per-step
movement envelope, and tests whether retessellating terrain keeps native
collision outcomes. Full respawn/exit cycles, actor endurance, timed complete
traversal and uncapped hardware work-time headroom remain outstanding.

Canonical metrics/artifact hashes: `reports/terrain/EXP-20260907-025.json`.
Private reproducible scripts, native instruction traces and rejected candidates:
`work/experiments/EXP-20260907-025/`. All sources are PC; no PS1 consultation,
live memory writes, debugger stops or original-file changes.

## Native limits

**Confirmed, bounded:** positive-count PC mesh faces carry unsigned 16-bit byte
offsets into 12-byte vertex rows (`0045A7F0` consumer, existing `terrain_foliage`
encoder). Thus the maximum referenced row is 5461, offset 65532: 5462 vertices
per mesh. A single aggregate mesh is bound by that limit; a partitioned layout
must encode each chunk separately to carry more vertices in total.

**Confirmed:** `004AB1A0` and `004ABE00` append triangle pointers at `007F3F50`
without a 400-entry check in the collector loop. Descriptor storage starts at
`007F4590`, 1600 bytes later. Native disassembly and write observations are retained
in `native-bounds.asm` and the movement probes. The new `level_density` guard
computes a conservative X/Z overlap from packed cell admission windows across
resolved static tag6/7/8 and clone instances in TERRAIN and PLANTTER. It ignores
Y/group/descriptor rejection, enlarges windows by 514 stored units, and rejects
bounds above 300. The movement envelope is a **3D** delta length <=10000 world
units: `004AB1E5..004AB209` squares all three components, takes a square root and
adds 6272. The height query uses the smaller 128-unit envelope. The remaining
100 slots are a reserve, not a proof about arbitrary dynamic actors. Larger
velocities and integer-overflow behavior are not accepted.

## Bounded density measurements

A flat-ground refinement trial kept the same extent, boundary, slopes, cliff
faces, spawn and exit, and added exact interior lattice points only to flat
terrain faces (recipe `build-density.py`):

| Measurement | Control | Flat-ground trial |
| --- | ---: | ---: |
| Ground triangles | 2092 | 4566 |
| Authored collision triangles | 2365 | 4839 |
| Conservative static candidate bound | 103 | 161 |
| Largest observed grid candidate count | 27 | 53 |
| Vertices emitted across 12 native camera contexts | 31077 | 44097 |
| Object-render native instruction total, same contexts | 19733564 | 29411296 |
| Largest native batch | 499 | 499 |

Native renderer calls execute original PC instructions with only six D3D COM calls
stubbed. Both runs cover all four chunks and validate finite vertices, index ranges
and native batch flushing. This is native CPU work, **not GPU timing**. At two of the
cameras the emitted vertices increase 1284→5712 and 857→3770; object
render instruction counts increase about 2.14× and 2.01×. Added RAM does not remove
this per-frame work.

`native-seams.json`: 124 crossings, five landings and two exit-helper cases pass;
all seam trajectories match exactly. `native-wall-seams.json`: 24 grounded/airborne
wall pushes match exactly. `native-grid.json`: 138 interior routes, eight movement
steps each, maximum position difference 3 world units against the existing 32-unit
tolerance. Candidate-count writes are observed and rejected above 400. These are
isolated native fixtures, not full live actor/transition simulation. In live
hardware runs, all four dense mesh/collision chunks matched exact expected
resident bytes and 147 samples of all170 model payloads passed.

## Rejected counterexamples and implementation checks

1. Rounded centroids exceeded 45 degrees on an apron face; schema rejected the
   first attempt before encoding. Exact lattice points replaced rounded positions.
2. Broad exact-plane refinement changed one seam trajectory by 45 world units,
   exceeding the existing 32-unit tolerance. Grounded wall comparisons also differed
   by small amounts. Saved under `rejected-full-refinement/`.
3. Retaining seam-adjacent triangles made all seam/wall gates pass, but three wider
   interior routes still differed by 103/51/64 world units. Saved under
   `rejected-seam-preserving-refinement/`. That candidate was never launched.
4. Final flat-ground refinement retains every original sloped triangle and passes
   the bounded gates. This does **not** establish arbitrary retessellation equivalence.

The first divergent pair has matching quantized normals and an exact geometric
plane, while the packed plane anchor and narrow-phase triangle differ.
`refinement-plane-comparison.json` records cell offsets and reconstructed plane
heights. **Inference:** finite-precision triangle/plane evaluation contributes;
**unknown:** the exact first responsible native branch. Next discriminator: trace
that saved pair at its first divergent narrow-phase instruction. Do not label
this a proven general collision-solver fix.

Synthetic tests cover an aggregate mesh above 5462 vertices, per-chunk rejection,
invalid indices, collision-window sweep versus exhaustive integer-grid results,
300/301 candidate rejection, preserved legacy budget rejection and seam bucketing.
The private test verifies unchanged slope/prop/spawn/exit records and requires
both chunking and the arena for the larger scene. Earlier full-check failure was
one outdated error-message assertion; size rejection still worked.
Raw failed logs remain; final check receipt is authoritative.

## Native frame pacing

Original frame start `004ED714` is written by `00405BE0` using imported WINMM
`timeGetTime` (`00864884` IAT). `00405AD0` includes a busy wait using the native
30 limit. Read-only polling measures paced frame-start intervals, not GPU duration
or unpaced CPU cost. Millisecond quantization and observer poll gaps are recorded.
The fresh control produced 625 intervals at exactly 32 ms over 20 seconds, with
matching before/after spawn coordinates. The dense spawn sample has625 frame
intervals over20s, mean32.0016ms, median/p95/p99 32ms, max33ms. This establishes
observed paced cadence only. A concurrent workload on the machine was not
controlled, and native pacing prevents an uncapped CPU/GPU headroom claim.

**1203 selected tests pass** in146.71s; unchanged unrelated R2q exclusions are in
`test-selection.json`.

Related: [[PC level authoring memory limits]], [[Known Unknowns]].
