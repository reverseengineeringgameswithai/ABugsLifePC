---
type: session
date: 2026-09-08
agent: Codex
topic: Native collision page retirement and repeated reloads
status: complete
tags: [session, terrain/authoring]
---

# Native terrain page residency

The user requested continued Milestone4 work. [[EXP-20260908-004 - Native terrain page residency]] adds checked native collision residency plans and
conservative readiness, with24 new synthetic regressions. All24 initialized
contact slots receive real native landing tests; simultaneous nonplayer slots
pin independent pages. The private adapter disables unused descriptors, verifies
incoming files, clears transient query workspace after complete queries and
unmaps retired pages while preserving contact and bucket state.

Three east/west cycles per executable yield1750 native collision steps, all
exact against resident controls, including instruction counts. Four additional
query paths yield24 exact comparisons with distant pages unmapped. A corrupt
second incoming file rolls back the first staged allocation and full publication.
Dedicated collision mappings peak48KiB during traversal; original full asset
buffers remain resident, so no total game RAM saving is claimed.

Straight-line control routes at several other Z lanes stalled; those rejected
attempts remain banked without attributing the obstruction to paging. A naive
numeric pointer census also overcounted preexisting instruction/packed-data words;
the corrected census distinguishes those from changed cached/descriptor pointers.

Twelve original-x86 renderer contexts also produce identical admissions,
vertex/index packet hashes and native work after culled mesh pages are unmapped.
Each camera uses a separate fixture; D3D calls are stubbed and original DAT remains
resident. This is bounded CPU-renderer evidence, not live/GPU streaming acceptance.

[[PC Large-Level Engine Roadmap]] records the remaining live frame, actor/query,
persistence, larger-coordinate and long hardware acceptance gates. Milestone4
is not complete and the normal game is not running streamed assets. Work uses
private offline copies; the normal project/session and protected other-agent
tree/session remain untouched.

Selected `make check`:1313 tests pass in157.28s, Vault0 errors/8 existing
warnings and tracked audit0 violations. The report freezes47 private artifacts,
source/dependency hashes and the exact test selection/receipt. Two claim sweeps
return `new_only`;34 earlier artifacts and two source files remain exact.
Fresh hashes verify721 normal assets, saved Blender and760 banked files. Normal
game154936/start2024608/group154693 remains at spawn; the existing ownership
binding accounts for the audit rows. No live input, writes, launch or debugger use.
