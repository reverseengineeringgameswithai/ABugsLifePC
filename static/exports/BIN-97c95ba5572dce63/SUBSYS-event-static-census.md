# PC event subsystem static census

> **Status: closed unaccepted, with a stated confidence limit.**
> See `DEC-20260817-138`.
>
> This document went through **six** independent hard-truth audits. Every one
> re-derived the model from the binary and found it sound — the table geometry,
> the record layout, the seven function extents, the two decoded records, and
> the disjointness from the creature scripts have now been independently
> confirmed six times. **Its conclusions can be cited normally.**
>
> Every one also found fresh defects in the surrounding detail: 12, 10, 16, 12,
> 15, 14. None ever touched a conclusion; they were miscited addresses,
> enumerations short by one or three, Confirmed/Inferred slips, and corrections
> that reached some carriers and not others. A seventh round would in all
> likelihood find more of the same.
>
> **So: trust the conclusions, re-derive the details.** Before relying on any
> individual address, offset, count or enumeration below — especially in a
> milestone-gating claim — check it against the binary. The audit history is
> recorded in `Vault/90-Sessions/2026-08-17 1130 - Claude - PC event subsystem
> census.md` and the six audit notes alongside it.
>
> This export is the **normative** statement of the packet; the Vault notes
> point to it rather than restate it, so corrections have one place to land.

## Scope and evidence boundary

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Work copy read: `work/copies/BUGS_PC-full-disc/bugs.exe` (hash re-verified
  before analysis).
- Tools: GNU objdump 2.46 (`-d -M intel`) and direct little-endian byte
  decoding of the same file.
- Offline only. No process was launched, no debugger attached, no target memory
  written, no `originals/` path opened, no PS1 source consulted, and no game
  asset was read.

Section-to-file mapping used throughout (from `objdump -h`):

| Section | VMA | Size | File offset |
|---|---|---|---|
| `.text` | `0x00401000` | `0x000BE765` | `0x000400` |
| `.rdata` | `0x004C0000` | `0x00000E88` | `0x0BEC00` |
| `.data` | `0x004C1000` | `0x0002C400` | `0x0BFC00` |

`.data`'s raw content ends at `0x004ED400`. Addresses between that and the next
section with file content (`.idata` at `0x00864000`) are `.bss`-class and are
named by address only. The lowest such address this document cites is
`0x00598290` — which §2.1 and §6 both record as lying *outside* this subsystem;
§2.1 also names `0x00597000` and `0x0059A000` purely as the bounds of a
discarded search window. No file bytes
are decoded at any address above `0x004ED400`.

This census claims **no** runtime behaviour. No callback is executed, no event
is observed registered, and no function reached from a callback is analysed.

## 0. Relation to earlier work

Grepped across **every** file in `static/exports/BIN-97c95ba5572dce63/`,
including the generated `ghidra-evidence.json`, and across the Vault.

**Prior art, authored:**

- `SUBSYS-creature-actor-static-census.md` §9 and
  [[EXP-20260816-172 - PC creature actor pool and behaviour VM census]]
  record the five `EVENT` log strings and that `0x004D82CC` is pushed at `0x0042DC14`, explicitly as an
  incidental find with "no event code read". That is the anchor the
  Event/scripting coverage row already carried.
- `SUBSYS-audio-static-census.md` has a section headed "Indirect dispatch
  record (`0x004D81E8`)" describing "a record of a count and three code
  pointers", and lays out `0x004D81E8`/`EC`/`F0`/`F4`/`F8` with the pointers
  `0x00401B04`, `0x004011D1`, `0x00401299` and the string `"DIRECTX"`.
  [[EXP-20260816-159 - PC audio subsystem static census]] words the same fact
  as "a count of 3 followed by thunk pointers `0x00401B04`, `0x004011D1` and
  `0x00401299` (to `0x0042BA60`, `0x0042BB30`, `0x0042BB50`), followed by the
  string `"DIRECTX"`", and both note that `0x0042BA60` has zero direct call
  sites. §4.1 below identifies what that record is and refines one field
  reading; **the offsets that census gives are exactly right**.

**Prior art, generated — and it covers more than the first draft of this
document credited.** `ghidra-evidence.json` carries full decompiled bodies for
three of the seven functions. It holds **six** relevant entries — a `FUN_`
entry and a `thunk_FUN_` entry for each of `0x0042D980`, `0x0042DA70` and
`0x0042DB10`.

Its `0x0042DB10` body already renders:

