---
type: session
date: 2026-09-05
agent: Codex
status: bounded-complete-test-arms-closed
tags: [session]
---

# 2026-09-05 1042 - Codex - Box movement and occluding views

The user asks to keep going with DEC-238's movement/view validation and later
reiterates continuing where work left off. Use normal inputs in two sequential
file-loaded research instances; preserve the existing paused user failure.
No live memory write or debugger authority is reused.

[[EXP-20260905-002 - Box movement and occluding-view validation]] records five
valid eight-second sweeps: 518 state samples, 107 frames, stable deck contact
and player reference points outside the walls. The original-location box also
accepts a jump, top crossing and step-off landing. Reuse the already tested
stationary placement for a more directly occluding camera view.

One original-location south route misses its intended approach after release/
settle motion, reaches the finite deck boundary and is rejected. Retain that
failure without promoting it to a game collision defect. Add an explicit
intended-wall position gate; the later stationary south retry passes. The
valid south result belongs to the stationary placement only.

The stationary west edge is preserved paused for read-only copying and the
existing original-PC drawing operator. All 84 mesh tuples and 179/355 actor
tuples match captured buffers. All 485 blue samples have actor coverage; 28
intersect the analytic top, and none are behind it. No new depth inversion
is demonstrated in this diagnostic. Moving captures remain asynchronous and
the analytic actor/rasterizer limits are explicit.

Update Current State, Environment Status, Project Roadmap, Known Unknowns,
the authoring roadmap, DEC-239 and relevant MOCs. Next is the separate EXP-005
return-floor defect; arbitrary geometry and universal diagonal rules stay open.

Both research instances close and all post-close audits match the same seven
user-session processes and sink. Original game 46701/start 1147812 remains
paused with its exact original mesh/collision/pose/camera. No original asset,
historical mapping, R2q source or protected stash was changed.

Validation: exact loaded prefixes and hardware/CD gates; all five trace
invariants; native capture hashes; original-instruction calls; diagnostic
triplet equality; lifecycle/original-user identity equality. Stationary builder
reproduces the existing fine-control hash, then changes only 138 top-table
bytes. The viewer's initial JavaScript newline error was fixed and syntax
checked before handoff. New evidence and numeric report are retained; no new
commit or complete repository-wide test run is claimed.

Final checks pass: all 728 report artifact hashes, 11 public operator copies,
107 viewer references and JavaScript syntax. Vault lint: 656 notes, zero errors,
eight existing warnings. Tracked-file audit: zero violations; whitespace clean.
The claim sweep finds only the updated movement-result wording. Receipt:
`work/experiments/EXP-20260905-002/checks.json`. HEAD remains `e5f4a3c`.
