---
type: implementation
status: active
created: 2026-08-12
updated: 2026-10-02
tags:
  - implementation/tooling
  - re/dynamic
---

# Runtime Tooling

Scripted, read-only runtime-evidence tools that automate the manual capture
methods without changing their authority. Decision: `DEC-20260812-019`. Design
patterns are adapted from [[External Source Registry#SRC-DUCKSTATION-DBG]] and
introduce no game semantics.

All tools share: exit codes `0` ok / `1` tool-negative / `2` usage / `3`
structured environment-or-ownership refusal; refusal JSON
`{"refused":true,"tool":...,"reason":...}`; an `ABLPC_ROOT` override so tests
sandbox their run directories; `RUN-<KIND>-<stamp>` provenance under
`dynamic/wine/` with collision refusal; refusal to execute from `originals/`;
and game-byte artifacts only under `git check-ignore`-verified `work/` paths,
with committed metadata carrying hashes but no payload bytes.

The original six tool families were **live-validated against the running game
on 2026-08-12**; see [[#Live validation results (2026-08-12)]]. The seventh,
PC input movies, has a separate bounded live validation from 2026-08-15 in
[[EXP-20260815-119 - PC input movie recorder and hardware replay]]. Later GDB
schemas through 6 also have the bounded live validations below. Harness
1.6.0/schema 6 remains one hard-coded exact-admission mode; it adds only the
fixture- and live-validated fixed three-cycle envelope while preserving
legacy one-cycle capture, not a general repeated-cycle interface. Live runs
are gated on the renderer-selection rule in [[Wine Linux Play Baseline]].

Observed limitations, workarounds, desired acceptance tests, and authority
requirements are centralized in [[Reverse Engineering Capability Gaps]]. That
register does not supersede this tool contract or [[Project Roadmap]].

The session-control tools added on 2026-08-17 — `game-session`, `game-memory`,
`send-keys`, `wait-for` — are documented separately in
[[Session control plane]]. They sit beside these tools rather than replacing
them: the capture families here are live-validated, while the session tools
are fixture-validated only and carry no runtime authority yet (CAP-010). The
exception, added the same day, is `game-memory`'s read/save/restore path,
which [[EXP-20260817-188 - Live game-memory read save restore validation]]
confirmed against the running game; launch, navigation, `send-keys` and
`wait-for` remain unvalidated live. The
one overlap to be aware of is that `game-memory` adds the repository's first
supported memory **write** verbs, gated per [[Decision Log#DEC-20260817-140 - Gate memory writes on authorization, a compare-before-write guard, and a receipt]];
`gdb-harness.py` remains read-only by construction with `write_verbs: []`.

Language selection follows [[Python and C reverse-engineering split]]. Current
Python tools remain appropriate where their measured cadence meets the bounded
contract. A C helper owns only a demonstrated hot loop or required native ABI,
uses a versioned loss-accounted boundary, and must match the Python reference;
it does not gain broader target-write or runtime authority.

## Live validation results (2026-08-12)

Validated against the exact Training hash under Wine 11 on the Fedora 44 host
(`DEC-20260812-020`). Game-byte artifacts (cores, frames, traces) stayed
in `git check-ignore`-verified `work/` paths; only curated metadata was kept.
Three real bugs surfaced that synthetic fixtures could not, each fixed with a
regression test.

- **GDB harness — confirmed.** `RUN-GDB-20260812-182412` attached to the live
  WoW64 game, installed the hardware access watchpoint on plant 10 slot
  `0x005B1AA4`, reached `NextLife` (`stop_reason: target_reached`, 4 stops,
  `cleanup_verified`, detached, game survived). Stop 3 caught the slot taking
  `0x006C342B`, byte-identical to the prior manual `RUN-GDB-20260812-153150`;
  firing PCs land in the `0x00445968` plant path (`EXP-20260812-015`).
  M2.17 `RUN-GDB-20260812-214545` repeats those four exact stops under result
  schema 2 and a required survival receipt: identity re-verification plus five
  post-detach samples all show process state `R` and `TracerPid == 0`, followed
  by a visually live game-only Training frame (`EXP-20260812-030`).
- **memory-snapshot + core-grep — confirmed.** `RUN-CORE-20260812-182803`
  `gcore`d the live game (3.3 GB core, ignored). `core-grep` scanned all 696
  PT_LOAD segments and found `0x006C342B` at exactly one address, `0x005B1AA4`
  — a third independent agreement with the watchpoint and the prior run.
- **frozen-capture — confirmed.** `RUN-FRZ-20260812-183223` froze the single
  game PID (verified `T` state), captured a 640×480 frame, and resumed the
  game. The capture backend is `gamescopectl screenshot <path>` under
  `GAMESCOPE_WAYLAND_DISPLAY`; it is asynchronous (returns before the file
  lands), so the backend command must wait for the file. This is the
  previously-uncommitted method the retained `/tmp/ablpc-*.png` captures used.
  A re-verification capture was visually confirmed to show the actual
  hardware-rendered game menu (the "fliks journey" / training selector), not a
  blank or stale frame.
- **apitrace — confirmed with `--api egl`.** On this Wayland/XWayland host
  WineD3D drives GL through EGL, not GLX, so the default GL wrapper captured
  nothing; `RUN-APITRACE-20260812-184544` with `--api egl` (`egltrace.so`)
  captured a 2.2 GB EGL trace. A re-verification hardware-path trace was
  `apitrace dump`-verified as a valid, parseable capture of the real render
  stream: EGL init, ~6,900 `glDrawElementsBaseVertex` draws, 2,339
  `glTexImage2D`/`glTexSubImage2D` texture uploads, and 2,209 `eglSwapBuffers`.
  It is therefore a usable capture; comparing its texture uploads against a
  control to discriminate `KU-012` remains open (`KU-030`).
- **wine-capture relay/file-trace — confirmed.** `RUN-WINE-20260812-184926`
  on the instrumented prefix set `RelayInclude=kernel32.CreateFileA`, captured
  filtered relay output plus `+file` lines, and the EXIT trap restored the
  registry (value deleted). Metadata carried every additive key
  (`relay_registry_restored: true`, `file_trace: true`).
- **rr — wrapper confirmed; recording blocked by `ntsync` (`KU-028`).**
  `rr-record.sh` passed preflight, forced the documented env, and created
  `RUN-RR-20260812-183423`, but `rr record` FATAL-aborted during Wine init on
  `ioctl(0x80044e88)` issued on `anon_inode:ntsync` fds — Wine 11's in-kernel
  `ntsync` synchronization driver, which `rr` 5.9.0 does not model. An
  `ioctl`-logging shim identified the fd; `rr record` succeeds on a trivial
  non-Wine program. It is not a GPU or disk issue (steering to AMD/Mesa and a
  tmpfs prefix changed nothing; a trivial `wine wineboot` reproduces it), and
  the `WINENTSYNC=0` / `WINE_DISABLE_FAST_SYNC=1` toggles do not disable
  `ntsync` here. Fix: make `/dev/ntsync` absent (`sudo modprobe -r ntsync`
  after closing Wine, or an `unshare` namespace that hides it) so Wine uses
  server-side sync that `rr` can record. See
  [[Runtime Tooling#The ntsync blocker for rr]].

Fixes committed this session: Windows-path cmdline basename in ownership proof;
Wine SIGUSR1 pass-through in the harness; per-API apitrace wrapper name
(`egltrace.so`, not `eglxtrace.so`).

## Shared foundation

- `scripts/evidence_lib.py` — stdlib-only library and CLI helper. Provides
  `ownership_proof` (the single `/proc`-only identity check: Wine loader regex,
  `bugs.exe` in the command line, working directory under `work/copies/`, and
  the on-disk executable SHA-256), run-directory stamping, watch-spec
  validation, and bounds-checked ELF core iteration. It never signals a
  process. Tests: `tests/test_evidence_lib.py`.

## PC input movies

`scripts/input-movie.py` 1.3.0 records keyboard `KeyPress`/`KeyRelease` events
selected on one exact internal Gamescope X11 game window, validates an asset-
free movie, replays keydown/keyup to one fresh verified window through a
persistent X11/XTEST connection, requires a separate exact-window echo, and
compares two or more accepted replay receipts. Log-anchored receipts also
capture bounded post-anchor log/`ROUTINE` checkpoints. See [[PC input movies]]
for the complete contract and command examples.

- **Identity:** every production arm proves the game PID, retail executable
  hash, work-copy CWD, exact window PID/owner/class/geometry, common process
  group, and focus before creating a run. Replay checks the movie's executable
  hash and stable window signature and checks focus before every event.
- **Capture scope:** production uses `XSelectInput` on the one target window.
  It does not use DuckStation, evdev, `/dev/input`, XRecord, a host keylogger,
  or display-wide capture. The fixture-only JSONL backend is marked synthetic
  and replay-refused unless a hidden test switch is explicitly used.
- **Movie schemas 1/2:** immutable create-only JSON with target hash/signature,
  manual-delay or new-log-byte anchor, optional independent frame-file hash,
  monotonic-nanosecond offsets, explicit paired down/up events, duration,
  termination, and canonical schedule hash. Unknown fields, empty/unpaired
  events, impossible bounds, or hash drift fail closed. Schema 2 additionally
  binds a log-anchored recording's bounded log/`ROUTINE` checkpoint; schema 1
  remains readable and unchanged.
- **Safety/receipt:** focus loss, target-echo mismatch, unrelated target input,
  or interruption aborts and releases held keys. Nested-display auto-repeat is
  restored on every replay exit.
  `RUN-INP-REC-*`/`RUN-INP-REP-*` metadata carries the exact implementation,
  ownership/window snapshots, movie/schedule hashes, dispatch timing, cleanup,
  and acceptance. `make input-movie-caps` reports that internal game-frame
  synchronization is unsupported. An optional inherited-FD NDJSON channel
  emits `armed`, `recording-started`, and `replay-started` transitions to a
  supervisor without mixing them into the final receipt on stdout.
- **Validation:** 11 focused synthetic regressions pass. Production
  `RUN-INP-REC-20260815-125142` captured Down/Return at the hardware selector;
  fresh replays `RUN-INP-REP-20260815-125230` and
  `RUN-INP-REP-20260815-125312` dispatched 4/4 events, released all keys,
  remained below 1.8 ms maximum absolute drift, agreed under `compare`, and
  independently passed the complete Direct3D/no-software log gates. This is
  an opening-selector validation, not a long gameplay or internal-frame claim.

`scripts/play-pristine-with-inputs.py` 1.3.0 is an optional desktop companion
for that same worker. It launches the unchanged hash-pinned
`scripts/play-pristine.sh` in one isolated session, discovers only that
session's exact owned 640x480 `bugs.exe` surface, and exposes Recording,
Replay, and Session controls in a small Tk window. The default gameplay
recording watches the first newly appended `NextLife.` after initialization;
Level Select is retained as a labeled menu-only choice and manual delay as a
weaker fallback. Backend status
drives visible `ARMED`, `RECORDING NOW`, and `REPLAYING NOW` transitions, and
the last saved path remains distinct from the next create-only output.

`EXP-20260815-120` is the original offline validation packet and live
`EXP-20260815-121` diagnoses the manual-delay divergence. Corrective
`EXP-20260815-122` passes 23 focused fixtures, including same-marker
record/replay, post-marker neutral-wait preservation, and cleanup after the
launcher leader has exited. It introduces no second capture backend or broader
input scope. `EXP-20260815-123` live-accepts that marker only for Hardware and
Training entry: 300/300 events dispatch and Training loads, but later gameplay
visibly desynchronizes. `EXP-20260815-124` timestamps `NextLife` before the
first gameplay key but simultaneously echoes a transformed target stream: 304
normalized events for the 300-event source plus 15-39 ms timing/hold changes.
The accepted receipt timestamps before send and cannot prove target delivery.
`EXP-20260815-125` corrects that backend and accepts two 300/300 target echoes
below 0.52 ms delivery drift, but one fresh arm returns to Level Select while
the other remains in Training. Exact keyboard delivery is accepted; complete
gameplay determinism is not. The next arm is a new user `NextLife` recording
with two matching exact-input and runtime-checkpoint receipts; CAP-002 remains
partial.

## PC coordinate overlay

`scripts/coordinate-overlay.py` 1.2.0 is a separate read-only display worker.
(The current file is 1.3.0: it also accepts the EXP-20260815-136 grain-gates
profile hash and adds an opt-in `--gates` readout, audited in
[[EXP-20260815-140 - Independent static gate geometry and overlay audit]].)
It verifies the known retail executable, exact work-copy CWD, launcher-owned
process group, and PID start time, then uses `process_vm_readv` to display
confirmed current Flik X/Y/Z from `0x0059D910`; bounded raw
level/flags/`NextLife`/state/collision fields are opt-in with `--details`.
It does not attach, pause, set breakpoints, or write target state.

`scripts/play-pristine-with-inputs.py` 1.5.0 can open it from the View menu or
button, and `--coordinates` starts it automatically after exact target
discovery. Default mode is a compact draggable translucent Tk panel on the
owned Gamescope display; the external-overlay atom and opacity are applied to
the mapped Tk top-level. Double-click supplies the ordinary decorated-window
fallback. Click-through and internal-frame synchronization are not claimed.
EXP-127 remains the read-only/lifecycle smoke; EXP-128 corrects its untested
coordinate source after a controlled Training jump. See [[PC coordinate overlay]]
and [[EXP-20260815-128 - Live Flik position globals]].

## GDB watch harness

`scripts/gdb-harness.py` — a dual-mode file. In CLI mode it validates a watch
spec, proves target identity before any ptrace, and launches gdb with itself as
the `-x` controller script; in controller mode (inside gdb) it installs up to
four hardware watch/breakpoints, runs a bounded window, writes one JSONL record
per stop, and deletes every breakpoint and detaches on every exit path.

- **Read-only by construction.** No memory/register/code/execution write verbs
  exist; `--capabilities` reports `write_verbs: []`. Every gdb command passes a
  frozen allowlist (`attach`/`continue`/`detach`/`info`/`handle` and only the
  startup `set can-use-hw-watchpoints 1`). Installing and deleting its own
  hardware watch/breakpoints at a natural pause is exactly the
  `DEC-20260812-006` surface.
- **Watch spec (schemas 1 through 6):** target block (mode
  `pid`/`name`/`spawn`, expected
  exe SHA-256, loader regex, cwd prefix); `watchpoints` `{id, address,
  kind:read|write|access, size:1|2|4}`; `breakpoints` `{id, address}` (1..4
  total); `window` `{max_stops, timeout_seconds, end_milestones, log_path}`
  (milestones matched only in `bugs.log` bytes appended after window start);
  `on_stop` `{registers, memory_reads ≤16×≤256B, backtrace_limit ≤32}`. Strict
  schema 1 remains accepted. Schema 2 optionally adds `survival` with required
  acceptance, settle/sample timing, and resumed/untraced requirements; its
  total sampling window is capped at 30 seconds. Schema 3 optionally adds a
  bounded `submission_capture`: ordered entry lattice, candidate indices,
  counter/capacity/base globals, output stride/record cap, rollover/cycle
  bounds, and either paired pre/post SHA-256 metadata or fail-closed
  `zero_post`. Optional exact stop-PC filters let data watches ignore unrelated
  accesses while retaining them in `stops.jsonl`. At most 1 MiB may be hashed
  per interval. Schema 4 optionally adds purpose-specific
  `direct3d_batch_capture`: exact pre/flush/post triggers, caller return and
  entry-lattice receipts, allowlisted roots and bounded pages, vertex/index
  counts and capacities, pre-reset segment capture, ordered candidate cycles,
  and a 16 MiB per-entry digest bound. It requires three data watchpoints and
  forbids general on-stop memory reads. Payload bytes are never placed in
  either capture result. The M2.27 spec uses two roots and 32 pages. Schema 5
  adds purpose-specific `record_outcome` capture: an exact ordered
  entry/offset/form plan, candidate subset, allowlisted family/page, and
  form-specific count deltas. It snapshots only batch roots, pointers, and
  counts; it neither reads nor hashes source, vertex, or index payloads.
  Schema 6 adds only `exact_0a6c_admission`: a hash-locked entry 7/offset
  `0x0A6C` evaluator at the same pre/post boundaries. It transiently reads
  the exact source words and active non-source lattice, retains only first
  reject/evaluated count/state digest/predicted-observed booleans, re-digests
  at post, and redacts all raw stop values. It is not a general predicate
  engine. Harness 1.6.0 keeps schema 6 and permits exact mode to use only its
  live-validated legacy one captured cycle or the M2.33 fixed three captured
  cycles after one warmup; arbitrary exact cycle counts remain forbidden.
- **Evidence:** `stops.jsonl` (per stop: monotonic+wall time, kind, trigger id,
  PC, registers, watched value, bounded memory reads, backtrace PCs);
  `metadata.json` is a strict superset of the hand-written
  `RUN-GDB-20260812-161520` shape plus result schema 4 `completion`
  `{completed, accepted, stop_reason, target_signal, stops_observed,
  watchpoints_installed/deleted, cleanup_verified, detached,
  survival_receipt}`; and an auto-drafted `debugger-evidence.txt`. Stop reasons
  add `capture_complete`, `target_signal`, and `survival_failed`. Read
  watchpoints are read-class
  hardware traps on x86 — recorded as access evidence, not proof of a read.
- **Signal and survival policy:** `SIGUSR1/SIGUSR2` are explicit Wine routine
  pass-through signals. Fatal `SIGSEGV/SIGILL/SIGBUS/SIGFPE/SIGABRT/SIGSYS`
  use `stop print nopass`; every observed non-allowlisted target signal is a
  structured terminal result with signal and PC, inspected before a concurrent
  log milestone. After cleanup/detach, schemas 2/3/4/5/6 can re-prove process
  identity and sample `/proc/<pid>/status`; required failure forces rejection.
  Schema 6 exact mode requires the accepted five-sample configuration.
- Tests: `tests/test_gdb_harness.py` drives real gdb against a compiled C
  sentinel fixture (max-stops, timeout, milestone, cleanup, detach-resume,
  routine/fatal signals, required-survival rejection, ownership refusal,
  allowlist), paired digest-only/coherent-zero submission captures, and a
  synthetic Direct3D append/flush/reset/append batch-segment regression, plus
  schema-5 per-record append and flushed-no-append outcomes, plus schema-6
  exact arithmetic/rejection, plan-envelope, digest/count mismatch, closure,
  and raw-output exclusion fixtures. M2.33 adds stable reject, stable pass,
  reject/pass/reject, unclosed/partial-final-cycle, fixed-bound, and multi-
  cycle output-exclusion fixtures.

M2.25 live-validates harness 1.2.0/schema 3 (`EXP-20260813-038`). Three fresh
Direct3D arms each use one data watch at `0x005B18E0`, filter exact post-call
PC `0x0044C8AB`, complete one ordered 23-candidate result, delete the point,
detach, and pass five survival samples. All rows are coherent zero-post
intervals, so no arena payload is read. A rejected preflight at execution
breakpoint `0x0044C898` receives same-PC `SIGSEGV`; the terminal-signal policy
safely rejects it and the accepted arms do not reuse that execution point.

M2.27 live-validates harness 1.3.0/watch-result schema 4
(`EXP-20260813-040`). Three fresh accepted hardware Direct3D arms each use
conditioned data watches on exact pre selector `0x0059F7F0`, pre-reset marker
`0x004C4118`, and post header `0x005B18E0`. Every arm completes one ordered
23-candidate cycle, deletes all three points, detaches, receives no target
signal, and passes five survival samples. Exact caller/root/page/count/order/
address bounds fail closed; only metadata/SHA-256 is retained. All selected
additions use root `0x004C4108`, page 16, and no selected call flushes.

M2.29 live-validates harness 1.4.0/watch-result schema 5
(`EXP-20260813-042`). Three fresh accepted hardware Direct3D arms reuse only
the exact pre-selector, pre-reset, and post-header data watches. Each audits
the complete ordered 168-call plan and retains count outcomes only for 124
candidates; no payload is read or hashed. Exact pointer/form/order,
root/page, delta, cleanup/detach, signal, and five-sample survival checks fail
closed. Every positive candidate outcome uses root `0x004C4108`, page 16,
and no selected call flushes.

M2.32's offline gate fixture-validates harness 1.5.0/watch-result schema 6
(`EXP-20260813-045`). The new mode accepts only a paused PID with the exact
executable/work-copy identity, existing three data watches, M2.29 forms/
families/root/page/survival gates, target entry 7/offset `0x0A6C`, and complete
168-call plan at canonical SHA-256
`5eb280a7bd54b56a9654fed7984e9677a15618c5376be703a85718ea3bb2ffec`.
Every native reject path and fail-closed schema gate passes synthetic tests;
stop records and receipt rows exclude raw values. At that offline gate the
mode had not run against the game and matched live capture remained separately
authorized.

Freshly authorized `EXP-20260813-046` then live-validates the same locked
schema-6 mode without changing the tool. Three post-`NextLife` hardware
Direct3D arms each complete one captured 168-call cycle at 400 stops, install
and delete only the existing three data watches, detach cleanly, observe no
target signal, and pass five resumed/untraced samples. Exact prediction agrees
with observed count in all arms, while the fresh append pattern varies as
`0/0/1`. Raw input retention remains false and payload retention remains zero.
Two title-boundary calibrations fail closed at `max_stops`, establishing that
this exact mode must attach after the logged gameplay boundary. This validates
the one-cycle purpose-specific path only.

M2.33's offline gate fixture-validates harness 1.6.0/schema 6
(`EXP-20260813-047`). Exact mode now accepts either that legacy one-cycle
envelope or exactly three captured cycles after one warmup. Three is the
smallest count capable of expressing an `A/B/A` recurrence. Each accepted
M2.32 exact arm consumed exactly 400 stops for two complete cycles, so four
total cycles project to 800 stops and retain 200 stops beneath the unchanged
1,000-stop ceiling; four captured cycles would leave no margin. The existing
controller emits only completely closed plan/candidate cycles, excludes a
partial final cycle, and retains the same payload-free receipt. No live three-
cycle capture had run at that gate.

Freshly authorized `EXP-20260813-048` then live-validates the fixed bound in
one unchanged post-`NextLife` hardware Direct3D process. It completes at 816
stops with four rollovers and ordered reject/pass/reject (`0/1/0`). Every
prediction matches the independent native count outcome; both rejects occur
at `0x004065B0` after seven slots, but all three active-state digests differ.
The arm installs/deletes only the existing three data watches, uses no
breakpoint, detaches cleanly, observes no target signal, and passes five
resumed/untraced samples. All stop rows redact watched/register/memory values,
receipts retain zero payload, and the raw GDB console stream is not curated.
The 816-stop result remains within the 1,000-stop ceiling but corrects the
offline 800-stop projection by 16 additional flush-watch stops.

### Current schema limits and resolved M2.16 status contradiction

All accepted spec schemas install one fixed set of no more than four hardware
points. They do not stage a second arm after a guard, evaluate stop predicates,
or read bounded register-relative expressions. Those remaining limits are
CAP-001/CAP-006 in [[Reverse Engineering Capability Gaps]]. Schema 3 resolves
the bounded submission-digest subset; schema 4 resolves one exact Direct3D
pre/flush/post state machine with fixed caller/root/page expressions; schema
5 specializes that state machine to an exact record plan and count-only
outcomes. Schema 6 adds one hard-coded exact-record evaluator and one fixed
three-cycle bound, not general predicates, arbitrary repeated capture, or
register-relative expressions. None provides general staging or general
predicate evaluation. Schemas 2/3/4/5/6 add the independent live-process receipt; result schema 2 fixed
the fatal-signal status gap described below.

In exploratory M2.15 `RUN-GDB-20260812-204252`, the harness recorded one
hardware-breakpoint stop at `0x0044D79A` and later reported deletion, cleanup,
and detach. Raw GDB output from that same run records thread 1 receiving
`SIGSEGV` at the breakpoint PC before the timeout; the structured completion
does not surface it. A following arm reported the same cleanup, and Wine later
reported the matching unhandled read fault while starting its debugger. The
instruction is `test al,0x10` and has no memory operand. Both affected arms are
quarantined from the accepted experiment result (`EXP-20260812-028`,
`KU-031`). Until a fresh simultaneous arm discriminates this, a harness
cleanup receipt is not by itself a fault-free game-survival receipt for that
address.

M2.16 `RUN-GDB-20260812-211649` performs the required fresh-process
discriminator with gate `0x0044D79A`, callee `0x0044CA00`, and both exact
plant 10 data watches armed simultaneously. It reproduces the contradiction:
one gate stop is followed by raw `SIGSEGV` at the same PC, but the harness
continues the signal and the appended `NextLife` milestone wins as
`target_reached`. Wine opens winedbg, and the isolated survival frame shows a
fatal-error dialog. Cleanup/detach describes harness-owned breakpoint state;
it does not prove target survival. This closes M2.16 as tooling-fault evidence
only (`EXP-20260812-029`, `KU-031`) and made CAP-001's fatal/survival subset
blocking for M2.17.

M2.17 implements and validates that repair (`DEC-20260812-025`,
`EXP-20260812-030`). A trigger-file-controlled synthetic `SIGSEGV` ends as
tool-negative `target_signal`, records fatal classification/non-null PC and
`stop-print-nopass`, deletes its point, detaches, and leaves the fixture
resumed/untraced across three samples. A real exited-process receipt fails
closed, while the existing routine `SIGUSR1` case remains green. Safe live
`RUN-GDB-20260812-214545` then reproduces prior plant-slot PCs/values with no
target signal and five passing post-detach samples. This resolves trust in the
structured result at tested boundaries; it does not explain or bless the
original continuation fault at exact `0x0044D79A` (`KU-031`).

M2.18 `RUN-GDB-20260812-221224` applies that controller to a fresh arm with
only adjacent execution breakpoint `0x0044D794` (`EXP-20260812-031`). One
breakpoint stop is followed by structured same-PC `SIGSEGV`; the result is
correctly tool-negative, deletes the point, detaches, and records five state-
`R`, `TracerPid == 0` samples. A later isolated game frame shows live Training
because the pending signal is not passed. This survival does not validate
continuation. Together with independent exact-`0x0044D79A` reproductions, the
result makes hardware execution breakpoints in this nearby caller-gate region
an unsafe evidence path under the tested Wine/native-GDB setup. M2 leaves the
region rather than treating new staged/predicate features as the answer.

### Reference live invocation

On an unchanged ignored Training copy, reach the natural title pause (hardware
renderer per [[Wine Linux Play Baseline]]), find the game PID, and run a
schema-2 spec watching plant 10 slot `0x005B1AA4` with
`end_milestones: ["NextLife"]` and a required survival block. Confirm
`completion.accepted`, `target_signal`, cleanup/detach, and every receipt
sample; reconcile stops against `RUN-GDB-20260812-153150` and
`RUN-GDB-20260812-214545`.

## rr record wrapper

`scripts/rr-record.sh` — records a Wine run under `rr` for deterministic replay
(unlimited replay watchpoints, reverse execution). Refuses unless
`kernel.perf_event_paranoid <= 1` (remedy: `sudo sysctl
kernel.perf_event_paranoid=1`) and refuses when `/dev/ntsync` is present (see
below). Forces and records with rationale `LIBGL_ALWAYS_SOFTWARE=1` (rr cannot
record GPU-written shared memory), `WINEESYNC=0`, and `WINEFSYNC=0`
(cross-process sync diverges under rr). Trace goes to git-ignored `work/rr/`.
This is a distinct llvmpipe environment arm — valid for memory-reader
questions, not pixel-fidelity questions. Tests: `tests/test_rr_record.py`
(stub recorder; perf, ntsync, and metadata paths).

### The ntsync blocker for rr

Wine 11 uses the in-kernel `ntsync` synchronization driver (`/dev/ntsync`).
Under `rr`, Wine issues `ioctl(0x80044e88)` on `anon_inode:ntsync` fds that
`rr` 5.9.0 does not model, so `rr record` FATAL-aborts during Wine init — even
for a trivial `wine wineboot`. This was misattributed to the NVIDIA GPU at
first; an `ioctl`-logging `LD_PRELOAD` shim proved the fd is `anon_inode:ntsync`,
not a GPU or NVMe device. Ruled out by test: GL/Vulkan steering to AMD/Mesa, a
tmpfs prefix, and the `WINENTSYNC=0` / `WINE_DISABLE_FAST_SYNC=1` env toggles
(4,172 ntsync ioctls persisted). No newer `rr` is packaged for Fedora 44.

`ntsync` is a loadable module (`ntsync.ko`), so the fix is to make
`/dev/ntsync` absent, after which Wine falls back to server-side synchronization
that `rr` records:

- **Per session (root, surgical):** close all Wine, `sudo modprobe -r ntsync`,
  run `rr`, then `sudo modprobe ntsync` to restore. `modprobe -r` fails while
  any Wine holds the module.
- **One time (root):** `blacklist ntsync` in `/etc/modprobe.d/` — automatic
  thereafter, but Wine loses fast-sync system-wide.
- **No root (unfinished):** an `unshare --map-root-user --mount` namespace that
  hides `/dev/ntsync` so `rr-record.sh` needs no privilege. Masking the device
  removed the FATAL, but a `/dev/null` bind lets `open()` succeed and Wine then
  breaks — a clean fallback needs the node genuinely absent (a curated `/dev`),
  which is not yet built.

### Staged live validation (KU-028)

With `/dev/ntsync` removed and `perf_event_paranoid <= 1`, record a Training
launch, then `rr ps` → `rr replay -a` → `rr pack`; confirm replay reaches the
recorded exit and a replay watchpoint on `0x005B1AA4` reproduces the known
plant 10 reads.

## wine-capture relay and file-trace extensions

`scripts/wine-capture.sh` gains additive `--relay-include LIST`,
`--relay-exclude LIST`, and `--file-trace`. Relay filters write
`HKCU\Software\Wine\Debug` `RelayInclude`/`RelayExclude`, which mutate the
prefix, so they are refused on the `baseline` prefix (require `--prefix
instrumented`) and require `+relay` in the channels; prior values are queried
and restored on exit. Metadata gains additive keys only (`relay_include`,
`relay_exclude`, `relay_prior_*`, `relay_registry_restored`, `file_trace`); a
plain run is byte-identical to before. Tests: `tests/test_wine_capture.py`
(stub wine; refusals, set/restore sequence, backward compatibility).

## Frozen-frame capture

`scripts/frozen-capture.sh` — freezes the single game PID with `SIGSTOP` (all
its threads; gamescope and wineserver keep running to serve the held frame),
optionally after a `bugs.log` milestone, captures one frame via a pluggable
command template (`--capture-cmd`/`CAPTURE_CMD`, `{out}` placeholder), then
`SIGCONT` via an EXIT trap. The capture backend is an explicit input because
the historical PipeWire invocation was never committed; documented candidates
are `gamescopectl take_screenshot`, gamescope `Super+S`, and a `gst-launch-1.0
pipewiresrc num-buffers=1` grab. Frame → ignored evidence dir; metadata records
ownership, milestone offsets, freeze/capture/resume timestamps, the verbatim
capture command, and the frame hash. Tests: `tests/test_frozen_capture.py`
(freeze/capture/resume with a `T`-state assertion, trap-resume on failure,
refusal paths send no signals).

### Staged live validation (KU-029)

Freeze at `NextLife`, capture a control frame, resume; compare a freeze/resume
control against an unfrozen control for post-resume divergence beyond the
`EXP-20260812-020` control-to-control variance.

## Memory snapshot and core scanner

`scripts/memory-snapshot.sh` — `gcore` at a natural pause with ownership proof;
core to the ignored evidence dir, `/proc/PID/maps` (ranges/paths only) and
hashes to `RUN-CORE-<stamp>/`. `scripts/core-grep.py` — read-only ELF core
scan for a `--hex` pattern or `--dword` value over PT_LOAD segments, reporting
match virtual addresses and clamping truncated segments. Together they locate
where DAT/asset bytes land in memory without spending hardware watchpoints.
Tests: `tests/test_memory_snapshot.py` (stub gcore, ignore-gate, ownership
refusal) and `tests/test_core_grep.py` (synthetic ELF cores: vaddr math,
endianness, chunk-boundary matches, truncation, reject cases).

## apitrace GL arm

`scripts/apitrace-capture.sh` — traces the host GL stream with the per-API
wrapper selected by `--api`: `glxtrace.so` for GL/GLX or `egltrace.so` for EGL.
This host requires `--api egl`. Under WoW64 wined3d runs the game's ddraw as
host GL, so this captures the wined3d
translation output behind `KU-012`; it is complementary to `wine-capture.sh
--relay-include ddraw.*`, which records the Windows-side ddraw API. Refuses if
the wrapper is absent; traces go to git-ignored `work/apitrace/` and every
produced trace (`bugs.trace`, `bugs.1.trace`, …) is hashed. Tests:
`tests/test_apitrace_capture.py` (stub tracer; multi-trace hashing,
wrapper-missing refusal).

### Next discrimination (KU-030)

Capture the GL stream of a control and a modified arm; inspect the `glTexImage2D`/
`glTexSubImage2D` formats and sizes for the brown/green stem region against the
matched control.

## Environment prerequisites

`rr` and `apitrace` are installed; `scripts/doctor.sh` reports `GDB`, `rr`,
`apitrace`, `perf_event_paranoid`, and `ptrace_scope`. The current runtime
`perf_event_paranoid` value is 1; `rr` recording is blocked by `/dev/ntsync`
until the separately authorized remedy in [[#The ntsync blocker for rr]] is
applied.
`Makefile` targets `harness-caps` and `rr-help` surface the new tools.
