---
type: experiment
id: EXP-20260816-172
date: 2026-08-16
question: 'Where does the PC actor pool live, and is there a state machine or program list behind it?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline static analysis; GNU objdump 2.46; rabin2 5.9.8; repository Python 3.14
environment_version: objdump 2.46-3.fc44
working_directory: /home/dev/ABLPC
configuration: read-only disassembly, string reads and direct byte decoding of the exact retail work copy, plus one metadata-only disc directory listing; no runtime process, debugger, breakpoint or target write
artifacts:
  - static/exports/BIN-97c95ba5572dce63/SUBSYS-creature-actor-static-census.md
addresses:
  - "0x0059B628"
  - "0x00599EB0"
  - "0x0046574D"
  - "0x004679A0"
  - "0x0041C420"
  - "0x0041BD10"
  - "0x0041B9F0"
  - "0x0041EC40"
  - "0x0041DC60"
  - "0x0041E848"
  - "0x004C83F0"
  - "0x004C8758"
  - "0x004C881F"
  - "0x00599C60"
  - "0x0059D7E0"
file_offsets:
  - "0x064B4D"
  - "0x01B820"
  - "0x01B110"
  - "0x01ADF0"
  - "0x01E040"
  - "0x01D060"
  - "0x01DC48"
  - "0x0C6FF0"
  - "0x0C7358"
  - "0x0DCEFC"
result: creature-actor-row-proposed-bounded-with-a-word-code-behaviour-vm
created: 2026-08-16T23:59:00
updated: 2026-08-16T23:59:00
tags:
  - re/experiment
  - re/static
  - re/actors
  - research/coverage
---

# EXP-20260816-172 - PC creature actor pool and behaviour VM census

## Date

2026-08-16.

## Question

[[Subsystem Coverage Map]] lists **Enemies, actors and AI** as Untouched, with
one incidental spider observation from `EXP-20260815-129` and the open
question "where is the actor pool, and is there a state machine or program
list?". This is the second coverage-driven packet after the audio census, and
the first row in the recorded Actors/AI → Input → Event/scripting preference.

It is bounded reconnaissance. It advances no milestone gate, and M5 stays
where `EXP-20260816-171` left it.

## Binary SHA-256

`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`, re-hashed
from `work/copies/BUGS_PC-full-disc/bugs.exe` before analysis.

## Environment

Fedora Linux 44, offline. GNU objdump 2.46 (`-d -M intel`), `rabin2` 5.9.8 for
the string table, and direct little-endian byte decoding of the same file from
repository Python 3.14.

## Environment version

`objdump 2.46-3.fc44`, `radare2 5.9.8`.

## Working directory

`/home/dev/ABLPC`.

## Configuration

Read-only. No process was launched, no debugger attached, no breakpoint set,
no target memory written, no `originals/` path opened, no PS1 source read, and
no game asset opened beyond one metadata-level listing of
`work/copies/BUGS_PC-full-disc/PC/BUGS/CD`.

## Procedure

1. Re-hash the work copy and dump `.text` with objdump.
2. Follow the already-known fixed pool at `0x0059B628` from the M2 exports
   outward: find its build, its per-frame update, and its release path.
3. Decode every switch table reached from those functions directly from file
   bytes rather than from decompiler text.
4. Follow the record field written by the builder from the level-data side and
   read the log string emitted at that load site.
5. Decode the resulting instruction stream format and validate it against all
   40 shipped programs.

## Expected

Either a pool with per-instance state that some dispatcher advances — in which
case the dispatcher's shape answers the "state machine or program list"
question — or no such structure, in which case the row stays Untouched with a
recorded negative.

## Observed

### Confirmed

- **A 64-slot instance pool exists at `[0x0059B628, 0x0059D728)`, stride
  `0x84`.** The clear at `0x0041C424`-`0x0041C430` writes `0x840` dwords; the
  build loop ends on `cmp ebx,0x40` at `0x0041C594`; the update loop ends on
  `cmp esi,0x59d792` at `0x0041ED55`, whose last base is `0x0059D6A4`. The
  extent agrees with the independently derived slots 2 and 3 in
  `M2-fixed-pool-index-producer-census.md`.
