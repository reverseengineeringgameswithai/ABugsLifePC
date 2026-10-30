---
type: experiment
id: EXP-20260816-154
date: 2026-08-16
question: 'Does independent fresh-context review support every M5.1 claim - the entry-gate admission, the 0x00432930 contract, the three refusals, the arithmetic, the four runtime-receipt reproductions, the corpus census, and the row-to-gate correspondence - at their stated boundaries?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static audit; radare2 5.9.8; repository Python 3.14.6; pytest 9.1.1
environment_version: radare2 5.9.8
working_directory: /home/dev/ABLPC
configuration: fresh-context adversarial audit at clean HEAD 2ce86861ca6a2ddbbbb084551cff966f098eb661 (subject commit 9044e24, parent dea6cde); read-only toward game media and originals; no game launch, debugger, breakpoint, target write, commit, or staging
artifacts:
  - reimplementation/ablpc/type1_reset.py
  - scripts/type1-reset.py
  - tests/test_type1_reset.py
  - static/exports/BIN-97c95ba5572dce63/M5-type1-reset-selector-static-trace.md
addresses:
  - "0x00432930"
  - "0x0043295C"
  - "0x0043299A"
  - "0x004329B0"
  - "0x004329F1"
  - "0x00436D25"
  - "0x00437A20"
  - "0x0044BC8B"
  - "0x0044BCA9"
  - "0x00464F31"
  - "0x004671D0"
  - "0x00467207"
  - "0x004019EC"
  - "0x004AC6B8"
  - "0x004ACDB2"
file_offsets:
  - "0x031D30"
  - "0x036E20"
  - "0x0D95C8"
result: reject-two-unreproducible-confirmed-numbers-and-one-uncited-retention-claim-behaviour-survives
created: 2026-08-16T17:05:00
updated: 2026-08-16T17:05:00
tags:
  - re/experiment
  - re/static
  - re/audit
  - milestone/m5
---

# EXP-20260816-154 - Independent M5.1 hard-truth audit

## Verdict

**REJECT.** This is the M5.2 packet: an independent fresh-context hard-truth
audit of `EXP-20260816-153` at clean HEAD `2ce8686` (subject commit `9044e24`,
parent `dea6cde`), performed by James.

The module's behaviour survives every attack. The selector contract, the three
refusals, the wrapping/shift/tie arithmetic, all four runtime-receipt
reproductions, the distance correction, and the corpus census reproduce
independently. What fails is evidence discipline in two places:

1. two numeric endpoints in a **Confirmed**-labelled structural claim do not
   reproduce from the cited evidence, and
2. a retention claim repeated in four artifacts is uncited inference stated as
   fact, with contradicting code in the binary that the worker never examined.

Under this project's evidence standard, and consistent with the
`EXP-20260816-145` precedent (`REJECT` over two wrong distance annotations),
these block acceptance. One bounded corrective packet, M5.3, follows.

No game process, Wine, Gamescope, or debugger was used; nothing was committed
or staged during the audit; `originals/` was untouched.

## Checks that passed

- **C1 identity.** Subject exe SHA-256 matches
  `97c95ba5...a27b878`. `9044e24` changes exactly 17 files (4 artifacts, 13
  Vault notes); `2ce8686` adds only the M5.2 packet. No game bytes, assets, or
  `originals/` content in either diff.
- **C2 contract re-derived.** Independent radare2 disassembly at `0x00432930`
  (file `0x031D30`) confirms every instruction-level claim: the `0x10` gate,
  the unsigned count word at `0x0043294A` with `jle` at `0x0043295C` taken only
  on zero, `sar 5`/`sar 3` reductions, wrapping `imul`/`add`, the strict
  `cmp`/`jge` at `0x0043299A`, the `<< 5` placement, the `0x7FFFFFFF` sentinel,
  and `sub eax, 0x100`. Frame analysis (`sub esp,0xC` plus four pushes) confirms
  `[esp+0x18]` is uninitialised scratch on the zero-count path.
- **C3 variant identity.** 185 bytes at file `0x31D30` equal 185 bytes at
  `0x36E20`; both calls resolve to `0x00401659`; the 17-byte tails are
  identical (`83c4042d00010000a364d959005b5d5e5f`).
- **C4 loader claims.** The nonnegative store at `0x0044BCA9`, the negative
  store at `0x0044BC8B-0x0044BC95` aliasing `-N` into slot `+N`, last-record
  overwrite, and all three advance strides confirmed.
- **C5 failure relation.** `0x004ACDB2` stores `0x80000000`, `0x004AC6B8`
  returns the block Y, `0x004329F1` yields `0x7FFFFF00`.
- **C6 arithmetic differential.** James wrote an independent instruction-level
  simulator from his own disassembly and diffed it against the module over
  **264,232 trials with zero mismatches**: edge grids including the ±2^31
  boundaries, `sar` rounding probes, 20,000 random multi-row selections
  comparing index and distance, exact-tie tables, the `0xC000` wrap case, and a
  wrap-flag sweep.
- **C7 mod-4 argument.** Verified analytically and by 200,000 random full-range
  samples: zero distances congruent to 3 modulo 4, zero equal to the seed. The
  uninitialised-index path is reachable only through a zero count.
- **C8 receipts from primary sources.** Recomputed from EXP-20260815-116/117/
  129/130 directly: both pit falls and the takeoff select row 7 with distances
  7,010 / 7,813 and placement `(497248, 31176, 547264)`, descriptor 543; the
  walkable point selects row 6 at distance 0 with exact `(501696, 30092,
  494016)`, descriptor 552; the candidate row moves X by `+4096`. Settled delta
  `+123` inside `[121, 126]`. The descriptor-543 agreement is genuinely
  independent (file geometry versus live sampler), and the row-6 zero delta is
  honestly disclosed as engine-path-originated.
