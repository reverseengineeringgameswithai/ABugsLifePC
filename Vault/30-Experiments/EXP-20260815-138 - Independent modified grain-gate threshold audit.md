---
type: experiment
id: EXP-20260815-138
date: 2026-08-15
question: Do EXP-137's two modified physical threshold claims survive an independent offline hard-truth audit?
status: accepted
binary_sha256: 69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b
environment: Fedora Linux 44; offline review of retained PC-native Wine 11 and Gamescope 3.16.25 evidence
configuration: exact clean worker HEAD b13b27e7c3ca64e1035793fbd56bc7baf49ed348; no runtime launch or target mutation
artifacts:
  - dynamic/wine/EXP-20260815-137-receipt.md
  - work/copies/EXP-20260815-137-grain-gate-runtime/evidence/hashes.sha256
  - work/copies/EXP-20260815-137-grain-gate-runtime/grain_gate_probe.c
addresses:
  - "0x00432B30"
  - "0x00433790"
  - "0x004DA9C8"
  - "0x0059A5B0"
  - "0x0059D910"
  - "0x0059D920"
  - "0x0059D960"
  - "0x0059D9B1"
  - "0x0059F020"
  - "0x0059F030"
  - "0x00861C84"
result: accept-exact-tunnels-row3-and-city-gate0-boundaries
created: 2026-08-15
updated: 2026-08-15
tags: [re/experiment, re/runtime, re/audit, mod/gameplay]
---

# EXP-20260815-138 - Independent modified grain-gate threshold audit

## Verdict and authority

**ACCEPT**, limited to Tunnels resident row 3 at the tested point and City
Entrance gate index 0 at the tested fixed trigger point. This is an offline
independent audit of PC-native evidence. No game, Wine, Gamescope, debugger,
or helper was attached to a live target, and no game state or target bytes
were changed.

The exact user wording authorized the below-minimum then exact-minimum test
(`yes, please do this`), delegated the mechanical approvals (`the approvals
are up to you` and `Assume yes for me`), and had already authorized teleport
and grain setup (`teleporting Flik, giving him grain if he needs it`). The
accepted writes therefore satisfy the manual's prior explicit-approval rule.

## Artifact and helper integrity

At exact clean worker HEAD
`b13b27e7c3ca64e1035793fbd56bc7baf49ed348`, the ignored packet contains no
links. `evidence/hashes.sha256` itself is
`4bbd20c1bceb2810490d705f08eb1a30c26ffab21989062a247b7487c8081b2c`;
all 69 listed files rehash successfully from repository root. The tracked
receipt formerly called it the complete raw-file manifest even though the two
packet-root helper files are deliberately outside it. The receipt now says
the exact truth: it is the complete `evidence/` manifest, while the helper is
pinned separately.

The final helper source and binary independently rehash to
`7d4332399debef6bfd0aa056f6585d4ab82b4829987f72b05a1d0a90ed6a592a`
and `fc441f4f2cd30cb9225469db010d76abe90b578aa104ea3fef84429eadbf5149`.
Compiling the reviewed source with the recorded
`gcc -std=c11 -O2 -Wall -Wextra -Werror` command reproduces the binary
byte-for-byte. Removing only the later City fixed-point operation reconstructs
the earlier source exactly at its recorded
`1e456b047d390fcc6b827c659d8ac59ace97dd0a0970bd2d8a4ef00e5e2c5442`.
The earlier compiled binary is not retained, so its separately stated hash
was not independently rebuilt; the snapshot, guarded grain-write, and
Tunnels-position functions are byte-identical in the reconstructed and final
sources. That limit does not create a contradictory behavioral receipt.

The helper uses exact-width `process_vm_readv`, refuses read failure, rejects
nonpositive/invalid arguments, checks internal level and current grain before
a grain write, limits each position operation to current plus preceding XYZ,
requires a 24-byte syscall and exact readback, and never writes auxiliary,
gate state, animation, life, registers, or code. Offline nonexistent-PID and
invalid-argument attacks return nonzero without a write.

## Executable recipe and static join

The retail work-copy executable remains 1,069,056 bytes at
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
An independent in-memory build with Tunnels `(1..9)` and City `(1,2,3)`
reproduces the exercised same-size output
`69881871c7b21d076a12585c62957efc700d33d2dfe7ea7118cf799459de284b`,
100 touched bytes, 46 changed bytes, and the existing work-copy byte for byte.
Reversing every guarded span reconstructs retail exactly. Both modified
Tunnels image/template tables contain requirements `(1..9)`, and the City
replacement reads `(1,2,3)` through the exact index.

