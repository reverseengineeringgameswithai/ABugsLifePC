---
type: session
date: 2026-09-05
agent: Codex
status: complete
tags: [session, terrain, collision, handoff]
---

# 2026-09-05 1126 - Codex - Terrain diagonal and movement checkpoint

## Subsequent EXP-003 result (2026-09-05)

[[EXP-20260905-003 - Shared floor return discriminator and stitched patch]]
reproduces the rigid EXP-005 return fall numerically and with normal live input.
The original-instruction witness distinguishes a vertical discontinuity and
entry from beneath a one-sided plane from an XZ gap or Y-window-only cause. A
connected six-cell star with paired render heights passes finite modeled and
live return paths. This is a successor experiment, not a change to this original
fixture or a universal authoring rule; its prop-confounded and blocked routes
remain explicitly open. Earlier unresolved wording below describes this note's
historical checkpoint, not the new experiment's result.


## Outcome

Bank the completed box-edge diagonal and movement/view work as one local Git
checkpoint, retain its private evidence without copied Wine environments, and
leave a concrete continuation prompt for the separate floor-boundary defect.
The expected commit subject is `terrain: bank diagonal and movement validation`.

The checkpoint contains [[EXP-20260904-011 - Box top diagonal edge discriminator]],
[[EXP-20260905-001 - Box top diagonal live comparison]], and
[[EXP-20260905-002 - Box movement and occluding-view validation]], their public
reports/operator sources, `scripts/terrain-deck-grid-probe.py`, its regression
tests, and the associated Current State, roadmap, MOC, decision, unknown, and
session updates. The result is bounded: it validates the alternate 4x4 top at
the preserved failure pose and across five finite movement sweeps. It does not
establish a universal triangulation rule or solve EXP-005's return-floor defect.

## Runtime state at bank

`make session-audit` at this checkpoint reports no game/Wine processes, no
owned or unattributed groups, no null sinks, no open session ledgers, and
`clean: true`. Its tracked receipt is
`reports/terrain/terrain-20260905-bank-session-audit.json`.

This differs from EXP-002's last retained observation, where game
46701/1147812 remained paused with exact original mesh/collision and pose. The
current audit does not establish who closed that session or when. Treat the
older paused-game statements as historical experiment handoff facts and the
clean audit as the current environment state. No runtime action was performed
as part of this bank.

## Private evidence checkpoint

The private archive is
`work/snapshots/terrain-20260905-diagonal-movement-evidence.tar.gz` with SHA-256
`0dbf147f3efa72feea6e8e0c248c0fcd3d30ebfe7ded63c2a9d2317b6567715c`.
Its companion manifest is
`work/snapshots/terrain-20260905-diagonal-movement-evidence.manifest.tsv`.
The archive contains every unique private artifact named by the three public
reports, the reports themselves, and only the authored Level01 `LEVEL.DAT` /
`TERRAIN.ALL` fixtures needed to distinguish the tested variants. Full copied
game trees, Wine prefixes, originals, and caches are excluded. Archive
verification read all 804 members: 803 regular files match the manifest's byte
counts and SHA-256 values, plus the manifest itself. The manifest SHA-256 is
`736d6326e06125a39e72aaa756d42d0816277a0da4432650def4134713bca528`.

The protected stash remains untouched:
`76db1c9ee1ffffce52cea6aee591c24ab6a1c39a`, `stash@{0}`,
`WIP R2q hard-truth round 91 file-fsync byte provenance 2026-08-30`.

## Validation at handoff

- The five terrain/deck test modules pass 72/72 in 31.87 seconds.
- `make check` ran to completion as a command after 11,089.48 seconds. Pytest
  reports 4,090 passed, 166 failed and 42 errors, then exits 2. The late cascade
  is `OSError: [Errno 122] Disk quota exceeded` after its `/tmp` tree filled the
  tmpfs user quota; no green full gate is claimed.
- After removing only that generated scratch tree, the isolated pre-existing
  R2q line-5899 discriminator fails 1/1: the test expects the R2q-029 design SHA
  while the implementation returns the R2q-031 SHA. This is unchanged from
  parent checkpoint `e5f4a3c` and outside the terrain scope.
- A clean-storage rerun of representative late suites passes 281 tests; 14
  fixture-only process-memory tests are blocked by the workspace sandbox. All
  four affected modules pass 110/110 outside that sandbox in 18.38 seconds.
- Vault lint reports 657 notes, 0 errors and eight existing warnings. The
  tracked-file audit reports zero violations. Pre-stage `git diff --check`
  passes for tracked modifications. The staged check flags one trailing blank
  line in the new test source; that exact byte stream is SHA-bound by EXP-011
  and the private manifest and remains unchanged. Four unbound operator copies
  were normalized before commit. Exact
  commands and counts are in
  `reports/terrain/terrain-20260905-bank-checks.txt`.