- **C9 distance correction.** EXP-129's `453,992,741` / `1,084,822,693` (and
  fall 2's `504,988,186`) reproduce exactly as world-unit squares; the
  engine-exact values are `7,010` and `16,466`. The worker's correction is
  right.
- **C10 census.** Reproduced from raw bytes with an independent stride walk:
  14 files with a claimant, 7 without, counts 12 to 329, no multi-claimant or
  negative-claimant file, every row scaling without wrap, shadow counts
  `{LEVEL02/LEVEL1: 1, LEVEL04/LEVEL1: 28, LEVEL04/LEVEL4: 28, LEVEL08/LEVEL1:
  233}`, and the Level04 mirror `rows[30+k] == rows[28-k]` for k in 0..27
  including the middle dword.
- **C13 refusals.** Every path routes through `engine_type1_record`; bounds,
  zero count, and row-end checks precede any row read; `select_row` refuses an
  empty table independently; the CLI maps errors to exit 2. Unknown fields are
  preserved; no decompiler pseudocode anywhere.
- **C14 gates.** Focused 24 passed (16 synthetic, 8 retail-gated); full suite
  647 passed; vault-lint 440/0/0; M4 statement valid with 5 anchors;
  tracked-file audit 0 violations; `git diff --check` clean. Zero M4
  authority/pin drift versus `dea6cde`. The report tool is byte-deterministic
  across runs; no test is tautological.
- **C15 naming and history.** No checkpoint/respawn promotion; dossiers stay
  address-named; `DEC-20260816-133` matches the commit; the commit message's
  claims match the diff.

## Defect 1 - two Confirmed numbers do not reproduce

The structural cross-check quoted "far-side row 37,231-**39,619**" and
"next-nearest gate **284,005** units or more" under an explicit
"**Confirmed:** the numeric correspondence above".

Reading the nine Tunnels gate records directly from `.data` at VA
`0x004DA9C8` (file `0x0D95C8`, stride `0x14`, type `0x10C7`) — which match
EXP-20260815-136 and the standoffs constants — the true extremes are:

| Quantity | Recorded | Actual | Where |
| --- | ---: | ---: | --- |
| Far-side maximum | 39,619 | **39,316** | row 11 -> gate 5 |
| Next-nearest gate minimum | 284,005 | **303,653** | row 9 -> gate 2 |

Neither recorded value reproduces under exact Euclid, integer square root,
Chebyshev, Manhattan, `sar`-space, 3D-with-height, or City-inclusive variants;
no row-to-gate, row-to-row, or gate-to-gate pair anywhere is within 400 units
of 284,005. The pairing itself, and the near-side range 13,729-17,993, are
correct.

Root cause, confirmed by the worker: both wrong numbers were lifted from the
*descriptor-anchor* computation — the exploratory pass the worker had
explicitly decided not to rely on because it depends on the disputed
descriptor Z bounds in `KU-061` — rather than from the row computation they
were presented as summarising.

The worker's own passing test asserted a bound of `39,400`, which a
39,619-unit row would have failed: an internal contradiction that should have
caught this before submission.

The wrong numbers had propagated to
[[FUNC-97C95BA5572D-00432930]], [[Current State]], and the M5.2 packet text.

## Defect 2 - uncited retention claim with contradicting code

Four artifacts stated that for a level with no type-1 record "the live slot
would retain whatever the previous level left there" — the experiment note,
the module's error message, the test docstring, and the implementation note.
No evidence was cited for it.

James found live contradicting code: `0x00467207-0x00467215` inside level-load
entry `0x004671D0` is `mov ecx,0x40; xor eax,eax; mov edi,0x5C5860; rep
stosd`, zeroing all 64 pointer-table dwords. A second, apparently unreferenced
copy sits at `0x00464F31-0x00464F3D`. Whether the clear runs on every level
load cannot be settled offline — which is precisely why the retained-pointer
story should have been recorded as Unknown with that discriminator rather than
asserted. The module's *refusal* is correct either way; only its *explanation*
was unsupported.

## Minor findings

1. "18 rows resolve to 18 distinct real terrain surfaces" is imprecise: all 18
   resolve at 18 distinct positions with no failed or ambiguous query, but the
   winning descriptors repeat (558, 517, and 484 each win twice).
2. An additional live reader of slot `0x005C5864` at `0x00436D25` is missing
   from the other-consumers list. The omission is in the conservative
   direction.
3. The implementation note's frontmatter `status: m5-module-accepted`
   overstates while M5.2 is pending; the note body is honest.
4. The `raw_count != record.count` cross-check is unreachable defensive code —
   correctly disclosed by the worker.

## Limitations of this audit

The terrain-height model (EXP-20260816-141/142) was not re-derived, per the
M5.2 evidence boundary, so descriptor indices and Y values inherit its
acceptance. No runtime work was permitted, so whether the `0x004671D0` table
clear executes between level loads is undetermined: the audit shows the
retention claim is unsupported and contradicted by live code, not that it is
false. The `0x0042DDB0` dispatch was not re-derived; byte-identity makes it
immaterial. Not every conceivable metric for the two wrong numbers could be
enumerated (eight variants were tested); the internal test contradiction
stands regardless.

## Corrective packet

M5.3 in [[Project Roadmap]]: correct the two numbers from the gate-centre
computation, bound the missing-record slot claim against the clear routine and
open a known-unknown with a live-readable discriminator, and fold in the four
minor findings — with no change to selector arithmetic, refusal behaviour, or
any currently passing assertion bound.
