---
type: research
status: bounded-evidence
created: 2026-09-08
updated: 2026-10-02
tags: [re/collision, implementation/modding, terrain/authoring]
---

# PC terrain streaming ownership ledger

*Status (2026-10-02 audit):* the user paused Milestone 4 on 2026-09-08 after
EXP-20260908-016, incomplete ([[PC Large-Level Engine Roadmap]]). This ledger
records that state; its open boundaries are not an active queue. Do not resume
streaming from it without new user direction.

This is the reference-lifetime map for [[PC Large-Level Engine Roadmap]]
Milestone4. The private four-page prototype is evidence for a finite profile.
A matching integer, an inactive actor, or a successful route is insufficient
on its own to establish that an allocation has no remaining consumer.

| Storage / consumer | Covered behavior and evidence | Remaining boundary |
| --- | --- | --- |
| Four managed DAT geometry fields | EXP009 renderer entry004498F0 ensures the requested page before original consumption. Frame retirement restores compact placeholders before freeing. EXP011 classifies the four published fields in EXP010's saved census. | Other dispatches and future scene layouts need their own consumption/ownership proof. |
| Primary collision descriptors at007F4590, stride48 | EXP009 patches five original reads at004AB499,004ABF56,004AC2BD,004AC5B6,004AC883. Publication changes payload+16; stable metadata remains resident. EXP011's census independently identifies four actual published payload fields. | The prototype scans other descriptor payloads as owners, including clones. Retained metadata/trailers have not been generalized to section unload. |
| Player0 and camera65 contacts at0107E000, stride20 | EXP006 separates all64 actor selectors from player/camera. EXP010 keeps player/camera raw pointers pinned. Native movement and wall comparisons cover the repair. | EXP012 validates selected contact64 pickup/local carry/throw/landing against contact2. Arbitrary populations and section persistence remain open. |
| Actor1..64 cached cell+4 | EXP010 stores validated page/offset anchors at0107F200, clears only the covered raw field and restores before004AB1A0/004ACFD0. Full native movement/getter tests cover both image bases. Runtime slots5/6/7 survive missing pages. | This preserves ground identity; actor132-byte and placement28-byte records remain resident. It is not a general actor/item serializer. |
| Unknown contact words | EXP010 retains the predecessor's conservative raw-value pins and all flags/unknown fields. Source and exact patch inverse are guarded. | No speculative field rename or release based on inactivity. |
| Query candidate scratch | EXP009 clears both2048-word lists at the outer frame boundary0040FFCA, after the preceding query/update/render work. Consumption fixtures compare full original collectors. | Do not clear during a query or use this boundary assumption in another caller. |
| Saved registers / active caller stack | EXP009's retirement scan retains numeric in-page roots from the saved frame and bounded active caller stack. EXP008/009 native tests exercise these pins. | This is a conservative selected-frame scan, not exhaustive thread, register, callback or stack-lifetime analysis. |
| CPU renderer submission buffers | EXP004/005 compare actual native vertex/index packets, including36 persistent frames with page unmaps. Submission storage lies outside mesh pages in the covered fixtures. | Direct3D calls are stubbed offline. Unknown driver/callback retention and arbitrary native dispatches remain open. |
| Native .data and used asset arena | EXP011 accounts for all515 EXP010 snapshot matches:8 actual published pointer fields,490 unchanged source-byte windows,14 overlapping native-generated integer-table windows and3 overlaps between established fields. Native0049CFF0 reconstructs all32767 saved table entries. | One snapshot, not all states. Source equality does not prove that no unknown reader could interpret those bytes as a pointer. |
| Other process memory | EXP011 captures75 writable private anonymous VMAs below4GiB after endurance RSS recording.EXP011 classifies4962 of5732 numeric matches. EXP012 adds459 long exact WAV-span windows and one initialized PE span;5422 are classified and310 remain candidates. | Read-only/file-backed/device/shared mappings, host64-bit heaps, encoded pointers and unobserved states remain separate unknowns. |

