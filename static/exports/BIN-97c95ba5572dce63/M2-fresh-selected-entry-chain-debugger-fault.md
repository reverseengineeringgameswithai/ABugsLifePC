# M2 fresh selected-entry chain debugger-fault trace

## Scope and identity

- PC executable SHA-256:
  `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Exact unchanged Training DAT SHA-256:
  `494d28187739782523757511a17414c41c04782d84f90f7333092d6f008d5a22`
- Runtime evidence: `RUN-GDB-20260812-211649` in
  [[EXP-20260812-029 - Fresh selected-entry chain debugger fault]]
- Prior static/runtime boundary:
  [[EXP-20260812-028 - Plant10 post-title selected-entry negative]]

No PS1 source or finding was consulted. This trace retains address-based names
and separates the one valid stop snapshot from the failed continuation.

## Exact static chain

```text
0044d78f  mov al,BYTE PTR [0x005c5edc]
0044d794  mov ecx,DWORD PTR [0x005ba80c]
0044d79a  test al,0x10
0044d79c  mov DWORD PTR [0x005b56d0],ecx
0044d7a2  jne 0x0044d7a9
0044d7a4  call 0x0040100a
0040100a  jmp 0x0044ca00
```

At the only structured stop, `AL == 0x40`, `[0x005C5EDC] == 0x40`, and
`[0x005BA80C] == 0x00000680`. Static flag evaluation would leave the `jne`
untaken because `0x40 & 0x10 == 0`. This describes the captured state and
instruction semantics only; it is not runtime proof that execution reached or
completed the call at `0x0044D7A4`.

## Simultaneous four-point arm

Before advancing the natural Training title, the harness installed exactly
four hardware points:

- execution breakpoint `0x0044D79A`;
- execution breakpoint `0x0044CA00`;
- two-byte read watch `0x005AAB2E`;
- two-byte read watch `0x005AAB7E`.

The arm recorded one stop at `0x0044D79A`. Its bounded snapshot retained plant
slot `0x005B1AA4 == 0x006C342B`, header words `1/3/66/68`, and both exact
80-byte entries. Four configured fixed source-table blocks
`[0x0059D9C0,0x0059DD88)` were zero at that stop. That last fact is bounded to
the configured addresses and does not locate or exclude a source record.

There was no structured stop at `0x0044CA00` or either exact data watch.
Those zero counts cannot be interpreted after the continuation fault.

## Reproduced continuation failure

Raw GDB stdout from the same arm records:

```text
Thread 1 "bugs.exe" hit Breakpoint 3, 0x000000000044d79a in ?? ()
Thread 1 "bugs.exe" received signal SIGSEGV, Segmentation fault.
0x000000000044d79a in ?? ()
```

The structured harness result nevertheless says `target_reached`, because
schema-1 control treats every unclassified non-`SIGINT` signal as a signal to
continue. Wine then reported an unhandled read from `FFFFFFFF` at
`0x0044D79A` and opened its debugger. The game-only post-detach capture showed
the Wine fatal-error dialog, not live gameplay.

The game log contains `NextLife`, but this is only the configured log
milestone. It does not override the fatal-signal and process-survival evidence.

## Evidence-strength boundary

**Confirmed:** the fresh simultaneous arm reached the outer gate once with the
captured register/memory state; continuation reproduced the same-address
`SIGSEGV`; schema 1 did not surface it; Wine did not survive normally.

**Static only:** the untaken-branch evaluation for captured `AL`, the call
edge at `0x0044D7A4`, and the thunk edge to `0x0044CA00`.

**Unknown:** the initial fault's root cause; whether this instruction can be
safely resumed under Wine/native GDB; a runtime-completed gate-to-callee edge;
the source selector/event; plant 10 field meanings; and any M1 dependency.
