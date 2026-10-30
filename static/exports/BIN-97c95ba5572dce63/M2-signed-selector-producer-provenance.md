# M2 signed-selector producer provenance

## Scope and inputs

- Exact PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Existing structured export:
  `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`.
- Independent native check: GNU `objdump` 2.44 against the exact derived
  work-copy executable.
- Destination set: only selector words
  `S[i] = *(int16_t *)(0x0059D9C0 + i * 0x30)`, `0 <= i < 20`.
- Route under test: the established M1 record/positive-target route through
  `0x0044D430`, `0x004498F0`, and `0x0045A7F0`.

No runtime, mutation, parser/schema work, semantic rename, other index or
resource family, whole-program indirect search, or cross-port evidence was
used.

## Exact writer census

The selector array lies in the zero-fill tail of the writable `.data`
section: initialized raw data ends at VA `0x004ED400`, while `.data` has
virtual size `0x003A2970` from VA `0x004C1000`. The PE loader therefore gives
the complete array an initial zero state before native code executes.

Structured references across `[0x0059D9C0,0x0059DD80)` identify five
functions whose native instructions can write the selector position. Native
disassembly classifies every write:

| Function | Native write | Selector effect |
| --- | --- | --- |
| `0x0042DDB0` | `0x0042DF4D-0x0042DF64` | Walks the 20 records with stride `0x30`; if record dword `+0x14` is nonzero, clears it and writes zero to selector `+0x00` at `0x0042DF58`. |
| `0x00465030` | `0x00465105-0x0046510F` | Clears `0xF0` dwords beginning at `0x0059D9C0`, exactly `0x3C0 == 20 * 0x30` bytes. |
| `0x00467D70` | `0x00467D73-0x00467D7F` | Clears the same `0xF0` dwords before conditionally rebuilding records. |
| `0x00467E60` | `0x00467ECC-0x00467EE9` | Sole nonzero writer. It loads a signed word from an image-initialized table rooted at `0x004DE9F0` and stores it in the current selector slot. |
| `0x00468BF0` | `0x00468C9A` | Writes zero to the current selector when its associated stream reaches its native zero terminator branch. |

The other exact-range functions are readers of the selector or writers of
neighboring record fields: `0x0043ED60`, `0x0044CA00`, and `0x00468010`.
They do not assign selector `+0x00`. The structured export exposes no direct
write to the selector set from `0x0044D430`, `0x004498F0`, or `0x0045A7F0`.

This is a census of the exact compiler-emitted base/range uses selected by
M2.38. An arbitrary indirect alias or memory corruption is not promoted into
a native producer; the packet deliberately did not widen into a whole-program
indirect search.

## Sole nonzero writer

`0x00467E60` selects slot
`0x0059D9C0 + 0x30 * *(int32_t *)0x00599C74`. Its closing loop increments
that cursor, wraps it after 19, and searches for a zero selector. Both direct
calls pass an element of the fixed 64-record pool
`[0x0059B628,0x0059D728)` with stride `0x84`:

- `0x00467D70` iterates the pool and calls through thunk `0x00401488` at
  `0x00467DF4` after its whole-array clear.
- `0x0041EC40` builds and walks a pointer list of the same pool and calls the
  thunk at `0x0041EDF8` when its local countdown reaches zero.

The writer derives its table index from two bytes behind the pool record's
pointer at `+0x80`. With `B = *(uint8_t *)(P[0x20] + 0x0F)`:

```text
if B != 0:
    K = (B >> 4) + 4 * (B & 0x0F)
else:
    U = *(uint8_t *)(P[0x20] + 0x0E)
    H = *(uint8_t *)(0x0059D9A8 + U) >> 4
    K = 4 * U + H - 1

S[current] = *(int16_t *)(0x004DE9F0 + 4 * K)
```

Native instructions `0x00467ECC` and `0x00467F5F` read the first and second
words of the same four-byte entry. `0x00416100` independently treats this
image region as five four-entry groups rooted at `0x004DE9F0`,
`0x004DEA00`, `0x004DEA10`, `0x004DEA20`, and `0x004DEA30`. Structured xrefs
record reads but no direct write in `[0x004DE9B4,0x004DEA40)`.

