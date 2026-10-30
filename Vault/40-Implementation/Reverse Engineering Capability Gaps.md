---
type: register
status: active
created: 2026-08-12
updated: 2026-10-02
tags:
  - implementation/tooling
  - register/capabilities
  - re/workflow
---

# Reverse Engineering Capability Gaps

This register explains which missing or incomplete capabilities would make the
PC reverse-engineering work safer, faster, or more discriminating. It is not a
second roadmap and it does not authorize privileged actions. [[Project Roadmap]]
still decides what work happens next; [[Environment Status]] records installed
state, and [[Known Unknowns]] records unresolved factual questions.

Use [[Capability Gap]] when a gap needs its own dossier. Each entry must state
the observed limitation, evidence, current workaround, acceptance test, and
authority boundary. A desired feature is not evidence that the current result
is weak, and an available feature is not automatically worth using.

## What would help most now

This ranking dates from 2026-08-17, when runtime instrumentation was the
focus. Since September the work has been mod authoring, and
[[Project Roadmap]] owns current priorities.

1. **Live validation of the session control plane (CAP-010).** The whole
   launch/address/close recipe is implemented and fixture-validated. The
   `game-memory` read/save/restore path is now partially live-validated
   (EXP-188); `game-session` launch/gate/navigation, `send-keys`, and
   `wait-for` have not run against the real game. Until an authorized arm
   confirms those, the manual procedure remains the only proven path for them,
   and only EXP-188's memory-path results in [[Session control plane]] may be
   cited as runtime evidence.
2. **Session checkpoint/restore (CAP-011).** There is no whole-process
   savestate (CRIU is blocked here, `make criu-check`), only same-process
   `.data` checkpoints through `game-memory` snapshot/restore (live round trip
   in EXP-188) and `scripts/savestate-hotkeys.py`. With no in-level
   return to the selector, every level-N experiment pays a full boot and
   carousel walk. This is now the single largest remaining cost per runtime
   arm, and it is actively steering work away from runtime evidence.
3. General staged hardware-point phases, stop predicates, and bounded
   register-relative reads would make other caller-to-data traces more
   discriminating (CAP-001). M2.17/M2.25 resolve fatal-signal,
   survival-receipt, and bounded submission-digest subsets; M2.27 adds one
   purpose-specific Direct3D pre/flush/post state machine. M2.18/M2.25 still
   show nearby execution points are unsafe continuation paths.
4. The bounded PC input-movie worker makes exact-window keyboard routes
   reproducible and hash-gated. Its opening-selector live validation is not
   engine-frame synchronization; KU-057 still needs a user-recorded Level03
   route paired with the read-only state trace (CAP-002).
5. An `rr`-compatible Wine synchronization environment would remove the
   four-slot hardware breakpoint limit and add replay/reverse execution
   (CAP-003).

## Active gaps

### CAP-001 — Safe staged and conditional debugger capture

- **Priority:** high; partially resolved by M2.17, M2.25, and M2.27. M2.20
  through M2.24 avoided the unsafe caller-gate surface; M2.27 uses conditioned
  data watches and no execution breakpoint.
- **Observed limitation:** watch-spec schemas 1/2/3/4 install one fixed set of at
  most four hardware points. They cannot arm a second phase after a guard,
  evaluate general stop predicates, or capture memory at a general
  register-relative expression. Harness 1.0 also continued every unclassified
  non-`SIGINT` signal and could turn a real `SIGSEGV` into false
  `target_reached`; harness 1.1/result schema 2 resolves that urgent subset and
  adds the independent survival receipt. Harness 1.2/result schema 3 adds one
  bounded ordered per-entry capture form. Harness 1.3/result schema 4 adds an
  exact Direct3D pre/flush/post state machine with fixed caller/root/page
  expressions, but does not supply general staged points or predicates.
