---
type: session
date: 2026-09-04
agent: Codex
topic: Direct collision instruction pivot
status: accepted-offline-checkpoint-full-suite-incomplete
---

# 2026-09-04 1809 - Codex - Direct collision instruction pivot

## Request and initial state

The user asked to inspect the project and continue toward a better way to solve
terrain/collision. Initial clean HEAD was `1c1c59380123fed848c0ac51a101486c5506d804`,
the R2q-032 activation bank. Its source/activation had James acceptance, but its
interrupted full gate had no terminal verdict. The round-91 stash remains
protected at `76db1c9ee1ffffce52cea6aee591c24ab6a1c39a`.

Read the mandated Vault orientation, operating manual, charter, relevant MOC,
collision/mesh dossiers, Ghidra caveats, KU-079/080/081, authoring roadmap,
bank session, and relevant historical runtime experiments. No external PS1
repository was consulted and no live action ran.

## Work and findings

Added `scripts/terrain-collision-probe.py` and47 regression tests. It hashes the
retail work-copy executable and executes original x86 instructions in Unicorn
with synthetic globals. The movement callee has no stubs; the descriptor slice
explicitly skips rendering. Outputs contain measurements/hashes only.

[[EXP-20260904-001 - Original PC lateral collision and descriptor-store probes]]
records exact code/data hashes, addresses, controls, results, and limitations.
Both X/Z vertical triangles change lateral response. No-candidate, moving-away,
outside-triangle, and reverse-winding controls do not. Special contact record
changes response gain. The direct render-side store loop targets N..N+19;
whole-subtree effects and actual template identity remain open.

James independently checked a second retail copy, raw instructions, and the
initial27 descriptor/10 movement fixtures, returning bounded ACCEPT. He also
identified existing independent runtime evidence binding the coordinator's
writer to Flik; parent verified the notes, preserved log and raw caller chain.
His corrections distinguish frequency hashes from ordered traces, encoded from
position units, and N's count from an unproved static-record high-watermark.
Final report includes two additional special-contact fixtures.

Updated Current State, Known Unknowns, relevant MOCs/dossier and roadmaps.
DEC-226 makes real-cell/candidate analysis the next offline work, independent
of R2q. Historical frozen artifacts and runtime authority are unchanged.

## Verification

- Focused probe + height + parser tests:70 passed in0.96s, no skips.
- Hooks already installed.
- First full `make check` attempt passed import, Vault, and compatibility gates,
  then stopped at384 passed /1 failed: `test_peek_reads_a_known_global` could
  not use `process_vm_readv` under the sandbox (`Operation not permitted`).
  This is not a collision regression or a full-suite pass.
- The unsandboxed retry passed the permission-blocked test and continued to
  **1,333 passed in523.91s**, then was deliberately interrupted to bound this
  offline checkpoint's verification cost. Pytest emitted a terminal
  `KeyboardInterrupt` at `reimplementation/ablpc/r2c_localizer.py:140`;
  `make` exited2. This is an **incomplete full gate**, not a pass or an assertion
  failure. The process was specifically identified (pytest PID16703, child of
  this make, repository cwd, start18:14:01) before SIGINT. No game process was
  targeted. It stopped in R2c localizer fixtures, before the later R2q suites.
- James returned **ACCEPT — EXP-20260904-001 source, reproduced results, and
  corrected scientific documentation**. He independently reproduced all27
  descriptor/12 movement cases and70 tests. Accepted experiment note SHA-256:
  `69c860940b0ac6adf3407c7b7211f4d157cf22ad7e60e0d051e50278845bc8b5`.
  He separately accepted the static reconnaissance addendum below.
- Claim-sweep old/new checks have zero old wording for the corrected height-only
  survey, collision-read-side scope, negative-control endpoints, and flag mask.
  Vault lint has0 errors (existing budget/staleness warnings remain); tracked
  asset audit has0 violations. Do not infer completed R2q finalization from
  acceptance of this separate collision experiment.
- Closing host session audit is clean: no owned/unattributed processes, null
  sinks, or open sessions. Protected stash identity is unchanged. The dedicated
  temporary pytest directory contains only4KiB of bookkeeping, no game capture.

## Bounded next-packet reconnaissance (static, not candidate admission)

Retail `CD/LEVEL01/TERRAIN.ALL` is236,940 bytes, SHA-256
`62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868`.
The directory has189 records:178 kind6,10 kind257 (`0x101`),1 kind260.
Reading only payload-bearing kind6/7/8 records with the existing bounded parser
gives6,379 stored cells: zero with normal Y exactly0 and nonzero X/Z, but2,541
with `max(abs(nx),abs(nz)) > abs(ny)`. Minimum absolute normal Y is2.
These counts are stored payload cells, not all instantiated descriptors,
deduplicated world triangles, admitted candidates, or gameplay walls.

Useful steep-cell locator: source record87, group offset988, cell offset1000
(`0x3e8`), normal `(-8178,-595,-14184)`. An indiscriminate attempt to parse
all payload kinds as triangle groups correctly rejected record178; it is
kind257, payload offset219180 (`0x3582c`), size452, **not** evidence that the
retail file is corrupt. Keep unknown record kinds opaque until their consumer
is decoded.

Raw `004a860f..004a862a` supplies a precise second lead: for an admitted
high-kind payload with marker `0x12345678`, the loader chains its pointer
through `007f3938 + 4*kind`. For kind257 this is `007f3d3c`, the linked-list
head read by the movement coordinator at `004ab5b7`. Its later collection
populates the separate segment candidates consumed by `004a95e0`. Therefore
inspect this high-kind path as well as steep triangles in the next packet.
The present instruction probe deliberately has zero segment candidates and
does not test this path's behavior or fully decode its record grammar.

Count reproduction (run Python with `PYTHONPATH=reimplementation`):

```python
from collections import Counter
from pathlib import Path
from ablpc.terrain_all import TerrainAll
t = TerrainAll.from_path(Path("work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL01/TERRAIN.ALL"))
cells = [(r.index, g.offset, c) for r in t.records
         if r.payload_size and r.field_10 in (6, 7, 8)
         for g in t.collision_payload(r.index).groups for c in g.cells]
print(Counter(r.field_10 for r in t.records))
print(len(cells))
print(sum(c.words[1] == 0 and bool(c.words[0] or c.words[2]) for _, _, c in cells))
print(sum(max(abs(c.words[0]), abs(c.words[2])) > abs(c.words[1]) for _, _, c in cells))
print(min(abs(c.words[1]) for _, _, c in cells))
```

## Next

Follow DEC-226: retail LEVEL01 cell/template census, then original candidate
admission with selected real geometry. Leave KU-079 open and retain the scoped
unknowns in KU-080/KU-081. No game/wrapper retry is implied.
