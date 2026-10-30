---
type: implementation
status: partially-live-validated
created: 2026-08-17
updated: 2026-10-02
platform: Windows PC under Wine
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence:
  - EXP-20260817-188
  - EXP-20260816-144
  - EXP-20260816-148
  - EXP-20260816-156
  - EXP-20260815-128
  - EXP-20260815-130
tags:
  - implementation/tooling
  - re/runtime
  - workflow/play
---

# Session control plane

Four command-line tools and one shared module that turn the live-session
recipe in [[PC autonomous game control]] from prose an agent must re-read and
re-implement into commands with receipts.

**Status boundary, stated first.** Most of this note is validated against
synthetic fixtures only. The **exception** is `game-memory`'s read, save, and
restore path, which [[EXP-20260817-188 - Live game-memory read save restore validation]]
confirmed against the running retail game: identity/`state` reads, the
single-contiguous-`.data` mapping assumption, a full `.data` `snapshot`, and a
`snapshot`→`poke`→`restore`→verify cycle that reverted a real global exactly.
**Everything else here — `game-session` launch/gate/navigation, `send-keys`,
`wait-for` — has not run against the real game, Wine, or Gamescope**, and its
live behaviour is Unknown until a separately authorized runtime arm proves it.
Do not cite the unvalidated parts as runtime evidence, and do not treat a
passing fixture as a hardware gate.

## Why it exists

The live-experiment lifecycle recorded across the 2026-08-15/16 runtime
packets is roughly twenty sequential steps per arm, most of them
re-establishing what is already known: identity proof, renderer selection,
menu navigation, and cleanup. Three specific findings had been learned and
then re-learned because they lived only in prose:

- Synthetic `XSendEvent` input is ignored — the chooser and menus poll
  `GetAsyncKeyState` at `0x004A7600`, which under Wine reflects real keyboard
  state ([[PC autonomous game control]]).
- A tapped key lasts about 12 ms and falls between polls. EXP-20260816-156
  lost two of three carousel presses that way and selected the wrong level.
- The game advances its logic loop only while its window holds focus
  ([[EXP-20260816-148 - Modified grain-gate thresholds for remaining gates]]),
  so a wait for a logic-dependent result must hold focus or it times out for
  the wrong reason.

Each is now enforced by code rather than remembered.

## Components

### `scripts/session_lib.py`

Shared foundation: `/proc` process records, nested-display resolution bound to
the owned process group, the `XDo` XTEST wrapper, exact game-window discovery,
the renderer log gate, `process_vm_readv`/`writev` access, the level roster,
and the session manifest.

Two invariants are encoded here deliberately:

- A session identity is `(pid, process group, PID start ticks)`. Start ticks
  make a **recycled PID detectable**, which is what turns "terminate only the
  identities recorded at launch" from an instruction into an enforceable
  check.
- Renderer acceptance comes from the game log only. `evaluate_renderer_log`
  requires all six positive markers from [[START HERE]] and rejects on any
  software marker. No screenshot, key receipt, or early selection summary can
  substitute.

### `scripts/game-session.py`

`preflight | launch | status | level | close | audit | list`.

`launch` performs the whole recipe: preflight audit, detached launch in its
own process group, owned-display and owned-window discovery, chooser
sequence (or the auto-hardware path), the six-marker gate, ownership
recording, and optional level navigation. A failed gate **rejects the arm**
and closes it unless `--keep-on-reject` is passed.

