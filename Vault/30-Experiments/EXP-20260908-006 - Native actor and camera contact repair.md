---
type: experiment
id: EXP-20260908-006
date: 2026-09-08
status: bounded
question: Can all 64 native actor selectors coexist with the camera without changing collision response?
result: Relocating the contact table to 66 records needs the 21 native table references plus the four camera-specific solver comparisons (004A9F44, 004AA027, 004AA862, 004AA983) moved to the camera slot; 3960 + 240 native movement comparisons match the original; hardware high-slot actor interaction remains unaccepted.
platform: Windows PC under Wine and isolated x86 fixtures
binary_sha256: 16b41c4cd0aebe8800d902e14331d8b30d58030a62e865f5fc5fb08952d11dbf
environment: Linux Wine hardware Direct3D and isolated Unicorn x86
tags: [experiment, terrain/authoring, re/memory]
---

# Native actor and camera contact repair

**Confirmed, bounded:** `reimplementation/ablpc/contact_slots.py` relocates the
native contact table into unused collision-workspace storage, so all 64 native
actor selectors coexist with the camera. This closes the allocation/alias defect
identified in EXP-20260908-005, not contact lifetime or complete actor-state
questions.

## Executables and static evidence

The PC retail reference remains SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
Input current-profile executable:
`b7566474e809cb6e930f3f674f2e272256d3c6474741f8c2e963a01b64d7ac3b`.
Expanded-contact candidate:
`16b41c4cd0aebe8800d902e14331d8b30d58030a62e865f5fc5fb08952d11dbf`.
Private packet: `work/experiments/EXP-20260908-006/`.
Frozen index: `reports/terrain/EXP-20260908-006.json`.

`static-contact-references.json` verifies 24 instruction operands: 21 native
contact/table references, two separate scalar references deliberately retained,
and the authored exit helper's PIC displacement. Native `0041C420` keeps its
original assignments1..64. Flik keeps0; camera `0041B30B` now supplies65.
`004A9078` initializes66 twenty-byte records at `0107E000..0107E527`, using the
existing `.colmem` tail. No executable/image size growth is needed.
The initializer still preserves unknown bytes+8/+12.

Four solver comparisons (`004A9F44`, `004AA027`, `004AA862`, `004AA983`) explicitly
recognize the camera record, so their operands also move to slot65. Blindly
relocating the table would retain the wrong camera behavior. The separate
scalar at `007F3F48` stays in place. All HIGHLOW relocations remain intact.
The exit wrapper at `004BBA6A` reads the relocated Flik record. Unrecognized PIC
readers, changed evidence windows, extra/missing references and duplicate
application reject. The exact inverse reproduces the input bytes.

## Native verification

`native-contacts.json` compares all66 slots after native landing over3960
prescribed wall-directed movement calls: player0 versus original0,
actors1..64 versus original noncamera1, and camera65 versus original camera16.
Position, flags, contact and instruction counts match; storage tails remain exact.
The first route did not reach the camera-specific wall-response branches.
`camera-solvers.json` separately approaches80 actual non-floor cell planes in
airborne/grounded states,240 further movement comparisons. All four camera
response branches execute with exact original/repaired results.

All66 actual landed contacts reject retirement of their referenced page. Actor64
and camera65 concurrently pin pages1/2. Calling the original entity initializer
with an empty actor table leaves those contacts intact. Pin release therefore
still requires evidence beyond entity inactivity/reset.

Regression tests execute full native initialization, assignment, contact-result
readers and the authored exit wrapper at the preferred base and+`10000000`.
They check all66 slots, unknown bytes, canaries, native hazard results, exit
bounds, PE relocations and fail-closed patch guards. The reference residency
API now accepts an explicit66-record profile; its original24-record/default
15-actor admission remains available for unrepaired binaries.

## Hardware evidence and rejected attempts

Three private derived builds pass the six-marker hardware/CD gates and are
closed afterward. `crowd27` reproduces the earlier27-selector/20-plant file
fixture. Fifty seconds of passive observations see all20 plants and native
contacts0/6/7, exact original-table zeros and spare-tail zeros. The corrected
15-second observation verifies lives5; the first observation's lives field
used the wrong address and is explicitly rejected in `harness-corrections.json`.
All170 models and four native chunks remain exact. The model expectation needs
an independently derived88190-byte shift: DAT+88184 and retained TERRAIN+6.
A first zero-shift comparison rejects; it is not model-corruption evidence.

`seeds64` proves all64 file-loaded selector assignments, but passive observations
show only Flik's retained contact. An attempted high-slot approach leaves the
preregistered interior rectangle and stops before pickup. A separate
`seeds64-near` fixture places seed63 near nominal spawn; Flik is displaced before
the pickup attempt, and the seed remains uncarried. No high-slot live movement
or general64-actor lifecycle acceptance follows. The displacement/interaction
route remains unresolved. Native offline high-slot movement is independently
verified above. Initial carousel input during fade also rejects; the retry uses
a settled, captured training carousel. Socket discovery excludes the separate
Gamescope input socket while retaining peer/PID/group checks.

## Preservation

The earlier EXP005's82 private artifacts reverify. Its superseded uncommitted
package source is archived by an exact inverse that matches the frozen SHA;
the old residency source also matches its predecessor hash. See
`predecessor-recheck.json` and `superseded/`.

Combined selected `make check` (recorded with EXP-20260908-007): 1467 tests pass
in169.86s. The selection excludes unrelated R2q/tool suites. No external live
memory writes, debugger stops, original changes or PS1 work.
