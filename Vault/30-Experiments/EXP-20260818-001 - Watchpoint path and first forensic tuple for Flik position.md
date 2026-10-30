---
type: experiment
id: EXP-20260818-001
date: 2026-08-18
question: 'Does the 86Box GDB stub`s hardware write-watchpoint actually fire at the instruction that writes a game global, and can it deliver a forensic tuple (CR3 + writer EIP + address + old + new value) for Flik`s live position?'
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: 86Box v6.0 GDBSTUB build (exec386 interpreter) running real Win95 OSR2 + A Bug`s Life in podman container abl-win95; host-side gdb 15 and a raw RSP client; live runtime
environment_version: 86Box tag v6.0 (4fef696a4eead1d55a28d6ac0e5bd2864e5454da), GDBSTUB=ON
working_directory: /home/dev/ABLPC
configuration: in-level Training gameplay; hardware write-watchpoint (Z2) on 0x0059D910; Flik moved via XTEST-held Up
artifacts:
  - work/86box/wexp.py
  - work/86box/wcmd.gdb
  - work/86box/rsp_exp.py
  - work/86box/rsp_clear.py
  - work/86box/logs/reboot_gameplay.png
addresses:
  - "0x004ab889"
  - "0x004ab88b"
  - "0x0059D910"
  - "0x0059D914"
  - "0x0059D918"
  - "0x0059D91C"
  - "0x00454000"
file_offsets: []
result: watchpoint-path-proven-one-forensic-tuple-runtime-plus-static; stub-tooling-too-fragile-for-continuous-capture
created: 2026-08-18T18:00:00
---

# Watchpoint path and first forensic tuple for Flik position

## Question

Before designing a "flight-recorder" write-trace, prove the underlying primitive:
does the 86Box GDB stub`s **hardware write-watchpoint** halt at the instruction
that writes a game global, and can we read a complete **forensic tuple** —
`CR3 + writer EIP + watched address + old value + new value` — for Flik`s live
position at `0x0059D910`? (User-specified stronger form: break in known `bugs.exe`
code and record CR3 first; verify the hit CR3 matches; repeat to check writer
consistency; and empirically test the ">4 hardware watchpoints" question.)

## Method

- Substrate: the v6.0 `GDBSTUB=ON` 86Box build (`work/86box/86box-v6-gdbstub`),
  real Win95, game launched from a DOS box (`C:\PC\BUGS\BUGS.EXE log cheat`),
  Training level entered. Input recipe (now durable): park the host pointer over
  the 86Box canvas for **PointerRoot** keyboard focus (no X window manager runs on
  the nested `:99`), tap `Right`/`Left` to rotate the carousel, **hold** `Return`
  then `Space` to confirm (the menu polls the keyboard, so a tap is missed). See
  [[86Box Win95 RE harness]].
- Stub reads/writes are **guest-linear** through the active CR3; `$pc` in
  `[0x401000,0x4c0000)` means the game`s address space is current.
