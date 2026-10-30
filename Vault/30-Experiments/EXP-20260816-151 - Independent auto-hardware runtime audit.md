---
type: experiment
id: EXP-20260816-151
date: 2026-08-16
question: Do EXP-20260816-150's auto-hardware paired transform build, disassembly, and two-restart runtime acceptance survive an independent fresh-context hard-truth audit?
status: accepted
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
modified_binary_sha256: 1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f
environment: Fedora Linux 44; offline independent builder reproduction, capstone 5.0.7 + objdump disassembly, PE relocation parse, and retained-log/screenshot review; no runtime launch
configuration: fresh-context adversarial audit at clean HEAD cfd06ed164c7c7b908b0f218b0ed34084ca4987f; read-only toward all game media; no target launch, write, commit, or staging; the only build was an in-memory/scratchpad copy, never the tracked retail path
working_directory: /home/dev/ABLPC
artifacts:
  - reimplementation/ablpc/auto_hardware_mod.py
  - scripts/make-auto-hardware
  - tests/test_auto_hardware_mod.py
  - work/copies/EXP-20260816-144-gate-mapping/evidence/auto-hardware/
addresses:
  - "0x004A7600"
  - "0x004A7866"
  - "0x004A786B"
  - "0x004A786F"
  - "0x004A7A56"
  - "0x004A7B2C"
file_offsets:
  - "0x000A6C6B"
  - "0x000FA912"
result: accept-auto-hardware-transform-and-two-restart-runtime-at-the-derived-build-hash
created: 2026-08-16
updated: 2026-08-16
tags: [re/experiment, re/runtime, re/direct3d, re/audit]
---

# EXP-20260816-151 - Independent auto-hardware runtime audit

## Verdict and authority