- **Each slot is bound one-to-one to a `0x1C`-byte record supplied by level
  data.** `0x0046574D`-`0x0046576A` zeroes and then copies exactly `0x700`
  bytes into `[0x00599EB0, 0x0059A5B0)` when the loader's record type is
  `0x23`; `0x700 / 0x1C = 64`, and the builder steps the source by `0x1C` and
  the pool by `0x84` in the same loop. **This is entirely prior art**, as two
  audits had to establish: the copy site, byte count, source extent,
  type-`0x23` gate and `0x1C` stride are in
  `M2-fixed-pool-index-producer-census.md`, and both 64s plus the
  `LOAD: Type 35, CreatListRam.` string are in
  `M2-plant-request-origin-static-trace.md` — which additionally observed that
  string in retained hardware logs. Restated here so the model reads whole; not
  a new result.
- **The executable names that packet itself** (prior art — see above).
  Directly after the copy,
  `0x0046576F` logs the string at `0x004DE2FC` (which carries no conversion
  specifier, though the site pushes an argument anyway):
  `LOAD: Type 35, CreatListRam.` — type 35 decimal is the `0x23` tested at
  `0x00465748`. The name is the game's, not this packet's.
- **The pool is built once during level load, under a gate.** `0x0041C420` is
  reachable only through thunk `0x00401AC3`, whose one call site `0x004679A0`
  is inside level-load entry `0x004671D0` (no `ret` between `0x00467971` and
  it) and is skipped when bit `0x10` of `0x005C5E88` is set.
- **The slot's first dword is a type id with a hard domain of 6..41.** Both the
  builder switch (`0x0041C493`, tables `0x0041C600`/`0x0041C5B0`) and the
  release/reinitialise switch (`0x0041BAF0`, tables `0x0041BC48`/`0x0041BC18`)
  test `type - 6` against `0x23`. The same dword indexes `0x005B18E0 + id * 4`
  at `0x004372B7`.
- **The builder's per-type arm writes a positive count of 1-8 into the source
  field that becomes slot `+0x6E`, a thunk pointer into slot `+0x7C`, both, or
  neither — and "neither" is the largest group.** Over the 36-type domain: 9
  types get both (6, 9, 10, 13, 15, 17, 34, 37, 39), 5 get only a thunk (16,
  22, 29, 31, 36), 5 get only a count (12, 18, 19, 40, 41), and 17 take the
  default arm and get neither. Ten distinct handlers appear, all inside
  `0x0041BEF0`-`0x0041C2C0`. Where a count is written it must be `> 0` for the
  activation branch at `0x0041EC74`, and the release path sets `+0x6E` to `0`
  at `0x0041BBBC`.
- **The per-frame update `0x0041EC40` selects slots by distance from the
  camera.** For each slot it clears flag `0x4000`, and when a squared distance
  built from `+0x64`/`+0x66`/`+0x68`, the position, and the accepted camera
  common block `0x00599C90`/`94`/`98` falls under `((+0x6A >> 3) + 0x258)²`, it
  appends the slot to a NULL-terminated pointer list at `0x0059D7E0` and sets
  `0x4000`. It is called from `0x00414597` inside `0x004144C0`.
- **A word-code interpreter runs per slot.** `0x0041DC60` loads the program
  counter from slot `+0x70`, decrements the wait counter `+0x60` and runs only
  when it goes negative, fetches a signed 16-bit opcode, range-checks
  `opcode + 1` against `0x19`, and dispatches through the 26-entry table at
  `0x0041E848` covering opcodes `-1` to `24`. It persists the program counter
  back to `+0x70` at `0x0041E147`, and at three further sites past it —
  `0x0041E1EB` (`+2`), `0x0041E2E1` (`+6`) and `0x0041E7FE` (`+2`) — each
  reached only when the pending opcode is a blocking one.
- **The interpreter invokes the per-type handlers.** At `0x0041E79E` it loads
  `[esi+0x7c]`, null-checks it, builds a stack record containing the pool
  record pointer, and executes `call eax` at `0x0041E7C7`. That is the only
  found edge from the interpreter to the ten handlers the builder installs,
  and it is register-indirect — no scan would have found it.
- **Scope of the interpreter reading.** `0x0041DC60` extends to `0x0041E845`.
  Its only `ret` is at `0x0041E7D3` and is **not** the end:
  `0x0041E7D4`-`0x0041E845` is entered from `0x0041E6CD`/`0x0041E6D8`, shares
  the frame, and leaves by `jmp 0x41e6e6` at `0x0041E841`, whose last byte —
  `0xFF` — is at `0x0041E845`. This packet analyses the fetch
  loop, the opcode handlers and the mode dispatch, i.e. through `0x0041E1A8`;
  the region past it is enumerated for `+0x5C` accesses, `+0x70` writers, its
  indirect call and the record fields it touches, but **what it computes is
  not analysed**.
