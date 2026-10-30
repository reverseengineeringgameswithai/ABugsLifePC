---
type: session
date: 2026-09-08
agent: Codex
topic: Milestone 4 compact native storage and reference limits
status: complete
tags: [session, terrain/authoring]
---

# Compact terrain pages and native selector limits

The user requested continuation and an attempt to finish Milestone 4.
[[EXP-20260908-005 - Compact terrain storage and actor selector limits]] advances
the native page prototype and records the remaining gates in
[[PC Large-Level Engine Roadmap]]. **Milestone 4 remains incomplete.**

The checked package builder removes 305,340 managed mesh/cell bytes from the
current resident DAT/TERRAIN files, preserving native IDs, supported offsets,
opaque records and trailers. The private six-chunk bank compile removes 197,312.
Placeholders require a native adapter and are not playable assets on their own.
Neither package is installed in the normal game.

Native DAT fixup preserves all 670/688 scene/object records in the two profiles.
The compact collision adapter binds pages before original spatial initialization;
1,750 movement calls exactly match full-source controls across repeated routes.
Only compact source buffers are mapped. Two persistent CPU renderer fixtures
match all geometry packets/admissions/native work over 36 frames and three
camera cycles, with actual mesh load/unmap and corrupt-load rollback. Driver
calls remain stubbed; allocation figures are explicit fixture bounds, not total
RAM or hardware completion evidence.

The native actor initializer assigns slots1..N without a table bound. Camera
slot16 conflicts with actor assignment16, and slot24 exceeds the initialized
24-contact table. The current packet has9 assignments; the prior crowd packet
has27. An offline guard admits at most15. Preserve the crowd's recorded finite
passes, but do not extend them to all later moving seeds. Entity initialization
does not clear cached contacts; conservative pin retention remains necessary.

Focused page/package regressions:93 pass. Selected `make check`:1,344 tests pass
in158.09s; the inherited selection excludes unrelated R2q/tool suites. Validation
results are frozen in `reports/terrain/EXP-20260908-005.json`, with all private
artifact/source hashes. Earlier81 private artifacts and four source/test entries
reverify. Hook installation was already correct. No commit was requested.

All721 normal files, saved Blender and760 banked files remain exact. Game154936/
start2024608/group154693 stays open. Its passive position changed during the task;
no agent input occurred. No launch/close, live writes, debugger stops, original
changes, PS1 work or changes to the other worktree/session occurred.

Next: close the actual frame/query/reference gate, then build the in-process
loader with combined visual/collision readiness and failure barriers. Actor/item
persistence, wider coordinates and long hardware memory/state acceptance follow.
