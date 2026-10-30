# M2 second-deferral hard-truth audit

## Scope

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Audit target: the post-M2.40 conclusion that no finite PC-native M2
  successor remained and M2 should return to `Deferred`.
- Evidence reviewed: `EXP-20260813-049` through `EXP-20260813-056`, their
  cited static reports, the exact work-copy executable, the eight-reader
  census, the first hard-truth audit, and the M2.40 producer census.
- Native verification: GNU objdump 2.46-3.fc44 and exact address arithmetic.

This was read-only and offline. It did not launch or mutate the game, inspect
another resource family, add parser/schema surface, assign field semantics,
perform a whole-program indirect search, or consult PS1 evidence.

## Premise matrix

| Premise | Adversarial check | Verdict |
|---|---|---|
| M2's causal exit gate and `KU-023` remain unsupported. | M2.40 proves a conditional ID-zero selection for slots 2/3, but its value and predicate lineage is separate `LEVEL.RAW` plus fixed-pool state, not M1. | Survives. M2 is not complete. |
| M2.40 completely retires its declared slots 2/3 candidate. | The exact writer set, reader ordering, and source-lineage evidence answer the M2.40 question at `0x0059B730/0x0059B7B4`. | Survives at the declared boundary. |
| No finite PC-native successor remains. | The first audit explicitly retained `0x0059D6A4` as lower-ranked. M2.40's stop rule explicitly excluded it and `0x0059C30C`. Exact arithmetic supplies the omitted pool classification for `0x0059C30C`: fixed-pool slot 25. Both feed already-censused generic header readers. | Fails. Unranked/excluded was again promoted into nonexistent. |
| M4.1 remains technically evidence-backed. | No M4.1 technical premise is changed by the residual fixed-pool candidates. | Survives, but does not establish priority. |
| M4.1 should be the sole active packet. | The one-active-packet rule cannot bypass an exact residual M2 discriminator already named by the evidence. | Fails as a priority conclusion. |

## Exact arithmetic correction

The 64-record pool is `[0x0059B628,0x0059D728)` with stride `0x84`.
Consequently:

```text
0x0059B628 + 25 * 0x84 = 0x0059C30C
0x0059B628 + 63 * 0x84 = 0x0059D6A4
```

The first hard-truth report correctly identified `0x0059D6A4` as slot 63 but
left `0x0059C30C` only as a “separate object.” That phrase is true if it means
a distinct record, but it cannot place the address outside the finite pool:
`0x0059C30C` is exactly the first dword of slot 25. Their corresponding
`0x1C`-stride source records are `0x0059A16C` and `0x0059A594` in the same
`LEVEL.RAW` type-`0x23` table classified by M2.40.

This correction does not prove either word is zero at a consumer or M1-
derived. It proves both are finite members of the already bounded pool and
cannot be dismissed as a new arbitrary-object search.

## Residual slot-25 reader

Dispatcher `0x00418780` case 1 tail-jumps at `0x00418791` through thunk
`0x00401294` to `0x004317D0`. That function uses exact slot 25:

- `0x00431804` tests flags at `0x0059C368`, which is slot 25 `+0x5C`;
- `0x00431983` pushes fixed record `0x0059C30C`;
- `0x004319CB` calls the thunk for `0x00459620`; and
- `0x00459628-0x0045962B` reads the record first dword and immediately uses
  it in `0x005B18E0 + I * 4`.

M2.40 proves that mode-2 removal can zero a positive fixed-pool record without
clearing `+0x5C`. Therefore the exact `0x4001` flag test at
`0x00431804-0x00431815` does not by itself rule out late zero at the fixed
reader. Other case-1 predicates and source/state conditions remain to be
classified. This is a bounded reader-time reachability question, not a zero
claim.

The normal-update order already used by M2.40 reaches fixed-pool update
`0x0041EC40` before the later dispatcher call at `0x004145BB`. Case 1 and
case 9 are two exact targets of that same finite dispatcher, so slot 25 is not
an arbitrary whole-program alias hypothesis.

## Residual slot-63 readers

`0x004467E0` and `0x00446870` each read their argument's first dword and use it
twice as an index into the exact header table:

- `0x004467E4-0x004467E6` and `0x0044681E-0x00446825`;
- `0x00446874-0x00446876` and `0x004468AE-0x004468B5`.

All five direct calls pass fixed slot 63 `0x0059D6A4`: `0x00415EFF`,
`0x0041C854`, `0x0042E92C`, `0x004401F5`, and `0x0046810D`. The calls at
`0x00415EFF` and `0x0042E92C` have an explicit `I == 0x23` gate. The other
three are guarded by surrounding state rather than an immediate first-dword
comparison. Whether those state gates can coexist with M2.40's late zero, and
whether any such path intersects M1, remains an exact finite question.

The first audit explicitly called slot 63 lower-ranked rather than exhausted.
M2.40 then expressly prohibited adding `0x0059D6A4`. Its completion cannot be
silently generalized into a slot-63 reader/caller disposition.

## Boundary of the surviving candidate

The next packet need not reopen all 64 pool objects. M2.36 already classifies
the list-driven and current-object generic readers at its current-invocation
boundary, while M2.40 supplies the shared first-dword writer/source census.
The residual surface is only:

- fixed slot 25 at `0x0059C30C` through case-1 call `0x004319CB` and reader
  `0x00459628-0x0045962B`; and
- fixed slot 63 at `0x0059D6A4` through the five cited calls and readers
  `0x004467E0/0x00446870`.

For those exact paths, a follow-up can reuse the M2.40 writer set, classify
consumer gates and update order, decide reader-time zero, and intersect the
value/predicate closure with the established M1 record/payload route. It must
stop with a causal edge or bounded negative and must not add another pool,
reader family, resource family, runtime, mutation, semantic name, or PS1
comparison.

## Hard-truth verdict

The second deferral does **not** survive. M2.40 remains complete and negative
for slots 2/3, but `DEC-20260813-051` incorrectly treats completion of that
declared packet as retirement of the wider fixed-pool candidate family. One
explicitly retained lower-ranked slot and one omitted exact pool-slot
classification leave a finite PC-native successor.

Restore M2 to `Active` on offline M2.41, limited to the residual fixed slot-25
and slot-63 reader/caller paths above. Return M4/M4.1 to `Planned`; the M4.1
technical boundary remains intact.
