---
type: experiment
id: EXP-20260815-130
date: 2026-08-15
question: What position writes safely teleport Flik in Level03, and can an inaccessible pit teleport count as natural row-6 reset evidence?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; Wine 11 Staging; Gamescope 3.16.25; Direct3D 640x480x16; Level03 Tunnels
configuration: user-authorized process_vm_writev position edits; 5 ms process_vm_readv observer; fresh owned work-copy arms
artifacts:
  - dynamic/wine/RUN-KU057-20260815-192558/metadata.json
  - dynamic/wine/RUN-KU057-20260815-192558/selected-events.tsv
  - dynamic/wine/RUN-KU057-20260815-192558/write-receipts.txt
  - dynamic/wine/RUN-KU057-20260815-192558/helper-hashes.txt
addresses:
  - "0x0059D910"
  - "0x0059D920"
  - "0x0059D960"
  - "0x0059D9A0"
  - "0x0059A5B0"
  - "0x007F3D68"
result: safe-known-floor-teleport-bounded-unsupported-equal-current-preceding-unsafe-ku057-unchanged
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - re/runtime
  - re/safety
  - milestone/m3
---

# EXP-20260815-130 - Write-assisted Level03 teleport safety boundary

## Question

Can the confirmed current, preceding, and auxiliary position triples be used
to teleport Flik safely in Level03? Does forcing Flik into the already-known
grain-gate pit supply the still-missing natural row-6 event?

## Authorization and evidence boundary

The user explicitly authorized teleporting Flik and adding grain if needed.
Every accepted arm used an exact-retail-hash work copy in Direct3D Tunnels,
with PID, process group, start time, CWD, internal level 3, window focus, and
renderer gates checked. The writes were runtime diagnostics, not unchanged-
state gameplay. No grain write was needed or made.

The first Tunnels arm wrote 36 bytes in one `process_vm_writev` call, setting
current, preceding, and auxiliary XYZ to `(501696,65000,494016)`. A brief
ordinary Right hold began a fall, `NextLife` became 2, and the engine repeatedly
returned to the written auxiliary point. Collision remained descriptor/value
`548/0`. The loop consumed lives and was a procedure error, not useful death
evidence.

## Known walkable-floor control

A fresh Level03 arm began at `(-16896,32043,6631)`. One 24-byte write changed
only current and preceding XYZ to the previously confirmed row-6 floor/reset
point `(501696,30092,494016)`. Readback left auxiliary at the original spawn.
About 10.1 ms later, the engine itself copied the stable target into the
auxiliary triple while flags remained `0x0008`, `NextLife` remained 0, and
collision remained `548/0`. Flik stood visibly on walkable terrain near the
first grain gate.

This confirms a bounded safe teleport recipe only when the destination is
already known to be walkable. It also confirms that omitting the auxiliary
triple does not guarantee that it will remain unchanged.

## Unsupported-point falsification

From that stable floor control, a second 24-byte write changed current and
preceding XYZ to the prior natural pit-contact tuple
`(494438,68730,526143)` while auxiliary initially remained at the safe row-6
point. About 10.1 ms later—before the captured fall request—the engine copied
the unsupported target into auxiliary. The later transition used
descriptor/value `548/0`, flags `0x0004`, and `NextLife=2`, then returned to
the same bad point and repeated.

The user correctly noted that zero-grain Flik cannot reach the pit normally
because the grain gate blocks access. This arm is therefore write-assisted
and cannot satisfy KU-057's natural-gameplay requirement even if it had
produced material 1. It did not: the complete selected trace contains zero
collision-value-1 samples.

## Conclusion

Confirmed at this exact boundary:

- a current+preceding write to a known walkable point can relocate Flik;
- the engine may adopt equal current/preceding as the auxiliary reset point
  within one observed approximately 10 ms interval;
- writing all three triples, or writing equal current/preceding to an
  unsupported point, can create a life-consuming reset loop;
- teleporting past a closed grain gate is diagnostic state injection, not a
  natural death or controller-reachable route.

The natural first grain-gate pit remains the row-7 producer established by
[[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]]. EXP-130
does not change KU-057 and supplies no new row-6 natural-selection evidence.
The next honest M3 step is a different naturally reachable material-1 surface
inside row 6's nearest region, or explicit milestone disposition of that
remaining requirement.

## Contradictions and limits

The planned assumption that omitting auxiliary would preserve a safe reset
anchor was falsified. No paused/single-step/current-only recovery method was
accepted in this experiment; do not present one as validated. The approximately
10 ms adoption time is a wall-clock observation from a 5 ms sampler, not an
engine-frame measurement. “Walkable” is confirmed only for the exact Level03
floor target used here.

One setup arm accidentally loaded Training after a stale instruction was
carried forward. It made no target write and was rejected. Two earlier setup
arms were also rejected before any write: one used software rendering and one
had no internal game-window focus.

## Lifecycle

All game/Wine/Gamescope groups, private sinks, and rejected setup arms were
closed. Targeted audits were empty. Wine `Y:` points to
`/home/dev/ABLPC/work/copies/BUGS_PC-full-disc`. No original, executable,
asset, or disc image was edited. The disclosed position writes were volatile;
ordinary work-copy log/Wine runtime churn is outside this claim.
