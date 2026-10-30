---
type: experiment
id: EXP-20260817-182
date: 2026-08-17
question: 'Does independent review support the input census - the identifier decodings, both function extents, the binding-table writer census, and the Bounded row?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline audit; GNU objdump 2.46; radare2 5.9.8; no runtime, debugger, or target write
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: fresh-context audit at clean HEAD 67ca1b5; read-only toward game media and originals; nothing committed or modified by the auditor
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-input-static-census.md
addresses:
  - "0x00430C3F"
  - "0x00431022"
  - "0x00430B10"
  - "0x00430FFD"
  - "0x004D9CF9"
  - "0x0042ED77"
file_offsets: []
result: reject-false-writer-negative-corrected-controls-are-configurable
created: 2026-08-17T08:30:00
updated: 2026-08-17T08:30:00
tags:
  - re/experiment
  - re/audit
  - re/input
  - research/coverage
---

# EXP-20260817-182 - Independent input census audit

## Verdict

**REJECT** at `67ca1b5`, on one failed completeness claim that was also the
packet's headline modding guidance — and the correction makes the packet
materially better, because the thing the census said it could not find is
there.

Everything else reproduced: both GUID decodings, both `DIDATAFORMAT`
decodings and their flag names, every vtable offset against the documented
`IDirectInputA` / `IDirectInputDeviceA` / `IDirectInputDevice2A` layouts, both
cooperative-level decodings, both function extents (every direct branch
enumerated in each), the twelve binding pairs and their DIK names, the twelve
loop iterations, the `DIK_TAB` special case, the direction jump/byte tables
including that only the four direction masks pass the bound check, the
right-modifier folding, the dead-thunk claim in full, and every quoted
disassembly block byte for byte.

The auditor also verified the §0 novelty negative exactly: **0 hits** for all
ten addresses, case-insensitively and in both leading-zero and short forms,
across all **504** Vault notes and all 43 markdown exports of the parent tree
`0f69566` —
and confirmed every token credited to `ghidra-evidence.json` is present. The
prior packet's prior-art failure mode did not recur.

## Defects

1. **The §3 writer census was false.** It said "No *other* writer was found",
   listing the remaining references as two reads and three byte reads. The
   image contains **22 further stores** into `[0x004D8430, 0x004D8490)`, in two
   blocks of eleven — `0x00430C3F`-`0x00430CBC` and
   `0x00431022`-`0x004310A4` — each copying scancodes out of a `0x18`-stride
   byte array based at `0x004D9CF9`. `0x00430B10` is the exact inverse and is
   **eleven** byte reads, not the single read listed. A dispatcher at
   `0x00430FF6` / `0x00430FFD` selects between the defaults writer and the
   array-apply block. So a key-configuration path exists, and the census
   declared it absent on the strength of a scan that, run correctly, is what
   finds it. The false negative had propagated to `KU-070`, the coverage row's
   open question, Current State and the modding guidance.
2. **`DIEDFL_ALLDEVICES` was a wrong identifier decoding.** The documented
   `DIEDFL_ALLDEVICES` is `0x00000000`; `1` is `DIEDFL_ATTACHEDONLY`. It was
   also the one named DirectInput identifier in the packet for which no
   byte-level comparison was shown, against the packet's own stated rule.
3. **§4's evidential limit was false.** It said "no instruction seen here
   indexes `DIJOYSTATE` with it" for the joystick pair table's first column.
   The eight-iteration loop at `0x0042ED6F`-`0x0042ED8C` — inside the extent §2
   establishes — does exactly that, testing `[esi + 0x00598B90]` where
   `0x00598B90 = 0x00598B60 + 0x30` is `rgbButtons`. The reading is Confirmed
   by instruction, not Inferred.
4. **Both "instruction order" claims were false**; the two tables are listed in
   address order. All values were correct — only the stated ordering property
   was asserted without being checked.
5. **"the two reads in §2" undercounted** its own section, which documents
   three.
6. **§6 cited `0x0042F6AC`** for a `GetDeviceState` call that is at
   `0x0042F6AE`.

## Minor findings, all applied

