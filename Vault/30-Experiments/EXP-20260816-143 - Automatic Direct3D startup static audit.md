---
type: experiment
id: EXP-20260816-143
date: 2026-08-16
question: Does the retail PC executable expose a native renderer-selection argument, and if not, what is the smallest statically defensible way to auto-confirm Direct3D without dropping required chooser initialization?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44; offline Ghidra-export, radare2, objdump, raw-byte, PE-relocation, and retained-log audit; no runtime process
configuration: read-only audit of the exact retail work copy; no executable, script, Vault, original, runtime, or repository mutation during the audit
artifacts:
  - static/exports/BIN-97c95ba5572dce63/ghidra-evidence.json
  - dynamic/wine/RUN-WINE-20260812-005110/bugs.log
  - dynamic/wine/RUN-WINE-20260812-231216/bugs.log
  - dynamic/wine/EXP-20260815-134-receipt.md
addresses:
  - "0x00403B90"
  - "0x004119E0"
  - "0x0041F990"
  - "0x0042C130"
  - "0x0043DA40"
  - "0x0049C520"
  - "0x004A7600"
  - "0x004A786B"
  - "0x004A7A56"
  - "0x004B1670"
result: no-native-renderer-argument-paired-static-candidate-requires-runtime-validation
created: 2026-08-16
updated: 2026-08-16
tags: [re/experiment, re/static, re/startup, re/direct3d]
---

# EXP-20260816-143 - Automatic Direct3D startup static audit

## Verdict and authority

The exact retail executable has **no native command-line argument** for
selecting hardware/Direct3D or bypassing the opening renderer chooser.

A two-location, exactly reversible executable transform is a defensible
**static candidate** for retaining the chooser's initialization and cleanup
while auto-confirming selector 2 before its interactive loop. It has not been
built or launched. It is not yet an accepted launcher feature and must not
replace the manual selector procedure or the complete renderer log gate.

The retail work copy rehashed to
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.
The audit did not launch the game or modify any file. An independent James
hard-truth pass first rejected a simpler whole-chooser bypass, then accepted
the corrected paired transform only as a static candidate pending fresh
runtime validation.

## Command-line census

The CRT entry at `0x004B1670` calls `GetCommandLineA` and passes the command
tail to the WinMain-like `0x0043DA40`. The game parser at `0x00403B90` reads
that tail from `0x0059F738`, tokenizes on the literal delimiter `" -"`, uses
case-sensitive `lstrcmpA`, and recognizes only:

- `cheat`
- `log`
- `mpeg`
- `high`

A second real parser at `0x0042C130` calls `GetCommandLineA` but belongs to
the DSStream/audio-stream path. Its case-insensitive tokens are only `PLAY`,
`LOOP`, `CLOSE`, `STICKY`, and `GLOBAL`. Other command-tail reads at
`0x00421328` and `0x0042BADF` pass the string to `0x00420C80`, which does not
consume a renderer parameter.

Therefore `hardware`, `d3d`, `-hardware`, and similar guessed arguments are
ignored. This conclusion is pinned to this executable hash; it is not a claim
about another PC release.

## Startup and chooser flow

`0x0041F990` creates the temporary `Examining Machine` window, enumerates
DirectDraw/Direct3D, selects device/mode records in `0x00582D0C`,
`0x00582D10`, and `0x00582D14`, and maps the native-software flag to renderer
selector `0x0059F7F0`: value 1 is native software; value 2 is Direct3D.

The WinMain-like function at `0x0043DA40` then:

1. calls chooser `0x004A7600` only when the probe left selector 2;
2. calls native-software initializer `0x0049C520` when the chooser returns 1;
3. calls Direct3D initializer `0x004119E0` when it returns 2.

Chooser `0x004A7600` initially sets index `0x007F1150` to zero. Confirmation
or the 60-second timeout converts `(index != 0) + 1` into selector 1 or 2, so
its untouched default is software. Before the interactive loop, however, it
also creates temporary DirectDraw surfaces and initializes shared width,
height, surface-derived pixel depth, pitch, and related display globals.

This explains the retained runtime contradiction. Both
`RUN-WINE-20260812-005110` and `RUN-WINE-20260812-231216` contain the early
probe summary claiming Direct3D hardware and 640x480x16. After
`SwitchDriverScreen`, the first proceeds through `SYSTEM MEMORY ONLY`,
320x200, and `INITSOFTRENDER`; the second proceeds through `VIDEO MEMORY
ONLY`, 640x480, and `INIT : Starting Direct3D renderer`. The early summary is
therefore insufficient evidence of the final renderer.

