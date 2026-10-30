---
type: experiment
id: EXP-20260817-186
date: 2026-08-17
question: 'Which candidate module from already-accepted PC evidence satisfies all six M5 entry-gate criteria, and which are rejected and why?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static analysis; GNU objdump 2.46; repository Python 3.14
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: read-only disassembly of the exact retail work copy; no runtime process, debugger, breakpoint or target write
artifacts: []
addresses:
  - "0x0042EBC0"
  - "0x0042ED3E"
  - "0x0042ED6F"
  - "0x0042ED9B"
  - "0x004D8490"
  - "0x00598B10"
  - "0x00598B90"
  - "0x0041DC60"
  - "0x0041E848"
file_offsets:
  - "0x02DFC0"
result: input-action-bit-resolver-selected-creature-vm-rejected-contract-not-bounded
created: 2026-08-17T18:30:00
updated: 2026-08-17T18:30:00
tags:
  - re/experiment
  - re/static
  - milestone/M5
---

# EXP-20260817-186 - M5 third-module candidacy ranking

## Date

2026-08-17.

## Question

[[Project Roadmap]] records M5 as Active with two accepted optional modules and
states that no third module is admitted automatically. A candidate must satisfy
six written entry-gate criteria. M5.1's procedure requires that candidates be
**ranked** and the rejected ones recorded with reasons, before any contract is
derived.

Which candidate from already-accepted PC evidence passes all six?

This packet ranks and selects. It does **not** implement; the implementation is
named as the next packet.

## Binary SHA-256

`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`, re-hashed
from `work/copies/BUGS_PC-full-disc/bugs.exe` before analysis.

## Environment

Fedora Linux 44, offline. GNU objdump 2.46 (`-d -M intel`).

## Environment version

`objdump 2.46-3.fc44`.

## Working directory

`/home/dev/ABLPC`.

## Configuration

Read-only. No process launched, no debugger, no breakpoint, no target write, no
`originals/` path, no PS1 source, no game asset read.

## Procedure

1. Enumerate candidate modules drawn only from **accepted** PC evidence.
2. For each, test entry-gate criterion 1 (bounded contract) directly against
   the binary by enumerating every outbound call in the candidate's code range
   — a candidate that calls engine services does not have a bounded contract.
3. Test the remaining five criteria against recorded evidence.
4. Select one, record why each other is rejected, and name the implementation
   packet.

## Expected

Either a candidate clears all six, or none does and M5 stays Active with the
gap recorded.

## Observed

### Confirmed

- **The creature behaviour VM `0x0041DC60` fails criterion 1.** Its code range
  `0x0041DC60`-`0x0041E845` contains **16 direct call sites to 15 distinct
  thunks**, plus one indirect `call eax` at `0x0041E7C7` (this packet did not trace where
  `eax` is loaded; the accepted census attributes the interpreter's indirect
  call to record `+0x7C`). Resolved targets: `0x004ABE00`, `0x0042AA50`, `0x00464D40`,
  `0x00403A10`, `0x0041A550`, `0x004148A0`, `0x0043C250`, `0x00428990`,
  `0x00428A60`, `0x00436AF0`, `0x0043ADD0`, `0x00431C90`, `0x00432A50`,
  `0x004287D0`, `0x004288F0`. **Three of the fifteen — `0x00464D40`,
  `0x00403A10`, `0x0041A550` — appear in no authored Vault note or export at
  all.** A module whose behaviour depends on fifteen engine services, a
  quarter of them unidentified, does not have a bounded input/output or
  state-transition contract.

- **The input action-bit resolver has a call-free core.** In
  `0x0042EBC0`-`0x0042EEBB` the last outbound transfer of any kind is the
  DirectInput vtable call at `0x0042ED3E` (`call DWORD PTR [ecx+0x1c]`).
  Everything from `0x0042ED41` to the end of the function — the whole binding
  walk and axis-processing body — contains **zero calls**. It is pure
  computation over buffers.

- **Its contract is readable off the instructions.** The keyboard pass at
  `0x0042ED6F`-`0x0042ED8C` walks `ecx` from `0x004D8494` to `0x004D84D4` in
  `0x08` steps; each record supplies a scancode at `[ecx-0x4]` used to index
  the key/button state array at `0x00598B90`, and a 16-bit mask at `[ecx]`
  OR-ed into `di` when that state byte is non-zero. The accumulated word is
  stored to `0x00598B10` at `0x0042ED9B`.

- **The axis path uses a fixed scaling and a symmetric limit.** Axis values are
  reduced by `sar 8` / `and 0xFF` / `sub 0x80` / `shl 8` and compared against
  `0xFFFFD440` and `0x2BC0` — that is **±11200**, the same magnitude either
  side.

- **The four remaining criteria are met from recorded evidence.** Addresses and
  offsets: `SUBSYS-input-static-census.md`, accepted at `EXP-20260817-184`.
  Runtime observations: the CAP-002 input-movie work,
  `EXP-20260815-119`/`-120`/`-121`/`-122`/`-124`/`-125`. Asset-free fixtures:
  both binding tables are executable data, so synthetic tables and synthetic
  state buffers need no game content. Known edge behaviour: the census records
  that `[0x004D8430, 0x004D8490)` is all zero in the file image and written at
  runtime by two distinct paths (46 stores).

### Inferred

That the axis limit is a **deadzone or clamp**. The instructions establish the
comparison and the magnitude; what the engine does with the result beyond the
stores enumerated in the census is not established here.

### Unknown

The three unidentified creature-VM callees; whether the `0x18`-stride
configuration record's layout beyond `0x00431013` affects the binding tables
(`KU-069`); and every runtime fact, since nothing was run.

## Result

**Selected: the input action-bit resolver.** Contract: (key/button state
buffer, axis values, binding tables) → action-bit word, with no engine
dependency.

**Rejected, with reasons:**

| Candidate | Criterion failed | Evidence |
|---|---|---|
| Creature behaviour VM `0x0041DC60` | 1 — bounded contract | 15 engine callees, 3 unidentified |
| Creature word-code **decoder** only (a subset of the above) | none outright — ranked below the winner | It would clear criterion 1, and criterion 5 says "where practical", so the absence of any original counterpart to differ against is a weakness rather than a hard failure. It is rejected as *strictly weaker* than the selected candidate, which has both a call-free core and recorded runtime receipts to test against |
| Event registry `0x0042DB10` | 6 — modding reason | The record holds three native code pointers and no algorithm; there is nothing to reimplement. Its packet is also closed unaccepted (`DEC-20260817-138`) |

The creature VM remains the better *research* target and the worse *module*:
`KU-072` records the three unidentified callees as the concrete next step
toward it.

## Follow-up

The named next packet is **M5.10 — input action-bit resolver contract and
implementation**: derive the full contract from `0x0042ED41`-`0x0042EEBB`
directly rather than from this note's prose, model the mask accumulation and
axis scaling with exact wrapping and shift semantics, refuse rather than guess
on undefined inputs, cover every refusal with an asset-free synthetic test,
and differential-test against the CAP-002 receipts where they constrain the
result.

Two cautions carried forward from the event packet, both recorded in
`DEC-20260817-138`: grep **every** export including `ghidra-evidence.json`
before claiming any of this is novel — the second binding table looked new
here and is in fact already documented at census line 430 — and keep one
normative statement rather than paraphrasing findings across carriers.