Every session writes `dynamic/wine/RUN-SESSION-<stamp>/session.json` — the
ownership ledger [[Agent Operating Manual#Runtime instance lifecycle]]
requires and that nothing previously produced. It records the process group,
game PID with start ticks, display, window, private sink, and **the inventory
of runtime processes that already existed before the launch**, so a later
audit can separate this session's residue from someone else's. That inventory
is the direct answer to the EXP-20260816-163 closure audit, which found 32
`winedevice.exe` processes it could neither attribute nor terminate.

`close` signals only recorded identities, re-checking start ticks per PID; a
PID whose ticks have changed is recorded as `skipped_recycled` and left alone.

### `scripts/game-memory.py`

`peek | state | watch | snapshot` are evidence gathering; `snapshot` also
briefly `SIGSTOP`s the game for an atomic capture. `poke | teleport | restore`
are writes, and are gated accordingly:

- `--authorize` is mandatory and is recorded in the receipt.
- `--expect-current` compare-before-write is mandatory; `--no-expect` exists
  only as a disclosed, receipt-recorded escape.
- The write is read back and verified.
- A receipt lands under `dynamic/wine/RUN-POKE-<stamp>/`, including refusals.
- `teleport` additionally requires `--destination-evidence` citing why the
  destination is already proven walkable, writes current and preceding only,
  never auxiliary, and reports a nonzero `NextLife` after settling as
  tool-negative — the observable signature of the EXP-20260815-130 reset loop.

This retires roughly ten per-experiment throwaway helpers under
`work/copies/EXP-*/` that each re-derived identity proof and syscall framing.

**A correction this work produced.** The current and preceding triples are
**not contiguous**: current occupies `0x0059D910/14/18` and preceding starts
at `0x0059D920`, leaving an unidentified dword at `0x0059D91C` between them.
"One 24-byte `process_vm_writev`" is therefore one *call carrying two 12-byte
vectors*, not a 24-byte contiguous range. A contiguous write would overwrite
that unknown dword and misalign the second triple. The tool writes two vectors
and reports `unknown_dword_preserved`. See [[PC Flik teleport procedure]].

#### Region state checkpoints (`snapshot` / `restore`)

`game-memory.py snapshot` captures curated game-data regions from a running
process; `restore` writes them back. This is the "save and reload" capability,
but it is a **memory-only state checkpoint, not a true savestate**, and the
name matters: it carries no renderer/GPU state, sound buffers, file positions,
thread execution points, or anything the kernel and Wine own.

The design follows from the PE layout. Every global the project has identified
— Flik position `0x0059D910`, internal level `0x00861C84`, `NextLife`
`0x0059A5B0`, the collision table `0x007F45A0`, the type-1 pointer
`0x005C5864` — lives inside the single writable `.data` section
(`0x004C1000`–`0x00864000`), which is neither code nor stack. Capturing
`.data` captures all of them in one contiguous region that can be written back
without corrupting the instruction stream or a thread's return addresses.

Safety boundaries, all enforced in code:

- **Same-process only by default.** Restore refuses a target that is not the
  exact process the snapshot was captured from (PID plus start ticks), because
  a fresh launch has a different heap base and the captured `.data` pointers
  would dangle. `--allow-different-process` is a disclosed override.
- **No level change by default.** Restoring `.data` across a level change is
  refused; `--allow-level-change` overrides it.
- **Executable hash must match** the snapshot.
- **Atomic capture and write.** The game process is `SIGSTOP`ed for the read
  and the write (the `frozen-capture.sh` technique), so a multi-megabyte
  region cannot tear against a running game thread. `--no-freeze` opts out.
- **Region mappings are validated** against `/proc/<pid>/maps` before every
  read and write: a region that straddles a gap, a read-only section, or a
  device mapping is refused rather than checkpointed. Stacks are deliberately
  not a supported region.
- **Restore is a write**: it needs `--authorize`, reads every region back to
  verify, and writes a receipt under `dynamic/wine/RUN-RESTORE-<stamp>/`.
  Snapshots hold game bytes and go to git-ignored `work/snapshots/`, refused
  if that path is not ignored.

**What this buys.** Within one long-lived session: launch once, navigate to a
level once, `snapshot` at the interesting point, then run any number of
experiment arms that each `restore` that point — with no relaunch between
arms. It amortizes one boot-plus-carousel over many experiments, which is the
cost CAP-011 exists to remove. **What it does not buy:** surviving a crash, a
deliberate close, or a relaunch. That is the durable-savestate path (CRIU),
which is separate and, on this host, blocked.

#### In-game save-state hotkeys

`scripts/savestate-hotkeys.py` is the ergonomic front end asked for over the
raw CLI: press a key while playing to save or load, with a filename popup on
save and a picker on load. It is emulator-style, but the game is Wine, not an
emulator, so the hotkeys are grabbed with `XGrabKey` **on the game's nested X
display only** (`:N`), never the host desktop `:0` — a save key pressed in the
game window fires the save; the same key on your desktop is untouched.

Defaults (all configurable, e.g. `--save-key F1`): F5 save (filename popup),
F9 load (picker), F6 quicksave, F7 quickload, F12 quit. It is a thin front end
over the live-validated `snapshot`/`restore` verbs — same `.data` capture, same
same-process and level guards, same receipts. A load is a memory write; here
the human keypress is the authorization, and every load still writes a receipt
recording it was hotkey-initiated. Saves land in git-ignored `work/snapshots/`.

Validation: the `game-memory` backend is live-validated (EXP-188), and the
`XGrabKey`/event-loop layer was confirmed live to grab keys on the running
game's nested display `:2` without conflict. The remaining unproven piece is
the full interactive flow — a real keypress raising the popup and completing a
save/load — which needs a human at the keyboard (its acceptance test). The Tk
popups follow the same nested-display pattern the coordinate overlay already
uses.

#### Why CRIU is not the checkpoint here

`scripts/criu-feasibility.py check` is a read-only survey — it never dumps,
freezes, or signals. Run against the live game it reports the durable path is
**blocked**: the process holds an open `/dev/ntsync` fd and `ntsync`
anonymous inodes (the same driver that already defeats `rr`, KU-028), a GPU
DRM fd, and open X11/Wayland/PulseAudio sockets — 35 hard-to-checkpoint fds in
total — and a dump additionally needs `CAP_CHECKPOINT_RESTORE` or root. The
in-process region checkpoint sidesteps all of that by moving memory only. See
CAP-011.

### `scripts/send-keys.py`

`send | levels`. XTEST only, focus re-established and verified before every
press, default 180 ms hold, press cap, and an exact game-window class/size
check. `--verify-level` re-reads `0x00861C84` afterwards, because dispatching
input is not the same as reaching a level.

### `scripts/wait-for.py`

`log | memory | level | file | window`. One implementation of the log-marker
wait that previously existed three times (`input-movie.py`, `gdb-harness.py`,
`frozen-capture.sh`), plus the waits that had none. `file` waits for existence
and size stability, which the asynchronous `gamescopectl screenshot` backend
requires. `--hold-focus` re-activates the game window between polls.

## Level navigation is verified, not assumed

Carousel position is not the internal level number
([[PC level roster and numbering]]). Navigation therefore reads two globals:

- `0x00599AF8`, the carousel position counter, after **each** press, so a
  press that fell between polls is detected immediately and retried rather
  than silently selecting the wrong level.
- `0x00861C84`, the internal level index, after confirming, as the acceptance
  check.

**Confirmed:** `0x00861C84` is the internal level global (EXP-20260812-013,
EXP-20260815-136, EXP-20260816-144). The progression→internal table is
statically derived at `0x004C6A30`.
**Inferred:** that `0x00599AF8` is readable at runtime as a 16-bit carousel
position with the semantics the static derivation implies. It is
static-derived only; its live width and update timing are unvalidated. The
tool always reports the raw observed values so a live arm can confirm or
refute this. Recorded as `KU-074`.

## What is validated, and how

`tests/game_fixture.py` builds a process tree structurally identical to a real
launch — a launcher owning its process group, a nested `Xwayland` on its own
display, and a `bugs.exe`-named process under `work/copies/` — with no Wine,
Gamescope, or game asset. The fake game maps anonymous memory over the real
global address window (`0x00599000`–`0x00862FFF`), so the tools exercise real
`process_vm_readv`/`writev` at the real addresses. It consumes the stub
`xdotool`'s key log, so a carousel press advances the counter, `Return`
confirms the chooser, and dropped presses can be injected. It also mirrors one
address to another every loop, giving write tests an independent confirmation
that a write landed in the target's own view rather than only in the writer's
readback.

162 focused regressions pass (`tests/test_session_lib.py` 66,
`tests/test_game_memory.py` 36, `tests/test_game_session.py` 21,
`tests/test_wait_for.py` 19, `tests/test_send_keys.py` 15,
`tests/test_criu_feasibility.py` 5) inside a 1,109-test canonical suite.
(Corrected 2026-10-02: these per-file counts, re-collected unchanged, sum to
162, not the 152 first written. `tests/test_savestate_hotkeys.py` adds 10 in
`17258b8`.) The
checkpoint round-trip is verified end to end: the fixture's game loop mirrors
one address to another every frame, so a restored value that the running game
re-propagates proves the write landed in the game's own memory, not only in
the tool's readback.

The stub deliberately refuses to record a `key --window` press as delivered,
so a tool that regressed to synthetic delivery would fail rather than pass
quietly.

## What is not claimed

- No live validation beyond `game-memory`'s read/snapshot/poke/restore cycle
  (EXP-20260817-188) and the hotkey grab on the nested display. See the
  status boundary above.
- No engine-frame synchronization, and no atomicity relative to the game's
  threads.
- No claim that a post-write observation is natural gameplay; a write-assisted
  setup stays write-assisted.
- No claim that closure can reclaim processes it did not record. Unattributed
  instances are reported, never guessed at.
- The 320x200 reject wording in the gate is derived from the positive marker
  forms rather than captured from a software arm; `INITSOFTRENDER` and
  `SYSTEM MEMORY ONLY` are verbatim. Recorded as `KU-075`.

## Next arm

The first live use should be the smallest possible: `game-session launch
--auto-hardware --dry-run`, then one authorized launch with
`--keep-on-reject`, comparing the tool's gate verdict against a hand-read log
and its discovered PID/window/display against the manual procedure. Only after
that agrees should `level` navigation or any write verb be used live.

## Related

- [[PC autonomous game control]] — the prose recipe this implements
- [[PC Flik teleport procedure]] — the write boundary `teleport` enforces
- [[PC level roster and numbering]] — the navigation table
- [[Runtime Tooling]] — the read-only capture tools this sits beside
- [[Reverse Engineering Capability Gaps]] — CAP-010 and the gaps still open
- [[Agent evidence and query tooling]] — the offline half of the same uplift
