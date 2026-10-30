# M2 fixed-pool index producer census

## Scope and evidence boundary

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact targets: first dwords `0x0059B730` and `0x0059B7B4`, slots 2 and
  3 of pool `[0x0059B628,0x0059D728)` with stride `0x84`.
- Exact consumers: `0x004372A2-0x004372B7` and
  `0x00437337-0x0043734C` in `0x00436B40`.
- Static sources: existing structured Ghidra evidence export and independent
  GNU objdump 2.46 native disassembly of the exact work-copy executable.

This was an offline PC-native census. It did not launch or mutate the game,
inspect another object or resource family, extend a parser or schema, assign
field semantics, or consult the PS1 source.

## Exact slot and source arithmetic

The destination words are exact record starts:

```text
0x0059B628 + 2 * 0x84 = 0x0059B730
0x0059B628 + 3 * 0x84 = 0x0059B7B4
```

`0x0041C420` walks the separate source table at `0x1C` bytes per record, so
the corresponding source records and structurally relevant bytes are:

| Pool slot | Source record | source `+0x0C` | source `+0x10` | source `+0x11` | source `+0x12` |
|---:|---:|---:|---:|---:|---:|
| 2 | `0x00599EE8` | `0x00599EF4` | `0x00599EF8` | `0x00599EF9` | `0x00599EFA` |
| 3 | `0x00599F04` | `0x00599F10` | `0x00599F14` | `0x00599F15` | `0x00599F16` |

`0x0046574D-0x0046576A` clears and then copies exactly `0x700` bytes from a
parsed `LEVEL.RAW` type-`0x23` packet into source table
`[0x00599EB0,0x0059A5B0)`. This source is separate from the M1
`LEVEL*.DAT` 20-byte records, relocated payloads, and positive targets.

## Complete bounded first-dword writer set

### 1. Whole-pool initialization clear

`0x0041C424-0x0041C430` loads count `0x840` dwords, zeroes `EAX`, points
`EDI` at `0x0059B628`, and executes `rep stosd`. This writes zero to both
target words as part of the exact `0x2100`-byte pool clear.

This zero cannot reach either indexed read by itself. Every update at
`0x0041EC5C-0x0041EC66` first clears record flag `0x4000`, and only a record
whose first dword is positive at `0x0041EC6A-0x0041EC6E` can be inserted and
have `0x4000` restored at `0x0041ECE3-0x0041ECF7`. The readers require that
flag at `0x0043728D-0x00437298` and `0x0043731E-0x0043732D`.

### 2. Source-byte copier at `0x0041BD10`

For a retained source pointer at record `+0x80`, native instructions
`0x0041BD19-0x0041BD24` read one unsigned byte from source `+0x0C` and store
it as the record first dword:

```text
record[0] = zero_extend(source[0x0C])
```

The direct thunk callers are exactly:

| Call site | Destination reachability | Classification |
|---:|---|---|
| `0x0041C559` | All 64 pool slots, including 2 and 3 | Initial population after the source gate |
| `0x0041ED3A` | The same 64-slot pool | Reinitializes an existing positive record |
| `0x0043213E` | Cursor constrained to slots 2 or 3 | Reinitializes the selected target slot |
| `0x00436257` | Fixed record `0x0059C9C0` | Outside the selected pool; excluded |

At `0x0041C458-0x0041C45D`, source `+0x0C == 0` skips the destination
population entirely. The retained source pointer is stored only on the
nonzero branch at `0x0041C490`. Therefore every valid initialized-pool call
to `0x0041BD10` rewrites the same nonzero source byte; a skipped slot remains
clear and lacks the retained source pointer needed by later calls. The copier
does not supply reader-time zero for a valid slot 2 or 3 record.

The same copier also establishes the later zero predicate and reader flag
inputs: source `+0x11` is copied to record `+0x62` at
`0x0041BD60-0x0041BD65`, while source `+0x12` is copied to record `+0x5C` at
`0x0041BD58-0x0041BD5C`.

### 3. Conditional active-list removal zero at `0x0041BBBA`

