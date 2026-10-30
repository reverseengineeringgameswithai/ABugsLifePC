---
type: experiment
id: EXP-20260908-001
date: 2026-09-08
created: 2026-09-08
updated: 2026-10-29
status: finite-repair-and-normal-hardware-checks-passed
environment: Offline Unicorn original-PC instructions and Wine Gamescope Direct3D
question: Can simultaneous native plants exhaust the plant pool or overflow the movement collision collector, and what must a repair relocate?
result: Yes. 00467E60's tail 00467F88..00467F9D searches indefinitely once all 20 slots of pool 0059D9C0 are full; unchecked collector appends at 007F3F50/007F2680 reach the first terrain descriptor at 007F4590 with nineteen coincident type-5 mushrooms (twenty peak at 508 candidates). Relocating the collector needs sixteen HIGHLOW operands over five append paths and three consumers; a bounded repair passes native and hardware checks.
binary_sha256: b7566474e809cb6e930f3f674f2e272256d3c6474741f8c2e963a01b64d7ac3b
evidence: [EXP-20260906-007, EXP-20260907-023, EXP-20260907-028, EXP-20260908-001]
tags: [experiment, terrain/collision, implementation/modding, re/runtime]
---

# Plant capacity and collision workspace repair

This packet tests simultaneous native plants against the native plant pool and
the movement collision collector on the EXP-026 chunked layout. Evidence root is
`work/experiments/EXP-20260908-001/`; tracked findings and private artifact
hashes are in `reports/terrain/EXP-20260908-001.json`. Full-pool hardware
acceptance of the repair followed in EXP-20260908-002.

## Confirmed original failures: static instructions and offline execution

`00467E60` fills the plant at `00599C74` in the 20-by-48-byte pool `0059D9C0`.
Its tail `00467F88..00467F9D` searches indefinitely for another empty slot.
Nineteen native constructions return. The twentieth fills slot 19, then repeats
indices 0 through 19; the isolated probe stops after 61 visits at `00467F96`.
This is bounded offline execution, not a deliberately induced live game hang.
`constructor-capacity.json`, `00467e60.c` and `constructor.asm.txt` provide the
sequence and static evidence. The first probe guessed a watch site in padding
and instead hit its execution bound; that rejected diagnostic is retained as
`constructor-capacity-initial-bounded-timeout.json`.

The movement collector writes pointers at `007F3F50 + count*4` and parallel
short descriptor indices at `007F2680 + count*2`. Neither append is checked.
Pointer index 400 begins at `007F4590`, the first terrain descriptor. Nineteen
coincident type 5 mushrooms created by native construction, opening animation
and descriptor registration reach that unsafe store at `004AB54D` on the actual
authored terrain, with restored source 8 plant collision. The probe stops on
the first unsafe write before the solver runs. This deliberate overlap is a
stress fixture, not the current authored plant distribution. See
`native-pressure.json`, `004ab1a0.c`, and `workspace-relocations.json`.

## Repair requirements

Relocating the collector arrays requires sixteen existing HIGHLOW operands,
which cover five append paths and three consumers. The apparent seventeenth
candidate-range relocation, `004A8976`, is actually the spatial bucket clearing
loop's end constant `007F2682` and must stay unchanged. This distinction is
verified against `initializer.asm.txt` and the native append-site tests. With
19 plants, 48 paired complete height/query calls through `004ABE00`, `004AC140`,
`004AC460` and `004AC770` match returned values, candidate pointer and index
order, player state and solver globals, including consumer `004ACA60`
(`native-query-parity.json`). With the arrays relocated to a 2048-entry
workspace, twenty actual native type 5 constructions, animations and collision
registrations reach a peak count of 508 across 24 complete/pre-solver movement
cases (`native-fixed-pressure.json`).

A bounded constructor must preserve the original level17 special case
(seed `0059B6AC`) and defer a seed growth tick while the pool is full, before
either countdown or height changes; countdown values 1, 10 and 32767 then remain
stationary while full and resume after a slot is released. The fixture slot
release is an offline test setup, not proof of the complete native removal
lifecycle. Both image bases `00400000` and `10400000` pass. Tests:
`tests/test_dynamic_limits.py`.

In ordinary hardware runs with the repair, two four-goal loops and one native
seed opening (slot 26, type 5/source 8, runtime descriptor 224, payload
10000361, tag 108; 9 and 10 separate Vy=-3328 onsets) pass with all 170 model
payloads and four chunk records intact and the expected one initial NextLife
call in each native log. Read-only checks confirm all 16 relocated operands.

**Recorded permission distinction:** PE `.colmem` flags are `C0000080` (RW,
without execute), but `/proc/145025/maps` shows its containing arena as `rwxp`.
The first host-NX assertion was rejected and banked; the corrected receipt
verifies readable/writable storage without claiming enforced host NX. Why this
Wine mapping differs from the PE declaration remains unestablished. Evidence:
`workspace-permission-assumption-rejected.json` and `handoff-detail/workspace-verified.json`.

This repairs two reproduced finite cases; it does not establish general
allocation safety. Relocated lists still have finite capacity and native appends
still have no runtime bound check. Arbitrary templates, the other reserved
dynamic descriptor classes, movements outside the tested envelope, live
full-pool release/reuse endurance and prolonged crowded rendering need further
validation. No external live writes or debugger stops were used.
