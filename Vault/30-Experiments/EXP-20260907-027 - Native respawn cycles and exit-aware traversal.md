---
type: experiment
id: EXP-20260907-027
date: 2026-09-07
binary_sha256: 431ec953b67bd3233f8fa58e7a22edbfabaeb153e3ee322d760c45f2a44c7d8f
environment: Guarded Wine hardware Direct3D previews and original PC native Unicorn probes
question: How do native death, damage, respawn and level re-entry work on PC, and do they preserve resident level and model storage?
result: 0043F9E0 dispatches contact result 1 to immediate death and result 4 to damage (field 0059D9A4); 0043DA40 calls reset 0042DDB0 and NextLife without ReStart, copying the auxiliary position 0059D960..68 that 004189E0 updates while excluding result 4; a one-byte result-word edit makes a damage hazard; six native reset cycles and exit/re-entry keep all 170 model payloads and four resident chunks intact
status: bounded
tags: [terrain/authoring, re/runtime, implementation/modding]
---

# Native respawn cycles and exit-aware traversal

> EXP028 evidence maintenance: the intentionally open handoff was later closed.
> Its indexed normal-detail launch console appended477 shutdown bytes. The
> original11056-byte prefix still has its indexed hash and is preserved separately;
> the other249 indexed files are unchanged. See
> [[EXP-20260907-028 - Representative update and render headroom]] and its
> `prior-packet-recheck.json`. The original historical manifest is retained.


The control and visual-detail candidate are the EXP-026 builds; normal geometry,
collision and executable are unchanged. Private packet:
`work/experiments/EXP-20260907-027/`; paths below are relative to that packet
unless stated otherwise. No PS1 consultation, external live writes or debugger
stops.

## Confirmed native lifecycle

Original PC executable SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`:
indexed static exports `0043f9e0.c`, `0041c6c0.c`, `0043da40.c`, `0042ddb0.c`,
`004189e0.c` identify the relevant native paths. The runtime controller compares
resident reset, damage and safe-position code against the actual derived image,
in addition to prior movement/exit/storage guards. `native-lifecycle-code.json`
independently confirms those bounded ranges match the original PC executable. The normal derived executable
is identical in every arm; no diagnostic executable hook is used here.

`0043F9E0` queries contact through `004ACF90`. Result 1 dispatches immediate
death through `0041C6C0`; result 4 dispatches damage. The damage path decrements
the signed field at `0059D9A4`; after it falls below zero it sets transition
`0059A5B0=2`. The outer loop `0043DA40` records the death, calls reset
`0042DDB0`, and enters `NextLife` without a full asset `ReStart`.
For Level01, the reset copies the auxiliary position at `0059D960..68` to Flik
and decrements byte `0059D9B0`. `004189E0` updates that auxiliary position under
several ground/state/nearby-actor checks and explicitly excludes result 4.
These are PC-specific observations; no general checkpoint implementation or
semantic renaming of other unknown fields is introduced.

Private fixture construction changes only source record 191's result word at
TERRAIN.ALL offset **382310** (`record.offset+0x28`, native directory stride76).
The accepted damage fixture changes `0000` to `0400`: exactly one byte differs.
SHA-256 `7462385d0a72ca78917202b880357b9ce7430349d145a2a0db506d43daf087f9`.
`hazard4-build.json` replays original native loading, landing/movement and
`004ACF90` at three points. NE returns4 instead of0; SE and spawn return0 in
both arms, with identical landing positions, flags, contacts and instruction
counts. Normal TERRAIN.ALL retains SHA
`f6f0da655ad1067ecee1d5a73683308ec16aa8c805fb6be0ef30e6021bdf64bc`.

`hazard4-control-lifecycle-summary.json` and
`hazard4-detail-lifecycle-summary.json` each verify three actual native deaths
and resets: lives 5→4→3→2, one new death/NextLife event per cycle, no asset restart,
no level-select transition and no completion event. Each arm ends with exactly
three death log entries and no GameOver entry. First asynchronously sampled
post-reset positions differ from the saved pre-death position by 13.15–34.50
world units; these samples include resumed native physics, not an atomic view
of the reset copy instruction. Both arms regain grounded flags and zero vertical
velocity. Camera matrices/translations are retained alongside the samples.

All170 native model payloads/extents pass repeated read-only checks spanning
cycles1 and 3:427 samples in control, 429 in detail. All four resident chunk meshes,
colliders, origins, relocated pointers and result words match before and after
the cycles. Arena root stays `0087B000`; cursor stays10300825 in control and
10387477 in detail. This is sampled integrity and finite lifecycle coverage,
not an uninterrupted proof of all memory or every actor reset.

The result4 fixture can still return Flik close enough to the chunk boundary
to take additional damage: both final retreats finish with damage field2 and
two lives remaining, on ordinary SE ground. Thus the six-cycle result does
**not** certify a hazard-free spawn placement. An airborne entry from a safe
interior point is a useful next discriminator before authoring actual hazards.

## Result-1 hazard counterexample

The first instant-death fixture used result1 (SHA
`63f2f61d355b827b0ff4e8b8700e23c51475c97b01ac2938eaa4455ad0e5a5f9`).
It allowed the auxiliary position to move inside the lethal NE section.
`hazard-control-death-01.json` records six deaths and repeated resets there,
eventually exhausting lives and entering GameOver. This rejected fixture is
retained in `hazard-control/rejection.json` and `gameover.log`; the prepared
result1 detail arm was never launched. The model observer then rejected pointer0
after the transition to the menu; that is outside its in-level contract and is
not evidence of model corruption.

## Exit completion and re-entry

Entering the authored exit records one native completion `LEVELDONE : Start/End`
and return to the Anthill carousel (`exploratory-exit.json`,
`exploratory-exit.log`); completion-animation coordinates after transition must
not be classified as a floor fall. In each normal arm, two guarded Return holds
then re-enter Level01, raising the full initialization count from 1 to 2 and
restoring the exact spawn(192000,-102400, 448000), heading 0. `reentry-1.json`,
`final-game.log` and `resident-chunks-after-reentry.json` in each arm bind the
new load, all four exact mesh/collider/pointer sets, and all 170 model payloads
at the same expected arena locations. The brief menu/score-screen allocation
reset is expected and is outside the in-level model-pointer verifier's contract.
Before the exit, both normal arms completed a four-goal loop visiting all four
contact sections 99/178/179/180 with zero death or completion transitions
(`normal-control-loop-summary.json`, `normal-detail-loop-summary.json`).

## Checks and limits

Artifact/hash index: `reports/terrain/EXP-20260907-027.json`. The selected
`make check` passes 1219 tests in 152.75 s. Full final inventory confirms all 721
normal game files unchanged and only `PC/BUGS/bugs.log` added at runtime.

Six finite native reset cycles add lifecycle evidence to EXP-026's exact
collision and bounded renderer checks. They do not establish representative
frame-work headroom, all-camera correctness, wider coordinates, complete actor
endurance, safe authored hazards or streaming. Hardware arms require all six
original Direct3D log markers; process audits serve ownership accounting only,
not CAP-010 runtime validation.
