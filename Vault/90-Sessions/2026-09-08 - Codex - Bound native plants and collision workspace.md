---
type: session
date: 2026-09-08
agent: Codex
status: completed-bounded-checkpoint
tags: [session, implementation/modding, terrain/collision]
---

# Bound native plants and collision workspace

Continued the user's Milestone 3 request from baseline `bae129d`, following
[[PC Large-Level Engine Roadmap]]. The earlier pebble layout, saved 15-clover
Blender project, wilderness design bank and other-agent aqua-glow tree/session
remain preserved. No subagents, PS1 work, original changes, external live writes
or debugger stops were used.

[[EXP-20260908-001 - Plant capacity and collision workspace repair]] owns the
findings, addresses, scope and artifact index. Native offline construction
reproduces the twentieth-plant infinite scan. Nineteen coincident native
mushrooms reproduce the 400-pointer collector overwriting descriptor0. Authored
PIC guards bound pool scans and defer seed ticks before height/countdown changes.
The chunks-plus-arena compiler adds 16 KiB of separate PE storage for 2048 pointers
and2048 indices, preserving all 16 real HIGHLOW references and the unrelated
spatial-bucket end constant. Static allowance 300 and saved geometry remain exact.

32 focused tests pass, including original constructor register/flag/pool parity,
two image bases, full-pool deferral/resumption, the level17 exception, sparse
pool wrap and all five append sites at both capacity edges. Native twenty-plant
opening/registration/solving passes24 cases at peak 508 ; 48 paired complete height
queries match. The QPC probe passes50 offline checks, decoder10 malformed cases.
Earlier72 targeted compiler/native tests also passed before the11 additional
append/wrap cases were added. Actual Blender Build matches the repaired image
and original assets without saving the blend. Final selected `make check` passes 1251 tests in 156.84s, Vault lint has
0 errors/8 existing warnings, and tracked-file audit has 0 violations. The
existing unrelated R2q exclusions are preserved in `test-selection.json`.
The static-density claim sweep reports `new_only`.

Both four-section hardware loops complete.4514 route frames have no errors,
lifecycle changes or missing publication rows; whole-work p99 0.6468ms, maximum
2.9494ms before pacing. A native seed opens and both jump checks bounce, adding
871 measured frames, candidate peak 25 and exact source 8 payload/descriptor.
All 170 model payloads and four chunks pass after routes/plant/final reload.
These live checks use one active mushroom; the 20-plant fixture is offline only.

Rejected harness assumptions are preserved: an initial constructor watch site
was in padding; the first Blender attempt omitted operator registration;
initial live discovery lacked launch metadata and sent no input. A host-NX
assertion failed because Wine maps0087B000..0107EFFF asrwxp despite PE flags
omitting execute; corrected receipts distinguish declaration from host behavior.
All 216 indexed EXP028 files remain exact after closing its previous handoff.

Previous game133402 and diagnostic142117 are CLOSED with owned cleanup/audits.
Normal repaired game145025/start1814671, leader/group144782/start1814542 is OPEN
at spawn on`:2`, window14680071. Controller:
`work/experiments/EXP-20260908-001/handoff-detail/control.py`.
Binding accounts 14 owned identities and all 10 audit rows, with 3 protected foreign
rows. Normal EXE SHA `b7566474e809cb6e930f3f674f2e272256d3c6474741f8c2e963a01b64d7ac3b`.
The normal image has the plant/workspace repair and no QPC probe or hazard.

Next: a bounded simultaneous-plant hardware fixture and full-pool removal/reuse
endurance, then the consolidated Milestone 3 gate. Native appends still lack a
runtime bound check beyond 2048; arbitrary templates/other dynamic classes,
wider coordinates and streaming remain unproved. The original seed tick guard
now preserves pending seeds, but isolated slot release is not complete native
removal-lifecycle proof. [[Current State]], [[Environment Status]],
[[Known Unknowns]], [[Decision Log]] and the relevant MOCs are updated.
