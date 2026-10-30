---
type: experiment
id: EXP-20260817-185
date: 2026-08-17
question: 'Does the PC port have an event VM or data-driven trigger stream, and is it the same machinery as the creature scripts or separate?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static analysis; GNU objdump 2.46; repository Python 3.14
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: read-only disassembly and direct byte decoding of the exact retail work copy; no runtime process, debugger, breakpoint or target write
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-event-static-census.md
addresses:
  - "0x005982B0"
  - "0x005982AC"
  - "0x00598670"
  - "0x0042D980"
  - "0x0042D9D0"
  - "0x0042DA00"
  - "0x0042DA70"
  - "0x0042DB10"
  - "0x0042DCA0"
  - "0x004D81A8"
  - "0x004D81E8"
  - "0x0043DAF5"
  - "0x0043DB10"
file_offsets:
  - "0x02CD80"
  - "0x02CE70"
  - "0x02CF10"
  - "0x02D0A0"
  - "0x0D6DA8"
  - "0x0D6DE8"
result: event-row-bounded-callback-registry-not-a-vm-and-disjoint-from-the-creature-scripts; closed unaccepted after six audits per DEC-20260817-138
created: 2026-08-17T11:30:00
updated: 2026-08-17T11:30:00
tags:
  - re/experiment
  - re/static
  - re/events
  - research/coverage
---

# EXP-20260817-185 - PC event subsystem static census

## Date

2026-08-17.

## Question

[[Subsystem Coverage Map]] lists Event/scripting at **Touched**, with one
anchor — five `EVENT : Event >>>%s<<< ...` log strings found incidentally by
the creature census, with no event code read — and the open question "does the
PC port have an event VM or data-driven trigger stream, and is it the same
machinery as the creature scripts or separate?". This is the third and last row
of the recorded Actors/AI → Input → Event/scripting preference.

Bounded reconnaissance. It advances no milestone gate and M5 stays where
`EXP-20260816-171` left it.

## Binary SHA-256

`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`, re-hashed
from `work/copies/BUGS_PC-full-disc/bugs.exe` before analysis.

## Environment

Fedora Linux 44, offline. GNU objdump 2.46 (`-d -M intel`) and direct
little-endian byte decoding from repository Python 3.14.

## Environment version

`objdump 2.46-3.fc44`.

## Working directory

`/home/dev/ABLPC`.

## Configuration

Read-only. No process launched, no debugger, no breakpoint, no target write, no
`originals/` path, no PS1 source, and no game asset read.

## Procedure

1. Re-hash the work copy and dump `.text`.
2. **Before any analysis**, grep every file in the export directory — including
   the generated `ghidra-evidence.json` — and the Vault, for the five `EVENT`
   strings and every address subsequently used.
3. Locate every reference to each string, and take the enclosing functions.
4. Establish each function's extent from its `ret` and padding, and enumerate
   every direct branch inside it, **before** scoping any claim to it.
5. Derive the table layout from the `id`-scaled addressing, then cross-check it
   against the destroy pass's completely different addressing form.
6. Decode the registered records from file bytes.
7. Test the "same machinery as the creature scripts?" question by address
   intersection in both directions.

## Expected

Either an interpreter over an instruction stream — in which case the row's
question resolves to "a VM", and the comparison against the creature scripts is
meaningful — or a different structure entirely, in which case say so and record
what it is.

## Observed

### Confirmed

- **The event table is `[0x005982B0, 0x00598670)`: 16 records of `0x3C`
  bytes.** `0x0042DB10` copies 15 dwords to `[eax*4+0x5982b0]` where `eax = id
  * 15`, so base `0x005982B0`, stride `0x3C`; the destroy pass `0x0042DA70` and
  dispatch pass `0x0042D980` each iterate 16 records; `0x005982B0 + 16 * 0x3C =
  0x00598670`, which is exactly where a buffer whose first 128 bytes are zeroed
  begins — 128 is the width of the write, not a known object size. That buffer
  is not the log formatter's output buffer — `0x004ADEA0` formats into a
  `0x400`-byte stack local — but a **vararg** pushed by the caller, supplying
  the second `%s` at the four log sites whose format string has two.
- **A record carries three native callbacks, not code.** `+0x04` is called at
  `0x0042DC2A`, `+0x08` at `0x0042D9A5` and tail-jumped at `0x0042D9E6`,
  `+0x0C` at `0x0042DB67`, `0x0042DCF6` and `0x0042DAAD`. `+0x04` and `+0x0C`
  are named **create** and **destroy** on the binary's own authority: each call
  is preceded, a few instructions earlier, by a log call passing `"create
  function %s called"` / `"destroy function %s called"`. `+0x08` has no such
  string and is left **unnamed**. `+0x00` is the id word used as the table
  index, `+0x10` a name passed as a `%s` at all eight log calls — though only
  two of them (`0x0042DAA5`, `0x0042DAD3`) take it from the *table* record, the
  other six from the caller's — and `+0x34` an in-use flag set to `1` at
  `0x0042DBE0`. `+0x10` is also the one field with no `id`-scaled absolute form
  at all: `0x005982C0` occurs zero times in the file.
