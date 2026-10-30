# M2 deferral hard-truth audit

## Scope

- Independently rechecked executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Audit target: the conclusion in `EXP-20260813-054` that M2 had no finite
  PC-native successor and should be deferred while M4.1 became active.
- Evidence reviewed: `EXP-20260813-049` through `EXP-20260813-054`, their
  cited static exports, native disassembly, the pre-M2.39 roadmap, the current
  implementation boundary, and the exact local work-copy hashes.
- No runtime, mutation, parser/schema change, asset edit, or cross-port source
  was used.

## Premise matrix

| Premise | Adversarial check | Verdict |
| --- | --- | --- |
| M2's causal exit gate remains unsupported. | `EXP-20260813-049/052/053` still provide no exact M1 record/positive-target-to-ID-zero resource-selection edge. | Survives. M2 cannot be marked complete. |
| The selected signed-selector candidate is exhausted. | `EXP-20260813-053` classifies its finite native writer set and proves that its canonical nonzero table has no signed `-103`. | Survives at the packet's current-invocation boundary. |
| No finite PC-native M2 successor remains. | `EXP-20260813-051` itself leaves exact persistent header-index inputs `0x0059B730` and `0x0059B7B4` unknown at `0x004372A2-0x004372B7` and `0x00437337-0x0043734C`. The later scope disposition did not census their producers. | Fails. "No ranked candidate had been selected" was incorrectly promoted into "no finite candidate exists." |
| M4.1 is technically evidence-backed. | `EXP-20260812-033/049` record one accepted exact replacement. The local user-owned work copy independently rechecks both files at 13,548 bytes with the recorded hashes. No protected game-data extension is tracked by Git. | Survives, but establishes viability rather than priority. |
| M4.1 should become the sole active packet. | The roadmap permits incremental M4 accumulation, but the one-active-packet rule does not justify bypassing an exact unresolved M2 surface. | Fails as a priority conclusion. M4.1 remains planned. |

## Exact missed surface

The generic-reader census records these native expressions in
`0x00436B40`:

- `I0 = *(uint32_t *)0x0059B730` at
  `0x004372A2-0x004372B7`;
- `I1 = *(uint32_t *)0x0059B7B4` at
  `0x00437337-0x0043734C`; and
- each index addresses the already selected header table as
  `0x005B18E0 + I * 4`, so exact value zero selects the ID-zero header.

These are not an unbounded "persistent state may exist" hypothesis. The
fixed pool is exactly `[0x0059B628,0x0059D728)`, has 64 records, and has stride
`0x84`, as independently recorded in `EXP-20260813-053`. Exact arithmetic
places the two words at record-first-dword slots 2 and 3:

```text
0x0059B730 - 0x0059B628 = 0x108 = 2 * 0x84
0x0059B7B4 - 0x0059B628 = 0x18C = 3 * 0x84
```

Native `0x0041C420` disassembly independently confirms the finite pool: it
clears `0x840` dwords (`0x2100` bytes) from `0x0059B628` at
`0x0041C424-0x0041C430`, then walks 64 source/destination records with
destination stride `0x84` at `0x0041C58A-0x0041C597`. This confirms initial
zero, not reader-time zero or an M1-derived producer. Those are precisely the
questions the omitted writer/producer census must decide.

`0x0059D6A4` is likewise fixed-pool slot 63, but it is lower-ranked for the
next packet because one retained consumer requires exact value `0x23` and the
two slot-2/slot-3 reads provide the tighter direct zero discriminator in a
single native reader. `0x0059C30C` remains a separate object and is not
implicitly added.

## M4.1 boundary recheck

The exact local user-owned work-copy observations are:

```text
CD/CHARS/FLICK.ALL   size 13548  SHA-256 a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6
CD/CHARS3/FLICKD.ALL size 13548  SHA-256 6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4
```

This matches `EXP-20260812-033/049`. It supports keeping M4.1 as a planned,
bounded implementation packet. It does not prove `.ALL` layout, compatibility,
resource identity, or that M4.1 should displace an available M2 packet.

## Hard-truth verdict

The deferral conclusion does **not** survive intact. M2 remains incomplete,
but deferring it was premature because an exact finite producer surface was
already preserved in the cited evidence and was not ranked during M2.39.
Restore M2 to `Active` and select an offline producer census of
`0x0059B730/0x0059B7B4`. Return M4 and M4.1 to `Planned`; their technical
boundary survives and can resume after the active M2 packet or a later
recorded reprioritization.

## Remaining unknown

This audit does not claim either fixed-pool first dword is zero when read, is
derived from an M1 record/payload, or supplies the missing causal edge. It
proves only that the question is finite, PC-native, directly tied to the
selected ID-zero header formula, and was omitted from the prior continuation
disposition.
