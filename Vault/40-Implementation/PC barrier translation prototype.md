---
type: implementation
status: prototype-live-tested-one-fixture
updated: 2026-10-02
tags: [implementation/collision, re/terrain]
---

# PC barrier translation prototype

`reimplementation/ablpc/terrain_barrier_edit.py` adds size-preserving translation
on top of [[PC TERRAIN ALL barrier strips]]. It moves every endpoint X/Z and
full-block X/Z minima, while retaining spans, loose bounds, unknown words,
sentinel tails, closing endpoints, headers, trailers and all other file bytes.

- `translate_payload(raw, dx, dz)` operates in stored units (32 world units).
- `translate_terrain_barrier(raw, index, dx, dz)` replaces only the selected
  kind-0x101 payload in a bounds-checked terrain container.

Inputs require canonical blocks whose bounds contain their points. Noninteger
deltas, invalid kind/index, impossible layout, int32 overflow and overflowing
world-coordinate conversion are rejected. No material assignment, new points,
new records, resizing, floor encoding or movement solver is implemented.

[[EXP-20260904-004 - Translated barrier live collision proof]] validates one
four-segment Level01 translation in the real game, including a restored-file
control and direct loaded-payload verification. Full-block metadata editing
is covered by synthetic tests and all 65 retail strips' reversible translation,
not by live testing of every strip.

`scripts/terrain-barrier-authoring-probe.py` reproduces the fixed authoring
experiment through the unchanged EXP-002/003 original-instruction harness.
Its default output is asset-free JSON. Optional `--write-terrain PATH` creates
only that fixed fixture at a new path under `work/copies/`, without overwriting
or launching. The source and authored file hashes are pinned in the probe.

The measured authored path skirts the relocated barrier while the original
file permits passage through its footprint. The next encoder step is raised
floor/ramp geometry, separately validated offline and live; this prototype
does not establish complete terrain authoring or visible-ground alignment.
That step followed in [[PC floor translation prototype]] (EXP-20260904-005);
complete authored terrain later comes from PC Blender level authoring.
