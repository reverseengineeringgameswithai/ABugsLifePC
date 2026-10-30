# M2 adjacent caller-gate continuation fault

## Scope and identity

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact unchanged Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Adjacent-only runtime evidence: `RUN-GDB-20260812-221224` in
  [[EXP-20260812-031 - Adjacent caller-gate continuation fault]]
- Independent exact-PC fault evidence:
  [[EXP-20260812-029 - Fresh selected-entry chain debugger fault]]

No PS1 source or finding was consulted. This export retains address-based
names and does not promote game semantics from a failed debugger continuation.

## Exact static boundary

```text
0044d78f  mov al,BYTE PTR [0x005c5edc]
0044d794  mov ecx,DWORD PTR [0x005ba80c]
0044d79a  test al,0x10
0044d79c  mov DWORD PTR [0x005b56d0],ecx
0044d7a2  jne 0x0044d7a9
0044d7a4  call 0x0040100a
0040100a  jmp 0x0044ca00
```

The M2.18 arm installed only a hardware execution breakpoint at
`0x0044D794`. Its one pre-instruction snapshot records:

- `AL == 0x40`, `RCX == 0`, and `RIP == 0x0044D794`;
- `[0x005C5EDC] == 0x40`;
- `[0x005BA80C] == 0x00000680`;
- `[0x005B56D0] == 0x00000480`;
- `[0x005B1AA4] == 0x006C342B`.

The zero `RCX` is captured before the instruction at `0x0044D794`. Static
instruction semantics say a completed instruction would load `0x680` into
`ECX`; the run does not prove that completion.

## Adjacent-only continuation result

Raw GDB stdout records:

```text
Thread 1 "bugs.exe" hit Breakpoint 1, 0x000000000044d794 in ?? ()
Thread 1 "bugs.exe" received signal SIGSEGV, Segmentation fault.
0x000000000044d794 in ?? ()
```

Harness 1.1/result schema 2 terminates at that signal with PC `0x44D794`,
deletes its single breakpoint, verifies cleanup, and detaches. The required
receipt then records five resumed/untraced process samples. A later isolated
game-surface capture visibly shows live Training gameplay because the pending
fatal signal was suppressed under the proven `nopass` detach policy. Target
survival does not convert the debugger arm into accepted continuation evidence.

## Evidence-strength boundary

**Confirmed:** the fresh adjacent-only hardware arm reached `0x0044D794` once,
then received `SIGSEGV` at that same instrumented PC; structured status rejected
the arm while post-detach process and game-surface evidence proved survival.

**Combined bound:** independent fresh evidence already records the corresponding
same-PC failure at exact `0x0044D79A`. The tested limitation is therefore not
confined only to the exact `test al,0x10` address. The M2.18 contract stopped
after adjacent failure, so no new schema-2 exact-PC arm was run.

**Static only:** the load into `ECX`, subsequent test/store/branch, and call
edge to `0x0044CA00`.

**Unknown:** whether the root lies in Wine WoW64, native GDB, hardware execution
breakpoint continuation, this nearby instruction region, or another condition;
normal runtime completion of the downstream chain; and any plant/resource
meaning.
