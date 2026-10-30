---
type: environment
status: confirmed
created: 2026-08-12
updated: 2026-10-02
evidence:
  - EXP-20260812-005
  - EXP-20260812-007
  - EXP-20260812-010
  - EXP-20260812-029
tags:
  - environment/wine
  - workflow/play
---

# Wine Linux Play Baseline

## Supported configuration

The current Linux play and visual-research baseline is:

- unchanged `bugs.exe`, SHA-256 `97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`;
- derived content under `work/copies/`, never `originals/`;
- Wine 11.0 (Staging) with `work/wine/baseline`;
- the game working directory shaped as `R:\PC\BUGS` through the prefix mapping established by `EXP-20260811-004`;
- **hardware acceleration**, the second option in the opening renderer selector;
- Gamescope nested at 640×480 with aspect-preserving `fit` scaling to the host output.

Run the verified wrapper from the repository root:

```bash
./scripts/play-pristine.sh
```

For the user's preferred ongoing research presentation, use:

```bash
./scripts/play-pristine.sh --research --windowed --mute
```

`--windowed` omits Gamescope fullscreen and defaults to a 1280x960 4:3
desktop window unless `--output` is supplied. `--mute` routes only this
invocation to a private PipeWire null sink and unloads it on launcher exit;
the game's DirectSound/audio path still runs. Both options were dry-run and
live validated in `EXP-20260812-029`. During the accepted launch, the game's
sink input was attached to the private sink, and the sink was absent after
scoped cleanup.

The default output is the tested 2560×1440 display. On another display:

```bash
./scripts/play-pristine.sh --output 1920x1080
```

## Renderer selection matters

Do not assume the retail chooser's current/default selection and do not infer
it from chooser pixels. Historical C0 produced software after no directional
input, while historical C1 and later accepted R2b arms produced hardware after
one Down; F0-001 and F0-002 later produced software after one Down. Those are
run-scoped observations, not a deterministic rule for a fresh process.

Every renderer-facing retail experiment must pre-register its exact selector
sequence and classify the result only from the complete log. The historical R2c
retail branch used fresh RC0 with no directional input before Return. Only if
RC0's complete log proved software could the sole fresh RC1 send exactly one
Down, settle, and Return. There was no third attempt. R2c moved to the
auto-hardware build on 2026-08-19. [[EXP-20260816-143 - Automatic Direct3D startup static audit]]
proves there is no native retail renderer command-line argument. The separate
guarded auto-hardware derived build is accepted only at its own hash. See
[[PC automatic Direct3D startup candidate]] rather than guessing parameters.

For renderer-facing reverse engineering, the selection is an evidence gate.
Require all six positive markers in the complete new log segment:

- require `Native software render mode is FALSE`;
- require `RenderMode set to Direct3d render mode`;
- require `INFO Screen mode 640x480x16 selected.`;
- require `SYSTEM : OnlySystemMemory status VIDEO MEMORY ONLY.`;
- require `D3DAPPCREATE : Mode set to 640x480.`;
- require `INIT : Starting Direct3D renderer.`;
- reject the run if it enters `INITSOFTRENDER`.
- also reject the run if any positive marker is absent or it records `SYSTEM
  MEMORY ONLY` or 320x200.

Do not infer the selected code path from intended input or a screenshot. A
software run is valid only when the bounded experiment explicitly asks about
software rendering.

**Confirmed:** the retained software run logs a 320×200 software surface, while the tested hardware run logs Direct3D at 640×480×16. Evidence: `RUN-WINE-20260812-000215`, `RUN-WINE-20260812-013633`, and [[EXP-20260812-007 - Gamescope hardware presentation baseline]].

`EXP-20260812-010` applies this gate to matched mod comparisons and rejects a
preliminary run that accidentally retained the default software option.

### Skipping the manual selection: `--auto-hardware`

```bash
./scripts/play-pristine.sh --auto-hardware --windowed --mute
```

`--auto-hardware` builds (or reuses) the guarded auto-hardware patched copy
(`scripts/make-auto-hardware`, output SHA-256
`1e1d5099b200e71ce25aa53d06c2f30eb7c2ca88bcd1642f52970065c8a9c41f`, cached at
`work/copies/auto-hardware/bugs.exe`) and launches **that** exe so the game
boots straight into hardware Direct3D with no manual chooser. The patch edits
only the executable; the selected game directory and its experiment-specific
content-drive mapping remain unchanged. The retail exe itself has no
renderer-selection argument, so a plain launch still requires its
experiment's pre-registered selector sequence and the full six-marker log
gate. Runtime-accepted in
[[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]] /
[[EXP-20260816-151 - Independent auto-hardware runtime audit]]; see
[[PC automatic Direct3D startup candidate]]. Still verify the six markers on
any renderer-facing arm.

