# PC executable import categories

## Subject

- Binary: `BIN-97c95ba5572dce63`
- SHA-256: `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`
- Source: PE import table reported by `rabin2 -ij work/copies/BUGS_PC-disc/bugs.exe`
- Import records observed: 150
- Experiment: `EXP-20260811-003`

These are investigation categories, not proof that the game uses an API for a particular higher-level purpose. Categories can overlap.

## P0: DirectX creation and enumeration

| DLL | Import | Import address | Immediate value |
|---|---|---:|---|
| DDRAW.dll | `DirectDrawCreate` | `0x008644d8` | DirectDraw object creation |
| DDRAW.dll | `DirectDrawEnumerateA` | `0x008644d4` | DirectDraw device enumeration |
| DINPUT.dll | `DirectInputCreateA` | `0x00864508` | DirectInput object creation |
| DSOUND.dll | `DirectSoundCreate` | `0x00864538` | DirectSound object creation |
| DSOUND.dll | `DirectSoundEnumerateA` | `0x0086453c` | DirectSound device enumeration |

No separate Direct3D creation import was observed. Static evidence at `0x00411D00`, `0x0041F990`, and `0x00423A20` shows Direct3D interfaces being reached through DirectDraw/COM-style interface calls. The exact interface ownership still needs runtime confirmation.

## P0: File, path, and stream access

### KERNEL32 file and path APIs

- `CreateFileA` at `0x008646ac`
- `ReadFile` at `0x00864640`
- `WriteFile` at `0x0086464c`
- `SetFilePointer` at `0x00864624`
- `FlushFileBuffers` at `0x0086469c`
- `CloseHandle` at `0x008646c8`
- `DeleteFileA` at `0x00864670`
- `GetFileType` at `0x00864634`
- `GetCurrentDirectoryA` at `0x008645e0`
- `GetModuleFileNameA` at `0x00864628`

### WINMM multimedia stream APIs

- `mmioOpenA`, `mmioClose`
- `mmioRead`, `mmioWrite`
- `mmioSeek`
- `mmioDescend`, `mmioAscend`
- `mmioCreateChunk`, `mmioAdvance`
- `mmioGetInfo`, `mmioSetInfo`

The multimedia APIs are high-value candidates for audio or RIFF-family data, but an import alone does not identify the game format or caller.

## P0: COM lifecycle

- `CoInitialize` at `0x008648bc`
- `CoCreateInstance` at `0x008648c0`
- `CoUninitialize` at `0x008648c4`

The instantiated class IDs and interface roles remain unknown until their call sites are mapped.

## P1: Window creation and event loop

High-value USER32 imports include:

- `RegisterClassA`, `RegisterClassExA`
- `CreateWindowExA`, `DestroyWindow`
- `ShowWindow`, `UpdateWindow`, `SetFocus`
- `GetMessageA`, `PeekMessageA`
- `TranslateMessage`, `DispatchMessageA`, `TranslateAcceleratorA`
- `LoadIconA`, `LoadCursorA`, `ShowCursor`
- `GetClientRect`, `ClientToScreen`

Static cross-references place a capability-probe window and device enumeration at `0x0041F990`, and message processing plus display-mode handling at `0x004129A0`.

## P1: Process and runtime initialization

High-value KERNEL32 imports include:

- `GetCommandLineA`
- `GetModuleHandleA`
- `GetStartupInfoA`
- `GetVersion`
- `LoadLibraryA`, `GetProcAddress`
- `ExitProcess`
- heap, virtual-memory, thread, and critical-section APIs

The PE entry point at `0x004B1670` uses the first four of these before dispatching through a thunk to `0x0043DA40`.

## P1: Timing and synchronization

The import table includes Win32 timing and synchronization support, while WINMM provides multimedia timing. Exact game-loop timing ownership remains unmapped and should be established from callers rather than import names.

## P2: GDI, palette, text, and diagnostics

GDI32 and USER32 imports cover device contexts, palette queries, stock objects, text/dialog display, and window geometry. Static evidence at `0x00423A20` uses GDI palette queries during graphics-device setup. Other GDI imports may serve setup UI, diagnostics, or gameplay; they are not yet separated.

## P2: C runtime and platform support

A substantial fraction of the table supports the statically linked runtime and ordinary Win32 process behavior. For example, `0x004B8B50` wraps `CreateFileA` in logic consistent with runtime file-descriptor flags. Such functions should not be named as game subsystems without a game-code caller.

## Limitation

The current Ghidra JSON export reports zero external imports because the exporter does not enumerate Ghidra external locations correctly. That is an exporter limitation, not evidence that the PE has no imports. Until corrected, use the independent PE import table and direct Ghidra cross-references together.
