# M2 character retained-range first-use static trace

## Provenance and scope

- Executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Review sources: the existing structured Ghidra export and GNU
  `objdump -d -Mintel` against the exact derived work-copy executable.
- Prior runtime correlation: accepted Direct3D substitution experiment
  `EXP-20260812-033` and retained request/range trace `EXP-20260812-034`.
- Experiment: `EXP-20260813-035`.

This report ranks only PC reads reachable after the `0x004679C7`
resource-batch boundary. It distinguishes a proven unindexed ID-zero read from
a reference to table base `0x005B18E0` whose runtime index is unknown. It does
not assign `.ALL` fields, resource identity, or gameplay semantics.

## Xref classification

The exact Ghidra export reports references to table base `0x005B18E0` in
`0x00402DC0`, `0x00436AF0`, `0x00436B40`, `0x00444C40`, `0x00444EF0`,
`0x00445020`, `0x004467E0`, `0x00446870`, `0x00448350`, `0x0044C440`,
`0x00456640`, and `0x00459620`.

- `0x00444C40` and `0x00445020` belong to the initialization chain and are
  before the post-initialization question.
- `0x00436AF0`, `0x00436B40`, `0x00444EF0`, `0x004467E0`, `0x00446870`,
  `0x00448350`, `0x00456640`, and `0x00459620` form addresses as
  `0x005B18E0 + runtime_index * 4`. Their static xrefs establish generic
  per-ID access, not ID zero. No M1-supported Training record supplies a
  proven zero index to these sites in the reviewed flow.
- `0x00402DC0` and `0x0044C440` load `0x005B18E0` directly, without a resource
  index. These are the two accepted post-initialization ID-zero candidates.

This classification resolves the apparent earlier candidates in
`0x004144C0`: calls before `0x00414653` can reach generic indexed readers, but
their indices are not statically bound to zero.

## First direct ID-zero use in the declared update event

The declared event is one normal `0x0040FFC0` update invocation where word
`0x0059A5F0 == 0`:

1. `0x0040FFD9` calls thunk `0x004017B7`, which jumps to `0x004144C0`.
2. `0x004144C0` calls thunk `0x00401019` at `0x00414653`; that thunk jumps to
   `0x00402DC0`.
3. `0x00402DC0` loads the ID-zero slot directly at `0x004032F0`. It selects a
   pointer at header offset `0x08 + selector * 4`, pushes destination index
   zero, and calls thunk `0x00401B86` at `0x004032FE`. A second selected
   pointer can be loaded at `0x0040330E`; the alternate branch directly loads
   header offset `0x88` at `0x004033C5`. Both converge on the same thunk.
4. Thunk `0x00401B86` jumps to `0x00445FF0`. With the caller-supplied third
   argument zero, `0x0044608D-0x004460AC` derives
   `0x005A9660 + destination_index * 0x50`. The function writes the entry
   values at exact addresses including `0x004460D6-0x004460EA`,
   `0x00446137-0x00446160`, and `0x0044622C-0x00446250`.
5. After `0x004144C0` returns, `0x0040FFDE` calls thunk `0x00401B81`, which
   jumps to M1 coordinator `0x0044D430`.

Thus, in this exact normal branch, `0x00402DC0` is the first proven direct
ID-zero reader and `0x00445FF0` is its immediate retained-range updater. The
claim is address- and branch-bounded: it does not promote any earlier generic
indexed reference to ID zero, and it does not cover the alternate
`0x0059A5F0 != 0` branch that skips `0x004144C0`.

## Nearest M1-side retained-range consumer

`0x0044D430` conditionally calls thunk `0x0040185C` at `0x0044D4BC` when
bit `0x10` of `0x005C5EDC` is clear. The thunk jumps to `0x0044C440`.

`0x0044C440` is an exact downstream consumer of both ID-zero structures:

- `0x0044C635` directly loads slot `0x005B18E0` and reads header words
  `+0x04/+0x06` as the shared-entry start/end bounds;
- `0x0044C64F` derives `0x005A9660 + start * 0x50`;
- the loop reads entry words/dwords through `0x0044C8A5`, advances by exact
  stride `0x50`, and compares against the ID-zero end bound;
- `0x0044C898-0x0044C899` passes the current shared-entry pointer to thunk
  `0x00401078`, whose target is `0x0044F8E0`.

This makes `0x0044C440` the nearest accepted M1-coordinator-side consumer,
but not an M1-record-dependent consumer. Native order is decisive:

- the `0x0044C440` call occurs at `0x0044D4BC`;
- only afterward does `0x0044D430` load record-list root `0x005BA7E0` at
  `0x0044D4FA`;
- the first 20-byte-record sentinel test is at `0x0044D57F`, followed by the
  record selection loop;
- selected records later reach `0x004498F0`; on the established `0x49` path,
  `0x00449E1A` reads payload `+0x1C` and `0x00449E20` calls thunk
  `0x00401604` to positive-target consumer `0x0045A7F0`.

The structured export independently shows no direct reference to
`0x005B18E0` or `[0x005A9660,0x005A9DE0)` in `0x0044D430`, `0x004498F0`, or
`0x0045A7F0`. None calls `0x00402DC0` or `0x00445FF0`; `0x0044D430` reaches
`0x0044C440` only through the earlier no-argument call described above.

## Bounded result

Confirmed for this executable and one normal `0x0040FFC0` update invocation:

- first proven unindexed post-initialization ID-zero reader:
  `0x00402DC0` at `0x004032F0`;
- immediate shared-range updater: `0x00445FF0`, rooted at `0x005A9660` with
  exact stride `0x50` and caller-supplied starting destination index zero;
- nearest M1-coordinator-side retained-range reader: `0x0044C440`, called at
  `0x0044D4BC` before the M1 record root is loaded or any 20-byte record is
  enumerated;
- no exact direct data flow from an M1-supported Training record or positive
  payload target to the first ID-zero use exists in this declared event.

The negative is limited to direct PC data flow and this branch/order window.
It does not rule out persistent copied state, a different update branch, a
later event, an indirect resource selector outside the reviewed path, or a
shared-entry contribution to the M2.20 rendered difference.

## Precise next discriminator

First extend the static trace from the exact shared-entry argument at
`0x0044C898` into `0x0044F8E0`, starting with its read of entry `+0x20`, and
compare that address lineage with the exact positive-target argument passed at
`0x00449E20`. If static lineage cannot distinguish them, a future approved
read-only natural-pause run should bracket one normal `0x0040FFC0` invocation,
capture only the exact shared-entry pointer at `0x0044C898` and one established
M1 record/payload call, and test address equality or an explicit copy edge.
Do not use `0x0044D794/0x0044D79A`, widen to unrelated entries, or modify
target state.
