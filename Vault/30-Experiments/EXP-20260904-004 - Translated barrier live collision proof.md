---
type: experiment
id: EXP-20260904-004
date: 2026-09-04
question: Does moving an existing PC barrier move its collision response into a naturally reachable walking path?
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora; Wine 11.0 Staging; Gamescope hardware Direct3D; original-instruction Unicorn reference
status: completed-runtime-not-independently-audited
result: translated-barrier-loaded-and-deflects-live-walking
---

# EXP-20260904-004 - Translated barrier live collision proof

## Result and scope

**PC confirmed, one authored fixture:** relocating Level01 source record 179
changes where the live game deflects Flik. The modified arm skirts the relocated
barrier; a fresh original-file control walks through that same footprint.
Both measured walks start at `(197091,2734,492897)` and hold Up for one host
second. The original collector/movement instructions independently demonstrate
response at the new location, removal at the old location, and unchanged
unrelated-floor movement.

This establishes a size-preserving barrier translation. It does not establish
raised floors, ramps, inserted geometry, a complete collision writer, visible
terrain/collision alignment, or universal static/render independence. Runtime
uses the accepted auto-hardware derived executable, not the retail executable
as a live control. No independent audit is claimed.

The user later manually tested a fresh play copy and reported “Confirmed
myself.” See [[2026-09-04 1909 - Codex - User barrier play session]]. This adds
user acceptance of the barrier effect; the retained measurement report is
unchanged and no independent code/evidence audit is implied.

## Prior work and authorization

Reused [[EXP-20260904-002 - Retail collision admission and separate XZ barriers]]
and [[EXP-20260904-003 - Barrier grammar and landing-seeded grounded movement]]
without changing their parsers, loader, probes or reports. No R2q successor or
historical wrapper was invoked; no PS1 research was consulted.

The user requested the moved-barrier step with actual runtime testing, asking
for any runtime blocker to be reported. That authorized this fresh experiment.
An isolated copy of `work/wine/baseline` was created under
`work/experiments/EXP-20260904-004/prefix`. Only that copy's drive mappings were
changed. Content arms are under `work/copies/EXP-20260904-004/`.

No live memory writes, teleport, save state, breakpoint or debugger attachment
occurred. Normal XTEST input and read-only `/proc/<game-pid>/mem` sampling
followed [[PC autonomous game control]]. Fixture-only session-control tools
were not used as runtime evidence; their CAP-010 status is unchanged.

## Authored bytes and offline prediction

Source `CD/LEVEL01/TERRAIN.ALL` SHA-256:
`62f3b73f21630eb19c04e585a92e1f3e32a76fdcb6ec36bae18f9c1ec3a2a868`.
Source record 179 is kind `0x101`, payload offset **219632**, size **68**,
with four segments/five points, an explicit closing point and a sentinel tail.

Translation is **(+2200,+19968)** stored X/Z units, or
**(+70400,+638976)** world units. Only the ten endpoint X/Z dwords are eligible
to change; exactly 25 byte values differ in the whole file. Count, middle
words, sentinel, directory, all other payloads and file length are unchanged.
The authored file SHA-256 is
`7329b620ba5038be2ba3d94e1d08be68935e06c51ef03b5defb45737efeda0ac`.

The footprint spans X `176928..185024`, Z `502144..508640`, a reachable path
from the observed spawn. A hand-packed fixed fixture was designed and run
through the existing original loader before launching the edited content.
The later reusable translator reproduces that exact live-tested file hash.

`scripts/terrain-barrier-authoring-probe.py` seeds a position 1024 units above
the measured spawn Y, then lets original landing instructions establish
contact. Both files land at `(196955,2755,492920)`, descriptor 99/cell 47716.
Thirty-five requested `(-900,0,700)` steps have matching state/response through
step 12. The moved fixture records segment responses on steps 13–21; the
retail control has none. Collector execution traces can differ earlier as
nearby candidates enter the query window; identical motion is not a claim of
identical instructions. The old-site grounded fixture loses its segment hit
after translation, and the unrelated flat-floor fixture remains exact.

## Runtime evidence

Live executable SHA-256:
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
It was built/launched through `play-pristine.sh --auto-hardware --research
--windowed --mute` with the isolated prefix and per-arm game directory.
All three arms have the six hardware markers and the intended `R:\PC\BUGS`
content-load log identity.

| Arm | Game PID / start ticks | Launcher group | Observation |
| --- | --- | --- | --- |
| Initial control | 26296 / 651404 | 26044 | Runtime capability, spawn, one short walk; no continuous trace |
| Moved barrier | 27067 / 664602 | 26823 | Edited payload verified live; 50 walking samples |
| Restored control | 27611 / 670967 | 27367 | Original payload verified live; 50 walking samples |

Guarded actions check game PID/start/group, exact working directory, window
ownership/focus, and 32 mapped movement-code bytes at `004ab1a0` against the
hash-verified derived PE. Inputs use owned display `:2`, window 14680071.
Game level is read at `00861c84`, position at `0059d910`. Walking starts only
in Level01 gameplay after the title screen and original spawn are observed.

