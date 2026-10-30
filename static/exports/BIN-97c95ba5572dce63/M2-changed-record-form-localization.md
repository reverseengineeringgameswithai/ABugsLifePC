# M2 changed-record form localization

## Provenance and scope

- Executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged `PC/BUGS/CD/CHARS/FLICK.ALL`, size `0x34EC`, SHA-256
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`.
- Exact accepted replacement source `PC/BUGS/CD/CHARS3/FLICKD.ALL`, size
  `0x34EC`, SHA-256
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
- Offline inputs: the exact two-file intervals and record walks from
  `EXP-20260813-037`, native PC disassembly, and the already retained
  metadata-only `EXP-20260813-040` control/replacement/control receipts.
- Experiment: `EXP-20260813-041`.

This report localizes only exact changed records in the 13 M2.27 candidates.
It records file offsets, forms, counts, and prior stop metadata. It retains no
file payload values or Direct3D batch payload bytes, creates no general
`.ALL` grammar or parser, and assigns no field, asset, primitive, identity, or
pixel meanings. No runtime was started and no PS1 source was consulted.

## Native call boundary

The exact native control flow distinguishes walking a record, reaching a
builder call, and appending a batch:

- `0x0044F8EE-0x0044F924` selects the masked `0x34` or `0x3C` form.
- A `0x3C` record first indexes a runtime table from its final word at
  `0x0044F92A-0x0044F93F`. A zero table word skips the record. A passing
  record reads renderer selector `0x0059F7F0` at `0x0044F94A`; the retained
  data-watch stop is `0x0044F951`, before the selector-2 call at
  `0x0044F99D -> 0x00405FE0`.
- A `0x34` record reads the renderer selector at `0x00450265`; the retained
  stop is `0x0045026C`, before the selector-2 call at
  `0x0045029F -> 0x00407450`.
- The builders then apply runtime page/root, transformed-coordinate,
  orientation, view-bound, and depth-related gates before changing the batch
  counters. Representative entry gates are `0x00405FE3-0x0040600F` and
  `0x00407450-0x00407460`; the remaining admission logic is inside the same
  two functions before their four-vertex/six-index or three-vertex/
  three-index append blocks.

The pre-call stop register `ESI` remains the current record pointer. The
already retained stop PC therefore identifies the form, and subtracting the
run's exact stream-arena base identifies the file offset without reading or
retaining a payload value.

This distinction corrects M2.27's `B4/B3` “builder call” label. Because exact
pre-call receipts outnumber the corresponding batch additions, `B4/B3` are
completed append-path counts inferred from `(V,I)`, not all function entries.
The original measurements and 13-entry discriminator remain unchanged.

## Offline receipt reconciliation

For each of `RUN-GDB-20260813-113620`, `RUN-GDB-20260813-113842`, and
`RUN-GDB-20260813-113954`, the retained stop sequence contains two complete
ordered entry cycles. Each complete cycle has:

- 126 `0x3C` pre-call stops at `0x0044F951`;
- 42 `0x34` pre-call stops at `0x0045026C`;
- 24 ordered entry-post stops.

The exact offset/form call sets are identical across both cycles and all
three arms. Of the 183 records mapped in `EXP-20260813-037`, 168 reach their
selected builder. The 15 pre-call omissions are all five `0x3C` records in
each of entries 21, 22, and 23. Those entries were already outside M2.27's
13-entry set.

All 145 changed records in exact entries
`{1,2,4,5,6,7,9,10,14,15,18,19,20}` reach their selected builder in every
complete retained cycle. The native pre-call predicates therefore do not
explain any M2.27 count delta inside the 13-entry set. The remaining
difference between a builder call and an append is decided inside
`0x00405FE0/0x00407450` from record inputs plus per-frame runtime state.

## Conservative form discriminator

For each entry and form, the control envelope is the inclusive range between
control A and control B's exact append counts. A form is retained below only
when the replacement count lies outside that envelope. The minimum count gap
is the distance from the replacement count to the nearest edge of the
control envelope. `B4` denotes only `0x00405FE0` appends from `0x3C`; `B3`
denotes only `0x00407450` appends from `0x34`.

Every listed record differs between the two exact files and reaches the
listed builder in all six complete retained cycles. Ranges are inclusive
arithmetic progressions.

| Entry | Form | Exact changed file offsets | Entry-relative offsets | Records | Append counts A/R/B | Minimum gap |
|---:|---:|---|---|---:|---:|---:|
| 1 | `0x34` | `0x0174` | `0x0000` | 1 | `1/0/1` | 1 |
| 2 | `0x3C` | `0x0290..0x0350/0x30` | `0x0048..0x0108/0x30` | 5 | `3/2/3` | 1 |
| 4 | `0x3C` | `0x0550..0x0640/0x30` | `0x006C..0x015C/0x30` | 6 | `3/4/3` | 1 |
| 5 | `0x3C` | `0x06BC..0x077C/0x30` | `0x0048..0x0108/0x30` | 5 | `3/2/3` | 1 |
| 5 | `0x34` | `0x0674..0x0698/0x24` | `0x0000..0x0024/0x24` | 2 | `2/1/2` | 1 |
| 6 | `0x34` | `0x0858` | `0x0000` | 1 | `1/0/1` | 1 |
| 7 | `0x3C` | `0x097C..0x0A6C/0x30` | `0x006C..0x015C/0x30` | 6 | `3/4/3` | 1 |
| 9 | `0x3C` | `0x0AC8..0x0C48/0x30` | `0x0024..0x01A4/0x30` | 9 | `6/5/6` | 1 |
| 9 | `0x34` | `0x0AA4` | `0x0000` | 1 | `0/1/0` | 1 |
| 10 | `0x3C` | `0x0E60..0x17F0/0x30` | `0x0120..0x0AB0/0x30` | 52 | `23/32/24` | 8 |
| 10 | `0x34` | `0x0D40..0x0E3C/0x24` | `0x0000..0x00FC/0x24` | 8 | `2/4/2` | 2 |
| 14 | `0x3C` | `0x1E68..0x1EC8/0x30` | `0x0024..0x0084/0x30` | 3 | `2/1/2` | 1 |
| 15 | `0x3C` | `0x1FB0..0x2040/0x30` | `0x00B4..0x0144/0x30` | 4 | `4/3/4` | 1 |
| 15 | `0x34` | `0x1EFC..0x1F8C/0x24` | `0x0000..0x0090/0x24` | 5 | `1/4/1` | 3 |
| 18 | `0x34` | `0x21C8..0x2234/0x24` | `0x0000..0x006C/0x24` | 4 | `1/2/1` | 1 |
| 19 | `0x3C` | `0x23A0..0x2400/0x30` | `0x0024..0x0084/0x30` | 3 | `2/1/2` | 1 |
| 20 | `0x3C` | `0x24E8..0x2578/0x30` | `0x00B4..0x0144/0x30` | 4 | `4/2/4` | 2 |
| 20 | `0x34` | `0x2434..0x24C4/0x24` | `0x0000..0x0090/0x24` | 5 | `1/3/1` | 2 |

These 18 entry/form groups contain 124 exact changed records. The minimum
count gaps sum to 30 append outcomes. The other 21 changed records inside the
13 entries belong to forms whose replacement total remains inside the two-
control envelope; they are excluded only from explaining the measured count
delta, not from possible batch-content or visible effects.

## Exact record results and irreducible alternatives

Three retained groups contain exactly one call, so aggregate form counts also
identify the exact record outcome in the bounded arms:

- entry 1, file offset `0x0174`, form `0x34`: controls append once;
  replacement appends zero times;
- entry 6, file offset `0x0858`, form `0x34`: controls append once;
  replacement appends zero times;
- entry 9, file offset `0x0AA4`, form `0x34`: controls append zero times;
  replacement appends once.

For the other 121 records in 15 groups, entry-level totals do not identify
which individual calls append. Several distinct per-record outcome sets
satisfy every observed count, especially entry 10's 52 `0x3C` calls. This is
an evidence limitation rather than a native count contradiction: every
observed append count is nonnegative and no larger than its exact call count.
Control variation at entries 10, 14, 18, and 19 independently demonstrates
that per-frame admission state cannot be reconstructed from the two files
alone.

## Bounded result

Confirmed for the exact files, executable, and retained M2.27 arms:

- every changed record in the 13-entry set reaches its selected Direct3D
  builder in both complete cycles of all three arms;
- 18 exact entry/form groups are required by replacement form counts outside
  both-control envelopes; their 124 changed records form the smallest exact
  candidate union supported by current aggregate evidence;
- at least 30 append outcomes separate the replacement totals from the
  nearest control-envelope edges;
- exact record offsets `0x0174`, `0x0858`, and `0x0AA4` have individually
  discriminated append outcomes at this aggregate boundary;
- the remaining 121 record identities are unresolved alternatives, not
  inferred individual-byte or visible-causality claims.

M2.28 is complete at the smallest boundary supported by the retained
metadata. A narrower result requires per-record append/non-append receipts,
not more whole-entry arithmetic.

## Precise next discriminator

M2.29 should first map the exact counter-write and no-append return boundaries
inside `0x00405FE0/0x00407450` and design a fail-closed, metadata-only
per-record state machine keyed by the already proven pre-call record pointer
and form. Any later runtime arm requires fresh explicit authority, fresh
matched Direct3D controls, all four positive hardware markers, absence of
`INITSOFTRENDER`, exact load/`NextLife`, cleanup, signal, and survival gates.
It must retain only record offsets/forms and append booleans or counts—never
file or batch payload bytes—and must not use the quarantined execution points.
