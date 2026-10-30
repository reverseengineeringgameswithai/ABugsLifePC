---
type: experiment
id: EXP-20260908-005
date: 2026-09-08
created: 2026-09-08
updated: 2026-10-29
status: bounded-native-prototype
question: How does the native actor initializer assign contact-table selectors, what population does the initialized table admit, and do native DAT fixup and terrain loading accept files with managed geometry removed?
result: 0041C420 walks 64 placements of 28 bytes and 0041C54A assigns selectors 1..N without a bound, but 004A9078..004A908D initializes only slots 0-23 and the camera uses constant slot 16 (0041B30B), so the sixteenth actor aliases the camera and the twenty-fourth is outside the table; DAT fixup 0044BB70 and loader 004A8410 accept placeholder meshes with collision bound before 004A89F8
environment: Offline Unicorn x86 and Python; guarded read-only normal Wine census
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
evidence: [EXP-20260908-003, EXP-20260908-004, EXP-20260908-002]
tags: [experiment, terrain/authoring, re/memory]
---

# Compact terrain storage and actor selector limits

Successor: [[EXP-20260908-006 - Native actor and camera contact repair]] supplies
a guarded 66-record contact profile and archives this packet's superseded source
bytes at their frozen hashes.

This packet discovers a native actor-contact population limit and records how
native DAT fixup and terrain loading behave when managed mesh and collision
payloads are removed from resident files. Frozen evidence index:
`reports/terrain/EXP-20260908-005.json`. Private artifacts named below are under
`work/experiments/EXP-20260908-005/`. All binary/data work uses copies.

## PC confirmed: native contact assignment has a separate population limit

`reference-audit.json` corroborates 28 Ghidra-reported callsites with exact PC
call/thunk instructions: three movement calls, 15 `004ABE00`, one `004AC140`,
seven `004AC460`, one `004AC770`, and one `004ACFD0`. Owning-function resolution
remains Ghidra inference; this is not proof against indirect/unseen consumers.

Original actor initialization `0041C420` walks 64 placements of 28 bytes. A
nonzero type at +12 and flag +18 bit0x20 select a counter initially 1
(`0041C440`). `0041C54A` writes it to placement +25 and increments without a
contact-table bound. `0041DA30` reads that selector for movement. The separate
camera call at `0041B30B` passes constant16, while Flik uses slot0. Spatial
initialization `004A9078–004A908D` initializes only slots0–23.

`native-selectors.json` executes the complete original actor initializer and
native height queries, with original constant bytes at `004C1000..004DD000`.
Synthetic populations 0/1/9/15/16/23/24/64 receive exactly selectors1..N. The
sixteenth assignment aliases camera slot16; the twenty-fourth is outside the
initialized table. `native_actor_selectors` therefore rejects populations above
15 for this unmodified layout. It is an offline admission guard, not an engine
table enlargement, compiler-wide restriction or runtime repair.

The original current creature packet has nine such placements, matching a
guarded read-only census of the normal game. The earlier EXP-002 crowd packet
has **27**, confirmed by actual native initialization of that packet. This is
an uncovered limit in that stress fixture: its recorded twenty-plant loading,
pickup/reuse and hardware route checks remain valid observations, but they do
not prove contact safety for all later seed movements. No new crowd movement
fault is asserted. The current normal nine-selector profile is unchanged.
A larger moving population must repair the table/slot allocation or use an
admitted population, then exercise every affected moving seed and the camera.

Entity initialization also leaves an existing nonzero contact table unchanged in
a native discriminator. Inactive/reinitialized entity state alone is insufficient
authority to clear a contact pin; nonzero contacts must still be treated as live.

## Native loading with placeholder geometry

Test files replace each managed mesh with a small empty placeholder and each
managed collision group with its terminator plus preserved trailer, preserving
native scene/object identities, source IDs/origins, unknown record bytes,
unrelated payloads and trailers, and updating supported offset fields and the
end-relative footer (`packages.json`). Such files are **unplayable
placeholders** on their own.

`native-storage.json` executes original `0044BB70` DAT fixup on both full and
compact files. All 670 current and 688 larger-profile scene/object records
preserve their nonpointer bytes. Native footer roots, the copied 64-dword table
and the opaque `0x11C` header match. This verifies relocation and bounded storage
preservation, not complete footer lifecycle.

`native-compact-harness.py` supplies only compact TERRAIN.ALL to original
`004A8410`; it binds independently verified collision files after that loader
returns and before native bounds/bucket construction at `004A89F8`. The resulting
bucket bytes equal full-source controls. Native high-kind list roots remain within
compact resident source allocations. `native-compact-transitions.json` records
1,750 prescribed movement calls on original and repaired code that match
full-source controls in position, flags, normalized source/cell identity and
instruction count.


## Validation

The focused suite passes 93 tests, including synthetic rejection/unknown-byte
regressions. Selected `make check` passes 1,344 tests in158.09s, with unrelated
R2q/tool suites excluded. This is not an unfiltered whole-repository test run.
No launch, close, external memory write, debugger stop, PS1 consultation or
original modification occurred. Session handoff:
[[2026-09-08 - Codex - Compact terrain pages and native selector limits]].
