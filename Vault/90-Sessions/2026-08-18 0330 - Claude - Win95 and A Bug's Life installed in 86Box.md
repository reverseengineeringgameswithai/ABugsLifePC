---
type: session
date: 2026-08-18
agent: Claude
status: complete
tags:
  - session
  - re/runtime
  - environment/86box
---

# Win95 and A Bug's Life installed in 86Box

## Agent

Claude.

## Goal

Stand up the real PC game on **real Windows 95** inside **86Box**, headless and as
unattended as possible, to become the runtime substrate for Gate 2 (host-side
guest-memory access via the GDB stub). The reusable recipe and machine config live
in [[86Box Win95 RE harness]]; this note is the narrative and the evidence for each
problem solved. The user supplied the Win95 OSR2 media and the OEM product key
(kept out of the Vault) and chose the **unattended/headless** path.

## Outcome

**A Bug's Life boots to its level-select menu (640×480 DirectDraw) on Win95 OSR2 in
86Box.** The install worked end-to-end; the only manual guest input was the OEM
certificate number. This is the environment, not the result — **Gate 2 (the GDB
probe) has not been run**, and **KU-076 (the CONVPSXTPAGE8 level load) is still
untested** because the menu is point-and-click and I could only drive the keyboard
headlessly.

## Headless method

Everything ran inside a throwaway `podman` container (`abl-win95`, `ubuntu:24.04`,
`--security-opt label=disable` for the SELinux bind mounts). No window on the host:
Xvfb on `:99`, screenshots via ImageMagick `import`, input via `xdotool` **XTEST**.
Key input lessons: `xdotool --window` uses XSendEvent, which 86Box ignores (like the
game) — plain XTEST with focus works; letter keys need `--clearmodifiers`; Xvfb +
86Box must be `setsid`-detached or they die when the `podman exec` returns.

## Windows 95 install — problems and fixes (evidence)

1. **FAT16 2 GB limit.** A single FAT16 partition maxes at 2 GB; the first 2.1 GB
   disk could not be one partition. Fix: sized the disk to 63/16/4000 CHS ≈
   1.97 GB. Evidence: `mformat` succeeded, `mdir c:` showed the WIN95 volume with
   2,064,056,320 B free.
2. **Boot order.** The Award i430VX BIOS default `A,C,SCSI` tried the (empty)
   floppy first and hung at *Verifying DMI Pool Data*. Fixed by setting boot
   sequence to `C,A,SCSI` in BIOS Setup (driven by XTEST keystrokes) and saving to
   the `.nvr`. Evidence: POST screenshots before/after; `nvr/430vx.nvr` created.
3. **Missing MBR boot code (the real cause of the DMI hang).** `od` of the disk
   showed the MBR's first 446 bytes all-zero while the VBR was a valid `MSWIN4.1`
   boot sector — mtools' `mpartition` writes the partition table but not the MBR
   boot loader, so the BIOS jumped into zeros. Fix: `install-mbr` (from the Debian
   `mbr` pkg); MBR then began `fc 31 c0 8e d0…` and the disk booted. This unblocked
   the entire install.
4. **CMOS checksum / mouse_type.** A fresh `.nvr` throws a CMOS-checksum F1 once
   (persists after); a minimal 86Box config must set `[Input devices] mouse_type`
   or `config_load` NULL-derefs (86Box `config.c:787`).
5. **Unattended setup.** Booted the OSR2 boot floppy (extracted from the ISO's El
   Torito), two-phase (`sys c:` to make C: bootable, then boot C: → `SETUP.EXE
   C:\MSBATCH.INF /IS /IM`). `MSBATCH.INF` (`Express=1`, `ProductKey`, name/org,
   `EBD=0`, `NoPrompt2Boot=1`) carried it through EULA→copy→reboots→desktop
   unattended, **except** the OEM **Certificate of Authenticity**: msbatch left it
   `-OEM-` (empty segments), so the `xxxxx-OEM-xxxxxxx-xxxxx` boxes were typed by
   hand (they auto-advance when full — type the 17 digits continuously).

## Game deployment — problems and fixes (evidence)

