---
type: session
date: 2026-08-15
agent: Codex
status: completed
related:
  - EXP-20260815-129
  - DEC-20260815-121
  - KU-057
created: 2026-08-15
updated: 2026-08-15
tags:
  - session/codex
  - re/runtime
  - re/gameplay
---

# 2026-08-15 1903 - Codex - Natural Level03 pit reset

## Scope

Resume the user-driven Tunnels probe with corrected live X/Y/Z, observe the
first grain gate, black-spider death, and exposed pit using PC-native runtime
state, update the durable Vault, and finish with no runtime or Git residue.

## Runtime and authorization boundary

One exact-retail-derived Direct3D Level03 session ran as
`RUN-KU057-20260815-184629`. The user explicitly requested ten grain via
memory editing. After exact SHA, CWD, PID/process-group, and before-value
checks, one `process_vm_writev` changed only byte `0x0059D9B1` from decimal
`1` to `10`; readback was 10. No other target write, executable or asset edit,
debugger attach, breakpoint, or pause occurred. The grain-gate access is
therefore not a pristine-state/no-write arm, while the later spider and pit
events remained ordinary user input.

## Result

[[EXP-20260815-129 - Natural Level03 pit material-1 and row-7 reset]] captures
two falls into the same single pit revealed by the first grain gate. Both
transitions read current descriptor/value `572/1`, flags `0x0014`, and
`NextLife=2`, then repeated first sampled post-reset position
`(497247,31299,547255)`. Authored Level03 row 7 is scaled X/Z
`(497248,547264)` and was nearer than row 6 at both contact samples. The 50 ms
sampler missed the exact coordinate-write instant, so the `(-1,-9)` residual
is retained.

The user visually confirmed that the black spider delivered the fatal hit in
the control event. That path used descriptor/value `543/0`, flags `0x0006`,
counter `-1`, and a post-reset X/Z not matching any authored type-1 row. The
game log independently recorded `Level done variable is 2.` and `NextLife.`
This rejects the prior descriptor-571/black-spider material-1 hypothesis.

Static PC evidence at `0x004ACF90`, `0x004408EA`, `0x0041C8CC`, and
`0x00432930` independently joins descriptor value 1 to flags `0x14` and the
nearest type-1 row consumer. KU-057 is narrowed to natural material-1 contact
inside row 6's nearest-region or an explicit milestone disposition. Repeating
the same pit is not useful because both tested approaches funnel to row 7.

## Evidence

- `dynamic/wine/RUN-KU057-20260815-184629/metadata.json`
- `dynamic/wine/RUN-KU057-20260815-184629/selected-events.tsv`
- `dynamic/wine/RUN-KU057-20260815-184629/runtime-log-markers.txt`
- exact executable SHA-256
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Level03 type-1 table at file offset `0x458`; row 6 at `0x4A4`; row 7 at
  `0x4B0`

## Validation and lifecycle

- complete `make check`: Vault 370 notes, 0 errors, 0 warnings; 567 tests
  passed; five M4 hash anchors valid; tracked-file audit 0 violations;
- `git diff --check`: passed;
- observer, coordinate overlay, game, Wine/Gamescope group, companion, and
  private sink were closed; targeted process and sink audits were empty;
- Wine `Y:` was restored to
  `/home/dev/ABLPC/work/copies/BUGS_PC-full-disc`;
- `originals/` was not modified.

## Boundary retained

This session does not prove that every descriptor value 1 is a pit, that every
type-1 consumer is a respawn/checkpoint path, that retained descriptor tuples
are geometry centers, or that row 6 is naturally selected. The one-byte grain
write is disclosed and is not evidence of unchanged-state gate access.
