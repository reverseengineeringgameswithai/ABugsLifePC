---
type: experiment
id: EXP-20260905-009
date: 2026-09-05
status: bounded-offline-accepted-runtime-investigated
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 43 static and native probes with isolated Wine runtime evidence
question: "Can an authored tiled play area and gentle ramp be added while preserving original Level01 terrain and collision?"
result: additive-route-bounded-with-later-isolation-successor
tags:
  - re/experiment
  - terrain/authoring
---

# EXP-20260905-009 - Additive terrain preservation and access ramp

Status: bounded offline crossing acceptance; ready for a controlled runtime comparison, not runtime accepted. Original exact-point controller failures remain preserved. Opened 2026-09-05, continued 2026-09-06.

## Question

Can the working tiled play area be appended while preserving the original Level01 collision and render geometry, with a gentle route back from the original floor? This follows the bounded removal inventory in [[EXP-20260905-008 - Whole-Level01 collision and render coverage audit]], rather than treating its sample points as a count of holes.

## Candidate implementation

`reimplementation/ablpc/terrain_additive.py` appends collision groups before source 99's original terminator, relocating the directory and updating its known payload count. All original groups and their unknown bytes are retained. Sixteen groups are added: the fourteen banked play-area groups and two connector triangles. The connector joins original cell 44140 near stored Z=10900 to the deck at Z=13000, over stored X=5750..6250. This connection is a candidate until native traversal proves it.

The DAT writer appends a combined mesh containing original mesh 160's vertices and complete command groups, the tiled play area, and connector geometry. It preserves the original scene center, mesh origin, vertex suffixes, command bytes and material fields. Known pointer, signed scene-bound and footer fields are updated. The combined batch deliberately uses the banked zero depth bias instead of the original value 8; this is a rendering-state exception, not a claim that every original render byte is unchanged.

Builder: `scripts/terrain-additive-area.py`. Offline proof driver: `scripts/terrain-additive-area-probe.py`. A fresh copy is now staged at `work/copies/EXP-20260905-009/game/PC/BUGS`; fixture assets are under that experiment's `fixture/`. No live process was accessed. The build receipt is `reports/terrain/EXP-20260905-009.json`; the current acceptance report is `reports/terrain/EXP-20260905-009-validation.json`.

## Evidence so far

`reports/terrain/EXP-20260905-009-progress.json` records the first regression run: **37 passed, 2 failed in 0.36 seconds**. `tests/test_terrain_additive.py` includes synthetic parser/writer bounds and preservation cases plus the private Level01/EXP-006 pair. Passing private-fixture cases preserve all 188 other collision records/payloads, all 134 original source-99 cells, original mesh-160 vertices/command bytes and all other supported static references. The in-memory candidate adds 704 TERRAIN bytes and brings source 99 to 150 cells, with its terminator at offset 49084.

Approved corrections applied on 2026-09-06. The mutable-input tests now expect `ValueError`, and the native top-landing setup starts within the one-step helper's range. The later command-audit argument correction, report-hash transcription correction and removal of the redundant overridden hash assignment are also complete. The final affected run passes **39/39 in 0.31 seconds**, and the explicit eleven-file terrain-only gate passes **224/224 in 26.40 seconds**, with four workers and repo-local scratch. Earlier 0.36/26.61-second results and the initial failing draft remain historical evidence, not the current gate result. No asset bytes changed during this controller diagnosis.

## Original-PC instruction results

`work/experiments/EXP-20260905-009/offline-proof.json` preserves the first 11 arms: six accepted, four exact-point route arms not accepted and one probe call error, in 10.938740 seconds. After the approved argument fix, `offline-proof-02.json` records **seven accepted arms, four retained exact-point failures and zero probe errors in 11.340866 seconds**. The original matrix still exits 1; it has not been relabelled green. The separately declared continuous-crossing acceptance below passes. All are offline Unicorn executions, not live game actions or a full actor/input replay.

