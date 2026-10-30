---
type: implementation
status: active
created: 2026-08-15
updated: 2026-08-15
tags:
  - implementation/tooling
  - re/method
  - re/static
  - re/dynamic
---

# Python and C reverse-engineering split

## Purpose

Choose Python or C according to the measured investigation boundary rather
than assuming that the faster compiled language always produces faster
research.

There are three different meanings of “faster”:

1. **Execution speed:** C normally wins for tight loops, native callbacks,
   repeated memory scans, and high-rate sampling.
2. **Investigation throughput:** Python normally wins for parsing, hypothesis
   changes, orchestration, receipts, visualization, and synthetic tests.
3. **Evidence quality:** neither language wins automatically. The authority is
   still exact PC bytes, addresses, controlled runtime behavior, and a bounded
   experiment.

Decompiler C-like output is evidence, not source code. Rewriting it in C does
not make a static conclusion more authoritative. Native x86, file bytes,
cross-references, and runtime receipts remain the PC evidence.

## Default split

### Use Python first for

- offline file-format inspection, lossless parsing, hash/corpus work, and
  static export analysis;
- experiment orchestration, ownership checks, process lifecycle, schemas,
  receipts, comparison, and report generation;
- synthetic fixtures, negative tests, fuzz/property tests, and a readable
  reference implementation;
- low-rate read-only memory observation when the measured cadence has ample
  headroom;
- one-off calculations where development and review time dominate execution
  time.

Small PC assets such as `LEVEL*.DAT` and `TERRAIN.ALL` do not justify C merely
because C can parse them faster. A bounds-checked Python parser that finishes
well below the experiment budget is preferable because it is easier to audit,
change, and test.

### Use C for a demonstrated hot path

- an in-process hook, DLL/native callback, ABI-sensitive boundary, or another
  task that intrinsically requires native code;
- sub-frame or otherwise high-rate sampling where the Python prototype misses
  declared deadlines or perturbs the target;
- repeated large memory scans, binary filtering, compression, or event
  reduction whose measured CPU/copy cost dominates the experiment;
- a native helper that must preserve exact structure layout, alignment, or
  operating-system calling conventions;
- a bounded loop whose Python profiler/benchmark identifies interpreter,
  allocation, serialization, or scheduling overhead as the actual blocker.

Do not move code to C because a result is surprising, a parser is large, or a
decompiler displayed C-like pseudocode. Those are not performance findings.

## Decision procedure

### 1. Define the observation contract

Before choosing a language, record:

- bounded question and experiment/run ID;
- input size, address ranges, record widths, and expected event rate;
- required sampling interval or completion budget;
- whether reads must be coherent, atomic, callback-timed, or merely ordered;
- permitted target effects—read-only by default;
- required output fields, loss/drop accounting, and cleanup behavior.

The contract must state whether an occasional late sample is acceptable. A
tool cannot claim success against an unstated timing requirement.

### 2. Build the smallest Python reference

Implement or retain a straightforward, bounds-checked Python version first
unless the ABI itself requires C. It serves as:

- the executable specification for field decoding and edge behavior;
- the synthetic-fixture oracle;
- the controller for identity, launch, lifecycle, and receipts; and
- the fallback when native complexity would weaken evidence quality.

### 3. Measure the representative boundary

Use a declared bounded control window and record at least:

- total records/bytes and elapsed monotonic time;
- p50/p95/p99 iteration or batch latency where cadence matters;
- requested versus completed samples/events;
- late, missed, partial, invalid, and dropped counts;
- probe CPU and memory use when material;
- target-side perturbation against an unchanged control;
- time spent in memory syscalls, copying, decoding, and serialization when a
  profiler can separate them.

Python is adequate when it meets the declared budget with comfortable measured
headroom and zero unexplained loss. Do not invent a universal sample-rate
threshold: the required headroom depends on the experiment and host.

### 4. Promote only the hot loop to C

If the measurement identifies a real bottleneck, keep Python responsible for
policy and move only the minimal native operation to C. Prefer one of these
boundaries:

