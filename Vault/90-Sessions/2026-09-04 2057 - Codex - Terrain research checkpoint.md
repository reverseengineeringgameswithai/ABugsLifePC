---
type: session
date: 2026-09-04
agent: Codex
status: research-checkpoint
---

# 2026-09-04 2057 - Codex - Terrain research checkpoint

The user asks whether to bank the terrain/collision work in Git or do more work
first. Bank the completed bounded research now; unresolved layout behavior does
not invalidate its experiments or require repeating them. This is a research
checkpoint, not a claim that arbitrary level authoring is complete.

The checkpoint follows parent `0f589de` and includes EXP-002 through EXP-010:
original retail collision loading/grounded controls, the canonical barrier
reader and rigid translation prototype, the floor translation prototype,
flat deck/block fixtures, depth-offset evidence, and the paused subdivision
comparison. Source, regression tests, numeric reports, original-instruction
evidence and Vault notes are included. The PNG/SVG included in reports are an
authored trajectory plot, not game screenshots or extracted assets.

Open follow-up work remains explicit: six residual analytic boundary samples,
other camera angles, a general render subdivision rule, EXP-005's return-floor
failure and shared boundaries. EXP-008/010 remain bounded improvements. No new
collision, rendering or R2q runtime conclusion is introduced by this Git bank.

## Validation and provenance

The mandatory `make check` was run but did not complete successfully. An initial
serial attempt was interrupted after 1,142 passed in 221.64 seconds. A six-worker
replacement reported 4,023 passed and 60 failed before interruption at 719.35
seconds. Its remaining workers were sampled, read-only, in unchanged R2q receipt
generation/validation. These are incomplete runs, never full-suite passes.

The parallel run exhausted the dedicated tmpfs user's storage quota (Errno 122).
A separate assertion expects `PREVIOUS_OUTPUT_029_SHA256` where the implementation
uses `PREVIOUS_OUTPUT_031_SHA256`: test line 5899 and implementation line 23234
in `test_r2q_quiet_census_design.py` / `r2q_quiet_census_design.py`.
Both files match parent `0f589de` exactly. Preserve this historical mismatch
without changing R2q code or weakening its test for a terrain checkpoint.

The serial disk rerun completes with **281 passed, 1 failed** in 451.67
seconds: all **222 terrain tests pass**, and 59 of the prior 60 failures pass.
Only the unchanged historical R2q expectation above still fails. Private log
hashes and validation limits are in
`reports/terrain/CHECKPOINT-20260904-terrain.json`. This bounded rerun does not
replace the unfinished full suite. Bank the research with that limit explicit.
Local optional test packages are pytest-xdist 3.8.0 and execnet 2.1.2;
pytest is 9.1.1. `uvx py-spy` sampled only test workers with `--nonblocking`.
No production dependency changed.

The staged asset audit passes. All 287 existing report file references with explicit
SHA-256 match their files; unavailable/ambiguous relative paths were not counted
as verified. EXP-008/009/010 JSON reports retain their earlier hashes.
Two generated text exports have trailing whitespace removed without changing
non-whitespace tokens. EXP-007's disassembly is hash-bound by its original
report, so its bytes are preserved using a narrowly scoped Git whitespace
attribute. The general whitespace check and other asset checks remain enabled.

Final environment, Vault, compatibility, asset and whitespace gates pass;
the claim sweep finds only the current checkpoint wording. Vault lint retains
eight warnings and no errors. All dedicated test scratch trees were removed
after retaining their logs and the serial JUnit result.

## Private evidence backup

A separate local archive preserves 1,115 private evidence files, 156,876,681
uncompressed bytes, with all members verified after writing:
`work/snapshots/terrain-20260904-evidence.tar.gz`, 34,812,935 bytes, SHA-256
`e2f0b8aca3e3610963ddb105fad479e4c7c9437348ce004b8b9cfceb10ee1731`.
It includes captured memory, screenshots, receipts and disposable operators;
Wine prefixes and symlinks are excluded. This is private local evidence backup,
not an off-machine backup or a restorable game save state. It is excluded from
Git along with the existing work copies. No originals are modified.

The banking work sends no input, memory write, debugger action, process signal
or restart to the user game. The final process/sink audit exactly matches EXP-010:
the same seven externally accounted user-session processes and `ablpc_mute_46458`,
with no test leftovers. Its nonzero status reflects the direct handoff's absence
from the fixture ledger, not a new leak. Game 46701/start 1147812 remains open;
its last verified gameplay state is the paused EXP-010 handoff with the original
zero-offset six-quad mesh restored.

Test-controller interrupts, read-only worker stacks and temporary-storage cleanup
are recorded under `work/experiments/BANK-20260904-terrain-001/`.
Historical R2q source, activation artifacts, mappings and protected stash
`76db1c9ee1ffffce52cea6aee591c24ab6a1c39a` remain unchanged.
