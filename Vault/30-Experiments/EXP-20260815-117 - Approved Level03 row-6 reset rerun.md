---
type: experiment
id: EXP-20260815-117
date: 2026-08-15
question: Does the exact Level03 row-6 X edit change the approved PC reset destination by the predicted fixed-point delta?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11 Staging; Gamescope; exact control and candidate PC work copies
environment_version: repository state at approved rerun; retail executable and exact Level03 DAT hashes recorded below
working_directory: /home/dev/ABLPC
configuration: fresh control/candidate Direct3D arms; two prior-authorized prerequisite-state writes; read-only route/reset trace
artifacts:
  - work/copies/EXP-20260815-117-approved-row6-reset/
addresses:
  - 0x0041C6C0
  - 0x00432930
  - 0x0059A5B0
  - 0x0059D9A0
file_offsets:
  - 0x4A4
result: accepted-row6-reset-coordinate-causality-natural-producer-open
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/runtime
  - re/gameplay
  - milestone/m3
---

# EXP-20260815-117 - Approved Level03 row-6 reset rerun

## Status

Complete. Hard-truth ACCEPT.

## Question

Does the one-field Level03 type-1 row-6 edit change the PC executable's
row-based reset destination by exactly the fixed-point value predicted by the
static consumer at `0x00432930`?

This experiment does not ask whether the table is semantically a checkpoint
table. It tests only row selection and reset-coordinate consumption.

## Authorization

The preceding forced diagnostic in [[EXP-20260815-116 - Level03 type-1 row discriminator]]
was not governance-valid because its target-memory writes lacked prior explicit
approval. Before this fresh rerun, the user was shown the exact proposed writes:

- byte `0x18` at `0x0059D9A0`;
- word `0x0002` at `0x0059A5B0`.

The user explicitly replied `yeah sure go for it` before either approved run
was armed. No other target-memory writes were made.

## Static PC evidence

- Executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Control `LEVEL03/LEVEL.DAT` SHA-256:
  `bda28dc7287ebc3648998425b3c09f19d6470a85c9fcd439cca5ad8e391c0f2b`.
- Candidate `LEVEL03/LEVEL.DAT` SHA-256:
  `4894b6159e5a36a37fb9a3f50243cdd816fa4e7f28e169bcadf45b48792d4c12`.
- The candidate changes row 6 X from `15678` to `15806`, a delta of
  `128`; row 6 Z remains `15438`.
- Row 7 remains `(15539, 0, 17102)`.
- `0x00432930` selects the nearest type-1 row from actor X/Z shifted right
  by 5, writes the selected X/Z shifted left by 5, and recomputes Y through
  the terrain helper. See [[FUNC-97C95BA5572D-00432930]].

## Runtime protocol

- Fresh control and candidate processes used `scripts/play-pristine.sh` with
  the baseline Wine prefix, a private null sink, and derived full-disc copies.
- The journey selector was inspected and internal level ID `3` was required
  before route input.
- Both sides received the same ordinary-input route protocol. Stochastic enemy
  contact produced different accepted endpoints, so endpoint equality is not
  claimed.
- Each endpoint was checked against rows 6 and 7 before arming.
- A continuous `process_vm_readv` sampler recorded coordinates, flags,
  NextLife, the counter, internal level ID, collision index, and collision
  material. The sampler did not pause or write the process.
- GDB then performed only the two approved writes and detached immediately.

## Control result

- Pre-arm: `(286160, 43864, 411065)`, flags `0x0008`, NextLife `0`,
  internal level ID `3`.
- Scaled X/Z: `(8942, 12845)`.
- Row-6 distance squared: `52,097,345`.
- Row-7 distance squared: `61,642,458`.
- At trace time 343 ms: flags `0x0018`, NextLife `2`.
- At trace time 354 ms: `(501696, 30092, 494016)`.
- The trace contained 243 exact `(501696, *, 494016)` samples.

## Candidate result

- Pre-arm: `(313732, 44316, 390770)`, flags `0x0008`, NextLife `0`,
  internal level ID `3`.
- Scaled X/Z: `(9804, 12211)`.
- Candidate row-6 distance squared: `46,437,533`.
- Row-7 distance squared: `56,812,106`.
- At trace time 514 ms: flags `0x0018`, NextLife `2`.
- At trace time 524 ms: `(505792, 30120, 494016)`.
- The trace contained 231 exact `(505792, *, 494016)` samples.

## Discriminator

- Control X: `15678 << 5 = 501696`.
- Candidate X: `15806 << 5 = 505792`.
- Observed X delta: `+4096 = 128 << 5`.
- Control and candidate Z are both `15438 << 5 = 494016`.
- Y is independently terrain-recomputed and is not expected to be equal; the
  accepted samples were `30092` and `30120`.

The one-field row-6 edit therefore caused the predicted one-axis reset change
while the unchanged row field produced an unchanged Z. This confirms the PC
row-6 reset-coordinate consumer. It does not by itself prove the semantic name
`checkpoint` or identify a natural gameplay producer.

## Exploratory natural-trigger evidence

This evidence was collected while pursuing a no-write alternative and was not
used as the causal discriminator:

- `0x0041C8CC` sets bits `0x14` when the fourth argument to
  `0x0041C6C0` differs from `2`.
- Call site `0x004408EA` passes fourth argument `1` for collision-dispatch
  result `1`.
- Helper `0x004ACF90` returns that result from the loaded PC collision
  descriptor's signed word at offset `0x1E`.
- The live Level03 descriptor table contained material/result value `1` at
  valid-looking indices `570` through `578`.

These observations define a bounded natural-trigger experiment. They do not
yet identify the material semantically or prove that ordinary gameplay reaches
it at the candidate row.

## Evidence

Ignored raw evidence is under:

`work/copies/EXP-20260815-117-approved-row6-reset/`

The directory contains route traces, reset traces, GDB before/after
transcripts, the exploratory material scan, and `SHA256SUMS`.

## Conclusion

Confirmed PC fact: after prior explicit authorization of the exact two
prerequisite writes, changing only Level03 type-1 row-6 X by `+128` changed the
selected reset X by exactly `+4096`, while the unchanged Z remained exact.

Open inference: type-1 rows are checkpoint records. Keep [[Known Unknowns#KU-057]]
open for the natural producer and semantic classification.

## Hard-truth verdict

James returned `ACCEPT` for the bounded claim that PC Level03 type-1 row 6
supplies X/Z to the reset-coordinate consumer reached through `0x00432930`,
and that the `+128` row-X edit causes exact reset-X delta `+4096` while the
unchanged row Z causes unchanged reset Z.

Acceptance explicitly excludes checkpoint semantics, a natural death/contact
trigger, semantic identification of collision result/material `1`, and
generalization to every row, level, or consumer. [[Known Unknowns#KU-057]]
therefore remains open.