- Native loader/initializer (`004A8410`, `004A89F8..004A908F`) preserves 7,307 original runtime cell instances across the loaded height-eligible descriptor payloads. This is not a count of unique Level01 triangles. It independently supports the writer's original-byte preservation tests.
- Native DAT relocation (`0044BB70`) passes. Original trailing pointers and the relocated trailer-table hash are unchanged; changed original-prefix bytes are only 8592, 8593, 18690, 18692, 18693 and 18694, within the declared bound/depth/pointer fields. Mesh 160 now has 439 vertices and 623 faces, including its original 92 vertices/69 faces.
- Native command traversal passes after the approved argument correction. The driver now supplies `LevelDat.parse(added_dat)` to the existing helper; its audited streams execute from `0045A8B0` to `00460266`. The original `AttributeError` remains in the first receipt as a probe error, not malformed-asset evidence. This is command traversal, not rendered-image acceptance.
- Box uphill/downhill, top landing and step-off pass in the additive context. The longest airborne run is one sample on each box ramp direction and thirteen on the top-to-deck step-off.
- The same finite fall inputs reproduce the replacing fixture's airborne failure: final position `(222504,-22531,383260)`, flags `[0,0]`, 157 consecutive airborne samples. The additive arm first lands on original cell `99/45884` at zero-based step 51, position `(222240,-87219,388735)`, after 30 airborne samples. It then slides across original cells 45488 and 45008, ending grounded at `(204253,-73640,405181)`. The final positions therefore diverge after contact; this is not a fixed-endpoint or exact keyboard/actor replay.
- All three connector outbound routes contact original cell `99/44140`, but do not reach their prescribed Z=10800 targets. Each subsequent return to the deck succeeds, with at most one airborne sample per direction. The longer route from the restored landing has the same unresolved original-floor target failure, although its subsequent return to the deck also succeeds. Do not count these four complete route arms as passes.

## Contradiction and retail discriminator

The connector reaches original-floor contact and supports return, but its prescribed outward target is not reached. `work/experiments/EXP-20260905-009/connector-retail-control.json` compares unchanged retail and additive terrain on three local lanes, at separately labelled speeds 900 and 1800, from stored Z=10900 toward Z=10800. All twelve runs stop while grounded on cell 44140; paired retail/additive endpoints differ by at most one world unit. Duration: 3.512078 seconds. Initial native landing/contact selection differs between files and is recorded, rather than hidden.

That first control argued against an additive-only defect, but did not isolate a cause. The follow-up `steering-discriminator.json` does separate fixed-forward traversal from adaptive target slowdown on the same original surface: twelve arms, two files, fixed/adaptive directions, and downward requests 512/128/0, in 2.406522 seconds. The altered-gravity arms are diagnostic only.

Original cell `99/44140` has normal words `(-4304,-14070,7206)` and raw-cell SHA `5aba7a6555036a5b97c89f69d53e254d7aba7d84f7093f9955f50e973f3f62de`. At the adaptive 512-downward stall, requested displacement `(156,512,-262)` produces native displacement `(0,1,0)`. The request is almost exactly opposite the cell normal: matching Y=512 predicts horizontal components `512*4304/14070` and `-512*7206/14070`. Both files stop about 305 world units from the exact point, outside the helper's 128-unit tolerance. Reduced-downward adaptive controls reach that tolerance; fixed-forward `(0,512,-900)` crosses the target Z in both files without reducing the downward input.

Inference, bounded to these native samples: horizontal target slowdown combined with fixed downward input approaches a normal-directed request, leaving almost no tangential motion. The existing helper's later sixteen settling steps then slide the still-grounded pose back down the original slope. This explains the local exact-point control failure without declaring a collision hole or modifying the original terrain. It is not a universal mesh/controller rule or a recovered full retail actor loop.

## Separate continuous-crossing and return acceptance

`work/experiments/EXP-20260905-009/through-route-proof.json` records **four accepted routes in 6.072251 seconds**. Criteria were stated before execution: cross world Z<=345600 within X=184000..200000, grounded on a preserved original source-99 cell, with at most two consecutive airborne samples and 220 outward steps. Steering aims beyond that crossing at Z=339200, using unchanged downward request 512 and maximum horizontal step 900. Return uses the existing deck-target helper with its original tolerance/settling. There is no reset between outward and return.

- Stored-X lane 5850 crosses at `(185549,-96143,345348)` on original cell 44140 and returns to deck X/Z `(187200,422400)`.
- Lane 6000 crosses at `(189851,-97473,345317)` and returns to `(192000,422400)`.
- Lane 6150 crosses at `(194334,-98853,345305)` and returns to `(196800,422400)`.
- The reproduced additive fall continues from its original-floor landing, crosses at `(189238,-97342,345210)`, and returns to `(192000,422400)` without a reset during that sequence.