- **The layout is confirmed twice, from different addressing forms.** It was
  derived from `id`-scaled absolute addresses, then checked against the destroy
  pass, which walks the same records backwards with `esi` on `+0x34` starting
  at `0x00598668` — all **nine** of its distinct record-relative displacements
  resolve consistently, reaching every field except `+0x00`. The check confirms
  the relative layout against a second addressing form; the origin itself is
  imported from the first derivation, so it is not independent of that anchor.
- **`0x005982AC` is written with the current record pointer** at `0x0042D99A`
  and `0x0042D9DA`, three instructions before the `+0x08` call, and **is never
  read**: both sites are `a3` stores and a whole-file little-endian scan finds
  exactly those two occurrences. What it is for is therefore unestablished.
- **The id is never bounds-checked.** All three `id`-addressed entry points
  (`0x0042DA00`, `0x0042DB18`, `0x0042DCA8`) `movsx` a signed word and scale it
  by `0x3C` with no range test before the first access. Only the two iterating
  passes are bounded, by their own counters.
- **`+0x00` and `+0x10` survive every clear.** None of the four clearing paths
  writes `0x005982B0` or the name block at `+0x10`. That block is never reached
  by an absolute address at all: `0x005982C0` occurs zero times in the file, so
  `+0x10` — uniquely among the ten fields — has one derivation, not two.
- **Seven functions, all with verified extents.** `0x0042D950`, `0x0042D980`,
  `0x0042D9D0`, `0x0042DA00`, `0x0042DA70`, `0x0042DB10`, `0x0042DCA0`. Each
  has a single `ret` followed by padding, and every direct branch inside each
  range was enumerated: the only outbound target from any of them is
  `0x00401CF8` (→ `0x004ADEA0`), which writes the log file `"bugs.log"`. That
  filename and the mode string `"at"` decode from file offsets
  `0x0E7E64`/`0x0E7E60`, and `0x004ADEA0` also reaches
  **`KERNEL32.dll!DeleteFileA`** with the filename, through the wrapper
  `0x004B13E0` (`call DWORD PTR ds:0x864670` at `0x004B13E5`, IAT slot
  `0x00864670`) — guarded by `0x004E9170` so it fires once. Its whole body is
  gated on `0x008620AC`. `ghidra-evidence.json` carries this function and all
  five of its callees, so the reading is also prior art.
- **Four of the seven have no reachable caller.** `0x0042D9D0` (run one),
  `0x0042DA00` (clear slot) and `0x0042DCA0` (delete one) are each reached only
  through a thunk with zero callers, and neither thunk nor function occurs
  anywhere in the file as a 4-byte little-endian value. `0x0042D950` is the
  fourth: it is reached through thunk `0x0040169F`, which also has zero
  callers, and the same `rep stos` is inlined at the four two-`%s` log sites
  instead. All four fail the same two-direction test in the same way; all eight
  scans return zero occurrences.
- **There are exactly two static registration call sites.** Whether either
  executes is not established — the enclosing function is unanalysed. The
  register thunk `0x004017B2` has two call sites, `0x0043DAF5` and
  `0x0043DB10`, both pushing static `.data` records: `0x004D81A8` — id 2, name
  `"WINDOWS"`, callbacks `0x004AE580` / `0x004AE780` / `0x004AE810` — and
  `0x004D81E8` — id 3, name `"DIRECTX"`, callbacks `0x0042BA60` / `0x0042BB30`
  / `0x0042BB50`.
- **This supplies the missing caller the audio census recorded.**
  `EXP-20260816-159` observed that `0x0042BA60`, its own central initializer,
  has zero direct call sites and is reached only through the `.data` record at
  `0x004D81E8`. That record is an event record, and `0x0042BA60` is its `+0x04`
  field — the slot the register function calls at `0x0042DC2A`. That is the
  static path by which the audio and input bring-up would be entered, not an
  observation that it runs; either way it is why a direct-call census found no
  entry point.
- **No absolute reference to the table exists outside these seven functions.**
  This is a negative on one addressing form, not a proof of isolation — see the
  export's §2.1, which is normative. All 26,713
  type-3 base relocations were decoded and dereferenced: exactly 47 point into
  `[0x005982A0, 0x005986F0)` and all 47 lie inside `0x0042D950`-`0x0042DD94`.
  Because a PE loader must relocate every absolute 32-bit reference, this is
  exhaustive **for the absolute form**; a computed reference carries no
  relocation. The range excludes `0x00598290`, which does have five external
  references and is recorded as outside this subsystem — widening to include it
  gives 52. Found by the second-round audit; restated with the correct range
  and re-derived by two methods after the third-round audit caught the first
  version mixing two ranges. The fifth-round audit then withdrew the claim that
  a window sweep closes the indexed-base gap: it does not, so this is a strong
  negative on the absolute addressing form only, not a proof of isolation.