- the base and stride, as `&DAT_005982b0 + *param_1 * 0x3c`;
- the 15-dword copy, as `for (iVar2 = 0xf; ...)` over `undefined4`;
- **two** of the three code-pointer slots as calls, `(**(code **)(&DAT_005982b4
  + *param_1 * 0x3c))()` and the `&DAT_005982bc` equivalent — `&DAT_005982b8`
  appears in this body only as a zero-store, and is rendered as a call in
  `thunk_FUN_0042d980` instead;
- the in-use flag as `(&DAT_005982e4)[*param_1 * 0xf] = 1`;
- the name as `param_1 + 8`, passed to the log call;
- the buffer `&DAT_00598670` and its `0x20`-iteration zeroing;
- the field clears at `&DAT_005982e8`, `e0`, `b2`, `e2`, `b4`, `b8`, `bc`;
- and **four** of the five format strings by symbol — `0x004D823C` appears only
  in `FUN_0042da70`.

`thunk_FUN_0042d980` likewise renders `_DAT_005982ac = puVar1 + -2` and the
`0x10`-iteration bound.

So **the table's base, stride and 16-record bound, and the record layout
including its three callback slots, are prior art** — independently re-derived
here from instructions, but not first found here.

**The caller data is prior art too.** The three `thunk_FUN_` entries carry
populated `callers` lists:

| Entry | Address | `callers` |
|---|---|---|
| `thunk_FUN_0042d980` | `004013ac` | `0043dc5a`, `00405cb0` |
| `thunk_FUN_0042da70` | `00401c44` | `0043daeb`, `00405c54`, `00405a73` |
| `thunk_FUN_0042db10` | `004017b2` | `0043daf5`, `0043db10` |

That is **7 of the 9** reachers §2 lists, already thunk-resolved. The `FUN_`
entries' `callers` lists are empty; the **second** draft of this section looked
only at those and asserted the lists are empty *for all three functions it
carries*, which is **false** and over-credited this census's novelty. (The
first draft made no callers claim at all.) Corrected here.

It carries **two further relevant entries**, `FUN_004adea0` and
`thunk_FUN_004adea0` (at `0x00401CF8`), whose bodies render the whole of §2's
log-formatter derivation: the `[256]`-dword stack buffer, the
`FUN_004b0150(buf, fmt, &stack)` call, and `s_bugs_log_004e9264` passed to
`FUN_004b13e0` and `FUN_004b0730`, whose returned handle then goes to
`FUN_004b13a0` and `FUN_004b04e0`. **That reading is prior art too.**
`thunk_FUN_004adea0`'s `callers` list also already contains six of this
subsystem's eight log-call sites — all but `0x0042DCE5` and `0x0042DD46`, which
sit in a function it has no entry for.

Three successive drafts of this section under-credited this file in three
different ways. This is the third correction on the same axis.

`ghidra-evidence.json` has **no entry at all** for `0x0042D950`, `0x0042D9D0`,
`0x0042DA00` or `0x0042DCA0`.

**As of the parent commit `4e0157f^`, no authored Vault note or markdown export
mentioned any of** (re-checked at that commit, all fifteen returning zero hits
— they of course appear in this tree now): `0x0042D950`, `0x0042D980`,
`0x0042D9D0`, `0x0042DA00`, `0x0042DA70`, `0x0042DB10`, `0x0042DCA0`,
`0x005982B0`, `0x005982AC`, `0x00598670`, `0x004D81A8`, `0x0043DAF5`,
`0x0043DB10`, `0x00401CF8` or `0x004ADEA0`.

What is new here, against **both** authored and generated prior art:

- the two reachers ghidra's lists do **not** carry — `0x004AE863` (call) and
  `0x004121A1` (tail `jmp`) — and the finding that four of the seven entry
  points are unreachable, for which ghidra has no entry at all;
- the four remaining functions' extents and bodies;
- the two static records decoded from file bytes, and the two registration
  sites;
- the demonstration that this machinery is disjoint from the creature script
  VM;
- the cross-link that closes the audio census's missing-caller question (§4.1);
- the negative results: `0x005982AC` is never read, the id is never
  bounds-checked, and `+0x00`/`+0x10` survive every clear.

## 1. The event table

Every access is a fixed-address or `id`-scaled reference; there is no pointer
indirection to the table itself.

`0x0042DB10` copies a whole record into place:

```text
42dbbe: 0f bf 03          movsx eax,WORD PTR [ebx]      ; id from the source
42dbc1: b9 0f 00 00 00    mov   ecx,0xf                 ; 15 dwords = 0x3C
42dbc6: 8b f3             mov   esi,ebx
42dbc8: 8d 04 40          lea   eax,[eax+eax*2]
42dbcb: 8d 04 80          lea   eax,[eax+eax*4]         ; eax = id * 15
42dbce: 8d 3c 85 b0 82 59 00  lea edi,[eax*4+0x5982b0]  ; base + id * 0x3C
42dbd5: f3 a5             rep movs DWORD PTR es:[edi],DWORD PTR ds:[esi]
```

So the **base is `0x005982B0`** and the **stride is `0x3C`** (60 bytes). The
destroy pass `0x0042DA70` and the dispatch pass `0x0042D980` both iterate
**16** records (`mov ebp,0x10` / `mov edi,0x10`), so the table is `[0x005982B0,
0x00598670)` — `16 * 0x3C = 0x3C0`, and `0x005982B0 + 0x3C0 = 0x00598670`.

`0x00598670` is a buffer whose **first 128 bytes are zeroed** (`mov ecx,0x20` +
`rep stos` of 32 dwords). Its own extent is not given by any instruction — 128
bytes is the width of the write, not a known object size. The table ends
exactly where that buffer begins.

It is **not** the log formatter's output buffer. `0x00401CF8` jumps to
`0x004ADEA0`, which formats into a `0x400`-byte *stack* local (`sub esp,0x400`
at `0x004ADEA5`; `mov ecx,0x100` / `rep stos` on `[esp+0x8]` at
`0x004ADEB1`-`0x004ADEC0`) and passes it with the format string and a varargs
pointer to `0x004B0150` — a `vsprintf`-shaped call — before writing the result
out through `0x004B0730`/`0x004B13A0`/`0x004B04E0`. `0x00598670` is *pushed as
an argument* by the caller, so it is a **vararg**: at the four sites whose
format string has two `%s`, it supplies the second one, and the bytes it points
at are zero at the moment of the call.

Four of the eight log calls in this subsystem clear it first, and they are
exactly the two-`%s` sites: the clear at `0x0042DA9A`, `0x0042DB4B`,
`0x0042DC0E` and `0x0042DCD5` precedes the call at `0x0042DAA5`, `0x0042DB56`,
`0x0042DC19` and `0x0042DCE5`. The other four calls — `0x0042DAD3`,
`0x0042DBB6`, `0x0042DC3A` and `0x0042DD46` — have one `%s` and no clear.

### 1.1 Record layout

Derived from the `id`-scaled absolute addresses each field is accessed by, then
cross-checked against the destroy pass, which walks the same records backwards
with `esi` on `+0x34`. The cross-check is **not fully independent** — its
origin is imported from the first derivation — and it does not reach `+0x00`.
It is, however, the only place that reaches the **table** record's name:
`+0x10` has no `id`-scaled absolute form at all, and the other accesses to a
`+0x10` are to the *caller's* record. See the limits stated below the table:

| Offset | Size | Accessed as | Role shown by the instructions |
|---|---|---|---|
| `+0x00` | word | `0x005982B0` | id; `movsx`-read from the source record and used as the table index |
| `+0x02` | word | `0x005982B2` | zeroed on clear/delete; no other access found |
| `+0x04` | dword | `0x005982B4` | **called** at `0x0042DC2A`; the log call four instructions earlier at `0x0042DC19` passes `"create function %s called"` — the executable's own word, so **create** is the binary's name, not this census's |
| `+0x08` | dword | `0x005982B8` | **called** at `0x0042D9A5` by the dispatch pass `0x0042D980`, and tail-jumped at `0x0042D9E6` by the run-one function `0x0042D9D0` — two different functions. **Unnamed**: unlike `+0x04` and `+0x0C` it has no log string, so nothing in the binary describes it. Called `the +0x08 callback` throughout |
| `+0x0C` | dword | `0x005982BC` | **called** at `0x0042DB67`, `0x0042DCF6` and `0x0042DAAD`, each a few instructions after a log call passing `"destroy function %s called"` (`0x0042DB56`, `0x0042DCE5`, `0x0042DAA5`) — again the binary's own word, so **destroy** is confirmed, not interpreted |
| `+0x10` | 32 bytes (inferred) | never by absolute address — only from a record pointer. All eight producers: `lea [esi-0x24]` at `0x0042DA9C` and `0x0042DABD` (the **table** record); and from the **caller's** record `lea [ebx+0x10]` at `0x0042DB4D`, `0x0042DB71` and `0x0042DC10`, `add ebx,0x10` at `0x0042DC31`, `lea [esi+0x10]` at `0x0042DCD7`, and `add esi,0x10` at `0x0042DD01` | name. **Unlike every other row this one has no `id`-scaled absolute form**: `0x005982C0` occurs zero times in the whole file, so `+0x10` has one derivation, not two. Passed as a `%s` at all 8 log calls, but only 2 of them (`0x0042DAA5`, `0x0042DAD3`, in the destroy-all pass) take it from the *table* record; the other 6 pass the caller's. No instruction gives the width: bounded below by the string starting here and above by the next accessed field at `+0x30`, so **32 is inference from adjacency, not a decoded field width** |
| `+0x30` | word | `0x005982E0` | zeroed on clear/delete; no other access found |
| `+0x32` | word | `0x005982E2` | zeroed on clear/delete; no other access found |
| `+0x34` | dword | `0x005982E4` | in-use flag: set to `1` at `0x0042DBE0`; tested at `0x0042DB26`, `0x0042DCB4`, `0x0042D992`, `0x0042D9D4` and `0x0042DA80`; zeroed at `0x0042DA10`, `0x0042DAB0`, `0x0042DB83` and `0x0042DD13` |
| `+0x38` | dword | `0x005982E8` | zeroed on clear/delete; no other access found |

