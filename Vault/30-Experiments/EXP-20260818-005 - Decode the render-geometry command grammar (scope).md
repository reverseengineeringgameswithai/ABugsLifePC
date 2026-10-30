---
type: experiment
id: EXP-20260818-005
date: 2026-08-18
question: 'What is the byte-level grammar of the LEVEL.DAT geometry payload that drives emission through the tri/quad primitives (FUN_00405fe0 / FUN_00407450, via thunks 0x00401d66 / 0x00401ccb)? Locate the walker and its dispatch, name the vertex/primitive record encoding, and confirm causally. (Linchpin for new-level authoring; KU-079. NOTE: the original wording assumed an opcode/table dispatch; Gate A refuted that - it is a type-switch.)'
status: superseded
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: 'static-first via scripts/ghidra-query.py over the bugs.exe export; runtime confirmation via the flight recorder (86Box, Phases 0/1/2) and/or play-pristine + game-memory causal A/B (user-observed, as in EXP-20260818-004)'
environment_version: 'ghidra-query current; export static/exports/BIN-97c95ba5572dce63/'
working_directory: /home/dev/ABLPC
configuration: 'static analysis (ghidra-query + raw objdump) plus offline decode of retail LEVEL01/LEVEL.DAT; no game execution, no target writes'
artifacts: []
addresses:
  - "0x00405FE0"
  - "0x00407450"
  - "0x00401D66"
  - "0x00401CCB"
  - "0x004C4108"
  - "0x005836A4"
  - "0x005BA240"
  - "0x0044BB70"
  - "0x005C5860"
  - "0x00418780"
file_offsets: []
result: 'Gate A GO + Gate B container grammar established BY INSTRUCTION EVIDENCE (the retail 7/7 payload chain pins only the 12-byte anchor stride).'
result_detail: ' Walker FUN_0044d430->FUN_004498f0->FUN_00453ff0->direct call 0x401d66; type-switch on instance+0xe (NOT an opcode fn-ptr table); payload = int32 group_count + count*12B anchors + per group int32 prim_count + prim_count*44B records. Open: semantics of the nine vertex int16, world scale. Gate C (causal) UNRUN.'
created: 2026-08-18T21:15:00
updated: 2026-10-02
---

# Decode the render-geometry command grammar (scope)

> Re-scoped 2026-08-18 by [[EXP-20260818-006 - R0 the static mesh format and where visible ground lives]]:
> type-3 is a camera-facing billboard batch, not terrain. Gate C moved to the
> type-0x41 format (the R2 track) and was never run on type-3.

Scopes **experiment #1** of the new-level authoring program
([[New-level authoring feasibility (PC)]]). Authoring a *visible* new level is
gated on this one decode: on the PC, level geometry is **emitted at runtime from
undecoded `LEVEL.DAT` command bytes**, so until the command grammar is known we
can compute collision but cannot draw new terrain. This is the linchpin (`KU-079`;
subsumes the render-side of `KU-009`/`014`/`023` and the `KU-038…043` Direct3D
append boundary).

## Confirmed static anchors (recon 2026-08-18)

Established by `ghidra-query` this session (byte-walks confirmed; names inferred):

- **Emit primitives are a twin pair:** `FUN_00405fe0` and `FUN_00407450` —
  near-identical (same callees, ~19,360-byte bodies), float-heavy (both call
  `__ftol` `0x004b0240`). `FUN_00405fe0`'s signature takes **up to four vertex
  pointer+attribute groups and two `short` indices**
  (`param_1/4/7/10` = `undefined4*`, each paired with a `uint` and an
  `undefined2`; `param_13/14` = `short`). Reading: these are the **per-primitive
  transform+emit** routines (triangle vs quad), *not* the byte-stream parser —
  they receive already-decoded vertices. This echoes the PS1 primitive pair
  `0x34` (3-pt) / `0x3C` (4-pt) (cross-port inference,
  [[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]]).
