---
type: session
date: 2026-08-16
agent: Claude
status: worker-complete
tags: [session, workflow/play, re/direct3d]
---

# Launcher auto-hardware flag

## Goal

Add an opt-in `--auto-hardware` flag to `scripts/play-pristine.sh` so runs
skip the manual renderer chooser, using the runtime-accepted auto-hardware
transform.

## Worker result

`scripts/play-pristine.sh` gained `--auto-hardware`. When set, it builds (or
reuses, by hash) the patched copy via `scripts/make-auto-hardware` into
`work/copies/auto-hardware/bugs.exe`, verifies its SHA-256
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`, and runs
that exe from the retail game directory. The retail assets and Wine `Y:` are
unchanged (the patch edits only the exe), so no full-disc copy or `Y:`
mutation is needed — verified live: the patched exe reaches hardware Direct3D
from the retail cwd with `Y:` pointing to retail.

Live end-to-end validation through the launcher: `--auto-hardware --windowed
--research --mute` booted straight to the level-select carousel in hardware
640x480 with all six markers and no visible chooser, running
`work/copies/auto-hardware/bugs.exe`, no input sent. A plain launch still uses
the retail exe and the manual procedure. Four dry-run tests cover the wiring
(help text, retail path, patched path + cache hash + retail cwd, cache reuse).

## Mutation and lifecycle boundary

Only the derived patched copy is launched; retail exe and `originals/`
untouched; `Y:` unchanged/retail; owned process groups and the private sink
closed; final audit clean.

## M4 machine-authority re-pin

`scripts/play-pristine.sh` is a pinned M4 compatibility machine authority
(EXP-082/083). Its structure check (`compatibility.py`
`_require_launcher_structure`) enforces the exact, unindented renderer-guidance
echo and the `COMMAND` gamescope surface/scaler, so the pinned echo line was
kept verbatim and the auto-hardware note added as a separate indented block.
The `--auto-hardware` build block and `wine "$EXE_RUN"` change do not touch any
checked structural field. Only the launcher's byte pin in
`reimplementation/ablpc/compatibility.py` was re-pinned
(`68c91717… -> 6ca3c657…`); the M4 v0.2 canonical statement bytes and every
semantic claim (manual renderer selection as the tested default, dims, hash
gate) are unchanged, and `check-m4-compatibility.py` passes. This is the
intended deliberate re-pin, not an M4 scope change.

## Durable changes

- Updated: `scripts/play-pristine.sh` (+`--auto-hardware`, pinned structure
  preserved), `reimplementation/ablpc/compatibility.py` (launcher byte re-pin),
  `tests/test_play_pristine_launcher.py` (new, 4 tests),
  [[Wine Linux Play Baseline]], [[PC automatic Direct3D startup candidate]],
  [[Current State]], this index.

## Next

- Optional independent audit of the launcher wiring (the transform + runtime
  behavior are already James-accepted in EXP-150/151).
