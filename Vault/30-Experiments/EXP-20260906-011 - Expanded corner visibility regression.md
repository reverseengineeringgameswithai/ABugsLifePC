---
type: experiment
id: EXP-20260906-011
date: 2026-09-06
status: diagnosed-fix-not-installed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 43 isolated Wine hardware preview and original PC instructions under Unicorn
question: Why does expanded terrain disappear at the far-east corner while collision remains?
result: live reproduction and native camera replay identify insufficient scene visibility bound; repair is offline only
tags: [re/experiment, terrain/authoring, re/rendering]
---

# EXP-20260906-011 - Expanded corner visibility regression

> **Subsequent repair:** EXP-20260906-012 implements the shared bound, loads a separate candidate and receives user visual confirmation. This note records the preceding diagnosed/uninstalled arm; its game350624 is now closed and retained as control. The actual differing byte is8593 within the two-byte bound word at8592.

## Outcome and scope

**Confirmed:** user-requested normal Up reproduces simultaneous ground/foliage disappearance in unchanged EXP-010. Releasing Up leaves it hidden; normal Down out of the corner restores it. Actor/HUD/background remain. The sampled floor height and contact source remain stable. This is separate from the previously corrected long-segment collision failure and blade-intersection issue.

**Confirmed, original-PC offline discriminator:** captured hidden cameras reject scene160 at horizontal branch `0x0044D677` with loaded bound10087. Changing only that word to the existing PC-aware helper's14183 admits every captured/sample camera. Resident gate bytes match retail; scene/object records stay identical throughout live observations. Entire loaded mesh/floor/barrier/retained mushroom prefix still compare against stage afterward.

**Strongly supported mechanism, not live branch/GPU trace:** expansion's geometric-only bound lets the PC cull the whole terrain incorrectly. Native replay agrees with visible/hidden/visible captures. No installed fix, live radius A/B or universal camera proof is claimed. User requested reproduction, not live memory writes or a replacement preview. Production source/tests/assets are unchanged; only notes/public metadata and ignored diagnostic receipts are new. Start was clean commit `90c8a44`. No originals/PS1 source, debugger, stops, teleport, save states, launch/close or memory/register/code writes.

Public metadata: `reports/terrain/EXP-20260906-011.json`. Private evidence: `work/experiments/EXP-20260906-011/` (`corner-observe.py`, `live-up.json`, `corner-return.py`, `live-return.json`, `corner-native.py`, `native.json`, `final-audit.json`, nine captures). Helpers import guards from the SHA-pinned EXP-010 operator. Hardware/content/executable/socket/window ownership is verified; input keys are released in finally. Captures and memory reads are asynchronous, not atomic. Prior EXP-010 mixed-input evidence remains qualified; this is a fresh user-requested reproduction.

## Live sequence

Up released at4.020s; Down released at1.541s. Camera/state reads bracket each capture.

| Capture | Flik XYZ after capture | Terrain | Native control/candidate |
| --- | --- | --- | --- |
| before | (250386,-102401,719976) | visible | accept / accept |
| held-0 | (276034,-102401,728311) | visible | accept / accept |
| held-1 | (304438,-102401,737544) | hidden | reject / accept |
| held-3 | (332062,-102401,740266) | hidden | reject / accept |
| after | (332340,-102401,740312) | hidden | reject / accept |
| return-after | (239669,-102400,720628) | visible | accept / accept |

Across80 Up samples,44 Down samples and18 capture endpoints, Y remains-102403..-102400, vertical velocity0 and contact source99. Flags include0,1,257: do not claim every call is grounded. Settled hidden/returned-visible poses have flags257. Scene20-byte/object24-byte records each have one unique value across142 observations. This is bounded support evidence, not broad collision acceptance.

Scene160 record address6605371 = DAT base6596791 + file8580; bound at6605383/file8592 remains10087. Mesh72110 bytes at7000763 remains SHA `a8cd38b29de2b9500a45c8f3328c5eccd3967c6150116a0cf96a9de361354be5`. Fresh operator `verify` also compares source99 (6308 bytes at7116801), barrier (head7293909,15 segments) and plant retained prefix (16692 bytes at7297297, SHA `42ae06619418ff0691f3984fcfc0c893444b32d6f792e3b94a52792554ff2257`).

## Static and native evidence

The private native probe reuses the original-PC gate setup from [[EXP-20260906-001 - PC-compatible ramp visibility bounds]] and its EXP-20260905-009 predecessor. Retail executable SHA is the frontmatter hash; actual auto-hardware/spawn executable remains `9d406ac0a1319ba58c9637eb51a45f499c2a0f901c674ce36e5d1d7aebb35ffe`.

- Entry `0x0044D59F`, transform `0x00448230`, accept `0x0044D6A7`, reject continuation `0x0044D728`. Resident bytes `[0x0044D59F,0x0044D729)` equal retail, SHA `e07bfb4095bfe5e3758e2e6dfd3ea22b84615fc4a7793925ff5ae476de8a0219`.
- Live width/height/focal (`0x00861C60 / 0x00861DAC / 0x00511508`) are640/480/320. At settled hidden pose the expanded matrix at `0x0063E888` agrees with9-short camera `0x005B58E0`; stored camera `0x005BDB9C` agrees with world translation `0x005BDB8C` truncated by32: `(9482,-3600,22943)`.
- Settled hidden transformed scene center `(5649,3030,-6594)` fails horizontal comparison: `abs(5649)-10087 = -4438` versus-6594, at `0x0044D677`. Candidate gives-8534 and passes. Control rejects109/124 movement snapshots and12/18 capture endpoints;14183 rejects0/142. Replay0.182s, finite sampled cameras only.
- `scripts/terrain-expand-area.py:71` calls `terrain_foliage.append_scene_mesh`; `reimplementation/ablpc/terrain_foliage.py:183` uses `max(previous, isqrt(distance2)+65)` instead of `scene_visibility_radius`. The additive builder already uses that established helper. EXP-001 explains the PC's unnormalised side planes and insufficiency of geometric sphere alone.
- Existing `patch_scene_visibility` computes geometric radius10023 from3393 vertices, squared radius100457133, retained center `(4243,-570,16018)`. Observed640x480/focal320 profile gives `ceil(R*sqrt(2))+8 = 14183`. In-memory candidate differs only at8592/8593; all geometry/collision/material/allocation/transform bytes remain exact. Candidate bytes were never installed or written to a game file.

## Handoff and next

Same game350624/start2935292, group350348 remains OPEN on`:2`, keys released, terrain visible on return. Final read-only audit accounts all14 unchanged owned identities,7 generic processes and one `ablpc_mute_350348` sink; audit is intentionally not clean. Stage/prefix/controller remain EXP-010 `expanded-game-02` / `expanded-preview-02`. Four pinned assets and loaded bound10087 unchanged. Protected stash `76db1c9ee1ffffce52cea6aee591c24ab6a1c39a` preserved.

**If implementation is requested:** route foliage mesh growth through the PC-aware helper with conservative integer rounding, preservation/overflow tests and this camera regression. Prepare a separate file-loaded candidate with identical geometry/collision/materials and verify corner appearance. Do not reuse old memory-write authorization or overwrite the active stage. EXP-010's780-test/complete-face-stream gate never covered these camera culls; its file/traversal conclusions stand, not broad visibility acceptance. [[2026-09-06 - Codex - Expanded corner visibility diagnosis]].
