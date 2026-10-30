---
type: cross-port
id: XPORT-20260818-006
date: 2026-08-18
source_id: SRC-PS1-ABL
source_commit: 1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51
pc_binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
status: confirmed-on-pc
updated: 2026-10-29
tags:
  - research/cross-port
  - re/static
  - re/gameplay
---

# XPORT-20260818-006 - Berry equip byte candidate from replay-seeded static search

> [!success] Confirmed on the PC (2026-08-18)
> The static candidate below (`0x0059D9A7`) was **confirmed causally on the PC**
> by independent runtime evidence — guarded authorized writes changed the thrown
> berry — in [[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]].
> The value→colour map (`1`=blue/super, `2`=green/homing, `3`=gold,
> `4`=purple/mega, `0`=red) and the source-not-mirror conclusion are now
> confirmed PC claims, not inference. The prose below is preserved as it stood
> at the inference stage.

## 1. Bounded question

`KU-073` asks which PC variable selects the thrown berry type; it was
unlocated, and [[XPORT-20260817-005 - Berry contact array and type marker shape]]
had ruled out the record `+0x2C` transfer. Can a deterministic PS1 input-movie
replay, instrumented at the PS1 equip marker, produce a code **shape** precise
enough for a purely static PC search to locate a candidate?

Under [[Cross-Port Evidence Policy]] every PS1 item below is a PS1 fact only.
The PC result is a **static candidate (Inferred)**; nothing here is a confirmed
PC semantic claim, and no unidentified PC symbol is renamed.

## 2. PS1 source and replay provenance

- Source ID `SRC-PS1-ABL`, external and read-only. Committed content cited at
  commit `1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`.
- The replay consumed **working-tree runtime artifacts** of the external
  repository, pinned by hash rather than commit per
  [[External Source Registry]]:
  - Movie `movies/Phase4/Interpreter/Hopper_white_berry_death.movie.json` —
    `DuckStationInputMovie` v4, 642 frames, port 0, state-anchored; canonical
    compact content SHA-256
    `de854c7ffaddcbcdf00094de919a57c5d7932e1dcd4164232cf16ec4c44cc9d4`
    (reported by `movie.loadAndArm` preflight).
  - Anchor state `/home/dev/Downloads/ABL/hopper_throwing_white_berry.sav`,
    SHA-256
    `e7c467bf439e45ac8c2a0277a943a5f702ba437bf3d7aadff37bd77b01ca02e5`,
    hash-verified by the fork before any mutation.
  - Emulator: `SRC-DUCKSTATION-DBG` fork (`external-debugger-control`),
    `build-release/bin/duckstation-qt` SHA-256
    `2ddaad7b1fdbca78110e3a871fd15496923e03be470d2e08e356a006b460dcf4`. This
    differs from the external project's 2026-08-03 capsule pin
    (`f34aaacd…`), consistent with their recorded post-phase-fix rebuild and
    2026-08-05 corpus re-validation; the anchor-hash verification and completed
    replay stand on their own receipts here.
- Procedure (external tooling, isolated instance; no external repository file
  was modified): own config root in the session scratchpad with
  `ExecutionMode=Interpreter` pinned (configured and effective verified via
  `debugger.status`), disc `Disney-Pixar A Bug's Life (v1.0).cue` serial
  `SCUS-94288`; `movie.loadAndArm` with `expected_media`, anchor load, and
  `phase_correction:"schedule"` (boundary
  `paused_with_phase_correction_pending`); `accessLog.addWatch` **after** the
  state load on `0x800A6597` (byte, readwrite) and `0x800B0D18` (256 bytes,
  write); `movie.resumeUntilMovieFrame` to frame 642 at normal speed —
  `execution.completed: true`, 643 frames advanced (the owed one-frame arm
  correction consumed), `speed_control.restored: true`. Instance stopped by
  verified PID; no emulator process or listener remained.

## 3. PS1 observations (PS1 facts only)

- The equip marker byte `0x800A6597` read **0 for every access** across the
  whole replay window (emulator frames 234340-234912) — the operator-labelled
  "white berry" run holds marker value 0. The label "white" comes from the
  movie filename, not from any binding established here.
- Seven PCs read the marker once per game-logic frame (~287 hits each over 572
  emulator frames, consistent with 30 Hz logic under 60 Hz vsync):
  `0x800484F8`, `0x80053880`, `0x80054634`, `0x800B4A48`, `0x800586FC`,
  `0x80058A5C`, `0x80058B04`.
- Two event-time readers fired exactly twice, at emulator frames 234478 and
  234572: `0x8004B4D0` and `0x8004B50C`.
- Live disassembly at `0x8004B4A0`-`0x8004B53C` (the block containing both):
  reads a row index from `*(s1)`, reads the marker, computes
  `row*5 + marker`, and byte-indexes a table at `0x80089938`:
  increment `+2` guarded by `sltiu 200` (cap), then a `sltiu 100` threshold
  branch; the same block compares against `lh 0x800A6594` (their true-health
  global). So on PS1 the marker is consumed at contact time as a **column
  index into a five-column per-(row, type) byte accumulator**.
- The `0x800B0D18` head-of-array write watch recorded a per-frame updater
  (`0x8005A518`-`0x8005A5A0` region) and a sequential-offset initializer
  (`0x8005A188`-`0x8005A1C0+`); not further pursued in this packet.

## 4. PC static investigation (PC evidence)

Search of the Ghidra export (`scripts/ghidra-query.py grep`, binary
`97c95ba5…`) for `* 5` indexing filtered by the constants 2/200/100:

- **Accumulator.** `FUN_0041C9B0` contains, verbatim shape:
  `bVar2 = (&DAT_00599b20)[uVar15 + *piVar4 * 5]` with
  `uVar15 = (uint)DAT_0059d9a7`, `if (bVar2 < 200)` then `= bVar2 + 2`,
  a `99 <` and a `< 100` threshold, and a decay branch
  (`0x40 <` then `-= 2`). Same expression family in `FUN_0041BD10`,
  `FUN_004288F0`, and `FUN_00429790` (which adds a `< 0x78` threshold and its
  own `-2`).
- **Writers.** `FUN_00417720` (the confirmed pickup/consumed-sentinel path of
  `EXP-20260814-111`/`EXP-20260812-016` lineage) and `FUN_004292C0` both write
  `DAT_0059d9a7` inside a switch over selector kinds `0x20`-`0x24`:
  `0x20 -> 0`, `0x21 -> 2`, `0x22 -> 3`, `0x23 -> 1`, `0x24 -> 4`, each case
  calling `thunk_FUN_00414cc0` with a distinct id (`0xfffffffd`, `0x36`,
  `0x38`, `0x35`, `0x37`).
- **Readers.** `== 3` gates in `FUN_004317D0`, `FUN_00431CB0`,
  `FUN_00434E10`, `FUN_00437B70` (also `== 4`), `FUN_00438A80`,
  `FUN_00439E90`, `FUN_0043AE00`, `FUN_0043C340`; and a copy/latch
  `DAT_0059f500 = (uint)DAT_0059d9a7` in `FUN_00437FD0` compared back in
  `FUN_00438040`.

Resulting PC candidates, named per the naming policy (no semantic promotion):

- `candidate_berry_equip_byte` = `0x0059D9A7`, discrete values 0-4.
- `candidate_berry_hit_accumulator` = `0x00599B20`, five-column byte table
  indexed `row*5 + equip_byte`, `+2` per hit, cap 200, thresholds 100 and
  0x78, decay `-2` while above 0x40.
- `0x0059F500` = candidate HUD/latch mirror of the equip byte.

`0x0059D9A7` sits adjacent to the confirmed player globals
(`0x0059D910` position, `0x0059D9A4` neighbour read in the same block,
`0x0059D9B1` grains), as the PS1 marker sits beside their health/lives.

## 5. Directly observed similarities

- Identical accumulator arithmetic on both ports: byte table indexed
  `row*5 + type-byte-global`, `+2` per hit, cap 200, threshold 100.
- Both ports arm one global equip byte from a five-kind pickup vocabulary; on
  PC the switch cases are literally selector kinds `0x20`-`0x24`, the same
  values the PS1 notes name for berry pickups
  (`ObsidianVault/Canon/Systems/SYS_berry_pickup_render_descriptors.md`, cited
  in XPORT-005).
- On both ports the equip byte lives in the player-state global neighbourhood.

## 6. Directly observed differences and cautions

- The PC statics show a decay path (`-2` above 0x40) and a `0x78` threshold
  that the bounded PS1 capture did not exhibit — unobserved on PS1 in this
  packet, not shown absent.
- The PC kind-to-value mapping (`0x20->0, 0x21->2, 0x22->3, 0x23->1,
  0x24->4`) was not compared against the PS1 mapping; no correspondence of
  individual values to colours is claimed on either port.
- Address spaces remain unrelated; the live PS1 value 0 does not bind any PC
  value to "white".

## 7. What remains unknown

Which colour each PC value 0-4 denotes; whether `0x0059D9A7` is causally
upstream of throw behaviour or itself a mirror; the meaning of the `== 3` /
`== 4` behaviour gates; the roles of the sound/event ids `0x35`-`0x38`;
whether the PC accumulator's decay/thresholds match PS1 behaviour.

2026-10-02 audit pointer: later PC-only work explains one `== 3` reader.
`0x004317D0` sets second-telescope suppression `0x00599C69` when the byte is
3 (gold), by static evidence plus flag-level replay, not a live gold pickup
([[FUNC-97C95BA5572D-004317D0]]). The confirmed byte also gates Training
lesson 12 at `0x0043C807`–`0x0043C868` ([[PC Mr Soil lesson triggers]]). The
other gates, sound ids and accumulator behaviour remain unknown.

## 8. Smallest discriminating PC experiment

1. **Read-only (no authorization beyond a live session):** with the user
   naming the equipped colour, sample `0x0059D9A7` (existing read-only
   `process_vm_readv` tooling); predictions from PC statics alone — a stable
   value in {0..4} per colour, transitions on pickups per the switch, and
   `0x0059F500` mirroring a frame later. This is `KU-073`'s labelled A/B and
   would bind values to colours.
2. **Causal (separately authorized):** one compare-before-write byte write to
   `0x0059D9A7` with revert, predicting the `== 3`/`== 4` gated behaviours
   and the accumulator column shift. Requires fresh explicit authorization,
   guard, and receipt per [[Agent Operating Manual]].

## 9. Method note

This is the second structural transfer test after XPORT-005. Running score:
**two hits** (the 64×`0x38` contact array; the equip-byte + five-column
accumulator shape) and **one miss** (`+0x2C` as the type byte). The new
element demonstrated here is the loop itself: a deterministic interpreter
movie replayed with an access watch turned a vague mechanic into exact
arithmetic constants in minutes, and those constants located the PC candidate
statically the same hour. Session record:
[[2026-08-18 1406 - Claude - Replay-seeded berry-type static candidate]].