The destroy pass's cross-check: `esi` starts at `0x00598668`, which is
`0x005982B0 + 15 * 0x3C + 0x34` — record 15's flag — and steps by `-0x3C`.
Under that origin its **nine** distinct record-relative operands resolve to
`[esi] = +0x34`, `[esi-0x28] = +0x0C`, `[esi-0x24] = +0x10`, `[esi-0x30] =
+0x04`, `[esi-0x2C] = +0x08`, `[esi-0x04] = +0x30`, `[esi-0x32] = +0x02`,
`[esi-0x02] = +0x32` (`mov WORD PTR [esi-0x2],bx` at `0x0042DAC0`) and
`[esi+0x04] = +0x38` — every one consistent with the table above, derived from
a completely different addressing form.

Two limits on how independent this cross-check is. It reaches nine of the ten
fields: `+0x00` is never touched by this pass (see §3). And the origin
`0x00598668` can only be placed on `+0x34` by importing the base, stride and
flag offset from the first derivation — so it confirms the *relative* layout
against a second addressing form, not the anchor.

`0x005982AC` — four bytes below the table — is written with the current record
pointer at `0x0042D99A` (three instructions before `call eax` at `0x0042D9A5`,
in the dispatch pass) and at `0x0042D9DA` (before `jmp eax` at `0x0042D9E6`, in
the run-one function — a tail jump, not a call). **Nothing in the file reads
it.** Both sites are `a3` (`mov ds:imm32,eax`) stores, and a whole-file 4-byte little-endian scan for
`0x005982AC` returns exactly those two occurrences and no others. Its purpose
is therefore unestablished; the "current record" reading is what the two stores
suggest, not something a reader confirms.

### 1.2 The index is not bounds-checked

The three `id`-addressed entry points all take the id as a **signed** word and
scale it without any range test: `movsx eax,WORD PTR [esp+0x4]` at
`0x0042DA00`, `movsx eax,WORD PTR [ebx]` at `0x0042DB18`, and `movsx eax,WORD
PTR [esi]` at `0x0042DCA8`, each followed by the `*3`/`*5`/`shl 2` scaling
sequence and then by a load or store at `[eax+0x5982xx]`. The scaling is not
always contiguous with the read: at `0x0042DB18` two `push`es intervene
(`0x0042DB1B`, `0x0042DB1C`) and at `0x0042DA00` an `xor` does (`0x0042DA05`).
(`0x0042DB16`'s `xor ebp,ebp` comes *before* the read, not between it and the
scaling.) But **no `cmp` against 16, or against anything, appears between the
read and the first access in any of the three**.

Only the two iterating passes are bounded, by their own `mov ebp,0x10` / `mov
edi,0x10` counters. So a record carrying an id outside `0..15` addresses memory
outside `[0x005982B0, 0x00598670)`, in either direction. Whether that can
happen depends on where records come from, which this census does not establish
— the two static records carry ids 2 and 3.

## 2. The seven functions

Each extent below was established from its single `ret` and following padding,
and every direct branch inside each range was enumerated: **the only outbound
*direct* branch target from any of them is `0x00401CF8`** (→ `0x004ADEA0`); the
six callback transfers are indirect.

