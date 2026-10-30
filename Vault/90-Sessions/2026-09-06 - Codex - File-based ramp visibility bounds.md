---
type: session
date: 2026-09-06
agent: Codex
status: completed
tags: [session, terrain/rendering]
---

# 2026-09-06 - Codex - File-based ramp visibility bounds

## Work

Created [[EXP-20260906-001 - PC-compatible ramp visibility bounds]] as the isolated file successor to EXP-009. Added `terrain_visibility.py`, integrated its conservative view-plane-aware calculation in `terrain_additive.py`, added34 regression cases in `test_terrain_visibility.py`, and added `terrain-visibility-fixture.py` to preserve the original copy while staging only the bound-word change. Mesh160 radius6047 ->8560, DAT offsets8592/8593 only; collision, geometry and unknown fields unchanged.

## Validation

Affected73 tests passed in.33s. Exact focused72-test terrain gate passed in26.17s using4 loadfile workers and repo-local failed-only scratch. Original-PC native sweep:6624 cases,5152 relevant target-in-viewport cases,544 control mesh rejections and0 candidate rejections;5 historical views pass. Native sweep1.4757455979997758s. No repository-wide/R2q tests, Git or commit. Reports: `reports/terrain/EXP-20260906-001.json`, `reports/terrain/EXP-20260906-001-validation.json`, `reports/terrain/EXP-20260906-001-camera-bounds.json`.

## Lifecycle and next action

Successor has not launched. Old EXP-009 game PID23853/start183505/group23606 remains after normal Alt+F4, pause/exit-level confirmation that returned to pause, and exact-window close. Final audit exit2 lists the same seven explicitly owned processes and private sink. No process signals/stops/debugger or further memory writes. New prefix not created; single-launch plan/operator prepared privately. Obtain scoped old-session termination permission, clean up/audit, then launch the isolated candidate via established auto-hardware/Anthill route and confirm resident bound8560 before live angle testing. Do not call this a live-tested fix yet.

The run/index allocation check had no existing EXP-20260906 IDs; metadata index had114 directories,7 unreadable entries,14 uncited directories and1 dangling citation, recorded without unrelated repair. Initial CLI-help import failed without PYTHONPATH; explicit-path test/stage invocations succeeded. Preserve all private assets/copies/receipts under `work/`.
