---
type: session
date: 2026-09-06
agent: Codex
status: completed-preview-left-open
tags: [session, terrain/collision, terrain/authoring]
---

# 2026-09-06 - Codex - Mushroom collision restoration and varied grass

## Outcome

[[EXP-20260906-007 - Plant-state collision regression]] confirms the observed mushroom is type5 / PLANTTER record8. The unopened type11 seed has a separate actor collider; the mushroom's descriptor and opening transition worked but its triangle template was stripped. A guarded restoration of two bytes at PLANTTER offset9808 restores both solid exclusion and bounce. Original-PC paired probes and a fresh file-loaded live preview agree; the user confirms the mushroom can now be jumped onto. See [[PC seed and mushroom collision state]] and `reports/terrain/EXP-20260906-007.json` for exact evidence, hashes, addresses and limits.

The live copy also loads the banked EXP-006 varied LEVEL.DAT unchanged:202 distinct grass templates /259 placements. Only PLANTTER record8 differs from that original variety fixture. Other templates, high0x104 and removed terrain remain disabled. No general all-plant or aesthetic acceptance is claimed.

## Work and evidence

- Followed startup/charter/manual, terrain MOCs/roadmaps, handoff and EXP-006/007, Ghidra caveats and PC autonomous-control procedure. No PS1 work or subagents.
- Added `reimplementation/ablpc/terrain_plant_templates.py`, `scripts/terrain-plant-probe.py`, and two test files. The writer checks whole-allocation identity/unknowns and patches only selected first markers. The probe executes retail instructions; no copied decompiler implementation.
- Fresh failing control supplied an exact seed/plant/descriptor census, then closed with identity-guarded termination after ignored normal close. Clean post-close/prelaunch audit precedes the repaired launch. Control artifacts remain under `work/experiments/EXP-20260906-007/control-01`.
- `native-03.json` (4.920093888s) passes seed contact/stomp/tenth-tick constructor,15-tick opening/descriptor registration, four lateral approaches, landing/bounce and continuous departure/floor/return. Finite synthetic cadence/flags/input impulse; rendering, input interpreter and audiovisual dispatch excluded.
- Requested Up3s shows exterior contact with tangential sliding. A normal jump supplies262 samples over3.989633473s and five -3328 bounce onsets at descriptor193. Later passive capture returns source99/Vy0. All controls released; no live writes, teleport, stops, registers, debugger or save states.

## Rejected checks and limits

- `native-01.json` rejected: omitted original bounce-history reset falsely entered the combo path. Execute `0x00467D70` and detect the actual PC bounce store. Native02 then passed the smaller gate; native03 adds complete countdown and return.
- One initial synthetic test assertion pointed at untouched high-payload bytes rather than the directory; corrected its malformed-directory target. Final plant tests pass.
- Black startup captures were not used for menu decisions. Verified later nonblack Training screens before input; six hardware markers and content-root bindings passed in both arms.
- Whole-file PLANTTER RAM comparison was overbroad at directory offset16692. All retained payload-prefix bytes matched. Original loader cursor logic supports the corrected prefix check; exact later directory-area writer remains unknown. Both rejected and corrected receipts are retained.
- Live RAM/frame captures are asynchronous, not atomic instruction traces. The broad repaired Z bound is retained as observed. Other plants, all upgrades/states, whole-perimeter proof, projectile equivalence and the inherited synthetic lower-ramp corner limit remain outside this result.

## Validation

- New plant tests:40 passed in5.01s; `work/experiments/EXP-20260906-007/plant-tests.xml`.
- Established focused five-file terrain gate:72 passed in26.76s, four workers/repo-local scratch; `terrain-gate.xml` in that directory.
- No full-suite/R2q run or commit. The prior checkpoint's unrelated unchanged R2p failure was not rerun or repaired.
- Vault lint:0 errors/8 existing maintenance warnings; tracked-file audit:0 violations; staged/unstaged diff whitespace checks clean. Corrected the historical unresolved-type wording and ran claim-sweep pairs for type identity and the experiment MOC status. No active unresolved-type claim remains. Protected stash rechecked unchanged.

## Deliberate live handoff

Leave repaired-variety preview OPEN for the user. At handoff:

- Game231286/start2242744; leader/group231047/start2242595.
- Gamescope231050/start2242596; Xwayland231083/start2242620; display`:2`, window14680071; socket `/run/user/1000/gamescope-0` peer231050/UID1000.
- Stage `work/copies/EXP-20260906-007/repaired-variety-game`; prefix/controller `work/experiments/EXP-20260906-007/repaired-variety-01/` (`prefix` and `control.py`).
- Sink `ablpc_mute_231047`; numeric module IDs are reusable and never sufficient identity.
- `live-handoff-binding.json` in that receipt directory accounts for14 exact-prefix/group processes. Generic audit has7 unattributed processes/1 sink and is **not clean**, but these are the accounted preview; no fixture-ledger runtime acceptance is implied.
- Latest captured floor pose `(189852,-102401,576129)` is historical, not guaranteed once user play continues. Do not issue further input or close this game merely for note cleanup.

## Preservation and next action

Starting HEAD `e5db2ff6f197be6adc05d345e24d70a0a00766fc`, clean worktree. All new changes belong to this session and remain uncommitted at this historical handoff. Protected stash object `76db1c9ee1ffffce52cea6aee591c24ab6a1c39a` is untouched; originals are untouched. Private assets, copied games, binary data and captures remain under `work/`, not Git.

Next is user play and varied-grass appearance feedback. Do not repeat the resolved type5 mapping or restore all PLANTTER templates. Another plant regression requires its own PC type/source mapping and bounded test. This session supersedes the closed/no-live-game instructions in 2026-09-06 - Codex - Terrain foliage and plant collision handoff.
