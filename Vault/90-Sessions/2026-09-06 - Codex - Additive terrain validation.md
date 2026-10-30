---
type: session
date: 2026-09-06
agent: Codex
status: completed
tags: [session, terrain/validation]
---

# 2026-09-06 - Codex - Additive terrain validation

Continued [[EXP-20260905-009 - Additive terrain preservation and access ramp]] with explicit user approval to correct the two exception expectations and offline landing setup, then continue terrain-only validation.

## First validation pass

- Corrected new tests: 39 passed in 0.36 seconds.
- Eleven-file terrain-only gate: 224 passed in 26.61 seconds; four workers, repo-local scratch, failed-only retention.
- Built a fresh isolated copy under `work/copies/EXP-20260905-009/game/PC/BUGS`. Original 134 source-99 cells remain active; sixteen cells are added. Original mesh-160 vertices and full command groups remain in the expanded mesh.
- Native proof: six accepted arms, four incomplete route arms, one new probe argument error; 10.938740 seconds. Preservation, loader, DAT relocator, box routes, landing/step-off and additive fall landing pass. The replacing fixture remains airborne for the same synthetic fall; the additive arm first lands on original cell 45884.
- Three connector targets and the longer original-floor target are not reached, although each subsequent return succeeds. Twelve retail/additive local controls at two labelled speeds stop grounded on cell 44140; paired endpoints differ by at most one world unit. Control duration: 3.512078 seconds. The cause is not isolated and thresholds were not changed.
- At this first pass, the new command-stream driver passed bytes rather than the parsed object its helper expects. The later approved correction and successful traversal are recorded in [[2026-09-06 - Codex - Additive crossing control diagnosis]].

## Evidence and boundaries

Public build/validation receipts: `reports/terrain/EXP-20260905-009.json` and `reports/terrain/EXP-20260905-009-validation.json`. Complete private trajectories: `work/experiments/EXP-20260905-009/offline-proof.json` and `connector-retail-control.json` in that directory. The initial progress receipt is explicitly historical.

No R2q/full repository check, Git/stash operation, original-file mutation, live game inspection/input/write, launch or close. Offline emulation is not runtime acceptance or a full actor/input replay. The existing OG session is untouched, with current pose/ownership not refreshed. Previous live write authorization was not reused. Existing private snapshots were not changed.

The next steps at this first pass were command-probe correction and route discrimination. [[2026-09-06 - Codex - Additive crossing control diagnosis]] now records their completion and separate four-route through-crossing acceptance. Runtime comparison remains next; do not report the finite fall repair as universal terrain/collision completion.
