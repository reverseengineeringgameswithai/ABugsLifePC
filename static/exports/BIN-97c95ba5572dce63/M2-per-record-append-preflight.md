# M2 per-record Direct3D append preflight

## Provenance and scope

- Executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Sources: exact native GNU `objdump -d -Mintel` disassembly, the checked
  M2.27 family/reset proof, and `EXP-20260813-041`'s exact 168-call plan and
  124-record candidate set.
- Roadmap packet: M2.29.

This PC-native preflight maps every counter write and no-append return in the
two selected builders. It designs a record-level count discriminator only for
M2.28's exact candidate set. It assigns no field, asset, primitive, identity,
or pixel meaning; retains no file or batch payload bytes; creates no `.ALL`
parser; and uses no other resource family or PS1 evidence.

## Exact append boundaries

Both builders perform all admission tests before their selected counter
writes. Once the vertex-count write below executes, control reaches the
function's ordinary epilogue without another no-append branch.

| Builder/form | Family | Index-count writes | Shared vertex-count write | Completed delta |
|---|---|---|---|---|
| `0x00405FE0` / `0x3C` | root through `0x004C410C` | `0x00406786`, `0x004067AF`, `0x004067D8`, `0x00406804`, `0x0040682A`, `0x00406858` | `0x004069A1` | +4 vertices, +6 indices |
| `0x00405FE0` / `0x3C` | root through `0x004C4108` | `0x004068BB`, `0x004068E4`, `0x0040690D`, `0x00406939`, `0x0040695F`, `0x0040698D` | `0x004069A1` | +4 vertices, +6 indices |
| `0x00407450` / `0x34` | root through `0x004C410C` | `0x004079E6`, `0x00407A0F`, `0x00407A37` | `0x00407B00` | +3 vertices, +3 indices |
| `0x00407450` / `0x34` | root through `0x004C4108` | `0x00407A9C`, `0x00407AC5`, `0x00407AED` | `0x00407B00` | +3 vertices, +3 indices |

The `0x00405FE0` family branches merge with the chosen root in `ECX` before
the `add word [ecx+edi],4` at `0x004069A1`. The `0x00407450` branches likewise
merge with the chosen root in `EAX` before `add word [eax+edi],3` at
`0x00407B00`. These exact vertex-count writes are therefore positive append
markers, while a completed call with zero counter delta is a no-append result.

The only reachable in-call resets remain the M2.27-proven flush paths:

- root `0x004C4108`: marker stop `0x00405838`, index reset `0x0040583E`,
  vertex reset `0x0040584D`;
- root `0x004C410C`: marker stop `0x004059AB`, index reset `0x004059B7`,
  vertex reset `0x004059C8`.

The marker stop precedes both resets, so a pre-reset count segment plus a
post-reset segment accounts for every reachable change. A decrease without
that marker is a contradiction.

## Exact no-append returns

`0x00405FE0` has one return at `0x0040702F`:

- entry checks at `0x00405FFF` and `0x0040600F` branch directly to epilogue
  `0x00407024`;
- later admission branches at `0x004064E4`, `0x00406502`, `0x00406533`,
  `0x0040654E`, `0x004065B0`, `0x004065E7`, `0x00406636`, `0x00406660`,
  `0x00406672`, `0x0040668B`, `0x004066A4`, and `0x004066BD` branch to
  cleanup `0x00407012`, then the same epilogue.

All those edges precede the first selected counter write. `0x00407450` has an
early no-append return at `0x00407469` when the check at `0x00407458` fails.
Its later admission branches at `0x0040784B`, `0x00407861`, `0x00407886`,
`0x0040789C`, `0x004078D4`, `0x00407917`, and `0x00407936` reach shared
epilogue `0x00407E6F` and return `0x00407E8C`, also before the first selected
counter write.

## Fail-closed metadata-only state machine

Harness 1.4.0/spec schema 5 adds the purpose-specific `record_outcome` mode.
It reuses only the three M2.27-proven data watches:

1. selector `0x0059F7F0`, filtered to exact pre-call stops
   `0x0044F951/0x0045026C` and caller return `0x0044C89E`;
2. flush marker `0x004C4118`, filtered to `0x00405838/0x004059AB`;
3. entry-post header `0x005B18E0`, filtered to `0x0044C8AB`.

At each exact pre-call stop the controller first closes the preceding call by
reading only allowlisted roots, vertex pointers, and 16-bit counters. It then
checks the entry lattice, saved entry index, exact record pointer/order/form,
and snapshots only the next call's counter metadata. Entry-post closes the
last call. The flush watch records the pre-reset metadata segment and resets
the controller's expected starting counts to zero. No source record, vertex,
index, or other payload byte is read or placed in a result.

The exact 168-call plan from `EXP-20260813-041` is required in full, but only
the 124 M2.28 candidate offsets may appear in retained outcome results. Each
candidate result must be exactly one of:

- no append: `(vertex,index) = (0,0)`;
- form `0x3C` append: `(4,6)` in root `0x004C4108`, page 16;
- form `0x34` append: `(3,3)` in root `0x004C4108`, page 16.

The arm fails closed on an unexpected caller, PC, entry, record pointer,
offset, form, order, root, page, pointer, count, delta, unmarked decrease,
flush, signal, cleanup, detach, survival, renderer gate, exact load, or
`NextLife` receipt. It uses no execution breakpoint and never arms quarantined
points `0x0044C898`, `0x0044D794`, or `0x0044D79A`.

## Static conclusion

**Confirmed:** exact counter writes and all no-append return edges support a
complete record-level append/non-append discriminator using only the existing
three safe data-watch boundaries. The static design is therefore sound for a
fresh matched control/replacement/control capture under the user's explicit
M2.29 authority. Runtime outcomes, individual replacement-local records, and
visible causality remain unknown until accepted arms are collected and
reconciled.
