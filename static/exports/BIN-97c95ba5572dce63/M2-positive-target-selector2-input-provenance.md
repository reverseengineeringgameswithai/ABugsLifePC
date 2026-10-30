# M2 positive-target selector-2 input provenance

## Scope

This is an offline PC-native trace of exact executable SHA-256
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
It reviews only the selector-2 branches of `0x0045A7F0`, using the existing
structured Ghidra export and independent GNU `objdump -d -Mintel`
disassembly. It tests provenance from ID-zero header `0x005B18E0`, retained
range `[0x005A9660,0x005A9DE0)`, or the exact selected `CHARS/FLICK.ALL`
state. No runtime, file mutation, parser work, semantic naming, other resource
family, or cross-port evidence is included.

## Exact caller inputs

The masked-`0x49` caller loads positive target `T` from relocated payload
`+0x1C` at `0x00449E1A`, pushes it first at `0x00449E1F`, and calls
`0x0045A7F0` through thunk `0x00401604` at `0x00449E20`.

The four formal inputs are classified as follows:

| `0x0045A7F0` input | Exact origin on the reviewed M1 route | Selector-2 use | ID-zero/resource provenance |
|---|---|---|---|
| first argument | `T = *(payload + 0x1C)` at `0x00449E1A`; loaded at `0x0045A7FF`, with table base `V = T + 4` at `0x0045A81E` | Count, table, command stream, offsets, packed attributes | Negative. `EXP-20260813-036` establishes a distinct M1 target lineage, and this function has no ID-zero header/range reference. |
| second argument | The third argument of `0x004498F0`, passed through at `0x00449E1E` | Unused: native code has no load from entry-stack slot `[esp+0xF8]` | Negative. It cannot parameterize a reviewed builder because it is not read. |
| third argument | The third argument of `0x004498F0` plus `8 * payload[+0x18]` at `0x00449DED-0x00449E1D`; the exact `0x0044D787` and `0x0044D818` calls pass zero as that caller argument | Low word added to transformed output coordinates at `0x0045AF3A-0x0045AF54` and `0x0045CFF4-0x0045D012` | Negative. Exact origin is the M1 payload byte plus the literal-zero caller input, not selected resource state. |
| fourth argument | Literal address `0x005BDB9C` pushed at `0x00449E0E` | Read at `0x0045A8A9`; its first two dwords feed the local helper/cached-coordinate calculations | Negative. It is a fixed caller-supplied global address, not `0x005B18E0` or the retained range. |

## Selector boundaries and target-derived inputs

The command header is read from the `T`-derived command stream at
`0x0045A8B0-0x0045A8D7`. Its low bit selects the 12-byte item path beginning
at `0x0045A8E4` or the 16-byte item path beginning at `0x0045C79C`.

- On the 12-byte path, `0x0045A946-0x0045A955` enters the reviewed Direct3D
  slice only when renderer selector `0x0059F7F0 == 2`; its slice ends at
  `0x0045C783`.
- On the 16-byte path, `0x0045C7FB-0x0045C80A` enters Direct3D only for the
  same selector value; its inline output paths finish by `0x0045F116` before
  the selector-1 branch at `0x0045F11B`.
- `0x0045A8E9-0x0045A8F6` and `0x0045C7A1-0x0045C7AE` derive the page/list
  input and mode mask solely from command-header bits. The Direct3D arms gate
  that page/list input through `0x005836A4` at `0x0045A95B-0x0045A967` and
  `0x0045C810-0x0045C81C`.
- The first Direct3D slice reads three 16-bit item offsets at
  `0x0045A973`, `0x0045A98E`, and `0x0045A9B0`; the second reads four at
  `0x0045C828`, `0x0045C843`, `0x0045C865`, and `0x0045C884`. Each addresses
  the `V` table. Coordinate pairs and later packed dwords at table-relative
  `+8` supply the inline vertex-record values.

The resulting coordinates are transformed by fixed renderer matrices and
projection/clip state, including `0x0063E888` through `0x0063E8C0`,
`0x00511508`, the `0x00573408/0x0057340A` per-page pair, and the
`0x00861DC4/0x00861DCC/0x00861DE0/0x00861DE4` bounds. Renderer switches such
as `0x005BA120` and `0x004DE030` choose between already-established Direct3D
batch families. Color/scale modifiers such as `0x005BA648`, `0x005BD738`,
and `0x005BA11C` combine with packed target-table bytes after admission.
These globals affect rendering but are not the selected ID-zero header or
retained entry range.