- ~~**Dispatch is table/pointer-driven.**~~ **REFUTED by Gate A — see the Gate A
  results below.** The original recon asserted that neither the primitives nor the
  thunks had any resolved caller, so the thunk addresses "appear only as data in a
  pointer table" and an opcode index selected the primitive. That was **wrong**:
  `thunk_FUN_00405fe0` has 12 callers and `thunk_FUN_00407450` has 2 in the same
  export, and `FUN_00453ff0` calls the primitive **directly**
  (`0x454199 call 0x401d66`). Dispatch is a **C `switch` on a per-instance type
  field**, not a function-pointer table. (Retained, struck through, as the audit
  trail for a corrected claim.) The one part that survives: inside `FUN_00405fe0`, `param_13` indexes `DAT_005836a4` (checked
  `!= 3`) and pointer table `PTR_DAT_004c4108[param_13*4]` (checked non-null)
  before drawing — a candidate **texture-page / material validity gate** at emit
  time (echoes PS1 texpage/CLUT state).
- **Load-path anchors (from the feasibility survey):** `LEVEL.DAT` buffer pointer
  global `0x005BA240`; fixup/relocator `0x0044BB70` (walks the 64-typed prefix,
  indexes the pointer table `0x005C5860` by signed record type, incl. the
  dispatch-`0x49` render path); level dispatcher `0x00418780` on internal index
  `0x00861C84`. Corpus parser `reimplementation/ablpc/level_dat.py` already
  locates the per-record payload regions.

## Plan — go/no-go gates

**Gate A — locate the walker + dispatch table (static).**
Find the routine that reads `LEVEL.DAT` command bytes and calls the emit thunks,
and the pointer table that maps an opcode/type to `0x00401d66`/`0x00401ccb`.
Route: `ghidra-query xrefs --to 0x004c4108` and `--to 0x005836a4` (the per-index
tables the primitives read); ~~find where the function-pointer table holding the
emit thunks is populated~~ *(premise refuted by Gate A — there is no such table;
the correct route was to grep decompiler text for the thunk callers, which exist)*;
identify the read cursor over the `0x005BA240` buffer.
- **Go:** a named walker function + the opcode/type -> handler table located.
- **No-go / reframe (still informative):** if geometry is emitted by a **fixed
  vertex-array walk with no opcode structure** (e.g. counted arrays of a single
  primitive record), the problem is *simpler*, not harder — record that and jump
  to Gate B on the fixed record.
- **Watch:** confirm the command bytes live in `LEVEL.DAT` (not `LEVEL.RAW`); if
  the walker's source buffer is the `LEVEL.RAW`/actor path, re-scope to that file.

**Gate B — first-tier grammar (static + corpus).**
Name **≥1 command/opcode's operand layout** and the **vertex/primitive record
encoding** (vertex stride, coordinate type and scale, index/material fields).
Cross-check the shape across the 21-file `LEVEL.DAT` corpus via `level_dat.py`. Use PS1 `FUNC_80010000` (visible-floor payload decode)
as an answer-key **lead only**.
- **Go:** a written record for one primitive type that predicts vertex count +
  coordinates from bytes.

**Gate C — causal confirmation.**
Prove the decoded bytes actually produce the predicted geometry, by **one** of:
(1) the flight recorder watching the walker read the exact command bytes and write
the vertex buffer (forensic, headless-friendly); or (2) a **berry-style guarded
A/B** — an explicitly user-authorized compare-before-write edit to one predicted
command byte under play-pristine, with the user observing the geometry change
(the method that confirmed KU-073 in `EXP-20260818-004`).
- **Go (experiment success):** a byte -> visible-geometry (or recorder-observed
  vertex-buffer) receipt matching the Gate-B prediction.

## Discriminating result

A single receipt in which **a named command byte at a known `LEVEL.DAT` offset
maps to a specific decoded primitive**, confirmed either by the recorder (walker
reads those bytes -> writes those vertices) or by a guarded causal edit that
changes the on-screen polygon as predicted. Absent that, the grammar stays
inferred.

## Risks / boundaries

- **Indirect dispatch** may not be statically resolvable from the export alone
  (the pointer table is populated at runtime); the recorder or a live pointer read
  may be needed to enumerate the opcode->handler map. Budget for a runtime assist.
- **Headless Direct3D capture is the recurring blocker** — prefer the recorder
  (forensic) or a user-eyes A/B under play-pristine over trying to screenshot
  headless geometry.
- **Static-first; no target writes** except a single explicitly-authorized,
  guarded, receipted causal A/B (Gate C option 2), reverted after.
- Cross-port items are **inference** until PC-confirmed; no unidentified symbol is
  renamed without evidence (candidates stay `candidate_*`/`FUN_*`).
- Scope is the **first grammar tier**, not the whole format — one command type +
  the vertex encoding + one causal receipt is a complete, bankable result.

