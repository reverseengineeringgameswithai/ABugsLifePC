---
type: experiment
id: EXP-20260906-007
date: 2026-09-06
status: bounded-repair-confirmed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 43 original-PC Unicorn probes and isolated Wine hardware-rendered runtime
question: "Why does seed collision survive while opened-mushroom exclusion and bounce disappear in the isolated terrain fixture?"
result: record8-restoration-recovers-mushroom-exclusion-and-bounce
tags:
  - re/experiment
  - terrain/collision
---

# EXP-20260906-007 - Plant-state collision regression

Date: 2026-09-06

Status: confirmed for the observed type 5 mushroom; repaired varied-grass preview open for the user. Other plant states remain outside this result.

## Confirmed result

The seed and opened mushroom use different collision paths. The seed is general actor type 11, with its own shape handled at `0x0041C9B0`. The mushroom is plant actor **type 5**, selecting **PLANTTER source record 8**, not type 7 / record 10. Its transition and dynamic descriptor were already correct in the failing control; the descriptor pointed to an emptied template. Restoring only `PLANTTER.ALL[0x2650:0x2652]` from `ff ff` to `01 00` recovers lateral exclusion and contact-dependent bounce. No other plant template, high `0x104` stream, removed terrain, or unknown byte is restored.

Evidence: original PC constructor `0x00467E60`, registration `0x0044CA00`, movement `0x004AB1A0`, bounce store `0x00468406`; paired original-instruction report `work/experiments/EXP-20260906-007/native-03.json`; fresh failing-control and repaired-runtime receipts below. Mechanism: [[PC seed and mushroom collision state]]. Public summary with full file hashes: `reports/terrain/EXP-20260906-007.json`.

## File census and minimal edit

Decimal offsets relative to `CD/BITS/PLANTTER.ALL`; size 17760, directory offset 16692. Records 0–12 are kind 8, record 13 is opaque high kind `0x104`; all have clone flag `+0x46 = 0`. Original/stripped directories are identical. Original-to-stripped changes total 30 bytes: two-byte first markers of 13 low-kind payloads and four bytes in the high payload. All stripped low-kind records have zero active groups/cells.

| Record | Payload offset | Size | Original groups / cells | Source +0x1a | PC plant type |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 4 | 2476 | 14 / 72 | 34 | 1 |
| 1 | 2480 | 844 | 14 / 21 | 43 | 10 |
| 2 | 3324 | 1476 | 16 / 40 | 44 | 11 |
| 3 | 4800 | 772 | 16 / 18 | 45 | 12 |
| 4 | 5572 | 748 | 14 / 18 | 46 | 13 |
| 5 | 6320 | 388 | 8 / 9 | 47 | 14 |
| 6 | 6708 | 1540 | 16 / 42 | 35 | 2 |
| 7 | 8248 | 1560 | 15 / 43 | 37 | 4 |
| 8 | 9808 | 964 | 16 / 24 | 38 | 5 |
| 9 | 10772 | 136 | 3 / 3 | 39 | 6 |
| 10 | 10908 | 772 | 16 / 18 | 40 | 7 |
| 11 | 11680 | 2412 | 14 / 70 | 41 | 8 |
| 12 | 14092 | 2584 | 15 / 75 | 42 | 9 |
| 13 | 16676 | 16 | opaque high stream | 0 | not assigned |

The type column follows the PC loader's `source +0x1a = type + 33`, not appearance. Per-record allocation/directory hashes are in `native-03.json`. Original SHA-256: `0a0cf7fa9e110eef8e2112760dcbefaa433b391ca613a3d673ee0327767eb468`; stripped SHA: `c7fadbec78ac2c35f880c0dd5025e86a12604482c01dd93be38a90f6ad2d0cc9`; repaired SHA: `c8251790b317e0458525d898237a54a88d473aac0758d01f36effcebeb38a762`.

`terrain_plant_templates.py` requires matching size/directory/suffix, explicit ordered unique selections, non-clone low kinds with established template IDs, a nonempty bounded donor, and full-allocation equality to `ff ff + donor[2:]`. Only then does a compare-guarded patch restore the selected marker. Tests reject malformed offsets/counts, bad selections, active/empty donors, and changed unknown bytes. Candidate `work/copies/EXP-20260906-007/record8-fixture` keeps first-grass LEVEL.DAT and authored TERRAIN.ALL unchanged.

## Original-PC discriminator

`scripts/terrain-plant-probe.py` executes original retail instructions and data in private Unicorn memory. Input receipt: `control-01/receipt-1788739476760182883.json` under this experiment's private directory; its seed shape equals the original executable's data. This is not live intervention or a decompiler-based reimplementation.

Paired results from accepted `native-03.json`, 4.920093888 seconds, SHA `0627682b5a07d04952086321706179d69f714bc4d0bc2d785867c0e21995ae66`:

- Seed present/absent yields velocity `(-512,0,0)` / `(0,0,0)` in both arms. Stomp sets seed `+0x6c = 10`; the tenth countdown tick calls the constructor. The slice stops before seed-list removal.
- Observed placement selectors `(0,0)` and global bytes `(17,0,0,0,0,0)` select type 5. Animation reaches flag bit 2 after 15 ticks. Both arms register descriptor `N+2 = 193` (`N=191`), tag 108, origin `(197902,-102403,561505)`, template descriptor 186 / source record 8. Control bounds are `(197870,561473,32,32)` because the first marker is `-1`.
- Four X/Z approaches cross the centre in the control (final signed distance `-7000` each); repaired distances `9617,9905,9894,9784` show exclusion/deflection in all four tested approaches.
- A 140-tick landing gives 0 versus 6 bounces. Events are actual execution of the velocity-store instruction, not merely matching velocity. Continuous departure, floor settling and jump-return preserve the route: both settle on source 99; return gives 0 versus 1 bounce.

Limits: synthetic physics cadence/gravity and jump impulse; input interpreter, rendering and `0x004148A0` audiovisual dispatch excluded; visible flag supplied from runtime state. `native-01.json` is rejected: omitted original `0x00467D70` reset left zeroed bounce history and selected a combo impulse. Corrected probes execute that reset. `native-02.json` passed the earlier contact/bounce gate; `native-03.json` adds countdown and continuous return. These are finite original-instruction tests, not full-loop emulation.

## Live comparison

Fresh first-grass control `control-game`: game 223411/start2191763, group223167. The user opened the seed and reported penetration/no bounce. Read-only census found slot2/type5/descriptor193 with correct origin but empty record8. Context frame `control-01/frame-1788739333337497247.png` SHA `91da3846f5334b1b414c3c6df7631d3b240ff02b54368dd67a10128b4ccaca8b` shows the overlap. This arm is CLOSED: after ignored normal close, exact PID/start-guarded termination removed owned processes/helpers/sink; final audit zero. Receipt `control-01/close-receipt.json`.

The repaired arm uses banked EXP-006 varied LEVEL.DAT byte-for-byte (`548c58717a92ced0f58e1ff4ab618746f624663ea97fa8649eb549f260eb6e93`), unchanged authored TERRAIN.ALL (`56c167c1786b9fa3bf91963efd5334996a8e6a28d8ca633b66aefacdde9f02ba`) and only the record8 restoration. Both launches use the established auto-hardware/spawn image `9d406ac0a1319ba58c9637eb51a45f499c2a0f901c674ce36e5d1d7aebb35ffe`, not unchanged retail code. Six hardware markers, isolated R: root and normal Training -> Anthill -> Level One menu checks passed. Initial black startup captures were rejected before input; later valid Training captures were used.

Evidence root: `work/experiments/EXP-20260906-007/repaired-variety-01/`.

- `receipt-1788739931237073241.json` verifies full source99 floor, eight-segment barrier allocation, 39886-byte varied mesh and retained PLANTTER prefix through offset16691. Prefix base7224921; record8 pointer7234729. Earlier whole-file check `receipt-1788739880308512930.json` was overbroad: directory area beginning16692 is not retained. Loader cursor advancement `0x004A8800..0x004A880A` supports payload-only verification; exact later writer into that area is unknown. Do not claim whole-file RAM equality.
- User opened the repaired mushroom and reported it works and can be jumped onto. Census again finds slot2/type5/source8, now marker1, origin `(198428,-102403,570546)`, bounds `(188828,560914,19296,406272)`. The large conservative Z bound is observed, not normalized.
- Requested three-second Up: `receipt-1788739880254283757.json`, position `(188856,-102400,569759)` -> `(191829,-102403,577146)`. Flik stays against the exterior while sliding around the side; not a fixed-position or all-direction proof.
- Normal jump (Shift 0.15 seconds with Right 0.45 seconds, then released): `receipt-1788739935331279279.json`, SHA `db4aae9cf05c6dc027724371796ddee75ee04a99b032ba597e1bbbfff661819c`. 262 samples / 3.989633473 seconds show source99 -> descriptor193, cells at PLANTTER offsets10300/10344, and **five distinct bounce onsets at upward velocity -3328**; minimumY -133049. This agrees with the native-store proof but is not a live instruction trace.
- Later passive frame `frame-1788739968354683444.png`, SHA `6f87acad6680f6482092ad09bbe2e6b5b572f3f52e17ad19c6e24be2547b718b`, brackets floor pose `(189852,-102401,576129)`, source99, flags257, Vy0. Sampling/captures are asynchronous; subsequent user pose is not guaranteed.

## Validation and handoff

40 plant tests pass in5.01s (`plant-tests.xml`); five-file terrain gate72 pass in26.76s (`terrain-gate.xml`), four workers/repo-local scratch. No R2q/full-suite or commit. Private binaries/assets/captures stay under `work/`; originals and protected stash untouched.

