---
type: session
date: 2026-09-11
agent: Codex
status: investigated
created: 2026-09-11
updated: 2026-09-11
tags: [sessions/codex, modding/training, re/rendering]
---

Subsequent implementation: [[EXP-20260911-013 - Twofold distance and Training performance]] installs the authorized shared2x setting,
verifies the corner/performance live and closes old game86443. The diagnosis-only
runtime and no-setting-change statements below describe EXP012's earlier stage.


# Diagnose missing Training corner

[[EXP-20260911-012 - Training corner render distance diagnosis]] confirms the
reported hole is a polygon draw-distance cutoff. The corner passes scene
admission and its geometry is present. The walls already use the longer group.
At the captured pose, raising the existing1.5x original setting to2x restores
the corner and adjacent clipped faces in50 original-PC admission/draw cases.
This is a recommendation with bounded offline evidence, not a live fix.

The first adapted probe mislabelled the shorter-group scratch as current;
staged/resident0x59 flags and the screenshot contradicted it. The corrected
probe respects existing flags. Both the rejected arm and correction are retained
privately, and the new claim is swept before closure. The final report records
selected make checks, code identity, output hashes and scope.

Existing muted garden game86443/group86212 stays open at the user's view.
There are no agent keys, pauses, relaunches, live writes or settings/build changes.
All audit identities and the private sink remain bound to EXP011; no new workers
or sinks are left. Git/Vault checkpoint contains only the diagnosis and evidence
metadata. Existing source project, accepted bank and originals remain untouched.

Current handoffs, Known Unknowns, Decision Log, implementation/research pointers,
roadmap and indexes record the finding. Next: a2x preview would need full-frame
and live visual/performance checks; global versus Training-only scope is still
undecided. The current session remains available to the user.
