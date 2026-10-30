# PC creature/actor pool and behaviour VM static census

## Scope and evidence boundary

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Work copy read: `work/copies/BUGS_PC-full-disc/bugs.exe` (hash re-verified
  before analysis).
- Tools: GNU objdump 2.46 (`-d -M intel`), `rabin2` 5.9.8 for strings, and
  direct little-endian byte decoding of the same file.
- Offline only. No process was launched, no debugger attached, no target
  memory written, no `originals/` path opened, no PS1 source consulted, and no
  game asset was read except the metadata-level directory listing of
  `work/copies/BUGS_PC-full-disc/PC/BUGS/CD`.

Section-to-file mapping used throughout (from `objdump -h`):

| Section | VMA | Size | File offset |
|---|---|---|---|
| `.text` | `0x00401000` | `0x000BE765` | `0x000400` |
| `.rdata` | `0x004C0000` | `0x00000E88` | `0x0BEC00` |
| `.data` | `0x004C1000` | `0x0002C400` | `0x0BFC00` |

`.data`'s raw content ends at `0x004ED400`; addresses above that have no file
content and are named by address only. The lowest such address this document
cites is `0x00599B20`.

This census claims **no** runtime behaviour, no per-type creature identity, no
render or collision linkage beyond the cited instructions, and no field
semantics beyond what an instruction directly performs.

## 0. Relation to earlier work

This subsystem is **not** untouched at the instruction level. Three successive
audits each had to widen this accounting; the list below is the third attempt
and the first that was produced by grepping every file in this directory
rather than the ones the author happened to have read.

**Nine** artifacts here reference the pool base `0x0059B628`: the markdown
exports `M2-plant-request-origin-static-trace.md`,
`M2-fixed-pool-index-producer-census.md`,
`M2-signed-selector-producer-provenance.md`,
`M2-plant-resource-static-trace.md`,
`M2-residual-fixed-pool-index-reader-disposition.md`,
`M2-independent-disposition-hard-truth-audit.md`,
`M2-deferral-hard-truth-audit.md`,
`M2-second-deferral-hard-truth-audit.md` — and the generated
`ghidra-evidence.json`. (The first two drafts listed only three exports. The **third** widened it to
eight, but named `M2-generic-resource-index-producer-census.md`, which contains
**no** occurrence of the address, and omitted
`M2-second-deferral-hard-truth-audit.md` and `ghidra-evidence.json`.)

Prior art that this census restates rather than establishes:

- **`M2-plant-request-origin-static-trace.md`** — that `0x004679A0` calls
  `0x0041C420`, "which rebuilds the **64** records rooted at `0x0059B628`";
  the `0x0041C424`-`0x0041C430` clear of `0x2100` bytes; that the builder
  "walks **64** source records at a `0x1C`-byte stride and 64 destination
  records at a `0x84`-byte stride"; the `0x0046574D`-`0x0046576A` copy of
  `0x700` bytes into `0x00599EB0`; the 64-dword clear of `0x005C5860` at
  `0x0046720E`; and the string **`LOAD: Type 35, CreatListRam.`** itself,
  observed in retained Training and Level 01 hardware logs — i.e. with runtime
  corroboration this offline census does not have.
- **`M2-second-deferral-hard-truth-audit.md`** — §1.1's headline arithmetic
  verbatim: "The 64-record pool is `[0x0059B628,0x0059D728)` with stride
  `0x84`" and `0x0059B628 + 63 * 0x84 = 0x0059D6A4`. It also already records
  `+0x5C` as a flags field via `0x00431804` testing slot 25's `+0x5C` at
  `0x0059C368`.
- **`M2-fixed-pool-index-producer-census.md`** — the pool extent and stride,
  the `0x0041C424` clear, the `0x0041BD10` source copier, the `0x0041BBBA`
  removal store, the `0x4000` active gate, the callback installed at record
  `+0x7C`, the `0x1C` source stride with the slot-2/slot-3 correspondence, and
  the mode-1/mode-2 classification of the calls into `0x0041B9F0` that §8
  restates. It also names `0x0041DC60` as a member of the active-record update
  closure.
- **`M2-generic-resource-index-producer-census.md`** — the update chain
  `0x004144C0 -> 0x0041EC40 -> 0x0041DC60 -> 0x00436AF0`, and the `0x00456640`
  and `0x00459620` calls that §7 restates. (It does not reference the pool
  base itself.)
- **`M2-signed-selector-producer-provenance.md`** — the
  `0x0041EDF8 -> 0x00467E60` edge.

**All of §1, §7 and §8 is restatement**, and carries no novelty claim.

### 0.0 The generated Ghidra export, and what novelty actually remains

The **third** draft (`3f0debd`) claimed that "no earlier export in this
directory mentions any of the addresses `0x0041E848`, `0x004C83F0`,
`0x004C8758`, `0x0041C600` or `0x0041BC48`". That is **false**,
and the correction is the most important thing in this section.

`ghidra-evidence.json` — an 8 MB machine-generated artifact committed in this
directory at the project's earliest baseline, and cited as evidence by many
Vault notes — already contains a decompilation of `FUN_0041dc60` — 18,101 characters in the
entry named for that address, and 18,205 in the `thunk_FUN_0041dc60` entry at
`0x004017F8`, which is the same body under the longer symbol. That decompilation renders the 26-way opcode switch, the
nine-way opcode-11 sub-switch with all nine targets,
`&DAT_004c8754 + operand * 4`, the `(&DAT_005c5860)[…]` indexing, the call
through record `+0x7C`, and — **three**, not two — extra program-counter
advances:

```text
piVar8[0x1c] = (int)psVar20;          ; the fetch-loop store, 0x0041E147
piVar8[0x1c] = (int)(psVar20 + 1);    ; +2,  0x0041E1EB
piVar8[0x1c] = piVar8[0x1c] + 6;      ; +6,  0x0041E2E1
if (2 < param_3) { … piVar8[0x1c] = piVar8[0x1c] + 2; }   ; +2, 0x0041E7FE
```

The last of those is the writer the third audit found missing from §5.1 and
which this export presented as that audit's discovery: it was already sitting
in the generated artifact, guard and all. The **fourth** draft (`1c499bf`),
which introduced this section, said "both extra program-counter advances" —
understating the artifact in the direction that flattered this packet. It also carries an explicit
`{"from":"0041dcf9","to":"0041e848","type":"DATA"}` reference and the symbols
`PTR_DAT_004c83f0` and `PTR_DAT_004c8758`.

So the honest statement of novelty is **not** about addresses, and this export
withdraws that framing. Two things remain genuinely this packet's:

- **the two byte case tables** `0x0041C600` and `0x0041BC48`, which are the
  only two of the five addresses that appear in no artifact here, generated or
  authored — decompiler output renders a `switch` without exposing the case
  index table it is built from; and
- **the authored, validated model**: per-opcode instruction sizes, the decoded
  40-program listing, and the four independent structural validations in §6.
  A decompiler dump contains none of those, and per
  [[Agent Operating Manual]] decompiler output is evidence, not a claim.

That is a much narrower contribution than the first two drafts asserted. The
generalisable lesson is in [[Subsystem Coverage Map]]: `ghidra-evidence.json`
is generated, unreviewed, enormous, and almost never grepped — and it can
contain a whole subsystem.

### 0.1 How much of the interpreter this census read