All four crossing contacts are original cell 44140 with flags `[1,1]`; all four final return contacts are appended deck cell 48392 with flags `[1,1]`. Each crossing/return has at most one airborne sample in a run. The initial fall and top step-off have their separately reported longer airborne spans. These are through-crossing results, not exact-point parking: the four old point-target failures remain controls and were not retroactively passed.

## Next runtime boundary

The candidate is ready for a controlled fresh file-loaded runtime comparison, not a claim of general terrain/collision completion. Preserve the original point-target failures and replacing fixture as controls. Runtime must check old/new render visibility, enlarged-batch culling/sorting, zero depth bias, overlap and actual actor/input behavior. Follow the authoritative PC control procedure and session audits; no previous live-memory authorization carries forward. Existing assets and all diagnostic receipts are retained under this experiment's `work/` paths.

No runtime acceptance, full suite, R2q test, Git operation or live-memory operation occurred in this continuation. The original EXP-006 replacement fixture is unchanged. Do not consume the previous EXP-007 teleport authorization again. The already-open game was not inspected, relaunched or changed; its current pose is not asserted. Runtime switching remains gated on the offline results and the authoritative autonomous-control procedure. Existing private snapshots were not rewritten and do not contain this later evidence.

## 2026-09-06 runtime startup: title guard pending

After the offline work above, the user authorized switching to the isolated build. The previous game was already closed and the immediate prelaunch audit was clean. One fresh `preview-01` launch used the established auto-hardware image `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`, not the unchanged retail image retained in the stage. Stage hashes matched the build receipt; the new private prefix maps R: to the EXP-009 stage, with its cdrom registry entry and sentinel checked. Both content-drive log identities and all six hardware markers passed, followed by Start LevelSelect and a one-second settle.

Discovery then stopped: the verified PID's 640x480 window is `Loading - A Bugs Life`, whereas the new title predicate requires `Bugs`. The other same-PID window is the 1x1 `Default IME` window. No active binding, menu input, RAM read/write, screenshot or Level01 confirmation followed. This is a launch-operator/title-policy mismatch, not terrain acceptance or terrain failure. Do not silently relax the guard or replay the launch; obtain approval for a phase-specific correction and continue the existing session.

Current ownership: game `23853/183505`, launcher/group `23606/183305`, Gamescope `23624/183306`, Xwayland `23650/183341`, display `:2`, game window `14680071`. The postlaunch audit reports seven generic-ledger unattributed processes and sink `ablpc_mute_23606` (module `536870916`); all are accounted for by the launch group or exact new-prefix/PID-start guards. The intended live session remains open; the audit is not clean. Evidence: `reports/terrain/EXP-20260905-009-runtime.json` and `work/experiments/EXP-20260905-009/preview-01/`. No R2q/full suite, Git, debugger, signal or memory-write action occurred.

### 2026-09-06 runtime continuation: Level01 loaded, user playtest pending

The user explicitly approved the exact-session title-guard correction. Discovery now accepts `Loading - A Bugs Life` only for game PID 23853/start tick 183505, with the existing ownership, executable, display and 640x480 guards retained. The initial rejection above remains historical; no second launch occurred. Normal Right / Return / Return input selected visually confirmed Anthill, loaded the Level One title, then entered gameplay. Read-only `0x00861C84` returned 1. Full resident source-99/source-100 payloads and mesh command streams 128/160/213/280 matched the staged EXP-009 files. Source 99 is 5,164 bytes; combined mesh 160 is 13,054 bytes in seven groups.

At the original start, the gameplay capture shows original ground and Flik; state was `(197091, 2734, 492897)` with contact `[99, 6990387]`, corresponding to original file cell offset 47716. The helper's `terrain_base` field was zero despite successful descriptor/payload comparisons; this field is not treated as evidence that collision is absent. No agent gameplay movement, teleport, memory write, debugger control, relaunch or close was used. The session remains open for the user. This is load/identity evidence, not live route acceptance.

