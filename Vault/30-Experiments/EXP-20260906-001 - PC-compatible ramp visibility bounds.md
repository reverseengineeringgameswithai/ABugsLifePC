---
type: experiment
id: EXP-20260906-001
date: 2026-09-06
status: offline-accepted-runtime-preview-closed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 43 file analysis, native PC instruction probes, and Wine runtime comparison
question: "Can a file-only scene-bound correction prevent camera-dependent rejection of the authored ramp?"
result: conservative-scene-radius-correction-user-accepted
updated: 2026-10-02
---

# PC-compatible ramp visibility bounds

## Question and evidence basis

Can a file-only scene-bound correction prevent the camera-dependent mesh rejection established in [[EXP-20260905-009 - Additive terrain preservation and access ramp]], without changing collision, geometry, unknown fields or the original control copy?

EXP-009 original-instruction replay identifies the horizontal rejection at `0x0044D677`, and its exactly authorized radius-only live 6047 -> 8192 -> 6047 comparison reversibly exposes/removes the ramp at fixed actor/camera/contact. Evidence: `reports/terrain/EXP-20260905-009-ramp-culling.json` and `reports/terrain/EXP-20260905-009-ramp-radius-live.json`. That permission was completed; no further live writes are inferred or used here.

## File correction

`reimplementation/ablpc/terrain_visibility.py` calculates a conservative bound for the PC's unnormalised view-plane comparisons:

`ceil(R * sqrt(1 + (max(width//2,height//2)/focal)**2)) + 8`

Here R is the ceiling geometric enclosing radius, profile is 640x480/focal320, and the eight stored-unit allowance is an explicit bounded rounding/strict-comparison allowance, not an all-angle quantisation theorem. The previous bound is never reduced; signed-short overflow is rejected, not clipped. The writer preserves the scene centre, object transform, geometry, unknown fields and every DAT byte outside the bound word. Nonzero rotation or unestablished matrix selection is rejected. `terrain_additive.py` now uses this calculation for future additive builds rather than a geometric sphere alone.

Source mesh 160 has 439 vertices, squared geometric radius 36557262, geometric radius 6047 and retained centre `(4243,-570,16018)`. The new bound is **8560**, not the experimental 8192. Only DAT offsets **8592 and 8593**, scene-record8580 +12, change. Scene/object/geometry offsets remain 8580/18672/332820. Collision and geometry are unchanged.

The isolated copy is `work/copies/EXP-20260906-001/game`; fixture and build receipt are in its sibling `fixture/`. Source EXP-009 remains untouched. `scripts/terrain-visibility-fixture.py` pins the source hashes, refuses an existing output directory and stages under `work/copies` only.

- TERRAIN.ALL, unchanged: `77a77456c3b9a0f4db5e7b20d257a9772e04c0f0ed3d0812590943d630851698`.
- Control LEVEL.DAT: `24b8c345d82bb3489ab765d3ad24f917fcacf1da4d5a910e715b4daf84b071e8`.
- Candidate LEVEL.DAT: `691674fdca9b87a95f477bfb144f9ff6d805fecc05785669c68162c8f4f17659`.

## Offline results

Affected tests (`test_terrain_additive.py`, `test_terrain_visibility.py`): **73 passed in 0.33 s**, including 34 new radius/writer cases. Synthetic writer tests isolate the byte writer with a stub reference; existing parser regressions and the private EXP-009 integration arm cover real parsing. Cases include byte preservation, idempotence, expected-value guards, truncation, impossible offsets/counts, unsupported transforms and overflow.

The exact five-file terrain gate: **72 passed in 26.17 s**, four loadfile workers, repo-local scratch and failed-only retention. No full `make check`, R2q tests or Git operations.

Original-PC offline camera sweep: **6624** cases across 32 yaw angles, three pitches, three distances and all 23 connector vertices. **5152** have their targeted vertex inside the viewport; the remaining1472 are explicitly excluded rather than counted as passes. The control bound wrongly rejects the mesh in **544** relevant cases; the candidate rejects **0/5152**. All five previously recorded camera poses pass with 8560. Duration **1.4757455979997758 s**. Original addresses include `0x00463C80`, `0x00448230`, `0x0044D59F`, `0x0044D6A7`, `0x0044D728`. This executes the native culling gate, not face rasterization, depth ordering or a universal visibility theorem.

Evidence: `reports/terrain/EXP-20260906-001.json`, `reports/terrain/EXP-20260906-001-validation.json`, `reports/terrain/EXP-20260906-001-camera-bounds.json`; private native probe and receipt under `work/experiments/EXP-20260906-001/`.

## Runtime boundary and next step