`0x004ADEA0` pushes `0x004E9264` and `0x004E9260` at `0x004ADEFB`-`0x004ADF05`
(and `0x004E9264` again at `0x004ADEE5`, that third push guarded by
`0x004E9170` — see below). Those decode from file offsets `0x0E7E64` and
`0x0E7E60` as **`"bugs.log"`** and **`"at"`** — bytes, not interpretation. It
then calls `0x004B0730` with them and passes the returned value to `0x004B13A0`
(with the formatted buffer) and `0x004B04E0`.

One of those four is decisive. `0x004B13E0`-`0x004B140C` (17 instructions, two
`ret`s) passes its argument to `call DWORD PTR ds:0x864670` at `0x004B13E5`,
where IAT slot `0x00864670` resolves to **`KERNEL32.dll!DeleteFileA`**; on
failure it calls `GetLastError` (IAT `0x008645DC`) at `0x004B13EF`, passes the
code to `0x004B4B50` and returns `-1`, otherwise `0`. The call reached with
`"bugs.log"` is therefore a **file deletion, by a named Win32 import**.

It is also guarded and one-shot:

```text
4adedb: 66 83 3d 70 91 4e 00 00  cmp  WORD PTR ds:0x4e9170,0x0
4adee3: 74 16                    je   0x4adefb
4adee5: 68 64 92 4e 00           push 0x4e9264            ; "bugs.log"
4adeea: 66 c7 05 70 91 4e 00 00 00  mov WORD PTR ds:0x4e9170,0x0
4adef3: e8 e8 34 00 00           call 0x4b13e0            ; DeleteFileA
```

`0x004E9170` holds `1` in the image (file `0x0E7D70`), so the first call
through this path deletes any existing `bugs.log` and clears the flag; later
calls skip straight to the `"at"` open. That is truncate-on-first-write, append
thereafter.

What that makes **Confirmed** is narrower than "writes a log file":
`0x004ADEA0` **deletes a file named `bugs.log`**, once, and then passes that
filename with the mode string `"at"` to `0x004B0730`. Both halves are a named
import and decoded bytes.

That it *writes* to the file remains **Inferred**: the write would run through
`0x004B0730`, `0x004B13A0` and `0x004B04E0`, whose fopen/fprintf/fclose shape is
a strong fit — an `"at"` mode string, a returned value used as a handle, a
formatted buffer — but none of the three is an import and none is decoded in
this census. (`ghidra-evidence.json` does decompile all three; this census did
not adopt those bodies as evidence.) Nothing here depends on the inference.

Its whole body is also **gated**: `mov eax,ds:0x8620ac` / `test eax,eax` / `je
0x004ADF2A` at `0x004ADEA0`-`0x004ADEAF` skips everything when that global is
zero. Nothing in this census establishes its value.

`ghidra-evidence.json` carries this function under `FUN_004adea0` /
`thunk_FUN_004adea0` and renders the same structure, so the reading is prior
art as well (§0).

