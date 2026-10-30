# M2 plant 10 runtime-destination trace

## Scope and identity

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Static anchors: `0x00444C40`, plant 10 caller `0x0044594F–0x004459A1`,
  M1 dispatch `0x00449B61–0x00449E25`
- Runtime evidence: `RUN-GDB-20260812-153150` in
  [[EXP-20260812-021 - Plant10 runtime destination and M1 negative window]]

No PS1 source or finding was consulted. The static interpretation below is
checked against exact executable instructions and the live unchanged PC run.

## Plant-10-specific destination

The call at `0x00445968` supplies resource ID `0x71`. At `0x00444C4F`, the
pair loader multiplies that ID by four. Its ANM pointer store at `0x00444D06`
therefore targets:

```text
0x005B18E0 + 0x71 * 4 = 0x005B1AA4
```

The live post-call stop at `0x0044596D` measured `0x005B1AA4 == 0x006C342B`.
The loader writes the current object index to ANM word `+0x04` before the ALL
consumer and the resulting index to ANM word `+0x06` afterward
(`0x00444D1D`, `0x00444DD9–0x00444DDC`). Live values `66` and `68` therefore
bound two `0x50`-byte entries in the statically established table:

```text
begin = 0x005A9660 + 66 * 0x50 = 0x005AAB00
end   = 0x005A9660 + 68 * 0x50 = 0x005AABA0
```

The two live entry-relative `+0x20` dwords were `0x006C3B3B` and
`0x006C3E57`. They point into the same scene arena after the ANM allocation,
but complete `.ALL` layout and field semantics remain unknown. At
`0x00445988` and the common store at `0x00445AFA`, the caller writes its two
local results to first-entry words `+0x24` and `+0x26`; the combined live
dword at `0x005AAB24` became `0xD7E00218` by `0x00445B01`.

The exact destination claim is consequently address- and offset-based:

- ANM pointer slot `0x005B1AA4`;
- ANM runtime index words `+0x04/+0x06`;
- bounded object-table range `[0x005AAB00, 0x005AABA0)` in this Training run;
- caller-adjusted first-entry words `+0x24/+0x26`.

No semantic structure or field names are promoted.

## Bounded M1 access test

For dispatch `0x49`, `0x00449B61` reads record `+0x10` and switches to the
relocated payload. `0x00449E1A` reads payload `+0x1C`, and `0x00449E20` passes
that target to `0x0045A7F0`. Runtime read watchpoints confirmed these exact
entry values:

| Record | Live record | Live payload | Live target |
|---:|---:|---:|---:|
| 124 | `0x00659F37` | `0x0065B7B3` | `0x0066C273` |
| 125 | `0x00659F4B` | `0x0065B7D3` | `0x0066A2BB` |
| 126 | `0x00659F5F` | `0x0065B7F3` | `0x0066A2BB` |

For each record, hardware read watchpoints on the plant 10 ANM slot and both
bounded entry `+0x20` dwords remained armed from the `0x00449B64` dispatch
stop through the target-renderer return at `0x00449E25`. The post-call
hardware breakpoint won all three times; no watched plant 10 destination was
read. The target arguments at return were the three DAT-relative live targets
above and do not alias the ANM buffer or object-table range.

## Evidence-strength boundary

**Confirmed:** The exact plant 10 call populates the address-based destination
above, and none of its ANM slot or two entry `+0x20` dwords is read in the
three direct M1 dispatch-to-renderer windows.

**Inferred:** The two entry `+0x20` values are pointer-like references into the
loaded pair's arena allocation. Their complete role is not established.

**Unknown:** Other object-entry dwords, copied state, later consumers, and any
indirect relationship to M1 placements. The bounded negative does not resolve
the broader placement/resource identity in `KU-023`.
