---
type: experiment
id: EXP-20260813-058
date: 2026-08-13
question: Can fixed-pool slots 25 or 63 hold zero at their exact fixed-pointer generic-header reads, and does either value or enabling predicate derive from the established M1 route?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora 44; offline PC-native static analysis
environment_version: GNU objdump 2.46-3.fc44; existing Ghidra structured evidence export
working_directory: /home/dev/ABLPC
configuration: Exact-hash work-copy executable; fixed-pool slots 25 and 63 and their seven declared fixed-pointer call paths only; M2.40 writer set reused; no runtime, mutation, parser/schema work, semantics, other pool object/reader/resource family, broad indirect search, or cross-port evidence
artifacts:
  - static/exports/BIN-97c95ba5572dce63/M2-residual-fixed-pool-index-reader-disposition.md
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
addresses:
  - 0x00414578
  - 0x00414592
  - 0x00414597
  - 0x004145A6
  - 0x004145BB
  - 0x00415E50
  - 0x00415EFF
  - 0x0041C854
  - 0x0042E92C
  - 0x004318E4
  - 0x004318F3
  - 0x004318F9
  - 0x004319CB
  - 0x004401F5
  - 0x004467E4
  - 0x00446874
  - 0x00459628
  - 0x0045962B
  - 0x004680FF
  - 0x0046810D
  - 0x0059C30C
  - 0x0059D6A4
  - 0x005B18E0
file_offsets: []
result: slots-25-and-63-reader-time-zero-statically-reachable-but-m1-negative
created: 2026-08-13
updated: 2026-08-13
tags:
  - re/experiment
  - re/resources
  - re/static
  - re/provenance
---

# EXP-20260813-058 - Residual fixed-pool index reader disposition

## Question

Can fixed-pool slot 25 first dword `0x0059C30C` or slot 63 first dword
`0x0059D6A4` equal zero at their exact fixed-pointer generic-header reads, and
does either value or enabling predicate derive from the established M1 record,
relocated payload, or positive-target route?

## Method

I independently rehashed the exact work-copy executable, reused rather than
reopened M2.40's complete first-dword writer census, disassembled the slot-25
caller and reader, classified all five direct slot-63 calls and both reader
functions, and fixed their order in the normal update. I then followed only
the direct call gates needed to decide zero visibility and compared their
value/predicate inputs with the established M1 closures.

No game process was launched or changed. No executable, asset, runtime state,
parser, schema, or tool was modified. No other pool object, list/current-object
reader, resource family, broad indirect search, semantic name, or PS1 evidence
was introduced.

## Observed

### Slot 25

The actual call gate is later than the flag test emphasized by the selecting
audit. `0x004318E4-0x004318F3` requires slot 25 `+0x5C` bit `0x4000` to be
clear, and `0x004318F9-0x00431900` requires modulo-eight counter
`0x00599AB0 == 0`; dispatcher case 1 and a positive route count also apply.
The fixed pointer is pushed at `0x00431983` and read through
`0x004319CB -> 0x00459620`.

`0x0041EC40` clears `0x4000` on every record before its positive-first-dword
test. Initial unpopulated zero therefore passes the later call gate. A
same-update conditional removal zero remains blocked because `0x4000` was
already set, but the next update clears that flag, preserves zero through the
positive gate, and can reach the reader.

At `0x00459628-0x00459632`, exact zero selects ID-zero table entry
`0x005B18E0`. The previously validated ID-zero header starts at retained index
zero, so its first word is zero and the function takes its zero-return arm.

### Slot 63

Two calls categorically exclude zero: `0x00415E50` gates the
`0x00415EFF -> 0x00446870` call on `I == 0x23`, and
`0x0042E91A-0x0042E925` applies the same test before
`0x0042E92C -> 0x004467E0`.

Three calls do not test the slot value:

- `0x0041C854` is reached when `0x0041C6C0` receives a nonzero fourth
  argument and `0x0059D9A0` bit `0x80` is set;
- `0x004401F5` is reached through a state arm in `0x0043F9E0` whose final
  gate at `0x004401CD` tests the same bit; and
- `0x0046810D` requires the exact event entry/index tests at
  `0x004680C9/0x004680D3/0x004680DE` plus the bit test at `0x004680FF`.

Both readers use `I` directly in `0x005B18E0 + I * 4` and then use header
`+0x04`. Exact zero therefore selects the validated ID-zero retained end
index 24. The bit-`0x80` state is set after the explicit `I == 0x23` call and
cleared after each state-gated consumer. Conditional removal does not write
that state. Native control/data flow therefore does not exclude zero at the
three state-gated calls, conditional on their cited route state.

### Update and M1 order

The normal update calls `0x0043F9E0` at `0x00414578`, `0x00415E30` at
`0x00414592`, pool update `0x0041EC40` at `0x00414597`, and `0x00468010` at
`0x004145A6`, before dispatcher `0x00418780` at `0x004145BB`. The outer
`0x0040FFC0` branch calls M1 coordinator `0x0044D430` only after this entire
update returns.

The slot values/removal predicate originate in separate `LEVEL.RAW`
type-`0x23` state. The direct gates are fixed-pool flags, initialized/update
counters, scene/mode state, player/position state, and event entries. No
selected closure loads an M1 20-byte record, relocated payload, or positive
target, and the established M1 closure contains none of these stores/calls.

## Confirmed

- Slot 25 zero is statically reader-reachable initially or one update after
  conditional removal, conditional on the exact dispatcher/counter/route
  gates.
- Slot 25 exact zero selects the ID-zero header and causes
  `0x00459620` to take its zero-return arm because that header starts at zero.
- Slot 63 zero is excluded at two explicit `I == 0x23` calls and statically
  reachable at three independently state-gated calls.
- Slot 63 exact zero selects the ID-zero header's retained end index at the
  two readers.
- No proven value or direct enabling predicate derives from the M1
  record/payload/positive-target route.

## Inferred

The state-gated slot-63 zero paths are real native ID-zero possibilities, not
evidence that a named unchanged scene realizes every predicate combination.
The slot-25 zero return is an exact lookup outcome, not a semantic or visible
effect claim.

## Contradictions and limitations

- `EXP-20260813-057` correctly selected slot 25 but cited an earlier
  `0x00431804` flag test as if it constrained the later call. The actual call
  reloads `+0x5C` and requires `0x4000` clear at `0x004318F3`. This packet
  records the correction explicitly.
- Static reachability does not prove a shipped scene realizes each combined
  route predicate. That limitation does not preserve an M1 candidate: the
  proven value and direct gate sources remain outside the M1 route.
- No semantic names are assigned to the pool objects, route structure, event
  entries, or state bits.

## Result

M2.41 is complete with a bounded causal negative. Both residual objects can
select ID zero at their declared reader boundaries under exact static gates,
but neither selection is produced or enabled by the established M1 record,
relocated payload, or positive-target route.

## Follow-up

Do not defer or close M2 on the worker's own authority. Advance exactly to an
independent fresh-context M2.42 hard-truth disposition audit. That audit must
attempt to falsify this packet's exhaustiveness and must either accept the
evidence-backed M2 disposition or name one exact bounded PC-native successor.
No technical family is widened by this handoff.
