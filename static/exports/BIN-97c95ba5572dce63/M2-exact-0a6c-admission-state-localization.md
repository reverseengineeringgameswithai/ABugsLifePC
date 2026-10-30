# Exact `0x0A6C` admission-state localization

## Scope and provenance

This is an offline, PC-native backward slice for executable
`BIN-97c95ba5572dce63`, SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
It covers only exact retained entry 7/file offset `0x0A6C`, form `0x3C`, at
caller `0x0044F8E0` and builder `0x00405FE0`, from function entry through the
last admission rejection at `0x004066BD`. Evidence is exact `objdump
-Mintel` disassembly of a hash-verified work copy, independently checked
against the Ghidra data-reference and decompiler export in
`ghidra-evidence.json`.

No game was launched. No source, vertex, or index payload was captured or
retained. No source file, runtime tool, parser, or original was changed. No
field, asset, primitive, material, or pixel meaning is assigned, and no PS1
evidence was consulted.

## Exact invariant source inputs

M2.30 proves that the replacement's 12 changed bytes first enter the builder
after successful count write `0x004069A1`. Admission instead uses four
unchanged signed-word triples in this structural order:

| input | pointer argument | exact record words |
|---:|---:|---|
| 0 | 1 | `S+0x04`, `S+0x06`, `S+0x08` |
| 1 | 4 | `S+0x0C`, `S+0x0E`, `S+0x10` |
| 2 | 7 | `S+0x1C`, `S+0x1E`, `S+0x20` |
| 3 | 10 | `S+0x14`, `S+0x16`, `S+0x18` |

Caller instructions `0x0044F92A..0x0044F959` derive a word from the sign and
zero classification of `S+0x2E`. Both exact files classify it positive and
nonzero, so the caller writes value 2 to `0x0055C794`. The page argument is
16 in both files and derives from unchanged `S+0x2F`. These source-derived
values must be validated by a future receipt, but they are not members of the
non-source set.

## Smallest non-source input lattice

The union of physical non-source locations that can affect an admission
decision contains 23 locations. A native-order evaluation needs 21 values
when policy mode is neither 0 nor 1, or 22 when it reads the one active
threshold; it never needs both mutually exclusive thresholds.

| group | exact location | role limited to this slice |
|---|---|---|
| early | `0x005836A4 + page*4` | dword compared with 3 at `0x00405FF7` |
| early | `0x004C4108` | dword root read at `0x00406005` |
| early | `[root + page*4]` | dword tested for zero at `0x0040600B` |
| transform | `0x0063E888`, `0x0063E88C`, `0x0063E890` | row 0 coefficients |
| transform | `0x0063E898`, `0x0063E89C`, `0x0063E8A0` | row 1 coefficients |
| transform | `0x0063E8A8`, `0x0063E8AC`, `0x0063E8B0` | row 2 coefficients |
| transform | `0x0063E8B8`, `0x0063E8BC`, `0x0063E8C0` | row offsets |
| projection | `0x00511508` | signed scale and half-scale input |
| projection | `0x00861DD8`, `0x00861DDC` | two signed offsets |
| bounds | `0x00861C60`, `0x00861DAC` | two signed upper bounds |
| policy | `0x005BA120` | depth-policy selector |
| policy | `0x005B56D0` | read only when policy mode is 0 |
| policy | `0x005BA80C` | read only when policy mode is 1 |

For the proven root value `0x004F1730` and page 16, the dynamic third early
location is `0x004F1770`. A future evaluator must still read the root and
derive the address rather than hard-code that resolved location. Ghidra's
static reference to root base `0x004F1730` is consistent with, but does not
replace, the native indexed memory operand.

Writes to `0x005C5D64` and `0x0076F9A0..0x0076F9AC` are projection scratch,
not inputs. The builder's write of zero to source-derived mode
`0x0055C794` after the orientation branch is likewise not a non-source
input. Batch roots, counts, and later append state are outside this
admission slice except for the early page-pointer existence test above.

This is a static influence union, not proof that every location changes once
per frame. No member can be removed from the exact decision model on the
available evidence, but runtime stability and semantic ownership remain
unmeasured.

## Native arithmetic model

For input signed words `(x_i,y_i,z_i)`, define structural intermediates
`(P_i,Q_i,R_i)` only for this report. Each multiply and add has x86 signed
32-bit wraparound. Each transform row rounds toward zero before shifting:

```text
row(v) = signed16(((v + ((v >> 31) & 0xFFF)) >> 12) + row_offset)
```

Here `v` is the wrapped sum of three coefficient products; the row offset is
added after the shift, then the result is truncated to signed 16 bits.
`R_i` is row 2. Projection uses:

```text
half = signed_trunc_toward_zero(scale / 2)
denom_i = max_signed(half, R_i)
P_i = signed16(signed_idiv(wrap32(row0_i * scale), denom_i) + offset0)
Q_i = signed16(signed_idiv(wrap32(row1_i * scale), denom_i) + offset1)
```

