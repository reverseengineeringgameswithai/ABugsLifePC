---
type: experiment
id: EXP-20260908-004
date: 2026-09-08
created: 2026-09-08
updated: 2026-10-29
status: bounded-native-prototype
question: Which native contact and query state caches terrain collision pointers, and can a collision descriptor be made inactive between completed queries without changing native movement?
result: Twenty-four 20-byte contact records at 007F3D68 cache the descriptor index (+0) and cell pointer (+4); all five candidate-producing coordinators test a descriptor's tag before reading its payload and four of them save/restore candidate count 007FC8D4; with tag/pointer zeroed between completed queries, offline movement, query and renderer arms match fully resident controls exactly
environment: Offline Unicorn x86 and Python; unchanged normal Wine session
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260908-003, EXP-20260908-001, EXP-20260907-026]
tags: [experiment, terrain/authoring, re/memory]
---

# Native terrain page residency

This experiment establishes the native contact and collision-query contract
that any change to resident terrain collision must respect, and checks it
offline by making distant collision descriptors inactive between completed
native calls. The normal game is unchanged and no live streaming is claimed.
Private artifacts below are under `work/experiments/EXP-20260908-004/`; the
frozen report is `reports/terrain/EXP-20260908-004.json`.

## Confirmed native contact and query contract

Original instructions004A9078–004A908D initialize24 records, each20 bytes, from
007F3D68 through007F3F48 exclusive. Record+0 is the descriptor index and+4 the
cached cell pointer used by004AB1A0 and its solvers004AAE30/004A9BA0/004AA4D0.
The initializer also clears+16.
`contact-asm.txt`, `spatial-init.json` and the bounded function exports corroborate
these facts. The call-site audit identifies slot0 at00440849, slot16 at0041B30B,
and a byte-selected argument at0041DA30. All runtime selector bounds/roles are
not established;24 initialized slots are not a general checked native API limit.

`native-contacts.json` constructs a real native landing in each of those24 slots.
Every resulting contact caches a cell pointer into the landed page, so that page
cannot be retired while the contact remains. Separate native landings in slots16
and23 simultaneously reference pages1 and2 while pages0 and3 unmap. No
inactive-slot clearing rule is established; nonzero contacts must be treated as
live even if a caller believes the slot inactive.

All five candidate-producing coordinators test a descriptor's tag before reading
its payload. Static exports cover004AB1A0,004ABE00,004AC140,004AC460 and004AC770.
The latter four save and restore candidate count007FC8D4 around their work;
publication must occur after the **whole query returns**, never inside the
temporary reset interval. Native query results below independently corroborate
the inactive-descriptor path. Spatial bucket membership contains descriptor IDs,
so stable IDs and existing bucket bytes can remain unchanged for this fixed
layout while tag/pointer become zero. This does not add new bucket geometry or
validate arbitrary newly positioned chunks.

The full0x470000-byte offline image is scanned at every byte alignment after
completed calls. Four changed pointer-valued words are the two retained
descriptor pointers and two contacts. Another468 matches already existed before
the pages were mapped, including instruction bytes and packed numerical fields;
they are reported as preexisting numeric matches, not pointer evidence. The
first naive census incorrectly treated every matching word as a pointer and was
rejected. Stack/register liveness and external game/renderer allocations remain
outside this census. It is not complete live-process reference closure.

## Offline native checks

`native-queries.json` adds24 exact comparisons across four native query paths,
three local positions and both the400-entry retail and2048-entry repaired
candidate workspaces, while distant descriptors have zero tag/pointer and their
payloads are unmapped. Return/output values, candidate sequences, restored counts
and selected solver globals match the resident control.004ACA60 executes as the
common consumer. Arbitrary caller contexts remain outside this finite check.

`native-transitions.json` runs three complete east/west cycles of prescribed
resolver deltas: 875 steps on original PC code and 875 on the repaired executable
SHA256 `b7566474e809cb6e930f3f674f2e272256d3c6474741f8c2e963a01b64d7ac3b`. All1750
steps match their fully resident controls in position, flags, contact **and
instruction count**, with descriptors deactivated and restored only between
completed native calls and no unmapped reads. Full restoration returns all
descriptor and payload bytes exactly. These are prescribed native collision
calls, not controller-input movies or the entire native actor/gravity update.

`native-render-pages.json` rebinds the four terrain mesh pointers to separate
allocations in each of12 camera contexts; mappings that the original native
culling gate rejects are unmapped before native drawing. All object admissions,
emitted vertex/index packet hashes, native instruction counts and batch bounds
match the fully resident DAT control; seven views have unmapped pages. Driver
COM calls remain stubbed; this is CPU mesh evidence, not GPU liveness or real
frame hooks.

Actual actor query/slot enumeration, native frame publication/file IO,
driver/register/stack lifetimes, state persistence and wider coordinates remain
open. Validation: 62 focused tests, then selected `make check` with1313 passing
tests in157.28s. No launch/close, live input, external memory write, debugger
stop, PS1 work or original modification occurs.
