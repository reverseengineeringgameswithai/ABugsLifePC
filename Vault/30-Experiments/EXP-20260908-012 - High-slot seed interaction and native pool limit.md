---
type: experiment
id: EXP-20260908-012
date: 2026-09-08
environment: Wine Gamescope hardware Direct3D, Linux perf CPU-clock sampling, offline Unicorn
question: Can a high native contact slot complete seed interaction, and why did a carried-seed route stall?
result: Contact slots 2 and 64 complete pickup, local carry and throw; the carry word at 0059D96C holds a byte offset (132 per actor index); the stall is original 0042AA50 cycling endlessly through a full 64-record pool at 00598CA8 with no full-cycle exit, and caller 0043EF06 writes through the result, so a null return is unsafe
binary_sha256: bc8e4c381da401906b93d882750f67f1bd8802ef4d92a8e7227c6457d7b8155d
status: bounded-pass
tags: [experiment/terrain, re/collision, implementation/modding]
---

# High-slot seed interaction and native pool limit

Continues EXP-20260908-006 and EXP-20260908-011. Private paths below are
relative to `work/experiments/EXP-20260908-012/`. Machine-readable report:
`reports/terrain/EXP-20260908-012.json`, SHA
`a34f4bbb0fc01e956c15a8ad7469f407b44cc356696286786c7d1406d7ebfdbd`.

## High-slot interaction

Two test copies with 64 file-loaded type11 seed records swap only actor1/63
coordinates so that contact slot2 or64 is near the ordinary start; all unknown
record bytes are retained (`positive-low-fixture.json`). Original0041C420
assigns selectors1..64 and the repaired camera setup uses65; eight fresh native
initializer/camera cases cover both image bases. In an offline selector fixture
without terrain, native004ABE00 returns the no-ground sentinel and initialization
adds0x3200, so file Y cannot be treated as retained ground height; the initial
rejected Y assumption is preserved.

The native carry word at0059D96C holds a byte offset, not an actor index: 132 for
actor1/contact2 and 8316 for actor63/contact64. Both arms use ordinary Control_L,
walk locally, then throw. Pickup samples cover states8..12; final carry state and
offset are zero, the seed is stationary at a new location, and its native carried
flag is clear. All64 selector/placement identities remain correct. Each arm's
`interaction-summary.json` contains the detailed positions and checks. This does
not establish every actor kind,64 simultaneous interactions, distant
carried-actor traversal, or actor/item serialization.

## Rejected controls and confirmed native pool limit

All failed or superseded arms are retained in `rejected-arms.json`; none is
silently counted as a successful comparison:

- `low` rejects at an unlabeled inherited observer assertion; `low2` identifies
  the incorrect arena expectation. Both close before movement.
- `low3` picks up actor0 and reaches the distant route destination, but stops
  advancing at native frame6780. The earlier route recorder's `accepted` field
  checked waypoints/lives, without sustained frame progress. `low3/review.json`
  explicitly rejects that lifecycle claim. Throw samples do not advance.
- `high` actually picks up actor63 at carry offset8316, then an observer wrongly
  expects the actor index63. It closes before carry/throw. `high2` repeats with
  the corrected, independently evidenced byte-offset rule.
- `low4` passes readiness and closes before interaction after the zero-offset
  control is found unsuitable for comparing positive-offset behavior.

Original0043EE08 adds0059B628 to the carry word;0043E82A branches differently for
nonpositive values. Zero is therefore a confounder for the original actor0 control.
`carry-word-instructions.txt` records original instruction/file offsets and
`0059d96c-xrefs.json` records native references. No claim that all actor0 behavior
is invalid is needed, nor is the stall attributed to contact64.

Read-only Linux perf sampling locates all196 CPU-clock IP samples in unchanged
0042AA5C..0042AA7E. The loop in0042AA50 cycles through64 records at00598CA8,
stride56, skipping a record when byte+51 has bit0x80 and u16+34 is nonzero. The
captured pool has those predicates true in all64 records: byte+51=229 and
u16+34 in{1,2}. There is no full-cycle termination branch. `low3/stalled-pool.json`
and `perf-ip.json` provide independent runtime evidence; loop bytes match retail.

`native-pool-search.json` executes192 original search cases: all64 starting
cursors remain in the loop after10000 instructions with the captured full pool;
clearing either tested field in one slot reaches that slot's initializer. Static
control flow, rather than an instruction timeout alone, establishes the endless
full-pool cycle. Field/object kinds remain unnamed.

No pool patch is installed. A null-return shortcut is unsafe for the covered
caller:0043EEFC calls thunk00401A9B→0042AA50 and0043EF06 immediately writes through
the result. The next bounded work is caller/owner lifetime analysis and a tested
capacity policy, with positive-offset distant-route controls to discriminate the
trigger. The current data does not establish whether dense seeds, actor0-specific
branches or other work cause saturation in ordinary profiles.

EXP011's569 indexed artifacts and13 source dependencies reverify exactly. All
private sessions are closed with scoped before/after audits. No original/PS1
changes, external live writes, debugger stops or deliberate exits occurred.
Linux perf sampling uses no ptrace or game writes.
