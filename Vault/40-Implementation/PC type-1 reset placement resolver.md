---
type: implementation
status: m5-module-accepted
created: 2026-08-16
updated: 2026-08-16
tags: [implementation, re/gameplay, milestone/m5]
---

# PC type-1 reset placement resolver

`reimplementation/ablpc/type1_reset.py` is the first module admitted through
the [[Project Roadmap#Module entry gate]]. It answers, offline and without
launching the game: when the engine's reset selector runs, which authored
type-1 coordinate row does it choose, and exactly what position does it write?

Evidence and the complete boundary are in
[[EXP-20260816-153 - M5 entry gate and type-1 reset placement resolver]];
disassembly is in
`static/exports/BIN-97c95ba5572dce63/M5-type1-reset-selector-static-trace.md`.

## Contract

Modelled from `0x00432930` (identical variant `0x00437A20`; both call
`0x00401659`):

| Step | Original | Module |
| --- | --- | --- |
| Which record | `0x005C5864`, written by `0x0044BB70` | last top record claiming the slot; type `-N` aliases to `+N` and is refused |
| Row count | unsigned word at `record + 0` (`0x0043294A`) | same, cross-checked against the parsed signed count |
| Query | `0x0059D960`/`0x0059D968` reduced by `sar 5` | caller-supplied X/Z, same reduction |
| Distance | `((q >> 5) - row) >> 3` squared and summed, 32-bit wrapping | identical, including overflow |
| Tie | strictly smaller wins (`0x0043299A`) | lowest index wins; losers reported |
| Placement | row X/Z `<< 5`, Y = height query − `0x100` | identical, via [[EXP-20260816-141 - Engine-faithful terrain height and gate standoffs]] |
| Failed height | `0x80000000` → `0x7FFFFF00` | identical, flagged |

## Deliberate divergences

- **Zero row count.** The original skips its scan and then indexes the record
  with an uninitialised stack local. The module refuses.
- **Negative-type record in the slot.** The loader stores it, but its element
  layout is not the 12-byte row form. The module refuses.
- **Missing type-1 record.** Seven retail files have none, so the loader never
  writes the slot for them. What the live slot then holds is unresolved
  (`KU-064`): level-load entry `0x004671D0` zeroes all 64 table dwords at
  `0x00467207-0x00467215`, so a retained previous-level pointer cannot be
  assumed. The module refuses either way.

## Use

```bash
# where does a reset from these auxiliary coordinates land?
python scripts/type1-reset.py \
  work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL03/LEVEL.DAT \
  --terrain work/copies/BUGS_PC-full-disc/PC/BUGS/CD/LEVEL03/TERRAIN.ALL \
  --query 494438 526143

# every row's placement, plus rows this selector can never reach
python scripts/type1-reset.py .../LEVEL03/LEVEL.DAT --terrain .../TERRAIN.ALL
```

Both forms are read-only and print deterministic JSON with source hashes. The
reported Y is the value the selector *writes*; an actor then settles deeper.
The reported `settled_y_estimate` uses the observed extremes over the cited
receipts, **121-129** units (EXP-20260815-129/137, EXP-20260816-156) — a range
of five samples, not a guarantee.

## Scope

The confirmed reset role is Level03/Tunnels only. Type 1 has other PC
consumers (`0x004317D0`, `0x004323A8`, `0x004369B0`, `0x00436D25`,
`0x0043CE60`), and four
retail files hold rows that are duplicated out-and-back sequences rather than
distinct places, so the table is still **not** named a respawn or checkpoint
table. Running the tool on another level reports what this selector would do
there, not that the level uses it.

This is not a level editor: it reads level data, never writes it. The
existing exact row edit stays in [[Level03 type-1 row discriminator]].

Related: [[PC TERRAIN ALL inspector]], [[PC grain gate threshold mod]],
[[Python and C reverse-engineering split]] (this module stays Python:
offline, low rate, no measured hot loop).
