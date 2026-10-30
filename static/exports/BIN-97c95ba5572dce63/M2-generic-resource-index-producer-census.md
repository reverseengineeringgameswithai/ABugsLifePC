# M2 generic resource-index producer census

## Scope and inputs

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Existing structured export:
  `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`.
- Independent native check: GNU `objdump` 2.44 against the exact derived
  work-copy executable.
- Candidate set: only the eight generic `0x005B18E0 + runtime_index * 4`
  readers retained by `EXP-20260813-035`.
- Route under test: normal `0x0040FFC0` branch through `0x004144C0`, M1
  coordinator `0x0044D430`, dispatcher `0x004498F0`, and positive-target
  consumer `0x0045A7F0`.

No runtime, target mutation, parser/schema work, semantic rename, other
reader/resource family, or cross-port evidence was used.

## Method

1. Rechecked each candidate's structured `0x005B18E0` references.
2. Resolved its exact import-style thunk and every structured/native direct
   call or tail-jump site.
3. Recorded the native register or memory value used as the scaled table
   index.
4. Normalized thunk edges in the structured call graph and intersected the
   candidates with the possible call closures of `0x0040FFC0`,
   `0x004144C0`, `0x0044D430`, `0x004498F0`, and `0x0045A7F0`.
5. Checked native order around the only coordinator-local reader and the
   active-object-list producer used by several earlier readers.

Possible call-graph reachability is not evidence that a conditional branch
executed. Conversely, a table-base reference or an index that might be zero
is not promoted into exact resource-ID-zero evidence.

## Thunk and caller census

| Reader | Thunk | Direct call/tail-jump sites and owning functions |
| --- | --- | --- |
| `0x00436AF0` | `0x00401460` | `0x0041DFAF` in `0x0041DC60` |
| `0x00436B40` | `0x0040198D` | tail jump `0x004187B9` in `0x00418780` |
| `0x00444EF0` | `0x00401ABE` | `0x00445297` in `0x00445020` |
| `0x004467E0` | `0x00401D48` | `0x004401F5` in `0x0043F9E0`; `0x0041C854` in `0x0041C6C0`; `0x0042E92C` in `0x0042E5C0`; `0x0046810D` in `0x00468010` |
| `0x00446870` | `0x004016DB` | `0x00415EFF` in `0x00415E30` |
| `0x00448350` | `0x00401532` | `0x0044D4E6` in `0x0044D430` |
| `0x00456640` | `0x00401069` | `0x0041ED75` in `0x0041EC40` |
| `0x00459620` | `0x00401DAC` | `0x0041ED19` in `0x0041EC40`; `0x004319CB` in `0x004317D0` |

The native whole-image direct-call/tail-jump scan produces exactly these 12
sites. Native thunk instructions independently jump to the eight reader
entry addresses.

## Native index expressions and route classification

