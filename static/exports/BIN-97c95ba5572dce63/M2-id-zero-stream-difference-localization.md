# M2 ID-zero stream-difference localization

> [!IMPORTANT] M2.26 correction
> `EXP-20260813-039` proves that the `0x80`-stride arena previously called
> hardware output is the selector-1 native-software path. Selector-2 Direct3D
> uses separate batch storage. The interval, difference, and bounded-walk
> results below remain unchanged.

## Provenance and scope

- Executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Exact unchanged `PC/BUGS/CD/CHARS/FLICK.ALL`, size `0x34EC`, SHA-256
  `a2f23220392d7fb4880bbab7acab9393fe6da059961d620e7b85c8df3f4f4ac6`.
- Exact accepted replacement source `PC/BUGS/CD/CHARS3/FLICKD.ALL`, size
  `0x34EC`, SHA-256
  `6e5afb4f9ea649bc305fdafeb027aece25914b27a017d04841bf4298634079a4`.
- PC address anchors: cursor construction and entry-pointer store in
  `0x00448010` at `0x00448085-0x00448181`; stream reader `0x0044F8E0` at
  `0x0044F8EA-0x004509EF`.
- Prior runtime correlation: accepted Direct3D replacement and repeated local
  visible difference in `EXP-20260812-033`.
- Experiment: `EXP-20260813-037`.

This report covers only the 24 retained ID-zero intervals established by
`EXP-20260812-034`. It records offsets and structural metadata, not file
payload bytes. It does not define a general `.ALL` layout or assign field,
asset, record, primitive, filename, or character meanings.

## Exact interval construction

Native instructions independently establish the arithmetic used here:

1. `0x00448085-0x0044808D` doubles the first dword, locates the table at file
   offset `0x2C00`, then advances the arena cursor from file offset zero to
   four.
2. Both files have count 30 at `0x2C00`; descriptors begin at `0x2C04` with
   exact stride `0x4C` and end at `0x34EC`.
3. `0x004480F4-0x004480F6` stores the current arena cursor to retained entry
   `+0x20` before `0x00448171-0x00448181` doubles the current descriptor's
   first dword and advances that cursor.
4. The 30 length values and the retained-entry comparison values are
   byte-identical between the two files. Their doubled lengths partition the
   stream arena `[0x0004,0x2C00)` without overlap or overflow. Descriptors
   0-23 map directly to retained entries 0-23; later descriptors are outside
   this packet.

The resulting retained intervals are listed below. Offsets are zero-based
file offsets and intervals are half-open.

## Walk classification rule

For each file independently, the walk starts at the interval beginning:

- a nonzero selector byte at stream-relative `+0x03` must mask to `0x34` or
  `0x3C`, selecting an exact `0x24` or `0x30` record span;
- a zero selector reaches the 16-bit control test; value one would consume a
  four-byte continuation marker, while another value terminates;
- every control read and selected record span must remain inside the enclosing
  entry interval.

Here, both files produce identical selector modes, record starts, and terminal
control offsets. No continuation marker occurs and no bound is contradictory.
A differing byte is classified **walk-reached** when it lies in a fully
bounded selected record span or control span visited by this procedure. This
is a cursor/record-span result; it does not claim that every byte in a selected
span is individually dereferenced or contributes to a hardware submission.

Notation in the table is `mode/signature @ stream-relative record start`.
Ranges such as `0x000..0x0C0/0x30` are inclusive arithmetic progressions.
The terminal offset is stream-relative, and the reached span includes its
four-byte control range.

