---
type: experiment
id: EXP-20260818-004
date: 2026-08-18
question: 'Is the PC candidate 0x0059D9A7 the equipped berry-type selector, causally upstream of the thrown berry (not a mirror), and what colour does each value 0-4 denote? (KU-073)'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: pristine PC executable under Wine/Gamescope on the Fedora desktop (scripts/play-pristine.sh --research --windowed --mute); live process reads/writes via scripts/game-memory.py (process_vm_readv/writev, identity-verified from /proc); cross-port shape from external read-only SRC-PS1-ABL
environment_version: game-memory 1.1.0; Wine pristine PID 4148084 (exe sha256 verified 97c95ba5...)
working_directory: /home/dev/ABLPC
configuration: Training (level 0x11); four user-authorized compare-before-write pokes to 0x0059D9A7 (values 1,2,4,3), each thrown and visually identified by the user, then reverted to 0
artifacts:
  - dynamic/wine/RUN-POKE-20260818-195515/receipt.json
  - dynamic/wine/RUN-POKE-20260818-195625/receipt.json
  - dynamic/wine/RUN-POKE-20260818-195846/receipt.json
  - dynamic/wine/RUN-POKE-20260818-195932/receipt.json
  - dynamic/wine/RUN-POKE-20260818-200025/receipt.json
addresses:
  - "0x0059D9A7"
  - "0x0059F500"
  - "0x0059D9B1"
file_offsets: []
result: CONFIRMED-PC 0x0059D9A7 is the causal equipped-berry-type selector; value->colour map confirmed (1 blue,2 green/homing,3 gold,4 purple/mega); mirror-vs-source resolved = source
created: 2026-08-18T20:05:00
---

# PC confirmation of the berry-type selector 0x0059D9A7

Closes the runtime half of `KU-073`. The static PC candidate `0x0059D9A7`
(replay-seeded search, [[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]])
was **"Inferred, not confirmed"**: unknown whether it is causally upstream of
throw behaviour or a mirror, and unknown which colour each value denotes. This
experiment confirms it on the PC by direct causal test.

## Cross-port translation (the lead)

The external read-only PS1 source `SRC-PS1-ABL`
(commit `1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`) has the berry mechanic fully
reverse-engineered (`docs/LEVEL01_TYPE3F_MAP.md`, `docs/EXPERIMENT_LOG.md`,
`src_re/berry_throw_80047170.c`). Berries are **special power-up pickups**
(source kinds `0x21`–`0x24`); the equipped-berry marker `0x800A6597`
(player+0x97, global mirror) is read by the throw dispatch `0x80047170` and
bounds-checked 0–4. Two cross-port anchors made `0x0059D9A7` the prime PC
suspect (inference only, per the Cross-Port Evidence Policy):
- **Offset:** PS1 berry `0x800A6597` = grain `0x800A65A1` − `0x0A`; PC berry
  `0x0059D9A7` = grain `0x0059D9B1` − `0x0A` (grain count runtime-confirmed in
  [[EXP-20260818-003 - Runtime reset and grain-gate captures with the flight recorder]]). Same `0x0A` on both ports.
- **Value map:** PS1 kind→marker `0x21→2, 0x22→3, 0x23→1, 0x24→4`; the PC static
  switch has the **identical non-obvious permutation** (`0x23→1`, not sequential).

## Method — PC causal confirmation

Pristine executable under Wine/Gamescope (`play-pristine.sh --research --windowed
--mute`; identity `exe sha256 97c95ba5…`, verified), in Training. Live reads and
**user-authorized** compare-before-write pokes via `game-memory.py` (each guarded
on the current byte, read back, receipted under `dynamic/wine/RUN-POKE-…/`). For
each write the user threw (Left-Ctrl) and identified the on-screen berry.

## Evidence

Baseline `0x0059D9A7 = 0`. Four guarded writes, each **visibly changed the thrown
berry** (user-confirmed):

| write | value | receipt (RUN-POKE-…) | user-observed berry |
| --- | ---: | --- | --- |
| `0→1` | 1 | `195515` | **blueberry / superberry** |
| `1→2` | 2 | `195625` | **green / homing berry** |
| `2→4` | 4 | `195846` | **purple / mega-homing berry** |
| `4→3` | 3 | `195932` | **gold berry** |
| `3→0` | 0 | `200025` | (revert to natural) |

The mirror `0x0059F500` stayed `0` throughout while `0x0059D9A7` drove the throw.

## Result — CONFIRMED (PC-native)

- **`0x0059D9A7` is the equipped berry-type selector, causally upstream of the
  thrown berry.** Writing it changed what Flik throws — so it is the **source,
  not a mirror** (`0x0059F500` is the downstream mirror, unchanged here). This
  resolves KU-073's central uncertainty by independent PC runtime evidence, and
  promotes the cross-port shape to a confirmed PC claim.
- **Value → colour (confirmed at runtime, values 1–4):** `1` = blue/super,
  `2` = green/homing, `3` = gold, `4` = purple/mega-homing. `0` = red/basic is
  the default/baseline (natural value; not separately write-confirmed, but the
  only remaining colour and the reverted state).

## Boundaries

Write-assisted: these are authorized pokes, not natural pickups — they prove the
*selector's* causal role and the value→colour map, not the natural pickup path
(that remains the PC-static switch in `FUN_00417720`/`FUN_004292C0`, corroborated
cross-port). The `==3`/`==4` behaviour gates are consistent with the homing /
mega-homing logic (values 2 and 4 → green/purple homing berries) but were not
separately instrumented here. No repository code changed; all writes reverted.

## Links

- `KU-073` (now confirmed for the selector + causality + the 1–4 map),
  [[XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search]],
  [[EXP-20260818-003 - Runtime reset and grain-gate captures with the flight recorder]]
  (grain-count anchor), [[Cross-Port Evidence Policy]],
  [[EXP-20260817-187 - Runtime berry throw reconnaissance]].
