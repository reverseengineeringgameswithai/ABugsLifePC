---
type: environment
id: ENV-86BOX-WIN95-HARNESS
status: active
updated: 2026-10-02
tags:
  - environment/86box
  - re/runtime
  - how-to
---

# 86Box Win95 RE harness

A reproducible **Windows 95 OSR2 + A Bug's Life** machine running under **86Box**,
built to enable Gate 2 (host-side guest-memory access via 86Box's GDB stub — see
[[Decision Log#DEC-20260817-146 - Guest memory read write watch is a hard prerequisite, tested before the determinism build]]
and `KU-077`). This is a **separate environment** from the Fedora/Wine dev box; it
runs the real PC executable on real Win95, so its behaviour is PC-native, not
Wine-mediated.

**Status (2026-08-18):** built and working — the game boots to its level-select
menu at 640×480 DirectDraw. **Gate 2 (the GDB probe) has NOT been run yet**; that
uses the `gdbstub` build against the same disk. **KU-076 is still untested here**
(the CONVPSXTPAGE8 level-load) because entering a level needs the mouse and the
menu is point-and-click. Narrative + every bug solved:
[[2026-08-18 0330 - Claude - Win95 and A Bug's Life installed in 86Box]].

**Superseded later on 2026-08-18:** Gate 2 read and write were proven with a
stub build from the 86Box `v6.0` tag, `work/86box/86box-v6-gdbstub`, and
**KU-076 was resolved here**: Training loaded to playable 3D with no
`CONVPSXTPAGE8` fault. See
[[2026-08-18 0500 - Claude - Live gameplay memory read and KU-076 resolution]]
and `KU-076`/`KU-077` in [[Known Unknowns]]. A write-watchpoint also fired in
[[EXP-20260818-001 - Watchpoint path and first forensic tuple for Flik position]].
KU-077's residual tests (A/D side effects, more than four watchpoints) stay open.

## Two 86Box builds, one disk

The Win95 disk image is **portable between builds**. Use:

- **Stock** `tools/86box/86Box-Linux-x86_64-b9001.AppImage` — has the **dynarec**
  (fast). Use for install and for just running/playing the game.
- **gdbstub** `tools/86box/86Box-gdbstub-628ce40.AppImage` — `GDBSTUB=ON` forces
  `DYNAREC=OFF` (interpreter, slow) but exposes the GDB stub on `:12345`. Use only
  for the Gate-2 probe. Built per
  [[2026-08-17 2330 - Claude - 86Box GDB stub feasibility for guest memory access]].
  Superseded 2026-08-18: this build's interpreter halts in BIOS POST, so it
  never reaches Win95. The working stub build is `work/86box/86box-v6-gdbstub`
  (tag `v6.0`); it also runs the interpreter, not the dynarec (`KU-077`).

## Artifacts (all under git-ignored `work/86box/`)

- `disk/win95_c.img` — the live game-installed disk (2,064,384,000 B, 63/16/4000
  CHS, FAT16). `disk/win95_c_clean.img` — pristine Win95 (pre-game).
  `disk/win95_c_game.img` — snapshot after the game install.
- `config/86box.cfg` (+ `config/nvr/430vx.nvr` = CMOS with the corrected boot
  order). `media/win95_osr2.iso`, `media/bugs_pc.iso` — copies of `originals/`
  (never run 86Box against `originals/`).
- `floppy/win95boot_orig.img` (the OSR2 boot floppy, extracted from the ISO's El
  Torito), `floppy/win95boot_pa.img` (phase-A variant).
- `build/` — the guest files pushed in with mtools (`CONFIG.SYS*`, `AUTOEXEC.BAT*`,
  `MSBATCH.INF`, `MSDOS.SYS`, `PA_AUTOEXEC.BAT`, `PLAY.BAT`).
- `emu.sh` (headless start/shot/key/stop helper), `mtoolsrc` (drive-C: mtools
  definition), `launch-on-host.sh` (open it natively on the Fedora desktop).
- ROMs: `tools/86box/roms/` (686bx/Voodoo/AWE ROMs already present).

## Machine config (`work/86box/config/86box.cfg`)

Intel **i430VX** board, **Pentium-S 200 MHz**, **64 MB**, **S3 Trio64V2/DX PCI**
(`s3_trio64v2dx_pci`), **SB16**, PS/2 mouse+keyboard, `qt_software` renderer. HDD
on IDE `0:0` (`63,16,4000` geometry), CD (ATAPI) on IDE `1:0`, 1.44 MB floppy.
`cpu_use_dynarec = 1` for the stock build; the gdbstub build ignores it
(interpreter). **BIOS boot sequence is `C,A,SCSI`** (persisted in the `.nvr`) — see
gotcha #2. Device internal names were discovered by grepping the 86Box binary
(`work/86box/probe-devs.sh`).

## Reproducing it from scratch

### 1. Headless container
`podman run -d --name abl-win95 --security-opt label=disable -v
$PWD/work/86box:/vm -v $PWD/tools/86box:/tools:ro ubuntu:24.04 sleep infinity`
(SELinux needs `label=disable`, else the bind mounts are permission-denied).
Install: `xvfb x11vnc imagemagick x11-utils mtools xdotool parted dosfstools mbr`
and the stock AppImage's runtime libs. Extract the stock AppImage once
(`--appimage-extract`) and run it via its **AppRun** (sets `LD_LIBRARY_PATH`;
running the inner binary directly fails on `libserialport`).

### 2. Prepare the disk (host-side, no root/loopback — all mtools)
`truncate -s 2064384000 win95_c.img` (≤2 GB — FAT16 limit, gotcha #1). Then with
`MTOOLSRC` pointing at a `drive c:` def (`partition=1 cylinders=4000 heads=16
sectors=63 mformat_only`): `mpartition -I/-c -t 6/-a c:`, `mformat c:`, then
**`install-mbr win95_c.img`** (writes the MBR boot code — mtools does NOT, gotcha
#3). The FAT16 VBR + system files come from a one-time in-emulator `sys c:` (the
phase-A floppy).

### 3. Win95 OSR2 unattended install
Boot the **OSR2 boot floppy** (extract `[BOOT]/Boot-1.44M.img` from the ISO with
`7z`; it carries the Oak `CD1.SYS` + `MSCDEX`). Two-phase: (A) a floppy whose
`AUTOEXEC.BAT` runs `sys c:` to make C: bootable; (B) eject floppy, boot C:, whose
`AUTOEXEC.BAT` runs `X:\WIN95\SETUP.EXE C:\MSBATCH.INF /IS /IM`. `MSBATCH.INF`
(git-ignored, holds the **product key** — never copy it into the Vault) uses
`Express=1`, `ProductKey`, `[NameAndOrg]`, `EBD=0`, `NoPrompt2Boot=1`. **The OEM
Certificate-of-Authenticity dialog must be typed by hand** — msbatch cannot fill
its segmented `xxxxx-OEM-xxxxxxx-xxxxx` field, and the boxes auto-advance when full
(type the 17 digits continuously, no Tabs).

### 4. Deploy the game to the HDD (bypasses the CD, gotcha #5)
The real-mode ATAPI CD driver hits 86Box regression
[#5432](https://github.com/86Box/86Box/issues/5432) (CDR101 "not ready") on builds
≥6700 — so the CD is unreliable inside the guest. Instead, extract the game on the
host (`7z x bugs_pc.iso`) and mtools-copy it to **`C:\PC\BUGS\`**: `bugs.exe`
(retail, sha256 `97c95ba5…`) + the `CD/` asset tree (`/PC/BUGS/CD/`) + `MSVCRT.DLL`
/ `MSVCIRT.DLL`. The 178 MB `AUDIO` (music) and 206 MB `TEMP` (`.BUG` cutscenes)
are trimmed for a ~59 MB core; they live in `work/86box/gamefiles/held/` if
needed. Install DirectX with `DXSETUP.EXE` (from `/DIRECTX`). **Remove the
real-mode CD driver** from the guest `CONFIG.SYS`/`AUTOEXEC.BAT` so no D: drive
exists (gotcha #4). Run from `C:\PC\BUGS` (`PLAY.BAT` does `cd \PC\BUGS` +
`bugs.exe log cheat`).

## Headless operation

Xvfb on `:99` (must be launched with `setsid` so it survives the `podman exec`;
clear stale `/tmp/.X99-lock` first). Observe with ImageMagick `import -window
root`. **Input is XTEST via `xdotool`** — do NOT use `xdotool --window` (that uses
XSendEvent, which 86Box ignores, exactly like the game). Letter keys need
`--clearmodifiers`; dialog buttons respond to `Alt+<accelerator>` or `Space` on the
focused control; `windowfocus` throws a harmless `BadMatch` but XTEST still lands.

## Driving the game into a level headless (validated EXP-20260818-001)

No window manager runs on `:99`, so X uses **PointerRoot** focus: keyboard goes to
whatever window the pointer is **over**. The whole recipe follows from that.

1. **Launch:** Start → Run (`Ctrl+Esc`, then `r`) → `command.com` → in the DOS box
   `cd \pc\bugs` then `bugs.exe log cheat`. There is **no `PLAY.BAT`** on the HDD;
   the only exe is `BUGS.EXE`. Give the `cd` its own `Return` with a pause, or it
   merges with the next line.
2. **Focus for every keypress:** `xdotool mousemove 330 300` to park the pointer
   **over the game canvas** (do *not* click — a click captures the mouse, and while
   the mouse is captured the carousel ignores keys). Then send keys with XTEST.
3. **Level-select carousel** ("fliks journey"): it is **keyboard-driven** — `Right`/
   `Left` (quick taps) rotate; **training is the start position** (1 Right =
   Anthill, matching [[PC autonomous game control]]). The arrows on screen are hints,
   not mouse buttons; mouse clicks do nothing useful (relative PS/2 mouse, no
   absolute positioning).
4. **Confirm = a *held* key.** The menu **polls** the keyboard, so a quick
   `Return` tap is missed. `keydown Return; sleep 0.5; keyup Return` selects the
   level; the same held-`Space` advances the "Training Level" title into gameplay.
   Disable auto-repeat around held keys (`xset r off` / `xset r on`) so the key
   stays cleanly down. Held movement keys (`Up`) then walk Flik.

Correction to the old "menu is mouse-only, native is the only way" note below: the
carousel **is** fully keyboard/XTEST-drivable with the above; native is convenient
but not required.

## Viewing / driving it yourself

`bash work/86box/launch-on-host.sh` opens the **stock** build natively on the
Fedora desktop (`QT_QPA_PLATFORM=xcb`, `APPIMAGE_EXTRACT_AND_RUN=1`), pointed at the
same `config/` + `disk/`. Only **one** 86Box may touch the disk at a time. Win95
will ScanDisk on first boot if the previous stop was unclean. The game menu is
point-and-click (mouse), so native is the easy way to play; the container/XTEST
path can only drive keyboard-reachable UI.

## Gotchas index (bugs solved, all with evidence in the session note)

1. FAT16 partition max is 2 GB → disk sized to ~1.97 GB.
2. Award default boot order `A,C,SCSI` tries the empty floppy and stalls → set
   `C,A,SCSI` in BIOS Setup, persisted in the `.nvr`.
3. **mtools writes the partition table but NOT the MBR boot loader** → the classic
   "hang at *Verifying DMI Pool Data*". Fix: `install-mbr`.
4. Removing the floppy *drive* (not just the disk) mismatches CMOS → "Floppy
   disk(s) fail" F1. Keep the drive, empty the disk.
5. Real-mode CD driver → CDR101 (86Box #5432). Deploy the game to HDD instead.
6. The game's CD gate loads from a **detected CD-ROM drive** if one exists
   (`D:\pc\bugs\cd\cd.txt`) and errors if that read fails; with **no** CD drive it
   falls back to the app layout (`C:\PC\BUGS\CD\CD.TXT`) — matching
   [[EXP-20260811-004 - Wine launch and CD sentinel gate]] and
   [[FUNC-97C95BA5572D-00403B90]].

## Next

Run **Gate 2** on the gdbstub build against `disk/win95_c.img` (procedure in
[[2026-08-17 2330 - Claude - 86Box GDB stub feasibility for guest memory access]]),
and close **KU-076** by entering a level and watching the CONVPSXTPAGE8 load.

Both were done on 2026-08-18 (see the status note above). What remains is
KU-077's residual tests.
