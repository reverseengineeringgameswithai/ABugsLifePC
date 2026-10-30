---
type: experiment
id: EXP-20260908-013
date: 2026-09-08
environment: Wine Gamescope hardware Direct3D, Linux perf CPU-clock sampling, offline Unicorn
question: Which seed call stalls in the shared 64-record pool, and which other native consumers depend on that pool?
result: Call 0041DA68 inside seed update 0041D5B0 stalls in 0042AA50; 0041DA90's template53 emission can create retained records (flag 229/life 2) matching the saturated capture; 125 direct call candidates reach allocators 0042AA50 and 0042B020 over the same pool at 00598CA8, and some consumers dereference or retain results (0043EF06, 0043F598, collectible path 004292C0), so a global null return or eviction is unsafe. A narrow emission budget passes two distant-carry arms, but an unpatched positive control also passes.
binary_sha256: 6e5f081f34fa39eae8397d718ea4c6b8a25c97378f980b6679fab5225f89d11d
status: bounded-pass
tags: [experiment/terrain, re/collision, implementation/modding]
---

# Seed auxiliary budget and distant carry

Continues [[EXP-20260908-012 - High-slot seed interaction and native pool limit]].
Private paths below are relative to `work/experiments/EXP-20260908-013/`. The
indexed public packet is `reports/terrain/EXP-20260908-013.json`; original bytes
and dumps remain private.

## Confirmed caller and native capacity behavior

Fresh original-image `repro0` repeats the actor0 distant-carry stall at frame2627.
All197 Linux CPU-clock IP samples lie in0042AA5C..0042AA7E; their user stack pointer
is0117FE40. The four native prologue pushes put the return PC0041DA6D at SP+16,
identifying call0041DA68 inside original seed update0041D5B0. Its arguments are
(353856,-152572,720796,1,1). The read-only pool capture has all64 native skip
predicates true: byte+51 bit0x80 set and u16+34 nonzero. `controls-summary.json`,
`repro0/perf-ip-stack.json`, `repro0/stalled-pool.bin`, original instruction bytes
and EXP012's192 native search cases support this conclusion independently.
The perf stack read occurs after sampling while the same loop remains stalled;
it is not an atomic whole-process snapshot. No ptrace, debugger stop or external
live memory/register write was used.

`caller-census.json` finds125 direct E8 candidates into the two entry/thunk pairs:
91 into0042AA50/00401A9B and34 into0042B020/00401E60. The second allocator uses the
same64 records at00598CA8, stride56, and cursor00599B00. These are all-offset call
candidates, not a proof of exhaustive instruction/function boundaries. No PE
HIGHLOW absolute reference to the four entry/thunk addresses was found.

Some consumers discard results; others dereference, persist or pass them into
floor queries. Examples:0043EF06 writes through EAX after0043EEFC;0043F598 stores
the second allocator's result into a retained object field. Original004292C0 also
uses this pool for player collectible interactions. A global null return or
unconditional eviction therefore lacks the required caller/owner proof. The
whole pool must not be renamed as a cosmetic-only subsystem.

Original0041DA68 requests template1/motion1 when the seed ground word is nonzero.
Original0041DA90 requests template53/motion3 under its native state/carry condition.
Both results are discarded before the original stack cleanup and seed Y correction.
Native template53 initialization produces flag229/life2 and other retained fields
matching the saturated capture. Template1 instead has flag32/life12 and is reusable
under the search predicate. This establishes that the second emission can create
such retained records; it does not prove the birth caller of every captured record.
`native-template-check.json` executes both initializers at two image bases and
checks1200 live template bytes exactly against the PE.


## Bounded guard result and counterevidence

A private executable that skips only the discarded-return emissions at
0041DA68/0041DA90 while eight or fewer slots meet the native reuse predicate
(existing records are not cleared or evicted; the allocators and every other
callsite keep their original full-pool behavior) completes two distant
carry/throw/landing arms, with actor0/contact1 and actor63/contact64, all64
selectors and placement pointers correct and all65 model payloads exact. The
reserve of8 is an authored budget, not a proven upper bound for unrelated
callers, and omitted emissions also omit their RNG consumption.

**Counterevidence retained:** unpatched `positive64` also completes the same
ordinary destination and throw with offset8316 and advancing frames1849/1865/1881.
It has initial page/model checks only. The feedback routes are not
identical-input timing replays. Do not claim every unpatched high-slot traversal
stalls or independently attribute the trigger to actor0, density, paging or
timing. `controls-summary.json` retains this passing control alongside the
rejected stalled actor0 control. The narrower claim is the verified native
full-pool failure under pressure. General shared-pool policy and owner lifetimes
remain open: a fixed reserve cannot protect arbitrary bursts from the other
callers.

59 focused tests pass at both image bases; selected `make check` passes1635 tests
in242.09s. No ptrace, debugger stop, external live memory/register write,
original or PS1 source change, and no level exit occurred.
