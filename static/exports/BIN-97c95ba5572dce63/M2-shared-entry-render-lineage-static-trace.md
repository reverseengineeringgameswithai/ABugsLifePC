# M2 shared-entry render-lineage static trace

> [!IMPORTANT] M2.26 correction
> `EXP-20260813-039` proves that the “hardware output” label used below was
> wrong: selector 1 is native software and owns the `0x80`-stride arena;
> selector 2 is Direct3D and uses separate batch storage through
> `0x00405FE0/0x00407450`. The address/topology convergence remains exact for
> the software branch. See `M2-direct3d-renderer-path-reconciliation.md`.

## Provenance and scope

- Executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Review sources: the existing structured Ghidra export and GNU
  `objdump -d -Mintel` against the exact unchanged derived work-copy
  executable.
- Prior runtime correlation: accepted Direct3D character substitution
  `EXP-20260812-033`, character request/range trace `EXP-20260812-034`, and
  M1 target substitution evidence `EXP-20260812-009/010`.
- Experiment: `EXP-20260813-036`.

This report traces one symbolic current retained entry from the exact call at
`0x0044C898` and compares that address lineage with the masked-dispatch-`0x49`
positive-target argument at `0x00449E20`. It covers the hardware submission
branch selected by the established Direct3D baseline. It does not assign
`.ALL` fields, source identity, primitive names, or a complete rendering
subsystem.

## Declared normal-update path

In the normal `0x0040FFC0` branch retained by `EXP-20260813-035`, coordinator
`0x0044D430` calls `0x0044C440` at `0x0044D4BC` before loading the M1 record
root at `0x0044D4FA` and enumerating records from `0x0044D57F`.

`0x0044C440` reads ID-zero bounds directly from slot `0x005B18E0`, derives
the current entry as `0x005A9660 + index * 0x50`, and tests entry word `+0x2E`
at `0x0044C661`. For the exact unchanged M2.20 file, descriptors 0-23 carry
the already recorded comparison value `1`; `0x00448117` copies that value to
entry `+0x2E`. Therefore every retained index in `[0,24)` takes the value-1
branch when the outer `0x0044C440` conditions are satisfied. The trace below
uses one symbolic current entry `E`; it does not reinterpret or enumerate
unrelated resources.

At `0x0044C898`, native code pushes `E` and calls thunk `0x00401078`; the
thunk target is `0x0044F8E0`. Later in the same coordinator invocation,
selected M1 records can reach `0x004498F0`, which reads positive-target
argument `T` from payload `+0x1C` at `0x00449E1A` and calls thunk
`0x00401604` at `0x00449E20`; its target is `0x0045A7F0`.

## Retained-entry input lineage

The exact address-forming chain is:

1. `0x004480F4-0x004480F6` loads the current scene-arena cursor and stores it
   at destination entry `+0x20` while the exact selected `.ALL` file is first
   consumed.
2. `0x0044C898-0x0044C899` passes current retained entry `E` to
   `0x0044F8E0`.
3. `0x0044F8E0` loads the argument and `0x0044F8EA` performs the first
   dereference, `S = *(E + 0x20)`.
4. `0x0044F8EE` reads byte `S + 3`. Masked values `0x34` and `0x3C` select
   two bounded record walks. The function forms only stream-relative
   addresses such as `S + 4`, `S + 0x0C`, `S + 0x14`, and `S + 0x1C`.
5. The selected paths advance `S` by exact strides `0x24` or `0x30` at
   `0x004509BC-0x004509D7` and `0x00450236-0x0045024E`. A zero byte at
   `S + 3` reaches the word test at `0x004509E6`; word value `1` advances
   four bytes and resumes, while other values return.

No instruction in this lineage forms an address from the M1 target argument,
the M1 12-byte table base, or an M1 command-item offset.

## M1 positive-target input lineage

The established masked-dispatch-`0x49` chain is structurally different:

1. `0x00449E1A` loads `T` from selected payload `+0x1C`; `0x00449E20`
   passes it as the first argument to `0x0045A7F0`.
2. `0x0045A7FF` loads `T`; `0x0045A81E` forms table base `V = T + 4`.
3. `0x0045A82E` reads signed count `n = *T`. On the bounded nonnegative path,
   `0x0045A897-0x0045A89E` forms command pointer `C = V + n * 12`.