Evidence: `reports/terrain/EXP-20260905-009-runtime-entry.json`, the retained startup checkpoint in `reports/terrain/EXP-20260905-009-runtime.json`, and private per-action receipts/captures under `work/experiments/EXP-20260905-009/preview-01/`. Capture file names and hashes are in the entry report. Pending: user checks of original ground, connector uphill/downhill/return, deck-edge fall/landing on original ground, box top and step-off, plus runtime visibility/overlap. No tests, R2q/full suite or Git operations were run in this continuation.

### 2026-09-06 user ramp traversal and camera-dependent visibility defect

The user reported that the requested ramp crossings work without falling through or sliding sideways. This is manual runtime testimony, not an instrumented trajectory. The user then identified disappearing ramp terrain when descending or viewing from some angles and clarified that the apparent original-ground standing pose was actually contact on the new ramp.

An agent comparison reproduced the visual change using normal input and read-only RAM. Baseline position `(192615,-97062,358630)` had contact `[99,6991679]`. The same-session source-99 payload base 6986595 maps that contact to file cell `43924 + (6991679 - 6986595) = 49008`, in the appended ramp. A requested 1 ms Down tap produced no observed pose/camera change. An announced 50 ms tap moved Flik to `(192863,-97167,359200)`; three subsequent captures retained exactly that position and contact while the camera rotated. Early views lacked the distinct added ramp; the final view rendered the connector strip and platform. The source of the player's support must not be inferred from the visible old terrain.

Evidence: `reports/terrain/EXP-20260905-009-ramp-visibility.json` records all camera states, capture paths/hashes, input scope and contact mapping. Private captures/receipts remain under `work/experiments/EXP-20260905-009/preview-01/`. Confirmed only: sampled ramp contact persists while visibility changes with camera pose. Reported flashing is not independently resolved by these sparse screenshots. Mesh/bounds culling, triangle-facing/clipping and draw ordering/overlap remain competing explanations. Next discriminator: replay these camera poses against the original-PC render path, distinguish pre-command rejection from face rejection or later occlusion, then use an isolated established-field A/B if warranted. Preserve this failing visual fixture; no speculative collision edits. Session remains open; no writes, teleport, debugger control, tests or Git operations.

### 2026-09-06 cause discriminator: captured poses fail native whole-mesh culling

**PC-confirmed offline:** the original scene gate rejects mesh 160 at horizontal branch `0x0044D677 -> 0x0044D728` for the hidden baseline and early post-tap cameras. The running scene record at 6605371 (`0x0064CA3B`, DAT offset 8580) contains centre `(4243,-570,16018)`, signed radius 6047 at DAT offset 8592, flags `0x41`, object pointer 6615463. The object retains translation `(8192,-8192,8192)`, zero rotation, byte `+0x12=0`, byte `+0x13=192`, and geometry at DAT offset 332820. Projection globals read live: width 640 at `0x00861C60`, height 480 at `0x00861DAC`, focal 320 at `0x00511508`, far setting 1664 at `0x005BA80C`, near setting 1152 at `0x005C02FC`.

The independently authored private probe executes original retail instructions `0x0044D59F` through acceptance at `0x0044D6A7` or rejection at `0x0044D728`, including original transform `0x00448230`, in an offline Unicorn instance. It supplies captured camera matrices, world camera positions truncated toward zero by 32, and the live scene/projection values. Original `0x00463C80` with the settled live Euler triple `(2,3819,0)` reproduces the settled live matrix byte-for-byte. Historical intermediate Euler triples were not captured; these remain captured-matrix replay rather than frame-synchronous live branch traces.

At the baseline, transformed centre `(3541,2863,-2796)` fails `abs(x)-radius < (width/2)*z/focal`: `-2506 < -2796` is false. The early post-tap view also fails (`-2576 < -2792` is false). Radius 8192 passes all five captured/settled gate arms; 6047 passes three and rejects those two. This identifies a concrete whole-mesh visibility rejection before face processing. Merely enclosing vertices in a geometric radius around the inherited centre did not guarantee acceptance at these cameras. The offline radius change is a discriminator, not a general mesh-authoring rule or file repair.

**Contradictory/remaining evidence:** the middle post-tap screenshot does not show a distinct ramp strip, but its captured matrix passes the native scene gate with 6047 (vertical margin only 110). Camera/framing and capture/read timing, face/clipping, or later depth/ordering remain possible for that sample. Do not claim all disappearance/flashing is explained or that 8192 repairs all views. User-reported ramp contact acceptance remains separate.

