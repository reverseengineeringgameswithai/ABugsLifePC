---
type: experiment
id: EXP-20260908-016
date: 2026-09-08
environment: Wine hardware Direct3D and offline Unicorn x86
question: Which native structures hold references to a carried and thrown seed after its terrain section goes out of range, and why do crowded seeds fly apart?
result: Exact seed start-address matches lie only in queue and selected-pointer fields, and queue publication uses the prefix before its terminator; 00415E30 writes slot63 XYZ when mode bit 0x80 at 0059D9A0 is set, so an empty queue is not a release certificate; pair routine 0041D390 adds -256/+256 X velocity per call to seeds within the 125000 squared-distance threshold with no speed clamp, a supported explanation for crowded-seed velocity buildup
binary_sha256: 0afe3144be70fc5f2046601fa55d777ec4122ea1fa527cd664cbe82d8279b53b
status: complete
tags: [experiment/terrain, re/collision, implementation/modding]
---

# Manual seed ownership and native scattering

Continues EXP-20260908-015. Private packet: `work/experiments/EXP-20260908-016/`;
asset-free public index: `reports/terrain/EXP-20260908-016.json`.

## Procedure

One fresh isolated copy uses 64 file-loaded seeds and 20 pregrown plants.
Automated ordinary Right/Return/Return input enters gameplay; the user supplies
pickup, carry, throw, departure, return and repeat pickup. `observe-roots.py`
reads `/proc/26409/mem` with O_RDONLY. It samples the contiguous
00599EB0..005A91EC placement/actor/Flik/queue/plant/selected span plus separate
contact and anchor records at about 10 Hz, saves owner-change records, and takes
twenty bounded 3,811,696-byte `.data` copies at 004C1000. All reads are
asynchronous. Before/after frame-counter equality is recorded, not atomicity.
No external RAM write, debugger stop, live slot removal or new engine patch occurs.

## PC confirmed: moved seed and actual enumerated owners

`manual64/user-roots-01/samples.jsonl` contains 5,965 accepted observations over
about ten minutes, with no owner-parser errors, level transition or life loss.
All 64 placement pointers/selectors remain correct. All twenty plant seed links
retain their initial type5/actor0..19 identities. The user did not free a plant
record during this arm; EXP014 owns the separate mushroom-release evidence.

The moved seed is actor63/contact64, address0059D6A4 and carry byte offset8316.
First pickup reaches state12 at elapsed20.117s; throw clears carry at26.855s.
The seed settles at (225692,-105140,569712), distinct from its initial position
(192000,-106499,435200). On departure, 2,043 consecutive samples spanning
205.369s / at least6,418 frames show its terrain page (page1) absent, the seed outside all enumerated
owners, and the exact same complete actor SHA-256. Page return at308.071s retains
that XYZ; repeat pickup reaches state12 at321.549s with the same selected pointer
and carry offset. `observation-summary.json` gives exact endpoints and hashes.

`manual64/user-cold63.json` captures the actual full queue, all twenty plant
records, selected pointer, carry offset/state and seed actor/placement/contact/
anchor. Selected/carry are zero, queue terminates at index12, and seed63 is not
pinned. Actor/placement bytes are re-read and compared before acceptance. Anchor
is file offset89834, descriptor178.

This supplies the real plant/selected roots missing from EXP015's different
sample. It still does not prove atomic quiescence or exhaustive ownership.
Actor and placement storage stayed resident throughout the live terrain cycle.
The ordinary live game never unloaded or restored the serialized actor record.

## PC confirmed: references beyond a raw-pointer census

All exact seed63 start-address matches in twenty native `.data` copies are queue
or selected-pointer fields. Each of the seven copies taken while the seed's section was out of range (elapsed120..300s)
contains only six stale queue suffix matches: 0059D82C, 0059D834, 0059D83C,
0059D850, 0059D860 and0059D868. Native queue publication uses the prefix before
its null terminator, as independently established in EXP014. This byte-aligned
and unaligned search covers only the exact start address in `.data`, not interior,
encoded, computed, heap, stack, driver or unobserved-state references.

`static/relocated-native-references.json` independently enumerates exact PE HIGHLOW
operands into bounded storage:957 actor,4 placement,47 queue,11 plant,9 selected
and22 carry references. Actor target literals span37 slot regions and50 candidate
function entries. Some operands are indexed bases, so these counts do not mean
37 exclusively fixed slots or957 active owners. `verify-static.py` matches951
actor operands to Ghidra target references and exact decoded instruction offsets.
Six others decode to the same PE target but lack a matching exported target:
one Ghidra reference resolves indexed base004320AE to0059B730, while its literal
operand is0059B628; five lie outside the candidate function's exported references.
Their function ownership remains unconfirmed. No guessed function name is added.

`native-fixed-slot.json` is the decisive independent counterexample to treating
an empty queue as a release certificate. Original00415E30 checks mode bit0x80
at0059D9A0 and writes slot63 XYZ at00415FB3 onward when the mode is set, even
with kind11 and an empty queue. Eight controls at two bases cover kind11/35 and
mode0/0x80. Mode0 returns without touching the slot; mode0x80 copies Flik XYZ,
stopping at00416000 before animation handling. All twenty live `.data` captures
have that mode bit clear. This is a possible native consumer, not evidence that
it caused this seed's behavior. Script00415140 also computes actor addresses from
script indices; raw-pointer scanning cannot establish those identity lifetimes.

## PC confirmed and inferred: seeds flying apart

The user reported that several seeds flew apart while approaching the far area.
Initial far slots32..62 are packed on a100-world-unit grid and already have flags
0x38 with velocity(0,-3328,0) before approach. At elapsed29.670s their activation
starts publishing flags0x4000 and changing velocities. This temporal association
does not by itself assign every displacement to paging or a single native routine.

Two seeds58/59 remain at captured edge coordinates (253369,-147310,858111) and
(263269,-147292,858108). Their X velocities grow in opposite directions while XYZ
stay fixed:2,072 adjacent sample pairs match -256/+256 per observed frame step,
covering6,511 frame steps. `native-seed-pairs.py` replays original0041D390 and
normalizer00464BE0 from the captured data-0120 records. At both image bases,
120 consecutive calls add exactly -256/+256 X velocity per call with no position
change. Moving the second seed400 world units away, publishing neither seed, or
publishing only one eliminates the impulse. All eight cases pass.

The native shape at004DDC00 has i16+14=250; the pair routine's squared-distance
threshold is2*250*250=125000, about353.55 world units. The captured pair is about
309.38 units apart. There is no speed clamp in that pair function. Original
0041D5B0 applies ground-dependent friction separately; its flag0x08 path initially
updates Y alone. The crowded launch state and eventual edge trapping therefore
provide a supported explanation for velocity buildup and a candidate cause of the
reported burst. The complete cause of initial scattering and boundary trapping is
still inferred; no full-frame terrain/spacing/launch-flag discriminator or fix is
claimed. Preserve this density stress fixture. Use a separately hashed spacing-only
control before changing native physics or the normal authoring pipeline.

## Validation and open questions

152 new bounded native cases pass:8 pair,8 fixed-slot,8 pickup and128
cached-cell-reader cases. Vault lint, M4 compatibility, tracked-asset and
whitespace checks are recorded in `final-gates.json`. No originals or PS1 source
is modified or consulted. Source and asset payloads, screenshots and memory copies
remain private under work; public evidence is metadata.

Open: classify the gated fixed-slot and script-index consumers, and keep the
scattering spacing control separate before changing native physics.
