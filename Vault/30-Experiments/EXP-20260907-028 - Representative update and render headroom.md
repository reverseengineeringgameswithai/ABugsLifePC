---
type: experiment
id: EXP-20260907-028
date: 2026-09-08
created: 2026-09-07
updated: 2026-10-29
status: bounded-measurement-passed
environment: Wine Gamescope Direct3D and offline Unicorn original-PC hook checks
question: Where do the native gameplay-update and render/present intervals begin and end, and how much per-frame work does a denser four-chunk layout use against native pacing?
result: Caller 0040FFC0 runs gameplay 004144C0 before renderer 0044D430 starts timestamp 00405C07, so the older timer covered render/present only; QPC hooks at 0040FFCA, 00405C07 and 00405B63 measure both; paired routes and one active mushroom stay below 1.7 ms of work against about 32 ms native pacing, with batches capped at 499 vertices.
binary_sha256: febbcaaef3a96d656ea75c495752a9612376dddc412c3cfec75c7855e9133b23
evidence: [EXP-20260907-023, EXP-20260907-026, EXP-20260907-027, EXP-20260907-028]
tags: [experiment, re/rendering, terrain/collision, implementation/modding]
---

# Representative update and render headroom

This experiment corrects the boundaries of the EXP-026 frame timer and measures
per-frame gameplay-update and render/present work on representative movement
over the EXP-026 control and visual-detail layouts, plus one native
active-mushroom contact. It does not accept arbitrary dynamic populations or
wider coordinates.

Evidence root: `work/experiments/EXP-20260907-028/`; tracked findings/index:
`reports/terrain/EXP-20260907-028.json`. Authored diagnostic assembly is in
`research/stage3-frame-probe/`. PC retail reference remains
`97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878`.

## Confirmed timing correction and boundaries

EXP026's coarse timer measures **render/present only**. It starts at timestamp
store00405C07 inside00405BE0, called from renderer0044D430 at0044D44A.
Caller0040FFC0 executes gameplay004144C0 first. Thus the old samples cannot
represent complete gameplay-update work. `0040ffc0.c`, `00405be0.c`,
`0044d430.c`, `004144c0.c` and `timing-boundaries.asm.txt` preserve the static
call order. EXP026's frozen private files remain unchanged; its note/report now
carry this correction. The new live measurements independently show a positive
update interval preceding the render interval.

The private probe resolves QueryPerformanceCounter/QueryPerformanceFrequency
through the existing kernel32 IAT. Start0040FFCA precedes gameplay; start00405C07
preserves the native timestamp and measures rendering separately; end00405B63
follows present and precedes the native pacing loop00405B72. All eight hooks and
the 192-byte record ABI are documented alongside the authored assembly.

