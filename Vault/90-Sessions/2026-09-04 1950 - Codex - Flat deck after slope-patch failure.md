---
type: session
date: 2026-09-04
agent: Codex
status: complete-user-session-superseded
---

# 2026-09-04 1950 - Codex - Flat deck after slope-patch failure

The user reports that EXP-005's paired slope patch drops Flik through the floor
on a return walk, and that the shallow visual change is hard to distinguish
from the native slope. Recorded failed manual acceptance and corrected the
inference that the local correspondence established reliable grouping/traversal.
The earlier height/pixel observations remain evidence; the return defect's exact
cause is not yet isolated or repaired.

Read the current Vault/mission/runtime policy and reused the original loader,
movement reference, height/mesh parsers and static consumers. No delegation,
PS1 consultation or R2q work. Examined flat candidates in Level01/03/Training;
a standalone high flat deck at the natural spawn gave the clearest bounded
fixture without navigating to a distant native surface.

[[EXP-20260904-006 - Flat deck and solid block test]] retains the fixed530-byte
collision and394-byte render prefix replacements. Twelve collision triangles,
six visible quads, a broad flat deck and a block6,144 world units higher. The
new renderer terminator is confirmed at retail0045A8B0/0045A8B4 and in live
loaded/rendered data. No general encoder or shared-edge repair is claimed.

Added `scripts/terrain-deck-probe.py` and11 regression cases. Five original-
instruction cases cover flat round trip, top landing/drop/return, and top/side
removal controls.188 focused tests pass in36.66s. Existing EXP-002/003/004/005
code and reports remain intact. Full `make check` and independent audit were
not run, and no commit was made.

Closed the prior user floor-play process by owned identity, with a clean audit.
Scientific EXP-006 game38125/934393, group37881, passed loaded-data checks and
two normal jump-off-return cycles. Its clean close is retained. An additional
camera-relative repositioning moved away from the desired initial view, so a
fresh copy/prefix was launched for the user instead of handing off that view.

**Leave open:** `USER-20260904-deck-play-001`, game40214/965017, group39970,
display`:2`, window14680071, private sink`ablpc_mute_39970`. Both data files match
EXP-006; source99 and primary160 loaded prefixes are verified. Ownership of all
audit processes/helpers and the private sink is recorded in
`work/experiments/USER-20260904-deck-play-001/handoff.json`. This expected nonclean
audit describes the user's requested open game, not orphaned instances. No
automated gameplay input is sent in the fresh handoff, only menu navigation.

Report757,745 bytes, SHA-256
`4112cc7f8400f006319d603501326b1af115bccee33888c4e8cfc6022a94a91c`.
Raw game assets, screenshots, logs, prefixes and receipts remain under work.
Runtime used normal XTEST and read-only process memory, no writes, teleport,
breakpoints, freezing or save states. Historical mappings are unchanged.

Updated Current State, Environment, Known Unknowns, DEC-231, roadmaps, format
notes, MOCs and Session Index. Subsequent user feedback confirms block contact
but reports a visibility defect; see [[EXP-20260904-007 - Deck visibility and inherited depth offset]]. The
old slope-patch failure remains separate. The broad deck has finite open edges,
and native objects elsewhere can overlap it. Lightweight gates and claim sweeps
are retained with the experiment.

## Subsequent closure

The original user deck session40214/965017 was closed cleanly for EXP-008's
requested depth-offset comparison. The corrected successor is recorded in
[[2026-09-04 2021 - Codex - Block visibility cause verified and corrected]].