Function `0x0041DC60`'s only `ret` is at `0x0041E7D3`, but that is **not** its
end. The block `0x0041E7D4`-`0x0041E845` is entered from inside the function
by `jne 0x41e7d4` at `0x0041E6CD` and `jge 0x41e7d4` at `0x0041E6D8`, shares
the same `esi`/`edi`/`ebp` frame, and returns into the function with
`jmp 0x41e6e6` at `0x0041E841`; `mov edi,edi` padding at `0x0041E846` then
precedes the dispatch table at `0x0041E848`. The code extent is therefore
**`0x0041DC60`-`0x0041E845`**.

Three drafts got this wrong, in two ways. Drafts 1-2 read only to
`0x0041E1A8` — **1,352 bytes** (half-open, `0x0041E1A8 - 0x0041DC60`) of the
extent's **3,046** (inclusive, `[0x0041DC60, 0x0041E845]`), **about 44%** —
while making scoped completeness
statements over the whole function. Draft 3 asserted `0x0041E7D3` as the end
and, sweeping only to there, missed a fourth program-counter writer at
`0x0041E7FE`. The share itself was then quoted wrongly twice more: draft 3 said
"45%" against the superseded extent, and draft 4 "under 40%", which no
candidate endpoint of this function yields (44.4% at `0x0041E845`, 46.1% at the
superseded `0x0041E7D3`). Byte counts are stated instead.

This draft records, over the full `0x0041DC60`-`0x0041E845`: every `+0x5C`
access (§2.2.1), every `+0x70` writer (§5.1), the `call eax` through `+0x7C`
at `0x0041E7C7` (§5.5), and the record fields touched (§2.2). What the region
past `0x0041E1A8` actually *computes* remains **unanalysed** and is listed in
§10 as such. It is referred to here as implementing the five "modes" because
that is the value §5.3's dispatch selects and this region reads; calling them
*movement* modes would exceed the evidence, and `EXP-20260816-172` correctly
registers what they do as Unknown.

## 1. The instance pool

### 1.1 Extent

`0x0041C424`-`0x0041C430` (file `0x01B824`-`0x01B830`):

```text
41c424: b9 40 08 00 00    mov ecx,0x840
41c429: 33 c0             xor eax,eax
41c42b: bf 28 b6 59 00    mov edi,0x59b628
41c430: f3 ab             rep stos DWORD PTR es:[edi],eax
```

`0x840` dwords = `0x2100` bytes at `0x0059B628`, so the pool is
`[0x0059B628, 0x0059D728)`.

The per-record stride is `0x84` and the record count is 64, proved twice
independently:

- the build loop increments the destination by `0x84` at `0x0041C58A` and ends
  on `cmp ebx,0x40 / jl` at `0x0041C594`-`0x0041C597`;
- the update loop increments by `0x84` at `0x0041ED4F` and ends on
  `cmp esi,0x59d792 / jl` at `0x0041ED55`, where `esi` is `record + 0x6A`, so
  the last base is `0x0059D6A4` and the exclusive end is `0x0059D728`.

`0x2100 / 0x84 = 64`, and `0x0059B628 + 63 * 0x84 = 0x0059D6A4`.

At least **four** sites reach a record by that index arithmetic
(`shl r,5 / add r,index / lea r,[r*4+0x59b628]`, i.e.
`index * 33 * 4 = index * 0x84`): `0x0043206B`, `0x004320AE`, `0x00432136`, and
`0x0041519B`, which uses `edx`/`ecx` instead of `ecx`/`eax` and then reads the
resulting record's `+0x5C` at `0x004151B0`. Earlier drafts said "**Two** consumers" while listing three
addresses (drafts 1-2) and then "**Three** sites" (drafts 3-4). No exhaustive
search for this pattern has been run, so "at least four" is the honest form.

This extent and stride agree with the earlier
`M2-fixed-pool-index-producer-census.md`, which reached the same pool from a
different direction (`0x0059B730` and `0x0059B7B4` as slots 2 and 3).

### 1.2 Source table and its level-data origin

`0x0046574D`-`0x0046576A` (file `0x064B4D`-`0x064B6A`), reached under
`cmp edi,0x23 / jne` at `0x00465748`:

```text
46574d: b9 c0 01 00 00    mov ecx,0x1c0
465752: 33 c0             xor eax,eax
465754: bf b0 9e 59 00    mov edi,0x599eb0
465759: f3 ab             rep stos DWORD PTR es:[edi],eax
46575b: 8d 45 04          lea eax,[ebp+0x4]
46575e: b9 c0 01 00 00    mov ecx,0x1c0
465763: 8b f0             mov esi,eax
465765: bf b0 9e 59 00    mov edi,0x599eb0
46576a: f3 a5             rep movs DWORD PTR es:[edi],DWORD PTR ds:[esi]
```

`0x1C0` dwords = `0x700` bytes, so the source table is
`[0x00599EB0, 0x0059A5B0)`. The build loop advances the source pointer by
`0x1C` at `0x0041C590`, and `0x700 / 0x1C = 64` — one source record per pool
slot.

Everything in the paragraph above, the explicit "64" included, was already
published — the stride and copy in `M2-fixed-pool-index-producer-census.md`
and both 64s in `M2-plant-request-origin-static-trace.md`. See §0.

Immediately after the copy, `0x0046576F`-`0x00465775` logs through the string
at `0x004DE2FC` (file `0x0DCEFC`) — which carries no conversion specifier,
though `0x0046576F` pushes an argument anyway:

```text
LOAD: Type 35, CreatListRam.\n
```

Type 35 decimal is the `0x23` record type tested at `0x00465748`. This is the
executable's own name for the packet: a **creature list** loaded to RAM. It is
first-party naming evidence, not an interpretation added here.

### 1.3 Build

`0x0041C420` (file `0x01B820`), reached only through thunk `0x00401AC3`, whose
single call site is `0x004679A0` (file `0x066DA0`). No `ret` occurs between
`0x00467971` and `0x004679A0`, so that call site is inside the level-load
entry `0x004671D0` already established by `EXP-20260816-155`/`KU-064`, and it
follows the `0x0044BB70` record walk called at `0x00467971`. The call is gated:
`test al,0x10 / jne 0x4679CA` at `0x0046799C` on a byte of `0x005C5E88`.

The builder:

1. clears the whole pool (§1.1);
2. clears `0x80` dwords at `0x00599CA8`, i.e. `[0x00599CA8, 0x00599EA8)`;
3. clears the active list head `0x0059D7E0`;
4. loops `ebx = 0..63` with source cursor `esi` at `source + 0x10` starting
   `0x00599EC0` and destination cursor `edi` at `record + 0x7C` starting
   `0x0059B6A4`;
5. skips a slot entirely when the source type byte is zero
   (`0x0041C458`-`0x0041C45D`);
6. stores the source pointer into record `+0x80` (`mov [edi+4],ecx` at
   `0x0041C490`);
7. applies the per-type setup switch of §3.1;
8. when source `+0x12` bit `0x20` is set, shifts source `+0x00`, `+0x04` and
   `+0x08` left 5 **in place** and writes an incrementing per-level counter
   into source `+0x19` (`0x0041C52A`-`0x0041C551`);
9. calls the per-record initializer through thunk `0x00401C99` at
   `0x0041C559`.

### 1.4 Unbounded type-byte index (original behaviour)