| Entry | Exact file interval | Record plan | Terminal | Reached span | Differing bytes | Reached | Not reached |
|---:|---:|---|---:|---:|---:|---:|---:|
| 0 | `[0x0004,0x0174)` | `3C/S1 @ 0x000..0x0C0/0x30` | `0x0F0` | `[0x000,0x0F4)` | 60 | 60 | 0 |
| 1 | `[0x0174,0x0248)` | `34/S2 @ 0x000`; `3C/S1 @ 0x024,0x054` | `0x084` | `[0x000,0x088)` | 33 | 33 | 0 |
| 2 | `[0x0248,0x042C)` | `34/S2 @ 0x000,0x024`; `3C/S1 @ 0x048..0x108/0x30` | `0x138` | `[0x000,0x13C)` | 78 | 78 | 0 |
| 3 | `[0x042C,0x04E4)` | `34/S2 @ 0x000`; `3C/S1 @ 0x024..0x084/0x30` | `0x0B4` | `[0x000,0x0B8)` | 45 | 45 | 0 |
| 4 | `[0x04E4,0x0674)` | `34/S2 @ 0x000..0x048/0x24`; `3C/S1 @ 0x06C..0x15C/0x30` | `0x18C` | `[0x000,0x190)` | 99 | 99 | 0 |
| 5 | `[0x0674,0x0858)` | `34/S2 @ 0x000,0x024`; `3C/S1 @ 0x048..0x108/0x30` | `0x138` | `[0x000,0x13C)` | 78 | 78 | 0 |
| 6 | `[0x0858,0x0910)` | `34/S2 @ 0x000`; `3C/S1 @ 0x024..0x084/0x30` | `0x0B4` | `[0x000,0x0B8)` | 45 | 45 | 0 |
| 7 | `[0x0910,0x0AA0)` | `34/S2 @ 0x000..0x048/0x24`; `3C/S1 @ 0x06C..0x15C/0x30` | `0x18C` | `[0x000,0x190)` | 99 | 99 | 0 |
| 8 | `[0x0AA0,0x0AA4)` | none | `0x000` | `[0x000,0x004)` | 0 | 0 | 0 |
| 9 | `[0x0AA4,0x0D40)` | `34/S2 @ 0x000`; `3C/S1 @ 0x024..0x1A4/0x30` | `0x1D4` | `[0x000,0x1D8)` | 117 | 117 | 0 |
| 10 | `[0x0D40,0x1C28)` | detailed below | `0xAE0` | `[0x000,0xAE4)` | 728 | 728 | 0 |
| 11 | `[0x1C28,0x1C5C)` | `3C/S1 @ 0x000` | `0x030` | `[0x000,0x034)` | 12 | 12 | 0 |
| 12 | `[0x1C5C,0x1C90)` | `3C/S1 @ 0x000` | `0x030` | `[0x000,0x034)` | 12 | 12 | 0 |
| 13 | `[0x1C90,0x1E44)` | `34/S2 @ 0x000..0x06C/0x24`; `3C/S1 @ 0x090..0x180/0x30` | `0x1B0` | `[0x000,0x1B4)` | 108 | 108 | 0 |
| 14 | `[0x1E44,0x1EFC)` | `34/S2 @ 0x000`; `3C/S1 @ 0x024..0x084/0x30` | `0x0B4` | `[0x000,0x0B8)` | 45 | 45 | 0 |
| 15 | `[0x1EFC,0x2160)` | `34/S2 @ 0x000..0x090/0x24`; `3C/S1 @ 0x0B4..0x144/0x30` | `0x174` | `[0x000,0x178)` | 93 | 93 | 0 |
| 16 | `[0x2160,0x2194)` | `3C/S1 @ 0x000` | `0x030` | `[0x000,0x034)` | 12 | 12 | 0 |
| 17 | `[0x2194,0x21C8)` | `3C/S1 @ 0x000` | `0x030` | `[0x000,0x034)` | 12 | 12 | 0 |
| 18 | `[0x21C8,0x237C)` | `34/S2 @ 0x000..0x06C/0x24`; `3C/S1 @ 0x090..0x180/0x30` | `0x1B0` | `[0x000,0x1B4)` | 108 | 108 | 0 |
| 19 | `[0x237C,0x2434)` | `34/S2 @ 0x000`; `3C/S1 @ 0x024..0x084/0x30` | `0x0B4` | `[0x000,0x0B8)` | 45 | 45 | 0 |
| 20 | `[0x2434,0x2698)` | `34/S2 @ 0x000..0x090/0x24`; `3C/S1 @ 0x0B4..0x144/0x30` | `0x174` | `[0x000,0x178)` | 93 | 93 | 0 |
| 21 | `[0x2698,0x2808)` | `3C/S1 @ 0x000..0x0C0/0x30` | `0x0F0` | `[0x000,0x0F4)` | 60 | 60 | 0 |
| 22 | `[0x2808,0x2978)` | `3C/S1 @ 0x000..0x0C0/0x30` | `0x0F0` | `[0x000,0x0F4)` | 60 | 60 | 0 |
| 23 | `[0x2978,0x2AE8)` | `3C/S1 @ 0x000..0x0C0/0x30` | `0x0F0` | `[0x000,0x0F4)` | 60 | 60 | 0 |

Entry 10 has `34/S2` at `0x000..0x0FC/0x24` and `3C` records at
`0x120..0xAB0/0x30`. Its `3C` signature is S1 except at these exact starts:

| Signature | Entry-10 stream-relative starts |
|---|---|
| S3 | `0x180` |
| S4 | `0x1B0` |
| S5 | `0x1E0` |
| S6 | `0x300`, `0x5A0`, `0x840`, `0x900` |
| S7 | `0x330` |
| S8 | `0x360` |
| S9 | `0x390` |
| S10 | `0x4E0` |
| S11 | `0x540` |
| S12 | `0x5D0` |
| S13 | `0x630`, `0x7B0` |
| S14 | `0x6C0` |
| S15 | `0x6F0` |
| S16 | `0x750` |

## Exact relative difference signatures

For any record listed above, its complete set of differing stream-relative
offsets is:

```text
record start + every member of the named signature
```

Ranges are inclusive. This representation accounts for every differing byte
inside the retained intervals without recording either file's byte values.

| Signature | Mode | Differing offsets relative to record start | Count per record | Occurrences |
|---|---:|---|---:|---:|
| S1 | `0x3C` | `0x00-0x02`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 12 | 123 |
| S2 | `0x34` | `0x00-0x02`, `0x1C-0x1E`, `0x20-0x22` | 9 | 42 |
| S3 | `0x3C` | `0x00-0x02`, `0x20`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 13 | 1 |
| S4 | `0x3C` | `0x00-0x02`, `0x10`, `0x18`, `0x1E`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 15 | 1 |
| S5 | `0x3C` | `0x00-0x02`, `0x08`, `0x20`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 14 | 1 |
| S6 | `0x3C` | `0x00-0x02`, `0x10`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 13 | 4 |
| S7 | `0x3C` | `0x00-0x02`, `0x06`, `0x10`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 14 | 1 |
| S8 | `0x3C` | `0x00-0x02`, `0x0E-0x0F`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 14 | 1 |
| S9 | `0x3C` | `0x00-0x02`, `0x06`, `0x16-0x17`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 15 | 1 |
| S10 | `0x3C` | `0x00-0x02`, `0x16-0x17`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 14 | 1 |
| S11 | `0x3C` | `0x00-0x02`, `0x0E-0x0F`, `0x1E`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 15 | 1 |
| S12 | `0x3C` | `0x00-0x02`, `0x06`, `0x20`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 14 | 1 |
| S13 | `0x3C` | `0x00-0x02`, `0x06`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 13 | 2 |
| S14 | `0x3C` | `0x00-0x02`, `0x0E`, `0x18`, `0x20`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 15 | 1 |
| S15 | `0x3C` | `0x00-0x02`, `0x08`, `0x10`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 14 | 1 |
| S16 | `0x3C` | `0x00-0x02`, `0x08`, `0x24-0x26`, `0x28-0x2A`, `0x2C-0x2E` | 13 | 1 |

The signatures cover 183 selected records and exactly 2,102 differing byte
positions. Terminal controls are identical and contain no differences.

## Whole-file reconciliation

An independent `cmp -l` count reports 2,115 whole-file differing positions:

- 2,102 lie in the contiguous retained interval union
  `[0x0004,0x2AE8)` and are assigned above;
- zero lie in the later, non-retained stream range `[0x2AE8,0x2C00)`;
- 13 lie outside the retained intervals, all in the descriptor table at exact
  file offsets `0x2F28`, `0x2F2C`, `0x2F2D`, `0x2F30`, `0x2F34`, `0x2F38`,
  `0x2F3A`, `0x2F3B`, `0x2F3C`, `0x332C`, `0x34CE`, `0x34CF`, and `0x34D2`.

The 13 descriptor-table differences are recorded only to reconcile the known
whole-file count. They are not retained-stream differences and are not
classified as reads by `0x0044F8E0`.

## Bounded result

Confirmed for the two exact accepted files:

- retained entry 8 is byte-identical across its exact four-byte interval;
- each of retained entries 0-7 and 9-23 contains at least one difference;
- all 2,102 retained-stream differences lie in record spans reached by
  identical, in-bounds `0x34`/`0x3C` walks in both files;
- no differing retained byte is beyond either demonstrated walk;
- the smallest exact stream candidate set for the M2.20 visible outcome is
  therefore `{0-7, 9-23}`, containing 23 entries.

This result does not show that every candidate emits hardware output in the
tested visible frame, that every changed byte is individually read, or that
any candidate accounts for the repeated local rendered difference. Those are
runtime provenance questions downstream of this packet.

## Precise next discriminator

A read-only, matched Direct3D submission-origin capture can compare the
pre/post `0x008082C8` output-counter interval around exact entry handoff
`0x0044C898-0x0044C89E`, recording only entry indices and metadata digests of
new `0x80`-stride records. Any breakpoints or execution control require prior
explicit approval under the Agent Operating Manual. Do not arm the
quarantined `0x0044D794/0x0044D79A` region, write target state, dump payload
bytes, or assign source semantics.