- **Evidence:** [[EXP-20260812-027 - Plant10 entry 28 bounded negative]] needed
  a manual two-stage GDB attachment. [[EXP-20260812-028 - Plant10 post-title selected-entry negative]]
  could record fixed watches and registers, but its
  exploratory caller-gate arm's raw GDB output recorded `SIGSEGV` at its
  breakpoint PC even though the harness later reported cleanup and detach.
  [[EXP-20260812-029 - Fresh selected-entry chain debugger fault]] reproduces
  the same contradiction in the required fresh simultaneous four-point arm;
  raw GDB, winedbg, and a game-only fatal-error frame disprove the structured
  status and appended `NextLife` milestone. [[EXP-20260812-030 - Unexpected-signal-safe GDB control]]
  then proves structured terminal signal/PC, safe fixture `nopass` detach,
  required-receipt rejection, routine-signal compatibility, and a previously
  safe live watchpoint with five resumed/untraced samples.
  [[EXP-20260812-031 - Adjacent caller-gate continuation fault]] applies the
  hardened controller with only adjacent `0x0044D794`; it also receives
  same-PC `SIGSEGV`, while cleanup/detach, five live samples, and a later game-
  only frame prove safe target survival under `nopass` rather than safe
  continuation. [[EXP-20260813-038 - Per-entry submission-arena negative]]
  finds the same continuation failure at `0x0044C898`, then live-validates
  schema 3 with a safe post-call data watch, ordered entry identity, bounded
  digest metadata, coherent-zero handling, cleanup/detach, and required
  survival. [[EXP-20260813-040 - Direct3D retained-entry batch provenance]]
  live-validates schema 4 with three conditioned data watches, exact caller/
  root/page/order bounds, pre-reset segment accounting, no payload retention,
  cleanup/detach, no target signal, and required survival.
- **Current workaround:** use fixed allowlisted ranges and split phases across
  fresh matched runs where hardware points have a proven safe control. Require
  schema-2/3/4 survival for risky live arms; any `target_signal` is terminal. Do
  not use execution breakpoints at `0x0044C898` or nearby
  `0x0044D794/0x0044D79A` as continuation evidence. M2.25 instead used the
  exact post-call data-watch boundary at `0x0044C8AB`; M2.27 used only exact
  conditioned data watches after a static flush/reset preflight.
- **Desired acceptance:** a versioned phase schema that can install/delete its
  own hardware points after a named stop; bounded allowlisted expressions such
  as `$edi-8`; and per-stop predicates. Preserve the now-proven terminal signal,
  target-exit, required survival, schema-1 compatibility, and read-only
  `write_verbs: []` regressions.
- **Authority:** ordinary repository implementation; any future live point or
  execution control requires a new exact question and fresh explicit user
  authority.

### CAP-002 — Deterministic PC input movies

- **Priority:** high; partially resolved for exact target-window keyboard
  delivery. Version 1.3.0 fixes the confirmed 1.1.0 delivered-stream defect,
  but two exact-input arms reach different gameplay states. Event-specific
  Level03 acceptance remains.
- **Observed limitation:** [[PC input movies]] now supplies executable-hash-
  gated record/validate/replay/compare, exact target-window/process/focus
  checks, explicit keydown/keyup offsets, new-log/manual-delay/optional-frame-
  hash anchors, mandatory exact-window replay echo, schema-2-bound bounded
  post-anchor log/`ROUTINE` checkpoints with schema-1 playback, JSON receipts,
  and emergency held-key release. It
  remains keyboard-only and monotonic-wall-clock scheduled. It cannot observe
  the game's internal frame counter or atomically bind a runtime state sample
  to an input event.
- **Evidence:** hardware selection and title advancement were already
  reproducible with remote Down/Return. `EXP-20260812-032` records exact
  key-down/up and capture timestamps for one bounded trajectory; its controls
  are byte-identical at 11/12 same-index frames. `EXP-20260812-033` finds later
  global divergence after movement, proving timestamps are not an engine-
  synchronized contract. [[EXP-20260815-119 - PC input movie recorder and hardware replay]]
  adds 11 asset-free regressions plus one production window-only recording and
  two fresh accepted hardware replays of the same four-event movie. All four
  events dispatch, all keys release, receipt comparison agrees, drift remains
  below 1.8 ms, and each complete log passes all Direct3D/no-software gates.
  [[EXP-20260815-121 - First companion route replay divergence]] accepts
  306/306 dispatches and the hardware gates after one disclosed missing-Down
  compensation, but visibly and log-independently diverges at Level Select
  without loading Training. It proves that input acceptance is not gameplay
  acceptance for the manual-delay companion workflow.
  [[EXP-20260815-122 - Anchored companion record and replay controls]] adds 23
  focused offline fixtures for a shared Level Select log marker, explicit
  supervisor readiness events, replay command construction, recorded neutral-
  wait preservation, saved/next path separation, and retained-group cleanup.
  [[EXP-20260815-123 - Level Select anchored route gameplay desynchronization]]
  then accepts 300/300 live dispatch, Hardware gates, and Training entry, but
  the user observes later gameplay desynchronization. The marker is therefore
  live-accepted only for menu/level entry, not a complete route.
  [[EXP-20260815-124 - Replay echo identifies target input stream distortion]]
  rules out direct loss of the first gameplay `z` during replay loading and
  proves that pre-send receipt acceptance is not delivered-stream fidelity. A
  simultaneous exact-window echo contains 304 normalized events for the 300-
  event source, two extra `Right` up/down pairs, and multiple 15-39 ms timing/
  hold changes.
  [[EXP-20260815-125 - Persistent echoed replay and residual gameplay divergence]]
  replaces that emitter with persistent X11/XTEST plus mandatory exact-window
  echo. Two fresh arms deliver 300/300 exact events below 0.52 ms maximum
  target drift, yet one returns to Level Select and the other remains in
  Training. This closes the measured delivery defect but proves that exact
  wall-clock keyboard delivery alone is not deterministic gameplay.
