---
type: experiment
id: EXP-20260815-124
date: 2026-08-15
question: Does the accepted Level Select replay deliver the recorded keyboard event stream to the PC game window without transformation?
status: completed
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora Linux 44 Workstation; Wine 11.0; Gamescope; input-movie.py 1.1.0; companion 1.1.0
environment_version: input-movie.py 2c7b3650d50a032f0e5ee2f83eba664171e46fa9089a0f394c6b2ca4e16281cc; companion 7997c53dffd39a02172df4e3a654ce73e8af2704d3a6a2e8f7be1ad704161918
working_directory: /home/dev/ABLPC
configuration: pristine PC work copy; research/windowed/muted; fresh replay; simultaneous exact-window X11 echo recorder; timestamped research-log observer
artifacts:
  - dynamic/wine/RUN-INP-REP-20260815-162512/metadata.json
  - dynamic/wine/RUN-INP-REC-20260815-162512/metadata.json
result: accepted-dispatch-receipt-hides-measured-target-stream-transformation
created: 2026-08-15
updated: 2026-08-15
tags:
  - re/experiment
  - implementation/tooling
  - input/replay
  - cap/CAP-002
---

# EXP-20260815-124 - Replay echo identifies target input stream distortion

## Question

Why did the accepted replay of the user's Training-completion movie visibly
desynchronize, and was the first gameplay key sent before Training finished
loading as previously inferred?

## Inputs and method

The immutable source movie remained
`work/copies/input-movies/input-20260815-160751.input-movie.json`, SHA-256
`abc45db6a5822c6eeb5f56b045e237b7b8c9a84814de13ed0abf4f79deb17b91`,
with 300 normalized events and schedule SHA-256
`23e0dbc0f237199bcf3cc84d08a9d481ccf38213396a1ad60d637e2c9dd119ad`.
It was replayed unchanged in a fresh pristine Hardware arm.

Before the shared `--- Start LevelSelect ---` marker, a second production X11
observer was armed on the same proved 640x480 `bugs.exe` window. It recorded
what that target window actually received during replay to the ignored,
create-only diagnostic file
`work/copies/input-movies/diagnostic-replay-echo.input-movie.json`, SHA-256
`50c951ed7797a25718c86e088f6b84fa94f83d9c4160c0971276c2e106158943`.
The echo observer used the same marker and zero neutral wait. Its reported
recording start followed replay's reported start by 1.032277 ms. An independent
monotonic observer timestamped appended PC research-log milestones against the
same host clock.

No game bytes, files, memory, debugger state, movie content, or PS1 evidence
were changed. The diagnostic echo movie remains ignored under `work/`; only
its asset-free record/replay receipts are curated.

## The loading hypothesis is not supported by this replay

Relative to replay's `replay-started` timestamp, the independent observer saw:

- `gfx\training.raw` at 3.564772852 s;
- `level07\level1.raw` at 3.974200803 s;
- `---End InitMainGame---` at 5.545018592 s; and
- `NextLife` at 5.545035213 s.

The source movie's first gameplay-looking `z` down is at 6.498976937 s. It
therefore reaches the replay target approximately 953.942 ms after `NextLife`,
not during the measured load. This corrects EXP-123's proposed direct
"first gameplay key lost during loading" mechanism. The original recording's
`NextLife` was not timestamped, so record-versus-replay phase at that boundary
remains unknown.

The fresh `bugs.log`, SHA-256
`1c2a67df62538810d079c73f820215bcd34667b8815066364e8a3f3f3423ed6e`,
again independently passes Hardware/Direct3D and loads Training before
`NextLife`.

## Accepted dispatch is not delivered-stream fidelity

`RUN-INP-REP-20260815-162512` accepts 300/300 scheduled events, releases all
keys, and reports maximum absolute pre-send drift 23,330,124 ns. Its metadata
is SHA-256
`a0e0dd7e0c5227904f828e455e206aa1fafbc7db8e3d51ed0e6c8f7439d1d1e8`.

The simultaneous echo contradicts an exact target-stream interpretation:

- the source has 300 normalized events, while the echo has 304;
- ordered comparison finds two inserted `Right` up/down pairs, before source
  events 213 and 241;
- the echo recorder also observes and normalizes away 150 unmatched release
  events, exactly one for every source keydown; the original recording receipt
  normalized away 139 such releases;
- source event-state values are `0/1/4/8`, while echo values are those same
  values plus `256`; the meaning and gameplay impact of that state-bit
  difference are not established here; and
- several nearly simultaneous source transitions are delivered about 15.1 ms
  apart. Source events 47-48 (`z` up then `Left` down) are 52,570 ns apart but
  echo 15,104,441 ns apart. Source events 69-70 (`Left` up/down) are 19,710 ns
  apart but echo 15,161,352 ns apart. Comparable dilation occurs at source
  pairs 71-72, 85-86, 87-88, 89-90, and 211-212.

After aligning the first normalized source/echo event, the first absolute
timing difference over 2 ms is source event 26. The first difference over
5 ms is event 48 at source offset 18.076880067 s, where it is 12.765516 ms.
Before the first inserted pair, aligned error ranges from -39.239264 ms to
+15.884774 ms. Individual holds also change materially: the source event
210-211 `Right` hold is 40.246728 ms but echoes as 5.065174 ms; event 212-214
is 155.903430 ms but echoes as 181.229799 ms; and event 213-218 `Up` is
598.483583 ms but echoes as 578.466369 ms.

The record receipt for the echo is
`RUN-INP-REC-20260815-162512`, metadata SHA-256
`e8887a69556e5d2dd167add2b6f8af2c57a1cf72b3a8a0b854e3088fe58832dd`.

## Mechanism and causal boundary

Static implementation evidence in `scripts/input-movie.py` explains why its
receipt did not catch this. `XDoTool._run` launches and waits for a new
`xdotool` subprocess. The replay loop performs one such focus query per event,
timestamps `dispatched_ns`, and only then launches another synchronous process
for `keydown` or `keyup`. Thus `drift_ns` measures arrival at the call boundary,
not the X11 event observed by the target; back-to-back recorded transitions
can already be late by the time the preceding send and next focus processes
finish. The source's very short same-key release/down pairs are consistent
with X11 key-repeat transitions, but that interpretation is inference rather
than required for the measured mismatch.

**Confirmed:** the current replay path does not reproduce this movie's
normalized event sequence or timing at the target window. It adds two
normalized events and changes multiple transitions/holds by approximately
15-39 ms. These changes are sufficient to let a frame-sampled game observe a
different input state and are a concrete input-side desynchronization
mechanism.

**Not yet confirmed:** which altered event produced the user's first visible
route divergence. That observation was not timestamped, and this experiment
does not compare internal PC game frames or state at each event. Variable
record-versus-replay game phase and the absence of engine-frame scheduling
remain independent possible contributors.

## Result and next discriminator

Reject the 1.1.0 `xdotool` subprocess backend as evidence of exact long-route
delivery, even when its dispatch receipt accepts. Before changing anchors or
using CAP-002 for KU-057, replace or redesign delivery so one persistent
connection can preserve the normalized sequence and close timing, and add a
simultaneous target-window echo regression. Then replay this immutable movie
as an A/B discriminator. A post-load anchor can be reconsidered only after
delivery fidelity passes; the current evidence does not justify treating it
as the primary fix.

## Lifecycle

The companion, exact launcher group, game/Wine/Gamescope processes, both input
workers, timestamp observer, and private `ablpc_mute_39067` sink were closed.
One exact Wine device process ignored `SIGTERM` and was removed with scoped
`SIGKILL`; the final process/sink audit was clear. The complete repository gate
passes 557 tests, Vault lint at 359 notes/zero errors/zero warnings, the five-
anchor M4 compatibility statement, and the tracked-file audit.

## Links

- Superseded inference:
  [[EXP-20260815-123 - Level Select anchored route gameplay desynchronization]]
- Contract: [[PC input movies]]
- Capability register:
  [[Reverse Engineering Capability Gaps#CAP-002 — Deterministic PC input movies]]
