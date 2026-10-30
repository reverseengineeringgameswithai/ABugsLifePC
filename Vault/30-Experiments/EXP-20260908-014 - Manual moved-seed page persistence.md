---
type: experiment
id: EXP-20260908-014
date: 2026-09-08
environment: offline Unicorn and Wine Gamescope hardware Direct3D
question: Can full-capacity seeds remain usable, and can a moved seed survive terrain retirement?
result: Bounded growth-admission and moved-seed terrain-cycle acceptance
binary_sha256: 0afe3144be70fc5f2046601fa55d777ec4122ea1fa527cd664cbe82d8279b53b
status: complete
tags: [experiment/terrain, re/collision, implementation/modding]
---

# Seed growth admission and moved-seed persistence

Continues [[PC Large-Level Engine Roadmap]]. Public receipt:
`reports/terrain/EXP-20260908-014.json`; private evidence:
`work/experiments/EXP-20260908-014/`. Source image:
`6e5f081f34fa39eae8397d718ea4c6b8a25c97378f980b6679fab5225f89d11d`
from [[EXP-20260908-013 - Seed auxiliary budget and distant carry]]. Its frozen300
artifacts/22 dependencies remain exact. The normal build is not changed.

## Confirmed user-observed capacity regression

User-controlled manual64 game466588/start7097663/group466340 reached20 occupied
native plant records and12 seeds with pending countdown10. The user reported that
non-glowing seeds could neither be cracked nor picked up; glowing ones still worked.
`plant-pressure-*.json`, `unresponsive-seed-*.json`, `pickup-attempt-*.json` and
`glowing-comparison-*.json` under `manual64/` retain the observations.266 pickup
samples include pending actor36 in states8..11. The1990-sample glowing comparison
reaches carry12 for nonpending actors17/35/41 with all20 plant slots occupied.
Glow is a user-visible correlation; the exact visual emitter is not isolated.

The existing authored full-pool guard004BD100 jumps to0041EEEF, skipping ordinary
0041D5B0, including pickup completion11→12 and seed emissions. Native pickup selection
0043ED60 can still mark a pending seed held. Native collision handling0041C9B0 also
rejects further interaction while its countdown is nonzero. New native tests reproduce
the stationary failed pickup and execute the complete movement/pickup update to12
with the repair. This distinguishes the20-plant defect from EXP013's shared64-record
auxiliary pool; only14 auxiliary records were busy in the original pickup capture.

The user then threw a grown mushroom, saw its seed return and reported disappearance
of the previously unresponsive seeds. The post-throw snapshot still contains11 of
those seeds at countdown1 and20 occupied plants. Eight matched captured endpoints
have identical XZ and Y+18432, exactly nine native growth ticks of2048.
`buried-seed-endpoints.json`, `seed-growth-disassembly.txt` and native twelve-request
regressions agree: one vacancy lets all animations advance together; after the first
finishes, the rest freeze partway into the ground. The precise user throw transition
was not sampled, so its timing is inferred from those endpoints and reproduction.

## New authored admission policy

`reimplementation/ablpc/seed_growth_admission.py` and
`research/plant-capacity/seed-growth-admission.asm` form a separately hash-guarded
adapter.199 PIC bytes occupy004BE400; a5-byte redirect replaces the old guard entry.
It adds no image storage, leaves native constructor/allocator instructions and the
existing auxiliary guard exact, and keeps four counters at0107F490. The exact inverse
recovers the source image; sections and PE relocations are unchanged.

For native ten-tick growth, count free20-plant records and reserve vacancies against
all live seed animations at countdown1..9 in the fixed64-actor profile. A rejected or
held request cancels its countdown, refunds partial Y displacement and runs ordinary
seed update. The seed can be interacted with again. Growth requires another native
request once space is available. This supersedes the earlier automatic deferred retry
policy for the private candidate; it is not inferred retail behavior. Unexpected
positive countdowns above10 retain the predecessor behavior. No new retained actor
pointer, speculative plant marker, global allocator eviction or null-return policy.

47 regressions cover exact inverse/fail-closed bytes, both image bases, unmodified
native blocks, full native seed movement and pickup, partial-height recovery, held
cancellation,12 simultaneous requests against1/2/7/20 vacancies, completion through
native queue removal, endpoint actor reservations and legacy countdowns.138 focused
tests pass. Selected `make check` passes1682 tests in252.10s; unrelated R2q suites
remain excluded by the inherited explicit selection. No additional public source
changes follow that check.