## Exact table values and `-103` test

The 20 in-range image entries are:

| `K` | Entry VA | Selector | Second word |
| ---: | --- | ---: | --- |
| 0 | `0x004DE9F0` | 5 | `0x0000` |
| 1 | `0x004DE9F4` | 3 | `0x0000` |
| 2 | `0x004DE9F8` | 8 | `0x0000` |
| 3 | `0x004DE9FC` | 2 | `0x0000` |
| 4 | `0x004DEA00` | 7 | `0x2000` |
| 5 | `0x004DEA04` | 7 | `0x3000` |
| 6 | `0x004DEA08` | 6 | `0x0000` |
| 7 | `0x004DEA0C` | 7 | `0x4000` |
| 8 | `0x004DEA10` | 4 | `0x0000` |
| 9 | `0x004DEA14` | 10 | `0x0000` |
| 10 | `0x004DEA18` | 9 | `0x0000` |
| 11 | `0x004DEA1C` | 1 | `0x0000` |
| 12 | `0x004DEA20` | 6 | `0x4000` |
| 13 | `0x004DEA24` | 6 | `0x2000` |
| 14 | `0x004DEA28` | 6 | `0x1000` |
| 15 | `0x004DEA2C` | 6 | `0x3000` |
| 16 | `0x004DEA30` | 14 | `0x0000` |
| 17 | `0x004DEA34` | 13 | `0x0000` |
| 18 | `0x004DEA38` | 11 | `0x0000` |
| 19 | `0x004DEA3C` | 11 | `0x0000` |

All native in-table nonzero writes are positive selectors in set
`{1,2,3,4,5,6,7,8,9,10,11,13,14}`. None is word `0xFF99` (signed `-103`).

As a conservative image check independent of the 20-entry interpretation,
the lookup formula was exhaustively evaluated against the canonical PE bytes
for:

- all 255 nonzero values of `B`; and
- all 256 values of `U` crossed with all 16 possible high nibbles `H`.

None of those 255 or 4096 over-approximated lookup cases reads `0xFF99`.
The structured export also records no direct write in that wider lookup
envelope. This check does not claim safety for corrupt pointers or arbitrary
indirect memory mutation.

A further native consistency check disfavors `-103`: immediately after the
selector store, `0x00467F13-0x00467F20` sign-extends it and loads
`*(0x004DE9B4 + selector * 4)`. For `-103`, this reads dword
`0x0000000F` at `0x004DE818` and then attempts a word read through that value.
No successful normal producer path is established for such a selector.

## M1 route intersection

The sole normal-update producer intersection occurs before M1 record
enumeration:

```text
0x0040FFD9 -> 0x004144C0
0x00414597 -> 0x0041EC40
0x0041EDF8 -> 0x00467E60
return to 0x0040FFC0
0x0040FFDE -> 0x0044D430
0x0044D4FA loads M1 root 0x005BA7E0
0x0044D57F-0x0044D730 walks M1 20-byte records
0x0044D7A4 -> 0x0044CA00 reads the selector array
```

`0x0044BB70` derives `0x005BA7E0` from the loaded `LEVEL*.DAT` buffer rooted
at `0x005BA240`. By contrast, both selector-producer call sites receive the
separate fixed `0x84`-stride pool. The selected-record dispatcher and exact
positive-target consumer contain neither writer nor selector destination
reference. Thus no current-invocation M1 record, relocated payload, or
positive target produces a selector word. The earlier fixed-pool state may
persist across updates, but no M1-derived copy edge is proved, and persistence
cannot change the nonzero writer's in-table values into `-103`.

## Conclusion

M2.38 is a complete negative at its declared finite boundary:

- four native writer paths only clear selectors to zero;
- the PE image mapping also supplies an initial all-zero state;
- the sole nonzero writer copies positive values from the 20-entry static
  table and has no `-103` case;
- its only normal-update reachability is through pre-coordinator fixed-pool
  state, not the later M1 record or positive-target lineage; and
- the M1 coordinator's post-record `0x0044CA00` call only consumes the array.

The signed-selector candidate is retired. This does not prove whole-program
or cross-frame independence, nor does it authorize another index/resource
family. The M2 causal dependency gate remains unsatisfied.