A future evaluator must fail closed on a zero divisor or x86 signed-division
overflow and must reproduce signed-16 truncation and signed-32 wrap exactly.
Host-language unbounded integers or floor division are not equivalent.

## Reduced ordered rejection chain

For exact source-derived mode 2, the admission path reduces to 12 ordered
predicate slots. The two depth-policy instructions are one mutually
exclusive logical slot. The mode-1 orientation rejection at `0x004065E7` is
unreachable for this exact source classification and is omitted; mode 2 must
nevertheless be validated.

| slot | rejecting instruction | reject exactly when |
|---:|---:|---|
| 1 | `0x00405FFF` | page-class dword is not 3 |
| 2 | `0x0040600F` | indexed page-pointer dword is zero |
| 3 | `0x004064E4` | all four `P_i > dword(0x00861C60)` |
| 4 | `0x00406502` | all four `P_i < 0` |
| 5 | `0x00406533` | all four `Q_i > dword(0x00861DAC)` |
| 6 | `0x0040654E` | all four `Q_i < 0` |
| 7 | `0x004065B0` | `A < 0` and `B < 0`, definitions below |
| 8a | `0x00406636` | policy mode 1 and all four `R_i < dword(0x005BA80C)` |
| 8b | `0x00406660` | policy mode 0 and all four `R_i > wrap32(4*dword(0x005B56D0))` |
| 9 | `0x00406672` | `abs(P_0) > 10000` |
| 10 | `0x0040668B` | `abs(P_1) > 10000` |
| 11 | `0x004066A4` | `abs(P_2) > 10000` |
| 12 | `0x004066BD` | `abs(P_3) > 10000` |

With signed-32 wrap at every subtraction, multiplication, and final
subtraction:

```text
A = (Q0-Q1)*(P2-P1) - (P0-P1)*(Q2-Q1)
B = (P2-P3)*(Q1-Q3) - (Q2-Q3)*(P1-P3)
```

If policy mode is neither 0 nor 1, slot 8 passes without reading a threshold.
Passing slot 12 reaches subsequent family/capacity/index work; it does not by
itself prove the final count write. M2.29's existing counter reconciliation
remains the observed append authority.

## Metadata-only discriminator design

The existing safe data watch on selector word `0x0059F7F0` already stops at
next PC `0x0044F951` once for each selected exact record. At this stop `ESI`
is `S`, exact entry/offset/form identity is available, no builder call has
occurred, and the caller has not yet written the source-derived mode. Native
instructions between this stop and call `0x0044F99D` only derive that mode
and construct arguments; they do not change the non-source lattice above.
No new execution breakpoint or watch slot is required.

A purpose-specific future evaluator should:

1. accept only the hash-locked 168-call plan and exact target entry 7/offset
   `0x0A6C`/form `0x3C`;
2. at its existing pre-call stop, transiently read the 12 unchanged source
   words, validate page 16 and derived mode 2, then read non-source values
   lazily in native predicate order;
3. emulate the exact arithmetic and retain only the first rejecting PC (or
   null), evaluated-slot count, predicted append boolean, and a SHA-256 over
   the canonical active non-source input encoding;
4. discard raw source, global, and derived values before any stdout, JSONL,
   or result serialization;
5. use the existing entry-post closure and schema-5 counter reconciliation
   to retain the observed append boolean, and require prediction to match it;
6. optionally re-digest the same active non-source addresses at entry-post
   and fail closed if the digest changed. Exact `0x0A6C` is the last selected
   builder call in entry 7, so this uses the already accepted closure; a
   mismatch rejects the receipt rather than guessing when state changed.

The smallest reviewable serialized target row is therefore:

```text
schema_version
entry_index=7, file_offset=0x0A6C, form=0x3C
page_16_validated=true, caller_mode_2_validated=true
active_state_sha256, evaluated_predicate_count
first_reject_pc=null|one_of_the_13_concrete_reject_PCs
predicted_append, observed_append, prediction_matches_observation
raw_inputs_retained=false, payload_bytes_retained=0
```

There are 13 concrete reject PCs because logical slot 8 has two mutually
exclusive native locations. A full predicate vector and raw `(P,Q,R)` values
are unnecessary: first reject plus evaluated count identifies the native
prefix. The digest is an equality/coherence receipt; no raw input value is
serialized.

Acceptance must retain M2.29's full plan/order, renderer markers, selected
root/page, no-flush, signal, cleanup, detach, survival, and source-hash gates.
Before any live use, synthetic tests must cover all 12 slots, both depth
branches and the skip, arithmetic wrap/truncation, zero-divisor and division-
overflow failures, prediction/counter mismatch, digest mismatch, and a scan
proving raw values never reach retained output.

## Discriminating interpretation

In a separately authorized fresh control/replacement/control packet, select
a first predicate only if both accepted controls have the same first-reject
PC and the replacement has no reject. If controls reject at different PCs,
or any predicted/observed/digest gate fails, preserve temporal variation or
the exact contradiction rather than selecting an input. Even an accepted
result would establish only arm-local admission state for this record. It
would not prove that a source byte caused admission, that appended data
reached a visible pixel, or any format semantics.
