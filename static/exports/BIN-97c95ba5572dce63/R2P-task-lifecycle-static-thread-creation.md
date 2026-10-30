# R2P PC static thread-creation boundary

## Source identity

- Retail `bugs.exe`: SHA-256 `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
- Auto-hardware `bugs.exe`: SHA-256 `1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`.
- `static/pe/BIN-97c95ba5572dce63/pefile.json`: SHA-256 `bba35a9338ad552a68b7e0fbf6784af92216275325908d62fc9a6450d6b41591`.
- `static/pe/BIN-97c95ba5572dce63/objdump.txt`: SHA-256 `f415674a5b6c57b5799ec5a150dec248e8b32eb8fdf8528033ba0848b0a42667`.
- `static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json`: SHA-256 `db2dc35a8dcbc9138a318b5ca07bdc1e5ac2703c5760b7b99207a29703c67f5d`.

## Exact PC evidence

The PE import record names `KERNEL32.dll!CreateThread` at IAT
`0x008645F8`. Full-image disassembly has one direct call through that IAT:

```text
0x0042CF04  ff 15 f8 45 86 00  call DWORD PTR ds:0x008645f8
```

It pushes start thunk `0x00401889`; the thunk bytes `e9 c2 f6 03 00` branch
to `0x00440F50`. The six call bytes at physical file offset `0x0002C304`
and the five thunk bytes at `0x00000C89` are identical in the retail and
auto-hardware executables. `0x00440F50` contains a long-lived
`WaitForMultipleObjects` loop in the Ghidra export. This bounds one PC-native
thread-start path. It does not prove that path created the task observed by
R2o.

Reproduction:

```bash
jq '.. | objects | select(.name? == "CreateThread") | {address,name}' \
  static/pe/BIN-97c95ba5572dce63/pefile.json
objdump -d -Mintel work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe \
  | rg -n -C 4 '8645f8'
objdump -d -Mintel --start-address=0x401880 --stop-address=0x401890 \
  work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe
scripts/ghidra-query.py function --addr 00440f50 \
  --max-decompiler-bytes 8000 --max-data-references 200
```

## Hard limit

The Ghidra export has an empty `imports` array and returns no data-reference or
decompiler-text xref for `0x008645F8`; its call graph therefore cannot name the
imported edge. The PE/IAT and disassembly evidence independently establish the
PC call, but neither source binds it to added Linux TID `1648646`. That task's
name, creator, module, role, lifetime, and debugger dependence remain unknown.
Absence of another PC import call is not evidence that Wine did not create the
task.

## P0C DirectSound role candidate

The later offline P0C pass narrows the PC call's role without binding it to a
Linux TID. `FUN_0042BB90` owns the level-music table, including string
`audio\Level1a.wav` at `0x004D7744`. Its successful track-start tail has this
exact native sequence:

```text
0x0042BF40  call 0x00401CF8                 ; PLAYTRACK log thunk
0x0042BF48  call 0x004015B9 -> 0x0042C9C0  ; WAV/stream-buffer setup
0x0042BF5E  mov  [0x004D7430],1             ; stream-active flag
0x0042BF68  call [0x008647D4]               ; SendMessageA, WM_COMMAND 0x9C46
```

The synchronous `0x9C46` command arm at `0x0042C768` requires both the active
flag and the stream buffer at `0x00596CE0`, then calls thunk
`0x00401276 -> 0x0042CE80`. That builder creates two notification events and
makes the unique direct `CreateThread` call at `0x0042CF04`. The worker at
`0x00440F50` waits on those two events and services the same stream-buffer
globals. PE import evidence independently identifies `SendMessageA` at IAT
`0x008647D4`, `CreateThread` at `0x008645F8`, and
`WaitForMultipleObjects` at `0x008645FC`.

The P0B retained post-title log append contains one
`PLAYTRACK ... audio\Level1a.wav` line followed by `SETMUSICVOL`, while its
sole new Linux task has generic `comm=bugs.exe`. Therefore “PC Level1a
DirectSound stream worker” is the strongest role candidate. It remains an
**inference**: the log has no per-line monotonic timestamp, and no retained
receipt binds TID `2086681` to the `CreateThread` return or start routine
`0x00440F50`. Wine-created generic tasks remain a live alternative.

The first machine-checking implementation and its `-001` output are retained
as rejected protocol history because publication could overwrite a racing
competitor and the checked spans omitted the `0x9C46` decoder. Its `-002`
correction is also retained as rejected history: it pinned the decoder/arm,
`0x004015B9` buffer-init thunk, two-event builder, and objdump input but omitted
imported intermediary `r2c_f0.py` from its complete executed-source claim.
The fresh successor pins that module, active `r2c_localizer.py`, and the
package-init/parser chain; its regression independently closes the wrapper-
rooted local import graph.

Current machine-checked P0C output:

- `work/copies/EXP-20260820-005/evidence/offline/task-attribution-003/analysis.json`
- SHA-256 `62af5c091c9f97499c346146c50d2ceaf0fb7e3d05ddd0056338da099a96d6ff`
- James **ACCEPTED** exact implementation commit `f2629944b9163ae39e608320e60e7fed76fabb09`, tree `9c7c1294e60f3c0ed6bb47f9f8575362d9ac1d45`.
