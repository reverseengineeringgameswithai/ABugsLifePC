---
type: experiment
id: EXP-20260907-014
date: 2026-09-07
created: 2026-09-07
updated: 2026-10-29
status: implemented-runtime-observed
environment: Wine Gamescope Direct3D preview plus offline Unicorn native PC execution
question: What causes a captured fall through a raised floor and sideways phantom pushes, and which native collision limits are involved?
result: Walls displaced from floor edges open an entry beneath raised floors (native 0x004AB1A0 reproduces; zero group markers do not disable cells); the actor-contact broad phase 0x0041CA3A..0x0041CA6B sums squared deltas in 32 bits, so extreme seed coordinates wrap to false contact. Shared wall/floor edges and a 64-bit distance guard hooked at 0x0041CA02 pass native regressions and bounded live observation.
binary_sha256: 3a2e6ca8463752463751c5eefc031e109d17e1ddaa9dc079615446b1f0454a77
evidence: [EXP-20260907-013, EXP-20260907-014, EXP-20260906-007]
tags: [experiment, terrain/collision, re/runtime, implementation/modding]
---

# EXP-20260907-014 - Cliff seam and phantom seed collision repair

Two distinct defects are **confirmed** in an authored terrace layout: collision
walls displaced from their floor edges leave an entry beneath raised floors; and
extreme-position retained seeds overflow the original actor distance check and
produce phantom pushes. Both are repaired. Report:
`reports/terrain/EXP-20260907-014.json`. PC retail executable
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878` is the native
instruction reference. No PS1 evidence, original-file changes or live memory
writes are involved.

## Floor-fall trace

`work/experiments/EXP-20260907-013/up-02-floor/floor-fall.mp4` preserves a
four-second Up hold. Trace:487 samples, 38 compositor frames. Starting world
position is `(270257,-100631,439052)`; Flik falls, dies and respawns. At1.975s
his Y reaches 98733; at2.124s he is back near `(267876,-100862,439566)`.
Frame018 is uniformly black during the death fade; no gameplay content is
claimed for it, and final settling samples were not persisted after the capture
script's postvalidation failure (`capture-status.json`).

## Confirmed cliff seam cause and repair

The eastern terrace begins at stored X8448. Its wall had been moved outward
48 units to X8400, while floor edges remained X8448. The sampled starting X is
8445.53125: inside the strip between wall and floor edge. Flik crosses beneath
the higher floor, with the collision wall behind him. Static compiler geometry
and live positions independently locate this opening. Initial supporting floor
cell is file85824, source99; the next raised-floor region includes file88552.
Stored coordinates scale by32 to runtime world coordinates.

Native movement `0x004AB1A0`, seeded from that position and contact, reproduces
the fall with repeated delta `(400,512,-680)`: old maximum below-floor gap60736
world units. Source99-only also falls, excluding scenery as necessary to this
specific failure. Moving261 cliff wall triangles back to the exact floor X/Z
edges reduces the maximum gap to89. The vertical collision offset remains
-96 stored units. The former `source99_no_walls` arm is **invalid**: zero group
markers do not disable cells. It is not used to identify the cause.

The repaired compiler emits these shared wall/floor edges. Four regression
speeds128/400/900/1800 preserve the failing old control and passing fix. A
separate native sweep lands outside and pushes at all49 generated cliff-strip
midpoints:49/49 within512 world units of the visible floor. Existing box/ramp
collision and visible geometry remain unchanged.

## Confirmed phantom seed cause and repair

Full native player controller `0x0043F9E0`, with EXP-013 player/camera state,
reproduces the next position but leaves velocity `(48,-537,-1801)` at the
position where the live sample later contains `(4004,-537,81)`. The extra push
therefore arrives later in the frame. Parent `0x004144C0` calls actor contact
`0x0041C9B0` after movement and other updates.

Fresh read-only images during normal navigation capture the relevant actor
list at `0x0059D7E0`. Replaying `0x0041C9B0` with the exact captured image and
zero initial horizontal velocity reproduces both recorded horizontal vectors:

| Capture | Culprit(s) and world position | Native/live velocity XYZ |
| --- | --- | --- |
| `side-watch-02/spike-02` | type11 at0x0059C078: `(-37834514,-2145129472,-22967450)` | `(3972,85,6132)` |
| `side-watch-02/spike-03` | final type11 at0x0059C180: `(-55904,-2145068832,-332096)`; preceding0x0059C0FC also pushes | `(4110,-54,-963)` |

Each offending seed alone reproduces its push; normal list members do not.
Stores are `0x0041CD5B` and `0x0041CD60`. The broad phase at
`0x0041CA3A..0x0041CA6B` squares signed shifted deltas and sums in32 bits.
These extreme coordinates wrap into a false near-contact result; the subsequent
native response produces the observed excess velocity. The captures are
non-atomic read-only images with matching before/after player position, not
save states. Exact native replay supplies a second evidence form.

`research/actor-contact/distance-guard.asm` is independently authored assembly.
`reimplementation/ablpc/actor_contact.py` installs its116 bytes in verified
padding at `0x004BBB00`, with a seven-byte hook at `0x0041CA02`. It checks
coordinate arithmetic overflow and a64-bit squared-distance sum before the
original contact response. Full original function identity, padding and relocation
checks reject an unsupported or already modified executable. The patch receipt
has a complete inverse. NASM/packaged-payload parity is tested.

Both captured phantom pushes disappear. Nearby native seed contact still
produces VX-512, absent seed VX0; stomping sets countdown10 and reaches the
original type5 plant constructor. [[PC seed and mushroom collision state]]
remains applicable. Objects are retained. **Inferred, not confirmed:** retained
original off-layout placements lost terrain support and entered their extreme
states; the complete lifecycle of each seed has not been traced. This fix
prevents those distant objects from influencing Flik through this contact path.

## Live observation

In a file-loaded run with both repairs (EXE
`3a2e6ca8463752463751c5eefc031e109d17e1ddaa9dc079615446b1f0454a77`, TERRAIN
`77949f180aeeeab73d3695de638344f20762ed869b2439d04ae7e14689504d21`; against the
pre-fix build, only `TERRAIN.ALL` among721 data files changes), six hardware markers, content drive, full
contact code/helper, source99 payload, mesh160, perimeter and retained plant
prefix match the files. A40-second passive trace has2643 samples, no missing
floor and maximum below-visible-floor gap138 world units, with no sample beyond
the512-unit criterion. Maximum horizontal velocity component2068. Two
change-threshold triggers are ordinary direction changes, not the earlier
oversized pushes. This is observed user play, not a matched deterministic
reproduction of the old Up route. Native exact-state A/B tests establish those
fixes.

## Checks and limits

81 unique affected tests pass after updating six obsolete full-EXE preservation
expectations to include the explicit reversible contact patch. Initial combined
run:75 pass/6 fail; corrected compiler file:20 pass. Floor-only initial11,
dependent initial57 and49/49 native sweep also pass. Logs remain in the packet.
Earlier player/current-world mixed snapshots did not contain the contemporaneous
jolt actors; their no-push outcomes do not exclude late actor contacts.

Arbitrary cliff meshes, all possible speeds/corners, complete actor placement
migration and sustained performance remain outside these bounded checks.