At `0x0041C463`-`0x0041C47D` the type byte is zero-tested only, then used
directly:

```text
41c463: 25 ff 00 00 00    and eax,0xff
41c468: 8a 88 1f 88 4c 00 mov cl,BYTE PTR [eax+0x4c881f]
...
41c476: 88 0c c5 a8 9c 59 00  mov BYTE PTR [eax*8+0x599ca8],cl
41c47d: eb 08                 jmp 0x41c487
41c47f: c6 04 c5 a8 9c 59 00 7f  mov BYTE PTR [eax*8+0x599ca8],0x7f
```

No upper bound is checked (`0x0041C463`-`0x0041C486`; the `jmp` at
`0x0041C47D` is what makes the two stores mutually exclusive). The cleared
region at `0x00599CA8` is `0x200` bytes,
so `type * 8` stays inside it only for `type <= 63`; `type = 65` writes exactly
`0x00599EB0`, the first byte of the source table copied in §1.2. The byte table
read at `0x004C881F` is likewise indexed by the raw byte with no bound.

This is a static property of the retail code under the stated arithmetic. **No
PC level file was parsed for this packet**, so nothing here claims that any
shipped `LEVEL.RAW` contains such a type byte.

Three sibling unbounded indexes exist in the same subsystem and are recorded
together with this one under `KU-069`:

- the initializer reads the 40-entry script pointer table with
  `mov edx,[edx*4+0x4c83f0]` at `0x0041BD45`, where `edx` is the raw source
  `+0x0D` byte — no bound check at all, so a byte of 40 or more yields a
  program counter read from beyond the table;
- VM opcode 13 reads the 28-entry frame-sequence table with
  `mov eax,[eax*4+0x4c8754]` at `0x0041E01A`, where `eax` is the
  sign-extended operand word — likewise unchecked (§6);
- VM opcodes 4 and 10 read the record-type pointer table `0x005C5860` with
  `mov reg,[ecx*4+0x5c5860]` at `0x0041DDD4` and `0x0041DEE1`, where `ecx` is
  the raw source `+0x0E`/`+0x0F` byte (range 0..255). The load-time clear at
  `0x00467207`-`0x00467215` zeroes 64 dwords there — the same clear `KU-064`
  already records, and already reported in
  `M2-plant-request-origin-static-trace.md` — so **64 is the bound of the
  zeroed region**, which is evidence for but not proof of the table's extent.
  On that reading a source byte of 64 or more indexes past it.

## 2. Record and source layouts

Field names below describe what an instruction does with the field. Fields
whose purpose is not shown by an instruction are left unnamed.

### 2.1 Source record, `0x1C` bytes

| Offset | Size | Evidence | Use |
|---|---|---|---|
| `+0x00` | dword | `0x0041BD26` | X; shifted left 5 into record `+0x04` |
| `+0x04` | dword | `0x0041BD2E` | Y; shifted left 5 into record `+0x08` |
| `+0x08` | dword | `0x0041BD37` | Z; shifted left 5 into record `+0x0C` |
| `+0x0C` | byte | `0x0041BD21` | type id → record `+0x00` |
| `+0x0D` | byte | `0x0041BD42` | index into the 40-entry script table `0x004C83F0` → record `+0x70` |
| `+0x0E`,`+0x0F` | byte | `0x0041DDCD`, `0x0041DEDD` | selector into the record-type pointer table `0x005C5860` (the same table whose entry 1 is the type-1 pointer `0x005C5864` of `EXP-20260816-153`); `+0x0F` also seeds record `+0x5E` at `0x0041DEC1` |
| `+0x10` | byte | `0x0041BD4F`; written per type at `0x0041C4A8`ff | → record `+0x6E` |
| `+0x11` | byte | `0x0041BD60` | → record `+0x62` |
| `+0x12` | word | `0x0041BD58` | → record `+0x5C` flags; bit `0x20` also gates the builder block at `0x0041C52A` |
| `+0x14` | word | `0x0041DC86`, `0x0041DCA7` | scalar shifted left 4; the multiplier used by VM opcode 3 |
| `+0x16` | word | `0x0041DC82`, `0x0041DC8D` | scalar shifted left 4, kept at `[esp+0x1c]`; consumed in the post-loop mode tail, **not** by opcode 3 |
| `+0x18`,`+0x1B` | byte | `0x0041DC96`, `0x0041E06D` | read by the VM; `+0x1B` written by opcode 15 |
| `+0x1A` | byte | `0x0041E46E` | read in the interpreter region past `0x0041E1A8`; purpose not analysed |
| `+0x19` | byte | written at `0x0041C54A`, read at `0x0041DC8A` | incrementing per-level counter assigned by the builder to bit-`0x20` records only |

Note on the bit-`0x20` records: the builder shifts source `+0x00`/`+0x04`/
`+0x08` left 5 in place at `0x0041C530`-`0x0041C54E`, and the initializer then
overwrites record `+0x04`/`+0x08`/`+0x0C` with the **unshifted** source values
at `0x0041BD76`-`0x0041BD84`. The net effect is a single shift, not a double
one, but both halves are recorded here because neither is obvious from the
other's site alone.

### 2.2 Pool record, `0x84` bytes

| Offset | Size | Evidence | Use |
|---|---|---|---|
| `+0x00` | dword | `0x0041BD24`, `0x0041BAF0`, `0x004372B7` | type id; `0` marks an unused slot; both type switches use domain 6..41; also indexes `0x005B18E0 + id*4` |
| `+0x04`/`+0x08`/`+0x0C` | dword | `0x0041BD2B`ff | X/Y/Z |
| `+0x1C`,`+0x24` | dword | `0x0041BAE7`, `0x0041BAF2` | written on release/reinit |
| `+0x28`/`+0x2C`/`+0x30` | dword | `0x0041BDCF`ff | copy of X/Y/Z at init; base for opcode 3 |
| `+0x34`/`+0x38`/`+0x3C` | dword | `0x0041BDD2`, `0x0041BDE0`, `0x0041BDE3` | copy of X/Y/Z at init; destination written by opcodes 3, 4 |
| `+0x40` | dword | ten stores across the five functions: `0x0041BB2A`, `0x0041BB60`, `0x0041BB7F`, `0x0041BBA2` (the §3.2 arms), `0x0041BDF8`, `0x0041BE34`, `0x0041E029`, and `0x0041E730`, `0x0041E785`, `0x0041E791` in the unanalysed interpreter region. `0x0041BB27` is the `shl` feeding the first, not a store | usually the first byte of the selected frame sequence shifted left 16, but the initializer zeroes it at `0x0041BDF8` and, for bit-`0x20` records, writes the raw source `+0x0D` script index at `0x0041BE34` |
| `+0x44` | dword | `0x0041BB10`ff, `0x0041E011` | small integer 0..3 set per type and by opcode 13 |
| `+0x48`,`+0x49` | byte | `0x0041BAEA`, `0x0041E0E0` | set to `0xC0` on reinit; written by opcode 22 |
| `+0x4A` | word | `0x0041BB21`ff, `0x0041EEA7`-`0x0041EEDF` | signed counter stepped toward zero each active frame; reaching zero calls `0x0041B9F0(record, 1)` |
| `+0x4C` | dword | `0x0041BE08`, `0x0041E021` | pointer to a frame-sequence byte array (§4) |
| `+0x50` | dword | `0x0041BE13`, `0x0041BE56`, `0x0041E0CE` | `0x80000000` default |
| `+0x5C` | word | `0x0041BD5C` | flags; see the note below |
| `+0x5E` | word | `0x0041DDE1`, `0x0041DEC6` | index into the selected path list |
| `+0x60` | word | `0x0041DCCD` | wait counter; decremented once per VM entry, and the VM body runs only when it becomes negative |
| `+0x62` | word | `0x0041BD65`, `0x0041ED4A` | countdown; `0x63`/`0x64` are special-cased at init |
| `+0x64`/`+0x66`/`+0x68` | word | `0x0041EC7F`-`0x0041ECA3` | signed inputs to the camera-distance test |
| `+0x6A` | word | `0x0041ECA3`, `0x0041ECC8` | radius input: `(value >> 3) + 0x258` |
| `+0x6C` | word | `0x0041ED9E`; also decremented at `0x0041DCBB` | counter stepped in the active-list pass and in the interpreter |
| `+0x6E` | word | `0x0041BD54`, `0x0041EC74`, `0x0041BBBC` | positive count, defaulted per type to 1..8 (§3.1); must be `> 0` for the activation branch; set to `0` when the slot is released |
| `+0x70` | dword | `0x0041BD4C`, `0x0041DC73`, `0x0041E147` | script program counter, persisted between frames |
| `+0x7C` | dword | written `0x0041C4AB`ff; **called** at `0x0041E7C7` | per-type thunk pointer written by the builder (§3.1) and invoked by the interpreter through `call eax` — see §5.5 |
| `+0x80` | dword | `0x0041C490`, `0x0041DC6D` | pointer to this slot's source record |

