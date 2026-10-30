---
type: experiment
id: EXP-20261018-005
date: 2026-10-18
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Static disassembly (capstone) of retail bugs.exe with imports resolved through static/pe rabin2-imports.json, plus the EVENT lines of 579 bugs.log files saved by earlier Wine runs (retail and derived builds); no new game launch
question: What do the six event callbacks do, and is any event registered besides WINDOWS and DIRECTX (KU-071)?
result: The event table is the app's platform-layer registry. WINDOWS creates the window and the DIRECTX record wraps Direct3D, input and sound. The unnamed +0x08 slot is a per-frame poll; for WINDOWS it is the Win32 message pump, for DIRECTX a no-op. Both registrations run in every saved log that gets past the renderer chooser, and no other event name appears in any of 579 logs
status: complete-bounded
created: 2026-10-18
updated: 2026-10-18
evidence: [EXP-20260817-185, EXP-20260816-159, EXP-20260816-143, EXP-20260817-181]
tags: [experiment/static, experiment/runtime, re/events]
---

# EXP-20261018-005 - Event callbacks and registrations

## Question

[[EXP-20260817-185 - PC event subsystem static census]] mapped a 16-slot
callback table at `0x005982B0`. It left open what the six callbacks of its
two static registrations do, and whether anything else registers. Both are
in KU-071, and section 7 of [[Next Tasks]] lists it as a small static
closure.

## Method

- **Static.** Each callback was disassembled from entry to `ret`, with IAT
  slots named from `static/pe/…/rabin2-imports.json`, and the code around
  the registrations and the dispatch callers was read.
- **Runtime logs.** The EVENT lines of 579 `bugs.log` files under `dynamic/`,
  `work/experiments/` and `work/copies/` were counted. Registration logs
  "create function %s called" before the create callback and "added" after
  it (`0x0042DC14`, `0x0042DC35`). The lines between them are what the
  create callback logged.

## The callbacks

| Slot | `"WINDOWS"` (id 2) | `"DIRECTX"` (id 3) |
|---|---|---|
| `+0x04` create | `0x004AE580` | `0x0042BA60` |
| `+0x08` per-frame | `0x004AE780` | `0x0042BB30` |
| `+0x0C` destroy | `0x004AE810` | `0x0042BB50` |

### WINDOWS: the application window

- **Create** (`0x004AE580`–`0x004AE704`):
  - `CoInitialize`;
  - `LoadIconA` "AppIcon";
  - `RegisterClassExA` (on failure, `FormatMessageA` and `MessageBoxA`);
  - `CreateWindowExA` with class and title "Bugs", the handle stored at
    `0x0059F73C` and `0x005835A0` ("CreateWindowEx failed" otherwise);
  - `UpdateWindow`, `SetFocus`, `ShowCursor`;
  - `LoadAcceleratorsA` "AppAccel", stored at `0x0059F72C`.

  In the logs, "LOADING : App run from …" and "LOADING : No CD-ROM found"
  fall inside this callback.
- **Per frame** (`0x004AE780`–`0x004AE7E8`), the Win32 message pump:
  - `PeekMessageA(…, PM_REMOVE)` into `0x0059F710`;
  - on `WM_QUIT` (`0x12`), sets `0x0059F7C8 = 1` and returns 0;
  - otherwise `TranslateAcceleratorA` with the window and accelerators
    above, then `TranslateMessage` and `DispatchMessageA`, returning 1.
- **Destroy** (`0x004AE810`): `PostQuitMessage(0)`.

### DIRECTX: the renderer, input and sound

- **Create** `0x0042BA60` was already known as this record's create
  callback (EXP-185, EXP-159). The lines it logs show what it does:
  - it loads `cd.txt`;
  - "CONFIG : Base CD track";
  - "SYSTEM : OnlySystemMemory status…";
  - "D3DAPPCREATE : Mode set to 640x480";
  - the texture-format list.

  "INIT : Starting Direct3D renderer." follows the "added" line.