Repaired-variety preview deliberately OPEN: game **231286/start2242744**, group/leader **231047/start2242595**, Gamescope **231050/start2242596**, Xwayland **231083/start2242620**, display`:2`, window14680071, sink `ablpc_mute_231047`. Stage `work/copies/EXP-20260906-007/repaired-variety-game`; prefix/controller under `repaired-variety-01`. `live-handoff-binding.json` accounts for14 owned processes via exact prefix/group/start and socket peer. Generic audit is not clean (7 unattributed processes/1 sink); these are the deliberate preview, not fixture-ledger evidence. Keys released. No live writes, process stops, registers, teleport, debugger or save states.

Next: user play/varied-grass aesthetic feedback. Other plants, high0x104, general isolation policy, projectile equivalence and inherited lower-ramp corner limit remain separate. See [[2026-09-06 - Codex - Mushroom collision restoration and varied grass]].

## Historical investigation plan and initial evidence

The following sections preserve the initial unresolved state. The confirmed result above supersedes their pending gates; do not repeat completed work.

## Question

Why does the isolated authored Level01 fixture retain collision on the unopened seed but lose both lateral exclusion and bounce after that seed becomes an opened mushroom?

## Control and provenance

- Parent fixture: EXP-20260906-006 first grass preview, built from the isolated EXP-20260906-005 playable area.
- Authoritative runtime: Windows PC executable under the identity-guarded Wine/Gamescope procedure.
- The preview used `LEVEL.DAT` SHA-256 `0cd3e85e5bc65c2791a05c5435c05ca194fb0d2508f45233bed325a5c3566b44`, `TERRAIN.ALL` SHA-256 `56c167c1786b9fa3bf91963efd5334996a8e6a28d8ca633b66aefacdde9f02ba`, and stripped `PLANTTER.ALL` SHA-256 `c7fadbec78ac2c35f880c0dd5025e86a12604482c01dd93be38a90f6ad2d0cc9`.
- Private live context is retained under `work/experiments/EXP-20260906-006/grass-preview-01`. Frame `frame-1788737356120204591.png` has SHA-256 `4b259e5cb7fa3fa97b97b289065cb6573e8519b070661c2eeb54f623f754bf11`.
- The session is closed. The final `make session-audit` was clean.

## Observations

User runtime observation:

- Before transformation, the seed has collision and Flik is blocked as expected.
- After Flik opens it into a mushroom, the mushroom does not push Flik out; the user could place Flik inside its visible volume.
- Jumping on the opened mushroom does not trigger the expected bounce.

The assistant did not yet record an input/contact trajectory for those transitions. The contextual capture changed from `(235072, -102402, 452424)` to `(233390, -102402, 451980)` while being acquired and retained source-99 floor contact, so it is not an atomic proof of mushroom collision state.

Static clue:

- `reimplementation/ablpc/terrain_isolated.py` deliberately empties non-kept tag 6/7/8 payloads and unlinks high `0x101`/`0x104` streams.
- The isolated build applied that operation to both `TERRAIN.ALL` and `PLANTTER.ALL`. The visible actors and plant models remain, but their original triangle templates are not active.
- Banked EXP-20260904-002 evidence mapped PC object types to PLANTTER template records, including type7 to record10. At planning time the visible mushroom had not been identified. The completed experiment establishes type5/source8 instead; record10 remains a different template.

## Competing explanations

- The opened state registers a dynamic triangle descriptor from an emptied `PLANTTER.ALL` template, while the seed uses a different actor collider.
- The transition creates the right descriptor but with a stale or incorrect origin/transform in the isolated layout.
- Solid contact and mushroom bounce are separate systems and both were lost for different reasons.
- The rendered mushroom is present but its collision-state transition is never registered.

The working seed state contradicts a blanket claim that all plant collision is disabled. The missing lateral contact and missing bounce make a purely render-only mismatch unlikely, but they do not establish one shared cause.

## Discriminating experiment

1. Parse original and isolated `PLANTTER.ALL` side by side. Enumerate records 0 through 13, exact payload offsets, kinds, counts, first changed bytes, clone identities, and the unlinked high stream. Preserve every unknown byte.
2. Establish the opened mushroom's PC object type and template record using static call-site evidence plus a read-only runtime descriptor census. Do not infer the mapping from appearance.
3. Record original-PC instruction trajectories for seed approach, opening, lateral approach to the opened mushroom, landing, bounce, step-off, and return. Include contact source/descriptor transitions and vertical motion.
4. Build a bounds-checked candidate that restores only the established tag 6/7/8 template bytes. Keep Level01's removed terrain collision empty and keep high `0x104` unlinked unless independent PC evidence requires it.
5. Use native probes and synthetic fixtures to prove malformed offsets/counts are rejected and unknown fields are unchanged.
6. In a fresh file-loaded runtime copy, repeat the complete seed-to-mushroom route. A solid-contact fix without bounce is contradictory evidence for separate systems, not a partial proof of a unified mechanism.

## Constraints

- No PS1 evidence is needed for this PC-native question.
- No memory writes, teleport, debugger control, or save-state manipulation without fresh explicit authorization for that exact use.
- Keep the EXP-006 stripped `PLANTTER.ALL` as the failing control.
- Use individual affected terrain tests and the five-file focused terrain gate during implementation. Do not run the R2q proof suite during ordinary terrain iteration.