**ACCEPT**, bounded to the derived build hash
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`. This is an
independent fresh-context hard-truth audit of the runtime-acceptance packet
[[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]], the fresh
James ratchet that [[PC automatic Direct3D startup candidate]] requires before
promotion. The transform build and disassembly were reproduced independently;
the two runtime arms were **not** relaunched (expensive Gamescope/Wine
launch) — their two retained logs and three screenshots were audited as the
runtime evidence.

No game process, Wine process, Gamescope, debugger, or target write was used.
`originals/` and the tracked retail work copy were not modified; nothing was
committed or staged. The one build performed was an in-memory `bytes` build in
the audit interpreter, never written to the tracked retail path.

Every material claim was re-derived from the repository. The core claims hold:
the guarded builder produces the pinned output with exactly nine changed bytes
and exact inverse; the patched instructions decode as claimed and enter the
chooser's genuine cleanup; both retained logs carry all six [[START HERE]]
hardware markers plus `Device has hardware acceleration` and none of the reject
markers; the screenshots show a full-frame carousel and full-frame gameplay
with no visible chooser; retail/`originals` identity and the `Y:` restore hold;
and the packet did **not** pre-promote the candidate note or edit START HERE.
One honest narrowing is recorded in the Defects section: the specific host-GPU
device identity (`RTX 5090`, not llvmpipe) is **asserted but not carried by the
two retained `bugs.log` files**, so the accepted boundary is hardware Direct3D
at the game-renderer level, not a proof of the physical GPU device from this
retained evidence.

## Check 1 - Transform bytes and build

- `work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe` rehashes to
  `97c95ba5...27b878` at 1,069,056 bytes.
- Raw bytes read directly: file `0x000A6C6B` = `ff d7 2b 05 34 12 7f 00 99`;
  file `0x000FA912` = `6f 38`. Both match the recipe.
- `build_auto_hardware_executable` on the retail bytes returns output SHA-256
  `1e1d5099...c8a9c41f` (matches), `output_size == source_size == 1069056`
  (size unchanged), and `changed_byte_count == 9`. An **independent** byte diff
  finds exactly nine changed offsets — `0xa6c6b..0xa6c71`, `0xa6c73` (8 of the
  9 code bytes; `0xa6c72` is unchanged because retail `00` equals replacement
  `00`) and `0xfa913` (the reloc high byte; `0xfa912` unchanged because both are
  `6f`). All nine lie inside the two declared spans. `touched_byte_count == 11`.
- `invert_auto_hardware_executable` reconstructs the retail bytes exactly
  (`back == src`, digest back to `97c95ba5...27b878`).
- **Builder source review** (`reimplementation/ablpc/auto_hardware_mod.py`):
  the source SHA-256 is checked first and any mismatch raises before any byte
  is touched; each patch's `expected` span is compared before it is applied and
  a mismatch raises `AutoHardwareModError`; both edits are applied to one local
  `bytearray` and the function returns only after **both** succeed and the
  inverse is reconstructed and re-verified, so a one-edit output is structurally
  impossible; every changed byte is confined to the two spans (independent diff
  above); overlap and out-of-range spans are rejected; the receipt records
  source/output SHA, sizes, and change counts. `_patches()` pins the exact
  offsets, VAs, and hex.
- **Script review** (`scripts/make-auto-hardware`): refuses symlinked source or
  output, requires both `source` and `output` under `work/`, requires
  `source != output`, requires the source to be a regular file, and is
  create-only on output (refuses an existing output). It copies mode from the
  source and prints the receipt JSON.
- `pytest tests/test_auto_hardware_mod.py -q`: **9 passed**.

Result: **PASS.**

## Check 2 - Disassembly correctness

Disassembled a built copy with capstone 5.0.7 (cross-checked byte-for-byte),
using the confirmed section delta `VA - 0x400C00` (VA `0x004A786B` = file
`0x000A6C6B`):

```text
; PATCHED
004A7866  bd 02 00 00 00   mov ebp, 2
004A786B  89 6c 24 10      mov dword ptr [esp + 0x10], ebp
004A786F  e9 e2 01 00 00   jmp 0x004A7A56
; RETAIL (same region)
004A786B  ff d7            call edi
004A786D  2b 05 34 12 7f00 sub eax, dword ptr [0x7f1234]
```

- `89 6c 24 10` = `mov [esp+0x10], ebp` — confirmed.
- `e9 e2 01 00 00` = `jmp 0x004A7A56`; displacement `0x1E2` from next-PC
  `0x004A7874` gives `0x004A7874 + 0x1E2 = 0x004A7A56` — confirmed.
- `0x004A7866` = `mov ebp, 2`, so the value written to `[esp+0x10]` is chooser
  result 2 — confirmed.
- **`0x004A7A56` is the chooser's genuine cleanup/epilogue**, not a landing in
  unrelated code. It decodes cleanly on an instruction boundary: it reloads
  `mov esi, [esp+0x10]` (reads back the result the patch just wrote), then runs
  a long release chain — for each surface global `0x861ca0, 0x861ca4, 0x861ca8,
  0x861cac, 0x861cb0, 0x861cb4, 0x861cb8` it does `if ptr != 0 { push ptr; call
  0x4b0270; ptr = 0 }` (a release/free-and-null idiom) — then loads the COM
  object at `0x7f1230` and issues virtual calls (`call [edx+0x4c]`) consistent
  with releasing/restoring the temporary display objects. This is the retained
  cleanup path.
- **Relocation reasoning** (PE parse): the reloc entry at file `0x000FA912`
  lives in the base-relocation block whose PageRVA is `0xA7000` (block size
  `0x214`). The retail entry is the 16-bit word `0x386F` — top nibble `3`
  (HIGHLOW), low 12 bits `0x86F` — so its target is RVA `0xA7000 + 0x86F =
  0xA786F`, exactly the absolute operand `0x007F1234` of the retail
  `sub eax, [0x7f1234]` (which now lies inside the new relative jump). The
  built entry is `0x086F` — top nibble `0` (ABSOLUTE/padding), low 12 bits
  `0x86F` preserved. Only the type nibble flips; leaving it HIGHLOW would let
  the loader rebase-corrupt the jump. Neighboring active entries target RVA
  `0xA785C`, `0xA7862`, `0xA7879`, `0xA787E`; none of their 4-byte ranges
  overlap the patched span `0xA786B..0xA7873`.
- **Not the rejected whole-chooser bypass**: the edit is inside the chooser
  function `0x004A7600` and enters **after** `0x004A7866` (at `0x004A786B`), so
  the pre-loop DirectDraw/surface setup and the `mov ebp, 2` are retained; it is
  not the WinMain-level (`0x0043DA40`) skip that EXP-143 rejected.

Result: **PASS.**

## Check 3 - Runtime evidence (retained logs and screenshots)

Both retained logs
(`work/copies/EXP-20260816-144-gate-mapping/evidence/auto-hardware/ah1-bugs.log`,
1474 lines, and `ah2-bugs.log`, 954 lines) were grepped:

- Each contains, exactly once, all six START-HERE markers —
  `Native software render mode is FALSE`,
  `RenderMode set to Direct3d render mode`,
  `Screen mode 640x480x16 selected`,
  `OnlySystemMemory status VIDEO MEMORY ONLY`,
  `D3DAPPCREATE : Mode set to 640x480`,
  `INIT : Starting Direct3D renderer` — plus
  `INFO Direct3D - Device has hardware acceleration.`
- Neither contains `SYSTEM MEMORY ONLY` or `INITSOFTRENDER` (0 hits each). The
  only `320x200` hits are the DDMODE enumeration listings (`DDMODE 0 -
  320x200x8`, `DDMODE 5 - 320x200x16`, `DDMODE 10 - 320x200x32`), explicitly
  not a reject; the sole `Screen mode ... selected` line is `640x480x16`, so
  there is no 320x200 **selected** surface.
- Ordering discriminates against the EXP-143 early-probe trap: the final-path
  markers (`VIDEO MEMORY ONLY` line 98, `D3DAPPCREATE 640x480` line 99,
  `INIT : Starting Direct3D renderer` line 127) all follow `SwitchDriverScreen`
  (line 86) in both logs, and no software-fallback marker appears after it. The
  selected drivers block records the Direct3D HAL device
  (`Direct3D HAL, Wine D3DDevice using WineD3D and OpenGL`) with
  `Device has hardware acceleration`.
- **Screenshots.** `ah1-t1.png` and `ah2-early.png` both show the "fliks
  journey" level-select carousel (with "training" selected) rendered full-frame
  at the 4:3 640x480 surface — no 320x200 corner surface and no visible
  renderer chooser. `ah1-gameplay.png` shows the "Training Level" scene
  (Flik before a crowd of bugs) rendered full-frame. The claims of "no visible
  chooser" and "playable rendering" are **supported** by these images; the two
  logs corroborate two distinct runs (different lengths; `ah1` proceeds into
  Training-level loading and `ClearLoadScreen`, `ah2` ends at the carousel with
  its music track).
- **"No chooser input sent"** is a negative that logs cannot prove; treated as
  the worker's asserted procedure. Nothing in the evidence contradicts it — the
  logs proceed from SELECT DRIVERS straight into SwitchDriverScreen and gameplay
  with no chooser interaction logged, consistent with the auto-confirm patch.

Result: **PASS** for the six-marker hardware-Direct3D gate, no-visible-chooser,
and playable rendering. See Defect 1 for the host-GPU sub-claim.

## Check 4 - Retail / originals integrity and lifecycle

- The retail exe still hashes `97c95ba5...27b878`. The patched build lives at
  `work/copies/auto-hardware-full-disc/PC/BUGS/bugs.exe`
  (`1e1d5099...c41f`), while that copy's top-level `bugs.exe` remains retail
  (`97c95ba5...`) — confirming a separate tree with only `PC/BUGS/bugs.exe`
  replaced.
- `originals/` tracks only `.gitkeep`; `git status --porcelain originals` is
  empty and the commit does not touch it — untouched.
- Wine `Y:` (`work/wine/baseline/dosdevices/y:`) currently resolves to
  `/home/dev/ABLPC/work/copies/BUGS_PC-full-disc`, matching the packet's
  claim that `Y:` was restored to retail.

Result: **PASS.**

## Check 5 - Overclaim / no premature promotion

- The packet frames itself as a runtime acceptance for the **derived build
  hash** only ("this transform produces a distinct build hash"; "the manual
  procedure and full log gate remain authoritative for the retail hash"), and
  the Follow-up defers promotion to a fresh James ratchet.
- At HEAD `cfd06ed`, [[PC automatic Direct3D startup candidate]] still has
  `status: proposed-static`, and [[START HERE]] still reads "Automatic
  selection is **not implemented**." `git show --stat cfd06ed` does not list
  either file, so this commit did not promote the candidate note or edit START
  HERE.

Result: **PASS.**

## Check 6 - Hygiene

- `git status --porcelain` is empty at HEAD `cfd06ed`.
- `git show --stat cfd06ed` adds only tool/test files and Vault notes
  (`auto_hardware_mod.py`, `make-auto-hardware`, `test_auto_hardware_mod.py`,
  and five Vault files); no game bytes.
- `git check-ignore` confirms the patched full-disc copy and the evidence
  logs/screenshots are ignored via `.gitignore:/work/copies/`; `git ls-files`
  lists none of them as tracked.
- `make check`: Python doctor passed, Vault lint **432 notes / 0 errors / 0
  warnings**, M4 compatibility statement valid (5 hash anchors), **619 tests
  passed**, tracked-file audit **0 violations**.

Result: **PASS.**

## Defects and recorded limits

Only Defect 1 narrows the accepted boundary; it does not change the
hardware-Direct3D acceptance. None reopen a milestone.

1. **Host-GPU device identity is asserted, not carried by the retained
   evidence.** The packet and the MOC state Gamescope selected the physical
   `NVIDIA GeForce RTX 5090` (not llvmpipe). The two retained `bugs.log` files
   contain no Gamescope/Vulkan device line; the game's
   `Device has hardware acceleration` reflects the wined3d Direct3D device caps,
   which wined3d advertises whether the underlying GL is a real GPU or llvmpipe,
   so it does **not** by itself distinguish RTX 5090 from a host software
   renderer. No separate Gamescope/host-GPU log was retained in this packet's
   evidence directory. This is exactly the EXP-143 acceptance criterion 7
   ("separately proves the intended host GPU path when that distinction
   matters"): the game-renderer hardware path is proven, but the physical-GPU
   identity is not, from the two retained logs. The accepted boundary is scoped
   accordingly. (Recorded, not blocking — the START HERE six-marker gate is a
   game-renderer hardware-vs-software gate and is satisfied.)
2. **Two carousel screenshots are pixel-identical.** `ah1-t1.png` and
   `ah2-early.png` are the same deterministic carousel frame, so the images
   alone cannot establish two distinct runs; the two distinct log files
   (different lengths and endpoints) do establish two runs. Not a defect in the
   claim, recorded for precision.

## Accepted boundary

Accepted, at the derived build hash
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`:

- the guarded paired transform in `auto_hardware_mod.py` /
  `make-auto-hardware` — hash-locked source refusal, mandatory both-edit atomic
  apply with no one-edit output, byte-preservation outside the two spans, proven
  exact inverse, and the create-only/`work/`-only script guards;
- the disassembly: `mov [esp+0x10], ebp` with `ebp==2`, `jmp 0x004A7A56` at
  displacement `0x1E2`, the `0x004A7A56` surface-release/display-restore
  cleanup, and the HIGHLOW→ABSOLUTE relocation neutralization with non-
  overlapping neighbors — retaining the chooser's pre-loop setup (not the
  rejected whole-chooser bypass);
- the two-restart runtime acceptance **at the game-renderer level**: all six
  hardware markers plus `Device has hardware acceleration`, none of the reject
  markers, full-frame carousel and full-frame Training-level rendering, and no
  visible chooser, across two distinct retained runs;
- retail and `originals/` integrity, the separate patched tree, and the `Y:`
  restore.

**Not** accepted / explicitly excluded: the specific host-GPU device identity
(`RTX 5090`, not llvmpipe) from the two retained logs (Defect 1); the retail
hash, for which the manual hardware-selection procedure and the full-log gate
in [[Wine Linux Play Baseline]] remain authoritative. This ratchet clears
[[PC automatic Direct3D startup candidate]] for the worker's promotion from
`proposed-static` and the corresponding [[START HERE]] update, scoped to the
derived build hash; the worker performs that reconciliation.