Offsets not listed are zeroed at `0x0041BDE6`-`0x0041BDFB` or were not
observed **in the parts of the interpreter this census analysed**. That
qualifier matters: `+0x14`, `+0x1C`, `+0x20`, `+0x24` and `+0x7A` are all read
or written in the interpreter tail (for example `add [esi+0x14],eax` at
`0x0041E455`, `imul edx,[esi+0x1c]` at `0x0041E353`, `imul eax,[esi+0x24]` at
`0x0041E34F`, and a write to `+0x7A` at `0x0041E6EE`), and the first two
drafts described them as merely zeroed.

### 2.2.1 Flag bits at `+0x5C`

Enumerated over the five functions this census establishes as pool code —
`0x0041B9F0`, `0x0041BD10`, `0x0041C420`, `0x0041DC60`, `0x0041EC40` — and, for
`0x0041DC60`, over its **whole** extent `0x0041DC60`-`0x0041E845` (§0.1).

Twelve bits are distinguished below. They are carried by **21 distinct
instructions** that touch `+0x5C` or `+0x5D` across the five functions —
`0x0041BA62`, `0x0041BAC2`, `0x0041BD5C`, `0x0041BD69`, `0x0041BDD7`,
`0x0041BE7B`, `0x0041DDB6`, `0x0041DED2`, `0x0041DFF2`, `0x0041DFF6`,
`0x0041E004`, `0x0041E201`, `0x0041E3E8`, `0x0041E43E`, `0x0041E583`,
`0x0041E65B`, `0x0041EC5C`, `0x0041EC66`, `0x0041ECF7`, `0x0041ED25`,
`0x0041ED9A` — several of which are the load feeding a test at the next
address, so the table cites both where they differ. The fourth draft (`1c499bf`) quoted an
aggregate "thirteen sites" that no reading of the table or the binary
produces; it is withdrawn in favour of the enumeration above.

The first two drafts read `0x0041DC60` only to `0x0041E1A8` and missed half of
its ten `+0x5C` sites, including a test this table once claimed did not exist;
the third missed a site in `0x0041BD10`.

| Bit | Sites in scope |
|---|---|
| `0x0001` | tested `0x0041EE89` (`test bl,cl`, `bl = 1`) |
| `0x0002` | tested **`0x0041E208`** (`test al,0x2`, on `mov al,[esi+0x5c]` at `0x0041E201`); cleared at `0x0041BE7B` |
| `0x0004` | tested `0x0041E589` (`test al,0x4`, load at `0x0041E583`) |
| `0x0008` | tested `0x0041DDBD` and `0x0041DED7` (`sar eax,3 / and eax,1`) |
| `0x0010` | tested `0x0041ED0E` |
| `0x0020` | tested `0x0041BD6C` and `0x0041BDD7` (both `test ...,bl`/`test bl,dl` with `bl = 0x20` from `0x0041BD17`), `0x0041ED25`, `0x0041EDA2` |
| `0x0040` | tested `0x0041BAC2` |
| `0x0100` | tested `0x0041E442`-`0x0041E448` (`and ecx,0x100 / test cx,cx`) |
| `0x0400` | tested `0x0041E3EC`-`0x0041E3F1` (`and eax,0x400 / test ax,ax`) |
| `0x2000` | tested `0x0041E65F`-`0x0041E669` (`and ecx,0x2000 / test cx,cx`) |
| `0x4000` | cleared `0x0041EC63`, set `0x0041ECEE` |
| `0x8000` | tested `0x0041BA62` (`test byte [esi+0x5d],0x80`) |

Opcode 12 rewrites the whole word at `0x0041DFF2`. A byte at `+0x5C` is a
common structure offset in this image, so an image-wide `[reg+0x5c]` search
would mix in unrelated structures; that search was not attempted and this
table is a completeness claim **only** over the five named functions.

Pool `+0x5C` is nevertheless reached from well outside them, and by two
different forms. `0x00418A6A` loads `0x0059B628` and `0x00418A77` tests `0xA0`
(bits `0x0080` and `0x0020` together). At least eight further sites use the
**absolute** address of slot 0's flag word, `0x0059B684` = `0x0059B628 + 0x5C`:
`0x00432063` (`mov dx,[ecx*4+0x59b684]`, then `and edx,0x4000`), `0x0043E82C`,
`0x0043FB31` and `0x004680EF` (`and byte [eax+0x59b684],0xbf`), `0x0043A194`
and `0x0043C343` (`mov eax,ds:0x59b684`), and `0x004335C3` and `0x0043E779`
(`mov eax,0x59b684`). None of their containing functions was analysed. This
also means the earlier `M2-second-deferral-hard-truth-audit.md` observation
that `0x00431804` tests slot 25's `+0x5C` at `0x0059C368` is one of a family,
not an isolated site.

## 2.3 Ground snap at build time

When source `+0x12` bit `0x20` is set, `0x0041C568`-`0x0041C587` calls thunk
`0x00401721` (`0x004ABE00`) with two arguments — a pointer to record `+0x04`
and the literal `0` (`push 0x0` at `0x0041C56B`, `push ecx` at `0x0041C56D`) —
adds `0x3200` to the result, and stores it into record `+0x08`, `+0x2C`,
`+0x38` and source `+0x04`. The called function is not named here.

## 3. Per-type tables

Both type switches use the same domain test — `type - 6`, `cmp 0x23`,
`ja default` — so the type id space handled by name is exactly **6..41**.

### 3.1 Builder switch (`0x0041C493`-`0x0041C529`)

Byte case table at `0x0041C600` (file `0x01BA00`, 36 entries); jump table at
`0x0041C5B0` (file `0x01B9B0`, 20 entries).