| Function | Extent | File | Role | Reached from |
|---|---|---|---|---|
| `0x0042D950` | `0x0042D950`-`0x0042D960` | `0x02CD50` | zeroes 128 bytes at `0x00598670` (the width of the write; the buffer's own extent is not given) | thunk `0x0040169F`, which has **no callers**; the same `rep stos` is inlined at the four two-`%s` log sites instead |
| `0x0042D980` | `0x0042D980`-`0x0042D9B3` | `0x02CD80` | dispatch pass: for each of 16 records with `+0x34 == 1`, store the record pointer to `0x005982AC` and call `+0x08` if non-null; returns `ax = 1` | thunk `0x004013AC`, from `0x00405CB0` and `0x0043DC5A` |
| `0x0042D9D0` | `0x0042D9D0`-`0x0042D9E8` | `0x02CDD0` | run one record by pointer: if `+0x34 == 1`, store to `0x005982AC` and tail-`jmp` to `+0x08` | thunk `0x0040179E`, which has **no callers** |
| `0x0042DA00` | `0x0042DA00`-`0x0042DA43` | `0x02CE00` | clear slot by id: zero every field except the id at `+0x00` and the name at `+0x10` | thunk `0x00401217`, which has **no callers** |
| `0x0042DA70` | `0x0042DA70`-`0x0042DAE5` | `0x02CE70` | destroy all: for each of 16 records with `+0x34 != 0`, call `+0x0C` if non-null, zero every field except the id at `+0x00` and the name at `+0x10`, then log | thunk `0x00401C44`, from `0x00405A73`, `0x00405C54`, `0x0043DAEB`, `0x004AE863` (calls) and `0x004121A1` (tail `jmp`) |
| `0x0042DB10` | `0x0042DB10`-`0x0042DC46` | `0x02CF10` | register: destroy any existing occupant of the slot, copy the 60-byte record in, set `+0x34 = 1`, call `+0x04` if non-null | thunk `0x004017B2`, from `0x0043DAF5` and `0x0043DB10` |
| `0x0042DCA0` | `0x0042DCA0`-`0x0042DD50` | `0x02D0A0` | delete one by record pointer: call `+0x0C` if non-null, zero every field except the id at `+0x00` and the name at `+0x10`, then log | thunk `0x00401140`, which has **no callers** |

Four of the seven have no reachable caller, and all four fail the same test in
the same way. Each is reached only through a thunk in the `0x00401000` table —
`0x0040169F`, `0x0040179E`, `0x00401217`, `0x00401140` — and for each of the
four pairs both directions were checked: no `call` or `jmp` anywhere in the
image targets the thunk, and neither the thunk address nor the function address
occurs anywhere in the file as a 4-byte little-endian value. All eight scans
return zero occurrences.

This is a completeness claim over the mechanisms named, not over all
mechanisms; §6's last item states what it can still miss.

### 2.1 Absolute references to the table

A narrower claim than the section heading of earlier drafts suggested, stated
plainly because three successive drafts over-reached here.

**Method.** Every *absolute* 32-bit reference in a PE image carries a base
relocation, so decoding `.reloc` enumerates that form completely. `.reloc`
(file `0x0EF000`, size `0x11800`) was decoded and all **26,713** type-3
(`HIGHLOW`) entries dereferenced.

**Result.** Exactly **47** point into `[0x005982A0, 0x005986F0)` — the table
plus its buffer — and all 47 lie inside the seven function extents of §2. A
whole-file little-endian scan of the same range returns the same 47 by a
different method.

**What this does and does not establish.** It establishes that no instruction
outside those seven functions holds an *absolute* reference whose value lands
in the range. It does **not** establish that nothing else reaches the table:

- a pointer computed into a register at runtime carries no relocation at the
  point of use (§6's last item);
- a base relocated to some address outside the range and then indexed into it —
  `[base + reg]`, the form this subsystem itself uses — has a relocation value
  outside the range and so is not counted. The image has 6,473 distinct
  relocated values, 4,673 below `0x005982A0` and 1,788 at or above
  `0x005986F0`, and `[base + reg]` has no distance bound, so no window sweep
  closes this. An earlier draft claimed a `[0x00597000, 0x0059A000)` sweep did;
  it does not, and that claim is withdrawn.

So this is a **strong negative on one addressing form**, not a proof of
isolation.

**The range excludes `0x00598290`**, deliberately: that address does have five
external references — `0x00405C0C` and `0x00405C82` read it, `0x0043DF65`,
`0x0043DFAF` and `0x004AE8F7` write it — and §6 records it as outside this
subsystem. Widening the range to include it gives 52 rather than 47.

Provenance: the second-round audit found the 47/all-inside result; the third
corrected a first version that mixed the two ranges' numbers; the fifth
withdrew the closure claim above.

`0x0042DD90` is a bare `ret` after `int3` padding and is a separate stub; it is
not treated as part of this subsystem.

## 3. Registration and lifecycle

`0x0042DB10`, in order:

1. `cmp [+0x34], 0` at `0x0042DB26` — if the slot is unused, jump straight to
   the copy at `0x0042DBBE`;
2. otherwise, if `[+0x0C]` is non-null, log `0x004D8264` ("destroy function %s
   called") and `call [+0x0C]` at `0x0042DB67`;
3. zero `+0x34`, `+0x38`, `+0x30`, `+0x02`, `+0x32`, `+0x04`, `+0x08`, `+0x0C`
   — every field except the **id** at `+0x00` and the **name** at `+0x10`, both
   of which survive the clear — and *then* log `0x004D830C` ("deleted"). The
   order is zero-then-log at all three sites that do both: the last store is at
   `0x0042DBB0` / `0x0042DAD0` / `0x0042DD40` and the log call follows at
   `0x0042DBB6` / `0x0042DAD3` / `0x0042DD46`. The exception among the four
   clearing paths is `0x0042DA00`, which zeroes without logging.

   The name each of those three log calls prints is **not** generally the table
   record's. At `0x0042DBB6` it is `lea edx,[ebx+0x10]` (`0x0042DB71`;
   `0x0042DB6E` is the `movsx` immediately before it) and at `0x0042DD46` it is
   `add esi,0x10` / `push esi` (`0x0042DD01`, `0x0042DD07`) — both the
   **caller's** record, which no clear touches. Only `0x0042DAD3` reads the
   table record, via `lea ecx,[esi-0x24]` at `0x0042DABD`, and only there does
   the surviving name matter. None of the four clearing paths writes
   `0x005982B0` or the name block;
4. `rep movs` 15 dwords from the caller's record into `base + id * 0x3C`;
5. `mov [+0x34], 1` at `0x0042DBE0`;
6. if `[+0x04]` is non-null, log `0x004D82CC` ("create function %s called") and
   `call [+0x04]` at `0x0042DC2A`;
7. log `0x004D82A4` ("added").

The five log strings map to the lifecycle exactly:

| String | Address | File | Emitted by |
|---|---|---|---|
| `EVENT : Event >>>%s<<< deleted.\n` | `0x004D823C` | `0x0D6E3C` | `0x0042DACB`, in the destroy-all pass |
| `EVENT : Event >>>%s<<< destroy function %s called.\n` | `0x004D8264` | `0x0D6E64` | `0x0042DAA0`, `0x0042DB51`, `0x0042DCE0` |
| `EVENT : Event >>>%s<<< added.\n\n` | `0x004D82A4` | `0x0D6EA4` | `0x0042DC35` |
| `EVENT : Event >>>%s<<< create function %s called.\n` | `0x004D82CC` | `0x0D6ECC` | `0x0042DC14` |
| `EVENT : Event >>>%s<<< deleted.\n\n` | `0x004D830C` | `0x0D6F0C` | `0x0042DB78`, `0x0042DD08` |

Each of the five is referenced exactly at the sites listed and nowhere else.

## 4. The two static registration sites

The register thunk `0x004017B2` has exactly two call sites, adjacent in one
function:

```text
43daeb: e8 54 41 fc ff    call 0x401c44        ; destroy all
43daf0: 68 a8 81 4d 00    push 0x4d81a8
43daf5: e8 b8 3c fc ff    call 0x4017b2        ; register
43dafa: 83 c4 04          add  esp,0x4
43dafd: 66 39 2d f0 f7 59 00  cmp WORD PTR ds:0x59f7f0,bp
43db04: 75 05             jne  0x43db0b
43db06: e8 25 41 fc ff    call 0x401c30
43db0b: 68 e8 81 4d 00    push 0x4d81e8
43db10: e8 9d 3c fc ff    call 0x4017b2        ; register
```

Both arguments are static `.data` records. Decoded from the file bytes under
the §1.1 layout:

| Field | `0x004D81A8` (file `0x0D6DA8`) | `0x004D81E8` (file `0x0D6DE8`) |
|---|---|---|
| `+0x00` id | `2` | `3` |
| `+0x02` | `0` | `0` |
| `+0x04` create | `0x00401A91` → `0x004AE580` | `0x00401B04` → `0x0042BA60` |
| `+0x08` (unnamed) | `0x00401AA5` → `0x004AE780` | `0x004011D1` → `0x0042BB30` |
| `+0x0C` destroy | `0x004017DA` → `0x004AE810` | `0x00401299` → `0x0042BB50` |
| `+0x10` name | `"WINDOWS"` | `"DIRECTX"` |
| `+0x30`..`+0x3B` | all zero | all zero |

So there are **two** static registration call sites, passing records whose ids
select slots 2 and 3 of the 16-slot table, and no other call site of the
register thunk exists.

Both calls are unconditional *within* this function: the `cmp`/`jne` at
`0x0043DAFD`-`0x0043DB04` skips only the intervening `call 0x401c30`, not the
registration at `0x0043DB0B`. But whether either ever executes is **not**
established — the enclosing function is unanalysed and its own callers were not
traced (§6). "Registers two events" would be a runtime claim; what is shown
here is two call sites and the records they name.

### 4.1 Refinement of a prior-art reading

`SUBSYS-audio-static-census.md` calls `0x004D81E8` "a record of a count and
three code pointers", and `EXP-20260816-159` words it as "a count of 3". Its
byte layout — `0x004D81E8`, then pointers at `EC`, `F0`, `F4`, then the name at
`F8` — is **exactly right** and matches §1.1 offset for offset.

The one refinement is the leading field. Under §1.1 the `3` is the **event
id**: a word, read with `movsx` at `0x0042DB18` and scaled by `0x3C` to select
the slot, not a count of the pointers that follow. (The two readings are
byte-compatible: `+0x02` is zero, so a dword read yields `3` either way.) The
three pointers and their targets are as that census recorded; this census adds
only where each is called from: `+0x04` at the create site, `+0x0C` at the
destroy sites, and `+0x08` from the dispatch pass `0x0042D980` and the run-one
function `0x0042D9D0` — the last with no name,
because no log string describes it.

This also supplies the missing caller that census noted: it observed that
`0x0042BA60` has **zero direct call sites** and is reached only through this
`.data` record. `0x0042BA60` is this record's `+0x04` field, and `+0x04` is the
target of the `call` at `0x0042DC2A` inside the register function. So the path
by which `0x0042BA60` would be entered is: something calls `0x004017B2` with
`0x004D81E8`, and the register function calls the record's `+0x04`. That is a
static path, not an observation that it runs — but it is why a direct-call
census could not find an entry point for `0x0042BA60`: there is no direct call
to find.

## 5. Is this the creature script machinery?

**No.** The two are disjoint by construction and by address.

| | Creature scripts | Events |
|---|---|---|
| Dispatch | word-code interpreter `0x0041DC60`, 26-opcode table `0x0041E848` | native function pointers in the record |
| Program store | 40 programs at `[0x004C7D00, 0x004C83F0)` | none — the record holds code pointers |
| Instances | 64-slot pool `[0x0059B628, 0x0059D728)`, stride `0x84` | 16-slot table `[0x005982B0, 0x00598670)`, stride `0x3C` |
| Source | `LEVEL.RAW` type-`0x23` records | static `.data` records |
| Per-instance state | program counter `+0x70`, wait counter `+0x60` | in-use flag `+0x34`; plus `+0x02`, `+0x30`, `+0x32`, `+0x38`, which are copied in by the `rep movs` and zeroed by every clearing path but never otherwise read (§6) — no advancing state of any kind |

Checked in both directions over the two code ranges: none of `0x0041DC60`,
`0x004C83F0`, `0x0041E848`, `0x0059B628` or `0x004C8758` is referenced anywhere
in `0x0042D950`-`0x0042DD90`, and none of `0x005982B0`, `0x005982B4`,
`0x005982AC` or `0x00598670` is referenced anywhere in
`0x0041DC60`-`0x0041E845`.

**Nor is this an event VM or a data-driven trigger stream.** There is no
opcode, no instruction stream, and no interpreter: an event is a name plus
three native code pointers, and the only data involved is the 60-byte record
itself. The word "event" here names a *subsystem lifecycle slot*, not a
gameplay trigger.

## 6. What this census does not establish

- Any runtime fact. Nothing was launched; no event was observed registered,
  dispatched or destroyed.
- What the six callback targets do. `0x004AE580`, `0x004AE780`, `0x004AE810`,
  `0x0042BA60`, `0x0042BB30` and `0x0042BB50` are named only as the pointers
  the records carry. `0x0042BA60`'s role is prior art from the audio census.
- Whether anything registers an event outside the two static sites, and
  therefore whether slots other than 2 and 3 are ever occupied.
- The meaning of `+0x02`, `+0x30`, `+0x32` and `+0x38`, which are only ever
  zeroed.
- What `+0x08` is for. It has no log string and no analysed callee, so it is
  left unnamed here rather than called an "update" hook.
- The width of the name at `+0x10`. 32 bytes is inference from the next
  accessed field, not a decoded width.
- What `0x005982AC` is for. It is written twice and read nowhere in the file.
- The roles of the roles of `0x004B0730`, `0x004B13A0` and `0x004B04E0`, which
  `0x004ADEA0` calls after `DeleteFileA` and which **this census** does not
  decode (`ghidra-evidence.json` decompiles all three; those bodies were not
  adopted as evidence here); and what sets `0x008620AC`,
  the global gating `0x004ADEA0`'s whole body, or `0x004E9170`, which arms its
  one-shot delete and holds `1` in the image.
- Whether an id outside `0..15` can ever reach the three unchecked `id`-scaled
  entry points (§1.2), which requires knowing where records come from.
- The enclosing functions and callers of the **nine** sites that reach the live
  entry points: `0x00405CB0`, `0x0043DC5A`, `0x00405A73`, `0x00405C54`,
  `0x0043DAEB`, `0x004AE863`, `0x004121A1`, `0x0043DAF5` and `0x0043DB10`; and
  the meaning of `0x0059F7F0` in the registration sequence.
- `0x00598290`, which is written and read outside this subsystem and is not
  part of the table.
- Whether register-indirect dispatch reaches any of these functions from
  callers this census did not find. Call instructions, both thunk directions
  and whole-file absolute-value scans were used; that combination is what the
  input census's own `GetAsyncKeyState` finding showed can still miss a
  computed call.
