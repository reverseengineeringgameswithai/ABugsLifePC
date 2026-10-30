---
type: experiment
id: EXP-20260816-153
date: 2026-08-16
question: 'Does a concrete module meet the M5 selective-reimplementation entry gate, and can the type-1 reset-placement selector be reimplemented engine-exactly and validated against retained PC runtime receipts?'
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static analysis; radare2 5.9.8; repository Python 3.14
environment_version: radare2 5.9.8
working_directory: /home/dev/ABLPC
configuration: read-only disassembly, raw byte reads, and metadata-only asset reads from the exact retail work copy; no runtime process, no debugger, no target write
artifacts:
  - reimplementation/ablpc/type1_reset.py
  - scripts/type1-reset.py
  - tests/test_type1_reset.py
  - static/exports/BIN-97c95ba5572dce63/M5-type1-reset-selector-static-trace.md
addresses:
  - "0x00401659"
  - "0x00432930"
  - "0x0043295C"
  - "0x0043299A"
  - "0x004329B0"
  - "0x004329C6"
  - "0x004329D6"
  - "0x004329E9"
  - "0x004329F1"
  - "0x00437A20"
  - "0x0042DDB0"
  - "0x0044BC8B"
  - "0x0044BCA9"
  - "0x004AC460"
  - "0x004AC6B8"
  - "0x004ACD41"
  - "0x004ACDB2"
file_offsets:
  - "0x031D30"
  - "0x036E20"
  - "0x04B08B"
  - "0x04B0A9"
result: m5-activated-and-first-module-accepted-at-the-level03-reset-boundary
created: 2026-08-16T16:10:00
updated: 2026-08-16T16:10:00
tags:
  - re/experiment
  - re/static
  - re/gameplay
  - milestone/m5
---

# EXP-20260816-153 - M5 entry gate and type-1 reset placement resolver

## Question

[[Project Roadmap]] leaves M5 deferred "until a concrete module meets the
entry gate". Does one exist in the already-accepted evidence, and if so, can
it be implemented as independent code that reproduces the original's observed
behaviour bit-exactly, with its error and edge cases stated rather than
smoothed over?

## Module entry-gate audit