6. **CD-ROM regression.** In-guest the real-mode Oak CD driver returned repeated
   `CDR101: Not ready reading drive D` / read once then failed — the known 86Box
   regression [#5432](https://github.com/86Box/86Box/issues/5432) (real-mode ATAPI
   CD on builds ≥6700; we are on b9001). So the CD is not a reliable in-guest
   source.
7. **Deploy to HDD instead.** Extracted the game from `bugs_pc.iso` on the host.
   The runnable exe is the ISO-root `BUGS.EXE` (retail, sha256 `97c95ba5…`), not
   anything under `/PC/BUGS/` (which holds only the `CD/` asset tree). Placed at
   **`C:\PC\BUGS\`** — `bugs.exe` + `CD/` + `MSVCRT.DLL`/`MSVCIRT.DLL` — matching
   the known-good Wine "installed layout" (`work/copies/BUGS_PC-full-disc`). Trimmed
   the 178 MB `AUDIO` (music) and 206 MB `TEMP` (`.BUG` FMV cutscenes) → 59 MB core
   copied via mtools. DirectX installed with `DXSETUP.EXE`.
8. **The CD gate (decisive).** `bugs.log` was explicit:
   ```
   LOADING : App run from C:\BUGS.
   LOADING : Files will be loaded off D:.
   LOAD : Loading file D:\pc\bugs\cd\cd.txt.
   FATAL ERROR - Failed to load file D:\pc\bugs\cd\cd.txt - error was Invalid argument.
   ```
   The game picks a **detected CD-ROM drive** (D:) and errors when that read fails
   — it does not fall back while a CD drive exists. Removing the real-mode CD driver
   (so there is **no** D:) made it use the app layout `C:\PC\BUGS\CD\CD.TXT` and
   pass, exactly as [[EXP-20260811-004 - Wine launch and CD sentinel gate]] and
   [[FUNC-97C95BA5572D-00403B90]] describe (drive scan unsatisfied → local
   fallback). Also required CWD = `C:\PC\BUGS` at launch.

With no CD drive and the game at `C:\PC\BUGS`, `bugs.exe log cheat` reached the
level-select menu (Flik's Journey / Training), 119 Hz. Screenshot retained.

## KU-076 status

**Untested here.** Entering a level is a point-and-click menu action; Enter/Space
did not select and Alt+F4 did not quit (fullscreen DirectDraw). Reaching the
CONVPSXTPAGE8 level load (the discriminator for whether that crash is Wine-9.0-
specific) needs the mouse — do it via a native launch or an 86Box mouse-capture
pass. KU-076 updated to reflect this.

## Handoff for the user

`work/86box/launch-on-host.sh` opens the stock build natively on the Fedora desktop
against the same disk/config, so the user can watch and use the mouse. Backups:
`disk/win95_c_clean.img` (pre-game) and `disk/win95_c_game.img` (post-game).

## Changes made

New: [[86Box Win95 RE harness]], this note, `DEC-20260818-148`. Updated:
[[Current State]], [[Known Unknowns]] (`KU-076`, `KU-078`). No repo **code** changed.
All disk images, ISOs, floppies and helper scripts live under git-ignored
`work/86box/`; the product key exists only in git-ignored `work/86box/build/
MSBATCH.INF` and the guest registry — it is **not** in any tracked note.

## Unresolved / next

Gate 2 (the GDB probe on the gdbstub build) and KU-076 (enter a level) — both
listed in [[86Box Win95 RE harness]]. The install workflow should also be turned
into scripts/a `make` target so it is one-command reproducible rather than a driven
session (`KU-078`).

## Process audit

All game/86Box/Win95 execution was inside the `abl-win95` podman container on Xvfb
`:99`; on the host only `86Box --help`/AppImage inspection and mtools/7z/od ran. No
`originals/` writes (ISOs were copied to `work/86box/media/`). Host state: the
git-ignored `work/86box/` tree and the `abl-win95` container + `abl-win95-img`
image (ephemeral, deps only). The container's emulator was left stopped
(zombie processes only) so the disk is free for a native launch.