Two §0 quotations were attributed to the right facts but the wrong source
wording; both are now quoted verbatim from the file named, and re-verified with
line-joined matching. §1.1's block silently elided `0x0042F39C: mov esi,0x1` —
the instruction §1.4's annotation depends on — now restored. §2.2 said the axis
store fires "when any of the four fired"; its guard is actually `edi`, set for
**any** pressed binding entry before the bound check. A second writer of the
joystick pairs at `0x0042F250`-`0x0042F2EB` was unrecorded. The
`0x0042EBC0` dossier's structure-access list omitted the `0x00598B90`
indexing.

## What survived

Listed in the verdict. Additionally: `0x0042F43D` is the **only** call to
`0x004AFEA8` in the image, so the audio census's "sole `DirectInputCreateA`
call site" anchor holds; the chooser contains zero references to any
DirectInput global and `0x0042EBC0` contains no `GetAsyncKeyState` reference,
so the disjointness claim holds; `esi` is not reloaded between `0x004A7841`
and any of the eight `call esi` sites; and the `DIJOYSTATE` layout is
self-confirmed by the binary, since `0x30 + 32 = 0x50` is the decoded
`dwDataSize`.

## Scope answers

- **Bounded is correct for Input.** `Mapped` requires runtime evidence, which
  the packet disclaims throughout. The row's open question was partly stale on
  arrival because of defect 1 and is now rewritten.
- **The §0 prior-art and novelty boundary is honest** — the strongest section
  of the packet, and verified exactly.
- **Both function extents are correct and complete.** But the extent being
  right is not the same as the range having been read: `0x0042ED6F`-`0x0042ED8C`
  lies inside the stated extent, went undocumented, and falsified an unhedged
  negative written over it.

## Limitations of this audit

Entirely static and offline. The DirectInput constants, GUIDs, `DIJOYSTATE`
layout and vtable orders were checked against documented values from
knowledge — no local `dinput.h` exists on this host, so there is no on-disk
citation for them, though the `DIJOYSTATE` layout is self-confirmed by the
binary. The enclosing functions of `0x00464E1C`/`0x0049BDB7`, the enumeration
callback, `0x005988E0`, and the consumers of `0x00598B10` were not analysed —
all correctly declared out of scope. The extents and callers of `0x00430C30`,
`0x00430B10` and the function containing `0x00431013` were not established;
only that they write the table and that the dispatcher branch is live.

## Hygiene

At the audited commit `67ca1b5`: `make vault-lint` 508 notes / 0 errors / 0
warnings; `make audit-tracked` 0 violations; `make test` **686 passed** of
denominator **686**, reproduced by a second run. Qualified by the open
`KU-065`. The auditor notes that `KU-065`'s register text is written against a
648-test suite and its denominator is now stale relative to the current 686.

**During the correction pass**, `make test` returned `1 failed, 685 passed` at
the `KU-065` node, with two immediately following runs at `686 passed`. The
first correction commit's message asserted "canonical suite 686 passed" before
that run had been read; the message was corrected by amendment, and both the
recurrence and the false assertion are recorded in `KU-065` and
[[Environment Status]]. Asserting a gate result without reading it is the same
class of error as asserting that corrections landed without verifying them.

## Correction

All six defects and every minor are applied in the commit recording this audit,
across the export, `EXP-20260817-181`, both dossiers, `KU-070`, the coverage
row and Current State. Each edit was re-read and the absence of the stale text
verified by search before the commit.

## Corrections to this audit

[[EXP-20260817-183 - Second independent input census audit]] found one figure
in this note wrong: the novelty negative was verified across **504** Vault
notes, not 508. 508 is the count at the audited commit `67ca1b5`, which
includes the packet's own notes; the negative was correctly run against the
parent `0f69566`, which has 504. The conclusion — 0 hits for all ten addresses
— was independently re-derived and stands.

That round also refined one of this audit's findings rather than overturning
it: block A (`0x00430C3F`-`0x00430CBC`) is reached only through thunk
`0x00401DF2`, which has **zero** call sites and zero data occurrences, so block
A's reachability is unestablished. The remappability conclusion rests on
block B, which is live off the dispatcher, and on `0x00430B10`.