Evidence owners: [[EXP-20260908-004 - Native terrain page residency]],
[[EXP-20260908-005 - Compact terrain storage and actor selector limits]],
[[EXP-20260908-006 - Native actor and camera contact repair]],
EXP-20260908-008,
EXP-20260908-009,
EXP-20260908-010, and
EXP-20260908-011, and
[[EXP-20260908-012 - High-slot seed interaction and native pool limit]].
Their guarded source/assembly, executable addresses, private receipts and indexed
reports distinguish authored adapters from original PC instructions.

The next release rule must name the actual owner and the boundary at which its
last read completes. If that cannot be proved, retain the owner or relocate its
reference before retirement. Page-allocation bounds alone do not bound native
metadata, items/actors, process RSS, driver memory or wider-world capacities.

EXP012 additionally exposes original0042AA50’s full64-entry pool search cycle.
It is a native capacity/caller-lifetime gate, not evidence that a terrain page
has no consumers. Native allocators remain unchanged; EXP013 budgets two seed callsites. General caller/owner lifetime is still open.


[[EXP-20260908-013 - Seed auxiliary budget and distant carry]] maps both shared64-record allocators0042AA50/0042B020 and125 direct call candidates.
The stalled seed caller0041DA68 is confirmed by native instructions and user stack
return0041DA6D;0041DA90 is the second discarded-return emission. Only those two calls
now defer at the authored8-slot reserve. Original004292C0 collectible handling and
unchecked/persisted return consumers prevent classifying the whole pool as cosmetic
or treating a global null return/eviction as safe. The distant seed interaction
check passes, while actual actor/placement storage remains resident.


[[EXP-20260908-014 - Manual moved-seed page persistence]] adds original-code reset and queue-writer discriminators.0041BD10 resets moved-seed position/state from
placement data;0041C420 rescales already-initialized placement XZ. At0041ED6A the
scheduler writes the active actor queue's terminator but preserves unused suffix
bytes. Ten native prefix cases leave63 old actor pointers after an all-far pass.
The16 recorded queue-base consumers still need lifetime analysis; suffix bytes alone
are not a live-owner census. EXP014 confirms moved-seed position across actual terrain-page absence and return,
including repeat pickup. Actor/placement storage remains resident, so actual section
serialization and full consumer lifetime remain open. Its private growth admission
uses no retained sidecar owner: live partial animations count against free plant
records; rejected/held requests cancel and ordinary native seed updates continue.


EXP-20260908-015 adds a bounded offline representation for the demonstrated detached cold
brown seed, including actor/placement opaque bytes and validated contact anchor.
It rejects enumerated active-queue, selected, carried and occupied-plant roots,
including actor 0's zero byte offset. Captured native queue/pickup and all 64
cached-cell selectors pass at both bases. These are storage/rebinding proofs;
the replay's absent plant/selection roots are synthetic. Unknown slot consumers,
callbacks, renderer retention and the exact native release/publication boundary
remain open. No existing owner is released merely because flags +92 are inactive.


[[EXP-20260908-016 - Manual seed ownership and native scattering]] adds actual cold queue/all20plant/selection/carry captures and twenty native
.data exact-start-address censuses. Cold seed63 appears only in six stale queue
suffix fields in seven cold copies. This is not a release certificate:957 actor
HIGHLOW operands include indexed bases and explicit slot consumers.951 match
exported Ghidra targets and decoded operand offsets; six have only the byte-level
check described in the experiment. Original00415E30 writes slot63 from Flik under
mode0x80 with no queue owner, independently demonstrated at two bases; all20 sampled
live mode bytes have that bit clear. Script00415140's index-derived actors are
another non-pointer identity boundary. Destination-slot policy must cover those
gates before live release/publication. EXP016's successful repeat pickup and136
storage/native-reader cases leave actor storage resident in the live arm.