The barrier list at `007f3d3c` is followed through ten nodes. The source179
node at **7149251** matches the staged 64 bytes after the loader's link word
exactly in both measured arms. Post-link SHA-256 is
`6b970a5555cb47771094284fac93432ac7a3e0961b56d14e287e09bccd82a456`
for moved, and
`355daf2780eb38bf93dba46676f999f77956ae635241d8ce4fc4744a51ec65d1`
for restored. This is direct loaded-data evidence, not an inference from a
stage directory existing.

| Spatial observation during held Up | Moved | Restored original |
| --- | --- | --- |
| First position | `(197091,2734,492897)` | Same |
| Samples strictly inside relocated footprint | 0 / 50 | 8 / 50 |
| Near Z 504500–504900 | `(187222,2447,504522)` | `(181940,1820,504809)` |
| Final held-input sample | `(185110,2209,508357)` | `(169081,-2435,514994)` |

The trajectory comparison uses spatial passage and deflection, not exact
host-time endpoint equality. Host samples are approximately 20 ms apart,
not frame-aligned; duplicate positions are retained. There is no live trace
of contact flags or response return sites. These runs do not measure an exact
universal live contact radius.

Comparison of **2,251 files**, excluding `bugs.log`, finds only
`PC/BUGS/CD/LEVEL01/TERRAIN.ALL` differs between the moved/restored arms.
The path plot is `reports/terrain/EXP-20260904-004-live-paths.png` (also SVG).
It shows the original path crossing the authored footprint and the edited
path deflecting around its edge.

## Operational limitations retained

The direct operator was developed interactively, not run as a frozen executor.
Initial discovery attempted to inspect Gamescope's protected maps; filtering
to the actual game process fixed that. First screenshot validation lacked
Pillow in the venv; validation switched to the installed system Python.
The moved arm's first Right was sent before carousel readiness and dropped;
a screenshot showed training, then a second Right reached Anthill before any
level selection. These events are retained, not silently discarded.

The raw operator field `terrain_base` samples preload global `007f3d60`, zero
in these runs; it is not a resident-buffer locator. Loaded-data proof uses the
barrier list instead. The raw field `settled` is just the sample 300 ms after
key release, not proof of rest. Control motion continued after that sample.

Cleanup first requested normal Alt+F4, then used identity-guarded termination
only for owned game-stack processes. The initial control left one Wine device
helper outside the launcher group; its exact isolated-prefix ownership was
verified before receipted TERM/KILL. Later cleanup included prefix-owned
helpers. Every arm ended with a clean session audit. No null sink or game
process remains, and historical baseline R:/Y: mappings were preserved.

## Artifacts and validation

- Main report: `reports/terrain/EXP-20260904-004.json`, 275,740 bytes,
  SHA-256 `242651dd93e7429565ec3851a840790a27d5100c2ab5033bd245d00842ac0200`.
  Includes original-instruction measurements, interpreted runtime receipts,
  raw receipt paths/hashes, game-log identities, asset comparison and final
  clean audit. No raw memory dumps or game assets are published.
- Final interactive operator snapshot:
  `reports/terrain/EXP-20260904-004-runtime-operator.txt`, SHA-256
  `ba6c46f0cc7e9a5d71b3f2945e71b2fd966d39801313f13a800b77f787e02e57`.
  This final snapshot is not claimed to be the exact source of all earlier
  receipts. The initial design is retained alongside it as `-runtime-design.txt`.
- Raw logs, captures, helpers and their receipts remain under the experiment's
  `work/` directories. The main report embeds the substantive measurements.
- Translator: `reimplementation/ablpc/terrain_barrier_edit.py`, SHA-256
  `be0e27927add652f58079258b88a80901b524bbdbbb1ddae1a5f5bb941fbf08e`.
- Offline probe: `scripts/terrain-barrier-authoring-probe.py`, SHA-256
  `9b9b00898fbf89036a3e0da73c3e2b14afeb8c431e9bd6ab0499e041e0f72e70`.
- **174 focused tests pass in 6.98 s**, including 20 new tests. Synthetic
  full-block/tail/unknown-byte/overflow tests and translation/reversal of all
  65 retail strips cover the translator. Only the four-segment fixture has
  live acceptance. An initial test wrongly required identical collector traces
  before impact; it now compares motion/contact/response instead.
- The offline report reproduced exactly as JSON values. EXP-002/003 source and
  report hashes remain pinned. The full repository suite and independent
  audit were not run; no commit is claimed.
- The CLI recreated the live-tested terrain file byte-for-byte at a new work
  path. A second write was rejected with `FileExistsError`, leaving it unchanged.

Reproduce offline measurements with:

```bash
.venv/bin/python scripts/terrain-barrier-authoring-probe.py
.venv/bin/python -m pytest -q tests/test_terrain_barrier_edit.py
```

`--write-terrain` can emit this exact fixture to a new path under
`work/copies/`; it refuses overwriting files and paths outside that subtree.
It does not launch or stage a live session. Do not rerun historical runtime
arms; a future comparison uses fresh directories and process ownership.

## Next boundary

Bank this first live authored-barrier result. Next is a bounded raised-floor
or gentle-ramp fixture: consistent plane/cell/bounds edits, original landing
and walking predictions, then the same direct live read/input method.
Preserve the different reset-height and movement-contact conventions.
Full mesh writing, visible-ground matching (KU-079) and deeper render coupling
(KU-081) remain separate open work. See DEC-229 / [[Project Roadmap]].
