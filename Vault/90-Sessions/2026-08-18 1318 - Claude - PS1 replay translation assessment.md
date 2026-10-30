---
type: session
date: 2026-08-18
agent: Claude
status: complete
tags:
  - session
  - research/cross-port
  - input/replay
  - cap/CAP-002
---

# PS1 replay translation assessment

## Agent

Claude.

## Goal

Answer a bounded question from the user: can the PS1 project's working input
replays (`SRC-PS1-ABL`, `/home/dev/Downloads/ABL`) be "translated" to ABLPC,
given the severe PC replayability problem (CAP-002: exact input delivery
proven, gameplay outcomes still diverge)?

This session was **read-only research**: no game, Wine, Gamescope, emulator,
debugger, or target process was launched; no file outside this note was
created or modified; `originals/` was not touched. The external PS1 repository
was read through `git show`/`git grep` on committed content only, per
[[Cross-Port Evidence Policy]].

## External source provenance

`SRC-PS1-ABL` re-observed at the same commit recorded in
[[External Source Registry]]: `1186eb6eb9712689a0ebd6a5d1d5c1ba61cc2f51`
(branch `master`, working tree still dirty; only committed blobs were read).
Material read, all at that commit:

- `ObsidianVault/Experiments/EXP_2026-08-01_savestate_movie_arm_phase_desync.md`
- `ObsidianVault/Experiments/EXP_2026-08-05_movie_state_binding_verified.md`
- `docs/PS1_RE_REGRESSION_ARCHITECTURE.md` (grep only)
- directory listings of `tools/`, `analysis/`, `tests/` movie infrastructure

This is **tooling/methodology** evidence in the same category as
`SRC-DUCKSTATION-DBG`: it establishes no PC game semantics and is not promoted
to any PC claim.

## Findings (assessment, no new PC evidence)

1. **What the PS1 side actually has.** A forked DuckStation with first-class
   input movies (`src/core/input_movie.cpp` in their fork): frame-indexed
   controller samples applied at the emulator's own per-frame input poll,
   anchored to a savestate, with the start-state SHA-256 bound into the movie
   and verified on both playback entry points before any mutation
   (their `EXP_2026-08-05`). Determinism is a property of the **emulator
   owning all time and input sampling**, not of the game or of host input
   precision.

2. **Why this cannot be transplanted onto the current PC harness.** The PC
   divergence is already proven not to be an input-delivery problem:
   [[EXP-20260815-125 - Persistent echoed replay and residual gameplay divergence]]
   shows two 300/300 exact, echoed, sub-millisecond deliveries reaching
   different game states. The PC engine does sample input once per frame into
   an action-bit word (`0x0042EBC0` reduces DirectInput state `0x00598A10` to
   `0x00598B10`, KU-070) — structurally the analogue of a PS1 pad word — but
   on host Wine the frame boundaries and durations are wall-clock and
   scheduler driven. Wall-clock X11 movies cannot become deterministic in
   place; this matches CAP-002's recorded limitation ("cannot observe the
   game's internal frame counter").

3. **The translation is architectural and is already decided.** The PS1
   model translated to PC = run the real PC binary under a full-system
   emulator that owns time, and put the movie at the emulator layer. That is
   exactly [[Decision Log#DEC-20260817-145 - Deterministic replay via libTAS + single-threaded PCem, not rr]]
   (Gate 1, libTAS + PCem-st, not yet run) plus Gate 2 (guest memory oracle,
   **proven** on the 86Box gdbstub build, KU-077, 2026-08-18). So the answer
   to "is it possible" is yes-in-principle by the same mechanism that makes
   the PS1 replays work; the remaining risk is Gate 1 execution, not concept.

4. **What newly translates from `SRC-PS1-ABL` (beyond DEC-145): the movie
   contract and its failure catalog.** Their experiments are a paid-for list
   of silent failure modes that the Gate-1 acceptance spec should require
   from day one:
   - **Arm-phase binding** (their `EXP_2026-08-01`): a savestate-anchored
     movie replayed one frame out of phase, silently, depending on whether
     recording was armed while paused or running; fixed by recording the arm
     phase in the movie (`armed_while_paused`) and honouring it on playback.
     The PC harness must record the equivalent arm/anchor phase.
   - **Drive-mode equivalence is not free**: their `movie.advanceToFrame`
     did not reproduce 60 Hz playback (different pump/poll path). Anything
     phase-sensitive must be verified in the same drive mode as recording.
   - **Start-state hash binding with provenance** (their `EXP_2026-08-05`):
     movie carries the anchor state's SHA-256, checked before mutation on
     every entry point; `recording` vs `backfill` provenance kept distinct
     because a backfilled hash certifies an already-drifted state as good.
   - **Bind the execution-core identity** into the movie (their movies are
     interpreter-scoped; ABLPC's 86Box interpreter-vs-dynarec distinction in
     KU-077 is the same hazard).
   - **Objective memory oracles at fixed frames** (their inv-timer
     write-count + grant-at-frame pattern) — the PC analogues are the already
     understood globals (`0x00861C84` level, `0x0059D910` Flik XYZ,
     `NextLife`) and DEC-145's progressive `.data` fingerprint plan.
   - **Corpus discipline**: never blanket-"correct" a movie corpus; correct
     only movies individually shown to be off (their `tools/rephase_movie.py`
     warning), plus inventory/minimizer/priority tooling as patterns.

5. **What does not translate.** The literal movie files and routes: different
   binary, platform, controller vocabulary (pad word vs PC action word), and
   frame timing; any frame-index correspondence would be cross-port inference
   only, and it would not address the actual PC failure (host
   nondeterminism), which exists regardless of input content. Also noted and
   set aside: a PC-native "frame-hook" alternative (write `0x00598B10` each
   frame under a debugger) is not currently viable — Wine execution
   breakpoints fault (Environment Status caution at `0x0044D79A` family) and
   the 86Box stub is fragile under repeated connects (KU-077), while a
   per-frame hook needs thousands of stops.

6. **Open Gate-1 caveats flagged, not resolved:** (a) the TASVideos PCem-st
   machine (686BX/Voodoo3 ROM set per DEC-145) differs from the 86Box harness
   machine (i430VX/Trio64V2), so the existing Win95 image will face hardware
   re-detection or a fresh install under PCem-st; (b) how Gate-1 oracle reads
   are taken **under PCem-st** (whose debugger is weaker than the 86Box stub)
   is the instrumentation question DEC-146 left open — options include
   pairing roles (PCem-st replays, 86Box stub audits an equivalent run) or a
   PCem-side memory access, to be settled at Gate 1.

## Changes made

This session note only. No Current State change (no runtime evidence, no new
PC fact, no milestone movement). External Source Registry unchanged (same
commit re-observed).

## Unresolved questions

Gate 1 itself (PCem-st determinism on this game), the two Gate-1 caveats
above, and CAP-002's event-specific acceptance — all pre-existing.

## Recommended next action

Adopt the `SRC-PS1-ABL` movie contract (arm phase, state-hash binding with
provenance, core identity, fixed-frame oracles, drive-mode equivalence) as
the written acceptance spec for Gate 1 before building PCem-st, so the PC
harness starts where the PS1 harness ended rather than rediscovering its
silent failure modes.

## Process audit

No processes launched; no sinks created; nothing to close. Read-only `git`
inspection of the external repository and Vault/tool file reads only.