Evidence: `reports/terrain/EXP-20260905-009-ramp-culling.json`, `reports/terrain/EXP-20260905-009-ramp-visibility.json`; private executable probe `work/experiments/EXP-20260905-009/ramp-culling-probe.py`, native result `ramp-culling-native.json`, and guarded read receipts in `preview-01/`. Static source is retail executable SHA `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`; live image remains auto-hardware SHA `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`. Raw disassembly independently confirms the arithmetic/branch at `0x0044D63A` through `0x0044D6A1`. Ghidra is used only as a bounded query surface.

Next proposed live discriminator, **not performed**: in exact game PID 23853/start 183505, compare-before-write the two radius bytes at `0x0064CA47` (`9f 17`, 6047) to `00 20` (8192), capture the settled failing view, then compare-before-write restore `00 20 -> 9f 17` and capture the control again. Requires fresh approval of that exact two-write use; the user's conditional general write authorization is not treated as that exact approval. No actor, camera, collision, code, file, process-stop or debugger changes proposed. No live writes, asset edits, tests, full/R2q suite, Git operations, launch or close occurred in this investigation. One attempted runtime-helper import hit its CLI argument guard before the requested RAM reads; supported guarded `read` actions then succeeded without modifying the operator.

### 2026-09-06 exact authorized radius A/B/A: live culling contribution confirmed

The user explicitly approved the proposed two-byte radius use. In the same game PID 23853/start 183505, a normal 50 ms Down tap returned to a hidden-ramp view, followed by three seconds and a bounded settle check. The exact live sequence at `0x0064CA47` was `6047 (9f 17) -> 8192 (00 20) -> 6047 (9f 17)`. Both writes were exactly two bytes, checked before and read back after, with durable intent and result receipts. Surrounding scene/object bytes, DAT base, process identity/start/group, cwd, prefix, executable and hardware-path guards passed. No other live writes or input occurred during the three arms.

**PC runtime confirmed, bounded:** in both radius-6047 initial captures the distinct ramp strip below Flik is absent; in both radius-8192 captures that surface is visible; in both restored-6047 captures it is absent again. All six captures and before/after reads have identical actor position `(192607,-97057,358628)`, contact `[99,6991679]` (appended ramp cell 49008), camera matrix `84f10000cc0600000010000034f9000084f1` and translation `(204439,-109864,384878)`. Each PNG had a recorded 200 ms file-size stability interval. All six were visually inspected. Actor/vegetation animation continued; this is not exact full-frame pixel restoration and no calibrated image-difference mask was used.

This reversible radius-only visibility change corroborates the original-instruction mesh-cull result: the scene bound is causally responsible for disappearance at the tested fixed pose, independently of collision. It does **not** establish 8192 as a general solution, resolve the earlier intermediate passing-but-visually-unclear sample, measure flashing, or validate all camera angles. Keep those limitations and the original file fixture. A permanent correction needs PC-compatible bounds or appropriately partitioned/recentred scene meshes, bounded regression cases and a fresh file-loaded runtime comparison; do not make speculative collision changes.

Evidence: `reports/terrain/EXP-20260905-009-ramp-radius-live.json` contains the authorization, two write intents/results, six captures/hashes and all pose guards. Private executable operator: `work/experiments/EXP-20260905-009/ramp-radius-live-ab.py`; private receipts: `work/experiments/EXP-20260905-009/preview-01/radius-ab-01/`. Static companion remains `reports/terrain/EXP-20260905-009-ramp-culling.json`. The actual live executable remains auto-hardware SHA `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.

**Current lifecycle:** original radius 6047 restored and verified; session remains open in the failing view. No collision, actor, camera, code, register or asset writes; no process stops/debugger, launch, close, tests, full/R2q suite or Git operations. The authorized two-write use is complete, not continuing authorization for further writes. The earlier proposal and no-write statements above are historical checkpoints.

### 2026-09-06 file-bound successor

[[EXP-20260906-001 - PC-compatible ramp visibility bounds]] preserves this complete failing control copy and creates a successor with only DAT bound bytes8592/8593 changed, 6047 -> 8560. Native camera-gate sweep removes544 control rejections across5152 relevant cases; affected73 tests and the exact72-test terrain gate pass. Fresh runtime remains pending because this owned session has not exited normally; no second instance or further RAM writes were used. See successor note for lifecycle/permission boundary.
