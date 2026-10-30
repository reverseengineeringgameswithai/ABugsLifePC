# M2 residual fixed-pool index reader disposition

## Scope and evidence boundary

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact objects: fixed-pool slot 25 first dword `0x0059C30C` and slot 63
  first dword `0x0059D6A4` in pool `[0x0059B628,0x0059D728)`, stride
  `0x84`.
- Exact consumers: slot 25 through `0x004319CB -> 0x00459620`; slot 63
  through the five fixed-pointer calls at `0x00415EFF`, `0x0041C854`,
  `0x0042E92C`, `0x004401F5`, and `0x0046810D` to
  `0x004467E0/0x00446870`.
- Static sources: the existing Ghidra evidence export, independent GNU
  objdump 2.46 disassembly of the exact work-copy executable, and the complete
  first-dword writer census from M2.40.

This was an offline PC-native analysis. It did not launch or mutate the game,
inspect another pool object or resource family, extend a parser or schema,
assign field semantics, perform a broad indirect search, or consult PS1
evidence.

## Reused complete writer result

M2.40 proves that every first dword in this fixed pool has the same complete
bounded store classes:

1. whole-pool zero at `0x0041C430`;
2. nonzero-gated retained-source byte copy at `0x0041BD24`; and
3. conditional mode-2 removal zero at `0x0041BBBA` when record `+0x62 == 0`.

Slots 25 and 63 correspond to retained source records `0x0059A16C` and
`0x0059A594`. Their initial nonzero first-dword values and the removal
predicate originate in the separate `LEVEL.RAW` type-`0x23` source table,
not the M1 `LEVEL*.DAT` 20-byte record, relocated payload, or positive target.

## Slot 25: `0x0059C30C -> 0x00459620`

### Exact call gates and order

Dispatcher `0x00418780` reaches `0x004317D0` only in case 1. The exact call
site is not controlled by the earlier `0x00431804` test highlighted in the
M2.41 premise. Native instructions reload slot 25 `+0x5C` at `0x004318E4`,
require bit `0x4000` to be clear at `0x004318EA-0x004318F3`, and require the
three-bit counter byte `0x00599AB0` to equal zero at
`0x004318F9-0x00431900`. A positive route count from the structure reached
through `0x005C5864` is also required at `0x00431912-0x0043191B`. The
function then passes fixed `0x0059C30C` at `0x00431983` and calls the reader
at `0x004319CB`.

The counter is initialized to zero at `0x0042E802` and advanced modulo eight
at `0x00418E8A-0x00418EB0`, at the end of `0x004144C0`; it is not an M1
record or payload field. The dispatcher selector `0x00861C84` is established
as scene/mode state before scene initialization and is only read by the
dispatcher in this update. The direct writer/read closure for
`0x005C5864` is initialization/scene-loader state; the selected call contains
no load from M1 root `0x005BA7E0`, an M1 20-byte record, relocated payload,
or positive target.

Main-update order is exact. `0x004144C0` calls fixed-pool update
`0x0041EC40` at `0x00414597`, then the dispatcher at `0x004145BB`. The outer
normal branch calls M1 coordinator `0x0044D430` only after `0x004144C0`
returns. Current-invocation M1 state therefore cannot produce this call's
index or gates.

### Reader-time zero

Every `0x0041EC40` pass clears record bit `0x4000` at
`0x0041EC5C-0x0041EC66`, then rejects a zero first dword at
`0x0041EC6A-0x0041EC6E` without calling the copier or restoring the flag.
Consequently:

- initial unpopulated zero retains a clear `0x4000` bit and can pass the
  slot-25 call gate; and
- a record zeroed late by `0x0041BBBA` remains blocked in that same update
  because list insertion already set `0x4000`, but the next update clears the
  flag, preserves the zero through the positive first-dword rejection, and
  can then reach the reader.

This corrects, rather than silently extends, the premise in
`EXP-20260813-057`: the earlier `0x00431804` test does not govern the actual
call; the later gate at `0x004318F3` does.