Candidates were ranked against the six gate criteria in
[[Project Roadmap#Module entry gate]]. The selected module is the **type-1
reset-placement selector**: given the auxiliary/reset coordinates the engine
holds when a reset is requested, which authored coordinate row does the game
choose, and exactly what position does it write?

| Gate criterion | Evidence |
| --- | --- |
| Bounded input/output contract | Inputs: one `LEVEL*.DAT` type-1 record and a query X/Z. Output: the exact triple written to `0x0059D960`/`64`/`68`. No hidden state; the caller's `0x10` gate is a precondition, not part of the contract. |
| Cited addresses, offsets, runtime observations | Selector `0x00432930` (file `0x031D30`) and identical variant `0x00437A20` (file `0x036E20`); loader slots at `0x0044BC8B`/`0x0044BCA9`; runtime receipts in EXP-20260815-116, -117, -129, -130. |
| Asset-free fixtures | 16 synthetic cases build minimal parseable DAT prefixes in-test; the 8 retail cases are hash-pinned and skip when the ignored work copy is absent. |
| Known error and edge behaviour | Zero count (original reads an uninitialised index), negative-type slot aliasing, missing type-1 record, truncated rows, 32-bit distance overflow, failed height query — each stated below and covered by a test. |
| Differential test against the original | Four independently accepted runtime receipts across three separate arms, reproduced below. |
| Reason replacement advances modding | Level authors editing type-1 rows currently have to launch the game and die to learn where a reset lands. This answers it offline, and reports rows the selector can never reach. |

Rejected for now: the `.ANM` first-level format (no bounded contract —
`KU-022`), and anything on the M2 dependency path (its causal gate is still
open under `KU-023`).

## Static contract

Full disassembly evidence is in
`static/exports/BIN-97c95ba5572dce63/M5-type1-reset-selector-static-trace.md`.
Confirmed, each with an address and file offset:

1. **Pointer slot.** `0x0044BB70` writes each top record's address into
   `0x005C5860 + type*4` for a nonnegative type (`0x0044BCA9`) and
   `0x005C5860 - type*4` for a negative one (`0x0044BC8B-0x0044BC95`), so
   type `-N` **aliases into slot `+N`**, and a later record of the same slot
   **overwrites** an earlier one. This is new relative to
   [[FUNC-97C95BA5572D-0044BB70]], which recorded only the nonnegative write.
2. **Gate.** `0x00432938` tests bit `0x10` of `0x0059D9A0`.
3. **Count.** `0x0043294A` reads the header word **unsigned**; the parser in
   `reimplementation/ablpc/level_dat.py` reads it signed and refuses a
   negative value, so the divergence is unreachable through this tooling and
   is reported rather than reconciled.
4. **Distance.** The query is reduced with `sar 5` (`0x0043296A`,
   `0x0043296D`), each difference with `sar 3` (`0x00432986`,
   `0x0043298D`) — arithmetic shifts, so negative values round toward
   negative infinity and truncating division would be wrong. Both squares
   and their sum are 32-bit `imul`/`add` and wrap.
5. **Tie-break.** `0x0043299A`'s `cmp`/`jge` keeps only a strictly smaller
   distance, so the **lowest index wins a tie**.
6. **Placement.** Selected row X and Z are stored shifted left by five
   (`0x004329C6`, `0x004329E0`), query Y is set to `0x7FFFFFFF`
   (`0x004329D6`), and the actor Y is the height query's return minus
   `0x100` (`0x004329F1`).
7. **Variant.** `0x00432930` and `0x00437A20` are byte-identical across the
   whole 185-byte selection body and both call `0x00401659`, so the
   `0x0042DDB0` mode/character dispatch cannot change the result.

Two derived facts:

- **The `0x7FFFFFFF` seed is always beaten.** Two squares sum to 0, 1 or 2
  modulo 4, 32-bit truncation preserves that residue, and `0x7FFFFFFF` is 3
  modulo 4. A non-empty row list therefore always selects a row, and the
  original's uninitialised-index path (`0x004329B0` reading `[esp+0x18]`
  after `0x0043295C` skips the loop) is reachable **only** through a zero
  row count.
- **A failed height query is not an error in the original.** `0x004ACDB2`
  stores `0x80000000` in the query block, `0x004AC6B8` returns it, and
  `0x004329F1` turns it into `0x7FFFFF00`. The module reproduces that exact
  value and flags it.

## Implementation

`reimplementation/ablpc/type1_reset.py` implements the contract on top of the
existing `LevelDat` parser and the accepted `TerrainHeightModel`
(EXP-20260816-141/142). Wrapping arithmetic, arithmetic shifts, tie order,
and the failure relation are modelled exactly. Two original behaviours are
deliberately **not** reproduced and refuse instead: a zero row count
(undefined in the original) and a negative-type record winning the slot (the
loader stores it, but its element layout is not the 12-byte row form). No
decompiler text was copied.

`scripts/type1-reset.py` is a read-only reporting tool: `--query X Z`
resolves one reset, the default lists every row's placement, and both emit
deterministic JSON with source hashes. It also reports a settled-Y estimate
band, because the written Y is a surface value and an actor comes to rest
121-126 units deeper (EXP-20260816-141/142).

## Differential validation against retained runtime receipts

| Receipt | Source | Model result | Agreement |
| --- | --- | --- | --- |
| Natural pit fall 1, contact `(494438, 68730, 526143)` | EXP-20260815-129 | selects row 7, writes `(497248, 31176, 547264)` | observed settled sample `(497247, 31299, 547255)`; X/Z within `(-1, -9)` as that note recorded, Y delta `+123` inside the accepted 121-126 settle band |
| Natural pit fall 2, contact `(505717, 66713, 526449)` | EXP-20260815-129 | selects row 7, same placement | same repeated endpoint |
| Fall-1 takeoff `(501522, 31785, 540782)` | EXP-20260815-129 | selects row 7, same placement | the auxiliary triple holds the last grounded position while airborne (EXP-20260815-128), so both plausible query instants agree |
| Walkable point `(501696, 494016)` | EXP-20260815-130, EXP-20260816-141 | selects row 6 at distance 0, writes `(501696, 30092, 494016)` | exact, zero delta — that Y originated from this engine path |
| Row-6 X `15678 -> 15806` | EXP-20260815-116, EXP-20260815-117 | control X `501696`, candidate X `505792`, unchanged Z `494016` | reproduces the observed `+4096` runtime delta from the accepted M3 recipe output |

One agreement was not predicted in advance: the model reports terrain
descriptor **543** at the row-7 placement, and the EXP-20260815-129 trace
sampled collision `543/0` at the first post-reset position. The descriptor
index comes from terrain file bytes and the observation from a live sampler,
so these are independent.

EXP-20260815-129 also quoted squared distances of `453,992,741` (row 7)
versus `1,084,822,693` (row 6) at the first contact. Those are **world-unit**
values; the engine's own arithmetic gives `7,010` and `16,466`. The winner is
the same, and the engine-exact values are now the recorded ones.

## Corpus census

Metadata only, over the 21 retail-derived `LEVEL*.DAT` files:

- 14 files carry a type-1 record (row counts 12 to 329); 7 carry none, so the
  loader never writes the slot for those levels and the module refuses. What
  the live slot then holds is **unknown**: `0x00467207-0x00467215` inside
  level-load entry `0x004671D0` zeroes all 64 table dwords with `rep stosd`,
  so a retained previous-level pointer cannot be assumed. Recorded as
  `KU-064`;
- no file contains two records claiming the slot, and none uses a negative
  type for it, so the "last wins" and alias rules are unexercised by retail
  data and are covered synthetically;
- every retail row scales by 32 without wrapping;
- four files contain rows this selector can never reach because a lower index
  shares their exact X/Z: `LEVEL02/LEVEL1.DAT` (1), `LEVEL04/LEVEL1.DAT` and
  `LEVEL04/LEVEL4.DAT` (28 each), `LEVEL08/LEVEL1.DAT` (233). The Level04
  duplicates mirror exactly around one pivot — rows `30+k` repeat rows `28-k`
  including the unread middle field — which is an out-and-back sequence
  rather than a set of distinct places. That fits the separate index-ordered
  type-1 consumers (`0x004369B0`, `0x004317D0`) and is one more reason not to
  name type 1 a respawn or checkpoint table.

## Structural cross-check (Level03)

All 18 Level03 rows resolve to a real terrain surface at 18 distinct
positions, with no failed and no ambiguous query. The winning descriptors are
not all distinct — 558, 517, and 484 each win for both rows of a pair.
Measured against the nine Tunnels gate centres that EXP-20260815-136/139
extracted from executable immediates — an independent evidence source — rows
`2n` and `2n+1` are the two rows nearest gate `n`, for every gate, with no
exceptions (integer square roots of exact squared distances):

- near-side row 13,729-17,993 units from its gate (minimum row 14, maximum
  row 6);
- far-side row 37,231-39,316 units (minimum row 15, maximum row 11);
- next-nearest gate 303,653 units or more (minimum row 9).

Which member of a pair is the near one is not fixed by index parity: at gate 1
the odd row (3) is nearer than the even row (2).

**Confirmed:** the numeric correspondence above. **Inferred:** that the pair
is an authored near/far reset pair per gate. It is consistent with
EXP-20260815-129 — the pit at gate T3 (the first gate, requirement 10) reset
to row 7, that pair's far-side row — and with EXP-20260815-131 finding
descriptor 572 as the sole result-1 region covering rows 6/7. A similar
anchor comparison for all nine result-1 descriptors also lands one-to-one on
the nine gates, but it depends on the descriptor Z bounds that `KU-061`
records as contradictory, so it is noted and not relied upon.

## Boundary

- The confirmed reset role remains Level03/Tunnels only. Running the resolver
  on another level reports what *this* selector would do there, not that the
  level uses it.
- The live value of the auxiliary triple at the instant of selection was
  never sampled directly; the receipts constrain it to the last grounded
  position, and both candidate instants agree here. Recorded as `KU-062`.
- This module changes no game bytes, ships no assets, and is not a level
  editor. It does not model the upstream events that set bit `0x10`.
- No runtime process, debugger, breakpoint, or target write was used.

## Validation

- 24 focused tests pass (`tests/test_type1_reset.py`); the full suite is
  647 passed.
- `make vault-lint`, `make m4-compatibility`, and `make audit-tracked` pass;
  the M4 authority pins and the v0.2 statement are untouched.

## Result

M5 is Active with its first admitted module. The selector contract is
implemented, differentially validated at four independently accepted runtime
receipts plus one unplanned descriptor agreement, and bounded by an explicit
list of refused and unsupported cases.