- **Blocking opcodes select the frame's mode.** An opcode whose handler does not advance the
  program counter ends the frame (`0x0041E131`-`0x0041E135`). After the loop, a
  second dispatch (`0x0041E14F`, tables `0x0041E8F4`/`0x0041E8D4`) reads the
  *pending* opcode and selects one of five modes for the rest of the frame.
  Eight opcodes have no handler body — 0, 5, 6, 7, 9, 17, 18, 20 — and seven of
  them are exactly the seven that select a mode. Opcode 0 is the single
  exception: it blocks but lies outside the `5..20` window, so it leaves the
  mode at its initialised `0`, which is what opcode 7 writes explicitly. The
  two dispatches are independent in the code and agree to that one case.
- **Forty programs ship in the image.** `0x004C83F0` holds 40 ascending
  pointers; the bodies are contiguous in `[0x004C7D00, 0x004C83F0)` and the
  last ends exactly at the table's first byte.
- **The program format decodes without a single inconsistency.** Using only
  the PC advances read from the handlers — plus the stall-breaker
  `add edi,0x2` at `0x0041E140` for the eight opcodes that have no handler
  body — all 40 bodies decode to 463 instructions with zero misalignment, all
  69 branch and jump targets land on instruction boundaries, and every opcode
  value in the dispatch table is used at least once.
- **Operands stay inside their tables, but only one handler enforces that.**
  Opcode 11's operands are exactly 1..9 against a 9-entry table, and it is the
  **only** handler with a range check (`dec eax / cmp eax,0x8 / ja` at
  `0x0041DF4C`-`0x0041DF50`). Opcode 13's sequence operands span 1..24 against
  a 28-entry table, but its handler at `0x0041E00D`-`0x0041E02F` has no `cmp`
  and no `ja` — it indexes `[eax*4+0x4c8754]` with the sign-extended operand
  directly. That span is therefore a property of the shipped data, not an
  invariant the code maintains, and opcode 13 joins the unbounded-index class
  recorded in `KU-069`.
- **An independent site confirms `+0x70` is that program counter.**
  `0x004372A8`-`0x004372BE` writes `[0x004C8474] + 0x1A` into slot 2's `+0x70`.
  `0x004C8474` is script-table entry 33, and `0x004C8240 + 0x1A` is exactly the
  seventh decoded instruction of script 33 — the head of that script's second
  behaviour block.
- **One opcode tests distance to Flik.** Opcode 16 (`0x0041E078`) compares the
  squared XZ distance between the slot's `+0x04`/`+0x0C` and
  `0x0059D910`/`0x0059D918` against the operand squared. Those two globals are
  the live Flik X and Z established at runtime by `EXP-20260815-128`, so a
  static AI primitive and an independent runtime identification agree.
- **The "random" opcodes read a shipped file.** Opcodes 2, 3 and 14 consume
  bytes through the cursor `0x00599C60`, which is set to `0x0081B428` at
  `0x00403C73` and `0x0042E7C8`; `0x0081B428` is the buffer passed with the
  string `"rand.dat"` at `0x0041011E`-`0x00410128`, and `RAND.DAT` is present
  in the retail `PC/BUGS/CD` listing.
- **The type byte is used as a table index without an upper bound.** At
  `0x0041C463`-`0x0041C47D` only a zero test precedes
  `mov cl,[eax+0x4c881f]` and `mov [eax*8+0x599ca8],cl`. The cleared region at
  `0x00599CA8` is `0x200` bytes, so `type = 65` writes exactly `0x00599EB0`,
  the first byte of the source table copied above.

### Inferred

That these 64 slots are **creatures** in the gameplay sense rests on the
executable's own `CreatListRam` log name, the per-type positive counts, the
player-distance opcode, and the release path — not on any runtime observation.
Which type id denotes which creature, and whether every id 6..41 is an enemy
rather than another kind of placed actor, is not established. No field is
named "health", "speed" or "AI state" anywhere in this packet.

That the shared `rand.dat` cursor bears on gameplay determinism is plausible —
it is referenced 380 times across the image (181 reads, 199 writes, of which 2
are the initialisation and 197 write a computed value back), so two runs that
consume it in different orders would diverge — but nothing here measures that, and
`EXP-20260815-125`'s open determinism question is untouched.

### Unknown