## Rejected shortcut

Changing the WinMain conditional so it skips the complete chooser call is
rejected. Although it appears to preserve selector 2, it also skips the only
relevant startup writer for shared BPP `0x00861E10` and related setup. The
Direct3D initializer does not independently supply every omitted value.

## Paired static candidate

Apply only to a derived copy after both the executable hash and both original
byte sequences match exactly. Never modify `originals/`.

| Purpose | VA / file offset | Exact original | Prospective replacement |
| --- | --- | --- | --- |
| Set result 2 and skip only the interactive loop | `0x004A786B` / `0x000A6C6B` | `FF D7 2B 05 34 12 7F 00 99` | `89 6C 24 10 E9 E2 01 00 00` |
| Convert the displaced HIGHLOW relocation to ABSOLUTE padding | target RVA `0x000A786F` / relocation-entry file offset `0x000FA912` | `6F 38` (`0x386F`) | `6F 08` (`0x086F`) |

At `0x004A7866`, EBP is explicitly set to 2. The first replacement decodes
as:

```text
004A786B  mov dword ptr [esp+0x10], ebp
004A786F  jmp 0x004A7A56
```

The jump displacement is exactly `0x1E2` from next PC `0x004A7874`. It
retains all temporary DirectDraw/surface setup through `0x004A7866`, skips
only the timing/fade/input/draw/flip loop, and enters the original cleanup at
`0x004A7A56`. The original tail restores the display mode, releases the
temporary surfaces and COM object, sets selector 2, writes
`0x00573FF4 = 0` and `0x00573FF0 = 1`, and returns through the existing
epilogue. Failures before the patch point keep their original failure paths.

The relocation change is inseparable from the code change. The overwritten
absolute operand at RVA `0x000A786F` has HIGHLOW entry `0x386F` in the
RVA-`0x000A7000` relocation block. Leaving it active would make the PE loader
rewrite bytes inside the new relative jump when rebasing. Type-zero entry
`0x086F` is ignored ABSOLUTE padding while preserving entry size, count,
ordering, and block alignment. Neighboring relocation targets
`0x000A7862` and `0x000A7879` do not overlap the nine replacement bytes.
The PE checksum and Security Directory are both zero.

## Static limits and required runtime discriminator

- Selector 2 means the game's Direct3D route. The machine probe can still
  select a Direct3D software device, so selector 2 alone does not prove
  hardware acceleration.
- The `Examining Machine` probe/window must remain because it discovers and
  selects the real device and mode records.
- The interactive chooser should not render, but its retained temporary
  display setup may still produce a brief blank/flash.
- The skipped helper would write the temporary chooser surface pitch to
  `0x0059F7F4`. Actual-surface lock paths independently set and clear this
  global, so this is not a static blocker; actual surface behavior remains a
  runtime check.
- Host GPU execution versus a host software renderer such as llvmpipe is a
  separate environment check. An internal Direct3D log is not sufficient for
  that claim.

A future runtime candidate is accepted only if it:

1. records `INFO Direct3D - Device has hardware acceleration.`;
2. passes all six canonical renderer markers in [[START HERE]];
3. contains none of `SYSTEM MEMORY ONLY`, 320x200, or `INITSOFTRENDER`;
4. renders playable gameplay with correct actual-surface state;
5. omits the visible chooser, allowing only a brief display-mode flash;
6. repeats across fresh restarts and completes scoped process/resource cleanup;
7. separately proves the intended host GPU path when that distinction matters.

Until that experiment exists, [[Wine Linux Play Baseline]] remains
authoritative: select hardware manually and judge the complete new log.

## Implementation boundary

If exposed as an option later, `--auto-hardware` should be a project-wrapper
option that verifies the exact retail hash and both original byte sequences,
builds a derived copy under `work/`, applies both changes atomically, verifies
the resulting bytes and exact inverse, and launches only that copy. It must
not be represented as a native argument passed to retail `bugs.exe`.

See [[PC automatic Direct3D startup candidate]] for the agent-facing
implementation checklist and
[[Decision Log#DEC-20260816-132 - Retain manual hardware selection until the paired candidate passes runtime]]
for the decision boundary.
