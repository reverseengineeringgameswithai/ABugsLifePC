---
type: session
date: 2026-08-19
agent: Codex
topic: R2c Wine prefix and CD gate correction
tags:
  - session
  - re/runtime
  - environment/wine
---

# 2026-08-19 1316 - Codex - R2c Wine prefix and CD gate correction

## Goal

Explain and correct the recurring R2c launch failures before consuming RC0,
then make the established Wine content-drive setup unambiguous in Obsidian.

## Rejected setup boundary

The unexpected `RC0-F0` paths were quarantined without deletion. RC0-F0-001
then failed a host-path matcher before audit or launch. RC0-F0-002 launched but
stopped before input after a capture targeted the owned `177x63` selector
instead of the nested `640x480` root. RC0-F0-003 launched but displayed
`Please insert A Bug's Life CD.` and exited before input.

No RC0 renderer Return, carousel/title input, `SIGSTOP`, `SIGCONT`, process
memory read, or DAT write occurred in those preparations. Each launched setup
was cleaned with retained intermediate audits, exact owned-group cleanup,
recorded residual Wine-device provenance, and a clear final audit.

## Root cause

`play-pristine.sh` was passed `--prefix
/home/dev/ABLPC/work/wine/baseline`. The attempted setup repointed
`$HOME/.wine/dosdevices/r:`, which belongs to a different prefix and therefore
cannot affect that launch. The baseline prefix's `R:` link still targeted the
earlier F0-retail-002 stage.

The rejected RC0-F0-003 log records `LOADING : App run from .`, then a
drive-less `LOAD : Loading file \cd\cd.txt.`, then the fatal missing-file/CD
path. By contrast, all three accepted R2b arms record the installed-layout
identities `App run from R:\PC\BUGS` and `LOAD : Loading file
R:\PC\BUGS\cd\cd.txt.`. `EXP-20260811-004` established the same
installed-layout fallback mechanism on day one.

RC0-F0-004 later proved that `No CD-ROM found` alone is nondiscriminating: its
log contains that line twice while successfully loading the exact
`R:\PC\BUGS\cd\cd.txt` path. The raw `cd-gate.txt` receipt is preserved and a
separate correction receipt records why its `rejection_markers=absent` label
is false. That run also preserved a stale `chooser-guard.txt` label for
transient window `14680065`; `window-transition.txt` and `session.env`
identify the real selector as `14680071`. Future guards resolve the current
`SELECTOR_WINDOW` and require the exact same-PID `640x480` `Bugs` window.

## Correction

The active baseline-prefix `R:` link was restored to
`/home/dev/ABLPC/work/copies/BUGS_PC-full-disc`. The exact retail sentinel is
`PC/BUGS/CD/CD.TXT`, SHA-256
`6ceffd34caf1b53332d76b344864bed1fbcd71ef1415312db9ed995fcd91a74d`; baseline
`user.reg` records `"r:"="cdrom"`.

The environment notes, autonomous-control procedure, EXP-002, Current State,
and roadmap now require each per-arm full-disc stage to be mapped through
`work/wine/baseline/dosdevices/r:`, verified before launch, confirmed by the
accepted `R:\PC\BUGS\cd\cd.txt` log path before renderer input, and restored
after the clear post-close audit. They explicitly reject relying on
`$HOME/.wine` and distinguish the small pre-renderer selector from the nested
root capture surface.

## Next action

James accepted the CD/prefix correction but rejected stale active instructions
that generalized historical Down/Return success into a universal software
default. The authoritative environment, operating-manual, capability, function,
current-state, and decision surfaces now treat old sequences as run-scoped;
new retail experiments must pre-register selector input and classify only from
the complete log. R2c remains RC0 no-direction followed only conditionally by
the sole fresh one-Down RC1. The M4 compatibility validator now pins that
corrected evidence rule instead of requiring the falsified deterministic-Down
sentence.

A later clean-pre-audited RC0 preparation passed the corrected CD path and
showed that the owned `177x63` `A Bug's Life` window is transient setup UI,
replaced by the same PID's actual owned `640x480` `Bugs` chooser. An
ImageMagick root capture waited for interaction until the chooser timeout
selected software; no input was sent, so RC0 was not consumed. After exact
cleanup and a clear audit, `capture-fixture-002` initially appeared to validate
the non-interactive `ffmpeg` X11 command because it produced two byte-identical
`640x480` PNGs and clean lifecycle audits. That interpretation was provisional;
the later live run below disproved that the PNGs contained game pixels.

That fixture conclusion was later falsified by RC0-F0-005. The fresh live run
passed source, baseline-prefix, installed-layout CD, PID, and current
same-PID-`Bugs`-`640x480` window gates. Its first `ffmpeg` capture is uniform
black at PNG SHA-256 `724319c36...c6931`, byte-identical to both fixture
images; decoded RGB is uniform and hashes to `0b150fd3...58366`. The backend
captured the rootless Xwayland black root, not the game surface. A malformed
receipt command and then an over-broad guard against the preliminary `Native
software render mode is FALSE` line allowed chooser timeout before a valid
triplet. No directional/Return input, signal, read, or DAT write occurred.
Normal close and group TERM were insufficient; exact guarded group KILL and
post-audit residual-device cleanup produced a clear final audit, and retail
`R:` was restored. The packet is retained under the rejected namespace and did
not consume RC0.

R2c now restores the earlier live-validated asynchronous compositor backend,
`GAMESCOPE_WAYLAND_DISPLAY=gamescope-0 gamescopectl screenshot <absolute-new-path>`,
followed by a size-stable wait and strict non-black/non-uniform/exact-640x480/
known-chooser image gates. Pixels prove only chooser presence. The committed
`scripts/r2c-rc0-executor.py` owns every launch, identity, capture, Return,
classification, receipt, and cleanup step before any fresh retry.

That executor revision was protocol-specific rather than configurable: it
accepted no path arguments and pinned retail source plus the stage/pending
identities for setup 006. The later RC0-F0-006 transition rejection and
DEC-20260819-154 supersede those consumed identities with setup 007. It
requires `R:` initially retail, applies a `3.000 s`
deadline to the compositor command, and uses the direct PC-autonomous XTEST
focus/keydown/0.180-s/keyup-in-finally sequence because `send-keys.py` remains
fixture-only under the governing boundary. It rehashes before Return and again
requires the exact live PID/window/stage mapping/hashes before hardware handoff.

Commit and obtain James acceptance of this corrected preflight. Then launch a
fresh RC0 under the unchanged no-direction renderer branch. The face-8
localizer remained uncreated and prohibited until F0 passed and its packet was
committed and James-accepted.

## Links

- [[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]
- [[Wine Linux Play Baseline]]
- [[PC autonomous game control]]
- [[EXP-20260811-004 - Wine launch and CD sentinel gate]]
- [[New-level authoring roadmap (terrain, collision, materials)]]
