---
type: implementation
status: active
created: 2026-09-26
updated: 2026-10-29
tags: [implementation/scenery]
---

# PC Anthill scenery assemblies

EXP-20260926-002 imports
the useful prop families identified by [[PC Anthill remaining object inventory]].
Original assets remain private under `work/`.

## Import of original records

The import retains original geometry and reuses only untouched disabled primary
allocations, comparing their records and object controls with the pinned base.
Secondary copies reuse untouched 32-byte allocations. All relevant original
material pages 0–4, including the late page 3 RAW packet at `0x46CD9`, are
decoded. The native mesh reader (`stored_scenery_mesh.py`) preserves the
negative-count plant's entire 656-byte auxiliary span. Its meaning and
interactive role remain **unknown**; it retains its original near renderer and
has no invented collision or distant counterpart.

## Collision evidence and limits

A first import with simplified visual-derived surfaces left rock, thornbush and
offering-leaf collision missing in a hardware preview; its passing isolated
contact samples had not established complete surface coverage. The revision
restores these original PC profiles:

| Visual primary records | TERRAIN source | Original record offset | Payload offset | Payload bytes |
|---|---:|---:|---:|---:|
| 131 + 132, offering assembly | 88 | 229264 | 2044 | 5608 |
| 245, thorny vine | 90 | 229416 | 15020 | 3708 |
| 315 + 438, curved stone/branch | 130 | 232456 | 144980 | 5804 |
| 120, large stone | 157 | 234508 | 188312 | 1476 |
| 45, forked twig | 169 | 235420 | 204748 | 2184 |
| 14, loose leaf (EXP-20261005-004) | 127 | 232228 | 140156 | 1548 |
| 209, hollow plant (EXP-20261005-004) | 87 | 229188 | 988 | 1056 |
| 227, broad leaf (EXP-20261005-004) | 175 | 235876 | 213992 | 1932 |

**Confirmed:** the original payloads and all descriptor fields except XYZ are
retained byte for byte. Visual objects and collision descriptors receive the same
translation. Original DAT hash starts `786b7a96`; terrain hash starts `62f3b73f`;
full hashes and final locators are in the experiment packet.

**Geometric correspondence:** 131/132 share object origin `(8192,-8192,24576)`;
source 88 encloses their combined original footprint. Sources 90, 157 and 169
closely follow the posed vine, stone and twig with the original contact margins.
Source 130 includes the curved stone and nearby branch. These are spatial/native
control correspondences, not a newly discovered explicit scene-to-terrain link.

**Leaves and hollow plant (2026-10-05):** EXP-20261005-003
found that the loose leaves, hollow plant and yellow leaves had no collision
and the broad leaves only an authored one, although the original gives each
its own. EXP-20261005-004
binds the three shells above. It also binds each yellow leaf
(196/197/198/201) to its original kind-0x101 loop
(183/182/181/179). The loop is a 4-segment, side-blocking strip round the
stem with no top; only the points' X/Z move. Animated leaves and the
auxiliary-data plant may be solid because their collision is original;
shoots, sprouts and daisies have no original collision.
Native walks and matched hardware arms show the original behaviour.

Static props without a paired original profile need authored shells; those are
approximations, not recovered original collision. Full traversal, all approach
directions and damage/interaction semantics are separate from a successful
import or isolated contact sample.

## Capacity

The shared DAT cap was 1,179,648 bytes at the time of this import, which left
352 bytes free (DAT 1,179,296 bytes); EXP-20260928-001 raised that shared cap to
1,441,792 (`terrain_scenery.MAX_BYTES` = `0x160000`). Combined DAT/terrain/plant
use was 1,944,558 of 2,000,000 bytes and the static collision bound 234 of 300
(EXP-20261005-004: 1,948,358 bytes, bound unchanged). Existing resource limits
remain in force. More ground or unrelated terrain fragments require their own
capacity check.