`0x00459628-0x00459632` loads the first dword as `I`, selects table entry
`0x005B18E0 + I * 4`, dereferences the header pointer, and tests its first
word. Exact `I == 0` therefore selects the ID-zero header. The independently
validated ID-zero header records retained indices `[0,24)`, so its first word
is zero; `0x00459620` returns zero without entering its positive header-start
branch. This is an exact ID-zero lookup outcome, not proof of a named visible
effect.

## Slot 63: five fixed-pointer calls

Both readers use the first dword with no range or nonzero check:
`0x004467E4-0x004467ED` and `0x00446874-0x0044687D` select
`0x005B18E0 + I * 4`; later loads at `0x0044681E-0x0044682C` and
`0x004468AE-0x004468BC` repeat the same selection. They read header `+0x04`
as a retained-entry index. For exact `I == 0`, the previously validated
ID-zero end index is 24.

| Fixed call | Exact gate | Order / zero disposition |
|---:|---|---|
| `0x00415EFF -> 0x00446870` | `0x00415E50` requires slot first dword `== 0x23`; input transition, prior-input, slot state, distance, and global state gates also apply; `0x00415F04` sets `0x0059D9A0` bit `0x80` after the call | Normal update before `0x0041EC40`; zero is categorically excluded |
| `0x0042E92C -> 0x004467E0` | `0x0042E91A-0x0042E925` requires slot first dword `== 0x23` | Scene initialization; zero is categorically excluded |
| `0x0041C854 -> 0x004467E0` | For nonzero fourth argument, `0x0041C6C0` branches directly to the true local route; `0x0041C846` then requires `0x0059D9A0` bit `0x80`, and `0x0041C864` clears that state after the call | State-gated; no slot first-dword or `+0x5C` test excludes zero |
| `0x004401F5 -> 0x004467E0` | One `0x0043F9E0` state arm culminates in `0x004401CD` testing bit `0x80` of `[0x0059D910 + 0x90]`, the same `0x0059D9A0` byte; the call clears the bit afterward | Called from `0x00414578`, before pool update; a prior-update zero is not excluded |
| `0x0046810D -> 0x004467E0` | Event entry/index tests at `0x004680C9`, `0x004680D3`, and `0x004680DE`, followed by `0x004680FF` bit-`0x80` test; `0x0046811D` clears the bit after the call | Called from `0x004145A6`, after `0x0041EC40`; a same-update late zero is not excluded |

The bit-`0x80` state is paired control state, not the slot first dword. The
explicit `I == 0x23` path at `0x00415EFF` sets it; each selected state-gated
consumer clears it after use. Mode-2 removal `0x0041B9F0` has no reference to
`0x0059D9A0`, so its first-dword zero does not itself invalidate the final
state gate. Native control/data flow therefore permits slot-63 zero at each of
the three state-gated readers, conditional on their cited independent route
state. This is static reachability, not an observation that an unchanged
scene realizes every predicate combination.

## M1 provenance intersection

The slot values, zero writer, and direct predicates do not supply the missing
M1 edge:

- first-dword population and record `+0x62` come from the separate
  `LEVEL.RAW` type-`0x23` table;
- bit `0x4000` is fixed-pool active-list state;
- `0x00599AB0` is an initialization/reset and modulo-eight update counter;
- `0x00861C84`, `0x0059D9A0`, the event entries, player/position state, and
  the route structure at `0x005C5864` are established update/scene state;
- all selected normal-update calls occur inside `0x004144C0`, before outer
  call `0x0044D430` loads and walks the M1 record root.

No selected function or exact gate closure loads an M1 20-byte record,
relocated payload, or positive target, and the established M1
selected-record/positive-target closure contains none of the fixed-pool
first-dword stores or these fixed-pointer calls. Same-scene or same-frame
coexistence is not promoted into a data-flow dependency.

## Result

M2.41 closes with a bounded causal negative. Slot 25 zero is statically
reader-reachable on an unpopulated record or one update after conditional
removal; it selects the ID-zero header and takes `0x00459620`'s zero-return
arm. Slot 63 zero is excluded at two explicit `I == 0x23` calls but remains
statically reachable at the three state-gated calls, which use the ID-zero
retained end index. None of the proven values or direct enabling predicates
derives from the M1 record, relocated payload, or positive-target route.
