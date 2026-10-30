# M2 exact `0x0A6C` builder-input localization

## Scope and provenance

This is an offline, PC-native slice of only record
`[0x0A6C,0x0A9C)` in the accepted M2.20 control and replacement
`CHARS/FLICK.ALL` files. The executable is the authoritative PC binary with
SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
The source files remain unmodified work copies with SHA-256 values:

- control: `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`;
- replacement: `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.

Byte positions were enumerated by an exact two-file comparison restricted to
the 48-byte record. Native data flow was checked with GNU `objdump -d
-Mintel` over caller `0x0044F8E0` and builder `0x00405FE0`. This report does
not retain source payload values or assign field, asset, primitive, material,
or pixel meanings.

## Exact differing-byte set

The record contains exactly 12 differing positions in four three-byte spans:

| absolute file span | record-relative span | unchanged separator |
|---|---|---|
| `0x0A6C..0x0A6E` | `S+0x00..S+0x02` | `S+0x03` |
| `0x0A90..0x0A92` | `S+0x24..S+0x26` | `S+0x27` |
| `0x0A94..0x0A96` | `S+0x28..S+0x2A` | `S+0x2B` |
| `0x0A98..0x0A9A` | `S+0x2C..S+0x2E` | `S+0x2F` |

The masked selector at `S+0x03` remains form `0x3C`. No other byte in this
record differs.

## Caller argument construction

At `0x0044F8EA`, `S = *(entry+0x20)`. The selector-2 route calls the thunk to
`0x00405FE0` at `0x0044F99D`. The fourteen arguments, numbered in callee
order, are:

| arg | caller source | relationship to the 12 differences |
|---:|---|---|
| 1 | pointer `S+0x04` | none |
| 2 | low word `S+0x0A`; high word retained from `S+0x2E` | high half includes `S+0x2E` |
| 3 | dword `S+0x00` | includes `S+0x00..S+0x02` |
| 4 | pointer `S+0x0C` | none |
| 5 | low word `S+0x12`; high word retained from `S+0x2E` | high half includes `S+0x2E` |
| 6 | dword `S+0x24` | includes `S+0x24..S+0x26` |
| 7 | pointer `S+0x1C` | none |
| 8 | low word `S+0x22`; high word retained from `S+0x2E` | high half includes `S+0x2E` |
| 9 | dword `S+0x2C` | includes `S+0x2C..S+0x2E` |
| 10 | pointer `S+0x14` | none |
| 11 | low word `S+0x1A`; high word retained from `S+0x2A` | high half includes `S+0x2A` |
| 12 | dword `S+0x28` | includes `S+0x28..S+0x2A` |
| 13 | `(word(S+0x2E) >> 8) & 0x1F` | depends only on unchanged `S+0x2F` |
| 14 | constant zero | none |

The apparent duplicate paths do not enlarge the changed-byte set. The
builder reads args 2, 5, 8, and 11 only as low words at
`0x00406AE8`, `0x00406C25`, `0x00406D88`, and `0x00406ED2`.
Consequently, the copied high halves containing `S+0x2E` or `S+0x2A` are
discarded on those paths. The same changed positions remain live through
args 9 and 12 instead.

## Admission slice

Before any direct changed-byte argument is read, the builder admission path
uses:

- arg 13 at `0x00405FE3` for the family/table gate; because it is derived
  only from unchanged `S+0x2F`, both files select the same index;
- args 1, 4, 7, and 10 at `0x00406015`, `0x00406028`,
  `0x00406035`, and `0x00406046`, reading only unchanged source spans
  `[S+0x04,S+0x0C)`, `[S+0x0C,S+0x14)`, `[S+0x1C,S+0x24)`, and
  `[S+0x14,S+0x1C)`;
- caller global `0x0055C794`, consulted from `0x00406554`; the caller derives
  its classification from the sign/zero state of `word(S+0x2E)`. That word
  is positive and nonzero in both files, so the stored classification is the
  same even though its low byte differs;
- per-frame globals and transformed values derived from the unchanged pointer
  spans at the mapped no-append branches.

All mapped no-append decisions precede the successful vertex-count write at
`0x004069A1`. Arg 14 is first loaded at `0x004066ED`, after those decisions,
and is constant. Arg 13 is also unchanged when reused after admission.

Therefore the smallest differing-byte set that reaches an admission
predicate is empty. Static PC data flow does not support attributing M2.29's
`0/1/0` append outcome to any of the 12 source differences.

## Post-admission append inputs

The successful vertex-count write at `0x004069A1` precedes the first reads of
the four direct changed-byte dwords:

| record-relative span | live arg | first builder read | extracted byte PCs | resulting store |
|---|---:|---|---|---|
| `S+0x00..S+0x02` | 3 | `0x004069B3` | `0x004069B7..0x00406AA1` | `0x00406C11`, vertex record `+0x10` |
| `S+0x24..S+0x26` | 6 | `0x004069C9` | `0x004069CD..0x00406AA4` | `0x00406D5B`, vertex record `+0x10` |
| `S+0x2C..S+0x2E` | 9 | `0x004069DF` | `0x004069E6..0x00406A84` | `0x00406EBE`, vertex record `+0x10` |
| `S+0x28..S+0x2A` | 12 | `0x004069F8` | `0x004069FF..0x00406AA7` | `0x00406FFF`, vertex record `+0x10` |

Each three-byte source span is independently extracted, scaled by native
state, packed, and stored as a dword at `+0x10` in one of the four appended
`0x20`-byte vertex records. This structural name intentionally assigns no
semantic meaning to that dword.

The smallest changed-byte-to-append-input set is therefore all 12 exact
positions. Native data flow distinguishes four separate post-admission
outputs; none is an alternative to another at this boundary.

## Result and contradiction

M2.30 closes with two exact results:

1. all 12 source differences reach four byte-derived, post-admission append
   inputs; and
2. no source difference reaches a builder admission predicate in a way that
   differs between these files.

This refines M2.29 rather than invalidating it. The fresh `0/1/0` receipt is
an exact arm-local outcome, but its append decision must depend on admission
state outside the differing source set. The record's changed inputs only
affect the conditional append payload after admission succeeds.

The next discriminator should remain offline first: backward-slice the exact
`0x00405FE0` no-append branches to the smallest non-source, per-frame input
set and design metadata-only evidence capable of identifying the first
different predicate. Any live capture requires a new exact question and
fresh explicit authority.
