---
type: environment
status: confirmed
created: 2026-08-16
updated: 2026-10-29
evidence:
  - EXP-20260816-144
  - EXP-20260816-143
tags:
  - environment/wine
  - workflow/play
  - re/runtime
---

# PC autonomous game control

> **2026-09-28, physical controllers:** Wine passes host game controllers to
> the game, so a controller the user is using elsewhere can move Flik and mix
> with scripted input. Launch with `scripts/soil-trigger-runtime-probe.py launch
> ... --disable-controllers`. That sets winebus `Enable SDL`=0,
> `DisableHidraw`=1 and `DisableInput`=1 in the private prefix copy only, never
> host-wide. Then confirm that no owned process holds `/dev/input` or hidraw
> handles. EXP-20260928-001.


Command-level recipe for driving the exact retail PC game under Gamescope
without a human at the keyboard.

> **Implementation.** [[Session control plane]] implements this recipe as
> `scripts/game-session.py` and its companions, including the XTEST-only
> delivery, held presses, focus handling, six-marker gate, and
> memory-confirmed carousel navigation described below. Those tools are
> fixture-validated and **not yet live-validated** (CAP-010), so this note
> remains the authoritative procedure and the two must be kept in agreement. This fills the gap noted in
[[EXP-20260816-143 - Automatic Direct3D startup static audit]] (documented
selection procedure, no command-level recipe) and is confirmed live in
[[EXP-20260816-144 - Runtime grain-gate visual mapping]].

## Launch and discovery