## Scaling and filtering

Gamescope `fit` retains the 4:3 aspect ratio. On a 2560×1440 display, this produces approximately 1920×1440 centered output with black side bars. It does not stretch the game to 16:9.

The wrapper defaults to `nearest`, which is crisp:

```bash
./scripts/play-pristine.sh --filter nearest
```

For a softer resample without changing the aspect ratio:

```bash
./scripts/play-pristine.sh --filter linear
```

Neither filter is currently claimed to be historically authoritative.

## Research mode

For the tested level selector and game-generated log:

```bash
./scripts/play-pristine.sh --research
```

This adds the known `log cheat mpeg` research arguments. Ordinary play uses only the tested `mpeg` argument. Note that `mpeg` **disables** all FMV cutscenes ([[PC FMV playback]]). In both modes the wrapper verifies the executable hash and refuses a game directory outside `work/copies/`.

## Mandatory content-drive preflight

`play-pristine.sh` does **not** create or repoint a Wine drive. Its default
prefix is `/home/dev/ABLPC/work/wine/baseline`, so only mappings under
`work/wine/baseline/dosdevices/` affect this launcher. A similarly named link
under `$HOME/.wine/dosdevices/` is irrelevant when `--prefix
work/wine/baseline` is used.

The accepted R2b arms exposed each exact full-disc work copy as this prefix's
`R:` drive and logged `LOAD : Loading file R:\PC\BUGS\cd\cd.txt.`. For a
per-arm copy, perform this preflight before the immediate pre-launch session
audit:

```bash
ROOT=/home/dev/ABLPC
PREFIX="$ROOT/work/wine/baseline"
STAGE="$ROOT/work/copies/<exact-full-disc-arm>"

test -f "$STAGE/PC/BUGS/bugs.exe"
test -f "$STAGE/PC/BUGS/CD/CD.TXT"
test "$(sha256sum "$STAGE/PC/BUGS/CD/CD.TXT" | awk '{print $1}')" = \
  6ceffd34caf1b53332d76b344864bed1fbcd71ef1415312db9ed995fcd91a74d
rg -q '^"r:"="cdrom"$' "$PREFIX/user.reg"
ln -sfn "$STAGE" "$PREFIX/dosdevices/r:"
test "$(readlink -f "$PREFIX/dosdevices/r:")" = "$STAGE"
```

Launch with both paths bound to that same identity:

```bash
./scripts/play-pristine.sh \
  --prefix "$PREFIX" \
  --game-dir "$STAGE/PC/BUGS" \
  --research --windowed --mute
```

Before any renderer input, reject the setup unless the new log contains both
`LOADING : App run from R:\PC\BUGS.` and `LOAD : Loading file
R:\PC\BUGS\cd\cd.txt.`. `No CD-ROM found` alone is nondiscriminating: a
directory-backed mapping can fail the game's CD-drive scan and still succeed
through the installed-layout path. The wrong-prefix rejection is the
drive-less `LOAD : Loading file \cd\cd.txt.` fallback, the fatal
missing-file/CD prompt, or absence of either required installed-layout
identity.

After the process is closed and the mandatory post-close session audit is
clear, restore `work/wine/baseline/dosdevices/r:` to
`/home/dev/ABLPC/work/copies/BUGS_PC-full-disc` and verify the resolved link.
Historical notes also mention `Y:` mappings for other experiments; that does
not replace the experiment-specific `R:` receipt above. Never infer the active
mapping from a link in `$HOME/.wine`.

Observed 2026-10-02 (audit, `readlink`): this prefix's `r:` still targets the
pending P0A stage `work/copies/EXP-20260820-005/P0A-auto-hardware-retail-001`,
which [[EXP-20260820-005 - R2p task lifecycle diagnostic]] left unrestored on
purpose; `y:` is retail `BUGS_PC-full-disc`. The `ln -sfn` above would replace
that retained mapping. Decision (2026-10-02): leave it. R2p is paused, its
protocol restores `R:` only after a clean zero-process audit, and the next
baseline arm's preflight re-links `R:` anyway.

## Scope and limitations

- **Confirmed:** this configuration reaches playable Direct3D gameplay under the recorded Fedora/Wine environment.
- **Inferred:** the earlier unusually small gameplay was caused principally by selecting the 320×200 software renderer inside the 640×480 Gamescope surface.
- **Unknown:** exact equivalence to a period Windows 98 graphics driver, monitor scaling, or any online comparison video.
- **Confirmed at the launcher boundary:** `--windowed --mute` retains the
  hardware renderer and game audio initialization while constraining captures
  to the isolated game surface and discarding final audio output at a private
  sink (`EXP-20260812-029`). This is not evidence about audio content or
  period-correct presentation.
