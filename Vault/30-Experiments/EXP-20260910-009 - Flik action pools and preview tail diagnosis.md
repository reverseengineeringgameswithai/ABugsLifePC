---
type: experiment
id: EXP-20260910-009
date: 2026-09-10
environment: Fedora, offline Unicorn, Tk, ffplay 8.1.1 and PipeWire
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
question: Which recordings belong to grain, shared-pickup and hurt action events, and how does native code choose among them?
result: Three native pools mapped - ordinary grain (USGN009/010, low-four-bits random gate, suppressed in Training via 00861C84==17), shared pickups (five recordings through 00414CC0(-3), table 004C7678) and nonfatal hurt (five recordings through 0041C821 -> 00414CC0(-1), table 004C7638); repeats fall back to the previously saved slot at 00572C08+ with shared last cue 00572C24
status: accepted-bounded
created: 2026-09-10
updated: 2026-10-29
tags: [experiment/audio, re/native]
---

# Flik action pools and preview tail diagnosis

This extends [[EXP-20260910-005 - Flik event voice mappings]] to the action rules
behind recordings such as grain USGN009/010. It does not change native triggers
or any saved recording. No PS1 evidence.

## Confirmed native action selection

Static original-PC instructions were checked against whole native handler
execution in `scripts/probe-flik-action-events.py`. Retail copy:
`work/copies/BUGS_PC-disc/bugs.exe`, SHA256 in frontmatter. Native bank2 loader
0049E3E0 supplies filenames via the existing 0049DF90 file-load interception.
Actual selection, guards, health/count state and 0041A2B0 cue translation execute;
the final device callback0049D820 is stubbed. Geometry/visual/HUD callbacks are
explicitly listed in the probe. Synthetic pickup/Flik/RNG state is offline only.
No live game memory read/write, input or executable change.

`reports/audio/EXP-20260910-009-native.json` records204 cases at each of PE
bases00400000/01000000, with identical normalized results. Direct harness calls
have a null native callsite rather than an invented address. Cases:96 grain
choice/eligibility,15 grain suppression,64 shared-pickup choice,8 Training
suppression,8 inactive/distant pickup,8 nonfatal hurt,3 hurt guard/fatal controls,
and2 previous-fallback checks. These are request/file proofs, not live listening.

| Event | Recordings | PC authority |
| --- | --- | --- |
| Ordinary grain | USGN009, USGN010 | 00418B90, 00417720/00417CCD, effect004292C0 |
| Shared pickups | USGN050, USGN052, USGN051, USGN028, USGN043 | stored00417720 → 00414CC0(-3), table004C7678 |
| Nonfatal hurt | USGN090, USGN091, USGN108, USGN109, USGN092 | 0041C6C0 → call0041C821 → 00414CC0(-1), table004C7638 |

**Grain:** both inline stored-collectible and helper paths consume a random byte
and require its low four bits to be zero. Engine global00861C84 is compared
with17 to suppress Training.
Outside Training the next random byte &1 selects cues48/49, samples33/34.
Tracked speech query0041A550 must return0; state0059A5B0 must not be2,
flag0059D9A0 bit04 must be absent and blocker00572C20 zero. Final native calls
are00417D73/00418C38. Grain byte0059D9B1 increments even when speech does not
dispatch. Tests execute the whole stored, helper and effect paths. There is no
round-robin/last-cue fallback in these grain branches. Nominal opportunity1/16
assumes uniform random bytes; this is not a measured gameplay frequency.

**Shared pickups:** native stored selectors10–13 (FLIK),20 (blueberry),29/2A/2B
(seed tokens) all reach the same -3 dispatcher, tested individually at all eight
RNG indexes. Selector identities are established in
[[PC original Training Blender mapping]] and its PC-native collectible evidence.
Training returns before consuming the selection byte. Else the next byte &7
indexes cues `[62,63,66,52,58,62,63,66]`. USGN050 is additionally a direct health
response; it must not be relabelled as an exclusively token/letter recording.
This is not an exhaustive census of every -3 caller or of other uses of its WAVs.

**Hurt:** normal damage0041C6C0 decrements the **word** at0059D9A4 and requests
-1 at0041C821 if the resulting signed health is nonnegative. Active positive
invulnerability0059D9A2 or invincibility0059D98E can prevent the decrement/voice;
negative tests retain health and issue no pool sample. The fatal arm calls
cue73 at0041C7E5 (sample58), not the random hurt pool. The hurt table's eight
selected cues are `[67,68,77,78,81,67,68,77]`; Training has no special exclusion
in this pool. Not every upstream damage source is covered.

**Repeat state:** 00414CC0 negative selectors use pool fallback slots00572C08+
4×(-1-selector) and the shared last cue00572C24. If the selected cue equals the
last cue, the **previously saved** fallback is used, not the table's new adjacent
entry. The probe sets a distinct previous fallback to discriminate these cases.
Otherwise the next table entry is saved for a future repeat. State2 and speech
blocker00572C20 can still suppress these pool cues. Weighted table entries and
shared history mean neither a five-item round-robin nor unconditional uniform
per-recording probabilities. These pools do not inherit all hint-helper guards.

## Limits

USGN091 itself is9370 bytes, PCM signed16-bit mono22050Hz,4663 frames:
**0.211473923 seconds**, SHA256
`2356061b5a428ba802e2567a5edffaa46eb5d2d008338b55fe111216438a6d76`; the original
recording really is short. US1A069 “Ant Island” has an unverified action trigger;
do not infer entry/idle/location from wording. Full voice/action and speaker
coverage, exact live frequencies and whole-campaign listening remain open.