First perform [[Wine Linux Play Baseline#Mandatory content-drive preflight]].
For the historical R2c procedure this meant that
`work/wine/baseline/dosdevices/r:` resolves to the exact per-arm full-disc
stage, not merely that `$HOME/.wine/dosdevices/r:` exists. Require the staged
`PC/BUGS/CD/CD.TXT` sentinel and its frozen hash, the baseline-prefix `r:`
`cdrom` registry entry, and both post-start log identities `LOADING : App run
from R:\PC\BUGS.` and `LOAD : Loading file R:\PC\BUGS\cd\cd.txt.` before
renderer input. `No CD-ROM found` alone is nondiscriminating. A drive-less
`LOAD : Loading file \cd\cd.txt.` fallback, fatal missing-file/CD prompt, or
absence of either required identity is a pre-input rejection. After the
transient setup window disappears, the input/capture guard must resolve the
current `SELECTOR_WINDOW` and require that exact window to be named `Bugs`, be
`640x480`, and belong to the recorded guarded game PID.

Launch detached so the process group is your own; each `gamescope --backend
wayland` creates its own nested Xwayland on a fresh display (`:2`, then `:3`,
...):

```bash
setsid ./scripts/play-pristine.sh --research --windowed --mute \
  > launch.out 2>&1 < /dev/null & disown
```

Discover the owned windows on the nested display (mirror
`scripts/play-pristine-with-inputs.py`): find the Xwayland whose process group
is yours, then `DISPLAY=$d xdotool search --class bugs.exe`. The first owned
`A Bug's Life` transient setup window may be `177x63`; it is **not** the
renderer chooser. Wait for it to disappear and for the same guarded game PID
to create the owned `Bugs` window at exactly `640x480`. That second window is
the chooser and later game window. Guard its PID under the owned process group,
`cwd` as the intended work copy, and the expected executable hash before
input.

Do not use ImageMagick `import -screen` here: it waits for interactive
selection. Do not use `import -window` on the transient setup window: it
captures only `177x63`. Do not use X11-root `ffmpeg`: RC0-F0-005 and both
`capture-fixture-002` frames are the same uniform black `640x480` PNG (SHA-256
`724319c36...c6931`), proving command completion against the rootless Xwayland
black root rather than game-pixel capture.

Use the game-surface compositor backend only:

```bash
GAMESCOPE_WAYLAND_DISPLAY=gamescope-0 \
  gamescopectl screenshot /canonical/absolute/initially-nonexistent/frame.png
python3 scripts/wait-for.py file --path /canonical/absolute/initially-nonexistent/frame.png \
  --stable-ms 200 --poll-ms 20 --timeout 10
```

The command is asynchronous. Validate the settled PNG, not merely command
return: exact `640x480` decoded RGB, non-uniform pixels, not the known black
PNG/RGB hashes, and the experiment's frozen chooser-presence allowlist. A
chooser hash never identifies renderer selection. The former R2c retail RC0
branch used `scripts/r2c-rc0-executor.py`; it is now superseded historical
tooling and must not be launched.

For the historical R2c RC0 branch, resolving the current same-PID `640x480` `Bugs` window is
not sufficient to begin the acceptance triplet. RC0-F0-006 proved that early
compositor frames can be startup/fade transitions: decoded-RGB
`9124b62c...d6413` then `64a124c5...94359`, followed by the already-known
stable chooser. Do not allowlist either transition. The executor must wait the
frozen `4.000 s` with no input while polling the exact PID/window and
pre-Return log, then take the triplet. One absolute `45.000 s` deadline covers
launch through Return so the 60-second timeout cannot select a renderer first.
Persist every capture command receipt and image observation atomically before
evaluating triplet stability or allowlist membership. The next frozen packet
was RC0-F0-007; RC0-F0-006 remains a pre-input rejection.

Historical R2c used only `scripts/r2c-f0-auto-hardware.py`. It expects no chooser,
classifies hardware only from the complete six-marker game log, and sends the
demonstrated Anthill route exactly: `Right`, `Return`, `Return`. The staged
full-disc tree retains retail `bugs.exe`, but the guarded Wine command must name
canonical cache `/home/dev/ABLPC/work/copies/auto-hardware/bugs.exe`, hash
`1e1d5099...a9c41f`. Never receipt the staged retail executable as the actual
executed image. This route supports build-scoped experimentation only.

**Parallel-session caution:** if another agent/session is already running the
game, a bare `pgrep Xwayland | grep -v :0 | head -1` may return *their*
display. Always bind to the Xwayland in your own launcher's process group,
never the first non-`:0` display.

## Input delivery: XTEST only

Historical R2c did not use `scripts/send-keys.py`: under the current AGENTS
boundary that tool remains fixture-validated only and cannot supply runtime
evidence until CAP-010 closes. Its committed executor performs and receipts the
authoritative direct sequence instead: exact-window/PID guard,
`windowactivate --sync`, `windowfocus --sync`, focused-window and ownership
recheck, `xdotool keydown Return`, requested host sleep `0.180 s`, and
`xdotool keyup Return` in `finally`. A command timeout or failed recheck stops
the arm and invokes fail-closed cleanup.

The renderer chooser and menus read input with `GetAsyncKeyState`
(chooser at `0x004A7600`, import loaded at `0x004A7841`). Under Wine that
reflects **real** keyboard state, so synthetic `XSendEvent` input is ignored:

- `xdotool key --window <id> <key>` — **does not work** (synthetic; the game
  never sees it).
- `DISPLAY=$d xdotool windowfocus --sync <id>` then
  `DISPLAY=$d xdotool key <key>` (no `--window`) — **works** (XTEST injects
  real input to the focused window). This is the same reason the input-movie
  tooling uses XTEST (EXP-125).

## Hardware (Direct3D) selection

The chooser polls `VK_DOWN` (0x28) / `VK_UP` (0x26) to move the highlight,
`VK_RETURN` (0x0D) or `VK_SPACE` (0x20) to confirm, and times out to the
timeout after 60000 ms (`cmp dword [0x7f1170], 0xea60`). The fresh chooser's
selected state is not established by an assumed default and is not reliably
classified by a screenshot. Historical no-direction and one-Down runs have
produced different paths; their sequences are evidence only for those runs.

1. Pre-register the experiment's exact directional/no-direction sequence,
   settle interval, confirmation mechanism, and alternate-arm limit before
   launch. Do not adapt it from chooser pixels.
2. Wait for a temporally stable chooser and guard the focused owned selector
   window. Retain nested-root captures only as stability evidence.
3. Apply the pre-registered sequence through XTEST. Do not batch a directional
   key with Return.
4. **Accept only from the log**, never the screenshot: require all six
   [[START HERE]] markers (`Native software render mode is FALSE`,
   `RenderMode set to Direct3d render mode`, `Screen mode 640x480x16
   selected`, `OnlySystemMemory status VIDEO MEMORY ONLY`, `D3DAPPCREATE :
   Mode set to 640x480`, `INIT : Starting Direct3D renderer`) and reject any
   of `SYSTEM MEMORY ONLY`, `INITSOFTRENDER`, or a selected 320x200 gameplay
   surface. The `DDMODE ... 320x200x*` lines are the mode *enumeration* list,
   not the selected mode and are not a reject condition on their own.

Historical R2c pre-registered RC0 with no directional input before Return. Only if
RC0's complete log proved software could one fresh RC1 send exactly one Down,
wait `1.000 s`, and Return. Hardware graduated in-process into F0; RC1 software
stopped the experiment. There was no third attempt. R2c replaced this retail
branch with the auto-hardware build on 2026-08-19
([[EXP-20260819-002 - R2c Anthill face-8 freeze and localization protocol]]).

The game recreates `bugs.log` fresh on each `log`-argument launch, so read
the whole current log rather than a byte offset from a prior run.

## Level Select carousel

With the `cheat` argument, confirming hardware lands on the "fliks journey"
level-select carousel (centered name = current selection). Navigate with
`Right`/`Left` (XTEST), ~1 s between presses (do not hold), and confirm with
`Return`. The visible carousel order (researcher-provided) is:

| Right presses from start | Level |
| ---: | --- |
| 1 | Anthill |
| 2 | Tunnels |
| 3 | Council Chamber |
| 4 | Cliffside |
| 5 | Riverbed Canyon |
| 6 | Bird Nest |
| 7 | **City Entrance** |
| 8 | City Square |
| 9 | Bug Bar |
| 10 | Clover Forest |
| 11 | The Tree |
| 12 | Battle Arena |
| 13 | Anthill Pt 2 |
| 14 | Riverbed Flight |
| 15 | Canyon Showdown |

**Carousel position is not the internal level number.** The carousel/
progression order (above) is the Flik's Journey play order; the internal
level global `0x00861C84` is a separate engine index set only after a level
loads (observed: Anthill=1, Council Chamber=2, Tunnels=3, City Entrance=4 —
so City Entrance is progression 7 but internal index 4). Always confirm the
loaded level by reading `0x00861C84`, not by carousel position. The full
progression↔internal-index table is in
[[PC level roster and numbering]]. There is no observed in-level "return to
select"; `Escape` does not exit a loaded level, so switching levels requires
relaunching.

## The game runs only while focused

On this Gamescope/Wine setup the game advances its **logic/physics loop only
while its window holds input focus** ([[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]]).
Consequences:

- `process_vm_readv`/`writev` (snapshots, teleports, grain writes) work
  regardless of focus, but game responses (gate opening, gravity, gameplay
  updates) only occur while focused. A teleport above the floor that does not
  fall, or a threshold write that does not take effect, usually means the
  window is unfocused, not that the logic is wrong.
- Menu/carousel key presses are **dropped when focus lapses**. Re-focus
  (`xdotool windowactivate --sync` + `windowfocus --sync`) before every press,
  and confirm the carousel name by screenshot before selecting — a dropped
  press silently lands on the wrong level.
- To observe a logic-dependent result (gate state, fall, animation), hold
  focus across the wait: re-issue `windowactivate` between short sleeps, then
  read memory.

## Frame capture

`GAMESCOPE_WAYLAND_DISPLAY=gamescope-0 gamescopectl screenshot
<canonical-absolute-initially-nonexistent-path>` is the established game-only
backend. It is asynchronous: wait for file existence and size stability, then
validate dimensions, decoded pixels, and the experiment-specific image gate.
Use `gamescope-0` only when a clean pre-audit proves this is the first and sole
Gamescope instance.

## Cleanup

Terminate only your own process group and unload only your own private null
sink; re-audit for `gamescope`/`bugs.exe`/`gamescopereaper` survivors and
null sinks. Never terminate another session's instance. See
[[Agent Operating Manual#Runtime instance lifecycle]].

## Key presses must be held, not tapped

`xdotool key <k>` presses and releases in about 12 ms. The menus poll
`GetAsyncKeyState`, so a tap frequently falls between polls and is silently
dropped: in `EXP-20260816-156` two of three carousel presses were lost that
way, landing the selection on the wrong level. Hold the key across several
frames instead:

```bash
DISPLAY=$d xdotool windowactivate --sync $w; DISPLAY=$d xdotool windowfocus --sync $w
DISPLAY=$d xdotool keydown Right; sleep 0.18; DISPLAY=$d xdotool keyup Right
```

Every press in both `EXP-20260816-156` arms landed with a ~180 ms hold. Still
verify the carousel name by screenshot before confirming.

## Gamescope's host window is a Wayland surface

With `--backend wayland` there is no X11 window on `:0`, so `xdotool` on the
host display cannot find or focus the session. Focus operations apply to the
game window on the **nested** display. In `EXP-20260816-156` the game advanced
normally (about 100% of one core, animating frames) with only nested-display
focus, so host focus was not required there; the focus caution in
`EXP-20260816-148` still applies to in-level logic waits.
## R2d live-grid capture receipt refinement

[[EXP-20260819-003 - R2d Anthill sampled phase calibration]] retains a separate compositor-command receipt and image observation for every live sample. Each receipt includes request start, compositor command return, file-stable, and hash-computed monotonic timestamps. A successful command return alone is not a completed capture; the file must stabilize and hash inside the frozen deadline, and adjacent requests may not overlap.

This is experiment-specific timing evidence, not a change to renderer selection. The exact auto-hardware executable and complete six-marker Direct3D log remain the renderer gate. R2d sends no input after title Return and performs no SIGSTOP/SIGCONT.

### Historical R2e classified-path provenance

For [[EXP-20260819-004 - R2e Anthill stable-background calibration]], compositor commands and raw receipts remain bound to their immutable `evidence/pending/...` acquisition paths. After a clean lifecycle rename, the independent validator recomputes existence and hashes from the corresponding `evidence/accepted/...` files. It must not rewrite a raw receipt or require the historical command to name a path that did not exist at acquisition time.

R2e used a fixed full-frame F0 identity plus three pinned animation-safe crops. Its authorized D1 later proved the full-frame requirement phase-sensitive: all three crops stayed exact across 121 captures while full-frame equality rejected. `lower-right-structure` remains excluded because consumed controls prove temporal content there. Do not rerun R2e.

### R2f phase-agnostic control capture

[[EXP-20260819-005 - R2f Anthill phase-agnostic stable-background calibration]] retained the immutable pending-to-classified receipt model, exact auto-hardware/Level01 route, fixed 121-frame grid, and three camera-control crops. Both authorized arms passed the complete six-marker Direct3D gate with no software marker. The aggregate later rejected on 233 D2 outside-mask observations and published no mask. This is not a renderer-selection or control-route failure; do not rerun the consumed identities.

### R2h D3 combined-mask holdout

[[EXP-20260819-006 - R2h Anthill D3 combined-mask holdout]] used one fresh argument-free D3 control through the same route. It pinned the consumed diagnostic, canonical binary mask, D1 reference, and prior D1/D2 identities; D3 had a distinct PID/start pair and accepted the finite-grid holdout. The consumed D3 authorization does not extend to a rerun or localizer successor.

### R2p passive task-lifecycle control

[[EXP-20260820-005 - R2p task lifecycle diagnostic]] freezes an unrun,
authorization-gated P0A exception to the ordinary focus-command recipe. It
opens two persistent nested-X11 connections before collection, retains one
exact focused `640x480` XID, and never activates, refocuses, reacquires, or
screenshots during its 521-point grid. The title Return worker and sampler are
independent because their requests coincide at sample 5. Per-sample guards use
direct X11, `/proc`, descriptor identity, and `R:` symlink reads rather than
subprocesses or full rehashes. Full source and asset hashes are pre/post gates.

P0A permits only normal guarded `Alt+F4` close. If that fails, evidence and the
stage mapping remain pending and no `SIGTERM`, `SIGKILL`, process-group, or
pidfd signal fallback is allowed without separate explicit authorization.
This P0A rule does not alter cleanup for other experiments.

P0A evidence classification also requires exact `game-session` `1.0.0` audit
timestamps and `R:` targets, an independent pre-navigation game-process
identity, full retained log-gate text, raw window/X-connection binding, and a
stage-to-retail `R:` restoration receipt. A collection failure cannot publish
as a procedural rejection unless that same complete prefix and lifecycle pass;
otherwise the packet remains pending. An isolated non-game Gamescope/Xwayland
fixture validates the two-connection X11/XTEST ABI and direct sub-10-ms window
guard, but is not runtime evidence about the game.

James's first implementation audit rejected exact `52d9a0f` before runtime.
Commit `b24890b` closed that audit's nine findings, but James's second audit
rejected five remaining finalization/validation counterexamples before runtime.
The corrected connection receipt is no longer an object-label string: each
persistent connection retains its actual `XConnectionNumber`, socket
device/inode/mode/target, Linux `SO_PEERCRED` PID/UID/GID, peer start ticks, and
a derived exact identity. Both peer PID/start pairs must equal the single owned
Xwayland PID/start/PGID/cmdline whose display token matches both connections.
Per-sample asset guards compare each exact live path's regular-file identity to
the already-open descriptor and frozen hash.
First-seen task metadata is admitted only when a post-metadata `stat` reread
matches the pre-metadata `(TID,start_ticks)` exactly.

Publication first moves the complete acquisition into the nonterminal
`evidence/published-unverified/P0A-AH-001`, then performs independent
validation, writes the post-validation receipt and manifest, revalidates the
exact current bytes, reauthenticates manifest closure, and performs
file/directory `fsync`. Only the final atomic rename creates accepted/rejected
evidence, after which both the removed-source and created-destination parents
are fsynced. Scientific publication requires timing success; rejected
publication permits only the exact derived timing failure retained in the
disposition.

James's third pre-run audit rejected exact `c05f167` because adjacent sample
deltas erased identity history across absences. P0A result classification now
derives an ordered presence history for every `(TID,start_ticks)` across all
521 samples. A changed start value remains reuse even across a gap; missing
metadata uses global first-seen sequence; and the same identity on both sides
of an absence fails closed as `task-identity-reappearance-unresolved` with
exact absent/reappearance boundaries. `short-lived` is limited to a
post-baseline identity that later disappears without reappearing and is not a
reuse endpoint.

The user has explicitly authorized the exact P0A runtime, but it
must not launch until James accepts the next immutable correction. This does not
widen the normal-close-only or no-signal boundary.

Superseded 2026-08-21: James accepted the P0A packet and P0A-AH-001 ran once
and is consumed. It loaded Level07 instead of Level01, collected no samples, and
its normal close failed ([[EXP-20260820-005 - R2p task lifecycle diagnostic]]).

## 2026-08-21 operational Level01 reconfirmation and P0B boundary

The deterministic direct PC route was never superseded by P0A's failed input
implementation. A fresh user-directed operational launch of auto-hardware
image `1e1d5099...c41f` waited for the exact LevelSelect marker and fixed
one-second no-input settle, then used the authoritative direct focused
`xdotool` delivery: Right held 180 ms, one-second gap, Return held 180 ms. The
log loaded Level01 and reached Start ClearLoadScreen; a final focused 180 ms
Return reached End ClearLoadScreen, End InitMainGame, and NextLife. Transient
frame `77f6eeff...84f598` visually corroborates live Anthill gameplay. No
process-memory access or save state occurred. This is an operational
reconfirmation rather than a new scientific packet.

P0A's Level07 result applies to its substituted persistent-X held-state input
path. It does not invalidate the direct route above. For the planned P0B
passive collector, direct `xdotool` sends only carousel Right and select
Return. After exact Level01/Start ClearLoadScreen, P0B opens two persistent X
connections and begins the unchanged 521-point grid; its independent worker
sends the sole title Return at sample 5. Sending a pre-grid title Return or a
second title Return would invalidate P0B. The operational game currently open
for the user is ineligible for adoption; a future P0B launch requires its own
fresh clean pre-audit, namespaces, `Y:` stage, James acceptance, and explicit
authorization without changing P0A's pending `R:` mapping or evidence.

The offline P0B implementation now enforces that split. Its production wrapper
fails closed as not runtime-authorized. It rejects existing or aliased
namespaces, authenticates complete P0A stage/pending manifests plus the exact
preserved `R:` link before and after, and refuses any dirty prelaunch audit. A
precollection failure may use the retained xdotool route only for guarded
normal `Alt_L+F4`; the existence of `collection.json` prohibits that fallback
permanently, leaving the persistent input connection as the sole normal-close
mechanism. Scientific acceptance requires the exact post-grid gameplay log
extension.

James rejected the first immutable packet at `2277b75` / `cf2f88c`. Most
importantly for operation, cloning the retail tree also cloned a stale
`PC/BUGS/bugs.log`, and xdotool receipts did not retain the exact nested
display. The correction deletes and fsyncs that staged log before launch,
retains an exact reset receipt, refuses symlink/non-regular/non-UTF-8/replaced
logs, binds every xdotool guard/key/settle to `runtime.x_display`, and checks
one append-only file identity across hardware, route, gameplay, and final-log
receipts. It also closes the audit's offline schema/publication/prohibited-
action boundaries. Focused offline tests passed 351/351 and the full repository
gate passed 2293/2293 with zero tracked-file violations; the next audit below
then rejected that exact candidate.

James's next immutable audit **REJECTED** exact `8b8d19d` / `e8b58c9`. For
live control, the material defects were a forward-slash wrong-level load that
could pass the pre-Right guard, and a later Level02 load that could be mistaken
for Level01 gameplay. The correction now shares one any-drive/either-slash
level-load parser across all live and retained gates and requires exactly one
total post-LevelSelect load, Level01, through the final gameplay log. The same
round closes exact P0A-manifest, X-window, audit, publication, connection, and
canonical-root validation gaps. The focused suite passes 396/396. This is an
offline correction only: the open operational game was not observed or
controlled, and P0B remains barred pending exact-commit James acceptance plus
fresh authorization.

The 396-test correction passed 2338/2338 full tests and became exact
`e0fa61a` / `02550b15`; James then **REJECTED** it. The control-relevant defect
was that a fresh wrong-level load before the sole LevelSelect marker could
still reach Right/Return because both paths inspected only the post-marker
suffix. The successor rejects any parsed load anywhere in the fresh
LevelSelect prefix before first input, and executor plus scientific/rejected
regressions pass in the 405/405 focused suite. The second defect was an offline
P0A entry-type raw exception. No live process was observed or controlled.

James then **ACCEPTED** the immutable offline design at exact `3c90a6f` /
`5fb8ea6`. Its focused suite passes 405/405 and the complete repository gate
passes 2347/2347 with zero tracked-file violations. Acceptance does not enable
the wrapper or authorize a game launch. At that checkpoint a future P0B arm
still needed fresh authorization; the next section records it. A clear
pre-audit and the exact frozen route remain mandatory, and the currently open
operational process cannot be adopted.

After that ACCEPT, the user replied `okay continue on`, authorizing exactly one
`P0B-AH-001` wrapper process invocation. One-shot means the first invocation
consumes the arm even if it fails before plan creation and is never retried.
If pending or terminal evidence exists, the activated source bytes remain
pinned because the packet authenticates them and namespace exclusivity is the
technical replay guard. Only a pre-namespace exit permits retiring the
entrypoint, while still leaving the authorization consumed. Before invoking,
all P0B namespaces must be absent and `make session-audit` must be exactly
clear.

That gate was not yet met. The prior operational game
`1978909/33236220` in Gamescope group `1978654` remains live on `:2`; the exact
activate/focus/unscoped-XTEST `Alt_L+F4` normal-close sequence did not clear it.
No signal fallback is authorized. Therefore no P0B path was created and the
authorized invocation was still unconsumed at that checkpoint. James
independently **ACCEPTED** the
minimal activation at exact `c3ad480` / `59acd5d` after 405/405 focused tests;
the exact tree also passed 2347/2347 full tests. The then-remaining gate was an
immediately preceding exact-clear session audit plus the frozen prechecks.

The user later explicitly authorized process killing. Exact group `1978654`
received TERM; only exact surviving `gamescopereaper 1978824/33236126` and
`winedevice 1978862/33236135` required guarded KILL. The following audit was
exactly clear, so the accepted P0B wrapper was invoked once after all frozen
checks matched. It completed the 521-sample collection but its own guarded
Alt+F4 normal close failed, leaving new group `2086248`, sink
`ablpc_mute_2086248`, the P0B stage mapping on `Y:`, and an exact 26-file
pending packet. The wrapper must never be invoked again.

Post-run signal recovery is a separate authorization and evidence namespace.
The additive candidate authenticates the untouched pending tree, rechecks
every frozen PID/start before exact group/helper TERM and survivor KILL,
records all polls and the exact sink action, requires a clear audit before
atomic/fsynced retail-`Y:` restoration, then proves a second clear audit,
unchanged P0A/`R:`, exact assets, and a closed recovered manifest. At that
checkpoint it had not run and required clean exact-commit James acceptance
first. It could not relabel the original run as normal-clean or authorize a
retry.

James rejected first implementation `575756d` / `004bf35d`: exact numeric and
command domains, group-census/error retention, event transitions and bounded
polls, complete immutable-tree/current-state checks, early one-shot
consumption, stable failure state, and genuine staged publication were not all
proved. No live inspection or signal occurred. The successor addresses those
boundaries and removes unauthenticated operator Git fields. James then rejected
exact `d4de863` for a retained nested numeric alias, post-deadline polling, and
check/rename overwrite races. The successor adds exact comparison, terminal
deadline enforcement, and atomic `RENAME_NOREPLACE`; it passes 48/48 recovery
plus 482/482 non-native P0B tests, native X, and 2395/2395 full tests. At that
checkpoint it remained unrun pending immutable commit and James ACCEPT.

The corrected recovery was subsequently accepted at exact `fae9b2f` and
invoked once. Its authorized group TERM began shutdown, but recovery failed
closed when the next identity guard saw still-present processes with cleared
command lines. It is consumed, did not restore `Y:`, and did not publish a
recovered result. Between the authenticated pre-recovery and post-TERM states,
160 bytes of shutdown text were appended to the original P0B `launch.stderr`.
Chronology, content, and retained-FD provenance make attribution to recovery
shutdown consistent, but it remains an inference. The current pending tree is
`1092fcb9...25f2`.

A separate, user-authorized operator cleanup at exact `4de8b08` was
James-accepted before execution. It targeted only three retained identities:
Gamescope `2086265/34784563`, gamescopereaper `2086416/34784596`, and
winedevice `2086454/34784605`. Individual TERM followed by fresh-guarded
survivor KILL cleared them. Both retained final audits are exactly clear, `Y:`
is retail, and `R:` remains P0A. James then accepted the 15-entry terminal
operator envelope `24df2fb7...d65b`. This does not make the P0B packet a normal
or recovered run and grants no future launch authority.
