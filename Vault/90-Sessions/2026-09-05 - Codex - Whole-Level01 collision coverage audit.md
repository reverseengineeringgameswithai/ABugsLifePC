---
type: session
date: 2026-09-05
agent: Codex
status: complete
created: 2026-09-05
updated: 2026-09-05
tags:
  - session
  - terrain/collision
---

# Whole-Level01 collision coverage audit

## Goal and evidence

Confirm whether the authored fixture changed collision elsewhere, and map collision replacement against render replacement. [[EXP-20260905-008 - Whole-Level01 collision and render coverage audit]] and `reports/terrain/EXP-20260905-008.json` carry the complete scope and evidence references.

## Conclusions

Only source 99 changed among 189 TERRAIN.ALL source records/payloads. Its 134 original active cells were replaced by 14 authored cells; 7,147 other active cell instances are unchanged. An earlier terminator disables 116 original cells whose raw bytes remain intact. All ten barrier payloads and 262 segments are unchanged. Only LEVEL.DAT and TERRAIN.ALL differ among the 16 compared Level01 files.

Only primary render reference 160 changed among 124 decoded static references. Its footprint is not source 99's collision footprint. The original fall endpoint retains mesh 213's rendering but has no authored active floor candidate. Forty-six retired-cell centroid probes have this projected collision/render mismatch; these are samples, not a count of independent holes. Rotated/scaled rendering and the user's exact invisible-ground location remain explicitly unresolved.

## Changes

Added a private offline audit operator, complete offset inventories, an SVG map, public metadata report, experiment/session notes, and durable state/roadmap/MOC updates. No shared parser, authoring code, assets or runtime state changed. Original material and protected stash were not touched.

## Tests and lifecycle

The final offline audit ran in 2.832952 seconds. No pytest, R2q, full repository suite, game controls, memory operations, runtime lifecycle operation, or Git operation was performed. The existing OG game was left untouched. The run-index still reports the known 14 uncited runs and one dangling citation, unrelated to this terrain audit.

## Next action

Plan additive collision/render integration preserving original active terrain rather than substituting unrelated native chunks. Prove any required allocation growth first, then run the earlier fall and cross-boundary routes in the original PC instruction model. Keep the replacing fixture as a control.

## Git commit

None. These findings are recorded in the working-tree Vault and reports, not newly committed or archived into a private checkpoint.