`0x0041B9F0` tests mode bit 2 at `0x0041BBAD-0x0041BBB2`. On that branch,
it writes zero to the record first dword at `0x0041BBBA` only when record
`+0x62 == 0` at `0x0041BBB4-0x0041BBB8`. It then clears record `+0x6E` and
`+0x5A` and removes the record pointer from the list, but does not write
record `+0x5C` or `+0x44`.

All direct thunk calls are classified:

| Call site | Mode | First-dword effect |
|---:|---:|---|
| `0x0041EEC6` | 1 | Mode-bit-2 branch not taken |
| `0x0041EEE4` | 2 | Can execute `0x0041BBBA` |
| `0x00429E00` | 1 | Mode-bit-2 branch not taken |

The mode-2 call consumes the active-list record pointer built from the same
64-slot pool. Slots 2 and 3 are therefore in its bounded destination set when
they satisfy the list gates.

## Other exact-address and pool-record closures

The structured export reports no other direct WRITE reference congruent with
a pool-record first dword; its only such direct write is the `rep stosd` at
`0x0041C430`. The remaining exact-address references were checked through
their callees:

- `0x004322E2/0x004322F8` pass slots 2 and 3 to `0x00428BB0`, which reads
  position/state fields but does not write record `+0x00`;
- `0x004372EA/0x00437380` pass the records to `0x0041DC20`, which writes only
  `+0x40`, `+0x44`, and `+0x4C`;
- `0x004372FB`, `0x00437391`, `0x00437446`, and `0x004374EA` pass a record to
  `0x00414F80`, whose record access is the `+0x5C` gate and `+0x04` position;
- `0x00445020` walks the bounded pool and writes later fields, including
  `+0x64` through `+0x74`, but reads rather than writes record `+0x00`.

The bounded active-record update closure was also checked. `0x0041DC60`,
`0x0041D5B0`, `0x00467E60`, and every callback installed at record `+0x7C`
by `0x0041C420` write later record/source fields, not record `+0x00`. Thus
the three store classes above are complete at the declared direct and bounded
fixed-pool boundary.

## Reader-time zero reachability

The initialization clear is not reader-reachable because it cannot pass the
`0x4000` reader gates. The source copier cannot write zero to a valid
initialized record because the same source byte is the population gate.

The removal writer is different. A positive record can be inserted and gain
`0x4000` at `0x0041ECF7`; later in that same `0x0041EC40` call, mode 2 can
reach `0x0041BBBA`. One concrete native state producer is
`0x0041CE5F`, which writes `-20` to record `+0x6C`; the per-frame path at
`0x0041EE7D-0x0041EE87` advances that word to zero and branches to the mode-2
call. If the separately copied record `+0x62` is zero, `0x0041BBBA` clears the
first dword after list insertion while leaving `0x4000` and a possible
`+0x44 == 0` reader state intact.

Native main-update order independently confirms visibility: `0x00414597`
calls `0x0041EC40`, then `0x004145BB` calls dispatcher `0x00418780`, whose
case 9 reaches `0x00436B40`. Therefore native control/data flow permits zero
at either exact indexed read, conditional on the cited source and state
predicates. No new runtime was authorized, so this is a static reachability
result, not an observation that a particular unchanged scene has those
predicate values.

## M1 provenance intersection

None of the three zero/value sources intersects the established M1 route:

- the initialization source is a constant zero in `0x0041C420`;
- the nonzero first-dword source and record `+0x62` predicate come from the
  separate `LEVEL.RAW` type-`0x23` table populated at
  `0x0046574D-0x0046576A`;
- the late zero is a control-state store in the pre-coordinator fixed-pool
  update, not a copied M1 record, relocated payload, or positive target.

The fact that scene initialization loads and fixes `LEVEL*.DAT` before calling
`0x0041C420` does not create a data-flow edge: the selected first-dword source
is the retained pointer into `0x00599EB0`, and the relevant late writer uses
only fixed-pool fields and constants. The prior M1 selected-record and
positive-target closures contain none of these first-dword stores.

## Result

M2.40 closes with a bounded negative for the required causal edge. A native
reader-time zero is statically reachable through `0x0041BBBA`, but it is
conditional and derives from separate `LEVEL.RAW` plus fixed-pool state. No
M1 20-byte record, relocated payload, or positive target produces either
target word or the zeroing predicate at the declared boundary.