## Acceptance (James-style)

Reproducible from the export: the walker + dispatch-table identities re-derivable
by an independent reader; the Gate-B record layout checkable against the corpus;
the Gate-C receipt independently replayable. Hand to fresh James on completion,
per the project's verification pattern.

## Gate A — RESULTS (2026-08-18): GO, with a reframe

Static-confirmed (decompiler-visible + cross-checked: the relocator writes the
pointers the walker reads; the `FUN_004498f0` type-switch and `case 3 →
FUN_00453ff0` were independently re-verified against the export). Names inferred.
**Not yet runtime-confirmed** (that is Gate C).

**Reframe:** emission is **not** an opcode → function-pointer table. It is a C
`switch` on a per-instance **type field**, and the geometry payload is a
**count-prefixed nested vertex array**, not a command bytestream. (Recon's "emit
primitives have no caller" was **under-querying, not an export artefact**: in the
same export `thunk_FUN_00405fe0` has `caller_count = 12` and `thunk_FUN_00407450`
has `2`, and `FUN_00453ff0` reaches the primitive by a **direct `call rel32`**
(`0x454199 e8 c8 db fa ff  call 0x401d66`) — not through a data table. The
thunk-breakage caveat explains only `FUN_00405fe0.callers == []`, not the thunks'.)
This is the "simpler, fixed-array" branch the scope anticipated → proceed to Gate B.

**Walker (three stages, all decompiler-visible):**
- `FUN_0044d430` — per-frame scene driver: walks instance arrays (`0x005ba7e0`
  primary, `0x005ba128` sprites), radius-culls, bins near/far, `>>5` (÷32) coords.
- `FUN_004498f0` — **type dispatch**: `switch(*(ushort*)(instance+0xe) & 0xbfef)`
  → per-type drawer.
- `FUN_00453ff0` — **type-3/0x43 quad-batch walker** → emits via
  `thunk_FUN_00405fe0` (`0x00401d66`, quad) on the `DAT_0059f7f0 == 2` path (labelled "hardware" by inference only).

**Type table (from `FUN_004498f0`):** `1/0x41` sprite (`FUN_0045a7f0`); `2/0x42`
& `0xa/0x4a` mesh (`FUN_00454b70`→`FUN_00405fe0`) (2026-10-02 audit: the later
[[EXP-20260927-001 - Complete original level Blender maps]] labels these the
other way round: `0045A7F0` draws ordinary meshes and `00454B70` camera-facing
sprites); **`3/0x43` textured quad batch** (see the billboard callout — *not* a grid)
(`FUN_00453ff0`→`FUN_00405fe0`); `4,9,0xc,0x21,0x24,0x29,0x2c` (+`|0x40`) →
`FUN_0045a7f0`. Load-time typed index `0x005c5860` is populated by relocator
`FUN_0044bb70` (record+2 signed type → `[type]`; `0x3f`→4× stride else 3×).

**Type-3 geometry payload (from `FUN_00453ff0(geom, rot3x3, translation)`):**
`int count_groups`; then `count_groups × 3 int` anchors (transformed by the 3×3
`short` rot + translation, `>>0xc` = ÷4096, 12-bit fixed); per group `int
count_prims`, then `count_prims × 44-byte` records **immediately** (there is **no
skipped `int`** — that was an early misread of the two-cursor `ebx` / `esi = ebx+4`
pattern; `0x4540f6 mov eax,[esi]` is the count, `lea ebx,[esi+4]` the first record).
**Record = 44 B**: nine vertex `int16`, four `int16` UV/attr words at
`0x14/0x16/0x18/0x1a`, four `uint32` RGB colours at `0x1c/0x20/0x24/0x28`
(unpacked `<<0xd` / `<<5` / `>>3 & 0x1fe000` — **RGB channel repositions, NOT a
world scale**) + **5-bit material/texture-page index** at
**record byte `0x12` `& 0x1f`** (`mov al,[esi+0xe]`, and `esi = record+4`; the
Gate-A wording "rec+0xe" was relative to the wrong cursor). It is `param_13` into
`FUN_00405fe0`'s `DAT_005836a4 != 3` / `PTR_DAT_004c4108` gate. Emit:
`DAT_0059f7f0 == 2` (branch confirmed at `0x45413f`–`0x454155`; the
"hardware/D3D" and "software" labels are both **inferred, not evidenced**) →
`thunk_FUN_00405fe0`; `==1` (software) → builds an `0x80`-byte display-list record
**tagged `0x49`** in `0x0081bc28[0x008082c8++]`.

**Source buffer = LEVEL.DAT** (`0x005ba240`), confirmed by relocator-writes /
walker-reads agreement (no `LEVEL.RAW` in this path). Nesting: **instance** (20 B
in `0x005ba7e0`: +0..8 world pos, +0xc radius, **+0xe type/flags**, +0x10→object)
→ **object** (+0x14 → geometry payload) → the count-prefixed payload above.

> [!warning] Contradiction to reconcile (do not silently merge)
> **`0x49` now has multiple candidate meanings:** (a) a **level instance type**
> `9/0x49` in the `FUN_004498f0` switch (sprite drawer `FUN_0045a7f0`); (b) the
> **software display-list primitive tag** written by `FUN_00453ff0`; and (c) the
> pre-existing "dispatch-`0x49`" in [[PC LEVEL DAT prefix]] (a record payload
> target). These are three different `0x49` contexts. **Discriminating step:** in
> Gate B, tabulate which structure each `0x49` indexes (instance type field vs
> display-list tag byte vs DAT record type) and confirm they are independent.

**Gate B next step:** decode the 44-byte type-3 primitive record — the 4-vertex
coordinate packing and the colour/UV fields — and establish the world scale by
matching decoded vertices against `reimplementation/ablpc/level_dat.py` payload
regions. Locate a concrete type-3 instance by walking `0x005ba7e0` (or the
object[+0x14] pointer) and predict vertex count + coords for one primitive.

## Gate B — PARTIAL (2026-08-18): header confirmed byte-exact, vertex stride contradictory

Static only (decompiler + **raw objdump of the retail exe**, VA `0x00453ff0`). No
runtime evidence yet; nothing here is causally confirmed (that is Gate C).

**CONFIRMED by raw disassembly** (`objdump -d --start-address=0x453ff0`, matching
the decompiler):
- **Payload header:** `int32 group_count` at +0, then `group_count × 12-byte
  anchors` (3 × `int32` = model-space X/Y/Z). Instruction evidence at `0x453ffd`–
  `0x45400b`, in program order: `lea edx,[eax+0x4]` (anchors) / `mov eax,[eax]`
  (count) /
  `lea ecx,[eax+eax*2]` + `lea ecx,[edx+ecx*4]` → primitives begin at
  `anchors + group_count*12`.
- **Group anchor transform:** anchor is rotated by the caller's **3×3 `int16`
  matrix** (loads `WORD PTR [edi+0x0…0xa]` at `0x454034`–`0x45408d`), `>>0xc`
  (÷4096, 12-bit fixed point), then translated by `param_3[0..2]`.
- **Vertex = 3 × `int16` (x, y, z) = 6 bytes**, padded to 8 in the emit slot.
  Evidence: the software path reads each vertex as three consecutive `movsx
  WORD PTR` at slot+0/+2/+4, with slots at an 8-byte pitch (`esp+0x44/0x46/0x48`,
  `0x4c/0x4e/0x50`, `0x54/0x56/0x58`, `0x5c/0x5e/0x60`) — matching the four
  `&local_38/&local_48/&local_50/&local_40` pairs handed to `FUN_00405fe0`.
- **Per-primitive record stride = 44 bytes** (`0xb` ints; both cursors advance by
  `0xb` per iteration).
- **Material index** = `record byte 0x12 & 0x1f` (5 bits) → `param_13` of
  `FUN_00405fe0`, gating `DAT_005836a4 != 3` / `PTR_DAT_004c4108`.
- **Colour/UV** at record ints 7–10, unpacked `(v & 0xff) << 0xd`,
  `(v & 0xff00) << 5`, `(v >> 3) & 0x1fe000` — an **RGB888 channel unpack**. NOTE:
  this `<<5` is a colour-channel reposition and is **not** evidence of the PS1 ×32
  world scale (an earlier note said otherwise; corrected). A `>>5` does appear in
  `FUN_0044d430`, but on the **view-origin globals** `DAT_005bdb9c/a0/a4` — not on
  instance coordinates (those take `>>4` there). No ×32 is established for vertex
  positions.

> [!success] RESOLVED (2026-08-18, same session) — the overlap is REAL
> Settled by **raw instruction evidence, not plausibility**. In the primitive loop
> (`0x45410a`–`0x45414e`) the exe keeps two cursors — `ebx` = record base
> (`add ebx,0x2c`) and `esi = ebx+4` (`lea esi,[ebx+0x4]`) — and **loads the same
> word twice into two different vertex slots**: `mov ecx,[esi+0x4] → [esp+0x50]`
> **and** `mov ecx,[esi+0x4] → [esp+0x44]` (both `R+0x08`); likewise `[esi+0x8]`
> (`R+0x0c`) → `[esp+0x48]` and `[esp+0x54]`. Hypothesis **(a) is REFUTED**
> (nothing was folded — the duplication is explicit in the object code) and
> **(c) is REFUTED** (`ebx` is the true record base; `esi` is merely a second
> cursor). **(b) holds: consecutive vertices genuinely share one `int16`.**
> Confirmed by exact byte budget (below): the layout accounts for all 44 bytes,
> whereas 6-byte-packed vertices would need 48. The *geometric* meaning of the
> sharing (deliberate strip-style compression?) is a **separate open question** —
> see "Remaining" below.
>
> **Confirmed 44-byte record layout (instruction-cited):**
> | Offset | Field | Evidence |
> | --- | --- | --- |
> | `0x00`–`0x11` | 9 × `int16`: v0=(s0,s1,s2), v1=(s2,s3,s4), v2=(s4,s5,s6), v3=(s6,s7,s8) | paired loads at `0x45410a`–`0x45414e`; 3 × `movsx` per slot at +0/+2/+4 |
> | `0x12` | material, 5 bits | `mov al,BYTE PTR [esi+0xe]` + `and eax,0x1f` (`0x45410c`, `0x454146`) |
> | `0x13` | spare (unread) | byte budget |
> | `0x14,0x16,0x18,0x1a` | 4 × `u16` per-vertex attr | `mov cx,WORD PTR [esi+0x10/0x12/0x14/0x16]` |
> | `0x1c,0x20,0x24,0x28` | 4 × `u32` per-vertex colour | `mov eax,DWORD PTR [esi+0x18/0x1c/0x20/0x24]` |
>
> Also confirmed: **group layout = `int32 prim_count` + `prim_count × 44 B`**
> (loop exit sets the next group header to the post-record cursor; `add edx,0xc`
> advances the anchor array), and the arg order pushed to `FUN_00405fe0` is
> vertex slots `0x5c, 0x4c, 0x44, 0x54` = records `R+0x00, R+0x04, R+0x08, R+0x0c`.

> [!warning] SUPERSEDED — original contradiction record (kept for audit trail)
> The four vertex loads **overlap**: with record base `R`, the decompiler gives
> `v0 = (lo(R0), hi(R0), lo(R1))`, `v1 = (lo(R1), hi(R1), lo(R2))`,
> `v2 = (lo(R2), hi(R2), lo(R3))`, `v3 = (lo(R3), hi(R3), lo(R4))` — so `v0.z` and
> `v1.x` read the **same two bytes**, i.e. a 4-byte stride between vertices that
> are each 6 bytes wide. That is geometrically impossible for four independent
> corners, so **one of these is wrong**: (a) vertices are 6-byte packed
> contiguously (v0@0, v1@6, v2@12, v3@18 = 24 B) and Ghidra folded the unaligned
> loads; or (b) the four "vertices" are a **sliding window over a shared strip**
> (consecutive corners genuinely share a coordinate); or (c) my record-base
> alignment is off by an int (the walker keeps two cursors exactly 1 int apart —
> `piVar23 = hdr+1`, `param_1 = hdr+2` — which is where an off-by-one would hide).
> **Do not pick one by plausibility.**
> **Discriminating experiment:** decode a real type-3 payload from a retail
> `LEVEL.DAT` under hypotheses (a) and (b)/(c) and compare: only the correct one
> yields coordinates inside the level's known world bounds AND quads that tile
> into a coherent grid (adjacent primitives sharing edges).
> *(Historical note: this block originally offered a byte-budget "prior" favouring
> (a). That prior was arithmetically wrong (24 + 16 = 40, not 44) and pointed at the
> hypothesis the evidence refutes; the correct accounting is in the RESOLVED block
> above — 18 + 2 + 8 + 16 = 44.)*

## Gate B — container grammar tested against real data (2026-08-18)

The discriminating test was run on retail data. It **partly** discriminates — see
the corrected strength assessment below; an earlier version of this note
overstated it as conclusive.

**Instance array identified in-file.** `LevelDat.summary()`'s `primary_records`
**are** the runtime instance array (`0x005ba7e0`): 20-byte stride (Level03:
480 × 20 = 9,600 B = `0x1694`–`0x3c14`), and across the **21-file corpus every
type value at `+0xe` (masked `& 0xbfef`) is a valid case of the `FUN_004498f0`
switch** (1, 2, 3, 4, 9, 0xa, 0xc, 0x41, 0x49, 0x4c) **with exactly one
exception**. Two independent confirmations of the Gate-A instance layout.
*(The exception: `LEVEL03/LEVEL1.DAT` idx 165, raw flags `0x93` → masked `0x83`,
i.e. `0x80|3`, which the switch does not handle. It is **not** a count overrun —
its coordinates are plausible, its object offset continues the sequence, and the
`0x8000…` sentinel follows immediately. A genuine record with an unhandled type;
unresolved.)*

**Chain resolved:** instance `+0x10` → object; object `+0x14` → geometry payload
(both in-file offsets, relocated at load by adding `0x005ba240`).

**Where type-3 geometry lives:** most levels have none. `LEVEL01/LEVEL.DAT`
has **7 type-3 instances** (+3 type-0xa meshes); `LEVEL00`, `LEVEL03/LEVEL1.DAT`
and `LEVEL07` have one or two type-2. Level03's `LEVEL.DAT` has **zero** — its
terrain is not type-3 geometry.

> [!note] The 7 payloads chain contiguously (what it does and does not prove)
> Parsing all 7 `LEVEL01` type-3 payloads with the confirmed grammar
> (`int32 group_count` + `group_count × 12 B` anchors + per group
> [`int32 prim_count` + `prim_count × 44 B`]) yields **every payload's computed
> end exactly equal to the next payload's start**:
> `0x44140 → 0x448c4 → 0x45048 → 0x455b0 → 0x45b54 → 0x4629c → 0x46a20 → 0x46e98`
> (instances 118, 267, 13, 80, 111, 202, 108). Group counts 19–32, all
> `prim_count` sane, all ends in-file. The payloads form one contiguous arena.
>
> **Strength of this test — corrected (an earlier version overclaimed).** Every
> one of the **193 groups has `prim_count == 1`**, so payload size collapses to
> `4 + gc*60` and the chain constrains only `anchor + 4 + skip + rec = 60`.
> Verified by brute force: it **does** pin `anchor_stride = 12` (anchor 16 fails a
> sanity gate on the first payload; anchors 0 and 8 read plausible counts but break
> the chain), but it gives **zero** discrimination on the skip/record split —
> **every** `(skip, rec)` with `skip + rec = 44` chains 7/7 identically, i.e. all
> **11** int-aligned combinations `skip = 0, 4, … 40` (including the "one skipped
> int" reading this note elsewhere refutes). So: `anchor = 12` is confirmed **by
> data** (anchor 16 fails a sanity gate; anchors 0 and 8 read plausible counts but
> then run past EOF); the
> `skip=0 / rec=44` split is confirmed **only by the instruction evidence**
> (`0x4540df lea ebx,[esi+0x4]` establishes the record base and `0x4540f6
> mov eax,[esi]` reads the count at the group base; `0x4548df add ebx,0x2c`
> advances one record). The conclusion stands; the *chain* is not what proves it.

**Both emit paths do the sliding-window read (settled statically).** An open
question here previously asked whether `FUN_00405fe0` reinterprets the four slots.
It does not: it reads three shorts per vertex pointer —
`local_8 = (short)*param_1; sStack_6 = (short)(*param_1 >> 0x10);
local_4 = (short)param_1[1];` (and identically for `param_4/7/10`) — then applies
the same 3×3 matrix. So the software path and the D3D path agree.

**Corpus regularity — a strong structural clue (193/193 records).**
- `s0 == s6` **and** `s2 == s4` in **every** record; `s8 ∈ {0, ±1}` (152/17/24).
- Material byte `0x12` is `0x62` (`& 0x1f` → 2) in **all 193**; byte `0x13` is `0`
  in all 193. So material is never exercised across this corpus.
- Consequence: under the sliding window the XZ corners are
  `(s0,s2) (s2,s2) (s2,s0) (s0,s8)` — i.e. **three corners are the combinations of
  just two values {s0, s2}** (an axis-aligned quad footprint), and the **fourth is
  degenerate in every record** (it needs `s0` to close the square but reads
  `s8 ∈ {0,±1}`). Example (`idx13` rec 0)
  `(91, 340, -92, 407, -92, -342, 91, -409, 0)` → XZ `(91,-92) (-92,-92) (-92,91)
  (91,0)`, with `y = (340, 407, -342, -409)` as the four corner heights.
- **Hypothesis (NOT confirmed):** a compact axis-aligned quad — two footprint
  values + four corner heights — which would map naturally onto a heightfield
  exporter. The competing reading is four `(x,y)` corner pairs + one spare. **Do
  not pick by plausibility**; the discriminator is **Gate C** (poke one short,
  observe which corner moves).
- **World scale: no evidence either way.** No ×32 has been shown for vertex
  positions (the `<<5` in this record is an RGB channel shift, not a coordinate
  scale).

> [!warning] Type-3 is probably NOT the terrain path — re-scope before building on it
> **20 of the 21 corpus files contain zero type-3 records**; only
> `LEVEL01/LEVEL.DAT` has any (7 payloads / **193 quads** / one material `0x62`).
> The quads are **tall and thin**: X/Z extent mean **153** (median 148, range
> 115–204) versus Y extent mean **790** (median 774, range 746–974) — about
> **5.2 : 1** — clustered 19–32 per instance around scattered anchors.
>
> **The drawer is an explicit billboard (static evidence, not just aspect ratio).**
> The vertex rotation matrix (globals `DAT_0063e888…8b0`) is written, in reachable
> code, only by `FUN_004636c0` (a second static write site exists at `0x49d0b0` but
> is **dead** — its only thunk `0x40173f` has no call sites), which `FUN_004498f0` **case 3** calls **once per instance** after
> building the matrix from `-DAT_005b1ec2` composed with the view
> (`0x463c80` → `0x463a60` → `0x4636c0`). Inside `FUN_00453ff0` the per-group calls
> are `0x463770` + `0x463740`, and `FUN_00463740` writes **only the translation**
> (`DAT_0063e8b8/8bc/8c0`). So the orientation is fixed per instance and derived
> from a camera-related global (`DAT_005b1ec2`, set in the camera path
> `FUN_00455710` — *identification as camera yaw is inferred*). Corroborating: all
> **7 objects carry Euler angles `(0,0,0)`** at `obj+0xc/0xe/0x10`, so model space
> is world orientation and no per-object rotation lays these panels flat.
>
> **Therefore type-3 is almost certainly camera-facing vertical panels (candidate
> foliage/props), not ground.** **What draws each level's visible ground is
> unidentified.** Note the next candidate is weak too: **16 of the 21 files contain
> no type-2, type-3 *or* type-0xa record at all** (including `LEVEL03/LEVEL.DAT`
> with 480 instances), so ground likely does **not** come from the `LEVEL.DAT`
> instance array — widen the search (`TERRAIN.ALL`, `LEVEL.RAW`, other paths).
> This materially re-scopes track R: R1's accept criterion "round-trip every type-3
> payload" is a far weaker bar than it sounds, and type-3 is likely the **wrong
> target** for terrain authoring.

**Gate B remaining:** (1) the **geometric intent** of the nine shorts (axis-aligned
quad vs corner pairs) — Gate C discriminates; (2) the **world scale** for vertex
positions (no evidence yet); (3) **which type carries visible ground** — note `FUN_00454b70`
(type-2/`0xa`) is a *weak* candidate: **16 of 21 corpus files contain no type-2,
type-3 or type-0xa record at all** (incl. `LEVEL03/LEVEL.DAT`, 480 instances), so
ground likely is not in the `LEVEL.DAT` instance array — widen to `TERRAIN.ALL`,
`LEVEL.RAW` and other paths; (4) the grammar is
untested for `prim_count > 1`, for materials other than `0x62`, and for byte
`0x13 != 0` — none occur in this corpus.

## Links

- [[New-level authoring feasibility (PC)]] (parent assessment), `KU-079`, `KU-080`,
  [[XPORT-20260818-007 - PS1 Blender-to-native level authoring pipeline and format leads]],
  [[PC LEVEL DAT prefix]], [[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]]
  (the causal-A/B method), [[Flight Recorder]] (Gate-C forensic option).