| Type | source `+0x10` default | record `+0x7C` thunk → target |
|---:|---:|---|
| 6 | 8 | `0x00401249` → `0x0041C160` |
| 9 | 2 | `0x004015D7` → `0x0041BEF0` |
| 10 | 2 | `0x00401AD2` → `0x0041C190` |
| 12 | 1 | — |
| 13 | 4 | `0x00401249` → `0x0041C160` |
| 15 | 6 | `0x00401A00` → `0x0041C050` |
| 16 | — | `0x00401253` → `0x0041C100` |
| 17 | 4 | `0x00401032` → `0x0041C2C0` |
| 18 | 3 | — |
| 19 | 6 | — |
| 22 | — | `0x00401253` → `0x0041C100` |
| 29 | — | `0x004018DE` → `0x0041C0C0` |
| 31 | — | `0x00401244` → `0x0041C130` |
| 34 | 2 | `0x0040106E` → `0x0041C210` |
| 36 | — | `0x00401253` → `0x0041C100` |
| 37 | 2 | `0x004015D7` → `0x0041BEF0` |
| 39 | 8 | `0x0040182A` → `0x0041C240` |
| 40 | 8 | — |
| 41 | 8 | — |

The four outcomes partition the 36-type domain exactly:

| Outcome | Count | Types |
|---|---:|---|
| both a count and a thunk | 9 | 6, 9, 10, 13, 15, 17, 34, 37, 39 |
| thunk only | 5 | 16, 22, 29, 31, 36 |
| count only | 5 | 12, 18, 19, 40, 41 |
| neither (default arm) | 17 | 7, 8, 11, 14, 20, 21, 23-28, 30, 32, 33, 35, 38 |

So **no** general statement of the form "per type, the builder writes a count
and a thunk" is true: only a quarter of the domain gets both, and just under
half gets neither. Ten distinct handler functions appear, all inside
`0x0041BEF0`-`0x0041C2C0`; their behaviour is not analysed here.

### 3.2 Release/reinitialise switch (`0x0041BAF0`-`0x0041BBAD`)

Byte case table at `0x0041BC48` (file `0x01B048`, 36 entries); jump table at
`0x0041BC18` (file `0x01B018`, 12 entries, index 11 = default). Exactly eleven
types take a non-default arm: 6, 9, 10, 13, 15, 17, 19, 34, 37, 39 and 41.
All eleven set record `+0x44` and all eleven select a frame sequence through
one of four `.data` pointers — `0x004C8758`, `0x004C8788`, `0x004C87A8`,
`0x004C87B8` — storing it in `+0x4C`, its first byte shifted left 16 in
`+0x40`, and a signed word (`0xFFDF`, `0xFFF0`, `0xFFE7` or `0xFFE8`) in
`+0x4A`. The default arm at `0x0041BBA7` writes only `+0x4A = 0xFFFF`.

### 3.3 Boolean table at `0x004C881F`

Indexed by the raw type byte (§1.4). Over the first **48** entries — the only
range examined — it is non-zero at exactly 1-5, 7, 8, 14, 16, 20-29, 32, 33,
36, 38 and zero at the rest. A non-zero entry makes the builder store
`slotIndex + 1` at `0x00599CA8 + type * 8`; a zero entry stores `0x7F`.

The table's **extent is not established**. Nothing in the code bounds the
index (§1.4), and the bytes immediately after index 48 are not obviously more
entries — indices 50, 52, 58, 60 and 62 hold `26`, `10`, `12`, `16` and `5`,
which look like an adjacent word array. Where this table actually ends is
therefore open, and that matters precisely because §1.4's index is unbounded.
The meaning of the table is not established either.

## 4. Frame-sequence table

`0x004C8758` (file `0x0C7358`) holds 28 dword pointers, all inside
`[0x004C8490, 0x004C8758)`, 25 of them distinct. Each target is a byte array
of small indices terminated by `0xFF`.

What follows the terminator is **not** a fixed two bytes. Measuring the gap
between each terminator and the next distinct array start across all 25
distinct targets gives:

```text
trailing bytes: 1 -> 2 arrays, 2 -> 4, 3 -> 4, 4 -> 2, 5 -> 5, 6 -> 1, 7 -> 6, 8 -> 1
```

Two arrays (`0x004C8658` and `0x004C8678`) have only one trailing byte before
the next array begins, so even "at least two" is wrong. Whether the surplus
bytes are part of the array, padding, or unrelated is not established.

Three values above `0xEF` appear mid-array, each three times: `0xFC`, `0xFD`
and `0xFE`. Examples:

```text
0x004C8490: 00 01 02 ... 17 FF 18 00
0x004C84C0: 00 01 ... 0C FE 0D 0E ... 17 FD FF 02 00
0x004C8710: 0F 0E 0D ... 01 00 FF 01 00
```

VM opcode 13 selects an entry with `mov eax,[eax*4+0x4c8754]`, i.e. the operand
is 1-based over this table. The operands actually present in the 40 scripts
range over 1..24, inside the 28-entry table.

The four `.data` pointers used by §3.2 are entries 0, 12, 20 and 24 of this
same table.

## 5. The per-actor behaviour VM

### 5.1 Interpreter

`0x0041DC60` (file `0x01D060`), reached through thunk `0x004017F8`. On entry it
loads `ebp = record[+0x80]` (source record) and `edi = record[+0x70]` (program
counter), decrements `record[+0x60]` at `0x0041DCCD`, and runs the body only
when that counter becomes negative.

The fetch/dispatch is:

```text
41dce8: 0f bf 07          movsx eax,WORD PTR [edi]
41dceb: 40                inc  eax
41dcec: 89 7c 24 30       mov  DWORD PTR [esp+0x30],edi   ; the saved PC
41dcf0: 83 f8 19          cmp  eax,0x19
41dcf3: 0f 87 38 04 00 00 ja   0x41e131
41dcf9: ff 24 85 48 e8 41 00  jmp DWORD PTR [eax*4+0x41e848]
```

so instructions are **signed 16-bit words** and the dispatch table at
`0x0041E848` (file `0x01DC48`) covers opcodes `-1` through `24` — 26 entries.

Loop control at `0x0041E131`-`0x0041E147`:

```text
41e131: cmp edi,DWORD PTR [esp+0x30]   ; PC before this instruction
41e135: jne 0x41dce4                   ; advanced → execute the next one
41e13b: cmp edi,DWORD PTR [esi+0x70]   ; unchanged since function entry?
41e13e: jne 0x41e143                   ; no → leave it alone
41e140: add edi,0x2                    ; yes → step past it
41e143: mov ebx,DWORD PTR [esp+0x14]
41e147: mov DWORD PTR [esi+0x70],edi   ; persist the PC
```

An instruction that does not advance the PC therefore ends execution for the
frame; if it was also the first instruction of the frame the PC is stepped by
one word so the actor cannot stall forever.

`0x0041E147` is **not** the function's only writer of `+0x70`. Over the full
extent `0x0041DC60`-`0x0041E845` there are **four**, and the three besides the
fetch loop all lie on paths entered only when the *pending* opcode is a
blocking one, so each steps past a blocking instruction:

| Site | Advance | Entered when |
|---|---|---|
| `0x0041E147` | the decoded PC | always, at the end of the fetch loop |
| `0x0041E1EB` | `+2` (`lea edx,[edi+0x2]` at `0x0041E1E2`) | mode local is 2, i.e. pending opcode 9 or 18 |
| `0x0041E2E1` | `+6` (`add eax,0x6` at `0x0041E2DE`) | pending opcode `0x11` (17) or `0x12` (18), gated at `0x0041E266`-`0x0041E27B`; that path additionally requires flag bit `0x0002` (`0x0041E208`), mode `< 3` (`0x0041E214`), `word[0x0059DD80] == 0` (`0x0041E21F`) and the source `+0x16` distance test at `0x0041E25E` |
| `0x0041E7FE` | `+2` (`add eax,0x2` at `0x0041E7FB`) | mode local `> 2` (`cmp ecx,0x3 / jl 0x41e801` at `0x0041E7EC`-`0x0041E7F2`, `ecx` from `[esp+0x4c]` at `0x0041E6C6`), i.e. mode 3 or 4, pending opcode 20 or 6 |

All three also zero the wait counter `+0x60`. The two `+2` sites independently
corroborate the 2-byte size used for blocking opcodes in §5.2. The `+6` site
is a consequence of the model that this census has **not** followed up: what
the six bytes it skips contain, and under what circumstances, is Unknown.

The `0x0041E7FE` writer was missed by the third draft, which swept only to
`0x0041E7D3` on the wrong extent — see §0.1.

### 5.2 Opcode table

For the eighteen opcodes with a handler body, the size is the PC advance that
handler performs. "blocking" means the handler does **not** advance the PC and
therefore ends the frame under §5.1; the eight blocking opcodes have no
handler of their own, and their 2-byte encoding comes from the stall-breaker
`add edi,0x2` at `0x0041E140`. §6.1's decoder uses size 2 for them for that
reason.

That derivation is sound — `[esi+0x70]` is not written until `0x0041E147`, so
`edi == [esi+0x70]` at `0x0041E13B` means nothing advanced this frame and the
resume point is blockingPC + 2 — but it is **not** the only site that steps
past a blocking instruction. See §5.1's writer list.

| Op | Handler | Size | What the handler does |
|---:|---|---:|---|
| -1 | `0x0041E128` | jump | `PC -= operand * 2` |
| 0 | `0x0041E131` | blocking | no body |
| 1 | `0x0041DD00` | 4 | `record[+0x60] = operand` |
| 2 | `0x0041DD10` | 6 | `record[+0x60] = (operand0 & *cursor++) + operand1` |
| 3 | `0x0041DD40` | 2 | takes two bytes from the cursor as a 12-bit value `a`, reads words `[0x004C2100 + ((a - 0x800) & 0xFFF) * 2]` and `[0x004C2100 + ((a - 0x400) & 0xFFF) * 2]`, multiplies each by the source `+0x14` scalar shifted left 4, arithmetic-shifts right 9, and writes `+0x34 = +0x28 + first` and `+0x3C = +0x30 + second` while `+0x38` copies `+0x2C` |
| 4 | `0x0041DDB6` | 2 | advances `+0x5E` through the list selected by source `+0x0E`/`+0x0F` in `0x005C5860`, writes `+0x34`/`+0x38`/`+0x3C`, sets the condition to `-1` one step before the end and `+1` at wrap |
| 5 | `0x0041E131` | blocking | no body; selects mode 1 (§5.3) |
| 6 | `0x0041E131` | blocking | no body; selects mode 4 and sets `+0x60 = 10` |
| 7 | `0x0041E131` | blocking | no body; selects mode 0 |
| 8 | `0x0041DE98` | 4 or jump | branch when the condition is `> 0` |
| 9 | `0x0041E131` | blocking | no body; selects mode 2 |
| 10 | `0x0041DEB4` | 4 | seeds `+0x5E` from source `+0x0F` (or 0) and writes `+0x04`/`+0x08`/`+0x0C` from that list entry |
| 11 | `0x0041DF48` | 4 | calls one of nine subroutines chosen by the operand (§5.4) |
| 12 | `0x0041DFEE` | 6 | `+0x5C = (+0x5C & operand0) \| operand1` |
| 13 | `0x0041E00D` | 6 | `+0x44 = operand0`; selects frame sequence `operand1` (§4) into `+0x4C` and `+0x40` |
| 14 | `0x0041E034` | 4 | condition = `(operand_low_byte & *cursor++) == 0` — only `[edi+0x2]`'s low byte participates (`mov cl,BYTE PTR [edi+0x2]`) |
| 15 | `0x0041E066` | 4 | `source[+0x1B] = (operand >> 4) & 0xFF` — the `mov dx,word` leaves the upper half of `edx` stale before `sar edx,4`, and only `dl` is stored |
| 16 | `0x0041E078` | 4 | condition = squared XZ distance from `+0x04`/`+0x0C` to `0x0059D910`/`0x0059D918` (each difference shifted right 5) is less than `operand * operand` |
| 17 | `0x0041E131` | blocking | no body; selects mode 1 |
| 18 | `0x0041E131` | blocking | no body; selects mode 2 |
| 19 | `0x0041E0B9` | 4 or jump | branch when the condition is `< 0` |
| 20 | `0x0041E131` | blocking | no body; selects mode 3, sets `+0x60 = 10` and `+0x50 = 0x80000000` |
| 21 | `0x0041E0CE` | 2 | `+0x50 = 0x80000000` |
| 22 | `0x0041E0DA` | 6 | `+0x48 = operand0`, `+0x49 = operand1` (byte writes) |
| 23 | `0x0041E0EB` | 4 | calls thunk `0x004017E4` (`0x004148A0`) with the operand and a pointer to `+0x04` |
| 24 | `0x0041E101` | 2 | condition = `byte[0x0059D9A6] != 0 \|\| (byte[0x0059D9A0] & 0x80)` |

Out-of-range opcodes take the same `0x0041E131` path and therefore block.

The "condition" is a function-local slot (`[esp+0x10]`) written by opcodes 4,
14, 16, 24 **and opcode 11 operand 5**, whose callee return value is stored at
`0x0041DFA2` (§5.4), and read by the branches 8 and 19. That enumeration is
over the **opcode handlers only**: the region past `0x0041E1A8` reuses the same
slot at ten further sites from `0x0041E369`, which this census has not
analysed.

`0x00599C60` is the shared byte cursor used by opcodes 2, 3 and 14. It is
initialised to `0x0081B428` at `0x00403C73` and `0x0042E7C8`, and `0x0081B428`
is the destination buffer passed together with the string `"rand.dat"`
(`0x004C5798`) at `0x0041011E`-`0x00410128`. `RAND.DAT` exists in the retail
`PC/BUGS/CD` listing.

The cursor is referenced **380** times across the image: 181 reads and 199
writes. Of the writes, exactly 2 are the immediate `0x0081B428` initialisation
above and **197** write back a computed register value. 197 is therefore the
figure that bounds how many sites can move the cursor — not 380 — and the
cursor is plainly not private to this subsystem.

### 5.3 Mode selection after the VM yields

`0x0041E14F`-`0x0041E1A8`: the opcode at the **just-persisted** PC is read —
that is the saved PC, or saved PC + 2 when the stall-breaker at `0x0041E140`
fired, or the entry PC when the function short-circuited at `0x0041DCD8` —
`opcode - 5` is range-checked against `0xF`, and a byte table at `0x0041E8F4`
(file `0x01DCF4`, 16 entries) selects one of eight arms in the jump table at
`0x0041E8D4` (file `0x01DCD4`).