- **Current workaround:** launch
  `scripts/play-pristine-with-inputs.py --research --windowed --mute` and use
  its separate Recording/Replay menus to discover the exact isolated
  Gamescope X11 game window and start or stop `scripts/input-movie.py` without
  manually entering PID, display, or window IDs. Version 1.3.0 defaults new
  gameplay recording to the first fresh `NextLife.` after initialization;
  Level Select is labeled menu only and manual delay remains weaker. Require
  exact target echo and runtime-log checkpoint agreement in at least two fresh
  replays. Treat event offsets as monotonic time, never as engine frames.
  `EXP-20260815-120` fixture-validates the original companion;
  `EXP-20260815-122` fixture-validates the corrective anchored workflow.
  Independently prove the reached game state; dispatch acceptance alone is
  insufficient.
- **Desired acceptance:** record and repeat the user-directed Level03 route
  from a fresh stable anchor through deliberate material-1 contact; first show
  source/target echo agreement, then pair both accepted replays with the read-
  only KU-057 state trace; retain current
  descriptor/material, flags, counter, and `NextLife`; and show agreement or
  preserve any divergence. Live-validate the chosen log anchor. Internal-
  frame synchronization and controller/gamepad input require separate work.
- **Authority:** ordinary repository implementation. Production capture uses
  `XSelectInput` only on one proved game window and must continue to refuse
  host input devices, display-wide capture, unrelated windows, focus loss,
  and process/window identity mismatch.

### CAP-003 — Deterministic Wine replay and reverse execution

- **Priority:** high, environment-blocked.
- **Observed limitation:** `rr` 5.9.0 cannot model Wine 11's `ntsync` ioctls;
  `/dev/ntsync` makes recording abort during Wine initialization.
