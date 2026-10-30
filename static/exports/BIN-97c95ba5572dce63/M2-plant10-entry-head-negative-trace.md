# M2 plant 10 entry-head negative trace

## Scope and identity

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Runtime entries: first `0x005AAB00`, second `0x005AAB50`, stride `0x50`
- Runtime evidence: `RUN-GDB-20260812-163111` and
  `RUN-GDB-20260812-163840` in
  [[EXP-20260812-024 - Plant10 entry-head bounded negatives]]

No PS1 source or finding was consulted. Field descriptions remain exact
entry-relative offsets.

## Exact population instructions

In `0x00448010`, `eax` selects four adjacent descriptor dwords and
`edi == edx - 0x20` selects the runtime entry head:

```text
004480d2  lea eax,[ecx-0x2e]
004480d6  mov ebx,DWORD PTR [eax]
004480dc  lea edi,[edx-0x20]
004480df  mov DWORD PTR [edx-0x20],ebx
004480e2  mov ebx,DWORD PTR [eax+0x4]
004480e5  mov DWORD PTR [edi+0x4],ebx
004480e8  mov ebx,DWORD PTR [eax+0x8]
004480eb  mov DWORD PTR [edi+0x8],ebx
004480ee  mov eax,DWORD PTR [eax+0xc]
004480f1  mov DWORD PTR [edi+0xc],eax
```

Both guarded Training runs reproduce the same entry heads:

```text
entry 66 at 0x005AAB00: 00000000 00000000 00000000 00000001
entry 67 at 0x005AAB50: 00000000 00000000 00000000 00000001
```

Thus M2.11 watches exactly six dword ranges populated by
`0x004480DF/0x004480E5/0x004480EB`. The observed zeros are exact values, not
an assertion that the offsets are padding or unused.

## Matched runtime windows

Both runs first stop at unique plant 10 post-call `0x0044596D`, verify
resource ID `0x71`, live ANM pointer `0x006C342B`, and indices `66/68`, then
accept only the immediately following common-tail `0x00445B01`.

- `RUN-GDB-20260812-163111` watches first-entry `+0x00/+0x04/+0x08`.
- `RUN-GDB-20260812-163840` watches second-entry `+0x00/+0x04/+0x08`.

In both runs, hardware return breakpoint `0x004679C7` wins with one hit while
all three read watchpoints remain enabled with no hit counts. After deleting
only the return breakpoint, the watches remain armed while execution crosses
the title and reaches logged `NextLife` plus captured live gameplay. The first
title was advanced by a queued load-phase Return; the second by user input.
Neither run retains an unattended title-pause capture, so the exact retained
endpoint is post-title gameplay rather than the pause itself.

## Static consumer context

The Ghidra export contains indexed references to shared-array base offsets
`+0x00/+0x04/+0x08` in multiple address-based functions, including
`0x00444EF0`, `0x00445FF0`, `0x00446430`, `0x00447E30`, `0x00448350`, and
`0x0044CA00`. M2.11 proves none of those or any other CPU instruction reads
the six exact plant 10 ranges during the retained windows. It does not prove
the fields have no consumers for other indices or later events.

Two static indexed reads make the remaining `+0x0C` dword a precise next
surface without assigning it a meaning:

```text
00446a97  mov ecx,DWORD PTR [eax+0xc]
00447668  mov ecx,DWORD PTR [eax+0xc]
```

Both occur in address-based function `0x00446970`. A separate population/copy
path at `0x00447E30` writes destination `+0x0C` at `0x00447EB0`; it is context,
not downstream-reader evidence. No exact plant 10 runtime hit is claimed for
either indexed reader.

## Evidence-strength boundary

**Confirmed within the exact windows:** No CPU read overlaps either entry's
`+0x00/+0x04/+0x08` dword after guarded final plant 10 population, before
scene-resource batch return, or while execution proceeds across the title to
the retained live-gameplay endpoint.

**Inferred:** The remaining observed nonzero entry-head dword `+0x0C` is a
narrower next discriminator than broadening to later unknown fields.

**Unknown:** The meanings and first exact plant 10 consumers of all four head
dwords, the later entry fields, and any M1 placement/resource identity.