Modified x86 independently confirms the behavioral discriminators:

- `0x00432F0C` reads unsigned grain byte `0x0059D9B1`, `0x00432F12` compares
  it with row `+0x08`, and the open branch is count-at-least requirement. It
  then arithmetic-shifts current-minus-row X/Z by eight and requires their
  squared sum to be below `0x2710` at `0x00432F49`.
- For current `(501696,494016)` and row-3 `(509676,510143)`, those shifted
  differences are `-32` and `-63`; the exact squared distance is
  `1,024 + 3,969 = 4,993`, genuinely below 10,000.
- `0x004337D1` reads the same unsigned grain byte, `0x004337D8` indexes the
  modified City lookup, and `0x004337E1` opens only when grain is at least the
  selected requirement. `0x00433944` calls the routine with index 0, joining
  the first state/animation slots to configured value 1.

## Runtime falsification

All three retained identity files name the same 1,069,056-byte profile and
the exact work-copy mapping/inode. Tunnels PID `178570`/start tick `2885702`
loads internal level 3; corrected City PID `182338`/start tick `3007022` loads
internal level 4. Their complete game logs contain all six current hardware
markers in one log, the correct level files, `---End InitMainGame---`, and
`NextLife`. Neither contains `SYSTEM MEMORY ONLY` or `INITSOFTRENDER` as a
selected path.

For Tunnels, the guarded 24-byte setup and snapshots all use PID `178570`.
At invariant current/preceding/auxiliary
`(501696,30092,494016)`, grain 3 leaves row 3 type `0x10C7`, distance 4,993,
and `NextLife=0`; the 640x480 frame shows the upright closed gate. The only
between-condition write receipt is one byte `3 -> 4`. The settled snapshot
retains all three triples and `NextLife=0`, changes only the relevant observed
row type to `0x0690`, and the paired frame shows the gate lowered/open. The
resident requirement remains 4 throughout.

For City, the corrected control uses PID `182338` throughout. After one
guarded current-plus-preceding setup, engine adoption makes all three triples
`(-87622,917,-182181)` before the discriminator. At grain 0 the triples remain
fixed, `NextLife=0`, states are `(-1,-1,-1)`, all animation values are zero,
and the 640x480 frame shows the closed gate. The only between-condition write
is one byte `0 -> 1`. At the same fixed triples, state 0 moves through 28 with
animation pair `-128/+128`, then settles at 0 and `-1024/+1024`; the paired
frame shows the gate open and `NextLife` remains zero.

The earlier PID `180056` City route is correctly limited. Its saved approach
`(-92603,1098,-181281)` keeps state `-1` at count 1 and is not acceptance
evidence; an ordinary step first produces index-0 state 25 at the later
trigger point. The later 320x200 `SYSTEM MEMORY ONLY`/`INITSOFTRENDER`
candidate is also expressly rejected before target write. Repository-wide
wording does not promote either failed isolation arm or generalize beyond row
3/gate 0.

## Lifecycle, repository, and result

Both Wine `Y:` mappings resolve to
`work/copies/BUGS_PC-full-disc`. The exact game/Gamescope/Wine/helper/launcher
process audit and private-null-sink audit are empty. `originals/` has no
tracked content, the raw packet remains ignored, no protected/game-bearing
artifact entered Git, and the work-copy retail hash is unchanged.

Validation passes:

- raw manifest: 69/69;
- final helper rebuild: byte-identical; earlier helper source reconstruction:
  exact hash;
- executable profile/inverse: exact; focused grain-gate tests: 12/12;
- complete `make check`: Python doctor passed, Vault 400/0/0, all five M4
  anchors valid, 588 tests passed, tracked-file audit 0;
- `git diff --check`, work/original boundary, process, sink, and Wine-mapping
  audits: clear.

KU-060 is resolved only for the demonstrated Tunnels row-3 `3 closed / 4
open` and City gate-0 `0 closed / 1 open` boundaries. Tunnels rows 0–2/4–8,
linked rows 0/4, City gates 1/2, controller reachability of the write-assisted
setups, numeral assets, persistence, and other executable versions remain
open. M3 remains Complete; M2/M5 remain Deferred and M4/M6 remain Complete.