| Pending opcode | Mode written |
|---:|---:|
| 5, 17 | 1 |
| 6 | 4 (also `+0x60 = 10`) |
| 7 | 0 |
| 9, 18 | 2 |
| 20 | 3 (also `+0x60 = 10`, `+0x50 = 0x80000000`) |
| anything else | unchanged (0) |

The mode is held in the function-local slot `[esp+0x4c]`, initialised to `0`
at `0x0041DCB5`, and read at **four** sites over the full extent:
`0x0041E1A8`, `0x0041E214`, `0x0041E3D7` and `0x0041E6C6` — the last being the
load whose value gates the fourth `+0x70` writer in §5.1. That slot aliases the
caller's argument area, but it is genuinely written and read within this
function.

It is written at **eight** sites: the five mode arms above, `0x0041E1BD`,
`0x0041E801`, and one that no `[esp+0x4c]` search will find — `0x0041E2E9`,
`mov DWORD PTR [esp+0x50],0x1`. That instruction reaches the same slot because
`push 0x59d910` at `0x0041E2E4` has just displaced `esp` by 4, so `[esp+0x50]`
there is `[esp+0x4c]` in the frame's own terms. It writes `1`, consistent with
§5.1's reading of the mode-`> 2` gate. The site was found by the eighth audit
and independently corroborated by `ghidra-evidence.json`, which models the slot
as `param_3` and emits `param_3 = (int *)0x1;` immediately before
`thunk_FUN_0041a550(&DAT_0059d910)`. Any future sweep of this slot must account
for `esp` deltas rather than matching on the displacement.

§5.2 has **eight** opcodes with no handler body — 0, 5, 6, 7, 9, 17, 18 and 20
— and seven of them are exactly the seven that select a mode here. Opcode 0 is
the exception: it blocks like the others but lies outside the `5..20` window,
so it leaves the mode at its initialised `0`, which is also what opcode 7
writes explicitly. Subject to that one case, a blocking opcode functions as a
persistent state and the non-blocking opcodes form the program that moves
between states.

### 5.4 Opcode 11 subroutines

Jump table at `0x0041E8B0` (file `0x01DCB0`), index `operand - 1`, range 1..9;
all nine operands occur in the shipped scripts.

| Operand | Thunk | Target | Argument |
|---:|---|---|---|
| 1 | `0x00401708` | `0x004288F0` | record |
| 2 | `0x00401131` | `0x004287D0` | record |
| 3 | `0x00401AA0` | `0x00432A50` | record |
| 4 | `0x00401893` | `0x00431C90` | none |
| 5 | `0x00401690` | `0x0043ADD0` | none; return value becomes the condition |
| 6 | `0x00401460` | `0x00436AF0` | record |
| 7 | `0x004019E7` | `0x00428A60` | record |
| 8 | `0x004017A8` | `0x00428990` | record |
| 9 | `0x0040105A` | `0x0043C250` | none |

### 5.5 The per-type handler call

At `0x0041E79E` the interpreter loads `eax = [esi+0x7c]`, null-checks it at
`0x0041E7A1`, builds a small stack record — including the pool record pointer
itself at `[esp+0x44]` (`0x0041E7B9`) — and executes:

```text
41e7c7: ff d0             call eax
```

This is the invocation point for the ten per-type handlers in
`0x0041BEF0`-`0x0041C2C0` that §3.1's builder installs, and it is the only
edge found between the interpreter and those handlers. It is an **outbound
register-indirect call**: the census's caller-completeness method (rel32 scans
plus absolute-value scans) would not have found it from the handler side, and
the first two drafts of this export missed it entirely.

What the handlers do with that stack record is not analysed.

## 6. Script table and shipped programs

`0x004C83F0` (file `0x0C6FF0`) holds 40 dword pointers. They are strictly
ascending, the first is `0x004C7D00`, each script ends where the next begins,
and the last ends exactly at `0x004C83F0` — the table's own first byte. The
bodies therefore occupy `[0x004C7D00, 0x004C83F0)`, `0x6F0` bytes.

Decoding all 40 bodies with the sizes of §5.2 gives **463 instructions**, with:

- **zero** misalignments — every body ends exactly on its recorded boundary;
- **zero** branch targets off an instruction boundary, across all 69 branch and
  jump instructions;
- every opcode value in the dispatch table (`-1` through `24`) used at least
  once;
- operand ranges inside their tables — opcode 11 operands are exactly 1..9
  against a 9-entry table, and opcode 13 sequence operands are 1..24 against a
  28-entry table.

One precision about that last check. **Opcode 11 is the only handler with a
range check**: `dec eax / cmp eax,0x8 / ja 0x41E0FC` at
`0x0041DF4C`-`0x0041DF50`. Opcode 13's handler
(`0x0041E00D`-`0x0041E02F`) contains no `cmp` and no `ja` — it indexes
`[eax*4+0x4c8754]` with the sign-extended operand directly. Opcodes 12, 14,
15, 16, 22 and 23 have no check either. So opcode 13's 1..24 span is a
property of the **shipped data**, not a bound the code enforces, and opcode 13
is a second instance of the unbounded-index class §1.4 records.

A fourth independent check comes from outside the table: `0x004372A8`-
`0x004372BE` sets pool slot 2's `+0x70` to `[0x004C8474] + 0x1A`.
`0x004C8474` is script-table entry 33, and `0x004C8240 + 0x1A = 0x004C825A`
falls exactly on the seventh decoded instruction of script 33.

Opcode use across the 40 scripts:

```text
-1:58   0:71   1:22   2:24   3:23   4:13   5:22   6: 7   7:34   8:10
 9:13  10: 5  11:12  12:20  13:61  14: 4  15: 4  16: 3  17: 1  18: 1
19: 1  20: 1  21: 1  22:46  23: 4  24: 2
```

Two decoded examples:

```text
script 33 @ 0x004C8240
  +0x00  22 set +0x48/+0x49        [64, -64]
  +0x06  13 select sequence        [0, 1]
  +0x0c   2 wait masked+offset     [63, 32]
  +0x12   3 cursor-derived target  []
  +0x14   5 blocking state 5       []
  +0x16  -1 jump back 5 words      []
  +0x1a  22 set +0x48/+0x49        [64, -64]     <- external entry point
  +0x20  13 select sequence        [1, 16]
  +0x26   6 blocking state 6       []
  +0x28  11 call subroutine        [6]
  +0x2c  -1 jump back 19 words     []

script 16 @ 0x004C7FB0
  22 [64,-64]; 12 [-5,4]; 13 [1,2]; 15 [1000]; 2 [63,32]; 3; 5;
  14 [1]; 8 [3]; -1 [9];
  12 [-5,0]; 13 [0,1]; 15 [400]; 2 [63,32]; 3; 5;
  14 [1]; 8 [3]; -1 [9];
  -1 [38]; 0
```

(Script 16's body is 21 instructions; the trailing `0` at `0x004C8006` is
included in the histogram above.)

### 6.1 Reproduction