The ten per-type `+0x7C` handlers; the nine opcode-11 subroutines
(`0x004288F0`, `0x004287D0`, `0x00432A50`, `0x00431C90`, `0x0043ADD0`,
`0x00436AF0`, `0x00428A60`, `0x00428990`, `0x0043C250`); what the five modes
do; the role of `0x00599CA8`, `0x004C881F`, `0x0059D99E`, `0x0059D9A0`,
`0x0059D9A6`, `0x0059D9A7` and `0x00599B20`; which shipped levels pass the
`0x005C5E88` bit-`0x10` gate; and every runtime fact, since nothing was run.

## Artifacts

`static/exports/BIN-97c95ba5572dce63/SUBSYS-creature-actor-static-census.md`
carries the full derivation, the record and source field maps, every decoded
table, and a self-checking reproduction snippet for the 40-program decode.

## Addresses

Pool `0x0059B628`; source table `0x00599EB0`; loader copy `0x0046574D`;
build call site `0x004679A0`; builder `0x0041C420`; slot initializer
`0x0041BD10`; release/reinitialise `0x0041B9F0`; per-frame update
`0x0041EC40`; interpreter `0x0041DC60`; opcode dispatch `0x0041E848`; script
pointer table `0x004C83F0`; frame-sequence table `0x004C8758`; per-type
boolean table `0x004C881F`; shared byte cursor `0x00599C60`; active list
`0x0059D7E0`.

## File offsets

`0x064B4D` (loader copy), `0x01B820` (builder), `0x01B110` (initializer),
`0x01ADF0` (release), `0x01E040` (update), `0x01D060` (interpreter),
`0x01DC48` (opcode dispatch), `0x0C6FF0` (script table), `0x0C7358`
(frame-sequence table), `0x0DCEFC` (`CreatListRam` string).

## Interpretation

The answer to the row's open question is both halves at once: the actor pool is
the 64-slot array at `0x0059B628`, and behind it sits a **program list** — 40
word-code programs selected per instance by a level-data byte — driven by an
interpreter whose blocking opcodes double as a small **state machine**. The
level supplies placement, type, script index, path list and flags; the
executable supplies the programs.

The instruction-size model is the load-bearing claim, and it is checked four
ways that could each have failed independently: contiguity of the 40 bodies,
zero misalignment on linear decode, all branch targets on boundaries, and an
external entry point from `0x004372A8` landing on a decoded boundary.

Honesty about novelty, corrected at every audit. **Nine** artifacts in the export
directory reference the pool base — not the three the first two drafts claimed,
and not the eight the third listed, which named a file containing no occurrence
of the address and omitted two that do.
`M2-plant-request-origin-static-trace.md` already published the pool rebuild,
both 64s, the `0x700` copy, and the `LOAD: Type 35, CreatListRam.` string
itself, the last with runtime corroboration from retained hardware logs that
this offline census does not have; `M2-second-deferral-hard-truth-audit.md`
already published the pool extent and stride with the exact closing arithmetic
`0x0059B628 + 63 * 0x84 = 0x0059D6A4`. So the subsystem's **identity**, which
the first drafts called the headline new result, is prior art.

The third draft then claimed novelty by address — "no earlier export mentions
`0x0041E848`, `0x004C83F0`, `0x004C8758`, `0x0041C600` or `0x0041BC48`". The
third audit falsified that too. `ghidra-evidence.json`, an 8 MB generated
artifact committed in the same directory at the project's earliest baseline,
already contains a decompilation of `FUN_0041dc60` rendering the 26-way opcode
switch, the nine-way opcode-11 sub-switch, `&DAT_004c8754 + operand * 4`, the
`0x005C5860` indexing, the call through record `+0x7C`, and both extra
program-counter advances — plus an explicit `0041dcf9 -> 0041e848` data
reference and the symbols `PTR_DAT_004c83f0` and `PTR_DAT_004c8758`.

The address-based framing is therefore **withdrawn**. What remains genuinely
this packet's is narrower and is stated as such in export §0.0: the two byte
case tables `0x0041C600` and `0x0041BC48`, which appear in no artifact here
(a decompiler renders a `switch` without exposing its case-index table); and
the authored, validated model — per-opcode instruction sizes, the decoded
40-program listing, and the four structural validations — none of which a
decompiler dump contains, and which under [[Agent Operating Manual]] is the
difference between evidence and a stated claim. Sections 1, 7 and 8 of the
export are restatement and say so.

## Result

The coverage row **Enemies, actors and AI** is proposed to move Untouched →
Bounded with the anchors above. No milestone status changes and no runtime
claim is made.

