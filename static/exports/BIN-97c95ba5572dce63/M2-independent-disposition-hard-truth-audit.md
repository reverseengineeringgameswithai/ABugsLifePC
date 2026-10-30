# M2 independent disposition hard-truth audit

## Scope and authority

- Independent verifier packet: M2.42.
- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Audit target: `EXP-20260813-058` and the stronger proposed conclusion that
  no exact finite PC-native M2 successor remains in the evidence already
  cited through that experiment.
- Evidence reviewed: `EXP-20260813-049` through `EXP-20260813-058`, their
  static reports, the M1 record/positive-target closures, `KU-023`, relevant
  address-based dossiers, the exact work-copy executable, and the current
  roadmap/decision history.
- Independent native verification: GNU objdump 2.46-3.fc44.

This was read-only, offline, and PC-native. It did not launch or mutate the
game, inspect PS1 evidence, change a parser or schema, assign semantic names,
or conduct a broad whole-program, pool, or resource-family search.

## Executable identity

The independently rehashed read-only work copy was:

```text
path: work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
size: 1069056 bytes
SHA-256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
format: pei-i386
```

This matches the canonical PC executable and the hash declared by
`EXP-20260813-058`.

## M2.41 packet-local falsification

### Exact object arithmetic and complete fixed-call census

The bounded pool remains `[0x0059B628,0x0059D728)` with stride `0x84`:

```text
0x0059B628 + 25 * 0x84 = 0x0059C30C
0x0059B628 + 63 * 0x84 = 0x0059D6A4
```

A fresh whole-image direct-call scan reproduces the complete relevant thunk
surface:

```text
0x00459620 thunk 0x00401DAC: calls 0x0041ED19 and 0x004319CB
0x00446870 thunk 0x004016DB: call  0x00415EFF
0x004467E0 thunk 0x00401D48: calls 0x0041C854, 0x0042E92C,
                                      0x004401F5, 0x0046810D
```

Only `0x004319CB` is the fixed slot-25 call; `0x0041ED19` uses the current
pool object and is independently dominated by the positive first-dword test
at `0x0041EC6A-0x0041EC6E`. The five slot-63 calls are therefore complete at
the declared direct-call boundary.

### Slot 25

Native instructions confirm that the load-bearing call gate is the later
sequence, not the earlier arm selected by `EXP-20260813-057`:

- `0x004318E4` reloads slot 25 `+0x5C`;
- `0x004318EA-0x004318F3` requires bit `0x4000` clear;
- `0x004318F9-0x00431900` requires counter `0x00599AB0 == 0`;
- a positive route count is required at `0x00431912-0x0043191B`;
- `0x00431983` passes fixed `0x0059C30C`; and
- `0x004319CB` calls `0x00459620`.

Every `0x0041EC40` pass clears `0x4000` before rejecting a zero first dword.
Thus an unpopulated zero retains a clear flag, and a value zeroed late by
`0x0041BBBA` can retain zero after the next pass clears the flag. This is
conditional static reachability, not proof that a named shipped scene
realizes every independent route/counter predicate.

At `0x00459628-0x00459636`, `I == 0` selects header table entry
`0x005B18E0`. The independently established ID-zero header starts at retained
index zero, so its first-word test branches to the zero return. The exact
reader-time result in M2.41 is supported.

### Slot 63

Native instructions independently reproduce both categorical exclusions:

- `0x00415E50` requires slot first dword `I == 0x23` before call
  `0x00415EFF -> 0x00446870`;
- `0x0042E91A-0x0042E925` requires the same value before call
  `0x0042E92C -> 0x004467E0`.

The other calls at `0x0041C854`, `0x004401F5`, and `0x0046810D` test paired
state, event, or route predicates but do not test the slot first dword.
Both readers use `I` directly in `0x005B18E0 + I * 4` and consume header
`+0x04`; exact zero therefore selects the validated ID-zero retained end
index 24. The bit-`0x80` state can survive independently of a later
first-dword removal until a selected consumer clears it. M2.41's conditional
zero-reachability claim is supported, while its shipped-scene realization
remains explicitly unclaimed.

### Order and M1 intersection

The exact normal update order is:

```text
0x00414578 -> 0x0043F9E0
0x00414592 -> 0x00415E30
0x00414597 -> 0x0041EC40
0x004145A6 -> 0x00468010
0x004145BB -> dispatcher 0x00418780
return from 0x004144C0
0x0040FFDE -> M1 coordinator 0x0044D430
```