| Reader | Native index source | Route intersection | ID-zero/M1 result |
| --- | --- | --- | --- |
| `0x00436AF0` | `I = *(uint32_t *)arg1` at `0x00436AF0-0x00436AF6` | Possible only before the M1 coordinator: `0x004144C0 -> 0x0041EC40 -> 0x0041DC60 -> 0x00436AF0`. `0x0041DC60` receives the current list object and passes the same pointer at `0x0041DFAE-0x0041DFAF`. | The active-list insertion path first requires the object's first dword to be positive at `0x0041EC6A-0x0041EC6E`. No current M1 record/payload value reaches this earlier read; no ID-zero selection is proved. |
| `0x00436B40` | `I0 = *(uint32_t *)0x0059B730` at `0x004372A2-0x004372B7`; `I1 = *(uint32_t *)0x0059B7B4` at `0x00437337-0x0043734C` | Possible pre-coordinator through `0x004144C0 -> 0x00418780`, whose argument selects a tail-jump case. It is absent from the coordinator, selected-record dispatcher, and positive-target closures. | Both persistent index values remain unknown. Neither has a current M1 record/payload producer or an exact zero proof on the declared route. |
| `0x00444EF0` | `I = sign_extend16(arg4)` at `0x00444EF0-0x00444EFA` | Outside the normal update closure; its sole call is in resource-batch initialization `0x00445020`. | The only direct caller pushes literal `0x0B` at `0x0044528E`, so this call selects index 11, not zero, and is not M1-record-derived. |
| `0x004467E0` | `I = *(uint32_t *)arg1` at `0x004467E0-0x004467E6` | Its four callers all pass `&0x0059D6A4`; the normal update can reach it only before the coordinator through `0x004144C0 -> 0x00468010`. | The persistent first dword is not assigned a semantic name and may vary, but no current M1 record/payload value reaches this earlier read and no exact zero is proved. |
| `0x00446870` | `I = *(uint32_t *)arg1` at `0x00446870-0x00446876` | Its sole caller passes `&0x0059D6A4`; the normal update reaches it only before the coordinator through `0x004144C0 -> 0x00415E30`. | Same conservative result as `0x004467E0`: unknown persistent value, no current M1 producer, and no exact zero proof. |
| `0x00448350` | For each `P` in the null-terminated pointer list rooted at `0x0059D7E0`, `I = *(uint32_t *)P` at `0x00448460-0x00448462` and the later repeated header reads | The sole candidate inside `0x0044D430`, called at `0x0044D4E6`. That call precedes M1 root load `0x0044D4FA` and first record test `0x0044D57F`. The normal branch builds the list earlier through `0x0040FFD9 -> 0x004144C0 -> 0x0041EC40`, before `0x0040FFDE -> 0x0044D430`. | List insertion at `0x0041ECF1` follows the positive first-dword gate at `0x0041EC6A-0x0041EC6E`. This is preexisting object state, not a value from the later selected M1 record. The insertion gate does not establish a whole-lifetime invariant, but neither an M1-derived index nor exact ID zero is proved at this reader. |
| `0x00456640` | For each list pointer `P`, `I = *(uint32_t *)P` at `0x00456661-0x00456669` | Called inside pre-coordinator `0x0041EC40` immediately after the list terminator write at `0x0041ED6A`. | Every inserted pointer passed the positive first-dword gate before the immediate call. The reviewed path therefore does not select zero and is earlier than the M1 record route. |
| `0x00459620` | `I = *(uint32_t *)arg2` at `0x00459628-0x0045962B` | The normal-update call at `0x0041ED19` passes the current fixed-pool object before the coordinator. The other call at `0x004319CB` passes fixed global object `0x0059C30C` and is outside the M1 coordinator/selected-record closure. | The `0x0041ED19` call is dominated by the positive first-dword test at `0x0041EC6A-0x0041EC6E`, so that path is nonzero. The other object's index remains unknown but has no declared-route M1 producer or exact zero proof. |

## Reachability and order result

On the normal `0x0040FFC0` branch, the native calls at `0x0040FFD9` and
`0x0040FFDE` order `0x004144C0` before `0x0044D430`. Six candidates are only
possibly reachable in the earlier `0x004144C0` closure. `0x00444EF0` is
outside the normal-update closure. `0x00448350` is the sole candidate in the
coordinator closure, but its call is before the record root and enumeration.

The normalized structured closures of record dispatcher `0x004498F0` and
positive-target consumer `0x0045A7F0` contain none of the eight candidates.
The structured export also records no direct reference from those functions
to the candidate object-index storage identified above. Native call-site and
instruction-order checks independently agree with that graph result.

## Conclusion

All eight generic readers are classified for the declared current-invocation
M1 route. None carries an M1 record/payload-derived value to the generic
header table and proves resource ID zero:

- six are confined to the pre-coordinator update closure;
- one is resource-batch initialization with exact index 11; and
- one is coordinator-local but consumes prebuilt object state before the M1
  root load and record walk.

This is a precise negative for the M2.36 route, not a lifetime-independence
claim. Persistent or copied state across frames, unidentified meanings of the
object/global first dwords, and indirect function-pointer paths remain
unknown. Those possibilities cannot satisfy the M2 gate without a new exact
PC edge and an exact ID-zero proof.
