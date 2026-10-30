---
type: experiment
id: EXP-20260815-126
date: 2026-08-15
question: Does a user-driven control Level03 route naturally contact collision value 1 and request the row-6 reset path?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; Wine 11 Staging; Gamescope; retail PC control work copy
configuration: user manual play; read-only 100 ms process_vm_readv trace; no debugger attach or writes
artifacts:
  - work/copies/EXP-20260815-126-manual-level03-probe/
addresses:
  - 0x0059D960
  - 0x0059D9A0
  - 0x0059A5B0
  - 0x007F3D68
result: bounded-manual-route-negative-natural-producer-open
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/runtime
  - re/gameplay
  - milestone/m3
---

# EXP-20260815-126 - Manual Level03 coordinate-guided probe

## Question and boundary

Can the researcher manually drive the unchanged PC control copy through
Tunnels toward the known descriptor-571 region, naturally contact collision
value `1`, and produce the `0x10`/`NextLife` reset path without relying on the
currently non-deterministic keyboard movies?

The running executable and `LEVEL03/LEVEL.DAT` matched retail/control SHA-256
`97c95ba5...b878` and `bda28dc7...0f2b`. The one-byte row-6 candidate was not
mounted. PGID `68047`, game PID `68289`, and private sink
`ablpc_mute_68047` were owned by this arm. All four Direct3D gates passed and
no `INITSOFTRENDER` marker appeared.

## Procedure

The user selected Tunnels and played manually while the prior
`m3_ku057_watch.c` sampler read actor coordinates, raw flags, `NextLife`, the
state counter, internal level, current collision index, and current collision
descriptor value every 100 ms. It did not attach, pause, set breakpoints, or
write memory/registers/code.

The sampler's existing nearest-material auxiliary scan begins from dynamic
base 602 and does not cover descriptors 570–578. Those auxiliary columns are
therefore ignored. Current collision index/value and the other direct fields
remain usable.

## Result

The accepted 100 ms trace contains 4,105 rows, including 3,750 live Level03
rows. It records the red-mushroom transition and upper-corridor traversal,
then samples auxiliary X/Z `(451089,507761)` approximately 36,378 units from
the then-mislabeled scanner tuple `(471712,537728)`. EXP-131 proves that tuple
is descriptor 572's base, not descriptor 571's.

At trace time 150,937 ms, the sampled auxiliary coordinate triple
`(410898,31962,469378)` retained current
collision index/value `552/0`, while flags briefly became `0x0002` and the
state counter changed `4 -> 3`. The user reported that this probably matched a
health loss. That semantic interpretation remains **inferred**; the raw
transition is confirmed.

Across the bounded live Level03 window:

- current collision value `1`: 0 rows;
- raw flags containing reset-request bit `0x10`: 0 rows;
- nonzero `NextLife`: 0 rows;
- counter transition after initialization: only `4 -> 3`;
- observed current collision indices included 324, 530, 542, 548, 552,
  559–562, 602, and 603.

The researcher changed the work plan before deliberate contact at the target
height, so this is a bounded negative, not route exhaustion and not evidence
that collision value `1` is unreachable.

## Evidence and lifecycle

- Trace SHA-256:
  `50dd0350cf65a70eec161d4a2f2e7ff1b76ea6c6eaf6484103086483aaca8ed9`.
- Sampler-source SHA-256:
  `5eaccdbb8afd81059a37de9f8ddbeead9eb22b3c34a98beabf6fdc6b93a98924`.
- Raw ignored evidence:
  `work/copies/EXP-20260815-126-manual-level03-probe/`.

On close, exact PGID `68047` received `SIGTERM`. Owned reaper PID `68209`
remained after the bounded wait and was force-closed by exact PID. The private
sink unloaded, no game/Wine/Gamescope/overlay process remained, and Wine `Y:`
was restored to its pre-arm target.

## Conclusion

`KU-057` remains open. This arm adds one natural raw damage-like transition
but no collision-value-1 or reset-path event. The next manual attempt should
use [[PC coordinate overlay]] to expose live coordinates to the researcher and
retain a separate read-only trace for evidence.

## 2026-08-15 coordinate-source correction

[[EXP-20260815-128 - Live Flik position globals]] proves that the sampler's
`0x0059D960` triple is auxiliary/reset-coordinate state, not current airborne
Flik XYZ. Therefore this experiment's exact coordinates and distance to the
then-mislabeled scanner tuple are accepted only as auxiliary ground-route steering values; they are
not a current-position trace. The visually observed route, collision
index/value, flags, counter, and `NextLife` results are unaffected. Future
KU-057 traces must read current XYZ at `0x0059D910`.

## 2026-08-15 route-hypothesis correction

[[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]] later
separates the black spider from the natural material-1 reset path. The spider
used current descriptor/value `543/0`; the first grain-gate pit used `572/1`
twice. The old scanner attribution to descriptor 571 is invalid; EXP-131 maps
its actual base to `(470112,64224,-423840)` and maps the hypothesized tuple to
descriptor 572/the first grain-gate pit. This preserves the raw bounded-
negative observations here while retiring the descriptor-571/spider steering
hypothesis.
