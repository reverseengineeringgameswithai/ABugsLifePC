---
type: experiment
id: EXP-20260910-007
date: 2026-09-10
environment: Fedora host, native x86 Unicorn at two PE bases, Wine hardware user playtest
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
question: Which native code draws the first Soil lesson's initial count sign, and what limits throw counts above six?
result: Separate initial-sign function 0043C250 (0043C270 selects ESI=5 for stages 0/1) draws the initial sign independently of the 0043C3C2 boundary; HUD renderer 00410A20 uses an unchecked frame index into the six-frame Training LEVEL1.RAW type 0x26/id 0x33 resource, confirmed in live RAM and the original RAW, so counts above six would index outside it; a five-count edit with a sign hook works live.
status: accepted-bounded
created: 2026-09-10
updated: 2026-10-29
tags: [experiment/tutorial, re/native]
---

# Five-throw Training sign and native defaults

Extends [[EXP-20260910-006 - First Soil throw count boundary proof]]. In a live
run of a target-5 build, the initial sign still showed6 although the five-event
boundary was already correct; this note identifies the separate native sign path
and the limit on counts above six.

## Initial-sign correction

The old proof executed0043C340 and captured its countdown HUD calls; it did not
execute the separate initial-sign function0043C250. Static PC disassembly shows
0043C270 selects ESI=5 for stages0/1 and ESI=2 for stages2/3 before calling
the numeric HUD51 at0043C2BD. That independent constant explains the initial6
despite the already-correct five-event boundary at0043C3C2 and countdown constant
at0043C3CF. The first live report of the mismatch is independent evidence.

A guarded hook at0043C25F replaces `33f683f804`, selects the configured count
minus1 for stages0–3 and resumes0043C275. Other stages retain zero/no numeric
sign as native. The hook keeps exact inverse/relocation guards. No live process
patch or original binary modification.

`tests/test_soil_triggers.py::throw_count_proof` now calls actual0043C250 before
whole native0043C340/countdown execution. Both PE bases prove initial frame4,
countdown frames3,2,1,0 and transition on throw5. All supported1–6 goals retain
N-1/N boundaries. A separate mixed-count test[5,2,6,1] executes initial signs for
all14 stages at both bases, covering independent throw/jump/bounce/seed settings.
The updated probe is private at
`work/experiments/EXP-20260910-007/updated-count-proof.json`; its reused probe
schema still names EXP006. The old tracked EXP006 two-byte report is historical:
current target3/6 builds also differ in the initial-sign table byte.

## Why seven is not currently supported

`reports/soil-triggers/EXP-20260910-007-sign-resource.json` records a read-only
live/static match. HUD renderer00410A20 uses its third parameter as an unchecked
frame index. Live pointer table0076F9B8 entry51, at0076FA84, points to00893F37
in the first user playtest. Header `2000200006000000` describes32×32 pixels,
six frames and no local palette entries. Header plus pixels is6152 bytes.

The exact resource matches original Training `LEVEL07/LEVEL1.RAW` type0x26/id0x33,
compressed packet at file offset314731,1274 bytes, decoded6160 bytes, payload
offset8. RAW SHA256:
`c5f81eed3c9d1a01cc188ead50fc10a5ae0f213b0ca165764fa7b311a02a0926`.
Payload SHA256:
`d6d5df3362e5d2bdf3f98ff6d90e4f0183986bb221f0d4748a360dd2f69e7f55`.
Native type26 loader00465030 publishes this resource. These are original PC
evidence, not PS1 correspondence or a decompiler-derived implementation.

Target7 would require frame6; its pixel offset8+6×1024=6152 is already outside
this bank. Current validation rejects7 before building. No seven-count live run
was attempted, so a specific crash or visible corruption is not asserted.
Supporting larger values requires expanded number graphics and safe indexing.
The six-frame display limit does not prove a six-event action-counter maximum.
Changing a target also does not rewrite the spoken wording in a recording.

## Live check

A corrected target-5 build (EXE SHA256
`831a170bc979297a73c25ad1395f7551049a00a0bac2d09249ba954059e48303`) passed all six
hardware markers; the user played Training directly and reported that the sign
counts 5 -> 0 and the lesson continues properly. Read-only state observes
Training17, lesson1/LESS2, idle stream and inactive policy owner/phase,
consistent with native jumping requirements waiting after the first task. It is
not a continuous input or timing trace. `reports/studio/EXP-20260910-007.json`
retains the native checks and runtime identities. No live memory writes or
process debugger stops.