**No successor launch yet.** The old EXP-009 PID23853/start183505 remains alive after normal Alt+F4, a pause/exit-level confirmation sequence that returned to pause, and an exact-window close request. Final `make session-audit` exits2 and reports the same seven explicitly owned, generic-ledger-unattributed processes plus private sink `ablpc_mute_23606`/module536870916. No signals, debugger control or extra RAM writes were used. The new prefix has not been created. Request scoped termination permission before replacing this session; do not start a second instance.

The preregistered single-launch plan is `work/experiments/EXP-20260906-001/preview-01/launch-plan.json`: isolated prefix, established auto-hardware executable, all six hardware/content-drive gates, visual Anthill confirmation, final Return, RAM level1 and resident data/bound verification. A generated private operator retains owned-PID/group/geometry/socket guards and accepts the two already observed window titles for the newly owned instance.

After clean closure/audit, launch the file-loaded candidate and test uphill/downhill views, short turns and side angles at the ramp. Keep the earlier intermediate-view discrepancy and flashing open until live comparison addresses them. No collision rewrite is warranted.

## Allocation and orientation

No EXP-20260906 entries were present in notes/reports/private experiment roots before allocation. Run-index metadata was recorded before the new note:114 run directories,7 unreadable metadata entries,14 uncited run directories and1 dangling citation. These pre-existing index conditions were not repaired or attributed to terrain. The first CLI help invocation lacked PYTHONPATH and failed before staging; subsequent tool/test commands used the explicit reimplementation path successfully.

## 2026-09-06 runtime continuation: corrected file loaded, angle playtest pending

The user approved the scoped old-session termination/cleanup. The first SIGTERM cleanup pass stopped on a Wine-helper environment-read PermissionError during shutdown; the game and old sink were already gone. Continuation targeted only pinned remaining identities, with SIGTERM/guarded SIGKILL fallback receipts in `reports/terrain/EXP-20260906-001-cleanup.json`. Both the completed post-cleanup and immediate prelaunch audits were clean. No second instance was launched while the old one remained.

One fresh isolated launch succeeded via the established auto-hardware path. All six hardware and both R-drive content markers passed in6.804338723999535s, then LevelSelect settled1s. Normal Right/Return/Return, with visually confirmed Anthill and Level One screens, entered gameplay. Read-only level global `0x00861C84=1`; DAT base6596791; scene6605371 has bound bytes`70 21` at `0x0064CA47`, **8560 loaded from the file**, not a RAM patch. Complete resident source99/source100 payloads and mesh streams128/160/213/280 match the corrected staged pair; geometry and collision are unchanged.

Actual live image is auto-hardware SHA `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`. Session: leader32301/start646307/group32301; game32550/start646434; Gamescope32319/start646308; Xwayland32345/start646331 on`:2`; window14680071; owned socket`gamescope-0`; prefix `work/experiments/EXP-20260906-001/preview-01/prefix`. Postlaunch audit exit2 is the intentional live direct-procedure session: seven generic-ledger-unattributed processes independently accounted for by launch-group or exact-prefix/start/UID checks. Helpers32472/start646342,32481/start646349,32506/start646353 are pinned. Private sink`ablpc_mute_32301`, module536870916. That module number was reused: never apply old cleanup by numeric sink ID alone.

Handoff is **at the original start, not the ramp**: position`(197091,2734,492897)`, contact`[99,6990387]`. Agent used menu input only; no new RAM writes, teleport, debugger/execution stops or gameplay movement. Game remains open for the user to return to the ramp and repeat downhill/turn/side-angle views. This establishes fresh-load identity, **not** completion of live camera-angle acceptance or closure of the earlier intermediate-view/flashing questions. Startup captures were visually inspected, without a separate200ms size-stability receipt. No tests/full/R2q suite or Git were rerun during launch.

Evidence: `reports/terrain/EXP-20260906-001-runtime.json`; private launch/cleanup/audit/ownership/action receipts and captures in `work/experiments/EXP-20260906-001/preview-01/`. The previous runtime-pending/cleanup-approval section above is historical; the original checkpoint is also retained in the validation report. Audit after eventual close remains required.

## 2026-09-06 user feedback and decorative successor

The user reports "I think this works now" and requests side faces down to the
ground, not guardrails. Record this as positive manual feedback, not a new
instrumented all-angle or flashing-frequency verdict. EXP-001 remains the
working control and its live session is untouched during the offline build of
EXP-20260906-002. The successor preserves all
collision/top geometry and bound8560; its new side appearance is unlaunched.

EXP-002 preview-switch update: the user requested replacing this preview.
EXP-001 group32301/game32550 is now closed with a clean post-close audit;
2026-09-06 - Codex - Ramp-side preview and missing blocking records the
single fresh successor. EXP-001 fixture assets remain the working control.