- **Per frame** (`0x0042BB30`): returns 1 and does nothing else.
- **Destroy** (`0x0042BB50`) calls, in order:
  - `0x0042F600`, which unacquires and releases the DirectInput keyboard
    device `0x00598B20` and the DirectInput object `0x00598B18`
    ([[EXP-20260817-181 - PC input subsystem static census]]);
  - `0x0049D390` (audio);
  - `0x0049E290`, which stops and releases the DirectSound object
    `0x007EDAE8` ([[FUNC-97C95BA5572D-004A3480]]);
  - `0x00424F90` (COM releases and GDI `DeleteObject`);
  - `0x0043E340` when that returns 0.

  In the shutdown log, the surface-restore attempts and "MEM : … tpage …
  destroyed" lines fall inside it.

### The per-frame slot

The dispatch pass `0x0042D980` calls every live record's `+0x08`. It has two
callers:

- the frame-begin routine `0x00405BE0` at `0x00405CB0`;
- the outer loop `0x0043DA40` at `0x0043DC5A`. That loop first calls
  `WaitMessage` (`0x0043DC54`) when `0x00590639` is 0 and `0x00573FF0` is
  nonzero, the classic idle wait of an inactive app.

So `+0x08` is a per-frame poll. Its only live users are WINDOWS's message
pump and DIRECTX's no-op. The name "poll" is inferred from those call sites
and those two bodies; no string names the slot.

## Registration order and shutdown

- **Startup.** The outer loop `0x0043DA40`, called from the entry
  `0x004B1670` at `0x004B17AA`:
  1. destroys all slots (`0x0043DAEB`);
  2. registers WINDOWS;
  3. if the render selector `0x0059F7F0` equals 2 (`ebp = 2` at
     `0x0043DAC9`), runs the renderer-choice screen `0x004A7600`
     ([[FUNC-97C95BA5572D-004A7600]]);
  4. registers DIRECTX.
- **Shutdown.** The quit path in `0x00405BE0`:
  1. logs "QUIT : Destroying Direct3D renderer." (`0x004C52B4`);
  2. destroys all slots (`0x00405C54`);
  3. calls `CoUninitialize`;
  4. logs "CheckForQuit : Code shutdown." (`0x004C528C`).

  The destroy-all pass walks from slot 15 down (`esi = 0x00598668`, slot
  15's `+0x34`), so DIRECTX (3) is destroyed before WINDOWS (2).

## Runtime logs

| EVENT lines | Logs |
|---|---:|
| WINDOWS created and added, DIRECTX created and added | 569 |
| WINDOWS only, the log ending at the renderer chooser ("SwitchDriverScreen") | 4 |
| as the first row, plus DIRECTX then WINDOWS destroyed and deleted (a clean quit) | 1 |
| none: runs that stopped before registration (four at a missing `cd.txt`, one during the machine examination) | 5 |

- **Names.** No other event name appears in any of the 579 logs; only
  `WINDOWS` and `DIRECTX` occur between the `>>>` and `<<<` of an EVENT line.
- **Retail runs.** The four WINDOWS-only logs are retail runs stopped at the
  chooser: EXP-20260819-002 RC0 and EXP-20260819-009's rejected A1 arms.
  They match step 3 of the startup order.
- **Function names.** The "%s" for the function name prints empty in every
  log.

## Confirmed, inferred, unknown

- **Confirmed (static).** The six callbacks' bodies and imports; the
  registration order with the chooser between; the shutdown path and its
  descending order.
- **Confirmed (static plus runtime logs).**
  - Both registrations execute.
  - Only those two events are registered in any saved run.
  - The create callbacks log what their code does, and the clean-quit log
    shows the destroy order the code predicts.
- **Inferred.** The name "per-frame poll" for `+0x08`.
- **Unknown, still open from EXP-185.**
  - The fields `+0x02`, `+0x30`, `+0x32` and `+0x38`, which are only ever
    zeroed.
  - The never-read global `0x005982AC`.
  - The name field's width.
  - Whether a computed call could reach the uncalled entry points.

  None bears on what the two live events do.

## Consequences

KU-071 is answered: the event table is the platform layer's lifecycle
registry for the window and the DirectX services, not a gameplay trigger
mechanism, which EXP-185 had already ruled out. The Event/scripting coverage
row can cite these two events' roles.