## Confirmed fresh hardware lifecycle

`admission64` game479714/start7279634/group479465 loads the candidate from a private
copy. The fixture uses the demonstrated RAW pregrown flag for20 mushrooms and44
ordinary seeds; native decoding verifies the one changed type35 packet and all other
compressed packets remain byte-exact. Geometry/collision/model source files are exact.
Hardware/CD, selector and all65-model checks pass. The user explicitly returned
ordinary automated control while away; direct guarded XTEST supplies the actions.

A successful stomp produces3 capacity cancellations with all20 plants intact.
Actor63/contact64 then completes pickup12, a carry leg, throw and grounded landing.
Plant0 pickup/throw frees its record and returns original seed0. Another stomp grows
actor63 through10 native ticks into that vacancy. The other19 plant kinds, positions
and seed links remain exact across release/reuse; animated fields are not assumed
constant. `admission-lifecycle.json` records the assertions. Live recovery of the old
already-buried state and twelve-way live contention are not claimed; they are covered
by offline native tests. First missed stomp and bounded approach/heading attempts are
retained as nondiscriminating controller outcomes. A60s page-observer invocation
rejects its55s parameter limit before sampling; a valid55s replacement passes.

## Confirmed moved-seed terrain cycle

The original user-driven actor63 cycle was superseded at awaiting_pickup, with5039
samples and76 successful observer subwindows; it is explicitly unaccepted. After
capacity checks, automated actor20/contact21 is carried from terrain178 into179 and
thrown. It settles at(309685,-157709,608401). Returning only to spawn or the southwest
area does not unload its page, so neither route alone is a retirement pass.

The farther western route unloads page2. Actor20 is outside the live queue, its raw
contact pointer is zero and its anchor remains(page+1=3,offset36218). At least2.106s
and66 native frames pass with the page absent.277 cold observations across a42.726s
sample span preserve all132 actor and28 placement bytes. The old allocation49741824
is reused by managed page3, independently verified by page bindings/payload hashes.
On return page2 is resident, actor20 is active and its exact settled position is
unchanged. An additional pickup reaches12 with carry offset2640.

`persistence-summary.json`, `admission64/manual-result.json`, raw JSONL samples,
`monitor-events.json`, routes and `return-pickup20.json` supply the evidence.
The monitor records3491 samples and53 successful page/model sub-observers. Across
all candidate windows there are8266 page observations and8702 checks of all65 models.
The manual source game has9160 page observations and9313 model checks. No page/model
failure or level exit occurs. Actor/placement arrays are still resident throughout;
this closes one terrain-cycle check, not actual actor serialization or all items.

## Native reset and queue evidence

`native-reset-discriminator.json`: four cases execute original0041BD10 on captured
moved seeds at two bases and lose the moved positions by resetting from placements.
Two original0041C420 cases rescale initialized placement XZ by32 again. Their no-ground
fixture retains the native sentinel; initialization is not a proven restoration path.
`native-queue-discriminator.json`: ten original0041EC40 prefix cases cover no/first/
last/all64 admissions and then all-far. It writes a null terminator at0041ED6A but
leaves63 stale pointers after an all-far null head.16 recorded queue-base references
and18 actor-base references are bounded export results, not complete indirect-owner
coverage.0041B9F0's membership assumption and native seed-pair helper0041D390 remain
explicit lifetime boundaries. No PS1 evidence is consulted or promoted.

## Closure and remaining gates

Both private games and all their observers are CLOSED after pinned ownership checks
and post-close audits. Normal154936/start2024608/group154693 remains open;721 normal
files, saved Blender and760 wilderness-bank files remain exact. All10 pre-existing
normal/foreign audit identities are accounted for. No original/other-worktree changes,
external live writes, debugger stops or new normal installation occurred.

Milestone4 remains incomplete: actual actor/item/collected-state unload/restore,
full consumer/callback/driver lifetimes,310 numeric reference candidates, general
world/overlap budgets, wider coordinates and total-memory bounds remain open.
Next: define state-preserving section activation and native queue publication from
this evidence, with stable placement identities and explicit carry/plant ownership;
do not use native reset as serialization. [[PC terrain streaming ownership ledger]]
and [[Known Unknowns]] retain those boundaries.

Normal pose differs between the EXP014 baseline and final read-only endpoints.
`work/experiments/EXP-20260908-014/normal-state-endpoints.json` preserves both;
there is no continuous trace assigning the cause. Preservation covers files, image
and owned identities, not an unchanged Flik position. No pose reset was performed.
