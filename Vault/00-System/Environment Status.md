---
type: environment
status: active
updated: 2026-10-29
tags: [environment/status]
---

# Environment Status

<!-- briefing: Current runtime handoff -->
## Current runtime handoff

**No game is open (2026-10-29).** The last runtime work was the two read-only
hardware arms of [[EXP-20261018-013 - Options screens and the creature gate live]]
(2026-10-18). They ran on reflink copies
`work/copies/EXP-20261018-013-{options,citysquare}` of a derived build (EXE
`c3d8b207…`, auto-hardware), with a private null sink and controllers disabled
in the private prefix. Each passed 6/6 markers, was closed through its packet
under `work/experiments/EXP-20261018-013/`, and had its `bugs.log` moved into
the packet. `make session-audit` was clean before each launch, after each
close and at the end.

**Read-only tooling audit (2026-10-07):**
`reports/kev/EXP-20261007-001/session-audit.txt` reports no game processes,
sinks or open sessions (`clean: true`). The existing local Kev server and
browser were used and left running; this session launched no service or game.
[[EXP-20261007-001 - Local Kev evidence classification probe]].

**Before the next arm:** run `make session-audit` and account for what it
reports, launch from a derived copy under `work/copies/` (the retail hash with
the manual hardware selection, or the auto-hardware build through
`scripts/make-auto-hardware`), and close through the arm's own packet.
[[PC autonomous game control]] remains authoritative; CAP-010 remains
fixture-only. Historical PIDs do not carry forward.

## Harness summary

Command-reported versions are in the generated block under
[[#Tool inventory]]; these are the functional limits recorded for each part.

- **Wine and Gamescope.** The play and visual-research baseline is the
  unchanged retail EXE in a Wine 11.0 (Staging) prefix with the working
  directory mapped as `R:\PC\BUGS` (EXP-20260811-004), hardware acceleration,
  and Gamescope nested at 640×480 ([[Wine Linux Play Baseline]],
  [[EXP-20260812-007 - Gamescope hardware presentation baseline]]). Hardware
  arms must pass the six-marker gate in [[START HERE#Before touching evidence]].
- **86Box.** A Windows 95 OSR2 machine runs the real executable outside Wine;
  its GDB stub build reads and writes guest memory (Gate 2), with residual
  tests open (`KU-077`), and the install is a driven session, not a script
  (`KU-078`) ([[86Box Win95 RE harness]]). The Windows 98 SE profile in
  [[86Box Reference Machine]] has no installer media. PCem is not installed
  ([[PCem Cross-Validation]]).
- **Windows debug VM.** KVM and libvirt work; Windows media and a licence are
  absent, so the VM is not built ([[Windows Debug VM]]).
- **Ghidra.** Ghidra with PyGhidra produces the static exports under
  `static/exports/`. Query them with `scripts/ghidra-query.py`, after reading
  [[Ghidra export structure and caveats]]. REA was trialled and kept optional
  ([[EXP-20261012-001 - REA Ghidra analysis trial]]).
- **Debuggers and capture.** `scripts/gdb-harness.py` drives GDB with
  natural-pause hardware watchpoints under Wine WoW64 (DEC-20260812-006) and
  unexpected-signal-safe control
  ([[EXP-20260812-030 - Unexpected-signal-safe GDB control]]). `rr` cannot
  record while Wine's `ntsync` driver is present (`KU-028`); CRIU is blocked by
  the same process shape (`make criu-check`, DEC-20260817-143); apitrace
  captures through EGL (`KU-030`). The flight recorder's write trace is in
  [[Flight Recorder]].
- **Session and memory tools.** `scripts/game-session.py`, `send-keys.py` and
  `wait-for.py` are fixture-validated only (CAP-010,
  [[Session control plane]]). `game-memory.py`'s read, snapshot and restore are
  live-validated ([[EXP-20260817-188 - Live game-memory read save restore validation]]);
  any write needs fresh permission, a compare-before-write guard and a receipt.
- **Python.** The project venv carries the parsers, harness and tests;
  [[Python and C reverse-engineering split]] sets when code moves to C.

## Human annotations

- **Historical instrumentation:** rr/ntsync, focus gating, R2q activation and
  emulator limits retain their dedicated evidence; this task does not activate them.
- **Obsidian:** `Vault/` remains the project vault. Markdown, wikilinks and stable
  settings are preserved. Workspace/layout files remain local and ignored;
  [[Obsidian Setup]] owns setup. No UI launch or layout reset.

## Historical record

[[Environment Status history through 2026-09-26]] preserves the previous note verbatim. [[Session Index]] indexes the original session records. Historical permissions and process IDs do not carry forward.

## Tool inventory

The generated block below was refreshed with `make doctor` on September 26.
It records command-reported versions and presence checks, not functional
acceptance of every tool. The script uses fixed labels for some installed
applications, including Obsidian and the pinned 86Box download. The preceding
August inventory remains in the historical snapshot.

<!-- BEGIN GENERATED: doctor -->

```text
ABLPC doctor
Generated: 2026-09-26T16:43:34-04:00

Fedora             Fedora Linux 44 (Workstation Edition)
Kernel             7.0.11-200.fc44.x86_64
Architecture       x86_64
CPU virtualization available
KVM                /dev/kvm accessible
Python             Python 3.14.6
Java               openjdk version "25.0.3" 2026-04-21
Wine               wine-11.0 (Staging)
Gamescope          gamescope-3.16.25-1.fc44.x86_64
QEMU               QEMU emulator version 10.2.2 (qemu-10.2.2-1.fc44)
libvirt            12.0.0
virt-manager       not installed
virt-install       not installed
radare2            radare2 5.9.8 0 @ linux-x86-64
Git                git version 2.54.0
strace             not installed
GDB                GNU gdb (Fedora Linux) 17.1-6.fc44
rr                 rr version 5.9.0
apitrace           apitrace 0.0-unknown
perf_event_paranoid 1 (rr needs <=1)
ptrace_scope       0
ripgrep            ripgrep 15.2.0 (rev e89fff89ac)
fzf                not installed
Codex              codex-cli 0.157.1
Claude             2.1.283 (Claude Code)
Ghidra JDK         openjdk version "21.0.12" 2026-07-21 LTS
Ghidra             12.1.2
PyGhidra           3.1.0
86Box              6.0 build 9001 (project-local)
PCem               not installed
Obsidian           1.13.6 (official extracted AppImage payload)
Python venv        Python 3.14.6
virtqemud socket   active
libvirt system     reachable
default network    yes
```

<!-- END GENERATED: doctor -->