**Event/scripting** is separately moved Untouched → Touched on an incidental
find: five `EVENT : Event >>>%s<<< ...` log strings at `0x004D823C`,
`0x004D8264`, `0x004D82A4`, `0x004D82CC` and `0x004D830C`, with `0x004D82CC`
pushed at `0x0042DC14`. That is the coverage map's own definition of Touched —
incidental observations, no model. No event code was read.

## Follow-up

The cheapest next step is still static: identify what the five modes do by
reading `0x0041E1A8` onward, then take one of the ten per-type `+0x7C`
handlers. That would say whether "state" here means a movement mode or a
broader behaviour class.

The cheapest *decisive* step is runtime and read-only, and it needs separate
authorization: on a level that passes the `0x005C5E88` gate, sample slot
`+0x70` for one active slot across several seconds and confirm it walks a
decoded program. That single receipt would move the row from a static model to
an observed one, and it would also discriminate `KU-068`.

New unknowns recorded: `KU-068` (does an actor slot's `+0x70` advance through
the decoded programs at runtime, and which levels build the pool at all) and
`KU-069` (the reachability and consequence of four unbounded table indexes in
this subsystem — the type byte at `0x0041C468`/`0x0041C476`, the script index
at `0x0041BD45`, opcode 13's sequence index at `0x0041E01A`, and opcodes 4/10's
record-type index at `0x0041DDD4`/`0x0041DEE1`).

Also left open by the audit and recorded rather than smoothed: the extent of
the `0x004C881F` boolean table is not established (§3.3), and the `+0x6E`
value `0x3E6` that gates the `0x0059D99E` decrement at `0x0041BA23` has no
known producer, since every per-type default is 1..8 (§8).

Discovered leads not pursued: `CREAT\CREAT00.BIN` at `0x004C7970` has no
reference of any kind — the 4-byte value `0x004C7970` occurs nowhere in the
image — and no `CREAT` directory exists in the retail PC tree.

## Audit history

Accepted at round 8; rejected by each of the seven fresh-context audits before
it. This section states one row of
facts per round and makes **no** global claim about whether findings landed —
three successive drafts asserted such a claim and each was falsified by the
next round.

| Round | Audit | Principal finding | Did that commit apply everything it declared? |
|---|---|---|---|
| 1 | [[EXP-20260816-173 - Independent creature census audit]] | register and attribution defects | Yes, as verified by round 2 |
| 2 | [[EXP-20260817-174 - Second independent creature census audit]] | under half of `0x0041DC60` read while making claims scoped to all of it; headline novelty was prior art in an uncited export | Yes, as verified by round 3 |
| 3 | [[EXP-20260817-175 - Third independent creature census audit]] | the corrected extent was still wrong (the only `ret` is not the end); a fourth `+0x70` writer and a bit-`0x20` test missing; the prior-art list named a file lacking the address and omitted two that have it; `ghidra-evidence.json` already decompiled the interpreter | Yes, as verified by round 4 |
| 4 | [[EXP-20260817-176 - Fourth independent creature census audit]] | the accounting layer — a wrong percentage, an unreproducible "thirteen sites", misattributed drafts, an understated Ghidra export, an incomplete mode-slot enumeration, a fourth record-index site | **No.** Round 5 found one defect and two minors declared applied that were not; that note's Correction section records it |
| 5 | [[EXP-20260817-177 - Fifth independent creature census audit]] | a correction declared applied had not landed; four counting and attribution defects | **No.** Round 7 found one minor — the 3,045→3,046 extent figure — applied only in the export; that note's Corrections section records it |
| 6 | [[EXP-20260817-178 - Sixth independent creature census audit]] | this section itself: it omitted round 5 and claimed all findings applied; a wrong round count in the coverage map's rule lead-in | Yes as edits — but the replacement text it introduced carried a new false completeness claim, which round 7 caught |
| 7 | [[EXP-20260817-179 - Seventh independent creature census audit]] | this table's predecessor asserted "one documented exception" when two rounds had unapplied findings; round 5's note was never amended | Yes, as verified by round 8 |
| 8 | [[EXP-20260817-180 - Eighth independent creature census audit]] | **ACCEPT**, zero defects. One new binary fact as a minor: an eighth mode-slot writer at `0x0041E2E9`, reachable only through `esp`-delta accounting | — |

The numeric analysis was reproduced in full by **every** auditor and **no
derived number in it has ever changed**. Each rejection concerned scope, the
Confirmed register, counting, or attribution — never the analysis.
