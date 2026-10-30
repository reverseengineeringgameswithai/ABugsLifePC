---
type: session
date: 2026-08-15
agent: Codex
status: completed
tags: [session, milestone/m3, re/file-format]
---

# 2026-08-15 2005 - Codex - Level03 collision geometry disposition

Refreshed [[START HERE]], current authorities, and the active M3.5 packet.
Traced the PC `TERRAIN.ALL` source directory and collision bounds through
`0x004A8410` and `0x004A8950`, then corrected EXP-118's 16-byte descriptor-row
misalignment.

Added the lossless read-only [[PC TERRAIN ALL inspector]] and its focused tests.
The exact Level03 map assigns result-1 descriptors 570–578 to nine spatial
regions paired with the 18 type-1 rows. Descriptor 572 is the sole rows-6/7
region and matches the natural grain-gate pit; both EXP-129 contacts lie on
its row-7 side. No second row-6-near result-1 descriptor exists.

Recorded [[EXP-20260815-131 - Level03 collision geometry and M3.5 disposition]]
and explicitly disposed of natural row-6 selection as an M3.5 blocker without
claiming it impossible. No runtime process, game input, memory write, asset
edit, or original-file access occurred. The next milestone action is final M3
exit-gate reconciliation, not another Tunnels pit probe.

Final validation: 576 tests pass; Vault lint reports 380 notes, 0 errors, and
0 warnings; M4 compatibility and tracked-file audit pass.
