---
type: session
agent: Codex
date: 2026-08-15
status: complete
tags:
  - sessions/codex
  - cap-002
  - input-movies
---

# First companion replay diagnosis

## Scope

Validate and replay the user's first companion movie, explain why it did not
repeat the observed hardware-to-Training-completion route, preserve runtime
evidence, and leave no obsolete PC runtime or private sink.

## Evidence

- The requested `input-20260815-145546.input-movie.json` was the companion's
  next unused path, not the saved movie.
- `RUN-INP-REC-20260815-145456` identifies the actual accepted movie
  `input-20260815-145429.input-movie.json`, SHA-256 `49261fa3...eb73f9`, with
  306 paired events and a manual-delay anchor.
- Its first event is Return at +5.336 seconds. No renderer-selector Down exists
  before it; the first Down is sequence 108 at +23.315 seconds.
- One fresh discriminating arm supplied only the missing pre-anchor Down and
  replayed the immutable movie. `RUN-INP-REP-20260815-150349` accepted 306/306
  dispatches, all-key release, and 17.772 ms maximum drift.
- The fresh PC log passed all four hardware gates but loaded only level00 and
  reached Level Select. The user observed Flik's Journey moving back and forth
  without entering Training.

## Conclusion

Exact input dispatch works, but the current companion's independent manual
delay does not establish a repeatable gameplay state. Dispatch acceptance is
not gameplay acceptance. The initial missing Down, saved/next filename
confusion, and terminal-Ctrl-C cleanup failure are separate live defects. See
[[EXP-20260815-121 - First companion route replay divergence]] for the bounded
confirmed/inferred/unknown split.

No implementation fix was made because this packet was diagnostic. The next
work should add a shared fresh log/game-state anchor, explicit anchor readiness
and saved path, a safe replay action, and process-group cleanup that survives
leader exit before attempting KU-057 again.

## Verification

- The actual user movie passes strict schema validation.
- The replay receipt accepts 306/306 exact-schedule dispatches and all-key
  cleanup; visible/log gameplay acceptance is separately rejected.
- `make check` passes 556 tests, 353-note Vault lint, all five M4 compatibility
  anchors, and the tracked-file audit with zero violations.

## Cleanup

The interrupted GUI arm and replay arm left exact owned Gamescope reapers and
one `ablpc_mute_18873` module after normal termination failed. Cleanup targeted
only the proven PIDs/process groups and module `536870916`. Final host process
and PipeWire audits matched no ABLPC game, Gamescope, Xwayland `:2`, recorder,
or private mute sink.