QPC reports frequency10000000 in both live arms. Back-to-back call gaps have
control median0.1 microsecond and p99 0.2 microsecond; this is a call-gap diagnostic,
not a guarantee of effective timer accuracy. The timer API contracts are the
[Microsoft QPC](https://learn.microsoft.com/en-us/windows/win32/api/profileapi/nf-profileapi-queryperformancecounter)
and [QPF](https://learn.microsoft.com/en-us/windows/win32/api/profileapi/nf-profileapi-queryperformancefrequency)
documentation, not game-behavior evidence.

Intervals are elapsed wall time for gameplay update plus render/present, and
render/present separately, including hook/host/Wine effects. End-record copying,
outer application-loop work and deliberate pacing are excluded. Present may
submit asynchronous GPU work; these are not isolated GPU completion timings.

## Private instrumentation validation

`build-probe.py` guards normal EXE431ec953…c7d8f, installs1566 authored code bytes
in4096 verified CC bytes at004BBC00, checks every displaced instruction, changes
only the necessary HIGHLOW entry at00405C08, and proves an exact inverse.
`test-probe.py` passes50 checks at image bases00400000 and01400000: integer
registers/ESP/flags, displaced operations, stdcall batch arguments, API failures,
64-bit subtraction borrow, inactive/level/cursor bypass, known record fields and
ring wrap. API internals/LastError and arbitrary whole-engine state are outside
that equivalence check. COM/helper/API calls are stubbed offline; real hardware
runs supply the separate integration evidence.

The diagnostic ring occupies01000000..010600FF inside the upper8MiB arena.
Exact fixture cursors stay below01000000; this is not a general reservation
protocol for arbitrary growing loads. The reader validates both publication
sequence words, continuity and frequency. One synthetic valid row and10 malformed
frequency/length/sequence/timing cases pass `test-decoder.py`.

## Representative route measurements

Each fresh hardware arm drove four goals in stored X/Z, two repetitions, plus
initial 8-second spawn and 8-second settled holds, producing contiguous per-frame
records with camera matrix/translation, primary admission/chunk mask, submitted
vertices/indices/batches, collision-collector calls/maxima, plant/seed counts,
contacts, lives and cursor (`accepted-measurements.json`, `comparison.json`,
`profile-phases.json`):

| Measurement | Earlier control | Visual detail |
| --- | ---: | ---: |
| Valid frames | 4561 | 4417 |
| Update+render/present p99 ms | 0.4921 | 0.6591 |
| Update+render/present maximum ms | 1.5033 | 1.6506 |
| Render/present p99 ms | 0.3978 | 0.5724 |
| Update interval p99 ms | 0.1047 | 0.1106 |
| Maximum submitted vertices/frame | 6345 | 11012 |
| Maximum vertices/batch | 499 | 499 |
| Maximum root0/root1 indices/batch | 747 / 744 | 747 / 741 |
| Maximum candidates, all / Flik calls | 17 / 17 | 18 / 16 |

Zero telemetry errors/dropped records/publication retries. All measured work
intervals are below the approximately32ms native pacing interval. This
establishes measured headroom for these routes, not a worst-case maximum. The
direction of increased rendering work agrees with EXP026's independent
identical-context native instruction/buffer comparisons.

## Native observations from the active-plant arm

PC controller0043F9E0 selects its airborne countdown at004402-region code when
input bit4000 is pressed after release. Input mapping004D8458 associates that
bit with left Shift. Decompiler evidence is retained as such in
`player-controller.json/.c`; actual keyboard/live state supplies corroboration.
No position, input or actor memory is externally written.

`seed-jump-1.json` records a nonzero seed countdown (sampled2..9), then plant
slot2/type5, runtime descriptor224/tag108. The observed mushroom uses exact964
bytes of PLANTTER source8, payload10000361, with descriptor origin matching
actor(197986,-101738,564000). `active-plant-verified.json` verifies these bytes
and the native template mapping after interaction. [[PC seed and mushroom collision state]]
contains the earlier native constructor/bounce-store evidence. The opening and
subsequent jump-return traces each observe nine distinct upward velocity-3328
onsets and contacts alternating178/224; these are observed velocity onsets, not
live instruction tracing.

The separate75.06s `active-plant.bin/.json` captures2342 contiguous frames.
Whole-work p99/max is0.6498/1.3971ms. Maximum collector candidates26 overall/25
for Flik; vertices/batch499, root0/root1 indices747/690. This is one active type5
interaction, not saturation of the20-plant/64-entity pools or a general dynamic
overlap bound.

## Integrity and evidence hygiene

Both diagnostics verify all four resident chunks and all170 model payloads
before/after traversal. `full-inventories.json` verifies721 expected files in
each arm; only the native log is added. Generic audit is ownership metadata,
not validated CAP-010 runtime evidence.

Normal level initialization logs one NextLife call. An initial overbroad log
predicate rejected it; `rejected-log-predicate.json` records the correction:
compare against the initial count1 and require unchanged events. No later
NextLife or in-route death is observed. Previously indexed EXP027 files retain
their whole-file hashes except one mutable launch console, preserved by prefix
hash in `prior-packet-recheck.json`; new indexing excludes mutable launch consoles.

Broader simultaneous local actors/collision density remain open. Validate
coordinate arithmetic before increasing extent. No R2q acceptance claim is made.