- **Evidence:** `RUN-RR-20260812-183423`, `KU-028`, and
  [[Runtime Tooling#The ntsync blocker for rr]].
- **Current workaround:** at most four native hardware watch/breakpoints per
  run, plus repeated fresh runs and core snapshots.
- **Desired acceptance:** with `/dev/ntsync` genuinely absent, record one
  Training session, complete `rr replay -a`, pack it, and reproduce the known
  plant 10 slot access from replay.
- **Authority:** removing/restoring the kernel module requires explicit user
  authorization and root. The unfinished unprivileged namespace alternative
  may be developed without root.

### CAP-004 — Hardware-renderer steering and acceptance receipt

- **Priority:** medium-high; every renderer-facing experiment depends on it.
- **Observed limitation:** a fresh retail chooser's selected state cannot be
  assumed from a default or reliably classified from pixels. Historical
  no-direction and one-Down processes produced different paths. Each current
  experiment must pre-register its selector sequence and accept hardware only
  after checking the complete new log segment for the six positive Direct3D/
  video-memory/mode markers in [[START HERE]] and rejecting the software
  markers. The superseded retail R2c chooser calibration used no-direction RC0
  and one conditional fresh one-Down
  RC1. EXP-143 proves the exact retail executable has no native renderer
  argument.
- **Evidence:** `EXP-20260812-007`, [[Wine Linux Play Baseline]], the accepted
  M2.15 run log, and M2.16's rejected-too-fast preflight followed by its
  accepted separately timed renderer selection (`EXP-20260812-029`). M2.17
  independently rejects a software preflight and accepts the separately timed
  hardware path again (`EXP-20260812-030`). All accepted M2.19 and M2.20 arms
  pass the same gates under `--windowed --mute` (`EXP-20260812-032`,
  `EXP-20260812-033`). M2.27 independently proves `Native software render
  mode is FALSE`, Direct3D render mode, 640×480×16, and renderer startup in
  every accepted arm (`EXP-20260813-040`).
- **Current workaround:** isolated Gamescope window control plus exact log
  verification of all six positive markers and no software markers before
  accepting evidence; [[START HERE]] makes this fail-closed gate durable.
- **Static candidate:** [[PC automatic Direct3D startup candidate]] records a
  paired exact-byte code/relocation transform that retains chooser setup and
  cleanup while skipping its interactive loop. James accepts its static
  plausibility only; it is not implemented or runtime-proven.
  Superseded 2026-08-16: `scripts/make-auto-hardware` builds it, and
  [[EXP-20260816-150 - Automatic Direct3D startup runtime acceptance]] /
  [[EXP-20260816-151 - Independent auto-hardware runtime audit]] accept it at
  the derived build hash (renderer-level hardware Direct3D, no chooser input).
  The retail hash still needs the manual chooser sequence.
- **Desired acceptance:** a hash/byte-guarded derived-copy builder, exact
  inverse and receipt, repeated playable hardware Direct3D launches, actual-
  surface and chooser-visibility checks, complete cleanup, host-renderer proof
  where claimed, and a fresh James ratchet.
- **Authority:** ordinary repository implementation. Do not persist a game or
  Wine renderer setting until `KU-013` is resolved.

### CAP-005 — Event-correlated frame capture

- **Priority:** medium.
- **Observed limitation:** frozen capture is real and game-only, but
  `gamescopectl screenshot` is asynchronous and freeze/resume perturbation is
  not yet bounded against a free-running control. Captures are not directly
  correlated with debugger stop IDs or input receipts.
- **Evidence:** `RUN-FRZ-20260812-183223`, `KU-029`, and [[Runtime Tooling]].
  `EXP-20260812-032` and `EXP-20260812-033` link each asynchronous game-only
  capture to a timestamped input receipt and hash, but explicitly observe
  residual camera/animation phase and do not claim internal-frame correlation.
  M2.20's 18-way all-phase intersection is an experiment-local discriminator,
  not a substitute for atomic engine-frame capture.
- **Current workaround:** wait for the file, hash it, retain it only under
  ignored `work/`, describe the nearest log/debugger/input boundary, and use
  repeated samples plus an unchanged control when phase matters.
- **Desired acceptance:** one atomic receipt linking run ID, debugger or log
  event, input event, freeze/capture/resume timestamps, frame hash, and an
  unfrozen perturbation control.
- **Authority:** ordinary repository implementation; capture remains limited
  to the isolated 640×480 game surface.

### CAP-006 — More than four simultaneous access probes

- **Priority:** medium; largely solved if CAP-003 succeeds.
- **Observed limitation:** x86 debug registers cap the proven harness at four
  hardware points, forcing field-by-field runs and preventing a broad caller,
  callee, and data watch set in one event.
- **Evidence:** the M2.9–M2.15 experiment sequence and
  `DEC-20260812-019`.
- **Current workaround:** use static evidence to choose four exact probes,
  split hypotheses across matched runs, and use memory snapshots for residency
  rather than access timing.
- **Desired acceptance:** replay watchpoints, or a tested trace/multiplexing
  method that does not patch executable bytes and reports its coverage gaps.
- **Authority:** depends on the chosen implementation; software breakpoint
  patching is outside the currently accepted method unless separately tested
  and authorized.

### CAP-007 — CPU-to-GPU resource causality

- **Priority:** medium-later.
- **Observed limitation:** apitrace captures the real hardware EGL stream, but
  there is no automated correspondence from PC resource loads/runtime
  addresses to texture uploads and draws.
- **Evidence:** `RUN-APITRACE-20260812-184544` and `KU-030`.
- **Current workaround:** compare bounded control/mod traces and manually
  inspect upload formats, dimensions, call order, and rendered frames.
- **Desired acceptance:** a report that correlates Wine file/relay events,
  CPU-side hashes or addresses, EGL texture uploads, draw intervals, and a
  phase-matched game-only frame without claiming semantic identity from timing
  alone.
- **Authority:** ordinary tooling work; raw traces and frames remain ignored.

### CAP-008 — Full host file/system-call tracing

- **Priority:** low until a loader question requires it.
- **Observed limitation:** host `strace` is not installed; Wine relay and
  `+file` diagnostics do not expose every host syscall or file-descriptor
  transition.
- **Evidence:** [[Environment Status]] and `KU-006`.
- **Current workaround:** `wine-capture.sh --file-trace`, focused relay
  filters, game log paths, and debugger call-site evidence.
- **Desired acceptance:** install `strace`, capture only the isolated Wine
  process tree, filter sensitive/unrelated host paths, and preserve a curated
  evidence summary rather than raw host-wide output.
- **Authority:** package installation requires explicit user authorization and
  sudo.

### CAP-009 — Native Windows and period-correct reference environments

- **Priority:** deferred; not on the Wine-first critical path.
- **Observed limitation:** no modern Windows debugging VM or Windows 98
  reference machine can be completed without user-owned media/licenses and
  the remaining documented firmware requirements.
- **Evidence:** `KU-002`, `KU-004`, [[86Box Reference Machine]], and
  [[Project Charter]].
- **Current workaround:** treat the exact PC executable under controlled Wine
  as the behavioral authority for current milestones and label compatibility
  questions separately.
- **Desired acceptance:** reproducible, licensed VM manifests and matched
  input/capture procedures that compare the same executable/data hashes.
- **Authority:** user-supplied media and licenses are required; agents must not
  download them.

### CAP-010 — Autonomous live-session control

- **Priority:** high; implemented and fixture-validated on 2026-08-17. The
  `game-memory` read/save/restore path is now **partially live-validated**
  ([[EXP-20260817-188 - Live game-memory read save restore validation]]);
  `game-session`, `send-keys`, and `wait-for` remain **not live-validated**.
- **Observed limitation:** the complete live-session recipe existed only as
  prose in [[PC autonomous game control]]. Every arm re-derived the nested
  display, re-proved identity, re-drove the chooser, re-navigated the carousel
  by screenshot, and cleaned up by hand — roughly twenty sequential steps, and
  three findings (XTEST-only delivery, held presses, focus-gated logic) that
  were learned, not codified, and then re-learned at the cost of a wrong-level
  arm in `EXP-20260816-156`.
- **Evidence:** `EXP-20260816-144`, `EXP-20260816-148`, `EXP-20260816-156`,
  and the launch/cleanup sections of the 2026-08-15 runtime packets.
- **Current state:** [[Session control plane]] implements `game-session`,
  `game-memory`, `send-keys`, and `wait-for` over a shared `session_lib`, with
  a per-session ownership ledger under
  `dynamic/wine/RUN-SESSION-<stamp>/session.json`. 129 focused regressions run
  against a synthetic fixture that maps the real global addresses.
- **Live so far:** EXP-188 confirmed, against the running game, the
  identity/`state` reads, the single-contiguous-`.data` mapping, a full
  `.data` `snapshot`, and a `snapshot`→`poke`→`restore`→verify cycle that
  reverted a real global exactly. It did not exercise launch, the gate,
  navigation, `send-keys`, `wait-for`, a full-`.data` restore, or a
  restored *running* state. Later, [[EXP-20260818-004 - PC confirmation of the berry-type selector 0x0059D9A7]]
  used four user-authorized, compare-guarded `game-memory` pokes in a live
  pristine session; it did not exercise the other unvalidated parts.
- **Desired acceptance:** one authorized live arm in which the tool's gate
  verdict matches a hand-read log, its discovered PID/window/display match the
  manual procedure, `close` leaves an empty targeted audit, and the ledger
  accounts for every process it signalled. Only then may `level` navigation or
  a write verb be used live.
- **Authority:** ordinary repository implementation. Live use is a runtime
  launch and follows [[Agent Operating Manual#Runtime instance lifecycle]];
  write verbs additionally require fresh explicit user authority per use.

### CAP-011 — Session checkpoint and restore

- **Priority:** high; a same-session region checkpoint now exists
  (fixture-validated, plus one live 12-byte round trip in EXP-188), the
  durable cross-launch savestate does not and is blocked on this host.
- **Observed limitation:** `Escape` does not exit a loaded level and no
  in-level return to the selector is observed, so **changing level requires a
  full relaunch** ([[PC autonomous game control]]). Every arm therefore
  repeats boot, chooser, and carousel before any new observation, and a
  destroyed state — for example the Tunnels row-1 boundary lost during the
  `EXP-20260816-148` focus diagnosis — cannot be recovered without repeating
  the whole setup.
- **Evidence:** `EXP-20260816-144` (twelve gates on one repeated launch
  apparatus), `EXP-20260816-148` (`KU-060` residual destroyed mid-arm), and the
  two follow-ups parked as "optional" in those packets purely because a launch
  costs too much.
- **Current state — the in-process path (built).**
  `scripts/game-memory.py snapshot`/`restore` implement a **memory-only region
  checkpoint** ([[Session control plane]]). It captures curated game-data
  regions — by default the single writable `.data` section
  `0x004C1000`–`0x00864000`, which holds every identified global and is
  neither code nor stack — with a `SIGSTOP` freeze for atomicity, and writes
  them back into the **same process** (PID plus start ticks), refusing a
  different process or a level change by default. This amortizes one
  boot-plus-carousel across many experiment arms in one session, which is the
  costly repetition above. `scripts/savestate-hotkeys.py` (F5 save, F9 load
  by default, grabbed on the game's nested display) is a front end over the
  same verbs; its full interactive save/load flow is not yet proven
  ([[Session control plane]]). It is **not** a savestate: it carries no
  renderer/GPU, sound, file-position, thread-execution, or kernel/Wine state,
  and it does not survive a crash, a close, or a relaunch. **First live
  confirmation:** [[EXP-20260817-188 - Live game-memory read save restore validation]]
  ran a full `snapshot`→change→`restore`→verify cycle against the real game
  (12-byte region; a full-`.data` restore and a restored *running* state are
  still unproven).
- **Current state — the durable path (blocked, measured).**
  `scripts/criu-feasibility.py check` is a read-only survey. Run against the
  live game it reports **blocked**: the process holds an open `/dev/ntsync` fd
  and `ntsync` anonymous inodes — the exact driver that defeats `rr`
  (`KU-028`) — plus a GPU DRM fd and open X11/Wayland/PulseAudio sockets, 35
  hard-to-checkpoint fds in total, and a dump additionally needs
  `CAP_CHECKPOINT_RESTORE` or root. `criu` 4.2 is installed and the kernel has
  `CONFIG_CHECKPOINT_RESTORE`/`CONFIG_MEM_SOFT_DIRTY`, so the blocker is the
  Wine/GPU/ntsync process shape, not the tooling.
- **Desired acceptance (durable path):** with `/dev/ntsync` genuinely absent
  (the `KU-028` remedy) and the GPU/socket fds handled, capture a checkpoint at
  a known in-level state, restore it twice, and show both restored runs read
  identical position, level, flags, and `NextLife` and that ordinary gameplay
  continues. An 86Box/VM snapshot (`CAP-009`) is the alternative that avoids
  the fd problem entirely by checkpointing the whole machine.
- **Desired acceptance (in-process path):** the CAP-010 live arm plus one
  demonstration that a real snapshot/restore round trip reproduces an
  in-level state and that gameplay continues from it.
- **Authority:** the in-process path is ordinary implementation (restore is an
  authorized memory write per use). CRIU removal of `/dev/ntsync` and any real
  dump require user authorization and root; the VM route depends on `CAP-009`
  media.

### CAP-012 — Running the game without holding input focus

- **Priority:** medium-high.
- **Observed limitation:** the game advances its logic/physics loop **only
  while its window holds input focus**. Memory reads and writes work
  regardless, so a teleport that does not fall or a threshold write that does
  not take effect looks like a wrong hypothesis rather than a lost focus.
- **Evidence:** [[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]],
  `KU-060`. Previously recorded only in [[PC autonomous game control]] with no
  register entry.
- **Current workaround:** `wait-for --hold-focus` re-activates the window
  between polls, which makes a logic-dependent wait survive; it does not let
  two arms run concurrently or let an unattended wait proceed while the
  researcher uses the desktop.
- **Desired acceptance:** either a dedicated virtual seat/display in which the
  game window unconditionally holds focus, or evidence identifying the focus
  check itself so its effect can be described exactly rather than worked
  around.
- **Authority:** ordinary implementation for the display route; identifying
  the check is static analysis.

### CAP-013 — Level switching without relaunch

- **Priority:** medium; folded into CAP-011's cost but separable.
- **Observed limitation:** no observed in-level return to the level-select
  carousel; `Escape` does not exit a loaded level.
- **Evidence:** [[PC autonomous game control]].
- **Current workaround:** relaunch, then walk the carousel — now automated and
  self-verifying via [[Session control plane]], but still a full boot.
- **Desired acceptance:** either a static identification of a
  return-to-selector path, or an authorized write to the internal level global
  plus whatever load trigger it requires, demonstrated to reach a playable
  second level in one process. Writing `0x00861C84` alone is not expected to
  load a level; the dispatcher and its data load are separate.
- **Authority:** static analysis is ordinary work; any live write needs fresh
  explicit authority.

### CAP-014 — Execution coverage and call tracing

- **Priority:** medium.
- **Observed limitation:** answering "which functions run when I do X" costs
  four hardware watchpoints and a fresh arm per hypothesis. Nothing aggregates
  execution into a call census. `wine-capture.sh --deep` records Windows-API
  relay lines with no aggregation; `apitrace` records GL only.
- **Evidence:** the M2.9-M2.15 sequence, `CAP-006`, `DEC-20260812-019`.
- **Current workaround:** static reference enumeration plus targeted
  watchpoints, split across matched runs.
- **Desired acceptance:** a coverage or call trace of one bounded gameplay
  interval that names executed functions, reports its own coverage gaps, and
  does not patch executable bytes; validated by containing the functions that
  independent watchpoint evidence already proved execute.
- **Authority:** depends on mechanism. `rr` (CAP-003), a relay-log aggregator
  (ordinary work, no new authority), and instrumentation frameworks
  (separately authorized) differ sharply here; the relay aggregator is the
  only one available today.

### CAP-015 — Menu and frame state verification without a human eye

- **Priority:** medium; partially mitigated.
- **Observed limitation:** [[PC autonomous game control]] requires verifying
  the chooser highlight and the carousel level name **by screenshot** before
  confirming. There is no OCR, pixel-anchor, or image-diff helper, and
  `scripts/frozen-capture.sh` still refuses with
  `capture_backend_not_established` unless a backend template is supplied.
  Two "distinct run" screenshots in `EXP-20260816-151` turned out to be
  pixel-identical, and an auditor could not resolve gate pose from the stills
  in `EXP-20260816-149`.
- **Current workaround:** avoid the visual check where a memory read answers
  the same question — [[Session control plane]] reads the carousel counter and
  the internal level global instead of reading the screen, and the renderer
  decision was already log-authoritative. This removes the two screenshot
  checks from the critical path; it does not give visual questions an answer.
- **Desired acceptance:** a committed capture backend for
  `frozen-capture.sh`, plus a bounded comparator that reports pass/fail
  against a named reference region with its own false-positive behaviour
  measured on two control frames.
- **Authority:** ordinary implementation; capture stays limited to the
  isolated 640x480 game surface.

### CAP-016 — Startup context budget

- **Priority:** high; resolved at the briefing boundary, with a residual.
- **Observed limitation:** the [[START HERE]] mandated reading set measured
  **~272,994 estimated tokens** on 2026-08-17, exceeding a 200K context window
  outright. No agent could comply as written, and the fresh-context audit loop
  paid the cost once per round.
- **Current state:** `scripts/briefing.py` produces a 4,615-token briefing
  (1.7%) whose safety rules are non-elidable and whose unparseable sections
  fail loudly; `vault-lint.py --budget-only` makes the budget a measured
  metric; [[Current State]]'s chronology moved verbatim to
  [[Current State Archive]] (241 KB → 131 KB).
- **Residual:** [[Project Roadmap]] (~92K tokens) and [[Decision Log]] (~78K)
  remain far over the 40K per-note budget and are still append-only. The
  mandated total is still ~246K. The same archive split would apply to both.
  Resolved 2026-09-26 (commit `c0e7268`): both chronologies moved to archive
  notes under [[Project history MOC]]. On 2026-10-02 `make budget` reports the
  seven mandated notes at about 34K estimated tokens (session budget 120K), none over the 40K
  per-note budget.
- **Desired acceptance:** the mandated set fits the session budget, or
  [[START HERE]] names the briefing as the required entry point and the full
  notes as reference. Either way `--budget-only` should report clean.
- **Authority:** ordinary Vault maintenance; a change to the mandate itself is
  a decision, not an edit.

### CAP-017 — Receipt-to-note evidence pipeline

- **Priority:** medium-high; resolved at the draft boundary.
- **Observed limitation:** run receipts already carried the hashes,
  environment, timing, and artifact lists that `new-experiment.py` emitted as
  blank fields, so every experiment note re-typed them. That is not a
  theoretical cost: it produced a wrong-rounding coordinate table
  (`EXP-20260816-145`) and a duration typed from memory as "7 seconds" against
  a retained trace showing 2.47 s (`EXP-20260816-157`), each costing a
  reject/correct/re-accept cycle. Separately, the newest runtime packets
  produced **no `RUN-*` directory at all** — their durable record is prose
  plus ignored artifacts.
- **Current state:** `scripts/experiment-draft.py` fills a note from receipts
  and asserts nothing; `scripts/run-index.py` cross-references runs against
  citations and found 14 orphaned runs and 0 dangling citations.
- **Residual:** ad-hoc probes still bypass the `RUN-*` convention. The
  session-control tools emit receipts natively, which should reduce this, but
  it is unproven until a live arm produces one.
- **Desired acceptance:** one runtime packet whose experiment note is
  generated from its receipts and passes an independent audit without a
  transcription defect.
- **Authority:** ordinary implementation.

### CAP-018 — Static export querying

- **Priority:** medium; resolved.
- **Observed limitation:** `ghidra-evidence.json` is 7.7 MB on one line with
  no index, so it was effectively unread; [[Current State Archive]] records at
  least four audit rounds lost to that, plus one counter-correction for
  over-crediting it.
- **Current state:** `scripts/ghidra-query.py` answers a function query in
  0.07 s with a 411 KB greppable sidecar index.
- **Residual, and it matters:** the export itself has structural defects
  recorded in [[Ghidra export structure and caveats]] — `imports` is empty,
  `callers` holds call-site rather than entry addresses, and the call graph
  breaks at 486 thunks, so an accepted module such as `0x00432930` appears to
  have no callers. Regeneration costs about 42 seconds.
- **Desired acceptance:** a re-export whose `imports` is populated and whose
  caller edges name functions, validated against `rabin2-imports.json` and
  against a caller relationship already proved by other evidence.
- **Authority:** ordinary tooling work.

## Resolved or available capabilities

- The fatal-signal/survival subset of CAP-001 is proven by
  [[EXP-20260812-030 - Unexpected-signal-safe GDB control]]: non-allowlisted
  target signals are terminal, fatal records include signal/PC, a required
  failed receipt cannot be accepted, routine Wine signals still pass, and the
  prior safe game watch survives with an independent receipt. Staged phases,
  predicates, and register-relative reads remain active above.
- The bounded submission-capture subset of CAP-001 is proven by
  [[EXP-20260813-038 - Per-entry submission-arena negative]]: schema 3 pairs
  ordered entry boundaries, caps digest reads at one MiB, retains no payload
  bytes, handles a coherent inactive arena without a null read, and preserves
  cleanup/detach/survival gates. General staged points and predicates remain
  active above.
- The purpose-specific Direct3D batch subset of CAP-001 is proven by
  [[EXP-20260813-040 - Direct3D retained-entry batch provenance]]: schema 4
  validates exact pre/flush/post conditions, caller and entry receipts, two
  fixed roots with bounded pages/counts, pre-reset segments, ordered cycles,
  digest-only output, and cleanup/detach/signal/survival gates. General staged
  points, predicates, and register-relative expressions remain active above.
- The GDB harness, memory snapshot/core scanner, frozen game-only capture,
  EGL apitrace arm, and Wine relay/file trace are proven at their documented
  boundaries in [[Runtime Tooling]].
- `gamescopectl screenshot` captures only the isolated game surface in the
  current workflow; M2.15 did not capture the host desktop.
- The bounded log-marker, memory-value, level, file-settle, and
  owned-window waits are available as one tool (`scripts/wait-for.py`),
  replacing three separate in-tool implementations. The file-settle wait
  removes the asynchronous-`gamescopectl` truncation hazard noted in CAP-005;
  the rest of CAP-005 (atomic event correlation) remains open.
- The renderer gate in CAP-004 is now executable rather than procedural:
  `game-session launch` requires all six positive markers and rejects on any
  software marker, and refuses the arm when the gate fails. The retail chooser
  sequence itself is automated but **not live-validated** (CAP-010).
- The startup context budget, receipt-to-note pipeline, and static-export
  query gaps are recorded above as CAP-016, CAP-017, and CAP-018 with their
  residuals stated, rather than being listed here as unqualified wins.
- A capability should move here only after its acceptance test is linked. If
  it becomes a research result or environment fact, update the authoritative
  note as well rather than leaving the resolution only in this register.

## Maintenance

Review this register when an active packet is slowed by tooling, a new tool is
live-validated, an authority requirement changes, or a workaround fails. Use
the template for a complex gap; keep small gaps inline. Closing a gap requires
an evidence link and an update to any affected `KU`, environment note, tooling
note, and roadmap dependency.