## Copy-ready continuation prompt

```text
Continue the terrain/collision authoring work in /home/dev/ABLPC from the
current HEAD. The expected banking commit subject is:
  terrain: bank diagonal and movement validation

First follow AGENTS.md exactly. Read Vault/00-System/START HERE.md, Current
State.md, Project Roadmap.md, Environment Status.md, Decision Log.md, Known
Unknowns.md, Project Charter.md, and the relevant terrain MOCs/roadmap. Run
make briefing as an orientation only, then verify any claim in its cited note.

Verify these handoff conditions before changing anything:
- git status is clean and git log -1 has the expected banking subject;
- make session-audit is clean; there is intentionally no live game to preserve;
- stash@{0} is the protected R2q round-91 stash with object
  76db1c9ee1ffffce52cea6aee591c24ab6a1c39a; do not apply, drop, or rewrite it;
- originals/ remains read-only and all authored assets stay under work/.

Do not redo the barrier grammar, original collision admission, grounded
movement, visible box diagnosis, top subdivision, or diagonal comparison.
Those are banked in EXP-20260904-002 through EXP-20260905-002. The useful box
result is bounded: alternate 4x4 top diagonals removed all 259 modeled/live
failure samples at the tested pose, and five finite sweeps (518 grounded state
samples, 107 captures) plus jump/top/step-off contact passed. It is still not a
universal mesh rule.

The next target is the unresolved EXP-20260904-005 shared-floor return failure.
Read these first:
- Vault/30-Experiments/EXP-20260904-005 - Raised floor and visible ground pairing.md
- Vault/30-Experiments/EXP-20260904-006 - Flat deck and solid block test.md
- Vault/20-Research/New-level authoring roadmap (terrain, collision, materials).md
- reimplementation/ablpc/terrain_floor_edit.py
- scripts/terrain-floor-authoring-probe.py
- scripts/terrain-floor-visual-fixture.py
- reports/terrain/EXP-20260904-005.json

Confirmed starting facts: Level01 source 99 group offset 47640 contains six
32-byte cells. EXP-005 changed only each cell's signed h0 by -64 stored units,
raising it 2,048 world units while preserving normals, edges, and relative
admission bounds. It added no side triangles and did not weld neighboring
cells. In the synthetic forward route both arms lose contact at step 22; retail
lands on unchanged cell 47544 at step 23, while the raised arm is airborne at
steps 23/24 and lands there at step 25. The user separately observed falling
through when walking up and back. At this checkpoint, that return trajectory had not been reproduced
as a numerical trajectory, so do not claim a cause yet. EXP-006's flat deck is
a separate regression fixture and does not repair EXP-005.

Start offline. Assign a fresh experiment ID after checking the run/index state.
Enumerate every collision cell touching group 47640's boundary and every
render face/duplicate vertex that shares the corresponding footprint. Record
exact offsets and preserve unknown fields. Add bidirectional original-instruction
paths that cross each relevant boundary, including the user's up-then-back
direction, with explicit contact/source transitions. Use those results to
discriminate among a raw vertical step, a gap/overlap, one-sided triangle
admission, stale normal/bounds data, and a render-only mismatch. Do not silently
select one explanation.

If the evidence supports an edit, build a small connected gentle ramp or
stitched patch in isolated files under work/copies. Recompute only fields whose
PC meaning is established, keep the rigid EXP-005 edit as a failing/control
fixture, and add bounds-checked parser/writer regressions plus synthetic
fixtures. Pair collision and LEVEL.DAT terrain deliberately. Prove downhill and
uphill crossings, landing, step-off, and return in the original PC instruction
model before launching.

For runtime, use a fresh file-loaded isolated copy and the authoritative PC
autonomous-control procedure. Run make session-audit before launch and after
close. Do not use memory writes, teleport, ptrace, process stops, save states,
or debugger control without fresh explicit user authorization for that exact
use. Normal launch/input and read-only capture should be enough for the first
comparison. The Windows PC executable and recorded behavior remain authoritative;
do not consult or promote PS1 evidence unless a separately recorded bounded
cross-port question actually requires it.

At the end, update the experiment note/report, Current State, Environment
Status, Known Unknowns, Decision Log, relevant MOCs, and Session Index. Run
the focused tests, make check, tracked-file/protected-path audits, diff checks,
and any required claim sweep. Keep private binaries, assets, screenshots,
memory captures, copied games, and Wine prefixes out of Git.
```