4. The command loop begins with the `0xFFFF` test at `0x0045A8B0` and uses
   unsigned 16-bit command-item offsets to form reads relative to `V`.

The retained exact target reports independently show only even command modes
for the two M1 substitution anchors: `0x60/0x8062/0x8064/0x8066` at `0x111E4`
and `0x60/0x8062/0x8064` at `0x1319C`. Native branch
`0x0045A8D1-0x0045A8D7` routes even modes into the output path containing the
representative hardware allocator sequences below. This is mode parity and
control-flow evidence only; no mode meaning is assigned.

The structured export records no call between `0x0044F8E0` and
`0x0045A7F0`, no ID-zero slot/range reference in `0x0045A7F0`, and no M1
target argument reference in `0x0044F8E0`. Static evidence therefore exposes
no copy or address-forming edge between source pointers `S` and `T`. It does
not, by itself, claim that every possible runtime numeric value of those
pointers is unequal.

## Exact hardware-output convergence

The two source walks converge after their independent record decoding. The
structured Ghidra export and native instructions independently agree on the
following shared hardware structures.

### Transform scratch

Both functions write and read the exact global range
`0x005BD740-0x005BD75C` while applying the same matrix globals rooted at
`0x0063E888`. This is sequentially reused scratch, not evidence that either
source pointer aliases the scratch addresses.

### Shared submission arena

Both functions test the same current count `0x008082C8` against capacity
`0x0081C138`, then form an output address with exact stride `0x80`:

```text
output = *(0x0081BC28) + *(0x008082C8) * 0x80
*(0x008082C8) += 1
```

For `0x0044F8E0`, representative native allocator sequences are
`0x0045005B-0x0045006F` and `0x00450838-0x0045084C`. For the bounded positive
path in `0x0045A7F0`, representative sequences are
`0x0045F974-0x0045F987` and `0x0045FFB8-0x0045FFCC`.

Both functions populate coordinate/color-like output positions, but those
field interpretations remain inferred. The structural facts are exact: both
write within one `0x80`-byte record, store a prior-list pointer at output
`+0x70`, and store a mode/flag word at output `+0x74`.

### Shared list-head topology

`0x0044F8E0` combines a depth index with the list-head array reached through
pointer global `0x004E8CC8`. It reads a per-depth word at `0x005C0410`, links
the previous head at output `+0x70`, and installs the new record at
`0x0045020E-0x00450223` or `0x00450981-0x004509A9`.

`0x0045A7F0` loads the same list-head root at `0x0045F7A4`, adds its
caller-supplied third-argument offset and derived depth at
`0x0045F7B6-0x0045F893`, and links a generated record through output `+0x70`
at `0x0045FFAC-0x0045FFB1` or `0x00460219-0x0046022E`. Exact list-head
equality for a particular pair of emissions depends on the M1 caller offset
and the separately derived depths; shared topology is not same-bucket proof.

## Bounded result

Confirmed for this executable and the declared normal-update/hardware branch:

- the retained-entry source is `S = *(E + 0x20)` and is walked as `0x24`- or
  `0x30`-stride records selected by byte `S + 3`;
- the M1 source is positive target `T`, with table base `T + 4`, command
  pointer `T + 4 + n * 12`, and table reads formed from command-item offsets;
- there is no direct source-pointer copy, call, or address-forming edge between
  those two input lineages;
- both hardware paths converge on the same transform scratch, capacity/count,
  `0x80`-stride output arena, output link/flag offsets, and list-head root.

This is a shared renderer-output bridge, not an M1 placement-to-resource
identity. `EXP-20260812-033` independently proves that changing the exact
ID-zero-loaded file changes a bounded rendered region, while
`EXP-20260812-009/010` independently tie the selected M1 target path to
visible placement-local output. Those dynamic anchors support the two inputs'
render relevance but do not make one input select the other.

## Precise next discriminator

Localize the already accepted `FLICK.ALL`/`FLICKD.ALL` byte differences only
across the 24 exact retained stream intervals supplied through entry `+0x20`.
For each changed interval, retain only bytes reached by the demonstrated
`0x0044F8E0` `0x34`/`0x3C` walk and its terminator rules. Stop after selecting
one exact changed retained stream or recording that multiple streams remain.
Do not create a general `.ALL` parser, assign field/asset/primitive semantics,
scan another resource family, consult PS1, or use the quarantined debugger
region.