```python
import struct
d = open('work/copies/BUGS_PC-full-disc/bugs.exe', 'rb').read()
def off(va):
    for vma, size, fo in ((0x401000, 0xbe765, 0x400),
                          (0x4c0000, 0xe88, 0xbec00),
                          (0x4c1000, 0x2c400, 0xbfc00)):
        if vma <= va < vma + size:
            return fo + (va - vma)
ptrs = list(struct.unpack('<40I', d[off(0x4c83f0):off(0x4c83f0) + 160]))
ends = ptrs[1:] + [0x4c83f0]
word = lambda va: struct.unpack('<h', d[off(va):off(va) + 2])[0]
SIZE = {-1: 4, 0: 2, 1: 4, 2: 6, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 4, 9: 2,
        10: 4, 11: 4, 12: 6, 13: 6, 14: 4, 15: 4, 16: 4, 17: 2, 18: 2,
        19: 4, 20: 2, 21: 2, 22: 6, 23: 4, 24: 2}
for start, end in zip(ptrs, ends):
    va = start
    while va < end:
        va += SIZE[word(va)]
    assert va == end, (hex(start), hex(va), hex(end))
```

## 7. Per-frame update

`0x0041EC40` (file `0x01E040`), reached through thunk `0x00401109` from
`0x00414597`, which lies inside `0x004144C0` (no `ret` between `0x004144C0` and
the call site). This reproduces the chain
`0x004144C0 -> 0x0041EC40 -> 0x0041DC60 -> 0x00436AF0` already recorded in
`M2-generic-resource-index-producer-census.md`, which reached the same three
functions from the resource-index direction without naming the subsystem.

**Pass 1** — `0x0041EC5C`-`0x0041ED5B`: for each of the 64 slots, clear flag
bit `0x4000`; skip when `+0x00 <= 0`; when `+0x6E > 0`, compute

```text
dx = (word[+0x64] - dword[+0x04] + [0x00599C90]) >> 8
dy = (word[+0x66] - dword[+0x08] + [0x00599C94]) >> 8
dz = (word[+0x68] - dword[+0x0C] + [0x00599C98]) >> 8
r  = (word[+0x6A] >> 3) + 0x258
```

and, when `dx² + dy² + dz² < r²`, append the record pointer to the list at
`0x0059D7E0`, set flag `0x4000`, and count it. `0x00599C90` is the camera
common block accepted by `EXP-20260816-165`. When `+0x6E <= 0` the slot instead
runs a separate branch that can call `0x00459620`, `0x004148A0` and the
initializer `0x0041BD10`, or decrement `+0x62` while it is below `0x1388`.

The list is NULL-terminated at `0x0041ED6A` and `0x00456640` is then called
with the camera block. That call and the `0x00459620` call at `0x0041ED19` are
both already tabulated in `M2-generic-resource-index-producer-census.md`; this
section is largely restatement (§0).

**Pass 2** — `0x0041ED9A`-`0x0041EEF7`: walks the list and branches on flag
`+0x5C` bit `0x20` and on `+0x6C`. In the bit-`0x20`, `+0x6C > 0` branch it
decrements `+0x6C` and adds `0x800` to `+0x08` (`0x0041EDB4`-`0x0041EDBE`) and
can call `0x00467E60` through thunk `0x00401488`. Other branches call
`0x0041D5B0` (thunk `0x0040147E`) or the VM `0x0041DC60` (thunk
`0x004017F8`). Finally it steps `+0x4A` toward zero; reaching zero calls
`0x0041B9F0(record, 1)` at `0x0041EEC6`, and the removal path calls
`0x0041B9F0(record, 2)` at `0x0041EEE4`.

`0x00467E60` is the same function `M2-signed-selector-producer-provenance.md`
identified as the sole non-zero writer of the positive image-table selector
words, over the same `0x0041EDF8 -> 0x00467E60` edge that export records. That
is the observed link from these records toward renderer-facing state; nothing
here proves a rendered result.

## 8. Release and reinitialise

`0x0041B9F0`-`0x0041BC16` (file `0x01ADF0`), thunk `0x00401528`, takes
`(record, mask)`.

With bit `0x01`: emits several positional calls through `0x0042AA50`, applies
the §3.2 type switch, and resets `+0x1C`, `+0x24`, `+0x48`, `+0x49`.

The `dec WORD PTR ds:0x0059D99E` at `0x0041BA23` is **conditional**, and the
condition matters: it sits inside the `cmp WORD PTR [esi+0x6e],0x3E6 / jne`
branch taken at `0x0041BA0A`-`0x0041BA10`. So it runs only for a slot whose
`+0x6E` is exactly `0x3E6` (998) — a value that no per-type default in §3.1
produces, since those are 1..8. Where such a value comes from is **Unknown**,
and it is the one place this census found `+0x6E` used as something other than
a small count.

With bit `0x02`: when `+0x62 == 0` it sets `+0x00 = 0` — releasing the slot —
then zeroes `+0x6E` and `+0x5A` and unlinks the record from `0x0059D7E0` by
shifting the remaining pointers down. This paragraph and the mode-1/mode-2
call classification restate
`M2-fixed-pool-index-producer-census.md`; see §0.

`0x0059D99E` has writers in at least eleven other functions, including
`cmp ...,0x39 / mov ...,0x38` at `0x004361CB` and `add ...,0xFFF9` at
`0x00438825`. It is **not** interpreted here.

## 9. Incidental string findings

- `CREAT\CREAT00.BIN` at `0x004C7970` (file `0x0C6570`). The 4-byte
  little-endian value `0x004C7970` occurs **nowhere** in the image, so the
  string has no immediate or stored-pointer reference; only computed access
  could reach it. No `CREAT` directory exists in the retail
  `work/copies/BUGS_PC-full-disc/PC/BUGS/CD` tree.
- An event subsystem logs through five strings at `0x004D823C`, `0x004D8264`,
  `0x004D82A4`, `0x004D82CC` and `0x004D830C`, including
  `EVENT : Event >>>%s<<< create function %s called.`; `0x004D82CC` is pushed
  at `0x0042DC14`. This was noticed while reading the string table for this
  packet and is recorded as a starting anchor only; no event code was read.

## 10. What this census does not establish

- Which creature each type id 6..41 denotes, and whether every one of them is
  an enemy rather than another kind of placed actor.
- **What the interpreter tail computes.** `0x0041E1A8`-`0x0041E845` is more
  than half of `0x0041DC60` and is where §5.3's five modes are consumed. This census
  records its `+0x5C` accesses, its `+0x70` writers, its `call eax` edge and
  the record fields it touches, but not what it calculates. Any claim about
  actor movement must start there.
- What the ten per-type `+0x7C` handlers, the nine opcode-11 subroutines, or
  the blocking states 0 and 5-20 actually do.
- The role of `0x00599CA8`, `0x004C881F`, `0x0059D99E`, `0x0059D9A0`,
  `0x0059D9A6`, `0x0059D9A7` or `0x00599B20`.
- Any runtime observation whatsoever: no slot was ever read live, no script was
  seen to execute, and the level-load gate on `0x005C5E88` bit `0x10` means it
  is not even established which shipped levels build the pool.
- Whether register-indirect dispatch reaches any of these functions from
  callers this census did not find; per the method note in
  `SUBSYS-audio-static-census.md`, call instructions, both thunk directions and
  `.data` pointer records were checked, but that does not exclude a computed
  call. The `call eax` at `0x0041E7C7` (§5.5) is a concrete demonstration that
  this method class misses computed dispatch by construction — it was found by
  reading the function, not by any scan.