- Watchpoint set with gdb `watch *(int*)0x0059d910` (a genuine **hardware**
  watchpoint per `info watchpoints`; the stub`s Z2 is a software linked-list +
  page-bitmap, see `KU-077`). Flik moved via an XTEST-held `Up` so X changes.

## Evidence — the watchpoint fired; forensic tuple captured

Baseline (STEP 1, break in known code): connect halted `$pc` inside `bugs.exe`
(e.g. `0x00481fc1`); **`CR3 = 0x00454000`** = the ABL process. `$cr3` is readable
directly; a plain `watch` allocated `Hardware watchpoint 1`.

First watchpoint hit (`work/86box/wexp.py`):

```
Hardware watchpoint 1: *(int*)0x59d910
Old value = -4378
New value = -4205
HIT 0 trap_pc=0x004ab88b cr3=0x00454000 cr3_matches_ABL=True oldX=-4378 newX=-4205 (Y=9623 Z=-9531)
```

**The forensic tuple (one row of the eventual flight-recorder format):**

| field | value |
| --- | --- |
| CR3 | `0x00454000` (ABL; matches baseline — not a foreign address space) |
| writer EIP | `0x004ab889` `mov [edx],eax` (trap-after PC `0x004ab88b`) |
| watched address | `0x0059D910` (edx held `0x0059D910`) |
| old value | `-4378` |
| new value | `-4205` |

## Cross-check — runtime disasm == on-disk `bugs.exe` (two evidence forms)

The runtime disassembly around the trap matches `bugs.exe` (sha256 `97c95ba5…`)
**byte-for-byte** at VA `0x004ab889` (GNU objdump, static):

```
4ab87b: 8b 54 24 50   mov edx,[esp+0x50]   ; edx = destination pointer
4ab87f: 8b 44 24 3c   mov eax,[esp+0x3c]   ; eax = X
4ab883: 8b 4c 24 40   mov ecx,[esp+0x40]   ; ecx = Y
4ab887: 33 f6         xor esi,esi
4ab889: 89 02         mov [edx],eax        ; WRITER  -> 0x0059D910 (X)
4ab88b: 8b 44 24 44   mov eax,[esp+0x44]   ; (trap-after PC)
4ab88f: 89 4a 04      mov [edx+0x4],ecx    ;         -> 0x0059D914 (Y)
4ab896: 89 42 08      mov [edx+0x8],eax    ;         -> 0x0059D918 (Z)
4ab899: 89 4a 0c      mov [edx+0xc],ecx    ;         -> 0x0059D91C (W)
```

So `0x004ab889` is one store inside a **4-dword vector copy** (X,Y,Z,W from stack
locals `[esp+0x3c/0x40/0x44/0x48]` to `[edx]`). It is a **reusable** vector-store
routine — the destination `edx` is loaded from `[esp+0x50]`, decided by the caller;
this frame`s `edx = 0x0059D910` is what makes it Flik`s position. Identifying which
caller sets `edx = Flik` is the next hop (a call-stack capture the recorder would
add). Runtime (watchpoint) and static (executable) evidence agree independently.

## Findings on the stub as a capture transport (load-bearing)

The watchpoint **mechanism** is correct, but driving it through gdb/RSP for
*repeated/continuous* capture proved unreliable on this stub:

1. **Leftover watchpoints across unclean exits.** Any gdb run that is killed or
   exits mid-run leaves its Z2 in the stub; the next insert then fails
   `Could not insert hardware watchpoint … too many`. Confirmed by a raw RSP probe:
   `z2,59d910,4 -> OK` removed exactly one leftover (everything else `E22`). This
   is the "retains across connects" fragility in `KU-077`, now root-caused to
   unclean removal, not a DR-slot cap.
2. **Malformed `T` stop-reply.** On some watchpoint stops the stub appends a
   trailing field with no `NN:` prefix (`…2c:…80;000000000080;`), which crashes
   gdb ≥15`s parser (`Malformed packet(a) (missing colon)`). This reproduces
   James`s documented breakage.
3. **Non-deterministic async continue.** gdb`s `continue` on this remote target is
   inconsistently asynchronous in batch mode — sometimes it blocks-and-fires (one
   clean hit), sometimes it returns immediately (`Cannot execute this command while
   the target is running`). `maint set target-async off` makes it block but then
   the hit did not arrive. So scripted multi-hit capture is not reliable.
4. **Raw RSP `c` did not reliably resume/fire** even with a correct
   `qSupported`/`?` handshake and a valid halt — a stub resume quirk.

Because of 1–4, the **writer-consistency repeat (step 6)** and the **>4-watchpoint
empirical test** could not be run cleanly. The `>4` question remains **source-
confirmed** (no linked-list count limit; the "4" is gdb`s client-side i386 cap) but
**empirically unverified** here. See `KU-077`.

## Conclusion

- **Watchpoint path PROVEN.** A hardware write-watchpoint on `0x0059D910` fired at
  the writing instruction and delivered a correct, CR3-verified forensic tuple; the
  writer (`0x004ab889`) is confirmed by independent runtime and static evidence.
  The data a flight-recorder needs (`CR3 + writer EIP + address + old + new`) is
  obtainable.
- **But the gdb/RSP transport is too fragile for continuous capture.** The
  implication for the recorder is decisive: build it as **emulator-side C
  instrumentation** (hook the `mem.c` write accessors that already carry
  `GDBSTUB_MEM_ACCESS`, filtered by CR3 and address range, into a circular buffer)
  rather than gdb-watchpoint-driven capture. The interpreter core routes every
  guest write through those C accessors (no dynarec fast-path), so a complete,
  reliable write-trace is feasible there. This confirms the ChatGPT "flight
  recorder" architecture and rules out the gdb-watchpoint shortcut.

## Links

- `KU-077` (updated with the fires-result and the transport findings),
  [[86Box Win95 RE harness]], [[PC autonomous game control]].
- [[Decision Log#DEC-20260817-147 - Build a GDBSTUB-enabled 86Box to prove Gate 2 memory access]].
- Prior live reads: [[2026-08-18 0500 - Claude - Live gameplay memory read and KU-076 resolution]].