- a standalone C helper controlled by Python;
- a small shared library behind a narrow `ctypes`/FFI contract; or
- a native injected component only when the bounded experiment requires
  in-process execution and separately authorizes that mutation surface.

The C side should sample, filter, or transform bytes. It should not silently
assign game semantics, choose experiments, broaden address ranges, launch
unverified targets, or own cleanup policy.

### 5. Freeze the interchange schema

Every Python/C boundary needs a versioned contract. At minimum preserve:

- schema version and tool version;
- monotonic timestamp and sequence number;
- executable SHA-256 or a receipt-level binding to it;
- PID plus start time/ownership identity for live work;
- address, width, raw value/bytes, and validity/partial-read state;
- requested/completed/dropped counters;
- byte order and integer signedness;
- run ID and configuration hash where applicable.

Use JSON/JSONL when its measured cost is safely below budget. At higher rates,
use a documented fixed-width or length-delimited binary stream and decode it
in Python. A binary format must have truncation detection, explicit bounds,
and synthetic corrupt-input tests; raw native structs without a declared wire
layout are not a portable evidence format.

### 6. Validate C against Python

Before live acceptance:

- run both implementations over the same synthetic fixtures and captured
  read-only snapshots;
- require identical decoded records, ordering, signedness, overflow behavior,
  and refusal results within the stated contract;
- test zero length, truncation, impossible counts/ranges, partial reads, PID
  reuse, target exit, output backpressure, and counter overflow as applicable;
- compile a diagnostic build with strong warnings and sanitizer coverage where
  supported, then record the exact compiler/version/flags used for the live
  helper;
- retain Python as the differential oracle unless a later evidence packet
  explicitly replaces that authority.

The optimized helper is accepted only if it both preserves results and solves
the measured bottleneck. “C is theoretically faster” is not an acceptance
test.

### 7. Validate the live control

For runtime probes, begin read-only and follow [[Runtime Tooling]] plus
[[Agent Operating Manual#Runtime instance lifecycle]]. Require exact target
ownership, executable hash, bounded address ranges, complete loss accounting,
and an unchanged control. Any write, injection, execution control, breakpoint,
or register/code change still requires its normal explicit authorization;
using C grants no additional authority.

### 8. Record and clean up

The experiment/session note records the language decision, benchmark,
interchange schema, compiler/Python versions, exact commands, hashes, result
comparison, limitations, and cleanup audit. Track C source and tests, not
compiled binaries. Put generated helpers, captures, and game-bearing data only
under ignored `work/` or an approved temporary location. Leave no owned game,
probe, debugger, or audio-sink process running.

## Practical architecture

```text
Python controller/reference
  identity + hashes + launch + schemas + receipts + analysis
                     |
                     | versioned bounded contract
                     v
C hot-path helper (only when measured)
  sample/scan/filter/callback + sequence/loss accounting
                     |
                     v
Python validation/reporting
  differential checks + evidence packet + Vault update
```

This split keeps iteration cheap without giving up native performance where it
matters. It also prevents a fast probe from becoming an opaque source of
unreviewable conclusions.

## Current ABLPC examples

- `reimplementation/ablpc/terrain_all.py` is correctly Python: its bounded
  asset sizes, static/offline role, lossless preservation, and synthetic tests
  dominate any irrelevant parse-time gain from C.
- `scripts/coordinate-overlay.py` is correctly Python at its demonstrated
  display-aid cadence. A C sampler becomes justified only if a future bounded
  experiment requires materially higher cadence and measurement shows Python
  loss or target perturbation.
- A future in-process engine-tick hook or high-rate scan is a plausible C
  candidate, but it remains unimplemented and unauthorized until a concrete
  evidence packet defines the need.

## Stop conditions

Stay with Python when it meets the contract. Stop a C promotion when:

- the benchmark does not reproduce the alleged bottleneck;
- the native helper changes decoded results or hides drops;
- ownership, bounds, cleanup, or partial-read behavior is weaker;
- the interface requires more semantic duplication than the hot loop saves;
- a larger batch/read strategy fixes the cost without native code; or
- the task is really an unresolved evidence question rather than a performance
  problem.
