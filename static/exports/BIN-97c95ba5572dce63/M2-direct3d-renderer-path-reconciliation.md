# M2 Direct3D renderer-path reconciliation

## Provenance and scope

- Executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Review sources: the checked structured Ghidra export and GNU
  `objdump -d -Mintel` against the exact unchanged derived work-copy
  executable.
- Prior evidence: `EXP-20260813-036` through `EXP-20260813-038`, plus the
  accepted Direct3D and visible-result anchors in `EXP-20260812-007/033`.
- Experiment: `EXP-20260813-039`.

This is a static, PC-native reconciliation of the renderer selector, the
conditional `0x80`-stride arena, and the nearest alternate calls from
`0x0044F8E0`. No runtime instrumentation, protected payload inspection,
cross-port evidence, `.ALL` parsing, or field/asset identity assignment was
used.

## Exact selector mapping

At `0x00420022-0x0042002E`, `0x0041F990` converts global `0x00573FF4` into
renderer selector `0x0059F7F0`:

| `0x00573FF4` | `0x0059F7F0` | diagnostic selected at `0x00420034-0x00420044` |
|---:|---:|---|
| nonzero | `1` | `native software render` (`0x004C9210`) |
| zero | `2` | `Direct3d render` (`0x004C91FC`) |

The calculation is native `neg`, `sbb`, then `add eax,2`; the diagnostic
branch independently verifies the value meanings. This corrects the earlier
unproven convention that called selector-1 arena writers a hardware path.

The main initialization dispatch at `0x0043DB15-0x0043DB31` and restart
dispatch at `0x00421358-0x00421374` use the same mapping:

- selector `1` calls thunk `0x004014E7 -> 0x0049C520`;
- selector `2` calls thunk `0x00401965 -> 0x004119E0`.

`0x004119E0` begins with the exact diagnostic
`INIT : Starting Direct3D renderer.` and initializes renderer state. The
accepted M2.20/M2.25 logs independently establish selector-2 Direct3D at
640x480x16 for the bounded runtime arms.

## Ownership of the inactive arena

`0x0049C520` is the native software renderer initializer, not a competing
Direct3D initializer:

- it logs `INITSOFTRENDER : Start.` and `INITSOFTRENDER : End.`;
- `0x0049C65E` writes arena capacity `0x0081C138 = 0x2800`;
- `0x0049C66B-0x0049C689` allocates `capacity << 7` bytes through
  `0x00401992 -> 0x004ADC10` and stores the base at `0x0081BC28`;
- the allocation cites embedded source path `E:\pc\BUGS\soft.cpp`;
- `0x0049C839` zeros counter `0x008082C8` and
  `0x0049C840-0x0049C850` clears 0x1000 list heads rooted through
  `0x004E8CC8`.

Thunk `0x0040152D -> 0x0049C3F0` is not the alternate renderer initializer.
It logs `InitSoftWindow(%i,%i)` and updates software-window dimensions and
clip/scaling globals. Its only structured call at `0x0040FEBA` is gated by
`0x0059F7F0 == 1`, and it does not reference the arena capacity, base, or
counter.

The M2.25 all-zero `(counter, capacity, base)` result is therefore expected in
selector-2 Direct3D runs: the only proven allocator for that triple belongs to
selector 1 and is not called by the selected initialization dispatch.

## Active retained-entry consumer path

`0x0044F8E0` reads the same selector before choosing its output path. Native
branches establish:

- masked stream selector `0x3C`, renderer selector `2`:
  `0x0044F99D -> 0x00401D66 -> 0x00405FE0`;
- masked stream selector `0x34`, renderer selector `2`:
  `0x0045029F -> 0x00401CCB -> 0x00407450`;
- renderer selector `1`: the existing `0x80`-stride arena writers beginning
  at `0x0044F9AA` or `0x004502AC`.

The two selector-2 callees transform three- or four-input records into
separate Direct3D batching storage rooted through pointer globals
`0x004C4108/0x004C410C`. They append `0x20`-byte vertex records and index
lists. When a per-batch vertex count reaches `0x1EE`, native calls
`0x0040127B -> 0x004056A0` or `0x00401618 -> 0x004058D0` flush the batch.
Those flush functions load Direct3D device global `0x005905F8` and invoke its
vtable `+0x78` slot at `0x00405816` or `0x0040598B`. Their exact error strings
identify the operation as `lpD3DDevice->DrawIndexedPrimitive`.

`0x0045A7F0` independently confirms the same renderer split: its selector-1
branches write the `0x80`-stride arena, while selector-2 branches append to
the `0x004C4108/0x004C410C` Direct3D batches and can call the same two flush
functions.

## Reconciliation and correction

The earlier shared-entry trace remains correct about two separate source
walks converging on one arena/list topology, but that convergence occurs on
the native-software branch. It is not the active Direct3D bridge. The exact
active path for the M2.20/M2.25 mode is instead:

```text
retained entry +0x20 stream
  -> 0x0044F8E0
  -> 0x00405FE0 or 0x00407450
  -> Direct3D vertex/index batches
  -> 0x004056A0 or 0x004058D0
  -> IDirect3DDevice2::DrawIndexedPrimitive vtable slot
```

This path is capable of carrying retained-stream differences to visible
Direct3D output without initializing or touching the software arena. Static
reachability does not identify which of the 23 changed retained entries,
which record, or which bytes caused the M2.20 replacement-local result.

## Next discriminator

M2.27 should remain bounded to the two proven selector-2 batch families and
design a metadata-only per-entry provenance comparison that handles
in-call flush/reset behavior. Any live points or execution control require
fresh explicit authority and the established signal/survival gates. Do not
reuse execution breakpoint `0x0044C898`, inspect another resource family,
retain protected batch bytes, assign primitive/asset/field semantics, begin a
general `.ALL` parser, or consult PS1.
