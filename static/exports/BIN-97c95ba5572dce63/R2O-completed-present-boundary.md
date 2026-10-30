# R2o completed-present boundary static trace

## Evidence identity

- Retail executable: `work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe`
- Retail SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Auto-hardware executable: `work/copies/auto-hardware/bugs.exe`
- Auto-hardware SHA-256: `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`
- Image base: `0x00400000`
- `.text`: VA `0x00401000`, file offset `0x00000400`
- Checked Ghidra export SHA-256: `db2dc35a8dcbc9138a318b5ca07bdc1e5ac2703c5760b7b99207a29703c67f5d`
- Predecessor R2n trace: `R2N-state-equivalence-read-candidates.md`

This is offline PC-static evidence. It launches no target, attaches no
debugger, changes no execution state or debug register, reads no process
memory, and writes no game or DAT byte. The Ghidra export is used as a search
surface; the accepted chain below is checked against native retail
instructions and exact derived-build byte spans.

## Exact normal-frame chain

One normal `0x0040FFC0` invocation has this CPU order when the instruction at
`0x0040FFCF` compares `uint16[0x0059A5F0] == 0`:

```text
0x0040FFD9 -> thunk 0x004017B7 -> 0x004144C0
  0x00414585 upstream R2n phase
  0x0041458F generated-view R2n phase
return
0x0040FFDE -> thunk 0x00401B81 -> 0x0044D430
  0x0044DBEE -> thunk 0x004017CB -> 0x00405AD0
    0x00405AFC reads renderer selector 0x0059F7F0
    selector 2 takes 0x00405B09 -> thunk 0x00401C7B -> 0x00405EF0
      EndScene call 0x00405F69, return PC 0x00405F6C
      ShowBackBuffer call 0x00405F8B -> thunk 0x004018BB -> 0x00424890
return
0x0040FFE3 normal outer completion PC
```

`0x0040FFF3` is the alternate outer completion after the branch that skips
`0x004144C0`. It is not a substitute for `0x0040FFE3`.

The phase PCs retain the exact R2n instruction semantics: `0x00414585` is
before the push/call that generates the view state, after the selected-copy
callee has returned; `0x0041458F` is before the stack adjustment, after the
view-transform callee has returned.

## Why outer completion alone is insufficient

The call at `0x00405F8B` does not prove presentation. `0x00424890` can return
before a buffer call when `uint8[0x0059063E] == 0` or when
`uint8[0x00590638] != 0`. It also contains lost-surface restoration and error
paths. Its caller ignores its return value. Therefore neither `0x00405F90`
nor later `0x0040FFE3` independently proves a successful present.

For R2o, `0x0040FFE3` may be called a **CPU-side completed-present boundary**
only after one of these mutually exclusive return gates in the same guarded
TID and enclosing `0x0040FFC0` invocation:

| Mode gate | COM call | Return PC | Exact success gate |
|---|---|---|---|
| `uint32[0x00573FF0] != 0` | fullscreen Flip vcall `0x004248EE` | `0x004248F1` | `EAX == 0` |
| `uint32[0x00573FF0] == 0` | windowed Blt vcall `0x004249C1` | `0x004249C4` | `EAX == 0` |

Both alternatives additionally require
`uint16[0x0059F7F0] == 2`, `uint8[0x0059063E] != 0`, and
`uint8[0x00590638] == 0`. R2o also requires nonnegative signed `EAX` at
EndScene return PC `0x00405F6C`; otherwise a later buffer flip could expose a
prior scene rather than the generated invocation under test. A surface-lost
HRESULT, any other nonzero present HRESULT, both present-return sites, no
present-return site, or a second present-return hit before `0x0040FFE3`
rejects the invocation.

These gates establish CPU ordering and a successful DirectDraw method return.
They do not establish when Wine, Xwayland, Gamescope, or the host compositor
latches or exposes the surface to a screenshot.

They also do not exclude another presentation between `0x0040FFE3` and the
next `0x00414585`; `0x0049CC40` is a separate ShowBackBuffer caller. Exact
screenshots at those two stops would be empirical equality, not proof of
surface identity or one compositor latch.

## Retail-to-auto-hardware byte binding

All intervals are half-open. File offsets use the `.text` relation
`file = VA - 0x00400C00`. Each range has the same SHA-256 in retail and the
executed auto-hardware build:

| Purpose | VA range | File range | Bytes | SHA-256 in both files |
|---|---|---|---:|---|
| normal/alternate outer branch | `[0x0040FFC0,0x0040FFF9)` | `[0x0000F3C0,0x0000F3F9)` | 57 | `434668f85602a9f113f406f4414ecc284672e9d7582e2dccf3ef6d7ba2251c79` |
| R2n phase anchors | `[0x00414573,0x00414592)` | `[0x00013973,0x00013992)` | 31 | `55ac0699aa2c748656d1ed8ba8abb0733444d242e9ad72f518f8fa059b25ae2a` |
| renderer tail/call | `[0x0044DBE9,0x0044DBFB)` | `[0x0004CFE9,0x0004CFFB)` | 18 | `3d632e6f6c4ec6b4ad89fed761a64a0dfa6e6cefd51ca3de52ce2b1942d649f2` |
| D3 selector branch | `[0x00405AFC,0x00405B10)` | `[0x00004EFC,0x00004F10)` | 20 | `3a5f077c451ef8e3f19371bab93795601eac56129ac36cc398f120a7111539d3` |
| EndScene/ShowBack dispatch | `[0x00405EF0,0x00405F90)` | `[0x000052F0,0x00005390)` | 160 | `557d3d51f9af806ac3a78d86bc3781338ae72244039dfdbcc9c50cbe431a94b2` |
| ShowBack entry, Flip path, and Blt return gate | `[0x00424780,0x004249D0)` | `[0x00023B80,0x00023DD0)` | 592 | `66247511724197774ba5523fb070e8c466b79cab25480f43257c875540da5bbe` |

The auto-hardware transform remains confined to startup-code file
`0x000A6C6B..0x000A6C73` and relocation byte `0x000FA913`; none overlaps
these ranges. Identical bytes bind the addresses and control flow to both
hashes without promoting derived-build behavior to retail confirmation.

## Future execution-control ceiling

A future runner must use hardware execution breakpoints only. An x86 software
breakpoint writes `0xCC` into process code and is a runtime write; it remains
prohibited unless separately and explicitly authorized with compare-before-
write and restoration receipts.

The hardware-breakpoint state machine must keep `0x0040FFC0` continuously
armed on one selected TID, read the exact normal-branch operand at
`0x0040FFCF`, then require both phase PCs, EndScene, exactly one successful
Flip/Blt return, and `0x0040FFE3`. It must reject an unexpected new invocation,
missed/out-of-order/duplicate hits, process identity drift, or deadline expiry.
Stopping all owned tasks for screenshots is an execution
perturbation, not passive observation. This report authorizes none of it.

## Reproduction

```bash
python scripts/ghidra-query.py function --addr 0x00405AD0
python scripts/ghidra-query.py xrefs --to 0x00590638
python scripts/ghidra-query.py xrefs --to 0x0059063E
python scripts/ghidra-query.py xrefs --to 0x00573FF0
objdump -d -Mintel --start-address=0x40ffb0 --stop-address=0x410010 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x405ed0 --stop-address=0x405fb0 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
objdump -d -Mintel --start-address=0x424780 --stop-address=0x424a00 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
```