- **The two machineries are disjoint.** None of `0x0041DC60`, `0x004C83F0`,
  `0x0041E848`, `0x0059B628` or `0x004C8758` is referenced anywhere in
  `0x0042D950`-`0x0042DD90`, and none of `0x005982B0`, `0x005982B4`,
  `0x005982AC` or `0x00598670` is referenced anywhere in
  `0x0041DC60`-`0x0041E845`.

### Inferred

Two things:

- the **32-byte** width of the name at `+0x10`, which comes from the next
  accessed field being `+0x30`, not from any instruction;
- the fopen/fprintf/fclose roles of `0x004B0730`, `0x004B13A0` and
  `0x004B04E0`, which are undecoded. That `0x004ADEA0` writes a log file is
  **not** inference — it reaches `DeleteFileA` with `"bugs.log"` — but the
  shape of the three calls after it is.

Everything else is an instruction or a decoded byte. `create` and `destroy` are
the binary's own words, taken from the log strings that precede those calls;
`+0x08` is deliberately left unnamed because nothing in the binary names it.

### Unknown

What the six callback targets do (`0x0042BA60`'s role is prior art from the
audio census); whether anything registers an event outside the two static
sites, and so whether slots other than 2 and 3 are ever occupied; the meaning
of `+0x02`, `+0x30`, `+0x32` and `+0x38`, which are only ever zeroed; the
meaning of `0x0059F7F0` in the registration sequence; the enclosing functions
and callers of the **nine** sites that reach the live entry points; and every
runtime fact, since nothing was run.

## Artifacts

`static/exports/BIN-97c95ba5572dce63/SUBSYS-event-static-census.md` carries the
full derivation, the quoted disassembly, the record layout with its second
derivation, the decoded records, the extent table and the disjointness check.

Its §0 records that `ghidra-evidence.json` already carries decompiled bodies
for `0x0042DB10`, `0x0042D980` and `0x0042DA70` which render the base, the
`0x3c` stride, the three callback slots, the flag and the name — so **the table
geometry and record layout are prior art**, re-derived here from instructions
rather than first found here. **Its caller data is prior art too**: the three
`thunk_FUN_` entries carry populated `callers` lists covering 7 of the 9
reachers this census lists, and an earlier draft of §0 wrongly asserted those
lists were empty. What is new is the four dead entry points (ghidra has no
entry for those four at all), the two reachers its lists omit (`0x004AE863`,
`0x004121A1`), the decoded records and registration sites, the disjointness
result, the audio cross-link, and the negative results.

## Addresses

Table `0x005982B0`; current-record pointer `0x005982AC`; log scratch
`0x00598670`; dispatch pass `0x0042D980`; run-one `0x0042D9D0`; clear-slot
`0x0042DA00`; destroy-all `0x0042DA70`; register `0x0042DB10`; delete-one
`0x0042DCA0`; the two registered records `0x004D81A8` and `0x004D81E8`;
registration sites `0x0043DAF5` and `0x0043DB10`.

## File offsets

`0x02CD80` (dispatch), `0x02CE70` (destroy all), `0x02CF10` (register),
`0x02D0A0` (delete one), `0x0D6DA8` and `0x0D6DE8` (the two records).

## Interpretation

The row's question has a clean negative answer on both halves.

**There is no event VM and no data-driven trigger stream.** There is no opcode,
no instruction stream and no interpreter anywhere in this subsystem. An "event"
is a 16-slot registry entry holding a name and three native code pointers, and
the only data involved is the 60-byte record itself. The word "event" here
names a *subsystem lifecycle slot* — bring this component up, tick it, tear it
down — not a gameplay trigger.

**It is not the creature machinery, and shares nothing with it.** The two were
tested by address intersection in both directions and are disjoint: different
table, different stride, different source of records, and native function
pointers where the creature scripts have interpreted opcodes.

That makes the honest scope of the row narrow but real: the PC port has an
event system, it is a callback registry, and gameplay triggers — if the port
has data-driven ones at all — are not here. The known trigger evidence remains
the grain-gate family under the separate Triggers row.

The cross-link to the audio census is the most useful by-product. That census
had a genuine loose end — its own central initializer with zero callers — and
this packet closes it: `0x0042BA60` is the `"DIRECTX"` event's create callback.
It also refines one field reading in that census, which called the record's
leading value "a count of 3"; it is the event id. Its offsets were exactly
right.

## Result

The coverage row **Event/scripting system** is proposed to move Touched →
**Bounded** with the anchors above. No milestone status changes and no runtime
claim is made. `KU-071` records what the six callbacks do, whether any event is
registered outside the two static sites, and the four never-read fields.

## Follow-up

The cheapest next step is static and has a concrete target: `0x004AE580` /
`0x004AE780` / `0x004AE810`, the `"WINDOWS"` event's three callbacks. Naming
those would say what the event abstraction is *for* — window/message pump, most
likely, but that is a guess this packet does not make.

The cheapest *decisive* step for `KU-071`'s registration question is also
static: determine whether the register thunk `0x004017B2` can be reached by
computed dispatch, since a scan-based negative is exactly what the input
census's `GetAsyncKeyState` finding showed can mislead.