Scene-initialization call `0x0042E92C` is also outside the M1 record and
positive-target closures. Structured references independently show no direct
fixed-pool first-dword, `0x00599AB0`, `0x0059D9A0`, or `0x005C5864`
provenance in `0x0044D430`, `0x004498F0`, or `0x0045A7F0`. The complete
first-dword writer result from M2.40 traces population/removal to separate
`LEVEL.RAW` type-`0x23` and fixed-pool state. No selected value or direct
enabling predicate is M1 record-, relocated-payload-, or positive-target-
derived. The M2.41 causal negative is supported at its declared boundary.

## Stronger disposition audit

The two earlier failed deferrals established the required distinction:
"nothing was ranked" is a roadmap fact; "no finite retained candidate
exists" requires an evidence census. The following matrix tests the latter
claim against every exact retained surface in the cited evidence.

| Retained surface | Independent disposition |
| --- | --- |
| Direct ID-zero reads in `0x00402DC0` and `0x0044C440` | `EXP-20260813-035` and native `0x0044D4BC -> 0x0044D4FA -> 0x0044D57F` order place the coordinator-side direct read before M1 root load and record enumeration. |
| Exact M1 positive-target selector-2 inputs in `0x0045A7F0` | `EXP-20260813-050` classifies the ten inline Direct3D allocation arms; no ID-zero header/range or selected-resource provenance remains inside that finite function surface. |
| Generic initializer `0x00444EF0` | Sole cited call supplies exact index 11, not zero. |
| Fixed slots 2/3 in `0x00436B40` | M2.40/`EXP-20260813-056` supplies the complete store set, conditional reader-time zero, and separate-source M1 negative. |
| Fixed slots 25/63 in `0x00459620`, `0x004467E0`, and `0x00446870` | M2.41/`EXP-20260813-058`, independently confirmed above. |
| Current/list readers `0x00459620`, `0x00456640`, and `0x00436AF0` | `0x0041ED19` is dominated by the positive first-dword test; `0x00456640` runs immediately after building a list only from positive first dwords; `0x00436AF0` is reached at `0x0041DFAF` before the possible mode-2 removal at `0x0041EEE4`. Zero is excluded at those exact reads. |
| Coordinator list reader `0x00448350` | Mode-2 removal at `0x0041BBBA` compacts the affected pointer out of list `0x0059D7E0` at `0x0041BBC4-0x0041BC0C`; the later coordinator reader therefore does not retain the newly zeroed object. Its call at `0x0044D4E6` also precedes M1 root load and enumeration. |
| Twenty signed selector words in `0x0044CA00` | `EXP-20260813-053` classifies the complete finite writer set; the sole nonzero image table has no `0xFF99`/signed `-103`, and the current M1 route does not produce the surface. |
| Alternate `0x0059A5F0 != 0` arm retained by `EXP-20260813-035` | Native `0x0040FFE9 -> 0x00413900 -> 0x0040FFEE -> 0x0044D430` order remains pre-M1. `0x00413900` has no direct ID-zero header/range reference; the coordinator retains the same pre-record direct-reader order. This is not an omitted M1-to-resource selector. |
| Persistent/copied cross-frame state, indirect aliases, other readers/families | These remain honest limitations, but the cited evidence supplies no exact producer-to-consumer edge, exact ID-zero value, or finite target set. They are not already-retained bounded successors. |

No item in the exact cited surface remains in the same state as the omitted
slot-2/slot-3 and slot-25/slot-63 candidates: each finite candidate has a
completed bounded disposition, while the remaining possibilities are not
exact candidates. This is not a whole-program proof that no M1-to-resource
edge exists in the executable.

## Verdict

**ACCEPT.** M2.41 is supported, and no exact finite PC-native M2 successor
remains in the evidence already cited through `EXP-20260813-058`.

The milestone itself is **not complete**: its first exit gate and `KU-023`
still lack an exact M1 scene-record/positive-target-to-ID-zero-resource
selection edge. The evidence-backed disposition is therefore:

- move M2 from `Active` to `Deferred`, with its causal gate unchanged;
- keep M3 `Planned` because its current entry condition remains unmet; and
- activate exact M4.1, whose hash-guarded asset-free whole-file replacement
  boundary survived both earlier audits.

Revisit M2 only when cited PC-native evidence exposes one exact finite
dependency candidate, a concrete mod goal supplies a bounded discriminator,
or a contradiction invalidates a completed negative. "Persistent state may
exist" or an unranked wider search is not such a trigger.