## Inline Direct3D allocation and flush arms

`0x0045A7F0` does not call `0x00405FE0` or `0x00407450`. It allocates and
fills its Direct3D batches inline. The complete allocation/flush set is:

| Allocation entry or pair | Added vertex records | Batch root | Capacity flush |
|---|---:|---|---|
| `0x0045AFF8` / `0x0045B0CF` | 3 | `0x004C410C` / `0x004C4108` | `0x0045B012 -> 0x004058D0` / `0x0045B0E9 -> 0x004056A0`, page/list argument from the command header |
| `0x0045BA24` | 3 | `0x004C410C`, fixed list slot `0x0E` | `0x0045BA36 -> 0x004058D0(0x0E)` |
| `0x0045C080` / `0x0045C14B` | 3 | `0x004C4108` / `0x004C410C` | `0x0045C09A -> 0x004056A0` / `0x0045C165 -> 0x004058D0`, page/list argument from the command header |
| `0x0045D0D2` / `0x0045D204` | 4 | `0x004C410C` / `0x004C4108` | `0x0045D0EC -> 0x004058D0` / `0x0045D21E -> 0x004056A0`, page/list argument from the command header |
| `0x0045DE85` | 4 | `0x004C410C`, fixed list slot `0x0E` | `0x0045DE98 -> 0x004058D0(0x0E)` |
| `0x0045E71F` / `0x0045E85F` | 4 | `0x004C4108` / `0x004C410C` | `0x0045E739 -> 0x004056A0` / `0x0045E879 -> 0x004058D0`, page/list argument from the command header |

The two thunk resolutions are native and exact:
`0x0040127B -> 0x004056A0` and `0x00401618 -> 0x004058D0`.
Capacity counters, index-list cursors, vertex-base pointers, and their updates
all reside beneath the chosen `0x004C4108/0x004C410C` root. Root convergence
is renderer topology, not resource-selection provenance.

The only other selector-2 callees are seven calls each through
`0x00401C26 -> 0x00448230` and `0x00401BD6 -> 0x00464BE0`, plus 24 calls to
`0x004B0240`. Native call-site context shows local coordinate/cached-pair
inputs and numeric conversions. None calls the loader, ID-zero consumers, or
retained-range updater from `EXP-20260812-034/035`.

## Scratch-state distinction

The nearby address `0x005B1ED0` is not ID-zero header `0x005B18E0`.
Selector-2 paths read and populate `0x005B1ED0` cached pairs around
`0x0045B900-0x0045BA01` and `0x0045DE20-0x0045DE62` from command offsets,
`V`-relative values, the caller's fourth argument, and the local helper
chain. It therefore does not provide an untraced alias to the selected
resource header. Coordinate scratch at `0x005BD740` through `0x005BD75C` is
likewise populated from `V`-relative values and transformation results before
the inline batch writes.

## Structured-xref cross-check

For `FUN_0045a7f0`, the structured export reports:

- zero direct references to exact ID-zero header `0x005B18E0`;
- zero direct references into `[0x005A9660,0x005A9DE0)`;
- direct references to the two Direct3D roots at each allocation arm; and
- only callees `0x00401618`, `0x0040127B`, `0x00401C26`, `0x00401BD6`, and
  `0x004B0240`.

Native instruction review independently supplies the indirect input origins,
call arguments, branch bounds, root selection, capacity thresholds, and
target-relative reads that a direct-xref census alone cannot establish.

## Result

Every resource-facing selector-2 input in the reviewed function is accounted
for by the M1 positive target/command stream, exact M1 caller inputs,
renderer transformation and policy state, local scratch derived from those
inputs, or existing Direct3D batch state. No value choosing a batch root,
page/list, flush, index append, vertex base, or emitted vertex record derives
from ID-zero header `0x005B18E0`, retained range
`[0x005A9660,0x005A9DE0)`, or the exact selected `CHARS/FLICK.ALL` state.

This is a complete negative for the M2.35 surface. It does not prove that the
selected resource has no rendered effect, that no wider-lifetime copied edge
exists, or that shared Direct3D submission implies resource identity.
